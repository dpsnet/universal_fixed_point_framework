/-
  ReadingZeroAudit.lean — R-ac：标量读数的归零集与量化可达性（§50）
  ==========================================================================

## 问题

§48 的「诚实边界 2」写下了唯一一处对**一般幅度**的让步：

> 非零性只对单位幅度（`bc = 1`）机检；一般幅度 `bc` 可取使读数归零的值
> （如标量型 `pq = h + h²`），故「`1 + h` 不是特征根」是**对框架量子化耦合**而言的结论，不是全称命题。

本批把这个让步**精确化并机检**：把「归零」从一句警告变成一个**确定的集合**——

> 标量型读数在退化点上归零 ⟺ 耦合乘积 `pq` 等于谱间隙的某个具体值。

## 结果

`t = 1`：`det (1•1₄ − M_scalar(p,q)) = pq·(pq − Δλ_min)` ⟹ 归零 ⟺ `pq ∈ {0, Δλ_min}`。
`t = 1 + Δλ_min`：`det = pq·(pq − Δλ_min − Δλ_min²)` ⟹ 归零 ⟺ `pq ∈ {0, Δλ_min(1+Δλ_min)}`。

## 判决

1. **归零集是两点集，且两点都由 `Δλ_min` 生成**（`0` 与 `Δλ_min`、`Δλ_min(1+Δλ_min)`）——
   「读数归零」不是任意幅度都能碰到的软条件，而是把**耦合乘积**与**谱间隙**直接绑定的硬约束。
2. **框架量子化幅度（`pq = ±1`）在两点上全不归零**：`1 − Δλ_min > 0`、`1 + Δλ_min > 0`、
   `1 − Δλ_min − Δλ_min² > 0`、`1 + Δλ_min + Δλ_min² > 0`（前两者由 `Δλ_min < 1`，第三由 `Δλ_min < 1/2`）。
   于是 §48 的「对框架量子化耦合成立」不仅是措辞，是可机检的范围声明。
3. **归零条件本身可以当作一条候选判据**：若要求「退化点上读数非零」，则 `pq ≠ Δλ_min`（且 `≠ 0`）。
   这与 §26–§27 的 `B_耦合` 悬案同型——但本批**只登记候选，不裁决**：`pq` 是否应当等于 `Δλ_min` 属用户裁决范围。

## 诚实边界

1. 只做**标量型**（`B = diag2 p p`、`C = diag2 q q`）；转动型与混型的归零集未在本批展开
   （§48 的转动读数 `bc(bc − h)`、混型 `(bc)²` 结构上不同：转动型同样在 `bc = h` 归零，混型只在 `bc = 0`）。
2. 归零是**单点读数**归零，不是谱退化：`det = 0` 表示该位移矩阵奇异，即该点成为特征根；这与 §48 的
   「两个退化点都不是特征根」不冲突——后者是对 `pq = 1` 而言的。
3. 不新增常数、不新增公设；`Δλ_min` 只引 `GNBridgeAudit.dlmin`。
-/

import MUFPFormalization.SmRootAudit
import Mathlib.Tactic

set_option warn.classDefReducibility false
set_option linter.unusedSimpArgs false
set_option linter.unusedTactic false
set_option linter.unreachableTactic false
set_option linter.style.haveILetI false

namespace MUFPF.ReadingZeroAudit

open MUFPF.IntertwinerExistenceAudit (diag2 dlmin_in_unit_interval)
open MUFPF.LayeredCarrierAudit (blk)
open MUFPF.GNBridgeAudit (dlmin dlmin_pos)
open MUFPF.SmRootAudit (scalar_reading_at_one scalar_reading_at_sm_root dlmin_lt_half)

abbrev M4 : Type := Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ

/-- 标量型载体：`B = diag2 p p`、`C = diag2 q q`。 -/
noncomputable abbrev scalBlk (p q : ℝ) : M4 :=
  blk (diag2 (0 : ℝ) 2) (diag2 p p) (diag2 q q) (diag2 (1 : ℝ) (1 + dlmin))

/-! ## 归零集（两个退化点） -/

/-- ★ **`t = 1` 处归零 ⟺ `pq = 0` 或 `pq = Δλ_min`**。 -/
theorem scalar_zero_at_one_iff (p q : ℝ) :
    Matrix.det ((1 : ℝ) • (1 : M4) - scalBlk p q) = 0 ↔
      p * q = 0 ∨ p * q = dlmin := by
  rw [scalar_reading_at_one p q]
  constructor
  · intro hzero
    rcases mul_eq_zero.mp hzero with h0 | h0
    · exact Or.inl h0
    · exact Or.inr (sub_eq_zero.mp h0)
  · rintro (h0 | h0)
    · rw [h0]; ring
    · have : p * q - dlmin = 0 := sub_eq_zero.mpr h0
      rw [this]; ring

/-- ★ **`t = 1 + Δλ_min` 处归零 ⟺ `pq = 0` 或 `pq = Δλ_min(1+Δλ_min)`**。 -/
theorem scalar_zero_at_sm_root_iff (p q : ℝ) :
    Matrix.det ((1 + dlmin) • (1 : M4) - scalBlk p q) = 0 ↔
      p * q = 0 ∨ p * q = dlmin + dlmin ^ 2 := by
  rw [scalar_reading_at_sm_root p q]
  constructor
  · intro hzero
    rcases mul_eq_zero.mp hzero with h0 | h0
    · exact Or.inl h0
    · exact Or.inr (sub_eq_zero.mp (by linarith [h0]))
  · rintro (h0 | h0)
    · rw [h0]; ring
    · have : p * q - dlmin - dlmin ^ 2 = 0 := by rw [h0]; ring
      rw [this]; ring

/-! ## 间隙界的机检 -/

/-- `Δλ_min < 1`（`dlmin_in_unit_interval` 的上界）。 -/
theorem gap_lt_one : dlmin < 1 := dlmin_in_unit_interval.2

/-- `Δλ_min² < Δλ_min`（由 `0 < Δλ_min < 1`）。 -/
theorem gap_sq_lt_gap : dlmin ^ 2 < dlmin := by
  have h := mul_lt_mul_of_pos_left gap_lt_one dlmin_pos
  simpa [pow_two] using h

/-- `Δλ_min + Δλ_min² < 1`（由 `Δλ_min < 1/2`）。 -/
theorem gap_add_sq_lt_one : dlmin + dlmin ^ 2 < 1 := by
  have h2 : dlmin ^ 2 < dlmin := gap_sq_lt_gap
  linarith [dlmin_lt_half, h2]

/-! ## 框架量子化幅度（`pq = ±1`）的非零性 -/

/-- `pq = 1` 时 `t = 1` 读数非零：`1 − Δλ_min ≠ 0`。 -/
theorem pq_one_reading_at_one_ne_zero (p q : ℝ) (hpq : p * q = 1) :
    Matrix.det ((1 : ℝ) • (1 : M4) - scalBlk p q) ≠ 0 := by
  rw [scalar_reading_at_one p q, hpq]
  have hlt : dlmin < 1 := gap_lt_one
  intro hzero
  nlinarith [hzero, hlt]

/-- `pq = −1` 时 `t = 1` 读数非零：`1 + Δλ_min ≠ 0`。 -/
theorem pq_neg_one_reading_at_one_ne_zero (p q : ℝ) (hpq : p * q = -1) :
    Matrix.det ((1 : ℝ) • (1 : M4) - scalBlk p q) ≠ 0 := by
  rw [scalar_reading_at_one p q, hpq]
  intro hzero
  nlinarith [hzero, dlmin_pos]

/-- `pq = 1` 时 `t = 1 + Δλ_min` 读数非零：`1 − Δλ_min − Δλ_min² ≠ 0`。 -/
theorem pq_one_reading_at_sm_root_ne_zero (p q : ℝ) (hpq : p * q = 1) :
    Matrix.det ((1 + dlmin) • (1 : M4) - scalBlk p q) ≠ 0 := by
  rw [scalar_reading_at_sm_root p q, hpq]
  have hlt : dlmin + dlmin ^ 2 < 1 := gap_add_sq_lt_one
  intro hzero
  linarith [hzero, hlt]

/-- `pq = −1` 时 `t = 1 + Δλ_min` 读数非零：`1 + Δλ_min + Δλ_min² ≠ 0`。 -/
theorem pq_neg_one_reading_at_sm_root_ne_zero (p q : ℝ) (hpq : p * q = -1) :
    Matrix.det ((1 + dlmin) • (1 : M4) - scalBlk p q) ≠ 0 := by
  rw [scalar_reading_at_sm_root p q, hpq]
  intro hzero
  nlinarith [hzero, dlmin_pos]

/-! ## 判决 -/

/-- ★★ **归零判决**：
    (1) 两个退化点的归零集恰为 `{0, Δλ_min}` 与 `{0, Δλ_min(1+Δλ_min)}`（由 `*_iff`）；
    (2) 框架量子化幅度 `pq = ±1` 在两点上都非零（四款并列）；
    (3) 归零条件把耦合乘积与谱间隙绑定，登记为 `B_耦合` 的候选判据（不裁决）。 -/
theorem reading_zero_verdict :
    (∀ p q : ℝ, (Matrix.det ((1 : ℝ) • (1 : M4) - scalBlk p q) = 0 ↔
        p * q = 0 ∨ p * q = dlmin)) ∧
    (∀ p q : ℝ, (Matrix.det ((1 + dlmin) • (1 : M4) - scalBlk p q) = 0 ↔
        p * q = 0 ∨ p * q = dlmin + dlmin ^ 2)) ∧
    (0 < dlmin ∧ dlmin < 1 ∧ dlmin + dlmin ^ 2 < 1) ∧
    (∀ p q : ℝ, p * q = 1 → Matrix.det ((1 : ℝ) • (1 : M4) - scalBlk p q) ≠ 0) ∧
    (∀ p q : ℝ, p * q = -1 → Matrix.det ((1 : ℝ) • (1 : M4) - scalBlk p q) ≠ 0) ∧
    (∀ p q : ℝ, p * q = 1 →
        Matrix.det ((1 + dlmin) • (1 : M4) - scalBlk p q) ≠ 0) ∧
    (∀ p q : ℝ, p * q = -1 →
        Matrix.det ((1 + dlmin) • (1 : M4) - scalBlk p q) ≠ 0) :=
  ⟨scalar_zero_at_one_iff, scalar_zero_at_sm_root_iff,
    ⟨dlmin_pos, gap_lt_one, gap_add_sq_lt_one⟩,
    pq_one_reading_at_one_ne_zero, pq_neg_one_reading_at_one_ne_zero,
    pq_one_reading_at_sm_root_ne_zero, pq_neg_one_reading_at_sm_root_ne_zero⟩

end MUFPF.ReadingZeroAudit
