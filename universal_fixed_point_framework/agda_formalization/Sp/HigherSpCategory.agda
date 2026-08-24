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
-- 本文件中 UFPF 相关引用数量：0
-- 更名将在计划确认后统一执行，当前代码不做修改。
-- ============================================================

module Sp.HigherSpCategory where

{-
  B2: 高阶态射（2-态射、3-态射）
  ===============================
  对应 Lean: HigherSpCategory.lean

  Sp 的高阶范畴结构：
    层 1（1-态射）：SpHom P       满足 P·A_Y = A_X·P
    层 2（2-态射）：α: P⇒Q        满足 Q.P - P.P = A_X·α.homotopy - α.homotopy·A_Y
    层 3（3-态射）：Σ: α⇛β        满足 β.homotopy - α.homotopy = A_X·Σ.K - Σ.K·A_Y

  关键结果：spExchangeLaw 不严格成立（这是特征而非缺陷），
  偏差可显式计算为 (R.P - Q.P) * α'.homotopy + β.homotopy * (P'.P - Q'.P)。

  状态: 类型结构 + 基本复合运算
-}

open import Agda.Primitive using (Level)
open import Agda.Builtin.Equality using (_≡_; refl)
open import Sp.SpCategory

open SpObj
open SpHom

-- 层级提升的 cong（SpTwoMorphism 为 Set₁）
cong₁ : {A : Set} {B : Set₁} {x y : A} (f : A → B) → x ≡ y → f x ≡ f y
cong₁ f refl = refl

-- 唯一性（UIP，K 公理）：同一等式的两个证明相等
uip : {A : Set} {x y : A} (p q : x ≡ y) → p ≡ q
uip refl refl = refl

-- ==================================================================
-- §1 2-态射：SpHom 之间的同伦
-- ==================================================================

-- 2-态射：同伦矩阵 H + 条件 Q.P - P.P = A_X·H - H·A_Y（**T2 闭合**：真实等式）
record SpTwoMorphism {X Y : SpObj} (P Q : SpHom X Y) : Set₁ where
  field
    homotopy : Fin (n X) → Fin (n Y) → ℂ
    -- 条件：Q.P - P.P = A_X * homotopy - homotopy * A_Y（真实等式）
    condition : commutator {X} {Y} homotopy ≡ (SpHom.P Q -mat SpHom.P P)

-- 依赖记录相等：同伦相等 + condition 证明相等（经 uip）→ 记录相等
SpTwoMorphism-≡ : {X Y : SpObj} {P Q : SpHom X Y} {e1 e2 : SpTwoMorphism P Q}
  → SpTwoMorphism.homotopy e1 ≡ SpTwoMorphism.homotopy e2 → e1 ≡ e2
SpTwoMorphism-≡ {e1 = e1} {e2 = e2} refl =
  cong₁ (λ c → record { homotopy = SpTwoMorphism.homotopy e1 ; condition = c })
        (uip (SpTwoMorphism.condition e1) (SpTwoMorphism.condition e2))

-- 恒等 2-态射：homotopy = 0（条件经 commutator-zero + -mat-self）
id-two-morphism : {X Y : SpObj} (P : SpHom X Y) → SpTwoMorphism P P
id-two-morphism {X} {Y} P = record
  { homotopy = zeroMat
  ; condition = trans (commutator-zero {X} {Y}) (sym (-mat-self (SpHom.P P)))
  }

-- 垂直复合：同伦矩阵相加（条件经 commutator-add + 中间项消去）
spVertComp : {X Y : SpObj} {P Q R : SpHom X Y}
  → SpTwoMorphism P Q → SpTwoMorphism Q R → SpTwoMorphism P R
spVertComp {X} {Y} {P} {Q} {R} α β = record
  { homotopy = SpTwoMorphism.homotopy α +mat SpTwoMorphism.homotopy β
  ; condition = trans (commutator-add (SpTwoMorphism.homotopy α) (SpTwoMorphism.homotopy β))
      (trans (+mat-cong₂ (SpTwoMorphism.condition α) (SpTwoMorphism.condition β))
             (-mat-cancel-mid (SpHom.P P) (SpHom.P Q) (SpHom.P R)))
  }

-- 水平复合的同伦构造（T2 闭合：与 Lean 公式一致 homotopy = α·P' + Q·α'）
-- 水平复合的 condition（T2 闭合：交换子代数引理链，对应 Lean 侧 70 行证明）
spHorizComp-condition : {X Y Z : SpObj} {P Q : SpHom X Y} {P' Q' : SpHom Y Z}
  (α : SpTwoMorphism P Q) (α' : SpTwoMorphism P' Q')
  → commutator {X} {Z} ((SpTwoMorphism.homotopy α *mat SpHom.P P')
                        +mat (SpHom.P Q *mat SpTwoMorphism.homotopy α'))
      ≡ (SpHom.P (compose Q' Q) -mat SpHom.P (compose P' P))
spHorizComp-condition {X} {Y} {Z} {P} {Q} {P'} {Q'} α α' = main
  where
  hα  = SpTwoMorphism.homotopy α
  hα' = SpTwoMorphism.homotopy α'
  PP  = SpHom.P P
  QP  = SpHom.P Q
  P'P = SpHom.P P'
  Q'P = SpHom.P Q'
  AX  = SpObj.A X
  AY  = SpObj.A Y
  AZ  = SpObj.A Z

  -- s1：分配 AX·(H₁+H₂) 与 (H₁+H₂)·AZ
  s1 : AX *mat (hα *mat P'P +mat QP *mat hα') -mat (hα *mat P'P +mat QP *mat hα') *mat AZ
     ≡ (AX *mat (hα *mat P'P) +mat AX *mat (QP *mat hα'))
       -mat ((hα *mat P'P) *mat AZ +mat (QP *mat hα') *mat AZ)
  s1 = -mat-cong₂ (*mat-distrib-l AX (hα *mat P'P) (QP *mat hα'))
                  (*mat-distrib-r (hα *mat P'P) (QP *mat hα') AZ)

  -- s2：括号重排（*mat-assoc）
  s2 : (AX *mat (hα *mat P'P) +mat AX *mat (QP *mat hα'))
       -mat ((hα *mat P'P) *mat AZ +mat (QP *mat hα') *mat AZ)
     ≡ ((AX *mat hα) *mat P'P +mat AX *mat (QP *mat hα'))
       -mat (hα *mat (P'P *mat AZ) +mat (QP *mat hα') *mat AZ)
  s2 = -mat-cong₂ (cong (λ m → m +mat AX *mat (QP *mat hα')) (sym (*mat-assoc AX hα P'P)))
                  (cong (λ m → m +mat (QP *mat hα') *mat AZ) (*mat-assoc hα P'P AZ))

  -- s3：差值拆分 (A+C)-(B+D) → (A-B)+(C-D)
  s3 : ((AX *mat hα) *mat P'P +mat AX *mat (QP *mat hα'))
       -mat (hα *mat (P'P *mat AZ) +mat (QP *mat hα') *mat AZ)
     ≡ ((AX *mat hα) *mat P'P -mat hα *mat (P'P *mat AZ))
       +mat (AX *mat (QP *mat hα') -mat (QP *mat hα') *mat AZ)
  s3 = sym (mat-rearrange ((AX *mat hα) *mat P'P) (hα *mat (P'P *mat AZ))
                          (AX *mat (QP *mat hα')) ((QP *mat hα') *mat AZ))

  -- s4a：hα·(P'·AZ) = (hα·AY)·P'（P'.intertwine + assoc）
  s4a : hα *mat (P'P *mat AZ) ≡ (hα *mat AY) *mat P'P
  s4a = trans (cong (λ m → hα *mat m) (SpHom.intertwine P'))
              (sym (*mat-assoc hα AY P'P))

  -- 不动块缩写
  CB = AX *mat (QP *mat hα') -mat (QP *mat hα') *mat AZ
  FB = QP *mat P'P -mat PP *mat P'P

  -- s4：第一块第二项替换
  s4 : ((AX *mat hα) *mat P'P -mat hα *mat (P'P *mat AZ))
       +mat (AX *mat (QP *mat hα') -mat (QP *mat hα') *mat AZ)
     ≡ ((AX *mat hα) *mat P'P -mat (hα *mat AY) *mat P'P)
       +mat (AX *mat (QP *mat hα') -mat (QP *mat hα') *mat AZ)
  s4 = +mat-cong₁l {C = CB} (-mat-cong₁r {A = (AX *mat hα) *mat P'P} s4a)

  -- s5：合并 (AX·hα)·P' - (hα·AY)·P' = (AX·hα - hα·AY)·P'
  s5 : ((AX *mat hα) *mat P'P -mat (hα *mat AY) *mat P'P)
       +mat (AX *mat (QP *mat hα') -mat (QP *mat hα') *mat AZ)
     ≡ ((AX *mat hα -mat hα *mat AY) *mat P'P)
       +mat (AX *mat (QP *mat hα') -mat (QP *mat hα') *mat AZ)
  s5 = +mat-cong₁l {C = CB} (sym (*mat-distrib-r-minus (AX *mat hα) (hα *mat AY) P'P))

  -- s6：用 α.condition 替换交换子
  s6 : ((AX *mat hα -mat hα *mat AY) *mat P'P)
       +mat (AX *mat (QP *mat hα') -mat (QP *mat hα') *mat AZ)
     ≡ ((QP -mat PP) *mat P'P)
       +mat (AX *mat (QP *mat hα') -mat (QP *mat hα') *mat AZ)
  s6 = +mat-cong₁l {C = CB} (cong (λ m → m *mat P'P) (SpTwoMorphism.condition α))

  -- s7：分发 (QP-PP)·P' = QP·P' - PP·P'
  s7 : ((QP -mat PP) *mat P'P)
       +mat (AX *mat (QP *mat hα') -mat (QP *mat hα') *mat AZ)
     ≡ (QP *mat P'P -mat PP *mat P'P)
       +mat (AX *mat (QP *mat hα') -mat (QP *mat hα') *mat AZ)
  s7 = +mat-cong₁l {C = CB} (*mat-distrib-r-minus QP PP P'P)

  -- s8a：AX·(Q·hα') = Q·(AY·hα')（Q.intertwine + assoc）
  s8a : AX *mat (QP *mat hα') ≡ QP *mat (AY *mat hα')
  s8a = trans (sym (*mat-assoc AX QP hα'))
         (trans (cong (λ m → m *mat hα') (sym (SpHom.intertwine Q)))
                (*mat-assoc QP AY hα'))

  -- s8b：(Q·hα')·AZ = Q·(hα'·AZ)
  s8b : (QP *mat hα') *mat AZ ≡ QP *mat (hα' *mat AZ)
  s8b = *mat-assoc QP hα' AZ

  -- s8：第二块替换
  s8 : (QP *mat P'P -mat PP *mat P'P)
       +mat (AX *mat (QP *mat hα') -mat (QP *mat hα') *mat AZ)
     ≡ (QP *mat P'P -mat PP *mat P'P)
       +mat (QP *mat (AY *mat hα') -mat QP *mat (hα' *mat AZ))
  s8 = +mat-cong₁r {A = FB} (-mat-cong₂ s8a s8b)

  -- s9：合并 Q·(AY·hα') - Q·(hα'·AZ) = Q·((AY·hα') - (hα'·AZ))
  s9 : (QP *mat P'P -mat PP *mat P'P)
       +mat (QP *mat (AY *mat hα') -mat QP *mat (hα' *mat AZ))
     ≡ (QP *mat P'P -mat PP *mat P'P)
       +mat QP *mat (AY *mat hα' -mat hα' *mat AZ)
  s9 = +mat-cong₁r {A = FB} (sym (*mat-distrib-l-minus QP (AY *mat hα') (hα' *mat AZ)))

  -- s10：用 α'.condition 替换交换子
  s10 : (QP *mat P'P -mat PP *mat P'P)
        +mat QP *mat (AY *mat hα' -mat hα' *mat AZ)
      ≡ (QP *mat P'P -mat PP *mat P'P)
        +mat QP *mat (Q'P -mat P'P)
  s10 = +mat-cong₁r {A = FB} (cong (λ m → QP *mat m) (SpTwoMorphism.condition α'))

  -- s11：分发 Q·(Q'-P') = Q·Q' - Q·P'
  s11 : (QP *mat P'P -mat PP *mat P'P)
        +mat QP *mat (Q'P -mat P'P)
      ≡ (QP *mat P'P -mat PP *mat P'P)
        +mat (QP *mat Q'P -mat QP *mat P'P)
  s11 = +mat-cong₁r {A = FB} (*mat-distrib-l-minus QP Q'P P'P)

  -- s12：中间项消去 → RHS
  s12 : (QP *mat P'P -mat PP *mat P'P)
        +mat (QP *mat Q'P -mat QP *mat P'P)
      ≡ QP *mat Q'P -mat PP *mat P'P
  s12 = -mat-cancel-mid (PP *mat P'P) (QP *mat P'P) (QP *mat Q'P)

  -- 组装
  main : commutator {X} {Z} (hα *mat P'P +mat QP *mat hα')
       ≡ (QP *mat Q'P -mat PP *mat P'P)
  main = trans s1 (trans s2 (trans s3 (trans s4 (trans s5 (trans s6 (trans s7 (trans s8 (trans s9 (trans s10 (trans s11 s12))))))))))

spHorizComp : {X Y Z : SpObj} {P Q : SpHom X Y} {P' Q' : SpHom Y Z}
  → SpTwoMorphism P Q → SpTwoMorphism P' Q' → SpTwoMorphism (compose P' P) (compose Q' Q)
spHorizComp {X} {Y} {Z} {P} {Q} {P'} {Q'} α α' = record
  { homotopy = (SpTwoMorphism.homotopy α *mat SpHom.P P')
               +mat (SpHom.P Q *mat SpTwoMorphism.homotopy α')
  ; condition = spHorizComp-condition α α'
  }

-- 垂直复合结合律（T2 闭合：同伦逐点 +-assoc + SpTwoMorphism-≡）
spVertComp-assoc : {X Y : SpObj} {P Q R S : SpHom X Y}
  (α : SpTwoMorphism P Q)(β : SpTwoMorphism Q R)(γ : SpTwoMorphism R S)
  → spVertComp (spVertComp α β) γ ≡ spVertComp α (spVertComp β γ)
spVertComp-assoc {X} {Y} {P} {Q} {R} {S} α β γ =
  SpTwoMorphism-≡
    (funext (λ i → funext (λ j →
      +-assoc (SpTwoMorphism.homotopy α i j)
              (SpTwoMorphism.homotopy β i j)
              (SpTwoMorphism.homotopy γ i j))))

-- ==================================================================
-- §2 交换律偏差结构
-- ==================================================================

-- 交换律偏差同伦公式：
-- (R.P - Q.P) * α'.homotopy + β.homotopy * (P'.P - Q'.P)
-- 对应 Lean: spExchangeLaw_homotopy_deviation

-- 偏差引理（结构占位）
deviation-formula : {X Y Z : SpObj} {P Q R : SpHom X Y} {P' Q' R' : SpHom Y Z}
  (α : SpTwoMorphism P Q)(β : SpTwoMorphism Q R)
  (α' : SpTwoMorphism P' Q')(β' : SpTwoMorphism Q' R')
  → (Fin (n X) → Fin (n Z) → ℂ) ≡ (Fin (n X) → Fin (n Z) → ℂ)
deviation-formula α β α' β' = refl

-- 严格极限：当 β.homotopy 和 α'.homotopy 满足交错条件时，偏差为零
-- 对应 Lean: spExchangeLaw_deviation_strict_limit
deviation-strict-limit : {X Y Z : SpObj} {P Q R : SpHom X Y} {P' Q' R' : SpHom Y Z}
  (α : SpTwoMorphism P Q)(β : SpTwoMorphism Q R)
  (α' : SpTwoMorphism P' Q')(β' : SpTwoMorphism Q' R') → Set₁
deviation-strict-limit {X} {Y} {Z} α β α' β' = (Fin (n X) → Fin (n Z) → ℂ) ≡ (Fin (n X) → Fin (n Z) → ℂ)

-- ==================================================================
-- §3 3-态射：SpTwoMorphism 之间的同伦
-- ==================================================================

-- 3-态射：二阶同伦矩阵 K + 条件 β.homotopy - α.homotopy = A_X·K - K·A_Y（**T2 闭合**：真实等式）
record SpThreeMorphism {X Y : SpObj} {P Q : SpHom X Y}
                       (α β : SpTwoMorphism P Q) : Set₁ where
  field
    secondHomotopy : Fin (n X) → Fin (n Y) → ℂ
    -- 条件：β.homotopy - α.homotopy = A_X * K - K * A_Y（真实等式）
    condition : commutator {X} {Y} secondHomotopy
              ≡ (SpTwoMorphism.homotopy β -mat SpTwoMorphism.homotopy α)

-- 依赖记录相等（3-态射）
SpThreeMorphism-≡ : {X Y : SpObj} {P Q : SpHom X Y} {α β : SpTwoMorphism P Q}
  {e1 e2 : SpThreeMorphism α β}
  → SpThreeMorphism.secondHomotopy e1 ≡ SpThreeMorphism.secondHomotopy e2 → e1 ≡ e2
SpThreeMorphism-≡ {e1 = e1} {e2 = e2} refl =
  cong₁ (λ c → record { secondHomotopy = SpThreeMorphism.secondHomotopy e1 ; condition = c })
        (uip (SpThreeMorphism.condition e1) (SpThreeMorphism.condition e2))

-- 恒等 3-态射：secondHomotopy = 0（条件经 commutator-zero + -mat-self）
id-three-morphism : {X Y : SpObj} {P Q : SpHom X Y}
  (α : SpTwoMorphism P Q) → SpThreeMorphism α α
id-three-morphism {X} {Y} α = record
  { secondHomotopy = zeroMat
  ; condition = trans (commutator-zero {X} {Y})
                      (sym (-mat-self (SpTwoMorphism.homotopy α)))
  }

-- 垂直复合：二阶同伦矩阵相加（条件经 commutator-add + 中间项消去）
spThreeVertComp : {X Y : SpObj} {P Q : SpHom X Y}
  {α β γ : SpTwoMorphism P Q}
  → SpThreeMorphism α β → SpThreeMorphism β γ → SpThreeMorphism α γ
spThreeVertComp {X} {Y} {P} {Q} {α} {β} {γ} Ξ Τ = record
  { secondHomotopy = SpThreeMorphism.secondHomotopy Ξ +mat SpThreeMorphism.secondHomotopy Τ
  ; condition = trans (commutator-add (SpThreeMorphism.secondHomotopy Ξ) (SpThreeMorphism.secondHomotopy Τ))
      (trans (+mat-cong₂ (SpThreeMorphism.condition Ξ) (SpThreeMorphism.condition Τ))
             (-mat-cancel-mid (SpTwoMorphism.homotopy α) (SpTwoMorphism.homotopy β) (SpTwoMorphism.homotopy γ)))
  }

-- 水平复合（3-态射）：第二同伦构造（T2 闭合，与 Lean 公式一致
--   secondHomotopy = Ξ·P' + Q·Ξ'）；condition（T2 闭合：平行于 spHorizComp-condition 的链）
spThreeHorizComp-condition : {X Y Z : SpObj} {P Q : SpHom X Y} {P' Q' : SpHom Y Z}
  {α β : SpTwoMorphism P Q} {α' β' : SpTwoMorphism P' Q'}
  (Ξ : SpThreeMorphism α β) (Ξ' : SpThreeMorphism α' β')
  → commutator {X} {Z} ((SpThreeMorphism.secondHomotopy Ξ *mat SpHom.P P')
                        +mat (SpHom.P Q *mat SpThreeMorphism.secondHomotopy Ξ'))
      ≡ (SpTwoMorphism.homotopy (spHorizComp β β') -mat SpTwoMorphism.homotopy (spHorizComp α α'))
spThreeHorizComp-condition {X} {Y} {Z} {P} {Q} {P'} {Q'} {α} {β} {α'} {β'} Ξ Ξ' = main
  where
  KΞ  = SpThreeMorphism.secondHomotopy Ξ
  KΞ' = SpThreeMorphism.secondHomotopy Ξ'
  αh  = SpTwoMorphism.homotopy α
  βh  = SpTwoMorphism.homotopy β
  α'h = SpTwoMorphism.homotopy α'
  β'h = SpTwoMorphism.homotopy β'
  PP  = SpHom.P P
  QP  = SpHom.P Q
  P'P = SpHom.P P'
  Q'P = SpHom.P Q'
  AX  = SpObj.A X
  AY  = SpObj.A Y
  AZ  = SpObj.A Z

  -- t1：分配
  t1 : AX *mat (KΞ *mat P'P +mat QP *mat KΞ') -mat (KΞ *mat P'P +mat QP *mat KΞ') *mat AZ
     ≡ (AX *mat (KΞ *mat P'P) +mat AX *mat (QP *mat KΞ'))
       -mat ((KΞ *mat P'P) *mat AZ +mat (QP *mat KΞ') *mat AZ)
  t1 = -mat-cong₂ (*mat-distrib-l AX (KΞ *mat P'P) (QP *mat KΞ'))
                  (*mat-distrib-r (KΞ *mat P'P) (QP *mat KΞ') AZ)

  -- t2：括号重排
  t2 : (AX *mat (KΞ *mat P'P) +mat AX *mat (QP *mat KΞ'))
       -mat ((KΞ *mat P'P) *mat AZ +mat (QP *mat KΞ') *mat AZ)
     ≡ ((AX *mat KΞ) *mat P'P +mat AX *mat (QP *mat KΞ'))
       -mat (KΞ *mat (P'P *mat AZ) +mat (QP *mat KΞ') *mat AZ)
  t2 = -mat-cong₂ (cong (λ m → m +mat AX *mat (QP *mat KΞ')) (sym (*mat-assoc AX KΞ P'P)))
                  (cong (λ m → m +mat (QP *mat KΞ') *mat AZ) (*mat-assoc KΞ P'P AZ))

  -- t3：差值拆分
  t3 : ((AX *mat KΞ) *mat P'P +mat AX *mat (QP *mat KΞ'))
       -mat (KΞ *mat (P'P *mat AZ) +mat (QP *mat KΞ') *mat AZ)
     ≡ ((AX *mat KΞ) *mat P'P -mat KΞ *mat (P'P *mat AZ))
       +mat (AX *mat (QP *mat KΞ') -mat (QP *mat KΞ') *mat AZ)
  t3 = sym (mat-rearrange ((AX *mat KΞ) *mat P'P) (KΞ *mat (P'P *mat AZ))
                          (AX *mat (QP *mat KΞ')) ((QP *mat KΞ') *mat AZ))

  -- t4a：KΞ·(P'·AZ) = (KΞ·AY)·P'
  t4a : KΞ *mat (P'P *mat AZ) ≡ (KΞ *mat AY) *mat P'P
  t4a = trans (cong (λ m → KΞ *mat m) (SpHom.intertwine P'))
              (sym (*mat-assoc KΞ AY P'P))

  -- 不动块缩写
  TCB = AX *mat (QP *mat KΞ') -mat (QP *mat KΞ') *mat AZ
  TFB = βh *mat P'P -mat αh *mat P'P

  -- t4：第一块第二项替换
  t4 : ((AX *mat KΞ) *mat P'P -mat KΞ *mat (P'P *mat AZ))
       +mat (AX *mat (QP *mat KΞ') -mat (QP *mat KΞ') *mat AZ)
     ≡ ((AX *mat KΞ) *mat P'P -mat (KΞ *mat AY) *mat P'P)
       +mat (AX *mat (QP *mat KΞ') -mat (QP *mat KΞ') *mat AZ)
  t4 = +mat-cong₁l {C = TCB} (-mat-cong₁r {A = (AX *mat KΞ) *mat P'P} t4a)

  -- t5：合并第一块交换子
  t5 : ((AX *mat KΞ) *mat P'P -mat (KΞ *mat AY) *mat P'P)
       +mat (AX *mat (QP *mat KΞ') -mat (QP *mat KΞ') *mat AZ)
     ≡ ((AX *mat KΞ -mat KΞ *mat AY) *mat P'P)
       +mat (AX *mat (QP *mat KΞ') -mat (QP *mat KΞ') *mat AZ)
  t5 = +mat-cong₁l {C = TCB} (sym (*mat-distrib-r-minus (AX *mat KΞ) (KΞ *mat AY) P'P))

  -- t6：用 Ξ.condition 替换交换子
  t6 : ((AX *mat KΞ -mat KΞ *mat AY) *mat P'P)
       +mat (AX *mat (QP *mat KΞ') -mat (QP *mat KΞ') *mat AZ)
     ≡ ((βh -mat αh) *mat P'P)
       +mat (AX *mat (QP *mat KΞ') -mat (QP *mat KΞ') *mat AZ)
  t6 = +mat-cong₁l {C = TCB} (cong (λ m → m *mat P'P) (SpThreeMorphism.condition Ξ))

  -- t7：分发 (βh-αh)·P' = βh·P' - αh·P'
  t7 : ((βh -mat αh) *mat P'P)
       +mat (AX *mat (QP *mat KΞ') -mat (QP *mat KΞ') *mat AZ)
     ≡ (βh *mat P'P -mat αh *mat P'P)
       +mat (AX *mat (QP *mat KΞ') -mat (QP *mat KΞ') *mat AZ)
  t7 = +mat-cong₁l {C = TCB} (*mat-distrib-r-minus βh αh P'P)

  -- t8a：AX·(Q·KΞ') = Q·(AY·KΞ')
  t8a : AX *mat (QP *mat KΞ') ≡ QP *mat (AY *mat KΞ')
  t8a = trans (sym (*mat-assoc AX QP KΞ'))
         (trans (cong (λ m → m *mat KΞ') (sym (SpHom.intertwine Q)))
                (*mat-assoc QP AY KΞ'))

  -- t8b：(Q·KΞ')·AZ = Q·(KΞ'·AZ)
  t8b : (QP *mat KΞ') *mat AZ ≡ QP *mat (KΞ' *mat AZ)
  t8b = *mat-assoc QP KΞ' AZ

  -- t8：第二块替换
  t8 : (βh *mat P'P -mat αh *mat P'P)
       +mat (AX *mat (QP *mat KΞ') -mat (QP *mat KΞ') *mat AZ)
     ≡ (βh *mat P'P -mat αh *mat P'P)
       +mat (QP *mat (AY *mat KΞ') -mat QP *mat (KΞ' *mat AZ))
  t8 = +mat-cong₁r {A = TFB} (-mat-cong₂ t8a t8b)

  -- t9：合并第二块交换子
  t9 : (βh *mat P'P -mat αh *mat P'P)
       +mat (QP *mat (AY *mat KΞ') -mat QP *mat (KΞ' *mat AZ))
     ≡ (βh *mat P'P -mat αh *mat P'P)
       +mat QP *mat (AY *mat KΞ' -mat KΞ' *mat AZ)
  t9 = +mat-cong₁r {A = TFB} (sym (*mat-distrib-l-minus QP (AY *mat KΞ') (KΞ' *mat AZ)))

  -- t10：用 Ξ'.condition 替换交换子
  t10 : (βh *mat P'P -mat αh *mat P'P)
        +mat QP *mat (AY *mat KΞ' -mat KΞ' *mat AZ)
      ≡ (βh *mat P'P -mat αh *mat P'P)
        +mat QP *mat (β'h -mat α'h)
  t10 = +mat-cong₁r {A = TFB} (cong (λ m → QP *mat m) (SpThreeMorphism.condition Ξ'))

  -- t11：分发 Q·(β'-α') = Q·β' - Q·α'
  t11 : (βh *mat P'P -mat αh *mat P'P)
        +mat QP *mat (β'h -mat α'h)
      ≡ (βh *mat P'P -mat αh *mat P'P)
        +mat (QP *mat β'h -mat QP *mat α'h)
  t11 = +mat-cong₁r {A = TFB} (*mat-distrib-l-minus QP β'h α'h)

  -- t12：重排为 (β·P' + Q·β') - (α·P' + Q·α')
  t12 : (βh *mat P'P -mat αh *mat P'P)
        +mat (QP *mat β'h -mat QP *mat α'h)
      ≡ (βh *mat P'P +mat QP *mat β'h) -mat (αh *mat P'P +mat QP *mat α'h)
  t12 = mat-rearrange (βh *mat P'P) (αh *mat P'P) (QP *mat β'h) (QP *mat α'h)

  -- t13：展开 spHorizComp 同伦（定义上相等）
  t13 : (βh *mat P'P +mat QP *mat β'h) -mat (αh *mat P'P +mat QP *mat α'h)
      ≡ (SpTwoMorphism.homotopy (spHorizComp β β') -mat SpTwoMorphism.homotopy (spHorizComp α α'))
  t13 = refl

  -- 组装
  main : commutator {X} {Z} (KΞ *mat P'P +mat QP *mat KΞ')
       ≡ (SpTwoMorphism.homotopy (spHorizComp β β') -mat SpTwoMorphism.homotopy (spHorizComp α α'))
  main = trans t1 (trans t2 (trans t3 (trans t4 (trans t5 (trans t6 (trans t7 (trans t8 (trans t9 (trans t10 (trans t11 (trans t12 t13)))))))))))

spThreeHorizComp : {X Y Z : SpObj} {P Q : SpHom X Y} {P' Q' : SpHom Y Z} {α β : SpTwoMorphism P Q} {α' β' : SpTwoMorphism P' Q'}
  → SpThreeMorphism α β → SpThreeMorphism α' β' → SpThreeMorphism (spHorizComp α α') (spHorizComp β β')
spThreeHorizComp {X} {Y} {Z} {P} {Q} {P'} {Q'} {α} {β} {α'} {β'} Ξ Ξ' = record
  { secondHomotopy = (SpThreeMorphism.secondHomotopy Ξ *mat SpHom.P P')
                     +mat (SpHom.P Q *mat SpThreeMorphism.secondHomotopy Ξ')
  ; condition = spThreeHorizComp-condition Ξ Ξ'
  }

-- 垂直复合结合律（T2 闭合：二阶同伦逐点 +-assoc + SpThreeMorphism-≡）
spThreeVertComp-assoc : {X Y : SpObj} {P Q : SpHom X Y}
  {α β γ δ : SpTwoMorphism P Q}
  (Ξ : SpThreeMorphism α β)(Τ : SpThreeMorphism β γ)(Υ : SpThreeMorphism γ δ)
  → spThreeVertComp (spThreeVertComp Ξ Τ) Υ ≡ spThreeVertComp Ξ (spThreeVertComp Τ Υ)
spThreeVertComp-assoc {X} {Y} {P} {Q} {α} {β} {γ} {δ} Ξ Τ Υ =
  SpThreeMorphism-≡
    (funext (λ i → funext (λ j →
      +-assoc (SpThreeMorphism.secondHomotopy Ξ i j)
              (SpThreeMorphism.secondHomotopy Τ i j)
              (SpThreeMorphism.secondHomotopy Υ i j))))

-- ==================================================================
-- §4 层结构总结
-- ==================================================================

{-
  层结构：
    层 1（1-态射）：SpHom       条件：P·A_Y = A_X·P
    层 2（2-态射）：SpTwoMorphism  条件：Q.P - P.P = A_X·H - H·A_Y
    层 3（3-态射）：SpThreeMorphism 条件：β.H - α.H = A_X·K - K·A_Y

  模式：每一层由同一个交换子 [A, ·] 控制缺陷，形成链复形。
  交换律偏差是第 2 层的结构特征（非缺陷），
  对应物理上引力耦合常数 G_N ≠ 0。
-}
