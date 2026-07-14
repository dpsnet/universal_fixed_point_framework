"""
希格斯×Cl(6)耦合全积分计算

核心: y_s = ⟨Tr( P_L · Γ_L · P_L · H_s · P_R )⟩_μ

其中:
  P_L, P_R = 手征投影
  Γ_L = SU(2)双元投影 (γ₁+iγ₂ 或 γ₃+iγ₄)
  H_s = 希格斯VEV的Cl(6)表示 (γ₃-iγ₄ 或 γ₁-iγ₂)
  ⟨·⟩_μ = IFS测度平均
"""
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

SM = np.sort(np.array([0.511, 2.2, 4.7, 95, 105.66, 1270, 1776.86, 4180, 173100]))
v_SM = 246000.0
target_C = np.array([1.0, 3.45, 6.53])

def pauli():
    return [np.array(s, dtype=complex) for s in [
        [[0,1],[1,0]], [[0,-1j],[1j,0]], [[1,0],[0,-1]]]]

def cl6_weyl_basis():
    """Cl(6) Gamma矩阵 + 手征投影 (Weyl基)"""
    s = pauli(); I2 = np.eye(2, dtype=complex)
    g = []
    for k in range(3):
        g.append(np.kron(np.kron(s[k], s[0]), I2))
    for k in range(3):
        g.append(np.kron(np.kron(I2, s[1]), s[k]))
    
    g7 = np.eye(8, dtype=complex)
    for k in range(6): g7 = g7 @ g[k] * (-1j)
    P_L = (np.eye(8) - g7) / 2
    P_R = (np.eye(8) + g7) / 2
    return g, P_L, P_R

def yukawa_couplings():
    """
    计算3个扇区的Yukawa耦合强度
    
    物理: 
      Lepton: L̅ Φ e_R → P_L(γ₁+iγ₂)P_L · P_L(γ₃-iγ₄)P_R
      Up:     Q̅ Φ̃ u_R → P_L(γ₃+iγ₄)P_L · P_L(γ₁-iγ₂)P_R
      Down:   Q̅ Φ d_R → P_L(γ₃+iγ₄)P_L · P_L(γ₃-iγ₄)P_R
    """
    g, P_L, P_R = cl6_weyl_basis()
    
    # SU(2)双元投影
    Gamma_L_lep = g[0] + 1j*g[1]   # γ₁+iγ₂ (轻子双元)
    Gamma_L_quark = g[2] + 1j*g[3]  # γ₃+iγ₄ (夸克双元)
    
    # 希格斯VEV投影
    H_lep_down = g[2] - 1j*g[3]     # γ₃-iγ₄ (轻子+下夸克)
    H_up = g[0] - 1j*g[1]           # γ₁-iγ₂ (上夸克)
    
    # 扇区耦合 = Tr( P_L · Γ_L · P_L · H · P_R )
    def coupling(Gamma_L, H):
        M = P_L @ Gamma_L @ P_L @ H @ P_R
        return np.abs(np.trace(M))
    
    y_lep = coupling(Gamma_L_lep, H_lep_down)
    y_up = coupling(Gamma_L_quark, H_up)
    y_down = coupling(Gamma_L_quark, H_lep_down)
    
    return np.array([y_lep, y_up, y_down])

def ifs_dim(c):
    def f(d): return np.sum(np.array(c)**d) - 1
    lo, hi = 0.01, 5.0
    for _ in range(50):
        mid = (lo+hi)/2
        if f(mid) > 0: lo = mid
        else: hi = mid
    return (lo+hi)/2

def ifs_fractal_measure(c, p, depth=12):
    """生成IFS分形测度原子"""
    atoms = []
    def traverse(pos, w, d):
        if d == 0:
            atoms.append((pos, w))
            return
        for i in range(len(c)):
            new_pos = (pos + (2*i - len(c) + 1) / (2*len(c))) * 0.5 + 0.5
            traverse(new_pos, w * p[i], d-1)
    traverse(0.5, 1.0, depth)
    return np.array(atoms)

def sector_integral(c, p, depth=10):
    """扇区全积分: ∫ K_s(x,y) dμ(x)dμ(y)"""
    atoms = ifs_fractal_measure(c, p, depth)
    N = len(atoms)
    
    # 各扇区Yukawa耦合
    y = yukawa_couplings()
    
    # 核矩阵: K(x,y) = exp(-(x-y)²/2σ²)
    sigma = 0.1
    K = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            dx = atoms[i,0] - atoms[j,0]
            K[i,j] = np.exp(-dx**2 / (2*sigma**2))
    
    # 扇区积分: y_s = ∫∫ K(x,y) dμ_s(x)dμ_s(y)
    sector_masses = np.zeros(3)
    for s in range(3):
        measure = atoms[:,1]
        weighted_K = K * measure.reshape(-1,1) * measure.reshape(1,-1)
        sector_masses[s] = np.sum(weighted_K) * y[s]
    
    return sector_masses / np.maximum(sector_masses[0], 1e-30)

def run():
    print("=" * 70)
    print("Higgs×Cl(6) Full Integral: SM Mass Prediction")
    print("=" * 70)
    
    # 基础Yukawa耦合
    y_base = yukawa_couplings()
    print(f"\nBase Yukawa couplings:")
    for i, name in enumerate(['Lepton', 'Up', 'Down']):
        print(f"  {name}: y = {y_base[i]:.6f}")
    print(f"  Ratios: {np.round(y_base/y_base[0], 4)}")
    
    # 扫描IFS参数
    configs = []
    for c1 in np.arange(0.2, 0.7, 0.1):
        for p1 in np.arange(0.3, 0.8, 0.12):
            c = [c1, 1-c1]
            p = [p1, 1-p1]
            configs.append((c, p))
    
    results = []
    
    for c, p in configs:
        try:
            s_ratios = sector_integral(c, p, depth=8)
            d = ifs_dim(c)
            
            # 扇区积分 → C_s
            C_s = 1.0 / np.maximum(s_ratios, 1e-30)
            C_s = C_s / C_s[0]
            
            # C_s → 质量
            k = np.array([1, 2, 3])
            intra = k ** (2.0 / np.maximum(d, 0.1))
            intra = intra / intra[0]
            
            masses = []
            for C in C_s:
                masses.extend(C * intra * v_SM)
            masses = np.sort(masses)
            
            error = np.sqrt(np.mean((np.log(masses) - np.log(SM))**2))
            C_err = np.mean(np.abs(C_s - target_C))
            
            results.append((error, C_err, c, p, d, C_s, masses))
            
            if C_err < 10:  # 只显示合理结果
                print(f"  c={c}, p={np.round(p,2)}: C_s={np.round(C_s,3)}, RMSE={error:.3f}, C_err={C_err:.3f}")
        except:
            pass
    
    results.sort(key=lambda x: x[0])
    
    if results:
        best = results[0]
        print(f"\n{'='*70}")
        print("BEST RESULT (Higgs×Cl(6) Full Integral)")
        print(f"{'='*70}")
        print(f"IFS: c={np.round(best[2],4)}, p={np.round(best[3],4)}, d={best[4]:.4f}")
        print(f"C_s: {np.round(best[5],4)} (target: {target_C})")
        print(f"RMSE: {best[0]:.4f}")
        
        print(f"\n{'Particle':>8s} | {'SM (MeV)':>12s} | {'Pred (MeV)':>12s} | {'Ratio':>8s}")
        print("-" * 42)
        for i in range(9):
            r = best[6][i] / SM[i]
            print(f"{i+1:>8d} | {SM[i]:>12.4f} | {best[6][i]:>12.2f} | {r:>8.2f}")
    
    plt.figure(figsize=(12, 5))
    if results:
        best = results[0]
        plt.subplot(121)
        plt.plot(range(1,10), np.log10(SM), 'o-', label='SM', linewidth=2, markersize=8)
        plt.plot(range(1,10), np.log10(best[6]), 's--', label='Predicted', linewidth=2, markersize=8)
        plt.xlabel('Particle index')
        plt.ylabel('log10(mass) [MeV]')
        plt.title(f'Higgs×Cl(6) Integral (RMSE={best[0]:.3f})')
        plt.legend()
        plt.grid(True)
        
        plt.subplot(122)
        plt.scatter(np.log10(SM), np.log10(best[6]), s=100, c='red')
        lims = [-1, 6]
        plt.plot(lims, lims, 'b--')
        plt.xlabel('log10(SM mass)')
        plt.ylabel('log10(Predicted)')
        plt.title('Correlation')
        plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('higgs_cl6_integral.png', dpi=300)
    
    print(f"\nResults saved to higgs_cl6_integral_results.txt")

if __name__ == "__main__":
    run()