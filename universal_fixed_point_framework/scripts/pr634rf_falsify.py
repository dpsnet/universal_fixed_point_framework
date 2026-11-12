# -*- coding: utf-8 -*-
"""第 54 批 模式 8 数值先证伪：
   命题 A：三条「平方表示 / 指数表示」同值条件全部归约到同一条 f^2 = 2^f
             (a) f^2 - 1 = 2^f - 1      <=>  f^2 = 2^f
             (b) 2 * f^2 = 2 * 2^f      <=>  f^2 = 2^f
             (c) 2 * 2^(f-1) = 2^f      （对 f >= 1 恒真）
   命题 B：在 f >= 3 上三者都只在 f = 4 成立
   命题 C：k_max 的平方形式（实数 f^2/2）与指数形式 2^(f-1) 只在 f = 4 同值
"""
F_MAX = 400

def sq(f): return f * f
def pw(f): return 1 << f

print("== A. 归约等价性（f = 1..%d）==" % F_MAX)
bad_a = [f for f in range(1, F_MAX + 1) if (sq(f) - 1 == pw(f) - 1) != (sq(f) == pw(f))]
bad_b = [f for f in range(1, F_MAX + 1) if (2 * sq(f) == 2 * pw(f)) != (sq(f) == pw(f))]
bad_c = [f for f in range(1, 200) if 2 * (1 << (f - 1)) != (1 << f)]
print("A_REDUCE_FAILS", bad_a)
print("B_REDUCE_FAILS", bad_b)
print("C_IDENTITY_FAILS", bad_c)
print("A_HOLDS", bad_a == [])
print("B_HOLDS", bad_b == [])
print("C_HOLDS", bad_c == [])

print("== B. 三形式同值点（f = 3..%d）==" % F_MAX)
set_a = [f for f in range(3, F_MAX + 1) if sq(f) - 1 == pw(f) - 1]
set_b = [f for f in range(3, F_MAX + 1) if 2 * sq(f) == 2 * pw(f)]
set_self = [f for f in range(3, F_MAX + 1) if sq(f) == pw(f)]
print("SET_SUB1", set_a)
print("SET_HALF", set_b)
print("SET_SELFREF", set_self)
print("ALL_SAME_SET", set_a == set_b == set_self == [4])

print("== C. k_max 双形式（实数，避免 Nat 截断）==")
from fractions import Fraction
km_sq = lambda f: Fraction(sq(f), 2)
km_exp = lambda f: Fraction(1 << (f - 1), 1)
coins = [f for f in range(3, 61) if km_sq(f) == km_exp(f)]
print("KMAX_COINCIDE", coins)
print("KMAX_ONLY_FOUR", coins == [4])
for f in (3, 4, 5, 6):
    print("F %d  KMAX_SQ %s  KMAX_EXP %s  EQ %s"
          % (f, km_sq(f), km_exp(f), km_sq(f) == km_exp(f)))

print("== D. 三常数在 f=4 的双表示 ==")
print("TOTAL16", "f^2=", sq(4), "2^f=", pw(4))
print("KMAX8", "f^2/2=", km_sq(4), "2^(f-1)=", km_exp(4))
print("SIGMA15", "f^2-1=", sq(4) - 1, "2^f-1=", pw(4) - 1)

print("VERDICT_A", bad_a == [] and bad_b == [] and bad_c == [])
print("VERDICT_B", set_a == set_b == set_self == [4])
print("VERDICT_C", coins == [4])
print("VERDICT_ALL_OK", bad_a == [] and bad_b == [] and bad_c == []
      and set_a == set_b == set_self == [4] and coins == [4])
