# -*- coding: utf-8 -*-
"""
S513 修正因子全谱 Lean 化预检（先证伪再证明——模式 8）
8 例修正因子精确有理恒等 + 系数框架身份：
  1. ε_μ (1+6σ³)   = 1127/1125（6 = 活跃×幂基）
  2. 公共残差 (1−12σ³) = 1121/1125（12 = 活跃×不动点）
  3. α_s (1−7σ³)   = 3368/3375（7 = 对合域）
  4. m_ρ (1−8/3σ³) = 10117/10125（8/3 = k_max÷活跃）
  5. κ (1−2σ/3)    = 43/45（2/3 = 幂基÷活跃）
  6. fnp (1−σ²/3)  = 674/675（1/3 = 活跃⁻¹）
  7. 观测边界 (1−3σ) = 4/5（3 = 活跃）
  8. δ_hf (3/4)(1−σ) = 7/10（修正因子 (1−σ) 系数 1 单位——前置 3/4 = 活跃÷不动点）
容差 0（精确有理）。
"""
from fractions import Fraction

sigma = Fraction(1, 15)
active, powBase, fixedPoint, involution, kMax = 3, 2, 4, 7, 8

checks = [
    # (名称, 左式, 右式)
    ("ε_μ (1+6σ³)", 1 + 6 * sigma ** 3, Fraction(1127, 1125)),
    ("公共残差 (1−12σ³)", 1 - 12 * sigma ** 3, Fraction(1121, 1125)),
    ("α_s (1−7σ³)", 1 - 7 * sigma ** 3, Fraction(3368, 3375)),
    ("m_ρ (1−8/3σ³)", 1 - Fraction(8, 3) * sigma ** 3, Fraction(10117, 10125)),
    ("κ (1−2σ/3)", 1 - Fraction(2, 3) * sigma, Fraction(43, 45)),
    ("fnp (1−σ²/3)", 1 - Fraction(1, 3) * sigma ** 2, Fraction(674, 675)),
    ("观测边界 (1−3σ)", 1 - 3 * sigma, Fraction(4, 5)),
    ("δ_hf (3/4)(1−σ)", Fraction(3, 4) * (1 - sigma), Fraction(7, 10)),
    # 系数框架身份
    ("6 = 活跃×幂基", Fraction(6), active * powBase),
    ("12 = 活跃×不动点", Fraction(12), active * fixedPoint),
    ("7 = 对合域", Fraction(7), involution),
    ("8/3 = k_max÷活跃", Fraction(8, 3), Fraction(kMax, active)),
    ("2/3 = 幂基÷活跃", Fraction(2, 3), Fraction(powBase, active)),
    ("1/3 = 活跃⁻¹", Fraction(1, 3), Fraction(1, active)),
    ("3 = 活跃", Fraction(3), active),
    ("3/4 = 活跃÷不动点", Fraction(3, 4), Fraction(active, fixedPoint)),
]

print("=" * 78)
print("S513 修正因子全谱 Lean 化预检（精确有理）")
print("=" * 78)
all_ok = True
for name, lhs, rhs in checks:
    ok = lhs == rhs
    all_ok = all_ok and ok
    print("   %-28s %-22s —— %s" % (name, str(lhs), ok))
print()
print("全部恒等一致：%s" % all_ok)
