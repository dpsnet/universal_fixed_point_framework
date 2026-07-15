import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.CategoryTheory.Category.Basic
import Mathlib.Tactic.Ext

namespace UFPFormalization

open CategoryTheory

/-- Spectral category object: a finite-dimensional complex vector space
    equipped with a linear operator. -/
structure SpecObj where
  n : ℕ
  A : Matrix (Fin n) (Fin n) ℂ

/-- Morphism in the spectral category: a matrix intertwining the operators. -/
@[ext]
structure SpecHom (X Y : SpecObj) where
  P : Matrix (Fin X.n) (Fin Y.n) ℂ
  intertwine : P * Y.A = X.A * P

instance specCategory : Category.{0, 0} SpecObj where
  Hom X Y := SpecHom X Y
  id X := ⟨1, by simp⟩
  comp f g := ⟨f.P * g.P, by
    rw [Matrix.mul_assoc, g.intertwine]
    rw [← Matrix.mul_assoc, f.intertwine]
    rw [Matrix.mul_assoc]⟩
  id_comp := by
    intro X Y f
    ext
    simp
  comp_id := by
    intro X Y f
    ext
    simp
  assoc := by
    intro W X Y Z f g h
    ext i j
    exact congr_arg (fun M => M i j) (Matrix.mul_assoc f.P g.P h.P)

@[simp]
lemma SpecHom.id_P (X : SpecObj) : ((𝟙 X) : SpecHom X X).P = 1 := rfl

@[simp]
lemma SpecHom.comp_P {X Y Z : SpecObj} (f : X ⟶ Y) (g : Y ⟶ Z) :
    ((f ≫ g) : SpecHom X Z).P = f.P * g.P := rfl

end UFPFormalization
