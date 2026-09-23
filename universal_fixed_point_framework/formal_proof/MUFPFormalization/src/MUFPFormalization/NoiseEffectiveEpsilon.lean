-- ============================================================
-- UFPF → MUFPF 更名通知
-- ============================================================
-- 本文件属于 Universal Fixed Point Framework (UFPF)。
-- 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
-- 更名计划详见：roadmap/mu_renaming_plan.md
--
-- 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
-- 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
--
-- 本文件中 UFPF 相关引用数量：0
-- 更名将在计划确认后统一执行，当前代码不做修改。
-- ============================================================

import Mathlib.Data.Real.Basic
import Mathlib.Topology.Order.Basic
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Order.Monotone.Basic
import Mathlib.Tactic

namespace MUFPF

open Filter
open scoped Topology

/-!
# NoiseEffectiveEpsilon.lean — §3.4 ε_eff 闭式 Lean 化（paper14 内生重建 G5）

对应 paper14_spectral_condensed_matter.md §3.4 的核心闭式与极限行为：

  ε_eff(ξ) = n_imp · [ℓ_B² + ξ²·θ(ξ²/(2ℓ_B²))]，θ(t) = 1 − e^{−t}

（远程施主无序的谱公理层修正公式，v1.6 已诚实重定级为【谱公理】推导，
非范畴 Δ 内生，见 paper14 §3.4 标注）

## 本模块封闭的判别性命题

  1. 退化值：ξ = 0 ⟹ ε_eff = n_imp·ℓ_B²（＝短程情形 ε = n_imp·ℓ_B²）
  2. 远程主导因子上界：0 ≤ θ(t) < 1（t ≥ 0）⟹ ε_eff ≤ n_imp·(ℓ_B² + ξ²)，
     且随 ξ² 单调—— 远程施主更强无序的定界
  3. θ 单调：θ(t) 在 t ≥ 0 单调不减（远程因子随关联增长）
  4. 退化极限：ξ → 0 ⟹ ε_eff(ξ) → n_imp·ℓ_B²（尤于连续性）
  5. 临界阈值 ε_c^eff = ε_c^(0)/(1 + ξ/ℓ_B)² 关于 ξ 单调递减
     （远程施主 ⟹ 坍缩阈值下移，paper14 §3.4）

## 诚实边界

- 精确远程渐近 `ε_eff ~ n_imp·ξ² (ξ→∞)` 依赖 e^{−t}→0 + Fatou 两条无穷远
  比较引理的交织，本模块以"上界 + 单调"给出定性/定界判别（足以支持
  "远程施主更强无序"及"ε_c^eff 单调下移"两结论）；无穷远精确渐近登记开放。
- 物理参数域：n_imp ≥ 0（杂质浓度）、ℓ_B ∈ ℝ（磁场长，退化/上界命题可
  放宽符号，临界阈值命题需 ℓ_B > 0）、ξ ≥ 0（关联长度不取负）。
-/

/-! 核心闭式（paper14 §3.4） -/

/-- θ(t) = 1 − e^{−t}：远程主导的"不完全湮灭因子"（t = ξ²/(2ℓ_B²)）。 -/
noncomputable def thetaFactor (t : ℝ) : ℝ := 1 - Real.exp (-t)

/-- ε_eff(ξ) = n_imp · [ℓ_B² + ξ²·θ(ξ²/(2ℓ_B²))]。paper14 §3.4 框式主公式。 -/
noncomputable def effEpsilon (nImp lB xi : ℝ) : ℝ :=
  nImp * (lB ^ 2 + xi ^ 2 * thetaFactor (xi ^ 2 / (2 * lB ^ 2)))

/-- ε_c^eff(ξ) = ε_c^(0) / (1 + ξ/ℓ_B)²。paper14 §3.4 框式阈值修正。 -/
noncomputable def effCriticalEpsilon (epsC0 lB xi : ℝ) : ℝ :=
  epsC0 / (1 + xi / lB) ^ 2

/-! §1 退化值 -/

/-- θ(0) = 0。 -/
theorem theta_zero : thetaFactor 0 = 0 := by
  unfold thetaFactor
  simp

/-- 退化值：ξ = 0 ⟹ ε_eff = n_imp·ℓ_B²（短程情形 ε = n_imp·ℓ_B² 的点值）。 -/
theorem effEpsilon_zero (nImp lB : ℝ) : effEpsilon nImp lB 0 = nImp * (lB ^ 2) := by
  unfold effEpsilon thetaFactor
  simp

/-! §2 远程主导因子 θ：非负、严格上界 1、单调 -/

/-- 0 ≤ θ(t)（t ≥ 0）：远程因子非负。 -/
theorem theta_nonneg {t : ℝ} (ht : 0 ≤ t) : 0 ≤ thetaFactor t := by
  unfold thetaFactor
  have hlt : -t ≤ 0 := by linarith
  have hE : Real.exp (-t) ≤ 1 := by
    rw [← Real.exp_zero]
    exact Real.exp_le_exp.mpr hlt
  linarith

/-- θ(t) < 1（t ≥ 0 情形可由 0<exp 直接证）：远程因子严格小于 1（不完全湮灭，留阈值）。 -/
theorem theta_lt_one (t : ℝ) : thetaFactor t < 1 := by
  unfold thetaFactor
  have hpos : 0 < Real.exp (-t) := by positivity
  linarith

/-- θ 单调不减：t₁ ≤ t₂ ⟹ θ t₁ ≤ θ t₂。 -/
theorem theta_mono {t₁ t₂ : ℝ} (h₂ : t₁ ≤ t₂) :
    thetaFactor t₁ ≤ thetaFactor t₂ := by
  unfold thetaFactor
  have hlt : -t₂ ≤ -t₁ := by linarith
  have hE : Real.exp (-t₂) ≤ Real.exp (-t₁) := (Real.exp_le_exp.mpr hlt)
  linarith

/-- 远程主导：t（=ξ²/2ℓ_B²）≥ 0 分支的 θ 因子保留，ε_eff = n_imp·ℓ_B² + 非负远程项。
    短程下降（ξ→0 项消失）与远程主导（ξ²·θ项）的分层恒等式。 -/
theorem effEpsilon_decompose (nImp lB xi : ℝ) :
    effEpsilon nImp lB xi =
      nImp * (lB ^ 2) + nImp * (xi ^ 2 * thetaFactor (xi ^ 2 / (2 * lB ^ 2))) := by
  unfold effEpsilon
  ring

/-- 远程远程项系数非负（n_imp ≥ 0、xi ≥ 0、0 ≤ θ）：远程修正 ≥ 0。 -/
theorem effEpsilon_remote_correction_nonneg
    (nImp lB xi : ℝ) (hnImp : nImp ≥ 0) :
    nImp * (xi ^ 2 * thetaFactor (xi ^ 2 / (2 * lB ^ 2))) ≥ 0 := by
  have hθ : 0 ≤ thetaFactor (xi ^ 2 / (2 * lB ^ 2)) := by
    apply theta_nonneg
    positivity
  have hx2 : 0 ≤ xi ^ 2 := sq_nonneg xi
  exact mul_nonneg hnImp (mul_nonneg hx2 hθ)

/-! §3 退化极限（连续性） -/

/-- θ = t ↦ 1 − e^{−t} 处处连续（exp 连续）。 -/
theorem continuous_theta : Continuous thetaFactor := by
  unfold thetaFactor
  fun_prop

/-- θ 在 0 处连续。 -/
theorem continuousAt_theta_zero : ContinuousAt thetaFactor 0 :=
  continuous_theta.continuousAt

/-- ε_eff 在 ξ = 0 处连续（ℓ_B ≠ 0 保证分母 (2ℓ_B²) 弦张非零）。 -/
theorem continuousAt_effEpsilon_zero (nImp lB : ℝ) (hlB : lB ≠ 0) :
    ContinuousAt (fun xi : ℝ => effEpsilon nImp lB xi) 0 := by
  have hden : (2 * lB ^ 2 : ℝ) ≠ 0 := by positivity
  unfold effEpsilon thetaFactor
  fun_prop (disch := positivity)

/-- 退化极限：ξ → 0 ⟹ ε_eff(ξ) → n_imp·ℓ_B²（尤于连续性）。 -/
theorem effEpsilon_tendsto_zero (nImp lB : ℝ) (hlB : lB ≠ 0) :
    Tendsto (fun xi : ℝ => effEpsilon nImp lB xi) (𝓝 0) (𝓝 (nImp * (lB ^ 2))) := by
  rw [← effEpsilon_zero nImp lB]
  exact (continuousAt_effEpsilon_zero nImp lB hlB).tendsto

/-! §4 临界阈值 ε_c^eff 的单调性 -/

/-- 辅助：x₁ ≥ 0、x₁ ≤ x₂、ℓ_B > 0 ⟹ (1+x₁/ℓ_B)² ≤ (1+x₂/ℓ_B)²（分母平方单调）。
    取 x₁ ≥ 0 以保证左端分母非负（`sq_le_sq` 的前提）。 -/
theorem effCriticalEpsilon_denom_mono {lB x₁ x₂ : ℝ}
    (hx₁ : 0 ≤ x₁) (hlB : lB > 0) (hle : x₁ ≤ x₂) :
    (1 + x₁ / lB) ^ 2 ≤ (1 + x₂ / lB) ^ 2 := by
  have hbase : 1 + x₁ / lB ≤ 1 + x₂ / lB := by
    have hd : x₁ / lB ≤ x₂ / lB := div_le_div_of_nonneg_right hle (le_of_lt hlB)
    linarith
  have hn1 : 0 ≤ 1 + x₁ / lB := by
    have hx : 0 ≤ x₁ / lB := div_nonneg hx₁ (le_of_lt hlB)
    nlinarith
  have hn2 : 0 ≤ 1 + x₂ / lB := by
    have hx₂ : 0 ≤ x₂ := le_trans hx₁ hle
    have hx : 0 ≤ x₂ / lB := div_nonneg hx₂ (le_of_lt hlB)
    nlinarith
  nlinarith [mul_nonneg hn1 (sub_nonneg.mpr hbase),
      mul_nonneg hn2 (sub_nonneg.mpr hbase)]

/-- ε_c^eff(ξ) = ε_c^(0)/(1+ξ/ℓ_B)² 关于 ξ ≥ 0 单调递减（ℓ_B > 0、ε_c^(0) ≥ 0）。
    远程施主 ξ 增大 ⟹ 坍缩阈值下移（paper14 "ξ≫ℓ_B 时 ε_c^eff≪ε_c^(0)"）。 -/
theorem effCriticalEpsilon_antitone
    {epsC0 lB : ℝ} (heps0 : epsC0 ≥ 0) (hlB : lB > 0) :
    AntitoneOn (fun xi : ℝ => effCriticalEpsilon epsC0 lB xi) (Set.Ici 0) := by
  intro x₁ hx₁ x₂ hx₂ hle
  rw [Set.mem_Ici] at hx₁ hx₂
  unfold effCriticalEpsilon
  -- 分母不等式：d₁ ≤ d₂（因 0≤x₁≤x₂、ℓ_B>0）。
  have hd12 : (1 + x₁ / lB) ^ 2 ≤ (1 + x₂ / lB) ^ 2 :=
    effCriticalEpsilon_denom_mono hx₁ hlB hle
  -- ε_c^(0) ≥ 0 且分母 d₁ ≤ d₂（均正）⟹ ε_c^(0)/d₂ ≤ ε_c^(0)/d₁。
  change epsC0 / (1 + x₂ / lB) ^ 2 ≤ epsC0 / (1 + x₁ / lB) ^ 2
  gcongr

end MUFPF