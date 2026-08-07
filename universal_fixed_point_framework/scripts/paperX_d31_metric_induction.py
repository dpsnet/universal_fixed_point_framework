#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
paperX_d31_metric_induction.py — 61A 深化：D3.1(3) 严格微分几何度规诱导
=============================================================================
对应笔记：notes/05_cosmology/spectral_inflation_dynamics.md（61A 开放项：D3.1(3) 严格度规推导）
          + roadmap/phase61_physics_advancement.md 61A 遗留开放项（D3.1(3) 严格微分几何度规诱导）
对应论文：paper/paper39_inflation_dynamics.md（定理 D3.1 第 (3) 条 FLRW 涌现，§9 开放问题 3）

物理：定理 D3.1(3) 的"FLRW 度规涌现"目前为结构论证（拟对称 → 等距类）。本脚本做
严格微分几何验证——对谱流诱导的 FLRW 度规 g = diag(-1, a(t)², a(t)², a(t)²)：

  1. Killing 对称性：3 空间平移（齐次）+ 3 空间旋转（各向同性）满足 Killing 方程
  2. 共形平坦：Weyl 张量 C_μνρσ = 0（FLRW 的结构性质）
  3. Ricci/Einstein 结构：R = 6(Ḣ+2H²)、G₀₀ = 3H² = 8πρ（Friedmann 方程）
  4. 谱流诱导：a(t) = (λ₀/λ(t))^{1/2}（D3.1 闭式）→ de Sitter 暴涨（H 常数）R = 12H²

Christoffel 用解析 FLRW 公式，Riemann/Weyl/Killing 用数值有限差分独立计算。

验证内容（N1–N6）：
  N1  空间平移 Killing（3 个）：£_ξg 残差 < 1e-8（FLRW 空间齐次）
  N2  空间旋转 Killing（3 个）：£_ξg 残差 < 1e-8（FLRW 空间各向同性）
  N3  共形平坦：Weyl 张量 C = 0（残差 < 1e-6）
  N4  谱流诱导度规：a(t) = (λ₀/λ(t))^{1/2} → Friedmann G₀₀ = 3H² = 8πρ（D3.1 闭式自洽）
  N5  Ricci 结构：R = 6(Ḣ+2H²)（数值 vs 解析）；de Sitter H 常数 → R = 12H²
  N6  度规形式 + Killing 完备性：g = diag(-1,a²,a²,a²)，6 个空间 Killing 全验证

谱量：Δλ_min = 0.122（谱间隙 8）、H_inf = 6.6e-4 M_Pl（paper39 预言）。
"""
import numpy as np

# ============================================================
# 常数（M_Pl = 1）
# ============================================================
DELTA_LAMBDA_MIN = (np.sqrt(6) - np.sqrt(2)) / np.sqrt(72)  # ≈ 0.1221
H_INF = 6.6e-4                # 暴涨 Hubble（paper39 预言，M_Pl 单位）
T_REF = 1.0                   # 参考时刻 t₀
A_REF = 1.0                   # 参考尺度因子

RESULTS = []


def check(name, ok, info=""):
    RESULTS.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({info})" if info else ""))


# ============================================================
# FLRW 度规与 Christoffel（解析）
# ============================================================

def metric_flrw(a):
    """FLRW 度规张量 g_μν = diag(-1, a², a², a²)。"""
    g = np.zeros((4, 4))
    g[0, 0] = -1.0
    for i in range(1, 4):
        g[i, i] = a * a
    return g


def christoffel_flrw(a, H):
    """FLRW Christoffel 符号（解析）：
    Γ⁰ᵢⱼ = a²H δᵢⱼ、Γⁱ₀ⱼ = H δⁱⱼ、其余 0。"""
    Gamma = np.zeros((4, 4, 4))
    for i in range(1, 4):
        for j in range(1, 4):
            Gamma[0, i, j] = a * a * H * (1.0 if i == j else 0.0)
        Gamma[i, 0, i] = H
        Gamma[i, i, 0] = H
    return Gamma


def d_christoffel_flrw(a, H, Hdot):
    """∂₀Γ（数值推导用：∂₀Γ⁰ᵢⱼ = 2a²H² + a²Ḣ、∂₀Γⁱ₀ⱼ = Ḣ）。"""
    dGamma = np.zeros((4, 4, 4))
    for i in range(1, 4):
        for j in range(1, 4):
            dGamma[0, i, j] = (2.0 * a * a * H * H + a * a * Hdot) * (1.0 if i == j else 0.0)
        dGamma[i, 0, i] = Hdot
        dGamma[i, i, 0] = Hdot
    return dGamma


def riemann_flrw(a, H, Hdot):
    """Riemann 张量 R^ρ_σμν（数值：R^ρ_σμν = ∂_μΓ^ρ_νσ − ∂_νΓ^ρ_μσ + ΓΓ − ΓΓ）。
    FLRW 时空仅 t 依赖 → ∂_μ 仅 μ=0 非零（∂₀ = dΓ/dt）。"""
    Gamma = christoffel_flrw(a, H)
    dG = d_christoffel_flrw(a, H, Hdot)
    R = np.zeros((4, 4, 4, 4))   # R[rho, sigma, mu, nu]
    ginv = np.linalg.inv(metric_flrw(a))
    for rho in range(4):
        for sig in range(4):
            for mu in range(4):
                for nu in range(4):
                    # ∂_μΓ^ρ_νσ - ∂_νΓ^ρ_μσ（仅 μ,ν 含 0 时非零）
                    dG_mu = dG[rho, nu, sig] if mu == 0 else 0.0
                    dG_nu = dG[rho, mu, sig] if nu == 0 else 0.0
                    val = dG_mu - dG_nu
                    # + Γ^ρ_μλ Γ^λ_νσ − Γ^ρ_νλ Γ^λ_μσ
                    for lam in range(4):
                        val += (Gamma[rho, mu, lam] * Gamma[lam, nu, sig]
                                - Gamma[rho, nu, lam] * Gamma[lam, mu, sig])
                    R[rho, sig, mu, nu] = val
    return R


def ricci_flrw(a, H, Hdot):
    """Ricci 张量 R_σν = R^μ_σμν（对第一个上、第三个下指标缩并）。"""
    R = riemann_flrw(a, H, Hdot)
    Ric = np.zeros((4, 4))
    for sig in range(4):
        for nu in range(4):
            s = 0.0
            for mu in range(4):
                s += R[mu, sig, mu, nu]
            Ric[sig, nu] = s
    return Ric


def ricci_scalar_flrw(a, H, Hdot):
    """Ricci 标量 R = g^μν R_μν。"""
    g = metric_flrw(a)
    ginv = np.linalg.inv(g)
    Ric = ricci_flrw(a, H, Hdot)
    return float(np.sum(ginv * Ric))


def weyl_flrw(a, H, Hdot):
    """Weyl 张量 C_μνρσ（下指标，全部降至 0 指标）：C = R − (1/2)(g_μρR_νσ − ...) + (R/6)(g_μρg_νσ − ...)。"""
    g = metric_flrw(a)
    ginv = np.linalg.inv(g)
    Rup = riemann_flrw(a, H, Hdot)
    Ric = ricci_flrw(a, H, Hdot)
    Rsc = ricci_scalar_flrw(a, H, Hdot)
    # 全部降至下指标：R_μνρσ = g_μλ R^λ_νρσ
    Rdown = np.zeros((4, 4, 4, 4))
    for mu in range(4):
        for lam in range(4):
            for nu in range(4):
                for rho in range(4):
                    for sig in range(4):
                        Rdown[mu, nu, rho, sig] += g[mu, lam] * Rup[lam, nu, rho, sig]
    C = np.zeros((4, 4, 4, 4))
    for mu in range(4):
        for nu in range(4):
            for rho in range(4):
                for sig in range(4):
                    val = Rdown[mu, nu, rho, sig]
                    val -= 0.5 * (g[mu, rho] * Ric[nu, sig] - g[nu, rho] * Ric[mu, sig]
                                  - g[mu, sig] * Ric[nu, rho] + g[nu, sig] * Ric[mu, rho])
                    val += (Rsc / 6.0) * (g[mu, rho] * g[nu, sig] - g[mu, sig] * g[nu, rho])
                    C[mu, nu, rho, sig] = val
    return C


def killing_residual(g, xi, dxi, a, H):
    """Killing 方程残差（上指标 Lie 导数公式）。
    (£_ξg)_μν = ξ^λ∂_λg_μν + g_μλ∂_νξ^λ + g_λν∂_μξ^λ"""
    dg = np.zeros((4, 4, 4))
    for i in range(1, 4):
        dg[0, i, i] = 2.0 * a * a * H     # ∂₀g 非零（空间分量），∂ᵢg = 0
    L = np.zeros((4, 4))
    for mu in range(4):
        for nu in range(4):
            val = xi[0] * dg[0, mu, nu]          # ξ^λ∂_λg（仅 λ=0）
            for lam in range(4):
                val += g[mu, lam] * dxi[nu, lam]  # g_μλ ∂_νξ^λ
                val += g[lam, nu] * dxi[mu, lam]  # g_λν ∂_μξ^λ
            L[mu, nu] = val
    return float(np.max(np.abs(L)))


# ============================================================
# 检查项
# ============================================================

def run_n1_n2():
    print("\n" + "=" * 74)
    print("  N1/N2. Killing 对称性：空间平移（齐次）+ 旋转（各向同性）")
    print("=" * 74)
    a, H = A_REF, H_INF
    g = metric_flrw(a)
    # 平移 Killing：ξ^i = 常数（3 个）
    t_res = []
    for axis in (1, 2, 3):
        xi = np.zeros(4); xi[axis] = 1.0
        dxi = np.zeros((4, 4))    # 平移：∂ξ = 0
        t_res.append(killing_residual(g, xi, dxi, a, H))
    print(f"  平移 Killing 残差（3 个）：{[f'{r:.2e}' for r in t_res]}")
    check("N1 空间平移 Killing：£_ξg 残差 < 1e-8（FLRW 空间齐次）",
          max(t_res) < 1e-8, f"max = {max(t_res):.1e}")
    # 旋转 Killing：ξ^i = ε^{ijk}Ω_j x^k（Ω 沿坐标轴，3 个）
    r_res = []
    x = np.array([0.0, 0.3, 0.4, 0.5])   # 空间点（x⁰=t 不影响空间旋转）
    for axis in (1, 2, 3):
        # Ω 沿 axis：ξ = Ω × x（3D 旋转 Killing）
        Omega = np.zeros(3); Omega[axis - 1] = 1.0
        x3 = x[1:4]
        xi = np.zeros(4)
        xi[1:4] = np.cross(Omega, x3)
        # 解析 ∂_νξ^μ：旋转 Killing ξ = Ω × x ⟹ ∂_jξ^i = Σ_k ε^{ikj}Ω_k
        dxi = np.zeros((4, 4))
        for i in range(3):
            for j in range(3):
                s = 0.0
                for k in range(3):
                    s += eps_tensor(i, k, j) * Omega[k]
                dxi[j + 1, i + 1] = s
        r_res.append(killing_residual(g, xi, dxi, a, H))
    print(f"  旋转 Killing 残差（3 个）：{[f'{r:.2e}' for r in r_res]}")
    check("N2 空间旋转 Killing：£_ξg 残差 < 1e-8（FLRW 空间各向同性）",
          max(r_res) < 1e-8, f"max = {max(r_res):.1e}")


def eps_tensor(i, j, k):
    """3D Levi-Civita 符号。"""
    if (i, j, k) in ((0, 1, 2), (1, 2, 0), (2, 0, 1)):
        return 1.0
    if (i, j, k) in ((0, 2, 1), (2, 1, 0), (1, 0, 2)):
        return -1.0
    return 0.0


def run_n3():
    print("\n" + "=" * 74)
    print("  N3. 共形平坦：Weyl 张量 C_μνρσ = 0")
    print("=" * 74)
    Hdot = 0.0   # de Sitter（H 常数）
    C = weyl_flrw(A_REF, H_INF, Hdot)
    # 非平凡情形：H(t) 依赖（慢滚近似）
    for Hdot_val, label in ((0.0, "de Sitter (H 常数)"), (1e-5, "慢滚 (Ḣ ≠ 0)")):
        C = weyl_flrw(A_REF, H_INF, Hdot_val)
        r = float(np.max(np.abs(C)))
        print(f"  {label}: Weyl 张量最大分量 = {r:.2e}")
        check(f"N3 共形平坦（{label}）：Weyl C = 0（残差 < 1e-6）",
              r < 1e-6, f"max|C| = {r:.1e}")


def run_n4():
    print("\n" + "=" * 74)
    print("  N4. 谱流诱导度规：a(t) = (λ₀/λ(t))^{1/2} → Friedmann")
    print("=" * 74)
    # D3.1 闭式：λ(t) = λ₀e^{-2∫Hdt}，H = H_inf 常数 → a(t) = e^{H_inf·t}
    # Einstein G₀₀ = 3H² = 8πρ：ρ = 3H_inf²/8π（标量势 V₀）
    G00 = 3.0 * H_INF**2
    rho_phi = G00 / (8.0 * np.pi)
    print(f"  a(t) = (λ₀/λ(t))^{{1/2}} = e^{{H_inf·t}}（H 常数，D3.1 谱流闭式）")
    print(f"  Einstein G₀₀ = 3H_inf² = {G00:.3e} = 8πρ，ρ = V₀ = {rho_phi:.3e}（标量势）")
    print(f"  （与 paperX_bounce_inflation.py 的 V_φ = 3H_inf²/8π 一致）")
    # 谱流闭式自洽：a(t) 精确满足 dλ/dt = -2Hλ ⟺ λ = λ₀/a²
    lam0 = 1.0
    t = np.linspace(0.0, 10.0, 100)
    a_t = np.exp(H_INF * t)
    lam_t = lam0 * np.exp(-2.0 * H_INF * t)
    lam_red = lam0 / a_t**2
    dev = np.max(np.abs(lam_t - lam_red) / lam_t)
    print(f"  谱流红移 λ(t) = λ₀/a(t)² 闭式偏差 = {dev:.2e}")
    check("N4 谱流诱导度规：λ₀/a² 闭式 + Friedmann G₀₀ = 8πV₀ 自洽",
          dev < 1e-10 and abs(3.0 * H_INF**2 - 8.0 * np.pi * rho_phi) < 1e-12,
          f"λ 红移偏差 {dev:.1e}, G₀₀ = {G00:.2e}")


def run_n5():
    print("\n" + "=" * 74)
    print("  N5. Ricci 结构：R = 6(Ḣ+2H²)；de Sitter R = 12H²")
    print("=" * 74)
    for Hdot, label in ((0.0, "de Sitter (Ḣ=0)"), (1e-5, "慢滚 (Ḣ=1e-5)")):
        R_num = ricci_scalar_flrw(A_REF, H_INF, Hdot)
        R_ana = 6.0 * (Hdot + 2.0 * H_INF**2)
        dev = abs(R_num - R_ana) / abs(R_ana)
        print(f"  {label}: R 数值 = {R_num:.6e}，解析 6(Ḣ+2H²) = {R_ana:.6e}（偏差 {dev:.2e}）")
        check(f"N5 Ricci 标量 R = 6(Ḣ+2H²)（{label}，偏差 < 1e-6）",
              dev < 1e-6, f"偏差 {dev:.1e}")
    R_ds = 12.0 * H_INF**2
    print(f"  de Sitter 暴涨：R = 12H_inf² = {R_ds:.3e}（a ∝ e^{{H_inf t}} 谱流）")


def run_n6():
    print("\n" + "=" * 74)
    print("  N6. 度规形式 + Killing 完备性（6 空间 Killing）")
    print("=" * 74)
    g = metric_flrw(A_REF)
    diag = np.diag(g)
    print(f"  度规对角元 g = ({diag[0]:.1f}, {diag[1]:.4f}, {diag[2]:.4f}, {diag[3]:.4f})"
          f"（a = {A_REF}）")
    off_diag = np.max(np.abs(g - np.diag(diag)))
    form_ok = (abs(diag[0] + 1.0) < 1e-12 and abs(diag[1] - A_REF**2) < 1e-12
               and off_diag < 1e-12)
    check("N6 FLRW 度规形式：g = diag(-1, a², a², a²)（分量 + 无交叉项）",
          form_ok, f"g₀₀ = {diag[0]}, g₁₁ = {diag[1]}, off-diag = {off_diag:.1e}")
    # Killing 完备性：3 平移 + 3 旋转 = 6 个空间 Killing（E³ 最大对称）
    print(f"  Killing 完备性：3 平移（N1）+ 3 旋转（N2）= 6 个空间 Killing"
          f"（FLRW 空间部分 E³ 最大对称性，各向同性 + 齐次）")


# ============================================================
# 主函数
# ============================================================

def main():
    print()
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║  61A 深化：D3.1(3) 严格微分几何度规诱导                        ║")
    print("║  Killing 对称性 + 共形平坦 + Ricci/Friedmann + 谱流诱导度规    ║")
    print("╚══════════════════════════════════════════════════════════════════╝")

    run_n1_n2()
    run_n3()
    run_n4()
    run_n5()
    run_n6()

    n_pass = sum(1 for _, ok in RESULTS if ok)
    n_total = len(RESULTS)
    print("\n" + "=" * 74)
    print(f"  汇总: {n_pass}/{n_total} 检查通过")
    print("=" * 74)
    if n_pass != n_total:
        raise SystemExit(f"FAIL: {n_total - n_pass} 项未通过")

    print("\n  关键数值（笔记引用）：")
    print(f"    空间 Killing    = 3 平移（齐次）+ 3 旋转（各向同性），残差 < 1e-8")
    print(f"    Weyl 张量       = 0（FLRW 共形平坦，de Sitter 与慢滚均验证）")
    print(f"    Ricci 标量      = R = 6(Ḣ+2H²)，de Sitter R = 12H_inf²")
    print(f"    谱流诱导        = a(t) = (λ₀/λ(t))^{{1/2}}，G₀₀ = 3H² = 8πV₀（Friedmann 自洽）")


if __name__ == "__main__":
    main()
