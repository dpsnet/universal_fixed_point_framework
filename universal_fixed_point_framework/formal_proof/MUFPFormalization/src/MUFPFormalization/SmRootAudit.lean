/-
  SmRootAudit.lean — R-bb：在 D 侧退化点上换主轴（§48）
  ==================================================================

## 问题

§46/§47 的三条闭式都只在 `t ≠ 1`、`t ≠ 1 + Δλ_min` 上机检，因为所用的 Schur 分解
`det (t•1₄ − M) = det (t•1 − D)·det (t•1 − A − B·⅟(t•1−D)·C)` 需要 `t•1 − D` 可逆，
而 `D = A_SM` 的两个根正是 `1` 与 `1 + Δλ_min`。于是 §46 把
`SPECTRUM_TWO_WAY_AT_SM_ROOT`（`t = 1 + Δλ_min` 时的读数）登记为开口。

## 做法

换主轴：改用**另一个 Schur 形式**
`det (blk A B C D) = det A · det (D − C·⅟A·B)`（Mathlib `det_fromBlocks₁₁`，需 `[Invertible A]`）。
在 `t = 1 + Δλ_min` 处 `t•1 − A_GR = diag(1+Δλ_min, Δλ_min − 1)`，两个对角元都非零，
故 A 侧可逆——退化点因此**只在 D 侧退化**。

## 结果（三条读数，均在 `t = 1 + Δλ_min`、A 侧 Schur）

- 纯标量（`B = diag2 p p`、`C = diag2 q q`）：`det = pq·(pq − Δλ_min − Δλ_min²)`；
- 纯转动（`B = b·A`、`C = c·A`）：`det = bc·(bc − Δλ_min + Δλ_min²)`；
- 混型（`B = diag2 b b`、`C = c·A`）：`det = (bc)²`。

三条都与 §46/§47 的闭式在该点的求值**逐项一致**（闭式在 `t = 1+Δλ_min` 处：
标量 `bc − h − h²`、转动 `bc(bc − h + h²)`、混型 `(bc)²`，因为混型的 `t(t−1)(t−2)(t−(1+h))` 项恰好归零）。
单位幅度（`bc = 1`）下三条读数分别为 `1 − h − h² ≈ 0.8631`、`1 − h + h² ≈ 0.8929`、`1`，
**全部非零** ⟹ `1 + Δλ_min` 在三类耦合下都不是双向载体特征根。

## 判决

- `t = 1 + Δλ_min` 处的「谱退化」是**工具退化**（Schur 主轴选择所致），不是谱本身的奇点：
  换主轴即得干净读数，闭式在该点连续延拓成立。
- 三条读数都非零 ⟹ 混型最强（`(bc)²`，与 `h` 完全无关）、纯型各带一项 `±h²` 修正；
  `h` 的符号在两类纯型里**相反**（标量 `−h²`、转动 `+h²`），这是 §47 三条闭式在终点的指纹。
- `SPECTRUM_TWO_WAY_AT_SM_ROOT` 由此收口：该点既不产生新根，也不使读数归零。

## 诚实边界

1. `det_blk_schur_left` 需 `[Invertible A]`；本批只在 `t = 1 + Δλ_min` 一处实例化，
   不主张「任意 `t` 都能换主轴」（在 `t = 1` 处 A 侧也退化，两侧同时退化时两条 Schur 都不适用）。
2. 非零性只对**单位幅度**（`bc = 1`）机检；一般幅度 `bc` 可取使读数归零的值
   （如标量型 `pq = h + h²`），故「`1 + h` 不是特征根」是**对框架量子化耦合**而言的结论，不是全称命题。
3. 不引入新常数、不新增公设；`bc` 仍无内生来源（§26–§27 悬案）。
-/

import MUFPFormalization.PureTypeSpectrumAudit
import Mathlib.Tactic

set_option warn.classDefReducibility false
set_option linter.unusedSimpArgs false
set_option linter.unusedTactic false
set_option linter.unreachableTactic false
set_option linter.style.haveILetI false

namespace MUFPF.SmRootAudit

open MUFPF.IntertwinerExistenceAudit (diag2 dlmin_in_unit_interval)
open MUFPF.LayeredCarrierAudit (blk)
open MUFPF.IntertwinerRepairAudit (rotGen)
open MUFPF.CarrierDetAudit (det_diag2)
open MUFPF.SchurCarrierAudit (blk_eq_fromBlocks_gen)
open MUFPF.TwoWayCarrierAudit (diag2_mul_diag2 diag2_sub_diag2)
open MUFPF.TwoWaySpectrumAudit (instDiagInv shift_blk_gen neg_sandwich)
open MUFPF.ScalarReadoutAudit (shift_diag2)
open MUFPF.PureTypeSpectrumAudit (rot_conj_diag diag2_sub_antidiag)
open MUFPF.GNBridgeAudit (dlmin dlmin_pos dlmin_sq_eq)

abbrev M2 : Type := Matrix (Fin 2) (Fin 2) ℝ
abbrev M4 : Type := Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ

/-! ## A 侧 Schur 形式（新工具） -/

/-- ★ **A 侧 Schur 分解**：`det (blk A B C D) = det A · det (D − C·⅟A·B)`（`A` 可逆）。
    这是 §46/§47 所用 D 侧形式的对偶；D 侧在 `t = 1`、`t = 1+Δλ_min` 处退化时，A 侧仍可逆。 -/
theorem det_blk_schur_left (A B C D : M2) [Invertible A] :
    Matrix.det (blk A B C D) = Matrix.det A * Matrix.det (D - C * ⅟A * B) := by
  rw [blk_eq_fromBlocks_gen A B C D]
  exact Matrix.det_fromBlocks₁₁ A B C D

/-! ## 退化点上的两个位移块 -/

/-- `t = 1 + Δλ_min` 处 `t•1 − A_GR = diag(1+h, h−1)`：两个对角元都非零（h>0、h−1<0）。 -/
theorem shift_gr_at_sm_root :
    (1 + dlmin) • (1 : M2) - diag2 (0 : ℝ) 2 = diag2 (1 + dlmin) (dlmin - 1) := by
  rw [shift_diag2 (1 + dlmin) 0 2, sub_zero]
  rw [show (1 + dlmin) - 2 = dlmin - 1 from by ring]

/-- `t = 1 + Δλ_min` 处 `t•1 − A_SM = diag(h, 0)`：D 侧奇异（正是需换主轴的原因）。 -/
theorem shift_sm_at_sm_root :
    (1 + dlmin) • (1 : M2) - diag2 (1 : ℝ) (1 + dlmin) = diag2 dlmin 0 := by
  rw [shift_diag2 (1 + dlmin) 1 (1 + dlmin), sub_self]
  rw [show (1 + dlmin) - 1 = dlmin from by ring]

/-- 反对角乘对角块的**一般**形式（两个对角元不等）：
    `!![0,a;−b,0] · diag(p,q) = !![0, a·q; −(b·p), 0]`。 -/
theorem antidiag_mul_diag2 (a b p q : ℝ) :
    (!![(0 : ℝ), a; -b, 0]) * diag2 p q = !![(0 : ℝ), a * q; -(b * p), 0] := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [diag2, Matrix.mul_apply, Fin.sum_univ_two] <;> ring

/-! ## 三条读数（`t = 1 + Δλ_min`，A 侧 Schur） -/

/-- ★★ **纯标量耦合在 `t = 1+Δλ_min` 的读数**：`det = pq·(pq − Δλ_min − Δλ_min²)`。 -/
theorem scalar_reading_at_sm_root (p q : ℝ) :
    Matrix.det ((1 + dlmin) • (1 : M4) -
        blk (diag2 (0 : ℝ) 2) (diag2 p p) (diag2 q q) (diag2 (1 : ℝ) (1 + dlmin))) =
      p * q * (p * q - dlmin - dlmin ^ 2) := by
  have h1 : (1 + dlmin) ≠ 0 := by linarith [dlmin_pos]
  have h2 : dlmin - 1 ≠ 0 := by have := dlmin_in_unit_interval.2; linarith
  rw [shift_blk_gen, shift_gr_at_sm_root, shift_sm_at_sm_root]
  letI := instDiagInv (1 + dlmin) (dlmin - 1) h1 h2
  rw [det_blk_schur_left]
  rw [show ⅟(diag2 (1 + dlmin) (dlmin - 1)) =
      diag2 ((1 + dlmin)⁻¹) ((dlmin - 1)⁻¹) from rfl]
  rw [neg_sandwich (diag2 q q) (diag2 ((1 + dlmin)⁻¹) ((dlmin - 1)⁻¹)) (diag2 p p)]
  rw [diag2_mul_diag2, diag2_mul_diag2]
  rw [diag2_sub_diag2]
  simp only [det_diag2]
  field_simp
  ring_nf

/-- ★★ **纯转动耦合在 `t = 1+Δλ_min` 的读数**：`det = bc·(bc − Δλ_min + Δλ_min²)`。 -/
theorem rotation_reading_at_sm_root (b c : ℝ) :
    Matrix.det ((1 + dlmin) • (1 : M4) -
        blk (diag2 (0 : ℝ) 2) (!![(0 : ℝ), b; -b, 0]) (!![(0 : ℝ), c; -c, 0])
          (diag2 (1 : ℝ) (1 + dlmin))) =
      b * c * (b * c - dlmin + dlmin ^ 2) := by
  have h1 : (1 + dlmin) ≠ 0 := by linarith [dlmin_pos]
  have h2 : dlmin - 1 ≠ 0 := by have := dlmin_in_unit_interval.2; linarith
  rw [shift_blk_gen, shift_gr_at_sm_root, shift_sm_at_sm_root]
  letI := instDiagInv (1 + dlmin) (dlmin - 1) h1 h2
  rw [det_blk_schur_left]
  rw [show ⅟(diag2 (1 + dlmin) (dlmin - 1)) =
      diag2 ((1 + dlmin)⁻¹) ((dlmin - 1)⁻¹) from rfl]
  rw [neg_sandwich (!![(0 : ℝ), c; -c, 0]) (diag2 ((1 + dlmin)⁻¹) ((dlmin - 1)⁻¹))
        (!![(0 : ℝ), b; -b, 0])]
  rw [rot_conj_diag c b ((1 + dlmin)⁻¹) ((dlmin - 1)⁻¹)]
  rw [diag2_sub_diag2]
  simp only [det_diag2]
  field_simp
  ring_nf

/-- ★★ **混型耦合在 `t = 1+Δλ_min` 的读数**：`det = (bc)²`——与 `Δλ_min` 完全无关。 -/
theorem mixed_reading_at_sm_root (b c : ℝ) :
    Matrix.det ((1 + dlmin) • (1 : M4) -
        blk (diag2 (0 : ℝ) 2) (diag2 b b) (!![(0 : ℝ), c; -c, 0])
          (diag2 (1 : ℝ) (1 + dlmin))) =
      (b * c) ^ 2 := by
  have h1 : (1 + dlmin) ≠ 0 := by linarith [dlmin_pos]
  have h2 : dlmin - 1 ≠ 0 := by have := dlmin_in_unit_interval.2; linarith
  rw [shift_blk_gen, shift_gr_at_sm_root, shift_sm_at_sm_root]
  letI := instDiagInv (1 + dlmin) (dlmin - 1) h1 h2
  rw [det_blk_schur_left]
  rw [show ⅟(diag2 (1 + dlmin) (dlmin - 1)) =
      diag2 ((1 + dlmin)⁻¹) ((dlmin - 1)⁻¹) from rfl]
  rw [neg_sandwich (!![(0 : ℝ), c; -c, 0]) (diag2 ((1 + dlmin)⁻¹) ((dlmin - 1)⁻¹))
        (diag2 b b)]
  rw [mul_assoc, diag2_mul_diag2, antidiag_mul_diag2]
  rw [diag2_sub_antidiag, Matrix.det_fin_two_of]
  simp only [det_diag2]
  field_simp
  ring_nf

/-! ## 另一个退化点：`t = 1`（A 侧同样可逆） -/

/-- `t = 1` 处 `1•1 − A_GR = diag(1, −1)`：A 侧可逆（D 侧此时奇异）。 -/
theorem shift_gr_at_one :
    (1 : ℝ) • (1 : M2) - diag2 (0 : ℝ) 2 = diag2 (1 : ℝ) (-1) := by
  rw [shift_diag2 (1 : ℝ) 0 2, sub_zero]
  rw [show (1 : ℝ) - 2 = -1 from by norm_num]

/-- `t = 1` 处 `1•1 − A_SM = diag(0, −Δλ_min)`：D 侧奇异。 -/
theorem shift_sm_at_one :
    (1 : ℝ) • (1 : M2) - diag2 (1 : ℝ) (1 + dlmin) = diag2 (0 : ℝ) (-dlmin) := by
  rw [shift_diag2 (1 : ℝ) 1 (1 + dlmin)]
  rw [show (1 : ℝ) - 1 = 0 from by norm_num]
  rw [show (1 : ℝ) - (1 + dlmin) = -dlmin from by ring]

/-- ★ **纯标量耦合在 `t = 1` 的读数**：`det = pq·(pq − Δλ_min)`。 -/
theorem scalar_reading_at_one (p q : ℝ) :
    Matrix.det ((1 : ℝ) • (1 : M4) -
        blk (diag2 (0 : ℝ) 2) (diag2 p p) (diag2 q q) (diag2 (1 : ℝ) (1 + dlmin))) =
      p * q * (p * q - dlmin) := by
  have h1 : (1 : ℝ) ≠ 0 := one_ne_zero
  have h2 : (-1 : ℝ) ≠ 0 := by norm_num
  rw [shift_blk_gen, shift_gr_at_one, shift_sm_at_one]
  letI := instDiagInv (1 : ℝ) (-1) h1 h2
  rw [det_blk_schur_left]
  rw [show ⅟(diag2 (1 : ℝ) (-1)) = diag2 ((1 : ℝ)⁻¹) ((-1 : ℝ)⁻¹) from rfl]
  rw [neg_sandwich (diag2 q q) (diag2 ((1 : ℝ)⁻¹) ((-1 : ℝ)⁻¹)) (diag2 p p)]
  rw [diag2_mul_diag2, diag2_mul_diag2]
  rw [diag2_sub_diag2]
  simp only [det_diag2]
  field_simp
  ring_nf

/-- ★ **纯转动耦合在 `t = 1` 的读数**：`det = bc·(bc − Δλ_min)`。 -/
theorem rotation_reading_at_one (b c : ℝ) :
    Matrix.det ((1 : ℝ) • (1 : M4) -
        blk (diag2 (0 : ℝ) 2) (!![(0 : ℝ), b; -b, 0]) (!![(0 : ℝ), c; -c, 0])
          (diag2 (1 : ℝ) (1 + dlmin))) =
      b * c * (b * c - dlmin) := by
  have h1 : (1 : ℝ) ≠ 0 := one_ne_zero
  have h2 : (-1 : ℝ) ≠ 0 := by norm_num
  rw [shift_blk_gen, shift_gr_at_one, shift_sm_at_one]
  letI := instDiagInv (1 : ℝ) (-1) h1 h2
  rw [det_blk_schur_left]
  rw [show ⅟(diag2 (1 : ℝ) (-1)) = diag2 ((1 : ℝ)⁻¹) ((-1 : ℝ)⁻¹) from rfl]
  rw [neg_sandwich (!![(0 : ℝ), c; -c, 0]) (diag2 ((1 : ℝ)⁻¹) ((-1 : ℝ)⁻¹))
        (!![(0 : ℝ), b; -b, 0])]
  rw [rot_conj_diag c b ((1 : ℝ)⁻¹) ((-1 : ℝ)⁻¹)]
  rw [diag2_sub_diag2]
  simp only [det_diag2]
  field_simp
  ring_nf

/-- ★ **混型耦合在 `t = 1` 的读数**：`det = (bc)²`——与 `t = 1 + Δλ_min` 处同为 `(bc)²`。 -/
theorem mixed_reading_at_one (b c : ℝ) :
    Matrix.det ((1 : ℝ) • (1 : M4) -
        blk (diag2 (0 : ℝ) 2) (diag2 b b) (!![(0 : ℝ), c; -c, 0])
          (diag2 (1 : ℝ) (1 + dlmin))) =
      (b * c) ^ 2 := by
  have h1 : (1 : ℝ) ≠ 0 := one_ne_zero
  have h2 : (-1 : ℝ) ≠ 0 := by norm_num
  rw [shift_blk_gen, shift_gr_at_one, shift_sm_at_one]
  letI := instDiagInv (1 : ℝ) (-1) h1 h2
  rw [det_blk_schur_left]
  rw [show ⅟(diag2 (1 : ℝ) (-1)) = diag2 ((1 : ℝ)⁻¹) ((-1 : ℝ)⁻¹) from rfl]
  rw [neg_sandwich (!![(0 : ℝ), c; -c, 0]) (diag2 ((1 : ℝ)⁻¹) ((-1 : ℝ)⁻¹))
        (diag2 b b)]
  rw [mul_assoc, diag2_mul_diag2, antidiag_mul_diag2]
  rw [diag2_sub_antidiag, Matrix.det_fin_two_of]
  simp only [det_diag2]
  field_simp
  ring_nf
/-! ## 非零性：`1 + Δλ_min` 不是特征根（单位幅度） -/

/-- `Δλ_min < 1/2`（由显式值 `(√3−1)/6` 与 `√3 < 4`）。 -/
theorem dlmin_lt_half : dlmin < 1 / 2 := by
  have hs : Real.sqrt 3 < 4 := by
    rw [Real.sqrt_lt' (by norm_num : (0 : ℝ) < 4)]
    norm_num
  unfold dlmin
  linarith

/-- 标量型单位幅度读数非零：`1 − h − h² > 0`。 -/
theorem unit_scalar_reading_ne_zero : 1 - dlmin - dlmin ^ 2 ≠ 0 := by
  have hd : dlmin ^ 2 < dlmin / 2 := by nlinarith [dlmin_lt_half, dlmin_pos]
  have : 0 < 1 - dlmin - dlmin ^ 2 := by nlinarith [hd, dlmin_lt_half]
  exact ne_of_gt this

/-- 转动型单位幅度读数非零：`1 − h + h² = (h − 1/2)² + 3/4 > 0`。 -/
theorem unit_rotation_reading_ne_zero : 1 - dlmin + dlmin ^ 2 ≠ 0 := by
  have : 0 < 1 - dlmin + dlmin ^ 2 := by nlinarith [sq_nonneg (dlmin - 1 / 2)]
  exact ne_of_gt this

/-- ★ **判决**：三条读数（单位幅度）全部非零，三条闭式在该退化点连续延拓成立，
    且 `1 + Δλ_min` 在三类量子化耦合下都不是双向载体的特征根。 -/
theorem sm_root_reading_verdict :
    (Matrix.det ((1 + dlmin) • (1 : M4) -
        blk (diag2 (0 : ℝ) 2) (diag2 (1 : ℝ) 1) (diag2 (1 : ℝ) 1)
          (diag2 (1 : ℝ) (1 + dlmin))) = 1 - dlmin - dlmin ^ 2) ∧
    (Matrix.det ((1 + dlmin) • (1 : M4) -
        blk (diag2 (0 : ℝ) 2) (!![(0 : ℝ), 1; -1, 0]) (!![(0 : ℝ), 1; -1, 0])
          (diag2 (1 : ℝ) (1 + dlmin))) = 1 - dlmin + dlmin ^ 2) ∧
    (Matrix.det ((1 + dlmin) • (1 : M4) -
        blk (diag2 (0 : ℝ) 2) (diag2 (1 : ℝ) 1) (!![(0 : ℝ), 1; -1, 0])
          (diag2 (1 : ℝ) (1 + dlmin))) = 1) ∧
    (1 - dlmin - dlmin ^ 2 ≠ 0) ∧ (1 - dlmin + dlmin ^ 2 ≠ 0) := by
  refine ⟨?_, ?_, ?_, unit_scalar_reading_ne_zero, unit_rotation_reading_ne_zero⟩
  · simpa using scalar_reading_at_sm_root 1 1
  · simpa using rotation_reading_at_sm_root 1 1
  · simpa using mixed_reading_at_sm_root 1 1

/-- `t = 1` 处单位幅度读数非零：`1 − Δλ_min ≠ 0`（`Δλ_min < 1`）。 -/
theorem unit_scalar_reading_at_one_ne_zero : 1 - dlmin ≠ 0 := by
  have := dlmin_in_unit_interval.2
  linarith

/-- ★★ **两个退化点都不是谱点**：`t = 1` 与 `t = 1 + Δλ_min` 两处、三条耦合型、
    单位幅度下读数全部非零（`1 − h`、`1 − h ± h²`、`1`）。 -/
theorem both_degenerate_points_not_spectral :
    (Matrix.det ((1 : ℝ) • (1 : M4) -
        blk (diag2 (0 : ℝ) 2) (diag2 (1 : ℝ) 1) (diag2 (1 : ℝ) 1)
          (diag2 (1 : ℝ) (1 + dlmin))) = 1 - dlmin) ∧
    (Matrix.det ((1 : ℝ) • (1 : M4) -
        blk (diag2 (0 : ℝ) 2) (!![(0 : ℝ), 1; -1, 0]) (!![(0 : ℝ), 1; -1, 0])
          (diag2 (1 : ℝ) (1 + dlmin))) = 1 - dlmin) ∧
    (Matrix.det ((1 : ℝ) • (1 : M4) -
        blk (diag2 (0 : ℝ) 2) (diag2 (1 : ℝ) 1) (!![(0 : ℝ), 1; -1, 0])
          (diag2 (1 : ℝ) (1 + dlmin))) = 1) ∧
    (1 - dlmin ≠ 0) ∧
    (1 - dlmin - dlmin ^ 2 ≠ 0) ∧
    (1 - dlmin + dlmin ^ 2 ≠ 0) := by
  refine ⟨?_, ?_, ?_, unit_scalar_reading_at_one_ne_zero,
    unit_scalar_reading_ne_zero, unit_rotation_reading_ne_zero⟩
  · simpa using scalar_reading_at_one 1 1
  · simpa using rotation_reading_at_one 1 1
  · simpa using mixed_reading_at_one 1 1
/-- ★ **型判别只在上面那个根出现**：`t = 1` 处两类纯型读数相同（对型全盲），
    `t = 1 + Δλ_min` 处相差恰为 `2·Δλ_min²`（二阶小量）。 -/
theorem type_discrimination_at_degenerate_points :
    ((1 - dlmin) - (1 - dlmin) = 0) ∧
      ((1 - dlmin + dlmin ^ 2) - (1 - dlmin - dlmin ^ 2) = 2 * dlmin ^ 2) := by
  constructor <;> ring
end MUFPF.SmRootAudit
