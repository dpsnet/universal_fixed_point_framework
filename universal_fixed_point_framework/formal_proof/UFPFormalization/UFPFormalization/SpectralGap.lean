import Mathlib.Data.Real.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic

open Matrix
open Real

namespace UFPFormalization

/-!
# Spectral Gap Δλ_min: From Cl(1,7) to First Principles Derivation

The spectral gap Δλ_min = λ₂ - λ₁ is determined by:
  1. SU(2) representation → λ_k ∝ √{k(k+1)}  (A_GR eigenvalue spectrum)
  2. Cl(1,7) ≅ M₈(ℝ) → k_max = 8
  3. Normalization: λ_max = M_Pl (Planck cutoff)

This file provides the minimal definitions needed for the deviation bound.
Numerical bounds (0.121 < Δλ_min < 0.123) are verified in `paper36_spectral_gap_derivation.py`.
-/

/-- The minimal faithful representation dimension of Cl(1,7): Cl(1,7) ≅ M₈(ℝ) has dimension 8. -/
def cl17_rep_dim : ℕ := 8

/-- Normalized A_GR eigenvalues from SU(2) representation theory.
    λ_k = √{k(k+1)} / √{k_max(k_max+1)} for k = 1, ..., k_max. -/
noncomputable def agEigenvalue (k k_max : ℕ) : ℝ :=
  if h : k ≥ 1 ∧ k ≤ k_max then
    Real.sqrt ((k : ℝ) * ((k : ℝ) + 1)) / Real.sqrt ((k_max : ℝ) * ((k_max : ℝ) + 1))
  else
    0

/-- The spectral gap: Δλ_min = λ₂ - λ₁ for k_max = 8 (the Cl(1,7) value).
    Analytic formula: Δλ_min(8) = (√6 - √2) / √72 ≈ 0.122... M_Pl. -/
noncomputable def spectralGap (k_max : ℕ) : ℝ :=
  agEigenvalue 2 k_max - agEigenvalue 1 k_max

/-- Analytic formula for the spectral gap at k_max = 8:
    Δλ_min(8) = (√6 - √2) / √72. -/
theorem spectralGap_at_kmax8 : spectralGap 8 = (Real.sqrt 6 - Real.sqrt 2) / Real.sqrt (72 : ℝ) := by
  unfold spectralGap agEigenvalue
  have h72pos : Real.sqrt (72 : ℝ) ≠ 0 := by positivity
  simp [show Real.sqrt ((2 : ℝ) * ((2 : ℝ) + 1)) = Real.sqrt 6 by norm_num,
        show Real.sqrt ((1 : ℝ) * ((1 : ℝ) + 1)) = Real.sqrt 2 by norm_num,
        show Real.sqrt ((8 : ℝ) * ((8 : ℝ) + 1)) = Real.sqrt 72 by norm_num]
  field_simp [h72pos]
  ring

/-- The spectral gap value is approximately 0.122 (numerically verified). -/
theorem spectralGap_approx_value : spectralGap 8 > 0.12 := by
  rw [spectralGap_at_kmax8]
  have h_sqrt2_lt : Real.sqrt 2 < 1.42 := by
    calc
      Real.sqrt 2 < Real.sqrt ((1.42 : ℝ) ^ 2) := Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
      _ = 1.42 := by norm_num
  have h_sqrt6_gt : Real.sqrt 6 > 2.44 := by
    calc
      2.44 = Real.sqrt ((2.44 : ℝ) ^ 2) := by norm_num
      _ < Real.sqrt 6 := Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  have h_sqrt72_lt : Real.sqrt (72 : ℝ) < 8.5 := by
    calc
      Real.sqrt (72 : ℝ) < Real.sqrt ((8.5 : ℝ) ^ 2) := Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
      _ = 8.5 := by norm_num
  have h_numer_gt : Real.sqrt 6 - Real.sqrt 2 > 1.02 := by
    nlinarith
  have h72pos : 0 < Real.sqrt (72 : ℝ) := by positivity
  have h_mul : 0.12 * Real.sqrt (72 : ℝ) < Real.sqrt 6 - Real.sqrt 2 := by
    calc
      0.12 * Real.sqrt (72 : ℝ) < 0.12 * 8.5 := by nlinarith
      _ = 1.02 := by norm_num
      _ < Real.sqrt 6 - Real.sqrt 2 := h_numer_gt
  have h72pos' : Real.sqrt (72 : ℝ) > 0 := h72pos
  field_simp [h72pos.ne']
  nlinarith

end UFPFormalization
