import Mathlib.GroupTheory.GroupAction.Basic
import Mathlib.GroupTheory.GroupAction.Quotient
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Set.Finite.Range

namespace UFPFormalization

/-- Orbit equivalence relation induced by a group action. -/
def orbitRel (G X : Type) [Group G] [MulAction G X] : Setoid X :=
  MulAction.orbitRel G X

/-- Quotient of X by the G-orbit equivalence relation. -/
def orbitQuotient (G X : Type) [Group G] [MulAction G X] : Type _ :=
  Quotient (orbitRel G X)

/-- Fintype instance for the orbit of a point under a finite group action. -/
instance orbitFintype {G X : Type} [Group G] [Fintype G] [MulAction G X] [Fintype X] [DecidableEq X]
    (x : X) : Fintype (MulAction.orbit G x) :=
  Set.fintypeRange (fun g : G => g • x)

/-- Orbit weight associated to a point: the cardinality of its orbit. -/
noncomputable def orbitWeight {G X : Type} [Group G] [Fintype G] [MulAction G X] [Fintype X]
    [DecidableEq X] (x : X) : ℕ :=
  Fintype.card (MulAction.orbit G x)

/-- Orbit-stabilizer cardinality identity for finite group actions:
    |Orbit(x)| · |Stab(x)| = |G|. -/
theorem orbitStabilizer {G X : Type} [Group G] [Fintype G] [DecidableEq G] [MulAction G X]
    [Fintype X] [DecidableEq X] (x : X) :
    Fintype.card (MulAction.orbit G x) * Fintype.card (MulAction.stabilizer G x) = Fintype.card G := by
  haveI := orbitFintype (G := G) (X := X) x
  convert MulAction.card_orbit_mul_card_stabilizer_eq_card_group (α := G) (β := X) x

/-- A trivial symmetry of the orbit weight definition (commutativity). -/
theorem orbitWeight_eq {G X : Type} [Group G] [Fintype G] [MulAction G X] [Fintype X]
    [DecidableEq X] (x : X) :
    orbitWeight (G := G) (X := X) x * Fintype.card G = Fintype.card G * orbitWeight (G := G) (X := X) x := by
  rw [mul_comm]

end UFPFormalization
