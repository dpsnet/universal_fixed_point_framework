/-
  BranchCaliberAudit.lean — R-j：`B` 的四口径之争的可判定化
  =====================================================================================

## 问题

§63 把 `B = 15` 的四种口径登记为「15 / 12 / 9 / 6，其中 6 个为交叉项」，并判
「口径四选一，选择无结构依据」。§25 又把「更强载体」的复活条件压在「`B` 的内生判据」上，
而 `B` 的身份候选正是这一处。于是本轮要回答的是一个可判定问题：

> 15、12、9、6 是**同一个对象的四种写法**（口径之争），
> 还是**四个不同对象**（那就不存在「选哪个写法」的问题）？

## 判决

四个值各有自己的组合对象，且**互不相等**：

| 值 | 组合对象 | 机检形式 |
|---|---|---|
| 15 | `Fin 4` 的**非空子集**数 `2^4 − 1` | `card (univ.powerset.erase ∅) = 15`；且 `= c² − 1` |
| 12 | `Fin 4` 的**有序不同对**数 `c² − c` | `card (offDiag univ) = 12` |
| 9 | `Fin 3`（活跃层）的**有序对**（含自对）`(c−1)²` | `card (univ ×ˢ univ) = 9` |
| 6 | `Fin 4` 的**无序对**数 `C(4,2)` | `Nat.choose 4 2 = 6`，同时 `= 2·nActive` |

所以 §63 的「四口径」不是同一个数目的四种写法，而是**四件不同的事**：

- 15 数的是「层的非空组合」，12 数的是「层的有序推进」，9 数的是「活跃层之间的有序对」，
  6 数的是「层的无序对」。
- 判 15 的读法已被恒等式封口：`(c−1)(c+1) = 2^c − 1 ⟺ c = 4`
  （`BranchCountOrigin.pair_product_mer_iff`），即「层对乘积」与「非空子集」在 `c = 4`
  处**是同一个数而不是两条路线**。12 / 9 / 6 没有这条封口——它们各自只有一条读法。
- 但 6 恰好有两条独立读法：`C(4,2) = 6` 与 `2·nActive = 6`。同一个 6，
  两条组合链，互不蕴含。

## 净结果

「选哪个当 `B`」不是口径规范问题（把同一对象的四种写法统一起来），
而是**「分支数该数什么」的物理指认问题**——四个候选各有一个无歧义的组合意义，
框架内没有判据选出其中一个。这正是 §63 原判断的机制化版本，也解释了
为什么 §25 的耦合块拿不到内生判据：

- §63 的 `B` 是**计数**（15/12/9/6 都是 `nActive × 层标号` 或组合计数）；
- §25 的 `B` 是**2×2 矩阵块**，自由度 `Fintype.card (Fin 2 × Fin 2) = 4`。
- 两处的 `B` 同名不同物，且 `4 ∉ {15,12,9,6}`：**禁止互推**。
  （若沿用同名，会把「耦合自由度 4」误当成「分支数 15」，或反之。）

## 诚实边界

1. 只机检组合计数与算术恒等式；不判「物理上的分支数到底是哪一个组合对象」。
2. 「交叉项 6 个」的解剖沿用 §63 的既有结论，本批不重做交叉项分解
   （本批只机检 `6 = C(4,2) = 2·nActive` 这一数值双读法）。
3. `4 = catOrder` 这一数值巧合**不在本模块登记为定理**（它只是四个四的偶合，
   需独立判据，属未判候选，见笔记 §26.6）。
4. 不新增常数、不新增公设；`catOrder`、`nActive`、`nTotal` 全部引用库内既有定义。
-/

import MUFPFormalization.BranchCountOrigin
import Mathlib.Tactic

namespace MUFPF.BranchCaliberAudit

open MUFPF.CategoryOrder (catOrder nTotal nActive)

/-! ## 一、四个计数对象，逐个用 `Finset.card` / `Nat.choose` 机检 -/

/-- ★ **15 = `Fin 4` 的非空子集数**：`card (univ.powerset.erase ∅) = 2^4 − 1 = 15`。
    这是「层的非空组合」这一组合对象。 -/
theorem fifteen_is_nonempty_subsets :
    ((Finset.univ : Finset (Fin 4)).powerset.erase ∅).card = 15 := by
  have hmem : (∅ : Finset (Fin 4)) ∈ (Finset.univ : Finset (Fin 4)).powerset := by
    simp
  rw [Finset.card_erase_of_mem hmem, Finset.card_powerset, Finset.card_univ, Fintype.card_fin]
  norm_num

/-- ★ **12 = `Fin 4` 的有序不同对数**（`offDiag`）：`card (offDiag univ) = 4 · 4 − 4 = 12`。
    这是「层的有序推进」这一组合对象。 -/
theorem twelve_is_ordered_distinct_pairs :
    (Finset.offDiag (Finset.univ : Finset (Fin 4))).card = 12 := by
  rw [Finset.offDiag_card, Finset.card_univ, Fintype.card_fin]

/-- ★ **9 = `Fin 3`（活跃层）的有序对数**（含自对）：`card (univ ×ˢ univ) = 3 · 3 = 9`。
    这是「活跃层之间的有序对」这一组合对象。 -/
theorem nine_is_active_ordered_pairs :
    ((Finset.univ : Finset (Fin 3)).product (Finset.univ : Finset (Fin 3))).card = 9 := by
  simp

/-- ★ **6 = `Fin 4` 的无序对数**：`Nat.choose 4 2 = 6`。这是「层的无序对」这一组合对象。 -/
theorem six_is_unordered_pairs : (Nat.choose 4 2 : ℕ) = 6 := by
  rw [Nat.choose_two_right]

/-! ## 二、四个值与框架整数对齐：它们都是 `catOrder` 的多项式形态 -/

/-- `15 = c² − 1 = 2^c − 1`（`c = 4`）；与 `BranchCountOrigin.branch_eq_mer` 同口径。 -/
theorem fifteen_forms :
    nActive * nTotal = 15 ∧ nActive * nTotal = 2 ^ catOrder - 1 ∧
      nActive * nTotal = catOrder ^ 2 - 1 :=
  ⟨MUFPF.BranchCountOrigin.branch_eq_fifteen,
    MUFPF.BranchCountOrigin.branch_eq_mer,
    MUFPF.BranchCountOrigin.branch_sq_form⟩

/-- `12 = c² − c = c · (c−1) = nActive · catOrder`：有序不同对。 -/ 
theorem twelve_forms : nActive * catOrder = 12 ∧ catOrder ^ 2 - catOrder = 12 := by
  refine ⟨?_, ?_⟩
  · norm_num [nActive, catOrder]
  · norm_num [catOrder]

/-- `9 = nActive² = (c−1)²`：活跃层有序对。 -/
theorem nine_forms : nActive ^ 2 = 9 := by
  norm_num [nActive, catOrder]

/-! ## 三、四个值互不相等 —— 故不可能同指一个对象 -/

/-- ★★ **四值两两不等**。若它们是同一对象的四种写法，则必有两值相等；
    机检否决该前提。 -/
theorem four_counts_pairwise_distinct :
    (15 : ℕ) ≠ 12 ∧ (15 : ℕ) ≠ 9 ∧ (15 : ℕ) ≠ 6 ∧
      (12 : ℕ) ≠ 9 ∧ (12 : ℕ) ≠ 6 ∧ (9 : ℕ) ≠ 6 := by
  norm_num

/-! ## 四、6 的双读法：同一个数，两条互不蕴含的组合链 -/

/-- ★★ **`6` 的两条链**：`C(4,2) = 6`（无序对）与 `2·nActive = 6`（活跃层的二倍）。
    两条链都只用到框架整数，却指向不同组合对象 ⟹ `6` 自身的生成链不唯一。 -/
theorem six_has_two_chains :
    (Nat.choose 4 2 : ℕ) = 6 ∧ 2 * nActive = 6 := by
  refine ⟨six_is_unordered_pairs, ?_⟩
  norm_num [nActive, catOrder]

/-! ## 五、`B_计数` 与 `B_耦合` 是两个对象：`4 ∉ {15, 12, 9, 6}` -/

/-- 耦合块的自由度：`2×2` 矩阵的条目数 `Fintype.card (Fin 2 × Fin 2) = 4`
    （§25 `blk` 的 `B` 块）。 -/
theorem coupling_block_dim : Fintype.card (Fin 2 × Fin 2) = 4 := by
  simp

/-- ★★★ **同名不同物**：耦合块维数 `4` 不等于四个计数值中的任何一个
    ⟹ §63 的 `B`（计数）与 §25 的 `B`（矩阵块）**禁止互推**。 -/
theorem coupling_dim_not_a_count :
    Fintype.card (Fin 2 × Fin 2) ≠ 15 ∧ Fintype.card (Fin 2 × Fin 2) ≠ 12 ∧
      Fintype.card (Fin 2 × Fin 2) ≠ 9 ∧ Fintype.card (Fin 2 × Fin 2) ≠ 6 := by
  norm_num [coupling_block_dim]

/-! ## 六、汇总判决 -/

/-- **R-j 判决汇总**：
    ① 四个值各自有独立的组合对象（非空子集 15 / 有序不同对 12 / 活跃有序对 9 / 无序对 6）；
    ② 四值两两不等 ⟹ 不是同一对象的四种写法；
    ③ `15` 的读法已被 `c² − 1 = 2^c − 1 ⟺ c = 4` 封口（唯一），`6` 反而有两条链；
    ④ 耦合块维数 `4` 与四个计数无一相符 ⟹ `B_计数 ≠ B_耦合`。 -/
theorem branch_caliber_verdict :
    (((Finset.univ : Finset (Fin 4)).powerset.erase ∅).card = 15 ∧
        (Finset.offDiag (Finset.univ : Finset (Fin 4))).card = 12 ∧
        ((Finset.univ : Finset (Fin 3)).product (Finset.univ : Finset (Fin 3))).card = 9 ∧
        (Nat.choose 4 2 : ℕ) = 6) ∧
      ((15 : ℕ) ≠ 12 ∧ (15 : ℕ) ≠ 9 ∧ (15 : ℕ) ≠ 6 ∧
        (12 : ℕ) ≠ 9 ∧ (12 : ℕ) ≠ 6 ∧ (9 : ℕ) ≠ 6) ∧
      (nActive * nTotal = 2 ^ catOrder - 1 ∧ 2 * nActive = 6 ∧
        (Nat.choose 4 2 : ℕ) = 6) ∧
      (Fintype.card (Fin 2 × Fin 2) ≠ 15 ∧ Fintype.card (Fin 2 × Fin 2) ≠ 12 ∧
        Fintype.card (Fin 2 × Fin 2) ≠ 9 ∧ Fintype.card (Fin 2 × Fin 2) ≠ 6) :=
  ⟨⟨fifteen_is_nonempty_subsets, twelve_is_ordered_distinct_pairs,
      nine_is_active_ordered_pairs, six_is_unordered_pairs⟩,
    four_counts_pairwise_distinct,
    ⟨MUFPF.BranchCountOrigin.branch_eq_mer, (six_has_two_chains).2, (six_has_two_chains).1⟩,
    coupling_dim_not_a_count⟩

end MUFPF.BranchCaliberAudit
