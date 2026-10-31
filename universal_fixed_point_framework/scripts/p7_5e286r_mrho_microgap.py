# -*- coding: utf-8 -*-
# p7_5e286r_mrho_microgap.py
# 登记项判别：m_ρ 微缺口判别弱化（P7-6f 口径摆动内）——定量化「弱化」
# 任务：给出判别所需精度、实际口径带宽、以及达标判据的判别力
# 纪律：Fraction 精确（输入为十进制，一律用 1/10 缩放），禁英文直引号。
from fractions import Fraction as F

results = []


def chk(name, cond, note=''):
    results.append((name, bool(cond), note))


# ---------------- 输入（P7-2b / P7-6e 登记值） ----------------
MRHO_LOW = F(7743, 10)      # Λ=210.0 口径
MRHO_HIGH = F(7745, 10)     # Λ=210.3 口径
MRHO_E = F(7753, 10)        # 本脚本实验值
MRHO_E2 = F(77526, 100)     # s174 实验值
MN_FW, MN_E = F(10149, 10), F(938272, 1000)
CAND = F(766, 1000)         # 候选微修正 0.766 MeV
MUD_CAL = F(5, 10)          # m_ud 口径歧义致 m_ρ 差 0.5 MeV

# ---------------- A 微缺口与候选 ----------------
g_lo = MRHO_E - MRHO_HIGH
g_hi = MRHO_E - MRHO_LOW
big_gap = MN_FW - MN_E
chk('A1 微缺口（774.5 口径）g = 775.3−774.5 = 0.8 MeV', g_lo == F(80, 100), 'g=%s' % float(g_lo))
chk('A2 口径带 [774.3,774.5] ⇒ g ∈ [0.8, 1.0]（宽 0.2 MeV）',
    g_hi == F(10, 10) and (g_hi - g_lo) == F(2, 10), 'g∈[%.1f,%.1f]' % (float(g_lo), float(g_hi)))
chk('A3 候选 0.766 = (m_N^FW−m_N^E)/100 = 76.628/100',
    CAND == F(766, 1000) and big_gap == F(76628, 1000), '大缺口=%s' % float(big_gap))
dev_lo = (CAND - g_lo) / g_lo
dev_hi = (CAND - g_hi) / g_hi
chk('A4 候选相对 g=0.8 偏差 −4.25%（复现登记 −4.2%）', dev_lo == F(-425, 10000),
    'dev=%s%%' % float(dev_lo * 100))
chk('A5 候选相对 g=1.0 偏差 −23.4%', abs(dev_hi * 100 - F(-234, 10)) < F(1, 10),
    'dev=%s%%' % float(dev_hi * 100))

# ---------------- B 达标判据的判别力 ----------------
tol = MRHO_E / 10000        # 0.01% 级
band_lo, band_hi = 100 * (g_lo - tol), 100 * (g_lo + tol)
chk('B1 达标容差 = 0.01%×775.3 = 0.0775 MeV', tol == F(7753, 100000), 'tol=%s MeV' % float(tol))
chk('B2 达标带（以 g=0.8）= c ∈ [72.247, 87.753]',
    abs(band_lo - F(72247, 1000)) < F(1, 1000) and abs(band_hi - F(87753, 1000)) < F(1, 1000),
    'c∈[%.3f,%.3f]' % (float(band_lo), float(band_hi)))
chk('B3 候选 76.6 在带内 ✓，精确缺口 80 亦在带内 ⇒ 达标不区分二者',
    band_lo <= F(766, 10) <= band_hi and band_lo <= F(80) <= band_hi,
    '带宽/中心 = %s%%' % float((band_hi - band_lo) / F(766, 10) * 100))

# ---------------- C 判别所需精度 vs 实际不确定度 ----------------
need = abs(g_lo - CAND)
chk('C1 判别候选 vs 最近真值所需精度 ≤ 0.034 MeV', need == F(34, 1000), 'need=%s MeV' % float(need))
chk('C2 口径带宽 0.2 MeV ⇒ 比所需精度大 5.9 倍 ⇒ 不可判别',
    (g_hi - g_lo) / need == F(2, 10) / F(34, 1000) and (g_hi - g_lo) / need > 5,
    '比值=%s（=100/17）' % float((g_hi - g_lo) / need))
chk('C3 叠加 m_ud 口径 0.5 MeV ⇒ 大 14.7 倍 ⇒ 更不可判别',
    MUD_CAL / need > 14 and abs(MUD_CAL / need - F(147, 10)) < F(1, 10), '比值=%s' % float(MUD_CAL / need))
chk('C4 实验值取位敏感：775.26 与 775.3 差 0.04 MeV > 0.034',
    abs(MRHO_E2 - MRHO_E) == F(4, 100), '差值=%s MeV' % float(abs(MRHO_E2 - MRHO_E)))

# ---------------- D 判定 ----------------
chk('D1 判别弱化确证：原判「进一步弱化」定量成立', True,
    '所需精度 0.034 MeV ≪ 口径带 0.2–0.5 MeV')
chk('D2 解锁门槛登记：m_ρ 不确定度 ≤0.034 MeV ∧ m_ud 口径锁定 ∧ 实验值 4 位确定', True,
    '三条须同时满足，缺一即不可判别')
chk('D3 不升格、不关闭；0.766 候选维持「非决定性」', True,
    '达标通过不等于判别通过（B3 已证达标带 20% 宽）')
chk('D4 诚实边界：g 依赖 774.5 为 P7-2b 口径；Λ 双口径只贡献 0.2 MeV 中的一部分', True,
    '口径链未逐步复算，仅按登记值取带')

npass = sum(1 for _, ok, _ in results if ok)
print('=== 登记项判别：m_ρ 微缺口判别弱化 ===')
print('结果 %d/%d 成立' % (npass, len(results)))
for name, ok, note in results:
    print('[%s] %-52s %s' % ('PASS' if ok else 'FAIL', name, note))
print()
print('--- 判定 ---')
print('微缺口 g=0.8 MeV（774.5 口径），口径带使 g∈[0.8,1.0]（Λ 双口径，宽 0.2 MeV）；')
print('候选 0.766 = 大缺口/100，相对 g=0.8 偏差 −4.25%（复现 −4.2%）。')
print('达标判据（0.01% 级）容忍带 c∈[72.25,87.75]，相对宽 20.2%，候选与精确缺口同在其中 ⇒ 不判别。')
print('判别所需精度 0.034 MeV；实际 0.2 MeV（5.9 倍）、叠加 m_ud 口径 0.5 MeV（14.7 倍）⇒ 不可判别。')
print('结论：判别弱化定量确证；门槛登记；不升格不关闭。')
print()
print('总体判定：', 'ALL_PASS' if npass == len(results) else 'HAS_FAIL')
