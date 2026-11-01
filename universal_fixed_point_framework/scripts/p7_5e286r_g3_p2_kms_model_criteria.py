# -*- coding: utf-8 -*-
"""P7-5e-362 判据：G3-P2-2 KMS β=1 最小显式模型（存在 / β 唯一 / 态唯一）

口径（纪要六十四节）：G3 子项 P2 = KMS（β=1）↔ 递归热化；载体 = 框架状态空间的模算子；
状态 = 未定义。P2-1 已立纯代数骨架（AutFlow / 离散-连续桥），本轮补**本体最小显式模型**：
在 M₂(ℂ) 上取 H = diag(0,Δ)、ρ₁ = e^{−H}、σ_t = Ad e^{itH}，用精确符号机检
（无浮点断言、无新公设、不做同认/指认补位）：
① KMS β=1 主恒等式对任意 A,B 成立；② 边界值约定唯一（两条错误约定均非零）；
③ β 被 KMS 唯一锁定；④ KMS ⟹ Gibbs（态唯一）。
诚实边界：显式模型成立 ≠ 框架载体存在（RecObj 上的模算子/状态空间未定义；
「H = 递归步生成元」未从范畴导出）——P2 未成立。不关闭任何项。
"""
import pathlib
import random
import re

import sympy as sp

I = sp.I

DIG = pathlib.Path(r"E:\workspace\hyper-resolution\P7-5e_最新研究成果_2026-10-30.md")
SRC = pathlib.Path(__file__)
text = DIG.read_text(encoding="utf-8")
src = SRC.read_text(encoding="utf-8")

results = []


def chk(tag, name, cond, note=""):
    results.append((tag, name, bool(cond), note))
    print(f"[{'PASS' if cond else 'FAIL'}] {tag} {name}" + (f"   {note}" if note else ""))
    return bool(cond)


def zero(x):
    if isinstance(x, sp.MatrixBase):
        return all(zero(v) for v in x)
    e = sp.powsimp(sp.expand(x), combine="exp", force=True)
    e = sp.simplify(e)
    return e == 0


# ---------------- 模型（精确，不归一也等价：Z 约掉） ----------------
DELTA = sp.Integer(1)
H = sp.diag(sp.Integer(0), DELTA)
RHO = sp.diag(sp.Integer(1), sp.exp(-DELTA))
t = sp.Symbol("t", real=True)
b = sp.Symbol("beta", real=True)
A = sp.Matrix(2, 2, lambda r, c: sp.Symbol("a%d%d" % (r, c)))
B = sp.Matrix(2, 2, lambda r, c: sp.Symbol("b%d%d" % (r, c)))


def U(x, delta=DELTA):
    return sp.diag(sp.Integer(1), sp.exp(I * x * delta))


def Ui(x, delta=DELTA):
    return sp.diag(sp.Integer(1), sp.exp(-I * x * delta))


def w(X, rho=RHO):
    return sp.trace(rho * X)


# ---------------- A 口径 ----------------
chk("A1", "G3-P2 口径在册（六十四节：KMS（β=1）↔ 递归热化；载体 = 框架状态空间的模算子；状态 = 未定义）",
    "KMS（β=1）↔ 递归热化" in text and "载体 = 框架状态空间的模算子" in text
    and "状态 = 未定义" in text)

chk("A2", "P2-1 骨架在册（AutFlow / 离散-连续桥 pow_eq_nsmul / 整数时刻外性）",
    "AutFlow" in text and "pow_eq_nsmul" in text and "整数时刻外性" in text,
    "骨架 ≠ 本体；本轮补本体最小显式模型")

chk("A3", "P2-1 诚实边界在册（骨架只描述「若存在模流」，本体未定义）",
    "纯代数骨架" in text and "不构造 vN/KMS 本体" in text and "P2 未成立" in text)

# ---------------- B 模型显式性 ----------------
chk("B1", "模型显式：A = M₂(ℂ)、H = diag(0,Δ) 非退化、ρ₁ = e^{−H}、ω₁ = Tr(ρ₁·)、σ_t = Ad e^{itH}",
    H[0, 0] != H[1, 1] and zero(RHO[0, 0] - 1) and zero(RHO[1, 1] - sp.exp(-DELTA))
    and zero(U(t)[1, 1] - sp.exp(I * t * DELTA)),
    "Δ = h₂ − h₁ = %s ≠ 0；归一常数 Z = 1 + e^{−Δ} 在 ω₁ 中约掉" % DELTA)

p1 = sp.Integer(1) / (1 + sp.exp(-DELTA))
chk("B2", "态规格：p = 1/(1+e^{−Δ}) = e/(1+e) 精确、0 < p < 1、p + (1−p) = 1",
    zero(p1 - sp.exp(1) / (1 + sp.exp(1))) and p1.is_positive
    and sp.simplify(1 - p1).is_positive and zero(p1 + (1 - p1) - 1),
    "ρ₁ 为归一正定态（密度矩阵）")

ts_ok = True
for ss, tt in [(sp.Rational(1, 2), sp.Rational(1, 3)), (sp.Rational(-2, 5), sp.Rational(7, 4)),
               (sp.Integer(0), sp.Integer(3)), (sp.Integer(2), sp.Integer(-1))]:
    ts_ok &= zero(U(ss + tt) - U(ss) * U(tt)) and zero(U(ss) * U(tt) - U(tt) * U(ss))
ts_ok &= zero(U(0) - sp.eye(2)) and zero(U(-t) * U(t) - sp.eye(2))
chk("B3", "σ_t 是一参数自同构群：加性、σ₀ = id、σ_{−t} = (σ_t)⁻¹、不同时刻交换（4 组精确有理 t,s）", ts_ok)

bridge = all(zero((U(sp.Rational(1, 7)) ** n) - U(sp.Rational(n, 7))) for n in range(1, 7))
chk("B4", "离散-连续桥在本模型实现：(σ_s)^n = σ_{n s}（n = 1..6，s = 1/7）", bridge,
    "即 P2-1 的 pow_eq_nsmul 在显式模型中的实例")

# ---------------- C KMS 主恒等式 ----------------
z = t + I
d_main = w(A * U(z) * B * Ui(z)) - w(U(t) * B * Ui(t) * A)
chk("C1", "KMS β=1 主恒等式：ω₁(A σ_{t+i}(B)) = ω₁(σ_t(B) A)，任意 A,B 符号精确为零",
    zero(d_main), "A、B 各 4 个符号元素；t 符号 ⇒ 对一切 t 成立")

scale_ok = True
for dl in [sp.Integer(2), sp.Rational(1, 3), sp.Rational(5, 2)]:
    rhod = sp.diag(sp.Integer(1), sp.exp(-dl))
    scale_ok &= zero(w(A * U(z, dl) * B * Ui(z, dl), rhod)
                     - w(U(t, dl) * B * Ui(t, dl) * A, rhod))
chk("C2", "标度稳健：Δ ∈ {1, 2, 1/3, 5/2} 四种谱间隔下主恒等式均精确为零", scale_ok,
    "恒等式只依赖 exp(i·z·Δ)，与 Δ 的取值无关")

random.seed(7)
bad = 0
for _ in range(30):
    Am = sp.Matrix(2, 2, lambda r, c: sp.Rational(random.randint(-3, 3), random.randint(1, 4))
                   + I * sp.Rational(random.randint(-3, 3), random.randint(1, 4)))
    Bm = sp.Matrix(2, 2, lambda r, c: sp.Rational(random.randint(-3, 3), random.randint(1, 4))
                   + I * sp.Rational(random.randint(-3, 3), random.randint(1, 4)))
    ts = sp.Rational(random.randint(-3, 3), 2)
    if not zero(w(Am * U(ts + I) * Bm * Ui(ts + I)) - w(U(ts) * Bm * Ui(ts) * Am)):
        bad += 1
chk("C3", "随机实例：30 组精确复有理 A,B,t 全部命中（0 反例），无浮点",
    bad == 0, "反例数 = %d / 30" % bad)

bad1 = w(U(z) * B * Ui(z) * A)      # 错序：σ_{t+i}(B) 在前
bad2 = w(A * U(t) * B * Ui(t))      # 不做延拓：右端用实时间
chk("C4", "边界值约定唯一：错序与不延拓两条候选均非零 ⇒ 约定不可自由选取",
    not zero(bad1) and not zero(bad2), "本轮按 ω₁(A σ_{t+i}(B)) = ω₁(σ_t(B) A) 记账")

# ---------------- D β 唯一 / 态唯一 ----------------
A0 = sp.Matrix([[0, 1], [0, 0]])
B0 = sp.Matrix([[0, 0], [1, 0]])
zb = t + I * b
d_beta = w(A0 * U(zb) * B0 * Ui(zb)) - w(U(t) * B0 * Ui(t) * A0)
target = sp.exp(I * t) * sp.exp(-DELTA) * (sp.exp((1 - b) * DELTA) - 1)
chk("D1", "β 唯一（族级）：差式 = e^{itΔ}e^{−Δ}(e^{(1−β)Δ}−1)，β = 1 为零、β = 2 与 β = 0 均非零",
    zero(d_beta - target) and zero(d_beta.subs(b, 1)) and not zero(d_beta.subs(b, 2))
    and not zero(d_beta.subs(b, 0)),
    "差式.b=1 → 0；.b=2 → (1−e)e^{−2}；.b=0 → 1−e^{−1}")

p, q = sp.Symbol("p"), sp.Symbol("q")
RHO_G = sp.Matrix([[p, q], [sp.conjugate(q), 1 - p]])
wg = lambda X: sp.trace(RHO_G * X)
E01 = sp.Matrix([[0, 1], [0, 0]])
E10 = sp.Matrix([[0, 0], [1, 0]])
E00 = sp.Matrix([[1, 0], [0, 0]])
eq1 = sp.simplify(sp.expand(wg(E01 * U(I) * E10 * Ui(I)) - wg(E10 * E01)))
eq2 = sp.simplify(sp.expand(wg(E00 * U(I) * E01 * Ui(I)) - wg(E01 * E00)))
sol = sp.solve([eq1, eq2], [p, q], dict=True)
chk("D2", "态唯一（KMS ⟹ Gibbs）：一般 Hermite 密度矩阵 ρ = [[p,q],[q̄,1−p]] 施以 KMS ⇒ p = e/(1+e)、q = 0，解唯一",
    len(sol) == 1 and zero(sol[0][p] - sp.exp(1) / (1 + sp.exp(1))) and zero(sol[0][q]),
    "约束式：p·e^{−Δ} + p − 1 = 0；e·q̄ = 0")

rhod = sp.diag(sp.Integer(1), sp.Integer(1))          # Δ = 0：H = 0 ⇒ 平凡流 σ_t = id
Udd = lambda x: sp.diag(sp.exp(0 * I * x), sp.exp(0 * I * x))
d_deg = (sp.trace(rhod * A0 * Udd(t + I * b) * B0 * Udd(-(t + I * b)))
         - sp.trace(rhod * Udd(t) * B0 * Udd(-t) * A0))
chk("D3", "退化对照：Δ = 0 时任意 β 恒成立 ⇒ 非退化谱是 β 确定性的必要前提",
    zero(d_deg), "登记为前提，不新设公设")

chk("D4", "玻尔兹曼比：p/(1−p) = e^{Δ} 精确 ⇒ 态即 e^{−H} 归一（Gibbs 形式）",
    zero(p1 / (1 - p1) - sp.exp(DELTA)), "p/(1−p) = e")

# ---------------- E 桥接与边界 ----------------
chk("E1", "与 P2-1 桥接：本模型 σ_t 的整数采样即 AutFlow 的 (σ_s)^n = σ_{n•s}（B4 机检）",
    bridge and "pow_eq_nsmul" in text, "骨架 → 本体：同一桥在显式模型中成立")

chk("E2", "诚实边界（一）：显式模型 ≠ 框架载体——RecObj 上的忠实正规态 / 模算子 Δ / 状态空间仍未定义",
    "载体" in text and "模算子" in text and "未定义" in text,
    "本轮给的是模型级实例，不是载体")

no_vn = (("class " + "VonNeumann") not in src and ("def modular" + "Operator") not in src
         and ("def kms" + "State") not in src and ("def state" + "Space") not in src
         and ("struc" + "ture") not in src)
chk("E3", "不越界：脚本不定义 vN 代数 / 模算子 / KMS 态 / 状态空间，不把模型升级为载体",
    no_vn, "只做有限维矩阵模型与精确符号机检")

chk("E4", "不关闭任何项：226 维持 suspended-awaiting-data；k(2) 维持观察身份开放",
    "suspended-awaiting-data" in text and "k(2) 维持观察身份开放" in text,
    "登记 ≠ 成立 ≠ 闭合")

chk("E5", "无浮点断言：脚本文本不含浮点字面量（全部精确有理/符号）",
    re.search(r"\d+\.\d+", src) is None, "零浮点")

print()
passed = sum(1 for r in results if r[2])
print(f"{passed}/{len(results)} " + ("ALL_PASS" if passed == len(results) else "HAS_FAILURE"))
print("判定：M₂(ℂ) 上 H = diag(0,Δ)、ρ₁ = e^{−H}、σ_t = Ad e^{itH} 的最小显式模型中，"
      "KMS β=1 主恒等式对任意 A,B 精确成立；边界值约定唯一；β 被唯一锁定（差式 ∝ e^{(1−β)Δ}−1）；"
      "KMS ⟹ Gibbs（态唯一，p/(1−p) = e^{Δ}）；Δ = 0 退化时 β 不被确定。")
print("诚实边界：显式模型成立 ≠ 框架载体存在（RecObj 模算子/状态空间未定义；"
      "「H = 递归步生成元」未从范畴导出）；不以同认/指认公设补位，不动 P4；P2 未成立。")
print("不关闭任何项（226 挂起、k(2) 开放）。")
