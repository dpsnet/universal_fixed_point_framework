-- ============================================================
-- UFPF → MUFPF 更名通知
-- ============================================================
-- 本文件属于 Universal Fixed Point Framework (UFPF)。
-- 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
-- 更名计划详见：roadmap/mu_renaming_plan.md
--
-- 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
-- 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
--
-- 本文件中 UFPF 相关引用数量：5
-- 更名将在计划确认后统一执行，当前代码不做修改。
-- ============================================================

import UFPFormalization.BlackHoleEvolution
import UFPFormalization.HawkingSpectrum
import UFPFormalization.SpectralDynamics
import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Sqrt

open Real

namespace UFPFormalization

/-!
# Black Hole Information & Page Curve (P1-3 §3-4)

Formalization of:
  - Bidirectional information preservation via spectral flow
  - Page curve derived from spectral principles (not external Page 1993 assumption)
  - Horizon quantum fluctuations in spectral form

Key physics:
  - Spectral flow A_t = U·A₀·U⁻¹ preserves the spectrum: σ(A_t) = σ(A₀)
  - Page curve: S_ent(t) = min(S_BH(t), S_rad(t)) with S_rad(t) = 4π(M₀²-M(t)²)
  - Page time at M(t)² = M₀²/2, i.e. t_Page/t_evap = 1 - 1/(2√2) ≈ 0.647
-/

/-!
## §1: Bidirectional Information Preservation

Spectral flow A_t = U·A₀·U⁻¹ with U = exp(t·A_F) is invertible,
so σ(A_t) = σ(A₀) in both directions.
-/

private lemma matrix_exp_smul_neg {n : ℕ} (A : Matrix (Fin n) (Fin n) ℂ) (t : ℝ) :
    NormedSpace.exp ((-t) • A) * NormedSpace.exp (t • A) =
      (1 : Matrix (Fin n) (Fin n) ℂ) := by
  have hc : Commute ((-t) • A) (t • A) := by
    simpa [Commute, SemiconjBy, smul_neg] using (Commute.refl (t • A)).neg_right
  rw [← Matrix.exp_add_of_commute ((-t) • A) (t • A) hc]
  simp [smul_neg]

/-- Spectral flow half-group property: flowing back by -t returns to A₀. -/
theorem spectralFlow_inv {n : ℕ} (A₀ A_F : Matrix (Fin n) (Fin n) ℂ) (t : ℝ) :
    spectralFlow (spectralFlow A₀ A_F t) A_F (-t) = A₀ := by
  unfold spectralFlow
  have hnegneg : -(-t) • A_F = t • A_F := by simp
  rw [hnegneg]
  have hsum : NormedSpace.exp ((-t) • A_F) * NormedSpace.exp (t • A_F) =
      (1 : Matrix (Fin n) (Fin n) ℂ) := matrix_exp_smul_neg A_F t
  calc
    NormedSpace.exp ((-t) • A_F) *
        (NormedSpace.exp (t • A_F) * A₀ * NormedSpace.exp ((-t) • A_F)) *
        NormedSpace.exp (t • A_F)
        = (NormedSpace.exp ((-t) • A_F) * NormedSpace.exp (t • A_F)) *
            (A₀ * (NormedSpace.exp ((-t) • A_F) * NormedSpace.exp (t • A_F))) := by
          simp [Matrix.mul_assoc]
    _ = (1 : Matrix (Fin n) (Fin n) ℂ) * (A₀ * (1 : Matrix (Fin n) (Fin n) ℂ)) := by
          rw [hsum]
    _ = A₀ := by simp

/-- Reverse information preservation: σ(A_t) ⊆ σ(A₀). -/
theorem bhInformationPreserved_reverse {n : ℕ}
    (A₀ A_F : Matrix (Fin n) (Fin n) ℂ) (t : ℝ) (a : ℂ)
    (ha : a ∈ Matrix.eigenvalues (spectralFlow A₀ A_F t)) :
    a ∈ Matrix.eigenvalues A₀ := by
  have hback : spectralFlow (spectralFlow A₀ A_F t) A_F (-t) = A₀ := spectralFlow_inv A₀ A_F t
  have h : a ∈ Matrix.eigenvalues (spectralFlow (spectralFlow A₀ A_F t) A_F (-t)) :=
    spectral_invariance (spectralFlow A₀ A_F t) A_F (-t) a ha
  simpa [hback] using h

/-- Complete spectral information preservation: σ(A₀) = σ(A_t). -/
theorem bhInformationPreserved_iff {n : ℕ}
    (A₀ A_F : Matrix (Fin n) (Fin n) ℂ) (t : ℝ) (a : ℂ) :
    a ∈ Matrix.eigenvalues A₀ ↔
      a ∈ Matrix.eigenvalues (spectralFlow A₀ A_F t) := by
  constructor
  · intro h
    exact bhInformationPreserved_forward A₀ A_F t a h
  · intro h
    exact bhInformationPreserved_reverse A₀ A_F t a h

/-!
## §2: Page Curve from Spectral Principles

Radiation entanglement entropy:
  S_rad(t) = 4π·(M₀² - M(t)²)

by purity of the total state: S_total = S_BH + S_rad = 4π·M₀² constant.

Page curve: S_ent(t) = min(S_BH(t), S_rad(t)).
Page time: M(t)² = M₀²/2, giving t_Page/t_evap = 1 - 1/(2√2) ≈ 0.647.
-/

/-- Radiation entanglement entropy: S_rad(t) = 4π(M₀² - M(t)²). -/
noncomputable def bhRadiationEntropy (ev : BHEvol) (t : ℝ)
    (h : 0 < bhMassCubed ev t) : ℝ :=
  4 * Real.pi * (ev.M₀^2 - (bhMass ev t (le_of_lt h))^2)

/-- Black hole entanglement entropy (Page curve): S_ent = min(S_BH, S_rad). -/
noncomputable def bhEntanglementEntropy (ev : BHEvol) (t : ℝ)
    (h : 0 < bhMassCubed ev t) : ℝ :=
  min (bekensteinHawkingEntropySchwarzschild (bhMass ev t (le_of_lt h)))
      (bhRadiationEntropy ev t h)

/-- Total entropy conservation: S_BH(t) + S_rad(t) = 4πM₀². -/
theorem bhEntropy_conservation (ev : BHEvol) (t : ℝ)
    (h : 0 < bhMassCubed ev t) :
    bekensteinHawkingEntropySchwarzschild (bhMass ev t (le_of_lt h)) +
      bhRadiationEntropy ev t h = 4 * Real.pi * ev.M₀^2 := by
  simp [bekensteinHawkingEntropySchwarzschild, bhRadiationEntropy]
  ring

/-- Page time: the time at which M(t)² = M₀²/2. -/
noncomputable def bhPageTime (ev : BHEvol) : ℝ :=
  ev.M₀^3 * (1 - 1 / (2 * Real.sqrt 2)) / (3 * ev.α)

/-- At Page time, the cubed mass is Δ(t_Page) = M₀³/(2√2). -/
theorem bhMassCubed_at_page_time (ev : BHEvol) :
    bhMassCubed ev (bhPageTime ev) = ev.M₀^3 / (2 * Real.sqrt 2) := by
  unfold bhPageTime bhMassCubed
  have hα_ne : ev.α ≠ 0 := ne_of_gt ev.α_pos
  have h3_ne : (3 : ℝ) ≠ 0 := by norm_num
  have hsqrt_ne : Real.sqrt 2 ≠ 0 := by positivity
  field_simp [hα_ne, h3_ne, hsqrt_ne]
  ring

/-- Page time fraction of evaporation time: t_Page/t_evap = 1 - 1/(2√2). -/
theorem bhPageTime_fraction (ev : BHEvol) :
    bhPageTime ev / bhEvaporationTime ev = 1 - 1 / (2 * Real.sqrt 2) := by
  unfold bhPageTime bhEvaporationTime
  have hα_ne : ev.α ≠ 0 := ne_of_gt ev.α_pos
  have h3_ne : (3 : ℝ) ≠ 0 := by norm_num
  have hM0_ne : ev.M₀ ≠ 0 := ne_of_gt ev.M₀_pos
  field_simp [hα_ne, h3_ne, hM0_ne]

/-- √2 > 1. -/
private lemma sqrt2_gt_one : (1 : ℝ) < Real.sqrt 2 := by
  have hsq : (1 : ℝ)^2 < (Real.sqrt 2)^2 := by
    rw [Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)]
    norm_num
  nlinarith [Real.sqrt_nonneg 2]

/-- √2 < 2. -/
private lemma sqrt2_lt_two : Real.sqrt 2 < (2 : ℝ) := by
  have hsq : (Real.sqrt 2)^2 < (2 : ℝ)^2 := by
    rw [Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)]
    norm_num
  nlinarith [Real.sqrt_nonneg 2]

/-- Page time occurs after half of the evaporation: 1/2 < t_Page/t_evap. -/
theorem bhPageTime_fraction_gt_half :
    (1 / 2 : ℝ) < 1 - 1 / (2 * Real.sqrt 2) := by
  have hsmall : 1 / (2 * Real.sqrt 2) < 1 / 2 := by
    have hpos : (0 : ℝ) < 2 * Real.sqrt 2 := by positivity
    have hfrac : 1 / (2 * Real.sqrt 2) * (2 * Real.sqrt 2) = 1 := by field_simp
    have htwo_frac : (1 / 2 : ℝ) * (2 * Real.sqrt 2) = Real.sqrt 2 := by field_simp
    have hlt : 1 / (2 * Real.sqrt 2) * (2 * Real.sqrt 2) < (1 / 2) * (2 * Real.sqrt 2) := by
      rw [hfrac, htwo_frac]
      exact sqrt2_gt_one
    exact lt_of_mul_lt_mul_right hlt (le_of_lt hpos)
  linarith

/-- Page time occurs before three quarters of the evaporation: t_Page/t_evap < 3/4. -/
theorem bhPageTime_fraction_lt_three_quarters :
    1 - 1 / (2 * Real.sqrt 2) < 3 / 4 := by
  have hbig : (1 / 4 : ℝ) < 1 / (2 * Real.sqrt 2) := by
    have hpos : (0 : ℝ) < 2 * Real.sqrt 2 := by positivity
    have hfrac : 1 / (2 * Real.sqrt 2) * (2 * Real.sqrt 2) = 1 := by field_simp
    have hfour_frac : (1 / 4 : ℝ) * (2 * Real.sqrt 2) = Real.sqrt 2 / 2 := by ring
    have hlt : (1 / 4 : ℝ) * (2 * Real.sqrt 2) < 1 / (2 * Real.sqrt 2) * (2 * Real.sqrt 2) := by
      rw [hfour_frac, hfrac]
      have : Real.sqrt 2 / 2 < 1 := by
        have hlt2 : Real.sqrt 2 < (2 : ℝ) := sqrt2_lt_two
        linarith
      exact this
    exact lt_of_mul_lt_mul_right hlt (le_of_lt hpos)
  linarith

/-- Early phase (M(t+dt)² ≥ M₀²/2): S_ent = S_rad, increasing in time.
    The condition at the later time t+dt implies it holds at t (since M_t > M_t2). -/
theorem bhEntanglementEntropy_early_increasing (ev : BHEvol) (t dt : ℝ)
    (hdt : 0 < dt)
    (h_pos : 0 < bhMassCubed ev t) (h_pos2 : 0 < bhMassCubed ev (t + dt))
    (h_early : (1 / 2 : ℝ) * ev.M₀^2 ≤ (bhMass ev (t + dt) (le_of_lt h_pos2))^2) :
    bhEntanglementEntropy ev t h_pos < bhEntanglementEntropy ev (t + dt) h_pos2 := by
  set M_t := bhMass ev t (le_of_lt h_pos) with hMt
  set M_t2 := bhMass ev (t + dt) (le_of_lt h_pos2) with hMt2
  have hMt_pos : 0 < M_t := bhMass_pos ev t h_pos
  have hMt2_pos : 0 < M_t2 := bhMass_pos ev (t + dt) h_pos2
  have h_mass_strict : M_t2 < M_t := bhMass_decreasing ev t dt hdt h_pos h_pos2
  have hMsq_lt : M_t2^2 < M_t^2 := by
    have h1 : (0 : ℝ) < M_t2^2 := sq_pos_of_pos hMt2_pos
    have h2 : (0 : ℝ) < M_t^2 := sq_pos_of_pos hMt_pos
    nlinarith
  have h_early_t : (1 / 2 : ℝ) * ev.M₀^2 ≤ M_t^2 := by
    have hM2_ge : (1 / 2 : ℝ) * ev.M₀^2 ≤ M_t2^2 := by simpa [hMt2] using h_early
    linarith
  have hS_BH_ge : bekensteinHawkingEntropySchwarzschild M_t ≥ bhRadiationEntropy ev t h_pos := by
    unfold bekensteinHawkingEntropySchwarzschild bhRadiationEntropy
    have : 4 * Real.pi * M_t^2 ≥ 4 * Real.pi * (ev.M₀^2 - M_t^2) := by
      have hpi_pos : 0 < Real.pi := Real.pi_pos
      have h4pi_pos : (0 : ℝ) < 4 * Real.pi := mul_pos (by norm_num : (0 : ℝ) < 4) hpi_pos
      have hm : (1 / 2 : ℝ) * ev.M₀^2 ≤ M_t^2 := h_early_t
      have : (ev.M₀^2 - M_t^2) ≤ M_t^2 := by linarith
      exact mul_le_mul_of_nonneg_left this (le_of_lt h4pi_pos)
    simpa [hMt] using this
  have hmin_t : bhEntanglementEntropy ev t h_pos = bhRadiationEntropy ev t h_pos := by
    unfold bhEntanglementEntropy
    have hS : bhRadiationEntropy ev t h_pos ≤
        bekensteinHawkingEntropySchwarzschild (bhMass ev t (le_of_lt h_pos)) := by
      simpa [hMt] using hS_BH_ge
    exact min_eq_right hS
  have hS_rad_lt : bhRadiationEntropy ev t h_pos < bhRadiationEntropy ev (t + dt) h_pos2 := by
    unfold bhRadiationEntropy
    have hpi_pos : 0 < Real.pi := Real.pi_pos
    have h4pi_pos : (0 : ℝ) < 4 * Real.pi := mul_pos (by norm_num : (0 : ℝ) < 4) hpi_pos
    have hdiff : ev.M₀^2 - M_t^2 < ev.M₀^2 - M_t2^2 := by linarith
    have hgt : (4 * Real.pi : ℝ) * (ev.M₀^2 - M_t^2) < (4 * Real.pi) * (ev.M₀^2 - M_t2^2) := by
      exact mul_lt_mul_of_pos_left hdiff h4pi_pos
    simpa [hMt, hMt2] using hgt
  have hS_BH_ge2 : bekensteinHawkingEntropySchwarzschild M_t2 ≥ bhRadiationEntropy ev (t + dt) h_pos2 := by
    unfold bekensteinHawkingEntropySchwarzschild bhRadiationEntropy
    have : 4 * Real.pi * M_t2^2 ≥ 4 * Real.pi * (ev.M₀^2 - M_t2^2) := by
      have hpi_pos : 0 < Real.pi := Real.pi_pos
      have h4pi_pos : (0 : ℝ) < 4 * Real.pi := mul_pos (by norm_num : (0 : ℝ) < 4) hpi_pos
      have hm : (1 / 2 : ℝ) * ev.M₀^2 ≤ M_t2^2 := by simpa [hMt2] using h_early
      have : (ev.M₀^2 - M_t2^2) ≤ M_t2^2 := by linarith
      exact mul_le_mul_of_nonneg_left this (le_of_lt h4pi_pos)
    simpa [hMt2] using this
  have hmin_t2 : bhEntanglementEntropy ev (t + dt) h_pos2 = bhRadiationEntropy ev (t + dt) h_pos2 := by
    unfold bhEntanglementEntropy
    have hS : bhRadiationEntropy ev (t + dt) h_pos2 ≤
        bekensteinHawkingEntropySchwarzschild (bhMass ev (t + dt) (le_of_lt h_pos2)) := by
      simpa [hMt2] using hS_BH_ge2
    exact min_eq_right hS
  linarith

/-- Late phase (M(t)² ≤ M₀²/2): S_ent = S_BH, decreasing in time. -/
theorem bhEntanglementEntropy_late_decreasing (ev : BHEvol) (t dt : ℝ)
    (hdt : 0 < dt)
    (h_pos : 0 < bhMassCubed ev t) (h_pos2 : 0 < bhMassCubed ev (t + dt))
    (h_late : (bhMass ev t (le_of_lt h_pos))^2 ≤ (1 / 2 : ℝ) * ev.M₀^2) :
    bhEntanglementEntropy ev (t + dt) h_pos2 < bhEntanglementEntropy ev t h_pos := by
  set M_t := bhMass ev t (le_of_lt h_pos) with hMt
  set M_t2 := bhMass ev (t + dt) (le_of_lt h_pos2) with hMt2
  have hMt_pos : 0 < M_t := bhMass_pos ev t h_pos
  have hMt2_pos : 0 < M_t2 := bhMass_pos ev (t + dt) h_pos2
  have h_mass_strict : M_t2 < M_t := bhMass_decreasing ev t dt hdt h_pos h_pos2
  have hMsq_lt : M_t2^2 < M_t^2 := by
    have h1 : (0 : ℝ) < M_t2^2 := sq_pos_of_pos hMt2_pos
    have h2 : (0 : ℝ) < M_t^2 := sq_pos_of_pos hMt_pos
    nlinarith
  have h_late_t2 : M_t2^2 ≤ (1 / 2 : ℝ) * ev.M₀^2 := by
    have hM_lt : (1 / 2 : ℝ) * ev.M₀^2 ≥ M_t^2 := by simpa [hMt] using h_late
    linarith
  have hS_BH_le : bekensteinHawkingEntropySchwarzschild M_t ≤ bhRadiationEntropy ev t h_pos := by
    unfold bekensteinHawkingEntropySchwarzschild bhRadiationEntropy
    have : 4 * Real.pi * M_t^2 ≤ 4 * Real.pi * (ev.M₀^2 - M_t^2) := by
      have hpi_pos : 0 < Real.pi := Real.pi_pos
      have h4pi_pos : (0 : ℝ) < 4 * Real.pi := mul_pos (by norm_num : (0 : ℝ) < 4) hpi_pos
      have hm : M_t^2 ≤ (1 / 2 : ℝ) * ev.M₀^2 := by simpa [hMt] using h_late
      have : M_t^2 ≤ (ev.M₀^2 - M_t^2) := by linarith
      exact mul_le_mul_of_nonneg_left this (le_of_lt h4pi_pos)
    simpa [hMt] using this
  have hmin_t : bhEntanglementEntropy ev t h_pos = bekensteinHawkingEntropySchwarzschild M_t := by
    unfold bhEntanglementEntropy
    have hS : bekensteinHawkingEntropySchwarzschild (bhMass ev t (le_of_lt h_pos)) ≤
        bhRadiationEntropy ev t h_pos := by
      simpa [hMt] using hS_BH_le
    exact min_eq_left hS
  have hS_BH_lt : bekensteinHawkingEntropySchwarzschild M_t2 < bekensteinHawkingEntropySchwarzschild M_t :=
    bhEntropySchwarzschild_increasing M_t2 M_t hMt2_pos hMt_pos h_mass_strict
  have hS_BH_le2 : bekensteinHawkingEntropySchwarzschild M_t2 ≤ bhRadiationEntropy ev (t + dt) h_pos2 := by
    unfold bekensteinHawkingEntropySchwarzschild bhRadiationEntropy
    have : 4 * Real.pi * M_t2^2 ≤ 4 * Real.pi * (ev.M₀^2 - M_t2^2) := by
      have hpi_pos : 0 < Real.pi := Real.pi_pos
      have h4pi_pos : (0 : ℝ) < 4 * Real.pi := mul_pos (by norm_num : (0 : ℝ) < 4) hpi_pos
      have hm : M_t2^2 ≤ (1 / 2 : ℝ) * ev.M₀^2 := h_late_t2
      have : M_t2^2 ≤ (ev.M₀^2 - M_t2^2) := by linarith
      exact mul_le_mul_of_nonneg_left this (le_of_lt h4pi_pos)
    simpa [hMt2] using this
  have hmin_t2 : bhEntanglementEntropy ev (t + dt) h_pos2 = bekensteinHawkingEntropySchwarzschild M_t2 := by
    unfold bhEntanglementEntropy
    have hS : bekensteinHawkingEntropySchwarzschild (bhMass ev (t + dt) (le_of_lt h_pos2)) ≤
        bhRadiationEntropy ev (t + dt) h_pos2 := by
      simpa [hMt2] using hS_BH_le2
    exact min_eq_left hS
  linarith

/-- Page curve cubic criterion: at Page time, M(t)³ = M₀³/(2√2).
    This is the spectral derivation of the Page time. -/
theorem bhPageTime_cubic_criterion (ev : BHEvol) :
    bhMassCubed ev (bhPageTime ev) = ev.M₀^3 / (2 * Real.sqrt 2) :=
  bhMassCubed_at_page_time ev

/-- rpow division property for nonnegative numerator and denominator. -/
private lemma rpow_div_nonneg (x y z : ℝ) (hx : 0 ≤ x) (hy : 0 ≤ y) :
    Real.rpow (x / y) z = Real.rpow x z / Real.rpow y z :=
  Real.div_rpow hx hy z

/-- √2 squared equals 2. -/
private lemma sqrt2_sq : (Real.sqrt 2)^2 = (2 : ℝ) :=
  Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)

/-- Exact entropy balance at Page time: S_BH(t_Page) = S_rad(t_Page),
    i.e. M(t_Page)² = M₀²/2. Previously an open item pending rpow algebra;
    now proven via the cube-root identity rpow_cube_root. -/
theorem bhPageTime_entropy_balance (ev : BHEvol)
    (h_page : 0 < bhMassCubed ev (bhPageTime ev)) :
    bekensteinHawkingEntropySchwarzschild (bhMass ev (bhPageTime ev) (le_of_lt h_page)) =
      bhRadiationEntropy ev (bhPageTime ev) h_page := by
  have hΔ : bhMassCubed ev (bhPageTime ev) = ev.M₀^3 / (2 * Real.sqrt 2) :=
    bhMassCubed_at_page_time ev
  have hM0_pos : 0 < ev.M₀ := ev.M₀_pos
  have hM0cubed : (0 : ℝ) < ev.M₀^3 := pow_pos hM0_pos 3
  have hsqrt_pos : (0 : ℝ) < Real.sqrt 2 := Real.sqrt_pos.2 (by norm_num : (0 : ℝ) < 2)
  have hsqrt_nonneg : (0 : ℝ) ≤ Real.sqrt 2 := le_of_lt hsqrt_pos
  have hden_nonneg : (0 : ℝ) ≤ 2 * Real.sqrt 2 :=
    mul_nonneg (by norm_num : (0 : ℝ) ≤ 2) hsqrt_nonneg
  have hM : bhMass ev (bhPageTime ev) (le_of_lt h_page) = ev.M₀ / Real.sqrt 2 := by
    unfold bhMass
    rw [hΔ]
    calc
      Real.rpow (ev.M₀^3 / (2 * Real.sqrt 2)) (1 / 3)
          = Real.rpow (ev.M₀^3) (1 / 3) / Real.rpow (2 * Real.sqrt 2) (1 / 3) :=
            rpow_div_nonneg (ev.M₀^3) (2 * Real.sqrt 2) (1 / 3) (le_of_lt hM0cubed) hden_nonneg
      _ = ev.M₀ / Real.rpow (2 * Real.sqrt 2) (1 / 3) := by
            rw [rpow_cube_root ev.M₀ hM0_pos]
      _ = ev.M₀ / Real.sqrt 2 := by
            have h2sq : 2 * Real.sqrt 2 = (Real.sqrt 2)^3 := by
              rw [pow_three]
              nlinarith [sqrt2_sq]
            rw [h2sq]
            rw [rpow_cube_root (Real.sqrt 2) hsqrt_pos]
  have hMsq : (bhMass ev (bhPageTime ev) (le_of_lt h_page))^2 = (1 / 2 : ℝ) * ev.M₀^2 := by
    rw [hM]
    have hsqrt_ne : Real.sqrt 2 ≠ 0 := ne_of_gt hsqrt_pos
    field_simp [hsqrt_ne]
    rw [sqrt2_sq]
  unfold bekensteinHawkingEntropySchwarzschild bhRadiationEntropy
  rw [hMsq]
  ring

/-!
## §3: Horizon Quantum Fluctuations

Relative temperature fluctuation (spectral representation of horizon
quantum fluctuations): δT/T = T_H/M = Δλ_min/(2πM²).

At Planck scale, these fluctuations bound the metric fluctuations at ∂Rec_D.
-/

/-- Relative temperature fluctuation: δT/T = T_H/M. -/
noncomputable def horizonTempFluctuation (M : ℝ) (hM : 0 < M) : ℝ :=
  hawkingTempSchwarzschild M hM / M

/-- Fluctuation is positive for M > 0. -/
theorem horizonTempFluctuation_pos (M : ℝ) (hM : 0 < M) :
    0 < horizonTempFluctuation M hM :=
  div_pos (hawkingTempSchwarzschild_pos M hM) hM

/-- Spectral representation: δT/T = Δλ_min/(2πM²). -/
theorem horizonTempFluctuation_spectral (M : ℝ) (hM : 0 < M) :
    horizonTempFluctuation M hM = spectralGap 8 / (2 * Real.pi * M^2) := by
  unfold horizonTempFluctuation hawkingTempSchwarzschild
  have hM_ne : M ≠ 0 := ne_of_gt hM
  have hpi_ne : Real.pi ≠ 0 := ne_of_gt (Real.pi_pos)
  have hgap_ne : spectralGap 8 ≠ 0 := ne_of_gt (spectralGap8_pos)
  field_simp [hM_ne, hpi_ne, hgap_ne]

/-- Fluctuation decreases with mass: larger black holes fluctuate less. -/
theorem horizonTempFluctuation_decreasing (M₁ M₂ : ℝ) (hM₁ : 0 < M₁)
    (hM₂ : 0 < M₂) (hlt : M₁ < M₂) :
    horizonTempFluctuation M₁ hM₁ > horizonTempFluctuation M₂ hM₂ := by
  have hgap_pos : 0 < spectralGap 8 := spectralGap8_pos
  have hpi_pos : (0 : ℝ) < Real.pi := Real.pi_pos
  have h2pi_pos : (0 : ℝ) < 2 * Real.pi := mul_pos (by norm_num : (0 : ℝ) < 2) hpi_pos
  have hC_pos : (0 : ℝ) < spectralGap 8 / (2 * Real.pi) := div_pos hgap_pos h2pi_pos
  have hC' : (spectralGap 8 / (2 * Real.pi)) / M₁^2 >
             (spectralGap 8 / (2 * Real.pi)) / M₂^2 :=
    div_constant_sq_decreasing (spectralGap 8 / (2 * Real.pi)) M₁ M₂ hC_pos hM₁ hM₂ hlt
  have hgt : spectralGap 8 / (2 * Real.pi * M₁^2) >
             spectralGap 8 / (2 * Real.pi * M₂^2) := by
    simpa [div_div] using hC'
  have h1 := horizonTempFluctuation_spectral M₁ hM₁
  have h2 := horizonTempFluctuation_spectral M₂ hM₂
  linarith

end UFPFormalization
