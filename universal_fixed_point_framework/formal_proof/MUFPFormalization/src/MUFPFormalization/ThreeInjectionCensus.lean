import Mathlib.Tactic
import MUFPFormalization.Unified3Theorem
import MUFPFormalization.CatOrderIsTimeOnly

/-!
# ThreeInjectionCensus.lean — 「3」的注入普查与焊接诊断（第 38 批）

## 本批做的是普查，不是证新定理

第 37 批链条闭合到「`N_active = 3` 只剩一处前提（`spaceLayerDim = 3`）」。本批转向
未闭合项第 1 条：「两个不同的 3」的同源性。

**先做全库普查（不是 Grep，是词法解析）。** `pr634om_scan3.py` 逐字符剥离块注释
（含 doc comment 与可嵌套的块注释）与行注释后，再匹配真实定义行：

```
真实 `def ... := 3` 共 21 处（排除注释里引用的代码块）
  ℕ 侧 6 处       ℝ 侧 15 处
```

**Grep 正则会多算 2 处。** 原因是 `FixedPointFactorOrigin.lean` L23 与
`CatOrderFromSpacetime.lean` L23 都在 doc comment 的 ``` 代码块里引用别人的定义
（第 31 批引用 `SpacetimeDimensionTwoPostulates.lean` L56–74 来展示循环路径；
第 34 批 `-- L56` 是行号标注）。**这两处不是 Lean 定义。**
⇒ 自我审计结论：第 31–37 批新增的 8 个模块**均未引入新的 `def := 3`**。

## 21 处按概念分组（本批核心分类）

| 组 | 概念 | 出现 | 类型 |
|---|---|---|---|
| **A** | 主动层数 | `N_active`（DHStructuralAnalysis L99）、`numActiveLayers`（Unified3Theorem L112） | ℕ |
| **A′** | 空间方向数 | `spaceLayerDim`（SpacetimeDimensionTwoPostulates L56） | ℕ |
| **B** | 世代数 `N_gen` | `nGen`（DivisorClosureIdentities L25、KMaxTwoPowerUnique L24）、`n_gen`（PellIdentity L32）、`Ngen`（ActiveSilentVieta L32、LambdaGapIdentity L36、MassChainConstants L36、NFamilyTheorems L30、NGKMOneIdentity L28） | ℕ 3 + ℝ 5 |
| **C** | 色数 | `Nc`（LambdaGapIdentity L30、MassChainConstants L30、SilenceDeltaIdentity L20）、`Nf`（LambdaGapIdentity L33、MassChainConstants L33） | ℝ 5 |
| **D** | `N_active` 的 ℝ 镜像 | `active`（AdjunctionUnitNorm L25、CorrectionFactorSpectrum L31、PublicResidueIdentity L30、RatioClosureIdentity L26）、`Nactive`（SilenceCriticalLayer L30） | ℝ 5 |

**⇒ 「两个不同的 3」的精确形式不是「两个」，是「5 个概念、21 份副本」。**
其中只有组 A / A′ 与 `N_active` 有关；组 B（世代数）与组 C（色数）是**恰好也等于 3 的
不同物理量**；组 D 是组 A 的 ℝ 重写。

**这一条澄清了第 29 / 33 / 36 批「两个不同的 3」的三次出现**：
第 33 批的「`N_active` 3 vs `spaceLayerDim` 3」其实是组 A vs 组 A′——**同一类的两个成员，
已被第 34 批焊成同一个变量 `d`（定义恒等 `(d+1)−1 = d`，这是有内容的）**；
第 36 批的「5 层去两层 vs `d + t` 去 t」是**两套分层**，不是两个 3。

## 焊接诊断（本批的主要结论）

**库内的「焊接」全部是 `x = 3 ∧ y = 3 ⇒ x = y`，中间一步没有结构内容。**

`weld_requires_both_three` 把这一点写成定理：它的两条前提里已经有 `3`，结论是传递。
**这条定理的内容为零**——把它写出来不是为了证明什么，是为了说清「现有材料只够这样」。

**有内容的焊接长什么样：** 前提只有一条指数等式。

```lean
exponential_weld (d c) (h : 2 ^ d = 2 ^ c) : d = c
```

这是可复用工具（`Nat.pow_right_injective`，`1 < 2`）。**它不写成「= 3」的形式，
所以不携带 3。** 若库内能提供 `2^d = 2^card`（`spaceLayerDim` 与 `card` 进入同一个
`2^·`），焊接就会有内容。

**但库里不能。** `k_max = 2^spaceLayerDim`（`SpacetimeDimensionTwoPostulates.lean` L68）
与 `k_max = 2^(card ActiveMorphismLayer)`（`BottTower.lean` L155）两条都存在，但：

* L68 的 `spaceLayerDim` 是 `def := 3`（组 A′ 的字面量）；
* `BottTower` L155 的 `card_active_layers` 是 `native_decide` 出的 3。

⇒ 两条等式的右边都是 `2^3`，中间那步仍然是「3 换皮」。**喂给 `exponential_weld`
的仍是 `2^3 = 2^3`。**

## 结论

**「两个 3 的同源性」不可能用现有材料闭合。** 需要的不是更多传递定理，而是一条
**新结构**：让「主动层数」与「空间方向数」由同一个代数对象算出，而不是各自被赋 `3`。

按本批诊断，那条约定理的形状应是：

```
初始代数（自函子 F 的不动点 μF）上的自由度计数 = 该层的空间方向数
```

这就是范畴论根系所在（泛性质 / 初始代数），而不是「对象 / 态射 / 函子」那层表述——
对象在范畴论里不承载结构，函子是第二阶概念。**库里没有这条定理。** 本批只把「要找什么」
说清，不假装找到。

## 边界

1. 本批的 21 处普查是**脚本 + 词法解析**结果，不是 Lean 定理（Lean 内无法表达
   「库内有 21 处 `def := 3`」）。脚本落 `scripts/pr634om_scan3.py`。
2. `card_eq_spaceDim_of_pow` 有内容（只要指数等式），但**库内没有它的前提**。
   它登记为「工具已备、弹药未到」。
3. 本批**不改**任何 `def := 3`（21 处分布在 21 个主题模块，合并风险远大于收益；
   且组 B/C 是物理常数，不是 `N_active` 相关）。
4. 组 D（`active` / `Nactive` 的 ℝ 镜像）是否为组 A 的有意重写，未核语义；
   本批只按名字与数值归组，**未逐条读 doc**。这一点标注为待核。
-/

namespace MUFPF.Census3

open MUFPF.Unified3
open MUFPF.PowersCube
open MUFPF.CatOrderTimeOnly

/-- ★★★ **有内容的焊接工具**：指数等式 ⇒ 指数相等。

    不写成 `= 3` 的形式，故不携带 `3`。只要拿到 `2^d = 2^c` 就得到 `d = c`。 -/
theorem exponential_weld (d c : ℕ) (h : 2 ^ d = 2 ^ c) : d = c :=
  Nat.pow_right_injective (by norm_num : 1 < 2) h

/-- ★★ 工具应用：若库内能给出 `2^d = 2^(card ActiveMorphismLayer)`，
    则主动层数 = 空间层数，**且此推导不经过 3**。 -/
theorem card_eq_spaceDim_of_pow (d : ℕ)
    (h : 2 ^ d = 2 ^ Fintype.card ActiveMorphismLayer) :
    d = Fintype.card ActiveMorphismLayer :=
  exponential_weld d (Fintype.card ActiveMorphismLayer) h

/-- ★★ **现有材料只能这样焊**：前提里已有两个 `3`，结论是传递。

    **本条内容为零。** 写出来是为了把「库内焊接只能是 3 = 3 换皮」这件事固定下来。 -/
theorem weld_requires_both_three (d : ℕ)
    (hD : 2 ^ d = fixedPoint * powers) : d = Fintype.card ActiveMorphismLayer := by
  have hd : d = 3 := spaceLayerDim_unique d hD
  rw [hd, card_active_layers]

/-- ★★ 三处「3」的来源各自独立（登记用，不作焊接）。

    `numActiveLayers` 是 `def := 3`；`card_active_layers` 是 `native_decide` 数构造子；
    `spaceLayerDim = 3` 是方程 `2^d = b³` 的唯一解。三者数值同、来源不同。 -/
theorem three_sources_independent :
    numActiveLayers = 3 ∧
      Fintype.card ActiveMorphismLayer = 3 ∧
      (∀ d : ℕ, 2 ^ d = fixedPoint * powers → d = 3) := by
  refine ⟨rfl, card_active_layers, ?_⟩
  intro d hD
  exact spaceLayerDim_unique d hD

/-- ★★ `numActiveLayers` 与 `card` 是同一个 3 的两种写法（第 38 批澄清组 A 内部）。
    这是 `def` 上的 `rfl`，不构成「构造子个数 = 3」的独立论证。 -/
theorem numActiveLayers_eq_card : numActiveLayers = Fintype.card ActiveMorphismLayer := by
  rw [show numActiveLayers = 3 from rfl, card_active_layers]

end MUFPF.Census3
