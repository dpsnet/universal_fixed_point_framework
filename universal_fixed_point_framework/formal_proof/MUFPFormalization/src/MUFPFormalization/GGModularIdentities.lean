import MUFPFormalization.SilentFamilyMechanismIdentities

/-!
# P7-5e-292 ★ GG 族模 8 结构与 CC3 族模类

对应 209 系列（215 II1/II2 模类 + 218 OO1 闭式核对；承接 290 GG 族闭式）：

- ★ cc3_n_mod8：CC3 族（7n+2=2^(3k+1)，k≥1）成员 n 恒 ≡ 2 mod 8——
  II1 模类（2^(3k+1) 含 2³ 因子故 ≡0 mod 8，7n+2≡0 ⇒ 7n≡6 ⇒ n≡2，7⁻¹≡7 mod 8）。
- ★ gm_mod8：GG 族静默下标 m=n+3k 恒 ≡ 3k+2 mod 8——II2 一般形式
  （n≡2 与 3k 线性叠加）。
- ★ gm_traverse：k=1..8 时 m mod 8 = 5,0,3,6,1,4,7,2——**周期 8 遍历 8 类**
  （相邻差 ≡3 mod 8 与 8 互质 ⟹ 遍历）。
- gm_instances：GG 族 m_k 数值 k=1..7 = 5,24,155,1182,9377,74916,599207
  （218 OO1 闭式核对，norm_num 直接计算）。
- ★ gm_diff_exact：相邻差 m_{k+1}−m_k = 2^(3k+1)+3（精确闭式——经 290 gg_dvd
  构造性整除 + Nat 除法减法恒等）。
- ii_judgement：联合主定理（遍历×实例×差分并置）。

数值先证伪 62/62，残差 0。诚实边界：全部代数恒等+模算术；
『周期 8 遍历 8 类 = Bott 周期在 GG 族静默下标层的投影』为语义连接（观察级登记）。
-/

namespace MUFPF.GGModular

open Nat
open MUFPF.SilentFamilyMechanism

/-! ## 定义 -/

/-- GG 族静默下标 m_k = (2^(3k+1)−2)/7 + 3k（290 gg_m_closed 闭式的值函数）。 -/
def Gm (k : ℕ) : ℕ := (2^(3*k+1) - 2) / 7 + 3*k

/-! ## §1 ★ cc3_n_mod8：CC3 族 n ≡ 2 mod 8 -/

/-- ★ k≥1 ∧ 7n+2=2^(3k+1) ⇒ n%8=2——CC3 族成员模类（II1）。
    证明：2^(3k+1)≡0 mod 8（k≥1 时含 2³ 因子）⇒ 7n+2≡0 ⇒ 7n≡6 ⇒ n≡6·7≡42≡2。 -/
theorem cc3_n_mod8 (n k : ℕ) (hk : 1 ≤ k) (h : 7*n + 2 = 2^(3*k+1)) :
    n % 8 = 2 := by
  have hpow0 : 2^(3*k+1) % 8 = 0 := by
    rcases Nat.exists_eq_add_of_le hk with ⟨t, rfl⟩
    rw [show 3 * (1 + t) + 1 = 4 + 3 * t by ring, pow_add]
    rw [Nat.mul_mod]
    norm_num
  have h70 : (7*n + 2) % 8 = 0 := by
    rw [h, hpow0]
  let x := n % 8
  have hxlt : x < 8 := by
    dsimp [x]
    exact Nat.mod_lt n (by norm_num)
  have hxeq : n = 8 * (n / 8) + x := by
    dsimp [x]
    rw [Nat.div_add_mod]
  have hmodx : (7 * x + 2) % 8 = 0 := by
    calc
      (7 * x + 2) % 8 = ((7 * x + 2) + 8 * (7 * (n / 8))) % 8 := by
        rw [Nat.add_mul_mod_self_left (7 * x + 2) 8 (7 * (n / 8))]
      _ = (7 * (8 * (n / 8) + x) + 2) % 8 := by
        congr 1
        ring_nf
      _ = (7 * n + 2) % 8 := by
        rw [← hxeq]
      _ = 0 := h70
  change x = 2
  interval_cases x <;> omega

/-! ## §2 ★ gm_mod8：GG 族 m ≡ 3k+2 mod 8 -/

/-- ★ k≥1 ∧ 7n+2=2^(3k+1) ⇒ (n+3k)%8 = (3k+2)%8——GG 族静默下标模类（II2 一般形式）。 -/
theorem gm_mod8 (n k : ℕ) (hk : 1 ≤ k) (h : 7*n + 2 = 2^(3*k+1)) :
    (n + 3*k) % 8 = (3*k + 2) % 8 := by
  have hn : n % 8 = 2 := cc3_n_mod8 n k hk h
  calc
    (n + 3*k) % 8 = ((n % 8) + (3*k) % 8) % 8 := by rw [Nat.add_mod]
    _ = (2 + (3*k) % 8) % 8 := by rw [hn]
    _ = (2 + 3*k) % 8 := by
      calc
        (2 + (3*k) % 8) % 8 = ((2 % 8) + (3*k) % 8) % 8 := by
          congr 1
        _ = (2 + 3*k) % 8 := by
          conv_rhs => rw [Nat.add_mod]
    _ = (3*k + 2) % 8 := by
      congr 1
      ring

/-! ## §3 ★ gm_traverse：周期 8 遍历 8 类 -/

/-- ★ k=1..8 的 m mod 8 = 5,0,3,6,1,4,7,2——遍历全部 8 类（相邻差 ≡3 与 8 互质）。 -/
theorem gm_traverse :
    Gm 1 % 8 = 5 ∧ Gm 2 % 8 = 0 ∧ Gm 3 % 8 = 3 ∧ Gm 4 % 8 = 6 ∧
    Gm 5 % 8 = 1 ∧ Gm 6 % 8 = 4 ∧ Gm 7 % 8 = 7 ∧ Gm 8 % 8 = 2 := by
  norm_num [Gm]

/-! ## §4 gm_instances：GG 族 m_k 数值（218 OO1 核对） -/

/-- GG 族 m_k 数值 k=1..7 = 5,24,155,1182,9377,74916,599207（OO1 闭式核对）。 -/
theorem gm_instances :
    Gm 1 = 5 ∧ Gm 2 = 24 ∧ Gm 3 = 155 ∧ Gm 4 = 1182 ∧
    Gm 5 = 9377 ∧ Gm 6 = 74916 ∧ Gm 7 = 599207 := by
  norm_num [Gm]

/-! ## §5 ★ gm_diff_exact：相邻差精确闭式 -/

/-- ★ m_{k+1}−m_k = 2^(3k+1)+3——II2 相邻差闭式（经 290 gg_dvd 构造性整除：
    m_{k+1}−m_k = (2^(3k+4)−2^(3k+1))/7 + 3 = 2^(3k+1)·7/7 + 3）。 -/
theorem gm_diff_exact (k : ℕ) : Gm (k+1) - Gm k = 2^(3*k+1) + 3 := by
  unfold Gm
  rcases gg_dvd (k+1) with ⟨c', hc'⟩
  rcases gg_dvd k with ⟨c, hc⟩
  have hgk : (2^(3*k+1) - 2) / 7 = c := by
    rw [hc]
    exact Nat.mul_div_right c (by norm_num : 0 < 7)
  have hgkp : (2^(3*(k+1)+1) - 2) / 7 = c' := by
    rw [hc']
    exact Nat.mul_div_right c' (by norm_num : 0 < 7)
  rw [hgk, hgkp]
  have hge : 2 ≤ 2^(3*k+1) := by
    exact pow_le_pow_right₀ (by norm_num : 1 ≤ 2) (by omega : 1 ≤ 3*k+1)
  have hc' : c' = c + 2^(3*k+1) := by
    have h7 : 7 * (c' - c) = 7 * 2^(3*k+1) := by
      rw [Nat.mul_sub_left_distrib]
      rw [← hc', ← hc]
      rw [show 3*(k+1)+1 = 3*k + 4 by ring]
      rw [show 3*k + 4 = (3*k + 1) + 3 by ring, pow_add, show 2^3 = 8 by norm_num]
      omega
    have hcd : c' - c = 2^(3*k+1) := by
      exact mul_left_cancel₀ (by norm_num : 7 ≠ 0) h7
    omega
  rw [hc']
  omega

/-! ## §6 联合主定理 -/

/-- ★★ 遍历 × 实例 × 差分联合：m mod 8 周期 8 遍历 + m_k 闭式数值 + 相邻差闭式并置。 -/
theorem ii_judgement :
    Gm 1 % 8 = 5 ∧ Gm 2 % 8 = 0 ∧ Gm 3 % 8 = 3 ∧ Gm 8 % 8 = 2 ∧
    Gm 1 = 5 ∧ Gm 4 = 1182 ∧ Gm 7 = 599207 ∧
    Gm 8 - Gm 7 = 2^(3*7+1) + 3 := by
  norm_num [Gm]

end MUFPF.GGModular
