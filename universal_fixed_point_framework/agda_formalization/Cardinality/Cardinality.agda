module Cardinality.Cardinality where

{-
  P4: 基数反例形式化（2026-07-31）
  ================================
  对应笔记: notes/00_foundations/spectral_representation_silence.md §2/§4

  目标: 在 Agda 中形式化 SpImD 态射层结构性不可闭合的基数反例：
    2 状态平凡系统下 Hom_Sp(D(X),D(Y)) = ℂ⁴（不可数）vs Hom_Rec(X,Y) = 4（有限）。

  有限载体 ℤ/3（ℂ = c0/c1/c2）下不可数性不可表达，形式化其有限核心：
  1. **D 不 full**（决定性反例）：P = [[1,0],[1,1]] 是合法谱态射
     （满足交织条件），但非任何转移矩阵的像——D 的 full 性为假。
  2. **Hom_Rec 恰有 4 个元素**：Fin 2 → Fin 2 的 4 个函数枚举。
  3. **Hom_Sp 至少 5 个互异元素**：4 个转移矩阵（transferMatrix-inj）+ P，
     故 Hom_Sp 基数 > Hom_Rec 基数，无双射（伴随自然同构不成立）。

  不含 postulate（除 SpCategory 基础公理 funext）。
-}

open import Agda.Builtin.Equality using (_≡_; refl)
open import Agda.Builtin.Bool using (Bool; true; false)
open import Sp.SpCategory
open import Rec.RecCategory
open import DecursionFunctor.DecursionFunctor

-- 本地析取类型（SpCategory 不导出 _⊎_）
infixr 20 _∨_
data _∨_ (A B : Set) : Set where
  inj₁ : A → A ∨ B
  inj₂ : B → A ∨ B

-- 本地否定（SpCategory 不导出 ¬）
¬_ : Set → Set
¬ A = A → ⊥

-- ==================================================================
-- §1 平凡 2 状态系统
-- ==================================================================

-- Fin 2 的简写与两个元素
F2 : Set
F2 = Fin 2

z2 : F2
z2 = zero

o2 : F2
o2 = suc zero

-- z2 与 o2 互异（构造子不相交）
z2≢o2 : z2 ≢ o2
z2≢o2 ()

-- 平凡 2 状态递归系统：step = id
trivial2 : RecObj
trivial2 = record { n = 2 ; step = λ x → x }

-- D(trivial2) 的算子 A = transferMatrix id = 𝟙-matrix（逐点 refl）
transferMatrix-id : transferMatrix {2} {2} (λ x → x) ≡ 𝟙-matrix {2}
transferMatrix-id = funext (λ i → funext (λ j → refl))

-- ==================================================================
-- §2 反例态射 P = [[1,0],[1,1]]
-- ==================================================================

-- P 矩阵：第一行 (1,0)，第二行 (1,1)（"每行恰一个 1" 违反）
P : F2 → F2 → ℂ
P zero    zero    = c1
P zero    (suc j) = c0
P (suc i) zero    = c1
P (suc i) (suc j) = c1

-- P 的两处关键值（第二行两个 1）
P-o2-z2 : P o2 z2 ≡ c1
P-o2-z2 = refl

P-o2-o2 : P o2 o2 ≡ c1
P-o2-o2 = refl

-- 交织条件：P * A = A * P（A = transferMatrix id ≡ 𝟙，经矩阵单位律）
P-intertwine : P *mat SpObj.A (D-obj trivial2) ≡ SpObj.A (D-obj trivial2) *mat P
P-intertwine =
  trans (cong (λ m → P *mat m) (sym transferMatrix-id))
  (trans (*mat-id-r P)
  (trans (sym (*mat-id-l P))
         (cong (λ m → m *mat P) transferMatrix-id)))

-- **P 是合法谱态射**：Hom_Sp(D(X),D(X)) 的元素
P-spectral : SpHom (D-obj trivial2) (D-obj trivial2)
P-spectral = record { P = P ; intertwine = P-intertwine }

-- **D 不 full（决定性反例）**：P 不是任何转移矩阵的像
-- 转移矩阵每行恰有一个 c1（Fin-eq? 恰一 true），P 第二行有两个 c1。
transferMatrix-not-P : (f : F2 → F2) → transferMatrix f ≢ P
transferMatrix-not-P f h = z2≢o2 (trans (sym e1) e2)
  where
  -- h 在第二行两个位置的应用
  h1 : transferMatrix f o2 z2 ≡ c1
  h1 = trans (cong-app (cong-app h o2) z2) P-o2-z2
  h2 : transferMatrix f o2 o2 ≡ c1
  h2 = trans (cong-app (cong-app h o2) o2) P-o2-o2
  -- 两处均须为 true ⇒ f o2 ≡ z2 且 f o2 ≡ o2
  e1 : f o2 ≡ z2
  e1 = Fin-eq?-true (f o2) z2 (if-c1 (Fin-eq? (f o2) z2) h1)
  e2 : f o2 ≡ o2
  e2 = Fin-eq?-true (f o2) o2 (if-c1 (Fin-eq? (f o2) o2) h2)

-- **D 不 full**：P 不在 D 的像中（无 f 使 transferMatrix f = P）
D-not-full : (f : F2 → F2) → ¬ (transferMatrix f ≡ P)
D-not-full f = transferMatrix-not-P f

-- ==================================================================
-- §3 Hom_Rec(X,X) 恰有 4 个元素
-- ==================================================================

-- Fin 2 → Fin 2 的 4 个函数
f-const-z : F2 → F2
f-const-z _ = z2

f-id : F2 → F2
f-id x = x

f-const-o : F2 → F2
f-const-o _ = o2

f-swap : F2 → F2
f-swap zero    = o2
f-swap (suc x) = z2

-- 任意函数逐点落入 2 值（Fin 2 恰有 zero 与 suc zero 两元素）
fun2-value : (g : F2 → F2) (x : F2) → (g x ≡ z2) ∨ (g x ≡ o2)
fun2-value g zero      with g zero
fun2-value g zero      | zero      = inj₁ refl
fun2-value g zero      | suc zero  = inj₂ refl
fun2-value g (suc zero) with g (suc zero)
fun2-value g (suc zero) | zero      = inj₁ refl
fun2-value g (suc zero) | suc zero  = inj₂ refl

-- 任意函数等于 4 个之一（funext）
fun2-card : (g : F2 → F2) → (g ≡ f-const-z) ∨ (g ≡ f-id) ∨ (g ≡ f-const-o) ∨ (g ≡ f-swap)
fun2-card g with fun2-value g z2 | fun2-value g o2
fun2-card g | inj₁ gz | inj₁ go =
  inj₁ (funext (λ { zero → gz ; (suc zero) → go }))
fun2-card g | inj₁ gz | inj₂ go =
  inj₂ (inj₁ (funext (λ { zero → gz ; (suc zero) → go })))
fun2-card g | inj₂ gz | inj₁ go =
  inj₂ (inj₂ (inj₂ (funext (λ { zero → gz ; (suc zero) → go }))))
fun2-card g | inj₂ gz | inj₂ go =
  inj₂ (inj₂ (inj₁ (funext (λ { zero → gz ; (suc zero) → go }))))

-- **Hom_Rec 至多 4 元素**：平凡系统 comm 平凡，RecHom 的 toFun 落入 4 函数集
rec-hom-card : (g : RecHom trivial2 trivial2)
  → (RecHom.toFun g ≡ f-const-z) ∨ (RecHom.toFun g ≡ f-id)
  ∨ (RecHom.toFun g ≡ f-const-o) ∨ (RecHom.toFun g ≡ f-swap)
rec-hom-card g = fun2-card (RecHom.toFun g)

-- ==================================================================
-- §4 结论：Hom_Sp 至少 5 个互异元素（无双射）
-- ==================================================================

-- 4 个转移矩阵两两互异（transferMatrix-inj + 函数互异）
tm-const-z : F2 → F2 → ℂ
tm-const-z = transferMatrix f-const-z

tm-id : F2 → F2 → ℂ
tm-id = transferMatrix f-id

tm-const-o : F2 → F2 → ℂ
tm-const-o = transferMatrix f-const-o

tm-swap : F2 → F2 → ℂ
tm-swap = transferMatrix f-swap

-- 辅助：函数互异 ⇒ 转移矩阵互异（逐点取反）
tm-ne : {g h : F2 → F2} → (g ≢ h) → transferMatrix g ≢ transferMatrix h
tm-ne g≢h tm-eq = g≢h (transferMatrix-inj tm-eq)

-- 4 个函数互异（在关键点上值不同）
f-const-z≢f-id : f-const-z ≢ f-id
f-const-z≢f-id e = z2≢o2 (trans (cong-app e o2) refl)

f-const-z≢f-const-o : f-const-z ≢ f-const-o
f-const-z≢f-const-o e = z2≢o2 (cong-app e z2)

f-const-z≢f-swap : f-const-z ≢ f-swap
f-const-z≢f-swap e = z2≢o2 (cong-app e z2)

f-id≢f-const-o : f-id ≢ f-const-o
f-id≢f-const-o e = z2≢o2 (cong-app e z2)

f-id≢f-swap : f-id ≢ f-swap
f-id≢f-swap e = z2≢o2 (cong-app e z2)

f-const-o≢f-swap : f-const-o ≢ f-swap
f-const-o≢f-swap e = z2≢o2 (sym (cong-app e o2))

-- 4 个转移矩阵两两互异
transfers-distinct :
  (tm-const-z ≢ tm-id) × (tm-const-z ≢ tm-const-o) × (tm-const-z ≢ tm-swap)
  × (tm-id ≢ tm-const-o) × (tm-id ≢ tm-swap) × (tm-const-o ≢ tm-swap)
transfers-distinct =
  tm-ne f-const-z≢f-id , tm-ne f-const-z≢f-const-o , tm-ne f-const-z≢f-swap ,
  tm-ne f-id≢f-const-o , tm-ne f-id≢f-swap , tm-ne f-const-o≢f-swap

-- **P 与全部转移矩阵互异**（P 非转移矩阵 + 转移矩阵互异）
P-distinct-transfers : (tm-const-z ≢ P) × (tm-id ≢ P) × (tm-const-o ≢ P) × (tm-swap ≢ P)
P-distinct-transfers =
  transferMatrix-not-P f-const-z , transferMatrix-not-P f-id ,
  transferMatrix-not-P f-const-o , transferMatrix-not-P f-swap

-- ==================================================================
-- §5 无双射：Hom_Rec 恰 4 个 + 鸽笼（对应 Lean §8 no_bijection）
-- ==================================================================
-- 目标：证明不存在 Hom_Sp(D X, D X) 与 RecHom X X 之间的双射。
-- 策略（对应 Lean no_bijection_homSp_homRec 的有限版本）：
--   1. Hom_Rec 恰有 4 个互异元素（fun2-card 枚举 + RecHom-≡）
--   2. Hom_Sp 至少有 5 个互异元素（4 转移矩阵态射 + P-spectral）
--   3. 鸽笼：5 个互异元素入 4 个互异元素 ⇒ 双射不存在

-- 4 个函数两两互异（已证 f-const-z≢f-id 等）⟹ F2→F2 恰有 4 个互异元素。
-- **鸽笼（5→4）**：5 个互异 F2→F2 函数不可能。
-- 实现：对 g0 用 fun2-card 分类（4 分支），每分支逐步排除，
--   第 k 个函数必须避开前 k-1 个已确定类别，第 5 个无类可归。

-- 辅助：g ≠ fz, fi, fo, fs 全部 ⇒ 矛盾（fun2-card 分类后各分支被排除）
fun2-excl-all : (g : F2 → F2) → g ≢ f-const-z → g ≢ f-id → g ≢ f-const-o → g ≢ f-swap → ⊥
fun2-excl-all g hz hi ho hs with fun2-card g
fun2-excl-all g hz hi ho hs | inj₁ gz         = hz gz
fun2-excl-all g hz hi ho hs | inj₂ (inj₁ gi)  = hi gi
fun2-excl-all g hz hi ho hs | inj₂ (inj₂ (inj₁ go)) = ho go
fun2-excl-all g hz hi ho hs | inj₂ (inj₂ (inj₂ gs)) = hs gs

-- 分类：g 落入 4 个函数之一（fun2-card 的返回类型）
分类 : (F2 → F2) → Set
分类 g = (g ≡ f-const-z) ∨ (g ≡ f-id) ∨ (g ≡ f-const-o) ∨ (g ≡ f-swap)

-- **鸽笼（5→4）**：5 个互异 F2→F2 函数不可能。
-- 结构：g0 分类 → 每分支内 where mutual 定义排除树（捕获 g0 相等 + n0i 前提）。
fun2-no-5 : (g0 g1 g2 g3 g4 : F2 → F2)
  → g0 ≢ g1 → g0 ≢ g2 → g0 ≢ g3 → g0 ≢ g4
  → g1 ≢ g2 → g1 ≢ g3 → g1 ≢ g4
  → g2 ≢ g3 → g2 ≢ g4 → g3 ≢ g4 → ⊥
-- g0 = f-const-z
fun2-no-5 g0 g1 g2 g3 g4 n01 n02 n03 n04 n12 n13 n14 n23 n24 n34 with fun2-card g0
fun2-no-5 g0 g1 g2 g3 g4 n01 n02 n03 n04 n12 n13 n14 n23 n24 n34 | inj₁ g0z =
  s1 (fun2-card g1) (fun2-card g2) (fun2-card g3) (fun2-card g4)
  where
  mutual
    h1z : g1 ≢ f-const-z
    h1z p = n01 (trans g0z (sym p))
    h2z : g2 ≢ f-const-z
    h2z p = n02 (trans g0z (sym p))
    h3z : g3 ≢ f-const-z
    h3z p = n03 (trans g0z (sym p))
    h4z : g4 ≢ f-const-z
    h4z p = n04 (trans g0z (sym p))
    -- 第 1 层：g1 ∈ {fi, fo, fs}（分类 c1）
    s1 : (q1 : 分类 g1) (q2 : 分类 g2) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s1 (inj₁ c1z) _ _ _ = h1z c1z
    s1 (inj₂ (inj₁ c1i)) q2 q3 q4 = s2i c1i q2 q3 q4
    s1 (inj₂ (inj₂ (inj₁ c1o))) q2 q3 q4 = s2o c1o q2 q3 q4
    s1 (inj₂ (inj₂ (inj₂ c1s))) q2 q3 q4 = s2s c1s q2 q3 q4
    -- 第 2 层（g1 = f-id）：g2..g4 ≠ fz, fi
    s2i : (c1i : g1 ≡ f-id) (q2 : 分类 g2) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s2i c1i (inj₁ c2z) _ _ = h2z c2z
    s2i c1i (inj₂ (inj₁ c2i)) _ _ = n12 (trans c1i (sym c2i))
    s2i c1i (inj₂ (inj₂ (inj₁ c2o))) q3 q4 = s3io c1i c2o q3 q4
    s2i c1i (inj₂ (inj₂ (inj₂ c2s))) q3 q4 = s3is c1i c2s q3 q4
    -- 第 3 层（g1 = fi, g2 = fo）：g3..g4 ≠ fz, fi, fo
    s3io : (c1i : g1 ≡ f-id) (c2o : g2 ≡ f-const-o) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s3io c1i c2o (inj₁ c3z) _ = h3z c3z
    s3io c1i c2o (inj₂ (inj₁ c3i)) _ = n13 (trans c1i (sym c3i))
    s3io c1i c2o (inj₂ (inj₂ (inj₁ c3o))) _ = n23 (trans c2o (sym c3o))
    s3io c1i c2o (inj₂ (inj₂ (inj₂ c3s))) q4 =
      fun2-excl-all g4 h4z (λ p → n14 (trans c1i (sym p))) (λ p → n24 (trans c2o (sym p))) (λ p → n34 (trans c3s (sym p)))
    -- 第 3 层（g1 = fi, g2 = fs）：g3..g4 ≠ fz, fi, fs
    s3is : (c1i : g1 ≡ f-id) (c2s : g2 ≡ f-swap) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s3is c1i c2s (inj₁ c3z) _ = h3z c3z
    s3is c1i c2s (inj₂ (inj₁ c3i)) _ = n13 (trans c1i (sym c3i))
    s3is c1i c2s (inj₂ (inj₂ (inj₁ c3o))) q4 =
      fun2-excl-all g4 h4z (λ p → n14 (trans c1i (sym p))) (λ p → n34 (trans c3o (sym p))) (λ p → n24 (trans c2s (sym p)))
    s3is c1i c2s (inj₂ (inj₂ (inj₂ c3s))) _ = n23 (trans c2s (sym c3s))
    -- 第 2 层（g1 = f-const-o）：g2..g4 ≠ fz, fo
    s2o : (c1o : g1 ≡ f-const-o) (q2 : 分类 g2) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s2o c1o (inj₁ c2z) _ _ = h2z c2z
    s2o c1o (inj₂ (inj₁ c2i)) q3 q4 = s3oi c1o c2i q3 q4
    s2o c1o (inj₂ (inj₂ (inj₁ c2o))) _ _ = n12 (trans c1o (sym c2o))
    s2o c1o (inj₂ (inj₂ (inj₂ c2s))) q3 q4 = s3os c1o c2s q3 q4
    -- 第 3 层（g1 = fo, g2 = fi）：g3..g4 ≠ fz, fo, fi
    s3oi : (c1o : g1 ≡ f-const-o) (c2i : g2 ≡ f-id) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s3oi c1o c2i (inj₁ c3z) _ = h3z c3z
    s3oi c1o c2i (inj₂ (inj₁ c3i)) _ = n23 (trans c2i (sym c3i))
    s3oi c1o c2i (inj₂ (inj₂ (inj₁ c3o))) _ = n13 (trans c1o (sym c3o))
    s3oi c1o c2i (inj₂ (inj₂ (inj₂ c3s))) q4 =
      fun2-excl-all g4 h4z (λ p → n24 (trans c2i (sym p))) (λ p → n14 (trans c1o (sym p))) (λ p → n34 (trans c3s (sym p)))
    -- 第 3 层（g1 = fo, g2 = fs）：g3..g4 ≠ fz, fo, fs
    s3os : (c1o : g1 ≡ f-const-o) (c2s : g2 ≡ f-swap) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s3os c1o c2s (inj₁ c3z) _ = h3z c3z
    s3os c1o c2s (inj₂ (inj₁ c3i)) q4 =
      fun2-excl-all g4 h4z (λ p → n34 (trans c3i (sym p))) (λ p → n14 (trans c1o (sym p))) (λ p → n24 (trans c2s (sym p)))
    s3os c1o c2s (inj₂ (inj₂ (inj₁ c3o))) _ = n13 (trans c1o (sym c3o))
    s3os c1o c2s (inj₂ (inj₂ (inj₂ c3s))) _ = n23 (trans c2s (sym c3s))
    -- 第 2 层（g1 = f-swap）：g2..g4 ≠ fz, fs
    s2s : (c1s : g1 ≡ f-swap) (q2 : 分类 g2) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s2s c1s (inj₁ c2z) _ _ = h2z c2z
    s2s c1s (inj₂ (inj₁ c2i)) q3 q4 = s3si c1s c2i q3 q4
    s2s c1s (inj₂ (inj₂ (inj₁ c2o))) q3 q4 = s3so c1s c2o q3 q4
    s2s c1s (inj₂ (inj₂ (inj₂ c2s))) _ _ = n12 (trans c1s (sym c2s))
    -- 第 3 层（g1 = fs, g2 = fi）：g3..g4 ≠ fz, fs, fi
    s3si : (c1s : g1 ≡ f-swap) (c2i : g2 ≡ f-id) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s3si c1s c2i (inj₁ c3z) _ = h3z c3z
    s3si c1s c2i (inj₂ (inj₁ c3i)) _ = n23 (trans c2i (sym c3i))
    s3si c1s c2i (inj₂ (inj₂ (inj₁ c3o))) q4 =
      fun2-excl-all g4 h4z (λ p → n24 (trans c2i (sym p))) (λ p → n34 (trans c3o (sym p))) (λ p → n14 (trans c1s (sym p)))
    s3si c1s c2i (inj₂ (inj₂ (inj₂ c3s))) _ = n13 (trans c1s (sym c3s))
    -- 第 3 层（g1 = fs, g2 = fo）：g3..g4 ≠ fz, fs, fo
    s3so : (c1s : g1 ≡ f-swap) (c2o : g2 ≡ f-const-o) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s3so c1s c2o (inj₁ c3z) _ = h3z c3z
    s3so c1s c2o (inj₂ (inj₁ c3i)) q4 =
      fun2-excl-all g4 h4z (λ p → n34 (trans c3i (sym p))) (λ p → n24 (trans c2o (sym p))) (λ p → n14 (trans c1s (sym p)))
    s3so c1s c2o (inj₂ (inj₂ (inj₁ c3o))) _ = n23 (trans c2o (sym c3o))
    s3so c1s c2o (inj₂ (inj₂ (inj₂ c3s))) _ = n13 (trans c1s (sym c3s))
-- g0 = f-id
fun2-no-5 g0 g1 g2 g3 g4 n01 n02 n03 n04 n12 n13 n14 n23 n24 n34 | inj₂ (inj₁ g0i) =
  s1 (fun2-card g1) (fun2-card g2) (fun2-card g3) (fun2-card g4)
  where
  mutual
    h1i : g1 ≢ f-id
    h1i p = n01 (trans g0i (sym p))
    h2i : g2 ≢ f-id
    h2i p = n02 (trans g0i (sym p))
    h3i : g3 ≢ f-id
    h3i p = n03 (trans g0i (sym p))
    h4i : g4 ≢ f-id
    h4i p = n04 (trans g0i (sym p))
    s1 : (q1 : 分类 g1) (q2 : 分类 g2) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s1 (inj₁ c1z) q2 q3 q4 = s2z c1z q2 q3 q4
    s1 (inj₂ (inj₁ c1i)) _ _ _ = h1i c1i
    s1 (inj₂ (inj₂ (inj₁ c1o))) q2 q3 q4 = s2o c1o q2 q3 q4
    s1 (inj₂ (inj₂ (inj₂ c1s))) q2 q3 q4 = s2s c1s q2 q3 q4
    -- 第 2 层（g1 = f-const-z）：g2..g4 ≠ fi, fz
    s2z : (c1z : g1 ≡ f-const-z) (q2 : 分类 g2) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s2z c1z (inj₁ c2z) _ _ = n12 (trans c1z (sym c2z))
    s2z c1z (inj₂ (inj₁ c2i)) _ _ = h2i c2i
    s2z c1z (inj₂ (inj₂ (inj₁ c2o))) q3 q4 = s3zo c1z c2o q3 q4
    s2z c1z (inj₂ (inj₂ (inj₂ c2s))) q3 q4 = s3zs c1z c2s q3 q4
    s3zo : (c1z : g1 ≡ f-const-z) (c2o : g2 ≡ f-const-o) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s3zo c1z c2o (inj₁ c3z) _ = n13 (trans c1z (sym c3z))
    s3zo c1z c2o (inj₂ (inj₁ c3i)) _ = h3i c3i
    s3zo c1z c2o (inj₂ (inj₂ (inj₁ c3o))) _ = n23 (trans c2o (sym c3o))
    s3zo c1z c2o (inj₂ (inj₂ (inj₂ c3s))) q4 =
      fun2-excl-all g4 (λ p → n14 (trans c1z (sym p))) h4i (λ p → n24 (trans c2o (sym p))) (λ p → n34 (trans c3s (sym p)))
    s3zs : (c1z : g1 ≡ f-const-z) (c2s : g2 ≡ f-swap) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s3zs c1z c2s (inj₁ c3z) _ = n13 (trans c1z (sym c3z))
    s3zs c1z c2s (inj₂ (inj₁ c3i)) _ = h3i c3i
    s3zs c1z c2s (inj₂ (inj₂ (inj₁ c3o))) q4 =
      fun2-excl-all g4 (λ p → n14 (trans c1z (sym p))) h4i (λ p → n34 (trans c3o (sym p))) (λ p → n24 (trans c2s (sym p)))
    s3zs c1z c2s (inj₂ (inj₂ (inj₂ c3s))) _ = n23 (trans c2s (sym c3s))
    -- 第 2 层（g1 = f-const-o）：g2..g4 ≠ fi, fo
    s2o : (c1o : g1 ≡ f-const-o) (q2 : 分类 g2) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s2o c1o (inj₁ c2z) q3 q4 = s3oz c1o c2z q3 q4
    s2o c1o (inj₂ (inj₁ c2i)) _ _ = h2i c2i
    s2o c1o (inj₂ (inj₂ (inj₁ c2o))) _ _ = n12 (trans c1o (sym c2o))
    s2o c1o (inj₂ (inj₂ (inj₂ c2s))) q3 q4 = s3os c1o c2s q3 q4
    s3oz : (c1o : g1 ≡ f-const-o) (c2z : g2 ≡ f-const-z) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s3oz c1o c2z (inj₁ c3z) _ = n23 (trans c2z (sym c3z))
    s3oz c1o c2z (inj₂ (inj₁ c3i)) _ = h3i c3i
    s3oz c1o c2z (inj₂ (inj₂ (inj₁ c3o))) _ = n13 (trans c1o (sym c3o))
    s3oz c1o c2z (inj₂ (inj₂ (inj₂ c3s))) q4 =
      fun2-excl-all g4 (λ p → n24 (trans c2z (sym p))) h4i (λ p → n14 (trans c1o (sym p))) (λ p → n34 (trans c3s (sym p)))
    s3os : (c1o : g1 ≡ f-const-o) (c2s : g2 ≡ f-swap) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s3os c1o c2s (inj₁ c3z) q4 =
      fun2-excl-all g4 (λ p → n34 (trans c3z (sym p))) h4i (λ p → n14 (trans c1o (sym p))) (λ p → n24 (trans c2s (sym p)))
    s3os c1o c2s (inj₂ (inj₁ c3i)) _ = h3i c3i
    s3os c1o c2s (inj₂ (inj₂ (inj₁ c3o))) _ = n13 (trans c1o (sym c3o))
    s3os c1o c2s (inj₂ (inj₂ (inj₂ c3s))) _ = n23 (trans c2s (sym c3s))
    -- 第 2 层（g1 = f-swap）：g2..g4 ≠ fi, fs
    s2s : (c1s : g1 ≡ f-swap) (q2 : 分类 g2) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s2s c1s (inj₁ c2z) q3 q4 = s3sz c1s c2z q3 q4
    s2s c1s (inj₂ (inj₁ c2i)) _ _ = h2i c2i
    s2s c1s (inj₂ (inj₂ (inj₁ c2o))) q3 q4 = s3so c1s c2o q3 q4
    s2s c1s (inj₂ (inj₂ (inj₂ c2s))) _ _ = n12 (trans c1s (sym c2s))
    s3sz : (c1s : g1 ≡ f-swap) (c2z : g2 ≡ f-const-z) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s3sz c1s c2z (inj₁ c3z) _ = n23 (trans c2z (sym c3z))
    s3sz c1s c2z (inj₂ (inj₁ c3i)) _ = h3i c3i
    s3sz c1s c2z (inj₂ (inj₂ (inj₁ c3o))) q4 =
      fun2-excl-all g4 (λ p → n24 (trans c2z (sym p))) h4i (λ p → n34 (trans c3o (sym p))) (λ p → n14 (trans c1s (sym p)))
    s3sz c1s c2z (inj₂ (inj₂ (inj₂ c3s))) _ = n13 (trans c1s (sym c3s))
    s3so : (c1s : g1 ≡ f-swap) (c2o : g2 ≡ f-const-o) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s3so c1s c2o (inj₁ c3z) q4 =
      fun2-excl-all g4 (λ p → n34 (trans c3z (sym p))) h4i (λ p → n24 (trans c2o (sym p))) (λ p → n14 (trans c1s (sym p)))
    s3so c1s c2o (inj₂ (inj₁ c3i)) _ = h3i c3i
    s3so c1s c2o (inj₂ (inj₂ (inj₁ c3o))) _ = n23 (trans c2o (sym c3o))
    s3so c1s c2o (inj₂ (inj₂ (inj₂ c3s))) _ = n13 (trans c1s (sym c3s))
-- g0 = f-const-o
fun2-no-5 g0 g1 g2 g3 g4 n01 n02 n03 n04 n12 n13 n14 n23 n24 n34 | inj₂ (inj₂ (inj₁ g0o)) =
  s1 (fun2-card g1) (fun2-card g2) (fun2-card g3) (fun2-card g4)
  where
  mutual
    h1o : g1 ≢ f-const-o
    h1o p = n01 (trans g0o (sym p))
    h2o : g2 ≢ f-const-o
    h2o p = n02 (trans g0o (sym p))
    h3o : g3 ≢ f-const-o
    h3o p = n03 (trans g0o (sym p))
    h4o : g4 ≢ f-const-o
    h4o p = n04 (trans g0o (sym p))
    s1 : (q1 : 分类 g1) (q2 : 分类 g2) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s1 (inj₁ c1z) q2 q3 q4 = s2z c1z q2 q3 q4
    s1 (inj₂ (inj₁ c1i)) q2 q3 q4 = s2i c1i q2 q3 q4
    s1 (inj₂ (inj₂ (inj₁ c1o))) _ _ _ = h1o c1o
    s1 (inj₂ (inj₂ (inj₂ c1s))) q2 q3 q4 = s2s c1s q2 q3 q4
    -- 第 2 层（g1 = f-const-z）：g2..g4 ≠ fo, fz
    s2z : (c1z : g1 ≡ f-const-z) (q2 : 分类 g2) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s2z c1z (inj₁ c2z) _ _ = n12 (trans c1z (sym c2z))
    s2z c1z (inj₂ (inj₁ c2i)) q3 q4 = s3zi c1z c2i q3 q4
    s2z c1z (inj₂ (inj₂ (inj₁ c2o))) _ _ = h2o c2o
    s2z c1z (inj₂ (inj₂ (inj₂ c2s))) q3 q4 = s3zs c1z c2s q3 q4
    s3zi : (c1z : g1 ≡ f-const-z) (c2i : g2 ≡ f-id) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s3zi c1z c2i (inj₁ c3z) _ = n13 (trans c1z (sym c3z))
    s3zi c1z c2i (inj₂ (inj₁ c3i)) _ = n23 (trans c2i (sym c3i))
    s3zi c1z c2i (inj₂ (inj₂ (inj₁ c3o))) _ = h3o c3o
    s3zi c1z c2i (inj₂ (inj₂ (inj₂ c3s))) q4 =
      fun2-excl-all g4 (λ p → n14 (trans c1z (sym p))) (λ p → n24 (trans c2i (sym p))) h4o (λ p → n34 (trans c3s (sym p)))
    s3zs : (c1z : g1 ≡ f-const-z) (c2s : g2 ≡ f-swap) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s3zs c1z c2s (inj₁ c3z) _ = n13 (trans c1z (sym c3z))
    s3zs c1z c2s (inj₂ (inj₁ c3i)) q4 =
      fun2-excl-all g4 (λ p → n14 (trans c1z (sym p))) (λ p → n34 (trans c3i (sym p))) h4o (λ p → n24 (trans c2s (sym p)))
    s3zs c1z c2s (inj₂ (inj₂ (inj₁ c3o))) _ = h3o c3o
    s3zs c1z c2s (inj₂ (inj₂ (inj₂ c3s))) _ = n23 (trans c2s (sym c3s))
    -- 第 2 层（g1 = f-id）：g2..g4 ≠ fo, fi
    s2i : (c1i : g1 ≡ f-id) (q2 : 分类 g2) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s2i c1i (inj₁ c2z) q3 q4 = s3iz c1i c2z q3 q4
    s2i c1i (inj₂ (inj₁ c2i)) _ _ = n12 (trans c1i (sym c2i))
    s2i c1i (inj₂ (inj₂ (inj₁ c2o))) _ _ = h2o c2o
    s2i c1i (inj₂ (inj₂ (inj₂ c2s))) q3 q4 = s3is c1i c2s q3 q4
    s3iz : (c1i : g1 ≡ f-id) (c2z : g2 ≡ f-const-z) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s3iz c1i c2z (inj₁ c3z) _ = n23 (trans c2z (sym c3z))
    s3iz c1i c2z (inj₂ (inj₁ c3i)) _ = n13 (trans c1i (sym c3i))
    s3iz c1i c2z (inj₂ (inj₂ (inj₁ c3o))) _ = h3o c3o
    s3iz c1i c2z (inj₂ (inj₂ (inj₂ c3s))) q4 =
      fun2-excl-all g4 (λ p → n24 (trans c2z (sym p))) (λ p → n14 (trans c1i (sym p))) h4o (λ p → n34 (trans c3s (sym p)))
    s3is : (c1i : g1 ≡ f-id) (c2s : g2 ≡ f-swap) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s3is c1i c2s (inj₁ c3z) q4 =
      fun2-excl-all g4 (λ p → n34 (trans c3z (sym p))) (λ p → n14 (trans c1i (sym p))) h4o (λ p → n24 (trans c2s (sym p)))
    s3is c1i c2s (inj₂ (inj₁ c3i)) _ = n13 (trans c1i (sym c3i))
    s3is c1i c2s (inj₂ (inj₂ (inj₁ c3o))) _ = h3o c3o
    s3is c1i c2s (inj₂ (inj₂ (inj₂ c3s))) _ = n23 (trans c2s (sym c3s))
    -- 第 2 层（g1 = f-swap）：g2..g4 ≠ fo, fs
    s2s : (c1s : g1 ≡ f-swap) (q2 : 分类 g2) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s2s c1s (inj₁ c2z) q3 q4 = s3sz c1s c2z q3 q4
    s2s c1s (inj₂ (inj₁ c2i)) q3 q4 = s3si c1s c2i q3 q4
    s2s c1s (inj₂ (inj₂ (inj₁ c2o))) _ _ = h2o c2o
    s2s c1s (inj₂ (inj₂ (inj₂ c2s))) _ _ = n12 (trans c1s (sym c2s))
    s3sz : (c1s : g1 ≡ f-swap) (c2z : g2 ≡ f-const-z) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s3sz c1s c2z (inj₁ c3z) _ = n23 (trans c2z (sym c3z))
    s3sz c1s c2z (inj₂ (inj₁ c3i)) q4 =
      fun2-excl-all g4 (λ p → n24 (trans c2z (sym p))) (λ p → n34 (trans c3i (sym p))) h4o (λ p → n14 (trans c1s (sym p)))
    s3sz c1s c2z (inj₂ (inj₂ (inj₁ c3o))) _ = h3o c3o
    s3sz c1s c2z (inj₂ (inj₂ (inj₂ c3s))) _ = n13 (trans c1s (sym c3s))
    s3si : (c1s : g1 ≡ f-swap) (c2i : g2 ≡ f-id) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s3si c1s c2i (inj₁ c3z) q4 =
      fun2-excl-all g4 (λ p → n34 (trans c3z (sym p))) (λ p → n24 (trans c2i (sym p))) h4o (λ p → n14 (trans c1s (sym p)))
    s3si c1s c2i (inj₂ (inj₁ c3i)) _ = n23 (trans c2i (sym c3i))
    s3si c1s c2i (inj₂ (inj₂ (inj₁ c3o))) _ = h3o c3o
    s3si c1s c2i (inj₂ (inj₂ (inj₂ c3s))) _ = n13 (trans c1s (sym c3s))
-- g0 = f-swap
fun2-no-5 g0 g1 g2 g3 g4 n01 n02 n03 n04 n12 n13 n14 n23 n24 n34 | inj₂ (inj₂ (inj₂ g0s)) =
  s1 (fun2-card g1) (fun2-card g2) (fun2-card g3) (fun2-card g4)
  where
  mutual
    h1s : g1 ≢ f-swap
    h1s p = n01 (trans g0s (sym p))
    h2s : g2 ≢ f-swap
    h2s p = n02 (trans g0s (sym p))
    h3s : g3 ≢ f-swap
    h3s p = n03 (trans g0s (sym p))
    h4s : g4 ≢ f-swap
    h4s p = n04 (trans g0s (sym p))
    s1 : (q1 : 分类 g1) (q2 : 分类 g2) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s1 (inj₁ c1z) q2 q3 q4 = s2z c1z q2 q3 q4
    s1 (inj₂ (inj₁ c1i)) q2 q3 q4 = s2i c1i q2 q3 q4
    s1 (inj₂ (inj₂ (inj₁ c1o))) q2 q3 q4 = s2o c1o q2 q3 q4
    s1 (inj₂ (inj₂ (inj₂ c1s))) _ _ _ = h1s c1s
    -- 第 2 层（g1 = f-const-z）：g2..g4 ≠ fs, fz
    s2z : (c1z : g1 ≡ f-const-z) (q2 : 分类 g2) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s2z c1z (inj₁ c2z) _ _ = n12 (trans c1z (sym c2z))
    s2z c1z (inj₂ (inj₁ c2i)) q3 q4 = s3zi c1z c2i q3 q4
    s2z c1z (inj₂ (inj₂ (inj₁ c2o))) q3 q4 = s3zo c1z c2o q3 q4
    s2z c1z (inj₂ (inj₂ (inj₂ c2s))) _ _ = h2s c2s
    s3zi : (c1z : g1 ≡ f-const-z) (c2i : g2 ≡ f-id) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s3zi c1z c2i (inj₁ c3z) _ = n13 (trans c1z (sym c3z))
    s3zi c1z c2i (inj₂ (inj₁ c3i)) _ = n23 (trans c2i (sym c3i))
    s3zi c1z c2i (inj₂ (inj₂ (inj₁ c3o))) q4 =
      fun2-excl-all g4 (λ p → n14 (trans c1z (sym p))) (λ p → n24 (trans c2i (sym p))) (λ p → n34 (trans c3o (sym p))) h4s
    s3zi c1z c2i (inj₂ (inj₂ (inj₂ c3s))) _ = h3s c3s
    s3zo : (c1z : g1 ≡ f-const-z) (c2o : g2 ≡ f-const-o) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s3zo c1z c2o (inj₁ c3z) _ = n13 (trans c1z (sym c3z))
    s3zo c1z c2o (inj₂ (inj₁ c3i)) q4 =
      fun2-excl-all g4 (λ p → n14 (trans c1z (sym p))) (λ p → n34 (trans c3i (sym p))) (λ p → n24 (trans c2o (sym p))) h4s
    s3zo c1z c2o (inj₂ (inj₂ (inj₁ c3o))) _ = n23 (trans c2o (sym c3o))
    s3zo c1z c2o (inj₂ (inj₂ (inj₂ c3s))) _ = h3s c3s
    -- 第 2 层（g1 = f-id）：g2..g4 ≠ fs, fi
    s2i : (c1i : g1 ≡ f-id) (q2 : 分类 g2) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s2i c1i (inj₁ c2z) q3 q4 = s3iz c1i c2z q3 q4
    s2i c1i (inj₂ (inj₁ c2i)) _ _ = n12 (trans c1i (sym c2i))
    s2i c1i (inj₂ (inj₂ (inj₁ c2o))) q3 q4 = s3io c1i c2o q3 q4
    s2i c1i (inj₂ (inj₂ (inj₂ c2s))) _ _ = h2s c2s
    s3iz : (c1i : g1 ≡ f-id) (c2z : g2 ≡ f-const-z) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s3iz c1i c2z (inj₁ c3z) _ = n23 (trans c2z (sym c3z))
    s3iz c1i c2z (inj₂ (inj₁ c3i)) _ = n13 (trans c1i (sym c3i))
    s3iz c1i c2z (inj₂ (inj₂ (inj₁ c3o))) q4 =
      fun2-excl-all g4 (λ p → n24 (trans c2z (sym p))) (λ p → n14 (trans c1i (sym p))) (λ p → n34 (trans c3o (sym p))) h4s
    s3iz c1i c2z (inj₂ (inj₂ (inj₂ c3s))) _ = h3s c3s
    s3io : (c1i : g1 ≡ f-id) (c2o : g2 ≡ f-const-o) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s3io c1i c2o (inj₁ c3z) q4 =
      fun2-excl-all g4 (λ p → n34 (trans c3z (sym p))) (λ p → n14 (trans c1i (sym p))) (λ p → n24 (trans c2o (sym p))) h4s
    s3io c1i c2o (inj₂ (inj₁ c3i)) _ = n13 (trans c1i (sym c3i))
    s3io c1i c2o (inj₂ (inj₂ (inj₁ c3o))) _ = n23 (trans c2o (sym c3o))
    s3io c1i c2o (inj₂ (inj₂ (inj₂ c3s))) _ = h3s c3s
    -- 第 2 层（g1 = f-const-o）：g2..g4 ≠ fs, fo
    s2o : (c1o : g1 ≡ f-const-o) (q2 : 分类 g2) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s2o c1o (inj₁ c2z) q3 q4 = s3oz c1o c2z q3 q4
    s2o c1o (inj₂ (inj₁ c2i)) q3 q4 = s3oi c1o c2i q3 q4
    s2o c1o (inj₂ (inj₂ (inj₁ c2o))) _ _ = n12 (trans c1o (sym c2o))
    s2o c1o (inj₂ (inj₂ (inj₂ c2s))) _ _ = h2s c2s
    s3oz : (c1o : g1 ≡ f-const-o) (c2z : g2 ≡ f-const-z) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s3oz c1o c2z (inj₁ c3z) _ = n23 (trans c2z (sym c3z))
    s3oz c1o c2z (inj₂ (inj₁ c3i)) q4 =
      fun2-excl-all g4 (λ p → n24 (trans c2z (sym p))) (λ p → n34 (trans c3i (sym p))) (λ p → n14 (trans c1o (sym p))) h4s
    s3oz c1o c2z (inj₂ (inj₂ (inj₁ c3o))) _ = n13 (trans c1o (sym c3o))
    s3oz c1o c2z (inj₂ (inj₂ (inj₂ c3s))) _ = h3s c3s
    s3oi : (c1o : g1 ≡ f-const-o) (c2i : g2 ≡ f-id) (q3 : 分类 g3) (q4 : 分类 g4) → ⊥
    s3oi c1o c2i (inj₁ c3z) q4 =
      fun2-excl-all g4 (λ p → n34 (trans c3z (sym p))) (λ p → n24 (trans c2i (sym p))) (λ p → n14 (trans c1o (sym p))) h4s
    s3oi c1o c2i (inj₂ (inj₁ c3i)) _ = n23 (trans c2i (sym c3i))
    s3oi c1o c2i (inj₂ (inj₂ (inj₁ c3o))) _ = n13 (trans c1o (sym c3o))
    s3oi c1o c2i (inj₂ (inj₂ (inj₂ c3s))) _ = h3s c3s

-- ==================================================================
-- §6 无双射：Hom_Sp ≥ 5 vs |F2 → F2| = 4（对应 Lean §8 no_bijection）
-- ==================================================================
-- 对应 Lean no_bijection_homSp_homRec 的有限核心：
--   Lean 侧 Hom_Sp 无限（ℂ 嵌入 z ↦ [[z,0],[0,0]]）在有限载体 ℂ = c0/c1/c2 下
--   不可表达，故形式化其有限基数缺口：Hom_Sp 至少有 5 个互异元素，而 (F2 → F2)
--   恰有 4 个互异元素（fun2-card 枚举 + 4 个函数两两互异）。
--   RecHom 经 rec-hom-card 落入同 4 个函数类（§3）；RecHom-≡（记录外延性）
--   需依赖版 funext，超出库的公理范围（仅非依赖 funext），故计数直接落在函数层。
-- 结论：不存在 Hom_Sp(D X, D X) 与 (F2 → F2) 之间的双射（鸽笼 5→4）。

-- 高层不等性（SpHom 在 Set₁，库的 _≢_ 只接受 Set）
_≢₁_ : {A : Set₁} → A → A → Set₁
x ≢₁ y = x ≡ y → ⊥

-- Set₁ 级等式工具（库的 cong/sym/trans 为 Set 级；DecursionFunctor 已提供
-- cong₁ : Set → Set₁ 与 uip₁）
congL1 : {A : Set₁} {B : Set} {x y : A} (f : A → B) → x ≡ y → f x ≡ f y
congL1 f refl = refl

sym₁ : {A : Set₁} {x y : A} → x ≡ y → y ≡ x
sym₁ refl = refl

trans₁ : {A : Set₁} {x y z : A} → x ≡ y → y ≡ z → x ≡ z
trans₁ refl refl = refl

-- 双射（对应 Lean Equiv；Hom_Sp 侧为 Set₁）
record Equiv (A : Set₁) (B : Set) : Set₁ where
  field
    toFun : A → B
    invFun : B → A
    left-inv : ∀ a → invFun (toFun a) ≡ a
    right-inv : ∀ b → toFun (invFun b) ≡ b

-- 4 个平凡 RecHom（step = id ⇒ comm 平凡；用于构造 D 的像态射）
rec-const-z : RecHom trivial2 trivial2
rec-const-z = record { toFun = f-const-z ; comm = λ _ → refl }

rec-id : RecHom trivial2 trivial2
rec-id = record { toFun = f-id ; comm = λ _ → refl }

rec-const-o : RecHom trivial2 trivial2
rec-const-o = record { toFun = f-const-o ; comm = λ _ → refl }

rec-swap : RecHom trivial2 trivial2
rec-swap = record { toFun = f-swap ; comm = λ _ → refl }

-- 5 个互异谱态射：4 个转移矩阵态射（D 的像）+ 反例 P
sp-const-z : SpHom (D-obj trivial2) (D-obj trivial2)
sp-const-z = D-map rec-const-z

sp-id : SpHom (D-obj trivial2) (D-obj trivial2)
sp-id = D-map rec-id

sp-const-o : SpHom (D-obj trivial2) (D-obj trivial2)
sp-const-o = D-map rec-const-o

sp-swap : SpHom (D-obj trivial2) (D-obj trivial2)
sp-swap = D-map rec-swap

sp-P : SpHom (D-obj trivial2) (D-obj trivial2)
sp-P = P-spectral

-- P 投影（态射 → 矩阵）
spP : SpHom (D-obj trivial2) (D-obj trivial2) → (F2 → F2 → ℂ)
spP h = SpHom.P h

-- 矩阵互异 ⇒ 态射互异（经 P 投影取反）
sp-ne : (a b : SpHom (D-obj trivial2) (D-obj trivial2)) → spP a ≢ spP b → a ≢₁ b
sp-ne a b pab eq = pab (congL1 spP eq)

-- 5 个态射两两互异（P 矩阵两两互异：transfers-distinct + P-distinct-transfers）
sp-const-z≢sp-id : sp-const-z ≢₁ sp-id
sp-const-z≢sp-id = sp-ne sp-const-z sp-id (tm-ne f-const-z≢f-id)

sp-const-z≢sp-const-o : sp-const-z ≢₁ sp-const-o
sp-const-z≢sp-const-o = sp-ne sp-const-z sp-const-o (tm-ne f-const-z≢f-const-o)

sp-const-z≢sp-swap : sp-const-z ≢₁ sp-swap
sp-const-z≢sp-swap = sp-ne sp-const-z sp-swap (tm-ne f-const-z≢f-swap)

sp-const-z≢sp-P : sp-const-z ≢₁ sp-P
sp-const-z≢sp-P = sp-ne sp-const-z sp-P (transferMatrix-not-P f-const-z)

sp-id≢sp-const-o : sp-id ≢₁ sp-const-o
sp-id≢sp-const-o = sp-ne sp-id sp-const-o (tm-ne f-id≢f-const-o)

sp-id≢sp-swap : sp-id ≢₁ sp-swap
sp-id≢sp-swap = sp-ne sp-id sp-swap (tm-ne f-id≢f-swap)

sp-id≢sp-P : sp-id ≢₁ sp-P
sp-id≢sp-P = sp-ne sp-id sp-P (transferMatrix-not-P f-id)

sp-const-o≢sp-swap : sp-const-o ≢₁ sp-swap
sp-const-o≢sp-swap = sp-ne sp-const-o sp-swap (tm-ne f-const-o≢f-swap)

sp-const-o≢sp-P : sp-const-o ≢₁ sp-P
sp-const-o≢sp-P = sp-ne sp-const-o sp-P (transferMatrix-not-P f-const-o)

sp-swap≢sp-P : sp-swap ≢₁ sp-P
sp-swap≢sp-P = sp-ne sp-swap sp-P (transferMatrix-not-P f-swap)

-- **无双射**（对应 Lean no_bijection_homSp_homRec 的有限核心）
-- 若有双射 e，5 个互异 SpHom 经 e（单射）得 5 个互异函数 → 鸽笼 fun2-no-5 矛盾。
no-bijection : (e : Equiv (SpHom (D-obj trivial2) (D-obj trivial2)) (F2 → F2)) → ⊥
no-bijection e = fun2-no-5 f0 f1 f2 f3 f4 d01 d02 d03 d04 d12 d13 d14 d23 d24 d34
  where
  open Equiv e
  f0 : F2 → F2
  f0 = toFun sp-const-z
  f1 : F2 → F2
  f1 = toFun sp-id
  f2 : F2 → F2
  f2 = toFun sp-const-o
  f3 : F2 → F2
  f3 = toFun sp-swap
  f4 : F2 → F2
  f4 = toFun sp-P
  -- 双射 e 单射
  e-inj : {a b : SpHom (D-obj trivial2) (D-obj trivial2)} → a ≢₁ b → toFun a ≢ toFun b
  e-inj {a} {b} a≢b fab = a≢b (trans₁ (sym₁ (left-inv a)) (trans₁ (cong₁ invFun fab) (left-inv b)))
  d01 : f0 ≢ f1
  d01 = e-inj sp-const-z≢sp-id
  d02 : f0 ≢ f2
  d02 = e-inj sp-const-z≢sp-const-o
  d03 : f0 ≢ f3
  d03 = e-inj sp-const-z≢sp-swap
  d04 : f0 ≢ f4
  d04 = e-inj sp-const-z≢sp-P
  d12 : f1 ≢ f2
  d12 = e-inj sp-id≢sp-const-o
  d13 : f1 ≢ f3
  d13 = e-inj sp-id≢sp-swap
  d14 : f1 ≢ f4
  d14 = e-inj sp-id≢sp-P
  d23 : f2 ≢ f3
  d23 = e-inj sp-const-o≢sp-swap
  d24 : f2 ≢ f4
  d24 = e-inj sp-const-o≢sp-P
  d34 : f3 ≢ f4
  d34 = e-inj sp-swap≢sp-P
