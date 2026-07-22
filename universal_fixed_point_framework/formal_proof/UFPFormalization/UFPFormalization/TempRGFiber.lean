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
import Mathlib.CategoryTheory.Category.Kleisli
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
  comp f g := ⟨g.r * f.r, mul_pos g.r_pos f.r_pos, by
    calc
      (g.r * f.r) * X.T = g.r * (f.r * X.T) := by ring
      _ = g.r * Y.T := by rw [f.eq]
      _ = Z.T := g.eq
    ⟩
  id_comp := by
    intro X Y f; ext; simp; ring
  comp_id := by
    intro X Y f; ext; simp; ring
  assoc := by
    intro W X Y Z f g h
    ext; ring

instance rgCategory : Category RGObj where
  Hom X Y := RGHom X Y
  id X := ⟨1, by linarith, by simp⟩
  comp f g := ⟨g.s * f.s, mul_pos g.s_pos f.s_pos, by
    calc
      (g.s * f.s) * X.μ = g.s * (f.s * X.μ) := by ring
      _ = g.s * Y.μ := by rw [f.eq]
      _ = Z.μ := g.eq
    ⟩
  id_comp := by
    intro X Y f; ext; simp; ring
  comp_id := by
    intro X Y f; ext; simp; ring
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

/-- Unit of the isomorphism: 𝒯⁻¹∘𝒯 ≅ id_Temp. -/
noncomputable def TUnitIso : 𝟭 TempObj ≅ TFunctor ⋙ TInvFunctor where
  hom := { app := λ X => ⟨1, by norm_num, by simp⟩ }
  inv := { app := λ X => ⟨1, by norm_num, by simp⟩ }

/-- Counit of the isomorphism: 𝒯∘𝒯⁻¹ ≅ id_RG. -/
noncomputable def TCounitIso : TFunctor ⋙ TInvFunctor ≅ 𝟭 TempObj :=
  (NatIso.ofComponents fun X =>
    { hom := ⟨1, by norm_num, by simp⟩
      inv := ⟨1, by norm_num, by simp⟩ })

/-- The adjoint equivalence 𝒯 ⊣ 𝒯⁻¹ (they are actually inverses). -/
noncomputable def TAdjEquiv : TFunctor ⊣ TInvFunctor :=
  Adjunction.mkOfUnitCounit
    { unit := TUnitIso.hom
      counit := TCounitIso.hom
      left_triangle := by
        ext X; dsimp [TUnitIso, TCounitIso]; simp
      right_triangle := by
        ext X; dsimp [TUnitIso, TCounitIso]; simp }

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
structure SpectralBundleTemp where
  base : TempObj
  fiberData : SpecFiberTemp base

/-- Total category Bun(RG, Spec): pairs (μ, spectral data over μ). -/
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
  comp f g :=
    { baseMap := f.baseMap ≫ g.baseMap
      fiberMap := f.fiberMap * g.fiberMap
      commut := by
        calc
          (f.fiberMap * g.fiberMap) * Z.fiberData.A
              = f.fiberMap * (g.fiberMap * Z.fiberData.A) := by ring
          _ = f.fiberMap * (Y.fiberData.A * g.fiberMap) := by rw [g.commut]
          _ = (f.fiberMap * Y.fiberData.A) * g.fiberMap := by ring
          _ = (X.fiberData.A * f.fiberMap) * g.fiberMap := by rw [f.commut]
          _ = X.fiberData.A * (f.fiberMap * g.fiberMap) := by ring
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
    · ring

instance bundleRGategory : Category SpectralBundleRG where
  Hom X Y := BundleRGHom X Y
  id X :=
    { baseMap := 𝟙 X.base
      fiberMap := 1
      commut := by simp }
  comp f g :=
    { baseMap := f.baseMap ≫ g.baseMap
      fiberMap := f.fiberMap * g.fiberMap
      commut := by
        calc
          (f.fiberMap * g.fiberMap) * Z.fiberData.A = f.fiberMap * (g.fiberMap * Z.fiberData.A) := by ring
          _ = f.fiberMap * (Y.fiberData.A * g.fiberMap) := by rw [g.commut]
          _ = (f.fiberMap * Y.fiberData.A) * g.fiberMap := by ring
          _ = (X.fiberData.A * f.fiberMap) * g.fiberMap := by rw [f.commut]
          _ = X.fiberData.A * (f.fiberMap * g.fiberMap) := by ring
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
    · ring

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
noncomputable def π_T : SpectralBundleTemp ⥤ TempObj where
  obj b := b.base
  map f := f.baseMap
  map_id X := rfl
  map_comp f g := rfl

/-- Projection π_μ : Bun(RG, Spec) → RGCat. -/
noncomputable def π_μ : SpectralBundleRG ⥤ RGObj where
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
    p.map (cartesian_morphism f) = f
  cartesian_universal {e : E} {b' : B} (f : b' ⟶ p.obj e) (Z : E) (h : Z ⟶ e)
    (w : p.obj Z ⟶ b') (h_comp : p.map h = f ≫ w) : Z ⟶ lift f
  cartesian_universal_prop {e : E} {b' : B} (f : b' ⟶ p.obj e) (Z : E) (h : Z ⟶ e)
    (w : p.obj Z ⟶ b') (h_comp : p.map h = f ≫ w) :
    h = cartesian_morphism f ≫ cartesian_universal f Z h w h_comp
  cartesian_universal_base {e : E} {b' : B} (f : b' ⟶ p.obj e) (Z : E) (h : Z ⟶ e)
    (w : p.obj Z ⟶ b') (h_comp : p.map h = f ≫ w) :
    p.map (cartesian_universal f Z h w h_comp) = w

/-- A Grothendieck fibration is a functor equipped with Cartesian lift data. -/
structure GrothendieckFibration (E B : Type u) [Category E] [Category B] (p : E ⥤ B) where
  cartesianLiftData : CartesianLiftData p

/-- π_T admits a Grothendieck fibration structure.
    Given a target (T₂, {λ_i}) and a base map f : T₁ → T₂, we construct the
    lift (T₁, f*{λ_i}) where f*{λ_i} is the spectral data pulled back through
    the spectral flow map. -/
noncomputable def π_T_cartesianLift : CartesianLiftData π_T where
  lift {e} {b'} f :=
    { base := b'
      fiberData :=
        { n := e.fiberData.n
          A := e.fiberData.A  -- In this finite prototype, spectral flow
                              -- preserves the matrix A under temperature
                              -- dilation (identity pullback)
        }
    }
  lift_base f := rfl
  cartesian_morphism {e} {b'} f :=
    { baseMap := f
      fiberMap := 1
      commut := by simp
    }
  cartesian_base f := rfl
  cartesian_universal {e} {b'} f Z h w h_comp :=
    { baseMap := w
      fiberMap := h.fiberMap
      commut := h.commut
    }
  cartesian_universal_prop {e} {b'} f Z h w h_comp := by
    apply BundleTempHom.ext
    · -- base component: h.baseMap = (fiberMap f, which is 1) ≫ w
      -- but we need h.baseMap = f ≫ w, which is given by h_comp
      -- Actually h_comp says π_T.map h = f ≫ w
      -- i.e., h.baseMap = f ≫ w
      -- And cartesian_morphism f has baseMap = f
      -- universal has baseMap = w
      -- So cartesian_morphism f ≫ universal = (f, 1) ≫ (w, h.fiberMap)
      -- The base comp: f ≫ w = h.baseMap  (by h_comp)
      -- We use h_comp directly
      have h_base := congrArg id h_comp
      -- h_comp is: p.map h = f ≫ w  which means h.baseMap = f ≫ w
      -- But we can't infer this equation directly
      -- Let's rewrite: h_comp says π_T.map h = f ≫ w
      -- π_T.map h = h.baseMap by definition of π_T
      -- So h_comp gives: h.baseMap = f ≫ w
      simpa using h_comp
    · -- fiber component
      simp
  cartesian_universal_base {e} {b'} f Z h w h_comp := rfl

noncomputable def π_T_fibration : GrothendieckFibration π_T :=
  { cartesianLiftData := π_T_cartesianLift }

/-- π_μ admits a Grothendieck fibration structure, dual to π_T. -/
noncomputable def π_μ_cartesianLift : CartesianLiftData π_μ where
  lift {e} {b'} f :=
    { base := b'
      fiberData :=
        { n := e.fiberData.n
          A := e.fiberData.A
        }
    }
  lift_base f := rfl
  cartesian_morphism {e} {b'} f :=
    { baseMap := f
      fiberMap := 1
      commut := by simp
    }
  cartesian_base f := rfl
  cartesian_universal {e} {b'} f Z h w h_comp :=
    { baseMap := w
      fiberMap := h.fiberMap
      commut := h.commut
    }
  cartesian_universal_prop {e} {b'} f Z h w h_comp := by
    apply BundleRGHom.ext
    · simpa using h_comp
    · simp
  cartesian_universal_base {e} {b'} f Z h w h_comp := rfl

noncomputable def π_μ_fibration : GrothendieckFibration π_μ :=
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
    · simp
    · simp
  map_comp f g := by
    apply BundleRGHom.ext
    · simp
    · simp

/-- T̂_Riem is base-faithful: the induced base map equals TFunctor applied to base. -/
theorem T_hat_Riem_base_commutes (X : SpectralBundleTemp) :
    π_μ.obj (T_hat_Riem.obj X) = TFunctor.obj (π_T.obj X) := rfl

theorem T_hat_Riem_map_base_commutes {X Y : SpectralBundleTemp} (f : X ⟶ Y) :
    π_μ.map (T_hat_Riem.map f) = TFunctor.map (π_T.map f) := rfl

/-- T̂_Riem preserves Cartesian morphisms.
    In this finite prototype, Cartesian lifts are mapped to Cartesian lifts
    because the spectral flow is identity on the fibers. -/
theorem T_hat_Riem_preserves_cartesian {e : SpectralBundleTemp} {b' : TempObj}
    (f : b' ⟶ π_T.obj e) :
    T_hat_Riem.map (π_T_cartesianLift.cartesian_morphism f) =
    π_μ_cartesianLift.cartesian_morphism (TFunctor.map f) := by
  apply BundleRGHom.ext
  · simp
  · simp

/-! =========================================================
    Section 7: 2-Category Structure (Strict 2-Category 2Bun)
   ========================================================= -/

/-- 1-morphism in 2Bun: a fibered functor between two fibrations. -/
structure FiberedFunctor (p : SpectralBundleTemp ⥤ TempObj) (q : SpectralBundleRG ⥤ RGObj)
    [GrothendieckFibration p] [GrothendieckFibration q] where
  F : SpectralBundleTemp ⥤ SpectralBundleRG
  base_map : SpectralBundleTemp → RGObj
  base_commutes : ∀ X, q.obj (F.obj X) = base_map X  -- π_μ(F(X)) = base_map(X)

/-- 2-morphism in 2Bun: a natural transformation between fibered functors. -/
structure FiberedNaturalTransformation (p q : SpectralBundleTemp ⥤ TempObj)
    (F G : SpectralBundleTemp ⥤ SpectralBundleRG)
    [GrothendieckFibration p] [GrothendieckFibration q]
    (hF : FiberedFunctor p q)
    (hG : FiberedFunctor p q) where
  η : F ⟶ G
  fiber_restricted : ∀ X, π_μ.map (η.app X) = 𝟙 (hF.base_map X)

end UFPFormalization
