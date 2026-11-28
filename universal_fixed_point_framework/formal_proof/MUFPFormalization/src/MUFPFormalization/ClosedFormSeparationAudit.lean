/-
  ClosedFormSeparationAudit.lean — R-ab：三条闭式的差恒等式与纯型可分解性判决（§49）
  ==============================================================================

## 问题

§47 给出三条谱闭式（纯标量 / 纯转动 / 混型），并在「诚实边界 2」里承认：

> 「混型无二次因子」由 sympy 的因式分解给出，**未**机检不可约性。

本批把这条从「外部观察」推进到「机检」：不做一般不可约性，而做**可判定的分离命题**——

> 混型的闭式能否等于任一**纯型闭式**（作为 `t` 的函数）？

不是「混型多项式有没有任何二次因子」，而是「混型是不是一条纯型闭式」。后者可判定、可机检，
且正是 §47 判决 `SPECTRUM_MIXED_NO_FACTOR` 的直接内容。

## 做法

三条闭式的公共骨架是同一个四次式

`q(t) = t·(t−1)·(t−2)·(t−(1+Δλ_min))`，

差别只在 `bc` 项：

- 纯转动：`q + bc·(A+B) + (bc)²`，其中 `A = t²−(1+Δλ_min)t`、`B = t²−3t+2`；
- 纯标量：`q − bc·(A'+B') + (bc)²`，其中 `A' = t²−t`、`B' = t²−(3+Δλ_min)t+2(1+Δλ_min)`；
- 混型：`q + (bc)²`（`bc` 项**完全不出现**）。

于是两条**差恒等式**（在 `t ≠ 1`、`t ≠ 1+Δλ_min` 上）：

```
mixed − rotation = −bc·(2t² − (4+Δλ_min)t + 2)
mixed − scalar   = +bc·(2t² − (4+Δλ_min)t + 2(1+Δλ_min))
```

## 判决

1. **混型与两条纯型闭式之差恒为 `bc` 的一次项**，且该一次项的二次括号在 `t = 0` 处取 `2` / `2(1+Δλ_min)`，
   非零 ⟹ `bc ≠ 0` 时混型**不可能**写成任一纯型闭式。§47 的 `SPECTRUM_MIXED_NO_FACTOR` 由此获得机检支撑。
2. **两个括号都实根二分**：判别式分别为 `Δλ_min(Δλ_min+8) ≈ 0.99095` 与 `8+Δλ_min² ≈ 8.01489`，均严格正
   ⟹ 混型与纯型闭式的差在 `t` 轴上变号两次（两者在两点上**取值相同但函数不同**）。
3. **纯标量闭式的一般幅度版**（`B = diag2 p p`、`C = diag2 q q`，不等幅度）本批一并机检：
   闭式只依赖乘积 `pq`。§46 只做过等幅 `s·1` 版，这是它的补足。

## 诚实边界

1. 两条差恒等式只在 `D` 侧可逆（`t ≠ 1`、`t ≠ 1+Δλ_min`）上成立；跨过这两点的延拓靠连续性论证，本批不引
   `Polynomial`，故**不主张**多项式恒等式层面的版本。
2. 机检的是「混型 ≠ 纯型闭式」这一**分离命题**；「混型四次式在 `ℝ[t]` 上不可约」是更强的命题，
   **本批未做、也未主张**（`SPECTRUM_MIXED_NO_FACTOR` 的措辞应按第 2 条收窄）。
3. `b, c` 仍是幅度见证，不主张内生来源（耦合幅度是 §26–§27 悬案）。
4. 不新增常数、不新增公设；`Δλ_min` 只引 `GNBridgeAudit.dlmin`。
-/

import MUFPFormalization.PureTypeSpectrumAudit
import Mathlib.Tactic

set_option warn.classDefReducibility false
set_option linter.unusedSimpArgs false
set_option linter.unusedTactic false
set_option linter.unreachableTactic false
set_option linter.style.haveILetI false

namespace MUFPF.ClosedFormSeparationAudit

open MUFPF.IntertwinerExistenceAudit (diag2)
open MUFPF.LayeredCarrierAudit (blk)
open MUFPF.CarrierDetAudit (det_diag2)
open MUFPF.TwoWayCarrierAudit (diag2_mul_diag2 diag2_sub_diag2)
open MUFPF.TwoWaySpectrumAudit (instDiagInv shift_blk_gen neg_sandwich)
open MUFPF.ScalarReadoutAudit (shift_diag2)
open MUFPF.GNBridgeAudit (dlmin dlmin_pos)
open MUFPF.SchurCarrierAudit (det_blk_schur)
open MUFPF.PureTypeSpectrumAudit (rotation_pure_factorization mixed_char_closed
  rotation_det_h_free mixed_det_h_free)

abbrev M2 : Type := Matrix (Fin 2) (Fin 2) ℝ

/-- 混型载体：`B = diag2 b b`、`C = !![0,c;−c,0]`。 -/
noncomputable abbrev mixMat (b c : ℝ) : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ :=
  blk (diag2 (0 : ℝ) 2) (diag2 b b) (!![(0 : ℝ), c; -c, 0]) (diag2 (1 : ℝ) (1 + dlmin))

/-- 纯转动载体：`B = !![0,b;−b,0]`、`C = !![0,c;−c,0]`。 -/
noncomputable abbrev rotMat (b c : ℝ) : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ :=
  blk (diag2 (0 : ℝ) 2) (!![(0 : ℝ), b; -b, 0]) (!![(0 : ℝ), c; -c, 0])
    (diag2 (1 : ℝ) (1 + dlmin))

/-- 纯标量载体：`B = diag2 b b`、`C = diag2 c c`。 -/
noncomputable abbrev sclMat (b c : ℝ) : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ :=
  blk (diag2 (0 : ℝ) 2) (diag2 b b) (diag2 c c) (diag2 (1 : ℝ) (1 + dlmin))

/-! ## 纯标量闭式的一般幅度版（§46 等幅版的补足） -/

/-- ★ **纯标量耦合闭式（不等幅度）**（`B = diag2 p p`、`C = diag2 q q`，`t ≠ 1`、`t ≠ 1+Δλ_min`）：
    `det (t•1₄ − M) = (t² − t − pq) · (t² − (3+Δλ_min)t + 2(1+Δλ_min) − pq)`。
    只依赖乘积 `p·q`；§46 的等幅 `s·1` 版是 `p = q = s` 的特例。 -/
theorem scalar_diag_factorization (t p q : ℝ) (h1 : t ≠ 1) (h2 : t ≠ 1 + dlmin) :
    Matrix.det (t • (1 : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ) -
        blk (diag2 (0 : ℝ) 2) (diag2 p p) (diag2 q q)
          (diag2 (1 : ℝ) (1 + dlmin))) =
      (t ^ 2 - t - p * q) * (t ^ 2 - (3 + dlmin) * t + 2 * (1 + dlmin) - p * q) := by
  have hd1 : t - 1 ≠ 0 := sub_ne_zero.mpr h1
  have hd2 : t - (1 + dlmin) ≠ 0 := sub_ne_zero.mpr h2
  rw [shift_blk_gen]
  rw [show t • (1 : M2) - diag2 (0 : ℝ) 2 = diag2 t (t - 2) from by
        rw [shift_diag2 t 0 2, sub_zero]
      , show t • (1 : M2) - diag2 (1 : ℝ) (1 + dlmin) =
          diag2 (t - 1) (t - (1 + dlmin)) from by
        rw [shift_diag2 t 1 (1 + dlmin)]]
  letI := instDiagInv (t - 1) (t - (1 + dlmin)) hd1 hd2
  rw [det_blk_schur]
  rw [show ⅟(diag2 (t - 1) (t - (1 + dlmin))) =
      diag2 ((t - 1)⁻¹) ((t - (1 + dlmin))⁻¹) from rfl]
  rw [neg_sandwich (diag2 p p) (diag2 ((t - 1)⁻¹) ((t - (1 + dlmin))⁻¹))
        (diag2 q q)]
  rw [diag2_mul_diag2, diag2_mul_diag2]
  rw [diag2_sub_diag2]
  simp only [det_diag2]
  field_simp
  ring

/-! ## 两条差恒等式 -/

/-- ★★ **混型 − 纯转动**（`t ≠ 1`、`t ≠ 1+Δλ_min`）：
    `det_mixed − det_rot = −bc · (2t² − (4+Δλ_min)t + 2)`。
    注意括号的常数项是 `2`（不是 `2(1+Δλ_min)`）——`Δλ_min` 只在一次项。 -/
theorem mixed_minus_rotation (t b c : ℝ) (h1 : t ≠ 1) (h2 : t ≠ 1 + dlmin) :
    Matrix.det (t • (1 : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ) -
        blk (diag2 (0 : ℝ) 2) (diag2 b b) (!![(0 : ℝ), c; -c, 0])
          (diag2 (1 : ℝ) (1 + dlmin))) -
      Matrix.det (t • (1 : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ) -
        blk (diag2 (0 : ℝ) 2) (!![(0 : ℝ), b; -b, 0]) (!![(0 : ℝ), c; -c, 0])
          (diag2 (1 : ℝ) (1 + dlmin))) =
      -(b * c) * (2 * t ^ 2 - (4 + dlmin) * t + 2) := by
  rw [mixed_char_closed t b c h1 h2, rotation_pure_factorization t b c h1 h2]
  ring

/-- ★★ **混型 − 纯标量**（同一组幅度 `b, c`，标量侧取 `B = diag2 b b`、`C = diag2 c c`）：
    `det_mixed − det_scalar = +bc · (2t² − (4+Δλ_min)t + 2(1+Δλ_min))`。
    与上一条只差括号的常数项——两条差恒等式的括号是同一个二次式的两种常数平移。 -/
theorem mixed_minus_scalar (t b c : ℝ) (h1 : t ≠ 1) (h2 : t ≠ 1 + dlmin) :
    Matrix.det (t • (1 : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ) -
        blk (diag2 (0 : ℝ) 2) (diag2 b b) (!![(0 : ℝ), c; -c, 0])
          (diag2 (1 : ℝ) (1 + dlmin))) -
      Matrix.det (t • (1 : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ) -
        blk (diag2 (0 : ℝ) 2) (diag2 b b) (diag2 c c)
          (diag2 (1 : ℝ) (1 + dlmin))) =
      b * c * (2 * t ^ 2 - (4 + dlmin) * t + 2 * (1 + dlmin)) := by
  rw [mixed_char_closed t b c h1 h2, scalar_diag_factorization t b c h1 h2]
  ring

/-! ## 两个括号的判别式 -/

/-- 转动侧括号的判别式：`(4+Δλ_min)² − 16 = Δλ_min·(Δλ_min+8)`。 -/
theorem rotation_bracket_discriminant :
    (4 + dlmin) ^ 2 - 16 = dlmin * (dlmin + 8) := by ring

/-- 标量侧括号的判别式：`(4+Δλ_min)² − 8(1+Δλ_min) = 8 + Δλ_min²`。 -/
theorem scalar_bracket_discriminant :
    (4 + dlmin) ^ 2 - 8 * (1 + dlmin) = 8 + dlmin ^ 2 := by ring

/-- 转动侧括号有两个不同实根（判别式严格正）。 -/
theorem rotation_bracket_disc_pos : 0 < (4 + dlmin) ^ 2 - 16 := by
  rw [rotation_bracket_discriminant]
  nlinarith [dlmin_pos]

/-- 标量侧括号有两个不同实根（判别式严格正）。 -/
theorem scalar_bracket_disc_pos : 0 < (4 + dlmin) ^ 2 - 8 * (1 + dlmin) := by
  rw [scalar_bracket_discriminant]
  nlinarith [sq_nonneg dlmin]

/-! ## `t = 0` 切片：混型与两条纯型闭式取值分离 -/

/-- 位移零点的退化：`det (0•1₄ − M) = det M`（`0•1 = 0`、`det (−M) = (−1)⁴·det M`）。 -/
theorem det_zero_shift (M : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ) :
    Matrix.det ((0 : ℝ) • (1 : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ) - M) =
      Matrix.det M := by
  rw [zero_smul, zero_sub, Matrix.det_neg, show Fintype.card (Fin 2 ⊕ Fin 2) = 4 from by
        simp [Fintype.card_sum]]
  norm_num

/-- `t = 0` 处混型与纯转动之差是 `−2·bc`（§47 的 `(bc)²` 与 `bc(2+bc)` 之差）。 -/
theorem mixed_minus_rotation_at_zero (b c : ℝ) :
    Matrix.det (blk (diag2 (0 : ℝ) 2) (diag2 b b) (!![(0 : ℝ), c; -c, 0])
        (diag2 (1 : ℝ) (1 + dlmin))) -
      Matrix.det (blk (diag2 (0 : ℝ) 2) (!![(0 : ℝ), b; -b, 0]) (!![(0 : ℝ), c; -c, 0])
        (diag2 (1 : ℝ) (1 + dlmin))) =
      -2 * (b * c) := by
  rw [mixed_det_h_free b c, rotation_det_h_free b c]
  ring

/-- `t = 0` 处混型与纯标量之差是 `2(1+Δλ_min)·bc`。 -/
theorem mixed_minus_scalar_at_zero (b c : ℝ) :
    Matrix.det (blk (diag2 (0 : ℝ) 2) (diag2 b b) (!![(0 : ℝ), c; -c, 0])
        (diag2 (1 : ℝ) (1 + dlmin))) -
      Matrix.det (blk (diag2 (0 : ℝ) 2) (diag2 b b) (diag2 c c)
        (diag2 (1 : ℝ) (1 + dlmin))) =
      b * c * (2 * (1 + dlmin)) := by
  have h := mixed_minus_scalar 0 b c (by norm_num) (by linarith [dlmin_pos])
  rw [det_zero_shift, det_zero_shift] at h
  simpa using h

/-- ★ 非零耦合下，混型 `det` 与纯转动 `det` **不相等**（在 `t = 0`）。 -/
theorem mixed_det_ne_rotation_det (b c : ℝ) (hbc : b * c ≠ 0) :
    Matrix.det (blk (diag2 (0 : ℝ) 2) (diag2 b b) (!![(0 : ℝ), c; -c, 0])
        (diag2 (1 : ℝ) (1 + dlmin))) ≠
      Matrix.det (blk (diag2 (0 : ℝ) 2) (!![(0 : ℝ), b; -b, 0]) (!![(0 : ℝ), c; -c, 0])
        (diag2 (1 : ℝ) (1 + dlmin))) := by
  have hne : -2 * (b * c) ≠ 0 := mul_ne_zero (by norm_num) hbc
  intro heq
  have h := mixed_minus_rotation_at_zero b c
  rw [heq, sub_self] at h
  exact hne h.symm

/-- ★ 非零耦合下，混型 `det` 与纯标量 `det` **不相等**（在 `t = 0`）。 -/
theorem mixed_det_ne_scalar_det (b c : ℝ) (hbc : b * c ≠ 0) :
    Matrix.det (blk (diag2 (0 : ℝ) 2) (diag2 b b) (!![(0 : ℝ), c; -c, 0])
        (diag2 (1 : ℝ) (1 + dlmin))) ≠
      Matrix.det (blk (diag2 (0 : ℝ) 2) (diag2 b b) (diag2 c c)
        (diag2 (1 : ℝ) (1 + dlmin))) := by
  have hpos : 0 < 1 + dlmin := by linarith [dlmin_pos]
  have hne : b * c * (2 * (1 + dlmin)) ≠ 0 :=
    mul_ne_zero hbc (mul_ne_zero (by norm_num) (ne_of_gt hpos))
  intro heq
  have h := mixed_minus_scalar_at_zero b c
  rw [heq, sub_self] at h
  exact hne h.symm

/-! ## 判决 -/

/-- 两条差恒等式的括号在 `t = 0` 处取 `2(1+Δλ_min)` 与 `2`，故 `bc ≠ 0` 时两式不可能恒等。 -/
theorem bc_linear_separation (b c : ℝ) (hbc : b * c ≠ 0) :
    b * c * (2 * (1 + dlmin)) ≠ -(b * c) * 2 := by
  intro h
  have hzero : b * c * (4 + 2 * dlmin) = 0 := by nlinarith [h]
  rcases mul_eq_zero.mp hzero with hz | hz
  · exact hbc hz
  · nlinarith [hz, dlmin_pos]

/-- ★★ **分离判决**：`bc ≠ 0` 时，混型的谱读数既不是纯转动型、也不是纯标量型；
    两条差恒等式说明差恒为 `bc` 一次项，两个括号的判别式均严格正。 -/
theorem separation_verdict (b c : ℝ) (hbc : b * c ≠ 0) :
    (Matrix.det (mixMat b c) ≠ Matrix.det (rotMat b c)) ∧
    (Matrix.det (mixMat b c) ≠ Matrix.det (sclMat b c)) ∧
    (0 < (4 + dlmin) ^ 2 - 16) ∧
    (0 < (4 + dlmin) ^ 2 - 8 * (1 + dlmin)) ∧
    (b * c * (2 * (1 + dlmin)) ≠ -(b * c) * 2) :=
  ⟨mixed_det_ne_rotation_det b c hbc, mixed_det_ne_scalar_det b c hbc,
    rotation_bracket_disc_pos, scalar_bracket_disc_pos,
    bc_linear_separation b c hbc⟩

end MUFPF.ClosedFormSeparationAudit
