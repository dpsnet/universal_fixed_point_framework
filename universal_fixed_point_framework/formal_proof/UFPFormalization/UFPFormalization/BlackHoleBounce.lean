import UFPFormalization.BlackHoleEvolution
import UFPFormalization.SpectralGap
import Mathlib.Data.Real.Basic

open Real

namespace UFPFormalization

/-!
# Black Hole Quantum Bounce (P1-3 §6 extension)

Formalization of the spectral-cutoff termination of black hole evaporation
and the quantum bounce seed mechanism (Paper IX §4.2-4.3).

Key physics:
  - Effective Friedmann equation: H² = (8π/3)ρ(1 − ρ/ρ_c)
  - Bounce point: H = 0 at ρ = ρ_c (spectral cutoff)
  - ρ_c = (8π/3)(M_Pl²/c₁) with c₁ = 1/(4Δλ_min²), M_Pl = 1
  - a_min ~ l_P/Δλ_min² > 0 (positive bounce scale from spectral gap)
  - Planck remnant at t_pl becomes the bounce seed
-/

/-- Bounce critical density ρ_c = (8π/3)·4Δλ_min² (M_Pl=1, c₁=1/(4Δλ_min²)). -/
noncomputable def bounceCriticalDensity : ℝ :=
  (8 * Real.pi / 3) * (4 * spectralGap 8^2)

/-- Effective Friedmann Hubble squared: H² = (8π/3)ρ(1 − ρ/ρ_c). -/
noncomputable def hubbleSquared (ρ : ℝ) : ℝ :=
  (8 * Real.pi / 3) * ρ * (1 - ρ / bounceCriticalDensity)

/-- ρ_c > 0 (the bounce density is positive). -/
theorem bounceCriticalDensity_pos : 0 < bounceCriticalDensity := by
  unfold bounceCriticalDensity
  have hgap_pos : 0 < spectralGap 8 := spectralGap8_pos
  have hsq : (0 : ℝ) < spectralGap 8^2 := sq_pos_of_pos hgap_pos
  have h4sq : (0 : ℝ) < 4 * spectralGap 8^2 := mul_pos (by norm_num : (0 : ℝ) < 4) hsq
  have hpi_pos : 0 < Real.pi := Real.pi_pos
  have h8pi : (0 : ℝ) < 8 * Real.pi := mul_pos (by norm_num : (0 : ℝ) < 8) hpi_pos
  have h8pi3 : (0 : ℝ) < 8 * Real.pi / 3 := div_pos h8pi (by norm_num : (0 : ℝ) < 3)
  exact mul_pos h8pi3 h4sq

/-- At the critical density, H² = 0 (the bounce point). -/
theorem hubbleSquared_zero_at_critical : hubbleSquared bounceCriticalDensity = 0 := by
  unfold hubbleSquared
  have hρc_ne : bounceCriticalDensity ≠ 0 := ne_of_gt bounceCriticalDensity_pos
  field_simp [hρc_ne]
  ring

/-- Below the critical density, H² > 0 (expansion phase before the bounce). -/
theorem hubbleSquared_pos_below_critical (ρ : ℝ)
    (hρ_pos : 0 < ρ) (hρ_lt : ρ < bounceCriticalDensity) :
    0 < hubbleSquared ρ := by
  unfold hubbleSquared
  have hpi_pos : 0 < Real.pi := Real.pi_pos
  have h8pi : (0 : ℝ) < 8 * Real.pi := mul_pos (by norm_num : (0 : ℝ) < 8) hpi_pos
  have h8pi3 : (0 : ℝ) < 8 * Real.pi / 3 := div_pos h8pi (by norm_num : (0 : ℝ) < 3)
  have hρc_pos : 0 < bounceCriticalDensity := bounceCriticalDensity_pos
  have hratio : ρ / bounceCriticalDensity < 1 := by
    have h1 : (ρ / bounceCriticalDensity) * bounceCriticalDensity = ρ := by
      field_simp [ne_of_gt hρc_pos]
    have hlt' : (ρ / bounceCriticalDensity) * bounceCriticalDensity <
        1 * bounceCriticalDensity := by
      rw [h1]
      simpa using hρ_lt
    exact lt_of_mul_lt_mul_right hlt' (le_of_lt hρc_pos)
  have hfactor : (0 : ℝ) < 1 - ρ / bounceCriticalDensity := by linarith
  exact mul_pos (mul_pos h8pi3 hρ_pos) hfactor

/-- Bounce minimal scale (Paper IX corollary 4.1): a_min ∝ 1/Δλ_min². -/
noncomputable def bounceMinScale : ℝ :=
  1 / spectralGap 8^2

/-- The bounce minimal scale is positive: a_min > 0 (no zero-scale singularity). -/
theorem bounceMinScale_pos : 0 < bounceMinScale := by
  unfold bounceMinScale
  have hgap_pos : 0 < spectralGap 8 := spectralGap8_pos
  have hsq : (0 : ℝ) < spectralGap 8^2 := sq_pos_of_pos hgap_pos
  exact one_div_pos.mpr hsq

/-- The Planck remnant at t_pl becomes the bounce seed:
    evaporation terminates at M = M_Pl (spectral cutoff), which seeds the bounce. -/
theorem bhPlanckRemnant_is_bounce_seed (ev : BHEvol) :
    bhMass ev (bhPlanckTime ev)
      (show 0 ≤ bhMassCubed ev (bhPlanckTime ev) from by
        rw [bhMassCubed_at_planck ev]
        have hMpl_pos : 0 < planckMass := by norm_num [planckMass]
        exact le_of_lt (pow_pos hMpl_pos 3)) = planckMass :=
  bhMass_at_planck ev

/-- Evaporation is cut off before reaching the classical singularity:
    the Planck time occurs strictly before the semiclassical evaporation time. -/
theorem bhPlanckCutoff_before_classical_end (ev : BHEvol) :
    bhPlanckTime ev < bhEvaporationTime ev :=
  bhPlanckTime_lt_evaporationTime ev

end UFPFormalization
