/-
RAP-2: 命题 R2 — Moran 方程非刚性
=====================================

定理陈述（命题 R2，RAP 修复方案 §3）：
  设 IFS 收缩比为 r_i(d) = {S₃S₄, S₄, 1}（即原框架的 S₃S₄:S₄:1）。
  则对每个 d > 0，存在唯一标度因子 k(d) = (∑ r_i(d)^d)^{-1/d}
  使 ∑ (k(d)·r_i(d))^d = 1 成立。

证明：
  f(k) = ∑ (k·r_i)^d = k^d·∑ r_i^d。令 S = ∑ r_i^d。
  f(k) = 1 ⇔ k^d·S = 1 ⇔ k = S^{-1/d}。显式解给出存在性，
  严格单调性保证唯一性。

推论：Moran 方程对 d_H 不构成任何约束。
-/

import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real

open Real

namespace UFPFormalization.RAP2

/-!
### Moran 方程非刚性

对任意 d > 0 和任意有限正数列 r_i > 0，
方程 ∑ (k·r_i)^d = 1 存在唯一正解 k = (∑ r_i^d)^{-1/d}。
-/

/-- 给定收缩比 r: Fin n → ℝ₊ 和 d > 0，Moran 方程 ∑ (k·r_i)^d = 1 有唯一正解 k。 -/
theorem moran_nonrigidity {n : ℕ} (r : Fin n → ℝ) (hr : ∀ i, 0 < r i) (d : ℝ) (hd : 0 < d) :
    ∃! k : ℝ, 0 < k ∧ ∑ i : Fin n, (k * r i) ^ d = 1 := by
  -- 定义总和 S = ∑ r_i^d
  set S := ∑ i : Fin n, (r i) ^ d with hS_def
  have hSpos : 0 < S := by
    apply Finset.sum_pos
    intro i hi
    exact Real.rpow_pos_of_pos (hr i) d
  have hSpos' : S ≠ 0 := by linarith

  -- 显式解：k₀ = S^{-1/d}
  set k₀ := S ^ (-1 / d) with hk₀_def
  have hk₀_pos : 0 < k₀ := Real.rpow_pos_of_pos hSpos (-1 / d)

  -- 验证 k₀ 满足方程
  have hk₀_solves : ∑ i : Fin n, (k₀ * r i) ^ d = 1 := by
    calc
      ∑ i : Fin n, (k₀ * r i) ^ d = ∑ i : Fin n, (k₀ ^ d) * ((r i) ^ d) := by
        refine Finset.sum_congr rfl fun i hi => ?_
        simp [Real.mul_rpow (by positivity : 0 ≤ k₀) (by positivity : 0 ≤ r i)]
      _ = k₀ ^ d * ∑ i : Fin n, (r i) ^ d := by simp [Finset.mul_sum]
      _ = k₀ ^ d * S := rfl
      _ = (S ^ (-1 / d)) ^ d * S := rfl
      _ = S ^ ((-1 / d) * d) * S := by
        rw [Real.rpow_mul (show (0 : ℝ) ≤ S from by positivity) (-1 / d) d]
      _ = S ^ (-1) * S := by ring
      _ = (1 / S) * S := by rw [Real.rpow_neg (show (0 : ℝ) ≤ S from by positivity), Real.rpow_one]
      _ = 1 := by field_simp [hSpos']

  -- 定义 Moran 函数 f(k) = ∑ (k·r_i)^d
  set f := fun (k : ℝ) => ∑ i : Fin n, (k * r i) ^ d with hf_def

  -- 引理：f(k) = k^d·S
  have hf_eq : ∀ (k : ℝ), f k = k ^ d * S := by
    intro k
    calc
      f k = ∑ i : Fin n, (k * r i) ^ d := rfl
      _ = ∑ i : Fin n, (k ^ d) * ((r i) ^ d) := by
        refine Finset.sum_congr rfl fun i hi => ?_
        simp [Real.mul_rpow (by
          by_cases hk_nonneg : 0 ≤ k
          · exact hk_nonneg
          · nlinarith
        ) (by positivity : 0 ≤ r i)]
      _ = k ^ d * ∑ i : Fin n, (r i) ^ d := by simp [Finset.mul_sum]
      _ = k ^ d * S := rfl

  -- f 在正数上严格递增
  have hf_strictMono : ∀ (x y : ℝ), 0 < x → x < y → f x < f y := by
    intro x y hxpos hxy
    rw [hf_eq x, hf_eq y]
    have hxpos' : 0 < x := hxpos
    have hypos' : 0 < y := by linarith
    have hpow : x ^ d < y ^ d := Real.rpow_lt_rpow_of_exponent_pos hxpos' hxy hd
    nlinarith [hSpos]

  -- 存在性：k₀ 是正解
  have h_exists : 0 < k₀ ∧ f k₀ = 1 := by
    constructor
    · exact hk₀_pos
    · rw [hf_eq k₀]
      calc
        k₀ ^ d * S = (S ^ (-1 / d)) ^ d * S := rfl
        _ = S ^ ((-1 / d) * d) * S := by
          rw [Real.rpow_mul (show (0 : ℝ) ≤ S from by positivity) (-1 / d) d]
        _ = S ^ (-1) * S := by ring
        _ = (1 / S) * S := by rw [Real.rpow_neg (show (0 : ℝ) ≤ S from by positivity), Real.rpow_one]
        _ = 1 := by field_simp [hSpos']

  -- 唯一性：若 k' 也是正解，由严格单调性 k' = k₀
  have h_unique : ∀ (k' : ℝ), (0 < k' ∧ f k' = 1) → k' = k₀ := by
    intro k' ⟨hk'_pos, hk'_val⟩
    by_contra! h_ne
    by_cases h_lt : k' < k₀
    · have : f k' < f k₀ := hf_strictMono k' k₀ hk'_pos h_lt
      rw [hk'_val, h_exists.2] at this
      linarith
    · have h_gt : k₀ < k' := by
        by_contra! h_not_gt
        nlinarith
      have : f k₀ < f k' := hf_strictMono k₀ k' hk₀_pos h_gt
      rw [h_exists.2, hk'_val] at this
      linarith

  -- 汇总
  exact ⟨k₀, h_exists, h_unique⟩

end UFPFormalization.RAP2
