/-
  EntryEfficacyAudit.lean — 唯一干净入口的效力判定：钉住数值 ≠ 钉住结构
  ==================================================================

## 接着什么往下做

§17 的全库审计把「形式承载常数」这一类收到 **4 条定理**，并指出它们几乎同源：

    BranchCountOrigin.catOrder_pinned_by_branch   (c−1)(c+1) = 2^c − 1  ⟹  c = 4
    BranchCountOrigin.pair_product_mer_iff        同上（iff 形式）
    ThreeInjectionCensus.exponential_weld          2^d = 2^c  ⟹  d = c
    ThreeInjectionCensus.card_eq_spaceDim_of_pow   前提含 card ActiveMorphismLayer（半污染）

真正独立的入口只有一个：`(c−1)(c+1) = 2^c − 1`。本模块判它的**效力**：
它钉住的东西是「数值 4」，还是「范畴阶 catOrder 这个结构」？

## 三条判据

| 编号 | 命题 | 判什么 |
|:--|:--|:--|
| ① | 4 在库内至少有三个结构来源 | 数值 4 是否为多源 |
| ② | 三个来源的**定义形式互不相同** | 来源是否真的不同，不是同一 def 的别名 |
| ③ | 任一 `ℕ → ℕ` 函数在三个来源上取同值 | 只拿数值的判别力是否为零 |

## 结论（先给，证明在下）

- ① **成立**：`catOrder = 4`（`CategoryOrder`）、`fixedPoint = 4`（`PowersCube`）、
  `spacetimeDim = 4`（`SpacetimeDimensionTwoPostulates`），三者定义在三个不同命名空间。
- ② **成立**：`catOrder` 是字面 4；`fixedPoint = powers ^ 2`（平方）；`spacetimeDim = spaceLayerDim + timeLayerDim`（求和）。三种定义形式不同。
- ③ **成立**：任何只看数值 4 的函数在三个来源上取值相同 ⟹ 数值不携带「来源」信息。

⇒ **判决：唯一干净入口钉住的是数值 4，不是结构。** 逆向能回到「某个数是 4」，
回不到「这个 4 是范畴阶、还是不动点、还是时空维数」。这是对本轮主问题
（「能否从物理层逆向推出范畴结构」）的**量化否决**：否决不是靠立场，是靠
「同一数值有三个结构来源」这一机检事实。

## 诚实边界

1. 本模块不证「这三个来源互不相关」。「三者都是 4」本身可能就是框架设计的
   后果（`fixedPoint = powers² = 4` 与 `catOrder = 4` 的数值重合在第 64 批已登记
   为数值合流，非导出）。本模块只主张：**在定义层面它们是三条不同的路径**。
2. ③ 是「数值盲」结论的通用形式，与 `PhysicsImpliesCategory.readout_value_blind`
   同型，但比较对象从「同一读数的不同原像」换成「同一数值的不同结构来源」。
3. 本模块不新增常数，不新增公设，全部结论为 `norm_num` / `rfl` / `rw` 级别，无 `sorry`。
4. `CatOrderFromSpacetime.lean` L23–25 还有一组**根命名空间**的同名 def
   （`spaceLayerDim`、`timeLayerDim`、`spacetimeDim`），本模块不用它们，避免与
   `MUFPF.SpacetimeDimensionTwoPostulates` 下的同名 def 混淆。
-/

import Mathlib.Tactic
import MUFPFormalization.BranchCountOrigin
import MUFPFormalization.ActiveFromPowersCube
import MUFPFormalization.SpacetimeDimensionTwoPostulates
import MUFPFormalization.PhysicsImpliesCategory

namespace MUFPF.EntryEfficacyAudit

/-! =========================================================
    §1 判①：数值 4 在库内至少有三个结构来源
   =========================================================

    三处各自独立定义，命名空间不同：
      MUFPF.CategoryOrder.catOrder                  = 4      （范畴阶，字面）
      MUFPF.PowersCube.fixedPoint                   = 4      （不动点，powers²）
      MUFPF.SpacetimeDimensionTwoPostulates.spacetimeDim = 4 （时空维数，求和）
-/

/-- **判①**：数值 4 有三个结构来源。 -/
theorem numeral_four_has_three_sources :
    MUFPF.CategoryOrder.catOrder = 4 ∧
    MUFPF.PowersCube.fixedPoint = 4 ∧
    MUFPF.SpacetimeDimensionTwoPostulates.spacetimeDim = 4 := by
  refine ⟨?_, ?_, ?_⟩
  · norm_num [MUFPF.CategoryOrder.catOrder]
  · norm_num [MUFPF.PowersCube.fixedPoint, MUFPF.PowersCube.powers]
  · norm_num [MUFPF.SpacetimeDimensionTwoPostulates.spacetimeDim,
      MUFPF.SpacetimeDimensionTwoPostulates.spaceLayerDim,
      MUFPF.SpacetimeDimensionTwoPostulates.timeLayerDim]

/-! =========================================================
    §2 判②：三个来源的定义形式互不相同
   =========================================================

    只证「三条路径的定义形式不同」，不证「互不相关」。
-/

/-- **判②**：`catOrder` 是字面常数，`fixedPoint` 是平方，`spacetimeDim` 是求和。 -/
theorem three_sources_defined_differently :
    MUFPF.CategoryOrder.catOrder = 4 ∧
    MUFPF.PowersCube.fixedPoint = MUFPF.PowersCube.powers ^ 2 ∧
    MUFPF.SpacetimeDimensionTwoPostulates.spacetimeDim
      = MUFPF.SpacetimeDimensionTwoPostulates.spaceLayerDim
        + MUFPF.SpacetimeDimensionTwoPostulates.timeLayerDim := by
  refine ⟨?_, ?_, ?_⟩
  · norm_num [MUFPF.CategoryOrder.catOrder]
  · rfl
  · rfl

/-! =========================================================
    §3 判③：只拿数值的判别力为零
   =========================================================
-/

/-- **判③**：任一 `ℕ → ℕ` 函数在三个来源上取同值。

    即：观测到「这个数是 4」之后，任何对该数值的加工都无法区分来源。 -/
theorem numeral_blind_across_sources (f : ℕ → ℕ) :
    f MUFPF.CategoryOrder.catOrder = f MUFPF.PowersCube.fixedPoint ∧
    f MUFPF.PowersCube.fixedPoint
      = f MUFPF.SpacetimeDimensionTwoPostulates.spacetimeDim := by
  have h1 : MUFPF.CategoryOrder.catOrder = 4 := by norm_num [MUFPF.CategoryOrder.catOrder]
  have h2 : MUFPF.PowersCube.fixedPoint = 4 := by
    norm_num [MUFPF.PowersCube.fixedPoint, MUFPF.PowersCube.powers]
  have h3 : MUFPF.SpacetimeDimensionTwoPostulates.spacetimeDim = 4 := by
    norm_num [MUFPF.SpacetimeDimensionTwoPostulates.spacetimeDim,
      MUFPF.SpacetimeDimensionTwoPostulates.spaceLayerDim,
      MUFPF.SpacetimeDimensionTwoPostulates.timeLayerDim]
  rw [h1, h2, h3]
  exact ⟨rfl, rfl⟩

/-! =========================================================
    §4 入口的自身形态：前提在框架内被自动满足
   =========================================================
-/

/-- 入口形式在 `c = catOrder` 处**自动成立**（不依赖任何物理输入）。

    即 `(catOrder − 1)(catOrder + 1) = 2^catOrder − 1` 是框架内部的恒等式：
    `catOrder = 4` 一旦固定，这条前提就被满足。所以从这条前提取信息，
    取到的只能是「框架已经放进去的 4」。 -/
theorem entry_premise_self_satisfied :
    (MUFPF.CategoryOrder.catOrder - 1) * (MUFPF.CategoryOrder.catOrder + 1)
      = 2 ^ MUFPF.CategoryOrder.catOrder - 1 := by
  norm_num [MUFPF.CategoryOrder.catOrder]

/-! =========================================================
    §5 判决汇总
   =========================================================
-/

/-- **本模块的判决**：唯一干净入口的效力 = 钉数值，不钉结构。

    三件事同时成立：
    1. 4 有三个结构来源（`numeral_four_has_three_sources`）；
    2. 三者的定义形式互不相同（`three_sources_defined_differently`）；
    3. 任一数值函数在三个来源上取同值（`numeral_blind_across_sources`）。

    ⇒ 观测到 4，无法判断来源是范畴阶、不动点还是时空维数。
      「逆向到结构」在唯一入口上也不成立。 -/
theorem entry_efficacy_verdict :
    (MUFPF.CategoryOrder.catOrder = 4 ∧
     MUFPF.PowersCube.fixedPoint = 4 ∧
     MUFPF.SpacetimeDimensionTwoPostulates.spacetimeDim = 4) ∧
    (∀ f : ℕ → ℕ,
      f MUFPF.CategoryOrder.catOrder = f MUFPF.PowersCube.fixedPoint ∧
      f MUFPF.PowersCube.fixedPoint
        = f MUFPF.SpacetimeDimensionTwoPostulates.spacetimeDim) :=
  ⟨numeral_four_has_three_sources, numeral_blind_across_sources⟩

end MUFPF.EntryEfficacyAudit
