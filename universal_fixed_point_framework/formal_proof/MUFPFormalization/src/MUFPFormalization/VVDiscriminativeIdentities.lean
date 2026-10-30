import MUFPFormalization.CoreConstantWindowIdentities
import MUFPFormalization.FermatMod24Identities
import MUFPFormalization.SilentMod3Identities

/-!
# VVDiscriminativeIdentities.lean — VV 判别性收尾：129 闭式常数地位（P7-5e-222）

对应 209 系列（222 ㉒ VV 判别性收尾，129 闭式常数地位 + 子线封存）：

- ★ VV1：特殊指数骨架 {1,4,7,16} = {2^0, 2^2, 2^3−1, 2^4}
  —— 偶 2 幂（Fermat 指数 1,4,16）∪ Mersenne 素数 7（=2^3−1）。
- ★ VV2：D(n) 平方成员仅 n=9（D(9)=129²，n=2..20 唯一）；
  129²−1=16640=2^8·65=128·130 差 2 分解（2^7 × 2·65——充分结构 = 满格 2^7 × 双倍修正锚点）。
- ★ VV3：129=2·65−1（代数恒等 2(2^6+1)−1=2^7+1）——129 是修正锚点 65 的双倍−1 后继
  （65=2^6+1 m=6、129=2^7+1 m=7 相邻）。
- ★ VV4：m 奇 → 2^m+1 恒含因子 3（129=3·43、8193=3·2731、524289=3·174763），
  m=7 是子列（m≡1 mod 3）最小素数指数。
- ★ VV5 判别综合：129 闭式常数地位四重身份——Mersenne 素数指数（7=2^3−1）×
  静默类（8·16+1）× D(9) 唯一平方根 × 65 后继。

数值先证伪 5/5（scripts/_phase102_p7_5e222_vv_prime_index_subcol_closure.py，
VV1..VV5 ok 全 true）。诚实边界：VV1 指数分解核对、VV2 枚举扫描 + 差 2 分解恒等、
VV3/VV4 代数恒等、VV5 判别综合（语义指认）——候选层未升定案层；
子线封存声明为研究管理登记（209~222 ⑨~㉒ 闭环，回主线）。
-/

namespace MUFPF.VVDiscriminative

open Nat
open MUFPF.CoreConstantWindow
open MUFPF.FermatMod24
open MUFPF.SilentMod3

/-! ## §1 ★ VV1：特殊指数骨架 -/

/-- VV1a：指数分解 {1,4,7,16} = {2^0, 2^2, 2^3−1, 2^4}。 -/
theorem vv1_index_decomp :
    2 ^ 0 = 1 ∧ 2 ^ 2 = 4 ∧ 2 ^ 3 - 1 = 7 ∧ 2 ^ 4 = 16 := by
  norm_num

/-- VV1b：7 是 Mersenne 素数（2^3−1）。 -/
theorem vv1_mersenne_prime_7 : Nat.Prime 7 ∧ 7 = 2 ^ 3 - 1 := by
  constructor <;> norm_num

/-- VV1c：7 不是 2 的幂（∀a，2^a ≠ 7）——骨架中 7 是唯一 Mersenne 成员。 -/
theorem vv1_7_not_pow2 (a : ℕ) : 2 ^ a ≠ 7 := by
  by_cases h0 : a = 0
  · rw [h0]
    norm_num
  · by_cases h1 : a = 1
    · rw [h1]
      norm_num
    · have h2 : 2 ≤ a := by omega
      have hpow : 2 ^ a = 4 * 2 ^ (a - 2) := by
        rw [show a = (a - 2) + 2 by omega, pow_add]
        norm_num
        exact (Nat.mul_comm (2 ^ (a - 2)) 4)
      have hmod : 2 ^ a % 4 = 0 := by
        rw [hpow, Nat.mul_mod]
        norm_num
      intro h
      have hm : 2 ^ a % 4 = 7 % 4 := by
        rw [h]
      rw [hmod] at hm
      norm_num at hm

/-! ## §2 ★ VV2：D(n) 平方成员唯一 + 差 2 分解 -/

/-- 平方 mod 3 不等于 2（平方剩余集 {0,1}）。 -/
lemma sq_mod3_neq2 (r : ℕ) : r ^ 2 % 3 ≠ 2 := by
  rw [pow_two, Nat.mul_mod]
  have hlt : r % 3 < 3 := Nat.mod_lt r (by norm_num)
  interval_cases r % 3 <;> norm_num

/-- 平方 mod 7 不等于 3（平方剩余集 {0,1,2,4}）。 -/
lemma sq_mod7_neq3 (r : ℕ) : r ^ 2 % 7 ≠ 3 := by
  rw [pow_two, Nat.mul_mod]
  have hlt : r % 7 < 7 := Nat.mod_lt r (by norm_num)
  interval_cases r % 7 <;> norm_num

/-- 平方 mod 7 不等于 5。 -/
lemma sq_mod7_neq5 (r : ℕ) : r ^ 2 % 7 ≠ 5 := by
  rw [pow_two, Nat.mul_mod]
  have hlt : r % 7 < 7 := Nat.mod_lt r (by norm_num)
  interval_cases r % 7 <;> norm_num

/-- n ≡ 1 (mod 3) ⇒ 2^n ≡ 2 (mod 7)（2^3 ≡ 1 周期 3）。 -/
lemma pow2_mod7_of_mod3_1 (n : ℕ) (hn : n % 3 = 1) : 2 ^ n % 7 = 2 := by
  calc
    2 ^ n % 7 = (2 ^ (3 * (n / 3) + n % 3)) % 7 := by
      rw [show 3 * (n / 3) + n % 3 = n by omega]
    _ = (2 ^ (3 * (n / 3)) * 2 ^ (n % 3)) % 7 := by rw [pow_add]
    _ = (2 ^ (3 * (n / 3)) % 7 * (2 ^ (n % 3) % 7)) % 7 := by rw [Nat.mul_mod]
    _ = (1 * (2 ^ (n % 3) % 7)) % 7 := by
      rw [show 2 ^ (3 * (n / 3)) % 7 = 1 by
        calc
          2 ^ (3 * (n / 3)) % 7 = (2 ^ 3) ^ (n / 3) % 7 := by rw [pow_mul]
          _ = 8 ^ (n / 3) % 7 := by norm_num
          _ = 1 := pow8_mod7 (n / 3)]
    _ = 2 := by
      rw [hn]
      norm_num

/-- n ≡ 2 (mod 3) ⇒ 2^n ≡ 4 (mod 7)。 -/
lemma pow2_mod7_of_mod3_2 (n : ℕ) (hn : n % 3 = 2) : 2 ^ n % 7 = 4 := by
  calc
    2 ^ n % 7 = (2 ^ (3 * (n / 3) + n % 3)) % 7 := by
      rw [show 3 * (n / 3) + n % 3 = n by omega]
    _ = (2 ^ (3 * (n / 3)) * 2 ^ (n % 3)) % 7 := by rw [pow_add]
    _ = (2 ^ (3 * (n / 3)) % 7 * (2 ^ (n % 3) % 7)) % 7 := by rw [Nat.mul_mod]
    _ = (1 * (2 ^ (n % 3) % 7)) % 7 := by
      rw [show 2 ^ (3 * (n / 3)) % 7 = 1 by
        calc
          2 ^ (3 * (n / 3)) % 7 = (2 ^ 3) ^ (n / 3) % 7 := by rw [pow_mul]
          _ = 8 ^ (n / 3) % 7 := by norm_num
          _ = 1 := pow8_mod7 (n / 3)]
    _ = 4 := by
      rw [hn]
      norm_num

/-- D(n) ≡ 2^n + 1 (mod 7)（7n ≡ 0，2^(n−1)·2 = 2^n；需 n ≥ 1）。 -/
lemma dn_mod7 (n : ℕ) (hn1 : 1 ≤ n) : Dn n % 7 = (2 ^ n + 1) % 7 := by
  unfold Dn
  have hlin : 2 ^ (n - 1) * (7 * n + 2) + 1 = 7 * (2 ^ (n - 1) * n) + (2 ^ n + 1) := by
    calc
      2 ^ (n - 1) * (7 * n + 2) + 1
          = 7 * (2 ^ (n - 1) * n) + 2 ^ (n - 1) * 2 + 1 := by ring
      _ = 7 * (2 ^ (n - 1) * n) + 2 ^ n + 1 := by
        rw [show 2 ^ (n - 1) * 2 = 2 ^ n by
          rw [show n = (n - 1) + 1 by omega, pow_add]
          norm_num]
  calc
    (2 ^ (n - 1) * (7 * n + 2) + 1) % 7
        = (7 * (2 ^ (n - 1) * n) + (2 ^ n + 1)) % 7 := by rw [hlin]
    _ = (0 + (2 ^ n + 1) % 7) % 7 := by
      rw [Nat.add_mod, Nat.mul_mod]
      norm_num
    _ = (2 ^ n + 1) % 7 := by
      rw [zero_add]
      exact Nat.mod_mod (2 ^ n + 1) 7

/-- ★ VV2a：D(9) = 129²（闭式分母平方根；CoreConstantWindow.nn_d9_square 引用）。 -/
theorem vv2_d9_square : Dn 9 = 129 ^ 2 := by
  exact MUFPF.CoreConstantWindow.nn_d9_square

/-- ★ VV2b：D(n) 平方成员唯一——n=2..20 中仅 n=9（D(9)=129²）。 -/
theorem vv2_unique_square (n : ℕ) (hn2 : 2 ≤ n) (hn20 : n ≤ 20) :
    (∃ r : ℕ, Dn n = r ^ 2) ↔ n = 9 := by
  constructor
  · intro h
    rcases h with ⟨r, hr⟩
    have hmod3 : n % 3 = 0 ∨ n % 3 = 1 ∨ n % 3 = 2 := by omega
    have heo : Even n ∨ Odd n := Nat.even_or_odd n
    rcases hmod3 with hm0 | hm1 | hm2
    · rcases heo with hev | hod
      · -- n%3=0 ∧ Even n：D ≡ 2 (mod 3)，非平方
        have h7n2 : (7 * n + 2) % 3 = 2 := by
          rw [Nat.add_mod, Nat.mul_mod, hm0]
        have h2nm1 : 2 ^ (n - 1) % 3 = 2 := by
          rcases hev with ⟨a, rfl⟩
          have ha1 : 1 ≤ a := by omega
          rw [show a + a - 1 = 2 * (a - 1) + 1 by omega]
          exact pow2_odd_mod3 (a - 1)
        have hD3 : Dn n % 3 = 2 := by
          unfold Dn
          calc
            (2 ^ (n - 1) * (7 * n + 2) + 1) % 3
                = ((2 ^ (n - 1) % 3 * ((7 * n + 2) % 3)) % 3 + 1 % 3) % 3 := by
              rw [Nat.add_mod, Nat.mul_mod]
            _ = 2 := by
              rw [h2nm1, h7n2]
        have hD' : Dn n % 3 = r ^ 2 % 3 := by
          rw [hr]
        rw [hD3] at hD'
        exfalso
        exact (sq_mod3_neq2 r) hD'.symm
      · -- n%3=0 ∧ Odd n：n ∈ {3,9,15} 逐个
        have hcand : n = 3 ∨ n = 9 ∨ n = 15 := by
          interval_cases n <;> clear hr <;> simp at hm0 ⊢ <;>
            try (rcases hod with ⟨t, ht⟩ <;> omega)
        rcases hcand with h3 | h9 | h15
        · -- n=3：D(3)=93 非平方（9² < 93 < 10² 夹逼）
          have h93 : Dn 3 = 93 := by
            unfold Dn
            norm_num
          rw [h3, h93] at hr
          have hlo : 9 * 9 < 93 := by norm_num
          have hhi : 93 < 10 * 10 := by norm_num
          have hrge : 10 ≤ r := by
            by_contra hnot
            nlinarith
          have hrle : r ≤ 9 := by
            by_contra hnot
            nlinarith
          omega
        · -- n=9：命中
          exact h9
        · -- n=15：D(15)=1753089 非平方（1324² < D < 1325² 夹逼）
          have h15v : Dn 15 = 1753089 := by
            unfold Dn
            norm_num
          rw [h15, h15v] at hr
          have hlo : 1324 * 1324 < 1753089 := by norm_num
          have hhi : 1753089 < 1325 * 1325 := by norm_num
          have hrge : 1325 ≤ r := by
            by_contra hnot
            nlinarith
          have hrle : r ≤ 1324 := by
            by_contra hnot
            nlinarith
          omega
    · -- n%3=1：D ≡ 2^n+1 ≡ 3 (mod 7)，非平方
      have hD : Dn n % 7 = 3 := by
        rw [dn_mod7 n (by omega)]
        rw [Nat.add_mod, pow2_mod7_of_mod3_1 n hm1]
      have hD' : Dn n % 7 = r ^ 2 % 7 := by
        rw [hr]
      rw [hD] at hD'
      exfalso
      exact (sq_mod7_neq3 r) hD'.symm
    · -- n%3=2：D ≡ 2^n+1 ≡ 5 (mod 7)，非平方
      have hD : Dn n % 7 = 5 := by
        rw [dn_mod7 n (by omega)]
        rw [Nat.add_mod, pow2_mod7_of_mod3_2 n hm2]
      have hD' : Dn n % 7 = r ^ 2 % 7 := by
        rw [hr]
      rw [hD] at hD'
      exfalso
      exact (sq_mod7_neq5 r) hD'.symm
  · intro h9
    refine ⟨129, ?_⟩
    rw [h9]
    exact MUFPF.CoreConstantWindow.nn_d9_square

/-- ★ VV2c：129²−1 = 2^8·65 = 128·130 差 2 分解（2^7 × 2·65）。 -/
theorem vv2_diff2 : Dn 9 - 1 = 128 * 130 ∧ 130 - 128 = 2 := by
  constructor
  · rw [MUFPF.CoreConstantWindow.nn_d9_minus1]
    norm_num
  · norm_num

/-- VV2c'：充分结构分解 2^8·65 = 2^7·(2·65)（满格 2^7 × 双倍修正锚点）。 -/
theorem vv2_diff2_full : 2 ^ 8 * 65 = 2 ^ 7 * (2 * 65) := by
  norm_num

/-! ## §3 ★ VV3：129 = 2·65 − 1（65 后继） -/

/-- VV3：129 = 2·65−1（代数恒等 2(2^6+1)−1 = 2^7+1；65=2^6+1 m=6、129=2^7+1 m=7 相邻）。 -/
theorem vv3_successor :
    129 = 2 * 65 - 1 ∧ 65 = 2 ^ 6 + 1 ∧ 129 = 2 ^ 7 + 1 := by
  norm_num

/-! ## §4 ★ VV4：m 奇 → 2^m+1 恒含因子 3 -/

/-- VV4a：m 奇 ⇒ 3 ∣ 2^m+1（x^m+1 = (x+1)(…) 的模 3 实现）。 -/
theorem vv4_three_dvd (m : ℕ) (hm : Odd m) : 3 ∣ 2 ^ m + 1 := by
  rcases hm with ⟨t, rfl⟩
  rw [Nat.dvd_iff_mod_eq_zero]
  calc
    (2 ^ (2 * t + 1) + 1) % 3 = (2 ^ (2 * t + 1) % 3 + 1 % 3) % 3 := by rw [Nat.add_mod]
    _ = (2 + 1) % 3 := by
      rw [pow2_odd_mod3 t]
    _ = 0 := by norm_num

/-- VV4b：实例 129=3·43、8193=3·2731、524289=3·174763。 -/
theorem vv4_instances : 129 = 3 * 43 ∧ 8193 = 3 * 2731 ∧ 524289 = 3 * 174763 := by
  norm_num

/-- VV4c：m=7 是静默子列（m≡1 mod 3）最小素数指数（t=0→1、t=1→4 均非素）。 -/
theorem vv4_smallest_prime_index :
    Nat.Prime 7 ∧ (∀ t : ℕ, t ≤ 2 → t ≠ 2 → ¬ Nat.Prime (3 * t + 1)) := by
  constructor
  · norm_num
  · intro t ht hne
    interval_cases t
    · norm_num
    · norm_num
    · exact False.elim (hne rfl)

/-! ## §5 ★ VV5 判别综合：129 闭式常数地位四重身份 -/

/-- ★★ VV5：129 地位四重身份——Mersenne 素数指数 × 静默类 × D(9) 唯一平方根 × 65 后继。 -/
theorem vv5_judgement :
    (Nat.Prime 7 ∧ 7 = 2 ^ 3 - 1) ∧
    (129 = 8 * 16 + 1 ∧ 129 % 8 = 1) ∧
    (Dn 9 = 129 * 129) ∧
    (129 = 2 * 65 - 1 ∧ 65 = 2 ^ 6 + 1) := by
  constructor
  · exact vv1_mersenne_prime_7
  · constructor
    · constructor <;> norm_num
    · constructor
      · exact MUFPF.CoreConstantWindow.nn_d9_square
      · exact ⟨vv3_successor.1, vv3_successor.2.1⟩

/-! ## §6 联合判别定理（数值主定理） -/

/-- ★★ VV× 联合（数值主定理）：骨架 + Mersenne 7 + 7 非 2 幂 + D(9) 平方唯一
    + 差 2 分解 + 65 后继 + 3 因子 + 实例 + 最小素数指数 + 静默类。 —— 222 ㉒ 的数值主定理。 -/
theorem vv_discriminative_judgement :
    (2 ^ 0 = 1 ∧ 2 ^ 2 = 4 ∧ 2 ^ 3 - 1 = 7 ∧ 2 ^ 4 = 16) ∧
    (Nat.Prime 7 ∧ 7 = 2 ^ 3 - 1) ∧
    (∀ a : ℕ, 2 ^ a ≠ 7) ∧
    (Dn 9 = 129 ^ 2 ∧ ∀ n : ℕ, 2 ≤ n → n ≤ 20 → ((∃ r : ℕ, Dn n = r ^ 2) ↔ n = 9)) ∧
    (Dn 9 - 1 = 128 * 130 ∧ 130 - 128 = 2) ∧
    (129 = 2 * 65 - 1 ∧ 65 = 2 ^ 6 + 1) ∧
    (∀ m : ℕ, Odd m → 3 ∣ 2 ^ m + 1) ∧
    (129 = 3 * 43 ∧ 8193 = 3 * 2731 ∧ 524289 = 3 * 174763) ∧
    (Nat.Prime 7 ∧ ∀ t : ℕ, t ≤ 2 → t ≠ 2 → ¬ Nat.Prime (3 * t + 1)) ∧
    (129 % 8 = 1 ∧ 129 = 8 * 16 + 1) := by
  constructor
  · exact vv1_index_decomp
  · constructor
    · exact vv1_mersenne_prime_7
    · constructor
      · exact vv1_7_not_pow2
      · constructor
        · constructor
          · exact vv2_d9_square
          · intro n h2 h20
            exact vv2_unique_square n h2 h20
        · constructor
          · exact vv2_diff2
          · constructor
            · exact ⟨vv3_successor.1, vv3_successor.2.1⟩
            · constructor
              · exact vv4_three_dvd
              · constructor
                · exact vv4_instances
                · constructor
                  · exact vv4_smallest_prime_index
                  · constructor <;> norm_num

end MUFPF.VVDiscriminative
