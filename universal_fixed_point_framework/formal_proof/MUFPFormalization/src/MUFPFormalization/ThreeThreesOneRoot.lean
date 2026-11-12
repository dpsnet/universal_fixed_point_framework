import Mathlib.Tactic
import Mathlib.Analysis.Complex.ExponentialBounds
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import MUFPFormalization.PowersSelfPinned
import MUFPFormalization.ActiveFromPowersCube

/-!
# ThreeThreesOneRoot.lean — 三条 `3` 路径同源于 `f = 4`（第 39 批）

## 起因：回扫早期「分形谱去递归」资料

第 38 批的诊断是：六步链条是**方程闭合**，不是范畴闭合；「两个 3 的同源性」不可能用
传递定理焊出来。本批按用户提示回扫仓库根目录的早期资料，找到两条被登记但未发展的线索：

1. `zhihu_引力不是一种力_质量与能量的谱学起源.md` L63：
   「空间维数 `d = 3` 来自**范畴中非对象态射的层数**」——比第 36 批
   `active_layer_is_space_layer` 更早、更直接的同一条主张。
2. `external_theory_presurvey/external_theory_lineage_presurvey.md` L138：
   「`N_active = ⌈d_H⌉`、可观测层 = `⌊d_H⌋`」——**`d_H` 是 Hausdorff 维数**。
   该行自己标注「数值候选非推导」。

`d_H` 在库内是已机检的量：`SpinorSilenceBranch.lean` L194
`corollary_entropy_eq_dH : Real.log 15 = -Real.log S4`，而 `S4 = 1/15`。
即 **`d_H = ln 15 ≈ 2.708`**（静默熵 / Moran 主项）。

## 本批的核心发现：同源不是「焊接」而是「同一输入的三个像」

`⌈ln 15⌉ = 3` 可机检。但光有这一条，只是「又找到了一个 3」。**真正的突破在于：
现有的三个 `3` 全是 `f = 4` 的算术像。**

| 路径 | 运算 | 结果 | 出处 |
|---|---|---|---|
| ① 减一 | `f − 1` = `4 − 1` | `3` | `SpectralGap.lean` L375–383 `fixedpoint_active_identity` |
| ② 乘幂取对数 | `log₂(f·b)` = `log₂(4·2)` = `log₂ 8` | `3` | 第 32 批 `k_max = f·b = b³` |
| ③ 平方减一再取上整 | `⌈ln(f² − 1)⌉` = `⌈ln 15⌉` | `3` | **本批**（`d_H = ln 15`） |

**三条路径的输入都是 `f = 4`，运算完全不同，输出都是 3。**

这就是「同源性」的精确含义：**不是同一条定理，是同一个输入被三个不同运算投影。**
第 29 / 33 / 36 批三次追问「两个 3 是否同源」之所以答不上来，是因为一直在找
「把两个 3 连起来的定理」；实际上要连的不是两个 3，是它们共同的输入 `f`。

而 `f = 4` 本身有来由：`FixedPointFactorOrigin.lean`（第 31 批）证明 `f² = 2^f` 在
`f < 9` 内唯一解为 `f = 4`；`PowersSelfPinned.lean`（第 35 批）进一步证明
`f = b² ∧ f² = b^f ∧ b ≥ 2 ⇒ b = 2 ∧ f = 4`（消掉了 `σ⁻¹ = 15` 这个中间量）。

## 为什么路径 ③ 比路径 ① 有内容

路径 ①（`4 − 1 = 3`）是纯减法，内容薄。路径 ③ 经过 `ln` 与 `⌈·⌉` 两个非线性运算：

```
f² − 1 = 15  ⇒  d_H = ln 15 ≈ 2.7080  ⇒  ⌈d_H⌉ = 3
```

**取上整不能由 `15` 的因子分解得到**（`15 = 3 × 5` 会给出 3，但那是分解，正是第 28 批
被判循环的做法）。`⌈ln 15⌉` 得到 3 是因为 `e² = 7.389 < 15 < e³ = 20.085`，
即 **3 在这里是「`15` 落在 `e` 的哪个整幂区间」的结果**，与 15 的因子无关。

**⇒ 路径 ③ 绕开了第 28 批的循环。**

## 但注入点没有消失，只是换了位置

| 链 | 注入点 | 性质 |
|---|---|---|
| 第 32 批（方程） | `spaceLayerDim = 3` 作为 `2^d = b³` 的解 | 方程的解，数值唯一 |
| 本批（维数） | `σ = 1/15`（`S4`） | 框架常数：静默分支权重 |
| 本批（规则） | 「层数 = `⌈d_H⌉`」 | **选择**，不是定理 |

**必须说清第三条。** `⌈d_H⌉ = 3` 是定理；「层数等于维数上整」是**规则**。它的几何理由
是：分形维数 `d_H` 表示有效维度，层数是整数且要覆盖整个分形，最小这样的整数就是
`⌈d_H⌉`。这条理由**有内容**，但**不是**库里已证的定理。

⇒ 本批的诚实结论：`N_active = 3` 现在有**两条互不依赖的路径**（方程 / 维数），
两条都上溯到 `f = 4`，且都不可避免地依赖一个框架常数（`b = 2` 一侧 / `σ = 1/15` 一侧）。
**把两条合成一条无注入的链，本批做不到。**

## 与第 38 批诊断的关系

第 38 批说「六步是算术闭合，不是范畴闭合」。本批补上的是：**这个算术闭合现在有了
一个统一的输入 `f = 4`，且三条路径互不重复**。范畴闭合（「`μF` 上的自由度计数」）
仍然缺，但「同源性」这一项从「未闭合」变为「已闭合（在算术层）」。

## 边界

1. `⌈ln 15⌉ = 3` 用 `Int.ceil_eq_iff` + `Real.exp_one_gt_d9` / `exp_one_lt_d9` 机检，
   不依赖任何数值近似的外部输入。
2. 「层数 = `⌈d_H⌉`」是规则选择，本批**只登记，不声称已证**。
3. `d_H = ln 15` 引用 `SpinorSilenceBranch` 的 `corollary_entropy_eq_dH`（已机检），
   本模块不重复证明，只做衔接。
4. 路径 ① 的 `f − 1 = 3` 引用 `SpectralGap.lean` 的既有结论，本模块以 `4 - 1 = 3`
   的算术形式登记（`norm_num`），语义衔接见 §21.50。
5. 早期资料里 `system1`~`system7`（七个 IFS/RG/NTK 系统）与 `Involution = 7` 的关系
   未核；`dimindextower_build1.log` 所指的「维数指数塔」模块源码未找到。**登记为待查。**
-/

namespace MUFPF.OneRoot

open MUFPF.PowersPinned
open MUFPF.PowersCube

/-- ★★★ **路径 ③ 的两个指数界**：`e² < 15 < e³`。

    `15` 落在 `e` 的第二个与第三个整幂之间——**这才是 `⌈ln 15⌉ = 3` 的真实理由**，
    与 `15 = 3 × 5` 的因子分解无关（后者正是第 28 批被判循环的做法）。 -/
theorem exp_two_lt_fifteen : Real.exp 2 < 15 := by
  have hsq : Real.exp 2 = Real.exp 1 * Real.exp 1 := by
    rw [show (2 : ℝ) = 1 + 1 by norm_num, Real.exp_add]
  have h1 : Real.exp 1 < 2.7182818286 := Real.exp_one_lt_d9
  have hp : 0 < Real.exp 1 := Real.exp_pos 1
  rw [hsq]
  nlinarith [h1, hp]

/-- ★★★ **路径 ③ 的上界**：`15 < e³`。 -/
theorem exp_three_gt_fifteen : 15 < Real.exp 3 := by
  have hcube : Real.exp 3 = Real.exp 2 * Real.exp 1 := by
    rw [show (3 : ℝ) = 2 + 1 by norm_num, Real.exp_add]
  have h2 : 7 < Real.exp 2 := by
    have hsq : Real.exp 2 = Real.exp 1 * Real.exp 1 := by
      rw [show (2 : ℝ) = 1 + 1 by norm_num, Real.exp_add]
    have h1 : 2.7182818283 < Real.exp 1 := Real.exp_one_gt_d9
    have hp : 0 < Real.exp 1 := Real.exp_pos 1
    rw [hsq]
    nlinarith [h1, hp]
  have h1 : 2.7182818283 < Real.exp 1 := Real.exp_one_gt_d9
  rw [hcube]
  nlinarith [h2, h1]

/-- ★★ `2 < ln 15`（由 `e² < 15`）。 -/
theorem log15_gt_two : 2 < Real.log 15 := by
  have he : (2 : ℝ) = Real.log (Real.exp 2) := (Real.log_exp 2).symm
  rw [he]
  exact (Real.log_lt_log_iff (Real.exp_pos 2) (by norm_num : (0 : ℝ) < 15)).mpr
    exp_two_lt_fifteen

/-- ★★ `ln 15 < 3`（由 `15 < e³`）。 -/
theorem log15_lt_three : Real.log 15 < 3 := by
  have he : (3 : ℝ) = Real.log (Real.exp 3) := (Real.log_exp 3).symm
  rw [he]
  exact (Real.log_lt_log_iff (by norm_num : (0 : ℝ) < 15) (Real.exp_pos 3)).mpr
    exp_three_gt_fifteen

/-- ★★★ **路径 ③ 的核心**：`⌈ln 15⌉ = 3`。

    不用 15 的任何因子分解，只用「15 落在 e 的哪两个整幂之间」。 -/
theorem hausdorff_ceil_three : Int.ceil (Real.log 15) = 3 := by
  refine Int.ceil_eq_iff.mpr ⟨?_, ?_⟩
  · have h : ((3 : ℤ) : ℝ) - 1 = 2 := by norm_num
    rw [h]
    exact log15_gt_two
  · have h : ((3 : ℤ) : ℝ) = 3 := by norm_num
    rw [h]
    exact log15_lt_three.le

/-- ★★ `⌈d_H⌉` 作为自然数（层数口径）：`d_H = ln 15`。 -/
theorem hausdorff_layer_is_three : (Int.ceil (Real.log 15)).toNat = 3 := by
  rw [hausdorff_ceil_three]
  rfl

/-! ## 三条路径同源于 `f = 4` -/

/-- ★★ 路径 ①：`f − 1 = 3`。 -/
theorem path_one_sub (f : ℕ) (hf : f = 4) : f - 1 = 3 := by
  omega

/-- ★★★ 路径 ②：`log₂(f·b) = 3`。`f·b = 8 = 2³`，故对数为 3。 -/
theorem path_two_log (f b : ℕ) (hf : f = 4) (hb : b = 2) :
    Nat.log 2 (f * b) = 3 := by
  rw [hf, hb]
  decide

/-- ★★★ 路径 ③：`⌈ln(f² − 1)⌉ = 3`。 -/
theorem path_three_ceil (f : ℕ) (hf : f = 4) :
    Int.ceil (Real.log ((f : ℝ) ^ 2 - 1)) = 3 := by
  subst hf
  norm_num
  exact hausdorff_ceil_three

/-- ★★★ **同源性**：三条完全不同的路径，同一个输入 `f = 4`，输出都是 3。

    这不是「两个 3 恰好相等」，是「一个输入在三种运算下的三个像」。 -/
theorem three_paths_one_root (f b : ℕ) (hf : f = 4) (hb : b = 2) :
    f - 1 = 3 ∧
      Nat.log 2 (f * b) = 3 ∧
      Int.ceil (Real.log ((f : ℝ) ^ 2 - 1)) = 3 :=
  ⟨path_one_sub f hf, path_two_log f b hf hb, path_three_ceil f hf⟩

/-- ★★★ **`f = 4` 的唯一性**（第 35 批 `powers_unique` 的直接引用）：
    `f = b² ∧ f² = b^f ∧ 2 ≤ b ⇒ b = 2 ∧ f = 4`。

    ⇒ 三条路径的共同输入不是自由参数，是那条方程自己的唯一解。 -/
theorem root_is_pinned {b f : ℕ} (hb : 2 ≤ b) (hf : f = b ^ 2)
    (hSq : f ^ 2 = b ^ f) : b = 2 ∧ f = 4 :=
  ⟨powers_self_pinned hb hf hSq, fixedpoint_eq_four hb hf hSq⟩

/-- ★★ **完整同源链**：`b = 2 ∧ f = 4` ⇒ 三条路径全部给出 3。 -/
theorem full_root_chain {b f : ℕ} (hb : 2 ≤ b) (hf : f = b ^ 2)
    (hSq : f ^ 2 = b ^ f) :
    b = 2 ∧ f = 2 ^ 2 ∧ f - 1 = 3 ∧
      Nat.log 2 (f * b) = 3 ∧
      Int.ceil (Real.log ((f : ℝ) ^ 2 - 1)) = 3 := by
  obtain ⟨hb2, hf4⟩ := root_is_pinned hb hf hSq
  have hf22 : f = 2 ^ 2 := by rw [hf4]; norm_num
  refine ⟨hb2, hf22, ?_, ?_, ?_⟩
  · omega
  · exact path_two_log f b hf4 hb2
  · exact path_three_ceil f hf4

/-! ## 两条路径互不依赖（登记） -/

/-- ★★★ **方程路径与维数路径互不依赖**：前者只用 `k_max = 2^d`，
    后者只用 `d_H = ln(f² − 1)`。两者给出同一个 3，但推导中没有共用中间量
    （共同的只有输入 `f = 4`）。 -/
theorem two_paths_independent (d : ℕ)
    (hD : 2 ^ d = fixedPoint * powers) :
    d = 3 ∧
      Int.ceil (Real.log ((fixedPoint : ℝ) ^ 2 - 1)) = 3 ∧
      Nat.log 2 (fixedPoint * powers) = 3 := by
  have hd : d = 3 := spaceLayerDim_unique d hD
  have hf : fixedPoint = 4 := by
    unfold fixedPoint powers
    norm_num
  refine ⟨hd, ?_, ?_⟩
  · exact path_three_ceil fixedPoint hf
  · rw [hf]
    unfold powers
    decide

end MUFPF.OneRoot
