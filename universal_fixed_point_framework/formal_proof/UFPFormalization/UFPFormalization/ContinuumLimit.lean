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
  ContinuumLimit.lean — B2 Step 3a: 编码树深度分层（2026-07-29，v1.49 修正）
  ======================================================================

  B2（连续极限）第三步 3a 的形式化：物理 3-map IFS 在单步 c₁ 映射
  下的直径上界 ≤ S₄。

  依赖:
    - IFSFractal.lean（物理 IFS、c1_physical、c_physical_strictly_ordered）
    - CoherenceToBranching.lean（silence_separation、silence_margin——备选路径）
    - Mathlib `LipschitzWith.diam_image_le`
-/

import UFPFormalization.HutchinsonAttractor
import UFPFormalization.IFSFractal
import Mathlib.Topology.MetricSpace.Lipschitz
import Mathlib.Topology.MetricSpace.Bounded
import Mathlib.Topology.Sets.Compacts
import Mathlib.Topology.Order.Compact
import Mathlib.Analysis.SpecialFunctions.Pow.Real

open Set
open Real
open Metric
open Bornology
open TopologicalSpace

namespace UFPFormalization

open scoped NNReal

/-! =========================================================
   §1 静默因子与基本不等式
   ========================================================= -/

/-- 静默因子 S₄ = e^{-d}（谱静默的辫层压制率）。 -/
noncomputable def S₄ (d : ℝ) : ℝ := Real.exp (-d)

/-- c₁ < S₄。

    c₁ = e^{-(3+d)} < e^{-d} = S₄，因为 −(3+d) < −d 且 exp 严格递增。 -/
theorem c1_lt_S₄ (d : ℝ) : c1_physical d < S₄ d := by
  dsimp [S₄, c1_physical]
  apply Real.exp_lt_exp.mpr
  linarith

/-! =========================================================
   §2 attractor 的公理化定义
   =========================================================

   B2 Step 3a 的完整形式化需将 `HutchinsonAttractor.lean` 中
   `hutchinson_attractor_exists_unique` 实例化到 `physicalIFS`。
   当前阶段使用公理化假设（与 IFSFractal.lean 中 `Attractor` 同级别）。
-/

/-- 物理 3-map IFS 的吸引子 K* 的公理化假设。
    它需要是非空紧集、吸引子方程成立、diam(K*) ≤ 1。 -/
structure AttractorAxioms (d : ℝ) (hd : 1 ≤ d) where
  /-- 吸引子集合 -/
  A : Set ℝ
  /-- 非空 -/
  hNonempty : A.Nonempty
  /-- 紧性 -/
  hCompact : IsCompact A
  /-- 吸引子方程：A = ⋃_{i=1}^3 f_i(A) -/
  hFixedPoint : A = ⋃ i : Fin 3, (physicalIFS d hd).maps i '' A
  /-- 归一化：吸引子直径 ≤ 1（f₂ 平移 1−c₃ 使 A ⊆ [0,1]，§3.5 机器证明） -/
  hDiamLeOne : Metric.diam A ≤ 1

/-! =========================================================
   §3 定理 3.1：编码树深度分层（完整证明）
   ========================================================= -/

/-- **定理 3.1（编码树深度分层，k = 1 情形）**。
    对物理 IFS 的单步 c₁ 映射，其像的直径 ≤ S₄。

    证明链：
      1. 物理 IFS 的 maps 0 在 hContracting 意义下是 Lipschitz 的，
         其 Lipschitz 常数 = ratios 0 = c1_physical d
      2. 由 `LipschitzWith.diam_image_le`，像直径 ≤ c₁·diam(A)
      3. 由吸引子归一化 diam(A) ≤ 1 得像直径 ≤ c₁
      4. 由 c₁ < S₄ 得最终结论 -/
theorem depthLayering (d : ℝ) (hd : 1 ≤ d) (ax : AttractorAxioms d hd) :
    Metric.diam ((physicalIFS d hd).maps (0 : Fin 3) '' ax.A) ≤ S₄ d := by
  -- 步骤 1：获取 Lipschitz 条件
  have hContract : ContractingWith ((physicalIFS d hd).ratios (0 : Fin 3))
      ((physicalIFS d hd).maps (0 : Fin 3)) :=
    (physicalIFS d hd).hContracting (0 : Fin 3)
  have hLipschitz : LipschitzWith ((physicalIFS d hd).ratios (0 : Fin 3))
      ((physicalIFS d hd).maps (0 : Fin 3)) :=
    hContract.2
  -- 步骤 2：吸引子紧 ⇒ 有界
  have hBounded : IsBounded ax.A := ax.hCompact.isBounded
  have hDiamBound : Metric.diam ((physicalIFS d hd).maps (0 : Fin 3) '' ax.A) ≤
      ((physicalIFS d hd).ratios (0 : Fin 3) : ℝ) * Metric.diam ax.A :=
    hLipschitz.diam_image_le ax.A hBounded
  -- 步骤 3-4：结合归一化和 c₁ < S₄
  have hRatios0_eq_c1 : ((physicalIFS d hd).ratios (0 : Fin 3) : ℝ) = c1_physical d := rfl
  rw [hRatios0_eq_c1] at hDiamBound
  have h_nonneg_c1 : 0 ≤ c1_physical d := by
    have hpos : 0 < c1_physical d := c1_physical_pos d
    exact le_of_lt hpos
  have hChain : Metric.diam ((physicalIFS d hd).maps (0 : Fin 3) '' ax.A) < S₄ d := by
    calc
      Metric.diam ((physicalIFS d hd).maps (0 : Fin 3) '' ax.A)
          ≤ c1_physical d * Metric.diam ax.A := hDiamBound
      _ ≤ c1_physical d * 1 := mul_le_mul_of_nonneg_left ax.hDiamLeOne h_nonneg_c1
      _ = c1_physical d := mul_one _
      _ < S₄ d := c1_lt_S₄ d
  exact le_of_lt hChain

/-! =========================================================
   §3.5 吸引子 ⊆ [0,1] 与 hDiamLeOne（O9 闭合，2026-08-04）
   =========================================================

   f₂ 平移归一化（1.0 → 1−c₃）后，三个映射均把 [0,1] 映到 [0,1]，
   且各映射的不动点 ∈ [0,1]。利用吸引子方程 A = ⋃ f_i(A)：
   sSup A 必为某个 f_i 的不动点（单调性 + 极值论证），故 sSup A ≤ 1；
   对称地 sInf A ≥ 0。因此 A ⊆ [0,1]，diam A ≤ 1。
   （收缩率/排序/Moran 定理不受影响——它们只依赖 ratios。）
-/

/-- physicalIFS 的每个映射单调递增（c_i > 0 的仿射映射）。 -/
lemma maps_monotone (d : ℝ) (hd : 1 ≤ d) (i : Fin 3) :
    Monotone ((physicalIFS d hd).maps i) := by
  fin_cases i
  · intro x y hxy
    simpa [physicalIFS] using mul_le_mul_of_nonneg_left hxy (le_of_lt (c1_physical_pos d))
  · intro x y hxy
    have h := mul_le_mul_of_nonneg_left hxy (le_of_lt (c2_physical_pos d))
    dsimp [physicalIFS]
    linarith
  · intro x y hxy
    have h := mul_le_mul_of_nonneg_left hxy (le_of_lt (c3_physical_pos d hd))
    dsimp [physicalIFS]
    linarith

/-- c₂ = e^{-d} ≤ 1/2（d ≥ 1，因 e^{-d} ≤ e^{-1} < 37/100 < 1/2）。 -/
lemma c2_le_half (d : ℝ) (hd : 1 ≤ d) : c2_physical d ≤ 1 / 2 := by
  dsimp [c2_physical]
  have hde : -d ≤ -1 := by linarith
  have hle : Real.exp (-d) ≤ Real.exp (-1) := Real.exp_le_exp.mpr hde
  have h1 : Real.exp (-1) < 37 / 100 := exp_neg_one_lt_37_100
  have h2 : (37 : ℝ) / 100 < 1 / 2 := by norm_num
  exact le_trans hle (le_of_lt (lt_trans h1 h2))

/-- f₀ 的唯一不动点是 0（c₁ < 1）。 -/
lemma maps0_fixedPoint (d : ℝ) (hd : 1 ≤ d) {x : ℝ}
    (h : (physicalIFS d hd).maps (0 : Fin 3) x = x) : x = 0 := by
  dsimp [physicalIFS] at h
  have hc_ne : c1_physical d ≠ 1 := ne_of_lt (c1_physical_lt_one d hd)
  have hmul : (c1_physical d - 1) * x = 0 := by nlinarith
  rcases mul_eq_zero.mp hmul with hc | hx
  · exfalso
    exact hc_ne (by linarith)
  · exact hx

/-- f₂ 的唯一不动点是 1（c₃ < 1，平移 1−c₃ 使不动点精确落在 1）。 -/
lemma maps2_fixedPoint (d : ℝ) (hd : 1 ≤ d) {x : ℝ}
    (h : (physicalIFS d hd).maps (2 : Fin 3) x = x) : x = 1 := by
  dsimp [physicalIFS] at h
  have hc_ne : c3_physical d ≠ 1 := ne_of_lt (c3_physical_lt_one d hd)
  have hmul : (1 - c3_physical d) * (x - 1) = 0 := by nlinarith
  rcases mul_eq_zero.mp hmul with hc | hx
  · exfalso
    exact hc_ne (by linarith)
  · linarith

/-- f₁ 的任意不动点 ≥ 0（x = 0.5/(1−c₂) > 0）。 -/
lemma maps1_fixedPoint_nonneg (d : ℝ) (hd : 1 ≤ d) {x : ℝ}
    (h : (physicalIFS d hd).maps (1 : Fin 3) x = x) : 0 ≤ x := by
  dsimp [physicalIFS] at h
  have hden_pos : 0 < 1 - c2_physical d := by linarith [c2_physical_lt_one d hd]
  have hmul : (1 - c2_physical d) * x = 1 / 2 := by nlinarith
  have hx : x = (1 / 2) / (1 - c2_physical d) := by
    rw [eq_div_iff (by linarith : 1 - c2_physical d ≠ 0)]
    nlinarith
  rw [hx]
  exact div_nonneg (by norm_num) (le_of_lt hden_pos)

/-- f₁ 的任意不动点 ≤ 1（d ≥ 1 ⟹ c₂ ≤ 1/2）。 -/
lemma maps1_fixedPoint_le_one (d : ℝ) (hd : 1 ≤ d) {x : ℝ}
    (h : (physicalIFS d hd).maps (1 : Fin 3) x = x) : x ≤ 1 := by
  have hc2 : c2_physical d ≤ 1 / 2 := c2_le_half d hd
  dsimp [physicalIFS] at h
  have hden_pos : 0 < 1 - c2_physical d := by linarith [c2_physical_lt_one d hd]
  have hmul : (1 - c2_physical d) * x = 1 / 2 := by nlinarith
  have hx : x = (1 / 2) / (1 - c2_physical d) := by
    rw [eq_div_iff (by linarith : 1 - c2_physical d ≠ 0)]
    nlinarith
  rw [hx]
  rw [div_le_one hden_pos]
  linarith

/-- 吸引子 ⊆ [0,1]（以分量形式陈述，供 hDiamLeOne 构造时避免结构循环）。
    论证：sSup A 是某映射的不动点（A = ⋃ f_i(A) + 各映射单调），
    而各映射不动点 ≤ 1；sInf A 同理 ≥ 0。 -/
theorem attractor_subset_unitInterval_of (d : ℝ) (hd : 1 ≤ d)
    (A : Set ℝ) (hNonempty : A.Nonempty) (hCompact : IsCompact A)
    (hFixedPoint : A = ⋃ i : Fin 3, (physicalIFS d hd).maps i '' A) :
    A ⊆ Set.Icc (0 : ℝ) 1 := by
  -- ---- sSup A ≤ 1 ----
  have hM_mem : sSup A ∈ A := hCompact.sSup_mem hNonempty
  have hM_union : sSup A ∈ (⋃ i : Fin 3, (physicalIFS d hd).maps i '' A) := by
    rw [← hFixedPoint]
    exact hM_mem
  rcases Set.mem_iUnion.mp hM_union with ⟨i, hi⟩
  rcases hi with ⟨y, hyA, hyM⟩
  have hy_le : y ≤ sSup A := le_csSup hCompact.bddAbove hyA
  have hmono : (physicalIFS d hd).maps i y ≤ (physicalIFS d hd).maps i (sSup A) :=
    (maps_monotone d hd i) hy_le
  have hM_le : sSup A ≤ (physicalIFS d hd).maps i (sSup A) := by
    calc
      sSup A = (physicalIFS d hd).maps i y := hyM.symm
      _ ≤ (physicalIFS d hd).maps i (sSup A) := hmono
  have himg_sub : (physicalIFS d hd).maps i '' A ⊆ A := by
    calc
      (physicalIFS d hd).maps i '' A ⊆
          ⋃ k : Fin 3, (physicalIFS d hd).maps k '' A :=
        Set.subset_iUnion (fun k : Fin 3 => (physicalIFS d hd).maps k '' A) i
      _ = A := hFixedPoint.symm
  have hMs_mem : (physicalIFS d hd).maps i (sSup A) ∈ A :=
    himg_sub (Set.mem_image_of_mem _ hM_mem)
  have hMs_le : (physicalIFS d hd).maps i (sSup A) ≤ sSup A :=
    le_csSup hCompact.bddAbove hMs_mem
  have hfix : (physicalIFS d hd).maps i (sSup A) = sSup A :=
    le_antisymm hMs_le hM_le
  have hM_le_one : sSup A ≤ 1 := by
    fin_cases i
    · have hz : sSup A = 0 := maps0_fixedPoint d hd hfix
      linarith
    · exact maps1_fixedPoint_le_one d hd hfix
    · have hz : sSup A = 1 := maps2_fixedPoint d hd hfix
      linarith
  -- ---- 0 ≤ sInf A ----
  have hm_mem : sInf A ∈ A := hCompact.sInf_mem hNonempty
  have hm_union : sInf A ∈ (⋃ i : Fin 3, (physicalIFS d hd).maps i '' A) := by
    rw [← hFixedPoint]
    exact hm_mem
  rcases Set.mem_iUnion.mp hm_union with ⟨j, hj⟩
  rcases hj with ⟨y, hyA, hym⟩
  have hy_ge : sInf A ≤ y := csInf_le hCompact.bddBelow hyA
  have hmono : (physicalIFS d hd).maps j (sInf A) ≤ (physicalIFS d hd).maps j y :=
    (maps_monotone d hd j) hy_ge
  have hm_le : (physicalIFS d hd).maps j (sInf A) ≤ sInf A := by
    calc
      (physicalIFS d hd).maps j (sInf A) ≤ (physicalIFS d hd).maps j y := hmono
      _ = sInf A := hym
  have himg_sub : (physicalIFS d hd).maps j '' A ⊆ A := by
    calc
      (physicalIFS d hd).maps j '' A ⊆
          ⋃ k : Fin 3, (physicalIFS d hd).maps k '' A :=
        Set.subset_iUnion (fun k : Fin 3 => (physicalIFS d hd).maps k '' A) j
      _ = A := hFixedPoint.symm
  have hms_mem : (physicalIFS d hd).maps j (sInf A) ∈ A :=
    himg_sub (Set.mem_image_of_mem _ hm_mem)
  have hms_ge : sInf A ≤ (physicalIFS d hd).maps j (sInf A) :=
    csInf_le hCompact.bddBelow hms_mem
  have hfix : (physicalIFS d hd).maps j (sInf A) = sInf A :=
    le_antisymm hm_le hms_ge
  have hzero_le_m : 0 ≤ sInf A := by
    fin_cases j
    · have hz : sInf A = 0 := maps0_fixedPoint d hd hfix
      linarith
    · exact maps1_fixedPoint_nonneg d hd hfix
    · have hz : sInf A = 1 := maps2_fixedPoint d hd hfix
      linarith
  -- ---- 组装：0 ≤ sInf A ≤ x ≤ sSup A ≤ 1 ----
  intro x hx
  constructor
  · exact le_trans hzero_le_m (csInf_le hCompact.bddBelow hx)
  · exact le_trans (le_csSup hCompact.bddAbove hx) hM_le_one

/-- AttractorAxioms 封装：吸引子 ⊆ [0,1]。 -/
theorem attractor_subset_unitInterval (d : ℝ) (hd : 1 ≤ d) (ax : AttractorAxioms d hd) :
    ax.A ⊆ Set.Icc (0 : ℝ) 1 :=
  attractor_subset_unitInterval_of d hd ax.A ax.hNonempty ax.hCompact ax.hFixedPoint

/-- 吸引子直径 ≤ 1（A ⊆ [0,1] ⟹ 任意两点距离 ≤ 1）。 -/
theorem attractor_diam_le_one (d : ℝ) (hd : 1 ≤ d) (ax : AttractorAxioms d hd) :
    Metric.diam ax.A ≤ 1 := by
  refine Metric.diam_le_of_forall_dist_le (by norm_num) ?_
  intro x hx y hy
  have hx01 := attractor_subset_unitInterval d hd ax hx
  have hy01 := attractor_subset_unitInterval d hd ax hy
  rw [Real.dist_eq]
  rw [abs_le]
  constructor
  · nlinarith [hx01.1, hx01.2, hy01.1, hy01.2]
  · nlinarith [hx01.1, hx01.2, hy01.1, hy01.2]

/-! =========================================================
   §4 从 HutchinsonAttractor 构造 AttractorAxioms
   =========================================================

   将 `hutchinson_attractor_exists_unique` 实例化到 `physicalIFS`，
   构造满足 `AttractorAxioms` 的具体吸引子。
-/

/-- 从 `hutchinson_attractor_exists_unique` 构造完整 `AttractorAxioms`（含 hDiamLeOne）。
    O9 闭合（2026-08-04）：f₂ 平移归一化后吸引子 ⊆ [0,1]（§3.5），
    `Metric.diam A ≤ 1` 获机器证明（零 sorry）。 -/
lemma exists_attractorAxioms (d : ℝ) (hd : 1 ≤ d) [Nonempty ℝ] :
    ∃ (A : Set ℝ) (hNonempty : A.Nonempty) (hCompact : IsCompact A)
      (hFixedPoint : A = ⋃ i : Fin 3, (physicalIFS d hd).maps i '' A)
      (hDiamLeOne : Metric.diam A ≤ 1), True := by
  set ifs := physicalIFS d hd
  have hn : 0 < ifs.n := by
    have h : ifs.n = 3 := rfl; rw [h]; norm_num
  have hcont : ∀ i : Fin ifs.n, Continuous (ifs.maps i) := by
    intro i
    have h := ifs.hContracting i; exact h.2.continuous
  have hexists : ∃ K : NonemptyCompacts ℝ, hutchinsonK ifs hn hcont K = K ∧
      ∀ K' : NonemptyCompacts ℝ, hutchinsonK ifs hn hcont K' = K' → K' = K :=
    hutchinson_attractor_exists_unique ifs hn hcont
  let K : NonemptyCompacts ℝ := Classical.choose hexists
  have hK_fixed : hutchinsonK ifs hn hcont K = K :=
    (Classical.choose_spec hexists).1
  have hK_fixed_set : (hutchinsonK ifs hn hcont K : Set ℝ) = (K : Set ℝ) :=
    congrArg (fun (C : NonemptyCompacts ℝ) => (C : Set ℝ)) hK_fixed
  have hn_eq_3 : ifs.n = 3 := rfl
  have hFixedPoint : (K : Set ℝ) = ⋃ i : Fin 3, (ifs.maps i) '' (K : Set ℝ) := by
    -- hutchinsonK K = K 且 hutchinsonK 的定义给出 ⋃ f_i(K)
    calc
      (K : Set ℝ) = (hutchinsonK ifs hn hcont K : Set ℝ) := by
        symm; exact hK_fixed_set
      _ = ⋃ i : Fin (ifs.n), (ifs.maps i) '' (K : Set ℝ) := rfl
      _ = ⋃ i : Fin 3, (ifs.maps i) '' (K : Set ℝ) := rfl
  refine ⟨(K : Set ℝ), K.nonempty', K.isCompact', hFixedPoint, ?_, trivial⟩
  · -- hDiamLeOne：由 §3.5 的 A ⊆ [0,1] 论证
    refine Metric.diam_le_of_forall_dist_le (by norm_num) ?_
    intro x hx y hy
    have hsub := attractor_subset_unitInterval_of d hd (K : Set ℝ)
      K.nonempty' K.isCompact' hFixedPoint
    have hx01 := hsub hx
    have hy01 := hsub hy
    rw [Real.dist_eq]
    rw [abs_le]
    constructor
    · nlinarith [hx01.1, hx01.2, hy01.1, hy01.2]
    · nlinarith [hx01.1, hx01.2, hy01.1, hy01.2]

/-! =========================================================
  §5 形式化状态总结
   ========================================================= -/

/-
  §1-§5 当前状态（2026-08-04 更新：O9 闭合）

  | 组件 | 内容 | 状态 |
  |:-----|:-----|:----:|
  | S₄ 定义   | 静默因子 e^{-d} | ✅ |
  | c1_lt_S₄  | c₁ < S₄ 机器证明 | ✅ `lake build` 通过 |
  | AttractorAxioms | 吸引子公理化定义 | ✅ |
  | depthLayering  | 深度分层定理完整证明 | ✅ `lake build` 通过 |
  | attractorAxioms_from_hutchinson | 连接真实吸引子 | ✅ 使用 `hutchinson_attractor_exists_unique` |
  | attractor_subset_unitInterval | 吸引子 ⊆ [0,1]（§3.5） | ✅ `lake build` 通过 |
  | attractor_diam_le_one / hDiamLeOne | diam(A) ≤ 1（§3.5） | ✅ 零 sorry，O9 闭合 |

  剩余工作
    - 连接 B2 3a 与 3b（2-map IFS 吸引子为拟弧）
-/

end UFPFormalization
