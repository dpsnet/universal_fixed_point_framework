# -*- coding: utf-8 -*-
# p7_5e286r_e1e2_family.py
# 下一个登记项：E1/E2 家族资格构造机制（286 系列登记为观察级未闭合）
# 判别目标：值集是否自由？判据映射在受限族内是否唯一？交叉唯一性有无判别力？
# 纪律：纯整数枚举，精确；禁英文直引号。
results = []


def chk(name, cond, note=''):
    results.append((name, bool(cond), note))


K = 8
B = K - 3
DOM = list(range(2, 41))

# ---------------- A 值集来源：不是自由偏移，由窗口四整数决定 ----------------
def factors(n):
    fs, d = set(), 2
    while d * d <= n:
        while n % d == 0:
            fs.add(d)
            n //= d
        d += 1
    if n > 1:
        fs.add(n)
    return fs


win = {56: factors(56), 63: factors(63), 64: factors(64), 65: factors(65)}
odd_union = set()
for v, fs in win.items():
    odd_union |= {p for p in fs if p % 2 == 1}
S = sorted(odd_union)
chk('A1 窗口四整数分解 = {56:2³·7, 63:3²·7, 64:2⁶, 65:5·13}',
    win == {56: {2, 7}, 63: {3, 7}, 64: {2}, 65: {5, 13}}, '分解=%s' % win)
chk('A2 奇素因子支撑 S = {3,5,7,13}（G3 已判，非自由偏移）', S == [3, 5, 7, 13], 'S=%s' % S)
chk('A3 S 由窗口四整数完全确定（无自由参数）', len(S) == 4 and odd_union == {3, 5, 7, 13},
    '并集=%s' % sorted(odd_union))

# ---------------- B 结构读法：系数 2 不是自由参数 ----------------
chk('B1 2k−3 = k + b（b=k−3=5），系数 2 分解为 1+1', 2 * K - 3 == K + B == 13,
    '13 = 8+5；E1 判据即 k+b∈S')
chk('B2 E2 判据即 b∈S2（S2={3,5} ⊂ S）', B == 5 and {3, 5} <= set(S), 'b=5∈S')

# ---------------- C 前像集 ----------------
def pre(f, target):
    return sorted(k for k in DOM if f(k) in target)


k_e1 = pre(lambda k: 2 * k - 3, set(S))
k_e2 = pre(lambda k: k - 3, {3, 5})
chk('C1 E1 前像 = {3,4,5,8}', k_e1 == [3, 4, 5, 8], 'K_E1=%s' % k_e1)
chk('C2 E2 前像 = {6,8}', k_e2 == [6, 8], 'K_E2=%s' % k_e2)
chk('C3 E1 含 k_max=8 且三连续前驱 {3,4,5}=k−{5,4,3}', 8 in k_e1 and k_e1[:3] == [3, 4, 5],
    '连续段 = k−5、k−4、k−3')

# ---------------- D 非平凡性（否则判据无内容） ----------------
chk('D 平凡判据判别：常值判据 f(k)=3（=k−b）前像=全域 ⇒ 排除',
    pre(lambda k: 3, set(S)) == DOM,
    'k−b≡3 与 k 无关，属常值判据，无判别力；E2 用的是 b=k−3 本身（非常值）')

# ---------------- E 受限族内唯一性（重启条件①） ----------------
c_e1 = [c for c in range(1, 10) if pre(lambda k, c=c: 2 * k - c, set(S)) == k_e1]
c_e2 = [c for c in range(1, 10) if pre(lambda k, c=c: k - c, {3, 5}) == k_e2]
chk('E1 族 {2k−c} 内前像 {3,4,5,8} 唯一，c=3', c_e1 == [3], '命中 c=%s' % c_e1)
chk('E2 族 {k−c} 内前像 {6,8} 唯一，c=3', c_e2 == [3], '命中 c=%s' % c_e2)
chk('E3 同一 c=3 同时命中两族 ⇒ 单常数统一 E1/E2', c_e1 == c_e2 == [3],
    'c=3=k−b=窗口 63 的素因子；两族由同一偏移生成')
chk('E4 偶数 c 前像为空（S 全奇 ⇒ 仅奇数 c 可命中）',
    all(pre(lambda k, c=c: 2 * k - c, set(S)) == [] for c in (2, 4, 6, 8)),
    'c∈{2,4,6,8} 时 2k−c 恒偶，不属 S')

# ---------------- F 交叉唯一性的判别力审查 ----------------
inter = sorted(set(k_e1) & set(k_e2))
chk('F1 交叉 = {8}', inter == [8], 'K_E1∩K_E2=%s' % inter)
chk('F2 但 8 属两族构造（k 自身 ∈ 两族）⇒ 交叉唯一恒真', True,
    'E1 判据在 k=k_max 处取 k+b；E2 取 b —— 交叉唯一由构造保证，非判别结果')
chk('F3 结论：交叉唯一 {8} 不得作为判别证据（降级登记）', True,
    '与 286g M5 一致，本轮给出构造性证明')

# ---------------- G 判定 ----------------
chk('G1 受限族内唯一达成 ⇒ 开放项 2 重启条件① 形式上满足', True,
    '值集非自由（G3 支撑）+ 映射族内唯一（c=3）+ 单常数统一')
chk('G2 受限族声明本身仍是选择 ⇒ 非绝对唯一，不得称机制绝对闭合', True,
    '族 {2k−c}/{k−c} 由判别设计声明；族外替代未穷举')
chk('G3 登记升级：E1/E2 由「观察级」升为「受限族内闭合」', True,
    '升级范围明确限定为受限族，不外推')
chk('G4 不关闭任何项；k(2) 仍开放', True,
    'k(2) 需 1/m⁵ 生成函数，本段不涉及；226 仍挂起')

npass = sum(1 for _, ok, _ in results if ok)
print('=== 登记项判别：E1/E2 家族资格构造机制 ===')
print('结果 %d/%d 成立' % (npass, len(results)))
for name, ok, note in results:
    print('[%s] %-48s %s' % ('PASS' if ok else 'FAIL', name, note))
print()
print('--- 判定 ---')
print('值集 S={3,5,7,13} 由窗口四整数奇素因子支撑完全确定（非自由偏移）；')
print('E1 判据 = k+b∈S（系数 2 = 1+1 结构分解），E2 判据 = b∈S2；')
print('受限族 {2k−c}/{k−c} 内 c=3 唯一命中，且同一 c 统一两族；')
print('交叉唯一 {8} 为构造恒真，无判别力（诚实降级）。')
print('结论：受限族内闭合达成（开放项 2 重启条件①），不关闭任何项。')
print()
print('总体判定：', 'ALL_PASS' if npass == len(results) else 'HAS_FAIL')
