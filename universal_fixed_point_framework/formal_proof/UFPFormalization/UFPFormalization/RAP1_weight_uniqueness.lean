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
import Mathlib.Data.Nat.Basic

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
  induction' k with k ih
  · -- base case k = 0: w(0) = s^0 = 1
    have h0 : w 0 = 1 := by
      have h0_mul : w 0 = w (0 + 0) := by simp
      have h0_eq : w (0 + 0) = w 0 * w 0 := h_mul 0 0
      have h_pos0 : 0 < w 0 := h_pos 0
      nlinarith
    simpa using h0
  · -- inductive step: w(k+1) = s · w(k) = s · s^k = s^(k+1)
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
  have h1 : ((1 + 1 : ℝ) ^ (-a) : ℝ) = ((1 : ℝ) ^ (-a)) * ((1 : ℝ) ^ (-a)) := h 1 1
  -- left side: 2^(-a); right side: 1 * 1 = 1
  have h_left : ((2 : ℝ) ^ (-a)) = (1 : ℝ) := by
    calc
      ((2 : ℝ) ^ (-a)) = ((1 + 1 : ℝ) ^ (-a)) := by norm_num
      _ = ((1 : ℝ) ^ (-a)) * ((1 : ℝ) ^ (-a)) := h1
      _ = 1 := by norm_num
  have h2a : (2 : ℝ) ^ (-a) = (1 : ℝ) := h_left
  have h2 : (2 : ℝ) ^ (-a) = 1 := h2a
  have h3 : (2 : ℝ) ^ a = 1 := by
    rw [← Real.rpow_inv_eq_iff (by positivity : (2 : ℝ) > 0) (by norm_num : (1 : ℝ) > 0) ha]
    simpa using h2
  -- Only possible when a = 0 (since 2^x = 1 iff x = 0)
  have h4 : a = 0 := by
    have : (2 : ℝ) ^ (a : ℝ) = (1 : ℝ) := by
      simpa using h3
    apply Real.strictMono_rpow_of_base_gt_one (by norm_num : (1 : ℝ) < 2) |>.injective
    simpa using this
  exact ha h4

end UFPFormalization.RAP1
