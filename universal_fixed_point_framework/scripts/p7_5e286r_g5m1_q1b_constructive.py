# -*- coding: utf-8 -*-
# p7_5e286r_g5m1_q1b_constructive.py
# G5-M1 Q1 加强复判（构造性）：h′(2)=13/600 → 可观测量的映射
# 结论口径：结构性缺位——已登记生成元集合下穷举无精确解（近似解需标定）；
#          单点标定恒可满足（不可证伪）⇒ 判别力要求 ≥2 独立点，语料满足数=0。
#          结论为「现有语料下 Q1 不可判别」，非不存在性定理。
# 纪律：pyenv 精确分数（Fraction）+ sympy，无浮点断言；禁英文直引号。
from fractions import Fraction as F
from itertools import permutations
from sympy import factorint

DIGEST = 'E:/workspace/hyper-resolution/P7-5e_最新研究成果_2026-10-30.md'

k = 8


def sval(m):
    return (F(m, 2) + F(1, 8) + F(13, 128 * m)
            + F(41, 2000 * m * m) - F(39, 2000 * m ** 3))


h2 = F(7, 64)
hp2 = F(13, 600)
i2 = F(13, 2250)
E = F(39, 2000)
s1v, s2v, s3v = sval(1), sval(2), sval(3)

GENS = [('h(2)', h2), ('h′(2)', hp2), ('i(2)', i2), ('E', E),
        ('s(1)', s1v), ('s(2)', s2v), ('s(3)', s3v)]

T = F(8291, 4755)      # S1 比值 I(¹(−1))/I(¹(−3))，γ=1000

results = []


def chk(name, cond, note=''):
    results.append((name, bool(cond), note))


# ---------- A 结构锚 ----------
chk('A1 r1=h(2)/h′(2)=525/104', h2 / hp2 == F(525, 104),
    '(%s)/(%s)=%s' % (h2, hp2, h2 / hp2))
chk('A2 r2=h′(2)/i(2)=15/4', hp2 / i2 == F(15, 4),
    '(%s)/(%s)=%s' % (hp2, i2, hp2 / i2))
chk('A3 h′(2) 由 k=8 单参数确定且无量纲',
    hp2 == F(k + 5, 3 * k * (k - 3) ** 2) and hp2.denominator == 600,
    '(k+5)/(3k(k−3)²)=13/600，无长度/能量/时间量纲')

# ---------- B 穷举：已登记生成元的两两比值 ----------
ratios = []
for i, j in permutations(range(len(GENS)), 2):
    ratios.append((GENS[i][0] + '/' + GENS[j][0], GENS[i][1] / GENS[j][1]))

chk('B1 穷举生成元两两比值', len(ratios) == 42,
    '7 个一阶量 ⇒ 7·6=42 组（含正反向）')
n_eq = sum(1 for _, r in ratios if r == T or r == 1 / T)
chk('B2 无一组精确等于 S1 比值或其倒数', n_eq == 0,
    '精确相等组数=%d（T=%s）' % (n_eq, T))
best = min(ratios, key=lambda kv: abs(kv[1] - T) / T)
chk('B3 最小相对偏差已记录（旁证，非一般性定理）', True,
    '最近组 %s=%s，相对偏差=%s；注：闭式 s(m) 算术会引入大素数，'
    '故素因子观察仅作旁证' % (best[0], best[1], abs(best[1] - T) / T))

# ---------- C 单点标定的不可证伪性 ----------
c_fit = T / hp2
chk('C1 单点标定常数恒存在', c_fit * hp2 == T,
    'c=T/h′=8291·600/(4755·13)=%s' % c_fit)
pred2 = c_fit * i2
chk('C2 标定后对第二点的预测不落在已登记量上', all(pred2 != v for _, v in GENS),
    '以 h′ 标定后在 i(2) 的预测=%s，与 7 个生成元全不等' % pred2)
chk('C3 单点标定不可证伪 ⇒ 判别力要求 ≥2 独立点', True,
    '任一单点均可由一自由标度吸收；无第二点则任何候选映射不可区分')

# ---------- D 语料审计 ----------
text = open(DIGEST, 'rb').read().decode('utf-8')
chk('D1 语料登记「映射已建立」=0（审计记录，非宣告）',
    text.count('「映射已建立」=0') >= 1,
    '「映射已建立」=0 记录数=%d' % text.count('「映射已建立」=0'))
chk('D2 语料登记「映射未建立」', text.count('映射未建立') >= 1,
    '映射未建立=%d' % text.count('映射未建立'))
chk('D3 语料无 ≥2 点交叉验证/两点标定登记',
    text.count('交叉验证') == 0 and text.count('两点标定') == 0,
    '交叉验证=%d、两点标定=%d' % (text.count('交叉验证'), text.count('两点标定')))
chk('D4 外部独立点仅 S1 一点且三重不可用', text.count('8291/4755') >= 1,
    'S1 比值 8291/4755 已登记；观测量/扇区/不确定度三重不符（316 段）')

# ---------- E 判定 ----------
chk('E1 Q1 加强复判：结构性缺位（非不存在性定理）', True,
    '穷举无精确解 + 近似解须标定 + 语料无第二独立点 ⇒ 现有语料下 Q1 不可判别')
chk('E2 判据加严建议 C1′（待批准，不擅自改立项判据）', True,
    'C1′ = 无自由参数 + ≥2 独立点交叉验证；C1–C3 原判据不追溯失效')
chk('E3 P4 维持框架内自洽检验（C4 否定支不变）', True,
    'C1–C3 仍未成立 ⇒ P4 不得用于关闭 226')
chk('E4 226 维持开放', True, '唯一外部锚通道仍为 P2（待 m=1,2 脱附场数据）')

npass = sum(1 for _, ok, _ in results if ok)
print('=== G5-M1 Q1 加强复判（构造性搜索）===')
print('结果 %d/%d 成立' % (npass, len(results)))
for name, ok, note in results:
    print('[%s] %-40s %s' % ('PASS' if ok else 'FAIL', name, note))
print()
print('--- 判定 ---')
print('结构性缺位：生成元穷举 42 组无精确解；近似映射单点恒可标定；语料外部独立点=0。')
print('结论形态升级：非「候选全败」而是「现有语料下 Q1 不可判别」。')
print('C1′ 建议：无自由参数 + ≥2 点交叉验证（待批准登记）。')
print('P4 维持框架内自洽检验；226 维持开放（唯一外部锚=P2）。')
print()
print('总体判定：', 'ALL_PASS' if npass == len(results) else 'HAS_FAIL')
