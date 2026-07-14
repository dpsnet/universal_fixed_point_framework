import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt

def sm_masses_sectors():
    """按扇区分组: [leptons, up-quarks, down-quarks]"""
    return [np.array([0.511, 105.66, 1776.86]),    # e, μ, τ
            np.array([2.2, 1270.0, 173100.0]),      # u, c, t
            np.array([4.7, 95.0, 4180.0])]          # d, s, b

def pauli():
    return [np.array(s, dtype=complex) for s in [
        [[0,1],[1,0]], [[0,-1j],[1j,0]], [[1,0],[0,-1]]]]

def cl6_gamma():
    s = pauli()
    I2 = np.eye(2, dtype=complex)
    g = []
    for k in range(3):
        g.append(np.kron(np.kron(s[k], s[0]), I2))
    for k in range(3):
        g.append(np.kron(np.kron(I2, s[1]), s[k]))
    return g

def chirality(g):
    g7 = np.eye(8, dtype=complex)
    for k in range(6):
        g7 = g7 @ g[k] * (-1j)
    return g7

class ThreeSectorKernel:
    """
    三扇区独立Cl(6)核: K_sector = Σ_k K_k Γ_k P_sector
    每个扇区使用不同的投影P_sector，得到独立特征值问题
    """
    def __init__(self, n_points=60):
        self.n = n_points
        self.x = np.linspace(0, 1, n_points)
        self.gamma = cl6_gamma()
        g7 = chirality(self.gamma)
        
        # 左/右手征投影
        P_L = (np.eye(8) - g7) / 2
        P_R = (np.eye(8) + g7) / 2
        
        # 扇区投影
        self.sector_ops = [
            P_L @ self.gamma[0] @ P_L,
            P_L @ self.gamma[1] @ P_L,
            P_L @ self.gamma[2] @ P_L,
        ]
    
    def sector_spectrum(self, sigmas, weights, sector_idx):
        """计算指定扇区的T_K特征值"""
        N = self.n
        X = self.x.reshape(-1, 1)
        D2 = (X - self.x.reshape(1, -1)) ** 2
        op = self.sector_ops[sector_idx]
        
        K_full = np.zeros((8*N, 8*N), dtype=complex)
        for k in range(6):
            Ks = weights[k] * np.exp(-D2 / (2 * sigmas[k]**2))
            K_full += np.kron(Ks, self.gamma[k])
        
        K_full = K_full @ np.kron(np.eye(N), op)
        
        w = np.ones(N) / N
        T = K_full.copy()
        for i in range(8):
            T[i*N:(i+1)*N, :] *= w.reshape(-1, 1)
        
        ev = la.eigvals(T)
        ev = np.real(ev)
        return np.sort(ev)[::-1][:6]

def run():
    print("=" * 70)
    print("Three-Sector Independent Mass Scale Fitting")
    print("=" * 70)
    
    sectors = sm_masses_sectors()
    sector_names = ['leptons', 'up-quarks', 'down-quarks']
    all_masses = np.sort(np.concatenate(sectors))
    
    kernel = ThreeSectorKernel(n_points=50)
    
    # 系统搜索
    best_error = float('inf')
    best_result = None
    
    sigma_grid = [
        [0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
        [0.8, 0.2, 0.05, 0.02, 0.01, 0.005],
        [0.9, 0.3, 0.08, 0.03, 0.01, 0.004],
        [0.6, 0.15, 0.04, 0.02, 0.01, 0.003],
    ]
    
    w_uniform = [1/6]*6
    
    for sg in sigma_grid:
        wg = w_uniform
        print(f"\n--- sigmas={sg} ---")
        
        all_predicted = []
        sector_Cs = []
        
        for s_idx in range(3):
            ev = kernel.sector_spectrum(sg, wg, s_idx)
            pos = ev[ev > 1e-15]
            
            if len(pos) < 3:
                continue
            
            log_eig = -np.log(pos[:3])
            log_sm = np.log(sectors[s_idx])
            C = np.exp(np.mean(log_sm - np.log(log_eig)))
            predicted = C * log_eig
            sector_Cs.append(C)
            all_predicted.extend(predicted)
            
            print(f"  {sector_names[s_idx]}: C={C:.2f}, top3 ev={np.round(pos[:3], 6)}")
        
        all_predicted = np.array(sorted(all_predicted))
        error = np.mean(np.abs(np.log(all_predicted) - np.log(all_masses)))
        
        print(f"  RMSE={error:.4f}")
        
        if error < best_error:
            best_error = error
            best_result = (sg, sector_Cs, all_predicted)
    
    print("\n" + "=" * 70)
    print("BEST RESULT (Three Sectors)")
    print("=" * 70)
    sg, Cs, pred = best_result
    masses = all_masses
    
    print(f"\nSector scales: C_lepton={Cs[0]:.1f}, C_up={Cs[1]:.1f}, C_down={Cs[2]:.1f}")
    print(f"RMSE = {best_error:.4f}")
    
    print(f"\n{'Index':>6s} | {'SM Mass':>10s} | {'Predicted':>10s} | {'Ratio':>8s} | {'Sector':>10s}")
    print("-" * 50)
    sector_labels = ['lepton']*3 + ['up']*3 + ['down']*3
    for i in range(9):
        ratio = pred[i] / masses[i]
        s_label = sector_labels[i] if i < 9 else ""
        print(f"{i+1:>6d} | {masses[i]:>10.4f} | {pred[i]:>10.4f} | {ratio:>8.2f} | {s_label:>10s}")
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    ax = axes[0]
    ax.plot(range(1,10), np.log10(masses), 'o-', label='SM', linewidth=2, markersize=8)
    ax.plot(range(1,10), np.log10(pred[:9]), 's--', label='Predicted', linewidth=2, markersize=8)
    ax.set_xlabel('Particle index')
    ax.set_ylabel('log10(mass) [MeV]')
    ax.set_title(f'Three-Sector Fit (RMSE={best_error:.3f})')
    ax.legend()
    ax.grid(True)
    
    ax = axes[1]
    ax.scatter(np.log10(masses), np.log10(pred[:9]), s=100, c='red')
    lims = [-1, 6]
    ax.plot(lims, lims, 'b--', label='Perfect')
    ax.set_xlabel('log10(SM mass)')
    ax.set_ylabel('log10(Predicted)')
    ax.set_title(f'Correlation')
    ax.legend()
    ax.grid(True)
    
    ax = axes[2]
    ax.bar(['Lepton', 'Up', 'Down'], Cs)
    ax.set_ylabel('Sector mass scale C')
    ax.set_title('Independent Sector Scales')
    ax.grid(True)
    
    plt.tight_layout()
    plt.savefig('cl6_three_sector_mass.png', dpi=300)
    
    with open('cl6_three_sector_results.txt', 'w') as f:
        f.write("=== Three-Sector Mass Prediction ===\n\n")
        f.write(f"RMSE: {best_error:.4f}\n")
        f.write(f"C_sectors: {np.round(Cs, 1)}\n\n")
        for i in range(9):
            f.write(f"  {i+1}: SM={masses[i]:>10.4f} Pred={pred[i]:>10.4f}\n")
    
    print(f"\nResults saved to cl6_three_sector_results.txt")
    print(f"Plot saved to cl6_three_sector_mass.png")

if __name__ == "__main__":
    run()