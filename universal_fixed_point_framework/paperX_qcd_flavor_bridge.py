#!/usr/bin/env python3
"""
61B Λ_QCD 跨味衔接方案（2026-08-05）
======================================
笔记出处：notes/01_qcd_higgs/spectral_color_dynamics.md §4.4 开放项 3
（跨味微扰单圈 Λ^(3) = 122 MeV 与谱框架有效值 Λ_eff = 210 MeV 的精确衔接）。

问题：跨味微扰单圈 Λ^(3)（谱值 α_s(M_Z)⁻¹ = 8.7 起步）= 121.8 MeV 与谱框架
有效值 Λ_eff = 210 MeV（F_π 定标）差 1.72 倍——之前仅登记"量级自洽"（210/122 落在
PDG 单圈→5-loop 修正因子 2.44 范围内）。

本方案给出三层衔接证据 + 有效性反证 + 谱量近似，把 1.72 倍从"量级自洽"
升级为"精确衔接"：
  证据 A（圈阶漂移带包含）：微扰 Λ 圈阶漂移带 [Λ^(3)_1loop, Λ^(3)_2loop] = [122, 578] MeV
          包含 F_π 定标 Λ_eff = 210——pole 圈阶漂移非物理，Λ_eff 为圈阶无关有效标度；
  证据 B（DS 非微扰桥）：Δ_dress = κ·Λ_eff = 401.3 MeV ≈ DS 动力学质量 M(0)(d_AB) = 401 MeV
          （完整 A/B 耦合 DS，推论 5.9）——210 的物理内容是禁闭区动力学质量生成；
  证据 C（有效性反证）：若用微扰 Λ_pert = 122 谱定 → m_ρ = 472 MeV（偏差 39% 不可用）；
          用 Λ_eff = 210 → m_ρ = 809 MeV（偏差 4.4%）——有效标度的物理地位。
  谱量近似：ξ = Λ_eff/Λ_pert = 1.726 ≈ √N_c = 1.732（偏差 0.4%，登记；
          机制性存疑诚实边界——主衔接证据为证据 B DS 桥 + 证据 A 带包含）。

输入（谱框架登记值）：
  F_π = 92.2 MeV、Δλ₃/Δλ_min = 1.4142、C_QCD = 2.25、N_c = 3
  κ = 1.9091（定理 5.3）、m_ud = 3.45 MeV
  M(0)(d_AB) = 401 MeV（推论 5.9，paperX_qcd_ds_ab.py 6/6 完整 A/B 耦合 DS）
  M_Z = 91.1876 GeV、m_b = 4.2、m_c = 1.27、m_s = 0.095 GeV、α_s(M_Z)⁻¹ = 8.7（谱值）
"""
import math

M_Z = 91.1876
M_B, M_C, M_S = 4.2, 1.27, 0.095          # GeV
F_PI = 92.2                                # MeV，谱框架登记值
RATIO_DL = 0.1725 / 0.122                  # Δλ₃/Δλ_min = 1.4142
C_QCD = 2.25
N_C = 3
KAPPA = 1.9091                             # 定理 5.3：κ = (N_c/π)(Δλ₃/Δλ_min)²
M_UD = 3.45                                # MeV，轻味平均裸质量
M0_DS = 401.0                              # MeV，推论 5.9 完整 A/B 耦合 DS（d_AB = 1.485）
A_INV_MZ = 8.7                             # 谱值 α_s(M_Z)⁻¹（三圈谱值，偏差 2.7%）
PDG_M_RHO = 775.3                          # MeV

checks = []

def check(name, cond, detail=""):
    checks.append((name, cond, detail))
    print(f"  [{'PASS' if cond else 'FAIL'}] {name} {detail}")

def b0(nf):
    return 11 - (2.0 / 3.0) * nf

def b1(nf):
    return 102 - (38.0 / 3.0) * nf   # 两圈 β 系数（SU(3)，MS-bar）

def alpha_inv_evolve(a_inv, b, mu1, mu2):
    """单圈跑动：1/α(μ₂) = 1/α(μ₁) + (b/2π)·ln(μ₂/μ₁)"""
    return a_inv + (b / (2 * math.pi)) * math.log(mu2 / mu1)

def Lambda_flavor_1loop(a_inv_MZ):
    """单圈跨味：N_f 分段跑动（M_Z→m_b→m_c→m_s），m_s 处解 Λ^(3)，返回 (Λ^(5), Λ^(3)) MeV"""
    a = alpha_inv_evolve(a_inv_MZ, b0(5), M_Z, M_B)
    a = alpha_inv_evolve(a, b0(4), M_B, M_C)
    a = alpha_inv_evolve(a, b0(3), M_C, M_S)
    L3 = M_S * math.exp(-a / (b0(3) / (2 * math.pi))) * 1000.0
    L5 = M_Z * math.exp(-a_inv_MZ / (b0(5) / (2 * math.pi))) * 1000.0
    return L5, L3

def du_dlmu(u, nf):
    """两圈 RGE（u = 1/α）：du/dlnμ = b₀/2π + b₁/(4π²u)"""
    return b0(nf) / (2 * math.pi) + b1(nf) / (4 * math.pi**2 * u)

def two_loop_pole(a_inv_MZ):
    """两圈跨味 RK4 积分（μ 对数网格，u = 1/α 变量）到 u → 0，返回 pole（MeV）"""
    dl = -2e-4
    segments = [(math.log(M_Z), math.log(M_B), 5),
                (math.log(M_B), math.log(M_C), 4),
                (math.log(M_C), math.log(M_S), 3),
                (math.log(M_S), math.log(2e-6), 3)]
    u = a_inv_MZ
    mu = M_Z
    for lmu_hi, lmu_lo, nf in segments:
        steps = max(20, int((lmu_hi - lmu_lo) / abs(dl)))
        ds = (lmu_lo - lmu_hi) / steps
        for _ in range(steps):
            k1 = du_dlmu(u, nf)
            k2 = du_dlmu(u + 0.5 * ds * k1, nf)
            k3 = du_dlmu(u + 0.5 * ds * k2, nf)
            k4 = du_dlmu(u + ds * k3, nf)
            u_new = u + (ds / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
            if u_new <= 0:          # 越过 pole：线性插值 pole 位置
                frac = u / (u - u_new)
                return math.exp(lmu_hi + ds * (frac - 1) * 1.0) * 1000.0
            u = u_new
            lmu_hi += ds
        mu = math.exp(lmu_hi)
    return mu * 1000.0

print("=" * 72)
print("61B Λ_QCD 跨味衔接方案：微扰 122 MeV ↔ 有效值 210 MeV 的三层证据闭环")
print("=" * 72)

# === C1：单圈跨味 Λ^(3) 复核 ===
L5_1, L3_1 = Lambda_flavor_1loop(A_INV_MZ)
print(f"\nC1. 单圈跨味 Λ^(3)（谱值起步）= {L3_1:.1f} MeV、Λ^(5) = {L5_1:.1f} MeV")
check("C1 单圈跨味 Λ^(3) ≈ 121.8 MeV（复核 61B 跨味脚本）",
      abs(L3_1 - 121.8) < 2.0, f"(Λ^(3) = {L3_1:.1f})")

# === C2：两圈跨味 pole 复核 ===
L3_2 = two_loop_pole(A_INV_MZ)
print(f"\nC2. 两圈跨味 pole Λ^(3) = {L3_2:.1f} MeV（61C 报告 578，漂移带上界）")
check("C2 两圈跨味 pole ∈ [450, 750] MeV（复核 61C 非微扰脚本）",
      450 <= L3_2 <= 750, f"(Λ^(3)_2loop = {L3_2:.1f})")

# === C3：F_π 谱公式反解 Λ_eff + 圈阶漂移带包含 ===
lam_eff = F_PI / (math.sqrt(N_C) * (RATIO_DL / (4 * math.pi)) * C_QCD)
print(f"\nC3. F_π 谱公式反解 Λ_eff = F_π/(√N_c·(Δλ₃/4πΔλ_min)·C_QCD)")
print(f"    = {F_PI}/({math.sqrt(N_C):.4f}·{(RATIO_DL/(4*math.pi)):.5f}·{C_QCD}) = {lam_eff:.1f} MeV")
print(f"    圈阶漂移带 [Λ^(3)_1loop, Λ^(3)_2loop] = [{L3_1:.0f}, {L3_2:.0f}] MeV")
print(f"    Λ_eff = {lam_eff:.0f} 落在带内：{L3_1:.0f} < {lam_eff:.0f} < {L3_2:.0f}")
check("C3 F_π 反解 Λ_eff ≈ 210 MeV 且落在圈阶漂移带内（证据 A）",
      abs(lam_eff - 210.0) < 2.0 and L3_1 < lam_eff < L3_2,
      f"(Λ_eff = {lam_eff:.1f}, 带 [{L3_1:.0f}, {L3_2:.0f}])")

# === C4：DS 非微扰桥：Δ_dress = κ·Λ_eff ≈ M(0) ===
d_dress = KAPPA * lam_eff
print(f"\nC4. DS 非微扰桥：Δ_dress = κ·Λ_eff = {KAPPA}·{lam_eff:.1f} = {d_dress:.1f} MeV")
print(f"    DS 动力学质量 M(0)(d_AB = 1.485) = {M0_DS} MeV（推论 5.9，完整 A/B 耦合）")
dev_m0 = abs(d_dress - M0_DS) / M0_DS * 100
check("C4 Δ_dress = κΛ_eff ≈ DS 动力学质量 M(0)（证据 B，偏差 < 2%）",
      dev_m0 < 2.0, f"(Δ_dress = {d_dress:.1f}, M(0) = {M0_DS}, 偏差 {dev_m0:.1f}%)")

# === C5：有效性反证：Λ_pert vs Λ_eff 谱定 m_ρ ===
def m_rho(Lam):
    return 2 * (M_UD + KAPPA * Lam)
mrho_pert = m_rho(L3_1)
mrho_eff = m_rho(lam_eff)
dev_pert = abs(mrho_pert - PDG_M_RHO) / PDG_M_RHO * 100
dev_eff = abs(mrho_eff - PDG_M_RHO) / PDG_M_RHO * 100
print(f"\nC5. 有效性反证：m_ρ(Λ) = 2·(m_ud + κΛ)")
print(f"    微扰 Λ_pert = {L3_1:.1f} → m_ρ = {mrho_pert:.1f} MeV（偏差 {dev_pert:.1f}%，不可用）")
print(f"    有效 Λ_eff = {lam_eff:.1f} → m_ρ = {mrho_eff:.1f} MeV（偏差 {dev_eff:.1f}%，定理 5.3 预言）")
check("C5 微扰标度谱定 m_ρ 偏差 > 30%（不可用）；有效标度偏差 < 5%（证据 C）",
      dev_pert > 30 and dev_eff < 5.0,
      f"(m_ρ(Λ_pert) = {mrho_pert:.0f} {dev_pert:.1f}%, m_ρ(Λ_eff) = {mrho_eff:.0f} {dev_eff:.1f}%)")

# === C6：衔接闭式 ξ = Λ_eff/Λ_pert ≈ √N_c ===
xi = lam_eff / L3_1
sqrt_nc = math.sqrt(N_C)
dev_xi = abs(xi - sqrt_nc) / sqrt_nc * 100
print(f"\nC6. 衔接闭式登记：ξ = Λ_eff/Λ_pert = {lam_eff:.1f}/{L3_1:.1f} = {xi:.4f}")
print(f"    √N_c = √3 = {sqrt_nc:.4f}（偏差 {dev_xi:.1f}%）—— 谱量近似，机制性存疑诚实边界")
check("C6 衔接闭式 ξ ≈ √N_c（偏差 < 1%，登记谱量近似）",
      dev_xi < 1.0, f"(ξ = {xi:.4f}, √N_c = {sqrt_nc:.4f}, 偏差 {dev_xi:.1f}%)")

# === 汇总 ===
print("\n" + "=" * 72)
n_pass = sum(1 for _, c, _ in checks if c)
print(f"汇总: {n_pass}/{len(checks)} 检查通过")
if n_pass != len(checks):
    raise SystemExit(f"FAIL: {len(checks)-n_pass} 项未通过")

print("\n关键数值（笔记引用）：")
print(f"  微扰链：单圈跨味 Λ^(3) = {L3_1:.1f} MeV → 两圈 pole = {L3_2:.1f} MeV（漂移带 [{L3_1:.0f}, {L3_2:.0f}]）")
print(f"  单圈跨味 Λ^(5) = {L5_1:.1f} MeV（比值 Λ^(3)/Λ^(5) = {L3_1/L5_1:.3f}，PDG 5-loop 1.558）")
print(f"  F_π 定标 Λ_eff = {lam_eff:.1f} MeV（圈阶无关有效标度，落在带内）")
print(f"  DS 桥：Δ_dress = {d_dress:.1f} MeV ≈ M(0)(d_AB) = {M0_DS} MeV（偏差 {dev_m0:.1f}%）")
print(f"  反证：m_ρ(Λ_pert) = {mrho_pert:.0f} MeV（{dev_pert:.1f}%）vs m_ρ(Λ_eff) = {mrho_eff:.0f} MeV（{dev_eff:.1f}%）")
print(f"  衔接闭式：ξ = {xi:.4f} ≈ √N_c = {sqrt_nc:.4f}（偏差 {dev_xi:.1f}%）")
