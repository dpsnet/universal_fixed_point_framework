import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt

def standard_model_fermion_masses():
    """标准模型费米子质量 (MeV)，按从小到大排序"""
    return np.sort(np.array([0.511, 2.2, 4.7, 95, 105.66, 1270, 1776.86, 4180, 173100]))

class IFSMeasure:
    """带权重的IFS不变测度采样"""
    def __init__(self, contraction_factors, probabilities, n_points=50000):
        self.contraction_factors = np.array(contraction_factors)
        self.probabilities = np.array(probabilities) / np.sum(probabilities)
        self.n_contract = len(contraction_factors)
        
        self.offsets = np.zeros(self.n_contract)
        total = np.sum(contraction_factors)
        cumsum = 0
        for i in range(self.n_contract):
            self.offsets[i] = cumsum / total
            cumsum += contraction_factors[i]
        
        self.points, self.density = self._generate(n_points)
    
    def _generate(self, n_points):
        points = np.zeros(n_points)
        x = 0.5
        for i in range(n_points):
            idx = np.random.choice(self.n_contract, p=self.probabilities)
            x = self.contraction_factors[idx] * x + self.offsets[idx]
            points[i] = x
        
        hist, edges = np.histogram(points, bins=1000, density=True)
        centers = (edges[:-1] + edges[1:]) / 2
        return points, (centers, hist)

class FractalSampledKernel:
    """基于IFS测度采样的分形核函数"""
    def __init__(self, measure, sigma):
        self.measure = measure
        self.sigma = sigma
        
        self.sample_points = np.sort(np.random.choice(measure.points, size=min(500, len(measure.points)), replace=False))
        self.n_samples = len(self.sample_points)
        
        self.weights = self._compute_weights()
    
    def _compute_weights(self):
        """基于IFS测度密度的权重"""
        centers, density = self.measure.density
        weights = np.interp(self.sample_points, centers, density)
        weights = weights / np.sum(weights)
        return weights
    
    def gaussian(self, x, y):
        return np.exp(-(x - y)**2 / (2 * self.sigma**2))
    
    def compute_TK(self):
        """构造分形转移算子T_K矩阵"""
        n = self.n_samples
        K = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                K[i, j] = self.gaussian(self.sample_points[i], self.sample_points[j])
        
        T = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                T[i, j] = K[i, j] * self.weights[j]
        
        return T
    
    def compute_eigenvalues(self, T, k=20):
        eigenvalues = la.eigvals(T)
        eigenvalues = np.real(eigenvalues)
        eigenvalues = np.sort(eigenvalues)[::-1]
        return eigenvalues[:k]

def optimize_parameters():
    print("=" * 70)
    print("Kernel Optimization V2: IFS Measure Sampling")
    print("=" * 70)
    
    sm_masses = standard_model_fermion_masses()
    
    # 网格搜索
    ifs_configs = [
        ([0.5, 0.5], [0.5, 0.5]),
        ([0.3, 0.3, 0.4], [1/3, 1/3, 1/3]),
        ([0.4, 0.3, 0.3], [0.4, 0.3, 0.3]),
        ([0.25, 0.25, 0.25, 0.25], [0.25, 0.25, 0.25, 0.25]),
        ([0.2, 0.2, 0.3, 0.3], [0.25, 0.25, 0.25, 0.25]),
        ([0.3, 0.2, 0.5], [0.3, 0.3, 0.4]),
        ([0.2, 0.4, 0.4], [0.2, 0.4, 0.4]),
        ([0.1, 0.2, 0.3, 0.4], [0.25, 0.25, 0.25, 0.25]),
    ]
    
    sigma_values = [0.01, 0.02, 0.03, 0.05, 0.08, 0.1, 0.15, 0.2]
    n_repeats = 3
    
    best_error = float('inf')
    best_result = None
    all_results = []
    
    for ifs_idx, (factors, probs) in enumerate(ifs_configs):
        print(f"\n--- IFS config {ifs_idx+1}: factors={factors} ---")
        
        measure = IFSMeasure(factors, probs, n_points=20000)
        
        for sigma in sigma_values:
            errors = []
            for _ in range(n_repeats):
                try:
                    kernel = FractalSampledKernel(measure, sigma)
                    T = kernel.compute_TK()
                    eigenvalues = kernel.compute_eigenvalues(T, k=20)
                    
                    if len(eigenvalues) < 9 or np.min(eigenvalues) <= 0:
                        continue
                    
                    log_eig = -np.log(eigenvalues[:9])
                    log_sm = np.log(sm_masses)
                    
                    C = np.exp(np.mean(log_sm - np.log(log_eig)))
                    predicted = C * log_eig
                    error = np.mean(np.abs(np.log(predicted) - log_sm))
                    errors.append(error)
                    
                    if error < best_error:
                        best_error = error
                        best_result = {
                            'ifs_factors': factors,
                            'ifs_probs': probs,
                            'sigma': sigma,
                            'C': C,
                            'eigenvalues': eigenvalues.copy(),
                            'predicted': predicted.copy(),
                            'sample_points': kernel.sample_points.copy(),
                            'weights': kernel.weights.copy(),
                        }
                        print(f"  * New best! sigma={sigma}, error={error:.4f}, C={C:.2f}")
                        print(f"    Top eigenvalues: {np.round(eigenvalues[:9], 6)}")
                except Exception as e:
                    continue
            
            if errors:
                avg_error = np.mean(errors)
                all_results.append((avg_error, ifs_idx, factors, sigma))
    
    # 输出最佳结果
    print("\n" + "=" * 70)
    print("Best Result")
    print("=" * 70)
    r = best_result
    print(f"IFS: factors={r['ifs_factors']}, probs={np.round(r['ifs_probs'], 2)}")
    print(f"sigma={r['sigma']}, C={r['C']:.2f}")
    print(f"Mean log error: {best_error:.4f}")
    
    print(f"\n{'Index':>6s} | {'SM Mass(MeV)':>14s} | {'Predicted(MeV)':>14s} | {'Lambda':>10s} | {'Ratio':>8s}")
    print("-" * 56)
    for i in range(9):
        ratio = r['predicted'][i] / sm_masses[i]
        print(f"{i+1:>6d} | {sm_masses[i]:>14.4f} | {r['predicted'][i]:>14.4f} | {r['eigenvalues'][i]:>10.6f} | {ratio:>8.2f}")
    
    # 绘图
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    
    ax = axes[0, 0]
    ax.hist(r['sample_points'], bins=50, density=True, alpha=0.7)
    ax.set_xlabel('x')
    ax.set_ylabel('Density')
    ax.set_title('IFS Sample Distribution')
    ax.grid(True)
    
    ax = axes[0, 1]
    ax.bar(range(1, 10), r['eigenvalues'][:9])
    ax.set_xlabel('Index')
    ax.set_ylabel('Eigenvalue')
    ax.set_title('T_K Eigenvalues (Best)')
    ax.grid(True)
    
    ax = axes[0, 2]
    ax.plot(r['weights'], 'o-', markersize=2)
    ax.set_xlabel('Sample index')
    ax.set_ylabel('Weight')
    ax.set_title('Sample Weights (IFS density)')
    ax.grid(True)
    
    ax = axes[1, 0]
    indices = np.arange(1, 10)
    ax.plot(indices, np.log10(sm_masses[:9]), 'o-', label='SM', linewidth=2, markersize=8)
    ax.plot(indices, np.log10(r['predicted'][:9]), 's--', label='Predicted', linewidth=2, markersize=8)
    ax.set_xlabel('Particle index')
    ax.set_ylabel('log10(mass) [MeV]')
    ax.set_title('Mass Spectrum Comparison')
    ax.legend()
    ax.grid(True)
    
    ax = axes[1, 1]
    ax.scatter(np.log10(sm_masses[:9]), np.log10(r['predicted'][:9]), s=100)
    lims = [min(np.log10(sm_masses.min()), np.log10(r['predicted'][:9].min())),
            max(np.log10(sm_masses.max()), np.log10(r['predicted'][:9].max()))]
    ax.plot(lims, lims, 'r--', label='Perfect')
    ax.set_xlabel('log10(SM mass)')
    ax.set_ylabel('log10(Predicted mass)')
    ax.set_title('Correlation')
    ax.legend()
    ax.grid(True)
    
    ax = axes[1, 2]
    ax.plot(np.log10(sm_masses[:9]), r['eigenvalues'][:9], 'o-')
    ax.set_xlabel('log10(SM mass)')
    ax.set_ylabel('Eigenvalue λ')
    ax.set_title('Eigenvalue Decay vs Mass')
    ax.grid(True)
    
    plt.tight_layout()
    plt.savefig('kernel_optimization_v2.png', dpi=300)
    
    with open('kernel_optimization_v2_results.txt', 'w') as f:
        f.write("=== Kernel Optimization V2 Results ===\n\n")
        f.write(f"Best parameters:\n")
        f.write(f"  IFS factors: {r['ifs_factors']}\n")
        f.write(f"  IFS probs: {np.round(r['ifs_probs'], 2)}\n")
        f.write(f"  sigma: {r['sigma']}\n")
        f.write(f"  scaling C: {r['C']:.2f}\n")
        f.write(f"  Mean log error: {best_error:.4f}\n\n")
        f.write(f"{'Index':>6s} | {'SM Mass':>12s} | {'Predicted':>12s} | {'Lambda':>12s}\n")
        f.write("-" * 44 + "\n")
        for i in range(9):
            f.write(f"{i+1:>6d} | {sm_masses[i]:>12.4f} | {r['predicted'][i]:>12.4f} | {r['eigenvalues'][i]:>12.6f}\n")
    
    print(f"\nResults saved to kernel_optimization_v2_results.txt")
    print(f"Plot saved to kernel_optimization_v2.png")

if __name__ == "__main__":
    optimize_parameters()