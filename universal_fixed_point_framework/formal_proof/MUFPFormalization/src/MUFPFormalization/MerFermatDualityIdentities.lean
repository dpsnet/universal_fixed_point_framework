/-
# MerFermatDualityIdentities.lean — 三层语义与 Mersenne/Fermat 对偶（P7-5e-285）

形式化目标（204 资产 KK+LL 统一 Lean 化）：

  KK ★ 窗口三层语义（窗口 = 家族段 × 塔段 × 静默段）：
    §1 三段恒等：家族段（Fermat 起边界 2^{j+1}+1）+ 宽度（Mersenne 2^{j+1}−1）= 塔段（2 幂 2^{j+2}）
        —— 284 jj_sum/jj_width 全链一般定理直接引用；宽度 = 终边界 − 起边界；
    §2 静默段登记：c_j = 8·k_j+1（{25,49,97,193,385,769}）+ 根窗口 c_1=9 对照；
  LL ★ Mersenne/Fermat ±1 对偶（一般 n）：
    §3 三恒等：和 = 2 幂塔 (2^n+1)+(2^n−1)=2^{n+1}；差 = 2；积 = M_{2n} (2^n+1)(2^n−1)=2^{2n}−1
        —— 本层核心增量（一般 n 新证，n=1..7 实例化）；
    §4 ★ 65/63 ±1 对（a_5=65=2^6+1 修正锚点 vs w_5=63=2^6−1 宽度：和=2^7、差=2、积=M_12）；
  §5 素数骨架对照：Fermat 素数骨架 m=2^k 截止（F_0..F_4 素、F_5 合——283 已证）vs
        Mersenne 指数奇素数（2^3−1/2^5−1/2^7−1 素 vs 合数指数——284 ii3_union 已证）；
  §6 ★ 联合主定理 kk_ll_judgement：KK 三段恒等 × LL 三恒等全部 ∀ 化并置。

★ 诚实边界：
  · KK 三层"语义指认"（家族段↔Rec 加法面、塔段↔Sp 乘法面、静默段↔对偶投影）为语义层，
    本模块只形式化其代数恒等（候选层登记，非机制推导）；
  · LL5 65/63 ±1 对为描述性观察（65 修正锚点 = b₁²+1 已在 193/275 层登记）；
  · 素数骨架对照为经典数论实例（Fermat 素性、Mersenne 指数素数性）。

数值先证伪记录（先证伪再证明，模式 8）：
  - p7_5e285_pycheck.py（sympy 精确）：79/79 全通过、残差 0。

关系链：import BottPeriodStepIdentities（284——传递 WindowShiftFermat4Identities/283、PeriodMapUnification/282、FermatFamily/281）。
-/

import Mathlib.Tactic
import MUFPFormalization.BottPeriodStepIdentities

namespace MUFPF.MerFermatDuality

/-! =========================================================
    §1 KK ★ 窗口三层语义（全链一般定理——284 直接引用）
   ========================================================= -/

/-- KK ★ 三层语义核心：家族段 + 宽度 = 塔段，且宽度 = 终边界 − 起边界（284 jj_judgement 引用）。 -/
theorem kk_three_layer (j : ℕ) :
    (2 ^ (j + 1) + 1) + (2 ^ (j + 1) - 1) = 2 ^ (j + 2) ∧
    2 ^ (j + 2) - (2 ^ (j + 1) + 1) = 2 ^ (j + 1) - 1 :=
  MUFPF.BottPeriodStep.jj_judgement j

/-- KK 三层语义之"宽度 = Mersenne"恒等（w_j = 2^{j+1}−1，全 j）。 -/
theorem kk_width_mersenne (j : ℕ) : 2 ^ (j + 1) - 1 = 2 ^ (j + 1) - 1 := rfl

/-- KK 静默段登记：c_j = 8·k_j+1（{25,49,97,193,385,769}——284 jj_silent_instances 引用）。 -/
theorem kk_silent_instances :
    (8 * 3 + 1 = 25) ∧ (8 * 6 + 1 = 49) ∧ (8 * 12 + 1 = 97) ∧
    (8 * 24 + 1 = 193) ∧ (8 * 48 + 1 = 385) ∧ (8 * 96 + 1 = 769) :=
  MUFPF.BottPeriodStep.jj_silent_instances

/-- KK 根窗口对照：c_1 = 8·1+1 = 9（窗口 1 位型例外）。 -/
theorem kk_root_c1 : 8 * 1 + 1 = 9 :=
  MUFPF.BottPeriodStep.jj_root_c1

/-- KK 窗口实例（j=2..7：a_j/w_j/b_j 三段取值，w_j={7,15,31,63,127,255}）。 -/
theorem kk_layer_instances :
    ((2 ^ 3 + 1) + (2 ^ 3 - 1) = 2 ^ 4) ∧ ((2 ^ 4 + 1) + (2 ^ 4 - 1) = 2 ^ 5) ∧
    ((2 ^ 5 + 1) + (2 ^ 5 - 1) = 2 ^ 6) ∧ ((2 ^ 6 + 1) + (2 ^ 6 - 1) = 2 ^ 7) ∧
    ((2 ^ 7 + 1) + (2 ^ 7 - 1) = 2 ^ 8) ∧ ((2 ^ 8 + 1) + (2 ^ 8 - 1) = 2 ^ 9) := by
  norm_num

/-! =========================================================
    §2 LL ★ Mersenne/Fermat ±1 对偶（一般 n——本层核心增量）
   ========================================================= -/

/-- LL1 ★ 和恒等：(2^n+1)+(2^n−1) = 2^{n+1}（Fermat 型 + Mersenne 型 = 2 幂塔）。 -/
theorem ll1_sum (n : ℕ) : (2 ^ n + 1) + (2 ^ n - 1) = 2 ^ (n + 1) := by
  have hge : 1 ≤ 2 ^ n := by
    exact Nat.succ_le_of_lt (by positivity : 0 < 2 ^ n)
  have hpow : 2 ^ (n + 1) = 2 * 2 ^ n := by
    calc
      2 ^ (n + 1) = 2 ^ n * 2 := by rw [pow_succ]
      _ = 2 * 2 ^ n := by rw [Nat.mul_comm]
  calc
    (2 ^ n + 1) + (2 ^ n - 1) = (2 ^ n + 1) + 2 ^ n - 1 := by
      exact (Nat.add_sub_assoc hge (2 ^ n + 1)).symm
    _ = (2 ^ n + 2 ^ n) + 1 - 1 := by omega
    _ = (2 * 2 ^ n) + 1 - 1 := by
      have h : 2 ^ n + 2 ^ n = 2 * 2 ^ n := by ring
      rw [h]
    _ = 2 ^ (n + 1) + 1 - 1 := by rw [hpow]
    _ = 2 ^ (n + 1) := by
      exact Nat.add_sub_cancel (2 ^ (n + 1)) 1

/-- LL2 ★ 差恒等：(2^n+1)−(2^n−1) = 2（±1 对偶间距恒定 2）。 -/
theorem ll2_diff (n : ℕ) : (2 ^ n + 1) - (2 ^ n - 1) = 2 := by
  have hge : 1 ≤ 2 ^ n := by
    exact Nat.succ_le_of_lt (by positivity : 0 < 2 ^ n)
  omega

/-- LL3 ★ 积恒等：(2^n+1)·(2^n−1) = 2^{2n}−1 = M_{2n}（±1 对偶积 = 下标翻倍 Mersenne）。 -/
theorem ll3_prod (n : ℕ) : (2 ^ n + 1) * (2 ^ n - 1) = 2 ^ (2 * n) - 1 := by
  have hpow2 : 2 ^ (2 * n) = 2 ^ n * 2 ^ n := by
    rw [show 2 * n = n + n by omega, pow_add]
  calc
    (2 ^ n + 1) * (2 ^ n - 1) = (2 ^ n + 1) * 2 ^ n - (2 ^ n + 1) * 1 := by
      exact Nat.mul_sub_left_distrib (2 ^ n + 1) (2 ^ n) 1
    _ = (2 ^ n + 1) * 2 ^ n - (2 ^ n + 1) := by simp
    _ = (2 ^ n * 2 ^ n + 2 ^ n) - (2 ^ n + 1) := by
      have h : (2 ^ n + 1) * 2 ^ n = 2 ^ n * 2 ^ n + 2 ^ n := by ring
      rw [h]
    _ = 2 ^ (2 * n) + 2 ^ n - (2 ^ n + 1) := by
      rw [hpow2]
    _ = 2 ^ (2 * n) - 1 := by omega

/-- ★ LL 三恒等联合（和=2 幂塔、差=2、积=M_{2n}，全 n）。 -/
theorem ll_duality (n : ℕ) :
    (2 ^ n + 1) + (2 ^ n - 1) = 2 ^ (n + 1) ∧
    (2 ^ n + 1) - (2 ^ n - 1) = 2 ∧
    (2 ^ n + 1) * (2 ^ n - 1) = 2 ^ (2 * n) - 1 := by
  constructor
  · exact ll1_sum n
  · constructor
    · exact ll2_diff n
    · exact ll3_prod n

/-- LL ±1 对偶实例（n=1..7：{3,1}/{5,3}/{9,7}/{17,15}/{33,31}/{65,63}/{129,127}）。 -/
theorem ll_instances :
    (2 ^ 1 + 1 = 3) ∧ (2 ^ 1 - 1 = 1) ∧ (2 ^ 2 + 1 = 5) ∧ (2 ^ 2 - 1 = 3) ∧
    (2 ^ 3 + 1 = 9) ∧ (2 ^ 3 - 1 = 7) ∧ (2 ^ 4 + 1 = 17) ∧ (2 ^ 4 - 1 = 15) ∧
    (2 ^ 5 + 1 = 33) ∧ (2 ^ 5 - 1 = 31) ∧ (2 ^ 6 + 1 = 65) ∧ (2 ^ 6 - 1 = 63) ∧
    (2 ^ 7 + 1 = 129) ∧ (2 ^ 7 - 1 = 127) := by
  norm_num

/-! =========================================================
    §3 LL5 ★ 65/63 ±1 对（修正锚点 × 宽度）
   ========================================================= -/

/-- LL5 ★：a_5 = 2^6+1 = 65（修正锚点）。 -/
theorem ll5_a5 : 2 ^ 6 + 1 = 65 := by
  norm_num

/-- LL5 ★：w_5 = 2^6−1 = 63（窗口 5 宽度）。 -/
theorem ll5_w5 : 2 ^ 6 - 1 = 63 := by
  norm_num

/-- ★ LL5 对联合：65/63 和=2^7、差=2、积=2^{12}−1=M_12。 -/
theorem ll5_pair :
    (2 ^ 6 + 1 = 65) ∧ (2 ^ 6 - 1 = 63) ∧ (65 - 63 = 2) ∧
    (65 * 63 = 2 ^ 12 - 1) ∧ (65 + 63 = 2 ^ 7) := by
  norm_num

/-! =========================================================
    §4 素数骨架对照（Fermat m=2^k 截止 vs Mersenne 指数奇素数）
   ========================================================= -/

/-- Fermat 素数骨架：F_0..F_4 全素（3/5/17/257/65537）。 -/
theorem fermat_prime_instances :
    Nat.Prime (2 ^ 1 + 1) ∧ Nat.Prime (2 ^ 2 + 1) ∧ Nat.Prime (2 ^ 4 + 1) ∧
    Nat.Prime (2 ^ 8 + 1) ∧ Nat.Prime (2 ^ 16 + 1) := by
  norm_num

/-- Fermat 骨架截止：F_5 = 2^32+1 = 4294967297 合数（Euler——283 f5_composite 引用）。 -/
theorem fermat_comp_F5 : ¬ Nat.Prime (2 ^ 32 + 1) := by
  rw [show 2 ^ 32 + 1 = 4294967297 by norm_num]
  exact MUFPF.WindowShiftFermat4.f5_composite

/-- Fermat 骨架联合：F_0..F_4 素 + F_5 合（m=2^k 截止 16）。 -/
theorem fermat_skeleton_union :
    (Nat.Prime (2 ^ 1 + 1) ∧ Nat.Prime (2 ^ 2 + 1) ∧ Nat.Prime (2 ^ 4 + 1) ∧
     Nat.Prime (2 ^ 8 + 1) ∧ Nat.Prime (2 ^ 16 + 1)) ∧ ¬ Nat.Prime (2 ^ 32 + 1) := by
  constructor
  · exact fermat_prime_instances
  · exact fermat_comp_F5

/-- Mersenne 指数奇素数：2^n−1 素数 ↔ 指数素数实例（284 ii3_union 引用）。 -/
theorem mersenne_prime_contrast :
    Nat.Prime (2 ^ 3 - 1) ∧ Nat.Prime (2 ^ 5 - 1) ∧ Nat.Prime (2 ^ 7 - 1) ∧
    ¬ Nat.Prime (2 ^ 4 - 1) ∧ ¬ Nat.Prime (2 ^ 6 - 1) ∧ ¬ Nat.Prime (2 ^ 8 - 1) :=
  MUFPF.BottPeriodStep.ii3_union

/-- ★ 素数骨架对照：Fermat 素数骨架（指数 2 幂、m=16 截止）vs Mersenne 指数奇素数。 -/
theorem prime_skeleton_contrast :
    ((Nat.Prime (2 ^ 1 + 1) ∧ Nat.Prime (2 ^ 2 + 1) ∧ Nat.Prime (2 ^ 4 + 1) ∧
      Nat.Prime (2 ^ 8 + 1) ∧ Nat.Prime (2 ^ 16 + 1)) ∧ ¬ Nat.Prime (2 ^ 32 + 1)) ∧
    (Nat.Prime (2 ^ 3 - 1) ∧ Nat.Prime (2 ^ 5 - 1) ∧ Nat.Prime (2 ^ 7 - 1) ∧
     ¬ Nat.Prime (2 ^ 4 - 1) ∧ ¬ Nat.Prime (2 ^ 6 - 1) ∧ ¬ Nat.Prime (2 ^ 8 - 1)) := by
  constructor
  · exact fermat_skeleton_union
  · exact MUFPF.BottPeriodStep.ii3_union

/-! =========================================================
    §5 ★★ 联合主定理：KK 三段恒等 × LL 三恒等
   ========================================================= -/

/-- ★★ 204 核心结论 Lean 化：窗口 = 家族段×塔段×静默段（KK）与 Mersenne/Fermat ±1 对偶（LL）全 ∀ 并置。 -/
theorem kk_ll_judgement :
    (∀ j : ℕ, (2 ^ (j + 1) + 1) + (2 ^ (j + 1) - 1) = 2 ^ (j + 2)) ∧
    (∀ j : ℕ, 2 ^ (j + 2) - (2 ^ (j + 1) + 1) = 2 ^ (j + 1) - 1) ∧
    (∀ n : ℕ, (2 ^ n + 1) + (2 ^ n - 1) = 2 ^ (n + 1)) ∧
    (∀ n : ℕ, (2 ^ n + 1) - (2 ^ n - 1) = 2) ∧
    (∀ n : ℕ, (2 ^ n + 1) * (2 ^ n - 1) = 2 ^ (2 * n) - 1) := by
  constructor
  · exact MUFPF.BottPeriodStep.jj_sum
  · constructor
    · exact MUFPF.BottPeriodStep.jj_width
    · constructor
      · exact ll1_sum
      · constructor
        · exact ll2_diff
        · exact ll3_prod

end MUFPF.MerFermatDuality
