/-
# `LayerBoundaryAudit.lean` — `N_total = catOrder + 1` 与 `N_active = catOrder − 1` 那一对边界 `±1`（第 60 批）

## 本批要回答的问题

第 59 批审完 `spacetimeDim` 里的 `+`，注入点修正为两项。沿同一条方法（专审从未被审的符号），
本批审 `N_total` 与 `N_active` 的**那一对 `±1`**：

```
nTotal := catOrder + 1      (= 5)
nActive := catOrder - 1     (= 3)
```

第 56 批把 `B` 归约到 `(c − 1)(c + 1) = c² − 1 = M₄`，但没有审这两个 offset 各自的地位。
三问：

1. 「`N_active` 去掉两层（对象层 0 + coherence 层 n）」是不是一个独立的结构事实？
2. `+1` 与 `−1` 是 `catOrder` 的两个独立计数，还是一个对称包装？
3. `+1` 声称「顶层停在层 4」——库内层结构停在哪里？

## 发现一：`±1` 是一对**代数对称包装**，「去两层」不携带信息

```
nTotal = c + 1,   nActive = c - 1
⇒ nActive = nTotal - 2
```

右侧那个 `−2` 不是「去掉对象层与 coherence 层」这个结构操作的结果，而是
`(c + 1) - 2 = c - 1` 这个**对任意 `c` 成立的恒等式**（`sub_one_eq_add_one_sub_two`）。

⇒ 库内 `nActive_eq_nTotal_sub_two`（`ActiveFromCategoryOrder` L115）虽然被写成「等价写法：
去掉对象层与 coherence 层」，但它是**定义的改写**，不是推导。与本批同型于第 58 批的
`catOrderOf spaceLayerDim = spacetimeDim`（`rfl` 型改名）。

⇒ 进一步：`(c−1)(c+1) + 1 = c²` 对 `c ≥ 1` 恒成立（`pm_one_product_add_one`）
⇒ **`B = c² − 1` 完全由 `c` 决定，两个 offset 不提供任何超出 `c` 的信息。**
`±1` 只是把 `c² − 1` 拆成两个因子。

## 发现二：库内有**四个** `N_total`，其中两个是裸常量

| 位置 | 定义 | 类型 |
|---|---|---|
| `CategoryOrder.nTotal` | `catOrder + 1` | 函数 |
| `CatOrderSpacetime.nTotalOf d` | `catOrderOf d + 1` | 函数 |
| `BranchCounting.N_total` | `:= 5` | **裸常量** |
| `DHStructural.N_total` | `:= 5` | **裸常量** |

数值先证伪（`pr634rl_falsify_result.txt`，`E_AGREE_ON_NTOTAL [4]`）：
函数口径 `c + 1` 与裸常量 `5` **只在 `c = 4` 重合**；`c = 5` 时函数给 6、常量仍是 5。

⇒ **裸常量 `5` 不可能是 `catOrder` 的函数，它只在 `c = 4` 处与结构口径偶然同值。**
这是第 58 批「数值同值非结构同一」（`total_eq_fixedpoint`）的同型现象，且比它更强：
不仅同值，而且**其中一侧根本不是函数**。

本批把此前缺失的桥建起来：

```
layerIndex_card_eq_nTotal : Fintype.card LayerIndex = nTotal
```

此前 `Fintype.card LayerIndex = 5`（`total_layers_count`）与 `nTotal = 5`（`nTotal_eq_five`）
是两条互不引用的定理。桥建成后仍要说明：**它只是把两个 5 接上，不解释 `+1`**。

## 发现三：`+1` 的「顶层停在层 4」被库内**自身反证**

`nTotal = catOrder + 1` 的 doc 写「对象层 0 到层 4」，`LayerIndex` 也恰有 5 个构造子
（`obj` / `one` / `two` / `three` / `four`）。但库内：

1. **层 5 结构已存在**：`SpFiveLayer.lean` L33 `structure SpFiveMorphism`，逐字同形于
   `SpFourMorphism`（`thirdHomotopy → fourthHomotopy`，同一 `R = A*L - L*A` 判据）。
2. **层 5 有非平凡态射**：`SpTowerWitness.lean` `five0 : SpFiveMorphism four0 four1`，
   `fourthHomotopy = diag(0,1,2) ≠ 0` ⇒ `tower_height_at_least_five_B`。
3. **层 4 本身就不「只含退化态射」**：`SpLayerNonCollapse.lean` L183–202 已机检
   `SpFourMorphism threeA threeB` 非空且 `threeA ≠ threeB`。
4. **B 相层数无界**：`SpTowerUnbounded.lean` L48
   `tower_height_unbounded_B : ∀ k, 2 ≤ k → LayerWitness jordan3`。

⇒ `Fintype.card LayerIndex = 5` 是**类型定义停止**（该 `inductive` 只有 5 个构造子），
不是「结构上只有 5 层」。`SpFiveLayer.lean` L4 自称的「库内层结构止于 `SpFourMorphism`」
已由该文件自身否证（`CatOrderIsTimeOnly.lean` L34 已登记同一事实）。

⇒ **`+1` 的「顶层」是 A 相（可对角化、`ker ∩ im = 0`）读法，不是普遍结论。**
`Unified3Theorem.lean` L79–80 与 `ActiveLayerIsSpaceLayer.lean` L32 已自认这条规则「分相成立」。

## 裁决（五条）

1. **`±1` 不是两个独立的结构计数，而是 `catOrder` 的一个对称包装。**
   `nActive = nTotal - 2` 是恒等式，`(c−1)(c+1) + 1 = c²` 对一切 `c ≥ 1` 成立
   ⇒ 两个 offset 对 `B` 的信息贡献为零，`B` 是 `c` 的一元函数。
2. **「去两层」的语义主张（对象层 + coherence 层）在库内始终未证。**
   `ActiveFromCategoryOrder` L76 自认「这条规则本身未被证明」，第 33 批已登记。
   本批把它钉死为「算术恒等式的伪装」，而不是留下一个「待证规则」。
3. **`+1` 的「5 层」与 `LayerIndex` 的 5 个构造子是同值巧合，不同源。**
   本批建了 `layerIndex_card_eq_nTotal` 桥，但桥只接数值。
   ⇒ 登记 `layer_index_stops_at_four_without_structural_witness`。
4. **`+1` 的顶层在 B 相被库内自身反证**（层 5 结构 + 层 5 非平凡态射 + 层数无界）
   ⇒ `N_total = 5` 是 A 相读法；`B = 15` 作为 `c² − 1` 的数值无条件，但「15 = 层对数」
   只在 A 相成立。
5. **注入点计数不变，仍两项**：`±1` 由 `catOrder` 决定（`nTotal = c + 1` 是定义），
   不构成第三个独立注入。但**新增一个适用范围限制**：`B = 15` 的层对读法限于 A 相。

## 与第 56/59 批的关系

- 第 56 批：`B = (c−1)(c+1) = c² − 1 = M₄`，数值上对。本批补上：这个 `−1` 来自
  `±1` 的代数对称，**不是**来自「去掉两层」；且 `(c−1)(c+1)` 与 `2^c − 1` 只在
  `c ∈ {2, 4}` 重合（`c ≥ 3` 唯一 `4`，数值先证伪已复算）⇒ 15 的真身仍是 `M₄`。
- 第 59 批：注入点两项 `{timeLayerDim = 1, 复合律 = 加法}`。本批确认 `±1` 不进这个集合。
-/

import Mathlib.Tactic
import MUFPFormalization.ActiveFromCategoryOrder
import MUFPFormalization.BranchCounting
import MUFPFormalization.SpTowerWitness

namespace MUFPF.LayerBoundary

open MUFPF.CategoryOrder (catOrder nTotal nActive nTotal_eq_five)
open MUFPF.BranchCounting (LayerIndex total_layers_count)

/-! ## 一、`±1` 是代数对称包装：「去两层」是恒等式 -/

/-- ★★★ **`c - 1 = (c + 1) - 2` 对一切 `c : ℕ` 成立。**

    ⇒ 「`N_active = N_total − 2`（去掉对象层与 coherence 层）」是**定义的改写**，
    不是结构推导：那个 `−2` 就是 `+1` 的逆。 -/
theorem sub_one_eq_add_one_sub_two (c : ℕ) : c - 1 = (c + 1) - 2 := by
  omega

/-- ★★ `±1` 关于 `c` 对称：两端之和是 `2 * c`。 -/
theorem pm_one_sum (c : ℕ) (h : 1 ≤ c) : (c + 1) + (c - 1) = 2 * c := by
  omega

/-- ★★★ **括号平方**：`(c − 1)(c + 1) + 1 = c * c`（`c ≥ 1`）。

    ⇒ `B = c² − 1` **完全由 `c` 决定**，两个 offset 不提供超出 `c` 的任何信息。 -/
theorem pm_one_product_add_one (c : ℕ) (h : 1 ≤ c) : (c - 1) * (c + 1) + 1 = c * c := by
  have hc : c - 1 + 1 = c := Nat.sub_add_cancel h
  calc (c - 1) * (c + 1) + 1
      = (c - 1) * c + (c - 1) + 1 := by rw [Nat.mul_succ]
    _ = (c - 1) * c + ((c - 1) + 1) := by rw [Nat.add_assoc]
    _ = (c - 1) * c + c := by rw [hc]
    _ = c * (c - 1) + c := by rw [Nat.mul_comm (c - 1) c]
    _ = c * ((c - 1) + 1) := by rw [Nat.mul_succ]
    _ = c * c := by rw [hc]

/-- ★★★ **库内实例**：`nActive * nTotal + 1 = catOrder ^ 2`，即 `B + 1 = c²`。

    第 56 批证到 `nActive * nTotal = catOrder ^ 2 - 1`；本定理指出它的**一般形式**：
    对任意 `c` 都成立，故两个 offset 的贡献是零。 -/
theorem branch_is_bracketed_square : nActive * nTotal + 1 = catOrder ^ 2 := by
  have h := pm_one_product_add_one catOrder (by norm_num [catOrder])
  simpa [nTotal, nActive, pow_two] using h

/-! ## 二、`+1` 的「5」与 `LayerIndex` 的 5 个构造子：同值不同源 -/

/-- ★★ **此前缺失的桥**：`Fintype.card LayerIndex = nTotal`。

    建成后仍须注意：桥只接数值。左端是「该 `inductive` 有 5 个构造子」（定义停止），
    右端是 `catOrder + 1`（算术）；两端相等不解释 `+1` 的来源。 -/
theorem layerIndex_card_eq_nTotal : Fintype.card LayerIndex = nTotal :=
  total_layers_count.trans nTotal_eq_five.symm

/-- ★★ `LayerIndex` 恰有 5 个构造子（`obj` / `one` / `two` / `three` / `four`）。 -/
theorem layerIndex_stops_at_four : Fintype.card LayerIndex = 5 := total_layers_count

/-! ## 三、`+1` 的「顶层停在层 4」被库内自身反证 -/

/-- ★★★ **层 5 结构已存在且非平凡**：`SpFiveMorphism four0 four1` 有一个
    `fourthHomotopy ≠ 0` 的实例。

    出处：`SpFiveLayer.lean` L33（`structure SpFiveMorphism`）+ `SpTowerWitness.lean`
    `five0`。⇒ `N_total = 5` 的「顶层 = 层 4」不是结构事实。 -/
theorem layer_five_structure_exists :
    ∃ Ψ : SpFiveMorphism four0 four1, Ψ.fourthHomotopy ≠ 0 :=
  MUFPF.tower_height_at_least_five_B

/-- ★★★ **层标号停在 4，层结构没停**：

    `LayerIndex` 只有 5 个构造子，而层 5 有非平凡态射（且 `SpTowerUnbounded` 给出
    B 相任意层 `k ≥ 2` 的见证）⇒ 「5 层」是**类型定义停止**，不是「结构上只有 5 层」。 -/
theorem index_does_not_track_structure :
    Fintype.card LayerIndex = 5 ∧
    (∃ Ψ : SpFiveMorphism four0 four1, Ψ.fourthHomotopy ≠ 0) :=
  ⟨layerIndex_stops_at_four, layer_five_structure_exists⟩

/-! ## 四、总述 -/

/-- ★★★ **本批裁决的可机检部分**（五合取）：

    1. 「去两层」是恒等式：`∀ c, c - 1 = (c + 1) - 2`；
    2. `B = c² − 1` 由 `c` 决定：`nActive * nTotal + 1 = catOrder ^ 2`；
    3. 补上缺失的桥：`Fintype.card LayerIndex = nTotal`；
    4. 该桥的左端是定义停止：`Fintype.card LayerIndex = 5`；
    5. 而层结构没停：存在 `fourthHomotopy ≠ 0` 的 `SpFiveMorphism`。

    ⇒ 合起来：`±1` 是 `catOrder` 的对称包装，不进注入点集合（仍两项）；
    ⇒ 但 `N_total = 5` 的「5 层」是 A 相读法，B 相层数无界 ⇒ `B = 15` 的层对读法受限。 -/
theorem boundary_verdict :
    (∀ c : ℕ, c - 1 = (c + 1) - 2) ∧
    nActive * nTotal + 1 = catOrder ^ 2 ∧
    Fintype.card LayerIndex = nTotal ∧
    Fintype.card LayerIndex = 5 ∧
    (∃ Ψ : SpFiveMorphism four0 four1, Ψ.fourthHomotopy ≠ 0) :=
  ⟨sub_one_eq_add_one_sub_two, branch_is_bracketed_square, layerIndex_card_eq_nTotal,
    layerIndex_stops_at_four, layer_five_structure_exists⟩

end MUFPF.LayerBoundary
