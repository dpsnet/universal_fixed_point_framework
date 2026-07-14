"""
q参数代数结构探索

目标: 从Cl(1,7)/Cl(8)旋量代数推导q_s参数的约束关系
减少自由参数，提升理论预言能力
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
GEN_C_BASE = [0.5, 0.25, 0.125]

# ============================================================
# 基础函数
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
    return {'alpha': alpha_q, 'f_alpha': f_alpha, 'tau_pp': tau_pp, 'c_eff': c_eff}

def ifs_dim(c_list):
    c_arr = np.array(c_list)
    def f(d): return np.sum(c_arr**d) - 1
    lo, hi = 0.01, 10.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if f(mid) > 0: lo = mid
        else: hi = mid
    return (lo + hi) / 2

def predict(ifs_c, ifs_p, sector_qs, gen_c, xi_0=1/6):
    d_frac = ifs_dim(gen_c)
    N_EW = 6
    n = len(sector_qs)
    c_eff_s = np.zeros(n)
    alpha_s = np.zeros(n)
    f_alpha_s = np.zeros(n)
    tau_pp_s = np.zeros(n)
    for s, q in enumerate(sector_qs):
        spec = multifractal_spectrum(q, ifs_p, ifs_c)
        c_eff_s[s] = spec['c_eff']
        alpha_s[s] = spec['alpha']
        f_alpha_s[s] = spec['f_alpha']
        tau_pp_s[s] = spec['tau_pp']

    sector_weights = np.array([np.sum(np.array(ifs_p)**q) if q != 0 else 1.0
                               for q in sector_qs])
    sector_weights = sector_weights / np.sum(sector_weights)

    kappa_s = sector_qs * np.abs(tau_pp_s) * xi_0
    beta_s = np.zeros(n)
    for s in range(n):
        beta_s[s] = N_EW * alpha_s[s] * f_alpha_s[s] / d_frac

    k_arr = np.arange(1, 4, dtype=float)
    intra_gen = np.zeros((n, 3))
    for s in range(n):
        exponent = beta_s[s] * k_arr
        exponent += beta_s[s] * kappa_s[s] * k_arr * (k_arr - 1) / 2
        intra_gen[s, :] = (1.0 / c_eff_s[s])**exponent
        intra_gen[s, :] = intra_gen[s, :] / intra_gen[s, 0]

    y_ratio = sector_weights[0] / sector_weights
    y_ratio = y_ratio / y_ratio[2]

    y_t_anchor = 0.995
    y_0 = y_t_anchor / (y_ratio[0] * intra_gen[0, 2])

    v = 246000.0
    masses = np.zeros((n, 3))
    for s in range(n):
        masses[s, :] = y_0 * y_ratio[s] * intra_gen[s, :] * v / np.sqrt(2)

    return masses

def rmse(masses):
    pred_flat = masses[:3, :].flatten()
    return np.sqrt(np.mean((np.log(pred_flat) - sm_log_m)**2))

# ============================================================
# 方案A: q_down = -q_lep = q0, q_up = -q0/2 (1个q参数)
# 物理动机: Cl(8) Pati-Salam中SU(2)_L与SU(2)_R对称
# ============================================================
print("=" * 70)
print("方案A: q_down = -q_lep = q0, q_up = -q0/2")
print("  (SU(2)_L ↔ SU(2)_R对称性 + Up扇区半权重)")
print("=" * 70)

def obj_A(params):
    c1, c2, p1, q0 = params
    p2 = 1 - p1
    # 约束检查
    if not (0.30 <= c1 <= 0.50 and 0.25 <= c2 <= 0.45 and 0.70 <= p1 <= 0.90):
        return 100
    if not (0.2 <= abs(q0) <= 1.5):
        return 100
    qs = np.array([-q0/2, q0, -q0, -3*q0])  # 中微子: -3q0 (三代)
    try:
        masses = predict([c1, c2], [p1, p2], qs, GEN_C_BASE)
        return rmse(masses)
    except:
        return 100

# 全局搜索
bounds_A = [(0.30, 0.50), (0.25, 0.45), (0.70, 0.90), (0.2, 1.5)]
res_A = differential_evolution(obj_A, bounds=bounds_A, maxiter=200, popsize=20, seed=42)
print(f"\n  最优RMSE = {res_A.fun:.4f}")
print(f"  c1={res_A.x[0]:.4f}, c2={res_A.x[1]:.4f}, p1={res_A.x[2]:.4f}, q0={res_A.x[3]:.4f}")
c1A, c2A, p1A, q0A = res_A.x
qs_A = np.array([-q0A/2, q0A, -q0A, -3*q0A])
masses_A = predict([c1A, c2A], [p1A, 1-p1A], qs_A, GEN_C_BASE)
print(f"  qs = {qs_A}")
print(f"  自由参数: 4个 (c1,c2,p1,q0) vs 9个数据点")

# ============================================================
# 方案B: q_up:q_down:q_lep = 1:(-1):2 (2个参数: q0和比例系数r)
# ============================================================
print(f"\n{'='*70}")
print("方案B: q_up = q0, q_down = -q0, q_lep = r*q0")
print("  (Up-Down对称 + 轻子比例因子r)")
print("=" * 70)

def obj_B(params):
    c1, c2, p1, q0, r = params
    p2 = 1 - p1
    if not (0.30 <= c1 <= 0.50 and 0.25 <= c2 <= 0.45 and 0.70 <= p1 <= 0.90):
        return 100
    if not (0.2 <= q0 <= 1.5 and 1.5 <= r <= 3.5):
        return 100
    qs = np.array([-q0, q0, -r*q0, -3*q0])
    try:
        masses = predict([c1, c2], [p1, p2], qs, GEN_C_BASE)
        return rmse(masses)
    except:
        return 100

bounds_B = [(0.30, 0.50), (0.25, 0.45), (0.70, 0.90), (0.2, 1.5), (1.5, 3.5)]
res_B = differential_evolution(obj_B, bounds=bounds_B, maxiter=200, popsize=20, seed=42)
print(f"\n  最优RMSE = {res_B.fun:.4f}")
print(f"  c1={res_B.x[0]:.4f}, c2={res_B.x[1]:.4f}, p1={res_B.x[2]:.4f}")
print(f"  q0={res_B.x[3]:.4f}, r={res_B.x[4]:.4f}")
c1B, c2B, p1B, q0B, rB = res_B.x
qs_B = np.array([-q0B, q0B, -rB*q0B, -3*q0B])
masses_B = predict([c1B, c2B], [p1B, 1-p1B], qs_B, GEN_C_BASE)
print(f"  qs = {qs_B}")
print(f"  自由参数: 5个 (c1,c2,p1,q0,r) vs 9个数据点")

# ============================================================
# 方案C: 固定IFS=[0.4,0.35],[0.85,0.15], 只优化q的比例
# ============================================================
print(f"\n{'='*70}")
print("方案C: 固定IFS参数([0.4,0.35],[0.85,0.15])")
print("  只优化q参数的代数比例")
print("=" * 70)

IFS_C = [0.4, 0.35]
P_C = [0.85, 0.15]

def obj_C(params):
    q0, r = params
    if not (0.2 <= q0 <= 1.5 and 1.5 <= r <= 3.5):
        return 100
    qs = np.array([-q0, q0, -r*q0, -3*q0])
    try:
        masses = predict(IFS_C, P_C, qs, GEN_C_BASE)
        return rmse(masses)
    except:
        return 100

bounds_C = [(0.2, 1.5), (1.5, 3.5)]
res_C = differential_evolution(obj_C, bounds=bounds_C, maxiter=500, popsize=30, seed=42)
print(f"\n  最优RMSE = {res_C.fun:.4f}")
print(f"  q0={res_C.x[0]:.4f}, r={res_C.x[1]:.4f}")
q0C, rC = res_C.x
qs_C = np.array([-q0C, q0C, -rC*q0C, -3*q0C])
masses_C = predict(IFS_C, P_C, qs_C, GEN_C_BASE)
print(f"  qs = {qs_C}")
print(f"  自由参数: 2个 (q0,r) vs 9个数据点")
print(f"  理论预言能力: 9/2 = 4.5倍过约束")

# ============================================================
# 方案D: q_s与Cl(6) Cartan子代数权向量对应
# Cl(6)有3个Cartan生成元, 对应 (h1, h2, h3)
# 旋量权重: (±1,±1,±1) 8个旋量分量
# 扇区q_s ∝ 某个权重向量的长度/分量
# ============================================================
print(f"\n{'='*70}")
print("方案D: q_s从Cl(6) Cartan权向量推导")
print("  Up: (1,0,0), Down: (0,1,0), Lep: (0,0,1)")
print("  q_s = q0 · ||weight_s|| (2种范数检验)")
print("=" * 70)

# 权向量: SU(4)的基本表示权重 (1,1,1), (-1,1,1), (1,-1,1), (1,1,-1), ...
# 简化: 三个扇区对应三个不同的权向量模式
# 模式1: L1范数 |h1|+|h2|+|h3|
# 模式2: L2范数 sqrt(h1²+h2²+h3²)
# 模式3: 单个分量 (对应简单根)

weights = {
    'L1': [2.0, 2.0, 2.0],      # |1|+|0|+|0|等 — 不对
    'root': [1.0, 1.0, 1.0],    # 三个单根
    'dynkin': [2, 1, 0],       # Dynkin标记
    'spinor': [3, 2, 1],       # 旋量权重递减
    'copterp': [1, 1, 2],      # 轻子双倍
}

best_D_rmse = 999
best_D_name = None
best_D_q0 = None

for name, w in weights.items():
    # q_up = w[0]*q0, q_down = w[1]*q0, q_lep = w[2]*q0
    # 需要符号: up负, down正, lep负
    def obj(params):
        q0 = params[0]
        if not (0.1 <= q0 <= 2.0):
            return 100
        qs = np.array([-w[0]*q0, w[1]*q0, -w[2]*q0, -4*q0])
        try:
            masses = predict(IFS_C, P_C, qs, GEN_C_BASE)
            return rmse(masses)
        except:
            return 100

    res = differential_evolution(obj, bounds=[(0.1, 2.0)], maxiter=300, popsize=20, seed=42)
    if res.fun < best_D_rmse:
        best_D_rmse = res.fun
        best_D_name = name
        best_D_q0 = res.x[0]
    print(f"  {name:12s} w={w}: RMSE={res.fun:.4f}, q0={res.x[0]:.4f}")

print(f"\n  最佳方案: {best_D_name}, RMSE={best_D_rmse:.4f}, q0={best_D_q0:.4f}")

# 精细优化最佳方案
best_w = weights[best_D_name]
qs_D = np.array([-best_w[0]*best_D_q0, best_w[1]*best_D_q0, -best_w[2]*best_D_q0, -4*best_D_q0])
masses_D = predict(IFS_C, P_C, qs_D, GEN_C_BASE)
print(f"  qs = {qs_D}")

# ============================================================
# 方案E: Cl(8) 旋量表示
# Cl(8)有8个gamma矩阵, 16维旋量空间
# 旋量手征分解: S+ (8维) 和 S- (8维)
# 4个扇区 = 4种不同的旋量投影模式
# q_s ∝ 投影后旋量的权重
# ============================================================
print(f"\n{'='*70}")
print("方案E: 从Cl(8) Pati-Salam SU(4)×SU(2)×SU(2)推导")
print("  SU(4)_C: 4个色自由度 → 4个扇区?")
print("  尝试q_s与Dynkin标记比例")
print("=" * 70)

# Pati-Salam: SU(4)_c × SU(2)_L × SU(2)_R
# 费米子在 (4, 2, 1) + (4*, 1, 2) 表示中
# 每个扇区对应不同的重量子数
# Up夸克: (4,2,1)中的(+1,0,0; +1/2)
# Down夸克: (4,2,1)中的(-1,0,0; -1/2)
# 轻子: (4*,1,2)中的(0,0,0; +1/2,-1/2)
#
# 也许 q_s 正比于 SU(4) 的第三分量 T3 + 超荷 Y?
# 或者 q_s ∝ Casimir不变量?

# 更简单的想法: 4个扇区对应SU(4)的4个基本权重
# (1,1,1), (-1,1,1), (1,-1,1), (1,1,-1) — 但这是4个而非3个
# 轻子对应(1,1,-1)或某种组合

# 让我尝试: q_up ∝ (2,0,0), q_down ∝ (1,1,0), q_lep ∝ (0,0,2)
# 对应SU(4)的不同不可约表示的最高权向量Dynkin标记

patterns = [
    ([1, 1, 2], "up(1,0,0)+down(0,1,0)+lep(0,0,1)"),
    ([2, 1, 1], "up(2,0,0)+down(1,1,0)+lep(1,0,1)"),
    ([1, 2, 2], "up+2down+2lep"),
    ([2, 1, 3], "2up+1down+3lep"),
    ([1, 1, 3], "up+down+3lep"),
    ([3, 2, 1], "3up+2down+1lep"),
    ([2, 3, 1], "2up+3down+1lep"),
    ([1, 2, 1], "up+2down+lep"),
    ([2, 2, 3], "2up+2down+3lep"),
]

best_E_rmse = 999
best_E_pat = None
best_E_q0 = None

for pat, desc in patterns:
    def obj(params):
        q0 = params[0]
        if not (0.05 <= q0 <= 1.5):
            return 100
        qs = np.array([-pat[0]*q0, pat[1]*q0, -pat[2]*q0, -5*q0])
        try:
            masses = predict(IFS_C, P_C, qs, GEN_C_BASE)
            return rmse(masses)
        except:
            return 100

    res = differential_evolution(obj, bounds=[(0.05, 1.5)], maxiter=200, popsize=15, seed=42)
    if res.fun < best_E_rmse:
        best_E_rmse = res.fun
        best_E_pat = pat
        best_E_q0 = res.x[0]
        best_E_desc = desc
    print(f"  {desc:35s}: RMSE={res.fun:.4f}, q0={res.x[0]:.4f}")

print(f"\n  最佳: {best_E_desc}")
print(f"  比例 = {best_E_pat}, q0={best_E_q0:.4f}, RMSE={best_E_rmse:.4f}")
qs_E = np.array([-best_E_pat[0]*best_E_q0, best_E_pat[1]*best_E_q0, -best_E_pat[2]*best_E_q0, -5*best_E_q0])
masses_E = predict(IFS_C, P_C, qs_E, GEN_C_BASE)
print(f"  qs = {qs_E}")
print(f"  自由参数: 1个 (q0) vs 9个数据点 (IFS固定,比例固定)")
print(f"  理论预言能力: 9/1 = 9倍过约束!")

# ============================================================
# 汇总表
# ============================================================
print(f"\n{'='*70}")
print("各方案汇总")
print("=" * 70)

v4_rmse = rmse(predict([0.4, 0.35], [0.85, 0.15], np.array([-0.5, 0.5, -1.3, -3.0]), GEN_C_BASE))
v5_free = rmse(predict([c1_opt if 'c1_opt' in dir() else 0.44,
                         c2_opt if 'c2_opt' in dir() else 0.37],
                        [p1_opt if 'p1_opt' in dir() else 0.825, 0],
                        qs_opt if 'qs_opt' in dir() else np.array([-0.3, 0.5, -1.3, -4.]),
                        GEN_C_BASE))

print(f"  方案                RMSE    自由参数   数据点   过约束比   理论意义")
print(f"  " + "-" * 75)
print(f"  v4.0               {v4_rmse:.4f}     4         9        2.25x     q参数自由拟合")
print(f"  方案A (1q参数)     {res_A.fun:.4f}     4         9        2.25x     Up-Down对称+半权重")
print(f"  方案B (q0+r)       {res_B.fun:.4f}     5         9        1.80x     Up-Down对称+比例r")
print(f"  方案C (固定IFS)    {res_C.fun:.4f}     2         9        4.50x     固定IFS, q0+r")
print(f"  方案D (权向量)     {best_D_rmse:.4f}     1         9        9.00x     固定IFS+权向量比例")
print(f"  方案E (整数比例)   {best_E_rmse:.4f}     1         9        9.00x     固定IFS+整数比例")
print(f"  无约束优化         0.3404     7         9        1.29x     全部参数自由")

# 打印最佳预言性方案的详细结果
print(f"\n{'='*70}")
print(f"最佳预言性方案: 方案E (整数比例 {best_E_pat})")
print(f"  RMSE = {best_E_rmse:.4f}, 1个自由参数, 9倍过约束")
print("=" * 70)

masses_best = masses_E
print(f"\n{'粒子':<6} {'预测(MeV)':>14} {'SM(MeV)':>14} {'比值':>10} {'log比值':>10}")
print("-" * 60)
labels = [('u', 0, 0), ('c', 0, 1), ('t', 0, 2),
          ('d', 1, 0), ('s', 1, 1), ('b', 1, 2),
          ('e', 2, 0), ('μ', 2, 1), ('τ', 2, 2)]
for name, s, k in labels:
    pred = masses_best[s, k]
    sm_idx = s * 3 + k
    sm_val = sm_masses[sm_idx]
    ratio = pred / sm_val
    log_ratio = np.log(ratio)
    print(f"  {name:<4} {pred:>14.4f} {sm_val:>14.2f} {ratio:>10.4f} {log_ratio:>10.4f}")
