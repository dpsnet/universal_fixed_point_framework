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
关键测试：使用复 Frobenius 指数 ν₀ 修复乘积形式连分数。

Leaver (1985) 的正确 Frobenius 指数（径向方程，视界处）：
    ν₀ = -s - i(ω·r₊ - a·m)/(r₊ - r₋)
    
之前代码中使用的是简化版 ν₀ = -s（纯实数），缺少了关键的 ω 依赖虚部。
"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dynamic_spectrum"))

from leaver_unified_solver import LeaverResidual


def kerr_params(a=0.0, M=1.0):
    """Kerr 视界参数。"""
    root = np.sqrt(max(0.0, M**2 - a**2))
    r_p = M + root
    r_m = M - root
    kappa = (r_p - r_m) / (2.0 * (r_p**2 + a**2))
    return r_p, r_m, kappa


def nu0_correct(s, omega, a=0.0, m=0.0, M=1.0):
    """
    正确的 Frobenius 指数（含 ω 依赖的虚部）。
    
    ν₀ = -s - i(ω·r₊ - a·m)/(r₊ - r₋)
    """
    r_p, r_m, _ = kerr_params(a, M)
    return -s - 1j * (omega * r_p - a * m) / (r_p - r_m)


def alpha_complex(s, n, omega, a=0.0, m=0.0, M=1.0):
    """用复 ν₀ 修正的 αₙ。"""
    nu0 = nu0_correct(s, omega, a, m, M)
    return (n + 1) * (n + 2 * nu0 + 1)


def beta_complex(s, n, omega, lam, a=0.0, m=0.0, M=1.0):
    """用复 ν₀ 修正的 βₙ。"""
    nu0 = nu0_correct(s, omega, a, m, M)
    
    term1 = -lam - n * (n + 2 * nu0 + 1) + omega**2
    
    denom = n + nu0
    if abs(denom) > 1e-15:
        term2 = a * m * (m + 2 * nu0) / denom
    else:
        term2 = 0.0j
    
    term3 = 2.0 * a * omega * m
    
    denom2 = 2.0 * n + 2.0 * nu0 + 1.0
    if abs(denom2) > 1e-15:
        term4 = -2.0 * a * m * omega * (n + nu0) / denom2
    else:
        term4 = 0.0j
    
    return term1 + term2 + term3 + term4


def gamma_complex(s, n, omega, a=0.0, m=0.0, M=1.0):
    """用复 ν₀ 修正的 γₙ。"""
    _, _, kappa = kerr_params(a, M)
    nu0 = nu0_correct(s, omega, a, m, M)
    return -2.0j * omega * kappa * (n + nu0)


def cf_complex_nu0(s, omega, lam, a=0.0, m=0.0, M=1.0, N_max=200):
    """
    用复 ν₀ 评估径向连分数。
    
    仍然是反向递推：r_n = γ_{n+1}/(β_{n+1} - α_{n+1}·r_{n+1})
    """
    # 检查 α₀ 是否为零
    a_0 = alpha_complex(s, 0, omega, a, m, M)
    alpha0_zero = abs(a_0) < 1e-30
    
    n_start = 1 if alpha0_zero else 0
    
    # 反向递推
    r = 0.0j
    for n in range(N_max, n_start, -1):
        a_n = alpha_complex(s, n, omega, a, m, M)
        b_n = beta_complex(s, n, omega, lam, a, m, M)
        g_n = gamma_complex(s, n, omega, a, m, M)
        
        if abs(a_n) < 1e-30:
            continue
        
        denom = b_n - a_n * r
        if abs(denom) < 1e-30:
            denom = 1e-30j
        r = g_n / denom
    
    # R_{n_start}
    a_s = alpha_complex(s, n_start, omega, a, m, M)
    b_s = beta_complex(s, n_start, omega, lam, a, m, M)
    return b_s - a_s * r


def test_cases():
    print("=" * 70)
    print("复 Frobenius 指数 ν₀ 的关键测试")
    print("=" * 70)
    
    cases = [
        # (s, l, m, a, ω_ref, λ, name)
        (-2, 2, 0, 0.0, 0.373672 - 0.088962j, 4.0, "引力 s=-2"),
        (-0.5, 0.5, 0.5, 0.0, 0.378721 - 0.096458j, 1.0, "Dirac s=-0.5"),
    ]
    
    for s, l, m, a, omega_ref, lam, name in cases:
        # 计算正确的复 ν₀
        nu0 = nu0_correct(s, omega_ref, a, m)
        nu0_simple = -s  # 之前使用的简化版
        
        print(f"\n[{name}]")
        print(f"  ω_ref = {omega_ref:.10f}")
        print(f"  λ = {lam}")
        print(f"  ν₀(简单) = {nu0_simple:.6f}")
        print(f"  ν₀(正确) = {complex(nu0):.10f}")
        
        # 检查 γ 系数在关键 n 处的值（之前有 γ₂=0 的问题）
        print(f"  γ₁(正确) = {gamma_complex(s, 1, omega_ref, a, m):.6e}")
        print(f"  γ₂(正确) = {gamma_complex(s, 2, omega_ref, a, m):.6e}")
        print(f"  γ₂(简单)  | < 1e-30? {abs(-2j*omega_ref*0.25*(2-s)) < 1e-30}")
        
        # 用复 ν₀ 评估 CF
        r_correct = cf_complex_nu0(s, omega_ref, lam, a, m, N_max=300)
        print(f"  |R₀(ω_ref)|(复 ν₀, N=300) = {abs(r_correct):.6e}")
        
        # 增大截断验证
        r_correct_500 = cf_complex_nu0(s, omega_ref, lam, a, m, N_max=500)
        print(f"  |R₀(ω_ref)|(复 ν₀, N=500) = {abs(r_correct_500):.6e}")
        
        # 多项式形式对比（对 s=-2）
        if abs(s - (-2)) < 1e-10:
            solver = LeaverResidual(M=1.0, a=a, s=int(s), max_iter=300)
            r_poly = solver.radial_cf_polynomial(omega_ref, lam, int(m))
            print(f"  |R₀(ω_ref)|(多项式) = {abs(r_poly):.6e}  ← 基准")
        
        # 简单 ν₀ 对比
        from _dirac_leaver_solver import radial_continued_fraction as simple_cf
        r_simple = simple_cf(s, omega_ref, lam, a, m, N_max=300)
        print(f"  |R₀(ω_ref)|(简单 ν₀) = {abs(r_simple):.6e}")
        
        # 复 ν₀ 修正后是否更接近零？
        if abs(r_correct) < abs(r_simple):
            improvement = abs(r_simple) / max(abs(r_correct), 1e-30)
            print(f"  → 改善因子: {improvement:.1f}x")
        else:
            print(f"  → 未改善（残差反而增大）")

    # 对 Dirac 做 λ 和 ω 的 2D 扫描
    print("\n" + "=" * 70)
    print("Dirac case: 复 ν₀ CF 的 λ-ω 二维扫描")
    print("=" * 70)
    
    s, m, a = -0.5, 0.5, 0.0
    lam_ref = 1.0
    
    print("\n  |R₀| 在 (ω, λ) 平面（复 ν₀）：")
    lam_range = np.linspace(0.5, 1.5, 11)
    omega_range = [0.35 - 0.10j, 0.38 - 0.10j, 0.38 - 0.096j, 0.3787 - 0.0965j,
                   0.40 - 0.08j, 0.35 - 0.12j, 0.42 - 0.10j]
    
    print(f"  {'λ':>8} | ", end="")
    for lam_try in lam_range:
        print(f" {lam_try:6.3f}", end="")
    print()
    print(f"  {'ω':>24} |" + "─" * 77)
    
    for omega_try in omega_range:
        print(f"  {complex(omega_try):>22.6f} |", end="")
        for lam_try in lam_range:
            r = cf_complex_nu0(s, omega_try, lam_try, a, m, N_max=300)
            log_r = np.log10(max(abs(r), 1e-20))
            print(f" {log_r:6.1f}", end="")
        print()


if __name__ == "__main__":
    test_cases()
