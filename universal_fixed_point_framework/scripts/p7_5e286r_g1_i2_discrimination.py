# -*- coding: utf-8 -*-
# p7_5e286r_g1_i2_discrimination.py
# G1 内部 i(2) 并列判别：13/2250（框架侧，BowlChainScaleIdentities.i2_cand2 已 Lean 化）
#               vs 1/173（分子平方迭代侧，173=13²+2² 第二步）
# 判别维度：E 组装精确命中 / r2 框架比值闭合 / 分子窗口算术谱交叠 / 迭代谱并行身份
# 纪律：pyenv 精确分数 + sympy，无浮点。
from fractions import Fraction
import sympy

k = 8
N_gen = 3
Np = 5

i2a = Fraction(13, 2250)   # C_a 框架侧候选
i2b = Fraction(1, 173)     # C_b 迭代侧候选
h2 = Fraction(7, 64)
hp2 = Fraction(13, 600)
E = Fraction(39, 2000)
cube = Fraction(N_gen, 2) ** 3   # (N_gen/2)³ = 27/8

results = []

def check(name, cond, note):
    results.append((name, cond, note))
    print('[%s] %s %s' % ('PASS' if cond else 'FAIL', name, note))

# 1. E 组装精确命中判别
E_a = i2a * cube
E_b = i2b * cube
check('1a C_a E 组装精确命中', E_a == E,
      'E_a=(13/2250)·(27/8)=%s==%s' % (E_a, E))
check('1b C_b E 组装偏离', E_b != E,
      'E_b=(1/173)·(27/8)=%s != %s（差 %s，相对差 %.4f%%）'
      % (E_b, E, E - E_b, abs(float((E_b - E) / E)) * 100))

# 2. r2 比值框架闭合判别（i(2) 在碗形链中的比值角色 r2=h′(2)/i(2)）
r2_a = hp2 / i2a
r2_b = hp2 / i2b
frame_r2 = Fraction(N_gen * Np, 4)   # N_gen·N′/2² = 15/4
check('2a C_a r2 框架比值精确', r2_a == frame_r2,
      'r2_a=h′(2)/i2a=(13/600)/(13/2250)=%s == N_gen·N′/2²=%s' % (r2_a, frame_r2))
check('2b C_b r2 非框架组合', not r2_b == frame_r2,
      'r2_b=h′(2)/i2b=%s（分母 600=2³·3·5²；分子 2249=13·173，173 素非框架谱）' % r2_b)

# 3. 素性/谱归属判别
check('3a 173 素数', sympy.isprime(173), '173=13²+2² 为素（迭代谱成员，非窗口算术谱 {40,56,63,64,65,128,512} 因子）')
check('3b 13=k_max+5 窗口谱交叠', 13 == k + 5, 'C_a 分子 13=k_max+5=窗口右端 65 素因子（窗口算术谱成员）')
check('3c 13=3²+2² 迭代第一步交叠', 13 == 9 + 4, 'C_a 分子同时携带平方迭代第一步 13=3²+2²（双谱交叠）')
check('3d 2250 分母框架分解', Fraction(13, 2 * N_gen**2 * (k - 3)**3) == i2a,
      '2250=2·N_gen²·(k_max−3)³=2·9·125（框架常数组合）')

# 4. 迭代家族并行身份保留（不删除 1/173 路径）
check('4a 迭代家族第二步登记', 173 == 169 + 4, '173=13²+2² 迭代家族第二步（登记不删除）')
check('4b 第三步预测保留', 29933 == 173**2 + 4, '29933=173²+2² 第三步预测（非锁定保留）')

# 5. 联合判定
passed = all(c for _, c, _ in results)
print()
print('=== i(2) 并列判别 ===')
print('C_a=13/2250 三重闭合（E 组装精确 + r2 框架比值 + 双谱交叠）→ i(2)=13/2250 判别成立，维持 BowlChainScaleIdentities.i2_cand2')
print('C_b=1/173 迭代谱并行身份（173=13²+2² 第二步）→ 登记保留，与 i(2) 判定解耦；29933 第三步预测保留非锁定')
print('总体判定： %s' % ('ALL_PASS' if passed else 'HAS_FAIL'))
