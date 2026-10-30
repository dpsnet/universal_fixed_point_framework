# -*- coding: utf-8 -*-
"""
S464 先证伪：R2a 指数步进代数侧（2026-10-29）
==============================================
S428 权威语义：18=16+2（全态+幂基——幂基步）、19=16+3
（全态+活跃——活跃步）——e 链指数步进。
代数侧锚候选（数学事实）：
  D1: e^{-18} = e^{-16}·e^{-2}（幂基步分解）
  D2: e^{-19} = e^{-16}·e^{-3}（活跃步分解）
  D3: 通用指数加法分解 exp(-(m+n)) = exp(-m)·exp(-n)
  D4: 数值恒等 18=16+2、19=16+3（norm_num 级）
验证残差容差 1e-12。
"""
import math

print("=" * 70)
print("S464 R2a 指数步进代数侧数值先证伪")
print("=" * 70)

# D1: e^{-18} = e^{-16}·e^{-2}
lhs = math.exp(-18.0)
rhs = math.exp(-16.0) * math.exp(-2.0)
res1 = abs(lhs - rhs)
assert res1 < 1e-12, f"D1 残差 {res1}"
print(f"D1 e^-18 = e^-16·e^-2 ✓  残差 {res1:.2e}")

# D2: e^{-19} = e^{-16}·e^{-3}
lhs2 = math.exp(-19.0)
rhs2 = math.exp(-16.0) * math.exp(-3.0)
res2 = abs(lhs2 - rhs2)
assert res2 < 1e-12, f"D2 残差 {res2}"
print(f"D2 e^-19 = e^-16·e^-3 ✓  残差 {res2:.2e}")

# D3: 通用分解（30 组随机 m,n）
import random
random.seed(20261029)
max_res = 0.0
for _ in range(30):
    m = random.uniform(0.5, 30.0)
    n = random.uniform(0.5, 30.0)
    r = abs(math.exp(-(m + n)) - math.exp(-m) * math.exp(-n))
    max_res = max(max_res, r)
assert max_res < 1e-9, f"D3 最大残差 {max_res}"
print(f"D3 通用 exp(-(m+n)) = exp(-m)·exp(-n)（30 组）✓  最大残差 {max_res:.2e}")

# D4: 数值恒等
assert 18 == 16 + 2 and 19 == 16 + 3
print("D4 18=16+2、19=16+3 ✓")

# 补充：五口径指数复核（S419 构造）
print("\n[五口径指数复核]")
constr = {
    "2018": 0,
    "Cs": 19,    # e^-19 活跃步
    "a_e": 18,   # e^-18 幂基步
    "Rb": 18,    # e^-18 幂基步
    "2022": "σ⁷",
}
for k, v in constr.items():
    print(f"  {k:<6} 指数 = {v}")

print("\n结论：D1-D4 全通过——R2a 指数步进锚可 Lean 化")
