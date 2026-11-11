-- ============================================================
-- `DFunctor` 值域重定向的结构见证（任务第 3 项第三部分）
-- ============================================================
-- 问题：`DFunctor : RecObj ⥤ SpObj` 的像能否整体落在自伴层 `SpHerm`？
-- 若可以，双范畴拆分（方案③）在 `D` 的像上是多余的；若不可以，
-- `DFunctor` 的真正值域只能是 `Sp_ℂ`（`SpC`），论文命题 2.4.4 L211
-- 的「`D` 的像始终在 `Sp` 中」只对 `D_diss`（定理 7.31 L1330）成立。
--
-- 本模块机检两件事：
--   1. n = 3 的循环置换算子（`stepMatrix ![1,2,0]`，即 `DFunctor_obj` 的原型）
--      非自伴：`(0,1)` 元为 1、`(1,0)` 元为 0。
--   2. 因此 `SpC` 不是「全自伴层」——自伴层 `SpHerm` 是真子范畴，
--      `DFunctor` 的值域不能取 `SpHerm`。
--
-- 边界（未机检，登记）：`DFunctor_obj X` 的 `A` 是 `stepMatrix` 在
-- `Fintype.equivFin X.T` 下的重标号形式；第 1 条给的是该族的原型，
-- 「`DFunctor` 的每个对象都属于这一族」由 `DecursionFunctor.lean` L73–74
-- 的定义直接读出，但把它逐字对上原型需要 `Fintype.equivFin (Fin 3)` 的具体实现，
-- 本模块不展开该实现。
-- ============================================================

import MUFPFormalization.DecursionFunctor
import MUFPFormalization.SpHermCategory

namespace MUFPF

open Matrix

/-- `Fin 3` 上的循环置换：`0 ↦ 1 ↦ 2 ↦ 0`（记作 `![1,2,0]`）。 -/
def cyclicStep3 : Fin 3 → Fin 3 := ![1, 2, 0]

/-- n = 3 循环置换对应的谱算子（`Sp_ℂ` 中的对象，`DFunctor_obj` 的矩阵原型）。 -/
abbrev cyclic3SpObj : SpObj := ⟨3, stepMatrix cyclicStep3⟩

/-- **循环置换算子非自伴**：`(0,1)` 元为 `1`、`(1,0)` 元为 `0`，
    与自伴判据 `A i j = star (A j i)` 冲突。 -/
theorem cyclic3SpObj_not_hermitian : ¬ IsHermitian cyclic3SpObj := by
  intro h
  have h01 := (isHermitian_iff_entries.mp h) (0 : Fin 3) (1 : Fin 3)
  simp [stepMatrix, transferMatrix, cyclicStep3] at h01

/-- **`SpC` 不是全自伴层**：存在非自伴对象 ⇒ 自伴层 `SpHerm` 是真子范畴。
    这是「双范畴不能合并」的对象级依据。 -/
theorem not_all_spObj_hermitian : ¬ ∀ E : SpObj, IsHermitian E := by
  intro h
  exact cyclic3SpObj_not_hermitian (h cyclic3SpObj)

/-- **遗忘函子在对象层面不满 —— `SpHerm` 是 `SpC` 的真子范畴**：
    n = 3 循环置换算子不可能被自伴化，因而没有 `SpHermObj` 以它为遗忘像。
    配合 `forgetFunctor_faithful` / `forgetFunctor_full`，得到对 `SpHerm` 位置的完整刻画：
    全忠实的真子范畴嵌入，对象被自伴条件严格裁掉。 -/
theorem forgetFunctor_not_surjective_on_objects :
    ∃ E : SpObj, ¬ ∃ X : SpHermObj, X.toSp = E := by
  refine ⟨cyclic3SpObj, ?_⟩
  rintro ⟨X, hX⟩
  exact cyclic3SpObj_not_hermitian (Eq.subst hX X.isHerm)

end MUFPF
