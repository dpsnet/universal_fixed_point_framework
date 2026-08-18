/-
预研形式化：t*_i 分布代数核心（外部理论预研 §7.68/§7.69）
====================================================================

推进对象：external_theory_presurvey/external_theory_derivation_chain.md §7.68/§7.69
（t*_i = d_H − k_i 权重比形式 + 非对角分量鲁棒性）。

已机器证明（零 sorry，v0.35）：
  - layerWeight/S4/dH/tstar：核心定义；
  - tstar_eq_log：t*_k = ln(S_k/S₄) 权重比形式机证（§7.69）；
  - tstar_window_endpoint：t*_1 = ln(15/e)（观测窗口终点）；
  - tstar_ordering：t*_1 > t*_2 > t*_3（层序严格降序）。
-/

import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Analysis.SpecialFunctions.Log.Basic

namespace PresurveyFormalization.TimeSpectrum

/-- 层 k 权重 S_k = e^{−k}（k = 0,1,2,...，R1 机证 S_k = s^k，s = e⁻¹）。 -/
noncomputable def layerWeight (k : ℕ) : ℝ := Real.exp (-(k : ℝ))

/-- 观测窗口阈值 S₄ = 1/15（§7.15 机器证明）。 -/
noncomputable def S4 : ℝ := 1 / 15

/-- 静默维数 d_H = ln 15（§7.15 机器证明 corollary_entropy_eq_dH）。 -/
noncomputable def dH : ℝ := Real.log 15

/-- 静默时刻 t*_k = d_H − k（§7.68 对角精确解，κ = 1）。 -/
noncomputable def tstar (k : ℕ) : ℝ := dH - (k : ℝ)

/--
权重比形式机证（§7.69）：t*_k = ln(S_k / S₄)。
代数：ln(e^{−k} / (1/15)) = ln(e^{−k} · 15) = ln(e^{−k}) + ln 15 = −k + d_H = d_H − k。
-/
theorem tstar_eq_log (k : ℕ) :
    tstar k = Real.log (layerWeight k / S4) := by
  unfold tstar dH layerWeight S4
  -- RHS: log(exp(-k) / (1/15)) = log(exp(-k) * 15)
  rw [show (1/15 : ℝ) = (15 : ℝ)⁻¹ from by norm_num]
  rw [div_eq_mul_inv, inv_inv]
  -- log(exp(-k) * 15) = log(exp(-k)) + log 15
  rw [Real.log_mul (by positivity) (by positivity)]
  -- log(exp(-k)) = -k
  rw [Real.log_exp]
  -- -k + log 15 = log 15 - k
  ring

/--
观测窗口终点（§7.69）：t*_1 = ln(15/e)（层 1 最后进入静默的时刻）。
-/
theorem tstar_window_endpoint :
    tstar 1 = Real.log (15 / Real.exp 1) := by
  unfold tstar dH
  -- log 15 - 1 = log(15/exp(1))
  have hlog_exp : Real.log (Real.exp 1) = 1 := Real.log_exp 1
  have hdiv : Real.log 15 - Real.log (Real.exp 1) = Real.log (15 / Real.exp 1) :=
    (Real.log_div (by positivity) (by positivity)).symm
  linarith

/--
层序严格降序（§7.69）：t*_1 > t*_2 > t*_3（上游层 t* 大，下游层 t* 小）。
-/
theorem tstar_ordering : tstar 1 > tstar 2 ∧ tstar 2 > tstar 3 := by
  unfold tstar dH
  push_cast
  have h12 : Real.log 15 - 1 > Real.log 15 - 2 := by linarith
  have h23 : Real.log 15 - 2 > Real.log 15 - 3 := by linarith
  exact ⟨h12, h23⟩

end PresurveyFormalization.TimeSpectrum
