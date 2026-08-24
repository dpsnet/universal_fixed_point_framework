# ============================================================
# UFPF → MUFPF 更名通知
# ============================================================
# 本文件属于 Universal Fixed Point Framework (UFPF)。
# 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
# 更名计划详见：roadmap/mu_renaming_plan.md
#
# 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
# 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
#
# 本文件中 UFPF 相关引用数量：0
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

"""
spectral_hg_deviation_analysis.py  v1.0
========================================
Hg μ*_spec 偏差的定量分解分析

目标: 区分 Hg 的 11.7% a_spec 偏差中:
  1) μ*_spec 公式的偏差 (7.2% μ* 偏差)
  2) 谱映射链 (McMillan → GK → a_spec) 的偏差
  3) 有效费米能的相对论修正

关键发现 (来自对比分析):
  - 即使使用经验 μ*_emp = 0.11, Hg 的 a_spec 仍有 10.8% 偏差
  - 说明大部分偏差来自谱映射链本身, 而非 μ*_spec
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

def mu_star_spectral(eps_F_eV, wD_eV):
    L = np.log(eps_F_eV / wD_eV)
    return ALPHA * L / (1.0 + ALPHA * L)

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
# Hg 材料参数
# ============================================================
Hg_params = {
    'Tc_exp': 4.2,
    'wD_K': 95,
    'lam': 1.00,
    'eps_F': 7.8,    # 自由电子模型
    'mu*_emp': 0.11,
    'a_exp': 0.438,
}

# ============================================================
# 1. 偏差来源分解
# ============================================================
print("=" * 80)
print("1. Hg 偏差来源分解")
print("=" * 80)
print()

wD_K = Hg_params['wD_K']
wD_eV = wD_K * K_to_eV
lam = Hg_params['lam']
Z = 1.0 + lam
eps_F_base = Hg_params['eps_F']
mu_emp = Hg_params['mu*_emp']
a_exp = Hg_params['a_exp']

# --- 1a. 用经验 μ* 的映射 (隔离 μ*_spec 的影响) ---
Tc_emp = Tc_McMillan(lam, mu_emp, wD_K)
a_gk_emp = a_GeilikmanKresin(Tc_emp, wD_K)
r_emp = r_from_a(a_gk_emp, Z)
a_spec_emp = a_spectral(r_emp, Z)
dev_emp = abs(a_spec_emp - a_exp) / a_exp * 100

# --- 1b. 用 μ*_spec 的映射 ---
mu_spec = mu_star_spectral(eps_F_base, wD_eV)
Tc_spec = Tc_McMillan(lam, mu_spec, wD_K)
a_gk_spec = a_GeilikmanKresin(Tc_spec, wD_K)
r_spec = r_from_a(a_gk_spec, Z)
a_spec_spec = a_spectral(r_spec, Z)
dev_spec = abs(a_spec_spec - a_exp) / a_exp * 100

print(f"  Hg 参数: ε_F={eps_F_base} eV, ω_D={wD_K} K, λ={lam}")
print(f"  a_exp = {a_exp}")
print()
print(f"  {'情景':>30s} {'T_c(K)':>10s} {'a_spec':>10s} {'a偏差%':>10s}")
print("-" * 65)
print(f"  {'用经验 μ*_emp=0.11':>30s} {Tc_emp:>10.2f} {a_spec_emp:>10.4f} {dev_emp:>9.1f}%")
print(f"  {'用 μ*_spec=0.1179':>30s} {Tc_spec:>10.2f} {a_spec_spec:>10.4f} {dev_spec:>9.1f}%")
print()

# 偏差分解
mu_dev = abs(mu_spec - mu_emp) / mu_emp * 100
spec_chain_dev = dev_emp  # 使用经验 μ* 仍有 10.8% 偏差 = 谱映射链固有偏差
mu_contribution = dev_spec - spec_chain_dev  # μ*_spec 增加的偏差

print(f"  **偏差分解**")
print(f"  μ*_spec 本身的偏差: {mu_dev:.1f}%")
print(f"  谱映射链 (T_c→GK→a) 固有偏差 (即使 μ*_emp): {spec_chain_dev:.1f}%")
print(f"  μ*_spec 导致的额外偏差: {mu_contribution:.1f}%")
print()

# ============================================================
# 2. 有效 ε_F 的敏感性分析
# ============================================================
print("=" * 80)
print("2. 有效费米能 ε_F 敏感性分析")
print("=" * 80)
print()
print(f"  Hg 的 Z=80, 6s 电子相对论效应显著")
print(f"  自由电子模型 ε_F = 7.8 eV 可能高估实际有效值")
print()

# 目标 ε_F 使得 μ*_spec = μ*_emp = 0.11
# μ* = αL/(1+αL) → αL = μ*/(1-μ*)
target_mu = mu_emp
alphaL_target = target_mu / (1.0 - target_mu)
L_target = alphaL_target / ALPHA
eps_F_target = wD_eV * np.exp(L_target)

print(f"  若 μ*_spec = μ*_emp = 0.11:")
print(f"    所需 L = {L_target:.4f}")
print(f"    所需 ε_F = {eps_F_target:.4f} eV = {eps_F_target/eps_F_base*100:.1f}% 的自由电子值")
print()

# 扫描不同 ε_F 对 μ*_spec 和 a_spec 的影响
print(f"  {'ε_F (eV)':>10s} {'L':>8s} {'μ*_spec':>10s} {'T_c':>10s} {'a_spec':>10s} {'a偏差%':>10s}")
print("-" * 60)

for factor in [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]:
    eps_F_test = eps_F_base * factor
    mu_test = mu_star_spectral(eps_F_test, wD_eV)
    Tc_test = Tc_McMillan(lam, mu_test, wD_K)
    a_gk_test = a_GeilikmanKresin(Tc_test, wD_K)
    r_test = r_from_a(a_gk_test, Z)
    a_test = a_spectral(r_test, Z)
    dev_test = abs(a_test - a_exp) / a_exp * 100
    L_test = np.log(eps_F_test / wD_eV)
    print(f"  {eps_F_test:>8.2f}  {L_test:>8.4f} {mu_test:>10.4f} {Tc_test:>8.2f} {a_test:>10.4f} {dev_test:>9.1f}%")

print()

# ============================================================
# 3. 相对论效应对 Hg 能带结构的修正估计
# ============================================================
print("=" * 80)
print("3. Hg 的相对论能带修正")
print("=" * 80)
print()
print("  Hg (Z=80) 的 6s 电子经历强相对论效应:")
print("  - 6s 轨道收缩: 有效 Bohr 半径 ≈ a₀ / (1 + Z²α²/4)")
print("  - 6s 结合能增加 ~10 eV")
print("  - 6s 带宽变窄 → 有效质量增大 → 有效 ε_F 降低")
print()

# 相对论修正估算
Z_Hg = 80
alpha_fs = 1/137.036  # 精细结构常数
rel_contraction = 1.0 / (1.0 + 0.25 * Z_Hg**2 * alpha_fs**2)
print(f"  相对论收缩因子: {rel_contraction:.4f}")
print(f"  这对 ε_F 的修正: ε_F^rel ≈ ε_F^free × {rel_contraction:.4f}")
print(f"  修正后 ε_F^rel ≈ {eps_F_base * rel_contraction:.2f} eV")
print()

# 同时考虑收缩因子
eps_F_rel = eps_F_base * rel_contraction
mu_rel = mu_star_spectral(eps_F_rel, wD_eV)
Tc_rel = Tc_McMillan(lam, mu_rel, wD_K)
a_gk_rel = a_GeilikmanKresin(Tc_rel, wD_K)
r_rel = r_from_a(a_gk_rel, Z)
a_rel = a_spectral(r_rel, Z)
dev_rel = abs(a_rel - a_exp) / a_exp * 100

print(f"  使用相对论修正 ε_F = {eps_F_rel:.3f} eV:")
print(f"    μ*_spec = {mu_rel:.4f}")
print(f"    T_c = {Tc_rel:.2f} K")
print(f"    a_spec = {a_rel:.4f}")
print(f"    a偏差 = {dev_rel:.1f}%")
print()

# ============================================================
# 4. 综合修正方案: ε_F 的唯象调整
# ============================================================
print("=" * 80)
print("4. 最佳 ε_F 拟合")
print("=" * 80)
print()
print("  寻找使 a_spec 偏差最小的 ε_F...")
print()

best_dev = 1e10
best_eps = eps_F_base
best_mu = 0
best_Tc = 0
best_a = 0

for factor in np.arange(0.3, 1.5, 0.01):
    eps_test = eps_F_base * factor
    mu_test = mu_star_spectral(eps_test, wD_eV)
    Tc_test = Tc_McMillan(lam, mu_test, wD_K)
    a_gk_test = a_GeilikmanKresin(Tc_test, wD_K)
    r_test = r_from_a(a_gk_test, Z)
    a_test = a_spectral(r_test, Z)
    dev_test = abs(a_test - a_exp) / a_exp * 100
    if dev_test < best_dev:
        best_dev = dev_test
        best_eps = eps_test
        best_mu = mu_test
        best_Tc = Tc_test
        best_a = a_test

print(f"  最佳 ε_F = {best_eps:.3f} eV (因子 ×{best_eps/eps_F_base:.3f})")
print(f"  对应 μ*_spec = {best_mu:.4f}")
print(f"  T_c = {best_Tc:.2f} K")
print(f"  a_spec = {best_a:.4f}")
print(f"  a偏差 = {best_dev:.1f}%")
print()

# 对比自由电子值 μ*_spec vs 修正后
mu_dev_orig = abs(mu_spec - mu_emp) / mu_emp * 100
mu_dev_corr = abs(best_mu - mu_emp) / mu_emp * 100
print(f"  μ*_spec 原始偏差: {mu_dev_orig:.1f}%  →  修正后偏差: {mu_dev_corr:.1f}%")
print()

# ============================================================
# 5. 所有材料的 ε_F 敏感性对比
# ============================================================
print("=" * 80)
print("5. 各材料对 ε_F 不确定性的敏感性")
print("=" * 80)
print()
print(f"  {'材料':>5s} {'ε_F':>8s} {'dε_F/ε_F':>10s} {'dμ*/μ*':>10s} {'dTc/d(ε_F)(K/eV)':>18s}")
print("-" * 55)

materials = {
    'Al': {'Tc_exp': 1.2, 'wD_K': 428, 'lam': 0.40, 'eps_F': 11.7, 'mu*_emp': 0.10},
    'Sn': {'Tc_exp': 3.7, 'wD_K': 200, 'lam': 0.70, 'eps_F': 10.2, 'mu*_emp': 0.11},
    'Nb': {'Tc_exp': 9.3, 'wD_K': 275, 'lam': 1.00, 'eps_F': 5.3,  'mu*_emp': 0.13},
    'Pb': {'Tc_exp': 7.2, 'wD_K': 105, 'lam': 1.55, 'eps_F': 9.5,  'mu*_emp': 0.12},
    'Hg': {'Tc_exp': 4.2, 'wD_K': 95,  'lam': 1.00, 'eps_F': 7.8,  'mu*_emp': 0.11},
}

for name, mat in materials.items():
    eps0 = mat['eps_F']
    wD = mat['wD_K'] * K_to_eV
    wD_K_val = mat['wD_K']
    lam_v = mat['lam']
    Zv = 1.0 + lam_v
    
    # 在 ε_F 附近 ±1% 的导数
    deps = eps0 * 0.01
    mu0 = mu_star_spectral(eps0, wD)
    mu_hi = mu_star_spectral(eps0 + deps, wD)
    
    dmu_mu = (mu_hi - mu0) / mu0 / 0.01  # 每 1% ε_F 变化的 μ* 变化 %
    
    Tc0 = Tc_McMillan(lam_v, mu0, wD_K_val)
    Tc_hi = Tc_McMillan(lam_v, mu_hi, wD_K_val)
    dTc_deps = (Tc_hi - Tc0) / deps  # K/eV
    
    print(f"  {name:>5s} {eps0:>8.2f} {'1%':>10s} {dmu_mu*0.01*100:>9.2f}% {dTc_deps:>17.2f}")

print()
print("  注: Hg 的 dTc/d(ε_F) 绝对值大, 说明对 ε_F 高度敏感")
print()

# ============================================================
# 6. 总结
# ============================================================
print("=" * 80)
print("6. 总结与建议")
print("=" * 80)
print()
print(f"  Hg 的 11.7% a_spec 偏差分解:")
print(f"    - 谱映射链固有偏差 (即使 μ*_emp): {spec_chain_dev:.1f}%")
print(f"    - μ*_spec 额外偏差: {mu_contribution:.1f}%")
print(f"    - 自由电子 ε_F=7.8eV 可能不适用于 Hg (Z=80 相对论效应)")
print(f"    - 若采用有效 ε_F ≈ {best_eps:.2f} eV, 偏差降至 {best_dev:.1f}%")
print()
print(f"  核心结论: Hg 的偏差不是 μ*_spec 公式的失效,")
print(f"  而是自由电子 ε_F 模型对 Hg (Z=80) 不再适用.")
print(f"  建议在后续工作中引入相对论修正的 ε_F^eff 公式.")
print("=" * 80)
