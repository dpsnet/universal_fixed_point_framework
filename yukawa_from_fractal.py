"""
从IFS分形测度推导Yukawa耦合层级

核心思想: Cl(6)的3个Cartan投影P_s Γ_k P_s选择不同的有效分形维数d_s
d_s → 不同的C_s → 跨10^5量级的Yukawa层级

方法:
1. 构造Cl(6) Cartan生成元的扇形投影
2. 计算每个投影的有效分形维数
3. 从d_s推导C_s和Yukawa权重w_s
"""
import numpy as np
import matplotlib.pyplot as plt

def pauli():
    return [np.array(s, dtype=complex) for s in [
        [[0,1],[1,0]], [[0,-1j],[1j,0]], [[1,0],[0,-1]]]]

def cl6_gamma():
    s = pauli(); I2 = np.eye(2, dtype=complex)
    g = []
    for k in range(3):
        g.append(np.kron(np.kron(s[k], s[0]), I2))
    for k in range(3):
        g.append(np.kron(np.kron(I2, s[1]), s[k]))
    return g

def chiral_projectors(g):
    g7 = np.eye(8, dtype=complex)
    for k in range(6):
        g7 = g7 @ g[k] * (-1j)
    P_L = (np.eye(8) - g7) / 2
    P_R = (np.eye(8) + g7) / 2
    return P_L, P_R

class FractalYukawa:
    """从IFS分形测度计算Yukawa耦合"""
    def __init__(self, contractions, probs=None):
        self.c = np.array(contractions)
        self.p = np.array(probs) if probs is not None else np.ones(len(contractions))/len(contractions)
        self.d = self._fractal_dimension()
        
        # Cl(6)代数结构
        g = cl6_gamma()
        P_L, P_R = chiral_projectors(g)
        
        # 3个Cartan生成元的扇形投影
        self.sector_projections = []
        for k in range(3):
            J = 1j * g[2*k] @ g[2*k+1]
            proj = P_L @ J @ P_L
            self.sector_projections.append(proj[:4, :4])
    
    def _fractal_dimension(self):
        def f(d): return np.sum(self.c**d) - 1
        lo, hi = 0.01, 5.0
        for _ in range(50):
            mid = (lo + hi)/2
            if f(mid) > 0: lo = mid
            else: hi = mid
        return (lo + hi)/2
    
    def effective_dimension(self, projection):
        """从投影矩阵计算有效分形维数"""
        ev = np.linalg.eigvalsh(projection)
        ev = np.abs(ev)
        ev = ev[ev > 1e-10]
        
        if len(ev) == 0:
            return self.d
        
        # 有效维数 = 投影范数 × 分形维数
        norm = np.sqrt(np.sum(ev**2))
        return self.d * norm
    
    def compute_yukawa_weights(self):
        """计算3个扇区的Yukawa权重"""
        d_eff = np.array([self.effective_dimension(p) for p in self.sector_projections])
        
        # 从有效维数计算C_s: C_s ∝ exp(α/d_eff)
        # d越小 → C_s越小 → Yukawa权重越小
        alpha = 1.0
        C_s = np.exp(alpha / d_eff)
        C_s = C_s / C_s[0]  # 归一化到轻子扇区
        
        # Yukawa权重: w_s = v_SM / C_s
        v_SM = 246000.0
        ws = v_SM / C_s
        
        return d_eff, C_s, ws

def run():
    print("=" * 70)
    print("Yukawa Hierarchy from IFS Fractal Measure")
    print("=" * 70)
    
    # 测试不同IFS配置
    configs = [
        ([0.5, 0.5], "Cantor d=1.0"),
        ([0.3, 0.3, 0.4], "3-Cantor"),
        ([0.2, 0.3, 0.5], "diverse"),
        ([0.15, 0.15, 0.15, 0.15], "small c"),
    ]
    
    sm_ws = {'lepton': 464150, 'up': 134426, 'down': 71098}
    
    for cf, name in configs:
        fy = FractalYukawa(cf)
        d_eff, C_s, ws = fy.compute_yukawa_weights()
        
        print(f"\n--- {name} (d={fy.d:.4f}) ---")
        print(f"  Effective dimensions: {np.round(d_eff, 4)}")
        print(f"  Sector scales C_s: {np.round(C_s, 4)}")
        print(f"  Yukawa weights w_s: {np.round(ws, 0).astype(int)}")
        print(f"  Weight ratios (lepton=1): {np.round(ws/ws[0], 4)}")
        print(f"  SM target w_s: {sm_ws}")
    
    # 扫描参数α寻找SM匹配
    print(f"\n\n{'='*70}")
    print("Parameter Scan: Finding α for SM Match")
    print(f"{'='*70}")
    
    fy = FractalYukawa([0.5, 0.5])
    
    best_error = float('inf')
    best = None
    
    for alpha in np.logspace(-2, 2, 50):
        d_eff = np.array([fy.effective_dimension(p) for p in fy.sector_projections])
        C_s = np.exp(alpha / d_eff)
        C_s = C_s / C_s[0]
        
        # 目标C_s比值 (从逆谱构造)
        target = np.array([1.0, 3.45, 6.53])
        error = np.mean(np.abs(C_s - target))
        
        if error < best_error:
            best_error = error
            best = (alpha, C_s.copy(), d_eff.copy())
    
    if best:
        alpha, C_s, d_eff = best
        print(f"\nBest α = {alpha:.4f}, RMSE = {best_error:.4f}")
        print(f"C_s ratios: {np.round(C_s, 4)} (target: [1, 3.45, 6.53])")
        print(f"d_eff: {np.round(d_eff, 4)}")
        
        # 由C_s → 质量预测
        v_SM = 246000.0
        k_arr = np.array([1, 2, 3])
        d = fy.d
        
        print(f"\nMass prediction with d={d:.4f}:")
        for s_idx, C in enumerate(C_s):
            sector_masses = C * k_arr**(2/d)
            print(f"  Sector {s_idx+1} (C={C:.2f}): {np.round(sector_masses, 2)} MeV")
    
    # 绘图
    plt.figure(figsize=(12, 5))
    
    plt.subplot(121)
    alphas = np.logspace(-2, 2, 100)
    errors = []
    for a in alphas:
        C = np.exp(a / d_eff)
        C = C / C[0]
        errors.append(np.mean(np.abs(C - target)))
    plt.loglog(alphas, errors)
    plt.axvline(x=best[0], color='r', linestyle='--', label=f'best α={best[0]:.3f}')
    plt.xlabel('α')
    plt.ylabel('RMSE')
    plt.title('Optimizing α for SM C_s ratios')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(122)
    labels = ['Lepton', 'Up', 'Down']
    x = np.arange(3)
    plt.bar(x - 0.2, [1, 3.45, 6.53], 0.4, label='SM target')
    plt.bar(x + 0.2, C_s, 0.4, label=f'Fractal α={best[0]:.2f}')
    plt.xticks(x, labels)
    plt.ylabel('C_s / C_lepton')
    plt.title('C_s Ratio: Fractal vs SM')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('yukawa_from_fractal.png', dpi=300)
    
    with open('yukawa_fractal_results.txt', 'w', encoding='utf-8') as f:
        f.write("=== Yukawa from Fractal ===\n\n")
        if best:
            f.write(f"Best α = {best[0]:.4f}\n")
            f.write(f"C_s: {np.round(C_s, 4)}\n")
            f.write(f"d_eff: {np.round(d_eff, 4)}\n")
            f.write(f"RMSE: {best_error:.4f}\n")
    
    print(f"\nResults saved to yukawa_fractal_results.txt")

if __name__ == "__main__":
    run()