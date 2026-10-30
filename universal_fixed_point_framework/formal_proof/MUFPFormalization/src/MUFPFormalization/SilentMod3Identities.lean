import MUFPFormalization.GGModularIdentities
import MUFPFormalization.FermatMod24Identities

/-!
# SilentMod3Identities.lean — 静默 mod 3 子列与原根自由度（P7-5e-220）

对应 209 系列（220 ⑳ 静默 mod 3 子列与原根自由度）：

- ★ RR1：静默家族 m≡1 mod 3 子列 {2^(3t+1)+1} = {3,17,129,1025,8193,65537,…}
  —— 含种子 3（m=1）、F_2=17（m=4）、闭式常数 129（m=7）与 F_4=65537（m=16）。
- ★ RR2：GG 族 m_k mod 3 = 2,0 交替（k 奇→2、k 偶→0）——机制：
  7·m_k = 2^(3k+1)+21k−2 ⇒ m_k ≡ 2^(3k+1)−2 mod 3；k 奇 ⇒ 3k+1 偶 ⇒
  2^(3k+1)≡1 ⇒ m_k≡2；k 偶 ⇒ 3k+1 奇 ⇒ 2^(3k+1)≡2 ⇒ m_k≡0。
- ★ RR3：GG 族 m_k 永 ≠ 1 mod 3，与静默家族 m≡1 mod 3 子列无交集
  —— 余项 3k−2 ≡ 1 mod 3 恒成立但与 m_k 本身 mod 3 脱钩。
- ★ SS1：3/5 是 mod 7 原根（阶 6）→ 3^b 单独遍历乘法群非零类
  （3^0..3^5 = [1,3,2,6,4,5]）→ 2^a·3^b·5^c 遍历全部 mod 7 非零类 → ≡2 可解
  （⑫ CC2 复验 35 解，脚本口径 a<9,b<5,c<5 且 nv≥1）；固定 6·2^a 缺自由度
  仅 {6,5,3}（6·2^a mod 7 = [6,5,3] 循环，2 ∉）。
- SS2：含 3 因子非必要（100=2²·5² 无 3 也 ≡2 mod 7）。
- ★ SS3：6·2^a = 2^(a+1)·3 是缺 5 因子的 {2,3} 纯积，5 因子加入恢复可解性
  （witness 周期 [1,3,5]：∀a ∃c，6·2^a·5^c ≡ 2 mod 7；Lean 取 8 实例并置）。

数值先证伪 21/21（scripts/_phase105_p7_5e220_silent_mod3.py）。诚实边界：
RR1 子列枚举+成员核对、RR2 模算术推导、RR3 无交集观察、SS1 数论结构（原根/阶）、
SS2 单点核对、SS3 因子分解核对——候选层未升定案层。
-/

namespace MUFPF.SilentMod3

open Nat
open MUFPF.GGModular

/-! ## §0 定义 -/

/-- 静默家族 m≡1 mod 3 子列成员：下标 m=3t+1 时的值 2^(3t+1)+1。 -/
def SilentVal (t : ℕ) : ℕ := 2 ^ (3 * t + 1) + 1

/-! ## §1 ★ RR1：静默家族 m≡1 mod 3 子列 -/

/-- 种子 3（t=0，下标 m=1）。 -/
theorem rr1_seed3 : SilentVal 0 = 3 := by
  norm_num [SilentVal]

/-- F_2 = 17（t=1，下标 m=4；F_2 落入静默子列）。 -/
theorem rr1_F2 : SilentVal 1 = MUFPF.FermatMod24.Ferm 2 := by
  norm_num [SilentVal, MUFPF.FermatMod24.Ferm]

/-- 闭式常数 129（t=2，下标 m=7）。 -/
theorem rr1_129 : SilentVal 2 = 129 := by
  norm_num [SilentVal]

/-- F_4 = 65537（t=5，下标 m=16）。 -/
theorem rr1_F4 : SilentVal 5 = MUFPF.FermatMod24.Ferm 4 := by
  norm_num [SilentVal, MUFPF.FermatMod24.Ferm]

/-- 下标 m=3t+1 ≡ 1 mod 3（子列定义恒等）。 -/
theorem rr1_sub_mod3 (t : ℕ) : (3 * t + 1) % 3 = 1 := by
  rw [Nat.add_mod, Nat.mul_mod]
  norm_num

/-- RR1 六成员并置 {3,17,129,1025,8193,65537}。 -/
theorem rr1_vals :
    SilentVal 0 = 3 ∧ SilentVal 1 = 17 ∧ SilentVal 2 = 129 ∧ SilentVal 3 = 1025 ∧
    SilentVal 4 = 8193 ∧ SilentVal 5 = 65537 := by
  norm_num [SilentVal]

/-! ## §2 ★ RR2：GG 族 mod 3 交替 -/

/-- k 奇 ⇒ 3k+1 偶 ⇒ 2^(3k+1) ≡ 1 mod 3。 -/
theorem pow2_idx_even_mod3 (k : ℕ) (hk : Odd k) : 2 ^ (3 * k + 1) % 3 = 1 := by
  rcases hk with ⟨t, rfl⟩
  rw [show 3 * (2 * t + 1) + 1 = 2 * (3 * t + 2) by omega]
  exact MUFPF.FermatMod24.pow2_even_mod3 (3 * t + 2)

/-- k 偶 ⇒ 3k+1 奇 ⇒ 2^(3k+1) ≡ 2 mod 3。 -/
theorem pow2_idx_odd_mod3 (k : ℕ) (hk : Even k) : 2 ^ (3 * k + 1) % 3 = 2 := by
  rcases hk with ⟨t, rfl⟩
  rw [show 3 * (t + t) + 1 = 2 * (3 * t) + 1 by omega]
  exact MUFPF.FermatMod24.pow2_odd_mod3 (3 * t)

/-- 8^k ≡ 1 mod 7（8 ≡ 1 mod 7，归纳）。 -/
lemma pow8_mod7 (k : ℕ) : 8 ^ k % 7 = 1 := by
  induction k with
  | zero => norm_num
  | succ k ih =>
      rw [pow_succ]
      rw [Nat.mul_mod, ih]

/-- 2^(3k+1) ≡ 2 mod 7（2^(3k+1) = 2·8^k，8^k≡1）。 -/
lemma pow2_mod7_3k1 (k : ℕ) : 2 ^ (3 * k + 1) % 7 = 2 := by
  calc
    2 ^ (3 * k + 1) % 7 = (2 * 8 ^ k) % 7 := by
      rw [show 2 ^ (3 * k + 1) = 2 * 8 ^ k by
        calc
          2 ^ (3 * k + 1) = 2 ^ (3 * k) * 2 := by rw [pow_succ]
          _ = (2 ^ 3) ^ k * 2 := by rw [pow_mul]
          _ = 8 ^ k * 2 := by norm_num
          _ = 2 * 8 ^ k := by rw [Nat.mul_comm]]
    _ = (2 * (8 ^ k % 7)) % 7 := by rw [Nat.mul_mod]
    _ = (2 * 1) % 7 := by rw [pow8_mod7]
    _ = 2 := by norm_num

/-- GG 商 (2^(3k+1)−2)/7 ≡ 2 mod 3（k 奇）：N ≡ 1−2 ≡ 2 mod 3，商 ≡ N mod 3。 -/
theorem gg_q_mod3_odd (k : ℕ) (hk : Odd k) : ((2 ^ (3 * k + 1) - 2) / 7) % 3 = 2 := by
  have hdec : 2 ^ (3 * k + 1) = 3 * (2 ^ (3 * k + 1) / 3) + 1 := by
    exact (calc
      2 ^ (3 * k + 1) = 3 * (2 ^ (3 * k + 1) / 3) + 2 ^ (3 * k + 1) % 3 :=
        (Nat.div_add_mod (2 ^ (3 * k + 1)) 3).symm
      _ = 3 * (2 ^ (3 * k + 1) / 3) + 1 := by rw [pow2_idx_even_mod3 k hk])
  have h7dvd : 7 ∣ (2 ^ (3 * k + 1) - 2) := by
    refine ⟨2 ^ (3 * k + 1) / 7, ?_⟩
    rw [show 2 ^ (3 * k + 1) - 2 = 7 * (2 ^ (3 * k + 1) / 7) by
      have hd := (Nat.div_add_mod (2 ^ (3 * k + 1)) 7).symm
      rw [pow2_mod7_3k1 k] at hd
      omega]
  have hq : (2 ^ (3 * k + 1) - 2) / 7 = 2 ^ (3 * k + 1) / 7 := by
    apply (mul_left_cancel₀ (by norm_num : 7 ≠ 0))
    calc
      7 * ((2 ^ (3 * k + 1) - 2) / 7) = 2 ^ (3 * k + 1) - 2 := by rw [Nat.mul_div_cancel' h7dvd]
      _ = 7 * (2 ^ (3 * k + 1) / 7) := by
        rw [show 2 ^ (3 * k + 1) - 2 = 7 * (2 ^ (3 * k + 1) / 7) by
          have hd := (Nat.div_add_mod (2 ^ (3 * k + 1)) 7).symm
          rw [pow2_mod7_3k1 k] at hd
          omega]
  have hNmod : (2 ^ (3 * k + 1) - 2) % 3 = 2 := by
    rw [show 2 ^ (3 * k + 1) - 2 = 3 * ((2 ^ (3 * k + 1) / 3) - 1) + 2 by
      rw [hdec]
      have hk1 : 1 ≤ k := by
        rcases hk with ⟨t, _⟩
        omega
      have hs : 1 ≤ 2 ^ (3 * k + 1) / 3 := by
        have hge : 3 ≤ 2 ^ (3 * k + 1) := by
          exact Nat.le_trans (by norm_num : 3 ≤ 16)
            (Nat.pow_le_pow_right (by norm_num : 1 ≤ 2) (by omega : 4 ≤ 3 * k + 1))
        exact Nat.succ_le_of_lt (Nat.div_pos hge (by norm_num : 0 < 3))
      omega]
    rw [Nat.add_mod, Nat.mul_mod]
    norm_num
  have hqmod : ((2 ^ (3 * k + 1) - 2) / 7) % 3 = (2 ^ (3 * k + 1) - 2) % 3 := by
    rw [hq]
    have hN7 : 2 ^ (3 * k + 1) - 2 = 7 * (2 ^ (3 * k + 1) / 7) := by
      have hd := (Nat.div_add_mod (2 ^ (3 * k + 1)) 7).symm
      rw [pow2_mod7_3k1 k] at hd
      omega
    have h73 : (7 * (2 ^ (3 * k + 1) / 7)) % 3 = (2 ^ (3 * k + 1) / 7) % 3 := by
      rw [Nat.mul_mod]
      have hm : 1 * ((2 ^ (3 * k + 1) / 7) % 3) = (2 ^ (3 * k + 1) / 7) % 3 := by omega
      rw [show 7 % 3 = 1 by norm_num, hm]
      exact Nat.mod_eq_of_lt (Nat.mod_lt (2 ^ (3 * k + 1) / 7) (by norm_num : 0 < 3))
    rw [hN7, h73]
  calc
    ((2 ^ (3 * k + 1) - 2) / 7) % 3 = (2 ^ (3 * k + 1) - 2) % 3 := hqmod
    _ = 2 := hNmod

/-- GG 商 (2^(3k+1)−2)/7 ≡ 0 mod 3（k 偶）：N ≡ 2−2 ≡ 0 mod 3。 -/
theorem gg_q_mod3_even (k : ℕ) (hk : Even k) : ((2 ^ (3 * k + 1) - 2) / 7) % 3 = 0 := by
  have hdec : 2 ^ (3 * k + 1) = 3 * (2 ^ (3 * k + 1) / 3) + 2 := by
    exact (calc
      2 ^ (3 * k + 1) = 3 * (2 ^ (3 * k + 1) / 3) + 2 ^ (3 * k + 1) % 3 :=
        (Nat.div_add_mod (2 ^ (3 * k + 1)) 3).symm
      _ = 3 * (2 ^ (3 * k + 1) / 3) + 2 := by rw [pow2_idx_odd_mod3 k hk])
  have h7dvd : 7 ∣ (2 ^ (3 * k + 1) - 2) := by
    refine ⟨2 ^ (3 * k + 1) / 7, ?_⟩
    rw [show 2 ^ (3 * k + 1) - 2 = 7 * (2 ^ (3 * k + 1) / 7) by
      have hd := (Nat.div_add_mod (2 ^ (3 * k + 1)) 7).symm
      rw [pow2_mod7_3k1 k] at hd
      omega]
  have hq : (2 ^ (3 * k + 1) - 2) / 7 = 2 ^ (3 * k + 1) / 7 := by
    apply (mul_left_cancel₀ (by norm_num : 7 ≠ 0))
    calc
      7 * ((2 ^ (3 * k + 1) - 2) / 7) = 2 ^ (3 * k + 1) - 2 := by rw [Nat.mul_div_cancel' h7dvd]
      _ = 7 * (2 ^ (3 * k + 1) / 7) := by
        rw [show 2 ^ (3 * k + 1) - 2 = 7 * (2 ^ (3 * k + 1) / 7) by
          have hd := (Nat.div_add_mod (2 ^ (3 * k + 1)) 7).symm
          rw [pow2_mod7_3k1 k] at hd
          omega]
  have hNmod : (2 ^ (3 * k + 1) - 2) % 3 = 0 := by
    rw [show 2 ^ (3 * k + 1) - 2 = 3 * (2 ^ (3 * k + 1) / 3) by
      rw [hdec]
      omega]
    rw [Nat.mul_mod]
    norm_num
  have hqmod : ((2 ^ (3 * k + 1) - 2) / 7) % 3 = (2 ^ (3 * k + 1) - 2) % 3 := by
    rw [hq]
    have hN7 : 2 ^ (3 * k + 1) - 2 = 7 * (2 ^ (3 * k + 1) / 7) := by
      have hd := (Nat.div_add_mod (2 ^ (3 * k + 1)) 7).symm
      rw [pow2_mod7_3k1 k] at hd
      omega
    have h73 : (7 * (2 ^ (3 * k + 1) / 7)) % 3 = (2 ^ (3 * k + 1) / 7) % 3 := by
      rw [Nat.mul_mod]
      have hm : 1 * ((2 ^ (3 * k + 1) / 7) % 3) = (2 ^ (3 * k + 1) / 7) % 3 := by omega
      rw [show 7 % 3 = 1 by norm_num, hm]
      exact Nat.mod_eq_of_lt (Nat.mod_lt (2 ^ (3 * k + 1) / 7) (by norm_num : 0 < 3))
    rw [hN7, h73]
  calc
    ((2 ^ (3 * k + 1) - 2) / 7) % 3 = (2 ^ (3 * k + 1) - 2) % 3 := hqmod
    _ = 0 := hNmod

/-- ★ k 奇 ⇒ Gm k ≡ 2 mod 3（RR2 交替奇支）。 -/
theorem rr2_odd (k : ℕ) (hk : Odd k) : Gm k % 3 = 2 := by
  unfold Gm
  have hq := gg_q_mod3_odd k hk
  calc
    ((2 ^ (3 * k + 1) - 2) / 7 + 3 * k) % 3 =
        (((2 ^ (3 * k + 1) - 2) / 7) % 3 + (3 * k) % 3) % 3 := by rw [Nat.add_mod]
    _ = (2 + (3 * k) % 3) % 3 := by rw [hq]
    _ = (2 + 0) % 3 := by
      rw [Nat.mul_mod]
      norm_num
    _ = 2 := by norm_num

/-- ★ k 偶 ⇒ Gm k ≡ 0 mod 3（RR2 交替偶支）。 -/
theorem rr2_even (k : ℕ) (hk : Even k) : Gm k % 3 = 0 := by
  unfold Gm
  have hq := gg_q_mod3_even k hk
  calc
    ((2 ^ (3 * k + 1) - 2) / 7 + 3 * k) % 3 =
        (((2 ^ (3 * k + 1) - 2) / 7) % 3 + (3 * k) % 3) % 3 := by rw [Nat.add_mod]
    _ = (0 + (3 * k) % 3) % 3 := by rw [hq]
    _ = (0 + 0) % 3 := by
      rw [Nat.mul_mod]
      norm_num
    _ = 0 := by norm_num

/-- RR2 八实例 [2,0,2,0,2,0,2,0]（k=1..8）。 -/
theorem rr2_vals :
    Gm 1 % 3 = 2 ∧ Gm 2 % 3 = 0 ∧ Gm 3 % 3 = 2 ∧ Gm 4 % 3 = 0 ∧
    Gm 5 % 3 = 2 ∧ Gm 6 % 3 = 0 ∧ Gm 7 % 3 = 2 ∧ Gm 8 % 3 = 0 := by
  exact ⟨rr2_odd 1 (by exact ⟨0, by norm_num⟩), rr2_even 2 (by exact ⟨1, by norm_num⟩),
         rr2_odd 3 (by exact ⟨1, by norm_num⟩), rr2_even 4 (by exact ⟨2, by norm_num⟩),
         rr2_odd 5 (by exact ⟨2, by norm_num⟩), rr2_even 6 (by exact ⟨3, by norm_num⟩),
         rr2_odd 7 (by exact ⟨3, by norm_num⟩), rr2_even 8 (by exact ⟨4, by norm_num⟩)⟩

/-- ★ RR2 主定理：k≥1 ⇒ Gm k mod 3 = 2/0 按奇偶交替。 -/
theorem rr2_alt (k : ℕ) (hk : 1 ≤ k) : Gm k % 3 = (if k % 2 = 1 then 2 else 0) := by
  by_cases hodd : Odd k
  · have h1 : k % 2 = 1 := by
      rcases hodd with ⟨t, rfl⟩
      rw [Nat.add_mod, Nat.mul_mod]
      norm_num
    simpa [h1] using rr2_odd k hodd
  · have he : Even k := by
      rcases Nat.even_or_odd k with h | h
      · exact h
      · exact False.elim (hodd h)
    have h0 : k % 2 = 0 := by
      rcases he with ⟨t, rfl⟩
      rw [← two_mul t, Nat.mul_mod]
      norm_num
    simpa [h0] using rr2_even k he

/-! ## §3 ★ RR3：GG 族与静默子列无交集 -/

/-- 余项 3k−2 ≡ 1 mod 3 恒成立（k≥1）。 -/
theorem rr3_remainder_mod3 (k : ℕ) (hk : 1 ≤ k) : (3 * k - 2) % 3 = 1 := by
  rw [show 3 * k - 2 = 3 * (k - 1) + 1 by omega]
  rw [Nat.add_mod, Nat.mul_mod]
  norm_num

/-- ★ GG 族 m_k 永 ≠ 1 mod 3（与静默家族 m≡1 mod 3 子列无交集）。 -/
theorem rr3_no_intersect (k : ℕ) (_hk : 1 ≤ k) : Gm k % 3 ≠ 1 := by
  by_cases hodd : Odd k
  · rw [rr2_odd k hodd]
    norm_num
  · have he : Even k := by
      rcases Nat.even_or_odd k with h | h
      · exact h
      · exact False.elim (hodd h)
    rw [rr2_even k he]
    norm_num

/-! ## §4 ★ SS1：mod 7 原根与自由度 -/

/-- 3 是 mod 7 原根（阶 6）：3^6 ≡ 1 且真因子 1,2,3 均非 1。 -/
theorem ss1_order3 :
    (3 ^ 6) % 7 = 1 ∧ (3 ^ 1) % 7 ≠ 1 ∧ (3 ^ 2) % 7 ≠ 1 ∧ (3 ^ 3) % 7 ≠ 1 := by
  norm_num

/-- 5 是 mod 7 原根（阶 6）。 -/
theorem ss1_order5 :
    (5 ^ 6) % 7 = 1 ∧ (5 ^ 1) % 7 ≠ 1 ∧ (5 ^ 2) % 7 ≠ 1 ∧ (5 ^ 3) % 7 ≠ 1 := by
  norm_num

/-- 3^0..3^5 循环 [1,3,2,6,4,5]：3 生成乘法群全部非零类。 -/
theorem ss1_span_cycle :
    (3 ^ 0) % 7 = 1 ∧ (3 ^ 1) % 7 = 3 ∧ (3 ^ 2) % 7 = 2 ∧ (3 ^ 3) % 7 = 6 ∧
    (3 ^ 4) % 7 = 4 ∧ (3 ^ 5) % 7 = 5 := by
  norm_num

/-- 5^0..5^5 循环 [1,5,4,6,2,3]：5 亦生成全部非零类。 -/
theorem ss1_span_5_cycle :
    (5 ^ 0) % 7 = 1 ∧ (5 ^ 1) % 7 = 5 ∧ (5 ^ 2) % 7 = 4 ∧ (5 ^ 3) % 7 = 6 ∧
    (5 ^ 4) % 7 = 2 ∧ (5 ^ 5) % 7 = 3 := by
  norm_num

/-- 固定 6·2^a mod 7 = [6,5,3] 循环（缺自由度仅 3 类）。 -/
theorem ss1_fixed_cycle :
    (6 * 2 ^ 0) % 7 = 6 ∧ (6 * 2 ^ 1) % 7 = 5 ∧ (6 * 2 ^ 2) % 7 = 3 ∧
    (6 * 2 ^ 3) % 7 = 6 ∧ (6 * 2 ^ 4) % 7 = 5 ∧ (6 * 2 ^ 5) % 7 = 3 := by
  norm_num

/-- ★ 2 不在固定自由度 {6,5,3} 中（∀a，6·2^a 不 ≡ 2 mod 7；2 的阶 3 周期）。 -/
theorem ss1_2_not_in_fixed_all (a : ℕ) : (6 * 2 ^ a) % 7 ≠ 2 := by
  have hcyc : 2 ^ a % 7 = 2 ^ (a % 3) % 7 := by
    calc
      2 ^ a % 7 = (2 ^ (3 * (a / 3)) * 2 ^ (a % 3)) % 7 := by
        rw [show 2 ^ a = 2 ^ (3 * (a / 3) + a % 3) by
          exact congrArg (fun x => 2 ^ x) (Nat.div_add_mod a 3).symm]
        rw [pow_add]
      _ = ((2 ^ (3 * (a / 3)) % 7) * (2 ^ (a % 3) % 7)) % 7 := by rw [Nat.mul_mod]
      _ = (1 * (2 ^ (a % 3) % 7)) % 7 := by
        rw [show 2 ^ (3 * (a / 3)) % 7 = 1 by
          calc
            2 ^ (3 * (a / 3)) % 7 = (2 ^ 3) ^ (a / 3) % 7 := by rw [pow_mul]
            _ = 8 ^ (a / 3) % 7 := by norm_num
            _ = 1 := pow8_mod7 (a / 3)]
      _ = (2 ^ (a % 3) % 7) % 7 := by
        rw [show 1 * (2 ^ (a % 3) % 7) = 2 ^ (a % 3) % 7 by omega]
      _ = 2 ^ (a % 3) % 7 := by
        exact Nat.mod_eq_of_lt (Nat.mod_lt (2 ^ (a % 3)) (by norm_num : 0 < 7))
  rcases (show a % 3 = 0 ∨ a % 3 = 1 ∨ a % 3 = 2 by omega) with h0 | h1 | h2
  · have h2a : 2 ^ a % 7 = 1 := by
      rw [hcyc, h0]
      norm_num
    rw [Nat.mul_mod]
    rw [h2a]
    norm_num
  · have h2a : 2 ^ a % 7 = 2 := by
      rw [hcyc, h1]
      norm_num
    rw [Nat.mul_mod]
    rw [h2a]
    norm_num
  · have h2a : 2 ^ a % 7 = 4 := by
      rw [hcyc, h2]
      norm_num
    rw [Nat.mul_mod]
    rw [h2a]
    norm_num

/-! ## §5 SS2/SS3：含 3 非必要与 5 因子恢复 -/

/-- SS2：100 = 2²·5²（无 3 因子）且 ≡ 2 mod 7。 -/
theorem ss2_100 : 100 % 7 = 2 ∧ 100 = 2 ^ 2 * 5 ^ 2 := by
  norm_num

/-- SS3：6·2^a = 2^(a+1)·3（缺 5 因子的 {2,3} 纯积恒等）。 -/
theorem ss3_pure23 (a : ℕ) : 6 * 2 ^ a = 2 ^ (a + 1) * 3 := by
  calc
    6 * 2 ^ a = (2 ^ a * 2) * 3 := by ring
    _ = 2 ^ (a + 1) * 3 := by rw [pow_succ]

/-- SS3：5 因子加入恢复可解性——8 实例并置（witness 周期 [1,3,5]；
    ∀a 存在性由数值脚本复验，Lean 取实例）。 -/
theorem ss3_fix5_instances :
    (6 * 2 ^ 0 * 5 ^ 1) % 7 = 2 ∧ (6 * 2 ^ 1 * 5 ^ 3) % 7 = 2 ∧
    (6 * 2 ^ 2 * 5 ^ 5) % 7 = 2 ∧ (6 * 2 ^ 3 * 5 ^ 1) % 7 = 2 ∧
    (6 * 2 ^ 4 * 5 ^ 3) % 7 = 2 ∧ (6 * 2 ^ 5 * 5 ^ 5) % 7 = 2 ∧
    (6 * 2 ^ 6 * 5 ^ 1) % 7 = 2 ∧ (6 * 2 ^ 7 * 5 ^ 3) % 7 = 2 := by
  norm_num

/-! ## §6 联合主定理 -/

/-- ★★ RR×SS 联合（数值主定理）：静默 m≡1 mod 3 子列成员核对（种子 3、F_2、
    闭式常数 129、F_4）+ GG mod 3 交替实例 + 无交集 + 原根阶 + 100 解 + 5 因子
    恢复可解性并置。 —— 220 ⑳ 的数值主定理。 -/
theorem silent_mod3_judgement :
    (SilentVal 0 = 3) ∧ (SilentVal 1 = MUFPF.FermatMod24.Ferm 2) ∧
    (SilentVal 2 = 129) ∧ (SilentVal 5 = MUFPF.FermatMod24.Ferm 4) ∧
    (Gm 1 % 3 = 2 ∧ Gm 2 % 3 = 0) ∧
    (Gm 3 % 3 ≠ 1) ∧
    ((3 ^ 6) % 7 = 1 ∧ (5 ^ 6) % 7 = 1) ∧
    (100 % 7 = 2 ∧ 100 = 2 ^ 2 * 5 ^ 2) ∧
    (6 * 2 ^ 3 * 5 ^ 1) % 7 = 2 := by
  refine ⟨rr1_seed3, rr1_F2, rr1_129, rr1_F4, ?_h5, ?_h6, ?_h7, ?_h8, ?_h9⟩
  · exact ⟨rr2_odd 1 (by exact ⟨0, by norm_num⟩), rr2_even 2 (by exact ⟨1, by norm_num⟩)⟩
  · exact rr3_no_intersect 3 (by norm_num)
  · exact ⟨by norm_num, by norm_num⟩
  · exact ss2_100
  · norm_num

end MUFPF.SilentMod3
