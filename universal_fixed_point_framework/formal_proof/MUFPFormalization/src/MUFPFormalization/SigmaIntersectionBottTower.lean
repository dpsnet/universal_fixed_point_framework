/-
  SigmaIntersectionBottTower.lean — σ 交汇封闭定理的 Lean 形式化（Phase 104az-93/95）
  =======================================================

  σ 交汇恒等（104az-91）: N_gen·(k_max−N_gen) = 2^{k_max/2}−1

  定理（交汇封闭，104az-93）：
    交汇方程 N·(2k−N) = 2^k−1 的整数解集 k ∈ {1, 2, 4}
    即 k_max = 2k ∈ {2, 4, 8} = Bott 塔前三层，k_max = 8 为最大解（封闭层）。

  证明路径：
    ① bound 引理：N·(2k−N) ≤ k²（cast 到 ℤ，N(2k−N) = k²−(N−k)²）
    ② 指数引理：k ≥ 5 → k²+1 < 2^k（归纳，辅助引理 2k+2 ≤ 2^k，全程无 Nat 减法）
    ③ 由 ①②：2^k−1 = N(2k−N) ≤ k² 与 k ≥ 5 矛盾 → k ≤ 4
    ④ interval_cases k：k=1,2,4 为解（k=3 无解，k=0 与 N ≥ 1 矛盾）

  先证伪再证明（模式 8）：Python 全枚举 k=1..12, N=1..2k−1 验证
    scripts/_phase104az95_falsify.py（exit 0）——解集 k ∈ {1,2,4}、
    bound 恒成立、k≥5 时 k² < 2^k−1、判别式完全平方 ⟺ k ∈ {1,2,4}。

  状态：定理形式化（精确数学结论——上界/指数论证；框架诠释在 roadmap）
-/

import Mathlib.Tactic

namespace MUFPF.SigmaIntersection

/-! =========================================================
    ① bound 引理：N·(2k−N) ≤ k²
   ========================================================= -/

/-- 对 1 ≤ N < 2k，乘积 N·(2k−N) ≤ k²（等号在 N=k 时成立）。 -/
lemma bound_prod (k N : ℕ) (_hN1 : 1 ≤ N) (hNlt : N < 2 * k) :
    N * (2 * k - N) ≤ k ^ 2 := by
  have hNle : N ≤ 2 * k := le_of_lt hNlt
  -- Nat 目标 cast 到 ℤ：N(2k−N) ↦ ↑N·(2↑k−↑N)
  have hgoal_z : (N * (2 * k - N) : ℤ) ≤ (k ^ 2 : ℤ) := by
    have hcast : (N * (2 * k - N) : ℤ) = (N : ℤ) * (2 * (k : ℤ) - (N : ℤ)) := by
      simp
    rw [hcast]
    -- 恒等: N·(2k−N) = k²−(N−k)²（ℤ 版本）
    have hz : (N : ℤ) * (2 * (k : ℤ) - (N : ℤ)) = (k : ℤ) ^ 2 - ((N : ℤ) - (k : ℤ)) ^ 2 := by
      ring
    nlinarith [hz, sq_nonneg ((N : ℤ) - (k : ℤ))]
  exact_mod_cast hgoal_z

/-! =========================================================
    ② 指数引理：k ≥ 5 → k²+1 < 2^k
   ========================================================= -/

/-- 辅助：k ≥ 1 → 2 ≤ 2^k。 -/
lemma two_le_two_pow (k : ℕ) (hk : 1 ≤ k) : 2 ≤ 2 ^ k := by
  induction k with
  | zero => omega
  | succ k ih =>
      rw [pow_succ]
      have h0 : 0 < 2 ^ k := by positivity
      have hpos : 1 ≤ 2 ^ k := by omega
      nlinarith

/-- 辅助：k ≥ 5 → 2k+2 ≤ 2^k（指数增长超越线性）。 -/
lemma two_mul_add_two_le_two_pow (k : ℕ) (hk : 5 ≤ k) : 2 * k + 2 ≤ 2 ^ k := by
  induction' k with k ih
  · omega
  · by_cases h : k + 1 = 5
    · rw [h]
      norm_num
    · have hk5 : 5 ≤ k := by omega
      have ih' : 2 * k + 2 ≤ 2 ^ k := ih hk5
      have hk1 : 1 ≤ k := by omega
      have htwo : 2 ≤ 2 ^ k := two_le_two_pow k hk1
      calc
        2 * (k + 1) + 2 = 2 * k + 4 := by ring
        _ ≤ 2 ^ k + 2 := by nlinarith [ih']
        _ ≤ 2 * 2 ^ k := by nlinarith [htwo]
        _ = 2 ^ (k + 1) := by
          rw [pow_succ]
          ring

/-- 指数超越平方：k ≥ 5 → k²+1 < 2^k（全程无 Nat 减法）。 -/
lemma sq_add_one_lt_two_pow (k : ℕ) (hk : 5 ≤ k) : k ^ 2 + 1 < 2 ^ k := by
  induction' k with k ih
  · omega
  · by_cases h : k + 1 = 5
    · rw [h]
      norm_num
    · have hk5 : 5 ≤ k := by omega
      have ih' : k ^ 2 + 1 < 2 ^ k := ih hk5
      have hlin : 2 * k + 2 ≤ 2 ^ k := two_mul_add_two_le_two_pow k hk5
      have hlin2 : 2 * k + 1 < 2 ^ k := by nlinarith [hlin]
      calc
        (k + 1) ^ 2 + 1 = k ^ 2 + 2 * k + 2 := by ring
        _ < 2 ^ k + 2 * k + 1 := by nlinarith [ih']
        _ < 2 ^ k + 2 ^ k := by nlinarith [hlin2]
        _ = 2 * 2 ^ k := by ring
        _ = 2 ^ (k + 1) := by
          rw [pow_succ]
          ring

/-! =========================================================
    ③ 主定理：交汇封闭
   ========================================================= -/

/-- σ 交汇方程（k = k_max/2 半指数）的解 k 只能是 1, 2, 4。 -/
theorem sigma_intersection_closed (k N : ℕ) (hN1 : 1 ≤ N) (hNlt : N < 2 * k)
    (hEq : N * (2 * k - N) = 2 ^ k - 1) :
    k = 1 ∨ k = 2 ∨ k = 4 := by
  -- ① N(2k−N) ≤ k² → 2^k−1 ≤ k²
  have hbound : N * (2 * k - N) ≤ k ^ 2 := bound_prod k N hN1 hNlt
  have hle : 2 ^ k - 1 ≤ k ^ 2 := by
    rw [← hEq]
    exact hbound
  -- ② 若 k ≥ 5，则 k²+1 < 2^k（即 k² < 2^k−1），与 hle 矛盾 → k ≤ 4
  have hk_le_4 : k ≤ 4 := by
    by_contra hk4
    have hk5 : 5 ≤ k := by omega
    have hgt : k ^ 2 + 1 < 2 ^ k := sq_add_one_lt_two_pow k hk5
    have hgt' : k ^ 2 < 2 ^ k - 1 := by omega
    nlinarith
  -- ③ 枚举 k ≤ 4
  interval_cases k
  · exfalso
    omega
  · left
    rfl
  · right
    left
    rfl
  · -- k = 3：无 N 满足（interval_cases 利用 hN1 枚举 N=1..5）
    exfalso
    interval_cases N <;> norm_num at hEq
  · right
    right
    rfl

/-! =========================================================
    ④ 解存在性与对偶结构（正面方向）
   ========================================================= -/

/-- (k_max, N_gen) = (2, 1)：1×1 = 2¹−1（自对偶）。 -/
theorem solution_k1 (hN : N = 1) : N * (2 * 1 - N) = 2 ^ 1 - 1 := by
  subst hN
  norm_num

/-- (k_max, N_gen) = (4, 1) 或 (4, 3)：1×3 = 2²−1（对偶对）。 -/
theorem solution_k2 (hN : N = 1 ∨ N = 3) : N * (2 * 2 - N) = 2 ^ 2 - 1 := by
  rcases hN with rfl | rfl <;> norm_num

/-- (k_max, N_gen) = (8, 3) 或 (8, 5)：3×5 = 2⁴−1（对偶对——(3,5) Rec/Sp 分岔互补对）。 -/
theorem solution_k4 (hN : N = 3 ∨ N = 5) : N * (2 * 4 - N) = 2 ^ 4 - 1 := by
  rcases hN with rfl | rfl <;> norm_num

/-- 交汇方程在 k=3（k_max=6）无解——判别式 k²−2^k+1 = 2 非平方。 -/
theorem no_solution_k3 (N : ℕ) (hNlt : N < 2 * 3) :
    ¬ N * (2 * 3 - N) = 2 ^ 3 - 1 := by
  intro hEq
  interval_cases N <;> norm_num at hEq

end MUFPF.SigmaIntersection
