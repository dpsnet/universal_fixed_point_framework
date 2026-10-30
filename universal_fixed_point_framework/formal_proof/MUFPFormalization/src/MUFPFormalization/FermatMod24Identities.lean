import MUFPFormalization.GGModularIdentities
import MUFPFormalization.Period24Identities

/-!
# FermatMod24Identities.lean — 偶 Fermat 交集与 mod24 联合周期（P7-5e-221）

对应 209 系列（221 ㉑ 偶 Fermat 交集与 mod 24 联合周期）：

- ★ TT1：m≡1 mod 3 子列 ∩ Fermat 数 = 偶 Fermat 全部（3t+1=2^n ⟺ n 偶，
  t=(2^n−1)/3）——tt1_backward 给构造（n=2r）、tt1_forward 给必要性（模 3）。
- ★ TT2：Fermat 奇偶性 ↔ m mod 3 类——偶 F_{2r} 指数 2^(2r) ≡ 1 mod 3、
  奇 F_{2r+1} 指数 2^(2r+1) ≡ 2 mod 3。
- ★ TT3：Fermat 命中点 t 间隔 = 2^(2r)（tt3_gap 闭式）；129 = 2^7+1 是子列
  非 Fermat 成员（tt3_129_sub / tt3_129_not_fermat）。
- ★ UU1：GG 族 m_k mod 24 两分支闭式（k 奇 → 3k+2：5,11,17,23；k 偶 → 3k−6：
  0,6,12,18）——经模 168 引理（pow2_mod168_odd/even）与商引理 div7_mod24。
- ★ UU2：mod 24 周期 8（uu2_cycle 八实例 + uu2_period8 周期引理）。
- ★ UU3：CRT 合成——mod 8 遍历（⑮ II2）× mod 3 交替（⑳ RR2）联合于
  lcm(3,8)=24：uu3_mod8/uu3_mod3 从 UU1 闭式导出（mod24_mod8/mod24_mod3
  分解），uu3_lcm 引用 294 ll1_lcm。

数值先证伪 14/14（scripts/_phase105_p7_5e221_fermat_mod24.py）。诚实边界：
TT1 指数恒等、TT2 模算术、TT3 间隔枚举+模分类、UU1 模 168 计算、UU2 周期观察、
UU3 结构说明——候选层未升定案层。
-/

namespace MUFPF.FermatMod24

open Nat
open MUFPF.GGModular

/-! ## §0 定义 -/

/-- Fermat 数 F_k = 2^(2^k)+1。 -/
def Ferm (k : ℕ) : ℕ := 2 ^ (2 ^ k) + 1

/-! ## §1 模 3 基础 -/

/-- 4^r ≡ 1 mod 3（几何：4≡1，归纳）。 -/
lemma pow4_mod3 (r : ℕ) : 4 ^ r % 3 = 1 := by
  induction r with
  | zero => norm_num
  | succ r ih =>
      calc
        4 ^ (r + 1) % 3 = (4 * 4 ^ r) % 3 := by rw [pow_succ, mul_comm]
        _ = (4 % 3 * (4 ^ r % 3)) % 3 := by rw [Nat.mul_mod]
        _ = 1 := by norm_num [ih]

/-- ★ 偶指数：2^(2r) ≡ 1 mod 3（= (2²)^r，4^r）。 -/
theorem pow2_even_mod3 (r : ℕ) : 2 ^ (2 * r) % 3 = 1 := by
  have h : 2 ^ (2 * r) = 4 ^ r := by
    rw [pow_mul]
    norm_num
  rw [h]
  exact pow4_mod3 r

/-- ★ 奇指数：2^(2r+1) ≡ 2 mod 3。 -/
theorem pow2_odd_mod3 (r : ℕ) : 2 ^ (2 * r + 1) % 3 = 2 := by
  have h : 2 ^ (2 * r + 1) = 2 * 4 ^ r := by
    rw [pow_add, pow_mul]
    norm_num
    ring
  rw [h]
  calc
    (2 * 4 ^ r) % 3 = (2 % 3 * (4 ^ r % 3)) % 3 := by rw [Nat.mul_mod]
    _ = 2 := by norm_num [pow4_mod3 r]

/-- 2^n ≡ 1 mod 3 当 n 偶。 -/
theorem pow2_mod3_even (n : ℕ) (h : Even n) : 2 ^ n % 3 = 1 := by
  rcases h with ⟨r, rfl⟩
  rw [← two_mul r]
  exact pow2_even_mod3 r

/-- 2^n ≡ 2 mod 3 当 n 奇。 -/
theorem pow2_mod3_odd (n : ℕ) (h : Odd n) : 2 ^ n % 3 = 2 := by
  rcases h with ⟨r, rfl⟩
  exact pow2_odd_mod3 r

/-! ## §2 ★ TT1：3t+1=2^n 可解 ⟺ n 偶 -/

/-- ★ 充分：n 偶（n=2r）时 t=(2^(2r)−1)/3 是整数解（3t+1=2^(2r)）。 -/
theorem tt1_backward (r : ℕ) : ∃ t, 3 * t + 1 = 2 ^ (2 * r) := by
  have hq : 2 ^ (2 * r) = 3 * (2 ^ (2 * r) / 3) + 1 := by
    rw [← pow2_even_mod3 r]
    exact (Nat.div_add_mod (2 ^ (2 * r)) 3).symm
  refine ⟨2 ^ (2 * r) / 3, hq.symm⟩

/-- ★ 必要：3t+1=2^n ⇒ n 偶（模 3：2^n ≡ 1，指数偶）。 -/
theorem tt1_forward (n t : ℕ) (h : 3 * t + 1 = 2 ^ n) : Even n := by
  have hmod : 2 ^ n % 3 = 1 := by
    rw [← h]
    calc
      (3 * t + 1) % 3 = ((3 * t) % 3 + 1 % 3) % 3 := by rw [Nat.add_mod]
      _ = 1 := by
        rw [Nat.mul_mod]
        norm_num
  by_cases hn : Even n
  · exact hn
  · exfalso
    have ho : Odd n := by
      rcases Nat.even_or_odd n with h' | h'
      · exact False.elim (hn h')
      · exact h'
    have h2 : 2 ^ n % 3 = 2 := pow2_mod3_odd n ho
    rw [h2] at hmod
    norm_num at hmod

/-- ★ TT1 联合（可解 ⟺ 指数偶）。 -/
theorem tt1_iff_solvable :
    (∀ n t : ℕ, 3 * t + 1 = 2 ^ n → Even n) ∧ (∀ r : ℕ, ∃ t, 3 * t + 1 = 2 ^ (2 * r)) := by
  constructor
  · intro n t h
    exact tt1_forward n t h
  · intro r
    exact tt1_backward r

/-! ## §3 ★ TT2：Fermat 奇偶性 ↔ m mod 3 类 -/

/-- ★ 偶 F_{2r} 的指数 m=2^(2r) ≡ 1 mod 3（落 m≡1 mod 3 子列）。 -/
theorem tt2_even (r : ℕ) : 2 ^ (2 * r) % 3 = 1 := pow2_even_mod3 r

/-- ★ 奇 F_{2r+1} 的指数 m=2^(2r+1) ≡ 2 mod 3（不在子列）。 -/
theorem tt2_odd (r : ℕ) : 2 ^ (2 * r + 1) % 3 = 2 := pow2_odd_mod3 r

/-! ## §4 ★ TT3：命中点间隔 + 129 子列非 Fermat -/

/-- ★ Fermat 命中点 t 间隔闭式：t_{r+1}−t_r = 2^(2r)。
    即 (2^(2(r+1))−1)/3 = (2^(2r)−1)/3 + 2^(2r)。 -/
theorem tt3_gap (r : ℕ) :
    (2 ^ (2 * (r + 1)) - 1) / 3 = (2 ^ (2 * r) - 1) / 3 + 2 ^ (2 * r) := by
  let A : ℕ := 2 ^ (2 * r)
  let B : ℕ := A - 1
  have hBdiv : 3 ∣ B := by
    unfold B A
    have hmod : 2 ^ (2 * r) % 3 = 1 := pow2_even_mod3 r
    have hq2 : 2 ^ (2 * r) = 3 * (2 ^ (2 * r) / 3) + 1 := by
      rw [← hmod]
      exact (Nat.div_add_mod (2 ^ (2 * r)) 3).symm
    refine ⟨2 ^ (2 * r) / 3, ?_⟩
    rw [hq2]
    omega
  rcases hBdiv with ⟨q, hq⟩
  have h4r : 4 ^ r = 2 ^ (2 * r) := by
    rw [pow_mul]
    norm_num
  have hA4 : 2 ^ (2 * (r + 1)) = 4 * A := by
    unfold A
    rw [show 2 * (r + 1) = 2 * r + 2 by omega]
    rw [pow_add, pow_mul]
    norm_num
    rw [h4r]
    ring
  have h4A : 4 * A - 1 = 3 * (A + q) := by
    unfold B at hq
    rw [mul_add, ← hq]
    omega
  have hBq : (A - 1) / 3 = q := by
    have hBq' : B / 3 = q := by
      rw [hq]
      exact Nat.mul_div_right q (by norm_num : 0 < 3)
    simpa [B] using hBq'
  calc
    (2 ^ (2 * (r + 1)) - 1) / 3 = (4 * A - 1) / 3 := by rw [hA4]
    _ = (3 * (A + q)) / 3 := by rw [h4A]
    _ = A + q := by exact Nat.mul_div_right (A + q) (by norm_num : 0 < 3)
    _ = (2 ^ (2 * r) - 1) / 3 + A := by
      change A + q = (A - 1) / 3 + A
      rw [← hBq]
      rw [Nat.add_comm]
    _ = (2 ^ (2 * r) - 1) / 3 + 2 ^ (2 * r) := by rfl

/-- ★ 129 = 2^7+1 且 m=7=3·2+1 落 m≡1 mod 3 子列。 -/
theorem tt3_129_sub : 2 ^ 7 + 1 = 129 ∧ 7 % 3 = 1 := by
  norm_num

/-- ★ 129 非 Fermat 数（全称）：F_k=2^(2^k)+1 ≠ 129。
    证明：k=0 → 3 ≠ 129；k≥1 → 2^k 偶 → F_k ≡ 2 mod 3 ≠ 0 = 129 mod 3。 -/
theorem tt3_129_not_fermat (k : ℕ) : Ferm k ≠ 129 := by
  by_cases hk0 : k = 0
  · rw [hk0]
    norm_num [Ferm]
  · have hk1 : 1 ≤ k := by omega
    have hpow_even : Even (2 ^ k) := by
      rcases Nat.exists_eq_add_of_le hk1 with ⟨t, rfl⟩
      refine ⟨2 ^ t, ?_⟩
      rw [pow_add]
      norm_num
      rw [two_mul]
    have hmodF : Ferm k % 3 = 2 := by
      unfold Ferm
      calc
        (2 ^ (2 ^ k) + 1) % 3 = (2 ^ (2 ^ k) % 3 + 1 % 3) % 3 := by rw [Nat.add_mod]
        _ = 2 := by norm_num [pow2_mod3_even (2 ^ k) hpow_even]
    intro h
    have hmod_eq : Ferm k % 3 = 129 % 3 := by rw [h]
    rw [hmodF] at hmod_eq
    norm_num at hmod_eq

/-! ## §5 模 168 引理（UU1 核心） -/

/-- 2^(6t+4) ≡ 16 mod 168（归纳：2^(6(t+1)+4) = 2^(6t+4)·64，16·64=1024≡16）。 -/
lemma pow2_mod168_6t4 (t : ℕ) : 2 ^ (6 * t + 4) % 168 = 16 := by
  induction t with
  | zero => norm_num
  | succ t ih =>
      have h1 : 2 ^ (6 * (t + 1) + 4) % 168 = (2 ^ (6 * t + 4) * 2 ^ 6) % 168 := by
        have hExp : 6 * (t + 1) + 4 = (6 * t + 4) + 6 := by omega
        rw [hExp, pow_add]
      rw [h1]
      rw [Nat.mul_mod]
      rw [ih]
      norm_num

/-- 64^t ≡ 64 mod 168（t≥1：归纳，64·64=4096≡64）。 -/
lemma pow64_mod168 (t : ℕ) (ht : 1 ≤ t) : 64 ^ t % 168 = 64 := by
  rcases Nat.exists_eq_add_of_le ht with ⟨s, rfl⟩
  induction s with
  | zero => norm_num
  | succ s ih =>
      have hExp : 1 + (s + 1) = (1 + s) + 1 := by omega
      rw [hExp, pow_succ]
      rw [Nat.mul_mod]
      rw [ih]
      norm_num

/-- k 奇 ⇒ 2^(3k+1) ≡ 16 mod 168（k=2t+1 → 2^(6t+4)）。 -/
lemma pow2_mod168_odd (k : ℕ) (hk : Odd k) : 2 ^ (3 * k + 1) % 168 = 16 := by
  rcases hk with ⟨t, rfl⟩
  calc
    2 ^ (3 * (2 * t + 1) + 1) % 168 = 2 ^ (6 * t + 4) % 168 := by
      rw [show 3 * (2 * t + 1) + 1 = 6 * t + 4 by omega]
    _ = 16 := pow2_mod168_6t4 t

/-- k 偶且 k>0 ⇒ 2^(3k+1) ≡ 128 mod 168（k=2t、t≥1 → 2^(6t+1) = 2·64^t）。 -/
lemma pow2_mod168_even (k : ℕ) (hk : Even k) (hpos : 0 < k) : 2 ^ (3 * k + 1) % 168 = 128 := by
  rcases hk with ⟨t, rfl⟩
  have ht : 1 ≤ t := by omega
  have hExp : 3 * (t + t) + 1 = 6 * t + 1 := by omega
  rw [hExp]
  have h6 : 2 ^ (6 * t + 1) = 2 * 64 ^ t := by
    rw [show 6 * t + 1 = 1 + 6 * t by omega]
    rw [pow_add, pow_mul]
    norm_num
  rw [h6]
  rw [Nat.mul_mod]
  norm_num [pow64_mod168 t ht]

/-- 商引理：N = 7r + 168t ⇒ (N/7) % 24 = r % 24（168 = 7·24）。 -/
theorem div7_mod24 (N r t : ℕ) (hN : N = 7 * r + 168 * t) : (N / 7) % 24 = r % 24 := by
  have h7 : 7 ∣ N := by
    refine ⟨r + 24 * t, ?_⟩
    rw [hN]
    ring
  have hq : N / 7 = r + 24 * t := by
    apply (mul_left_cancel₀ (by norm_num : 7 ≠ 0))
    calc
      7 * (N / 7) = N := by rw [Nat.mul_div_cancel' h7]
      _ = 7 * (r + 24 * t) := by rw [hN]; ring
  calc
    (N / 7) % 24 = (r + 24 * t) % 24 := by rw [hq]
    _ = r % 24 := by exact Nat.add_mul_mod_self_left r 24 t

/-- ★ GG 商 (2^(3k+1)−2)/7 ≡ 2 mod 24（k 奇）。 -/
theorem gg_q_mod24_odd (k : ℕ) (hk : Odd k) : ((2 ^ (3 * k + 1) - 2) / 7) % 24 = 2 := by
  have hpow : 2 ^ (3 * k + 1) % 168 = 16 := pow2_mod168_odd k hk
  have hdec : 2 ^ (3 * k + 1) = 168 * (2 ^ (3 * k + 1) / 168) + 16 := by
    rw [← hpow]
    exact (Nat.div_add_mod (2 ^ (3 * k + 1)) 168).symm
  have hN : 2 ^ (3 * k + 1) - 2 = 7 * 2 + 168 * (2 ^ (3 * k + 1) / 168) := by
    rw [hdec]
    omega
  calc
    ((2 ^ (3 * k + 1) - 2) / 7) % 24 = 2 % 24 :=
      div7_mod24 (2 ^ (3 * k + 1) - 2) 2 (2 ^ (3 * k + 1) / 168) hN
    _ = 2 := by norm_num

/-- ★ GG 商 (2^(3k+1)−2)/7 ≡ 18 mod 24（k 偶，k>0）。 -/
theorem gg_q_mod24_even (k : ℕ) (hk : Even k) (hpos : 0 < k) :
    ((2 ^ (3 * k + 1) - 2) / 7) % 24 = 18 := by
  have hpow : 2 ^ (3 * k + 1) % 168 = 128 := pow2_mod168_even k hk hpos
  have hdec : 2 ^ (3 * k + 1) = 168 * (2 ^ (3 * k + 1) / 168) + 128 := by
    rw [← hpow]
    exact (Nat.div_add_mod (2 ^ (3 * k + 1)) 168).symm
  have hN : 2 ^ (3 * k + 1) - 2 = 7 * 18 + 168 * (2 ^ (3 * k + 1) / 168) := by
    rw [hdec]
    omega
  calc
    ((2 ^ (3 * k + 1) - 2) / 7) % 24 = 18 % 24 :=
      div7_mod24 (2 ^ (3 * k + 1) - 2) 18 (2 ^ (3 * k + 1) / 168) hN
    _ = 18 := by norm_num

/-! ## §6 ★ UU1：GG 族 mod 24 两分支闭式 -/

/-- ★ k 奇 ⇒ Gm k ≡ 3k+2 mod 24（5,11,17,23 分支）。 -/
theorem uu1_odd (k : ℕ) (hk : Odd k) : Gm k % 24 = (3 * k + 2) % 24 := by
  unfold Gm
  have hq := gg_q_mod24_odd k hk
  calc
    ((2 ^ (3 * k + 1) - 2) / 7 + 3 * k) % 24 =
        (((2 ^ (3 * k + 1) - 2) / 7) % 24 + (3 * k) % 24) % 24 := by
      rw [Nat.add_mod]
    _ = (2 + (3 * k) % 24) % 24 := by rw [hq]
    _ = (2 + 3 * k) % 24 := by
      rw [Nat.add_mod]
      norm_num
    _ = (3 * k + 2) % 24 := by
      rw [show 2 + 3 * k = 3 * k + 2 by omega]

/-- ★ k 偶且 k>0 ⇒ Gm k ≡ 3k−6 mod 24（0,6,12,18 分支）。 -/
theorem uu1_even (k : ℕ) (hk : Even k) (hpos : 0 < k) : Gm k % 24 = (3 * k - 6) % 24 := by
  unfold Gm
  have hq := gg_q_mod24_even k hk hpos
  calc
    ((2 ^ (3 * k + 1) - 2) / 7 + 3 * k) % 24 =
        (((2 ^ (3 * k + 1) - 2) / 7) % 24 + (3 * k) % 24) % 24 := by
      rw [Nat.add_mod]
    _ = (18 + (3 * k) % 24) % 24 := by rw [hq]
    _ = (18 + 3 * k) % 24 := by
      rw [Nat.add_mod]
      norm_num
    _ = (3 * k - 6) % 24 := by
      have hk6 : 6 ≤ 3 * k := by
        rcases hk with ⟨t, ht⟩
        rw [ht]
        omega
      rw [show 18 + 3 * k = (3 * k - 6) + 24 by omega]
      simpa using Nat.add_mul_mod_self_left (3 * k - 6) 24 1

/-! ## §7 ★ UU2：mod 24 周期 8 -/

/-- ★ GG 族 m_k mod 24 八实例（5,0,11,6,17,12,23,18 循环）。 -/
theorem uu2_cycle :
    Gm 1 % 24 = 5 ∧ Gm 2 % 24 = 0 ∧ Gm 3 % 24 = 11 ∧ Gm 4 % 24 = 6 ∧
    Gm 5 % 24 = 17 ∧ Gm 6 % 24 = 12 ∧ Gm 7 % 24 = 23 ∧ Gm 8 % 24 = 18 := by
  norm_num [Gm]

/-- ★ 周期 8 引理：k≥1 ⇒ Gm(k+8) ≡ Gm k mod 24（k+8 与 k 同奇偶，
    3(k+8)± 相对 3k± 平移 24，mod 24 不动）。 -/
theorem uu2_period8 (k : ℕ) (hk : 1 ≤ k) : Gm (k + 8) % 24 = Gm k % 24 := by
  by_cases hodd : Odd k
  · have hodd8 : Odd (k + 8) := by
      rcases hodd with ⟨t, rfl⟩
      refine ⟨t + 4, ?_⟩
      omega
    rw [uu1_odd (k + 8) hodd8, uu1_odd k hodd]
    calc
      (3 * (k + 8) + 2) % 24 = ((3 * k + 2) + 24) % 24 := by
        rw [show 3 * (k + 8) + 2 = (3 * k + 2) + 24 by omega]
      _ = (3 * k + 2) % 24 := by
        simpa using Nat.add_mul_mod_self_left (3 * k + 2) 24 1
  · have he : Even k := by
      rcases Nat.even_or_odd k with h | h
      · exact h
      · exact False.elim (hodd h)
    have hke2 : 2 ≤ k := by
      rcases he with ⟨t, rfl⟩
      omega
    have he8 : Even (k + 8) := by
      rcases he with ⟨t, rfl⟩
      refine ⟨t + 4, ?_⟩
      omega
    rw [uu1_even (k + 8) he8 (by omega : 0 < k + 8), uu1_even k he (by omega : 0 < k)]
    calc
      (3 * (k + 8) - 6) % 24 = ((3 * k - 6) + 24) % 24 := by
        rw [show 3 * (k + 8) - 6 = (3 * k - 6) + 24 by omega]
      _ = (3 * k - 6) % 24 := by
        simpa using Nat.add_mul_mod_self_left (3 * k - 6) 24 1

/-! ## §8 ★ UU3：CRT 合成（mod 8 × mod 3 → mod 24） -/

/-- 24 的 8 分解：(x % 24) % 8 = x % 8（8 ∣ 24）。 -/
lemma mod24_mod8 (x : ℕ) : (x % 24) % 8 = x % 8 := by
  exact (calc
    x % 8 = (24 * (x / 24) + x % 24) % 8 := by
      congr 1
      exact (Nat.div_add_mod x 24).symm
    _ = ((24 % 8 * ((x / 24) % 8)) % 8 + (x % 24) % 8) % 8 := by
      rw [Nat.add_mod, Nat.mul_mod]
    _ = ((x % 24) % 8) % 8 := by
      norm_num
    _ = (x % 24) % 8 := by
      exact Nat.mod_eq_of_lt (Nat.mod_lt (x % 24) (by norm_num : 0 < 8))).symm

/-- 24 的 3 分解：(x % 24) % 3 = x % 3（3 ∣ 24）。 -/
lemma mod24_mod3 (x : ℕ) : (x % 24) % 3 = x % 3 := by
  exact (calc
    x % 3 = (24 * (x / 24) + x % 24) % 3 := by
      congr 1
      exact (Nat.div_add_mod x 24).symm
    _ = ((24 % 3 * ((x / 24) % 3)) % 3 + (x % 24) % 3) % 3 := by
      rw [Nat.add_mod, Nat.mul_mod]
    _ = ((x % 24) % 3) % 3 := by
      norm_num
    _ = (x % 24) % 3 := by
      exact Nat.mod_eq_of_lt (Nat.mod_lt (x % 24) (by norm_num : 0 < 3))).symm

/-- ★ mod 8 投影 = II2 遍历闭式（GG 族 m ≡ 3k+2 mod 8，从 UU1 导出）。 -/
theorem uu3_mod8 (k : ℕ) (hk : 1 ≤ k) : Gm k % 8 = (3 * k + 2) % 8 := by
  by_cases hodd : Odd k
  · have hu := uu1_odd k hodd
    calc
      Gm k % 8 = (Gm k % 24) % 8 := by rw [mod24_mod8 (Gm k)]
      _ = ((3 * k + 2) % 24) % 8 := by rw [hu]
      _ = (3 * k + 2) % 8 := mod24_mod8 (3 * k + 2)
  · have he : Even k := by
      rcases Nat.even_or_odd k with h | h
      · exact h
      · exact False.elim (hodd h)
    have hu := uu1_even k he (by omega : 0 < k)
    calc
      Gm k % 8 = (Gm k % 24) % 8 := by rw [mod24_mod8 (Gm k)]
      _ = ((3 * k - 6) % 24) % 8 := by rw [hu]
      _ = (3 * k - 6) % 8 := mod24_mod8 (3 * k - 6)
      _ = (3 * k + 2) % 8 := by
        have hk6 : 6 ≤ 3 * k := by
          rcases he with ⟨t, ht⟩
          rw [ht]
          omega
        calc
          (3 * k - 6) % 8 = ((3 * k - 6) + 8) % 8 := by
            simpa using (Nat.add_mul_mod_self_left (3 * k - 6) 8 1).symm
          _ = (3 * k + 2) % 8 := by
            rw [show (3 * k - 6) + 8 = 3 * k + 2 by omega]

/-- ★ mod 3 投影 = RR2 交替（k 奇 → 2、k 偶 → 0，从 UU1 导出）。 -/
theorem uu3_mod3 (k : ℕ) (hk : 1 ≤ k) : Gm k % 3 = (if k % 2 = 1 then 2 else 0) := by
  by_cases hodd : Odd k
  · have h1 : k % 2 = 1 := by
      rcases hodd with ⟨t, rfl⟩
      rw [Nat.add_mod, Nat.mul_mod]
      norm_num
    have hu := uu1_odd k hodd
    rw [h1]
    calc
      Gm k % 3 = (Gm k % 24) % 3 := by rw [mod24_mod3 (Gm k)]
      _ = ((3 * k + 2) % 24) % 3 := by rw [hu]
      _ = (3 * k + 2) % 3 := mod24_mod3 (3 * k + 2)
      _ = 2 := by
        rw [Nat.add_mod, Nat.mul_mod]
        norm_num
  · have he : Even k := by
      rcases Nat.even_or_odd k with h | h
      · exact h
      · exact False.elim (hodd h)
    have h1 : k % 2 = 0 := by
      rcases he with ⟨t, rfl⟩
      rw [← two_mul t, Nat.mul_mod]
      norm_num
    have hu := uu1_even k he (by omega : 0 < k)
    rw [h1]
    calc
      Gm k % 3 = (Gm k % 24) % 3 := by rw [mod24_mod3 (Gm k)]
      _ = ((3 * k - 6) % 24) % 3 := by rw [hu]
      _ = (3 * k - 6) % 3 := mod24_mod3 (3 * k - 6)
      _ = 0 := by
        have hk2 : 2 ≤ k := by
          rcases he with ⟨t, rfl⟩
          omega
        rw [show 3 * k - 6 = 3 * (k - 2) by omega]
        rw [Nat.mul_mod]
        norm_num

/-- ★ CRT 分解：mod 24 值可投影回 mod 8 / mod 3（lcm(3,8)=24 联合）。 -/
theorem uu3_crt (k : ℕ) (_hk : 1 ≤ k) :
    (Gm k % 24) % 8 = Gm k % 8 ∧ (Gm k % 24) % 3 = Gm k % 3 := by
  constructor
  · exact mod24_mod8 (Gm k)
  · exact mod24_mod3 (Gm k)

/-- ★ lcm(3,8) = 24（CRT 联合模；引用 217 LL1）。 -/
theorem uu3_lcm : Nat.lcm 3 8 = 24 := MUFPF.Period24.ll1_lcm

/-! ## §9 联合主定理 -/

/-- ★★ TT×UU 联合（数值主定理）：偶 Fermat 交集 + 奇偶性 mod 3 + 129 子列
    非 Fermat + GG mod 24 两分支实例 + 周期 8 + CRT 投影 + lcm=24 并置。
    —— 221 ㉑ 的数值主定理。 -/
theorem tt_uu_judgement :
    (∃ t, 3 * t + 1 = 2 ^ 4) ∧
    (2 ^ (2 * 2) % 3 = 1) ∧
    (2 ^ (2 * 2 + 1) % 3 = 2) ∧
    (2 ^ 7 + 1 = 129 ∧ 7 % 3 = 1) ∧
    (Ferm 2 ≠ 129) ∧
    (Gm 1 % 24 = 5 ∧ Gm 8 % 24 = 18) ∧
    (Gm 9 % 24 = Gm 1 % 24) ∧
    ((Gm 3 % 24) % 8 = Gm 3 % 8) ∧
    (Nat.lcm 3 8 = 24) := by
  refine ⟨tt1_backward 2, pow2_even_mod3 2, pow2_odd_mod3 2, tt3_129_sub,
          tt3_129_not_fermat 2, ?_h6, ?_h7, ?_h8, MUFPF.Period24.ll1_lcm⟩
  · norm_num [Gm]
  · simpa [show 9 = 1 + 8 by norm_num] using uu2_period8 1 (by norm_num)
  · exact mod24_mod8 (Gm 3)

end MUFPF.FermatMod24
