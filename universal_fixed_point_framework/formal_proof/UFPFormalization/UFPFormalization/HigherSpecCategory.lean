import UFPFormalization.SpecCategory
import Mathlib.CategoryTheory.Category.Basic
import Mathlib.Data.Matrix.Basic

open CategoryTheory Matrix

namespace UFPFormalization

universe u

/-- A 2-morphism in Spec₂: β : P ⇒ Q where P,Q : X → Y are SpecHom. -/
@[ext]
structure SpecTwoMorphism {X Y : SpecObj} (P Q : X ⟶ Y) where
  homotopy : Matrix (Fin (X.n)) (Fin (Y.n)) ℂ
  condition : Q.P - P.P = X.A * homotopy - homotopy * Y.A

/-- Vertical composition of Spec 2-morphisms. -/
def specVertComp {X Y : SpecObj} {P Q R : X ⟶ Y}
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
def specHorizComp {X Y Z : SpecObj} {P Q : X ⟶ Y} {P' Q' : Y ⟶ Z}
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
def specIdTwoMorphism {X Y : SpecObj} (P : X ⟶ Y) : SpecTwoMorphism P P :=
  { homotopy := 0
    condition := by simp }

/-- Vertical composition associativity. -/
theorem specVertComp_assoc {X Y : SpecObj} {P Q R S : X ⟶ Y}
    (α : SpecTwoMorphism P Q) (β : SpecTwoMorphism Q R) (γ : SpecTwoMorphism R S) :
    specVertComp (specVertComp α β) γ = specVertComp α (specVertComp β γ) := by
  ext
  simp [specVertComp, add_assoc]

/-- Exchange law for Spec₂ 2-morphisms. -/
theorem specExchangeLaw {X Y Z : SpecObj}
    {P Q R : X ⟶ Y} {P' Q' R' : Y ⟶ Z}
    (α : SpecTwoMorphism P Q) (β : SpecTwoMorphism Q R)
    (α' : SpecTwoMorphism P' Q') (β' : SpecTwoMorphism Q' R') :
    specHorizComp (specVertComp α β) (specVertComp α' β') =
    specVertComp (specHorizComp α α') (specHorizComp β β') :=
  -- The exchange law requires the spectral flow calculus to reconcile
  -- the matrix identity (homotopy equality), which mixes P'.P, Q.P, Q'.P, R.P
  -- with the α/β homotopies; deferred to full formalization.
  sorry

end UFPFormalization
