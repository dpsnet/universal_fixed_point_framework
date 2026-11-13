/-
# `timeLayerDim = 1` 的地位：`time_coordinate_unique` 不能作为它的依据

## 本批要回答的问题

第 56 批把 `N_total = 5` 归约到 `catOrder + 1` 之后，`catOrder = 4` 仍未消去。
第 37 批已证 `catOrder = 4 ⟺ timeLayerDim = 1`（`catOrder_four_iff_time_one`），
故消去 `catOrder = 4` 等价于消去 `timeLayerDim = 1`。

库内对 `timeLayerDim = 1` 给了三条「依据」标注：

| 位置 | 标注 |
|---|---|
| `CatOrderFromSpacetime.lean` L68 | `timeLayerDim = 1`（递归单向性：`time_coordinate_unique`） |
| `CatOrderFromSpacetime.lean` L96 | 结构依据：同文件 L135–144 `time_coordinate_unique` 与 L146–151 `time_orbit_injective` |
| `SpacetimeDimensionTwoPostulates.lean` L136 | 本定理「是「时间方向数 = 1」的结构依据」 |

但同一文件 `SpacetimeDimensionTwoPostulates.lean` 的模块头 L36–37 又自认：

> `time_orbit_injective` 只证层坐标良定义（G3 `StrictLayer` 的直接推论），
> **不等于物理时间一维性**；

而 `time_coordinate_unique` 自己的 doc L137 末句也写「此处**只做坐标良定义**」。

⇒ 于是同一组定理被文件头判为「不等于一维性」，又被另两处标为「一维性的依据」。

## 本批的答案：不是误标，是**逻辑上不可能**

`StrictLayer` 的定义（`RecursionModularityBridge.lean` L51–52）是

```
StrictLayer ev layerOf  :=  ∀ r, layerOf (ev r) = layerOf r + 1
```

它只说「每步升一层」。本批主定理 `strictLayer_forces_unbounded_layers` 证明：

> **任何满足 `StrictLayer` 的系统，其层函数必无上界**——
> `∀ N, ∃ s, layerOf s = layerOf r + N`（取 `s := recStep ev N r`）。

⇒ 而「时间层数 = 1」要求层集是单元集。二者**结构上不相容**。

⇒ 所以「`timeLayerDim = 1` 由 `time_coordinate_unique` 推出」不是措辞偏弱，
而是**前提与结论直接矛盾**：该定理的前提越是被满足，层数就越是无界。

⇒ 推论 `strictLayer_not_single_layer`：`StrictLayer` 排除「所有元素同层」，
即排除「时间只有一层」。

## 反例（可机检）

取 `R = ℕ`、`ev = fun n => n + 1`、`layerOf = fun n => n`：

- `StrictLayer ev layerOf` 成立（`nat_succ_strictLayer`）；
- `time_coordinate_unique` 的结论成立（`nat_succ_coordinate_unique`）；
- 而层函数在同一系统里既取到 5 也取到 10（`coordinate_unique_with_unbounded_layers`）。

⇒ 一个满足「时间坐标唯一」的系统，层数显然不是 1。⇒ 该定理不筛选 `catOrder`。

## 那么 `timeLayerDim = 1` 的真实来源是什么

唯一机检途径是 `SpacetimeDimensionTwoPostulates.time_dim_forced`：

```
time_dim_forced (q : ℕ) (h : spaceLayerDim + q = 4) : q = 1
```

⇒ 它把「时空总量 = 4」当作**前提**，从中解出 `q = 1`。本批把它桥接到
`timeLayerDim`（`timeLayerDim_forced_by_total`）与 `catOrder`（`catOrder_from_time_one`）。

⇒ 所以链条是：**「总量 4」→ `timeLayerDim = 1` → `catOrder = 4` → `N_total = 5` → `B = 15`**。
「总量 4」是这条链上唯一未被导出的前提。

## 裁决

1. **`timeLayerDim = 1` 仍是独立注入点，第 57 批没有减少它。** 但它现在有了明确的
   名字与位置：它是「总量 4」的下游，而不是「递归单向性」的下游。
2. **`time_coordinate_unique` / `time_orbit_injective` 的作用被重新定位**：它们是
   「时间坐标良定义」的定理，**不是**「时间方向数 = 1」的定理。二者不能互换。
3. **注入点表不变（两项）**，但 `catOrder = 4` 这一支的归属从「递归单向性」
   改为「总量 4」。⇒ 若未来能导出「时空总量 = 4」，则 `catOrder = 4`、`N_total = 5`、
   `B = 15` 三者一并成为推论。
4. **未就地改 Lean doc。** `CatOrderFromSpacetime` L68/L96 与
   `SpacetimeDimensionTwoPostulates` L136 三处标注仍偏强，登记待裁决。
-/

import Mathlib.Tactic
import MUFPFormalization.SpacetimeDimensionTwoPostulates
import MUFPFormalization.CatOrderIsTimeOnly

namespace MUFPF.TimeDirection

open MUFPF.RecursionModularityBridge (recStep StrictLayer recStep_layer)
open MUFPF.SpacetimeDimensionTwoPostulates (spaceLayerDim timeLayerDim)
open MUFPF.CatOrderTimeOnly (catOrderOfTime)

/-! ## 一、`StrictLayer` 蕴含层函数无上界 -/

/-- ★★★ **`StrictLayer` 蕴含层函数无上界**：从任一元素出发，`N` 步后到达
`layerOf r + N` 层。⇒ 前提越被满足，层数越无界。 -/
theorem strictLayer_forces_unbounded_layers {R : Type} (ev : R → R) (layerOf : R → ℕ)
    (r : R) (hlayer : StrictLayer ev layerOf) :
    ∀ N : ℕ, ∃ s : R, layerOf s = layerOf r + N := by
  intro N
  exact ⟨recStep ev N r, recStep_layer ev layerOf hlayer N r⟩

/-- ★★ **`StrictLayer` 排除「所有元素同层」**，即排除「时间只有一层」。 -/
theorem strictLayer_not_single_layer {R : Type} (ev : R → R) (layerOf : R → ℕ)
    (r : R) (hlayer : StrictLayer ev layerOf) :
    ¬ (∀ s : R, layerOf s = layerOf r) := by
  intro h
  have hstep := h (ev r)
  have hraise := hlayer r
  omega

/-- ★ 单步必升层：`layerOf (ev r) ≠ layerOf r`。 -/
theorem strictLayer_step_raises {R : Type} (ev : R → R) (layerOf : R → ℕ)
    (r : R) (hlayer : StrictLayer ev layerOf) :
    layerOf (ev r) ≠ layerOf r := by
  have hraise := hlayer r
  omega

/-! ## 二、反例：坐标唯一成立而层数远超 1 -/

/-- 后继推进在 `ℕ` 上满足 `StrictLayer`（把 `RecursionModularityBridge` 的
`example` 升为可引用的命名定理）。 -/
theorem nat_succ_strictLayer : StrictLayer (fun n : ℕ => n + 1) (fun n : ℕ => n) := by
  intro n
  simp

/-- 该系统的「时间坐标唯一」成立：`recStep` 的步数被层差锁定。 -/
theorem nat_succ_coordinate_unique (k₁ k₂ r : ℕ)
    (h : recStep (fun n : ℕ => n + 1) k₁ r = recStep (fun n : ℕ => n + 1) k₂ r) :
    k₁ = k₂ :=
  MUFPF.SpacetimeDimensionTwoPostulates.time_coordinate_unique
    (fun n : ℕ => n + 1) (fun n : ℕ => n) nat_succ_strictLayer k₁ k₂ r h

/-- ★★★ **反例**：存在一个「时间坐标唯一」成立、且层函数无上界的系统。

⇒ 该系统在同一实例里既取到第 5 层也取到第 10 层，故「时间层数 = 1」为假。
⇒ `time_coordinate_unique` 因此**不能**作为 `timeLayerDim = 1` 的依据。 -/
theorem coordinate_unique_with_unbounded_layers :
    StrictLayer (fun n : ℕ => n + 1) (fun n : ℕ => n) ∧
    (∀ k₁ k₂ r : ℕ,
      recStep (fun n : ℕ => n + 1) k₁ r = recStep (fun n : ℕ => n + 1) k₂ r → k₁ = k₂) ∧
    (∀ N : ℕ, ∃ s : ℕ, (fun n : ℕ => n) s = N) ∧
    (∃ s : ℕ, (fun n : ℕ => n) s = 5 ∧ ∃ s' : ℕ, (fun n : ℕ => n) s' = 10) := by
  refine ⟨nat_succ_strictLayer, ?_, ?_, ?_⟩
  · intro k₁ k₂ r h
    exact nat_succ_coordinate_unique k₁ k₂ r h
  · intro N
    exact ⟨N, rfl⟩
  · exact ⟨5, rfl, ⟨10, rfl⟩⟩

/-! ## 三、`timeLayerDim = 1` 的真实来源：总量 4 强制 -/

/-- ★★ **`timeLayerDim = 1` 由「总量 4」强制**：空间 3 + 时间 `q` = 4 ⇒ `q = timeLayerDim`。

⇒ 这是 `timeLayerDim = 1` 在库内唯一可机检的来源（`SpacetimeDimensionTwoPostulates.time_dim_forced`），
且其前提 `4` 是外部给定的，不由 `timeLayerDim` 自身定义导出。 -/
theorem timeLayerDim_forced_by_total (q : ℕ) (h : spaceLayerDim + q = 4) :
    q = timeLayerDim := by
  have h1 : q = 1 := MUFPF.SpacetimeDimensionTwoPostulates.time_dim_forced q h
  simp [timeLayerDim, h1]

/-- ★★ **`timeLayerDim = 1` ⇒ `catOrder = 4`**：把第 37 批的 `catOrderOfTime` 接上。 -/
theorem catOrder_from_time_one (t : ℕ) (ht : t = 1) : catOrderOfTime 3 t = 4 := by
  simp [catOrderOfTime, ht]

/-- `catOrder` 完全由时间层数决定：`catOrderOfTime 3 t = 3 + t`。 -/
theorem catOrder_pinned_by_time (t : ℕ) : catOrderOfTime 3 t = 3 + t := rfl

/-! ## 四、总述 -/

/-- ★★★ **本批裁决的可机检部分**：
1. 存在满足「时间坐标唯一」且层函数无界（故层数远非 1）的系统；
2. 「空间 3 + 时间 `q` = 4」强制 `q = timeLayerDim`；
3. `catOrder` 完全由时间层数决定。

⇒ 合起来：「`timeLayerDim = 1`」= 「总量 4」的下游；「坐标唯一」不是它的依据。 -/
theorem time_direction_verdict :
    (∃ (ev : ℕ → ℕ) (layerOf : ℕ → ℕ),
      StrictLayer ev layerOf ∧
      (∀ k₁ k₂ r : ℕ, recStep ev k₁ r = recStep ev k₂ r → k₁ = k₂) ∧
      (∀ N : ℕ, ∃ s : ℕ, layerOf s = N)) ∧
    (∀ q : ℕ, spaceLayerDim + q = 4 → q = timeLayerDim) ∧
    (∀ t : ℕ, catOrderOfTime 3 t = 3 + t) := by
  refine ⟨⟨fun n : ℕ => n + 1, fun n : ℕ => n, ?_, ?_, ?_⟩, ?_, ?_⟩
  · exact nat_succ_strictLayer
  · intro k₁ k₂ r h
    exact nat_succ_coordinate_unique k₁ k₂ r h
  · intro N
    exact ⟨N, rfl⟩
  · intro q h
    exact timeLayerDim_forced_by_total q h
  · intro t
    exact catOrder_pinned_by_time t

end MUFPF.TimeDirection
