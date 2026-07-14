import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt

def standard_model_masses():
    """9个SM费米子质量 (MeV)"""
    return np.sort(np.array([0.511, 2.2, 4.7, 95, 105.66, 1270, 1776.86, 4180, 173100]))

def pauli_matrices():
    s1 = np.array([[0,1],[1,0]], dtype=complex)
    s2 = np.array([[0,-1j],[1j,0]], dtype=complex)
    s3 = np.array([[1,0],[0,-1]], dtype=complex)
    return [s1, s2, s3]

def cl6_gamma_matrices():
    """Cl(6)的6个Gamma矩阵 (8x8)"""
    s = pauli_matrices()
    g = []
    # γ₁,γ₂,γ₃ = σ_k ⊗ σ₁ ⊗ I₂ (k=1,2,3)
    for k in range(3):
        g.append(np.kron(np.kron(s[k], s[0]), np.eye(2, dtype=complex)))
    # γ₄,γ₅,γ₆ = I₂ ⊗ σ₂ ⊗ σ_k (k=1,2,3)
    for k in range(3):
        g.append(np.kron(np.kron(np.eye(2, dtype=complex), s[1]), s[k]))
    return g

def chirality_7(gamma):
    """γ₇ = (-i)³ γ₁γ₂γ₃γ₄γ₅γ₆"""
    g7 = np.eye(8, dtype=complex)
    for k in range(6):
        g7 = g7 @ gamma[k] * (-1j)
    return g7

class Cl6ValuedKernel:
    """Cl(6)-值多尺度核 K(x,y) = Σ_k K_k(x,y) γ_k"""
    def __init__(self, n_points=40):
        self.n = n_points
        self.x = np.linspace(0, 1, n_points)
        self.gamma = cl6_gamma_matrices()
        self.g7 = chirality_7(self.gamma)
        self.P_L = (np.eye(8) - self.g7) / 2
        self.P_R = (np.eye(8) + self.g7) / 2
    
    def build_full_kernel(self, sigmas, weights):
        """构造完整8N×8N核矩阵"""
        N = self.n
        K_full = np.zeros((8*N, 8*N), dtype=complex)
        
        X = self.x.reshape(-1, 1)
        D2 = (X - self.x.reshape(1, -1)) ** 2
        
        for k in range(6):
            K_scalar = weights[k] * np.exp(-D2 / (2 * sigmas[k]**2))
            K_full += np.kron(K_scalar, self.gamma[k])
        
        return K_full
    
    def compute_masses(self, sigmas, weights, C=1.0):
        """计算Cl(6)-值T_K的特征质量和谱"""
        N = self.n
        K_full = self.build_full_kernel(sigmas, weights)
        
        w = np.ones(N) / N
        W = np.diag(np.tile(w, 8))
        T = K_full @ W
        
        eigvals = la.eigvals(T)
        eigvals = np.real(eigvals)
        eigvals = np.sort(eigvals)[::-1]
        
        return eigvals[:30]

def run_analysis():
    print("=" * 70)
    print("Cl(6)-valued Kernel: 3-Generation Mass Prediction")
    print("=" * 70)
    
    sm_masses = standard_model_masses()
    print(f"\nTarget masses span {np.log10(sm_masses[-1]) - np.log10(sm_masses[0]):.2f} orders")
    
    kernel = Cl6ValuedKernel(n_points=30)
    
    # Test different sigma configurations
    configs = [
        # (sigmas, weights, name) for 6 gamma channels
        ([0.5,0.5,0.5,0.5,0.5,0.5], [1/6]*6, "uniform"),
        ([0.5,0.1,0.05,0.02,0.01,0.005], [0.3,0.25,0.2,0.15,0.07,0.03], "hierarchical"),
        ([0.8,0.3,0.1,0.05,0.02,0.008], [0.25,0.25,0.2,0.15,0.1,0.05], "wide_range"),
        ([0.6,0.2,0.08,0.03,0.01,0.004], [1/6]*6, "equal_weight"),
        # Try to match the mass scales: heavy (γ1→t,b), medium (γ2→c,τ,s), light (γ3→μ,d,u,e)
        ([0.8,0.15,0.02,0.8,0.15,0.02], [0.25,0.25,0.25,0.08,0.08,0.09], "generational"),
    ]
    
    plt.figure(figsize=(14, 10))
    
    all_results = []
    best_error = float('inf')
    best_result = None
    
    for idx, (sigmas, weights, name) in enumerate(configs):
        print(f"\n--- Config {idx+1}: {name} ---")
        print(f"    sigmas: {[round(s,4) for s in sigmas]}")
        
        eigvals = kernel.compute_masses(sigmas, weights)
        
        pos_eig = eigvals[eigvals > 1e-15]
        print(f"    positive eigenvalues: {len(pos_eig)}")
        print(f"    top 12: {np.round(pos_eig[:12], 6)}")
        
        log_eig = -np.log(pos_eig[:9])
        log_sm = np.log(sm_masses)
        
        C = np.exp(np.mean(log_sm - np.log(log_eig)))
        predicted = C * log_eig
        error = np.mean(np.abs(np.log(predicted) - log_sm))
        
        print(f"    C={C:.2f}, RMSE={error:.4f}")
        
        all_results.append((error, name, sigmas, weights, C, pos_eig[:12], predicted))
        
        if error < best_error:
            best_error = error
            best_result = (error, name, sigmas, weights, C, pos_eig[:12], predicted)
        
        plt.subplot(2, 3, idx+1)
        plt.plot(range(1,10), np.log10(sm_masses), 'o-', label='SM', linewidth=2)
        plt.plot(range(1,10), np.log10(predicted[:9]), 's--', label=name, linewidth=2)
        plt.xlabel('Index')
        plt.ylabel('log10(mass) [MeV]')
        plt.title(f'{name} (RMSE={error:.3f})')
        plt.legend()
        plt.grid(True)
    
    # Best result
    print("\n" + "=" * 70)
    print(f"Best config: {best_result[1]} (RMSE={best_result[0]:.4f})")
    print(f"C={best_result[2]:.2f}" if len(best_result)>4 else "")
    print("=" * 70)
    
    r = best_result
    print(f"\n{'Index':>6s} | {'SM Mass':>10s} | {'Predicted':>10s} | {'Lambda':>12s} | {'Ratio':>8s}")
    print("-" * 50)
    for i in range(9):
        ratio = r[6][i] / sm_masses[i]
        print(f"{i+1:>6d} | {sm_masses[i]:>10.4f} | {r[6][i]:>10.4f} | {r[5][i]:>12.6f} | {ratio:>8.2f}")
    
    # Correlation plot
    plt.subplot(236)
    plt.scatter(np.log10(sm_masses), np.log10(r[6][:9]), s=80, c='red')
    lims = [-1, 6]
    plt.plot(lims, lims, 'b--', label='Perfect')
    plt.xlabel('log10(SM mass)')
    plt.ylabel('log10(Predicted)')
    plt.title(f'Correlation (RMSE={r[0]:.3f})')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('cl6_mass_prediction.png', dpi=300)
    
    with open('cl6_mass_prediction_results.txt', 'w') as f:
        f.write("=== Cl(6)-valued Multi-Scale Kernel Results ===\n\n")
        f.write(f"Best config: {best_result[1]}\n")
        f.write(f"RMSE: {best_result[0]:.4f}\n")
        f.write(f"C: {best_result[2]:.2f}\n\n")
        f.write(f"{'Index':>6s} | {'SM Mass':>10s} | {'Predicted':>10s}\n")
        f.write("-" * 30 + "\n")
        for i in range(9):
            f.write(f"{i+1:>6d} | {sm_masses[i]:>10.4f} | {r[6][i]:>10.4f}\n")
        f.write(f"\nBest eigenvalues:\n")
        for i, ev in enumerate(r[5][:12]):
            f.write(f"  λ_{i+1} = {ev:.8f}\n")
    
    print(f"\nResults saved to cl6_mass_prediction_results.txt")
    print(f"Plot saved to cl6_mass_prediction.png")

if __name__ == "__main__":
    run_analysis()