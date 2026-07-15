import UFPFormalization.RecCategory
import UFPFormalization.SpecCategory
import Mathlib.CategoryTheory.Functor.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Data.Fintype.Basic

namespace UFPFormalization

open CategoryTheory Matrix

/-- General transfer matrix induced by a function f : α → β. -/
def transferMatrix {α β : Type} [Fintype α] [DecidableEq α] [Fintype β] [DecidableEq β]
    (f : α → β) : Matrix α β ℂ :=
  fun i j => if f i = j then 1 else 0

/-- Square transfer matrix of a finite-state recursive step. -/
def stepMatrix {α : Type} [Fintype α] [DecidableEq α] (step : α → α) : Matrix α α ℂ :=
  transferMatrix step

/-- Object part of the spectral de-recursion functor. -/
noncomputable abbrev DFunctor_obj (X : RecObj) : SpecObj :=
  ⟨Fintype.card X.T, stepMatrix (Fintype.equivFin X.T ∘ X.step ∘ (Fintype.equivFin X.T).symm)⟩

/-- Morphism part of the spectral de-recursion functor. -/
noncomputable abbrev DFunctor_map {X Y : RecObj} (f : RecHom X Y) :
    DFunctor_obj X ⟶ DFunctor_obj Y :=
  let eX := Fintype.equivFin X.T
  let eY := Fintype.equivFin Y.T
  let φ := transferMatrix (eY ∘ f.toFun ∘ eX.symm)
  ⟨φ, sorry⟩

/-- Spectral de-recursion functor: encode a finite recursive system as a spectral operator.
    Functor laws and the morphism intertwining condition are admitted in the Level-A prototype. -/
noncomputable def DFunctor : RecObj ⥤ SpecObj where
  obj := DFunctor_obj
  map := DFunctor_map
  map_id X := sorry
  map_comp f g := sorry

end UFPFormalization
