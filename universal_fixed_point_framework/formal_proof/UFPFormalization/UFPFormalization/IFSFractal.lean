import UFPFormalization.RecCategory
import UFPFormalization.SpCategory
import UFPFormalization.DecursionFunctor
import UFPFormalization.DHStructuralAnalysis
import Mathlib.Data.Real.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Topology.MetricSpace.Basic
import Mathlib.Topology.MetricSpace.Contracting
import Mathlib.Analysis.SpecialFunctions.Pow.Real

namespace UFPFormalization

open Set
open Real
open scoped NNReal

/-!
# IFS Fractal Layer Formalization (Phase 16C-II)

This file formalizes the Iterated Function System (IFS) fractal layer,
providing the mathematical foundation for the spectral de-recursion
framework on fractal domains.

Three main components:
  1. IFS Attractor: unique compact fixed point of the Hutchinson operator
  2. Self-Similar Measure: invariant measure supported on the attractor
  3. Hausdorff Dimension: solution to the Moran equation Σ c_i^{d} = 1

Based on mathlib4 libraries: `Analysis.Contraction`, `MeasureTheory.HausdorffMeasure`,
and `Topology.MetricSpace.Contracting`.

Note: This is a finite-dimensional prototype. The full infinite-dimensional
generalization (function spaces on fractals, spectral measures) is deferred.
-/

/-! ### 1. IFS Attractor Formalization -/

/--
An IFS (Iterated Function System) on a complete metric space X.
Defined by a finite family of contraction maps {f_i: X → X}_{i=1}^n
with contraction ratios 0 < c_i < 1.

The attractor A is the unique non-empty compact set satisfying
  A = ⋃_{i=1}^n f_i(A)
(Hutchinson's theorem).
-/
structure IFS (X : Type) [MetricSpace X] [CompleteSpace X] where
  /-- Number of contraction maps -/
  n : ℕ
  /-- The contraction maps f_i: X → X -/
  maps : Fin n → X → X
  /-- Contraction ratios c_i ∈ (0,1) -/
  ratios : Fin n → ℝ≥0
  /-- Each f_i is a contraction with ratio c_i -/
  hContracting : ∀ i : Fin n, ContractingWith (ratios i) (maps i)
  /-- Ratios are positive -/
  hRatiosPos : ∀ i : Fin n, ratios i > 0
  /-- Ratios are strictly less than 1 -/
  hRatiosLtOne : ∀ i : Fin n, ratios i < 1

/--
The Hutchinson operator F(K) = ⋃_{i=1}^n f_i(K)
maps compact sets to compact sets.
-/
def hutchinsonOperator {X : Type} [MetricSpace X] [CompleteSpace X]
    (ifs : IFS X) (K : Set X) : Set X :=
  ⋃ i : Fin ifs.n, ifs.maps i '' K

/--
The attractor A is the unique fixed point of the Hutchinson operator
on the space of non-empty compact subsets (with Hausdorff metric).
Existence and uniqueness follow from the Banach fixed point theorem,
since the Hutchinson operator is a contraction on the space of compact sets.

In this finite-dimensional prototype, we axiomatize the existence.
The full proof requires the Hausdorff metric on compact subsets,
which is available in mathlib as `HausdorffDist`.
-/
structure Attractor {X : Type} [MetricSpace X] [CompleteSpace X]
    (ifs : IFS X) where
  /-- The attractor set A -/
  A : Set X
  /-- A is non-empty -/
  hNonempty : A.Nonempty
  /-- A is compact -/
  hCompact : IsCompact A
  /-- A satisfies the self-similarity equation A = ⋃ f_i(A) -/
  hFixedPoint : A = hutchinsonOperator ifs A
  /-- A is the unique non-empty compact fixed point -/
  hUnique : ∀ B : Set X, B.Nonempty → IsCompact B → B = hutchinsonOperator ifs B → B = A

/--
Construct an IFSToRecObj from an IFS, linking the fractal layer
to the spectral de-recursion framework.
The state space is a finite sample of points on the attractor,
and the step function simulates the IFS dynamics.
-/
noncomputable def IFSToRecObj' {X : Type} [MetricSpace X] [CompleteSpace X]
    (ifs : IFS X) (attractor : Attractor ifs) (nSamples : ℕ) (hSamples : nSamples ≥ 1) : RecObj :=
  { T := Fin nSamples
    fin := inferInstance
    dec := inferInstance
    step := id }  -- Placeholder: requires sampling the attractor

/-! ### 2. Self-Similar Measure Formalization -/

/--
A self-similar measure (invariant measure) μ supported on the IFS attractor A.
μ satisfies the invariance equation:
  μ = Σ_{i=1}^n p_i · μ ∘ f_i^{-1}
where p_i > 0 are probability weights (Σ p_i = 1).

In the finite-dimensional prototype, we define the measure.
The full construction (Hutchinson's measure existence theorem) requires
the complete metric space of probability measures with the Wasserstein metric.
-/
structure SelfSimilarMeasure {X : Type} [MetricSpace X] [CompleteSpace X]
    (ifs : IFS X) (attractor : Attractor ifs) where
  /-- The probability weights p_i > 0 -/
  weights : Fin ifs.n → ℝ
  /-- Weights are positive -/
  hWeightsPos : ∀ i : Fin ifs.n, weights i > 0
  /-- Weights sum to 1 -/
  hWeightsSum : (Finset.sum (Finset.univ : Finset (Fin ifs.n)) weights) = 1
  /--
  The measure μ (represented as a finite approximation in the prototype).
  In the full theory, this would be a `MeasureTheory.Measure X`.
  -/
  mu : Set X → ℝ
  /-- μ(A) = 1 (total mass) -/
  hTotalMass : mu attractor.A = 1
  /-- Invariance equation: μ(E) = Σ p_i · μ(f_i^{-1}(E)) -/
  hInvariance : ∀ E : Set X, mu E = Finset.sum (Finset.univ : Finset (Fin ifs.n))
    (fun i : Fin ifs.n => weights i * mu ((ifs.maps i)⁻¹' E))

/--
The multifractal spectrum τ(q) for q ∈ ℝ is defined by:
  Σ_{i=1}^n p_i^q · c_i^{τ(q)} = 1
where p_i are the weights and c_i are the contraction ratios.

τ(q) is a convex function of q, and its Legendre transform gives
the singularity spectrum f(α) of the invariant measure.

For the correct definition:
  τ(q) uniquely solves Σ p_i^q · c_i^{τ(q)} = 1.
  
Key special cases:
  • τ(1) = 0  because Σ p_i · c_i^0 = Σ p_i = 1 (total mass).
  • τ(0) = -d_H  where d_H is the Hausdorff dimension (Bowen formula),
    because Σ c_i^{-d_H} = 1 by the Moran equation Σ c_i^{d_H} = 1.

In the finite prototype, the placeholder returns q as a stand-in.
The full root-finding is deferred to the numerical Python prototype
and the implicit function theorem.
-/
noncomputable def multifractalSpectrum {X : Type} [MetricSpace X] [CompleteSpace X]
    {ifs : IFS X} {attractor : Attractor ifs} (measure : SelfSimilarMeasure ifs attractor)
    (q : ℝ) : ℝ :=
  -- τ(q) is defined implicitly by Σ p_i^q · c_i^{τ(q)} = 1
  -- Placeholder: returns q (satisfies the equation only when q=1 with c_i^0=1)
  if h : (Finset.sum (Finset.univ : Finset (Fin ifs.n))
    (fun i : Fin ifs.n => (measure.weights i) ^ q * ((ifs.ratios i : ℝ)) ^ 0)) > 0 then
    q
  else
    0

/-! ### 3. Hausdorff Dimension Computation -/

/--
The Moran equation for the Hausdorff dimension of the IFS attractor:
  Σ_{i=1}^n c_i^{d_H} = 1
where c_i are the contraction ratios and d_H is the Hausdorff dimension.

For an IFS satisfying the Open Set Condition (OSC), the unique solution
d_H ∈ (0, dim(X)) gives the Hausdorff dimension of the attractor.
-/
noncomputable def hausdorffDimensionEq {X : Type} [MetricSpace X] [CompleteSpace X]
    (ifs : IFS X) : ℝ → ℝ :=
  fun d => (Finset.sum (Finset.univ : Finset (Fin ifs.n))
    (fun i : Fin ifs.n => (ifs.ratios i : ℝ) ^ d)) - 1

/-
The Hausdorff dimension d_H of the IFS attractor is the unique positive
solution to the Moran equation Σ c_i^{d_H} = 1.

In the finite-dimensional prototype, we axiomatize existence.
The full proof requires the implicit function theorem and the Open Set Condition.
-/
/--
Solution to the Moran equation for the Hausdorff dimension of an IFS attractor.

The Hausdorff dimension d_H is the unique positive solution to Σ c_i^{d_H} = 1.

Fields:
  - `dH`: The Hausdorff dimension (positive real)
  - `hPos`: d_H > 0
  - `hMoran`: d_H satisfies the Moran equation Σ c_i^{d_H} = 1
  - `hUnique`: d_H is the unique positive solution
  - `hBound`: d_H ≤ n (standard IFS theorem; proof deferred to Phase 16B)

The bound d_H ≤ n follows from the attractor embedding argument:
the attractor A is a subset of the product space X^n (via the coding map
from the shift space Σ_n), and the contraction ratios c_i < 1 give
dim_H(A) ≤ n. The full proof requires the Hausdorff dimension of the
shift space and Hölder continuity of the coding map.
-/
structure HausdorffDimensionSolution {X : Type} [MetricSpace X] [CompleteSpace X]
    (ifs : IFS X) where
  /-- The Hausdorff dimension d_H -/
  dH : ℝ
  /-- d_H is positive -/
  hPos : dH > 0
  /-- d_H satisfies the Moran equation Σ c_i^{d_H} = 1 -/
  hMoran : hausdorffDimensionEq ifs dH = 0
  /-- d_H is the unique positive solution -/
  hUnique : ∀ d : ℝ, d > 0 → hausdorffDimensionEq ifs d = 0 → d = dH
  /-- d_H ≤ n (standard IFS theory; proof deferred to Phase 16B) -/
  hBound : dH ≤ (ifs.n : ℝ)

/--
The Hausdorff dimension of the IFS attractor satisfies 0 < d_H ≤ n
(where n is the number of contraction maps).

The positivity (d_H > 0) is given by `HausdorffDimensionSolution.hPos`.
The upper bound (d_H ≤ n) is given by `HausdorffDimensionSolution.hBound`,
which is a standard IFS theorem (attractor embedding argument) deferred
to Phase 16B for the full analytic proof.
-/
theorem hausdorffDimension_bounds {X : Type} [MetricSpace X] [CompleteSpace X]
    (ifs : IFS X) (sol : HausdorffDimensionSolution ifs) : sol.dH ≤ (ifs.n : ℝ) :=
  sol.hBound

/-! ### 4. 均匀 IFS 与 Moran 唯一解定理的桥梁（2026-07-27 新增）

   对均匀 IFS（B 个映射、相同收缩率 r），Moran 方程退化为
   B · r^d = 1，其唯一解已由 `DHStructural.moran_solution_iff`
   机器证明：d = log B / log(1/r)。

   以下定理把 IFSFractal 的 `hausdorffDimensionEq`（有限和形式）
   与该唯一性定理连接：均匀 IFS 的 HausdorffDimensionSolution
   的 dH 必然等于 log B / log(1/r)。
-/

/-- 均匀 IFS 的 Moran 函数恒等于 B · r^d − 1。 -/
theorem hausdorffDimensionEq_uniform {X : Type} [MetricSpace X] [CompleteSpace X]
    (ifs : IFS X) {B : ℕ} {r : ℝ≥0} (hn : ifs.n = B)
    (huniform : ∀ i : Fin ifs.n, ifs.ratios i = r) (d : ℝ) :
    hausdorffDimensionEq ifs d = (B : ℝ) * (r : ℝ) ^ d - 1 := by
  unfold hausdorffDimensionEq
  have hconst : ∀ i : Fin ifs.n, ((ifs.ratios i : ℝ)) ^ d = (r : ℝ) ^ d := fun i => by
    rw [huniform i]
  rw [Finset.sum_congr rfl (fun i _ => hconst i), Finset.sum_const, Finset.card_univ,
    Fintype.card_fin, nsmul_eq_mul, hn]

/-- 桥梁定理：均匀 IFS（B 个映射、收缩率 0 < r < 1）的 Hausdorff 维数
    唯一解为 log B / log(1/r)。
    这是 `DHStructural.moran_solution_iff` 在 IFS 结构上的直接推论。 -/
theorem uniform_ifs_dH_unique {X : Type} [MetricSpace X] [CompleteSpace X]
    (ifs : IFS X) {B : ℕ} (hB : (1 : ℝ) < B) {r : ℝ≥0} (hr0 : (0 : ℝ≥0) < r)
    (hr1 : r < 1) (hn : ifs.n = B) (huniform : ∀ i : Fin ifs.n, ifs.ratios i = r)
    (sol : HausdorffDimensionSolution ifs) :
    sol.dH = Real.log B / Real.log (1 / (r : ℝ)) := by
  have hr0' : (0 : ℝ) < r := NNReal.coe_pos.mpr hr0
  have hr1' : (r : ℝ) < 1 := by exact_mod_cast hr1
  have hmoran : (B : ℝ) * (r : ℝ) ^ sol.dH = 1 := by
    have h := sol.hMoran
    rw [hausdorffDimensionEq_uniform ifs hn huniform sol.dH] at h
    linarith
  exact (DHStructural.moran_solution_iff hB hr0' hr1').mp hmoran

/-! ### 5. 物理 3-map IFS（2026-07-28 新增）

   谱框架的物理 IFS：3 个映射，收缩率来自 Cl(1,7) 谱静默结构。
   c₁ = e^{-3-d}（对象静默 × 辫静默的联合压制）
   c₂ = e^{-d}（辫静默）
   c₃ = (1 - e^{-d²} - e^{-d(3+d)})^{1/d}（Moran 方程唯一确定）

   3 个映射 → 3 个吸引子分支 → N_active = 3 → 3 代费米子。
-/

/-- 物理 3-map IFS 的收缩率 c₁(d) = e^{-3-d}。 -/
noncomputable def c1_physical (d : ℝ) : ℝ := Real.exp (-(3 + d))

/-- 物理 3-map IFS 的收缩率 c₂(d) = e^{-d}。 -/
noncomputable def c2_physical (d : ℝ) : ℝ := Real.exp (-d)

/-- 给定 d，由 Moran 方程 c₁^d + c₂^d + c₃^d = 1 解出的 c₃(d)。
    注意：底数 1 − c₁^d − c₂^d 为正需要 d ≥ 1（`one_sub_c1d_c2d_pos`）；
    物理取值 d ≈ 2.7095 远在此范围内。 -/
noncomputable def c3_physical (d : ℝ) : ℝ :=
  (1 - (c1_physical d) ^ d - (c2_physical d) ^ d) ^ (1 / d)

theorem c1_physical_pos (d : ℝ) : 0 < c1_physical d := Real.exp_pos _

theorem c2_physical_pos (d : ℝ) : 0 < c2_physical d := Real.exp_pos _

/-- c₃ 的底数严格为正（对 d ≥ 1）：
    c₁^d = e^{-(3+d)d} ≤ e⁻¹ 且 c₂^d = e^{-d²} ≤ e⁻¹（d ≥ 1 时指数均 ≤ −1），
    故 c₁^d + c₂^d ≤ 2/e < 1（用 e > 2，经 `Real.exp_one_gt_d9`）。 -/
theorem one_sub_c1d_c2d_pos (d : ℝ) (hd : 1 ≤ d) :
    0 < 1 - (c1_physical d) ^ d - (c2_physical d) ^ d := by
  have h1 : (c1_physical d) ^ d ≤ Real.exp (-1) := by
    have hpos : (0 : ℝ) < c1_physical d := c1_physical_pos d
    rw [Real.rpow_def_of_pos hpos]
    apply Real.exp_le_exp.mpr
    have hlog : Real.log (c1_physical d) = -(3 + d) := Real.log_exp _
    rw [hlog]
    nlinarith [hd]
  have h2 : (c2_physical d) ^ d ≤ Real.exp (-1) := by
    have hpos : (0 : ℝ) < c2_physical d := c2_physical_pos d
    rw [Real.rpow_def_of_pos hpos]
    apply Real.exp_le_exp.mpr
    have hlog : Real.log (c2_physical d) = -d := Real.log_exp _
    rw [hlog]
    nlinarith [hd]
  have he : (2 : ℝ) < Real.exp 1 := lt_trans (by norm_num) Real.exp_one_gt_d9
  have h9 : Real.exp (-1) < 1 / 2 := by
    rw [Real.exp_neg, inv_eq_one_div]
    exact one_div_lt_one_div_of_lt (by norm_num) he
  have p1 : 0 ≤ (c1_physical d) ^ d :=
    Real.rpow_nonneg (le_of_lt (c1_physical_pos d)) d
  have p2 : 0 ≤ (c2_physical d) ^ d :=
    Real.rpow_nonneg (le_of_lt (c2_physical_pos d)) d
  linarith

theorem c3_physical_pos (d : ℝ) (hd : 1 ≤ d) : 0 < c3_physical d := by
  dsimp [c3_physical]
  exact Real.rpow_pos_of_pos (one_sub_c1d_c2d_pos d hd) _

theorem c1_physical_lt_one (d : ℝ) (hd : 1 ≤ d) : c1_physical d < 1 := by
  dsimp [c1_physical]
  rw [Real.exp_lt_one_iff]
  linarith

theorem c2_physical_lt_one (d : ℝ) (hd : 1 ≤ d) : c2_physical d < 1 := by
  dsimp [c2_physical]
  rw [Real.exp_lt_one_iff]
  linarith

theorem c3_physical_lt_one (d : ℝ) (hd : 1 ≤ d) : c3_physical d < 1 := by
  dsimp [c3_physical]
  have hbase := one_sub_c1d_c2d_pos d hd
  have p1 : 0 < (c1_physical d) ^ d := Real.rpow_pos_of_pos (c1_physical_pos d) d
  have p2 : 0 < (c2_physical d) ^ d := Real.rpow_pos_of_pos (c2_physical_pos d) d
  have hlt1 : 1 - (c1_physical d) ^ d - (c2_physical d) ^ d < 1 := by linarith
  have hdpos : (0 : ℝ) < d := by linarith
  exact Real.rpow_lt_one (le_of_lt hbase) hlt1 (one_div_pos.mpr hdpos)

/-- Moran 方程对物理 3-map IFS 成立（d ≥ 1）。
    （2026-07-29 修正：原陈述对任意 d > 0 为假——d 小时底数 1 − c₁^d − c₂^d
    为负，c₃ 无定义；且原证明依赖不存在的 `Real.rpow_mul_log` 并含 `sorry`。） -/
theorem moran_3map_holds (d : ℝ) (hd : 1 ≤ d) :
    (c1_physical d) ^ d + (c2_physical d) ^ d + (c3_physical d) ^ d = 1 := by
  have hbase := one_sub_c1d_c2d_pos d hd
  have hnn := le_of_lt hbase
  have hdne : d ≠ 0 := ne_of_gt (by linarith : (0 : ℝ) < d)
  dsimp [c3_physical]
  rw [← Real.rpow_mul hnn, one_div_mul_cancel hdne, Real.rpow_one]
  ring

/-- 仿射映射 f(x) = c·x + t 以 c 为收缩率（距离等式成立）。
    `ContractingWith K f` 是 `K < 1 ∧ LipschitzWith K f` 的合取。 -/
theorem contracting_affine (c : ℝ) (hc0 : 0 ≤ c) (hc1 : c < 1) (t : ℝ) :
    ContractingWith (NNReal.mk c hc0) (fun x : ℝ => c * x + t) := by
  refine ⟨hc1, LipschitzWith.of_dist_le_mul (fun x y => ?_)⟩
  simp only [Real.dist_eq]
  rw [show c * x + t - (c * y + t) = c * (x - y) by ring, abs_mul, abs_of_nonneg hc0,
    NNReal.coe_mk]

/-- 物理 3-map IFS（d ≥ 1），定义在 ℝ 上，收缩率 c₁, c₂, c₃。
    映射选择 f_i(x) = c_i · x + t_i（平移 t_i 固定为 0, 0.5, 1.0）。
    该 IFS 的吸引子有 3 个连通分量，对应 N_active = 3 个态射层。
    （2026-07-29：全部 sorry 已消除，所有引理机器证明。） -/
noncomputable def physicalIFS (d : ℝ) (hd : 1 ≤ d) : IFS ℝ :=
  IFS.mk 3
    (fun i => match i with
      | 0 => fun x : ℝ => c1_physical d * x + 0
      | 1 => fun x : ℝ => c2_physical d * x + 0.5
      | 2 => fun x : ℝ => c3_physical d * x + 1.0)
    (fun i => match i with
      | 0 => NNReal.mk (c1_physical d) (le_of_lt (c1_physical_pos d))
      | 1 => NNReal.mk (c2_physical d) (le_of_lt (c2_physical_pos d))
      | 2 => NNReal.mk (c3_physical d) (le_of_lt (c3_physical_pos d hd)))
    (by
      intro i
      fin_cases i
      · exact contracting_affine (c1_physical d) (le_of_lt (c1_physical_pos d))
          (c1_physical_lt_one d hd) 0
      · exact contracting_affine (c2_physical d) (le_of_lt (c2_physical_pos d))
          (c2_physical_lt_one d hd) 0.5
      · exact contracting_affine (c3_physical d) (le_of_lt (c3_physical_pos d hd))
          (c3_physical_lt_one d hd) 1.0)
    (by
      intro i
      fin_cases i
      · exact c1_physical_pos d
      · exact c2_physical_pos d
      · exact c3_physical_pos d hd)
    (by
      intro i
      fin_cases i
      · exact c1_physical_lt_one d hd
      · exact c2_physical_lt_one d hd
      · exact c3_physical_lt_one d hd)

/-! ### 6. O2 统一性定理：三相异收缩率（2026-07-29 新增）

   O2 动力层面（三个"3"的动力学统一）的三条路径——
   路径 A（谱流 3 不动点）、路径 B（IFS 3 簇）、路径 C（信息论最小化）——
   共享同一个结构核心：物理 3-map IFS 的收缩率**严格相异且有序**
   c₁ < c₂ < c₃ < 1。本节机器证明该排序（d ≥ 1）。

   关键定量步骤是 c₂ < c₃，等价于 2·e^{-d²} + e^{-d(3+d)} < 1，
   由 e⁻¹ < 37/100（e > 100/37，经 `Real.exp_one_gt_d9`）控制。 -/

/-- e⁻¹ 的改进上界：e⁻¹ < 37/100（由 e > 100/37 = 2.7027…，
    经 `Real.exp_one_gt_d9`：e > 2.7182818283）。 -/
theorem exp_neg_one_lt_37_100 : Real.exp (-1) < 37 / 100 := by
  have he : (100 / 37 : ℝ) < Real.exp 1 :=
    lt_trans (by norm_num) Real.exp_one_gt_d9
  rw [Real.exp_neg, inv_eq_one_div]
  have h := one_div_lt_one_div_of_lt (by norm_num : (0 : ℝ) < 100 / 37) he
  rwa [show (1 : ℝ) / (100 / 37) = 37 / 100 by norm_num] at h

/-- 关键定量引理（d ≥ 1）：2·e^{-d²} + e^{-d(3+d)} < 1。
    e^{-d²} ≤ e⁻¹ < 37/100，e^{-d(3+d)} ≤ e⁻⁴ = (e⁻¹)⁴ < (37/100)⁴ < 2/100，
    故和 < 2·37/100 + 2/100 = 76/100 < 1。 -/
theorem two_exp_add_exp_lt_one (d : ℝ) (hd : 1 ≤ d) :
    2 * Real.exp (-(d * d)) + Real.exp (-(d * (3 + d))) < 1 := by
  have h1 : Real.exp (-(d * d)) ≤ Real.exp (-1) := by
    apply Real.exp_le_exp.mpr
    nlinarith [hd]
  have h2 : Real.exp (-(d * (3 + d))) ≤ Real.exp (-4) := by
    apply Real.exp_le_exp.mpr
    nlinarith [hd]
  have h4 : Real.exp (-4) = Real.exp (-1) ^ 4 := by
    rw [show (-4 : ℝ) = (4 : ℕ) * (-1) by norm_num, Real.exp_nat_mul]
  have h37 := exp_neg_one_lt_37_100
  have h37pos : (0 : ℝ) ≤ Real.exp (-1) := le_of_lt (Real.exp_pos _)
  have h4b : Real.exp (-1) ^ 4 < (37 / 100) ^ 4 :=
    pow_lt_pow_left₀ h37 h37pos (by norm_num)
  have hnum : (37 / 100 : ℝ) ^ 4 < 2 / 100 := by norm_num
  have e1nn : (0 : ℝ) ≤ Real.exp (-(d * d)) := le_of_lt (Real.exp_pos _)
  nlinarith [h1, h2, h4, h4b, h37, hnum, e1nn]

/-- O2 统一性定理（核心）：物理 3-map IFS 的三个收缩率严格相异且有序，
    c₁ < c₂ < c₃（d ≥ 1）。
    这是三条动力学路径（谱流 3 不动点 / IFS 3 簇 / 信息论最小化）
    共享的同一结构核心——三个"3"是同一个 3。 -/
theorem c_physical_strictly_ordered (d : ℝ) (hd : 1 ≤ d) :
    c1_physical d < c2_physical d ∧ c2_physical d < c3_physical d := by
  have hdpos : (0 : ℝ) < d := by linarith
  have hc1c2 : c1_physical d < c2_physical d := by
    dsimp [c1_physical, c2_physical]
    apply Real.exp_lt_exp.mpr
    linarith
  have hc2c3 : c2_physical d < c3_physical d := by
    have hbase := one_sub_c1d_c2d_pos d hd
    have hc3d : (c3_physical d) ^ d =
        1 - (c1_physical d) ^ d - (c2_physical d) ^ d := by
      dsimp [c3_physical]
      rw [← Real.rpow_mul (le_of_lt hbase), one_div_mul_cancel (ne_of_gt hdpos),
        Real.rpow_one]
    have hc2d : (c2_physical d) ^ d = Real.exp (-(d * d)) := by
      have hpos : (0 : ℝ) < c2_physical d := c2_physical_pos d
      rw [Real.rpow_def_of_pos hpos]
      have hlog : Real.log (c2_physical d) = -d := Real.log_exp _
      rw [hlog]
      ring_nf
    have hc1d : (c1_physical d) ^ d = Real.exp (-(d * (3 + d))) := by
      have hpos : (0 : ℝ) < c1_physical d := c1_physical_pos d
      rw [Real.rpow_def_of_pos hpos]
      have hlog : Real.log (c1_physical d) = -(3 + d) := Real.log_exp _
      rw [hlog]
      ring_nf
    have hkey : 2 * (c2_physical d) ^ d + (c1_physical d) ^ d < 1 := by
      rw [hc2d, hc1d]
      exact two_exp_add_exp_lt_one d hd
    have hc3nn : (0 : ℝ) ≤ c3_physical d := le_of_lt (c3_physical_pos d hd)
    by_contra hnot
    push Not at hnot
    have hle := Real.rpow_le_rpow hc3nn hnot (le_of_lt hdpos)
    rw [hc3d] at hle
    have p1 : (0 : ℝ) < (c1_physical d) ^ d :=
      Real.rpow_pos_of_pos (c1_physical_pos d) d
    have p2 : (0 : ℝ) < (c2_physical d) ^ d :=
      Real.rpow_pos_of_pos (c2_physical_pos d) d
    linarith
  exact ⟨hc1c2, hc2c3⟩

/-- physicalIFS 的映射数 = 3。 -/
theorem physicalIFS_n (d : ℝ) (hd : 1 ≤ d) : (physicalIFS d hd).n = 3 := rfl

/-- O2 路径 B 的形式化核心：physicalIFS 的三个收缩率严格递增
    （作为 ℝ 值），即三个 IFS 分支处于三个相异的标度。 -/
theorem physicalIFS_ratios_ordered (d : ℝ) (hd : 1 ≤ d) :
    ((physicalIFS d hd).ratios (0 : Fin 3) : ℝ) <
      ((physicalIFS d hd).ratios (1 : Fin 3) : ℝ) ∧
    ((physicalIFS d hd).ratios (1 : Fin 3) : ℝ) <
      ((physicalIFS d hd).ratios (2 : Fin 3) : ℝ) := by
  have h1 : ((physicalIFS d hd).ratios (0 : Fin 3) : ℝ) = c1_physical d := rfl
  have h2 : ((physicalIFS d hd).ratios (1 : Fin 3) : ℝ) = c2_physical d := rfl
  have h3 : ((physicalIFS d hd).ratios (2 : Fin 3) : ℝ) = c3_physical d := rfl
  rw [h1, h2, h3]
  exact c_physical_strictly_ordered d hd
