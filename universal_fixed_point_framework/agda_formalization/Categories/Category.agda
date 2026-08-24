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
