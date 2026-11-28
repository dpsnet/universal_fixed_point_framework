/-
  QuantizedDetAudit.lean — R-y：量化耦合下的双向载体 `det` 读数（§40 开口 `TWO_WAY_QUANTIZED_DET` 收口）
  ==========================================================================================

## 问题

§40 把双向载体（`B`、`C` 同时非零）上的框架 `det` 算出两个实值，但耦合只取了恒等与第一槽投影。
§31 已把耦合量化成四个值 `1, −1, A, −A`（`A = rotGen`，四阶转动），§37 又证量化与保长度互不推出。
本批把 `B`、`C` **各自独立**取这四个值，跑完 16 个组合，问：`det` 在这些组合上究竟读到什么，
`Δλ_min` 还在不在读数里。

## 结果（全部机检；`h` = 范畴层第二对角元，框架实例取 `h = 1 + Δλ_min`）

读数只有**五个**，按耦合类型分三类：

| 耦合类（`B`, `C`） | 组合数 | `det` 读数 | 含 `Δλ_min`？ |
| --- | --- | --- | --- |
| 纯标量 `±1 / ±1`，同号 | 2 | `1 − 2h` | 含（只以 `2h` 出现） |
| 纯标量 `±1 / ±1`，异号 | 2 | `1 + 2h` | 含（同上，符号反） |
| 标量与转动混搭 | 8 | `1` | **不含**（精确常数） |
| 转动 `±A / ±A`，同号 | 2 | `3` | **不含**（精确常数） |
| 转动 `±A / ±A`，异号 | 2 | `−1` | **不含**（精确常数） |

机制：转动的夹心 `A·⅟A_SM·A = diag(−h⁻¹, −1)` 把 `h⁻¹` 打到**第一槽**，而 `A_GR = diag(0,2)` 的
第一对角元是 `0`，于是 `h⁻¹` 只出现一次、恰好与 `det A_SM = h` 相乘抵消——`Δλ_min` 连根消失。
纯标量夹心不换槽，`h⁻¹` 落到第二槽与 `2` 相加，`h` 退不掉，只能以 `1 ∓ 2h` 的形式出现。

## 判决

1. **`det` 的 `Δλ_min` 盲性不是普遍的，是分类型的**：12 / 16 个量化组合上 `det` 给出精确整数
   （`1`、`3`、`−1`），对 `Δλ_min` 完全不敏感；只有纯标量组合（4 / 16）把 `2h` 带进读数。
   §40 的「可读但混叠」因此再精确一层：不是「总是乘积」，而是「`h` 只在纯标量子空间有支撑」。
2. **加法可分性在任何分支上都不出现**：纯标量分支读 `1 ∓ 2h`（`h` 与 `1` 相加、且被加倍），
   转动/混搭分支读整数（连 `h` 都没有）。桥要的 `2` 与 `2 + h` 的相加可分，无一条分支给出。
3. **`det` 能读相对符号**：纯标量类 `1 − 2h ≠ 1 + 2h`，转动类 `3 ≠ −1`。这是对**给定**耦合的读数，
   不构成对耦合选择的约束——比特数仍为 0；但「`det` 完全无信息」要改述为「读得出相对符号、读不出量」。

## 诚实边界

1. `B`、`C` 独立量化取自 §31 的四个值，**不是**框架内生的双向耦合判据（§26–§27 悬案未决）；
   故这些读数不可被读作「框架预言」。
2. `3` 与 `N_active = catOrder − 1 = 3` 数值相同，本批**不主张同源**（`3` 的来源是 `2 − (−1)`：
   `A_GR` 的非零对角元减去转动夹心在第二槽的 `−1`）；开口 `DET_THREE_VS_N_ACTIVE`。
3. 不新增常数、不新增公设；§40 的两值在本批 `h = 1 + Δλ_min` 上作为特例复现。
-/

import MUFPFormalization.TwoWayCarrierAudit
import MUFPFormalization.QuarterTurnQuantizationAudit
import Mathlib.Tactic

-- 本批多处需要 local instance 使 `⅟` 按定义归约（`let` 会使其不透明），且矩阵夹心证明的
-- simp 集中难免有多余参数；四类 linter 在此统一关闭，警告计数保持基线。
set_option warn.classDefReducibility false
set_option linter.unusedSimpArgs false
set_option linter.unusedTactic false
set_option linter.unreachableTactic false
set_option linter.style.haveILetI false

namespace MUFPF.QuantizedDetAudit

open MUFPF.IntertwinerExistenceAudit (diag2)
open MUFPF.LayeredCarrierAudit (blk)
open MUFPF.IntertwinerRepairAudit (rotGen)
open MUFPF.CarrierDetAudit (det_diag2)
open MUFPF.TwoWayCarrierAudit (diag2_mul_diag2 diag2_sub_diag2 diag2_one_one)
open MUFPF.SchurCarrierAudit (det_blk_schur)
open MUFPF.GNBridgeAudit (dlmin dlmin_pos)

/-- 框架物理层 `A_GR = diag(0, 2)`（§20 既有登记，奇异）。 -/
abbrev gr : Matrix (Fin 2) (Fin 2) ℝ := diag2 (0 : ℝ) 2

/-- 2×2 实矩阵的类型别名（缩短陈述）。 -/
abbrev M2 : Type := Matrix (Fin 2) (Fin 2) ℝ

/-- `diag(1, h)` 的可逆实例（`h ≠ 0`）：使 Schur 律可对参数 `h` 直接调用，
    且 `⅟(diag(1,h))` 在该实例下按定义即 `diag(1, h⁻¹)`。 -/
noncomputable def instDiagOne (h : ℝ) (hh : h ≠ 0) : Invertible (diag2 (1 : ℝ) h) where
  invOf := diag2 (1 : ℝ) h⁻¹
  invOf_mul_self := by
    rw [diag2_mul_diag2, inv_mul_cancel₀ hh, show (1 : ℝ) * 1 = 1 by norm_num]
    exact diag2_one_one
  mul_invOf_self := by
    rw [diag2_mul_diag2, mul_inv_cancel₀ hh, show (1 : ℝ) * 1 = 1 by norm_num]
    exact diag2_one_one

/-! ### 夹心的块运算（`A = rotGen`，四阶转动） -/

/-- `diag(a,b) · A = !![0, a; −b, 0]`。 -/
theorem diag2_mul_rot (a b : ℝ) :
    diag2 a b * rotGen = !![(0 : ℝ), a; -b, 0] := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [diag2, rotGen, Matrix.mul_apply, Fin.sum_univ_two]

/-- `diag(a,b) · (−A) = !![0, −a; b, 0]`。 -/
theorem diag2_mul_neg_rot (a b : ℝ) :
    diag2 a b * (-rotGen) = !![(0 : ℝ), -a; b, 0] := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [diag2, rotGen, Matrix.mul_apply, Fin.sum_univ_two]

/-- `(−1) · diag(a,b) = diag(−a, −b)`。 -/
theorem neg_one_mul_diag (a b : ℝ) : (-1 : M2) * diag2 a b = diag2 (-a) (-b) := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [diag2, Matrix.mul_apply, Matrix.neg_apply,
    Fin.sum_univ_two]

/-- `diag(a,b) · (−1) = diag(−a, −b)`。 -/
theorem diag_mul_neg_one (a b : ℝ) : diag2 a b * (-1 : M2) = diag2 (-a) (-b) := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [diag2, Matrix.mul_apply, Matrix.neg_apply,
    Fin.sum_univ_two]

/-- `A · diag(a,b) = !![0, b; −a, 0]`。 -/
theorem rot_mul_diag2 (a b : ℝ) :
    rotGen * diag2 a b = !![(0 : ℝ), b; -a, 0] := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [diag2, rotGen, Matrix.mul_apply, Fin.sum_univ_two]

/-- `(−A) · diag(a,b) = !![0, −b; a, 0]`。 -/
theorem neg_rot_mul_diag2 (a b : ℝ) :
    (-rotGen) * diag2 a b = !![(0 : ℝ), -b; a, 0] := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [diag2, rotGen, Matrix.mul_apply, Fin.sum_univ_two]

/-- `A · diag(a,b) · (−1) = !![0, −b; a, 0]`。 -/
theorem rot_mul_diag2_neg_one (a b : ℝ) :
    rotGen * diag2 a b * (-1 : M2) = !![(0 : ℝ), -b; a, 0] := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [diag2, rotGen, Matrix.mul_apply, Matrix.neg_apply,
    Fin.sum_univ_two]

/-- `!![0, p; q, 0] · (−1) = !![0, −p; −q, 0]`。 -/
theorem antidiag_mul_neg_one (p q : ℝ) :
    !![(0 : ℝ), p; q, 0] * (-1 : M2) = !![(0 : ℝ), -p; -q, 0] := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [Matrix.mul_apply, Matrix.neg_apply,
    Fin.sum_univ_two]

/-- `A · diag(a,b) · A = diag(−b, −a)`（转动夹心：换槽并取负）。 -/
theorem rot_sandwich (a b : ℝ) : rotGen * diag2 a b * rotGen = diag2 (-b) (-a) := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [diag2, rotGen, Matrix.mul_apply, Fin.sum_univ_two]

/-- `A · diag(a,b) · (−A) = diag(b, a)`。 -/
theorem rot_anti_sandwich (a b : ℝ) : rotGen * diag2 a b * (-rotGen) = diag2 b a := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [diag2, rotGen, Matrix.mul_apply, Fin.sum_univ_two]

/-- `(−A) · diag(a,b) · A = diag(b, a)`。 -/
theorem negrot_rot_sandwich (a b : ℝ) : (-rotGen) * diag2 a b * rotGen = diag2 b a := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [diag2, rotGen, Matrix.mul_apply, Fin.sum_univ_two]

/-- `(−1) · diag(a,b) · (−1) = diag(a,b)`。 -/
theorem neg_one_sandwich (a b : ℝ) : (-1 : M2) * diag2 a b * (-1 : M2) = diag2 a b := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [diag2, Matrix.mul_apply, Matrix.neg_apply,
    Fin.sum_univ_two]

/-- `diag(x,y) − !![0, p; q, 0] = !![x, −p; −q, y]`。 -/
theorem diag2_sub_antidiag (p q x y : ℝ) :
    diag2 x y - !![(0 : ℝ), p; q, 0] = !![x, -p; -q, y] := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [diag2, Matrix.sub_apply, Fin.sum_univ_two]

/-- 同时翻转两个耦合块的符号，Schur 项不变：`(−B)·X·(−C) = B·X·C`。 -/
theorem neg_sandwich_gen (B C X : M2) : (-B) * X * (-C) = B * X * C := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [Matrix.mul_apply, Matrix.neg_apply, Fin.sum_univ_two] <;>
    ring

/-! ### 十六个组合的读数（`B`、`C` 各自独立取 `1, −1, A, −A`） -/

/-- 纯标量、同号（`B = C = 1`）：`det = 1 − 2h`。 -/
theorem det_scalar_aligned (h : ℝ) (hh : h ≠ 0) :
    Matrix.det (blk gr (1 : M2) (1 : M2) (diag2 (1 : ℝ) h)) = 1 - 2 * h := by
  letI := instDiagOne h hh
  have hD : Matrix.det (diag2 (1 : ℝ) h) = h := by rw [det_diag2]; ring
  rw [det_blk_schur, hD, show ⅟(diag2 (1 : ℝ) h) = diag2 (1 : ℝ) h⁻¹ from rfl]
  rw [Matrix.one_mul, Matrix.mul_one, diag2_sub_diag2, det_diag2]
  field_simp
  ring

/-- 纯标量、双负同号（`B = C = −1`）：`det = 1 − 2h`（与 `B = C = 1` 同读数）。 -/
theorem det_scalar_both_neg (h : ℝ) (hh : h ≠ 0) :
    Matrix.det (blk gr (-1 : M2) (-1 : M2) (diag2 (1 : ℝ) h)) = 1 - 2 * h := by
  letI := instDiagOne h hh
  have hD : Matrix.det (diag2 (1 : ℝ) h) = h := by rw [det_diag2]; ring
  rw [det_blk_schur, hD, show ⅟(diag2 (1 : ℝ) h) = diag2 (1 : ℝ) h⁻¹ from rfl]
  rw [neg_one_sandwich, diag2_sub_diag2, det_diag2]
  field_simp
  ring

/-- 纯标量、异号（`B = 1, C = −1`）：`det = 1 + 2h`。 -/
theorem det_scalar_flipped (h : ℝ) (hh : h ≠ 0) :
    Matrix.det (blk gr (1 : M2) (-1 : M2) (diag2 (1 : ℝ) h)) = 1 + 2 * h := by
  letI := instDiagOne h hh
  have hD : Matrix.det (diag2 (1 : ℝ) h) = h := by rw [det_diag2]; ring
  rw [det_blk_schur, hD, show ⅟(diag2 (1 : ℝ) h) = diag2 (1 : ℝ) h⁻¹ from rfl]
  rw [Matrix.one_mul, diag_mul_neg_one, diag2_sub_diag2, det_diag2]
  field_simp
  ring

/-- 纯标量、异号（`B = −1, C = 1`）：`det = 1 + 2h`。 -/
theorem det_scalar_neg_pos (h : ℝ) (hh : h ≠ 0) :
    Matrix.det (blk gr (-1 : M2) (1 : M2) (diag2 (1 : ℝ) h)) = 1 + 2 * h := by
  letI := instDiagOne h hh
  have hD : Matrix.det (diag2 (1 : ℝ) h) = h := by rw [det_diag2]; ring
  rw [det_blk_schur, hD, show ⅟(diag2 (1 : ℝ) h) = diag2 (1 : ℝ) h⁻¹ from rfl]
  rw [neg_one_mul_diag, Matrix.mul_one, diag2_sub_diag2, det_diag2]
  field_simp
  ring

/-- 标量在前、转动在后（`B = 1, C = A`）：`det = 1`（`Δλ_min` 消失）。 -/
theorem det_scalar_rot (h : ℝ) (hh : h ≠ 0) :
    Matrix.det (blk gr (1 : M2) rotGen (diag2 (1 : ℝ) h)) = 1 := by
  letI := instDiagOne h hh
  have hD : Matrix.det (diag2 (1 : ℝ) h) = h := by rw [det_diag2]; ring
  rw [det_blk_schur, hD, show ⅟(diag2 (1 : ℝ) h) = diag2 (1 : ℝ) h⁻¹ from rfl]
  rw [Matrix.one_mul, diag2_mul_rot]
  try simp only [neg_neg]
  rw [diag2_sub_antidiag 1 (-h⁻¹) 0 2,
    Matrix.det_fin_two_of]
  field_simp
  ring

/-- 转动在前、标量在后（`B = A, C = 1`）：`det = 1`。 -/
theorem det_rot_scalar (h : ℝ) (hh : h ≠ 0) :
    Matrix.det (blk gr rotGen (1 : M2) (diag2 (1 : ℝ) h)) = 1 := by
  letI := instDiagOne h hh
  have hD : Matrix.det (diag2 (1 : ℝ) h) = h := by rw [det_diag2]; ring
  rw [det_blk_schur, hD, show ⅟(diag2 (1 : ℝ) h) = diag2 (1 : ℝ) h⁻¹ from rfl]
  rw [Matrix.mul_one, rot_mul_diag2]
  try simp only [neg_neg]
  rw [diag2_sub_antidiag h⁻¹ (-1) 0 2,
    Matrix.det_fin_two_of]
  field_simp
  ring

/-- 标量在前、反转动在后（`B = 1, C = −A`）：`det = 1`。 -/
theorem det_scalar_neg_rot (h : ℝ) (hh : h ≠ 0) :
    Matrix.det (blk gr (1 : M2) (-rotGen) (diag2 (1 : ℝ) h)) = 1 := by
  letI := instDiagOne h hh
  have hD : Matrix.det (diag2 (1 : ℝ) h) = h := by rw [det_diag2]; ring
  rw [det_blk_schur, hD, show ⅟(diag2 (1 : ℝ) h) = diag2 (1 : ℝ) h⁻¹ from rfl]
  rw [Matrix.one_mul, diag2_mul_neg_rot]
  try simp only [neg_neg]
  rw [diag2_sub_antidiag (-1) h⁻¹ 0 2,
    Matrix.det_fin_two_of]
  field_simp
  ring

/-- 转动在前、标量取负在后（`B = A, C = −1`）：`det = 1`。 -/
theorem det_rot_neg_scalar (h : ℝ) (hh : h ≠ 0) :
    Matrix.det (blk gr rotGen (-1 : M2) (diag2 (1 : ℝ) h)) = 1 := by
  letI := instDiagOne h hh
  have hD : Matrix.det (diag2 (1 : ℝ) h) = h := by rw [det_diag2]; ring
  rw [det_blk_schur, hD, show ⅟(diag2 (1 : ℝ) h) = diag2 (1 : ℝ) h⁻¹ from rfl]
  rw [rot_mul_diag2_neg_one]
  try simp only [neg_neg]
  rw [diag2_sub_antidiag (-h⁻¹) 1 0 2, Matrix.det_fin_two_of]
  field_simp
  ring

/-- 反标量在前、转动在后（`B = −1, C = A`）：`det = 1`。 -/
theorem det_neg_scalar_rot (h : ℝ) (hh : h ≠ 0) :
    Matrix.det (blk gr (-1 : M2) rotGen (diag2 (1 : ℝ) h)) = 1 := by
  letI := instDiagOne h hh
  have hD : Matrix.det (diag2 (1 : ℝ) h) = h := by rw [det_diag2]; ring
  rw [det_blk_schur, hD, show ⅟(diag2 (1 : ℝ) h) = diag2 (1 : ℝ) h⁻¹ from rfl]
  rw [neg_one_mul_diag, diag2_mul_rot (-1) (-h⁻¹)]
  try simp only [neg_neg]
  rw [diag2_sub_antidiag (-1) h⁻¹ 0 2,
    Matrix.det_fin_two_of]
  field_simp
  ring

/-- 反标量在前、反转动在后（`B = −1, C = −A`）：`det = 1`。 -/
theorem det_neg_scalar_neg_rot (h : ℝ) (hh : h ≠ 0) :
    Matrix.det (blk gr (-1 : M2) (-rotGen) (diag2 (1 : ℝ) h)) = 1 := by
  letI := instDiagOne h hh
  have hD : Matrix.det (diag2 (1 : ℝ) h) = h := by rw [det_diag2]; ring
  rw [det_blk_schur, hD, show ⅟(diag2 (1 : ℝ) h) = diag2 (1 : ℝ) h⁻¹ from rfl]
  rw [neg_one_mul_diag, diag2_mul_neg_rot (-1) (-h⁻¹)]
  try simp only [neg_neg]
  rw [diag2_sub_antidiag 1 (-h⁻¹) 0 2,
    Matrix.det_fin_two_of]
  field_simp
  ring

/-- 反转动在前、标量在后（`B = −A, C = 1`）：`det = 1`。 -/
theorem det_neg_rot_scalar (h : ℝ) (hh : h ≠ 0) :
    Matrix.det (blk gr (-rotGen) (1 : M2) (diag2 (1 : ℝ) h)) = 1 := by
  letI := instDiagOne h hh
  have hD : Matrix.det (diag2 (1 : ℝ) h) = h := by rw [det_diag2]; ring
  rw [det_blk_schur, hD, show ⅟(diag2 (1 : ℝ) h) = diag2 (1 : ℝ) h⁻¹ from rfl]
  rw [neg_rot_mul_diag2, Matrix.mul_one]
  try simp only [neg_neg]
  rw [diag2_sub_antidiag (-h⁻¹) 1 0 2,
    Matrix.det_fin_two_of]
  field_simp
  ring

/-- 反转动在前、反标量在后（`B = −A, C = −1`）：`det = 1`。 -/
theorem det_neg_rot_neg_scalar (h : ℝ) (hh : h ≠ 0) :
    Matrix.det (blk gr (-rotGen) (-1 : M2) (diag2 (1 : ℝ) h)) = 1 := by
  letI := instDiagOne h hh
  have hD : Matrix.det (diag2 (1 : ℝ) h) = h := by rw [det_diag2]; ring
  rw [det_blk_schur, hD, show ⅟(diag2 (1 : ℝ) h) = diag2 (1 : ℝ) h⁻¹ from rfl]
  rw [neg_rot_mul_diag2, antidiag_mul_neg_one (-h⁻¹) 1]
  try simp only [neg_neg]
  rw [diag2_sub_antidiag h⁻¹ (-1) 0 2, Matrix.det_fin_two_of]
  field_simp
  ring

/-- 转动、同号（`B = C = A`）：`det = 3`（`Δλ_min` 消失）。 -/
theorem det_rot_aligned (h : ℝ) (hh : h ≠ 0) :
    Matrix.det (blk gr rotGen rotGen (diag2 (1 : ℝ) h)) = 3 := by
  letI := instDiagOne h hh
  have hD : Matrix.det (diag2 (1 : ℝ) h) = h := by rw [det_diag2]; ring
  rw [det_blk_schur, hD, show ⅟(diag2 (1 : ℝ) h) = diag2 (1 : ℝ) h⁻¹ from rfl]
  rw [rot_sandwich, diag2_sub_diag2, det_diag2]
  field_simp
  ring

/-- 转动、双负同号（`B = C = −A`）：`det = 3`（与 `B = C = A` 同读数）。 -/
theorem det_rot_both_neg (h : ℝ) (hh : h ≠ 0) :
    Matrix.det (blk gr (-rotGen) (-rotGen) (diag2 (1 : ℝ) h)) = 3 := by
  letI := instDiagOne h hh
  have hD : Matrix.det (diag2 (1 : ℝ) h) = h := by rw [det_diag2]; ring
  rw [det_blk_schur, hD, show ⅟(diag2 (1 : ℝ) h) = diag2 (1 : ℝ) h⁻¹ from rfl]
  rw [neg_sandwich_gen rotGen rotGen (diag2 (1 : ℝ) h⁻¹), rot_sandwich,
    diag2_sub_diag2, det_diag2]
  field_simp
  ring

/-- 转动、异号（`B = A, C = −A`）：`det = −1`（`Δλ_min` 消失）。 -/
theorem det_rot_anti (h : ℝ) (hh : h ≠ 0) :
    Matrix.det (blk gr rotGen (-rotGen) (diag2 (1 : ℝ) h)) = -1 := by
  letI := instDiagOne h hh
  have hD : Matrix.det (diag2 (1 : ℝ) h) = h := by rw [det_diag2]; ring
  rw [det_blk_schur, hD, show ⅟(diag2 (1 : ℝ) h) = diag2 (1 : ℝ) h⁻¹ from rfl]
  rw [rot_anti_sandwich, diag2_sub_diag2, det_diag2]
  field_simp
  ring

/-- 转动、异号（`B = −A, C = A`）：`det = −1`。 -/
theorem det_rot_neg_pos (h : ℝ) (hh : h ≠ 0) :
    Matrix.det (blk gr (-rotGen) rotGen (diag2 (1 : ℝ) h)) = -1 := by
  letI := instDiagOne h hh
  have hD : Matrix.det (diag2 (1 : ℝ) h) = h := by rw [det_diag2]; ring
  rw [det_blk_schur, hD, show ⅟(diag2 (1 : ℝ) h) = diag2 (1 : ℝ) h⁻¹ from rfl]
  rw [negrot_rot_sandwich, diag2_sub_diag2, det_diag2]
  field_simp
  ring

/-! ### 读数表与判决 -/

/-- ★★ **16 个组合的 `det` 读数表**：同号标量 `1 − 2h`（2 个）、异号标量 `1 + 2h`（2 个）、
    混搭 `1`（8 个）、同号转动 `3`（2 个）、异号转动 `−1`（2 个）。 -/
theorem quantized_det_table (h : ℝ) (hh : h ≠ 0) :
    Matrix.det (blk gr (1 : M2) (1 : M2) (diag2 (1 : ℝ) h)) = 1 - 2 * h ∧
    Matrix.det (blk gr (-1 : M2) (-1 : M2) (diag2 (1 : ℝ) h)) = 1 - 2 * h ∧
    Matrix.det (blk gr (1 : M2) (-1 : M2) (diag2 (1 : ℝ) h)) = 1 + 2 * h ∧
    Matrix.det (blk gr (-1 : M2) (1 : M2) (diag2 (1 : ℝ) h)) = 1 + 2 * h ∧
    Matrix.det (blk gr (1 : M2) rotGen (diag2 (1 : ℝ) h)) = 1 ∧
    Matrix.det (blk gr (-1 : M2) rotGen (diag2 (1 : ℝ) h)) = 1 ∧
    Matrix.det (blk gr (1 : M2) (-rotGen) (diag2 (1 : ℝ) h)) = 1 ∧
    Matrix.det (blk gr (-1 : M2) (-rotGen) (diag2 (1 : ℝ) h)) = 1 ∧
    Matrix.det (blk gr rotGen (1 : M2) (diag2 (1 : ℝ) h)) = 1 ∧
    Matrix.det (blk gr (-rotGen) (1 : M2) (diag2 (1 : ℝ) h)) = 1 ∧
    Matrix.det (blk gr rotGen (-1 : M2) (diag2 (1 : ℝ) h)) = 1 ∧
    Matrix.det (blk gr (-rotGen) (-1 : M2) (diag2 (1 : ℝ) h)) = 1 ∧
    Matrix.det (blk gr rotGen rotGen (diag2 (1 : ℝ) h)) = 3 ∧
    Matrix.det (blk gr (-rotGen) (-rotGen) (diag2 (1 : ℝ) h)) = 3 ∧
    Matrix.det (blk gr rotGen (-rotGen) (diag2 (1 : ℝ) h)) = -1 ∧
    Matrix.det (blk gr (-rotGen) rotGen (diag2 (1 : ℝ) h)) = -1 :=
  ⟨det_scalar_aligned h hh, det_scalar_both_neg h hh, det_scalar_flipped h hh,
    det_scalar_neg_pos h hh, det_scalar_rot h hh, det_neg_scalar_rot h hh,
    det_scalar_neg_rot h hh, det_neg_scalar_neg_rot h hh, det_rot_scalar h hh,
    det_neg_rot_scalar h hh, det_rot_neg_scalar h hh, det_neg_rot_neg_scalar h hh,
    det_rot_aligned h hh, det_rot_both_neg h hh, det_rot_anti h hh,
    det_rot_neg_pos h hh⟩

/-- ★★ **三个读数与 `Δλ_min` 完全无关**（对一切 `h ≠ 0` 成立）：
    混搭读 `1`、同号转动读 `3`、异号转动读 `−1`，都不含 `h`。 -/
theorem three_readings_dlmin_free :
    (∀ h : ℝ, h ≠ 0 → Matrix.det (blk gr (1 : M2) rotGen (diag2 (1 : ℝ) h)) = 1) ∧
      (∀ h : ℝ, h ≠ 0 → Matrix.det (blk gr rotGen rotGen (diag2 (1 : ℝ) h)) = 3) ∧
      (∀ h : ℝ, h ≠ 0 → Matrix.det (blk gr rotGen (-rotGen) (diag2 (1 : ℝ) h)) = -1) :=
  ⟨det_scalar_rot, det_rot_aligned, det_rot_anti⟩

/-- ★ **`det` 读得出相对符号、读不出量**：两类耦合内部，异号与同号读数不同
    （标量类 `1 − 2h ≠ 1 + 2h`、转动类 `3 ≠ −1`）。 -/
theorem det_separates_relative_sign (h : ℝ) (hh : h ≠ 0) :
    Matrix.det (blk gr (1 : M2) (1 : M2) (diag2 (1 : ℝ) h)) ≠
        Matrix.det (blk gr (1 : M2) (-1 : M2) (diag2 (1 : ℝ) h)) ∧
      Matrix.det (blk gr rotGen rotGen (diag2 (1 : ℝ) h)) ≠
        Matrix.det (blk gr rotGen (-rotGen) (diag2 (1 : ℝ) h)) := by
  refine ⟨?_, ?_⟩
  · rw [det_scalar_aligned h hh, det_scalar_flipped h hh]
    intro heq
    have h2 : 2 * h = 0 := by linarith
    exact hh (by linarith)
  · rw [det_rot_aligned h hh, det_rot_anti h hh]
    norm_num

/-- ★★ **框架实例（`h = 1 + Δλ_min`）上的读数**：`1 − 2(1+Δλ_min) = −1.24402`、
    `1 + 2(1+Δλ_min) = 3.24402`、`1`、`3`、`−1`。 -/
theorem framework_reading_table :
    Matrix.det (blk gr (1 : M2) (1 : M2) (diag2 (1 : ℝ) (1 + dlmin))) =
        1 - 2 * (1 + dlmin) ∧
      Matrix.det (blk gr (1 : M2) (-1 : M2) (diag2 (1 : ℝ) (1 + dlmin))) =
        1 + 2 * (1 + dlmin) ∧
      Matrix.det (blk gr (1 : M2) rotGen (diag2 (1 : ℝ) (1 + dlmin))) = 1 ∧
      Matrix.det (blk gr rotGen rotGen (diag2 (1 : ℝ) (1 + dlmin))) = 3 ∧
      Matrix.det (blk gr rotGen (-rotGen) (diag2 (1 : ℝ) (1 + dlmin))) = -1 := by
  have hh : (1 : ℝ) + dlmin ≠ 0 := by
    have hpos : (0 : ℝ) < 1 + dlmin := by linarith [dlmin_pos]
    linarith
  exact ⟨det_scalar_aligned (1 + dlmin) hh, det_scalar_flipped (1 + dlmin) hh,
    det_scalar_rot (1 + dlmin) hh, det_rot_aligned (1 + dlmin) hh,
    det_rot_anti (1 + dlmin) hh⟩

/-- **R-y 判决汇总**：
    ① 纯标量同号读 `1 − 2h`（含 `Δλ_min`）；
    ② 三个读数（混搭 `1`、同号转动 `3`、异号转动 `−1`）对一切 `h` 为常数，与 `Δλ_min` 无关；
    ③ `det` 读得出相对符号（同号/异号读数不同）。 -/
theorem quantized_det_verdict (h : ℝ) (hh : h ≠ 0) :
    (Matrix.det (blk gr (1 : M2) (1 : M2) (diag2 (1 : ℝ) h)) = 1 - 2 * h) ∧
      (∀ h' : ℝ, h' ≠ 0 → Matrix.det (blk gr rotGen rotGen (diag2 (1 : ℝ) h')) = 3) ∧
      (∀ h' : ℝ, h' ≠ 0 → Matrix.det (blk gr rotGen (-rotGen) (diag2 (1 : ℝ) h')) = -1) ∧
      (Matrix.det (blk gr (1 : M2) (1 : M2) (diag2 (1 : ℝ) h)) ≠
        Matrix.det (blk gr (1 : M2) (-1 : M2) (diag2 (1 : ℝ) h))) :=
  ⟨det_scalar_aligned h hh, det_rot_aligned, det_rot_anti,
    (det_separates_relative_sign h hh).1⟩

end MUFPF.QuantizedDetAudit
