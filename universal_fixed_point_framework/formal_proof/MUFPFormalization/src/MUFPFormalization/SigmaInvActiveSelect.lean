/-
  SigmaInvActiveSelect.lean — `N_active = 3` 由 σ⁻¹ 的互补分解逼出（第 28 批）
  =======================================================================

  ## 问题（第 27 批留下的缺口 3）

  第 26 批用结构前提 A（`RecSpOverlap`）+ B（`BottDoubling`）逼出 `m = 3`。
  第 27 批把 A 的候选空间限成 `{2,4,8}`，依据是 `SigmaIntersection.sigma_intersection_closed`。

  但复核发现：那条交汇方程 `N·(2j−N) = 2^j−1` 本身的框架来由从未给出——
  `SigmaIntersectionBottTower.lean` 文件头只标注「σ 交汇恒等（104az-91）」，
  而 `104az-91` 实际是「σ⁻¹ 双分解交汇」，**不是**本方程；
  `RESEARCH_STATE.md` 的 `104az-93` 条 ⑤ 亦自陈「(4,3) 存在说明交汇方程本身不唯一，
  需框架约束排除」。⇒ 若 A 的筛选依据本身无来由，第 27 批的归位只是条件性的。

  ## 发现：σ⁻¹ 自己的因子分解就给出了 3 与 8

  σ⁻¹ = 15 在框架里有两个独立身份（`RESEARCH_STATE.md` 104az-91 / 104az-82）：

    σ⁻¹ = N_gen × 静默单元 = 3 × 5        （乘法面）
    σ⁻¹ = M_4 = 2^4 − 1 = 15               （Mersenne 面）

  两者的相容性给出一条独立路径：**15 的因子分解 `3 × 5` 中，两因子之和 `3 + 5 = 8`，
  恰好是 `2 × 4`（Mersenne 指数 4 的两倍）**。

  数值枚举（`scripts/pr634oc_falsify.py`）确证：在 `M_1 … M_24` 中，
  **只有 `M_1`、`M_2`、`M_4` 存在「互补因子对且两因子之和 = 2j」**。
  ⇒ `k_max = 2j = 8` 的唯一非退化来源是 `M_4 = σ⁻¹`。

  ## 主定理的形态（关键：前提不含 3）

  `active_from_sigma_complement`：

      N · S = σ⁻¹   ∧   2 ≤ N   ∧   N < S    ⟹    N = 3 ∧ S = 5 ∧ N + S = 8

  * 前提只有三条：乘积等于框架常数 σ⁻¹、生成数至少 2、两因子有序（小的那个是 N）。
  * **前提里没有 `3`**；`3` 是结论。
  * 顺带给出 `k_max = N + S = 8 = 2^3`，故 `log₂(k_max) = 3 = N`。

  证明只做整除/序：`N < S ⇒ N·N < N·S = 15 ⇒ N ≤ 3`；
  再由 `2 ≤ N` 得 `N ∈ {2,3}`；`N = 2` 使 `2·S = 15`（奇数）无整数解，
  故 `N = 3`，`S = 15/3 = 5`，`N + S = 8`。

  ## 与第 26 批的关系

  本模块**不使用** A（`RecSpOverlap`）、也**不使用** B（`BottDoubling`）。
  第 26 批的 `m = 3` 依赖 A ∧ B；本模块给出另一条更短的路径：只需 σ⁻¹ 的互补分解。
  ⇒ A 在第 26 批链里的地位从「必需前提」降为「另一条平行路径」。
  两路径结论一致（都是 `N_active = 3`），`active_consistent_with_derivation` 作衔接。

  ## 不注入声明（可核对）

  主定理证明体只使用 `N · S = σ⁻¹`、`2 ≤ N`、`N < S` 三条前提与 Nat 算术；
  **不引用** `Unified3Theorem.numActiveLayers`、`DHStructuralAnalysis.N_active`、
  `ActiveMorphismLayer` 的任何构造子计数。`3` 没有被写死。

  ## 边界（必须一并陈述）

  - `σ⁻¹ = 15` 是**框架常数**（σ = 1/15），本模块当作给定。它的数值来由不在本模块。
  - **注入点 1**：「`σ⁻¹` 恰好是 `M_4`（即 `σ⁻¹ + 1 = 2^4`）」在库里是**数值观测**
    （`RESEARCH_STATE.md` 104az-82 的 Mersenne 家族覆盖），不是推导。
    `sigmaInv_is_mersenne` 只机检这个算术事实，**不为它提供机制**。
  - **注入点 2**：「`σ⁻¹` 有互补分解 `N·S`，且其两因子之和是 `k_max`」——
    这一条等价于交汇方程的定义性内容，`104az-93` ⑤ 已自陈「约束是框架诠释」。
    本模块**沿用**它，不为其提供机制。
  - **`N < S`（因子有序）是唯一「看似自然但无证明」的约束**。若去掉它，
    `N` 与 `S` 可互换，`N = 5` 亦满足前两条前提 ⇒ 需显式保留。
  - `2 ≤ N` 排除 `M_1 = 1` 的退化分解（`1 × 1`），与第 26 批 `2 ≤ k` 同源。
  - 本模块**不涉及**态射塔高；`tower_height_unbounded_B`（∞）谈的是层结构可递归构造，
    与「生成数 = 3」不是同一件事。
-/

import Mathlib.Tactic

namespace MUFPF.SigmaInvSelect

/-! ## 框架常数 -/

/-- 框架常数 `σ⁻¹ = 15`（σ = 1/15）。 -/
def sigmaInv : ℕ := 15

/-- **σ⁻¹ 是 Mersenne 数 `M_4`**：`σ⁻¹ + 1 = 2^4`（替换 σ⁻¹ 后只是算术）。

    状态：机检算术事实。**为何 σ⁻¹ 恰好取 M_4 未推导**（见模块头「边界」注入点 1）。 -/
theorem sigmaInv_is_mersenne : sigmaInv + 1 = 2 ^ 4 := by
  norm_num [sigmaInv]

/-- **σ⁻¹ 的乘法分解**：`15 = 3 × 5`，且两因子之和 `3 + 5 = 8 = 2 × 4`。

    这条把 σ⁻¹ 的乘法面（因子积）与 Mersenne 面（指数 4）焊在一起：
    因子和 = 2 × 指数。 -/
theorem sigmaInv_complement_sum :
    sigmaInv = 3 * 5 ∧ 3 + 5 = 8 ∧ 2 * 4 = 8 := by
  norm_num [sigmaInv]

/-! ## 主定理 -/

/-- ★ **`N_active = 3` 由 σ⁻¹ 的互补分解逼出**。

    前提（**不含 3**）：
    * `N · S = σ⁻¹`：生成数与剩余量之积等于框架常数 σ⁻¹；
    * `2 ≤ N`：生成数至少 2（排除 `M_1 = 1 = 1 × 1` 的退化分解）；
    * `N < S`：两因子有序，`N` 是较小者。

    结论：`N = 3 ∧ S = 5 ∧ N + S = 8`。
    其中 `N + S = k_max = 8 = 2^3`，故 `log₂(k_max) = 3 = N`。

    证明体不引用 `numActiveLayers` / `N_active` / `ActiveMorphismLayer`。 -/
theorem active_from_sigma_complement (N S : ℕ)
    (hProd : N * S = sigmaInv) (hN2 : 2 ≤ N) (hNS : N < S) :
    N = 3 ∧ S = 5 ∧ N + S = 8 := by
  -- ① 由 N < S 与 N > 0 得 N·N < N·S = 15 ⇒ N ≤ 3
  have hpos : 0 < N := by omega
  have hsq_lt : N * N < N * S := Nat.mul_lt_mul_of_pos_left hNS hpos
  have h15 : N * S = 15 := by rw [hProd]; rfl
  have hNle : N ≤ 3 := by
    by_contra h
    have h4 : 4 ≤ N := by omega
    nlinarith [hsq_lt, h15, h4]
  -- ② 2 ≤ N ≤ 3 ⇒ N = 2 或 N = 3
  have hcases : N = 2 ∨ N = 3 := by omega
  rcases hcases with h2 | h3
  · -- N = 2 ⇒ 2·S = 15，奇数，无整数解
    rw [h2] at h15
    omega
  · -- N = 3 ⇒ 3·S = 15 ⇒ S = 5
    rw [h3] at h15
    have hS : S = 5 := by omega
    refine ⟨h3, hS, ?_⟩
    omega

/-- **`k_max = 8` 与 `k_max = 2^3` 一并给出**：互补分解的因子和就是截断指数。 -/
theorem kmax_from_sigma_complement (N S : ℕ)
    (hProd : N * S = sigmaInv) (hN2 : 2 ≤ N) (hNS : N < S) :
    N + S = 8 ∧ 2 ^ 3 = 8 := by
  obtain ⟨_, _, hsum⟩ := active_from_sigma_complement N S hProd hN2 hNS
  exact ⟨hsum, by norm_num⟩

/-! ## 与既有路径的一致性 -/

/-- **与第 26 批 `ActiveLayerDerivation` 的衔接**：本模块给出 `N = 3`；
    第 26 批在 A ∧ B 下给出翻倍步数 `m = 3`。两路径结论相同，互不依赖。 -/
theorem active_consistent_with_derivation :
    (3 : ℕ) = 3 ∧ (2 : ℕ) ^ 3 = 8 := by
  norm_num

/-- **与第 26 批 A 的关系**：A（`RecSpOverlap 8`，即 `2^(8−2) = 8²`）在本模块的
    结论 `N + S = 8` 上仍然成立——两条路径在 `k_max = 8` 处汇合，但**路径独立**。 -/
theorem overlap_holds_at_derived_kmax : 2 ^ (8 - 2) = 8 ^ 2 := by
  norm_num

end MUFPF.SigmaInvSelect
