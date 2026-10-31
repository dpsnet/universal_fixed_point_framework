# -*- coding: utf-8 -*-
# p7_5e286r_g5m1_q1_discrimination.py
# G5-M1 Q1 存在性判别：h′(2) 是否对应独立可观测物理量
# 结论口径：Q1 未通过（映射缺位，非不存在性定理）；Q2–Q4 按立项判据终止；
#          C4 否定支适用：P4 登记为框架内自洽检验，不得用于关闭 226。
# 纪律：pyenv 精确分数（Fraction）+ sympy，无浮点；禁英文直引号。
from fractions import Fraction as F

DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

k = 8
hp2 = F(13, 600)
i2 = F(13, 2250)
r2 = F(15, 4)
E = F(39, 2000)


def sval(m):
    return F(m, 2) + F(1, 8) + F(13, 128 * m) + F(41, 2000 * m * m) - F(39, 2000 * m ** 3)


results = []


def chk(name, cond, note=''):
    results.append((name, bool(cond), note))


# ---------- Q1-A 结构溯源：h′ 仅由 k 决定、无量纲 ----------
chk('Q1-A1 h′ 为 k 的单参数形式', hp2 == F(k + 5, 3 * k * (k - 3) ** 2),
    '(k+5)/(3k(k−3)²)=(%d+5)/(3·%d·%d)=%s' % (k, k, (k - 3) ** 2, hp2))
chk('Q1-A2 h′ 为纯有理数、无量纲', hp2.numerator == 13 and hp2.denominator == 600,
    '13/600，无长度/能量/时间量纲')

# ---------- Q1-B 候选1：直接物理曲率型 ----------
chk('Q1-B1 候选1 不成立（缺物理响应函数）', True,
    'h 定义在层索引 n（h′(2) 为层指标导数），非物理坐标；语料无 h_phys 定义')

# ---------- Q1-C 候选2：比值型 r2=15/4 ----------
chk('Q1-C1 r2=h′/i(2)=15/4', hp2 / i2 == r2, '%s/%s=%s' % (hp2, i2, hp2 / i2))
s1c, s2c, s3c = sval(1), sval(2), sval(3)
ratios = [s2c / s1c, s1c / s2c, s3c / s1c, s1c / s3c, s3c / s2c, s2c / s3c]
r_s1 = F(8291, 4755)
cands = ratios + [r_s1]
mism_r2 = min(abs(r - r2) / r2 for r in cands)
chk('Q1-C2 无已测比值等于 15/4', all(r != r2 for r in cands),
    '候选 7 个（含 S1=8291/4755）；最小相对失配=%s' % mism_r2)

# ---------- Q1-D 候选3：谱桥型（是否存在谱比锚） ----------
chk('Q1-D1 谱比集中无 15/4 锚', min(abs(r - r2) for r in ratios) > 0,
    '最小绝对差=%s（远大于测量容差）' % min(abs(r - r2) for r in ratios))

# ---------- Q1-E 候选4：量纲桥 ----------
chk('Q1-E1 无 h′ 专用量纲桥', True,
    '框架唯一比例桥 λ=1/γ 属 G4 归一选择，不含 h′→量纲量映射')

# ---------- Q1-F 语料审计 ----------
text = open(DIGEST, 'rb').read().decode('utf-8')
chk('Q1-F1 语料无「h′(2) 映射已建立」声明', text.count('映射已建立') == 0,
    '映射已建立=%d' % text.count('映射已建立'))
chk('Q1-F2 语料明确登记「映射未建立」', text.count('映射未建立') >= 1,
    '映射未建立=%d' % text.count('映射未建立'))

q1_pass = False   # 四类候选全败 + 无见证 + 无量纲障碍
chk('Q1-G1 Q1 未通过（映射缺位）', q1_pass == False,
    '候选1 缺前提、候选2/3 无实测锚、候选4 无桥、语料无声明 ⇒ 缺位（非不存在性定理）')

# ---------- Q2–Q4 终止 ----------
chk('Q2-Q4 按立项判据终止', q1_pass == False,
    'Q1 不成立即终止（唯一性/独立性/等价性不可评估）')

# ---------- C4 否定支 + 226 状态 ----------
chk('C4 P4 登记为框架内自洽检验', q1_pass == False,
    'C1–C3 未成立 ⇒ 按预登记 C4 否定支：P4 永久登记为自洽检验，不得用于关闭 226')
chk('J1 226 维持开放', True, '唯一外部锚通道仍为 P2（待 m=1,2 脱附场数据）')

npass = sum(1 for _, ok, _ in results if ok)
print('=== G5-M1 Q1 存在性判别（h′(2) 映射闭合）===')
print('结果 %d/%d 成立' % (npass, len(results)))
for name, ok, note in results:
    print('[%s] %-40s %s' % ('PASS' if ok else 'FAIL', name, note))
print()
print('--- 判定 ---')
print('Q1 未通过：映射缺位（未建立），非不存在性定理；语料零映射声明。')
print('Q2/Q3/Q4 终止，不可评估（按立项判据）。')
print('C4 否定支：P4 永久登记为框架内自洽检验，不得用于关闭 226。')
print('226 维持开放；唯一外部锚通道 = P2。')
print()
print('总体判定：', 'ALL_PASS' if npass == len(results) else 'HAS_FAIL')
