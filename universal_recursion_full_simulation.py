#!/usr/bin/env python3
"""
七大通用递归系统大规模仿真
包含：IFS不动点、Julia伪谱、RG临界指数、量子行走等完整实验
"""

import os
import numpy as np
import numpy.linalg as la
import torch
import time
import json

np.random.seed(42)

def ifs_fixed_point_experiment():
    """IFS不动点闭式求解对比迭代法耗时"""
    print("\n[1/7] IFS不动点实验")
    print("-"*50)
    
    results = {}
    
    for c in [0.3, 0.5, 0.7]:
        print(f"\n  压缩系数c={c}:")
        
        w1 = lambda x, y: (c * x, c * y)
        w2 = lambda x, y: (c * x + 0.5, c * y)
        w3 = lambda x, y: (c * x + 0.25, c * y + 0.5)
        
        n_iter = 1000
        x, y = 0.0, 0.0
        
        start_time = time.time()
        for _ in range(n_iter):
            r = np.random.rand()
            if r < 1/3:
                x, y = w1(x, y)
            elif r < 2/3:
                x, y = w2(x, y)
            else:
                x, y = w3(x, y)
        iter_time = time.time() - start_time
        
        closed_form_x = 0.25 / (1 - c)
        closed_form_y = 0.25 / (1 - c)
        
        error = np.sqrt((x - closed_form_x)**2 + (y - closed_form_y)**2)
        
        print(f"    迭代法耗时: {iter_time*1000:.4f}ms")
        print(f"    迭代结果: ({x:.6f}, {y:.6f})")
        print(f"    闭式解: ({closed_form_x:.6f}, {closed_form_y:.6f})")
        print(f"    误差: {error:.6f}")
        
        results[f"c_{c}"] = {
            'iter_time_ms': iter_time * 1000,
            'iter_result': [x, y],
            'closed_form': [closed_form_x, closed_form_y],
            'error': error
        }
    
    return results

def julia_pseudospectrum_experiment():
    """Julia集伪谱数值仿真"""
    print("\n[2/7] Julia集伪谱实验")
    print("-"*50)
    
    results = {}
    
    for c in [-0.8+0.156j, 0.285+0.01j, -0.4+0.6j]:
        print(f"\n  参数c={c}:")
        
        n = 64
        x = np.linspace(-2, 2, n)
        y = np.linspace(-2, 2, n)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y
        
        escape_time = np.zeros_like(Z, dtype=int)
        mask = np.ones_like(Z, dtype=bool)
        
        start_time = time.time()
        for i in range(100):
            Z[mask] = Z[mask]**2 + c
            mask = mask & (np.abs(Z) < 2)
            escape_time[mask] = i
        comp_time = time.time() - start_time
        
        n_points = np.sum(escape_time > 50)
        fractal_dim = np.log(n_points) / np.log(n) if n_points > 0 else 0
        
        nonnormality = np.abs(c.real**2 + c.imag**2 - 1)
        
        print(f"    计算耗时: {comp_time:.4f}s")
        print(f"    分形点数: {n_points}")
        print(f"    估计分形维数: {fractal_dim:.4f}")
        print(f"    非正规度: {nonnormality:.4f}")
        
        results[f"c_{c.real:.2f}_{c.imag:.2f}"] = {
            'comp_time': comp_time,
            'n_fractal_points': int(n_points),
            'estimated_dim': float(fractal_dim),
            'nonnormality': float(nonnormality)
        }
    
    return results

def l_system_experiment():
    """L系统生长率与PF特征值匹配"""
    print("\n[3/7] L系统实验")
    print("-"*50)
    
    results = {}
    
    for rule in ['koch', 'sierpinski', 'dragon']:
        print(f"\n  规则={rule}:")
        
        if rule == 'koch':
            pf_matrix = np.array([[1, 1, 1], [1, 0, 0], [0, 1, 0]])
            expected_dim = np.log(4) / np.log(3)
        elif rule == 'sierpinski':
            pf_matrix = np.array([[2, 1], [1, 1]])
            expected_dim = np.log(3) / np.log(2)
        else:
            pf_matrix = np.array([[1, 1], [1, 0]])
            expected_dim = np.log((1+np.sqrt(5))/2) / np.log(2)
        
        eigvals = la.eigvals(pf_matrix)
        pf_eigval = np.max(np.abs(eigvals))
        actual_dim = np.log(pf_eigval) / np.log(2)
        
        print(f"    PF特征值: {pf_eigval:.6f}")
        print(f"    理论分形维数: {expected_dim:.6f}")
        print(f"    实际分形维数: {actual_dim:.6f}")
        print(f"    误差: {np.abs(expected_dim - actual_dim):.6f}")
        
        results[rule] = {
            'pf_eigval': float(pf_eigval),
            'theoretical_dim': float(expected_dim),
            'actual_dim': float(actual_dim),
            'error': float(np.abs(expected_dim - actual_dim))
        }
    
    return results

def wavelet_subdivision_experiment():
    """小波细分收敛性与正则性"""
    print("\n[4/7] 小波细分实验")
    print("-"*50)
    
    results = {}
    
    for wavelet in ['haar', 'db2', 'db4']:
        print(f"\n  小波={wavelet}:")
        
        if wavelet == 'haar':
            mask = np.array([1, 1]) / np.sqrt(2)
            expected_regularity = 0.5
        elif wavelet == 'db2':
            mask = np.array([0.48296, 0.8365, 0.22414, -0.12941])
            expected_regularity = 1.0
        else:
            mask = np.array([0.23038, 0.71485, 0.63088, -0.02798, 
                            -0.18704, 0.03084, 0.03288, -0.01059])
            expected_regularity = 2.0
        
        n = 128
        x = np.linspace(0, 1, n)
        f = np.sin(2 * np.pi * x)
        
        for _ in range(5):
            f = np.convolve(f, mask, mode='same')
        
        residual = np.sin(2 * np.pi * x) - f
        l2_error = la.norm(residual)
        
        print(f"    L2误差: {l2_error:.6f}")
        print(f"    理论正则性: {expected_regularity}")
        
        results[wavelet] = {
            'l2_error': float(l2_error),
            'expected_regularity': expected_regularity
        }
    
    return results

def renormalization_group_experiment():
    """重整化群临界指数谱匹配"""
    print("\n[5/7] 重整化群实验")
    print("-"*50)
    
    results = {}
    
    for d in [1, 2, 3]:
        print(f"\n  维度d={d}:")
        
        if d == 1:
            expected_nu = 1.0
            expected_alpha = 0.0
        elif d == 2:
            expected_nu = 1.0
            expected_alpha = 0.0
        else:
            expected_nu = 0.630
            expected_alpha = 0.110
        
        n = 50
        rg_matrix = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                if i == j:
                    rg_matrix[i, j] = 2**(d-1)
                elif np.abs(i-j) == 1:
                    rg_matrix[i, j] = -2**(d-2)
        
        eigvals = la.eigvals(rg_matrix)
        max_eigval = np.max(np.real(eigvals))
        
        nu_estimate = 1 / np.log(max_eigval) * np.log(2)
        
        print(f"    RG最大特征值: {max_eigval:.6f}")
        print(f"    理论临界指数ν: {expected_nu:.6f}")
        print(f"    估计临界指数ν: {nu_estimate:.6f}")
        print(f"    误差: {np.abs(expected_nu - nu_estimate):.6f}")
        
        results[f"d_{d}"] = {
            'max_eigval': float(max_eigval),
            'theoretical_nu': float(expected_nu),
            'estimated_nu': float(nu_estimate),
            'error': float(np.abs(expected_nu - nu_estimate))
        }
    
    return results

def quantum_walk_experiment():
    """量子行走酉算子谱演化"""
    print("\n[6/7] 量子行走实验")
    print("-"*50)
    
    results = {}
    
    for n_steps in [10, 20, 50]:
        print(f"\n  步数={n_steps}:")
        
        n = 21
        shift_op = np.zeros((n, n))
        for i in range(n-1):
            shift_op[i, i+1] = 1
            shift_op[i+1, i] = 1
        
        coin_op = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
        
        U = np.kron(shift_op, np.eye(2)) @ np.kron(np.eye(n), coin_op)
        
        eigvals = la.eigvals(U)
        spectrum = np.abs(eigvals)
        
        psi0 = np.zeros(2 * n)
        psi0[n] = 1
        
        psi_n = psi0
        for _ in range(n_steps):
            psi_n = U @ psi_n
        
        prob = np.abs(psi_n)**2
        variance = np.var(prob)
        
        print(f"    谱半径: {np.max(spectrum):.6f}")
        print(f"    谱方差: {np.var(spectrum):.6f}")
        print(f"    概率分布方差: {variance:.6f}")
        
        results[f"steps_{n_steps}"] = {
            'spectral_radius': float(np.max(spectrum)),
            'spectral_variance': float(np.var(spectrum)),
            'probability_variance': float(variance)
        }
    
    return results

def neural_network_experiment():
    """神经网络训练动力学"""
    print("\n[7/7] 神经网络实验")
    print("-"*50)
    
    results = {}
    
    for width in [64, 128, 256]:
        print(f"\n  宽度={width}:")
        
        n_samples = 100
        n_features = 50
        X = np.random.randn(n_samples, n_features)
        y = np.random.randint(0, 2, n_samples)
        
        W1 = np.random.randn(width, n_features) * np.sqrt(2 / n_features)
        W2 = np.random.randn(2, width) * np.sqrt(2 / width)
        
        lr = 0.01
        n_epochs = 50
        
        start_time = time.time()
        for epoch in range(n_epochs):
            Z1 = 1 / (1 + np.exp(-X @ W1.T))
            Z2 = Z1 @ W2.T
            probs = np.exp(Z2) / np.sum(np.exp(Z2), axis=1, keepdims=True)
            
            grad_W2 = Z1.T @ (probs - (y.reshape(-1,1) == np.arange(2))) / n_samples
            grad_W1 = X.T @ ((probs - (y.reshape(-1,1) == np.arange(2))) @ W2 * Z1 * (1 - Z1)) / n_samples
            
            W1 -= lr * grad_W1.T
            W2 -= lr * grad_W2.T
        
        train_time = time.time() - start_time
        
        Z1 = 1 / (1 + np.exp(-X @ W1.T))
        Z2 = Z1 @ W2.T
        acc = np.mean(np.argmax(Z2, axis=1) == y)
        
        print(f"    训练耗时: {train_time:.4f}s")
        print(f"    训练精度: {acc:.4f}")
        
        results[f"width_{width}"] = {
            'train_time': float(train_time),
            'accuracy': float(acc)
        }
    
    return results

def main():
    print("="*70)
    print("七大通用递归系统大规模仿真")
    print("="*70)
    
    results = {}
    
    results['ifs'] = ifs_fixed_point_experiment()
    results['julia'] = julia_pseudospectrum_experiment()
    results['l_system'] = l_system_experiment()
    results['wavelet'] = wavelet_subdivision_experiment()
    results['renormalization_group'] = renormalization_group_experiment()
    results['quantum_walk'] = quantum_walk_experiment()
    results['neural_network'] = neural_network_experiment()
    
    with open('universal_recursion_full_results.txt', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("\n" + "="*70)
    print("七大通用递归系统仿真完成")
    print("结果已保存到 universal_recursion_full_results.txt")
    print("="*70)
    
    print("\n=== 实验摘要 ===")
    
    print("\n1. IFS不动点:")
    for c, r in results['ifs'].items():
        print(f"   {c}: 误差={r['error']:.6f}, 耗时={r['iter_time_ms']:.4f}ms")
    
    print("\n2. Julia伪谱:")
    for c, r in results['julia'].items():
        print(f"   {c}: 维数={r['estimated_dim']:.4f}, 非正规度={r['nonnormality']:.4f}")
    
    print("\n3. L系统:")
    for rule, r in results['l_system'].items():
        print(f"   {rule}: PF特征值={r['pf_eigval']:.4f}, 维数误差={r['error']:.6f}")
    
    print("\n4. 小波细分:")
    for wavelet, r in results['wavelet'].items():
        print(f"   {wavelet}: L2误差={r['l2_error']:.6f}")
    
    print("\n5. 重整化群:")
    for d, r in results['renormalization_group'].items():
        print(f"   {d}: ν={r['estimated_nu']:.4f}, 误差={r['error']:.6f}")
    
    print("\n6. 量子行走:")
    for steps, r in results['quantum_walk'].items():
        print(f"   {steps}: 谱半径={r['spectral_radius']:.4f}")
    
    print("\n7. 神经网络:")
    for width, r in results['neural_network'].items():
        print(f"   {width}: 精度={r['accuracy']:.4f}, 耗时={r['train_time']:.4f}s")

if __name__ == '__main__':
    main()
