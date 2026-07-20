import UFPFormalization.RecCategory
import UFPFormalization.SpecCategory
import UFPFormalization.DecursionFunctor
import UFPFormalization.RecInfinity
import UFPFormalization.SpecInfinity
import UFPFormalization.AInfinityAlgebra
import Mathlib.CategoryTheory.Functor.Basic
import Mathlib.Data.Matrix.Basic

open CategoryTheory Matrix

namespace UFPFormalization

universe u

/-- D_∞ on objects: same as DFunctor. -/
noncomputable def DInfinity_obj (R : RecObj) : SpecObj :=
  DFunctor_obj R

/-- D_∞ on 1-morphisms: same as DFunctor_map. -/
noncomputable def DInfinity_one {X Y : RecObj} (f : X ⟶ Y) : DInfinity_obj X ⟶ DInfinity_obj Y :=
  DFunctor_map f

/-- D_∞ on ∞-morphisms. -/
noncomputable def DInfinity_inf {X Y : RecObj} (f : RecInfMorphism X Y) :
    SpecInfMorphism (DInfinity_obj X) (DInfinity_obj Y) :=
  { P := (DInfinity_one f).P
    generator := 0
    intertwine := (DInfinity_one f).intertwine }

/-- D_∞ preserves vertical composition (follows from functoriality of D). -/
theorem DInfinity_preserves_vertComp {X Y Z : RecObj}
    (α : RecInfMorphism X Y) (β : RecInfMorphism Y Z) :
    DInfinity_inf (recInfVertComp α β) =
    specInfVertComp (DInfinity_inf α) (DInfinity_inf β) := by
  apply SpecInfMorphism.ext
  · -- P equality
    ext i j
    unfold DInfinity_inf DInfinity_one DInfinity_obj recInfVertComp specInfVertComp
    have hP : (DFunctor_map (α ≫ β)).P = (DFunctor_map α).P * (DFunctor_map β).P := by
      have h := congrArg SpecHom.P (DFunctor.map_comp α β)
      calc
        (DFunctor_map (α ≫ β)).P = ((DFunctor_map α) ≫ (DFunctor_map β)).P := h
        _ = (DFunctor_map α).P * (DFunctor_map β).P := rfl
    simpa using congrArg (fun M : Matrix (Fin (DFunctor_obj X).n) (Fin (DFunctor_obj Z).n) ℂ => M i j) hP
  · simp [DInfinity_inf, DInfinity_one, recInfVertComp, specInfVertComp]

/-- D_∞ preserves identity ∞-morphisms (follows from functoriality of D). -/
theorem DInfinity_preserves_id (X : RecObj) :
    DInfinity_inf (recInfId X) = specInfId (DInfinity_obj X) := by
  apply SpecInfMorphism.ext
  · -- P equality
    unfold DInfinity_inf DInfinity_one DInfinity_obj recInfId specInfId
    ext i j
    have hP_mat : SpecHom.P (DFunctor_map (𝟙 X)) = 1 := by
      calc
        SpecHom.P (DFunctor_map (𝟙 X)) = SpecHom.P (𝟙 (DFunctor_obj X)) :=
          congrArg SpecHom.P (DFunctor.map_id X)
        _ = 1 := by
          simpa using (SpecHom.id_P (DFunctor_obj X))
    simpa using congrArg (fun M : Matrix (Fin (DFunctor_obj X).n) (Fin (DFunctor_obj X).n) ℂ => M i j) hP_mat
  · simp [DInfinity_inf, DInfinity_one, recInfId, specInfId]

end UFPFormalization
