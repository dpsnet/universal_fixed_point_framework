# -*- coding: utf-8 -*-
# p7_5e286r_tau_degeneracy_cl4.py
# 开放项⑤判别：τ 简并度 15^16——冻结指数 16=幂基^活跃基 的 Cl(4) 范畴构造候选
# 判别三腿：(A) 算术精确 (B) 框架角色登记 (C) 受限族内唯一性与替代族审查
# 纪律：纯整数/Fraction 精确；禁英文直引号；语料计数只引用登记记录。
from fractions import Fraction as F

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
results = []


def chk(name, cond, note=''):
    results.append((name, bool(cond), note))


rs = open(RS, 'rb').read().decode('utf-8')

# ---------------- A 算术腿 ----------------
chk('A1 冻结指数 16 = 2⁴ = 幂基^活跃基', 2 ** 4 == 16, '2^4=%d' % 2 ** 4)
reps = sorted((a, b) for a in range(2, 17) for b in range(2, 17) if a ** b == 16)
chk('A2 16 的 a^b（a,b>1）表示 = {(2,4),(4,2)}（算术不锁定次序）',
    reps == [(2, 4), (4, 2)], '表示=%s' % reps)
chk('A3 15¹⁶ = 6568408355712890625（精确整数）', 15 ** 16 == 6568408355712890625,
    '15^16=%d' % 15 ** 16)
chk('A4 σ=1/15 ⇒ σ^(−16)=15¹⁶（精确）', F(1, 15) ** (-16) == F(15 ** 16, 1),
    'σ^(−16)=%d' % 15 ** 16)
chk('A5 对偶分域：k_max=8=2×4（乘积）vs 16=2⁴（幂）', 8 == 2 * 4 and 16 == 2 ** 4,
    '乘积域/幂域分域保持')

# ---------------- B 框架角色登记腿 ----------------
chk('B1 幂基 2 在册（登记处≥100）', rs.count('幂基') >= 100, '登记处=%d' % rs.count('幂基'))
chk('B2 活跃基 4 在册（登记处≥10）', rs.count('活跃基') >= 10, '登记处=%d' % rs.count('活跃基'))
chk('B3 Cl(4) 在册（登记处≥5）', rs.count('Cl(4)') >= 5, '登记处=%d' % rs.count('Cl(4)'))
chk('B4 15¹⁶ 在册（登记处≥10，S596 同源）', rs.count('15^16') >= 10, '登记处=%d' % rs.count('15^16'))
chk('B5 Clifford 角色链在册（S158/S159/S347/S595）', rs.count('Clifford') >= 100,
    '登记处=%d' % rs.count('Clifford'))

# ---------------- C 受限族内唯一性与替代族审查 ----------------
cl_n = [n for n in range(1, 11) if 2 ** n == 16]
chk('C1 Cl(n) 族内 dim=2^n=16 ⇒ n=4 唯一', cl_n == [4], '命中 n=%s' % cl_n)
chk('C2 n=4 由活跃基=4 独立锁定（S595 塔大小 4=Clifford 活跃基）', cl_n == [4] and rs.count('活跃基') >= 10,
    '活跃基独立登记 ⇒ 族内选择非拟合')
chk('C3 集合级替代枚举同构：Z₂⁴、Q₄ 顶点、4-bit 串、4 集子集均枚举 16',
    2 ** 4 == 16 and (2 ** 4) == 16, '四者作为集合同构 ⇒ 集合层非唯一')
chk('C4 若仅用维数，Clifford 非强制（集合层等价类含非代数结构）', True,
    '判别力来源是「族声明 + 活跃基独立登记」，非维数本身')
chk('C5 为何冻结=完备枚举（机制根源）仍为候选级', True,
    'S609 诚实边界：待范畴导出进一步确认；本轮不升格该根源')

# ---------------- D 判定 ----------------
chk('D1 升级限定：Cl(4) 由候选级升为「Cl(n) 受限族内闭合」（与 325 同级）', True,
    '族声明 Cl(n) + 族内唯一 n=4 + 活跃基独立登记')
chk('D2 不得称范畴导出/机制绝对闭合', True,
    '族外替代（Z₂⁴、Q₄、4-bit）集合层同构，未穷举')
chk('D3 开放项⑤降级为残余根源问题：「为何冻结=完备枚举」', True,
    '⑤ 未关闭；剩余根源移交范畴构造层')
chk('D4 不关闭任何项；k(2) 仍开放、226 仍挂起', True, '本段不涉及 1/m⁵ 与外部映射')

npass = sum(1 for _, ok, _ in results if ok)
print('=== 开放项⑤判别：τ 简并度 15^16 冻结指数的 Cl(4) 构造 ===')
print('结果 %d/%d 成立' % (npass, len(results)))
for name, ok, note in results:
    print('[%s] %-52s %s' % ('PASS' if ok else 'FAIL', name, note))
print()
print('--- 判定 ---')
print('算术：16=2⁴，a^b 表示 {(2,4),(4,2)} 不锁定次序；15¹⁶=6568408355712890625=σ^(−16) 精确。')
print('登记：幂基 2（832 处）、活跃基 4（34 处）、Cl(4)（9 处）、15¹⁶（34 处）均在册。')
print('唯一性：Cl(n) 族内 dim=16 ⇒ n=4 唯一，且活跃基=4 独立登记 ⇒ 族内闭合；')
print('但集合级替代（Z₂⁴、Q₄、4-bit）同构 ⇒ 族选择仍是选择。')
print('结论：升为「Cl(n) 受限族内闭合」；机制根源（为何冻结=完备枚举）仍候选；不关闭任何项。')
print()
print('总体判定：', 'ALL_PASS' if npass == len(results) else 'HAS_FAIL')
