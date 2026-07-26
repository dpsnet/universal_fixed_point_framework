#!/usr/bin/env python3
"""
_fit_Dcoeffs.py —— 从三项递推数值拟合 D₀-D₄ 系数

思路：
1. 对 s=-2（已知正确），用多项式形式计算 αₙ, βₙ, γₙ 作为"精确参考"
2. 对 s=-0.5，用乘积形式（复 ν₀）× 修正因子拟合 D₀-D₄
3. 从拟合的 D₀-D₄ 反推理论公式中的错误项

多项式形式关系:
    αₙ = n² + (D₀+1)n + D₀
    βₙ = -2n² + (D₁+2)n + D₃
    γₙ = n² + (D₂-3)n + D₄ - D₂ + 2

反推:
    D₀ = α₀
    D₃ = β₀
    D₄ = γ₁
    D₁ = β₁ - β₀
    D₂ = γ₁ - γ₀ + 2
"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dynamic_spectrum"))

from leaver_unified_solver import LeaverResidual


def kerr_params(a=0.0, M=1.0):
    root = np.sqrt(max(0.0, M**2 - a**2))
    r_p = M + root
    r_m = M - root
    kappa = (r_p - r_m) / (2.0 * (r_p**2 + a**2))
    return r_p, r_m, kappa


def nu0_correct(s, omega, a=0.0, m=0.0, M=1.0):
    r_p, r_m, _ = kerr_params(a, M)
    return -s - 1j * (omega * r_p - a * m) / (r_p - r_m)


def alpha_product(s, n, omega, a=0.0, m=0.0, M=1.0):
    """乘积形式 αₙ（用复 ν₀）。"""
    nu0 = nu0_correct(s, omega, a, m, M)
    return (n + 1) * (n + 2 * nu0 + 1)


def beta_product(s, n, omega, lam, a=0.0, m=0.0, M=1.0):
    """乘积形式 βₙ（用复 ν₀）。"""
    nu0 = nu0_correct(s, omega, a, m, M)
    term1 = -lam - n * (n + 2 * nu0 + 1) + omega**2
    denom = n + nu0
    term2 = a * m * (m + 2 * nu0) / denom if abs(denom) > 1e-15 else 0.0j
    term3 = 2.0 * a * omega * m
    denom2 = 2.0 * n + 2.0 * nu0 + 1.0
    term4 = -2.0 * a * m * omega * (n + nu0) / denom2 if abs(denom2) > 1e-15 else 0.0j
    return term1 + term2 + term3 + term4


def gamma_product(s, n, omega, a=0.0, m=0.0, M=1.0):
    """乘积形式 γₙ（用复 ν₀）。"""
    _, _, kappa = kerr_params(a, M)
    nu0 = nu0_correct(s, omega, a, m, M)
    return -2.0j * omega * kappa * (n + nu0)


def D_from_coeffs(s, omega, lam, a=0.0, m=0.0, M=1.0, method='product'):
    """
    从递推系数反推 D₀-D₄。
    
    需要 α₀, α₁, β₀, β₁, γ₀, γ₁。
    """
    if method == 'product':
        a0 = alpha_product(s, 0, omega, a, m, M)
        a1 = alpha_product(s, 1, omega, a, m, M)
        b0 = beta_product(s, 0, omega, lam, a, m, M)
        b1 = beta_product(s, 1, omega, lam, a, m, M)
        g0 = gamma_product(s, 0, omega, a, m, M)
        g1 = gamma_product(s, 1, omega, a, m, M)
    else:
        raise ValueError(f"Unknown method: {method}")
    
    D = np.zeros(5, dtype=complex)
    D[0] = a0  # D₀ = α₀
    D[3] = b0  # D₃ = β₀
    D[4] = g1  # D₄ = γ₁
    D[1] = b1 - b0  # D₁ = β₁ - β₀
    D[2] = g1 - g0 + 2.0  # D₂ = γ₁ - γ₀ + 2
    
    return D


def polynomial_alpha(n, D):
    return n*n + (D[0]+1)*n + D[0]


def polynomial_beta(n, D):
    return -2*n*n + (D[1]+2)*n + D[3]


def polynomial_gamma(n, D):
    return n*n + (D[2]-3)*n + D[4] - D[2] + 2


def compare_coeffs(s, omega, lam, a=0.0, m=0.0, M=1.0, max_n=5):
    """比较乘积形式和多项式形式在各 n 处的系数。"""
    print(f"\n{'='*70}")
    print(f"系数对比: s={s}, ω={omega:.6f}, λ={lam:.4f}, a={a}")
    print(f"{'='*70}")
    
    # 用多项式形式（Cook-Zalutskiy）计算 D 系数
    solver_poly = LeaverResidual(M=M, a=a, s=int(s), max_iter=200)
    D_cook = solver_poly._D_coeffs(omega, lam, int(m))
    print(f"\nCook-Zalutskiy D₀-D₄: {D_cook}")
    
    # 用乘积形式（复 ν₀）反推 D
    D_fit = D_from_coeffs(s, omega, lam, a, m, M, method='product')
    print(f"乘积形式(复ν₀)反推 D₀-D₄: {D_fit}")
    
    print(f"\n{'n':>3} {'α_product':>18} {'α_polynomial':>18} {'β_product':>18} {'β_polynomial':>18} {'γ_product':>18} {'γ_polynomial':>18}")
    print('-' * 110)
    
    for n in range(max_n + 1):
        ap = alpha_product(s, n, omega, a, m, M)
        bp = beta_product(s, n, omega, lam, a, m, M)
        gp = gamma_product(s, n, omega, a, m, M)
        
        a_poly = polynomial_alpha(n, D_fit)
        b_poly = polynomial_beta(n, D_fit)
        g_poly = polynomial_gamma(n, D_fit)
        
        print(f"{n:3d} {ap:18.10f} {a_poly:18.10f} {bp:18.10f} {b_poly:18.10f} {gp:18.10f} {g_poly:18.10f}")
        
        # 验证多项式形式与乘积形式的一致性
        da = abs(ap - a_poly)
        db = abs(bp - b_poly)
        dg = abs(gp - g_poly)
        if da > 1e-10 or db > 1e-10 or dg > 1e-10:
            print(f"     Δα={da:.2e} Δβ={db:.2e} Δγ={dg:.2e}")
    
    # 检查多项式形式的连分数残差
    r_poly_fit = cf_from_D(omega, lam, m, D_fit)
    r_poly_cook = cf_from_D(omega, lam, m, D_cook)
    r_prod = cf_product(s, omega, lam, a, m, M)
    
    print(f"\n连分数残差:")
    print(f"  乘积形式(复ν₀):    |R₀| = {abs(r_prod):.6e}")
    print(f"  多项式(拟合 D):    |R₀| = {abs(r_poly_fit):.6e}")
    print(f"  多项式(Cook D):    |R₀| = {abs(r_poly_cook):.6e}")


def cf_from_D(omega, lam, m, D, max_iter=300, n_inv=0):
    """用 D 系数评估连分数。"""
    # 前向
    conv1 = 0.0j
    for i in range(0, n_inv):
        denom = polynomial_beta(i, D) - polynomial_gamma(i, D) * conv1
        if abs(denom) < 1e-30:
            denom = 1e-30j
        conv1 = polynomial_alpha(i, D) / denom
    # 后向
    conv2 = 0.0j
    for i in range(max_iter, n_inv, -1):
        denom = polynomial_beta(i, D) - polynomial_alpha(i, D) * conv2
        if abs(denom) < 1e-30:
            denom = 1e-30j
        conv2 = polynomial_gamma(i, D) / denom
    return polynomial_beta(n_inv, D) - polynomial_gamma(n_inv, D)*conv1 - polynomial_alpha(n_inv, D)*conv2


def cf_product(s, omega, lam, a=0.0, m=0.0, M=1.0, N_max=300):
    """乘积形式连分数（复 ν₀）。"""
    a_0 = alpha_product(s, 0, omega, a, m, M)
    n_start = 1 if abs(a_0) < 1e-30 else 0
    
    r = 0.0j
    for n in range(N_max, n_start, -1):
        a_n = alpha_product(s, n, omega, a, m, M)
        b_n = beta_product(s, n, omega, lam, a, m, M)
        g_n = gamma_product(s, n, omega, a, m, M)
        if abs(a_n) < 1e-30:
            continue
        denom = b_n - a_n * r
        if abs(denom) < 1e-30:
            denom = 1e-30j
        r = g_n / denom
    
    a_s = alpha_product(s, n_start, omega, a, m, M)
    b_s = beta_product(s, n_start, omega, lam, a, m, M)
    return b_s - a_s * r


def analyze_sigma_term():
    """
    分析 sigma_D 项中正确的 ω² 系数。
    
    通过比较 Cook 公式的 D 系数与"目标" D 系数（使 CF 残差为零），
    反推 sigma_D 中正确的 ω² 系数。
    """
    print("\n" + "=" * 70)
    print("sigma_D 项分析：寻找正确的 ω² 系数")
    print("=" * 70)
    
    cases = [
        (-2, 2, 0, 0.0, 0.373672 - 0.088962j, 4.0, "引力"),
        (-1, 1, 0, 0.0, 0.2483 - 0.0926j, 2.0, "电磁"),
    ]
    
    for s, l, m, a, omega_ref, lam, name in cases:
        print(f"\n[{name} s={s}]")
        solver = LeaverResidual(M=1.0, a=a, s=int(s), max_iter=200)
        
        # Cook 公式的 D 系数
        D_cook = solver._D_coeffs(omega_ref, lam, int(m))
        
        # 解析 D 系数中的各组成部分
        root = np.sqrt(max(0.0, 1.0 - a**2))
        r_p = 1.0 + root
        r_m = 1.0 - root
        sigma_p = (2.0 * omega_ref * r_p - a * m) / (2.0 * root)
        sigma_m = (2.0 * omega_ref * r_m - a * m) / (2.0 * root)
        zeta = 1.0j * omega_ref
        xi = -s - 1.0j * sigma_p
        eta = -1.0j * sigma_m
        p_val = root * zeta
        alpha = 1.0 + s + xi + eta - 2.0 * zeta + s
        gamma_coef = 1.0 + s + 2.0 * eta
        delta = 1.0 + s + 2.0 * xi
        
        # sigma_D 中除 ω² 项外的部分
        sigma_base = (lam + a**2 * omega_ref**2
                      + p_val * (2.0 * alpha + gamma_coef - delta)
                      + (1.0 + s - 0.5 * (gamma_coef + delta))
                      * (s + 0.5 * (gamma_coef + delta)))
        
        print(f"  sigma_base = {sigma_base:.10f}")
        print(f"  Cook D[3] = {D_cook[3]:.10f}")
        print(f"  Cook D[3] 表达式 = alpha·(4p - delta) - sigma_D")
        
        # 从 D[3] 反推 sigma_D 中使用的 ω² 项
        # D[3] = alpha·(4p - delta) - sigma_D
        # sigma_D = alpha·(4p - delta) - D[3]
        sigma_D_used = alpha * (4.0 * p_val - delta) - D_cook[3]
        print(f"  从 D[3] 反推 sigma_D = {sigma_D_used:.10f}")
        
        # 对比 sigma_base，找出 ω² 系数差
        # sigma_D = sigma_base + C·ω²
        C_omega2 = (sigma_D_used - sigma_base) / (omega_ref**2)
        print(f"  sigma_D 中的额外 ω² 系数: C = {C_omega2:.6f}")
        print(f"  4s = {4*s:.1f}, C ≈ 4s? {'✓' if abs(C_omega2 - 4*s) < 1e-6 else '✗'}")


if __name__ == "__main__":
    # 1. 分析 sigma_D 中的 ω² 系数
    analyze_sigma_term()
    
    # 2. 比较 s=-2 和 s=-0.5 的系数
    print("\n\n" + "=" * 70)
    print("系数逐项对比")
    print("=" * 70)
    
    # s=-2, a=0 参考
    compare_coeffs(-2, 0.373672 - 0.088962j, 4.0, a=0.0, m=0)
    
    # s=-0.5, a=0
    compare_coeffs(-0.5, 0.378721 - 0.096458j, 1.0, a=0.0, m=0.5)
    
    # s=-0.5, a=0 (m 符号变化)
    compare_coeffs(-0.5, 0.378721 - 0.096458j, 1.0, a=0.0, m=-0.5)
