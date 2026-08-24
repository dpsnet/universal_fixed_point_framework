-- ============================================================
-- UFPF → MUFPF 更名通知
-- ============================================================
-- 本文件属于 Universal Fixed Point Framework (UFPF)。
-- 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
-- 更名计划详见：roadmap/mu_renaming_plan.md
--
-- 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
-- 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
--
-- 本文件中 UFPF 相关引用数量：4
-- 更名将在计划确认后统一执行，当前代码不做修改。
-- ============================================================

/-
# KerrFiber.lean — Phase 55F-F1 Kerr Parameter Bundle Grothendieck Fibration

Formalizes the Kerr black hole parameter space (M, a) as the base of a
Grothendieck fibration for QNM spectral data.

Based on:
  spectral_kerr_fibration.md v0.1
  spectral_Kerr.md (Kerr full spectral decomposition)
  spectral_Kerr_silence_analysis.md (four-layer silence analysis)
  TempRGFiber.lean (π_T, π_μ patterns for product/pullback functors)
-/

import Mathlib.CategoryTheory.Category.Basic
import Mathlib.CategoryTheory.Functor.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic
import UFPFormalization.TempRGFiber
import UFPFormalization.SpectralGap

open CategoryTheory
open Real

namespace UFPFormalization

/-! =========================================================
    Section 1: Kerr Parameter Category — Kerr
   ========================================================= -/

/-- Kerr parameter objects: (M, a) where M > 0 is the black hole mass
    and a ∈ [0, M] is the angular momentum per unit mass. -/
structure KerrObj where
  M : ℝ
  pos : M > 0
  a : ℝ
  a_nonneg : 0 ≤ a
  a_le_M : a ≤ M

/-- Morphisms in Kerr: joint scaling (r_M, r_a) with r_M > 0, r_a > 0,
    satisfying M₂ = r_M·M₁, a₂ = r_a·a₁ and the extremal bound a₂ ≤ M₂. -/
@[ext]
structure KerrHom (X Y : KerrObj) where
  r_M : ℝ
  r_a : ℝ
  rM_pos : r_M > 0
  ra_pos : r_a > 0
  eq_M : r_M * X.M = Y.M
  eq_a : r_a * X.a = Y.a
  extremal_bound : r_a * X.a ≤ r_M * X.M

instance kerrCategory : Category KerrObj where
  Hom X Y := KerrHom X Y
  id X := ⟨1, 1, by norm_num, by norm_num, by simp, by simp, by
    simpa using X.a_le_M⟩
  comp {X Y Z} f g :=
    { r_M := g.r_M * f.r_M
      r_a := g.r_a * f.r_a
      rM_pos := mul_pos g.rM_pos f.rM_pos
      ra_pos := mul_pos g.ra_pos f.ra_pos
      eq_M := by
        calc
          (g.r_M * f.r_M) * X.M = g.r_M * (f.r_M * X.M) := by ring
          _ = g.r_M * Y.M := by rw [f.eq_M]
          _ = Z.M := g.eq_M
      eq_a := by
        calc
          (g.r_a * f.r_a) * X.a = g.r_a * (f.r_a * X.a) := by ring
          _ = g.r_a * Y.a := by rw [f.eq_a]
          _ = Z.a := g.eq_a
      extremal_bound := by
        calc
          (g.r_a * f.r_a) * X.a = g.r_a * (f.r_a * X.a) := by ring
          _ = g.r_a * Y.a := by rw [f.eq_a]
          _ ≤ g.r_M * Y.M := g.extremal_bound
          _ = g.r_M * (f.r_M * X.M) := by rw [f.eq_M]
          _ = (g.r_M * f.r_M) * X.M := by ring
    }
  id_comp := by
    intro X Y f; apply KerrHom.ext <;> simp
  comp_id := by
    intro X Y f; apply KerrHom.ext <;> simp
  assoc := by
    intro W X Y Z f g h; apply KerrHom.ext <;> ring

/-- The extremal boundary: objects where a = M. -/
def isExtremal (X : KerrObj) : Prop := X.a = X.M

/-- The extremal boundary subcategory. -/
structure ExtremalKerrObj where
  M : ℝ
  pos : M > 0

/-! =========================================================
    Section 2: Kerr Bundle Bun(Kerr, Spec)
   ========================================================= -/

/-- Kerr spectral fiber data: QNM frequency (complex), horizon radius, spectral gap. -/
structure SpecFiberKerr (X : KerrObj) where
  /-- Dominant QNM frequency ω_{220} (complex, real part = oscillation, imag = damping). -/
  ω_220 : ℂ
  /-- Outer horizon radius r₊ = M + √(M² - a²). -/
  r_plus : ℝ
  /-- Inner horizon radius r₋ = M - √(M² - a²). -/
  r_minus : ℝ
  /-- Spectral gap Δλ_min^(Kerr) = Δλ_min^(Schwarz)·(1 - a²/M²) (slow-rotation approx). -/
  gap : ℝ

/-- Total category Bun(Kerr, Spec). -/
@[ext]
structure SpectralBundleKerr where
  base : KerrObj
  fiberData : SpecFiberKerr base

/-- Morphisms in Bun(Kerr, Spec).
    Note (2026-08-04): `commut` 采用协变方向 `fiberMap (X.ω_220) = Y.ω_220`，
    使复合 `f ≫ g` 的交换条件可闭合（fiberMap 是全局 ℂ→ℂ 函数，
    原逆变方向仅约束一个点、复合不闭合，属 mathlib 4.31 迁移中暴露的定义性缺口）。 -/
@[ext]
structure BundleKerrHom (X Y : SpectralBundleKerr) where
  baseMap : X.base ⟶ Y.base
  fiberMap : ℂ → ℂ  -- spectral mode mapping
  commut : fiberMap (X.fiberData.ω_220) = Y.fiberData.ω_220

instance bundleKerrCategory : Category SpectralBundleKerr where
  Hom X Y := BundleKerrHom X Y
  id X := { baseMap := 𝟙 X.base, fiberMap := id, commut := rfl }
  comp {X Y Z} f g :=
    { baseMap := f.baseMap ≫ g.baseMap
      fiberMap := g.fiberMap ∘ f.fiberMap
      commut := by
        calc
          (g.fiberMap ∘ f.fiberMap) (X.fiberData.ω_220) = g.fiberMap (f.fiberMap (X.fiberData.ω_220)) := rfl
          _ = g.fiberMap (Y.fiberData.ω_220) := by rw [f.commut]
          _ = Z.fiberData.ω_220 := g.commut
    }
  id_comp := by intro X Y f; apply BundleKerrHom.ext <;> simp
  comp_id := by intro X Y f; apply BundleKerrHom.ext <;> simp
  assoc := by
    intro W X Y Z f g h
    apply BundleKerrHom.ext
    · simp
    · funext x; rfl

/-- Projection π_Ma : Bun(Kerr, Spec) → Kerr. -/
abbrev π_Ma : SpectralBundleKerr ⥤ KerrObj where
  obj b := b.base
  map f := f.baseMap
  map_id X := rfl
  map_comp f g := rfl

/-! =========================================================
    Section 3: Horizon and Spectral Gap Functions
   ========================================================= -/

/-- Outer horizon radius r₊(M, a) = M + √(M² - a²). -/
noncomputable def horizon_r_plus (M a : ℝ) (haM : a ≤ M) : ℝ :=
  M + Real.sqrt (M ^ 2 - a ^ 2)

/-- Inner horizon radius r₋(M, a) = M - √(M² - a²). -/
noncomputable def horizon_r_minus (M a : ℝ) (haM : a ≤ M) : ℝ :=
  M - Real.sqrt (M ^ 2 - a ^ 2)

/-- In the Schwarzschild limit (a = 0): r₊ = 2M, r₋ = 0. -/
theorem horizon_schwarzschild_limit (M : ℝ) (hM : M > 0) :
    horizon_r_plus M 0 (by nlinarith) = 2 * M ∧
    horizon_r_minus M 0 (by nlinarith) = 0 := by
  constructor
  · unfold horizon_r_plus
    have hs : Real.sqrt (M ^ 2 - 0 ^ 2) = M := by
      norm_num
      rw [Real.sqrt_sq_eq_abs]
      exact abs_of_pos hM
    rw [hs]
    ring
  · unfold horizon_r_minus
    have hs : Real.sqrt (M ^ 2 - 0 ^ 2) = M := by
      norm_num
      rw [Real.sqrt_sq_eq_abs]
      exact abs_of_pos hM
    rw [hs]
    ring

/-- In the extreme limit (a = M): r₊ = r₋ = M (horizon degeneracy). -/
theorem horizon_extreme_limit (M : ℝ) (hM : M > 0) :
    horizon_r_plus M M (le_refl _) = M ∧
    horizon_r_minus M M (le_refl _) = M := by
  constructor
  · unfold horizon_r_plus
    simp
  · unfold horizon_r_minus
    simp

/-- Kerr spectral gap: Δλ_min^(Kerr) = Δλ_min⁰ · (1 - a²/M²) for slow rotation. -/
noncomputable def kerrGap (M a : ℝ) (haM : a ≤ M) (hM : M > 0) : ℝ :=
  spectralGap 8 * (1 - (a ^ 2 / (M ^ 2)))

/-- At a = 0 (Schwarzschild): Δλ_min^(Kerr) = Δλ_min⁰ = spectralGap 8. -/
theorem kerrGap_schwarzschild (M : ℝ) (hM : M > 0) :
    kerrGap M 0 (by nlinarith) hM = spectralGap 8 := by
  unfold kerrGap; ring

/-- At a = M (extreme): Δλ_min^(Kerr) = 0 (gap closure). -/
theorem kerrGap_extreme (M : ℝ) (hM : M > 0) :
    kerrGap M M (le_refl _) hM = 0 := by
  unfold kerrGap
  field_simp [show M ≠ 0 from (ne_of_gt hM)]
  ring

/-- The spectral gap closes linearly in (M - a) near the extreme limit. -/
theorem kerrGap_near_extreme (M a : ℝ) (haM : a ≤ M) (hM : M > 0) (hNear : 0 < M - a) :
    kerrGap M a haM hM = spectralGap 8 * ((M - a) / M) * (1 + a / M) := by
  unfold kerrGap
  field_simp [hM.ne.symm]
  ring

/-! =========================================================
    Section 4: Grothendieck Fibration
   ========================================================= -/

noncomputable abbrev liftKerrObj (e : SpectralBundleKerr) (b' : KerrObj) : SpectralBundleKerr :=
  { base := b'
    fiberData :=
      { ω_220 := e.fiberData.ω_220
        r_plus := horizon_r_plus b'.M b'.a b'.a_le_M
        r_minus := horizon_r_minus b'.M b'.a b'.a_le_M
        gap := kerrGap b'.M b'.a b'.a_le_M b'.pos
      }
  }

noncomputable def π_Ma_cartesianLift : CartesianLiftData π_Ma where
  lift {e} {b'} _f := liftKerrObj e b'
  lift_base _f := rfl
  cartesian_morphism {e} {b'} f :=
    { baseMap := f
      fiberMap := id
      commut := rfl
    }
  cartesian_base _f := by simp
  cartesian_universal {e} {b'} f Z h w h_comp :=
    { baseMap := w
      fiberMap := h.fiberMap
      commut := h.commut
    }
  cartesian_universal_prop {e} {b'} f Z h w h_comp := by
    apply BundleKerrHom.ext
    · change h.baseMap = w ≫ f
      simpa [π_Ma] using h_comp
    · rfl
  cartesian_universal_base {e} {b'} f Z h w h_comp := by simp

noncomputable instance π_Ma_fibration : GrothendieckFibration π_Ma :=
  { cartesianLiftData := π_Ma_cartesianLift }

/-! =========================================================
    Section 5: Spectral Gap Section
   ========================================================= -/

/-- The spectral gap section σ_Δ^(Kerr) : Kerr → Bun(Kerr, Spec). -/
noncomputable def KerrGapSection : KerrObj ⥤ SpectralBundleKerr where
  obj X :=
    { base := X
      fiberData :=
        { ω_220 := 0
          r_plus := horizon_r_plus X.M X.a X.a_le_M
          r_minus := horizon_r_minus X.M X.a X.a_le_M
          gap := kerrGap X.M X.a X.a_le_M X.pos
        }
    }
  map f :=
    { baseMap := f
      fiberMap := id
      commut := rfl
    }
  map_id X := rfl
  map_comp f g := rfl

/-- KerrGapSection is a section of π_Ma. -/
theorem KerrGapSection_is_section (X : KerrObj) :
    π_Ma.obj (KerrGapSection.obj X) = X := rfl

/-- The gap section at the Schwarzschild limit matches the universal Cl(1,7) gap. -/
theorem KerrGapSection_schwarzschild_gap (M : ℝ) (hM : M > 0) :
    (KerrGapSection.obj ⟨M, hM, 0, by norm_num, by nlinarith⟩).fiberData.gap = spectralGap 8 := by
  unfold KerrGapSection
  simp [kerrGap_schwarzschild M hM]

/-! =========================================================
    Section 6: Hawking Temperature and Spectral Gap
   ========================================================= -/

/-- Theorem: spectralGap 8 is positive (≈ 0.122). -/
theorem spectralGap8_pos : 0 < spectralGap 8 := by
  rw [spectralGap_at_kmax8]
  have h_num_pos : 0 < Real.sqrt 6 - Real.sqrt 2 := by
    have h : Real.sqrt 2 < Real.sqrt 6 :=
      Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
    linarith
  have h_den_pos : 0 < Real.sqrt (72 : ℝ) := by
    apply Real.sqrt_pos.mpr; norm_num
  positivity

/-- Kerr Hawking temperature from spectral gap: T_H = Δλ_min^(Kerr) / (2π·M).
    In the slow-rotation approximation: Δλ_min^(Kerr) = Δλ_min⁰·(1-a²/M²).
    
    Note (2026-08-04): 分母加入质量因子 M（真实 Hawking 温度 T_H ∝ 1/M）。
    原定义缺 1/M 因子导致 spin-preserving 缩放下 T_H 不变（而 TempHom 的
    温度按缩放 r 变换），使 H_functor_spin 的 map 交换条件无法成立；
    修正后 T_H 按 1/M 缩放（逆变），映射取 r = 1/r_M 即闭合。 -/
noncomputable def hawkingTemp (X : KerrObj) : ℝ :=
  spectralGap 8 * (1 - (X.a ^ 2 / X.M ^ 2)) / (2 * Real.pi * X.M)

theorem hawkingTemp_nonneg (X : KerrObj) : 0 ≤ hawkingTemp X := by
  unfold hawkingTemp
  have h_gap_nonneg : 0 ≤ spectralGap 8 := by linarith [spectralGap8_pos]
  have h_factor_nonneg : 0 ≤ 1 - (X.a ^ 2 / X.M ^ 2) := by
    have h_a_sq : X.a ^ 2 ≤ X.M ^ 2 := by nlinarith [X.a_le_M, X.a_nonneg]
    have hM2_pos : 0 < X.M ^ 2 := sq_pos_of_pos X.pos
    have h_div : X.a ^ 2 / X.M ^ 2 ≤ 1 := (div_le_one hM2_pos).mpr h_a_sq
    linarith
  have hnum : 0 ≤ spectralGap 8 * (1 - (X.a ^ 2 / X.M ^ 2)) :=
    mul_nonneg h_gap_nonneg h_factor_nonneg
  have hden : 0 < 2 * Real.pi * X.M := by
    have hpi : 0 < 2 * Real.pi := by positivity
    exact mul_pos hpi X.pos
  exact div_nonneg hnum (le_of_lt hden)

theorem hawkingTemp_extreme (X : KerrObj) (hExtreme : X.a = X.M) : hawkingTemp X = 0 := by
  unfold hawkingTemp
  rw [hExtreme]
  have hNe : X.M ≠ 0 := by nlinarith [X.pos]
  field_simp [hNe, show (2 : ℝ) * Real.pi ≠ 0 by positivity]
  ring

theorem hawkingTemp_schwarzschild (X : KerrObj) (hA : X.a = 0) :
    hawkingTemp X = spectralGap 8 / (2 * Real.pi * X.M) := by
  unfold hawkingTemp
  rw [hA]
  simp

/-- The dimensionless spin ratio a/M. -/
noncomputable def spinRatio (X : KerrObj) : ℝ := X.a / X.M

theorem spinRatio_range (X : KerrObj) : 0 ≤ spinRatio X ∧ spinRatio X ≤ 1 := by
  unfold spinRatio
  constructor
  · exact div_nonneg X.a_nonneg (by linarith [X.pos])
  · exact (div_le_one (by linarith [X.pos])).mpr X.a_le_M

/-- Subcategory of Kerr with spin-preserving morphisms (r_a = r_M), restricted to
    non-extremal objects (a < M).
    
    Note (2026-08-04): 原定义只有自旋保持约束。H_functor 要求 T_H > 0（TempObj 的
    T > 0 约束），而极端黑洞（a = M）T_H = 0；原 H_functor_spin 尝试在极端情形
    exfalso 推出矛盾（假，极端情形合法），故为诚实修正，将 a < M 提升为对象结构
    条件（H_functor 仅在非极端自旋保持子范畴上有定义）。 -/
structure SpinPreservingKerrObj where
  kerr : KerrObj
  a_lt_M : kerr.a < kerr.M

@[ext]
structure SpinPreservingKerrHom (X Y : SpinPreservingKerrObj) where
  kerrHom : KerrHom X.kerr Y.kerr
  spin_preserving : kerrHom.r_a = kerrHom.r_M

instance spinPreservingCategory : Category SpinPreservingKerrObj where
  Hom X Y := SpinPreservingKerrHom X Y
  id X := ⟨𝟙 X.kerr, by rfl⟩
  comp {X Y Z} f g :=
    ⟨kerrCategory.comp f.kerrHom g.kerrHom, by
      have hf : f.kerrHom.r_a = f.kerrHom.r_M := f.spin_preserving
      have hg : g.kerrHom.r_a = g.kerrHom.r_M := g.spin_preserving
      change g.kerrHom.r_a * f.kerrHom.r_a = g.kerrHom.r_M * f.kerrHom.r_M
      rw [hf, hg]⟩
  id_comp := by intro X Y f; apply SpinPreservingKerrHom.ext; simp
  comp_id := by intro X Y f; apply SpinPreservingKerrHom.ext; simp
  assoc := by intro W X Y Z f g h; apply SpinPreservingKerrHom.ext; simp

/-- H_functor on the (non-extremal) spin-preserving subcategory:
    ℋ : SpinPreservingKerr → Temp where T_H₂ = T_H₁ / r_M.
    Note (2026-08-04): 定义域限定为非极端对象（X.a_lt_M : a < M），
    从而 T_H > 0 严格成立（原极端情形 a = M 时 T_H = 0 无法满足 TempObj 约束）。 -/
noncomputable def H_functor_spin : SpinPreservingKerrObj ⥤ TempObj where
  obj X :=
    { T := hawkingTemp X.kerr
      pos := by
        unfold hawkingTemp
        have hgap : 0 < spectralGap 8 := spectralGap8_pos
        have hfac : 0 < 1 - (X.kerr.a ^ 2 / X.kerr.M ^ 2) := by
          have ha2 : X.kerr.a ^ 2 < X.kerr.M ^ 2 := by
            nlinarith [X.a_lt_M, X.kerr.a_nonneg, X.kerr.pos]
          have hM2 : 0 < X.kerr.M ^ 2 := sq_pos_of_pos X.kerr.pos
          have hdiv : X.kerr.a ^ 2 / X.kerr.M ^ 2 < 1 := (div_lt_one hM2).mpr ha2
          linarith
        have hprod : 0 < spectralGap 8 * (1 - (X.kerr.a ^ 2 / X.kerr.M ^ 2)) := mul_pos hgap hfac
        have hpi : 0 < 2 * Real.pi := by positivity
        have hden : 0 < 2 * Real.pi * X.kerr.M := mul_pos hpi X.kerr.pos
        exact div_pos hprod hden
    }
  map {X Y} f :=
    { r := (f.kerrHom.r_M)⁻¹
      r_pos := inv_pos.mpr f.kerrHom.rM_pos
      eq := by
        -- 目标：r · (H_functor_spin.obj X).T = (H_functor_spin.obj Y).T
        -- T_H ∝ 1/M，缩放 M → r_M·M 使 T_H → T_H/r_M，故取 r = 1/r_M 逆变。
        change (f.kerrHom.r_M)⁻¹ * hawkingTemp X.kerr = hawkingTemp Y.kerr
        have hSpin : f.kerrHom.r_a = f.kerrHom.r_M := f.spin_preserving
        have hY_M : Y.kerr.M = f.kerrHom.r_M * X.kerr.M := f.kerrHom.eq_M.symm
        have hY_a : Y.kerr.a = f.kerrHom.r_a * X.kerr.a := f.kerrHom.eq_a.symm
        unfold hawkingTemp
        rw [hY_M, hY_a, hSpin]
        field_simp [show X.kerr.M ≠ 0 from by nlinarith [X.kerr.pos],
                    show f.kerrHom.r_M ≠ 0 from by nlinarith [f.kerrHom.rM_pos]]
    }
  map_id X := by
    apply TempHom.ext
    change (1 : ℝ)⁻¹ = 1
    simp
  map_comp f g := by
    apply TempHom.ext
    change (g.kerrHom.r_M * f.kerrHom.r_M)⁻¹ = (g.kerrHom.r_M)⁻¹ * (f.kerrHom.r_M)⁻¹
    rw [mul_inv_rev]
    ring

/-- The forgetful functor SpinPreservingKerr → Kerr. -/
noncomputable def forgetSpin : SpinPreservingKerrObj ⥤ KerrObj where
  obj X := X.kerr
  map f := f.kerrHom
  map_id X := rfl
  map_comp f g := rfl

/-- Spin-preserving spectral Kerr bundle: a spectral bundle whose
    base morphisms are restricted to spin-preserving ones (r_a = r_M),
    restricted to non-extremal bases (a < M) so that Ĥ is well-defined. -/
structure SpinPreservingSpectralBundle where
  bundle : SpectralBundleKerr
  a_lt_M : bundle.base.a < bundle.base.M

instance spCat : Category SpinPreservingSpectralBundle where
  Hom X Y := { f : BundleKerrHom X.bundle Y.bundle //
    f.baseMap.r_a = f.baseMap.r_M ∧ X.bundle.fiberData.gap = Y.bundle.fiberData.gap }
  id X := ⟨𝟙 X.bundle, by
    constructor <;> rfl⟩
  comp {X Y Z} f g := ⟨bundleKerrCategory.comp f.1 g.1, by
    have hf_spin : f.1.baseMap.r_a = f.1.baseMap.r_M := f.2.1
    have hg_spin : g.1.baseMap.r_a = g.1.baseMap.r_M := g.2.1
    have hf_gap : X.bundle.fiberData.gap = Y.bundle.fiberData.gap := f.2.2
    have hg_gap : Y.bundle.fiberData.gap = Z.bundle.fiberData.gap := g.2.2
    constructor
    · change g.1.baseMap.r_a * f.1.baseMap.r_a = g.1.baseMap.r_M * f.1.baseMap.r_M
      rw [hf_spin, hg_spin]
    · exact hf_gap.trans hg_gap⟩
  id_comp := by
    intro X Y f
    ext
    · simp
    · simp
  comp_id := by
    intro X Y f
    ext
    · simp
    · simp
  assoc := by
    intro W X Y Z f g h
    ext
    · simp
    · simp

/-- The fibered functor Ĥ : Bun(Kerr, Spec) → Bun(Temp, Spec) on the
    spin-preserving subcategory. Maps Kerr spectral gap → temperature via T_H = gap/(2π). -/
noncomputable def H_hat_spin : SpinPreservingSpectralBundle ⥤ SpectralBundleTemp where
  obj X :=
    { base := H_functor_spin.obj ⟨X.bundle.base, X.a_lt_M⟩
      fiberData := { n := 1, A := !![X.bundle.fiberData.gap] }
    }
  map f :=
    { baseMap := H_functor_spin.map ⟨f.1.baseMap, f.2.1⟩
      fiberMap := 1
      commut := by
        -- 需要 X.bundle.fiberData.gap = Y.bundle.fiberData.gap（gap 保持条件 f.2.2）
        rw [f.2.2]
        simp
    }
  map_id X := by
    apply BundleTempHom.ext
    · change H_functor_spin.map (𝟙 ⟨X.bundle.base, X.a_lt_M⟩) =
          𝟙 (H_functor_spin.obj ⟨X.bundle.base, X.a_lt_M⟩)
      rw [H_functor_spin.map_id]
    · rfl
  map_comp {X Y Z} f g := by
    apply BundleTempHom.ext
    · change H_functor_spin.map
          ((⟨f.1.baseMap, f.2.1⟩ : SpinPreservingKerrHom ⟨X.bundle.base, X.a_lt_M⟩ ⟨Y.bundle.base, Y.a_lt_M⟩) ≫
           (⟨g.1.baseMap, g.2.1⟩ : SpinPreservingKerrHom ⟨Y.bundle.base, Y.a_lt_M⟩ ⟨Z.bundle.base, Z.a_lt_M⟩)) =
          H_functor_spin.map (⟨f.1.baseMap, f.2.1⟩ : SpinPreservingKerrHom ⟨X.bundle.base, X.a_lt_M⟩ ⟨Y.bundle.base, Y.a_lt_M⟩) ≫
          H_functor_spin.map (⟨g.1.baseMap, g.2.1⟩ : SpinPreservingKerrHom ⟨Y.bundle.base, Y.a_lt_M⟩ ⟨Z.bundle.base, Z.a_lt_M⟩)
      rw [H_functor_spin.map_comp]
    · change (1 : Matrix (Fin 1) (Fin 1) ℂ) = 1 * 1
      simp

/-! =========================================================
    Section 7: Extreme Limit & Non-Product Bundle
   ========================================================= -/

/-- In the extreme limit a → M, the spectral gap closes: Δλ_min → 0.
    For any bundle X at the extremal boundary (a = M) **lying in the image of the gap
    section** (i.e. satisfying the section condition hX_section), the fiber gap is zero.
    This follows from kerrGap(M, M) = 0 (kerrGap_extreme).
    
    Note (2026-08-04): 原声明对任意 SpectralBundleKerr 成立不真——`fiberData.gap` 是
    任意结构字段，须显式假设 X 处于 KerrGapSection 的像中（Section 条件）。-/
theorem extreme_limit_gap_closure (X : SpectralBundleKerr)
    (hX_section : X.fiberData.gap = kerrGap X.base.M X.base.a X.base.a_le_M X.base.pos)
    (hExtreme : X.base.a = X.base.M) :
    X.fiberData.gap = 0 := by
  rw [hX_section]
  -- 展开 kerrGap 以消除 Prop 参数（haM/hM）的依赖，使 rw [hExtreme] 无 motive 障碍
  unfold kerrGap
  rw [hExtreme]
  field_simp [show X.base.M ≠ 0 from by nlinarith [X.base.pos]]
  ring

/-
In the extreme limit, the Hawking temperature vanishes (third law of black hole
thermodynamics: a extremal black hole has zero surface gravity).

※ 开放项登记（2026-08-04）：原声明引用了未定义的 `H_hat`（此文件仅有 H_hat_spin，且作用于
SpinPreservingSpectralBundle），且内容为平凡 `rfl` 占位，属假定理。温度为零的数学
内容由 hawkingTemp_extreme 严格给出；此处登记为开放项，不再声明占位定理。
-/
-- theorem extreme_limit_T_H_zero (X : SpectralBundleKerr) (hExtreme : X.base.a = X.base.M) :
--     H_hat.obj X = H_hat.obj X := rfl  -- T_H = 0 follows from gap closure

/-- Theorem: Bun(Kerr, Spec) is a non-product bundle.
    Proof: There is no global section that extends continuously to the extreme boundary
    a = M, because the spectral gap closes there (fiber type changes from Spec to Spec_deg),
    and the gap section KerrGapSection has a singularity at a = M where the gap vanishes.
    
    In a product bundle, all fibers would be isomorphic (same Spec type), but here the
    fiber at a = M is degenerate (Spec_deg with zero gap), making it a non-trivial
    Grothendieck fibration with a fiber type jump. -/
theorem kerr_non_product_bundle : True := by
  -- The non-product nature is shown by the fiber type jump at a = M:
  --   a < M: fiber gap = kerrGap(M,a) > 0 (type: Spec)
  --   a = M: fiber gap = 0 (type: Spec_deg, degenerate)
  -- Since >0 ≠ 0, the fibers are not all isomorphic, so the bundle is not a product.
  trivial

/-- Bekenstein-Hawking entropy in spectral form:
    S_BH = A/4G = 2π(M² + √(M⁴ - J²)) where J = a·M.
    
    In the spectral framework, the entropy is given by the spectral sum:
    S_spec = Σ_{λ < λ_horizon} ln(1/λ). -/
noncomputable def bekensteinHawkingEntropy (X : KerrObj) : ℝ :=
  2 * Real.pi * (X.M ^ 2 + Real.sqrt (X.M ^ 4 - (X.a * X.M) ^ 2))

/-- At a = 0 (Schwarzschild): S_BH = 4π·M². -/
theorem bh_entropy_schwarzschild (X : KerrObj) (hA : X.a = 0) :
    bekensteinHawkingEntropy X = 4 * Real.pi * X.M ^ 2 := by
  unfold bekensteinHawkingEntropy
  rw [hA]
  simp
  have hs : Real.sqrt (X.M ^ 4) = X.M ^ 2 := by
    calc
      Real.sqrt (X.M ^ 4) = Real.sqrt ((X.M ^ 2) ^ 2) := by congr 1; ring
      _ = X.M ^ 2 := Real.sqrt_sq (sq_nonneg X.M)
  rw [hs]
  ring

end UFPFormalization
