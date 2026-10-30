/-
  SilenceCriticalLayer.lean — 静默临界层定理的代数固化（Phase 104az-42/43）
  =======================================================

  背景（26.16j-89、-90 登记——"3 通道各 σ"机制桥梁）：
  - σ = S_4 = s^d_H = e^-ln15 = 1/15（静默临界层——Ruelle ζ 极点 s=ln15=d_H 处静默）
  - B = 2·k_max−1 = 15（分支数——对偶网络）
  - N_total = B/N_active = 5（总层数——B = N_active×N_total）
  - 缺口窗口阈值：0.8 = 1−N_active/B = (N_total−1)/N_total = 1−N_active·σ = 4/5
  - 唯一性：3·s^k = 3/15 的唯一解 k = ln15（对数单射）

  先证伪再证明（模式 8）：数值先证伪脚本 _phase104_s4lean_pre_tmp.py（exit 0）——
  S4 残差 1.39e-17、三表达全等 0.0、唯一性 0.0——解析恒等式——投入证明。

  状态：代数固化（机制动机诠释层——见 notes/06_photon_topology/note_paper48_reederivation_from_paper47）
-/

import Mathlib.Tactic
import MUFPFormalization.MassChainConstants

namespace MUFPF.SilenceCriticalLayer

open MUFPF.MassChain

/-! =========================================================
    常数定义
   ========================================================= -/

/-- 主动层数 N_active = 3（统一 3 定理——与 Ngen 同值）。 -/
noncomputable def Nactive : ℝ := 3

/-- 分支数 B = 2·k_max−1 = 15（对偶网络——dual_15 已证）。 -/
noncomputable def B : ℝ := 2 * kmax - 1

/-- 总层数 N_total = B/N_active = 5。 -/
noncomputable def Ntotal : ℝ := B / Nactive

/-- 缺口窗口阈值 0.8 = 1−N_active/B。 -/
noncomputable def threshold : ℝ := 1 - Nactive / B

/-- 静默临界层 S_4 = e^-ln15 = 1/15（σ 的解析身份——静默维数层）。 -/
noncomputable def S4 : ℝ := Real.exp (-Real.log 15)

/-- 收缩率 s = e^-1（静默族基元）。 -/
noncomputable def sLayer : ℝ := Real.exp (-1)

/-! =========================================================
    恒等定理
   ========================================================= -/

/-- B = 15（分支数——承 dual_15）。 -/
theorem B_eq_15 : B = 15 := by
  norm_num [B, kmax]

/-- N_total = 5（总层数）。 -/
theorem Ntotal_eq_5 : Ntotal = 5 := by
  norm_num [Ntotal, B, Nactive, kmax]

/-- 阈值 0.8 = 4/5。 -/
theorem threshold_eq_4_over_5 : threshold = 4 / 5 := by
  norm_num [threshold, B, Nactive, kmax]

/-- 三表达全等：1−N_active/B = (N_total−1)/N_total。 -/
theorem threshold_three_forms :
    1 - Nactive / B = (Ntotal - 1) / Ntotal := by
  norm_num [Ntotal, B, Nactive, kmax]

/-- σ 形式：1−N_active·σ = 4/5。 -/
theorem threshold_sigma_form : 1 - Nactive * sigma = 4 / 5 := by
  norm_num [Nactive, sigma]

/-- S_4 = σ（静默临界层 = 静默基元值 1/15——解析恒等）。 -/
theorem S4_eq_sigma : S4 = sigma := by
  unfold S4 sigma
  rw [Real.exp_neg, Real.exp_log]
  · norm_num
  · norm_num

/-- S_4 解析值 = 1/15（e^-ln15）。 -/
theorem S4_value : S4 = 1 / 15 := by
  unfold S4
  rw [Real.exp_neg, Real.exp_log]
  · norm_num
  · norm_num

/-! =========================================================
    唯一性（机制排除——3·s^k = 3/15 唯一解 k = ln15）
   ========================================================= -/

/-- 若 3·s^k = 3/15（k ∈ ℝ），则 k = ln15（exp 单射 + 对数恒等）。
    这是"3 通道各 σ"的 σ 唯一性——静默临界层 S_4 唯一命中 0.8 的代数核心。 -/
theorem uniqueness_k :
    ∀ k : ℝ, 3 * Real.exp (k * (-1)) = 3 / 15 → k = Real.log 15 := by
  intro k h
  have h1 : Real.exp (k * (-1)) = 1 / 15 := by
    -- 3 * x = 3/15 → x = 1/15（正数除）
    have h2 : Real.exp (k * (-1)) ≠ 0 := Real.exp_ne_zero _
    nlinarith [h]
  have h3 : k * (-1) = -Real.log 15 := by
    have hlog : Real.exp (-Real.log 15) = 1 / 15 := by
      rw [Real.exp_neg, Real.exp_log]
      · norm_num
      · norm_num
    have h_exp : Real.exp (k * (-1)) = Real.exp (-Real.log 15) := by
      rw [h1, hlog]
    exact Real.exp_injective h_exp
  linarith

end MUFPF.SilenceCriticalLayer
