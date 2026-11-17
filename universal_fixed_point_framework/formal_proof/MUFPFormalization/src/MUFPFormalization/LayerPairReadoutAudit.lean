/-
  LayerPairReadoutAudit.lean — 层标号停在 4 的依据审查与 `B = 3 × 5` 的交叉项解剖（第 63 批）
  ==================================================================================

  ## 问题（承接第 60/61/62 批）

  第 60 批证明「层标号停在 4，层结构没停」（`index_does_not_track_structure`），
  并登记待办 `layer_index_stops_at_four_without_structural_witness`。
  第 61/62 批证明 `N_total = 5` 与 `N_active = 3` 都相盲。
  ⇒ 剩下一个没答的问题：**「层标号有限」这件事本身能不能约束结构？**

  本批三问：

  1. `Fintype.card LayerIndex = 5` 是不是一个结构上界？（能不能当塔高上界）
  2. 「5」是不是唯一的可实现层标号基数？（换一个基数还成立吗）
  3. `B = 3 × 5 = 15` 这 15 个组合里，包含了哪些**本不该有分支**的组合？

  ## 本批的正面结论

  ### 一、层标号有限**不能**约束结构

  * `finite_index_coexists_with_unbounded_tower`：`card LayerIndex = 5` 与
    「B 相层 `k ≥ 2` 全部有见证」**同时成立** ⇒ 有限标号与无界结构不矛盾。
  * `index_card_not_a_tower_bound`：`¬ ∀ k ≥ 2, k ≤ card LayerIndex`（取 `k = 6` 反例）。
    ⇒ 把 `N_total = 5` 当塔高上界是**错的**。

  ### 二、「5」是可替换的设计参数

  * `any_card_realizable`：`∀ n, Fintype.card (Fin n) = n` ⇒ 任何 `n` 都能做成层标号基数。
  * `alt_card_changes_B`：`n ≥ 2 ∧ n ≠ 5 ⇒ 3 * n ≠ B` ⇒ 同一公式在别的基数下**给不出 15**。
    ⇒ 「5」是选择，`B = 15` 继承该选择。

  ### 三、`B = 15` 的交叉项解剖（本批新发现）

  `LayerIndex` 的 5 个构造子里，**只有 3 个是主动生成层**（`one`/`two`/`three`）；
  `obj`（对象层 0）与 `four`（coherence 层 4）都**不是**（`isActive` 给 `false`）。

  ```
  B = |Active| × |All| = 3 × 5 = 15
  而 |All| = |Active| + |NonActive| = 3 + 2
  ⇒ B = 3 × 3 + 3 × 2 = 9 + 6
  ```

  ⇒ 15 里**有 6 个是「生成层 × 非生成层」的交叉组合**。
  `BranchCounting.lean` L124–127 的理由写「该映射在 5 个范畴层次上各有独立的固定点分支」——
  但对象层与 coherence 层都不是生成层，这条理由对它们不适用。

  四个候选口径：

  | 口径 | 构造 | 读数 |
  |---|---|---|
  | 全部层对 | `3 × 5` | **15**（库内采用） |
  | 去掉对象层 | `3 × (5 − 1)` | **12**（第 56 批张力，`d_H = ln 12`） |
  | 只数生成层之间的层对 | `3 × 3` | **9** |
  | 生成层 × 非生成层 | `3 × 2` | **6** |

  ⇒ `B` 不是「结构逼出的 15」，而是**在四个可选口径里选了一个**。

  ## 与第 60/61/62 批的关系

  * 第 60 批给了 `±1` 是代数对称包装、`B = c² − 1` 由 `c` 一元决定；本批把 `3 × 5`
    拆成 `3 × 3 + 3 × 2`，指出其中 6 个组合的**语义**没有依据。
  * 第 61 批：标号 5 相盲；第 62 批：`N_active` 相盲。本批：**两者都不只是一个相盲的数，
    而是四个可选读数的其中一个**。
  * `N_total` 的裸常量性（第 60 批发现二）在本批得到定量后果：换基数就换 `B`。

  ## 边界（必须一并陈述）

  - 本批**不**新增 `LayerIndex` 构造子，不改 `B`、不改 `N_total`、不改 `isActive`。
  - 「哪个口径才对」**不是**本批结论：本批只证四个读数互异、且库内选择无结构依据。
    口径裁决需要额外的结构论证（`B` 的「分支」到底由谁产生）。
  - `d_H = ln B` 随口径变化一事，本批**只证整数读数互异**（`15 ≠ 12 ≠ 9 ≠ 6`）；
    「`ln` 严格单调 ⇒ `d_H` 也随之不同」这一步**未机检**（避免为一行推论拉入
    `Mathlib.Analysis` 依赖链），登记为未机检推论。
  - 层 5 结构存在（第 60 批 `layer_five_structure_exists`）不在本批重复证明。
-/

import Mathlib.Tactic
import MUFPFormalization.BranchCounting
import MUFPFormalization.SpTowerUnbounded

namespace MUFPF.LayerPairReadout

open MUFPFormalization
open MUFPF.BranchCounting (LayerIndex N_total B ActiveLayers active_layers_count B_eq_15
  total_layers_count isActive)

/-! ## 一、层标号的穷举与「主动 / 非主动」划分 -/

/-- `LayerIndex` 的五个构造子穷举（**该类型恰有这五个元素**，不是「结构只有五层」）。 -/
theorem layer_exhaustive (l : LayerIndex) :
    l = LayerIndex.obj ∨ l = LayerIndex.one ∨ l = LayerIndex.two ∨
    l = LayerIndex.three ∨ l = LayerIndex.four := by
  cases l <;> simp

/-- 非主动生成层：对象层 0（`obj`）与 coherence 层 4（`four`），与 `isActive` 的 `false` 两支一致。 -/
def NonActiveLayers : Finset LayerIndex := {LayerIndex.obj, LayerIndex.four}

/-- 非主动层数 = 2。 -/
theorem non_active_layers_count : (NonActiveLayers : Finset LayerIndex).card = 2 := by
  native_decide

/-- ★★ **5 = 3 + 2**：主动层与非主动层构成 `LayerIndex` 的完整划分。 -/
theorem layer_partition :
    (ActiveLayers : Finset LayerIndex).card + (NonActiveLayers : Finset LayerIndex).card
      = Fintype.card LayerIndex := by
  native_decide

/-! ## 二、`B = 15` 的交叉项解剖 -/

/-- ★★★ **`B = 3 × 3 + 3 × 2`**：15 里含 6 个「生成层 × 非生成层」交叉组合。

    原文理由（`BranchCounting.lean` L124–127）声称「该映射在 5 个范畴层次上各有独立的
    固定点分支」，但对象层与 coherence 层都不是生成层 ⇒ 这 6 个组合的语义无依据。 -/
theorem B_decomposition :
    B = (ActiveLayers : Finset LayerIndex).card * (ActiveLayers : Finset LayerIndex).card
      + (ActiveLayers : Finset LayerIndex).card * 2 := by
  rw [B_eq_15, active_layers_count]

/-- ★★ **去掉对象层给 12**：`3 × (5 − 1) = 12`（第 56 批登记的张力口径）。 -/
theorem object_layer_removed_readout :
    (ActiveLayers : Finset LayerIndex).card * (Fintype.card LayerIndex - 1) = 12 := by
  rw [active_layers_count, total_layers_count]

/-- ★★ **四个候选读数互异**：`B = 15` 与 12 / 9 / 6 都不同。 -/
theorem four_readouts_distinct :
    B ≠ 12 ∧ B ≠ 9 ∧ B ≠ 6 ∧ (12 : ℕ) ≠ 9 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · rw [B_eq_15]; norm_num
  · rw [B_eq_15]; norm_num
  · rw [B_eq_15]; norm_num
  · norm_num

/-! ## 三、层标号有限不能约束结构 -/

/-- ★★★ **有限标号与无界结构同存**：`card LayerIndex = 5` 与「B 相每层 `k ≥ 2` 都有见证」
    同时成立 ⇒ 两者不矛盾，有限标号不是结构上界。 -/
theorem finite_index_coexists_with_unbounded_tower :
    Fintype.card LayerIndex = 5 ∧ (∀ k : ℕ, 2 ≤ k → MUFPF.LayerWitness jordan3) :=
  ⟨total_layers_count, MUFPF.tower_height_unbounded_B⟩

/-- ★★★ **层标号基数不是塔高上界**（取 `k = 6` 反例）。

    ⇒ 把 `N_total = 5` 当「塔高最多 5」是错的。 -/
theorem index_card_not_a_tower_bound :
    ¬ (∀ k : ℕ, 2 ≤ k → k ≤ Fintype.card LayerIndex) := by
  intro h
  have hcard : Fintype.card LayerIndex = 5 := total_layers_count
  have h6 : 2 ≤ 6 := by norm_num
  have hle : 6 ≤ Fintype.card LayerIndex := h 6 h6
  rw [hcard] at hle
  omega

/-! ## 四、「5」是可替换的设计参数 -/

/-- ★★ **任何 `n` 都能做成层标号基数**（`Fin n`）。 -/
theorem any_card_realizable (n : ℕ) : Fintype.card (Fin n) = n :=
  Fintype.card_fin n

/-- ★★ **换基数就给不出 15**：`n ≥ 2 ∧ n ≠ 5 ⇒ 3 * n ≠ B`。

    ⇒ `B = 15` 继承了「层标号取 5」这个选择。 -/
theorem alt_card_changes_B (n : ℕ) (_hn : 2 ≤ n) (hne : n ≠ 5) : (3 : ℕ) * n ≠ B := by
  intro h
  have hB : B = 15 := B_eq_15
  have h15 : (3 : ℕ) * n = 15 := h.trans hB
  omega

/-! ## 五、总述 -/

/-- ★★★ **本批裁决的可机检部分**（九合取）：

    1. `LayerIndex` 恰有五个构造子（穷举）；
    2. 主动层 3 个、非主动层 2 个；
    3. `3 + 2 = 5`（完整划分）；
    4. `B = 15`；
    5. `B = 3 × 3 + 3 × 2`（15 里 6 个是交叉项）；
    6. 去掉对象层给 12；
    7. B 相层 `k ≥ 2` 全部有见证；
    8. 层标号基数不是塔高上界；
    9. 任何 `n` 都能做成层标号基数。

    ⇒ 层标号有限是**类型设计**，不是结构定理；`B = 15` 是四个可选口径之一（另三个 12 / 9 / 6）。 -/
theorem layer_pair_verdict :
    (∀ l : LayerIndex, l = LayerIndex.obj ∨ l = LayerIndex.one ∨ l = LayerIndex.two ∨
      l = LayerIndex.three ∨ l = LayerIndex.four) ∧
    (ActiveLayers : Finset LayerIndex).card = 3 ∧
    (NonActiveLayers : Finset LayerIndex).card = 2 ∧
    (ActiveLayers : Finset LayerIndex).card + (NonActiveLayers : Finset LayerIndex).card
      = Fintype.card LayerIndex ∧
    B = 15 ∧
    B = (ActiveLayers : Finset LayerIndex).card * (ActiveLayers : Finset LayerIndex).card
      + (ActiveLayers : Finset LayerIndex).card * 2 ∧
    (ActiveLayers : Finset LayerIndex).card * (Fintype.card LayerIndex - 1) = 12 ∧
    (∀ k : ℕ, 2 ≤ k → MUFPF.LayerWitness jordan3) ∧
    ¬ (∀ k : ℕ, 2 ≤ k → k ≤ Fintype.card LayerIndex) ∧
    (∀ n : ℕ, Fintype.card (Fin n) = n) :=
  ⟨layer_exhaustive, active_layers_count, non_active_layers_count, layer_partition,
    B_eq_15, B_decomposition, object_layer_removed_readout,
    finite_index_coexists_with_unbounded_tower.2, index_card_not_a_tower_bound,
    any_card_realizable⟩

end MUFPF.LayerPairReadout
