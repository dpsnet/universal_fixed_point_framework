/-
# N7Criterion.lean

Phase 72 延伸（n=7 判据形式化·级联机制论证）

目标：为 n=7 判据的**级联机制**建立 Lean 代数证明——
16 因子最小充分基座全部不含粒子 1，但 s1_A（[λ1, λ_A]）被基座完全决定。
机制 = **动量守恒三分割恒等式**：
  设 λ1 + λ_A + λ_B = 0（A,B 分割 {2..7}），则 [λ1, λ_A] = [λ_A, λ_B]。
推导：[λ1, λ_A] = [-(λ_A+λ_B), λ_A] = -[λ_A+λ_B, λ_A]
     = -([λ_A,λ_A] + [λ_B,λ_A]) = -[λ_B,λ_A] = [λ_A,λ_B]
（双线性 + 自零 + 反对称，仅需动量守恒；数值验证 40000 样本 0 违反，
  paperX_n7_identities.py，值级残差 <1e-8。）

具体实例（级联目标全部在 16 因子基座内）：
  s1_2    = s2_34567：  bk{0}{1}    = bk{1}{234567}
  s1_23   = s23_4567：  bk{0}{12}   = bk{12}{34567}
  s1_234  = s234_567：  bk{0}{123}  = bk{123}{4567}
  s1_2345 = s2345_67：  bk{0}{1234} = bk{1234}{567}
  s1_23456= s23456_7：  bk{0}{12345}= bk{12345}{6}
  s1_234567 = 0：       bk{0}{123456} = 0（1-6 分割，动量守恒直接）

证明策略（N6 同款 ZA/B 块积模式）：设
  W0 = ω1, Z0 = ω1z̄1, WA = Σ_{i∈A}ωi, ZA = Σ_{i∈A}ωi z̄i,
  WB = Σ_{i∈B}ωi, ZB = Σ_{i∈B}ωi z̄i（A∪B={2..7}）。
动量守恒 ⇒ W0=-(WA+WB), Z0=-(ZA+ZB)。则
  bk{0}{A} = Z0·WA - W0·ZA = WB·ZA - ZB·WA = ZA·WB - WA·ZB = bk{A}{B}。
第一步/末步 ring_nf 展开，中间 rw [守恒式] + ring。

状态：零 sorry 目标（参照 N6Criterion 风格）。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Data.Int.Basic
import Mathlib.Tactic
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import MUFPFormalization.SingleMinusAmplitude

namespace N7Criterion

open SingleMinusAmplitude

/-- 粒子对括号 [λ_i, λ_j] = ω_i·ω_j·(z̄_i − z̄_j)（n=7 版） -/
noncomputable def br (w z : Fin 7 → ℝ) (i j : Fin 7) : ℝ :=
  w i * w j * (z i - z j)

/-- 块和括号 [λA, λB] = Σ_{i∈A}Σ_{j∈B} br i j -/
noncomputable def bk (w z : Fin 7 → ℝ) (A B : Finset (Fin 7)) : ℝ :=
  A.sum (fun i => B.sum (fun j => br w z i j))

-- ==================== 括号代数性质（Fin 7 版，与 N5/N6 同构） ====================

lemma br_antisymm (w z : Fin 7 → ℝ) (i j : Fin 7) : br w z i j + br w z j i = 0 := by
  unfold br
  ring

lemma br_self_zero (w z : Fin 7 → ℝ) (i : Fin 7) : br w z i i = 0 := by
  unfold br
  ring

lemma bk_add_left (w z : Fin 7 → ℝ) (A B C : Finset (Fin 7)) (hdisj : Disjoint A C) :
    bk w z (A ∪ C) B = bk w z A B + bk w z C B := by
  unfold bk
  rw [Finset.sum_union hdisj]

lemma bk_add_right (w z : Fin 7 → ℝ) (A B D : Finset (Fin 7)) (hdisj : Disjoint B D) :
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

lemma bk_antisymm (w z : Fin 7 → ℝ) (A B : Finset (Fin 7)) : bk w z B A = -bk w z A B := by
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

lemma bk_self_zero (w z : Fin 7 → ℝ) (A : Finset (Fin 7)) : bk w z A A = 0 := by
  have h : bk w z A A = -bk w z A A := bk_antisymm w z A A
  linarith

-- ==================== 动量守恒（七项）→ 级联恒等式 ====================
-- 通用机制：[λ1, λ_A] = [λ_A, λ_B]（λ1 + λ_A + λ_B = 0）。
-- ZA/B 块积模式：bk{0}{A} = Z0·WA − W0·ZA → rw [守恒] → WB·ZA − ZB·WA → ring → bk{A}{B}。

/-- 动量守恒（七项）⇒ [λ1, λ234567] = 0（1-6 分割） -/
lemma bk_1_234567_zero
    (w z : Fin 7 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 + w 5 + w 6 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6 = 0) :
    bk w z ({0} : Finset (Fin 7)) ({1, 2, 3, 4, 5, 6} : Finset (Fin 7)) = 0 := by
  let W0 : ℝ := w 0
  let Z0 : ℝ := w 0 * z 0
  let WA : ℝ := w 1 + w 2 + w 3 + w 4 + w 5 + w 6
  let ZA : ℝ := w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6
  have hW0 : W0 = -WA := by
    dsimp [W0, WA]
    linarith
  have hZ0 : Z0 = -ZA := by
    dsimp [Z0, ZA]
    linarith
  calc
    bk w z ({0} : Finset (Fin 7)) ({1, 2, 3, 4, 5, 6} : Finset (Fin 7)) = Z0 * WA - W0 * ZA := by
      unfold bk
      simp [br, W0, Z0, WA, ZA]
      ring_nf
    _ = 0 := by
      rw [hW0, hZ0]
      ring

/-- 级联：s1_2 = s2_34567 —— bk{0}{1} = bk{1}{234567} -/
lemma cascade_1_2
    (w z : Fin 7 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 + w 5 + w 6 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6 = 0) :
    bk w z ({0} : Finset (Fin 7)) ({1} : Finset (Fin 7)) =
      bk w z ({1} : Finset (Fin 7)) ({2, 3, 4, 5, 6} : Finset (Fin 7)) := by
  let W0 : ℝ := w 0
  let Z0 : ℝ := w 0 * z 0
  let WA : ℝ := w 1
  let ZA : ℝ := w 1 * z 1
  let WB : ℝ := w 2 + w 3 + w 4 + w 5 + w 6
  let ZB : ℝ := w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6
  have hW0 : W0 = -(WA + WB) := by
    dsimp [W0, WA, WB]
    linarith
  have hZ0 : Z0 = -(ZA + ZB) := by
    dsimp [Z0, ZA, ZB]
    linarith
  calc
    bk w z ({0} : Finset (Fin 7)) ({1} : Finset (Fin 7)) = Z0 * WA - W0 * ZA := by
      unfold bk
      simp [br, W0, Z0, WA, ZA]
      ring_nf
    _ = WB * ZA - ZB * WA := by
      rw [hW0, hZ0]
      ring
    _ = ZA * WB - WA * ZB := by
      ring
    _ = bk w z ({1} : Finset (Fin 7)) ({2, 3, 4, 5, 6} : Finset (Fin 7)) := by
      unfold bk
      simp [br, WA, ZA, WB, ZB]
      ring_nf

/-- 级联：s1_23 = s23_4567 —— bk{0}{12} = bk{12}{34567} -/
lemma cascade_1_23
    (w z : Fin 7 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 + w 5 + w 6 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6 = 0) :
    bk w z ({0} : Finset (Fin 7)) ({1, 2} : Finset (Fin 7)) =
      bk w z ({1, 2} : Finset (Fin 7)) ({3, 4, 5, 6} : Finset (Fin 7)) := by
  let W0 : ℝ := w 0
  let Z0 : ℝ := w 0 * z 0
  let WA : ℝ := w 1 + w 2
  let ZA : ℝ := w 1 * z 1 + w 2 * z 2
  let WB : ℝ := w 3 + w 4 + w 5 + w 6
  let ZB : ℝ := w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6
  have hW0 : W0 = -(WA + WB) := by
    dsimp [W0, WA, WB]
    linarith
  have hZ0 : Z0 = -(ZA + ZB) := by
    dsimp [Z0, ZA, ZB]
    linarith
  calc
    bk w z ({0} : Finset (Fin 7)) ({1, 2} : Finset (Fin 7)) = Z0 * WA - W0 * ZA := by
      unfold bk
      simp [br, W0, Z0, WA, ZA]
      ring_nf
    _ = WB * ZA - ZB * WA := by
      rw [hW0, hZ0]
      ring
    _ = ZA * WB - WA * ZB := by
      ring
    _ = bk w z ({1, 2} : Finset (Fin 7)) ({3, 4, 5, 6} : Finset (Fin 7)) := by
      unfold bk
      simp [br, WA, ZA, WB, ZB]
      ring_nf

/-- 级联：s1_234 = s234_567 —— bk{0}{123} = bk{123}{4567} -/
lemma cascade_1_234
    (w z : Fin 7 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 + w 5 + w 6 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6 = 0) :
    bk w z ({0} : Finset (Fin 7)) ({1, 2, 3} : Finset (Fin 7)) =
      bk w z ({1, 2, 3} : Finset (Fin 7)) ({4, 5, 6} : Finset (Fin 7)) := by
  let W0 : ℝ := w 0
  let Z0 : ℝ := w 0 * z 0
  let WA : ℝ := w 1 + w 2 + w 3
  let ZA : ℝ := w 1 * z 1 + w 2 * z 2 + w 3 * z 3
  let WB : ℝ := w 4 + w 5 + w 6
  let ZB : ℝ := w 4 * z 4 + w 5 * z 5 + w 6 * z 6
  have hW0 : W0 = -(WA + WB) := by
    dsimp [W0, WA, WB]
    linarith
  have hZ0 : Z0 = -(ZA + ZB) := by
    dsimp [Z0, ZA, ZB]
    linarith
  calc
    bk w z ({0} : Finset (Fin 7)) ({1, 2, 3} : Finset (Fin 7)) = Z0 * WA - W0 * ZA := by
      unfold bk
      simp [br, W0, Z0, WA, ZA]
      ring_nf
    _ = WB * ZA - ZB * WA := by
      rw [hW0, hZ0]
      ring
    _ = ZA * WB - WA * ZB := by
      ring
    _ = bk w z ({1, 2, 3} : Finset (Fin 7)) ({4, 5, 6} : Finset (Fin 7)) := by
      unfold bk
      simp [br, WA, ZA, WB, ZB]
      ring_nf

/-- 级联：s1_2345 = s2345_67 —— bk{0}{1234} = bk{1234}{567} -/
lemma cascade_1_2345
    (w z : Fin 7 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 + w 5 + w 6 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6 = 0) :
    bk w z ({0} : Finset (Fin 7)) ({1, 2, 3, 4} : Finset (Fin 7)) =
      bk w z ({1, 2, 3, 4} : Finset (Fin 7)) ({5, 6} : Finset (Fin 7)) := by
  let W0 : ℝ := w 0
  let Z0 : ℝ := w 0 * z 0
  let WA : ℝ := w 1 + w 2 + w 3 + w 4
  let ZA : ℝ := w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4
  let WB : ℝ := w 5 + w 6
  let ZB : ℝ := w 5 * z 5 + w 6 * z 6
  have hW0 : W0 = -(WA + WB) := by
    dsimp [W0, WA, WB]
    linarith
  have hZ0 : Z0 = -(ZA + ZB) := by
    dsimp [Z0, ZA, ZB]
    linarith
  calc
    bk w z ({0} : Finset (Fin 7)) ({1, 2, 3, 4} : Finset (Fin 7)) = Z0 * WA - W0 * ZA := by
      unfold bk
      simp [br, W0, Z0, WA, ZA]
      ring_nf
    _ = WB * ZA - ZB * WA := by
      rw [hW0, hZ0]
      ring
    _ = ZA * WB - WA * ZB := by
      ring
    _ = bk w z ({1, 2, 3, 4} : Finset (Fin 7)) ({5, 6} : Finset (Fin 7)) := by
      unfold bk
      simp [br, WA, ZA, WB, ZB]
      ring_nf

/-- 级联：s1_23456 = s23456_7 —— bk{0}{12345} = bk{12345}{6} -/
lemma cascade_1_23456
    (w z : Fin 7 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 + w 5 + w 6 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6 = 0) :
    bk w z ({0} : Finset (Fin 7)) ({1, 2, 3, 4, 5} : Finset (Fin 7)) =
      bk w z ({1, 2, 3, 4, 5} : Finset (Fin 7)) ({6} : Finset (Fin 7)) := by
  let W0 : ℝ := w 0
  let Z0 : ℝ := w 0 * z 0
  let WA : ℝ := w 1 + w 2 + w 3 + w 4 + w 5
  let ZA : ℝ := w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5
  let WB : ℝ := w 6
  let ZB : ℝ := w 6 * z 6
  have hW0 : W0 = -(WA + WB) := by
    dsimp [W0, WA, WB]
    linarith
  have hZ0 : Z0 = -(ZA + ZB) := by
    dsimp [Z0, ZA, ZB]
    linarith
  calc
    bk w z ({0} : Finset (Fin 7)) ({1, 2, 3, 4, 5} : Finset (Fin 7)) = Z0 * WA - W0 * ZA := by
      unfold bk
      simp [br, W0, Z0, WA, ZA]
      ring_nf
    _ = WB * ZA - ZB * WA := by
      rw [hW0, hZ0]
      ring
    _ = ZA * WB - WA * ZB := by
      ring
    _ = bk w z ({1, 2, 3, 4, 5} : Finset (Fin 7)) ({6} : Finset (Fin 7)) := by
      unfold bk
      simp [br, WA, ZA, WB, ZB]
      ring_nf

-- ==================== 符号版级联定理（sgn 级） ====================
-- 值级相等（cascade_*）→ 符号相等（congrArg sgn）。sgn 定义见 SingleMinusAmplitude。

theorem sgn_cascade_1_2
    (w z : Fin 7 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 + w 5 + w 6 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6 = 0) :
    sgn (bk w z ({0} : Finset (Fin 7)) ({1} : Finset (Fin 7))) =
      sgn (bk w z ({1} : Finset (Fin 7)) ({2, 3, 4, 5, 6} : Finset (Fin 7))) := by
  exact congrArg sgn (cascade_1_2 w z h_sum h_mom)

theorem sgn_cascade_1_23456
    (w z : Fin 7 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 + w 5 + w 6 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6 = 0) :
    sgn (bk w z ({0} : Finset (Fin 7)) ({1, 2, 3, 4, 5} : Finset (Fin 7))) =
      sgn (bk w z ({1, 2, 3, 4, 5} : Finset (Fin 7)) ({6} : Finset (Fin 7))) := by
  exact congrArg sgn (cascade_1_23456 w z h_sum h_mom)

end N7Criterion
