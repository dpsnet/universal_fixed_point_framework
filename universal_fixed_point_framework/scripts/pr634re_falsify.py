# -*- coding: utf-8 -*-
"""第 53 批 模式 8 数值先证伪：
   命题 A：在 f >= 3 上，f^2 - 1 = 2^f - 1  <=>  f = 4（唯一重合点）
   命题 B：数值 15 反解两条形式的 f 都唯一（f = 4），故「数值唯一」但「函数形式不唯一」
   命题 C：f = 3 / 5 两处分歧的显式值
"""
import sys

SIGMA_INV = 15
F_MAX = 400

sq = lambda f: f * f - 1
mer = lambda f: (1 << f) - 1          # 2^f - 1
pm1 = lambda f: (1 << (f - 1)) - 1 if f >= 1 else -1   # 2^(f-1) - 1

print("== A. 两形式重合点（f 从 2 到 %d）==" % F_MAX)
coin = [f for f in range(2, F_MAX + 1) if sq(f) == mer(f)]
print("COINCIDE_SET", coin)
print("A_HOLDS", coin == [2, 4])

coin3 = [f for f in range(3, F_MAX + 1) if sq(f) == mer(f)]
print("COINCIDE_SET_GE3", coin3)
print("A_HOLDS_GE3", coin3 == [4])

print("== B. 数值 %d 反解 ==" % SIGMA_INV)
sq_roots = [f for f in range(1, F_MAX + 1) if sq(f) == SIGMA_INV]
mer_roots = [f for f in range(1, F_MAX + 1) if mer(f) == SIGMA_INV]
pm1_roots = [f for f in range(1, F_MAX + 1) if pm1(f) == SIGMA_INV]
print("SQ_ROOTS", sq_roots)
print("MER_ROOTS", mer_roots)
print("PM1_ROOTS", pm1_roots)
print("B_VALUE_UNIQUE", sq_roots == [4] and mer_roots == [4])
print("B_FORM_NOT_UNIQUE", sq_roots == mer_roots == [4] and pm1_roots != [4])

print("== C. 分歧点显式值 ==")
for f in (3, 5, 6, 7, 8):
    print("F %d  SQ_INV %d  MER_INV %d  DIFF %+d  PM1 %d"
          % (f, sq(f), mer(f), mer(f) - sq(f), pm1(f)))

print("== D. 三条候选形式两两重合点（f = 2..60）==")
def coincide(x, y, lo=2, hi=60):
    return [f for f in range(lo, hi + 1) if x(f) == y(f)]
print("SQ_vs_MER", coincide(sq, mer))
print("SQ_vs_PM1", coincide(sq, pm1))
print("MER_vs_PM1", coincide(mer, pm1))

print("== E. 各自在 f=4 的取值 ==")
print("SQ4", sq(4), "MER4", mer(4), "PM1_4", pm1(4))
print("E_TWO_AGREE_ONE_DISAGREE", sq(4) == mer(4) == 15 and pm1(4) == 7)

print("VERDICT_A", coin3 == [4])
print("VERDICT_B", sq_roots == [4] and mer_roots == [4])
print("VERDICT_C", sq(3) == 8 and mer(3) == 7 and sq(5) == 24 and mer(5) == 31)
print("VERDICT_D", coincide(sq, mer) == [2, 4])
print("VERDICT_ALL_OK", coin3 == [4] and sq_roots == [4] and mer_roots == [4]
      and sq(3) == 8 and mer(3) == 7 and sq(5) == 24 and mer(5) == 31
      and coincide(sq, mer) == [2, 4])
