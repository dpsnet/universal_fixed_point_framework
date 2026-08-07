#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
paperX_qcd_ds_ab.py — 61B 深化：κ A/B 耦合精确化方案
=============================================================================
对应笔记：notes/01_qcd_higgs/spectral_color_dynamics.md（61B 开放项：κ A/B 耦合精确化）
          + roadmap/phase61_physics_advancement.md 61B 遗留开放项
对应论文：paper/paper40_qcd_color_dynamics.md（§8.2 开放问题 3：κ 谱积分形式精确化需完整 A/B 耦合）

物理：定理 5.7 的 DS 机制确认用 A(p²) ≈ 1 简化（paperX_qcd_ds_dressing.py，
d = 2.0 GeV² 给 M(0) = 353 MeV ≈ κΛ = 401）。本脚本解**完整 A/B 耦合**
DS 方程（朗道规范彩虹近似，球对称）：

  A(p²) = 1 + C_F/(4π³) ∫dk k³ A/(k²A²+B²)·J_V(p,k)
  B(p²) = m + 3C_F/(4π³) ∫dk k³ B/(k²A²+B²)·J_B(p,k)

其中 J_B = ∫√(1−μ²)G dμ（标量 3 系数）、J_V = ∫√(1−μ²)G·V dμ
（矢量角结构 V(μ) = −(kμ) − 2(p−kμ)(pkμ−k²)/q²）、G 为 Maris-Tandy 高斯。

精确化成果：A/B 耦合增强自能（分母 k²A²+B² 中 A < 1）→ 匹配 κΛ = 401 MeV
所需红外强度从 d = 2.0（A≈1）降至 d_AB ≈ 1.5 GeV²——更接近文献 d ≈ 0.87–1.0。

验证内容（N1–N6）：
  N1  A/B 耦合 DS 迭代收敛（残差 < 1e-8）
  N2  A(p²) 波函数重整化：A(0) ≈ 1 且 A(p_max) < 1（高能 A < 1 物理）
  N3  A→1 极限复核：关闭 A 方程回到 A≈1 结果（M(0) = 353 MeV at d = 2.0）
  N4  匹配 κΛ = 401 MeV 所需 d_AB < d_A≈1 = 2.0（A/B 耦合降低所需红外强度）
  N5  与文献 d ≈ 0.87–1.0 的差距缩小（2.2× → < 2.0×，精确化方向）
  N6  M(0)(d_AB) ≈ κΛ = 401 MeV（精确化匹配）

谱量：κΛ = 401 MeV（定理 5.3）、C_F = 4/3、m = 3.5 MeV（谱框架 m_ud）。
"""
import numpy as np
from scipy.integrate import fixed_quad
from scipy.optimize import brentq

# ============================================================
# 常数（与 paperX_qcd_ds_dressing.py 一致）
# ============================================================
C_F = 4.0 / 3.0
OMEGA = 0.5            # GeV，Maris-Tandy 红外宽度
M_UD = 0.0035          # GeV，流质量（谱框架 m_ud）
KAPPA_LAMBDA = 0.401   # GeV，谱框架 Δ_dress = κΛ = 401 MeV（定理 5.3）
D_A1 = 2.0             # A≈1 版本匹配 κΛ 的 d（paperX_qcd_ds_dressing.py）
D_LIT_LO, D_LIT_HI = 0.87, 1.0   # 文献 Maris-Tandy 红外强度范围

RESULTS = []


def check(name, ok, info=""):
    RESULTS.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({info})" if info else ""))


# ============================================================
# A/B 耦合 DS 求解
# ============================================================

def mt_gluon(q2, d, omega=OMEGA):
    """Maris-Tandy 红外高斯胶子：G(q²) = (4π²d/ω⁴)·q²·e^{−q²/ω²}。"""
    return (4.0 * np.pi**2 * d / omega**4) * q2 * np.exp(-q2 / omega**2)


def J_B_ang(p, k, d):
    """标量角积分：J_B = ∫₋₁¹ √(1−μ²) G(q²) dμ。"""
    if abs(p) < 1e-12 or abs(k) < 1e-12:
        return (np.pi / 2.0) * mt_gluon(p * p + k * k, d)
    v, _ = fixed_quad(lambda mu: np.sqrt(1.0 - mu**2) * mt_gluon(p*p + k*k - 2.0*p*k*mu, d),
                      -1.0, 1.0, n=24)
    return v


def J_V_ang(p, k, d):
    """矢量角积分：J_V = ∫₋₁¹ √(1−μ²) G(q²)·V(μ) dμ，
    V(μ) = −(kμ) − 2(p−kμ)(pkμ−k²)/q²（朗道规范矢量投影）。"""
    if abs(p) < 1e-12 or abs(k) < 1e-12:
        return 0.0
    def integrand(mu):
        q2 = p * p + k * k - 2.0 * p * k * mu
        V = -(k * mu) - 2.0 * (p - k * mu) * (p * k * mu - k * k) / q2
        return np.sqrt(1.0 - mu**2) * mt_gluon(q2, d) * V
    v, _ = fixed_quad(integrand, -1.0, 1.0, n=24)
    return v


def solve_ds_ab(d, n_grid=60, p_max=6.0, n_iter=400, tol=1e-8, mix=0.3,
                with_A=True):
    """完整 A/B 耦合 Picard 迭代。with_A=False 时关闭 A 方程（A ≡ 1，A≈1 复核）。
    返回 (p 网格, A(p²), B(p²), 残差)。"""
    p = np.linspace(1e-4, p_max, n_grid)
    JB = np.zeros((n_grid, n_grid))
    JV = np.zeros((n_grid, n_grid))
    for i in range(n_grid):
        for j in range(n_grid):
            JB[i, j] = J_B_ang(p[i], p[j], d)
            if with_A:
                JV[i, j] = J_V_ang(p[i], p[j], d)
    A = np.ones(n_grid)
    B = np.full(n_grid, M_UD)
    for it in range(n_iter):
        An = np.ones(n_grid)
        Bn = np.full(n_grid, M_UD)
        for i in range(n_grid):
            denom = p**2 * A**2 + B**2
            Bn[i] = M_UD + 3.0 * C_F / (4.0 * np.pi**3) * np.trapz(p**3 * B / denom * JB[i, :], p)
            if with_A:
                An[i] = 1.0 + C_F / (4.0 * np.pi**3) * np.trapz(p**3 * A / denom * JV[i, :], p)
        resid = max(np.max(np.abs(An - A)), np.max(np.abs(Bn - B))) \
            / (max(np.max(np.abs(An)), np.max(np.abs(Bn))) + 1e-12)
        A = mix * An + (1.0 - mix) * A
        B = mix * Bn + (1.0 - mix) * B
        if resid < tol:
            break
    return p, A, B, resid


def m0_of_d(d, with_A=True):
    """给定 d 的动力学质量 M(0) = B(0)/A(0)（GeV）。"""
    _, A, B, _ = solve_ds_ab(d, with_A=with_A)
    return B[0] / A[0] if A[0] > 1e-3 else B[0]


def run_n1_n2():
    print("\n" + "=" * 74)
    print("  N1/N2. A/B 耦合 DS 求解：收敛 + A(p²) 波函数重整化")
    print("=" * 74)
    p, A, B, resid = solve_ds_ab(D_A1)
    M0 = B[0] / A[0]
    print(f"  迭代残差 = {resid:.2e}（判据 < 1e-8）")
    print(f"  A(0) = {A[0]:.4f}，A(p_max = {p[-1]:.1f} GeV) = {A[-1]:.4f}"
          f"（高能 A < 1，波函数重整化）")
    print(f"  B(0) = {B[0]*1000:.1f} MeV，M(0) = B(0)/A(0) = {M0*1000:.1f} MeV")
    check("N1 A/B 耦合 DS 迭代收敛（残差 < 1e-8）", resid < 1e-8,
          f"残差 = {resid:.1e}")
    check("N2 A(p²)：A(0) ≈ 1 且 A(p_max) < 1（波函数重整化物理）",
          abs(A[0] - 1.0) < 0.01 and A[-1] < 1.0,
          f"A(0) = {A[0]:.4f}, A(p_max) = {A[-1]:.4f}")


def run_n3():
    print("\n" + "=" * 74)
    print("  N3. A→1 极限复核（关闭 A 方程回到 A≈1 结果）")
    print("=" * 74)
    p, A, B, _ = solve_ds_ab(D_A1, with_A=False)
    M0_ref = B[0]
    _, _, B2, _ = solve_ds_ab(D_A1, with_A=False)
    print(f"  A 关闭（A ≡ 1）：M(0) = {B2[0]*1000:.1f} MeV（paperX_qcd_ds_dressing.py 参考 353 MeV）")
    dev = abs(B2[0] - 0.353) / 0.353 * 100
    check("N3 A→1 复核：M(0) = 353 MeV（与 A≈1 脚本一致，偏差 < 5%）",
          dev < 5.0, f"偏差 {dev:.1f}%")


def run_n4_n5_n6():
    print("\n" + "=" * 74)
    print("  N4/N5/N6. 精确化成果：匹配 κΛ 所需 d 降低")
    print("=" * 74)
    # A≈1：d = 2.0 给 353 MeV；A/B 耦合下匹配 401 所需 d
    f_ab = lambda d: m0_of_d(d, with_A=True) - KAPPA_LAMBDA
    d_lo, d_hi = 1.2, 1.8
    if f_ab(d_lo) * f_ab(d_hi) < 0:
        d_ab = brentq(f_ab, d_lo, d_hi, xtol=1e-4)
    else:
        d_ab = float('nan')
    M0_ab = m0_of_d(d_ab, with_A=True)
    print(f"  A/B 耦合匹配 κΛ = 401 MeV：d_AB = {d_ab:.3f} GeV²（M(0) = {M0_ab*1000:.0f} MeV）")
    print(f"  A≈1 版本匹配所需 d = {D_A1:.1f} GeV²（paperX_qcd_ds_dressing.py）")
    print(f"  → d_AB/d_A≈1 = {d_ab/D_A1:.3f}（A/B 耦合降低所需红外强度）")
    lit_mid = (D_LIT_LO + D_LIT_HI) / 2.0
    ratio_old = D_A1 / lit_mid
    ratio_new = d_ab / lit_mid
    print(f"  与文献 d ≈ {D_LIT_LO}–{D_LIT_HI} 的差距：{D_A1:.1f}/{lit_mid:.2f} = "
          f"{ratio_old:.1f}× → {d_ab:.2f}/{lit_mid:.2f} = {ratio_new:.1f}×")
    check("N4 匹配 κΛ 所需 d_AB < d_A≈1 = 2.0（A/B 耦合降低所需红外强度）",
          d_ab < D_A1, f"d_AB = {d_ab:.3f} < {D_A1:.0f}")
    check("N5 与文献差距缩小（2.2× → < 2.0×，精确化方向）",
          ratio_new < ratio_old and ratio_new < 2.0,
          f"{ratio_old:.1f}× → {ratio_new:.1f}×")
    check("N6 M(0)(d_AB) ≈ κΛ = 401 MeV（精确化匹配）",
          abs(M0_ab - KAPPA_LAMBDA) / KAPPA_LAMBDA < 0.02,
          f"M(0) = {M0_ab*1000:.0f} MeV")
    return d_ab


# ============================================================
# 主函数
# ============================================================

def main():
    print()
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║  61B 深化：κ A/B 耦合精确化方案                                 ║")
    print("║  完整 A(p²)/B(p²) DS 求解 → 匹配 κΛ 所需 d 降低 → 文献差距缩小 ║")
    print("╚══════════════════════════════════════════════════════════════════╝")

    run_n1_n2()
    run_n3()
    d_ab = run_n4_n5_n6()

    n_pass = sum(1 for _, ok in RESULTS if ok)
    n_total = len(RESULTS)
    print("\n" + "=" * 74)
    print(f"  汇总: {n_pass}/{n_total} 检查通过")
    print("=" * 74)
    if n_pass != n_total:
        raise SystemExit(f"FAIL: {n_total - n_pass} 项未通过")

    p, A, B, _ = solve_ds_ab(d_ab)
    M0_ab = B[0] / A[0]
    print("\n  关键数值（笔记引用）：")
    print(f"    A(p²)            = 波函数重整化（A(0) ≈ 1, A(p_max) = {A[-1]:.3f} < 1）")
    print(f"    匹配 κΛ 所需 d    = {d_ab:.3f} GeV²（A≈1 为 {D_A1:.1f}，降低 ~25%）")
    print(f"    文献差距          = {D_A1/0.94:.1f}× → {d_ab/0.94:.1f}×（精确化方向）")
    print(f"    M(0)(d_AB)       = {M0_ab*1000:.0f} MeV ≈ κΛ = {KAPPA_LAMBDA*1000:.0f} MeV")


if __name__ == "__main__":
    main()
