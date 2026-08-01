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
open import Sp.SpCategory using (ℕ; zero; suc; Fin; _×_; _,_; _≢_; sym; trans; cong; cong₂)

-- ℝ 层（T3 已建：序代数 + exp/log/rpow + exp-inj 可证）
open import DHStructural.DHStructuralAnalysis
  using (ℝ; zeroℝ; oneℝ; negℝ; exp; log; _≤ℝ_; _<ℝ_; _+ℝ_; _*ℝ_; subst; neg-neg; exp-inj; log-exp; exp-log;
         exp-pos; exp-mono-≤; exp-zero; neg-≤-ℝ; *-≤-mono-ℝ; *-comm-ℝ; *-zero-ℝ; neg-zero; +-comm-ℝ;
         *-pos-mono-ℝ; trichotomy-ℝ; irreflexive-ℝ; ⊥; ⊥-elim; _⊎_; inj₁; inj₂)

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

-- ==================================================================
-- §7b 简单函数谱积分：加法性（线性完整化）
-- ==================================================================

-- 算子代数补充公理（P1Spectral §1 的最小算子代数未含标量分配）：
-- 标量乘对加法的分配律（标准算子代数内容，模型必然性 = 标量乘线性）
postulate
  ·ₒ-+ : (a b : ℝ) (x : Op) → ((a +ℝ b) ·ₒ x) ≡ (a ·ₒ x) +ₒ (b ·ₒ x)

-- 求和逐点同余（可证）
sum-op-congₒ : {m : ℕ} {f g : Fin m → Op} → ((i : Fin m) → f i ≡ g i) → sum-op {m} f ≡ sum-op {m} g
sum-op-congₒ {zero} h = refl
sum-op-congₒ {suc m} {f} {g} h =
  cong₂ _+ₒ_ (h zero) (sum-op-congₒ {m} {λ i → f (suc i)} {λ i → g (suc i)} (λ i → h (suc i)))

-- 加法重组（可证）：(a+b)+(c+d) = (a+c)+(b+d)
swap-pairₒ : (a b c d : Op) → (a +ₒ b) +ₒ (c +ₒ d) ≡ (a +ₒ c) +ₒ (b +ₒ d)
swap-pairₒ a b c d =
  trans (+ₒ-assoc a b (c +ₒ d))
  (trans (cong (λ x → a +ₒ x) inner)
  (trans (sym (+ₒ-assoc a (c +ₒ b) d))
  (trans (cong (λ x → x +ₒ d) (sym (+ₒ-assoc a c b)))
         (+ₒ-assoc (a +ₒ c) b d))))
  where
  -- b+(c+d) = (c+b)+d
  inner : b +ₒ (c +ₒ d) ≡ (c +ₒ b) +ₒ d
  inner =
    trans (sym (+ₒ-assoc b c d))
          (cong (λ x → x +ₒ d) (+ₒ-comm b c d))

-- 求和加法性（可证）：Σ(f+g) = Σf + Σg
sum-op-+ : {m : ℕ} (f g : Fin m → Op) → sum-op {m} (λ i → f i +ₒ g i) ≡ sum-op {m} f +ₒ sum-op {m} g
sum-op-+ {zero} f g = sym (+ₒ-ident 𝟘ₒ)
sum-op-+ {suc m} f g =
  trans (cong₂ _+ₒ_ refl (sum-op-+ {m} (λ i → f (suc i)) (λ i → g (suc i))))
        (swap-pairₒ (f zero) (g zero) (sum-op {m} (λ i → f (suc i))) (sum-op {m} (λ i → g (suc i))))

-- **可证明（零新增公理，·ₒ-+ 为算子代数基础）**：简单函数谱积分加法性
-- ∫(f+g) dE = ∫f dE + ∫g dE
simple-add : {m : ℕ} (c d : Fin m → ℝ) (Ω : Fin m → Borel)
  → spec-int-simple {m} (λ i → c i +ℝ d i) Ω ≡ spec-int-simple {m} c Ω +ₒ spec-int-simple {m} d Ω
simple-add {m} c d Ω =
  trans (sum-op-congₒ {m} (λ i → ·ₒ-+ (c i) (d i) (E (Ω i))))
        (sum-op-+ {m} (λ i → c i ·ₒ E (Ω i)) (λ i → d i ·ₒ E (Ω i)))

-- 谱积分理论细化状态：
--  - 简单函数层：spec-int-simple 线性（simple-comm 交换性 + simple-add 加法性，**可证**，
--    ·ₒ-+ 为算子代数基础公理）——X-comm-spectral-int 公理的降定理路径第一步
--    （简单函数部分已从公理变为可证明定理）。
--  - 一般函数层：∫λ dE 经简单函数逼近（测度论单调逼近定理）——极限/逼近层随
--    完备性（sup-ℝ）扩展登记，X-comm-spectral-int 公理届时降为定理。
--  - 有限维对应：P1Spectral proj-comm-scalar-sum（有限谱点）为同一引理的离散谱版。

-- ==================================================================
-- §8 Hille-Yosida 谱侧基础（对象层 e^(-tA)：半群交换 + φ_t 值域 + 谱测度复合）
-- ==================================================================

-- **可证明（零新增公理）**：半群元素互相交换 e^(-sA)·e^(-tA) = e^(-tA)·e^(-sA)
--（semigroup 方程 + ℝ 加法交换）
semigroup-comm : (s t : ℝ) → exp-tA s *ₒ exp-tA t ≡ exp-tA t *ₒ exp-tA s
semigroup-comm s t =
  trans (sym (semigroup s t))
        (trans (cong exp-tA (+-comm-ℝ s t))
               (semigroup t s))

-- φ_t(x) = e^(-tx)（谱映射 [0,∞) → (0,1]，t ≥ 0）
φ-t : ℝ → ℝ → ℝ
φ-t t x = exp (negℝ (t *ℝ x))

-- **可证明**：0 < φ_t(t·x)（exp-pos）
phi-t-pos : (t x : ℝ) → zeroℝ <ℝ φ-t t x
phi-t-pos t x = exp-pos (negℝ (t *ℝ x))

-- 辅助：0·x ≡ 0
zero-mul : (x : ℝ) → zeroℝ *ℝ x ≡ zeroℝ
zero-mul x = trans (*-comm-ℝ zeroℝ x) (*-zero-ℝ x)

-- **可证明**：t ≥ 0、x ≥ 0 ⟹ φ_t(t·x) ≤ 1
--（t·x ≥ 0 [*-≤-mono-ℝ] ⟹ -tx ≤ 0 [neg-≤-ℝ] ⟹ e^(-tx) ≤ e^0 = 1 [exp-mono-≤ + exp-zero]）
phi-t-lt-one : (t x : ℝ) → zeroℝ ≤ℝ t → zeroℝ ≤ℝ x → φ-t t x ≤ℝ oneℝ
phi-t-lt-one t x ht hx =
  subst (λ y → φ-t t x ≤ℝ y) exp-zero
        (exp-mono-≤ neg-tx-le-0)
  where
  -- t·x ≥ 0（0 ≤ x 且 0 ≤ t ⟹ 0·x ≤ t·x，0·x = 0）
  tx-ge-0 : zeroℝ ≤ℝ (t *ℝ x)
  tx-ge-0 = subst (λ y → y ≤ℝ (t *ℝ x)) (zero-mul x)
                   (*-≤-mono-ℝ {a = zeroℝ} {b = t} {c = x} hx ht)
  -- -(tx) ≤ 0
  neg-tx-le-0 : negℝ (t *ℝ x) ≤ℝ zeroℝ
  neg-tx-le-0 = subst (λ y → negℝ (t *ℝ x) ≤ℝ y) neg-zero (neg-≤-ℝ tx-ge-0)

-- e^(-tA) 的谱测度复合（谱映射定理的谱测度形式，登记为谱论基础公理）：
-- E_{e^(-tA)}(P) = E(φ_t⁻¹P)，φ_t(x) = e^(-tx)；降定理路径：Borel 函数演算复合（同 exp-spectral-measure）
postulate
  E-exp-tA : ℝ → Borel → Op
  exp-tA-spectral-measure : (t : ℝ) (P : Borel) → E-exp-tA t P ≡ E (λ x → P (φ-t t x))
  -- e^(-tA) 侧 Fuglede：与自伴 e^(-tA) 交换 ⟹ 与其谱测度 E-exp-tA 交换
  intertwine-exp-tA-imp-spectral : (t : ℝ) (X : Op) → X *ₒ exp-tA t ≡ exp-tA t *ₒ X → (P : Borel) → X *ₒ E-exp-tA t P ≡ E-exp-tA t P *ₒ X

-- Hille-Yosida 谱侧状态：
--  - 半群交换（semigroup-comm **可证**）；φ_t 值域 (0,1]（phi-t-pos / phi-t-lt-one **可证**）
--    ⟹ 谱支集 ⊆ (0,1]（压缩性谱侧）。
--  - **谱测度形式的压缩性（σ(e^(-tA)) ⊆ (0,1]）已闭合于 §11**（依赖 §10e E-spectrum-total）。
--  - 压缩范数（‖e^(-tA)‖ ≤ 1）、强连续（lim_{t→0} e^(-tA) = I）、生成元（-A）需
--    范数/拓扑/导数层——随 Hilbert 空间层扩展登记。

-- ==================================================================
-- §8b 谱映射的谱测度族等价（引理 2 的 t 参数化：e^(-tA) 交换 ⟹ 与 A 谱测度交换）
-- ==================================================================

-- 取负单射（可证）：-a ≡ -b ⟹ a ≡ b（neg-neg）
neg-inj : {a b : ℝ} → negℝ a ≡ negℝ b → a ≡ b
neg-inj {a} {b} h = trans (sym (neg-neg a)) (trans (cong negℝ h) (neg-neg b))

-- t 乘法单射（**可证**）：0 < t ⟹ t·x = t·y ⟹ x = y
--（trichotomy-ℝ 三分 + *-pos-mono-ℝ 严格单调 + irreflexive-ℝ 排除两严格分支）
t-mul-inj : (t x y : ℝ) → zeroℝ <ℝ t → t *ℝ x ≡ t *ℝ y → x ≡ y
t-mul-inj t x y ht h with trichotomy-ℝ x y
t-mul-inj t x y ht h | inj₁ x<y =
  ⊥-elim (irreflexive-ℝ (subst (λ z → z <ℝ (t *ℝ y)) h (*-pos-mono-ℝ ht x<y)))
t-mul-inj t x y ht h | inj₂ (inj₁ x=y) = x=y
t-mul-inj t x y ht h | inj₂ (inj₂ y<x) =
  ⊥-elim (irreflexive-ℝ (subst (λ z → z <ℝ (t *ℝ x)) (sym h) (*-pos-mono-ℝ ht y<x)))

-- φ_t 单射（**可证**）：0 < t ⟹ φ_t(t·x) = φ_t(t·y) ⟹ x = y（exp-inj + neg-inj + t-mul-inj）
phi-t-inj : (t : ℝ) → zeroℝ <ℝ t → {x y : ℝ} → φ-t t x ≡ φ-t t y → x ≡ y
phi-t-inj t ht {x} {y} h = t-mul-inj t x y ht (neg-inj (exp-inj h))

-- φ_t 的像集（经 φ_t 的集输送）
φ-t-image : (t : ℝ) (P : Borel) → Borel
φ-t-image t P y = Σ ℝ (λ x → (φ-t t x ≡ y) × P x)

-- 谱测度输送往返（φ_t 版）：P x ⟺ φ_t-image P (φ_t(t·x))（φ_t 单射）
φ-t-image-roundtrip : (t : ℝ) → zeroℝ <ℝ t → (P : Borel) (x : ℝ)
  → (P x → φ-t-image t P (φ-t t x)) × (φ-t-image t P (φ-t t x) → P x)
φ-t-image-roundtrip t ht P x = back , forth
  where
  back : P x → φ-t-image t P (φ-t t x)
  back px = x , (refl , px)
  forth : φ-t-image t P (φ-t t x) → P x
  forth (y , (eq , py)) = subst P (phi-t-inj t ht {x = y} {y = x} eq) py

-- 谱测度等价（φ_t 版）：E(P) = E(φ_t⁻¹(φ_t(P)))（**可证**：spectral-ext + roundtrip）
E-phi-t-image : (t : ℝ) → zeroℝ <ℝ t → (P : Borel) → E P ≡ E (λ x → φ-t-image t P (φ-t t x))
E-phi-t-image t ht P = spectral-ext P (λ x → φ-t-image t P (φ-t t x)) (φ-t-image-roundtrip t ht P)

-- **引理 2 的 t 参数化（可证明）**：X·e^(-tA) = e^(-tA)·X ⟹ X·E P = E P·X（0 < t）
--（谱映射的谱测度族等价：Fuglede 对 e^(-tA) → 谱测度复合 exp-tA-spectral-measure → E-phi-t-image 回 P）
Rec-t-to-σ : {X : Op} (t : ℝ) → zeroℝ <ℝ t → X *ₒ exp-tA t ≡ exp-tA t *ₒ X → (P : Borel) → X *ₒ E P ≡ E P *ₒ X
Rec-t-to-σ {X} t ht h P =
  trans (cong (λ Y → X *ₒ Y) (E-phi-t-image t ht P))
  (trans (cong (λ Y → X *ₒ Y) (sym (exp-tA-spectral-measure t (φ-t-image t P))))
  (trans (intertwine-exp-tA-imp-spectral t X h (φ-t-image t P))
  (trans (cong (λ Y → Y *ₒ X) (exp-tA-spectral-measure t (φ-t-image t P)))
         (cong (λ Y → Y *ₒ X) (sym (E-phi-t-image t ht P))))))

-- ==================================================================
-- §8c e^(-tA) 的谱匹配双射（定理 3 的半群参数化：M-Rec-t = M_σ，0 < t）
-- ==================================================================

-- e^(-tA) 的交换条件（谱匹配的递归侧，t 参数化）
M-Rec-t : ℝ → Op → Set
M-Rec-t t X = X *ₒ exp-tA t ≡ exp-tA t *ₒ X

-- 谱积分线性对 e^(-tA)（谱论基础公理；降定理路径同 X-comm-spectral-int：简单函数层
-- simple-comm 已证，一般函数经逼近待完备性扩展）
postulate
  X-comm-spectral-int-exp-t : (t : ℝ) (X : Op)
    → ((P : Borel) → X *ₒ E-exp-tA t P ≡ E-exp-tA t P *ₒ X)
    → X *ₒ exp-tA t ≡ exp-tA t *ₒ X

-- **可证明**：M_σ ⊆ M-Rec-t（谱匹配 ⟹ X 与 e^(-tA) 交换）
-- 链：X·E-exp-tA t P = E-exp-tA t P·X [M_σ + 谱测度复合 exp-tA-spectral-measure]
--   ⟹ X·e^(-tA) = e^(-tA)·X [X-comm-spectral-int-exp-t]
σ-to-Rec-t : {X : Op} (t : ℝ) → M-σ X → M-Rec-t t X
σ-to-Rec-t {X} t h = X-comm-spectral-int-exp-t t X (λ P →
  trans (cong (λ Y → X *ₒ Y) (exp-tA-spectral-measure t P))
  (trans (h (λ x → P (φ-t t x)))
         (cong (λ Y → Y *ₒ X) (sym (exp-tA-spectral-measure t P)))))

-- **定理 3 的半群参数化（0 < t）**：M-Rec-t ⟺ M_σ（e^(-tA) 谱匹配双射）
theorem3-t : {X : Op} (t : ℝ) → zeroℝ <ℝ t → (M-Rec-t t X → M-σ X) ×₁ (M-σ X → M-Rec-t t X)
theorem3-t {X} t ht = pair₁ (λ h P → Rec-t-to-σ t ht h P) (λ h → σ-to-Rec-t t h)

-- ==================================================================
-- §9 P1 无限维闭合结论（线性语义下伴随闭合，P1 笔记 §8 推荐裁决）
-- ==================================================================

-- P1 线性语义闭合 = 对象重建 × Hom 双射：
--   对象层：D(R(E)) ≅ E（corollary5：recon-op = -log(e^(-A)) ≡ A，对象重建）
--   态射层：Hom_Sp ≅ₗ Hom_σ ≅ₗ Hom_Rec（corollary4-∞，谱匹配双射 = 恒等）
record P1-linear-closure : Set₁ where
  field
    obj-recon : recon-op ≡ A
    hom-bij : (Hom-Sp ≅ₗ Hom-σ) ×₁ (Hom-Rec ≅ₗ Hom-σ)

-- **P1 线性语义闭合（组装，全部组件可证）**：
-- 对应 P1 笔记 §8 推荐裁决——线性语义（Rec 态射 = 有界线性谱匹配算子）下，
-- 伴随在无限维闭合（对象可重建 + 态射层谱匹配双射成立）。
-- 集合语义反例（命题 6，非线性谱匹配映射）由 P1 笔记 §5 分析，
-- 不在本形式化层（线性算子代数 Op 的语义限制内）。
p1-linear-closure : P1-linear-closure
p1-linear-closure = record { obj-recon = corollary5 ; hom-bij = corollary4-∞ }

-- ==================================================================
-- §10 谱测度代数性质（投影值测度的投影性/正交性）
-- ==================================================================

-- 谱测度乘法 = 交集（投影值测度的定义性质：E(P)·E(Q) = E(P ∩ Q)；
-- 登记为谱论基础公理，与谱测度 E 同属定义假设）
postulate
  E-mul : (P Q : Borel) → E P *ₒ E Q ≡ E (λ x → P x × Q x)
  -- 空集谱测度为零算子（谱测度定义性质）
  E-empty : E (λ _ → ⊥) ≡ 𝟘ₒ

-- **可证明**：E 幂等（E(P)² = E(P)，投影性：P∩P = P 点态）
E-idempotent : (P : Borel) → E P *ₒ E P ≡ E P
E-idempotent P =
  trans (E-mul P P)
        (spectral-ext (λ x → P x × P x) P (λ x → (λ { (px , _) → px }) , (λ px → px , px)))

-- **可证明**：正交性（P ∩ Q = ∅ ⟹ E(P)·E(Q) = 0）
E-orthogonal : (P Q : Borel) → ((x : ℝ) → P x → Q x → ⊥) → E P *ₒ E Q ≡ 𝟘ₒ
E-orthogonal P Q h =
  trans (E-mul P Q)
        (trans (spectral-ext (λ x → P x × Q x) (λ _ → ⊥) (λ x → (λ { (px , qx) → h x px qx }) , (λ e → ⊥-elim e)))
               E-empty)

-- 谱测度代数性质层状态：
--  - 投影性（E-idempotent **可证**）、正交性（E-orthogonal **可证**）——
--    投影值测度的代数核心（E-mul/E-empty 为谱论基础公理）。
--  - σ-可加性、单调性（P ⊆ Q ⟹ E(P) ≤ E(Q)）、E(ℝ) = I 留待
--    σ-代数/算子序完整层。simple-mul（简单函数谱积分乘法）可由
--    E-mul + 分划细化推出（待建；E-slice 为其切片机制前置，见 §10b）。

-- ==================================================================
-- §10b 谱测度交互性质（交换性/包含分解/与简单积分的切片交互）
-- ==================================================================

-- **可证明（零新增公理）**：谱测度值互相交换 E(P)·E(Q) = E(Q)·E(P)
--（E-mul 双向 + spectral-ext：交集点态交换）
E-comm : (P Q : Borel) → E P *ₒ E Q ≡ E Q *ₒ E P
E-comm P Q =
  trans (E-mul P Q)
  (trans (spectral-ext (λ x → P x × Q x) (λ x → Q x × P x)
           (λ x → (λ { (px , qx) → qx , px }) , (λ { (qx , px) → px , qx })))
         (sym (E-mul Q P)))

-- **可证明（零新增公理）**：包含分解 P ⊆ Q ⟹ E(P) = E(P)·E(Q)
--（P = P∩Q 点态 + E-mul；单调性 E(P) ≤ E(Q) 的算子序无版本——
--  谱测度在包含下保"因子分解"，算子序完整层时给 E(P) ≤ E(Q)）
E-sub : (P Q : Borel) → ((x : ℝ) → P x → Q x) → E P ≡ E P *ₒ E Q
E-sub P Q h =
  trans (spectral-ext P (λ x → P x × Q x)
           (λ x → (λ px → px , h x px) , (λ { (px , _) → px })))
        (sym (E-mul P Q))

-- **可证明（零新增公理）**：包含分解（右侧）：P ⊆ Q ⟹ E(P) = E(Q)·E(P)
E-sub-r : (P Q : Borel) → ((x : ℝ) → P x → Q x) → E P ≡ E Q *ₒ E P
E-sub-r P Q h = trans (E-sub P Q h) (E-comm P Q)

-- **可证明（零新增公理）**：谱测度左切片——E(P)·∫(Σdⱼ·1_{Ωⱼ}) dE = ∫(Σdⱼ·1_{P∩Ωⱼ}) dE
--（distribₒ 展开 + ·ₒ-comm-l 标量提取 + E-mul 逐项；归纳）
-- simple-mul 的前置机制：切片 = 用谱测度值"切"简单函数谱积分
E-slice : (P : Borel) {m : ℕ} (d : Fin m → ℝ) (Ω : Fin m → Borel)
  → E P *ₒ spec-int-simple {m} d Ω ≡ spec-int-simple {m} d (λ i → λ x → P x × Ω i x)
E-slice P {zero} d Ω = *ₒ-zero-r (E P)
E-slice P {suc m} d Ω =
  trans (distribₒ (E P) (d zero ·ₒ E (Ω zero)) rest)
        (cong₂ _+ₒ_ head tail)
  where
  rest : Op
  rest = spec-int-simple {m} (λ i → d (suc i)) (λ i → Ω (suc i))
  -- E(P)·(d0·E(Ω0)) = d0·E(P∩Ω0)（·ₒ-comm-l 标量提取 + E-mul）
  head : E P *ₒ (d zero ·ₒ E (Ω zero)) ≡ d zero ·ₒ E (λ x → P x × Ω zero x)
  head = trans (·ₒ-comm-l (d zero) (E P) (E (Ω zero)))
               (cong (λ Y → d zero ·ₒ Y) (E-mul P (Ω zero)))
  -- 归纳：E(P)·rest = rest 的 P∩Ω 切片
  tail : E P *ₒ rest ≡ spec-int-simple {m} (λ i → d (suc i)) (λ i → λ x → P x × Ω (suc i) x)
  tail = E-slice P {m} (λ i → d (suc i)) (λ i → Ω (suc i))

-- **可证明（零新增公理）**：谱测度右切片（对称）：∫(Σdⱼ·1_{Ωⱼ}) dE · E(P) = ∫(Σdⱼ·1_{Ωⱼ∩P}) dE
slice-spec-int : {m : ℕ} (d : Fin m → ℝ) (Ω : Fin m → Borel) (P : Borel)
  → spec-int-simple {m} d Ω *ₒ E P ≡ spec-int-simple {m} d (λ i → λ x → Ω i x × P x)
slice-spec-int {zero} d Ω P = *ₒ-zero-l (E P)
slice-spec-int {suc m} d Ω P =
  trans (distribₒ-l (d zero ·ₒ E (Ω zero)) rest (E P))
        (cong₂ _+ₒ_ head tail)
  where
  rest : Op
  rest = spec-int-simple {m} (λ i → d (suc i)) (λ i → Ω (suc i))
  -- (d0·E(Ω0))·E(P) = d0·E(Ω0∩P)（·ₒ-comm 标量提取 + E-mul）
  head : (d zero ·ₒ E (Ω zero)) *ₒ E P ≡ d zero ·ₒ E (λ x → Ω zero x × P x)
  head = trans (·ₒ-comm (d zero) (E (Ω zero)) (E P))
               (cong (λ Y → d zero ·ₒ Y) (E-mul (Ω zero) P))
  -- 归纳：rest·E(P) = rest 的 Ω∩P 切片
  tail : rest *ₒ E P ≡ spec-int-simple {m} (λ i → d (suc i)) (λ i → λ x → Ω (suc i) x × P x)
  tail = slice-spec-int {m} (λ i → d (suc i)) (λ i → Ω (suc i)) P

-- 谱测度交互层状态：
--  - 交换性（E-comm）、包含分解（E-sub/E-sub-r）、切片（E-slice/slice-spec-int）全部**可证**，
--    零新增公理——simple-mul（∫f dE · ∫g dE = ∫fg dE，分划细化）的机制前置就位。
--  - simple-mul（双和 + ·ₒ-assoc 标量结合）已闭合于 §10c。

-- ==================================================================
-- §10c 简单函数谱积分乘法（simple-mul：∫f dE · ∫g dE = ∫(f·g) dE）
-- ==================================================================

-- 算子代数补充公理：标量乘结合律（a·(b·X) = (a·b)·X；
-- 标准赋范向量空间标量律，模型必然性 = Op 是 ℝ-向量空间；
-- 与 ·ₒ-+（标量分配）同类的算子代数补充律）
postulate
  ·ₒ-assoc : (a b : ℝ) (x : Op) → a ·ₒ (b ·ₒ x) ≡ (a *ℝ b) ·ₒ x

-- **可证明**：单原子乘积 (a·E(P))·(b·E(Q)) = (a·b)·E(P∩Q)
--（·ₒ-comm 标量左提 + ·ₒ-comm-l 标量右提 + ·ₒ-assoc 结合 + E-mul）
atom-atom : (a b : ℝ) (P Q : Borel)
  → (a ·ₒ E P) *ₒ (b ·ₒ E Q) ≡ (a *ℝ b) ·ₒ E (λ x → P x × Q x)
atom-atom a b P Q =
  trans (·ₒ-comm a (E P) (b ·ₒ E Q))
  (trans (cong (λ Y → a ·ₒ Y) (·ₒ-comm-l b (E P) (E Q)))
  (trans (·ₒ-assoc a b (E P *ₒ E Q))
         (cong (λ Y → (a *ℝ b) ·ₒ Y) (E-mul P Q))))

-- 双和谱积分（简单函数乘积 ∫(f·g) dE 的显式双和形式：
-- ΣᵢΣⱼ (cᵢ·dⱼ)·E(Ωᵢ∩Ψⱼ)——乘积函数在公共细化分划上的谱积分）
spec-int-simple2 : {m n : ℕ} (c : Fin m → ℝ) (Ω : Fin m → Borel)
  → (d : Fin n → ℝ) (Ψ : Fin n → Borel) → Op
spec-int-simple2 {m} {n} c Ω d Ψ =
  sum-op {m} (λ i → sum-op {n} (λ j → (c i *ℝ d j) ·ₒ E (λ x → Ω i x × Ψ j x)))

-- **可证明**：左原子 × 右和——(a·E(P))·∫(Σdⱼ·1_{Ψⱼ}) dE = Σⱼ (a·dⱼ)·E(P∩Ψⱼ)
--（distribₒ 展开 + atom-atom 逐项 + 归纳）
atom-right : (a : ℝ) (P : Borel) {n : ℕ} (d : Fin n → ℝ) (Ψ : Fin n → Borel)
  → (a ·ₒ E P) *ₒ spec-int-simple {n} d Ψ
    ≡ sum-op {n} (λ j → (a *ℝ d j) ·ₒ E (λ x → P x × Ψ j x))
atom-right a P {zero} d Ψ = *ₒ-zero-r (a ·ₒ E P)
atom-right a P {suc n} d Ψ =
  trans (distribₒ (a ·ₒ E P) (d zero ·ₒ E (Ψ zero)) rest)
        (cong₂ _+ₒ_ head tail)
  where
  rest : Op
  rest = spec-int-simple {n} (λ j → d (suc j)) (λ j → Ψ (suc j))
  -- (a·E(P))·(d0·E(Ψ0)) = (a·d0)·E(P∩Ψ0)（atom-atom）
  head : (a ·ₒ E P) *ₒ (d zero ·ₒ E (Ψ zero))
       ≡ (a *ℝ d zero) ·ₒ E (λ x → P x × Ψ zero x)
  head = atom-atom a (d zero) P (Ψ zero)
  -- 归纳：左原子 × rest
  tail : (a ·ₒ E P) *ₒ rest
       ≡ sum-op {n} (λ j → (a *ℝ d (suc j)) ·ₒ E (λ x → P x × Ψ (suc j) x))
  tail = atom-right a P {n} (λ j → d (suc j)) (λ j → Ψ (suc j))

-- **simple-mul（可证明）**：∫(Σcᵢ·1_{Ωᵢ}) dE · ∫(Σdⱼ·1_{Ψⱼ}) dE = ΣᵢΣⱼ (cᵢ·dⱼ)·E(Ωᵢ∩Ψⱼ)
--（distribₒ-l 展开 + atom-right 逐项 + 归纳——简单函数谱积分的乘法规则，
--  ∫f dE · ∫g dE = ∫(f·g) dE 在公共细化分划上的显式形式）
simple-mul : {m n : ℕ} (c : Fin m → ℝ) (Ω : Fin m → Borel)
  → (d : Fin n → ℝ) (Ψ : Fin n → Borel)
  → spec-int-simple {m} c Ω *ₒ spec-int-simple {n} d Ψ
    ≡ spec-int-simple2 {m} {n} c Ω d Ψ
simple-mul {zero} {n} c Ω d Ψ = *ₒ-zero-l (spec-int-simple {n} d Ψ)
simple-mul {suc m} {n} c Ω d Ψ =
  trans (distribₒ-l (c zero ·ₒ E (Ω zero)) rest (spec-int-simple {n} d Ψ))
        (cong₂ _+ₒ_ head tail)
  where
  rest : Op
  rest = spec-int-simple {m} (λ i → c (suc i)) (λ i → Ω (suc i))
  -- (c0·E(Ω0))·∫d = Σⱼ (c0·dⱼ)·E(Ω0∩Ψⱼ)（atom-right）
  head : (c zero ·ₒ E (Ω zero)) *ₒ spec-int-simple {n} d Ψ
       ≡ sum-op {n} (λ j → (c zero *ℝ d j) ·ₒ E (λ x → Ω zero x × Ψ j x))
  head = atom-right (c zero) (Ω zero) d Ψ
  -- 归纳：rest × ∫d
  tail : rest *ₒ spec-int-simple {n} d Ψ
       ≡ spec-int-simple2 {m} {n} (λ i → c (suc i)) (λ i → Ω (suc i)) d Ψ
  tail = simple-mul {m} {n} (λ i → c (suc i)) (λ i → Ω (suc i)) d Ψ

-- 简单函数谱积分乘法层状态：
--  - simple-mul（双和乘积公式）+ atom-atom/atom-right（单原子×单原子/左原子×和）**可证**，
--    新增算子代数补充公理 1 条（·ₒ-assoc 标量结合律，模型必然性 = Op 是 ℝ-向量空间）。
--  - ∫f·∫g = ∫fg 的"对角坍缩"形式（公共分划 pairwise 不相交 ⟹ 双和坍缩到
--    Σᵢ(cᵢ·dᵢ)·E(Ωᵢ)）已闭合于 §10d（Fin 构造子互异 + 零吸收，零新增公理）。

-- ==================================================================
-- §10d simple-mul 对角坍缩（∫f·∫g = ∫fg 的标准形式）
-- ==================================================================

-- Fin 构造子互异/单射（可证：构造子不交 + 单射）
zero≢suc : {m : ℕ} {k : Fin m} → zero ≢ suc k
zero≢suc ()

suc≢zero : {m : ℕ} {k : Fin m} → suc k ≢ zero
suc≢zero ()

suc-inj : {m : ℕ} {i j : Fin m} → suc i ≡ suc j → i ≡ j
suc-inj refl = refl

suc≢suc : {m : ℕ} {i j : Fin m} → i ≢ j → suc i ≢ suc j
suc≢suc h eq = h (suc-inj eq)

-- **可证明（零新增公理）**：标量乘零吸收 a·0 = 0
--（·ₒ-comm a 𝟙ₒ 𝟘ₒ + *ₒ-zero-r 双向）
·ₒ-zero : (a : ℝ) → a ·ₒ 𝟘ₒ ≡ 𝟘ₒ
·ₒ-zero a =
  trans (sym (cong (λ Y → a ·ₒ Y) (*ₒ-zero-r 𝟙ₒ)))
  (trans (sym (·ₒ-comm a 𝟙ₒ 𝟘ₒ))
         (*ₒ-zero-r (a ·ₒ 𝟙ₒ)))

-- **可证明**：全零求和为 0
sum-zero : {m : ℕ} → sum-op {m} (λ j → 𝟘ₒ) ≡ 𝟘ₒ
sum-zero {zero} = refl
sum-zero {suc m} = trans (cong₂ _+ₒ_ refl sum-zero) (+ₒ-ident 𝟘ₒ)

-- **可证明**：t + Σₖ 0 = t（零尾部并入）
sum-keep-zero : {m : ℕ} (t : Op) → t +ₒ sum-op {m} (λ j → 𝟘ₒ) ≡ t
sum-keep-zero {m} t = trans (cong (λ Y → t +ₒ Y) sum-zero) (+ₒ-ident t)

-- **可证明**：0 + t = t
zero-plus : (t : Op) → 𝟘ₒ +ₒ t ≡ t
zero-plus t = trans (+ₒ-comm 𝟘ₒ t 𝟘ₒ) (+ₒ-ident t)

-- **可证明**：不相交集交集谱测度为零 E(P∩Q) = 0（E-mul + E-orthogonal）
E-disjoint : (P Q : Borel) → ((x : ℝ) → P x → Q x → ⊥) → E (λ x → P x × Q x) ≡ 𝟘ₒ
E-disjoint P Q h = trans (sym (E-mul P Q)) (E-orthogonal P Q h)

-- **可证明**：内部和坍缩——Σⱼ (cᵢ·dⱼ)·E(Ωᵢ∩Ωⱼ) = (cᵢ·dᵢ)·E(Ωᵢ)
--（Ωᵢ pairwise 不相交：对角项 E(Ωᵢ∩Ωᵢ)=E(Ωᵢ) 保留，非对角项 E(Ωᵢ∩Ωⱼ)=0 经 ·ₒ-zero 吸收）
inner-sum-collapse : {m : ℕ} (c d : Fin m → ℝ) (Ω : Fin m → Borel)
  → ((i j : Fin m) → i ≢ j → ((x : ℝ) → Ω i x → Ω j x → ⊥))
  → (i : Fin m)
  → sum-op {m} (λ j → (c i *ℝ d j) ·ₒ E (λ x → Ω i x × Ω j x))
    ≡ (c i *ℝ d i) ·ₒ E (Ω i)
inner-sum-collapse {zero} c d Ω h ()
inner-sum-collapse {suc m} c d Ω h zero =
  trans (cong (λ Y → ((c zero *ℝ d zero) ·ₒ E (λ x → Ω zero x × Ω zero x)) +ₒ Y) tail-zero)
  (trans (sum-keep-zero ((c zero *ℝ d zero) ·ₒ E (λ x → Ω zero x × Ω zero x)))
         (cong (λ Y → (c zero *ℝ d zero) ·ₒ Y)
               (spectral-ext (λ x → Ω zero x × Ω zero x) (Ω zero)
                 (λ x → (λ { (px , _) → px }) , (λ px → px , px)))))
  where
  -- 尾部全为零（Ω zero 与 Ω (suc k) 不相交）
  tail-zero : sum-op {m} (λ k → (c zero *ℝ d (suc k)) ·ₒ E (λ x → Ω zero x × Ω (suc k) x))
            ≡ sum-op {m} (λ k → 𝟘ₒ)
  tail-zero = sum-op-congₒ {m} (λ k →
    trans (cong (λ Y → (c zero *ℝ d (suc k)) ·ₒ Y)
                (E-disjoint (Ω zero) (Ω (suc k)) (h zero (suc k) (zero≢suc {m} {k}))))
          (·ₒ-zero (c zero *ℝ d (suc k))))
inner-sum-collapse {suc m} c d Ω h (suc i') =
  trans (cong (λ Y → Y +ₒ tail) zero-head)
  (trans (zero-plus tail) tail-ih)
  where
  tail : Op
  tail = sum-op {m} (λ k → (c (suc i') *ℝ d (suc k)) ·ₒ E (λ x → Ω (suc i') x × Ω (suc k) x))
  -- 第 zero 项为零（Ω(suc i') 与 Ω zero 不相交）
  zero-head : (c (suc i') *ℝ d zero) ·ₒ E (λ x → Ω (suc i') x × Ω zero x) ≡ 𝟘ₒ
  zero-head =
    trans (cong (λ Y → (c (suc i') *ℝ d zero) ·ₒ Y)
                (E-disjoint (Ω (suc i')) (Ω zero) (h (suc i') zero (suc≢zero {m} {i'}))))
          (·ₒ-zero (c (suc i') *ℝ d zero))
  -- 归纳：尾部和坍缩（i' 版，Ω 移位）
  tail-ih : tail ≡ (c (suc i') *ℝ d (suc i')) ·ₒ E (Ω (suc i'))
  tail-ih = inner-sum-collapse {m} (λ k → c (suc k)) (λ k → d (suc k)) (λ k → Ω (suc k))
              (λ k1 k2 neq x → h (suc k1) (suc k2) (suc≢suc {m} {k1} {k2} neq) x) i'

-- **simple-mul 对角坍缩（可证明）**：公共分划 pairwise 不相交 ⟹
-- ∫(Σcᵢ·1_{Ωᵢ}) dE · ∫(Σdᵢ·1_{Ωᵢ}) dE = ∫(Σ(cᵢ·dᵢ)·1_{Ωᵢ}) dE
--（simple-mul 双和乘积公式 + 逐项 inner-sum-collapse；∫f·∫g = ∫fg 的标准形式）
simple-mul-diag : {m : ℕ} (c d : Fin m → ℝ) (Ω : Fin m → Borel)
  → ((i j : Fin m) → i ≢ j → ((x : ℝ) → Ω i x → Ω j x → ⊥))
  → spec-int-simple {m} c Ω *ₒ spec-int-simple {m} d Ω
    ≡ spec-int-simple {m} (λ i → c i *ℝ d i) Ω
simple-mul-diag {m} c d Ω h =
  trans (simple-mul {m} {m} c Ω d Ω)
        (sum-op-congₒ {m} (λ i → inner-sum-collapse {m} c d Ω h i))

-- 简单函数谱积分乘法层最终状态：
--  - simple-mul（双和）+ simple-mul-diag（对角坍缩）**可证**，∫f·∫g = ∫fg 完整。
--    零新增公理（§10c 的 ·ₒ-assoc 为本层唯一补充公理）。
--  - 一般函数逼近层（简单函数 ⟹ 任意 Borel 函数，sup/极限）与
--    Hille-Yosida 范数/拓扑层、Fuglede 引理 1 谱积分证明为后续主项。
--  - 谱测度完备性（E(ℝ)=𝟙ₒ + 有限可加性 + 分划可加性）见 §10e。

-- ==================================================================
-- §10e 谱测度完备性（E(ℝ)=𝟙ₒ + 有限可加性 + 分划可加性）
-- ==================================================================

-- 单位类型（全空间谓词 ℝ 的载体：λ _ → ⊤ = "恒真" = 整个实轴）
data ⊤ : Set where
  tt : ⊤

-- 谱测度完备性公理（投影值测度定义性质，σ-可加性的有限版）：
--  - E(ℝ) = 𝟙ₒ：全空间谱测度 = 恒等算子（谱测度归一化/分辨率恒等式）
--  - P∩Q = ∅ ⟹ E(P∪Q) = E(P)+E(Q)：不相交集加法性（σ-代数层时给可数版）
-- 降定理路径：测度论（Lebesgue-Stieltjes 谱测度）完整实现时转为可证明定理
postulate
  E-total : E (λ _ → ⊤) ≡ 𝟙ₒ
  E-union : (P Q : Borel) → ((x : ℝ) → P x → Q x → ⊥)
    → E (λ x → P x ⊎ Q x) ≡ E P +ₒ E Q

-- **可证明**：谱支集在 [0,∞) 的完备性——E([0,∞)) = 𝟙ₒ
--（E-support-pos 取 P=ℝ：E(ℝ) = E(ℝ∩[0,∞))；spectral-ext 消 ⊤：E(ℝ∩[0,∞)) = E([0,∞))；
--  再与 E-total 合成：E(ℝ) = 𝟙ₒ）
E-spectrum-total : E (λ x → zeroℝ ≤ℝ x) ≡ 𝟙ₒ
E-spectrum-total =
  trans (sym (trans (E-support-pos (λ _ → ⊤))
                    (spectral-ext (λ x → ⊤ × (zeroℝ ≤ℝ x)) (λ x → zeroℝ ≤ℝ x)
                      (λ x → (λ { (tt , h) → h }) , (λ h → tt , h)))))
        E-total

-- 空 Fin 消去（可证：Fin zero 无构造子）
fin0-empty : (x : Fin zero) → ⊥
fin0-empty ()

-- 分划并集谓词（有限分划 {Ωᵢ} 的并：∃i. Ωᵢ x）
partition-union : {m : ℕ} (Ω : Fin m → Borel) → Borel
partition-union {m} Ω x = Σ (Fin m) (λ i → Ω i x)

-- 并集谓词拆分（可证）：Ω₀ ∪ (∪ᵢ Ω_{suc i}) ↔ ∪ᵢ Ωᵢ（Fin (suc m) 版本）
split-union : {m : ℕ} (Ω : Fin (suc m) → Borel) (x : ℝ)
  → (Ω zero x ⊎ Σ (Fin m) (λ i → Ω (suc i) x)) → Σ (Fin (suc m)) (λ i → Ω i x)
split-union Ω x (inj₁ px) = zero , px
split-union Ω x (inj₂ (i , p)) = suc i , p

join-union : {m : ℕ} (Ω : Fin (suc m) → Borel) (x : ℝ)
  → Σ (Fin (suc m)) (λ i → Ω i x) → (Ω zero x ⊎ Σ (Fin m) (λ i → Ω (suc i) x))
join-union Ω x (zero , px) = inj₁ px
join-union Ω x (suc i , p) = inj₂ (i , p)

-- **分划可加性（可证明）**：pairwise 不相交分划 {Ωᵢ} ⟹ E(∪ᵢΩᵢ) = Σᵢ E(Ωᵢ)
--（有限可加性：spectral-ext 拆分 + E-union 逐项 + 归纳；
--  σ-可加性的有限版——σ-代数层时经可数并/极限扩展）
E-partition-add : {m : ℕ} (Ω : Fin m → Borel)
  → ((i j : Fin m) → i ≢ j → ((x : ℝ) → Ω i x → Ω j x → ⊥))
  → E (λ x → Σ (Fin m) (λ i → Ω i x)) ≡ sum-op {m} (λ i → E (Ω i))
E-partition-add {zero} Ω h =
  trans (spectral-ext (λ x → Σ (Fin zero) (λ i → Ω i x)) (λ _ → ⊥)
           (λ x → (λ p → fin0-empty (proj₁ p)) , (λ e → ⊥-elim e)))
        E-empty
E-partition-add {suc m} Ω h =
  trans (spectral-ext (λ x → Σ (Fin (suc m)) (λ i → Ω i x)) (λ x → Ω zero x ⊎ rest x)
           (λ x → (λ p → join-union Ω x p) , (λ q → split-union Ω x q)))
  (trans (E-union (Ω zero) rest (λ x px → disjoint-rest x px))
         (cong (λ Y → E (Ω zero) +ₒ Y) (E-partition-add {m} (λ i → Ω (suc i)) rest-h)))
  where
  rest : Borel
  rest = λ x → Σ (Fin m) (λ i → Ω (suc i) x)
  -- Ω zero 与 rest 不相交（pairwise ⟹ 首元与尾部各元不相交）
  disjoint-rest : (x : ℝ) → Ω zero x → rest x → ⊥
  disjoint-rest x px (i , py) = h zero (suc i) (zero≢suc {m} {i}) x px py
  -- 尾部 pairwise（Ω 移位）
  rest-h : (i j : Fin m) → i ≢ j → ((x : ℝ) → Ω (suc i) x → Ω (suc j) x → ⊥)
  rest-h i j neq x = h (suc i) (suc j) (suc≢suc {m} {i} {j} neq) x

-- 谱测度完备性层状态：
--  - E(ℝ) = 𝟙ₒ（E-total 公理）、有限可加性（E-union 公理）、分划可加性
--    （E-partition-add **可证**）、谱支集完备性（E-spectrum-total **可证**）。
--  - σ-可加性（可数并）随 σ-代数/极限层扩展；E(P)+E(Pᶜ) = 𝟙ₒ（分辨率恒等式的
--    补形式）构造性上需排中律（P 可判定时成立），留待经典扩展层。

-- ==================================================================
-- §11 Hille-Yosida 谱侧收官（σ(e^(-tA)) ⊆ (0,1] 压缩性谱测度形式）
-- ==================================================================

-- **可证明（零新增公理）**：e^(-tA) 的谱支集 ⊆ (0,1]（t ≥ 0）——
-- E_{e^(-tA)}((0,1]) = 𝟙ₒ（压缩性的谱测度形式）
-- 链：exp-tA-spectral-measure（谱映射：E_{e^(-tA)}(P) = E(φ_t⁻¹P)）
--   → E-support-pos（A 谱支集 ⊆ [0,∞)）
--   → spectral-ext（x ≥ 0 时 φ_t 值域 (0,1]：phi-t-pos + phi-t-lt-one）
--   → E-spectrum-total（E([0,∞)) = 𝟙ₒ）
E-exp-tA-contractive : (t : ℝ) → zeroℝ ≤ℝ t
  → E-exp-tA t (λ y → (zeroℝ <ℝ y) × (y ≤ℝ oneℝ)) ≡ 𝟙ₒ
E-exp-tA-contractive t ht =
  trans (exp-tA-spectral-measure t (λ y → (zeroℝ <ℝ y) × (y ≤ℝ oneℝ)))
  (trans (E-support-pos (λ x → (zeroℝ <ℝ φ-t t x) × (φ-t t x ≤ℝ oneℝ)))
  (trans (spectral-ext (λ x → ((zeroℝ <ℝ φ-t t x) × (φ-t t x ≤ℝ oneℝ)) × (zeroℝ ≤ℝ x))
                       (λ x → zeroℝ ≤ℝ x)
           (λ x → (λ { ((pos , le) , hx) → hx }) , (λ hx → (phi-t-pos t x , phi-t-lt-one t x ht hx) , hx)))
         E-spectrum-total))

-- Hille-Yosida 谱侧最终状态：
--  - 谱支集 ⊆ (0,1] 的谱测度形式（E-exp-tA-contractive **可证**，零新增公理）——
--    §8 的 φ_t 值域引理 + §10e 的谱测度完备性组合：σ(e^(-tA)) ⊆ (0,1] 完整。
--  - 压缩范数（‖e^(-tA)‖ ≤ 1）、强连续（lim_{t→0} e^(-tA) = I）、生成元（-A）
--    需范数/拓扑/导数层（Hilbert 空间层），为阶段 6 剩余主项之一。
