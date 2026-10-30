# -*- coding: utf-8 -*-
"""
S505 公共残差恒等 Lean 化预检（先证伪再证明——模式 8）
目标恒等（全部精确有理——norm_num/ring 级）：
  1. sigma = 1/15；active = 3；powBase = 2；fixedPoint = 4；
     silenceUnit = 5；24 = 4!
  2. 30·σ⁵ = 2·σ⁴（S489——σ⁴ 禁制替代）
  3. 30 = 静默×活跃×幂基（S489 多身份）
  4. 12 = 活跃×不动点（S502）
  5. 12σ³ = 4/1125（S500 有理形式）
  6. 1−12σ³ = 1121/1125（S500）
  7. 公共残差 = 30σ⁵(1−12σ³) = 30σ⁵−360σ⁸（S494——360 = 5×24×3）
  8. 公共残差 = 2242/56953125（S504）
  9. 360 = 静默×4!×活跃（S494）
残差容差 1e-8——全部为 0 才可投入证明。
"""
from fractions import Fraction

sigma = Fraction(1, 15)
active = 3
powBase = 2
fixedPoint = 4
silenceUnit = 5

checks = []
# 2. 30σ⁵ = 2σ⁴
checks.append(("30·σ⁵ = 2·σ⁴", 30 * sigma**5, 2 * sigma**4))
# 3. 30 = 5×3×2
checks.append(("30 = 静默×活跃×幂基", Fraction(30), silenceUnit * active * powBase))
# 4. 12 = 3×4
checks.append(("12 = 活跃×不动点", Fraction(12), active * fixedPoint))
# 5. 12σ³ = 4/1125
checks.append(("12σ³ = 4/1125", 12 * sigma**3, Fraction(4, 1125)))
# 6. 1−12σ³ = 1121/1125
checks.append(("1−12σ³ = 1121/1125", 1 - 12 * sigma**3, Fraction(1121, 1125)))
# 7. 30σ⁵(1−12σ³) = 30σ⁵−360σ⁸
lhs7 = 30 * sigma**5 * (1 - 12 * sigma**3)
rhs7 = 30 * sigma**5 - 360 * sigma**8
checks.append(("30σ⁵(1−12σ³) = 30σ⁵−360σ⁸", lhs7, rhs7))
# 8. 公共残差 = 2242/56953125
checks.append(("公共残差 = 2242/56953125", lhs7, Fraction(2242, 56953125)))
# 9. 360 = 5×24×3
checks.append(("360 = 静默×4!×活跃", Fraction(360), silenceUnit * 24 * active))
# 附加：30σ⁵ = 2/50625
checks.append(("30σ⁵ = 2/50625", 30 * sigma**5, Fraction(2, 50625)))
# 附加：2242 = 2×1121；56953125 = 50625×1125
checks.append(("2242 = 2×1121", Fraction(2242), 2 * 1121))
checks.append(("56953125 = 50625×1125", Fraction(56953125), 50625 * 1125))

print("=" * 78)
print("S505 公共残差恒等 Lean 化预检（精确有理）")
print("=" * 78)
all_ok = True
for name, lhs, rhs in checks:
    ok = lhs == rhs
    all_ok = all_ok and ok
    print("   %-34s %s —— 一致 %s" % (name, lhs, ok))
print()
print("全部恒等一致：%s" % all_ok)
