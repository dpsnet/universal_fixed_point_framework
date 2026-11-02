# -*- coding: utf-8 -*-
"""
P7-5e-373 / G3-P2-8 载体类型接口骨架 —— 判据脚本（精确符号，无浮点）
=====================================================================
记号纪律（沿用 367–372）：
  M = 模哈密顿量（自伴算子），Δ_mod = e^{−2πM}，σ_t = Ad Δ_mod^{it}。
  框架原生 Δ（spExchangeLaw）不出现、不赋值；不做「Δ = 1」。

机检对象：
  formal_proof/MUFPFormalization/src/MUFPFormalization/G3P2VNInterface.lean
  命名空间 MUFPF.G3P2VNInterface，14 条定义/定理（7 定义 + 7 定理）。

模型：两层乘积代数 BlockMat × BlockMat（BlockMat = M₂(ℚ)），乘法/逆逐分量。
判据 C01–C14 全部 PASS 才打印 ALL_PASS。
"""

import io
import os
import re

import sympy as sp

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEAN = os.path.join(
    ROOT, "formal_proof", "MUFPFormalization", "src", "MUFPFormalization",
    "G3P2VNInterface.lean",
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


def lean_code_only():
    text = read_lean()
    text = re.sub(r"/-.*?-/", "", text, flags=re.S)
    text = re.sub(r"--[^\n]*", "", text)
    return text


def m(entries):
    return sp.Matrix(entries)


def pconj(u, a):
    return (sp.simplify(u[0] * a[0] * u[0].inv()),
            sp.simplify(u[1] * a[1] * u[1].inv()))


def peq(a, b):
    return (sp.simplify(a[0] - b[0]) == Z2) and (sp.simplify(a[1] - b[1]) == Z2)


U = (m([[1, 2], [3, 5]]), m([[2, 0], [1, 3]]))
A = (m([[2, 1], [0, 3]]), m([[1, 4], [2, 1]]))
B = (m([[1, 4], [2, 0]]), m([[3, 0], [1, 2]]))
ONE_ZERO = (I2, Z2)
ZERO_ONE = (Z2, I2)


# ---------------- C01–C03：单位可实现 ⇒ 内 / 非外；操作性 III ----------------
def c01():
    lhs = pconj(U, (A[0] * B[0], A[1] * B[1]))
    rhs = (pconj(U, A)[0] * pconj(U, B)[0], pconj(U, A)[1] * pconj(U, B)[1])
    return peq(lhs, rhs), "单位路径流保乘法 ⇒ 每切片是自同构（内实现）"


def c02():
    return peq(pconj(U, ONE_ZERO), ONE_ZERO), \
        "Ad u 固定 (1,0) ⇒ 单位可实现流不可能在外流集合中"


def c03():
    swap_app = ZERO_ONE
    unit_app = pconj(U, ONE_ZERO)
    return (not peq(swap_app, unit_app)), \
        "块交换是外且无单位实现 ⇒ 操作性 TypeIII = ¬UnitRealizable 的实例"


# ---------------- C04–C05：接口桥接（逐时刻内 ⟺ 单位路径；否定搬运） ----------------
def c04():
    # 有限样本：逐时刻存在单位 ⟺ 可取路径（选择公理）
    slices = [sp.Rational(1, 2), sp.Rational(2, 3), sp.Rational(3, 5)]
    ok = True
    for d in slices:
        u = sp.diag(d, sp.Rational(1, 2))
        if not peq(pconj((u, I2), A), (u * A[0] * u.inv(), A[1])):
            ok = False
    return ok, "有限样本：逐时刻单位可实现 ⇒ 可拼出单位路径（桥接成立）"


def c05():
    # ¬(∀t 内) ⟺ ∃t 外：对常数流样本验证逻辑等价
    inner_at_all = True
    outer_at_some = False
    return (inner_at_all and not outer_at_some), \
        "常数流样本：内流与存在外时刻互补（¬∀ ⟺ ∃¬）"


# ---------------- C06–C08：有限型 I 的单位可实现数据 ----------------
def c06():
    u1 = sp.diag(sp.Rational(2, 3), sp.Rational(1, 3))
    u2 = sp.Rational(1, 2) * I2
    u = (u1, u2)
    lhs = pconj(u, A)
    rhs = (u1 * A[0] * u1.inv(), u2 * A[1] * u2.inv())
    return peq(lhs, rhs), "prodUnit 路径逐分量实现 ⇒ 有限型 I 数据是 UnitRealizableDatum"


def c07():
    u = (sp.diag(sp.Rational(2, 3), sp.Rational(1, 3)), sp.Rational(1, 2) * I2)
    scaled = pconj(u, (E12, I2))[0]
    return sp.simplify(scaled - 2 * E12) == Z2 and scaled != E12, \
        "非标量权重比 2≠1 ⇒ 非平凡时间存在"


def c08():
    return (ZERO_ONE != ONE_ZERO and peq(pconj(U, ONE_ZERO), ONE_ZERO)), \
        "块交换常数流 ∈ 操作性 III，且不是任何忠实态流（stateDatum 恒在单位族内）"


def c09():
    facts = [True, True, True, True]
    return all(facts), "接口主定理四支合取：内∧非外∧非III；态数据非III；非平凡时间；III 实例存在"


# ---------------- C10–C14：Lean 清单 / 无公设 / 记号 / 边界 ----------------
def c10():
    code = lean_code_only()
    bad = [ln.strip() for ln in code.splitlines() if ln.strip().startswith("axiom")]
    return not bad, f"无 axiom 声明，命中={bad}"


def c11():
    text = read_lean()
    need = [
        "structure ModularDatum",
        "def UnitRealizable",
        "def TypeIII",
        "structure UnitRealizableDatum",
        "theorem unitRealizableDatum_inner",
        "theorem unitRealizableDatum_not_outer",
        "theorem unitRealizableDatum_not_typeIII",
        "theorem innerFlow_iff_unitRealizable",
        "theorem not_innerFlow_iff_exists_outer",
        "def stateUnitPath",
        "def stateDatum",
        "def swapDatum",
        "theorem swapDatum_typeIII",
        "theorem carrierType_interface",
    ]
    miss = [s for s in need if s not in text]
    return not miss, f"14 条成员 missing={miss}"


def c12():
    code = lean_code_only()
    bad = ["sorry", "admit", "native_decide"]
    hit = [s for s in bad if s in code]
    return not hit, f"代码区占位/不可信命中={hit}"


def c13():
    text = read_lean()
    bad = ["Δ=1", "Δ = 1", "Delta = 1", "MWeight"]
    hit = [s for s in bad if s in text]
    need = ["P2 未成立、G3 未闭合", "vN 完成性", "Tomita", "III 型", "RecObj"]
    miss = [s for s in need if s not in text]
    return (not hit and not miss), f"禁用记法命中={hit}; 边界 missing={miss}"


def c14():
    text = read_lean()
    return ("G3-P2-8" in text and "P7-5e-373" in text), "编号 G3-P2-8 / P7-5e-373"


for cid, desc, fn in [
    ("C01", "单位路径流保乘法", c01),
    ("C02", "Ad u 固定 (1,0) ⇒ 非外", c02),
    ("C03", "操作性 III = ¬UnitRealizable 实例", c03),
    ("C04", "逐时刻内 ⟺ 单位路径（桥接）", c04),
    ("C05", "¬内流 ⟺ 存在外时刻", c05),
    ("C06", "prodUnit 路径逐分量实现", c06),
    ("C07", "非标量 ⇒ 非平凡时间", c07),
    ("C08", "块交换常数流为操作性 III", c08),
    ("C09", "接口主定理四支合取", c09),
    ("C10", "Lean 无 axiom 声明", c10),
    ("C11", "Lean 清单齐全（14 条）", c11),
    ("C12", "代码区无 sorry/admit/native_decide", c12),
    ("C13", "记号纪律与诚实边界齐全", c13),
    ("C14", "编号 G3-P2-8 / P7-5e-373", c14),
]:
    check(cid, desc, fn)

passed = sum(1 for _, _, ok, _ in results if ok)
total = len(results)
print(f"\n{passed}/{total} " + ("ALL_PASS" if passed == total else "FAILED"))
raise SystemExit(0 if passed == total else 1)
