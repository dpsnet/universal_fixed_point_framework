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
-- 本文件中 UFPF 相关引用数量：4
-- 更名将在计划确认后统一执行，当前代码不做修改。
-- ============================================================

import UFPFormalization.RecCategory
import UFPFormalization.AInfinityAlgebra
import Mathlib.CategoryTheory.Category.Basic
import Mathlib.Data.Matrix.Basic

open CategoryTheory Matrix

namespace UFPFormalization

/-! 
# Rec_∞ : ∞-Category of Recursive Systems (Phase 31.1)

Rec_∞ is the strict ∞-category lifting of the ordinary category `Rec`.

In this finite prototype we keep the same objects and 1-morphisms as `Rec`,
and declare all higher homotopies to be trivial (identity).  This is the
natural ∞-category associated to an ordinary category: it has no non-trivial
higher cells.

The non-trivial ∞-structure appears after applying the decursion functor
D_∞ : Rec_∞ → Spec_∞, where spectral flow generates genuine higher homotopies.
-/

universe u

/-- Rec_∞ has the same objects as Rec. -/
def RecInfinity : Type _ := RecObj

/-- An ∞-morphism in Rec_∞ is just an ordinary RecHom.

All higher cells are trivial, so the ∞-structure collapses to the underlying
1-category. -/
def RecInfMorphism (X Y : RecObj) : Type _ := X ⟶ Y

/-- The underlying RecHom of an ∞-morphism is the morphism itself. -/
def RecInfMorphism.toRecHom {X Y : RecObj} (α : RecInfMorphism X Y) : X ⟶ Y :=
  α

/-- Vertical composition of ∞-morphisms is ordinary category composition. -/
def recInfVertComp {X Y Z : RecObj} (α : RecInfMorphism X Y) (β : RecInfMorphism Y Z) :
    RecInfMorphism X Z :=
  α ≫ β

/-- Identity ∞-morphism. -/
def recInfId (X : RecObj) : RecInfMorphism X X :=
  𝟙 X

/-- Vertical composition is associative (follows from category axioms). -/
theorem recInfVertComp_assoc {W X Y Z : RecObj}
    (α : RecInfMorphism W X) (β : RecInfMorphism X Y) (γ : RecInfMorphism Y Z) :
    recInfVertComp (recInfVertComp α β) γ = recInfVertComp α (recInfVertComp β γ) :=
  Category.assoc α β γ

/-- Left identity law. -/
theorem recInfId_left {X Y : RecObj} (α : RecInfMorphism X Y) :
    recInfVertComp (recInfId X) α = α :=
  Category.id_comp α

/-- Right identity law. -/
theorem recInfId_right {X Y : RecObj} (α : RecInfMorphism X Y) :
    recInfVertComp α (recInfId Y) = α :=
  Category.comp_id α

end UFPFormalization
