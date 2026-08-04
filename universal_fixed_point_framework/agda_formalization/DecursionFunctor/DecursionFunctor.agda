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
-- （**T2 闭合**：具体定义，对应 Lean transferMatrix = fun i j => if f i = j then 1 else 0）
transferMatrix : {n m : ℕ} (f : Fin n → Fin m) → Fin n → Fin m → ℂ
transferMatrix f i j = if Fin-eq? (f i) j then c1 else c0

-- 转移矩阵反变复合：(g∘f) 的转移矩阵 = f 的转移矩阵 · g 的转移矩阵
-- （对应 Lean: transferMatrix_comp）
transferMatrix-comp : {n m p : ℕ} (f : Fin n → Fin m) (g : Fin m → Fin p)
  → transferMatrix (λ x → g (f x)) ≡ transferMatrix f *mat transferMatrix g
transferMatrix-comp {n} {m} {p} f g = funext (λ i → funext (λ j → pt i j))
  where
  pt : (i : Fin n) (j : Fin p)
    → transferMatrix (λ x → g (f x)) i j ≡ (transferMatrix f *mat transferMatrix g) i j
  pt i j =
    trans (sym (sumFin-pick-dep-l {m} (f i) (λ k → if Fin-eq? (g k) j then c1 else c0)))
          (sym (sumFin-cong {m} (λ k → if-mul-lemma (Fin-eq? (f i) k)
                                        (if Fin-eq? (g k) j then c1 else c0))))

-- 转移矩阵单射：transferMatrix f ≡ transferMatrix g → f ≡ g
-- （对应 Lean: transferMatrix_injective；**T2 闭合**：D 忠实性的基础）
transferMatrix-inj : {n m : ℕ} {f g : Fin n → Fin m} → transferMatrix f ≡ transferMatrix g → f ≡ g
transferMatrix-inj {n} {m} {f} {g} h = funext (λ x → step x)
  where
  step : (x : Fin n) → f x ≡ g x
  step x = sym (Fin-eq?-true (g x) (f x) (if-c1 (Fin-eq? (g x) (f x)) (lemma x)))
    where
    lemma : (x : Fin n) → (if Fin-eq? (g x) (f x) then c1 else c0) ≡ c1
    lemma x = trans (sym (cong-app (cong-app h x) (f x)))
                    (cong (λ b → if b then c1 else c0) (Fin-eq?-refl (f x)))

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
-- （**T2 闭合**：transferMatrix-comp + RecHom.comm，对应 Lean DFunctor_map）
D-map-intertwine : {X Y : RecObj} (f : RecHom X Y)
  → transferMatrix (RecHom.toFun f) *mat transferMatrix (RecObj.step Y)
      ≡ transferMatrix (RecObj.step X) *mat transferMatrix (RecHom.toFun f)
D-map-intertwine {X} {Y} f =
  trans (sym (transferMatrix-comp (RecHom.toFun f) (RecObj.step Y)))
  (trans (cong transferMatrix (sym (funext (λ x → RecHom.comm f x))))
         (transferMatrix-comp (RecObj.step X) (RecHom.toFun f)))

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

-- R-map: SpHom S T → RecHom (R-obj S) (R-obj T)
-- （登记待闭合：论文正确构造 R11/C2.2 用演化映射 e^{-A_E}（保留谱信息），
--   Lean 侧恒等 toFun（Adjunction.lean L29-33）隐含 nS=nT 且 S.A=单位矩阵两个
--   未声明条件，非论文构造的忠实实现；Agda 泛化下恒等不可构造，
--   有限维化依赖 exp（T3）。）
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

-- 右三角恒等式（登记待闭合：对应论文构造 C2.2/R11 的有限维化，依赖 T3 分析层）
-- 论文正确构造（定理 2.4.5 / 定理 R11）：R(E) 状态空间 = D(A_E)，演化映射 = e^{-A_E}
-- （保留谱信息），仅在 D 的像（可对角化谱对象的全子范畴）上严格成立。
-- Lean 侧恒等原型（step=id, P=1）丢失谱信息且隐含 nS=nT 与 S.A=单位矩阵两个未声明条件，
-- 非论文构造的忠实实现；Agda 有限载体（ℤ/3）无法承载 e^{-A}，有限维化需 exp（T3）。
postulate
  right-triangle : {S : SpObj} → compRec (R-map (adjCounit S)) (adjUnit (R-obj S)) ≡ idRec (R-obj S)

-- ==================================================================
-- §5 R11 有限维化：SpImD 子范畴（对应 RAP5a_explicit_adjunction.lean）
-- ==================================================================
-- 论文正确构造（定理 2.4.5 / 定理 R11）的有限维对应：
-- 伴随限制在 D 的像子范畴 SpImD = Σ(src, tgt, Iso(D(src), tgt)) 上，
-- R_im = 第一投影。本节省去泛化 R-map（不可构造），对象层闭合。

-- 本地 UIP / 层级提升 cong（Set₁ 版，避免耦合 HigherSpCategory）
uip₁ : {A : Set} {x y : A} (p q : x ≡ y) → p ≡ q
uip₁ refl refl = refl

cong₁ : {A : Set} {B : Set₁} {x y : A} (f : A → B) → x ≡ y → f x ≡ f y
cong₁ f refl = refl

-- Sp 范畴中的矩阵同构：P·Q = Q·P = 𝟙（方形 ⇒ nS = nT，规避泛化维度问题）
record SpIso (S T : SpObj) : Set where
  field
    P : Fin (SpObj.n S) → Fin (SpObj.n T) → ℂ
    Q : Fin (SpObj.n T) → Fin (SpObj.n S) → ℂ
    isP-intertwine : P *mat SpObj.A T ≡ SpObj.A S *mat P
    isQ-intertwine : Q *mat SpObj.A S ≡ SpObj.A T *mat Q
    P-Q : P *mat Q ≡ 𝟙-matrix
    Q-P : Q *mat P ≡ 𝟙-matrix

-- 恒等同构（单位矩阵）
SpIso-refl : (S : SpObj) → SpIso S S
SpIso-refl S = record
  { P = 𝟙-matrix
  ; Q = 𝟙-matrix
  ; isP-intertwine = unit-intertwine
  ; isQ-intertwine = unit-intertwine
  ; P-Q = *mat-id-l (𝟙-matrix {SpObj.n S})
  ; Q-P = *mat-id-l (𝟙-matrix {SpObj.n S})
  }

-- Sp 真实恒等态射（单位矩阵；区别于 §辅助的 zeroMat 占位版本）
idSp-real : (S : SpObj) → SpHom S S
idSp-real S = record { P = 𝟙-matrix ; intertwine = unit-intertwine }

-- SpHom 记录相等：P 相等 + 交织证明相等（uip）
SpHom-≡ : {X Y : SpObj} {f g : SpHom X Y} → SpHom.P f ≡ SpHom.P g → f ≡ g
SpHom-≡ {f = f} {g = g} refl =
  cong₁ (λ p → record { P = SpHom.P f ; intertwine = p })
        (uip₁ (SpHom.intertwine f) (SpHom.intertwine g))

-- D 的像子范畴：源递归系统 + 目标谱对象 + 同构见证（对应 Lean SpImD）
record SpImD : Set where
  field
    src : RecObj
    tgt : SpObj
    conn : SpIso (D-obj src) tgt

-- R_im 对象映射：第一投影（对应 Lean RIm_obj）
R-obj-img : SpImD → RecObj
R-obj-img E = SpImD.src E

-- 编码函子 D_im：Rec → SpImD（对应 Lean DIm_obj）
DIm-obj : RecObj → SpImD
DIm-obj X = record { src = X ; tgt = D-obj X ; conn = SpIso-refl (D-obj X) }

-- DR 同构：D(R_im(E)) ≅ E.tgt（由 conn 给出，对应 Lean DR_iso）
DR-iso : (E : SpImD) → SpIso (D-obj (R-obj-img E)) (SpImD.tgt E)
DR-iso E = SpImD.conn E

-- 单位 η_E = conn 的逆（Q 矩阵，对应 Lean adjUnit）
adjUnit-img : (E : SpImD) → SpHom (SpImD.tgt E) (D-obj (R-obj-img E))
adjUnit-img E = record
  { P = SpIso.Q (SpImD.conn E)
  ; intertwine = SpIso.isQ-intertwine (SpImD.conn E)
  }

-- 余单位 ε_X = 恒等递归同态（对应 Lean adjCounit）
adjCounit-img : (X : RecObj) → RecHom (R-obj-img (DIm-obj X)) X
adjCounit-img X = idRec X

-- 左三角恒等式（对象层闭合）：(Dε)∘η = id，P 部分 𝟙·𝟙 = 𝟙（*mat-id-l）
left-triangle-img : {X : RecObj} →
  compose (D-map (adjCounit-img X)) (adjUnit-img (DIm-obj X)) ≡ idSp-real (D-obj X)
left-triangle-img {X} = SpHom-≡ (*mat-id-l (𝟙-matrix {SpObj.n (D-obj X)}))

-- 态射层（RIm_map/右三角）结构性不可闭合（基数反例，全范畴/集合语义）：
--   2 状态平凡系统下 Hom_Sp(D(X),D(Y)) = ℂ⁴（不可数）vs Hom_Rec(X,Y) = 4（有限），
--   自然同构无双射；P = [[1,0],[1,1]] 是合法谱态射但非转移矩阵（D 的 full 性为假）。
--   闭合仅当态射限制为转移矩阵（线性语义，Lean 侧已实现：RAP5a SpImDMor
--   限制为线性态射层后 RIm_map = 恒等提取，D_im ⊣ R_im 完整伴随，2026-08-04）
--   或转无限维（论文 R11，需 T3 谱定理）。
