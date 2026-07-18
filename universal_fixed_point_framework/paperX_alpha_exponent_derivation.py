#!/usr/bin/env python3
"""
paperX_alpha_exponent_derivation.py — Direction 2: α 指数第一原理公式

假设: α(R) = ∫_{M_Z}^{M_Pl} γ_m(R, μ) d(ln μ)
γ_m(R) = 3C₂(R₃)α_s/π + 3/4 C₂(R₂)α₂/π + 3/4 Y²α₁/π

通过 SM 规范耦合的单圈 RG 跑动计算各费米子扇区的 α 值，
并与谱零参数框架中的拟合值 α_u=1.945, α_d=1.229, α_l=1.358 比较。

输出:
  - 各扇区 γ_m 系数
  - 规范耦合的积分结果
  - 第一原理预测 α 值
  - 与拟合值的比例比较
"""
import numpy as np

# ============================================================
# 物理常数
# ============================================================
M_Z = 91.1876       # GeV
M_PL = 1.22e19      # GeV
L_max = np.log(M_PL / M_Z)  # ln(M_Pl/M_Z)

# SM 单圈 beta 函数系数 (dg/d(ln μ) = b_i * g^3 / (16π^2))
# 对应 dα_i^{-1}/d(ln μ) = -b_i/(2π)
b = {
    'U1': 41.0 / 10.0,    # U(1)_Y (GUT 归一化)
    'SU2': -19.0 / 6.0,    # SU(2)_L
    'SU3': -7.0,            # SU(3)_C
}

# M_Z 处规范耦合 (GUT 归一化 α_1)
alpha_inv_MZ = {
    'U1': 59.0,    # α_1^{-1}(M_Z)
    'SU2': 29.6,   # α_2^{-1}(M_Z)
    'SU3': 8.5,    # α_3^{-1}(M_Z)
}

# ============================================================
# 1. 费米子扇区: Casimir 与超荷
# ============================================================
# 每个扇区有左手(L)和右手(R)两个手性分量
# 质量反常维度 γ_m 是两个分量贡献的和

# 二次 Casimir: C₂(3) = 4/3 (SU(3) 基本表示), C₂(2) = 3/4 (SU(2) 基本表示)
C2_3 = 4.0 / 3.0
C2_2 = 3.0 / 4.0

# 费米子手性分量信息
# 每个条目: (name, C₂(3), C₂(2), Y)
# 超荷约定: Q = T₃ + Y (与谱 SM 注记一致)
chiral_components = {
    'up': {
        'L':  (C2_3, C2_2,  1.0/3.0),   # Q_L  = (3,2)_{1/3}
        'R':  (C2_3, 0.0,   4.0/3.0),   # u_R  = (3,1)_{4/3}
    },
    'down': {
        'L':  (C2_3, C2_2,  1.0/3.0),   # Q_L  = (3,2)_{1/3}
        'R':  (C2_3, 0.0,  -2.0/3.0),   # d_R  = (3,1)_{-2/3}
    },
    'lepton': {
        'L':  (0.0,  C2_2, -1.0),       # L    = (1,2)_{-1}
        'R':  (0.0,  0.0,  -2.0),       # e_R  = (1,1)_{-2}
    },
}


def gamma_coefficients(sector):
    """
    计算给定扇区的 γ_m 系数 (c_s, c_2, c_1)。
    γ_m = c_s * α_s + c_2 * α_2 + c_1 * α_1

    对每个手性分量:
      γ_m_chiral = 3*C₂(3)*α_s/π + (3/4)*C₂(2)*α₂/π + (3/4)*Y²*α₁/π

    返回: (c_s, c_2, c_1)
    """
    c_s, c_2, c_1 = 0.0, 0.0, 0.0
    for chirality, (c3, c2, y) in chiral_components[sector].items():
        cs = 3.0 * c3 / np.pi
        c2_term = 0.75 * c2 / np.pi
        c1_term = 0.75 * y**2 / np.pi
        c_s += cs
        c_2 += c2_term
        c_1 += c1_term
    return c_s, c_2, c_1


# ============================================================
# 2. 规范耦合积分 I_i = ∫ α_i(μ) d(ln μ)
# ============================================================
# α_i(μ)⁻¹ = α_i(M_Z)⁻¹  -  b_i * ln(μ/M_Z) / (2π)
#           = A_i - B_i * L
# 其中 A_i = α_i(M_Z)⁻¹, B_i = b_i/(2π), L = ln(μ/M_Z)
#
# I_i = ∫₀^{L_max} dL / (A_i - B_i * L)
#     = -(1/B_i) * ln(1 - B_i * L_max / A_i)

def compute_integral(gauge_name):
    """计算 ∫ α_i d(ln μ) 从 M_Z 到 M_Pl."""
    A = alpha_inv_MZ[gauge_name]          # α(M_Z)^{-1}
    B = b[gauge_name] / (2.0 * np.pi)     # b/(2π)
    L = L_max

    ratio = B * L / A
    arg = 1.0 - ratio

    if arg <= 0:
        # 规范耦合在到达 M_Pl 前遇到 Landau 极点
        # 对 SU(3), b<0 意味着 α₃⁻¹ 递减, 可能在 M_Pl 前变负
        # 这是已知的 SM 外推到 Planck 能标的问题
        return None, f"Landau pole at L = {A/B:.2f} (< L_max={L:.2f})"

    integral = -np.log(arg) / B
    return integral, None


# ============================================================
# 3. 主计算
# ============================================================
print("=" * 72)
print("Direction 2: α 指数第一原理公式")
print("α(R) = ∫_{M_Z}^{M_Pl} γ_m(R, μ) d(ln μ)")
print("=" * 72)

# 3.1 规范耦合积分
print("\n" + "-" * 72)
print("【步骤 1】规范耦合积分 I_i = ∫ α_i d(ln μ)")
print("-" * 72)
print(f"  M_Z   = {M_Z:.1f} GeV")
print(f"  M_Pl  = {M_PL:.3e} GeV")
print(f"  ln(M_Pl/M_Z) = {L_max:.4f}")
print()

integrals = {}
for g in ['U1', 'SU2', 'SU3']:
    val, err = compute_integral(g)
    integrals[g] = val
    if val is not None:
        print(f"  I_{{{g}}} = {val:.6f}")
    else:
        print(f"  I_{{{g}}} = FAILED: {err}")

# 3.2 各扇区 γ_m 系数
print("\n" + "-" * 72)
print("【步骤 2】各扇区 γ_m 系数")
print("-" * 72)
print(f"  {'扇区':<10s} {'c_s':>10s} {'c_2':>10s} {'c_1':>10s}")
print(f"  {'-'*42}")

coeffs = {}
for sector in ['up', 'down', 'lepton']:
    cs, c2, c1 = gamma_coefficients(sector)
    coeffs[sector] = (cs, c2, c1)
    print(f"  {sector:<10s} {cs:>10.4f} {c2:>10.4f} {c1:>10.4f}")

# 3.3 第一原理 α 值
print("\n" + "-" * 72)
print("【步骤 3】第一原理 α 预测")
print("-" * 72)

fitted = {
    'up': 1.945,
    'down': 1.229,
    'lepton': 1.358,
    'up_ratio': 1.945 / 1.229,    # α_u/α_d
    'down_ratio': 1.229 / 1.358,  # α_d/α_l
    'lepton_ratio': 1.358 / 1.945, # α_l/α_u
}

print(f"  {'扇区':<10s} {'α(第一原理)':<15s} {'α(拟合)':<12s} {'偏差因子':<10s}")
print(f"  {'-'*47}")

predictions = {}
for sector in ['up', 'down', 'lepton']:
    cs, c2, c1 = coeffs[sector]
    i3 = integrals['SU3']
    i2 = integrals['SU2']
    i1 = integrals['U1']

    if None in (i3, i2, i1):
        alpha_pred = float('nan')
    else:
        alpha_pred = cs * i3 + c2 * i2 + c1 * i1

    predictions[sector] = alpha_pred
    ratio = alpha_pred / fitted[sector] if not np.isnan(alpha_pred) else float('nan')
    print(f"  {sector:<10s} {alpha_pred:<15.6f} {fitted[sector]:<12.3f} "
          f"{'N/A' if np.isnan(ratio) else f'×{ratio:.3f}'}")

# 3.4 比例比较
print("\n" + "-" * 72)
print("【步骤 4】扇区间 α 比例比较")
print("-" * 72)

if not any(np.isnan(predictions[s]) for s in ['up', 'down', 'lepton']):
    p = predictions
    ratios_pred = {
        'up/down': p['up'] / p['down'],
        'down/lepton': p['down'] / p['lepton'],
        'lepton/up': p['lepton'] / p['up'],
    }
    ratios_fitted = {
        'up/down': fitted['up_ratio'],
        'down/lepton': fitted['down_ratio'],
        'lepton/up': fitted['lepton_ratio'],
    }

    print(f"  {'比例':<15s} {'第一原理':<12s} {'拟合':<12s} {'偏差':<10s}")
    print(f"  {'-'*49}")
    for key in ratios_pred:
        rp = ratios_pred[key]
        rf = ratios_fitted[key]
        dev = rp / rf if rp >= rf else rf / rp
        print(f"  {key:<15s} {rp:<12.4f} {rf:<12.4f} {'×{:.3f}'.format(dev) if abs(dev-1)>0.01 else '✅ 匹配':<10s}")

    # 归一化到 α_up=1 比较
    print(f"\n  归一化到 α_up:")
    print(f"    {'扇区':<10s} {'第一原理':<12s} {'拟合':<12s} {'偏差':<10s}")
    print(f"    {'-'*44}")
    for sector in ['up', 'down', 'lepton']:
        norm_pred = p[sector] / p['up']
        norm_fit = fitted[sector] / fitted['up']
        dev = norm_pred / norm_fit if norm_pred >= norm_fit else norm_fit / norm_pred
        status = '✅' if dev < 1.5 else '⚠️'
        print(f"    {sector:<10s} {norm_pred:<12.4f} {norm_fit:<12.4f} "
              f"{'×{:.3f}'.format(dev):<10s} {status}")
else:
    print("  警告: 部分积分发散，无法计算比例")

# ============================================================
# 4. 归一化讨论
# ============================================================
print("\n" + "-" * 72)
print("【步骤 5】归一化因子分析")
print("-" * 72)
print("""
如果直接使用 α = ∫γ d ln μ 给出不匹配的值，考虑以下归一化因子:
""")

if not any(np.isnan(predictions[s]) for s in ['up', 'down', 'lepton']):
    # 用 up 扇区确定归一化常数: α_pred_N = k * α_fitted
    k_u = fitted['up'] / predictions['up']
    k_d = fitted['down'] / predictions['down']
    k_l = fitted['lepton'] / predictions['lepton']

    print(f"  归一化因子 k = α_fit / α_pred:")
    print(f"    上型夸克: k_u = {k_u:.4f}")
    print(f"    下型夸克: k_d = {k_d:.4f}")
    print(f"    带电轻子: k_l = {k_l:.4f}")
    print()

    if abs(k_u - k_d) / max(k_u, k_d) < 0.3 and abs(k_d - k_l) / max(k_d, k_l) < 0.3:
        k_mean = np.mean([k_u, k_d, k_l])
        print(f"  归一化因子 k ≈ {k_mean:.3f} (三个扇区接近，符合单一归一化假设)")
    else:
        print(f"  归一化因子差异较大: 表明 γ_m 公式或超荷归一化可能需要调整")

# ============================================================
# 5. 规范耦合 Landau 极点诊断
# ============================================================
print("\n" + "-" * 72)
print("【诊断】规范耦合单圈 Landau 极点")
print("-" * 72)

for g in ['U1', 'SU2', 'SU3']:
    A = alpha_inv_MZ[g]
    B = b[g] / (2.0 * np.pi)
    landau_L = A / B if B != 0 else float('inf')

    if B > 0:
        # 对 U(1): α⁻¹ 随能量递减, 在 L = A/B 处 → 0
        if landau_L < L_max:
            print(f"  {g}: Landau pole at ln(μ/M_Z) = {landau_L:.2f} (< L_max={L_max:.2f}) ⚠️")
        else:
            print(f"  {g}: Landau pole at ln(μ/M_Z) = {landau_L:.2f} (> L_max={L_max:.2f}) ✅")
    elif B < 0:
        # 对 SU(2), SU(3): α⁻¹ 随能量递增, 无 Landau 极点
        alpha_inv_at_Pl = A - B * L_max
        print(f"  {g}: α⁻¹(M_Pl) = {alpha_inv_at_Pl:.2f} (渐近自由, 无 Landau 极点 ✅)")

# ============================================================
# 6. 总结
# ============================================================
print("\n" + "=" * 72)
print("结果总结")
print("=" * 72)
print("""
假设: α(R) = ∫_{M_Z}^{M_Pl} γ_m(R, μ) d(ln μ)

预期:
  - α_u 略大于 α_d (U(1) 贡献不同)
  - α_l 远小于 α_u, α_d (轻子无 SU(3) 贡献)
  - 比值 α_u:α_d:α_l 应与拟合值约化比较
""")

if not any(np.isnan(predictions[s]) for s in ['up', 'down', 'lepton']):
    print(f"  第一原理预测: α_u={predictions['up']:.3f}, "
          f"α_d={predictions['down']:.3f}, α_l={predictions['lepton']:.3f}")
    print(f"  拟合值:        α_u=1.945, α_d=1.229, α_l=1.358")
    print()
    print(f"  比例 (预测):   {predictions['up']/predictions['down']:.3f} : "
          f"{predictions['down']/predictions['lepton']:.3f} : "
          f"{predictions['lepton']/predictions['up']:.3f}")
    print(f"  比例 (拟合):   {fitted['up']/fitted['down']:.3f} : "
          f"{fitted['down']/fitted['lepton']:.3f} : "
          f"{fitted['lepton']/fitted['up']:.3f}")
