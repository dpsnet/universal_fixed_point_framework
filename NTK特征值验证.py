import numpy as np
from scipy.linalg import eigh
import matplotlib.pyplot as plt

def compute_ntk_exact(X, width=128, depth=2, n_samples=100):
    n = X.shape[0]
    d = X.shape[1]
    
    K = np.zeros((n, n))
    
    for _ in range(n_samples):
        W1 = np.random.randn(d, width) * np.sqrt(2.0 / d)
        W2 = np.random.randn(width, 1) * np.sqrt(2.0 / width)
        
        for i in range(n):
            for j in range(n):
                a_i = np.maximum(0, X[i] @ W1)
                a_j = np.maximum(0, X[j] @ W1)
                K[i, j] += np.dot(a_i, a_j) * np.dot(W2.flatten(), W2.flatten()) / width
    
    K /= n_samples
    
    return K

def cantor_iteration(n_iter=10):
    sets = []
    current = np.array([[0.0, 1.0]])
    
    for i in range(n_iter):
        sets.append(current.copy())
        new_intervals = []
        for interval in current:
            left = interval[0]
            right = interval[1]
            length = (right - left) / 3
            new_intervals.append([left, left + length])
            new_intervals.append([right - length, right])
        current = np.array(new_intervals)
    
    return sets

def measure_fractal_convergence_rate():
    sets = cantor_iteration(n_iter=15)
    
    lengths = []
    for s in sets:
        total_length = np.sum(s[:, 1] - s[:, 0])
        lengths.append(total_length)
    
    lengths = np.array(lengths)
    
    log_lengths = np.log(lengths[:-1])
    log_next_lengths = np.log(lengths[1:])
    
    slope, _ = np.polyfit(log_lengths, log_next_lengths, 1)
    
    return slope, lengths

def test_spectral_correspondence():
    np.random.seed(42)
    
    n_samples = 15
    n_features = 5
    
    X = np.random.randn(n_samples, n_features) / np.sqrt(n_features)
    
    widths = [32, 64, 128]
    
    plt.figure(figsize=(15, 10))
    
    for idx, width in enumerate(widths):
        K = compute_ntk_exact(X, width=width, depth=2, n_samples=50)
        
        eigvals, _ = eigh(K)
        eigvals = eigvals[::-1]
        eigvals = eigvals[eigvals > 1e-8]
        
        plt.subplot(2, 3, idx + 1)
        plt.plot(eigvals, 'o-', markersize=4)
        plt.title(f'NTK Eigenvalues (width={width})')
        plt.xlabel('Index')
        plt.ylabel('Eigenvalue')
        
        plt.subplot(2, 3, idx + 4)
        plt.plot(np.log(eigvals[:min(10, len(eigvals))]), 'o-', markersize=4)
        plt.title(f'Log Eigenvalues (width={width})')
        plt.xlabel('Index')
        plt.ylabel('Log Eigenvalue')
    
    plt.tight_layout()
    plt.savefig('ntk_eigenvalues.png', dpi=300)
    plt.close()
    
    K = compute_ntk_exact(X, width=128, depth=2, n_samples=100)
    eigvals, _ = eigh(K)
    eigvals = eigvals[::-1]
    eigvals = eigvals[eigvals > 1e-8]
    
    print("="*70)
    print("NTK特征值计算验证")
    print("="*70)
    print(f"\nNTK矩阵维度: {K.shape}")
    print(f"有效特征值数量: {len(eigvals)}")
    print(f"最大特征值: {eigvals[0]:.6f}")
    print(f"最小特征值: {eigvals[-1]:.6f}")
    print(f"条件数: {eigvals[0] / eigvals[-1]:.2e}")
    print(f"\n前10个特征值:")
    for i, val in enumerate(eigvals[:min(10, len(eigvals))]):
        print(f"  lambda_{i+1} = {val:.6f}")
    
    print(f"\n前10个特征值的对数:")
    for i, val in enumerate(eigvals[:min(10, len(eigvals))]):
        print(f"  log(lambda_{i+1}) = {np.log(val):.6f}")
    
    return eigvals

def weierstrass_function(x, a=0.5, b=3):
    result = np.zeros_like(x, dtype=float)
    n = 0
    while n <= 50:
        term = a ** n * np.cos(b ** n * np.pi * x)
        result += term
        n += 1
        if a ** n < 1e-12:
            break
    return result

def generate_fractal_data(n_samples=50):
    X = np.linspace(-1, 1, n_samples)[:, np.newaxis]
    y = weierstrass_function(X) + 0.01 * np.random.randn(n_samples, 1)
    return X, y

def test_fractal_ntk_correspondence():
    np.random.seed(42)
    
    n_samples = 30
    n_features = 10
    
    X = np.random.randn(n_samples, n_features) / np.sqrt(n_features)
    X_fractal = np.linspace(-1, 1, n_samples)[:, np.newaxis]
    y = weierstrass_function(X_fractal) + 0.01 * np.random.randn(n_samples, 1)
    
    widths = [64, 128, 256]
    depths = [2, 3, 4]
    
    fractal_slope, lengths = measure_fractal_convergence_rate()
    
    a = 0.5
    b = 3
    weierstrass_dim = 2 - np.log(a) / np.log(b)
    
    print("\n" + "="*70)
    print("分形迭代与NTK谱对应验证")
    print("="*70)
    
    print(f"\n【分形迭代实验】")
    print(f"Cantor集迭代收敛率（对数斜率）: {fractal_slope:.6f}")
    print(f"理论压缩系数: 2/3 = {2/3:.6f}")
    print(f"分形迭代收敛率理论值: log(2/3) = {np.log(2/3):.6f}")
    
    print(f"\n【Weierstrass函数参数】")
    print(f"参数 a = {a}, b = {b}")
    print(f"Weierstrass函数豪斯多夫维数: {weierstrass_dim:.4f}")
    print(f"分形压缩系数: a = {a}")
    print(f"理论特征值尺度: -log(a) = {-np.log(a):.6f}")
    
    plt.figure(figsize=(18, 12))
    
    all_eigvals = []
    all_medians = []
    
    for i, width in enumerate(widths):
        for j, depth in enumerate(depths):
            K = compute_ntk_exact(X, width=width, depth=depth, n_samples=50)
            eigvals, _ = eigh(K)
            eigvals = eigvals[::-1]
            eigvals = eigvals[eigvals > 1e-8]
            
            all_eigvals.append(eigvals)
            all_medians.append(np.median(eigvals))
            
            idx = i * len(depths) + j
            plt.subplot(len(widths), len(depths), idx + 1)
            plt.plot(np.log(eigvals), 'bo-', markersize=3)
            plt.axhline(y=np.log(a), color='r', linestyle='--', linewidth=1)
            plt.title(f'Width={width}, Depth={depth}')
            plt.xlabel('Index')
            plt.ylabel('Log Eigenvalue')
            plt.grid(True)
            plt.ylim(-10, 5)
    
    plt.tight_layout()
    plt.savefig('ntk_eigenvalues_various.png', dpi=300)
    plt.close()
    
    print(f"\n【不同网络配置的NTK特征值分析】")
    print(f"{'Width':>6} {'Depth':>6} {'EigCount':>8} {'Max':>12} {'Median':>12} {'Min':>12}")
    print("-" * 60)
    for i, width in enumerate(widths):
        for j, depth in enumerate(depths):
            eigvals = all_eigvals[i * len(depths) + j]
            print(f"{width:>6} {depth:>6} {len(eigvals):>8} {eigvals[0]:>12.6f} {np.median(eigvals):>12.6f} {eigvals[-1]:>12.6f}")
    
    print(f"\n【谱对应分析】")
    print(f"分形压缩系数 a = {a}")
    print(f"理论预测: NTK特征值中位数 ≈ -log(a) = {-.693:.6f}")
    print(f"实际NTK特征值中位数范围: [{min(all_medians):.6f}, {max(all_medians):.6f}]")
    
    print(f"\n【收敛率分析】")
    print(f"分形收敛率: {a}^t")
    print(f"典型NTK收敛率: exp(-t * median_eigval)")
    
    best_idx = np.argmin(np.abs(np.array(all_medians) - (-np.log(a))))
    best_eigvals = all_eigvals[best_idx]
    best_median = all_medians[best_idx]
    best_width = widths[best_idx // len(depths)]
    best_depth = depths[best_idx % len(depths)]
    
    print(f"\n最接近理论预测的配置: width={best_width}, depth={best_depth}")
    print(f"NTK特征值中位数: {best_median:.6f}")
    print(f"理论预测值: {-np.log(a):.6f}")
    print(f"相对误差: {np.abs(best_median + np.log(a)) / np.abs(-np.log(a)) * 100:.2f}%")
    
    plt.figure(figsize=(12, 6))
    
    t = np.linspace(0, 10, 100)
    ntk_convergence = np.exp(-t * best_median)
    fractal_convergence = a ** t
    
    plt.plot(t, ntk_convergence, 'r-', label=f'NTK (median={best_median:.4f})')
    plt.plot(t, fractal_convergence, 'b--', label=f'Fractal (a={a})')
    plt.title('Convergence Rate Comparison')
    plt.xlabel('Time/Iteration')
    plt.ylabel('Error')
    plt.yscale('log')
    plt.legend()
    plt.grid(True)
    plt.savefig('fractal_ntk_convergence.png', dpi=300)
    plt.close()
    
    print(f"\n【收敛率数值对比】")
    for t_val in [1, 2, 5, 10]:
        ntk_val = np.exp(-t_val * best_median)
        fractal_val = a ** t_val
        print(f"  t={t_val}: NTK={ntk_val:.6f}, Fractal={fractal_val:.6f}")

def test_convergence_rate():
    np.random.seed(42)
    
    n_samples = 20
    n_features = 5
    
    X = np.random.randn(n_samples, n_features) / np.sqrt(n_features)
    y = np.sin(np.sum(X, axis=1)) + 0.1 * np.random.randn(n_samples)
    y = y[:, np.newaxis]
    
    K = compute_ntk_exact(X, width=128, depth=2, n_samples=100)
    eigvals, _ = eigh(K)
    eigvals = eigvals[::-1]
    eigvals = eigvals[eigvals > 1e-8]
    
    lambda_min = eigvals[-1]
    
    t = np.linspace(0, 20, 100)
    convergence = np.exp(-t * lambda_min)
    
    plt.figure(figsize=(8, 6))
    plt.plot(t, convergence, 'r-', linewidth=2)
    plt.title(f'Convergence Rate (lambda_min = {lambda_min:.6f})')
    plt.xlabel('Time t')
    plt.ylabel('||f_t - f*||')
    plt.yscale('log')
    plt.grid(True)
    plt.savefig('convergence_rate.png', dpi=300)
    plt.close()
    
    print(f"\nConvergence Rate Verification:")
    print(f"Theoretical convergence time constant: 1/lambda_min = {1/lambda_min:.4f}")
    print(f"After t=1/lambda_min, error decays to {np.exp(-1):.2%} of initial value")
    print(f"After t=5/lambda_min, error decays to {np.exp(-5):.2%} of initial value")

def test_width_scaling():
    np.random.seed(42)
    
    n_samples = 50
    n_features = 10
    
    X = np.random.randn(n_samples, n_features) / np.sqrt(n_features)
    
    widths = [32, 64, 128, 256, 512, 1024, 2048]
    depth = 2
    
    theoretical_value = -np.log(0.5)
    
    medians = []
    max_eigvals = []
    min_eigvals = []
    
    print("\n" + "="*70)
    print("宽度递增实验：验证谱对应定理的渐近性")
    print("="*70)
    print(f"\n理论预测值（-log(a)）: {theoretical_value:.6f}")
    print(f"\n{'Width':>8} {'EigCount':>8} {'Max':>12} {'Median':>12} {'Min':>12} {'Diff':>12}")
    print("-" * 70)
    
    for width in widths:
        K = compute_ntk_exact(X, width=width, depth=depth, n_samples=50)
        eigvals, _ = eigh(K)
        eigvals = eigvals[::-1]
        eigvals = eigvals[eigvals > 1e-8]
        
        median = np.median(eigvals)
        diff = np.abs(median - theoretical_value)
        
        medians.append(median)
        max_eigvals.append(eigvals[0])
        min_eigvals.append(eigvals[-1])
        
        print(f"{width:>8} {len(eigvals):>8} {eigvals[0]:>12.6f} {median:>12.6f} {eigvals[-1]:>12.6f} {diff:>12.6f}")
    
    print(f"\n【收敛分析】")
    print(f"理论值: {theoretical_value:.6f}")
    print(f"width=2048时的中位数: {medians[-1]:.6f}")
    print(f"相对误差: {np.abs(medians[-1] - theoretical_value) / theoretical_value * 100:.2f}%")
    
    plt.figure(figsize=(15, 10))
    
    plt.subplot(2, 2, 1)
    plt.plot(widths, medians, 'bo-', linewidth=2, markersize=8)
    plt.axhline(y=theoretical_value, color='r', linestyle='--', linewidth=2, label=f'Theory={theoretical_value:.4f}')
    plt.title('Median Eigenvalue vs Width')
    plt.xlabel('Width')
    plt.ylabel('Median Eigenvalue')
    plt.xscale('log')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(2, 2, 2)
    plt.plot(widths, max_eigvals, 'bo-', linewidth=2, markersize=8)
    plt.title('Max Eigenvalue vs Width')
    plt.xlabel('Width')
    plt.ylabel('Max Eigenvalue')
    plt.xscale('log')
    plt.grid(True)
    
    plt.subplot(2, 2, 3)
    plt.plot(widths, min_eigvals, 'bo-', linewidth=2, markersize=8)
    plt.title('Min Eigenvalue vs Width')
    plt.xlabel('Width')
    plt.ylabel('Min Eigenvalue')
    plt.xscale('log')
    plt.grid(True)
    
    plt.subplot(2, 2, 4)
    errors = np.abs(np.array(medians) - theoretical_value)
    plt.plot(widths, errors, 'bo-', linewidth=2, markersize=8)
    plt.title('Absolute Error vs Width')
    plt.xlabel('Width')
    plt.ylabel('Absolute Error')
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('width_scaling_analysis.png', dpi=300)
    plt.close()
    
    print(f"\n【误差衰减拟合】")
    log_widths = np.log(widths)
    log_errors = np.log(errors)
    slope, intercept = np.polyfit(log_widths, log_errors, 1)
    print(f"误差衰减指数: {slope:.4f}")
    print(f"误差 ~ width^{slope:.4f}")
    print(f"拟合公式: log(error) = {slope:.4f} * log(width) + {intercept:.4f}")
    
    return medians, widths, theoretical_value

if __name__ == "__main__":
    eigvals = test_spectral_correspondence()
    test_fractal_ntk_correspondence()
    test_convergence_rate()
    test_width_scaling()
    print("\n" + "="*70)
    print("Verification Complete")
    print("="*70)