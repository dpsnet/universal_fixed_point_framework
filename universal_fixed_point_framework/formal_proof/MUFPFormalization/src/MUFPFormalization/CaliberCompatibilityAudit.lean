/-
  CaliberCompatibilityAudit.lean — R-k：`B` 的口径能否被「与 `σ⁻¹` 同形」这条约束裁决
  =====================================================================================

## 问题

§26 判定：15 / 12 / 9 / 6 是**四个不同的组合对象**（非空子集 / 有序不同对 / 活跃有序对 /
无序对），故「统一口径」不存在，缺的是「分支数该数什么」的物理定义。

但 §26 没有排除另一种可能：四个候选之中，**只有一个与框架已定的常数形式相容**。
框架的 `σ⁻¹ = 15` 在 `SigmaFormOrigin` 里被写成 `f² − 1`（不动点 ± 1 之积，`f = 4`）。
若要求 `B` 与 `σ⁻¹` **共用同一函数形式**（`c² − 1`），则四个候选里只剩 15 相容。

## 判决

机检结果：

| 候选 | 在 `c = 4` 处的多项式形式 | 与 `c² − 1` 同形？ |
|---|---|---|
| 15 | `c² − 1` | **是**（`= σ⁻¹` 的形式） |
| 12 | `c² − c` | 否 |
| 9 | `(c−1)²` | 否 |
| 6 | `2·(c−1)` | 否 |

所以口径可以**条件式闭合**：

> 接受「`B` 与 `σ⁻¹` 同形（都是不动点 ± 1 之积）」这条形式约束 ⟹ `B = 15` 唯一。
> 不接受 ⟹ 仍是四选一（§26 的状态）。

这与 §53 对 `σ⁻¹` 自身形式的裁决**同型**：那条裁决说「`σ⁻¹ = f² − 1` 要么由
『必须是不动点 ± 1 之积』这条对称性决定，要么仍是建模选择」。本批把这个「要么」
从常数搬到了 `B` 上，并证明搬过去之后是一个**可判的相容性筛**：
形式约束一下，四选一立刻降到唯一。

## 诚实边界

1. 本批只证「同形 ⟹ 唯一」这一条件句，**不证**这条形式约束本身该不该接受。
   该不该接受是理论裁决项（与 §53 同一裁决）。
2. 只用 `c = 4` 的数值相容性，不做一般 `c` 的函数形式比较（后者属 `SigmaFormOrigin`、
   `BranchCountOrigin` 两处既有定理，本批只引用）。
3. 12 / 9 / 6 的三个多项式形式是本批给出的**读法**（与 §26 的组合对象对应），
   不声称它们是框架的原生表达。
4. 不新增常数、不新增公设。
-/

import MUFPFormalization.BranchCaliberAudit
import MUFPFormalization.SigmaFormOrigin
import Mathlib.Tactic

namespace MUFPF.CaliberCompatibilityAudit

open MUFPF.CategoryOrder (catOrder nActive)

/-- `σ⁻¹` 在 `f = 4` 处的值：`sigmaInvSq 4 = 4² − 1 = 15`（复用 `SigmaFormOrigin` 的定义）。 -/
theorem sigmaInvSq_at_four : MUFPF.SigmaFormOrigin.sigmaInvSq 4 = 15 := by
  norm_num [MUFPF.SigmaFormOrigin.sigmaInvSq]

/-- ★★ **三个非 15 候选各有自己的关于 `c` 的多项式形式**（`c = 4` 处）：
    12 = `c² − c`，9 = `(c−1)²`，6 = `2·(c−1)`；而 15 = `c² − 1`。
    四者形式互不相同 ⟹ 排除它们不是排除「近似」，而是排除「不同对象」。 -/
theorem other_calibers_have_own_forms :
    nActive * catOrder = catOrder ^ 2 - catOrder ∧
      nActive ^ 2 = (catOrder - 1) ^ 2 ∧
      2 * nActive = 2 * (catOrder - 1) ∧
      nActive * MUFPF.CategoryOrder.nTotal = catOrder ^ 2 - 1 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · norm_num [nActive, catOrder]
  · norm_num [nActive, catOrder]
  · norm_num [nActive, catOrder]
  · exact MUFPF.BranchCountOrigin.branch_sq_form

/-- ★★ **只有 15 与 `σ⁻¹` 同形**（`c = 4`）：
    `15 = c² − 1`，而 `12 ≠ c² − 1`、`9 ≠ c² − 1`、`6 ≠ c² − 1`。 -/
theorem only_fifteen_matches_sigma_form :
    nActive * MUFPF.CategoryOrder.nTotal = catOrder ^ 2 - 1 ∧
      nActive * catOrder ≠ catOrder ^ 2 - 1 ∧
      nActive ^ 2 ≠ catOrder ^ 2 - 1 ∧
      2 * nActive ≠ catOrder ^ 2 - 1 := by
  refine ⟨MUFPF.BranchCountOrigin.branch_sq_form, ?_, ?_, ?_⟩
  · norm_num [nActive, catOrder]
  · norm_num [nActive, catOrder]
  · norm_num [nActive, catOrder]

/-- ★★★ **口径的条件式闭合**：若 `B` 取与 `σ⁻¹` 相同的函数形式（`f² − 1`），
    则 `B = sigmaInvSq catOrder` 且四个候选中只有 `15` 满足。

    ⇒ 「同形」这条形式约束把四选一降为唯一；`B` 的内生判据在此意义上**可以**给出，
    代价是接受一条形式公设（与 §53 对 `σ⁻¹` 形式的裁决同一项）。 -/
theorem caliber_pinned_by_form :
    nActive * MUFPF.CategoryOrder.nTotal = MUFPF.SigmaFormOrigin.sigmaInvSq catOrder ∧
      nActive * catOrder ≠ MUFPF.SigmaFormOrigin.sigmaInvSq catOrder ∧
      nActive ^ 2 ≠ MUFPF.SigmaFormOrigin.sigmaInvSq catOrder ∧
      2 * nActive ≠ MUFPF.SigmaFormOrigin.sigmaInvSq catOrder ∧
      MUFPF.SigmaFormOrigin.sigmaInvSq 4 = 15 := by
  refine ⟨?_, ?_, ?_, ?_, sigmaInvSq_at_four⟩
  · rw [MUFPF.SigmaFormOrigin.sigmaInvSq]
    norm_num [nActive, catOrder, MUFPF.CategoryOrder.nTotal]
  · rw [MUFPF.SigmaFormOrigin.sigmaInvSq]
    norm_num [nActive, catOrder]
  · rw [MUFPF.SigmaFormOrigin.sigmaInvSq]
    norm_num [nActive, catOrder]
  · rw [MUFPF.SigmaFormOrigin.sigmaInvSq]
    norm_num [nActive, catOrder]

/-- **R-k 判决汇总**：① 三个非 15 候选各有独立多项式形式；② 只有 15 与 `c² − 1` 同形；
    ③ `σ⁻¹(4) = 15`；④ 故「同形」约束下口径唯一。 -/
theorem caliber_compatibility_verdict :
    (nActive * catOrder = catOrder ^ 2 - catOrder ∧
        nActive ^ 2 = (catOrder - 1) ^ 2 ∧
        2 * nActive = 2 * (catOrder - 1)) ∧
      (nActive * MUFPF.CategoryOrder.nTotal = catOrder ^ 2 - 1 ∧
        nActive * catOrder ≠ catOrder ^ 2 - 1 ∧
        nActive ^ 2 ≠ catOrder ^ 2 - 1 ∧
        2 * nActive ≠ catOrder ^ 2 - 1) ∧
      (MUFPF.SigmaFormOrigin.sigmaInvSq 4 = 15 ∧
        nActive * MUFPF.CategoryOrder.nTotal = MUFPF.SigmaFormOrigin.sigmaInvSq catOrder) := 
  ⟨⟨(other_calibers_have_own_forms).1, (other_calibers_have_own_forms).2.1,
      (other_calibers_have_own_forms).2.2.1⟩,
    ⟨(only_fifteen_matches_sigma_form).1, (only_fifteen_matches_sigma_form).2.1,
      (only_fifteen_matches_sigma_form).2.2.1, (only_fifteen_matches_sigma_form).2.2.2⟩,
    ⟨sigmaInvSq_at_four, (caliber_pinned_by_form).1⟩⟩

end MUFPF.CaliberCompatibilityAudit
