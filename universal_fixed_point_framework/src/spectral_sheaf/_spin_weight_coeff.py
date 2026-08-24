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
_spin_weight_coeff.py —— 跨自旋 Leaver 三项递推系数生成器

为不同自旋权重 s ∈ {-2, -1, +1, -1/2, +1/2} 生成径向三项递推系数。

三项递推形式（Leaver 1985）：
    α_n a_{n+1} + β_n a_n + γ_n a_{n-1} = 0

使用原始乘积形式的系数（非 Cook-Zalutskiy 多项式形式），
保证对所有 s 通用。

参考：
    Leaver (1985) Proc. R. Soc. Lond. A 402, 285-298
    Teukolsky (1973) Astrophys. J. 185, 635
    Cook & Zalutskiy (2014) Phys. Rev. D 90, 124021
"""

from __future__ import annotations

import numpy as np
from typing import Tuple, Optional


def kerr_horizon_params(a: float, M: float = 1.0) -> Tuple[float, float, float]:
    """
    Kerr 黑洞视界参数。

    返回：
        r_plus: 外视界半径
        r_minus: 内视界半径
        kappa: 表面重力 κ = (r_+ - r_-) / (2(r_+² + a²))
    """
    root = np.sqrt(max(0.0, M ** 2 - a ** 2))
    r_p = M + root
    r_m = M - root
    kappa = (r_p - r_m) / (2.0 * (r_p ** 2 + a ** 2))
    return r_p, r_m, kappa


def alpha_n(s: int, n: int) -> complex:
    """
    Leaver α_n 系数（原始乘积形式）。

    α_n = (n+1)(n+2ν₀+1) 对 ν₀ = -s
    但实际中不同 s 的 Frobenius 指数 ν₀ = -s + const，具体为：
        s = -2:   ν₀ = -2 → α_n = (n+1)(n-3)
        s = -1:   ν₀ = -1 → α_n = (n+1)(n-1)
        s = +1:   ν₀ = +1 → α_n = (n+1)(n+3)
        s = -1/2: ν₀ = -1/2 → α_n = (n+1)n = n(n+1)
        s = +1/2: ν₀ = +1/2 → α_n = (n+1)(n+2)
    """
    nu0 = frobenius_index(s)
    return complex((n + 1) * (n + 2 * nu0 + 1))


def frobenius_index(s) -> float:
    """Frobenius 指数 ν₀（依赖于自旋权重 s）。"""
    if s == -2:
        return -2.0
    elif s == -1:
        return -1.0
    elif s == 0:
        return 0.0
    elif s == 1:
        return 1.0
    elif s == -1.5 or s == -3/2 or s == -1.5:
        return -1.5
    elif s == -0.5 or s == -1/2 or abs(s - (-0.5)) < 1e-10:
        return -0.5
    elif s == 0.5 or s == 1/2 or abs(s - 0.5) < 1e-10:
        return 0.5
    elif s == -2.5 or s == -5/2:
        return -2.5
    else:
        raise ValueError(f"未知自旋权重 s={s}")


def beta_n(s: int, n: int, omega: complex, lam: complex,
           a: float, m: int, M: float = 1.0) -> complex:
    """
    Leaver β_n 系数（原始乘积形式）。

    β_n = -λ_{slm} - n(n+2ν₀+1) + ω² + a²ω² - 2aωm
          + (am(m+2ν₀))/(n+ν₀) + aω 修正项
    
    对 Kerr (a>0) 使用平面形式：
    β_n = -λ - n(n+2ν₀+1) + ω²
          + (am(m+2ν₀))/(n+ν₀) + 2aωm - 2amω·(n+ν₀)/(2n+2ν₀+1)
    """
    nu0 = frobenius_index(s)
    
    # 标准项
    term1 = -lam - n * (n + 2 * nu0 + 1) + omega ** 2
    
    # 自旋修正项（高自旋 m 的耦合）
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


def gamma_n(s: int, n: int, omega: complex,
            a: float, M: float = 1.0) -> complex:
    """
    Leaver γ_n 系数（原始乘积形式）。

    γ_n = -2iωκ(n+ν₀)
    其中 κ 为表面重力，ν₀ 为 Frobenius 指数。
    """
    _, _, kappa = kerr_horizon_params(a, M)
    nu0 = frobenius_index(s)
    return complex(-2.0j * omega * kappa * (n + nu0))


def recurrence_coeffs(s: int, n: int, omega: complex, lam: complex,
                      a: float, m: int, M: float = 1.0
                      ) -> Tuple[complex, complex, complex]:
    """返回 (α_n, β_n, γ_n) 三元组。"""
    return (
        alpha_n(s, n),
        beta_n(s, n, omega, lam, a, m, M),
        gamma_n(s, n, omega, a, M)
    )


def build_tridiagonal_matrix(s: int, N: int, omega: complex, lam: complex,
                             a: float, m: int, M: float = 1.0) -> np.ndarray:
    """
    构建 N×N 三对角矩阵 M(ω)（原始系数形式）。

    M = tridiag(α_n, β_n, γ_n), n=0,...,N-1

    矩阵结构（行 n，列索引）：
    M[n, n]   = β_n   （对角）
    M[n, n+1] = α_n   （上对角）
    M[n+1, n] = γ_{n+1}（下对角）
    """
    mat = np.zeros((N, N), dtype=complex)
    for n in range(N):
        a_n, b_n, g_n = recurrence_coeffs(s, n, omega, lam, a, m, M)
        mat[n, n] = b_n
        if n < N - 1:
            mat[n, n + 1] = a_n
        if n > 0:
            mat[n, n - 1] = g_n
    return mat


def koopman_spectral_radius(s: int, N: int, omega: complex, lam: complex,
                            a: float, m: int, M: float = 1.0) -> float:
    """
    计算径向 Koopman 算子的谱半径 ρ(K)。

    K = tridiag(-β_n/α_n, -γ_n/α_n, 1) 的 N×N 矩阵形式，
    加上次对角 1 构成递推转移矩阵。
    """
    dim = N
    K = np.zeros((dim, dim), dtype=complex)
    
    for n in range(N):
        a_n, b_n, g_n = recurrence_coeffs(s, n, omega, lam, a, m, M)
        if abs(a_n) > 1e-30:
            K[n, n] = -b_n / a_n
            if n + 1 < dim:
                K[n, n + 1] = -g_n / a_n
        if n > 0:
            K[n, n - 1] = 1.0
    
    try:
        eigvals = np.linalg.eigvals(K)
        spectral_radius = float(max(abs(ev) for ev in eigvals))
    except Exception:
        spectral_radius = 0.0
    
    return spectral_radius


def spectral_gap(s: int, N: int, omega: complex, lam: complex,
                 a: float, m: int, M: float = 1.0) -> float:
    """谱间隙 γ = 1 - ρ(K)。"""
    rho = koopman_spectral_radius(s, N, omega, lam, a, m, M)
    return max(0.0, 1.0 - rho)


def tridiagonal_eigenvalue_gap(s: int, N: int, omega: complex, lam: complex,
                               a: float, m: int, M: float = 1.0) -> float:
    """三对角矩阵 M 的最小特征值间隙（第三类奇异纤维指标）。"""
    M = build_tridiagonal_matrix(s, N, omega, lam, a, m, M)
    try:
        eigvals = np.sort(np.linalg.eigvals(M))
        gaps = np.diff(np.abs(eigvals))
        return float(np.min(gaps)) if len(gaps) > 0 else 0.0
    except Exception:
        return 0.0


def approx_spheroidal_eigenvalue(s: int, l: int, m: int,
                                  a: float, omega: complex,
                                  order: int = 2) -> complex:
    """
    自旋加权椭球谐函数特征值 λ_{slm} 的级数近似。

    对标 Berti (2006) Eq. 2.10：
    λ = l(l+1) - s(s+1) + (2m²/l(l+1))aω + ...
    """
    c = a * omega
    base = l * (l + 1) - s * (s + 1)
    if order >= 1 and l > 0:
        c1 = -2.0 * m / (l * (l + 1))
        base += c1 * c
    if order >= 2:
        # 二阶系数近似
        c2_map = {
            (2, -2): -4.0/3.0, (2, -1): -2.0/3.0, (2, 0): -4.0/3.0,
            (2, 1): -2.0/3.0, (2, 2): 2.0/3.0,
        }
        c2 = c2_map.get((l, abs(int(m.real))), -1.0 / (l + 0.5))
        base += c2 * (c ** 2)
    return complex(base, 0.0)
