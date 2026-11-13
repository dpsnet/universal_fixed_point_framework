/-
# 分支数 B = 15 的真身：`catOrder` 的相邻整数之积

## 本批要回答的问题

第 55 批把「推出 3」主线的注入点收窄为「两项半」，其中一项是 `N_total = 5`。
库内存在**两套关于它的说法**，且从未接上：

- `DHStructuralAnalysis.lean` L109：`def N_total : ℕ := 5` —— 裸字面量，doc 自承
  「本库把对象层 0 计入 `N_total`，故取 5；论文 §5.5 的 `N_total = N_active + 1 = 4`
  不含对象层。两者是**不同口径的计数**」；
- `ActiveFromCategoryOrder.lean` L96：`def nTotal : ℕ := catOrder + 1` —— 由范畴阶算出，
  且 `nTotal_eq_five` 已是定理。

⇒ 于是问题不是「5 从哪来」，而是「`3 × 5` 到底是不是一个独立的前提」。

## 本批的答案

`N_active = catOrder − 1`、`N_total = catOrder + 1`（后者在 `CategoryOrder` 里就是定义）。
因此有效分支数

```
B = N_active · N_total = (c − 1)(c + 1) = c² − 1 ，  c := catOrder
```

而 Mersenne 数 `M_c = 2^c − 1`。本批主定理证明：

> **`(c − 1)(c + 1) = 2^c − 1 ⟺ c = 4`（`c ≥ 3`）**

⇒ 所以 `B = 15` 既等于 `3 × 5`，也等于 `2^4 − 1 = M_4`，**并不是两条竞争路线，
而是 `c² − 1` 与 `2^c − 1` 在自指方程 `c² = 2^c` 的唯一非平凡解处的同值**。

⇒ 第 53/54 批已证 `f² = 2^f ⟺ f = 4`（`f ≥ 3`）；本批把其中的 `f² − 1` 换成
因式分解 `(c−1)(c+1)`，从而把「层对计数 `3 × 5`」与「Mersenne `M_4`」接成同一件事。

## 为什么必须限制 `c ≥ 3`

数值先证伪（模式 8，`c` 扫 0..40）显示全域解集是 `{2, 4}`：

```
c = 2 ： (2−1)(2+1) = 1·3 = 3 = 2² − 1   ← 平凡解，也在解集内
c = 3 ： 8  vs  7     差 +1
c = 4 ： 15 vs 15     差  0
c = 5 ： 24 vs 31     差 −7
c = 6 ： 35 vs 63     差 −28
c = 8 ： 63 vs 255    差 −192
c = 10： 99 vs 1023   差 −924
```

⇒ `c = 2` 是自指方程 `c² = 2^c` 的平凡解（`f = 2`），与第 51 批全域解集
`{(2,2),(2,4)}` 里的 `f = 2` 同源。框架域是 `c = catOrder = 4 > 2`，故全部陈述
带 `3 ≤ c` 前提；这与第 54 批 `sq_selfref_iff_four` 的前提一致。

## 与既有模块的关系

- `ActiveFromCategoryOrder`：提供 `catOrder` / `nTotal` / `nActive` / `nTotal_eq_five`。
- `ConstantDualForms`：提供 `sq_selfref_iff_four`（`f ≥ 3` 上 `f² = 2^f ⟺ f = 4`）。
- `SigmaFormOrigin`：提供 `sub_one_injective`（两侧 `≥ 1` 时 `a − 1 = b − 1 ⇒ a = b`）。
- `DHStructuralAnalysis`：提供裸定义 `N_active` / `N_total` / `B` 与 `B_eq_15`；
  本批给它们的桥接，但不改其定义（第 55 批登记的「是否就地订正 doc」仍待裁决）。
-/

import Mathlib.Tactic
import MUFPFormalization.ActiveFromCategoryOrder
import MUFPFormalization.DHStructuralAnalysis
import MUFPFormalization.ConstantDualForms

namespace MUFPF.BranchCountOrigin

open MUFPF.CategoryOrder (catOrder nTotal nActive)
open MUFPF.ConstantDualForms (sq_selfref_iff_four)
open MUFPF.SigmaFormOrigin (sub_one_injective)

/-! ## 一、因式分解：`B` 是 `catOrder` 的相邻整数之积 -/

/-- ★★ **`(c − 1)(c + 1) = c² − 1`**（`c ≥ 1`）。

⇒ `N_active = c − 1` 与 `N_total = c + 1` 的乘积不是两个独立计数的拼接，
而是「`c²` 少一格」。这一步把 `B` 从「3 × 5」改写成「`catOrder² − 1`」。 -/
theorem pair_product_eq_sq_sub_one (c : ℕ) :
    (c - 1) * (c + 1) = c ^ 2 - 1 := by
  calc (c - 1) * (c + 1)
      = c * (c + 1) - 1 * (c + 1) := by rw [Nat.sub_mul]
    _ = c * (c + 1) - (c + 1) := by rw [Nat.one_mul]
    _ = c * c + c - (c + 1) := by rw [Nat.mul_add, Nat.mul_one]
    _ = c * c + c - (1 + c) := by rw [Nat.add_comm c 1]
    _ = c * c - 1 := by rw [Nat.add_sub_add_right]
    _ = c ^ 2 - 1 := by rw [pow_two]

/-- `nTotal` 就是 `catOrder + 1`（定义即等式，不含额外内容）。 -/
theorem ntotal_is_catOrder_add_one : nTotal = catOrder + 1 := rfl

/-- ★ **`B = catOrder² − 1`**（在 `CategoryOrder` 口径下）。 -/
theorem branch_sq_form : nActive * nTotal = catOrder ^ 2 - 1 := by
  have hp := pair_product_eq_sq_sub_one catOrder
  simpa [nActive, nTotal] using hp

/-- ★★ **`B = catOrder² − 1` 同时等于 `2^catOrder − 1`**（`catOrder = 4` 处）。 -/
theorem branch_eq_mer : nActive * nTotal = 2 ^ catOrder - 1 := by
  norm_num [nActive, nTotal, catOrder]

/-- `B = 15`（层对计数的算术结果）。 -/
theorem branch_eq_fifteen : nActive * nTotal = 15 := by
  norm_num [nActive, nTotal, catOrder]

/-! ## 二、主定理：Mersenne 表示只在 `c = 4` 与平方表示同值 -/

/-- ★★★ **`(c − 1)(c + 1) = 2^c − 1 ⟺ c = 4`**（`c ≥ 3`）。

两段合成：
1. 左式经 `pair_product_eq_sq_sub_one` 改写为 `c² − 1`；
2. 两侧各 `≥ 1`，故 `c² − 1 = 2^c − 1 ⟺ c² = 2^c`（`sub_one_injective`）；
3. `c² = 2^c ⟺ c = 4`（`sq_selfref_iff_four`，`c ≥ 3`）。

⇒ 结论：**「层对计数」与「Mersenne `M_c`」不是两条路线**，它们在且仅在
`c = 4` 处同值，而同值的判据正是自指方程 `c² = 2^c`。 -/
theorem pair_product_mer_iff (c : ℕ) (hc : 3 ≤ c) :
    (c - 1) * (c + 1) = 2 ^ c - 1 ↔ c = 4 := by
  constructor
  · intro h
    have hp : (c - 1) * (c + 1) = c ^ 2 - 1 := pair_product_eq_sq_sub_one c
    rw [hp] at h
    have hpos1 : 0 < c ^ 2 := pow_pos (by omega : 0 < c) 2
    have hpos2 : 0 < 2 ^ c := pow_pos (by norm_num : (0 : ℕ) < 2) c
    have hsq : c ^ 2 = 2 ^ c := sub_one_injective hpos1 hpos2 h
    exact (sq_selfref_iff_four c hc).mp hsq
  · intro h
    subst h
    norm_num

/-- `c = 4` 处两种表示同时成立：`3 × 5 = 15 = 2^4 − 1`。 -/
theorem mer_pair_at_four : (4 - 1) * (4 + 1) = 2 ^ 4 - 1 := by norm_num

/-- ★★ **反解性**：若某 `c ≥ 3` 同时给出 `B = 15` 与 `B = 2^c − 1`，则 `c = 4`。 -/
theorem catOrder_pinned_by_branch (c : ℕ) (hc : 3 ≤ c)
    (hB : (c - 1) * (c + 1) = 2 ^ c - 1) : c = 4 :=
  (pair_product_mer_iff c hc).mp hB

/-! ## 三、桥接：`DHStructuralAnalysis` 的裸定义与 `CategoryOrder` 的计数是同一个数 -/

/-- ★★ **`DHStructural.B = nActive * nTotal`**：两处定义给出同一个 15。

⇒ `DHStructuralAnalysis` 的 `B := 3 * 5` 与 `CategoryOrder` 的 `(c−1)(c+1)` 在
`c = 4` 处是同一个数；本定理把它们接上，从而「`N_total = 5` 是裸约定」这一读法失效
——它在 `CategoryOrder` 口径下由 `catOrder` 决定。 -/
theorem dhstructural_B_bridge : MUFPF.DHStructural.B = nActive * nTotal := by
  rw [MUFPF.DHStructural.B_eq_15]
  norm_num [nActive, nTotal, catOrder]

/-- ★★★ **`B = 15` 的三种写法在 `catOrder = 4` 处同时成立**：
`B = 15` ∧ `B = 3 × 5` ∧ `B = 2^4 − 1` ∧ `B = catOrder² − 1`。 -/
theorem branch_count_verdict :
    MUFPF.DHStructural.B = 15 ∧
    nActive * nTotal = 15 ∧
    nActive * nTotal = 2 ^ catOrder - 1 ∧
    nActive * nTotal = catOrder ^ 2 - 1 ∧
    catOrder = 4 := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · exact MUFPF.DHStructural.B_eq_15
  · exact branch_eq_fifteen
  · exact branch_eq_mer
  · exact branch_sq_form
  · norm_num [catOrder]

/-- ★★ **`N_total` 不是自由参数**：`nTotal = catOrder + 1`，而 `catOrder` 由
`spaceLayerDim` 与 `timeLayerDim` 之和决定（`catOrder = d + t`，第 34/37 批）。

⇒ 本批只证到「层对口径下 `N_total` 由 `catOrder` 决定」；`catOrder = 4` 本身
仍是 `t = 1` 的等价陈述（第 37 批 `catOrder_four_iff_time_one`），未在本批消去。 -/
theorem ntotal_not_free :
    nTotal = catOrder + 1 ∧ nActive = catOrder - 1 ∧
    nActive * nTotal = catOrder ^ 2 - 1 := by
  exact ⟨rfl, rfl, branch_sq_form⟩

end MUFPF.BranchCountOrigin
