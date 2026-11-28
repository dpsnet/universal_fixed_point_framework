/-
  PureTypeSpectrumAudit.lean — R-aa：耦合的「纯粹性」决定谱的可分离性（§47）
  ==================================================================================

## 问题

§46 只做了**标量**耦合 `B = C = s·1` 的谱因子化，并登记 `SPECTRUM_FACTOR_NONSCALAR`：
`B`、`C` 取转动型（§31 的 `±A`）时是否有同类闭式。本批把这个开口做成**三分闭式**。

## 结果（三条闭式，均经 Schur 谱分解机检）

设 `A = rotGen = !![0,1;−1,0]`、`A_GR = diag(0,2)`、`A_SM = diag(1, 1+Δλ_min)`，
`b, c` 为耦合幅度（`bc` 只以乘积出现）：

1. **纯标量**（`B = diag2 b b`、`C = diag2 c c`，§46）：
   `det (t•1₄ − M) = (t² − t − bc)·(t² − (3+Δλ_min)t + 2(1+Δλ_min) − bc)`。
2. **纯转动**（`B = !![0,b;−b,0]`、`C = !![0,c;−c,0]`）：
   `det (t•1₄ − M) = (t² − (1+Δλ_min)t + bc)·(t² − 3t + 2 + bc)`。
   注意 `Δλ_min` **只出现在线性项**，常数项与另一因子完全不含它。
3. **混型**（`B = diag2 b b`、`C = !![0,c;−c,0]`，或反之）：
   `det (t•1₄ − M) = t·(t−1)·(t−2)·(t−(1+Δλ_min)) + (bc)²`。
   `Δλ_min` 的足迹恰是 `−Δλ_min · t(t−1)(t−2)`——它被打散成**四个层地标之积**，没有可分离因子。

## 判决

- **盲对的存在性取决于耦合的纯粹性**：纯型（同型 `1` 或同型 `A`）恒有一个不含 `Δλ_min` 的二次因子；
  混型没有。§46 的「谱里永远有一对不携带框架常数的根」**只在纯型成立**。
- **盲对的形状由类型决定**：标量型是 `t² − t − bc`（`bc = 1` 时即金色因子 `t² − t − 1`）；
  转动型是 `t² − 3t + 2 + bc`（`bc = 1` 时 `t² − 3t + 3`，根为复对 `(3 ± √3 i)/2`）。
- **§41 的五个读数 = 三条闭式的 `t = 0` 切片**：标量 `−bc(2 + 2Δλ_min − bc)`（`±1` 给 `−1.244 / 3.244`）、
  转动 `bc(2 + bc)`（`±1` 给 `3 / −1`，**完全免 `Δλ_min`**）、混型 `(bc)²`（恒 `1`）。五个读数由此得到机制，
  且从四值 `±1, ±A` 推广到连续幅度 `b, c`。
- **单点干净 ≠ 谱可分离**：混型的 `det` 最干净（精确 `(bc)²`、`Δλ_min` 全无），但它的谱最脏
  （`Δλ_min` 散在三处）。§41 的「12/16 读整数」是单点现象，不能读作谱层面的盲性。

## 诚实边界

1. 三条闭式都只在 `t ≠ 1`、`t ≠ 1+Δλ_min`（`D` 侧可逆）上成立；多项式恒等式层面的延拓靠连续性论证，
   本批不引 `Polynomial`。
2. 「混型无二次因子」由 sympy 的因式分解给出（`t=0` 处 `Δλ_min` 不可消），**未**机检不可约性；
   机检的是它的闭式与足迹结构（`mixed_char_closed`）。
3. `b, c` 只作幅度见证，不主张它们有内生来源（耦合幅度仍是 §26–§27 悬案）。
4. 不新增常数、不新增公设；`Δλ_min` 只引 `GNBridgeAudit.dlmin`。
-/

import MUFPFormalization.TwoWaySpectrumAudit
import MUFPFormalization.IntertwinerRepairAudit
import Mathlib.Tactic

set_option warn.classDefReducibility false
set_option linter.unusedSimpArgs false
set_option linter.unusedTactic false
set_option linter.unreachableTactic false
set_option linter.style.haveILetI false

namespace MUFPF.PureTypeSpectrumAudit

open MUFPF.IntertwinerExistenceAudit (diag2)
open MUFPF.LayeredCarrierAudit (blk)
open MUFPF.IntertwinerRepairAudit (rotGen)
open MUFPF.CarrierDetAudit (det_diag2)
open MUFPF.TwoWayCarrierAudit (diag2_mul_diag2 diag2_sub_diag2)
open MUFPF.TwoWaySpectrumAudit (instDiagInv shift_blk_gen det_shift_blk_schur neg_sandwich)
open MUFPF.ScalarReadoutAudit (shift_diag2)
open MUFPF.GNBridgeAudit (dlmin dlmin_pos)
open MUFPF.SchurCarrierAudit (det_blk_schur)

abbrev M2 : Type := Matrix (Fin 2) (Fin 2) ℝ

/-! ## 两个 2×2 条目引理 -/

/-- 转动穿过对角块：`(x·A)·diag(a,b)·(y·A) = diag(−x·y·b, −x·y·a)`（两槽互换并取负）。 -/
theorem rot_conj_diag (x y a b : ℝ) :
    (!![(0 : ℝ), x; -x, 0]) * diag2 a b * (!![(0 : ℝ), y; -y, 0])
      = diag2 (-(x * y * b)) (-(x * y * a)) := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [diag2, Matrix.mul_apply, Fin.sum_univ_two] <;> ring

/-- 对角块乘反对角：`diag(p,q)·!![0,a;−b,0] = !![0, p·a; −(q·b), 0]`。 -/
theorem diag2_mul_antidiag (p q a b : ℝ) :
    diag2 p q * (!![(0 : ℝ), a; -b, 0]) = !![(0 : ℝ), p * a; -(q * b), 0] := by
  rw [diag2, Matrix.mul_fin_two]
  ext i j
  fin_cases i <;> fin_cases j <;> simp <;> ring

/-- 对角块减反对角：`diag(p,q) − !![0,a;−b,0] = !![p, −a; b, q]`。 -/
theorem diag2_sub_antidiag (p q a b : ℝ) :
    diag2 p q - (!![(0 : ℝ), a; -b, 0]) = !![p, -a; b, q] := by
  rw [diag2]
  ext i j
  fin_cases i <;> fin_cases j <;> simp

/-! ## 纯转动耦合的谱因子化 -/

/-- ★★ **纯转动耦合的谱因子化**（`B = !![0,b;−b,0]`、`C = !![0,c;−c,0]`，`t ≠ 1`、`t ≠ 1+Δλ_min`）：
    `det (t•1₄ − M) = (t² − (1+Δλ_min)·t + b·c) · (t² − 3·t + 2 + b·c)`。
    `Δλ_min` 只出现在前一因子的线性项——后一因子（含 `bc = 1` 时 `t²−3t+3`）完全不含它。 -/
theorem rotation_pure_factorization (t b c : ℝ) (h1 : t ≠ 1) (h2 : t ≠ 1 + dlmin) :
    Matrix.det (t • (1 : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ) -
        blk (diag2 (0 : ℝ) 2) (!![(0 : ℝ), b; -b, 0]) (!![(0 : ℝ), c; -c, 0])
          (diag2 (1 : ℝ) (1 + dlmin))) =
      (t ^ 2 - (1 + dlmin) * t + b * c) * (t ^ 2 - 3 * t + 2 + b * c) := by
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
  rw [neg_sandwich (!![(0 : ℝ), b; -b, 0]) (diag2 ((t - 1)⁻¹) ((t - (1 + dlmin))⁻¹))
        (!![(0 : ℝ), c; -c, 0])]
  rw [rot_conj_diag b c ((t - 1)⁻¹) ((t - (1 + dlmin))⁻¹)]
  rw [diag2_sub_diag2]
  simp only [det_diag2]
  field_simp
  ring

/-- **纯转动耦合的 `det` 完全免 `Δλ_min`**：`det M = b·c·(2 + b·c)`。 -/
theorem rotation_det_h_free (b c : ℝ) :
    Matrix.det (blk (diag2 (0 : ℝ) 2) (!![(0 : ℝ), b; -b, 0]) (!![(0 : ℝ), c; -c, 0])
        (diag2 (1 : ℝ) (1 + dlmin))) = b * c * (2 + b * c) := by
  have hne : (1 + dlmin) ≠ 0 := by linarith [dlmin_pos]
  letI := instDiagInv (1 : ℝ) (1 + dlmin) (by norm_num) hne
  rw [det_blk_schur]
  rw [show ⅟(diag2 (1 : ℝ) (1 + dlmin)) =
      diag2 ((1 : ℝ)⁻¹) ((1 + dlmin)⁻¹) from rfl]
  rw [inv_one]
  rw [rot_conj_diag b c 1 ((1 + dlmin)⁻¹)]
  rw [diag2_sub_diag2]
  simp only [det_diag2]
  field_simp
  ring

/-! ## 混型耦合的谱闭式 -/

/-- ★★ **混型耦合的谱闭式**（`B = diag2 b b`、`C = !![0,c;−c,0]`，`t ≠ 1`、`t ≠ 1+Δλ_min`）：
    `det (t•1₄ − M) = t·(t−1)·(t−2)·(t−(1+Δλ_min)) + (b·c)²`。
    `Δλ_min` 的足迹恰为 `−Δλ_min·t(t−1)(t−2)`——没有可分离的二次因子。 -/
theorem mixed_char_closed (t b c : ℝ) (h1 : t ≠ 1) (h2 : t ≠ 1 + dlmin) :
    Matrix.det (t • (1 : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ) -
        blk (diag2 (0 : ℝ) 2) (diag2 b b) (!![(0 : ℝ), c; -c, 0])
          (diag2 (1 : ℝ) (1 + dlmin))) =
      t * (t - 1) * (t - 2) * (t - (1 + dlmin)) + (b * c) ^ 2 := by
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
  rw [neg_sandwich (diag2 b b) (diag2 ((t - 1)⁻¹) ((t - (1 + dlmin))⁻¹))
        (!![(0 : ℝ), c; -c, 0])]
  rw [diag2_mul_diag2, diag2_mul_antidiag]
  rw [diag2_sub_antidiag]
  rw [det_diag2, Matrix.det_fin_two_of]
  field_simp
  ring

/-- **混型的 `det` 同样免 `Δλ_min`**：`det M = (b·c)²`（单点最干净）。 -/
theorem mixed_det_h_free (b c : ℝ) :
    Matrix.det (blk (diag2 (0 : ℝ) 2) (diag2 b b) (!![(0 : ℝ), c; -c, 0])
        (diag2 (1 : ℝ) (1 + dlmin))) = (b * c) ^ 2 := by
  have hne : (1 + dlmin) ≠ 0 := by linarith [dlmin_pos]
  letI := instDiagInv (1 : ℝ) (1 + dlmin) (by norm_num) hne
  rw [det_blk_schur]
  rw [show ⅟(diag2 (1 : ℝ) (1 + dlmin)) =
      diag2 ((1 : ℝ)⁻¹) ((1 + dlmin)⁻¹) from rfl]
  rw [diag2_mul_diag2, diag2_mul_antidiag]
  rw [diag2_sub_antidiag]
  rw [det_diag2, Matrix.det_fin_two_of]
  field_simp
  ring

/-! ## 汇总判决 -/

/-- **R-aa 判决汇总**（三分闭式 + 两条 `det` 免常性）：
    ① 纯转动：`(t²−(1+Δλ_min)t+bc)(t²−3t+2+bc)`；
    ② 混型：`t(t−1)(t−2)(t−(1+Δλ_min)) + (bc)²`；
    ③ 转动 `det = bc(2+bc)`、混型 `det = (bc)²`——两者都在单点上免 `Δλ_min`；
    ④ 故「盲对」只存在于纯型：混型在最干净的单点上也没有可分离因子。 -/
theorem pure_type_trichotomy (t b c : ℝ) (h1 : t ≠ 1) (h2 : t ≠ 1 + dlmin) :
    (Matrix.det (t • (1 : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ) -
        blk (diag2 (0 : ℝ) 2) (!![(0 : ℝ), b; -b, 0]) (!![(0 : ℝ), c; -c, 0])
          (diag2 (1 : ℝ) (1 + dlmin))) =
      (t ^ 2 - (1 + dlmin) * t + b * c) * (t ^ 2 - 3 * t + 2 + b * c)) ∧
    (Matrix.det (t • (1 : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ) -
        blk (diag2 (0 : ℝ) 2) (diag2 b b) (!![(0 : ℝ), c; -c, 0])
          (diag2 (1 : ℝ) (1 + dlmin))) =
      t * (t - 1) * (t - 2) * (t - (1 + dlmin)) + (b * c) ^ 2) ∧
    (Matrix.det (blk (diag2 (0 : ℝ) 2) (!![(0 : ℝ), b; -b, 0]) (!![(0 : ℝ), c; -c, 0])
        (diag2 (1 : ℝ) (1 + dlmin))) = b * c * (2 + b * c)) :=
  ⟨rotation_pure_factorization t b c h1 h2, mixed_char_closed t b c h1 h2,
    rotation_det_h_free b c⟩

end MUFPF.PureTypeSpectrumAudit
