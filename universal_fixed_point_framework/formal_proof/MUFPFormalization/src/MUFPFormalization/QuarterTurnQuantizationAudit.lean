/-
  QuarterTurnQuantizationAudit.lean — R-o：角的量化（θ 的离散化）
  =====================================================================================

## 问题

§30 判决：接受「保长度」后，耦合块从 4 个实参数降到 **1 个自由角 `θ`**
（`α = cos θ`、`δ = sin θ`）。开口收成一句：

> `θ` 的内生来源是什么？

本批不再引入任何新数，只用**载体自身的槽数 4**（`Fin 2 ⊕ Fin 2`，其基数由
`carrier_slots_four` 机检）。若要耦合是载体的**内部循环**，其阶应整除 4：

> **第 100 批订正**：原稿此处把 `card (Fin 2 × Fin 2) = 4` 当作「槽数 4」的依据——对象错了：
> `Fin 2 × Fin 2` 是单个耦合块的**条目数**，不是载体基数。载体基数是 `Fintype.card (Fin 2 ⊕ Fin 2)`，
> 由本文件 `carrier_slots_four` 机检（§43 的 `slot_count_four` 同款）。另须注意 `4` **不是**载体迹读数：
> §43 `trace_four_iff` 已机检 `trace = k + 1 + Δλ_min`，`trace = 4` 只是一组条目约束（`k + Δλ_min = 3`），
> 与槽数**不同源**。因此 `B⁴ = 1` 的依据只能是「载体 4 维」，不能表述为「迹读数 4」。

```
  B ^ 4 = 1
```

## 判据与答案

- **判①**：`BᵀB = 1 ∧ det B = 1 ∧ B⁴ = 1` ⟹ `θ ∈ {0, π/2, π, 3π/2}`，
  即 `(α, δ) ∈ {(1,0), (0,1), (−1,0), (0,−1)}`。
- **判②**：于是 `B` 只可能是 `1`、`−1`、`rotGen`、`−rotGen` 四个值。
- **判③**：其中 `±1` 是「无耦合」（`α = ±1`、`δ = 0`，层间不交换）；
  真正的耦合只剩 `±rotGen`，彼此只差一个**符号位**——一个比特（朝向）。

## 净结果

> 4 个实参数 →（保长度）→ 1 个连续角 →（阶整除 4）→ **0 个连续参数 + 1 个比特**。

`α`、`δ` 的大小到此**完全定了**（0 或 ±1），不再是「无判据」的数；
剩下的唯一自由是朝向（`rotGen` 还是 `−rotGen`），即 `ℤ/2`。

## 关键代数事实（推导骨架）

`B = α·1 + δ·A`（`A = rotGen`，`A² = −1`），故

```
  B² = (α² − δ²)·1 + 2αδ·A
  B⁴ = ((α²−δ²)² − (2αδ)²)·1 + 2(α²−δ²)(2αδ)·A
```

`B⁴ = 1` 给出两条条目方程：`A` 项为零（`αδ(α²−δ²) = 0`）与 `1` 项为一。
与圆关系 `α²+δ²=1` 联立：

- `α² = δ² = 1/2` 那一支（`θ = π/4` 型）被 `1` 项方程判死（代入得 `−1 = 1`）；
- 故只剩 `αδ = 0`，再由圆关系得 `(α,δ) ∈ {(±1,0), (0,±1)}`。

## 诚实边界

1. `B⁴ = 1` 是**第二条新结构要求**（与 §30 的「保长度」同级）。它只用「阶整除载体槽数」
   这一条计数原则，不引入新常数；但**是否接受仍待裁决**。
2. `4` 的来源是载体槽数（`Fintype.card (Fin 2 ⊕ Fin 2)`，本文件 `carrier_slots_four`），不是 `catOrder`，
   **也不是**载体迹读数（§43 `trace_four_iff`：`trace = k + 1 + Δλ_min`，`trace = 4` 只是条目约束）；
   数值同为 4 但**不声称同源**——§26 已禁「计数对象」与「矩阵块」互推，此处同样不混。
3. 只做 `SO(2)`（`det = 1`）分支；`det = −1` 的反射分支未展开。
4. 不把 `θ` 的四个离散值指认为任何物理相位；不做物理指认。
-/

import MUFPFormalization.LengthConstraintAudit
import Mathlib.Tactic

namespace MUFPF.QuarterTurnQuantizationAudit

open MUFPF.DeltaInvarianceAudit (alp dlt)
open MUFPF.LengthConstraintAudit (orth_forces_rotation_form)
open MUFPF.IntertwinerRepairAudit (rotGen)

/-- 载体槽数：`Fin 2 ⊕ Fin 2` 共 4 槽（本批唯一用到的「4」的来源）。 -/
theorem carrier_slots_four : Fintype.card (Fin 2 ⊕ Fin 2) = 4 := by
  simp [Fintype.card_sum]

/-- `(x·1 + y·A)² = (x² − y²)·1 + 2xy·A`（`A² = −1` 的展开）。 -/
theorem rot_combo_sq (x y : ℝ) :
    (x • (1 : Matrix (Fin 2) (Fin 2) ℝ) + y • rotGen) ^ 2
      = (x * x - y * y) • (1 : Matrix (Fin 2) (Fin 2) ℝ) + (2 * (x * y)) • rotGen := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [rotGen, pow_two, Matrix.mul_apply, Fin.sum_univ_two, Matrix.one_apply] <;> ring

/-- `M⁴ = (M²)²`（`4 = 2·2`）。 -/
theorem pow_four_eq_sq_sq (M : Matrix (Fin 2) (Fin 2) ℝ) : M ^ 4 = (M ^ 2) ^ 2 := by
  have h : (4 : ℕ) = 2 * 2 := by norm_num
  rw [h, pow_mul]

/-- ★★ **四次幂的闭式**（量化定理的代数骨架）：
    `(x·1 + y·A)⁴ = ((x²−y²)² − (2xy)²)·1 + 2(x²−y²)(2xy)·A`。 -/
theorem rot_combo_four (x y : ℝ) :
    (x • (1 : Matrix (Fin 2) (Fin 2) ℝ) + y • rotGen) ^ 4
      = ((x * x - y * y) * (x * x - y * y) - (2 * (x * y)) * (2 * (x * y)))
          • (1 : Matrix (Fin 2) (Fin 2) ℝ)
        + (2 * ((x * x - y * y) * (2 * (x * y)))) • rotGen := by
  rw [pow_four_eq_sq_sq, rot_combo_sq]
  rw [rot_combo_sq (x * x - y * y) (2 * (x * y))]

/-- 四次幂的 `(0,1)` 条目：`A` 方向系数。 -/
theorem combo_four_zero_one (x y : ℝ) :
    ((x • (1 : Matrix (Fin 2) (Fin 2) ℝ) + y • rotGen) ^ 4) 0 1
      = 2 * ((x * x - y * y) * (2 * (x * y))) := by
  rw [rot_combo_four]
  simp [Matrix.add_apply, Matrix.smul_apply, rotGen]

/-- 四次幂的 `(0,0)` 条目：`1` 方向系数。 -/
theorem combo_four_zero_zero (x y : ℝ) :
    ((x • (1 : Matrix (Fin 2) (Fin 2) ℝ) + y • rotGen) ^ 4) 0 0
      = ((x * x - y * y) * (x * x - y * y) - (2 * (x * y)) * (2 * (x * y))) := by
  rw [rot_combo_four]
  simp [Matrix.add_apply, Matrix.smul_apply, rotGen]

/-- ★★ **判①：量化**。`BᵀB = 1 ∧ det B = 1 ∧ B⁴ = 1` ⟹
    `(α, δ) ∈ {(1,0), (0,1), (−1,0), (0,−1)}`，即 `θ ∈ {0, π/2, π, 3π/2}`。 -/
theorem quarter_turn_quantization (B : Matrix (Fin 2) (Fin 2) ℝ)
    (hgram : B.transpose * B = 1) (hdet : Matrix.det B = 1) (h4 : B ^ 4 = 1) :
    (alp B = 1 ∧ dlt B = 0) ∨ (alp B = 0 ∧ dlt B = 1) ∨
      (alp B = -1 ∧ dlt B = 0) ∨ (alp B = 0 ∧ dlt B = -1) := by
  obtain ⟨-, -, hcirc, hform⟩ := orth_forces_rotation_form B hgram hdet
  set a := alp B with ha
  set d := dlt B with hd
  rw [hform] at h4
  have hcircle : a * a + d * d = 1 := by simpa [ha, hd] using hcirc
  -- `B⁴ = 1` 的 (0,1) 条目 ⟹ αδ(α²−δ²) = 0
  have e01 : (a * a - d * d) * (a * d) = 0 := by
    have h := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 0 1) h4
    rw [combo_four_zero_one] at h
    have hone : (1 : Matrix (Fin 2) (Fin 2) ℝ) 0 1 = 0 := by simp
    rw [hone] at h
    nlinarith [h]
  -- `B⁴ = 1` 的 (0,0) 条目 ⟹ (α²−δ²)² − (2αδ)² = 1
  have e00 : (a * a - d * d) * (a * a - d * d) - (2 * (a * d)) * (2 * (a * d)) = 1 := by
    have h := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 0 0) h4
    rw [combo_four_zero_zero] at h
    simpa [Matrix.one_apply] using h
  by_cases had : a * d = 0
  · rcases mul_eq_zero.mp had with ha0 | hd0
    · -- a = 0 ⟹ d = ±1
      have hdd : d * d = 1 := by nlinarith [hcircle, ha0]
      have hfac : (d - 1) * (d + 1) = 0 := by nlinarith [hdd]
      rcases mul_eq_zero.mp hfac with h | h
      · refine Or.inr (Or.inl ⟨ha0, ?_⟩)
        linarith
      · refine Or.inr (Or.inr (Or.inr ⟨ha0, ?_⟩))
        linarith
    · -- d = 0 ⟹ a = ±1
      have haa : a * a = 1 := by nlinarith [hcircle, hd0]
      have hfac : (a - 1) * (a + 1) = 0 := by nlinarith [haa]
      rcases mul_eq_zero.mp hfac with h | h
      · refine Or.inl ⟨?_, hd0⟩
        linarith
      · refine Or.inr (Or.inr (Or.inl ⟨?_, hd0⟩))
        linarith
  · -- αδ ≠ 0：由 e01 得 α² = δ²，再被 e00 判死
    exfalso
    have hx : a * a - d * d = 0 := by
      rcases mul_eq_zero.mp e01 with h | h
      · linarith
      · exact absurd h had
    nlinarith [e00, hx, sq_nonneg (2 * (a * d))]

/-- ★★ **判②：四个值**。`B ∈ {1, −1, rotGen, −rotGen}`。 -/
theorem coupling_four_values (B : Matrix (Fin 2) (Fin 2) ℝ)
    (hgram : B.transpose * B = 1) (hdet : Matrix.det B = 1) (h4 : B ^ 4 = 1) :
    B = 1 ∨ B = -1 ∨ B = rotGen ∨ B = -rotGen := by
  obtain ⟨-, -, -, hform⟩ := orth_forces_rotation_form B hgram hdet
  rcases quarter_turn_quantization B hgram hdet h4 with ⟨ha, hd⟩ | ⟨ha, hd⟩ | ⟨ha, hd⟩ | ⟨ha, hd⟩
  · left
    rw [hform]
    simp [ha, hd]
  · right; right; left
    rw [hform]
    simp [ha, hd]
  · right; left
    rw [hform]
    simp [ha, hd]
  · right; right; right
    rw [hform]
    simp [ha, hd]

/-- ★★ **判③：非平凡耦合只剩一个符号位**（`ℤ/2`）：
    `rotGen ≠ 0`、`(−1)·rotGen = −rotGen`、翻转两次复原。 -/
theorem nontrivial_coupling_is_one_bit :
    rotGen ≠ 0 ∧ ((-1 : ℝ) • rotGen = -rotGen) ∧
      ((-1 : ℝ) • ((-1 : ℝ) • rotGen) = rotGen) := by
  refine ⟨?_, ?_, ?_⟩
  · intro h
    have := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 0 1) h
    simp [rotGen] at this
  · simp
  · simp

/-- **R-o 判决汇总**：
    ① 量化：`BᵀB = 1 ∧ det B = 1 ∧ B⁴ = 1` ⟹ `(α,δ)` 只取四个离散值；
    ② 取值枚举：`B ∈ {1, −1, rotGen, −rotGen}`；
    ③ 非平凡耦合的差只剩一个符号位（`ℤ/2`）。 -/
theorem quarter_turn_verdict :
    (∀ B : Matrix (Fin 2) (Fin 2) ℝ,
        B.transpose * B = 1 → Matrix.det B = 1 → B ^ 4 = 1 →
          (alp B = 1 ∧ dlt B = 0) ∨ (alp B = 0 ∧ dlt B = 1) ∨
            (alp B = -1 ∧ dlt B = 0) ∨ (alp B = 0 ∧ dlt B = -1)) ∧
      (∀ B : Matrix (Fin 2) (Fin 2) ℝ,
        B.transpose * B = 1 → Matrix.det B = 1 → B ^ 4 = 1 →
          B = 1 ∨ B = -1 ∨ B = rotGen ∨ B = -rotGen) ∧
      (rotGen ≠ 0 ∧ ((-1 : ℝ) • rotGen = -rotGen) ∧
        ((-1 : ℝ) • ((-1 : ℝ) • rotGen) = rotGen)) :=
  ⟨quarter_turn_quantization, coupling_four_values, nontrivial_coupling_is_one_bit⟩

end MUFPF.QuarterTurnQuantizationAudit
