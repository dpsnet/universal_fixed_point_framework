/-
第 42 批（第 41 批续）：DimensionSelfReference
—— 从「分形谱去递归」到 MUFPF 的抽象过程中丢失了「维度演化的阶数」；
   它在 `d_H` 里存活，其方程形式是「维度自指」。

## 起因

用户指出 MUFPF 的早期不是泛泛的分形研究，而是**由 SNN 大模型训练的递归迭代效率问题**
触发的分形谱去递归研究，中间经历了一次**抽象**。要问的是：**这次抽象丢掉了什么。**

## 原文证据（paper1_fractal_spectral_derecursion.md L68–74）

> **起点：计算瓶颈**……在早期针对**脉冲神经网络（SNN）**的研究中，递归迭代训练耗时极长，
> 频繁陷入局部震荡，且看不到明确的收敛路径。
> **核心直觉**：**递归迭代并非单纯的时间循环，而是一种维度演化。**
> **从 SNN 到谱理论**……$D$ 函子正是"谱化"的严格范畴论形式化。

## 丢失的地址（精确到定义）

`Rec` 对象（paper1 定义 2.1）：`R = (S_R, Φ_R, T_R, M_R)`，其中 **`T_R ⊆ ℝ≥0` 是时间半群**。
`Sp` 对象（paper1 定义 2.3）：`E = (H_E, A_E, σ_E)`。
`D` 函子：`A_R = −log U_R`（`U_R` 为 Koopman 算子）。

`log` 把「时间」换成「谱参数」，于是 **`T_R` 在 `Sp` 中没有对应物**。
「维度演化」这个原始直觉，在对象层就被压掉了——它只以两种方式残余：

1. **`d_H`（Hausdorff 维数）**：维数本身活下来了，但「演化到第几阶」的信息没了，`d_H` 变成连续值。
2. **`T_R` 的离散残余**：迭代步数，即「从单位倍增到 `k_max` 要走几步」。

⇒ **本模块的工作**：把第 2 条残余精确化。它给出的语义是 `N_active = log₂ k_max`，
这在库里已有（`BottTower.log2_k_max_eq_active_layers`），但 `BottTower` L170–183
把这条焊接降级为「**数值巧合对齐**」。本批的裁决是：那条注释**已过时**
——第 39–41 批已证三个 3 同源于 `f = 4`，故它们不是巧合，而是同一不动点方程的四个像。
但 `BottTower` 本身未改（**登记不改正**，见本模块末 `bott_note_superseded`）。

## 核心：维度自指

不动点方程是 `f² = 2^f`。两边开方（`f > 0`）得到**自指形式**：

$$f = 2^{f/2}$$

即「**维数等于 2 的（维数/2）次方**」——维度由维度自己定义。这是分形自相似的代数内核，
也正是 paper1 L70「递归迭代 = 维度演化」那句话在抽象后唯一还活着的数学内容。

`fixedpoint_implies_selfref` 是本模块唯一的**新数学**（ℝ 上 `Real.rpow` 域）；
其余定理是把既有算术事实按**语义**重新归位，并明确标注它们仍依赖 `f := 4` 这一选择。

## 诚实边界

1. `f = 4` 仍是选择（`f² = 2^f` 的解集 `{2, 4}`，`f = 2` 给退化 `N = 1`）。
   本模块只证「若 `f` 是不动点则 `f` 自指」，**不证** `f` 必然取 4。
2. `f² = 2^f ↔ f = 2^{f/2}` 的**反向**未机检，只证了正向蕴含（`f² = 2^f ⇒ f = 2^{f/2}`）。
   反向是同一代数事实的逆推，未纳入本模块以免扩大 `rpow` 域的形式化面。
3. 「`T_R` 在 `Sp` 中无对应物」是**文本层**判定（依据 paper1 定义 2.1 / 2.3 的字段对比），
   不是 Lean 定理——Lean 里 `RecObj` / `SpObj` 都是 `structure`，没有「字段必须出现」的约束。
4. 语义归位不产生新的数值结论；本模块**不新增任何常数**。
5. 四个「3」的语义标注是解释，不是证明；它们数值相等这件事在第 39–41 批已机检。

-/

import Mathlib.Tactic
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import MUFPFormalization.DHThreeSources

namespace MUFPF.SelfRef

open MUFPF.DHThree

/-! ## §1 维度自指：不动点方程的另一种写法 -/

/-- **维度自指（正向）**：若 `f > 0` 满足不动点方程 `f² = 2^f`，
则 `f` 可写成「2 的 `f/2` 次方」——即维数由自身定义。

证明走 `Real.log`：`f² = 2^f` 两边取对数得 `2 log f = f log 2`，
即 `log f = (f/2) log 2`；再由 `Real.exp_log` 与 `Real.rpow_def_of_pos` 还原。 -/
theorem fixedpoint_implies_selfref {f : ℝ} (hf : 0 < f) (h : f ^ 2 = 2 ^ f) :
    f = (2 : ℝ) ^ (f / 2) := by
  have h2 : (0 : ℝ) < 2 := by norm_num
  have hlog : Real.log (f ^ 2) = Real.log ((2 : ℝ) ^ f) := by rw [h]
  rw [Real.log_pow, Real.log_rpow h2] at hlog
  have key : Real.log f = (f / 2) * Real.log 2 := by
    have hh : (2 : ℝ) * Real.log f = f * Real.log 2 := hlog
    calc Real.log f = ((2 : ℝ) * Real.log f) / 2 := by ring
      _ = (f * Real.log 2) / 2 := by rw [hh]
      _ = (f / 2) * Real.log 2 := by ring
  calc f = Real.exp (Real.log f) := (Real.exp_log hf).symm
    _ = Real.exp ((f / 2) * Real.log 2) := by rw [key]
    _ = Real.exp (Real.log 2 * (f / 2)) := by rw [mul_comm]
    _ = (2 : ℝ) ^ (f / 2) := (Real.rpow_def_of_pos h2 (f / 2)).symm

/-- `f = 4` 时自指式成立：`4 = 2^2`。 -/
theorem four_is_selfref : (4 : ℝ) = (2 : ℝ) ^ ((4 : ℝ) / 2) := by
  have h : (4 : ℝ) / 2 = ((2 : ℕ) : ℝ) := by norm_num
  rw [h, Real.rpow_natCast]
  norm_num

/-- `f = 4` 同时满足自指方程的两种写法：`4² = 2⁴` 与 `4 = 2^(4/2)`。 -/
theorem four_satisfies_selfref_equation :
    (4 : ℝ) ^ 2 = (2 : ℝ) ^ (4 : ℝ) ∧ (4 : ℝ) = (2 : ℝ) ^ ((4 : ℝ) / 2) := by
  refine ⟨?_, four_is_selfref⟩
  have h : (4 : ℝ) = ((4 : ℕ) : ℝ) := by norm_num
  rw [h, Real.rpow_natCast]
  norm_num

/-! ## §2 第二个语义：`N_active` 是「倍增步数」

`k_max = 8 = 2³`。从单位 `1` 出发，每步翻倍，走到 `k_max` 要走 `3` 步。
这 `3` 步就是「维度演化」在抽象后留下的离散残余，也是 `log₂ k_max` 的含义。

注意：本节的算术都是既有事实的重新归位，**不是新定理**；
语义归位本身（「层数 = 步数」）是解释，其数值相等在 `BottTower` 已机检。 -/

/-- 从单位倍增三步到 `k_max = 8`。 -/
theorem kmax_is_three_doublings : (2 : ℕ) ^ 3 = 8 := by norm_num

/-- 倍增步数的对数形式：`Nat.log 2 8 = 3`。 -/
theorem doubling_steps_is_three : Nat.log 2 8 = 3 := by native_decide

/-- 从单位到不动点 `f = 4` 的步数：`4 − 1 = 3`。 -/
theorem step_count_to_fixedpoint : (4 : ℝ) - 1 = 3 := by norm_num

/-- 自然数版本，与 `step_count_to_fixedpoint` 同值。 -/
theorem step_count_to_fixedpoint_nat : (4 : ℕ) - 1 = 3 := by norm_num

/-! ## §3 四个像的语义表

四个「3」的语义：

| 记号 | 语义 | 本模块的出处 |
|---|---|---|
| `N_active = f − 1` | 自指步数（从单位到不动点的步数） | `step_count_to_fixedpoint` |
| `log₂ k_max = 3` | 倍增步数（从 1 倍增到 k_max） | `doubling_steps_is_three` |
| `N_active = 3` | 态射层数（类型构造子计数） | 第 38 批普查（`def := 3`） |
| `⌈d_H⌉ = 3` | 维数取整（Moran 维数上取整） | `hausdorff_layer_via_fixedpoint2` |

前三个都是「步数/计数」，第四个是「维数」。它们数值相等不是巧合，
因为四者都由 `f = 4` 决定（第 39–41 批）。 -/

/-- 四个语义在 `f = 4` 处同值：全部等于 `3`。 -/
theorem four_semantics_agree :
    ((4 : ℝ) - 1 = 3) ∧
    ((2 : ℕ) ^ 3 = 8 ∧ Nat.log 2 8 = 3) ∧
    (Int.ceil (Real.log ((4 : ℝ) ^ 2 - 1)) = 3) := by
  refine ⟨step_count_to_fixedpoint, ⟨kmax_is_three_doublings, doubling_steps_is_three⟩,
    hausdorff_layer_via_fixedpoint2⟩

/-- 自指步数与倍增步数是同一个数：`f − 1 = ℕ` 上的 `3` 同时是 `2³ = 8` 的指数。 -/
theorem selfref_step_is_doubling_exponent :
    (4 : ℕ) - 1 = 3 ∧ (2 : ℕ) ^ ((4 : ℕ) - 1) = 8 := by
  refine ⟨step_count_to_fixedpoint_nat, ?_⟩
  rw [step_count_to_fixedpoint_nat]
  norm_num

/-! ## §4 边界：`f := 4` 仍是选择

本模块把「层数」的语义从「态射层计数」搬到「倍增步数」，但**没有**消除 `f := 4` 这个注入点。
`f² = 2^f` 的解集是 `{2, 4}`（`FixedPointFactorOrigin` L57–58 已机检 `overlap_neg_two` /
`overlap_neg_four`），其中 `f = 2` 给 `N = 1`（退化）。选择 `f = 4` 的理由是「取非退化解」，
这是**选择**而非必然。 -/

/-- 注入点仍在 `f = 4`：本模块证到的只是「若 `f` 是不动点，则四个 3 同源于它」。 -/
theorem remaining_choice_is_fixedpoint :
    (4 : ℝ) ^ 2 = (2 : ℝ) ^ (4 : ℝ) ∧ (4 : ℝ) - 1 = 3 :=
  ⟨four_satisfies_selfref_equation.1, step_count_to_fixedpoint⟩

/-! ## §5 登记：`BottTower` 的「数值巧合」定性已过时（未改） -/

/-- **登记项（非定理）**：`BottTower.lean` L170–183 与 L196–207 的诚实版声明称
「`N_active = 3`、`log₂ k_max = 3`、`dim GenSpace = 3` 三者相等是
**三条独立事实的数值巧合对齐**，不是『一个结构决定的三个侧面』」。

第 39–41 批的机检结论已推翻这一措辞：
`ThreeThreesOneRoot.three_paths_one_root`、`FifteenMersenneRoot.two_fifteens_one_root`、
`DHThreeSources.all_paths_collapse_to_fixedpoint` 三条链都归结到 `f = 4`，
所以三者的相等**不是巧合，是同一不动点方程的不同投影**。

但「根 `f = 4` 本身是选择」这一点仍然成立——即 `BottTower` 的**结论力度**
（「不能称为结构推论」）在方向上仍正确，只是理由应从「数值巧合」改为「同源但根是选择」。

`BottTower.lean` 本身**未修改**（避免动已机检文件的结论措辞），本项在此登记。 -/
theorem bott_note_superseded_annotation :
    True := trivial

end MUFPF.SelfRef
