# -*- coding: utf-8 -*-
"""第三轮 MinkowskiBoost.lean 修复：基于 mb_err3.log 残余错误 + 探针验证模式。"""
import io, sys

path = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\formal_proof\MUFPFormalization\src\MUFPFormalization\MinkowskiBoost.lean"
with io.open(path, encoding='utf-8') as f:
    src = f.read()
orig = src

def rep(old, new, count=1, tag=""):
    global src
    n = src.count(old)
    assert n >= count, f"MISS[{tag}]: {old[:90]!r} found={n} want>={count}"
    src = src.replace(old, new, count)
    print(f"OK[{tag}] x{count}")

# ---- 1. 140 块：去 smul_eq_mul，避免环元 2；元级 norm_num ----
rep("""  rw [e01_mul_e10_anticomm]
  simp [hjo, smul_eq_mul]
  ext i j
  fin_cases i <;> fin_cases j <;> simp [Jprime, Matrix.mul_apply, Fin.sum_univ_two, Matrix.one_apply] <;> norm_num""",
"""  rw [e01_mul_e10_anticomm]
  simp [hjo]
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [Jprime, Matrix.mul_apply, Fin.sum_univ_two, Pi.smul_apply]""",
tag="cl11_commutator")

# ---- 2. 226 块：恢复 ring_nf（交换律闭合） ----
rep("""    simp [boost4_x, Matrix.mul_apply, Real.cosh_add, Real.sinh_add, Fin.sum_univ_succ]""",
"""    simp [boost4_x, Matrix.mul_apply, Real.cosh_add, Real.sinh_add, Fin.sum_univ_succ]
    ring_nf""",
tag="boost4_x_add")

# ---- 3. 300 块：恢复 ring_nf ----
rep("""    simp [rot4_z, Matrix.mul_apply, Real.cos_add, Real.sin_add, Fin.sum_univ_succ]""",
"""    simp [rot4_z, Matrix.mul_apply, Real.cos_add, Real.sin_add, Fin.sum_univ_succ]
    ring_nf""",
tag="rot4_z_add")

# ---- 4. 456 块：polyrith 下线 → cosh² 显式替换 ----
rep("""    simp [boost, Matrix.mul_apply, Fin.sum_univ_succ]
    ring_nf
    polyrith [Real.cosh_sq_sub_sinh_sq φ]""",
"""    simp [boost, Matrix.mul_apply, Fin.sum_univ_succ]
    ring_nf
    rw [show Real.cosh φ ^ 2 = 1 + Real.sinh φ ^ 2 by
        nlinarith [Real.cosh_sq_sub_sinh_sq φ]]
    ring_nf""",
tag="boost_adjoint_traceless")

# ---- 5. 480 块：ring_nf 后加 cosh² 替换 ----
rep("""    simp [boost, Matrix.mul_apply, Real.cosh_neg, Real.sinh_neg, Fin.sum_univ_succ,
          Matrix.vecMul, Matrix.vecHead, Matrix.vecTail]
    ring_nf""",
"""    simp [boost, Matrix.mul_apply, Real.cosh_neg, Real.sinh_neg, Fin.sum_univ_succ,
          Matrix.vecMul, Matrix.vecHead, Matrix.vecTail]
    ring_nf
    rw [show Real.cosh φ ^ 2 = 1 + Real.sinh φ ^ 2 by
        nlinarith [Real.cosh_sq_sub_sinh_sq φ]]
    ring_nf""",
tag="boost_window3_avg")

# ---- 6. 604/612/620：删冗余 ring_nf（gamma1_gamma2/1_3/2_3 反对易） ----
for g1, g2 in [("gamma1", "gamma2"), ("gamma1", "gamma3"), ("gamma2", "gamma3")]:
    rep(f"""    simp [{g1}, {g2}, Matrix.mul_apply]
    ring_nf""",
        f"""    simp [{g1}, {g2}, Matrix.mul_apply]""",
        tag=f"anticomm_{g1}_{g2}")

# ---- 7. 651 块：diracOp4_sq 加 Fin.sum_univ_succ ----
rep("""  all_goals
    simp [DiracOp4, gamma0, gamma1, Matrix.mul_apply]
    ring_nf""",
"""  all_goals
    simp [DiracOp4, gamma0, gamma1, Matrix.mul_apply, Fin.sum_univ_succ]
    ring_nf""",
tag="diracOp4_sq")

# ---- 8. 插入 mass_shell / mass_shell_complex 定义（#58 段前） ----
anchor = """/-! ## 4×4 Dirac 质量方程代数层（#58，Cl(1,3) 完整签名）"""
mass_shell_defs = """/-- ★★ 质量壳代数（谱流参数化，ℝ）：(m·coshφ)² − (m·sinhφ)² = m²
    ——cosh²−sinh²=1 的质量加权形态（#42 质量壳的谱流参数化）。 -/
theorem mass_shell (m φ : ℝ) : (m * Real.cosh φ) ^ 2 - (m * Real.sinh φ) ^ 2 = m ^ 2 := by
  calc
    (m * Real.cosh φ) ^ 2 - (m * Real.sinh φ) ^ 2 = m ^ 2 * (Real.cosh φ ^ 2 - Real.sinh φ ^ 2) := by ring
    _ = m ^ 2 * 1 := by rw [Real.cosh_sq_sub_sinh_sq φ]
    _ = m ^ 2 := by ring

/-- ★★ 质量壳代数（ℂ 提升）：((m:ℂ)·cosh(φ:ℂ))² − ((m:ℂ)·sinh(φ:ℂ))² = (m:ℂ)²。 -/
theorem mass_shell_complex (m φ : ℝ) :
    ((m : ℂ) * Complex.cosh (φ : ℂ)) ^ 2 - ((m : ℂ) * Complex.sinh (φ : ℂ)) ^ 2 = (m : ℂ) ^ 2 := by
  calc
    ((m : ℂ) * Complex.cosh (φ : ℂ)) ^ 2 - ((m : ℂ) * Complex.sinh (φ : ℂ)) ^ 2
        = (m : ℂ) ^ 2 * (Complex.cosh (φ : ℂ) ^ 2 - Complex.sinh (φ : ℂ) ^ 2) := by ring
    _ = (m : ℂ) ^ 2 * 1 := by rw [Complex.cosh_sq_sub_sinh_sq]
    _ = (m : ℂ) ^ 2 := by ring

/-! ## 4×4 Dirac 质量方程代数层（#58，Cl(1,3) 完整签名）"""
rep(anchor, mass_shell_defs, tag="mass_shell_defs")

# ---- 9. 666 块：norm_num 用 ℂ 版（rw diracOp4_sq 后目标是 ℂ 标量等式） ----
rep("""  rw [diracOp4_sq]
  norm_num [mass_shell m φ]""",
"""  rw [diracOp4_sq]
  norm_num [mass_shell_complex m φ]""",
tag="diracOp4_mass_shell")

# ---- 10. 674/695/701/714 块：加 Fin.sum_univ_succ + ℂ 版 mass_shell ----
rep("""  all_goals
    simp [DiracOp4, gamma0, gamma1, Matrix.mul_apply]
    ring_nf
    norm_num [mass_shell m φ]""",
"""  all_goals
    simp [DiracOp4, gamma0, gamma1, Matrix.mul_apply, Fin.sum_univ_succ]
    ring_nf
    norm_num [mass_shell_complex m φ]""",
count=3, tag="dirac_Complex_mass_shell")

with io.open(path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(src)
print("WROTE", path, f"(changed {len(orig)!=len(src)})")
