"""
z_down理论值验证: 固定z_down后重新优化其他参数

验证方案:
  方案A: 固定z_down=0.6863(严格RG推导), 优化IFS+q0+eta+zeta
  方案B: 固定z_down=0.72(目标值), 优化IFS+q0+eta+zeta
  方案C: 固定z_down=0.8895(v5.2优化值), 优化其他参数(基准)

比较三种方案的RMSE差异,验证理论推导的正确性
"""
import numpy as np
from scipy.optimize import differential_evolution, minimize

# SM基准数据
sm_masses = np.array([2.2, 1270.0, 173100.0, 4.7, 95.0, 4180.0, 0.511, 105.66, 1776.86])
sm_log_m = np.log(sm_masses)

GEN_C = [0.5, 0.25, 0.125]
N_c = 3
N_EW = 6
Z_LEP = 1.0 / np.sqrt(N_c)

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
    var_ln_p = np.sum(p_q * (np.log(p_arr))**2) / sum_pq - mean_ln_p**2
    tau_pp = var_ln_p / ln_c
    skew_ln_p = np.sum(p_q * (np.log(p_arr) - mean_ln_p)**3) / sum_pq
    tau_ppp = skew_ln_p / ln_c
    m4 = np.sum(p_q * (np.log(p_arr) - mean_ln_p)**4) / sum_pq
    kurt_cumulant = m4 - 3 * var_ln_p**2
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

def predict_with_z_down(ifs_c, ifs_p, q0, gen_c, eta_up, eta_down, eta_lep, z_lep, z_down_fixed, zeta_scale):
    qs = np.array([-q0, q0, -3*q0, -5*q0])
    d_frac = ifs_dim(gen_c)
    xi_0 = 1.0 / N_EW
    specs = [multifractal_spectrum_full(q, ifs_p, ifs_c) for q in qs]
    sector_weights = np.array([np.sum(np.array(ifs_p)**q) if q != 0 else 1.0 for q in qs])
    sector_weights = sector_weights / np.sum(sector_weights)
    
    eta_scales = [eta_up, eta_down, eta_lep, eta_lep]
    z_factors = [1.0, z_down_fixed, z_lep, z_lep]
    
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

def rmse(masses):
    pred_flat = masses[:3, :].flatten()
    return np.sqrt(np.mean((np.log(pred_flat) - sm_log_m)**2))

def optimize_with_fixed_z(z_down_fixed, label):
    def objective(params):
        c1, c2, p1, q0, eta_up, eta_down, eta_lep, zeta = params
        p2 = 1 - p1
        if not (0.30 <= c1 <= 0.50 and 0.25 <= c2 <= 0.45 and 0.70 <= p1 <= 0.90):
            return 100
        if not (0.1 <= q0 <= 1.5):
            return 100
        if not (-8 <= eta_up <= 8 and -8 <= eta_down <= 8 and -8 <= eta_lep <= 8):
            return 100
        if not (-10 <= zeta <= 10):
            return 100
        try:
            masses = predict_with_z_down([c1, c2], [p1, p2], q0, GEN_C,
                                         eta_up, eta_down, eta_lep, Z_LEP, z_down_fixed, zeta)
            return rmse(masses)
        except:
            return 100
    
    bounds = [(0.30, 0.50), (0.25, 0.45), (0.70, 0.90), (0.1, 1.5),
              (-8, 8), (-8, 8), (-8, 8), (-10, 10)]
    
    print(f"\n优化{label} (z_down={z_down_fixed:.4f})...")
    res_de = differential_evolution(objective, bounds, maxiter=600, popsize=40, seed=42)
    res_nm = minimize(objective, res_de.x, method='Nelder-Mead',
                      options={'maxiter': 10000, 'xatol': 1e-10, 'fatol': 1e-10})
    
    c1, c2, p1, q0, eta_up, eta_down, eta_lep, zeta = res_nm.x
    p2 = 1 - p1
    
    masses = predict_with_z_down([c1, c2], [p1, p2], q0, GEN_C,
                                 eta_up, eta_down, eta_lep, Z_LEP, z_down_fixed, zeta)
    
    return {
        'rmse': res_nm.fun,
        'params': {'c1': c1, 'c2': c2, 'p1': p1, 'p2': p2, 'q0': q0,
                   'eta_up': eta_up, 'eta_down': eta_down, 'eta_lep': eta_lep, 'zeta': zeta},
        'masses': masses
    }

print("=" * 75)
print("z_down理论值验证: 固定z_down后重新优化其他参数")
print("=" * 75)

print("\n【验证方案】")
print("  方案A: z_down=0.6863 (严格RG跑动方程推导)")
print("  方案B: z_down=0.72 (目标值)")
print("  方案C: z_down=0.8895 (v5.2优化值 - 基准)")

results = {}

results['A'] = optimize_with_fixed_z(0.6863, "方案A")
results['B'] = optimize_with_fixed_z(0.72, "方案B")
results['C'] = optimize_with_fixed_z(0.8895, "方案C")

print("\n" + "=" * 75)
print("【验证结果对比】")
print("=" * 75)

print("  {:<8} {:<12} {:<10} {:<12}".format('方案', 'z_down', 'RMSE', 'RMSE变化'))
print("-" * 45)
for key in ['A', 'B', 'C']:
    rmse_val = results[key]['rmse']
    rmse_change = (rmse_val - results['C']['rmse']) / results['C']['rmse'] * 100
    z_down_val = 0.6863 if key == 'A' else (0.72 if key == 'B' else 0.8895)
    print("  {:<6} {:<12.4f} {:<10.4f} {:<12.2f}%".format(key+":", z_down_val, rmse_val, rmse_change))

print("\n【详细参数对比】")
for key in ['A', 'B', 'C']:
    z_down_val = 0.6863 if key == 'A' else (0.72 if key == 'B' else 0.8895)
    print(f"\n方案{key} (z_down={z_down_val:.4f}):")
    p = results[key]['params']
    print(f"  IFS: c=[{p['c1']:.4f}, {p['c2']:.4f}], p=[{p['p1']:.4f}, {p['p2']:.4f}]")
    print(f"  q0 = {p['q0']:.4f}")
    print(f"  eta: up={p['eta_up']:.4f}, down={p['eta_down']:.4f}, lep={p['eta_lep']:.4f}")
    print(f"  zeta = {p['zeta']:.4f}")
    print(f"  RMSE = {results[key]['rmse']:.4f}")

print("\n" + "=" * 75)
print("【质量谱预测对比】")
print("=" * 75)

labels = [('u', 0, 0), ('c', 0, 1), ('t', 0, 2),
          ('d', 1, 0), ('s', 1, 1), ('b', 1, 2),
          ('e', 2, 0), ('μ', 2, 1), ('τ', 2, 2)]

print(f"\n{'粒子':<4} {'SM':>12} {'方案A':>12} {'方案B':>12} {'方案C':>12}")
print("-" * 55)
for name, s, gen in labels:
    sm_val = sm_masses[s*3 + gen]
    a_val = results['A']['masses'][s, gen]
    b_val = results['B']['masses'][s, gen]
    c_val = results['C']['masses'][s, gen]
    print(f"  {name:<4} {sm_val:>12.2f} {a_val:>12.2f} {b_val:>12.2f} {c_val:>12.2f}")

print("\n" + "=" * 75)
print("【结论】")
print("=" * 75)

rmse_A = results['A']['rmse']
rmse_B = results['B']['rmse']
rmse_C = results['C']['rmse']

print(f"\nRMSE对比:")
print(f"  方案A (z_down=0.6863): RMSE = {rmse_A:.4f}")
print(f"  方案B (z_down=0.72):   RMSE = {rmse_B:.4f}")
print(f"  方案C (z_down=0.8895): RMSE = {rmse_C:.4f}")

if rmse_A <= rmse_C * 1.1:
    print(f"\n✓ 理论推导验证通过:")
    print(f"  z_down=0.6863的RMSE({rmse_A:.4f})与基准({rmse_C:.4f})相比增加了{(rmse_A-rmse_C)/rmse_C*100:.2f}%")
    print(f"  增加幅度<10%, 理论推导正确")
else:
    print(f"\n✗ 理论推导需要修正:")
    print(f"  z_down=0.6863的RMSE({rmse_A:.4f})与基准({rmse_C:.4f})相比增加了{(rmse_A-rmse_C)/rmse_C*100:.2f}%")
    print(f"  增加幅度>10%, 需要重新审视理论推导")

print(f"\n理论推导公式:")
print(f"  z_down = √[(1+Q_down²)/(1+Q_up²)] × [C₂(SU(2))/C₂(SU(3))]^0.25")
print(f"  Q_up=2/3, Q_down=-1/3, C₂(SU(2))=1/2, C₂(SU(3))=4/3")
print(f"  z_down = {np.sqrt((1 + (1/3)**2)/(1 + (2/3)**2)) * (0.5/1.3333333333)**0.25:.6f}")

print("\n" + "=" * 75)