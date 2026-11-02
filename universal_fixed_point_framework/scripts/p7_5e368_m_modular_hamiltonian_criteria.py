# -*- coding: utf-8 -*-
"""
P7-5e-368 / G3-P1b-3 真逆向 —— 判据脚本（精确符号，无浮点）
================================================================
更正后的记号（用户 2026-11-02 澄清）：
  M = 模哈密顿量（自伴算子），Δ_mod = e^{−2πM}，σ_t = Ad Δ_mod^{it} = Ad e^{−2πitM}。
  M 不是标量「模指数」；「M=1」读作「模哈密顿量在层塔上的相邻谱间隔归一为 1」。
  框架原生 Δ（spExchangeLaw）不出现、不赋值。

机检对象：
  scripts/../formal_proof/MUFPFormalization/src/MUFPFormalization/G3P1b3ConverseModular.lean
  命名空间 MUFPF.G3P1b3Converse，14 条定理/定义。

判据 C01–C16 全部 PASS 才打印 ALL_PASS。
无浮点：只用 int / sympy Integer / sympy Rational / 符号 pi、exp。
"""

import io
import os

import sympy as sp

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEAN = os.path.join(
    ROOT, "formal_proof", "MUFPFormalization", "src", "MUFPFormalization",
    "G3P1b3ConverseModular.lean",
)

gap, n, m, k = sp.symbols("gap n m k", integer=True)
gap_r = sp.symbols("gap", real=True)

results = []


def check(cid, desc, fn):
    try:
        ok, detail = fn()
    except Exception as exc:  # noqa: BLE001
        ok, detail = False, f"EXC {type(exc).__name__}: {exc}"
    results.append((cid, desc, bool(ok), detail))
    print(f"[{cid}] {'PASS' if ok else 'FAIL'} — {desc} :: {detail}")


def w(g, idx):
    return sp.exp(-2 * sp.pi * g * idx)


# ---------------- C01–C06：模权代数 ----------------
def c01():
    lhs = sp.simplify(w(gap_r, 0) - 1)
    return lhs == 0, f"w(0)=1, residual={lhs}"


def c02():
    lhs = sp.simplify(w(gap_r, n + 1) - w(gap_r, n) * sp.exp(-2 * sp.pi * gap_r))
    return lhs == 0, "w(n+1)=w(n)·e^{−2π·gap}"


def c03():
    lhs = sp.simplify(w(gap_r, n + k) - w(gap_r, n) * w(gap_r, k))
    return lhs == 0, "w(n+k)=w(n)·w(k)"


def c04():
    sol = sp.solve(sp.Eq(-2 * sp.pi * gap_r * n, -2 * sp.pi * gap_r * m), n)
    return sol == [m], f"exponent equality ⇒ n∈{sol}（gap≠0 时 n=m）"


def c05():
    lhs = sp.simplify(w(0, n) - 1)
    return lhs == 0, "gap=0 ⇒ 全部层权坍缩为 1（单射失效）"


def c06():
    one = sp.simplify(w(1, 1) - sp.exp(-2 * sp.pi))
    ratio = sp.simplify(w(1, n + 1) / w(1, n) - sp.exp(-2 * sp.pi))
    return one == 0 and ratio == 0, "gap=1 ⇒ w(1)=e^{−2π}，层权比=e^{−2π}（367 数值结论不变）"


# ---------------- C07–C08：单向层步 ----------------
def c07():
    failures = []
    for kk in range(0, 5):
        for start in range(0, 4):
            for steps in range(0, 6):
                cur = start
                for _ in range(steps):
                    cur = cur + kk
                if cur != start + steps * kk:
                    failures.append((kk, start, steps, cur))
    return not failures, f"显式迭代 0..5 步 × k∈0..4 × n∈0..3 全等于 n+m·k（failures={failures}）"


def c08():
    sol = sp.solve(sp.Eq(n + m * k, n), m)
    return sol == [0], f"n+m·k=n ⇒ m∈{sol}（k≠0 时 m=0，无回退）"


# ---------------- C09–C10：刚性 / 反例 ----------------
LAYERS = [0, 1, 2]


def c09():
    from itertools import permutations
    bad = []
    for perm in permutations(LAYERS):
        tau = {i: perm[i] for i in LAYERS}
        if all(sp.simplify(w(1, tau[i]) - w(1, i)) == 0 for i in LAYERS):
            if tau != {i: i for i in LAYERS}:
                bad.append(tau)
    return not bad, f"3 层权互异：仅恒等置换保全部层权（反例={bad}）"


def c10():
    tau = {0: 1, 1: 2, 2: 0}
    cur = dict(tau)
    for _ in range(2):
        cur = {i: tau[cur[i]] for i in LAYERS}
    returns = cur == {i: i for i in LAYERS}
    moves = all(sp.simplify(w(1, tau[i]) - w(1, i)) != 0 for i in LAYERS)
    return returns and moves and tau != {i: i for i in LAYERS}, (
        "三阶循环：τ³=id、τ≠id、且每层模权都改变 ⇒ 非平凡/权重移动 ⇏ 无周期"
    )


# ---------------- C11–C16：Lean 资产与口径审计 ----------------
def read_lean():
    with io.open(LEAN, "r", encoding="utf-8") as fh:
        return fh.read()


def c11():
    text = read_lean()
    need = ["模哈密顿量", "Δ_mod", "modularWeight", "谱间隔"]
    miss = [s for s in need if s not in text]
    banned = ["模指数"]
    hit = [s for s in banned if s in text]
    return not miss and not hit, f"missing={miss}, banned_hit={hit}"


def c12():
    text = read_lean()
    bad = ["Δ=1", "Δ = 1", "Delta = 1", "MWeight"]
    hit = [s for s in bad if s in text]
    return not hit, f"禁用记法命中={hit}"


def c13():
    text = read_lean()
    bad = ["sorry", "admit", "native_decide"]
    hit = [s for s in bad if s in text]
    return not hit, f"占位/不可信命中={hit}"


def c14():
    text = read_lean()
    need = [
        "theorem modularWeight_injective",
        "theorem weight_perm_rigid",
        "theorem advanceIter_no_return",
        "theorem outer_moves_modular_weight",
        "theorem modularWeight_unit_gap",
        "theorem bnotEquiv_period_two",
        "theorem isOuter_of_layer_shift",
        "theorem outer_not_diagonal",
    ]
    miss = [s for s in need if s not in text]
    return not miss, f"missing={miss}"


def c15():
    text = read_lean()
    need = ["模流本身是周期的", "σ_{t+1} = σ_t", "递归层深"]
    miss = [s for s in need if s not in text]
    return not miss, f"诚实边界 missing={miss}"


def c16():
    # 367 兼容性：Δ_mod = e^{−2πM} 在单位谱（M=N）下逐层为 e^{−2πn}
    lhs = sp.simplify(sp.exp(-2 * sp.pi * 1 * n) - w(1, n))
    return lhs == 0, "Δ_mod=e^{−2πM}, spec(M)=ℤ ⇒ 层权 e^{−2πn}（与 367 一致）"


for cid, desc, fn in [
    ("C01", "模权第 0 层归一", c01),
    ("C02", "相邻层权比 e^{−2π·gap}", c02),
    ("C03", "层权加法分解", c03),
    ("C04", "谱间隔≠0 ⇒ 层权单射", c04),
    ("C05", "gap=0 退化", c05),
    ("C06", "单位谱间隔 ⇒ e^{−2π}", c06),
    ("C07", "单向迭代闭式", c07),
    ("C08", "单向无回退", c08),
    ("C09", "层权刚性（保权置换=恒等）", c09),
    ("C10", "非平凡/周期反例（外 ⇏ 无周期）", c10),
    ("C11", "Lean 记号：M=模哈密顿量", c11),
    ("C12", "禁用记法 Δ=1/MWeight", c12),
    ("C13", "无 sorry/admit", c13),
    ("C14", "定理清单齐全", c14),
    ("C15", "模流周期性与深度单向边界", c15),
    ("C16", "与 367 数值结论兼容", c16),
]:
    check(cid, desc, fn)

passed = sum(1 for _, _, ok, _ in results if ok)
total = len(results)
print(f"\n{passed}/{total} " + ("ALL_PASS" if passed == total else "FAILED"))
raise SystemExit(0 if passed == total else 1)
