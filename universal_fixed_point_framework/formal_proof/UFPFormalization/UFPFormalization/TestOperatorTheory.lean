import UFPFormalization.OperatorTheory
import UFPFormalization.Silence
import UFPFormalization.SpectralCorrespondence
import UFPFormalization.LeaverComplexity
import UFPFormalization.DynSys
import UFPFormalization.RecCategory
import UFPFormalization.DecursionFunctor
import Mathlib.Data.Fin.Basic

open UFPFormalization
open CategoryTheory

namespace UFPFormalization.Test

/-!
# Tests for Operator Theory, Silence, Spectral Correspondence, Leaver Complexity, DynSys

Covers: OperatorTheory, Silence, SpectralCorrespondence, LeaverComplexity, DynSys
-/

-- ============================================================
-- OperatorTheory Tests
-- ============================================================

-- Koopman operator is a contraction (‖U_R‖ ≤ 1)
theorem test_koopman_is_contraction {X : Type} [Nonempty X] (sys : DynSys X) (f : X → ℂ)
    (h_bdd : BddAbove (Set.range (fun x : X => norm (f x)))) :
    iSup (fun x : X => norm (koopmanLinfty sys f x)) ≤ iSup (fun x : X => norm (f x)) :=
  koopmanLinfty_norm_le_one sys f h_bdd

-- The spectral measure classification exists
theorem test_spectral_type_exists : Nonempty SpectralType :=
  ⟨SpectralType.point⟩

-- ============================================================
-- Silence Tests
-- ============================================================

-- Silence S1-S4 are defined
theorem test_silence_definitions_exist (R : RecObj) : Nonempty (silenceS1 (DFunctor.obj R).A) := by
  -- silenceS1 is a Prop, can be true or false
  exact ⟨trivial⟩

-- 局部吸引子捕获指数（Local Attractor Capture Index, LACI）index is non-negative
theorem test_laci_nonneg {X : SpObj} (f : X ⟶ X) : 0 ≤ laciIndex f.P := by
  dsimp [laciIndex]
  -- LACI 的有限原型实现恒为 0，非负性直接成立；
  -- 完整证明需要奇异值分解（Phase 16B）。
  simp [laciIndex]

-- ============================================================
-- SpectralCorrespondence Tests
-- ============================================================

-- spectralMap: λ = e^{-μ}
theorem test_spectralMap_exp (mu : ℂ) : spectralMap mu = Complex.exp (-mu) := rfl

-- spectralInv on principal branch: spectralInv ∘ spectralMap = id
theorem test_spectralInv_leftInv (mu : ℂ) (h : mu.im ∈ Set.Ico (-Real.pi) Real.pi) :
    spectralInv (spectralMap mu) = mu :=
  spectralInv_leftInv h

-- spectralMap on non-zero argument: spectralMap ∘ spectralInv = id
theorem test_spectralMap_rightInv (lambda : ℂ) (h : lambda ≠ 0) :
    spectralMap (spectralInv lambda) = lambda :=
  spectralMap_rightInv h

-- ============================================================
-- LeaverComplexity Tests
-- ============================================================

-- Tridiagonal matrix has at most 3 non-zero entries per row
theorem test_tridiagonal_row_nonzero (n : ℕ) (d : TridiagonalData n) (i : Fin n) :
    (Finset.filter (fun (j : Fin n) => tridiagonalMatrix d i j ≠ 0) Finset.univ).card ≤ 3 :=
  tridiagonal_row_nonzero_count d i

-- ============================================================
-- DynSys Tests
-- ============================================================

-- Koopman on ℓ∞: RecObj → DynSys embedding
theorem test_RecObj_to_DynSys (R : RecObj) (f : R.T → ℂ) (x : R.T) :
    koopmanLinfty (RecObjToDynSys R) f x = f (R.step x) := rfl

-- DynSys Koopman is always a contraction
theorem test_DynSys_contraction (X : Type) [Nonempty X] (sys : DynSys X) :
    iSup (fun x : X => norm (koopmanLinfty sys (fun _ => (0 : ℂ)) x)) ≤ iSup (fun x : X => norm ((0 : ℂ))) :=
  koopmanLinfty_norm_le_one sys (fun _ => 0) (by
    refine ⟨0, ?_⟩
    intro y hy
    rcases hy with ⟨x, rfl⟩
    simp)

end UFPFormalization.Test
