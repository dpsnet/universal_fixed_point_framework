-- ============================================================
-- 塔高 4 的机检形式（任务第 2 项的数值侧）
-- ============================================================
-- `SpTowerCriterion.lean` 已证：层 3 与层 4 共用同一个判据 `HasConditionForm`
-- （= 层 condition 的形态，矩形 `L`），因此「塔高 3 → 4」不引入新代数条件。
--
-- 本题补的是数值侧：**层 4 在 B 相确有非零解、在 A 相只有零解**，
-- 即 `塔高(A) = 2` 而 `塔高(B) ≥ 4`。这与层 3 的
-- `jordan3_extends_past_layer2` / `diag3_stops_at_layer2` 完全同形，
-- 因层 3 的判据与层 4 同形，故层 4 的结论由同一组代数事实承接。
--
-- 关键代数事实：`ad_{J₃}(diag(0,1,2)) = J₃`（R4 构造的 Lean 版）。
-- ============================================================

import MUFPFormalization.HigherSpCategory
import MUFPFormalization.SpTowerCriterion
import MUFPFormalization.SpLayerSeparability

namespace MUFPF

open Matrix MUFPFormalization

/-- 位移对角阵 `h = diag(0, 1, 2)`（`ad_{J₃}(h) = J₃` 的见证）。 -/
def shiftDiag3 : Matrix (Fin 3) (Fin 3) ℂ :=
  Matrix.of ![![0, 0, 0], ![0, 1, 0], ![0, 0, 2]]

/-- **核心代数恒等式（R4 构造的 Lean 版）**：`ad_{J₃}(diag(0,1,2)) = J₃`。 -/
theorem adLin_jordan3_shiftDiag3 : adLin jordan3 shiftDiag3 = jordan3 := by
  ext i j
  fin_cases i
  all_goals fin_cases j
  all_goals simp [adLin, shiftDiag3, jordan3, Matrix.of_apply]
  all_goals norm_num

/-- **B 相层 4 非平凡（塔高 ≥ 4）**：右端 `R = J₃` 非零、属于层 4 的 condition 形态、
    且在 `ker(ad_{J₃})` 内。⇒ 层 4 承接非零 defect，塔高越过层 3。
    硬啃要点：`L = diag(0,1,2)` 由上述恒等式直接供给。 -/
theorem layer4_nontrivial_B :
    ∃ R : Matrix (Fin 3) (Fin 3) ℂ,
      R ≠ 0 ∧ HasConditionForm jordan3 jordan3 R ∧ adLin jordan3 R = 0 :=
  ⟨jordan3, jordan3_ne_zero,
    ⟨shiftDiag3, by simpa [adLin] using adLin_jordan3_shiftDiag3.symm⟩,
    by simpa using jordan3_mem_ker⟩

/-- **A 相层 4 平凡（塔高止于 2）**：对角相下任何满足层 4 condition 且在
    `ker(ad_{diag3})` 内的右端必为零。由 `diag3_ker_inf_range_eq_bot` 直接推出，
    与 `diag3_stops_at_layer2`（层 3 版）同形。 -/
theorem layer4_trivial_A (R : Matrix (Fin 3) (Fin 3) ℂ)
    (hcond : HasConditionForm diag3 diag3 R) (hker : adLin diag3 R = 0) : R = 0 := by
  have hrange : R ∈ LinearMap.range (adLin diag3) := by
    obtain ⟨L, hL⟩ := hcond
    exact ⟨L, by simpa [adLin] using hL.symm⟩
  have hmem : R ∈ LinearMap.ker (adLin diag3) ⊓ LinearMap.range (adLin diag3) :=
    Submodule.mem_inf.mpr ⟨by simpa using hker, hrange⟩
  rw [diag3_ker_inf_range_eq_bot] at hmem
  simpa using hmem

/-- **层 3/层 4 的 A/B 二分（塔高的机检上界）**：
    同一判据下，B 相在层 4 有非零解、A 相在层 4 只有零解。
    ⇒ 塔高 `A = 2`（止于层 2）、`B ≥ 4`（越过层 3、层 4）。
    「`B` 塔高恰为 4」或「∞」需要 `SpFiveMorphism` 才能继续，
    本库不存在该结构（`HigherSpCategory.lean` 止于 `SpFourMorphism`），故不主张。 -/
theorem tower_height_A2_B4 :
    (∃ R : Matrix (Fin 3) (Fin 3) ℂ,
        R ≠ 0 ∧ HasConditionForm jordan3 jordan3 R ∧ adLin jordan3 R = 0) ∧
    (∀ R : Matrix (Fin 3) (Fin 3) ℂ,
        HasConditionForm diag3 diag3 R → adLin diag3 R = 0 → R = 0) :=
  ⟨layer4_nontrivial_B, layer4_trivial_A⟩

end MUFPF
