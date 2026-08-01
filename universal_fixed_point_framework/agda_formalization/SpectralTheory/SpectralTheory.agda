module SpectralTheory.SpectralTheory where

{-
  T3 谱定理层（阶段 6，2026-08-01）
  ========================================
  对应笔记: notes/00_foundations/spectral_R11_morphism_layer.md §4（引理 1/2、定理 3、推论 5）
  对应蓝图: notes/00_foundations/spectral_T3_analysis_foundation.md §5.14（阶段 6 立项）

  目标：建立无限维谱论形式化层——P1（R11 无限维态射层验证）的前置依赖。
  P1 笔记 §9 所需引理：谱测度输送（Fuglede，引理 1）、exp/log 函数演算单射性
  （引理 2）、Hille-Yosida 半群（对象层）。

  结构：
    1. 谱论基础公理（谱测度 E / 谱表示 / 函数演算 / Fuglede 方向 / 谱积分线性 /
       谱测度复合 / 谱测度外延 / Hille-Yosida 半群）
    2. φ(x) = e^(-x) 的可证引理（exp 单射 ⟹ φ 单射；exp-log ⟹ 值域刻画）
    3. 引理 2 核心（可证）：M_Rec ⊆ M_σ（exp 单射 + 谱测度复合 + Fuglede）
    4. 三条件谓词 M_Sp / M_σ / M_Rec 与定理 3（无限维版）
    5. 推论 5 核心：-log(φ(x)) = x（可证）+ 对象重建公理登记

  公理纪律（谱论基础假设，对齐"ℝ 公理是基础假设"立场）：
    - 谱测度 E、谱表示（谱定理）、Fuglede 方向（交织 ⟹ 谱交换）、谱积分线性、
      谱测度外延、谱测度复合、Hille-Yosida 半群 = 谱论基础公理——
      每个注明模型必然性与降定理路径（谱积分/测度论完整实现时转为可证明定理）
    - **核心定理真实证明**（不允许占位）：φ 单射（exp-inj + neg-neg）、
      谱测度输送往返（φ-image-roundtrip）、M_Rec ⊆ M_σ（Rec-to-σ）、
      M_σ ⊆ M_Sp / M_σ ⊆ M_Rec（谱积分线性 + 谱表示重写）、-log(φ(x)) = x
-}

open import Agda.Builtin.Equality using (_≡_; refl)
open import Agda.Primitive using (Level; _⊔_)
open import Sp.SpCategory using (ℕ; zero; suc; Fin; _×_; _,_; sym; trans; cong; cong₂)

-- ℝ 层（T3 已建：序代数 + exp/log/rpow + exp-inj 可证）
open import DHStructural.DHStructuralAnalysis
  using (ℝ; zeroℝ; oneℝ; negℝ; exp; log; _≤ℝ_; subst; neg-neg; exp-inj; log-exp; exp-log; _+ℝ_)

-- 复用 P1Spectral 的算子代数（using 只取 Op 代数公理，避免有限维谱设定名字冲突）
open import P1Spectral.P1Spectral
  using (Op; _+ₒ_; _*ₒ_; _·ₒ_; 𝟘ₒ; 𝟙ₒ;
         +ₒ-assoc; +ₒ-comm; +ₒ-ident;
         *ₒ-assoc; *ₒ-ident; *ₒ-ident-l; *ₒ-zero-r; *ₒ-zero-l;
         distribₒ; distribₒ-l; ·ₒ-comm; ·ₒ-comm-l)

-- 本地依赖对（库未提供 Agda.Builtin.Sigma）
data Σ (A : Set) (B : A → Set) : Set where
  _,_ : (a : A) → B a → Σ A B

proj₁ : {A : Set} {B : A → Set} → Σ A B → A
proj₁ (a , b) = a

proj₂ : {A : Set} {B : A → Set} → (p : Σ A B) → B (proj₁ p)
proj₂ (a , b) = b

-- 本地 Set₁ 层积（SpCategory 的 _×_ 为 Set 层，Set₁ 值需自有积；构造子独立命名避免歧义）
data _×₁_ (A B : Set₁) : Set₁ where
  pair₁ : A → B → A ×₁ B

-- ==================================================================
-- §1 谱论基础公理（无限维自伴算子 + 谱测度 + 函数演算）
-- ==================================================================

-- Borel 集 = ℝ 上的谓词（避免 σ-代数构造：量化和谓词已足够）
Borel : Set₁
Borel = ℝ → Set

-- 无限维自伴正定算子（P1 设定 E = (H_E, A_E, σ_E) 的 A_E）
postulate
  A : Op
  -- 谱测度 E : Borel → Op（投影值测度；投影/正交/σ-可加为谱论基础公理，
  -- 当前证明仅用谱支集与集合外延）
  E : Borel → Op
  -- 谱支集在 [0,∞)（A 自伴正定，σ(A) ⊆ [0,∞)）：E(P) = E(P ∩ [0,∞))
  E-support-pos : (P : Borel) → E P ≡ E (λ x → (P x) × (zeroℝ ≤ℝ x))
  -- 谱表示（谱定理）：A = ∫ λ dE(λ)，spec-int-A 为抽象谱积分记号
  spec-int-A : Op
  spectral-rep-A : A ≡ spec-int-A
  -- 谱积分线性：X 与谱测度逐集交换 ⟹ X 与谱表示交换
  --（谱积分基本性质：有界 X 与 E 交换时 X 可穿过积分；谱积分理论完整实现时降为定理）
  X-comm-spectral-int : (X : Op) → ((P : Borel) → X *ₒ E P ≡ E P *ₒ X) → X *ₒ spec-int-A ≡ spec-int-A *ₒ X
  -- Fuglede（引理 1 ⟹ 方向）：交织 ⟹ 谱匹配
  --（Fuglede 定理：X 与自伴 A 交换 ⟹ X 与 A 的每个谱测度投影交换；
  --  标准谱论事实，Reed-Simon；谱测度输送引理，P1 笔记引理 1）
  intertwine-imp-spectral : (X : Op) → X *ₒ A ≡ A *ₒ X → (P : Borel) → X *ₒ E P ≡ E P *ₒ X

-- 函数演算：e^(-A)（Borel 函数演算，φ(x) = e^(-x) 作用于谱）
postulate
  exp-A : Op
  -- e^(-A) 的谱测度：E-exp(P) = E(φ⁻¹P)（函数演算复合：谱测度经 φ 输送）
  E-exp : Borel → Op
  exp-spectral-measure : (P : Borel) → E-exp P ≡ E (λ x → P (exp (negℝ x)))
  -- e^(-A) 谱表示
  spec-int-exp : Op
  exp-spectral-rep : exp-A ≡ spec-int-exp
  -- e^(-A) 侧谱积分线性
  X-comm-spectral-int-exp : (X : Op) → ((P : Borel) → X *ₒ E P ≡ E P *ₒ X) → X *ₒ spec-int-exp ≡ spec-int-exp *ₒ X
  -- e^(-A) 侧 Fuglede：与自伴算子 e^(-A) 交换 ⟹ 与其谱测度 E-exp 交换
  --（e^(-A) 由 Borel 函数演算保持自伴性；exp 单射保证谱点分离）
  intertwine-exp-imp-spectral-exp : (X : Op) → X *ₒ exp-A ≡ exp-A *ₒ X → (P : Borel) → X *ₒ E-exp P ≡ E-exp P *ₒ X
  -- 谱测度外延：点态等价 ⟹ 谱测度相等（谱测度只依赖集合）
  spectral-ext : (P Q : Borel) → ((x : ℝ) → (P x → Q x) × (Q x → P x)) → E P ≡ E Q

-- Hille-Yosida 半群（对象层：R(E) 的演化映射 e^(-tA)）
-- 登记为基础公理；强连续/压缩（需范数/拓扑）随 Hilbert 空间层补充
postulate
  exp-tA : ℝ → Op
  semigroup : (s t : ℝ) → exp-tA (s +ℝ t) ≡ exp-tA s *ₒ exp-tA t
  exp-tA-zero : exp-tA zeroℝ ≡ 𝟙ₒ
  exp-tA-one : exp-tA oneℝ ≡ exp-A

-- ==================================================================
-- §2 φ(x) = e^(-x) 的可证引理（exp 单射 + log 逆）
-- ==================================================================

-- φ(x) = e^(-x)（谱映射 [0,∞) → (0,1]）
φ : ℝ → ℝ
φ x = exp (negℝ x)

-- φ 单射：φ x = φ y ⟹ x = y（exp-inj 可证 + neg-neg）
phi-inj : {x y : ℝ} → φ x ≡ φ y → x ≡ y
phi-inj {x} {y} h =
  trans (sym (neg-neg x))
        (trans (cong negℝ (exp-inj h)) (neg-neg y))

-- φ 的像集：φ-image P = {y : ∃x. φ x = y × P x}（经 φ 的集输送）
φ-image : (P : Borel) → Borel
φ-image P y = Σ ℝ (λ x → (φ x ≡ y) × P x)

-- 谱测度输送往返：对任意 x，P x ⟺ φ-image P (exp (negℝ x))（φ 单射）
--（引理 2 的谱测度族等价核心：E(φ⁻¹(φ(P))) = E(P)；
--  谓词用显式 exp (negℝ x) 形式，对齐 exp-spectral-measure）
φ-image-roundtrip : (P : Borel) (x : ℝ) → (P x → φ-image P (exp (negℝ x))) × (φ-image P (exp (negℝ x)) → P x)
φ-image-roundtrip P x = back , forth
  where
  -- P x ⟹ ∃y. φ y = φ x × P y（取 y = x）
  back : P x → φ-image P (exp (negℝ x))
  back px = x , (refl , px)
  -- ∃y. φ y = φ x × P y ⟹ P x（φ 单射 ⟹ y = x）
  forth : φ-image P (exp (negℝ x)) → P x
  forth (y , (eq , py)) = subst P (phi-inj {x = y} {y = x} eq) py

-- 谱测度等价：E(P) = E(φ⁻¹(φ(P)))（spectral-ext + roundtrip，**可证明**）
E-phi-image : (P : Borel) → E P ≡ E (λ x → φ-image P (exp (negℝ x)))
E-phi-image P = spectral-ext P (λ x → φ-image P (exp (negℝ x))) (φ-image-roundtrip P)

-- ==================================================================
-- §3 引理 2（无限维版）：exp 单射 ⟹ 换位代数相等（M_Rec ⊆ M_σ）
-- ==================================================================

-- 三条件谓词（对应 P1 笔记 §2 的 M_Sp / M_σ / M_Rec，无限维版）
M-Sp : Op → Set
M-Sp X = X *ₒ A ≡ A *ₒ X

M-σ : Op → Set₁
M-σ X = (P : Borel) → X *ₒ E P ≡ E P *ₒ X

M-Rec : Op → Set
M-Rec X = X *ₒ exp-A ≡ exp-A *ₒ X

-- 引理 2 核心（**可证明**）：M_Rec ⊆ M_σ
-- 链：X·e^(-A) = e^(-A)·X
--   ⟹ ∀P. X·E-exp P = E-exp P·X        [Fuglede 对 e^(-A)，公理]
--   ⟹ ∀P. X·E(φ⁻¹P) = E(φ⁻¹P)·X        [exp-spectral-measure]
--   ⟹ ∀Q. X·E Q = E Q·X                [φ-image-roundtrip（φ 单射）+ spectral-ext]
Rec-to-σ : {X : Op} → M-Rec X → M-σ X
Rec-to-σ {X} h P =
  trans (cong (λ Y → X *ₒ Y) (E-phi-image P))
  (trans (cong (λ Y → X *ₒ Y) (sym (exp-spectral-measure (φ-image P))))
  (trans (intertwine-exp-imp-spectral-exp X h (φ-image P))
  (trans (cong (λ Y → Y *ₒ X) (exp-spectral-measure (φ-image P)))
         (cong (λ Y → Y *ₒ X) (sym (E-phi-image P))))))

-- 引理 1 代数方向（**可证明**，谱积分线性公理 + 谱表示重写）：M_σ ⊆ M_Sp
σ-to-Sp : {X : Op} → M-σ X → M-Sp X
σ-to-Sp {X} h =
  trans (cong (λ Y → X *ₒ Y) spectral-rep-A)
  (trans (X-comm-spectral-int X h)
         (cong (λ Y → Y *ₒ X) (sym spectral-rep-A)))

-- 引理 2 反向（**可证明**，谱积分线性公理 + exp 谱表示重写）：M_σ ⊆ M_Rec
σ-to-Rec : {X : Op} → M-σ X → M-Rec X
σ-to-Rec {X} h =
  trans (cong (λ Y → X *ₒ Y) exp-spectral-rep)
  (trans (X-comm-spectral-int-exp X h)
         (cong (λ Y → Y *ₒ X) (sym exp-spectral-rep)))

-- 引理 1 方向（Fuglede，公理）：M_Sp ⊆ M_σ
Sp-to-σ : {X : Op} → M-Sp X → M-σ X
Sp-to-σ {X} h P = intertwine-imp-spectral X h P

-- ==================================================================
-- §4 定理 3（无限维版）：M_Sp = M_σ = M_Rec（线性语义下谱匹配双射）
-- ==================================================================

theorem3-Sp-σ : {X : Op} → (M-Sp X → M-σ X) ×₁ (M-σ X → M-Sp X)
theorem3-Sp-σ = pair₁ (λ h → Sp-to-σ h) (λ h → σ-to-Sp h)

theorem3-Rec-σ : {X : Op} → (M-Rec X → M-σ X) ×₁ (M-σ X → M-Rec X)
theorem3-Rec-σ = pair₁ (λ h → Rec-to-σ h) (λ h → σ-to-Rec h)

theorem3 : {X : Op} → ((M-Sp X → M-σ X) ×₁ (M-σ X → M-Sp X))
               ×₁ ((M-Rec X → M-σ X) ×₁ (M-σ X → M-Rec X))
theorem3 = pair₁ (pair₁ (λ h → Sp-to-σ h) (λ h → σ-to-Sp h))
                 (pair₁ (λ h → Rec-to-σ h) (λ h → σ-to-Rec h))

-- ==================================================================
-- §5 推论 5（对象重建 D(R(E)) ≅ E）：-log(e^(-A)) = A
-- ==================================================================

-- 函数演算（Borel 函数演算 f(A)，抽象记号）
postulate
  fc : (ℝ → ℝ) → Op
  -- 恒等函数 ⟹ A（函数演算保持恒等：∫ id dE = A，谱表示）
  fc-id : fc (λ x → x) ≡ A
  -- 函数演算点态外延：f ≡ g 点态 ⟹ f(A) = g(A)
  fc-ext : {f g : ℝ → ℝ} → ((x : ℝ) → f x ≡ g x) → fc f ≡ fc g
  -- 复合：-log(e^(-A)) 的算子 = (-log∘φ)(A)（函数演算复合：g(f(A)) = (g∘f)(A)）
  recon-op : Op
  recon-op-fc : recon-op ≡ fc (λ x → negℝ (log (φ x)))

-- -log(φ(x)) = x 在 [0,∞) 上（log-exp + neg-neg；**可证明**，推论 5 函数演算核心）
neg-log-phi-id : (x : ℝ) → negℝ (log (φ x)) ≡ x
neg-log-phi-id x = trans (cong negℝ (log-exp (negℝ x))) (neg-neg x)

-- 推论 5（对象重建，**可证明**，函数演算公理之上）：
-- recon-op = -log(e^(-A)) ≡ fc(-log∘φ) [复合] ≡ fc(id) [点态外延 + neg-log-phi-id] ≡ A [恒等保持]
corollary5 : recon-op ≡ A
corollary5 =
  trans recon-op-fc
        (trans (fc-ext (λ x → neg-log-phi-id x)) fc-id)

-- ==================================================================
-- §6 P1 无限维组装（推论 4 无限维版：Hom_Sp ≅ Hom_σ ≅ Hom_Rec）
-- ==================================================================

-- level 多态 cong（Hom-σ 的 prop 为 Set₁，M-σ 为 Set₁ 值；Agda.Builtin.Equality 的 _≡_ 为 level-多态）
cong₁ : {a b : Level} {A : Set a} {B : Set b} {x y : A} (f : A → B) → x ≡ y → f x ≡ f y
cong₁ f refl = refl

-- 互逆往返一致性（定义性公理：谱表示（spectral-rep-A / exp-spectral-rep）与
-- 谱积分线性（X-comm-spectral-int / -exp）之间的往返一致性；
-- 谱积分理论完整实现时降为定理）
postulate
  σ→Sp∘Sp→σ : {X : Op} (h : M-Sp X) → σ-to-Sp (Sp-to-σ h) ≡ h
  Sp→σ∘σ→Sp : {X : Op} (h : M-σ X) → Sp-to-σ (σ-to-Sp h) ≡ h
  σ→Rec∘Rec→σ : {X : Op} (h : M-Rec X) → σ-to-Rec (Rec-to-σ h) ≡ h
  Rec→σ∘σ→Rec : {X : Op} (h : M-σ X) → Rec-to-σ (σ-to-Rec h) ≡ h

-- Hom 集合（无限维：谱态射 / 谱匹配态射 / 递归态射）
-- 注：Hom-σ 为 Set₁（prop : M-σ op 量化 Borel 集）
record Hom-Sp : Set where
  field
    op : Op
    prop : M-Sp op

record Hom-σ : Set₁ where
  field
    op : Op
    prop : M-σ op

record Hom-Rec : Set where
  field
    op : Op
    prop : M-Rec op

-- 双射（恒等映射：两边都是 M_σ 上的同构，对应 P1 笔记推论 4 无限维版；
-- level 多态以容纳 Hom-Sp : Set 与 Hom-σ : Set₁）
record _≅ₗ_ {a b : Level} (A : Set a) (B : Set b) : Set (a ⊔ b) where
  field
    to : A → B
    from : B → A
    to∘from : (b : B) → to (from b) ≡ b
    from∘to : (a : A) → from (to a) ≡ a

Sp≅σ₁ : Hom-Sp ≅ₗ Hom-σ
Sp≅σ₁ = record
  { to = λ h → record { op = Hom-Sp.op h ; prop = Sp-to-σ (Hom-Sp.prop h) }
  ; from = λ h → record { op = Hom-σ.op h ; prop = σ-to-Sp (Hom-σ.prop h) }
  ; to∘from = λ b → cong₁ (λ w → record { op = Hom-σ.op b ; prop = w }) (Sp→σ∘σ→Sp (Hom-σ.prop b))
  ; from∘to = λ a → cong₁ (λ w → record { op = Hom-Sp.op a ; prop = w }) (σ→Sp∘Sp→σ (Hom-Sp.prop a))
  }

Rec≅σ₁ : Hom-Rec ≅ₗ Hom-σ
Rec≅σ₁ = record
  { to = λ h → record { op = Hom-Rec.op h ; prop = Rec-to-σ (Hom-Rec.prop h) }
  ; from = λ h → record { op = Hom-σ.op h ; prop = σ-to-Rec (Hom-σ.prop h) }
  ; to∘from = λ b → cong₁ (λ w → record { op = Hom-σ.op b ; prop = w }) (Rec→σ∘σ→Rec (Hom-σ.prop b))
  ; from∘to = λ a → cong₁ (λ w → record { op = Hom-Rec.op a ; prop = w }) (σ→Rec∘Rec→σ (Hom-Rec.prop a))
  }

-- 推论 4（无限维版）：Hom_Sp 与 Hom_Rec 都 ≅ Hom_σ（同一集合 M_σ，恒等双射）
corollary4-∞ : (Hom-Sp ≅ₗ Hom-σ) ×₁ (Hom-Rec ≅ₗ Hom-σ)
corollary4-∞ = pair₁ Sp≅σ₁ Rec≅σ₁

-- ==================================================================
-- §7 简单函数谱积分层（谱积分理论细化：X-comm-spectral-int 的降定理路径）
-- ==================================================================

-- 有限求和（Op 层）
sum-op : {m : ℕ} → (Fin m → Op) → Op
sum-op {zero} f = 𝟘ₒ
sum-op {suc m} f = f zero +ₒ sum-op {m} (λ i → f (suc i))

-- 简单函数谱积分：∫(Σᵢ cᵢ·1_{Ωᵢ}) dE = Σᵢ cᵢ·E(Ωᵢ)
--（简单函数 = 有限 Borel 划分 {Ωᵢ} 上的有限线性组合；谱积分对简单函数是有限组合）
spec-int-simple : {m : ℕ} → (Fin m → ℝ) → (Fin m → Borel) → Op
spec-int-simple {m} c Ω = sum-op {m} (λ i → c i ·ₒ E (Ω i))

-- **可证明（零新增公理）**：X 与谱测度逐集交换 ⟹ X 与简单函数谱积分交换
--（引理 1 代数方向（谱匹配 ⟹ 交织）的简单函数版：
--  谱积分线性 + X 与 E 可交换时 X 可穿过有限组合——distribₒ + ·ₒ-comm 逐项）
simple-comm : {m : ℕ} (X : Op) (c : Fin m → ℝ) (Ω : Fin m → Borel)
  → ((P : Borel) → X *ₒ E P ≡ E P *ₒ X)
  → X *ₒ spec-int-simple {m} c Ω ≡ spec-int-simple {m} c Ω *ₒ X
simple-comm {zero} X c Ω h =
  trans (*ₒ-zero-r X) (sym (*ₒ-zero-l X))
simple-comm {suc m} X c Ω h =
  trans (distribₒ X (c zero ·ₒ E (Ω zero)) rest)
        (trans (cong₂ _+ₒ_ head tail-comm)
               (sym (distribₒ-l (c zero ·ₒ E (Ω zero)) rest X)))
  where
  rest : Op
  rest = spec-int-simple {m} (λ i → c (suc i)) (λ i → Ω (suc i))
  -- X·(c0·E(Ω0)) = (c0·E(Ω0))·X（标量中心 + h 逐集）
  head : X *ₒ (c zero ·ₒ E (Ω zero)) ≡ (c zero ·ₒ E (Ω zero)) *ₒ X
  head = trans (·ₒ-comm-l (c zero) X (E (Ω zero)))
               (trans (cong (λ y → c zero ·ₒ y) (h (Ω zero)))
                      (sym (·ₒ-comm (c zero) (E (Ω zero)) X)))
  -- 归纳：X·rest = rest·X
  tail-comm : X *ₒ rest ≡ rest *ₒ X
  tail-comm = simple-comm {m} X (λ i → c (suc i)) (λ i → Ω (suc i)) h

-- 谱积分理论细化状态：
--  - 简单函数层：spec-int-simple 线性（simple-comm，**可证**）——X-comm-spectral-int 公理的
--    降定理路径第一步（简单函数部分已从公理变为可证明定理）。
--  - 一般函数层：∫λ dE 经简单函数逼近（测度论单调逼近定理）——极限/逼近层随
--    完备性（sup-ℝ）扩展登记，X-comm-spectral-int 公理届时降为定理。
--  - 有限维对应：P1Spectral proj-comm-scalar-sum（有限谱点）为同一引理的离散谱版。
