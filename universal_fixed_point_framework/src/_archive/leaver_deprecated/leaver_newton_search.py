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
在正确 ω 附近做 Newton 迭代，找 Leaver CF 的根。

输入：a=0, M=1, s=-2, l=2, m=0, λ=4
初始猜测：ω₀ = 0.373672 - 0.088962j
"""

import numpy as np


def radial_cf(omega, lam, m, a=0.0, M=1.0, max_iter=500):
    r_p = M + np.sqrt(M**2 - a**2)
    r_m = M - np.sqrt(M**2 - a**2)
    sigma_plus = (omega * r_p - a * m) / (r_p - r_m)

    cf = complex(0.0, 0.0)
    for n in range(max_iter, 0, -1):
        alpha = -2.0j * omega * (n + 1.0) * (n - 4.0j * sigma_plus)
        beta = (n * (n + 1.0) + 4.0 * sigma_plus**2
                - 8.0 * omega * sigma_plus - lam)
        gamma_next = 2.0j * omega * ((n + 1) - 4.0j * sigma_plus - 1.0)
        denom = beta - alpha * gamma_next * cf
        if abs(denom) < 1e-30:
            denom = complex(1e-30, 0.0)
        cf = 1.0 / denom
    beta_0 = (4.0 * sigma_plus**2 - 8.0 * omega * sigma_plus - lam)
    alpha_0 = -2.0j * omega * 1.0 * (-4.0j * sigma_plus)
    gamma_1 = 2.0j * omega * (1.0 - 4.0j * sigma_plus - 1.0)
    return beta_0 - alpha_0 * gamma_1 * cf


omega = complex(0.373672, -0.088962)
lam = 4.0
eps = 1e-8

print("=" * 72)
print("  Newton 迭代找 a=0 Leaver CF 的根")
print("=" * 72)
print(f"\n  初始: ω = {omega.real:.6f} {omega.imag:+.6f}i")
print(f"  λ = {lam}")

for i in range(30):
    f = radial_cf(omega, lam, 0)
    print(f"\n  iter {i:2d}: ω={omega.real:.8f} {omega.imag:+.8f}i  |f|={abs(f):.4e}")
    if abs(f) < 1e-12:
        print(f"  ✅ 收敛")
        break

    f_re = radial_cf(omega + eps, lam, 0)
    f_im = radial_cf(omega + 1j*eps, lam, 0)
    jac = np.array([
        [(f_re - f).real / eps, (f_im - f).real / eps],
        [(f_re - f).imag / eps, (f_im - f).imag / eps],
    ])
    try:
        delta = np.linalg.solve(jac, -np.array([f.real, f.imag]))
    except np.linalg.LinAlgError:
        print("  Jacobian 奇异")
        break

    # 线搜索
    for step in [1.0, 0.5, 0.25, 0.1]:
        w_new = omega + step * complex(delta[0], delta[1])
        if w_new.imag > 0:
            w_new = complex(w_new.real, -1e-10)
        f_new = radial_cf(w_new, lam, 0)
        if abs(f_new) < abs(f) * (1.0 + 1e-6):
            omega = w_new
            break
