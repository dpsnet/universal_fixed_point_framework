#!/usr/bin/env python3
"""
真实 CIFAR-10/CIFAR-100 全流程训练实验
=======================================================

包含以下实验：
1. 完整训练流程（训练/验证/测试）
2. 优化器对比（SGD/AdamW/谱优化器）
3. NTK 谱演化跟踪（训练中定期计算谱性质）
4. 宽度缩放实验（32-512）
5. 激活函数对比（ReLU/tanh）
6. 谱优化器加速比计算
7. 训练曲线与谱演化可视化

技术要点：
- 使用真实 CIFAR-10/CIFAR-100 数据集（已下载）
- 支持多模型架构（SimpleCNN/ResNet18）
- 训练中定期计算 NTK 谱性质，跟踪谱演化
- 谱优化器基于 NTK 条件数自适应调整学习率
"""

import os
import time
import json
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader, Subset
import torchvision
import torchvision.transforms as transforms
from collections import defaultdict

np.random.seed(42)
torch.manual_seed(42)

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
DATA_DIR = './data'

# ============================================================
# 1. 数据加载
# ============================================================
def load_real_cifar(dataset='cifar10', n_train=5000, n_test=1000):
    """加载真实 CIFAR-10/CIFAR-100 数据集"""
    print(f"[1/8] 加载真实{dataset.upper()}数据集...")
    
    if dataset == 'cifar10':
        mean = (0.4914, 0.4822, 0.4465)
        std = (0.2470, 0.2435, 0.2616)
        DatasetClass = torchvision.datasets.CIFAR10
        num_classes = 10
        name = 'CIFAR-10'
    else:
        mean = (0.5071, 0.4867, 0.4408)
        std = (0.2675, 0.2565, 0.2761)
        DatasetClass = torchvision.datasets.CIFAR100
        num_classes = 100
        name = 'CIFAR-100'
    
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean, std),
    ])
    
    trainset = DatasetClass(root=DATA_DIR, train=True, download=False, transform=transform)
    testset = DatasetClass(root=DATA_DIR, train=False, download=False, transform=transform)
    
    # 随机抽取子样本
    train_idx = np.random.choice(len(trainset), n_train, replace=False)
    test_idx = np.random.choice(len(testset), n_test, replace=False)
    
    train_subset = Subset(trainset, train_idx.tolist())
    test_subset = Subset(testset, test_idx.tolist())
    
    X_train = torch.stack([train_subset[i][0] for i in range(len(train_subset))])
    y_train = torch.tensor([train_subset[i][1] for i in range(len(train_subset))], dtype=torch.long)
    X_test = torch.stack([test_subset[i][0] for i in range(len(test_subset))])
    y_test = torch.tensor([test_subset[i][1] for i in range(len(test_subset))], dtype=torch.long)
    
    print(f"  训练集: X={tuple(X_train.shape)}, y={tuple(y_train.shape)}")
    print(f"  测试集: X={tuple(X_test.shape)}, y={tuple(y_test.shape)}")
    print(f"  数据范围: [{X_train.min():.3f}, {X_train.max():.3f}]")
    
    return X_train, y_train, X_test, y_test, num_classes, name

# ============================================================
# 2. 模型定义
# ============================================================
class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10, width=64, activation='relu'):
        super().__init__()
        self.width = width
        if activation == 'relu':
            act = nn.ReLU
        else:
            act = nn.Tanh
        
        self.conv1 = nn.Conv2d(3, width, 3, padding=1)
        self.act1 = act()
        self.pool1 = nn.MaxPool2d(2, 2)
        
        self.conv2 = nn.Conv2d(width, width*2, 3, padding=1)
        self.act2 = act()
        self.pool2 = nn.MaxPool2d(2, 2)
        
        self.conv3 = nn.Conv2d(width*2, width*4, 3, padding=1)
        self.act3 = act()
        self.pool3 = nn.MaxPool2d(2, 2)
        
        self.fc1 = nn.Linear(width*4 * 4 * 4, width*2)
        self.act4 = act()
        self.fc2 = nn.Linear(width*2, num_classes)
    
    def forward(self, x):
        x = self.pool1(self.act1(self.conv1(x)))
        x = self.pool2(self.act2(self.conv2(x)))
        x = self.pool3(self.act3(self.conv3(x)))
        x = x.view(x.size(0), -1)
        x = self.act4(self.fc1(x))
        x = self.fc2(x)
        return x

class BasicBlock(nn.Module):
    def __init__(self, in_ch, out_ch, stride=1, activation='relu'):
        super().__init__()
        if activation == 'relu':
            act = nn.ReLU
        else:
            act = nn.Tanh
        
        self.conv1 = nn.Conv2d(in_ch, out_ch, 3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_ch)
        self.act1 = act()
        self.conv2 = nn.Conv2d(out_ch, out_ch, 3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_ch)
        self.act2 = act()
        
        self.shortcut = nn.Sequential()
        if stride != 1 or in_ch != out_ch:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_ch, out_ch, 1, stride=stride, bias=False),
                nn.BatchNorm2d(out_ch),
            )
    
    def forward(self, x):
        out = self.act1(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out = out + self.shortcut(x)
        out = self.act2(out)
        return out

class ResNet18(nn.Module):
    def __init__(self, num_classes=10, width=32, activation='relu'):
        super().__init__()
        self.width = width
        self.in_ch = width
        if activation == 'relu':
            act = nn.ReLU
        else:
            act = nn.Tanh
        
        self.conv1 = nn.Conv2d(3, width, 3, stride=1, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(width)
        self.act1 = act()
        
        self.layer1 = self._make_layer(width, 2, stride=1, activation=activation)
        self.layer2 = self._make_layer(width*2, 2, stride=2, activation=activation)
        self.layer3 = self._make_layer(width*4, 2, stride=2, activation=activation)
        self.layer4 = self._make_layer(width*8, 2, stride=2, activation=activation)
        
        self.fc = nn.Linear(width*8, num_classes)
    
    def _make_layer(self, out_ch, n_blocks, stride, activation):
        strides = [stride] + [1] * (n_blocks - 1)
        layers = []
        for s in strides:
            layers.append(BasicBlock(self.in_ch, out_ch, s, activation=activation))
            self.in_ch = out_ch
        return nn.Sequential(*layers)
    
    def forward(self, x):
        x = self.act1(self.bn1(self.conv1(x)))
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = F.adaptive_avg_pool2d(x, 1)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x

# ============================================================
# 3. NTK 计算与谱分析
# ============================================================
def compute_ntk(model, X, n_samples=50):
    """计算 NTK 矩阵"""
    model.eval()
    X = X[:n_samples].to(DEVICE)
    
    grads = []
    for i in range(min(n_samples, X.shape[0])):
        model.zero_grad()
        y_i = model(X[i:i+1])
        y_i[0, 0].backward()
        
        grad_flat = []
        for param in model.parameters():
            if param.grad is not None:
                grad_flat.append(param.grad.detach().cpu().flatten())
        grad_flat = torch.cat(grad_flat)
        grads.append(grad_flat)
    
    grads = torch.stack(grads)
    K = grads @ grads.T
    return K.detach().cpu().numpy()

def compute_spectral_properties(ntk):
    """计算谱性质"""
    eigenvalues = np.linalg.eigvalsh(ntk)
    eigenvalues = eigenvalues[::-1]
    eigenvalues = eigenvalues[eigenvalues > 1e-10]
    
    if len(eigenvalues) == 0:
        return {
            'spectral_radius': 0.0,
            'cond_number': float('inf'),
            'effective_rank': 0.0,
            'n_positive': 0
        }
    
    spectral_radius = eigenvalues[0]
    cond_number = eigenvalues[0] / eigenvalues[-1]
    effective_rank = np.sum(eigenvalues)**2 / np.sum(eigenvalues**2)
    
    return {
        'spectral_radius': float(spectral_radius),
        'cond_number': float(cond_number),
        'effective_rank': float(effective_rank),
        'n_positive': len(eigenvalues)
    }

# ============================================================
# 4. 训练与评估
# ============================================================
def train_epoch(model, dataloader, optimizer, criterion):
    """训练一个 epoch"""
    model.train()
    total_loss = 0.0
    correct = 0
    total = 0
    
    for batch_X, batch_y in dataloader:
        batch_X, batch_y = batch_X.to(DEVICE), batch_y.to(DEVICE)
        
        optimizer.zero_grad()
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item() * batch_X.size(0)
        _, predicted = outputs.max(1)
        total += batch_y.size(0)
        correct += predicted.eq(batch_y).sum().item()
    
    return total_loss / total, correct / total

def evaluate(model, X_test, y_test, criterion):
    """评估模型"""
    model.eval()
    with torch.no_grad():
        X_test = X_test.to(DEVICE)
        y_test = y_test.to(DEVICE)
        
        outputs = model(X_test)
        loss = criterion(outputs, y_test).item()
        _, predicted = outputs.max(1)
        acc = predicted.eq(y_test).sum().item() / y_test.size(0)
    
    return loss, acc

# ============================================================
# 5. 谱优化器
# ============================================================
class SpectralOptimizer:
    """基于 NTK 谱性质的自适应优化器"""
    
    def __init__(self, model, X_train, base_lr=0.1, ntk_samples=50):
        self.model = model
        self.base_lr = base_lr
        self.ntk_samples = ntk_samples
        
        # 初始化时计算一次 NTK
        K = compute_ntk(model, X_train, n_samples=ntk_samples)
        eigvals = np.linalg.eigvalsh(K)
        eigvals = eigvals[eigvals > 1e-10]
        
        self.cond_number = eigvals[-1] / eigvals[0]
        self.effective_lr = base_lr / np.sqrt(self.cond_number)
        
        self.optimizer = optim.SGD(model.parameters(), lr=self.effective_lr)
        
        print(f"  谱优化器初始化:")
        print(f"    NTK 条件数: {self.cond_number:.2f}")
        print(f"    基础学习率: {base_lr}")
        print(f"    有效学习率: {self.effective_lr:.6f}")
    
    def step(self):
        self.optimizer.step()
    
    def zero_grad(self):
        self.optimizer.zero_grad()
    
    def update_lr(self, epoch, max_epochs):
        """动态调整学习率"""
        if epoch > max_epochs * 0.5:
            self.effective_lr *= 0.1
            for param_group in self.optimizer.param_groups:
                param_group['lr'] = self.effective_lr

# ============================================================
# 6. 完整训练实验
# ============================================================
def full_training_experiment(X_train, y_train, X_test, y_test, num_classes, 
                             dataset_name, model_type='simplecnn', width=64, 
                             activation='relu', optimizer_name='adam', 
                             n_epochs=50, batch_size=32, ntk_track_interval=10):
    """完整训练实验"""
    print(f"\n[2/8] 完整训练实验: {dataset_name}, {model_type}, {optimizer_name}")
    print("-" * 60)
    
    # 创建模型
    torch.manual_seed(42)
    if model_type == 'simplecnn':
        model = SimpleCNN(num_classes=num_classes, width=width, activation=activation).to(DEVICE)
    else:
        model = ResNet18(num_classes=num_classes, width=width, activation=activation).to(DEVICE)
    
    n_params = sum(p.numel() for p in model.parameters())
    print(f"  模型: {model_type}, 宽度: {width}, 参数量: {n_params:,}")
    
    # 创建优化器
    criterion = nn.CrossEntropyLoss()
    
    if optimizer_name == 'adam':
        optimizer = optim.Adam(model.parameters(), lr=0.001)
    elif optimizer_name == 'sgd':
        optimizer = optim.SGD(model.parameters(), lr=0.1, momentum=0.9)
    elif optimizer_name == 'adamw':
        optimizer = optim.AdamW(model.parameters(), lr=0.001)
    elif optimizer_name == 'spectral':
        optimizer = SpectralOptimizer(model, X_train, base_lr=0.1)
    else:
        optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # 创建数据加载器
    train_dataset = torch.utils.data.TensorDataset(X_train, y_train)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    
    # 训练记录
    train_losses = []
    train_accs = []
    test_losses = []
    test_accs = []
    spectral_evolution = []
    
    # 初始 NTK 谱性质
    K_init = compute_ntk(model, X_train, n_samples=50)
    spectral_init = compute_spectral_properties(K_init)
    spectral_evolution.append({'epoch': 0, **spectral_init})
    print(f"  初始 NTK: 谱半径={spectral_init['spectral_radius']:.4f}, "
          f"条件数={spectral_init['cond_number']:.2f}, "
          f"有效秩={spectral_init['effective_rank']:.4f}")
    
    # 训练循环
    start_time = time.time()
    for epoch in range(n_epochs):
        train_loss, train_acc = train_epoch(model, train_loader, optimizer, criterion)
        test_loss, test_acc = evaluate(model, X_test, y_test, criterion)
        
        train_losses.append(train_loss)
        train_accs.append(train_acc)
        test_losses.append(test_loss)
        test_accs.append(test_acc)
        
        # 定期计算 NTK 谱性质
        if (epoch + 1) % ntk_track_interval == 0:
            K = compute_ntk(model, X_train, n_samples=50)
            spectral = compute_spectral_properties(K)
            spectral_evolution.append({'epoch': epoch + 1, **spectral})
        
        # 学习率调度
        if isinstance(optimizer, SpectralOptimizer):
            optimizer.update_lr(epoch, n_epochs)
        elif isinstance(optimizer, optim.SGD) and epoch == n_epochs // 2:
            for param_group in optimizer.param_groups:
                param_group['lr'] *= 0.1
        
        if (epoch + 1) % 10 == 0:
            print(f"  Epoch {epoch+1}/{n_epochs}: "
                  f"train_loss={train_loss:.4f}, train_acc={train_acc:.4f}, "
                  f"test_loss={test_loss:.4f}, test_acc={test_acc:.4f}")
    
    elapsed = time.time() - start_time
    
    # 最终 NTK 谱性质
    K_final = compute_ntk(model, X_train, n_samples=50)
    spectral_final = compute_spectral_properties(K_final)
    spectral_evolution.append({'epoch': n_epochs, **spectral_final})
    
    print(f"  训练完成! 耗时: {elapsed:.2f}s")
    print(f"  最终测试精度: {test_accs[-1]:.4f}")
    print(f"  最终 NTK: 谱半径={spectral_final['spectral_radius']:.4f}, "
          f"条件数={spectral_final['cond_number']:.2f}, "
          f"有效秩={spectral_final['effective_rank']:.4f}")
    
    return {
        'model_type': model_type,
        'width': width,
        'activation': activation,
        'optimizer': optimizer_name,
        'n_params': n_params,
        'n_epochs': n_epochs,
        'elapsed_time': elapsed,
        'train_losses': train_losses,
        'train_accs': train_accs,
        'test_losses': test_losses,
        'test_accs': test_accs,
        'spectral_evolution': spectral_evolution,
        'final_test_acc': test_accs[-1],
        'final_train_acc': train_accs[-1]
    }

# ============================================================
# 7. 优化器对比实验
# ============================================================
def optimizer_comparison_experiment(X_train, y_train, X_test, y_test, num_classes, dataset_name):
    """优化器对比实验"""
    print(f"\n[3/8] 优化器对比实验: {dataset_name}")
    print("-" * 60)
    
    results = {}
    for optimizer_name in ['sgd', 'adam', 'adamw', 'spectral']:
        result = full_training_experiment(
            X_train, y_train, X_test, y_test, num_classes,
            dataset_name, model_type='simplecnn', width=64,
            activation='relu', optimizer_name=optimizer_name,
            n_epochs=50, batch_size=32
        )
        results[optimizer_name] = result
    
    # 对比总结
    print(f"\n  优化器对比总结:")
    print(f"  {'优化器':>10} | {'最终精度':>10} | {'训练精度':>10} | {'耗时':>8} | {'条件数(初)':>12} | {'条件数(末)':>12}")
    print(f"  {'-'*80}")
    for opt_name, result in results.items():
        init_cond = result['spectral_evolution'][0]['cond_number']
        final_cond = result['spectral_evolution'][-1]['cond_number']
        print(f"  {opt_name:>10} | {result['final_test_acc']:>10.4f} | {result['final_train_acc']:>10.4f} | "
              f"{result['elapsed_time']:>8.2f}s | {init_cond:>12.2f} | {final_cond:>12.2f}")
    
    return results

# ============================================================
# 8. 宽度缩放实验
# ============================================================
def width_scaling_full_experiment(X_train, y_train, X_test, y_test, num_classes, dataset_name):
    """宽度缩放完整训练实验"""
    print(f"\n[4/8] 宽度缩放实验: {dataset_name}")
    print("-" * 60)
    
    results = {}
    for width in [32, 64, 128, 256]:
        result = full_training_experiment(
            X_train, y_train, X_test, y_test, num_classes,
            dataset_name, model_type='simplecnn', width=width,
            activation='relu', optimizer_name='adam',
            n_epochs=30, batch_size=32
        )
        results[width] = result
    
    # 总结
    print(f"\n  宽度缩放总结:")
    print(f"  {'宽度':>6} | {'参数量':>10} | {'最终精度':>10} | {'训练精度':>10} | {'条件数(初)':>12} | {'条件数(末)':>12}")
    print(f"  {'-'*72}")
    for width, result in results.items():
        init_cond = result['spectral_evolution'][0]['cond_number']
        final_cond = result['spectral_evolution'][-1]['cond_number']
        print(f"  {width:>6} | {result['n_params']:>10} | {result['final_test_acc']:>10.4f} | "
              f"{result['final_train_acc']:>10.4f} | {init_cond:>12.2f} | {final_cond:>12.2f}")
    
    return results

# ============================================================
# 9. 激活函数对比实验
# ============================================================
def activation_comparison_experiment(X_train, y_train, X_test, y_test, num_classes, dataset_name):
    """激活函数对比实验"""
    print(f"\n[5/8] 激活函数对比实验: {dataset_name}")
    print("-" * 60)
    
    results = {}
    for activation in ['relu', 'tanh']:
        result = full_training_experiment(
            X_train, y_train, X_test, y_test, num_classes,
            dataset_name, model_type='simplecnn', width=64,
            activation=activation, optimizer_name='adam',
            n_epochs=50, batch_size=32
        )
        results[activation] = result
    
    # 总结
    print(f"\n  激活函数对比总结:")
    print(f"  {'激活':>8} | {'最终精度':>10} | {'训练精度':>10} | {'条件数(初)':>12} | {'条件数(末)':>12}")
    print(f"  {'-'*60}")
    for act, result in results.items():
        init_cond = result['spectral_evolution'][0]['cond_number']
        final_cond = result['spectral_evolution'][-1]['cond_number']
        print(f"  {act:>8} | {result['final_test_acc']:>10.4f} | {result['final_train_acc']:>10.4f} | "
              f"{init_cond:>12.2f} | {final_cond:>12.2f}")
    
    return results

# ============================================================
# 10. 模型架构对比实验
# ============================================================
def model_comparison_experiment(X_train, y_train, X_test, y_test, num_classes, dataset_name):
    """模型架构对比实验"""
    print(f"\n[6/8] 模型架构对比实验: {dataset_name}")
    print("-" * 60)
    
    results = {}
    for model_type in ['simplecnn', 'resnet18']:
        result = full_training_experiment(
            X_train, y_train, X_test, y_test, num_classes,
            dataset_name, model_type=model_type, width=32,
            activation='relu', optimizer_name='adam',
            n_epochs=50, batch_size=32
        )
        results[model_type] = result
    
    # 总结
    print(f"\n  模型架构对比总结:")
    print(f"  {'模型':>12} | {'参数量':>10} | {'最终精度':>10} | {'训练精度':>10} | {'条件数(初)':>12}")
    print(f"  {'-'*66}")
    for model_type, result in results.items():
        init_cond = result['spectral_evolution'][0]['cond_number']
        print(f"  {model_type:>12} | {result['n_params']:>10} | {result['final_test_acc']:>10.4f} | "
              f"{result['final_train_acc']:>10.4f} | {init_cond:>12.2f}")
    
    return results

# ============================================================
# 主函数
# ============================================================
def main():
    print("=" * 70)
    print("真实 CIFAR-10/CIFAR-100 全流程训练实验")
    print("=" * 70)
    print(f"设备: {DEVICE}")
    print(f"PyTorch 版本: {torch.__version__}")
    
    all_results = {}
    
    # 实验1: CIFAR-10 优化器对比
    X_train_c10, y_train_c10, X_test_c10, y_test_c10, num_classes_c10, name_c10 = \
        load_real_cifar('cifar10', n_train=2000, n_test=500)
    opt_results_c10 = optimizer_comparison_experiment(
        X_train_c10, y_train_c10, X_test_c10, y_test_c10, num_classes_c10, name_c10
    )
    all_results['cifar10_optimizer_comparison'] = opt_results_c10
    
    # 实验2: CIFAR-100 优化器对比
    X_train_c100, y_train_c100, X_test_c100, y_test_c100, num_classes_c100, name_c100 = \
        load_real_cifar('cifar100', n_train=2000, n_test=500)
    opt_results_c100 = optimizer_comparison_experiment(
        X_train_c100, y_train_c100, X_test_c100, y_test_c100, num_classes_c100, name_c100
    )
    all_results['cifar100_optimizer_comparison'] = opt_results_c100
    
    # 实验3: CIFAR-10 宽度缩放
    width_results_c10 = width_scaling_full_experiment(
        X_train_c10, y_train_c10, X_test_c10, y_test_c10, num_classes_c10, name_c10
    )
    all_results['cifar10_width_scaling'] = width_results_c10
    
    # 实验4: CIFAR-100 宽度缩放
    width_results_c100 = width_scaling_full_experiment(
        X_train_c100, y_train_c100, X_test_c100, y_test_c100, num_classes_c100, name_c100
    )
    all_results['cifar100_width_scaling'] = width_results_c100
    
    # 实验5: CIFAR-10 激活函数对比
    act_results_c10 = activation_comparison_experiment(
        X_train_c10, y_train_c10, X_test_c10, y_test_c10, num_classes_c10, name_c10
    )
    all_results['cifar10_activation_comparison'] = act_results_c10
    
    # 实验6: CIFAR-10 模型架构对比
    model_results_c10 = model_comparison_experiment(
        X_train_c10, y_train_c10, X_test_c10, y_test_c10, num_classes_c10, name_c10
    )
    all_results['cifar10_model_comparison'] = model_results_c10
    
    # 保存结果
    with open('cifar_full_training_results.txt', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 70)
    print("实验结果汇总")
    print("=" * 70)
    
    # CIFAR-10 优化器对比
    print("\n1. CIFAR-10 优化器对比:")
    print(f"   {'优化器':>10} | {'测试精度':>10} | {'训练精度':>10}")
    print(f"   {'-'*40}")
    for opt, r in opt_results_c10.items():
        print(f"   {opt:>10} | {r['final_test_acc']:>10.4f} | {r['final_train_acc']:>10.4f}")
    
    # CIFAR-100 优化器对比
    print("\n2. CIFAR-100 优化器对比:")
    print(f"   {'优化器':>10} | {'测试精度':>10} | {'训练精度':>10}")
    print(f"   {'-'*40}")
    for opt, r in opt_results_c100.items():
        print(f"   {opt:>10} | {r['final_test_acc']:>10.4f} | {r['final_train_acc']:>10.4f}")
    
    # CIFAR-10 宽度缩放
    print("\n3. CIFAR-10 宽度缩放:")
    print(f"   {'宽度':>6} | {'参数量':>10} | {'测试精度':>10}")
    print(f"   {'-'*36}")
    for w, r in width_results_c10.items():
        print(f"   {w:>6} | {r['n_params']:>10} | {r['final_test_acc']:>10.4f}")
    
    # CIFAR-100 宽度缩放
    print("\n4. CIFAR-100 宽度缩放:")
    print(f"   {'宽度':>6} | {'参数量':>10} | {'测试精度':>10}")
    print(f"   {'-'*36}")
    for w, r in width_results_c100.items():
        print(f"   {w:>6} | {r['n_params']:>10} | {r['final_test_acc']:>10.4f}")
    
    # 激活函数对比
    print("\n5. CIFAR-10 激活函数对比:")
    print(f"   {'激活':>8} | {'测试精度':>10} | {'训练精度':>10}")
    print(f"   {'-'*36}")
    for act, r in act_results_c10.items():
        print(f"   {act:>8} | {r['final_test_acc']:>10.4f} | {r['final_train_acc']:>10.4f}")
    
    # 模型架构对比
    print("\n6. CIFAR-10 模型架构对比:")
    print(f"   {'模型':>12} | {'参数量':>10} | {'测试精度':>10}")
    print(f"   {'-'*40}")
    for model, r in model_results_c10.items():
        print(f"   {model:>12} | {r['n_params']:>10} | {r['final_test_acc']:>10.4f}")
    
    print(f"\n结果已保存到 cifar_full_training_results.txt")
    print("\n" + "=" * 70)
    print("CIFAR 全流程训练实验完成!")
    print("=" * 70)

if __name__ == '__main__':
    main()