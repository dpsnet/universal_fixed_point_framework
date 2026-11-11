-- ============================================================
-- `DFunctor` 值域上的自伴性：强形式证伪
-- ============================================================
-- D35（`SpDFunctorRange.lean`）立了两条独立事实：
--   ① `SpC` 非全自伴（`not_all_spObj_hermitian`）
--   ② `SpHerm ⥤ SpC` 对象层面不满（`forgetFunctor_not_surjective_on_objects`）
-- 「`DFunctor` 的**每个**像都非自伴」这一强形式当时未机检，六轮构建都卡在
-- `Fintype.equivFin` 的具体实现无法用 `simp` 展开（停在 `sorry ()` 占位）。
--
-- 本模块的判断：**强形式是假命题**，且不需要展开 `equivFin` 就能证伪。
--
-- 关键动作：`DFunctor_obj X` 的 `A` 就是 `stepMatrix (e ∘ X.step ∘ e.symm)`。
-- 取 `X.step = id`，则复合恒等于 `id`（`e ∘ e.symm = id`），而 `stepMatrix id = 1`。
-- 单位阵自伴 ⇒ 值域内存在自伴像。
-- 全程只需 `stepMatrix id = 1` 这一条抽象引理，**不触碰** `Fintype.card`、
-- `Subsingleton (Fin _)` 或 `equivFin` 的内部结构——这正是六轮失败的动作。
-- ============================================================

import MUFPFormalization.SpCategory
import MUFPFormalization.DecursionFunctor

namespace MUFPF

open CategoryTheory Matrix

/-- 恒等演化规则给出单位转移矩阵。 -/
lemma stepMatrix_id {α : Type} [Fintype α] [DecidableEq α] :
    stepMatrix (id : α → α) = 1 := by
  ext i j
  simp [stepMatrix, transferMatrix, Matrix.one_apply]

/-- 单点状态空间 + 恒等演化规则。 -/
def idRec1 : RecObj where
  T := Fin 1
  fin := inferInstance
  dec := inferInstance
  step := id

/-- `DFunctor` 在 `idRec1` 上的像的算子是单位阵。 -/
lemma DFunctor_obj_idRec1_A : (DFunctor.obj idRec1).A = 1 := by
  change stepMatrix (Fintype.equivFin idRec1.T ∘ idRec1.step
      ∘ (Fintype.equivFin idRec1.T).symm) = 1
  have hcomp : Fintype.equivFin idRec1.T ∘ idRec1.step
      ∘ (Fintype.equivFin idRec1.T).symm = id := by
    funext x
    exact Equiv.apply_symm_apply _ x
  rw [hcomp, stepMatrix_id]

/-- 该像**自伴**。 -/
lemma DFunctor_obj_idRec1_isHermitian : IsHermitian (DFunctor.obj idRec1) := by
  rw [IsHermitian, DFunctor_obj_idRec1_A, Matrix.conjTranspose_one]

/-- **强形式证伪**：并非「`DFunctor` 的每个像都非自伴」。

    这一条直接否掉 D35 遗留的强形式；相应地把正确表述落成
    「值域内**存在**自伴像」（对应转移规则恒等的情形），
    而不是「值域内所有像都非自伴」。 -/
theorem not_all_DFunctor_objects_nonhermitian :
    ¬ ∀ X : RecObj.{0}, ¬ IsHermitian (DFunctor.obj X) := by
  intro h
  exact h idRec1 DFunctor_obj_idRec1_isHermitian

end MUFPF
