import Mathlib.Analysis.SpecificLimits.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Topology.MetricSpace.Pseudo.Lemmas
import Mathlib.Logic.Function.Iterate
import MUFPFormalization.CoherenceToBranching
import MUFPFormalization.PublicResidueIdentity

/-!
# 轨道动力学的收缩层与速率通道（S625——2026-11-10）

## 动机

`RecOrbitDynamics.lean`（S624）把动力学的**必然性层**关掉了：
有限观测下可分辨的新状态必有尽头（`exists_visible_repetition`），
但「尽头是否静止」不必然（`swap_not_frozen` 的二循环反例），
故收缩机制仍登记为开口。论文 §3 的候选级段落当时进一步判断
「速率层不可由现有公设内生」——理由是唯一可充当压缩率角色的 σ = 1/15
已在 α 链承担比例语义。

## 本轮查证：该判断不成立

1. 库内 §10b 的 IFS 收缩因子比已是 `c₁⁰ : c₂⁰ : c₃⁰ = S₃S₄ : S₄ : 1`
   （`CoherenceToBranching.silent_factor_c1/c2/c3`），其中 `S₄ = e^{-d}`；
   该文件注释写明 **d = ln 15 为机器证明实例**。
2. 因 `15 = σ⁻¹`，`d = ln 15` 时 `S₄ = e^{-ln 15} = 1/15 = σ`。
3. `PublicResidueIdentity.sigma_eq_S4` 已机检 `σ = S₄`，而 σ 的 15 本身有生成链
   （`SpinorSilenceBranch.S4_eq_inv_two_pow_succ_minus_one`：
   `N_active = 3 → k_max = 8 → 16 = 2·k_max → 15 = 16 − 1`）。

∴ σ 不是「被 α 链占用、不可挪用」的常数，而是**比例 / 谱残差 / 收缩率
三条语义链的同一常数**；收缩率因此可由既有生成链内生，不需要新公设。
本文件把这条链的算术接驳与几何收敛机检下来。

## 结论（八条定理，零 sorry）

1. `exp_neg_log_fifteen`：`e^{-ln 15} = 1/15`——§10b 的 S₄ 与 σ 的算术接驳。
2. `silent_factor_c2_ln15`：`silent_factor_c2 (ln 15) = 1/15`（单重静默收缩因子）。
3. `silent_factor_c1_ln15`：`silent_factor_c1 (ln 15) = e^{-3}/15`（双重静默）。
4. `silent_factor_c2_ln15_eq_sigma`：`silent_factor_c2 (ln 15) = sigma`
   ——收缩率与框架常数 σ 的**机检同一**（不是候选级比对）。
5. `tendsto_sigma_pow_zero`：`σ^n → 0`。
6. `contraction_iterate_bound`：压缩率 c < 1 时迭代以 `c^n` 为界。
7. `contraction_iterate_tendsto`：同条件下迭代收敛到不动点——即
   「周期塌成不动点」在收缩条件下的机制侧。
8. `sigma_rate_contraction`：取 c = σ 的特例，速率就是 `σ^n`。

## 边界（如实标注，不越界）

- 本文件证明的是**条件命题**：给定 `|step x − a| ≤ c|x − a|`，则收敛。
  它不证明「本框架的 `step` 满足该条件」——后者仍需投影/谱投影的有损结构
  给出定量压缩，属**收缩条件本身的来源**，本轮仍为候选级。
- 因此速率层的结论是：**候选值已内生并且机检（σ^n）**，
  但「本框架的 step 是否被该条件覆盖」仍登记为开口。
- 零 sorry。
-/

namespace MUFPF

open Filter
open scoped Topology

/-- `e^{-ln 15} = 1/15`：§10b 静默因子 `S₄ = e^{-d}` 在 `d = ln 15` 处的值
    正是框架常数 σ 的倒数之逆。 -/
theorem exp_neg_log_fifteen : Real.exp (-(Real.log 15)) = (1 / 15 : ℝ) := by
  rw [Real.exp_neg, Real.exp_log (by norm_num : (0 : ℝ) < 15)]
  norm_num

/-- 单重静默收缩因子在 `d = ln 15` 处等于 `1/15`。 -/
theorem silent_factor_c2_ln15 :
    MUFPF.CoherenceToBranching.silent_factor_c2 (Real.log 15) = (1 / 15 : ℝ) := by
  rw [MUFPF.CoherenceToBranching.silent_factor_c2]
  exact exp_neg_log_fifteen

/-- 双重静默收缩因子在 `d = ln 15` 处等于 `e^{-3}/15`。 -/
theorem silent_factor_c1_ln15 :
    MUFPF.CoherenceToBranching.silent_factor_c1 (Real.log 15)
      = Real.exp (-3) * (1 / 15 : ℝ) := by
  rw [MUFPF.CoherenceToBranching.silent_factor_c1]
  rw [exp_neg_log_fifteen]

/-- 收缩率与框架常数 σ 是同一个数：`silent_factor_c2 (ln 15) = sigma`。

    这是把「σ 已在 α 链承担比例语义、不可挪用」这一判断关掉的关键一步——
    两处本就是同一常数的不同语义链。 -/
theorem silent_factor_c2_ln15_eq_sigma :
    MUFPF.CoherenceToBranching.silent_factor_c2 (Real.log 15)
      = MUFPF.PublicResidueIdentity.sigma := by
  rw [silent_factor_c2_ln15, MUFPF.PublicResidueIdentity.sigma_value]

/-- σ 的幂序列几何衰减：`σ^n → 0`。 -/
theorem tendsto_sigma_pow_zero :
    Tendsto (fun n : ℕ => (1 / 15 : ℝ) ^ n) atTop (𝓝 0) :=
  tendsto_pow_atTop_nhds_zero_of_lt_one
    (by norm_num : (0 : ℝ) ≤ 1 / 15)
    (by norm_num : (1 / 15 : ℝ) < 1)

/-- 收缩迭代的几何界：若 `|step x − a| ≤ c|x − a|` 且 `0 ≤ c`，则
    `|step^[n] x − a| ≤ c^n|x − a|`。 -/
theorem contraction_iterate_bound {step : ℝ → ℝ} {a c : ℝ}
    (hc : 0 ≤ c) (hstep : ∀ x : ℝ, |step x - a| ≤ c * |x - a|) :
    ∀ (x : ℝ) (n : ℕ), |step^[n] x - a| ≤ c ^ n * |x - a| := by
  intro x n
  induction n with
  | zero => simp
  | succ k ih =>
      rw [show step^[k + 1] x = step (step^[k] x) from
        Function.iterate_succ_apply' step k x]
      calc
        |step (step^[k] x) - a| ≤ c * |step^[k] x - a| := hstep _
        _ ≤ c * (c ^ k * |x - a|) := mul_le_mul_of_nonneg_left ih hc
        _ = c ^ (k + 1) * |x - a| := by
              rw [pow_succ]
              ring

/-- 收缩迭代收敛到不动点：`0 ≤ c < 1` 且 `|step x − a| ≤ c|x − a|`，则
    `step^[n] x → a`。这是「周期塌成不动点」在收缩条件下的机制侧。 -/
theorem contraction_iterate_tendsto {step : ℝ → ℝ} {a c : ℝ}
    (hc0 : 0 ≤ c) (hc1 : c < 1)
    (hstep : ∀ x : ℝ, |step x - a| ≤ c * |x - a|) (x : ℝ) :
    Tendsto (fun n : ℕ => step^[n] x) atTop (𝓝 a) := by
  have hbound : ∀ n : ℕ, |step^[n] x - a| ≤ c ^ n * |x - a| :=
    fun n => contraction_iterate_bound hc0 hstep x n
  have hpow : Tendsto (fun n : ℕ => c ^ n) atTop (𝓝 0) :=
    tendsto_pow_atTop_nhds_zero_of_lt_one hc0 hc1
  have hg : Tendsto (fun n : ℕ => c ^ n * |x - a|) atTop (𝓝 0) := by
    simpa using hpow.mul_const (|x - a|)
  rw [tendsto_iff_norm_sub_tendsto_zero]
  simpa only [Real.norm_eq_abs] using
    squeeze_zero (fun n => abs_nonneg _) hbound hg

/-- 以 σ 为压缩率：界为 `σ^n`，且迭代收敛到不动点。

    这是速率层的候选级落点——`σ = silent_factor_c2 (ln 15)` 已机检
    （`silent_factor_c2_ln15_eq_sigma`），故速率值内生，不再需要新常数。 -/
theorem sigma_rate_contraction {step : ℝ → ℝ} {a : ℝ}
    (hstep : ∀ x : ℝ, |step x - a| ≤ (1 / 15 : ℝ) * |x - a|) (x : ℝ) :
    (∀ n : ℕ, |step^[n] x - a| ≤ (1 / 15 : ℝ) ^ n * |x - a|)
      ∧ Tendsto (fun n : ℕ => step^[n] x) atTop (𝓝 a) := by
  refine ⟨fun n => contraction_iterate_bound (by norm_num) hstep x n, ?_⟩
  exact contraction_iterate_tendsto (by norm_num) (by norm_num) hstep x

end MUFPF
