/-
  NGKMOneIdentity.lean — 恒等 N_gen+k_max−1 = 幂基·静默 + 织³ 纯素基分解（104az-162）
  =======================================================

  I1：框架恒等 N_gen + k_max − 1 = 幂基 × 静默单元 = 10
       N_gen = 3、k_max = 8、幂基 = 2、静默单元 = 5
       3 + 8 − 1 = 10 = 2·5
  I2：织 = N_gen²/(幂基·静默单元) = 9/10
       （104az-67 形式 (N_gen²/(N_gen+k_max−1))³ 的简化等价——104az-162 新表达）
  I3：织³ = (9/10)³ = 729/1000——纯素基 {2,3,5}（729 = 3⁶、1000 = 2³·5³）
  I4：织³ 幂展开 = N_gen⁶/(幂基³·静默³)——与 LambdaGapIdentity L3 的 N_gen⁶/10³ 同构

  先证伪再证明（模式 8）：scripts/falsify_ngkm1.py Fraction 精确检验全部通过
  （LHS = RHS = 10、织 = 9/10、织³ = 729/1000、3⁶/(2³·5³) = 729/1000，exit 0）。

  状态：纯代数恒等（norm_num 闭合，零 sorry）
-/

import Mathlib.Tactic

namespace MUFPF.NGKMOne

/-! =========================================================
    基础常数
   ========================================================= -/

/-- 代数数 N_gen = 3。 -/
noncomputable def Ngen : ℝ := 3

/-- k_max = 2^N_active = 8。 -/
noncomputable def kmax : ℝ := 8

/-- 幂基 = 2。 -/
noncomputable def Powers : ℝ := 2

/-- 静默单元 = 5。 -/
noncomputable def SilenceUnit : ℝ := 5

/-! =========================================================
    I1：恒等 N_gen + k_max − 1 = 幂基 × 静默单元 = 10
   ========================================================= -/

/-- N_gen + k_max − 1 = 幂基 × 静默单元（10 = 10——104az-162 框架新恒等）。 -/
theorem ngkm1_eq_powers_silence : Ngen + kmax - 1 = Powers * SilenceUnit := by
  rw [Ngen, kmax, Powers, SilenceUnit]
  norm_num

/-- N_gen + k_max − 1 = 10 显式（与 LambdaGapIdentity.ten_eq_sum 同值）。 -/
theorem ngkm1_eq_ten : Ngen + kmax - 1 = (10 : ℝ) := by
  rw [Ngen, kmax]
  norm_num

/-! =========================================================
    I2：织 = N_gen²/(幂基·静默单元) = 9/10
   ========================================================= -/

/-- 织 = N_gen²/(幂基·静默单元) = 9/10（104az-162 简化表达——分子分母全框架量）。 -/
theorem weave_eq_nine_tenths :
    Ngen ^ 2 / (Powers * SilenceUnit) = (9 : ℝ) / 10 := by
  rw [Ngen, Powers, SilenceUnit]
  norm_num

/-- 织的 LambdaGap 等价：N_gen²/(N_gen+k_max−1) ≡ N_gen²/(幂基·静默单元)（两形式同值）。 -/
theorem weave_ngkm1_equiv :
    Ngen ^ 2 / (Ngen + kmax - 1) = Ngen ^ 2 / (Powers * SilenceUnit) := by
  congr 1
  exact ngkm1_eq_powers_silence

/-! =========================================================
    I3：织³ = (9/10)³ = 729/1000
   ========================================================= -/

/-- 织³ = 729/1000（729 = 3⁶、1000 = 2³·5³——纯素基 {2,3,5}）。 -/
theorem weave_cubed_rational :
    (Ngen ^ 2 / (Powers * SilenceUnit)) ^ 3 = (729 : ℝ) / 1000 := by
  rw [Ngen, Powers, SilenceUnit]
  norm_num

/-! =========================================================
    I4：织³ 幂展开 = N_gen⁶/(幂基³·静默³)——纯素基分解
   ========================================================= -/

/-- 织³ = N_gen⁶/(幂基³·静默³) = 729/(8·125)（LambdaGapIdentity.fnp_base_Ngen_power 同构）。 -/
theorem weave_cubed_decomposed :
    (Ngen ^ 2 / (Powers * SilenceUnit)) ^ 3 =
      Ngen ^ 6 / (Powers ^ 3 * SilenceUnit ^ 3) := by
  rw [Ngen, Powers, SilenceUnit]
  norm_num

end MUFPF.NGKMOne
