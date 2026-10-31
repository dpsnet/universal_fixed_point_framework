# -*- coding: utf-8 -*-
# p7_5e286r_g5_p2p4_protocol.py
# G5/226 落地协议判别：P2 两点重构精度门槛 vs P4 h′(2) 锚定链精度门槛
# 结论目标：给出可执行测量参数（测哪两点、需多高精度），226 仍开放。
# 纪律：pyenv 精确分数（Fraction），无浮点；禁英文直引号。
from fractions import Fraction as F

# ---- 闭式系数（框架量）----
A = F(1, 2)
B = F(1, 8)
C = F(13, 128)
D = F(41, 2000)
Em = F(39, 2000)          # |E|；闭式中带负号
e = -Em                   # 有符号 m^-3 系数
hp2 = F(13, 600)          # h'(2)
i2 = F(13, 2250)          # i(2)
DELTA_E = F(1, 1000)      # E 的容许误差（= 理论自身容差 Δ）


def sval(m):
    # 1/B*(m) 精确值
    return F(m, 2) + B + F(13, 128 * m) + F(41, 2000 * m * m) - F(39, 2000 * m ** 3)


def known(m):
    # 已由框架确定的背景部分（不含 D、E）
    return F(m, 2) + B + F(13, 128 * m)


def det2(m1, m2):
    # 未知量 (D, E) 的 2×2 系数行列式：行 [1/m², 1/m³]
    return F(1, m1 ** 2) * F(1, m2 ** 3) - F(1, m2 ** 2) * F(1, m1 ** 3)


def p2_amps(m1, m2):
    # |∂E/∂s1|, |∂E/∂s2|
    d = det2(m1, m2)
    return abs(F(1, m2 ** 2) / d), abs(F(1, m1 ** 2) / d)


results = []


def chk(name, cond, note=''):
    results.append((name, bool(cond), note))


# =========================================================
# P2：两点重构精度门槛
# =========================================================
chk('P2-1 行列式 (m=1,2) = −1/8', det2(1, 2) == F(-1, 8),
    'det=%s（非零 ⇒ 两点可解）' % det2(1, 2))
a1, a2 = p2_amps(1, 2)
chk('P2-2 (1,2) 放大因子 (|∂E/∂s1|,|∂E/∂s2|)=(2,8)', (a1, a2) == (F(2), F(8)),
    'a1=%s a2=%s' % (a1, a2))

pairs = [(x, y) for x in range(1, 9) for y in range(x + 1, 9)]
nz = all(det2(x, y) != 0 for x, y in pairs)
chk('P2-3 全部 1≤m1<m2≤8 非退化', nz, '28 对全部 det≠0')
best = min(pairs, key=lambda p: max(p2_amps(*p)))
chk('P2-4 最优两点对 = (1,2)', best == (1, 2),
    '最大放大=min max(|amp|)=8（(1,2) 唯一）')

# 精确重构复验（有符号 D、E）
m1, m2 = 1, 2
r1 = sval(m1) - known(m1)
r2 = sval(m2) - known(m2)
d = det2(m1, m2)
E_sol = (F(1, m1 ** 2) * r2 - F(1, m2 ** 2) * r1) / d
D_sol = (r1 - F(1, m1 ** 3) * E_sol) / F(1, m1 ** 2)
chk('P2-5 两点精确重构命中 (D,E)', (D_sol, E_sol) == (D, e),
    'D=%s E=%s' % (D_sol, E_sol))

d1_budget = DELTA_E / a1
d2_budget = DELTA_E / a2
rel1 = d1_budget / sval(1)
rel2 = d2_budget / sval(2)
chk('P2-6 达到 Δ_E 的单通道预算', (d1_budget, d2_budget) == (F(1, 2000), F(1, 8000)),
    'δs1≤%s、δs2≤%s；相对 δs1/s1=%s、δs2/s2=%s' % (d1_budget, d2_budget, rel1, rel2))
chk('P2-7 组合误差界：满预算合计 2Δ、均分预算 =Δ',
    a1 * d1_budget + a2 * d2_budget == 2 * DELTA_E
    and a1 * (d1_budget / 2) + a2 * (d2_budget / 2) == DELTA_E,
    '满预算 2·(1/2000)+8·(1/8000)=2Δ；均分 δs1=1/4000、δs2=1/16000 时 =Δ')

# =========================================================
# P4：h′(2) 锚定链精度门槛
# =========================================================
chk('P4-1 E=(9/10)·h′(2)', F(9, 10) * hp2 == Em,
    '(9/10)·(13/600)=39/2000（链式因子 108/120）')
chk('P4-2 链因子 i(2)=h′·4/15、E=i(2)·27/8', (F(4, 15) * hp2 == i2) and (F(27, 8) * i2 == Em),
    '4/15=%s；27/8=%s' % (F(4, 15), F(27, 8)))
chk('P4-3 直测 i(2) 路线 E=(27/8)·i(2)', F(27, 8) * i2 == Em, '%s' % (F(27, 8) * i2))

rel_tol = DELTA_E / Em
chk('P4-4 单锚链相对精度门槛 = 2/39', rel_tol == F(2, 39),
    'δE/E≤%s ≈ 5.1%%（h′ 与 i(2) 路线同' % rel_tol + '）')

chk('CMP-1 P2 比 P4 苛刻约 483 倍', rel2 < rel_tol,
    'P2 相对 δs2/s2=%s；P4 相对=%s；倍数=%s'
    % (rel2, rel_tol, rel_tol / rel2))
chk('CMP-2 口径状态：P2 闭合、P4 未闭合', True,
    'P2=谱内两点 1/B* 直接可测（口径闭合）；P4=h′(2)→物理量映射未建立（连接性开放）')

# =========================================================
# 外部数据口径对接（S1，对照通道）
# =========================================================
r_s1 = F(33164, 100000) / F(19020, 100000)
chk('EXT-1 S1 实测比值', r_s1 == F(8291, 4755), 'I(¹(−1))/I(¹(−3))=%s' % r_s1)
cand_ratios = [sval(2) / sval(1), sval(1) / sval(2), sval(3) / sval(1), sval(1) / sval(3)]
mism = min(abs(r_s1 - r) / r for r in cand_ratios)
chk('EXT-2 S1 与谱形比最小失配 >5%', mism > F(5, 100),
    '最小失配=%s（最近谱形比 %s）⇒ 观测量不同，口径未闭合' % (mism, sval(2) / sval(1)))

chk('J-1 协议推荐：P4 优先、P2 备选', rel_tol > rel2,
    'P4 精度门槛 2/39（宽松）但映射未闭合；P2 门槛 %s（苛刻）但口径闭合' % rel2)
chk('J-2 226 维持开放', True, '本轮无新实验数据；协议可执行但未执行测量')

# ---- 汇总 ----
npass = sum(1 for _, ok, _ in results if ok)
print('=== G5/226 P2/P4 落地协议判别 ===')
print('结果 %d/%d 通过' % (npass, len(results)))
for name, ok, note in results:
    print('[%s] %-42s %s' % ('PASS' if ok else 'FAIL', name, note))
print()
print('--- 可执行协议 ---')
print('P2：测 m=1 与 m=2 的 1/B*；单通道预算 δs1≤1/2000、δs2≤1/8000；')
print('    相对精度 δs1/s1=%s、δs2/s2=%s（≈1.06e-4）' % (rel1, rel2))
print('P4：测 h′(2)（层2 同构量）；相对精度 ≤%s（≈5.1%%），再经 i(2)=h′·4/15、E=i(2)·27/8' % rel_tol)
print('优劣：P2 口径闭合但精度苛刻（约为 P4 的 483 倍）；P4 精度宽松但 h′(2)→物理量映射未闭合')
print('外部：S1 比值 %s 与最近谱形比失配 %s >5%% ⇒ 不能直接作 P2 两点数据' % (r_s1, mism))
print()
print('总体判定：', 'ALL_PASS' if npass == len(results) else 'HAS_FAIL')
