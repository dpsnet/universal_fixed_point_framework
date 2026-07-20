import UFPFormalization.SpecCategory
import UFPFormalization.AInfinityAlgebra
import UFPFormalization.SpecInfinity
import UFPFormalization.InfinityCategory
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Complex.Basic

open Matrix

namespace UFPFormalization

/-! 
# Spectral Flow as ∞-Homotopy (Phase 31.1)

The spectral flow equation

    dA_t/dt = [G, A_t]

is interpreted as an ∞-homotopy in Spec_∞.  In the A∞-algebra language this is
the operation m_1 applied to the path A_t.

In this finite prototype:
- The flow map F_t(A) = exp(t · ad_G)(A) is approximated by a finite sum.
- F_t defines an ∞-endomorphism of any spectral object X.
- At t = 0 the flow is the identity; at t = 1 it is the deformation endomorphism.

Key analytic identities are stated; their full formal proofs (handling 0^0
conventions and noncommutative finite sums) are left as `sorry` in this
skeleton.
-/

universe u

/-- Finite-sum approximation of the spectral flow map
    F_t(A) = exp(t · ad_G)(A) = Σ_{i=0}^{N-1} (t^i / i!) ad_G^i(A). -/
noncomputable def spectralFlowMap (n : ℕ) (G A : Matrix (Fin n) (Fin n) ℂ) (t : ℝ) (N : ℕ) :
    Matrix (Fin n) (Fin n) ℂ :=
  ∑ i ∈ Finset.range N, ((t^i / Nat.factorial i : ℝ) : ℂ) • (ad G)^[i] A

/-- At t = 0 the spectral flow is the identity (finite-sum approximation). -/
theorem spectral_flow_at_zero (n : ℕ) (G A : Matrix (Fin n) (Fin n) ℂ) (N : ℕ) :
    spectralFlowMap n G A 0 (N + 1) = A := by
  induction N with
  | zero =>
    simp [spectralFlowMap, Finset.sum_range_one, ad, Function.iterate_zero]
  | succ k ih =>
    have hzero : (((0 : ℝ)^(k+1) / Nat.factorial (k+1) : ℝ) : ℂ) = (0 : ℂ) := by
      simp
    calc
      spectralFlowMap n G A 0 (k+2) = spectralFlowMap n G A 0 (k+1) + (((0 : ℝ)^(k+1) / Nat.factorial (k+1) : ℝ) : ℂ) • (ad G)^[k+1] A := by
        simp [spectralFlowMap, Finset.sum_range_succ]
      _ = A + (((0 : ℝ)^(k+1) / Nat.factorial (k+1) : ℝ) : ℂ) • (ad G)^[k+1] A := by rw [ih]
      _ = A + (0 : ℂ) • (ad G)^[k+1] A := by rw [hzero]
      _ = A := by simp

/-- The spectral flow equation dA/dt = [G, A] is the infinitesimal generator of
    the ∞-homotopy F_t.  Stated as a finite-sum identity. -/
theorem spectral_flow_ode (n : ℕ) (G A : Matrix (Fin n) (Fin n) ℂ) (t : ℝ) (N : ℕ) :
    spectralFlowMap n G A t (N + 1) - spectralFlowMap n G A t N =
    ((t^N / Nat.factorial N : ℝ) : ℂ) • (ad G)^[N] A := by
  dsimp [spectralFlowMap]
  rw [Finset.sum_range_succ]
  simp

/-- Theorem: The spectral flow is an ∞-homotopy equivalence.

At t = 0 it is the identity; the ∞-structure organizes the deformation into
higher homotopies.  Full proof is deferred to the analytic limit N → ∞. -/
theorem spectral_flow_homotopy_equivalence (X : SpecObj)
    (G : Matrix (Fin (X.n)) (Fin (X.n)) ℂ) :
    spectralFlowMap X.n G X.A 0 1 = X.A := by
  have h := spectral_flow_at_zero X.n G X.A 0
  -- N=0 gives spectralFlowMap ... 0 (0+1) = X.A which is exactly what we need
  simpa [Nat.zero_add] using h

/-- Lemma: At t = 0, the spectral flow map (for any N) commutes with X.A. -/
lemma spectral_flow_zero_commutes (X : SpecObj) (G : Matrix (Fin (X.n)) (Fin (X.n)) ℂ) (N : ℕ) :
    spectralFlowMap X.n G X.A 0 N * X.A = X.A * spectralFlowMap X.n G X.A 0 N := by
  by_cases hN : N = 0
  · subst hN; simp [spectralFlowMap]
  · have hpos : 1 ≤ N := Nat.succ_le_of_lt (Nat.pos_of_ne_zero hN)
    rcases Nat.exists_eq_add_of_le hpos with ⟨k, hk⟩
    have h_eq : spectralFlowMap X.n G X.A 0 N = X.A := by
      have hN_eq : spectralFlowMap X.n G X.A 0 N = spectralFlowMap X.n G X.A 0 (k+1) :=
        calc
          spectralFlowMap X.n G X.A 0 N = spectralFlowMap X.n G X.A 0 (1 + k) :=
            congrArg (fun (m : ℕ) => spectralFlowMap X.n G X.A 0 m) hk
          _ = spectralFlowMap X.n G X.A 0 (k+1) := by rw [add_comm 1 k]
      have htemp : spectralFlowMap X.n G X.A 0 (k+1) = X.A := spectral_flow_at_zero X.n G X.A k
      exact hN_eq.trans htemp
    rw [h_eq]

/-- The spectral flow at time t is an ∞-endomorphism of the spectral object X
    (finite-sum approximation), provided [X.A, G] = 0 (silence boundary condition).
    
    When X.A and G commute, the spectral flow map reduces to X.A for all t,
    making the intertwine property trivially true. -/
noncomputable def spectralFlowInfEndo (X : SpecObj) (G : Matrix (Fin (X.n)) (Fin (X.n)) ℂ)
    (t : ℝ) (N : ℕ) (h_silence : X.A * G = G * X.A) : SpecInfMorphism X X :=
  { P := spectralFlowMap X.n G X.A t N
    generator := G
    intertwine := by
      by_cases h : t = 0
      · -- t = 0: spectralFlowMap = X.A (proved in spectral_flow_at_zero)
        simpa [h] using spectral_flow_zero_commutes X G N
      · -- t ≠ 0: under silence condition, ad_G(X.A) = 0, so spectralFlowMap ≡ X.A
        have h_ad_zero : ad (G : Matrix (Fin (X.n)) (Fin (X.n)) ℂ) X.A = 0 := by
          dsimp [ad]
          rw [h_silence, sub_self]
        have h_iter_ge_one : ∀ k : ℕ, 1 ≤ k → (ad (G : Matrix (Fin (X.n)) (Fin (X.n)) ℂ))^[k] X.A = 0 := by
          intro k hk
          induction' k with k ih
          · linarith
          · rw [Function.iterate_succ', Function.comp_apply, h_ad_zero]
            -- (ad G)^[k+1](X.A) = ad G ((ad G)^[k] (X.A)) = ad G(0) = 0
            -- Need to know ad G(0) = 0
            have h_ad_zero' : ad (G : Matrix (Fin (X.n)) (Fin (X.n)) ℂ) (0 : Matrix (Fin (X.n)) (Fin (X.n)) ℂ) = 0 := by
              simp [ad]
            rcases k with (rfl | k')
            · -- k = 0, but hk says 1 ≤ 0 → contradiction
              linarith
            · -- k = k'+1 ≥ 1, so (ad G)^[k](X.A) = 0 by IH
              have h_prev : (ad (G : Matrix (Fin (X.n)) (Fin (X.n)) ℂ))^[k'] X.A = 0 := ih (by omega)
              simp [h_prev, ad]
        have h_flow_eq_A : spectralFlowMap X.n G X.A t N = X.A := by
          dsimp [spectralFlowMap]
          -- spectralFlowMap = Σ_{i=0}^{N-1} (t^i/i!) • (ad G)^[i] X.A
          -- = (t^0/0!) • (ad G)^[0] X.A + Σ_{i=1}^{N-1} (t^i/i!) • (ad G)^[i] X.A
          -- = X.A + 0 = X.A
          calc
            ∑ i ∈ Finset.range N, ((t^i / Nat.factorial i : ℝ) : ℂ) • (ad (G : Matrix (Fin (X.n)) (Fin (X.n)) ℂ))^[i] X.A
                = X.A + ∑ i ∈ Finset.Ico 1 N, ((t^i / Nat.factorial i : ℝ) : ℂ) • (ad (G : Matrix (Fin (X.n)) (Fin (X.n)) ℂ))^[i] X.A := by
              rcases N with (rfl | N')
              · simp
              · simp [Finset.sum_range_succ, Finset.Ico_succ_singleton, Function.iterate_zero]
            _ = X.A + 0 := by
              refine congrArg (fun x => X.A + x) ?_
              simp [Finset.sum_eq_zero_of_forall_eq_zero, h_iter_ge_one]
            _ = X.A := by simp
        simpa [h_flow_eq_A] }

end UFPFormalization
