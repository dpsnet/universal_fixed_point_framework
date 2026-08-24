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
-- 本文件中 UFPF 相关引用数量：1
-- 更名将在计划确认后统一执行，当前代码不做修改。
-- ============================================================

module Categories.NaturalTransformation where

-- 自然变换定义（UFPF Agda 重形式化用）
-- 简化版：不依赖标准库

open import Agda.Primitive using (Level; _⊔_)
open import Categories.Category
open import Categories.Functor

record NaturalTransformation {o₁ m₁ o₂ m₂ : Level}
                             {C : Category o₁ m₁} {D : Category o₂ m₂}
                             (F G : Functor C D) : Set (o₁ ⊔ m₂) where
  open Category C renaming (Obj to Obj₁; Hom to Hom₁; _∘_ to _∘₁_)
  open Category D renaming (_∘_ to _∘₂_)
  open Functor F renaming (F-obj to F₀; F-hom to F₁)
  open Functor G renaming (F-obj to G₀; F-hom to G₁)

  field
    component : (X : Obj₁) → Hom₂ D (F₀ X) (G₀ X)
    natural   : {X Y : Obj₁} (f : Hom₁ X Y) →
                component Y ∘₂ F₁ f ≡ G₁ f ∘₂ component X
