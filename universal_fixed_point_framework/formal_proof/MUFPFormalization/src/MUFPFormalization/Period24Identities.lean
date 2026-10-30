import MUFPFormalization.SilentFamilyMechanismIdentities

/-!
# P7-5e-294 ★ 周期 24 联结 + 单位位交集（217 LL/MM）

对应 209 系列（217 ⑰ 周期 24 联结与第二交集检查）：
- ★ LL1：3 与 8 互质（DD2 族下标步进 3 在 8 步内遍历全部 mod 8 类）、
  完整周期 lcm(3,8)=24=lcm(6,8)；DD2 族下标 j_t=1+3t（t=0..7）mod 8 = [1,4,7,2,5,0,3,6]；
- ★ LL2：DD2 族 2 进指数 e_t=2j+4=6t+6（t=0..3）mod 8 = [6,4,2,0]（周期 4）；
  7n+2=2^e+1 且 e≥4 ⇒ n%8=1——n 静默类与指数类脱钩；
- ★ MM1：GG 族 m<129 窗口内 {5,24} 与单位位指数集 {3,4,5,6,7,8} 交集 = {5}
  （无第二交集，负结果确认）；
- ★ KK3：单位位家族值 {9,17,33,65,129,257} 含修正锚点 65（m=6）与闭式常数 129（m=7）。

数值先证伪 20/20，残差 0。诚实边界：LL1/LL2 数论恒等与模算术、
MM1 枚举交集（负结果）、KK3 身份核对——候选层未升定案层。
-/

namespace MUFPF.Period24

open Nat

/-! ## §1 定义 -/

/-- 单位位静默家族指数集 {3,4,5,6,7,8}（值 2^m+1 = {9,17,33,65,129,257}）。 -/
def UnitMember (m : ℕ) : Prop := m = 3 ∨ m = 4 ∨ m = 5 ∨ m = 6 ∨ m = 7 ∨ m = 8

/-! ## §2 ★ LL1：互质 + lcm + 下标遍历 -/

/-- ★ 3 与 8 互质——DD2 族下标步进 3 在 8 步内遍历全部 mod 8 类的前提。 -/
theorem ll1_coprime : Nat.Coprime 3 8 := by
  norm_num

/-- ★ 完整周期 lcm(3,8) = 24 = lcm(6,8)（下标步进 3 与指数步进 6 均与
    Bott 周期 8 的 lcm 为 24——Bott 步进 × 下标步进的满格组合）。 -/
theorem ll1_lcm : Nat.lcm 3 8 = 24 := by
  norm_num

/-- ★ DD2 族下标 j_t = 1+3t（t=0..7）mod 8 遍历 8 类 [1,4,7,2,5,0,3,6]。 -/
theorem ll1_traverse :
    (1 + 3*0) % 8 = 1 ∧ (1 + 3*1) % 8 = 4 ∧ (1 + 3*2) % 8 = 7 ∧
    (1 + 3*3) % 8 = 2 ∧ (1 + 3*4) % 8 = 5 ∧ (1 + 3*5) % 8 = 0 ∧
    (1 + 3*6) % 8 = 3 ∧ (1 + 3*7) % 8 = 6 := by
  norm_num

/-! ## §3 ★ LL2：指数 mod 8 与 n 静默类 -/

/-- ★ DD2 族 2 进指数 e_t = 2j+4 = 6t+6（t=0..3）mod 8 = [6,4,2,0]
    （指数步进 6 ≡ −2 mod 8，周期 4；n 恒 ≡1 mod 8 与指数类无关）。 -/
theorem ll2_exp_mod8 :
    (6*0 + 6) % 8 = 6 ∧ (6*1 + 6) % 8 = 4 ∧ (6*2 + 6) % 8 = 2 ∧ (6*3 + 6) % 8 = 0 := by
  norm_num

/-- ★ n 恒 ≡1 mod 8：7n+2=2^e+1 且 4≤e ⇒ n%8=1——n 静默类与指数类脱钩
    （7n = 2^e−1，2^e≡0 mod 8（e≥4）⇒ 7n≡7 ⇒ n≡1，7 是 8 的模逆）。 -/
theorem ll2_n_silent (n e : ℕ) (he : 4 ≤ e) (h : 7*n + 2 = 2^e + 1) : n % 8 = 1 := by
  have hpow0 : 2^e % 8 = 0 := by
    have hdecomp : 2^e = 2^3 * 2^(e-3) := by
      rw [← pow_add]
      congr 1
      omega
    calc
      2^e % 8 = (2^3 * 2^(e-3)) % 8 := by rw [hdecomp]
      _ = 0 := by
        rw [Nat.mul_mod]
        norm_num
  have hmod8 : (7*n + 2) % 8 = 1 := by
    calc
      (7*n + 2) % 8 = (2^e + 1) % 8 := by rw [h]
      _ = 1 := by
        calc
          (2^e + 1) % 8 = (2^e % 8 + 1 % 8) % 8 := by rw [Nat.add_mod]
          _ = (0 + 1) % 8 := by rw [hpow0]
          _ = 1 := by norm_num
  have h1 : ((7 * n % 8) + 2) % 8 = 1 := by
    calc
      ((7 * n % 8) + 2) % 8 = (7 * n + 2) % 8 := by
        rw [Nat.add_mod]
        norm_num
      _ = 1 := hmod8
  have h7n : 7 * n % 8 = 7 := by
    have hk_lt : 7 * n % 8 < 8 := Nat.mod_lt (7*n) (by norm_num : 0 < 8)
    interval_cases k : 7 * n % 8 <;> simp at h1 <;> first | contradiction | trivial
  have hmul : 7 * n % 8 = 7 * (n % 8) % 8 := by
    rw [Nat.mul_mod]
  have h7m : 7 * (n % 8) % 8 = 7 := by
    rw [← hmul]
    exact h7n
  have hn_lt : n % 8 < 8 := Nat.mod_lt n (by norm_num : 0 < 8)
  interval_cases m : n % 8 <;> simp at h7m <;> first | contradiction | trivial

/-! ## §4 ★ MM1：GG 族与单位位交集（负结果确认） -/

/-- ★ GG 族 m<129 窗口内 {5,24}（k=1,2；第三成员 m₃=155 ≥ 129）。 -/
theorem mm1_gg_lt129 :
    (2^(3*1+1) + 21*1 - 2) / 7 = 5 ∧
    (2^(3*2+1) + 21*2 - 2) / 7 = 24 ∧
    129 ≤ (2^(3*3+1) + 21*3 - 2) / 7 := by
  norm_num

/-- ★ GG 族与单位位交集 = {5}：5 ∈ 单位位、24 ∉ 单位位（无第二交集）。 -/
theorem mm1_intersect :
    UnitMember 5 ∧ ¬ UnitMember 24 := by
  constructor
  · unfold UnitMember
    simp
  · unfold UnitMember
    simp

/-! ## §5 ★ KK3：单位位家族身份 -/

/-- ★ 单位位家族值 = 2^m+1, m=3..8 = {9,17,33,65,129,257}。 -/
theorem kk3_unit_vals :
    2^3 + 1 = 9 ∧ 2^4 + 1 = 17 ∧ 2^5 + 1 = 33 ∧
    2^6 + 1 = 65 ∧ 2^7 + 1 = 129 ∧ 2^8 + 1 = 257 := by
  norm_num

/-- ★ 单位位家族含修正锚点 65（m=6，闭式 129 的 1/65 项）与闭式常数 129（m=7）。 -/
theorem kk3_65_129 : 2^6 + 1 = 65 ∧ 2^7 + 1 = 129 := by
  norm_num

/-! ## §6 联合主定理 -/

/-- ★★ LL×MM 联合（数值主定理）：互质 × lcm=24 × 下标遍历（末点 6）×
    指数遍历（末点 0）× n 静默类（9 实例）× 交集 {5} × 单位位 65/129。
    —— 217 ⑰ 的数值主定理。 -/
theorem ll_mm_judgement :
    Nat.Coprime 3 8 ∧ Nat.lcm 3 8 = 24 ∧
    (1 + 3*7) % 8 = 6 ∧
    (6*3 + 6) % 8 = 0 ∧
    (7*9 + 2 = 2^6 + 1 → 9 % 8 = 1) ∧
    UnitMember 5 ∧ ¬ UnitMember 24 ∧
    2^6 + 1 = 65 ∧ 2^7 + 1 = 129 := by
  constructor
  · exact ll1_coprime
  · constructor
    · exact ll1_lcm
    · constructor
      · norm_num
      · constructor
        · norm_num
        · constructor
          · intro h
            exact ll2_n_silent 9 6 (by norm_num) h
          · constructor
            · exact mm1_intersect.1
            · constructor
              · exact mm1_intersect.2
              · constructor
                · exact kk3_65_129.1
                · exact kk3_65_129.2

end MUFPF.Period24
