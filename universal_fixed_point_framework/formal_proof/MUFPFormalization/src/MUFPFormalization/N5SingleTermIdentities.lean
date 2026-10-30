/-
# N5SingleTermIdentities.lean

Phase 72：单非零项解析闭合的代数恒等式（推论 5.2 第 1 步的代数底座）

目标：机器证明 4 条恒等式（先证伪已过：2000 随机样本残差 < 1e-8）：
  Z : 动量守恒 ⇒ bk A univ = 0（∀A，一般引理）
  E-a: [λ₂,λ₃₄₅] = [λ₁,λ₂]        （bk{1}{234} = bk{0}{1}）
  E-b: [λ₂₃,λ₄₅] = [λ₁,λ₂₃]       （bk{12}{34} = bk{0}{12}）
  E-c: [λ₂₃₄,λ₅] = [λ₅,λ₁]        （bk{123}{4} = bk{4}{0}）
这些恒等式把"困难模式 ratio 符号"归约到 8sg/扩展因子（推论 5.3 已证
C0=E6、C1=E7），构成单非零项完全解析的代数骨架。

依赖：N5Criterion（br/bk、双线性、反对称、动量守恒零括号引理）。
状态：零 sorry 目标。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Data.Int.Basic
import Mathlib.Tactic
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import MUFPFormalization.N5Criterion

namespace N5SingleTermIdentities

open N5Criterion

-- ==================== Z：动量守恒 ⇒ bk A univ = 0 ====================

/-- 动量守恒（显式五项）⇒ Σ_{j∈univ} w j = 0 -/
lemma univ_w_sum_zero
    (w : Fin 5 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 = 0) :
    Finset.univ.sum (fun j : Fin 5 => w j) = 0 := by
  have h : Finset.univ.sum (fun j : Fin 5 => w j) = w 0 + w 1 + w 2 + w 3 + w 4 := by
    simp [Fin.sum_univ_succ]
    ring
  rw [h]
  exact h_sum

/-- 动量守恒（显式五项）⇒ Σ_{j∈univ} w j * z j = 0 -/
lemma univ_wz_sum_zero
    (w z : Fin 5 → ℝ)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 = 0) :
    Finset.univ.sum (fun j : Fin 5 => w j * z j) = 0 := by
  have h : Finset.univ.sum (fun j : Fin 5 => w j * z j) =
      w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 := by
    simp [Fin.sum_univ_succ]
    ring
  rw [h]
  exact h_mom

/-- 动量守恒 ⇒ bk A univ = 0（对任意块 A） -/
lemma bk_A_univ_zero
    (w z : Fin 5 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 = 0)
    (A : Finset (Fin 5)) :
    bk w z A Finset.univ = 0 := by
  unfold bk
  have h_sum_u : Finset.univ.sum (fun j : Fin 5 => w j) = 0 := univ_w_sum_zero w h_sum
  have h_mom_u : Finset.univ.sum (fun j : Fin 5 => w j * z j) = 0 := univ_wz_sum_zero w z h_mom
  calc
    A.sum (fun i => Finset.univ.sum (fun j => w i * w j * (z i - z j)))
      = A.sum (fun i => w i * z i * Finset.univ.sum (fun j => w j) -
          w i * Finset.univ.sum (fun j => w j * z j)) := by
        apply Finset.sum_congr rfl
        intro i hi
        calc
          Finset.univ.sum (fun j => w i * w j * (z i - z j))
            = Finset.univ.sum (fun j => w i * w j * z i - w i * w j * z j) := by
              apply Finset.sum_congr rfl
              intro j hj
              ring
          _ = Finset.univ.sum (fun j => w i * w j * z i) -
              Finset.univ.sum (fun j => w i * w j * z j) := by
              rw [Finset.sum_sub_distrib]
          _ = w i * z i * Finset.univ.sum (fun j => w j) -
              w i * Finset.univ.sum (fun j => w j * z j) := by
              congr 1
              · calc
                  Finset.univ.sum (fun j => w i * w j * z i)
                    = Finset.univ.sum (fun j => (w i * z i) * w j) := by
                      apply Finset.sum_congr rfl
                      intro j hj
                      ring
                  _ = w i * z i * Finset.univ.sum (fun j => w j) := by
                      rw [← Finset.mul_sum]
              · calc
                  Finset.univ.sum (fun j => w i * w j * z j)
                    = Finset.univ.sum (fun j => w i * (w j * z j)) := by
                      apply Finset.sum_congr rfl
                      intro j hj
                      ring
                  _ = w i * Finset.univ.sum (fun j => w j * z j) := by
                      rw [← Finset.mul_sum]
    _ = A.sum (fun i => w i * (z i * 0 - 0)) := by
        apply Finset.sum_congr rfl
        intro i hi
        rw [h_sum_u, h_mom_u]
        ring
    _ = 0 := by
        simp

-- ==================== E-a：[λ₂,λ₃₄₅] = [λ₁,λ₂] ====================

/-- E-a：bk{1}{234} = bk{0}{1}
   证明链：bk{1}{01234}=0（bk_A_univ_zero）→ bk{1}{01}+bk{1}{234}=0（右双线性）
           bk{1}{01}=bk{1}{0}（bk{1}{1}=0）→ bk{1}{234}=-bk{1}{0}=bk{0}{1}（反对称） -/
lemma bk_2_345_eq_12
    (w z : Fin 5 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 = 0) :
    bk w z ({1} : Finset (Fin 5)) ({2, 3, 4} : Finset (Fin 5)) =
      bk w z ({0} : Finset (Fin 5)) ({1} : Finset (Fin 5)) := by
  have hb : bk w z ({1} : Finset (Fin 5)) ({0, 1} : Finset (Fin 5)) +
      bk w z ({1} : Finset (Fin 5)) ({2, 3, 4} : Finset (Fin 5)) = 0 := by
    have hsp : bk w z ({1} : Finset (Fin 5)) (Finset.univ) =
        bk w z ({1} : Finset (Fin 5)) ({0, 1} : Finset (Fin 5)) +
        bk w z ({1} : Finset (Fin 5)) ({2, 3, 4} : Finset (Fin 5)) := by
      exact bk_add_right w z ({1} : Finset (Fin 5)) ({0, 1} : Finset (Fin 5))
        ({2, 3, 4} : Finset (Fin 5)) (by decide)
    rw [← hsp, bk_A_univ_zero w z h_sum h_mom ({1} : Finset (Fin 5))]
  have hb01 : bk w z ({1} : Finset (Fin 5)) ({0, 1} : Finset (Fin 5)) =
      bk w z ({1} : Finset (Fin 5)) ({0} : Finset (Fin 5)) := by
    have hb' : bk w z ({1} : Finset (Fin 5)) ({0, 1} : Finset (Fin 5)) =
        bk w z ({1} : Finset (Fin 5)) ({0} : Finset (Fin 5)) +
        bk w z ({1} : Finset (Fin 5)) ({1} : Finset (Fin 5)) := by
      exact bk_add_right w z ({1} : Finset (Fin 5)) ({0} : Finset (Fin 5))
        ({1} : Finset (Fin 5)) (by decide)
    rw [hb', bk_self_zero]
    ring
  have hant : bk w z ({1} : Finset (Fin 5)) ({0} : Finset (Fin 5)) =
      -bk w z ({0} : Finset (Fin 5)) ({1} : Finset (Fin 5)) :=
    bk_antisymm w z ({0} : Finset (Fin 5)) ({1} : Finset (Fin 5))
  rw [hb01] at hb
  linarith

-- ==================== E-b：[λ₂₃,λ₄₅] = [λ₁,λ₂₃] ====================

/-- E-b：bk{12}{34} = bk{0}{12}
   证明链：bk{12}{012345}=0（bk_A_univ_zero）→ bk{12}{012}+bk{12}{34}=0
           bk{12}{012}=bk{12}{0}（bk{12}{12}=0）→ bk{12}{34}=-bk{12}{0}=bk{0}{12} -/
lemma bk_23_45_eq_1_23
    (w z : Fin 5 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 = 0) :
    bk w z ({1, 2} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)) =
      bk w z ({0} : Finset (Fin 5)) ({1, 2} : Finset (Fin 5)) := by
  have hb : bk w z ({1, 2} : Finset (Fin 5)) ({0, 1, 2} : Finset (Fin 5)) +
      bk w z ({1, 2} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)) = 0 := by
    have hsp : bk w z ({1, 2} : Finset (Fin 5)) (Finset.univ) =
        bk w z ({1, 2} : Finset (Fin 5)) ({0, 1, 2} : Finset (Fin 5)) +
        bk w z ({1, 2} : Finset (Fin 5)) ({3, 4} : Finset (Fin 5)) := by
      exact bk_add_right w z ({1, 2} : Finset (Fin 5)) ({0, 1, 2} : Finset (Fin 5))
        ({3, 4} : Finset (Fin 5)) (by decide)
    rw [← hsp, bk_A_univ_zero w z h_sum h_mom ({1, 2} : Finset (Fin 5))]
  have hb012 : bk w z ({1, 2} : Finset (Fin 5)) ({0, 1, 2} : Finset (Fin 5)) =
      bk w z ({1, 2} : Finset (Fin 5)) ({0} : Finset (Fin 5)) := by
    have hb' : bk w z ({1, 2} : Finset (Fin 5)) ({0, 1, 2} : Finset (Fin 5)) =
        bk w z ({1, 2} : Finset (Fin 5)) ({0} : Finset (Fin 5)) +
        bk w z ({1, 2} : Finset (Fin 5)) ({1, 2} : Finset (Fin 5)) := by
      exact bk_add_right w z ({1, 2} : Finset (Fin 5)) ({0} : Finset (Fin 5))
        ({1, 2} : Finset (Fin 5)) (by decide)
    rw [hb', bk_self_zero]
    ring
  have hant : bk w z ({1, 2} : Finset (Fin 5)) ({0} : Finset (Fin 5)) =
      -bk w z ({0} : Finset (Fin 5)) ({1, 2} : Finset (Fin 5)) :=
    bk_antisymm w z ({0} : Finset (Fin 5)) ({1, 2} : Finset (Fin 5))
  rw [hb012] at hb
  linarith

-- ==================== E-c：[λ₂₃₄,λ₅] = [λ₅,λ₁] ====================

/-- E-c：bk{123}{4} = bk{4}{0}
   证明链：bk{0123}{4}=0（bk_1234_5_zero）→ bk{0}{4}+bk{123}{4}=0（左双线性）
           → bk{123}{4}=-bk{0}{4}=bk{4}{0}（反对称） -/
lemma bk_234_5_eq_51
    (w z : Fin 5 → ℝ)
    (h_sum : w 0 + w 1 + w 2 + w 3 + w 4 = 0)
    (h_mom : w 0 * z 0 + w 1 * z 1 + w 2 * z 2 + w 3 * z 3 + w 4 * z 4 = 0) :
    bk w z ({1, 2, 3} : Finset (Fin 5)) ({4} : Finset (Fin 5)) =
      bk w z ({4} : Finset (Fin 5)) ({0} : Finset (Fin 5)) := by
  have hb : bk w z ({0} : Finset (Fin 5)) ({4} : Finset (Fin 5)) +
      bk w z ({1, 2, 3} : Finset (Fin 5)) ({4} : Finset (Fin 5)) = 0 := by
    have hsp : bk w z ({0, 1, 2, 3} : Finset (Fin 5)) ({4} : Finset (Fin 5)) =
        bk w z ({0} : Finset (Fin 5)) ({4} : Finset (Fin 5)) +
        bk w z ({1, 2, 3} : Finset (Fin 5)) ({4} : Finset (Fin 5)) := by
      exact bk_add_left w z ({0} : Finset (Fin 5)) ({4} : Finset (Fin 5))
        ({1, 2, 3} : Finset (Fin 5)) (by decide)
    rw [← hsp, bk_1234_5_zero w z h_sum h_mom]
  have hant : bk w z ({0} : Finset (Fin 5)) ({4} : Finset (Fin 5)) =
      -bk w z ({4} : Finset (Fin 5)) ({0} : Finset (Fin 5)) :=
    bk_antisymm w z ({4} : Finset (Fin 5)) ({0} : Finset (Fin 5))
  linarith

end N5SingleTermIdentities
