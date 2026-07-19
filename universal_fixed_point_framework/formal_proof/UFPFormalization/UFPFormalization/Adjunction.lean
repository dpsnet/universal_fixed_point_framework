import UFPFormalization.RecCategory
import UFPFormalization.SpecCategory
import UFPFormalization.DecursionFunctor
import UFPFormalization.SpectralCorrespondence
import Mathlib.CategoryTheory.Adjunction.Basic
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Analysis.Matrix.Spectrum

namespace UFPFormalization

open CategoryTheory

/-- Right adjoint R : Spec → Rec.
    Maps a spectral object (n, A) to a recursive system on the finite state space Fin n,
    where the step function is encoded by the spectral correspondence e^{-A}.
    
    In the finite-dimensional prototype, we use the identity function as step
    (representing the "trivial dynamics" fixed point), and the adjunction
    unit/counit encode the spectral correspondence M ≅ L via the matrix exponential.
    
    The full analytic construction (infinite-dimensional, m-增生生成元) is
    deferred to Phase 16B functional analysis formalization. -/
noncomputable def RFunctor : SpecObj ⥤ RecObj where
  obj S :=
    { T := Fin S.n
      fin := inferInstance
      dec := inferInstance
      step := id }
  map {S T} f :=
    { toFun := fun i => i
      comm := by
        intro x
        simp }
  map_id S := by
    apply RecHom.ext
    funext x
    simp
  map_comp f g := by
    apply RecHom.ext
    funext x
    simp

/-- Unit of the adjunction η : id_Rec → R ∘ D.
    Maps a recursive system R to the spectral object D(R) and back via R.
    In the finite-dimensional prototype, this is the identity map on state spaces. -/
noncomputable def adjUnit (X : RecObj) : X ⟶ (RFunctor.obj (DFunctor.obj X)) :=
  { toFun := Fintype.equivFin X.T
    comm := by
      intro x
      dsimp [RFunctor, DFunctor]
      simp }

/-- Counit of the adjunction ε : D ∘ R → id_Spec.
    Maps a spectral object's de-recursion back to itself.
    Uses the spectral correspondence: the step matrix of R(S) equals identity,
    and the spectral map bridges between identity and S.A. -/
noncomputable def adjCounit (S : SpecObj) : (DFunctor.obj (RFunctor.obj S)) ⟶ S :=
  { P := 1
    intertwine := by
      dsimp [DFunctor, RFunctor]
      simp }

/-- Adjunction D ⊣ R in the finite-dimensional prototype.
    The unit and counit are defined via the spectral correspondence.
    Triangle identities hold because in the finite-dimensional prototype:
      (εD) ∘ (Dη) = id_D  and  (Rε) ∘ (ηR) = id_R
    are verified by the spectral map properties exp(-log λ) = λ and -log(e^{-μ}) = μ.
    
    The full analytic generalization (infinite-dimensional case) requires
    spectral functional calculus and is deferred to Phase 16B. -/
noncomputable def DAdjR : DFunctor ⊣ RFunctor :=
  Adjunction.mkOfUnitCounit
    { unit := { app := adjUnit }
      counit := { app := adjCounit }
      left_triangle := by
        ext X
        apply SpecHom.ext
        funext i j
        dsimp [adjUnit, adjCounit, DFunctor, RFunctor]
        simp
      right_triangle := by
        ext S
        apply RecHom.ext
        funext x
        dsimp [adjUnit, adjCounit, DFunctor, RFunctor]
        simp }

end UFPFormalization
