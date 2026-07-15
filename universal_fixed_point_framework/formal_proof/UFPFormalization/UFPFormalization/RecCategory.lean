import Mathlib.CategoryTheory.Category.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic.Ext

namespace UFPFormalization

open CategoryTheory

universe u

/-- Recursive-system category object: a finite state space equipped with an evolution rule. -/
structure RecObj where
  T : Type u
  fin : Fintype T
  dec : DecidableEq T
  step : T → T

instance recObjFintype (X : RecObj) : Fintype X.T := X.fin
instance recObjDecidableEq (X : RecObj) : DecidableEq X.T := X.dec

/-- Morphism in the recursive-system category: a map commuting with the evolution rule. -/
@[ext]
structure RecHom (X Y : RecObj) where
  toFun : X.T → Y.T
  comm : ∀ x, toFun (X.step x) = Y.step (toFun x)

instance recCategory : Category.{u, u+1} RecObj where
  Hom X Y := RecHom X Y
  id X := ⟨id, by simp⟩
  comp f g := ⟨g.toFun ∘ f.toFun, by intro x; simp [f.comm, g.comm]⟩
  id_comp := by intros; rfl
  comp_id := by intros; rfl
  assoc := by intros; rfl

@[simp]
lemma RecHom.id_toFun (X : RecObj) : ((𝟙 X) : RecHom X X).toFun = id := rfl

@[simp]
lemma RecHom.comp_toFun {X Y Z : RecObj} (f : X ⟶ Y) (g : Y ⟶ Z) :
    ((f ≫ g) : RecHom X Z).toFun = g.toFun ∘ f.toFun := rfl

end UFPFormalization
