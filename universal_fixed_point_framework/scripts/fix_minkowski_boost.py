# -*- coding: utf-8 -*-
"""MinkowskiBoost.lean 批量修复：mathlib 漂移兼容（Fin 求和显式展开、引理替换）"""
import io, sys

P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\formal_proof\MUFPFormalization\src\MUFPFormalization\MinkowskiBoost.lean"

with io.open(P, "r", encoding="utf-8") as f:
    src = f.read()

pairs = [
    # 1. boost4_x 保度规：Fin 求和显式展开
    ("simp [boost4_x, MinkowskiEta4, Matrix.mul_apply]\n    ring_nf\n    try nlinarith [Real.cosh_sq_sub_sinh_sq φ]",
     "simp [boost4_x, MinkowskiEta4, Matrix.mul_apply, Fin.sum_univ_succ]\n    ring_nf\n    try nlinarith [Real.cosh_sq_sub_sinh_sq φ]"),
    # 2. boost4_x_add
    ("simp [boost4_x, Matrix.mul_apply, Real.cosh_add, Real.sinh_add]\n    ring_nf",
     "simp [boost4_x, Matrix.mul_apply, Real.cosh_add, Real.sinh_add, Fin.sum_univ_succ]\n    ring_nf"),
    # 3. rot4_z 保度规
    ("simp [rot4_z, MinkowskiEta4, Matrix.mul_apply]\n    ring_nf\n    try nlinarith [Real.cos_sq_add_sin_sq θ]",
     "simp [rot4_z, MinkowskiEta4, Matrix.mul_apply, Fin.sum_univ_succ]\n    ring_nf\n    try nlinarith [Real.cos_sq_add_sin_sq θ]"),
    # 4. rot4_z_add
    ("simp [rot4_z, Matrix.mul_apply, Real.cos_add, Real.sin_add]\n    ring_nf",
     "simp [rot4_z, Matrix.mul_apply, Real.cos_add, Real.sin_add, Fin.sum_univ_succ]\n    ring_nf"),
    # 5. 李代数 5 处：simp 已闭合，删多余 ring
    ("simp [K_x, J_z, K_y, Matrix.mul_apply]\n    ring",
     "simp [K_x, J_z, K_y, Matrix.mul_apply]"),
    ("simp [J_x, J_y, J_z, Matrix.mul_apply]\n    ring",
     "simp [J_x, J_y, J_z, Matrix.mul_apply]"),
    ("simp [J_x, K_y, K_z, Matrix.mul_apply]\n    ring",
     "simp [J_x, K_y, K_z, Matrix.mul_apply]"),
    ("simp [K_x, K_y, J_z, Matrix.mul_apply]\n    ring",
     "simp [K_x, K_y, J_z, Matrix.mul_apply]"),
    ("simp [J_x, K_x, Matrix.mul_apply]\n    ring",
     "simp [J_x, K_x, Matrix.mul_apply]"),
    # 6. cl11 交换子：环元 2 乘矩阵求值
    ("fin_cases i <;> fin_cases j <;> simp [Jprime] <;> norm_num",
     "fin_cases i <;> fin_cases j <;> simp [Jprime, Matrix.mul_apply, Fin.sum_univ_two] <;> norm_num"),
    # 7. Dirac 迹：simp 已闭合删 ring
    ("simp [Matrix.trace, Matrix.diag, sum_fin_two, e_01, e_10, smul_eq_mul]\n  ring",
     "simp [Matrix.trace, Matrix.diag, sum_fin_two, e_01, e_10, smul_eq_mul]"),
    # 8. Dirac 壳上零因子：矩阵积展开
    ("simp [e_01, e_10, Matrix.mul_fin_two, smul_eq_mul]\n    nlinarith [hsq]",
     "simp [e_01, e_10, Matrix.mul_fin_two, smul_eq_mul, Matrix.mul_apply, Fin.sum_univ_two]\n    nlinarith [hsq]"),
    # 9. boost 共轭保对称：结合律方向
    ("simp [Matrix.transpose_mul, Matrix.transpose_transpose, h]",
     "simp [Matrix.transpose_mul, Matrix.transpose_transpose, h]\n  rw [← Matrix.mul_assoc]"),
    # 10. 无迹显式形态：Fin 求和展开 + try nlinarith
    ("simp [boost, Matrix.mul_apply]\n    ring_nf\n    nlinarith [Real.cosh_sq_sub_sinh_sq φ]",
     "simp [boost, Matrix.mul_apply, Fin.sum_univ_succ]\n    ring_nf\n    try nlinarith [Real.cosh_sq_sub_sinh_sq φ]"),
    # 11. 窗口平均形态：Fin 求和展开
    ("simp [boost, Matrix.mul_apply, Real.cosh_neg, Real.sinh_neg]\n    ring_nf",
     "simp [boost, Matrix.mul_apply, Real.cosh_neg, Real.sinh_neg, Fin.sum_univ_succ]\n    ring_nf"),
    # 12. 缩放因子 ≥1：one_le_cosh 替换（cosh²−sinh²=1 路径）
    ("rw [one_le_div (by norm_num : (0 : ℝ) < 3)]\n  nlinarith [Real.one_le_cosh (2 * φ)]",
     "rw [one_le_div (by norm_num : (0 : ℝ) < 3)]\n  have hc : 0 ≤ Real.cosh (2 * φ) := by positivity\n  have hsq : 1 ≤ Real.cosh (2 * φ) ^ 2 := by\n    nlinarith [Real.cosh_sq_sub_sinh_sq (2 * φ), sq_nonneg (Real.sinh (2 * φ))]\n  exact le_of_sq_le_sq hsq hc"),
    # 13. gamma 平方族 + 反对易族：Fin 求和展开（Fin.sum_univ_succ 递归覆盖 Fin 4）
    ("simp [gamma0, Matrix.mul_apply]\n    ring_nf",
     "simp [gamma0, Matrix.mul_apply, Fin.sum_univ_succ]\n    ring_nf"),
    ("simp [gamma1, Matrix.mul_apply]\n    ring_nf",
     "simp [gamma1, Matrix.mul_apply, Fin.sum_univ_succ]\n    ring_nf"),
    ("simp [gamma2, Matrix.mul_apply]\n    ring_nf",
     "simp [gamma2, Matrix.mul_apply, Fin.sum_univ_succ, Complex.I_mul_I]\n    ring_nf"),
    ("simp [gamma3, Matrix.mul_apply]\n    ring_nf",
     "simp [gamma3, Matrix.mul_apply, Fin.sum_univ_succ]\n    ring_nf"),
    ("simp [gamma0, gamma1, Matrix.mul_apply]\n    ring_nf",
     "simp [gamma0, gamma1, Matrix.mul_apply, Fin.sum_univ_succ]\n    ring_nf"),
    ("simp [gamma0, gamma2, Matrix.mul_apply]\n    ring_nf",
     "simp [gamma0, gamma2, Matrix.mul_apply, Fin.sum_univ_succ, Complex.I_mul_I]\n    ring_nf"),
    ("simp [gamma0, gamma3, Matrix.mul_apply]\n    ring_nf",
     "simp [gamma0, gamma3, Matrix.mul_apply, Fin.sum_univ_succ]\n    ring_nf"),
]

n = 0
for old, new in pairs:
    c = src.count(old)
    if c == 0:
        print(f"[MISS] {old[:60]!r}")
        continue
    src = src.replace(old, new)
    n += c
    print(f"[OK x{c}] {old[:60]!r}")

with io.open(P, "w", encoding="utf-8") as f:
    f.write(src)
print(f"done, {n} replacements")
