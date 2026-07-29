/-
  HutchinsonAttractor.lean — Hutchinson 吸引子存在唯一性（B2 第一步，2026-07-29）
  ==============================================================================

  B2（连续极限）的可形式化内核：**连续对象从离散迭代涌现**。

  IFS（有限个收缩映射）的 Hutchinson 算子 F(K) = ⋃ᵢ fᵢ(K) 在非空紧集
  的 Hausdorff 度量空间上是压缩映射（比率 = max cᵢ < 1），由 Banach
  不动点定理（Mathlib: `ContractingWith.fixedPoint`）存在唯一不动点
  K*（吸引子），且任意初始紧集的迭代 Fⁿ(K₀) 收敛到 K*。

  这把 `IFSFractal.lean` 中公理化的 `Attractor` 结构（hFixedPoint/hUnique
  字段）从假设升级为定理——离散 IFS 迭代 → 连续吸引子的涌现获得机器证明。
-/

import UFPFormalization.IFSFractal
import Mathlib.Topology.MetricSpace.Closeds

namespace UFPFormalization

open TopologicalSpace Set Metric
open scoped NNReal ENNReal

variable {X : Type} [MetricSpace X] [CompleteSpace X]

/-- IFS 的最大收缩率（Fin n 上的 Finset 最大值）。 -/
noncomputable def maxRatio (ifs : IFS X) (hn : 0 < ifs.n) : ℝ≥0 :=
  (Finset.univ.image (fun i : Fin ifs.n => ifs.ratios i)).max'
    (Finset.univ.image_nonempty.mpr
      (Finset.univ_nonempty_iff.mpr ⟨⟨0, hn⟩⟩))

theorem maxRatio_mem (ifs : IFS X) (hn : 0 < ifs.n) :
    maxRatio ifs hn ∈ Finset.univ.image (fun i : Fin ifs.n => ifs.ratios i) :=
  Finset.max'_mem _ _

theorem ratio_le_maxRatio (ifs : IFS X) (hn : 0 < ifs.n) (i : Fin ifs.n) :
    ifs.ratios i ≤ maxRatio ifs hn :=
  Finset.le_max' _ _ (Finset.mem_image.mpr ⟨i, Finset.mem_univ i, rfl⟩)

theorem maxRatio_lt_one (ifs : IFS X) (hn : 0 < ifs.n) : maxRatio ifs hn < 1 := by
  obtain ⟨i, _, hi⟩ := Finset.mem_image.mp (maxRatio_mem ifs hn)
  rw [← hi]
  exact ifs.hRatiosLtOne i

/-- Hausdorff 距离的达到引理：非空紧集 B 中，infEDist 由某点达到。 -/
theorem exists_edist_eq_infEDist_of_isCompact {B : Set X} (hB : B.Nonempty)
    (hBc : IsCompact B) (z : X) : ∃ w ∈ B, edist z w = infEDist z B := by
  obtain ⟨w, hwB, hwmin⟩ :=
    hBc.exists_isMinOn hB (Continuous.edist continuous_const continuous_id).continuousOn
  refine ⟨w, hwB, le_antisymm (le_infEDist.mpr (fun y hy => hwmin hy)) ?_⟩
  exact iInf_le_of_le w (iInf_le (fun _ : w ∈ B => edist z w) hwB)

/-- Hutchinson 算子（NonemptyCompacts 版本）：F(K) = ⋃ᵢ fᵢ(K)。 -/
noncomputable def hutchinsonK (ifs : IFS X) (hn : 0 < ifs.n)
    (hcont : ∀ i : Fin ifs.n, Continuous (ifs.maps i))
    (K : NonemptyCompacts X) : NonemptyCompacts X :=
  ⟨⟨⋃ i : Fin ifs.n, (ifs.maps i) '' (K : Set X),
    isCompact_iUnion (fun i => K.isCompact'.image (hcont i))⟩,
    (by
      obtain ⟨x, hx⟩ := K.nonempty'
      exact ⟨(ifs.maps ⟨0, hn⟩) x,
        Set.mem_iUnion.mpr ⟨⟨0, hn⟩, Set.mem_image_of_mem _ hx⟩⟩)⟩

/-- Hutchinson 算子是压缩映射（比率 = max cᵢ）。 -/
theorem hutchinsonK_contracting (ifs : IFS X) (hn : 0 < ifs.n)
    (hcont : ∀ i : Fin ifs.n, Continuous (ifs.maps i)) :
    ContractingWith (maxRatio ifs hn) (hutchinsonK ifs hn hcont) := by
  refine ⟨maxRatio_lt_one ifs hn, ?_⟩
  intro A B
  -- 目标：hausdorffEDist (⋃ fᵢ''A) (⋃ fᵢ''B) ≤ maxRatio * hausdorffEDist A B
  have dir : ∀ (P Q : NonemptyCompacts X) (x : X),
      x ∈ (⋃ i : Fin ifs.n, (ifs.maps i) '' (P : Set X)) →
      ∃ y ∈ (⋃ i : Fin ifs.n, (ifs.maps i) '' (Q : Set X)),
        edist x y ≤ (maxRatio ifs hn : ℝ≥0∞) * hausdorffEDist (P : Set X) Q := by
    intro P Q x hx
    obtain ⟨i, hi⟩ := Set.mem_iUnion.mp hx
    obtain ⟨z, hzP, rfl⟩ := hi
    obtain ⟨w, hwQ, hzw⟩ :=
      exists_edist_eq_infEDist_of_isCompact Q.nonempty' Q.isCompact' z
    have hzw' : edist z w = infEDist z (Q : Set X) := hzw
    have h1 : infEDist z (Q : Set X) ≤ hausdorffEDist (P : Set X) Q :=
      infEDist_le_hausdorffEDist_of_mem hzP
    refine ⟨(ifs.maps i) w, Set.mem_iUnion.mpr ⟨i, Set.mem_image_of_mem _ hwQ⟩, ?_⟩
    calc edist ((ifs.maps i) z) ((ifs.maps i) w)
        ≤ (ifs.ratios i : ℝ≥0∞) * edist z w := (ifs.hContracting i).2 z w
      _ = (ifs.ratios i : ℝ≥0∞) * infEDist z (Q : Set X) := by rw [hzw']
      _ ≤ (ifs.ratios i : ℝ≥0∞) * hausdorffEDist (P : Set X) Q :=
          mul_le_mul_left' h1 _
      _ ≤ (maxRatio ifs hn : ℝ≥0∞) * hausdorffEDist (P : Set X) Q :=
          mul_le_mul_right'
            (ENNReal.coe_le_coe.mpr (ratio_le_maxRatio ifs hn i)) _
  -- edist on NonemptyCompacts = hausdorffEDist（实例定义）
  show hausdorffEDist (⋃ i : Fin ifs.n, (ifs.maps i) '' (A : Set X))
      (⋃ i : Fin ifs.n, (ifs.maps i) '' (B : Set X)) ≤
    (maxRatio ifs hn : ℝ≥0∞) * hausdorffEDist (A : Set X) B
  exact hausdorffEDist_le_of_mem_edist (fun x hx => dir A B x hx)
    (fun x hx => (hausdorffEDist_comm (s := (A : Set X)) (t := (B : Set X))).symm ▸ dir B A x hx)

instance [Nonempty X] : Nonempty (NonemptyCompacts X) :=
  ⟨⟨⟨{Classical.choice ‹Nonempty X›}, isCompact_singleton⟩,
    Set.singleton_nonempty _⟩⟩

/-- **Hutchinson 吸引子存在唯一性定理**（B2 第一步的机器证明）：
    有限 IFS 的 Hutchinson 算子在非空紧集空间上是压缩映射，
    因此存在唯一不动点 K*（吸引子）。 -/
theorem hutchinson_attractor_exists_unique (ifs : IFS X) (hn : 0 < ifs.n)
    (hcont : ∀ i : Fin ifs.n, Continuous (ifs.maps i)) [Nonempty X] :
    ∃! K : NonemptyCompacts X, hutchinsonK ifs hn hcont K = K := by
  have hc := hutchinsonK_contracting ifs hn hcont
  exact ⟨ContractingWith.fixedPoint _ hc, hc.fixedPoint_isFixedPt,
    fun K hK => hc.fixedPoint_unique hK⟩

/-- 迭代收敛定理：任意初始紧集 K₀ 的 Hutchinson 迭代 Fⁿ(K₀)
    收敛到唯一吸引子 K*——**连续吸引子从离散 IFS 迭代涌现**。 -/
theorem hutchinson_iterate_tendsto (ifs : IFS X) (hn : 0 < ifs.n)
    (hcont : ∀ i : Fin ifs.n, Continuous (ifs.maps i)) [Nonempty X]
    (K : NonemptyCompacts X) :
    Filter.Tendsto (fun n => (hutchinsonK ifs hn hcont)^[n] K) Filter.atTop
      (nhds (ContractingWith.fixedPoint _ (hutchinsonK_contracting ifs hn hcont))) :=
  (hutchinsonK_contracting ifs hn hcont).tendsto_iterate_fixedPoint K

end UFPFormalization
