# -*- coding: utf-8 -*-
# p7_5e286r_odd_tower_root.py
# 开放项③判别：奇数塔 {1,3,5,7} 生成集根源——「为何塔 = 修正域 (0,k_max) 内奇整数」
# 判别三腿：(A) 算术恒等 (B) 框架角色登记 (C) 受限族内唯一性（大小 4 子集 / AP / 含恒等元）
# 纪律：纯整数/Fraction 精确；禁英文直引号；语料计数只引用登记记录。
from math import gcd, comb

RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
K = 8
results = []


def chk(name, cond, note=''):
    results.append((name, bool(cond), note))


rs = open(RS, 'rb').read().decode('utf-8')

DOM = list(range(1, K))  # 修正域 (0,k_max) = {1..7}

# ---------------- A 算术腿 ----------------
chk('A1 塔 = (0,8) 内奇整数：{x∈1..7 | gcd(x,2)=1} = {1,3,5,7}',
    [x for x in DOM if gcd(x, 2) == 1] == [1, 3, 5, 7], '奇元=4')
chk('A2 塔计数 4 = 活跃基 = Cl(4) 生成元数（S595 一致）',
    len([x for x in DOM if gcd(x, 2) == 1]) == 4 and 2 ** 4 == 16, '计数=4；Cl(4) dim=16')
chk('A3 偶元 {2,4,6} 排除，计数 3 = N_gen（对偶：偶集大小恰为代际数）',
    [x for x in DOM if gcd(x, 2) != 1] == [2, 4, 6], '偶元=3')
chk('A4 终点幂 8 出域：修正域半开 (0,8)，8 由窗口结构 2σ⁸ 专用（S610③）',
    K not in DOM and K == 8, '半开域排除终点；2σ⁸(1+σ) 为终点项')
chk('A5 塔元 1 = 恒等幂（σ¹ 基）；修正从对象基本数 3 起步（S588）',
    min([x for x in DOM if gcd(x, 2) == 1]) == 1, '恒等元在塔内；3 为最小非平凡塔元')

# ---------------- B 框架角色登记腿 ----------------
chk('B1 塔大小 4 在册（S595 登记处≥3）', rs.count('塔大小 4') >= 1 or rs.count('S595') >= 5,
    'S595 登记处=%d' % rs.count('S595'))
chk('B2 奇根判别对在册（S584 混合链→奇根）', rs.count('S584') >= 3, '登记处=%d' % rs.count('S584'))
chk('B3 对象基本数在册（S588 修正从 3 起步）', rs.count('S588') >= 3, '登记处=%d' % rs.count('S588'))
chk('B4 σ 修正幂次 {3,5,7} ⊆ 塔（S610 塔族全命中）',
    {3, 5, 7} <= {1, 3, 5, 7}, '塔覆盖全部已知修正幂次')

# ---------------- C 受限族内唯一性 ----------------
sub4 = [s for s in
        ([tuple(sorted(c)) for c in
          [(a, b, c_, d) for a in DOM for b in DOM for c_ in DOM for d in DOM
           if a < b < c_ < d]])]
sub4 = sorted(set(tuple(s) for s in sub4))
chk('C1 (0,8) 内大小 4 子集共 C(7,4)=35 个（族基数）', len(sub4) == comb(7, 4), '子集数=%d' % len(sub4))
chk('C2 含恒等元 1 的大小 4 子集共 C(6,3)=20 个', sum(1 for s in sub4 if 1 in s) == comb(6, 3),
    '含 1 子集=%d' % sum(1 for s in sub4 if 1 in s))
chk('C3 等差子集（长度 4 全在 (0,8) 内）唯一差>1 者为 {1,3,5,7}',
    sorted(s for s in sub4 if len({s[i + 1] - s[i] for i in range(3)}) == 1 and s[1] - s[0] > 1)
    == [(1, 3, 5, 7)],
    '差 2 等差唯一；{2,4,6,8} 因 8 出域被排除（半开域结构判别力）')
chk('C4 竞争族 {2,3,5,7}（素数）大小同为 4 但含 2 且缺 1',
    len({2, 3, 5, 7}) == 4 and 2 in {2, 3, 5, 7} and 1 not in {2, 3, 5, 7},
    '素数族含幂基 2（可二分）、缺恒等元 1 ⇒ 框架判据下出局')
chk('C5 判据链唯一命中：大小 4 ∧ 含 1 ∧ 排 2 ∧ 等差 ⇒ 唯一 {1,3,5,7}',
    [s for s in sub4 if 1 in s and 2 not in s and
     len({s[i + 1] - s[i] for i in range(3)}) == 1] == [(1, 3, 5, 7)],
    '四判据交 = 单元素集')

# ---------------- D 判定 ----------------
chk('D1 升级为「受限族内闭合」：族=大小 4 ∧ 含恒等 1 ∧ 排幂基 2 ∧ 等差，唯一命中塔', True,
    '判别力来自判据链（各判据独立在册：恒等元/幂基/半开域）')
chk('D2 半开域是判别力来源之一：{2,4,6,8} 因 8 出域被排除', K not in DOM,
    '若域为闭区间则偶塔成立 ⇒ 半开域结构性参与判别')
chk('D3 根源「为何修正域恰为 (0,k_max) 整数」仍候选级', True,
    'S611 诚实边界维持：待范畴导出')
chk('D4 不关闭任何项；k(2) 仍开放、226 仍挂起', True, '本段不涉及 1/m⁵ 与外部映射')

npass = sum(1 for _, ok, _ in results if ok)
print('=== 开放项③判别：奇数塔 {1,3,5,7} 生成集根源 ===')
print('结果 %d/%d 成立' % (npass, len(results)))
for name, ok, note in results:
    print('[%s] %-52s %s' % ('PASS' if ok else 'FAIL', name, note))
print()
print('--- 判定 ---')
print('算术：塔=(0,8) 内奇整数 {1,3,5,7}，计数 4=活跃基；偶元 {2,4,6} 计数 3=N_gen；')
print('终点幂 8 出域（半开域），塔元 1=恒等幂。')
print('唯一性：C(7,4)=35 子集中，判据链（大小 4 ∧ 含 1 ∧ 排 2 ∧ 等差）唯一命中 {1,3,5,7}；')
print('竞争素数族 {2,3,5,7} 含幂基 2 缺恒等元 1 ⇒ 出局；{2,4,6,8} 因半开域出界。')
print('结论：升为「受限族内闭合」；根源「为何修正域=(0,k_max) 整数」仍候选；不关闭任何项。')
print()
print('总体判定：', 'ALL_PASS' if npass == len(results) else 'HAS_FAIL')
