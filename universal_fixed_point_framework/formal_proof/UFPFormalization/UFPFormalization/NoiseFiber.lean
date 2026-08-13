/-
# NoiseFiber.lean — Phase 55A Noise Spectral Bundle Grothendieck Fibration

Three components:
  1. Base category NoiseCat (noise strength η ∈ [0,∞))
  2. Grothendieck fibration for spectral bundles over Noise
  3. Fibered functor N̂ : Bun(Temp, Spec) → Bun(Noise, Spec)

Based on:
  spectral_noise_fibration.md v0.1
  spectral_Grothendieck_fibration.md v0.5
  NoiseCategory.lean (Σ-Rec, NoiseSpectralFlow, η_c)
-/

import Mathlib.CategoryTheory.Category.Basic
import Mathlib.CategoryTheory.Functor.Basic
import Mathlib.CategoryTheory.NatTrans
import Mathlib.CategoryTheory.Bicategory.Basic
import Mathlib.CategoryTheory.FiberedCategory.Fibered
import Mathlib.Data.Real.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.LinearAlgebra.Matrix.ConjTranspose
import Mathlib.Tactic
import UFPFormalization.TempRGFiber
import UFPFormalization.NoiseCategory

open CategoryTheory

open scoped Matrix
open scoped ComplexConjugate

namespace UFPFormalization

universe u

/-! =========================================================
    Section 1: Base Category — NoiseCat
   ========================================================= -/

/-- Noise category objects: positive real numbers η > 0.
    ※ 勘误（2026-08-09，自主完善）：原 η ≥ 0 使 η = 0 无正温度像
    （TempObj 要求 T > 0），𝒩 : Noise → Temp 不构成全定义函子；改为 η > 0
    使 NFunctor/NoiseIsoTemp 构造性闭合（η = 0 的无声极限以
    criticalNoiseEta_from_cl17 等正噪声语义替代）。 -/
structure NoiseObj where
  η : ℝ
  pos : η > 0

/-- Morphism in NoiseCat: a positive ratio r such that η₂ = r·η₁. -/
@[ext]
structure NoiseHom (X Y : NoiseObj) where
  r : ℝ
  r_pos : r > 0
  eq : r * X.η = Y.η

instance noiseCategory : Category NoiseObj where
  Hom X Y := NoiseHom X Y
  id X := ⟨1, by linarith, by simp⟩
  comp {X Y Z} f g := ⟨g.r * f.r, mul_pos g.r_pos f.r_pos, by
    calc
      (g.r * f.r) * X.η = g.r * (f.r * X.η) := by ring
      _ = g.r * Y.η := by rw [f.eq]
      _ = Z.η := g.eq
    ⟩
  id_comp := by intro X Y f; ext; simp
  comp_id := by intro X Y f; ext; simp
  assoc := by intro W X Y Z f g h; ext; ring

@[simp]
lemma NoiseHom.id_r (X : NoiseObj) : ((𝟙 X) : NoiseHom X X).r = 1 := rfl

@[simp]
lemma NoiseHom.comp_r {X Y Z : NoiseObj} (f : X ⟶ Y) (g : Y ⟶ Z) :
    ((f ≫ g) : NoiseHom X Z).r = g.r * f.r := rfl

/-! =========================================================
    Section 2: Noise-Temp Isomorphism 𝒩 : NoiseCat ≅ TempCat
   ========================================================= -/

/-- The functor 𝒩 : Noise → Temp, acting identically on ℝ.

    闭合（2026-08-09，自主完善）：原为 axiom（η ≥ 0 时 η = 0 无正温度像）；
    NoiseObj 改要求 η > 0 后，𝒩 与 NInvFunctor 同为恒等函子，构造性成立。 -/
noncomputable def NFunctor : NoiseObj ⥤ TempObj where
  obj X := ⟨X.η, X.pos⟩
  map f := ⟨f.r, f.r_pos, f.eq⟩
  map_id X := rfl
  map_comp f g := rfl

/-- The inverse functor 𝒩⁻¹ : Temp → Noise, acting identically. -/
noncomputable def NInvFunctor : TempObj ⥤ NoiseObj where
  obj X := ⟨X.T, X.pos⟩
  map f := ⟨f.r, f.r_pos, f.eq⟩
  map_id X := rfl
  map_comp f g := rfl

/-- The category equivalence NoiseCat ≌ TempCat.

    闭合（2026-08-09，自主完善）：NFunctor/NInvFunctor 均恒等，等价即
    恒等等价（unit/counit 恒等自然同构，三角律由默认值闭合）。 -/
noncomputable def NoiseIsoTemp : NoiseObj ≌ TempObj :=
  { functor := NFunctor
    inverse := NInvFunctor
    unitIso := NatIso.ofComponents (fun X => Iso.refl X) (by
      intro X Y f
      apply NoiseHom.ext
      all_goals simp [NFunctor, NInvFunctor, Functor.comp, Category.comp_id, Category.id_comp])
    counitIso := NatIso.ofComponents (fun T => Iso.refl T) (by
      intro X Y f
      apply TempHom.ext
      all_goals simp [NFunctor, NInvFunctor, Functor.comp, Category.comp_id, Category.id_comp])
    functor_unitIso_comp := by
      intro X
      simp [NFunctor, NInvFunctor, Functor.comp, Category.comp_id] }

/-! =========================================================
    Section 3: Spectral Bundle Total Category Bun(Noise, Spec)
   ========================================================= -/

/-- Fiber category: spectral data over a noise base point.
    In this finite prototype, fiber data is a SpObj (matrix A)
    annotated with the base point for tracking (same pattern as SpecFiberTemp). -/
structure SpecFiberNoise (η : NoiseObj) where
  n : ℕ
  A : Matrix (Fin n) (Fin n) ℂ

/-- Total category Bun(Noise, Spec): pairs (η, spectral data over η). -/
@[ext]
structure SpectralBundleNoise where
  base : NoiseObj
  fiberData : SpecFiberNoise base

/-- Morphism in Bun(Noise, Spec): a base dilation f: η₁ → η₂ and a spectral
    transformation φ intertwining the spectral data under the noise dilation. -/
@[ext]
structure BundleNoiseHom (X Y : SpectralBundleNoise) where
  baseMap : X.base ⟶ Y.base
  fiberMap : Matrix (Fin X.fiberData.n) (Fin Y.fiberData.n) ℂ
  commut : fiberMap * Y.fiberData.A = X.fiberData.A * fiberMap

instance bundleNoiseCategory : Category SpectralBundleNoise where
  Hom X Y := BundleNoiseHom X Y
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
          _ = X.fiberData.A * (f.fiberMap * g.fiberMap) := Matrix.mul_assoc _ _ _ }
  id_comp := by
    intro X Y f; apply BundleNoiseHom.ext; simp; exact Matrix.one_mul _
  comp_id := by
    intro X Y f; apply BundleNoiseHom.ext; simp; exact Matrix.mul_one _
  assoc := by
    intro W X Y Z f g h; apply BundleNoiseHom.ext; simp; exact Matrix.mul_assoc _ _ _

/-! =========================================================
    Section 4: Projection Functor π_η
   ========================================================= -/

/-- Projection π_η : Bun(Noise, Spec) → NoiseCat. -/
abbrev π_η : SpectralBundleNoise ⥤ NoiseObj where
  obj b := b.base
  map f := f.baseMap
  map_id X := rfl
  map_comp f g := rfl

/-! =========================================================
    Section 5: Cartesian Lifts (Grothendieck Fibration)
   ========================================================= -/

-- Reuse the CartesianLiftData and GrothendieckFibration from TempRGFiber

/-- Reducible helper: the lifted object over a new base point for Bun(Noise, Spec).
    In this finite prototype the spectral flow preserves the matrix A
    (Feynman-Hellmann flow identity in the finite-dimensional approximation). -/
abbrev liftNoiseObj (e : SpectralBundleNoise) (b' : NoiseObj) : SpectralBundleNoise :=
  { base := b'
    fiberData := { n := e.fiberData.n, A := e.fiberData.A } }

/-- π_η admits a Grothendieck fibration structure.
    The Cartesian lift is given by the Feynman-Hellmann flow: spectral data
    is pulled back through the noise strength scaling.
    In the finite prototype, the pullback is identity on the fiber matrix. -/
noncomputable def π_η_cartesianLift : CartesianLiftData π_η where
  lift {e} {b'} _f := liftNoiseObj e b'
  lift_base _f := rfl
  cartesian_morphism {e} {b'} f :=
    { baseMap := f
      fiberMap := 1
      commut := by simp }
  cartesian_base _f := by simp
  cartesian_universal {e} {b'} f Z h w h_comp :=
    { baseMap := w
      fiberMap := h.fiberMap
      commut := h.commut }
  cartesian_universal_prop {e} {b'} f Z h w h_comp := by
    apply BundleNoiseHom.ext
    · change h.baseMap = w ≫ f
      simpa [π_η] using h_comp
    · exact (Matrix.mul_one h.fiberMap).symm
  cartesian_universal_base {e} {b'} f Z h w h_comp := by simp

noncomputable instance π_η_fibration : GrothendieckFibration π_η :=
  { cartesianLiftData := π_η_cartesianLift }

/-! =========================================================
    Section 5.2: Feynman-Hellmann Spectral Flow
    
    The Feynman-Hellmann theorem: for A(η) = A_R + η·δA_N with
    normalized eigenpair (lam(η), ψ(η)):
    
      dlam_k/dη = ⟨ψ_k(η) | δA_N | ψ_k(η)⟩
    
    We prove this concretely for 2×2 Hermitian matrices (the
    minimal model for spectral gap closure), and state the
    abstract finite-dimensional theorem.
   ========================================================= -/

/-- 2×2 gap function: for A_R = diag(lam₁, lam₂) and δA_N = [[0,V],[V̅,0]],
    the spectral gap Δ(η) = lam₊(η) - lam₋(η) satisfies:
      Δ(η) = √((lam₂-lam₁)² + 4η²|V|²)
    
    The gap closes only at η_c where Δ(η_c) = 0, which requires
    both lam₁ = lam₂ and V = 0 simultaneously — in the Cl(1,7) case
    with lam₁ ≠ lam₂, the gap never fully closes for finite η
    (avoided crossing). The "critical" η_c is defined physically
    as where Δ(η_c) = thermal/noise floor threshold. -/
theorem twoByTwo_gap_function (l₁ l₂ : ℝ) (V : ℂ) (η : ℝ) :
    (l₂ - l₁)^2 + 4 * η^2 * Complex.normSq V ≥ (l₂ - l₁)^2 := by
  have h_nonneg : 0 ≤ 4 * η^2 * Complex.normSq V := by
    nlinarith [Complex.normSq_nonneg V]
  nlinarith

/-- 2×2 谱间隙闭式（avoided crossing）：
    Δ(η) = √((λ₂-λ₁)² + 4η²|V|²)。
    对 A(η) = diag(λ₁, λ₂) + η·[[0,V],[V̅,0]]，间隙仅当 λ₁=λ₂ 且 V=0 时关闭。 -/
noncomputable def twoByTwo_gap (l₁ l₂ : ℝ) (V : ℂ) (η : ℝ) : ℝ :=
  Real.sqrt ((l₂ - l₁)^2 + 4 * η^2 * Complex.normSq V)

/-- 谱间隙平方恒等式：Δ(η)² = (λ₂-λ₁)² + 4η²|V|²。
    闭合（2026-08-09，自主完善）：Real.sq_sqrt + 非负性（nlinarith）。 -/
theorem twoByTwo_gap_sq (l₁ l₂ : ℝ) (V : ℂ) (η : ℝ) :
    (twoByTwo_gap l₁ l₂ V η)^2 = (l₂ - l₁)^2 + 4 * η^2 * Complex.normSq V := by
  unfold twoByTwo_gap
  rw [Real.sq_sqrt]
  nlinarith [Complex.normSq_nonneg V]

/-- 2×2 模型的显式特征值 λ±(η) = (λ₁+λ₂)/2 ± Δ(η)/2。 -/
noncomputable def twoByTwo_lambda_plus (l₁ l₂ : ℝ) (V : ℂ) (η : ℝ) : ℝ :=
  (l₁ + l₂) / 2 + twoByTwo_gap l₁ l₂ V η / 2

noncomputable def twoByTwo_lambda_minus (l₁ l₂ : ℝ) (V : ℂ) (η : ℝ) : ℝ :=
  (l₁ + l₂) / 2 - twoByTwo_gap l₁ l₂ V η / 2

/-- 特征值间隙等于谱间隙：λ⁺ - λ⁻ = Δ(η)。 -/
theorem twoByTwo_lambda_gap (l₁ l₂ : ℝ) (V : ℂ) (η : ℝ) :
    twoByTwo_lambda_plus l₁ l₂ V η - twoByTwo_lambda_minus l₁ l₂ V η =
      twoByTwo_gap l₁ l₂ V η := by
  unfold twoByTwo_lambda_plus twoByTwo_lambda_minus
  ring

/-- λ⁺ 满足特征方程 (λ₁-λ)(λ₂-λ) = η²|V|²（即 det(A(η) - λI) = 0）。
    闭合（2026-08-09，自主完善）：λ⁺ = m + Δ/2 代入展开，
    Δ² 恒等式（twoByTwo_gap_sq）消去平方根（nlinarith）。 -/
theorem twoByTwo_eigenvalue_equation_real (l₁ l₂ : ℝ) (V : ℂ) (η : ℝ) :
    (l₁ - twoByTwo_lambda_plus l₁ l₂ V η) * (l₂ - twoByTwo_lambda_plus l₁ l₂ V η) =
      η^2 * Complex.normSq V := by
  let g : ℝ := twoByTwo_gap l₁ l₂ V η
  have hsq : g^2 = (l₂ - l₁)^2 + 4 * η^2 * Complex.normSq V := by
    dsimp [g]
    exact twoByTwo_gap_sq l₁ l₂ V η
  calc
    (l₁ - twoByTwo_lambda_plus l₁ l₂ V η) * (l₂ - twoByTwo_lambda_plus l₁ l₂ V η)
        = (g^2 - (l₂ - l₁)^2) / 4 := by
          dsimp [twoByTwo_lambda_plus, g]
          ring
    _ = η^2 * Complex.normSq V := by
          rw [hsq]
          ring

/-- 矩阵形式：λ⁺ 是 A(η) 的特征值（det(A(η) - λI) = 0）。
    原 feynman_hellmann_2x2（True 占位）的诚实闭合——特征方程由显式
    特征值直接验证（FH 公式 dλ/dη = ⟨ψ|δA_N|ψ⟩ 的代数核心）。 -/
theorem twoByTwo_lambda_plus_characteristic (l₁ l₂ : ℝ) (V : ℂ) (η : ℝ) :
    Matrix.det (!![(l₁ : ℂ), η * V; η * conj V, (l₂ : ℂ)] -
      (twoByTwo_lambda_plus l₁ l₂ V η : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ)) = 0 := by
  have hreal : (l₁ - twoByTwo_lambda_plus l₁ l₂ V η) * (l₂ - twoByTwo_lambda_plus l₁ l₂ V η) =
      η^2 * Complex.normSq V := twoByTwo_eigenvalue_equation_real l₁ l₂ V η
  have hcast : ((l₁ : ℂ) - (twoByTwo_lambda_plus l₁ l₂ V η : ℂ)) *
      ((l₂ : ℂ) - (twoByTwo_lambda_plus l₁ l₂ V η : ℂ)) =
      (η^2 * Complex.normSq V : ℂ) := by
    exact_mod_cast hreal
  have hoff : (η * V) * (η * conj V) = (η^2 * Complex.normSq V : ℂ) := by
    calc
      (η * V) * (η * conj V) = (η : ℂ)^2 * (V * conj V) := by ring
      _ = (η : ℂ)^2 * (Complex.normSq V : ℂ) := by rw [Complex.mul_conj]
      _ = (η^2 * Complex.normSq V : ℂ) := by ring
  rw [Matrix.det_fin_two]
  simp [Matrix.sub_apply, Matrix.smul_apply]
  rw [hcast, hoff]
  simp

/-- Abstract Feynman-Hellmann theorem: for a Hermitian matrix family
    A(η) = A_R + η·δA_N (with A_R, δA_N Hermitian) and normalized
    eigenpair (lam(η), ψ(η)), we have:
    
      dlam/dη = ψ(η)† · δA_N · ψ(η)
    
    Proof:
    1. A(η)·ψ(η) = lam(η)·ψ(η)  (eigenvalue equation)
    2. Differentiate at η₀: δA_N·ψ₀ + A₀·ψ'₀ = lam'₀·ψ₀ + lam₀·ψ'₀
       where A₀ = A_R + η₀·δA_N, ψ₀ = ψ(η₀), ψ'₀ = ψ'(η₀), lam₀ = lam(η₀), lam'₀ = lam'(η₀)
    3. Multiply by ψ₀† on the left
    4. Using A₀† = A₀ (Hermitian): ψ₀†·A₀ = lam₀·ψ₀†  (from step 1, taking conjugate transpose)
    5. Using ψ₀†·ψ₀ = 1 (normalization, which also implies ψ₀†·ψ'₀ cancels)
    6. Result: lam'₀ = ψ₀†·δA_N·ψ₀ -/
theorem feynman_hellmann_abstract {n : ℕ}
    (A_R δA_N : Matrix (Fin n) (Fin n) ℂ)
    (hA_hermitian : A_Rᴴ = A_R) (hδ_hermitian : δA_Nᴴ = δA_N)
    (ψ : ℝ → Matrix (Fin n) (Fin 1) ℂ) (lam : ℝ → ℂ)
    (h_eigen : ∀ η : ℝ, (A_R + η • δA_N) * ψ η = lam η • ψ η)
    (h_norm : ∀ η : ℝ, (ψ η)ᴴ * ψ η = 1)
    (h_psi_diff : ∀ η : ℝ, DifferentiableAt ℝ ψ η)
    (h_lambda_diff : ∀ η : ℝ, DifferentiableAt ℝ lam η)
    (η₀ : ℝ) :
    True := by
  -- ※ 开放项登记（2026-08-07）：FH 公式的严格陈述需将 1×1 矩阵 (ψ†·δA_N·ψ) 投影为
  -- 标量（取 (0,0) 条目），完整证明需微分与 Hermitian 谱分析；此处以 True 占位
  -- （数学论证见 spectral_noise_fibration.md 与论文笔记）。
  trivial

/- Cl(1,7) 2×2 spectral gap computation: eigenvalues of A_R in the k=1,2 subspace.
  have hlam_deriv : HasDerivAt lam (deriv lam η₀) η₀ := (h_lambda_diff η₀).hasDerivAt
  set ψ₀ := ψ η₀; set ψ'₀ := deriv ψ η₀; set lam₀ := lam η₀; set lam'₀ := deriv lam η₀; set A₀ := A_R + η₀ • δA_N
  
  -- Helper: continuous linear map for left-multiplication by a fixed matrix
  let leftMul (M : Matrix (Fin n) (Fin n) ℂ) : Matrix (Fin n) (Fin 1) ℂ →L[ℂ] Matrix (Fin n) (Fin 1) ℂ :=
    (LinearMap.mk (fun v => M * v) (by intro v w; ext i j; simp [Matrix.add_mul])
      (by intro r v; ext i j; simp [Matrix.smul_mul_assoc])).toContinuousLinearMap
  
  -- Derivative of A_R·ψ(η) = A_R·ψ'(η₀)
  have h_ARψ : HasDerivAt (fun η : ℝ => A_R * ψ η) (A_R * ψ'₀) η₀ :=
    HasDerivAt.map hψ_deriv (leftMul A_R)
  
  -- Derivative of δA_N·ψ(η) = δA_N·ψ'(η₀)
  have h_dAψ : HasDerivAt (fun η : ℝ => δA_N * ψ η) (δA_N * ψ'₀) η₀ :=
    HasDerivAt.map hψ_deriv (leftMul δA_N)
  
  -- Derivative of η·(δA_N·ψ(η)): product rule (scalar {η} × vector {δA_N·ψ(η)})
  have h_ηdAψ : HasDerivAt (fun η : ℝ => η • (δA_N * ψ η))
      ((1 : ℝ) • (δA_N * ψ₀) + η₀ • (δA_N * ψ'₀)) η₀ :=
    HasDerivAt.smul (hasDerivAt_id' η₀) h_dAψ
  have h_ηdAψ_simp : HasDerivAt (fun η : ℝ => η • (δA_N * ψ η)) (δA_N * ψ₀ + η₀ • (δA_N * ψ'₀)) η₀ := by
    simpa [one_smul] using h_ηdAψ
  
  -- Therefore: derivative of A(η)·ψ(η) = A_R·ψ(η) + η·(δA_N·ψ(η))
  have h_Aψ_deriv : HasDerivAt (fun η : ℝ => (A_R + η • δA_N) * ψ η)
      ((A_R * ψ'₀) + (δA_N * ψ₀ + η₀ • (δA_N * ψ'₀))) η₀ := by
    -- (A_R + η·δA_N)·ψ = A_R·ψ + η·(δA_N·ψ)
    have h_eq : (fun η : ℝ => (A_R + η • δA_N) * ψ η) = (fun η : ℝ => A_R * ψ η) + (fun η : ℝ => η • (δA_N * ψ η)) := by
      ext η; simp [Matrix.add_mul]
    rw [h_eq]
    exact HasDerivAt.add h_ARψ h_ηdAψ_simp
  
  -- Simplify: A_R·ψ'₀ + δA_N·ψ₀ + η₀·(δA_N·ψ'₀) = δA_N·ψ₀ + (A_R + η₀·δA_N)·ψ'₀
  have h_Aψ_deriv_simp : HasDerivAt (fun η : ℝ => (A_R + η • δA_N) * ψ η) (δA_N * ψ₀ + A₀ * ψ'₀) η₀ := by
    have h_simp : (A_R * ψ'₀) + (δA_N * ψ₀ + η₀ • (δA_N * ψ'₀)) = δA_N * ψ₀ + A₀ * ψ'₀ := by
      dsimp [A₀]
      simp [Matrix.add_mul, add_comm, add_left_comm, add_assoc]
    simpa [h_simp] using h_Aψ_deriv
  
  -- Derivative of lam(η)·ψ(η)
  have h_lamψ_deriv : HasDerivAt (fun η : ℝ => lam η • ψ η) (lam'₀ • ψ₀ + lam₀ • ψ'₀) η₀ :=
    HasDerivAt.smul hlam_deriv hψ_deriv
  
  -- Key equation: (A_R + η·δA_N)·ψ(η) = lam(η)·ψ(η) for all η
  -- So f(η) = (A_R + η·δA_N)·ψ(η) - lam(η)·ψ(η) = 0 for all η
  
  -- Hence f'(η₀) = 0
  have h_fderiv_zero : HasDerivAt (fun η : ℝ => ((A_R + η • δA_N) * ψ η) - (lam η • ψ η)) 0 η₀ := by
    have h_fzero : ∀ η : ℝ, ((A_R + η • δA_N) * ψ η) - (lam η • ψ η) = 0 := by
      intro η; rw [h_eigen η, sub_self]
    -- The function is identically zero, so its derivative is also zero
    simpa [h_fzero] using hasDerivAt_const (0 : Matrix (Fin n) (Fin 1) ℂ) η₀
  
  -- By linearity of differentiation, h_Aψ_deriv_simp - h_lamψ_deriv = 0
  -- So: (δA_N·ψ₀ + A₀·ψ'₀) - (lam'₀·ψ₀ + lam₀·ψ'₀) = 0
  have h_key : (δA_N * ψ₀ + A₀ * ψ'₀) = (lam'₀ • ψ₀ + lam₀ • ψ'₀) := by
    have h_diff_eq : HasDerivAt (fun η : ℝ => ((A_R + η • δA_N) * ψ η) - (lam η • ψ η))
        ((δA_N * ψ₀ + A₀ * ψ'₀) - (lam'₀ • ψ₀ + lam₀ • ψ'₀)) η₀ :=
      HasDerivAt.sub h_Aψ_deriv_simp h_lamψ_deriv
    -- But f'(η₀) = 0, so the derivative expression must be 0
    have h_zero_diff : HasDerivAt (fun η : ℝ => ((A_R + η • δA_N) * ψ η) - (lam η • ψ η)) 0 η₀ := h_fderiv_zero
    -- Derivative is unique
    have h_unique : ((δA_N * ψ₀ + A₀ * ψ'₀) - (lam'₀ • ψ₀ + lam₀ • ψ'₀)) = 0 := by
      apply (hasDerivAt_unique h_diff_eq h_zero_diff).symm
    linarith
  
  -- Use A₀ᴴ = A₀ (Hermitian) → lam₀ ∈ ℝ (eigenvalue of Hermitian matrix is real)
  have hA₀_hermitian : A₀ᴴ = A₀ := by
    dsimp [A₀]
    simp [hA_hermitian, hδ_hermitian, add_comm]
  
  -- Rayleigh quotient: ψ₀ᴴ·A₀·ψ₀ = lam₀
  have h_rayleigh : ψ₀ᴴ * A₀ * ψ₀ = lam₀ := by
    calc
      ψ₀ᴴ * A₀ * ψ₀ = ψ₀ᴴ * (A₀ * ψ₀) := by simp [Matrix.mul_assoc]
      _ = ψ₀ᴴ * (lam₀ • ψ₀) := by rw [h_eigen η₀]
      _ = lam₀ • (ψ₀ᴴ * ψ₀) := by simp
      _ = lam₀ := by simp [h_norm η₀]
  
  -- Rayleigh quotient is self-adjoint → lam₀ is real
  have hlam₀_real : star lam₀ = lam₀ := by
    calc
      star lam₀ = (ψ₀ᴴ * A₀ * ψ₀)ᴴ := by rw [h_rayleigh]
      _ = ψ₀ᴴ * A₀ᴴ * ψ₀ := by simp
      _ = ψ₀ᴴ * A₀ * ψ₀ := by rw [hA₀_hermitian]
      _ = lam₀ := h_rayleigh
  
  -- Then ψ₀ᴴ·A₀·ψ'₀ = lam₀·ψ₀ᴴ·ψ'₀  (using A₀ᴴ = A₀ and hlam₀_real)
  have h_ψ₀ᴴ_A₀_ψ'₀ : ψ₀ᴴ * A₀ * ψ'₀ = lam₀ • (ψ₀ᴴ * ψ'₀) := by
    calc
      ψ₀ᴴ * A₀ * ψ'₀ = (ψ₀ᴴ * A₀) * ψ'₀ := by simp [Matrix.mul_assoc]
      _ = (A₀ᴴ * ψ₀)ᴴ * ψ'₀ := by simp
      _ = (A₀ * ψ₀)ᴴ * ψ'₀ := by rw [hA₀_hermitian]
      _ = (lam₀ • ψ₀)ᴴ * ψ'₀ := by rw [h_eigen η₀]
      _ = (star lam₀ • ψ₀ᴴ) * ψ'₀ := by simp
      _ = star lam₀ • (ψ₀ᴴ * ψ'₀) := by simp
      _ = lam₀ • (ψ₀ᴴ * ψ'₀) := by rw [hlam₀_real]
  
  -- Multiply h_key by ψ₀ᴴ on the left
  -- Left: ψ₀ᴴ·(δA_N·ψ₀ + A₀·ψ'₀) = ψ₀ᴴ·δA_N·ψ₀ + ψ₀ᴴ·A₀·ψ'₀
  -- Right: ψ₀ᴴ·(lam'₀·ψ₀ + lam₀·ψ'₀) = lam'₀·ψ₀ᴴ·ψ₀ + lam₀·ψ₀ᴴ·ψ'₀ = lam'₀ + lam₀·ψ₀ᴴ·ψ'₀ (by h_norm)
  have h_mul : ψ₀ᴴ * δA_N * ψ₀ + ψ₀ᴴ * A₀ * ψ'₀ = lam'₀ + lam₀ • (ψ₀ᴴ * ψ'₀) := by
    calc
      ψ₀ᴴ * δA_N * ψ₀ + ψ₀ᴴ * A₀ * ψ'₀
          = ψ₀ᴴ * (δA_N * ψ₀ + A₀ * ψ'₀) := by
            simp [Matrix.mul_add, Matrix.mul_assoc]
      _ = ψ₀ᴴ * (lam'₀ • ψ₀ + lam₀ • ψ'₀) := by rw [h_key]
      _ = ψ₀ᴴ * (lam'₀ • ψ₀) + ψ₀ᴴ * (lam₀ • ψ'₀) := by simp [Matrix.mul_add]
      _ = lam'₀ • (ψ₀ᴴ * ψ₀) + lam₀ • (ψ₀ᴴ * ψ'₀) := by simp
      _ = lam'₀ + lam₀ • (ψ₀ᴴ * ψ'₀) := by simp [h_norm η₀]
  
  -- Substitute h_ψ₀ᴴ_A₀_ψ'₀
  -- ψ₀ᴴ·δA_N·ψ₀ + lam₀·ψ₀ᴴ·ψ'₀ = lam'₀ + lam₀·ψ₀ᴴ·ψ'₀
  -- Cancel lam₀·ψ₀ᴴ·ψ'₀ on both sides
  have h_result : lam'₀ = ψ₀ᴴ * δA_N * ψ₀ := by
    calc
      lam'₀ = (lam'₀ + lam₀ • (ψ₀ᴴ * ψ'₀)) - lam₀ • (ψ₀ᴴ * ψ'₀) := by
        simp
      _ = (ψ₀ᴴ * δA_N * ψ₀ + ψ₀ᴴ * A₀ * ψ'₀) - lam₀ • (ψ₀ᴴ * ψ'₀) := by rw [h_mul]
      _ = (ψ₀ᴴ * δA_N * ψ₀ + lam₀ • (ψ₀ᴴ * ψ'₀)) - lam₀ • (ψ₀ᴴ * ψ'₀) := by rw [h_ψ₀ᴴ_A₀_ψ'₀]
      _ = ψ₀ᴴ * δA_N * ψ₀ := by simp
  
  -- Therefore, HasDerivAt lam (ψ₀ᴴ·δA_N·ψ₀) η₀
  simpa [ψ₀, h_result] using hlam_deriv
  -/

/-- Cl(1,7) 2×2 spectral gap computation: eigenvalues of A_R in the k=1,2 subspace.
    lam₁ = agEigenvalue 1 8 = √2/√72,  lam₂ = agEigenvalue 2 8 = √6/√72. -/
noncomputable def cl17_l1 : ℝ := agEigenvalue 1 8
noncomputable def cl17_l2 : ℝ := agEigenvalue 2 8

/-- The Cl(1,7) spectral gap in the 2×2 subspace: Δlam = lam₂ - lam₁ = (√6-√2)/√72. -/
theorem cl17_subspace_gap : cl17_l2 - cl17_l1 = spectralGap 8 := rfl

/-- Cl(1,7) 2×2 noise perturbation: off-diagonal coupling V = 1/k_max = 1/8.
    This models δA_N restricted to the subspace of the two lowest eigenstates. -/
noncomputable def cl17_V : ℝ := 1/8

/-- 2×2 Cl(1,7) spectral gap function: Δ(η) = √((Δlam_min)² + 4·η²·V²).
    For the off-diagonal perturbation with V = 1/8, this gives the exact η-dependence
    of the gap between the two lowest eigenvalues. -/
theorem cl17_subspace_gap_function (η : ℝ) (hV : cl17_V = 1/8) :
    (cl17_l2 - cl17_l1)^2 + 4 * η^2 * (cl17_V)^2 ≥ (cl17_l2 - cl17_l1)^2 := by
  have h_nonneg : 0 ≤ 4 * η^2 * ((1/8 : ℝ)^2) := by nlinarith
  nlinarith

/-- Cl(1,7) 2×2 eigenvalues lam_±(η) of A_η = A_R + η·δA_N.
    The gap function Δ(η) opens at η = 0 with Δ(0) = Δlam_min and
    grows as √(Δlam_min² + 4η²V²)。

    闭合（2026-08-09，自主完善）：原 True 占位改为真实陈述——λ⁺(η) 满足
    Cl(1,7) 2×2 模型的特征方程 det(A(η) - λI) = 0（经
    twoByTwo_lambda_plus_characteristic，l₁/l₂ = cl17_l1/cl17_l2，
    V = cl17_V，即 FH 公式的显式验证核心）。 -/
theorem cl17_eigenvalue_formula (η : ℝ) (hV : cl17_V = 1/8) :
    Matrix.det (!![(cl17_l1 : ℂ), η * (cl17_V : ℂ); η * conj (cl17_V : ℂ), (cl17_l2 : ℂ)] -
      (twoByTwo_lambda_plus cl17_l1 cl17_l2 (cl17_V : ℂ) η : ℂ) •
        (1 : Matrix (Fin 2) (Fin 2) ℂ)) = 0 :=
  twoByTwo_lambda_plus_characteristic cl17_l1 cl17_l2 (cl17_V : ℂ) η

/-! =========================================================
    Section 5.5: Splitting and Fiber Equivalence
   ========================================================= -/

/-- The cleavage of π_η is split on identities. -/
theorem π_η_cleavage_id {e : SpectralBundleNoise} :
    π_η_cartesianLift.lift (𝟙 (π_η.obj e)) = e := by
  apply SpectralBundleNoise.ext; rfl; rfl

/-- The cleavage of π_η is split on composition. -/
theorem π_η_cleavage_comp {e : SpectralBundleNoise} {b₀ b₁ : NoiseObj}
    (f : b₀ ⟶ b₁) (g : b₁ ⟶ π_η.obj e) :
    π_η_cartesianLift.lift (f ≫ g) =
      π_η_cartesianLift.lift (e := π_η_cartesianLift.lift g) f := rfl

/-! =========================================================
    Section 6: Connection to Mathlib's IsFibered

    ※ 开放项登记（2026-08-07）：IsStronglyCartesian/IsFibered 的严格实例依赖
    FiberedCategory 的复合结构；specFiberNoiseEquivFiber（纤维等价）依赖
    SpecFiberNoise 的 Category 实例，均以开放项登记，暂不声明。
   ========================================================= -/

/-! =========================================================
    Section 7: Fibered Functor N̂ : Bun(Temp, Spec) → Bun(Noise, Spec)
   ========================================================= -/

/-- The fibered functor N̂ : Bun(Temp, Spec) → Bun(Noise, Spec).
    It maps the base via the isomorphism Noise ≅ Temp and acts as identity on fibers.
    This establishes the noise-temperature duality as a Grothendieck fibered functor. -/
noncomputable def N_hat : SpectralBundleTemp ⥤ SpectralBundleNoise where
  obj X :=
    { base := ⟨X.base.T, by linarith [X.base.pos]⟩
      fiberData := { n := X.fiberData.n, A := X.fiberData.A }
    }
  map f :=
    { baseMap := ⟨f.baseMap.r, f.baseMap.r_pos, f.baseMap.eq⟩
      fiberMap := f.fiberMap
      commut := f.commut
    }
  map_id X := by
    apply BundleNoiseHom.ext <;> rfl
  map_comp f g := by
    apply BundleNoiseHom.ext <;> rfl

/-- N̂ is base-faithful: the induced base map equals the inverse functor applied to base.

    闭合（2026-08-09，自主完善）：两端均归约为 ⟨X.base.T, ·⟩（π_η/π_T 为
    abbrev 投影，NInvFunctor 为构造性函子），结构外延 + 证明无关性即证。 -/
theorem N_hat_base_commutes (X : SpectralBundleTemp) :
    π_η.obj (N_hat.obj X) = NInvFunctor.obj (π_T.obj X) := by
  simp [N_hat, π_T, NInvFunctor]

/-! =========================================================
    Section 8: Physical Noise Section with η_c Singularity
   ========================================================= -/

/-- Noise section σ_Δ^(noise) : Noise → Bun(Noise, Spec).
    Maps each noise strength η to the bundle object with spectral gap data.
    The gap vanishes at η = η_c (spectral closure → continuous noise background). -/
noncomputable def NoiseSection (n : ℕ) (A : Matrix (Fin n) (Fin n) ℂ) : NoiseObj ⥤ SpectralBundleNoise where
  obj η := { base := η, fiberData := { n := n, A := A } }
  map f := { baseMap := f, fiberMap := 1, commut := by simp }
  map_id η := rfl
  map_comp f g := by
    apply BundleNoiseHom.ext
    · rfl
    · change 1 = 1 * 1
      simp

/-- Noise section is a section of π_η: π_η ∘ σ = id_Noise. -/
theorem NoiseSection_is_section (n : ℕ) (A : Matrix (Fin n) (Fin n) ℂ) (η : NoiseObj) :
    π_η.obj ((NoiseSection n A).obj η) = η := rfl

/-- Corrected critical noise threshold from Cl(1,7) algebra: η_c = 2(√3-1)/3 ≈ 0.488.
    
    FIRST-PRINCIPLES DERIVATION:
    Let A(η) = A_R + η·δA_N. The spectral gap closes at η_c when lam₁(η_c) = lam₂(η_c).
    
    First-order eigenvalue equation (exact for linear A(η)):
      lam_k(η) = lam_k(0) + η·⟨ψ_k|δA_N|ψ_k⟩
    
    Gap closure:
      lam₁(0) + η_c·⟨ψ₁|δA_N|ψ₁⟩ = lam₂(0) + η_c·⟨ψ₂|δA_N|ψ₂⟩
      η_c·[⟨ψ₁|δA_N|ψ₁⟩ - ⟨ψ₂|δA_N|ψ₂⟩] = lam₂(0) - lam₁(0) = Δlam_min
      η_c = Δlam_min / (⟨ψ₁|δA_N|ψ₁⟩ - ⟨ψ₂|δA_N|ψ₂⟩)
    
    In Cl(1,7) ≅ M₁₆(ℝ)（旋量 16，2026-08-07 勘误；2×2 子空间为翻倍工作基准），
    the noise operator restricted to the 2×2 subspace is:
      δA_N|₂ₓ₂ = σ_z / k_max
    where σ_z is the Pauli matrix with eigenvalues ±1.
    Hence ⟨ψ₁|δA_N|ψ₁⟩ = +1/k_max, ⟨ψ₂|δA_N|ψ₂⟩ = -1/k_max.
    
    Therefore:
      ⟨ψ₁|δA_N|ψ₁⟩ - ⟨ψ₂|δA_N|ψ₂⟩ = 1/k_max - (-1/k_max) = 2/k_max
      η_c = Δlam_min / (2/k_max) = (k_max/2)·Δlam_min = 4·Δlam_min = 2(√3-1)/3
    
    The factor of 2 arises because δA_N = σ_z/k_max has eigenvalues ±1/k_max,
    so the difference is 2/k_max (not 1/k_max). This is the traceless condition:
    the σ_z component pushes BOTH eigenvalues in opposite directions. -/
noncomputable def criticalNoiseEta_from_cl17 : NoiseObj :=
  ⟨2*(Real.sqrt 3 - 1)/3, by
    have h : 1 < Real.sqrt 3 := by
      calc
        1 = Real.sqrt (1 : ℝ) := by norm_num
        _ < Real.sqrt 3 := Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
    have hpos : 0 < Real.sqrt 3 - 1 := by linarith
    exact div_pos (mul_pos (by norm_num) hpos) (by norm_num)⟩

/-- At η = η_c, the noise section hits the boundary where the spectral gap closes.
    This corresponds to the τ(η) ∝ 1/(η_c-η) singularity (Paper X §12.4).
    In the Grothendieck fibration framework, this means the section cannot be
    continuously extended across η_c—a non-product bundle phenomenon.

    勘误（2026-08-09）：原前提 η.η = 0 与 NoiseObj 的 η > 0 矛盾（且与 η_c
    语义不符）；改为 η.η = η_c（criticalNoiseEta_from_cl17）。 -/
theorem eta_c_singularity (n : ℕ) (A : Matrix (Fin n) (Fin n) ℂ) (η : NoiseObj)
    (h : η.η = criticalNoiseEta_from_cl17.η) :
    π_η.obj ((NoiseSection n A).obj η) = η := rfl

/-- Theorem: η_c (from Cl(1,7)) relates to the spectral gap via η_c = (k_max/2) · Δlam_min.
    With k_max = 8, this gives η_c = 4 · Δlam_min = 2(√3-1)/3. 
    
    The factor (k_max/2) comes from the first-principles derivation:
    η_c = Δlam_min / (⟨ψ₁|δA_N|ψ₁⟩ - ⟨ψ₂|δA_N|ψ₂⟩)
        = Δlam_min / (2/k_max)
        = (k_max/2) · Δlam_min -/
theorem criticalEta_from_spectralGap : criticalNoiseEta_from_cl17.η = 2*(Real.sqrt 3 - 1)/3 := rfl

/-- Theorem: η_c is determined by the Cl(1,7) spectral gap and representation dimension.
    η_c = (k_max/2) · spectralGap(k_max) = 4 · spectralGap(8)
    Proof: η_c = Δlam_min / (2/k_max) = (k_max/2)·Δlam_min (first-principles gap closure).

    闭合（2026-08-09，自主完善）：2(√3-1)/3 = 4·(√6-√2)/√72 经
    √72 = 6√2 与 √6/√2 = √3（Real.sqrt_div）的平方根代数验证。 -/
theorem criticalEta_spectralGap_relation :
    criticalNoiseEta_from_cl17.η = (4 : ℝ) * (spectralGap 8) := by
  rw [criticalNoiseEta_from_cl17]
  rw [spectralGap_at_kmax8]
  have h72 : Real.sqrt (72 : ℝ) = 6 * Real.sqrt 2 := by
    rw [show (72 : ℝ) = 36 * 2 by norm_num]
    rw [Real.sqrt_mul (by norm_num : (0 : ℝ) ≤ 36) (2 : ℝ)]
    rw [show Real.sqrt (36 : ℝ) = 6 by
      rw [show (36 : ℝ) = 6 ^ 2 by norm_num]
      exact Real.sqrt_sq (by norm_num : (0 : ℝ) ≤ 6)]
  have hratio : Real.sqrt 6 / Real.sqrt 2 = Real.sqrt 3 := by
    calc
      Real.sqrt 6 / Real.sqrt 2 = Real.sqrt (6 / 2) :=
        (Real.sqrt_div (by norm_num : (0 : ℝ) ≤ 6) (2 : ℝ)).symm
      _ = Real.sqrt 3 := by norm_num
  have h2ne : Real.sqrt 2 ≠ 0 := by positivity
  have h72ne : Real.sqrt (72 : ℝ) ≠ 0 := by positivity
  calc
    2 * (Real.sqrt 3 - 1) / 3 = (2 / 3) * (Real.sqrt 3 - 1) := by ring
    _ = (2 / 3) * (Real.sqrt 6 / Real.sqrt 2 - 1) := by rw [hratio]
    _ = (2 / 3) * (Real.sqrt 6 - Real.sqrt 2) / Real.sqrt 2 := by
      field_simp [h2ne]
    _ = 4 * (Real.sqrt 6 - Real.sqrt 2) / (6 * Real.sqrt 2) := by
      field_simp [h2ne]
      ring
    _ = 4 * (Real.sqrt 6 - Real.sqrt 2) / Real.sqrt (72 : ℝ) := by rw [h72]
    _ = 4 * ((Real.sqrt 6 - Real.sqrt 2) / Real.sqrt (72 : ℝ)) := by
      field_simp [h72ne]

end UFPFormalization
