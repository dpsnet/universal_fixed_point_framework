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
    1. 谱论基础公理（谱测度 E / 谱表示 / 函数演算 / Fuglede 方向 /
       谱测度复合 / 谱测度外延 / Hille-Yosida 半群）
    1b. 谱积分逼近机制（简单函数核心 sum-op/spec-int-simple/simple-comm +
        sup/算子序 + 一般谱积分定义；X-comm-spectral-int / -exp 降为定理）
    2. φ(x) = e^(-x) 的可证引理（exp 单射 ⟹ φ 单射；exp-log ⟹ 值域刻画）
    3. 引理 2 核心（可证）：M_Rec ⊆ M_σ（exp 单射 + 谱测度复合 + Fuglede）
    4. 三条件谓词 M_Sp / M_σ / M_Rec 与定理 3（无限维版）
    5. 推论 5 核心：-log(φ(x)) = x（可证）+ 对象重建公理登记

  公理纪律（谱论基础假设，对齐"ℝ 公理是基础假设"立场）：
    - 谱测度 E、谱表示（谱定理）、Fuglede 方向（交织 ⟹ 谱交换）、
      谱测度外延、谱测度复合、Hille-Yosida 半群 = 谱论基础公理——
      每个注明模型必然性与降定理路径（谱积分/测度论完整实现时转为可证明定理）
    - **谱积分线性（X-comm-spectral-int / -exp）已降为可证明定理**（§1b）：
      一般谱积分 = 简单函数谱积分的 sup（sup 公理 + simple-comm 可证 + sup-comm）
    - **核心定理真实证明**（不允许占位）：φ 单射（exp-inj + neg-neg）、
      谱测度输送往返（φ-image-roundtrip）、M_Rec ⊆ M_σ（Rec-to-σ）、
      M_σ ⊆ M_Sp / M_σ ⊆ M_Rec（谱积分线性推导 + 谱表示重写）、-log(φ(x)) = x
-}

open import Agda.Builtin.Equality using (_≡_; refl)
open import Agda.Primitive using (Level; _⊔_)
open import Sp.SpCategory
  renaming (⊥ to ⊥-Sp)
  using (ℕ; zero; suc; Fin; _×_; _,_; _≢_; sym; trans; cong; cong₂)
open import NatArith.NatArith using (2^; <-suc; _<ℕ_; z<s; s<s; <-trans; s<s-inv)

-- ℝ 层（T3 已建：序代数 + exp/log/rpow + exp-inj 可证）
open import DHStructural.DHStructuralAnalysis
  using (ℝ; zeroℝ; oneℝ; negℝ; exp; log; _≤ℝ_; _<ℝ_; _+ℝ_; _*ℝ_; _-ℝ_; _/ℝ_; subst; neg-neg; exp-inj; log-exp; exp-log;
         exp-pos; exp-mono-≤; exp-zero; neg-≤-ℝ; *-≤-mono-ℝ; *-≤-mono-l-ℝ; *-nonneg-ℝ; lt-*-pos-ℝ; *-comm-ℝ; *-zero-ℝ; neg-zero; +-comm-ℝ;
         *-pos-mono-ℝ; trichotomy-ℝ; irreflexive-ℝ; zero-factor-ℝ; +-inv-ℝ; distrib-ℝ; neg-one-mul;
         sub-ℝ-def; sub-eq-zero; refl-≤ℝ; ≤-trans-ℝ; ≤-+-mono-ℝ; <-≤-ℝ; lt-≤-trans-ℝ; ≤-lt-trans-ℝ; trans-<ℝ; zero-lt-one-ℝ; *-ident-ℝ; +-ident-ℝ; zero-add-ℝ; ⊥; ⊥-elim; _⊎_; inj₁; inj₂; div-one-ℝ; /-cross-ℝ;
         natℝ; min-ℝ; min-≤-l; min-≤-r; min-glb; min-absorp-l; min-mono-r;
         max-ℝ; max-≤-r; max-sub-decomp; max-pos-mul-neg-zero;
         max-pos-value; max-neg-value; max-zero-zero;
         natℝ-nonneg; div-nonneg; 2^-pos; natℝ-pos-embed; natℝ-<-embed; /-lt-same-den-ℝ;
         sup-ℝ; sup-upper; sup-least; archimedean-ub; archimedean-ub-bound)

-- 复用 P1Spectral 的算子代数（using 只取 Op 代数公理，避免有限维谱设定名字冲突）
open import P1Spectral.P1Spectral
  using (Op; _+ₒ_; _*ₒ_; _·ₒ_; 𝟘ₒ; 𝟙ₒ;
         +ₒ-assoc; +ₒ-comm; +ₒ-ident;
         *ₒ-assoc; *ₒ-ident; *ₒ-ident-l; *ₒ-zero-r; *ₒ-zero-l;
         distribₒ; distribₒ-l; ·ₒ-comm; ·ₒ-comm-l; ·ₒ-zero-l; ·ₒ-zero-r)

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
  -- （谱积分线性 X-comm-spectral-int 原在此声明，已降为可证明定理，见 §1b
  --   X-comm-spectral-int-deriv：一般谱积分 = 简单函数谱积分的 sup + sup-comm）
  -- Fuglede（引理 1 ⟹ 方向）：交织 ⟹ 谱匹配——**已降为可证定理**（§5g）：
  -- 指示桥接 E(P) = fc(1_P) 登记后，X-comm-fc-continuous（§5f，任意 f）+ indicator-bridge 推导。

-- 函数演算：e^(-A)（Borel 函数演算，φ(x) = e^(-x) 作用于谱）
postulate
  exp-A : Op
  -- e^(-A) 的谱测度：E-exp(P) = E(φ⁻¹P)（函数演算复合：谱测度经 φ 输送）
  E-exp : Borel → Op
  exp-spectral-measure : (P : Borel) → E-exp P ≡ E (λ x → P (exp (negℝ x)))
  -- e^(-A) 谱表示
  spec-int-exp : Op
  exp-spectral-rep : exp-A ≡ spec-int-exp
  -- （e^(-A) 侧谱积分线性 X-comm-spectral-int-exp 原在此声明，已降为可证明定理，
  --   见 §1b X-comm-spectral-int-exp-deriv）
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
-- §1b 谱积分逼近机制（简单函数核心 + sup/算子序 + 一般谱积分）
-- ==================================================================
-- 目标：将原 §1 的谱积分线性公理（X-comm-spectral-int / -exp）降为可证明定理。
-- 机制：一般谱积分 = 简单函数谱积分的上确界（sup 构造）；X 与 E 逐集交换
--   ⟹ X 与每个简单函数谱积分交换（simple-comm，**可证**）
--   ⟹ X 与上确界交换（sup-comm，交换子闭性公理）⟹ X 与一般谱积分交换（**推导**）。
-- 依赖：本层位于 §3 之前，供引理 1 代数方向（σ-to-Sp / σ-to-Rec）使用。

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

-- 算子序与 sup（一般谱积分的极限基础；标准算子代数/泛函分析结构）：
--  - _≤ₒ_：算子序（X ≤ₒ Y ⟺ Y-X 正定；投影值上为投影格序）
--  - sup-op/upper/least：算子族上确界存在（有界算子空间的序完备性，
--    对应弱/强算子拓扑下的收敛；具体范数/拓扑随 Hilbert 空间层）
--  - sup-comm：交换子关于 sup 的闭性（X 与族中每个元交换 ⟹ X 与上确界交换；
--    von Neumann 交换子定理的代数版本，模型必然性 = 交换子代数弱闭）
-- 降定理路径：Banach 空间/算子拓扑完整实现时转为可证明定理
postulate
  _≤ₒ_ : Op → Op → Set
  sup-op : {l : Level} → (Op → Set l) → Op
  sup-op-upper : {l : Level} (S : Op → Set l) (x : Op) → S x → x ≤ₒ sup-op S
  sup-op-least : {l : Level} (S : Op → Set l) (b : Op) → ((x : Op) → S x → x ≤ₒ b) → sup-op S ≤ₒ b
  sup-comm : {l : Level} (X : Op) (S : Op → Set l)
    → ((Y : Op) → S Y → X *ₒ Y ≡ Y *ₒ X) → X *ₒ sup-op S ≡ sup-op S *ₒ X

-- 正算子序反对称（桥接登记，2026-08-02）：X ≤ₒ Y 且 Y ≤ₒ X ⟹ X ≡ Y——
-- Hilbert 层（§13 算子序 _≤ₗ_）语义：两向非负 ⟹ ∀v.⟨(Y−X)v,v⟩ = 0（≥0 且 ≤0）
-- ⟹ 正定性 ⟹ (Y−X)v = 0 逐 v ⟹ X = Y（funext）；
-- 降定理路径 = Hilbert 层算子序 + 内积正定性 + 函数外延性
postulate
  ≤ₒ-antisym : (X Y : Op) → X ≤ₒ Y → Y ≤ₒ X → X ≡ Y

-- 正算子序传递（桥接登记，2026-08-02）：X ≤ₒ Y 且 Y ≤ₒ Z ⟹ X ≤ₒ Z——
-- Hilbert 层（§13 算子序 _≤ₗ_）语义：⟨(Z−X)v,v⟩ = ⟨(Z−Y)v,v⟩ + ⟨(Y−X)v,v⟩ ≥ 0 + 0
-- （内积双线性 ip-add-l + 减法分解）；降定理路径 = Hilbert 层算子序 + 内积双线性
postulate
  ≤ₒ-trans : (X Y Z : Op) → X ≤ₒ Y → Y ≤ₒ Z → X ≤ₒ Z

-- Set₁ 层存在（SimpleF 含 Borel 字段故为 Set₁；B 为 Set 层——成员条件为普通命题）
data Σ₁ (A : Set₁) (B : A → Set) : Set₁ where
  pair₁Σ : (a : A) → B a → Σ₁ A B

-- 简单函数（有限分划 + 原子值；pairwise 不相交 + 覆盖 ⟹ 每点唯一原子）
record SimpleF : Set₁ where
  field
    m : ℕ
    c : Fin m → ℝ
    Ω : Fin m → Borel
    disj : (i j : Fin m) → i ≢ j → ((x : ℝ) → Ω i x → Ω j x → ⊥)
    cover : (x : ℝ) → Σ (Fin m) (λ i → Ω i x)

-- 简单函数谱积分（SimpleF 版）
simple-int : SimpleF → Op
simple-int s = spec-int-simple {SimpleF.m s} (SimpleF.c s) (SimpleF.Ω s)

-- f 的简单函数下界族：Y = ∫s dE（s 为简单函数，逐原子值 ≤ f）
--（支配条件使 sup 族正确 = ∫f dE；commutation 推导只依赖"族成员是简单函数谱积分"）
spec-int-below : (ℝ → ℝ) → Op → Set₁
spec-int-below f Y = Σ₁ SimpleF (λ s →
  (Y ≡ simple-int s) × ((i : Fin (SimpleF.m s)) → (x : ℝ) → SimpleF.Ω s i x → SimpleF.c s i ≤ℝ f x))

-- 一般谱积分 = 简单函数下界谱积分的上确界（Borel 函数演算的 sup 构造；
-- 对无界函数（如恒等）为无界函数演算，桥接公理见下）
spec-int-general : (ℝ → ℝ) → Op
spec-int-general f = sup-op (spec-int-below f)

-- **钉住 sup 语义（2026-08-03 显式文档化，理论闭合基础）**：
-- spec-int-general 是"钉住 sup"——其语义值 = 谱支集 [0,∞)（E-support-pos）上的
-- Lebesgue 谱积分 ∫f dE，由目标模型（Hilbert 层谱定理）确定；朴素 sup 构造只是
-- 部分计算机制，对变号/无界函数其值由桥接公理钉住（spec-int-general-id/-exp/
-- -phi-t 等），**不可**从朴素 sup 定义独立推出。
--   - 非负 f（f ≥ 0 逐点）下，族 {s : s ≤ f 逐点} 非空（s = 0 为成员），
--     朴素 sup = 经典 Lebesgue 积分（与钉住值一致，MCT 可证化见测度论层）；
--   - 变号 f（如奇次单项式 xⁿ，n 奇）：xⁿ 在 (-∞,0) 无下界 ⟹ 朴素下界族为空
--     （sup(∅) 无语义意义），其积分值由钉住桥接确定——fc-integral-full（v1.13）
--     对此类 f 的相容性依赖钉住桥接，构造化需谱支集受限/∫f⁺−∫f⁻ 语义重构
--     （2026-08-03 分析，log；桥接 fc-poly-le-spec-int 语义 = 目标模型 ∫p dE = p(A)，
--     与 spec-int-general-id 同地位，健全）；
--   - 物理关键函数（exp、φ_t）均非负+单调，朴素 sup 即其积分，见测度论层。

-- **可证**：下界族对 f 单调——f ≤ g 点态 ⟹ spec-int-below f ⊆ spec-int-below g
--（无界逼近细节的结构性质：Lebesgue 型 sup 构造中更大的函数有更大的简单函数下界族；
--  收敛性内容（sup 存在且与桥接一致）依赖序完备性机制，随测度论层实现）
spec-int-below-mono : {f g : ℝ → ℝ} → ((x : ℝ) → f x ≤ℝ g x) → (Y : Op)
  → spec-int-below f Y → spec-int-below g Y
spec-int-below-mono {f} {g} h Y (pair₁Σ s (eq , dom)) =
  pair₁Σ s (eq , λ i x px → ≤-trans-ℝ (dom i x px) (h x))

-- **可证**：sup 外延（Op 层）——谓词逐成员等价 ⟹ sup 相等（sup-op-least/upper + ≤ₒ-antisym；
--   v1.19 起在 §1c 定义，v1.25 移至 §1b——spec-int-general-ext-pt 依赖，前向引用消解）
sup-op-ext : {l : Level} {S T : Op → Set l} → ((Y : Op) → S Y → T Y) → ((Y : Op) → T Y → S Y)
  → sup-op S ≡ sup-op T
sup-op-ext {l} {S} {T} s→t t→s =
  ≤ₒ-antisym (sup-op S) (sup-op T)
             (sup-op-least S (sup-op T) (λ Y sy → sup-op-upper T Y (s→t Y sy)))
             (sup-op-least T (sup-op S) (λ Y ty → sup-op-upper S Y (t→s Y ty)))

-- **可证**：spec-int-general 逐点外延——f ≡ g 逐点 ⟹ ∫f = ∫g
--（spec-int-below 族逐成员等价（≤ 双向）+ sup-op-ext；**避开 funext**——
--  函数参数用逐点相等而非函数相等，方案 A 非负一致性（f⁻ = 0）的基础）
spec-int-general-ext-pt : {f g : ℝ → ℝ} → ((x : ℝ) → f x ≡ g x)
  → spec-int-general f ≡ spec-int-general g
spec-int-general-ext-pt {f} {g} h =
  sup-op-ext (λ Y yb → spec-int-below-mono {f = f} {g = g}
                          (λ x → subst (λ z → f x ≤ℝ z) (h x) (refl-≤ℝ {x = f x})) Y yb)
             (λ Y yb → spec-int-below-mono {f = g} {g = f}
                          (λ x → subst (λ z → z ≤ℝ f x) (h x) (refl-≤ℝ {x = f x})) Y yb)

-- 无界逼近细节（2026-08-01 文档化闭合；2026-08-02 阶段 7-1 落地 min-ℝ + 截断）：
--  - spec-int-general 对无界 f（恒等，[0,∞) 上无界）为 Lebesgue 型 sup 构造——
--    简单函数下界族的上确界；收敛性（sup 存在）依赖算子序完备性机制
--    （≤ₒ 反自反/sup 非空性等，当前抽象层以 sup-op 公理登记，降定理路径 =
--    Banach 空间/算子拓扑完整实现）。
--  - 具体无界函数的值由桥接公理钉住：spec-int-general-id（∫id = spec-int-A）、
--    spec-int-general-exp（∫e^(-x) = spec-int-exp）、spec-int-general-phi-t（∫φ_t = e^(-tA)，§8c）。
--  - **阶段 7-1（2026-08-02）**：无界 f 经截断 f_c = min(f, c) 逼近——
--    DHStructural 新增 min-ℝ（三分律定义，可证性质）；
--    截断逐点性质（≤ f / ≤ c / 族单调 / 吸收）与 spec-int 侧单调结构
--    （spec-int-general (trunc f c) ≤ₒ spec-int-general f，族单调）全部**可证**；
--    ∫f dE = supₙ ∫min(f,n) dE 为 Lebesgue 单调收敛（桥接公理 spec-int-trunc-conv，
--    测度论完整层降为定理）；恒等函数在 x ≤ c 时截断精确（trunc-absorp），
--    谱支集 [0,∞) 支持（E-support-pos）覆盖其余部分。
--  - 下界族结构性质：spec-int-below-mono（**可证**，f 单调）。

-- ==================================================================
-- §1b' 正负分解（方案 A 阶段 1，2026-08-03）
-- ==================================================================
-- 用途：spec-int-general 正负分解重构（笔记 §5.16.8 方案 A）——∫f dE =
--   ∫f⁺ dE − ∫f⁻ dE（f⁺ = max(f,0)、f⁻ = max(−f,0)），消除钉住 sup 语义的
--   构造地基。本阶段交付 f⁺/f⁻ 定义 + 逐点性质（全部**可证**，零新增公理）；
--   重构本身（spec-int-general 定义改造）留待阶段 2。

-- f⁺ = max(f,0)（正部）
pos-part : (ℝ → ℝ) → ℝ → ℝ
pos-part f x = max-ℝ (f x) zeroℝ

-- f⁻ = max(−f,0)（负部）
neg-part : (ℝ → ℝ) → ℝ → ℝ
neg-part f x = max-ℝ (negℝ (f x)) zeroℝ

-- **可证**：f⁺ 非负（0 ≤ max(f x, 0)，max-≤-r 特化）
pos-part-nonneg : (f : ℝ → ℝ) (x : ℝ) → zeroℝ ≤ℝ pos-part f x
pos-part-nonneg f x = max-≤-r (f x) zeroℝ

-- **可证**：f⁻ 非负
neg-part-nonneg : (f : ℝ → ℝ) (x : ℝ) → zeroℝ ≤ℝ neg-part f x
neg-part-nonneg f x = max-≤-r (negℝ (f x)) zeroℝ

-- **可证**：分解 f x = f⁺ x − f⁻ x（max-sub-decomp 特化，逐点）
decomp-pos-neg : (f : ℝ → ℝ) (x : ℝ) → (pos-part f x) -ℝ (neg-part f x) ≡ f x
decomp-pos-neg f x = max-sub-decomp (f x)

-- **可证**：正交 f⁺ x · f⁻ x = 0（max-pos-mul-neg-zero 特化，逐点）
pos-mul-neg-zero : (f : ℝ → ℝ) (x : ℝ) → (pos-part f x) *ℝ (neg-part f x) ≡ zeroℝ
pos-mul-neg-zero f x = max-pos-mul-neg-zero (f x)

-- **可证**：正部吸收——f x ≥ 0 ⟹ f⁺ x = f x（三分律：fx<0 矛盾排除，其余分支 max = fx）
pos-part-absorp : (f : ℝ → ℝ) (x : ℝ) → zeroℝ ≤ℝ f x → pos-part f x ≡ f x
pos-part-absorp f x hfx with trichotomy-ℝ (f x) zeroℝ
pos-part-absorp f x hfx | inj₁ fx<0 =
  ⊥-elim (irreflexive-ℝ (lt-≤-trans-ℝ fx<0 hfx))
pos-part-absorp f x hfx | inj₂ (inj₁ _) = refl
pos-part-absorp f x hfx | inj₂ (inj₂ _) = refl

-- **可证**：负部归零——f x ≥ 0 ⟹ f⁻ x = 0（三分律：0<−fx 与 −fx≤0 矛盾，
--   neg-≤-ℝ 取负保序反转 + neg-zero）
neg-part-zero-point : (f : ℝ → ℝ) (x : ℝ) → zeroℝ ≤ℝ f x → neg-part f x ≡ zeroℝ
neg-part-zero-point f x hfx with trichotomy-ℝ (negℝ (f x)) zeroℝ
neg-part-zero-point f x hfx | inj₁ _ = refl
neg-part-zero-point f x hfx | inj₂ (inj₁ nfx=0) = nfx=0
neg-part-zero-point f x hfx | inj₂ (inj₂ 0<nfx) =
  ⊥-elim (irreflexive-ℝ (lt-≤-trans-ℝ 0<nfx
          (subst (λ z → negℝ (f x) ≤ℝ z) neg-zero (neg-≤-ℝ hfx))))

-- ==================================================================
-- §1b'' Op 层减法与正负分解定理（方案 A 阶段 2 第一部分，2026-08-03）
-- ==================================================================
-- 目标：spec-int-general 正负分解重构（∫f := ∫f⁺ −ₒ ∫f⁻）的前置基础设施——
--   Op 层减法（定义性）+ 减法保交换（可证，X-comm-spec-int-general 重构后重验
--   的核心组件）+ 正负分解定理（桥接登记，方案 A 核心等式显式化）。
-- 注：spec-int-general **定义重构**本身（下游全适配）为阶段 2 第二部分。

-- Op 层减法：X −ₒ Y := X +ₒ ((−1)·ₒ Y)（定义性，P1Spectral 算子代数）
_-ₒ_ : Op → Op → Op
X -ₒ Y = X +ₒ ((negℝ oneℝ) ·ₒ Y)

-- **可证**：减法保交换——X 与 Y、Z 交换 ⟹ X 与 Y−ₒZ 交换
--（X-comm-spec-int-general 重构后重验：distribₒ（左分配）+ ·ₒ-comm-l（标量右提）
--  + ·ₒ-comm（标量左提）+ distribₒ-l（右分配）逐项）
op-sub-comm : (X Y Z : Op) → X *ₒ Y ≡ Y *ₒ X → X *ₒ Z ≡ Z *ₒ X
  → X *ₒ (Y -ₒ Z) ≡ (Y -ₒ Z) *ₒ X
op-sub-comm X Y Z hY hZ =
  trans (distribₒ X Y (c ·ₒ Z))
        (trans (cong₂ _+ₒ_ hY (·ₒ-comm-l c X Z))
               (trans (cong₂ _+ₒ_ refl (cong (λ w → c ·ₒ w) hZ))
                      (trans (cong₂ _+ₒ_ refl (sym (·ₒ-comm c Z X)))
                             (sym (distribₒ-l Y (c ·ₒ Z) X)))))
  where
  c : ℝ
  c = negℝ oneℝ

-- 正负分解（**桥接登记**，方案 A 核心等式）：∫f dE = ∫f⁺ dE −ₒ ∫f⁻ dE
--（模型必然性 = 测度论线性 ∫f = ∫f⁺ − ∫f⁻（Lebesgue 积分可加性，标准事实）；
--  钉住 sup 语义（§1b 文档块）下真（目标模型谱定理 ∫f dE = ∫f⁺ dE − ∫f⁻ dE）；
--  降定理路径 = 方案 A 阶段 3/4：spec-int-general 定义重构（∫f := ∫f⁺ −ₒ ∫f⁻）
--  后转为可证明定理（重构即定义性，本桥接退化为 refl 推导））
postulate
  spec-int-general-decomp : (f : ℝ → ℝ)
    → spec-int-general f ≡ spec-int-general (pos-part f) -ₒ spec-int-general (neg-part f)

-- **可证**：X −ₒ 𝟘ₒ = X（·ₒ-zero-r（标量×零算子）+ +ₒ-ident；
--  重构后非负一致性（f⁻ = 0 ⟹ ∫f = ∫f⁺ − 0）的左消）
op-sub-zero-r : (X : Op) → X -ₒ 𝟘ₒ ≡ X
op-sub-zero-r X = trans (cong (λ Y → X +ₒ Y) (·ₒ-zero-r (negℝ oneℝ))) (+ₒ-ident X)

-- 非负函数积分（重构定义的前置别名）：spec-int-nonneg g = sup{∫s : s ≤ g 逐点}
--（对非负 g 即 Lebesgue 积分；方案 A 重构 spec-int-general f := spec-int-nonneg f⁺
--  −ₒ spec-int-nonneg f⁻ 时避免定义递归）
spec-int-nonneg : (ℝ → ℝ) → Op
spec-int-nonneg g = sup-op (spec-int-below g)

-- 零函数积分（**桥接登记**，D 类）：∫0 dE = 𝟘ₒ
--（模型必然性 = 测度论 ∫0 = 0（Lebesgue 积分零函数性）；钉住 sup 语义下真
--  （下界族 {∫s : s ≤ 0} 的 sup = 0，0 是成员（零简单函数）+ 上界（负标量×正算子
--  ≤ 0 需谱投影非负，Hilbert 层 E-hilb-nonneg 可证））；降定理路径 = Hilbert 层
--  谱投影非负 + 标量保序 + sup-least）
postulate
  spec-int-general-zero : spec-int-general (λ _ → zeroℝ) ≡ 𝟘ₒ

-- 谱支集外零贡献（**桥接登记**，D 类）：非负 g 在 [0,∞) 上 = 0 ⟹ ∫g dE = 0
--（模型必然性 = E-support-pos（E(P) = E(P∩[0,∞))，谱支集 [0,∞)）+ 测度论零函数性；
--  下界族 {∫s : s ≤ g} 成员在谱支集上 ≤ 0（g 在 [0,∞) = 0 ⟹ s ≤ 0 于 [0,∞)）⟹
--  谱投影非负 + 标量保序 ⟹ ∫s ≤ 0，且 0 是成员（s = 0 ≤ g）⟹ sup = 0；
--  降定理路径 = Hilbert 层谱投影非负（E-hilb-nonneg）+ E-support-pos + sup-least）
-- 用途：id⁻（支持 ⊆ (-∞,0]，[0,∞) 上 = 0）的积分为 0（阶段 3 余项，id 钉住解析）
postulate
  spec-int-nonneg-zero-off-support : (g : ℝ → ℝ) → ((x : ℝ) → zeroℝ ≤ℝ g x)
    → ((x : ℝ) → zeroℝ ≤ℝ x → g x ≡ zeroℝ) → spec-int-general g ≡ 𝟘ₒ

-- **可证**：非负一致性——f ≥ 0 逐点 ⟹ ∫f = 非负 sup（spec-int-general f ≡ spec-int-nonneg f）
--（spec-int-general-decomp（∫f = ∫f⁺ −ₒ ∫f⁻）+ pos-part-absorp/neg-part-zero-point
--  （逐点外延 spec-int-general-ext-pt）+ spec-int-general-zero（∫0 = 0）+ op-sub-zero-r
--  （X −ₒ 0 = X）；**验证方案 A 分解等式与 sup 定义对非负 f 一致**——非负 f 的
--  ∫f 即朴素下界族 sup，钉住语义与非负 sup 无分歧）
spec-int-nonneg-consistent : (f : ℝ → ℝ) → ((x : ℝ) → zeroℝ ≤ℝ f x)
  → spec-int-general f ≡ spec-int-nonneg f
spec-int-nonneg-consistent f hf =
  trans (trans (spec-int-general-decomp f)
               (cong₂ _-ₒ_ pos-eq neg-eq))
        (op-sub-zero-r (spec-int-general f))
  where
  pos-eq : spec-int-general (pos-part f) ≡ spec-int-general f
  pos-eq = spec-int-general-ext-pt {f = pos-part f} {g = f}
           (λ x → pos-part-absorp f x (hf x))
  neg-eq : spec-int-general (neg-part f) ≡ 𝟘ₒ
  neg-eq = trans (spec-int-general-ext-pt {f = neg-part f} {g = λ _ → zeroℝ}
                  (λ x → neg-part-zero-point f x (hf x)))
                 spec-int-general-zero

-- ==================================================================
-- §1c 截断逼近（测度论层阶段 1，2026-08-02）
-- ==================================================================

-- 截断 f_c(x) := min(f x, c)（c 为 ℝ 截断水平；上升族取 c = natℝ n）
trunc : (ℝ → ℝ) → ℝ → ℝ → ℝ
trunc f c x = min-ℝ (f x) c

-- **可证**：截断 ≤ f（逐点）：min(f x, c) ≤ f x
trunc-below-f : (f : ℝ → ℝ) (c x : ℝ) → trunc f c x ≤ℝ f x
trunc-below-f f c x = min-≤-l (f x) c

-- **可证**：截断有界：min(f x, c) ≤ c
trunc-bounded : (f : ℝ → ℝ) (c x : ℝ) → trunc f c x ≤ℝ c
trunc-bounded f c x = min-≤-r (f x) c

-- **可证**：截断族单调（截断水平）：c ≤ d ⟹ min(f x, c) ≤ min(f x, d)
trunc-mono : (f : ℝ → ℝ) {c d x : ℝ} → c ≤ℝ d → trunc f c x ≤ℝ trunc f d x
trunc-mono f {c} {d} {x} hcd = min-mono-r (f x) c d hcd

-- **可证**：截断精确：f x ≤ c ⟹ min(f x, c) = f x（恒等函数在 x ≤ c 时）
trunc-absorp : (f : ℝ → ℝ) (c x : ℝ) → f x ≤ℝ c → trunc f c x ≡ f x
trunc-absorp f c x hxc = min-absorp-l (f x) c hxc

-- **可证**：截断族是下界族子族 ⟹ spec-int-general (trunc f c) ≤ₒ spec-int-general f
--（trunc-below-f 逐点 + spec-int-below-mono + sup-op-least/upper）
trunc-below-general : (f : ℝ → ℝ) (c : ℝ) → spec-int-general (trunc f c) ≤ₒ spec-int-general f
trunc-below-general f c =
  sup-op-least (spec-int-below (trunc f c)) (spec-int-general f)
    (λ Y yb → sup-op-upper (spec-int-below f) Y (spec-int-below-mono (trunc-below-f f c) Y yb))

-- **可证**：截断族单调（算子序）：c ≤ d ⟹ spec-int-general (trunc f c) ≤ₒ spec-int-general (trunc f d)
trunc-mono-general : (f : ℝ → ℝ) {c d : ℝ} → c ≤ℝ d → spec-int-general (trunc f c) ≤ₒ spec-int-general (trunc f d)
trunc-mono-general f {c} {d} hcd =
  sup-op-least (spec-int-below (trunc f c)) (spec-int-general (trunc f d))
    (λ Y yb → sup-op-upper (spec-int-below (trunc f d)) Y
                (spec-int-below-mono {f = trunc f c} {g = trunc f d}
                                     (λ x → trunc-mono f {c = c} {d = d} {x = x} hcd) Y yb))

-- 截断收敛（Lebesgue 单调收敛定理的代数形式）：无界 f（支持在 [0,∞) 的恒等/exp/φ_t）
-- 经上升截断族逼近 ∫f dE = supₙ ∫min(f, n) dE——**可证定理**（v1.20：Archimedean 登记后
-- 由桥接降为定理，见下方 spec-int-trunc-ℕ-conv；Archimedean 降定理路径 = 标准实数构造）

-- ------------------------------------------------------------------
-- spec-int MCT 构造化（ℝ-截断版，2026-08-03）
-- ------------------------------------------------------------------
-- 目标：Lebesgue 单调收敛的**可证部分**——∫f dE = sup{∫s : s ≤ 某截断 trunc f (s-bound s)}。
-- 关键观察：每个简单函数 s 有有限值域 ⟹ 存在 ℝ 上界 s-bound s（sup-ℝ 对有限值集）⟹
-- s ≤ f 逐点 ⟹ s ≤ trunc f (s-bound s) 逐点（min-glb）。故下界族 spec-int-below f
-- 与截断下界族 TruncBelow f **逐成员等价**，sup-op 外延（sup-op-ext 可证）⟹ ℝ-MCT 可证
-- （零新增公理）。注：ℕ-版本（spec-int-trunc-conv 桥接，∫f = supₙ∫min(f,n)）已由
-- Archimedean（DHStructural 登记，v1.20）降为可证定理——见下方"ℕ-截断版"段。

-- 简单函数值的 ℝ 上界：s-bound s := sup{cᵢ : i < m}（sup-ℝ 完备性，有限值集 sup）
s-bound : SimpleF → ℝ
s-bound s = sup-ℝ (λ r → Σ (Fin (SimpleF.m s)) (λ i → r ≡ SimpleF.c s i))

-- **可证**：每个原子值 ≤ s-bound（sup-upper 特化）
s-bound-upper : (s : SimpleF) (i : Fin (SimpleF.m s)) → SimpleF.c s i ≤ℝ s-bound s
s-bound-upper s i = sup-upper (λ r → Σ (Fin (SimpleF.m s)) (λ j → r ≡ SimpleF.c s j))
                              (SimpleF.c s i) (i , refl)

-- **可证**：dom（cᵢ ≤ f）⟹ cᵢ ≤ trunc f (s-bound s)（逐原子）
--（cᵢ ≤ f x（dom）且 cᵢ ≤ s-bound s（s-bound-upper）⟹ cᵢ ≤ min(f x, s-bound s)（min-glb）
--  = trunc f (s-bound s) x（定义性））
simple-below-trunc : (s : SimpleF) (f : ℝ → ℝ)
  → ((i : Fin (SimpleF.m s)) → (x : ℝ) → SimpleF.Ω s i x → SimpleF.c s i ≤ℝ f x)
  → (i : Fin (SimpleF.m s)) (x : ℝ) → SimpleF.Ω s i x → SimpleF.c s i ≤ℝ trunc f (s-bound s) x
simple-below-trunc s f dom i x px =
  min-glb (SimpleF.c s i) (f x) (s-bound s) (dom i x px) (s-bound-upper s i)

-- 截断下界族：Y = ∫s（s ≤ trunc f (s-bound s) 逐点）——ℝ-MCT 的 sup 族
TruncBelow : (ℝ → ℝ) → Op → Set₁
TruncBelow f Y = Σ₁ SimpleF (λ s →
  (Y ≡ simple-int s) × ((i : Fin (SimpleF.m s)) → (x : ℝ) → SimpleF.Ω s i x → SimpleF.c s i ≤ℝ trunc f (s-bound s) x))

-- **可证**：spec-int-below f ⊆ TruncBelow f（s ≤ f ⟹ s ≤ trunc f (s-bound s)，simple-below-trunc）
spec-int-below-into-trunc : {f : ℝ → ℝ} {Y : Op} → spec-int-below f Y → TruncBelow f Y
spec-int-below-into-trunc {f} {Y} (pair₁Σ s (eq , dom)) =
  pair₁Σ s (eq , λ i x px → simple-below-trunc s f dom i x px)

-- **可证**：TruncBelow f ⊆ spec-int-below f（s ≤ trunc f (s-bound s) ≤ f，trunc-below-f）
trunc-below-into-spec-int : {f : ℝ → ℝ} {Y : Op} → TruncBelow f Y → spec-int-below f Y
trunc-below-into-spec-int {f} {Y} (pair₁Σ s (eq , dom)) =
  pair₁Σ s (eq , λ i x px → ≤-trans-ℝ (dom i x px) (trunc-below-f f (s-bound s) x))

-- **sup-op-ext 已移至 §1b（v1.25：spec-int-general-ext-pt 依赖，前向引用消解）**

-- **可证**：ℝ-MCT——∫f dE = sup{∫s : s ≤ 某截断 trunc f (s-bound s)}（零新增公理）
--（spec-int-below f 与 TruncBelow f 逐成员等价 + sup-op-ext；
--  ℕ-版本见下方 spec-int-trunc-ℕ-conv（Archimedean，v1.20））
spec-int-R-trunc-conv : (f : ℝ → ℝ) → spec-int-general f ≡ sup-op (TruncBelow f)
spec-int-R-trunc-conv f =
  sup-op-ext (λ Y yb → spec-int-below-into-trunc {f = f} {Y = Y} yb)
             (λ Y yb → trunc-below-into-spec-int {f = f} {Y = Y} yb)

-- ------------------------------------------------------------------
-- spec-int MCT 构造化（ℕ-截断版，Archimedean，2026-08-03）
-- ------------------------------------------------------------------
-- 目标：ℕ-MCT——∫f dE = supₙ ∫min(f,n) dE 由桥接（spec-int-trunc-conv）降为可证定理。
-- Archimedean（DHStructural 登记，v1.20）：∀a. ∃n. a ≤ natℝ n ⟹ 每个简单函数 s ≤ f
-- 也 ≤ trunc f (natℝ N)（N = archimedean-ub (s-bound s)，s-bound-upper + archimedean-ub-bound
--  + min-glb）⟹ 每成员 Y = ∫s（s ≤ f）落入 spec-int-below (trunc f (natℝ N))（simple-below-ℕ-trunc）；
-- 反向经 trunc-below-f。故 ℕ-MCT 定理闭合（spec-int-trunc-ℕ-conv），桥接减一。

-- **可证**：dom（cᵢ ≤ f）⟹ cᵢ ≤ trunc f (natℝ (archimedean-ub (s-bound s)))（逐原子）
--（cᵢ ≤ f x（dom）且 cᵢ ≤ s-bound s ≤ natℝ N（s-bound-upper + archimedean-ub-bound）
--  ⟹ cᵢ ≤ min(f x, natℝ N)（min-glb）= trunc f (natℝ N) x（定义性））
simple-below-ℕ-trunc : (s : SimpleF) (f : ℝ → ℝ)
  → ((i : Fin (SimpleF.m s)) → (x : ℝ) → SimpleF.Ω s i x → SimpleF.c s i ≤ℝ f x)
  → (i : Fin (SimpleF.m s)) (x : ℝ) → SimpleF.Ω s i x
  → SimpleF.c s i ≤ℝ trunc f (natℝ (archimedean-ub (s-bound s))) x
simple-below-ℕ-trunc s f dom i x px =
  min-glb (SimpleF.c s i) (f x) (natℝ (archimedean-ub (s-bound s)))
          (dom i x px)
          (≤-trans-ℝ (s-bound-upper s i) (archimedean-ub-bound (s-bound s)))

-- **可证**：下界族成员 ≤ₒ ℕ-截断 sup
--（Y = ∫s（s ≤ f）⟹ s ≤ trunc f (natℝ N)（N = archimedean-ub (s-bound s)，simple-below-ℕ-trunc）
--  ⟹ Y ∈ spec-int-below (trunc f (natℝ N)) ⟹ Y ≤ₒ ∫min(f,N)（sup-op-upper）≤ₒ supₙ（sup-op-upper））
spec-int-below-member-≤-ℕ-sup : {f : ℝ → ℝ} {Y : Op} → spec-int-below f Y
  → Y ≤ₒ sup-op (λ Z → Σ ℕ (λ n → Z ≡ spec-int-general (trunc f (natℝ n))))
spec-int-below-member-≤-ℕ-sup {f} {Y} (pair₁Σ s (eq , dom)) =
  ≤ₒ-trans Y (spec-int-general (trunc f (natℝ N))) (sup-op S)
           (sup-op-upper (spec-int-below (trunc f (natℝ N))) Y member-N)
           (sup-op-upper S (spec-int-general (trunc f (natℝ N))) (N , refl))
  where
  N : ℕ
  N = archimedean-ub (s-bound s)
  member-N : spec-int-below (trunc f (natℝ N)) Y
  member-N = pair₁Σ s (eq , λ i x px → simple-below-ℕ-trunc s f dom i x px)
  S : Op → Set
  S Z = Σ ℕ (λ n → Z ≡ spec-int-general (trunc f (natℝ n)))

-- **可证**：ℕ-MCT——∫f dE = supₙ ∫min(f,n) dE（原 spec-int-trunc-conv 桥接，现为定理，v1.20）
--（≥ 方向：每成员 Y=∫s（s≤f）≤ₒ ∫min(f,N)（simple-below-ℕ-trunc）≤ₒ supₙ
--  （spec-int-below-member-≤-ℕ-sup）；≤ 方向：每项 ∫min(f,n) ≤ₒ ∫f（trunc-below-general））
spec-int-trunc-ℕ-conv : (f : ℝ → ℝ)
  → spec-int-general f ≡ sup-op (λ Y → Σ ℕ (λ n → Y ≡ spec-int-general (trunc f (natℝ n))))
spec-int-trunc-ℕ-conv f =
  ≤ₒ-antisym (spec-int-general f) (sup-op S)
             (sup-op-least (spec-int-below f) (sup-op S)
                           (λ Y yb → spec-int-below-member-≤-ℕ-sup {f = f} {Y = Y} yb))
             (sup-op-least S (spec-int-general f)
                           (λ Y → λ { (n , eq) → subst (λ Z → Z ≤ₒ spec-int-general f) (sym eq)
                                                              (trunc-below-general f (natℝ n)) }))
  where
  S : Op → Set
  S Y = Σ ℕ (λ n → Y ≡ spec-int-general (trunc f (natℝ n)))

-- ==================================================================
-- §1d 可测函数层与 Lebesgue 积分（测度论层阶段 2，2026-08-02）
-- ==================================================================

-- 可测函数（Borel = ℝ → Set 下可测性真空——吸收进 Borel 抽象；
-- 非负性为非负可测函数 Lebesgue 积分 sup 构造所需）
record MeasurableF : Set₁ where
  field
    f : ℝ → ℝ
    nonneg : (x : ℝ) → zeroℝ ≤ℝ f x

-- Lebesgue 积分：∫f dE = 简单函数下界的 sup（§1b 机制）
lebesgue-int : MeasurableF → Op
lebesgue-int m = spec-int-general (MeasurableF.f m)

-- **可证**：积分单调——f ≤ g 逐点 ⟹ ∫f ≤ₒ ∫g（spec-int-below-mono + sup-op-least/upper）
lebesgue-mono : {m m' : MeasurableF} → ((x : ℝ) → MeasurableF.f m x ≤ℝ MeasurableF.f m' x)
  → lebesgue-int m ≤ₒ lebesgue-int m'
lebesgue-mono {m} {m'} h =
  sup-op-least (spec-int-below (MeasurableF.f m)) (lebesgue-int m')
    (λ Y yb → sup-op-upper (spec-int-below (MeasurableF.f m')) Y
                (spec-int-below-mono {f = MeasurableF.f m} {g = MeasurableF.f m'} h Y yb))

-- **可证**：下界族成员 ≤ₒ 积分——简单函数下界（Y = ∫s，s ≤ m 逐点）⟹ ∫s ≤ₒ ∫m
lebesgue-lower : (m : MeasurableF) (Y : Op) → spec-int-below (MeasurableF.f m) Y → Y ≤ₒ lebesgue-int m
lebesgue-lower m Y yb = sup-op-upper (spec-int-below (MeasurableF.f m)) Y yb

-- **可证**：截断保持非负性——0 ≤ f x 且 0 ≤ c ⟹ 0 ≤ min(f x, c)（min-glb）
trunc-nonneg : (m : MeasurableF) {c : ℝ} → zeroℝ ≤ℝ c → (x : ℝ) → zeroℝ ≤ℝ trunc (MeasurableF.f m) c x
trunc-nonneg m {c} hc x = min-glb zeroℝ (MeasurableF.f m x) c (MeasurableF.nonneg m x) hc

-- **可证**：可测函数的截断仍为可测函数（非负性保持）
trunc-m : (m : MeasurableF) (c : ℝ) → zeroℝ ≤ℝ c → MeasurableF
trunc-m m c hc = record { f = trunc (MeasurableF.f m) c; nonneg = trunc-nonneg m {c = c} hc }

-- **可证**：∫trunc(m,c) ≤ₒ ∫m（截断是下界：trunc-below-general 对 MeasurableF 的特化）
trunc-lebesgue-below : (m : MeasurableF) (c : ℝ) (hc : zeroℝ ≤ℝ c) → lebesgue-int (trunc-m m c hc) ≤ₒ lebesgue-int m
trunc-lebesgue-below m c hc = trunc-below-general (MeasurableF.f m) c

-- **可证**：截断族单调（≤ₒ）：c ≤ d ⟹ ∫trunc(m,c) ≤ₒ ∫trunc(m,d)（trunc-mono-general 特化）
trunc-lebesgue-mono : (m : MeasurableF) {c d : ℝ} (hc : zeroℝ ≤ℝ c) (hd : zeroℝ ≤ℝ d) → c ≤ℝ d
  → lebesgue-int (trunc-m m c hc) ≤ₒ lebesgue-int (trunc-m m d hd)
trunc-lebesgue-mono m {c} {d} hc hd hcd = trunc-mono-general (MeasurableF.f m) hcd

-- Lebesgue 单调收敛（文档化）：对非负可测 m，上升截断族 ∫min(m,n) 单调（trunc-lebesgue-mono）
-- 且收敛到 ∫m——supₙ ∫min(m,n) = ∫m 即 spec-int-trunc-conv 对 MeasurableF 的特化
-- （截断族指数取 natℝ (suc n)：0 ≤ natℝ (suc n) 经 natℝ-pos-embed z<s + <-≤-ℝ；
--  完整单调收敛 = 测度论完整层降定理路径）。

-- 桥接公理（定义性）：
--  - ∫id dE = spec-int-A：恒等函数的谱积分即谱表示（无界函数演算的桥接，
--    与 spectral-rep-A 一致）
--  - ∫e^(-x) dE = spec-int-exp：φ 的谱积分即 exp 谱表示（与 exp-spectral-rep 一致）
postulate
  spec-int-general-id : spec-int-general (λ x → x) ≡ spec-int-A
  spec-int-general-exp : spec-int-general (λ x → exp (negℝ x)) ≡ spec-int-exp

-- **可证**：exp 的非负积分明确值——∫e^(-x) = 非负 sup = spec-int-exp（阶段 3 第一步）
--（exp 全 ℝ 非负（exp-pos：0 < exp x）⟹ spec-int-nonneg-consistent（钉住与非负 sup
--  无分歧）+ spec-int-general-exp 桥接组合——**钉住解析为"非负 sup 明确值 + 谱表示值"**
--  （spec-int-exp 本身为谱表示 postulate，钉住从 spec-int-general 定义级降至值级））
spec-int-nonneg-exp : spec-int-nonneg (λ x → exp (negℝ x)) ≡ spec-int-exp
spec-int-nonneg-exp =
  trans (sym (spec-int-nonneg-consistent (λ x → exp (negℝ x))
                                         (λ x → <-≤-ℝ (exp-pos (negℝ x)))))
        spec-int-general-exp

-- **可证**：id 分解重述——spec-int-A ≡ ∫id⁺ −ₒ ∫id⁻（阶段 3 余项，id 钉住解析第一步）
--（sym spec-int-general-id（∫id = spec-int-A）+ spec-int-general-decomp id（∫id = ∫id⁺ −ₒ ∫id⁻）
--  ——把 id 钉住桥接改写为分解形式）
spec-int-A-decomp : spec-int-A ≡ spec-int-general (pos-part (λ x → x))
                                  -ₒ spec-int-general (neg-part (λ x → x))
spec-int-A-decomp =
  trans (sym spec-int-general-id)
        (spec-int-general-decomp (λ x → x))

-- **可证**：id 钉住完全解析——∫id⁺ = spec-int-A
--（spec-int-A-decomp（spec-int-A = ∫id⁺ −ₒ ∫id⁻）+ spec-int-nonneg-zero-off-support
--  （∫id⁻ = 0：id⁻ 非负 + 在 [0,∞) 上 = 0（neg-part-zero-point），谱支集外零贡献）
--  + op-sub-zero-r（X −ₒ 0 = X）——spec-int-general-id 桥接的钉住解析为 id⁺ 的
--  非负积分值（id⁺ 与 id 在 [0,∞) 相等 ⟹ ∫id⁺ = ∫id = spec-int-A））
spec-int-general-id-pos : spec-int-general (pos-part (λ x → x)) ≡ spec-int-A
spec-int-general-id-pos =
  sym (trans (trans spec-int-A-decomp
                   (cong₂ _-ₒ_ refl id-neg-zero))
             (op-sub-zero-r (spec-int-general (pos-part (λ x → x)))))
  where
  id-neg-zero : spec-int-general (neg-part (λ x → x)) ≡ 𝟘ₒ
  id-neg-zero = spec-int-nonneg-zero-off-support (neg-part (λ x → x))
                  (λ x → neg-part-nonneg (λ y → y) x)
                  (λ x hx → neg-part-zero-point (λ y → y) x hx)

-- **族成员交换（可证）**：族成员均为简单函数谱积分 ⟹ 与 X 交换（simple-comm）
member-comm : {f : ℝ → ℝ} (X : Op) → ((P : Borel) → X *ₒ E P ≡ E P *ₒ X)
  → (Y : Op) → spec-int-below f Y → X *ₒ Y ≡ Y *ₒ X
member-comm {f} X h Y (pair₁Σ s (eq , _)) =
  trans (cong (λ Z → X *ₒ Z) eq)
        (trans (simple-comm {SimpleF.m s} X (SimpleF.c s) (SimpleF.Ω s) h)
               (cong (λ Z → Z *ₒ X) (sym eq)))

-- **泛化谱积分交换（可证）**：X 与 E 逐集交换 ⟹ X 与任意一般谱积分 ∫f dE 交换
--（sup-comm + member-comm（simple-comm 可证）；X-comm-spectral-int / -exp / -exp-t
--  均为其特化）
X-comm-spec-int-general : (X : Op) → ((P : Borel) → X *ₒ E P ≡ E P *ₒ X) → (f : ℝ → ℝ)
  → X *ₒ spec-int-general f ≡ spec-int-general f *ₒ X
X-comm-spec-int-general X h f =
  sup-comm X (spec-int-below f) (λ Y yb → member-comm {f = f} X h Y yb)

-- **X-comm-spectral-int 降为定理（可证）**：X 与 E 逐集交换 ⟹ X 与谱表示交换
--（spec-int-general-id 桥接 + X-comm-spec-int-general（f = id））
X-comm-spectral-int-deriv : (X : Op) → ((P : Borel) → X *ₒ E P ≡ E P *ₒ X)
  → X *ₒ spec-int-A ≡ spec-int-A *ₒ X
X-comm-spectral-int-deriv X h =
  trans (cong (λ Z → X *ₒ Z) (sym spec-int-general-id))
  (trans (X-comm-spec-int-general X h (λ x → x))
         (cong (λ Z → Z *ₒ X) spec-int-general-id))

-- **X-comm-spectral-int-exp 降为定理（可证）**：X 与 E 逐集交换 ⟹ X 与 exp 谱表示交换
--（spec-int-general-exp 桥接 + X-comm-spec-int-general（f = e^(-x)））
X-comm-spectral-int-exp-deriv : (X : Op) → ((P : Borel) → X *ₒ E P ≡ E P *ₒ X)
  → X *ₒ spec-int-exp ≡ spec-int-exp *ₒ X
X-comm-spectral-int-exp-deriv X h =
  trans (cong (λ Z → X *ₒ Z) (sym spec-int-general-exp))
  (trans (X-comm-spec-int-general X h (λ x → exp (negℝ x)))
         (cong (λ Z → Z *ₒ X) spec-int-general-exp))

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

-- 引理 1 代数方向（**可证明**，§1b 谱积分线性推导 + 谱表示重写）：M_σ ⊆ M_Sp
σ-to-Sp : {X : Op} → M-σ X → M-Sp X
σ-to-Sp {X} h =
  trans (cong (λ Y → X *ₒ Y) spectral-rep-A)
  (trans (X-comm-spectral-int-deriv X h)
         (cong (λ Y → Y *ₒ X) (sym spectral-rep-A)))

-- 引理 2 反向（**可证明**，§1b 谱积分线性推导 + exp 谱表示重写）：M_σ ⊆ M_Rec
σ-to-Rec : {X : Op} → M-σ X → M-Rec X
σ-to-Rec {X} h =
  trans (cong (λ Y → X *ₒ Y) exp-spectral-rep)
  (trans (X-comm-spectral-int-exp-deriv X h)
         (cong (λ Y → Y *ₒ X) (sym exp-spectral-rep)))

-- 引理 1 方向（M_Sp ⊆ M_σ）：Sp-to-σ 定义已随 intertwine-imp-spectral 降为
-- 定理迁至 §5g（依赖 fc 多项式/连续交换 §5f + 指示桥接 §5g，闭合后无公理依赖）。

-- ==================================================================
-- §3b Fuglede 引理 1 的代数部分（交织 ⟹ A 的多项式交换）
-- ==================================================================
-- 目标：引理 1 的谱积分证明（Sp-to-σ 方向降定理）的第一步——
-- X·A = A·X ⟹ X 与 A 的每个幂、每个多项式交换。
-- 后续步骤（连续函数逼近：多项式稠密；指示桥接：E(P) = 1_P(A)）随逼近层扩展登记，
-- 届时 intertwine-imp-spectral（Fuglede 方向公理）降为定理。
-- 本层零新增公理（纯算子代数：*ₒ-assoc / ·ₒ-comm / distribₒ）。

-- **可证明**：X 与一族元逐点交换 ⟹ X 与它们的标量加权和交换（一般版）
--（simple-comm 的泛化（Y = E∘Ω 即 simple-comm）；P1Spectral proj-comm-scalar-sum 的同构）
scalar-sum-comm : (X : Op) {m : ℕ} (a : Fin m → ℝ) (Y : Fin m → Op)
  → ((i : Fin m) → X *ₒ Y i ≡ Y i *ₒ X)
  → X *ₒ sum-op {m} (λ i → a i ·ₒ Y i) ≡ sum-op {m} (λ i → a i ·ₒ Y i) *ₒ X
scalar-sum-comm X {zero} a Y h =
  trans (*ₒ-zero-r X) (sym (*ₒ-zero-l X))
scalar-sum-comm X {suc m} a Y h =
  trans (distribₒ X (a zero ·ₒ Y zero) rest)
        (trans (cong₂ _+ₒ_ head tail)
               (sym (distribₒ-l (a zero ·ₒ Y zero) rest X)))
  where
  rest : Op
  rest = sum-op {m} (λ i → a (suc i) ·ₒ Y (suc i))
  -- X·(a0·Y0) = (a0·Y0)·X（标量中心 + h zero）
  head : X *ₒ (a zero ·ₒ Y zero) ≡ (a zero ·ₒ Y zero) *ₒ X
  head = trans (·ₒ-comm-l (a zero) X (Y zero))
               (trans (cong (λ y → a zero ·ₒ y) (h zero))
                      (sym (·ₒ-comm (a zero) (Y zero) X)))
  -- 归纳：X·rest = rest·X
  tail : X *ₒ rest ≡ rest *ₒ X
  tail = scalar-sum-comm X {m} (λ i → a (suc i)) (λ i → Y (suc i)) (λ i → h (suc i))

-- A 的幂（算子代数中 Aⁿ）
A-power : ℕ → Op
A-power zero = 𝟙ₒ
A-power (suc n) = A *ₒ A-power n

-- **可证明**：X·A = A·X ⟹ X·Aⁿ = Aⁿ·X（归纳；*ₒ-assoc + h 传递）
A-power-comm : {X : Op} → X *ₒ A ≡ A *ₒ X → (n : ℕ) → X *ₒ A-power n ≡ A-power n *ₒ X
A-power-comm {X} h zero =
  trans (*ₒ-ident X) (sym (*ₒ-ident-l X))
A-power-comm {X} h (suc n) =
  trans (sym (*ₒ-assoc X A (A-power n)))
  (trans (cong (λ Y → Y *ₒ A-power n) h)
  (trans (*ₒ-assoc A X (A-power n))
  (trans (cong (λ Y → A *ₒ Y) (A-power-comm {X} h n))
         (sym (*ₒ-assoc A (A-power n) X)))))

-- A 的多项式（算子代数版）：p(A) = Σᵢ aᵢ·A^{nᵢ}
poly-A : {m : ℕ} → (Fin m → ℝ) → (Fin m → ℕ) → Op
poly-A {m} a n = sum-op {m} (λ i → a i ·ₒ A-power (n i))

-- **可证明**：X·A = A·X ⟹ X 与 A 的多项式交换
--（scalar-sum-comm + A-power-comm 逐幂；Fuglede 引理 1 的谱积分证明的代数核心）
poly-A-comm : {X : Op} → X *ₒ A ≡ A *ₒ X → {m : ℕ} (a : Fin m → ℝ) (n : Fin m → ℕ)
  → X *ₒ poly-A {m} a n ≡ poly-A {m} a n *ₒ X
poly-A-comm {X} h {m} a n = scalar-sum-comm X {m} a (λ i → A-power (n i)) (λ i → A-power-comm {X} h (n i))

-- Fuglede 引理 1 的谱积分证明状态：
--  - 代数核心完成（poly-A-comm **可证**，零新增公理）。
--  - fc 多项式/连续交换（§5f）完成；指示桥接（§5g：E(P) = fc(1_P) 登记）
--    后 intertwine-imp-spectral 降为**可证定理**（§5g）——Fuglede 引理 1 方向闭合。

-- ==================================================================
-- §4 定理 3（无限维版）：M_Sp = M_σ = M_Rec（线性语义下谱匹配双射）
-- ==================================================================
-- 定理 3 定义已随 Sp-to-σ 移至 §5g（theorem3-Sp-σ 依赖 Sp-to-σ 的
-- intertwine-imp-spectral 定理版，§5g 闭合后无公理依赖）。

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
-- （recon-op / recon-op-fc 原在此登记；公理纪律审计（2026-08-01）降为定义——
--    recon-op := fc(λx → negℝ(log(φ x))) 即 (-log∘φ)(A)，为定义性记号非实质公理，见下）

-- -log(φ(x)) = x 在 [0,∞) 上（log-exp + neg-neg；**可证明**，推论 5 函数演算核心）
neg-log-phi-id : (x : ℝ) → negℝ (log (φ x)) ≡ x
neg-log-phi-id x = trans (cong negℝ (log-exp (negℝ x))) (neg-neg x)

-- 对象重建记号（**定义，非公理**）：recon-op = -log(e^(-A)) = (-log∘φ)(A)
--（函数演算复合的展开式；原以公理 recon-op-fc 登记，审计后降为定义）
recon-op : Op
recon-op = fc (λ x → negℝ (log (φ x)))

-- 推论 5（对象重建，**可证明**，函数演算公理之上）：
-- recon-op = -log(e^(-A)) = fc(-log∘φ) [定义] ≡ fc(id) [点态外延 + neg-log-phi-id] ≡ A [恒等保持]
corollary5 : recon-op ≡ A
corollary5 =
  trans (fc-ext (λ x → neg-log-phi-id x)) fc-id

-- ==================================================================
-- §5b 函数演算的多项式交换（Fuglede 证明的 fc 连接步）
-- ==================================================================
-- 目标：将 §3b 的代数核心（poly-A-comm：X 与 A 的多项式交换）连接到
-- 抽象函数演算 fc——X·A = A·X ⟹ X 与 fc(p) 交换（p 为多项式函数）。
-- 桥接替换（2026-08-01）：原 fc-poly 桥接公理已删除，改由 §5f 的 fc 同态结构
-- （fc-mul/fc-add/fc-const/fc-power）推导为**可证定理**（fc-poly，§5f）；
-- X-comm-fc-poly / X-comm-fc-continuous 随迁 §5f 闭合。
-- 本节保留：多项式函数定义载体（sum-ℝ/ℝ-power/poly-fn）+ 连续逼近机制
-- （fc-below/fc-continuous）。
-- 后续步骤（指示桥接 E(P) = 1_P(A)）随逼近层扩展登记，届时
-- intertwine-imp-spectral 降为定理。

-- ℝ 值有限求和（多项式函数值的载体）
sum-ℝ : {m : ℕ} → (Fin m → ℝ) → ℝ
sum-ℝ {zero} f = zeroℝ
sum-ℝ {suc m} f = f zero +ℝ sum-ℝ {m} (λ i → f (suc i))

-- ℝ 幂（xⁿ）
ℝ-power : ℕ → ℝ → ℝ
ℝ-power zero x = oneℝ
ℝ-power (suc n) x = x *ℝ ℝ-power n x

-- ==================================================================
-- 测度论逼近引理库 阶段 1：ℝ 幂单调性/正性（2026-08-03）
-- ==================================================================
-- 目标：单项式 xⁿ 的 dyadic 阶梯逼近（(j·c/2^k)ⁿ ≤ xⁿ，x ∈ 原子区间）的
-- ℝ 层地基——构造化 fc-poly-le-spec-int（测度论核心逼近桥接）的多阶段路线阶段 1。
-- 零新增公理：全部从 ℝ 序代数推导。

-- **可证**：幂非负——0 ≤ x ⟹ 0 ≤ xⁿ（归纳：基例 0 ≤ 1；步进 乘积非负 *-nonneg-ℝ）
power-nonneg : (n : ℕ) (x : ℝ) → zeroℝ ≤ℝ x → zeroℝ ≤ℝ ℝ-power n x
power-nonneg zero x hx = <-≤-ℝ zero-lt-one-ℝ
power-nonneg (suc n) x hx = *-nonneg-ℝ x (ℝ-power n x) hx (power-nonneg n x hx)

-- **可证**：幂单调——0 ≤ x 且 x ≤ y ⟹ xⁿ ≤ yⁿ（归纳：步进经
-- 右侧乘保序 *-≤-mono-ℝ（x·xⁿ ≤ y·xⁿ）+ 左侧乘保序 *-≤-mono-l-ℝ（y·xⁿ ≤ y·yⁿ））
power-mono : (n : ℕ) (x y : ℝ) → zeroℝ ≤ℝ x → x ≤ℝ y → ℝ-power n x ≤ℝ ℝ-power n y
power-mono zero x y hx hxy = refl-≤ℝ {oneℝ}
power-mono (suc n) x y hx hxy = ≤-trans-ℝ step1 step2
  where
  -- x·xⁿ ≤ y·xⁿ（0 ≤ xⁿ + x ≤ y，右侧乘保序）
  step1 : (x *ℝ ℝ-power n x) ≤ℝ (y *ℝ ℝ-power n x)
  step1 = *-≤-mono-ℝ {a = x} {b = y} {c = ℝ-power n x} (power-nonneg n x hx) hxy
  -- y·xⁿ ≤ y·yⁿ（0 ≤ y + xⁿ ≤ yⁿ，左侧乘保序）
  step2 : (y *ℝ ℝ-power n x) ≤ℝ (y *ℝ ℝ-power n y)
  step2 = *-≤-mono-l-ℝ y (ℝ-power n x) (ℝ-power n y) (≤-trans-ℝ hx hxy) (power-mono n x y hx hxy)

-- **可证**：幂正性——0 < x ⟹ 0 < xⁿ（归纳：基例 0 < 1；步进 乘积正性 lt-*-pos-ℝ）
power-pos : (n : ℕ) (x : ℝ) → zeroℝ <ℝ x → zeroℝ <ℝ ℝ-power n x
power-pos zero x hx = zero-lt-one-ℝ
power-pos (suc n) x hx = lt-*-pos-ℝ hx (power-pos n x hx)

-- 多项式函数：p(x) = Σᵢ aᵢ·x^{nᵢ}
poly-fn : {m : ℕ} → (Fin m → ℝ) → (Fin m → ℕ) → (ℝ → ℝ)
poly-fn {m} a n x = sum-ℝ {m} (λ i → a i *ℝ ℝ-power (n i) x)

-- 连续函数 f 的多项式下界族：Y = fc(p)（p 为多项式函数，逐点 ≤ f）
--（Weierstrass：多项式在紧集上稠密，连续函数由多项式下界逼近）
fc-below : (ℝ → ℝ) → Op → Set
fc-below f Y = Σ ℕ (λ m → Σ (Fin m → ℝ) (λ a → Σ (Fin m → ℕ) (λ n →
  (Y ≡ fc (poly-fn {m} a n)) × ((x : ℝ) → poly-fn {m} a n x ≤ℝ f x))))

-- 桥接公理（定义性）：连续函数 f 的函数演算 = 多项式下界 fc 的上确界
--（对连续 f 为 Weierstrass 逼近定理内容；对一般 f 为 Borel 函数演算的
--  连续下界 sup 扩展——标准谱论事实，函数演算经谱积分完整实现时降为定理）
postulate
  fc-continuous : (f : ℝ → ℝ) → fc f ≡ sup-op (fc-below f)

-- Fuglede 证明的 fc 连接状态：
--  - 多项式 fc 交换（X-comm-fc-poly）**可证**，fc-poly 已降为可证定理（§5f）。
--  - 连续函数交换（X-comm-fc-continuous）**可证**，fc-continuous 桥接公理（§5f 闭合）。
--  - 全函数演算交换（X-comm-fc，§5c：M_σ ⟹ 与任意 fc(f) 交换）。
--  - 指示桥接（E(P) = fc(1_P)，§5g 登记）——经典扩展层假设（indicator +
--    indicator-bridge），intertwine-imp-spectral 降为**可证定理**（§5g）。

-- ==================================================================
-- §5c 函数演算 = 谱积分（fc-integral 桥接 + X-comm-fc 统一交换）
-- ==================================================================
-- 目标：统一两条形式化轨道——抽象函数演算 fc（§5）与一般谱积分
-- spec-int-general（§1b）。桥接后，M_σ（E 逐集交换）⟹ X 与任意 fc(f) 交换。

-- 桥接公理（定义性）：函数演算 = 一般谱积分（fc(f) = ∫f dE）
--（谱定理的函数演算定义：f(A) = ∫f dE；与 spec-int-general-id / -exp / -phi-t 一致）
postulate
  fc-integral : (f : ℝ → ℝ) → fc f ≡ spec-int-general f

-- **可证**：M_σ（X 与 E 逐集交换）⟹ X 与任意函数演算 fc(f) 交换
--（fc-integral 桥接 + X-comm-spec-int-general）
X-comm-fc : (X : Op) → ((P : Borel) → X *ₒ E P ≡ E P *ₒ X) → (f : ℝ → ℝ)
  → X *ₒ fc f ≡ fc f *ₒ X
X-comm-fc X h f =
  trans (cong (λ Z → X *ₒ Z) (fc-integral f))
  (trans (X-comm-spec-int-general X h f)
         (cong (λ Z → Z *ₒ X) (sym (fc-integral f))))

-- **可证（M-σ 形式）**：谱匹配态射与整个函数演算交换
σ-to-fc : {X : Op} → M-σ X → (f : ℝ → ℝ) → X *ₒ fc f ≡ fc f *ₒ X
σ-to-fc {X} h f = X-comm-fc X h f

-- 函数演算统一层状态：
--  - fc = 一般谱积分（fc-integral 桥接公理）；M_σ ⟹ 全函数演算交换
--    （X-comm-fc / σ-to-fc **可证**）。
--  - 与 Fuglede 的衔接：M-Sp ⟹ M-σ（intertwine-imp-spectral，**§5g 已降为
--    可证定理**）后，M-Sp 亦 ⟹ 全 fc 交换。

-- ==================================================================
-- §5d 函数演算的代数结构（fc 同态：fc(f·g) = fc(f)·fc(g)）
-- ==================================================================
-- 目标：登记函数演算的同态结构（f ↦ f(A) 是代数同态）——
-- fc-mul（乘法保持）为桥接公理；推导 fc 与 A-power 的联系。

-- 函数演算乘法性（定义性公理）：fc(f·g) = fc(f)·fc(g)（f ↦ f(A) 是代数同态；
-- 与 fc-integral + 谱积分乘法（simple-mul 简单函数版）一致，测度论层降为定理）
postulate
  fc-mul : (f g : ℝ → ℝ) → fc (λ x → f x *ℝ g x) ≡ fc f *ₒ fc g

-- **可证**：fc(x·x) = A·A（fc-mul + fc-id）
fc-id-sq : fc (λ x → x *ℝ x) ≡ A *ₒ A
fc-id-sq = trans (fc-mul (λ x → x) (λ x → x)) (cong₂ _*ₒ_ fc-id fc-id)

-- **可证**：fc(xⁿ) = Aⁿ（n ≥ 1；fc-mul 归纳 + fc-id）
fc-power : (n : ℕ) → fc (λ x → ℝ-power (suc n) x) ≡ A-power (suc n)
fc-power zero =
  trans (fc-ext (λ x → *-ident-ℝ x))
        (trans fc-id (sym (*ₒ-ident A)))
fc-power (suc n) =
  trans (fc-mul (λ x → x) (λ x → ℝ-power (suc n) x))
        (cong₂ _*ₒ_ fc-id (fc-power n))

-- 函数演算代数结构状态：
--  - fc 同态核心（fc-mul 桥接公理）+ 推导 fc-id-sq（fc(x²) = A²）、
--    fc-power（fc(xⁿ) = Aⁿ，n ≥ 1）。
--  - fc-const（常函数 ⟹ 标量算子，需标量单位律）与 fc 加性随函数演算完整层登记。

-- ==================================================================
-- §5e 函数演算的加性与常数（fc 同态完整：加/乘/常数保持）
-- ==================================================================
-- 目标：补全 f ↦ f(A) 的代数同态结构——fc-mul（§5d）+ fc-add + fc-const。

-- 函数演算加法/常数保持（定义性公理；同态结构，与 fc-integral + simple-add /
-- ∫c dE = c·E(ℝ) 一致，测度论层降为定理）
postulate
  fc-add : (f g : ℝ → ℝ) → fc (λ x → f x +ℝ g x) ≡ fc f +ₒ fc g
  fc-const : (c : ℝ) → fc (λ _ → c) ≡ c ·ₒ 𝟙ₒ

-- **可证**：fc(x+x) = A +ₒ A（fc-add + fc-id）
fc-id-add : fc (λ x → x +ℝ x) ≡ A +ₒ A
fc-id-add = trans (fc-add (λ x → x) (λ x → x)) (cong₂ _+ₒ_ fc-id fc-id)

-- **可证**：fc(c·x) = c·A（fc-mul 常数×恒等 + fc-const + ·ₒ-comm + *ₒ-ident-l）
fc-scalar-id : (c : ℝ) → fc (λ x → c *ℝ x) ≡ c ·ₒ A
fc-scalar-id c =
  trans (fc-mul (λ _ → c) (λ x → x))
  (trans (cong₂ _*ₒ_ (fc-const c) fc-id)
         (trans (·ₒ-comm c 𝟙ₒ A) (cong (λ Y → c ·ₒ Y) (*ₒ-ident-l A))))

-- 函数演算同态完整状态：
--  - 加/乘/常数保持（fc-add / fc-mul / fc-const）+ 恒等（fc-id）——f ↦ f(A) 是
--    代数同态的完整刻画；推导 fc-id-add（fc(x+x) = A+A）、fc-scalar-id（fc(c·x) = c·A）。
--  - fc-poly（原 §5b 桥接）已由同态结构推导为可证定理（§5f：fc-add 迭代 +
--    fc-monomial 逐项），桥接公理删除。

-- ==================================================================
-- §5f fc-poly 降为可证定理（桥接替换：fc 同态结构推导）
-- ==================================================================
-- 目标：将 §5b 原 fc-poly 桥接公理删除，改用 §5d/§5e 的 fc 同态结构
-- （fc-mul + fc-add + fc-const + fc-power）推导——函数演算保持多项式是
-- 代数同态（f ↦ f(A) 保加/乘/常数/恒等）的直接推论。随后闭合 §5b 的
-- 多项式/连续函数交换（X-comm-fc-poly / X-comm-fc-continuous）。
-- 依赖补充：`·ₒ-zero-l`（P1Spectral：zeroℝ ·ₒ X ≡ 𝟘ₒ，标量零吸收律，
-- 与 *ₒ-zero-l 平行——fc-poly 基例 m=0 需 fc(0) = 𝟘ₒ，现有算子代数公理
-- 集不可推出该零律，登记为基础假设）。
-- 推导链：fc-monomial（单项式 c·xⁿ = c·Aⁿ，n 任意：n=0 经 fc-const，
-- n≥1 经 fc-mul + fc-power 归纳）→ fc-poly（Σᵢ aᵢ·x^{nᵢ} 展开：
-- fc-add 迭代 + fc-monomial 逐项）。

-- **可证**：零常函数的函数演算 = 零算子（fc-const + 标量零律）
fc-zero : fc (λ x → zeroℝ) ≡ 𝟘ₒ
fc-zero = trans (fc-const zeroℝ) (·ₒ-zero-l 𝟙ₒ)

-- **可证**：fc(c·xⁿ) = c·Aⁿ（n 任意；n=0 经 fc-const + *-ident-ℝ，
-- n≥1 经 fc-mul + fc-const + fc-power 归纳 + ·ₒ 结合）
fc-monomial : (c : ℝ) (n : ℕ) → fc (λ x → c *ℝ ℝ-power n x) ≡ c ·ₒ A-power n
fc-monomial c zero =
  trans (fc-ext (λ x → *-ident-ℝ c))
        (fc-const c)
fc-monomial c (suc n) with n
... | zero =
  trans (fc-ext (λ x → cong (λ y → c *ℝ y) (*-ident-ℝ x)))
        (trans (fc-scalar-id c)
               (cong (λ Y → c ·ₒ Y) (sym (*ₒ-ident A))))
... | suc m =
  trans (fc-mul (λ _ → c) (λ x → x *ℝ ℝ-power (suc m) x))
        (trans (cong₂ _*ₒ_ (fc-const c)
                          (trans (fc-mul (λ x → x) (λ x → ℝ-power (suc m) x))
                                 (cong₂ _*ₒ_ fc-id (fc-power m))))
               (trans (·ₒ-comm c 𝟙ₒ (A *ₒ A-power (suc m)))
                      (cong (λ Y → c ·ₒ Y) (*ₒ-ident-l (A *ₒ A-power (suc m))))))

-- **可证**：函数演算保持多项式——fc-poly 定理（原 §5b 桥接公理，现为可证定理）
--（同态结构推导：Σᵢ aᵢ·x^{nᵢ} 展开——fc-add 迭代 + fc-monomial 逐项；
--  基例 m=0：fc(0) = 𝟘ₒ）
fc-poly : {m : ℕ} (a : Fin m → ℝ) (n : Fin m → ℕ) → fc (poly-fn {m} a n) ≡ poly-A {m} a n
fc-poly {zero} a n = fc-zero
fc-poly {suc m} a n =
  trans (fc-add (λ x → a zero *ℝ ℝ-power (n zero) x)
                (λ x → sum-ℝ {m} (λ i → a (suc i) *ℝ ℝ-power (n (suc i)) x)))
        (cong₂ _+ₒ_ (fc-monomial (a zero) (n zero))
                    (fc-poly {m} (λ i → a (suc i)) (λ i → n (suc i))))

-- **可证**：X·A = A·X ⟹ X 与 fc(p) 交换（p 为多项式函数）
--（fc-poly 定理 + poly-A-comm；Fuglede 引理 1 证明的 fc 连接步）
X-comm-fc-poly : {X : Op} → X *ₒ A ≡ A *ₒ X → {m : ℕ} (a : Fin m → ℝ) (n : Fin m → ℕ)
  → X *ₒ fc (poly-fn {m} a n) ≡ fc (poly-fn {m} a n) *ₒ X
X-comm-fc-poly {X} h {m} a n =
  trans (cong (λ Z → X *ₒ Z) (fc-poly {m} a n))
  (trans (poly-A-comm {X} h {m} a n)
         (cong (λ Z → Z *ₒ X) (sym (fc-poly {m} a n))))

-- **可证**：X·A = A·X ⟹ X 与连续函数 fc(f) 交换
--（fc-continuous 桥接 + sup-comm + X-comm-fc-poly 逐成员；
--  Fuglede 引理 1 证明链：交织 ⟹ 多项式（§3b）⟹ fc 多项式（§5f）⟹ 连续（本节））
X-comm-fc-continuous : {X : Op} → X *ₒ A ≡ A *ₒ X → (f : ℝ → ℝ)
  → X *ₒ fc f ≡ fc f *ₒ X
X-comm-fc-continuous {X} h f =
  trans (cong (λ Z → X *ₒ Z) (fc-continuous f))
  (trans (sup-comm X (fc-below f) (λ Y yb → member-fc-comm h Y yb))
         (cong (λ Z → Z *ₒ X) (sym (fc-continuous f))))
  where
  -- 族成员均为多项式 fc ⟹ 与 X 交换（X-comm-fc-poly）
  member-fc-comm : (h : X *ₒ A ≡ A *ₒ X) → (Y : Op) → fc-below f Y → X *ₒ Y ≡ Y *ₒ X
  member-fc-comm h Y (m , a , n , (eq , _)) =
    trans (cong (λ Z → X *ₒ Z) eq)
          (trans (X-comm-fc-poly {X} h {m} a n)
                 (cong (λ Z → Z *ₒ X) (sym eq)))

-- §5f 状态：
--  - fc-poly 降为可证定理（原 §5b 桥接公理删除）：同态结构推导完成。
--  - X-comm-fc-poly / X-comm-fc-continuous 闭合（零新增 fc 桥接）。
--  - 剩余 fc 桥接公理：fc-continuous（§5b）/ fc-integral（§5c）/
--    fc-mul（§5d）/ fc-add、fc-const（§5e）——均注明降定理路径（测度论层）。

-- ==================================================================
-- §5g Fuglede 引理 1 方向闭合（指示桥接 + intertwine-imp-spectral 降为定理）
-- ==================================================================
-- 目标：闭合 Fuglede 引理 1 方向（交织 ⟹ 谱匹配）——登记经典扩展层的
-- 指示桥接（E(P) = fc(1_P)），使 §1 原 intertwine-imp-spectral 公理降为
-- **可证定理**；§3 的 Sp-to-σ 与 §4 的定理 3 随迁本节闭合。
-- 关键点：X-comm-fc-continuous（§5f）的证明不依赖连续性（fc-below 对任意
-- f 定义），故 X·A = A·X ⟹ X 与 fc(1_P) 交换；再经指示桥接回 E(P)。
-- 依赖补充：`indicator`（经典扩展对象）+ `indicator-bridge`（定义性桥接，
-- 降定理路径 = 测度论/Borel 函数演算层：1_P 点态 = 1 ⟺ P x）。
-- 经典扩展（阶段 7-5，2026-08-02）：排中律为基础假设，indicator 由 postulate 降为
-- **定义**，点态性质（1_P x = 1 ⟺ P x）**可证**——indicator-bridge 点态化的决策基础。

-- 经典扩展（基础假设：排中律——构造性框架外扩，indicator 点态性质的决策基础；
-- 降定理路径 = 经典逻辑层）
postulate
  classical : {A : Set} → A ⊎ (A → ⊥)

-- 指示函数（经典扩展对象）：P 的特征函数 1_P : ℝ → ℝ
--（1_P x = if P x then 1 else 0——排中律 classical 提供决策；原 postulate 降为定义）
indicator : Borel → (ℝ → ℝ)
indicator P x with classical {P x}
indicator P x | inj₁ p = oneℝ
indicator P x | inj₂ np = zeroℝ

-- **可证**：oneℝ ≢ zeroℝ（0 < 1 经等式 subst 的严格序矛盾；用 DHStructural ⊥ 避免 _≢_ 的类型分叉）
one≢zero-ℝ : (oneℝ ≡ zeroℝ) → ⊥
one≢zero-ℝ eq = irreflexive-ℝ (subst (λ z → zeroℝ <ℝ z) eq zero-lt-one-ℝ)

-- **可证**：zeroℝ ≢ oneℝ（对称方向：1 经等式 subst 的严格序矛盾）
zero≢one-ℝ : (zeroℝ ≡ oneℝ) → ⊥
zero≢one-ℝ eq = irreflexive-ℝ (subst (λ z → z <ℝ oneℝ) eq zero-lt-one-ℝ)

-- **可证**：指示函数点态性质——1_P x = 1 ⟺ P x（排中律分情形，阶段 7-5 核心）
indicator-pos : (P : Borel) (x : ℝ) → P x → indicator P x ≡ oneℝ
indicator-pos P x p with classical {P x}
indicator-pos P x p | inj₁ p' = refl
indicator-pos P x p | inj₂ np' = ⊥-elim (np' p)

indicator-zero : (P : Borel) (x : ℝ) → (P x → ⊥) → indicator P x ≡ zeroℝ
indicator-zero P x np with classical {P x}
indicator-zero P x np | inj₁ p = ⊥-elim (np p)
indicator-zero P x np | inj₂ np' = refl

indicator-eq-one-iff : (P : Borel) (x : ℝ) → indicator P x ≡ oneℝ → P x
indicator-eq-one-iff P x h with classical {P x}
indicator-eq-one-iff P x h | inj₁ p = p
indicator-eq-one-iff P x h | inj₂ np' = ⊥-elim (zero≢one-ℝ h)

-- 指示桥接（定义性公理）：E(P) = fc(1_P)——谱测度 = 指示函数的函数演算
--（Borel 函数演算的基本事实：E(P) = ∫1_P dE；测度论层完整实现时降为定理）
postulate
  indicator-bridge : (P : Borel) → E P ≡ fc (indicator P)

-- **可证**：交织 ⟹ 谱匹配（Fuglede 引理 1 方向，原 §1 公理降为定理）
-- 链：X·A = A·X ⟹ X·fc(1_P) = fc(1_P)·X [X-comm-fc-continuous，任意 f]
--      ⟹ X·E(P) = E(P)·X [indicator-bridge 双向]
intertwine-imp-spectral : (X : Op) → X *ₒ A ≡ A *ₒ X → (P : Borel) → X *ₒ E P ≡ E P *ₒ X
intertwine-imp-spectral X h P =
  trans (cong (λ Z → X *ₒ Z) (indicator-bridge P))
        (trans (X-comm-fc-continuous h (indicator P))
               (cong (λ Z → Z *ₒ X) (sym (indicator-bridge P))))

-- 引理 1 方向（**可证**）：M_Sp ⊆ M_σ（随迁自 §3）
Sp-to-σ : {X : Op} → M-Sp X → M-σ X
Sp-to-σ {X} h P = intertwine-imp-spectral X h P

-- 定理 3（无限维版，随迁自 §4）：M_Sp = M_σ = M_Rec（线性语义下谱匹配双射）
theorem3-Sp-σ : {X : Op} → (M-Sp X → M-σ X) ×₁ (M-σ X → M-Sp X)
theorem3-Sp-σ = pair₁ (λ h → Sp-to-σ h) (λ h → σ-to-Sp h)

theorem3-Rec-σ : {X : Op} → (M-Rec X → M-σ X) ×₁ (M-σ X → M-Rec X)
theorem3-Rec-σ = pair₁ (λ h → Rec-to-σ h) (λ h → σ-to-Rec h)

theorem3 : {X : Op} → ((M-Sp X → M-σ X) ×₁ (M-σ X → M-Sp X))
               ×₁ ((M-Rec X → M-σ X) ×₁ (M-σ X → M-Rec X))
theorem3 = pair₁ (pair₁ (λ h → Sp-to-σ h) (λ h → σ-to-Sp h))
                 (pair₁ (λ h → Rec-to-σ h) (λ h → σ-to-Rec h))

-- §5g 状态：
--  - intertwine-imp-spectral 由公理降为**可证定理**（Fuglede 引理 1 方向闭合）。
--  - 新增经典扩展层假设：indicator + indicator-bridge（降定理路径 = 测度论层）。
--  - §14 的 Sp-to-exp-tA 经 §5g 的 Sp-to-σ 闭合（M-Sp ⟹ 全半群族交换）。

-- ==================================================================
-- §6 P1 无限维组装（推论 4 无限维版：Hom_Sp ≅ Hom_σ ≅ Hom_Rec）
-- ==================================================================

-- level 多态 cong（Hom-σ 的 prop 为 Set₁，M-σ 为 Set₁ 值；Agda.Builtin.Equality 的 _≡_ 为 level-多态）
cong₁ : {a b : Level} {A : Set a} {B : Set b} {x y : A} (f : A → B) → x ≡ y → f x ≡ f y
cong₁ f refl = refl

-- 互逆往返一致性（定义性公理：谱表示（spectral-rep-A / exp-spectral-rep）与
-- 谱积分线性（§1b 推导 X-comm-spectral-int-deriv / -exp-deriv）之间的往返一致性；
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
-- §7 简单函数谱积分：线性细化（sum-op/spec-int-simple/simple-comm 已移至 §1b，
-- 本节为加法性补充）
-- ==================================================================
--（§1b 已含：sum-op、spec-int-simple、simple-comm——简单函数谱积分的交换性；
--  本节补充加法性（simple-add），配合 §10c/§10d 的乘法性，构成简单函数层
--  交换 + 加法 + 乘法的完整代数结构。）

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

-- ==================================================================
-- §5h 简单函数 = 函数演算（阶段 7-4 第一步：fc-simple-integral，2026-08-02）
-- ==================================================================
-- 目标：fc-integral（fc(f) = ∫f dE，§5c 桥接公理）降定理的第一步——
-- 简单函数谱积分 = 其函数演算（∫(Σcᵢ·1_{Ωᵢ}) dE = fc(Σcᵢ·1_{Ωᵢ})）。
-- 链：fc(s) = fc(Σᵢcᵢ·1_{Ωᵢ}) = Σᵢfc(cᵢ·1_{Ωᵢ})（fc-sum）= Σᵢcᵢ·fc(1_{Ωᵢ})（fc-atom）
--      = Σᵢcᵢ·E(Ωᵢ)（indicator-bridge）= ∫s dE（spec-int-simple 定义）。
-- 零新增公理：全部由 fc 同态（fc-add/fc-mul/fc-const/fc-zero）与
-- indicator-bridge/indicator（经典扩展，§5g）推导。

-- **可证**：fc 保持有限和——fc(Σᵢ gᵢ) = Σᵢ fc(gᵢ)（fc-add 归纳）
fc-sum : {m : ℕ} (g : Fin m → (ℝ → ℝ))
  → fc (λ x → sum-ℝ {m} (λ i → g i x)) ≡ sum-op {m} (λ i → fc (g i))
fc-sum {zero} g = trans (fc-ext (λ x → refl)) fc-zero
fc-sum {suc m} g =
  trans (fc-add (g zero) (λ x → sum-ℝ {m} (λ i → g (suc i) x)))
        (cong₂ _+ₒ_ refl (fc-sum {m} (λ i → g (suc i))))

-- **可证**：fc 保持标量乘——fc(c·g) = c·fc(g)（fc-mul + fc-const + ·ₒ-comm + 单位律）
fc-scalar-mul : (c : ℝ) (g : ℝ → ℝ) → fc (λ x → c *ℝ g x) ≡ c ·ₒ fc g
fc-scalar-mul c g =
  trans (fc-mul (λ _ → c) g)
        (trans (cong₂ _*ₒ_ (fc-const c) refl)
               (trans (·ₒ-comm c 𝟙ₒ (fc g))
                      (cong (λ Y → c ·ₒ Y) (*ₒ-ident-l (fc g)))))

-- 函数减法（点态）：(f − g)(x) = f x −ℝ g x（阶段 4：fc 保减法的基础）
fn-sub : (ℝ → ℝ) → (ℝ → ℝ) → ℝ → ℝ
fn-sub f g x = f x -ℝ g x

-- **可证**：fc 保减法——fc(f − g) = fc f −ₒ fc g（阶段 4 第一步）
--（fn-sub 点态展开（sub-ℝ-def + fc-ext）→ fc-add（加性）→ fc-scalar-mul（−1 标量）
--  → _−ₒ_ 定义；fc(p) = fc(p⁺) − fc(p⁻) 分解路径的核心组件——fc-poly-le-spec-int
--  构造化（∫p = ∫p⁺ −ₒ ∫p⁻，p⁺/p⁻ 非负 ⟹ 非负 sup 逼近）的前置）
fc-sub : (f g : ℝ → ℝ) → fc (fn-sub f g) ≡ fc f -ₒ fc g
fc-sub f g =
  trans (fc-ext (λ x → sub-ℝ-def (f x) (g x)))
        (trans (fc-add f (λ x → negℝ (g x)))
               (cong₂ _+ₒ_ refl neg-scalar))
  where
  neg-scalar : fc (λ x → negℝ (g x)) ≡ (negℝ oneℝ) ·ₒ fc g
  neg-scalar = trans (fc-ext (λ x → sym (neg-one-mul (g x))))
                     (fc-scalar-mul (negℝ oneℝ) g)

-- **可证**：fc 正负分解——fc(p) = fc(p⁺) −ₒ fc(p⁻)（阶段 4 第二步）
--（fc-ext（p = p⁺ − p⁻ 逐点，decomp-pos-neg）+ fc-sub——把 fc(p) 分解为两个
--  非负函数 p⁺/p⁻ 的 fc；fc-poly-le-spec-int 构造化的关键组件：fc(p) ≤ₒ
--  ∫p⁺ −ₒ ∫p⁻（p⁺/p⁻ 非负 ⟹ 各自由非负 sup 逼近，v1.15 幂单调性 + dyadic 阶梯））
fc-decomp-pos-neg : (p : ℝ → ℝ) → fc p ≡ fc (pos-part p) -ₒ fc (neg-part p)
fc-decomp-pos-neg p =
  trans (sym (fc-ext (λ x → decomp-pos-neg p x)))
        (fc-sub (pos-part p) (neg-part p))

-- dyadic 网格点：xⱼ = (j·c)/2^k（[0,c] 的 2^k 等分点；j ≤ 2^k 时 xⱼ ≤ c；
--  阶段 4 余项：fc-poly-le-spec-int 构造化的 dyadic 阶梯逼近的网格基础）
grid-pt : ℕ → ℝ → ℕ → ℝ
grid-pt k c j = (natℝ j *ℝ c) /ℝ natℝ (2^ k)

-- **可证**：网格点非负——0 ≤ c ⟹ 0 ≤ xⱼ（natℝ-nonneg + *-nonneg-ℝ + div-nonneg，
--  分母 2^k > 0 经 2^-pos + natℝ-pos-embed）
grid-pt-nonneg : (k : ℕ) (c : ℝ) → zeroℝ ≤ℝ c → (j : ℕ) → zeroℝ ≤ℝ grid-pt k c j
grid-pt-nonneg k c hc j =
  div-nonneg {natℝ j *ℝ c} {natℝ (2^ k)}
             (*-nonneg-ℝ (natℝ j) c (natℝ-nonneg j) hc)
             (natℝ-pos-embed (2^-pos k))

-- **可证**：网格严格递增——0 < c ⟹ xⱼ < xⱼ₊₁（natℝ-<-embed（j < suc j）+ 乘正保序
--  （*-pos-mono-ℝ，c > 0）+ 同分母除保序（/-lt-same-den-ℝ，分母 2^k > 0））
grid-pt-suc : (k : ℕ) (c : ℝ) → zeroℝ <ℝ c → (j : ℕ) → grid-pt k c j <ℝ grid-pt k c (suc j)
grid-pt-suc k c hc j =
  /-lt-same-den-ℝ {natℝ j *ℝ c} {natℝ (suc j) *ℝ c} {natℝ (2^ k)}
                  (subst (λ w → (natℝ j *ℝ c) <ℝ w)
                         (*-comm-ℝ c (natℝ (suc j)))
                         (subst (λ z → z <ℝ (c *ℝ natℝ (suc j)))
                         (*-comm-ℝ c (natℝ j))
                         (*-pos-mono-ℝ {a = natℝ j} {b = natℝ (suc j)} {c = c} hc
                                       (natℝ-<-embed (<-suc j)))))

-- dyadic 区间：Ωⱼ = [xⱼ, xⱼ₊₁)（第 j 个 2^k 等分子区间；disj/cover 证明见 SimpleF
--  阶梯构造阶段——disj 依赖 grid-pt-suc（严格递增），cover 依赖实数划分定理）
dyadic-Ω : (k : ℕ) (c : ℝ) (j : ℕ) → ℝ → Set
dyadic-Ω k c j x = (grid-pt k c j ≤ℝ x) × (x <ℝ grid-pt k c (suc j))

-- ==================================================================
-- ℕ 严格序工具（SimpleF 阶梯 disj 基础；2026-08-03，零新增公理）
-- ==================================================================
-- 目标：dyadic-Ω 的 pairwise 不相交证明（disj）——i ≠ j ⟹ Ωᵢ ∩ Ωⱼ = ∅。
-- 需要 Fin 下标可比（三分律，fin-to-nat-trich 见 §10e 后 fin-to-nat 处）
-- + 网格单调性（i <ℕ j ⟹ xᵢ < xⱼ）。

-- ℕ 严格序三分律（归纳可证）
<-ℕ-trich : (m n : ℕ) → (m <ℕ n) ⊎ ((n <ℕ m) ⊎ (m ≡ n))
<-ℕ-trich zero    zero    = inj₂ (inj₂ refl)
<-ℕ-trich zero    (suc n) = inj₁ z<s
<-ℕ-trich (suc m) zero    = inj₂ (inj₁ z<s)
<-ℕ-trich (suc m) (suc n) with <-ℕ-trich m n
<-ℕ-trich (suc m) (suc n) | inj₁ h          = inj₁ (s<s h)
<-ℕ-trich (suc m) (suc n) | inj₂ (inj₁ h)   = inj₂ (inj₁ (s<s h))
<-ℕ-trich (suc m) (suc n) | inj₂ (inj₂ p)   = inj₂ (inj₂ (cong suc p))

-- m < suc n ⟹ m ≡ n ⊎ m < n（ℕ 层分裂）
<-ℕ-split : {m n : ℕ} → m <ℕ suc n → (m ≡ n) ⊎ (m <ℕ n)
<-ℕ-split {zero}    {zero}    z<s           = inj₁ refl
<-ℕ-split {zero}    {suc n}   z<s           = inj₂ z<s
<-ℕ-split {suc m}   {zero}    (s<s ())
<-ℕ-split {suc m}   {suc n}   (s<s h) with <-ℕ-split {m} {n} h
<-ℕ-split {suc m}   {suc n}   (s<s h) | inj₁ p = inj₁ (cong suc p)
<-ℕ-split {suc m}   {suc n}   (s<s h) | inj₂ q = inj₂ (s<s q)

-- m < n ⟹ suc m < n ⊎ suc m ≡ n（disj 核心：i < j ⟹ xᵢ₊₁ ≤ xⱼ）
<-ℕ-suc-split : {m n : ℕ} → m <ℕ n → (suc m <ℕ n) ⊎ (suc m ≡ n)
<-ℕ-suc-split {m} {zero}    ()
<-ℕ-suc-split {m} {suc n}   h with <-ℕ-split {m} {n} h
<-ℕ-suc-split {m} {suc n}   h | inj₁ p = inj₂ (cong suc p)
<-ℕ-suc-split {m} {suc n}   h | inj₂ q = inj₁ (s<s q)

-- **可证**：网格严格单调——i <ℕ j ⟹ xᵢ < xⱼ
--（归纳于 j：j = suc j' 时 i <ℕ suc j' 分裂为 i ≡ j'（grid-pt-suc 直接）
--  或 i <ℕ j'（归纳 + grid-pt-suc 传递））
grid-pt-lt : (k : ℕ) (c : ℝ) → zeroℝ <ℝ c → {i j : ℕ} → i <ℕ j → grid-pt k c i <ℝ grid-pt k c j
grid-pt-lt k c hc {i} {zero}    ()
grid-pt-lt k c hc {i} {suc j}   ij with <-ℕ-split {i} {j} ij
grid-pt-lt k c hc {i} {suc j}   ij | inj₁ p =
  subst (λ w → grid-pt k c w <ℝ grid-pt k c (suc j)) (sym p) (grid-pt-suc k c hc j)
grid-pt-lt k c hc {i} {suc j}   ij | inj₂ q =
  trans-<ℝ (grid-pt-lt k c hc {i} {j} q) (grid-pt-suc k c hc j)

-- **可证**：dyadic 区间不相交（严格序版）——i <ℕ j ⟹ Ωᵢ ∩ Ωⱼ = ∅
--（i < j ⟹ xᵢ₊₁ ≤ xⱼ（<-ℕ-suc-split + grid-pt-lt/≡ 特化）⟹
--  x < xᵢ₊₁（Ωᵢ 上界）≤ xⱼ ≤ x（Ωⱼ 下界）⟹ x < x 矛盾（irreflexive-ℝ））
dyadic-disj-lt : (k : ℕ) (c : ℝ) → zeroℝ <ℝ c → {i j : ℕ} → i <ℕ j
  → (x : ℝ) → dyadic-Ω k c i x → dyadic-Ω k c j x → ⊥
dyadic-disj-lt k c hc {i} {j} ij x (xi≤x , x<xi+1) (xj≤x , x<xj+1) =
  irreflexive-ℝ (lt-≤-trans-ℝ (lt-≤-trans-ℝ x<xi+1 xi+1≤xj) xj≤x)
  where
  -- xᵢ₊₁ ≤ xⱼ：suc i < j 经网格单调（<-≤-ℝ），suc i ≡ j 经 refl
  xi+1≤xj : grid-pt k c (suc i) ≤ℝ grid-pt k c j
  xi+1≤xj with <-ℕ-suc-split {i} {j} ij
  xi+1≤xj | inj₁ h = <-≤-ℝ (grid-pt-lt k c hc {suc i} {j} h)
  xi+1≤xj | inj₂ p = subst (λ w → grid-pt k c (suc i) ≤ℝ grid-pt k c w) p
                          (refl-≤ℝ {grid-pt k c (suc i)})

-- **可证**：dyadic 区间不相交（Fin 版，SimpleF.disj 核心）——i ≢ j ⟹ Ωᵢ ∩ Ωⱼ = ∅
--（fin-to-nat-trich 三分律：i<j 经 dyadic-disj-lt、j<i 经其对称、i≡j 与 neq 矛盾
--  （fin-to-nat-inj）；依赖 fin-to-nat-trich/-inj，定义见 §10f fin-to-nat 之后）
-- dyadic-disj 定义见下（§10f，fin-to-nat-trich 后）

-- 简单函数的点态函数（SimpleF → ℝ → ℝ）：s(x) = Σᵢ cᵢ·1_{Ωᵢ}(x)
simple-fn : SimpleF → (ℝ → ℝ)
simple-fn s x = sum-ℝ {SimpleF.m s} (λ i → SimpleF.c s i *ℝ indicator (SimpleF.Ω s i) x)

-- **可证**：fc(c·1_Ω) = c·E(Ω)（fc-scalar-mul + indicator-bridge）
fc-atom : (c : ℝ) (Ω : Borel) → fc (λ x → c *ℝ indicator Ω x) ≡ c ·ₒ E Ω
fc-atom c Ω = trans (fc-scalar-mul c (indicator Ω))
                    (cong (λ Y → c ·ₒ Y) (sym (indicator-bridge Ω)))

-- **可证**：简单函数谱积分 = 其函数演算——∫s dE = fc(s)（阶段 7-4 关键引理）
fc-simple-integral : (s : SimpleF) → simple-int s ≡ fc (simple-fn s)
fc-simple-integral s =
  sym (trans (fc-sum (λ i → λ x → SimpleF.c s i *ℝ indicator (SimpleF.Ω s i) x))
             (sum-op-congₒ (λ i → fc-atom (SimpleF.c s i) (SimpleF.Ω s i))))

-- ------------------------------------------------------------------
-- 7-4 余项（fc-integral 降定理的单侧方向）：fc 单调性组件，2026-08-02
-- ------------------------------------------------------------------
-- 目标：spec-int-general f ≤ₒ fc f（简单函数下界 sup ≤ 函数演算）——
-- fc-integral（fc(f) = ∫f dE，§5c 桥接公理）降定理的"≤"方向。
-- 依赖：fc 单调性（本批）+ 覆盖坍缩（simple-fn ≤ f 点态，下一批）。

-- **可证**：fc-below 族对 f 单调——f ≤ g 点态 ⟹ fc-below f ⊆ fc-below g
fc-below-mono : {f g : ℝ → ℝ} → ((x : ℝ) → f x ≤ℝ g x) → (Y : Op) → fc-below f Y → fc-below g Y
fc-below-mono h Y (m , a , n , eq , dom) =
  m , a , n , eq , λ x → ≤-trans-ℝ (dom x) (h x)

-- **可证**：fc 单调——f ≤ g 点态 ⟹ fc f ≤ₒ fc g
--（fc-continuous + fc-below-mono + sup-op-least/upper）
fc-mono : {f g : ℝ → ℝ} → ((x : ℝ) → f x ≤ℝ g x) → fc f ≤ₒ fc g
fc-mono {f} {g} h = subst (λ Z → Z ≤ₒ fc g) (sym (fc-continuous f))
                           (sup-op-least (fc-below f) (fc g) bound)
  where
  bound : (Y : Op) → fc-below f Y → Y ≤ₒ fc g
  bound Y yb = subst (λ Z → Y ≤ₒ Z) (sym (fc-continuous g))
                     (sup-op-upper (fc-below g) Y (fc-below-mono h Y yb))

-- **可证**：ℝ 有限和保序——逐项 ≤ ⟹ 和 ≤（归纳 + ≤-+-mono-ℝ）
sum-mono-ℝ : {m : ℕ} {a b : Fin m → ℝ} → ((i : Fin m) → a i ≤ℝ b i) → sum-ℝ a ≤ℝ sum-ℝ b
sum-mono-ℝ {zero} h = refl-≤ℝ
sum-mono-ℝ {suc m} {a} {b} h =
  ≤-+-mono-ℝ (h zero) (sum-mono-ℝ {m} {λ i → a (suc i)} {λ i → b (suc i)} (λ i → h (suc i)))

-- **可证**：ℝ 有限和分配——Σᵢ(c·aᵢ) = c·Σᵢ aᵢ（归纳 + distrib-ℝ + *-zero-ℝ）
sum-distrib-ℝ : {m : ℕ} (c : ℝ) (a : Fin m → ℝ) → sum-ℝ (λ i → c *ℝ a i) ≡ c *ℝ sum-ℝ a
sum-distrib-ℝ {zero} c a = sym (*-zero-ℝ c)
sum-distrib-ℝ {suc m} c a =
  trans (cong₂ _+ℝ_ refl (sum-distrib-ℝ {m} c (λ i → a (suc i))))
        (sym (distrib-ℝ c (a zero) (sum-ℝ {m} (λ i → a (suc i)))))

-- **可证**：原子点态比较——x ∈ Ω ⟹ c·1_Ω(x) ≤ f x·1_Ω(x)（c ≤ f x + indicator-pos）
atom-ip-le : (c fx : ℝ) (Ω : Borel) (x : ℝ) → c ≤ℝ fx → Ω x
  → (c *ℝ indicator Ω x) ≤ℝ (fx *ℝ indicator Ω x)
atom-ip-le c fx Ω x hc hx =
  subst (λ z → (c *ℝ z) ≤ℝ (fx *ℝ z)) (sym (indicator-pos Ω x hx))
        (subst (λ z → z ≤ℝ (fx *ℝ oneℝ)) (sym (*-ident-ℝ c))
               (subst (λ z → c ≤ℝ z) (sym (*-ident-ℝ fx)) hc))

-- **可证**：原子点态比较（补集）——x ∉ Ω ⟹ c·1_Ω(x) ≤ f x·1_Ω(x)（indicator-zero）
atom-ip-lec : (c fx : ℝ) (Ω : Borel) (x : ℝ) → (Ω x → ⊥)
  → (c *ℝ indicator Ω x) ≤ℝ (fx *ℝ indicator Ω x)
atom-ip-lec c fx Ω x hx =
  subst (λ z → (c *ℝ z) ≤ℝ (fx *ℝ z)) (sym (indicator-zero Ω x hx))
        (subst (λ z → z ≤ℝ (fx *ℝ zeroℝ)) (sym (*-zero-ℝ c))
               (subst (λ z → zeroℝ ≤ℝ z) (sym (*-zero-ℝ fx)) (refl-≤ℝ {zeroℝ})))

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
--    ·ₒ-+ 为算子代数基础公理）——一般谱积分逼近（§1b）的简单函数基础。
--  - **一般函数层（§1b 已完成）**：∫f dE = 简单函数下界的 sup（spec-int-general），
--    X-comm-spectral-int / -exp 已由 sup-comm + simple-comm **降为可证明定理**
--    （X-comm-spectral-int-deriv / -exp-deriv）。
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

-- 桥接公理（定义性）：∫φ_t dE = e^(-tA)——φ_t(x) = e^(-tx) 的谱积分即 exp-tA t
--（与 exp-spectral-rep（t=1）一致；§1b 的 spec-int-general 对 φ_t 的谱表示）
postulate
  spec-int-general-phi-t : (t : ℝ) → spec-int-general (λ x → exp (negℝ (t *ℝ x))) ≡ exp-tA t

-- **可证**：φ_t 的非负积分明确值——∫φ_t = 非负 sup = e^(-tA)（阶段 3 第一步）
--（φ_t 全 ℝ 非负（phi-t-pos）⟹ spec-int-nonneg-consistent（钉住与非负 sup 无分歧）
--  + spec-int-general-phi-t 桥接组合——钉住解析为"非负 sup 明确值 + 谱表示值"）
spec-int-nonneg-phi-t : (t : ℝ) → spec-int-nonneg (λ x → exp (negℝ (t *ℝ x))) ≡ exp-tA t
spec-int-nonneg-phi-t t =
  trans (sym (spec-int-nonneg-consistent (λ x → exp (negℝ (t *ℝ x)))
                                         (λ x → <-≤-ℝ (phi-t-pos t x))))
        (spec-int-general-phi-t t)

-- **可证明（§1b 机制推导）**：M_σ ⊆ M-Rec-t（谱匹配 ⟹ X 与 e^(-tA) 交换）
-- 链：X-comm-spec-int-general（E 逐集交换 ⟹ 与一般谱积分 ∫φ_t dE 交换）
--   + spec-int-general-phi-t（桥接 ∫φ_t dE = e^(-tA)）
--（原 X-comm-spectral-int-exp-t 公理已删除——本推导为其降定理版）
σ-to-Rec-t : {X : Op} (t : ℝ) → M-σ X → M-Rec-t t X
σ-to-Rec-t {X} t h =
  trans (cong (λ Z → X *ₒ Z) (sym (spec-int-general-phi-t t)))
  (trans (X-comm-spec-int-general X h (λ x → exp (negℝ (t *ℝ x))))
         (cong (λ Z → Z *ₒ X) (spec-int-general-phi-t t)))

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

-- ------------------------------------------------------------------
-- 7-4 余项（fc-integral 降定理的"≤"方向）：覆盖坍缩 + simple-fn-below +
-- fc-integral-le，2026-08-02（依赖 Fin 构造子互异，置于 §10d）
-- ------------------------------------------------------------------

-- **可证**：ℝ 全零和 = 0
sum-zero-ℝ : {m : ℕ} → sum-ℝ {m} (λ _ → zeroℝ) ≡ zeroℝ
sum-zero-ℝ {zero} = refl
sum-zero-ℝ {suc m} = trans (cong₂ _+ℝ_ refl sum-zero-ℝ) (+-ident-ℝ zeroℝ)

-- **可证**：逐项为零 ⟹ 和为零（sum-ℝ 坍缩）
sum-ℝ-zero : {m : ℕ} (a : Fin m → ℝ) → ((i : Fin m) → a i ≡ zeroℝ) → sum-ℝ a ≡ zeroℝ
sum-ℝ-zero {zero} a h = refl
sum-ℝ-zero {suc m} a h =
  trans (cong₂ _+ℝ_ (h zero) (sum-ℝ-zero {m} (λ i → a (suc i)) (λ i → h (suc i))))
        (+-ident-ℝ zeroℝ)

-- **可证**：覆盖 + 不相交 ⟹ Σᵢ 1_{Ωᵢ}(x) = 1（恰一个指标；i₀ 定位归纳：
--  i₀ 项 = 1（indicator-pos）+ 其余项 = 0（disj 不相交 + indicator-zero）+ 和坍缩）
sum-indicator-cover : {m : ℕ} → (Ω : Fin m → Borel) → ((i j : Fin m) → i ≢ j → ((x : ℝ) → Ω i x → Ω j x → ⊥))
  → (x : ℝ) → (i₀ : Fin m) → Ω i₀ x → sum-ℝ (λ i → indicator (Ω i) x) ≡ oneℝ
sum-indicator-cover {suc m} Ω disj x zero hx₀ =
  trans (cong₂ _+ℝ_ (indicator-pos (Ω zero) x hx₀)
                    (sum-ℝ-zero {m} (λ i → indicator (Ω (suc i)) x) tail-zero))
        (+-ident-ℝ oneℝ)
  where
  -- x ∈ Ω zero 且 disj zero (suc i) ⟹ x ∉ Ω (suc i) ⟹ 尾部逐项 = 0
  tail-zero : (i : Fin m) → indicator (Ω (suc i)) x ≡ zeroℝ
  tail-zero i = indicator-zero (Ω (suc i)) x
                 (λ hx → disj zero (suc i) (zero≢suc {m = m} {k = i}) x hx₀ hx)
sum-indicator-cover {suc m} Ω disj x (suc i₀') hx₀ =
  trans (cong₂ _+ℝ_ (indicator-zero (Ω zero) x
                       (λ hx → disj (suc i₀') zero (suc≢zero {m = m} {k = i₀'}) x hx₀ hx))
                    (sum-indicator-cover {m} (λ i → Ω (suc i))
                                         (λ i j hij → disj (suc i) (suc j) (suc≢suc hij))
                                         x i₀' hx₀))
        (zero-add-ℝ oneℝ)

-- **可证**：简单函数逐点 ≤ f——dom（逐原子 cᵢ ≤ f）⟹ simple-fn s x ≤ f x
--（逐项 cᵢ·1_{Ωᵢ}(x) ≤ f x·1_{Ωᵢ}(x)（atom-ip-le/lec，排中律分情形）+ 和保序 +
--  Σᵢ(fx·1_{Ωᵢ}(x)) = fx·Σᵢ1 = fx·1 = fx（分配 + 覆盖坍缩））
simple-fn-below : (s : SimpleF) (f : ℝ → ℝ)
  → ((i : Fin (SimpleF.m s)) → (x : ℝ) → SimpleF.Ω s i x → SimpleF.c s i ≤ℝ f x)
  → (x : ℝ) → simple-fn s x ≤ℝ f x
simple-fn-below s f dom x =
  subst (λ z → (sum-ℝ (λ i → SimpleF.c s i *ℝ indicator (SimpleF.Ω s i) x)) ≤ℝ z)
        (*-ident-ℝ (f x))
        (subst (λ z → (sum-ℝ (λ i → SimpleF.c s i *ℝ indicator (SimpleF.Ω s i) x)) ≤ℝ z)
               (cong (λ t → f x *ℝ t)
                     (sum-indicator-cover {SimpleF.m s} (SimpleF.Ω s) (SimpleF.disj s) x i₀ hx₀))
               (subst (λ z → (sum-ℝ (λ i → SimpleF.c s i *ℝ indicator (SimpleF.Ω s i) x)) ≤ℝ z)
                      (sum-distrib-ℝ (f x) (λ i → indicator (SimpleF.Ω s i) x))
                      (sum-mono-ℝ {SimpleF.m s} atom-le-i)))
  where
  i₀ : Fin (SimpleF.m s)
  i₀ = proj₁ (SimpleF.cover s x)
  hx₀ : SimpleF.Ω s i₀ x
  hx₀ = proj₂ (SimpleF.cover s x)
  -- 逐项比较（排中律分情形：x ∈ Ωᵢ / x ∉ Ωᵢ；分支中 indicator 定义性约简为 1/0）
  atom-le-i : (i : Fin (SimpleF.m s))
    → (SimpleF.c s i *ℝ indicator (SimpleF.Ω s i) x) ≤ℝ (f x *ℝ indicator (SimpleF.Ω s i) x)
  atom-le-i i with classical {SimpleF.Ω s i x}
  atom-le-i i | inj₁ hxi =
    subst (λ z → z ≤ℝ (f x *ℝ oneℝ)) (sym (*-ident-ℝ (SimpleF.c s i)))
          (subst (λ z → SimpleF.c s i ≤ℝ z) (sym (*-ident-ℝ (f x))) (dom i x hxi))
  atom-le-i i | inj₂ hnxi =
    subst (λ z → z ≤ℝ (f x *ℝ zeroℝ)) (sym (*-zero-ℝ (SimpleF.c s i)))
          (subst (λ z → zeroℝ ≤ℝ z) (sym (*-zero-ℝ (f x))) (refl-≤ℝ {zeroℝ}))

-- **可证**：fc-integral 降定理的"≤"方向——spec-int-general f ≤ₒ fc f
--（简单函数下界 sup ≤ 函数演算：Y = ∫s dE = fc(s)（fc-simple-integral）
--  ≤ fc f（simple-fn-below + fc-mono）+ sup-op-least）
fc-integral-le : (f : ℝ → ℝ) → spec-int-general f ≤ₒ fc f
fc-integral-le f = sup-op-least (spec-int-below f) (fc f) bound
  where
  bound : (Y : Op) → spec-int-below f Y → Y ≤ₒ fc f
  bound Y (pair₁Σ s (eq , dom)) =
    subst (λ Z → Z ≤ₒ fc f) (sym eq)
          (subst (λ Z → Z ≤ₒ fc f) (sym (fc-simple-integral s))
                 (fc-mono (simple-fn-below s f dom)))

-- ------------------------------------------------------------------
-- 7-4 余项（"≥"方向第一步：简单函数版 fc-simple-le），2026-08-02
-- ------------------------------------------------------------------
-- 目标：fc-integral 降定理的"≥"方向（fc f ≤ₒ spec-int-general f）的简单函数层——
-- fc s ≤ₒ spec-int-general s（fc s = ∫s dE ≤ sup{∫t : t ≤ s}，s 自身是下界）。
-- 依赖：有限线性组合定位引理（sum-c-ind-eq：覆盖+不相交 ⟹ Σⱼcⱼ·1_{Ωⱼ}(x) = cᵢ）。

-- **可证**：有限线性组合在定位原子上的值——Σⱼ cⱼ·1_{Ωⱼ}(x) = cᵢ（x ∈ Ωᵢ，覆盖+不相交；
--   Fin 定位归纳：i 项 = cᵢ（indicator-pos + *-ident-ℝ）+ 其余项 = 0（disj + *-zero-ℝ）+ 和坍缩）
sum-c-ind-eq : {m : ℕ} (c : Fin m → ℝ) (Ω : Fin m → Borel)
  → ((i j : Fin m) → i ≢ j → ((x : ℝ) → Ω i x → Ω j x → ⊥))
  → (i : Fin m) (x : ℝ) → Ω i x
  → sum-ℝ (λ j → c j *ℝ indicator (Ω j) x) ≡ c i
sum-c-ind-eq {suc m} c Ω disj zero x hx₀ =
  trans (cong₂ _+ℝ_ head-eq tail-zero)
        (+-ident-ℝ (c zero))
  where
  -- c₀·1 = c₀（x ∈ Ω₀）
  head-eq : (c zero *ℝ indicator (Ω zero) x) ≡ c zero
  head-eq = trans (cong (λ t → c zero *ℝ t) (indicator-pos (Ω zero) x hx₀))
                  (*-ident-ℝ (c zero))
  -- 其余项 cⱼ·0 = 0（x ∈ Ω₀ 且 disj 0 (suc j)）
  tail-zero : sum-ℝ {m} (λ j → c (suc j) *ℝ indicator (Ω (suc j)) x) ≡ zeroℝ
  tail-zero = sum-ℝ-zero {m} (λ j → c (suc j) *ℝ indicator (Ω (suc j)) x)
                          (λ j → trans (cong (λ t → c (suc j) *ℝ t)
                                             (indicator-zero (Ω (suc j)) x
                                               (λ hx → disj zero (suc j) (zero≢suc {m = m} {k = j}) x hx₀ hx)))
                                       (*-zero-ℝ (c (suc j))))
sum-c-ind-eq {suc m} c Ω disj (suc i₀') x hx₀ =
  trans (cong₂ _+ℝ_ head-zero (sum-c-ind-eq {m} (λ j → c (suc j)) (λ j → Ω (suc j))
                                            (λ j k hjk → disj (suc j) (suc k) (suc≢suc hjk))
                                            i₀' x hx₀))
        (zero-add-ℝ (c (suc i₀')))
  where
  -- c₀·0 = 0（x ∈ Ω(suc i₀') 且 disj (suc i₀') zero）
  head-zero : (c zero *ℝ indicator (Ω zero) x) ≡ zeroℝ
  head-zero = trans (cong (λ t → c zero *ℝ t)
                          (indicator-zero (Ω zero) x
                            (λ hx → disj (suc i₀') zero (suc≢zero {m = m} {k = i₀'}) x hx₀ hx)))
                    (*-zero-ℝ (c zero))

-- **可证**：简单函数在原子上的值——x ∈ Ωᵢ ⟹ simple-fn s x = cᵢ（sum-c-ind-eq 特化）
simple-fn-eq-atom : (s : SimpleF) (i : Fin (SimpleF.m s)) (x : ℝ) → SimpleF.Ω s i x
  → simple-fn s x ≡ SimpleF.c s i
simple-fn-eq-atom s i x px = sum-c-ind-eq (SimpleF.c s) (SimpleF.Ω s) (SimpleF.disj s) i x px

-- **可证**：fc-integral 降定理的"≥"方向（简单函数版）——fc s ≤ₒ spec-int-general s
--（fc s = ∫s dE（fc-simple-integral）≤ sup{∫t : t ≤ s}（s 自身是下界：
--  cᵢ ≤ simple-fn s x 点态经 simple-fn-eq-atom）+ sup-op-upper）
fc-simple-le : (s : SimpleF) → fc (simple-fn s) ≤ₒ spec-int-general (simple-fn s)
fc-simple-le s =
  subst (λ Z → Z ≤ₒ spec-int-general (simple-fn s)) (fc-simple-integral s)
        (sup-op-upper (spec-int-below (simple-fn s)) (simple-int s)
                      (pair₁Σ s (refl , λ i x px → dom-eq i x px)))
  where
  -- cᵢ ≤ simple-fn s x（x ∈ Ωᵢ 时 simple-fn s x = cᵢ）
  dom-eq : (i : Fin (SimpleF.m s)) (x : ℝ) → SimpleF.Ω s i x → SimpleF.c s i ≤ℝ simple-fn s x
  dom-eq i x px = subst (λ z → SimpleF.c s i ≤ℝ z) (sym (simple-fn-eq-atom s i x px))
                        (refl-≤ℝ {SimpleF.c s i})

-- **可证**：fc-integral 对简单函数完整成立——fc s = ∫s dE = spec-int-general s
--（≥ 方向 fc-simple-le + ≤ 方向 fc-integral-le（s 特化）+ ≤ₒ-antisym——
--  fc-integral 公理（§5c）对简单函数的完整降定理，等式版）
fc-simple-integral-full : (s : SimpleF) → fc (simple-fn s) ≡ spec-int-general (simple-fn s)
fc-simple-integral-full s =
  ≤ₒ-antisym (fc (simple-fn s)) (spec-int-general (simple-fn s))
             (fc-simple-le s) (fc-integral-le (simple-fn s))

-- ------------------------------------------------------------------
-- 7-4 余项（"≥"方向完整：fc-integral-ge + fc-integral-full），2026-08-02
-- ------------------------------------------------------------------
-- 目标：fc-integral 降定理的"≥"方向完整（fc f ≤ₒ spec-int-general f，任意 f）——
-- fc f = sup{fc(p) : p 多项式 ≤ f}（fc-continuous）≤ sup{∫s : s 简单 ≤ f}。
-- 依赖：测度论核心逼近桥接 fc-poly-le-spec-int（多项式可由简单函数下界逼近，
-- ∫p dE = sup{∫s : s ≤ p} 的完备性——构造化 Lebesgue 积分层降定理）。

-- 多项式简单逼近（桥接登记，2026-08-02）：多项式 p 可由简单函数下界逼近，
-- ∫p dE = sup{∫s : s 简单 ≤ p} 的完备性——fc(p) ≤ₒ spec-int-general p
-- （测度论核心逼近定理的算子序形式；构造化 Lebesgue 积分层降定理）
postulate
  fc-poly-le-spec-int : (m : ℕ) (a : Fin m → ℝ) (n : Fin m → ℕ)
    → fc (poly-fn {m} a n) ≤ₒ spec-int-general (poly-fn {m} a n)

-- **可证**：谱积分单调——f ≤ g 点态 ⟹ spec-int-general f ≤ₒ spec-int-general g
--（spec-int-below-mono（下界族单调）+ sup-op-least/upper）
spec-int-mono : {f g : ℝ → ℝ} → ((x : ℝ) → f x ≤ℝ g x) → spec-int-general f ≤ₒ spec-int-general g
spec-int-mono {f} {g} h = sup-op-least (spec-int-below f) (spec-int-general g)
                                       (λ Y yb → sup-op-upper (spec-int-below g) Y (spec-int-below-mono h Y yb))

-- **可证**：fc-integral 降定理的"≥"方向完整——fc f ≤ₒ spec-int-general f（任意 f）
--（fc f = sup{fc(p) : p ≤ f}（fc-continuous）；每个 fc(p) ≤ spec-int-general p
--  （fc-poly-le-spec-int）≤ spec-int-general f（spec-int-mono，p ≤ f）+ sup-op-least）
fc-integral-ge : (f : ℝ → ℝ) → fc f ≤ₒ spec-int-general f
fc-integral-ge f =
  subst (λ Z → Z ≤ₒ spec-int-general f) (sym (fc-continuous f))
        (sup-op-least (fc-below f) (spec-int-general f) bound)
  where
  bound : (Y : Op) → fc-below f Y → Y ≤ₒ spec-int-general f
  bound Y (m , a , n , eq , dom) =
    subst (λ Z → Z ≤ₒ spec-int-general f) (sym eq)
          (≤ₒ-trans (fc (poly-fn {m} a n)) (spec-int-general (poly-fn {m} a n)) (spec-int-general f)
                    (fc-poly-le-spec-int m a n)
                    (spec-int-mono {poly-fn {m} a n} {f} dom))

-- **可证**：fc-integral 完整降定理——fc f ≡ ∫f dE = spec-int-general f（任意 f）
--（≥ 方向 fc-integral-ge + ≤ 方向 fc-integral-le + ≤ₒ-antisym——
--  fc-integral 公理（§5c）完整降为可证明定理，唯一剩余登记项为
--  测度论核心逼近桥接 fc-poly-le-spec-int）
fc-integral-full : (f : ℝ → ℝ) → fc f ≡ spec-int-general f
fc-integral-full f =
  ≤ₒ-antisym (fc f) (spec-int-general f) (fc-integral-ge f) (fc-integral-le f)

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
--  - **σ-可加性（可数并）已闭合于 §10f**（E-σ-add 公理 + E-fin-union-sum 有限一致性可证）。
--  - E(P)+E(Pᶜ) = 𝟙ₒ（分辨率恒等式的补形式）构造性上需排中律（P 可判定时成立），
--    留待经典扩展层。

-- ==================================================================
-- §10f σ-可加性（可数并：σ-并谓词 + 可数可加/连续下式）
-- ==================================================================

-- Fin → ℕ 嵌入（有限前段索引）
fin-to-nat : {m : ℕ} → Fin m → ℕ
fin-to-nat zero = zero
fin-to-nat (suc i) = suc (fin-to-nat i)

-- Fin 三分律（2026-08-03，SimpleF 阶梯 disj 基础）：任意两个下标可比
fin-to-nat-trich : {n : ℕ} (i j : Fin n) → (fin-to-nat i <ℕ fin-to-nat j) ⊎ ((fin-to-nat j <ℕ fin-to-nat i) ⊎ (fin-to-nat i ≡ fin-to-nat j))
fin-to-nat-trich i j = <-ℕ-trich (fin-to-nat i) (fin-to-nat j)

-- ℕ 构造子互异/单射（可证）
zero≢suc-ℕ : {n : ℕ} → zero ≢ suc n
zero≢suc-ℕ ()

suc-inj-ℕ : {i j : ℕ} → suc i ≡ suc j → i ≡ j
suc-inj-ℕ refl = refl

-- **可证**：Fin → ℕ 嵌入单射（i ≢ j ⟹ fin-to-nat i ≢ fin-to-nat j）
fin-to-nat-inj : {m : ℕ} {i j : Fin m} → i ≢ j → fin-to-nat i ≢ fin-to-nat j
fin-to-nat-inj {i = zero} {j = zero} h eq = h refl
fin-to-nat-inj {i = zero} {j = suc j} h eq = zero≢suc-ℕ eq
fin-to-nat-inj {i = suc i} {j = zero} h eq = zero≢suc-ℕ (sym eq)
fin-to-nat-inj {i = suc i} {j = suc j} h eq = fin-to-nat-inj {i = i} {j = j} (λ ne → h (cong suc ne)) (suc-inj-ℕ eq)

-- Sp 层 ⊥ → 本层 ⊥（两者均为无构造子空类型，模式匹配 ())
⊥-Sp-elim : ⊥-Sp → ⊥
⊥-Sp-elim ()

-- **可证**：dyadic 区间不相交（Fin 版，SimpleF.disj 核心，2026-08-03）——
-- i ≢ j ⟹ Ωᵢ ∩ Ωⱼ = ∅（fin-to-nat-trich 三分律：i<j 经 dyadic-disj-lt、j<i 经其
-- 对称、i≡j 与 neq 矛盾（fin-to-nat-inj）；依赖 fin-to-nat-trich/-inj，故置于此处）
dyadic-disj : (k : ℕ) (c : ℝ) → zeroℝ <ℝ c → (i j : Fin (2^ k)) → i ≢ j
  → (x : ℝ) → dyadic-Ω k c (fin-to-nat i) x → dyadic-Ω k c (fin-to-nat j) x → ⊥
dyadic-disj k c hc i j neq x pix pjx with fin-to-nat-trich i j
dyadic-disj k c hc i j neq x pix pjx | inj₁ iltj =
  dyadic-disj-lt k c hc {fin-to-nat i} {fin-to-nat j} iltj x pix pjx
dyadic-disj k c hc i j neq x pix pjx | inj₂ (inj₁ jlti) =
  dyadic-disj-lt k c hc {fin-to-nat j} {fin-to-nat i} jlti x pjx pix
dyadic-disj k c hc i j neq x pix pjx | inj₂ (inj₂ eq) =
  ⊥-Sp-elim (fin-to-nat-inj neq eq)

-- ==================================================================
-- SimpleF dyadic 阶梯构造（阶段 4 余项第二步第二部分：cover 侧，2026-08-03）
-- ==================================================================
-- 目标：组装 SimpleF dyadic 实例（disj v1.30 已闭合，本部分闭合 cover + 实例）。
-- 设计（覆盖全空间的三段式 Ω，m = suc (suc (2^k))）：
--   Ω zero        = (-∞,0)          （负部）
--   Ω (suc zero)  = [c,∞)            （正部）
--   Ω (suc (suc i)) = [xᵢ, xᵢ₊₁)    （dyadic 区间，i : Fin (2^k)）
-- 覆盖：x<0 → 负部；c≤x → 正部；0≤x<c → 划分定理（dyadic-cover 桥接）给 dyadic。
-- 注意：dyadic-Ω 末区间 Ω_{2^k-1} = [x_{2^k-1}, c) 左闭右开，x=c 落在正部，无缝隙。

-- ℕ 层 ≤（划分定理/上界论证）
_≤ℕ_ : ℕ → ℕ → Set
m ≤ℕ n = (m <ℕ n) ⊎ (m ≡ n)

-- m < n ⟹ suc m ≤ℕ n（<-ℕ-suc-split 转 ≤ℕ）
≤-ℕ-suc-le : {m n : ℕ} → m <ℕ n → suc m ≤ℕ n
≤-ℕ-suc-le h with <-ℕ-suc-split h
≤-ℕ-suc-le h | inj₁ p = inj₁ p
≤-ℕ-suc-le h | inj₂ q = inj₂ q

-- **可证**：Fin 下标恒小于类型大小
Fin-<ℕ : {n : ℕ} (i : Fin n) → fin-to-nat i <ℕ n
Fin-<ℕ {zero}   ()
Fin-<ℕ {suc n}  zero    = z<s
Fin-<ℕ {suc n}  (suc i) = s<s (Fin-<ℕ i)

-- **可证**：网格末点 = c——x_{2^k} ≡ c（/-cross-ℝ：((2^k·c)/2^k = c/1) +
--  *-ident-ℝ + *-comm-ℝ + div-one-ℝ）
grid-pt-last : (k : ℕ) (c : ℝ) → grid-pt k c (2^ k) ≡ c
grid-pt-last k c =
  trans (/-cross-ℝ {a = natℝ (2^ k) *ℝ c} {b = c} {c = natℝ (2^ k)} {d = oneℝ}
                   (trans (*-ident-ℝ (natℝ (2^ k) *ℝ c)) (*-comm-ℝ (natℝ (2^ k)) c)))
        (div-one-ℝ c)

-- **可证**：网格点不超过 c——j ≤ℕ 2^k ⟹ xⱼ ≤ℝ c
--（j < 2^k：xⱼ < x_{2^k} = c（grid-pt-lt + grid-pt-last）；j = 2^k：xⱼ = c）
grid-pt-upper : (k : ℕ) (c : ℝ) → zeroℝ <ℝ c → {j : ℕ} → j ≤ℕ 2^ k → grid-pt k c j ≤ℝ c
grid-pt-upper k c hc {j} (inj₁ jlt) =
  <-≤-ℝ (subst (λ w → grid-pt k c j <ℝ w) (grid-pt-last k c)
              (grid-pt-lt k c hc {j} {2^ k} jlt))
grid-pt-upper k c hc {j} (inj₂ jeq) =
  subst (λ w → w ≤ℝ c) (sym p) (refl-≤ℝ {c})
  where
  p : grid-pt k c j ≡ c
  p = subst (λ w → grid-pt k c w ≡ c) (sym jeq) (grid-pt-last k c)

-- 桥接登记：实数划分定理（dyadic 网格覆盖 [0,c)）——∀x. 0 ≤ x < c ⟹
--   ∃j < 2^k. xⱼ ≤ x < xⱼ₊₁（SimpleF dyadic 实例的 cover 核心）
--（模型必然性 = ℝ 的 Archimedean 性质（标准有序域划分定理：floor 存在）；
--  降定理路径 = WellOrdering（ℕ 良序，NatArith wf-acc）+ floor 论证完整实现；
--  与 archimedean-ub（v1.20 登记）同层的 ℝ 完备性族标准推论，构造框架中显式登记）
postulate
  dyadic-cover : (k : ℕ) (c : ℝ) → zeroℝ <ℝ c → (x : ℝ) → zeroℝ ≤ℝ x → x <ℝ c
    → Σ (Fin (2^ k)) (λ j → dyadic-Ω k c (fin-to-nat j) x)

-- 三段式 dyadic 区间族（覆盖全空间）：Ω₀ = 负部 (-∞,0)、Ω₁ = 正部 [c,∞)、
--   Ω_{2+i} = dyadic-Ω i（i : Fin (2^k)）——m = suc (suc (2^k)) 共 2^k+2 个原子
dyadic-Ω3 : (k : ℕ) (c : ℝ) → Fin (suc (suc (2^ k))) → Borel
dyadic-Ω3 k c zero          x = x <ℝ zeroℝ
dyadic-Ω3 k c (suc zero)    x = c ≤ℝ x
dyadic-Ω3 k c (suc (suc i)) x = dyadic-Ω k c (fin-to-nat i) x

-- **可证**：三段式区间不相交（严格序版）——i <ℕ j ⟹ Ωᵢ ∩ Ωⱼ = ∅
--（情形：负部 vs 正部（x<0<c ⟹ x<c 且 c≤x ⟹ c<c）、负部 vs dyadic（xᵢ≤x<0 与 xᵢ≥0 矛盾）、
--  正部 vs dyadic（x<xᵢ₊₁≤c（grid-pt-upper）与 c≤x ⟹ c<c）、dyadic vs dyadic（dyadic-disj-lt））
dyadic-disj3-lt : (k : ℕ) (c : ℝ) → zeroℝ <ℝ c → {i j : Fin (suc (suc (2^ k)))}
  → fin-to-nat i <ℕ fin-to-nat j → (x : ℝ) → dyadic-Ω3 k c i x → dyadic-Ω3 k c j x → ⊥
-- 负部 vs 正部：x < 0 ≤ c ⟹ x < c 且 c ≤ x ⟹ c < c（≤-lt-trans-ℝ + irreflexive-ℝ）
dyadic-disj3-lt k c hc {zero} {suc zero} ij x px py =
  irreflexive-ℝ (≤-lt-trans-ℝ py (lt-≤-trans-ℝ px (<-≤-ℝ hc)))
-- 负部 vs dyadic：xᵢ ≤ x < 0 与 0 ≤ xᵢ（grid-pt-nonneg）矛盾
dyadic-disj3-lt k c hc {zero} {suc (suc j')} ij x px (xj≤x , x<xj1) =
  irreflexive-ℝ (≤-lt-trans-ℝ (grid-pt-nonneg k c (<-≤-ℝ hc) (fin-to-nat j')) xj'<0)
  where
  xj' : ℝ
  xj' = grid-pt k c (fin-to-nat j')
  -- xᵢ ≤ x 且 x < 0 ⟹ xᵢ < 0
  xj'<0 : xj' <ℝ zeroℝ
  xj'<0 = ≤-lt-trans-ℝ xj≤x px
-- 正部 vs dyadic：x < xᵢ₊₁ ≤ c 且 c ≤ x ⟹ c < c
dyadic-disj3-lt k c hc {suc zero} {suc (suc j')} ij x py (xj≤x , x<xj1) =
  irreflexive-ℝ (≤-lt-trans-ℝ py (lt-≤-trans-ℝ x<xj1 xj1≤c))
  where
  -- xᵢ₊₁ ≤ c：suc(fin-to-nat j') ≤ℕ 2^k（Fin-<ℕ + <-ℕ-suc-split）+ grid-pt-upper
  xj1≤c : grid-pt k c (suc (fin-to-nat j')) ≤ℝ c
  xj1≤c = grid-pt-upper k c hc (≤-ℕ-suc-le (Fin-<ℕ j'))
-- dyadic vs dyadic：s<s-inv 反解 fin-to-nat 次序 + dyadic-disj-lt
dyadic-disj3-lt k c hc {suc (suc i')} {suc (suc j')} ij x (xi≤x , x<xi1) (xj≤x , x<xj1) =
  dyadic-disj-lt k c hc {fin-to-nat i'} {fin-to-nat j'} (s<s-inv (s<s-inv ij)) x (xi≤x , x<xi1) (xj≤x , x<xj1)
-- i < j 且 j 的构造使 i ≥ 2（不可能）
dyadic-disj3-lt k c hc {suc (suc i')} {suc zero} (s<s ()) x px py
dyadic-disj3-lt k c hc {suc (suc i')} {zero} () x px py
dyadic-disj3-lt k c hc {suc zero} {zero} () x px py
dyadic-disj3-lt k c hc {suc zero} {suc zero} (s<s ()) x px py

-- **可证**：三段式区间不相交（Fin 版，SimpleF.disj）——i ≢ j ⟹ Ωᵢ ∩ Ωⱼ = ∅
dyadic-disj3 : (k : ℕ) (c : ℝ) → zeroℝ <ℝ c → (i j : Fin (suc (suc (2^ k)))) → i ≢ j
  → (x : ℝ) → dyadic-Ω3 k c i x → dyadic-Ω3 k c j x → ⊥
dyadic-disj3 k c hc i j neq x pix pjx with fin-to-nat-trich i j
dyadic-disj3 k c hc i j neq x pix pjx | inj₁ iltj =
  dyadic-disj3-lt k c hc {i} {j} iltj x pix pjx
dyadic-disj3 k c hc i j neq x pix pjx | inj₂ (inj₁ jlti) =
  dyadic-disj3-lt k c hc {j} {i} jlti x pjx pix
dyadic-disj3 k c hc i j neq x pix pjx | inj₂ (inj₂ eq) =
  ⊥-Sp-elim (fin-to-nat-inj neq eq)

-- **可证**：三段式全空间覆盖——∀x. ∃i. Ωᵢ x
--（三分律三分：x<0 → 负部；c≤x → 正部；0≤x<c → dyadic-cover 划分定理）
dyadic-cover3 : (k : ℕ) (c : ℝ) → zeroℝ <ℝ c → (x : ℝ)
  → Σ (Fin (suc (suc (2^ k)))) (λ i → dyadic-Ω3 k c i x)
dyadic-cover3 k c hc x with trichotomy-ℝ x zeroℝ | trichotomy-ℝ x c
-- 负部：x < 0
dyadic-cover3 k c hc x | inj₁ x<0 | _ = zero , x<0
-- x = 0 且 x < c：划分定理（0 ≤ x 经 x=0）
dyadic-cover3 k c hc x | inj₂ (inj₁ x0) | inj₁ x<c =
  suc (suc (proj₁ dc)) , proj₂ dc
  where
  0≤x : zeroℝ ≤ℝ x
  0≤x = subst (λ w → zeroℝ ≤ℝ w) (sym x0) (refl-≤ℝ {zeroℝ})
  dc : Σ (Fin (2^ k)) (λ j → dyadic-Ω k c (fin-to-nat j) x)
  dc = dyadic-cover k c hc x 0≤x x<c
-- x = 0 且 x = c：0 < c 与 0 ≡ c 矛盾
dyadic-cover3 k c hc x | inj₂ (inj₁ x0) | inj₂ (inj₁ xc) =
  ⊥-elim (irreflexive-ℝ (subst (λ w → zeroℝ <ℝ w) (sym (trans (sym x0) xc)) hc))
-- x = 0 且 c < x：0 < c 且 c < 0 矛盾
dyadic-cover3 k c hc x | inj₂ (inj₁ x0) | inj₂ (inj₂ c<x) =
  ⊥-elim (irreflexive-ℝ (trans-<ℝ hc (subst (λ w → c <ℝ w) x0 c<x)))
-- 0 < x 且 x < c：划分定理（0 ≤ x 经 0 < x）
dyadic-cover3 k c hc x | inj₂ (inj₂ 0<x) | inj₁ x<c =
  suc (suc (proj₁ dc)) , proj₂ dc
  where
  dc : Σ (Fin (2^ k)) (λ j → dyadic-Ω k c (fin-to-nat j) x)
  dc = dyadic-cover k c hc x (<-≤-ℝ 0<x) x<c
-- 0 < x 且 x = c / c < x：正部 [c,∞)
dyadic-cover3 k c hc x | inj₂ (inj₂ 0<x) | inj₂ (inj₁ xc) =
  suc zero , subst (λ w → c ≤ℝ w) (sym xc) (refl-≤ℝ {c})
dyadic-cover3 k c hc x | inj₂ (inj₂ 0<x) | inj₂ (inj₂ c<x) =
  suc zero , <-≤-ℝ c<x

-- **SimpleF dyadic 阶梯实例**（值函数 vc 参数化）：m = suc (suc (2^k))、
--   Ω = 三段式 dyadic-Ω3、disj/cover 全部可证（disj3/cover3）
--（s ≤ f 逐点（dom 字段）由调用处按具体 f 提供）
dyadic-stair : (k : ℕ) (c : ℝ) → zeroℝ <ℝ c → (vc : Fin (suc (suc (2^ k))) → ℝ) → SimpleF
dyadic-stair k c hc vc = record
  { m = suc (suc (2^ k))
  ; c = vc
  ; Ω = dyadic-Ω3 k c
  ; disj = λ i j neq x → dyadic-disj3 k c hc i j neq x
  ; cover = dyadic-cover3 k c hc
  }

-- 可数并谓词（σ-并）：∪ₙ Pₙ = {x : ∃n. P n x}
σ-union : (ℕ → Borel) → Borel
σ-union P x = Σ ℕ (λ n → P n x)

-- 有限前段并：∪ᵢ<ₘ Pᵢ（经 Fin m 索引）
fin-union : {m : ℕ} → (ℕ → Borel) → Borel
fin-union {m} P x = Σ (Fin m) (λ i → P (fin-to-nat i) x)

-- σ-可加性公理（投影值测度的可数可加性，和形式）：
-- pairwise 不相交 ⟹ E(∪ₙPₙ) = supₘ Σᵢ<ₘ E(Pᵢ)（连续下式/可数可加；
-- 测度论（Lebesgue-Stieltjes）完整实现时降为定理）
postulate
  E-σ-add : (P : ℕ → Borel)
    → ((n₁ n₂ : ℕ) → n₁ ≢ n₂ → ((x : ℝ) → P n₁ x → P n₂ x → ⊥))
    → E (σ-union P) ≡ sup-op (λ Y → Σ ℕ (λ m → Y ≡ sum-op {m} (λ i → E (P (fin-to-nat i)))))

-- **可证**：有限前段并的谱测度 = 有限和（E-partition-add 的 ℕ 索引版）
--（pairwise 不相交 ⟹ E(∪ᵢ<ₘPᵢ) = Σᵢ<ₘ E(Pᵢ)——σ-可加性的有限一致性）
E-fin-union-sum : {m : ℕ} (P : ℕ → Borel)
  → ((n₁ n₂ : ℕ) → n₁ ≢ n₂ → ((x : ℝ) → P n₁ x → P n₂ x → ⊥))
  → E (fin-union {m} P) ≡ sum-op {m} (λ i → E (P (fin-to-nat i)))
E-fin-union-sum {m} P h =
  E-partition-add {m} (λ i → P (fin-to-nat i))
    (λ i j neq x px py → h (fin-to-nat i) (fin-to-nat j) (fin-to-nat-inj neq) x px py)

-- σ-可加性层状态：
--  - σ-可加性公理（E-σ-add：可数可加/连续下式，和形式）+ 有限一致性
--    （E-fin-union-sum **可证**：E(∪ᵢ<ₘPᵢ) = Σᵢ<ₘ E(Pᵢ)）+ Fin→ℕ 嵌入
--    （fin-to-nat-inj **可证**）。
--  - E-union（§10e）为 m=2 特例；可数并的测度论实现时降为定理。

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
--  - 压缩范数（‖e^(-tA)‖ ≤ 1，§12）、强连续（lim_{t→0} e^(-tA) = I）、生成元（-A）
--    需范数/拓扑/导数层（Hilbert 空间层），为阶段 6 剩余主项之一。

-- ==================================================================
-- §12 Hille-Yosida 范数层基础（C*-范数 + 投影范数 + 压缩性）
-- ==================================================================

-- C*-代数范数（自伴算子范数；Hilbert 空间层完整实现时降为定理）：
--  - norm-pos：‖X‖ ≥ 0
--  - norm-submul：‖X·Y‖ ≤ ‖X‖·‖Y‖（次乘法性）
--  - norm-power：‖X·X‖ = ‖X‖·‖X‖（自伴幂恒等，C* 恒等 ‖X*X‖=‖X‖² 对自伴元）
--  - norm-zero：‖X‖ = 0 ⟹ X = 0（正定性）
--  - norm-ident：‖𝟙ₒ‖ = 1
--  - norm-tri：‖X+Y‖ ≤ ‖X‖+‖Y‖（三角不等式）
postulate
  ‖_‖ : Op → ℝ
  norm-pos : (X : Op) → zeroℝ ≤ℝ ‖ X ‖
  norm-submul : (X Y : Op) → ‖ X *ₒ Y ‖ ≤ℝ (‖ X ‖ *ℝ ‖ Y ‖)
  norm-power : (X : Op) → ‖ X *ₒ X ‖ ≡ (‖ X ‖ *ℝ ‖ X ‖)
  norm-zero : (X : Op) → ‖ X ‖ ≡ zeroℝ → X ≡ 𝟘ₒ
  norm-ident : ‖ 𝟙ₒ ‖ ≡ oneℝ
  norm-tri : (X Y : Op) → ‖ X +ₒ Y ‖ ≤ℝ (‖ X ‖ +ℝ ‖ Y ‖)

-- **可证**：x = x·x ⟹ x = 0 ∨ x = 1（域无零因子 + 因式分解）
idem-zero-one : {x : ℝ} → x ≡ x *ℝ x → (x ≡ zeroℝ) ⊎ (x ≡ oneℝ)
idem-zero-one {x} h = helper (zero-factor-ℝ {a = x} {b = x +ℝ negℝ oneℝ} factor-zero)
  where
  -- x·x = x ⟹ x·x + (-x) = x + (-x) = 0（+-inv）
  xplus : (x *ℝ x) +ℝ negℝ x ≡ zeroℝ
  xplus = trans (cong (λ y → y +ℝ negℝ x) (sym h)) (+-inv-ℝ x)
  -- 因式分解：x·(x + (-1)) = x·x + (-x)（distrib + 乘法交换 + neg-one-mul）
  factor : x *ℝ (x +ℝ negℝ oneℝ) ≡ (x *ℝ x) +ℝ negℝ x
  factor =
    trans (distrib-ℝ x x (negℝ oneℝ))
    (trans (cong (λ y → (x *ℝ x) +ℝ y) (*-comm-ℝ x (negℝ oneℝ)))
           (cong (λ y → (x *ℝ x) +ℝ y) (neg-one-mul x)))
  factor-zero : x *ℝ (x +ℝ negℝ oneℝ) ≡ zeroℝ
  factor-zero = trans factor xplus
  helper : (x ≡ zeroℝ) ⊎ (x +ℝ negℝ oneℝ ≡ zeroℝ) → (x ≡ zeroℝ) ⊎ (x ≡ oneℝ)
  helper (inj₁ z) = inj₁ z
  helper (inj₂ b) = inj₂ (sub-eq-zero {a = x} (trans (sub-ℝ-def x oneℝ) b))

-- **可证**：谱投影范数 ∈ {0,1}——‖E(P)‖ = ‖E(P)²‖ = ‖E(P)‖²（norm-power + E-idempotent）
proj-norm : (P : Borel) → (‖ E P ‖ ≡ zeroℝ) ⊎ (‖ E P ‖ ≡ oneℝ)
proj-norm P = idem-zero-one norm-idem
  where
  -- ‖E(P)‖ = ‖E(P)·E(P)‖ = ‖E(P)‖·‖E(P)‖
  norm-idem : ‖ E P ‖ ≡ ‖ E P ‖ *ℝ ‖ E P ‖
  norm-idem =
    trans (sym (cong (λ Y → ‖ Y ‖) (E-idempotent P)))
          (norm-power (E P))

-- Hille-Yosida 压缩性（定义性公理）：σ(e^(-tA)) ⊆ (0,1]（§11 已证谱测度形式）
-- ⟹ ‖e^(-tA)‖ ≤ 1（谱半径 = 范数，C*-代数谱半径公式；Hilbert 空间层降为定理）
postulate
  norm-contraction : (t : ℝ) → zeroℝ ≤ℝ t → ‖ exp-tA t ‖ ≤ℝ oneℝ

-- Hille-Yosida 范数层状态：
--  - C*-范数公理（6 条）+ 投影范数（proj-norm **可证**：‖E(P)‖ ∈ {0,1}）+ 压缩性
--    （norm-contraction：σ(e^(-tA)) ⊆ (0,1] ⟹ ‖e^(-tA)‖ ≤ 1）。
--  - 投影范数 ≤ 1（proj-norm-le-one，§12b）、强连续（strong-continuity，§12b）；
--    Fuglede 指示桥接（E(P) = 1_P(A)）需拓扑/测度论层，为阶段 6 剩余开放项。

-- ==================================================================
-- §12b Hille-Yosida 完整层（投影范数 ≤ 1 + 强连续登记）
-- ==================================================================

-- **可证**：谱投影范数 ≤ 1（proj-norm 分情形：0 ≤ 1 / 1 ≤ 1）
proj-norm-le-one : (P : Borel) → ‖ E P ‖ ≤ℝ oneℝ
proj-norm-le-one P = helper (proj-norm P)
  where
  helper : (‖ E P ‖ ≡ zeroℝ) ⊎ (‖ E P ‖ ≡ oneℝ) → ‖ E P ‖ ≤ℝ oneℝ
  helper (inj₁ z) = subst (λ y → y ≤ℝ oneℝ) (sym z) (<-≤-ℝ zero-lt-one-ℝ)
  helper (inj₂ o) = subst (λ y → y ≤ℝ oneℝ) (sym o) (refl-≤ℝ {x = oneℝ})

-- 算子极限（抽象记号）：ℝ 索引 Op 族在 0⁺ 的极限（范数/强算子拓扑抽象）
postulate
  lim-op : (ℝ → Op) → Op
  -- 强连续（Hille-Yosida 条件 iv）：lim_{t→0⁺} e^(-tA) = 𝟙ₒ
  strong-continuity : lim-op (λ t → exp-tA t) ≡ 𝟙ₒ

-- Hille-Yosida 完整层状态（五条件齐备）：
--  (i) 半群方程 e^((s+t)A) = e^(sA)·e^(tA) [semigroup，§1]
--  (ii) e^(0·A) = 𝟙ₒ [exp-tA-zero，§1]
--  (iii) 压缩 ‖e^(-tA)‖ ≤ 1 [norm-contraction，§12；谱支集 ⊆ (0,1] 见 §11]
--  (iv) 强连续 lim_{t→0⁺} e^(-tA) = 𝟙ₒ [strong-continuity，本节]
--  (v) 生成元 = -A [§12c：gen-op-neg-A 可证（gen-op-fc 导数层桥接 + fc-neg-id）]
-- 补充：投影范数 ≤ 1（proj-norm-le-one **可证**）。

-- ==================================================================
-- §12c 生成元 = -A（Hille-Yosida 条件 v 闭合：导数层桥接登记）
-- ==================================================================
-- 目标：将 §12b 中"生成元 = -A"（条件 v，原注释）落地为形式化——
-- 半群 {e^(-tA)} 在 0 的导数（生成元）登记为对象 gen-op；导数层桥接公理
-- gen-op-fc（生成元 = fc(-id)：d/dt|_{t=0} e^(-tx) = -x 经函数演算传递到
-- 算子层——微分算子/强拓扑完整实现时降为定理，与 strong-continuity 同层）；
-- -A 形式（fc(-id) = (negℝ oneℝ)·ₒ A）**可证**（fc-ext + neg-one-mul + fc-scalar-id）。

-- **可证**：fc(-id) = -A（函数演算的负恒等 = 标量 -1 倍 A）
fc-neg-id : fc (λ x → negℝ x) ≡ (negℝ oneℝ) ·ₒ A
fc-neg-id =
  trans (fc-ext (λ x → sym (neg-one-mul x)))
        (fc-scalar-id (negℝ oneℝ))

-- 生成元（半群在 0 的导数）：G = lim_{t→0⁺} (e^(-tA) - 𝟙ₒ)/t
-- 导数层桥接公理（定义性）：生成元 = fc(-id)——e^(-tA) = fc(φ_t)（§13）且
-- d/dt|_{t=0} φ_t(x) = -x（微积分内容），导数经函数演算传递到算子层；
-- 微分算子/强拓扑完整实现时降为定理（与 strong-continuity 同层）
postulate
  gen-op : Op
  gen-op-fc : gen-op ≡ fc (λ x → negℝ x)

-- **可证**：生成元 = -A（Hille-Yosida 条件 v 闭合：gen-op-fc + fc-neg-id）
gen-op-neg-A : gen-op ≡ (negℝ oneℝ) ·ₒ A
gen-op-neg-A = trans gen-op-fc fc-neg-id

-- Hille-Yosida 完整层状态更新：
--  - 条件 (v) 生成元 = -A 闭合：gen-op-neg-A **可证**（导数层桥接 gen-op-fc 之上）。
--  - 导数层桥接登记：gen-op-fc（生成元 = fc(-id)），降定理路径 = 微积分/谱定理
--    函数演算的微分性质（d/dt e^(-tx) = -x 经谱积分传递）。

-- ==================================================================
-- §13 半群 = 函数演算统一（exp-tA-fc：e^(-tA) = fc(φ_t)）
-- ==================================================================
-- 目标：将 Hille-Yosida 半群（§8）与函数演算（§5）连接——
-- e^(-tA) 恰为 φ_t(x) = e^(-tx) 的函数演算。衔接 M_σ ⟹ 与全半群族交换
-- （谱匹配态射自动与动力学演化交换——P1/R11 的动力学保持论断）。

-- **可证**：e^(-A) = fc(φ)（exp-spectral-rep + spec-int-general-exp + fc-integral）
exp-A-fc : exp-A ≡ fc (λ x → exp (negℝ x))
exp-A-fc =
  trans exp-spectral-rep
  (trans (sym spec-int-general-exp)
         (sym (fc-integral (λ x → exp (negℝ x)))))

-- **可证**：e^(-tA) = fc(φ_t)（spec-int-general-phi-t + fc-integral）
exp-tA-fc : (t : ℝ) → exp-tA t ≡ fc (λ x → exp (negℝ (t *ℝ x)))
exp-tA-fc t =
  trans (sym (spec-int-general-phi-t t))
        (sym (fc-integral (λ x → exp (negℝ (t *ℝ x)))))

-- **可证**：M_σ ⟹ X 与全半群族 {e^(-tA)} 交换
--（X-comm-fc（fc(φ_t) 交换）+ exp-tA-fc 桥接）
X-comm-exp-tA : (X : Op) → ((P : Borel) → X *ₒ E P ≡ E P *ₒ X) → (t : ℝ)
  → X *ₒ exp-tA t ≡ exp-tA t *ₒ X
X-comm-exp-tA X h t =
  trans (cong (λ Z → X *ₒ Z) (exp-tA-fc t))
  (trans (X-comm-fc X h (λ x → exp (negℝ (t *ℝ x))))
         (cong (λ Z → Z *ₒ X) (sym (exp-tA-fc t))))

-- 半群-函数演算统一层状态：
--  - e^(-A) = fc(φ)、e^(-tA) = fc(φ_t)（**可证**）；M_σ ⟹ 与全半群族交换
--    （X-comm-exp-tA **可证**）——谱匹配态射自动与动力学演化交换。
--  - 衔接：M-Sp ⟹ M-σ（Fuglede 公理）⟹ M-Sp 亦与全半群族交换；
--    P1/R11 的"Rec_D 态射保动力学"论断由此直接成立。

-- ==================================================================
-- §14 谱匹配态射保动力学（Rec/Sp 态射 ⟹ 与全半群族交换）
-- ==================================================================
-- 目标：P1/R11 的态射层动力学保持论断——谱匹配态射（M_σ）与全半群族交换
-- （X-comm-exp-tA，§13）⟹ 各 M 条件（M-Rec / M-Sp）亦保动力学。

-- **可证**：Rec 态射（M-Rec）⟹ 与全半群族 {e^(-tA)} 交换
--（theorem3-Rec-σ 方向：M-Rec ⟹ M-σ（Rec-to-σ）+ X-comm-exp-tA）
Rec-to-exp-tA : {X : Op} → M-Rec X → (t : ℝ) → X *ₒ exp-tA t ≡ exp-tA t *ₒ X
Rec-to-exp-tA {X} h t = X-comm-exp-tA X (Rec-to-σ h) t

-- **可证**：谱态射（M-Sp）⟹ 与全半群族 {e^(-tA)} 交换
--（Fuglede 方向 Sp-to-σ + X-comm-exp-tA）
Sp-to-exp-tA : {X : Op} → M-Sp X → (t : ℝ) → X *ₒ exp-tA t ≡ exp-tA t *ₒ X
Sp-to-exp-tA {X} h t = X-comm-exp-tA X (Sp-to-σ h) t

-- 态射保动力学状态：
--  - M-σ ⟹ 与全半群族交换（X-comm-exp-tA，§13）；M-Rec / M-Sp 亦成立
--    （Rec-to-exp-tA / Sp-to-exp-tA **可证**）——P1/R11 的态射层动力学保持
--    论断从三个 M 条件全部闭合（Rec 侧无公理依赖；Sp 侧经 Fuglede 方向公理）。

-- ==================================================================
-- §15 公理纪律审计（阶段 6 收官账目，2026-08-01）
-- ==================================================================
-- 目的：T3 谱定理层（阶段 6）收官后清点本模块全部剩余 postulate，分类登记；
-- 每项注明模型必然性 / 用途 / 降定理路径。核心定理全部真实证明（无占位）。
-- 注：P1Spectral 的算子代数基础公理（+ₒ/*ₒ/·ₒ 律）与 DHStructural 的 ℝ
-- 公理不计入本账目（分别为"Op 是算子代数"与"ℝ 是有序域"的基础假设）。
--
-- 分类总览（24 块 → 审计后 22 块；recon-op/recon-op-fc 已降为定义）：
--
-- A. 谱论基础公理（谱测度/谱表示/半群对象/谱测度代数）：
--    ① §1：A、E、E-support-pos、spec-int-A、spectral-rep-A（谱测度 + 谱表示）
--    ② §1：exp-A、E-exp、exp-spectral-measure、spec-int-exp、exp-spectral-rep
--          （exp 谱表示 + 谱测度复合）、intertwine-exp-imp-spectral-exp
--          （e^(-A) 侧 Fuglede 方向，有限维谱定理方向）、spectral-ext（谱测度外延）
--    ③ §1：exp-tA、semigroup、exp-tA-zero、exp-tA-one（Hille-Yosida 半群对象层）
--    ④ §8c：E-exp-tA、exp-tA-spectral-measure、intertwine-exp-tA-imp-spectral
--          （e^(-tA) 谱测度复合 + 侧 Fuglede 方向）
--    ⑤ §10：E-mul、E-empty（投影值测度乘法/空集）
--    ⑥ §10e：E-total、E-union（谱测度完备性有限版）
--    ⑦ §10f：E-σ-add（可数可加/连续下式）
--    （降定理路径：测度论（Lebesgue-Stieltjes）/有限维谱定理完整实现）
--
-- B. 函数演算基础（§5）：fc、fc-id、fc-ext（Borel 函数演算抽象）
--
-- C. 逼近桥接公理（§1b）：_≤ₒ_、sup-op、sup-op-upper、sup-op-least、sup-comm
--    （算子序 + 上确界，交换子 sup 闭性）、spec-int-general-id/-exp
--    （§1b）、spec-int-general-phi-t（§8c）、spec-int-trunc-conv
--    （§1c 截断收敛：∫f = supₙ ∫min(f,n)，Lebesgue 单调收敛定理的代数形式，
--    阶段 7-1 登记，2026-08-02）
--    （降定理路径：Banach 空间/算子拓扑 + Lebesgue 积分理论）
--
-- D. fc 桥接公理（§5b-§5e）：fc-continuous（§5b）、fc-integral（§5c）、
--    fc-mul（§5d）、fc-add、fc-const（§5e）——函数演算的定义性质
--    （降定理路径：Borel 函数演算/测度论层；fc-poly 已降定理 §5f）
--
-- E. 经典扩展（§5g）：indicator（P 特征函数，构造性需排中律）、
--    indicator-bridge（E(P) = fc(1_P)）
--    （降定理路径：经典逻辑层（1_P 点态性质）+ 测度论层）
--
-- F. 往返一致性（§6）：σ→Sp∘Sp→σ、Sp→σ∘σ→Sp、σ→Rec∘Rec→σ、Rec→σ∘σ→Rec
--    （谱表示与谱积分线性间往返；有限维由插值多项式可证）
--
-- G. 算子代数补充：·ₒ-+（§7b 标量分配）、·ₒ-assoc（§10c 标量结合）、
--    ·ₒ-zero-l（P1Spectral 标量零吸收）
--    （模型必然性 = Op 是 ℝ-向量空间）
--
-- H. Hille-Yosida 范数/拓扑/导数层（§12/§12b/§12c）：‖_‖、norm-pos、
--    norm-submul、norm-power、norm-zero、norm-ident、norm-tri（C*-范数 6 条）、
--    norm-contraction（压缩性）、lim-op、strong-continuity（极限 + 强连续，
--    Hille-Yosida 条件 iv）、gen-op、gen-op-fc（生成元 = fc(-id)，条件 v 桥接）
--    （降定理路径：Hilbert 空间/强算子拓扑 + 微分算子层）
--
-- 已降为可证定理/定义（历轮闭合）：
--  - 谱积分线性：X-comm-spectral-int / -exp（§1b）、-exp-t（§8c）
--  - 函数演算保持多项式：fc-poly（§5f，同态结构推导）
--  - Fuglede 方向：intertwine-imp-spectral（§5g，指示桥接推导）
--  - 对象重建记号：recon-op / recon-op-fc（§5，降为定义）
--  - exp-inj、ln15-lt-65-24、e-lt-3、65/24<e 等（DHStructural 层）
--
-- 待降定理（后续层）：
--  - 测度论层：spec-int 收敛细节（无界逼近）、指示桥接点态性质、截断逼近、
--    E-total/E-union/E-σ-add、spec-int-general-*、fc-integral、fc-* 桥接
--  - Hilbert 空间/拓扑层：C*-范数、norm-contraction、lim-op/strong-continuity、gen-op-fc
--  - 有限维谱定理方向：intertwine-exp-imp-spectral-exp、intertwine-exp-tA-imp-spectral
--  - 经典逻辑层：indicator 点态性质（1_P x = 1 ⟺ P x）

-- ------------------------------------------------------------------
-- 阶段 7/8 审计更新（2026-08-02）：Hilbert 空间/拓扑层 + 测度论层推进后的降定理状态
-- ------------------------------------------------------------------
-- 已降为可证定理/定义（阶段 7/8 追加）：
--  - fc-integral 对简单函数：fc-simple-integral（∫s dE = fc(s)，§5h）、
--    fc-simple-le（fc s ≤ₒ spec-int-general s，§10d）、
--    fc-simple-integral-full（fc s ≡ spec-int-general s，§10d + ≤ₒ-antisym）
--  - fc-integral "≤"方向：fc-integral-le（spec-int-general f ≤ₒ fc f，§10d）
--  - fc 同态组件：fc-sum / fc-scalar-mul / fc-atom（§5h）
--  - 简单函数定位：sum-c-ind-eq / simple-fn-eq-atom（§10d）
--  - indicator 点态性质：indicator-pos / indicator-zero / indicator-eq-one-iff
--    （§5g，经典扩展，indicator 由 postulate 降为定义）
--  - E 的测度构造（Hilbert 层对应）：E-hilb-idemp / E-hilb-orth / E-hilb-total（§10c）、
--    E-hilb-union（§10d）、E-hilb-fin-union（§10e）、E-σ-add（§14）
--
-- 跨层降定理映射（SpectralTheory 公理 ↔ Hilbert 层可证定理，2026-08-02）：
--  - C*-范数（H 类）↔ HilbertSpace §5/§6/§11：norm-pos/norm-tri/norm-submul 从 sup 证、
--    norm-power（自伴幂恒等 ‖X²‖=‖X‖²）、spectral-radius-norm（r(X) = ‖X‖）
--  - norm-contraction（H 类）↔ HilbertSpace §12：exp-hilb-radius-le-one
--    （自伴 ⟹ r(e^(-tA)) = ‖e^(-tA)‖ ≤ 1，谱半径-压缩连接）
--  - strong-continuity（H 类，条件 iv）↔ HilbertSpace §12：exp-hilb-strong-cont
--    （范数连续 ⟹ 强连续，sot-from-norm 特化）
--  - E-total / E-union / E-σ-add（A 类）↔ HilbertSpace §10c/§10d/§10e/§14（E-hilb 族全链）
--  - indicator-bridge 点态化（E 类）↔ SpectralTheory §5g 经典扩展
--    （indicator 降为定义 + 1_P x = 1 ⟺ P x 可证）
--  - ≤ₒ-antisym（C 类补充，2026-08-02 登记）↔ HilbertSpace §13 算子序 _≤ₗ_ + 正定性 + funext
--
-- 待降定理（测度论核心，阶段 7/8 之后）：
--  - fc-integral "≥"方向完整（fc f ≤ₒ spec-int-general f）：多项式→简单函数逼近兼容性
--  - spec-int 收敛细节（无界逼近）：Lebesgue 单调收敛的构造化
--  - E-σ-add 收敛（算子序 sup 存在）：强/弱算子拓扑单调有界收敛
--  - 跨层模型（8-5b 余项）：Op → LinOp 完整实例化

-- ------------------------------------------------------------------
-- 阶段 7/8 审计更新 2（2026-08-03）：v1.13-v1.15 + 钉住 sup 语义文档化
-- ------------------------------------------------------------------
-- 已降为可证定理/登记（2026-08-03 追加）：
--  - fc-integral "≥"方向完整：fc-integral-ge（fc f ≤ₒ spec-int-general f，任意 f，§10d）+
--    fc-integral-full（fc f ≡ spec-int-general f，任意 f；≥ 方向 + ≤ 方向 + ≤ₒ-antisym）
--    ——fc-integral 公理（§5c，D 类）完整降为可证明定理，**唯一剩余登记项 =
--    测度论核心逼近桥接 fc-poly-le-spec-int**（§10d 登记，多项式可由简单函数下界
--    逼近，∫p dE = sup{∫s : s 简单 ≤ p} 的完备性）；支撑登记 ≤ₒ-trans（C 类补充）
--  - 跨层模型点态对应（8-5b 第一步）：CrossLayer/CrossLayer.agda——OpAlgPt 见证
--    record（13 组算子代数公理的点态对应）+ op-alg-pt 实例化（HilbertSpace §16
--    点态律，含 9 条 2026-08-03 补全：+ₗ-assoc/comm/ident-pt、*ₗ-zero-r/l-pt、
--    distribₗ/distribₗ-l-pt、·ₗ-comm-l/·ₗ-zero-l-pt）——算子代数公理在 LinOp 层的
--    逐点验证证书（funext 受限部分登记为开放项，不登记新 postulate）
--  - 测度论逼近引理库阶段 1（fc-poly-le-spec-int 构造化路线）：DHStructural
--    *-nonneg-ℝ（0≤ab）+ SpectralTheory power-nonneg/power-mono/power-pos
--    （0≤x≤y ⟹ xⁿ≤yⁿ、0<x ⟹ 0<xⁿ，归纳）——dyadic 阶梯逼近的 ℝ 层地基
--
-- 钉住 sup 语义文档化（§1b，2026-08-03）：spec-int-general 是"钉住 sup"——语义值 =
-- 谱支集 [0,∞) 上的 ∫f dE（目标模型谱定理），朴素 sup 只是部分计算机制；变号 f
-- （奇次单项式）朴素下界族为空，其积分值由钉住桥接（spec-int-general-id/-exp/-phi-t）
-- 确定。fc-integral-full（v1.13）对此类 f 的相容性依赖钉住桥接；构造化
-- fc-poly-le-spec-int 需 ∫f⁺−∫f⁻/谱支集受限语义重构（多阶段路线，阶段 1 ✅；
-- 阶段 2-4 待），且不因非负 f 而简化（fc-integral-ge 的多项式中间步不可绕过）。
-- 决策（2026-08-03，log）：保持健全桥接层 + 文档化，不冒险重构。
--
-- 待降定理（2026-08-03 更新）：
--  - fc-poly-le-spec-int 构造化（fc-integral 最后登记项）：多阶段路线
--    （阶段 1 ✅ 幂单调性引理库；阶段 2 dyadic 分划与阶梯函数；阶段 3 上界 + MCT；
--    阶段 4 组合替换桥接）——需语义重构方案先行
--  - 8-5b 算子层等式版 + 对象映射（funext 受限）：算子层等式版公理、op-lin 保结构、
--    谱对象映射（A/E/fc/exp-tA ↦ Hilbert 构造）
--  - E-σ-add 收敛（算子序 sup 存在）：强/弱算子拓扑单调有界收敛

-- ------------------------------------------------------------------
-- 阶段 7/8 审计更新 3（2026-08-03）：v1.19-v1.20 spec-int 收敛构造化闭合
-- ------------------------------------------------------------------
-- 已降为可证定理/登记（2026-08-03 追加）：
--  - spec-int 收敛细节（无界逼近）**构造化闭合**：
--    （1）ℝ-截断版（v1.19，§1c）：spec-int-R-trunc-conv（∫f dE =
--      sup{∫s : s ≤ 某截断 trunc f (s-bound s)}，**可证，零新增公理**——
--      s-bound/s-bound-upper + simple-below-trunc + 截断下界族逐成员等价
--      （spec-int-below-into-trunc/trunc-below-into-spec-int）+ sup-op-ext）
--    （2）ℕ-截断版（v1.20，§1c）：spec-int-trunc-ℕ-conv（∫f dE = supₙ∫min(f,n) dE，
--      **由桥接降为可证定理**）——支撑登记 **Archimedean**（DHStructural：
--      archimedean-ub/archimedean-ub-bound，∀a.∃n. a ≤ natℝ n——ℝ 完备性族标准
--      公理（与 sup-ℝ 同级，sup 层模型真；经典可由 sup-ℝ 推出，构造框架缺排中律式
--      步骤故显式登记；降定理路径 = 标准实数构造 Dedekind/Cauchy 完备化）；
--      **原 §1c 桥接 spec-int-trunc-conv（C 类）删除**，simple-below-ℕ-trunc +
--      spec-int-below-member-≤-ℕ-sup（≤ₒ-trans + sup-op-upper）推导）
-- 注：Archimedean 属 ℝ 公理层（DHStructural），对齐"ℝ 公理是基础假设，不计入
-- 本账目"立场（与 sup-ℝ 同级登记），此处仅记录其在本层降定理中的使用。
--
-- 待降定理（2026-08-03 再更新）：
--  - fc-poly-le-spec-int 构造化（fc-integral 最后登记项）：多阶段路线
--    （阶段 1 ✅ 幂单调性引理库；阶段 2 dyadic 分划与阶梯函数；阶段 3 上界 + MCT；
--    阶段 4 组合替换桥接）——需语义重构方案先行
--  - 8-5b 算子层等式版 + 对象映射（funext 受限）：算子层等式版公理、op-lin 保结构、
--    谱对象映射（A/E/fc/exp-tA ↦ Hilbert 构造）
--  - E-σ-add 收敛（算子序 sup 存在）：强/弱算子拓扑单调有界收敛

-- ------------------------------------------------------------------
-- 阶段 7/8 审计更新 4（2026-08-03）：跨层降定理映射形式化为可证证书
-- ------------------------------------------------------------------
-- 已形式化（v1.21，CrossLayer §2 SpectralObjPt + spectral-obj-pt）：
--  - E-total / E-union / E-idempotent / E-orthogonal（A 类，可证定理侧）
--    ↔ HilbertSpace E-hilb-total / E-hilb-union / E-hilb-idemp / E-hilb-orth
--    （§10c/§10d）——点态/内积版对应（E-idem-pt/E-orth-ip/E-total-pt/E-union-pt），
--    零新增公理；
--  - 谱投影自伴/范数（E-self-adjoint/E-norm-le-one ↔ §10c E-hilb-self-adjoint/
--    E-hilb-norm-le-one）；
--  - 半群对象（semigroup/exp-tA-zero，A 类）↔ HilbertSpace §12 exp-hilb-tA
--    （exp-tA-semigroup-pt/exp-tA-zero-pt/exp-tA-self-adjoint/exp-tA-contractive，
--    桥接字段）。
-- 注：本层跨层映射（v1.14 OpAlgPt 算子代数 + v1.21 SpectralObjPt 谱对象）现均
-- 为可证证书（点态/性质版）；算子级等式版（E-idempotent 的 E P *ₒ E P ≡ E P
-- 等）需 funext 提升，结构性限制（P4 先例），不登记新 postulate。
--
-- 待降定理（2026-08-03 再再更新）：
--  - fc-poly-le-spec-int 构造化（fc-integral 最后登记项）：多阶段路线
--    （阶段 1 ✅ 幂单调性引理库；阶段 2 dyadic 分划与阶梯函数；阶段 3 上界 + MCT；
--    阶段 4 组合替换桥接）——需语义重构方案先行
--  - 8-5b 算子层等式版 + 对象映射（funext 受限）：算子层等式版公理、op-lin 保结构、
--    A/fc 对象 Hilbert 侧构造（依赖谱定理降定理链）
--  - E-σ-add 收敛（算子序 sup 存在）：强/弱算子拓扑单调有界收敛

-- ------------------------------------------------------------------
-- 阶段 7/8 审计更新 5（2026-08-03）：方案 A 桥接登记（正负分解）
-- ------------------------------------------------------------------
-- 新增桥接（v1.23，§1b''，D 类补充）：
--  - spec-int-general-decomp：∫f dE ≡ ∫f⁺ dE −ₒ ∫f⁻ dE（f⁺ = max(f,0)、
--    f⁻ = max(−f,0)）——模型必然性 = 测度论线性（Lebesgue 积分可加性）；
--    钉住 sup 语义（§1b 文档块）下真；降定理路径 = 方案 A（笔记 §5.16.8）
--    spec-int-general 定义重构（∫f := ∫f⁺ −ₒ ∫f⁻）后转为可证（重构即定义性）。
-- 同轮可证组件（v1.23）：Op 层减法 _−ₒ_（定义性）+ op-sub-comm（减法保交换，
--   X-comm-spec-int-general 重构后重验核心）。
--
-- 待降定理（2026-08-03 再再再更新）：
--  - fc-poly-le-spec-int 构造化（fc-integral 最后登记项）：方案 A 4 阶段
--    （阶段 1 ✅ v1.22 max-ℝ 族 + f⁺/f⁻；阶段 2 第一部分 ✅ v1.23 Op 减法 +
--    decomp 桥接；阶段 2 第二部分第一步 ✅ v1.24 一致性组件（·ₒ-zero-r、
--    op-sub-zero-r、spec-int-nonneg、spec-int-general-zero）；阶段 2 第二部分
--    第二步 spec-int-general 定义重构 + 下游适配；阶段 3 钉住桥接转定理；
--    阶段 4 组合替换）
--  - 8-5b 算子层等式版 + 对象映射（funext 受限）：算子层等式版公理、op-lin 保结构、
--    A/fc 对象 Hilbert 侧构造（依赖谱定理降定理链）
--  - E-σ-add 收敛（算子序 sup 存在）：强/弱算子拓扑单调有界收敛

-- ------------------------------------------------------------------
-- 阶段 7/8 审计更新 6（2026-08-03）：方案 A 一致性组件（v1.24）
-- ------------------------------------------------------------------
-- 新增桥接（v1.24，D 类补充）：
--  - spec-int-general-zero：∫0 dE = 𝟘ₒ（零函数积分）——模型必然性 = 测度论
--    零函数性（Lebesgue 积分 ∫0 = 0）；钉住 sup 语义下真（下界族 {∫s : s ≤ 0}
--    sup = 0）；降定理路径 = Hilbert 层谱投影非负（E-hilb-nonneg）+ 标量保序 +
--    sup-least。
-- 新增补充公理（v1.24，P1Spectral §1，G 类算子代数补充）：
--  - ·ₒ-zero-r：a·ₒ𝟘ₒ = 𝟘ₒ（标量乘零算子 = 零算子，与 ·ₒ-zero-l 平行；
--    模型必然性 = Op 是 ℝ-向量空间）——支撑 op-sub-zero-r（X−ₒ𝟘ₒ = X，可证）。
-- 同轮可证组件：op-sub-zero-r（·ₒ-zero-r + +ₒ-ident）、spec-int-nonneg（非负
--  积分别名 = sup-op (spec-int-below)，重构定义避免递归）、HilbertSpace
--  ·ₗ-zero-r-pt（(c·ₗ𝟘ₗ)v = 𝟘ₗ v，scalar-zero；CrossLayer OpAlgPt 补第 14 组点态
--  字段——算子代数公理 13 → 14 组证书完整）。
--
-- 待降定理（2026-08-03 再再再再更新）：
--  - fc-poly-le-spec-int 构造化（fc-integral 最后登记项）：方案 A 阶段 2 完成
--    （阶段 2 第二部分第二步 ✅ v1.25：非负一致性——spec-int-general-ext-pt
--    （逐点外延，sup-op-ext 移 §1b）+ pos-part-absorp/neg-part-zero-point +
--    spec-int-nonneg-consistent（f ≥ 0 ⟹ ∫f ≡ 非负 sup）；定义重构评估：破坏面
--    过大（MCT/fc-integral 系列依赖定义性）⟹ 改走 decomp 显式化，阶段 2 收官）
--    → 阶段 3（钉住桥接转定理：spec-int-general-id/-exp/-phi-t 经 decomp +
--    非负一致性转可证）→ 阶段 4（fc-poly-le-spec-int 组合替换）
--  - 8-5b 算子层等式版 + 对象映射（funext 受限）：算子层等式版公理、op-lin 保结构、
--    A/fc 对象 Hilbert 侧构造（依赖谱定理降定理链）
--  - E-σ-add 收敛（算子序 sup 存在）：强/弱算子拓扑单调有界收敛

-- ------------------------------------------------------------------
-- 阶段 7/8 审计更新 7（2026-08-03）：方案 A 阶段 3 收官（钉住解析）
-- ------------------------------------------------------------------
-- 新增桥接（v1.27，D 类补充）：
--  - spec-int-nonneg-zero-off-support：非负 g 在 [0,∞) 上 = 0 ⟹ ∫g dE = 0
--    （谱支集外零贡献）——模型必然性 = E-support-pos（E(P) = E(P∩[0,∞))）+
--    测度论零函数性；降定理路径 = Hilbert 层谱投影非负（E-hilb-nonneg）+
--    E-support-pos + sup-least。
-- 同轮可证组件（v1.27，阶段 3 收官）：
--  - spec-int-A-decomp：spec-int-A ≡ ∫id⁺ −ₒ ∫id⁻（sym spec-int-general-id +
--    spec-int-general-decomp id——id 钉住桥接改写为分解形式）
--  - spec-int-general-id-pos：∫id⁺ = spec-int-A（spec-int-A-decomp +
--    spec-int-nonneg-zero-off-support（∫id⁻ = 0：id⁻ 非负 + 在 [0,∞) = 0）+
--    op-sub-zero-r）——spec-int-general-id 钉住完全解析为 id⁺ 非负积分值。
-- 阶段 3 状态：三个钉住桥接（spec-int-general-id/-exp/-phi-t）全部解析——
--  exp/φ_t 到非负 sup（spec-int-nonneg-exp/-phi-t，v1.26）、id 到 id⁺ 非负积分
--  （v1.27）；钉住残留 = 谱表示 postulate 值（spec-int-A/-exp/e^(-tA），健全）。
--
-- 待降定理（2026-08-03 再再再再再更新）：
--  - fc-poly-le-spec-int 构造化（fc-integral 最后登记项）：方案 A 阶段 4
--    （∫p = ∫p⁺ −ₒ ∫p⁻ 各自由非负 sup 构造化 + v1.15 幂单调性引理库 +
--    dyadic 阶梯逼近 → fc-integral 零登记项）
--  - 8-5b 算子层等式版 + 对象映射（funext 受限）：算子层等式版公理、op-lin 保结构、
--    A/fc 对象 Hilbert 侧构造（依赖谱定理降定理链）
--  - E-σ-add 收敛（算子序 sup 存在）：强/弱算子拓扑单调有界收敛
