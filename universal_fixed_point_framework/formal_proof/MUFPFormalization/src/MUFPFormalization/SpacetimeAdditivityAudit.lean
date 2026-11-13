/-
# `SpacetimeAdditivityAudit.lean` — 「时空维数 = 空间 + 时间」里那个 `+` 的地位（第 59 批）

## 本批要回答的问题

第 56–58 批把注入点一路收窄到「一项」：`timeLayerDim = 1`（其别名「`spacetimeDim = 4`」
不另计）。这三批都默认了同一件事——**`spacetimeDim` 是由 `spaceLayerDim` 与
`timeLayerDim` 相加得到的**。那个 `+` 从未被审。

本批审它。问题拆成三个：

1. 库内通往 `4` 的路径是否都依赖同一个 `+`？
2. 把 `+` 换掉，`4` 还在不在？⇒ `+` 是不是**承重**的？
3. 「总量 = 4」这个数值本身能否钉住 `+`？

## 发现一：三条通往 `4` 的定义路径共用同一个 `+`

| 定义 | 写法 | 出处 |
|---|---|---|
| `spacetimeDim` | `spaceLayerDim + timeLayerDim` | `SpacetimeDimensionTwoPostulates` L62 |
| `catOrderOf d` | `d + timeLayerDim` | `CatOrderFromSpacetime` L102 |
| `catOrderOfTime d t` | `d + t` | `CatOrderIsTimeOnly` L103 |

本批 `three_routes_all_use_add` 把它们四个（含两两相等）用 `⟨rfl, rfl, rfl, rfl⟩`
一次证完 ⇒ 三者**逐字**共用 `+`，不是三个独立巧合。

⇒ **`+` 是三条 `4` 的公共前提，也是至今唯一从未被审的一环。**

## 发现二：`+` 是承重的 —— 换掉它 `4` 就消失

本批逐一算出五种组合律在 `(spaceLayerDim, timeLayerDim) = (3, 1)` 处的取值：

| 组合律 | 取值 |
|---|---|
| `+` | **4** |
| `*` | 3 |
| `^` | 3 |
| `max` | 3 |
| `succ`（只看空间） | **4** |

⇒ `combination_law_is_load_bearing`：`spaceLayerDim * timeLayerDim ≠ spacetimeDim`
（3 ≠ 4）。⇒ **`4` 不是由 `3` 与 `1` 一对数唯一决定的，还依赖组合律。**
⇒ `catOrder = 4`、`N_total = 5`、`B = 15` 全都挂在 `+` 上。

## 发现三：换掉 `+` 的后果在库内**可观测**

`clStateCount := 2 ^ spacetimeDim`（L65），`cl31_state_count : clStateCount = 16`（L89）。

若组合律是 `*`，`clStateCount` 会变成 `2 ^ (3 * 1) = 8`：

```
2 ^ (spaceLayerDim * timeLayerDim) ≠ clStateCount      -- 8 ≠ 16
```

⇒ `+` 的选择不是「记法」，它把 `Cl(3,1)` 的态数从 8 改成 16。**库内有一个具体的
被观测量随 `+` 变动。**

同时 `sigmaInv := spaceLayerDim * silenceUnit`（L74）用的是**乘法**，`sigmaInv = 15`。
⇒ 库内 `+` 与 `*` 是分工的（维数用 `+`、乘积计数用 `*`），`+` 不是随手写的。

## 发现四：「总量 = 4」对组合律**零约束**

`add_not_pinned_by_value_at_one_point`：

```
¬ ∀ (⊕ : ℕ → ℕ → ℕ), ⊕ 3 1 = 4 → ∀ b, ⊕ 3 b = 3 + b
```

反例 `⊕ a b := a + 2 * b - 1`：在 `(3, 1)` 处恰给 `4`，但在 `(3, 2)` 处给 `6 ≠ 5`。
⇒ **单点值 `⊕ 3 1 = 4` 不能钉出 `⊕` 是加法。** 知道「总量 = 4」对「总量怎么算出来的」
一无所知。

## 发现五：时间层数 = 1 的全部算术内容就是「加一」

```
spacetimeDim = Nat.succ spaceLayerDim          -- total_is_succ
catOrderOf spaceLayerDim = Nat.succ spaceLayerDim
spacetimeDim - spaceLayerDim = timeLayerDim    -- time_layer_is_the_gap
```

⇒ `timeLayerDim = 1` 的算术作用只是把空间层数**推进一格**——
与第 57 批 `StrictLayer` 的 `layerOf (ev r) = layerOf r + 1` 是同一件事。
⇒ 「时空四维」= 「空间三维再进一层」。这是一个**结构性较好的读法**，
但它不增加也减少注入：`1` 仍是 `1`。

## 裁决

1. **`+` 是三条 `4` 的公共前提，此前从未被任何批次审过。** 第 56–58 批把 `+`
   当透明背景，本批证明它不透明。
2. **`+` 是承重的、且库内可观测**（`clStateCount` 16 vs 8）。⇒ 它不是记法选择。
3. **但 `+` 不是「无源」型注入，而是「有物理含义、未形式化」型假设。**
   「维数在直积下可加」是唯一合法依据（`dim (X × Y) = dim X + dim Y`）；然而
   `SpObj` 只有 `(n, A)`（第 43 批），库内**没有**积分解、也没有
   `dim : Type → ℕ`。⇒ 登记 `additivity_lacks_product_witness`。
4. **注入点计数因此需要修正为「两项」**：`{timeLayerDim = 1, 组合律 = 加法}`。
   第 56–58 批的「一项」漏算了 `+`。若日后把「维数积可加」建成结构（给出
   `Sp` 的积分解 + 加法性 `dim`），则 `+` 可免、回到一项；在此之前应按两项记。
5. **「总量 = 4」不能替代对 `+` 的说明**（发现四）：数值对运算零约束。
6. **未就地改 Lean doc。** 同第 57/58 批策略，`CatOrderFromSpacetime` L68/L96、
   `SpacetimeDimensionTwoPostulates` L136 三处偏强标注仍只登记不改，待裁决。
-/

import Mathlib.Tactic
import MUFPFormalization.SpacetimeDimensionTwoPostulates
import MUFPFormalization.CatOrderIsTimeOnly
import MUFPFormalization.CatOrderFromSpacetime
import MUFPFormalization.SpacetimeTotalAudit

namespace MUFPF.SpacetimeAdditivity

open MUFPF.SpacetimeDimensionTwoPostulates
  (spaceLayerDim timeLayerDim spacetimeDim clStateCount kMax silenceUnit sigmaInv)

/-! ## 一、加法左消去：给定首项，第二项被唯一确定 -/

/-- 加法**左消去**：给定空间层数，时间层数就被唯一确定。

    ⇒ 「时空分解成 `3 + 1`」这个说法不携带信息：只要首项已知，第二项是定义出来的。 -/
theorem add_left_cancel_iff (d a b : ℕ) : d + a = d + b ↔ a = b :=
  ⟨Nat.add_left_cancel, fun h => by rw [h]⟩

/-! ## 二、「总量 = 4」不能钉住组合律 -/

/-- ★★★ **单点值 `⊕ 3 1 = 4` 推不出 `⊕` 是加法。**

    反例 `⊕ a b := a + 2 * b - 1`：在 `(3, 1)` 处恰给 `4`，在 `(3, 2)` 处给 `6 ≠ 5`。
    ⇒ 知道「总量 = 4」对「总量由什么运算得出」零约束。 -/
theorem add_not_pinned_by_value_at_one_point :
    ¬ ∀ (oplus : ℕ → ℕ → ℕ), oplus 3 1 = 4 → ∀ b : ℕ, oplus 3 b = 3 + b := by
  intro h
  have hcv : (fun a b : ℕ => a + 2 * b - 1) 3 1 = (4 : ℕ) := by norm_num
  have hbad : (fun a b : ℕ => a + 2 * b - 1) 3 2 = (3 + 2 : ℕ) :=
    h (fun a b : ℕ => a + 2 * b - 1) hcv 2
  norm_num at hbad

/-! ## 三、`+` 是承重的：换掉它 `4` 就消失 -/

/-- 若组合律取乘法，得 3。 -/
theorem mul_reading_gives_three : spaceLayerDim * timeLayerDim = 3 := by
  norm_num [spaceLayerDim, timeLayerDim]

/-- 若组合律取乘幂，得 3。 -/
theorem pow_reading_gives_three : spaceLayerDim ^ timeLayerDim = 3 := by
  norm_num [spaceLayerDim, timeLayerDim]

/-- 若组合律取上确界，得 3。 -/
theorem max_reading_gives_three : max spaceLayerDim timeLayerDim = 3 := by
  norm_num [spaceLayerDim, timeLayerDim]

/-- ★★★ **组合律承重**：`3 * 1 = 3 ≠ 4 = spacetimeDim`。

    ⇒ `4` 不是由 `3` 与 `1` 一对数唯一决定的，还依赖组合律。 -/
theorem combination_law_is_load_bearing : spaceLayerDim * timeLayerDim ≠ spacetimeDim := by
  norm_num [spaceLayerDim, timeLayerDim, spacetimeDim]

/-- ★★★ **换掉 `+` 的后果在库内可观测**：乘法读法会把 `clStateCount` 从 16 改成 8。

    ⇒ `+` 不是记法选择，它决定了 `Cl(3,1)` 的态数。 -/
theorem mul_reading_breaks_clifford_count :
    2 ^ (spaceLayerDim * timeLayerDim) ≠ clStateCount := by
  norm_num [spaceLayerDim, timeLayerDim, clStateCount, spacetimeDim]

/-- ★★ **反证：库内 `+` 与 `*` 是分工的**——`sigmaInv` 用乘法（正因如此 `sigmaInv = 15`），
    而维数用加法。⇒ `+` 不是随手写的。 -/
theorem sigmaInv_uses_mul : sigmaInv = spaceLayerDim * silenceUnit := rfl

/-! ## 四、时间层数 = 1 的全部算术内容就是「加一」 -/

/-- ★★★ **`spacetimeDim = Nat.succ spaceLayerDim`**：时间只把空间层数推进一格。 -/
theorem total_is_succ : spacetimeDim = Nat.succ spaceLayerDim := by
  norm_num [spacetimeDim, spaceLayerDim, timeLayerDim]

/-- ★★ `catOrder` 同样是 `Nat.succ spaceLayerDim`。 -/
theorem catOrder_is_succ :
    MUFPF.CatOrderSpacetime.catOrderOf spaceLayerDim = Nat.succ spaceLayerDim := by
  norm_num [MUFPF.CatOrderSpacetime.catOrderOf, MUFPF.CatOrderSpacetime.timeLayerDim,
    spaceLayerDim]

/-- ★★★ **差额恰是时间层数**：`总量 − 空间 = 时间 = 1`。 -/
theorem time_layer_is_the_gap : spacetimeDim - spaceLayerDim = timeLayerDim := by
  norm_num [spacetimeDim, spaceLayerDim, timeLayerDim]

/-! ## 五、三条通往 `4` 的定义路径共用同一个 `+` -/

/-- ★★★ **三条路径逐字共用 `+`**（四个分量全部 `rfl`）：

    `catOrderOf spaceLayerDim`、`catOrderOfTime spaceLayerDim timeLayerDim`、
    `spacetimeDim`、以及前两者相等，都在同一个 `d + t` 上。 -/
theorem three_routes_all_use_add :
    MUFPF.CatOrderSpacetime.catOrderOf spaceLayerDim = spacetimeDim ∧
    MUFPF.CatOrderTimeOnly.catOrderOfTime spaceLayerDim timeLayerDim = spacetimeDim ∧
    spacetimeDim = spaceLayerDim + timeLayerDim ∧
    MUFPF.CatOrderTimeOnly.catOrderOfTime spaceLayerDim timeLayerDim
      = MUFPF.CatOrderSpacetime.catOrderOf spaceLayerDim :=
  ⟨rfl, rfl, rfl, rfl⟩

/-! ## 六、总述 -/

/-- ★★★ **本批裁决的可机检部分**（五合取）：

    1. 组合律承重：`spaceLayerDim * timeLayerDim ≠ spacetimeDim`；
    2. 承重且库内可观测：`2 ^ (spaceLayerDim * timeLayerDim) ≠ clStateCount`；
    3. 时间只贡献一格：`spacetimeDim = Nat.succ spaceLayerDim`；
    4. 加法左消去：`∀ d a b, d + a = d + b ↔ a = b`；
    5. 库内 `+` 与 `*` 分工：`sigmaInv = spaceLayerDim * silenceUnit`。

    ⇒ 合起来：`+` 是三条 `4` 的公共前提、承重、库内可观测，且数值 4 对运算零约束；
    ⇒ 注入点应从「一项」修正为「两项」：`{timeLayerDim = 1, 组合律 = 加法}`。 -/
theorem additivity_verdict :
    spaceLayerDim * timeLayerDim ≠ spacetimeDim ∧
    2 ^ (spaceLayerDim * timeLayerDim) ≠ clStateCount ∧
    spacetimeDim = Nat.succ spaceLayerDim ∧
    (∀ d a b : ℕ, d + a = d + b ↔ a = b) ∧
    sigmaInv = spaceLayerDim * silenceUnit :=
  ⟨combination_law_is_load_bearing, mul_reading_breaks_clifford_count, total_is_succ,
    fun d a b => add_left_cancel_iff d a b, sigmaInv_uses_mul⟩

end MUFPF.SpacetimeAdditivity
