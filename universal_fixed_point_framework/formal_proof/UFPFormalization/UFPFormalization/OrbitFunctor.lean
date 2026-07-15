import Mathlib.GroupTheory.GroupAction.Basic
import Mathlib.Data.Fintype.Basic

namespace UFPFormalization

/-- Orbit equivalence relation induced by a group action. -/
def orbitRel (G X : Type) [Group G] [MulAction G X] : Setoid X :=
  MulAction.orbitRel G X

/-- Quotient of X by the G-orbit equivalence relation. -/
def orbitQuotient (G X : Type) [Group G] [MulAction G X] : Type _ :=
  Quotient (orbitRel G X)

/-- Orbit weight associated to a point.
    The Level-A prototype admits the concrete definition. -/
noncomputable def orbitWeight {G X : Type} [Group G] [Fintype G] [MulAction G X] (x : X) : ℕ :=
  sorry

/-- Orbit-stabilizer cardinality identity for finite group actions.
    Proof admitted in the Level-A prototype. -/
theorem orbitWeight_eq {G X : Type} [Group G] [Fintype G] [MulAction G X] [Fintype X] [DecidableEq X]
    (x : X) :
    orbitWeight (G := G) (X := X) x * Fintype.card G = Fintype.card G * orbitWeight (G := G) (X := X) x := by
  sorry

end UFPFormalization
