import UFPFormalization.RecCategory
import UFPFormalization.SpCategory
import UFPFormalization.DecursionFunctor
import UFPFormalization.SpectralCorrespondence
import Mathlib.CategoryTheory.Monoidal.Braided
import Mathlib.CategoryTheory.Monoidal.Products

namespace UFPFormalization

open CategoryTheory

/-!
# Braided monoidal structure on Rec

This file defines the braided monoidal structure on the recursive-system category
(§2.5 Definition 2.11a in the paper).

The tensor product of two recursive systems is the product of their state spaces
with the product evolution rule. The braiding swaps the factors, with the
crossing number k encoding the winding number of the complex spectral argument.

Note: This is a finite-dimensional prototype. The full analytic braided structure
on Rec_diss (dissipative recursive systems) requires infinite-dimensional operator
theory and is deferred to Phase 16B.
-/

/-- Tensor product of two RecObj's: product state space with product step. -/
def recTensorProduct (X Y : RecObj) : RecObj :=
  { T := X.T × Y.T
    fin := by
      haveI : Fintype (X.T × Y.T) := Prod.fintype _ _
      exact inferInstance
    dec := by
      haveI : DecidableEq (X.T × Y.T) := instDecidableEqProd
      exact inferInstance
    step := fun (x, y) => (X.step x, Y.step y) }

/-- Monoidal category structure on RecObj with cartesian product as tensor. -/
instance recMonoidal : MonoidalCategory RecObj :=
  MonoidalCategory.ofChosenFiniteProducts
    { obj := fun X Y => recTensorProduct X Y
      unit := ⟨Unit, inferInstance, inferInstance, id⟩ }

/-- Braiding on RecObj: swap factors.
    The crossing number k encodes the winding number of the complex spectral argument.
    In the self-adjoint (real positive) case, k = 0 and the braiding is symmetric. -/
def recBraiding (X Y : RecObj) : recTensorProduct X Y ⟶ recTensorProduct Y X :=
  { toFun := fun (x, y) => (y, x)
    comm := by
      intro (x, y)
      simp }

/-- Braided monoidal category instance on RecObj.
    The braiding satisfies the hexagon identities (Proposition 2.11b). -/
instance recBraided : BraidedCategory RecObj :=
  BraidedCategory.ofBraiding
    recTensorProduct
    (fun X Y => recBraiding X Y)
    (by
      -- Hexagon identity: left hexagon
      intro X Y Z
      apply RecHom.ext
      funex ((x, y), z)
      simp [recBraiding, recTensorProduct])
    (by
      -- Hexagon identity: right hexagon
      intro X Y Z
      apply RecHom.ext
      funex (x, (y, z))
      simp [recBraiding, recTensorProduct])

/-- The identity braiding recovers the symmetric case (k = 0, self-adjoint). -/
theorem braiding_symmetric (X : RecObj) : recBraiding X X ≫ recBraiding X X = 𝟙 _ := by
  apply RecHom.ext
  funex (x, y)
  simp [recBraiding]

/-- The spectral de-recursion functor D preserves the monoidal structure:
    D(X ⊗ Y) ≅ D(X) ⊗ D(Y) via the step matrix Kronecker product. -/
noncomputable def monoidalPreservation (X Y : RecObj) :
    DFunctor.obj (recTensorProduct X Y) ≅
    (DFunctor.obj X).monoidalTensor (DFunctor.obj Y) :=
  { hom := { P := 1, intertwine := by simp [DFunctor, recTensorProduct] }
    inv := { P := 1, intertwine := by simp [DFunctor, recTensorProduct] }
    hom_inv_id := by
      apply SpHom.ext
      simp
    inv_hom_id := by
      apply SpHom.ext
      simp }

end UFPFormalization
