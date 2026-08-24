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
"""临时诊断：Dirac 产品形式 CF 在参考频率处的行为。"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _dirac_leaver_solver import (
    dirac_recurrence_coeffs, radial_continued_fraction,
    find_dirac_qnm, dirac_angular_eigenvalue_approx
)

s, l, m, a = -0.5, 0.5, 0.5, 0.0
omega_ref = 0.378721 - 0.096458j

# ===== λ 的正确值 =====
lam_formula = complex(l*(l+1) - s*(s+1), 0.0)
lam_approx = dirac_angular_eigenvalue_approx(s, l, m, a, omega_ref, order=2)

print(f"s={s}  l={l}  m={m}  a={a}")
print(f"ω_ref = {omega_ref:+.10f}")
print(f"λ(formula) = {lam_formula}")
print(f"λ(approx)  = {lam_approx}")
print()

# ===== 检查 λ 对 CF 的影响 =====
print("=== λ 扫描 (固定 ω_ref) ===")
for lam_try in [0.5, 0.8, 1.0, 1.2, 1.5, 2.0, 3.0, 4.0]:
    r = radial_continued_fraction(s, omega_ref, complex(lam_try), a, m, N_max=200)
    print(f"  λ={lam_try:.1f}  |R₀|={abs(r):.6e}")

print()
print("=== 系数表 (λ=1) ===")
for n in range(6):
    a_n, b_n, g_n = dirac_recurrence_coeffs(s, n, omega_ref, lam_formula, a, m)
    print(f"n={n}:  α={a_n.real:+.4e}  β={b_n.real:+.4e}{b_n.imag:+.4e}j  γ={g_n.real:+.4e}{g_n.imag:+.4e}j")

print()
print("=== CF 截断收敛 ===")
for N in [10, 20, 50, 100, 200, 400, 800]:
    r = radial_continued_fraction(s, omega_ref, lam_formula, a, m, N_max=N)
    print(f"  N={N:4d}  |R₀|={abs(r):.6e}")

print()
print("=== 关键诊断 ===")
a0, b0, g0 = dirac_recurrence_coeffs(s, 0, omega_ref, lam_formula, a, m)
print(f"α₀ = {a0}")
print(f"β₀ = {b0}")
print(f"ω²-λ = {omega_ref**2 - lam_formula}")
print(f"α₀=0 → 代码 R₀ = β₁ - α₁·r₁ (n_start=1)")
print(f"这个值应该等于 β₀ · (CF tail)?")

print()
print("=== ω 扫描: Re(ω) 固定 0.379, 变 Im(ω) ===")
for im in [0.0, -0.02, -0.04, -0.06, -0.08, -0.096458, -0.12, -0.14, -0.16]:
    w = complex(0.378721, im)
    r = radial_continued_fraction(s, w, lam_formula, a, m, N_max=200)
    print(f"  Im={im:+.6f}  |R₀|={abs(r):.6e}  R₀={r:.4e}")

print()
print("=== ω 扫描: Im(ω) 固定 -0.096, 变 Re(ω) ===")
for re in [0.0, 0.1, 0.2, 0.3, 0.35, 0.378721, 0.4, 0.5, 0.6, 0.7]:
    w = complex(re, -0.096458)
    r = radial_continued_fraction(s, w, lam_formula, a, m, N_max=200)
    print(f"  Re={re:+.4f}  |R₀|={abs(r):.6e}  R₀={r:.4e}")

print()
print("=== 对比: 多项式形式 (Cook-Zalutskiy D 系数) ===")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dynamic_spectrum"))
from leaver_unified_solver import LeaverResidual
lr = LeaverResidual(M=1.0, a=a, s=int(s), max_iter=200)
r_poly = lr.radial_cf_polynomial(omega_ref, lam_formula, int(m))
print(f"  |R₀_poly| = {abs(r_poly):.6e}")
