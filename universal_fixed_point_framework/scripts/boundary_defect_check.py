import math
from math import log
v = 4 * math.log(15)
print('4*ln15 =', repr(v))
print('integer?', float(v).is_integer())
print('ln15 =', repr(math.log(15)))
# 对照：解集两成员在离散侧的实现（数值已由 verify_reverse_translation PASS）
print('orbitCount(univ)=15, orbitCount(univ-{14})=15')
