import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.CategoryTheory.Category.Basic
import Mathlib.Tactic.Ext

namespace UFPFormalization

open CategoryTheory

/-- Spectral category object: a finite-dimensional complex vector space
    equipped with a linear operator. -/
structure SpObj where
  n : ℕ
  A : Matrix (Fin n) (Fin n) ℂ

/-- Morphism in the spectral category: a matrix intertwining the operators. -/
@[ext]
structure SpHom (X Y : SpObj) where
  P : Matrix (Fin X.n) (Fin Y.n) ℂ
  intertwine : P * Y.A = X.A * P

instance spCategory : Category.{0, 0} SpObj where
  Hom X Y := SpHom X Y
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
lemma SpHom.id_P (X : SpObj) : ((𝟙 X) : SpHom X X).P = 1 := rfl

@[simp]
lemma SpHom.comp_P {X Y Z : SpObj} (f : X ⟶ Y) (g : Y ⟶ Z) :
    ((f ≫ g) : SpHom X Z).P = f.P * g.P := rfl

end UFPFormalization
