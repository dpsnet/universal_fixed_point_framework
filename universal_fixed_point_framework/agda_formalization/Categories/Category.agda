module Categories.Category where

-- 基础范畴定义（UFPF Agda 重形式化用）
-- 简化版：不依赖标准库，使用 Agda 内建类型

open import Agda.Primitive using (Level; lzero; lsuc; _⊔_)

-- 范畴定义
record Category (o m : Level) : Set (lsuc (o ⊔ m)) where
  field
    Obj  : Set o
    Hom  : Obj → Obj → Set m
    id   : (X : Obj) → Hom X X
    _∘_  : {X Y Z : Obj} → Hom Y Z → Hom X Y → Hom X Z

  field
    assoc   : {W X Y Z : Obj} (f : Hom W X) (g : Hom X Y) (h : Hom Y Z) →
              (h ∘ g) ∘ f ≡ h ∘ (g ∘ f)
    identity-left  : {X Y : Obj} (f : Hom X Y) → id Y ∘ f ≡ f
    identity-right : {X Y : Obj} (f : Hom X Y) → f ∘ id X ≡ f
