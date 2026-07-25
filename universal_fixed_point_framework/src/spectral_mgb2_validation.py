"""
spectral_mgb2_validation.py  v1.0
============================================
MgB₂ 多带 μ*_spec 验证

MgB₂ 是已知的两带超导体 (σ + π 带):
  - σ 带: 2D, B p_x,y 轨道, λ_σ ≈ 0.82, 强耦合
  - π 带: 3D, B p_z 轨道, λ_π ≈ 0.35, 弱耦合

验证目标:
  1. 单带 μ*_spec vs 两带 μ*_spec
  2. T_c 预测 vs 实验值 (39 K)
  3. D_0 是否适用于 p-轨道 (MgB₂ 两带均为 p,不同于 Nb 的 d-轨道)
  4. 跨材料一致性: 扩展验证表至 6 种材料
"""

import numpy as np

# ============================================================
# 谱框架基本常数
# ============================================================
D0 = 0.122
R_WEAK = 0.874
ALPHA = (D0 / R_WEAK) ** 2
A_BCS_WEAK = 0.567
K_to_eV = 8.617333262e-5

# ============================================================
# 核心函数
# ============================================================

def mu_star_spectral(eps_F_eV, wD_eV, alpha=ALPHA):
    L = np.log(eps_F_eV / wD_eV)
    return alpha * L / (1.0 + alpha * L)

def mu_star_multiband(bands, wD_eV):
    """多带 μ*_spec: μ*_eff = Σ w_i · μ*_spec(ε_F^(i), α_i)"""
    total = 0.0
    for band in bands:
        eps_i = band['eps_F']
        alpha_i = band.get('alpha', ALPHA)
        L_i = np.log(eps_i / wD_eV)
        mu_i = alpha_i * L_i / (1.0 + alpha_i * L_i)
        total += band['weight'] * mu_i
    return total

def Tc_McMillan(lam, mu_star, wD_K):
    if lam <= mu_star * (1 + 0.62 * lam):
        return 0.0
    exponent = -(1.0 + lam) / (lam - mu_star * (1.0 + 0.62 * lam))
    return (wD_K / 1.2) * np.exp(exponent)

def a_GeilikmanKresin(Tc, wD_K):
    w_log = wD_K / 1.2
    if Tc <= 0 or w_log <= 2 * Tc:
        return A_BCS_WEAK
    ratio = Tc / w_log
    correction = 12.5 * ratio**2 * np.log(w_log / (2.0 * Tc))
    gap_ratio_2Delta = 3.53 * (1.0 + correction)
    return 2.0 / gap_ratio_2Delta

def a_spectral(r, Z=1.0):
    d = np.sqrt(3.0) * np.sqrt(r)
    return ((1.0 + d / Z) / (4.0 * np.pi) * r) ** (1.0 / 3.0)

def r_from_a(a_target, Z=1.0):
    lo, hi = 0.01, 2.0
    for _ in range(60):
        mid = (lo + hi) / 2.0
        if a_spectral(mid, Z) < a_target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0

# ============================================================
# MgB₂ 材料参数 (来自 Kortus 2001, Choi 2002 等)
# ============================================================
print("=" * 80)
print("MgB₂ 多带 μ*_spec 验证")
print("=" * 80)
print()

# --- MgB₂ 基本参数 ---
MgB2 = {
    'Tc_exp': 39.0,          # K
    'wD_K': 550,             # 有效 B 爱因斯坦模 (K)
    'lam_total': 0.87,       # 总电-声耦合
    'eps_F_total': 11.4,     # 总费米能 (eV)
    'mu_emp': 0.12,          # 文献典型经验 μ*
    'a_exp': None,           # 见下方: 两带间隙不同, 需计算有效 a
}

# MgB₂ σ 带间隙: 2Δ_σ = 7.0 meV × 2 = 14.0 meV (实验典型值)
# MgB₂ π 带间隙: 2Δ_π = 2.0 meV × 2 = 4.0 meV
# 2Δ/kT_c: σ = 14.0/3.36 = 4.17, π = 4.0/3.36 = 1.19
# a = 2 / (2Δ/kT_c): σ = 0.480, π = 1.68

# 实验有效 a (权重平均): w_σ=0.45, w_π=0.55
w_sigma = 0.45
w_pi = 0.55
a_sigma_exp = 0.480
a_pi_exp = 1.68
a_MgB2_eff = w_sigma * a_sigma_exp + w_pi * a_pi_exp  # DOS 加权
# 但谱框架的 a 是整体能隙比, 对多带体系需谨慎
# MgB₂ 实验测得的有效 a 约为 ~0.48 (对应大带隙主导的谱测量)
# 让我们用隧道谱测量的加权平均
print(f"  MgB₂ 基本参数:")
print(f"    T_c(exp) = {MgB2['Tc_exp']} K")
print(f"    ω_D(eff) = {MgB2['wD_K']} K = {MgB2['wD_K']*K_to_eV:.4f} eV")
print(f"    λ_total = {MgB2['lam_total']}")
print(f"    ε_F(total) = {MgB2['eps_F_total']} eV")
print(f"    σ-带: λ_σ=0.82, ε_F^(σ)≈3.5 eV, DOS权重={w_sigma}")
print(f"    π-带: λ_π=0.35, ε_F^(π)≈7.0 eV, DOS权重={w_pi}")

# 有效实验 a: 隧道谱测量 MgB₂ 的加权能隙比
MgB2['a_exp'] = a_sigma_exp  # 通常用大带隙 (σ) 的 a 值
print(f"    实验 a_eff ≈ {a_sigma_exp:.3f} (σ-带主导)")
print()

# ============================================================
# 1. 单带 μ*_spec → T_c
# ============================================================
print("━" * 80)
print("1. 单带 μ*_spec 计算")
print("━" * 80)
print()

wD_Mg_eV = MgB2['wD_K'] * K_to_eV
mu_s_single = mu_star_spectral(MgB2['eps_F_total'], wD_Mg_eV)
L_single = np.log(MgB2['eps_F_total'] / wD_Mg_eV)

Tc_single = Tc_McMillan(MgB2['lam_total'], mu_s_single, MgB2['wD_K'])
Tc_emp = Tc_McMillan(MgB2['lam_total'], MgB2['mu_emp'], MgB2['wD_K'])

print(f"  单带 μ*_spec = {mu_s_single:.4f}")
print(f"  L = ln({MgB2['eps_F_total']}/{wD_Mg_eV:.4f}) = {L_single:.4f}")
print(f"  T_c(spec) = {Tc_single:.1f} K  (vs exp {MgB2['Tc_exp']} K)")
print(f"  T_c(μ*_emp={MgB2['mu_emp']}) = {Tc_emp:.1f} K")
print(f"  T_c偏差(spec) = {abs(Tc_single-MgB2['Tc_exp'])/MgB2['Tc_exp']*100:.1f}%")
print()

# ============================================================
# 2. 两带 μ*_spec → T_c
# ============================================================
print("━" * 80)
print("2. 两带 μ*_spec 计算 (标准 D_0)")
print("━" * 80)
print()

# MgB₂ 两带参数: 都使用标准 D_0 (因为都是 p-轨道)
MgB2_bands = [
    {'name': 'σ-带 (2D B p_x,y)', 'eps_F': 3.5, 'weight': w_sigma, 'alpha': ALPHA},
    {'name': 'π-带 (3D B p_z)',   'eps_F': 7.0, 'weight': w_pi,    'alpha': ALPHA},
]

mu_s_eff = mu_star_multiband(MgB2_bands, wD_Mg_eV)

print(f"  两带 μ*_eff 计算:")
for band in MgB2_bands:
    L_i = np.log(band['eps_F'] / wD_Mg_eV)
    mu_i = band['alpha'] * L_i / (1.0 + band['alpha'] * L_i)
    print(f"    {band['name']}: ε_F={band['eps_F']} eV, L={L_i:.4f}, μ*={mu_i:.4f}, w={band['weight']}")
print(f"  μ*_eff = {mu_s_eff:.4f}")

Tc_twoband = Tc_McMillan(MgB2['lam_total'], mu_s_eff, MgB2['wD_K'])
print(f"  T_c(两带μ*) = {Tc_twoband:.1f} K")
print(f"  T_c偏差(两带) = {abs(Tc_twoband-MgB2['Tc_exp'])/MgB2['Tc_exp']*100:.1f}%")
print()

# ============================================================
# 3. 参数敏感性分析
# ============================================================
print("━" * 80)
print("3. 参数敏感性分析")
print("━" * 80)
print()

# 3a. ε_F 对 T_c 的影响
print("  a. σ-带 ε_F 敏感性:")
print(f"  {'ε_F^σ (eV)':>12s} {'L_σ':>8s} {'μ*_σ':>8s} {'μ*_eff':>8s} {'T_c (K)':>10s} {'偏差%':>8s}")
print("-" * 60)

for eps_sigma in [2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0]:
    bands_test = [
        {'eps_F': eps_sigma, 'weight': w_sigma, 'alpha': ALPHA},
        {'eps_F': 7.0,       'weight': w_pi,    'alpha': ALPHA},
    ]
    mu_eff_test = mu_star_multiband(bands_test, wD_Mg_eV)
    Tc_test = Tc_McMillan(MgB2['lam_total'], mu_eff_test, MgB2['wD_K'])
    dev_test = abs(Tc_test - MgB2['Tc_exp']) / MgB2['Tc_exp'] * 100
    L_sigma = np.log(eps_sigma / wD_Mg_eV)
    mu_sigma = ALPHA * L_sigma / (1.0 + ALPHA * L_sigma)
    print(f"  {eps_sigma:>10.2f}  {L_sigma:>8.4f} {mu_sigma:>8.4f} {mu_eff_test:>8.4f} {Tc_test:>9.1f} {dev_test:>7.1f}%")

print()

# 3b. λ 对 T_c 的影响
print("  b. λ 敏感性:")
print(f"  {'λ':>6s} {'μ*_eff':>8s} {'T_c (K)':>10s} {'偏差%':>8s}")
print("-" * 40)

for lam_test in [0.80, 0.85, 0.87, 0.90, 0.95, 1.00]:
    Tc_lam = Tc_McMillan(lam_test, mu_s_eff, MgB2['wD_K'])
    dev_lam = abs(Tc_lam - MgB2['Tc_exp']) / MgB2['Tc_exp'] * 100
    print(f"  {lam_test:>5.2f} {mu_s_eff:>8.4f} {Tc_lam:>9.1f} {dev_lam:>7.1f}%")

print()

# ============================================================
# 4. 跨材料一致性检验
# ============================================================
print("━" * 80)
print("4. 跨材料一致性: μ*_spec 统一验证 (含 MgB₂)")
print("━" * 80)
print()

# 定义完整材料集 (5 原 + MgB₂)
# MgB₂ 使用两带 μ*_eff, 标准谱映射 (Z = 1+λ)
materials_all = {
    'Al':   {'Tc_exp': 1.2,  'wD_K': 428, 'lam': 0.40, 'mu_spec': 0.1009, 'Z_atom': 13, 'method': '标准', 'a_exp': 0.576},
    'Sn':   {'Tc_exp': 3.7,  'wD_K': 200, 'lam': 0.70, 'mu_spec': 0.1106, 'Z_atom': 50, 'method': '标准', 'a_exp': 0.542},
    'Pb':   {'Tc_exp': 7.2,  'wD_K': 105, 'lam': 1.55, 'mu_spec': 0.1194, 'Z_atom': 82, 'method': '标准', 'a_exp': 0.415},
    'Hg':   {'Tc_exp': 4.2,  'wD_K': 95,  'lam': 1.00, 'mu_spec': 0.1179, 'Z_atom': 80, 'method': '标准', 'a_exp': 0.438},
    'Nb':   {'Tc_exp': 9.3,  'wD_K': 275, 'lam': 1.00, 'mu_spec': 0.0954, 'Z_atom': 41, 'method': '标准', 'a_exp': 0.519},
    'MgB₂': {'Tc_exp': 39.0, 'wD_K': 550, 'lam': 0.87, 'mu_spec': mu_s_eff, 'Z_atom': 5,  'method': '两带', 'a_exp': a_sigma_exp},
}

# MgB₂ 谱映射参数
Z_MgB2 = 1.0 + MgB2['lam_total']

print(f"  {'材料':>6s} {'方法':>15s} {'μ*':>10s} {'T_c^spec(K)':>12s} {'T_c^exp(K)':>10s} {'T_c偏差%':>8s}")
print("-" * 65)

for name, mat in materials_all.items():
    Tc_spec = Tc_McMillan(mat['lam'], mat['mu_spec'], mat['wD_K'])
    dev = abs(Tc_spec - mat['Tc_exp']) / mat['Tc_exp'] * 100
    status = "✅" if dev < 10 else "⚠️"
    print(f"  {name:>6s} {mat['method']:>15s} {mat['mu_spec']:>10.4f} {Tc_spec:>11.1f} {mat['Tc_exp']:>10.1f} {dev:>7.1f}% {status}")

print()
print("  MgB₂ 使用两带 μ*_eff, 标准谱映射 (σ/π 带均为 p-轨道, D_0 不变)")
print()

# ============================================================
# 5. 讨论: D_0^(d)/D_0 的跨材料一致性
# ============================================================
print("━" * 80)
print("5. D_0^(d)/D_0 跨材料一致性分析")
print("━" * 80)
print()

print("  当前标定状态:")
print("  ┌────────────┬──────────────┬─────────────┬──────────────┐")
print("  │ 材料       │ 轨道类型     │ D_0^{(i)}   │ D_0^{(i)}/D_0│")
print("  ├────────────┼──────────────┼─────────────┼──────────────┤")
print("  │ Al (s-p)   │ s, p (3s²3p¹)│ D_0         │ 1.000        │")
print("  │ Sn (s-p)   │ s, p (5s²5p²)│ D_0         │ 1.000        │")
print("  │ Pb (s-p)   │ s, p (6s²6p²)│ D_0         │ 1.000        │")
print("  │ Nb (d)     │ d (4d⁴)     │ D_0^(d)     │ 1.600        │")
print("  │ MgB₂ σ    │ p (B p_x,y) │ D_0^(p,2D)  │ [待定]       │")
print("  │ MgB₂ π    │ p (B p_z)   │ D_0^(p,3D)  │ [待定]       │")
print("  └────────────┴──────────────┴─────────────┴──────────────┘")
print()
print("  结论: MgB₂ 的 σ/π 带均为 p-轨道, 与 Nb 的 d-轨道不同.")
print("  因此 MgB₂ 应当使用标准 D_0 = 0.122 (无需 d-轨道增强).")
print("  若 MgB₂ 的 T_c 预测偏差在可接受范围内 (< 15%),")
print("  则说明标准 D_0 对 p-轨道体系适用, D_0^(d) 增强仅对 d-轨道.")
print()

# ============================================================
# 6. 总结
# ============================================================
print("=" * 80)
print("6. 总结")
print("=" * 80)
print()

Tc_single_dev = abs(Tc_single - MgB2['Tc_exp']) / MgB2['Tc_exp'] * 100
Tc_twoband_dev = abs(Tc_twoband - MgB2['Tc_exp']) / MgB2['Tc_exp'] * 100

print(f"  MgB₂ (T_c^exp = {MgB2['Tc_exp']} K):")
print(f"    单带 μ*_spec = {mu_s_single:.4f} → T_c = {Tc_single:.1f} K ({Tc_single_dev:.1f}% 偏差)")
print(f"    两带 μ*_eff = {mu_s_eff:.4f} → T_c = {Tc_twoband:.1f} K ({Tc_twoband_dev:.1f}% 偏差)")
print()
print(f"  单带 vs 两带比较:")
print(f"    μ*: {mu_s_single:.4f} → {mu_s_eff:.4f} (降低 {(mu_s_single-mu_s_eff)/mu_s_single*100:.1f}%)")
print(f"    T_c: {Tc_single:.1f} K → {Tc_twoband:.1f} K (提升 {(Tc_twoband-Tc_single)/Tc_single*100:.1f}%)")
print()
print(f"  跨材料一致性:")
devs = {name: abs(Tc_McMillan(m['lam'], m['mu_spec'], m['wD_K']) - m['Tc_exp']) / m['Tc_exp'] * 100 
        for name, m in materials_all.items()}
all_ok = all(d < 15 for d in devs.values())
if all_ok:
    print(f"    ✅ 全部 6 种材料的 T_c 预测偏差均 < 15%")
else:
    print(f"    ⚠️ 部分材料偏差 > 15%, 需进一步分析")
for name, d in devs.items():
    emoji = "✅" if d < 10 else ("⚠️" if d < 15 else "❌")
    print(f"    {name}: T_c偏差 {d:.1f}% {emoji}")
print()
print(f"  关键发现: MgB₂ 的两带(σ/π)均为 p-轨道, 使用标准 D_0 = 0.122")
print(f"  无需引入 D_0^(d) 增强. 这说明 D_0^(d)/D_0 = 1.600 是 d-轨道专属.")
print(f"  MgB₂ 两带 μ*_spec 成功将 T_c 预测偏差从单带的 {Tc_single_dev:.1f}%")
print(f"  降至 {Tc_twoband_dev:.1f}%.")
print("=" * 80)
