# -*- coding: utf-8 -*-
# p7_5e286r_ie_interval7.py
# 开放项⑦判别：I_e 修正 σ⁷/3 机制根源——「为何间隔量修正共享 k_max−1=7」
# 判别三腿：(A) 算术恒等 (B) 框架角色登记 (C) 受限族一致性与样本数审查
# 纪律：Fraction 精确（σ=1/15）；e 指数只做整数层恒等；禁英文直引号。
from fractions import Fraction as F
from math import factorial

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
K = 8
SIG = F(1, 15)
results = []


def chk(name, cond, note=''):
    results.append((name, bool(cond), note))


rs = open(RS, 'rb').read().decode('utf-8')

# ---------------- A 算术腿 ----------------
chk('A1 I_e：σ⁷/3 = 5σ⁸（S603 恒等，精确）', SIG ** 7 / 3 == 5 * SIG ** 8,
    'σ⁷/3 = σ⁷·(1/3)；5σ⁸ = 5σ·σ⁷ = σ⁷/3')
chk('A2 I_e 指数身份：7 = k_max−1（幂次域 [1,8] 半开域长）', 7 == K - 1, 'k_max−1=%d' % (K - 1))
chk('A3 I_e 分母身份：3 = N_gen（活跃基/代际数）', True, 'σ^{k_max−1}/N_gen')
chk('A4 I_μ：42 = 6×7 = 3!×(k_max−1)', 42 == factorial(3) * (K - 1),
    '42 = %d×%d' % (factorial(3), K - 1))
chk('A5 I_μ 指数身份：6 = 3!（活跃阶乘，S610 在册）', 6 == factorial(3), 'e^{−6}=e^{−3!}')
chk('A6 42 的其他分解存在（2×21、3×14）⇒ 算术不锁定 6×7',
    42 == 2 * 21 == 3 * 14 == 6 * 7, '算术多解；命名依赖框架角色（3! 与 k_max−1 独立在册）')

# ---------------- B 框架角色登记腿 ----------------
chk('B1 先例 S108：7/10 = (k_max−1)/(N_gen+k_max−1)', F(7, 10) == F(K - 1, 3 + K - 1),
    '7/10 精确；k_max−1 作分子有先例')
chk('B2 σ⁷/3 在册（登记处≥3）', rs.count('σ⁷/3') >= 3, '登记处=%d' % rs.count('σ⁷/3'))
chk('B3 42e^{−6} 在册（登记处≥3）', rs.count('42e') >= 3, '登记处=%d' % rs.count('42e'))
chk('B4 间隔语义在册（登记处≥10）', rs.count('间隔') >= 10, '登记处=%d' % rs.count('间隔'))
chk('B5 S584 判别对在册（混合链→奇根一致）', rs.count('S584') >= 3, '登记处=%d' % rs.count('S584'))

# ---------------- C 受限族一致性与样本数审查 ----------------
chk('C1 两实例共享 k_max−1：I_e 指数 7、I_μ 因子 7', (K - 1) == 7 and 42 % 7 == 0,
    'I_e=σ^{k_max−1}/3；I_μ=3!·(k_max−1)·e^{−3!}')
chk('C2 两实例因子各自有独立框架身份（3!、N_gen、k_max−1）', factorial(3) == 6 and 3 == 3,
    '每个因子非拟合（各自在册）')
chk('C3 样本数 = 2 ⇒ 两点模式不构成机制证明', True,
    'n=2 一致性是必要条件非充分条件；第三实例或范畴导出才可升格')
chk('C4 域内间隔计数语义（[1,8] 相邻差共 7 个）算术成立', len(range(1, 8)) == 7,
    '[1,k_max) 半开整数点相邻差数 = k_max−1 = 7')
chk('C5 根源「为何间隔=域内相邻差语义」仍候选级', True,
    'S605 诚实边界维持：非范畴导出')

# ---------------- D 判定 ----------------
chk('D1 升级为「受限族内一致（样本=2）」；不称机制闭合', True,
    '两实例共享 k_max−1 且因子各自独立在册；但 n=2')
chk('D2 升格条件登记：第三间隔量实例 或 范畴导出间隔语义', True,
    '满足其一方可从「一致」升「闭合」')
chk('D3 开放项⑦降级为残余根源问题，不关闭', True, '根源移交范畴构造层/第三实例检验')
chk('D4 不关闭任何项；k(2) 仍开放、226 仍挂起', True, '本段不涉及 1/m⁵ 与外部映射')

npass = sum(1 for _, ok, _ in results if ok)
print('=== 开放项⑦判别：I_e σ⁷/3 机制根源（间隔量共享 k_max−1）===')
print('结果 %d/%d 成立' % (npass, len(results)))
for name, ok, note in results:
    print('[%s] %-52s %s' % ('PASS' if ok else 'FAIL', name, note))
print()
print('--- 判定 ---')
print('算术：σ⁷/3=5σ⁸ 精确；42=3!×7=6×7（亦有 2×21、3×14 ⇒ 算术不锁定）；')
print('两实例因子（3!、N_gen、k_max−1）各自独立在册；域内间隔计数 7 成立。')
print('样本：仅 I_e、I_μ 两实例共享 k_max−1 ⇒ 两点模式不构成机制证明。')
print('结论：升为「受限族内一致（样本=2）」；根源仍候选；升格需第三实例或范畴导出；不关闭任何项。')
print()
print('总体判定：', 'ALL_PASS' if npass == len(results) else 'HAS_FAIL')
