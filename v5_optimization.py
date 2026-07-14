"""
v5.0 物理约束优化分析

约束条件:
  1. IFS收缩因子 c_i ∈ [0.30, 0.50]（分形几何合理范围）
  2. IFS概率 p1 ∈ [0.70, 0.90]（主导收缩高概率）
  3. q参数范围:
     - up夸克: q_up ∈ [-0.8, -0.2]（弱负偏，低概率区）
     - down夸克: q_down ∈ [0.2, 0.8]（弱正偏，高概率区）
     - 轻子: q_lep ∈ [-1.8, -0.8]（更强负偏）
     - 中微子: q_nu ∈ [-4.0, -2.0]（最强负偏，极稀有）
  4. ξ_0 = 1/N_EW = 1/6（固定，从电弱对称群推导）
  5. η_0 = 0（三阶修正暂不启用，保持框架简洁）

目标: 在物理约束下最小化RMSE，同时验证参数的物理意义
"""
import numpy as np
from scipy.optimize import minimize, differential_evolution

# ============================================================
# SM基准数据
# ============================================================
sm_masses = np.array([
    2.2, 1270.0, 173100.0,     # u, c, t
    4.7, 95.0, 4180.0,         # d, s, b
    0.511, 105.66, 1776.86,    # e, mu, tau
])
sm_log_m = np.log(sm_masses)

# ============================================================
# 多分形谱函数
# ============================================================
def multifractal_spectrum(q, p, c_arr):
    p_arr = np.array(p)
    c_arr = np.array(c_arr)
    c_geo = np.exp(np.mean(np.log(c_arr)))
    ln_c_geo = np.log(c_geo)

    p_q = p_arr**q
    sum_pq = np.sum(p_q)
    tau_q = np.log(sum_pq) / ln_c_geo
    mean_ln_p = np.sum(p_q * np.log(p_arr)) / sum_pq
    alpha_q = mean_ln_p / ln_c_geo
    f_alpha = q * alpha_q - tau_q
    var_ln_p = np.sum(p_q * (np.log(p_arr))**2) / sum_pq - mean_ln_p**2
    tau_pp = var_ln_p / ln_c_geo
    c_eff = np.sum(p_q * c_arr) / sum_pq

    return {'tau': tau_q, 'alpha': alpha_q, 'f_alpha': f_alpha,
            'tau_pp': tau_pp, 'c_eff': c_eff}

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
# 完整预测函数
# ============================================================
def predict_masses_v5(ifs_c, ifs_p, sector_qs, gen_c, xi_0=1/6,
                      use_3rd_order=False, eta_0=0.0, y0_method='anchor'):
    c_geo = np.exp(np.mean(np.log(ifs_c)))
    d_frac = ifs_dim(gen_c)
    N_EW = 6
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

    # 扇区权重
    sector_weights = np.array([np.sum(np.array(ifs_p)**q) if q != 0 else 1.0
                               for q in sector_qs])
    sector_weights = sector_weights / np.sum(sector_weights)

    # 二阶形状修正
    kappa_s = sector_qs * np.abs(tau_pp_s) * xi_0

    # 三阶修正
    kappa_3rd = np.zeros(n_sectors)
    if use_3rd_order:
        ln_c_geo = np.log(c_geo)
        for s, q in enumerate(sector_qs):
            p_arr = np.array(ifs_p)
            p_q = p_arr**q
            sum_pq = np.sum(p_q)
            mean_ln_p = np.sum(p_q * np.log(p_arr)) / sum_pq
            skew_ln_p = np.sum(p_q * (np.log(p_arr) - mean_ln_p)**3) / sum_pq
            tau_ppp = skew_ln_p / ln_c_geo
            kappa_3rd[s] = (q**2) * tau_ppp * eta_0

    # 代内因子 β_s
    beta_s = np.zeros(n_sectors)
    for s in range(n_sectors):
        beta_s[s] = N_EW * alpha_s[s] * f_alpha_s[s] / d_frac

    # 三代代内因子
    k_arr = np.arange(1, 4, dtype=float)
    intra_gen = np.zeros((n_sectors, 3))
    for s in range(n_sectors):
        exponent = beta_s[s] * k_arr
        exponent += beta_s[s] * kappa_s[s] * k_arr * (k_arr - 1) / 2
        if use_3rd_order:
            exponent += beta_s[s] * kappa_3rd[s] * k_arr * (k_arr - 1) * (k_arr - 2) / 6
        intra_gen[s, :] = (1.0 / c_eff_s[s])**exponent
        intra_gen[s, :] = intra_gen[s, :] / intra_gen[s, 0]

    # 扇区比例 (以leptons=1为基准)
    y_ratio = sector_weights[0] / sector_weights
    y_ratio = y_ratio / y_ratio[2]

    # y_0
    y_t_anchor = 0.995
    y_0 = y_t_anchor / (y_ratio[0] * intra_gen[0, 2])

    # 绝对质量
    v = 246000.0
    masses = np.zeros((n_sectors, 3))
    for s in range(n_sectors):
        masses[s, :] = y_0 * y_ratio[s] * intra_gen[s, :] * v / np.sqrt(2)

    return {'masses': masses, 'y_0': y_0, 'y_ratio': y_ratio,
            'intra_gen': intra_gen, 'beta_s': beta_s,
            'kappa_s': kappa_s, 'kappa_3rd': kappa_3rd,
            'c_eff_s': c_eff_s, 'alpha_s': alpha_s, 'f_alpha_s': f_alpha_s,
            'tau_pp_s': tau_pp_s, 'd_frac': d_frac}

def compute_rmse(masses):
    pred_flat = masses[:3, :].flatten()
    log_pred = np.log(pred_flat)
    return np.sqrt(np.mean((log_pred - sm_log_m)**2))

# ============================================================
# 优化约束
# ============================================================
GEN_C_BASE = [0.5, 0.25, 0.125]

# 物理约束边界
BOUNDS = [
    (0.30, 0.50),   # c1: IFS收缩因子1
    (0.25, 0.45),   # c2: IFS收缩因子2
    (0.70, 0.90),   # p1: IFS概率1
    (-0.80, -0.20), # q_up: up夸克q参数
    (0.20, 0.80),   # q_down: down夸克q参数
    (-1.80, -0.80), # q_lep: 轻子q参数
    (-4.00, -2.00), # q_nu: 中微子q参数
]
PARAM_NAMES = ['c1', 'c2', 'p1', 'q_up', 'q_down', 'q_lep', 'q_nu']

def objective(params):
    c1, c2, p1, qu, qd, ql, qn = params
    p2 = 1 - p1
    qs = np.array([qu, qd, ql, qn])
    try:
        res = predict_masses_v5([c1, c2], [p1, p2], qs, GEN_C_BASE,
                                xi_0=1/6, use_3rd_order=False, y0_method='anchor')
        return compute_rmse(res['masses'])
    except:
        return 100

print("=" * 70)
print("v5.0 物理约束优化")
print("=" * 70)

# 初始点: v4.0参数
x0 = np.array([0.4, 0.35, 0.85, -0.5, 0.5, -1.3, -3.0])
rmse_v4 = objective(x0)
print(f"\nv4.0参数 RMSE = {rmse_v4:.4f}")

# 用differential_evolution做全局优化
print(f"\n全局优化（差分进化）...")
result_de = differential_evolution(objective, bounds=BOUNDS,
                                    maxiter=200, popsize=30,
                                    tol=1e-6, seed=42)
x_de = result_de.x
rmse_de = result_de.fun

print(f"  全局最优 RMSE = {rmse_de:.4f}")
print(f"  最优参数:")
for name, val in zip(PARAM_NAMES, x_de):
    print(f"    {name} = {val:.6f}")

# 用Nelder-Mead精细微调
print(f"\n精细微调（Nelder-Mead）...")
result_nm = minimize(objective, x_de, method='Nelder-Mead',
                     options={'maxiter': 5000, 'xatol': 1e-8, 'fatol': 1e-8})
x_opt = result_nm.x
rmse_v5 = result_nm.fun
print(f"  微调后 RMSE = {rmse_v5:.4f}")
print(f"  最优参数:")
for name, val in zip(PARAM_NAMES, x_opt):
    print(f"    {name} = {val:.6f}")

# 详细结果
c1_opt, c2_opt, p1_opt, qu_opt, qd_opt, ql_opt, qn_opt = x_opt
p2_opt = 1 - p1_opt
qs_opt = np.array([qu_opt, qd_opt, ql_opt, qn_opt])

res_v5 = predict_masses_v5([c1_opt, c2_opt], [p1_opt, p2_opt], qs_opt, GEN_C_BASE,
                            xi_0=1/6, use_3rd_order=False, y0_method='anchor')

print(f"\n--- v5.0 详细预测结果 ---")
masses = res_v5['masses']
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

print(f"\n  RMSE(log) = {rmse_v5:.4f}")

# 扇区参数分析
print(f"\n--- 扇区参数分析 ---")
sector_names = ["Up quarks", "Down quarks", "Leptons", "Neutrinos"]
print(f"{'扇区':<14} {'q_s':>8} {'c_eff':>10} {'alpha_s':>10} {'f(alpha)':>10} {'tau''':>10} {'kappa_s':>10} {'beta_s':>10}")
print("-" * 90)
for s in range(4):
    print(f"  {sector_names[s]:<12} {qs_opt[s]:>8.4f} {res_v5['c_eff_s'][s]:>10.6f} "
          f"{res_v5['alpha_s'][s]:>10.4f} {res_v5['f_alpha_s'][s]:>10.4f} "
          f"{res_v5['tau_pp_s'][s]:>10.6f} {res_v5['kappa_s'][s]:>10.6f} "
          f"{res_v5['beta_s'][s]:>10.4f}")

# 代内因子分析
print(f"\n--- 代内因子分析 ---")
print(f"{'扇区':<14} {'intra_1':>12} {'intra_2':>12} {'intra_3':>12} {'间隔比':>10}")
print("-" * 65)
for s in range(3):
    ig = res_v5['intra_gen'][s]
    ratio = np.log(ig[2]/ig[1]) / np.log(ig[1]/ig[0])
    sm_ratio = np.log(sm_masses[s*3+2]/sm_masses[s*3+1]) / np.log(sm_masses[s*3+1]/sm_masses[s*3])
    print(f"  {sector_names[s]:<12} {ig[0]:>12.2f} {ig[1]:>12.2f} {ig[2]:>12.2f} {ratio:>10.4f} (SM: {sm_ratio:.4f})")

# y_ratio分析
print(f"\n--- 扇区Yukawa比例分析 ---")
print(f"  y_up/y_lep = {res_v5['y_ratio'][0]:.4f} (SM: {2.2/0.511*1776.86/173100*np.sqrt(2)*173100/1776.86:.4f}... 直接质量比)")
print(f"  y_down/y_lep = {res_v5['y_ratio'][1]:.4f}")
print(f"  y_nu/y_lep = {res_v5['y_ratio'][3]:.6f}")

# 直接质量比
m_up_sm = 2.2 / 0.511 * 1776.86 / 173100
print(f"  (参考: m_up/m_e = {2.2/0.511:.2f}, m_down/m_e = {4.7/0.511:.2f})")
print(f"  预测: m_up/m_e = {masses[0,0]/masses[2,0]:.2f}, m_down/m_e = {masses[1,0]/masses[2,0]:.2f}")

# ============================================================
# 实验: 尝试从Cl(1,7)旋量结构推导q参数模式
# ============================================================
print(f"\n{'='*70}")
print("探索: q参数的代数结构分析")
print("=" * 70)

# q参数的模式分析
print(f"\n最优q参数: {qs_opt[:3]}")
print(f"  q_up = {qs_opt[0]:.4f}")
print(f"  q_down = {qs_opt[1]:.4f}")
print(f"  q_lep = {qs_opt[2]:.4f}")

# 分析模式: q_down ≈ -q_up?
print(f"\n模式检验:")
print(f"  q_up + q_down = {qs_opt[0] + qs_opt[1]:.4f} (对称? 0=完全对称)")
print(f"  q_lep / q_up = {qs_opt[2]/qs_opt[0]:.4f} (比例?)")
print(f"  q_lep - q_up = {qs_opt[2] - qs_opt[0]:.4f} (差?)")

# Cl(6) Cartan子代数有3个生成元, 对应3个q参数
# 也许 q_s = n_s * q_0, 其中n_s是某种量子数
print(f"\n简单比例假设检验 (q_s = n_s * q0):")
for n1, n2, n3 in [(1, -1, 3), (1, -1, 2), (1, 1, 3),
                    (1, -2, 3), (1, -1, 2.5), (1, -1, 2.6)]:
    # q_up = n1*q0, q_down = n2*q0, q_lep = n3*q0
    # 用最小二乘拟合q0
    q_vals = qs_opt[:3]
    n_vals = np.array([n1, n2, n3])
    q0_fit = np.sum(q_vals * n_vals) / np.sum(n_vals**2)
    pred = q0_fit * n_vals
    err = np.sqrt(np.mean((q_vals - pred)**2))
    print(f"  n=[{n1}, {n2}, {n3}]: q0={q0_fit:.4f}, RMSE={err:.4f}")

# ============================================================
# 精度改善汇总
# ============================================================
print(f"\n{'='*70}")
print("精度改善汇总 (物理约束下)")
print("=" * 70)

rmse_v2 = 3.20
rmse_v3 = 1.0174
print(f"  v2.x (幂律代内因子):  RMSE = {rmse_v2:.2f}")
print(f"  v3.0 (指数代内因子):   RMSE = {rmse_v3:.4f}  改善 {rmse_v2/rmse_v3:.2f}x")
print(f"  v4.0 (τ''形状修正):    RMSE = {rmse_v4:.4f}  改善 {rmse_v3/rmse_v4:.2f}x (累计 {rmse_v2/rmse_v4:.2f}x)")
print(f"  v5.0 (IFS+q优化, 物理约束): RMSE = {rmse_v5:.4f}  改善 {rmse_v4/rmse_v5:.2f}x (累计 {rmse_v2/rmse_v5:.2f}x)")

# 自由参数数分析
print(f"\n自由参数统计:")
print(f"  v3.0: 4个q参数 = 4个自由参数")
print(f"  v4.0: 4个q参数 = 4个自由参数 (ξ_0=1/N_EW从框架推导)")
print(f"  v5.0: 2个IFS参数 + 4个q参数 = 6个自由参数 (ξ_0=1/N_EW固定)")
print(f"  数据点: 9个费米子质量")
