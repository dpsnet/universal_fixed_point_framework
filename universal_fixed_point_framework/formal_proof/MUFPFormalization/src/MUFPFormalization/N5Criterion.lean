/-
# N5Criterion.lean

Phase 72 阶段 4：n=5 符号判据的形式化（推论 5.3 恒等式）

目标：证明 C0=E6、C1=E7 恒等式（仅需动量守恒，无需 R₁ 半共线）：
  sgn(bk{3}{45}) = sgn(bk{12}{123})   （C0 = E6）
  sgn(bk{34}{5}) = sgn(bk{12}{1234})  （C1 = E7）
其中 bk 为块和括号 [λA, λB] = Σ_{i∈A}Σ_{j∈B} ω_i ω_j (z̄_i − z̄_j)，
动量守恒（显式五项形式，等价于 Σuniv=0 且 Σuniv ωz̄=0）。

状态：括号代数骨架（双线性 + 反对称 + 动量守恒引理），零 sorry 目标。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Data.Int.Basic
import Mathlib.Tactic
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import MUFPFormalization.SingleMinusAmplitude

namespace N5Criterion

open SingleMinusAmplitude

/-- 粒子对括号 [λ_i, λ_j] = ω_i·ω_j·(z̄_i − z̄_j) -/
noncomputable def br (w z : Fin 5 → ℝ) (i j : Fin 5) : ℝ :=
  w i * w j * (z i - z j)

/-- 块和括号 [λA, λB] = Σ_{i∈A}Σ_{j∈B} br i j（显式 .sum 写法，避免 ∑ 语法依赖） -/
noncomputable def bk (w z : Fin 5 → ℝ) (A B : Finset (Fin 5)) : ℝ :=
  A.sum (fun i => B.sum (fun j => br w z i j))

-- ==================== 括号代数性质 ====================

/-- 反对称：br i j + br j i = 0 -/
lemma br_antisymm (w z : Fin 5 → ℝ) (i j : Fin 5) : br w z i j + br w z j i = 0 := by
  unfold br
  ring

/-- 对角线为零：br i i = 0 -/
lemma br_self_zero (w z : Fin 5 → ℝ) (i : Fin 5) : br w z i i = 0 := by
  unfold br
  ring

/-- bk 左双线性（A∩C=∅）：bk (A∪C) B = bk A B + bk C B -/
lemma bk_add_left (w z : Fin 5 → ℝ) (A B C : Finset (Fin 5)) (hdisj : Disjoint A C) :
    bk w z (A ∪ C) B = bk w z A B + bk w z C B := by
  unfold bk
  rw [Finset.sum_union hdisj]

/-- bk 右双线性（B∩D=∅）：bk A (B∪D) = bk A B + bk A D -/
lemma bk_add_right (w z : Fin 5 → ℝ) (A B D : Finset (Fin 5)) (hdisj : Disjoint B D) :
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
lemma bk_antisymm (w z : Fin 5 → ℝ) (A B : Finset (Fin 5)) : bk w z B A = -bk w z A B := by
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
lemma bk_self_zero (w z : Fin 5 → ℝ) (A : Finset (Fin 5)) : bk w z A A = 0 := by
  have h : bk w z A A = -bk w z A A := bk_antisymm w z A A
  linarith

-- ==================== 动量守恒 → 括号为零 ====================

/-- 动量守恒（显式五项）⇒ [λ123, λ45] = 0 -/
lemma bk_123_45_zero
    (w z : Fin 5 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 = 0) :
    bk w z ({0, 1, 2} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)) = 0 := by
  let A : ℝ := w 0 + w 1 + w 2
  let B : ℝ := w 3 + w 4
  let ZA : ℝ := w 0 * z 0 + w 1 * z 1 + w 2 * z 2
  let ZB : ℝ := w 3 * z 3 + w 4 * z 4
  have hAB : A = -B := by
    dsimp [A, B]
    linarith
  have hZA : ZA = -ZB := by
    dsimp [ZA, ZB]
    linarith
  calc
    bk w z ({0, 1, 2} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)) = ZA * B - A * ZB := by
      unfold bk
      simp [br, A, B, ZA, ZB]
      ring_nf
    _ = 0 := by
      rw [hAB, hZA]
      ring

/-- 动量守恒（显式五项）⇒ [λ1234, λ5] = 0 -/
lemma bk_1234_5_zero
    (w z : Fin 5 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 = 0) :
    bk w z ({0, 1, 2, 3} : Finset (Fin 5)) ({4} : Finset (Fin 5)) = 0 := by
  let A : ℝ := w 0 + w 1 + w 2 + w 3
  let B : ℝ := w 4
  let ZA : ℝ := w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3
  let ZB : ℝ := w 4 * z 4
  have hAB : A = -B := by
    dsimp [A, B]
    linarith
  have hZA : ZA = -ZB := by
    dsimp [ZA, ZB]
    linarith
  calc
    bk w z ({0, 1, 2, 3} : Finset (Fin 5)) ({4} : Finset (Fin 5)) = ZA * B - A * ZB := by
      unfold bk
      simp [br, A, B, ZA, ZB]
      ring_nf
    _ = 0 := by
      rw [hAB, hZA]
      ring

/-- 动量守恒（显式五项）⇒ [λ12, λ345] = 0 -/
lemma bk_12_345_zero
    (w z : Fin 5 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 = 0) :
    bk w z ({0, 1} : Finset (Fin 5)) ({2, 3, 4} : Finset (Fin 5)) = 0 := by
  let A : ℝ := w 0 + w 1
  let B : ℝ := w 2 + w 3 + w 4
  let ZA : ℝ := w 0 * z 0 + w 1 * z 1
  let ZB : ℝ := w 2 * z 2 + w 3 * z 3 + w 4 * z 4
  have hAB : A = -B := by
    dsimp [A, B]
    linarith
  have hZA : ZA = -ZB := by
    dsimp [ZA, ZB]
    linarith
  calc
    bk w z ({0, 1} : Finset (Fin 5)) ({2, 3, 4} : Finset (Fin 5)) = ZA * B - A * ZB := by
      unfold bk
      simp [br, A, B, ZA, ZB]
      ring_nf
    _ = 0 := by
      rw [hAB, hZA]
      ring

-- ==================== 推论 5.3：C0=E6、C1=E7 恒等式 ====================

/-- 推论 5.3（C0=E6）：sgn([λ3,λ45]) = sgn([λ12,λ123])，仅需动量守恒。
   证明链：bk{12}{123} = bk{12}{3}（右双线性+自零）
            bk{12}{345} = 0 → bk{12}{3} = -bk{12}{45}（右双线性）
            bk{123}{45} = 0 → bk{12}{45} = -bk{3}{45}（左双线性）
            ⇒ bk{12}{3} = bk{3}{45}（数值相等） -/
theorem corollary53_c0_eq_e6
    (w z : Fin 5 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 = 0) :
    sgn (bk w z ({2} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5))) =
      sgn (bk w z ({0, 1} : Finset (Fin 5)) ({0, 1, 2} : Finset (Fin 5))) := by
  have h1 : bk w z ({0, 1} : Finset (Fin 5)) ({0, 1, 2} : Finset (Fin 5)) =
      bk w z ({0, 1} : Finset (Fin 5)) ({2} : Finset (Fin 5)) := by
    have hb : bk w z ({0, 1} : Finset (Fin 5)) ({0, 1, 2} : Finset (Fin 5)) =
        bk w z ({0, 1} : Finset (Fin 5)) ({0, 1} : Finset (Fin 5)) +
        bk w z ({0, 1} : Finset (Fin 5)) ({2} : Finset (Fin 5)) := by
      exact bk_add_right w z ({0, 1} : Finset (Fin 5)) ({0, 1} : Finset (Fin 5))
        ({2} : Finset (Fin 5)) (by decide)
    rw [hb, bk_self_zero]
    ring
  have h2 : bk w z ({0, 1} : Finset (Fin 5)) ({2} : Finset (Fin 5)) =
      bk w z ({2} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)) := by
    have hb1 : bk w z ({0, 1} : Finset (Fin 5)) ({2, 3, 4} : Finset (Fin 5)) =
        bk w z ({0, 1} : Finset (Fin 5)) ({2} : Finset (Fin 5)) +
        bk w z ({0, 1} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)) := by
      exact bk_add_right w z ({0, 1} : Finset (Fin 5)) ({2} : Finset (Fin 5))
        ({3, 4} : Finset (Fin 5)) (by decide)
    have hz1 : bk w z ({0, 1} : Finset (Fin 5)) ({2, 3, 4} : Finset (Fin 5)) = 0 :=
      bk_12_345_zero w z h_sum h_mom
    have he1 : bk w z ({0, 1} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)) =
        -bk w z ({0, 1} : Finset (Fin 5)) ({2} : Finset (Fin 5)) := by
      have : bk w z ({0, 1} : Finset (Fin 5)) ({2} : Finset (Fin 5)) +
          bk w z ({0, 1} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)) = 0 := by
        rw [← hb1, hz1]
      linarith
    have hb2 : bk w z ({0, 1, 2} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)) =
        bk w z ({0, 1} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)) +
        bk w z ({2} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)) := by
      exact bk_add_left w z ({0, 1} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5))
        ({2} : Finset (Fin 5)) (by decide)
    have hz2 : bk w z ({0, 1, 2} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)) = 0 :=
      bk_123_45_zero w z h_sum h_mom
    have he2 : bk w z ({0, 1} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)) =
        -bk w z ({2} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)) := by
      have : bk w z ({0, 1} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)) +
          bk w z ({2} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)) = 0 := by
        rw [← hb2, hz2]
      linarith
    linarith
  rw [h1, h2]

/-- 推论 5.3（C1=E7）：sgn([λ34,λ5]) = sgn([λ12,λ1234])，仅需动量守恒。
   证明链：bk{12}{1234} = bk{12}{34}（右双线性+自零）
            bk{12}{345} = 0 → bk{12}{34} = -bk{12}{5}（右双线性）
            bk{1234}{5} = 0 → bk{12}{5} = -bk{34}{5}（左双线性）
            ⇒ bk{12}{34} = bk{34}{5}（数值相等） -/
theorem corollary53_c1_eq_e7
    (w z : Fin 5 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 = 0) :
    sgn (bk w z ({2, 3} : Finset (Fin 5)) ({4} : Finset (Fin 5))) =
      sgn (bk w z ({0, 1} : Finset (Fin 5)) ({0, 1, 2, 3} : Finset (Fin 5))) := by
  have h1 : bk w z ({0, 1} : Finset (Fin 5)) ({0, 1, 2, 3} : Finset (Fin 5)) =
      bk w z ({0, 1} : Finset (Fin 5)) ({2, 3} : Finset (Fin 5)) := by
    have hb : bk w z ({0, 1} : Finset (Fin 5)) ({0, 1, 2, 3} : Finset (Fin 5)) =
        bk w z ({0, 1} : Finset (Fin 5)) ({0, 1} : Finset (Fin 5)) +
        bk w z ({0, 1} : Finset (Fin 5)) ({2, 3} : Finset (Fin 5)) := by
      exact bk_add_right w z ({0, 1} : Finset (Fin 5)) ({0, 1} : Finset (Fin 5))
        ({2, 3} : Finset (Fin 5)) (by decide)
    rw [hb, bk_self_zero]
    ring
  have h2 : bk w z ({0, 1} : Finset (Fin 5)) ({2, 3} : Finset (Fin 5)) =
      bk w z ({2, 3} : Finset (Fin 5)) ({4} : Finset (Fin 5)) := by
    have hb1 : bk w z ({0, 1} : Finset (Fin 5)) ({2, 3, 4} : Finset (Fin 5)) =
        bk w z ({0, 1} : Finset (Fin 5)) ({2, 3} : Finset (Fin 5)) +
        bk w z ({0, 1} : Finset (Fin 5)) ({4} : Finset (Fin 5)) := by
      exact bk_add_right w z ({0, 1} : Finset (Fin 5)) ({2, 3} : Finset (Fin 5))
        ({4} : Finset (Fin 5)) (by decide)
    have hz1 : bk w z ({0, 1} : Finset (Fin 5)) ({2, 3, 4} : Finset (Fin 5)) = 0 :=
      bk_12_345_zero w z h_sum h_mom
    have he1 : bk w z ({0, 1} : Finset (Fin 5)) ({2, 3} : Finset (Fin 5)) =
        -bk w z ({0, 1} : Finset (Fin 5)) ({4} : Finset (Fin 5)) := by
      have : bk w z ({0, 1} : Finset (Fin 5)) ({2, 3} : Finset (Fin 5)) +
          bk w z ({0, 1} : Finset (Fin 5)) ({4} : Finset (Fin 5)) = 0 := by
        rw [← hb1, hz1]
      linarith
    have hb2 : bk w z ({0, 1, 2, 3} : Finset (Fin 5)) ({4} : Finset (Fin 5)) =
        bk w z ({0, 1} : Finset (Fin 5)) ({4} : Finset (Fin 5)) +
        bk w z ({2, 3} : Finset (Fin 5)) ({4} : Finset (Fin 5)) := by
      exact bk_add_left w z ({0, 1} : Finset (Fin 5)) ({4} : Finset (Fin 5))
        ({2, 3} : Finset (Fin 5)) (by decide)
    have hz2 : bk w z ({0, 1, 2, 3} : Finset (Fin 5)) ({4} : Finset (Fin 5)) = 0 :=
      bk_1234_5_zero w z h_sum h_mom
    have he2 : bk w z ({0, 1} : Finset (Fin 5)) ({4} : Finset (Fin 5)) =
        -bk w z ({2, 3} : Finset (Fin 5)) ({4} : Finset (Fin 5)) := by
      have : bk w z ({0, 1} : Finset (Fin 5)) ({4} : Finset (Fin 5)) +
          bk w z ({2, 3} : Finset (Fin 5)) ({4} : Finset (Fin 5)) = 0 := by
        rw [← hb2, hz2]
      linarith
    linarith
  rw [h1, h2]

end N5Criterion
