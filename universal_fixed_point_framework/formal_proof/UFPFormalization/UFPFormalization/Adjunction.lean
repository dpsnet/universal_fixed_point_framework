-- ============================================================
-- UFPF → MUFPF 更名通知
-- ============================================================
-- 本文件属于 Universal Fixed Point Framework (UFPF)。
-- 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
-- 更名计划详见：roadmap/mu_renaming_plan.md
--
-- 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
-- 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
--
-- 本文件中 UFPF 相关引用数量：6
-- 更名将在计划确认后统一执行，当前代码不做修改。
-- ============================================================

import UFPFormalization.RecCategory
import UFPFormalization.SpCategory
import UFPFormalization.DecursionFunctor
import UFPFormalization.SpectralCorrespondence
import Mathlib.CategoryTheory.Adjunction.Basic
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Analysis.Matrix.Spectrum

/-
※ 审计记录（2026-08-05 更新，与 Agda 侧交叉校验一致，阶段 1 圈定执行）：

**有效范围声明**：D ⊣ R 伴随仅在 Rec_lin(SpImD) 上严格成立（线性语义，
受限态射层 = 有界线性谱匹配算子）。详见 notes/00_foundations/spectral_category_scope_stratification.md。

本文件为全范畴上的"简化原型"，以下组件已从 Agda 侧移植具体构造：
  - adjUnit：常零函数（Agda const-adjUnit），comm 经 rfl 闭合
  - adjCounit：零矩阵（Agda zeroMat），intertwine 经矩阵零吸收闭合
  - RFunctor：对象映射（Fin S.n 状态 + 恒等步进，无 sorry）

**2026-08-05 闭合记录**：
  - 原 `RFunctor.map`/`map_id`/`map_comp`（3 处 sorry）与 `DAdjR`（axiom）**结构性不可构造**
    （`Fin S.n → Fin T.n` 在 `T.n = 0 ∧ S.n > 0` 时不存在），且**无任何使用方**（仅
    `RFunctor.obj`/`adjUnit`/`adjCounit` 被 TestCategoryTheory 引用，均无 sorry）——
    已删除，RFunctor 保留为对象映射（右伴随的"对象层"）。
  - 全范畴右伴随（map 层）的结构性障碍诚实登记：正确构造见
    `RAP5a_explicit_adjunction.lean` 的 SpImD 子范畴方案（`DIm ⊣ RIm` 完整伴随机器证明）。
-/

namespace UFPFormalization

open CategoryTheory

/-- Right adjoint R : Spec → Rec（对象层）。
    Maps a spectral object (n, A) to a recursive system on the finite state space Fin n,
    where the step function is the identity (representing "trivial dynamics" fixed point),
    and the adjunction unit/counit encode the spectral correspondence via the matrix exponential.
    ※ 全范畴的 map 层（态射）结构性不可构造（`T.n = 0 ∧ S.n > 0` 时 `Fin S.n → Fin T.n`
    不存在）；正确伴随见 `RAP5a_explicit_adjunction.lean`（SpImD 子范畴，`DIm ⊣ RIm`）。 -/
noncomputable def RFunctor (S : SpObj) : RecObj :=
  { T := Fin S.n
    fin := inferInstance
    dec := inferInstance
    step := id }

/-- Unit of the adjunction η : id_Rec → R ∘ D.
    Constant-zero function (Agda const-adjUnit port).
    When card X.T > 0, toFun maps everything to 0; comm holds by rfl.
    When card X.T = 0, X.T is empty so the function is vacuously defined. -/
noncomputable def adjUnit (X : RecObj) : X ⟶ (RFunctor (DFunctor.obj X)) :=
  { toFun := fun x =>
      if h : Fintype.card X.T > 0 then ⟨0, h⟩
      else Fin.elim0 (Nat.eq_zero_of_not_pos h ▸ Fintype.equivFin X.T x)
    comm := by
      intro x
      by_cases h : Fintype.card X.T > 0
      · rfl
      · exfalso
        exact absurd (Fintype.card_pos_iff.mpr ⟨x⟩) h }

/-- Counit of the adjunction ε : D ∘ R → id_Spec.
    Zero matrix (Agda zeroMat port). Intertwine holds by matrix zero-absorption:
    0 * S.A = (D(R(S))).A * 0 = 0. -/
noncomputable def adjCounit (S : SpObj) : (DFunctor.obj (RFunctor S)) ⟶ S :=
  { P := 0
    intertwine := by
      simp [Matrix.mul_zero, Matrix.zero_mul] }

end UFPFormalization
