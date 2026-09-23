-- ============================================================
-- UFPF → MUFPF 更名通知
-- ============================================================
-- 本文件属于 Universal Fixed Point Framework (UFPF)。
-- 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
-- 更名计划详见：roadmap/mu_renaming_plan.md
-- ============================================================

import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic
import MUFPFormalization.SpectralFlowRG

open Real

namespace MUFPF

/-!
# SpectralFlowDynamicsRG.lean — 谱流方程的尺度动力学（Paper LVII §8.7#5 动力学层第一注入）

§8.6d（`SpectralFlowRG.lean`）把单级自洽倍率 1/r* 分解为两级链
Δλ_min → Δλ_min^(EM) → δ_SC，但 k₂ = r*/√3 是**后验代数倍率**（§8.7#5 所指
"动力学 RG 常演化"仍开放：逐级倍率须由谱流方程重新求解涌现）。本文件对该动力学层
给出**第一注入**——不改变 k₂ 的定义，而把"动力学"内容钉在谱流自洽方程自身的
尺度结构上：

1. **运行反常维度**（anomalous dimension，局部尺度指数）
     ζ(r) = r f'(r)/f(r) = (1 + (3/2)√3·√r)/(1 + √3·√r)
   对任意 r>0 严格落入 (1, 3/2)，且随 r 从 0→+∞ 单调从 1 跑到 3/2。这精确诊断：
   **谱流方程 f 不是标度不变的**（无单一幂律），故"多级常演化"只能是有限两级
   固定倍率因子分解，而非连续重整化流——动力学 RG 层"为何只能是代数骨架"有了
   定量判据。

2. **EM 残差流闭合**（把 k₂ 与谱流方程重新求解挂钩）：
     f_EM(u) := selfConsFunc (√3·u) = √3·u + 3·√√3·u·√u
   是单级自洽方程在规范缩放坐标 u = r/√3 下的"残差流"。定理 `em_residual_closure`
   表明 k₂ 恰使残差流在**同一**闭合常数 c = a_BCS³·4π 处闭合：
     f_EM(k₂) = f(r*) = c。
   即：**BCS 动力学闭合常数 c 在纯规范表示因子 √3 的尺度缩放下保持不变（常演化）**，
   只有坐标被 r* → k₂ = r*/√3 重标度。这与 §8.6d 的折叠 k₁·k₂ = r* 是同一几何事实
   的两种读法，且 `em_residual_root_unique` 保证 k₂ 是 f_EM(u)=c 的唯一正根。

诚实边界（动力学层，延续 §8.6d / §0）：
- 本文件闭合的是**谱流方程的尺度诊断**（运行指数 + 非标度不变）与**规范缩放坐标下的
  残差流重构**。k₂ 仍由共享常数 c 与 r* 的方程唯一根经规范因子 √3 重标度给出。
- **仍开放**：一个*独立*于 r*（带新的物理锚）的 EM 中间级谱流闭合——即让 k₂ 不由
  单一 c 的反向重标度、而由 **EM 尺度自身的独立谱流方程**自洽涌现。这需真正发展
  §8.7#5 所述"跨尺度的谱流方程重整化群方法"，本文件不伪称。
- a_BCS、E_F 仍是物理输入；范畴 Δ 内生的是 Δλ_min、Δλ_min^(EM) 与 r* 的方程唯一性。
-/

/-! ## Section 1: 运行反常维度（局部尺度指数） -/

/-- 谱流自洽函数的局部尺度指数（anomalous dimension）闭式：
    ζ(r) = r f'(r)/f(r) = (1 + (3/2)√3·√r)/(1 + √3·√r)。
    笔算：f = (1+√3√r)r，f' = 1 + (3/2)√3·√r。 -/
noncomputable def anom_dim (r : ℝ) : ℝ :=
  (1 + (3 / 2 : ℝ) * Real.sqrt 3 * Real.sqrt r) /
    (1 + Real.sqrt 3 * Real.sqrt r)

/-- 分母 1 + √3·√r > 0（r>0）。 -/
theorem anom_dim_denom_pos {r : ℝ} (hr : 0 < r) :
    0 < 1 + Real.sqrt 3 * Real.sqrt r := by
  have hsqrt : 0 < Real.sqrt r := Real.sqrt_pos_of_pos hr
  have hx : 0 < Real.sqrt 3 * Real.sqrt r :=
    mul_pos (Real.sqrt_pos_of_pos (by norm_num : (0 : ℝ) < 3)) hsqrt
  linarith

/-- ζ(r) > 1（运行指数下界：清洁谱间隙极限 1）。 -/
theorem anom_dim_gt_one {r : ℝ} (hr : 0 < r) : 1 < anom_dim r := by
  unfold anom_dim
  have hsqrt : 0 < Real.sqrt r := Real.sqrt_pos_of_pos hr
  have hx : 0 < Real.sqrt 3 * Real.sqrt r :=
    mul_pos (Real.sqrt_pos_of_pos (by norm_num : (0 : ℝ) < 3)) hsqrt
  have hd : 0 < 1 + Real.sqrt 3 * Real.sqrt r := by linarith
  rw [lt_div_iff₀ hd]
  ring_nf
  nlinarith [hx]

/-- ζ(r) < 3/2（运行指数上界：强耦合偶参极限 3/2）。 -/
theorem anom_dim_lt_threehalf {r : ℝ} (hr : 0 < r) : anom_dim r < 3 / 2 := by
  unfold anom_dim
  have hd : 0 < 1 + Real.sqrt 3 * Real.sqrt r := anom_dim_denom_pos hr
  rw [div_lt_iff₀ hd]
  nlinarith

/-- 运行指数严格落在 (1, 3/2)（分量式）。 -/
theorem anom_dim_interior {r : ℝ} (hr : 0 < r) :
    1 < anom_dim r ∧ anom_dim r < 3 / 2 :=
  ⟨anom_dim_gt_one hr, anom_dim_lt_threehalf hr⟩

/-! ## Section 2: EM 残差流（规范缩放坐标下的谱流闭合） -/

/-- 电磁中间级坐标 u 下的残差谱流：
    f_EM(u) = selfConsFunc (√3 u) = √3·u + 3·√(√3)·u·√u。
    与单级自洽方程共享同一闭合常数 c，坐标经纯规范因子 √3 缩放。 -/
noncomputable def em_residual_flow (u : ℝ) : ℝ :=
  Real.sqrt 3 * u + 3 * Real.sqrt (Real.sqrt 3) * u * Real.sqrt u

/-- f_EM(u) = f(√3 u)——残差流与单级流在规范缩放坐标下的解析等价。 -/
theorem em_residual_flow_eq_selfCons (u : ℝ) :
    em_residual_flow u = selfConsFunc (Real.sqrt 3 * u) := by
  unfold em_residual_flow selfConsFunc
  rw [Real.sqrt_mul (by norm_num : 0 ≤ (Real.sqrt 3 : ℝ)) u]
  ring_nf
  rw [Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 3)]
  ring

/-- 第 2 级倍率 k₂ > 0。 -/
theorem RG_k2_pos : 0 < RG_k2 := by
  rw [RG_k2_eq]
  exact mul_pos (Real.sqrt_pos_of_pos (by norm_num : (0 : ℝ) < 1 / 3)) r_star_pos

/-- **EM 残差流闭合**：k₂ 使残差流在共享闭合常数 c 处精确闭合——
    f_EM(k₂) = f(r*) = c = a_BCS³·4π。
    "BCS 动力学闭合常数 c 在规范因子 √3 的尺度缩放下保持不变（常演化）"。 -/
theorem em_residual_closure : em_residual_flow RG_k2 = selfConsC := by
  rw [em_residual_flow_eq_selfCons]
  rw [← RG_k1_eq_sqrt3, RG_telescoping, r_star_closure]

/-- 单级自洽的闭合常数 c = f(r*) 在 EM 残差流处重现（RG 常演化，另一表述）。 -/
theorem closed_constant_rg_invariant : selfConsFunc r_star = em_residual_flow RG_k2 := by
  rw [r_star_closure, em_residual_closure]

/-- **k₂ 是残差自洽方程的唯一正根**：对任意 u>0，
    f_EM(u) = c 当且仅当 u = k₂。 -/
theorem em_residual_root_unique :
    ∀ u : ℝ, 0 < u → (em_residual_flow u = selfConsC ↔ u = RG_k2) := by
  intro u hu
  constructor
  · intro hf
    have hf' : selfConsFunc (Real.sqrt 3 * u) = selfConsC := by
      rw [← em_residual_flow_eq_selfCons u]
      exact hf
    have huniq : ∀ y : ℝ, (0 ≤ y ∧ selfConsFunc y = selfConsC) → y = r_star :=
      (Classical.choose_spec (selfConsFunc_existsUnique selfConsC selfConsC_pos)).2
    have hle : 0 ≤ Real.sqrt 3 * u := by positivity
    have hfac : Real.sqrt 3 * u = r_star := huniq (Real.sqrt 3 * u) ⟨hle, hf'⟩
    have hsqrt3 : Real.sqrt 3 ≠ 0 :=
      ne_of_gt (Real.sqrt_pos_of_pos (by norm_num : (0 : ℝ) < 3))
    have hu_eq : u = (Real.sqrt 3)⁻¹ * r_star := by
      rw [← hfac]
      field_simp [hsqrt3, hu.ne']
    have hk : RG_k2 = (Real.sqrt 3)⁻¹ * r_star := by
      rw [RG_k2_eq]
      have hrv : Real.sqrt (1 / 3 : ℝ) = (Real.sqrt 3)⁻¹ := by
        rw [show (1 / 3 : ℝ) = (3 : ℝ)⁻¹ by norm_num]
        rw [Real.sqrt_inv]
      rw [hrv]
    exact hu_eq.trans hk.symm
  · intro heq
    rw [heq]
    exact em_residual_closure

end MUFPF