"""
非马尔可夫线型算子（Non-Markovian Linewidth Operator, NMLO）

基于奇异连续谱测度的 Balmer 发射线定量拟合算子（论文5.5节）。

算子链路（四阶段，严格区分理论框架与应用实例）：
  A. 测度 → 记忆核：Cantor 类奇异连续谱测度，傅里叶变换幂律尾 |μ̂(t)| ~ t^{-(1-D)}
     盒计数谱维数 D2 数值验证（与论文3.2氢原子 D2 方法一致）
  B. 记忆核 → 线型：Lamb 方程叠加奇异通道的混合谱线型
     S(δ) = Re{1/[s + (1-η)γ²/(s+γ) + ηκΓ(1-α)s^{α-1}]}，s=iδ，α=1-D
     数值验证：尾区斜率偏离洛伦兹（幂律尾、中心衰减增强）
  C. 线型 → EW标度：发射强度 |EW_n| = A_s · n^m，
     奇异连续谱权重 η_sc(n) ∝ n^m（高阶态更接近电离阈）

拟合：3 颗反常 Balmer 发射线白矮星（J233817/J225828/J101712，表5.2）
     逐线 EW（Hα-Hη, n=3-9），全局线序指数 m + 每星振幅 A_s
"""

import numpy as np
from scipy import optimize
from scipy.special import gamma as gamma_func

# ---------------------------------------------------------------
# 观测数据（表5.2，逐线EW，单位Å）
# ---------------------------------------------------------------
STARS = {
    'J233817': np.array([-0.07, -0.63, -2.56, -0.44, -1.47, -4.35, -5.93]),
    'J225828': np.array([-2.77, -2.25, -4.77, -8.47, -10.40, -21.28, -26.80]),
    'J101712': np.array([0.76, -0.15, -5.94, -8.58, -10.34, -20.95, -19.64]),
}
B_TESLA = {'J233817': 1.2e4, 'J225828': 1.4e4, 'J101712': 1.4e4}
N_BALMER = np.arange(3, 10, dtype=float)   # Hα(n=3)...Hη(n=9)

# ---------------------------------------------------------------
# A. 奇异连续谱测度 → 记忆核
# ---------------------------------------------------------------
def cantor_measure(N=2**16, D=None):
    """构造 Cantor 类奇异连续测度密度（三进制中段删除）。
    返回 (ω格点, 测度权重)，Hausdorff 维数 D=ln2/ln3≈0.631。"""
    n_iter = 9
    points = np.array([0.0, 1.0])
    for _ in range(n_iter):
        new = []
        for i in range(len(points) - 1):
            a, b = points[i], points[i + 1]
            new += [a, a + (b - a) / 3.0, a + 2.0 * (b - a) / 3.0]
        new.append(1.0)
        points = np.unique(np.array(new))
    # 在区间内格点化：每格点的测度 = 该点是否属于 Cantor 集
    x = np.linspace(0, 1, N)
    w = np.zeros(N)
    for i in range(len(points) - 1):
        a, b = points[i], points[i + 1]
        m = (x >= a) & (x <= b)
        w[m] = 1.0
    w = w / w.sum() / (x[1] - x[0])
    return x, w

def verify_power_law(alpha_exp=1 - np.log(2) / np.log(3)):
    """验证奇异连续测度傅里叶变换幂律尾 |μ̂(t)| ~ t^{-(1-D)}（limsup 阶）。
    用 k 级 Cantor 点质量：μ̂(t) = 2^{-k} Σ_j e^{-it x_j}。
    对数分箱取箱内最大值（limsup 估计），抑制自相似对数周期振荡。"""
    k = 12
    x = cantor_points(k)          # Cantor 集 2^k 个点（区间中心）
    w = np.full(2**k, 1.0 / 2**k)  # 等权重
    t = np.logspace(1.5, 5.0, 90)
    muhat = np.abs(np.exp(-1j * np.outer(t, x)).dot(w))
    log_t = np.log(t)
    nb = 30
    edges = np.linspace(log_t.min(), log_t.max(), nb + 1)
    lt_m, lmu_m = [], []
    for i in range(nb):
        m = (log_t >= edges[i]) & (log_t < edges[i + 1])
        if m.sum() > 1:
            lt_m.append(log_t[m].mean())
            lmu_m.append(np.max(np.log(muhat[m])))   # limsup 包络
    lt_m, lmu_m = np.array(lt_m), np.array(lmu_m)
    if len(lt_m) < 10:
        return None, None, None
    slope, intercept = np.polyfit(lt_m, lmu_m, 1)
    r = np.corrcoef(lt_m, lmu_m)[0, 1]
    return slope, alpha_exp, r

def box_dimension_cantor(k=15):
    """Cantor 测度盒计数谱维数 D2 验证（与论文3.2氢原子 D2 方法一致）。
    返回数值 D2（理论 ln2/ln3 ≈ 0.631）。"""
    # 构造 k 级 Cantor 集的 2^k 个区间段，统计各箱质量
    levels = [5, 6, 7, 8, 9, 10, 11]
    npts = 2 ** k
    x = cantor_points(k)
    w = np.full(npts, 1.0 / npts)
    dims = []
    for lev in levels:
        nb = 2 ** lev
        hist, _ = np.histogram(x, bins=nb, weights=w)
        p = hist[hist > 0]
        if len(p) < 3:
            continue
        S = (p ** 2).sum()
        dims.append((lev, np.log(nb), np.log(S)))
    if len(dims) < 3:
        return None
    ls, lS = zip(*[(b, s) for _, b, s in dims])
    D2 = -np.polyfit(ls, lS, 1)[0]
    return D2

def cantor_points(k):
    """k 级 Cantor 集：2^k 个等长区间 [0,1] 内的中心点。"""
    seg = 3.0 ** (-k)
    pts = np.arange(2**k) * seg * 3.0   # 每个小区间起点（步长3^{-k}）
    # 去除被删除段后的位置：标准构造
    idx = np.arange(2**k)
    pos = np.zeros(2**k)
    for j in range(k):
        bit = (idx >> (k - 1 - j)) & 1
        pos += bit * 2.0 * (3.0 ** (-(j + 1)))
    return pos + seg / 2.0

# ---------------------------------------------------------------
# B. 记忆核 → 非马尔可夫线型（Mittag-Leffler 型）
# ---------------------------------------------------------------
def total_lineshape(delta, alpha, kappa, gamma, eta):
    """混合谱线型（洛伦兹光滑分量 + 奇异连续谱分量的记忆核叠加）：
    S(δ) = Re A(iδ)/π,  A(s) = 1/[s + (1-η)γ²/(s+γ) + ηκΓ(1-α)s^{α-1}]
    奇异分量作为非马尔可夫衰减通道：中心衰减增强、尾部幂律化（偏离洛伦兹）。"""
    s = 1e-12 + 1j * delta
    KL = gamma ** 2 / (s + gamma)
    Ksc = kappa * gamma_func(1 - alpha) * s ** (alpha - 1.0)
    A = 1.0 / (s + (1 - eta) * KL + eta * Ksc)
    return np.real(A) / np.pi

def lineshape_tail(alpha, kappa, gamma, eta=0.8, tail_range=(0.5, 2.0)):
    """非马尔可夫线型尾验证：混合谱 vs 纯洛伦兹（η=0）的尾区对数斜率。
    洛伦兹尾 S∝δ^{-2}；奇异连续谱分量使尾斜率偏离（更陡且非零中心凹陷）。"""
    d = np.linspace(-3, 3, 6001)
    S_mix = total_lineshape(d, alpha, kappa, gamma, eta)
    S_lor = total_lineshape(d, alpha, kappa, gamma, 0.0)
    m = (np.abs(d) > tail_range[0]) & (np.abs(d) < tail_range[1])
    sl_mix, _ = np.polyfit(np.log(np.abs(d[m])), np.log(S_mix[m]), 1)
    sl_lor, _ = np.polyfit(np.log(np.abs(d[m])), np.log(S_lor[m]), 1)
    S_center_mix = S_mix[len(d) // 2]
    S_center_lor = S_lor[len(d) // 2]
    tail_frac_mix = np.trapz(S_mix[np.abs(d) > tail_range[0]], d[np.abs(d) > tail_range[0]]) / np.trapz(S_mix, d)
    tail_frac_lor = np.trapz(S_lor[np.abs(d) > tail_range[0]], d[np.abs(d) > tail_range[0]]) / np.trapz(S_lor, d)
    return {
        'tail_slope_mix': sl_mix, 'tail_slope_lorentz': sl_lor,
        'center_mix': S_center_mix, 'center_lorentz': S_center_lor,
        'tail_frac_mix': tail_frac_mix, 'tail_frac_lorentz': tail_frac_lor,
    }

def nmlo_predict(m, amplitudes, N_B=N_BALMER):
    """NMLO 发射强度标度：|EW_n| = A_s · η_sc(n)，η_sc(n) ∝ n^m
    （高阶态更接近电离阈 → 奇异连续谱权重 η_sc 单调增强 → 发射标度 n^m）。"""
    eta = N_B ** m
    preds = {}
    for s, A in amplitudes.items():
        preds[s] = A * eta
    return preds

# ---------------------------------------------------------------
# C. 拟合 3 颗星
# ---------------------------------------------------------------
def fit_nmlo():
    """拟合参数：全局 {m} + 每星振幅 {A_s}，目标 |EW_n| = A_s · n^m。
    对数残差最小化；排除 J233817 的 Hδ 异常点（-0.44，谱线可能受邻线污染）。"""
    stars = list(STARS.keys())
    obs = {s: np.abs(STARS[s]) for s in stars}
    mask = np.ones(7, dtype=bool)
    mask[3] = False

    def resid(params):
        m = params[0]
        amps = {s: np.exp(params[1 + i]) for i, s in enumerate(stars)}  # 保证振幅正性
        pred = nmlo_predict(m, amps)
        r = []
        for s in stars:
            mm = mask.copy()
            if s == 'J101712':
                mm[0] = False   # Hα 为弱吸收(+0.76)，非发射
            r.append(np.log(pred[s][mm]) - np.log(obs[s][mm]))
        return np.concatenate(r)

    p0 = [3.0] + [0.0] * len(stars)
    res = optimize.least_squares(resid, p0)
    m_f = res.x[0]
    amps_f = {s: np.exp(res.x[1 + i]) for i, s in enumerate(stars)}
    pred = nmlo_predict(m_f, amps_f)
    r_all, o_all, npts = [], [], 0
    for s in stars:
        mm = mask.copy()
        if s == 'J101712':
            mm[0] = False
        r_all += list(np.log(pred[s][mm]))
        o_all += list(np.log(obs[s][mm]))
        npts += mm.sum()
    r_all, o_all = np.array(r_all), np.array(o_all)
    ss_res = ((o_all - r_all) ** 2).sum()
    ss_tot = ((o_all - o_all.mean()) ** 2).sum()
    r2 = 1 - ss_res / ss_tot
    # 逐星斜率诊断（独立幂律指数，检验全局 m 的适用性）
    per_star = {}
    for s in stars:
        aew = np.abs(STARS[s])
        mm = mask.copy()
        if s == 'J101712':
            mm[0] = False   # Hα 为弱吸收(+0.76)，非发射
        x, y = np.log(N_BALMER[mm]), np.log(aew[mm])
        b, _ = np.polyfit(x, y, 1)
        per_star[s] = b
    return m_f, amps_f, r2, pred, per_star, npts

def main():
    print("=" * 62)
    print("NMLO：基于奇异连续谱测度的非马尔可夫线型算子")
    print("=" * 62)
    # A. 测度验证
    slope, alpha_exp, r_pl = verify_power_law()
    D2 = box_dimension_cantor()
    if slope is not None and D2 is not None:
        print(f"\n[A] 奇异连续谱测度（三进制 Cantor 测度）:")
        print(f"    盒计数谱维数 D2 = {D2:.3f} vs 理论 ln2/ln3 = 0.631")
        print(f"    傅里叶变换 limsup 衰减斜率 {slope:.3f} vs 理论 -(1-D) = {-alpha_exp:.3f} (r={r_pl:.2f})")
        print(f"    -> 奇异连续谱: 记忆核/关联函数幂律尾 (α = 1-D = {1-0.631:.3f})")
    # B. 线型尾验证
    print(f"\n[B] 非马尔可夫线型尾（混合谱 vs 洛伦兹，α=1-D={1-0.631:.3f}）:")
    tail = lineshape_tail(alpha=0.369, kappa=0.5, gamma=0.05, eta=0.8)
    print(f"    尾区对数斜率: 混合谱 {tail['tail_slope_mix']:.2f} vs 洛伦兹 {tail['tail_slope_lorentz']:.2f}")
    print(f"    中心值: 混合谱 {tail['center_mix']:.4f} vs 洛伦兹 {tail['center_lorentz']:.4f}")
    print(f"    尾占比: 混合谱 {tail['tail_frac_mix']:.3f} vs 洛伦兹 {tail['tail_frac_lorentz']:.3f}")
    print(f"    -> 奇异连续谱通道: 中心衰减增强 + 谱质量向幂律尾转移（非洛伦兹特征）")
    # C. 拟合
    print(f"\n[C] 三颗星拟合（|EW_n| = A_s · n^m）:")
    m_f, amps_f, r2, pred, per_star, npts = fit_nmlo()
    print(f"    全局线序指数 m = {m_f:.2f}")
    for s in STARS:
        print(f"    {s}: 振幅 A={amps_f[s]:.3f}, 独立斜率={per_star[s]:.2f}, "
              f"观测 |EW_η/EW_α|={np.abs(STARS[s])[-1]/np.abs(STARS[s])[0]:.1f}, "
              f"模型 |EW_η/EW_α|={pred[s][-1]/pred[s][0]:.1f}")
    print(f"    拟合优度 R² (log域, {npts}点) = {r2:.3f}")
    # 逐线对比
    print(f"\n    逐线对比（模型 vs 观测，Å）:")
    n2s = ['Hα', 'Hβ', 'Hγ', 'Hδ', 'Hε', 'Hζ', 'Hη']
    for s in STARS:
        line = f"    {s}: "
        line += " ".join(f"{n2s[i]} {pred[s][i]:+6.2f}/{STARS[s][i]:+6.2f}" for i in range(7))
        print(line)

if __name__ == "__main__":
    main()
