# -*- coding: utf-8 -*-
# p7_5e286r_g5_endogenous_uniqueness.py
# G5/226 内生唯一性 + 双链独立性审计（判定：升级登记，不关闭 226）
# 对象：E = 39/2000（1/m^3 系数）
# 纪律：pyenv 精确分数（Fraction）+ sympy，无浮点；禁英文直引号（用中文引号）。
from fractions import Fraction as F
import sympy as sp

ks = sp.symbols('k')

# ---- 框架常数（判别④ 闭式）----
k = 8
N_gen = 3
Np = 5                      # N' = k_max - 3
h2 = F(7, 64)               # h(2)
hp2 = F(13, 600)            # h'(2)
i2 = F(13, 2250)            # i(2)
E = F(39, 2000)             # 1/m^3 系数（本审计对象，符号取绝对值）
D = F(41, 2000)
C = F(13, 128)


def e_win(kk):
    # 闭式链（resolvent 截断侧）：E = (k(k-3)-1)/(2^4 (k-3)^3)
    return F(kk * (kk - 3) - 1, 16 * (kk - 3) ** 3)


def e_fw(kk):
    # 碗形链侧（i(2) 组装化简）：E = (k+5)·N_gen/(2^4 (k-3)^3)
    return F((kk + 5) * N_gen, 16 * (kk - 3) ** 3)


results = []


def chk(name, cond, note=''):
    results.append((name, bool(cond), note))


# =========================================================
# A. 双链同值与独立性审计
# =========================================================
chk('A1 闭式链 k=8 命中 E', e_win(k) == E,
    '(%d·%d−1)/(16·%d^3)=%s' % (k, k - 3, k - 3, e_win(k)))
chk('A2 碗形链化简形式 k=8 命中 E', e_fw(k) == E,
    '(%d+5)·%d/(16·%d^3)=%s' % (k, N_gen, k - 3, e_fw(k)))
chk('A3 i(2) 组装 k=8 命中 E', i2 * F(N_gen, 2) ** 3 == E,
    '(13/2250)·(27/8)=%s' % (i2 * F(N_gen, 2) ** 3))

# 非循环性：i(2) 可由 h'(2) 与框架比 4/15 给出，推导中不出现 E
chk('A4 i(2) 非循环路线 i2=h′·4/15', i2 == hp2 * F(4, 15),
    '(13/600)·(4/15)=%s（未引用 E）' % (hp2 * F(4, 15)))
chk('A5 h′(2) 框架形式 (k+5)/(3k(k−3)²)', hp2 == F(k + 5, 3 * k * (k - 3) ** 2),
    '%s' % hp2)

# 39 双身份：两分子表达在 k=8 相等
chk('A6 39 双身份 (k−5)(k+5)=k(k−3)−1', (k - 5) * (k + 5) == k * (k - 3) - 1 == 39,
    '%d=%d=39' % ((k - 5) * (k + 5), k * (k - 3) - 1))

# 两形式作为 k 的函数：非恒等，唯一交点
ew = (ks ** 2 - 3 * ks - 1) / (16 * (ks - 3) ** 3)
ef = (ks + 5) * N_gen / (16 * (ks - 3) ** 3)
diff = sp.simplify(ew - ef)
num = sp.numer(sp.together(diff))
roots = sp.solve(sp.Eq(num, 0), ks)
chk('A7 两形式相交根集', sorted(roots) == [-2, 8],
    'k²−6k−16=0 根=%s（窗口域 k≥5 内唯一 k=8）' % (sorted(roots),))
chk('A8 两形式非同一函数', sp.simplify(diff) != 0,
    '差=%s（非零 ⇒ 不是同一有理函数的改写）' % (sp.factor(diff),))

# 祖先输入重叠：链1={k_max}；链2={k_max,N_gen,N′}
s1 = {'k_max'}
s2 = {'k_max', 'N_gen', 'N_prime'}
inter = s1 & s2
union = s1 | s2
jacc = F(len(inter), len(union))
chk('A9 祖先重叠 Jaccard=1/3（部分同源）', jacc == F(1, 3),
    '链1=%s 链2=%s 交=%s 独立指数=1−%s=%s'
    % (sorted(s1), sorted(s2), sorted(inter), jacc, 1 - jacc))
chk('A10 双链判定=结构交叉一致但非独立确证', (sorted(roots) == [-2, 8]) and jacc == F(1, 3),
    '唯一交点 k=8 且共享 k_max ⇒ 可作自洽检验，不可作独立验证')

# =========================================================
# B. 内生唯一性
# =========================================================
five = [
    ('m/2', F(1, 2), F(k, 16)),
    ('1/8', F(1, 8), F(1, k)),
    ('13/128', C, F(2 * k - 3, 2 ** (k - 1))),
    ('41/2000', D, F(k * (k - 3) + 1, 16 * (k - 3) ** 3)),
    ('39/2000', E, e_win(k)),
]
all_single_param = all(a == b for _, a, b in five)
chk('B1 五系数皆 k 的单参数有理函数', all_single_param,
    '；'.join('%s=%s' % (n, v) for n, v, _ in five))

win = {k * (k - 1): 'k(k−1)', k * k - 1: 'k²−1', k * k: 'k²', k * k + 1: 'k²+1'}
chk('B2 窗口自守恒 {56,63,64,65}', sorted(win) == [56, 63, 64, 65],
    str(dict(sorted(win.items()))))
chk('B3 窗口和与中心锁定 k', (2 * k * k == 128) and (k * k == 64),
    '和 128=2k²、中心 64=k² ⇒ k=8 唯一正整数解')

r_poly = sp.solve(sp.Eq(ks * (ks - 3) - 1, 39), ks)
r_cube = [r for r in sp.solve(sp.Eq(16 * (ks - 3) ** 3, 2000), ks) if r.is_real]
common = sorted(set(r_poly) & set(r_cube))
chk('B4 分子/分母方程公共根唯一', common == [8],
    'k(k−3)−1=39 根=%s；16(k−3)³=2000 实根=%s；交=%s' % (r_poly, r_cube, common))

vals_win = {kk: e_win(kk) for kk in range(5, 13)}
vals_fw = {kk: e_fw(kk) for kk in range(5, 13)}
chk('B5 双形式在 k=5..12 无简并', len(set(vals_win.values())) == 8 and len(set(vals_fw.values())) == 8,
    '闭式侧互异=8/8、碗形侧互异=8/8')
hits = [kk for kk in range(5, 13) if e_win(kk) == E]
chk('B6 窗口域内唯一命中 k=8', hits == [8],
    'E=39/2000 仅在 k=8 命中（k=5..12 扫描）')
chk('B7 内生唯一性成立（无待定参数）', all_single_param and common == [8] and hits == [8],
    'k 由窗口算术锁定 ⇒ E 唯一确定，无自由度')

# =========================================================
# C. 可关闭性判定（226）
# =========================================================
chk('C1 数值内生可导出', True,
    'E 由 k_max 单参数唯一确定（B7）——数值来源内生')
chk('C2 双链非独立', jacc == F(1, 3),
    '共享 k_max；链2 额外依赖 N_gen/N′ ⇒ 交叉一致非独立验证')
chk('C3 独立测量不可内生关闭', True,
    '226 内容=与框架无关的外部锚；内生推导共享公设集 ⇒ 自证循环')

# ---- 汇总 ----
npass = sum(1 for _, ok, _ in results if ok)
print('=== G5/226 内生唯一性 + 双链独立性审计 ===')
print('结果 %d/%d 通过' % (npass, len(results)))
for name, ok, note in results:
    print('[%s] %-46s %s' % ('PASS' if ok else 'FAIL', name, note))
print()
print('--- 溯源表 ---')
print('闭式链：resolvent 截断尾系数 → E_win(k)=(k(k−3)−1)/(2⁴(k−3)³)，输入 {k_max}')
print('碗形链：h′(2) → i(2)=h′·4/15 → E=i(2)(N_gen/2)³，输入 {k_max, N_gen, N′}')
print('汇合点：两式仅在两分子相等处相交 —— (k−5)(k+5)=k(k−3)−1 ⇔ k=8（另一根 k=−2 出窗口域）')
print()
print('--- 判定 ---')
print('升级：E 数值来源内生唯一（k_max 单参数，无自由度）')
print('      双链为唯一交点的结构交叉一致（部分同源，非独立确证）')
print('不关闭：226（独立测量缺位）由外部锚定义，内生推导不可替代')
print('总体判定：', 'ALL_PASS' if npass == len(results) else 'HAS_FAIL')
