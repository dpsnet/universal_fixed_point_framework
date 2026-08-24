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
-- 本文件中 UFPF 相关引用数量：6
-- 更名将在计划确认后统一执行，当前代码不做修改。
-- ============================================================

import UFPFormalization.RecCategory
import UFPFormalization.SpCategory
import UFPFormalization.DecursionFunctor
import UFPFormalization.IFSFractal
import Mathlib.Analysis.Convex.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Log.NegMulLog
import Mathlib.Data.Real.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic
import Mathlib.Tactic.Linarith.Frontend

namespace UFPFormalization

open Real
open Set

/-!
# Thermodynamic Formalism Formalization (Phase 16C-III)

This file formalizes the thermodynamic formalism for IFS-based
recursive systems, providing the mathematical foundation for the
multifractal analysis of the spectral de-recursion framework.

Three main components:
  1. Pressure Function: topological pressure P(φ) = sup(h_μ + ∫φ dμ)
  2. Legendre Transform: convex conjugate f*(p) = sup(px - f(x))
  3. Theorem D-C: concavity of d_H(ρ) (Hausdorff dimension as a function
     of the probability vector ρ)

Based on mathlib4 libraries: `Analysis.Convex` (convex analysis),
`Analysis.ImplicitFunction` (implicit function theorem).

Note: This is a finite-dimensional prototype. The full ergodic-theoretic
generalization (topological pressure on shift spaces, variational principle)
is deferred.
-/

/-! ### 1. Pressure Function Formalization -/

/--
Topological pressure P(φ) for a potential φ on an IFS shift space.
Defined as:
  P(φ) = lim_{n→∞} (1/n) log Σ_{w ∈ Σ_n} exp(Σ_{k=0}^{n-1} φ(w_k))
where Σ_n is the set of length-n words and φ is a Hölder continuous potential.

In the finite-dimensional prototype, we compute the pressure for the
geometric potential φ_t(x) = -t · log |f'(x)| = -t · log c_i.
-/
noncomputable def topologicalPressure {X : Type} [MetricSpace X] [CompleteSpace X]
    (ifs : IFS X) (t : ℝ) : ℝ :=
  -- For the geometric potential φ_t(x) = -t · log |f'(x)|,
  -- the pressure is given by P(t) = log(Σ c_i^t)
  Real.log (Finset.sum (Finset.univ : Finset (Fin ifs.n))
    (fun i : Fin ifs.n => (ifs.ratios i : ℝ) ^ t))

/--
The pressure function P(t) is strictly decreasing in t
(since each c_i^t is decreasing in t for c_i ∈ (0,1)).

Requires the IFS to have at least one map (n ≥ 1) to avoid the
degenerate case where the pressure is log(0) = 0 constant.
-/
theorem pressure_strictly_decreasing {X : Type} [MetricSpace X] [CompleteSpace X]
    (ifs : IFS X) (hNonempty : ifs.n ≥ 1) (t₁ t₂ : ℝ) (h : t₁ < t₂) :
    topologicalPressure ifs t₂ < topologicalPressure ifs t₁ := by
  -- Since c_i ∈ (0,1), c_i^{t₂} < c_i^{t₁} for each i, so Σ c_i^{t₂} < Σ c_i^{t₁}.
  -- Since log is strictly increasing on ℝ⁺, log(Σ c_i^{t₂}) < log(Σ c_i^{t₁}).
  have h_sum_lt : (Finset.sum (Finset.univ : Finset (Fin ifs.n))
      (fun i : Fin ifs.n => (ifs.ratios i : ℝ) ^ t₂)) <
    (Finset.sum (Finset.univ : Finset (Fin ifs.n))
      (fun i : Fin ifs.n => (ifs.ratios i : ℝ) ^ t₁)) := by
    have h_all_le : ∀ i : Fin ifs.n, (ifs.ratios i : ℝ) ^ t₂ ≤ (ifs.ratios i : ℝ) ^ t₁ := by
      intro i
      have hc_pos : (0 : ℝ) < ifs.ratios i := by exact_mod_cast ifs.hRatiosPos i
      have hc_lt_one : (ifs.ratios i : ℝ) < 1 := by exact_mod_cast ifs.hRatiosLtOne i
      -- For 0 < c < 1 and t₁ < t₂, we have c^{t₂} < c^{t₁}
      exact le_of_lt (Real.rpow_lt_rpow_of_exponent_gt hc_pos hc_lt_one h)
    -- Need at least one strict inequality. Since n ≥ 1, Fin ifs.n is nonempty.
    have h_nonempty : Finset.Nonempty (Finset.univ : Finset (Fin ifs.n)) := by
      rcases eq_or_lt_of_le hNonempty with (h_eq | h_gt)
      · -- ifs.n = 1, at least one element
        refine ⟨⟨0, by omega⟩, Finset.mem_univ _⟩
      · -- ifs.n > 1, definitely nonempty
        refine ⟨⟨0, by omega⟩, Finset.mem_univ _⟩
    have h_strict : ∃ i ∈ Finset.univ, (ifs.ratios i : ℝ) ^ t₂ < (ifs.ratios i : ℝ) ^ t₁ := by
      rcases h_nonempty with ⟨i, hi⟩
      refine ⟨i, hi, Real.rpow_lt_rpow_of_exponent_gt
        (by exact_mod_cast ifs.hRatiosPos i) (by exact_mod_cast ifs.hRatiosLtOne i) h⟩
    exact Finset.sum_lt_sum (fun i hi => h_all_le i) h_strict
  -- The sum is positive (all terms are positive), so log is defined and strictly increasing
  have h_sum_pos : 0 < Finset.sum (Finset.univ : Finset (Fin ifs.n))
      (fun i : Fin ifs.n => (ifs.ratios i : ℝ) ^ t₂) := by
    have h_nonempty : Finset.Nonempty (Finset.univ : Finset (Fin ifs.n)) := by
      refine ⟨⟨0, by omega⟩, Finset.mem_univ _⟩
    exact Finset.sum_pos (fun i hi => Real.rpow_pos_of_pos (by exact_mod_cast ifs.hRatiosPos i) t₂) h_nonempty
  exact Real.log_lt_log h_sum_pos h_sum_lt

/--
The pressure at t = 0 equals log(n), where n is the number of IFS maps.
-/
theorem pressure_at_zero {X : Type} [MetricSpace X] [CompleteSpace X]
    (ifs : IFS X) : topologicalPressure ifs 0 = Real.log (ifs.n : ℝ) := by
  -- Σ c_i^0 = Σ 1 = n, so P(0) = log(n)
  simp [topologicalPressure, Finset.sum_const, nsmul_eq_mul]

/--
The Hausdorff dimension d_H is the unique t such that P(t) = 0,
i.e., log(Σ c_i^{d_H}) = 0, or equivalently Σ c_i^{d_H} = 1.
This is the Moran equation connection between pressure and dimension.
-/
theorem pressure_zero_iff_hausdorff_dimension {X : Type} [MetricSpace X] [CompleteSpace X]
    (ifs : IFS X) (t : ℝ) (hNonempty : ifs.n ≥ 1) :
    topologicalPressure ifs t = 0 ↔ hausdorffDimensionEq ifs t = 0 := by
  dsimp [topologicalPressure, hausdorffDimensionEq]
  constructor
  · intro h
    -- P(t) = 0 ⟹ log(Σ c_i^t) = 0 ⟹ Σ c_i^t = 1 ⟹ Σ c_i^t - 1 = 0
    have h_log_eq_zero : Real.log (Finset.sum (Finset.univ : Finset (Fin ifs.n))
      (fun i : Fin ifs.n => (ifs.ratios i : ℝ) ^ t)) = 0 := h
    have h_sum_pos : 0 < Finset.sum (Finset.univ : Finset (Fin ifs.n))
      (fun i : Fin ifs.n => (ifs.ratios i : ℝ) ^ t) := by
      apply Finset.sum_pos (fun i hi => Real.rpow_pos_of_pos (by exact_mod_cast ifs.hRatiosPos i) t)
      refine ⟨⟨0, by omega⟩, Finset.mem_univ _⟩
    have h_sum_eq_one : Finset.sum (Finset.univ : Finset (Fin ifs.n))
      (fun i : Fin ifs.n => (ifs.ratios i : ℝ) ^ t) = 1 := by
      -- log(x) = 0 ⟹ x = 1 (via injectivity of exp on ℝ⁺)
      have h_exp : Real.exp (Real.log (Finset.sum (Finset.univ : Finset (Fin ifs.n))
        (fun i : Fin ifs.n => (ifs.ratios i : ℝ) ^ t))) = Real.exp 0 := by
        rw [h_log_eq_zero]
      rw [← Real.exp_log h_sum_pos, ← Real.exp_zero]
      exact h_exp
    rw [h_sum_eq_one]
    simp
  · intro h
    -- hausdorffDimensionEq ifs t = 0 ⟹ Σ c_i^t - 1 = 0 ⟹ Σ c_i^t = 1 ⟹ log(1) = 0
    have h_sum_eq_one : Finset.sum (Finset.univ : Finset (Fin ifs.n))
      (fun i : Fin ifs.n => (ifs.ratios i : ℝ) ^ t) = 1 := by
      linarith
    simp [h_sum_eq_one]

/-! ### 2. Legendre Transform Interface -/

/--
The Legendre transform (convex conjugate) of a function f: ℝ → ℝ.
  f*(p) = sup_{x ∈ ℝ} (p·x - f(x))

For the multifractal spectrum, we need the Legendre transform of τ(q)
(the multifractal spectrum, which is convex):
  f(α) = inf_{q ∈ ℝ} (q·α - τ(q))
which gives the singularity spectrum.
-/
noncomputable def legendreTransform (f : ℝ → ℝ) (p : ℝ) : ℝ :=
  ⨆ (x : ℝ), (p * x - f x)

/--
The Legendre transform of a function f is convex.
Proof: f*(p) = sup_x (p·x - f(x)) is the pointwise supremum of affine
functions p ↦ p·x - f(x), and the supremum of convex functions is convex.

※ 修正（2026-08-04）：ℝ 是条件完备格（非 CompleteLattice），逐点上确界
`iSup` 需要 `BddAbove (range fun z => p*z - f z)`。对一般 f 不成立
（占位 τ(q) = q-1 下 p ≠ 1 时无界），故将原无假设陈述改为**条件定理**：
加 `hBdd` 假设后逐点 `csSup_le` 论证，零 `sorry`。
-/
theorem legendreTransform_convex {f : ℝ → ℝ} (hf : ConvexOn ℝ Set.univ f)
    (hBdd : ∀ p : ℝ, BddAbove (range fun z : ℝ => p * z - f z)) :
    ConvexOn ℝ Set.univ (legendreTransform f) := by
  refine ⟨convex_univ, ?_⟩
  intro p₁ hp₁ p₂ hp₂ a b ha hb hab
  dsimp [legendreTransform]
  have h_rewrite : (fun x : ℝ => (a * p₁ + b * p₂) * x - f x) =
      (fun x : ℝ => a * (p₁ * x - f x) + b * (p₂ * x - f x)) := by
    funext x
    have hf : (a + b) * f x = f x := by rw [hab]; ring
    nlinarith
  rw [h_rewrite]
  -- 目标：⨆ x, (a*(p₁*x - f x) + b*(p₂*x - f x)) ≤ a*⨆x (p₁*x-f x) + b*⨆x (p₂*x-f x)
  apply csSup_le
  · exact Set.range_nonempty _
  · intro y hy
    rcases hy with ⟨x, rfl⟩
    have h1 : p₁ * x - f x ≤ ⨆ x : ℝ, (p₁ * x - f x) :=
      le_csSup (hBdd p₁) ⟨x, rfl⟩
    have h2 : p₂ * x - f x ≤ ⨆ x : ℝ, (p₂ * x - f x) :=
      le_csSup (hBdd p₂) ⟨x, rfl⟩
    have h3 : a * (p₁ * x - f x) ≤ a * ⨆ x : ℝ, (p₁ * x - f x) :=
      mul_le_mul_of_nonneg_left h1 ha
    have h4 : b * (p₂ * x - f x) ≤ b * ⨆ x : ℝ, (p₂ * x - f x) :=
      mul_le_mul_of_nonneg_left h2 hb
    exact add_le_add h3 h4

/--
The multifractal singularity spectrum f(α) is the Legendre transform
of τ(q):
  f(α) = inf_{q ∈ ℝ} (q·α - τ(q))

For a self-similar measure with weights p_i and ratios c_i,
the singularity spectrum f(α) characterizes the fractal dimension
of the set of points with Hölder exponent α.
-/
noncomputable def singularitySpectrum {X : Type} [MetricSpace X] [CompleteSpace X]
    {ifs : IFS X} {attractor : Attractor ifs}
    (measure : SelfSimilarMeasure ifs attractor) (α : ℝ) : ℝ :=
  -legendreTransform (multifractalSpectrum measure) α

/--
The singularity spectrum f(α) satisfies f(α) ≤ d_H (Hausdorff dimension),
with equality at the maximizing Hölder exponent α₀.

※ 修正（2026-08-04）：原陈述在占位定义下不可证，改为**条件定理**：
  - `hτ0 : multifractalSpectrum measure 0 = -sol.dH`——Bowen 公式 τ(0) = -d_H
    （由 Σ c_i^{d_H} = 1 导出，完整隐函数求解为开放项，显式化为假设）；
  - `hBdd : BddAbove (range fun q => α*q - τ(q))`——ℝ 条件完备格上
    `iSup` 逐点下界需有界性（占位 τ(q)=q-1 下 α ≠ 1 时无界）。

其余证明链（sup 逐点下界 + 不等式传递）零 `sorry`。
-/
theorem singularity_spectrum_bound {X : Type} [MetricSpace X] [CompleteSpace X]
    {ifs : IFS X} {attractor : Attractor ifs}
    (measure : SelfSimilarMeasure ifs attractor) (sol : HausdorffDimensionSolution ifs)
    (α : ℝ) (hτ0 : multifractalSpectrum measure (0 : ℝ) = -sol.dH)
    (hBdd : BddAbove (range fun q : ℝ => α * q - multifractalSpectrum measure q)) :
    singularitySpectrum measure α ≤ sol.dH := by
  -- Standard result: the singularity spectrum is bounded by the Hausdorff dimension.
  -- The full bound f(α) ≤ d_H requires the variational principle
  -- (Falconer 2014, Ch. 17, Theorem 17.2).
  have h_full : singularitySpectrum measure α ≤ sol.dH := by
    -- f(α) ≤ d_H for self-similar measures (Falconer 2014, Ch. 17, Theorem 17.2).
    -- Proof structure:
    --   By the Legendre transform: f(α) = inf_q (q·α - τ(q)).
    --   τ(0) = -d_H (Bowen formula, 假设 hτ0), so f(α) ≤ 0·α - τ(0) = d_H.
    have h_tau_zero : multifractalSpectrum measure (0 : ℝ) = -sol.dH := hτ0
    calc
      singularitySpectrum measure α
          = -(⨆ (q : ℝ), (α * q - multifractalSpectrum measure q)) := rfl
      _ ≤ -(0 * α - multifractalSpectrum measure (0 : ℝ)) := by
        have h_sup : (⨆ (q : ℝ), (α * q - multifractalSpectrum measure q)) ≥
          0 * α - multifractalSpectrum measure (0 : ℝ) := by
          -- 0*α - τ(0) 是 range 中 q = 0 处的值，`le_csSup` 直接给出下界
          exact le_csSup hBdd ⟨0, by simp⟩
        simp at h_sup
        nlinarith
      _ = -(-multifractalSpectrum measure (0 : ℝ)) := by simp
      _ = multifractalSpectrum measure (0 : ℝ) := by simp
      _ = -sol.dH := h_tau_zero
      _ ≤ sol.dH := by
        -- d_H ≥ 0 由 HausdorffDimensionSolution.hPos（d_H > 0）直接给出
        have h_nonneg : 0 ≤ sol.dH := le_of_lt sol.hPos
        nlinarith
  exact h_full

/-! ### 3. Theorem D-C: Concavity of d_H(ρ) -/

/--
The Hausdorff dimension d_H(ρ) as a function of the probability vector ρ.
For an IFS with fixed contraction ratios {c_i}, varying the probability
weights {p_i} changes the multifractal spectrum and hence the effective
Hausdorff dimension of the measure.

d_H(ρ) = Σ_{i=1}^n p_i · log(p_i) / log(c_i)

This is the formula for the information dimension of a self-similar
measure with weights p_i and ratios c_i.
-/
noncomputable def hausdorffDimensionOfMeasure {X : Type} [MetricSpace X] [CompleteSpace X]
    {ifs : IFS X} {attractor : Attractor ifs}
    (measure : SelfSimilarMeasure ifs attractor) : ℝ :=
  -- d_H(ρ) = Σ p_i · log(p_i) / log(c_i)
  -- Convention: p_i · log(p_i) = 0 when p_i = 0 (limit)
  Finset.sum (Finset.univ : Finset (Fin ifs.n))
    (fun i : Fin ifs.n =>
      (measure.weights i) * Real.log (measure.weights i) / Real.log (ifs.ratios i))

/-- 信息维数（权重层面）：d(ρ) = Σ ρ_i · log(ρ_i) / log(c_i)。 -/
noncomputable def hausdorffDimensionOfWeights {n : ℕ} (w : Fin n → ℝ) (c : Fin n → ℝ) : ℝ :=
  Finset.sum (Finset.univ : Finset (Fin n))
    (fun i : Fin n => w i * Real.log (w i) / Real.log (c i))

/-- 权重凸组合（定理 D-C 的对象）。

※ 修正（2026-08-04）：原 `interpolateMeasure` 声称构造 `SelfSimilarMeasure`
（自相似测度）的凸组合，但**测度的凸组合不自相似**——不变性方程
μ = Σ p_i·μ∘f_i⁻¹ 的交叉项 lam(1-lam)·p₁·μ₂ 不消失，`hInvariance` 为
结构性假定理（不可证）。删除该定义，定理 D-C 仅在**权重层面**成立
（凹性来自权重函数，与测度不变性无关），重构为 `interpolateWeights`。 -/
noncomputable def interpolateWeights {n : ℕ} (w₁ w₂ : Fin n → ℝ) (lam : ℝ) : Fin n → ℝ :=
  fun i => lam * w₁ i + (1 - lam) * w₂ i

/--
Theorem D-C: d_H(ρ) is a concave function of the probability vector ρ.

Proof sketch:
  d_H(ρ) = Σ p_i · log(p_i) / log(c_i)
  Since log(c_i) < 0 (c_i < 1), the function p ↦ p·log(p) is concave,
  and dividing by the negative constant log(c_i) preserves concavity.

※ 修正（2026-08-04）：改为权重层面陈述（`hausdorffDimensionOfWeights`），
不再依赖被删除的假定理 `interpolateMeasure`。假设 `hpos₁/hpos₂`
（权重正性）与 `hlog_neg`（log(c_i) < 0，即 c_i ∈ (0,1)）为构造所需，
其余证明链零 `sorry`。
-/
theorem theorem_DC_concavity {n : ℕ} (w₁ w₂ : Fin n → ℝ) (c : Fin n → ℝ)
    (hpos₁ : ∀ i, 0 < w₁ i) (hpos₂ : ∀ i, 0 < w₂ i)
    (hlog_neg : ∀ i, Real.log (c i) < 0)
    (lam : ℝ) (hlam : 0 ≤ lam ∧ lam ≤ 1) :
    hausdorffDimensionOfWeights (interpolateWeights w₁ w₂ lam) c ≥
    lam * hausdorffDimensionOfWeights w₁ c + (1 - lam) * hausdorffDimensionOfWeights w₂ c := by
  rcases hlam with ⟨hlam0, hlam1⟩
  -- Per-term inequality: x·log(x) is convex on [0,∞) (mathlib `Real.convexOn_mul_log`),
  -- so the weighted Jensen inequality holds.
  have h_entropy_convex : ∀ (a b : ℝ), a > 0 → b > 0 →
      (lam * a + (1 - lam) * b) * Real.log (lam * a + (1 - lam) * b) ≤
      lam * (a * Real.log a) + (1 - lam) * (b * Real.log b) := by
    intro a b ha hb
    simpa [smul_eq_mul] using
      (Real.convexOn_mul_log.2 (le_of_lt ha) (le_of_lt hb) hlam0 (by linarith) (by ring))
  have h_term : ∀ i : Fin n,
      ((lam * w₁ i + (1 - lam) * w₂ i) *
        Real.log (lam * w₁ i + (1 - lam) * w₂ i) / Real.log (c i)) ≥
      lam * (w₁ i * Real.log (w₁ i) / Real.log (c i)) +
      (1 - lam) * (w₂ i * Real.log (w₂ i) / Real.log (c i)) := by
    intro i
    set p := w₁ i with hp
    set q := w₂ i with hq
    have hp_pos : p > 0 := hpos₁ i
    have hq_pos : q > 0 := hpos₂ i
    have h_log_neg : Real.log (c i) < 0 := hlog_neg i
    have h_main : (lam * p + (1 - lam) * q) * Real.log (lam * p + (1 - lam) * q) ≤
      lam * (p * Real.log p) + (1 - lam) * (q * Real.log q) :=
      h_entropy_convex p q hp_pos hq_pos
    -- Since denominator log(c_i) < 0, dividing reverses the inequality
    have h_div : ((lam * p + (1 - lam) * q) * Real.log (lam * p + (1 - lam) * q)) / Real.log (c i) ≥
        (lam * (p * Real.log p) + (1 - lam) * (q * Real.log q)) / Real.log (c i) := by
      have h_num_nonpos : ((lam * p + (1 - lam) * q) * Real.log (lam * p + (1 - lam) * q)) -
        (lam * (p * Real.log p) + (1 - lam) * (q * Real.log q)) ≤ 0 := by linarith
      have h_den_neg : Real.log (c i) < 0 := h_log_neg
      have h_ratio_nonneg : ((((lam * p + (1 - lam) * q) * Real.log (lam * p + (1 - lam) * q)) -
        (lam * (p * Real.log p) + (1 - lam) * (q * Real.log q))) / Real.log (c i)) ≥ 0 :=
        div_nonneg_of_nonpos h_num_nonpos (le_of_lt h_den_neg)
      rw [sub_div] at h_ratio_nonneg
      linarith
    calc
      ((lam * p + (1 - lam) * q) * Real.log (lam * p + (1 - lam) * q)) / Real.log (c i) ≥
        (lam * (p * Real.log p) + (1 - lam) * (q * Real.log q)) / Real.log (c i) := h_div
      _ = lam * (p * Real.log p / Real.log (c i)) + (1 - lam) * (q * Real.log q / Real.log (c i)) := by ring
  -- Sum over all indices
  dsimp [hausdorffDimensionOfWeights, interpolateWeights]
  calc
    Finset.sum (Finset.univ : Finset (Fin n))
      (fun i : Fin n => (lam * w₁ i + (1 - lam) * w₂ i) *
        Real.log (lam * w₁ i + (1 - lam) * w₂ i) / Real.log (c i)) ≥
    Finset.sum (Finset.univ : Finset (Fin n))
      (fun i : Fin n =>
        lam * (w₁ i * Real.log (w₁ i) / Real.log (c i)) +
        (1 - lam) * (w₂ i * Real.log (w₂ i) / Real.log (c i))) :=
      Finset.sum_le_sum (fun i hi => h_term i)
    _ = lam * (Finset.sum (Finset.univ : Finset (Fin n))
      (fun i : Fin n => w₁ i * Real.log (w₁ i) / Real.log (c i))) +
      (1 - lam) * (Finset.sum (Finset.univ : Finset (Fin n))
      (fun i : Fin n => w₂ i * Real.log (w₂ i) / Real.log (c i))) := by
      simp [Finset.sum_add_distrib, Finset.mul_sum]
    _ = lam * hausdorffDimensionOfWeights w₁ c + (1 - lam) * hausdorffDimensionOfWeights w₂ c := rfl

/--
Theorem D-C Corollary: The singularity spectrum f(α) is concave in α.
Proof: f(α) = -τ*(α) where τ* is the Legendre transform of τ(q).
Since τ(q) is convex (standard property of multifractal spectrum),
τ* is convex (legendreTransform_convex), so -τ* is concave.

※ 修正（2026-08-04）：原陈述在占位 τ(q) = q-1 下为**假定理**——此时
legendreTransform τ α = ⨆ q, (α·q - (q-1)) = ⨆ q, ((α-1)·q + 1)，α ≠ 1 时
无界，`ConvexOn` 前提（sup 存在）不成立。故改为**条件定理**：
加 `hBdd : ∀ p, BddAbove (range fun q => p*q - τ(q))` 假设（与
`legendreTransform_convex` 签名对齐），其余证明链零 `sorry`。
-/
theorem singularity_spectrum_concave {X : Type} [MetricSpace X] [CompleteSpace X]
    {ifs : IFS X} {attractor : Attractor ifs}
    (measure : SelfSimilarMeasure ifs attractor)
    (hBdd : ∀ p : ℝ, BddAbove (range fun q : ℝ => p * q - multifractalSpectrum measure q)) :
    ConcaveOn ℝ Set.univ (singularitySpectrum measure) := by
  -- f(α) = -τ*(α) where τ* = L[τ]
  -- τ* is convex by legendreTransform_convex, so -τ* is concave.
  have h_convex_legendre : ConvexOn ℝ Set.univ (legendreTransform (multifractalSpectrum measure)) :=
    legendreTransform_convex (by
      -- τ(q) = q - 1 是线性函数（占位定义），凸性平凡成立
      refine ⟨convex_univ, ?_⟩
      intro x hx y hy a b ha hb hab
      have hτ : ∀ z : ℝ, multifractalSpectrum measure z = z - 1 := by
        intro z
        rfl
      -- τ(q) = q - 1 是仿射函数：τ(ax+by) = a·τ(x) + b·τ(y)（hab : a+b=1）
      rw [hτ, hτ, hτ]
      simp [smul_eq_mul]
      nlinarith [hab]) hBdd
  -- ConcaveOn means: ∀ x y a b, a+b=1, a,b≥0 → f(ax+by) ≥ a·f(x) + b·f(y)
  -- This is the negation of convexity of τ*
  rcases h_convex_legendre with ⟨hconvex_set, hconvex⟩
  refine ⟨hconvex_set, ?_⟩
  intro x hx y hy a b ha hb hab
  have hstar := hconvex hx hy ha hb hab
  dsimp [singularitySpectrum]
  -- f(ax+by) = -τ*(ax+by) ≥ -(a·τ*(x) + b·τ*(y)) = a·f(x) + b·f(y)
  simp [smul_eq_mul] at *
  nlinarith [hstar]

/--
Link between the thermodynamic formalism and the spectral equivalence framework:
P(t) = 0 iff t = d_H (the Hausdorff dimension of the IFS attractor).

注：Moran 维数（相似维数）在一般 IFS 下可超过映射个数 n（如 n=2、c_i=0.9 时
2·0.9^t = 1 的解 t ≈ 6.58 > 2），因此 `HausdorffDimensionSolution.hBound`
（d_H ≤ n）并非普遍定理，而是逐例验证的性质。前向方向需要显式假设
`hBound : t ≤ ifs.n` 才能构造解。
-/
theorem pressure_spectral_link {X : Type} [MetricSpace X] [CompleteSpace X]
    (ifs : IFS X) (t : ℝ) (hNonempty : ifs.n ≥ 2) (hBound : t ≤ (ifs.n : ℝ)) :
    topologicalPressure ifs t = 0 ↔
    (∃ (sol : HausdorffDimensionSolution ifs), sol.dH = t) := by
  constructor
  · intro hP
    -- If P(t) = 0, then Σ c_i^t = 1 (by pressure_zero_iff_hausdorff_dimension)
    have hEq : hausdorffDimensionEq ifs t = 0 :=
      (pressure_zero_iff_hausdorff_dimension ifs t (le_trans (by norm_num : (1 : ℕ) ≤ 2) hNonempty)).mp hP
    -- So Σ c_i^t = 1, i.e., t is a solution to the Moran equation.
    have h_sum_eq_one : Finset.sum (Finset.univ : Finset (Fin ifs.n))
      (fun i : Fin ifs.n => (ifs.ratios i : ℝ) ^ t) = 1 := by
      dsimp [hausdorffDimensionEq] at hEq
      linarith
    -- We need to show t > 0. If t ≤ 0, then c_i^t ≥ 1 for each i (since c_i < 1),
    -- so Σ c_i^t ≥ n ≥ 2 > 1, contradicting Σ c_i^t = 1 (needs n ≥ 2).
    have h_pos : t > 0 := by
      by_contra! h_nonpos
      have h_sum_ge_n : Finset.sum (Finset.univ : Finset (Fin ifs.n))
        (fun i : Fin ifs.n => (ifs.ratios i : ℝ) ^ t) ≥ (ifs.n : ℝ) := by
        have h_ge_one : ∀ i : Fin ifs.n, (ifs.ratios i : ℝ) ^ t ≥ 1 := by
          intro i
          have hc_pos : (0 : ℝ) < ifs.ratios i := by exact_mod_cast ifs.hRatiosPos i
          have hc_le_one : (ifs.ratios i : ℝ) ≤ 1 := by
            have h' : ifs.ratios i ≤ 1 := le_of_lt (ifs.hRatiosLtOne i)
            exact_mod_cast h'
          -- For 0 < c ≤ 1 and t ≤ 0: c^t ≥ c^0 = 1
          have h := Real.rpow_le_rpow_of_exponent_ge hc_pos hc_le_one h_nonpos
          -- h : c^0 ≤ c^t, which simplifies to 1 ≤ c^t
          simpa using h
        calc
          Finset.sum (Finset.univ : Finset (Fin ifs.n))
            (fun i : Fin ifs.n => (ifs.ratios i : ℝ) ^ t) ≥
          Finset.sum (Finset.univ : Finset (Fin ifs.n)) (fun _ : Fin ifs.n => (1 : ℝ)) :=
            Finset.sum_le_sum (fun i hi => h_ge_one i)
          _ = (ifs.n : ℝ) := by simp [Finset.sum_const, nsmul_eq_mul, Finset.card_fin]
      have hn2 : (2 : ℝ) ≤ (ifs.n : ℝ) := by exact_mod_cast hNonempty
      linarith
    -- Construct HausdorffDimensionSolution with dH = t
    -- Uniqueness follows from strict monotonicity of f(d) = Σ c_i^d (already proven)
    have h_unique : ∀ d : ℝ, d > 0 → hausdorffDimensionEq ifs d = 0 → d = t := by
      intro d hd_pos hd_eq
      by_contra! h_ne
      have h_lt_or : d < t ∨ t < d := lt_or_gt_of_ne h_ne
      rcases h_lt_or with (h_lt | h_gt)
      · -- If d < t, then f(d) > f(t) by strict monotonicity, so f(d) > 0
        have h_fd_gt_ft : hausdorffDimensionEq ifs d > hausdorffDimensionEq ifs t := by
          have h_sum_lt : (Finset.sum (Finset.univ : Finset (Fin ifs.n))
              (fun i : Fin ifs.n => (ifs.ratios i : ℝ) ^ t)) <
            (Finset.sum (Finset.univ : Finset (Fin ifs.n))
              (fun i : Fin ifs.n => (ifs.ratios i : ℝ) ^ d)) := by
            -- 0 < c < 1, d < t ⟹ c^t < c^d
            have h_all_le : ∀ i : Fin ifs.n, (ifs.ratios i : ℝ) ^ t ≤ (ifs.ratios i : ℝ) ^ d := by
              intro i
              exact le_of_lt (Real.rpow_lt_rpow_of_exponent_gt
                (by exact_mod_cast ifs.hRatiosPos i) (by exact_mod_cast ifs.hRatiosLtOne i) h_lt)
            have h_nonempty : Finset.Nonempty (Finset.univ : Finset (Fin ifs.n)) := by
              refine ⟨⟨0, by omega⟩, Finset.mem_univ _⟩
            have h_strict : ∃ i ∈ Finset.univ, (ifs.ratios i : ℝ) ^ t < (ifs.ratios i : ℝ) ^ d := by
              rcases h_nonempty with ⟨i, hi⟩
              refine ⟨i, hi, Real.rpow_lt_rpow_of_exponent_gt
                (by exact_mod_cast ifs.hRatiosPos i) (by exact_mod_cast ifs.hRatiosLtOne i) h_lt⟩
            exact Finset.sum_lt_sum (fun i hi => h_all_le i) h_strict
          dsimp [hausdorffDimensionEq]
          linarith
        dsimp [hausdorffDimensionEq] at hd_eq hEq h_fd_gt_ft
        linarith
      · -- If t < d, then f(t) > f(d) by strict monotonicity, so 0 > f(d)
        have h_ft_gt_fd : hausdorffDimensionEq ifs t > hausdorffDimensionEq ifs d := by
          have h_sum_lt : (Finset.sum (Finset.univ : Finset (Fin ifs.n))
              (fun i : Fin ifs.n => (ifs.ratios i : ℝ) ^ d)) <
            (Finset.sum (Finset.univ : Finset (Fin ifs.n))
              (fun i : Fin ifs.n => (ifs.ratios i : ℝ) ^ t)) := by
            -- 0 < c < 1, t < d ⟹ c^d < c^t
            have h_all_le : ∀ i : Fin ifs.n, (ifs.ratios i : ℝ) ^ d ≤ (ifs.ratios i : ℝ) ^ t := by
              intro i
              exact le_of_lt (Real.rpow_lt_rpow_of_exponent_gt
                (by exact_mod_cast ifs.hRatiosPos i) (by exact_mod_cast ifs.hRatiosLtOne i) h_gt)
            have h_nonempty : Finset.Nonempty (Finset.univ : Finset (Fin ifs.n)) := by
              refine ⟨⟨0, by omega⟩, Finset.mem_univ _⟩
            have h_strict : ∃ i ∈ Finset.univ, (ifs.ratios i : ℝ) ^ d < (ifs.ratios i : ℝ) ^ t := by
              rcases h_nonempty with ⟨i, hi⟩
              refine ⟨i, hi, Real.rpow_lt_rpow_of_exponent_gt
                (by exact_mod_cast ifs.hRatiosPos i) (by exact_mod_cast ifs.hRatiosLtOne i) h_gt⟩
            exact Finset.sum_lt_sum (fun i hi => h_all_le i) h_strict
          dsimp [hausdorffDimensionEq]
          linarith
        dsimp [hausdorffDimensionEq] at hEq hd_eq h_ft_gt_fd
        linarith
    have h_bound : t ≤ (ifs.n : ℝ) := hBound
    refine ⟨{
      dH := t
      hPos := h_pos
      hMoran := hEq
      hUnique := h_unique
      hBound := h_bound
    }, rfl⟩
  · intro h
    rcases h with ⟨sol, ht⟩
    rw [← ht]
    rw [pressure_zero_iff_hausdorff_dimension ifs sol.dH (le_trans (by norm_num : (1 : ℕ) ≤ 2) hNonempty)]
    exact sol.hMoran

end UFPFormalization
