module Rec.RecCategory where

{-
  Rec 范畴定义（UFPF Agda 重形式化用）
  对应 Lean: RecCategory.lean

  对象：有限状态 Fin n + 演化规则 step : Fin n → Fin n
  态射：保持 step 的函数 f : Fin n → Fin m（f ∘ step_X = step_Y ∘ f）

  简化：直接使用 Fin n 作为状态空间（通过 Fintype.equivFin 归一化）
-}

open import Agda.Builtin.Equality using (_≡_; refl)
open import Sp.SpCategory using (ℕ; Fin; cong; trans)

-- （trans/cong 统一定义于 SpCategory 基础层，此处引用）

-- Rec 对象：有限状态 Fin n + 演化规则 step
record RecObj : Set where
  field
    n : ℕ
    step : Fin n → Fin n

-- Rec 态射：函数 f + 交换条件 f ∘ step_X = step_Y ∘ f
record RecHom (X Y : RecObj) : Set where
  open RecObj X renaming (n to nX; step to stepX)
  open RecObj Y renaming (n to nY; step to stepY)

  field
    toFun : Fin nX → Fin nY
    comm  : ∀ (x : Fin nX) → toFun (stepX x) ≡ stepY (toFun x)

-- 恒等态射
idRec : (X : RecObj) → RecHom X X
idRec X = record
  { toFun = λ x → x
  ; comm  = λ _ → refl
  }

-- 态射复合
compRec : {X Y Z : RecObj} → RecHom Y Z → RecHom X Y → RecHom X Z
compRec {X} {Y} {Z} g f = record
  { toFun = λ x → RecHom.toFun g (RecHom.toFun f x)
  ; comm  = λ x → trans (cong (RecHom.toFun g) (RecHom.comm f x))
                        (RecHom.comm g (RecHom.toFun f x))
  }
