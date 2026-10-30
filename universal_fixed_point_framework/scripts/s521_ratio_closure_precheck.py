# -*- coding: utf-8 -*-
"""
S521 预检：比值复合律 + k_max 身份恒等（Lean 化前——模式 8）
目标恒等（纯有理）：
  1. 静默/幂基 = 5/2
  2. 幂基/活跃 = 2/3
  3. 静默/活跃 = 5/3
  4. 比值复合律：(5/2)×(2/3) = 5/3
  5. k_max = 幂基³（8 = 2³）
  6. k_max = 不动点×幂基（8 = 4×2）
  7. 不动点 = 幂基²（4 = 2²）
  8. 复合：(5/2)(2/3) 与 5/3 数值残差 = 0
"""
from fractions import Fraction

# 框架常数
active, powBase, silence, fixedPoint, kMax, involution = 3, 2, 5, 4, 8, 7

checks = [
    ("静默/幂基 = 5/2", Fraction(silence, powBase), Fraction(5, 2)),
    ("幂基/活跃 = 2/3", Fraction(powBase, active), Fraction(2, 3)),
    ("静默/活跃 = 5/3", Fraction(silence, active), Fraction(5, 3)),
    ("比值复合：(5/2)(2/3)", Fraction(silence, powBase) * Fraction(powBase, active), Fraction(silence, active)),
    ("k_max = 幂基³", kMax, powBase ** 3),
    ("k_max = 不动点×幂基", kMax, fixedPoint * powBase),
    ("不动点 = 幂基²", fixedPoint, powBase ** 2),
    ("比值复合残差", float(Fraction(silence, powBase) * Fraction(powBase, active) - Fraction(silence, active)), 0.0),
]
print("S521 预检——比值复合律 + k_max 身份（模式 8 先证伪）")
all_ok = True
for name, lhs, rhs in checks:
    ok = lhs == rhs
    all_ok = all_ok and ok
    print("  %-28s %s == %s → %s" % (name, lhs, rhs, "PASS" if ok else "FAIL"))
print("\n结论：%s" % ("全部一致——可投入 Lean 证明" if all_ok else "有失败——需勘误"))
