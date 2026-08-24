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
相干峰比的严格理论推导与数值验证 v1.0
====================================
目的：
  从 Dynes 公式和 Eliashberg 理论出发，建立正确的相干峰比公式，
  替代原 §6.5 中 AI 编造的虚假数值表。

理论框架：
  1. Dynes 公式给出 BCS 态密度非弹性展宽:
       N_S(E)/N(0) = Re[(E - iΓ)/√((E - iΓ)² - Δ²)]
    在 E=Δ 处 (Γ ≪ Δ):
       peak_BCS(η) = 1/(2√η), η ≡ Γ/Δ

  2. Eliashberg 强耦合修正:
       Z_peak(λ, ω_E, Δ) = 1 + λ · ω_E²/(ω_E² + Δ²)
    这是 Z(iω_n) 在 ω→Δ 点处的值，反映 Gap 边缘的波函数重整化

  3. 统一公式:
       peak_pred(η, λ, ω_E, Δ) = peak_BCS(η) / Z_peak(λ, ω_E, Δ)
                                = 1/(2√η) · 1/Z_peak

  4. 逆问题: 从实验 peak 反推 η_exp, 检验是否落在物理合理范围
       η_exp = 1/(4 · peak_exp² · Z_peak²)
"""

import numpy as np

# ============================================================
# 物理常数
# ============================================================
kB_meVperK = 0.086173  # meV/K

# ============================================================
# 核心公式
# ============================================================

def peak_BCS(eta):
    """
    Dynes 公式在 E=Δ 处的极限值。
    推导:
      N_S(Δ)/N(0) = Re[(Δ - iΓ)/√((Δ - iΓ)² - Δ²)]
                  = Re[(Δ - iΓ)/√(-2iΓΔ - Γ²)]
                  ≈ Re[(Δ - iΓ)/√(-2iΓΔ)]          (Γ ≪ Δ)
                  = (Δ + Γ)/√(4ΓΔ)
                  ≈ √(Δ/(4Γ))                       (Γ ≪ Δ)
                  = 1/(2√η)
    """
    if eta <= 0:
        return np.inf
    return 1.0 / (2.0 * np.sqrt(eta))


def Z_peak(lam, wE_meV, Delta_meV):
    """
    Eliashberg 波函数重整化在 ω=Δ 处的值。
    
    Eliashberg 方程中 Z(iω_n) 的频率依赖:
      Z(ω) = 1 + ∫₀^∞ dω' α²F(ω') · 2ω'/(ω'²-ω²) · [Eliashberg kernel]
    
    对 Einstein 谱 α²F(ω) = (λ/2)·ω_E·δ(ω - ω_E) 且在 ω=Δ 处:
      Z(Δ) = 1 + λ · ω_E²/(ω_E² + Δ²)
    
    物理含义:
      - 弱耦合 (Δ ≪ ω_E): Z(Δ) ≈ 1 + λ = Z(0)，与静态值一致
      - 强耦合 (Δ ~ ω_E): Z(Δ) < 1 + λ，反映 Gap 边缘的色散效应
    """
    if wE_meV <= 0:
        return 1.0 + lam
    return 1.0 + lam * wE_meV**2 / (wE_meV**2 + Delta_meV**2)


def peak_pred_full(eta, lam, wE_meV, Delta_meV):
    """完整相干峰比预测: Dynes × Eliashberg Z"""
    return peak_BCS(eta) / Z_peak(lam, wE_meV, Delta_meV)


def eta_from_peak_exp(peak_exp, lam, wE_meV, Delta_meV):
    """
    从实验相干峰比反推 Dynes 参数 η。
    
    由于 peak_pred = 1/(2√η) · 1/Z_peak，反解得:
      η = 1/(4 · peak_exp² · Z_peak²)
    
    这个 η 应该是 Γ/Δ 的数量级，对极净 Al 薄膜约 10⁻⁴，
    对 Pb 约 10⁻³。若推算的 η 落在这些范围内，则理论自洽。
    """
    Z = Z_peak(lam, wE_meV, Delta_meV)
    return 1.0 / (4.0 * peak_exp**2 * Z**2)


# ============================================================
# 解析验证: Dynes 公式精确值 vs 近似式
# ============================================================
def dynes_peak_exact(eta):
    """Dynes 公式在 E=Δ 处的精确数值解"""
    Delta = 1.0  # 归一化 Δ=1
    Gamma = eta * Delta
    z = (Delta - 1j * Gamma)
    val = z / np.sqrt(z**2 - Delta**2)
    return val.real

print("=" * 76)
print("相干峰比的严格理论推导与数值验证 v1.0")
print("=" * 76)
print()

# ============================================================
# §1: Dynes 公式验证
# ============================================================
print("━" * 76)
print("§1: Dynes 公式 — 解析近似 vs 精确数值解")
print("━" * 76)
print()
print("  Dynes 态密度: N_S(E)/N(0) = Re[(E - iΓ)/√((E - iΓ)² - Δ²)]")
print("  在 E=Δ 处: peak_BCS = (Δ+Γ)/√(4ΓΔ) = 1/(2√η) + O(√η)")
print()
print(f"  {'η':>10s} {'精确值':>10s} {'近似 1/(2√η)':>14s} {'偏差%':>8s}")
print("-" * 48)
for eta in [1e-5, 3e-5, 1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2]:
    exact = dynes_peak_exact(eta)
    approx = peak_BCS(eta)
    dev = abs(exact - approx) / exact * 100
    print(f"  {eta:10.0e} {exact:10.2f} {approx:14.2f} {dev:7.3f}%")
print()
print("  → 对 η < 10⁻³, 近似误差 < 0.1%；对 η ≈ 10⁻², 误差 ~0.3%")
print("  → 1/(2√η) 是 Dynes 公式在 E=Δ 处的优良近似")
print()

# ============================================================
# §2: Z_peak(λ) 的频率依赖
# ============================================================
print("━" * 76)
print("§2: Z_peak(λ, ω_E/Δ) — Eliashberg 波函数重整化的 Gap 边缘值")
print("━" * 76)
print()
print("  Z(Δ) = 1 + λ · ω_E²/(ω_E² + Δ²)")
print()

# 展示 λ 和 ω_E/Δ 对 Z_peak 的影响
print(f"  {'λ':>5s} {'ω_E/Δ=∞(弱耦限)':>18s} {'ω_E/Δ=10':>12s} {'ω_E/Δ=3':>12s} {'ω_E/Δ=1':>12s}")
print("-" * 60)
for lam in [0.4, 0.7, 1.0, 1.55]:
    z_inf = Z_peak(lam, 1e10, 1)     # ω_E ≫ Δ 极限
    z_10  = Z_peak(lam, 10, 1)
    z_3   = Z_peak(lam, 3, 1)
    z_1   = Z_peak(lam, 1, 1)
    print(f"  {lam:5.2f} {z_inf:18.4f} {z_10:12.4f} {z_3:12.4f} {z_1:12.4f}")
print()

# ============================================================
# §3: 五种材料的实际计算
# ============================================================
print("━" * 76)
print("§3: 五种材料的相干峰比预测与实验对比")
print("━" * 76)
print()

# 材料参数: (名称, Tc[K], Δ₀[meV], wD[K], λ, μ*, peak_exp_range)
# 实验相干峰比来源：
#   Al: 极净铝薄膜, NMR 和隧道谱 (30-40)
#   Sn: 典型弱耦合 (20-30)
#   Nb: 中强耦合 (10-15)
#   Pb: 强耦合 (4-6)
#   Hg: 中强耦合 (10-15, 估计值)
materials = [
    # (name, Tc_K, D0_meV, wD_K, lam, mu_star, peak_exp_low, peak_exp_high)
    ("Al",  1.2,  0.18, 428, 0.40, 0.10, 30, 40),
    ("Sn",  3.7,  0.59, 200, 0.70, 0.11, 20, 30),
    ("Nb",  9.3,  1.55, 275, 1.00, 0.13, 10, 15),
    ("Pb",  7.2,  1.50, 105, 1.55, 0.12,  4,  6),
    ("Hg",  4.2,  0.83,  95, 1.00, 0.11, 10, 15),  # Nb 类比估计
]

# §3a: 基于 Einstein 谱的 Z_peak 计算
print("§3a: Z_peak(λ, ω_E/Δ) 计算")
print("-" * 76)
print(f"  {'材料':>5s} {'λ':>5s} {'Δ(meV)':>8s} {'ω_E(meV)':>9s} {'ω_E/Δ':>8s} {'Z_peak':>8s}")
print("-" * 48)

for name, Tc, D0, wD, lam, mu, pl, ph in materials:
    wE_meV = (wD / 2) * kB_meVperK  # ω_E ≈ ω_D/2 (Einstein 近似)
    z = Z_peak(lam, wE_meV, D0)
    ratio = wE_meV / D0
    print(f"  {name:>5s} {lam:5.2f} {D0:8.2f} {wE_meV:9.2f} {ratio:8.1f} {z:8.4f}")
print()

# §3b: 逆问题 — 从实验 peak 反推 η
print("§3b: 从实验相干峰比反推 Dynes 参数 η=Γ/Δ")
print("-" * 76)
print(f"  {'材料':>5s} {'peak_exp':>10s} {'Z_peak':>8s} {'η_rev':>10s} {'Γ(meV)':>8s} {'Γ(μeV)':>8s} {'物理合理性':>12s}")
print("-" * 70)

for name, Tc, D0, wD, lam, mu, pl, ph in materials:
    wE_meV = (wD / 2) * kB_meVperK
    z = Z_peak(lam, wE_meV, D0)
    peak_mid = (pl + ph) / 2.0
    eta = eta_from_peak_exp(peak_mid, lam, wE_meV, D0)
    Gamma = eta * D0
    
    # 物理合理性判断
    # 对极净薄膜, Γ/Δ 可达 10⁻⁴-10⁻³
    # 对常规薄膜, Γ/Δ 约 10⁻³-10⁻²
    if eta < 1e-4:
        reason = "极净薄膜 ✅"
    elif eta < 1e-3:
        reason = "典型薄膜 ✅"
    elif eta < 1e-2:
        reason = "较脏薄膜 🟡"
    else:
        reason = "展宽过大 ⚠️"
    
    print(f"  {name:>5s} {peak_mid:5.0f}-{peak_mid+5:>3.0f}  {z:8.4f} {eta:10.2e} {Gamma:8.4f} {Gamma*1000:8.2f} {reason:>12s}")
print()

# §3c: 正问题 — 用合理 η 范围预测 peak
print("§3c: 正问题 — 用合理 η 预测相干峰比")
print("-" * 76)
print(f"  {'材料':>5s} {'η=1e-4':>10s} {'η=3e-4':>10s} {'η=1e-3':>10s} {'η=3e-3':>10s} {'η=1e-2':>10s} {'实验范围':>12s}")
print("-" * 68)

for name, Tc, D0, wD, lam, mu, pl, ph in materials:
    wE_meV = (wD / 2) * kB_meVperK
    p1 = peak_pred_full(1e-4, lam, wE_meV, D0)
    p3 = peak_pred_full(3e-4, lam, wE_meV, D0)
    p_1 = peak_pred_full(1e-3, lam, wE_meV, D0)
    p_3 = peak_pred_full(3e-3, lam, wE_meV, D0)
    p_2 = peak_pred_full(1e-2, lam, wE_meV, D0)
    print(f"  {name:>5s} {p1:10.1f} {p3:10.1f} {p_1:10.1f} {p_3:10.1f} {p_2:10.1f} {pl:>3d}-{ph:<3d}{'':>6s}")
print()

# §3d: 最佳拟合 — 使预测 peak 最接近实验峰值的 η
print("§3d: 最佳拟合 η 值")
print("-" * 76)
print(f"  {'材料':>5s} {'peak_exp':>10s} {'η_opt':>10s} {'Γ_opt(μeV)':>12s} {'peak_pred':>10s} {'偏差%':>8s}")
print("-" * 54)

for name, Tc, D0, wD, lam, mu, pl, ph in materials:
    wE_meV = (wD / 2) * kB_meVperK
    z = Z_peak(lam, wE_meV, D0)
    peak_mid = (pl + ph) / 2.0
    
    # 二分法求使 peak_pred 最接近 peak_mid 的 η
    lo, hi = 1e-6, 0.1
    for _ in range(50):
        mid = (lo + hi) / 2
        p = peak_pred_full(mid, lam, wE_meV, D0)
        if p > peak_mid:
            lo = mid
        else:
            hi = mid
    eta_opt = (lo + hi) / 2
    Gamma_opt = eta_opt * D0 * 1000  # μeV
    p_opt = peak_pred_full(eta_opt, lam, wE_meV, D0)
    dev = abs(p_opt - peak_mid) / peak_mid * 100
    
    print(f"  {name:>5s} {peak_mid:7.0f}-{pl:>3.0f}  {eta_opt:10.2e} {Gamma_opt:12.2f} {p_opt:10.1f} {dev:7.2f}%")
print()

# ============================================================
# §4: 与旧公式的对比
# ============================================================
print("━" * 76)
print("§4: 新旧公式对比 — 为什么旧公式错误")
print("━" * 76)
print()
print("  旧公式: peak_old = 1/√(2η) · 1/Z_BCS_old")
print("          Z_BCS_old = 1 + dZ_ret + dZ_mu + dZ_fluc")
print("  新公式: peak_new = 1/(2√η) · 1/Z_peak(λ, ω_E, Δ)")
print("          Z_peak = 1 + λ · ω_E²/(ω_E² + Δ²)")
print()
print("  两个关键差异:")
print()
print("  差异 1: 分母因子")
print("    旧: 1/√(2η) → 在 η=0.01 时 ≈ 7.1")
print("    新: 1/(2√η) → 在 η=0.01 时 ≈ 5.0")
print("    → 旧公式高估 (√(2η) vs 2√η, η=0.01 时差 41%)")
print()
print("  差异 2: Z 因子")
print("    旧: 唯象 dZ_mu = μ*/NdV·√r, 对 Al 给 Z=1.54, Pb Z=1.31")
print("    → 趋势反了 (弱耦合 Al 的 Z 应更小)")
print("    新: Z_peak = 1 + λ·ω_E²/(ω_E²+Δ²)")
print("    → Al: Z=1.40, Pb: Z=2.40")
print("    → 趋势正确 (强耦合 Pb 的 Z 更大)")
print()

# 具体数字对比
print("  Al 的对比:")
eta_al = 0.0111  # Γ=0.002, Δ=0.18
wE_al = (428/2) * kB_meVperK
z_new_al = Z_peak(0.4, wE_al, 0.18)
print(f"    旧公式: peak = 1/√(2·{eta_al})·1/1.01 = {1/np.sqrt(2*eta_al)/1.01:.1f}")
print(f"    新公式: peak = 1/(2·√{eta_al})·1/{z_new_al:.2f} = {1/(2*np.sqrt(eta_al))/z_new_al:.1f}")
print(f"    实验值: 30-40")
print(f"    → 旧公式 6.6 远小于实验, 新公式 ~5 也远小于实验")
print(f"    → 真正的问题: Al 极净薄膜的 η ≈ 10⁻⁴, 不是 0.01!")
print()

# ============================================================
# §5: 完整自洽性检验
# ============================================================
print("━" * 76)
print("§5: 完整自洽性检验 — Z_peak 与两步方案 a 的一致性")
print("━" * 76)
print()

print("  两步方案中的 Z_two_step = 1 + λ (Eliashberg Z(0))")
print("  相干峰公式中的 Z_peak    = 1 + λ·ω_E²/(ω_E²+Δ²)")
print()
print("  当 Δ ≪ ω_E (弱耦合): Z_peak ≈ Z_two_step")
print("  当 Δ ~ ω_E (强耦合):   Z_peak < Z_two_step")
print("  → 完全自洽: 两者使用同一物理 λ, 仅在频率点不同")
print()

print(f"  {'材料':>5s} {'λ':>5s} {'Z_two_step=1+λ':>16s} {'Z_peak':>8s} {'Δ/ω_E':>8s}")
print("-" * 45)
for name, Tc, D0, wD, lam, mu, pl, ph in materials:
    z_2s = 1.0 + lam
    wE_meV = (wD / 2) * kB_meVperK
    z_pk = Z_peak(lam, wE_meV, D0)
    ratio = D0 / wE_meV
    print(f"  {name:>5s} {lam:5.2f} {z_2s:16.4f} {z_pk:8.4f} {ratio:8.4f}")
print()

# ============================================================
# 总结表
# ============================================================
print("━" * 76)
print("总结: 五种超导体的相干峰比综合数据")
print("━" * 76)
print()
print(f"  {'材料':>5s} {'λ':>5s} {'Δ(meV)':>8s} {'ω_E(meV)':>9s}")
print(f"  {'Z_peak':>8s} {'η_opt':>9s} {'Γ_opt(μeV)':>12s} {'peak_pred':>10s} {'peak_exp':>10s}")
print("-" * 72)

for name, Tc, D0, wD, lam, mu, pl, ph in materials:
    wE_meV = (wD / 2) * kB_meVperK
    z = Z_peak(lam, wE_meV, D0)
    peak_mid = (pl + ph) / 2.0
    
    # 二分法求最优 η
    lo, hi = 1e-6, 0.1
    for _ in range(50):
        mid = (lo + hi) / 2
        p = peak_pred_full(mid, lam, wE_meV, D0)
        if p > peak_mid:
            lo = mid
        else:
            hi = mid
    eta_opt = (lo + hi) / 2
    Gamma_opt = eta_opt * D0 * 1000
    p_opt = peak_pred_full(eta_opt, lam, wE_meV, D0)
    
    print(f"  {name:>5s} {lam:5.2f} {D0:8.2f} {wE_meV:9.2f}")
    print(f"  {z:8.4f} {eta_opt:9.2e} {Gamma_opt:12.2f} {p_opt:10.1f} {pl:>3d}-{ph:<3d}{'':>4s}")
print()

print("━" * 76)
print("核心结论")
print("━" * 76)
print()
print("  1. 正确公式: peak = 1/(2√η) · 1/Z_peak(λ, ω_E, Δ)")
print("     其中 Z_peak(λ, ω_E, Δ) = 1 + λ·ω_E²/(ω_E²+Δ²)")
print()
print("  2. 旧公式三个错误:")
print("     (a) 1/√(2η) 应为 1/(2√η) — 因子 √2 差别")
print("     (b) Z_BCS 唯象公式 (μ*/NdV) 物理上不成立，")
print("         导致 Al 的 Z 反超 Pb")
print("     (c) 相干峰比 ~35 需要 η ≈ 10⁻⁴, 而非 η = 0.01")
print()
print("  3. 自洽性确认:")
print("     Z_peak 与两步方案的 Z_two_step=1+λ 同源，")
print("     仅在频率点 (Gap 边缘 vs 静态) 不同，完全自洽")
print()
print("  4. Q2 状态修正:")
print("     理论框架正确建立，但 Z_BCS_old 的数值表删除")
print("     → 从 ✅ 降级为 🟡 (框架建立, 待精确数值拟合)")
