/-
第 41 批（候选 A）：d_H 的三条路径 —— 哪一条的前提还站着

====================================================================
起因
--------------------------------------------------------------------
第 39 批把「层数 = ⌈d_H⌉ = 3」登记为一条规则（`hausdorff_ceil_three`），
第 40 批给出 σ⁻¹ = M_4 = 15 的 Mersenne 身份。本批（候选 A）回扫早期
分形谱去递归理论的 6 份大文档，目的是找「比 ⌈d_H⌉ 更强的层数论证」。

回扫结果（pr634op_scan.txt / pr634op_dh.txt）
--------------------------------------------------------------------
1. 早期文档里 `N_active` 出现次数 = 0（8 份文件全部为 0），
   「层数」一词最多 11 次。⇒「层数」不是从分形谱研究继承来的概念。
2. 早期 `分形谱去递归理论严格证明.md` L1471-1473 的 d_H 是
   Weierstrass 函数的 Hausdorff 维数 d_H = 2 − log a / log b（实测 3.4650、
   2.9861 等连续值）；同文件 L1301-1302 的 d_H 又是 Hausdorff 距离。
3. 库内 `IFSFractal.lean` L221-232 把 d_H 严格定义为 Moran 方程
   Σ c_i^{d_H} = 1 的唯一正解（`structure HausdorffDimensionSolution`），
   并诚实登记 L216-218：一般 IFS 下 d_H 可远大于 n（实测 d ≈ 6.58 > 2）。
4. 库内 `SpinorSilenceBranch.lean` L15/L29 的 d_H 却是「熵」：
   `S₄ = e^{−d_H} = 1/15`、`熵 H = ln 15 = d_H`，而 `S4 := (1:ℝ)/15` 是字面量定义。
   ⇒ 同一符号 d_H 承载了两个不同的数学对象。

库内既有的两条 d_H = ln 15 路径
--------------------------------------------------------------------
路径 ①（Moran 方程，`DHStructuralAnalysis.lean` L71-89 + L117-123）：
    B = N_active × N_total = 3 × 5 = 15
    r = e⁻¹
    ⇒ B · r^{d_H} = 1 ⇒ 15 · (e⁻¹)^{d_H} = 1 ⇒ d_H = ln 15
  ※ 该文件 L45 / L88 自标「条件定理」；L103-108 又自登记：
    `N_total := 5`「来自 𝐒𝐩 严格 4-范畴（对象层 + 4 个态射层）」，
    且 `B_eq_15` 只是「层对计数」。
  ⇒ **第 37 批已机检证伪「Sp 是严格 4-范畴」**（`SpFiveLayer.lean` L33、
    `SpTowerWitness.lean` L110/L126 给出非退化见证）。
  ⇒ 路径 ① 的**结构前提已倒**，只剩算术。

路径 ②（维数对偶，`CoherenceToBranching.lean` L352 / L366-368）：
    d_H = ln(2·k_max − 1) = ln 15
  ※ 该文件 L353-354 诚实登记：这些恒等式本身是初等算术事实（norm_num 可判），
    其「结构对偶」解释属于物理论证，不在形式化范围内。
  ※ 但此式**不经过 N_total**，只经过 k_max = 8；
    而 k_max = 8 在第 32 批（k_max = f·b = b³）与第 40 批（k_max = f²/2 = 2^(f−1)）
    都有推导。

本批裁决
--------------------------------------------------------------------
三条路径到 15：
    (I)  2·k_max − 1        （对偶，只用 k_max）
    (II) N_active × N_total （分支配积，只用两个计数；前提已倒）
    (III) f² − 1           （不动点，只用 f；第 40 批 Mersenne）
(I) 与 (III) 在 k_max = 2^(f−1) 下是同一个式子（2·2^(f−1) − 1 = 2^f − 1 = f² − 1）。
(II) 的三个因子也全是 f 的函数：N_active = f − 1、N_total = f + 1。
⇒ **三条路径全部归结到同一个 f = 4，唯一剩余注入点是 `f`。**

诚实边界（本文件不声称的）
--------------------------------------------------------------------
1. 不证「N_total = 5 必然」——本文件只能证 3 × 5 = 15 这个算术事实；
   `N_total := 5` 的**口径**（把对象层计入）与其「严格 4-范畴」依据
   已被第 37 批证伪，本文件只作登记。
2. 不证「r = e⁻¹ 必然」——路径 ① 的第二个前提取自「信息论最优静默因子（定理 R1）」，
   本文件不重证 R1。
3. 不证 `f = 4` 必然（f² = 2^f 有非退化解 f = 4；全域解集未证，见第 39 批补正）。
4. d_H 的「熵」解释（S₄ = e^{−d_H}）与「Moran 维数」解释（Σ c_i^{d_H} = 1）
   在本文件中不做统一——本文件只处理数值层 d_H = ln 15 的两侧恒等式。
-/

import Mathlib.Tactic
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import MUFPFormalization.FifteenMersenneRoot

open MUFPF.OneRoot
open MUFPF.FifteenMersenne

namespace MUFPF.DHThree

/-! ## §1 三条路径到同一个 15 -/

/-- 路径 (I)：对偶式的底数 2·k_max − 1 = 15（k_max = 8）。 -/
theorem dual_base_eq_fifteen : ((2 : ℝ) * 8 - 1) = 15 := by norm_num

/-- 路径 (II)：分支配积 N_active × N_total = 3 × 5 = 15。 -/
theorem branch_base_eq_fifteen : ((3 : ℝ) * 5) = 15 := by norm_num

/-- 路径 (III)：不动点平方减一 f² − 1 = 4² − 1 = 15。 -/
theorem fixedpoint_base_eq_fifteen : ((4 : ℝ) ^ 2 - 1) = 15 := by norm_num

/-- 路径 (I) 到 d_H：`Real.log (2·k_max − 1) = Real.log 15`。 -/
theorem dh_via_duality : Real.log ((2 : ℝ) * 8 - 1) = Real.log 15 :=
  congrArg Real.log dual_base_eq_fifteen

/-- 路径 (II) 到 d_H：`Real.log (N_active × N_total) = Real.log 15`。 -/
theorem dh_via_branch_product : Real.log ((3 : ℝ) * 5) = Real.log 15 :=
  congrArg Real.log branch_base_eq_fifteen

/-- 路径 (III) 到 d_H：`Real.log (f² − 1) = Real.log 15`。 -/
theorem dh_via_fixedpoint : Real.log ((4 : ℝ) ^ 2 - 1) = Real.log 15 :=
  congrArg Real.log fixedpoint_base_eq_fifteen

/-- ★ 三条路径给出同一个 d_H。 -/
theorem dh_three_sources_agree :
    Real.log ((2 : ℝ) * 8 - 1) = Real.log 15 ∧
    Real.log ((3 : ℝ) * 5) = Real.log 15 ∧
    Real.log ((4 : ℝ) ^ 2 - 1) = Real.log 15 :=
  ⟨dh_via_duality, dh_via_branch_product, dh_via_fixedpoint⟩

/-- ★ (I) 与 (III) 是同一个式子：2·2^3 − 1 = 2^4 − 1，且 2^4 − 1 = 4² − 1。 -/
theorem dual_eq_fixedpoint_base :
    ((2 : ℝ) * (2 : ℝ) ^ 3 - 1) = ((4 : ℝ) ^ 2 - 1) := by norm_num

/-! ## §2 d_H 与 σ 的关系 -/

/-- `σ = e^{−d_H}`（`S4 = 1/15` 的指数写法）。 -/
theorem sigma_eq_exp_neg_dh : ((1 : ℝ) / 15) = Real.exp (-(Real.log 15)) := by
  rw [Real.exp_neg, Real.exp_log (by norm_num : (0 : ℝ) < 15)]
  norm_num

/-- ★ σ 的直接来源：`1/(f² − 1) = 1/15`，不经过 d_H。 -/
theorem sigma_from_fixedpoint : ((1 : ℝ) / ((4 : ℝ) ^ 2 - 1)) = 1 / 15 := by norm_num

/-- ★ σ 的另一种来源：`σ⁻¹ = N_active × N_total` 时 `σ = 1/(3·5)`。 -/
theorem sigma_from_branch_product : ((1 : ℝ) / ((3 : ℝ) * 5)) = 1 / 15 := by norm_num

/-- ★ `σ⁻¹ = e^{d_H}`（σ 与 d_H 互为指数/对数）。 -/
theorem sigma_inv_eq_exp_dh : (15 : ℝ) = Real.exp (Real.log 15) :=
  (Real.exp_log (by norm_num : (0 : ℝ) < 15)).symm

/-! ## §3 层数：三条路径都给出 ⌈d_H⌉ = 3 -/

/-- 路径 (I) 给出的层数。 -/
theorem hausdorff_layer_via_dual : Int.ceil (Real.log ((2 : ℝ) * 8 - 1)) = 3 := by
  rw [dh_via_duality]
  exact hausdorff_ceil_three

/-- 路径 (II) 给出的层数。 -/
theorem hausdorff_layer_via_branch : Int.ceil (Real.log ((3 : ℝ) * 5)) = 3 := by
  rw [dh_via_branch_product]
  exact hausdorff_ceil_three

/-- 路径 (III) 给出的层数。 -/
theorem hausdorff_layer_via_fixedpoint2 : Int.ceil (Real.log ((4 : ℝ) ^ 2 - 1)) = 3 := by
  rw [dh_via_fixedpoint]
  exact hausdorff_ceil_three

/-- ★ 三条路径的层数一致。 -/
theorem layer_three_from_all_paths :
    Int.ceil (Real.log ((2 : ℝ) * 8 - 1)) = 3 ∧
    Int.ceil (Real.log ((3 : ℝ) * 5)) = 3 ∧
    Int.ceil (Real.log ((4 : ℝ) ^ 2 - 1)) = 3 :=
  ⟨hausdorff_layer_via_dual, hausdorff_layer_via_branch, hausdorff_layer_via_fixedpoint2⟩

/-! ## §4 路径的输入依赖：谁能独立于已倒前提 -/

/-- 路径 (I) 的输入只有 k_max：式子里没有 N_active、没有 N_total。 -/
theorem duality_inputs_only_kmax :
    (∃ (KM : ℝ), KM = 8 ∧ ((2 : ℝ) * KM - 1) = 15) :=
  ⟨8, rfl, dual_base_eq_fifteen⟩

/-- 路径 (II) 的输入是分支配积：式子里没有 k_max。 -/
theorem branch_inputs_only_counts :
    (∃ (NA NT : ℝ), NA = 3 ∧ NT = 5 ∧ NA * NT = 15) :=
  ⟨3, 5, rfl, rfl, branch_base_eq_fifteen⟩

/-- ★ 路径 (II) 的两个因子也全是 f 的函数：f − 1 = 3、f + 1 = 5。 -/
theorem branch_factors_from_fixedpoint :
    ((4 : ℝ) - 1) = 3 ∧ ((4 : ℝ) + 1) = 5 := by
  refine ⟨by norm_num, by norm_num⟩

/-- ★ 于是 (II) = (III)：`(f−1)(f+1) = f² − 1`。 -/
theorem branch_equals_fixedpoint :
    (((4 : ℝ) - 1) * ((4 : ℝ) + 1)) = ((4 : ℝ) ^ 2 - 1) := by ring

/-- ★ 三条路径全部归结到 f：两两两种等价写法都在 f = 4 处成立。 -/
theorem all_paths_collapse_to_fixedpoint :
    ((2 : ℝ) * (2 : ℝ) ^ 3 - 1) = ((4 : ℝ) ^ 2 - 1) ∧
    (((4 : ℝ) - 1) * ((4 : ℝ) + 1)) = ((4 : ℝ) ^ 2 - 1) :=
  ⟨dual_eq_fixedpoint_base, branch_equals_fixedpoint⟩

/-! ## §5 K_max 的两条写法（承接第 40 批）与 2^f − 1 -/

/-- `2·k_max − 1 = 2^f − 1`（k_max = 2^(f−1)、f = 4）。 -/
theorem dual_base_eq_two_pow_f_sub_one :
    ((2 : ℝ) * (2 : ℝ) ^ 3 - 1) = ((2 : ℝ) ^ 4 - 1) := by norm_num

/-- `2^f − 1 = f² − 1`（f² = 2^f）。 -/
theorem two_pow_f_sub_one_eq_fixedpoint :
    ((2 : ℝ) ^ 4 - 1) = ((4 : ℝ) ^ 2 - 1) := by norm_num

/-- ★ d_H 的 Mersenne 身份：`d_H = ln M_f`（f = 4 时 M_f = 15）。 -/
theorem dh_eq_log_mersenne : Real.log ((2 : ℝ) ^ 4 - 1) = Real.log 15 := by
  rw [two_pow_f_sub_one_eq_fixedpoint]
  exact dh_via_fixedpoint

/-- ★ 三式合一：2·k_max − 1 = 2^f − 1 = f² − 1 = 15。 -/
theorem fifteen_three_forms :
    ((2 : ℝ) * (2 : ℝ) ^ 3 - 1) = 15 ∧
    ((2 : ℝ) ^ 4 - 1) = 15 ∧
    ((4 : ℝ) ^ 2 - 1) = 15 :=
  ⟨by norm_num, by norm_num, by norm_num⟩

/-! ## §6 唯一剩余注入点 -/

/-- ★ 汇总：d_H = ln 15 的三条路径，其底数都是 f = 4 的函数；
    σ = 1/15 亦然。故唯一剩余注入点是 `f`（以及 `N_total` 的口径）。 -/
theorem remaining_injection_point :
    Real.log ((4 : ℝ) ^ 2 - 1) = Real.log 15 ∧
    ((1 : ℝ) / ((4 : ℝ) ^ 2 - 1)) = 1 / 15 ∧
    ((4 : ℝ) - 1) = 3 ∧ ((4 : ℝ) + 1) = 5 :=
  ⟨dh_via_fixedpoint, sigma_from_fixedpoint, by norm_num, by norm_num⟩

/-- ★ 路径 (II) 的结构前提已倒的算术留痕：`B = 3 × 5` 只需两个计数正确，不需要 4-范畴。 -/
theorem branch_product_needs_no_category :
    (3 : ℝ) * 5 = 15 ∧ (15 : ℝ) = 2 * (2 : ℝ) ^ 3 - 1 :=
  ⟨branch_base_eq_fifteen, by norm_num⟩

end MUFPF.DHThree
