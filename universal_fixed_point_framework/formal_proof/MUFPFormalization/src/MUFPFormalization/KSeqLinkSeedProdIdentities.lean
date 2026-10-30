import MUFPFormalization.FamilyIndexIdentities
import MUFPFormalization.SilentClassBinaryIdentities

/-!
# P7-5e-212 ★ BB+CC：两 k 序列连接与纯种子积条件

对应 209 系列（212 ⑫）：
- BB1 结构同构：k_j = 2^{j−2}·3（线性因子恒 3）、k_n = 2^{n−4}(7n+2)
  （线性因子 7n+2）——都是"2 进幂 × 线性因子"结构；成员交集为空（枚举）；
- BB2 3 因子机制归因：7n+2 ≡ 0 mod 3 ⇔ n ≡ 1 mod 3（7≡1 mod 3）——AA 命中
  7/13 中 5 个（n=4,7,10,13,16）由 3 的周期性产生；
- BB3 k_9 线性因子 65 与窗口宽度 63 互锁：65 = 7·9+2、63 = 7·9——
  差 2、和 128 = 2^7；
- CC1 纯种子积条件：7n+2 为纯 {2,3,5} 积的 n = {4,10,14}（3/13：
  30=2·3·5、72=2³·3²、100=2²·5²）；
- CC2 mod 7 条件：7n+2 = 2^a·3^b·5^c ⇒ 2^a·3^b·5^c ≡ 2 (mod 7)；
  反向可解性 v ≡ 2 (mod 7) ⟺ ∃n, 7n+2=v（解 n=v/7）。

数值先证伪（勿重跑）：`scripts/_phase102_p7_5e212_kseq_link_seedprod.py` + 同目录 json
（2026-10-16，全 ok）。

诚实边界：BB1 结构同构是形式观察、交集为空是枚举；BB2 为模算术归因；
BB3 为算术恒等；CC1 是枚举（纯积"无其他素因子"不形式化）；
CC2 同余过滤为数论事实（正向形式化、反向可解性形式化、解枚举不形式化）——
候选层未升定案层。
-/

namespace MUFPF.KSeqLinkSeedProd

open MUFPF.FamilyIndex
open Nat

/-! ## §1 ★ BB1：结构同构（2 进幂 × 线性因子） -/

/-- ★ 210/293 同一性：SilentClassBinary.k_n ≡ FamilyIndex.kn（同一定义跨模块引用，
    "两 k 序列"中 k_n 侧的唯一表述）。 -/
theorem bb1_kn_link (n : ℕ) : MUFPF.SilentClassBinary.k_n n = kn n := by
  rfl

/-- ★ k_j 实例表（j=2..7：{3,6,12,24,48,96}，线性因子恒 3）。 -/
theorem bb1_kj_instances :
    kj 2 = 3 ∧ kj 3 = 6 ∧ kj 4 = 12 ∧ kj 5 = 24 ∧ kj 6 = 48 ∧ kj 7 = 96 := by
  unfold kj
  repeat constructor

/-- ★ k_n 实例抽样（n=4,5,9,16；k_9=2080 修正锚点窗口）。 -/
theorem bb1_kn_instances :
    kn 4 = 30 ∧ kn 5 = 74 ∧ kn 9 = 2080 ∧ kn 16 = 466944 := by
  unfold kn
  repeat constructor

/-! ## §2 ★ BB2：3 因子机制归因 -/

/-- ★ 7n+2 ≡ n+2 mod 3（7≡1 mod 3）——归约引理。 -/
theorem bb2_mod3_reduce (n : ℕ) : (7 * n + 2) % 3 = (n + 2) % 3 := by
  have hnum1 : (7 % 3) = 1 := by norm_num
  have hnum2 : (2 % 3) = 2 := by norm_num
  calc
    (7 * n + 2) % 3 = (n % 3 + 2) % 3 := by
      rw [Nat.add_mod, Nat.mul_mod]
      rw [hnum1, hnum2]
      rw [one_mul]
      rw [Nat.mod_mod]
    _ = (n + 2) % 3 := by
      rw [← hnum2]
      rw [← Nat.add_mod]

/-- ★★ 3 因子机制归因：3 ∣ (7n+2) ⇔ 3 ∣ (n+2)（7≡1 mod 3）。 -/
theorem bb2_mod3 (n : ℕ) : 3 ∣ (7 * n + 2) ↔ 3 ∣ (n + 2) := by
  have h := bb2_mod3_reduce n
  constructor
  · intro hd
    rw [Nat.dvd_iff_mod_eq_zero] at hd
    rw [h] at hd
    rw [← Nat.dvd_iff_mod_eq_zero] at hd
    exact hd
  · intro hd
    rw [Nat.dvd_iff_mod_eq_zero] at hd
    rw [← h] at hd
    rw [← Nat.dvd_iff_mod_eq_zero] at hd
    exact hd

/-- ★★ BB2 归因闭合：3 ∣ (7n+2) ⇔ n ≡ 1 mod 3（AA 命中 5 个的周期性根源）。 -/
theorem bb2_div3_iff (n : ℕ) : 3 ∣ (7 * n + 2) ↔ n % 3 = 1 := by
  rw [bb2_mod3]
  rw [Nat.dvd_iff_mod_eq_zero]
  constructor
  · intro h
    rw [Nat.add_mod] at h
    have hn : n % 3 < 3 := Nat.mod_lt n (by norm_num : 0 < 3)
    interval_cases h3 : n % 3
    · norm_num at h
    · rfl
    · norm_num at h
  · intro h
    rw [Nat.add_mod]
    rw [h]

/-- ★ BB2 命中实例（n≡1 mod 3 的 n=4,7,10,13,16——AA 5 个命中）。 -/
theorem bb2_hits :
    3 ∣ (7 * 4 + 2) ∧ 3 ∣ (7 * 7 + 2) ∧ 3 ∣ (7 * 10 + 2) ∧
    3 ∣ (7 * 13 + 2) ∧ 3 ∣ (7 * 16 + 2) := by
  norm_num

/-! ## §3 ★ BB3：k_9 线性因子与窗口宽度互锁 -/

/-- ★★ 65×63 互锁：65=7·9+2、63=7·9——差 2、和 128=2^7（2 的幂）。 -/
theorem bb3_interlock :
    7 * 9 + 2 = 65 ∧ 7 * 9 = 63 ∧ (7 * 9 + 2) + (7 * 9) = 2^7 ∧
    (7 * 9 + 2) - (7 * 9) = 2 := by
  norm_num

/-! ## §4 ★ CC1：纯种子积条件 -/

/-- ★ CC1 命中：7n+2 为纯 {2,3,5} 积的 n = {4,10,14}（30=2·3·5、
    72=2³·3²、100=2²·5²）。 -/
theorem cc1_hits :
    7 * 4 + 2 = 2 * 3 * 5 ∧ 7 * 10 + 2 = 2^3 * 3^2 ∧ 7 * 14 + 2 = 2^2 * 5^2 := by
  norm_num

/-! ## §5 ★ CC2：mod 7 条件与可解性 -/

/-- ★ 线性恒等：7n+2 ≡ 2 mod 7（纯线性，无种子假设）。 -/
theorem cc2_mod7_linear (n : ℕ) : (7 * n + 2) % 7 = 2 := by
  rw [Nat.add_mod, Nat.mul_mod]
  have h0 : (7 % 7) * (n % 7) % 7 = 0 := by norm_num
  rw [h0]

/-- ★★ CC2 正向：7n+2 = 2^a·3^b·5^c ⇒ 2^a·3^b·5^c ≡ 2 mod 7
    （纯种子积必落 2 同余类——同余过滤）。 -/
theorem cc2_mod7 (n a b c : ℕ) (h : 7 * n + 2 = 2^a * 3^b * 5^c) :
    (2^a * 3^b * 5^c) % 7 = 2 := by
  rw [← h]
  exact cc2_mod7_linear n

/-- ★ CC2 反向可解性：v ≡ 2 mod 7 ⇒ ∃ n, 7n+2 = v（同余类必有线性解，
    解 n=v/7）。 -/
theorem cc2_solvable (v : ℕ) (h : v % 7 = 2) : ∃ n, 7 * n + 2 = v := by
  refine ⟨v / 7, ?_⟩
  calc
    7 * (v / 7) + 2 = 2 + 7 * (v / 7) := by omega
    _ = v := by
      rw [← h]
      rw [Nat.add_comm]
      exact Nat.div_add_mod v 7

/-- ★★ CC2 闭合：∃n, 7n+2=v ⟺ v ≡ 2 mod 7（同余过滤的双向形式）。 -/
theorem cc2_iff (v : ℕ) : (∃ n, 7 * n + 2 = v) ↔ v % 7 = 2 := by
  constructor
  · rintro ⟨n, rfl⟩
    exact cc2_mod7_linear n
  · exact cc2_solvable v

/-! ## §6 联合主定理 -/

/-- ★★ BB×CC 联合（数值主定理）：k_9 锚点×65 互锁 + BB2 命中 + BB3 互锁 +
    CC1 命中 + CC2 线性。 -/
theorem bb_cc_judgement :
    MUFPF.SilentClassBinary.k_n 9 = 2^5 * 65 ∧
    (7 * 9 + 2 = 65 ∧ 7 * 9 = 63 ∧ (7 * 9 + 2) + (7 * 9) = 2^7) ∧
    (3 ∣ (7 * 4 + 2) ∧ 3 ∣ (7 * 10 + 2) ∧ 3 ∣ (7 * 16 + 2)) ∧
    (7 * 4 + 2 = 2 * 3 * 5 ∧ 7 * 10 + 2 = 2^3 * 3^2 ∧ 7 * 14 + 2 = 2^2 * 5^2) ∧
    (7 * 10 + 2) % 7 = 2 := by
  constructor
  · exact MUFPF.SilentClassBinary.zz4_k9
  · constructor
    · norm_num
    · constructor
      · norm_num
      · constructor
        · norm_num
        · exact cc2_mod7_linear 10

end MUFPF.KSeqLinkSeedProd
