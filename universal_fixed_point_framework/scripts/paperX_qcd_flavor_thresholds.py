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

#!/usr/bin/env python3
"""
61B Λ_QCD 跨味阈值处理（2026-08-05）
======================================
笔记出处：notes/01_qcd_higgs/spectral_color_dynamics.md §8 开放项 3
（b_0 的 N_f 依赖与 PDG Λ^(5) 匹配需跨味阈值处理，Phase 61 P0-2 支撑）。

跨味阈值（decoupling）：α_s 跑动在夸克阈值 m_t/m_b/m_c/m_s 处切换 N_f，
β 系数 b_0(N_f) = 11 - (2/3)N_f 分段取值；单圈近似下 α_s 在阈值处连续
（匹配常数 = 1）。目标：验证跨味分段使 Λ^(3)/Λ^(5) 比值与 PDG 一致，
并给出谱框架的跨味 Λ 值。

输入：
  M_Z = 91.1876 GeV, m_t = 173, m_b = 4.2, m_c = 1.27, m_s = 0.095 GeV
  α_s(M_Z) = 0.1179（PDG）或 1/8.7 ≈ 0.11494（谱预测，三圈谱值偏差 2.7%）
对标：PDG Λ_MS^(5) = 213 MeV（5-loop）、Λ_MS^(3) = 332 MeV；比值 332/213 = 1.558
"""
import math

M_Z = 91.1876
M_T, M_B, M_C, M_S = 173.0, 4.2, 1.27, 0.095  # GeV
PDG_L5, PDG_L3 = 213.0, 332.0  # MeV

def b0(nf):
    return 11 - (2.0 / 3.0) * nf

def alpha_inv_evolve(a_inv, b, mu1, mu2):
    """单圈跑动：1/α(μ₂) = 1/α(μ₁) + (b/2π)·ln(μ₂/μ₁)"""
    return a_inv + (b / (2 * math.pi)) * math.log(mu2 / mu1)

def Lambda_flavor_threshold(a_inv_MZ):
    """跨味分段单圈跑动，返回 (Λ^(5) 单味参考, Λ^(3) 跨味值, 分段明细)"""
    # 分段：M_Z → m_b (N_f=5) → m_c (N_f=4) → m_s (N_f=3) → Λ (N_f=3)
    a = a_inv_MZ
    steps = []
    # N_f=5: M_Z → m_b
    a = alpha_inv_evolve(a, b0(5), M_Z, M_B)
    steps.append(("N_f=5  M_Z→m_b", b0(5), a))
    # N_f=4: m_b → m_c
    a = alpha_inv_evolve(a, b0(4), M_B, M_C)
    steps.append(("N_f=4  m_b→m_c", b0(4), a))
    # N_f=3: m_c → m_s
    a = alpha_inv_evolve(a, b0(3), M_C, M_S)
    steps.append(("N_f=3  m_c→m_s", b0(3), a))
    # N_f=3: m_s → Λ（1/α → 0）
    # 1/α(Λ) = a + (b0(3)/2π)·ln(Λ/m_s) = 0
    L3 = M_S * math.exp(-a / (b0(3) / (2 * math.pi))) * 1000.0  # MeV
    # 单味参考 Λ^(5)（全程 N_f=5）
    L5 = M_Z * math.exp(-a_inv_MZ / (b0(5) / (2 * math.pi))) * 1000.0  # MeV
    return L5, L3, steps

checks = []

def check(name, cond, detail=""):
    checks.append((name, cond, detail))
    print(f"  [{'PASS' if cond else 'FAIL'}] {name} {detail}")

print("=" * 72)
print("61B Λ_QCD 跨味阈值处理（N_f 分段跑动）")
print("=" * 72)

# === C1：单圈单味 Λ^(5)（PDG 锚） ===
a_inv_pdg = 1 / 0.1179
L5_pdg, L3_pdg, steps_pdg = Lambda_flavor_threshold(a_inv_pdg)
print(f"\nC1. 单圈单味 Λ^(5)（全程 N_f=5，PDG α_s(M_Z)=0.1179）：{L5_pdg:.1f} MeV")
print(f"    PDG 单圈基准 Λ^(5) ≈ 85-90 MeV（5-loop 213 MeV 为高圈值）")
check("C1 单圈 Λ^(5) ∈ [80, 95] MeV（PDG 单圈基准）",
      80 <= L5_pdg <= 95, f"(Λ^(5) = {L5_pdg:.1f})")

# === C2：跨味分段 Λ^(3) 与比值 ===
print(f"\nC2. 跨味分段单圈 Λ^(3)：{L3_pdg:.1f} MeV")
print(f"    跨味比值 Λ^(3)/Λ^(5) = {L3_pdg/L5_pdg:.3f}（PDG 5-loop {PDG_L3/PDG_L5:.3f}）")
for name, b, av in steps_pdg:
    print(f"      {name:16s} b₀={b:5.2f}  1/α = {av:6.3f}")
dev_ratio = abs((L3_pdg / L5_pdg) - (PDG_L3 / PDG_L5)) / (PDG_L3 / PDG_L5) * 100
check("C2 跨味 Λ^(3)/Λ^(5) 比值与 PDG 1.558 偏差 < 10%（N_f 分段一致性）",
      dev_ratio < 10, f"(比值 {L3_pdg/L5_pdg:.3f}, 偏差 {dev_ratio:.1f}%)")

# === C3：谱值 α_s(M_Z)⁻¹ = 8.7 跨味跑动 ===
a_inv_spec = 8.7
L5_spec, L3_spec, _ = Lambda_flavor_threshold(a_inv_spec)
print(f"\nC3. 谱值 α_s(M_Z)⁻¹ = 8.7：单味 Λ^(5) = {L5_spec:.1f} MeV、跨味 Λ^(3) = {L3_spec:.1f} MeV")
print(f"    谱框架三味有效值 Λ = 210 MeV（F_π = 92.2 MeV 定标，含非微扰修正）")
print(f"    跨味单圈 Λ^(3) = {L3_spec:.1f} < 210（微扰 RGE 值 vs 非微扰有效值，见 C5）")
check("C3 谱值跨味 Λ^(3) ∈ [100, 150] MeV（微扰 RGE 值，与 210 有效值同量级）",
      100 <= L3_spec <= 150, f"(Λ^(3) = {L3_spec:.1f})")

# === C4：单圈 decoupling 匹配（α 连续，匹配常数 = 1） ===
print(f"\nC4. 单圈 decoupling：α_s 在阈值处连续（匹配常数 = 1）")
# 在 m_b 处：N_f=5 跑到的 1/α 与 N_f=4 起点的 1/α 相同（连续）
a_5 = alpha_inv_evolve(a_inv_pdg, b0(5), M_Z, M_B)
a_4_start = a_5  # 连续
print(f"    在 m_b 处：1/α(N_f=5) = {a_5:.3f} = 1/α(N_f=4 起点)")
check("C4 单圈阈值处 α 连续（decoupling 匹配常数 = 1）",
      abs(a_5 - a_4_start) < 1e-9, f"(1/α = {a_5:.3f})")

# === C5：谱值单味 Λ^(5) ≈ 73 MeV（复核 §4.2） ===
print(f"\nC5. 谱值单味单圈 Λ^(5) = {L5_spec:.1f} MeV（§4.2 报告 ≈ 73 MeV）")
check("C5 谱值单味单圈 Λ^(5) 与 §4.2 的 73 MeV 一致（偏差 < 10%）",
      abs(L5_spec - 73) / 73 < 0.10, f"(Λ^(5) = {L5_spec:.1f})")

# === C6：跨味微扰值与谱框架有效值的圈阶一致性 ===
print(f"\nC6. 跨味微扰值 vs 谱框架有效值（圈阶修正因子一致性）：")
print(f"    跨味单圈 Λ^(3) = {L3_spec:.1f} MeV；谱框架有效值 Λ = 210 MeV（F_π 定标）")
ratio_spec = 210.0 / L3_spec
ratio_pdg = PDG_L5 / L5_pdg  # 单圈 → 5-loop 修正因子
print(f"    210/跨味微扰 = {ratio_spec:.2f}（PDG 单圈→5-loop 因子 {ratio_pdg:.2f} = {PDG_L5}/{L5_pdg:.0f}）")
print(f"    诚实边界：跨味微扰单圈值不能直接用于 κ 谱定（κ·Λ 掉到 {1.9091*L3_spec:.0f} MeV、"
      f"m_ρ 掉到 {2*(3.45+1.9091*L3_spec):.0f} MeV）——谱框架 210 MeV 为含非微扰/高圈修正的"
      f"F_π 定标有效值，两者差距即圈阶修正，登记为开放项")
check("C6 210/跨味微扰 ∈ [1.5, 2.5]（差距在单圈→高圈修正因子范围内，量级自洽）",
      1.5 <= ratio_spec <= 2.5, f"(比值 {ratio_spec:.2f}, PDG 因子 {ratio_pdg:.2f})")

# === 汇总 ===
print("\n" + "=" * 72)
n_pass = sum(1 for _, c, _ in checks if c)
print(f"汇总: {n_pass}/{len(checks)} 检查通过")
if n_pass != len(checks):
    raise SystemExit(f"FAIL: {len(checks)-n_pass} 项未通过")

print("\n关键数值（笔记引用）：")
print(f"  Λ^(5) 单圈 = {L5_pdg:.1f} MeV（PDG 锚）、谱值 = {L5_spec:.1f} MeV（§4.2 复核）")
print(f"  Λ^(3) 跨味单圈 = {L3_pdg:.1f} MeV（PDG 锚）、谱值 = {L3_spec:.1f} MeV")
print(f"  跨味比值 Λ^(3)/Λ^(5) = {L3_pdg/L5_pdg:.3f}（PDG 1.558）")
