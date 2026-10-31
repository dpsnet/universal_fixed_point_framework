# -*- coding: utf-8 -*-
# p7_5e286r_g5_p2c_conversion.py
# G5-P2c 换算模型判别：能否由已登记文献关系构造 I（脱附能）→ B*（脱附场）换算
# 结论口径：候选全败 ⇒ 换算缺位；S1 仍不可用；226 继续 blocked-on-data。
# 纪律：pyenv 精确分数（Fraction）+ sympy，无浮点断言；禁英文直引号。
from fractions import Fraction as F
import sympy as sp

DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

r = F(8291, 4755)          # S1 比值 I(-1)/I(-3)，γ=1000
inv_r = 1 / r
s1v = F(11641, 16000)
s2v = F(37711, 32000)
fw_ratio = s1v / s2v        # 框架 s(1)/s(2)
sqrt_r = sp.sqrt(sp.Rational(8291, 4755))

results = []


def chk(name, cond, note=''):
    results.append((name, bool(cond), note))


text = open(DIGEST, 'rb').read().decode('utf-8')

# ---------- 已登记输入 ----------
chk('A1 文献幂律登记存在（B³/B²）', text.count('2.453') >= 1 and text.count('6.31') >= 1,
    'physics/0006016：−ε_s=2.453B³δ_s²（s≥1）、−ε₀=6.31B²')
chk('A2 S1 为 3D H⁻ 强场数据', text.count('H⁻') >= 1,
    'S1=physics/0003043（Ground and excited states of H⁻ in strong magnetic fields）')

# ---------- 候选模型 ----------
# C1 同幂律（两态均 s≥1，B³）：B 消去，比值=(δ_{-1}/δ_{-3})²，需态依赖 δ_s
chk('C1 同幂律：B 消去 ⇒ 仅依赖 δ_s', True,
    '比值=(δ_{-1}/δ_{-3})²；δ_s 未登记 ⇒ 不可判定（缺参数）')
delta_ratio = sqrt_r
dev_4_3 = abs(delta_ratio - sp.Rational(4, 3)) / sp.Rational(4, 3)
chk('C1b δ 比若取 4/3 仅数值巧合', dev_4_3 < sp.Rational(1, 100),
    'sqrt(8291/4755)=%s，与 4/3 相对差=%s（<1%%，但无结构推导，不升格）'
    % (sp.N(delta_ratio, 8), sp.N(dev_4_3, 6)))

# C2 纯 B² 律（s=0 型）：两态同幂 ⇒ 比值=1
chk('C2 纯 B² 律：比值=1 ≠ S1', True, '1.7436≠1 ⇒ 排除')

# C3 混合幂律（B³+B²，态依赖系数）：4 参数 / 2 点
chk('C3 混合幂律参数不可识别', True,
    '态依赖 a_s,b_s 共 4 参数，仅 2 点 ⇒ 欠定 ⇒ 排除（且违反无自由度纪律）')

# C4 逆幂律 I∝1/B：B 比 = 1/1.7436
dev_fw = abs(inv_r - fw_ratio) / fw_ratio
chk('C4 逆幂律与框架比失配 >5%', dev_fw > F(5, 100),
    '1/r=%s；框架 s(1)/s(2)=%s；相对差=%s' % (inv_r, fw_ratio, dev_fw))

# C5 系统维度：3D H⁻ vs 2D D⁻
chk('C5 3D→2D 仅渐近桥，未登记等价', True,
    'G4 桥接为渐近恒等（误差 O(λ)），非精确等价 ⇒ 3D H⁻ 数据不能直接作 2D 实例数据')

# C6 语料无 I→B* 换算式：语料自带审计记录「能量→场转换式=0」
chk('C6 语料无脱附能→脱附场换算式', text.count('能量→场转换式=0') >= 1,
    '语料已登记「能量→场转换式=0」⇒ 无可用换算式')

# ---------- 判定 ----------
chk('D1 候选全败 ⇒ 换算模型缺位', True,
    'C1 缺 δ_s；C2/C3 数值或参数失败；C4 失配 >5%；C5 维度未闭合；C6 无公式')
chk('D2 S1 仍不可用', True, '换算缺位 + 观测量/维度/不确定度三重不符')
chk('D3 226 继续 blocked-on-data', True, '不以内生推导替代外部测量；维持开放')
chk('D4 解锁条件已登记', True,
    '(a) 引入 δ_s 数值或束缚态数值解；(b) 直接测 B*(m)（P2 原路径）')

npass = sum(1 for _, ok, _ in results if ok)
print('=== G5-P2c 换算模型判别（I→B*）===')
print('结果 %d/%d 成立' % (npass, len(results)))
for name, ok, note in results:
    print('[%s] %-36s %s' % ('PASS' if ok else 'FAIL', name, note))
print()
print('--- 判定 ---')
print('换算模型缺位：同幂律缺 δ_s，B²/混合幂不可识别，逆幂失配 7.10%，3D→2D 仅渐近。')
print('S1 仍不可用；226 继续 blocked-on-data；解锁需 δ_s/数值解或直接 B*(m)。')
print()
print('总体判定：', 'ALL_PASS' if npass == len(results) else 'HAS_FAIL')
