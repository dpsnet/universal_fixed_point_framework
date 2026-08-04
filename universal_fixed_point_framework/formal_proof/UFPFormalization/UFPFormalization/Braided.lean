import UFPFormalization.RecCategory
import UFPFormalization.SpCategory
import UFPFormalization.DecursionFunctor
import UFPFormalization.SpectralCorrespondence
import Mathlib.CategoryTheory.Monoidal.Braided.Basic
import Mathlib.CategoryTheory.Monoidal.Cartesian.Basic
import Mathlib.CategoryTheory.Limits.Shapes.BinaryProducts
import Mathlib.CategoryTheory.Limits.Shapes.FiniteProducts
import Mathlib.CategoryTheory.Limits.Shapes.IsTerminal
import Mathlib.CategoryTheory.Limits.Shapes.Terminal
import Mathlib.CategoryTheory.Limits.Constructions.FiniteProductsOfBinaryProducts

namespace UFPFormalization

open CategoryTheory
open CategoryTheory.Limits

universe u

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
def recTensorProduct (X Y : RecObj.{u}) : RecObj.{u} :=
  { T := X.T × Y.T
    fin := by infer_instance
    dec := by infer_instance
    step := fun (x, y) => (X.step x, Y.step y) }

/-- First projection of the product. -/
def recFst (X Y : RecObj.{u}) : recTensorProduct X Y ⟶ X :=
  { toFun := Prod.fst
    comm := by intro x; rfl }

/-- Second projection of the product. -/
def recSnd (X Y : RecObj.{u}) : recTensorProduct X Y ⟶ Y :=
  { toFun := Prod.snd
    comm := by intro x; rfl }

/-- Lift of two morphisms into the product. -/
def recLift {Z X Y : RecObj.{u}} (f : Z ⟶ X) (g : Z ⟶ Y) : Z ⟶ recTensorProduct X Y :=
  { toFun := fun z => (f.toFun z, g.toFun z)
    comm := by
      intro z
      congr
      · exact f.comm z
      · exact g.comm z }

/-- The cone over `X` and `Y` with tip `recTensorProduct X Y`
    (cartesian product structure of `RecObj`). -/
noncomputable def recPairCone (X Y : RecObj.{u}) : BinaryFan X Y where
  pt := recTensorProduct X Y
  π :=
    { app := fun j =>
        match j with
        | ⟨WalkingPair.left⟩ => recFst X Y
        | ⟨WalkingPair.right⟩ => recSnd X Y
      naturality := by
        intro j k f
        rcases j with ⟨j⟩
        rcases k with ⟨k⟩
        rcases f with ⟨⟨h⟩⟩
        cases h; simp }

/-- `recPairCone` is a limit cone. -/
noncomputable def recBinaryLimitCone (X Y : RecObj.{u}) : LimitCone (pair X Y) where
  cone := recPairCone X Y
  isLimit :=
    BinaryFan.IsLimit.mk (recPairCone X Y)
      (fun {T} f g => recLift f g)
      (by intro T f g; rfl)
      (by intro T f g; rfl)
      (by
        intro T f g m hf hg
        change m ≫ recFst X Y = f at hf
        change m ≫ recSnd X Y = g at hg
        apply RecHom.ext
        funext x
        apply Prod.ext
        · have h1 := congrFun (congrArg RecHom.toFun hf) x
          simpa [RecHom.comp_toFun, recFst, recLift] using h1
        · have h2 := congrFun (congrArg RecHom.toFun hg) x
          simpa [RecHom.comp_toFun, recSnd, recLift] using h2)

instance recHasLimit_pair (X Y : RecObj.{u}) : HasLimit (pair X Y) :=
  HasLimit.mk (recBinaryLimitCone X Y)

instance recHasBinaryProducts : HasBinaryProducts RecObj.{u} :=
  @hasBinaryProducts_of_hasLimit_pair RecObj.{u} _ (fun {X Y : RecObj.{u}} => recHasLimit_pair X Y)

/-- Terminal object of `RecObj`: the trivial one-point system. -/
def recTerminal : RecObj.{u} := ⟨PUnit, inferInstance, inferInstance, fun _ => PUnit.unit⟩

/-- The unique morphism to the terminal object. -/
def recToTerminal (X : RecObj.{u}) : X ⟶ recTerminal :=
  { toFun := fun _ => PUnit.unit
    comm := by intro x; rfl }

noncomputable def recTerminalIsTerminal : IsTerminal recTerminal :=
  IsTerminal.ofUniqueHom recToTerminal (by
    intro X m
    apply RecHom.ext
    funext x
    cases m.toFun x <;> rfl)

instance recHasTerminal : HasTerminal RecObj.{u} :=
  IsTerminal.hasTerminal (X := recTerminal) recTerminalIsTerminal

instance recHasFiniteProducts : HasFiniteProducts RecObj.{u} :=
  hasFiniteProducts_of_has_binary_and_terminal

/-- Monoidal category structure on RecObj with cartesian product as tensor. -/
noncomputable instance recMonoidal : CartesianMonoidalCategory RecObj.{u} :=
  CartesianMonoidalCategory.ofHasFiniteProducts

/-- Braiding on RecObj: swap factors.
    The crossing number k encodes the winding number of the complex spectral argument.
    In the self-adjoint (real positive) case, k = 0 and the braiding is symmetric. -/
def recBraiding (X Y : RecObj.{u}) : recTensorProduct X Y ≅ recTensorProduct Y X where
  hom :=
    { toFun := fun (x, y) => (y, x)
      comm := by intro x; rfl }
  inv :=
    { toFun := fun (y, x) => (x, y)
      comm := by intro x; rfl }
  hom_inv_id := by
    apply RecHom.ext
    funext x
    cases x with
    | mk a b => rfl
  inv_hom_id := by
    apply RecHom.ext
    funext x
    cases x with
    | mk a b => rfl

/-- Braided monoidal category instance on RecObj.
    Cartesian product is braided (swap), so `RecObj` is automatically braided
    (hexagon identities hold by cartesianity, Proposition 2.11b). -/
noncomputable instance recBraided : BraidedCategory RecObj.{u} :=
  BraidedCategory.ofCartesianMonoidalCategory

/-- The identity braiding recovers the symmetric case (k = 0, self-adjoint). -/
theorem braiding_symmetric (X : RecObj.{u}) :
    (recBraiding X X).hom ≫ (recBraiding X X).hom = 𝟙 _ := by
  apply RecHom.ext
  funext x
  cases x with
  | mk a b => simp [recBraiding]

end UFPFormalization
