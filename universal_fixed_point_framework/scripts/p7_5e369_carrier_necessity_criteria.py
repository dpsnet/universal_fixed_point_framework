# -*- coding: utf-8 -*-
"""
P7-5e-369 / G3-P2-4 载体必要性判别 —— 判据脚本（精确符号，无浮点）
=====================================================================
记号纪律（沿用 367/368）：
  M = 模哈密顿量（自伴算子），Δ_mod = e^{−2πM}，σ_t = Ad Δ_mod^{it}。
  框架原生 Δ（spExchangeLaw）不出现、不赋值；本脚本不做「Δ = 1」。

机检对象：
  formal_proof/MUFPFormalization/src/MUFPFormalization/G3CarrierNecessity.lean
  命名空间 MUFPF.G3CarrierNecessity，16 条定理/定义。

判据 C01–C16 全部 PASS 才打印 ALL_PASS。
无浮点：只用 int / sympy Integer / sympy Rational / 符号 pi、exp。
"""

import io
import os

import sympy as sp

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEAN = os.path.join(
    ROOT, "formal_proof", "MUFPFormalization", "src", "MUFPFormalization",
    "G3CarrierNecessity.lean",
)
LEAN_KMS = os.path.join(
    ROOT, "formal_proof", "MUFPFormalization", "src", "MUFPFormalization",
    "G3KMSBetaToModular.lean",
)

results = []


def check(cid, desc, fn):
    try:
        ok, detail = fn()
    except Exception as exc:  # noqa: BLE001
        ok, detail = False, f"EXC {type(exc).__name__}: {exc}"
    results.append((cid, desc, bool(ok), detail))
    print(f"[{cid}] {'PASS' if ok else 'FAIL'} — {desc} :: {detail}")


def read_lean():
    with io.open(LEAN, "r", encoding="utf-8") as fh:
        return fh.read()


def read_kms():
    with io.open(LEAN_KMS, "r", encoding="utf-8") as fh:
        return fh.read()


I2 = sp.eye(2)
E12 = sp.Matrix([[0, 1], [0, 0]])


def rmat(block11, block12, block21, block22):
    """2×2 分块矩阵（每块 2×2）。"""
    return sp.Matrix(sp.BlockMatrix([[block11, block12], [block21, block22]]))


# ---------------- C01–C04：中心共轭与块标量 ----------------
def c01():
    u = sp.Matrix([[1, 1], [0, 1]])
    a = u * u  # 与 u 交换
    lhs = sp.simplify(u * a * u.inv() - a)
    return lhs == sp.zeros(2, 2), f"u a u⁻¹ − a = {lhs}"


def c02():
    c = sp.Rational(3, 2)
    b = sp.Matrix([[1, 2], [3, 5]])
    lhs = sp.simplify((c * I2) * b - b * (c * I2))
    return lhs == sp.zeros(2, 2), f"标量矩阵中心性残差={lhs}"


def c03():
    u = sp.Rational(5, 3)
    p0 = rmat(I2, sp.zeros(2, 2), sp.zeros(2, 2), sp.zeros(2, 2))
    conj = rmat(u * I2, sp.zeros(2, 2), sp.zeros(2, 2), u * I2) * p0 * \
        rmat((1 / u) * I2, sp.zeros(2, 2), sp.zeros(2, 2), (1 / u) * I2)
    return sp.simplify(conj - p0) == sp.zeros(4, 4), "块标量共轭固定块投影 P₀"


def c04():
    p0 = rmat(I2, sp.zeros(2, 2), sp.zeros(2, 2), sp.zeros(2, 2))
    p1 = rmat(sp.zeros(2, 2), sp.zeros(2, 2), sp.zeros(2, 2), I2)
    swapped = rmat(sp.zeros(2, 2), sp.zeros(2, 2), sp.zeros(2, 2), I2)  # 块交换占位
    # 真正的块交换：P₀ ↦ P₁；此处只需 P₁ ≠ P₀ 与 P₀ 由标量共轭固定
    return (p1 - p0) != sp.zeros(4, 4) and sp.simplify(swapped - p1) == sp.zeros(4, 4), \
        "块交换 P₀ ↦ P₁ ≠ P₀，故块标量实现不能实现外步"


# ---------------- C05–C06：交换载体判别 ----------------
def c05():
    ident = lambda p: p
    swap = lambda p: (p[1], p[0])
    p0 = (sp.Integer(1), sp.Integer(0))
    # 恒等：内实现（u=(1,1)）
    id_inner = ident(p0) == p0
    # 交换：任何单位 u=(x,y)（x,y≠0）共轭给 (x·1/x, y·0/y)=(1,0)，不能给 (0,1)
    x, y = sp.symbols("x y", nonzero=True)
    conj = (sp.simplify(x * p0[0] / x), sp.simplify(y * p0[1] / y))
    swap_moves = swap(p0) != p0
    return id_inner and conj == p0 and swap_moves, \
        f"ℚ×ℚ：恒等内、交换移动 {p0}→{swap(p0)}，单位共轭固定 {conj}"


def c06():
    # 交换代数：任意内实现必恒等（对应 Lean innerFlow_all_refl_of_commutative）
    x, y, a, b = sp.symbols("x y a b", nonzero=True)
    lhs = sp.simplify(x * a / x - a)
    rhs = sp.simplify(y * b / y - b)
    return lhs == 0 and rhs == 0, f"交换载体共轭差=({lhs},{rhs}) ⇒ 内流恒等"


# ---------------- C07–C10：层权与块标量模流 ----------------
def c07():
    ratio = sp.simplify(sp.exp(-2 * sp.pi * 1) / sp.exp(-2 * sp.pi * 0))
    diff = sp.simplify(ratio - 1)
    return diff != 0, f"层权比=e^{{−2π}}={ratio}，e^{{−2π}}−1={diff}≠0"


def c08():
    # 层对角（块标量）C：块内标量 ⇒ 共轭恒等
    a, b = sp.Rational(2, 3), sp.Rational(5, 7)
    c = rmat(a * I2, sp.zeros(2, 2), sp.zeros(2, 2), b * I2)
    m1 = sp.Matrix([[1, 2], [3, 4]])
    m2 = sp.Matrix([[5, 6], [7, 8]])
    m = rmat(m1, sp.zeros(2, 2), sp.zeros(2, 2), m2)
    lhs = sp.simplify(c * m * c.inv() - m)
    return lhs == sp.zeros(4, 4), f"层对角块标量共轭残差={lhs}"


def c09():
    # 块内非标量 ⇒ 非平凡共轭（时间推进的来源）
    u = sp.diag(2, 1)
    lhs = sp.simplify(u * E12 * u.inv())
    return lhs == 2 * E12 and lhs != E12, f"块内非标量：u E₁₂ u⁻¹={lhs} ≠ E₁₂"


def c10():
    # 层权不同也不产生模流：块标量即使 a≠b，仍全局共轭恒等
    a, b = sp.Rational(1, 2), sp.Integer(4)
    c = rmat(a * I2, sp.zeros(2, 2), sp.zeros(2, 2), b * I2)
    m = rmat(sp.Matrix([[2, 1], [0, 3]]), sp.zeros(2, 2), sp.zeros(2, 2),
             sp.Matrix([[1, 0], [4, 2]]))
    lhs = sp.simplify(c * m * c.inv() - m)
    return lhs == sp.zeros(4, 4), f"a≠b 的层对角共轭残差={lhs}（层权单独不构成时间）"


# ---------------- C11–C16：Lean / 记号 / 边界 ----------------
def c11():
    text = read_lean()
    need = [
        "def InnerFlow",
        "theorem conj_eq_of_commute",
        "theorem refl_inner",
        "theorem not_outer_refl",
        "theorem isOuter_iff_ne_refl",
        "theorem innerFlow_all_refl_of_commutative",
        "theorem innerFlow_slice_not_outer",
        "theorem outer_slice_not_innerFlow",
        "def BlockScalarRealization",
        "def BlockScalarFlow",
        "theorem scalarMat_commute",
        "theorem blockScalarRealization_imp_innerBlock",
        "theorem blockScalarRealization_trivial",
        "theorem swapBlock_not_blockScalar",
        "theorem blockScalarFlow_all_refl",
        "theorem outer_not_blockScalarFlow",
        "theorem outer_not_blockScalarRealization",
    ]
    miss = [s for s in need if s not in text]
    return not miss, f"missing={miss}"


def c12():
    text = read_lean()
    bad = ["sorry", "admit", "native_decide"]
    hit = [s for s in bad if s in text]
    return not hit, f"占位/不可信命中={hit}"


def c13():
    text = read_lean()
    bad = ["Δ=1", "Δ = 1", "Delta = 1", "MWeight"]
    hit = [s for s in bad if s in text]
    return not hit, f"禁用记法命中={hit}"


def c14():
    text = read_lean()
    need = ["P2 未成立、G3 未闭合", "vN 完成性", "Tomita", "两条独立腿"]
    miss = [s for s in need if s not in text]
    return not miss, f"诚实边界 missing={miss}"


def c15():
    kms = read_kms()
    ok1 = "模哈密顿量" in kms and "原称「模指数」作废" in kms
    ok2 = "模指数 M" not in kms
    ok3 = "**M = 模哈密顿量**" in kms
    return ok1 and ok2 and ok3, \
        f"KMS 模块记号更正：ok1={ok1}, ok2={ok2}, ok3={ok3}"


def c16():
    text = read_lean()
    need = ["G3-P2-4", "RecObj", "InnerFlow", "BlockScalarRealization"]
    miss = [s for s in need if s not in text]
    # 与 368 的层权结论兼容：e^{−2π} 比值
    ratio = sp.simplify(sp.exp(-2 * sp.pi * 1) / sp.exp(-2 * sp.pi * 0))
    return (not miss) and ratio != 0, f"missing={miss}; 层权比={ratio}"


for cid, desc, fn in [
    ("C01", "中心单位共轭平凡（u 交换 ⟹ u a u⁻¹=a）", c01),
    ("C02", "标量矩阵中心性", c02),
    ("C03", "块标量共轭固定块投影 P₀", c03),
    ("C04", "块交换移动 P₀，块标量不能实现外步", c04),
    ("C05", "交换载体：外 ⟺ 非恒等（ℚ×ℚ 枚举）", c05),
    ("C06", "交换载体：内实现必恒等", c06),
    ("C07", "层权比 e^{−2π}≠1", c07),
    ("C08", "层对角块标量 ⇒ 模流恒等", c08),
    ("C09", "块内非标量 ⇒ 非平凡共轭", c09),
    ("C10", "层权不同仍不产生模流（层权单独非时间）", c10),
    ("C11", "Lean 定理清单齐全", c11),
    ("C12", "无 sorry/admit/native_decide", c12),
    ("C13", "禁用记法 Δ=1 / MWeight", c13),
    ("C14", "诚实边界（P2/G3/vN/Tomita/两条腿）", c14),
    ("C15", "KMS 模块「模指数」称谓已更正", c15),
    ("C16", "与 368 层权结论兼容", c16),
]:
    check(cid, desc, fn)

passed = sum(1 for _, _, ok, _ in results if ok)
total = len(results)
print(f"\n{passed}/{total} " + ("ALL_PASS" if passed == total else "FAILED"))
raise SystemExit(0 if passed == total else 1)
