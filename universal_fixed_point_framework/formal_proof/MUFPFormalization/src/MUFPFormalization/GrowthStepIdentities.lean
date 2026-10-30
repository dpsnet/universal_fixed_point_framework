import MUFPFormalization.Period24Identities

/-!
# P7-5e-295 ★ 增长递推步进联结 + 单位位交集（216 JJ/KK）

对应 209 系列（216 ⑯ 增长递推步进联结与单位位交集）：
- ★ JJ1：j 步进 3 ⇔ 2 进指数步进 6=2·3——n 增长因子 2^6=64=b_1² 满格平方
  （分子层恒等 2^(2(j+3)+4)−1 = 64·(2^(2j+4)−1)+63）；
- ★ JJ2：DD2 族 2 进指数 2j+4 ≡ 0 (mod 6)（j≡1 mod 3 时），mod 8 循环 6,4,2,0；
- ★ JJ3：HH 递推系数与常数全框架量（64=b_1²、9=静默单元、63=b_1²−1 窗口宽度）；
- ★ KK1：GG 族与单位位静默家族交集 {m=5}（m₁=5∈、m₂=24∉、m₃=155∉）；
- ★ KK2：下标类与值类脱钩（2^m+1 恒 ≡1 mod 8 对 m≥3——值类恒静默）。

数值先证伪 32/32，残差 0。诚实边界：JJ1 分子层恒等（商层 n_{j+3}=64n_j+9
的 j≡1 mod 3 整除论证登记未做）、JJ2 模算术、JJ3/KK1 身份核对与枚举、
KK2 模算术——候选层未升定案层。
-/

namespace MUFPF.GrowthStep

open Nat
open MUFPF.Period24

/-! ## §1 ★ JJ1：增长因子 64 = b_1² -/

/-- ★ 分子层增长恒等：指数步进 6=2·3 ⇔ 增长因子 2^6=64=b_1² 满格平方
    （2^(2(j+3)+4)−1 = 64·(2^(2j+4)−1)+63；商层 n_{j+3}=64n_j+9 需
    j≡1 mod 3 整除，见诚实边界）。 -/
theorem jj1_mol (j : ℕ) :
    2^(2*(j+3)+4) - 1 = 64 * (2^(2*j+4) - 1) + 63 := by
  have hpow : 2^(2*(j+3)+4) = 64 * 2^(2*j+4) := by
    have hidx : 2*(j+3)+4 = 2*j+4+6 := by omega
    calc
      2^(2*(j+3)+4) = 2^(2*j+4+6) := by rw [hidx]
      _ = 2^(2*j+4) * 2^6 := by rw [pow_add]
      _ = 64 * 2^(2*j+4) := by
        rw [show 2^6 = 64 by norm_num]
        ring
  have ha : 1 ≤ 2^(2*j+4) := by
    exact one_le_pow₀ (by norm_num : 1 ≤ 2)
  calc
    2^(2*(j+3)+4) - 1 = 64 * 2^(2*j+4) - 1 := by rw [hpow]
    _ = 64 * 2^(2*j+4) - 64 + 63 := by omega
    _ = 64 * (2^(2*j+4) - 1) + 63 := by
      congr 1
      rw [show 64 * (2^(2*j+4) - 1) = 64 * 2^(2*j+4) - 64 * 1 by
        exact Nat.mul_sub_left_distrib 64 (2^(2*j+4)) 1]

/-- ★ b_1=8：2^6=64=8^2（增长因子 = b_1² 框架量）。 -/
theorem jj1_pow64 : 2^6 = 64 ∧ 8^2 = 64 := by
  constructor <;> norm_num

/-! ## §2 ★ JJ2：指数步进 6 的模结构 -/

/-- ★ DD2 族 2 进指数 2j+4 ≡ 0 (mod 6)（j≡1 mod 3）——下标步进 3 ↔
    指数步进 6=2·3 的模 6 表述。 -/
theorem jj2_dvd6 (j : ℕ) (hj : j % 3 = 1) : 6 ∣ (2*j + 4) := by
  have hjdiv0 : j = 3 * (j / 3) + j % 3 := (Nat.div_add_mod j 3).symm
  have hjdiv : j = 3 * (j / 3) + 1 := by
    calc
      j = 3 * (j / 3) + j % 3 := hjdiv0
      _ = 3 * (j / 3) + 1 := by rw [hj]
  refine ⟨j / 3 + 1, ?_⟩
  calc
    2*j + 4 = 2*(3*(j/3) + 1) + 4 := by rw [← hjdiv]
    _ = 6*(j/3) + 6 := by ring
    _ = 6*(j/3 + 1) := by ring

/-- ★ e=2j+4 mod 8 对 DD2 族下标 j=1,4,7,10 = [6,4,2,0]（指数步进 6≡−2 mod 8，周期 4）。 -/
theorem jj2_mod8 :
    (2*1 + 4) % 8 = 6 ∧ (2*4 + 4) % 8 = 4 ∧ (2*7 + 4) % 8 = 2 ∧ (2*10 + 4) % 8 = 0 := by
  norm_num

/-! ## §3 ★ JJ3：HH 递推系数全框架量 -/

/-- ★ HH 递推系数与常数全框架量：64=b_1²（增长）、9=8+1（静默单元）、
    63=8²−1（窗口宽度）——⑨ b₁²±1 对的动力学化（递推形式）。 -/
theorem jj3_consts :
    64 = 8^2 ∧ 9 = 8 + 1 ∧ 63 = 8^2 - 1 := by
  constructor <;> norm_num

/-! ## §4 ★ KK1：GG 族与单位位交集 -/

/-- ★ GG 族 m_k 闭式值 k=1..3 = {5,24,155}（第三成员已超单位位窗口 8）。 -/
theorem kk1_gg_vals :
    (2^(3*1+1) + 21*1 - 2) / 7 = 5 ∧
    (2^(3*2+1) + 21*2 - 2) / 7 = 24 ∧
    (2^(3*3+1) + 21*3 - 2) / 7 = 155 := by
  norm_num

/-- ★ GG 族与单位位静默家族交集 = {m=5}：5 ∈ 单位位、24/155 ∉
    （m≥24>8=max 单位位；∀k≥2 无交集的递增性边界登记，未 Lean 化）。 -/
theorem kk1_intersect :
    UnitMember 5 ∧ ¬ UnitMember 24 ∧ ¬ UnitMember 155 := by
  constructor
  · unfold UnitMember
    simp
  · constructor <;> unfold UnitMember <;> simp

/-! ## §5 ★ KK2：下标类与值类脱钩 -/

/-- ★ 值类恒静默：2^m+1 ≡ 1 (mod 8) 对 m≥3（D(n)=2^m+1 恒静默，
    与下标 mod 8 类无关——下标类与值类脱钩）。 -/
theorem kk2_val_mod8 (m : ℕ) (hm : 3 ≤ m) : (2^m + 1) % 8 = 1 := by
  have hpow0 : 2^m % 8 = 0 := by
    have hdecomp : 2^m = 2^3 * 2^(m-3) := by
      rw [← pow_add]
      congr 1
      omega
    calc
      2^m % 8 = (2^3 * 2^(m-3)) % 8 := by rw [hdecomp]
      _ = 0 := by
        rw [Nat.mul_mod]
        norm_num
  calc
    (2^m + 1) % 8 = (2^m % 8 + 1 % 8) % 8 := by rw [Nat.add_mod]
    _ = (0 + 1) % 8 := by
      rw [hpow0]
    _ = 1 := by norm_num

/-! ## §6 联合主定理 -/

/-- ★★ JJ×KK 联合（数值主定理）：分子增长恒等 × 64=b_1² × 指数 6 整除 ×
    mod 8 末点 × HH 框架量 × 交集 {5} × 值类静默。
    —— 216 ⑯ 的数值主定理。 -/
theorem jj_kk_judgement :
    2^(2*(1+3)+4) - 1 = 64 * (2^(2*1+4) - 1) + 63 ∧
    2^6 = 64 ∧ 8^2 = 64 ∧
    (1 % 3 = 1 → 6 ∣ (2*1 + 4)) ∧
    (2*10 + 4) % 8 = 0 ∧
    64 = 8^2 ∧ 9 = 8 + 1 ∧ 63 = 8^2 - 1 ∧
    (2^(3*1+1) + 21*1 - 2) / 7 = 5 ∧
    UnitMember 5 ∧ ¬ UnitMember 24 ∧
    (2^7 + 1) % 8 = 1 := by
  constructor
  · exact jj1_mol 1
  · constructor
    · exact jj1_pow64.1
    · constructor
      · exact jj1_pow64.2
      · constructor
        · intro h
          exact jj2_dvd6 1 h
        · constructor
          · exact jj2_mod8.2.2.2
          · constructor
            · exact jj3_consts.1
            · constructor
              · exact jj3_consts.2.1
              · constructor
                · exact jj3_consts.2.2
                · constructor
                  · exact kk1_gg_vals.1
                  · constructor
                    · exact kk1_intersect.1
                    · constructor
                      · exact kk1_intersect.2.1
                      · exact kk2_val_mod8 7 (by norm_num)

end MUFPF.GrowthStep
