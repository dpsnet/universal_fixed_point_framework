/-
  SlotVersusTraceAudit.lean — R-w：载体迹里的 `4` 与槽数 `4` 是否同源（§35 散文结论的机检收口）
  ==========================================================================================

## 问题

§35 曾在散文里断言「`4 + Δλ_min` 中的 `4` 来自 `2 + 2`，与槽数 `4` 是巧合、非同源」，但当时只机检了
「迹可加」「四值同一迹」，**没有机检这个『非同源』本身**。本批把两条生成链拆开各自钉死。

## 结果

- 槽数 `4`：`Fintype.card (Fin 2 ⊕ Fin 2) = 4`——载体类型 `Fin 2 ⊕ Fin 2` 的**基数**，与任何条目无关。
- 迹的 `4`：`trace (blk (diag(0,k)) B C (diag(1,h))) = k + 1 + h`——**两块的迹之和**，随层数据条目连续变。
  框架实例（`k = 2`、`h = 1`）恰为 `4`；把 `k` 换成 `3` 读数变 `5`。
- 迹读 `4` 的**充要条件**是条目满足 `k + h = 3`（即 `k = 2 ∧ h = 1` 一类），是**关于数据的约束**；
  槽数 `4` 不约束任何数据。

## 判决

两条 `4` 的生成链输入类型不同：一个是对**类型**取基数（常量），一个是对**条目**取迹和（可变量）。
故 §35 的散文结论升级为机检判决：`4 + Δλ_min` 里的 `4` 与槽数 `4` **数值重合、不同源**，
不得用槽数去预测迹读数，也不得用迹读数去论证槽数为 `4`。

诚实边界：本批不判「`blk` 只能建在 `Fin 2 ⊕ Fin 2` 上」（那是 §25 的载体定义）；
`k = 3` / `h = 1` 仅为见证。不新增常数、不新增公设。
-/

import MUFPFormalization.LayeredCarrierAudit
import MUFPFormalization.IntertwinerExistenceAudit
import Mathlib.Tactic

namespace MUFPF.SlotTraceAudit

open MUFPF.IntertwinerExistenceAudit (diag2)
open MUFPF.LayeredCarrierAudit (blk trace_blk)
open MUFPF.GNBridgeAudit (dlmin)

/-- ★ **槽数 `4` 的生成链**：载体类型 `Fin 2 ⊕ Fin 2` 的基数，与任何矩阵条目无关。 -/
theorem slot_count_four : Fintype.card (Fin 2 ⊕ Fin 2) = 4 := by
  simp

/-- ★★ **迹读数的生成链**：`trace (blk (diag(0,k)) B C (diag(1,h))) = k + 1 + h`，
    对任意实数 `k, h` 与任意耦合块 `B, C`——读数只由两个对角块的迹决定。 -/
theorem trace_general (k h : ℝ) (B C : Matrix (Fin 2) (Fin 2) ℝ) :
    Matrix.trace (blk (diag2 (0 : ℝ) k) B C (diag2 (1 : ℝ) h)) = k + 1 + h := by
  rw [trace_blk]
  have h1 : Matrix.trace (diag2 (0 : ℝ) k) = k := by
    simp [diag2, Matrix.trace, Fin.sum_univ_two]
  have h2 : Matrix.trace (diag2 (1 : ℝ) h) = 1 + h := by
    simp [diag2, Matrix.trace, Fin.sum_univ_two]
  rw [h1, h2]
  ring

/-- 框架式条目（`k = 2`、`h = 1`）恰读 `4`：`4 = 2 + (1 + 1)`。 -/
theorem trace_four_at_unit :
    Matrix.trace (blk (diag2 (0 : ℝ) 2) 0 0 (diag2 (1 : ℝ) 1)) = 4 := by
  rw [trace_general 2 1 0 0]
  norm_num

/-- 改一个条目（`k = 3`）读数变 `5`：迹的 `4` 不是常数。 -/
theorem trace_varies_with_entries :
    Matrix.trace (blk (diag2 (0 : ℝ) 3) 0 0 (diag2 (1 : ℝ) 1)) = 5 ∧ (5 : ℝ) ≠ 4 := by
  refine ⟨?_, by norm_num⟩
  rw [trace_general 3 1 0 0]
  norm_num

/-- ★ **迹读 `4` 是关于条目的约束**：`k + 1 + h = 4 ⟺ k + h = 3`。 -/
theorem trace_four_iff (k h : ℝ) : k + 1 + h = 4 ↔ k + h = 3 := by
  constructor
  · intro hk; linarith
  · intro hk; linarith

/-- ★ **迹读数不是常数 `4`**（存在条目使读数为 `5`）。 -/
theorem trace_not_constant :
    ¬ (∀ k h : ℝ,
        Matrix.trace (blk (diag2 (0 : ℝ) k) 0 0 (diag2 (1 : ℝ) h)) = 4) := by
  intro H
  have h4 := H 3 1
  rw [trace_general 3 1 0 0] at h4
  norm_num at h4

/-- ★★ **判决**：① 槽数 `= 4`（类型基数、常量）；② 迹读数 `= k + 1 + h`（条目迹和、可变量）；
    ③ 存在条目使迹读数 `= 5 ≠ 4` ⟹ 两个 `4` 数值重合、生成链不同源。 -/
theorem slot_vs_trace_verdict :
    Fintype.card (Fin 2 ⊕ Fin 2) = 4 ∧
      (∀ k h : ℝ, ∀ B C : Matrix (Fin 2) (Fin 2) ℝ,
        Matrix.trace (blk (diag2 (0 : ℝ) k) B C (diag2 (1 : ℝ) h)) = k + 1 + h) ∧
      (Matrix.trace (blk (diag2 (0 : ℝ) 3) 0 0 (diag2 (1 : ℝ) 1)) = 5 ∧ (5 : ℝ) ≠ 4) :=
  ⟨slot_count_four, trace_general, trace_varies_with_entries⟩

end MUFPF.SlotTraceAudit
