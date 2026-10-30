/-
P7-5e-219（⑲ 两族汇合点与余项框架连接）Lean 形式化，2026-10-18。
数值先证伪：scripts/_phase105_p7_5e219_confluence.py（12 项：11 PASS + 1 预期 FAIL=登记勘误）。

覆盖论文 §7.5 第 11 项 ⑲：
- PP1：系数 2 族是系数 1 基础族的约束子列（DD2 子列 ⊂ k_n 因子条件 + 窗口对合 kj(2j+3)=3·2^{2j+1}）
- PP2：两族无汇合（7n+2≠6·2^a 模 7 无解——kj(2j+3)=6·4^j 与 kn 值集无交集的机制核心）
- QQ1：余项 3 周期（3k-2≡1 mod 3）；登记等式 21k-2=7(3k-2) 勘误：真实恒等 21k-2=7(3k-2)+12
- QQ2：21=7·3 框架分解（主模数×种子）
- QQ3：m_k=n_k+3k 加法结构 + 7n_k+2=2^{3k+1} CC3 分母构造性

诚实边界：PP1 子列核对、PP2 模算术无解证明（负结果）、QQ1 模算术观察、QQ2 恒等分解、
QQ3 代数恒等——候选层未升定案层。kj(2j+3)∩kn(n)=∅ 的完整 2 进论证留开放（数值枚举核对）。
-/
import MUFPFormalization.FamilyIndexIdentities
import MUFPFormalization.SilentFamilyMechanismIdentities
import MUFPFormalization.LinearFactorIdentities

namespace MUFPF.Confluence

open MUFPF.FamilyIndex
open MUFPF.SevenPlusMinusOne
open MUFPF.LinearFactor
open MUFPF.SilentFamilyMechanism

/-! ## §1 PP1：系数 2 族是系数 1 基础族的约束子列 -/

/-- PP1a：DD2 子列 ⊂ k_n —— j≡1 (mod 3) ⇒ 存在 n 使 7n+2 = b_j²+1（213 dd2_solution 直接引用）。 -/
theorem pp1_dd2_factor (j : ℕ) (hj : j % 3 = 1) :
    ∃ n, 7 * n + 2 = B j ^ 2 + 1 :=
  dd2_solution j hj

/-- PP1b：窗口对合 ⊂ k_j —— kj(2j+3) = 3·2^{2j+1}（293 yy_same_family 直接引用）。 -/
theorem pp1_window_subset (j : ℕ) :
    kj (2 * j + 3) = 3 * 2 ^ (2 * j + 1) :=
  yy_same_family j

/-! ## §2 PP2：两族无汇合（模 7 无解） -/

/-- helper：8^q ≡ 1 (mod 7)（归纳）。 -/
lemma pow8_mod7 (q : ℕ) : (8 ^ q) % 7 = 1 := by
  induction q with
  | zero => norm_num
  | succ q ih =>
      calc
        (8 ^ (q + 1)) % 7 = (8 ^ q * 8) % 7 := by
          rw [pow_succ]
        _ = ((8 ^ q % 7) * (8 % 7)) % 7 := by
          rw [Nat.mul_mod]
        _ = (1 * 1) % 7 := by
          rw [ih]
        _ = 1 := by rfl

/-- helper：2^{3q} ≡ 1 (mod 7)（(2³)^q = 8^q）。 -/
lemma two_pow3q_mod7 (q : ℕ) : (2 ^ (3 * q)) % 7 = 1 := by
  calc
    (2 ^ (3 * q)) % 7 = ((2 ^ 3) ^ q) % 7 := by
      rw [pow_mul]
    _ = (8 ^ q) % 7 := by norm_num
    _ = 1 := pow8_mod7 q

/-- helper：2^a mod 7 只取 {1,2,4}（2 的 3 周期）。 -/
lemma two_pow_mod7_cases (a : ℕ) :
    (2 ^ a) % 7 = 1 ∨ (2 ^ a) % 7 = 2 ∨ (2 ^ a) % 7 = 4 := by
  have hda : 3 * (a / 3) + a % 3 = a := Nat.div_add_mod a 3
  have hlt : a % 3 < 3 := Nat.mod_lt a (by norm_num : 0 < 3)
  by_cases h0 : a % 3 = 0
  · have ha : a = 3 * (a / 3) := by
      have h2 : 3 * (a / 3) + a % 3 = a := hda
      rw [h0] at h2
      simp at h2
      exact h2.symm
    left
    rw [ha]
    exact two_pow3q_mod7 (a / 3)
  · by_cases h1 : a % 3 = 1
    · have ha : a = 3 * (a / 3) + 1 := by
        have h2 : 3 * (a / 3) + a % 3 = a := hda
        rw [h1] at h2
        exact h2.symm
      right; left
      calc
        (2 ^ a) % 7 = (2 ^ (3 * (a / 3) + 1)) % 7 := by
          exact congrArg (fun x : ℕ => (2 ^ x) % 7) ha
        _ = (2 ^ (3 * (a / 3)) * 2) % 7 := by
          rw [pow_add]
          norm_num
        _ = ((2 ^ (3 * (a / 3)) % 7) * (2 % 7)) % 7 := by rw [Nat.mul_mod]
        _ = (1 * 2) % 7 := by rw [two_pow3q_mod7 (a / 3)]
        _ = 2 := by rfl
    · have h2v : a % 3 = 2 := by omega
      have ha : a = 3 * (a / 3) + 2 := by
        have h2 : 3 * (a / 3) + a % 3 = a := hda
        rw [h2v] at h2
        exact h2.symm
      right; right
      calc
        (2 ^ a) % 7 = (2 ^ (3 * (a / 3) + 2)) % 7 := by
          exact congrArg (fun x : ℕ => (2 ^ x) % 7) ha
        _ = (2 ^ (3 * (a / 3)) * 4) % 7 := by
          rw [pow_add]
          norm_num
        _ = ((2 ^ (3 * (a / 3)) % 7) * (4 % 7)) % 7 := by rw [Nat.mul_mod]
        _ = (1 * 4) % 7 := by rw [two_pow3q_mod7 (a / 3)]
        _ = 4 := by rfl

/-- PP2 核心（模 7 无解）：∀ n a，7n+2 ≠ 6·2^a。
    —— k_{2j+3} = 6·4^j = 6·2^{2j} 落入 6·2^a 形态，与 k_n 的 (7n+2) 因子无交集。 -/
theorem pp2_core (n a : ℕ) : 7 * n + 2 ≠ 6 * 2 ^ a := by
  intro h
  have hL : (7 * n + 2) % 7 = 2 := by
    rw [Nat.add_comm (7 * n) 2]
    rw [Nat.add_mul_mod_self_left]
  have hR : (6 * 2 ^ a) % 7 ≠ 2 := by
    rcases two_pow_mod7_cases a with h1 | h2 | h3
    · calc
        (6 * 2 ^ a) % 7 = ((6 % 7) * (2 ^ a % 7)) % 7 := by
          rw [Nat.mul_mod]
        _ = (6 * 1) % 7 := by
          rw [h1]
        _ ≠ 2 := by norm_num
    · calc
        (6 * 2 ^ a) % 7 = ((6 % 7) * (2 ^ a % 7)) % 7 := by
          rw [Nat.mul_mod]
        _ = (6 * 2) % 7 := by
          rw [h2]
        _ ≠ 2 := by norm_num
    · calc
        (6 * 2 ^ a) % 7 = ((6 % 7) * (2 ^ a % 7)) % 7 := by
          rw [Nat.mul_mod]
        _ = (6 * 4) % 7 := by
          rw [h3]
        _ ≠ 2 := by norm_num
  have hEq : (6 * 2 ^ a) % 7 = (7 * n + 2) % 7 := by
    rw [h]
  have : (6 * 2 ^ a) % 7 = 2 := by
    rw [hEq, hL]
  exact hR this

/-- PP2 推论：若 7n+2 落入 6·2^a 形态则矛盾（kj(2j+3) 值集与 kn 因子无汇合）。 -/
theorem pp2_meet_absurd (n a : ℕ) (h : 7 * n + 2 = 6 * 2 ^ a) : False :=
  pp2_core n a h

/-! ## §3 QQ1：余项 3 周期（含登记勘误） -/

/-- QQ1 勘误：登记等式 21k-2 = 7(3k-2) 不成立（数值证伪，差 12）；
    真实恒等 21k-2 = 7(3k-2) + 12（k≥1）。 -/
theorem qq1_factor12 (k : ℕ) (hk : 1 ≤ k) : 21 * k - 2 = 7 * (3 * k - 2) + 12 := by
  omega

/-- QQ1 核心：3k-2 ≡ 1 (mod 3)（与 ⑫ BB2 "7n+2≡0 mod 3 ⇔ n≡1" 3 周期同源）。 -/
theorem qq1_mod3 (k : ℕ) (hk : 1 ≤ k) : (3 * k - 2) % 3 = 1 := by
  have hk2 : 3 * k - 2 = 3 * (k - 1) + 1 := by omega
  rw [hk2]
  rw [Nat.add_comm (3 * (k - 1)) 1]
  rw [Nat.add_mul_mod_self_left]

/-- QQ1 附加：21k-2 ≡ 5 (mod 7)（余项不被 7 整除——分子余项不可整体吸收进 7 因子）。 -/
theorem qq1_mod7 (k : ℕ) (hk : 1 ≤ k) : (21 * k - 2) % 7 = 5 := by
  have hk2 : 21 * k - 2 = 7 * (3 * k - 1) + 5 := by omega
  rw [hk2]
  rw [Nat.add_comm (7 * (3 * k - 1)) 5]
  rw [Nat.add_mul_mod_self_left]

/-! ## §4 QQ2/QQ3：框架分解与加法结构 -/

/-- QQ2：21 = 7·3（主模数 × 种子）。 -/
theorem qq2_frames : 21 = 7 * 3 := by
  norm_num

/-- CC3 分母（7n+2=2^{3k+1} 的解）：n_k = (2^{3k+1}−2)/7。 -/
def cc3_den (k : ℕ) : ℕ := (2 ^ (3 * k + 1) - 2) / 7

/-- QQ3a：m_k = n_k + 3k（分母 n + 种子×族下标的加法结构；290 gg_m_closed 左式）。 -/
theorem qq3_decomp (k : ℕ) :
    cc3_den k + 3 * k = (2 ^ (3 * k + 1) + 21 * k - 2) / 7 := by
  unfold cc3_den
  exact gg_m_closed k

/-- QQ3b：7·n_k + 2 = 2^{3k+1}（CC3 分母构造性——gg_dvd 商）。 -/
theorem qq3_cc3_n (k : ℕ) : 7 * cc3_den k + 2 = 2 ^ (3 * k + 1) := by
  unfold cc3_den
  have hdiv : 7 ∣ (2 ^ (3 * k + 1) - 2) := gg_dvd k
  rcases hdiv with ⟨c, hc⟩
  have hc2 : (2 ^ (3 * k + 1) - 2) / 7 = c := by
    rw [hc]
    rw [Nat.mul_div_right c (by norm_num : 0 < 7)]
  calc
    7 * ((2 ^ (3 * k + 1) - 2) / 7) + 2 = 7 * c + 2 := by rw [hc2]
    _ = 2 ^ (3 * k + 1) - 2 + 2 := by
      rw [← hc]
    _ = 2 ^ (3 * k + 1) := by
      have ha : 2 ≤ 2 ^ (3 * k + 1) := by
        exact pow_le_pow_right₀ (by norm_num : 1 ≤ 2) (by omega : 1 ≤ 3 * k + 1)
      exact Nat.sub_add_cancel ha

/-! ## §5 联合主定理 -/

/-- ★ PP2+QQ 联合：两族无汇合 + 余项框架连接的联合实例。 -/
theorem confluence_judgement (n a k : ℕ) (hk : 1 ≤ k) :
    7 * n + 2 ≠ 6 * 2 ^ a ∧
    (3 * k - 2) % 3 = 1 ∧
    (21 * k - 2) % 7 = 5 ∧
    21 = 7 * 3 ∧
    7 * cc3_den k + 2 = 2 ^ (3 * k + 1) :=
  ⟨pp2_core n a, qq1_mod3 k hk, qq1_mod7 k hk, by norm_num, qq3_cc3_n k⟩
