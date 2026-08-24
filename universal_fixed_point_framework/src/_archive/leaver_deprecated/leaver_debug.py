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
Leaver CF 逐 n 比对诊断。

比较两个实现中每个 n 的 alpha, beta, gamma, cf 值。
输入：a=0, M=1, s=-2, l=2, m=0, ω=0.373672-0.088962j, λ=4.0
"""

import numpy as np


def old_implementation(omega, lam, m, a=0.0, M=1.0, s=-2, max_iter=5):
    """physics_open_problems_advanced.py 中的系数公式"""
    r_plus = M + np.sqrt(M**2 - a**2)
    r_minus = M - np.sqrt(M**2 - a**2)
    sigma_plus = (omega * r_plus - a * m) / (r_plus - r_minus)

    print(f"  sigma_plus = {sigma_plus:.8f}")

    cf = complex(0.0, 0.0)
    for n in range(max_iter, 0, -1):
        alpha = -2.0j * omega * (n + 1.0) * (n - 4.0j * sigma_plus)
        beta = (n * (n + 1.0) + 4.0 * sigma_plus**2
                - 8.0 * omega * sigma_plus - complex(lam, 0.0))
        gamma_next = 2.0j * omega * ((n + 1) - 4.0j * sigma_plus - 1.0)
        print(f"  n={n}: α={alpha:.6e} β={beta:.6e} γ(n+1)={gamma_next:.6e}")
        denom = beta - alpha * gamma_next * cf
        print(f"        denom={denom:.6e}")
        if abs(denom) < 1e-30:
            denom = complex(1e-30, 0.0)
        cf = 1.0 / denom
        print(f"        cf={cf:.6e}")

    beta_0 = (4.0 * sigma_plus**2 - 8.0 * omega * sigma_plus - complex(lam, 0.0))
    alpha_0 = -2.0j * omega * 1.0 * (-4.0j * sigma_plus)
    gamma_1 = 2.0j * omega * (1.0 - 4.0j * sigma_plus - 1.0)
    print(f"  n=0: α₀={alpha_0:.6e} β₀={beta_0:.6e} γ₁={gamma_1:.6e}")
    result = beta_0 - alpha_0 * gamma_1 * cf
    print(f"  residual = β₀ - α₀·γ₁·cf = {result:.6e}")
    return result


def my_implementation(omega, lam, m, a=0.0, M=1.0, s=-2, max_iter=5):
    """kerr_fixed_solver.py 中的系数公式"""
    r_plus = M + np.sqrt(M**2 - a**2)
    r_minus = M - np.sqrt(M**2 - a**2)
    sigma_plus = (omega * r_plus - a * m) / (r_plus - r_minus)

    print(f"  sigma_plus = {sigma_plus:.8f}")

    cf = complex(0.0, 0.0)
    for n in range(max_iter, 0, -1):
        alpha = -2.0j * omega * (n + 1.0) * (n - 4.0j * sigma_plus)
        beta = (n * (n + 1.0) + 4.0 * sigma_plus**2
                - 8.0 * omega * sigma_plus - lam)
        gamma_next = 2.0j * omega * ((n + 1) - 4.0j * sigma_plus - 1.0)
        print(f"  n={n}: α={alpha:.6e} β={beta:.6e} γ(n+1)={gamma_next:.6e}")
        denom = beta - alpha * gamma_next * cf
        print(f"        denom={denom:.6e}")
        if abs(denom) < 1e-30:
            denom = complex(1e-30, 0.0)
        cf = 1.0 / denom
        print(f"        cf={cf:.6e}")

    beta_0 = (4.0 * sigma_plus**2 - 8.0 * omega * sigma_plus - lam)
    alpha_0 = -2.0j * omega * 1.0 * (-4.0j * sigma_plus)
    gamma_1 = 2.0j * omega * (1.0 - 4.0j * sigma_plus - 1.0)
    print(f"  n=0: α₀={alpha_0:.6e} β₀={beta_0:.6e} γ₁={gamma_1:.6e}")
    result = beta_0 - alpha_0 * gamma_1 * cf
    print(f"  residual = β₀ - α₀·γ₁·cf = {result:.6e}")
    return result


# 测试输入
omega_true = complex(0.373672, -0.088962)
lam_true = 4.0  # l=2, s=-2, a=0: λ = l(l+1)-s(s+1) = 4

print("=" * 72)
print("  Old implementation:")
print("=" * 72)
r1 = old_implementation(omega_true, lam_true, 0, max_iter=5)

print("\n" + "=" * 72)
print("  My implementation:")
print("=" * 72)
r2 = my_implementation(omega_true, lam_true, 0, max_iter=5)

print("\n" + "=" * 72)
print(f"  差异: Δresidual = {abs(r1 - r2):.2e}")
print("=" * 72)
