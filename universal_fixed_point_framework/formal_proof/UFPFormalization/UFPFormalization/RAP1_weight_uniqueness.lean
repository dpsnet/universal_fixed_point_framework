/-
RAP-1: 定理 R1 — 加权严格 n-范畴权重函数的唯一性
=====================================================

定理陈述（定理 R1，RAP 修复方案 §2）：
  设 (C,w) 为加权严格 n-范畴。权重函数 w: {1,…,n} → (0,1]
  满足：
    (W1) 权重只依赖层级 k ∈ {1,…,n}
    (W2) 复合乘性：w_{k+l} = w_k · w_l
    (W3) 归一化：w_1 = s ∈ (0,1]
  则权重函数恰为单参数指数族 w_k = s^k。

证明：
  由 (W1)–(W2)，k → w_k 满足正整数上的 Cauchy 指数函数方程
    w(k+l) = w(k)·w(l)  且 w(1) = s
  由归纳法得 w(k) = s^k。
  反之，任何非指数形式（k^{-a}、1/(1+k) 等）必然违反 (W2)。

本文件形式化该定理的 ℕ → ℝ 版本。
-/

import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Log.Basic

open Real

namespace UFPFormalization.RAP1

/-!
### 加权严格 n-范畴的权重族唯一性

设 w : ℕ → ℝ 满足：
  (1) w(k+l) = w(k) · w(l) 对任意 k,l ∈ ℕ 成立（复合乘性）
  (2) w(1) = s ∈ (0, 1]
则 w(k) = s^k 对任意 k ∈ ℕ 成立。
-/

/-- 满足 Cauchy 指数方程 w(k+l) = w(k)·w(l) 的函数。
    本定义仅要求 ℕ 上的乘性同态性质。 -/
structure CauchyExponential (w : ℕ → ℝ) : Prop where
  h_mul : ∀ k l, w (k + l) = w k * w l
  h_pos : ∀ k, 0 < w k
  h_le_one : ∀ k, w k ≤ 1

theorem weight_uniqueness (w : ℕ → ℝ) (s : ℝ) (h_cauchy : CauchyExponential w)
    (h_s : w 1 = s) : ∀ k : ℕ, w k = s ^ k := by
  rcases h_cauchy with ⟨h_mul, h_pos, h_le_one⟩
  intro k
  induction k with
  | zero =>
      -- base case k = 0: w(0) = s^0 = 1
      have h0 : w 0 = 1 := by
        have h0_mul : w 0 = w (0 + 0) := by simp
        have h0_eq : w (0 + 0) = w 0 * w 0 := h_mul 0 0
        have h_pos0 : 0 < w 0 := h_pos 0
        nlinarith
      simpa using h0
  | succ k ih =>
      -- inductive step: w(k+1) = s · w(k) = s · s^k = s^(k+1)
      have h_succ : w (k + 1) = w 1 * w k := by
        simpa [add_comm] using h_mul 1 k
      calc
        w (k + 1) = w 1 * w k := h_succ
        _ = s * w k := by rw [h_s]
        _ = s * (s ^ k) := by rw [ih]
        _ = s ^ (k + 1) := by ring

/-- 任何非指数形式（以 k^{-a} 为例）必然违反复合乘性。 -/
theorem nonexponential_violates_multiplicativity (a : ℝ) (ha : a ≠ 0) :
    ¬ (∀ (k l : ℕ), ((k + l : ℝ) ^ (-a) : ℝ) = ((k : ℝ) ^ (-a)) * ((l : ℝ) ^ (-a))) := by
  intro h
  have h11 := h 1 1
  -- h11: (2 : ℝ) ^ (-a) = (1 : ℝ) ^ (-a) * (1 : ℝ) ^ (-a)
  -- But (1 : ℝ) ^ any = 1, so RHS = 1
  have h2 : (2 : ℝ) ^ (-a) = 1 := by
    have h_same_base : (2 : ℝ) = (1 + 1 : ℝ) := by norm_num
    have h11' : ((1 + 1 : ℝ) ^ (-a) : ℝ) = ((1 : ℝ) ^ (-a)) * ((1 : ℝ) ^ (-a)) := by
      simpa using h 1 1
    calc
      (2 : ℝ) ^ (-a) = ((1 + 1 : ℝ) ^ (-a) : ℝ) := by rw [h_same_base]
      _ = ((1 : ℝ) ^ (-a)) * ((1 : ℝ) ^ (-a)) := h11'
      _ = 1 := by simp
  -- From 2^(-a) = 1, take log: (-a) * ln 2 = 0 ⇒ a = 0 (since ln 2 > 0)
  have h_ln2_pos : Real.log (2 : ℝ) > 0 := Real.log_pos (by norm_num : (1 : ℝ) < 2)
  have h_log_2_ne_zero : Real.log (2 : ℝ) ≠ 0 := by linarith
  have h_mul_zero : (-a) * Real.log (2 : ℝ) = 0 := by
    calc
      (-a) * Real.log (2 : ℝ) = Real.log ((2 : ℝ) ^ (-a)) := by
        rw [Real.log_rpow (by norm_num : (0 : ℝ) < 2)]
      _ = Real.log 1 := by rw [h2]
      _ = 0 := Real.log_one
  rcases mul_eq_zero.mp h_mul_zero with (h_neg_a_zero | h_log_zero)
  · -- case -a = 0
    have ha0 : a = 0 := by linarith
    exact ha ha0
  · -- case Real.log 2 = 0, contradiction
    exact h_log_2_ne_zero h_log_zero

end UFPFormalization.RAP1
