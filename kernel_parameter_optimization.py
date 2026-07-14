import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt
from itertools import product

def standard_model_fermion_masses():
    """返回标准模型费米子质量 (MeV)，按从小到大排序"""
    masses = np.array([0.511, 2.2, 4.7, 95, 105.66, 1270, 1776.86, 4180, 173100])
    return np.sort(masses)

class IFSMeasure:
    def __init__(self, contraction_factors, probabilities, n_points=50000):
        self.contraction_factors = np.array(contraction_factors)
        self.probabilities = np.array(probabilities) / np.sum(probabilities)
        self.n_points = n_points
        self.points = self._generate()
    
    def _generate(self):
        points = np.zeros(self.n_points)
        x = 0.5
        n_contract = len(self.contraction_factors)
        
        offsets = np.cumsum(self.contraction_factors) - self.contraction_factors
        offsets = offsets / np.sum(self.contraction_factors)
        
        for i in range(self.n_points):
            idx = np.random.choice(n_contract, p=self.probabilities)
            x = self.contraction_factors[idx] * x + offsets[idx]
            points[i] = x
        return points

class MultiScaleKernel:
    def __init__(self, sigmas, weights=None):
        self.sigmas = np.array(sigmas)
        if weights is None:
            self.weights = np.ones_like(sigmas) / len(sigmas)
        else:
            self.weights = np.array(weights) / np.sum(weights)
    
    def kernel_value(self, x, y):
        total = 0.0
        for sigma, w in zip(self.sigmas, self.weights):
            total += w * np.exp(-(x - y)**2 / (2 * sigma**2))
        return total

def compute_TK_eigenvalues(sample_points, kernel, weights):
    n = len(sample_points)
    K = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            K[i, j] = kernel.kernel_value(sample_points[i], sample_points[j])
    
    T = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            T[i, j] = K[i, j] * weights[j]
    
    eigenvalues = la.eigvals(T)
    eigenvalues = np.real(eigenvalues)
    eigenvalues = np.sort(eigenvalues)[::-1]
    return eigenvalues[:20]

def mass_spectrum_fit(eigenvalues, n_particles=9):
    """用T_K特征值拟合质量谱"""
    log_eig = -np.log(np.maximum(eigenvalues[:n_particles], 1e-15))
    
    sm_masses = standard_model_fermion_masses()[:n_particles]
    log_sm = np.log(sm_masses)
    
    C = np.exp(np.mean(log_sm - np.log(log_eig)))
    
    predicted = C * log_eig
    
    error = np.mean(np.abs(np.log(predicted) - np.log(sm_masses)))
    
    return predicted, C, error

def grid_search():
    print("=" * 70)
    print("Kernel Parameter Optimization for Standard Model Mass Matching")
    print("=" * 70)
    
    sm_masses = standard_model_fermion_masses()
    print(f"\nTarget: {len(sm_masses)} Standard Model fermion masses")
    print(f"Range: {sm_masses[0]:.3f} MeV to {sm_masses[-1]:.0f} MeV")
    print(f"Log range: {np.log10(sm_masses[0]):.2f} to {np.log10(sm_masses[-1]):.2f}")
    
    best_error = float('inf')
    best_params = None
    best_eigenvalues = None
    best_predicted = None
    
    # 网格搜索参数空间
    ifs_configs = [
        ([0.3, 0.3, 0.4], [1/3, 1/3, 1/3]),
        ([0.25, 0.25, 0.25, 0.25], [0.25, 0.25, 0.25, 0.25]),
        ([0.4, 0.3, 0.3], [0.4, 0.3, 0.3]),
        ([0.2, 0.3, 0.5], [1/3, 1/3, 1/3]),
        ([0.5, 0.5], [0.5, 0.5]),
        ([0.4, 0.4, 0.2], [0.4, 0.4, 0.2]),
    ]
    
    n_samples_options = [100, 200]
    sigma_grid = [
        [0.02, 0.05, 0.1],
        [0.03, 0.08, 0.15],
        [0.01, 0.04, 0.12, 0.2],
        [0.02, 0.06, 0.18],
    ]
    
    results = []
    
    for ifs_idx, (factors, probs) in enumerate(ifs_configs):
        print(f"\n--- IFS config {ifs_idx+1}: factors={factors}, probs={np.round(probs, 2)} ---")
        
        for n_samples in n_samples_options:
            measure = IFSMeasure(factors, probs, n_points=50000)
            sample_points = np.linspace(0, 1, n_samples)
            weights = np.ones(n_samples) / n_samples
            
            for sigmas in sigma_grid:
                kernel = MultiScaleKernel(sigmas)
                
                eigenvalues = compute_TK_eigenvalues(sample_points, kernel, weights)
                
                if len(eigenvalues) < 9:
                    continue
                
                predicted, C, error = mass_spectrum_fit(eigenvalues, n_particles=9)
                
                results.append((error, ifs_idx, factors, probs, n_samples, sigmas, C, eigenvalues, predicted))
                
                if error < best_error:
                    best_error = error
                    best_params = (ifs_idx, factors, probs, n_samples, sigmas, C)
                    best_eigenvalues = eigenvalues.copy()
                    best_predicted = predicted.copy()
                    print(f"  New best! error={error:.4f}, C={C:.2f}, sigmas={sigmas}")
    
    results.sort(key=lambda x: x[0])
    
    print("\n" + "=" * 70)
    print("Top 5 Parameter Combinations")
    print("=" * 70)
    for i in range(min(5, len(results))):
        r = results[i]
        print(f"\n{i+1}. Error={r[0]:.4f}")
        print(f"   IFS: factors={r[2]}, probs={np.round(r[3], 2)}")
        print(f"   Samples: {r[4]}, Sigmas: {r[5]}")
        print(f"   C={r[6]:.2f}")
        print(f"   Top 5 eigenvalues: {np.round(r[7][:5], 6)}")
    
    # 绘制最佳结果
    print("\n" + "=" * 70)
    print("Best Result Details")
    print("=" * 70)
    print(f"IFS config #{best_params[0]+1}: factors={best_params[1]}, probs={np.round(best_params[2], 2)}")
    print(f"n_samples={best_params[3]}, sigmas={best_params[4]}, C={best_params[5]:.2f}")
    print(f"Mean log error: {best_error:.4f}")
    
    print(f"\n{'Particle':>10s} | {'SM Mass(MeV)':>14s} | {'Predicted(MeV)':>14s} | {'Lambda':>10s} | {'Ratio':>8s}")
    print("-" * 60)
    for i in range(9):
        ratio = best_predicted[i] / sm_masses[i] if sm_masses[i] > 0 else 0
        print(f"{i+1:>10d} | {sm_masses[i]:>14.2f} | {best_predicted[i]:>14.2f} | {best_eigenvalues[i]:>10.6f} | {ratio:>8.2f}")
    
    # 绘图
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    ax = axes[0]
    ax.bar(range(1, 10), best_eigenvalues[:9])
    ax.set_xlabel('Index')
    ax.set_ylabel('Eigenvalue')
    ax.set_title('T_K Eigenvalues (Best Fit)')
    ax.grid(True)
    
    ax = axes[1]
    indices = np.arange(1, 10)
    ax.plot(indices, np.log10(sm_masses[:9]), 'o-', label='SM masses', linewidth=2)
    ax.plot(indices, np.log10(best_predicted[:9]), 's--', label='Predicted', linewidth=2)
    ax.set_xlabel('Particle index')
    ax.set_ylabel('log10(mass) [MeV]')
    ax.set_title('Mass Spectrum: SM vs Predicted')
    ax.legend()
    ax.grid(True)
    
    ax = axes[2]
    ax.scatter(np.log10(sm_masses[:9]), np.log10(best_predicted[:9]), s=100)
    min_val = min(np.min(np.log10(sm_masses[:9])), np.min(np.log10(best_predicted[:9])))
    max_val = max(np.max(np.log10(sm_masses[:9])), np.max(np.log10(best_predicted[:9])))
    ax.plot([min_val, max_val], [min_val, max_val], 'r--', label='Perfect fit')
    ax.set_xlabel('log10(SM mass) [MeV]')
    ax.set_ylabel('log10(Predicted mass) [MeV]')
    ax.set_title('Correlation Plot')
    ax.legend()
    ax.grid(True)
    
    plt.tight_layout()
    plt.savefig('kernel_optimization_best_fit.png', dpi=300)
    
    with open('kernel_optimization_results.txt', 'w') as f:
        f.write("=== Kernel Parameter Optimization Results ===\n\n")
        f.write(f"Best Mean Log Error: {best_error:.4f}\n")
        f.write(f"Best Parameters:\n")
        f.write(f"  IFS factors: {best_params[1]}\n")
        f.write(f"  IFS probabilities: {np.round(best_params[2], 2)}\n")
        f.write(f"  n_samples: {best_params[3]}\n")
        f.write(f"  sigmas: {best_params[4]}\n")
        f.write(f"  scaling C: {best_params[5]:.2f}\n\n")
        f.write(f"Mass Predictions:\n")
        f.write(f"{'Index':>8s} | {'SM Mass':>12s} | {'Predicted':>12s} | {'Lambda':>12s}\n")
        f.write("-" * 48 + "\n")
        for i in range(9):
            f.write(f"{i+1:>8d} | {sm_masses[i]:>12.2f} | {best_predicted[i]:>12.2f} | {best_eigenvalues[i]:>12.6f}\n")
        f.write("\nTop 5 Combinations:\n")
        for i in range(min(5, len(results))):
            r = results[i]
            f.write(f"\n{i+1}. Error={r[0]:.4f}, factors={r[2]}, sigmas={r[5]}, C={r[6]:.2f}\n")
    
    print(f"\nResults saved to kernel_optimization_results.txt")
    print(f"Plot saved to kernel_optimization_best_fit.png")

if __name__ == "__main__":
    grid_search()