#!/usr/bin/env python3
"""
分形RKHS曲率与泛化误差CIFAR大规模定量消融
验证定理5.10/5.11和推论5.9
"""

import os
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
from torch.utils.data import Subset
import json
import time

np.random.seed(42)
torch.manual_seed(42)

DEVICE = torch.device('cpu')

def load_cifar_data(n_samples=200, dataset='cifar10'):
    """加载CIFAR数据"""
    DATA_DIR = './data'
    
    if dataset == 'cifar10':
        mean = (0.4914, 0.4822, 0.4465)
        std = (0.2470, 0.2435, 0.2616)
        DatasetClass = torchvision.datasets.CIFAR10
    else:
        mean = (0.5071, 0.4867, 0.4408)
        std = (0.2675, 0.2565, 0.2761)
        DatasetClass = torchvision.datasets.CIFAR100
    
    transform = torchvision.transforms.Compose([
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Normalize(mean, std),
    ])
    
    trainset = DatasetClass(root=DATA_DIR, train=True, download=False, transform=transform)
    testset = DatasetClass(root=DATA_DIR, train=False, download=False, transform=transform)
    
    train_idx = np.random.choice(len(trainset), n_samples, replace=False)
    test_idx = np.random.choice(len(testset), 100, replace=False)
    
    X_train = torch.stack([trainset[i][0] for i in train_idx])
    y_train = torch.tensor([trainset[i][1] for i in train_idx], dtype=torch.long)
    X_test = torch.stack([testset[i][0] for i in test_idx])
    y_test = torch.tensor([testset[i][1] for i in test_idx], dtype=torch.long)
    
    return X_train, y_train, X_test, y_test

class CNN(nn.Module):
    def __init__(self, width=64, activation='relu', num_classes=10):
        super().__init__()
        self.conv1 = nn.Conv2d(3, width, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(width, width*2, 3, padding=1)
        self.conv3 = nn.Conv2d(width*2, width*4, 3, padding=1)
        self.fc1 = nn.Linear(width*4 * 4 * 4, width*2)
        self.fc2 = nn.Linear(width*2, num_classes)
        
        if activation == 'tanh':
            self.act = nn.Tanh()
        else:
            self.act = nn.ReLU()
    
    def forward(self, x):
        x = self.pool(self.act(self.conv1(x)))
        x = self.pool(self.act(self.conv2(x)))
        x = self.pool(self.act(self.conv3(x)))
        x = x.view(x.size(0), -1)
        x = self.act(self.fc1(x))
        x = self.fc2(x)
        return x

def compute_ntk(model, X):
    """计算NTK矩阵"""
    model.train()
    X = X.to(DEVICE)
    
    grads = []
    n_samples = min(30, X.shape[0])
    
    for i in range(n_samples):
        x_i = X[i:i+1]
        model.zero_grad()
        y_i = model(x_i)
        y_i[0, 0].backward(retain_graph=True)
        
        grad_flat = []
        for param in model.parameters():
            if param.grad is not None:
                grad_flat.append(param.grad.detach().cpu().flatten())
        grad_flat = torch.cat(grad_flat)
        grads.append(grad_flat)
    
    grads = torch.stack(grads)
    K = grads @ grads.T
    return K.detach().cpu().numpy()

def compute_curvature(K):
    """计算曲率"""
    print(f"  K矩阵形状: {K.shape}, 范数: {np.linalg.norm(K):.4f}")
    eigvals = np.linalg.eigvalsh(K)
    print(f"  特征值范围: [{np.min(eigvals):.6f}, {np.max(eigvals):.6f}]")
    eigvals = eigvals[eigvals > 1e-10]
    
    if len(eigvals) < 2:
        return 0.0
    
    avg_eig = np.mean(eigvals)
    curvature = np.sum((eigvals - avg_eig)**2) / np.sum(eigvals**2)
    
    return float(curvature)

def train_model(model, X_train, y_train, X_test, y_test, n_epochs=30, lr=0.001):
    """训练模型"""
    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()
    
    for epoch in range(n_epochs):
        model.train()
        optimizer.zero_grad()
        outputs = model(X_train.to(DEVICE))
        loss = criterion(outputs, y_train.to(DEVICE))
        loss.backward()
        optimizer.step()
    
    model.eval()
    with torch.no_grad():
        train_acc = (model(X_train.to(DEVICE)).argmax(dim=1) == y_train.to(DEVICE)).float().mean().item()
        test_acc = (model(X_test.to(DEVICE)).argmax(dim=1) == y_test.to(DEVICE)).float().mean().item()
    
    K = compute_ntk(model, X_train)
    curvature = compute_curvature(K)
    generalization_gap = train_acc - test_acc
    
    return {
        'final_train_acc': float(train_acc),
        'final_test_acc': float(test_acc),
        'generalization_gap': float(generalization_gap),
        'final_curvature': float(curvature)
    }

def main():
    print("="*70)
    print("分形RKHS曲率与泛化误差CIFAR大规模定量消融")
    print("="*70)
    
    results = {}
    
    # 加载数据
    print("\n[1/4] 加载CIFAR数据...")
    X_train, y_train, X_test, y_test = load_cifar_data(n_samples=200)
    print(f"  CIFAR-10: X_train={tuple(X_train.shape)}, X_test={tuple(X_test.shape)}")
    
    # 实验1: 不同宽度的曲率-泛化关系
    print("\n[2/4] 实验1: 不同宽度的曲率-泛化关系")
    print("-"*50)
    
    width_results = {}
    for width in [32, 64, 128, 256]:
        print(f"\n  宽度={width}:")
        model = CNN(width=width, num_classes=10).to(DEVICE)
        train_results = train_model(model, X_train, y_train, X_test, y_test, n_epochs=30)
        
        final_train = train_results['final_train_acc']
        final_test = train_results['final_test_acc']
        final_curvature = train_results['final_curvature']
        generalization_gap = train_results['generalization_gap']
        
        print(f"    训练精度: {final_train:.4f}")
        print(f"    测试精度: {final_test:.4f}")
        print(f"    泛化间隙: {generalization_gap:.4f}")
        print(f"    NTK曲率: {final_curvature:.6f}")
        
        width_results[f"width_{width}"] = train_results
    
    results['width_ablation'] = width_results
    
    # 实验2: tanh vs ReLU曲率对比
    print("\n[3/4] 实验2: tanh vs ReLU曲率对比")
    print("-"*50)
    
    activation_results = {}
    for activation in ['tanh', 'relu']:
        print(f"\n  激活函数={activation}:")
        model = CNN(width=64, activation=activation, num_classes=10).to(DEVICE)
        train_results = train_model(model, X_train, y_train, X_test, y_test, n_epochs=30)
        
        final_train = train_results['final_train_acc']
        final_test = train_results['final_test_acc']
        final_curvature = train_results['final_curvature']
        generalization_gap = train_results['generalization_gap']
        
        print(f"    训练精度: {final_train:.4f}")
        print(f"    测试精度: {final_test:.4f}")
        print(f"    泛化间隙: {generalization_gap:.4f}")
        print(f"    NTK曲率: {final_curvature:.6f}")
        
        activation_results[activation] = train_results
    
    results['activation_ablation'] = activation_results
    
    # 实验3: CIFAR-10 vs CIFAR-100曲率对比
    print("\n[4/4] 实验3: CIFAR-10 vs CIFAR-100曲率对比")
    print("-"*50)
    
    dataset_results = {}
    for dataset in ['cifar10', 'cifar100']:
        print(f"\n  数据集={dataset}:")
        X_tr, y_tr, X_te, y_te = load_cifar_data(n_samples=200, dataset=dataset)
        num_classes = 10 if dataset == 'cifar10' else 100
        
        model = CNN(width=64, num_classes=num_classes).to(DEVICE)
        train_results = train_model(model, X_tr, y_tr, X_te, y_te, n_epochs=30)
        
        final_train = train_results['final_train_acc']
        final_test = train_results['final_test_acc']
        final_curvature = train_results['final_curvature']
        generalization_gap = train_results['generalization_gap']
        
        print(f"    训练精度: {final_train:.4f}")
        print(f"    测试精度: {final_test:.4f}")
        print(f"    泛化间隙: {generalization_gap:.4f}")
        print(f"    NTK曲率: {final_curvature:.6f}")
        
        dataset_results[dataset] = train_results
    
    results['dataset_ablation'] = dataset_results
    
    with open('curvature_cifar_results.txt', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("\n" + "="*70)
    print("曲率-泛化误差消融实验完成")
    print("结果已保存到 curvature_cifar_results.txt")
    print("="*70)
    
    print("\n=== 实验摘要 ===")
    
    print("\n1. 宽度消融:")
    for width, r in width_results.items():
        print(f"   {width}: 泛化间隙={r['generalization_gap']:.4f}, 曲率={r['final_curvature']:.4f}")
    
    print("\n2. 激活函数对比:")
    for act, r in activation_results.items():
        print(f"   {act}: 泛化间隙={r['generalization_gap']:.4f}, 曲率={r['final_curvature']:.4f}")
    
    print("\n3. 数据集对比:")
    for dataset, r in dataset_results.items():
        print(f"   {dataset}: 泛化间隙={r['generalization_gap']:.4f}, 曲率={r['final_curvature']:.4f}")

if __name__ == '__main__':
    main()
