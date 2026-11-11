-- ============================================================
-- 层 5 结构与「塔高 ∞」的机检形式（任务第 2 项收口）
-- ============================================================
-- 库内层结构止于 `SpFourMorphism`（`HigherSpCategory.lean` L362–370，`end` 在 L573），
-- 因此 B 相的「塔高恰为 4」与「塔高 ∞」此前没有任何陈述可证——不是判据问题，
-- 而是**结构缺口**：层 5 起没有结构，就没有 condition 可写。
--
-- 本模块做两件事：
--   1. 按层 3/4 的同形模式补出 `SpFiveMorphism`（结构 + 垂直复合 + 单位），
--      使「层 5 的 condition」在库内第一次有定义；
--   2. 机检「判据不含层号」：层 3、4、5 的 condition 全部化为同一个
--      `HasConditionForm`。⇒ 塔高由 `ker ∩ im` 决定，与层号无关。
--
-- 边界（必须一起引用）：
--   - 「层 6 起继续延伸」是**结构公设**，不是本库定理（库内只到层 5）。因此
--     「塔高 ∞」的机检形式是「判据层号无关 + 缺陷决定塔高」，**不是**「塔无限高」。
--   - B 相非零解 / A 相零解由 `SpTowerLayer4.lean` 的
--     `layer4_nontrivial_B` / `layer4_trivial_A` 供给，本模块只把它与层号无关性并置。
-- ============================================================

import MUFPFormalization.SpTowerCriterion
import MUFPFormalization.SpTowerLayer4

namespace MUFPF

open Matrix MUFPFormalization

/-- 层 5 结构：`Ψ : Χ ⇛ Ω`，其中 `Χ Ω : SpFourMorphism Ξ Τ` 是层 4 态射。

    与 `SpFourMorphism`（`HigherSpCategory.lean` L362–370）逐字同形：
    `thirdHomotopy → fourthHomotopy`，条件仍是 `R = X.A * L - L * Y.A`。 -/
@[ext]
structure SpFiveMorphism {X Y : SpObj} {P Q : X ⟶ Y} {α β : SpTwoMorphism P Q}
    {Ξ Τ : SpThreeMorphism α β} (Χ Ω : SpFourMorphism Ξ Τ) where
  /-- 第四层 homotopy：满足 `Ω.thirdHomotopy - Χ.thirdHomotopy = X.A*L - L*Y.A`。 -/
  fourthHomotopy : Matrix (Fin (X.n)) (Fin (Y.n)) ℂ
  /-- 第四层 condition（与层 3/4 同一形态）。 -/
  condition : Ω.thirdHomotopy - Χ.thirdHomotopy = X.A * fourthHomotopy - fourthHomotopy * Y.A

/-- 层 5 的垂直复合（`Χ ⇛ Ω ⇛ Υ`）。 -/
def spFiveVertComp {X Y : SpObj} {P Q : X ⟶ Y} {α β : SpTwoMorphism P Q}
    {Ξ Τ : SpThreeMorphism α β} {Χ Ω Υ : SpFourMorphism Ξ Τ}
    (Φ : SpFiveMorphism Χ Ω) (Ψ : SpFiveMorphism Ω Υ) : SpFiveMorphism Χ Υ :=
  { fourthHomotopy := Φ.fourthHomotopy + Ψ.fourthHomotopy
    condition := by
      have h1 : Υ.thirdHomotopy - Χ.thirdHomotopy =
          (Υ.thirdHomotopy - Ω.thirdHomotopy) + (Ω.thirdHomotopy - Χ.thirdHomotopy) := by abel
      rw [h1, Ψ.condition, Φ.condition, Matrix.mul_add, Matrix.add_mul]
      abel }

/-- 层 5 的单位态射 `id_Χ : Χ ⇛ Χ`。 -/
def spIdFiveMorphism {X Y : SpObj} {P Q : X ⟶ Y} {α β : SpTwoMorphism P Q}
    {Ξ Τ : SpThreeMorphism α β} (Χ : SpFourMorphism Ξ Τ) : SpFiveMorphism Χ Χ :=
  { fourthHomotopy := 0
    condition := by simp }

/-- 「判据不含层号」这一命题：层 3、层 4、层 5 的 condition
    全部是同一个 `HasConditionForm X.A Y.A R`。

    抽成 `def` 而非直接写成定理，是为了让 `tower_height_determined_by_defect`
    能在**类型位置**引用这条命题（Lean 不允许把定理名当命题用）。 -/
def LevelFreeCondition : Prop :=
  (∀ {X Y : SpObj} {P Q : X ⟶ Y} {α β : SpTwoMorphism P Q}
      (_ : SpThreeMorphism α β),
      HasConditionForm X.A Y.A (β.homotopy - α.homotopy)) ∧
  (∀ {X Y : SpObj} {P Q : X ⟶ Y} {α β : SpTwoMorphism P Q}
      {Ξ Τ : SpThreeMorphism α β} (_ : SpFourMorphism Ξ Τ),
      HasConditionForm X.A Y.A (Τ.secondHomotopy - Ξ.secondHomotopy)) ∧
  (∀ {X Y : SpObj} {P Q : X ⟶ Y} {α β : SpTwoMorphism P Q}
      {Ξ Τ : SpThreeMorphism α β} {Χ Ω : SpFourMorphism Ξ Τ}
      (_ : SpFiveMorphism Χ Ω),
      HasConditionForm X.A Y.A (Ω.thirdHomotopy - Χ.thirdHomotopy))

/-- **判据不含层号（塔高 ∞ 的可机检形式）**：层 3、4、5 的 condition 同形。

    这条定理的价值不在「又证了一遍同形」，而在**它把层号从判据里彻底消掉**：
    判据只依赖 `X.A`、`Y.A` 和右端 `R`。因此「某层能不能穿越」不取决于它在第几层，
    只取决于该相下 `ker ∩ im` 是否非零。⇒ 「塔高 4」与「塔高 ∞」的差别不在代数，
    而在库内层结构写到第几层。 -/
theorem layer_condition_level_free : LevelFreeCondition :=
  ⟨fun Ξ => ⟨Ξ.secondHomotopy, Ξ.condition⟩,
   fun Φ => ⟨Φ.thirdHomotopy, Φ.condition⟩,
   fun Ψ => ⟨Ψ.fourthHomotopy, Ψ.condition⟩⟩

/-- **塔高由缺陷决定（跨层合取）**：把「判据层号无关」与「B 相非零解 / A 相零解」
    并置为一条。⇒ 只要层结构按同一 `condition` 形态延伸，某一层的可穿越性
    与其它层完全一致：A 相永远止步，B 相永远能过。

    这就是「塔高 ∞」能入定理的全部内容——**不是**「塔有无穷多层」（那是结构公设），
    而是「延伸与否不由判据决定」。 -/
theorem tower_height_determined_by_defect :
    LevelFreeCondition ∧
    (∃ R : Matrix (Fin 3) (Fin 3) ℂ,
        R ≠ 0 ∧ HasConditionForm jordan3 jordan3 R ∧ adLin jordan3 R = 0) ∧
    (∀ R : Matrix (Fin 3) (Fin 3) ℂ,
        HasConditionForm diag3 diag3 R → adLin diag3 R = 0 → R = 0) :=
  ⟨layer_condition_level_free, ⟨layer4_nontrivial_B, layer4_trivial_A⟩⟩

end MUFPF
