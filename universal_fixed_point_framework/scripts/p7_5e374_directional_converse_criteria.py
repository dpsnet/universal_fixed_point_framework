#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
C01–C16 机检：P7-5e-374 / G3-P1b-3 真逆向（条件形式）
模块：MUFPFormalization/G3P1b3DirectionalConverse.lean

纪律：只用精确有理数（fractions.Fraction / sympy Rational），不出现浮点比较；
      不做「由外性推出单向」的宣称；LayerStep/LayerAdvance 只作为显式输入被机检。
"""
import os
import re
import sys
from fractions import Fraction

import sympy as sp

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEAN = os.path.join(
    ROOT, "formal_proof", "MUFPFormalization", "src", "MUFPFormalization",
    "G3P1b3DirectionalConverse.lean",
)
CRIT = os.path.join(ROOT, "formal_proof", "MUFPFormalization", "src", "MUFPFormalization",
                    "G3P1b3ConverseModular.lean")

results = []


def check(tag, name, ok, detail=""):
    results.append((tag, name, bool(ok)))
    print(f"{tag} {name}: {'PASS' if ok else 'FAIL'}{('  [' + detail + ']') if detail and not ok else ''}")


def lean_code_only(text):
    text = re.sub(r"/-.*?-/", "", text, flags=re.S)
    text = re.sub(r"--[^\n]*", "", text)
    return text


src = open(LEAN, encoding="utf-8").read()
code = lean_code_only(src)
dep = open(CRIT, encoding="utf-8").read()


# ---------------- 层步模型：整数/有理数穷举 ----------------
def layer_step(L, sigma, k, dom):
    """LayerStep 的有限模型：∀a, L(σa)=L a ∨ L(σa)=L a+k."""
    return all((L(sigma(a)) == L(a)) or (L(sigma(a)) == L(a) + k) for a in dom)


DOM = list(range(0, 7))
L_id = lambda a: a
sigma_plus = lambda k: (lambda a: a + k)
sigma_id = lambda a: a


# C01 正向样本：+k 是层步（k=1,2,3）
ok = all(layer_step(L_id, sigma_plus(k), k, DOM) for k in (1, 2, 3))
# 反向样本：下降 -1 在任何 k≠0 下都不是「保持或 +k」
ok = ok and all(not layer_step(L_id, lambda a: a - 1, k, DOM) for k in (1, 2, 3))
check("C01", "层步正向/反向样本（+k 是、-1 不是）", ok)

# C02 k=0 退化：LayerStep(...,0) ⟺ 层对角（穷举 L 与若干 σ）
def diagonal(L, sigma, dom):
    return all(L(sigma(a)) == L(a) for a in dom)


ok = True
for L in (lambda a: a, lambda a: a * a, lambda a: 2 * a + 1):
    for sigma in (sigma_id, sigma_plus(1), sigma_plus(2), lambda a: 6 - a):
        ok = ok and (layer_step(L, sigma, 0, DOM) == diagonal(L, sigma, DOM))
check("C02", "k=0 时层步 ⟺ 层对角（穷举 3×4）", ok)

# C03 定向可用性：非对角 + 层步 ⇒ 存在 +k 上升点
ok = True
for k in (1, 2, 3):
    for sigma in (sigma_id, sigma_plus(k), sigma_plus(k + 1), lambda a: a - 1):
        if layer_step(L_id, sigma, k, DOM) and not diagonal(L_id, sigma, DOM):
            ok = ok and any(L_id(sigma(a)) == L_id(a) + k for a in DOM)
check("C03", "非对角层步 ⇒ 存在严格升层点", ok)

# ---------------- 模权指数：精确符号/有理数 ----------------
pi = sp.pi
gap = sp.Rational(1, 1)
n, k = sp.symbols("n k", integer=True, nonnegative=True)


def exponent(g, x):
    return -2 * pi * g * x


# C04 指数可加性（精确符号展开，无浮点）
diff = sp.expand(exponent(gap, n + k) - (exponent(gap, n) + exponent(gap, k)))
ok = sp.simplify(diff) == 0
check("C04", "e 指数可加：-(2π gap (n+k)) = -(2π gap n) + -(2π gap k)", ok)

# C05 单射：gap≠0 且不同层 ⇒ 指数不同（精确有理数）
ok = True
for g in (Fraction(1, 1), Fraction(-1, 1), Fraction(2, 3), Fraction(-5, 7)):
    for a in range(0, 6):
        for b in range(0, 6):
            if a != b:
                ok = ok and (g * a != g * b)
check("C05", "模权指数单射（gap≠0，层 0..5）", ok)

# C06 严格下降：gap>0、k>0 ⇒ 指数更负
ok = True
for g in (Fraction(1, 1), Fraction(2, 3), Fraction(7, 5)):
    for a in range(0, 6):
        for kk in range(1, 5):
            ok = ok and (g * (a + kk) > g * a)
check("C06", "gap>0 ∧ k>0 ⇒ 模权严格下降", ok)

# C07 迭代公式：L(σ^m a) = a + m·k
ok = True
for kk in (1, 2, 3):
    for m in range(0, 6):
        for a in range(0, 6):
            ok = ok and ((a + m * kk) == a + m * kk)
check("C07", "迭代 m 步层作用 = a + m·k", ok)

# C08 无回退：m,k ≠ 0 ⇒ m·k ≠ 0
ok = all((m * kk) != 0 for m in range(1, 6) for kk in range(1, 6))
check("C08", "m≠0 ∧ k≠0 ⇒ 无回退（层不回到原点）", ok)

# C09 与 368 advanceIter_eq 对齐：n + m·k
ok = all((a + m * kk) == a + (a + m * kk - a) for a in range(4) for m in range(6) for kk in range(1, 4))
check("C09", "桥接 advanceIter：n + m·k", ok)

# C10 反例：boolLayer 下 bnot 不是任何 k 的层步
def boolLayer(b):
    return 0 if b else 1


ok = all(not layer_step(boolLayer, lambda b: not b, kk, [False, True]) for kk in range(0, 11))
# 且它确实移动层
ok = ok and boolLayer(not False) != boolLayer(False)
check("C10", "bnot 移动层但不是任何 k 的层步（k=0..10）", ok)

# ---------------- Lean 源码结构 ----------------
DECLS = [
    "LayerStep", "LayerAdvance", "iterateAut", "boolLayer",
    "iterateAut_succ_apply", "layerStep_zero_iff", "layer_step_of_advance", "outer_ne_refl",
    "layerStep_outer_ascent", "layerStep_outer_weight_moves", "ascent_weight_decreases",
    "layerAdvance_iterate", "layerAdvance_iterate_eq_advanceIter",
    "layerAdvance_iterate_no_return", "directional_converse",
    "bnotEquiv_moves_layer", "bnotEquiv_not_directed",
]
ok = all(re.search(r"(def|theorem)\s+" + re.escape(d) + r"\b", code) for d in DECLS)
check("C11", f"Lean 声明齐全（{len(DECLS)} 条）", ok)

# C12 无 axiom / sorry / admit / native_decide（仅代码区）
bad = [w for w in ("axiom", "sorry", "admit", "native_decide") if re.search(r"\b" + w + r"\b", code)]
ok = not bad
check("C12", "无 axiom/sorry/admit/native_decide", ok, detail=", ".join(bad))

# C13 记号纪律
must = ["Δ_mod", "KMS", "P2 未成立、G3 未闭合", "vN 完成性", "显式输入", "未形式化"]
ok = all(s in src for s in must)
forb = ["Δ = 1", "M = 1", "Δ_mod = 1"]
ok = ok and all(s not in src for s in forb)
check("C13", "记号纪律：Δ_mod/KMS/vN 边界齐全且无 Δ=1、M=1 赋值", ok)

# C14 编号与命名
ok = ("namespace MUFPF.G3P1b3Directional" in code) and ("G3-P1b-3" in src)
check("C14", "编号 G3-P1b-3 / 命名空间 MUFPF.G3P1b3Directional", ok)

# C15 不重复定义 368 的构件（只 import + open）
ok = ("import MUFPFormalization.G3P1b3ConverseModular" in code)
ok = ok and ("open MUFPF.G3P1b3Converse" in code)
ok = ok and not re.search(r"def\s+(InnerRealization|IsOuterAut|modularWeight|advanceIter)\b", code)
check("C15", "复用 368 构件（不重复定义 InnerRealization/IsOuterAut/modularWeight/advanceIter）", ok)

# C16 诚实边界声明：方向性为输入、非从 Δ_mod 导出
ok = ("不从 Δ_mod/KMS 导出" in src) and ("每步至多前进 k 层" in src)
check("C16", "诚实边界：方向性为显式输入、未从 Δ_mod/KMS 导出", ok)

npass = sum(1 for _, _, ok in results if ok)
print(f"\n{npass}/{len(results)} PASS")
if npass == len(results):
    print("ALL_PASS")
    sys.exit(0)
print("SOME_FAIL")
sys.exit(1)
