/-
  TwoWayCarrierAudit.lean — R-x：双向载体上的框架 `det` 实值（§39 开口 `TWO_WAY_FRAMEWORK_DET` 收口）
  ==========================================================================================

## 问题

§39 把 `det` 的一般律写成 `det D · det (A − B·⅟D·C)`，但框架实例的双向版**只停在符号层**，
数值未出：开口 `TWO_WAY_FRAMEWORK_DET`。本批把 `⅟A_SM` 显式算出，再取两组耦合见证，
把框架双向载体的 `det` 真实值钉死。

## 结果（全部机检）

1. `⅟(diag(1, 1+Δλ_min)) = diag(1, (1+Δλ_min)⁻¹)`——由 `invOf_eq_right_inv` + 逐条目乘法给出，
   乘法律是自建的 `diag2_mul_diag2`；不依赖 Mathlib 的对角逆引理。
2. **耦合取恒等（`B = C = 1`）**：`det (blk A_GR 1 1 A_SM) = 1 − 2·(1+Δλ_min) = −1 − 2Δλ_min`。
3. **耦合取第一个槽的投影（`B = C = diag(1,0)`）**：`det (blk A_GR P P A_SM) = −2·(1+Δλ_min)`。
4. 两值**不等**（差 1），且**都非零** ⟹ 双向载体上 `det` 既不为恒零（推翻 §38 在框架实例上的恒零判读），
   也随耦合选择变（§39 的「`C ≠ 0` ⟹ 看到 `B`」在框架实例上落实为具体数字）。

## 读数结构（判决）

- 恒等耦合值 `1 − 2·(1+Δλ_min)` 与投影耦合值 `−2·(1+Δλ_min)` 都是
  「`A_GR = diag(0,2)` 的非零对角元 `2` 与 `det A_SM = 1+Δλ_min`」的**乘积/线性组合**。
- 即 `det` 把层数据压成一个标量：`2` 与 `1+Δλ_min` 只能以 `2·det A_SM` 这类乘积出现，
  **不能**分开读成 `2` 与 `2+Δλ_min`（那是 `trace` 才有的加法可分性，见 §38 `trace = 4 + Δλ_min`）。
- 结论：`det` 这条路在双向载体上并没有变「免疫」，而是变「可读但混叠」——读到一个乘积，
  而桥需要的正是可分性。载体桥仍不成立，但阻塞理由已从「`det` 恒零」精确到「`det` 只给乘积」。

## 诚实边界

1. 只测两组耦合见证（恒等、第一槽投影）；一般 `B, C` 的闭式由 §39 的 `det_blk_schur` 覆盖（含 `⅟D` 符号），
   本批不给一般 `B, C` 的数值表。
2. 这两组耦合是**见证**而非框架内生耦合；`B, C` 的内生判据仍属 §26–§27 的未决悬案，
   故这两个数值不可被读作「框架预言」。
3. `⅟A_SM` 的显式值只对 `diag(1, 1+Δλ_min)` 这一实例成立（不推广到一般 `A_SM`）。
-/

import MUFPFormalization.SchurCarrierAudit
import Mathlib.Tactic

namespace MUFPF.TwoWayCarrierAudit

open MUFPF.IntertwinerExistenceAudit (diag2)
open MUFPF.LayeredCarrierAudit (blk)
open MUFPF.CarrierDetAudit (framework_sm_det)
open MUFPF.GNBridgeAudit (dlmin dlmin_pos)
open MUFPF.SchurCarrierAudit (det_blk_schur instFrameworkSmInvertible)

/-- 对角块的乘法：`diag(a,b) · diag(c,d) = diag(a·c, b·d)`。 -/
theorem diag2_mul_diag2 (a b c d : ℝ) :
    diag2 a b * diag2 c d = diag2 (a * c) (b * d) := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [diag2, Matrix.mul_apply, Fin.sum_univ_two]

/-- 对角块的减法：`diag(a,b) − diag(c,d) = diag(a−c, b−d)`。 -/
theorem diag2_sub_diag2 (a b c d : ℝ) :
    diag2 a b - diag2 c d = diag2 (a - c) (b - d) := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [diag2, Matrix.sub_apply]

/-- `diag(1,1) = 1`。 -/
theorem diag2_one_one : diag2 (1 : ℝ) 1 = (1 : Matrix (Fin 2) (Fin 2) ℝ) := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [diag2]

/-- 恒等耦合的读数化简：`h · (⅟h − 2) = 1 − 2h`。 -/
theorem identity_reading (h : ℝ) (hh : h ≠ 0) :
    h * (h⁻¹ - 2) = 1 - 2 * h := by
  rw [mul_sub, mul_inv_cancel₀ hh]
  ring

/-- 投影耦合的读数化简：`h · 2 = 2h`（符号已由 `simp`/`norm_num` 吸收）。 -/
theorem projection_reading (h : ℝ) : h * 2 = 2 * h := by
  ring

/-- ★★ **框架范畴层的显式逆**：`⅟(diag(1, 1+Δλ_min)) = diag(1, (1+Δλ_min)⁻¹)`。 -/
theorem invOf_diag2_sm :
    ⅟(diag2 (1 : ℝ) (1 + dlmin)) = diag2 (1 : ℝ) ((1 + dlmin)⁻¹) := by
  have hne : (1 : ℝ) + dlmin ≠ 0 := by
    have hpos : (0 : ℝ) < 1 + dlmin := by linarith [dlmin_pos]
    linarith
  refine invOf_eq_right_inv ?_
  rw [diag2_mul_diag2, mul_inv_cancel₀ hne, one_mul, diag2_one_one]

/-- ★★ **框架双向载体，恒等耦合的 `det`**：`B = C = 1` ⟹ `det = 1 − 2·(1+Δλ_min)`。 -/
theorem framework_two_way_identity :
    Matrix.det (blk (diag2 (0 : ℝ) 2) (1 : Matrix (Fin 2) (Fin 2) ℝ)
        (1 : Matrix (Fin 2) (Fin 2) ℝ) (diag2 (1 : ℝ) (1 + dlmin))) =
      1 - 2 * (1 + dlmin) := by
  have hne : (1 : ℝ) + dlmin ≠ 0 := by
    have hpos : (0 : ℝ) < 1 + dlmin := by linarith [dlmin_pos]
    linarith
  rw [det_blk_schur, invOf_diag2_sm, Matrix.one_mul, Matrix.mul_one,
    diag2_sub_diag2, framework_sm_det, Matrix.det_fin_two]
  simp only [diag2, Matrix.of_apply]
  norm_num
  rw [identity_reading (1 + dlmin) hne]

/-- ★★ **框架双向载体，第一槽投影耦合的 `det`**：
    `B = C = diag(1,0)` ⟹ `det = −2·(1+Δλ_min)`。 -/
theorem framework_two_way_projection :
    Matrix.det (blk (diag2 (0 : ℝ) 2) (diag2 (1 : ℝ) 0) (diag2 (1 : ℝ) 0)
        (diag2 (1 : ℝ) (1 + dlmin))) = -(2 * (1 + dlmin)) := by
  rw [det_blk_schur, invOf_diag2_sm, diag2_mul_diag2, diag2_mul_diag2,
    diag2_sub_diag2, framework_sm_det, Matrix.det_fin_two]
  simp only [diag2, Matrix.of_apply]
  norm_num
  rw [projection_reading (1 + dlmin)]

/-- ★★ **双向载体上 `det` 非零**（推翻「框架实例载体 `det` 恒零」的普遍读法）。 -/
theorem framework_two_way_det_ne_zero :
    Matrix.det (blk (diag2 (0 : ℝ) 2) (1 : Matrix (Fin 2) (Fin 2) ℝ)
        (1 : Matrix (Fin 2) (Fin 2) ℝ) (diag2 (1 : ℝ) (1 + dlmin))) ≠ 0 := by
  rw [framework_two_way_identity]
  intro h
  have hneg : (1 : ℝ) - 2 * (1 + dlmin) = -(1 + 2 * dlmin) := by ring
  rw [hneg] at h
  linarith [dlmin_pos]

/-- ★★ **双向载体上 `det` 随耦合选择变**（两值相差 1）。 -/
theorem framework_two_way_det_depends_on_coupling :
    Matrix.det (blk (diag2 (0 : ℝ) 2)
        (1 : Matrix (Fin 2) (Fin 2) ℝ) (1 : Matrix (Fin 2) (Fin 2) ℝ)
        (diag2 (1 : ℝ) (1 + dlmin))) ≠
      Matrix.det (blk (diag2 (0 : ℝ) 2) (diag2 (1 : ℝ) 0) (diag2 (1 : ℝ) 0)
        (diag2 (1 : ℝ) (1 + dlmin))) := by
  rw [framework_two_way_identity, framework_two_way_projection]
  intro h
  nlinarith

/-- **R-x 判决汇总**（`det` 两值；`⅟A_SM` 显式见 `invOf_diag2_sm`）：
    ① 恒等耦合 `det = 1 − 2·(1+Δλ_min)`；
    ② 投影耦合 `det = −2·(1+Δλ_min)`。 -/
theorem two_way_carrier_verdict :
    (Matrix.det (blk (diag2 (0 : ℝ) 2) (1 : Matrix (Fin 2) (Fin 2) ℝ)
        (1 : Matrix (Fin 2) (Fin 2) ℝ) (diag2 (1 : ℝ) (1 + dlmin))) =
      1 - 2 * (1 + dlmin)) ∧
    (Matrix.det (blk (diag2 (0 : ℝ) 2) (diag2 (1 : ℝ) 0) (diag2 (1 : ℝ) 0)
        (diag2 (1 : ℝ) (1 + dlmin))) = -(2 * (1 + dlmin))) :=
  ⟨framework_two_way_identity, framework_two_way_projection⟩

end MUFPF.TwoWayCarrierAudit
