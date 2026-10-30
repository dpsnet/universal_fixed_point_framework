/-
# N8Criterion.lean

Phase 72 延伸（n=8 判据形式化·级联机制论证）

目标：为 n=8 判据的**级联机制**建立 Lean 代数证明——
23 因子基座（20 尾部 + 3 头部补因子 s12_34/s12_345/s12_34567），
"补因子 = 级联目标缺失的粒子 1 因子"的结构解释。

机制 = **动量守恒三分割恒等式**（推广到 n=8，双家族）：
  s1_A 家族（λ1 起头）：λ1 + λ_A + λ_B = 0（A,B 分割 {2..8}）⇒ [λ1, λ_A] = [λ_A, λ_B]
  s12_X 家族（λ12 起头）：λ12 + λ_A + λ_B = 0（A,B 分割 {3..8}）⇒ [λ12, λ_A] = [λ_A, λ_B]
推导（双线性 + 自零 + 反对称，仅需动量守恒）：
  [λC, λ_A] = [-(λ_A+λ_B), λ_A] = -[λ_A+λ_B, λ_A] = -([λ_A,λ_A]+[λ_B,λ_A]) = [λ_A,λ_B]

具体实例（数值验证 40000 样本 0 违反，paperX_n8_cascade.py，原始值残差 <1e-9）：
  s1_2=s2_345678：  bk{0}{1}     = bk{1}{2345678}
  s1_23=s23_45678： bk{0}{12}    = bk{12}{345678}
  s1_234=s234_5678：bk{0}{123}   = bk{123}{45678}
  s1_2345=s2345_678：bk{0}{1234} = bk{1234}{5678}
  s1_23456=s23456_78：bk{0}{12345}= bk{12345}{678}
  s1_234567=s234567_8：bk{0}{123456}= bk{123456}{78}
  s1_2345678=0：     bk{0}{1234567} = 0（1-7 分割）
  s12_3=s3_45678：   bk{01}{2}    = bk{2}{345678}
  s12_34=s34_5678：  bk{01}{23}   = bk{23}{45678}
  s12_345=s345_678： bk{01}{234}  = bk{234}{5678}
  s12_3456=s3456_78：bk{01}{2345} = bk{2345}{678}
  s12_34567=s34567_8：bk{01}{23456}= bk{23456}{78}
  s12_345678=0：     bk{01}{234567} = 0（2-6 分割）

证明策略（N7 同款 ZA/B 块积模式）：
  s1_A：W0=w0, Z0=w0·z0；s12_X：W0=w0+w1, Z0=w0·z0+w1·z1；
  WA/ZA=左块和、WB/ZB=右块和。动量守恒 ⇒ W0=-(WA+WB), Z0=-(ZA+ZB)。则
  bk{0或01}{A} = Z0·WA − W0·ZA = WB·ZA − ZB·WA = ZA·WB − WA·ZB = bk{A}{B}。
第一步/末步 ring_nf 展开，中间 rw [守恒式] + ring。

状态：零 sorry 目标（参照 N7Criterion 风格）。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Data.Int.Basic
import Mathlib.Tactic
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import MUFPFormalization.SingleMinusAmplitude

namespace N8Criterion

open SingleMinusAmplitude

/-- 粒子对括号 [λ_i, λ_j] = ω_i·ω_j·(z̄_i − z̄_j)（n=8 版） -/
noncomputable def br (w z : Fin 8 → ℝ) (i j : Fin 8) : ℝ :=
  w i * w j * (z i - z j)

/-- 块和括号 [λA, λB] = Σ_{i∈A}Σ_{j∈B} br i j -/
noncomputable def bk (w z : Fin 8 → ℝ) (A B : Finset (Fin 8)) : ℝ :=
  A.sum (fun i => B.sum (fun j => br w z i j))

-- ==================== 括号代数性质（Fin 8 版，与 N7 同构） ====================

lemma br_antisymm (w z : Fin 8 → ℝ) (i j : Fin 8) : br w z i j + br w z j i = 0 := by
  unfold br
  ring

lemma br_self_zero (w z : Fin 8 → ℝ) (i : Fin 8) : br w z i i = 0 := by
  unfold br
  ring

lemma bk_add_left (w z : Fin 8 → ℝ) (A B C : Finset (Fin 8)) (hdisj : Disjoint A C) :
    bk w z (A ∪ C) B = bk w z A B + bk w z C B := by
  unfold bk
  rw [Finset.sum_union hdisj]

lemma bk_add_right (w z : Fin 8 → ℝ) (A B D : Finset (Fin 8)) (hdisj : Disjoint B D) :
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

lemma bk_antisymm (w z : Fin 8 → ℝ) (A B : Finset (Fin 8)) : bk w z B A = -bk w z A B := by
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

lemma bk_self_zero (w z : Fin 8 → ℝ) (A : Finset (Fin 8)) : bk w z A A = 0 := by
  have h : bk w z A A = -bk w z A A := bk_antisymm w z A A
  linarith

-- ==================== 动量守恒（八项）→ 级联恒等式 ====================

/-- 动量守恒（八项）⇒ [λ1, λ2345678] = 0（1-7 分割） -/
lemma bk_1_2345678_zero
    (w z : Fin 8 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 + w 5 + w 6 + w 7 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6 + w 7 * z 7 = 0) :
    bk w z ({0} : Finset (Fin 8)) ({1, 2, 3, 4, 5, 6, 7} : Finset (Fin 8)) = 0 := by
  let W0 : ℝ := w 0
  let Z0 : ℝ := w 0 * z 0
  let WA : ℝ := w 1 + w 2 + w 3 + w 4 + w 5 + w 6 + w 7
  let ZA : ℝ := w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6 + w 7 * z 7
  have hW0 : W0 = -WA := by
    dsimp [W0, WA]
    linarith
  have hZ0 : Z0 = -ZA := by
    dsimp [Z0, ZA]
    linarith
  calc
    bk w z ({0} : Finset (Fin 8)) ({1, 2, 3, 4, 5, 6, 7} : Finset (Fin 8)) = Z0 * WA - W0 * ZA := by
      unfold bk
      simp [br, W0, Z0, WA, ZA]
      ring_nf
    _ = 0 := by
      rw [hW0, hZ0]
      ring

/-- 动量守恒（八项）⇒ [λ12, λ345678] = 0（2-6 分割） -/
lemma bk_12_345678_zero
    (w z : Fin 8 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 + w 5 + w 6 + w 7 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6 + w 7 * z 7 = 0) :
    bk w z ({0, 1} : Finset (Fin 8)) ({2, 3, 4, 5, 6, 7} : Finset (Fin 8)) = 0 := by
  let W0 : ℝ := w 0 + w 1
  let Z0 : ℝ := w 0 * z 0 + w 1 * z 1
  let WA : ℝ := w 2 + w 3 + w 4 + w 5 + w 6 + w 7
  let ZA : ℝ := w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6 + w 7 * z 7
  have hW0 : W0 = -WA := by
    dsimp [W0, WA]
    linarith
  have hZ0 : Z0 = -ZA := by
    dsimp [Z0, ZA]
    linarith
  calc
    bk w z ({0, 1} : Finset (Fin 8)) ({2, 3, 4, 5, 6, 7} : Finset (Fin 8)) = Z0 * WA - W0 * ZA := by
      unfold bk
      simp [br, W0, Z0, WA, ZA]
      ring_nf
    _ = 0 := by
      rw [hW0, hZ0]
      ring

-- ==================== s1_A 家族（W0 = w0, Z0 = w0·z0） ====================

/-- 级联：s1_2 = s2_345678 —— bk{0}{1} = bk{1}{2345678} -/
lemma cascade_1_2
    (w z : Fin 8 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 + w 5 + w 6 + w 7 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6 + w 7 * z 7 = 0) :
    bk w z ({0} : Finset (Fin 8)) ({1} : Finset (Fin 8)) =
      bk w z ({1} : Finset (Fin 8)) ({2, 3, 4, 5, 6, 7} : Finset (Fin 8)) := by
  let W0 : ℝ := w 0
  let Z0 : ℝ := w 0 * z 0
  let WA : ℝ := w 1
  let ZA : ℝ := w 1 * z 1
  let WB : ℝ := w 2 + w 3 + w 4 + w 5 + w 6 + w 7
  let ZB : ℝ := w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6 + w 7 * z 7
  have hW0 : W0 = -(WA + WB) := by
    dsimp [W0, WA, WB]
    linarith
  have hZ0 : Z0 = -(ZA + ZB) := by
    dsimp [Z0, ZA, ZB]
    linarith
  calc
    bk w z ({0} : Finset (Fin 8)) ({1} : Finset (Fin 8)) = Z0 * WA - W0 * ZA := by
      unfold bk
      simp [br, W0, Z0, WA, ZA]
      ring_nf
    _ = WB * ZA - ZB * WA := by
      rw [hW0, hZ0]
      ring
    _ = ZA * WB - WA * ZB := by
      ring
    _ = bk w z ({1} : Finset (Fin 8)) ({2, 3, 4, 5, 6, 7} : Finset (Fin 8)) := by
      unfold bk
      simp [br, WA, ZA, WB, ZB]
      ring_nf

/-- 级联：s1_23 = s23_45678 —— bk{0}{12} = bk{12}{345678} -/
lemma cascade_1_23
    (w z : Fin 8 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 + w 5 + w 6 + w 7 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6 + w 7 * z 7 = 0) :
    bk w z ({0} : Finset (Fin 8)) ({1, 2} : Finset (Fin 8)) =
      bk w z ({1, 2} : Finset (Fin 8)) ({3, 4, 5, 6, 7} : Finset (Fin 8)) := by
  let W0 : ℝ := w 0
  let Z0 : ℝ := w 0 * z 0
  let WA : ℝ := w 1 + w 2
  let ZA : ℝ := w 1 * z 1 + w 2 * z 2
  let WB : ℝ := w 3 + w 4 + w 5 + w 6 + w 7
  let ZB : ℝ := w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6 + w 7 * z 7
  have hW0 : W0 = -(WA + WB) := by
    dsimp [W0, WA, WB]
    linarith
  have hZ0 : Z0 = -(ZA + ZB) := by
    dsimp [Z0, ZA, ZB]
    linarith
  calc
    bk w z ({0} : Finset (Fin 8)) ({1, 2} : Finset (Fin 8)) = Z0 * WA - W0 * ZA := by
      unfold bk
      simp [br, W0, Z0, WA, ZA]
      ring_nf
    _ = WB * ZA - ZB * WA := by
      rw [hW0, hZ0]
      ring
    _ = ZA * WB - WA * ZB := by
      ring
    _ = bk w z ({1, 2} : Finset (Fin 8)) ({3, 4, 5, 6, 7} : Finset (Fin 8)) := by
      unfold bk
      simp [br, WA, ZA, WB, ZB]
      ring_nf

/-- 级联：s1_234 = s234_5678 —— bk{0}{123} = bk{123}{45678} -/
lemma cascade_1_234
    (w z : Fin 8 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 + w 5 + w 6 + w 7 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6 + w 7 * z 7 = 0) :
    bk w z ({0} : Finset (Fin 8)) ({1, 2, 3} : Finset (Fin 8)) =
      bk w z ({1, 2, 3} : Finset (Fin 8)) ({4, 5, 6, 7} : Finset (Fin 8)) := by
  let W0 : ℝ := w 0
  let Z0 : ℝ := w 0 * z 0
  let WA : ℝ := w 1 + w 2 + w 3
  let ZA : ℝ := w 1 * z 1 + w 2 * z 2 + w 3 * z 3
  let WB : ℝ := w 4 + w 5 + w 6 + w 7
  let ZB : ℝ := w 4 * z 4 + w 5 * z 5 + w 6 * z 6 + w 7 * z 7
  have hW0 : W0 = -(WA + WB) := by
    dsimp [W0, WA, WB]
    linarith
  have hZ0 : Z0 = -(ZA + ZB) := by
    dsimp [Z0, ZA, ZB]
    linarith
  calc
    bk w z ({0} : Finset (Fin 8)) ({1, 2, 3} : Finset (Fin 8)) = Z0 * WA - W0 * ZA := by
      unfold bk
      simp [br, W0, Z0, WA, ZA]
      ring_nf
    _ = WB * ZA - ZB * WA := by
      rw [hW0, hZ0]
      ring
    _ = ZA * WB - WA * ZB := by
      ring
    _ = bk w z ({1, 2, 3} : Finset (Fin 8)) ({4, 5, 6, 7} : Finset (Fin 8)) := by
      unfold bk
      simp [br, WA, ZA, WB, ZB]
      ring_nf

/-- 级联：s1_2345 = s2345_678 —— bk{0}{1234} = bk{1234}{5678} -/
lemma cascade_1_2345
    (w z : Fin 8 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 + w 5 + w 6 + w 7 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6 + w 7 * z 7 = 0) :
    bk w z ({0} : Finset (Fin 8)) ({1, 2, 3, 4} : Finset (Fin 8)) =
      bk w z ({1, 2, 3, 4} : Finset (Fin 8)) ({5, 6, 7} : Finset (Fin 8)) := by
  let W0 : ℝ := w 0
  let Z0 : ℝ := w 0 * z 0
  let WA : ℝ := w 1 + w 2 + w 3 + w 4
  let ZA : ℝ := w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4
  let WB : ℝ := w 5 + w 6 + w 7
  let ZB : ℝ := w 5 * z 5 + w 6 * z 6 + w 7 * z 7
  have hW0 : W0 = -(WA + WB) := by
    dsimp [W0, WA, WB]
    linarith
  have hZ0 : Z0 = -(ZA + ZB) := by
    dsimp [Z0, ZA, ZB]
    linarith
  calc
    bk w z ({0} : Finset (Fin 8)) ({1, 2, 3, 4} : Finset (Fin 8)) = Z0 * WA - W0 * ZA := by
      unfold bk
      simp [br, W0, Z0, WA, ZA]
      ring_nf
    _ = WB * ZA - ZB * WA := by
      rw [hW0, hZ0]
      ring
    _ = ZA * WB - WA * ZB := by
      ring
    _ = bk w z ({1, 2, 3, 4} : Finset (Fin 8)) ({5, 6, 7} : Finset (Fin 8)) := by
      unfold bk
      simp [br, WA, ZA, WB, ZB]
      ring_nf

/-- 级联：s1_23456 = s23456_78 —— bk{0}{12345} = bk{12345}{678} -/
lemma cascade_1_23456
    (w z : Fin 8 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 + w 5 + w 6 + w 7 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6 + w 7 * z 7 = 0) :
    bk w z ({0} : Finset (Fin 8)) ({1, 2, 3, 4, 5} : Finset (Fin 8)) =
      bk w z ({1, 2, 3, 4, 5} : Finset (Fin 8)) ({6, 7} : Finset (Fin 8)) := by
  let W0 : ℝ := w 0
  let Z0 : ℝ := w 0 * z 0
  let WA : ℝ := w 1 + w 2 + w 3 + w 4 + w 5
  let ZA : ℝ := w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5
  let WB : ℝ := w 6 + w 7
  let ZB : ℝ := w 6 * z 6 + w 7 * z 7
  have hW0 : W0 = -(WA + WB) := by
    dsimp [W0, WA, WB]
    linarith
  have hZ0 : Z0 = -(ZA + ZB) := by
    dsimp [Z0, ZA, ZB]
    linarith
  calc
    bk w z ({0} : Finset (Fin 8)) ({1, 2, 3, 4, 5} : Finset (Fin 8)) = Z0 * WA - W0 * ZA := by
      unfold bk
      simp [br, W0, Z0, WA, ZA]
      ring_nf
    _ = WB * ZA - ZB * WA := by
      rw [hW0, hZ0]
      ring
    _ = ZA * WB - WA * ZB := by
      ring
    _ = bk w z ({1, 2, 3, 4, 5} : Finset (Fin 8)) ({6, 7} : Finset (Fin 8)) := by
      unfold bk
      simp [br, WA, ZA, WB, ZB]
      ring_nf

/-- 级联：s1_234567 = s234567_8 —— bk{0}{123456} = bk{123456}{78} -/
lemma cascade_1_234567
    (w z : Fin 8 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 + w 5 + w 6 + w 7 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6 + w 7 * z 7 = 0) :
    bk w z ({0} : Finset (Fin 8)) ({1, 2, 3, 4, 5, 6} : Finset (Fin 8)) =
      bk w z ({1, 2, 3, 4, 5, 6} : Finset (Fin 8)) ({7} : Finset (Fin 8)) := by
  let W0 : ℝ := w 0
  let Z0 : ℝ := w 0 * z 0
  let WA : ℝ := w 1 + w 2 + w 3 + w 4 + w 5 + w 6
  let ZA : ℝ := w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6
  let WB : ℝ := w 7
  let ZB : ℝ := w 7 * z 7
  have hW0 : W0 = -(WA + WB) := by
    dsimp [W0, WA, WB]
    linarith
  have hZ0 : Z0 = -(ZA + ZB) := by
    dsimp [Z0, ZA, ZB]
    linarith
  calc
    bk w z ({0} : Finset (Fin 8)) ({1, 2, 3, 4, 5, 6} : Finset (Fin 8)) = Z0 * WA - W0 * ZA := by
      unfold bk
      simp [br, W0, Z0, WA, ZA]
      ring_nf
    _ = WB * ZA - ZB * WA := by
      rw [hW0, hZ0]
      ring
    _ = ZA * WB - WA * ZB := by
      ring
    _ = bk w z ({1, 2, 3, 4, 5, 6} : Finset (Fin 8)) ({7} : Finset (Fin 8)) := by
      unfold bk
      simp [br, WA, ZA, WB, ZB]
      ring_nf

-- ==================== s12_X 家族（W0 = w0+w1, Z0 = w0·z0+w1·z1） ====================

/-- 级联：s12_3 = s3_45678 —— bk{01}{2} = bk{2}{345678} -/
lemma cascade_12_3
    (w z : Fin 8 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 + w 5 + w 6 + w 7 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6 + w 7 * z 7 = 0) :
    bk w z ({0, 1} : Finset (Fin 8)) ({2} : Finset (Fin 8)) =
      bk w z ({2} : Finset (Fin 8)) ({3, 4, 5, 6, 7} : Finset (Fin 8)) := by
  let W0 : ℝ := w 0 + w 1
  let Z0 : ℝ := w 0 * z 0 + w 1 * z 1
  let WA : ℝ := w 2
  let ZA : ℝ := w 2 * z 2
  let WB : ℝ := w 3 + w 4 + w 5 + w 6 + w 7
  let ZB : ℝ := w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6 + w 7 * z 7
  have hW0 : W0 = -(WA + WB) := by
    dsimp [W0, WA, WB]
    linarith
  have hZ0 : Z0 = -(ZA + ZB) := by
    dsimp [Z0, ZA, ZB]
    linarith
  calc
    bk w z ({0, 1} : Finset (Fin 8)) ({2} : Finset (Fin 8)) = Z0 * WA - W0 * ZA := by
      unfold bk
      simp [br, W0, Z0, WA, ZA]
      ring_nf
    _ = WB * ZA - ZB * WA := by
      rw [hW0, hZ0]
      ring
    _ = ZA * WB - WA * ZB := by
      ring
    _ = bk w z ({2} : Finset (Fin 8)) ({3, 4, 5, 6, 7} : Finset (Fin 8)) := by
      unfold bk
      simp [br, WA, ZA, WB, ZB]
      ring_nf

/-- 级联：s12_34 = s34_5678 —— bk{01}{23} = bk{23}{45678}（补因子级联） -/
lemma cascade_12_34
    (w z : Fin 8 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 + w 5 + w 6 + w 7 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6 + w 7 * z 7 = 0) :
    bk w z ({0, 1} : Finset (Fin 8)) ({2, 3} : Finset (Fin 8)) =
      bk w z ({2, 3} : Finset (Fin 8)) ({4, 5, 6, 7} : Finset (Fin 8)) := by
  let W0 : ℝ := w 0 + w 1
  let Z0 : ℝ := w 0 * z 0 + w 1 * z 1
  let WA : ℝ := w 2 + w 3
  let ZA : ℝ := w 2 * z 2 + w 3 * z 3
  let WB : ℝ := w 4 + w 5 + w 6 + w 7
  let ZB : ℝ := w 4 * z 4 + w 5 * z 5 + w 6 * z 6 + w 7 * z 7
  have hW0 : W0 = -(WA + WB) := by
    dsimp [W0, WA, WB]
    linarith
  have hZ0 : Z0 = -(ZA + ZB) := by
    dsimp [Z0, ZA, ZB]
    linarith
  calc
    bk w z ({0, 1} : Finset (Fin 8)) ({2, 3} : Finset (Fin 8)) = Z0 * WA - W0 * ZA := by
      unfold bk
      simp [br, W0, Z0, WA, ZA]
      ring_nf
    _ = WB * ZA - ZB * WA := by
      rw [hW0, hZ0]
      ring
    _ = ZA * WB - WA * ZB := by
      ring
    _ = bk w z ({2, 3} : Finset (Fin 8)) ({4, 5, 6, 7} : Finset (Fin 8)) := by
      unfold bk
      simp [br, WA, ZA, WB, ZB]
      ring_nf

/-- 级联：s12_345 = s345_678 —— bk{01}{234} = bk{234}{5678}（补因子级联） -/
lemma cascade_12_345
    (w z : Fin 8 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 + w 5 + w 6 + w 7 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6 + w 7 * z 7 = 0) :
    bk w z ({0, 1} : Finset (Fin 8)) ({2, 3, 4} : Finset (Fin 8)) =
      bk w z ({2, 3, 4} : Finset (Fin 8)) ({5, 6, 7} : Finset (Fin 8)) := by
  let W0 : ℝ := w 0 + w 1
  let Z0 : ℝ := w 0 * z 0 + w 1 * z 1
  let WA : ℝ := w 2 + w 3 + w 4
  let ZA : ℝ := w 2 * z 2 + w 3 * z 3 + w 4 * z 4
  let WB : ℝ := w 5 + w 6 + w 7
  let ZB : ℝ := w 5 * z 5 + w 6 * z 6 + w 7 * z 7
  have hW0 : W0 = -(WA + WB) := by
    dsimp [W0, WA, WB]
    linarith
  have hZ0 : Z0 = -(ZA + ZB) := by
    dsimp [Z0, ZA, ZB]
    linarith
  calc
    bk w z ({0, 1} : Finset (Fin 8)) ({2, 3, 4} : Finset (Fin 8)) = Z0 * WA - W0 * ZA := by
      unfold bk
      simp [br, W0, Z0, WA, ZA]
      ring_nf
    _ = WB * ZA - ZB * WA := by
      rw [hW0, hZ0]
      ring
    _ = ZA * WB - WA * ZB := by
      ring
    _ = bk w z ({2, 3, 4} : Finset (Fin 8)) ({5, 6, 7} : Finset (Fin 8)) := by
      unfold bk
      simp [br, WA, ZA, WB, ZB]
      ring_nf

/-- 级联：s12_3456 = s3456_78 —— bk{01}{2345} = bk{2345}{678} -/
lemma cascade_12_3456
    (w z : Fin 8 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 + w 5 + w 6 + w 7 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6 + w 7 * z 7 = 0) :
    bk w z ({0, 1} : Finset (Fin 8)) ({2, 3, 4, 5} : Finset (Fin 8)) =
      bk w z ({2, 3, 4, 5} : Finset (Fin 8)) ({6, 7} : Finset (Fin 8)) := by
  let W0 : ℝ := w 0 + w 1
  let Z0 : ℝ := w 0 * z 0 + w 1 * z 1
  let WA : ℝ := w 2 + w 3 + w 4 + w 5
  let ZA : ℝ := w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5
  let WB : ℝ := w 6 + w 7
  let ZB : ℝ := w 6 * z 6 + w 7 * z 7
  have hW0 : W0 = -(WA + WB) := by
    dsimp [W0, WA, WB]
    linarith
  have hZ0 : Z0 = -(ZA + ZB) := by
    dsimp [Z0, ZA, ZB]
    linarith
  calc
    bk w z ({0, 1} : Finset (Fin 8)) ({2, 3, 4, 5} : Finset (Fin 8)) = Z0 * WA - W0 * ZA := by
      unfold bk
      simp [br, W0, Z0, WA, ZA]
      ring_nf
    _ = WB * ZA - ZB * WA := by
      rw [hW0, hZ0]
      ring
    _ = ZA * WB - WA * ZB := by
      ring
    _ = bk w z ({2, 3, 4, 5} : Finset (Fin 8)) ({6, 7} : Finset (Fin 8)) := by
      unfold bk
      simp [br, WA, ZA, WB, ZB]
      ring_nf

/-- 级联：s12_34567 = s34567_8 —— bk{01}{23456} = bk{23456}{78}（补因子级联） -/
lemma cascade_12_34567
    (w z : Fin 8 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 + w 5 + w 6 + w 7 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6 + w 7 * z 7 = 0) :
    bk w z ({0, 1} : Finset (Fin 8)) ({2, 3, 4, 5, 6} : Finset (Fin 8)) =
      bk w z ({2, 3, 4, 5, 6} : Finset (Fin 8)) ({7} : Finset (Fin 8)) := by
  let W0 : ℝ := w 0 + w 1
  let Z0 : ℝ := w 0 * z 0 + w 1 * z 1
  let WA : ℝ := w 2 + w 3 + w 4 + w 5 + w 6
  let ZA : ℝ := w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6
  let WB : ℝ := w 7
  let ZB : ℝ := w 7 * z 7
  have hW0 : W0 = -(WA + WB) := by
    dsimp [W0, WA, WB]
    linarith
  have hZ0 : Z0 = -(ZA + ZB) := by
    dsimp [Z0, ZA, ZB]
    linarith
  calc
    bk w z ({0, 1} : Finset (Fin 8)) ({2, 3, 4, 5, 6} : Finset (Fin 8)) = Z0 * WA - W0 * ZA := by
      unfold bk
      simp [br, W0, Z0, WA, ZA]
      ring_nf
    _ = WB * ZA - ZB * WA := by
      rw [hW0, hZ0]
      ring
    _ = ZA * WB - WA * ZB := by
      ring
    _ = bk w z ({2, 3, 4, 5, 6} : Finset (Fin 8)) ({7} : Finset (Fin 8)) := by
      unfold bk
      simp [br, WA, ZA, WB, ZB]
      ring_nf

-- ==================== 符号版级联定理（sgn 级） ====================
-- 值级相等（cascade_*）→ 符号相等（congrArg sgn）。

theorem sgn_cascade_1_2
    (w z : Fin 8 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 + w 5 + w 6 + w 7 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6 + w 7 * z 7 = 0) :
    sgn (bk w z ({0} : Finset (Fin 8)) ({1} : Finset (Fin 8))) =
      sgn (bk w z ({1} : Finset (Fin 8)) ({2, 3, 4, 5, 6, 7} : Finset (Fin 8))) := by
  exact congrArg sgn (cascade_1_2 w z h_sum h_mom)

theorem sgn_cascade_1_23456
    (w z : Fin 8 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 + w 5 + w 6 + w 7 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6 + w 7 * z 7 = 0) :
    sgn (bk w z ({0} : Finset (Fin 8)) ({1, 2, 3, 4, 5} : Finset (Fin 8))) =
      sgn (bk w z ({1, 2, 3, 4, 5} : Finset (Fin 8)) ({6, 7} : Finset (Fin 8))) := by
  exact congrArg sgn (cascade_1_23456 w z h_sum h_mom)

theorem sgn_cascade_12_34
    (w z : Fin 8 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 + w 5 + w 6 + w 7 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6 + w 7 * z 7 = 0) :
    sgn (bk w z ({0, 1} : Finset (Fin 8)) ({2, 3} : Finset (Fin 8))) =
      sgn (bk w z ({2, 3} : Finset (Fin 8)) ({4, 5, 6, 7} : Finset (Fin 8))) := by
  exact congrArg sgn (cascade_12_34 w z h_sum h_mom)

theorem sgn_cascade_12_34567
    (w z : Fin 8 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 + w 5 + w 6 + w 7 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 + w 5 * z 5 + w 6 * z 6 + w 7 * z 7 = 0) :
    sgn (bk w z ({0, 1} : Finset (Fin 8)) ({2, 3, 4, 5, 6} : Finset (Fin 8))) =
      sgn (bk w z ({2, 3, 4, 5, 6} : Finset (Fin 8)) ({7} : Finset (Fin 8))) := by
  exact congrArg sgn (cascade_12_34567 w z h_sum h_mom)

end N8Criterion
