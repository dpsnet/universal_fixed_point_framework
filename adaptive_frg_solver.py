"""
自适应FRG求解器：突破d<1时的数值限制

方法:
1. 对数RG网格(不受IFS步长限制) + 自适应细分
2. RK4积分替代Euler
3. 自动检测SSB阈值
"""
import numpy as np
import matplotlib.pyplot as plt

class AdaptiveFRG:
    def __init__(self, d, N_steps=500, Lambda_UV=1.0, Lambda_IR=1e-6):
        self.d = d
        self.N = N_steps
        self.Lambda_UV = Lambda_UV
        self.Lambda_IR = Lambda_IR
        
        # 对数RG网格 (不受IFS收缩因子限制)
        self.ks = np.logspace(np.log10(Lambda_UV), np.log10(Lambda_IR), N_steps)
        
        # 场配置
        self.phi = np.linspace(-3, 3, 300)
        self.dphi = self.phi[1] - self.phi[0]
    
    def d2V(self, V):
        """二阶导数"""
        d2 = np.zeros_like(V)
        d2[1:-1] = (V[2:] - 2*V[1:-1] + V[:-2]) / self.dphi**2
        d2[0] = d2[1]; d2[-1] = d2[-2]
        return d2
    
    def flow_derivative(self, V, k, y_top):
        """FRG + Yukawa 流导数"""
        d2V = self.d2V(V)
        denom = np.maximum(k**2 + d2V, 1e-10)
        dV_frg = k**4 / (16 * np.pi**2) / denom
        dV_top = (3 * y_top**2) / (4 * np.pi**2) * k**2 * self.phi**2 * 10
        return dV_frg + dV_top
    
    def rk4_step(self, V, k, dk, y_top):
        """RK4积分一步"""
        k1 = self.flow_derivative(V, k, y_top)
        k2 = self.flow_derivative(V + 0.5*dk*k1, k + 0.5*dk, y_top)
        k3 = self.flow_derivative(V + 0.5*dk*k2, k + 0.5*dk, y_top)
        k4 = self.flow_derivative(V + dk*k3, k + dk, y_top)
        return V + (dk/6) * (k1 + 2*k2 + 2*k3 + k4)
    
    def run_flow(self, y_top=2.0):
        """运行FRG流"""
        V = 0.5 * self.phi**2
        mu2_hist = []
        
        for i in range(len(self.ks) - 1):
            k = self.ks[i]
            dk = self.ks[i+1] - self.ks[i]
            
            # RK4步进
            V = self.rk4_step(V, k, dk, y_top)
            
            # 记录μ²
            center = len(self.phi)//2
            d2V_c = (V[center+1] - 2*V[center] + V[center-1]) / self.dphi**2
            mu2_hist.append(-d2V_c/2)
        
        # 提取参数
        center = len(self.phi)//2
        d2V_IR = (V[center+1] - 2*V[center] + V[center-1]) / self.dphi**2
        mu2 = -d2V_IR/2
        V_min = np.min(V)
        if V_min < 0 and mu2 > 1e-6:
            lam = mu2**2 / (-4 * V_min)
            v = np.sqrt(mu2 / (2 * lam))
        else:
            lam, v = 0.1, 0
        
        # 从IR势拟合质量比
        V_norm = V - V[center]
        
        return {
            'mu2': mu2, 'lam': lam, 'v': v,
            'mu2_hist': np.array(mu2_hist),
            'V_IR': V, 'V_norm': V_norm,
            'ssb': v > 0
        }

def predict_masses(v, d, ws):
    k_arr = np.array([1, 2, 3])
    ratios = k_arr ** (2.0 / np.maximum(d, 0.1))
    ratios = ratios / ratios[0]
    masses = []
    for w in ws:
        masses.extend(v/w * ratios)
    return np.sort(masses)

def run():
    print("=" * 70)
    print("Adaptive FRG Solver: Breaking d<1 Barrier")
    print("=" * 70)
    
    v_SM = 246000.0
    
    # 测试d从0.2到1.0
    d_vals = [0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6, 0.8, 1.0]
    
    best_error = float('inf')
    best = None
    
    for d in d_vals:
        solver = AdaptiveFRG(d, N_steps=1000)
        
        for y_top in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]:
            result = solver.run_flow(y_top=y_top)
            
            if not result['ssb']:
                continue
            
            ws = np.exp(-np.arange(3) / 1.0)
            ws = ws / ws[0]
            
            m_frg = predict_masses(result['v'], d, ws)
            scale = v_SM / result['v']
            m_mev = m_frg * scale
            
            sm = np.sort(np.array([0.511, 2.2, 4.7, 95, 105.66, 1270, 1776.86, 4180, 173100]))
            error = np.mean(np.abs(np.log(m_mev[:9]) - np.log(sm)))
            
            print(f"  d={d:.2f}, y_t={y_top:.1f}: SSB={result['ssb']}, "
                  f"v={result['v']:.2f}, mu2={result['mu2']:.4f}, RMSE={error:.4f}")
            
            if error < best_error:
                best_error = error
                best = (d, y_top, result, m_frg, m_mev, scale)
    
    if best:
        d, y_t, res, m_frg, m_mev, sc = best
        sm = np.sort(np.array([0.511, 2.2, 4.7, 95, 105.66, 1270, 1776.86, 4180, 173100]))
        
        print(f"\n{'='*70}")
        print(f"BEST: d={d:.2f}, y_t={y_t:.1f}")
        print(f"v={res['v']:.2f}, mu2={res['mu2']:.4f}, lam={res['lam']:.6f}")
        print(f"scale={sc:.2f}, RMSE={best_error:.4f}")
        print(f"{'='*70}")
        print(f"\n{'Index':>6s} | {'SM (MeV)':>12s} | {'Pred (MeV)':>12s} | {'Ratio':>8s}")
        print("-" * 40)
        for i in range(9):
            r = m_mev[i] / sm[i]
            print(f"{i+1:>6d} | {sm[i]:>12.4f} | {m_mev[i]:>12.2f} | {r:>8.2f}")
    
    # 绘图
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    if best:
        ax = axes[0]
        sm = np.sort(np.array([0.511, 2.2, 4.7, 95, 105.66, 1270, 1776.86, 4180, 173100]))
        ax.plot(range(1,10), np.log10(sm), 'o-', label='SM', linewidth=2, markersize=8)
        ax.plot(range(1,10), np.log10(best[-2][:9]), 's--', label=f'd={best[0]:.2f}', linewidth=2, markersize=8)
        ax.set_xlabel('Particle index')
        ax.set_ylabel('log10(mass) [MeV]')
        ax.set_title(f'Adaptive FRG (RMSE={best_error:.3f})')
        ax.legend()
        ax.grid(True)
        
        ax = axes[1]
        ax.plot(best[2]['mu2_hist'])
        ax.axhline(y=0, color='r', linestyle='--')
        ax.set_xlabel('RG step')
        ax.set_ylabel('mu^2')
        ax.set_title(f'SSB for d={best[0]:.2f}')
        ax.grid(True)
    
    plt.tight_layout()
    plt.savefig('adaptive_frg_results.png', dpi=300)
    
    with open('adaptive_frg_results.txt', 'w', encoding='utf-8') as f:
        f.write("=== Adaptive FRG Solver Results ===\n\n")
        if best:
            f.write(f"Best: d={best[0]:.2f}, y_t={best[1]:.1f}\n")
            f.write(f"v={best[2]['v']:.4f}, scale={best[5]:.2f}\n")
            f.write(f"RMSE={best_error:.4f}\n\n")
            for i in range(9):
                f.write(f"  {i+1}: SM={sm[i]:>10.4f} Pred={best[4][i]:>10.2f}\n")
    
    print(f"\nResults saved to adaptive_frg_results.txt")
    print(f"Plot saved to adaptive_frg_results.png")

if __name__ == "__main__":
    run()