import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt

def sm_masses():
    return np.sort(np.array([0.511, 2.2, 4.7, 95, 105.66, 1270, 1776.86, 4180, 173100]))

def pauli():
    return [np.array(s, dtype=complex) for s in [
        [[0,1],[1,0]], [[0,-1j],[1j,0]], [[1,0],[0,-1]]]]

def cl6_gamma_8x8():
    """Cl(6)的6个Gamma矩阵 (8x8) Weyl基"""
    s = pauli()
    I2 = np.eye(2, dtype=complex)
    g = []
    for k in range(3):
        g.append(np.kron(np.kron(s[k], s[0]), I2))
    for k in range(3):
        g.append(np.kron(np.kron(I2, s[1]), s[k]))
    return g

def g7(gamma):
    g7 = np.eye(8, dtype=complex)
    for k in range(6):
        g7 = g7 @ gamma[k] * (-1j)
    return g7

class Cl6FullKernel:
    """全8×8 Cl(6)-值核，6个非交换Gamma矩阵"""
    def __init__(self, n_points=35):
        self.n = n_points
        self.x = np.linspace(0, 1, n_points)
        self.gamma = cl6_gamma_8x8()
        # 添加3个Cartan生成元(iγ_iγ_j)和1个单位元，共10通道
        self.ops = []
        # 6个Gamma矩阵（非交换）
        for k in range(6):
            self.ops.append(self.gamma[k])
        # 3个Cartan生成元（对角的）
        for k in range(3):
            J = 1j * self.gamma[2*k] @ self.gamma[2*k+1]
            self.ops.append(J)
    
    def compute_spectrum(self, sigmas_6, weight_6, sigmas_3, weight_3):
        """6+3=9通道核的特征值"""
        N = self.n
        X = self.x.reshape(-1, 1)
        D2 = (X - self.x.reshape(1, -1)) ** 2
        
        K_full = np.zeros((8*N, 8*N), dtype=complex)
        
        # 6个非交换Gamma通道
        for k in range(6):
            Ks = weight_6[k] * np.exp(-D2 / (2 * sigmas_6[k]**2))
            K_full += np.kron(Ks, self.ops[k])
        
        # 3个Cartan通道（对角化）
        for k in range(3):
            Ks = weight_3[k] * np.exp(-D2 / (2 * sigmas_3[k]**2))
            K_full += np.kron(Ks, self.ops[6+k])
        
        w_vec = np.ones(N) / N
        T = K_full.copy()
        for i in range(8):
            T[i*N:(i+1)*N, :] *= w_vec.reshape(-1, 1)
        
        eigvals = la.eigvals(T)
        eigvals = np.real(eigvals)
        return np.sort(eigvals)[::-1][:20]

def run():
    print("=" * 70)
    print("Cl(6) Full 8×8 Kernel: 9-Channel Non-commuting Generators")
    print("=" * 70)
    
    masses = sm_masses()
    kernel = Cl6FullKernel(n_points=60)
    
    # 6 gamma sigmas + 3 Cartan sigmas
    configs = [
        # (gamma_sigmas, gamma_weights, cartan_sigmas, cartan_weights, name)
        ([0.5]*6, [1/6]*6, [0.5]*3, [1/3]*3, "uniform_all"),
        ([0.8,0.3,0.1,0.05,0.02,0.008], [0.25,0.2,0.2,0.15,0.1,0.1],
         [0.8,0.1,0.01], [0.5,0.3,0.2], "hierarchical"),
        ([0.9,0.5,0.2,0.08,0.03,0.01], [0.25,0.2,0.15,0.15,0.15,0.1],
         [0.6,0.06,0.006], [0.6,0.25,0.15], "wide_spectrum"),
        ([0.95,0.4,0.15,0.06,0.025,0.008], [0.3,0.2,0.15,0.15,0.1,0.1],
         [0.5,0.05,0.005], [0.5,0.3,0.2], "best_guess"),
    ]
    
    best_error = float('inf')
    best = None
    
    for idx, (sg, wg, sc, wc, name) in enumerate(configs):
        print(f"\n--- {name} ---")
        ev = kernel.compute_spectrum(sg, wg, sc, wc)
        print(f"    Top 12: {np.round(ev[:12], 6)}")
        print(f"    Unique top 9: {len(set(np.round(ev[:9], 8)))}")
        
        log_eig = -np.log(np.maximum(ev[:9], 1e-30))
        log_sm = np.log(masses)
        C = np.exp(np.mean(log_sm - np.log(log_eig)))
        predicted = C * log_eig
        error = np.mean(np.abs(np.log(predicted) - log_sm))
        
        print(f"    C={C:.2f}, RMSE={error:.4f}")
        
        if error < best_error:
            best_error = error
            best = (sg, wg, sc, wc, C, ev[:9], predicted, name)
    
    print("\n" + "=" * 70)
    print("BEST RESULT")
    print("=" * 70)
    sg, wg, sc, wc, C, ev, pred, name = best
    print(f"Config: {name}")
    print(f"C = {C:.2f}, RMSE = {best_error:.4f}")
    print(f"\nUnique eigenvalues: {len(set(np.round(ev, 8)))} out of 9")
    
    print(f"\n{'Index':>6s} | {'SM Mass':>10s} | {'Predicted':>10s} | {'Lambda':>12s} | {'Ratio':>8s}")
    print("-" * 50)
    for i in range(9):
        ratio = pred[i] / masses[i]
        print(f"{i+1:>6d} | {masses[i]:>10.4f} | {pred[i]:>10.4f} | {ev[i]:>12.6f} | {ratio:>8.2f}")
    
    plt.figure(figsize=(12, 5))
    plt.subplot(121)
    plt.plot(range(1,10), np.log10(masses), 'o-', label='SM', linewidth=2, markersize=8)
    plt.plot(range(1,10), np.log10(pred[:9]), 's--', label=name, linewidth=2, markersize=8)
    plt.xlabel('Index')
    plt.ylabel('log10(mass) [MeV]')
    plt.title(f'Mass Spectrum (RMSE={best_error:.3f})')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(122)
    plt.scatter(np.log10(masses), np.log10(pred[:9]), s=100, c='red')
    lims = [-1, 6]
    plt.plot(lims, lims, 'b--', label='Perfect')
    plt.xlabel('log10(SM mass)')
    plt.ylabel('log10(Predicted)')
    plt.title(f'Correlation')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('cl6_full8d_mass.png', dpi=300)
    
    with open('cl6_full8d_results.txt', 'w') as f:
        f.write("=== Cl(6) Full 8×8 Kernel Results ===\n\n")
        f.write(f"Best: {name}\n")
        f.write(f"RMSE: {best_error:.4f}\n")
        f.write(f"C: {C:.2f}\n\n")
        for i in range(9):
            f.write(f"  {i+1}: SM={masses[i]:>10.4f} Pred={pred[i]:>10.4f} λ={ev[i]:.6f}\n")
    
    print(f"\nResults saved to cl6_full8d_results.txt")

if __name__ == "__main__":
    run()