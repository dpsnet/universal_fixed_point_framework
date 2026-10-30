# -*- coding: utf-8 -*-
# fix8: mass_shell one_apply+ring、852 ring 前置、865/878 Cast 线性 rw [h]
import io

path = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\formal_proof\MUFPFormalization\src\MUFPFormalization\MinkowskiBoost.lean"

with io.open(path, "r", encoding="utf-8") as f:
    src = f.read()

reps = []

# 1) mass_shell 系列（3 处）：cosh² rw try 后加 one_apply simp + ring
old_ms = """  all_goals
    try
      rw [show Complex.cosh (φ : ℂ) ^ 2 = 1 + Complex.sinh (φ : ℂ) ^ 2 by
        rw [← Complex.cosh_sq_sub_sinh_sq (φ : ℂ)]
        ring]
      ring"""
new_ms = """  all_goals
    try
      rw [show Complex.cosh (φ : ℂ) ^ 2 = 1 + Complex.sinh (φ : ℂ) ^ 2 by
        rw [← Complex.cosh_sq_sub_sinh_sq (φ : ℂ)]
        ring]
      ring
  all_goals
    try simp [Matrix.one_apply, Pi.one_apply]
  all_goals
    try ring"""
reps.append((old_ms, new_ms, "mass_shell one_apply+ring x3"))

# 2) 852 diracOp4full_sq：ring 前置
old_852 = """    simp [DiracOp4Full, gamma0, gamma1, gamma2, gamma3, Matrix.mul_apply, Fin.sum_univ_succ]
    try ring_nf
    try ring
    try norm_num"""
new_852 = """    simp [DiracOp4Full, gamma0, gamma1, gamma2, gamma3, Matrix.mul_apply, Fin.sum_univ_succ]
    try ring
    try ring_nf
    try norm_num"""
reps.append((old_852, new_852, "852 ring 前置"))

# 3) 865 diracOp4full_mass_shell：Cast 线性 rw [h]
old_865 = """  rw [diracOp4full_sq]
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [Matrix.one_apply, Pi.smul_apply, Pi.one_apply]
    try norm_num [h]"""
new_865 = """  rw [diracOp4full_sq]
  ext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [Matrix.one_apply, Pi.smul_apply, Pi.one_apply]
  all_goals
    try
      rw [show (E : ℂ) ^ 2 - (p₁ : ℂ) ^ 2 - (p₂ : ℂ) ^ 2 - (p₃ : ℂ) ^ 2
            = ↑(E ^ 2 - p₁ ^ 2 - p₂ ^ 2 - p₃ ^ 2) by ring]
      rw [h]
  all_goals
    try norm_num [h]"""
reps.append((old_865, new_865, "865 Cast 线性 rw [h]"))

# 4) 878 diracOp4full_mass_factorization：one_apply + ring + Cast 线性 rw [h]
old_878 = """  all_goals
    simp [DiracOp4Full, gamma0, gamma1, gamma2, gamma3, Matrix.mul_apply, Fin.sum_univ_succ]
    try ring_nf
    norm_num [h]"""
new_878 = """  all_goals
    simp [DiracOp4Full, gamma0, gamma1, gamma2, gamma3, Matrix.mul_apply, Fin.sum_univ_succ,
          Matrix.one_apply, Pi.one_apply]
    try ring
    try ring_nf
  all_goals
    try
      rw [show (E : ℂ) ^ 2 - (p₁ : ℂ) ^ 2 - (p₂ : ℂ) ^ 2 - (p₃ : ℂ) ^ 2
            = ↑(E ^ 2 - p₁ ^ 2 - p₂ ^ 2 - p₃ ^ 2) by ring]
      rw [h]
    try norm_num [h]"""
reps.append((old_878, new_878, "878 one_apply+ring+Cast rw [h]"))

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
