/-
# `SpacetimeTotalAudit.lean` — 「时空总量 = 4」的地位审计（第 58 批）

## 本批要回答的问题

第 57 批的裁决（三）写：

> `catOrder = 4` 这一支的归属从「递归单向性」改为「**总量 4**」。
> ⇒ 若未来能导出「时空总量 = 4」，则 `timeLayerDim = 1`、`catOrder = 4`、
> `N_total = 5`、`B = 15` **四者一并成为推论**。

这句话把「总量 4」当成了尚未被导出的**上游**。本批审的就是这个上游本身：
`spacetimeDim` 在库里是

```
def spacetimeDim : ℕ := spaceLayerDim + timeLayerDim      -- L62
```

而 `spaceLayerDim := 3`、`timeLayerDim := 1`。⇒ `spacetimeDim = 4` 是 `3 + 1`
的**定义展开**，不是一个可以被「导出」的独立命题。

## 更强的发现：`catOrder` 与 `spacetimeDim` 是同一个定义式

`CatOrderFromSpacetime.lean` L102 的

```
def catOrderOf (d : ℕ) : ℕ := d + timeLayerDim
```

与 `spacetimeDim := spaceLayerDim + timeLayerDim` 在 `d := spaceLayerDim` 处
**逐字相同**。⇒ 本批主定理 `catOrder_is_spacetimeDim`：

```
catOrderOf spaceLayerDim = spacetimeDim          -- rfl
```

⇒ 第 57 批说的「把 `catOrder = 4` 归位到 `spacetimeDim = 4`」不是把一个结论
归到一个更上游的前提，而是**把它归到它自己**——两个名字指同一个定义式。
「归位」是重命名，不是归约。

## 于是三条等价把「强制」变成同义反复

`SpacetimeDimensionTwoPostulates.time_dim_forced`（L121）是

```
time_dim_forced (q : ℕ) (h : spaceLayerDim + q = 4) : q = 1
```

它被第 57 批当作 `timeLayerDim = 1` 的唯一机检来源。本批证它的**逆**也成立
（`total_forces_q_iff`、`forced_is_no_new_information`）：

```
spaceLayerDim + q = 4   ↔   q = 1
```

⇒ 前提与结论**逻辑等价** ⇒ 该定理没有信息增量，它只是在说
「`3 + q = 3 + 1` 等价于 `q = 1`」。

更彻底的一条是 `total_constraint_is_definitional`：

```
spaceLayerDim + q = spacetimeDim   ↔   q = timeLayerDim
```

⇒ `timeLayerDim` 在库里能遇到的**唯一约束**就是 `spacetimeDim`，
而 `spacetimeDim` 的定义**用到了 `timeLayerDim` 本身**。⇒ 该约束是自指的，
不能反过来钉住 `timeLayerDim`。

## `4` 在库里有四条互不引用的定义路径

| 路径 | 定义 | 出处 |
|---|---|---|
| ① | `fixedPoint := powers ^ 2`（`2²`） | `ActiveFromPowersCube.lean` L90 |
| ② | `fixedPoint : ℕ := 4`（裸字面量） | `FixedPointFactorOrigin.lean` L98 |
| ③ | `fixedPoint : ℕ := 4`（裸字面量） | `DivisorClosureIdentities.lean` L27 |
| ④ | `spacetimeDim := spaceLayerDim + timeLayerDim`（`3 + 1`） | `SpacetimeDimensionTwoPostulates.lean` L62 |

本批证明 ① 与 ④ 同值（`total_eq_fixedpoint`），但**这个同值是数值巧合，
不是结构同一**：两条定义互不引用，没有任何定理把「`f`」与「时空维数」挂上。
⇒ 「总量 4」不能借 `f = 4` 的来由。

## `3` 有源、`1` 无源 —— `4` 的地位等于 `1` 的地位

- **`3` 有源**：`three_is_pinned`（借第 32 批 `spaceLayerDim_unique`）证明
  `spaceLayerDim` 是方程 `2 ^ d = fixedPoint * powers` 的**唯一解**，
  即它是被一条非平凡约束钉住的。
- **`1` 无源**：`strictLayer_does_not_pin_layer_count` 证明
  `StrictLayer` 型的层结构**不能**把层的取值钉成唯一值
  （同一个 `f = id` 系统里 0…20 全部取到；配合第 57 批「层函数必无上界」，
  层计数根本不是 1）。

⇒ 相加得到 `4` 的两个数里，`3` 是被钉住的，`1` 是自由的（除自指约束外）。
⇒ **`spacetimeDim = 4` 的 `4` 只继承到 `3` 的那一半来由；`1` 的那一半仍是注入。**

## 顺带闭合第 34 批登记的一处洞

`CatOrderFromSpacetime.lean` 模块头边界 2 自认：

> 本批不 import `SpacetimeDimensionTwoPostulates` …… 因此本模块的 `timeLayerDim`
> 是**独立重写**的同值定义 …… **跨模块一致性未建成定理**——登记为未做项。

本批 `cross_module_timeLayerDim_agrees` 把这条洞闭合：

```
MUFPF.CatOrderSpacetime.timeLayerDim = MUFPF.SpacetimeDimensionTwoPostulates.timeLayerDim
```

## 裁决

1. **「时空总量 = 4」不是注入点，也不是上游。** 它是 `3 + 1` 的定义展开；
   把它当上游是负债转移，不是消去。
2. **第 57 批裁决（三）的承诺是空的。** 「若导出总量 4 ⇒ 四者成为推论」
   不成立，因为「总量 4」不可独立导出——它与 `catOrder = 4` 是同一个定义式。
3. **注入点净数不变（一项，不是两项）。** `timeLayerDim = 1` 与
   「`spacetimeDim = 4`」是**同一个东西的两个名字**，不能各记一项。
4. **`4` 的另一条来由（`f = 4`）不能挪用。** `spacetimeDim = fixedPoint`
   只是数值同值，两条定义互不引用；要挪用须另建结构桥，库内没有。
5. **未就地改 Lean doc。** `CatOrderFromSpacetime` L68/L96、
   `SpacetimeDimensionTwoPostulates` L136 三处偏强标注仍按「只登记、不就地改」
   策略保留，待裁决。
-/

import Mathlib.Tactic
import MUFPFormalization.SpacetimeDimensionTwoPostulates
import MUFPFormalization.CatOrderIsTimeOnly
import MUFPFormalization.ActiveFromPowersCube
import MUFPFormalization.CatOrderFromSpacetime

namespace MUFPF.SpacetimeTotal

open MUFPF.RecursionModularityBridge (StrictLayer)
open MUFPF.SpacetimeDimensionTwoPostulates (spaceLayerDim timeLayerDim spacetimeDim)

/-! ## 一、四个定义的原值 -/

/-- 总量是空间层数与时间层数之和——**定义式**，不是命题。 -/
theorem total_is_sum : spacetimeDim = spaceLayerDim + timeLayerDim := rfl

/-- `spaceLayerDim = 3`（库内裸定义）。 -/
theorem spaceLayerDim_eq_three : spaceLayerDim = 3 := rfl

/-- `timeLayerDim = 1`（库内裸定义）。 -/
theorem timeLayerDim_eq_one : timeLayerDim = 1 := rfl

/-- `spacetimeDim = 4`。 -/
theorem total_eq_four : spacetimeDim = 4 := by
  norm_num [spacetimeDim, spaceLayerDim, timeLayerDim]

/-! ## 二、「总量 4」与「`t = 1`」逻辑等价 -/

/-- ★★★ **「总量 = 4」⟺「时间层数 = 1」**。

    ⇒ 二者不是上下游关系，而是同一个命题的两个写法。
    ⇒ 把 `catOrder = 4` 归位到「总量 4」不构成归约。 -/
theorem total_four_iff_time_one : spacetimeDim = 4 ↔ timeLayerDim = 1 := by
  constructor
  · intro h
    have hs : spaceLayerDim + timeLayerDim = 4 := by
      rw [← total_is_sum]
      exact h
    have h3 : spaceLayerDim = 3 := spaceLayerDim_eq_three
    omega
  · intro h
    rw [total_is_sum, h]
    norm_num [spaceLayerDim]

/-- ★★★ **「空间 3 + 时间 `q` = 4」⟺「`q = timeLayerDim`」**（双向）。

    库内 `time_dim_forced` 只有正向（`→ q = 1`）；本批补上逆向，
    从而证明该「强制」的前提与结论**等价**。 -/
theorem total_forces_q_iff (q : ℕ) : spaceLayerDim + q = 4 ↔ q = timeLayerDim := by
  constructor
  · intro h
    have h3 : spaceLayerDim = 3 := spaceLayerDim_eq_three
    have h1 : timeLayerDim = 1 := timeLayerDim_eq_one
    omega
  · intro h
    rw [h, ← total_is_sum]
    exact total_eq_four

/-- ★★★ **`time_dim_forced` 无信息增量**：`spaceLayerDim + q = 4 ⟺ q = 1`。

    前提与结论等价 ⇒ 该定理是算术重述，不是从「总量 4」推导出 `q = 1`。 -/
theorem forced_is_no_new_information (q : ℕ) : spaceLayerDim + q = 4 ↔ q = 1 := by
  constructor
  · intro h
    have hq : q = timeLayerDim := (total_forces_q_iff q).mp h
    rw [hq]
    exact timeLayerDim_eq_one
  · intro h
    exact (total_forces_q_iff q).mpr (h.trans timeLayerDim_eq_one.symm)

/-- ★★★ **`timeLayerDim` 的唯一约束是自指的**：`spaceLayerDim + q = spacetimeDim`
    的解恰是 `q = timeLayerDim`，而 `spacetimeDim` 的定义**用到了 `timeLayerDim`**。

    ⇒ 库里不存在一条不提及 `timeLayerDim` 就能钉住它的约束。 -/
theorem total_constraint_is_definitional (q : ℕ) :
    spaceLayerDim + q = spacetimeDim ↔ q = timeLayerDim := by
  constructor
  · intro h
    have hs : spaceLayerDim + q = spaceLayerDim + timeLayerDim := by
      rw [total_is_sum] at h
      exact h
    have h3 : spaceLayerDim = 3 := spaceLayerDim_eq_three
    have h1 : timeLayerDim = 1 := timeLayerDim_eq_one
    omega
  · intro h
    rw [h, ← total_is_sum]

/-! ## 三、`catOrder` 与 `spacetimeDim` 是同一个定义式 -/

/-- ★★★ **`catOrder` 就是时空总量**：`catOrderOf spaceLayerDim = spacetimeDim`。

    `catOrderOf d := d + timeLayerDim` 与 `spacetimeDim := spaceLayerDim + timeLayerDim`
    在 `d := spaceLayerDim` 处逐字相同 ⇒ 两个名字指同一个定义式。
    ⇒ 第 57 批的「归位」是重命名，不是归约。 -/
theorem catOrder_is_spacetimeDim :
    MUFPF.CatOrderSpacetime.catOrderOf spaceLayerDim = spacetimeDim := rfl

/-- ★★ **跨模块一致性**（闭合第 34 批模块头边界 2 的未做项）：
    两处独立重写的 `timeLayerDim` 同值。 -/
theorem cross_module_timeLayerDim_agrees :
    MUFPF.CatOrderSpacetime.timeLayerDim = timeLayerDim := rfl

/-! ## 四、`4` 的另一条来由：`f = 4`（数值同值，非结构同一） -/

/-- ★★ **`spacetimeDim = fixedPoint`**（都是 4）。

    注意：这是**数值同值**，两条定义互不引用（`fixedPoint := powers ^ 2`，
    `spacetimeDim := spaceLayerDim + timeLayerDim`）。库内不存在把「不动点」
    与「时空维数」挂上的结构桥。 -/
theorem total_eq_fixedpoint : spacetimeDim = MUFPF.PowersCube.fixedPoint :=
  total_eq_four.trans MUFPF.PowersCube.fixedpoint_eq_four.symm

/-! ## 五、`3` 有源、`1` 无源 -/

/-- ★★★ **`3` 有源**：`spaceLayerDim` 是方程 `2 ^ d = fixedPoint * powers`
    的**唯一解**，故它是被一条非平凡约束钉住的（借第 32 批 `spaceLayerDim_unique`）。 -/
theorem three_is_pinned (d : ℕ)
    (h : 2 ^ d = MUFPF.PowersCube.fixedPoint * MUFPF.PowersCube.powers) :
    d = spaceLayerDim :=
  (MUFPF.PowersCube.spaceLayerDim_unique d h).trans spaceLayerDim_eq_three.symm

/-- ★★★ **`1` 无源**：`StrictLayer` 型的层结构**不能**把层的取值钉成唯一值。

    反例：`f = id`、`ev = succ` 的系统里层取值 0 与 1 同时出现 ⇒ 不存在唯一的层值。
    ⇒ 任何以 `StrictLayer` 为前提的定理都推不出「时间层数 = 1」。 -/
theorem strictLayer_does_not_pin_layer_count :
    ¬ ∀ (f : ℕ → ℕ), (∃ ev : ℕ → ℕ, StrictLayer ev f) →
        ∀ n m : ℕ, (∃ s, f s = n) → (∃ s, f s = m) → n = m := by
  intro h
  have hh := h (fun k : ℕ => k) ⟨fun k : ℕ => k + 1, by intro k; rfl⟩
  have h0 : ∃ s : ℕ, (fun k : ℕ => k) s = 0 := ⟨0, rfl⟩
  have h1 : ∃ s : ℕ, (fun k : ℕ => k) s = 1 := ⟨1, rfl⟩
  have hcontra : 0 = 1 := hh 0 1 h0 h1
  omega

/-! ## 六、总述 -/

/-- ★★★ **本批裁决的可机检部分**（五合取）：

    1. `spacetimeDim = spaceLayerDim + timeLayerDim`（定义式，不是命题）；
    2. `spaceLayerDim + q = 4 ⟺ q = timeLayerDim`（前提与结论等价）；
    3. `catOrderOf spaceLayerDim = spacetimeDim`（同一个定义式）；
    4. `spacetimeDim = fixedPoint`（数值同值，非结构同一）；
    5. `spaceLayerDim` 是 `2 ^ d = fixedPoint * powers` 的唯一解（`3` 有源）。

    ⇒ 合起来：「总量 4」既不是独立输入也不是上游；`4` 的地位等于 `1` 的地位。 -/
theorem total_audit_verdict :
    spacetimeDim = spaceLayerDim + timeLayerDim ∧
    (∀ q : ℕ, spaceLayerDim + q = 4 ↔ q = timeLayerDim) ∧
    MUFPF.CatOrderSpacetime.catOrderOf spaceLayerDim = spacetimeDim ∧
    spacetimeDim = MUFPF.PowersCube.fixedPoint ∧
    (∀ d : ℕ, 2 ^ d = MUFPF.PowersCube.fixedPoint * MUFPF.PowersCube.powers →
      d = spaceLayerDim) := by
  refine ⟨total_is_sum, ?_, catOrder_is_spacetimeDim, total_eq_fixedpoint, ?_⟩
  · intro q
    exact total_forces_q_iff q
  · intro d h
    exact three_is_pinned d h

end MUFPF.SpacetimeTotal
