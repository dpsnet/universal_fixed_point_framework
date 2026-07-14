#!/usr/bin/env python3
"""
改进版谱优化器 v2.0
=======================================================

针对小样本CIFAR、NLI任务的谱优化器适配策略改进：

改进策略：
1. 学习率预热机制（warmup）- 解决初始学习率过高问题
2. NTK条件数动态反馈 - 根据实时条件数调整学习率
3. 梯度裁剪 - 防止梯度爆炸
4. 学习率余弦退火 - 后期稳定收敛
5. 自适应动量 - 根据训练进度调整动量
6. 正则化策略增强 - 权重衰减、Dropout

目标：
- CIFAR小样本：精度提升至>45%
- NLI任务：精度超越Adam（>40%）
"""

import os
import time
import json
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from collections import defaultdict

np.random.seed(42)
torch.manual_seed(42)

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# ============================================================
# 改进版谱优化器 v2.0
# ============================================================
class SpectralOptimizerV2(optim.Optimizer):
    """改进版谱优化器 v2.0"""
    
    def __init__(self, params, lr=0.1, ntk_update_freq=5, 
                 warmup_steps=50, cosine_annealing=True,
                 momentum=0.9, adaptive_momentum=True,
                 weight_decay=0.01, grad_clip=1.0,
                 lr_scaling_factor=0.1):
        defaults = dict(
            lr=lr,
            ntk_update_freq=ntk_update_freq,
            warmup_steps=warmup_steps,
            cosine_annealing=cosine_annealing,
            momentum=momentum,
            adaptive_momentum=adaptive_momentum,
            weight_decay=weight_decay,
            grad_clip=grad_clip,
            lr_scaling_factor=lr_scaling_factor
        )
        super(SpectralOptimizerV2, self).__init__(params, defaults)
        self.step_count = 0
        self.ntk_condition_number = 1.0
        self.warmup_progress = 0.0
    
    def set_condition_number(self, cond_number):
        """设置NTK条件数"""
        self.ntk_condition_number = cond_number
    
    def get_current_lr(self, base_lr):
        """计算当前学习率（预热+余弦退火+条件数缩放）"""
        lr = base_lr
        
        # 学习率预热
        if self.step_count < self.defaults['warmup_steps']:
            self.warmup_progress = self.step_count / self.defaults['warmup_steps']
            lr *= self.warmup_progress
        else:
            self.warmup_progress = 1.0
        
        # 余弦退火
        if self.defaults['cosine_annealing'] and self.step_count >= self.defaults['warmup_steps']:
            total_steps = 1000  
            progress = (self.step_count - self.defaults['warmup_steps']) / total_steps
            lr *= 0.5 * (1 + np.cos(np.pi * progress))
        
        # 基于NTK条件数的自适应缩放
        if self.ntk_condition_number > 1:
            lr *= self.defaults['lr_scaling_factor'] / np.sqrt(self.ntk_condition_number)
        
        return max(lr, 1e-7)
    
    def get_current_momentum(self):
        """计算当前动量（自适应调整）"""
        momentum = self.defaults['momentum']
        
        # 预热阶段降低动量
        if self.defaults['adaptive_momentum']:
            momentum *= self.warmup_progress
        
        return momentum
    
    def step(self, closure=None):
        """优化步骤"""
        loss = None
        if closure is not None:
            loss = closure()
        
        self.step_count += 1
        
        for group in self.param_groups:
            base_lr = group['lr']
            current_lr = self.get_current_lr(base_lr)
            current_momentum = self.get_current_momentum()
            
            for p in group['params']:
                if p.grad is None:
                    continue
                
                grad = p.grad.data
                
                # 梯度裁剪
                if group['grad_clip'] > 0:
                    grad = grad.clamp(-group['grad_clip'], group['grad_clip'])
                
                # 权重衰减
                if group['weight_decay'] != 0:
                    grad.add_(group['weight_decay'], p.data)
                
                # 动量
                if current_momentum != 0:
                    param_state = self.state[p]
                    if 'momentum_buffer' not in param_state:
                        buf = param_state['momentum_buffer'] = torch.clone(grad).detach()
                    else:
                        buf = param_state['momentum_buffer']
                        buf.mul_(current_momentum).add_(grad)
                    grad = buf
                
                p.data.add_(grad, alpha=-current_lr)
        
        return loss

# ============================================================
# NTK谱计算模块
# ============================================================
class NTKSpectralAnalyzer:
    """NTK谱分析器"""
    
    def __init__(self):
        pass
    
    def compute_ntk_spectral_properties(self, model, X, n_samples=20):
        """计算NTK谱性质"""
        try:
            model.eval()
            X = X[:n_samples].to(DEVICE)
            
            grads = []
            for i in range(min(n_samples, X.shape[0])):
                model.zero_grad()
                y_i = model(X[i:i+1])
                y_i_sum = y_i[0, 0].sum() if y_i[0, 0].dim() > 0 else y_i[0, 0]
                y_i_sum.backward()
                
                grad_flat = []
                for param in model.parameters():
                    if param.grad is not None:
                        grad_flat.append(param.grad.detach().cpu().flatten())
                grad_flat = torch.cat(grad_flat)
                grads.append(grad_flat)
            
            grads = torch.stack(grads)
            K = grads @ grads.T
            K_np = K.detach().cpu().numpy()
            
            K_np = (K_np + K_np.T) / 2
            K_np += np.eye(K_np.shape[0]) * 1e-10
            
            eigenvalues = np.linalg.eigvalsh(K_np)
            eigenvalues = eigenvalues[::-1]
            eigenvalues = eigenvalues[eigenvalues > 1e-10]
            
            spectral_radius = float(eigenvalues[0]) if len(eigenvalues) > 0 else 0
            cond_number = float(eigenvalues[0] / eigenvalues[-1]) if len(eigenvalues) > 1 else 1
            effective_rank = float(np.sum(eigenvalues) / eigenvalues[0]) if len(eigenvalues) > 0 else 0
            
            return {
                'spectral_radius': spectral_radius,
                'cond_number': cond_number,
                'effective_rank': effective_rank,
                'n_positive': len(eigenvalues)
            }
        except Exception as e:
            print(f"  NTK谱计算失败: {e}")
            return {
                'spectral_radius': 0.0,
                'cond_number': 1.0,
                'effective_rank': 0.0,
                'n_positive': 0
            }

# ============================================================
# CNN模型
# ============================================================
class SimpleCNN(nn.Module):
    """SimpleCNN模型"""
    
    def __init__(self, n_classes=10, width=64, dropout_rate=0.3):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, width, 3, padding=1)
        self.bn1 = nn.BatchNorm2d(width)
        self.conv2 = nn.Conv2d(width, width*2, 3, padding=1)
        self.bn2 = nn.BatchNorm2d(width*2)
        self.conv3 = nn.Conv2d(width*2, width*4, 3, padding=1)
        self.bn3 = nn.BatchNorm2d(width*4)
        self.pool = nn.MaxPool2d(2, 2)
        self.dropout = nn.Dropout(dropout_rate)
        self.fc1 = nn.Linear(width*4 * 4 * 4, 256)
        self.fc2 = nn.Linear(256, n_classes)
    
    def forward(self, x):
        x = self.pool(F.relu(self.bn1(self.conv1(x))))
        x = self.pool(F.relu(self.bn2(self.conv2(x))))
        x = self.pool(F.relu(self.bn3(self.conv3(x))))
        x = x.view(-1, self.fc1.in_features)
        x = self.dropout(F.relu(self.fc1(x)))
        x = self.fc2(x)
        return x

# ============================================================
# NLI模型
# ============================================================
class NLIModel(nn.Module):
    """NLI模型"""
    
    def __init__(self, n_features=64, n_classes=3, dropout_rate=0.3):
        super(NLIModel, self).__init__()
        self.fc1 = nn.Linear(n_features, 128)
        self.bn1 = nn.BatchNorm1d(128)
        self.fc2 = nn.Linear(128, 64)
        self.bn2 = nn.BatchNorm1d(64)
        self.fc3 = nn.Linear(64, n_classes)
        self.dropout = nn.Dropout(dropout_rate)
    
    def forward(self, x):
        x = self.dropout(F.relu(self.bn1(self.fc1(x))))
        x = self.dropout(F.relu(self.bn2(self.fc2(x))))
        x = self.fc3(x)
        return x

# ============================================================
# 训练框架
# ============================================================
class Trainer:
    """训练框架"""
    
    def __init__(self):
        self.ntk_analyzer = NTKSpectralAnalyzer()
    
    def create_optimizer(self, model, optimizer_name, lr=0.1):
        """创建优化器"""
        if optimizer_name == 'adam':
            return optim.Adam(model.parameters(), lr=0.001, weight_decay=0.01)
        elif optimizer_name == 'adamw':
            return optim.AdamW(model.parameters(), lr=0.001, weight_decay=0.01)
        elif optimizer_name == 'sgd':
            return optim.SGD(model.parameters(), lr=0.1, momentum=0.9, weight_decay=0.01)
        elif optimizer_name == 'spectral_v1':
            return SpectralOptimizerV2(
                model.parameters(),
                lr=lr,
                ntk_update_freq=5,
                warmup_steps=20,
                cosine_annealing=True,
                momentum=0.9,
                adaptive_momentum=True,
                weight_decay=0.01,
                grad_clip=5.0,
                lr_scaling_factor=0.5
            )
        elif optimizer_name == 'spectral_v2':
            return SpectralOptimizerV2(
                model.parameters(),
                lr=lr,
                ntk_update_freq=3,
                warmup_steps=50,
                cosine_annealing=True,
                momentum=0.95,
                adaptive_momentum=True,
                weight_decay=0.001,
                grad_clip=1.0,
                lr_scaling_factor=1.0
            )
        else:
            return optim.Adam(model.parameters(), lr=0.001)
    
    def train_model(self, model, X_train, y_train, X_test, y_test, 
                    optimizer_name, n_epochs=100, batch_size=32):
        """训练模型"""
        criterion = nn.CrossEntropyLoss()
        optimizer = self.create_optimizer(model, optimizer_name)
        
        train_loader = DataLoader(TensorDataset(X_train, y_train), 
                                 batch_size=batch_size, shuffle=True)
        test_loader = DataLoader(TensorDataset(X_test, y_test), 
                                batch_size=batch_size)
        
        results = {
            'optimizer': optimizer_name,
            'n_epochs': n_epochs,
            'train_losses': [],
            'train_accs': [],
            'test_losses': [],
            'test_accs': [],
            'spectral_evolution': [],
            'lr_evolution': []
        }
        
        start_time = time.time()
        
        for epoch in range(n_epochs):
            model.train()
            train_loss = 0
            train_correct = 0
            
            for X_batch, y_batch in train_loader:
                X_batch, y_batch = X_batch.to(DEVICE), y_batch.to(DEVICE)
                
                optimizer.zero_grad()
                outputs = model(X_batch)
                loss = criterion(outputs, y_batch)
                loss.backward()
                optimizer.step()
                
                train_loss += loss.item() * X_batch.size(0)
                train_correct += (outputs.argmax(1) == y_batch).sum().item()
            
            train_loss /= len(train_loader.dataset)
            train_acc = train_correct / len(train_loader.dataset)
            
            model.eval()
            test_loss = 0
            test_correct = 0
            
            with torch.no_grad():
                for X_batch, y_batch in test_loader:
                    X_batch, y_batch = X_batch.to(DEVICE), y_batch.to(DEVICE)
                    outputs = model(X_batch)
                    loss = criterion(outputs, y_batch)
                    test_loss += loss.item() * X_batch.size(0)
                    test_correct += (outputs.argmax(1) == y_batch).sum().item()
            
            test_loss /= len(test_loader.dataset)
            test_acc = test_correct / len(test_loader.dataset)
            
            results['train_losses'].append(train_loss)
            results['train_accs'].append(train_acc)
            results['test_losses'].append(test_loss)
            results['test_accs'].append(test_acc)
            
            if epoch % 5 == 0 or epoch == n_epochs - 1:
                spectral_prop = self.ntk_analyzer.compute_ntk_spectral_properties(model, X_train)
                results['spectral_evolution'].append({
                    'epoch': epoch,
                    **spectral_prop
                })
                
                if hasattr(optimizer, 'set_condition_number'):
                    optimizer.set_condition_number(spectral_prop['cond_number'])
                
                if hasattr(optimizer, 'get_current_lr'):
                    lr_val = optimizer.get_current_lr(optimizer.defaults['lr'])
                    results['lr_evolution'].append({'epoch': epoch, 'lr': lr_val})
            
            if epoch % 10 == 0:
                print(f"  Epoch {epoch}/{n_epochs}: train_loss={train_loss:.4f}, "
                      f"train_acc={train_acc:.4f}, test_loss={test_loss:.4f}, "
                      f"test_acc={test_acc:.4f}")
        
        results['elapsed_time'] = time.time() - start_time
        results['final_test_acc'] = test_acc
        results['final_train_acc'] = train_acc
        
        return results

# ============================================================
# 主函数
# ============================================================
def main():
    print("=" * 70)
    print("改进版谱优化器 v2.0 - 小样本任务测试")
    print("=" * 70)
    print(f"设备: {DEVICE}")
    print(f"PyTorch 版本: {torch.__version__}")
    
    all_results = {}
    trainer = Trainer()
    
    # 1. CIFAR-10小样本测试
    print("\n[1/2] CIFAR-10小样本测试（500训练样本）...")
    import torchvision
    import torchvision.transforms as transforms
    
    transform = transforms.Compose([
        transforms.RandomCrop(32, padding=4),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2470, 0.2435, 0.2616))
    ])
    
    trainset = torchvision.datasets.CIFAR10(root='./data', train=True, 
                                           download=True, transform=transform)
    testset = torchvision.datasets.CIFAR10(root='./data', train=False, 
                                          download=True, transform=transform)
    
    n_samples = 500
    X_train = torch.stack([trainset[i][0] for i in range(n_samples)])
    y_train = torch.tensor([trainset[i][1] for i in range(n_samples)])
    
    X_test = torch.stack([testset[i][0] for i in range(100)])
    y_test = torch.tensor([testset[i][1] for i in range(100)])
    
    cifar_results = {}
    for optimizer_name in ['adam', 'adamw', 'sgd', 'spectral_v1', 'spectral_v2']:
        print(f"\n  CIFAR-10 {optimizer_name}:")
        model = SimpleCNN(n_classes=10, width=64, dropout_rate=0.3).to(DEVICE)
        result = trainer.train_model(model, X_train, y_train, X_test, y_test, 
                                    optimizer_name, n_epochs=100)
        cifar_results[optimizer_name] = result
        print(f"  最终测试精度: {result['final_test_acc']:.4f}")
    
    all_results['cifar_small_sample'] = cifar_results
    
    # 2. NLI小样本测试
    print("\n[2/2] NLI小样本测试（500训练样本）...")
    
    n_features = 64
    n_classes = 3
    
    X_train = torch.randn(500, n_features)
    y_train = torch.randint(0, n_classes, (500,))
    
    X_test = torch.randn(100, n_features)
    y_test = torch.randint(0, n_classes, (100,))
    
    nli_results = {}
    for optimizer_name in ['adam', 'adamw', 'sgd', 'spectral_v1', 'spectral_v2']:
        print(f"\n  NLI {optimizer_name}:")
        model = NLIModel(n_features=n_features, n_classes=n_classes, dropout_rate=0.3).to(DEVICE)
        result = trainer.train_model(model, X_train, y_train, X_test, y_test, 
                                    optimizer_name, n_epochs=100)
        nli_results[optimizer_name] = result
        print(f"  最终测试精度: {result['final_test_acc']:.4f}")
    
    all_results['nli_small_sample'] = nli_results
    
    # 保存结果
    with open('improved_spectral_optimizer_results.txt', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 70)
    print("改进版谱优化器测试完成!")
    print("=" * 70)
    print("结果已保存到 improved_spectral_optimizer_results.txt")
    
    # 输出总结
    print("\n=== 实验结果总结 ===")
    print("\nCIFAR-10小样本（500训练样本）:")
    for opt, res in cifar_results.items():
        print(f"  {opt}: 测试精度={res['final_test_acc']*100:.2f}%, 训练精度={res['final_train_acc']*100:.2f}%")
    
    print("\nNLI小样本（500训练样本）:")
    for opt, res in nli_results.items():
        print(f"  {opt}: 测试精度={res['final_test_acc']*100:.2f}%, 训练精度={res['final_train_acc']*100:.2f}%")

if __name__ == "__main__":
    main()