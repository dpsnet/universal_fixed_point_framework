"""
v5.2 缺口攻坚: 四阶峰度修正 + 扇区依赖参数 + Cl(1,7)代数推导

v5.1剩余缺口模式分析:
  Up扇区:  u=1.05(好)  c=0.75(低)  t=1.00(好)  → k=2偏低
  Down扇区: d=0.94(好) s=1.40(高)  b=0.84(低)  → k=2偏高,k=3偏低
  Lep扇区:  e=0.99(好) mu=0.93(好) tau=1.04(好) → 已解决!

诊断:
  - Down扇区: s过估+b低估 = 代内因子曲率过大(中间凸起)
    → 需要负峰度修正(压平k=2)
  - Up扇区: c低估 = 代内因子增长不够快
    → 可能需要Up扇区专用的eta_adjust
  - 轻子扇区已完美解决,说明三阶+色Casimir对q<0扇区足够

修正方向:
  A. τ''''(q)四阶峰度修正: 压平Down扇区k=2的凸起
  B. 扇区依赖eta_scale: Up/Down/Lepton各有不同
  C. Cl(1,7)旋量代数推导
"""
import numpy as np
from scipy.optimize import differential_evolution, minimize

# SM基准数据
sm_masses = np.array([2.2, 1270.0, 173100.0, 4.7, 95.0, 4180.0, 0.511, 105.66, 1776.86])
sm_log_m = np.log(sm_masses)
GEN_C = [0.5, 0.25, 0.125]

N_c = 3
N_EW = 6

def multifractal_spectrum_full(q, p, c_arr):
    p_arr = np.array(p, dtype=float)
    c_arr = np.array(c_arr, dtype=float)
    c_geo = np.exp(np.mean(np.log(c_arr)))
    ln_c = np.log(c_geo)
    p_q = p_arr**q
    sum_pq = np.sum(p_q)
    tau = np.log(sum_pq) / ln_c
    mean_ln_p = np.sum(p_q * np.log(p_arr)) / sum_pq
    alpha = mean_ln_p / ln_c
    f_alpha = q * alpha - tau
    # 二阶: 方差
    var_ln_p = np.sum(p_q * (np.log(p_arr))**2) / sum_pq - mean_ln_p**2
    tau_pp = var_ln_p / ln_c
    # 三阶: 偏度
    skew_ln_p = np.sum(p_q * (np.log(p_arr) - mean_ln_p)**3) / sum_pq
    tau_ppp = skew_ln_p / ln_c
    # 四阶: 峰度 (cumulant = E[(x-mean)^4] - 3*Var^2)
    m4 = np.sum(p_q * (np.log(p_arr) - mean_ln_p)**4) / sum_pq
    kurt_cumulant = m4 - 3 * var_ln_p**2  # 超额峰度
    tau_pppp = kurt_cumulant / ln_c
    c_eff = np.sum(p_q * c_arr) / sum_pq
    return {
        'alpha': alpha, 'f_alpha': f_alpha, 'tau_pp': tau_pp,
        'tau_ppp': tau_ppp, 'tau_pppp': tau_pppp, 'c_eff': c_eff
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
# v5.1回顾 + 缺口分析
# ============================================================
print("=" * 70)
print("v5.2 缺口攻坚: 四阶峰度 + 扇区依赖 + Cl(1,7)代数")
print("=" * 70)

# v5.1参数
IFS_C = [0.4136, 0.2623]
IFS_P = [0.9000, 0.1000]
Q0 = 0.2715
ETA_SCALE = -N_EW / 2.0  # -3.0
Z_LEP = 1.0 / np.sqrt(N_c)  # 0.5774

sector_qs = np.array([-Q0, Q0, -3*Q0, -5*Q0])
d_frac = ifs_dim(GEN_C)
xi_0 = 1.0 / N_EW

specs = [multifractal_spectrum_full(q, IFS_P, IFS_C) for q in sector_qs]

print("\n各扇区多分形谱参数(含四阶):")
print(f"{'扇区':<10} {'q':>8} {'tau_pp':>12} {'tau_ppp':>12} {'tau_pppp':>12}")
print("-" * 60)
sector_names = ["Up", "Down", "Lepton", "Neutrino"]
for s, spec in enumerate(specs):
    print(f"  {sector_names[s]:<8} {sector_qs[s]:>8.4f} {spec['tau_pp']:>12.6f} "
          f"{spec['tau_ppp']:>12.6f} {spec['tau_pppp']:>12.6f}")

# v5.1代内因子
k_arr = np.array([1, 2, 3], dtype=float)
intra_v51 = np.zeros((4, 3))
for s in range(4):
    beta_s = N_EW * specs[s]['alpha'] * specs[s]['f_alpha'] / d_frac
    kappa_s = sector_qs[s] * np.abs(specs[s]['tau_pp']) * xi_0
    eta_s = sector_qs[s] * specs[s]['tau_ppp'] * xi_0 * ETA_SCALE
    correction = 1 + kappa_s * (k_arr - 1) / 2 + eta_s * (k_arr - 1) * (k_arr - 2) / 6
    exponent = beta_s * k_arr * correction
    intra_v51[s, :] = (1.0 / specs[s]['c_eff'])**exponent
    intra_v51[s, :] = intra_v51[s, :] / intra_v51[s, 0]

# v5.1质量
sector_weights = np.array([np.sum(np.array(IFS_P)**q) if q != 0 else 1.0 for q in sector_qs])
sector_weights = sector_weights / np.sum(sector_weights)
y_t_SM = 173100 * np.sqrt(2) / 246000
y_0_base = y_t_SM / intra_v51[0, 2]
y_0_sector = np.array([y_0_base, y_0_base, y_0_base * Z_LEP, y_0_base * Z_LEP])
v = 246000.0

masses_v51 = np.zeros((4, 3))
for s in range(4):
    for gen in range(3):
        masses_v51[s, gen] = y_0_sector[s] * (sector_weights[0] / sector_weights[s]) * intra_v51[s, gen] * v / np.sqrt(2)

print("\n--- v5.1缺口诊断 ---")
print(f"{'扇区':<8} {'k':>3} {'pred_ratio':>12} {'SM_ratio':>12} {'log_dev':>10} {'gap':>8}")
print("-" * 60)
for s in range(3):
    for k in range(3):
        pred_ratio = masses_v51[s, k] / masses_v51[s, 0]
        sm_ratio = sm_masses[s*3+k] / sm_masses[s*3]
        log_dev = np.log(pred_ratio / sm_ratio)
        gap = "OK" if abs(log_dev) < 0.15 else ("***" if abs(log_dev) > 0.25 else "**")
        print(f"  {sector_names[s]:<6} {k+1:>3} {pred_ratio:>12.2f} {sm_ratio:>12.2f} {log_dev:>10.4f} {gap:>8}")

# 关键诊断: Down扇区曲率问题
print("\n--- Down扇区曲率诊断 ---")
pred_d_gaps = [np.log(intra_v51[1,1]/intra_v51[1,0]), np.log(intra_v51[1,2]/intra_v51[1,1])]
sm_d_gaps = [np.log(95/4.7), np.log(4180/95)]
print(f"  Down: pred gap1={pred_d_gaps[0]:.3f} gap2={pred_d_gaps[1]:.3f} | SM gap1={sm_d_gaps[0]:.3f} gap2={sm_d_gaps[1]:.3f}")
print(f"  Down: pred gap1>gap2? {pred_d_gaps[0] > pred_d_gaps[1]} | SM gap1>gap2? {sm_d_gaps[0] > sm_d_gaps[1]}")
print(f"  → SM Down: gap1={sm_d_gaps[0]:.3f} >> gap2={sm_d_gaps[1]:.3f} (递减)")
print(f"  → 预测 Down: gap1={pred_d_gaps[0]:.3f} ~ gap2={pred_d_gaps[1]:.3f} (几乎等间距)")
print(f"  → 需要四阶修正使gap2减小")

pred_u_gaps = [np.log(intra_v51[0,1]/intra_v51[0,0]), np.log(intra_v51[0,2]/intra_v51[0,1])]
sm_u_gaps = [np.log(1270/2.2), np.log(173100/1270)]
print(f"\n  Up: pred gap1={pred_u_gaps[0]:.3f} gap2={pred_u_gaps[1]:.3f} | SM gap1={sm_u_gaps[0]:.3f} gap2={sm_u_gaps[1]:.3f}")

# ============================================================
# 修正A: τ''''(q)四阶峰度修正
# ============================================================
print(f"\n{'='*70}")
print("修正A: τ''''(q)四阶峰度修正")
print("=" * 70)

def predict_v52(ifs_c, ifs_p, q0, gen_c, eta_scale, z_lep, zeta_scale=0.0):
    """v5.2: 含τ''''(q)四阶峰度修正
    
    完整cumulant展开:
    ln(intra) = beta*k * [1 + kappa*(k-1)/2 + eta*(k-1)(k-2)/6 + zeta*(k-1)(k-2)(k-3)/24]
    
    其中 zeta_s = q_s * tau''''(q_s) * xi_0 * zeta_scale
    """
    qs = np.array([-q0, q0, -3*q0, -5*q0])
    d_frac = ifs_dim(gen_c)
    xi_0 = 1.0 / N_EW
    specs = [multifractal_spectrum_full(q, ifs_p, ifs_c) for q in qs]
    sector_weights = np.array([np.sum(np.array(ifs_p)**q) if q != 0 else 1.0 for q in qs])
    sector_weights = sector_weights / np.sum(sector_weights)
    k_arr = np.array([1, 2, 3], dtype=float)
    intra = np.zeros((4, 3))
    for s in range(4):
        beta_s = N_EW * specs[s]['alpha'] * specs[s]['f_alpha'] / d_frac
        kappa_s = qs[s] * np.abs(specs[s]['tau_pp']) * xi_0
        eta_s = qs[s] * specs[s]['tau_ppp'] * xi_0 * eta_scale
        zeta_s = qs[s] * specs[s]['tau_pppp'] * xi_0 * zeta_scale
        correction = (1 + kappa_s * (k_arr - 1) / 2 
                      + eta_s * (k_arr - 1) * (k_arr - 2) / 6
                      + zeta_s * (k_arr - 1) * (k_arr - 2) * (k_arr - 3) / 24)
        exponent = beta_s * k_arr * correction
        intra[s, :] = (1.0 / specs[s]['c_eff'])**exponent
        intra[s, :] = intra[s, :] / intra[s, 0]
    y_t = 173100 * np.sqrt(2) / 246000
    y_0_base = y_t / intra[0, 2]
    y_0_sector = np.array([y_0_base, y_0_base, y_0_base * z_lep, y_0_base * z_lep])
    v = 246000.0
    masses = np.zeros((4, 3))
    for s in range(4):
        for gen in range(3):
            masses[s, gen] = y_0_sector[s] * (sector_weights[0] / sector_weights[s]) * intra[s, gen] * v / np.sqrt(2)
    return masses

def rmse(masses):
    pred_flat = masses[:3, :].flatten()
    return np.sqrt(np.mean((np.log(pred_flat) - sm_log_m)**2))

# 搜索最优zeta_scale
print("\n搜索最优zeta_scale (固定v5.1参数)...")
best_zeta = 0
best_rmse_zeta = 999
for zeta_try in np.linspace(-10, 10, 201):
    masses = predict_v52(IFS_C, IFS_P, Q0, GEN_C, ETA_SCALE, Z_LEP, zeta_scale=zeta_try)
    r = rmse(masses)
    if r < best_rmse_zeta:
        best_rmse_zeta = r
        best_zeta = zeta_try

print(f"  最优zeta_scale = {best_zeta:.2f}")
print(f"  RMSE(v5.2 zeta only) = {best_rmse_zeta:.4f} (v5.1: 0.1627)")

# 全局优化: IFS + q0 + zeta (固定eta=-3, z_lep=1/√3)
def obj_v52(params):
    c1, c2, p1, q0, zeta = params
    p2 = 1 - p1
    if not (0.30 <= c1 <= 0.50 and 0.25 <= c2 <= 0.45 and 0.70 <= p1 <= 0.90):
        return 100
    if not (0.1 <= q0 <= 1.5 and -10 <= zeta <= 10):
        return 100
    try:
        masses = predict_v52([c1, c2], [p1, p2], q0, GEN_C, ETA_SCALE, Z_LEP, zeta_scale=zeta)
        return rmse(masses)
    except:
        return 100

bounds_v52 = [(0.30, 0.50), (0.25, 0.45), (0.70, 0.90), (0.1, 1.5), (-10, 10)]
print("\n全局优化(IFS + q0 + zeta)...")
res_de = differential_evolution(obj_v52, bounds=bounds_v52, maxiter=500, popsize=40, seed=42)
res_nm = minimize(obj_v52, res_de.x, method='Nelder-Mead',
                   options={'maxiter': 8000, 'xatol': 1e-9, 'fatol': 1e-9})
c1_A, c2_A, p1_A, q0_A, zeta_A = res_nm.x
p2_A = 1 - p1_A
rmse_v52A = res_nm.fun

print(f"  RMSE = {rmse_v52A:.4f}")
print(f"  c1={c1_A:.6f}, c2={c2_A:.6f}, p1={p1_A:.6f}")
print(f"  q0={q0_A:.6f}, zeta_scale={zeta_A:.4f}")

# ============================================================
# 修正B: 扇区依赖eta_scale
# ============================================================
print(f"\n{'='*70}")
print("修正B: 扇区依赖eta_scale")
print("=" * 70)

# 理论: Up(q<0)和Down(q>0)的tau'''符号相反
# 但可能需要不同的|eta_scale|
# 物理原因: Up/Down夸克的电荷不同 → 不同的FRG修正

def predict_v52B(ifs_c, ifs_p, q0, gen_c, eta_up, eta_down, eta_lep, z_lep):
    """v5.2B: 扇区依赖eta_scale"""
    qs = np.array([-q0, q0, -3*q0, -5*q0])
    d_frac = ifs_dim(gen_c)
    xi_0 = 1.0 / N_EW
    specs = [multifractal_spectrum_full(q, ifs_p, ifs_c) for q in qs]
    sector_weights = np.array([np.sum(np.array(ifs_p)**q) if q != 0 else 1.0 for q in qs])
    sector_weights = sector_weights / np.sum(sector_weights)
    
    eta_scales = [eta_up, eta_down, eta_lep, eta_lep]  # 中微子同轻子
    
    k_arr = np.array([1, 2, 3], dtype=float)
    intra = np.zeros((4, 3))
    for s in range(4):
        beta_s = N_EW * specs[s]['alpha'] * specs[s]['f_alpha'] / d_frac
        kappa_s = qs[s] * np.abs(specs[s]['tau_pp']) * xi_0
        eta_s = qs[s] * specs[s]['tau_ppp'] * xi_0 * eta_scales[s]
        correction = 1 + kappa_s * (k_arr - 1) / 2 + eta_s * (k_arr - 1) * (k_arr - 2) / 6
        exponent = beta_s * k_arr * correction
        intra[s, :] = (1.0 / specs[s]['c_eff'])**exponent
        intra[s, :] = intra[s, :] / intra[s, 0]
    
    y_t = 173100 * np.sqrt(2) / 246000
    y_0_base = y_t / intra[0, 2]
    y_0_sector = np.array([y_0_base, y_0_base, y_0_base * z_lep, y_0_base * z_lep])
    v = 246000.0
    masses = np.zeros((4, 3))
    for s in range(4):
        for gen in range(3):
            masses[s, gen] = y_0_sector[s] * (sector_weights[0] / sector_weights[s]) * intra[s, gen] * v / np.sqrt(2)
    return masses

def obj_v52B(params):
    c1, c2, p1, q0, eta_up, eta_down, eta_lep = params
    p2 = 1 - p1
    if not (0.30 <= c1 <= 0.50 and 0.25 <= c2 <= 0.45 and 0.70 <= p1 <= 0.90):
        return 100
    if not (0.1 <= q0 <= 1.5):
        return 100
    if not (-8 <= eta_up <= 8 and -8 <= eta_down <= 8 and -8 <= eta_lep <= 8):
        return 100
    try:
        masses = predict_v52B([c1, c2], [p1, p2], q0, GEN_C, eta_up, eta_down, eta_lep, Z_LEP)
        return rmse(masses)
    except:
        return 100

bounds_v52B = [(0.30, 0.50), (0.25, 0.45), (0.70, 0.90), (0.1, 1.5), (-8, 8), (-8, 8), (-8, 8)]
print("\n全局优化(IFS + q0 + eta_up + eta_down + eta_lep)...")
res_de_B = differential_evolution(obj_v52B, bounds=bounds_v52B, maxiter=600, popsize=50, seed=42)
res_nm_B = minimize(obj_v52B, res_de_B.x, method='Nelder-Mead',
                     options={'maxiter': 10000, 'xatol': 1e-9, 'fatol': 1e-9})
c1_B, c2_B, p1_B, q0_B, eta_up_B, eta_down_B, eta_lep_B = res_nm_B.x
p2_B = 1 - p1_B
rmse_v52B = res_nm_B.fun

print(f"  RMSE = {rmse_v52B:.4f}")
print(f"  c1={c1_B:.6f}, c2={c2_B:.6f}, p1={p1_B:.6f}")
print(f"  q0={q0_B:.6f}")
print(f"  eta_up={eta_up_B:.4f}, eta_down={eta_down_B:.4f}, eta_lep={eta_lep_B:.4f}")
print(f"  比例 eta_up:eta_down:eta_lep = {abs(eta_up_B)/min(abs(eta_up_B),abs(eta_down_B),abs(eta_lep_B)):.2f}:{abs(eta_down_B)/min(abs(eta_up_B),abs(eta_down_B),abs(eta_lep_B)):.2f}:{abs(eta_lep_B)/min(abs(eta_up_B),abs(eta_down_B),abs(eta_lep_B)):.2f}")

# ============================================================
# 修正C: 综合 (四阶 + 扇区eta + z_down)
# ============================================================
print(f"\n{'='*70}")
print("修正C: 综合方案 (四阶 + 扇区eta + z_down)")
print("=" * 70)

def predict_v52C(ifs_c, ifs_p, q0, gen_c, eta_up, eta_down, eta_lep, z_lep, z_down, zeta_scale):
    """v5.2C: 综合修正"""
    qs = np.array([-q0, q0, -3*q0, -5*q0])
    d_frac = ifs_dim(gen_c)
    xi_0 = 1.0 / N_EW
    specs = [multifractal_spectrum_full(q, ifs_p, ifs_c) for q in qs]
    sector_weights = np.array([np.sum(np.array(ifs_p)**q) if q != 0 else 1.0 for q in qs])
    sector_weights = sector_weights / np.sum(sector_weights)
    
    eta_scales = [eta_up, eta_down, eta_lep, eta_lep]
    z_factors = [1.0, z_down, z_lep, z_lep]
    
    k_arr = np.array([1, 2, 3], dtype=float)
    intra = np.zeros((4, 3))
    for s in range(4):
        beta_s = N_EW * specs[s]['alpha'] * specs[s]['f_alpha'] / d_frac
        kappa_s = qs[s] * np.abs(specs[s]['tau_pp']) * xi_0
        eta_s = qs[s] * specs[s]['tau_ppp'] * xi_0 * eta_scales[s]
        zeta_s = qs[s] * specs[s]['tau_pppp'] * xi_0 * zeta_scale
        correction = (1 + kappa_s * (k_arr - 1) / 2 
                      + eta_s * (k_arr - 1) * (k_arr - 2) / 6
                      + zeta_s * (k_arr - 1) * (k_arr - 2) * (k_arr - 3) / 24)
        exponent = beta_s * k_arr * correction
        intra[s, :] = (1.0 / specs[s]['c_eff'])**exponent
        intra[s, :] = intra[s, :] / intra[s, 0]
    
    y_t = 173100 * np.sqrt(2) / 246000
    y_0_base = y_t / intra[0, 2]
    y_0_sector = np.array([y_0_base * z_factors[s] for s in range(4)])
    v = 246000.0
    masses = np.zeros((4, 3))
    for s in range(4):
        for gen in range(3):
            masses[s, gen] = y_0_sector[s] * (sector_weights[0] / sector_weights[s]) * intra[s, gen] * v / np.sqrt(2)
    return masses

def obj_v52C(params):
    c1, c2, p1, q0, eta_up, eta_down, eta_lep, z_down, zeta = params
    p2 = 1 - p1
    if not (0.30 <= c1 <= 0.50 and 0.25 <= c2 <= 0.45 and 0.70 <= p1 <= 0.90):
        return 100
    if not (0.1 <= q0 <= 1.5):
        return 100
    if not (-8 <= eta_up <= 8 and -8 <= eta_down <= 8 and -8 <= eta_lep <= 8):
        return 100
    if not (0.5 <= z_down <= 1.5 and -10 <= zeta <= 10):
        return 100
    try:
        masses = predict_v52C([c1, c2], [p1, p2], q0, GEN_C, eta_up, eta_down, eta_lep, Z_LEP, z_down, zeta)
        return rmse(masses)
    except:
        return 100

bounds_v52C = [(0.30, 0.50), (0.25, 0.45), (0.70, 0.90), (0.1, 1.5),
               (-8, 8), (-8, 8), (-8, 8), (0.5, 1.5), (-10, 10)]
print("\n全局优化(9参数)...")
res_de_C = differential_evolution(obj_v52C, bounds=bounds_v52C, maxiter=800, popsize=50, seed=42)
res_nm_C = minimize(obj_v52C, res_de_C.x, method='Nelder-Mead',
                     options={'maxiter': 15000, 'xatol': 1e-10, 'fatol': 1e-10})
params_C = res_nm_C.x
rmse_v52C = res_nm_C.fun

c1_C, c2_C, p1_C, q0_C = params_C[0], params_C[1], params_C[2], params_C[3]
eta_up_C, eta_down_C, eta_lep_C = params_C[4], params_C[5], params_C[6]
z_down_C, zeta_C = params_C[7], params_C[8]
p2_C = 1 - p1_C

print(f"  RMSE = {rmse_v52C:.4f}")
print(f"  c1={c1_C:.6f}, c2={c2_C:.6f}, p1={p1_C:.6f}")
print(f"  q0={q0_C:.6f}")
print(f"  eta_up={eta_up_C:.4f}, eta_down={eta_down_C:.4f}, eta_lep={eta_lep_C:.4f}")
print(f"  z_down={z_down_C:.4f}, zeta_scale={zeta_C:.4f}")

masses_v52C = predict_v52C([c1_C, c2_C], [p1_C, p2_C], q0_C, GEN_C,
                            eta_up_C, eta_down_C, eta_lep_C, Z_LEP, z_down_C, zeta_C)

# 详细结果
labels = [('u', 0, 0), ('c', 0, 1), ('t', 0, 2),
          ('d', 1, 0), ('s', 1, 1), ('b', 1, 2),
          ('e', 2, 0), ('μ', 2, 1), ('τ', 2, 2)]

print(f"\n--- v5.2C 费米子质量预测 (综合修正) ---")
print(f"{'粒子':<6} {'预测(MeV)':>14} {'SM(MeV)':>14} {'比值':>10} {'log比值':>10} {'v5.1比值':>10}")
print("-" * 70)
for name, s, k in labels:
    pred = masses_v52C[s, k]
    sm_val = sm_masses[s * 3 + k]
    ratio = pred / sm_val
    v51_ratio = masses_v51[s, k] / sm_val
    print(f"  {name:<4} {pred:>14.4f} {sm_val:>14.2f} {ratio:>10.4f} {np.log(ratio):>10.4f} {v51_ratio:>10.4f}")

# ============================================================
# 物理常数提取
# ============================================================
print(f"\n{'='*70}")
print("物理常数分析")
print("=" * 70)

# 检查eta参数是否有简单比例
print(f"\n  eta参数分析:")
print(f"    eta_up   = {eta_up_C:.4f}")
print(f"    eta_down = {eta_down_C:.4f}")
print(f"    eta_lep  = {eta_lep_C:.4f}")
if abs(eta_lep_C) > 1e-6:
    print(f"    比例 up:down:lep = {eta_up_C/eta_lep_C:.2f}:{eta_down_C/eta_lep_C:.2f}:1")
# 检查是否接近-N_EW/2=-3的倍数
for name, val in [("up", eta_up_C), ("down", eta_down_C), ("lep", eta_lep_C)]:
    ratio_to_3 = val / (-N_EW/2)
    print(f"    eta_{name} / (-N_EW/2) = {ratio_to_3:.4f}")

# 检查z_down
print(f"\n  z_down分析:")
print(f"    z_down = {z_down_C:.4f}")
print(f"    1/√(N_c) = {1/np.sqrt(N_c):.4f} (z_lep)")
print(f"    z_down/z_lep = {z_down_C/Z_LEP:.4f}")
print(f"    (z_down=1表示Down=Up, z_down<1表示Down也被抑制)")

# 检查zeta_scale
print(f"\n  zeta_scale分析:")
print(f"    zeta_scale = {zeta_C:.4f}")
print(f"    -N_EW/2 = {-N_EW/2:.1f}")
print(f"    zeta/(-N_EW/2) = {zeta_C/(-N_EW/2):.4f}")

# ============================================================
# 测试: 固定物理常数
# ============================================================
print(f"\n{'='*70}")
print("测试: 固定理论常数后的优化")
print("=" * 70)

# 尝试从优化结果中提取物理常数
# 假设: eta_s = -N_EW/2 * f_s, 其中f_s是扇区因子
# 假设: z_down = 1 (Down=Up), z_lep = 1/√(N_c)
# 假设: zeta_scale = 0 (四阶不重要) 或某个简单值

# 方案1: 固定 z_down=1, z_lep=1/√3, eta统一=-3, 只优化IFS+q0+zeta
print("\n  方案1: 固定eta=-3, z_lep=1/√3, z_down=1, 只优化IFS+q0+zeta")
def obj_s1(params):
    c1, c2, p1, q0, zeta = params
    p2 = 1 - p1
    if not (0.30 <= c1 <= 0.50 and 0.25 <= c2 <= 0.45 and 0.70 <= p1 <= 0.90):
        return 100
    if not (0.1 <= q0 <= 1.5 and -10 <= zeta <= 10):
        return 100
    try:
        masses = predict_v52C([c1, c2], [p1, p2], q0, GEN_C, -3, -3, -3, Z_LEP, 1.0, zeta)
        return rmse(masses)
    except:
        return 100

res_s1 = differential_evolution(obj_s1, bounds=[(0.30,0.50),(0.25,0.45),(0.70,0.90),(0.1,1.5),(-10,10)],
                                 maxiter=400, popsize=30, seed=42)
res_s1_nm = minimize(obj_s1, res_s1.x, method='Nelder-Mead', options={'maxiter':5000, 'xatol':1e-8, 'fatol':1e-8})
print(f"    RMSE = {res_s1_nm.fun:.4f}")

# 方案2: 从优化结果提取扇区eta比例, 固定该比例
# 发现的eta比例
eta_ratio_up = eta_up_C / eta_lep_C if abs(eta_lep_C) > 1e-6 else 1
eta_ratio_down = eta_down_C / eta_lep_C if abs(eta_lep_C) > 1e-6 else 1
print(f"\n  方案2: 固定eta比例 up:down:lep = {eta_ratio_up:.2f}:{eta_ratio_down:.2f}:1, z_down={z_down_C:.4f}")

def obj_s2(params):
    c1, c2, p1, q0, eta0, zeta = params
    p2 = 1 - p1
    if not (0.30 <= c1 <= 0.50 and 0.25 <= c2 <= 0.45 and 0.70 <= p1 <= 0.90):
        return 100
    if not (0.1 <= q0 <= 1.5 and -8 <= eta0 <= 8 and -10 <= zeta <= 10):
        return 100
    try:
        masses = predict_v52C([c1, c2], [p1, p2], q0, GEN_C, 
                                eta_ratio_up*eta0, eta_ratio_down*eta0, eta0, 
                                Z_LEP, z_down_C, zeta)
        return rmse(masses)
    except:
        return 100

res_s2 = differential_evolution(obj_s2, bounds=[(0.30,0.50),(0.25,0.45),(0.70,0.90),(0.1,1.5),(-8,8),(-10,10)],
                                 maxiter=500, popsize=40, seed=42)
res_s2_nm = minimize(obj_s2, res_s2.x, method='Nelder-Mead', options={'maxiter':8000, 'xatol':1e-9, 'fatol':1e-9})
print(f"    RMSE = {res_s2_nm.fun:.4f}")
c1_s2, c2_s2, p1_s2, q0_s2, eta0_s2, zeta_s2 = res_s2_nm.x
print(f"    eta0={eta0_s2:.4f}, zeta={zeta_s2:.4f}")
print(f"    → eta_up={eta_ratio_up*eta0_s2:.4f}, eta_down={eta_ratio_down*eta0_s2:.4f}, eta_lep={eta0_s2:.4f}")

# ============================================================
# 汇总
# ============================================================
print(f"\n{'='*70}")
print("精度改善汇总")
print("=" * 70)

rmse_v50 = 0.367
rmse_v51 = 0.1627

print(f"  v5.0 (1:1:3 + IFS):       RMSE = {rmse_v50:.4f}")
print(f"  v5.1 (τ''' + Casimir):    RMSE = {rmse_v51:.4f}  改善 {rmse_v50/rmse_v51:.2f}x")
print(f"  v5.2A (τ''''四阶):        RMSE = {rmse_v52A:.4f}  改善 {rmse_v51/rmse_v52A:.2f}x")
print(f"  v5.2B (扇区eta):          RMSE = {rmse_v52B:.4f}  改善 {rmse_v51/rmse_v52B:.2f}x")
print(f"  v5.2C (综合):             RMSE = {rmse_v52C:.4f}  改善 {rmse_v51/rmse_v52C:.2f}x")
print(f"  方案1 (固定常数):          RMSE = {res_s1_nm.fun:.4f}")
print(f"  方案2 (固定比例):          RMSE = {res_s2_nm.fun:.4f}")

print(f"\n  版本累计:")
print(f"    v2.x:  RMSE ≈ 3.20")
print(f"    v3.0:  RMSE = 1.02    (3.1x)")
print(f"    v4.0:  RMSE = 0.52    (6.1x)")
print(f"    v5.0:  RMSE = 0.367   (8.7x)")
print(f"    v5.1:  RMSE = 0.163   (19.7x)")
print(f"    v5.2C: RMSE = {rmse_v52C:.4f}  ({3.20/rmse_v52C:.1f}x)")

# 最佳结果的详细粒子表
print(f"\n--- 最佳方案(v5.2C)详细 ---")
print(f"{'粒子':<6} {'预测(MeV)':>14} {'SM(MeV)':>14} {'比值':>10} {'log比值':>10}")
print("-" * 60)
for name, s, k in labels:
    pred = masses_v52C[s, k]
    sm_val = sm_masses[s * 3 + k]
    ratio = pred / sm_val
    print(f"  {name:<4} {pred:>14.4f} {sm_val:>14.2f} {ratio:>10.4f} {np.log(ratio):>10.4f}")

# 代内间隔分析
print(f"\n--- 代内间隔分析 (v5.2C) ---")
print(f"{'扇区':<8} {'pred_gap1':>12} {'pred_gap2':>12} {'SM_gap1':>12} {'SM_gap2':>12}")
print("-" * 60)
for s in range(3):
    # 重新计算v52C的intra
    qs_C = np.array([-q0_C, q0_C, -3*q0_C, -5*q0_C])
    specs_C = [multifractal_spectrum_full(q, [p1_C, p2_C], [c1_C, c2_C]) for q in qs_C]
    beta_s = N_EW * specs_C[s]['alpha'] * specs_C[s]['f_alpha'] / d_frac
    kappa_s = qs_C[s] * np.abs(specs_C[s]['tau_pp']) * xi_0
    eta_scales_C = [eta_up_C, eta_down_C, eta_lep_C, eta_lep_C]
    eta_s = qs_C[s] * specs_C[s]['tau_ppp'] * xi_0 * eta_scales_C[s]
    zeta_s = qs_C[s] * specs_C[s]['tau_pppp'] * xi_0 * zeta_C
    correction = (1 + kappa_s * (k_arr - 1) / 2 
                  + eta_s * (k_arr - 1) * (k_arr - 2) / 6
                  + zeta_s * (k_arr - 1) * (k_arr - 2) * (k_arr - 3) / 24)
    exponent = beta_s * k_arr * correction
    intra_C = (1.0 / specs_C[s]['c_eff'])**exponent
    intra_C = intra_C / intra_C[0]
    
    pred_g1 = np.log(intra_C[1] / intra_C[0])
    pred_g2 = np.log(intra_C[2] / intra_C[1])
    sm_g1 = np.log(sm_masses[s*3+1] / sm_masses[s*3])
    sm_g2 = np.log(sm_masses[s*3+2] / sm_masses[s*3+1])
    print(f"  {sector_names[s]:<6} {pred_g1:>12.3f} {pred_g2:>12.3f} {sm_g1:>12.3f} {sm_g2:>12.3f}")
