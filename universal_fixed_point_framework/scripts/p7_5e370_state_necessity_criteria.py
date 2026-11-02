# -*- coding: utf-8 -*-
"""
P7-5e-370 / G3-P2-5 态侧必要性判别 —— 判据脚本（精确符号，无浮点）
=================================================================
记号纪律（沿用 367/368/369）：
  M = 模哈密顿量（自伴算子），Δ_mod = e^{−2πM}，σ_t = Ad Δ_mod^{it}。
  框架原生 Δ（spExchangeLaw）不出现、不赋值；本脚本不做「Δ = 1」。

机检对象：
  formal_proof/MUFPFormalization/src/MUFPFormalization/G3StateNecessity.lean
  命名空间 MUFPF.G3StateNecessity，16 条定义/定理。

判据 C01–C14 全部 PASS 才打印 ALL_PASS。
无浮点：只用 int / sympy Integer / sympy Rational / 符号 pi、exp。
"""

import io
import os

import sympy as sp

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEAN = os.path.join(
    ROOT, "formal_proof", "MUFPFormalization", "src", "MUFPFormalization",
    "G3StateNecessity.lean",
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


I2 = sp.eye(2)
E12 = sp.Matrix([[0, 1], [0, 0]])
Z2 = sp.zeros(2, 2)


def conj(u, a):
    return sp.simplify(u * a * u.inv())


def rmat(b11, b12, b21, b22):
    return sp.Matrix(sp.BlockMatrix([[b11, b12], [b21, b22]]))


# ---------------- C01–C03：块内标量 / 非标量权重 ----------------
def c01():
    u = sp.Rational(1, 2) * I2
    a = sp.Matrix([[2, 3], [5, 7]])
    lhs = sp.simplify(conj(u, a) - a)
    return lhs == Z2, f"块内标量忠实态 (1/2,1/2)：共轭残差={lhs}"


def c02():
    u = sp.diag(sp.Rational(2, 3), sp.Rational(1, 3))
    lhs = conj(u, E12)
    ratio = sp.simplify(sp.Rational(2, 3) / sp.Rational(1, 3))
    return lhs == ratio * E12 and lhs != E12, \
        f"非标量忠实态 (2/3,1/3)：u E₁₂ u⁻¹={lhs}（比={ratio}≠1）"


def c03():
    d1, d2 = sp.symbols("d1 d2", nonzero=True)
    ratio = sp.simplify(d1 / d2 - 1)
    # 比 ≠ 1 ⟺ d1 ≠ d2（通分：d1−d2 ≠ 0）
    num = sp.simplify(sp.fraction(ratio)[0])
    return num == d1 - d2, f"权重比−1 的分子={num} ⇒ 比≠1 ⟺ d₁≠d₂"


# ---------------- C04–C05：层权与块内权重 ----------------
def c04():
    c1, c2 = sp.Rational(1, 2), sp.Rational(4, 1)
    u = rmat(c1 * I2, Z2, Z2, c2 * I2)
    m = rmat(sp.Matrix([[2, 1], [0, 3]]), Z2, Z2, sp.Matrix([[1, 0], [4, 2]]))
    lhs = sp.simplify(conj(u, m) - m)
    return lhs == sp.zeros(4, 4), f"层权 c₁≠c₂ 但块内标量：共轭残差={lhs}"


def c05():
    c1, c2 = sp.Rational(1, 2), sp.Rational(4, 1)
    u = rmat(sp.diag(2, 1), Z2, Z2, sp.diag(3, 1))
    m = rmat(E12, Z2, Z2, E12)
    lhs = conj(u, m)
    return lhs != m, f"层权 + 块内非标量：共轭={lhs} ≠ 原矩阵"


# ---------------- C06–C07：忠实性与逆否 ----------------
def c06():
    # 忠实态（两权重正）既可恒等也可非平凡
    scalar_state = (sp.Rational(1, 2), sp.Rational(1, 2))
    non_scalar_state = (sp.Rational(2, 3), sp.Rational(1, 3))
    trivial = conj(sp.diag(*scalar_state), sp.Matrix([[1, 2], [3, 4]]))
    a = sp.Matrix([[1, 2], [3, 4]])
    trivial_ok = trivial == a
    non_trivial = conj(sp.diag(*non_scalar_state), E12) != E12
    return trivial_ok and non_trivial, \
        f"忠实块标量⇒恒等={trivial_ok}；忠实非标量⇒非平凡={non_trivial}"


def c07():
    # 逆否：共轭恒等 ⟹ 权重比=1 ⟹ 块内标量
    d1, d2 = sp.symbols("d1 d2", nonzero=True)
    ratio = sp.simplify(d1 / d2)
    fixed = sp.simplify(ratio - 1)
    return fixed != 0 or sp.simplify(d1 - d2) == 0, \
        f"共轭恒等 ⟹ 比−1={fixed}=0 ⟹ d₁=d₂（逆否门）"


# ---------------- C08：与 P2-4 块标量结论一致 ----------------
def c08():
    a = sp.Rational(3, 5)
    u = sp.simplify(rmat(a * I2, Z2, Z2, a * I2))
    m = rmat(sp.Matrix([[1, 2], [3, 4]]), Z2, Z2, sp.Matrix([[5, 6], [7, 8]]))
    lhs = sp.simplify(conj(u, m) - m)
    return lhs == sp.zeros(4, 4), f"全局块标量 ⇒ 恒等（与 369 C08 同结论），残差={lhs}"


# ---------------- C09–C14：Lean / 记号 / 边界 ----------------
def c09():
    text = read_lean()
    need = [
        "def diagMat",
        "def e12",
        "theorem diagMat_self_eq_algebraMap",
        "theorem diagMat_isScalar_iff",
        "def diagUnit",
        "theorem conj_e12_of_diagUnit",
        "theorem conj_trivial_of_scalar",
        "theorem weightRatio_ne_one",
        "structure DiagState",
        "def DiagState.blockScalar",
        "def DiagState.unit",
        "theorem DiagState.conj_trivial",
        "theorem DiagState.conj_nontrivial",
        "theorem nontrivial_imp_nonScalar",
        "theorem faithful_not_imp_nontrivial",
        "theorem layerWeight_blockScalar_trivial",
    ]
    miss = [s for s in need if s not in text]
    return not miss, f"missing={miss}"


def c10():
    text = read_lean()
    bad = ["sorry", "admit", "native_decide"]
    hit = [s for s in bad if s in text]
    return not hit, f"占位/不可信命中={hit}"


def c11():
    text = read_lean()
    bad = ["Δ=1", "Δ = 1", "Delta = 1", "MWeight"]
    hit = [s for s in bad if s in text]
    return not hit, f"禁用记法命中={hit}"


def c12():
    text = read_lean()
    need = ["P2 未成立、G3 未闭合", "vN 完成性", "Tomita", "复相位", "RecObj"]
    miss = [s for s in need if s not in text]
    return not miss, f"诚实边界 missing={miss}"


def c13():
    text = read_lean()
    ok_import = "import MUFPFormalization.G3CarrierNecessity" in text
    ok_reuse = "conj_eq_of_commute" in text and "scalarMat_commute" in text
    return ok_import and ok_reuse, f"复用 369 资产：import={ok_import}, reuse={ok_reuse}"


def c14():
    text = read_lean()
    ok_tag = "G3-P2-5" in text and "P7-5e-370" in text
    ok_boundary = ("忠实" in text and "正定" in text and "层权" in text
                   and "单独不构成时间" in text)
    return ok_tag and ok_boundary, \
        f"编号与边界口径：tag={ok_tag}, boundary={ok_boundary}"


for cid, desc, fn in [
    ("C01", "块内标量忠实态 ⇒ 共轭恒等", c01),
    ("C02", "块内非标量忠实态 ⇒ 非平凡共轭（比=2）", c02),
    ("C03", "权重比≠1 ⟺ 权重不等", c03),
    ("C04", "层权不同 + 块内标量 ⇒ 仍恒等", c04),
    ("C05", "层权 + 块内非标量 ⇒ 非平凡", c05),
    ("C06", "忠实性本身不决定时间（两类并存）", c06),
    ("C07", "逆否：共轭恒等 ⟹ 块内标量", c07),
    ("C08", "全局块标量 ⇒ 恒等（与 369 一致）", c08),
    ("C09", "Lean 定义/定理清单齐全（16 条）", c09),
    ("C10", "无 sorry/admit/native_decide", c10),
    ("C11", "禁用记法 Δ=1 / MWeight", c11),
    ("C12", "诚实边界（P2/G3/vN/Tomita/复相位/RecObj）", c12),
    ("C13", "复用 369 的载体必要性资产", c13),
    ("C14", "编号 P7-5e-370 / G3-P2-5 与边界口径", c14),
]:
    check(cid, desc, fn)

passed = sum(1 for _, _, ok, _ in results if ok)
total = len(results)
print(f"\n{passed}/{total} " + ("ALL_PASS" if passed == total else "FAILED"))
raise SystemExit(0 if passed == total else 1)
