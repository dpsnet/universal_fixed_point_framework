#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
C01–C14 机检：P7-5e-377 / G3-P2-9 载体类型判据的谱刚性
模块：MUFPFormalization/G3P2CarrierTypeSpectral.lean

纪律：只用整数/有理数（fractions.Fraction），不出现浮点比较；
不宣称经典因子类型分类、不宣称 vN 完成性。
"""
import os
import re
import sys
from fractions import Fraction as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEAN = os.path.join(
    ROOT, "formal_proof", "MUFPFormalization", "src", "MUFPFormalization",
    "G3P2CarrierTypeSpectral.lean",
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


def ratio(d1, d2):
    return F(d1) / F(d2)


def diag(d1, d2):
    a, b = F(d1), F(d2)
    return [[a, F(0)], [F(0), b]]


def diag_inv(d1, d2):
    return [[F(1) / F(d1), F(0)], [F(0), F(1) / F(d2)]]


def matmul(A, B):
    return [
        [A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]],
        [A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]],
    ]


def conj(d1, d2, A):
    return matmul(matmul(diag(d1, d2), A), diag_inv(d1, d2))


def entries(d1, d2):
    return [F(d1), F(d2)]


MATS = [
    [[F(1), F(0)], [F(0), F(0)]],
    [[F(0), F(1)], [F(0), F(0)]],
    [[F(0), F(0)], [F(1), F(0)]],
    [[F(1), F(2)], [F(3), F(4)]],
    [[F(-1), F(2)], [F(0), F(5)]],
]

# C01 谱比定义：d₁/d₂（正有理网格）
ok = all(ratio(d1, d2) == F(d1) / F(d2) for d1 in range(1, 6) for d2 in range(1, 6))
check("C01", "谱比定义 d₁/d₂（1..5 网格）", ok)

# C02 整体放大不改变谱比（规范化不变性的算术骨架）
ok = True
for c in range(1, 6):
    for d1 in range(1, 5):
        for d2 in range(1, 5):
            ok = ok and (ratio(c * d1, c * d2) == ratio(d1, d2))
check("C02", "整体放大权重不改变谱比（c=1..5，d=1..4）", ok)

# C03 逐元公式：共轭把 aᵢⱼ 乘上 dᵢ/dⱼ
ok = True
for d1 in range(1, 5):
    for d2 in range(1, 5):
        e = entries(d1, d2)
        for A in MATS:
            C = conj(d1, d2, A)
            for i in (0, 1):
                for j in (0, 1):
                    ok = ok and (C[i][j] == (e[i] / e[j]) * A[i][j])
check("C03", "对角共轭逐元公式（4×4 权重 × 5 矩阵 × 2×2 位置）", ok)

# C04 谱比相同 ⟹ 共轭相同（整体放大与等比放大的等价）
ok = True
for p in range(1, 4):
    for q in range(1, 4):
        for c in range(1, 4):
            for A in MATS:
                ok = ok and (conj(p, q, A) == conj(c * p, c * q, A))
check("C04", "相同谱比 ⟹ 相同共轭（p,q,c=1..3）", ok)

# C05 谱比不同 ⟹ 流不同（E₁₂ 的像只依赖谱比）
ok = True
ratios = [(p, q) for p in range(1, 4) for q in range(1, 4)]
E12 = [[F(0), F(1)], [F(0), F(0)]]
for a in ratios:
    for b in ratios:
        if ratio(*a) != ratio(*b):
            ok = ok and (conj(a[0], a[1], E12) != conj(b[0], b[1], E12))
check("C05", "谱比不同 ⟹ 共轭不同（E₁₂ 探针，1..3）", ok)

# C06 恒等 ⟺ 谱比 = 1（单块与双块）
ok = True
for d1 in range(1, 4):
    for d2 in range(1, 4):
        trivial = all(conj(d1, d2, A) == A for A in MATS)
        ok = ok and (trivial == (ratio(d1, d2) == F(1)))
check("C06", "单块恒等 ⟺ 谱比 = 1（1..3 网格，5 矩阵）", ok)
ok = True
for d1 in range(1, 4):
    for d2 in range(1, 4):
        for e1 in range(1, 4):
            for e2 in range(1, 4):
                both = all(conj(d1, d2, A) == A and conj(e1, e2, A) == A for A in MATS)
                ok = ok and (both == (ratio(d1, d2) == F(1) and ratio(e1, e2) == F(1)))
check("C07", "双块恒等 ⟺ 两块谱比皆为 1（1..3 网格）", ok)

# C08 具体规范化见证：(2,1) 与 (6,3) 同谱比 ⟹ 同共轭（双块）
ok = True
for A1 in MATS:
    for A2 in MATS:
        ok = ok and (conj(2, 1, A1) == conj(6, 3, A1))
        ok = ok and (conj(1, 2, A2) == conj(3, 6, A2))
check("C08", "规范化见证 (2,1)≡(6,3)、(1,2)≡(3,6)（5×5 双块）", ok)

# C09 同一载体两类型：对角共轭保持 (1,0)，块交换把 (1,0) 送到 (0,1) ⇒ 块交换 ≠ 任何对角共轭
ok = True
for d1 in range(1, 5):
    for d2 in range(1, 5):
        img = conj(d1, d2, [[F(1), F(0)], [F(0), F(0)]])
        ok = ok and img[0][0] == F(1) and img[0][1] == F(0) and img[1][0] == F(0)
check("C09", "对角共轭固定 (1,0)（1..4 网格）⇒ 块交换不可由任何对角共轭实现", ok)

# ---- Lean 源码结构 ----
DECLS = [
    "diagRatio", "diagConj_entry", "diagConj_eq_of_ratio",
    "blockStateAut_eq_of_ratio", "stateFlow_eq_of_ratio",
    "stateFlow_scale_invariant", "stateFlow_trivial_iff_ratio_one",
    "stateFlow_unitRealizable", "swapFlow_not_unitRealizable",
    "exists_nontrivial_unitRealizable_flow", "exists_nontrivial_not_unitRealizable_flow",
    "carrierType_not_algebra_only", "carrierType_spectral_criterion",
]
ok = all(re.search(r"(theorem|def)\s+" + re.escape(d) + r"\b", code) for d in DECLS)
check("C10", f"Lean 声明齐全（{len(DECLS)} 条）", ok)

bad = [w for w in ("axiom", "sorry", "admit", "native_decide") if re.search(r"\b" + w + r"\b", code)]
check("C11", "无 axiom/sorry/admit/native_decide", not bad, detail=", ".join(bad))

must = [
    "Δ_mod", "KMS", "P2 未成立、G3 未闭合", "vN 完成性", "未形式化",
    "操作性谓词", "谱比决定流", "类型不由代数单独决定",
]
ok = all(s in src for s in must)
forb = ["Δ = 1", "M = 1", "Δ_mod = 1", "Δ_mod = 1.0"]
ok = ok and all(s not in src for s in forb)
check("C12", "记号纪律：边界齐全且无 Δ=1、M=1 赋值", ok)

ok = ("namespace MUFPF.G3P2CarrierTypeSpectral" in code) and ("G3-P2-9" in src) \
     and ("P7-5e-377" in src)
check("C13", "编号 G3-P2-9 / P7-5e-377 / 命名空间 MUFPF.G3P2CarrierTypeSpectral", ok)

ok = ("import MUFPFormalization.G3P2VNInterface" in code)
ok = ok and not re.search(
    r"(def|theorem)\s+(stateFlow|blockStateAut|stateDatum|swapDatum|UnitRealizable|TypeIII|"
    r"swapBlockAlgEquiv|DiagState|diagMat|blockwiseAut)\b",
    code)
check("C14", "复用 372/373 构件（不重复定义 stateFlow/UnitRealizable/DiagState 等）", ok)

npass = sum(1 for _, _, ok in results if ok)
print(f"\n{npass}/{len(results)} PASS")
if npass == len(results):
    print("ALL_PASS")
    sys.exit(0)
print("SOME_FAIL")
sys.exit(1)
