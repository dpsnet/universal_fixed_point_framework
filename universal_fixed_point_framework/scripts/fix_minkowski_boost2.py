# -*- coding: utf-8 -*-
"""MinkowskiBoost.lean 第二轮修复：删冗余 ring_nf、polyrith、vecMul 展开、sqrt 路径"""
import io

P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\formal_proof\MUFPFormalization\src\MUFPFormalization\MinkowskiBoost.lean"

with io.open(P, "r", encoding="utf-8") as f:
    src = f.read()

pairs = [
    # R1: cl11 交换子：环元 2 求值需 Matrix.one_apply
    ("fin_cases i <;> fin_cases j <;> simp [Jprime, Matrix.mul_apply, Fin.sum_univ_two] <;> norm_num",
     "fin_cases i <;> fin_cases j <;> simp [Jprime, Matrix.mul_apply, Fin.sum_univ_two, Matrix.one_apply] <;> norm_num"),
    # R2a: boost4_x 保度规：删 ring_nf（simp 已闭合）
    ("simp [boost4_x, MinkowskiEta4, Matrix.mul_apply, Fin.sum_univ_succ]\n    ring_nf\n    try nlinarith [Real.cosh_sq_sub_sinh_sq φ]",
     "simp [boost4_x, MinkowskiEta4, Matrix.mul_apply, Fin.sum_univ_succ]\n    try nlinarith [Real.cosh_sq_sub_sinh_sq φ]"),
    # R2b: boost4_x_add
    ("simp [boost4_x, Matrix.mul_apply, Real.cosh_add, Real.sinh_add, Fin.sum_univ_succ]\n    ring_nf",
     "simp [boost4_x, Matrix.mul_apply, Real.cosh_add, Real.sinh_add, Fin.sum_univ_succ]"),
    # R2c: rot4_z 保度规
    ("simp [rot4_z, MinkowskiEta4, Matrix.mul_apply, Fin.sum_univ_succ]\n    ring_nf\n    try nlinarith [Real.cos_sq_add_sin_sq θ]",
     "simp [rot4_z, MinkowskiEta4, Matrix.mul_apply, Fin.sum_univ_succ]\n    try nlinarith [Real.cos_sq_add_sin_sq θ]"),
    # R2d: rot4_z_add
    ("simp [rot4_z, Matrix.mul_apply, Real.cos_add, Real.sin_add, Fin.sum_univ_succ]\n    ring_nf",
     "simp [rot4_z, Matrix.mul_apply, Real.cos_add, Real.sin_add, Fin.sum_univ_succ]"),
    # R3: 无迹显式形态：nlinarith → polyrith（cosh²−sinh²=1 多项式环）
    ("simp [boost, Matrix.mul_apply, Fin.sum_univ_succ]\n    ring_nf\n    try nlinarith [Real.cosh_sq_sub_sinh_sq φ]",
     "simp [boost, Matrix.mul_apply, Fin.sum_univ_succ]\n    ring_nf\n    polyrith [Real.cosh_sq_sub_sinh_sq φ]"),
    # R4: 窗口平均形态：vecMul/vecHead/vecTail 展开
    ("simp [boost, Matrix.mul_apply, Real.cosh_neg, Real.sinh_neg, Fin.sum_univ_succ]\n    ring_nf",
     "simp [boost, Matrix.mul_apply, Real.cosh_neg, Real.sinh_neg, Fin.sum_univ_succ,\n          Matrix.vecMul, Matrix.vecHead, Matrix.vecTail]\n    ring_nf"),
    # R5: 缩放因子：le_of_sq_le_sq 正确路径（3 ≤ 1+2cosh）
    ("rw [one_le_div (by norm_num : (0 : ℝ) < 3)]\n  have hc : 0 ≤ Real.cosh (2 * φ) := by positivity\n  have hsq : 1 ≤ Real.cosh (2 * φ) ^ 2 := by\n    nlinarith [Real.cosh_sq_sub_sinh_sq (2 * φ), sq_nonneg (Real.sinh (2 * φ))]\n  exact le_of_sq_le_sq hsq hc",
     "rw [one_le_div (by norm_num : (0 : ℝ) < 3)]\n  have hc : 0 ≤ Real.cosh (2 * φ) := by positivity\n  have hsq : (1 : ℝ) ^ 2 ≤ Real.cosh (2 * φ) ^ 2 := by\n    nlinarith [Real.cosh_sq_sub_sinh_sq (2 * φ), sq_nonneg (Real.sinh (2 * φ))]\n  have hcosh : 1 ≤ Real.cosh (2 * φ) := le_of_sq_le_sq hsq hc\n  nlinarith [hcosh]"),
    # R6: gamma 平方族 + 反对易族：删 ring_nf
    ("simp [gamma0, Matrix.mul_apply, Fin.sum_univ_succ]\n    ring_nf",
     "simp [gamma0, Matrix.mul_apply, Fin.sum_univ_succ]"),
    ("simp [gamma1, Matrix.mul_apply, Fin.sum_univ_succ]\n    ring_nf",
     "simp [gamma1, Matrix.mul_apply, Fin.sum_univ_succ]"),
    ("simp [gamma2, Matrix.mul_apply, Fin.sum_univ_succ, Complex.I_mul_I]\n    ring_nf",
     "simp [gamma2, Matrix.mul_apply, Fin.sum_univ_succ, Complex.I_mul_I]"),
    ("simp [gamma3, Matrix.mul_apply, Fin.sum_univ_succ]\n    ring_nf",
     "simp [gamma3, Matrix.mul_apply, Fin.sum_univ_succ]"),
    ("simp [gamma0, gamma1, Matrix.mul_apply, Fin.sum_univ_succ]\n    ring_nf",
     "simp [gamma0, gamma1, Matrix.mul_apply, Fin.sum_univ_succ]"),
    ("simp [gamma0, gamma2, Matrix.mul_apply, Fin.sum_univ_succ, Complex.I_mul_I]\n    ring_nf",
     "simp [gamma0, gamma2, Matrix.mul_apply, Fin.sum_univ_succ, Complex.I_mul_I]"),
    ("simp [gamma0, gamma3, Matrix.mul_apply, Fin.sum_univ_succ]\n    ring_nf",
     "simp [gamma0, gamma3, Matrix.mul_apply, Fin.sum_univ_succ]"),
]

n = 0
for old, new in pairs:
    c = src.count(old)
    if c == 0:
        print(f"[MISS] {old[:70]!r}")
        continue
    src = src.replace(old, new)
    n += c
    print(f"[OK x{c}] {old[:70]!r}")

with io.open(P, "w", encoding="utf-8") as f:
    f.write(src)
print(f"done, {n} replacements")
