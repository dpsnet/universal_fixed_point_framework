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
