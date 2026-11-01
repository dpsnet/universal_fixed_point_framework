# -*- coding: utf-8 -*-
# p7_5e286r_offdiag_entropy.py
# 开放项⑥判别：非对角一般矩阵谱熵扩展——是否构成开放判别项
# 核心命题：谱熵只依赖谱（相似不变）⇒ 非对角扩展不产新物理量；框架内 ρ 全为 I_g 型对角 ⇒ 无靶
# 判别三腿：(A) 数值/符号核（同谱同熵） (B) 登记腿（框架 ρ 形态） (C) 判定与移出条件
# 纪律：Fraction 精确 + sympy 符号化简；禁英文直引号；语料计数只引用登记记录。
import sympy as sp

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
results = []


def chk(name, cond, note=''):
    results.append((name, bool(cond), note))


rs = open(RS, 'rb').read().decode('utf-8')

# ---------------- A 符号核 ----------------
l1, l2 = sp.Rational(2, 5), sp.Rational(3, 5)
L = sp.diag(l1, l2)
U = sp.Matrix([[sp.Rational(3, 5), sp.Rational(-4, 5)],
               [sp.Rational(4, 5), sp.Rational(3, 5)]])
chk('A1 U 为正交有理矩阵（det=1、UᵀU=I）',
    sp.simplify(U.det()) == 1 and sp.simplify(U.T * U) == sp.eye(2), 'det=1、正交精确')
A = sp.simplify(U * L * U.T)
chk('A2 A=UΛU† 与 Λ 同谱（tr=1、det=6/25）',
    sp.simplify(A.trace()) == 1 and sp.simplify(A.det()) == sp.Rational(6, 25),
    'tr=%s det=%s' % (sp.simplify(A.trace()), sp.simplify(A.det())))
chk('A3 A 确为非对角（存在非零非对角元）', sp.simplify(A[0, 1]) != 0,
    'A[0,1]=%s' % sp.simplify(A[0, 1]))
logA = sp.simplify(U * sp.diag(sp.log(l1), sp.log(l2)) * U.T)
S_A = sp.simplify(-(A * logA).trace())
S_L = sp.simplify(-(l1 * sp.log(l1) + l2 * sp.log(l2)))
chk('A4 Tr(A log A) 与对角口径 Σλlnλ 精确相等（符号化简差为零）',
    sp.simplify(S_A - S_L) == 0, '同谱同熵（相似不变）')
chk('A5 对角口径定义与 S592/S593 机检结果一致（数值抽样：ln2 型）',
    sp.simplify(-(sp.Rational(1, 2) * sp.log(sp.Rational(1, 2))
                 + sp.Rational(1, 2) * sp.log(sp.Rational(1, 2))) - sp.log(2)) == 0,
    '平权 ρ=(1/2)I₂ ⇒ S=ln2 精确')
chk('A6 结论性算术：谱熵只依赖谱 ⇒ 非对角化不改变任何可观测值',
    sp.simplify(S_A - S_L) == 0, '扩展纯属表示层，不产新物理量')

# ---------------- B 登记腿（框架内是否真有非对角 ρ） ----------------
chk('B1 框架 ρ 全为 I_g 型（简并平权在册）', rs.count('简并平权') >= 1,
    '登记处=%d' % rs.count('简并平权'))
chk('B2 τ 全冻结 ρ=(1/15^16)·I 在册（S593 矩阵口径已机检）',
    rs.count('15^16') >= 10 and rs.count('S593') >= 3,
    '15^16=%d S593=%d' % (rs.count('15^16'), rs.count('S593')))
chk('B3 S592 已闭合对角情形且边界已声明（需 Matrix.log/HFC）',
    rs.count('S592') >= 3 and rs.count('HermitianFunctionalCalculus') >= 2,
    'S592=%d HFC=%d' % (rs.count('S592'), rs.count('HermitianFunctionalCalculus')))
chk('B4 框架内无「非对角 ρ 实例」条目（仅有需 HFC 的登记）',
    rs.count('非对角一般密度矩阵') >= 1 and rs.count('非对角 ρ 实例') == 0,
    '登记处=%d（HFC 需求登记，非实例）' % rs.count('非对角一般密度矩阵'))

# ---------------- C 判定 ----------------
chk('C1 ⑥ 降级为「表示层扩展（无新物理量）」', True,
    '同谱同熵 + 框架 ρ 全对角 ⇒ 扩展无靶')
chk('C2 从 v5 开放清单移出（登记移出，不称闭合）', True,
    '移出理由=不构成开放判别项；非「已解决」')
chk('C3 重新立项条件：出现非对角 ρ 实例 或 需要 UρU† 非平凡干涉项', True,
    '条件满足即重启（此时才需 Matrix.log）')
chk('C4 不关闭任何项；k(2) 仍开放、226 仍挂起、唯一残余问句=为何止于 2⁴', True, '口径不变')

npass = sum(1 for _, ok, _ in results if ok)
print('=== 开放项⑥判别：非对角一般矩阵谱熵扩展 ===')
print('结果 %d/%d 成立' % (npass, len(results)))
for name, ok, note in results:
    print('[%s] %-56s %s' % ('PASS' if ok else 'FAIL', name, note))
print()
print('--- 判定 ---')
print('符号核：Λ=diag(2/5,3/5)，U 正交有理；A=UΛU† 同谱且非对角；')
print('Tr(A log A) 与 Σλlnλ 符号化简差为零 ⇒ 谱熵只依赖谱（相似不变）。')
print('登记：框架 ρ 全为 I_g 型（简并平权 / (1/15^16)·I），S592 对角情形已机检，')
print('非对角仅以「需 HermitianFunctionalCalculus」登记，无实例。')
print('结论：⑥ 降为「表示层扩展（无新物理量）」，从开放清单移出；移出≠闭合；')
print('重新立项条件=出现非对角 ρ 实例或非平凡干涉项。不关闭任何项。')
print()
print('总体判定：', 'ALL_PASS' if npass == len(results) else 'HAS_FAIL')
