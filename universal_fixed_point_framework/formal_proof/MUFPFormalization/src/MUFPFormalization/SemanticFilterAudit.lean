/-
  SemanticFilterAudit.lean — 语义判据能否把读数四解压到一解
  ============================================================

## 接着什么往下做

`ReverseReadoutAudit.lean` 机检裁决：

    同一个读数 15
      走层对路线 `p ↦ p.1 * p.2` ⟹ 四个原像 (1,15)、(3,5)、(5,3)、(15,1) ⟹ 非单射
      走范畴阶路线 `n ↦ n² − 1`    ⟹ 唯一原像 n = 4              ⟹ 单射

结论是「可逆性由路线决定，不由读数决定」。但那只是把问题推了一步：**读数 15 与层语义
之间到底是什么关系？** 本模块回答这一问：把层语义写成判据，看它能不能在四解里
筛出唯一一个。

## 做了什么

1. 判据 `layerTable p`：`p.1 = 主动层数 ∧ p.2 = 总层数`，两个分量都取自
   `BranchCounting` 的实际定义（`ActiveLayers.card`、`N_total`），不是新写常数。
2. `active_layers_eq_filter`：`ActiveLayers` 恰是「用 `isActive` 在 5 个层标号上
   筛一遍」的结果。这条让「3」从字面量变成可计算的谓词筛选结果。
3. `active_by_predicate`：`(univ.filter isActive).card = 3`，与 `active_layers_count`
   交叉验证。
4. 四原像逐一判：`(3,5)` 通过，其余三个不通过（`four_preimages_one_survivor`）。
5. 唯一性：`routeLayerPair p = 15 → layerTable p → p = (3,5)`。
6. 合取判决 `readout_plus_semantics_pins`：**读数单独不定解，读数 + 语义判据唯一**。

## 结论的口径（重要，勿加强）

- 本模块证明的是：**给定判据，四解压成一解**。它**不**证明「判据本身为什么是这一条」。
  判据的两分量仍是 `ActiveLayers` 与 `N_total` 的定义读法；第 63 批已登记
  「层标号有限性是类型设计而非结构定理」，此处沿用同一口径。
- 因此本模块给的是**正向构造**：结构信息确实不在读数里，在判据里；判据一旦给定，
  逆向就唯一。这比「读数永远不可逆」更强的说法要弱一档，也更诚实。
- 判据用的是 `ActiveLayers`（字面 `{one, two, three}`）。`active_layers_eq_filter`
  只说明它与 `isActive` 筛选结果相等，不说明 `isActive` 的定义有独立根据。
-/

import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic
import MUFPFormalization.ReverseReadoutAudit

open MUFPF.BranchCounting
open MUFPF.ReverseReadoutAudit

namespace MUFPF.SemanticFilterAudit

/-! =========================================================
    §1 层语义判据
   =========================================================
-/

/-- 层表判据：第一分量 = 主动生成层数，第二分量 = 总层数。

    两个分量都取自库内定义，不自造常数。 -/
def layerTable (p : ℕ × ℕ) : Prop :=
  p.1 = (ActiveLayers : Finset LayerIndex).card ∧ p.2 = N_total

/-! =========================================================
    §2 「3」是谓词筛选的结果，不是孤立字面量
   =========================================================
-/

/-- `ActiveLayers` 等于「用 `isActive` 在全部层标号上筛一遍」。 -/
theorem active_layers_eq_filter :
    ActiveLayers = Finset.univ.filter (fun l : LayerIndex => isActive l) := by
  ext l
  rcases l with obj | one | two | three | four <;> decide

/-- 交叉验证：谓词筛选后的基数也是 3。 -/
theorem active_by_predicate :
    (Finset.univ.filter (fun l : LayerIndex => isActive l)).card = 3 := by
  rw [← active_layers_eq_filter, active_layers_count]

/-! =========================================================
    §3 四原像里的唯一幸存者
   =========================================================
-/

/-- 框架取的那一对通过判据。 -/
theorem layerTable_holds : layerTable (3, 5) := by
  refine ⟨?_, ?_⟩
  · rw [active_layers_count]
  · rfl

/-- `(1,15)` 不通过：主动层数是 3，不是 1。 -/
theorem layerTable_fails_one : ¬ layerTable (1, 15) := by
  intro h
  have h1 : (1 : ℕ) = (ActiveLayers : Finset LayerIndex).card := h.1
  rw [active_layers_count] at h1
  norm_num at h1

/-- `(5,3)` 不通过。 -/
theorem layerTable_fails_five : ¬ layerTable (5, 3) := by
  intro h
  have h1 : (5 : ℕ) = (ActiveLayers : Finset LayerIndex).card := h.1
  rw [active_layers_count] at h1
  norm_num at h1

/-- `(15,1)` 不通过。 -/
theorem layerTable_fails_fifteen : ¬ layerTable (15, 1) := by
  intro h
  have h1 : (15 : ℕ) = (ActiveLayers : Finset LayerIndex).card := h.1
  rw [active_layers_count] at h1
  norm_num at h1

/-- **四原像，一幸存**：15 的四个原像里只有 `(3,5)` 满足层表判据。 -/
theorem four_preimages_one_survivor :
    layerTable (3, 5) ∧ ¬ layerTable (1, 15) ∧ ¬ layerTable (5, 3) ∧
    ¬ layerTable (15, 1) :=
  ⟨layerTable_holds, layerTable_fails_one, layerTable_fails_five, layerTable_fails_fifteen⟩

/-! =========================================================
    §4 判据下的唯一性
   =========================================================
-/

/-- **判据压解**：任何满足层表判据的赋值就是 `(3,5)`。 -/
theorem layer_table_pins (p : ℕ × ℕ) (h : layerTable p) : p = (3, 5) := by
  obtain ⟨h1, h2⟩ := h
  have h1' : p.1 = 3 := by
    rw [active_layers_count] at h1
    exact h1
  have h2' : p.2 = 5 := h2
  exact Prod.ext h1' h2'

/-- **合取判决**：

    1. 读数 15 单独不定解（存在别的原像）；
    2. 读数 15 + 层表判据 ⟹ 唯一 `(3,5)`。

    ⇒ 结构信息不在读数里，在判据里；判据一旦给定，逆向唯一。 -/
theorem readout_plus_semantics_pins :
    (∃ p : ℕ × ℕ, routeLayerPair p = 15 ∧ p ≠ (3, 5)) ∧
    (∀ p : ℕ × ℕ, routeLayerPair p = 15 → layerTable p → p = (3, 5)) := by
  refine ⟨?_, ?_⟩
  · exact ⟨(1, 15), by norm_num [routeLayerPair], by norm_num⟩
  · intro p _ htab
    exact layer_table_pins p htab

/-- 与 `ReverseReadoutAudit.routeLayerPair_not_injective` 对照的收束式：

    层对路线非单射（读数不定解），但加判据后唯一。 -/
theorem filter_compresses_four_to_one :
    ¬ Function.Injective routeLayerPair ∧
    (∀ p : ℕ × ℕ, routeLayerPair p = 15 → layerTable p → p = (3, 5)) :=
  ⟨routeLayerPair_not_injective, fun p _ h => layer_table_pins p h⟩

end MUFPF.SemanticFilterAudit
