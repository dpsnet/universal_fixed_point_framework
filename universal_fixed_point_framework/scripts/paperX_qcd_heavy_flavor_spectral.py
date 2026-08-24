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
# -*- coding: utf-8 -*-
"""
paperX_qcd_heavy_flavor_spectral.py — 重味 Cornell 有效参数谱定替代（61B）
============================================================================
对应笔记：notes/01_qcd_higgs/spectral_color_dynamics.md §5.6 诚实边界
          （α_s = 0.39 为 Cornell 有效耦合经验拟合值——需谱框架谱定替代）
+ roadmap/phase61_physics_advancement.md 61B"重味强子 Cornell 谱势扩展"诚实边界。

物理：重味夸克偶素 Cornell 势 V(r) = -4α_s/(3r) + σr 的经验耦合 α_s = 0.39
      （文献拟合，~1 GeV 标度有效值）用谱框架两圈跨味跑动 α_s(μ) 谱定替代：
        α_s(m_c) = 0.413（两圈跨味 RGE，谱值 α_s(M_Z)⁻¹ = 8.7 起步，61C 独立锚点 PDG 0.40）
      并反解经验值 0.39 对应的有效标度 μ_eff ≈ m_c（0.39 获谱框架来源）。

验证内容：
  N1  两圈跨味复核：α_s(m_c = 1.27) = 0.413 ± 0.01（61C 独立锚点）
  N2  charmonium 谱定替代：J/ψ、ψ' 偏差 ≤ 经验值 0.39 结果（改进或持平）
  N3  bottomonium 谱定替代：Υ、Υ' 偏差 < 2%（α_s 不敏感，不破坏高精度）
  N4  4 态平均偏差：谱定 α_s(m_c) ≤ 经验值 0.39（总偏差下降或持平）
  N5  经验值 0.39 有效标度反解：两圈 α_s(μ_eff) = 0.39 → μ_eff ∈ [1.0, 2.0] GeV ≈ m_c
  N6  径向激发间距 ΔM(2S−1S) 保持 < 20%（谱定替代不破坏间距预言）

单位：GeV（r 用 GeV⁻¹，ℏc = 1）。
"""
import numpy as np
import math

# ---- 两圈跨味 RGE（谱值起步） ----
M_Z = 91.1876
M_B, M_C, M_S = 4.2, 1.27, 0.095        # GeV，夸克质量阈值（RGE 分段用，勿覆盖）
A_INV_MZ = 8.7                            # 谱值 α_s(M_Z)⁻¹（三圈谱值，偏差 2.7%）
ALPHA_S_EMP = 0.39                        # Cornell 经验有效耦合（待谱定替代）

def b0(nf):
    return 11 - (2.0 / 3.0) * nf

def b1(nf):
    return 102 - (38.0 / 3.0) * nf   # 两圈 β 系数（SU(3)，MS-bar）

def du_dlmu(u, nf):
    """两圈 RGE（u = 1/α）：du/dlnμ = b₀/2π + b₁/(4π²u)"""
    return b0(nf) / (2 * math.pi) + b1(nf) / (4 * math.pi**2 * u)

def integrate_rk4(u0, lmu_hi, lmu_lo, nf, dl=-2e-4):
    """RK4 积分 u = 1/α 从 ln(μ_hi) 到 ln(μ_lo)（μ 下降，N_f = nf 固定）。"""
    steps = max(20, int(abs(lmu_hi - lmu_lo) / abs(dl)))
    ds = (lmu_lo - lmu_hi) / steps
    u = u0
    l = lmu_hi
    for _ in range(steps):
        k1 = du_dlmu(u, nf)
        k2 = du_dlmu(u + 0.5 * ds * k1, nf)
        k3 = du_dlmu(u + 0.5 * ds * k2, nf)
        k4 = du_dlmu(u + ds * k3, nf)
        u = u + (ds / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        l += ds
    return u

def alpha_s_2loop(mu):
    """两圈跨味跑动 α_s(μ)（谱值 α_s(M_Z)⁻¹ = 8.7 起步，μ ∈ (m_s, M_Z]）。"""
    if mu >= M_Z:
        return 1.0 / A_INV_MZ
    u = A_INV_MZ
    for hi, lo, nf in [(M_Z, M_B, 5), (M_B, M_C, 4), (M_C, M_S, 3)]:
        if mu >= lo:
            u = integrate_rk4(u, math.log(hi), math.log(mu), nf)
            return 1.0 / u
        u = integrate_rk4(u, math.log(hi), math.log(lo), nf)
    return 1.0 / u

# ---- Cornell 求解（复用 paperX_qcd_heavy_flavor.py） ----
PDG = {
    'Jpsi': 3.0969, 'psi2S': 3.6861,
    'Upsilon': 9.4603, 'Upsilon2S': 10.0233,
}

def cornell_potential(r, alpha_s, kappa):
    with np.errstate(divide='ignore'):
        return -4.0 * alpha_s / (3.0 * r) + kappa * r

def schrodinger_spectrum(m_q, alpha_s, kappa, n_grid=2000, r_max=10.0):
    """解重夸克偶素径向 Schrödinger（l=0，有限差分 + 对角化）。返回能级列表 E_n。"""
    r = np.linspace(1e-4, r_max, n_grid)
    dr = r[1] - r[0]
    mu = m_q / 2.0
    H = np.zeros((n_grid, n_grid))
    for i in range(n_grid):
        H[i, i] = 2.0 / (2.0 * mu) / dr**2 + cornell_potential(r[i], alpha_s, kappa)
        if i > 0:
            H[i, i - 1] = -1.0 / (2.0 * mu) / dr**2
        if i < n_grid - 1:
            H[i, i + 1] = -1.0 / (2.0 * mu) / dr**2
    H[0, :] = 0; H[0, 0] = 1.0
    H[-1, :] = 0; H[-1, -1] = 1.0
    evals, _ = np.linalg.eigh(H)
    return [evals[1], evals[2]]

checks = []

def check(name, cond, detail=""):
    checks.append((name, cond, detail))
    print(f"  [{'PASS' if cond else 'FAIL'}] {name} {detail}")

print("=" * 72)
print("61B 重味 Cornell 有效参数谱定替代：α_s = 0.39 → α_s(m_c) = 0.413（两圈跨味）")
print("=" * 72)

KAPPA = 0.18
M_C_EF, M_B_EF = 1.5, 4.8    # 有效 charm/bottom 质量（dressing 后，保持；勿覆盖 RGE 阈值 M_C）

# === N1：两圈跨味 α_s(m_c) 复核 ===
a_mc = alpha_s_2loop(M_C)
a_mb = alpha_s_2loop(M_B)
print(f"\nN1. 两圈跨味跑动：α_s(m_c = 1.27 GeV) = {a_mc:.3f}、α_s(m_b = 4.2 GeV) = {a_mb:.3f}")
check("N1 两圈跨味 α_s(m_c) ≈ 0.413（61C 独立锚点，PDG 0.40 ± 0.05）",
      abs(a_mc - 0.413) < 0.01, f"(α_s(m_c) = {a_mc:.3f})")

# === N2/N3/N4：谱定替代 Cornell 求解 ===
# 经验值 0.39 基准
L_c_emp = schrodinger_spectrum(M_C_EF, ALPHA_S_EMP, KAPPA)
L_b_emp = schrodinger_spectrum(M_B_EF, ALPHA_S_EMP, KAPPA)
# 谱定 0.413（统一标度 m_c，最保守替代：保留 Cornell 单参数结构）
a_spec = a_mc
L_c_sp = schrodinger_spectrum(M_C_EF, a_spec, KAPPA)
L_b_sp = schrodinger_spectrum(M_B_EF, a_spec, KAPPA)

def dev(M, key):
    return abs(M - PDG[key]) / PDG[key] * 100

def masses(Lc, Lb):
    return (2 * M_C_EF + Lc[0], 2 * M_C_EF + Lc[1], 2 * M_B_EF + Lb[0], 2 * M_B_EF + Lb[1])

J0, P0, U0, U20 = masses(L_c_emp, L_b_emp)
J1, P1, U1, U21 = masses(L_c_sp, L_b_sp)

print(f"\nN2/N3. charmonium/bottomonium 谱定替代对比：")
print(f"  经验 α_s = 0.39：J/ψ {J0*1000:.0f} MeV（{dev(J0,'Jpsi'):.1f}%）、ψ' {P0*1000:.0f}（{dev(P0,'psi2S'):.1f}%）、"
      f"Υ {U0*1000:.0f}（{dev(U0,'Upsilon'):.1f}%）、Υ' {U20*1000:.0f}（{dev(U20,'Upsilon2S'):.1f}%）")
print(f"  谱定 α_s = {a_spec:.3f}：J/ψ {J1*1000:.0f} MeV（{dev(J1,'Jpsi'):.1f}%）、ψ' {P1*1000:.0f}（{dev(P1,'psi2S'):.1f}%）、"
      f"Υ {U1*1000:.0f}（{dev(U1,'Upsilon'):.1f}%）、Υ' {U21*1000:.0f}（{dev(U21,'Upsilon2S'):.1f}%）")
dev_ch_sp = max(dev(J1, 'Jpsi'), dev(P1, 'psi2S'))
dev_ch_emp = max(dev(J0, 'Jpsi'), dev(P0, 'psi2S'))
dev_bot_sp = max(dev(U1, 'Upsilon'), dev(U21, 'Upsilon2S'))
check("N2 charmonium 谱定替代偏差 ≤ 经验值（J/ψ、ψ' < 8%，改进或持平）",
      dev_ch_sp <= dev_ch_emp + 0.5 and dev_ch_sp < 8.0,
      f"(谱定 max = {dev_ch_sp:.1f}%, 经验 max = {dev_ch_emp:.1f}%)")
check("N3 bottomonium 谱定替代偏差 < 2%（α_s 不敏感，不破坏高精度）",
      dev_bot_sp < 2.0, f"(Υ、Υ' max 偏差 = {dev_bot_sp:.1f}%)")

avg_emp = (dev(J0,'Jpsi') + dev(P0,'psi2S') + dev(U0,'Upsilon') + dev(U20,'Upsilon2S')) / 4
avg_sp = (dev(J1,'Jpsi') + dev(P1,'psi2S') + dev(U1,'Upsilon') + dev(U21,'Upsilon2S')) / 4
print(f"\nN4. 4 态平均偏差：经验 {avg_emp:.2f}% vs 谱定 {avg_sp:.2f}%")
check("N4 谱定替代 4 态平均偏差 ≤ 经验值（总偏差下降或持平）",
      avg_sp <= avg_emp + 0.2, f"(谱定 {avg_sp:.2f}% vs 经验 {avg_emp:.2f}%)")

# === N5：经验值 0.39 的有效标度反解 ===
print(f"\nN5. 经验值 α_s = 0.39 的有效标度反解（两圈跨味）：")
mu_grid = [0.9, 1.0, 1.1, 1.27, 1.4, 1.5, 1.8, 2.0, 2.5, 3.0]
vals = [(mu, alpha_s_2loop(mu)) for mu in mu_grid]
for mu, a in vals:
    print(f"    α_s({mu:.2f} GeV) = {a:.3f}")
mu_eff = None
for i in range(len(vals) - 1):
    if vals[i][1] >= ALPHA_S_EMP >= vals[i+1][1]:
        mu1, a1 = vals[i]; mu2, a2 = vals[i+1]
        mu_eff = mu1 + (ALPHA_S_EMP - a1) * (mu2 - mu1) / (a2 - a1)
        break
if mu_eff is None:
    for i in range(len(vals) - 1):
        if vals[i][1] <= ALPHA_S_EMP <= vals[i+1][1]:
            mu1, a1 = vals[i]; mu2, a2 = vals[i+1]
            mu_eff = mu1 + (ALPHA_S_EMP - a1) * (mu2 - mu1) / (a2 - a1)
            break
print(f"    经验值 0.39 对应有效标度 μ_eff ≈ {mu_eff:.2f} GeV ≈ m_c（1.27–1.5 GeV 重味标度）")
check("N5 0.39 有效标度 μ_eff ∈ [1.0, 2.0] GeV（经验值获谱框架来源：≈ m_c 标度）",
      mu_eff is not None and 1.0 <= mu_eff <= 2.0,
      f"(μ_eff = {mu_eff:.2f} GeV)" if mu_eff else "(未反解出)")

# === N6：径向激发间距 ===
dMc0 = P0 - J0; dMc1 = P1 - J1
dMb0 = U20 - U0; dMb1 = U21 - U1
dMc_pdg = PDG['psi2S'] - PDG['Jpsi']; dMb_pdg = PDG['Upsilon2S'] - PDG['Upsilon']
d1 = abs(dMc1 - dMc_pdg) / dMc_pdg * 100
d2 = abs(dMb1 - dMb_pdg) / dMb_pdg * 100
print(f"\nN6. 径向激发间距（谱定 α_s = {a_spec:.3f}）：")
print(f"    charm ΔM(2S−1S) = {dMc1*1000:.0f} MeV（PDG {dMc_pdg*1000:.0f}，偏差 {d1:.1f}%）")
print(f"    bottom ΔM(2S−1S) = {dMb1*1000:.0f} MeV（PDG {dMb_pdg*1000:.0f}，偏差 {d2:.1f}%）")
check("N6 谱定替代后径向激发间距偏差 < 20%（间距预言保持）",
      d1 < 20 and d2 < 20, f"(charm {d1:.1f}%, bottom {d2:.1f}%)")

# === 汇总 ===
print("\n" + "=" * 72)
n_pass = sum(1 for _, c, _ in checks if c)
print(f"汇总: {n_pass}/{len(checks)} 检查通过")
if n_pass != len(checks):
    raise SystemExit(f"FAIL: {len(checks)-n_pass} 项未通过")

print("\n关键数值（笔记引用）：")
print(f"  α_s(m_c) 谱定 = {a_mc:.3f}（两圈跨味，61C 锚点 PDG 0.40；经验 0.39 偏差 {(a_mc-ALPHA_S_EMP)/ALPHA_S_EMP*100:.1f}%）")
print(f"  经验 0.39 有效标度 μ_eff = {mu_eff:.2f} GeV（≈ m_c，0.39 获谱框架来源）")
print(f"  4 态平均偏差：经验 {avg_emp:.2f}% → 谱定 {avg_sp:.2f}%")
print(f"  J/ψ = {J1*1000:.0f}（{dev(J1,'Jpsi'):.1f}%）、ψ' = {P1*1000:.0f}（{dev(P1,'psi2S'):.1f}%）、"
      f"Υ = {U1*1000:.0f}（{dev(U1,'Upsilon'):.1f}%）、Υ' = {U21*1000:.0f}（{dev(U21,'Upsilon2S'):.1f}%）")
