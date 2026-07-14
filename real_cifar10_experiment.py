#!/usr/bin/env python3
"""
真实CIFAR-10数据集下载与NTK谱分析实验
"""

import os
import urllib.request
import tarfile
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
CIFAR_URL = 'https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz'

def download_cifar10():
    """下载CIFAR-10数据集"""
    os.makedirs(DATA_DIR, exist_ok=True)
    tar_path = os.path.join(DATA_DIR, 'cifar-10-python.tar.gz')
    
    if os.path.exists(tar_path):
        print("CIFAR-10压缩包已存在，重新下载...")
        os.remove(tar_path)
    
    print(f"正在下载CIFAR-10到 {tar_path}...")
    urllib.request.urlretrieve(CIFAR_URL, tar_path)
    print("下载完成")
    
    print("正在解压...")
    with tarfile.open(tar_path, 'r:gz') as tar:
        tar.extractall(DATA_DIR)
    print("解压完成")
    
    # 验证
    extracted_dir = os.path.join(DATA_DIR, 'cifar-10-batches-py')
    if os.path.exists(extracted_dir):
        files = os.listdir(extracted_dir)
        print(f"解压后的文件: {files}")
        return True
    return False

def load_real_cifar10(n_samples=300):
    """加载真实CIFAR-10数据"""
    print("[1/4] 加载真实CIFAR-10数据集...")
    
    transform = torchvision.transforms.Compose([
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Normalize(
            (0.4914, 0.4822, 0.4465), (0.2470, 0.2435, 0.2616)
        ),
    ])
    
    trainset = torchvision.datasets.CIFAR10(
        root=DATA_DIR, train=True, download=False, transform=transform
    )
    
    idx = np.random.choice(len(trainset), n_samples, replace=False)
    subset = Subset(trainset, idx.tolist())
    
    X = torch.stack([subset[i][0] for i in range(len(subset))])
    y = torch.tensor([subset[i][1] for i in range(len(subset))], dtype=torch.long)
    
    print(f"真实CIFAR-10数据: X={tuple(X.shape)}, y={tuple(y.shape)}")
    print(f"数据范围: [{X.min():.3f}, {X.max():.3f}]")
    return X, y

class SimpleCNN(nn.Module):
    def __init__(self, width=64, activation='relu'):
        super().__init__()
        self.conv1 = nn.Conv2d(3, width, 3, padding=1)
        self.conv2 = nn.Conv2d(width, width*2, 3, padding=1)
        self.conv3 = nn.Conv2d(width*2, width*4, 3, padding=1)
        self.fc1 = nn.Linear(width*4 * 4 * 4, width*2)
        self.fc2 = nn.Linear(width*2, 10)
        
        if activation == 'tanh':
            self.act = nn.Tanh()
        else:
            self.act = nn.ReLU()
    
    def forward(self, x):
        x = self.act(self.conv1(x))
        x = self.act(self.conv2(x))
        x = self.act(self.conv3(x))
        x = x.view(x.size(0), -1)
        x = self.act(self.fc1(x))
        x = self.fc2(x)
        return x

def compute_ntk(model, X):
    """计算NTK矩阵"""
    model.eval()
    X = X.to(DEVICE)
    
    grads = []
    for i in range(min(100, X.shape[0])):
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
    print("真实CIFAR-10数据集NTK谱分析")
    print("="*70)
    
    # 下载数据集
    success = download_cifar10()
    if not success:
        print("CIFAR-10下载失败，使用合成数据回退")
        return
    
    # 加载数据
    X, y = load_real_cifar10(n_samples=200)
    
    # 实验1：基础NTK谱性质
    print("\n" + "="*70)
    print("[2/4] 基础NTK谱性质分析")
    print("="*70)
    
    model = SimpleCNN(width=64).to(DEVICE)
    K = compute_ntk(model, X)
    
    eigvals = np.linalg.eigvalsh(K)
    eigvals = eigvals[eigvals > 1e-10]
    
    results = {
        'dataset': 'CIFAR-10 (real)',
        'n_samples': 100,
        'base_spectral': {
            'spectral_radius': float(eigvals[-1]),
            'cond_number': float(eigvals[-1] / eigvals[0]),
            'effective_rank': float(np.sum(eigvals)**2 / np.sum(eigvals**2)),
            'n_positive_eigvals': len(eigvals)
        }
    }
    
    print(f"    谱半径: {eigvals[-1]:.4f}")
    print(f"    条件数: {eigvals[-1]/eigvals[0]:.2f}")
    print(f"    有效秩: {np.sum(eigvals)**2 / np.sum(eigvals**2):.4f}")
    print(f"    正特征值数: {len(eigvals)}")
    
    # 实验2：宽度缩放
    print("\n" + "="*70)
    print("[3/4] 宽度缩放实验")
    print("="*70)
    
    width_list = [32, 64, 128]
    width_results = []
    for width in width_list:
        model = SimpleCNN(width=width).to(DEVICE)
        K = compute_ntk(model, X)
        
        eigvals = np.linalg.eigvalsh(K)
        eigvals = eigvals[eigvals > 1e-10]
        
        result = {
            'width': width,
            'spectral_radius': float(eigvals[-1]),
            'cond_number': float(eigvals[-1] / eigvals[0]),
            'effective_rank': float(np.sum(eigvals)**2 / np.sum(eigvals**2))
        }
        width_results.append(result)
        
        print(f"    宽度={width}: 谱半径={eigvals[-1]:.4f}, 条件数={eigvals[-1]/eigvals[0]:.2f}, 有效秩={result['effective_rank']:.4f}")
    
    results['width_scaling'] = width_results
    
    # 实验3：tanh vs ReLU对比
    print("\n" + "="*70)
    print("[4/4] tanh vs ReLU对比")
    print("="*70)
    
    activation_results = []
    for act in ['tanh', 'relu']:
        model = SimpleCNN(width=64, activation=act).to(DEVICE)
        K = compute_ntk(model, X)
        
        eigvals = np.linalg.eigvalsh(K)
        eigvals = eigvals[eigvals > 1e-10]
        
        result = {
            'activation': act,
            'spectral_radius': float(eigvals[-1]),
            'cond_number': float(eigvals[-1] / eigvals[0]),
            'effective_rank': float(np.sum(eigvals)**2 / np.sum(eigvals**2))
        }
        activation_results.append(result)
        
        print(f"    激活={act}: 谱半径={eigvals[-1]:.4f}, 条件数={eigvals[-1]/eigvals[0]:.2f}, 有效秩={result['effective_rank']:.4f}")
    
    results['activation_comparison'] = activation_results
    
    # 保存结果
    with open('real_cifar10_results.txt', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n结果已保存到 real_cifar10_results.txt")
    
    print("\n" + "="*70)
    print("真实CIFAR-10实验完成")
    print("="*70)

if __name__ == '__main__':
    main()
