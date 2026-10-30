/-
# FermatFamilyIdentities.lean — Fermat 家族身份（P7-5e-281）

形式化目标（199 BB1-BB5 + 200 BB3 资产统一 Lean 化）：

  a_j = 2^{j+1}+1 家族中的 Fermat 子结构：
    §1 Fermat 数家族：F_k = 2^{2^k}+1（k=0..3——3/5/17/257）；
    §2 F_k = a_{2^k−1}（BB2：a_0=3、a_1=5、a_3=17、a_7=257——2^k−1 指数
        = 2^m+1 家族 m 取 2 的幂子列，278 重合）；
    §3 a_j 素数性 ↔ j+1 为 2 的幂（BB1：j=0,1,3,7 素、j=2,4,5,6 合——
        3/5/17/257 素数、9/33/65/129 合数）；
    §4 合数分解（BB4）：9 = 3²、33 = 3·11、65 = 5·13、129 = 3·43；
    §5 ★ 窗口差分（BB3）：b_j−a_j = 2^{j+1}−1 = F_k−2（j=2^k−1，k=1,2,3——
        3/15/255——255 与周期映射重合登记）；
    §6 a_j ≡ 1 mod 8（BB5：j≥2——9/17/33/65/129/257，280 位型重合面）。

★ 诚实边界：
  · 素数性 ↔ j+1 为 2 的幂为描述性观察（200 边界登记），本文件只机器验证 8 个实例；
  · F_2=17、F_3=257 与 278 家族成员数值重合（2^4+1/2^8+1）；
  · 255 与周期映射重合为观察级登记（200 ①）。

数值先证伪记录（先证伪再证明，模式 8）：
  - p7_5e281_pycheck.py（sympy 精确）：35/35 全通过、残差 0。

关系链：import SilentBittypeIdentities（280——传递 279/278，s65_factor 可用）。
-/

import Mathlib.Tactic
import MUFPFormalization.SilentBittypeIdentities

open MUFPF.BottTower

namespace MUFPF.FermatFamily

/-! =========================================================
    §1 Fermat 数家族（F_k = 2^{2^k}+1，k=0..3）
   ========================================================= -/

/-- F_0 = 2^{2⁰}+1 = 3。 -/
theorem ferma0 : 2 ^ (2 ^ 0) + 1 = 3 := by
  norm_num

/-- F_1 = 2^{2¹}+1 = 5。 -/
theorem ferma1 : 2 ^ (2 ^ 1) + 1 = 5 := by
  norm_num

/-- F_2 = 2^{2²}+1 = 17（= 2⁴+1，278 p2_4 数值重合）。 -/
theorem ferma2 : 2 ^ (2 ^ 2) + 1 = 17 := by
  norm_num

/-- F_3 = 2^{2³}+1 = 257（= 2⁸+1，278 p2_8 数值重合）。 -/
theorem ferma3 : 2 ^ (2 ^ 3) + 1 = 257 := by
  norm_num

/-- ★ Fermat 四成员联合（F_0..F_3 = 3/5/17/257）。 -/
theorem fermat_union :
    (2 ^ (2 ^ 0) + 1 = 3) ∧ (2 ^ (2 ^ 1) + 1 = 5) ∧
    (2 ^ (2 ^ 2) + 1 = 17) ∧ (2 ^ (2 ^ 3) + 1 = 257) := by
  norm_num

/-! =========================================================
    §2 F_k = a_{2^k−1}（BB2：a_j = 2^{j+1}+1）
   ========================================================= -/

/-- F_0 = a_0（2^{0+1}+1 = 3）。 -/
theorem fk_a0 : 2 ^ (0 + 1) + 1 = 3 := by
  norm_num

/-- F_1 = a_1（2^{1+1}+1 = 5）。 -/
theorem fk_a1 : 2 ^ (1 + 1) + 1 = 5 := by
  norm_num

/-- F_2 = a_3（2^{3+1}+1 = 17）。 -/
theorem fk_a3 : 2 ^ (3 + 1) + 1 = 17 := by
  norm_num

/-- F_3 = a_7（2^{7+1}+1 = 257）。 -/
theorem fk_a7 : 2 ^ (7 + 1) + 1 = 257 := by
  norm_num

/-- ★ F_k = a_{2^k−1} 四实例联合（指数 2^k−1 = 0/1/3/7）。 -/
theorem fk_union :
    (2 ^ (0 + 1) + 1 = 3) ∧ (2 ^ (1 + 1) + 1 = 5) ∧
    (2 ^ (3 + 1) + 1 = 17) ∧ (2 ^ (7 + 1) + 1 = 257) := by
  norm_num

/-! =========================================================
    §3 a_j 素数性 ↔ j+1 为 2 的幂（BB1）
   ========================================================= -/

/-- a_0 = 3 是素数（j+1=1=2⁰）。 -/
theorem prime3 : Nat.Prime 3 := by
  norm_num

/-- a_1 = 5 是素数（j+1=2=2¹）。 -/
theorem prime5 : Nat.Prime 5 := by
  norm_num

/-- a_3 = 17 是素数（j+1=4=2²）。 -/
theorem prime17 : Nat.Prime 17 := by
  norm_num

/-- a_7 = 257 是素数（j+1=8=2³）。 -/
theorem prime257 : Nat.Prime 257 := by
  norm_num

/-- a_2 = 9 是合数（j+1=3 非 2 的幂——9 = 3²）。 -/
theorem notprime9 : ¬ Nat.Prime 9 := by
  norm_num

/-- a_4 = 33 是合数（j+1=5——33 = 3·11）。 -/
theorem notprime33 : ¬ Nat.Prime 33 := by
  norm_num

/-- a_5 = 65 是合数（j+1=6——65 = 5·13）。 -/
theorem notprime65 : ¬ Nat.Prime 65 := by
  norm_num

/-- a_6 = 129 是合数（j+1=7——129 = 3·43）。 -/
theorem notprime129 : ¬ Nat.Prime 129 := by
  norm_num

/-- ★ 素数成员联合（j+1 为 2 的幂 → 素数：3/5/17/257）。 -/
theorem prime_union : Nat.Prime 3 ∧ Nat.Prime 5 ∧ Nat.Prime 17 ∧ Nat.Prime 257 := by
  constructor
  · exact prime3
  · constructor
    · exact prime5
    · constructor
      · exact prime17
      · exact prime257

/-- ★ 合数成员联合（j+1 非 2 的幂 → 合数：9/33/65/129）。 -/
theorem notprime_union : ¬ Nat.Prime 9 ∧ ¬ Nat.Prime 33 ∧ ¬ Nat.Prime 65 ∧ ¬ Nat.Prime 129 := by
  constructor
  · exact notprime9
  · constructor
    · exact notprime33
    · constructor
      · exact notprime65
      · exact notprime129

/-! =========================================================
    §4 合数分解（BB4）
   ========================================================= -/

/-- 9 = 3²。 -/
theorem c9_sq : 9 = 3 ^ 2 := by
  norm_num

/-- 33 = 3·11。 -/
theorem c33_fac : 33 = 3 * 11 := by
  norm_num

/-- 65 = 5·13（= s65_factor 数值重合）。 -/
theorem c65_fac : 65 = 5 * 13 := by
  norm_num

/-- 129 = 3·43。 -/
theorem c129_fac : 129 = 3 * 43 := by
  norm_num

/-- ★ 合数分解四成员联合。 -/
theorem comp_union : (9 = 3 ^ 2) ∧ (33 = 3 * 11) ∧ (65 = 5 * 13) ∧ (129 = 3 * 43) := by
  norm_num

/-! =========================================================
    §5 窗口差分 b_j−a_j = F_k−2（BB3：j=2^k−1，k=1,2,3）
   ========================================================= -/

/-- b_1−a_1 = 2³−(2²+1) = 3 = F_1−2（k=1）。 -/
theorem wdiff1 : 2 ^ 3 - (2 ^ 2 + 1) = 2 ^ (2 ^ 1) - 1 := by
  norm_num

/-- b_3−a_3 = 2⁵−(2⁴+1) = 15 = F_2−2（k=2）。 -/
theorem wdiff3 : 2 ^ 5 - (2 ^ 4 + 1) = 2 ^ (2 ^ 2) - 1 := by
  norm_num

/-- b_7−a_7 = 2⁹−(2⁸+1) = 255 = F_3−2（k=3——255 周期映射重合）。 -/
theorem wdiff7 : 2 ^ 9 - (2 ^ 8 + 1) = 2 ^ (2 ^ 3) - 1 := by
  norm_num

/-- ★ 窗口差分三成员联合（b_j−a_j = 2^{j+1}−1 = F_k−2：3/15/255）。 -/
theorem wdiff_union :
    (2 ^ 3 - (2 ^ 2 + 1) = 2 ^ (2 ^ 1) - 1) ∧
    (2 ^ 5 - (2 ^ 4 + 1) = 2 ^ (2 ^ 2) - 1) ∧
    (2 ^ 9 - (2 ^ 8 + 1) = 2 ^ (2 ^ 3) - 1) := by
  norm_num

/-! =========================================================
    §6 a_j ≡ 1 mod 8（BB5：j≥2）
   ========================================================= -/

/-- ★ a_j ≡ 1 mod 8 六成员联合（j≥2——280 位型重合面）。 -/
theorem mod8_union :
    (9 % 8 = 1) ∧ (17 % 8 = 1) ∧ (33 % 8 = 1) ∧
    (65 % 8 = 1) ∧ (129 % 8 = 1) ∧ (257 % 8 = 1) := by
  norm_num

end MUFPF.FermatFamily
