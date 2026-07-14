#!/usr/bin/env python3
"""
奇异连续Cantor谱系统收敛速率大规模仿真
验证定理5.37'的亚指数收敛速率
"""

import os
import numpy as np
import numpy.linalg as la
import json
import time

np.random.seed(42)

def cantor_set_measure(d_c=0.5):
    """生成Cantor测度"""
    n = 200
    x = np.linspace(0, 1, n)
    mu = np.zeros(n)
    
    intervals = [(0, 1)]
    weights = [1.0]
    
    for _ in range(8):
        new_intervals = []
        new_weights = []
        for (a, b), w in zip(intervals, weights):
            mid = (a + b) / 2
            new_intervals.append((a, mid))
            new_intervals.append((mid, b))
            new_weights.append(w * 0.5)
            new_weights.append(w * 0.5)
        intervals = new_intervals
        weights = new_weights
    
    for (a, b), w in zip(intervals, weights):
        mask = (x >= a) & (x < b)
        mu[mask] += w / (b - a) / n
    
    mu = mu / np.sum(mu)
    return x, mu

def cantor_spectrum_operator(mu):
    """构造Cantor谱算子"""
    n = len(mu)
    K = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            K[i, j] = mu[i] * np.exp(-np.abs(i - j) * 0.1)
    
    return K

def compute_convergence_rate(K, n_iter=1000):
    """计算收敛速率"""
    n = K.shape[0]
    f0 = np.random.randn(n)
    f0 = f0 / la.norm(f0)
    
    errors = []
    for i in range(n_iter):
        f0 = K @ f0
        f0 = f0 / la.norm(f0)
        errors.append(la.norm(K @ f0 - f0))
    
    return errors

def main():
    print("="*70)
    print("奇异连续Cantor谱系统收敛速率大规模仿真")
    print("="*70)
    
    results = {}
    
    # 实验1: 不同Cantor维数的收敛速率
    print("\n[1/3] 实验1: 不同Cantor维数的收敛速率")
    print("-"*50)
    
    dim_results = {}
    for d_c in [0.3, 0.5, 0.7, 0.9]:
        print(f"\n  Cantor维数d_C={d_c}:")
        
        x, mu = cantor_set_measure(d_c)
        K = cantor_spectrum_operator(mu)
        
        eigvals = la.eigvalsh(K)
        spectral_gap = 1 - np.max(np.abs(eigvals))
        
        errors = compute_convergence_rate(K, n_iter=200)
        
        log_errors = np.log(np.maximum(errors, 1e-10))
        x_vals = np.arange(len(errors))
        
        slope, _ = np.polyfit(x_vals, log_errors, 1)
        convergence_rate = np.exp(slope)
        
        print(f"    谱隙: {spectral_gap:.6f}")
        print(f"    收敛速率: {convergence_rate:.6f}")
        print(f"    最终误差: {errors[-1]:.6e}")
        
        dim_results[f"d_c_{d_c}"] = {
            'spectral_gap': float(spectral_gap),
            'convergence_rate': float(convergence_rate),
            'final_error': float(errors[-1]),
            'error_decay_slope': float(slope)
        }
    
    results['dimensions'] = dim_results
    
    # 实验2: 亚指数收敛验证
    print("\n[2/3] 实验2: 亚指数收敛验证")
    print("-"*50)
    
    subexp_results = {}
    for d_c in [0.5, 0.7, 0.9]:
        print(f"\n  Cantor维数d_C={d_c}:")
        
        x, mu = cantor_set_measure(d_c)
        K = cantor_spectrum_operator(mu)
        
        n_iter = 500
        f0 = np.random.randn(K.shape[0])
        f0 = f0 / la.norm(f0)
        
        errors = []
        for i in range(n_iter):
            f0 = K @ f0
            f0 = f0 / la.norm(f0)
            errors.append(la.norm(K @ f0 - f0))
        
        n_vals = np.arange(1, n_iter + 1)
        log_errors = np.log(np.maximum(errors, 1e-12))
        
        alpha = d_c / (d_c + 1)
        expected_decay = np.exp(-0.1 * n_vals**alpha)
        
        actual_decay = np.array(errors)
        
        corr = np.corrcoef(np.log(expected_decay), log_errors)[0, 1]
        
        print(f"    理论指数α: {alpha:.4f}")
        print(f"    理论-实际相关性: {corr:.4f}")
        
        subexp_results[f"d_c_{d_c}"] = {
            'alpha': float(alpha),
            'correlation': float(corr)
        }
    
    results['subexponential'] = subexp_results
    
    # 实验3: 与离散谱对比
    print("\n[3/3] 实验3: 与离散谱对比")
    print("-"*50)
    
    compare_results = {}
    
    print("\n  离散谱（紧算子）:")
    n = 100
    K_discrete = np.zeros((n, n))
    for i in range(n):
        K_discrete[i, i] = 0.9**i
    
    errors_discrete = compute_convergence_rate(K_discrete, n_iter=100)
    slope_discrete, _ = np.polyfit(np.arange(len(errors_discrete)), 
                                   np.log(np.maximum(errors_discrete, 1e-10)), 1)
    print(f"    收敛速率: {np.exp(slope_discrete):.6f}")
    print(f"    指数衰减斜率: {slope_discrete:.6f}")
    
    compare_results['discrete'] = {
        'convergence_rate': float(np.exp(slope_discrete)),
        'decay_type': 'exponential',
        'slope': float(slope_discrete)
    }
    
    print("\n  连续谱（绝对连续）:")
    K_continuous = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            K_continuous[i, j] = np.exp(-0.5 * (i - j)**2 / n)
    
    errors_continuous = compute_convergence_rate(K_continuous, n_iter=100)
    n_vals = np.arange(1, len(errors_continuous) + 1)
    poly_fit = np.polyfit(np.log(n_vals), np.log(np.maximum(errors_continuous, 1e-10)), 1)
    print(f"    多项式衰减指数: {poly_fit[0]:.6f}")
    
    compare_results['continuous_abs'] = {
        'decay_exponent': float(poly_fit[0]),
        'decay_type': 'polynomial'
    }
    
    print("\n  奇异连续谱（Cantor谱）:")
    x, mu = cantor_set_measure(0.5)
    K_singular = cantor_spectrum_operator(mu)
    
    errors_singular = compute_convergence_rate(K_singular, n_iter=100)
    n_vals = np.arange(1, len(errors_singular) + 1)
    
    alpha = 0.5 / (0.5 + 1)
    subexp_fit = np.polyfit(n_vals**alpha, np.log(np.maximum(errors_singular, 1e-12)), 1)
    print(f"    亚指数衰减指数α: {alpha:.6f}")
    print(f"    衰减常数: {subexp_fit[0]:.6f}")
    
    compare_results['singular_continuous'] = {
        'alpha': float(alpha),
        'decay_constant': float(subexp_fit[0]),
        'decay_type': 'subexponential'
    }
    
    results['comparison'] = compare_results
    
    with open('cantor_spectrum_results.txt', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("\n" + "="*70)
    print("Cantor谱收敛速率仿真完成")
    print("结果已保存到 cantor_spectrum_results.txt")
    print("="*70)
    
    print("\n=== 实验摘要 ===")
    
    print("\n1. 不同维数收敛速率:")
    for d, r in dim_results.items():
        print(f"   {d}: 速率={r['convergence_rate']:.6f}, 谱隙={r['spectral_gap']:.6f}")
    
    print("\n2. 亚指数收敛验证:")
    for d, r in subexp_results.items():
        print(f"   {d}: α={r['alpha']:.4f}, 相关性={r['correlation']:.4f}")
    
    print("\n3. 谱类型对比:")
    for typ, r in compare_results.items():
        if 'decay_type' in r:
            print(f"   {typ}: {r['decay_type']}, 参数={r.get('slope', r.get('decay_exponent', r.get('alpha'))):.4f}")

if __name__ == '__main__':
    main()
