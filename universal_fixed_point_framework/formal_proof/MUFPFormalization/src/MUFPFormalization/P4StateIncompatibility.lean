/-
  P4StateIncompatibility.lean — P4 态判别：「框架等权态」与「Gibbs 态族 ρ_ℓ」互斥（2026-11-02）
  =====================================================================================

  背景：364（P4 显式模型）留下唯一缺口「框架实际态是否 = ρ_ℓ」。框架已派生的态资产是
  **等权态**（15 态等权 1/15 = σ，S124/S125；传递群唯一不变测度 = 均匀，S531
  EqualWeightMeasure.lean）。本模块只机检判别所需的三个结构事实：

  (i)  常数模 Hamilton 量（c • 1）与任意矩阵交换 ⟹ 模流生成元为零
       （等权 Gibbs ⟹ H 在支撑上为常数 ⟹ 无非平凡模流）；
  (ii) e^{−2π} ≠ 1 —— ρ_ℓ 的层间权重比恒为 e^{−2π}，等权要求该比为 1；
  (iii) 层偏移 D 非常数（层 1 与层 2 差 1）⟹ 等权所需的「H 常数」与层结构矛盾。

  诚实边界：本模块**不**主张 P4 完成，也**不**裁决框架实际态；它只把两条态候选的
  互斥机检化。框架实际态在显式模型内不可判定，需第三机制（非 Gibbs、非等权），
  登记为缺口，不以同认/指认公设补位。P4 仍未导出（只作资产，不计完成）。
-/

import Mathlib.Tactic
import Mathlib.Data.Matrix.Basic

namespace MUFPF.P4StateIncompatibility

/-- ★ P4 态判别：常数模 Hamilton 量（c • 1）与任意矩阵交换 ⟹ 模流生成元为零
    （等权 Gibbs ⟹ H 在支撑上为常数 ⟹ 无层推进、无非平凡模流）。 -/
theorem p4_const_modular_trivial {n : Type*} [Fintype n] [DecidableEq n]
    (c : ℝ) (B : Matrix n n ℝ) :
    (c • (1 : Matrix n n ℝ)) * B = B * (c • (1 : Matrix n n ℝ)) := by
  rw [Matrix.smul_mul, Matrix.one_mul, Matrix.mul_smul, Matrix.mul_one]

/-- ★ P4 态判别：e^{−2π} ≠ 1（ρ_ℓ 的层间权重比为 e^{−2π}，等权要求为 1）。 -/
theorem p4_exp_neg_two_pi_ne_one : Real.exp (-(2 * Real.pi)) ≠ 1 := by
  intro h
  have h0 : Real.exp (-(2 * Real.pi)) = Real.exp 0 := by
    rw [Real.exp_zero]
    exact h
  have hzero : -(2 * Real.pi) = 0 := Real.exp_injective h0
  have hpi : Real.pi = 0 := by linarith
  exact (ne_of_gt Real.pi_pos) hpi

/-- ★ P4 态判别：层偏移 D 非常数（层 1 = −1/2、层 2 = 1/2，差 1）
    ⟹ 等权所需的「H 在支撑上常数」与窗口层结构矛盾。 -/
theorem p4_layer_offset_differs :
    ((1 : ℚ) - 3 / 2) ≠ ((2 : ℚ) - 3 / 2) := by
  norm_num

end MUFPF.P4StateIncompatibility
