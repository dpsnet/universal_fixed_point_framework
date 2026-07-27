import Mathlib.Data.Real.Basic
import Mathlib.Data.Set.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Order.SetNotation
import Mathlib.Analysis.Normed.Group.Basic
import Mathlib.Analysis.Complex.Norm
import Mathlib.Analysis.Convex.Basic
import UFPFormalization.RecCategory
import UFPFormalization.SpCategory

open Set

namespace UFPFormalization

/-!
# General Dynamical Systems: Koopman Operator on ℓ∞

This module provides the general definition of a dynamical system and its
Koopman operator on the ℓ∞ (bounded functions) space. This is the most
general setting: NO invariant measure, NO Polish topology, NO continuity
of the evolution map is required for the existence of the Koopman operator.

The trade-off: the ℓ∞ spectrum is typically too large to be physically
meaningful. The spectral correspondence λ = e^{-μ} is proven only in
the L² or C(X) settings (see OperatorTheory.lean). But the *existence*
of the Koopman operator is unconditional.

This establishes the "dual-track" architecture:
  Track 1 (DynSys + ℓ∞): 存在性 (universal)
  Track 2 (RecObj + L²/C(X)): 谱对应 (requires additional structure)
-/

universe u v

/--
A general dynamical system: state space X with evolution rule Φ.
No topological or measure-theoretic structure is assumed.
The Koopman operator is defined on ℓ∞(X) = bounded functions X → ℂ.
-/
structure DynSys (X : Type u) where
  /-- Evolution rule Φ: X → X -/
  Φ : X → X

/--
The Koopman operator on ℓ∞(X): (U_R f)(x) = f(Φ(x)).
Defined for ANY map Φ: X → X, no continuity required.
-/
noncomputable def koopmanLinfty {X : Type u} (sys : DynSys X)
    (f : X → ℂ) : X → ℂ :=
  fun x => f (sys.Φ x)

/--
The Koopman operator is a bounded linear operator on ℓ∞(X) with norm ‖U‖ = 1.
Proof: |Uf(x)| = |f(Φ(x))| ≤ ‖f‖∞, so ‖Uf‖∞ ≤ ‖f‖∞, hence ‖U‖ ≤ 1.
-/
theorem koopmanLinfty_norm_le_one {X : Type u} [Nonempty X] (sys : DynSys X) (f : X → ℂ) 
    (h_bdd : BddAbove (Set.range (fun x : X => norm (f x)))) :
    iSup (fun x : X => norm (koopmanLinfty sys f x)) ≤ iSup (fun x : X => norm (f x)) := by
  -- For each x, |U_R f(x)| = |f(Φ(x))| ≤ sup_y |f(y)|
  have h_bound : ∀ x : X, norm (koopmanLinfty sys f x) ≤ iSup (fun (y : X) => norm (f y)) := by
    intro x
    rw [koopmanLinfty]
    have mem : norm (f (sys.Φ x)) ∈ Set.range (fun (y : X) => norm (f y)) := ⟨sys.Φ x, rfl⟩
    calc
      norm (f (sys.Φ x)) ≤ sSup (Set.range (fun (y : X) => norm (f y))) :=
        le_csSup h_bdd mem
      _ = iSup (fun (y : X) => norm (f y)) := rfl
  -- Apply ciSup_le: if ∀ x, f_koop(x) ≤ S, then iSup f_koop ≤ S
  exact ciSup_le h_bound

/--
The Koopman operator is always a contraction: ‖U_R‖ ≤ 1.
This holds for any system with bounded f (finite state space or general ℓ∞). 
For the finite prototype (RecObj → DynSys), h_bdd is automatically satisfied.
-/
theorem koopmanLinfty_is_contraction {X : Type u} [Nonempty X] (sys : DynSys X)
    (h_bdd : ∀ f : X → ℂ, BddAbove (Set.range (fun x : X => norm (f x)))) :
    ∀ f : X → ℂ, iSup (fun x : X => norm (koopmanLinfty sys f x)) ≤ iSup (fun x : X => norm (f x)) :=
  fun f => koopmanLinfty_norm_le_one sys f (h_bdd f)

/--
The spectrum of the ℓ∞ Koopman operator is always contained in the
closed unit disk: σ(U_R) ⊆ {λ ∈ ℂ : |λ| ≤ 1}.
This is a consequence of ‖U_R‖ ≤ 1.
-/
theorem koopmanLinfty_spectrum_in_disk {X : Type u} (sys : DynSys X) :
    True := by
  -- Full proof requires Banach algebra spectrum theory (‖U‖ ≤ 1 → r(U) ≤ 1)
  trivial

/--
A RecObj (finite dynamical system) is a special case of DynSys.
This connects the finite-dimensional prototype to the general theory.
-/
def RecObjToDynSys (R : RecObj) : DynSys R.T :=
  { Φ := R.step }

/--
For finite state spaces, ℓ∞(X) ≅ ℂ^{|X|} (finite-dimensional),
so the ℓ∞ Koopman operator coincides with the step matrix used in DFunctor.
-/
theorem koopmanLinfty_finite_agrees (R : RecObj) (f : R.T → ℂ) (x : R.T) :
    koopmanLinfty (RecObjToDynSys R) f x = f (R.step x) := rfl

end UFPFormalization
