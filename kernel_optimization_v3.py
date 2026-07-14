import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt

def standard_model_masses():
    return np.sort(np.array([0.511, 2.2, 4.7, 95, 105.66, 1270, 1776.86, 4180, 173100]))

class HierarchicalIFS:
    """分层IFS测度——不同尺度对应不同谱层"""
    def __init__(self, n_levels=4, base=0.5, n_points=50000):
        self.n_levels = n_levels
        self.factors = [base ** (k+1) for k in range(n_levels)]
        self.probs = [base ** (2*k) for k in range(n_levels)]
        self.probs = np.array(self.probs) / np.sum(self.probs)
        self.points = self._generate(n_points)
    
    def _generate(self, n_points):
        points = np.zeros(n_points)
        n_f = len(self.factors)
        offsets = np.cumsum(self.factors) - self.factors
        offsets = offsets / np.sum(self.factors)
        x = 0.5
        for i in range(n_points):
            idx = np.random.choice(n_f, p=self.probs)
            x = self.factors[idx] * x + offsets[idx]
            points[i] = x
        return points

class MultiScaleKernel:
    """分层多尺度核——每层对应不同σ的Gaussian"""
    def __init__(self, measure, sigmas, weights=None):
        self.measure = measure
        self.sigmas = np.array(sigmas)
        n = len(sigmas)
        if weights is None:
            self.scale_weights = np.array([1/n**2 for _ in range(n)])
            self.scale_weights = self.scale_weights / np.sum(self.scale_weights)
        else:
            self.scale_weights = np.array(weights) / np.sum(weights)
        
        self.sample_points = np.sort(np.random.choice(measure.points, 400, replace=False))
        self.n_samples = len(self.sample_points)
    
    def kernel_3d(self, x, y):
        """返回3维向量值核 (代表不同Cl(6)扇形)"""
        k = np.zeros(3)
        for sigma, w in zip(self.sigmas, self.scale_weights):
            phase = np.exp(-(x - y)**2 / (2 * sigma**2))
            k += w * phase
        return k
    
    def compute_block_TK(self, sigma_idx):
        """对单个σ尺度的T_K构造"""
        n = self.n_samples
        sigma = self.sigmas[sigma_idx]
        K = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                K[i, j] = np.exp(-(self.sample_points[i] - self.sample_points[j])**2 / (2 * sigma**2))
        
        T = np.zeros((n, n))
        weights = np.ones(n) / n
        for i in range(n):
            for j in range(n):
                T[i, j] = K[i, j] * weights[j]
        return T
    
    def compute_combined_TK(self):
        """组合多尺度T_K"""
        combined = np.zeros((self.n_samples, self.n_samples))
        for idx, w in enumerate(self.scale_weights):
            combined += w * self.compute_block_TK(idx)
        return combined

def run_analysis():
    print("=" * 70)
    print("Multi-Scale Kernel Analysis for Mass Spectrum")
    print("=" * 70)
    
    sm_masses = standard_model_masses()
    
    # 分层IFS: 不同尺度
    print("\n1. Generating hierarchical IFS measure...")
    hifs = HierarchicalIFS(n_levels=4, base=0.5, n_points=50000)
    
    # 多尺度σ——跨越6个数量级的质量
    sigma_groups = [
        # 每组包含大、中、小三个尺度
        ([0.5, 0.1, 0.02], [0.2, 0.5, 0.3]),
        ([0.8, 0.15, 0.01, 0.001], [0.1, 0.3, 0.4, 0.2]),
        ([1.0, 0.2, 0.03, 0.002], [0.1, 0.3, 0.3, 0.3]),
        ([0.6, 0.12, 0.02, 0.003], [0.1, 0.4, 0.3, 0.2]),
    ]
    
    best_error = float('inf')
    best = None
    
    for sg_idx, (sigmas, weights) in enumerate(sigma_groups):
        print(f"\n--- Sigma group {sg_idx+1}: {sigmas} ---")
        for _ in range(3):
            kernel = MultiScaleKernel(hifs, sigmas, weights)
            T_combined = kernel.compute_combined_TK()
            
            eigenvalues = la.eigvals(T_combined)
            eigenvalues = np.real(eigenvalues)
            eigenvalues = np.sort(eigenvalues)[::-1][:15]
            
            if len(eigenvalues) < 9 or np.min(eigenvalues) <= 0:
                continue
            
            log_eig = -np.log(np.maximum(eigenvalues[:9], 1e-30))
            log_sm = np.log(sm_masses)
            C = np.exp(np.mean(log_sm - np.log(log_eig)))
            predicted = C * log_eig
            error = np.mean(np.abs(np.log(predicted) - log_sm))
            
            if error < best_error:
                best_error = error
                best = {
                    'sigmas': sigmas,
                    'weights': weights,
                    'eigenvalues': eigenvalues.copy(),
                    'predicted': predicted.copy(),
                    'C': C,
                }
                print(f"  New best! error={error:.4f}, C={C:.2f}")
                print(f"  Top eigenvalues: {np.round(eigenvalues[:9], 6)}")
    
    # 再试一次性构造：不同测度扇形独立计算
    print("\n\n2. Multi-branch independent eigenvalue analysis...")
    ifs_branches = [
        ([0.5, 0.5], [0.5, 0.5], 0.01),
        ([0.3, 0.3, 0.4], [1/3, 1/3, 1/3], 0.05),
        ([0.2, 0.4, 0.4], [0.2, 0.4, 0.4], 0.15),
        ([0.1, 0.2, 0.3, 0.4], [0.25, 0.25, 0.25, 0.25], 0.5),
    ]
    
    all_branch_eigenvalues = []
    for factors, probs, sigma in ifs_branches:
        measure = HierarchicalIFS(n_levels=2, base=0.3, n_points=50000)
        
        from kernel_optimization_v2 import IFSMeasure, FractalSampledKernel
        imeasure = IFSMeasure(factors, probs, n_points=20000)
        kernel = FractalSampledKernel(imeasure, sigma)
        T = kernel.compute_TK()
        ev = kernel.compute_eigenvalues(T, k=5)
        all_branch_eigenvalues.append(ev[0] if len(ev) > 0 else 0)
        print(f"  Branch factors={factors}, sigma={sigma}: top eigenvalue = {ev[0]:.6f}" if len(ev) > 0 else f"  Branch factors={factors}: no eigenvalues")
    
    # 输出最佳结果
    print("\n" + "=" * 70)
    print("Best Multi-Scale Result")
    print("=" * 70)
    r = best
    print(f"Sigmas: {r['sigmas']}")
    print(f"Weights: {np.round(r['weights'], 3)}")
    print(f"C = {r['C']:.2f}")
    print(f"Mean log error: {best_error:.4f}")
    
    print(f"\n{'Index':>6s} | {'SM Mass':>12s} | {'Predicted':>12s} | {'Lambda':>12s} | {'Ratio':>8s}")
    print("-" * 52)
    for i in range(9):
        ratio = r['predicted'][i] / sm_masses[i]
        print(f"{i+1:>6d} | {sm_masses[i]:>12.4f} | {r['predicted'][i]:>12.4f} | {r['eigenvalues'][i]:>12.6f} | {ratio:>8.2f}")
    
    # 绘图
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    ax = axes[0]
    ax.semilogy(range(1, 10), r['eigenvalues'][:9], 'o-', linewidth=2, markersize=8)
    ax.set_xlabel('Index')
    ax.set_ylabel('Eigenvalue (log scale)')
    ax.set_title('T_K Eigenvalues (Best)')
    ax.grid(True)
    
    ax = axes[1]
    indices = np.arange(1, 10)
    ax.plot(indices, np.log10(sm_masses[:9]), 'o-', label='SM', linewidth=2, markersize=8)
    ax.plot(indices, np.log10(r['predicted'][:9]), 's--', label='Predicted', linewidth=2, markersize=8)
    ax.set_xlabel('Particle index')
    ax.set_ylabel('log10(mass) [MeV]')
    ax.set_title('Mass Spectrum: SM vs Predicted')
    ax.legend()
    ax.grid(True)
    
    ax = axes[2]
    ax.scatter(np.log10(sm_masses[:9]), np.log10(r['predicted'][:9]), s=80)
    lims = [-1, 6]
    ax.plot(lims, lims, 'r--', label='Perfect')
    ax.set_xlabel('log10(SM mass)')
    ax.set_ylabel('log10(Predicted mass)')
    ax.set_title(f'Correlation (RMSE={best_error:.3f})')
    ax.legend()
    ax.grid(True)
    
    plt.tight_layout()
    plt.savefig('kernel_optimization_v3.png', dpi=300)
    
    with open('kernel_optimization_v3_results.txt', 'w') as f:
        f.write("=== Multi-Scale Kernel Optimization Results ===\n\n")
        f.write(f"Best sigmas: {r['sigmas']}\n")
        f.write(f"Best weights: {np.round(r['weights'], 3)}\n")
        f.write(f"C = {r['C']:.2f}\n")
        f.write(f"Mean log error: {best_error:.4f}\n\n")
        f.write(f"{'Index':>6s} | {'SM Mass':>12s} | {'Predicted':>12s} | {'Lambda':>12s}\n")
        f.write("-" * 44 + "\n")
        for i in range(9):
            f.write(f"{i+1:>6d} | {sm_masses[i]:>12.4f} | {r['predicted'][i]:>12.4f} | {r['eigenvalues'][i]:>12.6f}\n")
    
    print(f"\nResults saved to kernel_optimization_v3_results.txt")
    print(f"Plot saved to kernel_optimization_v3.png")

if __name__ == "__main__":
    run_analysis()