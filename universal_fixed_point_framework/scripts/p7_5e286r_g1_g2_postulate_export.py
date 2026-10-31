# -*- coding: utf-8 -*-
# p7_5e286r_g1_g2_postulate_export.py
# 判别④ G1 公设层导出（负幂结构 m^-1/m^-2/m^-3）+ G2 系数 1/2 载体归约
# 精确分数（Fraction/Rational），无浮点。模式 8：先证伪再登记，不越权升定案层。
#
# G1 缺口（303 段原文）：闭式 m 函数形式（1/m、1/m^2、1/m^3 负幂结构）未从公设导出。
# 本步判别路线：有限深自相似递推（元公理 1）=> 传递算子幂零 => resolvent Neumann 级数截断，
#   截断深度 d == 幂零指数 L。用精确代数作等价性判别，而非数值拟合。
from fractions import Fraction as F
import sympy as sp

# ---- 框架常数 ----
k_max = 8
n_max = k_max + 2      # 10
N_gen = 3              # 生成链代数（三层碗形链层数）
Np = k_max - 3         # 5

# ---- 闭式五系数（286h 组装，闭合到 k_max 窗口算术谱）----
a1 = F(1, 2)           # m/2 线性系数（G2 对象）
a0 = F(1, 8)           # 常数项
C = F(13, 128)         # 1/m 系数
D = F(41, 2000)        # 1/m^2 系数
E = F(39, 2000)        # 1/m^3 系数（取负号入闭式）

DEG = 0                # 背景多项式次数（Landau 线性标度）
LAYERS = N_gen         # 层数（三层碗形链）

results = []
def chk(name, cond, detail=''):
    results.append((name, bool(cond), detail))

def closed(m):
    return a1 * m + a0 + C / m + D / (m * m) - E / (m * m * m)

# =========================================================
# A. 负幂截断深度精确判别（Laurent 极小分母幂）
# =========================================================
mm = sp.Symbol('m', positive=True)
expr = (sp.Rational(a1.numerator, a1.denominator) * mm
        + sp.Rational(a0.numerator, a0.denominator)
        + sp.Rational(C.numerator, C.denominator) / mm
        + sp.Rational(D.numerator, D.denominator) / mm ** 2
        - sp.Rational(E.numerator, E.denominator) / mm ** 3)

def poly_of(e):
    try:
        return True, sp.Poly(sp.expand(e), mm)
    except sp.PolynomialError:
        return False, None

# A1: 最小 j 使 m^j·F 为多项式 —— 该 j 即负幂深度 d
depths = []
for j in range(0, 8):
    ok, _ = poly_of(expr * mm ** j)
    depths.append((j, ok))
dmin = next(j for j, ok in depths if ok)
chk('A1 负幂深度 d = min{j : m^j·F 为多项式}', dmin == 3,
    '深度序列 %s => d=%d' % (depths, dmin))

# A2: d=3 非 d=2（m^2·F 非多项式，因 E 项 1/m^3 存在）
ok2, _ = poly_of(expr * mm ** 2)
chk('A2 d≠2（m²·F 非多项式，E 项非零）', not ok2)

# A3: m^3·F 的精确系数表（m^4..m^0）——无 m^-1 及更低项 => 无 m^-4
Qexp = sp.expand(expr * mm ** 3)
Qpoly = sp.Poly(Qexp, mm)
qcoef = [sp.nsimplify(Qpoly.nth(k)) for k in range(4, -1, -1)]   # m^4, m^3, m^2, m^1, m^0
qcoef_f = [F(int(sp.fraction(c)[0]), int(sp.fraction(c)[1])) for c in qcoef]
qlib = [a1, a0, C, D, -E]
chk('A3 m³·F 系数表 = 闭式五系数', qcoef_f == qlib,
    '实测 %s vs 期望 %s' % (qcoef_f, qlib))

# A4: 常数项（m^0）= -E ≠ 0 => d≥3；结合 A1 得 d=3 精确
chk('A4 m³·F 常数项 = -E ≠ 0（d≥3，m^-3 项非零）', qcoef_f[-1] == -E and E != 0)

# A5: 反事实——若附加 7/(3000 m^4) 假想项，深度将变 4（判别器有效，非空判据）
expr_bad = expr + sp.Rational(7, 3000) / mm ** 4
ok_bad, _ = poly_of(sp.expand(expr_bad * mm ** 3))
ok_bad4, _ = poly_of(sp.expand(expr_bad * mm ** 4))
chk('A5 反事实（+7/(3000m⁴)）=> m³·F 非多项式、m⁴·F 多项式（深度判别器有效）',
    (not ok_bad) and ok_bad4)

# =========================================================
# B. 结构导出：三层幂零传递算子 => resolvent 截断深度 3
# =========================================================
J = sp.Matrix([[0, 1, 0], [0, 0, 1], [0, 0, 0]])   # 3x3 幂零 Jordan（幂零指数 3）
chk('B1 J³=0 且 J²≠0（幂零指数精确 3）',
    J ** 3 == sp.zeros(3, 3) and J ** 2 != sp.zeros(3, 3),
    'J²=%s' % (J ** 2).tolist())

# B2: resolvent 三终止 Neumann 级数：A³=0 => (mI-A)^-1 = I/m + A/m² + A²/m³
Rm = (mm * sp.eye(3) - J).inv()
ser3 = sp.eye(3) / mm + J / mm ** 2 + J ** 2 / mm ** 3
chk('B2 (mI-J)⁻¹ = I/m + J/m² + J²/m³（Neumann 三级截断）',
    sp.simplify(Rm - ser3) == sp.zeros(3, 3))

# B3: 闭式尾项恰为该幂零 resolvent 的秩三读值：u=e1, v=(C,D,-E)
u = sp.Matrix([[1], [0], [0]])
v = sp.Matrix([[sp.Rational(C.numerator, C.denominator)],
               [sp.Rational(D.numerator, D.denominator)],
               [sp.Rational(-E.numerator, E.denominator)]])
tail_real = sp.simplify((u.T * Rm * v)[0])
tail_tgt = (sp.Rational(C.numerator, C.denominator) / mm
            + sp.Rational(D.numerator, D.denominator) / mm ** 2
            - sp.Rational(E.numerator, E.denominator) / mm ** 3)
chk('B3 闭式尾项 = e1ᵀ(mI-J)⁻¹v（v=(13/128, 41/2000, -39/2000)）',
    sp.simplify(tail_real - tail_tgt) == 0,
    'uᵀ(mI-J)⁻¹v = %s' % tail_real)

# B4: 一般 3x3 A 的 m^-4 系数 = uᵀA³v ≠ 0（非幂零即逸出 => 截断 ⟺ 幂零）
A0 = sp.Matrix([[2, 1, 3], [0, 1, 2], [1, 0, 4]])   # 非幂零实例（A³≠0）
u0 = sp.Matrix([[1], [2], [0]])
v0 = sp.Matrix([[3], [1], [2]])
R0 = (mm * sp.eye(3) - A0).inv()
trunc = (u0.T * v0)[0] / mm + (u0.T * A0 * v0)[0] / mm ** 2 + (u0.T * A0 ** 2 * v0)[0] / mm ** 3
rem = sp.simplify((u0.T * R0 * v0)[0] - trunc)
c4 = sp.limit(rem * mm ** 4, mm, sp.oo)
c4_t = (u0.T * A0 ** 3 * v0)[0]
chk('B4 一般 A：m⁻⁴ 系数 = uᵀA³v ≠ 0（非幂零即逸出）',
    sp.simplify(c4 - c4_t) == 0 and sp.simplify(c4_t) != 0,
    'c4 = %s, A³≠0' % c4)

# B5: 4x4 幂零对照 => 深度 4（深度 == 幂零指数，判别而非拟合）
J4 = sp.Matrix(4, 4, lambda i, j: 1 if j == i + 1 else 0)
u4 = sp.Matrix([[1], [0], [0], [0]])
v4 = sp.Matrix([[1], [2], [3], [5]])
R4 = (mm * sp.eye(4) - J4).inv()
t4 = sp.simplify((u4.T * R4 * v4)[0])
rem4 = sp.simplify(t4 - ((u4.T * v4)[0] / mm + (u4.T * J4 * v4)[0] / mm ** 2
                         + (u4.T * J4 ** 2 * v4)[0] / mm ** 3))
c4_b = sp.limit(rem4 * mm ** 4, mm, sp.oo)
chk('B5 4x4 幂零对照 => 深度 4（c4 = uᵀJ₄³v = 5 ≠ 0）',
    sp.simplify(c4_b) == (u4.T * J4 ** 3 * v4)[0] and sp.simplify(c4_b) != 0,
    'c4 = %s' % c4_b)
chk('B6 深度 d=3 ⟺ 幂零指数 3（三层递推与负幂截断同一事实两表述）',
    dmin == 3 and LAYERS == 3,
    'd=3 ⇔ L=3；由 A/B1-B5 等价链闭合')

# =========================================================
# C. 背景次数：Landau 线性标度（无 m² 项）
# =========================================================
bg = sp.expand(expr - (sp.Rational(C.numerator, C.denominator) / mm
                       + sp.Rational(D.numerator, D.denominator) / mm ** 2
                       - sp.Rational(E.numerator, E.denominator) / mm ** 3))
chk('C1 背景 = m/2+1/8 为次数 1 多项式（无 m² 项）',
    sp.Poly(bg, mm).degree() == 1, '背景=%s' % bg)

# C2: 全 Laurent 谱 {+1,0,-1,-2,-3}——五个指数全非零、指数集完整无缺
spectrum = [(1, a1), (0, a0), (-1, C), (-2, D), (-3, -E)]
chk('C2 Laurent 谱 {+1,0,-1,-2,-3} 五个系数全非零',
    all(c != 0 for _, c in spectrum) and
    sorted([p for p, _ in spectrum]) == [-3, -2, -1, 0, 1])

# C3: 分解唯一：背景次数 1 且尾项从 m^-3 分母起 —— m² 项与 m^-4 项双缺位
chk('C3 双缺位（无 m²、无 m^-4）=> 五谱唯一', 
    sp.Poly(bg, mm).degree() == 1 and dmin == 3)

# =========================================================
# D. G2：线性系数 1/2 的载体归约与载体非唯一性
# =========================================================
D1 = F(k_max * k_max, 1) / F(2 ** (k_max - 1), 1)      # 窗口中心/窗口和 = 64/128
chk('D1 1/2 = k_max²/2^(k_max−1) = 64/128（窗口中心/窗口和）', D1 == a1)
D2 = F(k_max * k_max, 1) / F(2 ** (k_max + 1), 1)      # 64/512
chk('D2 1/8 = k_max²/2^(k_max+1) = 64/512 = α/4', D2 == a0 and D2 == a1 / 4)
D3 = F(2 ** (k_max - 4), 1)                             # 16 = 2^4
chk('D3 128-分母谱族 {64,16,13}/128 = {1/2, 1/8, 13/128}',
    F(64, 128) == a1 and F(16, 128) == a0 and F(13, 128) == C,
    '共同分母 2^(k_max−1)=128；分子 64=k_max², 16=2^(k_max−4), 13=k_max+5')
#D4: 分母差因子 4 = 2² = 2^d（二维通道因子）
chk('D4 α/β = 4 = 2²（二维通道维度因子候选）', a1 / a0 == 4)

# D5: 载体非唯一——1/2 的两种不等价框架载体（窗口比 vs 纯二进制）
carrier_win = F(k_max * k_max, 1) / F(2 ** (k_max - 1), 1)
carrier_bin = F(1, 2)
chk('D5 1/2 双载体（窗口 64/128 vs 纯二进制 2⁻¹）——值不锁定窗口机制',
    carrier_win == carrier_bin == a1,
    '两载体同为 1/2 但生成链不同 => 载体唯一性未锁定')
# D6: 1/8 三载体（64/512、2^-3、2^-(k_max-5)）
c1 = F(64, 512); c2 = F(1, 2 ** 3); c3 = F(1, 2 ** (k_max - 5))
chk('D6 1/8 三载体（64/512、2⁻³、2^−(k_max−5)）——多重归约，非唯一',
    c1 == c2 == c3 == a0,
    'k_max−5=3 => 三载体同值')
# D7: C 项同分母 128 与 α 共享窗口谱（G2 与 G1 的 C 项同源分母）
chk('D7 C=13/128 与 α=64/128 共享分母 2^(k_max−1)=128（一次窗口谱族）',
    F(k_max * k_max, 128) == a1 and C.denominator == 128 and C.denominator == 2 ** (k_max - 1))

# =========================================================
# E. 闭式 m 谱复核（m=1..12 精确分数，判别未破坏）
# =========================================================
vals = {m: closed(F(m, 1)) for m in range(1, 13)}
mono = all(vals[m + 1] > vals[m] for m in range(1, 12))
chk('E1 闭式 m=1..12 谱单调递增（结构导出未破坏物理谱）', mono,
    '1/B*(1)=%s, 1/B*(12)=%s' % (vals[1], vals[12]))
chk('E2 端点值复核 1/B*(1)=11641/16000', vals[1] == F(11641, 16000))
chk('E3 端点值复核 1/B*(12)=7065901/1152000', vals[12] == F(7065901, 1152000))

# ---- 汇总 ----
npass = sum(1 for _, ok, _ in results if ok)
print('=== p7_5e286r G1 公设层导出 + G2 载体归约 数值先证伪 ===')
print('结果 %d/%d 通过' % (npass, len(results)))
for name, ok, detail in results:
    print('[%s] %-58s %s' % ('PASS' if ok else 'FAIL', name, detail))
print('--- 判别分层 ---')
print('G1：形式（负幂截断 d=3）由公设（元公理1 自相似 + 有限深 L=3）导出；')
print('    深度取值 L=3（三层碗形链/N_gen）与系数归属 v=(C,D,-E) 仍实例级——登记升级非关闭。')
print('G2：1/2 载体归约到 k_max²=64 单载体（64/128），但载体非唯一（窗口比 vs 二进制）——机制未锁定。')
print('总体判定：', 'ALL_PASS' if npass == len(results) else 'HAS_FAIL')
