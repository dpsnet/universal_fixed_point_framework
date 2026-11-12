import Mathlib.Tactic
import MUFPFormalization.ActiveFromCategoryOrder

/-!
# CatOrderFromSpacetime.lean — `catOrder = 4` 是输出：`4 = 3 + 1`（第 34 批）

## 本批要打掉什么

第 33 批把 `N_active = 3` 建成了 `catOrder − 1`，并证到了第 32 批登记的那座桥
`spaceLayerDim = N_active`。但那一批的底注仍是：

```
① catOrder := 4 —— Sp 为什么是 4-范畴，是框架公设
```

本批就把这条打掉：**`4` 不是公设，是 `3 + 1` 的输出。**

## 原料

`SpacetimeDimensionTwoPostulates.lean` L56–62 的三行定义：

```lean
def spaceLayerDim : ℕ := 3                       -- L56
def timeLayerDim : ℕ := 1                        -- L59
def spacetimeDim : ℕ := spaceLayerDim + timeLayerDim   -- L62
```

第 32 批已经把 `spaceLayerDim` 从 `def := 3` 换成方程 `2^d = b³` 的唯一解。
剩下的 `timeLayerDim := 1` 也不是裸字面量——它有一条结构依据，就写在同一个文件里：

* L59 doc：「时间方向数 = 递归单向性给出的 1 个方向（共享 G3 的 `StrictLayer` 语义）」
* L135–144 `time_coordinate_unique`：**严格升层下，同一终点的两个递归步数必相等**——
  时间是一条 ℕ 链（单一坐标），这是「时间方向数 = 1」的结构依据。
* L146–151 `time_orbit_injective`：`k ↦ recStep ev k r` 是单射——时间轴为单一 ℕ 链。

所以 `1` 的来由是：**递归步数坐标唯一 ⇒ 时间轴只有一条 ℕ 链 ⇒ 时间方向数 = 1。**

## 于是 `4` 是算出来的

```
catOrder = spaceLayerDim + timeLayerDim
         = d + 1
         = 3 + 1                     （d = 3 由 2^d = b³，第 32 批）
         = 4
```

**`4` 不再是输入。** 它由两个各自有机检来由的量相加得到：
`3` 来自幂基立方，`1` 来自递归单向性。

## 而且那座桥变成了 rfl

第 33 批的 `nActive = catOrder − 1`，现在把 `catOrder = d + 1` 代进去：

```
nActive = (d + 1) − 1 = d = spaceLayerDim
```

**`N_active = spaceLayerDim` 不再是两个独立算出的 3 恰好相等，
而是 `(spaceLayerDim + 1) − 1 = spaceLayerDim` 的定义恒等。**

这是第 32 批那座桥能成立的真实原因——桥不是巧合，是 `+1` 与 `−1` 相互抵消。

## 完整链条（本批之后的最终形态）

```
k_max = f · b = b³ = 2³           （第 32 批：三条已机检原料相乘）
   ⇒ 2^d = 2³ ⇒ d = 3             （第 32 批：spaceLayerDim_unique）
timeLayerDim = 1                  （递归单向性：time_coordinate_unique）
   ⇒ catOrder = d + 1 = 4         （本批）
   ⇒ nActive = catOrder − 1 = d   （本批：桥成 rfl 级恒等）
```

四个箭头，每一步都是机检算式；**没有任何一步是把目标数写进定义。**

## 边界（诚实，必须原样保留）

1. **`timeLayerDim := 1` 的依据不是物理时间一维性的证明。**
   `SpacetimeDimensionTwoPostulates.lean` L36–37 自己写明：「time_orbit_injective 只证层坐标
   良定义（G3 StrictLayer 的直接推论），**不等于物理时间一维性**」。本批沿用这条结构依据，
   并把「时间一维」的物理层面留在公设层。
2. **本批不 import `SpacetimeDimensionTwoPostulates`**（它牵着 `KMaxAlgebra` /
   `RecursionModularityBridge`，会引入 simp 扰动，历史上有坑）。因此本模块的
   `timeLayerDim` 是**独立重写**的同值定义，与库内 L59 一致但无形式依赖。
   跨模块一致性未建成定理——登记为未做项。
3. `b = 2`（`Powers`）仍是数值 `def`，是本批链条上唯一的数值输入。
4. 「主动生成层 = 排除对象层与 coherence 层」这条规则仍未被证明（第 33 批已登记）。
-/

namespace MUFPF.CatOrderSpacetime

open MUFPF.PowersCube

/-- 时间方向数 = 1（递归单向性：时间坐标是一条 ℕ 链）。

    库内同值定义：`SpacetimeDimensionTwoPostulates.lean` L59；
    结构依据：同文件 L135–144 `time_coordinate_unique` 与 L146–151 `time_orbit_injective`。 -/
def timeLayerDim : ℕ := 1

/-- 范畴阶 = 空间层数 + 时间层数（= 时空维数）。

    库内同值定义：`SpacetimeDimensionTwoPostulates.lean` L62 `spacetimeDim`。 -/
def catOrderOf (d : ℕ) : ℕ := d + timeLayerDim

/-- 总层数 = 范畴阶 + 1（对象层 0 到层 n，共 n+1 层）。 -/
def nTotalOf (d : ℕ) : ℕ := catOrderOf d + 1

/-- 主动生成层 = 范畴阶 − 1（排除对象层 0 与 coherence 层 n）。 -/
def nActiveOf (d : ℕ) : ℕ := catOrderOf d - 1

/-- `timeLayerDim = 1`。 -/
theorem timeLayerDim_eq_one : timeLayerDim = 1 := rfl

/-- ★★ **`catOrder` 是输出**：给定 `2^d = b³`（`d = 3`），`catOrder = 4`。

    即 `4` 由 `3 + 1` 算出，不是写进定义的字面量。 -/
theorem catOrder_eq_four (d : ℕ) (hD : 2 ^ d = fixedPoint * powers) :
    catOrderOf d = 4 := by
  have h3 : d = 3 := spaceLayerDim_unique d hD
  simp only [catOrderOf, timeLayerDim]
  omega

/-- ★★★ **桥成恒等**：`N_active = spaceLayerDim`，且是定义恒等而非两个 3 的巧合。

    第 33 批的 `nActive = catOrder − 1`，代入 `catOrder = d + 1` 即 `(d + 1) − 1 = d`。 -/
theorem nActive_eq_spaceLayerDim (d : ℕ) : nActiveOf d = d := by
  simp only [nActiveOf, catOrderOf, timeLayerDim]
  omega

/-- ★ `N_active = 3`（由 `catOrder = 4` 与「去一层」算出）。 -/
theorem nActive_eq_three (d : ℕ) (hD : 2 ^ d = fixedPoint * powers) :
    nActiveOf d = 3 := by
  have hD3 : d = 3 := spaceLayerDim_unique d hD
  rw [nActive_eq_spaceLayerDim]
  exact hD3

/-- `N_total = 5`（`catOrder + 1 = 4 + 1`）。 -/
theorem nTotal_eq_five (d : ℕ) (hD : 2 ^ d = fixedPoint * powers) :
    nTotalOf d = 5 := by
  have h4 : catOrderOf d = 4 := catOrder_eq_four d hD
  simp only [nTotalOf]
  omega

/-- ★ **`4 = 3 + 1`**：范畴阶恰是空间层数与时间层数之和，且空间层数被 `b³` 钉住。 -/
theorem four_is_three_add_one (d : ℕ) (hD : 2 ^ d = fixedPoint * powers) :
    catOrderOf d = 3 + 1 := by
  have h4 : catOrderOf d = 4 := catOrder_eq_four d hD
  omega

/-- `N_total = N_active + 2`（两条被去掉的层）。 -/
theorem nTotal_eq_nActive_add_two (d : ℕ) : nTotalOf d = nActiveOf d + 2 := by
  simp only [nTotalOf, nActiveOf, catOrderOf, timeLayerDim]
  omega

/-- ★★★ **全链汇总**：本批之后 `N_active = 3` 的每一步都是机检算式，
    没有一步把目标数写进定义。

    `hD` 是第 32 批的幂基立方链；结论同时给出
    `spaceLayerDim = 3`、`catOrder = 4`、`N_active = 3`、`N_active = spaceLayerDim`、
    `N_total = 5`、`4 = 3 + 1` 六件事。 -/
theorem whole_chain (d : ℕ) (hD : 2 ^ d = fixedPoint * powers) :
    d = 3 ∧
    catOrderOf d = 4 ∧
    nActiveOf d = 3 ∧
    nActiveOf d = d ∧
    nTotalOf d = 5 ∧
    catOrderOf d = d + 1 := by
  have h3 : d = 3 := spaceLayerDim_unique d hD
  have h4 : catOrderOf d = 4 := catOrder_eq_four d hD
  have hA : nActiveOf d = 3 := nActive_eq_three d hD
  have hB : nActiveOf d = d := nActive_eq_spaceLayerDim d
  have hT : nTotalOf d = 5 := nTotal_eq_five d hD
  have hSum : catOrderOf d = d + 1 := by simp only [catOrderOf, timeLayerDim]
  exact ⟨h3, h4, hA, hB, hT, hSum⟩

/-- 一致性备注：本模块 `timeLayerDim = 1` 与 `SpacetimeDimensionTwoPostulates.lean` L59
    同值（未建跨模块定理，见模块头边界 2）。 -/
theorem timeLayerDim_is_one_not_two : timeLayerDim ≠ 2 ∧ timeLayerDim = 1 := by
  refine ⟨?_, timeLayerDim_eq_one⟩
  simp only [timeLayerDim]
  omega

end MUFPF.CatOrderSpacetime
