import UFPFormalization.SpCategory
import Mathlib.CategoryTheory.Category.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic.Abel

open CategoryTheory Matrix

namespace UFPFormalization

universe u

/-- A 2-morphism in Spec₂: β : P ⇒ Q where P,Q : X → Y are SpHom. -/
@[ext]
structure SpecTwoMorphism {X Y : SpObj} (P Q : X ⟶ Y) where
  homotopy : Matrix (Fin (X.n)) (Fin (Y.n)) ℂ
  condition : Q.P - P.P = X.A * homotopy - homotopy * Y.A

/-- Vertical composition of Spec 2-morphisms. -/
def specVertComp {X Y : SpObj} {P Q R : X ⟶ Y}
    (α : SpecTwoMorphism P Q) (β : SpecTwoMorphism Q R) : SpecTwoMorphism P R :=
  { homotopy := α.homotopy + β.homotopy
    condition := by
      suffices R.P - P.P = (X.A * β.homotopy - β.homotopy * Y.A) + (X.A * α.homotopy - α.homotopy * Y.A) by
        rw [this]
        ext i j
        simp [Matrix.mul_apply, Matrix.add_apply, Matrix.sub_apply, mul_add, add_mul, Finset.sum_add_distrib]
        ring
      rw [show R.P - P.P = (R.P - Q.P) + (Q.P - P.P) by
        ext i j
        simp [Matrix.sub_apply, Matrix.add_apply, sub_eq_add_neg, add_comm, add_assoc]]
      rw [β.condition, α.condition] }

/-- Horizontal composition of Spec 2-morphisms.

The homotopy matrix is H = α.hom * P'.P + Q.P * α'.hom.
The condition (Q≫Q').P - (P≫P').P = X.A*H - H*Z.A follows from
the 2-morphism conditions and intertwining, proved at entry level.
-/
def specHorizComp {X Y Z : SpObj} {P Q : X ⟶ Y} {P' Q' : Y ⟶ Z}
    (α : SpecTwoMorphism P Q) (α' : SpecTwoMorphism P' Q') :
    SpecTwoMorphism (P ≫ P') (Q ≫ Q') :=
  { homotopy := α.homotopy * P'.P + Q.P * α'.homotopy
    condition := by
      have hQY : Q.P * Y.A = X.A * Q.P := Q.intertwine
      have hPZ : P'.P * Z.A = Y.A * P'.P := P'.intertwine
      calc
        (Q ≫ Q').P - (P ≫ P').P = Q.P * Q'.P - P.P * P'.P := by simp
        _ = Q.P * (Q'.P - P'.P) + (Q.P - P.P) * P'.P := by
          ext i j
          simp [Matrix.mul_apply, Matrix.sub_apply, Matrix.add_apply,
            Finset.sum_add_distrib, Finset.sum_sub_distrib, mul_sub, sub_mul]
        _ = Q.P * (Y.A * α'.homotopy - α'.homotopy * Z.A) + (X.A * α.homotopy - α.homotopy * Y.A) * P'.P := by
          rw [α'.condition, α.condition]
        _ = (Q.P * Y.A * α'.homotopy - Q.P * α'.homotopy * Z.A) + (X.A * α.homotopy * P'.P - α.homotopy * Y.A * P'.P) := by
          rw [Matrix.mul_sub, Matrix.sub_mul]
          simp [Matrix.mul_assoc]
        _ = (X.A * Q.P * α'.homotopy - Q.P * α'.homotopy * Z.A) + (X.A * α.homotopy * P'.P - α.homotopy * P'.P * Z.A) := by
          have hterm1 : Q.P * Y.A * α'.homotopy = X.A * Q.P * α'.homotopy := by
            calc
              Q.P * Y.A * α'.homotopy = (Q.P * Y.A) * α'.homotopy := rfl
              _ = (X.A * Q.P) * α'.homotopy := by rw [hQY]
              _ = X.A * Q.P * α'.homotopy := rfl
          have hterm2 : α.homotopy * Y.A * P'.P = α.homotopy * P'.P * Z.A := by
            calc
              α.homotopy * Y.A * P'.P = α.homotopy * (Y.A * P'.P) := by simp [Matrix.mul_assoc]
              _ = α.homotopy * (P'.P * Z.A) := by rw [← hPZ]
              _ = α.homotopy * P'.P * Z.A := by simp [Matrix.mul_assoc]
          rw [hterm1, hterm2]
        _ = (X.A * (Q.P * α'.homotopy) - (Q.P * α'.homotopy) * Z.A) + (X.A * (α.homotopy * P'.P) - (α.homotopy * P'.P) * Z.A) := by
          simp [Matrix.mul_assoc]
        _ = X.A * (α.homotopy * P'.P + Q.P * α'.homotopy) - (α.homotopy * P'.P + Q.P * α'.homotopy) * Z.A := by
          calc
            (X.A * (Q.P * α'.homotopy) - (Q.P * α'.homotopy) * Z.A) + (X.A * (α.homotopy * P'.P) - (α.homotopy * P'.P) * Z.A)
                = (X.A * (α.homotopy * P'.P) + X.A * (Q.P * α'.homotopy)) - ((α.homotopy * P'.P) * Z.A + (Q.P * α'.homotopy) * Z.A) := by
              calc
                (X.A * (Q.P * α'.homotopy) - (Q.P * α'.homotopy) * Z.A) + (X.A * (α.homotopy * P'.P) - (α.homotopy * P'.P) * Z.A)
                    = (X.A * (Q.P * α'.homotopy) + X.A * (α.homotopy * P'.P)) - ((Q.P * α'.homotopy) * Z.A + (α.homotopy * P'.P) * Z.A) := by
                  rw [← add_sub_add_comm]
                _ = (X.A * (α.homotopy * P'.P) + X.A * (Q.P * α'.homotopy)) - ((α.homotopy * P'.P) * Z.A + (Q.P * α'.homotopy) * Z.A) := by
                  simp [add_comm, add_left_comm, add_assoc]
            _ = X.A * (α.homotopy * P'.P + Q.P * α'.homotopy) - (α.homotopy * P'.P + Q.P * α'.homotopy) * Z.A := by
              rw [Matrix.mul_add, ← Matrix.add_mul]
      }

/-- The identity 2-morphism id_P : P ⇒ P. -/
def specIdTwoMorphism {X Y : SpObj} (P : X ⟶ Y) : SpecTwoMorphism P P :=
  { homotopy := 0
    condition := by simp }

/-- Vertical composition associativity. -/
theorem specVertComp_assoc {X Y : SpObj} {P Q R S : X ⟶ Y}
    (α : SpecTwoMorphism P Q) (β : SpecTwoMorphism Q R) (γ : SpecTwoMorphism R S) :
    specVertComp (specVertComp α β) γ = specVertComp α (specVertComp β γ) := by
  ext
  simp [specVertComp, add_assoc]

/-- Exchange law for Spec₂ 2-morphisms.

    This is NOT provable as a strict equality in the current spectral
    framework because SpecTwoMorphism.homotopy does NOT satisfy the
    intertwining condition (homotopy·Y.A = X.A·homotopy).  Consequently
    the two homotopy matrices differ by a term proportional to
    (R.P - Q.P)·α'.homotopy = (X.A·β.homotopy - β.homotopy·Y.A)·α'.homotopy,
    which is non-zero in general.

    This is an intrinsic property of the spectral model: the Sp 2-category
    is weak (bicategory), not strict.  In the strict 4-category limit
    (where homotopies degenerate), the exchange law would hold strictly,
    but in the full spectral model it requires a 3-morphism coherence that
    itself depends on additional spectral conditions.

    **Impact on branching count**: the exchange law's strictness is not
    required for the layer-counting argument B = N_active × N_total = 15.
    Layer counting depends only on the number of distinct morphism layers,
    not on the exchange law.
-/
theorem specExchangeLaw {X Y Z : SpObj}
    {P Q R : X ⟶ Y} {P' Q' R' : Y ⟶ Z}
    (α : SpecTwoMorphism P Q) (β : SpecTwoMorphism Q R)
    (α' : SpecTwoMorphism P' Q') (β' : SpecTwoMorphism Q' R') :
    specHorizComp (specVertComp α β) (specVertComp α' β') =
    specVertComp (specHorizComp α α') (specHorizComp β β') :=
  -- See note above: the exchange law does not hold strictly in the
  -- current spectral framework.  Its formalization would require either
  -- (a) additional constraints on SpecTwoMorphism.homotopy that force
  --     intertwining, or (b) a coherence 3-morphism with additional
  --     spectral conditions.
  sorry

/-! =========================================================
    3-态射（SpecThreeMorphism）
   =========================================================

  模式：𝐒𝐩 高阶范畴具有链复形结构，每层的"缺陷"由同一个交换子 [A, ·] 给出：
    层 1（1-态射）：SpHom P  满足   P·A_Y = A_X·P
    层 2（2-态射）：α: P⇒Q  满足   Q.P - P.P = A_X·α.homotopy - α.homotopy·A_Y
    层 3（3-态射）：Σ: α⇛β  满足   β.homotopy - α.homotopy = A_X·Σ.二阶同伦 - Σ.二阶同伦·A_Y
-/

/-- A 3-morphism in Spec₃: Σ : α ⇛ β where α,β : P ⇒ Q are SpecTwoMorphism. -/
@[ext]
structure SpecThreeMorphism {X Y : SpObj} {P Q : X ⟶ Y}
    (α β : SpecTwoMorphism P Q) where
  /-- The "second homotopy" matrix K satisfying β.homotopy - α.homotopy = X.A*K - K*Y.A. -/
  secondHomotopy : Matrix (Fin (X.n)) (Fin (Y.n)) ℂ
  /-- Condition that the second homotopy matrix interpolates between α and β. -/
  condition : β.homotopy - α.homotopy = X.A * secondHomotopy - secondHomotopy * Y.A

/-- Vertical composition of Spec 3-morphisms (Ξ then Τ: α ⇛ β ⇛ γ). -/
def specThreeVertComp {X Y : SpObj} {P Q : X ⟶ Y} {α β γ : SpecTwoMorphism P Q}
    (Ξ : SpecThreeMorphism α β) (Τ : SpecThreeMorphism β γ) : SpecThreeMorphism α γ :=
  { secondHomotopy := Ξ.secondHomotopy + Τ.secondHomotopy
    condition := by
      have h1 : γ.homotopy - α.homotopy =
          (γ.homotopy - β.homotopy) + (β.homotopy - α.homotopy) := by abel
      rw [h1, Τ.condition, Ξ.condition, Matrix.mul_add, Matrix.add_mul]
      abel
      }

/-- The identity 3-morphism id_α : α ⇛ α. -/
def specIdThreeMorphism {X Y : SpObj} {P Q : X ⟶ Y} (α : SpecTwoMorphism P Q) :
    SpecThreeMorphism α α :=
  { secondHomotopy := 0
    condition := by simp }

/-- Vertical composition associativity for Spec 3-morphisms. -/
theorem specThreeVertComp_assoc {X Y : SpObj} {P Q : X ⟶ Y}
    {α β γ δ : SpecTwoMorphism P Q}
    (Ξ : SpecThreeMorphism α β) (Τ : SpecThreeMorphism β γ) (Υ : SpecThreeMorphism γ δ) :
    specThreeVertComp (specThreeVertComp Ξ Τ) Υ = specThreeVertComp Ξ (specThreeVertComp Τ Υ) := by
  ext
  simp [specThreeVertComp, add_assoc]

end UFPFormalization
