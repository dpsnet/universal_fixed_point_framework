module Categories.Functor where

-- 函子定义（UFPF Agda 重形式化用）
-- 简化版：不依赖标准库

open import Agda.Primitive using (Level; _⊔_)
open import Categories.Category

record Functor {o₁ m₁ o₂ m₂ : Level}
               (C : Category o₁ m₁) (D : Category o₂ m₂) : Set (o₁ ⊔ m₁ ⊔ o₂ ⊔ m₂) where
  open Category C renaming (Obj to Obj₁; Hom to Hom₁; id to id₁; _∘_ to _∘₁_)
  open Category D renaming (Obj to Obj₂; Hom to Hom₂; id to id₂; _∘_ to _∘₂_)

  field
    F-obj : Obj₁ → Obj₂
    F-hom : {X Y : Obj₁} → Hom₁ X Y → Hom₂ (F-obj X) (F-obj Y)
    F-id  : {X : Obj₁} → F-hom (id₁ X) ≡ id₂ (F-obj X)
    F-comp : {X Y Z : Obj₁} (f : Hom₁ X Y) (g : Hom₁ Y Z) →
             F-hom (g ∘₁ f) ≡ F-hom g ∘₂ F-hom f

-- 忠实函子
record FaithfulFunctor {o₁ m₁ o₂ m₂ : Level} {C : Category o₁ m₁} {D : Category o₂ m₂}
                       (F : Functor C D) : Set (o₁ ⊔ m₁ ⊔ m₂) where
  open Functor F
  field
    faithful : {X Y : Obj₁ C} {f g : Hom₁ C X Y} → F-hom {X} {Y} f ≡ F-hom {X} {Y} g → f ≡ g
