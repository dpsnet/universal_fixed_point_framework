/-
# N6Criterion.lean

Phase 72 延伸（n=6 判据形式化·第一步：括号代数底座）

目标：为 n=6 符号判据（12 因子基座）建立 Lean 代数基础：
  1. br/bk 的 Fin 6 版（bk = 块和括号 [λA, λB] = Σ_{i∈A}Σ_{j∈B} ω_i·ω_j·(z̄_i − z̄_j)）
  2. 括号代数性质（反对称/自零/双线性——与 N5 同构，仅 Fin 5 → Fin 6）
  3. 动量守恒（显式六项 Σω=0 且 Σωz̄=0）⇒ 关键块对零恒等式：
     [λ123, λ456]=0（3-3 分割）、[λ1234, λ56]=0（4-2）、[λ12345, λ6]=0（5-1）、
     [λ12, λ3456]=0（2-4）——(32) 公式因子化简的代数底座，
     也是 n=6 判定表数值闭合（609 模式 0 真违反）之外的第一层解析结构。

状态：代数骨架（对齐 N5Criterion 风格），零 sorry 目标。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Data.Int.Basic
import Mathlib.Tactic
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import MUFPFormalization.SingleMinusAmplitude

namespace N6Criterion

open SingleMinusAmplitude

/-- 粒子对括号 [λ_i, λ_j] = ω_i·ω_j·(z̄_i − z̄_j)（n=6 版） -/
noncomputable def br (w z : Fin 6 → ℝ) (i j : Fin 6) : ℝ :=
  w i * w j * (z i - z j)

/-- 块和括号 [λA, λB] = Σ_{i∈A}Σ_{j∈B} br i j（显式 .sum 写法） -/
noncomputable def bk (w z : Fin 6 → ℝ) (A B : Finset (Fin 6)) : ℝ :=
  A.sum (fun i => B.sum (fun j => br w z i j))

-- ==================== 括号代数性质（Fin 6 版） ====================

/-- 反对称：br i j + br j i = 0 -/
lemma br_antisymm (w z : Fin 6 → ℝ) (i j : Fin 6) : br w z i j + br w z j i = 0 := by
  unfold br
  ring

/-- 对角线为零：br i i = 0 -/
lemma br_self_zero (w z : Fin 6 → ℝ) (i : Fin 6) : br w z i i = 0 := by
  unfold br
  ring

/-- bk 左双线性（A∩C=∅）：bk (A∪C) B = bk A B + bk C B -/
lemma bk_add_left (w z : Fin 6 → ℝ) (A B C : Finset (Fin 6)) (hdisj : Disjoint A C) :
    bk w z (A ∪ C) B = bk w z A B + bk w z C B := by
  unfold bk
  rw [Finset.sum_union hdisj]

/-- bk 右双线性（B∩D=∅）：bk A (B∪D) = bk A B + bk A D -/
lemma bk_add_right (w z : Fin 6 → ℝ) (A B D : Finset (Fin 6)) (hdisj : Disjoint B D) :
    bk w z A (B ∪ D) = bk w z A B + bk w z A D := by
  calc
    bk w z A (B ∪ D) = A.sum (fun i => (B ∪ D).sum (fun j => br w z i j)) := by rfl
    _ = A.sum (fun i => B.sum (fun j => br w z i j) + D.sum (fun j => br w z i j)) := by
      apply Finset.sum_congr rfl
      intro i hi
      exact Finset.sum_union hdisj
    _ = bk w z A B + bk w z A D := by
      unfold bk
      rw [Finset.sum_add_distrib]

/-- 块交换反号：bk B A = -bk A B -/
lemma bk_antisymm (w z : Fin 6 → ℝ) (A B : Finset (Fin 6)) : bk w z B A = -bk w z A B := by
  calc
    bk w z B A = A.sum (fun j => B.sum (fun i => br w z i j)) := by
      unfold bk
      rw [Finset.sum_comm]
    _ = -bk w z A B := by
      unfold bk
      rw [← Finset.sum_neg_distrib]
      apply Finset.sum_congr rfl
      intro j hj
      rw [← Finset.sum_neg_distrib]
      apply Finset.sum_congr rfl
      intro i hi
      unfold br
      ring

/-- 对角块为零：bk A A = 0 -/
lemma bk_self_zero (w z : Fin 6 → ℝ) (A : Finset (Fin 6)) : bk w z A A = 0 := by
  have h : bk w z A A = -bk w z A A := bk_antisymm w z A A
  linarith

-- ==================== 动量守恒（六项）→ 块对零恒等式 ====================
-- 通用模式：设 A/B = 左右块 ω 和、ZA/ZB = 左右块 ωz̄ 和；
-- 动量守恒（六项 Σω=0、Σωz̄=0）⇒ A=-B、ZA=-ZB ⇒ bk = ZA·B − A·ZB = 0。

/-- 动量守恒（显式六项）⇒ [λ123, λ456] = 0（3-3 分割） -/
lemma bk_123_456_zero
    (w z : Fin 6 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 + w 5 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 = 0) :
    bk w z ({0, 1, 2} : Finset (Fin 6)) ({3, 4, 5} : Finset (Fin 6)) = 0 := by
  let A : ℝ := w 0 + w 1 + w 2
  let B : ℝ := w 3 + w 4 + w 5
  let ZA : ℝ := w 0 * z 0 + w 1 * z 1 + w 2 * z 2
  let ZB : ℝ := w 3 * z 3 + w 4 * z 4 + w 5 * z 5
  have hAB : A = -B := by
    dsimp [A, B]
    linarith
  have hZA : ZA = -ZB := by
    dsimp [ZA, ZB]
    linarith
  calc
    bk w z ({0, 1, 2} : Finset (Fin 6)) ({3, 4, 5} : Finset (Fin 6)) = ZA * B - A * ZB := by
      unfold bk
      simp [br, A, B, ZA, ZB]
      ring_nf
    _ = 0 := by
      rw [hAB, hZA]
      ring

/-- 动量守恒（显式六项）⇒ [λ1234, λ56] = 0（4-2 分割） -/
lemma bk_1234_56_zero
    (w z : Fin 6 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 + w 5 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 = 0) :
    bk w z ({0, 1, 2, 3} : Finset (Fin 6)) ({4, 5} : Finset (Fin 6)) = 0 := by
  let A : ℝ := w 0 + w 1 + w 2 + w 3
  let B : ℝ := w 4 + w 5
  let ZA : ℝ := w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3
  let ZB : ℝ := w 4 * z 4 + w 5 * z 5
  have hAB : A = -B := by
    dsimp [A, B]
    linarith
  have hZA : ZA = -ZB := by
    dsimp [ZA, ZB]
    linarith
  calc
    bk w z ({0, 1, 2, 3} : Finset (Fin 6)) ({4, 5} : Finset (Fin 6)) = ZA * B - A * ZB := by
      unfold bk
      simp [br, A, B, ZA, ZB]
      ring_nf
    _ = 0 := by
      rw [hAB, hZA]
      ring

/-- 动量守恒（显式六项）⇒ [λ12345, λ6] = 0（5-1 分割） -/
lemma bk_12345_6_zero
    (w z : Fin 6 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 + w 5 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 = 0) :
    bk w z ({0, 1, 2, 3, 4} : Finset (Fin 6)) ({5} : Finset (Fin 6)) = 0 := by
  let A : ℝ := w 0 + w 1 + w 2 + w 3 + w 4
  let B : ℝ := w 5
  let ZA : ℝ := w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4
  let ZB : ℝ := w 5 * z 5
  have hAB : A = -B := by
    dsimp [A, B]
    linarith
  have hZA : ZA = -ZB := by
    dsimp [ZA, ZB]
    linarith
  calc
    bk w z ({0, 1, 2, 3, 4} : Finset (Fin 6)) ({5} : Finset (Fin 6)) = ZA * B - A * ZB := by
      unfold bk
      simp [br, A, B, ZA, ZB]
      ring_nf
    _ = 0 := by
      rw [hAB, hZA]
      ring

/-- 动量守恒（显式六项）⇒ [λ12, λ3456] = 0（2-4 分割） -/
lemma bk_12_3456_zero
    (w z : Fin 6 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 + w 5 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 = 0) :
    bk w z ({0, 1} : Finset (Fin 6)) ({2, 3, 4, 5} : Finset (Fin 6)) = 0 := by
  let A : ℝ := w 0 + w 1
  let B : ℝ := w 2 + w 3 + w 4 + w 5
  let ZA : ℝ := w 0 * z 0 + w 1 * z 1
  let ZB : ℝ := w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5
  have hAB : A = -B := by
    dsimp [A, B]
    linarith
  have hZA : ZA = -ZB := by
    dsimp [ZA, ZB]
    linarith
  calc
    bk w z ({0, 1} : Finset (Fin 6)) ({2, 3, 4, 5} : Finset (Fin 6)) = ZA * B - A * ZB := by
      unfold bk
      simp [br, A, B, ZA, ZB]
      ring_nf
    _ = 0 := by
      rw [hAB, hZA]
      ring

/-- 动量守恒（显式六项）⇒ [λ1, λ23456] = 0（1-5 分割） -/
lemma bk_1_23456_zero
    (w z : Fin 6 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 + w 5 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 = 0) :
    bk w z ({0} : Finset (Fin 6)) ({1, 2, 3, 4, 5} : Finset (Fin 6)) = 0 := by
  let A : ℝ := w 0
  let B : ℝ := w 1 + w 2 + w 3 + w 4 + w 5
  let ZA : ℝ := w 0 * z 0
  let ZB : ℝ := w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5
  have hAB : A = -B := by
    dsimp [A, B]
    linarith
  have hZA : ZA = -ZB := by
    dsimp [ZA, ZB]
    linarith
  calc
    bk w z ({0} : Finset (Fin 6)) ({1, 2, 3, 4, 5} : Finset (Fin 6)) = ZA * B - A * ZB := by
      unfold bk
      simp [br, A, B, ZA, ZB]
      ring_nf
    _ = 0 := by
      rw [hAB, hZA]
      ring

-- ==================== 零恒等式与双线性组合推论 ====================
-- 零恒等式（bk_123_456_zero 等）+ 双线性（bk_add_left/right）组合出
-- (32) 项化简需要的块间关系。此处给出两个直接分解实例（双线性特例），
-- 供后续判定表解析论证引用。

/-- 左双线性实例：[λ012, λ345] = [λ01, λ345] + [λ2, λ345] -/
lemma bk_012_345_decompose_left
    (w z : Fin 6 → ℝ) :
    bk w z ({0, 1, 2} : Finset (Fin 6)) ({3, 4, 5} : Finset (Fin 6)) =
      bk w z ({0, 1} : Finset (Fin 6)) ({3, 4, 5} : Finset (Fin 6))
      + bk w z ({2} : Finset (Fin 6)) ({3, 4, 5} : Finset (Fin 6)) := by
  rw [← bk_add_left w z ({0, 1} : Finset (Fin 6)) ({3, 4, 5} : Finset (Fin 6)) ({2} : Finset (Fin 6))]
  · simp
  · simp

/-- 右双线性实例：[λ01, λ2345] = [λ01, λ345] + [λ01, λ2] -/
lemma bk_01_2345_decompose_right
    (w z : Fin 6 → ℝ) :
    bk w z ({0, 1} : Finset (Fin 6)) ({2, 3, 4, 5} : Finset (Fin 6)) =
      bk w z ({0, 1} : Finset (Fin 6)) ({3, 4, 5} : Finset (Fin 6))
      + bk w z ({0, 1} : Finset (Fin 6)) ({2} : Finset (Fin 6)) := by
  calc
    bk w z ({0, 1} : Finset (Fin 6)) ({2, 3, 4, 5} : Finset (Fin 6))
        = bk w z ({0, 1} : Finset (Fin 6)) (({3, 4, 5} : Finset (Fin 6)) ∪ ({2} : Finset (Fin 6))) := by
      congr 1
      ext x
      fin_cases x <;> simp
    _ = bk w z ({0, 1} : Finset (Fin 6)) ({3, 4, 5} : Finset (Fin 6))
      + bk w z ({0, 1} : Finset (Fin 6)) ({2} : Finset (Fin 6)) := by
      rw [bk_add_right w z ({0, 1} : Finset (Fin 6)) ({3, 4, 5} : Finset (Fin 6)) ({2} : Finset (Fin 6)) (by simp)]

end N6Criterion
