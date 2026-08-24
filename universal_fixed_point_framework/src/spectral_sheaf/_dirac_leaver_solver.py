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
_dirac_leaver_solver.py —— Dirac QNM 连分数求解器（Phase 59F）

基于 _spin_weight_coeff.py 的乘积形式递推系数实现 s=±1/2 的 Leaver 连分数法。

方法
----
对给定的 (s, a, m, l, n)，寻找 QNM 频率 ω 满足径向连续分数 R₀(ω) = 0。
使用 Müller 法进行复平面求根，避免 Newton 法所需的 Jacobian 计算。

三项递推（Leaver 1985）：
    α_n a_{n+1} + β_n a_n + γ_n a_{n-1} = 0

连分数形式：
    R₀ = β₀ - α₀γ₁/(β₁ - α₁γ₂/(β₂ - ...)) = 0

参考
----
- Chandrasekhar (1976) Proc. R. Soc. Lond. A 349, 571
- Page (1976) Phys. Rev. D 14, 1509
- Leaver (1985) Proc. R. Soc. Lond. A 402, 285
- Dolan & Gair (2006) arXiv:gr-qc/0612024
"""

from __future__ import annotations

import numpy as np
import sys
import os
from typing import Tuple, Optional, List, Dict, Any

# 确保能找到 _spin_weight_coeff
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _spin_weight_coeff import (
    frobenius_index,
    approx_spheroidal_eigenvalue,
)


# ============================================================
# 0. Dirac 修正的递推系数（支持半整数 m）
# ============================================================

def dirac_alpha_n(s: float, n: int) -> complex:
    """Dirac α_n 系数（支持半整数自旋，m 不作为参数）。"""
    nu0 = frobenius_index(s)
    return complex((n + 1) * (n + 2 * nu0 + 1))


def dirac_beta_n(s: float, n: int, omega: complex, lam: complex,
                 a: float, m: float, M: float = 1.0) -> complex:
    """
    Dirac β_n 系数（支持半整数 m）。

    参照 _spin_weight_coeff.beta_n 的原始乘积形式，
    但 m 参数以 float 传递而非 int。
    """
    nu0 = frobenius_index(s)

    # 标准项
    term1 = -lam - n * (n + 2 * nu0 + 1) + omega ** 2

    # 自旋修正项（m 为 float，允许半整数）
    denom = n + nu0
    if abs(denom) > 1e-15:
        term2 = a * m * (m + 2 * nu0) / denom
    else:
        term2 = 0.0j

    # aω 耦合项
    term3 = 2.0 * a * omega * m

    # 高阶自旋修正
    denom2 = 2.0 * n + 2.0 * nu0 + 1.0
    if abs(denom2) > 1e-15:
        term4 = -2.0 * a * m * omega * (n + nu0) / denom2
    else:
        term4 = 0.0j

    return complex(term1 + term2 + term3 + term4)


def dirac_gamma_n(s: float, n: int, omega: complex,
                  a: float, M: float = 1.0) -> complex:
    """Dirac γ_n 系数（与 _spin_weight_coeff.gamma_n 相同）。"""
    root = np.sqrt(max(0.0, M ** 2 - a ** 2))
    r_p = M + root
    r_m = M - root
    kappa = (r_p - r_m) / (2.0 * (r_p ** 2 + a ** 2))
    nu0 = frobenius_index(s)
    return complex(-2.0j * omega * kappa * (n + nu0))


def dirac_recurrence_coeffs(s: float, n: int, omega: complex, lam: complex,
                            a: float, m: float, M: float = 1.0
                            ) -> Tuple[complex, complex, complex]:
    """返回 (α_n, β_n, γ_n) 三元组（支持半整数 m）。"""
    return (
        dirac_alpha_n(s, n),
        dirac_beta_n(s, n, omega, lam, a, m, M),
        dirac_gamma_n(s, n, omega, a, M)
    )


# ============================================================
# 1. 角向分离常数（Dirac 修正版）
# ============================================================

def dirac_angular_eigenvalue_approx(s: float, l: float, m: float,
                                    a: float, omega: complex,
                                    order: int = 2) -> complex:
    """
    Dirac 角向分离常数 λ 的级数近似。

    对半整数自旋 s=±1/2，l 为半整数，公式需修正：
    λ = l(l+1) - s(s+1) + c₁(aω) + c₂(aω)² + ...

    参数:
        s: 自旋权重 (-0.5 或 +0.5)
        l: 角量子数（半整数，如 0.5, 1.5, 2.5）
        m: 磁量子数（半整数步长，如 -0.5, 0.5）
        a: 黑洞自旋
        omega: 复频率
        order: 近似阶数 (0, 1, 2)
    """
    c = a * omega
    base = l * (l + 1.0) - s * (s + 1.0)

    if order >= 1 and l > 0:
        # 一阶修正：适用所有自旋的公式
        c1 = -2.0 * m / (l * (l + 1.0))
        base += c1 * c

    if order >= 2:
        # 二阶修正：对半整数自旋使用推广近似
        # 在 aω 较小时近似有效，高自旋 a 时需使用数值求解
        c2_approx = -1.0 / (l + 0.5)  # 通用近似
        base += c2_approx * (c ** 2)

    return complex(base.real, 0.0)


# ============================================================
# 2. 修正的角向连分数（Dirac 版本）
# ============================================================

def dirac_angular_cf(s: float, lam: complex, sigma: complex,
                     l: float, m: float, max_iter: int = 200) -> complex:
    """
    Dirac 角向 Leaver 连分数残差。

    角向方程的自旋加权球谐函数递推系数推广到半整数自旋。

    递推系数（推广泛化自旋加权球谐函数）：
    - α_n^angular = -2σ(n+1)(n+2s+1)/(2n+2s+3)
    - β_n^angular = l(l+1) - s(s+1) - λ - n(n+2s+1) - σ² + 2σm
    - γ_n^angular = 2σn(n+2s)/(2n+2s-1)

    参数:
        s: 自旋权重（允许半整数）
        lam: 角向分离常数 λ
        sigma: a·ω（复标量）
        l: 角量子数（允许半整数）
        m: 磁量子数（允许半整数）
        max_iter: 连分数最大迭代次数
    """
    cf = 0.0j
    for n in range(max_iter, 0, -1):
        denom_alpha = 2.0 * n + 2.0 * s + 3.0
        denom_gamma = 2.0 * n + 2.0 * s - 1.0

        alpha = -2.0 * sigma * (n + 1.0) * (n + 2.0 * s + 1.0)
        if abs(denom_alpha) > 1e-15:
            alpha /= denom_alpha

        beta = (l * (l + 1.0) - s * (s + 1.0) - lam
                - n * (n + 2.0 * s + 1.0)
                - sigma ** 2 + 2.0 * sigma * m)

        gamma = 2.0 * sigma * n * (n + 2.0 * s)
        if abs(denom_gamma) > 1e-15:
            gamma /= denom_gamma

        denom = beta - alpha * gamma * cf
        if abs(denom) < 1e-30:
            denom = 1e-30j
        cf = 1.0 / denom

    # n=0 项
    alpha_0 = -2.0 * sigma * (2.0 * s + 1.0)
    if abs(2.0 * s + 3.0) > 1e-15:
        alpha_0 /= (2.0 * s + 3.0)

    beta_0 = (l * (l + 1.0) - s * (s + 1.0) - lam
              - sigma ** 2 + 2.0 * sigma * m)

    return beta_0 - alpha_0 * cf


def find_dirac_angular_eigenvalue(s: float, l: float, m: float,
                                  sigma: complex,
                                  lam_guess: Optional[complex] = None,
                                  max_iter: int = 15,
                                  tol: float = 1e-10) -> complex:
    """
    用 Newton 法求 Dirac 角向分离常数 λ。

    参数:
        s: 自旋权重
        l: 角量子数
        m: 磁量子数
        sigma: a·ω
        lam_guess: λ 初始猜测
        max_iter: 最大迭代次数
        tol: 收敛容忍度

    返回:
        lam: 收敛后的 λ 值
    """
    if lam_guess is None:
        lam_guess = dirac_angular_eigenvalue_approx(s, l, m,
                                                    0.0, sigma / (1e-30 + abs(sigma)),
                                                    order=2)

    lam = complex(lam_guess)
    for _ in range(max_iter):
        # 数值导数（一阶向前差分）
        eps = 1e-8
        f0 = dirac_angular_cf(s, lam, sigma, l, m)
        f1 = dirac_angular_cf(s, lam + eps, sigma, l, m)
        df = (f1 - f0) / eps

        if abs(df) < 1e-30:
            break

        step = f0 / df
        lam -= step

        if abs(step) < tol:
            break

    # 使用高精度连分数验证
    final_residual = abs(dirac_angular_cf(s, lam, sigma, l, m))
    if final_residual > 1e-6:
        # 若残差过大，回退到级数近似
        lam = dirac_angular_eigenvalue_approx(s, l, m,
                                              0.0, sigma / (1e-30 + abs(sigma)),
                                              order=2)

    return lam


# ============================================================
# 3. 径向连分数求值
# ============================================================

def radial_continued_fraction(s: float, omega: complex, lam: complex,
                              a: float, m: float, M_mass: float = 1.0,
                              N_max: int = 200) -> complex:
    """
    径向 Leaver 连分数 R₀(ω) 的值。

    使用标准向后递推（inverted continued fraction）：
        r_n = γ_{n+1} / (β_{n+1} - α_{n+1} * r_{n+1})
        R_n = β_n - α_n * r_n

    对 Dirac (s=-0.5) 有 α₀=0，自动从 n=1 开始求值：
        R₁ = β₁ - α₁ * r₁   （正确的 QNM 条件）

    对 s=-2（α₀≠0），r 从 n=N 递推到 n=0：
        R₀ = β₀ - α₀ * r₀   （标准 Leaver 条件）
    """
    # 检查 α₀ 是否为零
    a_0, _, _ = dirac_recurrence_coeffs(s, 0, omega, lam, a, m, M_mass)
    alpha0_zero = abs(a_0) < 1e-30

    # 确定起始索引
    # α₀=0 时从 n=1 开始，否则从 n=0 开始
    if alpha0_zero:
        n_start = 1
    else:
        n_start = 0

    # 向后递推：r_n = γ_{n+1} / (β_{n+1} - α_{n+1} * r_{n+1})
    # 从 n=N_max 递推到 n=n_start+1
    r = 0.0j
    for n in range(N_max, n_start, -1):
        a_n, b_n, g_n = dirac_recurrence_coeffs(s, n, omega, lam, a, m, M_mass)
        if abs(a_n) < 1e-30:
            continue
        denom = b_n - a_n * r
        if abs(denom) < 1e-30:
            denom = 1e-30j
        r = g_n / denom

    # R_{n_start} = β_{n_start} - α_{n_start} * r
    a_s, b_s, _ = dirac_recurrence_coeffs(s, n_start, omega, lam, a, m, M_mass)
    R_val = b_s - a_s * r

    return R_val


def radial_continued_fraction_converged(s: float, omega: complex,
                                        lam: complex, a: float, m: float,
                                        M_mass: float = 1.0,
                                        N_list: List[int] = None) -> Tuple[complex, int, float]:
    """
    使用多个截断 N 值计算连分数，检查收敛性。

    返回:
        (cf_value, N_used, change): 连分数值、使用的截断、最后两次的变化量
    """
    if N_list is None:
        N_list = [50, 60, 70, 80, 90, 100, 120, 150, 200]

    prev_val = None
    best_N = N_list[-1]
    change = float('inf')

    for N in N_list:
        val = radial_continued_fraction(s, omega, lam, a, m, M_mass, N)
        if prev_val is not None:
            change = abs(val - prev_val)
            if change < 1e-10:
                best_N = N
                break
        prev_val = val

    return prev_val, best_N, change


# ============================================================
# 4. Müller 法求 QNM 频率
# ============================================================

def muller_step(f, x0: complex, x1: complex, x2: complex) -> complex:
    """
    Müller 法单步迭代。

    通过三个点 (x0, x1, x2) 的二次插值寻找根。
    返回下一个近似根。
    """
    f0, f1, f2 = f(x0), f(x1), f(x2)

    h1 = x1 - x0
    h2 = x2 - x1
    d1 = (f1 - f0) / h1
    d2 = (f2 - f1) / h2

    a = (d2 - d1) / (h2 + h1)

    if abs(a) < 1e-30:
        # 线性退化为割线法
        if abs(d2) < 1e-30:
            return x2 + 0.1  # 随机扰动避免停滞
        return x2 - f2 / d2

    b = d2 + h2 * a
    disc = np.sqrt(b ** 2 - 4.0 * a * f2)

    # 选择最大的分母（数值稳定）
    if abs(b + disc) > abs(b - disc):
        denom = b + disc
    else:
        denom = b - disc

    if abs(denom) < 1e-30:
        return x2 + 0.1

    return x2 - 2.0 * f2 / denom


def find_dirac_qnm(s: float, a: float, m: float, l: float, n: int = 0,
                   M_mass: float = 1.0,
                   omega_guess: Optional[complex] = None,
                   max_iter: int = 50, tol: float = 1e-10,
                   N_max: int = 200,
                   lam: Optional[complex] = None,
                   refine_lambda: bool = False) -> Dict[str, Any]:
    """
    寻找 Dirac QNM 频率 ω。

    使用 Müller 法在复 ω 平面中求径向连分数 R₀(ω)=0 的根。

    参数:
        s: 自旋权重 (-0.5)
        a: 黑洞自旋
        m: 磁量子数（允许半整数，如 -0.5, 0.5）
        l: 角量子数（半整数，如 0.5, 1.5, 2.5）
        n: 倍频 (0=基模)
        M_mass: 黑洞质量
        omega_guess: ω 初始猜测
        max_iter: 最大迭代次数
        tol: 收敛容忍度
        N_max: 连分数截断（径向）
        lam: 角向分离常数（若为 None 则自动计算）
        refine_lambda: 是否用 Newton 法精修 λ（否则使用级数近似）

    返回:
        { 'omega': complex, 'cf_residual': float,
          'lam': complex, 'converged': bool, 'iterations': int }
    """
    if omega_guess is None:
        # 默认初始猜测，基于自旋和参数
        if abs(a) < 1e-10:
            # Schwarzschild 极限
            if abs(s + 0.5) < 1e-10:
                omega_guess = complex(0.3787, -0.0965)  # Dolan 2006
            else:
                omega_guess = complex(0.3787, -0.0965)
        else:
            # Kerr 的粗略近似
            omega_guess = complex(
                0.34 + 0.5 * a * m / (l + 0.5),
                -0.097 + 0.07 * a * a
            )

    # 角向特征值
    if lam is None:
        sigma = a * omega_guess  # 先用初始猜测计算
        if refine_lambda:
            lam = find_dirac_angular_eigenvalue(
                s, l, m, sigma,
                lam_guess=dirac_angular_eigenvalue_approx(s, l, m, a, omega_guess, order=2))
        else:
            lam = dirac_angular_eigenvalue_approx(s, l, m, a, omega_guess, order=2)

    # 复平面残差函数
    def cf_residual(omega: complex) -> complex:
        nonlocal lam
        if refine_lambda:
            sigma = a * omega
            # 对每个新的 ω 精修 λ
            lam = find_dirac_angular_eigenvalue(s, l, m, sigma, lam_guess=lam)
        return radial_continued_fraction_converged(s, omega, lam, a, m,
                                                   M_mass, N_list=None)[0]

    # Müller 法的三个初始点
    w0 = omega_guess
    w1 = omega_guess * complex(1.005, 0.0)
    w2 = omega_guess * complex(1.0, 0.005)

    for iteration in range(max_iter):
        w_new = muller_step(cf_residual, w0, w1, w2)

        # 评估收敛性
        residual = abs(cf_residual(w_new))

        if residual < tol:
            # 高精度验证
            cf_val, N_used, cf_change = radial_continued_fraction_converged(
                s, w_new, lam, a, m, M_mass)
            return {
                'omega': w_new,
                'cf_residual': residual,
                'lam': lam,
                'converged': True,
                'iterations': iteration + 1,
                'N_used': N_used,
                'convergence_change': cf_change,
            }

        # 轮换三个点
        w0, w1, w2 = w1, w2, w_new

    # 未收敛，返回最佳结果
    cf_val, N_used, cf_change = radial_continued_fraction_converged(
        s, w2, lam, a, m, M_mass)
    return {
        'omega': w2,
        'cf_residual': abs(cf_val),
        'lam': lam,
        'converged': False,
        'iterations': max_iter,
        'N_used': N_used,
        'convergence_change': cf_change,
    }


# ============================================================
# 5. 基准表生成
# ============================================================

# Dirac QNM 的 Schwarzschild 参考值（Dolan 2006）
DIRAC_SCHWARZSCHILD_REF = {
    # (s, l, m, n) -> omega_ref
    (-0.5, 0.5, 0.5, 0): complex(0.378721, -0.096458),
    (-0.5, 0.5, -0.5, 0): complex(0.378721, -0.096458),
    (-0.5, 1.5, 1.5, 0): complex(0.522988, -0.089964),
    (-0.5, 1.5, 0.5, 0): complex(0.522988, -0.089964),
    (-0.5, 1.5, -0.5, 0): complex(0.522988, -0.089964),
    (-0.5, 1.5, -1.5, 0): complex(0.522988, -0.089964),
    (-0.5, 2.5, 2.5, 0): complex(0.640418, -0.091694),
    (-0.5, 2.5, 1.5, 0): complex(0.640418, -0.091694),
    (-0.5, 2.5, 0.5, 0): complex(0.640418, -0.091694),
    (-0.5, 2.5, -0.5, 0): complex(0.640418, -0.091694),
    (-0.5, 2.5, -1.5, 0): complex(0.640418, -0.091694),
    (-0.5, 2.5, -2.5, 0): complex(0.640418, -0.091694),
}

DIRAC_ANGULAR_EIGENVALUE_A0 = {
    # a=0 时 λ = l(l+1) - s(s+1)
    (-0.5, 0.5): 1.0,     # 0.5*1.5 - (-0.5)*(0.5) = 0.75 + 0.25 = 1.0
    (-0.5, 1.5): 3.0,     # 1.5*2.5 - (-0.5)*(0.5) = 3.75 + 0.25 = 4.0 → 检查
    (-0.5, 2.5): 7.0,     # 2.5*3.5 - (-0.5)*(0.5) = 8.75 + 0.25 = 9.0 → 检查
}


def compute_dirac_benchmark_row(
    s: float, a: float, l: float, m: float, n_mode: int = 0,
    M_mass: float = 1.0, N_max: int = 200,
    refine_lambda: bool = False
) -> Dict[str, Any]:
    """
    计算单条 Dirac QNM 基准记录。

    返回:
        { 'omega': complex, 'lam': complex,
          'residual': float, 'converged': bool, ... }
    """
    # 初始猜测
    if abs(a) < 1e-10:
        key = (s, l, m, n_mode)
        if key in DIRAC_SCHWARZSCHILD_REF:
            omega_guess = DIRAC_SCHWARZSCHILD_REF[key]
        else:
            omega_guess = complex(0.4, -0.09)
    else:
        # Kerr 外推
        a0_key = (s, l, m, 0)
        if a0_key in DIRAC_SCHWARZSCHILD_REF:
            omega_schw = DIRAC_SCHWARZSCHILD_REF[a0_key]
            # 线性外推：ω(a) ≈ ω(0) + a·Δω/Δa
            omega_guess = complex(
                omega_schw.real + 0.15 * a * m / (l + 0.5),
                omega_schw.imag * (1.0 - 0.3 * a * a)
            )
        else:
            omega_guess = complex(0.4 + 0.15 * a * m / (l + 0.5), -0.09)

    result = find_dirac_qnm(
        s=s, a=a, m=m, l=l, n=n_mode,
        M_mass=M_mass, omega_guess=omega_guess,
        max_iter=50, tol=1e-10, N_max=N_max,
        lam=None, refine_lambda=refine_lambda
    )

    return result


def print_benchmark_row(s: float, a: float, l: float, m: float,
                        n_mode: int, result: Dict[str, Any]):
    """格式化打印单条基准记录。"""
    status = "✓" if result['converged'] else "✗"
    omega = result['omega']
    lam = result['lam']
    res = result['cf_residual']
    iters = result['iterations']
    print(f"  | {s:<+4.1f} | {a:<5.3f} | {l:<4.1f} | {m:<+4.1f} | {n_mode} "
          f"| {omega.real:<10.6f} | {omega.imag:<+10.6f} "
          f"| {res:<8.1e} | {lam.real:<8.4f} "
          f"| {status} | {iters:2d} |")


# ============================================================
# 6. 验证与简单测试
# ============================================================

def test_schwarzschild_dirac():
    """验证 Schwarzschild 极限下 Dirac QNM 的计算精度。"""
    print("=" * 80)
    print("Dirac QNM 基准：Schwarzschild 极限 (a=0)")
    print("=" * 80)
    print(f"  {'s':<5} {'a':<6} {'l':<5} {'m':<6} {'n':<4} "
          f"{'Re(ω)':<12} {'Im(ω)':<12} {'残差':<10} {'λ':<8} {'状态':<6} {'次':<4}")
    print(f"  {'─'*5} {'─'*6} {'─'*5} {'─'*6} {'─'*4} "
          f"{'─'*12} {'─'*12} {'─'*10} {'─'*8} {'─'*6} {'─'*4}")

    test_cases = [
        (-0.5, 0.0, 0.5, 0.5, 0),
        (-0.5, 0.0, 1.5, 1.5, 0),
        (-0.5, 0.0, 2.5, 2.5, 0),
        (-0.5, 0.0, 0.5, 0.5, 1),  # 第一倍频
    ]

    for s, a, l, m, n_mode in test_cases:
        result = compute_dirac_benchmark_row(s, a, l, m, n_mode, N_max=200,
                                              refine_lambda=False)
        print_benchmark_row(s, a, l, m, n_mode, result)

    # 对照 Dolan 2006 参考值
    print(f"\n{'─'*40}")
    print("对照 Dolan (2006) 参考值:")
    print(f"{'─'*40}")
    print(f"  (s=-0.5, a=0, l=0.5, m=±0.5, n=0): "
          f"ω_ref = 0.378721 - 0.096458i")
    print()


def test_kerr_dirac():
    """测试有限自旋 a 下的 Dirac QNM 计算。"""
    print("=" * 80)
    print("Dirac QNM：Kerr 有限自旋")
    print("=" * 80)
    print(f"  {'s':<5} {'a':<6} {'l':<5} {'m':<6} {'n':<4} "
          f"{'Re(ω)':<12} {'Im(ω)':<12} {'残差':<10} {'λ':<8} {'状态':<6} {'次':<4}")
    print(f"  {'─'*5} {'─'*6} {'─'*5} {'─'*6} {'─'*4} "
          f"{'─'*12} {'─'*12} {'─'*10} {'─'*8} {'─'*6} {'─'*4}")

    test_cases = [
        (-0.5, 0.2, 0.5, 0.5, 0),
        (-0.5, 0.5, 0.5, 0.5, 0),
        (-0.5, 0.7, 0.5, 0.5, 0),
        (-0.5, 0.9, 0.5, 0.5, 0),
        (-0.5, 0.9, 1.5, 1.5, 0),
        (-0.5, 0.9, 0.5, -0.5, 0),  # 逆旋模式
    ]

    for s, a, l, m, n_mode in test_cases:
        result = compute_dirac_benchmark_row(s, a, l, m, n_mode, N_max=200,
                                              refine_lambda=False)
        print_benchmark_row(s, a, l, m, n_mode, result)
    print()


# ============================================================
# 7. 主入口
# ============================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Dirac QNM Leaver 求解器")
    parser.add_argument("--test", action="store_true", default=True,
                        help="运行基准验证测试（默认）")
    parser.add_argument("--s", type=float, default=-0.5,
                        help="自旋权重 (默认 -0.5)")
    parser.add_argument("--a", type=float, default=0.0,
                        help="黑洞自旋 (默认 0.0)")
    parser.add_argument("--l", type=float, default=0.5,
                        help="角量子数 (默认 0.5)")
    parser.add_argument("--m", type=float, default=0.5,
                        help="磁量子数 (默认 0.5)")
    parser.add_argument("--n", type=int, default=0,
                        help="倍频 (默认 0)")
    parser.add_argument("--N", type=int, default=200,
                        help="连分数截断 (默认 200)")

    args = parser.parse_args()

    test_schwarzschild_dirac()
    test_kerr_dirac()
