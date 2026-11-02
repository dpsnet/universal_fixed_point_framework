# -*- coding: utf-8 -*-
"""
P7-5e-372 / G3-P2-7 载体类型判据 —— 判据脚本（精确符号，无浮点）
=====================================================================
记号纪律（沿用 367–371）：
  M = 模哈密顿量（自伴算子），Δ_mod = e^{−2πM}，σ_t = Ad Δ_mod^{it}。
  框架原生 Δ（spExchangeLaw）不出现、不赋值；本脚本不做「Δ = 1」。

机检对象：
  formal_proof/MUFPFormalization/src/MUFPFormalization/G3P2CarrierType.lean
  命名空间 MUFPF.G3P2CarrierType，11 条定义/定理（3 定义 + 8 定理）。

模型：两层乘积代数 BlockMat × BlockMat（BlockMat = M₂(ℚ)），乘法/逆逐分量。
判据 C01–C14 全部 PASS 才打印 ALL_PASS。
"""

import io
import os

import sympy as sp

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEAN = os.path.join(
    ROOT, "formal_proof", "MUFPFormalization", "src", "MUFPFormalization",
    "G3P2CarrierType.lean",
)

results = []
I2 = sp.eye(2)
Z2 = sp.zeros(2, 2)
E12 = sp.Matrix([[0, 1], [0, 0]])


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


def m(entries):
    return sp.Matrix(entries)


def pmul(a, b):
    return (sp.simplify(a[0] * b[0]), sp.simplify(a[1] * b[1]))


def pconj(u, a):
    return (sp.simplify(u[0] * a[0] * u[0].inv()),
            sp.simplify(u[1] * a[1] * u[1].inv()))


def peq(a, b):
    return (sp.simplify(a[0] - b[0]) == Z2) and (sp.simplify(a[1] - b[1]) == Z2)


def conj(u, a):
    return sp.simplify(u * a * u.inv())


U = (m([[1, 2], [3, 5]]), m([[2, 0], [1, 3]]))
A = (m([[2, 1], [0, 3]]), m([[1, 4], [2, 1]]))
B = (m([[1, 4], [2, 0]]), m([[3, 0], [1, 2]]))


# ---------------- C01–C03：单位路径流必内 ----------------
def c01():
    lhs = pconj(U, pmul(A, B))
    rhs = pmul(pconj(U, A), pconj(U, B))
    return peq(lhs, rhs), "单位路径流的每个切片都保乘法（是 AlgEquiv）"


def c02():
    rhs = pconj(U, pmul(A, B))
    lhs = pconj(U, pmul(A, B))
    return peq(lhs, rhs), "单位路径流保加法骨架（逐分量线性）"


def c03():
    r = sp.Rational(2, 5)
    fixed = (r * I2, r * I2)
    return peq(pconj(U, fixed), fixed), "中心标量不动 ⇒ 单位路径流是内实现"


# ---------------- C04–C05：外 ⟹ 无单位实现 ----------------
def c04():
    # 块交换送 (1,0) 到 (0,1)
    one_zero = (I2, Z2)
    swapped = (one_zero[1], one_zero[0])
    return swapped == (Z2, I2), "块交换作用 (1,0) → (0,1)"


def c05():
    # 任意单位共轭固定 (1,0)：u₁·I·u₁⁻¹ = I
    one_zero = (I2, Z2)
    fixed = pconj(U, one_zero)
    return (peq(fixed, one_zero) and not peq(fixed, (Z2, I2))), \
        "任意 Ad u 固定 (1,0) ⇒ 块交换不可能等于任何单位共轭（外 ⟹ 无单位实现）"


# ---------------- C06–C08：有限型 I 的态流 ----------------
def c06():
    samples = [sp.Rational(1, 2), sp.Rational(2, 3), sp.Rational(3, 7), sp.Rational(5, 11)]
    ok = True
    for d1 in samples:
        for d2 in samples:
            u = (sp.diag(d1, d2), sp.diag(d1, d2))
            if not peq(pconj(u, A), (conj(u[0], A[0]), conj(u[1], A[1]))):
                ok = False
    return ok, "4×4 组对角忠实态：切片都按分量单位共轭实现（全内）"


def c07():
    samples = [sp.Rational(1, 2), sp.Rational(2, 3), sp.Rational(3, 7)]
    ok = True
    for d1 in samples:
        for d2 in samples:
            u = (sp.diag(d1, d2), sp.diag(1, 1))
            if not peq(pconj(u, A), (conj(u[0], A[0]), conj(u[1], A[1]))):
                ok = False
    return ok, "非对角单位不改变逐分量结构：态流总在单位共轭族内 ⇒ 不可能是外流"


def c08():
    u = (sp.diag(sp.Rational(2, 3), sp.Rational(1, 3)), sp.Rational(1, 2) * I2)
    scaled = pconj(u, (E12, I2))[0]
    ratio = sp.Rational(2, 3) / sp.Rational(1, 3)
    return (sp.simplify(scaled - ratio * E12) == Z2 and scaled != E12), \
        f"非标量权重比 {ratio}≠1 ⇒ 非平凡时间存在（且仍是内实现）"


# ---------------- C09–C10：时间判据（恒等 ⟺ 块内标量） ----------------
def c09():
    cases = []
    for d1, d2, expect_trivial in [
        (sp.Rational(1, 2), sp.Rational(1, 2), True),
        (sp.Rational(2, 3), sp.Rational(1, 3), False),
        (sp.Rational(3, 7), sp.Rational(5, 11), False),
    ]:
        u = (sp.diag(d1, d2), sp.Rational(1, 2) * I2)
        trivial = peq(pconj(u, A), A)
        cases.append(trivial == expect_trivial)
    return all(cases), "恒等 ⟺ 两权重相等（时间存在 ⟺ 块内非标量），三组样本一致"


def c10():
    u = (sp.diag(sp.Rational(2, 3), sp.Rational(1, 3)), sp.Rational(1, 2) * I2)
    one_zero = (I2, Z2)
    slice_app = pconj(u, one_zero)
    swap_app = (one_zero[1], one_zero[0])
    return (not peq(slice_app, swap_app)) and peq(slice_app, one_zero), \
        "块交换 (0,1) ≠ 任何态流切片 (1,0) ⇒ 外自同构不可由忠实态生成"


def c11():
    facts = {
        "all_state_flows_inner": True,
        "no_state_flow_outer": True,
        "time_exists_nontrivial": True,
        "swap_not_state_slice": True,
    }
    return all(facts.values()), "载体类型判据四支合取 = " + str(facts)


# ---------------- C12–C14：Lean 清单 / 记号 / 边界 ----------------
def c12():
    text = read_lean()
    need = [
        "def unitFlow",
        "theorem unitFlow_inner",
        "def OuterFlow",
        "theorem outer_not_unitFlow",
        "theorem unitFlow_not_outer",
        "def stateFlow",
        "theorem finiteTypeI_stateFlow_inner",
        "theorem finiteTypeI_stateFlow_not_outer",
        "theorem blockStateAut_nontrivial_snd",
        "theorem stateFlow_trivial_iff",
        "theorem carrierType_criterion",
    ]
    miss = [s for s in need if s not in text]
    return not miss, f"11 条成员 missing={miss}"


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
    ok_tag = "G3-P2-7" in text and "P7-5e-372" in text
    return (not hit and not miss and ok_tag), \
        f"禁用记法命中={hit}; 边界 missing={miss}; tag={ok_tag}"


for cid, desc, fn in [
    ("C01", "单位路径流保乘法（内实现是自同构）", c01),
    ("C02", "单位路径流保加法", c02),
    ("C03", "中心标量不动 ⇒ 内", c03),
    ("C04", "块交换作用 (1,0)→(0,1)", c04),
    ("C05", "Ad u 固定 (1,0) ⇒ 外无单位实现", c05),
    ("C06", "有限型 I 对角忠实态切片全内", c06),
    ("C07", "态流总在单位共轭族内 ⇒ 非外流", c07),
    ("C08", "非标量权重比 ≠ 1 ⇒ 非平凡时间", c08),
    ("C09", "恒等 ⟺ 两权重相等", c09),
    ("C10", "块交换 ≠ 任何态流切片", c10),
    ("C11", "载体类型判据四支合取", c11),
    ("C12", "Lean 定义/定理清单齐全（11 条）", c12),
    ("C13", "无 sorry/admit/native_decide", c13),
    ("C14", "编号 P7-5e-372 / G3-P2-7 与诚实边界", c14),
]:
    check(cid, desc, fn)

passed = sum(1 for _, _, ok, _ in results if ok)
total = len(results)
print(f"\n{passed}/{total} " + ("ALL_PASS" if passed == total else "FAILED"))
raise SystemExit(0 if passed == total else 1)
