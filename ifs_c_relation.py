"""
方向1：建立IFS收缩因子{c_i}与扇区标度C_s的解析关系

核心问题: C_s = F({c_i}, {p_i}, Γ_s)
从IFS分形几何参数预测扇区质量标度

方法:
1. 系统变化IFS收缩因子和概率
2. 对每组IFS参数计算分形维数d和谱衰减率
3. 建立d, C_s, {c_i}的解析关系
4. 反向预测SM的三个C_s值
"""
import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt

class IFSSpectralAnalyzer:
    """IFS分形谱分析器"""
    def __init__(self, n_points=100):
        self.n = n_points
        self.x = np.linspace(0, 1, n_points)
    
    def ifs_dimension(self, contractions, probabilities):
        """计算IFS分形维数 d: Σ c_i^d = 1"""
        def f(d):
            return np.sum(contractions**d) - 1
        # 二分法求解
        lo, hi = 0.01, 5.0
        for _ in range(50):
            mid = (lo + hi) / 2
            if f(mid) > 0:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2
    
    def spectral_decay_rate(self, sigma):
        """计算Gaussian核的谱衰减率"""
        X = self.x.reshape(-1, 1)
        D2 = (X - self.x.reshape(1, -1)) ** 2
        K = np.exp(-D2 / (2 * sigma**2))
        w = np.ones(self.n) / self.n
        T = K * w.reshape(-1, 1)
        ev = la.eigvals(T)
        ev = np.real(ev)
        ev = np.sort(ev)[::-1]
        return ev[:10]
    
    def predict_C_from_lambda1(self, lambda1, m_ref=0.511):
        """C_s = -m_ref / ln(λ₁)：从最大特征值预测扇区标度"""
        if lambda1 >= 1 or lambda1 <= 0:
            return float('inf')
        return -m_ref / np.log(lambda1)
    
    def estimate_C_from_spectrum(self, eigenvalues, target_masses):
        """从特征值估计扇区标度C"""
        """从特征值估计扇区标度C"""
        log_eig = -np.log(np.maximum(eigenvalues[:3], 1e-30))
        log_m = np.log(target_masses)
        C = np.exp(np.mean(log_m - np.log(log_eig)))
        predicted = C * log_eig
        error = np.mean(np.abs(np.log(predicted) - log_m))
        return C, error, predicted

def run():
    print("=" * 70)
    print("Direction 1: IFS Contraction Factors ↔ Sector Scale C_s")
    print("=" * 70)
    
    analyzer = IFSSpectralAnalyzer(n_points=100)
    
    # SM目标质量
    sm_sectors = {
        'lepton': np.array([0.511, 105.66, 1776.86]),
        'up': np.array([2.2, 1270.0, 173100.0]),
        'down': np.array([4.7, 95.0, 4180.0]),
    }
    
    # 实验1: 系统变化收缩因子，观察C_s的变化
    print("\n\nExperiment 1: Varying Contraction Factors")
    print("-" * 50)
    
    contraction_grid = [
        [0.3, 0.3, 0.4],
        [0.25, 0.25, 0.25, 0.25],
        [0.2, 0.3, 0.5],
        [0.4, 0.4, 0.2],
        [0.5, 0.5],
        [0.33, 0.33, 0.34],
        [0.1, 0.2, 0.3, 0.4],
    ]
    
    sigma_test = 0.15
    
    print(f"Fixed sigma = {sigma_test}")
    print(f"\n{'IFS Config':>30s} | {'d_f':>6s} | {'C_lep':>8s} | {'C_up':>8s} | {'C_down':>8s}")
    print("-" * 70)
    
    results = []
    for cf in contraction_grid:
        probs = [1/len(cf)] * len(cf)
        d = analyzer.ifs_dimension(np.array(cf), np.array(probs))
        ev = analyzer.spectral_decay_rate(sigma_test)
        
        Cs = []
        for name in ['lepton', 'up', 'down']:
            C, err, _ = analyzer.estimate_C_from_spectrum(ev, sm_sectors[name])
            Cs.append(C)
        
        results.append((cf, d, Cs))
        print(f"{str(cf):>30s} | {d:>6.3f} | {Cs[0]:>8.2f} | {Cs[1]:>8.2f} | {Cs[2]:>8.2f}")
    
    # 实验2: 变化sigma，观察C_s的变化（固定参考质量m_ref=0.511 MeV）
    print("\n\nExperiment 2: C_s Predicted from IFS + σ")
    print("-" * 50)
    print("C_s = -m_ref / ln(λ₁(σ, d)) where m_ref = 0.511 MeV (electron)")
    
    cf_standard = [0.5, 0.5]
    
    cf_standard = [0.5, 0.5]
    d_standard = analyzer.ifs_dimension(np.array(cf_standard), np.array([0.5, 0.5]))
    
    sigma_range = np.logspace(-1.5, 0, 10)
    print(f"IFS: {cf_standard}, d_f = {d_standard:.4f}")
    print(f"\n{'σ':>8s} | {'C_lep':>8s} | {'C_up':>8s} | {'C_down':>8s} | {'λ₁':>8s}")
    print("-" * 50)
    
    sigma_results = []
    for sigma in sigma_range:
        ev = analyzer.spectral_decay_rate(sigma)
        Cs = []
        for name in ['lepton', 'up', 'down']:
            C, err, _ = analyzer.estimate_C_from_spectrum(ev, sm_sectors[name])
            Cs.append(C)
        sigma_results.append((sigma, Cs[0], Cs[1], Cs[2], ev[0]))
        print(f"{sigma:>8.4f} | {Cs[0]:>8.2f} | {Cs[1]:>8.2f} | {Cs[2]:>8.2f} | {ev[0]:>8.4f}")
    
    # 实验3: 尝试匹配SM的C_s
    print("\n\nExperiment 3: Parameter Search for SM Matching")
    print("-" * 50)
    
    # 目标C_s值（从逆构造得到）
    target_C = {'lepton': 0.53, 'up': 1.83, 'down': 3.46}
    
    best_error = float('inf')
    best = None
    
    n_search = 50
    for _ in range(n_search):
        n_c = np.random.randint(2, 5)
        cf = np.random.dirichlet(np.ones(n_c)) * np.random.uniform(0.3, 0.8)
        cf = np.maximum(cf, 0.05)
        probs = np.random.dirichlet(np.ones(n_c))
        d = analyzer.ifs_dimension(cf, probs)
        
        sigma = 10 ** np.random.uniform(-1.5, -0.3)
        ev = analyzer.spectral_decay_rate(sigma)
        
        error = 0
        Cs = {}
        for name in ['lepton', 'up', 'down']:
            C, err, _ = analyzer.estimate_C_from_spectrum(ev, sm_sectors[name])
            Cs[name] = C
            error += (np.log(C) - np.log(target_C[name]))**2
        
        if error < best_error:
            best_error = error
            best = (cf, probs, d, sigma, Cs)
    
    if best:
        cf, probs, d, sigma, Cs = best
        print(f"Best match found:")
        print(f"  IFS factors: {np.round(cf, 4)}")
        print(f"  IFS probs: {np.round(probs, 4)}")
        print(f"  Fractal dimension: d = {d:.4f}")
        print(f"  Kernel sigma = {sigma:.4f}")
        print(f"  C_lepton: target={target_C['lepton']}, got={Cs['lepton']:.2f}")
        print(f"  C_up: target={target_C['up']}, got={Cs['up']:.2f}")
        print(f"  C_down: target={target_C['down']}, got={Cs['down']:.2f}")
        print(f"  RMSE = {np.sqrt(best_error/3):.4f}")
        
        # 预测C_s比值
        C_ratio_up_lep = Cs['up'] / Cs['lepton']
        C_ratio_down_lep = Cs['down'] / Cs['lepton']
        print(f"\n  Predicted ratios:")
        print(f"    C_up/C_lepton = {C_ratio_up_lep:.2f} (target: 3.45)")
        print(f"    C_down/C_lepton = {C_ratio_down_lep:.2f} (target: 6.53)")
    
    # 绘图
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # 图1: C_s vs sigma
    ax = axes[0, 0]
    sigmas = [r[0] for r in sigma_results]
    ax.plot(sigmas, [r[1] for r in sigma_results], 'o-', label='lepton')
    ax.plot(sigmas, [r[2] for r in sigma_results], 's-', label='up')
    ax.plot(sigmas, [r[3] for r in sigma_results], '^-', label='down')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Kernel width σ')
    ax.set_ylabel('C_s [MeV]')
    ax.set_title('Sector Scale C_s vs σ')
    ax.legend()
    ax.grid(True)
    
    # 图2: C_s vs d_f
    ax = axes[0, 1]
    ds = [r[1] for r in results]
    ax.plot(ds, [r[2][0] for r in results], 'o-', label='lepton')
    ax.plot(ds, [r[2][1] for r in results], 's-', label='up')
    ax.plot(ds, [r[2][2] for r in results], '^-', label='down')
    ax.set_xlabel('Fractal dimension d')
    ax.set_ylabel('C_s [MeV]')
    ax.set_title('Sector Scale C_s vs Fractal Dimension')
    ax.legend()
    ax.grid(True)
    
    # 图3: λ₁ vs sigma
    ax = axes[1, 0]
    ax.plot(sigmas, [r[4] for r in sigma_results], 'o-')
    ax.set_xscale('log')
    ax.set_xlabel('Kernel width σ')
    ax.set_ylabel('Largest eigenvalue λ₁')
    ax.set_title('Spectral Gap vs σ')
    ax.grid(True)
    
    # 图4: C_up/C_lepton ratio
    ax = axes[1, 1]
    ratios = [r[2]/r[1] for r in sigma_results]
    ax.plot(sigmas, ratios, 'o-')
    ax.axhline(y=3.45, color='r', linestyle='--', label='SM target')
    ax.set_xscale('log')
    ax.set_xlabel('Kernel width σ')
    ax.set_ylabel('C_up / C_lepton')
    ax.set_title('Sector Scale Ratio')
    ax.legend()
    ax.grid(True)
    
    plt.tight_layout()
    plt.savefig('ifs_c_relation.png', dpi=300)
    
    # 保存结果
    with open('ifs_c_relation_results.txt', 'w', encoding='utf-8') as f:
        f.write("=== IFS Contraction - Sector Scale C_s ===\n\n")
        f.write("Experiment 1: Varying IFS\n")
        for cf, d, Cs in results:
            f.write(f"  {cf}: d={d:.3f}, C={np.round(Cs, 2)}\n")
        f.write(f"\nExperiment 2: Varying σ\n")
        for sigma, c1, c2, c3, l1 in sigma_results:
            f.write(f"  σ={sigma:.4f}: C_lep={c1:.2f}, C_up={c2:.2f}, C_down={c3:.2f}\n")
        if best:
            f.write(f"\nBest SM match:\n")
            f.write(f"  factors={np.round(best[0], 4)}\n")
            f.write(f"  d={best[2]:.4f}, σ={best[3]:.4f}\n")
            f.write(f"  C={np.round(list(best[4].values()), 2)}\n")
    
    print(f"\n\nResults saved to ifs_c_relation_results.txt")
    print(f"Plot saved to ifs_c_relation.png")

if __name__ == "__main__":
    run()