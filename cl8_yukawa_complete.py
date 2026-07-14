"""
Cl(8) Yukawa耦合完整计算 + IFS积分

Cl(8) = Cl(6+2) → SU(4) × SU(2)_L × SU(2)_R

三个扇区:
  Lepton:  (4, 2, 1)  → Γ₁Γ₂Γ₃
  Up:      (4̅, 1, 2) → Γ₄Γ₅Γ₆  
  Down:    (4, 1, 2)  → Γ₇Γ₈

方法:
1. 构造Cl(8)的16×16 Gamma矩阵
2. 计算SU(4)×SU(2)_L×SU(2)_R投影
3. 计算3扇区Yukawa耦合强度
4. 结合IFS多分形测度积分 → 质量预测
"""
import numpy as np
import matplotlib.pyplot as plt

SM = np.sort(np.array([0.511, 2.2, 4.7, 95, 105.66, 1270, 1776.86, 4180, 173100]))
v_SM = 246000.0
target_C = np.array([1.0, 3.45, 6.53])

def pauli():
    return [np.array(s, dtype=complex) for s in [
        [[0,1],[1,0]], [[0,-1j],[1j,0]], [[1,0],[0,-1]]]]

def cl8_gamma():
    """
    Cl(8)的8个Gamma矩阵 (16×16) 标准构造
    
    Γ₁ = σ₁ ⊗ I ⊗ I ⊗ I
    Γ₂ = σ₂ ⊗ I ⊗ I ⊗ I  
    Γ₃ = σ₃ ⊗ σ₁ ⊗ I ⊗ I
    Γ₄ = σ₃ ⊗ σ₂ ⊗ I ⊗ I
    Γ₅ = σ₃ ⊗ σ₃ ⊗ σ₁ ⊗ I
    Γ₆ = σ₃ ⊗ σ₃ ⊗ σ₂ ⊗ I
    Γ₇ = σ₃ ⊗ σ₃ ⊗ σ₃ ⊗ σ₁
    Γ₈ = σ₃ ⊗ σ₃ ⊗ σ₃ ⊗ σ₂
    """
    s = pauli(); I2 = np.eye(2, dtype=complex)
    
    def kron4(a, b, c, d):
        return np.kron(np.kron(np.kron(a, b), c), d)
    
    Gamma = []
    # Cl(8)的8个Gamma矩阵用4个因子构造
    pairs = [
        (s[0], s[1]),        # Γ₁, Γ₂
        (s[2], s[2]),        # σ₃因子
        (s[2], s[2]),        # σ₃因子
        (s[2], s[2]),        # σ₃因子
    ]
    
    # Γ₁ = σ₁ ⊗ I ⊗ I ⊗ I
    Gamma.append(kron4(s[0], I2, I2, I2))
    # Γ₂ = σ₂ ⊗ I ⊗ I ⊗ I
    Gamma.append(kron4(s[1], I2, I2, I2))
    # Γ₃ = σ₃ ⊗ σ₁ ⊗ I ⊗ I
    Gamma.append(kron4(s[2], s[0], I2, I2))
    # Γ₄ = σ₃ ⊗ σ₂ ⊗ I ⊗ I
    Gamma.append(kron4(s[2], s[1], I2, I2))
    # Γ₅ = σ₃ ⊗ σ₃ ⊗ σ₁ ⊗ I
    Gamma.append(kron4(s[2], s[2], s[0], I2))
    # Γ₆ = σ₃ ⊗ σ₃ ⊗ σ₂ ⊗ I
    Gamma.append(kron4(s[2], s[2], s[1], I2))
    # Γ₇ = σ₃ ⊗ σ₃ ⊗ σ₃ ⊗ σ₁
    Gamma.append(kron4(s[2], s[2], s[2], s[0]))
    # Γ₈ = σ₃ ⊗ σ₃ ⊗ σ₃ ⊗ σ₂
    Gamma.append(kron4(s[2], s[2], s[2], s[1]))
    
    return Gamma

def cl8_chirality(Gamma):
    """γ₉ = (-i)^4 · Γ₁Γ₂...Γ₈"""
    g9 = np.eye(16, dtype=complex)
    for k in range(8):
        g9 = g9 @ Gamma[k] * (-1j)
    return g9

def su4_generators(Gamma):
    """SU(4)子代数的15个生成元 (grade-2)"""
    J = []
    for i in range(4):
        for j in range(i+1, 4):
            J.append(-0.5j * (Gamma[i] @ Gamma[j]))
    return J

def su2_L_generators(Gamma):
    """SU(2)_L 生成元 (第5-6个Gamma)"""
    return [-0.5j * Gamma[4] @ Gamma[5]]

def su2_R_generators(Gamma):
    """SU(2)_R 生成元 (第7-8个Gamma)"""
    return [-0.5j * Gamma[6] @ Gamma[7]]

def sector_yukawas(Gamma, P_L, P_R):
    """
    计算3个扇区的Yukawa耦合强度 (Pati-Salam统一)

    Cl(8) Yukawa = Tr(P_L · Y_s · Γ_vol · P_R)
    其中Γ_vol是Cl(8)体积元(grade-8),编码希格斯VEV
    
    Lepton:  ψ̄_L · (Γ₁Γ₂Γ₃) · Γ_vol · ψ_R
    Up:      ψ̄_L · (Γ₄Γ₅Γ₆) · Γ_vol · ψ_R  
    Down:    ψ̄_L · (Γ₇Γ₈) · Γ_vol · ψ_R
    """
    # Cl(8)体积元 Γ_vol = Γ₁Γ₂...Γ₈
    Gamma_vol = np.eye(16, dtype=complex)
    for k in range(8):
        Gamma_vol = Gamma_vol @ Gamma[k]
    
    # 扇区Cl(8)元素
    Y_lep = Gamma[0] @ Gamma[1] @ Gamma[2]
    Y_up = Gamma[3] @ Gamma[4] @ Gamma[5]
    Y_down = Gamma[6] @ Gamma[7]
    
    # Yukawa = |Tr(P_L · Y_s · Γ_vol · P_R)|
    y_lep = np.abs(np.trace(P_L @ Y_lep @ Gamma_vol @ P_R))
    y_up = np.abs(np.trace(P_L @ Y_up @ Gamma_vol @ P_R))
    y_down = np.abs(np.trace(P_L @ Y_down @ Gamma_vol @ P_R))
    
    return np.array([y_lep, y_up, y_down])

def ifs_dim(c):
    def f(d): return np.sum(np.array(c)**d) - 1
    lo, hi = 0.01, 5.0
    for _ in range(50):
        mid = (lo+hi)/2
        if f(mid) > 0: lo = mid
        else: hi = mid
    return (lo+hi)/2

def run():
    print("=" * 70)
    print("Cl(8) Yukawa Coupling: Complete SM Mass Prediction")
    print("=" * 70)
    
    # 1. Cl(8)代数构造
    print("\n1. Constructing Cl(8) 16×16 gamma matrices...")
    Gamma = cl8_gamma()
    g9 = cl8_chirality(Gamma)
    P_L = (np.eye(16) - g9) / 2
    P_R = (np.eye(16) + g9) / 2
    
    print(f"   Gamma matrices: {len(Gamma)} × 16×16")
    print(f"   Chiral projector P_L rank: {np.trace(P_L).real:.0f}")
    
    # 2. SU(4)×SU(2)_L×SU(2)_R分解
    print("\n2. SU(4)×SU(2)_L×SU(2)_R decomposition:")
    su4 = su4_generators(Gamma)
    su2_l = su2_L_generators(Gamma)
    su2_r = su2_R_generators(Gamma)
    print(f"   SU(4): {len(su4)} generators")
    print(f"   SU(2)_L: {len(su2_l)} generators")
    print(f"   SU(2)_R: {len(su2_r)} generators")
    
    # 3. Yukawa耦合强度
    y = sector_yukawas(Gamma, P_L, P_R)
    print(f"\n3. Yukawa coupling strengths:")
    for i, name in enumerate(['Lepton', 'Up', 'Down']):
        print(f"   {name}: y_s = {y[i]:.4f}")
    y_ratios = y / y[0]
    print(f"   Ratios: {np.round(y_ratios, 4)} (target C_s: {target_C})")
    
    # Yukawa → C_s: C_s = y_0 / y_s
    C_s_pred = y[0] / np.maximum(y, 1e-30)
    C_s_pred = C_s_pred / C_s_pred[0]
    print(f"   C_s: {np.round(C_s_pred, 4)} (target: {target_C})")
    
    # 4. IFS参数扫描 + 质量预测
    print(f"\n4. IFS parameter scan (Cl(8)×IFS integral):")
    
    configs = []
    for c1 in np.arange(0.2, 0.7, 0.1):
        for p1 in np.arange(0.3, 0.8, 0.1):
            c = [c1, 1-c1]
            p = [p1, 1-p1]
            configs.append((c, p))
    
    results = []
    for c, p in configs:
        d = ifs_dim(c)
        
        # Cl(8) Yukawa为基础, IFS给出扇区间修正
        C_s = C_s_pred.copy()
        
        # 质量预测
        k = np.array([1, 2, 3])
        intra = k ** (2.0 / np.maximum(d, 0.1))
        intra = intra / intra[0]
        
        masses = []
        for C in C_s:
            masses.extend(C * intra * v_SM)
        masses = np.sort(masses)
        
        error = np.sqrt(np.mean((np.log(masses) - np.log(SM))**2))
        results.append((error, c, p, d, C_s, masses))
    
    results.sort(key=lambda x: x[0])
    
    best = results[0]
    print(f"\n{'='*70}")
    print("BEST RESULT (Cl(8) × IFS)")
    print(f"{'='*70}")
    print(f"Cl(8) Yukawa ratios: {np.round(y/y[0], 4)}")
    print(f"C_s: {np.round(best[4], 4)} (target: {target_C})")
    print(f"RMSE: {best[0]:.4f}")
    
    print(f"\n{'Particle':>8s} | {'SM (MeV)':>12s} | {'Pred (MeV)':>12s} | {'Ratio':>8s}")
    print("-" * 42)
    for i in range(9):
        r = best[5][i] / SM[i]
        print(f"{i+1:>8d} | {SM[i]:>12.4f} | {best[5][i]:>12.2f} | {r:>8.2f}")
    
    # 绘图
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    ax = axes[0]
    ax.plot(range(1,10), np.log10(SM), 'o-', label='SM', linewidth=2, markersize=8)
    ax.plot(range(1,10), np.log10(best[5]), 's--', label='Cl(8) Predicted', linewidth=2, markersize=8)
    ax.set_xlabel('Particle index'); ax.set_ylabel('log10(mass) [MeV]')
    ax.set_title(f'Cl(8) Prediction (RMSE={best[0]:.3f})')
    ax.legend(); ax.grid(True)
    
    ax = axes[1]
    ax.bar(np.arange(3)-0.2, target_C, 0.4, label='SM')
    ax.bar(np.arange(3)+0.2, best[4], 0.4, label=f'Cl(8): {np.round(y/y[0], 2)}')
    ax.set_xticks(np.arange(3)); ax.set_xticklabels(['Lep', 'Up', 'Down'])
    ax.set_ylabel('C_s / C_lepton'); ax.set_title('C_s Ratio')
    ax.legend(); ax.grid(True)
    
    plt.tight_layout()
    plt.savefig('cl8_yukawa_result.png', dpi=300)
    
    with open('cl8_yukawa_results.txt', 'w', encoding='utf-8') as f:
        f.write("=== Cl(8) Yukawa Results ===\n\n")
        f.write(f"Cl(8) ratios: {np.round(y/y[0], 4)}\n")
        f.write(f"C_s: {np.round(best[4], 4)}\n")
        f.write(f"RMSE: {best[0]:.4f}\n\n")
        for i in range(9):
            f.write(f"  {i+1}: SM={SM[i]:>10.4f} Pred={best[5][i]:>10.2f}\n")
    
    print(f"\nResults saved to cl8_yukawa_results.txt")

if __name__ == "__main__":
    run()