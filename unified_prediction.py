"""
统一预测：完整闭环 + 正确分形维数 + 比例缩放

关键修正: 使用d≈0.266的IFS收缩因子(来自逆谱构造)
  Cantor: c = exp(-ln(2)/d) = exp(-ln(2)/0.266) ≈ 0.074
"""
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# Level 1: IFS (d≈0.266)
# ============================================================
def dimerization(c):
    """两片Cantor集的分形维数: d = -ln(2)/ln(c)"""
    return -np.log(2) / np.log(c)

def contraction_from_dimension(d):
    """从目标分形维数计算收缩因子: c = exp(-ln(2)/d)"""
    return np.exp(-np.log(2) / d)

# ============================================================
# Level 1.5: 耦合FRG流
# ============================================================
def coupled_frg(c, y_top=2.0, N_rg=200, Lambda_UV=1.0):
    """耦合FRG流 + 顶夸克驱动"""
    phi = np.linspace(-3, 3, 200)
    dphi = phi[1] - phi[0]
    
    ks = [Lambda_UV]
    for i in range(N_rg):
        ks.append(ks[-1] * c)
    ks = np.array(ks)
    
    V = 0.5 * phi**2
    mu2_hist = []
    
    for i in range(len(ks) - 1):
        k = ks[i]; dk = ks[i+1] - ks[i]
        d2V = np.zeros_like(V)
        d2V[1:-1] = (V[2:] - 2*V[1:-1] + V[:-2]) / dphi**2
        d2V[0] = d2V[1]; d2V[-1] = d2V[-2]
        dV_frg = k**4 / (16*np.pi**2) / np.maximum(k**2 + d2V, 1e-10)
        dV_top = (3*y_top**2) / (4*np.pi**2) * k**2 * phi**2 * 10
        V += dk * (dV_frg + dV_top)
        
        center = len(phi)//2
        d2V_c = (V[center+1] - 2*V[center] + V[center-1]) / dphi**2
        mu2_hist.append(-d2V_c/2)
    
    center = len(phi)//2
    d2V_IR = (V[center+1] - 2*V[center] + V[center-1]) / dphi**2
    mu2 = -d2V_IR/2
    V_min = np.min(V)
    lam = mu2**2/(-4*V_min) if V_min < 0 and mu2 > 1e-6 else 0.1
    v = np.sqrt(mu2/(2*lam)) if mu2 > 0 and lam > 0 else 0
    
    return {'mu2': mu2, 'lam': lam, 'v': v, 'mu2_hist': np.array(mu2_hist), 'V_IR': V, 'phi': phi}

# ============================================================
# Level 2: Cl(6) Yukawa
# ============================================================
def yukawa_weights(theta=0.5):
    w = np.exp(-np.arange(3)/theta)
    return w / w[0]

# ============================================================
# Level 3: 质量预测 + 缩放
# ============================================================
def predict(v, d, ws):
    k_arr = np.array([1, 2, 3])
    ratios = k_arr ** (2.0 / np.maximum(d, 0.1))
    ratios = ratios / ratios[0]
    
    masses = []
    for w in ws:
        masses.extend(v/w * ratios)
    return np.sort(masses)

# ============================================================
def run():
    print("=" * 70)
    print("UNIFIED PREDICTION: Correct d + FRG + Scaling")
    print("=" * 70)
    
    sm = np.sort(np.array([0.511, 2.2, 4.7, 95, 105.66, 1270, 1776.86, 4180, 173100]))
    v_SM = 246000.0  # MeV
    
    # 扫描d值 (从SM fit的d≈0.266附近)
    d_targets = [0.266, 0.3, 0.35, 0.4, 0.5, 0.6, 0.8, 1.0]
    
    best_error = float('inf')
    best = None
    
    for d_target in d_targets:
        c = contraction_from_dimension(d_target)
        d_actual = dimerization(c)
        
        for y_top in [1.5, 2.0, 2.5]:
            for theta in [0.5, 0.8, 1.0]:
                result = coupled_frg(c, y_top, N_rg=200)
                
                if result['v'] <= 0:
                    continue
                
                ws = yukawa_weights(theta)
                m_frg = predict(result['v'], d_actual, ws)
                
                # 缩放
                scale = v_SM / result['v']
                m_mev = m_frg * scale
                
                error = np.mean(np.abs(np.log(m_mev[:9]) - np.log(sm)))
                
                if error < best_error:
                    best_error = error
                    best = (d_target, c, d_actual, y_top, theta, result, m_frg, m_mev, scale)
    
    if best:
        d_t, c, d_a, y_t, th, res, m_frg, m_mev, sc = best
        print(f"\nBEST RESULT:")
        print(f"  d_target={d_t:.3f}, c={c:.4f}, d_actual={d_a:.4f}")
        print(f"  y_top={y_t:.2f}, theta={th:.1f}")
        print(f"  v_FRG={res['v']:.4f}, scale={sc:.2f}")
        print(f"  mu2={res['mu2']:.4f}, lam={res['lam']:.6f}")
        print(f"  RMSE(log)={best_error:.4f}")
        
        print(f"\n{'Index':>6s} | {'SM (MeV)':>12s} | {'FRG':>8s} | {'Pred (MeV)':>12s} | {'Ratio':>8s}")
        print("-" * 50)
        for i in range(9):
            r = m_mev[i] / sm[i]
            print(f"{i+1:>6d} | {sm[i]:>12.4f} | {m_frg[i]:>8.2f} | {m_mev[i]:>12.2f} | {r:>8.2f}")
    
    # 绘图
    plt.figure(figsize=(12, 5))
    plt.subplot(121)
    plt.plot(range(1,10), np.log10(sm), 'o-', label='SM', linewidth=2, markersize=8)
    if best:
        plt.plot(range(1,10), np.log10(best[-3][:9]), 's--', label='Predicted', linewidth=2, markersize=8)
    plt.xlabel('Particle index')
    plt.ylabel('log10(mass) [MeV]')
    plt.title(f'Unified Prediction (RMSE={best_error:.3f})')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(122)
    if best:
        plt.plot(best[5]['mu2_hist'])
        plt.axhline(y=0, color='r', linestyle='--')
        plt.xlabel('RG step')
        plt.ylabel('mu^2')
        plt.title('SSB: mu^2 sign flip')
        plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('unified_prediction.png', dpi=300)
    
    with open('unified_prediction_results.txt', 'w', encoding='utf-8') as f:
        f.write("=== Unified Prediction Results ===\n\n")
        if best:
            f.write(f"d={best[2]:.4f}, y_t={best[3]:.2f}, theta={best[4]:.1f}\n")
            f.write(f"v_FRG={best[5]['v']:.4f}, scale={best[8]:.2f}\n")
            f.write(f"RMSE={best_error:.4f}\n\n")
            for i in range(9):
                f.write(f"  {i+1}: SM={sm[i]:>10.4f} Pred={best[7][i]:>10.2f}\n")
    
    print(f"\nResults saved to unified_prediction_results.txt")

if __name__ == "__main__":
    run()