#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
C01–C14 机检：P7-5e-375 / G3-P1b-3 层步输入强度校准
模块：MUFPFormalization/G3P1b3LayerStepInstance.lean

纪律：只用整数/精确符号，不出现浮点比较；不宣称由外性推出单向。
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEAN = os.path.join(
    ROOT, "formal_proof", "MUFPFormalization", "src", "MUFPFormalization",
    "G3P1b3LayerStepInstance.lean",
)

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

DOM = list(range(0, 5))
L_id = lambda a: a


def layer_step(L, sigma, k, dom):
    return all((L(sigma(a)) == L(a)) or (L(sigma(a)) == L(a) + k) for a in dom)


def layer_advance(L, sigma, k, dom):
    return all(L(sigma(a)) == L(a) + k for a in dom)


# C01 弱性：恒等是任意 k 的层步
ok = all(layer_step(L_id, lambda a: a, k, DOM) for k in range(0, 6))
check("C01", "恒等是任意 k 的层步（k=0..5，层 0..4）", ok)

# C02 非对角层步 ⇒ 存在升层点（穷举 4 个 σ × k=1..3）
ok = True
for k in (1, 2, 3):
    for sigma in (lambda a: a, lambda a: a + k, lambda a: a + k + 1, lambda a: a - 1):
        if layer_step(L_id, sigma, k, DOM) and any(sigma(a) != a for a in DOM):
            ok = ok and any(L_id(sigma(a)) == L_id(a) + k for a in DOM)
check("C02", "非对角层步 ⇒ 存在严格升层点", ok)

# C03 外性不可去：σ=id、k=1 是反例（层步成立但无升层点）
ok = layer_step(L_id, lambda a: a, 1, DOM) and not any(
    L_id((lambda a: a)(a)) == L_id(a) + 1 for a in DOM)
check("C03", "反例 σ=id,k=1：层步成立但无升层（外性不可去）", ok)

# C04 非空性：advance k 同时是 LayerStep 与 LayerAdvance
ok = all(layer_step(L_id, lambda a, kk=k: a + kk, k, DOM) for k in range(0, 6))
ok = ok and all(layer_advance(L_id, lambda a, kk=k: a + kk, k, DOM) for k in range(0, 6))
check("C04", "非空性：advance k 是层步且是强制前进（k=0..5）", ok)

# C05 强制前进对恒等失败（k≠0）
ok = all(not layer_advance(L_id, lambda a: a, k, DOM) for k in range(1, 6))
check("C05", "LayerAdvance 对恒等失败（k=1..5）", ok)

# C06 无有限阶：迭代 m 步后层值 ≠ 原层（k,m 1..5）
ok = True
for k in range(1, 6):
    for m in range(1, 6):
        for a in range(0, 4):
            x = a
            for _ in range(m):
                x = x + k
            ok = ok and (x != a)
check("C06", "强制前进 ⇒ m 步不回原层（k,m=1..5）", ok)

# C07 bnot 不是任何非零 k 的 LayerAdvance
def boolLayer(b):
    return 0 if b else 1


ok = all(not layer_advance(boolLayer, lambda b: not b, k, [False, True]) for k in range(1, 6))
check("C07", "bnot 不是任何非零 k 的强制前进（k=1..5）", ok)

# C08 对照：bnot 二阶（bnot^2 = id），与 C06 的「无有限阶」互斥
ok = all((lambda b: not not b)(b) == b for b in (False, True))
check("C08", "bnot 是二阶置换（bnot²=id）——与强制前进不相容", ok)

# ---- Lean 源码结构 ----
DECLS = [
    "layerStep_refl", "layerStep_nondiag_ascent", "not_layerStep_imp_ascent",
    "layerStep_advance", "layerAdvance_advance", "layerAdvance_not_refl",
    "layerAdvance_no_power_refl", "bnotEquiv_not_layerAdvance", "input_necessity",
]
ok = all(re.search(r"theorem\s+" + re.escape(d) + r"\b", code) for d in DECLS)
check("C09", f"Lean 声明齐全（{len(DECLS)} 条定理）", ok)

bad = [w for w in ("axiom", "sorry", "admit", "native_decide") if re.search(r"\b" + w + r"\b", code)]
check("C10", "无 axiom/sorry/admit/native_decide", not bad, detail=", ".join(bad))

must = ["Δ_mod", "KMS", "P2 未成立、G3 未闭合", "vN 完成性", "未形式化", "外性不可去"]
ok = all(s in src for s in must)
forb = ["Δ = 1", "M = 1", "Δ_mod = 1"]
ok = ok and all(s not in src for s in forb)
check("C11", "记号纪律：边界齐全且无 Δ=1、M=1 赋值", ok)

ok = ("namespace MUFPF.G3P1b3Witness" in code) and ("G3-P1b-3" in src)
check("C12", "编号 G3-P1b-3 / 命名空间 MUFPF.G3P1b3Witness", ok)

ok = ("import MUFPFormalization.G3P1b3DirectionalConverse" in code)
ok = ok and ("open MUFPF.G3P1b3Converse MUFPF.G3P1b3Directional" in code)
ok = ok and not re.search(r"(def|theorem)\s+(LayerStep|LayerAdvance|iterateAut|boolLayer)\b", code)
check("C13", "复用 374/368 构件（不重复定义 LayerStep/LayerAdvance/iterateAut/boolLayer）", ok)

ok = ("LayerStep` **单独很弱**" in src) and ("外性/非对角**不可去**" in src)
ok = ok and ("`LayerStep` / `LayerAdvance` 仍是**显式输入**" in src)
check("C14", "诚实边界：层步弱性、外性不可去、方向性为显式输入", ok)

npass = sum(1 for _, _, ok in results if ok)
print(f"\n{npass}/{len(results)} PASS")
if npass == len(results):
    print("ALL_PASS")
    sys.exit(0)
print("SOME_FAIL")
sys.exit(1)
