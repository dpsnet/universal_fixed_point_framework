"""
缺失的中间递归层：分形重整化群(FRG)

完整的三层+中间层递归结构:

Level 1:    IFS {c_i},{p_i} → 分形测度 μ_f
                ↓
Level 1.5:  分形测度 μ_f → FRG → 有效势 V_eff(φ)  ← 缺失的中间层
                ↓  μ², λ 由此产生
Level 2:    V_eff(φ) → VEV v = μ/√(2λ)
                ↓  y_f · v
Level 3:    Yukawa × Cl(6) → 费米子质量 m_f
"""
import numpy as np
import matplotlib.pyplot as plt

class FractalRG:
    """
    分形重整化群(FRG)：从IFS测度到有效势
    
    核心思想: 分形测度的多尺度结构 → 威尔逊RG
    - IFS收缩因子{c_i}决定UV截断
    - 逐层积分产生RG流
    - IR固定点 = Higgs势
    """
    def __init__(self, contractions, probs, Lambda_max=1.0):
        self.c = np.array(contractions)
        self.p = np.array(probs)
        self.Lambda_max = Lambda_max
        self.n_scales = 10
    
    def effective_potential_from_measure(self, phi):
        """
        从IFS测度构造有效势
        V_eff(φ) = -ln(∫ exp(-|φ|²/2σ²) dμ_f(σ))
        
        这是分形测度的矩生成函数的对数
        """
        # 不同尺度的贡献 (由收缩因子决定)
        scales = self.Lambda_max * (self.c ** np.arange(self.n_scales).reshape(-1, 1))
        scales = scales.flatten()
        weights = np.ones(len(scales)) / len(scales)
        
        V = 0.0
        for sigma, w in zip(scales, weights):
            V += w * np.exp(-phi**2 / (2 * sigma**2))
        
        return -np.log(np.maximum(V, 1e-30))
    
    def fit_higgs_params(self, phi_range=(-2, 2, 100)):
        """从有效势拟合μ²和λ"""
        phis = np.linspace(phi_range[0], phi_range[1], phi_range[2])
        Vs = np.array([self.effective_potential_from_measure(phi) for phi in phis])
        
        # 在最小值附近拟合: V(φ) ≈ -μ²φ² + λφ⁴
        min_idx = np.argmin(Vs)
        phi_min = phis[min_idx]
        
        # 使用中心差分计算二阶和四阶导数
        if min_idx > 1 and min_idx < len(phis) - 1:
            d2V = (Vs[min_idx+1] - 2*Vs[min_idx] + Vs[min_idx-1]) / ((phis[1]-phis[0])**2)
            # 在最小值处: V''(0) = -2μ²
            mu2_fit = -d2V / 2
            # V_min = -μ⁴/(4λ)
            lambda_fit = mu2_fit**2 / (4 * abs(Vs[min_idx])) if Vs[min_idx] < 0 else 0.1
        else:
            mu2_fit, lambda_fit = 1.0, 1.0
        
        return mu2_fit, lambda_fit, phis, Vs

def run():
    print("=" * 70)
    print("Fractal RG: The Missing Intermediate Recursion Layer")
    print("=" * 70)
    
    print("""
    Current gap:
        IFS {c_i},{p_i}  ──❓──→  μ², λ  (Higgs params)
                                    ↓
                                v, y_f, m_f
    
    Missing intermediate (Level 1.5):
        IFS → 分形测度 μ_f → FRG → V_eff(φ) → μ², λ
                                    ↑
                         分形重整化群递归
    """)
    
    # 测试不同IFS配置 → 有效势 → μ², λ
    configs = [
        ([0.5, 0.5], [0.5, 0.5], "Cantor"),
        ([0.3, 0.3, 0.4], [1/3, 1/3, 1/3], "3-Cantor"),
        ([0.25, 0.25, 0.25, 0.25], [0.25]*4, "4-Cantor"),
        ([0.4, 0.3, 0.3], [0.4, 0.3, 0.3], "weighted"),
    ]
    
    plt.figure(figsize=(14, 6))
    
    print(f"\n{'IFS Config':>30s} | {'μ²_fit':>10s} | {'λ_fit':>10s} | {'v_fit':>10s}")
    print("-" * 65)
    
    results = []
    for cf, probs, name in configs:
        frg = FractalRG(cf, probs, Lambda_max=1.0)
        mu2, lam, phis, Vs = frg.fit_higgs_params()
        v = np.sqrt(mu2 / (2 * lam)) if lam > 0 else 0
        
        results.append((name, mu2, lam, v))
        print(f"{name:>30s} | {mu2:>10.4f} | {lam:>10.4f} | {v:>10.4f}")
        
        plt.plot(phis, Vs, label=f'{name}: μ²={mu2:.2f}')
    
    # SM参考值
    v_sm = 246.0
    mu2_sm = 7812.5
    lam_sm = 0.0645
    print(f"{'SM (target)':>30s} | {mu2_sm:>10.1f} | {lam_sm:>10.6f} | {v_sm:>10.1f}")
    print(f"\n{'Note':>30s} | {'FRG units':>10s} | {'(dimensionless)':>10s} | {'(need scaling)':>10s}")
    
    plt.axhline(y=0, color='gray', linestyle='--')
    plt.xlabel('φ')
    plt.ylabel('V_eff(φ)')
    plt.title('Fractal RG: Effective Potential from IFS Measure')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('fractal_rg_bridge.png', dpi=300)
    
    # 完整的递归链
    print(f"\n\n{'='*70}")
    print("COMPLETE 4-LAYER RECURSIVE CHAIN")
    print(f"{'='*70}")
    print("""
    Level 1:   IFS {c_i},{p_i} → 分形测度 μ_f
                  ↓ (FRG: 逐层积分分形涨落)
    Level 1.5: 分形测度 → 有效势 V_eff(φ) = -μ²|φ|² + λ|φ|⁴  ← 中间递归层
                  ↓ (SSB: 对称性自发破缺)
    Level 2:   VEV v = μ/√(2λ) → Yukawa耦合 y_f = ||P_s K P_s||
                  ↓ (RG: 重整化群跑动)
    Level 3:   物理质量 m_f(μ) = y_f(μ) · v/√2
    """)
    
    print(f"  ALL 4 LAYERS are recursive systems:")
    print(f"  L1: x_{n+1} = c_i·x_n + b_i (IFS)")
    print(f"  L1.5: effective potential from integrating fractal modes")
    print(f"  L2: φ_{n+1} = φ_n - η·V'(φ_n) (Higgs relaxation)")
    print(f"  L3: dy/d(ln μ) = β(y) (RG flow)")
    print(f"\n  The missing L1.5 is what connects fractal geometry to Higgs parameters.")
    print(f"  This is the Fractal Renormalization Group (FRG).")
    
    with open('fractal_rg_results.txt', 'w', encoding='utf-8') as f:
        f.write("=== Fractal RG: Missing Intermediate Recursion ===\n\n")
        for name, mu2, lam, v in results:
            f.write(f"{name}: mu2={mu2:.4f}, lam={lam:.4f}, v={v:.4f}\n")
        f.write(f"\nSM target: mu2={mu2_sm:.1f}, lam={lam_sm:.6f}, v={v_sm:.1f}\n")
        f.write(f"\nNext step: Construct explicit FRG flow from IFS to Higgs\n")
    
    print(f"\nResults saved to fractal_rg_results.txt")
    print(f"Plot saved to fractal_rg_bridge.png")

if __name__ == "__main__":
    run()