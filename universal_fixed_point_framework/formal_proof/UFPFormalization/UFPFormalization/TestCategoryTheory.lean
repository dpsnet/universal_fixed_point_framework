import UFPFormalization.RecCategory
import UFPFormalization.SpecCategory
import UFPFormalization.DecursionFunctor
import UFPFormalization.Adjunction
import UFPFormalization.Braided
import UFPFormalization.IsolationConstraints
import Mathlib.Data.Fin.Basic

open UFPFormalization
open CategoryTheory

namespace UFPFormalization.Test

/-!
# Tests for Category-Theoretic Foundations (Rec, Spec, D, Adjunction, Braided, IC)

Covers: RecCategory, SpecCategory, DecursionFunctor, Adjunction, Braided, IsolationConstraints
-/

-- ============================================================
-- RecCategory Tests
-- ============================================================

-- Sample recursive objects
def testRecObj (n : ℕ) : RecObj :=
  { T := Fin n, fin := inferInstance, dec := inferInstance, step := id }

-- RecObj identity morphism
example (n : ℕ) : (𝟙 (testRecObj n) : RecHom (testRecObj n) (testRecObj n)).toFun = id := by
  simp

-- RecHom composition
example (n : ℕ) (f g : RecHom (testRecObj n) (testRecObj n)) (x : Fin n) :
    ((f ≫ g) : RecHom (testRecObj n) (testRecObj n)).toFun x = g.toFun (f.toFun x) := rfl

-- Category axioms: identity
theorem test_recCategory_id_comp (n : ℕ) (f : RecHom (testRecObj n) (testRecObj n)) :
    (𝟙 (testRecObj n) ≫ f) = f := by
  apply RecHom.ext
  intro x; simp

theorem test_recCategory_comp_id (n : ℕ) (f : RecHom (testRecObj n) (testRecObj n)) :
    (f ≫ 𝟙 (testRecObj n)) = f := by
  apply RecHom.ext
  intro x; simp

-- ============================================================
-- SpecCategory Tests
-- ============================================================

def testSpecObj (n : ℕ) : SpecObj :=
  { n := n, A := 1 }

-- SpecHom identity
example (n : ℕ) : ((𝟙 (testSpecObj n) : SpecHom (testSpecObj n) (testSpecObj n)).P = 1) := rfl

-- SpecHom intertwine property for identity
theorem test_SpecHom_id_intertwine (n : ℕ) :
    (𝟙 (testSpecObj n) : SpecHom (testSpecObj n) (testSpecObj n)).P * (testSpecObj n).A =
    (testSpecObj n).A * (𝟙 (testSpecObj n) : SpecHom (testSpecObj n) (testSpecObj n)).P := by
  simp

-- ============================================================
-- DecursionFunctor Tests
-- ============================================================

-- D functor object: DFunctor.obj returns a SpecObj
theorem test_DFunctor_obj_type (n : ℕ) : (DFunctor.obj (testRecObj n) : SpecObj).n = n := by
  simp [DFunctor, testRecObj]

-- D functor preserves identity
theorem test_DFunctor_map_id (n : ℕ) : DFunctor.map (𝟙 (testRecObj n)) = 𝟙 (DFunctor.obj (testRecObj n)) := by
  apply DFunctor.map_id

-- ============================================================
-- Adjunction Tests
-- ============================================================

-- D ⊣ R adjunction unit exists
theorem test_adjUnit_exists (R : RecObj) : Nonempty (R ⟶ RFunctor.obj (DFunctor.obj R)) :=
  ⟨adjUnit R⟩

-- D ⊣ R adjunction counit exists
theorem test_adjCounit_exists (S : SpecObj) : Nonempty (DFunctor.obj (RFunctor.obj S) ⟶ S) :=
  ⟨adjCounit S⟩

-- ============================================================
-- Braided Tests
-- ============================================================

-- recTensorProduct is symmetric for self-adjoint case
theorem test_braiding_symmetric (n : ℕ) :
    recBraiding (testRecObj n) (testRecObj n) ≫ recBraiding (testRecObj n) (testRecObj n) =
    𝟙 (recTensorProduct (testRecObj n) (testRecObj n)) := by
  apply braiding_symmetric

-- recBraiding is natural
theorem test_braiding_natural (R₁ R₂ : RecObj) :
    (recBraiding R₁ R₂).toFun = fun (x, y) => (y, x) := rfl

-- ============================================================
-- IsolationConstraint Tests
-- ============================================================

-- IC is reflexive (in finite prototype)
theorem test_IC_reflexive (R : RecObj) : isolationConstraint R R := by
  simp [isolationConstraint, spectralScaleCompatible, morphismExtendable, topologicallyCompatible]

end UFPFormalization.Test
