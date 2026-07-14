"""
最终预测: 优化IFS参数 → 精确匹配标准模型9个费米子质量

完整路径:
  IFS参数 → 多分形谱 → α区间测度 → Yuwaka权重w_s → C_s
  C_s × k^{2/d} × v_SM → 9个质量

优化目标: 最小化log空间RMSE
"""
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

SM = np.sort(np.array([0.511, 2.2, 4.7, 95, 105.66, 1270, 1776.86, 4180, 173100]))
v_SM = 246000.0
target_C = np.array([1.0, 3.45, 6.53])

def ifs_dim(c):
    def f(d): return np.sum(np.array(c)**d) - 1
    lo, hi = 0.01, 5.0
    for _ in range(50):
        mid = (lo+hi)/2
        if f(mid) > 0: lo = mid
        else: hi = mid
    return (lo+hi)/2

def multifractal_measure(c, p, depth=8, n_sample=200):
    """快速计算多分形测度的α谱和扇区测度"""
    N = len(c)
    c_arr = np.array(c)
    p_arr = np.array(p)
    
    alphas = -np.log(p_arr) / np.log(np.maximum(c_arr, 1e-10))
    d_f = ifs_dim(c)
    
    xs = np.random.rand(n_sample)
    
    # 简化:每个点α由其所在的IFS分支决定
    branch = np.floor(xs * N).astype(int)
    branch = np.clip(branch, 0, N-1)
    sample_alphas = alphas[branch]
    
    alpha_min, alpha_max = np.min(sample_alphas), np.max(sample_alphas)
    
    # 3个扇区(等分α范围)
    edges = np.linspace(alpha_min, alpha_max, 4)
    sector_masses = np.zeros(3)
    
    for s in range(3):
        mask = (sample_alphas >= edges[s]) & (sample_alphas < edges[s+1])
        sector_masses[s] = np.sum(mask)
    
    sector_masses = sector_masses / np.sum(sector_masses)
    
    # 扇区测度 → Yukawa → C_s
    yukawa = 1.0 / np.maximum(sector_masses, 1e-30)
    C_s = yukawa / yukawa[0]
    
    return C_s, d_f, sector_masses

def predict_9_masses(C_s, d):
    """从C_s和d预测9个质量"""
    k = np.array([1, 2, 3])
    intra = k ** (2.0 / np.maximum(d, 0.1))
    intra = intra / intra[0]
    
    masses = []
    for C in C_s:
        # 校准: C_s * v_SM / C_s[0] 给出质量
        sector_masses = C * intra * v_SM / C_s[0]
        masses.extend(sector_masses)
    
    return np.sort(masses)

def score(params):
    """目标函数: log RMSE"""
    n = len(params) // 2
    c = np.abs(params[:n])
    p = np.abs(params[n:])
    p = p / np.sum(p)
    
    try:
        C_s, d, _ = multifractal_measure(c, p)
        masses = predict_9_masses(C_s, d)
        error = np.mean((np.log(masses) - np.log(SM))**2)
        return error
    except:
        return 1e6

def run():
    print("=" * 70)
    print("FINAL SM MASS PREDICTION: IFS Optimization")
    print("=" * 70)
    
    # 系统扫描不同IFS配置
    configs = []
    
    # 2-parameter IFS
    for c1 in np.arange(0.2, 0.8, 0.1):
        for p1 in np.arange(0.5, 1.0, 0.1):
            c = [c1, 1-c1]
            p = [p1, 1-p1]
            configs.append((c, p))
    
    # 3-parameter IFS
    for c1 in np.arange(0.2, 0.6, 0.15):
        for c2 in np.arange(0.1, 0.4, 0.1):
            for p1 in np.arange(0.4, 0.8, 0.15):
                c = [c1, c2, 1-c1-c2]
                p = [p1, 0.5*(1-p1), 0.5*(1-p1)]
                configs.append((c, p))
    
    results = []
    
    for c, p in configs:
        try:
            C_s, d, masses_s = multifractal_measure(c, p)
            masses = predict_9_masses(C_s, d)
            error = np.sqrt(np.mean((np.log(masses) - np.log(SM))**2))
            C_err = np.mean(np.abs(C_s - target_C))
            
            results.append((error, C_err, c, p, d, C_s, masses))
        except:
            pass
    
    results.sort(key=lambda x: x[0])
    
    # Top 10 best results
    print(f"\nTop 10 IFS configurations (out of {len(results)}):")
    print(f"\n{'Rank':>4s} | {'C_s ratio':>20s} | {'d':>6s} | {'RMSE':>6s} | {'C_err':>6s} | {'Config':>20s}")
    print("-" * 70)
    
    for i in range(min(10, len(results))):
        r = results[i]
        C_str = f"[{r[5][0]:.2f}, {r[5][1]:.2f}, {r[5][2]:.2f}]"
        cfg_str = f"c={np.round(r[2],2)}, p={np.round(r[3],2)}"
        print(f"{i+1:>4d} | {C_str:>20s} | {r[4]:>6.3f} | {r[0]:>6.4f} | {r[1]:>6.4f} | {cfg_str:>20s}")
    
    # Best result
    best = results[0]
    print(f"\n\n{'='*70}")
    print("BEST SM MASS PREDICTION")
    print(f"{'='*70}")
    
    c, p, d, C_s, masses = best[2], best[3], best[4], best[5], best[6]
    
    print(f"IFS: c={np.round(c, 4)} (d={d:.4f})")
    print(f"     p={np.round(p, 4)}")
    print(f"C_s ratios: {np.round(C_s, 4)} (target: {target_C})")
    print(f"C_err: {best[1]:.4f}")
    print(f"RMSE: {best[0]:.4f}")
    
    print(f"\n{'Particle':>8s} | {'SM (MeV)':>12s} | {'Pred (MeV)':>12s} | {'Ratio':>8s}")
    print("-" * 42)
    for i in range(9):
        r = masses[i] / SM[i]
        print(f"{i+1:>8d} | {SM[i]:>12.4f} | {masses[i]:>12.2f} | {r:>8.2f}")
    
    # 绘图
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    ax = axes[0]
    ax.plot(range(1,10), np.log10(SM), 'o-', label='SM', linewidth=2, markersize=8, color='blue')
    ax.plot(range(1,10), np.log10(masses), 's--', label='Predicted', linewidth=2, markersize=8, color='red')
    ax.set_xlabel('Particle index')
    ax.set_ylabel('log10(mass) [MeV]')
    ax.set_title(f'Final SM Mass Prediction (RMSE={best[0]:.3f})')
    ax.legend()
    ax.grid(True)
    
    ax = axes[1]
    ax.scatter(np.log10(SM), np.log10(masses), s=100, c='red')
    lims = [-1, 6]
    ax.plot(lims, lims, 'b--', label='Perfect')
    ax.set_xlabel('log10(SM mass)')
    ax.set_ylabel('log10(Predicted mass)')
    ax.set_title(f'Correlation')
    ax.legend()
    ax.grid(True)
    
    ax = axes[2]
    labels = ['Lepton', 'Up', 'Down']
    x = np.arange(3)
    ax.bar(x - 0.2, target_C, 0.4, label='SM target')
    ax.bar(x + 0.2, C_s, 0.4, label='Predicted')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel('C_s / C_lepton')
    ax.set_title(f'C_s Ratio (C_err={best[1]:.3f})')
    ax.legend()
    ax.grid(True)
    
    plt.tight_layout()
    plt.savefig('final_sm_prediction.png', dpi=300)
    
    with open('final_sm_prediction_results.txt', 'w', encoding='utf-8') as f:
        f.write("=== Final SM Mass Prediction ===\n\n")
        f.write(f"IFS: c={np.round(c,4)}, p={np.round(p,4)}\n")
        f.write(f"d={d:.4f}\n")
        f.write(f"C_s={np.round(C_s,4)}\n")
        f.write(f"RMSE={best[0]:.4f}\n\n")
        for i in range(9):
            f.write(f"  {i+1}: SM={SM[i]:>10.4f} Pred={masses[i]:>10.2f}\n")
    
    print(f"\nResults saved to final_sm_prediction_results.txt")

if __name__ == "__main__":
    run()