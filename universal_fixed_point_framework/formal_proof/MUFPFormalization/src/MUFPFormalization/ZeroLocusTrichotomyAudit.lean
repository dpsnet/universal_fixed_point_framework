/-
  ZeroLocusTrichotomyAudit.lean — R-ac2：三类型归零集的三分（§51）
  ==========================================================================

## 问题

§50 只做了标量型，把 §48 的「一般幅度让步」精确化到两个点；§50.7-1 留着的开口是：
转动型、混型的归零集未机检。本批补满，并给出三类型的对照表。

## 结果

| 型 | `t = 1` 读数 | `t = 1+h` 读数 | 归零集（`bc` 或 `pq`） |
| --- | --- | --- | --- |
| 纯标量 | `pq(pq−h)` | `pq(pq−h−h²)` | `{0, h}` / `{0, h+h²}` |
| 纯转动 | `bc(bc−h)` | `bc(bc−h+h²)` | `{0, h}` / `{0, h−h²}` |
| 混型 | `(bc)²` | `(bc)²` | `{0}` / `{0}` |

## 判决

1. **归零集三分**：纯型各有两个归零点（一个恒为 `0`，另一个随型不同而落在 `h±h²`），
   混型只有一个（`bc = 0`）。
2. **三个非零归零点互不相同且有序**：`h − h² < h < h + h²`（差均为 `h² ≈ 0.014886`）。
   于是「读数为零」在这两个退化点上至多区分出三个幅度值，与 §49 的「差恒等式变号两次」互不冲突。
3. **混型在非零耦合下永不归零**（读数恒 `≥ 0`，且只在 `bc = 0` 取到 `0`）——
   这是 §47「混型谱最脏（四根全复）」的对照面：**谱最脏者读数最稳**，纯型反过来（谱可分离但读数可被调到零）。
4. 本批不裁决任何理论选择；「读数非零是否升格为公设」仍属用户裁决范围（§50.3 已登记）。

## 诚实边界

1. 混型只取 `B = diag2 b b`、`C = 反对角 c`（§48 的取法）；反向取法（`B` 转动、`C` 标量）由
   `(bc)²` 的对称性应同结论，**未逐条机检**。
2. 「归零」仍指单点位移矩阵奇异（该点成为特征根），不是谱退化。
3. 不新增常数、不新增公设。
-/

import MUFPFormalization.ReadingZeroAudit
import Mathlib.Tactic

set_option warn.classDefReducibility false
set_option linter.unusedSimpArgs false
set_option linter.unusedTactic false
set_option linter.unreachableTactic false
set_option linter.style.haveILetI false

namespace MUFPF.ZeroLocusTrichotomyAudit

open MUFPF.IntertwinerExistenceAudit (diag2)
open MUFPF.LayeredCarrierAudit (blk)
open MUFPF.GNBridgeAudit (dlmin dlmin_pos)
open MUFPF.SmRootAudit (rotation_reading_at_one rotation_reading_at_sm_root
  mixed_reading_at_one mixed_reading_at_sm_root)
open MUFPF.ReadingZeroAudit (gap_sq_lt_gap gap_lt_one gap_add_sq_lt_one)

abbrev M4 : Type := Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ

/-- 纯转动型载体。 -/
noncomputable abbrev rotBlk (b c : ℝ) : M4 :=
  blk (diag2 (0 : ℝ) 2) (!![(0 : ℝ), b; -b, 0]) (!![(0 : ℝ), c; -c, 0])
    (diag2 (1 : ℝ) (1 + dlmin))

/-- 混型载体（`B` 标量、`C` 转动）。 -/
noncomputable abbrev mixBlk (b c : ℝ) : M4 :=
  blk (diag2 (0 : ℝ) 2) (diag2 b b) (!![(0 : ℝ), c; -c, 0])
    (diag2 (1 : ℝ) (1 + dlmin))

/-! ## 纯转动型 -/

/-- ★ **纯转动型 `t = 1` 归零 ⟺ `bc = 0` 或 `bc = Δλ_min`**。 -/
theorem rotation_zero_at_one_iff (b c : ℝ) :
    Matrix.det ((1 : ℝ) • (1 : M4) - rotBlk b c) = 0 ↔
      b * c = 0 ∨ b * c = dlmin := by
  rw [rotation_reading_at_one b c]
  constructor
  · intro hzero
    rcases mul_eq_zero.mp hzero with h0 | h0
    · exact Or.inl h0
    · exact Or.inr (sub_eq_zero.mp h0)
  · rintro (h0 | h0)
    · rw [h0]; ring
    · have : b * c - dlmin = 0 := sub_eq_zero.mpr h0
      rw [this]; ring

/-- ★ **纯转动型 `t = 1+Δλ_min` 归零 ⟺ `bc = 0` 或 `bc = Δλ_min − Δλ_min²`**。 -/
theorem rotation_zero_at_sm_root_iff (b c : ℝ) :
    Matrix.det ((1 + dlmin) • (1 : M4) - rotBlk b c) = 0 ↔
      b * c = 0 ∨ b * c = dlmin - dlmin ^ 2 := by
  rw [rotation_reading_at_sm_root b c]
  constructor
  · intro hzero
    rcases mul_eq_zero.mp hzero with h0 | h0
    · exact Or.inl h0
    · exact Or.inr (sub_eq_zero.mp (by linarith [h0]))
  · rintro (h0 | h0)
    · rw [h0]; ring
    · have : b * c - dlmin + dlmin ^ 2 = 0 := by rw [h0]; ring
      rw [this]; ring

/-! ## 混型 -/

/-- ★ **混型 `t = 1` 归零 ⟺ `bc = 0`**（读数恰为 `(bc)²`，对 `Δλ_min` 全盲）。 -/
theorem mixed_zero_at_one_iff (b c : ℝ) :
    Matrix.det ((1 : ℝ) • (1 : M4) - mixBlk b c) = 0 ↔ b * c = 0 := by
  rw [mixed_reading_at_one b c, pow_two]
  exact mul_self_eq_zero

/-- ★ **混型 `t = 1 + Δλ_min` 归零 ⟺ `bc = 0`**。 -/
theorem mixed_zero_at_sm_root_iff (b c : ℝ) :
    Matrix.det ((1 + dlmin) • (1 : M4) - mixBlk b c) = 0 ↔ b * c = 0 := by
  rw [mixed_reading_at_sm_root b c, pow_two]
  exact mul_self_eq_zero

/-- 非零混型耦合在两点上都不归零。 -/
theorem mixed_never_zero_of_ne (b c : ℝ) (hbc : b * c ≠ 0) :
    Matrix.det ((1 : ℝ) • (1 : M4) - mixBlk b c) ≠ 0 ∧
      Matrix.det ((1 + dlmin) • (1 : M4) - mixBlk b c) ≠ 0 := by
  constructor
  · intro hzero; exact hbc ((mixed_zero_at_one_iff b c).mp hzero)
  · intro hzero; exact hbc ((mixed_zero_at_sm_root_iff b c).mp hzero)

/-! ## 三个非零归零点的次序 -/

/-- `Δλ_min² > 0`。 -/
theorem gap_sq_pos : 0 < dlmin ^ 2 := by
  have := dlmin_pos; positivity

/-- `Δλ_min − Δλ_min² > 0`（转动型 `t = 1+h` 的非零归零点为正）。 -/
theorem gap_sub_sq_pos : 0 < dlmin - dlmin ^ 2 := by
  have hlt : dlmin ^ 2 < dlmin := gap_sq_lt_gap
  linarith

/-- ★ **三个非零归零点严格有序**：`h − h² < h < h + h²`。 -/
theorem zero_points_ordered :
    dlmin - dlmin ^ 2 < dlmin ∧ dlmin < dlmin + dlmin ^ 2 := by
  have h1 : 0 < dlmin ^ 2 := gap_sq_pos
  have h2 : 0 < dlmin ^ 2 := h1
  constructor <;> linarith

/-- 三个非零归零点两两不等。 -/
theorem zero_points_pairwise_distinct :
    dlmin - dlmin ^ 2 ≠ dlmin ∧ dlmin ≠ dlmin + dlmin ^ 2 ∧
      dlmin - dlmin ^ 2 ≠ dlmin + dlmin ^ 2 := by
  have h := zero_points_ordered
  constructor
  · linarith [h.1]
  constructor
  · linarith [h.2]
  · linarith [h.1, h.2]

/-! ## 判决 -/

/-- ★★ **归零集三分判决**：
    纯标量两点 `{0, h}`/`{0, h+h²}`、纯转动两点 `{0, h}`/`{0, h−h²}`、混型单点 `{0}`；
    三个非零归零点严格有序且两两不等；非零耦合的混型永不归零。 -/
theorem zero_locus_trichotomy_verdict :
    (∀ p q : ℝ, (Matrix.det ((1 : ℝ) • (1 : M4) -
        blk (diag2 (0 : ℝ) 2) (diag2 p p) (diag2 q q) (diag2 (1 : ℝ) (1 + dlmin))) = 0 ↔
      p * q = 0 ∨ p * q = dlmin)) ∧
    (∀ b c : ℝ, (Matrix.det ((1 : ℝ) • (1 : M4) - rotBlk b c) = 0 ↔
      b * c = 0 ∨ b * c = dlmin)) ∧
    (∀ b c : ℝ, (Matrix.det ((1 + dlmin) • (1 : M4) - rotBlk b c) = 0 ↔
      b * c = 0 ∨ b * c = dlmin - dlmin ^ 2)) ∧
    (∀ b c : ℝ, (Matrix.det ((1 : ℝ) • (1 : M4) - mixBlk b c) = 0 ↔ b * c = 0)) ∧
    (∀ b c : ℝ, (Matrix.det ((1 + dlmin) • (1 : M4) - mixBlk b c) = 0 ↔ b * c = 0)) ∧
    (dlmin - dlmin ^ 2 < dlmin ∧ dlmin < dlmin + dlmin ^ 2) ∧
    (∀ b c : ℝ, b * c ≠ 0 →
      Matrix.det ((1 : ℝ) • (1 : M4) - mixBlk b c) ≠ 0 ∧
        Matrix.det ((1 + dlmin) • (1 : M4) - mixBlk b c) ≠ 0) :=
  ⟨MUFPF.ReadingZeroAudit.scalar_zero_at_one_iff,
    rotation_zero_at_one_iff, rotation_zero_at_sm_root_iff,
    mixed_zero_at_one_iff, mixed_zero_at_sm_root_iff,
    zero_points_ordered, mixed_never_zero_of_ne⟩

end MUFPF.ZeroLocusTrichotomyAudit
