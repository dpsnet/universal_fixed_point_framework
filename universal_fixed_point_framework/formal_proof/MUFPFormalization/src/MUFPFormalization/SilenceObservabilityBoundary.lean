/-
  SilenceObservabilityBoundary.lean — 可观测性边界的代数固化（Phase 104az-45）
  =======================================================

  背景（26.16j-92 登记——用户洞察"静默临界层 = 可观测界面到不可观测的过渡层"）：
  - rho(s) = B·e^-s（分支收缩积——B=15 分支 × 收缩率 e^-s）
  - Moran/Bowen 临界：rho(d_H) = 15·e^-ln15 = 1（B·r^dH = 1 —— 08_silence §13.2）
  - 可观测性域分割：rho(s) < 1 ⟺ s > ln15（收敛/可观测）
                        rho(s) > 1 ⟺ s < ln15（发散/不可观测）
                        rho(s) = 1 ⟺ s = ln15（临界/可观测性边界）
  - 静默临界层身份：S_4 = e^-dH = 1/B —— rho = 1 的临界点对应的收缩值
    —— "静默临界层 = 可观测性边界的收缩值"（假说的数学核心）

  先证伪再证明（模式 8）：数值先证伪脚本 _phase104_obsboundary_leanpre_tmp.py
  （rho(d_H)=1 残差 0.0、20 样本域分割全对、临界根唯一残差 4.4e-16——exit 0）。

  状态：代数固化（物理语义"可观测性过渡层"为假说层——诚实边界保持）
-/

import Mathlib.Tactic
import MUFPFormalization.MassChainConstants

namespace MUFPF.ObservabilityBoundary

open MUFPF.MassChain

/-! =========================================================
    定义
   ========================================================= -/

/-- 分支收缩积 rho(s) = B·e^-s（B=15 分支——ζ_R 分母项）。 -/
noncomputable def rho (s : ℝ) : ℝ := 15 * Real.exp (-s)

/-- 静默临界层收缩值 S_4 = e^-dH = 1/15（承 SilenceCriticalLayer.S4_value）。 -/
noncomputable def S4 : ℝ := Real.exp (-Real.log 15)

/-! =========================================================
    rho 临界（Moran/Bowen）
   ========================================================= -/

/-- exp(-log 15) = 1/15（对数恒等）。 -/
theorem exp_neg_log15 : Real.exp (-Real.log 15) = 1 / 15 := by
  rw [Real.exp_neg, Real.exp_log]
  · norm_num
  · norm_num

/-- S_4 = 1/15。 -/
theorem S4_value : S4 = 1 / 15 := by
  unfold S4
  exact exp_neg_log15

/-- rho(d_H) = 1（Moran 临界——B·r^dH = 1——可观测性边界）。 -/
theorem rho_at_dH : rho (Real.log 15) = 1 := by
  unfold rho
  rw [Real.exp_neg, Real.exp_log]
  · norm_num
  · norm_num

/-! =========================================================
    可观测性域分割（exp 严格单调）
   ========================================================= -/

/-- 辅助：15·x < 1 ⟺ x < 1/15（x>0）。 -/
theorem mul15_lt_iff (x : ℝ) (_hx : 0 < x) : 15 * x < 1 ↔ x < 1 / 15 := by
  constructor
  · intro h
    nlinarith
  · intro h
    nlinarith

/-- 收敛域：rho(s) < 1 ⟺ s > ln15（可观测——exp 单调）。 -/
theorem rho_lt_one_iff_gt :
    rho s < 1 ↔ s > Real.log 15 := by
  unfold rho
  constructor
  · intro h
    have hx : 0 < Real.exp (-s) := Real.exp_pos _
    have h1 : Real.exp (-s) < 1 / 15 := (mul15_lt_iff (Real.exp (-s)) hx).mp h
    have h2 : Real.exp (-s) < Real.exp (-Real.log 15) := by
      rw [exp_neg_log15]
      exact h1
    have h3 : -s < -Real.log 15 := Real.exp_strictMono.lt_iff_lt.mp h2
    linarith
  · intro h
    have h3 : -s < -Real.log 15 := by linarith
    have h2 : Real.exp (-s) < Real.exp (-Real.log 15) := Real.exp_strictMono.lt_iff_lt.mpr h3
    have h1 : Real.exp (-s) < 1 / 15 := by
      rw [← exp_neg_log15]
      exact h2
    have hx : 0 < Real.exp (-s) := Real.exp_pos _
    exact (mul15_lt_iff (Real.exp (-s)) hx).mpr h1

/-- 发散域：rho(s) > 1 ⟺ s < ln15（不可观测——exp 单调）。 -/
theorem rho_gt_one_iff_lt :
    rho s > 1 ↔ s < Real.log 15 := by
  unfold rho
  constructor
  · intro h
    have hx : 0 < Real.exp (-s) := Real.exp_pos _
    have h1 : 1 / 15 < Real.exp (-s) := by
      -- 15*x > 1 -> x > 1/15（与 mul15_lt_iff 对称）
      have hlt : 15 * (1 / 15) < 15 * Real.exp (-s) := by
        norm_num at h ⊢
        exact h
      nlinarith
    have h2 : Real.exp (-Real.log 15) < Real.exp (-s) := by
      rw [exp_neg_log15]
      exact h1
    have h3 : -Real.log 15 < -s := Real.exp_strictMono.lt_iff_lt.mp h2
    linarith
  · intro h
    have h3 : -Real.log 15 < -s := by linarith
    have h2 : Real.exp (-Real.log 15) < Real.exp (-s) := Real.exp_strictMono.lt_iff_lt.mpr h3
    have h1 : 1 / 15 < Real.exp (-s) := by
      rw [← exp_neg_log15]
      exact h2
    have hx : 0 < Real.exp (-s) := Real.exp_pos _
    nlinarith

/-! =========================================================
    临界唯一性
   ========================================================= -/

/-- 辅助：15·x = 1 ⟺ x = 1/15（x>0）。 -/
theorem mul15_eq_iff (x : ℝ) (_hx : 0 < x) : 15 * x = 1 ↔ x = 1 / 15 := by
  constructor
  · intro h
    nlinarith
  · intro h
    nlinarith

/-- 临界唯一：rho(s) = 1 ⟺ s = ln15（可观测性边界唯一——exp 单射）。 -/
theorem rho_eq_one_iff :
    rho s = 1 ↔ s = Real.log 15 := by
  unfold rho
  constructor
  · intro h
    have hx : 0 < Real.exp (-s) := Real.exp_pos _
    have h1 : Real.exp (-s) = 1 / 15 := (mul15_eq_iff (Real.exp (-s)) hx).mp h
    have h2 : Real.exp (-s) = Real.exp (-Real.log 15) := by
      rw [exp_neg_log15]
      exact h1
    have h3 : -s = -Real.log 15 := Real.exp_injective h2
    linarith
  · intro h
    rw [h]
    exact rho_at_dH

/-! =========================================================
    静默临界层 = 可观测性边界（假说数学核心）
   ========================================================= -/

/-- 静默临界层是 rho=1（可观测性边界）对应的收缩值：
    rho(s) = 1 ⟺ e^-s = 1/15 = S_4。
    —— "可观测性过渡层"假说的代数核心：边界处收缩值恰为静默临界层。 -/
theorem silence_layer_is_obs_boundary :
    rho s = 1 ↔ Real.exp (-s) = 1 / 15 := by
  unfold rho
  constructor
  · intro h
    have hx : 0 < Real.exp (-s) := Real.exp_pos _
    exact (mul15_eq_iff (Real.exp (-s)) hx).mp h
  · intro h
    have hx : 0 < Real.exp (-s) := Real.exp_pos _
    exact (mul15_eq_iff (Real.exp (-s)) hx).mpr h

end MUFPF.ObservabilityBoundary
