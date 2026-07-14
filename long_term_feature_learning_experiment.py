#!/usr/bin/env python3
"""
强特征学习长周期完整对照实验
验证定理5.25-5.27：长训练周期、大学习率核漂移、时间平均有效核泛化
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
    model.train()
    X = X.to(DEVICE)
    
    grads = []
    n_samples = min(30, X.shape[0])
    for i in range(n_samples):
        x_i = X[i:i+1]
        model.zero_grad()
        y_i = model(x_i)
        y_i.backward(retain_graph=True)
        
        grad_flat = []
        for param in model.parameters():
            if param.grad is not None:
                grad_flat.append(param.grad.detach().cpu().flatten())
        grad_flat = torch.cat(grad_flat)
        grads.append(grad_flat)
    
    grads = torch.stack(grads)
    K = grads @ grads.T
    return K.detach().cpu().numpy()

def long_term_training(X_train, y_train, X_test, y_test, model, optimizer, n_epochs=200, 
                       lr=0.01, track_interval=20):
    """长周期训练"""
    dataset = TensorDataset(X_train, y_train)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
    
    K_initial = compute_ntk(model, X_train)
    
    results = {
        'epochs': [],
        'delta_K': [],
        'train_loss': [],
        'test_loss': [],
        'train_acc': [],
        'test_acc': [],
        'spectral_radius': [],
        'cond_number': []
    }
    
    K_history = [K_initial]
    
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
            K_history.append(K_current)
            
            delta_K = np.linalg.norm(K_current - K_initial, 'fro') / np.linalg.norm(K_initial, 'fro')
            
            eigvals = np.linalg.eigvalsh(K_current)
            eigvals = eigvals[eigvals > 1e-10]
            
            model.eval()
            with torch.no_grad():
                train_preds = model(X_train.to(DEVICE))
                test_preds = model(X_test.to(DEVICE))
                train_loss = nn.MSELoss()(train_preds, y_train.to(DEVICE)).item()
                test_loss = nn.MSELoss()(test_preds, y_test.to(DEVICE)).item()
                train_acc = ((train_preds > 0) == (y_train.to(DEVICE) > 0)).float().mean().item()
                test_acc = ((test_preds > 0) == (y_test.to(DEVICE) > 0)).float().mean().item()
            
            results['epochs'].append(epoch + 1)
            results['delta_K'].append(float(delta_K))
            results['train_loss'].append(float(train_loss))
            results['test_loss'].append(float(test_loss))
            results['train_acc'].append(float(train_acc))
            results['test_acc'].append(float(test_acc))
            results['spectral_radius'].append(float(eigvals[-1]))
            results['cond_number'].append(float(eigvals[-1] / eigvals[0]))
    
    # 时间平均有效核
    K_avg = np.mean(K_history, axis=0)
    eigvals_avg = np.linalg.eigvalsh(K_avg)
    
    results['time_averaged_K'] = {
        'spectral_radius': float(np.max(eigvals_avg)),
        'cond_number': float(np.max(eigvals_avg) / np.min(eigvals_avg[np.abs(eigvals_avg) > 1e-10]))
    }
    
    return results

def main():
    print("="*70)
    print("强特征学习长周期完整对照实验")
    print("="*70)
    
    # 生成数据
    print("\n[1/5] 生成分形数据...")
    X_train, y_train = generate_fractal_data(n_samples=200, n_features=50, fractal_dim=1.5)
    X_test, y_test = generate_fractal_data(n_samples=100, n_features=50, fractal_dim=1.5)
    print(f"  数据: X_train={tuple(X_train.shape)}, X_test={tuple(X_test.shape)}")
    
    results = {}
    
    # 实验1: 不同学习率的长周期核漂移
    print("\n[2/5] 实验1: 不同学习率的长周期核漂移")
    print("-"*50)
    
    lr_results = {}
    for lr in [0.001, 0.01, 0.1, 0.5]:
        print(f"\n  学习率={lr}:")
        model = MLP(width=128, depth=3).to(DEVICE)
        optimizer = optim.Adam(model.parameters(), lr=lr)
        lr_results[f"lr_{lr}"] = long_term_training(X_train, y_train, X_test, y_test, 
                                                    model, optimizer, n_epochs=200, 
                                                    lr=lr, track_interval=40)
        
        final_delta = lr_results[f"lr_{lr}"]['delta_K'][-1]
        final_acc = lr_results[f"lr_{lr}"]['test_acc'][-1]
        print(f"    最终delta_K: {final_delta:.6f}")
        print(f"    最终测试精度: {final_acc:.4f}")
    
    results['learning_rates'] = lr_results
    
    # 实验2: 惰性训练vs非惰性训练长周期对比
    print("\n[3/5] 实验2: 惰性训练vs非惰性训练长周期对比")
    print("-"*50)
    
    lazy_model = MLP(width=128, depth=3).to(DEVICE)
    lazy_optimizer = optim.Adam(lazy_model.parameters(), lr=0.01)
    lazy_results = long_term_training(X_train, y_train, X_test, y_test, 
                                      lazy_model, lazy_optimizer, n_epochs=200, 
                                      track_interval=40)
    
    active_model = MLP(width=128, depth=3).to(DEVICE)
    active_optimizer = optim.SGD(active_model.parameters(), lr=0.1)
    active_results = long_term_training(X_train, y_train, X_test, y_test, 
                                        active_model, active_optimizer, n_epochs=200, 
                                        track_interval=40)
    
    results['lazy_vs_active'] = {
        'lazy': lazy_results,
        'active': active_results
    }
    
    print(f"  惰性训练:")
    print(f"    最终delta_K: {lazy_results['delta_K'][-1]:.6f}")
    print(f"    最终测试精度: {lazy_results['test_acc'][-1]:.4f}")
    print(f"  非惰性训练:")
    print(f"    最终delta_K: {active_results['delta_K'][-1]:.6f}")
    print(f"    最终测试精度: {active_results['test_acc'][-1]:.4f}")
    
    # 实验3: 时间平均有效核泛化误差
    print("\n[4/5] 实验3: 时间平均有效核泛化误差")
    print("-"*50)
    
    avg_results = {}
    for width in [64, 128, 256]:
        print(f"\n  宽度={width}:")
        model = MLP(width=width, depth=3).to(DEVICE)
        optimizer = optim.Adam(model.parameters(), lr=0.01)
        train_results = long_term_training(X_train, y_train, X_test, y_test, 
                                           model, optimizer, n_epochs=200, 
                                           track_interval=50)
        
        final_train_acc = train_results['train_acc'][-1]
        final_test_acc = train_results['test_acc'][-1]
        generalization_gap = final_train_acc - final_test_acc
        
        print(f"    训练精度: {final_train_acc:.4f}")
        print(f"    测试精度: {final_test_acc:.4f}")
        print(f"    泛化间隙: {generalization_gap:.4f}")
        print(f"    时间平均条件数: {train_results['time_averaged_K']['cond_number']:.2f}")
        
        avg_results[f"width_{width}"] = {
            'final_train_acc': float(final_train_acc),
            'final_test_acc': float(final_test_acc),
            'generalization_gap': float(generalization_gap),
            'time_averaged_cond': float(train_results['time_averaged_K']['cond_number'])
        }
    
    results['time_averaged'] = avg_results
    
    # 实验4: 训练阶段划分验证
    print("\n[5/5] 实验4: 训练阶段划分验证")
    print("-"*50)
    
    stage_results = {}
    model = MLP(width=128, depth=3).to(DEVICE)
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    train_results = long_term_training(X_train, y_train, X_test, y_test, 
                                       model, optimizer, n_epochs=200, 
                                       track_interval=10)
    
    epochs = np.array(train_results['epochs'])
    delta_K = np.array(train_results['delta_K'])
    
    stage1_end = np.argmax(delta_K > 0.5) if np.any(delta_K > 0.5) else len(epochs)
    stage2_end = np.argmax(delta_K > 1.5) if np.any(delta_K > 1.5) else len(epochs)
    
    print(f"  阶段1（惰性）: epochs 0-{epochs[min(stage1_end, len(epochs)-1)]}")
    print(f"  阶段2（过渡）: epochs {epochs[min(stage1_end, len(epochs)-1)]}-{epochs[min(stage2_end, len(epochs)-1)]}")
    print(f"  阶段3（特征学习）: epochs {epochs[min(stage2_end, len(epochs)-1)]}+")
    
    stage_results['stage_boundaries'] = {
        'stage1_end_epoch': int(epochs[min(stage1_end, len(epochs)-1)]) if len(epochs) > 0 else 0,
        'stage2_end_epoch': int(epochs[min(stage2_end, len(epochs)-1)]) if len(epochs) > 0 else 0
    }
    stage_results['delta_K_history'] = [float(d) for d in delta_K]
    stage_results['epochs'] = [int(e) for e in epochs]
    
    results['stage_division'] = stage_results
    
    # 保存结果
    with open('long_term_feature_learning_results.txt', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("\n" + "="*70)
    print("强特征学习长周期实验完成")
    print("结果已保存到 long_term_feature_learning_results.txt")
    print("="*70)
    
    print("\n=== 实验摘要 ===")
    
    print("\n1. 学习率影响:")
    for lr, r in lr_results.items():
        print(f"   {lr}: delta_K={r['delta_K'][-1]:.6f}, acc={r['test_acc'][-1]:.4f}")
    
    print("\n2. 惰性vs非惰性:")
    print(f"   惰性: delta_K={lazy_results['delta_K'][-1]:.6f}, acc={lazy_results['test_acc'][-1]:.4f}")
    print(f"   非惰性: delta_K={active_results['delta_K'][-1]:.6f}, acc={active_results['test_acc'][-1]:.4f}")
    
    print("\n3. 时间平均有效核:")
    for width, r in avg_results.items():
        print(f"   {width}: 泛化间隙={r['generalization_gap']:.4f}, 条件数={r['time_averaged_cond']:.2f}")

if __name__ == '__main__':
    main()
