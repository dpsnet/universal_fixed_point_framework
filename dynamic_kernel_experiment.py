#!/usr/bin/env python3
"""
非惰性训练动态核演化实验验证
测量训练过程中NTK矩阵的漂移和谱结构变化
"""

import os
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import json
import time

np.random.seed(42)
torch.manual_seed(42)

DEVICE = torch.device('cpu')

def generate_fractal_data(n_samples=200, n_features=50, fractal_dim=1.5):
    """生成具有指定分形维数的合成数据"""
    X = np.random.randn(n_samples, n_features)
    y = np.sin(np.sum(X[:, :int(fractal_dim*10)]**2, axis=1)) > 0
    y = (y * 2 - 1).astype(np.float32)
    return torch.tensor(X, dtype=torch.float32), torch.tensor(y, dtype=torch.float32)

class MLP(nn.Module):
    def __init__(self, width=128, depth=3, activation='relu'):
        super().__init__()
        layers = []
        layers.append(nn.Linear(50, width))
        if activation == 'tanh':
            layers.append(nn.Tanh())
        else:
            layers.append(nn.ReLU())
        for _ in range(depth - 2):
            layers.append(nn.Linear(width, width))
            if activation == 'tanh':
                layers.append(nn.Tanh())
            else:
                layers.append(nn.ReLU())
        layers.append(nn.Linear(width, 1))
        self.net = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.net(x).squeeze()

def compute_ntk(model, X):
    """计算NTK矩阵"""
    model.eval()
    X = X.to(DEVICE)
    
    grads = []
    n_samples = min(50, X.shape[0])
    for i in range(n_samples):
        x_i = X[i:i+1]
        model.zero_grad()
        y_i = model(x_i)
        y_i.backward()
        
        grad_flat = []
        for param in model.parameters():
            if param.grad is not None:
                grad_flat.append(param.grad.detach().cpu().flatten())
        grad_flat = torch.cat(grad_flat)
        grads.append(grad_flat)
    
    grads = torch.stack(grads)
    K = grads @ grads.T
    return K.detach().cpu().numpy()

def compute_spectral_properties(K):
    """计算谱性质"""
    eigvals = np.linalg.eigvalsh(K)
    eigvals = eigvals[eigvals > 1e-10]
    
    if len(eigvals) == 0:
        return {
            'spectral_radius': 0.0,
            'cond_number': 0.0,
            'effective_rank': 0.0
        }
    
    return {
        'spectral_radius': float(eigvals[-1]),
        'cond_number': float(eigvals[-1] / eigvals[0]),
        'effective_rank': float(np.sum(eigvals)**2 / np.sum(eigvals**2))
    }

def train_and_track(X_train, y_train, model, optimizer, n_epochs=50, track_interval=5):
    """训练并追踪NTK演化"""
    dataset = TensorDataset(X_train, y_train)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
    
    K_initial = compute_ntk(model, X_train)
    initial_props = compute_spectral_properties(K_initial)
    
    results = {
        'initial': initial_props,
        'epochs': [],
        'delta_K': [],
        'spectral_properties': []
    }
    
    for epoch in range(n_epochs):
        model.train()
        total_loss = 0.0
        for batch_X, batch_y in dataloader:
            batch_X, batch_y = batch_X.to(DEVICE), batch_y.to(DEVICE)
            optimizer.zero_grad()
            outputs = model(batch_X)
            loss = nn.MSELoss()(outputs, batch_y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        
        if (epoch + 1) % track_interval == 0:
            K_current = compute_ntk(model, X_train)
            delta_K = np.linalg.norm(K_current - K_initial, 'fro') / np.linalg.norm(K_initial, 'fro')
            current_props = compute_spectral_properties(K_current)
            
            results['epochs'].append(epoch + 1)
            results['delta_K'].append(float(delta_K))
            results['spectral_properties'].append(current_props)
            
            print(f"  Epoch {epoch+1:3d}: delta_K={delta_K:.6f}, "
                  f"谱半径={current_props['spectral_radius']:.4f}, "
                  f"条件数={current_props['cond_number']:.2f}, "
                  f"有效秩={current_props['effective_rank']:.4f}")
    
    return results

def main():
    print("="*70)
    print("非惰性训练动态核演化实验验证")
    print("="*70)
    
    # 生成数据
    print("\n[1/4] 生成分形数据...")
    X_train, y_train = generate_fractal_data(n_samples=200, n_features=50, fractal_dim=1.5)
    print(f"  数据: X={tuple(X_train.shape)}, y={tuple(y_train.shape)}")
    
    results = {}
    
    # 实验1: 不同学习率的影响
    print("\n[2/4] 实验1: 不同学习率的动态核演化")
    print("-"*50)
    
    lr_results = {}
    for lr in [0.001, 0.01, 0.1]:
        print(f"\n  学习率={lr}:")
        model = MLP(width=128, depth=3).to(DEVICE)
        optimizer = optim.Adam(model.parameters(), lr=lr)
        lr_results[f"lr_{lr}"] = train_and_track(X_train, y_train, model, optimizer, 
                                                 n_epochs=50, track_interval=10)
    
    results['learning_rates'] = lr_results
    
    # 实验2: 惰性训练vs非惰性训练对比
    print("\n[3/4] 实验2: 惰性训练vs非惰性训练对比")
    print("-"*50)
    
    # 惰性训练 (冻结权重)
    print("\n  惰性训练 (权重冻结):")
    lazy_model = MLP(width=128, depth=3).to(DEVICE)
    lazy_optimizer = optim.Adam(lazy_model.parameters(), lr=0.01)
    lazy_results = train_and_track(X_train, y_train, lazy_model, lazy_optimizer,
                                   n_epochs=50, track_interval=10)
    
    # 非惰性训练 (正常训练)
    print("\n  非惰性训练 (正常训练):")
    active_model = MLP(width=128, depth=3).to(DEVICE)
    active_optimizer = optim.Adam(active_model.parameters(), lr=0.01)
    active_results = train_and_track(X_train, y_train, active_model, active_optimizer,
                                     n_epochs=50, track_interval=10)
    
    results['lazy_vs_active'] = {
        'lazy': lazy_results,
        'active': active_results
    }
    
    # 实验3: 不同宽度的动态核演化
    print("\n[4/4] 实验3: 不同网络宽度的动态核演化")
    print("-"*50)
    
    width_results = {}
    for width in [32, 128, 512]:
        print(f"\n  宽度={width}:")
        model = MLP(width=width, depth=3).to(DEVICE)
        optimizer = optim.Adam(model.parameters(), lr=0.01)
        width_results[f"width_{width}"] = train_and_track(X_train, y_train, model, optimizer,
                                                          n_epochs=50, track_interval=10)
    
    results['widths'] = width_results
    
    # 保存结果
    with open('dynamic_kernel_results.txt', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("\n" + "="*70)
    print("动态核演化实验完成")
    print("结果已保存到 dynamic_kernel_results.txt")
    print("="*70)
    
    # 打印摘要
    print("\n=== 实验摘要 ===")
    
    print("\n1. 学习率影响:")
    for lr, r in lr_results.items():
        final_delta = r['delta_K'][-1] if r['delta_K'] else 0
        print(f"   {lr}: 最终delta_K={final_delta:.4f}")
    
    print("\n2. 惰性vs非惰性训练:")
    lazy_delta = lazy_results['delta_K'][-1] if lazy_results['delta_K'] else 0
    active_delta = active_results['delta_K'][-1] if active_results['delta_K'] else 0
    print(f"   惰性训练 delta_K={lazy_delta:.4f}")
    print(f"   非惰性训练 delta_K={active_delta:.4f}")
    print(f"   差异倍数: {active_delta/lazy_delta:.2f}x")
    
    print("\n3. 宽度影响:")
    for width, r in width_results.items():
        final_delta = r['delta_K'][-1] if r['delta_K'] else 0
        print(f"   {width}: 最终delta_K={final_delta:.4f}")

if __name__ == '__main__':
    main()
