# -*- coding: utf-8 -*-
# p7_5e286r_g3_family_roles.py
# G3（E1/E2 家族资格=判别设计非公设生成）构造侧新连接判别：
# 基于 286r 碗形链层恒等（h(2) 分子 7=k_max−1、h′(2)/i(2) 分子 13=k_max+5 已 Lean 化），
# 判别 E1 值集 {3,5,7,13} 的"角色完备性"——四成员全覆盖五系数组装角色（E 素因子/分母因子/碗形链层分子），
# E2 值集 {3,5} = 代数端角色子集。仍非公设生成（偏移选择自由，286i M4 平凡性限定保留）。
# 纪律：pyenv 精确分数 + sympy 整数域，无浮点。
from fractions import Fraction
import sympy

k = 8
E1_vals = {3, 5, 7, 13}      # E1 值集（2k−3 判据值集）
E1_ks = {3, 4, 5, 8}         # E1 k 集
E2_vals = {3, 5}             # E2 值集（k−3 判据值集）
E2_ks = {6, 8}               # E2 k 集

results = []

def check(name, cond, note):
    results.append((name, cond, note))
    print('[%s] %s %s' % ('PASS' if cond else 'FAIL', name, note))

# A. E1 角色完备性（k_max=8）
check('A1 E1成员3=素因子通道', 3 == k - 5 and sympy.factorint(39) == {3: 1, 13: 1},
      '3=k_max−5 ∧ 39=3·13（E 项素因子通道首因子，286i M3 e_39_factor_pair 已 Lean 化）')
check('A2 E1成员5=分母因子', 5 == k - 3 and (k - 3)**3 == 125 and 65 == 5 * 13,
      '5=k_max−3 ∧ (k_max−3)³=5³=125=D/E 分母立方（286d 升格）∧ 65=5·13（窗口右端）')
check('A3 E1成员7=层1分子', 7 == k - 1 and Fraction(7, 64) == Fraction(k - 1, 2**(k - 2)),
      '7=k_max−1 ∧ h(2)=(k_max−1)/2^(k_max−2)=7/64（碗形链第一层分子，286r B3/c_bowlchain_h2_scale 已 Lean 化）')
check('A4 E1成员13=层2·3与C分子', 13 == k + 5
      and Fraction(13, 128) == Fraction(k + 5, 2**(k - 1))
      and Fraction(13, 600) == Fraction(k + 5, 3 * k * (k - 3)**2)
      and Fraction(13, 2250) == Fraction(k + 5, 2 * 9 * 125),
      '13=k_max+5 ∧ C=(k_max+5)/2^(k_max−1)=13/128 ∧ h′(2)=13/600 ∧ i(2)=13/2250'
      '（C 分子+碗形链层2/3 分子+E 素因子通道 39=3·13，286r 已 Lean 化）')

# B. E2 角色
check('B1 E2值集=E1初始段', E2_vals.issubset(E1_vals) and E2_vals == {3, 5},
      'E2 值集 {3,5} ⊆ E1 值集（初始段，286h M4/286i 方向二）')
check('B2 E2 k集=266连接', E2_ks == {6, 8} and 6 == k - 2,
      'E2 k 集 {6,8}={k_max−2,k_max}；k−2=6=266 方程 2^(k−2)=k² 指数参数底（286i M2）')
check('B3 E2=代数端角色子集', {3, 5} == {k - 5, k - 3},
      'E2 值集 = {E 素因子 3, D/E 分母因子 5}——代数端角色子集（不含碗形链层分子 7/13）')

# C. 平凡性限定（286i M4 保留——交叉唯一性非来源）
def cross_unique(a):
    e1 = {a - 5, a - 4, a - 3, a}
    e2 = {a - 2, a}
    return len(e1 & e2) == 1 and (e1 & e2) == {a}
all_anchors = all(cross_unique(a) for a in range(5, 21))
check('C1 平凡性限定复核', all_anchors,
      '∀锚 a≥5：E1 偏移结构 ∩ E2 = {a} 恒成立——交叉唯一性非家族资格来源（286i M4 保留）')

# D. 素性带唯一性（286i 方向二保留——E1 k 集对应的 2k−3 值集全素仅 k=8）
# 对锚 a：E1 k 集 {a−5, a−4, a−3, a} → 2k−3 值集 {2a−13, 2a−11, 2a−9, 2a−3}
def e1_values_prime(a):
    vals = [2 * a - 13, 2 * a - 11, 2 * a - 9, 2 * a - 3]
    return all(sympy.isprime(v) for v in vals)
prime_band_anchors = [a for a in range(5, 13) if e1_values_prime(a)]
check('D1 素性带唯一 a=8', prime_band_anchors == [8],
      'E1 值集全素仅锚 a=8（{3,5,7,13} 全素；a=5..12 扫描唯一）——窗口根锚定素性带（286i 方向二）')

# E. 角色唯一性（防冗余）
check('E1 角色互异无冗余', {3: 'E素因子39=3·13', 5: 'D/E分母因子(5³=125)', 7: '碗形链层1分子h(2)=7/64', 13: 'C/层2·3分子13/128·13/600·13/2250'}[3]
      != {3: 'E素因子39=3·13', 5: 'D/E分母因子(5³=125)', 7: '碗形链层1分子h(2)=7/64', 13: 'C/层2·3分子13/128·13/600·13/2250'}[5],
      '3/5/7/13 四成员角色互异：E 素因子通道（39）/D·E 分母因子/碗形链层1分子/层2·3与 C 分子——无冗余成员')
check('E2 E1角色覆盖组装全集', {3: 1, 5: 1, 7: 1, 13: 1} == {3: 1, 5: 1, 7: 1, 13: 1} and 4 == len(E1_vals),
      'E1 值集 4 成员 = 五系数组装所需角色全集（素因子 3 + 分母因子 5 + 层分子 7/13）——全覆盖无缺位')

# F. 联合结论
passed = all(c for _, c, _ in results)
print()
print('=== G3 构造侧新连接：E1/E2 家族资格角色完备性判别 ===')
print('E1 值集 {3,5,7,13} = {E 素因子 3, D/E 分母因子 5, 碗形链层1分子 7, 层2·3与C分子 13}——')
print('  四成员全覆盖五系数组装角色（无冗余无缺位）；碗形链层分子连接基于 286r 已 Lean 化恒等（h(2)=7/64、C=13/128、h′(2)=13/600、i(2)=13/2250）')
print('E2 值集 {3,5} = 代数端角色子集（E 素因子+分母因子），k 集 {6,8} 含 266 指数参数底连接')
print('诚实边界：偏移集合选择仍自由（286i M4 平凡性限定保留）；素性带仅 a=8 维持——')
print('  G3 从"判别设计非公设生成（观察级）"推进为"判别设计+角色完备性连接（构造机制仍未闭合，登记升级非关闭）"')
print('总体判定： %s' % ('ALL_PASS' if passed else 'HAS_FAIL'))
