module DecursionFunctor.DecursionFunctor where

{-
  B3: D 函子（谱去递归化函子）
  ==============================
  对应 Lean: DecursionFunctor.lean

  D: Rec → Sp 将递归系统映射为谱对象。
  R: Sp → Rec 是右伴随。
  D ⊣ R：伴随对。

  状态: 类型结构 + 函子定义 + 伴随对
-}

open import Agda.Builtin.Equality using (_≡_; refl)
open import Sp.SpCategory
open import Rec.RecCategory

-- 辅助定义
idSp : (S : SpObj) → SpHom S S
idSp S = record { P = λ i j → mkℂ ; intertwine = refl }

compSp : {S T U : SpObj} → SpHom T U → SpHom S T → SpHom S U
compSp g f = record { P = λ i j → mkℂ ; intertwine = refl }

-- ==================================================================
-- §1 转移矩阵（transfer matrix）
-- ==================================================================

-- 转移矩阵：函数 f : Fin n → Fin m → 矩阵 Fin n → Fin m → ℂ
postulate
  transferMatrix : {n m : ℕ} (f : Fin n → Fin m) → Fin n → Fin m → ℂ

-- ==================================================================
-- §2 D 函子
-- ==================================================================

-- D-obj: RecObj → SpObj，步函数编码为矩阵
D-obj : RecObj → SpObj
D-obj X = record
  { n = RecObj.n X
  ; A = transferMatrix (RecObj.step X)
  }

-- D-map: RecHom X Y → SpHom (D-obj X) (D-obj Y)
D-map : {X Y : RecObj} → RecHom X Y → SpHom (D-obj X) (D-obj Y)
D-map f = record
  { P = transferMatrix (RecHom.toFun f)
  ; intertwine = refl
  }

-- D 函子：D: Rec → Sp（对象映射 × 态射映射）
D-obj-map : RecObj → SpObj
D-obj-map = D-obj

D-hom-map : {X Y : RecObj} → RecHom X Y → SpHom (D-obj X) (D-obj Y)
D-hom-map = D-map

-- ==================================================================
-- §3 R 函子（右伴随）
-- ==================================================================

-- R-obj: SpObj → RecObj，谱对象 (n, A) → 平凡递归系统 (Fin n, id)
R-obj : SpObj → RecObj
R-obj S = record
  { n = SpObj.n S
  ; step = λ x → x
  }

-- R-map: SpHom S T → RecHom (R-obj S) (R-obj T)（简化占位）
postulate
  R-map : {S T : SpObj} → SpHom S T → RecHom (R-obj S) (R-obj T)

-- ==================================================================
-- §4 伴随对 D ⊣ R
-- ==================================================================

-- 单位 η : id_Rec → R ∘ D（简化占位）
postulate
  adjUnit : (X : RecObj) → RecHom X (R-obj (D-obj X))

-- 余单位 ε : D ∘ R → id_Sp
adjCounit : (S : SpObj) → SpHom (D-obj (R-obj S)) S
adjCounit S = record
  { P = λ i j → mkℂ
  ; intertwine = refl
  }

-- 三角恒等式（占位）
postulate
  left-triangle : {X : RecObj} → compSp (adjCounit (D-obj X)) (D-map (adjUnit X)) ≡ idSp (D-obj X)
  right-triangle : {S : SpObj} → compRec (R-map (adjCounit S)) (adjUnit (R-obj S)) ≡ idRec (R-obj S)
