/-
  G3KMSBetaToModular.lean — G3-P2-3（记号更正版）：β=1 ⟹ 模哈密顿量谱间隔归一 1 ⟹ Δ_mod = e^{−2π}
  =====================================================================================

  **纠偏说明（P7-5e-367）**：上一版 `G3KMSBetaToDelta.lean` 把谱隙记作 Δ 并推出「Δ=1」，
  这是**记号误用**：
  - MUFPF 原生 **Δ** = `spExchangeLaw` 交换律偏差（HigherSpCategory.lean 的 Δ 2-胞腔），
    是结构常数（Δ≠0 ⟺ δ≠0 ⟺ G_N>0），**不是谱隙**，也不能被赋值为 1；
  - 文献侧 **Δ_mod** = 模算子（Tomita–Takesaki）；RESEARCH_STATE 明令「禁止混用」：
    框架 Δ 原生保持、文献侧加注 Δ_mod。
  - S97：`Δ_mod = e^{−2πM}`（**M = 模哈密顿量**，自伴算子；2026-11-02 用户更正，
    原称「模指数」作废），模流 `Δ_mod^{it}` 的**参数周期 = 1/M**（不是 2π/M）；
    2π 在模流语境是 BW 指数系数与 Rindler 逆温 `β = 2π/K`。

  本模块给出纠偏后的代数骨架（谱隙一律记 **M**，Δ_mod 只表示模算子）：

  (i)   尺度协变：`(H,β) ↦ (λH, β/λ)` 保态不变 ⟹ β 单独不内蕴；
  (ii)  模流参数周期 = 1/M（`(1/M)·M = 1`）；周期归一为 1 ⟹ 谱间隔 M = 1；
  (iii) M = 1 ⟹ `Δ_mod = e^{−2πM} = e^{−2π}`（S106 一致）；
  (iv)  层步长 1 ⟹ 每层模权比 `Δ_mod^{M+1}/Δ_mod^M = e^{−2π}`；
  (v)   层偏移 D 的层间步长 = 1。

  诚实边界：归一化前提「模流参数周期取 1」是解释性输入（非范畴导出）；
  载体（RecObj 忠实正规态/模算子/状态空间）未定义，vN 完成性未证。
  P2 未成立，G3 未闭合，不关闭任何项（226 挂起、k(2) 开放）。
-/

import Mathlib.Tactic
import Mathlib.Data.Complex.Basic

namespace MUFPF.G3KMSBetaToModular

/-- ★ 尺度协变（态）：ρ_{β/λ}(λ·M) = ρ_β(M)——β 单独不内蕴。 -/
theorem p2_state_scale_invariant (β lam M : ℝ) (hlam : lam ≠ 0) :
    Real.exp (-((β / lam) * (lam * M))) = Real.exp (-(β * M)) := by
  congr 1
  field_simp

/-- ★ 任意 β ≠ 0 可归一：β ⟹ 1。 -/
theorem p2_beta_normalizable (β : ℝ) (hβ : β ≠ 0) : β * (1 / β) = 1 := by
  field_simp

/-- ★ 流的时间重标：σ_t^{(λH)} = σ_{tλ}^{(H)}。 -/
theorem p2_flow_scale (t lam M : ℝ) :
    Complex.exp (Complex.I * (t * (lam * M))) = Complex.exp (Complex.I * ((t * lam) * M)) := by
  congr 1
  ring

/-- ★ 模流参数周期 = 1/M（`Δ_mod = e^{−2πM}` ⟹ `Δ_mod^{it}` 周期 1/M）。 -/
theorem p2_mod_period_reciprocal (M : ℝ) (hM : M ≠ 0) : (1 / M) * M = 1 := by
  field_simp

/-- ★ 参数周期归一为 1 ⟹ 谱间隔 M = 1（模哈密顿量谱间隔归一，非标量赋值）。 -/
theorem p2_mod_period_unit_implies_index_one (M : ℝ) (hM : M ≠ 0)
    (h : 1 / M = 1) : M = 1 := by
  field_simp at h
  linarith

/-- ★ M = 1 ⟹ `Δ_mod = e^{−2πM} = e^{−2π}`（S106）。 -/
theorem p2_mod_operator_index_one :
    Real.exp (-(2 * Real.pi * 1)) = Real.exp (-(2 * Real.pi)) := by
  congr 1
  ring

/-- ★ 层步长 1 ⟹ 每层模权比 `Δ_mod^{M+1}/Δ_mod^M = e^{−2π}`。 -/
theorem p2_layer_ratio (M : ℝ) :
    Real.exp (-(2 * Real.pi * (M + 1))) =
      Real.exp (-(2 * Real.pi * M)) * Real.exp (-(2 * Real.pi)) := by
  rw [← Real.exp_add]
  congr 1
  ring

/-- ★ 层偏移 D 的层间步长 = 1。 -/
theorem p2_layer_step_unit (n : ℚ) :
    ((n + 1) - 3 / 2) - (n - 3 / 2) = 1 := by
  ring

end MUFPF.G3KMSBetaToModular
