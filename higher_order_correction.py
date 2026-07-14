"""
高阶修正分析工具（v5.0探索）

方向：
  1. τ'''(q)三阶修正（cumulant展开三阶项）
  2. IFS参数网格优化反推
  3. q_s精细调优 + 物理约束

目标：将费米子RMSE(log)从0.52进一步降低
"""
import numpy as np
from itertools import product

# ============================================================
# SM基准数据
# ============================================================
sm_masses = np.array([
    2.2, 1270.0, 173100.0,     # u, c, t (up quarks)
    4.7, 95.0, 4180.0,         # d, s, b (down quarks)
    0.511, 105.66, 1776.86,    # e, mu, tau (leptons)
])
sm_log_m = np.log(sm_masses)
sector_names = ["Up quarks", "Down quarks", "Leptons", "Neutrinos"]

# ============================================================
# 多分形谱计算函数
# ============================================================
def multifractal_spectrum(q, p, c_arr):
    """计算多分形谱 tau(q), alpha(q), f(alpha), tau'(q), tau''(q), tau'''(q)"""
    p_arr = np.array(p)
    c_arr = np.array(c_arr)
    c_geo = np.exp(np.mean(np.log(c_arr)))
    ln_c_geo = np.log(c_geo)

    p_q = p_arr**q
    sum_pq = np.sum(p_q)

    # tau(q)
    tau_q = np.log(sum_pq) / ln_c_geo

    # alpha(q) = tau'(q) = <ln p> / ln c_geo
    mean_ln_p = np.sum(p_q * np.log(p_arr)) / sum_pq
    alpha_q = mean_ln_p / ln_c_geo

    # f(alpha) = q*alpha - tau(q)
    f_alpha = q * alpha_q - tau_q

    # tau''(q) = Var_q(ln p) / ln c_geo  (<= 0)
    var_ln_p = np.sum(p_q * (np.log(p_arr))**2) / sum_pq - mean_ln_p**2
    tau_pp = var_ln_p / ln_c_geo

    # tau'''(q) = Skew_q(ln p) / ln c_geo
    # 三阶中心矩（偏度）
    skew_ln_p = np.sum(p_q * (np.log(p_arr) - mean_ln_p)**3) / sum_pq
    tau_ppp = skew_ln_p / ln_c_geo

    # 有效收缩因子 c_eff = <c>_q (q-加权平均)
    c_eff = np.sum(p_q * c_arr) / sum_pq

    return {
        'tau': tau_q, 'alpha': alpha_q, 'f_alpha': f_alpha,
        'tau_pp': tau_pp, 'tau_ppp': tau_ppp,
        'c_eff': c_eff, 'c_geo': c_geo,
        'mean_ln_p': mean_ln_p, 'var_ln_p': var_ln_p, 'skew_ln_p': skew_ln_p,
    }

def ifs_dim(c_list):
    c_arr = np.array(c_list)
    def f(d): return np.sum(c_arr**d) - 1
    lo, hi = 0.01, 10.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if f(mid) > 0: lo = mid
        else: hi = mid
    return (lo + hi) / 2

# ============================================================
# 完整质量预测函数（可配置参数）
# ============================================================
def predict_masses(ifs_c, ifs_p, sector_qs, gen_c, xi_0=1/6,
                   use_3rd_order=False, eta_0=0.0,
                   y0_method='ifs', y0_anchor=None):
    """
    完整质量预测

    参数:
      ifs_c: IFS收缩因子 [c1, c2]
      ifs_p: IFS概率 [p1, p2]
      sector_qs: 4个扇区的q值 [up, down, lep, nu]
      gen_c: 三代收缩因子 [c1, c2, c3] (用于d_frac)
      xi_0: 形状修正稀释系数 (默认1/N_EW=1/6)
      use_3rd_order: 是否使用三阶修正τ'''(q)
      eta_0: 三阶修正强度系数
      y0_method: 'ifs' | 'anchor'
      y0_anchor: 锚定的y_t值（当y0_method='anchor'时使用）
    """
    c_geo = np.exp(np.mean(np.log(ifs_c)))
    ln_c_geo = np.log(c_geo)
    d_frac = ifs_dim(gen_c)
    N_EW = 6

    # 扇区参数
    n_sectors = len(sector_qs)
    c_eff_s = np.zeros(n_sectors)
    alpha_s = np.zeros(n_sectors)
    f_alpha_s = np.zeros(n_sectors)
    tau_pp_s = np.zeros(n_sectors)
    tau_ppp_s = np.zeros(n_sectors)

    for s, q in enumerate(sector_qs):
        spec = multifractal_spectrum(q, ifs_p, ifs_c)
        c_eff_s[s] = spec['c_eff']
        alpha_s[s] = spec['alpha']
        f_alpha_s[s] = spec['f_alpha']
        tau_pp_s[s] = spec['tau_pp']
        tau_ppp_s[s] = spec['tau_ppp']

    # 扇区权重 (μ_s 比例)
    sector_weights = np.array([np.sum(np.array(ifs_p)**q) if q != 0 else 1.0
                               for q in sector_qs])
    sector_weights = sector_weights / np.sum(sector_weights)

    # 形状修正 κ_s (二阶)
    kappa_s_2nd = sector_qs * np.abs(tau_pp_s) * xi_0

    # 三阶修正 λ_s (τ'''(q)项)
    # 物理意义：cumulant展开三阶项，衡量代内因子的非对称偏差
    # κ_s^{(3)} = q_s^2 · τ'''(q_s) · η_0
    # 注意：τ'''可正可负，偏度方向由τ'''符号决定
    kappa_s_3rd = np.zeros(n_sectors)
    if use_3rd_order:
        # 三阶修正: intra_{s,k} 中的指数增加 η·τ'''·(k-1)(k-2)/6 项
        kappa_s_3rd = (sector_qs**2) * tau_ppp_s * eta_0

    # 代内因子 β_s
    beta_s = np.zeros(n_sectors)
    for s in range(n_sectors):
        beta_s[s] = N_EW * alpha_s[s] * f_alpha_s[s] / d_frac

    # 三代代内因子 (k=1,2,3)
    k_arr = np.arange(1, 4, dtype=float)
    intra_gen = np.zeros((n_sectors, 3))

    for s in range(n_sectors):
        # 基础指数: β·k
        exponent = beta_s[s] * k_arr

        # 二阶修正: β·k·κ·(k-1)/2  (即 k(k-1)·βκ/2)
        exponent += beta_s[s] * kappa_s_2nd[s] * k_arr * (k_arr - 1) / 2

        # 三阶修正: β·λ·k(k-1)(k-2)/6
        if use_3rd_order:
            exponent += beta_s[s] * kappa_s_3rd[s] * k_arr * (k_arr - 1) * (k_arr - 2) / 6

        intra_gen[s, :] = (1.0 / c_eff_s[s])**exponent
        intra_gen[s, :] = intra_gen[s, :] / intra_gen[s, 0]

    # 扇区比例 (y_up/y_lep 等)
    # y_s ∝ 1/μ_s (扇区测度反比于Yukawa耦合)
    # 用扇区权重的比值
    y_ratio = sector_weights[0] / sector_weights  # up / s
    y_ratio = y_ratio / y_ratio[2]  # 以leptons为基准=1

    # FRG重整化因子 (共用)
    Z_f = 1.0 / (1 + 3 * 0.1)  # 费米子圈
    Z_g = 1.0 / (1 + 0.01)     # 规范圈
    Z_d = d_frac / 4.0         # 分形维数
    Z_rec = 1.0 / (1 + 0.3)    # 递归深度
    Z_y = Z_f * Z_g * Z_d * Z_rec

    # RG跑动圈数
    Lambda = 1e19  # Planck
    m_Z_val = 91.1876
    ln_ratio = np.log(Lambda / m_Z_val)
    N_RG = ln_ratio / (2 * np.pi)

    # IFS测度矩 (共用)
    M2 = np.sum(np.array(ifs_p) * np.array(ifs_c)**2)
    M4 = np.sum(np.array(ifs_p) * np.array(ifs_c)**4)
    lambda_bare = M4 / M2**2

    # y_0计算
    if y0_method == 'ifs':
        y_0 = np.sqrt(lambda_bare) * Z_y**N_RG
    else:
        y_t_anchor = y0_anchor if y0_anchor else 0.995
        y_0 = y_t_anchor / (y_ratio[0] * intra_gen[0, 2])

    # 绝对Yukawa耦合
    y_abs = np.zeros((n_sectors, 3))
    for s in range(n_sectors):
        y_abs[s, :] = y_0 * y_ratio[s] * intra_gen[s, :]

    # 费米子质量 m = y * v/sqrt(2)
    v = 246000.0  # MeV
    masses = y_abs * v / np.sqrt(2)

    # 规范耦合
    # sin^2(theta_W) = 3/8 (GUT), RG修正至m_Z
    alpha_em = 1.0 / 128.0
    e = np.sqrt(4 * np.pi * alpha_em)
    sin2_theta_W = 0.231  # 实验值锚定
    g = e / np.sqrt(sin2_theta_W)
    g_prime = e / np.sqrt(1 - sin2_theta_W)
    g_s = 1.1555  # 强耦合

    # 规范玻色子
    m_W = g * v / 2
    m_Z = np.sqrt(g**2 + g_prime**2) * v / 2

    # Higgs
    Z_lambda = Z_y
    lambda_phys = lambda_bare * Z_lambda
    m_H = np.sqrt(2 * lambda_phys) * v

    return {
        'masses': masses,          # [4扇区, 3代]
        'y_abs': y_abs,
        'y_0': y_0,
        'y_ratio': y_ratio,
        'intra_gen': intra_gen,
        'beta_s': beta_s,
        'kappa_s_2nd': kappa_s_2nd,
        'kappa_s_3rd': kappa_s_3rd,
        'c_eff_s': c_eff_s,
        'alpha_s': alpha_s,
        'f_alpha_s': f_alpha_s,
        'tau_pp_s': tau_pp_s,
        'tau_ppp_s': tau_ppp_s,
        'd_frac': d_frac,
        'm_W': m_W,
        'm_Z': m_Z,
        'm_H': m_H,
        'g': g, 'g_prime': g_prime, 'g_s': g_s,
    }

def compute_rmse(pred_masses):
    """计算9个费米子的log空间RMSE"""
    pred_flat = pred_masses[:3, :].flatten()  # up, down, lep (neutrinos不计)
    log_pred = np.log(pred_flat)
    return np.sqrt(np.mean((log_pred - sm_log_m)**2))

def print_comparison(result):
    """打印对比表"""
    masses = result['masses']
    print(f"\n{'粒子':<6} {'预测(MeV)':>14} {'SM(MeV)':>14} {'比值':>10} {'log比值':>10}")
    print("-" * 60)
    labels = [('u', 0, 0), ('c', 0, 1), ('t', 0, 2),
              ('d', 1, 0), ('s', 1, 1), ('b', 1, 2),
              ('e', 2, 0), ('μ', 2, 1), ('τ', 2, 2)]
    for name, s, k in labels:
        pred = masses[s, k]
        sm_idx = s * 3 + k
        sm_val = sm_masses[sm_idx]
        ratio = pred / sm_val
        log_ratio = np.log(ratio)
        print(f"  {name:<4} {pred:>14.4f} {sm_val:>14.2f} {ratio:>10.4f} {log_ratio:>10.4f}")
    rmse = compute_rmse(masses)
    print(f"\n  费米子RMSE(log) = {rmse:.4f}")

    print(f"\n  规范玻色子:")
    print(f"    m_W = {result['m_W']:.1f} MeV (SM: 80400, ratio={result['m_W']/80400:.4f})")
    print(f"    m_Z = {result['m_Z']:.1f} MeV (SM: 91200, ratio={result['m_Z']/91200:.4f})")
    print(f"    m_H = {result['m_H']:.1f} MeV (SM: 125000, ratio={result['m_H']/125000:.4f})")

# ============================================================
# 实验1: 三阶修正τ'''(q)的影响
# ============================================================
print("=" * 70)
print("实验1: 三阶修正τ'''(q)对RMSE的影响")
print("=" * 70)

ifs_c_base = [0.4, 0.35]
ifs_p_base = [0.85, 0.15]
qs_base = np.array([-0.5, 0.5, -1.3, -3.0])
gen_c_base = [0.5, 0.25, 0.125]

# 基础 (二阶)
res_base = predict_masses(ifs_c_base, ifs_p_base, qs_base, gen_c_base,
                          xi_0=1/6, use_3rd_order=False, y0_method='anchor')
print("\n--- v4.0 基础（二阶修正，top锚定）---")
print_comparison(res_base)

# 三阶修正（扫描eta_0）
print(f"\n--- 三阶修正扫描 η_0 ---")
print(f"{'η_0':>10} {'RMSE':>10} {'改善':>10}")
print("-" * 35)
best_eta = 0
best_eta_rmse = 999
for eta in np.linspace(-2.0, 2.0, 41):
    res = predict_masses(ifs_c_base, ifs_p_base, qs_base, gen_c_base,
                         xi_0=1/6, use_3rd_order=True, eta_0=eta,
                         y0_method='anchor')
    rmse = compute_rmse(res['masses'])
    if rmse < best_eta_rmse:
        best_eta_rmse = rmse
        best_eta = eta
    if abs(eta) < 0.01 or abs(eta - round(eta)) < 0.01:
        print(f"  {eta:>10.3f} {rmse:>10.4f} {rmse/compute_rmse(res_base['masses']):>10.3f}x")

print(f"\n  最优 η_0 = {best_eta:.3f}, RMSE = {best_eta_rmse:.4f}")

res_3rd = predict_masses(ifs_c_base, ifs_p_base, qs_base, gen_c_base,
                         xi_0=1/6, use_3rd_order=True, eta_0=best_eta,
                         y0_method='anchor')
print(f"\n--- 最优三阶修正结果 ---")
print_comparison(res_3rd)

# ============================================================
# 实验2: IFS参数优化反推
# ============================================================
print(f"\n{'='*70}")
print("实验2: IFS参数网格优化反推")
print("=" * 70)

best_ifs_rmse = 999
best_ifs_params = None

c1_range = np.linspace(0.30, 0.50, 11)
c2_range = np.linspace(0.25, 0.45, 11)
p1_range = np.linspace(0.70, 0.95, 11)

print(f"\n  扫描范围: c1∈[{c1_range[0]:.2f},{c1_range[-1]:.2f}], "
      f"c2∈[{c2_range[0]:.2f},{c2_range[-1]:.2f}], "
      f"p1∈[{p1_range[0]:.2f},{p1_range[-1]:.2f}]")
print(f"  网格大小: {len(c1_range)*len(c2_range)*len(p1_range)}")

import sys
count = 0
for c1 in c1_range:
    for c2 in c2_range:
        for p1 in p1_range:
            p2 = 1 - p1
            res = predict_masses([c1, c2], [p1, p2], qs_base, gen_c_base,
                                 xi_0=1/6, use_3rd_order=True, eta_0=best_eta,
                                 y0_method='anchor')
            rmse = compute_rmse(res['masses'])
            count += 1
            if rmse < best_ifs_rmse:
                best_ifs_rmse = rmse
                best_ifs_params = (c1, c2, p1, p2)

print(f"\n  最优IFS参数:")
print(f"    c = [{best_ifs_params[0]:.4f}, {best_ifs_params[1]:.4f}]")
print(f"    p = [{best_ifs_params[2]:.4f}, {best_ifs_params[3]:.4f}]")
print(f"    RMSE = {best_ifs_rmse:.4f}")

res_opt_ifs = predict_masses(
    [best_ifs_params[0], best_ifs_params[1]],
    [best_ifs_params[2], best_ifs_params[3]],
    qs_base, gen_c_base,
    xi_0=1/6, use_3rd_order=True, eta_0=best_eta,
    y0_method='anchor')
print(f"\n--- 最优IFS+三阶修正结果 ---")
print_comparison(res_opt_ifs)

# ============================================================
# 实验3: q_s精细调优 (从SM反推)
# ============================================================
print(f"\n{'='*70}")
print("实验3: q_s精细调优 + IFS优化 + 三阶修正")
print("=" * 70)

# 用最优IFS参数作为基础
c1_opt, c2_opt, p1_opt, p2_opt = best_ifs_params

# q_s网格搜索
q_ranges = [
    np.linspace(-1.0, 0.0, 11),   # up
    np.linspace(0.0, 1.0, 11),    # down
    np.linspace(-2.0, -0.5, 16),  # lepton
    np.linspace(-4.0, -2.0, 11),  # neutrino
]

best_q_rmse = 999
best_qs = None

print(f"\n  4维q参数网格搜索...")
print(f"  网格大小: {len(q_ranges[0])*len(q_ranges[1])*len(q_ranges[2])*len(q_ranges[3])}")

count = 0
for q_up in q_ranges[0]:
    for q_down in q_ranges[1]:
        for q_lep in q_ranges[2]:
            for q_nu in q_ranges[3]:
                qs = np.array([q_up, q_down, q_lep, q_nu])
                res = predict_masses(
                    [c1_opt, c2_opt], [p1_opt, p2_opt],
                    qs, gen_c_base,
                    xi_0=1/6, use_3rd_order=True, eta_0=best_eta,
                    y0_method='anchor')
                rmse = compute_rmse(res['masses'])
                count += 1
                if rmse < best_q_rmse:
                    best_q_rmse = rmse
                    best_qs = qs.copy()

print(f"\n  最优q参数: {best_qs}")
print(f"  RMSE = {best_q_rmse:.4f}")

res_opt_q = predict_masses(
    [c1_opt, c2_opt], [p1_opt, p2_opt],
    best_qs, gen_c_base,
    xi_0=1/6, use_3rd_order=True, eta_0=best_eta,
    y0_method='anchor')
print(f"\n--- 最优q + 最优IFS + 三阶修正结果 ---")
print_comparison(res_opt_q)

# ============================================================
# 实验4: 全部参数联合精细优化 (梯度下降)
# ============================================================
print(f"\n{'='*70}")
print("实验4: 全部参数联合精细优化（梯度下降微调）")
print("=" * 70)

from scipy.optimize import minimize

def objective(params):
    """优化目标: log空间RMSE"""
    c1, c2, p1, qu, qd, ql, qn, xi0, eta0 = params
    p2 = 1 - p1
    # 参数约束
    if c1 <= 0 or c2 <= 0 or c1 >= 1 or c2 >= 1:
        return 100
    if p1 <= 0 or p1 >= 1:
        return 100
    if xi0 <= 0 or xi0 >= 1:
        return 100

    qs = np.array([qu, qd, ql, qn])
    try:
        res = predict_masses(
            [c1, c2], [p1, p2], qs, gen_c_base,
            xi_0=xi0, use_3rd_order=True, eta_0=eta0,
            y0_method='anchor')
        return compute_rmse(res['masses'])
    except:
        return 100

# 初始点：当前最优
x0 = np.array([c1_opt, c2_opt, p1_opt,
               best_qs[0], best_qs[1], best_qs[2], best_qs[3],
               1/6, best_eta])

print(f"\n  初始RMSE: {objective(x0):.4f}")
print(f"  初始参数: c=[{x0[0]:.4f},{x0[1]:.4f}], p=[{x0[2]:.4f},{1-x0[2]:.4f}]")
print(f"           q=[{x0[3]:.3f},{x0[4]:.3f},{x0[5]:.3f},{x0[6]:.3f}]")
print(f"           xi0={x0[7]:.4f}, eta0={x0[8]:.4f}")

# Nelder-Mead优化
result_opt = minimize(objective, x0, method='Nelder-Mead',
                      options={'maxiter': 5000, 'xatol': 1e-6, 'fatol': 1e-6})

x_opt = result_opt.x
print(f"\n  优化后RMSE: {result_opt.fun:.4f}")
print(f"  迭代次数: {result_opt.nit}")
print(f"  最优参数:")
print(f"    c = [{x_opt[0]:.6f}, {x_opt[1]:.6f}]")
print(f"    p = [{x_opt[2]:.6f}, {1-x_opt[2]:.6f}]")
print(f"    q = [{x_opt[3]:.6f}, {x_opt[4]:.6f}, {x_opt[5]:.6f}, {x_opt[6]:.6f}]")
print(f"    ξ_0 = {x_opt[7]:.6f}")
print(f"    η_0 = {x_opt[8]:.6f}")

res_v5 = predict_masses(
    [x_opt[0], x_opt[1]], [x_opt[2], 1-x_opt[2]],
    np.array([x_opt[3], x_opt[4], x_opt[5], x_opt[6]]),
    gen_c_base,
    xi_0=x_opt[7], use_3rd_order=True, eta_0=x_opt[8],
    y0_method='anchor')
print(f"\n--- v5.0 精细优化结果 ---")
print_comparison(res_v5)

# ============================================================
# 汇总
# ============================================================
print(f"\n{'='*70}")
print("精度改善汇总")
print("=" * 70)

rmse_v2 = 3.20  # 粗略估计
rmse_v3 = 1.0174
rmse_v4 = compute_rmse(res_base['masses'])
rmse_v5 = result_opt.fun

print(f"  v2.x (幂律代内因子):  RMSE = {rmse_v2:.2f}")
print(f"  v3.0 (指数代内因子):   RMSE = {rmse_v3:.4f}  改善 {rmse_v2/rmse_v3:.2f}x")
print(f"  v4.0 (τ''形状修正):    RMSE = {rmse_v4:.4f}  改善 {rmse_v3/rmse_v4:.2f}x (累计 {rmse_v2/rmse_v4:.2f}x)")
print(f"  v5.0 (τ'''+IFS+q优化): RMSE = {rmse_v5:.4f}  改善 {rmse_v4/rmse_v5:.2f}x (累计 {rmse_v2/rmse_v5:.2f}x)")
