/-
P7-5e-213（⑬ 线性因子互锁推广与纯积角色）Lean 形式化，2026-10-18。
数值先证伪：scripts/_phase105_p7_5e213_linear_factor.py（12/12 all_pass，残差 0）。

覆盖论文 §7.5 第 11 项 ⑬：
- DD1：65/63 = b₁²±1 互锁（212 BB3 再现，非新结构）
- DD2：7n+2 = b_j²+1 的解 j≡1 (mod 3)（构造性整除 + 商）
- DD3：CC3 族 7n+2=2^{3k+1}：k 奇 ⇒ 满格平方 b_j²（j=3(k−1)/2）、k 偶 ⇒ 非平方
- EE1：线性因子纯种子积核对（n=4/10/14，kn 直接推论）
- EE2：72=8·9、30=2·3·5、100=(8+2)² 框架组合
- EE3：纯积解 n 分布 {4,10,14} 差序列非等差（枚举核对）

诚实边界：DD2/DD3 代数求解（同余/奇偶）、DD1 恒等再现、EE1 直接推论、EE2/EE3 核对枚举——
候选层未升定案层。
-/
import MUFPFormalization.FamilyIndexIdentities
import MUFPFormalization.SevenPlusMinusOneIdentities

namespace MUFPF.LinearFactor

open MUFPF.SevenPlusMinusOne
open MUFPF.FamilyIndex

/-! ## §1 DD1：65/63 = b₁²±1 互锁（212 BB3 再现） -/

/-- DD1：65 = b₁²+1、63 = b₁²−1，差 2、和 2·b₁² = 2⁷（b₁ = 2³ = 8 满格）。 -/
theorem dd1_interlock :
    B 1 ^ 2 + 1 = 65 ∧ B 1 ^ 2 - 1 = 63 ∧ (B 1 ^ 2 + 1) - (B 1 ^ 2 - 1) = 2 ∧
    (B 1 ^ 2 + 1) + (B 1 ^ 2 - 1) = 2 ^ 7 := by
  norm_num [B]

/-! ## §2 DD2：7n+2 = b_j²+1 的解 j≡1 (mod 3) -/

/-- 核心整除：j≡1 (mod 3) ⇒ 7 | (2^{2j+4} − 1)（2^{2j+4} = 8^{2t+2}，8 ≡ 1 mod 7）。 -/
theorem dd2_dvd (j : ℕ) (hj : j % 3 = 1) : 7 ∣ 2 ^ (2 * j + 4) - 1 := by
  -- 从 j%3=1 提取 j = 3t+1（t = j/3）
  have hdec : j = 3 * (j / 3) + 1 := by
    have h := Nat.div_add_mod j 3
    rw [hj] at h
    exact h.symm
  set t := j / 3
  -- 2^{2j+4} = 8^{2t+2}
  have hpow : 2 ^ (2 * j + 4) = 8 ^ (2 * t + 2) := by
    have hIdx : 2 * j + 4 = 3 * (2 * t + 2) := by
      rw [hdec]
      ring
    rw [hIdx, pow_mul]
    norm_num
  -- 8^{2t+2} ≡ 1 mod 7
  have hmod8 : 8 ^ (2 * t + 2) % 7 = 1 := by
    rw [Nat.pow_mod]
    norm_num
  -- 2^{2j+4} ≡ 1 mod 7
  have h2mod : 2 ^ (2 * j + 4) % 7 = 1 := by
    rw [hpow, hmod8]
  -- 构造商：2^{2j+4} = 7·(2^{2j+4}/7) + 1 ⇒ 7 | (2^{2j+4} − 1)
  have hdivmod := Nat.div_add_mod (2 ^ (2 * j + 4)) 7
  rw [h2mod] at hdivmod
  refine ⟨2 ^ (2 * j + 4) / 7, ?_⟩
  calc
    2 ^ (2 * j + 4) - 1 = (7 * (2 ^ (2 * j + 4) / 7) + 1) - 1 := by
      congr 1
      exact hdivmod.symm
    _ = 7 * (2 ^ (2 * j + 4) / 7) := by
      exact Nat.add_sub_cancel_right (7 * (2 ^ (2 * j + 4) / 7)) 1

/-- ★ DD2 一般化：j≡1 (mod 3) ⇒ ∃n，7n+2 = b_j²+1（充分条件族）。 -/
theorem dd2_solution (j : ℕ) (hj : j % 3 = 1) : ∃ n, 7 * n + 2 = B j ^ 2 + 1 := by
  -- b_j² = 2^{2j+4}
  have hB : B j ^ 2 = 2 ^ (2 * j + 4) := by
    rw [B]
    rw [← pow_mul]
    congr 1
    ring
  have hdvd : 7 ∣ B j ^ 2 - 1 := by
    rw [hB]
    exact dd2_dvd j hj
  rcases hdvd with ⟨q, hq⟩
  refine ⟨q, ?_⟩
  rw [← hq]
  have hgt : 0 < B j ^ 2 := by
    rw [B]
    positivity
  have hge : 1 ≤ B j ^ 2 := Nat.succ_le_of_lt hgt
  omega

/-- DD2 实例：n = 9/585/37449（j = 1/4/7）。 -/
theorem dd2_instances :
    7 * 9 + 2 = B 1 ^ 2 + 1 ∧ 7 * 585 + 2 = B 4 ^ 2 + 1 ∧ 7 * 37449 + 2 = B 7 ^ 2 + 1 := by
  norm_num [B]

/-- DD2 再现：b₄²+1 = 4097 = F₂·D(4) = 17·241。 -/
theorem dd2_f2d4 : (2 ^ (2 ^ 2) + 1) * MUFPF.CoreConstantWindow.Dn 4 = 4097 := by
  norm_num [MUFPF.CoreConstantWindow.Dn]

/-! ## §3 DD3：CC3 族 7n+2=2^{3k+1} 的平方判别 -/

/-- ★ DD3：k 奇（k=2t+1）⇒ 2^{3k+1} = b_{3t}² 满格平方（j = 3(k−1)/2）。 -/
theorem dd3_square (t : ℕ) : 2 ^ (3 * (2 * t + 1) + 1) = (B (3 * t)) ^ 2 := by
  rw [B]
  rw [← pow_mul]
  congr 1
  ring

/-- DD3 实例：n=146 的线性因子 1024 = b₃² = 2^{3·3+1}。 -/
theorem dd3_n146 : 7 * 146 + 2 = 1024 ∧ (B 3) ^ 2 = 1024 := by
  norm_num [B]

/-- ★ DD3：k 偶（k=2t）⇒ ¬∃j，b_j² = 2^{3k+1}（b_j² 指数 2j+4 恒偶 vs 3k+1 奇）。 -/
theorem dd3_nonsquare (t : ℕ) : ¬ ∃ j, (B j) ^ 2 = 2 ^ (3 * (2 * t) + 1) := by
  intro h
  rcases h with ⟨j, hj⟩
  rw [B] at hj
  rw [← pow_mul] at hj
  have hIdx : (j + 2) * 2 = 3 * (2 * t) + 1 := by
    exact Nat.pow_right_injective (by norm_num : 2 ≤ 2) hj
  -- 2(j+2) 偶 vs 6t+1 奇：奇偶矛盾
  omega

/-! ## §4 EE1：线性因子纯种子积核对（n=4/10/14） -/

/-- EE1：n=4 ⇒ 线性因子 30 = 2·15（15 = 3·5 纯种子积）。 -/
theorem ee1_n4 : 7 * 4 + 2 = 2 * 15 ∧ 15 = 3 * 5 := by
  constructor <;> norm_num

/-- EE1：n=10 ⇒ 线性因子 72 = 8·9（9 = 3² 纯种子积）。 -/
theorem ee1_n10 : 7 * 10 + 2 = 8 * 9 ∧ 9 = 3 ^ 2 := by
  constructor <;> norm_num

/-- EE1：n=14 ⇒ 线性因子 100 = 4·25（25 = 5² 纯种子积）。 -/
theorem ee1_n14 : 7 * 14 + 2 = 4 * 25 ∧ 25 = 5 ^ 2 := by
  constructor <;> norm_num

/-- EE1 kn 推论（k_n = 2^{n−4}·线性因子直接推论）：k_4=2·15、k_10=2⁹·9、k_14=2¹²·25。 -/
theorem ee1_kn_cor :
    kn 4 = 2 * 15 ∧ kn 10 = 2 ^ 9 * 9 ∧ kn 14 = 2 ^ 12 * 25 := by
  norm_num [kn]

/-! ## §5 EE2/EE3：框架组合与分布核对 -/

/-- EE2：72 = b₁·(b₁+1)（满格×静默单元）、30 = 2·3·5 纯种子积、100 = (b₁+2)²。 -/
theorem ee2_frames :
    72 = B 1 * (B 1 + 1) ∧ 30 = 2 * 3 * 5 ∧ 100 = (B 1 + 2) ^ 2 := by
  norm_num [B]

/-- EE3：纯积解 n 分布 {4,10,14} 差序列 (6,4) 非等差（枚举核对）。 -/
theorem ee3_diffs : 10 - 4 = 6 ∧ 14 - 10 = 4 ∧ 6 ≠ 4 := by
  norm_num

/-! ## §6 联合主定理 -/

/-- ★ 联合主定理：DD1×DD2×DD3×EE1×EE2×EE3 全 ∀ 并置。 -/
theorem dd_ee_judgement :
    (B 1 ^ 2 + 1 = 65 ∧ B 1 ^ 2 - 1 = 63 ∧ B 1 ^ 2 + 1 - (B 1 ^ 2 - 1) = 2 ∧
     B 1 ^ 2 + 1 + (B 1 ^ 2 - 1) = 2 ^ 7) ∧
    (∀ j, j % 3 = 1 → ∃ n, 7 * n + 2 = B j ^ 2 + 1) ∧
    (7 * 9 + 2 = B 1 ^ 2 + 1 ∧ 7 * 585 + 2 = B 4 ^ 2 + 1 ∧ 7 * 37449 + 2 = B 7 ^ 2 + 1) ∧
    ((2 ^ 2 ^ 2 + 1) * CoreConstantWindow.Dn 4 = 4097) ∧
    (∀ t, 2 ^ (3 * (2 * t + 1) + 1) = (B (3 * t)) ^ 2) ∧
    (7 * 146 + 2 = 1024 ∧ B 3 ^ 2 = 1024) ∧
    (∀ t, ¬ ∃ j, (B j) ^ 2 = 2 ^ (3 * (2 * t) + 1)) ∧
    (7 * 4 + 2 = 2 * 15 ∧ 15 = 3 * 5) ∧
    (7 * 10 + 2 = 8 * 9 ∧ 9 = 3 ^ 2) ∧
    (7 * 14 + 2 = 4 * 25 ∧ 25 = 5 ^ 2) ∧
    (kn 4 = 2 * 15 ∧ kn 10 = 2 ^ 9 * 9 ∧ kn 14 = 2 ^ 12 * 25) ∧
    (72 = B 1 * (B 1 + 1) ∧ 30 = 2 * 3 * 5 ∧ 100 = (B 1 + 2) ^ 2) ∧
    (10 - 4 = 6 ∧ 14 - 10 = 4 ∧ 6 ≠ 4) := by
  exact ⟨dd1_interlock,
    ⟨fun j hj => dd2_solution j hj,
    ⟨dd2_instances,
    ⟨dd2_f2d4,
    ⟨fun t => dd3_square t,
    ⟨dd3_n146,
    ⟨fun t => dd3_nonsquare t,
    ⟨ee1_n4,
    ⟨ee1_n10,
    ⟨ee1_n14,
    ⟨ee1_kn_cor,
    ⟨ee2_frames, ee3_diffs⟩⟩⟩⟩⟩⟩⟩⟩⟩⟩⟩⟩

end MUFPF.LinearFactor
