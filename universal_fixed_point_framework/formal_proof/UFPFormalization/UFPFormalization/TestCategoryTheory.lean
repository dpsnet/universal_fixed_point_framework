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
-- 本文件中 UFPF 相关引用数量：9
-- 更名将在计划确认后统一执行，当前代码不做修改。
-- ============================================================

import UFPFormalization.RecCategory
import UFPFormalization.SpCategory
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

Covers: RecCategory, SpCategory, DecursionFunctor, Adjunction, Braided, IsolationConstraints
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
    (@CategoryStruct.comp RecObj _ (testRecObj n) (testRecObj n) (testRecObj n) f g).toFun x =
      g.toFun (f.toFun x) := rfl

-- Category axioms: identity
theorem test_recCategory_id_comp (n : ℕ) (f : RecHom (testRecObj n) (testRecObj n)) :
    (@CategoryStruct.comp RecObj _ (testRecObj n) (testRecObj n) (testRecObj n) (𝟙 (testRecObj n)) f) = f := by
  apply RecHom.ext
  simp

theorem test_recCategory_comp_id (n : ℕ) (f : RecHom (testRecObj n) (testRecObj n)) :
    (@CategoryStruct.comp RecObj _ (testRecObj n) (testRecObj n) (testRecObj n) f (𝟙 (testRecObj n))) = f := by
  apply RecHom.ext
  simp

-- ============================================================
-- SpCategory Tests
-- ============================================================

def testSpObj (n : ℕ) : SpObj :=
  { n := n, A := 1 }

-- SpHom identity
example (n : ℕ) : ((𝟙 (testSpObj n) : SpHom (testSpObj n) (testSpObj n)).P = 1) := rfl

-- SpHom intertwine property for identity
theorem test_SpHom_id_intertwine (n : ℕ) :
    (𝟙 (testSpObj n) : SpHom (testSpObj n) (testSpObj n)).P * (testSpObj n).A =
    (testSpObj n).A * (𝟙 (testSpObj n) : SpHom (testSpObj n) (testSpObj n)).P := by
  simp

-- ============================================================
-- DecursionFunctor Tests
-- ============================================================

-- D functor object: DFunctor.obj returns a SpObj
theorem test_DFunctor_obj_type (n : ℕ) : (DFunctor.obj (testRecObj n) : SpObj).n = n := by
  simp [DFunctor, testRecObj]

-- D functor preserves identity
theorem test_DFunctor_map_id (n : ℕ) : DFunctor.map (𝟙 (testRecObj n)) = 𝟙 (DFunctor.obj (testRecObj n)) := by
  apply DFunctor.map_id

-- ============================================================
-- Adjunction Tests
-- ============================================================

-- D ⊣ R adjunction unit exists
theorem test_adjUnit_exists (R : RecObj) : Nonempty (R ⟶ RFunctor (DFunctor.obj R)) :=
  ⟨adjUnit R⟩

-- D ⊣ R adjunction counit exists
theorem test_adjCounit_exists (S : SpObj) : Nonempty (DFunctor.obj (RFunctor S) ⟶ S) :=
  ⟨adjCounit S⟩

-- ============================================================
-- Braided Tests
-- ============================================================

-- recTensorProduct is symmetric for self-adjoint case
theorem test_braiding_symmetric (n : ℕ) :
    (recBraiding (testRecObj n) (testRecObj n)).hom ≫ (recBraiding (testRecObj n) (testRecObj n)).hom =
    𝟙 (recTensorProduct (testRecObj n) (testRecObj n)) := by
  apply braiding_symmetric

-- recBraiding is natural
theorem test_braiding_natural (R₁ R₂ : RecObj) :
    (recBraiding R₁ R₂).hom.toFun = fun (x, y) => (y, x) := rfl

-- ============================================================
-- IsolationConstraint Tests
-- ============================================================

-- IC is reflexive (in finite prototype)
theorem test_IC_reflexive (R : RecObj) : isolationConstraint R R := by
  simp [isolationConstraint, spectralScaleCompatible, morphismExtendable, topologicallyCompatible]

end UFPFormalization.Test
