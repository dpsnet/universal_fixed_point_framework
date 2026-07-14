#!/usr/bin/env python3
"""
真实CIFAR-10/CIFAR-100数据集NTK谱分析实验
"""

import os
import numpy as np
import torch
import torch.nn as nn
import torchvision
from torch.utils.data import Subset
import json
import time

np.random.seed(42)
torch.manual_seed(42)

DEVICE = torch.device('cpu')
DATA_DIR = './data'

def load_real_cifar(dataset='cifar10', n_samples=300):
    """加载真实CIFAR数据"""
    print(f"[1/4] 加载真实{dataset.upper()}数据集...")
    
    if dataset == 'cifar10':
        mean = (0.4914, 0.4822, 0.4465)
        std = (0.2470, 0.2435, 0.2616)
        DatasetClass = torchvision.datasets.CIFAR10
        num_classes = 10
    else:
        mean = (0.5071, 0.4867, 0.4408)
        std = (0.2675, 0.2565, 0.2761)
        DatasetClass = torchvision.datasets.CIFAR100
        num_classes = 100
    
    transform = torchvision.transforms.Compose([
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Normalize(mean, std),
    ])
    
    trainset = DatasetClass(
        root=DATA_DIR, train=True, download=False, transform=transform
    )
    
    idx = np.random.choice(len(trainset), n_samples, replace=False)
    subset = Subset(trainset, idx.tolist())
    
    X = torch.stack([subset[i][0] for i in range(len(subset))])
    y = torch.tensor([subset[i][1] for i in range(len(subset))], dtype=torch.long)
    
    print(f"真实{dataset.upper()}数据: X={tuple(X.shape)}, y={tuple(y.shape)}")
    print(f"数据范围: [{X.min():.3f}, {X.max():.3f}]")
    return X, y, num_classes

class SimpleCNN(nn.Module):
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
    model.eval()
    X = X.to(DEVICE)
    
    grads = []
    n_samples = min(100, X.shape[0])
    for i in range(n_samples):
        x_i = X[i:i+1]
        model.zero_grad()
        y_i = model(x_i)
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

def main():
    print("="*70)
    print("真实CIFAR-10/CIFAR-100数据集NTK谱分析")
    print("="*70)
    
    results = {}
    
    # CIFAR-100实验
    print("\n" + "="*70)
    print("[1/2] CIFAR-100 NTK谱分析")
    print("="*70)
    
    X_c100, y_c100, num_classes_c100 = load_real_cifar('cifar100', n_samples=200)
    
    model = SimpleCNN(width=64, num_classes=num_classes_c100).to(DEVICE)
    K = compute_ntk(model, X_c100)
    
    eigvals = np.linalg.eigvalsh(K)
    eigvals = eigvals[eigvals > 1e-10]
    
    cifar100_results = {
        'spectral_radius': float(eigvals[-1]),
        'cond_number': float(eigvals[-1] / eigvals[0]),
        'effective_rank': float(np.sum(eigvals)**2 / np.sum(eigvals**2)),
        'n_positive_eigvals': len(eigvals),
        'n_samples': 100
    }
    
    print(f"    谱半径: {eigvals[-1]:.4f}")
    print(f"    条件数: {eigvals[-1]/eigvals[0]:.2f}")
    print(f"    有效秩: {np.sum(eigvals)**2 / np.sum(eigvals**2):.4f}")
    print(f"    正特征值数: {len(eigvals)}")
    
    results['cifar100'] = cifar100_results
    
    # CIFAR-10实验（如果可用）
    print("\n" + "="*70)
    print("[2/2] CIFAR-10 NTK谱分析（如果可用）")
    print("="*70)
    
    try:
        X_c10, y_c10, num_classes_c10 = load_real_cifar('cifar10', n_samples=200)
        
        model = SimpleCNN(width=64, num_classes=num_classes_c10).to(DEVICE)
        K = compute_ntk(model, X_c10)
        
        eigvals = np.linalg.eigvalsh(K)
        eigvals = eigvals[eigvals > 1e-10]
        
        cifar10_results = {
            'spectral_radius': float(eigvals[-1]),
            'cond_number': float(eigvals[-1] / eigvals[0]),
            'effective_rank': float(np.sum(eigvals)**2 / np.sum(eigvals**2)),
            'n_positive_eigvals': len(eigvals),
            'n_samples': 100
        }
        
        print(f"    谱半径: {eigvals[-1]:.4f}")
        print(f"    条件数: {eigvals[-1]/eigvals[0]:.2f}")
        print(f"    有效秩: {np.sum(eigvals)**2 / np.sum(eigvals**2):.4f}")
        print(f"    正特征值数: {len(eigvals)}")
        
        results['cifar10'] = cifar10_results
    except Exception as e:
        print(f"    CIFAR-10不可用: {e}")
        print("    请重新下载完整的CIFAR-10数据集")
        results['cifar10'] = {"error": str(e)}
    
    # 保存结果
    with open('real_cifar_results.txt', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n结果已保存到 real_cifar_results.txt")
    
    print("\n" + "="*70)
    print("真实CIFAR实验完成")
    print("="*70)

if __name__ == '__main__':
    main()
