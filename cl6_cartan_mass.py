import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt

def sm_masses():
    return np.sort(np.array([0.511, 2.2, 4.7, 95, 105.66, 1270, 1776.86, 4180, 173100]))

class Cl6CartanKernel:
    """
    Cl(6) Cartan生成元核: K(x,y) = Σ_k K_k(x,y) J_k
    J_k = iγ_{2k-1}γ_{2k} are the 3 Cartan generators of SU(4)
    In the chiral basis, J_k are 4×4 diagonal matrices with eigenvalues ±1
    """
    def __init__(self, n_points=50):
        self.n = n_points
        self.x = np.linspace(0, 1, n_points)
        self.J = self._cartan_generators()
    
    def _cartan_generators(self):
        """3个Cartan生成元 J_k = iγ_{2k-1}γ_{2k} 在Weyl基下的4×4块"""
        s1 = np.array([[0,1],[1,0]], dtype=complex)
        s2 = np.array([[0,-1j],[1j,0]], dtype=complex)
        s3 = np.array([[1,0],[0,-1]], dtype=complex)
        
        I2 = np.eye(2, dtype=complex)
        
        # γ₁ = s₁ ⊗ s₁ ⊗ I₂, γ₂ = s₂ ⊗ s₁ ⊗ I₂
        # J₁ = iγ₁γ₂ = i(s₁s₂) ⊗ I₂ ⊗ I₂ = -s₃ ⊗ I₂ ⊗ I₂
        J1_PL = -np.kron(np.kron(s3, I2), I2)[:4,:4]
        
        # J₂ = iγ₃γ₄, γ₃ = s₃ ⊗ s₁ ⊗ I₂, γ₄ = I₂ ⊗ s₂ ⊗ s₁
        # In PL sector (first 4×4 block)
        g3 = np.kron(np.kron(s3, s1), I2)
        g4 = np.kron(np.kron(I2, s2), s1)
        J2_full = 1j * g3 @ g4
        J2_PL = J2_full[:4,:4]
        
        # J₃ = iγ₅γ₆, γ₅ = I₂ ⊗ s₂ ⊗ s₂, γ₆ = I₂ ⊗ s₂ ⊗ s₃
        g5 = np.kron(np.kron(I2, s2), s2)
        g6 = np.kron(np.kron(I2, s2), s3)
        J3_full = 1j * g5 @ g6
        J3_PL = J3_full[:4,:4]
        
        return [J1_PL, J2_PL, J3_PL]
    
    def masses_from_sigmas(self, sigmas, weights):
        """由3个σ计算T_K特征值并提取9个质量"""
        N = self.n
        X = self.x.reshape(-1, 1)
        D2 = (X - self.x.reshape(1, -1)) ** 2
        
        # 全4N×4N核矩阵
        K_full = np.zeros((4*N, 4*N), dtype=complex)
        for k in range(3):
            K_scalar = weights[k] * np.exp(-D2 / (2 * sigmas[k]**2))
            K_full += np.kron(K_scalar, self.J[k])
        
        T_full = np.zeros_like(K_full)
        w_vec = np.ones(N) / N
        for i in range(4):
            T_full[i*N:(i+1)*N, i*N:(i+1)*N] = K_full[i*N:(i+1)*N, i*N:(i+1)*N] * w_vec.reshape(-1,1)
        
        eigvals = la.eigvals(T_full)
        eigvals = np.real(eigvals)
        return np.sort(np.abs(eigvals))[::-1][:20]

def run_analysis():
    print("=" * 70)
    print("Cl(6) Cartan Generator Kernel: 3-Generation Mass Splitting")
    print("=" * 70)
    
    masses = sm_masses()
    
    kernel = Cl6CartanKernel(n_points=50)
    
    configs = [
        ([0.8, 0.2, 0.05], [1/3, 1/3, 1/3], "equal"),
        ([0.8, 0.15, 0.02], [0.5, 0.3, 0.2], "heavy_dominated"),
        ([0.6, 0.1, 0.01], [1/3, 1/3, 1/3], "mid_range"),
        ([0.5, 0.08, 0.008], [0.4, 0.35, 0.25], "light_tuned"),
        # 多尺度宽范围：一个σ覆盖一代
        ([0.9, 0.3, 0.03], [0.4, 0.35, 0.25], "multi_scale"),
        ([0.95, 0.25, 0.015], [0.5, 0.3, 0.2], "best_guess"),
    ]
    
    best_error = float('inf')
    best = None
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    for idx, (sigmas, weights, name) in enumerate(configs):
        print(f"\n--- {name}: sigmas={sigmas}, weights={[round(w,3) for w in weights]} ---")
        
        eigvals = kernel.masses_from_sigmas(sigmas, weights)
        
        print(f"    Top 12 eigenvalues: {np.round(eigvals[:12], 6)}")
        
        # 取前9个正特征值
        n_phys = min(9, len(eigvals[eigvals > 1e-15]))
        top9 = eigvals[:n_phys]
        
        log_eig = -np.log(np.maximum(top9[:9], 1e-30))
        log_sm = np.log(masses)
        C = np.exp(np.mean(log_sm - np.log(log_eig)))
        predicted = C * log_eig
        error = np.mean(np.abs(np.log(predicted) - log_sm))
        
        print(f"    C={C:.2f}, RMSE={error:.4f}")
        
        if error < best_error:
            best_error = error
            best = (sigmas, weights, C, eigvals[:9], predicted, name)
        
        row, col = idx // 3, idx % 3
        ax = axes[row, col]
        ax.plot(range(1,10), np.log10(masses), 'o-', label='SM', linewidth=2, color='blue')
        ax.plot(range(1,10), np.log10(predicted[:9]), 's--', label=name, linewidth=2, color='red')
        ax.set_xlabel('Particle index')
        ax.set_ylabel('log10(mass) [MeV]')
        ax.set_title(f'{name} (RMSE={error:.3f})')
        ax.legend()
        ax.grid(True)
    
    # Best result
    print("\n" + "=" * 70)
    print("BEST RESULT")
    print("=" * 70)
    s, w, C, ev, pred, name = best
    print(f"Config: {name}")
    print(f"Sigmas: {s}")
    print(f"Weights: {[round(x,3) for x in w]}")
    print(f"C = {C:.2f}")
    print(f"RMSE = {best_error:.4f}")
    
    print(f"\n{'Index':>6s} | {'SM Mass':>10s} | {'Predicted':>10s} | {'Lambda':>12s} | {'Ratio':>8s}")
    print("-" * 50)
    for i in range(9):
        ratio = pred[i] / masses[i]
        print(f"{i+1:>6d} | {masses[i]:>10.4f} | {pred[i]:>10.4f} | {ev[i]:>12.6f} | {ratio:>8.2f}")
    
    # 关联图
    ax = axes[1, 2]
    ax.scatter(np.log10(masses), np.log10(pred[:9]), s=80, c='red')
    lims = [-1, 6]
    ax.plot(lims, lims, 'b--', label='Perfect')
    ax.set_xlabel('log10(SM mass)')
    ax.set_ylabel('log10(Predicted)')
    ax.set_title(f'Correlation (RMSE={best_error:.3f})')
    ax.legend()
    ax.grid(True)
    
    plt.tight_layout()
    plt.savefig('cl6_cartan_mass.png', dpi=300)
    
    with open('cl6_cartan_results.txt', 'w') as f:
        f.write("=== Cl(6) Cartan Generator Mass Prediction ===\n\n")
        f.write(f"Best: {name}\n")
        f.write(f"Sigmas: {s}\n")
        f.write(f"Weights: {[round(x,3) for x in w]}\n")
        f.write(f"C = {C:.2f}\n")
        f.write(f"RMSE = {best_error:.4f}\n\n")
        for i in range(9):
            f.write(f"  {i+1}: SM={masses[i]:>10.4f} Pred={pred[i]:>10.4f} λ={ev[i]:.6f}\n")
    
    print(f"\nResults saved to cl6_cartan_results.txt")
    print(f"Plot saved to cl6_cartan_mass.png")

if __name__ == "__main__":
    run_analysis()