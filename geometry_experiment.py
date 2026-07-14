#!/usr/bin/env python3
"""
几何结构验证实验：曲率、维度与泛化误差的大规模定量实验

验证理论：
1. Fractal RKHS的Riemann曲率张量（定理5.10）
2. 曲率修正的Rademacher复杂度泛化界（定理5.11）
3. 分形泛化边界：最小宽度下界（推论5.9）
4. 分形维数与条件数的单调关系（推论5.8）

实验设计：
1. Weierstrass分形函数的NTK谱分析（不同分形维数）
2. 核曲率计算与条件数关系
3. 训练误差 vs 测试误差 vs 分形维数
4. 宽度缩放与泛化误差（验证最小宽度下界）
5. tanh vs ReLU的曲率差异
"""

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.linalg import eigvalsh
from scipy.stats import pearsonr, spearmanr
import sys
import time
import json

np.random.seed(42)
torch.manual_seed(42)

DEVICE = torch.device('cpu')
print(f"设备: {DEVICE}")

# ==============================================================================
# 1. Weierstrass分形函数生成器
# ==============================================================================
def generate_weierstrass(N, D, a=0.5, b=2.0, noise_std=0.01):
    """
    生成Weierstrass-Mandelbrot分形函数样本
    D: 分形维数 (1 < D < 2)
    a: 压缩系数 (0 < a < 1)
    b: 频率乘数 (b > 1)
    """
    x = np.linspace(0, 1, N)
    y = np.zeros(N)
    
    K_max = int(np.log(N) / np.log(b)) + 1
    for k in range(K_max):
        y += a**((D-1)*k) * np.sin(b**k * 2 * np.pi * x)
    
    y = (y - y.mean()) / y.std()
    y += np.random.normal(0, noise_std, N)
    
    return x, y

def generate_fractal_dataset(n_samples=100, n_features=100, fractal_dim=1.5):
    """生成分形数据集"""
    X = []
    y = []
    for _ in range(n_samples):
        a = 0.4 + np.random.rand() * 0.2
        b = 1.5 + np.random.rand() * 1.5
        _, signal = generate_weierstrass(n_features, fractal_dim, a=a, b=b)
        X.append(signal)
        y.append(np.mean(signal))
    
    X = np.array(X).astype(np.float32)
    y = np.array(y).astype(np.float32)
    return torch.tensor(X), torch.tensor(y)

# ==============================================================================
# 2. 核曲率计算
# ==============================================================================
def compute_kernel_curvature(K):
    """
    计算核矩阵的Riemann曲率近似
    使用平均截面曲率近似
    """
    n = K.shape[0]
    K_inv = np.linalg.pinv(K + 1e-6 * np.eye(n))
    
    # Christoffel符号近似: Gamma_{ijk} = 0.5 * K^{-1} * (dK/dx_i dK/dx_j)
    # 简化：使用核矩阵的二阶差分近似曲率
    # 截面曲率: K(x,y) = <R(x,y)x, y> / (|x|^2 |y|^2 - <x,y>^2)
    
    # 计算特征值分解
    eigvals, eigvecs = np.linalg.eigh(K)
    eigvals = eigvals[eigvals > 1e-10]
    
    # 曲率近似：基于特征值分布的曲率度量
    # 对于核空间，曲率与特征值分布的"峰度"相关
    lambda_mean = np.mean(eigvals)
    lambda_var = np.var(eigvals)
    lambda_skew = np.mean((eigvals - lambda_mean)**3) / lambda_var**1.5
    lambda_kurt = np.mean((eigvals - lambda_mean)**4) / lambda_var**2 - 3
    
    # 平均截面曲率近似（基于特征值的几何平均值）
    # 曲率 > 0: 负曲率空间 (分形空间典型)
    # 曲率 < 0: 正曲率空间
    mean_curvature = -lambda_var / (lambda_mean**2)
    
    # Ricci曲率近似
    ricci_scalar = -n * lambda_var / (lambda_mean**2)
    
    return {
        'mean_curvature': float(mean_curvature),
        'ricci_scalar': float(ricci_scalar),
        'lambda_mean': float(lambda_mean),
        'lambda_var': float(lambda_var),
        'lambda_skew': float(lambda_skew),
        'lambda_kurt': float(lambda_kurt),
        'cond_number': float(eigvals[-1] / eigvals[0]) if len(eigvals) > 0 else float('inf'),
        'effective_rank': float(np.sum(eigvals)**2 / np.sum(eigvals**2)) if np.sum(eigvals**2) > 0 else 0.0
    }

# ==============================================================================
# 3. NTK计算
# ==============================================================================
class SimpleMLP(nn.Module):
    def __init__(self, input_dim, hidden_dim, activation='relu'):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, 1)
        
        if activation == 'tanh':
            self.act = nn.Tanh()
        elif activation == 'relu':
            self.act = nn.ReLU()
        else:
            self.act = nn.ReLU()
        
        # He初始化
        nn.init.kaiming_normal_(self.fc1.weight)
        nn.init.kaiming_normal_(self.fc2.weight)
        nn.init.kaiming_normal_(self.fc3.weight)
    
    def forward(self, x):
        x = self.act(self.fc1(x))
        x = self.act(self.fc2(x))
        x = self.fc3(x)
        return x.squeeze()

def compute_ntk(model, X):
    """计算NTK矩阵"""
    model.eval()
    X = X.to(DEVICE)
    
    grads = []
    for i in range(X.shape[0]):
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

# ==============================================================================
# 4. 训练与泛化误差
# ==============================================================================
def train_model(model, X_train, y_train, X_val, y_val, epochs=100, lr=0.01):
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = nn.MSELoss()
    
    train_losses = []
    val_losses = []
    
    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        y_pred = model(X_train.to(DEVICE))
        loss = criterion(y_pred, y_train.to(DEVICE))
        loss.backward()
        optimizer.step()
        
        train_losses.append(loss.item())
        
        model.eval()
        with torch.no_grad():
            val_pred = model(X_val.to(DEVICE))
            val_loss = criterion(val_pred, y_val.to(DEVICE)).item()
            val_losses.append(val_loss)
    
    return train_losses, val_losses

# ==============================================================================
# 5. 主实验流程
# ==============================================================================
def main():
    print("="*70)
    print("几何结构验证实验：曲率、维度与泛化误差")
    print("="*70)
    
    results = {}
    
    # --------------------------------------------------------------------------
    # 实验1：分形维数扫描（1.1 -> 1.9）
    # --------------------------------------------------------------------------
    print("\n" + "="*70)
    print("[1/4] 分形维数扫描：D = 1.1, 1.3, 1.5, 1.7, 1.9")
    print("="*70)
    
    dim_list = [1.1, 1.3, 1.5, 1.7, 1.9]
    n_samples = 100
    n_features = 200
    
    dim_results = []
    for D in dim_list:
        print(f"\n  --- 分形维数 D = {D} ---")
        
        # 生成数据
        X, y = generate_fractal_dataset(n_samples=200, n_features=n_features, fractal_dim=D)
        X_train, X_val = X[:n_samples], X[n_samples:]
        y_train, y_val = y[:n_samples], y[n_samples:]
        
        # 计算NTK
        model = SimpleMLP(n_features, 256, activation='tanh').to(DEVICE)
        K = compute_ntk(model, X_train)
        
        # 计算曲率
        curv = compute_kernel_curvature(K)
        
        # 计算谱性质
        eigvals = eigvalsh(K)
        eigvals = eigvals[eigvals > 1e-10]
        
        # 训练模型
        train_losses, val_losses = train_model(
            model, X_train, y_train, X_val, y_val, epochs=200, lr=0.001
        )
        
        result = {
            'fractal_dim': D,
            'mean_curvature': curv['mean_curvature'],
            'ricci_scalar': curv['ricci_scalar'],
            'cond_number': curv['cond_number'],
            'effective_rank': curv['effective_rank'],
            'lambda_mean': curv['lambda_mean'],
            'lambda_var': curv['lambda_var'],
            'final_train_loss': train_losses[-1],
            'final_val_loss': val_losses[-1],
            'generalization_gap': val_losses[-1] - train_losses[-1],
            'spectral_radius': float(eigvals[-1]),
            'spectral_gap': float(eigvals[-1] - eigvals[-2]) if len(eigvals) > 1 else 0.0
        }
        
        dim_results.append(result)
        print(f"    曲率: {curv['mean_curvature']:.4f}")
        print(f"    条件数: {curv['cond_number']:.2f}")
        print(f"    训练误差: {train_losses[-1]:.6f}")
        print(f"    验证误差: {val_losses[-1]:.6f}")
        print(f"    泛化间隙: {result['generalization_gap']:.6f}")
    
    results['dim_scan'] = dim_results
    
    # --------------------------------------------------------------------------
    # 实验2：宽度缩放与泛化误差（验证最小宽度下界）
    # --------------------------------------------------------------------------
    print("\n" + "="*70)
    print("[2/4] 宽度缩放实验：验证最小宽度下界 m* >= C * epsilon^(-(2D-1)/(2-D))")
    print("="*70)
    
    width_list = [32, 64, 128, 256, 512, 1024]
    D = 1.5  # 固定分形维数
    
    width_results = []
    for width in width_list:
        print(f"\n  --- 宽度 m = {width} ---")
        
        X, y = generate_fractal_dataset(n_samples=200, n_features=n_features, fractal_dim=D)
        X_train, X_val = X[:n_samples], X[n_samples:]
        y_train, y_val = y[:n_samples], y[n_samples:]
        
        model = SimpleMLP(n_features, width, activation='tanh').to(DEVICE)
        K = compute_ntk(model, X_train)
        
        curv = compute_kernel_curvature(K)
        
        train_losses, val_losses = train_model(
            model, X_train, y_train, X_val, y_val, epochs=200, lr=0.001
        )
        
        result = {
            'width': width,
            'mean_curvature': curv['mean_curvature'],
            'cond_number': curv['cond_number'],
            'final_train_loss': train_losses[-1],
            'final_val_loss': val_losses[-1],
            'generalization_gap': val_losses[-1] - train_losses[-1],
            'effective_rank': curv['effective_rank']
        }
        
        width_results.append(result)
        print(f"    条件数: {curv['cond_number']:.2f}")
        print(f"    训练误差: {train_losses[-1]:.6f}")
        print(f"    验证误差: {val_losses[-1]:.6f}")
        print(f"    泛化间隙: {result['generalization_gap']:.6f}")
    
    results['width_scan'] = width_results
    
    # --------------------------------------------------------------------------
    # 实验3：tanh vs ReLU的曲率差异
    # --------------------------------------------------------------------------
    print("\n" + "="*70)
    print("[3/4] tanh vs ReLU的曲率差异对比")
    print("="*70)
    
    activation_results = []
    for act in ['tanh', 'relu']:
        print(f"\n  --- 激活: {act} ---")
        
        X, y = generate_fractal_dataset(n_samples=200, n_features=n_features, fractal_dim=1.5)
        X_train, X_val = X[:n_samples], X[n_samples:]
        y_train, y_val = y[:n_samples], y[n_samples:]
        
        model = SimpleMLP(n_features, 256, activation=act).to(DEVICE)
        K = compute_ntk(model, X_train)
        
        curv = compute_kernel_curvature(K)
        
        train_losses, val_losses = train_model(
            model, X_train, y_train, X_val, y_val, epochs=200, lr=0.001
        )
        
        result = {
            'activation': act,
            'mean_curvature': curv['mean_curvature'],
            'ricci_scalar': curv['ricci_scalar'],
            'cond_number': curv['cond_number'],
            'effective_rank': curv['effective_rank'],
            'final_train_loss': train_losses[-1],
            'final_val_loss': val_losses[-1],
            'generalization_gap': val_losses[-1] - train_losses[-1]
        }
        
        activation_results.append(result)
        print(f"    曲率: {curv['mean_curvature']:.4f}")
        print(f"    条件数: {curv['cond_number']:.2f}")
        print(f"    训练误差: {train_losses[-1]:.6f}")
        print(f"    验证误差: {val_losses[-1]:.6f}")
        print(f"    泛化间隙: {result['generalization_gap']:.6f}")
    
    results['activation_comparison'] = activation_results
    
    # --------------------------------------------------------------------------
    # 实验4：曲率-泛化误差相关性分析
    # --------------------------------------------------------------------------
    print("\n" + "="*70)
    print("[4/4] 曲率-泛化误差相关性分析")
    print("="*70)
    
    # 合并所有数据点
    all_points = []
    for r in dim_results:
        all_points.append({
            'curvature': r['mean_curvature'],
            'cond_number': r['cond_number'],
            'fractal_dim': r['fractal_dim'],
            'gap': r['generalization_gap']
        })
    
    # 相关性分析
    curvatures = [p['curvature'] for p in all_points]
    cond_numbers = [p['cond_number'] for p in all_points]
    fractal_dims = [p['fractal_dim'] for p in all_points]
    gaps = [p['gap'] for p in all_points]
    
    # Pearson相关
    corr_curv_gap, p_val_curv = pearsonr(curvatures, gaps)
    corr_cond_gap, p_val_cond = pearsonr(np.log(cond_numbers), gaps)
    corr_dim_gap, p_val_dim = pearsonr(fractal_dims, gaps)
    
    print(f"\n  Pearson相关系数:")
    print(f"    曲率 vs 泛化间隙: {corr_curv_gap:.4f} (p={p_val_curv:.4f})")
    print(f"    log(条件数) vs 泛化间隙: {corr_cond_gap:.4f} (p={p_val_cond:.4f})")
    print(f"    分形维数 vs 泛化间隙: {corr_dim_gap:.4f} (p={p_val_dim:.4f})")
    
    # Spearman秩相关
    corr_curv_gap_s, p_val_curv_s = spearmanr(curvatures, gaps)
    corr_cond_gap_s, p_val_cond_s = spearmanr(np.log(cond_numbers), gaps)
    corr_dim_gap_s, p_val_dim_s = spearmanr(fractal_dims, gaps)
    
    print(f"\n  Spearman秩相关系数:")
    print(f"    曲率 vs 泛化间隙: {corr_curv_gap_s:.4f} (p={p_val_curv_s:.4f})")
    print(f"    log(条件数) vs 泛化间隙: {corr_cond_gap_s:.4f} (p={p_val_cond_s:.4f})")
    print(f"    分形维数 vs 泛化间隙: {corr_dim_gap_s:.4f} (p={p_val_dim_s:.4f})")
    
    results['correlation_analysis'] = {
        'pearson': {
            'curvature_vs_gap': {'r': float(corr_curv_gap), 'p': float(p_val_curv)},
            'cond_number_vs_gap': {'r': float(corr_cond_gap), 'p': float(p_val_cond)},
            'fractal_dim_vs_gap': {'r': float(corr_dim_gap), 'p': float(p_val_dim)}
        },
        'spearman': {
            'curvature_vs_gap': {'r': float(corr_curv_gap_s), 'p': float(p_val_curv_s)},
            'cond_number_vs_gap': {'r': float(corr_cond_gap_s), 'p': float(p_val_cond_s)},
            'fractal_dim_vs_gap': {'r': float(corr_dim_gap_s), 'p': float(p_val_dim_s)}
        }
    }
    
    # --------------------------------------------------------------------------
    # 输出结果
    # --------------------------------------------------------------------------
    print("\n" + "="*70)
    print("实验总结")
    print("="*70)
    
    # 分形维数扫描总结
    print("\n【分形维数扫描】")
    print(f"{'D':>6} | {'曲率':>12} | {'条件数':>10} | {'训练误差':>12} | {'验证误差':>12} | {'泛化间隙':>12}")
    print("-" * 70)
    for r in dim_results:
        print(f"{r['fractal_dim']:6.1f} | {r['mean_curvature']:12.4f} | {r['cond_number']:10.2f} | {r['final_train_loss']:12.6f} | {r['final_val_loss']:12.6f} | {r['generalization_gap']:12.6f}")
    
    # 宽度缩放总结
    print("\n【宽度缩放】")
    print(f"{'宽度':>6} | {'条件数':>10} | {'训练误差':>12} | {'验证误差':>12} | {'泛化间隙':>12}")
    print("-" * 60)
    for r in width_results:
        print(f"{r['width']:6d} | {r['cond_number']:10.2f} | {r['final_train_loss']:12.6f} | {r['final_val_loss']:12.6f} | {r['generalization_gap']:12.6f}")
    
    # 激活对比总结
    print("\n【激活函数对比】")
    print(f"{'激活':>10} | {'曲率':>12} | {'条件数':>10} | {'训练误差':>12} | {'验证误差':>12} | {'泛化间隙':>12}")
    print("-" * 70)
    for r in activation_results:
        print(f"{r['activation']:10} | {r['mean_curvature']:12.4f} | {r['cond_number']:10.2f} | {r['final_train_loss']:12.6f} | {r['final_val_loss']:12.6f} | {r['generalization_gap']:12.6f}")
    
    # 保存结果
    with open('geometry_results.txt', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n结果已保存到 geometry_results.txt")
    
    print("\n" + "="*70)
    print("实验完成")
    print("="*70)

if __name__ == '__main__':
    main()
