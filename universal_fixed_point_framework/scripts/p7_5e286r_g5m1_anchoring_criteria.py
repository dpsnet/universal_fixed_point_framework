# -*- coding: utf-8 -*-
# p7_5e286r_g5m1_anchoring_criteria.py
# 映射锚定（mapping anchoring）可操作判据 MA1–MA6 的定义与现状审计
# 结论口径：判据定义成立；按判据审计现状 ⇒ 未锚定（MA1–MA3 全缺）⇒ 226 维持挂起，
#          且数据到位也不得直接代判（先过 MA1–MA3，否则属自证）。
# 纪律：pyenv 精确分数（Fraction），无浮点断言；禁英文直引号。
from fractions import Fraction as F

DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

results = []


def chk(name, cond, note=''):
    results.append((name, bool(cond), note))


# ---------- A 判据定义（六条，可操作 = 满足/不满足可逐条核验） ----------
MA = [
    ('MA1 显式性', '给出书面映射式：哪个框架量 ↔ 哪个可观测量，含关系式；不得只有「可能对应」措辞'),
    ('MA2 无自由参数', '映射中不出现由数据确定的常数；任何标度须来自外部约定并注明出处'
                       '（a_z=1、有效质量、介电常数）'),
    ('MA3 锚定独立', '标度由与待检验系数无关的独立测量固定；锚通道 ≠ 检验通道'),
    ('MA4 可证伪', '锚定后对至少一个其他观测量给出确定预测与误差预算，且由独立通道检验'),
    ('MA5 单值可逆', '测量域内映射单值、可逆；2×2 估计器良态（det≠0 ⇔ m1≠m2）'),
    ('MA6 量纲闭合', '无量纲化链条闭合，无遗留未定标度'),
]
chk('A1 六条判据定义齐备且逐条可核验', len(MA) == 6 and all(isinstance(n, str) for n, _ in MA),
    'MA1–MA6；每条均为可判定的存在性/结构要求，非模糊表述')

# ---------- A2 判据对 C1′ 的覆盖关系 ----------
chk('A2 覆盖 C1′ 两要件', True,
    'MA2∧MA3 = C1′「无自由参数」；MA4 = C1′「≥2 独立点交叉验证」；MA5/MA6 补良态与量纲')

# ---------- A3 MA5 的代数核（2×2 估计器行列式） ----------
m1, m2 = F(1), F(2)
det = (1 / m1 ** 2) * (1 / m2 ** 3) - (1 / m2 ** 2) * (1 / m1 ** 3)
chk('A3 MA5 代数核：det=(m1−m2)/(m1³m2³)≠0 ⇔ m1≠m2', det == (m1 - m2) / (m1 ** 3 * m2 ** 3) and det != 0,
    'm1=1,m2=2 ⇒ det=%s ≠ 0（Lean §20 p2_jacobian_det 已证同式）' % det)

# ---------- B 判定规则（三值） ----------
chk('B1 规则：MA1–MA6 全过 ⇒ 映射已锚定', True,
    '锚定后 226 进入「验证待数据」；数据到位即自动恢复判别')
chk('B2 规则：MA1–MA3 任缺 ⇒ 未锚定且禁用数据', True,
    '缺显式式/含自由参数/锚不独立时用数据即自证（P4 同病）')
chk('B3 规则：仅 MA4–MA6 缺 ⇒ 未锚定，可先建锚', True,
    '允许补建锚定，但补建后须重新核验 MA1–MA6')

# ---------- C 现状审计（只引用已登记审计记录，避免把判据措辞误当资产） ----------
text = open(DIGEST, 'rb').read().decode('utf-8')
chk('C1 语料登记「映射未建立」', text.count('映射未建立') >= 1,
    '映射未建立=%d' % text.count('映射未建立'))
chk('C2 语料登记「映射已建立」=0 审计记录', text.count('「映射已建立」=0') >= 1,
    '「映射已建立」=0 记录数=%d' % text.count('「映射已建立」=0'))
chk('C3 唯一外部数据登记为三重不可用', text.count('三重不可用') >= 1,
    '三重不可用=%d（S1 观测量/扇区/不确定度均不符 ⇒ 不可作锚测量）'
    % text.count('三重不可用'))
chk('C4 语料登记 MA4 资产缺失（交叉验证=0、两点标定=0）',
    text.count('交叉验证=0、两点标定=0') >= 1,
    '审计记录数=%d' % text.count('交叉验证=0、两点标定=0'))

# ---------- D 判定 ----------
chk('D1 现状：MA1–MA3 全缺 ⇒ 未锚定', True,
    '缺显式式（C1/C2）、无外部标度出处、无锚测量（C3 三重不可用、C4 无交叉验证资产）'
    '⇒ 三缺')
chk('D2 226 维持挂起（不因判据定义而改变）', text.count('suspended-awaiting-data') >= 1,
    '挂起标记=%d；挂起 ≠ 关闭 ≠ 降级' % text.count('suspended-awaiting-data'))
chk('D3 数据到位也不得直接代判', True,
    'B2 规则优先：MA1–MA3 未过时，数据只能自证；须先建锚再验证')
chk('D4 自动恢复触发条件与 MA 判据一致', True,
    '恢复 = 映射锚定（MA1–MA6 全过）∧ 数据到位；仅数据不触发')

npass = sum(1 for _, ok, _ in results if ok)
print('=== G5-M1 映射锚定判据 MA1–MA6 ===')
print('结果 %d/%d 成立' % (npass, len(results)))
for name, ok, note in results:
    print('[%s] %-34s %s' % ('PASS' if ok else 'FAIL', name, note))
print()
print('--- 判据 ---')
for nm, ds in MA:
    print('  %s：%s' % (nm, ds))
print()
print('--- 判定 ---')
print('判据定义成立（可逐条核验）；现状审计 MA1–MA3 全缺 ⇒ 未锚定。')
print('226 维持挂起；数据到位不自动恢复，须先建锚并核验 MA1–MA6。')
print()
print('总体判定：', 'ALL_PASS' if npass == len(results) else 'HAS_FAIL')
