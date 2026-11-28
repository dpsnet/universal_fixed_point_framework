/-
  ThreeVersusActiveAudit.lean — R-z：`det` 读数里的 `3` 与 `N_active` 是否同源（§41 开口 `DET_THREE_VS_N_ACTIVE` 收口）
  ==========================================================================================

## 问题

§41 在转动同号分支（`B = C = A`）读出的 `det` 精确为 `3`，而 `N_active = catOrder − 1 = 3`。
两处数值相同，必须判：**同一个 3 吗？**

## 做法

不去比对两个 3 的字面，而是查 `det` 那个 3 的**生成式对什么敏感**：把 `A_GR = diag(0, 2)` 换成
`diag(0, k)`（`k` 为层数据的第二对角元），保持耦合 `B = C = A`、`A_SM = diag(1, h)` 不变，重算读数。
若读数是 `k + 1`，则 `3` 只是 `k = 2` 的特例；`k` 可任取实数（`k = 0` 读 `1`、`k = 5` 读 `6`），
而 `N_active` 由 `catOrder = 4` 钉住、与 `k` 无关。

## 结果

- `rot_reading_general`：`det (blk (diag(0,k)) A A (diag(1,h))) = k + 1`，**对任意实数 `k`**；
- 框架实例（`k = 2`、`h = 1 + Δλ_min`）读 `2 + 1 = 3`，复现 §41；
- `reading_varies_with_layer_entry`：`k = 0` 读 `1`、`k = 5` 读 `6`，两读数不同；
- `reading_not_three_for_other_k`：`k = 5` 读 `6 ≠ 3`；
- `nActive_as_real`：`N_active = 3`（由 `catOrder − 1`）。

## 判决

`3` 的生成链是「`A_GR` 非零对角元 `k` + 1」——`k` 是**层数据条目，可任取实数**，读数随之线性变；
`N_active` 的生成链是「`catOrder − 1`，而 `catOrder` 由硬等式 `n² = 2ⁿ` 钉在 `4`」——`ℕ` 值、与层数据无关。
两条链的输入类型不同（一个连续可调、一个由整数硬等式钉住），且读数在别的 `k` 上取到 `1` 与 `6`，
故**数值相等、生成链不同源**：`DET_THREE_VS_N_ACTIVE` 判为巧合，不得互推。

诚实边界：本批只判「`det` 读数不随 `catOrder` 变」，**不**判「两个 3 永不可能在别的构造里同源」；
`k` 取 `0`、`5` 仅为见证，不代表层数据的物理取值。
-/

import MUFPFormalization.QuantizedDetAudit
import MUFPFormalization.ActiveFromCategoryOrder
import Mathlib.Tactic

set_option linter.unusedSimpArgs false
set_option linter.unusedTactic false
set_option linter.unreachableTactic false
-- `letI` 使 `⅟` 按定义归约（`let` 会使其不透明），故此处保留 local instance 写法
set_option linter.style.haveILetI false

namespace MUFPF.CoincidenceAudit

open MUFPF.IntertwinerExistenceAudit (diag2)
open MUFPF.LayeredCarrierAudit (blk)
open MUFPF.IntertwinerRepairAudit (rotGen)
open MUFPF.CarrierDetAudit (det_diag2)
open MUFPF.TwoWayCarrierAudit (diag2_sub_diag2)
open MUFPF.SchurCarrierAudit (det_blk_schur)
open MUFPF.QuantizedDetAudit (instDiagOne rot_sandwich)
open MUFPF.GNBridgeAudit (dlmin dlmin_pos)
open MUFPF.CategoryOrder (catOrder nActive catOrder_eq_fixedpoint nActive_eq_three)

/-- ★★ **转动同号分支的 `det` 读数是层数据条目的线性函数**：
    `det (blk (diag(0,k)) A A (diag(1,h))) = k + 1`，对**任意**实数 `k` 成立。
    机制：`A·⅟A_SM·A = diag(−h⁻¹, −1)`，故 `A_GR −` 该项 `= diag(h⁻¹, k + 1)`，
    行列式 `= h⁻¹·(k+1)`，乘 `det A_SM = h` 后 `h⁻¹` 抵消，只剩 `k + 1`。 -/
theorem rot_reading_general (k h : ℝ) (hh : h ≠ 0) :
    Matrix.det (blk (diag2 (0 : ℝ) k) rotGen rotGen (diag2 (1 : ℝ) h)) = k + 1 := by
  letI := instDiagOne h hh
  have hD : Matrix.det (diag2 (1 : ℝ) h) = h := by rw [det_diag2]; ring
  rw [det_blk_schur, hD, show ⅟(diag2 (1 : ℝ) h) = diag2 (1 : ℝ) h⁻¹ from rfl]
  rw [rot_sandwich, diag2_sub_diag2, det_diag2]
  field_simp
  ring

/-- 框架实例（`k = 2` 即 `A_GR = diag(0,2)`、`h = 1 + Δλ_min`）读 `2 + 1 = 3`：复现 §41。 -/
theorem framework_three_is_gr_plus_one :
    Matrix.det (blk (diag2 (0 : ℝ) 2) rotGen rotGen (diag2 (1 : ℝ) (1 + dlmin))) = 3 := by
  have hh : (1 : ℝ) + dlmin ≠ 0 := by
    have hpos : (0 : ℝ) < 1 + dlmin := by linarith [dlmin_pos]
    linarith
  rw [rot_reading_general 2 (1 + dlmin) hh]
  norm_num

/-- `det` 读数随层数据条目变：`k = 0` 读 `1`、`k = 5` 读 `6`，两者不同。 -/
theorem reading_varies_with_layer_entry :
    Matrix.det (blk (diag2 (0 : ℝ) 0) rotGen rotGen (diag2 (1 : ℝ) (1 + dlmin))) ≠
      Matrix.det (blk (diag2 (0 : ℝ) 5) rotGen rotGen (diag2 (1 : ℝ) (1 + dlmin))) := by
  have hh : (1 : ℝ) + dlmin ≠ 0 := by
    have hpos : (0 : ℝ) < 1 + dlmin := by linarith [dlmin_pos]
    linarith
  rw [rot_reading_general 0 (1 + dlmin) hh, rot_reading_general 5 (1 + dlmin) hh]
  norm_num

/-- `k = 5`（`A_GR = diag(0,5)`）读 `6`，与 `3` 不同：读数不是常数。 -/
theorem reading_not_three_for_other_k :
    Matrix.det (blk (diag2 (0 : ℝ) 5) rotGen rotGen (diag2 (1 : ℝ) (1 + dlmin))) = 6 ∧
      (6 : ℝ) ≠ 3 := by
  have hh : (1 : ℝ) + dlmin ≠ 0 := by
    have hpos : (0 : ℝ) < 1 + dlmin := by linarith [dlmin_pos]
    linarith
  refine ⟨?_, by norm_num⟩
  rw [rot_reading_general 5 (1 + dlmin) hh]
  norm_num

/-- `N_active` 作为实数等于 `3`（由 `catOrder − 1` 与 `catOrder = 4` 钉住）。 -/
theorem nActive_as_real : ((nActive : ℕ) : ℝ) = 3 := by
  rw [nActive_eq_three]
  norm_num

/-- `catOrder` 由硬等式 `n² = 2ⁿ` 钉住（引既有登记），故 `N_active` 的输入是整数硬等式，
    与层数据条目 `k`（连续可调）分属两类输入。 -/
theorem catOrder_pinned_by_fixed_point : catOrder = 4 := by
  rw [catOrder_eq_fixedpoint]
  rfl

/-- ★ **判决**：① `N_active = 3`；② `det` 读数对任意 `k` 为 `k + 1`（框架实例给 `3`）；
    ③ 存在 `k` 使读数为 `6`（≠ 3）⟹ 读数不是 `catOrder` 的函数，两个 `3` **不同源**。 -/
theorem three_vs_nactive_verdict :
    ((nActive : ℕ) : ℝ) = 3 ∧
      (∀ k h : ℝ, h ≠ 0 →
        Matrix.det (blk (diag2 (0 : ℝ) k) rotGen rotGen (diag2 (1 : ℝ) h)) = k + 1) ∧
      (Matrix.det (blk (diag2 (0 : ℝ) 5) rotGen rotGen (diag2 (1 : ℝ) (1 + dlmin))) = 6 ∧
        (6 : ℝ) ≠ 3) :=
  ⟨nActive_as_real, rot_reading_general, reading_not_three_for_other_k⟩

end MUFPF.CoincidenceAudit
