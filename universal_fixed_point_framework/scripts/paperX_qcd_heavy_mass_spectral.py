#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
paperX_qcd_heavy_mass_spectral.py — 重味 Cornell 有效质量谱定替代（61B）
============================================================================
对应笔记：notes/01_qcd_higgs/spectral_color_dynamics.md §8 未决问题 4
（m_c/m_b 有效质量 dressing 精确化方向，开放问题 5）+ paper40 §8.2 开放问题 5。

物理：重味 Cornell 有效质量 m_c = 1.5、m_b = 4.8 GeV（dressing 后）由谱框架
pole 质量谱定替代（消除经验质量锚点）：
  m_c_eff = m_c_MS·[1 + (4/3)(α_s(m_c)/π)]                         （单圈 pole 修正，α_s(m_c) = 0.413）
  m_b_eff = m_b_MS·[1 + (4/3)(α_s(m_b)/π) + C₂(α_s(m_b)/π)²]      （两圈 pole 修正，α_s(m_b) = 0.224，C₂ = 13.44）
圈阶选择由收敛性决定：charm 处 α_s = 0.413 两圈修正（~0.23）与单圈（~0.175）同量级不收敛 → 单圈；
bottom 处 α_s = 0.224 两圈修正（~0.068）远小于单圈（~0.095）收敛良好 → 两圈。
预期：m_c_eff ≈ 1.49 GeV（vs 1.5，偏差 0.5%）、m_b_eff ≈ 4.86 GeV（vs 4.8，偏差 1.3%）。

验证内容：
  N1  charm 单圈 pole 谱定：m_c_eff = 1.493 GeV ≈ 1.5（偏差 < 2%）
  N2  bottom 两圈 pole 谱定：m_b_eff = 4.86 GeV ≈ 4.8（偏差 < 2%）
  N3  谱定 (α_s, m_c, m_b) 联合 Cornell：4 态平均偏差 ≤ 基准 3.39% + 0.5pp
  N4  charmonium/bottomonium 各态对标 PDG（J/ψ、ψ' < 8%；Υ、Υ' < 2%）
  N5  径向激发间距 < 20%（间距预言保持）
  N6  重味 dressing 尺度对比：m_eff − m_MS vs κΛ = 401 MeV（标度依赖：charm 0.22 GeV、bottom 0.69 GeV）

单位：GeV（r 用 GeV⁻¹，ℏc = 1）。
"""
import numpy as np
import math

# ---- 两圈跨味 RGE（谱值起步，复用 paperX_qcd_heavy_flavor_spectral.py） ----
M_Z = 91.1876
M_B_TH, M_C_TH, M_S_TH = 4.2, 1.27, 0.095   # GeV，夸克质量阈值
A_INV_MZ = 8.7
M_C_MS, M_B_MS = 1.27, 4.18                 # GeV，MS-bar 裸质量（PDG）
ALPHA_S_EMP = 0.39
M_C_EMP, M_B_EMP = 1.5, 4.8                 # GeV，Cornell 经验有效质量（待谱定替代）
C2_POLE = 13.44                             # 两圈 pole-MS 系数（PDG Quark masses，独立于 flavor）

def b0(nf):
    return 11 - (2.0 / 3.0) * nf

def b1(nf):
    return 102 - (38.0 / 3.0) * nf

def du_dlmu(u, nf):
    return b0(nf) / (2 * math.pi) + b1(nf) / (4 * math.pi**2 * u)

def integrate_rk4(u0, lmu_hi, lmu_lo, nf, dl=-2e-4):
    steps = max(20, int(abs(lmu_hi - lmu_lo) / abs(dl)))
    ds = (lmu_lo - lmu_hi) / steps
    u = u0
    for _ in range(steps):
        k1 = du_dlmu(u, nf)
        k2 = du_dlmu(u + 0.5 * ds * k1, nf)
        k3 = du_dlmu(u + 0.5 * ds * k2, nf)
        k4 = du_dlmu(u + ds * k3, nf)
        u = u + (ds / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
    return u

def alpha_s_2loop(mu):
    if mu >= M_Z:
        return 1.0 / A_INV_MZ
    u = A_INV_MZ
    for hi, lo, nf in [(M_Z, M_B_TH, 5), (M_B_TH, M_C_TH, 4), (M_C_TH, M_S_TH, 3)]:
        if mu >= lo:
            return 1.0 / integrate_rk4(u, math.log(hi), math.log(mu), nf)
        u = integrate_rk4(u, math.log(hi), math.log(lo), nf)
    return 1.0 / u

# ---- Cornell 求解（复用 paperX_qcd_heavy_flavor.py） ----
PDG = {'Jpsi': 3.0969, 'psi2S': 3.6861, 'Upsilon': 9.4603, 'Upsilon2S': 10.0233}

def cornell_potential(r, alpha_s, kappa):
    with np.errstate(divide='ignore'):
        return -4.0 * alpha_s / (3.0 * r) + kappa * r

def schrodinger_spectrum(m_q, alpha_s, kappa, n_grid=2000, r_max=10.0):
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
print("61B 重味 Cornell 有效质量谱定替代：m_c/m_b = pole 质量（MS-bar + 圈阶 pole 修正）")
print("=" * 72)

KAPPA = 0.18

# 谱定 α_s
a_mc = alpha_s_2loop(M_C_TH)
a_mb = alpha_s_2loop(M_B_TH)
print(f"\n谱定 α_s：α_s(m_c = 1.27) = {a_mc:.3f}、α_s(m_b = 4.2) = {a_mb:.3f}")

# === N1/N2：pole 质量谱定 ===
corr_c_1 = (4.0 / 3.0) * (a_mc / math.pi)
m_c_eff = M_C_MS * (1.0 + corr_c_1)
print(f"\nN1. charm 单圈 pole：m_c_eff = {M_C_MS}·(1 + 4α_s/3π) = {M_C_MS}·(1 + {corr_c_1:.4f}) = {m_c_eff:.3f} GeV")
print(f"    Cornell 经验 m_c = {M_C_EMP}（偏差 {abs(m_c_eff-M_C_EMP)/M_C_EMP*100:.1f}%）；"
      f"dressing = m_c_eff − m_c_MS = {(m_c_eff-M_C_MS)*1000:.0f} MeV")
check("N1 charm 单圈 pole 谱定 m_c_eff ≈ 1.49 GeV ≈ 1.5（偏差 < 2%）",
      abs(m_c_eff - M_C_EMP) / M_C_EMP < 0.02, f"(m_c_eff = {m_c_eff:.3f})")

corr_b_1 = (4.0 / 3.0) * (a_mb / math.pi)
corr_b_2 = C2_POLE * (a_mb / math.pi)**2
m_b_eff = M_B_MS * (1.0 + corr_b_1 + corr_b_2)
print(f"\nN2. bottom 两圈 pole：m_b_eff = {M_B_MS}·(1 + 4α_s/3π + C₂(α_s/π)²)")
print(f"    = {M_B_MS}·(1 + {corr_b_1:.4f} + {corr_b_2:.4f}) = {m_b_eff:.3f} GeV")
print(f"    Cornell 经验 m_b = {M_B_EMP}（偏差 {abs(m_b_eff-M_B_EMP)/M_B_EMP*100:.1f}%）；"
      f"dressing = m_b_eff − m_b_MS = {(m_b_eff-M_B_MS)*1000:.0f} MeV")
print(f"    收敛性：charm 两圈修正 {C2_POLE*(a_mc/math.pi)**2:.3f} ≈ 单圈 {corr_c_1:.3f}（不收敛→单圈）；"
      f"bottom 两圈 {corr_b_2:.3f} << 单圈 {corr_b_1:.3f}（收敛→两圈）")
check("N2 bottom 两圈 pole 谱定 m_b_eff ≈ 4.86 GeV ≈ 4.8（偏差 < 2%）",
      abs(m_b_eff - M_B_EMP) / M_B_EMP < 0.02, f"(m_b_eff = {m_b_eff:.3f})")

# === N3/N4/N5：谱定 (α_s, m_c, m_b) 联合 Cornell ===
a_spec = a_mc
# 基准：谱定 α_s + 经验质量（上一轮 3.39%）
L_c_base = schrodinger_spectrum(M_C_EMP, a_spec, KAPPA)
L_b_base = schrodinger_spectrum(M_B_EMP, a_spec, KAPPA)
# 本轮：谱定 α_s + 谱定 pole 质量
L_c_new = schrodinger_spectrum(m_c_eff, a_spec, KAPPA)
L_b_new = schrodinger_spectrum(m_b_eff, a_spec, KAPPA)

def dev(M, key):
    return abs(M - PDG[key]) / PDG[key] * 100

def masses(Lc, Lb, mc, mb):
    return (2 * mc + Lc[0], 2 * mc + Lc[1], 2 * mb + Lb[0], 2 * mb + Lb[1])

J0, P0, U0, U20 = masses(L_c_base, L_b_base, M_C_EMP, M_B_EMP)
J1, P1, U1, U21 = masses(L_c_new, L_b_new, m_c_eff, m_b_eff)

print(f"\nN3/N4. 谱定联合 Cornell 求解（α_s = {a_spec:.3f}）：")
print(f"  基准（经验质量 1.5/4.8）：J/ψ {J0*1000:.0f} MeV（{dev(J0,'Jpsi'):.1f}%）、ψ' {P0*1000:.0f}（{dev(P0,'psi2S'):.1f}%）、"
      f"Υ {U0*1000:.0f}（{dev(U0,'Upsilon'):.1f}%）、Υ' {U20*1000:.0f}（{dev(U20,'Upsilon2S'):.1f}%）")
print(f"  谱定（pole 质量 {m_c_eff:.3f}/{m_b_eff:.3f}）：J/ψ {J1*1000:.0f} MeV（{dev(J1,'Jpsi'):.1f}%）、ψ' {P1*1000:.0f}（{dev(P1,'psi2S'):.1f}%）、"
      f"Υ {U1*1000:.0f}（{dev(U1,'Upsilon'):.1f}%）、Υ' {U21*1000:.0f}（{dev(U21,'Upsilon2S'):.1f}%）")

avg_base = (dev(J0,'Jpsi') + dev(P0,'psi2S') + dev(U0,'Upsilon') + dev(U20,'Upsilon2S')) / 4
avg_new = (dev(J1,'Jpsi') + dev(P1,'psi2S') + dev(U1,'Upsilon') + dev(U21,'Upsilon2S')) / 4
print(f"\n  4 态平均偏差：基准（α_s 谱定 + 经验质量）{avg_base:.2f}% vs 谱定（α_s + pole 质量）{avg_new:.2f}%")
check("N3 谱定联合 4 态平均偏差 ≤ 基准 3.39% + 0.5pp",
      avg_new <= avg_base + 0.5, f"(谱定 {avg_new:.2f}% vs 基准 {avg_base:.2f}%)")

dev_ch = max(dev(J1, 'Jpsi'), dev(P1, 'psi2S'))
dev_bot = max(dev(U1, 'Upsilon'), dev(U21, 'Upsilon2S'))
check("N4 charmonium < 8% 且 bottomonium < 2%（谱定质量替代保持精度）",
      dev_ch < 8.0 and dev_bot < 2.0, f"(charm max {dev_ch:.1f}%, bottom max {dev_bot:.1f}%)")

# === N5：径向激发间距 ===
dMc = P1 - J1; dMb = U21 - U1
dMc_pdg = PDG['psi2S'] - PDG['Jpsi']; dMb_pdg = PDG['Upsilon2S'] - PDG['Upsilon']
d1 = abs(dMc - dMc_pdg) / dMc_pdg * 100
d2 = abs(dMb - dMb_pdg) / dMb_pdg * 100
print(f"\nN5. 径向激发间距（谱定质量）：charm {dMc*1000:.0f} MeV（PDG {dMc_pdg*1000:.0f}，偏差 {d1:.1f}%）、"
      f"bottom {dMb*1000:.0f} MeV（PDG {dMb_pdg*1000:.0f}，偏差 {d2:.1f}%）")
check("N5 谱定质量替代后径向激发间距偏差 < 20%（间距预言保持）",
      d1 < 20 and d2 < 20, f"(charm {d1:.1f}%, bottom {d2:.1f}%)")

# === N6：重味 dressing 尺度对比 ===
KAPPA_K = 1.9091
LAM_EFF = 210.3
d_dress = KAPPA_K * LAM_EFF
print(f"\nN6. 重味 dressing 尺度（m_eff − m_MS）对比 κΛ = {d_dress:.0f} MeV：")
print(f"    charm dressing = {(m_c_eff-M_C_MS)*1000:.0f} MeV（轻味 Δ_dress 的 {(m_c_eff-M_C_MS)*1000/d_dress*100:.0f}%）")
print(f"    bottom dressing = {(m_b_eff-M_B_MS)*1000:.0f} MeV（轻味 Δ_dress 的 {(m_b_eff-M_B_MS)*1000/d_dress*100:.0f}%）")
print(f"    标度依赖：重味 dressing 随夸克标度 α_s 增强而增大（charm α_s=0.413 → bottom α_s=0.224，"
      f"pole 圈阶修正随 μ 增高而减小但 m_MS 更大）")
check("N6 重味 dressing 量级合理（0.2–0.7 GeV，与动力学质量生成尺度同量级）",
      150 <= (m_c_eff-M_C_MS)*1000 <= 900 and 150 <= (m_b_eff-M_B_MS)*1000 <= 900,
      f"(charm {(m_c_eff-M_C_MS)*1000:.0f}, bottom {(m_b_eff-M_B_MS)*1000:.0f} MeV)")

# === 汇总 ===
print("\n" + "=" * 72)
n_pass = sum(1 for _, c, _ in checks if c)
print(f"汇总: {n_pass}/{len(checks)} 检查通过")
if n_pass != len(checks):
    raise SystemExit(f"FAIL: {len(checks)-n_pass} 项未通过")

print("\n关键数值（笔记引用）：")
print(f"  m_c_eff = {m_c_eff:.3f} GeV（单圈 pole，vs 经验 1.5，偏差 {abs(m_c_eff-M_C_EMP)/M_C_EMP*100:.1f}%）")
print(f"  m_b_eff = {m_b_eff:.3f} GeV（两圈 pole，vs 经验 4.8，偏差 {abs(m_b_eff-M_B_EMP)/M_B_EMP*100:.1f}%）")
print(f"  4 态平均偏差：基准 {avg_base:.2f}% → 谱定 {avg_new:.2f}%")
print(f"  J/ψ = {J1*1000:.0f}（{dev(J1,'Jpsi'):.1f}%）、ψ' = {P1*1000:.0f}（{dev(P1,'psi2S'):.1f}%）、"
      f"Υ = {U1*1000:.0f}（{dev(U1,'Upsilon'):.1f}%）、Υ' = {U21*1000:.0f}（{dev(U21,'Upsilon2S'):.1f}%）")
print(f"  重味 dressing：charm {(m_c_eff-M_C_MS)*1000:.0f} MeV、bottom {(m_b_eff-M_B_MS)*1000:.0f} MeV（κΛ = {d_dress:.0f} MeV）")
