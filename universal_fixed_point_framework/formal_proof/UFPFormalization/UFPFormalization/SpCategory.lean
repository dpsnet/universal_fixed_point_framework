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
-- 本文件中 UFPF 相关引用数量：2
-- 更名将在计划确认后统一执行，当前代码不做修改。
-- ============================================================

import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.CategoryTheory.Category.Basic
import Mathlib.Tactic.Ext

namespace UFPFormalization

open CategoryTheory

/-- Spectral category object: a finite-dimensional complex vector space
    equipped with a linear operator. -/
structure SpObj where
  n : ℕ
  A : Matrix (Fin n) (Fin n) ℂ

/-- Morphism in the spectral category: a matrix intertwining the operators. -/
@[ext]
structure SpHom (X Y : SpObj) where
  P : Matrix (Fin X.n) (Fin Y.n) ℂ
  intertwine : P * Y.A = X.A * P

instance spCategory : Category.{0, 0} SpObj where
  Hom X Y := SpHom X Y
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
    exact congr_arg (fun M => M i j) (Matrix.mul_assoc f.P g.P h.P)

@[simp]
lemma SpHom.id_P (X : SpObj) : ((𝟙 X) : SpHom X X).P = 1 := rfl

@[simp]
lemma SpHom.comp_P {X Y Z : SpObj} (f : X ⟶ Y) (g : Y ⟶ Z) :
    ((f ≫ g) : SpHom X Z).P = f.P * g.P := rfl

end UFPFormalization
