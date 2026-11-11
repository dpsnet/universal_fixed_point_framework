-- ============================================================
-- D22 方案③ 第一段：双范畴骨架（自伴层 `SpHerm` vs 复谱层 `SpC`）
-- ============================================================
-- 背景：论文命题 2.4.4 L207/L211 的自伴层 `Sp`，与定义 5.11 L852 / 定理 7.31 L1330
-- 的 `Sp_ℂ` / `D_diss` 是两个不同的层。本库的 `SpObj`（SpCategory.lean L31–33）
-- 只有 `n` 与 `A`，对应的是后者（`Sp_ℂ`）。
--
-- 本模块不改 `SpCategory.lean`，只在其上叠一层：
--   * `SpHermObj` = `SpObj` + 自伴见证 `IsHermitian`（即论文 `Sp`）；
--   * `SpHermHom` 与 `SpHom` 同形（交织等式不受自伴条件影响）；
--   * `forgetObj : SpHermObj → SpObj` 给出对象层面的遗忘。
--
-- 结论（本模块机检）：A 相代表 `diag3` 在自伴层内，B 相代表 `jordan3` 不在
-- ⇒ 遗忘不是满的，这正是「需要两个范畴」的结构理由。
-- ============================================================

import MUFPFormalization.SpCategory
import MUFPFormalization.SpLayerSeparability

namespace MUFPF

open CategoryTheory

/-- 自伴层的对象：`SpObj` 加一个自伴见证。 -/
structure SpHermObj where
  toSp : SpObj
  isHerm : IsHermitian toSp

/-- 自伴层的态射：与 `SpHom` 同形。交织等式 `P * Y.A = X.A * P` 不因加自伴条件而改变，
    因为自伴性是对象的属性而非态射的约束。 -/
@[ext]
structure SpHermHom (X Y : SpHermObj) where
  P : Matrix (Fin X.toSp.n) (Fin Y.toSp.n) ℂ
  intertwine : P * Y.toSp.A = X.toSp.A * P

instance spHermCategory : Category.{0, 0} SpHermObj where
  Hom X Y := SpHermHom X Y
  id X := ⟨1, by simp⟩
  comp f g := ⟨f.P * g.P, by
    rw [Matrix.mul_assoc, g.intertwine]
    rw [← Matrix.mul_assoc, f.intertwine]
    rw [Matrix.mul_assoc]⟩
  id_comp := by
    intro X Y f
    ext
    simp
  comp_id := by
    intro X Y f
    ext
    simp
  assoc := by
    intro W X Y Z f g h
    ext i j
    exact congrArg (fun M => M i j) (Matrix.mul_assoc f.P g.P h.P)

/-- 遗忘到复谱层（对象层面）：`SpHerm → SpC`。 -/
def forgetObj : SpHermObj → SpObj := SpHermObj.toSp

/-- A 相代表（自伴、塔高 2）是自伴层内的对象。 -/
def diag3HermObj : SpHermObj where
  toSp := ⟨3, MUFPFormalization.diag3⟩
  isHerm := by
    show IsHermitian ⟨3, MUFPFormalization.diag3⟩
    exact MUFPFormalization.diag3_conjTranspose_eq

/-- **遗忘非满（对象层面）**：B 相代表 `jordan3`（塔高 4/∞）不是自伴层内的对象。
    这正是「需要两个范畴」的结构理由——有引力相在 `Sp_ℂ` 里，不在自伴 `Sp` 里。 -/
theorem jordan3_not_in_herm_layer :
    ¬ ∃ E : SpHermObj, E.toSp = ⟨3, MUFPFormalization.jordan3⟩ := by
  rintro ⟨E, h⟩
  have hh : IsHermitian ⟨3, MUFPFormalization.jordan3⟩ := h ▸ E.isHerm
  have h2 : MUFPFormalization.jordan3 = Matrix.conjTranspose MUFPFormalization.jordan3 := hh
  exact MUFPFormalization.jordan3_conjTranspose_ne h2

end MUFPF
