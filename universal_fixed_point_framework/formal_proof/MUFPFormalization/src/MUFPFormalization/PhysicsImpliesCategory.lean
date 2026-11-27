/-
  PhysicsImpliesCategory.lean — R-a：「若物理则范畴必有 X」的显式引理
  ==============================================================

## 为什么写这一批

前三批（R-c′ / R-c″ / R-c‴）走的都是「读数 → 参数」：给一条物理读数，问它能不能
反定范畴参数。结论是能，但只在参数层；判据（结构）必须由框架给出。

R-a 换方向：不再问「读数反定什么」，而问「**物理命题本身强制范畴侧必须有哪一条
结构**」。写成显式蕴含，每条都把物理侧前提摆在假设里，让读者一眼看见「哪一半是
物理、哪一半是范畴」。

## 本模块三条

| 编号 | 蕴含 | 物理侧前提（假设） | 范畴侧结论 |
|:--|:--|:--|:--|
| A1 | `2^E = 2^nActive → E = nActive` | 偏差界是**以 2 为基的指数形式** | 指数 = 主动层数 |
| A2 | `B = 2^n − 1 → n = 4` | 分支数等于「2 的幂减一」 | 幂指数 = `catOrder` |
| A3 | `f (routeLayerPair (1,15)) = f (routeLayerPair (3,5))` | 读数只经乘积这一条通道 | **无**判别信息（负向） |

## 结论的口径（勿加强）

- A1、A2 是**正向穿透**：它们说明「物理命题只要带了指数/幂结构，范畴常数就被钉住」。
  但这不解除 R-b 的二分——物理侧大部分定理仍然不含这些常数，穿透的是少数几条。
- A1 的前提「基为 2」是**物理侧假设**，本模块不证它。它成立的理由在
  `BranchCounting`（静默/活跃二值分解）与光子拓扑的 16 维表示，都是既有材料。
- A3 是负向的：任何**只**取读数值的函数在四原像上取值相同，故读数单独永远选不出
  `(3,5)`。这与 `SemanticFilterAudit` 的正面结论互为两面：选出 `(3,5)` 的东西必须是
  层表判据，不能是读数的任何函数。
- C3（`PhotonTopology`）**没有可形式化的正向蕴含**：该模块 8 个 import 全为 Mathlib，
  闭包内零范畴层常数（R-b 已机检）。此处如实登记为空缺，不用 `True` 充数。
- 全部结论为 `norm_num` / `omega` / `rw` 级别，无新公设、无 `sorry`、无 `axiom`。
-/

import Mathlib.Tactic
import MUFPFormalization.BranchCounting
import MUFPFormalization.ActiveFromCategoryOrder
import MUFPFormalization.ReverseReadoutAudit

open MUFPF.BranchCounting
open MUFPF.CategoryOrder
open MUFPF.ReverseReadoutAudit

namespace MUFPF.PhysicsImpliesCategory

/-! =========================================================
    §1 A1：偏差界的指数形式强制「指数 = 主动层数」
   =========================================================

    物理侧形式：`2^E`，E 是偏差界的指数。范畴侧：`nActive = catOrder − 1 = 3`。
    本节的蕴含是：一旦物理把偏差界写成以 2 为基的指数形式，E 就被钉死，
    没有第二种取值。
-/

/-- **A1（符号形式）**：基为 2 的指数相等 ⟹ 指数相等。

    前提「基为 2」是物理侧假设；结论是范畴侧计数被钉住。 -/
theorem deviationBound_exponent_pinned (E : ℕ) (h : 2 ^ E = 2 ^ nActive) :
    E = nActive :=
  Nat.pow_right_injective (by norm_num) h

/-- **A1（数值形式）**：读到偏差界 `2^E = 8` 就只能有 `E = 3 = nActive`。

    这是 R-a 的正面结论：物理读数（8）→ 指数（3）→ 范畴常数（`nActive`）。
    与 §14① 的连续读数通道不同，这里走的是**幂指数**通道，且不需要连续性，
    只需要「知道基是 2」。 -/
theorem deviationBound_three (E : ℕ) (h : 2 ^ E = 8) : E = 3 := by
  have h' : (2 : ℕ) ^ E = (2 : ℕ) ^ 3 := by
    rw [h]
    norm_num
  have hE : E = 3 := Nat.pow_right_injective (by norm_num) h'
  exact hE

/-! =========================================================
    §2 A2：分支数的「2 的幂减一」形式强制幂指数 = catOrder
   =========================================================

    `B = 15` 是库内定理（`B_eq_15`），不是假设。本节再给它一条幂形式：
    若同时知道 `B = 2^n − 1`，则 n 只能是 4。注意方向与 §13 相反：
    这里是从「幂形式 + 分支数」反推指数，即物理侧读数反定范畴阶。
-/

/-- **A2**：`B = 2^n − 1` ⟹ `n = catOrder = 4`。

    证明链：`2^n − 1 = B = 15` ⟹ `2^n = 16 = 2^4` ⟹ 指数单射 ⟹ `n = 4`。 -/
theorem branchCount_forces_order (n : ℕ) (h : B = 2 ^ n - 1) : n = catOrder := by
  have h15 : (2 : ℕ) ^ n - 1 = 15 := by
    rw [← h]
    exact B_eq_15
  have h16 : (2 : ℕ) ^ n = 16 := by omega
  have h' : (2 : ℕ) ^ n = (2 : ℕ) ^ 4 := by
    rw [h16]
    norm_num
  exact Nat.pow_right_injective (by norm_num) h' ▸ (by rfl : (4 : ℕ) = catOrder)

/-! =========================================================
    §3 A3（负向）：读数单独不含判别信息
   =========================================================

    `SemanticFilterAudit` 已证「读数 + 层表判据 ⟹ 唯一」。本节补它的另一面：
    读数本身对**任何**函数都没有区分力。四原像在两两之间取值完全相同，
    所以想选出 `(3,5)`，函数不能只看读数。
-/

/-- **A3**：任取读数函数 `f`，`1×15` 与 `3×5` 给出同一读数。

    `f` 可以是任意 `ℕ → ℕ` 的函数——这正说明「读数的任何加工」都不带判别力。 -/
theorem readout_value_blind (f : ℕ → ℕ) :
    f (routeLayerPair (1, 15)) = f (routeLayerPair (3, 5)) := by
  rw [show routeLayerPair (1, 15) = routeLayerPair (3, 5) from by
    norm_num [routeLayerPair]]

/-- **A3（全纤维版）**：四原像在任意读数函数下取值相同。 -/
theorem four_preimages_same_readout (f : ℕ → ℕ) :
    f (routeLayerPair (1, 15)) = f (routeLayerPair (3, 5)) ∧
    f (routeLayerPair (5, 3)) = f (routeLayerPair (3, 5)) ∧
    f (routeLayerPair (15, 1)) = f (routeLayerPair (3, 5)) := by
  refine ⟨readout_value_blind f, ?_, ?_⟩
  · rw [show routeLayerPair (5, 3) = routeLayerPair (3, 5) from by
      norm_num [routeLayerPair]]
  · rw [show routeLayerPair (15, 1) = routeLayerPair (3, 5) from by
      norm_num [routeLayerPair]]

/-- **A3 的判别式形式**：不存在「只凭读数」就能把 `(3,5)` 与 `(1,15)` 分开的函数。

    若 `g` 能分开，则必有 `g 15 ≠ g 15`——矛盾。 -/
theorem no_readout_separates (g : ℕ → ℕ) :
    ¬ (g (routeLayerPair (3, 5)) ≠ g (routeLayerPair (1, 15))) := by
  intro h
  exact h (readout_value_blind g).symm

/-! =========================================================
    §4 判决汇总
   =========================================================
-/

/-- **R-a 的三条合并**：两条正向穿透（A1、A2）+ 一条负向边界（A3）。

    - A1：物理给基为 2 的指数形式 ⟹ 指数被钉为范畴主动层数；
    - A2：物理给「2 的幂减一」的分支形式 ⟹ 幂指数被钉为范畴阶；
    - A3：任何只经读数的函数都没有判别力 ⟹ 选 `(3,5)` 必须用层表判据。

    三者合起来即 R-a 的判决：**物理侧能反向钉住范畴侧的数，但钉不住范畴侧的判据。
    判据只能由框架给出。** -/
theorem physics_implies_category_summary :
    (∀ E : ℕ, 2 ^ E = 2 ^ nActive → E = nActive) ∧
    (∀ n : ℕ, B = 2 ^ n - 1 → n = catOrder) ∧
    (∀ g : ℕ → ℕ, ¬ (g (routeLayerPair (3, 5)) ≠ g (routeLayerPair (1, 15)))) :=
  ⟨deviationBound_exponent_pinned,
   fun n h => branchCount_forces_order n h,
   no_readout_separates⟩

end MUFPF.PhysicsImpliesCategory
