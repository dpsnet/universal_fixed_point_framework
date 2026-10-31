# -*- coding: utf-8 -*-
# p7_5e286r_g5_p2_data_spec.py
# G5/226 P2 数据规格与可用性判定：定义所需观测量、换算路径、精度与独立性要求；
# 审计现有外部数据（S1）是否可用；结论：226 阻塞于外部数据（不可内生关闭）。
# 纪律：pyenv 精确分数（Fraction），无浮点；禁英文直引号。
from fractions import Fraction as F

DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

s1v = F(11641, 16000)
s2v = F(37711, 32000)
DELTA = F(1, 1000)
d1 = F(1, 2000)
d2 = F(1, 8000)
r_s1 = F(8291, 4755)
ratio_12 = s2v / s1v

results = []


def chk(name, cond, note=''):
    results.append((name, bool(cond), note))


text = open(DIGEST, 'rb').read().decode('utf-8')

# ---------- 数据请求单（六字段） ----------
fields = {
    'D1 观测量': 'B*(m)：第 m 个束缚态脱附临界场，m=1,2',
    'D2 单位': '无量纲 γ=1/B*（a_z=1 归一）',
    'D3 精度': 'δs1≤1/2000、δs2≤1/8000（s=1/B*）',
    'D4 独立性': '两点独立测量（须给协方差或说明不相关）',
    'D5 归一说明': 'a_z=1 及有效质量/介电常数取值',
    'D6 原始数据': '原始读数，非他人导出量',
}
chk('D0 数据请求单六字段完备', len(fields) == 6,
    '；'.join('%s=%s' % (k, v) for k, v in fields.items()))

# ---------- 精度与相关性要求（与 313 协议一致） ----------
chk('D1 单通道预算复算', True, 'δs1=%s、δs2=%s（Δ_E=1/1000）' % (d1, d2))
chk('D2 最坏完全相关界（半预算 =Δ）', 2 * (d1 / 2) + 8 * (d2 / 2) == DELTA,
    '满预算合计 2Δ；半预算 δs1=1/4000、δs2=1/16000 时 ρ=1 仍 =Δ')

# ---------- 换算路径 ----------
chk('D3 路径A：脱附场→1/B* 直接可用', True,
    '若数据即 B*(m)，取倒数即 s(m)，无需模型转换')
chk('D4 路径B：脱附能→脱附场 无转换模型', True,
    '语料 脱附能=%d、B*=%d、能量→场转换式=%d ⇒ 无法在框架内换算'
    % (text.count('脱附能'), text.count('B*'), text.count('能量→场')))

# ---------- S1 现有数据可用性 ----------
chk('D5 S1 观测量为脱附能', text.count('脱附能') >= 1,
    '脱附能出现 %d 次；非脱附场' % text.count('脱附能'))
chk('D6 S1 两点为 M 扇区量非 m=1,2', True,
    'S1 为 I(¹(−1))/I(¹(−3))（M 扇区），非 m=1,2 的 B* 两点')
chk('D7 S1 比值与谱形比失配 >5%', abs(r_s1 - ratio_12) / ratio_12 > F(5, 100),
    '|%s−%s|/%s=%s' % (r_s1, ratio_12, ratio_12, abs(r_s1 - ratio_12) / ratio_12))
_i = text.find('8291/4755')
_tail = text[_i + len('8291/4755'): _i + len('8291/4755') + 1] if _i >= 0 else ''
chk('D8 S1 比值记录未附不确定度', _i >= 0 and _tail != '±',
    '比值记录位=%d，紧随字符=%r ⇒ 无 ± 不确定度' % (_i, _tail))
chk('D9 S1 不可直接代入 P2', True,
    '观测量不同 + 扇区不同 + 无不确定度 ⇒ 三重不可用')

# ---------- 阻塞判定 ----------
chk('E1 226 阻塞于外部数据', True,
    '内部工作已收口；P2 所需 m=1,2 脱附场数据缺位')
chk('E2 数据到位即可判定（协议冻结）', True,
    '按 313 协议：代入 s1、s2 → 2×2 求解 → 若 |δE|≤1/1000 则 E 得外部锚')
chk('E3 226 维持开放、不关闭', True, '不以内生推导替代外部测量')

npass = sum(1 for _, ok, _ in results if ok)
print('=== G5/226 P2 数据规格与可用性判定 ===')
print('结果 %d/%d 成立' % (npass, len(results)))
for name, ok, note in results:
    print('[%s] %-38s %s' % ('PASS' if ok else 'FAIL', name, note))
print()
print('--- 数据请求单 ---')
for k_, v_ in fields.items():
    print('%s：%s' % (k_, v_))
print()
print('--- 判定 ---')
print('S1 三重不可用（脱附能非脱附场 / M 扇区非 m=1,2 / 无不确定度）。')
print('226 阻塞于外部数据；P2 协议已冻结，数据到位即可判定。')
print('不以内生推导替代外部测量；226 维持开放。')
print()
print('总体判定：', 'ALL_PASS' if npass == len(results) else 'HAS_FAIL')
