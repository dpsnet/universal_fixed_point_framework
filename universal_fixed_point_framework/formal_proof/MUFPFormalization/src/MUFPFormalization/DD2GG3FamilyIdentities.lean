import MUFPFormalization.SilentFamilyMechanismIdentities
import MUFPFormalization.SilentClassBinaryIdentities

/-!
# P7-5e-214 ★ FF+GG：DD2 族结构 + CC3 族静默下标

对应 209 系列（214 ⑭）：
- FF1 DD2 族静默类：DD2 族 n = {9,585,37449}（7n+2 = b_j²+1 = 2^(2j+4)+1 的解，
  j ≡ 1 mod 3）全 ≡ 1 mod 8——模推理内核：7n+2 ≡ 1 mod 8 ⇒ n ≡ 1 mod 8
  （7 的 mod 8 乘法逆元是 7，interval_cases 8 分支核对）；
- FF2 分解：n=585 = 9·65（静默单元 × 修正锚点）= 3²·5·13；n=37449 = 3³·19·73
  （73 = 8·9+1 静默类）；
- FF3 平方：4097 = b_4²+1 = 2^12+1（= F_2·D(4)，207 已知再现，n=585 线性因子）；
- GG1 下标：GG（CC3）族 n_k = (2^(3k+1)−2)/7、静默下标 m_k = n_k + 3k
  （k=1..5：m = 5/24/155/1182/9377，290 gg_m_closed 复用）；
- GG2 奇偶：n_k 恒偶（2^(3k+1)−2 = 2·(2^(3k)−1) 偶数，除以奇数 7 保偶）；
  m_k ≡ k mod 2（m = n+3k，3≡1 mod 2）；
- GG3 静默成员：D(n_k) = 2^(m_k) + 1（290 cc3_silent 在 GG 族闭式下的表述——
  7n+2 = 2 的幂 ⇒ D(n) 落静默家族，186『2 进幂集组织』直接体现）。

数值先证伪（勿重跑）：`scripts/_phase102_p7_5e214_ff_gg_dd2_gg3_families.py` + 同目录 json
（2026-10-16，全 ok）。

诚实边界：FF1 为模算术（2^(2j+4) ≡ 0 mod 8）与实例核对；FF2 为分解核对；
FF3 为 207 已知再现；GG1/GG2 为代数恒等（下标定义 + 奇偶判别）；
GG3 为语义连接（186 体现，机制代数内核已形式化）——候选层未升定案层。
-/

namespace MUFPF.DD2GG3Family

open MUFPF.SilentFamilyMechanism
open MUFPF.CoreConstantWindow
open Nat

/-! ## §0 定义 -/

/-- DD2 族 n 闭式：7·n_j + 2 = b_j² + 1 = 2^(2j+4) + 1 的解 n_j = (2^(2j+4) − 1)/7
    （j ≡ 1 mod 3 时整数；实例 j=1,4,7 → n = 9,585,37449）。 -/
def dd2_n (j : ℕ) : ℕ := (2^(2*j + 4) - 1) / 7

/-- 满格平方族 b_j = 2^(j+2)（b_j² = 2^(2j+4)；b_1=8、b_4=64、b_7=512）。 -/
def bj (j : ℕ) : ℕ := 2^(j + 2)

/-- GG（CC3）族 n 闭式：7·n_k + 2 = 2^(3k+1) 的解 n_k = (2^(3k+1) − 2)/7
    （290 gg_dvd 保证整数性）。 -/
def gg_n (k : ℕ) : ℕ := (2^(3*k + 1) - 2) / 7

/-- GG 族静默下标 m_k = n_k + 3k（D(n_k) = 2^(m_k) + 1）。 -/
def gg_m (k : ℕ) : ℕ := gg_n k + 3 * k

/-! ## §1 ★ FF1：DD2 族静默类 -/

/-- ★ 2^(≥3) ≡ 0 mod 8：2^(2j+4) % 8 = 0（2^(2j+4) = 2^3·2^(2j+1)，2j+4 ≥ 4 恒真）。 -/
theorem two_pow_mod8 (j : ℕ) : 2^(2*j + 4) % 8 = 0 := by
  rw [show 2^(2*j + 4) = 2^3 * 2^(2*j + 1) by
    rw [← pow_add]
    congr 1
    omega]
  rw [Nat.mul_mod]
  norm_num

/-- ★★ FF1 模推理内核：7n+2 ≡ 1 mod 8 ⇒ n ≡ 1 mod 8（7 的 mod 8 乘法逆元是 7；
    interval_cases 8 分支逐一核对，仅 n%8=1 分支存活）。 -/
theorem ff1_mod8_reduction (n : ℕ) (h : (7 * n + 2) % 8 = 1) : n % 8 = 1 := by
  rw [Nat.add_mod, Nat.mul_mod] at h
  have hn : n % 8 < 8 := Nat.mod_lt n (by norm_num : 0 < 8)
  interval_cases h8 : n % 8
  · norm_num at h
  · rfl
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h
  · norm_num at h

/-- ★★ FF1 一般机制：线性因子闭式 7n+2 = 2^(2j+4)+1 ⇒ n 落静默类
    （2^(2j+4) ≡ 0 mod 8 → 7n+2 ≡ 1 mod 8 → n ≡ 1 mod 8）。 -/
theorem ff1_linear_to_silent (j n : ℕ) (h : 7 * n + 2 = 2^(2*j + 4) + 1) :
    n % 8 = 1 := by
  apply ff1_mod8_reduction
  rw [h]
  rw [Nat.add_mod]
  rw [two_pow_mod8 j]

/-- ★★ FF1 实例：DD2 族三成员 n={9,585,37449} 均 ≡ 1 mod 8（机制链应用：
    闭式 → 静默类）。 -/
theorem ff1_instances_silent :
    dd2_n 1 % 8 = 1 ∧ dd2_n 4 % 8 = 1 ∧ dd2_n 7 % 8 = 1 := by
  constructor
  · exact ff1_linear_to_silent 1 (dd2_n 1) (by norm_num [dd2_n])
  · constructor
    · exact ff1_linear_to_silent 4 (dd2_n 4) (by norm_num [dd2_n])
    · exact ff1_linear_to_silent 7 (dd2_n 7) (by norm_num [dd2_n])

/-! ## §2 ★ FF2：分解核对 -/

/-- ★ FF2：n=585 = 9·65（静默单元 × 修正锚点）= 3²·5·13；n=9 = 8·1+1 静默单元。 -/
theorem ff2_585 : 585 = 9 * 65 ∧ 585 = 3^2 * 5 * 13 ∧ 9 = 8 * 1 + 1 := by
  norm_num

/-- ★ FF2：n=37449 = 3³·19·73（73 = 8·9+1 静默类成员——n ≡ 1 mod 8 的因子印证）。 -/
theorem ff2_37449 : 37449 = 3^3 * 19 * 73 ∧ 73 = 8 * 9 + 1 := by
  norm_num

/-! ## §3 ★ FF3：满格平方族 -/

/-- ★★ b_j² + 1 = 2^(2j+4) + 1（满格平方族：b_j = 2^(j+2)，j=1→8²、j=4→64²、j=7→512²）。 -/
theorem ff3_bj_square (j : ℕ) : bj j ^ 2 + 1 = 2^(2*j + 4) + 1 := by
  unfold bj
  rw [show (2^(j + 2))^2 = 2^(2 * (j + 2)) by
    rw [← pow_mul]
    congr 1
    omega]
  rw [show 2 * (j + 2) = 2*j + 4 by omega]

/-- ★ FF3：4097 = b_4² + 1 = 2^12 + 1（= F_2·D(4) 为 207 已知再现——n=585 线性因子）。 -/
theorem ff3_4097 : bj 4 ^ 2 + 1 = 4097 ∧ 4097 = 2^12 + 1 := by
  norm_num [bj]

/-! ## §4 ★ GG1：静默下标 m = n + 3k -/

/-- ★★ GG1 一般：m_k 闭式（290 gg_m_closed 在 gg_n/gg_m 定义下的表述）。 -/
theorem gg1_m_closed (k : ℕ) : gg_m k = (2^(3*k + 1) + 21*k - 2) / 7 := by
  unfold gg_m gg_n
  exact gg_m_closed k

/-- ★ GG1 实例：n_k（k=1..5：{2,18,146,1170,9362}——7n+2 = 2 的幂的解）。 -/
theorem gg1_n_instances :
    gg_n 1 = 2 ∧ gg_n 2 = 18 ∧ gg_n 3 = 146 ∧ gg_n 4 = 1170 ∧ gg_n 5 = 9362 := by
  norm_num [gg_n]

/-- ★ GG1 实例：m_k（k=1..5：{5,24,155,1182,9377}——静默家族下标）。 -/
theorem gg1_m_instances :
    gg_m 1 = 5 ∧ gg_m 2 = 24 ∧ gg_m 3 = 155 ∧ gg_m 4 = 1182 ∧ gg_m 5 = 9377 := by
  norm_num [gg_m, gg_n]

/-! ## §5 ★ GG2：奇偶判别 -/

/-- ★★ GG2 一般：n_k 恒偶（2^(3k+1)−2 = 2·(2^(3k)−1) 偶数；除以奇数 7 保偶）。 -/
theorem gg2_n_even (k : ℕ) : gg_n k % 2 = 0 := by
  unfold gg_n
  have hdiv : 7 ∣ (2^(3*k + 1) - 2) := gg_dvd k
  rcases hdiv with ⟨c, hc⟩
  have hmul : 7 * ((2^(3*k + 1) - 2) / 7) = 2^(3*k + 1) - 2 := by
    rw [hc]
    rw [Nat.mul_div_right c (by norm_num : 0 < 7)]
  have hsub : 2^(3*k + 1) - 2 = 2 * (2^(3*k) - 1) := by
    rw [pow_succ]
    rw [mul_comm]
    rw [show 2 * 2^(3*k) - 2 = 2 * 2^(3*k) - 2 * 1 by rw [mul_one]]
    rw [← Nat.mul_sub_left_distrib]
  have hpow : (2^(3*k + 1) - 2) % 2 = 0 := by
    rw [hsub]
    rw [Nat.mul_mod]
    norm_num
  have hmul2 : (7 * ((2^(3*k + 1) - 2) / 7)) % 2 = 0 := by
    rw [hmul]
    exact hpow
  rw [Nat.mul_mod] at hmul2
  norm_num at hmul2
  simpa [Nat.mod_mod] using hmul2

/-- ★★ GG2 一般：m_k ≡ k mod 2（n_k 偶 → m_k = n_k + 3k ≡ 3k ≡ k mod 2）。 -/
theorem gg2_m_parity (k : ℕ) : gg_m k % 2 = k % 2 := by
  unfold gg_m
  rw [Nat.add_mod]
  rw [gg2_n_even]
  rw [zero_add]
  rw [Nat.mod_mod]
  rw [Nat.mul_mod]
  have h3 : 3 % 2 = 1 := by norm_num
  rw [h3]
  rw [one_mul]
  rw [Nat.mod_mod]

/-! ## §6 ★ GG3：静默家族成员 -/

/-- ★★ GG3 机制：D(n_k) = 2^(m_k) + 1——7n+2 = 2 的幂 ⇒ D(n) 落静默家族
    （290 cc3_silent 在 GG 族闭式下的表述，k≥1；186『2 进幂集组织』的代数内核）。 -/
theorem gg3_silent_member (k : ℕ) (hk : 1 ≤ k) :
    MUFPF.CoreConstantWindow.Dn (gg_n k) = 2^(gg_m k) + 1 := by
  have hlin : 7 * gg_n k + 2 = 2^(3*k + 1) := by
    unfold gg_n
    have hdiv : 7 ∣ (2^(3*k + 1) - 2) := gg_dvd k
    rcases hdiv with ⟨c, hc⟩
    have hmul : 7 * ((2^(3*k + 1) - 2) / 7) = 2^(3*k + 1) - 2 := by
      rw [hc]
      rw [Nat.mul_div_right c (by norm_num : 0 < 7)]
    have ha : 2 ≤ 2^(3*k + 1) := by
      exact pow_le_pow_right₀ (by norm_num : 1 ≤ 2) (by omega : 1 ≤ 3*k + 1)
    rw [hmul]
    rw [Nat.sub_add_cancel ha]
  have hcc := cc3_silent (gg_n k) k hk hlin
  exact hcc

/-- ★★ GG3 实例：k=1,2,3 → D(n) = 2^m + 1（2^5+1、2^24+1、2^155+1）。 -/
theorem gg3_family_instances :
    MUFPF.CoreConstantWindow.Dn (gg_n 1) = 2^(gg_m 1) + 1 ∧
    MUFPF.CoreConstantWindow.Dn (gg_n 2) = 2^(gg_m 2) + 1 ∧
    MUFPF.CoreConstantWindow.Dn (gg_n 3) = 2^(gg_m 3) + 1 := by
  constructor
  · exact gg3_silent_member 1 (by norm_num)
  · constructor
    · exact gg3_silent_member 2 (by norm_num)
    · exact gg3_silent_member 3 (by norm_num)

/-! ## §7 联合主定理 -/

/-- ★★ FF×GG 联合（数值主定理）：DD2 族三实例 + FF1 静默 + FF2 分解 +
    FF3 平方 + GG1 下标实例 + GG2 奇偶实例 + GG3 静默成员。 -/
theorem ff_gg_judgement :
    dd2_n 1 = 9 ∧ dd2_n 4 = 585 ∧ dd2_n 7 = 37449 ∧
    (dd2_n 1 % 8 = 1 ∧ dd2_n 4 % 8 = 1 ∧ dd2_n 7 % 8 = 1) ∧
    (585 = 9 * 65 ∧ 37449 = 3^3 * 19 * 73) ∧
    (bj 4 ^ 2 + 1 = 4097 ∧ 4097 = 2^12 + 1) ∧
    (gg_m 1 = 5 ∧ gg_m 2 = 24 ∧ gg_m 3 = 155 ∧ gg_m 4 = 1182 ∧ gg_m 5 = 9377) ∧
    (gg_n 1 % 2 = 0 ∧ gg_n 2 % 2 = 0 ∧ gg_n 3 % 2 = 0) ∧
    (gg_m 1 % 2 = 1 ∧ gg_m 2 % 2 = 0 ∧ gg_m 3 % 2 = 1) ∧
    MUFPF.CoreConstantWindow.Dn (gg_n 1) = 2^(gg_m 1) + 1 := by
  constructor
  · norm_num [dd2_n]
  · constructor
    · norm_num [dd2_n]
    · constructor
      · norm_num [dd2_n]
      · constructor
        · exact ff1_instances_silent
        · constructor
          · norm_num
          · constructor
            · exact ff3_4097
            · constructor
              · norm_num [gg_m, gg_n]
              · constructor
                · norm_num [gg_n]
                · constructor
                  · norm_num [gg_m, gg_n]
                  · exact gg3_silent_member 1 (by norm_num)

end MUFPF.DD2GG3Family
