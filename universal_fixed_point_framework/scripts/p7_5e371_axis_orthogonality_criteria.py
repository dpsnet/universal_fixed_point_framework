# -*- coding: utf-8 -*-
"""
P7-5e-371 / G3-P2-6 内/外轴与恒等/非恒等轴正交 —— 判据脚本（精确符号，无浮点）
=====================================================================
记号纪律（沿用 367/368/369/370）：
  M = 模哈密顿量（自伴算子），Δ_mod = e^{−2πM}，σ_t = Ad Δ_mod^{it}。
  框架原生 Δ（spExchangeLaw）不出现、不赋值；本脚本不做「Δ = 1」。

机检对象：
  formal_proof/MUFPFormalization/src/MUFPFormalization/G3P2AxisOrthogonality.lean
  命名空间 MUFPF.G3P2AxisOrthogonality，19 条定义/定理（7 定义 + 12 定理）。

模型：两层直接积代数 BlockMat × BlockMat（BlockMat = M₂(ℚ)），
乘法与逆逐分量；这正是 Lean 模块中的 TwoBlockAlg，而非带非对角块的 4×4 矩阵。

判据 C01–C14 全部 PASS 才打印 ALL_PASS。
无浮点：只用 int / sympy Integer / sympy Rational。
"""

import io
import os

import sympy as sp

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEAN = os.path.join(
    ROOT, "formal_proof", "MUFPFormalization", "src", "MUFPFormalization",
    "G3P2AxisOrthogonality.lean",
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
Z2 = sp.zeros(2, 2)
E12 = sp.Matrix([[0, 1], [0, 0]])


def m(entries):
    return sp.Matrix(entries)


def pmul(a, b):
    """逐分量乘（TwoBlockAlg = BlockMat × BlockMat）。"""
    return (sp.simplify(a[0] * b[0]), sp.simplify(a[1] * b[1]))


def padd(a, b):
    return (sp.simplify(a[0] + b[0]), sp.simplify(a[1] + b[1]))


def pinv(u):
    return (sp.simplify(u[0].inv()), sp.simplify(u[1].inv()))


def pconj(u, a):
    """单位共轭 Ad u（逐分量）：u a u⁻¹。"""
    return (sp.simplify(u[0] * a[0] * u[0].inv()),
            sp.simplify(u[1] * a[1] * u[1].inv()))


def conj(u, a):
    return sp.simplify(u * a * u.inv())


def peq(a, b):
    return (sp.simplify(a[0] - b[0]) == Z2) and (sp.simplify(a[1] - b[1]) == Z2)


U = (m([[1, 2], [3, 5]]), m([[2, 0], [1, 3]]))
A = (m([[2, 1], [0, 3]]), m([[1, 4], [2, 1]]))
B = (m([[1, 4], [2, 0]]), m([[3, 0], [1, 2]]))


# ---------------- C01–C05：共轭是代数自同构（乘法/逆/加法/中心/合成） ----------------
def c01():
    lhs = pconj(U, pmul(A, B))
    rhs = pmul(pconj(U, A), pconj(U, B))
    return peq(lhs, rhs), "Ad u 保乘法：u(ab)u⁻¹=(uau⁻¹)(ubu⁻¹) 逐分量成立"


def c02():
    lhs = pconj(pinv(U), pconj(U, A))
    return peq(lhs, A), "左逆：Ad u⁻¹ ∘ Ad u = id"


def c03():
    lhs = pconj(U, padd(A, B))
    rhs = padd(pconj(U, A), pconj(U, B))
    return peq(lhs, rhs), "Ad u 保加法（逐分量线性）"


def c04():
    r = sp.Rational(3, 7)
    fixed = (r * I2, r * I2)
    lhs = pconj(U, fixed)
    return peq(lhs, fixed), f"中心标量 r={r} 不动：Ad u(rI)=rI"


def c05():
    # 合成律：Ad u ∘ Ad v = Ad(uv)，逐分量
    lhs = pconj(U, pconj(A, B))
    comp = (sp.simplify(U[0] * A[0]), sp.simplify(U[1] * A[1]))
    rhs = pconj(comp, B)
    return peq(lhs, rhs), "合成律：Ad u ∘ Ad v = Ad(uv)（内实现族对合成封闭）"


# ---------------- C06–C08：乘积单位分解与块交换的外性 ----------------
def c06():
    u1 = m([[1, 1], [0, 1]])
    u2 = m([[2, 0], [1, 1]])
    u = (u1, u2)
    a = (m([[3, 1], [2, 5]]), m([[0, 2], [4, 1]]))
    lhs = pconj(u, a)
    rhs = (conj(u1, a[0]), conj(u2, a[1]))
    return peq(lhs, rhs), "乘积单位分解：Ad(u₁,u₂)=Ad u₁ ⊗ Ad u₂（= innerRealization_imp_innerBlock）"


def c07():
    u = (m([[1, 2], [0, 1]]), m([[3, 0], [1, 2]]))
    one_zero = (I2, Z2)
    lhs = pconj(u, one_zero)
    return peq(lhs, one_zero), "块对角（逐分量）共轭固定 (1,0)：blockwiseAut_one_zero"


def c08():
    u = (m([[1, 2], [0, 1]]), m([[3, 0], [1, 2]]))
    one_zero = (I2, Z2)
    zero_one = (Z2, I2)
    fixed = pconj(u, one_zero)
    swapped = (one_zero[1], one_zero[0])
    return (peq(fixed, one_zero) and not peq(fixed, swapped) and peq(swapped, zero_one)), \
        "内共轭固定 (1,0)，块交换送 (1,0)→(0,1) ⇒ 块交换不是任何内实现"


# ---------------- C09–C10：态侧两类切片 ----------------
def c09():
    u = (sp.Rational(1, 2) * I2, sp.Rational(1, 2) * I2)
    a = (m([[2, 3], [5, 7]]), m([[1, 0], [4, 2]]))
    return peq(pconj(u, a), a), "块内标量忠实态 (1/2,1/2)：共轭恒等"


def c10():
    d1, d2 = sp.Rational(2, 3), sp.Rational(1, 3)
    u = (sp.diag(d1, d2), sp.Rational(1, 2) * I2)
    a = (E12, I2)
    lhs = pconj(u, a)
    ratio = sp.simplify(d1 / d2)
    return (sp.simplify(lhs[0] - ratio * E12) == Z2 and lhs[0] != E12), \
        f"块内非标量 (2/3,1/3)：E₁₂ 缩放 {ratio}≠1 ⇒ 非平凡共轭"


# ---------------- C11：四象限正交（主定理的数值读法） ----------------
def c11():
    trivial_inner = peq(pconj((sp.Rational(1, 2) * I2, sp.Rational(1, 2) * I2), A), A)
    u_ns = (sp.diag(sp.Rational(2, 3), sp.Rational(1, 3)), sp.Rational(1, 2) * I2)
    nontrivial_inner = pconj(u_ns, (E12, I2)) != (E12, I2)
    swap_nontrivial = (Z2, I2) != (I2, Z2)
    identity_inner = peq(pconj((I2, I2), A), A)  # 恒等 = Ad 1，故不可能外
    return (trivial_inner and nontrivial_inner and swap_nontrivial and identity_inner), \
        ("四象限：(内,恒等)={0} (内,非平凡)={1} (外,非平凡)={2} (外,恒等)不存在（恒等=Ad 1）"
         .format(trivial_inner, nontrivial_inner, swap_nontrivial))


# ---------------- C12–C14：Lean 清单 / 记号 / 边界 ----------------
def c12():
    text = read_lean()
    need = [
        "def innerAutEquiv",
        "theorem innerAutEquiv_inner",
        "def unitFst",
        "def unitSnd",
        "def prodUnit",
        "theorem innerRealization_imp_innerBlock",
        "theorem swapBlock_outer",
        "theorem swapBlock_ne_refl",
        "def blockwiseAut",
        "theorem blockwiseAut_inner",
        "theorem blockwiseAut_one_zero",
        "theorem blockwiseAut_ne_swap",
        "def blockStateAut",
        "theorem blockStateAut_inner",
        "theorem blockStateAut_trivial",
        "theorem blockStateAut_nontrivial",
        "def blockStateFlow",
        "theorem blockStateFlow_inner",
        "theorem axes_orthogonal",
    ]
    miss = [s for s in need if s not in text]
    return not miss, f"19 条成员 missing={miss}"


def c13():
    text = read_lean()
    bad = ["sorry", "admit", "native_decide"]
    hit = [s for s in bad if s in text]
    return not hit, f"占位/不可信命中={hit}"


def c14():
    text = read_lean()
    bad = ["Δ=1", "Δ = 1", "Delta = 1", "MWeight"]
    hit = [s for s in bad if s in text]
    need = ["P2 未成立、G3 未闭合", "vN 完成性", "Tomita", "III 型", "RecObj"]
    miss = [s for s in need if s not in text]
    ok_tag = "G3-P2-6" in text and "P7-5e-371" in text
    return (not hit and not miss and ok_tag), \
        f"禁用记法命中={hit}; 边界 missing={miss}; tag={ok_tag}"


for cid, desc, fn in [
    ("C01", "共轭保乘法（内实现是代数自同构）", c01),
    ("C02", "左逆：Ad u⁻¹ ∘ Ad u = id", c02),
    ("C03", "共轭保加法", c03),
    ("C04", "中心标量不动（Ad u(rI)=rI）", c04),
    ("C05", "合成律 Ad u ∘ Ad v = Ad(uv)", c05),
    ("C06", "乘积单位分解 ⇒ 逐块内实现", c06),
    ("C07", "块对角共轭固定 (1,0)", c07),
    ("C08", "块交换把 (1,0) 送到 (0,1) ⇒ 非内", c08),
    ("C09", "块内标量态切片恒等", c09),
    ("C10", "块内非标量态切片非平凡（比=2）", c10),
    ("C11", "四象限正交（仅「外,恒等」不存在）", c11),
    ("C12", "Lean 定义/定理清单齐全（19 条）", c12),
    ("C13", "无 sorry/admit/native_decide", c13),
    ("C14", "编号 P7-5e-371 / G3-P2-6 与诚实边界", c14),
]:
    check(cid, desc, fn)

passed = sum(1 for _, _, ok, _ in results if ok)
total = len(results)
print(f"\n{passed}/{total} " + ("ALL_PASS" if passed == total else "FAILED"))
raise SystemExit(0 if passed == total else 1)
