# -*- coding: utf-8 -*-
# fix7: 140 try rfl、mass_shell 系列 cosh² rw、832 try ring、853 ext+one_apply
import io

path = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\formal_proof\MUFPFormalization\src\MUFPFormalization\MinkowskiBoost.lean"

with io.open(path, "r", encoding="utf-8") as f:
    src = f.read()

reps = []

# 1) 140 cl11：try 块加 try rfl
old_140 = """  all_goals
    simp [Jprime, Matrix.mul_apply, Pi.add_apply, Pi.smul_apply, Fin.sum_univ_two]
  all_goals
    try norm_num
  all_goals
    try native_decide"""
new_140 = """  all_goals
    simp [Jprime, Matrix.mul_apply, Pi.add_apply, Pi.smul_apply, Fin.sum_univ_two]
  all_goals
    try norm_num
  all_goals
    try rfl
  all_goals
    try native_decide"""
reps.append((old_140, new_140, "140 try rfl"))

# 2) mass_shell_complex 系列：try norm_num 后加 cosh² rw + ring（4 处形态统一）
old_ms_try = """    try ring_nf
    try norm_num [mass_shell_complex m φ]"""
new_ms_try = """    try ring_nf
    try norm_num [mass_shell_complex m φ]
  all_goals
    try
      rw [show Complex.cosh (φ : ℂ) ^ 2 = 1 + Complex.sinh (φ : ℂ) ^ 2 by
        rw [← Complex.cosh_sq_sub_sinh_sq (φ : ℂ)]
        ring]
      ring"""
reps.append((old_ms_try, new_ms_try, "mass_shell cosh² rw x3"))

# 3) 832 diracOp4full_sq：加 try ring
old_832 = """    simp [DiracOp4Full, gamma0, gamma1, gamma2, gamma3, Matrix.mul_apply, Fin.sum_univ_succ]
    try ring_nf
    try norm_num"""
new_832 = """    simp [DiracOp4Full, gamma0, gamma1, gamma2, gamma3, Matrix.mul_apply, Fin.sum_univ_succ]
    try ring_nf
    try ring
    try norm_num"""
reps.append((old_832, new_832, "832 try ring"))

# 4) 853/859 diracOp4full_mass_shell：ext + simp one + try norm_num [h]
old_853 = """  rw [diracOp4full_sq]
  norm_num [h]"""
new_853 = """  rw [diracOp4full_sq]
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [Matrix.one_apply, Pi.smul_apply, Pi.one_apply]
    try norm_num [h]"""
reps.append((old_853, new_853, "853 ext one_apply"))

total = 0
for old, new, tag in reps:
    if old not in src:
        print("MISS: " + tag)
        continue
    n = src.count(old)
    src = src.replace(old, new)
    print("OK(%d): %s" % (n, tag))
    total += n

with io.open(path, "w", encoding="utf-8", newline="") as f:
    f.write(src)
print("total replacements: %d" % total)
