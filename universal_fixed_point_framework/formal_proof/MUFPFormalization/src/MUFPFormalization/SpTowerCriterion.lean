-- ============================================================
-- 塔高 4 的判据一致性（对应任务第 2 项）
-- ============================================================
-- 背景：库内没有 `SpFiveMorphism`，层 4 是现存的最高层。
-- 本段要回答的问题是：层 4 引入的 condition 是否需要**新的代数判据**。
--
-- 结论（本模块机检）：不需要。层 3（`SpThreeMorphism.condition`，
-- HigherSpCategory.lean L245）与层 4（`SpFourMorphism.condition`，L370）
-- 的右端是**同一个**谓词 `R = A * L - L * B`，`L` 甚至允许是矩形
-- （`Matrix (Fin X.n) (Fin Y.n)`），因此层 3 与层 4 共用同一判据。
--
-- 由此得到两条结构性事实：
--   1. condition 本身**恒可满足**（`R = 0` 时取 `L = 0`），
--      ⇒ 挡住越层的不是 condition，而是 `R ≠ 0`（D25 的「非平凡」判据）。
--   2. 判据在层间**可传递**：层 4 只要 `R₄` 等于某个层 3 已可解的 `R₃`，
--      就直接可解——这是「塔高 4 沿用层 3 判据」的形式表述。
--
-- 边界（未机检，仅登记）：层 ≥ 5 需要 `SpFiveMorphism` 结构（库内不存在），
-- 因此「塔高 ∞」不进入定理，只能按上述同形机制做外推。
-- ============================================================

import MUFPFormalization.HigherSpCategory
import MUFPFormalization.SpLayerSeparability

namespace MUFPF

open Matrix

/-- 层 3 / 层 4 condition 的统一形状：`R = A * L - L * B`。

    与 `SpLayerSeparability.adLin2` 的区别：此处 `A` 与 `B` 的阶可以不同，
    `L` 是**矩形**（`Matrix (Fin m) (Fin n) ℂ`），与 `HigherSpCategory` 的字段类型一致；
    `adLin2` 只在同阶方阵上有定义，是它的方形特例。 -/
def HasConditionForm {m n : ℕ} (A : Matrix (Fin m) (Fin m) ℂ)
    (B : Matrix (Fin n) (Fin n) ℂ) (R : Matrix (Fin m) (Fin n) ℂ) : Prop :=
  ∃ L : Matrix (Fin m) (Fin n) ℂ, R = A * L - L * B

/-- **层 3 的 condition 就是 `HasConditionForm`**：`secondHomotopy` 正是见证 `L`。
    直接取自 `HigherSpCategory.lean` L245 的字段定义，因此这不是重述而是字段实例化。 -/
theorem spThreeMorphism_condition_form {X Y : SpObj} {P Q : X ⟶ Y}
    {α β : SpTwoMorphism P Q} (Ξ : SpThreeMorphism α β) :
    HasConditionForm X.A Y.A (β.homotopy - α.homotopy) :=
  ⟨Ξ.secondHomotopy, Ξ.condition⟩

/-- **层 4 的 condition 是同一个 `HasConditionForm`**：`thirdHomotopy` 正是见证 `L`。
    层 3 与层 4 只在「取哪个矩阵差作 `R`」「用哪个 homotopy 作 `L`」上不同，
    判据本身完全一致 ⇒ 塔高从 3 升到 4 不引入新的代数条件。 -/
theorem spFourMorphism_condition_form {X Y : SpObj} {P Q : X ⟶ Y}
    {α β : SpTwoMorphism P Q} {Ξ Τ : SpThreeMorphism α β} (Φ : SpFourMorphism Ξ Τ) :
    HasConditionForm X.A Y.A (Τ.secondHomotopy - Ξ.secondHomotopy) :=
  ⟨Φ.thirdHomotopy, Φ.condition⟩

/-- **condition 恒可满足**：`R = 0` 时取 `L = 0` 即可。

    因此 condition 从不阻止越层；真正阻止的是 `R ≠ 0`。
    这与 D25 的判据「层 k 非平凡 ⟺ `∃ R_k ≠ 0` 且 `R_k ∈ im(d_A)`」在层 3/4 上对齐。 -/
theorem conditionForm_zero {m n : ℕ} (A : Matrix (Fin m) (Fin m) ℂ)
    (B : Matrix (Fin n) (Fin n) ℂ) : HasConditionForm A B 0 :=
  ⟨0, by simp⟩

/-- **判据在层间可传递**（塔高 4 沿用层 3 判据的形式表述）：
    若 `R₄` 等于某个已可用 `L₃` 求解的 `R₃`，则 `R₄` 同样可解，且见证就是 `L₃`。 -/
theorem conditionForm_reuse {m n : ℕ} {A : Matrix (Fin m) (Fin m) ℂ}
    {B : Matrix (Fin n) (Fin n) ℂ} {R₃ R₄ : Matrix (Fin m) (Fin n) ℂ}
    (L₃ : Matrix (Fin m) (Fin n) ℂ) (h₃ : R₃ = A * L₃ - L₃ * B) (h₄ : R₄ = R₃) :
    HasConditionForm A B R₄ :=
  ⟨L₃, h₄.trans h₃⟩

end MUFPF
