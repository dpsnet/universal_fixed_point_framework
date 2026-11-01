/-
  P4DiamondScale.lean — P4「大钻石极限 = 窗口取大」的系数标度核算（2026-11-02）
  =====================================================================

  背景：S89（SilenceFamily.lean）已机检 τ = −ℓ 家族的系数化简：
  ln Δ_◇ = (π/ℓ)[(ℓ²−τ²)H + 2τD + K] ⟹ τ = −ℓ 时系数为 (0·H, −2π·D, (π/ℓ)·K)。

  本模块**只**机检该系数的标度结构，不涉及任何范畴对应：
  (i)  D 系数 = π × (2τ/ℓ)——2π = π × 2（π 为文献式 2.65 的前因子，
       2 = |2τ/ℓ| 的尖点无量纲比），**不是** 2π×ℓ（ℓ 精确约掉）；
  (ii) 对任意重标度 ℓ ↦ cℓ、τ ↦ −cℓ（c ≠ 0），D 系数恒 = −2π
       ——代数对「哪个框架量充当窗口标度 ℓ」完全不可选（不可选择性）；
  (iii) τ = 0（窗口中点）时 D 系数 = 0——中点族不生成 dilation/时间平移。

  诚实边界：以上是**文献式 2.65 的系数代数**，不是框架内生；
  「钻石 = 窗口」的范畴对应仍未导出，不得以同认/指认公设补位。
  本模块不主张 P4 完成。
-/

import Mathlib.Tactic

namespace MUFPF.P4DiamondScale

/-- ★ P4：D 系数 = π × (2τ/ℓ)——2π = π × 2 的标度核算（无 2π×ℓ 因子）。 -/
theorem p4_d_coeff_factor (ℓ τ : ℝ) (hℓ : ℓ ≠ 0) :
    (Real.pi / ℓ) * (2 * τ) = Real.pi * (2 * τ / ℓ) := by
  field_simp

/-- ★ P4：D 系数对窗口标度的任意重标度不变
    （c ≠ 0 ⟹ 恒 = −2π）——代数无法从任一候选尺度中择一。 -/
theorem p4_tip_scale_invariance (ℓ c : ℝ) (hℓ : ℓ ≠ 0) (hc : c ≠ 0) :
    (Real.pi / (c * ℓ)) * (2 * (-(c * ℓ))) = -2 * Real.pi := by
  field_simp

/-- ★ P4：τ = 0（窗口中点）时 D 系数 = 0——中点族不生成时间平移。 -/
theorem p4_center_no_dilation (ℓ : ℝ) :
    (Real.pi / ℓ) * (2 * 0) = 0 := by
  ring

/-- ★ P4：尖点族（τ = −ℓ）与中点族（τ = 0）的 D 系数互斥：
    中点为零、尖点为 −2π（ℓ ≠ 0）——两支生成元不同，不能互换。 -/
theorem p4_tip_center_dichotomy (ℓ : ℝ) (hℓ : ℓ ≠ 0) :
    (Real.pi / ℓ) * (2 * 0) ≠ (Real.pi / ℓ) * (2 * (-ℓ)) := by
  rw [p4_center_no_dilation ℓ]
  intro h
  have htip : (Real.pi / ℓ) * (2 * (-ℓ)) = -2 * Real.pi := by
    field_simp [hℓ]
  rw [htip] at h
  nlinarith [Real.pi_pos, h]

end MUFPF.P4DiamondScale
