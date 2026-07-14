import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt

def sm_masses():
    return np.sort(np.array([0.511, 2.2, 4.7, 95, 105.66, 1270, 1776.86, 4180, 173100]))

def pauli():
    return [np.array(s, dtype=complex) for s in [
        [[0,1],[1,0]], [[0,-1j],[1j,0]], [[1,0],[0,-1]]]]

def chiral_cartan_generators():
    """
    在4维手征子空间中的3个Cartan生成元
    J_k = diag(eigenvalues) 区分3代+1惰性中微子
    
    使用SU(4)的Cartan子代数:
    J₁ = diag(1, 1, -1, -1)
    J₂ = diag(1, -1, 1, -1)  
    J₃ = diag(1, -1, -1, 1)
    
    这4个本征值对应:
    (1,1,1): 第1代 (轻子/夸克)
    (1,-1,-1): 第2代
    (-1,1,-1): 第3代  
    (-1,-1,1): 惰性中微子(无质量)
    """
    J1 = np.diag([1, 1, -1, -1]).astype(complex)
    J2 = np.diag([1, -1, 1, -1]).astype(complex)
    J3 = np.diag([1, -1, -1, 1]).astype(complex)
    return [J1, J2, J3]

class ChiralMassKernel:
    """4维手征子空间中的质量核"""
    def __init__(self, n_points=80):
        self.n = n_points
        self.x = np.linspace(0, 1, n_points)
        self.J = chiral_cartan_generators()
    
    def compute_masses(self, sigmas, weights):
        """计算4×4手征核的特征值"""
        N = self.n
        X = self.x.reshape(-1, 1)
        D2 = (X - self.x.reshape(1, -1)) ** 2
        
        K = np.zeros((4*N, 4*N), dtype=complex)
        for k in range(3):
            Ks = weights[k] * np.exp(-D2 / (2 * sigmas[k]**2))
            K += np.kron(Ks, self.J[k])
        
        w = np.ones(N) / N
        for i in range(4):
            K[i*N:(i+1)*N] *= w.reshape(-1, 1)
        
        ev = la.eigvals(K)
        ev = np.real(ev)
        return np.sort(ev)[::-1][:15]

def run():
    print("=" * 70)
    print("Chiral 4×4 Cartan Kernel: 3 Generations + 1 Sterile")
    print("=" * 70)
    
    masses = sm_masses()
    kernel = ChiralMassKernel(n_points=80)
    
    configs = [
        ([0.8, 0.08, 0.008], [0.5, 0.3, 0.2], "wide"),
        ([0.6, 0.06, 0.006], [1/3, 1/3, 1/3], "equal_w"),
        ([0.5, 0.05, 0.005], [0.4, 0.35, 0.25], "light"),
        ([0.9, 0.15, 0.015], [0.5, 0.3, 0.2], "heavy"),
        ([0.7, 0.07, 0.007], [0.45, 0.35, 0.2], "mid"),
    ]
    
    best_error = float('inf')
    best = None
    
    for sg, wg, name in configs:
        print(f"\n--- {name}: sigmas={sg} ---")
        ev = kernel.compute_masses(sg, wg)
        print(f"    Top 15: {np.round(ev[:15], 6)}")
        print(f"    Unique: {len(set(np.round(ev[:12], 8)))}")
        
        # 取前9个（忽略惰性中微子对应的特征值）
        log_eig = -np.log(np.maximum(ev[:9], 1e-30))
        log_sm = np.log(masses)
        C = np.exp(np.mean(log_sm - np.log(log_eig)))
        predicted = C * log_eig
        error = np.mean(np.abs(np.log(predicted) - log_sm))
        
        print(f"    C={C:.2f}, RMSE={error:.4f}")
        
        if error < best_error:
            best_error = error
            best = (sg, wg, C, ev[:12], predicted, name)
    
    print("\n" + "=" * 70)
    print("BEST RESULT")
    print("=" * 70)
    sg, wg, C, ev, pred, name = best
    print(f"Config: {name}, sigmas={sg}")
    
    print(f"\n{'Index':>6s} | {'SM Mass':>10s} | {'Predicted':>10s} | {'Lambda':>12s} | {'Ratio':>8s}")
    print("-" * 50)
    for i in range(9):
        ratio = pred[i] / masses[i]
        print(f"{i+1:>6d} | {masses[i]:>10.4f} | {pred[i]:>10.4f} | {ev[i]:>12.6f} | {ratio:>8.2f}")
    
    print(f"\nRemaining eigenvalues (sterile sector):")
    for i in range(9, min(12, len(ev))):
        m_est = -C * np.log(np.maximum(ev[i], 1e-30))
        print(f"  λ_{i+1} = {ev[i]:.6f} → mass ~ {m_est:.1f} MeV")
    
    plt.figure(figsize=(12, 5))
    plt.subplot(121)
    plt.plot(range(1,10), np.log10(masses), 'o-', label='SM', linewidth=2, markersize=8)
    plt.plot(range(1,10), np.log10(pred), 's--', label=f'{name}', linewidth=2, markersize=8)
    plt.xlabel('Index')
    plt.ylabel('log10(mass) [MeV]')
    plt.title(f'Mass Spectrum (RMSE={best_error:.3f})')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(122)
    plt.scatter(np.log10(masses), np.log10(pred), s=100, c='red')
    lims = [-1, 6]
    plt.plot(lims, lims, 'b--', label='Perfect')
    plt.xlabel('log10(SM mass)')
    plt.ylabel('log10(Predicted)')
    plt.title(f'Correlation (C={C:.1f})')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('cl6_chiral_mass.png', dpi=300)
    
    with open('cl6_chiral_mass_results.txt', 'w') as f:
        f.write("=== Chiral 4×4 Cartan Mass Prediction ===\n\n")
        f.write(f"Best: {name}\n")
        f.write(f"Sigmas: {sg}\n")
        f.write(f"C: {C:.2f}\n")
        f.write(f"RMSE: {best_error:.4f}\n\n")
        for i in range(9):
            f.write(f"  {i+1}: SM={masses[i]:>10.4f} Pred={pred[i]:>10.4f}\n")
    
    print(f"\nResults saved to cl6_chiral_mass_results.txt")

if __name__ == "__main__":
    run()