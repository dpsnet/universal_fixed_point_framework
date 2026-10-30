/-
# KMaxTwoPowerUnique.lean — k_max=8 的平方差涌现路径机器证明（Phase 104az-133）

判别结论（133）：k_max = 8 = N_gen² − 1（3²−1=8）——k_max 第二涌现路径。
主定理：n²−1 = 2^m 的唯一整数解 (n,m) = (3,3)。
证明路线：n 奇（n 偶 → n²−1 奇 → m=0 → n²=2 矛盾）；n=3 case 验证 m=3；
n≥5 奇 → n=2k+1、k≥2 → 4k(k+1)=2^m → k | 2^m 且 k+1 | 2^m
→ （2 的素幂因数引理）k=2^a、k+1=2^b → 2^b=2^a+1 → a=0 → k=1 矛盾。

双涌现路径（3↔8 绑定）：
  路径 A：2^m = 2m+2 唯一解 m=3（263/266 机器证明 power_unique）
  路径 B：n²−1 = 2^m 唯一解 (n,m)=(3,3)（本模块）
  迭代平方差链 f(x)=x²−1：f(幂基)=N_gen、f(N_gen)=k_max。

数值先证伪（_phase104az133_kmax_two_power.py）：Q1 n=2..200 唯一命中 n=3、
Q2 (n−1)(n+1) 两因子 2 幂唯一 (2,4)、Q4 两路径唯一——全 PASS。
-/

import Mathlib.Tactic

namespace MUFPF.KMaxTwoPower

def kMax : ℕ := 8
def nGen : ℕ := 3
def powerBase : ℕ := 2

/-! 迭代平方差链：f(幂基)=N_gen、f(N_gen)=k_max（f(x)=x²−1）。 -/
theorem iter_sq_minus_one_chain :
    powerBase ^ 2 - 1 = nGen ∧ nGen ^ 2 - 1 = kMax := by
  constructor
  · norm_num [powerBase, nGen]
  · norm_num [nGen, kMax]

/-! 框架量平方差全落框架结构表（无一野值）。 -/
theorem sq_minus_one_frame_table :
    powerBase ^ 2 - 1 = nGen ∧
    nGen ^ 2 - 1 = kMax ∧
    4 ^ 2 - 1 = 5 * nGen ∧          -- 15 = 静默×N_gen（差 1 链首段）
    7 ^ 2 - 1 = 48 ∧                -- 差 1 链中段
    8 ^ 2 - 1 = 7 * nGen ^ 2 := by  -- 63 = 对合域×N_gen²（商闭包）
  constructor
  · norm_num [powerBase, nGen]
  constructor
  · norm_num [nGen, kMax]
  constructor
  · norm_num [nGen]
  constructor
  · norm_num
  · norm_num [nGen]

/-! 引理：2^b = 2^a + 1 的唯一解 a=0（连续 2 幂差 1）。 -/
lemma pow_two_diff_one (a b : ℕ) (h : 2 ^ b = 2 ^ a + 1) : a = 0 := by
  by_contra ha0
  have ha1 : 1 ≤ a := Nat.succ_le_of_lt (Nat.pos_of_ne_zero ha0)
  -- 2^a < 2^b → a < b
  have hlt_pow : 2 ^ a < 2 ^ b := by
    rw [h]
    exact Nat.lt_succ_self (2 ^ a)
  have hlt : a < b := by
    exact (pow_lt_pow_iff_right₀ (by norm_num : 1 < 2)).mp hlt_pow
  -- 2^a | 2^b → 2^a | 2^a + 1 → 2^a | 1
  have h2a_dvd : 2 ^ a ∣ 2 ^ b := pow_dvd_pow 2 (le_of_lt hlt)
  have h2a_dvd1 : 2 ^ a ∣ 1 := by
    rw [h] at h2a_dvd
    have htmp : 2 ^ a ∣ 1 + 2 ^ a := by
      simpa [Nat.add_comm] using h2a_dvd
    exact (Nat.dvd_add_self_right (m := 2 ^ a) (n := 1)).mp htmp
  have h2a_eq1 : 2 ^ a = 1 := Nat.dvd_one.mp h2a_dvd1
  have : 2 ≤ 2 ^ a := by
    have hlt2 : 1 < 2 ^ a := pow_lt_pow_right₀ (by norm_num : 1 < 2) (by omega : 0 < a)
    omega
  omega

/-! ★★★ 主定理：n²−1 = 2^m 且 2≤n ⟹ (n,m) = (3,3)。 -/
theorem kmax_two_power_unique (n m : ℕ) (h : n ^ 2 - 1 = 2 ^ m) (hn2 : 2 ≤ n) :
    n = 3 ∧ m = 3 := by
  -- n ≠ 2（n=2 → 3=2^m → 2^m 偶性与 3 矛盾）
  have hn_ne2 : n ≠ 2 := by
    intro h2
    subst h2
    by_cases hm0 : m = 0
    · subst hm0
      norm_num at h
    · have hmge1 : 1 ≤ m := Nat.succ_le_of_lt (Nat.pos_of_ne_zero hm0)
      have hmod0 : 2 ^ m % 2 = 0 := by
        rcases Nat.exists_eq_succ_of_ne_zero hm0 with ⟨k, rfl⟩
        rw [pow_succ]
        omega
      have hmod3 : 3 % 2 = 0 := by
        rw [← h] at hmod0
        exact hmod0
      norm_num at hmod3
  -- n 奇（n 偶 → n²−1 奇 → m=0 → n²=2 矛盾）
  have hn_odd : n % 2 = 1 := by
    by_contra hc
    have hn_even : n % 2 = 0 := by omega
    have hn2_mod0 : n ^ 2 % 2 = 0 := by
      rw [Nat.pow_mod]
      simp [hn_even]
    have h1le : 1 ≤ n ^ 2 := by nlinarith [hn2]
    have hn2_odd : (n ^ 2 - 1) % 2 = 1 := by omega
    have hpow_odd : (2 ^ m) % 2 = 1 := by
      rw [← h]
      exact hn2_odd
    have hm0 : m = 0 := by
      by_contra hm0c
      have hmge1 : 1 ≤ m := Nat.succ_le_of_lt (Nat.pos_of_ne_zero hm0c)
      have : (2 ^ m) % 2 = 0 := by
        rcases Nat.exists_eq_succ_of_ne_zero hm0c with ⟨k, rfl⟩
        rw [pow_succ]
        omega
      omega
    have hn2_eq2 : n ^ 2 = 2 := by
      rw [hm0] at h
      omega
    have : 4 ≤ n ^ 2 := by nlinarith [hn2]
    omega
  -- n = 3 case
  by_cases hn3 : n = 3
  · subst hn3
    have hpow8 : 2 ^ m = 8 := by
      norm_num at h
      omega
    have hm3 : m = 3 := by
      by_contra hmc
      by_cases hlt : m < 3
      · interval_cases m <;> norm_num at hpow8
      · have hmgt3 : 3 < m := by omega
        have : 8 < 2 ^ m := pow_lt_pow_right₀ (by norm_num : 1 < 2) hmgt3
        omega
    exact ⟨rfl, hm3⟩
  -- n ≥ 5 奇 → n=2k+1、k≥2 → 4k(k+1)=2^m → 矛盾
  · have hn5 : 5 ≤ n := by omega
    -- n 奇 → ∃k, n=2k+1（Nat.odd_iff）
    have hn_odd' : Odd n := (Nat.odd_iff).2 hn_odd
    rcases hn_odd' with ⟨k, hn_k⟩
    have hk_ge2 : 2 ≤ k := by omega
    -- 4k(k+1) = 2^m
    have hsub : n ^ 2 - 1 = 4 * (k * (k + 1)) := by
      rw [hn_k]
      have hring : (2 * k + 1) ^ 2 = 4 * (k * (k + 1)) + 1 := by ring
      have h1le : 1 ≤ (2 * k + 1) ^ 2 := by
        have hx : 1 ≤ 2 * k + 1 := by omega
        simpa using pow_le_pow_right₀ hx (by norm_num : 0 ≤ 2)
      rw [Nat.sub_eq_iff_eq_add h1le]
      exact hring
    have h4 : 4 * (k * (k + 1)) = 2 ^ m := by
      rw [← hsub]
      exact h
    -- k | 2^m 且 k+1 | 2^m
    have hkdvd : k ∣ 2 ^ m := by
      rw [← h4]
      exact ⟨4 * (k + 1), by ring⟩
    have hk1dvd : k + 1 ∣ 2 ^ m := by
      rw [← h4]
      exact ⟨4 * k, by ring⟩
    -- 素幂因数引理：k=2^ea、k+1=2^eb
    rcases (Nat.dvd_prime_pow (by norm_num : Nat.Prime 2)).mp hkdvd with ⟨ea, hea, hkea⟩
    rcases (Nat.dvd_prime_pow (by norm_num : Nat.Prime 2)).mp hk1dvd with ⟨eb, heb, hkeb⟩
    -- 2^eb = 2^ea + 1
    have hdiff : 2 ^ eb = 2 ^ ea + 1 := by omega
    have hea0 : ea = 0 := pow_two_diff_one ea eb hdiff
    have : k = 1 := by simpa [hea0] using hkea
    omega

/-! 双涌现路径判别：路径 A（2^m=2m+2 唯一 m=3，数字验证；266 机器证明）∧
    路径 B（本主定理）——两条独立代数路径绑定 N_gen=3 ↔ k_max=8。 -/
theorem two_path_judgement :
    (2 ^ nGen = 2 * nGen + 2 ∧ ∀ n m : ℕ, n ^ 2 - 1 = 2 ^ m → 2 ≤ n → n = 3 ∧ m = 3) := by
  constructor
  · norm_num [nGen]
  · intro n m h hm
    exact kmax_two_power_unique n m h hm

end MUFPF.KMaxTwoPower
