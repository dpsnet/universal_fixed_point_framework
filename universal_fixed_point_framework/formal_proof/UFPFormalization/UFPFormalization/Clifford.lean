import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Complex.Basic

namespace UFPFormalization

/-- Generator of Cl(0,1): a 2×2 real matrix squaring to the identity. -/
def e_01 : Matrix (Fin 2) (Fin 2) ℝ
  | 0, 0 => 1
  | 0, 1 => 0
  | 1, 0 => 0
  | 1, 1 => -1
  | _, _ => 0

/-- Generator of Cl(1,0): a 2×2 real matrix squaring to minus the identity. -/
def e_10 : Matrix (Fin 2) (Fin 2) ℝ
  | 0, 0 => 0
  | 0, 1 => -1
  | 1, 0 => 1
  | 1, 1 => 0
  | _, _ => 0

/-- First generator of Cl(2,0): a 2×2 complex matrix. -/
def e1_20 : Matrix (Fin 2) (Fin 2) ℂ
  | 0, 0 => 0
  | 0, 1 => 1
  | 1, 0 => 1
  | 1, 1 => 0
  | _, _ => 0

/-- Second generator of Cl(2,0): a 2×2 complex matrix. -/
def e2_20 : Matrix (Fin 2) (Fin 2) ℂ
  | 0, 0 => 0
  | 0, 1 => -Complex.I
  | 1, 0 => Complex.I
  | 1, 1 => 0
  | _, _ => 0

private lemma sum_fin_two {α : Type} [AddCommMonoid α] (f : Fin 2 → α) :
    ∑ x : Fin 2, f x = f 0 + f 1 := by
  rw [Finset.sum_fin_eq_sum_range, Finset.sum_range_succ, Finset.sum_range_one]
  simp

/-- Verification that e_01 squares to the identity. -/
theorem e_01_sq : e_01 * e_01 = 1 := by
  funext i j
  fin_cases i <;> fin_cases j <;> simp [e_01, Matrix.mul_apply, sum_fin_two]
  all_goals norm_num

/-- Verification that e_10 squares to minus the identity. -/
theorem e_10_sq : e_10 * e_10 = -1 := by
  funext i j
  fin_cases i <;> fin_cases j <;> simp [e_10, Matrix.mul_apply, sum_fin_two]
  all_goals norm_num

/-- The two Cl(2,0) generators anticommute. -/
theorem e_20_anticomm : e1_20 * e2_20 = - (e2_20 * e1_20) := by
  funext i j
  fin_cases i <;> fin_cases j <;> simp [e1_20, e2_20, Matrix.mul_apply, sum_fin_two, Complex.I_mul_I]
  all_goals norm_num

/-- Verification that e1_20 squares to the identity. -/
theorem e1_20_sq : e1_20 * e1_20 = 1 := by
  funext i j
  fin_cases i <;> fin_cases j <;> simp [e1_20, Matrix.mul_apply, sum_fin_two]
  all_goals norm_num

/-- Verification that e2_20 squares to the identity. -/
theorem e2_20_sq : e2_20 * e2_20 = 1 := by
  funext i j
  fin_cases i <;> fin_cases j <;> simp [e2_20, Matrix.mul_apply, sum_fin_two, Complex.I_mul_I]
  all_goals norm_num

end UFPFormalization
