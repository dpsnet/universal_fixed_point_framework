/-
# MersennePellUniqueness.lean — Mersenne-Pell 唯一性（Phase 104az-128 形式化）

形式化目标：(2^n−1)² − n·2^(2n−2) = 1 的唯一自然数解 n ∈ {2, 3}（128）。
  n=2 解 (3, 2) = (N_gen, 幂基)——x²−2y² = 1 最小非平凡解（D = 幂基 = 2）
  n=3 解 (7, 4) = (对合域, 不动点)——x²−3y² = 1 第二非平凡解（D = N_gen = 3）
  —— {幂基, N_gen} 既是方程 n 值也是 D 值（框架常数自指生成）

证明策略：
  ← 方向：n=2 ∨ n=3 代入 norm_num。
  → 方向：n ≤ 3 直接 case 检查；n ≥ 4 时证明 n·2^(2n−2) > (2^n−1)²
    （放缩链：(2^n−1)² < 2^(2n) ≤ n·2^(2n−2)，n≥4）
    → ℕ 饱和减法 = 0 ≠ 1，矛盾。

数值先证伪记录（先证伪再证明，模式 8）：
  - p104az130_pre.py：n=0..12 穷举唯一解集 {2,3} + 6/6 随机抽样通过、残差 0。
-/

import Mathlib.Tactic

namespace MUFPF.MersennePellUniqueness

/-! 引理：1 ≤ 2^n（pow_pos：0 < 2^n ⟹ 1 ≤ 2^n）。 -/
lemma one_le_two_pow (n : ℕ) : 1 ≤ 2 ^ n := by
  have hpos : 0 < 2 ^ n := pow_pos (by norm_num : (0 : ℕ) < 2) n
  omega

/-! 引理：平方严格单调（Nat）：a < b → a² < b²。
    避免 Nat 饱和减法：用 a+1 ≤ b + 平方差分解（纯多项式）。 -/
lemma sq_strict_mono {a b : ℕ} (hab : a < b) : a ^ 2 < b ^ 2 := by
  have hb : a + 1 ≤ b := by omega
  have hsq1 : a ^ 2 < (a + 1) ^ 2 := by
    nlinarith [sq_nonneg a]
  have hsq2 : (a + 1) ^ 2 ≤ b ^ 2 := by
    rcases Nat.exists_eq_add_of_le hb with ⟨k, rfl⟩
    nlinarith [sq_nonneg k, sq_nonneg (a + 1)]
  exact lt_of_lt_of_le hsq1 hsq2

/-! 引理：(2^n)² = 2^(2n)。 -/
lemma sq_two_pow (n : ℕ) : (2 ^ n) ^ 2 = 2 ^ (2 * n) := by
  calc
    (2 ^ n) ^ 2 = 2 ^ (n * 2) := by rw [pow_mul]
    _ = 2 ^ (2 * n) := by congr 1; omega

/-! 引理：n ≥ 1 时 2^(2n) = 4·2^(2n−2)。 -/
lemma four_mul_two_pow (n : ℕ) (_hn : 1 ≤ n) : 2 ^ (2 * n) = 4 * 2 ^ (2 * n - 2) := by
  calc
    2 ^ (2 * n) = 2 ^ (2 + (2 * n - 2)) := by congr 1; omega
    _ = 2 ^ 2 * 2 ^ (2 * n - 2) := by rw [pow_add]
    _ = 4 * 2 ^ (2 * n - 2) := by norm_num

/-! 引理：n ≥ 4 时 (2^n−1)² < 2^(2n)。
    放缩：2^n−1 < 2^n（Nat.sub_lt）→ 平方严格单调 → (2^n−1)² < (2^n)² = 2^(2n)。 -/
lemma sq_lt_two_pow (n : ℕ) (_hn : 4 ≤ n) : (2 ^ n - 1) ^ 2 < 2 ^ (2 * n) := by
  have hpos : 0 < 2 ^ n := pow_pos (by norm_num : (0 : ℕ) < 2) n
  have hsub : 2 ^ n - 1 < 2 ^ n := Nat.sub_lt hpos (by norm_num)
  have hlt : (2 ^ n - 1) ^ 2 < (2 ^ n) ^ 2 := sq_strict_mono hsub
  calc
    (2 ^ n - 1) ^ 2 < (2 ^ n) ^ 2 := hlt
    _ = 2 ^ (2 * n) := sq_two_pow n

/-! 引理：n ≥ 4 时 2^(2n) ≤ n·2^(2n−2)。
    放缩：2^(2n) = 4·2^(2n−2) ≤ n·2^(2n−2)（n ≥ 4）。 -/
lemma n_mul_ge_two_pow (n : ℕ) (hn : 4 ≤ n) : 2 ^ (2 * n) ≤ n * 2 ^ (2 * n - 2) := by
  have h4 : 2 ^ (2 * n) = 4 * 2 ^ (2 * n - 2) := four_mul_two_pow n (by omega)
  have hx : 0 ≤ 2 ^ (2 * n - 2) := Nat.zero_le _
  rw [h4]
  nlinarith [hn, hx]

/-! 引理：n ≥ 4 时 n·2^(2n−2) > (2^n−1)²（主放缩链）。 -/
lemma n_mul_gt_sq (n : ℕ) (hn : 4 ≤ n) : n * 2 ^ (2 * n - 2) > (2 ^ n - 1) ^ 2 := by
  have h1 : (2 ^ n - 1) ^ 2 < 2 ^ (2 * n) := sq_lt_two_pow n hn
  have h2 : 2 ^ (2 * n) ≤ n * 2 ^ (2 * n - 2) := n_mul_ge_two_pow n hn
  exact lt_of_lt_of_le h1 h2

/-! ★★★ 主定理：Mersenne-Pell 唯一性——(2^n−1)² − n·2^(2n−2) = 1 ⟺ n = 2 ∨ n = 3。 -/
theorem mersenne_pell_uniqueness (n : ℕ) :
    (2 ^ n - 1) ^ 2 - n * 2 ^ (2 * n - 2) = 1 ↔ n = 2 ∨ n = 3 := by
  constructor
  · intro h
    by_cases h3 : n ≤ 3
    · interval_cases n <;> norm_num at h <;> omega
    · have h4 : 4 ≤ n := by omega
      have hbig : n * 2 ^ (2 * n - 2) > (2 ^ n - 1) ^ 2 := n_mul_gt_sq n h4
      have hsat : (2 ^ n - 1) ^ 2 - n * 2 ^ (2 * n - 2) = 0 := by
        exact Nat.sub_eq_zero_of_le (le_of_lt hbig)
      rw [hsat] at h
      norm_num at h
  · intro h
    rcases h with h2 | h3
    · subst n
      norm_num
    · subst n
      norm_num

end MUFPF.MersennePellUniqueness
