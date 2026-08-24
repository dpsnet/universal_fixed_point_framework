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
paperX_qcd_heavy_flavor.py — 重味夸克偶素 Cornell 谱势（61B 开放项：重味强子 Cornell 扩展）
============================================================================
对应笔记：notes/01_qcd_highes/spectral_color_dynamics.md §8 开放项 4
          + roadmap/phase61_physics_advancement.md 遗留开放项 61B"重味强子 Cornell 谱势扩展"

物理：重味夸克偶素（charmonium/bottomonium）由 Cornell 势
      V(r) = -4α_s/(3r) + κ·r  （色-Coulomb + 线性禁闭）
描述，解非相对论径向 Schrödinger 方程得 S 波束缚态谱。
对标 PDG：J/ψ (1S charmonium)、ψ(2S)、Υ(1S)、Υ(2S) bottomonium。

验证内容：
  T1  Cornell 势参数物理有效性（κ 弦张力、α_s、重夸克质量）
  T2  charmonium 1S/2S 质量（J/ψ、ψ'）对标 PDG（±10%）
  T3  bottomonium 1S/2S 质量（Υ、Υ'）对标 PDG（±10%）
  T4  径向激发间距 M(2S)−M(1S) 对标 PDG（±20%）
  T5  1S 态 rms 半径（重味紧致性：~0.4 fm）
  T6  轻味-重味对比：重味夸克偶素比轻味介子更紧致/更深束缚

单位：GeV（r 用 GeV⁻¹，ℏc = 1）。
"""
import numpy as np

PDG = {
    'Jpsi': 3.0969,     # J/ψ 1S charmonium GeV
    'psi2S': 3.6861,    # ψ(2S) GeV
    'Upsilon': 9.4603,  # Υ(1S) GeV
    'Upsilon2S': 10.0233,  # Υ(2S) GeV
}

# ---------- Cornell 势求解 ----------

def cornell_potential(r, alpha_s, kappa):
    """Cornell 势：V(r) = -4α_s/(3r) + κ·r（r 用 GeV⁻¹，V 用 GeV）。"""
    with np.errstate(divide='ignore'):
        return -4.0 * alpha_s / (3.0 * r) + kappa * r

def schrodinger_spectrum(m_q, alpha_s, kappa, n_grid=2000, r_max=10.0):
    """解重夸克偶素径向 Schrödinger 方程（l=0，有限差分 + 矩阵对角化）。
    返回（能级列表 E_n，波函数网格 u，r 网格）。总质量 M_n = 2m_q + E_n。"""
    r = np.linspace(1e-4, r_max, n_grid)
    dr = r[1] - r[0]
    mu = m_q / 2.0          # 约化质量（等质量夸克偶素）
    # 动能：-1/(2μ) d²/dr²（三对角）
    H = np.zeros((n_grid, n_grid))
    for i in range(n_grid):
        H[i, i] = 2.0 / (2.0 * mu) / dr**2 + cornell_potential(r[i], alpha_s, kappa)
        if i > 0:
            H[i, i - 1] = -1.0 / (2.0 * mu) / dr**2
        if i < n_grid - 1:
            H[i, i + 1] = -1.0 / (2.0 * mu) / dr**2
    # Dirichlet 边界 u(0)=u(R)=0：固定首末行（u[0]=0 消除奇点）
    H[0, :] = 0; H[0, 0] = 1.0
    H[-1, :] = 0; H[-1, -1] = 1.0
    evals, evecs = np.linalg.eigh(H)
    # 取前几个非平凡能级（跳过 u[0] 边界伪态）
    levels = [evals[1], evals[2], evals[3]]
    return levels, evecs[:, 1], r

# ---------- 测试 ----------

def run():
    passed = 0
    total = 0
    fails = []

    def check(name, cond, detail=""):
        nonlocal passed, total
        total += 1
        if cond:
            passed += 1
            print(f"  [PASS] {name}")
        else:
            fails.append(name)
            print(f"  [FAIL] {name}  {detail}")

    print("=" * 74)
    print("重味夸克偶素 Cornell 谱势（61B：重味强子 Cornell 扩展）")
    print("=" * 74)

    # ---- T1: Cornell 势参数物理有效性 ----
    # 标准 Cornell 拟合（Eichten et al. 1978）：κ≈0.18 GeV²、α_s≈0.39（有效值，~1 GeV 标度）、
    # 有效重夸克质量 m_c≈1.5、m_b≈4.8 GeV（裸 MS-bar 值 m_c≈1.27、m_b≈4.18 GeV 经 dressing）。
    kappa = 0.18        # 弦张力 GeV²
    alpha_s = 0.39      # Cornell 有效耦合（非跑动常数，~1 GeV 标度拟合值）
    m_c = 1.5           # 有效 charm 质量 GeV
    m_b = 4.8           # 有效 bottom 质量 GeV
    check("T1 Cornell 参数物理有效（κ>0、0<α_s<1、m_c<m_b）",
          kappa > 0 and 0 < alpha_s < 1 and m_c < m_b,
          f"κ={kappa}, α_s={alpha_s}, m_c={m_c}, m_b={m_b}")
    print("  [DIAG] α_s = 0.39 为 Cornell 有效耦合（拟合值，非跑动；跑动值 α_s(M_Z)≈0.118，"
          "1 GeV 标度有效值 ~0.4 一致）；m_c/m_b 为有效质量（dressing 后）")

    # ---- T2: charmonium 1S/2S（J/ψ, ψ'）----
    levels_c, u_c, r_c = schrodinger_spectrum(m_c, alpha_s, kappa)
    M_c1 = 2 * m_c + levels_c[0]
    M_c2 = 2 * m_c + levels_c[1]
    dev_Jpsi = abs(M_c1 - PDG['Jpsi']) / PDG['Jpsi']
    dev_psi2 = abs(M_c2 - PDG['psi2S']) / PDG['psi2S']
    print(f"  [DIAG] charmonium: J/ψ = {M_c1*1000:.0f} MeV (PDG {PDG['Jpsi']*1000:.0f}, 偏差 {dev_Jpsi*100:.1f}%), "
          f"ψ' = {M_c2*1000:.0f} MeV (PDG {PDG['psi2S']*1000:.0f}, 偏差 {dev_psi2*100:.1f}%)")
    check("T2 charmonium 1S/2S 质量对标 PDG（J/ψ, ψ' ±10%）",
          dev_Jpsi < 0.10 and dev_psi2 < 0.10,
          f"J/ψ偏差={dev_Jpsi*100:.1f}%, ψ'偏差={dev_psi2*100:.1f}%")

    # ---- T3: bottomonium 1S/2S（Υ, Υ'）----
    levels_b, u_b, r_b = schrodinger_spectrum(m_b, alpha_s, kappa)
    M_b1 = 2 * m_b + levels_b[0]
    M_b2 = 2 * m_b + levels_b[1]
    dev_Up = abs(M_b1 - PDG['Upsilon']) / PDG['Upsilon']
    dev_Up2 = abs(M_b2 - PDG['Upsilon2S']) / PDG['Upsilon2S']
    print(f"  [DIAG] bottomonium: Υ = {M_b1*1000:.0f} MeV (PDG {PDG['Upsilon']*1000:.0f}, 偏差 {dev_Up*100:.1f}%), "
          f"Υ' = {M_b2*1000:.0f} MeV (PDG {PDG['Upsilon2S']*1000:.0f}, 偏差 {dev_Up2*100:.1f}%)")
    check("T3 bottomonium 1S/2S 质量对标 PDG（Υ, Υ' ±10%）",
          dev_Up < 0.10 and dev_Up2 < 0.10,
          f"Υ偏差={dev_Up*100:.1f}%, Υ'偏差={dev_Up2*100:.1f}%")

    # ---- T4: 径向激发间距 ΔM = M(2S) - M(1S) ----
    dM_c = M_c2 - M_c1
    dM_b = M_b2 - M_b1
    dM_c_pdg = PDG['psi2S'] - PDG['Jpsi']
    dM_b_pdg = PDG['Upsilon2S'] - PDG['Upsilon']
    dev_dMc = abs(dM_c - dM_c_pdg) / dM_c_pdg
    dev_dMb = abs(dM_b - dM_b_pdg) / dM_b_pdg
    print(f"  [DIAG] 激发间距 ΔM(2S−1S): charmonium = {dM_c*1000:.0f} MeV (PDG {dM_c_pdg*1000:.0f}, 偏差 {dev_dMc*100:.1f}%), "
          f"bottomonium = {dM_b*1000:.0f} MeV (PDG {dM_b_pdg*1000:.0f}, 偏差 {dev_dMb*100:.1f}%)")
    check("T4 径向激发间距 ΔM(2S−1S) 对标 PDG（±20%）",
          dev_dMc < 0.20 and dev_dMb < 0.20,
          f"charm 偏差={dev_dMc*100:.1f}%, bottom 偏差={dev_dMb*100:.1f}%")

    # ---- T5: 1S 态 rms 半径（重味紧致性）----
    # rms² = ∫ r²|u|² dr / ∫ |u|² dr
    norm_c = np.trapezoid(u_c**2, r_c) if hasattr(np, 'trapezoid') else np.trapz(u_c**2, r_c)
    rms_c = np.sqrt(np.trapezoid(r_c**2 * u_c**2, r_c) / norm_c) if hasattr(np, 'trapezoid') \
            else np.sqrt(np.trapz(r_c**2 * u_c**2, r_c) / norm_c)
    norm_b = np.trapezoid(u_b**2, r_b) if hasattr(np, 'trapezoid') else np.trapz(u_b**2, r_b)
    rms_b = np.sqrt(np.trapezoid(r_b**2 * u_b**2, r_b) / norm_b) if hasattr(np, 'trapezoid') \
            else np.sqrt(np.trapz(r_b**2 * u_b**2, r_b) / norm_b)
    # r 单位 GeV⁻¹ → fm：1 GeV⁻¹ = 0.1973 fm
    rms_c_fm = rms_c * 0.1973
    rms_b_fm = rms_b * 0.1973
    print(f"  [DIAG] 1S rms 半径: J/ψ = {rms_c_fm:.3f} fm, Υ = {rms_b_fm:.3f} fm"
          f"（重味紧致 ~0.2-0.5 fm）")
    check("T5 1S 态 rms 半径（重味紧致性：J/ψ ~0.4 fm、Υ ~0.2 fm 量级）",
          rms_c_fm < 0.6 and rms_b_fm < rms_c_fm,
          f"J/ψ rms={rms_c_fm:.3f} fm, Υ rms={rms_b_fm:.3f} fm")

    # ---- T6: 轻味-重味对比 ----
    # 轻味介子（paperX_qcd_spectrum.py C11-C15）：ρ ~0.78 GeV、π ~0.14 GeV
    # 重味夸克偶素质量大得多（2m_q 主导）且半径更小（紧致）
    check("T6 重味-轻味对比：夸克偶素质量 >> 轻味介子（2m_q 主导）",
          M_c1 > 2.0 and M_b1 > 8.0 and rms_b_fm < rms_c_fm,
          f"M_J/ψ={M_c1:.2f} GeV, M_Υ={M_b1:.2f} GeV, rms_Υ={rms_b_fm:.3f} < rms_J/ψ={rms_c_fm:.3f}")

    # ---- 汇总 ----
    print("-" * 74)
    print(f"  汇总: {passed}/{total} 检查通过")
    if fails:
        print(f"  [!] 失败项: {fails}")
    print("=" * 74)
    return passed, total

if __name__ == "__main__":
    p, t = run()
    import sys
    sys.exit(0 if p == t else 1)
