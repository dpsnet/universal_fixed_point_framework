# -*- coding: utf-8 -*-
"""第四轮 MinkowskiBoost.lean 修复 v2：全量替换（幂等修正）。"""
import io

path = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\formal_proof\MUFPFormalization\src\MUFPFormalization\MinkowskiBoost.lean"
with io.open(path, encoding='utf-8') as f:
    src = f.read()

def rep(old, new, count, tag=""):
    global src
    n = src.count(old)
    assert n >= count, f"MISS[{tag}]: {old[:90]!r} found={n} want>={count}"
    src = src.replace(old, new, count)
    print(f"OK[{tag}] x{n}")

# ---- 1. 全部 4 空格 ring_nf → try ring_nf ----
rep("    ring_nf", "    try ring_nf", 0, tag="try_ring_nf_all")

# ---- 2. 全部 4 空格 norm_num（无参数）→ try ----
rep("    norm_num\n", "    try norm_num\n", 0, tag="try_norm_num_all")

# ---- 3. 674 块三处 norm_num[complex]：统一加 one_apply（先处理后残留的裸形态） ----
# 已是 try 版前缀的（701）：
rep("    try norm_num [mass_shell_complex m φ]\n",
    "    try norm_num [mass_shell_complex m φ, Matrix.one_apply, Pi.one_apply, Pi.zero_apply]\n",
    0, tag="complex_one_a")
# 仍裸的（722/735）：
rep("    norm_num [mass_shell_complex m φ]\n",
    "    try norm_num [mass_shell_complex m φ, Matrix.one_apply, Pi.one_apply, Pi.zero_apply]\n",
    0, tag="complex_one_b")

# ---- 4. 140 块：norm_num 加 one_apply（numeral 矩阵元） ----
rep("""  fin_cases i <;> fin_cases j <;> norm_num [Jprime, Matrix.mul_apply, Fin.sum_univ_two, Pi.smul_apply]""",
"""  fin_cases i <;> fin_cases j <;> norm_num [Jprime, Matrix.mul_apply, Fin.sum_univ_two,
        Pi.smul_apply, Matrix.one_apply, Pi.one_apply, Pi.zero_apply]""",
1, tag="cl11_norm_one")

# ---- 5. gamma_clifford_relation 两段式 + gamma_ofFin 引理 ----
rep("""theorem gamma_clifford_relation (a b : Fin 4) :
    gamma a * gamma b + gamma b * gamma a
      = (2 * gammaEta a b) • (1 : Matrix (Fin 4) (Fin 4) ℂ) := by
  fin_cases a <;> fin_cases b <;>
    simp [gamma, gammaEta, gamma0_sq, gamma1_sq, gamma2_sq, gamma3_sq,
          gamma0_gamma1_anticomm, gamma0_gamma2_anticomm, gamma0_gamma3_anticomm,
          gamma1_gamma2_anticomm, gamma1_gamma3_anticomm, gamma2_gamma3_anticomm]""",
"""lemma gamma_ofFin0 : gamma (0 : Fin 4) = gamma0 := by rfl
lemma gamma_ofFin1 : gamma (1 : Fin 4) = gamma1 := by rfl
lemma gamma_ofFin2 : gamma (2 : Fin 4) = gamma2 := by rfl
lemma gamma_ofFin3 : gamma (3 : Fin 4) = gamma3 := by rfl

theorem gamma_clifford_relation (a b : Fin 4) :
    gamma a * gamma b + gamma b * gamma a
      = (2 * gammaEta a b) • (1 : Matrix (Fin 4) (Fin 4) ℂ) := by
  fin_cases a <;> fin_cases b
  all_goals
    simp [gamma_ofFin0, gamma_ofFin1, gamma_ofFin2, gamma_ofFin3, gammaEta,
          gamma0_sq, gamma1_sq, gamma2_sq, gamma3_sq,
          gamma0_gamma1_anticomm, gamma0_gamma2_anticomm, gamma0_gamma3_anticomm,
          gamma1_gamma2_anticomm, gamma1_gamma3_anticomm, gamma2_gamma3_anticomm]
  all_goals
    try
      ext i j
      fin_cases i <;> fin_cases j
      norm_num [Pi.add_apply, Pi.smul_apply, Matrix.one_apply, Pi.one_apply, Pi.zero_apply]""",
1, tag="gamma_clifford")

# ---- 6. Jz/Kx/diracOp4full_sq：simp 加 Fin.sum_univ_succ ----
rep("    simp [J_z, Matrix.mul_apply]",
    "    simp [J_z, Matrix.mul_apply, Fin.sum_univ_succ]", 1, tag="Jz_sum")
rep("    simp [K_x, Matrix.mul_apply]",
    "    simp [K_x, Matrix.mul_apply, Fin.sum_univ_succ]", 1, tag="Kx_sum")
rep("    simp [DiracOp4Full, gamma0, gamma1, gamma2, gamma3, Matrix.mul_apply]",
    "    simp [DiracOp4Full, gamma0, gamma1, gamma2, gamma3, Matrix.mul_apply, Fin.sum_univ_succ]",
    1, tag="DiracFull_sum")

with io.open(path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(src)
print("WROTE")
