/-
  ActiveSilentVieta.lean — 活跃/静默韦达结构 + Mersenne k_max 和分解唯一性 + 奇数塔（104az-191/192）
  =======================================================

  V1：韦达方程根——x² − k_max·x + σ⁻¹ = 0 的两根恰为 {静默 5, 活跃 3}
       x² − 8x + 15 = 0 ⟺ x = 5 ∨ x = 3（活跃+静默 = k_max、活跃×静默 = σ⁻¹ = 对合域+k_max）
  V2：判别式 = k_max² − 4σ⁻¹ = 4 = 幂基²（完全平方 → 整数根保证）
  V3：活跃×静默 = σ⁻¹（15 = 3×5 = 对合域+k_max = 7+8）
  V4：活跃+静默 = k_max（3+5 = 8）
  V5：Mersenne k_max 和分解唯一性（ℕ）——n ≥ 1 ∧ a+b = 8 ∧ ab+1 = 2^n → n = 3 ∨ n = 4
       （等价判别式条件：68 − 2^(n+2) 完全平方 ⟺ n ∈ {3,4}）
  V6：Mersenne 分解存在——(7,1)→M₃、(5,3)→M₄（和均 = k_max）
  V7：奇数塔 {1,3,5,7} Σ = 16 = 幂基^不动点 = Cℓ(3,1) 全态数
  V8：奇数塔全积 = 105 = 禁闭域×静默/幂基 = Λ_QCD/2（42×5/2）
  C1~C15：奇数塔子集闭包——15 个非空子集和/积均落框架量（104az-192）

  先证伪再证明（模式 8）：scripts/falsify_vieta_odd_tower.py 全部通过
  （V1 韦达根 2070 样本零违反；V5 n=1..60 × a=0..8 零违反；子集闭包 15/15 ✓）。

  状态：纯代数恒等（norm_num / ring / omega 闭合，零 sorry）
-/

import Mathlib.Tactic

namespace MUFPF.ActiveSilentVieta

/-! =========================================================
    基础常数
   ========================================================= -/

/-- 代数数 N_gen = 3。 -/
noncomputable def Ngen : ℝ := 3

/-- k_max = 8。 -/
noncomputable def Kmax : ℝ := 8

/-- 幂基 = 2。 -/
noncomputable def Powers : ℝ := 2

/-- 静默单元 = 5。 -/
noncomputable def SilenceUnit : ℝ := 5

/-- 对合域 = 7。 -/
noncomputable def Involution : ℝ := 7

/-- 不动点 = 4。 -/
noncomputable def FixedPoint : ℝ := 4

/-- 禁闭域 = 42。 -/
noncomputable def ConfinementDomain : ℝ := 42

/-- σ⁻¹ = 15（对合域 + k_max；N_gen×静默；不动点²−1）。 -/
noncomputable def SigmaInv : ℝ := 15

/-! =========================================================
    V1：韦达方程根——x² − k_max·x + σ⁻¹ = 0 ⟺ x = 静默 ∨ x = 活跃
   ========================================================= -/

/-- 韦达方程 x² − k_max·x + σ⁻¹ = 0 的两根恰为 {静默 5, 活跃 3}（104az-191 ①）。
    证明：因式分解 (x−5)(x−3) + 零积 + 代入。 -/
theorem vieta_roots : ∀ x : ℝ, x ^ 2 - Kmax * x + SigmaInv = 0 ↔ x = SilenceUnit ∨ x = Ngen := by
  intro x
  constructor
  · intro h
    have hfac : x ^ 2 - Kmax * x + SigmaInv = (x - SilenceUnit) * (x - Ngen) := by
      rw [Kmax, SilenceUnit, Ngen, SigmaInv]
      ring
    have hzero : (x - SilenceUnit) * (x - Ngen) = 0 := by
      simpa [hfac] using h
    rcases mul_eq_zero.mp hzero with hx5 | hx3
    · left
      exact sub_eq_zero.mp hx5
    · right
      exact sub_eq_zero.mp hx3
  · intro h
    rcases h with hx5 | hx3
    · subst x
      norm_num [Kmax, SigmaInv, SilenceUnit]
    · subst x
      norm_num [Kmax, SigmaInv, Ngen]

/-! =========================================================
    V2：判别式 = 幂基²
   ========================================================= -/

/-- 韦达方程判别式 k_max² − 4σ⁻¹ = 64 − 60 = 4 = 幂基²——完全平方保证整数根。 -/
theorem vieta_discriminant : Kmax ^ 2 - 4 * SigmaInv = Powers ^ 2 := by
  norm_num [Kmax, SigmaInv, Powers]

/-! =========================================================
    V3/V4：活跃×静默 = σ⁻¹、活跃+静默 = k_max
   ========================================================= -/

/-- 活跃×静默 = N_gen×静默 = 15 = σ⁻¹（韦达积）。 -/
theorem active_silent_prod : Ngen * SilenceUnit = SigmaInv := by
  norm_num [Ngen, SilenceUnit, SigmaInv]

/-- 活跃+静默 = N_gen+静默 = 8 = k_max（韦达和；104az-84 已立）。 -/
theorem active_silent_sum : Ngen + SilenceUnit = Kmax := by
  norm_num [Ngen, SilenceUnit, Kmax]

/-! =========================================================
    V5：Mersenne k_max 和分解唯一性（ℕ）
   ========================================================= -/

/-- Mersenne 数 M_n = 2^n − 1（以 ab+1 = 2^n 表述）若存在因子分解 ab 且 a+b = k_max = 8，
    则 n = 3 ∨ n = 4 唯一（判别式 68 − 2^(n+2) 完全平方 ⟺ n ∈ {3,4}，104az-191 ②）。
    证明：ab ≤ 16（(a−b)² ≥ 0）→ 2^n ≤ 17 → n ≤ 4；枚举 a ∈ {0..8}、n ∈ {1..4}。 -/
theorem mersenne_kmax_sum_uniqueness (n a b : ℕ) (hn1 : 1 ≤ n) (hab : a + b = 8)
    (hprod : a * b + 1 = 2 ^ n) : n = 3 ∨ n = 4 := by
  have habR : (a : ℝ) + (b : ℝ) = 8 := by exact_mod_cast hab
  have hsq : (0 : ℝ) ≤ ((a : ℝ) - (b : ℝ)) ^ 2 := sq_nonneg _
  have hab16R : (a : ℝ) * (b : ℝ) ≤ 16 := by nlinarith [habR, hsq]
  have hprodR : (a : ℝ) * (b : ℝ) + 1 = (2 : ℝ) ^ n := by exact_mod_cast hprod
  have h2nR17 : (2 : ℝ) ^ n ≤ 17 := by nlinarith [hprodR, hab16R]
  have hn4 : n ≤ 4 := by
    by_contra h
    have h5 : 5 ≤ n := by omega
    have h32R : (32 : ℝ) ≤ (2 : ℝ) ^ n := by
      have hpow : (2 : ℝ) ^ 5 ≤ (2 : ℝ) ^ n := by
        exact pow_le_pow_right₀ (by norm_num : (1 : ℝ) ≤ 2) h5
      norm_num at hpow
      exact hpow
    nlinarith
  have hn_range : n = 1 ∨ n = 2 ∨ n = 3 ∨ n = 4 := by omega
  have ha8 : a ≤ 8 := by omega
  interval_cases a
  all_goals
    norm_num at hprod
    rcases hn_range with rfl | rfl | rfl | rfl
    all_goals norm_num at hprod
    all_goals omega

/-! =========================================================
    V6：Mersenne 分解存在——(7,1)→M₃、(5,3)→M₄（和均 = k_max）
   ========================================================= -/

/-- M₃ 的 k_max 分解：对合域×单位元 = 7 = 2³−1 且 对合域+单位元 = k_max。 -/
theorem mersenne_decomp3 : (Involution : ℝ) * 1 = (2 : ℝ) ^ 3 - 1 ∧ (Involution : ℝ) + 1 = Kmax := by
  constructor <;> norm_num [Involution, Kmax]

/-- M₄ 的 k_max 分解：静默×活跃 = 15 = 2⁴−1 且 静默+活跃 = k_max。 -/
theorem mersenne_decomp4 : (SilenceUnit : ℝ) * Ngen = (2 : ℝ) ^ 4 - 1 ∧ (SilenceUnit : ℝ) + Ngen = Kmax := by
  constructor <;> norm_num [SilenceUnit, Ngen, Kmax]

/-! =========================================================
    V7/V8：奇数塔 {1,3,5,7}
   ========================================================= -/

/-- 奇数塔和：1+3+5+7 = 16 = 幂基^不动点 = Cℓ(3,1) 全态数。 -/
theorem odd_tower_sum : (1 + 3 + 5 + 7 : ℝ) = Powers ^ FixedPoint := by
  norm_num [Powers, FixedPoint]

/-- 奇数塔全积：1×3×5×7 = 105 = 禁闭域×静默/幂基 = Λ_QCD/2（42×5/2，104az-155）。 -/
theorem odd_tower_prod_confinement : (1 * 3 * 5 * 7 : ℝ) = ConfinementDomain * SilenceUnit / Powers := by
  norm_num [ConfinementDomain, SilenceUnit, Powers]

/-- 奇数塔全积显式：1×3×5×7 = 105。 -/
theorem odd_tower_prod_105 : (1 * 3 * 5 * 7 : ℝ) = 105 := by
  norm_num

/-! =========================================================
    子集闭包 C1~C15：奇数塔 15 非空子集和/积均落框架量（104az-192）
   ========================================================= -/

/-- 双元素和：{1,3} → 4 = 不动点。 -/
theorem closure_sum_13 : (1 + 3 : ℝ) = FixedPoint := by
  norm_num [FixedPoint]
/-- 双元素和：{1,5} → 6 = 幂基×N_gen。 -/
theorem closure_sum_15 : (1 + 5 : ℝ) = Powers * Ngen := by
  norm_num [Powers, Ngen]
/-- 双元素和：{1,7} → 8 = k_max。 -/
theorem closure_sum_17 : (1 + 7 : ℝ) = Kmax := by
  norm_num [Kmax]
/-- 双元素和：{3,5} → 8 = k_max。 -/
theorem closure_sum_35 : (3 + 5 : ℝ) = Kmax := by
  norm_num [Kmax]
/-- 双元素和：{3,7} → 10 = 幂基×静默。 -/
theorem closure_sum_37 : (3 + 7 : ℝ) = Powers * SilenceUnit := by
  norm_num [Powers, SilenceUnit]
/-- 双元素和：{5,7} → 12 = N_gen×不动点。 -/
theorem closure_sum_57 : (5 + 7 : ℝ) = Ngen * FixedPoint := by
  norm_num [Ngen, FixedPoint]
/-- 双元素积：{1,3} → 3 = N_gen。 -/
theorem closure_prod_13 : (1 * 3 : ℝ) = Ngen := by
  norm_num [Ngen]
/-- 双元素积：{1,5} → 5 = 静默。 -/
theorem closure_prod_15 : (1 * 5 : ℝ) = SilenceUnit := by
  norm_num [SilenceUnit]
/-- 双元素积：{1,7} → 7 = 对合域。 -/
theorem closure_prod_17 : (1 * 7 : ℝ) = Involution := by
  norm_num [Involution]
/-- 双元素积：{3,5} → 15 = σ⁻¹。 -/
theorem closure_prod_35 : (3 * 5 : ℝ) = SigmaInv := by
  norm_num [SigmaInv]
/-- 双元素积：{3,7} → 21 = N_gen×对合域。 -/
theorem closure_prod_37 : (3 * 7 : ℝ) = Ngen * Involution := by
  norm_num [Ngen, Involution]
/-- 双元素积：{5,7} → 35 = 静默×对合域。 -/
theorem closure_prod_57 : (5 * 7 : ℝ) = SilenceUnit * Involution := by
  norm_num [SilenceUnit, Involution]
/-- 三元素和：{1,3,5} → 9 = b₀ = N_gen²。 -/
theorem closure_trip_sum_135 : (1 + 3 + 5 : ℝ) = Ngen ^ 2 := by
  norm_num [Ngen]
/-- 三元素和：{1,3,7} → 11 = k_max+N_gen。 -/
theorem closure_trip_sum_137 : (1 + 3 + 7 : ℝ) = Kmax + Ngen := by
  norm_num [Kmax, Ngen]
/-- 三元素和：{1,5,7} → 13 = k_max+静默。 -/
theorem closure_trip_sum_157 : (1 + 5 + 7 : ℝ) = Kmax + SilenceUnit := by
  norm_num [Kmax, SilenceUnit]
/-- 三元素和：{3,5,7} → 15 = σ⁻¹。 -/
theorem closure_trip_sum_357 : (3 + 5 + 7 : ℝ) = SigmaInv := by
  norm_num [SigmaInv]
/-- 三元素积：{1,3,5} → 15 = σ⁻¹。 -/
theorem closure_trip_prod_135 : (1 * 3 * 5 : ℝ) = SigmaInv := by
  norm_num [SigmaInv]
/-- 三元素积：{1,3,7} → 21 = N_gen×对合域。 -/
theorem closure_trip_prod_137 : (1 * 3 * 7 : ℝ) = Ngen * Involution := by
  norm_num [Ngen, Involution]
/-- 三元素积：{1,5,7} → 35 = 静默×对合域。 -/
theorem closure_trip_prod_157 : (1 * 5 * 7 : ℝ) = SilenceUnit * Involution := by
  norm_num [SilenceUnit, Involution]
/-- 三元素积：{3,5,7} → 105 = 禁闭域×静默/幂基。 -/
theorem closure_trip_prod_357 : (3 * 5 * 7 : ℝ) = ConfinementDomain * SilenceUnit / Powers := by
  norm_num [ConfinementDomain, SilenceUnit, Powers]
/-- 四元素和：{1,3,5,7} → 16 = 幂基^不动点（= odd_tower_sum）。 -/
theorem closure_quad_sum : (1 + 3 + 5 + 7 : ℝ) = Powers ^ FixedPoint := by
  norm_num [Powers, FixedPoint]
/-- 四元素积：{1,3,5,7} → 105 = 禁闭域×静默/幂基（= odd_tower_prod_confinement）。 -/
theorem closure_quad_prod : (1 * 3 * 5 * 7 : ℝ) = ConfinementDomain * SilenceUnit / Powers := by
  norm_num [ConfinementDomain, SilenceUnit, Powers]

/-! =========================================================
    S267b：分域判据锚——对合 7 非韦达根（2026-10-28）
   =========================================================

  分域假说 C 的机制核心：动力学量 σ 幂次 = 韦达根闭包 {3,5,8}（冻结
  同态 σ³·σ⁵ = σ⁸）；结构量 σ 幂次 = 域常数级联全集 {3,5,7,8}。
  差集 {7} = 分域唯一区分样本。本锚把 "对合 7 非韦达根" 显式化：
  7 不满足韦达方程（根 = {静默 5, 活跃 3}）——对合 = 折叠非增长
  （S135/S158）——不进入冻结代数——但经组装通道（42 = 7×6、
  7/10、35/3）进入结构。 -/

/-- 分域判据：对合 7 不是韦达方程的根（7² − 8·7 + 15 ≠ 0——根
    仅为 {静默 5, 活跃 3}——折叠非增长——不进入冻结核闭包）。 -/
theorem involution_not_vieta_root : Involution ^ 2 - Kmax * Involution + SigmaInv ≠ 0 := by
  norm_num [Involution, Kmax, SigmaInv]

end MUFPF.ActiveSilentVieta
