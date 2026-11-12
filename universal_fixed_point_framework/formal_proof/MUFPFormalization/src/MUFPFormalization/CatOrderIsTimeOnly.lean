import Mathlib.Tactic
import MUFPFormalization.ActiveLayerIsSpaceLayer

/-!
# CatOrderIsTimeOnly.lean — `catOrder = 4` 不是独立输入（第 37 批）

## 本批先勘破一条路线，并发现一处注释已过时

第 36 批 §21.47.9 拟的路线 3 是：若 `t ≥ 2` 则 `catOrder = d + t ≥ 5`，与 `Sp` 是
严格 4-范畴冲突 ⇒ `t = 1`。这条**已勘破**，依据是库内自查：

```
SpFiveLayer.lean L33            structure SpFiveMorphism（层 5 结构，逐字同形于 SpFourMorphism）
SpTowerWitness.lean L110        def five0 : SpFiveMorphism four0 four1     （实例存在）
SpTowerWitness.lean L126        ∃ Ψ : SpFiveMorphism four0 four1, Ψ.fourthHomotopy ≠ 0 （非退化）
MUFPFormalization.lean L171     import MUFPFormalization.SpFiveLayer        （在库根闭包内）
MUFPFormalization.lean L172     import MUFPFormalization.SpTowerWitness     （在库根闭包内）
```

⇒ **「`Sp` 是严格 4-范畴」在库里不成立：层 5 有结构、有非退化实例。**
所以「`catOrder ≥ 5` 冲突」这个反证无效，路线 3 作废。

顺带查出**一处注释已过时**（本批登记，未改档）：

```
SpTowerCriterion.lean L4
-- 背景：库内没有 `SpFiveMorphism`，层 4 是现存的最高层。
```

`SpFiveLayer.lean` 补出了 `SpFiveMorphism` 且在库根闭包内，该行注释与现状不符。
**本批不改它**（改一行 doc 也触发全库重编；且 `SpTowerCriterion` 的其余论证不依赖这行），
仅登记于笔记 §21.48.2，留待后续批次统一订正。

（同理 `SpFiveLayer.lean` L4「库内层结构止于 SpFourMorphism」已由本文件自身否证。）

## 主结果：`catOrder = 4` 与 `t = 1` 是同一个陈述，不是两处输入

第 33 批的 `ActiveFromCategoryOrder.lean` 写

```lean
def catOrder : ℕ := 4
```

并在 doc 里说「`n = 4` 由层表算出」。第 34 批把它重写成 `catOrderOf d := d + timeLayerDim`。
本批把两件事一起说清：

**（一）`catOrder` 不是 `Sp` 的结构读数。** 因为层 5 存在（上面四条证据），
「`Sp` 恰好 4 层」为假。`catOrder = 4` 只能来自 `d + t`，而 `d = 3` 是第 32 批方程的解。

**（二）`catOrder = 4` ⟺ `t = 1`（在 `d = 3` 下）。** 这是本批的机检核心
（`catOrder_four_iff_time_one`）。既然两者等价，`catOrder = 4` **不能作为独立的结构输入**
去推 `t = 1`——那是把同一个 `1` 数两遍。

⇒ **注入点清单里「`catOrder = 4`」与「`timeLayerDim = 1`」是同一处，不是两处。**

## 解耦：`N_active` 不知道 `t` 存在，`catOrder` 随 `t` 漂移

两条一正一反，构成完整机检：

```
nactive_decoupled_from_time   (d t₁ t₂) : (d+t₁)−t₁ = (d+t₂)−t₂        ★★★
catorder_not_decoupled        (d t₁ t₂) (h : t₁ ≠ t₂) : d+t₁ ≠ d+t₂    ★★★
```

⇒ **`N_active` 恒等于 `d`，与 `t` 无关；`catOrder` 严格随 `t` 变。**
所以 `catOrder` 那条链的不稳定性（它依赖 `t = 1`，而 `t = 1` 未证）**不会传染到 `N_active`**。

`nactive_three_while_catorder_moves` 把两者放到同一条定理里：
`N_active = 3`（固定）与 `catOrder = 3 + t`（漂移）并存，说明 `N_active` 不是从 `catOrder`
读出来的。

## 注入点清点（第 37 批后）

| # | 注入点 | 状态 |
|---|---|---|
| ① | 「主动层 = 排除对象层与 coherence 层」 | 第 36 批判不可普遍证，已替换为真命题 |
| ② | `timeLayerDim = 1` | 不影响 `N_active`；且与 `catOrder = 4` 是同一处，不是两处 |
| — | `catOrder = 4` | 第 37 批并入 ②，不再独立计数 |
| ③ | `spaceLayerDim = 3` | 第 32 批：`2^d = b³` 的唯一解；`b` 是第 35 批方程的解 |

⇒ **`N_active = 3` 的链条上只剩 ③ 一处，而 ③ 不是字面量，是方程 `2^d = 2³` 的唯一解。**

## 边界

1. 本批**不 import** `HigherSpCategory` / `SpFiveLayer`——它们会引入 simp 扰动（已知坑）。
   「层 5 存在」以 Grep 行号作事实引用，**未在 Lean 内机检为定理**。这一条标注清楚。
2. `catOrder_four_iff_time_one` 需要在 `d = 3` 的前提下（`hD`）。无 `hD` 时
   `d + t = 4 ↔ (d,t) = (4,0) ∨ (3,1) ∨ (2,2) ∨ (1,3) ∨ (0,4)`——本批不展开。
3. 本批不改 `ActiveFromCategoryOrder.lean` 的 `def catOrder : ℕ := 4`（已提交）。
   只证明它与 `t = 1` 等价，从而取消其独立输入地位。
4. 「层 5 存在 ⇒ `catOrder` 是约定」这个推理是**文字论证**（Grep 证据 + 语义），
   不是 Lean 定理。它给出的是「第 33 批那句『由层表算出』应读作『是约定』」，
   而不是一个形式化反证。
-/

namespace MUFPF.CatOrderTimeOnly

open MUFPF.ActiveIsSpace
open MUFPF.PowersCube
open MUFPF.CatOrderSpacetime

/-- 时间参数化的范畴阶：`d + t`。 -/
def catOrderOfTime (d t : ℕ) : ℕ := d + t

/-- 定义展开。 -/
theorem catOrderOfTime_eq (d t : ℕ) : catOrderOfTime d t = d + t := rfl

/-- ★★ `spaceLayerDim = 3` 的前提下，范畴阶 = `3 + t`。 -/
theorem catOrder_eq_three_add_time (d t : ℕ) (hD : 2 ^ d = fixedPoint * powers) :
    catOrderOfTime d t = 3 + t := by
  unfold catOrderOfTime
  rw [spaceLayerDim_unique d hD]

/-- ★★★ **`catOrder = 4` ⟺ `t = 1`**（在 `spaceLayerDim = 3` 下）。

    核心：`catOrder = 4` 不是独立的结构输入，它与 `timeLayerDim = 1` 是同一个陈述。
    若把 `catOrder = 4` 再当作前提去推 `t = 1`，是把同一个 1 数两遍。 -/
theorem catOrder_four_iff_time_one (d t : ℕ) (hD : 2 ^ d = fixedPoint * powers) :
    catOrderOfTime d t = 4 ↔ t = 1 := by
  rw [catOrder_eq_three_add_time d t hD]
  omega

/-- ★★ **`catOrder` 随 `t` 漂移**：不同时间层数给出不同范畴阶。 -/
theorem catorder_not_decoupled (d t₁ t₂ : ℕ) (h : t₁ ≠ t₂) :
    catOrderOfTime d t₁ ≠ catOrderOfTime d t₂ := by
  unfold catOrderOfTime
  omega

/-- ★★★ **`N_active` 不知道 `t` 存在**：任意两个时间层数给出同一个主动层数。 -/
theorem nactive_decoupled_from_time (d t₁ t₂ : ℕ) :
    nActiveOfTime d t₁ = nActiveOfTime d t₂ := by
  unfold nActiveOfTime
  omega

/-- ★★★ **并存但不同**：`N_active` 固定为 3，`catOrder` 随 `t` 漂移。
    ⇒ `N_active` 不是从 `catOrder` 读出来的。 -/
theorem nactive_three_while_catorder_moves (d t : ℕ)
    (hD : 2 ^ d = fixedPoint * powers) :
    nActiveOfTime d t = 3 ∧ catOrderOfTime d t = 3 + t := by
  exact ⟨nActive_eq_three_no_time d t hD, catOrder_eq_three_add_time d t hD⟩

/-- ★★ **注入点只剩一处**：`N_active = 3` 对任意 `t` 成立，唯一结构性前提是
    `spaceLayerDim = 3`（第 32 批 `2^d = b³` 的唯一解；`b` 由第 35 批方程钉住）。 -/
theorem only_one_input_left (d : ℕ) (hD : 2 ^ d = fixedPoint * powers) :
    (∀ t : ℕ, nActiveOfTime d t = 3) ∧
      (∀ t : ℕ, catOrderOfTime d t = 3 + t) ∧
      catOrderOfTime d 1 = 4 := by
  refine ⟨fun t => nActive_eq_three_no_time d t hD,
          fun t => catOrder_eq_three_add_time d t hD, ?_⟩
  unfold catOrderOfTime
  rw [spaceLayerDim_unique d hD]

/-- ★ 第 34 批口径的一致性：`t = timeLayerDim` 时本批的 `catOrderOfTime` 等于 `catOrderOf`。 -/
theorem catOrderOfTime_eq_catOrderOf (d : ℕ) :
    catOrderOfTime d timeLayerDim = catOrderOf d := by
  unfold catOrderOfTime catOrderOf
  rw [timeLayerDim_eq_one]

end MUFPF.CatOrderTimeOnly
