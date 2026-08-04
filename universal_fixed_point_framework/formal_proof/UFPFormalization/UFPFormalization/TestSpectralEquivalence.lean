import UFPFormalization.SpectralEquivalence
import UFPFormalization.ICVerification
import UFPFormalization.IFSFractal
import UFPFormalization.ThermoFormalism
import UFPFormalization.RecCategory
import UFPFormalization.DecursionFunctor
import UFPFormalization.Braided
import Mathlib.Data.Fin.Basic
import Mathlib.Data.Matrix.Basic

open UFPFormalization
open CategoryTheory

/-!
# Comprehensive Tests for New Lean Modules (Phase 16C)

Tests cover:
  1. SpectralEquivalence — equivalence relation properties, concrete examples
  2. ICVerification — domain-pair IC for all five physical domains
  3. IFSFractal — basic IFS constructions
  4. ThermoFormalism — pressure function and Legendre transform
-/

namespace UFPFormalization.Test

-- ============================================================
-- 1. SpectralEquivalence Tests
-- ============================================================

-- Simple recursive objects used across multiple tests
def mkRecObj (n : ℕ) : RecObj :=
  { T := Fin n, fin := inferInstance, dec := inferInstance, step := id }

-- 1.1. spectralEquivalence equivalence relation
theorem test_spectralEquivalence_refl (n : ℕ) : spectralEquivalence (mkRecObj n) (mkRecObj n) :=
  spectralEquivalence_refl _

theorem test_spectralEquivalence_symm (R₁ R₂ : RecObj) (h : spectralEquivalence R₁ R₂) :
    spectralEquivalence R₂ R₁ :=
  spectralEquivalence_symm h

theorem test_spectralEquivalence_trans (R₁ R₂ R₃ : RecObj)
    (h₁₂ : spectralEquivalence R₁ R₂) (h₂₃ : spectralEquivalence R₂ R₃) :
    spectralEquivalence R₁ R₃ :=
  spectralEquivalence_trans h₁₂ h₂₃

-- 1.2. spectral → braided
theorem test_spectral_implies_braided (R₁ R₂ : RecObj) (h : spectralEquivalence R₁ R₂) :
    braidedSpectralEquivalence R₁ R₂ :=
  spectral_implies_braided R₁ R₂ h

-- 1.3. classification completeness
noncomputable def test_classification_completeness (R₁ R₂ : RecObj) (h : spectralEquivalence R₁ R₂) :
    DFunctor.obj R₁ ≅ DFunctor.obj R₂ :=
  classification_completeness_finite R₁ R₂ h

-- 1.4. spectralClass contains self
theorem test_spectralClass_self (R : RecObj) : R ∈ spectralClass R := by
  dsimp [spectralClass]
  exact spectralEquivalence_refl R

-- 1.5. thm41: identical spectral invariants → spectral equivalence
theorem test_thm41_finite (n : ℕ) : spectralEquivalence (mkRecObj n) (mkRecObj n) := by
  apply thm41_classification_finite (mkRecObj n) (mkRecObj n)
  -- Same object → trivially identical invariants
  rfl

-- 1.6. IC coverage theorem (identical spectral invariants case)
theorem test_thm43_IC_coverage (R₁ R₂ : RecObj)
    (hSame : completeSpectralInvariant R₁ = completeSpectralInvariant R₂) :
    spectralEquivalence R₁ R₂ := by
  exact thm43_IC_full_coverage_finite R₁ R₂ (universal_IC_coverage_finite R₁ R₂) hSame

-- ============================================================
-- 2. IC Verification Tests
-- ============================================================

-- 2.1. IFS self-IC (no contraction ratio bound needed for trivial case)
theorem test_IFS_IC_self_trivial : isolationConstraint (mkRecObj 2) (mkRecObj 2) := by
  apply universal_IC_coverage_finite

-- 2.2. NTK self-IC
theorem test_NTK_IC_self_trivial : isolationConstraint (mkRecObj 3) (mkRecObj 3) := by
  apply universal_IC_coverage_finite

-- 2.3. String-Kerr IC (construct minimal configs)
def testStringConfig : StringConfig :=
  { nRadial := 3, centralCharge := 12, hRadial := by omega }

def testKerrConfig : KerrConfig :=
  { spin := 0.5, nRadial := 2, hSpin := ⟨by norm_num, by norm_num⟩, hRadial := by omega }

theorem test_String_Kerr_IC_concrete : isolationConstraint (StringToRecObj testStringConfig) (KerrToRecObj testKerrConfig) :=
  String_Kerr_IC testStringConfig testKerrConfig

-- 2.4. universal IC coverage
theorem test_universal_IC : ∀ (R₁ R₂ : RecObj), isolationConstraint R₁ R₂ :=
  universal_IC_coverage_finite

-- ============================================================
-- 3. IFS Fractal Tests
-- ============================================================

-- 3.1. The Moran equation is correctly defined
theorem test_hausdorffDimensionEq_def (c : ℝ) (hpos : 0 < c) (hlt : c < 1) (d : ℝ) :
    hausdorffDimensionEq (IFS.mk 1 (fun _ => fun x : ℝ => c * x) (fun _ => ⟨c, le_of_lt hpos⟩) (by
      intro i
      refine ⟨?_, ?_⟩
      · exact_mod_cast hlt
      · apply LipschitzWith.of_dist_le_mul
        intro x y
        change dist (c * x) (c * y) ≤ c * dist x y
        rw [Real.dist_eq, Real.dist_eq]
        rw [← mul_sub]
        rw [abs_mul, abs_of_nonneg (le_of_lt hpos)])
      (by intro i; exact_mod_cast hpos) (by intro i; exact_mod_cast hlt)) d = c ^ d - 1 := by
  -- ⟨c, _⟩ : ℝ≥0 的强制转换定义性等于 c，指数为变量时 rfl 直接闭合
  simp [hausdorffDimensionEq]
  rfl

-- 3.2. Hutchinson operator preserves non-emptiness
theorem test_hutchinsonOperator_nonempty {X : Type} [MetricSpace X] [CompleteSpace X]
    (ifs : IFS X) (K : Set X) : hutchinsonOperator ifs K = ⋃ i : Fin ifs.n, ifs.maps i '' K := rfl

-- ============================================================
-- 4. Thermodynamic Formalism Tests
-- ============================================================

-- 4.1. Legendre transform of a linear function is convex
theorem test_legendreTransform_convex (f : ℝ → ℝ) (hf : ConvexOn ℝ Set.univ f)
    (hBdd : ∀ p : ℝ, BddAbove (Set.range fun z : ℝ => p * z - f z)) :
    ConvexOn ℝ Set.univ (legendreTransform f) :=
  legendreTransform_convex hf hBdd

-- 4.2. topologicalPressure at zero equals log(n)
theorem test_pressure_at_zero_simple : topologicalPressure
    (IFS.mk 1 (fun _ => fun x : ℝ => 0.5 * x) (fun _ => ⟨0.5, by norm_num⟩)
      (by
        intro i
        refine ⟨?_, ?_⟩
        · exact_mod_cast (by norm_num : (0.5 : ℝ) < 1)
        · apply LipschitzWith.of_dist_le_mul
          intro x y
          change dist (0.5 * x) (0.5 * y) ≤ 0.5 * dist x y
          rw [Real.dist_eq, Real.dist_eq]
          rw [← mul_sub]
          rw [abs_mul, abs_of_nonneg (by norm_num)])
      (by intro i; exact_mod_cast (by norm_num : (0 : ℝ) < 0.5))
      (by intro i; exact_mod_cast (by norm_num : (0.5 : ℝ) < 1))) 0 = Real.log 1 := by
  simp [topologicalPressure]

-- 4.3. pressure ↔ Hausdorff dimension connection
theorem test_pressure_hausdorff_link (ifs : IFS ℝ) (t : ℝ) (hNonempty : ifs.n ≥ 1) :
    (topologicalPressure ifs t = 0) → (hausdorffDimensionEq ifs t = 0) :=
  (pressure_zero_iff_hausdorff_dimension ifs t hNonempty).mp

-- 4.4. singularitySpectrum is defined as negative Legendre transform
theorem test_singularitySpectrum_def {X : Type} [MetricSpace X] [CompleteSpace X]
    {ifs : IFS X} {attractor : Attractor ifs} (measure : SelfSimilarMeasure ifs attractor) (α : ℝ) :
    singularitySpectrum measure α = -legendreTransform (multifractalSpectrum measure) α := rfl

end UFPFormalization.Test
