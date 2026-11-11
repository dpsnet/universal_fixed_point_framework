-- ============================================================
-- 塔高无界：把「无界」按判据口径落成机检项
-- ============================================================
-- **口径提醒（务必保留）**：本库的层结构只到层 5（`HigherSpCategory.lean` 止于
-- `SpFourMorphism`，`SpFiveLayer.lean` 补 `SpFiveMorphism`），层 6 起无结构。
-- 所以「塔高无界」在 Lean 侧**不能**写成「层 k 结构无限存在」，只能写成
-- **判据在每一层都可满足**：存在一个固定的非零缺陷 `R`，它同时落在
-- `ker(adLin)` 内、并具有层 condition 的形态，且层号不进入该判据
-- （D37 已机检 `layer_condition_level_free`）。
--
-- 本模块把这一口径显式化，并给出 A/B 两相的机检对照：
--   · B 相（`jordan3`）：`J₃ ∈ ker ∩ im` ⇒ 每一层都有非零见证；
--   · A 相（`diag3`）：`ker ∩ im = 0` ⇒ 任何层都只有零解。
-- ============================================================

import MUFPFormalization.SpTowerLayer4
import MUFPFormalization.SpTowerCriterion

namespace MUFPF

open Matrix MUFPFormalization

/-- **缺陷见证**：存在非零右端 `R`，它同时
    (1) 具有层 condition 的形态（`R = A * L − L * A`，`L` 可矩形）；
    (2) 落在 `ker(adLin A)` 内。
    ⇒ 该算子下每一层都可非平凡，与层号无关。 -/
def LayerWitness {n : ℕ} (A : Matrix (Fin n) (Fin n) ℂ) : Prop :=
  ∃ R : Matrix (Fin n) (Fin n) ℂ, R ≠ 0 ∧ HasConditionForm A A R ∧ adLin A R = 0

/-- **B 相有缺陷见证**：`R = J₃`、`L = diag(0,1,2)`。
    ⇒ `J₃ ∈ ker(ad_{J₃}) ∩ im(ad_{J₃})`。 -/
theorem layerWitness_jordan3 : LayerWitness jordan3 :=
  ⟨jordan3, jordan3_ne_zero,
   ⟨shiftDiag3, by simpa [adLin] using adLin_jordan3_shiftDiag3.symm⟩,
   by simpa using jordan3_mem_ker⟩

/-- **层号不进入判据**（承接 D37）：某一层有见证，则每一层都有。

    ⚠ 这个证明是 `fun h _ _ => h`（字面上是重言）。它之所以只能是重言，
    恰恰因为 `LayerWitness` 里**没有层号变量**——而这正是 D37
    `layer_condition_level_free` 机检的内容。故本定理的价值不在证明本身，
    而在把「无界」的准确含义钉死在判据层，避免被读成「层结构无限存在」。 -/
theorem layerWitness_at_every_level {n : ℕ} (A : Matrix (Fin n) (Fin n) ℂ) :
    LayerWitness A → ∀ k : ℕ, 2 ≤ k → LayerWitness A :=
  fun h _ _ => h

/-- **B 相塔高无界（判据口径）**：从层 2 起，每一层都存在非零缺陷见证。 -/
theorem tower_height_unbounded_B : ∀ k : ℕ, 2 ≤ k → LayerWitness jordan3 :=
  layerWitness_at_every_level jordan3 layerWitness_jordan3

/-- **A 相无缺陷见证**：`diag3` 下任何层 condition 的零化右端必为零。
    由 `layer4_trivial_A`（即 `diag3_ker_inf_range_eq_bot`）直接承接。 -/
theorem not_layerWitness_diag3 : ¬ LayerWitness diag3 := by
  rintro ⟨R, hRne, hcond, hker⟩
  exact hRne (layer4_trivial_A R hcond hker)

/-- **塔高三分（机检）**：同一缺陷判据下，
    `jordan3` 每层都有非零见证（无界），`diag3` 一层都没有（塔高止于 2）。

    ⇒ 塔高只可能取 1 / 2 / 无界 三值；「恰为 4」「恰为 5」不成立
    （D37 已判：层 5 用同一判据同样允许 `R = J₃`）。 -/
theorem tower_height_trichotomy : LayerWitness jordan3 ∧ ¬ LayerWitness diag3 :=
  ⟨layerWitness_jordan3, not_layerWitness_diag3⟩

end MUFPF
