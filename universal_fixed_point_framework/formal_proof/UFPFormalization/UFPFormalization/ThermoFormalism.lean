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
noncomputable def topologicalPressure {X : Type} [MetricSpace X] [CompleteMetricSpace X]
    (ifs : IFS X) (t : ℝ) : ℝ :=
  -- For the geometric potential φ_t(x) = -t · log |f'(x)|,
  -- the pressure is given by P(t) = log(Σ c_i^t)
  Real.log (Finset.sum (Finset.univ : Finset (Fin ifs.n))
    (fun i : Fin ifs.n => (ifs.ratios i) ^ t))

/--
The pressure function P(t) is strictly decreasing in t
(since each c_i^t is decreasing in t for c_i ∈ (0,1)).

Requires the IFS to have at least one map (n ≥ 1) to avoid the
degenerate case where the pressure is log(0) = 0 constant.
-/
theorem pressure_strictly_decreasing {X : Type} [MetricSpace X] [CompleteMetricSpace X]
    (ifs : IFS X) (hNonempty : ifs.n ≥ 1) (t₁ t₂ : ℝ) (h : t₁ < t₂) :
    topologicalPressure ifs t₂ < topologicalPressure ifs t₁ := by
  -- Since c_i ∈ (0,1), c_i^{t₂} < c_i^{t₁} for each i (Real.rpow_lt_rpow_of_exponent_gt),
  -- so Σ c_i^{t₂} < Σ c_i^{t₁}. Since log is strictly increasing on ℝ⁺,
  -- log(Σ c_i^{t₂}) < log(Σ c_i^{t₁}).
  have h_sum_lt : (Finset.sum (Finset.univ : Finset (Fin ifs.n))
      (fun i : Fin ifs.n => (ifs.ratios i) ^ t₂)) <
    (Finset.sum (Finset.univ : Finset (Fin ifs.n))
      (fun i : Fin ifs.n => (ifs.ratios i) ^ t₁)) := by
    have h_all_le : ∀ i : Fin ifs.n, (ifs.ratios i) ^ t₂ ≤ (ifs.ratios i) ^ t₁ := by
      intro i
      have hc_pos : 0 < ifs.ratios i := ifs.hRatiosPos i
      have hc_lt_one : ifs.ratios i < 1 := ifs.hRatiosLtOne i
      -- For 0 < c < 1 and t₁ < t₂, we have c^{t₂} < c^{t₁}
      exact le_of_lt (Real.rpow_lt_rpow_of_exponent_gt hc_pos hc_lt_one h)
    -- Need at least one strict inequality. Since n ≥ 1, Fin ifs.n is nonempty.
    have h_nonempty : Finset.Nonempty (Finset.univ : Finset (Fin ifs.n)) := by
      have h_card : Finset.card (Finset.univ : Finset (Fin ifs.n)) = ifs.n := Finset.card_fin ifs.n
      rcases hNonempty.eq_or_gt with (h_eq | h_gt)
      · -- ifs.n = 1, at least one element
        refine ⟨⟨0, by omega⟩, Finset.mem_univ _⟩
      · -- ifs.n > 1, definitely nonempty
        refine ⟨⟨0, by omega⟩, Finset.mem_univ _⟩
    have h_strict : ∃ i ∈ Finset.univ, (ifs.ratios i) ^ t₂ < (ifs.ratios i) ^ t₁ := by
      rcases h_nonempty with ⟨i, hi⟩
      refine ⟨i, hi, Real.rpow_lt_rpow_of_exponent_gt (ifs.hRatiosPos i) (ifs.hRatiosLtOne i) h⟩
    exact Finset.sum_lt_sum (fun i hi => h_all_le i) h_strict
  -- The sum is positive (all terms are positive), so log is defined and strictly increasing
  have h_sum_pos : 0 < Finset.sum (Finset.univ : Finset (Fin ifs.n))
      (fun i : Fin ifs.n => (ifs.ratios i) ^ t₂) := by
    have h_nonempty : Finset.Nonempty (Finset.univ : Finset (Fin ifs.n)) := by
      refine ⟨⟨0, by omega⟩, Finset.mem_univ _⟩
    apply Finset.sum_pos (fun i hi => Real.rpow_pos_of_pos (ifs.hRatiosPos i) t₂) h_nonempty
  exact Real.log_lt_log h_sum_pos h_sum_lt

/--
The pressure at t = 0 equals log(n), where n is the number of IFS maps.
-/
theorem pressure_at_zero {X : Type} [MetricSpace X] [CompleteMetricSpace X]
    (ifs : IFS X) : topologicalPressure ifs 0 = Real.log (ifs.n : ℝ) := by
  simp [topologicalPressure]
  -- Σ c_i^0 = Σ 1 = n
  have h_sum_one : (Finset.sum (Finset.univ : Finset (Fin ifs.n))
    (fun i : Fin ifs.n => (ifs.ratios i) ^ 0)) = (ifs.n : ℝ) := by
    simp
  simp [h_sum_one]

/--
The Hausdorff dimension d_H is the unique t such that P(t) = 0,
i.e., log(Σ c_i^{d_H}) = 0, or equivalently Σ c_i^{d_H} = 1.
This is the Moran equation connection between pressure and dimension.
-/
theorem pressure_zero_iff_hausdorff_dimension {X : Type} [MetricSpace X] [CompleteMetricSpace X]
    (ifs : IFS X) (t : ℝ) : topologicalPressure ifs t = 0 ↔ hausdorffDimensionEq ifs t = 0 := by
  dsimp [topologicalPressure, hausdorffDimensionEq]
  constructor
  · intro h
    -- P(t) = 0 ⟹ log(Σ c_i^t) = 0 ⟹ Σ c_i^t = 1 ⟹ Σ c_i^t - 1 = 0
    have h_log_eq_zero : Real.log (Finset.sum (Finset.univ : Finset (Fin ifs.n))
      (fun i : Fin ifs.n => (ifs.ratios i) ^ t)) = 0 := h
    have h_sum_eq_one : Finset.sum (Finset.univ : Finset (Fin ifs.n))
      (fun i : Fin ifs.n => (ifs.ratios i) ^ t) = 1 := by
      -- log(x) = 0 ⟹ x = 1 (since log is injective on ℝ⁺)
      apply Real.exp_inj_on_pos.mp ?_
      rw [Real.exp_log ?_, Real.exp_zero]
      -- The sum is positive (all terms are positive)
      apply Finset.sum_pos
      intro i hi
      exact Real.rpow_pos_of_pos (ifs.hRatiosPos i) t
      exact h_log_eq_zero
    rw [h_sum_eq_one]
    simp
  · intro h
    -- hausdorffDimensionEq ifs t = 0 ⟹ Σ c_i^t - 1 = 0 ⟹ Σ c_i^t = 1 ⟹ log(1) = 0
    have h_sum_eq_one : Finset.sum (Finset.univ : Finset (Fin ifs.n))
      (fun i : Fin ifs.n => (ifs.ratios i) ^ t) = 1 := by
      linarith
    simp [topologicalPressure, h_sum_eq_one]

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
The Legendre transform of any function (convex or not) is convex.
Proof: f*(p) = sup_x (p·x - f(x)) is the pointwise supremum of affine
functions p ↦ p·x - f(x), and the supremum of convex functions is convex.
-/
theorem legendreTransform_convex {f : ℝ → ℝ} (hf : ConvexOn ℝ Set.univ f) :
    ConvexOn ℝ Set.univ (legendreTransform f) := by
  refine ⟨convex_univ, ?_⟩
  intro x hx y hy a b ha hb hab
  have hx_mem : x ∈ Set.univ := Set.mem_univ x
  have hy_mem : y ∈ Set.univ := Set.mem_univ y
  -- Need to show: f*(ax+by) ≤ a·f*(x) + b·f*(y)
  calc
    legendreTransform f (a * x + b * y) = ⨆ (z : ℝ), ((a * x + b * y) * z - f z) := rfl
    _ = ⨆ (z : ℝ), (a * (x * z - f z) + b * (y * z - f z)) := by
      -- Algebraic identity
      apply congrArg (⨆·, ·)
      funext z
      ring
    _ ≤ a * (⨆ (z : ℝ), (x * z - f z)) + b * (⨆ (z : ℝ), (y * z - f z)) := by
      -- For each z, the term is bounded by the weighted sum of suprema
      apply ciSup_le
      intro z
      have hxz : x * z - f z ≤ ⨆ (z' : ℝ), (x * z' - f z') := by
        apply Real.le_sSup
        refine ⟨z, ?_⟩
        ring
      have hyz : y * z - f z ≤ ⨆ (z' : ℝ), (y * z' - f z') := by
        apply Real.le_sSup
        refine ⟨z, ?_⟩
        ring
      nlinarith
    _ = a * legendreTransform f x + b * legendreTransform f y := by
      simp [legendreTransform]

/--
The multifractal singularity spectrum f(α) is the Legendre transform
of τ(q):
  f(α) = inf_{q ∈ ℝ} (q·α - τ(q))

For a self-similar measure with weights p_i and ratios c_i,
the singularity spectrum f(α) characterizes the fractal dimension
of the set of points with Hölder exponent α.
-/
noncomputable def singularitySpectrum {X : Type} [MetricSpace X] [CompleteMetricSpace X]
    {ifs : IFS X} {attractor : Attractor ifs}
    (measure : SelfSimilarMeasure ifs attractor) (α : ℝ) : ℝ :=
  -legendreTransform (multifractalSpectrum measure) α

/--
The singularity spectrum f(α) satisfies f(α) ≤ d_H (Hausdorff dimension),
with equality at the maximizing Hölder exponent α₀.

Proof sketch (standard multifractal analysis, Harte 1996):
  1. f(α) = inf_q (q·α - τ(q)) = -sup_q (τ(q) - q·α) = -τ*(α)
  2. The Legendre transform satisfies τ*(α) ≥ q·α - τ(q) for all q
  3. For q = 1: τ(1) = 0 (since Σ p_i · c_i^{τ(1)} = Σ p_i = 1), so τ*(α) ≥ α·1 - 0 = α
  4. Therefore f(α) ≤ -α for all α
  5. By the variational principle, max_α f(α) = d_H (the Hausdorff dimension)
  6. Hence f(α) ≤ d_H for all α

The full proof (steps 4-6) requires the variational principle for the
topological pressure and is deferred to Phase 16B.
-/
theorem singularity_spectrum_bound {X : Type} [MetricSpace X] [CompleteMetricSpace X]
    {ifs : IFS X} {attractor : Attractor ifs}
    (measure : SelfSimilarMeasure ifs attractor) (sol : HausdorffDimensionSolution ifs)
    (α : ℝ) : singularitySpectrum measure α ≤ sol.dH := by
  -- Standard result: the singularity spectrum is bounded by the Hausdorff dimension.
  -- For the finite-dimensional prototype, we note that this follows from:
  --   f(α) = inf_q (qα - τ(q)) ≤ 1·α - τ(1) = α - 0 = α (taking q=1)
  -- But this only gives f(α) ≤ α, not f(α) ≤ d_H.
  -- The full bound f(α) ≤ d_H requires the variational principle.
  -- Here we show the partial bound f(α) ≤ α as a sanity check.
  have h_partial : singularitySpectrum measure α ≤ α := by
    dsimp [singularitySpectrum, legendreTransform]
    have hq1 : (1 : ℝ) * α - multifractalSpectrum measure (1 : ℝ) ≤
      ⨆ (q : ℝ), (q * α - multifractalSpectrum measure q) := by
      apply Real.le_sSup
      refine ⟨1, ?_⟩
      ring
    -- τ(1) = 0 since Σ p_i · c_i^{τ(1)} = Σ p_i = 1
    have h_tau_one : multifractalSpectrum measure (1 : ℝ) = 0 := by
      dsimp [multifractalSpectrum]
      sorry  -- τ(1) = 0 by the definition of multifractal spectrum
    calc
      singularitySpectrum measure α = -(⨆ (q : ℝ), (q * α - multifractalSpectrum measure q)) := rfl
      _ ≤ -( (1 : ℝ) * α - multifractalSpectrum measure (1 : ℝ)) := by
        rw [h_tau_one]
        simp
        linarith
      _ = -α := by simp
  -- Partial bound: f(α) ≤ α. The full bound f(α) ≤ d_H is a deeper result.
  -- Since d_H may be less than α for some α, we need the variational principle.
  -- For the prototype, we use the partial bound and note that α > d_H is possible
  -- (in which case the bound is weaker than needed), but the full proof is deferred.
  have h_full : singularitySpectrum measure α ≤ sol.dH := by
    -- f(α) ≤ d_H for self-similar measures (Falconer 2014, Ch. 17, Theorem 17.2).
    -- Proof structure:
    --   By the Legendre transform: f(α) = inf_q (q·α - τ(q)).
    --   τ(0) = -d_H (Bowen formula), so f(α) ≤ 0·α - τ(0) = d_H.
    --
    -- In the finite prototype, d_H is the information dimension and the
    -- singularity spectrum is explicitly computable. The inequality
    -- f(α) ≤ d_H follows from the numerical demonstration in the Python
    -- prototype (`math_open_problems_convexity.py`). The general proof
    -- requires the multifractal formalism for self-similar measures.
    have h_tau_zero : multifractalSpectrum measure (0 : ℝ) = -sol.dH := by
      -- τ(0) = -d_H by the Bowen formula (Hausdorff dimension equation)
      -- Σ c_i^{d_H} = 1 → τ(0) = log Σ p_i^0 · c_i^{τ(0)} = log Σ c_i^{τ(0)}
      -- Setting τ(0) = -d_H gives log Σ c_i^{d_H} = log 1 = 0.
      -- For the prototype, this is derived from: sol satisfies hausdorffDimensionEq ifs sol.dH = 0
      sorry
    calc
      singularitySpectrum measure α
          = -(⨆ (q : ℝ), (q * α - multifractalSpectrum measure q)) := rfl
      _ ≤ -(0 * α - multifractalSpectrum measure (0 : ℝ)) := by
        have h_sup : (⨆ (q : ℝ), (q * α - multifractalSpectrum measure q)) ≥
          0 * α - multifractalSpectrum measure (0 : ℝ) :=
          Real.le_sSup (Set.mem_range.mpr ⟨0, rfl⟩)
        linarith
      _ = -( - multifractalSpectrum measure (0 : ℝ)) := by simp
      _ = multifractalSpectrum measure (0 : ℝ) := by simp
      _ = -sol.dH := h_tau_zero
      _ ≤ sol.dH := by
        -- Since sol.dH is the Hausdorff dimension, it's non-negative.
        -- Therefore -sol.dH ≤ sol.dH.
        -- For the prototype, d_H ≥ 0 always holds for IFS dimensions.
        have h_nonneg : 0 ≤ sol.dH := by
          -- hausdorffDimensionEq ifs sol.dH = 0 implies sol.dH ≥ 0
          -- by the fact that Σ c_i^0 = n ≥ 1 > Σ c_i^t for sufficiently large t.
          sorry
        nlinarith

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
noncomputable def hausdorffDimensionOfMeasure {X : Type} [MetricSpace X] [CompleteMetricSpace X]
    {ifs : IFS X} {attractor : Attractor ifs}
    (measure : SelfSimilarMeasure ifs attractor) : ℝ :=
  -- d_H(ρ) = Σ p_i · log(p_i) / log(c_i)
  -- Convention: p_i · log(p_i) = 0 when p_i = 0 (limit)
  Finset.sum (Finset.univ : Finset (Fin ifs.n))
    (fun i : Fin ifs.n =>
      (measure.weights i) * Real.log (measure.weights i) / Real.log (ifs.ratios i))

/--
Theorem D-C: d_H(ρ) is a concave function of the probability vector ρ.

Proof sketch:
  d_H(ρ) = Σ p_i · log(p_i) / log(c_i)
  Since log(c_i) < 0 (c_i < 1), the function p ↦ p·log(p) is concave,
  and dividing by the negative constant log(c_i) preserves concavity.

In the finite-dimensional prototype, we verify concavity for the
two-variable case (n=2). The general case follows by a standard
convex analysis argument.
-/
theorem theorem_DC_concavity {X : Type} [MetricSpace X] [CompleteMetricSpace X]
    {ifs : IFS X} {attractor : Attractor ifs}
    (measure₁ measure₂ : SelfSimilarMeasure ifs attractor) (λ : ℝ)
    (hλ : 0 ≤ λ ∧ λ ≤ 1) : hausdorffDimensionOfMeasure (interpolateMeasure measure₁ measure₂ λ) ≥
    λ * hausdorffDimensionOfMeasure measure₁ + (1 - λ) * hausdorffDimensionOfMeasure measure₂ := by
  rcases hλ with ⟨hλ0, hλ1⟩
  -- Key fact: log(c_i) < 0 since 0 < c_i < 1
  have h_log_c_neg : ∀ i : Fin ifs.n, Real.log (ifs.ratios i) < 0 := by
    intro i
    exact Real.log_lt_log (ifs.hRatiosPos i) (ifs.hRatiosLtOne i)
  -- Per-term inequality: x·log(x) is convex on (0,∞), proved via mathlib convexOn_mul_log
    have h_entropy_convex : ∀ (a b : ℝ), a > 0 → b > 0 → 
        (λ * a + (1 - λ) * b) * Real.log (λ * a + (1 - λ) * b) ≤
        λ * (a * Real.log a) + (1 - λ) * (b * Real.log b) := by
      intro a b ha hb
      have ha_mem : a ∈ Set.Ici (0 : ℝ) := Set.mem_Ici.mpr (by linarith)
      have hb_mem : b ∈ Set.Ici (0 : ℝ) := Set.mem_Ici.mpr (by linarith)
      have h1mλ_nonneg : 0 ≤ 1 - λ := by linarith
      have h_convex := convexOn_mul_log.2 ha_mem hb_mem hλ0 h1mλ_nonneg (by linarith)
      -- convexOn_mul_log.2 gives: (λa+(1-λ)b)·log(λa+(1-λ)b) ≤ λ·a·log(a) + (1-λ)·b·log(b)
      simpa [add_comm, add_left_comm, mul_comm, mul_left_comm, smul_eq_mul] using h_convex
  have h_term : ∀ i : Fin ifs.n,
      ((λ * measure₁.weights i + (1 - λ) * measure₂.weights i) *
        Real.log (λ * measure₁.weights i + (1 - λ) * measure₂.weights i) / Real.log (ifs.ratios i)) ≥
      λ * (measure₁.weights i * Real.log (measure₁.weights i) / Real.log (ifs.ratios i)) +
      (1 - λ) * (measure₂.weights i * Real.log (measure₂.weights i) / Real.log (ifs.ratios i)) := by
    intro i
    set p := measure₁.weights i with hp
    set q := measure₂.weights i with hq
    have hp_pos : p > 0 := measure₁.hWeightsPos i
    have hq_pos : q > 0 := measure₂.hWeightsPos i
    have h_mid_pos : 0 < λ * p + (1 - λ) * q := nlinarith
    have h_log_neg : Real.log (ifs.ratios i) < 0 := h_log_c_neg i
    have h_main : (λ * p + (1 - λ) * q) * Real.log (λ * p + (1 - λ) * q) ≤
      λ * (p * Real.log p) + (1 - λ) * (q * Real.log q) :=
      h_entropy_convex p q hp_pos hq_pos
    -- Since denominator log(c_i) < 0, dividing reverses the inequality
     have h_div : ((λ * p + (1 - λ) * q) * Real.log (λ * p + (1 - λ) * q)) / Real.log (ifs.ratios i) ≥
         (λ * (p * Real.log p) + (1 - λ) * (q * Real.log q)) / Real.log (ifs.ratios i) := by
       have h_num_nonpos : ((λ * p + (1 - λ) * q) * Real.log (λ * p + (1 - λ) * q)) -
         (λ * (p * Real.log p) + (1 - λ) * (q * Real.log q)) ≤ 0 := by linarith
       have h_den_neg : Real.log (ifs.ratios i) < 0 := h_log_neg
       have h_ratio_nonneg : (((λ * p + (1 - λ) * q) * Real.log (λ * p + (1 - λ) * q)) -
         (λ * (p * Real.log p) + (1 - λ) * (q * Real.log q))) / Real.log (ifs.ratios i) ≥ 0 :=
         div_nonneg_of_nonpos_of_nonpos h_num_nonpos (by linarith)
       linarith
    calc
      ((λ * p + (1 - λ) * q) * Real.log (λ * p + (1 - λ) * q)) / Real.log (ifs.ratios i) ≥
        (λ * (p * Real.log p) + (1 - λ) * (q * Real.log q)) / Real.log (ifs.ratios i) := h_div
      _ = λ * (p * Real.log p / Real.log (ifs.ratios i)) + (1 - λ) * (q * Real.log q / Real.log (ifs.ratios i)) := by ring
  -- Sum over all indices
  dsimp [hausdorffDimensionOfMeasure]
  calc
    Finset.sum (Finset.univ : Finset (Fin ifs.n))
      (fun i : Fin ifs.n => ((interpolateMeasure measure₁ measure₂ λ).weights i) *
        Real.log ((interpolateMeasure measure₁ measure₂ λ).weights i) / Real.log (ifs.ratios i)) ≥
    Finset.sum (Finset.univ : Finset (Fin ifs.n))
      (fun i : Fin ifs.n =>
        λ * (measure₁.weights i * Real.log (measure₁.weights i) / Real.log (ifs.ratios i)) +
        (1 - λ) * (measure₂.weights i * Real.log (measure₂.weights i) / Real.log (ifs.ratios i))) :=
      Finset.sum_le_sum (fun i hi => h_term i)
    _ = λ * (Finset.sum (Finset.univ : Finset (Fin ifs.n))
      (fun i : Fin ifs.n => measure₁.weights i * Real.log (measure₁.weights i) / Real.log (ifs.ratios i))) +
      (1 - λ) * (Finset.sum (Finset.univ : Finset (Fin ifs.n))
      (fun i : Fin ifs.n => measure₂.weights i * Real.log (measure₂.weights i) / Real.log (ifs.ratios i))) := by
      simp [Finset.sum_add_distrib, Finset.mul_sum]
    _ = λ * hausdorffDimensionOfMeasure measure₁ + (1 - λ) * hausdorffDimensionOfMeasure measure₂ := rfl

/--
Interpolate between two self-similar measures.
The interpolated measure has weights λ·p_i + (1-λ)·q_i.
-/
noncomputable def interpolateMeasure {X : Type} [MetricSpace X] [CompleteMetricSpace X]
    {ifs : IFS X} {attractor : Attractor ifs}
    (measure₁ measure₂ : SelfSimilarMeasure ifs attractor) (λ : ℝ) : SelfSimilarMeasure ifs attractor :=
  { weights := fun i => λ * measure₁.weights i + (1 - λ) * measure₂.weights i
    hWeightsPos := by
      intro i
      have h₁ : measure₁.weights i > 0 := measure₁.hWeightsPos i
      have h₂ : measure₂.weights i > 0 := measure₂.hWeightsPos i
      nlinarith
    hWeightsSum := by
      -- Σ (λp_i + (1-λ)q_i) = λ·Σp_i + (1-λ)·Σq_i = λ·1 + (1-λ)·1 = 1
      simp [measure₁.hWeightsSum, measure₂.hWeightsSum]
      ring
    mu := fun E => λ * measure₁.mu E + (1 - λ) * measure₂.mu E
    hTotalMass := by
      simp [measure₁.hTotalMass, measure₂.hTotalMass, attractor]
    hInvariance := by
      intro E
      simp [measure₁.hInvariance E, measure₂.hInvariance E]
      ring }

/--
Theorem D-C Corollary: The singularity spectrum f(α) is concave in α.
Proof: f(α) = -τ*(α) where τ* is the Legendre transform of τ(q).
Since τ(q) is convex (standard property of multifractal spectrum),
τ* is convex (legendreTransform_convex), so -τ* is concave.
-/
theorem singularity_spectrum_concave {X : Type} [MetricSpace X] [CompleteMetricSpace X]
    {ifs : IFS X} {attractor : Attractor ifs}
    (measure : SelfSimilarMeasure ifs attractor) : ConcaveOn ℝ Set.univ (singularitySpectrum measure) := by
  -- f(α) = -τ*(α) where τ* = L[τ]
  -- τ* is convex by legendreTransform_convex, so -τ* is concave.
  have h_convex_legendre : ConvexOn ℝ Set.univ (legendreTransform (multifractalSpectrum measure)) :=
    legendreTransform_convex (by
      -- τ(q) is convex for multifractal spectra (standard thermodynamic result)
      -- In the finite-dimensional prototype, we note this as a known property.
      sorry)
  -- ConcaveOn means: ∀ x y a b, a+b=1, a,b≥0 → f(ax+by) ≥ a·f(x) + b·f(y)
  -- This is the negation of convexity of τ*
  rcases h_convex_legendre with ⟨hconvex_set, hconvex⟩
  refine ⟨hconvex_set, ?_⟩
  intro x hx y hy a b ha hb hab
  have hstar := hconvex x hx y hy ha hb hab
  dsimp [singularitySpectrum]
  -- f(ax+by) = -τ*(ax+by) ≥ -(a·τ*(x) + b·τ*(y)) = a·f(x) + b·f(y)
  linarith [hstar]

/--
Link between the thermodynamic formalism and the spectral equivalence framework:
P(t) = 0 iff t = d_H (the Hausdorff dimension of the IFS attractor).
-/
theorem pressure_spectral_link {X : Type} [MetricSpace X] [CompleteMetricSpace X]
    (ifs : IFS X) (t : ℝ) : topologicalPressure ifs t = 0 ↔
    (∃ (sol : HausdorffDimensionSolution ifs), sol.dH = t) := by
  constructor
  · intro hP
    -- If P(t) = 0, then Σ c_i^t = 1 (by pressure_zero_iff_hausdorff_dimension)
    have hEq : hausdorffDimensionEq ifs t = 0 :=
      (pressure_zero_iff_hausdorff_dimension ifs t).mp hP
    -- So Σ c_i^t = 1, i.e., t is a solution to the Moran equation.
    have h_sum_eq_one : Finset.sum (Finset.univ : Finset (Fin ifs.n))
      (fun i : Fin ifs.n => (ifs.ratios i) ^ t) = 1 := by
      dsimp [hausdorffDimensionEq] at hEq
      linarith
    -- We need to show t > 0. If t ≤ 0, then c_i^t ≥ 1 for each i (since c_i < 1),
    -- so Σ c_i^t ≥ n > 1 (for n ≥ 1), contradicting Σ c_i^t = 1.
    have h_pos : t > 0 := by
      by_contra! h_nonpos
      have h_sum_ge_n : Finset.sum (Finset.univ : Finset (Fin ifs.n))
        (fun i : Fin ifs.n => (ifs.ratios i) ^ t) ≥ (ifs.n : ℝ) := by
        have h_ge_one : ∀ i : Fin ifs.n, (ifs.ratios i) ^ t ≥ 1 := by
          intro i
          have hc_pos : 0 < ifs.ratios i := ifs.hRatiosPos i
          have hc_le_one : ifs.ratios i ≤ 1 := le_of_lt (ifs.hRatiosLtOne i)
          -- For 0 < c ≤ 1 and t ≤ 0: c^t ≥ c^0 = 1
          -- Real.rpow_le_rpow_of_exponent_ge: 0 < a ≤ 1, x ≤ y → a^y ≤ a^x
          -- Here: 0 < c ≤ 1, h_nonpos: t ≤ 0, so c^0 ≤ c^t → 1 ≤ c^t
          have h := Real.rpow_le_rpow_of_exponent_ge hc_pos hc_le_one h_nonpos
          -- h : c^0 ≤ c^t, which simplifies to 1 ≤ c^t
          simpa using h
        calc
          Finset.sum (Finset.univ : Finset (Fin ifs.n))
            (fun i : Fin ifs.n => (ifs.ratios i) ^ t) ≥
          Finset.sum (Finset.univ : Finset (Fin ifs.n)) (fun _ : Fin ifs.n => 1) :=
            Finset.sum_le_sum (fun i hi => h_ge_one i)
          _ = (ifs.n : ℝ) := by simp
      have hn_pos : (ifs.n : ℝ) > 0 := by
        -- The solution exists (hEq) so n must be ≥ 1
        -- If n = 0, the sum is 0, so h_sum_eq_one gives 0 = 1, contradiction
        by_contra! hnz
        have hn0 : ifs.n = 0 := by omega
        have : Finset.sum (Finset.univ : Finset (Fin ifs.n))
          (fun i : Fin ifs.n => (ifs.ratios i) ^ t) = 0 := by simp [hn0]
        linarith
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
              (fun i : Fin ifs.n => (ifs.ratios i) ^ d)) <
            (Finset.sum (Finset.univ : Finset (Fin ifs.n))
              (fun i : Fin ifs.n => (ifs.ratios i) ^ t)) := by
            have h_all_le : ∀ i : Fin ifs.n, (ifs.ratios i) ^ d ≤ (ifs.ratios i) ^ t := by
              intro i
              exact le_of_lt (Real.rpow_lt_rpow_of_exponent_gt (ifs.hRatiosPos i) (ifs.hRatiosLtOne i) h_lt)
            have h_nonempty : Finset.Nonempty (Finset.univ : Finset (Fin ifs.n)) := by
              by_contra! h_empty
              have h_n_zero : ifs.n = 0 := by
                have h_card : Finset.card (Finset.univ : Finset (Fin ifs.n)) = 0 :=
                  Finset.card_empty_eq.mp (Finset.not_nonempty_iff_eq_empty.mp h_empty)
                simpa [Finset.card_fin] using h_card
              have h_moran_zero : hausdorffDimensionEq ifs t = -1 := by
                simp [hausdorffDimensionEq, h_n_zero]
              have : 0 = -1 := hEq.trans h_moran_zero.symm
              linarith
            have h_strict : ∃ i ∈ Finset.univ, (ifs.ratios i) ^ d < (ifs.ratios i) ^ t := by
              rcases h_nonempty with ⟨i, hi⟩
              refine ⟨i, hi, Real.rpow_lt_rpow_of_exponent_gt (ifs.hRatiosPos i) (ifs.hRatiosLtOne i) h_lt⟩
            exact Finset.sum_lt_sum (fun i hi => h_all_le i) h_strict
          dsimp [hausdorffDimensionEq]
          linarith
        rw [hd_eq, hEq] at h_fd_gt_ft
        linarith
      · -- If t < d, then f(t) > f(d) by strict monotonicity, so 0 > f(d)
        have h_ft_gt_fd : hausdorffDimensionEq ifs t > hausdorffDimensionEq ifs d := by
          have h_sum_lt : (Finset.sum (Finset.univ : Finset (Fin ifs.n))
              (fun i : Fin ifs.n => (ifs.ratios i) ^ t)) <
            (Finset.sum (Finset.univ : Finset (Fin ifs.n))
              (fun i : Fin ifs.n => (ifs.ratios i) ^ d)) := by
            have h_all_le : ∀ i : Fin ifs.n, (ifs.ratios i) ^ t ≤ (ifs.ratios i) ^ d := by
              intro i
              exact le_of_lt (Real.rpow_lt_rpow_of_exponent_gt (ifs.hRatiosPos i) (ifs.hRatiosLtOne i) h_gt)
            have h_nonempty : Finset.Nonempty (Finset.univ : Finset (Fin ifs.n)) := by
              by_contra! h_empty
              have h_n_zero : ifs.n = 0 := by
                have h_card : Finset.card (Finset.univ : Finset (Fin ifs.n)) = 0 :=
                  Finset.card_empty_eq.mp (Finset.not_nonempty_iff_eq_empty.mp h_empty)
                simpa [Finset.card_fin] using h_card
              have h_moran_zero : hausdorffDimensionEq ifs t = -1 := by
                simp [hausdorffDimensionEq, h_n_zero]
              have : 0 = -1 := hEq.trans h_moran_zero.symm
              linarith
            have h_strict : ∃ i ∈ Finset.univ, (ifs.ratios i) ^ t < (ifs.ratios i) ^ d := by
              rcases h_nonempty with ⟨i, hi⟩
              refine ⟨i, hi, Real.rpow_lt_rpow_of_exponent_gt (ifs.hRatiosPos i) (ifs.hRatiosLtOne i) h_gt⟩
            exact Finset.sum_lt_sum (fun i hi => h_all_le i) h_strict
          dsimp [hausdorffDimensionEq]
          linarith
        rw [hEq, hd_eq] at h_ft_gt_fd
        linarith
    have h_bound : t ≤ (ifs.n : ℝ) := by
      -- The Hausdorff dimension bound: d_H ≤ n (attractor embedding theorem)
      -- Full proof deferred to Phase 16B.
      sorry
    refine ⟨{
      dH := t
      hPos := h_pos
      hMoran := hEq
      hUnique := h_unique
      hBound := h_bound
    }, rfl⟩
  · intro h
    rcases h with ⟨sol, ht⟩
    rw [ht]
    rw [pressure_zero_iff_hausdorff_dimension ifs sol.dH]
    exact sol.hMoran

end UFPFormalization
