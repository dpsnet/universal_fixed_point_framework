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

import UFPFormalization.KerrFiber
import UFPFormalization.SpectralDynamics
import UFPFormalization.SpectralGap
import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Analysis.SpecialFunctions.Log.Basic

open Matrix
open Real

namespace UFPFormalization

/-!
# Black Hole Quantum Evolution (P1-3)

Formalization of black hole evaporation dynamics from spectral principles.
Based on Paper VIII, Paper 27, and spectral dynamics notes.
-/

/-!
## §1: Black Hole Mass Evolution

M(t) = (M₀³ - 3αt)^(1/3), with cubed mass Δ(t) = M₀³ - 3αt.
-/

/-- Black hole evaporation parameters. -/
structure BHEvol where
  M₀ : ℝ
  M₀_pos : M₀ > 0
  α : ℝ
  α_pos : α > 0

/-- The cubed mass Δ(t) = M₀³ - 3α·t. -/
noncomputable def bhMassCubed (ev : BHEvol) (t : ℝ) : ℝ :=
  ev.M₀^3 - 3 * ev.α * t

/-- Black hole mass M(t) = Δ(t)^(1/3). -/
noncomputable def bhMass (ev : BHEvol) (t : ℝ) (h : 0 ≤ bhMassCubed ev t) : ℝ :=
  Real.rpow (bhMassCubed ev t) (1 / 3)

/-- bhMass is positive when cubed mass is positive. -/
theorem bhMass_pos (ev : BHEvol) (t : ℝ) (h_pos : 0 < bhMassCubed ev t) :
    0 < bhMass ev t (le_of_lt h_pos) := by
  have h : bhMass ev t (le_of_lt h_pos) = Real.rpow (bhMassCubed ev t) (1 / 3) := rfl
  rw [h]
  exact Real.rpow_pos_of_pos h_pos (1 / 3)

/-- Δ(0) = M₀³. -/
theorem bhMassCubed_initial (ev : BHEvol) :
    bhMassCubed ev 0 = ev.M₀^3 := by
  simp [bhMassCubed]

/-- Δ(t) is strictly decreasing. -/
theorem bhMassCubed_decreasing (ev : BHEvol) (t dt : ℝ) (hdt : 0 < dt) :
    bhMassCubed ev (t + dt) < bhMassCubed ev t := by
  simp [bhMassCubed]
  have hα_pos : 0 < ev.α := ev.α_pos
  linarith [mul_pos hα_pos hdt]

/-- Mass is strictly decreasing. -/
theorem bhMass_decreasing (ev : BHEvol) (t dt : ℝ)
    (hdt : 0 < dt) (h_pos : 0 < bhMassCubed ev t)
    (h_pos2 : 0 < bhMassCubed ev (t + dt)) :
    bhMass ev t (le_of_lt h_pos) > bhMass ev (t + dt) (le_of_lt h_pos2) := by
  have h_dec : bhMassCubed ev (t + dt) < bhMassCubed ev t :=
    bhMassCubed_decreasing ev t dt hdt
  have h13_pos : (0 : ℝ) < (1 / 3 : ℝ) := by norm_num
  have hy_pos : (0 : ℝ) < bhMassCubed ev (t + dt) := h_pos2
  have hx_pos : (0 : ℝ) < bhMassCubed ev t := h_pos
  have hlt : Real.rpow (bhMassCubed ev (t + dt)) (1 / 3) <
              Real.rpow (bhMassCubed ev t) (1 / 3) := by
    exact Real.rpow_lt_rpow (le_of_lt hy_pos) h_dec h13_pos
  simpa [bhMass] using hlt

/-- Evaporation time: t_stop = M₀³/(3α). -/
noncomputable def bhEvaporationTime (ev : BHEvol) : ℝ :=
  ev.M₀^3 / (3 * ev.α)

/-- At t_stop, Δ = 0. -/
theorem bhEvaporationTime_condition (ev : BHEvol) :
    bhMassCubed ev (bhEvaporationTime ev) = 0 := by
  have hα_ne : ev.α ≠ 0 := ne_of_gt ev.α_pos
  have h3_ne : (3 : ℝ) ≠ 0 := ne_of_gt (by norm_num : (0 : ℝ) < 3)
  have h : ev.M₀^3 - 3 * ev.α * (ev.M₀^3 / (3 * ev.α)) = 0 := by
    field_simp
    ring
    <;> linarith
  simpa [bhMassCubed, bhEvaporationTime] using h

/-- Mass = 0 at evaporation time. -/
theorem bhMass_at_evaporation_time (ev : BHEvol) :
    bhMass ev (bhEvaporationTime ev)
      (show 0 ≤ bhMassCubed ev (bhEvaporationTime ev) from
        le_of_eq (bhEvaporationTime_condition ev).symm) = 0 := by
  have hΔ0 : bhMassCubed ev (bhEvaporationTime ev) = 0 := bhEvaporationTime_condition ev
  have h13_pos : (0 : ℝ) < (1 / 3 : ℝ) := by norm_num
  have hz : Real.rpow (0 : ℝ) (1 / 3) = 0 := by
    exact Real.zero_rpow (ne_of_gt h13_pos)
  simpa [bhMass, hΔ0, hz]

/-!
## §1b: Spectral Cutoff Termination (Planck scale)

Physical endpoint: evaporation terminates at M ~ M_Pl (spectral cutoff,
Paper IX §4.3), NOT at M = 0. The semiclassical mass reaches M_Pl at
t_pl < t_evap; below the Planck scale the spectral cutoff takes over.
-/

/-- Planck mass in normalized units (G=ħ=c=1): M_Pl = 1. -/
def planckMass : ℝ := 1

/-- rpow cube-root identity: (x³)^(1/3) = x for x > 0. -/
lemma rpow_cube_root (x : ℝ) (hx : 0 < x) :
    Real.rpow (x^3) (1 / 3) = x := by
  have hx3_pos : 0 < x^3 := pow_pos hx 3
  calc
    Real.rpow (x^3) (1 / 3) = Real.exp (Real.log (x^3) * (1 / 3)) :=
      Real.rpow_def_of_pos hx3_pos (1 / 3)
    _ = Real.exp ((3 * Real.log x) * (1 / 3)) := by
      congr 1
      rw [Real.log_pow x 3]
      norm_num
    _ = Real.exp (Real.log x) := by
      have hsimp : (3 * Real.log x) * (1 / 3) = Real.log x := by ring
      rw [hsimp]
    _ = x := Real.exp_log hx

/-- Planck time: when the semiclassical mass reaches M_Pl, the spectral
    cutoff terminates the evaporation. -/
noncomputable def bhPlanckTime (ev : BHEvol) : ℝ :=
  (ev.M₀^3 - planckMass^3) / (3 * ev.α)

/-- At Planck time, the cubed mass equals M_Pl³. -/
theorem bhMassCubed_at_planck (ev : BHEvol) :
    bhMassCubed ev (bhPlanckTime ev) = planckMass^3 := by
  unfold bhPlanckTime bhMassCubed planckMass
  have hα_ne : ev.α ≠ 0 := ne_of_gt ev.α_pos
  have h3_ne : (3 : ℝ) ≠ 0 := by norm_num
  field_simp [hα_ne, h3_ne]
  ring

/-- At Planck time, the mass reaches M_Pl (spectral cutoff). -/
theorem bhMass_at_planck (ev : BHEvol) :
    bhMass ev (bhPlanckTime ev)
      (show 0 ≤ bhMassCubed ev (bhPlanckTime ev) from by
        rw [bhMassCubed_at_planck ev]
        have hMpl_pos : 0 < planckMass := by norm_num [planckMass]
        exact le_of_lt (pow_pos hMpl_pos 3)) = planckMass := by
  have hΔ : bhMassCubed ev (bhPlanckTime ev) = planckMass^3 := bhMassCubed_at_planck ev
  have hMpl_pos : 0 < planckMass := by norm_num [planckMass]
  have hcube : Real.rpow (planckMass^3) (1 / 3) = planckMass := rpow_cube_root planckMass hMpl_pos
  unfold bhMass
  rw [hΔ]
  exact hcube

/-- Planck time occurs before the semiclassical evaporation time
    (evaporation is cut off before reaching M = 0). -/
theorem bhPlanckTime_lt_evaporationTime (ev : BHEvol) :
    bhPlanckTime ev < bhEvaporationTime ev := by
  unfold bhPlanckTime bhEvaporationTime planckMass
  have hM0_pos : (0 : ℝ) < ev.M₀ := ev.M₀_pos
  have hM0cubed : (0 : ℝ) < ev.M₀^3 := pow_pos hM0_pos 3
  have h3_pos : (0 : ℝ) < 3 := by norm_num
  have hα_pos : 0 < ev.α := ev.α_pos
  have hden_pos : (0 : ℝ) < 3 * ev.α := mul_pos h3_pos hα_pos
  have hlt_num : ev.M₀^3 - 1^3 < ev.M₀^3 := by linarith
  have hlt : (ev.M₀^3 - 1^3) / (3 * ev.α) < ev.M₀^3 / (3 * ev.α) := by
    have h1 : (ev.M₀^3 - 1^3) / (3 * ev.α) * (3 * ev.α) = ev.M₀^3 - 1^3 := by field_simp
    have h2 : ev.M₀^3 / (3 * ev.α) * (3 * ev.α) = ev.M₀^3 := by field_simp
    have hlt' : (ev.M₀^3 - 1^3) / (3 * ev.α) * (3 * ev.α) <
        ev.M₀^3 / (3 * ev.α) * (3 * ev.α) := by
      rw [h1, h2]
      exact hlt_num
    exact lt_of_mul_lt_mul_right hlt' (le_of_lt hden_pos)
  exact hlt

/-- Before the Planck time, the mass is always above the Planck scale:
    evaporation does not cross below M_Pl (no naked singularity). -/
theorem bhMass_above_planck_before (ev : BHEvol) (t : ℝ)
    (h_lt : t < bhPlanckTime ev) (h_pos : 0 < bhMassCubed ev t) :
    planckMass < bhMass ev t (le_of_lt h_pos) := by
  have hΔ_lt : bhMassCubed ev (bhPlanckTime ev) < bhMassCubed ev t := by
    unfold bhMassCubed
    have h3α : (0 : ℝ) < 3 * ev.α := mul_pos (by norm_num : (0 : ℝ) < 3) ev.α_pos
    have hsub : t - bhPlanckTime ev < 0 := by linarith
    have hneg : (3 * ev.α) * (t - bhPlanckTime ev) < 0 :=
      mul_neg_of_pos_of_neg h3α hsub
    linarith
  have hΔpl_pos : 0 < bhMassCubed ev (bhPlanckTime ev) := by
    rw [bhMassCubed_at_planck ev]
    have hMpl_pos : 0 < planckMass := by norm_num [planckMass]
    exact pow_pos hMpl_pos 3
  have hM_gt : Real.rpow (bhMassCubed ev (bhPlanckTime ev)) (1 / 3) <
               Real.rpow (bhMassCubed ev t) (1 / 3) := by
    exact Real.rpow_lt_rpow (le_of_lt hΔpl_pos) hΔ_lt (by norm_num : (0 : ℝ) < (1 / 3 : ℝ))
  have hpl : Real.rpow (bhMassCubed ev (bhPlanckTime ev)) (1 / 3) = planckMass := by
    have hMpl_pos : 0 < planckMass := by norm_num [planckMass]
    rw [bhMassCubed_at_planck ev]
    exact rpow_cube_root planckMass hMpl_pos
  have hM : bhMass ev t (le_of_lt h_pos) = Real.rpow (bhMassCubed ev t) (1 / 3) := rfl
  linarith

/-!
## §2: Hawking Radiation Spectrum

T_H(M) = Δλ_min / (2π·M)
N(ω) = 1/(e^(2πMω/Δλ_min) - 1)
-/

/-- Hawking temperature (Schwarzschild, a=0). -/
noncomputable def hawkingTempSchwarzschild (M : ℝ) (_hM : M > 0) : ℝ :=
  spectralGap 8 / (2 * Real.pi * M)

/-- T_H > 0 for M > 0. -/
theorem hawkingTempSchwarzschild_pos (M : ℝ) (hM : M > 0) :
    0 < hawkingTempSchwarzschild M hM := by
  have hgap_pos : 0 < spectralGap 8 := spectralGap8_pos
  have hpi_pos : 0 < Real.pi := Real.pi_pos
  have h2Mpi_pos : (0 : ℝ) < 2 * Real.pi * M := by
    exact mul_pos (mul_pos (by norm_num : (0 : ℝ) < 2) hpi_pos) hM
  unfold hawkingTempSchwarzschild
  exact div_pos hgap_pos h2Mpi_pos

/-- T_H is strictly decreasing in M. -/
theorem hawkingTempSchwarzschild_decreasing (M₁ M₂ : ℝ) (hM₁ : M₁ > 0)
    (hM₂ : M₂ > 0) (hlt : M₁ < M₂) :
    hawkingTempSchwarzschild M₁ hM₁ > hawkingTempSchwarzschild M₂ hM₂ := by
  have hgap_pos : 0 < spectralGap 8 := spectralGap8_pos
  have hpi_pos : 0 < Real.pi := Real.pi_pos
  have hC_pos : (0 : ℝ) < spectralGap 8 / (2 * Real.pi) := by
    exact div_pos hgap_pos (mul_pos (by norm_num : (0 : ℝ) < 2) hpi_pos)
  have hgt : spectralGap 8 / (2 * Real.pi * M₁) >
             spectralGap 8 / (2 * Real.pi * M₂) := by
    have hgt' : spectralGap 8 / (2 * Real.pi) / M₁ >
                spectralGap 8 / (2 * Real.pi) / M₂ := by
      have h : spectralGap 8 / (2 * Real.pi) / M₁ > spectralGap 8 / (2 * Real.pi) / M₂ := by
        gcongr
      exact h
    simpa [div_div] using hgt'
  unfold hawkingTempSchwarzschild
  simpa [div_div] using hgt

/-- Hawking temperature as a function of time. -/
noncomputable def hawkingTempTime (ev : BHEvol) (t : ℝ)
    (h_pos : 0 < bhMassCubed ev t) : ℝ :=
  hawkingTempSchwarzschild (bhMass ev t (le_of_lt h_pos)) (bhMass_pos ev t h_pos)

/-- T_H increases as black hole evaporates. -/
theorem hawkingTempTime_increasing (ev : BHEvol) (t dt : ℝ)
    (hdt : 0 < dt) (h_pos : 0 < bhMassCubed ev t)
    (h_pos2 : 0 < bhMassCubed ev (t + dt)) :
    hawkingTempTime ev t h_pos < hawkingTempTime ev (t + dt) h_pos2 := by
  set M_t := bhMass ev t (le_of_lt h_pos) with hMt
  set M_t2 := bhMass ev (t + dt) (le_of_lt h_pos2) with hMt2
  have hMt_pos : 0 < M_t := bhMass_pos ev t h_pos
  have hMt2_pos : 0 < M_t2 := bhMass_pos ev (t + dt) h_pos2
  have h_mass_strict : M_t2 < M_t := bhMass_decreasing ev t dt hdt h_pos h_pos2
  have h_temp_gt : hawkingTempSchwarzschild M_t2 hMt2_pos > hawkingTempSchwarzschild M_t hMt_pos :=
    hawkingTempSchwarzschild_decreasing M_t2 M_t hMt2_pos hMt_pos h_mass_strict
  have h_temp_lt : hawkingTempSchwarzschild M_t hMt_pos < hawkingTempSchwarzschild M_t2 hMt2_pos := by linarith
  simpa [hawkingTempTime, hMt, hMt2] using h_temp_lt

/-- Planck occupation N(ω) = 1/(e^(βMω) - 1). -/
noncomputable def planckOccupation (M : ℝ) (ω : ℝ) (_hM : M > 0) : ℝ :=
  let βM : ℝ := 2 * Real.pi * M / spectralGap 8
  1 / (Real.exp (βM * ω) - 1)

/-- N(ω) > 0 for ω > 0. -/
theorem planckOccupation_pos (M ω : ℝ) (hM : M > 0) (hω : 0 < ω) :
    0 < planckOccupation M ω hM := by
  have hgap_pos : 0 < spectralGap 8 := spectralGap8_pos
  have hpi_pos : 0 < Real.pi := Real.pi_pos
  have h2Mpi : (0 : ℝ) < 2 * Real.pi * M := by
    exact mul_pos (mul_pos (by norm_num : (0 : ℝ) < 2) hpi_pos) hM
  have hβM_pos : (0 : ℝ) < 2 * Real.pi * M / spectralGap 8 :=
    div_pos h2Mpi hgap_pos
  have hβMω_pos : (0 : ℝ) < 2 * Real.pi * M / spectralGap 8 * ω :=
    mul_pos hβM_pos hω
  have hexp_gt_one : (1 : ℝ) < Real.exp (2 * Real.pi * M / spectralGap 8 * ω) := by
    have hx_pos : (0 : ℝ) < 2 * Real.pi * M / spectralGap 8 * ω := hβMω_pos
    have h : Real.exp 0 < Real.exp (2 * Real.pi * M / spectralGap 8 * ω) := by
      simpa [Real.exp_lt_exp] using hx_pos
    have hexp0 : Real.exp (0 : ℝ) = 1 := Real.exp_zero
    linarith
  have hden_pos : (0 : ℝ) < Real.exp (2 * Real.pi * M / spectralGap 8 * ω) - 1 := by linarith
  unfold planckOccupation
  exact div_pos one_pos hden_pos

/-!
## §3: Bekenstein-Hawking Entropy

S_BH = 4π·M² for Schwarzschild.
-/

/-- Bekenstein-Hawking entropy. -/
noncomputable def bekensteinHawkingEntropySchwarzschild (M : ℝ) : ℝ :=
  4 * Real.pi * M^2

/-- S_BH > 0 for M > 0. -/
theorem bhEntropySchwarzschild_pos (M : ℝ) (hM : M > 0) :
    0 < bekensteinHawkingEntropySchwarzschild M := by
  have hpi_pos : 0 < Real.pi := Real.pi_pos
  have h4pi_pos : (0 : ℝ) < 4 * Real.pi := mul_pos (by norm_num : (0 : ℝ) < 4) hpi_pos
  have hM2_pos : (0 : ℝ) < M^2 := sq_pos_of_pos hM
  unfold bekensteinHawkingEntropySchwarzschild
  exact mul_pos h4pi_pos hM2_pos

/-- S_BH strictly increases with M. -/
theorem bhEntropySchwarzschild_increasing (M₁ M₂ : ℝ) (hM₁ : M₁ > 0)
    (hM₂ : M₂ > 0) (hlt : M₁ < M₂) :
    bekensteinHawkingEntropySchwarzschild M₁ < bekensteinHawkingEntropySchwarzschild M₂ := by
  have hpi_pos : 0 < Real.pi := Real.pi_pos
  have h4pi_pos : (0 : ℝ) < 4 * Real.pi := mul_pos (by norm_num : (0 : ℝ) < 4) hpi_pos
  have hsq_lt : (M₁ : ℝ)^2 < M₂^2 := by
    have h1sq : (0 : ℝ) < M₁^2 := sq_pos_of_pos hM₁
    have h2sq : (0 : ℝ) < M₂^2 := sq_pos_of_pos hM₂
    nlinarith
  unfold bekensteinHawkingEntropySchwarzschild
  have hgt : 4 * Real.pi * M₁^2 < 4 * Real.pi * M₂^2 := by
    change (4 * Real.pi : ℝ) * M₁^2 < (4 * Real.pi) * M₂^2
    exact mul_lt_mul_of_pos_left hsq_lt h4pi_pos
  exact hgt

/-- Entropy as function of time. -/
noncomputable def bhEntropyTime (ev : BHEvol) (t : ℝ)
    (h_pos : 0 < bhMassCubed ev t) : ℝ :=
  bekensteinHawkingEntropySchwarzschild (bhMass ev t (le_of_lt h_pos))

/-- Entropy decreases during evaporation. -/
theorem bhEntropyTime_decreasing (ev : BHEvol) (t dt : ℝ)
    (hdt : 0 < dt) (h_pos : 0 < bhMassCubed ev t)
    (h_pos2 : 0 < bhMassCubed ev (t + dt)) :
    bhEntropyTime ev (t + dt) h_pos2 < bhEntropyTime ev t h_pos := by
  set M_t := bhMass ev t (le_of_lt h_pos) with hMt
  set M_t2 := bhMass ev (t + dt) (le_of_lt h_pos2) with hMt2
  have hMt_pos : 0 < M_t := bhMass_pos ev t h_pos
  have hMt2_pos : 0 < M_t2 := bhMass_pos ev (t + dt) h_pos2
  have h_mass_strict : M_t2 < M_t := bhMass_decreasing ev t dt hdt h_pos h_pos2
  have h_entropy_lt : bekensteinHawkingEntropySchwarzschild M_t2 < bekensteinHawkingEntropySchwarzschild M_t :=
    bhEntropySchwarzschild_increasing M_t2 M_t hMt2_pos hMt_pos h_mass_strict
  simpa [bhEntropyTime, hMt, hMt2] using h_entropy_lt

/-!
## §4: Information Preservation

Spectral flow preserves eigenvalues: σ(A_t) = σ(A₀).
-/

/-- Spectral information preservation (σ(A₀) ⊆ σ(A_t)). -/
theorem bhInformationPreserved_forward {n : ℕ}
    (A₀ A_F : Matrix (Fin n) (Fin n) ℂ) (t : ℝ) (a : ℂ)
    (ha : a ∈ Matrix.eigenvalues A₀) :
    a ∈ Matrix.eigenvalues (spectralFlow A₀ A_F t) := by
  exact spectral_invariance A₀ A_F t a ha

end UFPFormalization