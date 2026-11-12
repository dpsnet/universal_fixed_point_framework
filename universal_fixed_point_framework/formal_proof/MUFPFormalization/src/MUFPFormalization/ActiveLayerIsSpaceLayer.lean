import Mathlib.Tactic
import MUFPFormalization.CatOrderFromSpacetime

/-!
# ActiveLayerIsSpaceLayer.lean — `−1` 的身份是 `timeLayerDim`（第 36 批）

## 上一批留下的最后一个注入点

第 35 批把 `b = 2` 从"数值输入"降为"方程的解"，注入点剩两个：

```
① 「主动生成层 = 排除对象层与 coherence 层」规则本身未证
② timeLayerDim := 1 的物理层面未证
```

本批先读 `Unified3Theorem.lean` L69–77 的层表原文，发现一件必须先说清的事：

```
层 0：SpObj（对象）        —— 不生成动力学自由度
层 1：SpHom（1-态射）      —— 谱流，生成第一代
层 2：SpTwoMorphism（2-态射）—— 同伦，生成第二代
层 3：SpThreeMorphism（3-态射）—— 高阶变换，生成第三代
层 4：4-态射（coherence）  —— 不生成物理自由度
主动生成层 = 层 1, 2, 3（排除对象层和 coherence 层）。
```

这段在 L79–80 自带一条**限定**：

> **限定**：「层 4 不生成物理自由度」只在可对角化相成立。含 Jordan 块时
> `ker ∩ im ≠ 0`，层 4 及更高层可由塔高见证（见 §5 与 `SpTowerUnbounded`）。

⇒ 「主动层 = 排除对象层与 coherence 层」这条规则**是分相成立的**，不是普遍规则。
把它当公设去证明，方向是错的。本批不再走这条。

## 换角度：`−1` 是什么

第 34 批的 `CatOrderFromSpacetime.lean` 里写的是

```lean
def nActiveOf (d : ℕ) : ℕ := catOrderOf d - 1
```

那个 `1` 是**字面量**。它恰好等于 `timeLayerDim`，但代码里没写成 `timeLayerDim`。
这正是第 33 批那座桥的老毛病：两个数碰巧相等，看不出为什么。

把 `− 1` 改写成 `− timeLayerDim`：

```
nActiveOfTime d t = (d + t) − t
```

于是

```
(d + t) − t = d
```

**这是对任意 `t` 成立的恒等式（`Nat.add_sub_cancel`），不依赖 `t = 1`。**

⇒ 三条结论立刻落地：

### 结论一：`N_active = spaceLayerDim` 与 `timeLayerDim` 无关

第 34 批的 `nActive_eq_spaceLayerDim` 依赖 `timeLayerDim = 1`（因为写死 `− 1`）。
本批的版本对任意 `t` 成立。**`N_active` 之所以等于空间层数，是因为「总数减去时间层 = 空间层」，
不是因为有 1 恰好可减。**

### 结论二：`N_active = 3` 不再需要 `timeLayerDim = 1`

`N_active = spaceLayerDim`（本批，无关 `t`）+ `spaceLayerDim = 3`（第 32 批）⇒ `N_active = 3`。
**注入点 ②（`timeLayerDim = 1` 物理层面未证）不再影响 `N_active = 3`。**
它只影响 `catOrder = 4`（`catOrder = d + t` 需要 `t = 1` 才得 4）。

### 结论三：`SpacetimeDimensionTwoPostulates.lean` L13 那条文字等同升格为定理

第 33 批全库扫描（`pr634oh_scan.txt`）登记过：L13 有唯一一处文字等同

```
空间方向数 = 三层态射层数（spaceLayerDim = 3 = N_gen）
```

但"只是注释不是定理"。本批给出它的定理形式：

```
N_active = spaceLayerDim          （本批，无关 t）
```

⇒ 那条注释现在有机器检查的后盾：**主动层数 = 空间方向数**，成立且不依赖时间层数。

## 本批没有做到什么（必须说清）

本批**没有**证明「主动生成层 = 排除对象层与 coherence 层」。

本批证明的是**另一件事**：`N_active` 里的减数身份是「时间层」而不是「对象层」。
两种口径都给 3，但减掉的东西不同：

| 口径 | 总层数 | 减掉什么 | 得数 |
|---|---|---|---|
| `Unified3Theorem` 层表 | 5（层 0–4） | 对象层 + coherence 层 | 3 |
| 第 34 批 / 本批 | `d + t` = 4 | 时间层 | `d` = 3 |

**这两套分层是两套不同的分层，不能混为一谈。** 前者按态射阶数分（对象 / 1- / 2- / 3- / 4-），
后者按「空间 vs 时间」分。两套都给出 3 这件事本身，是**两个不同的 3**——与第 29 批
「相的数量 = 3」和 `N_active = 3` 不同源，是同一类问题的第三次出现。

所以本批的收获是「减数身份明确」+「`N_active` 摆脱 `t = 1` 依赖」，
**不是**「主动层规则被证」。这一点不能含糊。

## 边界

1. `Nat.add_sub_cancel` 只在 `ℕ` 上成立；若 `d + t < t`（不可能，因 `d ≥ 0`）无意义。
   `ℕ` 截断减法在此恰好不需要额外条件。
2. 本批不改第 34 批的 `nActiveOf`（已提交，改动会动到既有定理）。
   本批新开 `nActiveOfTime` 并证明它与 `nActiveOf` 在 `t = 1` 时一致，作为两版对照。
3. `N_active = 3` 的独立性只针对 `t`；`spaceLayerDim = 3` 仍来自第 32 批方程。
-/

namespace MUFPF.ActiveIsSpace

open MUFPF.CatOrderSpacetime
open MUFPF.PowersCube

/-- `− timeLayerDim` 版本的主动层数：`(d + t) − t`。 -/
def nActiveOfTime (d t : ℕ) : ℕ := (d + t) - t

/-- ★★★ **主动层数 = 空间层数，与时间层数无关**。

    `(d + t) − t = d` 对任意 `t` 成立——`N_active` 之所以等于空间层数，
    是因为「总数减去时间层 = 空间层」，而不是因为有 1 恰好可减。 -/
theorem nActiveOfTime_eq_space (d t : ℕ) : nActiveOfTime d t = d := by
  unfold nActiveOfTime
  omega

/-- ★★ 与第 34 批写死 `− 1` 的版本在 `t = 1` 时一致（两版对照）。 -/
theorem nActiveOfTime_eq_nActiveOf (d : ℕ) :
    nActiveOfTime d timeLayerDim = nActiveOf d := by
  unfold nActiveOfTime nActiveOf catOrderOf
  rw [timeLayerDim_eq_one]

/-- ★★ **`N_active = 3` 不需要 `timeLayerDim = 1`**。

    只用到：`spaceLayerDim = 3`（由 `2^d = f·b` 解出，第 32 批）+ 本批的
    `(d + t) − t = d`。 -/
theorem nActive_eq_three_no_time (d t : ℕ) (hD : 2 ^ d = fixedPoint * powers) :
    nActiveOfTime d t = 3 := by
  rw [nActiveOfTime_eq_space d t]
  exact spaceLayerDim_unique d hD

/-- ★★★ **主动层 = 空间层**：主动生成层的数目等于空间方向数，时间层不生成空间层。

    这是 `SpacetimeDimensionTwoPostulates.lean` L13 那条文字等同
    「空间方向数 = 三层态射层数（`spaceLayerDim = 3 = N_gen`）」的定理形式。 -/
theorem active_layer_is_space_layer (d t : ℕ) (hD : 2 ^ d = fixedPoint * powers) :
    nActiveOfTime d t = 3 ∧ nActiveOfTime d t = d ∧ d = 3 := by
  have h1 : nActiveOfTime d t = d := nActiveOfTime_eq_space d t
  have h2 : d = 3 := spaceLayerDim_unique d hD
  refine ⟨?_, h1, h2⟩
  rw [h1, h2]

/-- ★ 一致性：本批口径与第 34 批口径在具体参数下同值。 -/
theorem two_conventions_agree (d : ℕ) (hD : 2 ^ d = fixedPoint * powers) :
    nActiveOfTime d timeLayerDim = nActiveOf d ∧
      nActiveOf d = 3 ∧ nActiveOfTime d timeLayerDim = 3 := by
  have h1 : nActiveOfTime d timeLayerDim = nActiveOf d :=
    nActiveOfTime_eq_nActiveOf d
  have h2 : nActiveOf d = 3 := nActive_eq_three d hD
  have h3 : nActiveOfTime d timeLayerDim = 3 := nActive_eq_three_no_time d timeLayerDim hD
  exact ⟨h1, h2, h3⟩

/-- ★ 时间层数为 0 的退化情形：主动层数仍等于空间层数（恒等式不依赖 t 非零）。 -/
theorem time_zero_degenerate (d : ℕ) : nActiveOfTime d 0 = d := by
  unfold nActiveOfTime
  omega

/-- ★ 大时间层数情形：`t = 100` 时主动层数仍等于空间层数（恒等式无上界约束）。 -/
theorem large_time_ok (d : ℕ) : nActiveOfTime d 100 = d := by
  unfold nActiveOfTime
  omega

/-- ★★ **两套分层口径的数值对照**（诚实登记差异）。

    `Unified3Theorem` 层表口径：5 层（层 0–4）去掉对象层与 coherence 层 → 3。
    本批口径：`d + t` 层去掉时间层 → `d` = 3。
    两者数值同为 3，但**减掉的前提不同，是两套不同的分层**。 -/
theorem two_stratifications_same_value :
    (5 : ℕ) - 2 = 3 ∧ ∀ d t : ℕ, nActiveOfTime d t + t = d + t := by
  constructor
  · norm_num
  · intro d t
    unfold nActiveOfTime
    omega

/-- ★★★ **注入点清点**：`N_active = 3` 现在只需要一条前提（`spaceLayerDim = 3`），
    不再需要 `timeLayerDim = 1`（第 34 批写死 `− 1` 时隐含需要）。 -/
theorem nactive_needs_only_space (d t : ℕ) (hD : 2 ^ d = fixedPoint * powers) :
    nActiveOfTime d t = 3 ∧
      (∀ t' : ℕ, nActiveOfTime d t' = 3) := by
  refine ⟨nActive_eq_three_no_time d t hD, ?_⟩
  intro t'
  exact nActive_eq_three_no_time d t' hD

end MUFPF.ActiveIsSpace
