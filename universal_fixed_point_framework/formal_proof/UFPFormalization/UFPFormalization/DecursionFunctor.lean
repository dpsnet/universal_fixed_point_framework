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

/-- Transfer matrices compose contravariantly with function composition. -/
theorem transferMatrix_comp {α β γ : Type} [Fintype α] [DecidableEq α]
    [Fintype β] [DecidableEq β] [Fintype γ] [DecidableEq γ]
    (f : α → β) (g : β → γ) :
    transferMatrix (g ∘ f) = transferMatrix f * transferMatrix g := by
  funext i j
  by_cases h : g (f i) = j
  · -- left side equals 1; show the matrix product equals 1
    rw [Matrix.mul_apply]
    rw [Finset.sum_eq_single (f i)]
    · simp [transferMatrix, h]
    · intro k _ hk
      have h_ne : f i ≠ k := by
        intro h'
        apply hk
        exact h'.symm
      simp [transferMatrix, h_ne]
    · intro h'
      exfalso
      apply h'
      exact Finset.mem_univ (f i)
  · -- left side equals 0; show the matrix product equals 0
    rw [Matrix.mul_apply]
    simp [transferMatrix, h]
    rw [eq_comm]
    apply Finset.sum_eq_zero
    intro k _
    by_cases hk : f i = k
    · rw [hk]
      have h' : g k ≠ j := by
        intro h''
        apply h
        rw [hk]
        exact h''
      simp [h']
    · simp [hk]

/-- Object part of the spectral de-recursion functor. -/
noncomputable abbrev DFunctor_obj (X : RecObj) : SpecObj :=
  ⟨Fintype.card X.T, stepMatrix (Fintype.equivFin X.T ∘ X.step ∘ (Fintype.equivFin X.T).symm)⟩

/-- Morphism part of the spectral de-recursion functor. -/
noncomputable abbrev DFunctor_map {X Y : RecObj} (f : RecHom X Y) :
    DFunctor_obj X ⟶ DFunctor_obj Y :=
  ⟨transferMatrix (Fintype.equivFin Y.T ∘ f.toFun ∘ (Fintype.equivFin X.T).symm), by
    dsimp [DFunctor_obj, stepMatrix]
    rw [← transferMatrix_comp, ← transferMatrix_comp]
    apply congr_arg
    funext x
    simp only [Function.comp_apply]
    rw [Equiv.symm_apply_apply (Fintype.equivFin Y.T), Equiv.symm_apply_apply (Fintype.equivFin X.T)]
    rw [← RecHom.comm f ((Fintype.equivFin X.T).symm x)]⟩

/-- Spectral de-recursion functor: encode a finite recursive system as a spectral operator. -/
noncomputable def DFunctor : RecObj ⥤ SpecObj where
  obj := DFunctor_obj
  map := DFunctor_map
  map_id X := by
    apply SpecHom.ext
    funext i j
    dsimp [DFunctor_map, DFunctor_obj]
    simp [transferMatrix]
    rw [Matrix.one_apply]
  map_comp {X Y Z} f g := by
    apply SpecHom.ext
    funext i j
    dsimp [DFunctor_map, DFunctor_obj]
    rw [← transferMatrix_comp]
    suffices
      (Fintype.equivFin Z.T ∘ (g.toFun ∘ f.toFun) ∘ (Fintype.equivFin X.T).symm) =
      ((Fintype.equivFin Z.T ∘ g.toFun ∘ (Fintype.equivFin Y.T).symm) ∘
       (Fintype.equivFin Y.T ∘ f.toFun ∘ (Fintype.equivFin X.T).symm)) by
      rw [this]
    funext x
    simp [Equiv.symm_apply_apply]

end UFPFormalization
