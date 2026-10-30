/-
# KMaxAlgebra.lean — k_max=8 的代数唯一性（P7-5e-263/264/265 形式化）

形式化目标（P7-5e-263~265 新资产，Unified3Theorem/BottTower 未覆盖的部分）：
  1. k_max = 8 是方程 2^(k-2) = k² 的**唯一**整数解（263：Rec 2 幂与 Sp 平方唯一重合点）
  2. 等价形式 2^m = 2m + 2 的唯一解 m = 3（264：m = 类空数 = N_active）
  3. 邻居基立方恒等 (k_max-3)³ = 2⁷ - 3（5³ = 128 - 3，263 升格）
  4. 因式分解 (k-3)³ - (2k²-3) = (k-8)(k²-3k+3)，k=8 唯一整数根
  5. 静默单元 7 = 2³-1 = k_max-1（= Cl(3) 非平凡基元数、= (1,7) 签名空间维数 q）
  6. (1,7) 签名和 p+q = 8 = k_max（265 跨论文闭合）

数值先证伪记录（先证伪再证明，模式 8）：
  - p7_5e263_kmax_algebra.py：2^(k-2)=k² 扫描 1..32 唯一解 8；2^m=2m+2 唯一解 3；
    (k-3)³=2k²-3 因式分解 (k-8)(k²-3k+3)（sympy 精确）；5³=2⁷-3；2000=2⁴(2·8²-3)。
  - p7_5e264_cl31.py：dim Cl(3)=2³=8、dim Cl⁰(3,1)=8、静默 7=2³-1、C 分子 13=16-3。
  - p7_5e265_paper20_link.py：(1,3)=闵氏、(1,7) p+q=8=k_max、无限塔周期 ℤ/8。
  全部数值通过（残差 0），本文件投入形式化。

关系链：
  BottTower.lean 已形式化 k_max=8 的结构来源（spinorDim(0) 工作基准 + 统一 3 定理 2^N_active）。
  本文件补充其**代数唯一性**：k_max=8 不仅被结构定义，而且是方程 2^(k-2)=k² 的唯一天然数解。
  263 的恒等 2^(k-2)=k² ⟺ (k=2^m 时) 2^m=2m+2 给出 m=3——与 Unified3Theorem.N_active=3 汇合。
-/

import Mathlib.Tactic
import MUFPFormalization.BottTower

open MUFPF.BottTower

namespace MUFPF.KMaxAlgebra

/-! =========================================================
    §1 k_max=8 满足代数自洽方程
   ========================================================= -/

/-- k_max = 8 满足 2^(k-2) = k²（2⁶ = 8²）。 -/
theorem kmax_satisfies_self_consistent :
    2 ^ (k_max - 2) = k_max ^ 2 := by
  rw [k_max_value]; norm_num

/-- 2 幂（Rec 计数）与平方（Sp 几何）在 k_max 处的重合：4·k_max² = 2^k_max。 -/
theorem kmax_four_sq_eq_two_pow :
    4 * k_max ^ 2 = 2 ^ k_max := by
  rw [k_max_value]; norm_num

/-! =========================================================
    §2 唯一性：2^(k-2)=k² 的唯一自然数解是 k=8
   ========================================================= -/

/-- 引理：对 k ≥ 9，2^(k-2) 严格大于 k²（指数增长快于平方）。
    归纳证明，base k=9（128 > 81）。 -/
lemma two_pow_subtwo_gt_sq : ∀ k : ℕ, 9 ≤ k → 2 ^ (k - 2) > k ^ 2 := by
  intro k
  induction k with
  | zero =>
      intro hk; omega
  | succ k ih =>
      intro hk
      by_cases hk8 : k = 8
      · subst k; norm_num
      · have hkge : 9 ≤ k := by omega
        have ih' : 2 ^ (k - 2) > k ^ 2 := ih hkge
        have hpow : 2 ^ (k + 1 - 2) = 2 * 2 ^ (k - 2) := by
          rw [show k + 1 - 2 = k - 2 + 1 by omega]
          rw [pow_succ]
          ring
        rw [hpow]
        have hsq : 2 * k ^ 2 ≥ (k + 1) ^ 2 := by
          nlinarith [sq_nonneg (k - 1)]
        nlinarith

/-- ★ 核心新定理：2^(k-2)=k² 的唯一自然数解是 k = 8（263 判别性资产）。 -/
theorem kmax_unique : ∀ k : ℕ, 2 ≤ k → 2 ^ (k - 2) = k ^ 2 → k = 8 := by
  intro k hk hEq
  by_cases hle : k ≤ 8
  · interval_cases k <;> norm_num at hEq <;> try omega
  · have hge : 9 ≤ k := by omega
    have hgt : 2 ^ (k - 2) > k ^ 2 := two_pow_subtwo_gt_sq k hge
    omega

/-- 推论：k_max 是唯一满足自洽方程的有效截断（为何塔截断在 8：n=16 等塔层不满足）。 -/
theorem kmax_is_unique_solution :
    ∀ k : ℕ, 2 ≤ k → 2 ^ (k - 2) = k ^ 2 → k = k_max := by
  intro k hk hEq
  rw [kmax_unique k hk hEq, k_max_value]

/-! =========================================================
    §3 等价形式：2^m = 2m + 2 的唯一解 m = 3
   ========================================================= -/

/-- 引理：对 m ≥ 4，2^m > 2m + 2。 -/
lemma two_pow_gt_linear : ∀ m : ℕ, 4 ≤ m → 2 ^ m > 2 * m + 2 := by
  intro m
  induction m with
  | zero =>
      intro hm; omega
  | succ m ih =>
      intro hm
      by_cases hm3 : m = 3
      · subst m; norm_num
      · have hmge : 4 ≤ m := by omega
        have ih' : 2 ^ m > 2 * m + 2 := ih hmge
        rw [pow_succ]
        nlinarith

/-- ★ 等价唯一性：2^m = 2m + 2 的唯一自然数解是 m = 3。
    由 k = 2^m 代入 2^(k-2) = k² 消得（263/264：m = 类空数 = N_active）。 -/
theorem power_unique : ∀ m : ℕ, 2 ^ m = 2 * m + 2 → m = 3 := by
  intro m hEq
  by_cases hle : m ≤ 3
  · interval_cases m <;> norm_num at hEq <;> try omega
  · have hge : 4 ≤ m := by omega
    have hgt : 2 ^ m > 2 * m + 2 := two_pow_gt_linear m hge
    omega

/-- 推论：唯一解 m = 3 与 Unified3Theorem 的主动生成层数 N_active = 3 汇合。 -/
theorem power_unique_matches_active_layers :
    3 = Fintype.card MUFPF.Unified3.ActiveMorphismLayer := by
  exact (MUFPF.BottTower.doubling_steps_equal_active_layers).symm

/-! =========================================================
    §4 邻居基立方恒等：5³ = 2⁷ - 3
   ========================================================= -/

/-- 邻居基 5 = k_max - 3（264：2³ - 类空数 3）。 -/
theorem neighbor_base : k_max - 3 = 5 := by
  norm_num [k_max_value]

/-- ★ 邻居基立方恒等：(k_max-3)³ = 2^(k_max-1) - 3，即 5³ = 2⁷ - 3（125 = 128 - 3）。
    263 升格：由 k_max=8 满足 2^(k-2)=k²（⟺ 2^(k-1)=2k²）推出，非观察巧合。 -/
theorem neighbor_cube_identity :
    (k_max - 3) ^ 3 = 2 ^ (k_max - 1) - 3 := by
  norm_num [k_max_value]

/-- 同一恒等的 k² 形式：2·k_max² - 3 = 5³（2000 = 2⁴·5³ 的分母生成基础）。 -/
theorem neighbor_cube_via_sq :
    2 * k_max ^ 2 - 3 = (k_max - 3) ^ 3 := by
  norm_num [k_max_value]

/-- ★ 因式分解：2k² - 3 与 (k-3)³ 之差 = (k-8)(k²-3k+3)，k=8 唯一整数根。 -/
theorem factor_identity (k : ℤ) :
    (k - 3) ^ 3 - (2 * k ^ 2 - 3) = (k - 8) * (k ^ 2 - 3 * k + 3) := by
  ring

/-- 整数根唯一性（复根 3/2 ± i√3/2 非整数，实数根唯一）。 -/
theorem integer_root_unique (k : ℤ) :
    (k - 3) ^ 3 = 2 * k ^ 2 - 3 → k = 8 := by
  intro h
  have hf := factor_identity k
  rw [h] at hf
  have hz : (k - 8) * (k ^ 2 - 3 * k + 3) = 0 := by nlinarith
  have hsq : k ^ 2 - 3 * k + 3 ≠ 0 := by
    -- k² - 3k + 3 无整数零点（判别式 Δ = 9 - 12 < 0，即 (2k-3)² = -3 不可能）
    intro hz0
    have hneg : (2 * k - 3) ^ 2 = -3 := by
      calc
        (2 * k - 3) ^ 2 = 4 * (k ^ 2 - 3 * k + 3) - 3 := by ring
        _ = 4 * 0 - 3 := by rw [hz0]
        _ = -3 := by ring
    have hnn : (2 * k - 3) ^ 2 ≥ 0 := sq_nonneg (2 * k - 3)
    nlinarith
  cases mul_eq_zero.mp hz with
  | inl hl => omega
  | inr hr => exact False.elim (hsq hr)

/-! =========================================================
    §5 静默单元 7 与 (1,7) 签名（265 跨论文闭合）
   ========================================================= -/

/-- 静默单元 7 = 2³ - 1 = k_max - 1（Cl(3) 非平凡基元数：8 基元减标量）。 -/
theorem silence_unit : 2 ^ 3 - 1 = k_max - 1 := by
  norm_num [k_max_value]

/-- 静默单元数值：7。 -/
theorem silence_unit_value : 2 ^ 3 - 1 = 7 := by
  norm_num

/-- 三类空组合数：2³ = 8 = k_max（Cl(3,1) 类空生成元组合，264）。 -/
theorem cl3_dim_eq_kmax : 2 ^ 3 = k_max := by
  norm_num [k_max_value]

/-- 偶子代数维度：dim Cl⁰(3,1) = 2^(4-1) = 8 = k_max（洛伦兹旋量代数，264）。 -/
theorem cl01_even_dim_eq_kmax : 2 ^ (4 - 1) = k_max := by
  norm_num [k_max_value]

/-- C 分子：dim Cl(3,1) - 3 = 2⁴ - 3 = 13（2k_max - 3，264 结构量对照）。 -/
theorem c_numerator_cl31 : 2 ^ 4 - 3 = 2 * k_max - 3 := by
  norm_num [k_max_value]

/-- δ∞ 分母：7·8 = 56（非平凡基元 × 总基元，264/265）。 -/
theorem delta_inf_denominator : (2 ^ 3 - 1) * 2 ^ 3 = 56 := by
  norm_num

/-- ★ (1,7) 签名（paper20 谱间隙截止）：空间维数 q = 7 = 静默单元 = k_max - 1。 -/
theorem sign17_space_dim : 7 = k_max - 1 := by
  rw [k_max_value]

/-- (1,7) 签名和：p + q = 8 = k_max（265：无限塔 Level 0 的签名和 = 截断）。 -/
theorem sign17_sum_eq_kmax : 1 + 7 = k_max := by
  rw [k_max_value]

/-- C 的分母：2^7 = dim Cl(7) = 2^(k_max-1)（(1,7) 纯空间子代数维度，265）。 -/
theorem c_denominator_cl7 : 2 ^ 7 = 2 ^ (k_max - 1) := by
  rw [k_max_value]

end MUFPF.KMaxAlgebra
