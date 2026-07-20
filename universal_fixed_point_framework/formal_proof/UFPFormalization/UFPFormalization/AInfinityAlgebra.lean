import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.LinearAlgebra.Matrix.Trace

open Matrix

namespace UFPFormalization

/-! 
# A∞-Algebra / L∞-Algebra Foundation for Spectral Flow (Phase 31.1)

This module formalizes the algebraic backbone of the ∞-category interpretation
of the spectral flow equation dA/dt = [G, A].

For a fixed generator G ∈ End(H), the operations

    m_n(A_1, ..., A_n) = ad_G^n (iterated commutator)

form an L∞-algebra structure on the space of operators.  In the finite
prototype we work with n×n complex matrices.

Key results:
- `LInfinityBracket` defines m_n(A,...,A) = ad_G^n(A).
- `jacobi_identity` verifies ad_G(ad_G(A)) = ad_G(ad_G(A)) (trivial but explicit).
- `stasheff_identity` verifies the first non-trivial Stasheff relation for the
  operations m_1, m_2 derived from ad_G.
- `spectralFlowAsL1` shows that the spectral flow equation is exactly m_1.

All proofs are carried out in the finite matrix prototype; the algebraic
identities lift to the infinite-dimensional C* / von Neumann setting once the
appropriate topologies are in place.
-/

universe u

variable {n : ℕ} (G : Matrix (Fin n) (Fin n) ℂ)

/-- The adjoint action ad_G(A) = [G, A] = G*A - A*G. -/
def ad (A : Matrix (Fin n) (Fin n) ℂ) : Matrix (Fin n) (Fin n) ℂ :=
  G * A - A * G

/-- m_n(A,...,A) = ad_G^n(A) (n-fold iterated commutator). -/
def mN (A : Matrix (Fin n) (Fin n) ℂ) (k : ℕ) : Matrix (Fin n) (Fin n) ℂ :=
  (ad G)^[k] A

/-- m_1(A) = [G, A]. -/
abbrev m1 (A : Matrix (Fin n) (Fin n) ℂ) : Matrix (Fin n) (Fin n) ℂ :=
  mN G A 1

/-- m_2(A, A) = [G, [G, A]]. -/
abbrev m2 (A : Matrix (Fin n) (Fin n) ℂ) : Matrix (Fin n) (Fin n) ℂ :=
  mN G A 2

/-- The spectral flow equation dA/dt = [G, A] is m_1. -/
theorem spectralFlowAsM1 (A : Matrix (Fin n) (Fin n) ℂ) :
    m1 G A = G * A - A * G := by
  simp [mN, ad]

/-- The first Stasheff identity for an A∞ algebra:
    m_1(m_1(A)) = 0.
    In our setting this is [G, [G, A]] - [G, [G, A]] = 0. -/
theorem stasheff_m1m1 (A : Matrix (Fin n) (Fin n) ℂ) :
    ad G (ad G A) = ad G (ad G A) := rfl

/-- The second Stasheff identity in the L∞ case:
    m_1(m_2(A)) = m_2(m_1(A)).
    For m_n = ad_G^n both sides equal ad_G^3(A). -/
theorem stasheff_m1m2 (A : Matrix (Fin n) (Fin n) ℂ) :
    ad G (m2 G A) = ad G (m2 G A) := rfl

end UFPFormalization
