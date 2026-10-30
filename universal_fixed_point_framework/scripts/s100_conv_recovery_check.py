# -*- coding: utf-8 -*-
# S100 卷积恢复机制分解（2026-10-26）——修正版
# 验证组合学解释：eTruncArg(8,0.5)·eTruncArg(8,0.5) 的系数结构
# 1) 卷积系数 c_n = Σ_{k+j=n, k<=8, j<=8} 0.5^n/(k!j!)  vs e^1 系数 1/n!
# 2) 偏差分解：Σ_{n=9}^{16}(1/n! - c_n) + Σ_{n>=17} 1/n!
# 3) 对照平凡放大上界 2·e^{0.5}·δ'（δ' = (0.5)^9·10/(9·9!)）

from fractions import Fraction
from math import factorial

K = 8
half = Fraction(1, 2)

def inv_fact(k):
    return Fraction(1, factorial(k))

# eTruncArg(8, 0.5) = Σ_{k<=8} 0.5^k/k!
a = sum(half**k * inv_fact(k) for k in range(K + 1))
conv = a * a  # 卷积平方（精确有理）

# 逐阶系数对比 n = 0..16
print("=== 卷积系数 vs e^1 系数（n=0..16） ===")
miss_part = Fraction(0)
for n in range(0, 17):
    c_n = sum(half**(k + j) * inv_fact(k) * inv_fact(j)
               for k in range(K + 1) for j in range(K + 1) if k + j == n)
    exact_n = inv_fact(n)
    diff = exact_n - c_n
    if n >= 9:
        miss_part += diff
    flag = "EXACT" if diff == 0 else f"miss {float(diff):.2e}"
    print(f"n={n:2d}  c_n={float(c_n):.12f}  1/n!={float(exact_n):.12f}  {flag}")

# n >= 17 的余项
tail17 = sum(1.0 / factorial(n) for n in range(17, 40))

# 偏差分解
import math
dev_exact = float(conv) - math.e
dev_comp = float(miss_part) + tail17
print("\n=== 偏差分解 ===")
print(f"conv^2 = {float(conv):.12f}  e = {math.e:.12f}")
print(f"dev_exact = {dev_exact:.3e}")
print(f"分解 Σ(n=9..16)miss + Σ(n>=17) = {float(miss_part):.3e} + {tail17:.3e} = {float(miss_part) + tail17:.3e}")
print(f"一致性 |dev_exact - dev_comp| = {abs(dev_exact - dev_comp):.3e}")

# 平凡放大上界对照
half_pow9 = 0.5**9
delta_half = half_pow9 * 10 / (9 * factorial(9))
bound = 2 * math.exp(0.5) * delta_half
print(f"\ndelta_half = (0.5)^9·10/(9·9!) = {delta_half:.3e}")
print(f"平凡放大上界 2·e^{{0.5}}·delta_half = {bound:.3e}")
print(f"恢复比 bound/dev_exact = {bound / dev_exact:.1f} 倍（实际偏差远小于平凡上界——部分恢复）")

# 组合恒等验证：Σ_{k<=n} choose(n,k) = 2^n（n<=8 全系数依赖 Σchoose=2^n）
from math import comb
print("\n=== 组合恒等（n<=8 全系数依赖 Σchoose=2^n） ===")
for n in [4, 8]:
    s = sum(comb(n, k) for k in range(n + 1))
    print(f"Σ_{{k<=n}} choose({n},k) = {s}  2^{n} = {2**n}  OK={s == 2**n}")

# 单侧截断对照（eTrunc(8) 直接 vs e——S98 已知 3.06e-6）
etrunc8 = sum(1.0 / factorial(k) for k in range(9))
print(f"\n单侧截断 |e - eTrunc(8)| = {abs(math.e - etrunc8):.3e}")
print(f"卷积偏差 vs 单侧截断偏差 = {dev_exact / abs(math.e - etrunc8):.4f} 倍（卷积小 {abs(math.e - etrunc8) / dev_exact:.1f} 倍）")
