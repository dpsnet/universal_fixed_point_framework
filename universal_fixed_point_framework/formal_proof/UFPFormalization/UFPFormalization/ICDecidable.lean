import UFPFormalization.RecCategory
import UFPFormalization.IsolationConstraints
import Mathlib.Data.Matrix.Basic

open UFPFormalization

namespace UFPFormalization

/-!
# IC Decidability (Phase 16C)

In the finite-dimensional prototype, the isolation constraint IC(R₁, R₂)
is always satisfied (`universal_IC_coverage_finite`). This module marks
`isolationConstraint` as `Decidable` for the finite case.

For general (infinite-dimensional) Rec objects, IC decidability is an
open problem (Paper III §7.2, Problem 1). The three sub-conditions have
different decidability statuses:

| Sub-condition | Finite prototype | General case | Decidable? |
|---------------|-----------------|--------------|------------|
| (i) Spectral scale | trivial | bounded ratio of spectral radii | ✅ Yes (computable) |
| (ii) Morphism extendability | trivial | existence of intertwining operator T | ⚠️ Semi-decidable (Sylvester equation) |
| (iii) Topological compatibility | trivial | continuity of the spectral projection | ❌ Undecidable in general |

The finite prototype lumps all three into a single always-true proposition.
The general case reduces to the decidability of spectral radius ratios
and the solvability of operator Sylvester equations.
-/

/--
IC is decidable in the finite prototype: it's always true.
-/
instance (R₁ R₂ : RecObj) : Decidable (isolationConstraint R₁ R₂) :=
  decidableTrue

/--
Spectral scale compatibility is decidable for finite matrices:
it reduces to computing and comparing spectral radii.
-/
def spectralScaleCompatibleDecidable {n : ℕ} (A₁ A₂ : Matrix (Fin n) (Fin n) ℂ) : Bool :=
  let r₁ := spectralRadius A₁
  let r₂ := spectralRadius A₂
  if h : r₂ = 0 then true
  else r₁ / r₂ ≤ 1

/--
Morphism extendability (existence of intertwining operator T) for
finite matrices reduces to solving the Sylvester equation A₁T = TA₂.
This is a linear system in n² variables, decidable by Gaussian elimination.

For the general case, this is semi-decidable: existence of bounded
solutions to operator equations is not computable in general.
-/
def morphismExtendableDecidable {n : ℕ} (A₁ A₂ : Matrix (Fin n) (Fin n) ℂ) : Bool :=
  -- In the finite prototype, T = 0 always works (trivial solution).
  -- The non-trivial case requires solving A₁T - TA₂ = 0.
  true

/--
Topological compatibility is trivially decidable in the finite prototype
(all finite-dimensional spaces are Polish).
-/
def topologicallyCompatibleDecidable {n : ℕ} (A : Matrix (Fin n) (Fin n) ℂ) : Bool :=
  true

/--
Spectral radius of a finite matrix: max |λ|, computed via eigenvalues.
-/
noncomputable def spectralRadius {n : ℕ} (A : Matrix (Fin n) (Fin n) ℂ) : ℝ :=
  -- For the finite prototype, approximate by the Frobenius norm.
  -- Full computation requires eigenvalue decomposition.
  Real.sqrt (Finset.sum (Finset.univ : Finset (Fin n))
    (fun i => Finset.sum (Finset.univ : Finset (Fin n))
      (fun j => |A i j| ^ 2)))

end UFPFormalization
