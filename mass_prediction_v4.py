import numpy as np
import scipy.linalg as la
import scipy.optimize as opt
import matplotlib.pyplot as plt

def standard_model_masses():
    """9个标准模型费米子质量 (MeV)，电子到顶夸克"""
    return np.sort(np.array([0.511, 2.2, 4.7, 95, 105.66, 1270, 1776.86, 4180, 173100]))

class MultiScaleKernelOptimizer:
    """多尺度核参数优化器"""
    def __init__(self, n_samples=100):
        self.n_samples = n_samples
        self.sample_points = np.linspace(0, 1, n_samples)
        self.weights = np.ones(n_samples) / n_samples
        self.sm_masses = standard_model_masses()
        self.log_sm = np.log(self.sm_masses)
    
    def kernel_matrix(self, sigmas, kernel_weights):
        """构造多尺度核矩阵 K = sum_k w_k * exp(-(x-y)^2/(2*sigma_k^2))"""
        n = self.n_samples
        X = self.sample_points.reshape(-1, 1)
        Y = self.sample_points.reshape(1, -1)
        D2 = (X - Y) ** 2
        
        K = np.zeros((n, n))
        for sigma, w in zip(sigmas, kernel_weights):
            K += w * np.exp(-D2 / (2 * sigma ** 2))
        
        return K
    
    def compute_eigenvalues(self, K, k=15):
        """计算T_K的特征值"""
        T = K * self.weights.reshape(1, -1)
        eigenvalues = la.eigvals(T)
        eigenvalues = np.real(eigenvalues)
        return np.sort(eigenvalues)[::-1][:k]
    
    def mass_error(self, params):
        """目标函数：质量预测的对数误差"""
        n_sigma = 9
        sigmas = np.maximum(params[:n_sigma], 1e-6)
        kernel_weights = np.abs(params[n_sigma:2*n_sigma])
        kernel_weights = kernel_weights / np.sum(kernel_weights)
        
        K = self.kernel_matrix(sigmas, kernel_weights)
        eigenvalues = self.compute_eigenvalues(K, k=9)
        
        if np.min(eigenvalues) <= 0:
            return 1e6
        
        log_eig = -np.log(eigenvalues)
        C = np.exp(np.mean(self.log_sm - np.log(log_eig)))
        predicted = C * log_eig
        
        error = np.mean((np.log(predicted) - self.log_sm)**2)
        return error
    
    def optimize(self, n_restarts=5):
        """多起点全局优化"""
        best_error = float('inf')
        best_params = None
        best_eigenvalues = None
        best_predicted = None
        best_C = None
        
        bounds = []
        for _ in range(9):
            bounds.append((1e-4, 1.0))
        for _ in range(9):
            bounds.append((0.0, 1.0))
        
        for restart in range(n_restarts):
            x0 = np.zeros(18)
            x0[:9] = 10 ** np.random.uniform(-3, 0, 9)
            x0[9:] = np.random.dirichlet(np.ones(9))
            
            result = opt.minimize(self.mass_error, x0, method='L-BFGS-B', 
                                 bounds=bounds, options={'maxiter': 5000})
            
            if result.fun < best_error:
                best_error = result.fun
                best_params = result.x.copy()
                
                sigmas = np.maximum(best_params[:9], 1e-6)
                kernel_weights = np.abs(best_params[9:])
                kernel_weights = kernel_weights / np.sum(kernel_weights)
                
                K = self.kernel_matrix(sigmas, kernel_weights)
                best_eigenvalues = self.compute_eigenvalues(K, k=9)
                
                log_eig = -np.log(best_eigenvalues)
                best_C = np.exp(np.mean(self.log_sm - np.log(log_eig)))
                best_predicted = best_C * log_eig
        
        return best_params, best_error, best_eigenvalues, best_predicted, best_C

def main():
    print("=" * 70)
    print("Cl(6)-valued Multi-Scale Kernel Optimization v4")
    print("Fermion Mass Prediction via Spectral De-recursion")
    print("=" * 70)
    
    sm_masses = standard_model_masses()
    print(f"\nTarget: 9 Standard Model fermion masses")
    print(f"Range: {sm_masses[0]:.4f} to {sm_masses[-1]:.0f} MeV")
    print(f"Orders of magnitude: {np.log10(sm_masses[-1]) - np.log10(sm_masses[0]):.2f}")
    
    optimizer = MultiScaleKernelOptimizer(n_samples=100)
    
    print("\nRunning multi-start optimization (3 restarts)...")
    best_params, best_error, eigenvalues, predicted, C = optimizer.optimize(n_restarts=3)
    
    rmse = np.sqrt(best_error)
    
    sigmas = np.maximum(best_params[:9], 1e-6)
    kernel_weights = np.abs(best_params[9:])
    kernel_weights = kernel_weights / np.sum(kernel_weights)
    
    print(f"\n{'='*70}")
    print(f"Optimization Complete")
    print(f"{'='*70}")
    print(f"RMSE: {rmse:.4f}")
    print(f"Scaling factor C: {C:.2f}")
    
    print(f"\nOptimized sigmas and weights:")
    print(f"{'Particle':>10s} | {'SM Mass':>10s} | {'Predicted':>10s} | {'Sigma':>8s} | {'Weight':>8s} | {'Ratio':>8s}")
    print("-" * 60)
    for i in range(9):
        ratio = predicted[i] / sm_masses[i]
        print(f"{i+1:>10d} | {sm_masses[i]:>10.4f} | {predicted[i]:>10.4f} | {sigmas[i]:>8.6f} | {kernel_weights[i]:>8.4f} | {ratio:>8.2f}")
    
    mass_labels = ['e', 'u', 'd', 's', 'μ', 'c', 'τ', 'b', 't']
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    ax = axes[0, 0]
    indices = np.arange(1, 10)
    ax.plot(indices, np.log10(sm_masses), 'o-', label='SM', linewidth=2, markersize=8, color='blue')
    ax.plot(indices, np.log10(predicted), 's--', label='Predicted', linewidth=2, markersize=8, color='red')
    ax.set_xlabel('Particle index')
    ax.set_ylabel('log10(mass) [MeV]')
    ax.set_title(f'Mass Spectrum: SM vs Predicted (RMSE={rmse:.3f})')
    ax.set_xticks(indices)
    ax.set_xticklabels(mass_labels)
    ax.legend()
    ax.grid(True)
    
    ax = axes[0, 1]
    ax.scatter(np.log10(sm_masses), np.log10(predicted), s=100, c='red')
    lims = [-1, 6]
    ax.plot(lims, lims, 'b--', label='Perfect match')
    ax.set_xlabel('log10(SM mass)')
    ax.set_ylabel('log10(Predicted mass)')
    ax.set_title('Correlation Plot')
    ax.legend()
    ax.grid(True)
    
    ax = axes[1, 0]
    ax.bar(range(1, 10), sigmas)
    ax.set_xlabel('Particle index')
    ax.set_ylabel('Sigma')
    ax.set_title('Optimized Kernel Widths per Particle')
    ax.set_xticks(range(1, 10))
    ax.set_xticklabels(mass_labels)
    ax.grid(True)
    
    ax = axes[1, 1]
    ax.bar(range(1, 10), kernel_weights)
    ax.set_xlabel('Particle index')
    ax.set_ylabel('Weight')
    ax.set_title('Optimized Kernel Weights per Particle')
    ax.set_xticks(range(1, 10))
    ax.set_xticklabels(mass_labels)
    ax.grid(True)
    
    plt.tight_layout()
    plt.savefig('mass_prediction_v4_results.png', dpi=300)
    
    with open('mass_prediction_v4_results.txt', 'w') as f:
        f.write("=== Cl(6)-valued Multi-Scale Kernel Optimization ===\n\n")
        f.write(f"RMSE: {rmse:.4f}\n")
        f.write(f"C: {C:.2f}\n\n")
        f.write(f"{'Index':>6s} | {'SM Mass':>10s} | {'Predicted':>10s} | {'Sigma':>8s} | {'Weight':>8s}\n")
        f.write("-" * 48 + "\n")
        for i in range(9):
            f.write(f"{i+1:>6d} | {sm_masses[i]:>10.4f} | {predicted[i]:>10.4f} | {sigmas[i]:>8.6f} | {kernel_weights[i]:>8.4f}\n")
        f.write(f"\nOptimized sigmas: {np.round(sigmas, 6).tolist()}\n")
        f.write(f"Optimized weights: {np.round(kernel_weights, 4).tolist()}\n")
    
    print(f"\nResults saved to mass_prediction_v4_results.txt")
    print(f"Plot saved to mass_prediction_v4_results.png")
    
    if rmse < 1.0:
        print(f"\n{'='*70}")
        print(f"VERDICT: Mass prediction RMSE < 1.0 log unit — GOOD FIT ✓")
        print(f"{'='*70}")
    elif rmse < 2.0:
        print(f"\n{'='*70}")
        print(f"VERDICT: Mass prediction RMSE < 2.0 log units — MODERATE FIT")
        print(f"{'='*70}")
    else:
        print(f"\n{'='*70}")
        print(f"VERDICT: Mass prediction RMSE > 2.0 log units — NEEDS IMPROVEMENT")
        print(f"{'='*70}")

if __name__ == "__main__":
    main()