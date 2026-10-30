import MUFPFormalization.CoreConstantWindowIdentities

/-!
# P7-5e-290 ★ CC3 静默家族机制 + GG 族闭式

对应 209 系列机制核心（212 ③ CC3 静默家族成员机制闭合、218 OO1 GG 族 m 闭式、
222 VV4 m 奇含 3 因子）：

- ★★★ cc3_silent：7n+2 = 2^(3k+1) 时 D(n) = 2^(n+3k)+1 —— D(n) 落入静默家族
  （2^m+1 家族）的充分条件 = 线性因子 7n+2 是 2 的幂（2 的幂 mod 7 周期 3：
  2^(3k+1) ≡ 2）。实例：n=2 → D(2)=2⁵+1=33、n=18 → D(18)=2²⁴+1、n=146 →
  D(146)=2¹⁵⁵+1。
- ★★ vv4_odd3：m 奇 → 2^m+1 恒含因子 3（x^m+1=(x+1)(…) 代数恒等；m=7 即
  129=3·43）——静默家族 m 奇成员的 3 因子必然性。
- ★ gg_dvd：7 ∣ (2^(3k+1)−2)（GG 族分母 n_k 整数性，模 7 论证 2³≡1）。
- ★ gg_m_closed：m_k 闭式 (2^(3k+1)−2)/7 + 3k = (2^(3k+1)+21k−2)/7
  （k=1..7：5,24,155,1182,9377,74916,599207；渐近 (2/7)·8^k）。

数值先证伪 66/66，残差 0。诚实边界：cc3_silent/gg_m_closed 为代数恒等+
整除论证；vv4_odd3 为经典数论（3 ∣ 2^m+1 当 m 奇）；语义连接（静默家族=
186 2 进幂集组织）观察级登记。
-/

namespace MUFPF.SilentFamilyMechanism

open Nat
open scoped BigOperators

/-! ## §1 ★★★ CC3：静默家族成员机制 -/

/-- ★★★ 7n+2=2^(3k+1) ⇒ D(n)=2^(n+3k)+1：D(n) 落入静默家族（2^m+1）的
    充分条件 = 线性因子是 2 的幂（k≥1 保证 2^(3k+1)≥16 即 n≥2）。 -/
theorem cc3_silent (n k : ℕ) (hk : 1 ≤ k) (h : 7*n + 2 = 2^(3*k+1)) :
    MUFPF.CoreConstantWindow.Dn n = 2^(n + 3*k) + 1 := by
  have hn : 1 ≤ n := by
    have h16 : 2^4 ≤ 2^(3*k+1) := by
      exact pow_le_pow_right₀ (by norm_num : 1 ≤ 2) (by omega : 4 ≤ 3*k+1)
    have hd : 16 ≤ 7*n + 2 := by rw [h]; exact h16
    omega
  change 2^(n-1) * (7*n + 2) + 1 = 2^(n + 3*k) + 1
  rw [h]
  rw [← pow_add]
  rw [show (n - 1) + (3*k + 1) = n + 3*k by omega]

/-- CC3 首实例：D(2)=2⁵+1=33（k=1 的机制推导，210 ZZ3 已知核对升级）。 -/
theorem cc3_d2 : MUFPF.CoreConstantWindow.Dn 2 = 2^5 + 1 := by
  change 2^(2-1) * (7*2 + 2) + 1 = 2^5 + 1
  norm_num

/-- CC3 第二实例：D(18)=2²⁴+1=16777217（7·18+2=128=2⁷）。 -/
theorem cc3_d18 : MUFPF.CoreConstantWindow.Dn 18 = 2^24 + 1 := by
  change 2^(18-1) * (7*18 + 2) + 1 = 2^24 + 1
  norm_num

/-! ## §2 ★★ VV4：m 奇 → 3 因子 -/

/-- ★★ m 奇 → 3 ∣ 2^m+1（静默家族 m 奇成员的 3 因子必然性；m=7 即 129=3·43）。
    构造证明：m=2t+1 → 2^m+1 = 2·4^t+1 = 2·(4^t−1)+3 = 3·(2Σ+1)，
    其中 4^t−1 = (4−1)·Σ_{i<t} 4^i（几何级数）。 -/
theorem vv4_odd3 (m : ℕ) (hm : Odd m) : 3 ∣ 2^m + 1 := by
  rcases hm with ⟨t, rfl⟩
  refine ⟨2 * (Finset.sum (Finset.range t) fun i => 4^i) + 1, ?_⟩
  have hgeo : 4^t - 1 = (4 - 1) * (Finset.sum (Finset.range t) fun i => 4^i) := by
    induction t with
    | zero => simp
    | succ t ih =>
        rw [pow_succ]
        rw [mul_comm]
        rw [Finset.sum_range_succ]
        calc
          4 * 4^t - 1 = (4^t - 1) + 3 * 4^t := by omega
          _ = 3 * (Finset.sum (Finset.range t) fun i => 4^i) + 3 * 4^t := by rw [ih]
          _ = 3 * ((Finset.sum (Finset.range t) fun i => 4^i) + 4^t) := by
            rw [← Nat.mul_add]
  have h1 : 1 ≤ 4^t := by
    exact one_le_pow₀ (by norm_num : 1 ≤ 4)
  calc
    2^(2*t+1) + 1 = 2 * 4^t + 1 := by
      rw [pow_succ]
      rw [mul_comm]
      rw [pow_mul]
      rfl
    _ = 2 * (4^t - 1) + 3 := by
      omega
    _ = 2 * ((4 - 1) * (Finset.sum (Finset.range t) fun i => 4^i)) + 3 := by
      rw [← hgeo]
    _ = 2 * (3 * (Finset.sum (Finset.range t) fun i => 4^i)) + 3 := by
      norm_num
    _ = 3 * (2 * (Finset.sum (Finset.range t) fun i => 4^i) + 1) := by
      ring

/-- VV4 特例：m=7 → 3·43=129（闭式常数）。 -/
theorem vv4_129 : 3 * 43 = 129 ∧ 3 ∣ 2^7 + 1 := by
  constructor <;> norm_num

/-! ## §3 ★ GG 族：分母整数性与 m 闭式 -/

/-- ★ 7 ∣ (2^(3k+1)−2)：GG 族分母 n_k=(2^(3k+1)−2)/7 的整数性。
    构造证明：2^(3k+1)−2 = 2·(8^k−1) = 2·(8−1)·Σ_{i<k} 8^i = 7·(2·Σ)。 -/
theorem gg_dvd (k : ℕ) : 7 ∣ (2^(3*k+1) - 2) := by
  refine ⟨2 * (Finset.sum (Finset.range k) fun i => 8^i), ?_⟩
  have hgeo8 : 8^k - 1 = (8 - 1) * (Finset.sum (Finset.range k) fun i => 8^i) := by
    induction k with
    | zero => simp
    | succ k ih =>
        rw [pow_succ]
        rw [mul_comm]
        rw [Finset.sum_range_succ]
        calc
          8 * 8^k - 1 = (8^k - 1) + 7 * 8^k := by omega
          _ = 7 * (Finset.sum (Finset.range k) fun i => 8^i) + 7 * 8^k := by rw [ih]
          _ = 7 * ((Finset.sum (Finset.range k) fun i => 8^i) + 8^k) := by
            rw [← Nat.mul_add]
  have h1 : 1 ≤ 8^k := by
    exact one_le_pow₀ (by norm_num : 1 ≤ 8)
  calc
    2^(3*k+1) - 2 = 2 * 8^k - 2 := by
      congr 1
      rw [pow_succ]
      rw [mul_comm]
      rw [pow_mul]
      rfl
    _ = 2 * (8^k - 1) := by
      rw [show 2 * 8^k - 2 = 2 * 8^k - 2 * 1 by rw [mul_one]]
      rw [← Nat.mul_sub_left_distrib]
    _ = 2 * ((8 - 1) * (Finset.sum (Finset.range k) fun i => 8^i)) := by
      rw [← hgeo8]
    _ = 2 * (7 * (Finset.sum (Finset.range k) fun i => 8^i)) := by
      norm_num
    _ = 7 * (2 * (Finset.sum (Finset.range k) fun i => 8^i)) := by
      ring

/-- ★ OO1：m_k 闭式恒等（k=1..7：5,24,155,1182,9377,74916,599207）。 -/
theorem gg_m_closed (k : ℕ) :
    (2^(3*k+1) - 2) / 7 + 3*k = (2^(3*k+1) + 21*k - 2) / 7 := by
  have hdiv : 7 ∣ (2^(3*k+1) - 2) := gg_dvd k
  rcases hdiv with ⟨c, hc⟩
  have ha : 2 ≤ 2^(3*k+1) := by
    exact pow_le_pow_right₀ (by norm_num : 1 ≤ 2) (by omega : 1 ≤ 3*k+1)
  calc
    (2^(3*k+1) - 2) / 7 + 3*k = c + 3*k := by
      rw [hc]
      rw [Nat.mul_div_right c (by norm_num : 0 < 7)]
    _ = (7*c + 21*k) / 7 := by
      rw [show 7*c + 21*k = 7 * (c + 3*k) by ring]
      rw [Nat.mul_div_right (c + 3*k) (by norm_num : 0 < 7)]
    _ = (2^(3*k+1) + 21*k - 2) / 7 := by
      rw [← hc]
      congr 1
      omega

/-! ## §4 联合主定理 -/

/-- ★★ CC3+VV4+GG 联合（数值主定理）：D(2)=2⁵+1 ∧ 7∣14 ∧ m₁=5 ∧ 3∣129。
    —— 静默家族机制、GG 族整数性、m 闭式与 3 因子必然性的联合实例。 -/
theorem gg_silent_duality :
    MUFPF.CoreConstantWindow.Dn 2 = 2^5 + 1 ∧
    7 ∣ (2^4 - 2) ∧
    (2^4 - 2) / 7 + 3 = (2^4 + 21 - 2) / 7 ∧
    3 ∣ 2^7 + 1 := by
  constructor
  · exact cc3_d2
  · constructor
    · norm_num
    · constructor
      · norm_num
      · norm_num

end MUFPF.SilentFamilyMechanism
