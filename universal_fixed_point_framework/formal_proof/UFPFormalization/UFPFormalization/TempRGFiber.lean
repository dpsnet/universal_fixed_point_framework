/-
# TempRGFiber.lean — Phase 54B Grothendieck Fiber Category Formalization

Three components:
  1. Base categories TempCat and RGCat with their isomorphism 𝒯
  2. Grothendieck fibration structure for spectral bundles over Temp and RG
  3. Fibered functor T̂_Riem : Bun(Temp, Spec) → Bun(RG, Spec)

Based on the mathematical framework in
  spectral_T_category.md v0.1
  spectral_Riem_functoriality.md v0.2
  spectral_Grothendieck_fibration.md v0.1
-/

import Mathlib.CategoryTheory.Category.Basic
import Mathlib.CategoryTheory.Functor.Basic
import Mathlib.CategoryTheory.NatTrans
import Mathlib.CategoryTheory.Adjunction.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Tactic
import UFPFormalization.RecCategory
import UFPFormalization.SpecCategory

open CategoryTheory

namespace UFPFormalization

universe u

/-! =========================================================
    Section 1: Base Categories — TempCat & RGCat
   ========================================================= -/

/-- Temperature category objects: positive real numbers T > 0. -/
structure TempObj where
  T : ℝ
  pos : T > 0

/-- RGCat (RG scale) category objects: positive real scale μ > 0. -/
structure RGObj where
  μ : ℝ
  pos : μ > 0

/-- Morphism in TempCat: a positive ratio r such that T₂ = r·T₁. -/
@[ext]
structure TempHom (X Y : TempObj) where
  r : ℝ
  r_pos : r > 0
  eq : r * X.T = Y.T

/-- Morphism in RGCat: a positive ratio s such that μ₂ = s·μ₁. -/
@[ext]
structure RGHom (X Y : RGObj) where
  s : ℝ
  s_pos : s > 0
  eq : s * X.μ = Y.μ

instance tempCategory : Category TempObj where
  Hom X Y := TempHom X Y
  id X := ⟨1, by linarith, by simp⟩
  comp {X Y Z} f g := ⟨g.r * f.r, mul_pos g.r_pos f.r_pos, by
    calc
      (g.r * f.r) * X.T = g.r * (f.r * X.T) := by ring
      _ = g.r * Y.T := by rw [f.eq]
      _ = Z.T := g.eq
    ⟩
  id_comp := by
    intro X Y f; ext; simp
  comp_id := by
    intro X Y f; ext; simp
  assoc := by
    intro W X Y Z f g h
    ext; ring

instance rgCategory : Category RGObj where
  Hom X Y := RGHom X Y
  id X := ⟨1, by linarith, by simp⟩
  comp {X Y Z} f g := ⟨g.s * f.s, mul_pos g.s_pos f.s_pos, by
    calc
      (g.s * f.s) * X.μ = g.s * (f.s * X.μ) := by ring
      _ = g.s * Y.μ := by rw [f.eq]
      _ = Z.μ := g.eq
    ⟩
  id_comp := by
    intro X Y f; ext; simp
  comp_id := by
    intro X Y f; ext; simp
  assoc := by
    intro W X Y Z f g h
    ext; ring

@[simp]
lemma TempHom.id_r (X : TempObj) : ((𝟙 X) : TempHom X X).r = 1 := rfl

@[simp]
lemma TempHom.comp_r {X Y Z : TempObj} (f : X ⟶ Y) (g : Y ⟶ Z) :
    ((f ≫ g) : TempHom X Z).r = g.r * f.r := rfl

@[simp]
lemma RGHom.id_s (X : RGObj) : ((𝟙 X) : RGHom X X).s = 1 := rfl

@[simp]
lemma RGHom.comp_s {X Y Z : RGObj} (f : X ⟶ Y) (g : Y ⟶ Z) :
    ((f ≫ g) : RGHom X Z).s = g.s * f.s := rfl

/-! =========================================================
    Section 2: TempRG Isomorphism 𝒯 : TempCat ≅ RGCat
   ========================================================= -/

/-- The functor 𝒯 : TempCat → RGCat given by 𝒯(T) = T.
    Since TempCat and RGCat are isomorphic as categories
    (both are ℝ⁺ with dilation morphisms), 𝒯 acts identically. -/
noncomputable def TFunctor : TempObj ⥤ RGObj where
  obj X := ⟨X.T, X.pos⟩
  map f := ⟨f.r, f.r_pos, f.eq⟩
  map_id X := rfl
  map_comp f g := rfl

/-- The inverse functor 𝒯⁻¹ : RGCat → TempCat, also acting identically. -/
noncomputable def TInvFunctor : RGObj ⥤ TempObj where
  obj X := ⟨X.μ, X.pos⟩
  map f := ⟨f.s, f.s_pos, f.eq⟩
  map_id X := rfl
  map_comp f g := rfl

/-- Unit of the isomorphism: 𝟭 Temp ≅ 𝒯 ⋙ 𝒯⁻¹. -/
noncomputable def TUnitIso : 𝟭 TempObj ≅ TFunctor ⋙ TInvFunctor where
  hom :=
    { app := fun X => ⟨1, by norm_num, by simp [TFunctor, TInvFunctor]⟩
      naturality := fun {X Y} f => by
        apply TempHom.ext
        simp [TFunctor, TInvFunctor] }
  inv :=
    { app := fun X => ⟨1, by norm_num, by simp [TFunctor, TInvFunctor]⟩
      naturality := fun {X Y} f => by
        apply TempHom.ext
        simp [TFunctor, TInvFunctor] }
  hom_inv_id := by
    apply NatTrans.ext; funext X; apply TempHom.ext; simp
  inv_hom_id := by
    apply NatTrans.ext; funext X; apply TempHom.ext; simp

/-- Counit of the isomorphism: 𝒯⁻¹ ⋙ 𝒯 ≅ 𝟭 RG. -/
noncomputable def TCounitIso : TInvFunctor ⋙ TFunctor ≅ 𝟭 RGObj where
  hom :=
    { app := fun X => ⟨1, by norm_num, by simp [TFunctor, TInvFunctor]⟩
      naturality := fun {X Y} f => by
        apply RGHom.ext
        simp [TFunctor, TInvFunctor] }
  inv :=
    { app := fun X => ⟨1, by norm_num, by simp [TFunctor, TInvFunctor]⟩
      naturality := fun {X Y} f => by
        apply RGHom.ext
        simp [TFunctor, TInvFunctor] }
  hom_inv_id := by
    apply NatTrans.ext; funext X; apply RGHom.ext; simp
  inv_hom_id := by
    apply NatTrans.ext; funext X; apply RGHom.ext; simp

/-- The category equivalence TempCat ≌ RGCat. -/
noncomputable def TempIsoRG : TempObj ≌ RGObj :=
  CategoryTheory.Equivalence.mk TFunctor TInvFunctor TUnitIso TCounitIso

/-! =========================================================
    Section 3: Spectral Bundle Total Category
   ========================================================= -/

/-- Fiber category: spectral data over a temperature base point.
    The fiber is equivalent to SpecObj at that temperature.
    In this finite prototype, the fiber data is a SpecObj (matrix A)
    annotated with the base point for tracking. -/
structure SpecFiberTemp (T : TempObj) where
  n : ℕ
  A : Matrix (Fin n) (Fin n) ℂ

/-- Fiber category: spectral data over an RG scale base point. -/
structure SpecFiberRG (μ : RGObj) where
  n : ℕ
  A : Matrix (Fin n) (Fin n) ℂ

/-- Total category Bun(Temp, Spec): pairs (T, spectral data over T). -/
@[ext]
structure SpectralBundleTemp where
  base : TempObj
  fiberData : SpecFiberTemp base

/-- Total category Bun(RG, Spec): pairs (μ, spectral data over μ). -/
@[ext]
structure SpectralBundleRG where
  base : RGObj
  fiberData : SpecFiberRG base

/-- Morphism in Bun(Temp, Spec): a base dilation f: T₁ → T₂ and a spectral
    transformation φ intertwining the spectral data under the dilation. -/
@[ext]
structure BundleTempHom (X Y : SpectralBundleTemp) where
  baseMap : X.base ⟶ Y.base
  fiberMap : Matrix (Fin X.fiberData.n) (Fin Y.fiberData.n) ℂ
  commut : fiberMap * Y.fiberData.A = X.fiberData.A * fiberMap

/-- Morphism in Bun(RG, Spec): analogous to BundleTempHom. -/
@[ext]
structure BundleRGHom (X Y : SpectralBundleRG) where
  baseMap : X.base ⟶ Y.base
  fiberMap : Matrix (Fin X.fiberData.n) (Fin Y.fiberData.n) ℂ
  commut : fiberMap * Y.fiberData.A = X.fiberData.A * fiberMap

instance bundleTempCategory : Category SpectralBundleTemp where
  Hom X Y := BundleTempHom X Y
  id X :=
    { baseMap := 𝟙 X.base
      fiberMap := 1
      commut := by simp }
  comp {X Y Z} f g :=
    { baseMap := f.baseMap ≫ g.baseMap
      fiberMap := f.fiberMap * g.fiberMap
      commut := by
        calc
          (f.fiberMap * g.fiberMap) * Z.fiberData.A
              = f.fiberMap * (g.fiberMap * Z.fiberData.A) := Matrix.mul_assoc _ _ _
          _ = f.fiberMap * (Y.fiberData.A * g.fiberMap) := by rw [g.commut]
          _ = (f.fiberMap * Y.fiberData.A) * g.fiberMap := (Matrix.mul_assoc _ _ _).symm
          _ = (X.fiberData.A * f.fiberMap) * g.fiberMap := by rw [f.commut]
          _ = X.fiberData.A * (f.fiberMap * g.fiberMap) := Matrix.mul_assoc _ _ _
    }
  id_comp := by
    intro X Y f
    apply BundleTempHom.ext
    · simp
    · exact Matrix.one_mul _
  comp_id := by
    intro X Y f
    apply BundleTempHom.ext
    · simp
    · exact Matrix.mul_one _
  assoc := by
    intro W X Y Z f g h
    apply BundleTempHom.ext
    · simp
    · exact Matrix.mul_assoc _ _ _

instance bundleRGategory : Category SpectralBundleRG where
  Hom X Y := BundleRGHom X Y
  id X :=
    { baseMap := 𝟙 X.base
      fiberMap := 1
      commut := by simp }
  comp {X Y Z} f g :=
    { baseMap := f.baseMap ≫ g.baseMap
      fiberMap := f.fiberMap * g.fiberMap
      commut := by
        calc
          (f.fiberMap * g.fiberMap) * Z.fiberData.A = f.fiberMap * (g.fiberMap * Z.fiberData.A) := Matrix.mul_assoc _ _ _
          _ = f.fiberMap * (Y.fiberData.A * g.fiberMap) := by rw [g.commut]
          _ = (f.fiberMap * Y.fiberData.A) * g.fiberMap := (Matrix.mul_assoc _ _ _).symm
          _ = (X.fiberData.A * f.fiberMap) * g.fiberMap := by rw [f.commut]
          _ = X.fiberData.A * (f.fiberMap * g.fiberMap) := Matrix.mul_assoc _ _ _
    }
  id_comp := by
    intro X Y f
    apply BundleRGHom.ext
    · simp
    · exact Matrix.one_mul _
  comp_id := by
    intro X Y f
    apply BundleRGHom.ext
    · simp
    · exact Matrix.mul_one _
  assoc := by
    intro W X Y Z f g h
    apply BundleRGHom.ext
    · simp
    · exact Matrix.mul_assoc _ _ _

@[simp]
lemma BundleTempHom.id_baseMap (X : SpectralBundleTemp) :
    ((𝟙 X) : BundleTempHom X X).baseMap = 𝟙 X.base := rfl

@[simp]
lemma BundleTempHom.comp_baseMap {X Y Z : SpectralBundleTemp} (f : X ⟶ Y) (g : Y ⟶ Z) :
    ((f ≫ g) : BundleTempHom X Z).baseMap = f.baseMap ≫ g.baseMap := rfl

@[simp]
lemma BundleRGHom.id_baseMap (X : SpectralBundleRG) :
    ((𝟙 X) : BundleRGHom X X).baseMap = 𝟙 X.base := rfl

@[simp]
lemma BundleRGHom.comp_baseMap {X Y Z : SpectralBundleRG} (f : X ⟶ Y) (g : Y ⟶ Z) :
    ((f ≫ g) : BundleRGHom X Z).baseMap = f.baseMap ≫ g.baseMap := rfl

/-! =========================================================
    Section 4: Projection Functors π_T and π_μ
   ========================================================= -/

/-- Projection π_T : Bun(Temp, Spec) → TempCat. -/
abbrev π_T : SpectralBundleTemp ⥤ TempObj where
  obj b := b.base
  map f := f.baseMap
  map_id X := rfl
  map_comp f g := rfl

/-- Projection π_μ : Bun(RG, Spec) → RGCat. -/
abbrev π_μ : SpectralBundleRG ⥤ RGObj where
  obj b := b.base
  map f := f.baseMap
  map_id X := rfl
  map_comp f g := rfl

/-! =========================================================
    Section 5: Cartesian Lifts (Grothendieck Fibration)
   ========================================================= -/

/-- Data for a Grothendieck fibration: for every object e in the total
    category and every morphism f : b' → π(e) in the base, we can construct
    a Cartesian lift. -/
structure CartesianLiftData {E B : Type u} [Category E] [Category B] (p : E ⥤ B) where
  lift {e : E} {b' : B} (f : b' ⟶ p.obj e) : E
  lift_base {e : E} {b' : B} (f : b' ⟶ p.obj e) : p.obj (lift f) = b'
  cartesian_morphism {e : E} {b' : B} (f : b' ⟶ p.obj e) : lift f ⟶ e
  cartesian_base {e : E} {b' : B} (f : b' ⟶ p.obj e) :
    p.map (cartesian_morphism f) = eqToHom (lift_base f) ≫ f
  cartesian_universal {e : E} {b' : B} (f : b' ⟶ p.obj e) (Z : E) (h : Z ⟶ e)
    (w : p.obj Z ⟶ b') (h_comp : p.map h = w ≫ f) : Z ⟶ lift f
  cartesian_universal_prop {e : E} {b' : B} (f : b' ⟶ p.obj e) (Z : E) (h : Z ⟶ e)
    (w : p.obj Z ⟶ b') (h_comp : p.map h = w ≫ f) :
    h = cartesian_universal f Z h w h_comp ≫ cartesian_morphism f
  cartesian_universal_base {e : E} {b' : B} (f : b' ⟶ p.obj e) (Z : E) (h : Z ⟶ e)
    (w : p.obj Z ⟶ b') (h_comp : p.map h = w ≫ f) :
    p.map (cartesian_universal f Z h w h_comp) = w ≫ eqToHom (lift_base f).symm

/-- A Grothendieck fibration is a functor equipped with Cartesian lift data. -/
class GrothendieckFibration {E B : Type u} [Category E] [Category B] (p : E ⥤ B) where
  cartesianLiftData : CartesianLiftData p

/-- Reducible helper: the lifted object over a new base point for Bun(Temp, Spec).
    In this finite prototype the spectral flow preserves the matrix A
    (identity pullback under temperature dilation). -/
abbrev liftTempObj (e : SpectralBundleTemp) (b' : TempObj) : SpectralBundleTemp :=
  { base := b'
    fiberData := { n := e.fiberData.n, A := e.fiberData.A } }

/-- Reducible helper: the lifted object over a new base point for Bun(RG, Spec). -/
abbrev liftRGObj (e : SpectralBundleRG) (b' : RGObj) : SpectralBundleRG :=
  { base := b'
    fiberData := { n := e.fiberData.n, A := e.fiberData.A } }

-- sanity checks on definitional unfolding
example (e : SpectralBundleTemp) (b' : TempObj) : (liftTempObj e b').base = b' := rfl
example (e : SpectralBundleTemp) : (π_T.obj e) = e.base := rfl
example (Z e : SpectralBundleTemp) (h : Z ⟶ e) : π_T.map h = h.baseMap := rfl

/-- π_T admits a Grothendieck fibration structure.
    Given a target (T₂, {λ_i}) and a base map f : T₁ → T₂, we construct the
    lift (T₁, f*{λ_i}) where f*{λ_i} is the spectral data pulled back through
    the spectral flow map. -/
noncomputable def π_T_cartesianLift : CartesianLiftData π_T where
  lift {e} {b'} _f := liftTempObj e b'
  lift_base _f := rfl
  cartesian_morphism {e} {b'} f :=
    { baseMap := f
      fiberMap := 1
      commut := by simp
    }
  cartesian_base _f := by simp
  cartesian_universal {e} {b'} f Z h w h_comp :=
    { baseMap := w
      fiberMap := h.fiberMap
      commut := h.commut
    }
  cartesian_universal_prop {e} {b'} f Z h w h_comp := by
    apply BundleTempHom.ext
    · -- base component: h.baseMap = w ≫ f, given by h_comp (π_T.map h = h.baseMap)
      simpa [π_T] using h_comp
    · -- fiber component: h.fiberMap = h.fiberMap * 𝟙
      exact (Matrix.mul_one h.fiberMap).symm
  cartesian_universal_base {e} {b'} f Z h w h_comp := by simp

noncomputable instance π_T_fibration : GrothendieckFibration π_T :=
  { cartesianLiftData := π_T_cartesianLift }

/-- π_μ admits a Grothendieck fibration structure, dual to π_T. -/
noncomputable def π_μ_cartesianLift : CartesianLiftData π_μ where
  lift {e} {b'} _f := liftRGObj e b'
  lift_base _f := rfl
  cartesian_morphism {e} {b'} f :=
    { baseMap := f
      fiberMap := 1
      commut := by simp
    }
  cartesian_base _f := by simp
  cartesian_universal {e} {b'} f Z h w h_comp :=
    { baseMap := w
      fiberMap := h.fiberMap
      commut := h.commut
    }
  cartesian_universal_prop {e} {b'} f Z h w h_comp := by
    apply BundleRGHom.ext
    · simpa [π_μ] using h_comp
    · exact (Matrix.mul_one h.fiberMap).symm
  cartesian_universal_base {e} {b'} f Z h w h_comp := by simp

noncomputable instance π_μ_fibration : GrothendieckFibration π_μ :=
  { cartesianLiftData := π_μ_cartesianLift }

/-! =========================================================
    Section 6: Fibered Functor T̂_Riem : Bun(Temp, Spec) → Bun(RG, Spec)
   ========================================================= -/

/-- The fibered functor T̂_Riem : Bun(Temp, Spec) → Bun(RG, Spec).
    It maps the base via 𝒯 and acts as the identity on the spectral fiber
    (in this finite prototype, spectral flow preserves the matrix A). -/
noncomputable def T_hat_Riem : SpectralBundleTemp ⥤ SpectralBundleRG where
  obj X :=
    { base := ⟨X.base.T, X.base.pos⟩
      fiberData :=
        { n := X.fiberData.n
          A := X.fiberData.A
        }
    }
  map f :=
    { baseMap := ⟨f.baseMap.r, f.baseMap.r_pos, f.baseMap.eq⟩
      fiberMap := f.fiberMap
      commut := f.commut
    }
  map_id X := by
    apply BundleRGHom.ext
    · -- base map: TFunctor.map (𝟙 X.base) = 𝟙 (T_hat_Riem.obj X).base
      apply RGHom.ext
      simp [TFunctor, RGHom.id_s]
    · -- fiber map
      rfl
  map_comp f g := by
    apply BundleRGHom.ext
    · -- base map commutes with composition
      apply RGHom.ext
      simp [TFunctor, RGHom.comp_s]
    · -- fiber map
      rfl

/-- T̂_Riem is base-faithful: the induced base map equals TFunctor applied to base. -/
theorem T_hat_Riem_base_commutes (X : SpectralBundleTemp) :
    π_μ.obj (T_hat_Riem.obj X) = TFunctor.obj (π_T.obj X) := rfl

theorem T_hat_Riem_map_base_commutes {X Y : SpectralBundleTemp} (f : X ⟶ Y) :
    π_μ.map (T_hat_Riem.map f) = TFunctor.map (π_T.map f) := rfl

/-- T̂_Riem preserves Cartesian morphisms (component-wise formulation).
    In this finite prototype, Cartesian lifts are mapped to Cartesian lifts
    because the spectral flow is identity on the fibers. -/
theorem T_hat_Riem_preserves_cartesian {e : SpectralBundleTemp} {b' : TempObj}
    (f : b' ⟶ π_T.obj e) :
    T_hat_Riem.obj (π_T_cartesianLift.lift f) =
      π_μ_cartesianLift.lift (e := T_hat_Riem.obj e) (b' := TFunctor.obj b') (TFunctor.map f) ∧
    (T_hat_Riem.map (π_T_cartesianLift.cartesian_morphism f)).baseMap.s =
      (π_μ_cartesianLift.cartesian_morphism (e := T_hat_Riem.obj e) (b' := TFunctor.obj b')
        (TFunctor.map f)).baseMap.s ∧
    (T_hat_Riem.map (π_T_cartesianLift.cartesian_morphism f)).fiberMap =
      (π_μ_cartesianLift.cartesian_morphism (e := T_hat_Riem.obj e) (b' := TFunctor.obj b')
        (TFunctor.map f)).fiberMap := by
  constructor
  · -- sources are equal: both are ⟨TFunctor.obj b', ⟨e.fiberData.n, e.fiberData.A⟩⟩
    apply SpectralBundleRG.ext
    · -- base: ⟨b'.T, b'.pos⟩ = ⟨b'.T, b'.pos⟩
      rfl
    · -- fiberData (HEq; types coincide by the base equality above)
      rfl
  constructor
  · -- base map s-field equality: both equal f.r
    rfl
  · -- fiber map equality: both equal 𝟙
    rfl

/-! =========================================================
    Section 6.5: Splitting of the Cleavages (Note Prop 2.2)
   ========================================================= -/

/-- The cleavage of π_T is split on identities: the lift of 𝟙 is the object itself
    (Prop 2.2, part 1). -/
theorem π_T_cleavage_id {e : SpectralBundleTemp} :
    π_T_cartesianLift.lift (𝟙 (π_T.obj e)) = e := by
  apply SpectralBundleTemp.ext
  · rfl
  · rfl

/-- The Cartesian morphism over 𝟙 has identity base component. -/
theorem π_T_cleavage_id_cartesian_base {e : SpectralBundleTemp} :
    (π_T_cartesianLift.cartesian_morphism (𝟙 (π_T.obj e))).baseMap = 𝟙 e.base := rfl

/-- The Cartesian morphism over 𝟙 has identity fiber component. -/
theorem π_T_cleavage_id_cartesian_fiber {e : SpectralBundleTemp} :
    (π_T_cartesianLift.cartesian_morphism (𝟙 (π_T.obj e))).fiberMap =
      (1 : Matrix (Fin e.fiberData.n) (Fin e.fiberData.n) ℂ) := rfl

/-- The cleavage of π_T is split on composition: the lift of g ∘ f equals the lift
    of f computed over the lifted object of g (Prop 2.2, part 2). -/
theorem π_T_cleavage_comp {e : SpectralBundleTemp} {b₀ b₁ : TempObj}
    (f : b₀ ⟶ b₁) (g : b₁ ⟶ π_T.obj e) :
    π_T_cartesianLift.lift (f ≫ g) =
      π_T_cartesianLift.lift (e := π_T_cartesianLift.lift g) f := rfl

/-- The Cartesian morphism over g ∘ f has the expected base component. -/
theorem π_T_cleavage_comp_cartesian_base {e : SpectralBundleTemp} {b₀ b₁ : TempObj}
    (f : b₀ ⟶ b₁) (g : b₁ ⟶ π_T.obj e) :
    (π_T_cartesianLift.cartesian_morphism (f ≫ g)).baseMap = f ≫ g := rfl

/-- The Cartesian morphism over g ∘ f has fiber component 𝟙 = 𝟙 * 𝟙,
    matching the composite of the individual Cartesian morphisms. -/
theorem π_T_cleavage_comp_cartesian_fiber {e : SpectralBundleTemp} {b₀ b₁ : TempObj}
    (f : b₀ ⟶ b₁) (g : b₁ ⟶ π_T.obj e) :
    (π_T_cartesianLift.cartesian_morphism (f ≫ g)).fiberMap =
      (π_T_cartesianLift.cartesian_morphism (e := π_T_cartesianLift.lift g) f).fiberMap *
        (π_T_cartesianLift.cartesian_morphism g).fiberMap :=
  (Matrix.one_mul 1).symm

/-- RG dual: cleavage of π_μ is split on identities. -/
theorem π_μ_cleavage_id {e : SpectralBundleRG} :
    π_μ_cartesianLift.lift (𝟙 (π_μ.obj e)) = e := by
  apply SpectralBundleRG.ext
  · rfl
  · rfl

/-- RG dual: Cartesian morphism over 𝟙 has identity base component. -/
theorem π_μ_cleavage_id_cartesian_base {e : SpectralBundleRG} :
    (π_μ_cartesianLift.cartesian_morphism (𝟙 (π_μ.obj e))).baseMap = 𝟙 e.base := rfl

/-- RG dual: Cartesian morphism over 𝟙 has identity fiber component. -/
theorem π_μ_cleavage_id_cartesian_fiber {e : SpectralBundleRG} :
    (π_μ_cartesianLift.cartesian_morphism (𝟙 (π_μ.obj e))).fiberMap =
      (1 : Matrix (Fin e.fiberData.n) (Fin e.fiberData.n) ℂ) := rfl

/-- RG dual: cleavage of π_μ is split on composition. -/
theorem π_μ_cleavage_comp {e : SpectralBundleRG} {b₀ b₁ : RGObj}
    (f : b₀ ⟶ b₁) (g : b₁ ⟶ π_μ.obj e) :
    π_μ_cartesianLift.lift (f ≫ g) =
      π_μ_cartesianLift.lift (e := π_μ_cartesianLift.lift g) f := rfl

/-- RG dual: Cartesian morphism over g ∘ f has fiber component 𝟙 = 𝟙 * 𝟙. -/
theorem π_μ_cleavage_comp_cartesian_fiber {e : SpectralBundleRG} {b₀ b₁ : RGObj}
    (f : b₀ ⟶ b₁) (g : b₁ ⟶ π_μ.obj e) :
    (π_μ_cartesianLift.cartesian_morphism (f ≫ g)).fiberMap =
      (π_μ_cartesianLift.cartesian_morphism (e := π_μ_cartesianLift.lift g) f).fiberMap *
        (π_μ_cartesianLift.cartesian_morphism g).fiberMap :=
  (Matrix.one_mul 1).symm

/-! =========================================================
    Section 6.6: Fiber Categories ≅ Spec (Note Prop 2.3, Prop 3.1)
   ========================================================= -/

/-- Morphisms in the Spec fiber category at T (spectral transformations
    intertwining the matrices). -/
@[ext]
structure SpecFiberTempHom {T : TempObj} (X Y : SpecFiberTemp T) where
  mat : Matrix (Fin X.n) (Fin Y.n) ℂ
  commut : mat * Y.A = X.A * mat

instance specFiberTempCategory (T : TempObj) : Category (SpecFiberTemp T) where
  Hom X Y := SpecFiberTempHom X Y
  id X := ⟨1, by simp⟩
  comp f g := ⟨f.mat * g.mat, by
    calc (f.mat * g.mat) * Z.A = f.mat * (g.mat * Z.A) := Matrix.mul_assoc _ _ _
      _ = f.mat * (Y.A * g.mat) := by rw [g.commut]
      _ = (f.mat * Y.A) * g.mat := (Matrix.mul_assoc _ _ _).symm
      _ = (X.A * f.mat) * g.mat := by rw [f.commut]
      _ = X.A * (f.mat * g.mat) := Matrix.mul_assoc _ _ _⟩
  id_comp := by intro X Y f; ext; exact Matrix.one_mul _
  comp_id := by intro X Y f; ext; exact Matrix.mul_one _
  assoc := by intro W X Y Z f g h; ext; exact Matrix.mul_assoc _ _ _

/-- Morphisms in the Spec fiber category at μ (RG dual). -/
@[ext]
structure SpecFiberRGHom {μ : RGObj} (X Y : SpecFiberRG μ) where
  mat : Matrix (Fin X.n) (Fin Y.n) ℂ
  commut : mat * Y.A = X.A * mat

instance specFiberRGCateogry (μ : RGObj) : Category (SpecFiberRG μ) where
  Hom X Y := SpecFiberRGHom X Y
  id X := ⟨1, by simp⟩
  comp f g := ⟨f.mat * g.mat, by
    calc (f.mat * g.mat) * Z.A = f.mat * (g.mat * Z.A) := Matrix.mul_assoc _ _ _
      _ = f.mat * (Y.A * g.mat) := by rw [g.commut]
      _ = (f.mat * Y.A) * g.mat := (Matrix.mul_assoc _ _ _).symm
      _ = (X.A * f.mat) * g.mat := by rw [f.commut]
      _ = X.A * (f.mat * g.mat) := Matrix.mul_assoc _ _ _⟩
  id_comp := by intro X Y f; ext; exact Matrix.one_mul _
  comp_id := by intro X Y f; ext; exact Matrix.mul_one _
  assoc := by intro W X Y Z f g h; ext; exact Matrix.mul_assoc _ _ _

/-- The fiber of Bun(Temp, Spec) over T: bundle objects based at T. -/
def FiberAtTemp (T : TempObj) := { X : SpectralBundleTemp // X.base = T }

/-- Vertical morphisms in the fiber over T. -/
@[ext]
structure FiberAtTempHom {T : TempObj} (X Y : FiberAtTemp T) where
  fiberMap : Matrix (Fin X.1.fiberData.n) (Fin Y.1.fiberData.n) ℂ
  commut : fiberMap * Y.1.fiberData.A = X.1.fiberData.A * fiberMap

instance fiberAtTempCategory (T : TempObj) : Category (FiberAtTemp T) where
  Hom X Y := FiberAtTempHom X Y
  id X := ⟨1, by simp⟩
  comp f g := ⟨f.fiberMap * g.fiberMap, by
    calc (f.fiberMap * g.fiberMap) * Z.1.fiberData.A
          = f.fiberMap * (g.fiberMap * Z.1.fiberData.A) := Matrix.mul_assoc _ _ _
      _ = f.fiberMap * (Y.1.fiberData.A * g.fiberMap) := by rw [g.commut]
      _ = (f.fiberMap * Y.1.fiberData.A) * g.fiberMap := (Matrix.mul_assoc _ _ _).symm
      _ = (X.1.fiberData.A * f.fiberMap) * g.fiberMap := by rw [f.commut]
      _ = X.1.fiberData.A * (f.fiberMap * g.fiberMap) := Matrix.mul_assoc _ _ _⟩
  id_comp := by intro X Y f; ext; exact Matrix.one_mul _
  comp_id := by intro X Y f; ext; exact Matrix.mul_one _
  assoc := by intro W X Y Z f g h; ext; exact Matrix.mul_assoc _ _ _

/-- The fiber of Bun(RG, Spec) over μ. -/
def FiberAtRG (μ : RGObj) := { X : SpectralBundleRG // X.base = μ }

/-- Vertical morphisms in the fiber over μ. -/
@[ext]
structure FiberAtRGHom {μ : RGObj} (X Y : FiberAtRG μ) where
  fiberMap : Matrix (Fin X.1.fiberData.n) (Fin Y.1.fiberData.n) ℂ
  commut : fiberMap * Y.1.fiberData.A = X.1.fiberData.A * fiberMap

instance fiberAtRGCategory (μ : RGObj) : Category (FiberAtRG μ) where
  Hom X Y := FiberAtRGHom X Y
  id X := ⟨1, by simp⟩
  comp f g := ⟨f.fiberMap * g.fiberMap, by
    calc (f.fiberMap * g.fiberMap) * Z.1.fiberData.A
          = f.fiberMap * (g.fiberMap * Z.1.fiberData.A) := Matrix.mul_assoc _ _ _
      _ = f.fiberMap * (Y.1.fiberData.A * g.fiberMap) := by rw [g.commut]
      _ = (f.fiberMap * Y.1.fiberData.A) * g.fiberMap := (Matrix.mul_assoc _ _ _).symm
      _ = (X.1.fiberData.A * f.fiberMap) * g.fiberMap := by rw [f.commut]
      _ = X.1.fiberData.A * (f.fiberMap * g.fiberMap) := Matrix.mul_assoc _ _ _⟩
  id_comp := by intro X Y f; ext; exact Matrix.one_mul _
  comp_id := by intro X Y f; ext; exact Matrix.mul_one _
  assoc := by intro W X Y Z f g h; ext; exact Matrix.mul_assoc _ _ _

/-- The equivalence Spec_T ≌ (fiber of Bun(Temp, Spec) over T) (Note Prop 2.3). -/
noncomputable def specFiberTempEquivFiber (T : TempObj) : SpecFiberTemp T ≌ FiberAtTemp T where
  functor :=
    { obj := fun X => ⟨⟨T, X⟩, rfl⟩
      map := fun φ => ⟨φ.mat, φ.commut⟩
      map_id := fun X => rfl
      map_comp := fun f g => rfl }
  inverse :=
    { obj := fun X => X.2 ▸ X.1.fiberData
      map := fun φ => ⟨φ.fiberMap, φ.commut⟩
      map_id := fun X => rfl
      map_comp := fun f g => rfl }
  unitIso := NatIso.ofComponents (fun X => Iso.refl _)
  counitIso := NatIso.ofComponents (fun X =>
    { hom := ⟨1, by simp⟩
      inv := ⟨1, by simp⟩ })

/-- RG dual: Spec_μ ≌ (fiber of Bun(RG, Spec) over μ) (Note Prop 3.1). -/
noncomputable def specFiberRGEquivFiber (μ : RGObj) : SpecFiberRG μ ≌ FiberAtRG μ where
  functor :=
    { obj := fun X => ⟨⟨μ, X⟩, rfl⟩
      map := fun φ => ⟨φ.mat, φ.commut⟩
      map_id := fun X => rfl
      map_comp := fun f g => rfl }
  inverse :=
    { obj := fun X => X.2 ▸ X.1.fiberData
      map := fun φ => ⟨φ.fiberMap, φ.commut⟩
      map_id := fun X => rfl
      map_comp := fun f g => rfl }
  unitIso := NatIso.ofComponents (fun X => Iso.refl _)
  counitIso := NatIso.ofComponents (fun X =>
    { hom := ⟨1, by simp⟩
      inv := ⟨1, by simp⟩ })

/-! =========================================================
    Section 7: 2-Category Structure (Strict 2-Category 2Bun)
   ========================================================= -/

/-- 1-morphism in 2Bun: a fibered functor between two fibrations. -/
structure FiberedFunctor (p : SpectralBundleTemp ⥤ TempObj) (q : SpectralBundleRG ⥤ RGObj) where
  F : SpectralBundleTemp ⥤ SpectralBundleRG
  base_map : SpectralBundleTemp → RGObj
  base_commutes : ∀ X, q.obj (F.obj X) = base_map X  -- π_μ(F(X)) = base_map(X)

/-- 2-morphism in 2Bun: a natural transformation between fibered functors. -/
structure FiberedNaturalTransformation (p : SpectralBundleTemp ⥤ TempObj) (q : SpectralBundleRG ⥤ RGObj)
    (hF : FiberedFunctor p q)
    (hG : FiberedFunctor p q) where
  base_map_eq : hF.base_map = hG.base_map
  η : hF.F ⟶ hG.F
  fiber_restricted : ∀ X,
    let base_eq : hF.base_map X = hG.base_map X := congr_fun base_map_eq X
    q.map (η.app X) = eqToHom (hF.base_commutes X) ≫ 𝟙 (hF.base_map X) ≫
      eqToHom (base_eq.trans (hG.base_commutes X).symm)

end UFPFormalization
