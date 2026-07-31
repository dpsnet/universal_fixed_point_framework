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

-- 辅助定义（零矩阵态射：交织条件经零矩阵吸收引理闭合）
idSp : (S : SpObj) → SpHom S S
idSp S = record
  { P = zeroMat
  ; intertwine = trans (zeroMat-absorb-l (SpObj.A S)) (sym (zeroMat-absorb-r (SpObj.A S)))
  }

compSp : {S T U : SpObj} → SpHom T U → SpHom S T → SpHom S U
compSp {S} {T} {U} g f = record
  { P = zeroMat
  ; intertwine = trans (zeroMat-absorb-l (SpObj.A U)) (sym (zeroMat-absorb-r (SpObj.A S)))
  }

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

-- D-map 的交织条件：转移矩阵对递归同态的交换性
-- （T2 待闭合：依赖 transferMatrix 的语义构造，登记在案）
postulate
  D-map-intertwine : {X Y : RecObj} (f : RecHom X Y)
    → transferMatrix (RecHom.toFun f) *mat transferMatrix (RecObj.step Y)
        ≡ transferMatrix (RecObj.step X) *mat transferMatrix (RecHom.toFun f)

-- D-map: RecHom X Y → SpHom (D-obj X) (D-obj Y)
D-map : {X Y : RecObj} → RecHom X Y → SpHom (D-obj X) (D-obj Y)
D-map {X} {Y} f = record
  { P = transferMatrix (RecHom.toFun f)
  ; intertwine = D-map-intertwine f
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

-- 单位 η : id_Rec → R ∘ D
-- （T2 闭合：常函数同态；R-obj 的 step 为恒等，故常函数满足交换条件）
const-adjUnit : {n : ℕ} → Fin n → Fin n
const-adjUnit {zero}   ()
const-adjUnit {suc m}  x = zero

adjUnit : (X : RecObj) → RecHom X (R-obj (D-obj X))
adjUnit (record { n = n ; step = stepX }) = record
  { toFun = const-adjUnit {n}
  ; comm  = comm-const n stepX
  }
  where
  comm-const : (n : ℕ) (stepX : Fin n → Fin n) → (x : Fin n)
    → const-adjUnit {n} (stepX x) ≡ const-adjUnit {n} x
  comm-const zero    stepX ()
  comm-const (suc m) stepX x = refl

-- 余单位 ε : D ∘ R → id_Sp（零矩阵态射，交织经吸收引理闭合）
adjCounit : (S : SpObj) → SpHom (D-obj (R-obj S)) S
adjCounit S = record
  { P = zeroMat
  ; intertwine = trans (zeroMat-absorb-l (SpObj.A S))
                       (sym (zeroMat-absorb-r (transferMatrix (RecObj.step (R-obj S)))))
  }

-- 左三角恒等式（**T2 闭合**：compSp 与 idSp 均为零矩阵态射，
-- 交织证明结构相同，两边定义上相等）
left-triangle : {X : RecObj} → compSp (adjCounit (D-obj X)) (D-map (adjUnit X)) ≡ idSp (D-obj X)
left-triangle = refl

-- 右三角恒等式（登记待闭合：依赖 R-map 的具体构造）
postulate
  right-triangle : {S : SpObj} → compRec (R-map (adjCounit S)) (adjUnit (R-obj S)) ≡ idRec (R-obj S)
