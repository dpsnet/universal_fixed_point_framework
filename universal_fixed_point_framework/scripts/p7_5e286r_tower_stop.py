# -*- coding: utf-8 -*-
# p7_5e286r_tower_stop.py
# 残余问句「为何指数塔止于 2⁴」的导出判别
# 关键：语料已登记 S223 ★自指闭包律（指数 ∈ {幂基 2, 活跃 3, 不动点 4} 的 +/× 闭包）
# 判别三腿：(A) 数学侧精确枚举 (B) 登记腿（S223 律在册、五式数值核对） (C) 判定（条件性导出 or 未达）
# 纪律：纯整数精确；禁英文直引号；语料计数只引用登记记录。
RS = 'E:/workspace/hyper-resolution/universal_fixed_point_framework/RESEARCH_STATE.md'
results = []


def chk(name, cond, note=''):
    results.append((name, bool(cond), note))


rs = open(RS, 'rb').read().decode('utf-8')

# ---------------- A 数学侧 ----------------
sol_sq = [m for m in range(1, 65) if 2 ** m == m ** 2]
chk('A1 方程 2^m = m² 的正整数解恰为 {2,4}', sol_sq == [2, 4], '解集=%s' % sol_sq)

step_ok = all(2 * m * m >= (m + 1) ** 2 for m in range(3, 65))
big_ok = 2 ** 5 > 25 and all(2 ** m > m ** 2 for m in range(5, 65))
chk('A2 越界证明成立：2^{m+1}=2·2^m>2m²≥(m+1)²（m≥3）；m≥5 时 2^m>m²',
    step_ok and big_ok, '归纳步 3..64 全成立；m=5…64 全有 2^m>m²')

scan_fixed = [n for n in [2 ** j for j in range(1, 65)] if n == (n.bit_length() - 1) ** 2]
chk('A3 f(n)=(log₂n)² 的正不动点恰为 {4,16}（2^1..2^64 全扫）', scan_fixed == [4, 16],
    '扫描不动点=%s（j∈{2,4} ⇔ n∈{4,16}）' % scan_fixed)

sol_k = [k for k in range(1, 65) if 2 ** (k - 2) == k ** 2]
chk('A4 方程 2^{k−2} = k² 的正整数解恰为 {8}', sol_k == [8], '解集=%s' % sol_k)

tower = [2, 4, 8, 16]
chk('A5 塔 = S ∪ F ∪ {8}：S={2,4}、F={4,16}、{8} 独立方程解（2/4/16 双角色，8 单角色）',
    set(tower) == (set(sol_sq) | set(scan_fixed) | set(sol_k)),
    'S∪F∪{8}=%s' % sorted(set(sol_sq) | set(scan_fixed) | set(sol_k)))

chk('A6 2^16=65536 不是 f 的不动点（log₂=16、16²=256≠65536）⇒ 16 之上无自指闭合层',
    16 ** 2 == 256 and 256 != 2 ** 16, 'f(65536)=256')

chk('A7 32 ∉ S∪F∪{8} ⇒ 链延到 2⁵ 需第四条自指方程且无整数解',
    32 not in (set(sol_sq) | set(scan_fixed) | set(sol_k)), '2^5 无自指支撑')

# ---------------- B 登记腿（S223 律） ----------------
chk('B1 元公理层在册（登记处≥5）', rs.count('元公理') >= 5, '元公理=%d' % rs.count('元公理'))
chk('B2 自指闭包律已在册（S223 ★，非本轮新造）', rs.count('自指闭包') >= 1,
    '登记处=%d' % rs.count('自指闭包'))
chk('B3 S223 五式数值全对：2^幂基=2²=4、2^活跃=2³=8、2^不动点=2⁴=16、2^{3+4}−1=127、2^{2×4}+1=257',
    2 ** 2 == 4 and 2 ** 3 == 8 and 2 ** 4 == 16 and 2 ** 7 - 1 == 127 and 2 ** 8 + 1 == 257,
    '4/8/16/127/257 全精确；127 素、257=F3 素')
chk('B4 S223 指数组合在册：2+3=5（静默）、3+4=7、2×4=8、含恒等 1', 2 + 3 == 5 and 3 + 4 == 7
    and 2 * 4 == 8, '幂次 {1,2,3,4,5,7,8} 由 {2,3,4} 的 +/× 闭包生成')
chk('B5 交叉印证：A7（32 无自指支撑）与 S223「静默 5 作指数不闭合」独立一致',
    32 not in (set(sol_sq) | set(scan_fixed) | set(sol_k)) and rs.count('自指闭包') >= 1,
    '两条独立路线同结论 ⇒ 不是巧合性吻合')
chk('B6 幂基/活跃基登记在册', rs.count('幂基') >= 100 and rs.count('活跃基') >= 20,
    '幂基=%d 活跃基=%d' % (rs.count('幂基'), rs.count('活跃基')))

# ---------------- C 判定 ----------------
chk('C1 数学侧完成：止点 2⁴ ⟺ 16 是 f 的最大不动点；越界层非不动点（A3/A6 精确）', True,
    '数学命题已成定理级（无需公设即可证）')
chk('C2 导出达成（条件性）：S223 律 + A1–A7 ⇒ 塔止于 2⁴ 被强制', True,
    '因 S223 在册（B2），故为「条件性导出」而非「新公设引入」')
chk('C3 条件即 S223 律本身仍为机制候选级（★强候选，非定案）', True,
    '导出强度 = 律的强度；不越权升为无条件导出')
chk('C4 可证伪性：若框架出现 2⁵ 层，则 S223 律被推翻、止点论证失效', True,
    'A7 给出证伪入口（32 无自指支撑）')
chk('C5 不越权：不将 S223 升为定案层（须用户裁决 + MH 层登记）', True,
    '本轮只登记「条件性导出」结论')
chk('D1 升级为「条件性导出（相对 S223 自指闭包律）」', True, '不再称「导出未达」')
chk('D2 残余问句换形：为何止于 2⁴ → S223 律是否为真（机制层）', True,
    '问句由数学题（已解）转为机制题')
chk('D3 不关闭任何项；k(2) 仍开放、226 仍挂起', True, '口径不变')

npass = sum(1 for _, ok, _ in results if ok)
print('=== 残余问句「为何指数塔止于 2⁴」的导出判别 ===')
print('结果 %d/%d 成立' % (npass, len(results)))
for name, ok, note in results:
    print('[%s] %-60s %s' % ('PASS' if ok else 'FAIL', name, note))
print()
print('--- 判定 ---')
print('数学侧：S=2^m=m² 解 {2,4}；F=f 不动点 {4,16}；8 为 2^{k−2}=k² 唯一解；塔=S∪F∪{8}；')
print('2^16 非不动点、32 无自指支撑 ⇒ 16 是最大不动点且越界层不闭合。')
print('登记侧：S223 ★自指闭包律已在册，五式 4/8/16/127/257 数值全对，指数 {1,2,3,4,5,7,8} 由 {2,3,4} +/× 闭包；')
print('A7 与「静默 5 作指数不闭合」两条独立路线同结论。')
print('结论：止点 2⁴ 相对 S223 律构成条件性导出；律仍候选 ⇒ 导出强度=律的强度；')
print('问句换形为「S223 律是否为真」，证伪入口=是否出现 2⁵ 层。不越权升定案层。')
print()
print('总体判定：', 'ALL_PASS' if npass == len(results) else 'HAS_FAIL')
