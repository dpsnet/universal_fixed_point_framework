/-
# N5ProjectionOrder.lean

Phase 72 剩余②：投影序事实 sg([λ₂₃,λ₄]) = s₂₃₄（数值层面 +1）的形式化。

定理 projection_order_fact_A：模式 A 投影序（0-based z̄₃<z̄₄<z̄₁<z̄₀<z̄₂，
即 1-based z̄₄<z̄₅<z̄₂<z̄₁<z̄₃）+ R1 ω 符号（w₁..w₃ > 0，粒子 2/3/4）⇒
sgn(bk{1,2}{3}) = +1，其中 bk{1,2}{3} = [λ₂₃,λ₄] = br 1 3 + br 2 3
（λ₂₃ 的粒子 4 与块 {3}=粒子 4 的对易展开）。

推导：br 1 3 = w₁·w₃·(z̄₁−z̄₃) > 0（w₁,w₃>0，z̄₁>z̄₃ 由序链传递）
      br 2 3 = w₂·w₃·(z̄₂−z̄₃) > 0（同，z̄₂>z̄₃）
      → bk = 两项之和 > 0 → sgn = +1。
对应 h_extra（N5HardModeA 的前提），把该前提从"假设"兑现为"可推导"。

先证伪：n5_projection_order_falsify.py，200000 样本 0 违反。
零 sorry 目标。注意 ω₁（粒子 1，R1 中 <0）不参与本括号。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Data.Int.Basic
import Mathlib.Tactic
import MUFPFormalization.N5Criterion

namespace N5ProjectionOrder

open N5Criterion SingleMinusAmplitude

/-- 投影序事实（模式 A）：sgn(bk{1,2}{3}) = +1
   前提：R1 ω 符号（粒子 2/3/4 的 ω>0）+ 模式 A 投影序
   （0-based z̄₃<z̄₄<z̄₁<z̄₀<z̄₂，即 1-based z̄₄<z̄₅<z̄₂<z̄₁<z̄₃）。 -/
theorem projection_order_fact_A (w z : Fin 5 → ℝ)
    (h_om2 : 0 < w 1) (h_om3 : 0 < w 2) (h_om4 : 0 < w 3)
    (h_ord1 : z 3 < z 4) (h_ord2 : z 4 < z 1) (h_ord3 : z 1 < z 0) (h_ord4 : z 0 < z 2) :
    sgn (bk w z ({1, 2} : Finset (Fin 5)) ({3} : Finset (Fin 5))) = 1 := by
  -- 展开 bk：{1,2} × {3} → br 1 3 + br 2 3
  have hb : bk w z ({1, 2} : Finset (Fin 5)) ({3} : Finset (Fin 5)) = br w z 1 3 + br w z 2 3 := by
    unfold bk
    simp [br]
  -- br 1 3 = w₁·w₃·(z̄₁−z̄₃) > 0：z̄₁−z̄₃ > 0（序链 z₃<z₄<z₁ 传递）
  have hz13 : 0 < z 1 - z 3 := by linarith
  have hbr13 : 0 < br w z 1 3 := by
    unfold br
    positivity
  -- br 2 3 = w₂·w₃·(z̄₂−z̄₃) > 0：z̄₂−z̄₃ > 0（序链 z₃<z₄<z₁<z₀<z₂ 传递）
  have hz23 : 0 < z 2 - z 3 := by linarith
  have hbr23 : 0 < br w z 2 3 := by
    unfold br
    positivity
  -- bk = br 1 3 + br 2 3 > 0（两项全正）
  have hbpos : 0 < bk w z ({1, 2} : Finset (Fin 5)) ({3} : Finset (Fin 5)) := by
    rw [hb]
    exact add_pos hbr13 hbr23
  -- sgn = +1
  exact sgn_of_gt_zero hbpos

/-- 逆序版本（模式 B 的对称事实）：0-based z̄₂<z̄₀<z̄₁<z̄₄<z̄₃ ⇒ sgn(bk{1,2}{3}) = -1。
   用于模式 B（A_BG=−1 ⟺ E6=E7=+1）的签名翻转。 -/
theorem projection_order_fact_B (w z : Fin 5 → ℝ)
    (h_om2 : 0 < w 1) (h_om3 : 0 < w 2) (h_om4 : 0 < w 3)
    (h_ord1 : z 2 < z 0) (h_ord2 : z 0 < z 1) (h_ord3 : z 1 < z 4) (h_ord4 : z 4 < z 3) :
    sgn (bk w z ({1, 2} : Finset (Fin 5)) ({3} : Finset (Fin 5))) = -1 := by
  have hb : bk w z ({1, 2} : Finset (Fin 5)) ({3} : Finset (Fin 5)) = br w z 1 3 + br w z 2 3 := by
    unfold bk
    simp [br]
  -- z̄₁−z̄₃ < 0（z₁<z₄<z₃ 传递）、z̄₂−z̄₃ < 0（z₂<z₀<z₁<z₄<z₃ 传递）
  have hz13 : z 1 - z 3 < 0 := by linarith
  have hw13pos : 0 < w 1 * w 3 := mul_pos h_om2 h_om4
  have hbr13 : br w z 1 3 < 0 := by
    unfold br
    exact mul_neg_of_pos_of_neg hw13pos hz13
  have hz23 : z 2 - z 3 < 0 := by linarith
  have hw23pos : 0 < w 2 * w 3 := mul_pos h_om3 h_om4
  have hbr23 : br w z 2 3 < 0 := by
    unfold br
    exact mul_neg_of_pos_of_neg hw23pos hz23
  have hbneg : bk w z ({1, 2} : Finset (Fin 5)) ({3} : Finset (Fin 5)) < 0 := by
    rw [hb]
    exact add_neg hbr13 hbr23
  exact sgn_of_lt_zero hbneg

end N5ProjectionOrder
