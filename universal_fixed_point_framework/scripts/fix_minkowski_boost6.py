# -*- coding: utf-8 -*-
# fix6: 140 rfl、459/493 try rw、637 gamma_clifford 探针30方案、714/735/748 try norm_num
import io

path = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\formal_proof\MUFPFormalization\src\MUFPFormalization\MinkowskiBoost.lean"

with io.open(path, "r", encoding="utf-8") as f:
    src = f.read()

reps = []

# 1) 140：cl11_commutator 尾部 norm_num -> rfl
old_140 = """  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [Jprime, Matrix.mul_apply, Fin.sum_univ_two,
        Pi.smul_apply, Matrix.one_apply, Pi.one_apply, Pi.zero_apply]"""
new_140 = """  ext i j
  fin_cases i <;> fin_cases j <;> rfl"""
reps.append((old_140, new_140, "140 cl11 rfl"))

# 2) 459/493：rw [show cosh...] -> try rw（两处相同文本）
old_rw = """    rw [show Real.cosh φ ^ 2 = 1 + Real.sinh φ ^ 2 by
        nlinarith [Real.cosh_sq_sub_sinh_sq φ]]
    try ring_nf"""
new_rw = """    try rw [show Real.cosh φ ^ 2 = 1 + Real.sinh φ ^ 2 by
        nlinarith [Real.cosh_sq_sub_sinh_sq φ]]
    try ring_nf"""
reps.append((old_rw, new_rw, "459/493 try rw"))

# 3) 637：gamma_clifford 完整证明换探针30方案
old_637 = """  fin_cases a <;> fin_cases b
  all_goals
    simp [gamma_ofFin0, gamma_ofFin1, gamma_ofFin2, gamma_ofFin3, gammaEta,
          gamma0_sq, gamma1_sq, gamma2_sq, gamma3_sq,
          gamma0_gamma1_anticomm, gamma0_gamma2_anticomm, gamma0_gamma3_anticomm,
          gamma1_gamma2_anticomm, gamma1_gamma3_anticomm, gamma2_gamma3_anticomm]
  all_goals
    try
      ext i j
      fin_cases i <;> fin_cases j
      norm_num [Pi.add_apply, Pi.smul_apply, Matrix.one_apply, Pi.one_apply, Pi.zero_apply]"""
new_637 = """  fin_cases a <;> fin_cases b
  all_goals
    simp [gamma_ofFin0, gamma_ofFin1, gamma_ofFin2, gamma_ofFin3, gammaEta,
          gamma0_sq, gamma1_sq, gamma2_sq, gamma3_sq,
          gamma0_gamma1_anticomm, gamma0_gamma2_anticomm, gamma0_gamma3_anticomm,
          gamma1_gamma2_anticomm, gamma1_gamma3_anticomm, gamma2_gamma3_anticomm]
  all_goals
    try
      ext i j
      fin_cases i <;> fin_cases j
      simp [Matrix.mul_apply, Matrix.one_apply, Pi.add_apply, Pi.one_apply,
            Pi.zero_apply, Pi.smul_apply, Fin.sum_univ_succ, gamma0, gamma1,
            gamma2, gamma3]
  all_goals
    try norm_num
  all_goals
    try norm_num [Matrix.mul_apply, gamma0, gamma1, gamma2, gamma3, Fin.sum_univ_succ]
  all_goals
    try native_decide
  all_goals
    try rfl"""
reps.append((old_637, new_637, "637 gamma_clifford 探针30方案"))

# 4) 714/735/748：norm_num [mass_shell_complex m φ] -> try norm_num
old_ms = """    norm_num [mass_shell_complex m φ]"""
new_ms = """    try norm_num [mass_shell_complex m φ]"""
reps.append((old_ms, new_ms, "714/735/748 try norm_num"))

# 执行（无 count = 全部替换）
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
