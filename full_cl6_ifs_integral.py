"""
Cl(6)投影×IFS测度全积分计算

核心: y_s = ∫∫ ψ_s(x) K(x,y) ψ_s(y) dμ(x) dμ(y)

方法: IFS树叶子节点的Cl(6)加权求和
  每个叶子 = IFS分支序列 {b₁, b₂, ..., b_D}
  Cl(6)投影 = ∏ J_{b_k} (Cartan生成元的乘积)
  Yukawa权重 = Σ |Cl(6)投影|² × IFS测度
"""
import numpy as np
import matplotlib.pyplot as plt

SM = np.sort(np.array([0.511, 2.2, 4.7, 95, 105.66, 1270, 1776.86, 4180, 173100]))
v_SM = 246000.0
target_C = np.array([1.0, 3.45, 6.53])

def pauli():
    return [np.array(s, dtype=complex) for s in [
        [[0,1],[1,0]], [[0,-1j],[1j,0]], [[1,0],[0,-1]]]]

def cl6_cartan_4x4():
    """3个Cartan生成元的4×4手征表示"""
    s = pauli(); I2 = np.eye(2, dtype=complex)
    g = []
    for k in range(3):
        g.append(np.kron(np.kron(s[k], s[0]), I2))
    for k in range(3):
        g.append(np.kron(np.kron(I2, s[1]), s[k]))
    J = []
    for k in range(3):
        Jk = 1j * g[2*k] @ g[2*k+1]
        J.append(Jk[:4, :4])
    return J

def sector_projection_matrices():
    """3个扇区的投影矩阵P_s"""
    J = cl6_cartan_4x4()
    
    # 扇区投影 = 不同Cartan生成元的组合
    # 轻子: J₁ (SU(2)弱作用)
    # 上夸克: J₂ (U(1)超荷)
    # 下夸克: J₃ (色-弱混合)
    return [J[0], J[1], J[2]]

class Cl6IFSIntegrator:
    """Cl(6)投影×IFS测度全积分器"""
    def __init__(self, contractions, probabilities, depth=10):
        self.c = np.array(contractions)
        self.p = np.array(probabilities)
        self.N = len(contractions)
        self.depth = depth
        self.P = sector_projection_matrices()  # 3个扇区投影
    
    def compute_yukawa_weights(self):
        """计算3个扇区的Yukawa权重"""
        sector_weights = np.zeros(3, dtype=complex)
        total_measure = np.zeros(3)
        
        # 递归遍历IFS树
        def traverse(pos, measure, depth, cl6_state):
            if depth == 0:
                # 叶子节点: 计算Cl(6)投影
                for s in range(3):
                    proj_val = np.trace(self.P[s] @ cl6_state)
                    sector_weights[s] += measure * proj_val
                    total_measure[s] += measure
                return
            
            for i in range(self.N):
                new_pos = pos + (self.c[i]**depth) * (2*np.random.random() - 1)
                new_measure = measure * self.p[i]
                
                # Cl(6)状态演化: J_i @ cl6_state
                J = sector_projection_matrices()[i % 3]
                new_state = J @ cl6_state
                
                traverse(new_pos, new_measure, depth-1, new_state)
        
        # 从单位矩阵开始
        traverse(0.5, 1.0, self.depth, np.eye(4, dtype=complex))
        
        # Yukawa权重 = 归一化后的扇区投影
        yukawa = np.abs(sector_weights) / np.maximum(np.abs(total_measure), 1e-30)
        yukawa = yukawa / np.maximum(yukawa[0], 1e-30)
        
        return yukawa

def run():
    print("=" * 70)
    print("Full Cl(6)×IFS Integral: Final SM Mass Prediction")
    print("=" * 70)
    
    # 扫描IFS参数
    configs = []
    for c1 in np.arange(0.2, 0.7, 0.12):
        for p1 in np.arange(0.4, 0.8, 0.15):
            c = [c1, 1-c1]
            p = [p1, 1-p1]
            configs.append((c, p, f"c={c1:.2f},p={p1:.2f}"))
    
    results = []
    
    for c, p, name in configs:
        integrator = Cl6IFSIntegrator(c, p, depth=8)
        yukawa = integrator.compute_yukawa_weights()
        
        # Yukawa权重 → C_s
        C_s = 1.0 / np.maximum(yukawa, 1e-30)
        C_s = C_s / C_s[0]
        
        # C_s → 质量预测
        d = _dimension(c)
        k_arr = np.array([1, 2, 3])
        intra = k_arr ** (2.0 / np.maximum(d, 0.1))
        intra = intra / intra[0]
        
        masses = []
        for C in C_s:
            sector_masses = C * intra * v_SM
            masses.extend(sector_masses)
        masses = np.sort(masses)
        
        error = np.sqrt(np.mean((np.log(masses) - np.log(SM))**2))
        C_err = np.mean(np.abs(C_s - target_C))
        
        results.append((error, C_err, c, p, d, C_s, masses, name))
        print(f"  {name}: C_s={np.round(C_s,3)}, C_err={C_err:.3f}, RMSE={error:.3f}")
    
    results.sort(key=lambda x: x[0])
    
    if results:
        best = results[0]
        print(f"\n{'='*70}")
        print("BEST SM MASS PREDICTION (Full Integral)")
        print(f"{'='*70}")
        print(f"IFS: c={np.round(best[2],4)}, p={np.round(best[3],4)}, d={best[4]:.4f}")
        print(f"C_s: {np.round(best[5],4)} (target: {target_C})")
        print(f"C_err: {best[1]:.4f}, RMSE: {best[0]:.4f}")
        
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
        plt.title(f'Full Cl(6)×IFS Integral (RMSE={best[0]:.3f})')
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
    plt.savefig('full_cl6_ifs_integral.png', dpi=300)
    
    with open('full_integral_results.txt', 'w', encoding='utf-8') as f:
        if results:
            f.write("=== Full Cl(6)×IFS Integral ===\n\n")
            f.write(f"c={np.round(best[2],4)}, p={np.round(best[3],4)}\n")
            f.write(f"C_s={np.round(best[5],4)}\n")
            f.write(f"RMSE={best[0]:.4f}\n\n")
            for i in range(9):
                f.write(f"  {i+1}: SM={SM[i]:>10.4f} Pred={best[6][i]:>10.2f}\n")
    
    print(f"\nResults saved to full_integral_results.txt")

def _dimension(c):
    def f(d): return np.sum(np.array(c)**d) - 1
    lo, hi = 0.01, 5.0
    for _ in range(50):
        mid = (lo+hi)/2
        if f(mid) > 0: lo = mid
        else: hi = mid
    return (lo+hi)/2

if __name__ == "__main__":
    run()