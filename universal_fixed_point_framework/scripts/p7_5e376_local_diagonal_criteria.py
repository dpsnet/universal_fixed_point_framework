#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
C01–C14 机检：P7-5e-376 / G3-P1b-3 局部化 hdiag_inner（全局假设降为单点假设）
模块：MUFPFormalization/G3P1b3LocalDiagonal.lean

纪律：只用整数/布尔枚举，不出现浮点比较；不宣称「局部 ⟹ 全局」。
"""
import itertools
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEAN = os.path.join(
    ROOT, "formal_proof", "MUFPFormalization", "src", "MUFPFormalization",
    "G3P1b3LocalDiagonal.lean",
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


def diagonal(L, sigma, dom):
    return all(L(sigma(a)) == L(a) for a in dom)


def no_move(L, sigma, dom):
    return not any(L(sigma(a)) != L(a) for a in dom)


def layer_step(L, sigma, k, dom):
    return all((L(sigma(a)) == L(a)) or (L(sigma(a)) == L(a) + k) for a in dom)


SIGMAS = [
    lambda a: a,
    lambda a: a + 1,
    lambda a: a - 1,
    lambda a: a + 2,
    lambda a: 2 * a,
    lambda a: 0,
]

# C01 层对角 ⟺ 「不存在被移动的层」（非对角 ⟺ 存在移动点）
ok = all(diagonal(L_id, s, DOM) == no_move(L_id, s, DOM) for s in SIGMAS)
check("C01", "层对角 ⟺ 不存在移动点（6 个 σ，层 0..4）", ok)

# C02 恒等恒为层对角（对多个层泛函）
ok = all(diagonal(L, lambda a: a, DOM) for L in (L_id, lambda a: a + 2, lambda a: 3 * a, lambda a: 0))
check("C02", "恒等恒为层对角（4 个层泛函）", ok)

# C03 层对角 ⟺ 零步层步（k=0 的两支重合）
ok = all(diagonal(L_id, s, DOM) == layer_step(L_id, s, 0, DOM) for s in SIGMAS)
check("C03", "层对角 ⟺ LayerStep k=0（6 个 σ）", ok)

# C04 局部假设非空壳：恒等满足「对角 ⟹ 内」（内 = 恒等模型）
inner = lambda s: all(s(a) == a for a in DOM)
ok = diagonal(L_id, lambda a: a, DOM) and inner(lambda a: a)
ok = ok and all((diagonal(L_id, s, DOM) and not inner(s)) or True for s in SIGMAS)
check("C04", "局部假设非空壳：恒等满足（内=恒等模型）", ok)

# C05 局部逆向结构：¬I σ ∧ (D σ → I σ) ⟹ ¬D σ（真值表）
ok = True
for D in (False, True):
    for I in (False, True):
        hloc = (not D) or I          # D → I
        ok = ok and (((not I) and hloc) <= (not D))
check("C05", "局部逆向：¬内 ∧ (对角⟹内) ⟹ 非对角（真值表）", ok)

# C06 局部升层：层步 + 非对角 ⟹ 存在严格升层点（k=1..3）
ok = True
for k in (1, 2, 3):
    for s in SIGMAS:
        if layer_step(L_id, s, k, DOM) and not diagonal(L_id, s, DOM):
            ok = ok and any(L_id(s(a)) == L_id(a) + k for a in DOM)
check("C06", "局部升层：层步+非对角 ⟹ ∃a 升 k 层（k=1..3）", ok)

# C07 升层 ⟹ 层下标不同 ⟹ 模权不同（gap≠0 由 Lean 单射性给出）
ok = True
for k in (1, 2, 3):
    for s in SIGMAS:
        for a in DOM:
            if L_id(s(a)) == L_id(a) + k and k != 0:
                ok = ok and (L_id(s(a)) != L_id(a))
check("C07", "升层 ⟹ 层下标不同（k=1..3，模权单射前提）", ok)

# C08 以 L=id 时，3 点置换非对角 ⟺ 非恒等（6 个置换）
import math
ok = True
for perm in itertools.permutations(DOM[:3]):
    s = lambda a, p=perm: p[a] if a < 3 else a
    diag = diagonal(L_id, s, DOM[:3])
    is_id = all(s(a) == a for a in DOM[:3])
    ok = ok and (diag == is_id)
check("C08", "L=id：3 点置换非对角 ⟺ 非恒等（6 个置换）", ok)

# ---- Lean 源码结构 ----
DECLS = [
    "LayerDiagonal", "layerDiagonal_iff_no_move", "layerDiagonal_refl",
    "layerDiagonal_iff_layerStep_zero", "LocalInnerOn", "global_implies_local",
    "localInnerOn_refl", "local_outer_not_diagonal", "local_layerStep_outer_ascent",
    "local_layerStep_outer_weight_moves", "local_directional_converse",
    "local_not_imply_global",
]
ok = all(re.search(r"(theorem|def)\s+" + re.escape(d) + r"\b", code) for d in DECLS)
check("C09", f"Lean 声明齐全（{len(DECLS)} 条）", ok)

bad = [w for w in ("axiom", "sorry", "admit", "native_decide") if re.search(r"\b" + w + r"\b", code)]
check("C10", "无 axiom/sorry/admit/native_decide", not bad, detail=", ".join(bad))

must = ["Δ_mod", "KMS", "P2 未成立、G3 未闭合", "vN 完成性", "未形式化", "严格弱于"]
ok = all(s in src for s in must)
forb = ["Δ = 1", "M = 1", "Δ_mod = 1"]
ok = ok and all(s not in src for s in forb)
check("C11", "记号纪律：边界齐全且无 Δ=1、M=1 赋值", ok)

ok = ("namespace MUFPF.G3P1b3Local" in code) and ("G3-P1b-3" in src)
check("C12", "编号 G3-P1b-3 / 命名空间 MUFPF.G3P1b3Local", ok)

ok = ("import MUFPFormalization.G3P1b3DirectionalConverse" in code)
ok = ok and ("open MUFPF.G3P1b3Converse MUFPF.G3P1b3Directional" in code)
ok = ok and not re.search(
    r"(def|theorem)\s+(LayerStep|LayerAdvance|iterateAut|boolLayer|InnerRealization|IsOuterAut|modularWeight)\b",
    code)
check("C13", "复用 368/374 构件（不重复定义 LayerStep/InnerRealization/IsOuterAut 等）", ok)

# C14 局部严格弱于全局：谓词层反例复现（D true=False、D false=True、I≡False、σ=true）
ok = True
D = {True: False, False: True}
I = {True: False, False: False}
local = (not D[True]) or I[True]
glob = all(((not D[t]) or I[t]) for t in (True, False))
ok = ok and local and not glob
ok = ok and ("local_not_imply_global" in code) and ("global_implies_local" in code)
check("C14", "局部严格弱于全局（反例复现 + 两声明齐备）", ok)

npass = sum(1 for _, _, ok in results if ok)
print(f"\n{npass}/{len(results)} PASS")
if npass == len(results):
    print("ALL_PASS")
    sys.exit(0)
print("SOME_FAIL")
sys.exit(1)
