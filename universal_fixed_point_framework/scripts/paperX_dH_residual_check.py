#!/usr/bin/env python3
"""
检查 d_H 残差 8×10⁻⁷ 与 2^3×10⁻⁷ = 8×10⁻⁷ 的关系。
"""
import numpy as np

ln15 = np.log(15)
sqrt5 = np.sqrt(5)

# 从自洽方程求 d (ε̄/ε₃ = √5)
def solve_d_for_k(k):
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

d_k = solve_d_for_k(sqrt5)
d_fit = 2.7095
residual = d_fit - d_k

print("=" * 60)
print("残差分析: d_H = d_√5 + Δ")
print("=" * 60)
print(f"  d_√5 (k=√5 的解)       = {d_k:.10f}")
print(f"  d_H_fit                = {d_fit:.10f}")
print(f"  残差 Δ                 = {residual:.2e}")
print(f"  2³ × 10⁻⁷             = {8e-7:.2e}")
print(f"  |Δ - 8×10⁻⁷|          = {abs(residual - 8e-7):.2e}")

# 检查不同 d_H 精度下的稳定性
print("\n" + "-" * 60)
print("稳健性: 残差对 d_H 输入精度的依赖")
print("-" * 60)
for d_h in [2.7095, 2.70950, 2.709500, 2.7095000]:
    resid = d_h - d_k
    match_8 = abs(resid - 8e-7)
    print(f"  d_H = {d_h:.8f}  →  Δ = {resid:.2e}  |Δ-8e-7| = {match_8:.2e}")

# 如果残差 = 2^N_active × 10⁻⁷ 有意义, 检查 k 需要调整多少
print("\n" + "-" * 60)
print("反问题: 若 Δ=8×10⁻⁷ 是系统性的, 求 k'")
print("-" * 60)
# 假设 d_H = solve(k') + 8e-7, 求 k'
# 需解 d_H - 8e-7 在方程中的 k
target_d = d_fit - 8e-7
print(f"  目标 d = {d_fit} - 8×10⁻⁷ = {target_d:.10f}")

def find_k_for_d(d_target):
    def g(k):
        d_sol = solve_d_for_k(k)
        return d_sol - d_target
    lo_k, hi_k = 2.23, 2.24
    for _ in range(100):
        mid = (lo_k+hi_k)/2
        if g(mid)*g(lo_k) > 0:
            lo_k = mid
        else:
            hi_k = mid
    return (lo_k+hi_k)/2

try:
    k_corrected = find_k_for_d(target_d)
    print(f"  修正后 k' = {k_corrected:.8f}")
    print(f"  √5        = {sqrt5:.8f}")
    print(f"  偏差      = {abs(k_corrected - sqrt5):.2e}")
    print(f"  相对偏差  = {abs(k_corrected - sqrt5)/sqrt5*100:.4f}%")
except:
    print("  (求解范围越界)")

# 检查 N_active = 3 的其他表达式
print("\n" + "-" * 60)
print("与 N_active = 3 相关的候选修正因子")
print("-" * 60)
candidates = [
    ("2^N_active × 10⁻⁷", 2**3 * 1e-7),
    ("N_active × 10⁻⁷", 3 * 1e-7),
    ("(2^N_active - 1) × 10⁻⁷", (2**3 - 1) * 1e-7),
    ("ln(2^N_active) × 10⁻⁷", np.log(8) * 1e-7),
    ("(d_H/ln15)^2 × 10⁻⁶", (d_fit/ln15)**2 * 1e-6),
]
for name, val in candidates:
    match = abs(residual - val)
    pct = match / abs(residual) * 100 if residual != 0 else 0
    print(f"  {name:>30s} = {val:.2e}  |Δ - val| = {match:.2e}  ({pct:.1f}%)")

print("\n" + "=" * 60)
print("诚实判断")
print("=" * 60)
print(f"""
  残差 Δ = {residual:.2e}
  8×10⁻⁷  = {8e-7:.2e}
  |Δ - 8×10⁻⁷| = {abs(residual - 8e-7):.2e}

  如果残差完全随机: 无意义。
  如果残差 = 2³×10⁻⁷: 有意义（Bott 翻倍 × 三代量级）。
  即使有意义: 即使用 6 位 d_H 有效数字也只能确认
  残差的量级（10⁻⁷），无法确认其精确值。
  
  更可能: 残差是 k=√5 的自洽方程的一阶近似误差。
  用 k = √5 + δk 的高阶修正可以吸收残差。
""")
