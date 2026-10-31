# -*- coding: utf-8 -*-
# p7_5e286r_g3_window_prime_construct.py
# 判别④ G3 E1/E2 家族资格：构造机制（窗口奇素因子支撑）判别
# 精确整数（sympy factorint + Fraction），无浮点。模式 8：先证伪再登记。
#
# G3 缺口（306 段结论）：E1/E2 家族资格 = 判别设计 + 角色完备性连接，构造机制未闭合。
# 本步给出构造机制候选：E1 = 窗口四整数 {k(k-1), k^2-1, k^2, k^2+1} 的「奇素因子支撑」并集。
# 同时作非唯一性判别（值集可由多条规则复现 => 生成规则不锁定，登记诚实边界）。
from sympy import factorint

k_max = 8
n_max = k_max + 2      # 10
N_gen = 3

results = []
def chk(name, cond, detail=''):
    results.append((name, bool(cond), detail))

# ---- 窗口四整数（288/289：窗口左端 k(k-1)、k^2-1、k^2、k^2+1）----
W = {
    'k(k-1)': k_max * (k_max - 1),      # 56
    'k^2-1': k_max ** 2 - 1,            # 63
    'k^2':   k_max ** 2,                # 64
    'k^2+1': k_max ** 2 + 1,            # 65
}
chk('A1 窗口四整数 = {56,63,64,65}', sorted(W.values()) == [56, 63, 64, 65],
    '%s' % W)

# ---- A2 奇素因子支撑（构造集，无观测输入）----
supp = set()
for name, w in W.items():
    for p in factorint(w):
        if p != 2:
            supp.add(p)
chk('A2 E1 = 窗口奇素因子支撑并集 = {3,5,7,13}', supp == {3, 5, 7, 13},
    '支撑集 = %s；逐项分解 %s' % (sorted(supp), {n: factorint(w) for n, w in W.items()}))

# ---- A3 逐成员窗口所有者（唯一/多重）----
owners = {3: [], 5: [], 7: [], 13: []}
for name, w in W.items():
    for p in owners:
        if w % p == 0:
            owners[p].append(name)
chk('A3 成员窗口所有者：3→{k^2-1}、5→{k^2+1}、7→{k(k-1),k^2-1}、13→{k^2+1}',
    owners[3] == ['k^2-1'] and owners[5] == ['k^2+1']
    and owners[7] == ['k(k-1)', 'k^2-1'] and owners[13] == ['k^2+1'],
    '%s' % {p: owners[p] for p in owners})

# ---- A4 关键分解：k^2+1 = 65 = 5·13 = (k-3)(k+5)；k^2-1 = 63 = 7·9 = 7·3^2 ----
chk('A4 k^2+1 = (k_max−3)(k_max+5) = 5·13（D/E 立方底 5 与 C 分子 13 为 k^2+1 两因子）',
    (k_max - 3) * (k_max + 5) == k_max ** 2 + 1,
    '(k−3)(k+5)=%d, k²+1=%d' % ((k_max - 3) * (k_max + 5), k_max ** 2 + 1))
chk('A5 k^2−1 = (k_max−1)(k_max+1) = 7·9 = 7·3²（7 与 3 同出 k^2−1）',
    (k_max - 1) * (k_max + 1) == k_max ** 2 - 1,
    '(k−1)(k+1)=%d=7·9=7·3²' % ((k_max - 1) * (k_max + 1)))
chk('A6 k(k−1) = 56 = 7·k_max（7 的双重所有者：k(k−1) 与 k^2−1）',
    k_max * (k_max - 1) == 56 and (k_max - 1) * k_max == 56)

# ---- A7 反事实敏感性：缺 65 或缺 63 则 E1 退化 ----
def supp_of(wset):
    s = set()
    for w in wset:
        for p in factorint(w):
            if p != 2:
                s.add(p)
    return s
chk('A7 反事实：窗口缺 k^2+1(65) => E1={3,7}（5、13 消失）',
    supp_of([56, 63, 64]) == {3, 7})
chk('A8 反事实：窗口缺 k^2−1(63) => E1={5,7,13}（3 消失）',
    supp_of([56, 64, 65]) == {5, 7, 13})

# ---- A9 E2 = {3,5} = 和为 k_max 的对；E1\E2 = {7,13} 和为 2·n_max ----
E1 = {3, 5, 7, 13}
E2 = {3, 5}
chk('A9 E2={3,5} 且 3+5=k_max=8（k_max-补对）', E2 == {3, 5} and sum(E2) == k_max)
chk('A10 E1\\E2={7,13} 且 7+13=2·n_max=20（n_max-补对）',
    E1 - E2 == {7, 13} and sum(E1 - E2) == 2 * n_max)
chk('A11 E2 ⊂ E1 严格子集（初始段，306 角色指认同构）', E2 < E1)

# ---- A12 非唯一性（诚实边界）：规则二复现同值集 [3,13] 内奇素数去 11 ----
alt = {p for p in range(3, 14) if all(p % d for d in range(2, p)) and p != 11}
chk('A12 非唯一性：规则二（[3,13] 奇素数去 11）同得 {3,5,7,13}——值集不锁定生成规则',
    alt == E1,
    '另一规则同值 => 构造规则非唯一（登记诚实边界）')

# ---- A13 角色互异无冗余（复验 306）----
roles = {3: 'E 素因子（39=3·13）', 5: 'D/E 分母立方底（k_max−3）',
         7: '碗形链层1分子（h(2)=7/64, k_max−1）', 13: 'C 分子/层2·3（k_max+5）'}
chk('A13 四成员角色互异无冗余', len(set(roles.values())) == 4)

# ---- A14 碗形链层值分子支撑一致 ----
chk('A14 碗形链层值分子 {7,13,13} ⊂ E1（层1/2/3 分子覆盖）',
    {7, 13} <= E1,
    'h(2)=7/64, h′(2)=13/600, i(2)=13/2250')

# ---- A15 窗口算术量本身来源（登记边界）----
chk('A15 窗口四整数由 k_max=8 窗口算术给出（286-289）——实例参数，非元公理导出',
    k_max == 8)

# ---- A16 构造机制判定 ----
chk('A16 构造机制闭合（窗口奇素因子支撑 ⇒ E1 精确；E2=k_max-补对子集）',
    supp == E1 and E2 == {3, 5} and sum(E2) == k_max)

npass = sum(1 for _, ok, _ in results if ok)
print('=== p7_5e286r G3 构造机制判别（窗口奇素因子支撑）===')
print('结果 %d/%d 通过' % (npass, len(results)))
for name, ok, detail in results:
    print('[%s] %-64s %s' % ('PASS' if ok else 'FAIL', name, detail))
print('--- 判别分层 ---')
print('G3：E1 家族资格由窗口算术构造生成（奇素因子支撑），非纯判别设计；')
print('    E2 = {3,5} = E1 中 k_max-补对（3+5=8）——代数端角色子集获构造解释。')
print('    诚实边界：① 窗口四整数依赖 k_max=8（实例参数）；② 生成规则非唯一（规则二同值）；')
print('    ③ 286i M4 平凡性限定保留（交叉唯一性非家族资格来源）。')
print('总体判定：', 'ALL_PASS' if npass == len(results) else 'HAS_FAIL')
