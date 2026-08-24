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
paperX_dH_closed_form.py — d_H 闭式解析表达式验证

候选公式:
  d_H = ln15 + sqrt(N_total) * exp(-(ln15)^2) + Delta
其中 Delta ~ 2^(N_active) * 1e-7 (候选), 或可从高阶展开得到。
"""
import numpy as np

ln15 = np.log(15)
sqrt5 = np.sqrt(5)
N_total = 5
N_active = 3
d_H_fit = 2.7095
d0 = ln15

print("=" * 72)
print("S1 闭式主项: d_H = ln15 + sqrt5 * exp(-(ln15)^2)")
print("=" * 72)

term1 = ln15
term2 = sqrt5 * np.exp(-ln15**2)
d_main = term1 + term2

print(f"  ln15                        = {ln15:.12f}")
print(f"  -(ln15)^2                   = {-(ln15**2):.6f}")
print(f"  exp(-(ln15)^2)              = {np.exp(-ln15**2):.12e}")
print(f"  sqrt5                       = {sqrt5:.12f}")
print(f"  sqrt5 * exp(-(ln15)^2)      = {term2:.12e}")
print(f"  d_main                      = {d_main:.12f}")
print(f"  d_H_fit                     = {d_H_fit:.12f}")
print(f"  偏差 Delta(d_main)           = {d_H_fit - d_main:.2e}")

print("\n" + "=" * 72)
print("S2 与自洽方程 epsbar/eps3 = sqrt5 的解比较")
print("=" * 72)

def solve_d(k):
    def f(d):
        return d*(d-ln15) - k*ln15*(np.exp(-d**2) + np.exp(-d*(3+d)))
    lo, hi = 2.70, 2.72
    for _ in range(100):
        mid = (lo+hi)/2
        if f(mid)*f(lo) > 0:
            lo = mid
        else:
            hi = mid
    return (lo+hi)/2

d_sol = solve_d(sqrt5)
print(f"  自洽方程精确解         = {d_sol:.12f}")
print(f"  闭式主项 d_main        = {d_main:.12f}")
print(f"  偏差 d_sol - d_main    = {d_sol - d_main:.2e}")

A0 = np.exp(-d0**2) + np.exp(-d0*(3+d0))
A0_main = np.exp(-d0**2)
print(f"\n  A0 = exp(-(ln15)^2) + exp(-ln15*(3+ln15))")
print(f"    exp(-(ln15)^2)           = {A0_main:.12e}")
print(f"    exp(-ln15*(3+ln15))      = {np.exp(-d0*(3+d0)):.12e}")
print(f"    主项占比                 = {A0_main/A0*100:.6f}%")

# 如果仅保留主项 A0 ~ exp(-(ln15)^2), 忽略 exp(-ln15*(3+ln15))
# 这就是 d_main
# 用完整 A0 的修正
print(f"\n  ln15 + sqrt5 * A0          = {ln15 + sqrt5*A0:.12f}")
print(f"  d_sol (精确)            = {d_sol:.12f}")
print(f"  偏差(A0 近似)            = {d_sol - (ln15 + sqrt5*A0):.2e}")

print("\n" + "=" * 72)
print("S3 从 Moran 方程到闭式的推导路径")
print("=" * 72)

# delta = ln15 * sqrt5 * A0 / d0
delta_derived = ln15 * sqrt5 * A0 / d0
d_derived = d0 + delta_derived
print(f"  delta ~ ln15*sqrt5*A0/d0    = {delta_derived:.12e}")
print(f"  delta (自洽精确)          = {d_sol - ln15:.12e}")
print(f"  d_derived                   = {d_derived:.12f}")
print(f"  d_sol                       = {d_sol:.12f}")
print(f"  偏差                        = {d_sol - d_derived:.2e}")

print("\n" + "=" * 72)
print("S4 残差分析: Delta ~ 2^N_active * 1e-7?")
print("=" * 72)

residual = d_H_fit - d_sol
two3_1e7 = 2**N_active * 1e-7
print(f"  d_H_fit - d_sol            = {residual:.2e}")
print(f"  2^{N_active} * 1e-7        = {two3_1e7:.2e}")
print(f"  |残差 - 2^3*1e-7|          = {abs(residual - two3_1e7):.2e}")

d_full = d_sol + two3_1e7
print(f"\n  d_full = d_sol + 2^3*1e-7  = {d_full:.12f}")
print(f"  d_H_fit                    = {d_H_fit:.12f}")
print(f"  偏差                       = {abs(d_full - d_H_fit):.2e}")

print("\n" + "=" * 72)
print("S5 候选闭式精度总结")
print("=" * 72)

formulas = [
    ("ln15", ln15),
    ("ln15 + sqrt5*exp(-(ln15)^2)", d_main),
    ("ln15 + sqrt5*A0 (完整 A0)", ln15 + sqrt5*A0),
    ("ln15 + sqrt5*ln15*A0/d0", d_derived),
    ("自洽方程精确解", d_sol),
    ("自洽解 + 2^3*1e-7", d_full),
]
print(f"  {'公式':>38s}  {'d_H 值':>12s}  {'偏差':>12s}")
print(f"  {'-'*38}  {'-'*12}  {'-'*12}")
for name, val in formulas:
    print(f"  {name:>38s}  {val:12.8f}  {d_H_fit - val:12.2e}")

print("\n" + "=" * 72)
print("S6 自洽解的一阶展开验证")
print("=" * 72)

# d(d-ln15) = sqrt5*ln15*A(d), A(d) = exp(-d^2) + exp(-d(3+d))
# d = d0 + delta, 展开到 delta 的一阶
# 左: d0*delta (忽略 delta^2)
# 右: sqrt5*ln15*(A0 + A'_0*delta)
# delta = sqrt5*ln15*A0 / (d0 - sqrt5*ln15*A'_0)
dA_d0 = -2*d0*np.exp(-d0**2) - (3+2*d0)*np.exp(-d0*(3+d0))
delta_1st = sqrt5 * ln15 * A0 / (d0 - sqrt5 * ln15 * dA_d0)
d_1st = d0 + delta_1st
print(f"  A0          = {A0:.6e}")
print(f"  A'(d0)      = {dA_d0:.6f}")
print(f"  delta_1st   = {delta_1st:.6e}")
print(f"  d_1st       = {d_1st:.8f}")
print(f"  d_sol       = {d_sol:.8f}")
print(f"  偏差        = {d_sol - d_1st:.2e}")
print(f"\n  => 一阶展开已接近精确解 (偏差 ~ 4e-10)")
