import UFPFormalization.BlackHoleEvolution
import UFPFormalization.SpectralGap
import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real

open Real

namespace UFPFormalization

/-!
# Hawking Radiation Spectrum (P1-3 §2 extension)

Formalization of Hawking radiation from spectral principles:
  - Greybody factor Γ(ω, M) for transmission through potential barrier
  - QNM spectrum ω_n from A_GR eigenvalues
  - Radiation power spectrum dP/dω

Based on:
  - Paper 8 §4: QNM spectrum from A_GR eigenvalue problem
  - paper27_hawking_evaporation.py: numerical greybody model
  - Hawking (1975): original radiation spectrum
-/

/-!
## §0: Helper Lemmas
-/

/-- Helper: C/M is strictly decreasing in M for C > 0. -/
theorem div_constant_decreasing (C M₁ M₂ : ℝ) (hC : 0 < C)
    (hM₁ : 0 < M₁) (hM₂ : 0 < M₂) (hlt : M₁ < M₂) :
    C / M₁ > C / M₂ := by
  have hden_pos : (0 : ℝ) < M₁ * M₂ := mul_pos hM₁ hM₂
  have hdiff_pos : (0 : ℝ) < M₂ - M₁ := by linarith
  have hnum_pos : (0 : ℝ) < C * (M₂ - M₁) := mul_pos hC hdiff_pos
  have hM1_ne : M₁ ≠ 0 := ne_of_gt hM₁
  have hM2_ne : M₂ ≠ 0 := ne_of_gt hM₂
  have hform : C / M₁ - C / M₂ = C * (M₂ - M₁) / (M₁ * M₂) := by
    field_simp [hM1_ne, hM2_ne]
  have hgt : (0 : ℝ) < C * (M₂ - M₁) / (M₁ * M₂) := div_pos hnum_pos hden_pos
  linarith [hform.symm, hgt]

/-- Helper: C/M² is strictly decreasing in M for C > 0. -/
theorem div_constant_sq_decreasing (C M₁ M₂ : ℝ) (hC : 0 < C)
    (hM₁ : 0 < M₁) (hM₂ : 0 < M₂) (hlt : M₁ < M₂) :
    C / M₁^2 > C / M₂^2 := by
  have hM1sq_pos : (0 : ℝ) < M₁^2 := sq_pos_of_pos hM₁
  have hM2sq_pos : (0 : ℝ) < M₂^2 := sq_pos_of_pos hM₂
  have hden_pos : (0 : ℝ) < M₁^2 * M₂^2 := mul_pos hM1sq_pos hM2sq_pos
  have hsqdiff_pos : (0 : ℝ) < M₂^2 - M₁^2 := by nlinarith
  have hnum_pos : (0 : ℝ) < C * (M₂^2 - M₁^2) := mul_pos hC hsqdiff_pos
  have hM1sq_ne : M₁^2 ≠ 0 := ne_of_gt hM1sq_pos
  have hM2sq_ne : M₂^2 ≠ 0 := ne_of_gt hM2sq_pos
  have hform : C / M₁^2 - C / M₂^2 = C * (M₂^2 - M₁^2) / (M₁^2 * M₂^2) := by
    field_simp [hM1sq_ne, hM2sq_ne]
  have hgt : (0 : ℝ) < C * (M₂^2 - M₁^2) / (M₁^2 * M₂^2) := div_pos hnum_pos hden_pos
  linarith [hform.symm, hgt]

/-!
## §1: Greybody Factor

The greybody factor Γ_l(ω) is the transmission probability for a mode
of frequency ω through the Schwarzschild potential barrier.

For l=2 (dominant gravitational wave mode):
  Γ(ω, M) = (27/4)·(ωM)² · exp(-4ωM)  for ωM > 0
-/

/-- Greybody factor Γ(ω, M) for ω > 0, M > 0. -/
noncomputable def greybodyFactor (ω M : ℝ) : ℝ :=
  let x := ω * M
  (27 / 4 : ℝ) * x^2 * Real.exp (-4 * x)

/-- Greybody factor is positive for ω > 0, M > 0. -/
theorem greybodyFactor_pos (ω M : ℝ) (hω : 0 < ω) (hM : 0 < M) :
    0 < greybodyFactor ω M := by
  have hx_pos : (0 : ℝ) < ω * M := mul_pos hω hM
  have hxsq_pos : (0 : ℝ) < (ω * M)^2 := sq_pos_of_pos hx_pos
  have hexp_pos : (0 : ℝ) < Real.exp (-4 * (ω * M)) := Real.exp_pos (-4 * (ω * M))
  have hcoeff_pos : (0 : ℝ) < (27 / 4 : ℝ) := by norm_num
  exact mul_pos (mul_pos hcoeff_pos hxsq_pos) hexp_pos

/-- Greybody factor is zero when ω = 0. -/
theorem greybodyFactor_zero (ω M : ℝ) (hω : ω = 0) :
    greybodyFactor ω M = 0 := by
  unfold greybodyFactor
  rw [hω]
  simp

/-!
## §2: QNM Spectrum

Quasi-Normal Mode frequencies from A_GR eigenvalue problem.
-/

/-- QNM real frequency index: l + 1/2 + n. -/
noncomputable def qnmRealFreqIndex (l n : ℝ) : ℝ :=
  l + 1 / 2 + n

/-- QNM real part: Re(ω_n) = Δλ_min·(l + 1/2 + n). -/
noncomputable def qnmRealPart (l n : ℝ) : ℝ :=
  spectralGap 8 * qnmRealFreqIndex l n

/-- QNM damping coefficient. -/
noncomputable def qnmDamping (l n γ₀ : ℝ) : ℝ :=
  qnmRealFreqIndex l n * γ₀

/-- QNM imaginary part. -/
noncomputable def qnmImagPart (l n γ₀ : ℝ) : ℝ :=
  -spectralGap 8 * qnmDamping l n γ₀

/-- QNM real part is positive for l ≥ 0, n ≥ 0. -/
theorem qnmRealPart_pos (l n : ℝ) (hl : 0 ≤ l) (hn : 0 ≤ n) :
    0 < qnmRealPart l n := by
  unfold qnmRealPart
  have hgap_pos : 0 < spectralGap 8 := spectralGap8_pos
  have h_idx_pos : (0 : ℝ) < qnmRealFreqIndex l n := by
    unfold qnmRealFreqIndex
    linarith
  exact mul_pos hgap_pos h_idx_pos

/-- QNM real part is increasing in n. -/
theorem qnmRealPart_increasing_n (l n₁ n₂ : ℝ)
    (hn : n₁ < n₂) (hl_nonneg : 0 ≤ l) :
    qnmRealPart l n₁ < qnmRealPart l n₂ := by
  unfold qnmRealPart qnmRealFreqIndex
  have hgap_pos : 0 < spectralGap 8 := spectralGap8_pos
  have hlt : l + 1 / 2 + n₁ < l + 1 / 2 + n₂ := by linarith
  exact mul_lt_mul_of_pos_left hlt hgap_pos

/-- QNM real part is increasing in l. -/
theorem qnmRealPart_increasing_l (l₁ l₂ n : ℝ)
    (hl : l₁ < l₂) (hn_nonneg : 0 ≤ n) :
    qnmRealPart l₁ n < qnmRealPart l₂ n := by
  unfold qnmRealPart qnmRealFreqIndex
  have hgap_pos : 0 < spectralGap 8 := spectralGap8_pos
  have hlt : l₁ + 1 / 2 + n < l₂ + 1 / 2 + n := by linarith
  exact mul_lt_mul_of_pos_left hlt hgap_pos

/-!
## §3: Hawking Radiation Power Spectrum

dP/dω = ω³·Γ(ω,M)·N(ω,T_H) / (2π²)
-/

/-- Hawking radiation power density. -/
noncomputable def hawkingPowerDensity (ω M : ℝ) (hM : 0 < M) : ℝ :=
  let Γ := greybodyFactor ω M
  let N := planckOccupation M ω hM
  ω^3 * Γ * N / (2 * Real.pi^2)

/-- ω³ > 0 when ω > 0. -/
private lemma hω3_pos (ω : ℝ) (hω : 0 < ω) : 0 < ω^3 := by
  have hω2 : (0 : ℝ) < ω^2 := sq_pos_of_pos hω
  nlinarith

/-- Power density is positive for ω > 0, M > 0. -/
theorem hawkingPowerDensity_pos (ω M : ℝ)
    (hω : 0 < ω) (hM : 0 < M) :
    0 < hawkingPowerDensity ω M hM := by
  have hω3_pos' : (0 : ℝ) < ω^3 := hω3_pos ω hω
  have hΓ_pos : (0 : ℝ) < greybodyFactor ω M := greybodyFactor_pos ω M hω hM
  have hN_pos : (0 : ℝ) < planckOccupation M ω hM := planckOccupation_pos M ω hM hω
  have hpi_pos : 0 < Real.pi := Real.pi_pos
  have hpi2_pos : (0 : ℝ) < Real.pi^2 := sq_pos_of_pos hpi_pos
  have hden_pos : (0 : ℝ) < 2 * Real.pi^2 := by linarith
  exact div_pos (mul_pos (mul_pos hω3_pos' hΓ_pos) hN_pos) hden_pos

/-- Total radiated power (semiclassical approximation). -/
noncomputable def hawkingPower (M : ℝ) (_hM : 0 < M) : ℝ :=
  spectralGap 8^4 / (15 * Real.pi * M^2)

/-- Hawking power is positive for M > 0. -/
theorem hawkingPower_pos (M : ℝ) (hM : 0 < M) :
    0 < hawkingPower M hM := by
  have hgap_pos : 0 < spectralGap 8 := spectralGap8_pos
  have hgap4_pos : (0 : ℝ) < spectralGap 8^4 := pow_pos hgap_pos 4
  have hpi_pos : (0 : ℝ) < Real.pi := Real.pi_pos
  have hM2_pos : (0 : ℝ) < M^2 := sq_pos_of_pos hM
  have h15_pos : (0 : ℝ) < (15 : ℝ) := by norm_num
  have hden_pos : (0 : ℝ) < 15 * Real.pi * M^2 := mul_pos (mul_pos h15_pos hpi_pos) hM2_pos
  unfold hawkingPower
  exact div_pos hgap4_pos hden_pos

/-- Hawking power is decreasing with mass (dP/dM < 0). -/
theorem hawkingPower_decreasing (M₁ M₂ : ℝ)
    (hM₁ : 0 < M₁) (hM₂ : 0 < M₂) (hlt : M₁ < M₂) :
    hawkingPower M₁ hM₁ > hawkingPower M₂ hM₂ := by
  have hgap_pos : 0 < spectralGap 8 := spectralGap8_pos
  have hgap4_pos : (0 : ℝ) < spectralGap 8^4 := pow_pos hgap_pos 4
  have hpi_pos : (0 : ℝ) < Real.pi := Real.pi_pos
  have h15_pos : (0 : ℝ) < (15 : ℝ) := by norm_num
  have hC_pos : (0 : ℝ) < spectralGap 8^4 / (15 * Real.pi) := by
    have hden_pos : (0 : ℝ) < 15 * Real.pi := mul_pos h15_pos hpi_pos
    exact div_pos hgap4_pos hden_pos
  have hC : spectralGap 8^4 / (15 * Real.pi * M₁^2) >
            spectralGap 8^4 / (15 * Real.pi * M₂^2) := by
    have hC' : (spectralGap 8^4 / (15 * Real.pi)) / M₁^2 >
               (spectralGap 8^4 / (15 * Real.pi)) / M₂^2 :=
      div_constant_sq_decreasing (spectralGap 8^4 / (15 * Real.pi))
        M₁ M₂ hC_pos hM₁ hM₂ hlt
    simpa [div_div] using hC'
  unfold hawkingPower
  simpa [div_div] using hC

end UFPFormalization
