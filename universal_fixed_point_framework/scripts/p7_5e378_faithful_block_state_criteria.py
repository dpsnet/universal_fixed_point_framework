#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
C01–C14 机检：P7-5e-378 / G3-P2-10 非对角忠实态的单位可实现性
模块：MUFPFormalization/G3P2FaithfulBlockState.lean

纪律：只用整数/有理数（fractions.Fraction），不出现浮点比较；
不宣称 KMS 导出、不宣称谱分解、不宣称 vN 完成性。
"""
import os
import re
import sys
from fractions import Fraction as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEAN = os.path.join(
    ROOT, "formal_proof", "MUFPFormalization", "src", "MUFPFormalization",
    "G3P2FaithfulBlockState.lean",
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


def det(a, b, c):
    return F(a) * F(c) - F(b) * F(b)


def mat(a, b, c):
    return [[F(a), F(b)], [F(b), F(c)]]


def inv(a, b, c):
    d = det(a, b, c)
    return [[F(c) / d, -F(b) / d], [-F(b) / d, F(a) / d]]


def mul(A, B):
    return [
        [A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]],
        [A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]],
    ]


def conj(a, b, c, A):
    return mul(mul(mat(a, b, c), A), inv(a, b, c))


I2 = [[F(1), F(0)], [F(0), F(1)]]
E12 = [[F(0), F(1)], [F(0), F(0)]]

# C01 Sylvester 判据：a>0 且 a*c−b²>0 ⇒ c>0 且 det≠0
ok = True
count = 0
for a in range(1, 6):
    for c in range(1, 6):
        for b in range(-3, 4):
            if a > 0 and det(a, b, c) > 0:
                count += 1
                ok = ok and (c > 0) and (det(a, b, c) != 0) and (b * b * F(1) < a * c)
check("C01", f"Sylvester：a>0 且 det>0 ⇒ c>0、det≠0（{count} 个正定样本）", ok)

# C02 显式逆公式：A * A⁻¹ = I 且 A⁻¹ * A = I
ok = True
for a in range(1, 5):
    for c in range(1, 5):
        for b in range(-2, 3):
            if det(a, b, c) > 0:
                A = mat(a, b, c)
                ok = ok and (mul(A, inv(a, b, c)) == I2) and (mul(inv(a, b, c), A) == I2)
check("C02", "显式逆公式双侧单位（1..4 × −2..2，正定样本）", ok)

# C03 共轭恒等 ⟺ 标量（只用四个基矩阵判据）
BASIS = [
    [[F(1), F(0)], [F(0), F(0)]], E12,
    [[F(0), F(0)], [F(1), F(0)]], [[F(0), F(0)], [F(0), F(1)]],
]
ok = True
for a in range(1, 5):
    for c in range(1, 5):
        for b in range(-2, 3):
            if det(a, b, c) > 0:
                triv = all(conj(a, b, c, B) == B for B in BASIS)
                scalar = (b == 0 and a == c)
                ok = ok and (triv == scalar)
check("C03", "共轭恒等 ⟺ b=0 且 a=c（1..4 × −2..2）", ok)

# C04 非标量 ⇒ 非平凡共轭（E₁₂ 探针必不同）
ok = True
n_non = 0
for a in range(1, 5):
    for c in range(1, 5):
        for b in range(-2, 3):
            if det(a, b, c) > 0 and not (b == 0 and a == c):
                n_non += 1
                ok = ok and (conj(a, b, c, E12) != E12)
check("C04", f"非标量 ⇒ E₁₂ 共轭不同（{n_non} 个非标量样本）", ok)

# C05 非对角见证 (2,1,1)：det=1>0、b≠0、Ad(E₁₂) ≠ E₁₂
A = mat(2, 1, 1)
d = det(2, 1, 1)
img = conj(2, 1, 1, E12)
ok = (d == F(1)) and (2 > 0) and (1 != 0) and (img != E12)
check("C05", "非对角见证 (2,1,1)：det=1、b=1、Ad(E₁₂)≠E₁₂", ok)

# C06 双块恒等 ⟺ 两块都标量
ok = True
small = [(a, b, c) for a in range(1, 4) for c in range(1, 4) for b in range(-1, 2)
         if det(a, b, c) > 0]
for s1 in small:
    for s2 in small:
        triv = all(conj(*s1, B) == B for B in BASIS) and all(conj(*s2, B) == B for B in BASIS)
        scalar = (s1[1] == 0 and s1[0] == s1[2]) and (s2[1] == 0 and s2[0] == s2[2])
        ok = ok and (triv == scalar)
check("C06", f"双块恒等 ⟺ 两块标量（{len(small)}×{len(small)} 样本）", ok)

# C07 对称共轭的逐元公式：(Ad ρ A)ᵢⱼ = (ρᵢ/ρⱼ)·Aᵢⱼ / det? 对非对角不适用；
# 改用不变量：Ad ρ 保持行列式（det(Ad ρ A) = det A）在正定样本上成立
def det2(M):
    return M[0][0] * M[1][1] - M[0][1] * M[1][0]

ok = True
for a in range(1, 4):
    for c in range(1, 4):
        for b in range(-1, 2):
            if det(a, b, c) > 0:
                for B in BASIS:
                    ok = ok and det2(conj(a, b, c, B)) == det2(B)
check("C07", "Ad ρ 保持行列式（正定样本 × 4 基矩阵）", ok)

# C08 单位可实现与标量性正交：正定样本中非对角非标量样本非空
ok = any(det(a, b, c) > 0 and b != 0 for a in range(1, 4) for c in range(1, 4) for b in range(-2, 3))
check("C08", "正定样本中存在非对角（b≠0）非标量态", ok)

DECLS = [
    "FaithfulBlockState", "FaithfulBlockState.mat", "FaithfulBlockState.det",
    "FaithfulBlockState.det_eq", "FaithfulBlockState.isUnit_det", "matUnit",
    "FaithfulBlockState.unit", "FaithfulBlockState.isScalar",
    "FaithfulBlockState.conj_trivial_iff", "FaithfulBlockState.conj_nontrivial",
    "faithfulFlow", "faithfulFlow_unitRealizable", "blockwiseAut_fst", "blockwiseAut_snd",
    "faithfulFlow_trivial_iff", "faithfulFlow_nontrivial", "nonDiagonalState",
    "nonDiagonalState_not_scalar", "nonDiagonalFlow_nontrivial", "faithfulBlockState_criterion",
]
ok = all(re.search(r"(theorem|noncomputable def|def|structure)\s+" + re.escape(d) + r"\b", code)
         for d in DECLS)
check("C09", f"Lean 声明齐全（{len(DECLS)} 条）", ok)

bad = [w for w in ("axiom", "sorry", "admit", "native_decide") if re.search(r"\b" + w + r"\b", code)]
check("C10", "无 axiom/sorry/admit/native_decide", not bad, detail=", ".join(bad))

must = [
    "Δ_mod", "KMS", "P2 未成立、G3 未闭合", "vN 完成性", "未形式化", "操作性",
    "谱比判据仍只对对角态成立", "代数替身", "非对角",
]
ok = all(s in src for s in must)
forb = ["Δ = 1", "M = 1", "Δ_mod = 1", "Δ_mod = 1.0"]
ok = ok and all(s not in src for s in forb)
check("C11", "记号纪律：边界齐全且无 Δ=1、M=1 赋值", ok)

ok = ("namespace MUFPF.G3P2FaithfulBlockState" in code) and ("G3-P2-10" in src) \
     and ("P7-5e-378" in src)
check("C12", "编号 G3-P2-10 / P7-5e-378 / 命名空间 MUFPF.G3P2FaithfulBlockState", ok)

ok = ("import MUFPFormalization.G3P2VNInterface" in code)
ok = ok and not re.search(
    r"(def|theorem|noncomputable def|structure)\s+"
    r"(BlockMat|TwoBlockAlg|UnitRealizable|TypeIII|blockwiseAut|innerAutEquiv|prodUnit|"
    r"conj_trivial_of_scalar|e12|swapBlockAlgEquiv)\b",
    code)
check("C13", "复用 372/373 构件（不重复定义 BlockMat/TwoBlockAlg/UnitRealizable/blockwiseAut/e12 等）", ok)

ok = all(s in code for s in (
    "faithfulFlow_unitRealizable", "faithfulFlow_trivial_iff", "nonDiagonalState",
    "faithfulBlockState_criterion"))
check("C14", "主定理三支合取与见证齐备", ok)

npass = sum(1 for _, _, ok in results if ok)
print(f"\n{npass}/{len(results)} PASS")
if npass == len(results):
    print("ALL_PASS")
    sys.exit(0)
print("SOME_FAIL")
sys.exit(1)
