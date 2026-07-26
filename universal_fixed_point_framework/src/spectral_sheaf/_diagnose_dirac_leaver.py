#!/usr/bin/env python3
"""
_diagnose_dirac_leaver.py —— Dirac Leaver 系数全面诊断脚本

系统检查每个实现环节，定位可能疏忽。
"""

import numpy as np
import sys
import os

# 确保能找到模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dynamic_spectrum"))

from _spin_weight_coeff import (
    frobenius_index, alpha_n, beta_n, gamma_n, recurrence_coeffs,
    approx_spheroidal_eigenvalue
)
from _dirac_leaver_solver import (
    dirac_alpha_n, dirac_beta_n, dirac_gamma_n, dirac_recurrence_coeffs,
    dirac_angular_eigenvalue_approx, dirac_angular_cf, find_dirac_angular_eigenvalue,
    radial_continued_fraction as dirac_radial_cf
)

# 导入 leaver_unified_solver 用于多项式形式对比
from leaver_unified_solver import LeaverResidual


def diagnose_angular_eigenvalue():
    """诊断 1：角向特征值 λ 的计算正确性。"""
    print("=" * 70)
    print("诊断 1：角向特征值 λ 的计算正确性")
    print("=" * 70)

    # Schwarzschild 极限 a=0 下，λ 应退化为 l(l+1) - s(s+1)
    test_cases = [
        # (s, l, m, a, omega, expected_λ)
        (-2, 2, 0, 0.0, 0.373672 - 0.088962j, 2.0 * 3 - (-2) * (-1)),  # = 6 - 2 = 4
        (-0.5, 0.5, 0.5, 0.0, 0.378721 - 0.096458j, 0.5 * 1.5 - (-0.5) * 0.5),  # = 0.75 + 0.25 = 1.0
        (-0.5, 0.5, -0.5, 0.0, 0.378721 - 0.096458j, 0.5 * 1.5 - (-0.5) * 0.5),  # = 1.0
        (-0.5, 1.5, 0.5, 0.0, 0.378721 - 0.096458j, 1.5 * 2.5 - (-0.5) * 0.5),  # = 3.75 + 0.25 = 4.0
    ]

    print(f"\n{'s':>6} {'l':>6} {'m':>6} {'a':>6} {'expected λ':>16} {'approx λ(0)':>16} {'approx λ(2)':>16} {'match':>8}")
    print("-" * 76)

    for s, l, m, a, omega, lam_expected in test_cases:
        if abs(s - (-2)) < 1e-10:
            lam_approx_0 = approx_spheroidal_eigenvalue(s, int(l), int(m), a, omega, order=0)
            lam_approx_2 = approx_spheroidal_eigenvalue(s, int(l), int(m), a, omega, order=2)
        else:
            lam_approx_0 = dirac_angular_eigenvalue_approx(s, l, m, a, omega, order=0)
            lam_approx_2 = dirac_angular_eigenvalue_approx(s, l, m, a, omega, order=2)

        match_0 = "✓" if abs(lam_approx_0 - lam_expected) < 1e-10 else "✗"
        match_2 = "✓" if abs(lam_approx_2 - lam_expected) < 1e-10 else "✗"

        print(f"{s:6.1f} {l:6.1f} {m:6.1f} {a:6.2f} {lam_expected:16.10f} "
              f"{complex(lam_approx_0):16.10f} {complex(lam_approx_2):16.10f} {match_2:>8}")

    # 检查角向连分数求值（在正确的 λ 处应接近零）
    print("\n\n角向连分数验证（在正确 λ 处应接近零）：")
    for s, l, m, a, omega, lam_expected in test_cases:
        if abs(s - (-2)) < 1e-10:
            continue  # 跳过整数自旋（使用不同的角向 CF）
        sigma = a * omega
        cf_res = dirac_angular_cf(s, lam_expected, sigma, l, m)
        print(f"  s={s:.1f} l={l:.1f} m={m:.1f} λ={lam_expected:.6f} → |angular_CF| = {abs(cf_res):.2e}")


def diagnose_product_form():
    """
    诊断 2：乘积形式系数（_spin_weight_coeff.py / _dirac_leaver_solver.py）。

    检查在已知参考频率处，各项递推系数是否符合预期。
    """
    print("\n" + "=" * 70)
    print("诊断 2：乘积形式系数检查")
    print("=" * 70)

    # Schwarzschild a=0 参考值
    ref_dirac = (0.378721, -0.096458)  # ω_real, ω_imag
    omega_d = complex(*ref_dirac)
    ref_grav = (0.373672, -0.088962)  # l=2, n=0
    omega_g = complex(*ref_grav)

    # 在 Schwarzschild 极限下检验系数渐近行为
    print("\n2a. Dirac (s=-0.5) 系数在 n 较大时的渐近行为：")
    s_d = -0.5
    lam_d = 1.0  # a=0, l=1/2, s=-1/2
    a = 0.0
    m_d = 0.5
    for n in [0, 1, 2, 5, 10, 50, 100]:
        a_n, b_n, g_n = dirac_recurrence_coeffs(s_d, n, omega_d, lam_d, a, m_d)
        print(f"    n={n:3d}: α_n={complex(a_n):12.6e}  β_n={complex(b_n):12.6e}  γ_n={complex(g_n):12.6e}")

    print("\n2b. Dirac (s=-0.5) α₀=0 检查：")
    a_0, _, _ = dirac_recurrence_coeffs(s_d, 0, omega_d, lam_d, a, m_d)
    print(f"    α₀ = {complex(a_0):.2e}  {'→ 为零 ✓' if abs(a_0) < 1e-15 else '→ 非零 ✗'}")

    print("\n2c. 引力 (s=-2) 系数在 n 较大时的渐近行为：")
    s_g = -2
    lam_g = 4.0  # a=0, l=2, s=-2
    m_g = 0
    for n in [0, 1, 2, 5, 10, 50, 100]:
        a_n, b_n, g_n = recurrence_coeffs(s_g, n, omega_g, lam_g, a, m_g)
        print(f"    n={n:3d}: α_n={complex(a_n):12.6e}  β_n={complex(b_n):12.6e}  γ_n={complex(g_n):12.6e}")

    # 检查狄拉克系数的大 n 渐近比率
    print("\n2d. 渐近比率检查（CF 收敛判定）：")
    n_large = 100
    a_n_d, b_n_d, g_n_d = dirac_recurrence_coeffs(s_d, n_large, omega_d, lam_d, a, m_d)
    a_n_g, b_n_g, g_n_g = recurrence_coeffs(s_g, n_large, omega_g, lam_g, a, m_g)

    if abs(a_n_d) > 1e-30:
        print(f"    Dirac   αₙ/γₙ (n={n_large}): {abs(a_n_d / g_n_d):.6f}  "
              f"(应 ≈ 1 以收敛)")
    if abs(a_n_g) > 1e-30:
        print(f"    引力    αₙ/γₙ (n={n_large}): {abs(a_n_g / g_n_g):.6f}  "
              f"(应 ≈ 1 以收敛)")


def diagnose_product_cf_at_reference():
    """
    诊断 3：乘积形式连分数在参考频率处的残差。

    这是核心测试——正确的实现应在参考频率处给出接近零的残差。
    """
    print("\n" + "=" * 70)
    print("诊断 3：乘积形式连分数在参考频率处的残差")
    print("=" * 70)

    ref_cases = [
        # (s, l, m, a, ω_ref, 名称)
        (-2, 2, 0, 0.0, 0.373672 - 0.088962j, "引力 l=2"),
        (-0.5, 0.5, 0.5, 0.0, 0.378721 - 0.096458j, "Dirac l=1/2 m=+1/2"),
        (-0.5, 0.5, -0.5, 0.0, 0.378721 - 0.096458j, "Dirac l=1/2 m=-1/2"),
    ]

    for s, l, m, a, omega_ref, name in ref_cases:
        # 计算角向特征值
        if abs(s - (-2)) < 1e-10:
            lam = approx_spheroidal_eigenvalue(s, int(l), int(m), a, omega_ref, order=2)
            lam = complex(lam)
        else:
            lam = dirac_angular_eigenvalue_approx(s, l, m, a, omega_ref, order=2)

        print(f"\n  [{name}]")
        print(f"    ω_ref = {omega_ref:.12f}")
        print(f"    λ     = {lam:.12f}")

        # 评估径向 CF
        r_val = dirac_radial_cf(s, omega_ref, lam, a, m, N_max=200)
        r_val_400 = dirac_radial_cf(s, omega_ref, lam, a, m, N_max=400)

        print(f"    |R₀(ω_ref)| (N=200) = {abs(r_val):.6e}")
        print(f"    |R₀(ω_ref)| (N=400) = {abs(r_val_400):.6e}")

        # 检查 λ 扫描（如果残差大，可能 λ 不对）
        if abs(r_val) > 1e-4:
            print(f"\n    → 残差较大！尝试扫描 λ 附近 10%")
            lam_scan = np.linspace(0.5 * abs(lam), 1.5 * abs(lam), 20)
            min_res = float('inf')
            best_lam = lam
            for l_try in lam_scan:
                r = abs(dirac_radial_cf(s, omega_ref, complex(l_try), a, m, N_max=200))
                if r < min_res:
                    min_res = r
                    best_lam = l_try
            if min_res < abs(r_val):
                print(f"    → 发现更好的 λ = {best_lam:.6f} 使 |R₀| = {min_res:.6e}")
            else:
                print(f"    → λ 扫描未改善，问题可能在系数定义")


def diagnose_polynomial_form():
    """
    诊断 4：多项式形式 Cook-Zalutskiy D 系数检查。

    注意：_D_coeffs 是为 s=-2 推导的，检查其对 s=-0.5 的适用性。
    """
    print("\n" + "=" * 70)
    print("诊断 4：多项式形式 (Cook-Zalutskiy) D 系数检查")
    print("=" * 70)

    ref_cases = [
        (-2, 2, 0, 0.0, 0.373672 - 0.088962j, "引力 s=-2 l=2"),
        (-0.5, 0.5, 0.5, 0.0, 0.378721 - 0.096458j, "Dirac s=-0.5 l=0.5"),
    ]

    for s, l, m, a, omega_ref, name in ref_cases:
        print(f"\n  [{name}]")

        solver = LeaverResidual(M=1.0, a=a, s=int(s), max_iter=200)

        # 计算角向特征值
        if abs(s - (-2)) < 1e-10:
            lam = complex(approx_spheroidal_eigenvalue(int(s), int(l), int(m), a, omega_ref, order=2))
        else:
            lam = dirac_angular_eigenvalue_approx(s, l, m, a, omega_ref, order=2)

        print(f"    ω_ref = {omega_ref:.12f}")
        print(f"    λ     = {lam:.12f}")

        # 尝试多项式形式——可能需要整数 m
        try:
            r_poly = solver.radial_cf_polynomial(omega_ref, lam, int(m))
            print(f"    |R₀_poly(ω_ref)| = {abs(r_poly):.6e}")
        except Exception as e:
            print(f"    polynomial CF error: {e}")

        # 检查 D 系数
        try:
            D = solver._D_coeffs(omega_ref, lam, int(m))
            print(f"    D₀-D₄ = {D}")
            # 检查 D 系数的渐近形式
            n_test = 50
            alpha_p = solver._polynomial_alpha(n_test, D)
            beta_p = solver._polynomial_beta(n_test, D)
            gamma_p = solver._polynomial_gamma(n_test, D)
            print(f"    α_{n_test} = {alpha_p:.6e}, β_{n_test} = {beta_p:.6e}, γ_{n_test} = {gamma_p:.6e}")
            # 大 n 下 αₙ → n², γₙ → n², βₙ → -2n²
            print(f"    αₙ/n² → {alpha_p/(n_test**2):.4f} (应 ≈ 1)")
            print(f"    γₙ/n² → {gamma_p/(n_test**2):.4f} (应 ≈ 1)")
        except Exception as e:
            print(f"    D coeffs error: {e}")


def diagnose_leaver_unified_extended():
    """
    诊断 5：将 leaver_unified_solver 扩展到 s=-0.5 是否正确。

    关键问题是 leaver_unified_solver 的 _D_coeffs 函数中的 "-8.0*omega**2" 项
    是 s=-2 的 Starobinsky 常数项，对 s=-0.5 不应使用。
    """
    print("\n" + "=" * 70)
    print("诊断 5：leaver_unified_solver 多项式形式对 s=-0.5 的适用性")
    print("=" * 70)

    print("""
    Cook-Zalutskiy (2014) 的多项式形式 D 系数推导基于 Teukolsky 方程，
    其 Starobinsky 常数项依赖于自旋权重 s：

    对 s=±2:   Starobinsky 常数 = (λ + 2)² + 4aω(aω - m)  
               → 在 D 系数公式中以 "-8ω²" 等形式出现
    对 s=±1:   Starobinsky 常数形式不同
    对 s=±1/2: 无非平凡 Starobinsky 常数（半整数自旋的 Teukolsky-Starobinsky
               恒等式退化为平凡的 Weyl 关系）

    因此：多项式形式 D 系数直接用于 s=-0.5 是**数学上不正确**的。
    "-8.0 * omega ** 2" 项在 _D_coeffs 中硬编码为 s=-2 专用。
    """)

    # 检查 s=-0.5 时 _D_coeffs 中的 "-8.0*omega**2"
    s_cases = [-2, -1, -0.5]
    m = 0
    lam = 4.0
    a = 0.0
    omega = 0.3 - 0.1j

    for s in s_cases:
        try:
            solver = LeaverResidual(M=1.0, a=a, s=int(s), max_iter=200)
            D = solver._D_coeffs(omega, lam, m)
            print(f"\n  s={s}: D₀-D₄ = {D}")
        except Exception as e:
            print(f"\n  s={s}: error - {e}")


def diagnose_beta_structure():
    """
    诊断 6：β_n 系数的结构差异——γ-spin 和 Dirac 的本质不同。

    Dirac 扰动在 Chandrasekhar 形式中满足一阶耦合方程组，
    化为二阶方程时，有效势形式与 Teukolsky 方程不同。
    """
    print("\n" + "=" * 70)
    print("诊断 6：Dirac 与引力 β_n 系数的结构差异分析")
    print("=" * 70)

    print("""
    Leaver 乘积形式系数的来源：

    Teukolsky 径向方程（引力 s=-2）：
    Δ² d/dr(1/Δ dR/dr) + ... = 0
    递推系数：
    α_n = (n+1)(n+2ν₀+1)  
    β_n = -λ - n(n+2ν₀+1) + ω² + a²ω² - 2aωm + ...
    γ_n = -2iωκ(n+ν₀)

    Dirac 在 Kerr 背景下的方程（Chandrasekhar 1976）：
    通过 Chandrasekhar 变换解耦为一对二阶方程，有效势为：
    V_Dirac = f(r)[κ²/r² ± κ df/dr / (2r)] 其中 κ = l + 1/2
    
    此势与 Teukolsky 势形式不同，Leaver CF 递推系数也应不同。
    但若通过 Teukolsky 方程框架处理 s=-0.5，则上述系数形式仍成立。

    关键检查点：
    1. β_n 中的 a²ω² - 2aωm 项：在 Teukolsky 框架中，角向 λ 已吸收此耦合，
       但不同实现对此处理方式不同。
    2. _spin_weight_coeff.py 的 beta_n 中只有 ω²，无 a²ω² 项。
       这意味着 λ 已被定义为包含了 a²ω² - 2aωm。
    """)

    # 检查 beta_n 中是否丢失了 a²ω² 项
    print("\nβ_n 中 a²ω² 项检查：")
    s = -2
    n = 0
    lam = 4.0
    a = 0.5
    m = 0
    omega = 0.38 - 0.09j

    # 有旋转的情况
    b_n_kerr = beta_n(s, n, omega, lam, a, m)
    b_n_schw = beta_n(s, n, omega, lam, 0.0, m)
    a_sq_omega_sq_term = a**2 * omega**2

    print(f"  s={s}, n={n}, a={a}:  β_n = {complex(b_n_kerr):.10f}")
    print(f"  s={s}, n={n}, a=0:  β_n = {complex(b_n_schw):.10f}")
    print(f"  a²ω² = {a_sq_omega_sq_term:.10f}")
    print(f"  β_n(a={a}) - β_n(a=0) = {complex(b_n_kerr - b_n_schw):.10f}")
    print(f"  期望差（若不含 a²ω² in λ）= {complex(-a_sq_omega_sq_term):.10f}")


def diagnose_cf_grid():
    """
    诊断 7：在复平面上绘制 R₀(ω) 的等高线图，直接观察零点位置。

    这可以排除 Muller 法的收敛问题，直观判断根的位置。
    """
    print("\n" + "=" * 70)
    print("诊断 7：复平面 CF 残差扫描（直接观察零点）")
    print("=" * 70)

    # 对 Dirac (a=0, l=0.5) 在参考值附近扫描
    s = -0.5
    l = 0.5
    m = 0.5
    a = 0.0
    lam = dirac_angular_eigenvalue_approx(s, l, m, a, 0.378721 - 0.096458j, order=2)

    print(f"\n  Dirac s={s}, l={l}, m={m}, a={a}")
    print(f"  角向 λ ≈ {lam:.10f}")
    print(f"  参考 ω_ref = 0.378721 - 0.096458i")
    print(f"\n  扫描网格：Re(ω) ∈ [0.0, 1.0], Im(ω) ∈ [-0.5, 0.0]")

    re_grid = np.linspace(0.0, 1.0, 21)
    im_grid = np.linspace(-0.5, 0.0, 21)

    print(f"\n  |R₀(ω)| 的 log10 值（行=Im, 列=Re）：")
    print(f"  {'Re(ω)→':>8}", end="")
    for re_w in re_grid[::4]:
        print(f" {re_w:6.2f}", end="")
    print()

    for im_w in im_grid[::5]:
        print(f"  Im={im_w:5.2f}  ", end="")
        for re_w in re_grid[::4]:
            omega = complex(re_w, im_w)
            r_val = dirac_radial_cf(s, omega, lam, a, m, N_max=100)
            log_r = np.log10(max(abs(r_val), 1e-20))
            print(f" {log_r:6.1f}", end="")
        print()

    # 在参考值附近精细扫描
    print(f"\n  精细扫描：围绕参考值附近")
    re_fine = np.linspace(0.25, 0.50, 11)
    im_fine = np.linspace(-0.20, -0.02, 10)

    min_res = float('inf')
    best_omega = 0j
    for re_w in re_fine:
        for im_w in im_fine:
            omega = complex(re_w, im_w)
            r_val = dirac_radial_cf(s, omega, lam, a, m, N_max=200)
            if abs(r_val) < min_res:
                min_res = abs(r_val)
                best_omega = omega

    print(f"    扫描中最小的 |R₀| = {min_res:.6e} 在 ω = {best_omega:.10f}")
    print(f"    参考 ω_ref = 0.378721 - 0.096458i")
    print(f"    差值 = {abs(best_omega - (0.378721 - 0.096458j)):.6e}")

    # 在参考点处的精确残差
    r_ref = dirac_radial_cf(s, 0.378721 - 0.096458j, lam, a, m, N_max=200)
    print(f"\n    在 ω_ref 处的 |R₀| = {abs(r_ref):.6e}")


if __name__ == "__main__":
    print("=" * 70)
    print("Dirac Leaver 系数全面诊断")
    print("=" * 70)

    diagnose_angular_eigenvalue()
    diagnose_product_form()
    diagnose_product_cf_at_reference()
    diagnose_polynomial_form()
    diagnose_leaver_unified_extended()
    diagnose_beta_structure()
    diagnose_cf_grid()

    print("\n" + "=" * 70)
    print("诊断完成")
    print("=" * 70)
