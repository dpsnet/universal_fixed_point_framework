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

module P1Spectral.P1Spectral where

-- P1: 谱匹配双射的有限维特例（2026-08-01）
-- ========================================
-- 对应笔记: notes/00_foundations/spectral_R11_morphism_layer.md §4（定理 3）
-- 对应 Lean: （P1 目标，定理 3 有限维退化版）
--
-- 目标：在 Agda 中形式化定理 3 的有限维退化——
--   M_Sp = M_σ = M_Rec（线性语义下谱匹配双射 = 恒等）。
--
-- 设定：有限维、自伴、有限点谱（谱定理有限维版）。
--   - 算子代数 Op（抽象载体，域律公理）
--   - 谱分解 A = Σᵢ evᵢ·Eᵢ（Eᵢ 谱投影，有限点谱）
--   - e^(-A) = Σᵢ e^(-evᵢ)·Eᵢ（Borel 函数演算）
--   - 三条件：交织 M_Sp / 谱匹配 M_σ / exp 交换 M_Rec
--
-- 公理纪律：
--   - 算子代数律、谱分解、exp 谱展开：定义性公理（标准谱论内容）
--   - 谱定理方向（与 A 交换 ⟹ 与谱投影交换；与 e^(-A) 交换 ⟹ 与谱投影交换）：
--     登记为定义性公理（有限维谱定理/Fuglede 内容，T3 谱定理待自建）
--   - **代数方向完全可证**：谱匹配 ⟹ 交织、谱匹配 ⟹ exp 交换
--     （proj-comm-scalar-sum：与谱投影交换 ⟹ 与任意特征值加权谱和交换，
--       零新增公理）
--
-- 注：谱投影的正交幂等性（EᵢEⱼ=δᵢⱼEᵢ、ΣEᵢ=𝟙）为本设定前提，当前证明不
-- 直接依赖，故不声明（最小公理纪律）；M_σ 以谱投影交换定义（有限维谱测度
-- 由谱投影族生成）。

open import Agda.Builtin.Equality using (_≡_; refl)
open import Sp.SpCategory using (ℕ; zero; suc; Fin; _×_; _,_; sym; trans; cong; cong₂)

-- ℝ 层（DHStructural 公理类型：ℝ、+、*、负、exp、自然数嵌入）
open import DHStructural.DHStructuralAnalysis
  using (ℝ; _+ℝ_; _*ℝ_; zeroℝ; oneℝ; negℝ; exp; natℝ; subst)

-- ==================================================================
-- §1 有限维算子代数（定义性公理）
-- ==================================================================

postulate
  Op : Set                    -- 有界线性算子空间
  _+ₒ_ : Op → Op → Op
  _*ₒ_ : Op → Op → Op
  _·ₒ_ : ℝ → Op → Op          -- 标量乘
  𝟘ₒ 𝟙ₒ : Op                  -- 零算子、恒等算子
  -- 加法：结合/交换/单位
  +ₒ-assoc : (x y z : Op) → (x +ₒ y) +ₒ z ≡ x +ₒ (y +ₒ z)
  +ₒ-comm : (x y z : Op) → x +ₒ y ≡ y +ₒ x
  +ₒ-ident : (x : Op) → x +ₒ 𝟘ₒ ≡ x
  -- 乘法：结合/单位/零吸收
  *ₒ-assoc : (x y z : Op) → (x *ₒ y) *ₒ z ≡ x *ₒ (y *ₒ z)
  *ₒ-ident : (x : Op) → x *ₒ 𝟙ₒ ≡ x
  *ₒ-ident-l : (x : Op) → 𝟙ₒ *ₒ x ≡ x
  *ₒ-zero-r : (x : Op) → x *ₒ 𝟘ₒ ≡ 𝟘ₒ
  *ₒ-zero-l : (x : Op) → 𝟘ₒ *ₒ x ≡ 𝟘ₒ
  -- 分配律
  distribₒ : (x y z : Op) → x *ₒ (y +ₒ z) ≡ (x *ₒ y) +ₒ (x *ₒ z)
  distribₒ-l : (x y z : Op) → (x +ₒ y) *ₒ z ≡ (x *ₒ z) +ₒ (y *ₒ z)
  -- 标量乘与乘法的交换（标量视为"中心"元）
  ·ₒ-comm : (a : ℝ) (x y : Op) → (a ·ₒ x) *ₒ y ≡ a ·ₒ (x *ₒ y)
  ·ₒ-comm-l : (a : ℝ) (x y : Op) → x *ₒ (a ·ₒ y) ≡ a ·ₒ (x *ₒ y)
  -- 标量零吸收：0·X = 0（标量零律，与 *ₒ-zero-l 平行；模型必然性 = Op 是 ℝ-向量空间）
  ·ₒ-zero-l : (X : Op) → zeroℝ ·ₒ X ≡ 𝟘ₒ
  -- 标量乘零算子：a·0 = 0（标量零律右版，2026-08-03；模型必然性 = Op 是 ℝ-向量空间，
  -- 标量乘零向量 = 零向量；用途 = 方案 A 的 op-sub-zero-r（X−ₒ0 = X）与一致性）
  ·ₒ-zero-r : (a : ℝ) → a ·ₒ 𝟘ₒ ≡ 𝟘ₒ

-- ==================================================================
-- §2 求和（Fin 索引，可证明）
-- ==================================================================

sumOp : {m : ℕ} → (Fin m → Op) → Op
sumOp {zero} f = 𝟘ₒ
sumOp {suc m} f = f zero +ₒ sumOp {m} (λ i → f (suc i))

sumOp-cong : {m : ℕ} {f g : Fin m → Op} → (∀ i → f i ≡ g i) → sumOp {m} f ≡ sumOp {m} g
sumOp-cong {zero} h = refl
sumOp-cong {suc m} {f} {g} h =
  cong₂ _+ₒ_ (h zero) (sumOp-cong {m} {λ i → f (suc i)} {λ i → g (suc i)} (λ i → h (suc i)))

-- 谱匹配 ⟹ 与任意"特征值加权谱和"交换（定理 3 的代数核心，可证明）
proj-comm-scalar-sum : {m : ℕ} (X : Op) (c : Fin m → ℝ) (P : Fin m → Op)
  → (∀ i → X *ₒ P i ≡ P i *ₒ X)
  → X *ₒ sumOp {m} (λ i → c i ·ₒ P i) ≡ sumOp {m} (λ i → c i ·ₒ P i) *ₒ X
proj-comm-scalar-sum {zero} X c P h =
  trans (*ₒ-zero-r X) (sym (*ₒ-zero-l X))
proj-comm-scalar-sum {suc m} X c P h =
  trans (distribₒ X (c zero ·ₒ P zero) rest)
        (trans (cong₂ _+ₒ_ head tail-comm)
               (sym (distribₒ-l (c zero ·ₒ P zero) rest X)))
  where
  rest : Op
  rest = sumOp {m} (λ i → c (suc i) ·ₒ P (suc i))
  -- X·(c0·P0) = (c0·P0)·X（标量中心 + h zero）
  head : X *ₒ (c zero ·ₒ P zero) ≡ (c zero ·ₒ P zero) *ₒ X
  head = trans (·ₒ-comm-l (c zero) X (P zero))
               (trans (cong (λ y → c zero ·ₒ y) (h zero))
                      (sym (·ₒ-comm (c zero) (P zero) X)))
  -- 归纳：X·rest = rest·X
  tail-comm : X *ₒ rest ≡ rest *ₒ X
  tail-comm = proj-comm-scalar-sum {m} X (λ i → c (suc i)) (λ i → P (suc i)) (λ i → h (suc i))

-- ==================================================================
-- §3 有限谱表示（定义性公理：谱定理有限维版）
-- ==================================================================

-- 谱点数（有限维特例：固定但未指定）
postulate
  n : ℕ

-- 谱设定：A 自伴（谱分解 A = Σ evᵢ·Eᵢ），E 为谱投影族，exp-A = e^(-A)
postulate
  A : Op
  ev : Fin n → ℝ               -- 特征值（互异，简单谱或重数合并）
  E : Fin n → Op               -- 谱投影
  exp-A : Op                   -- e^(-A)（Borel 函数演算）
  -- 谱分解与 exp 谱展开
  spectral-decomp : A ≡ sumOp {n} (λ i → ev i ·ₒ E i)
  exp-spectral : exp-A ≡ sumOp {n} (λ i → exp (negℝ (ev i)) ·ₒ E i)
  -- 谱定理有限维版（⟹ 方向，Fuglede/谱测度输送内容）：
  -- 与 A 交换 ⟹ 与每个谱投影交换
  intertwine-imp-proj : (X : Op) → X *ₒ A ≡ A *ₒ X → (i : Fin n) → X *ₒ E i ≡ E i *ₒ X
  -- 与 e^(-A) 交换 ⟹ 与每个谱投影交换（exp 单射 + 谱定理）
  intertwine-exp-imp-proj : (X : Op) → X *ₒ exp-A ≡ exp-A *ₒ X → (i : Fin n) → X *ₒ E i ≡ E i *ₒ X

-- ==================================================================
-- §4 三条件谓词（对应 P1 笔记 §2 的 M_Sp / M_σ / M_Rec）
-- ==================================================================

M-Sp : Op → Set
M-Sp X = X *ₒ A ≡ A *ₒ X

M-σ : Op → Set
M-σ X = (i : Fin n) → X *ₒ E i ≡ E i *ₒ X

M-Rec : Op → Set
M-Rec X = X *ₒ exp-A ≡ exp-A *ₒ X

-- ==================================================================
-- §5 定理 3（线性语义下 M_Sp = M_σ = M_Rec）
-- ==================================================================

-- 谱匹配 ⟹ 交织（可证：谱分解 + proj-comm-scalar-sum）
σ→Sp : {X : Op} → M-σ X → M-Sp X
σ→Sp {X} h =
  subst (λ Y → X *ₒ Y ≡ Y *ₒ X) (sym spectral-decomp)
        (proj-comm-scalar-sum {n} X ev E h)

-- 谱匹配 ⟹ exp 交换（可证：exp 谱展开 + proj-comm-scalar-sum）
σ→Rec : {X : Op} → M-σ X → M-Rec X
σ→Rec {X} h =
  subst (λ Y → X *ₒ Y ≡ Y *ₒ X) (sym exp-spectral)
        (proj-comm-scalar-sum {n} X (λ i → exp (negℝ (ev i))) E h)

-- 交织 ⟹ 谱匹配（定义性公理：谱定理有限维版）
Sp→σ : {X : Op} → M-Sp X → M-σ X
Sp→σ {X} h i = intertwine-imp-proj X h i

-- exp 交换 ⟹ 谱匹配（定义性公理：exp 单射 + 谱定理）
Rec→σ : {X : Op} → M-Rec X → M-σ X
Rec→σ {X} h i = intertwine-exp-imp-proj X h i

-- 定理 3（有限维版）：三条件两两逻辑等价（解空间一致）
theorem3-Sp-σ : {X : Op} → (M-Sp X → M-σ X) × (M-σ X → M-Sp X)
theorem3-Sp-σ = (λ h → Sp→σ h) , (λ h → σ→Sp h)

theorem3-Rec-σ : {X : Op} → (M-Rec X → M-σ X) × (M-σ X → M-Rec X)
theorem3-Rec-σ = (λ h → Rec→σ h) , (λ h → σ→Rec h)

theorem3 : {X : Op} → (M-Sp X → M-σ X) × (M-σ X → M-Sp X)
               × (M-Rec X → M-σ X) × (M-σ X → M-Rec X)
theorem3 = (λ h → Sp→σ h) , (λ h → σ→Sp h) , (λ h → Rec→σ h) , (λ h → σ→Rec h)

-- ==================================================================
-- §7 推论 4：恒等双射（Hom_Sp ≅ Hom_σ ≅ Hom_Rec，P1 笔记 §4 推论 4）
-- ==================================================================

-- 互逆往返一致性（定义性公理：谱分解（spectral-decomp）与谱定理方向
-- （intertwine-imp-proj / intertwine-exp-imp-proj）之间的往返一致性；
-- 有限维由"Eᵢ 是 A 的插值多项式"可证，谱定理层完整实现时降为定理）
postulate
  σ→Sp∘Sp→σ : {X : Op} (h : M-Sp X) → σ→Sp (Sp→σ h) ≡ h
  Sp→σ∘σ→Sp : {X : Op} (h : M-σ X) → Sp→σ (σ→Sp h) ≡ h
  σ→Rec∘Rec→σ : {X : Op} (h : M-Rec X) → σ→Rec (Rec→σ h) ≡ h
  Rec→σ∘σ→Rec : {X : Op} (h : M-σ X) → Rec→σ (σ→Rec h) ≡ h

-- Hom 集合（有限维：谱态射 / 谱匹配态射 / 递归态射）
record Hom-Sp : Set where
  field
    op : Op
    prop : M-Sp op

record Hom-σ : Set where
  field
    op : Op
    prop : M-σ op

record Hom-Rec : Set where
  field
    op : Op
    prop : M-Rec op

-- 双射（恒等映射：两边都是 M_σ 上的同构，对应 P1 笔记推论 4）
record _≅_ (A B : Set) : Set where
  field
    to : A → B
    from : B → A
    to∘from : (b : B) → to (from b) ≡ b
    from∘to : (a : A) → from (to a) ≡ a

Sp≅σ : Hom-Sp ≅ Hom-σ
Sp≅σ = record
  { to = λ h → record { op = Hom-Sp.op h ; prop = Sp→σ (Hom-Sp.prop h) }
  ; from = λ h → record { op = Hom-σ.op h ; prop = σ→Sp (Hom-σ.prop h) }
  ; to∘from = λ b → cong (λ w → record { op = Hom-σ.op b ; prop = w }) (Sp→σ∘σ→Sp (Hom-σ.prop b))
  ; from∘to = λ a → cong (λ w → record { op = Hom-Sp.op a ; prop = w }) (σ→Sp∘Sp→σ (Hom-Sp.prop a))
  }

Rec≅σ : Hom-Rec ≅ Hom-σ
Rec≅σ = record
  { to = λ h → record { op = Hom-Rec.op h ; prop = Rec→σ (Hom-Rec.prop h) }
  ; from = λ h → record { op = Hom-σ.op h ; prop = σ→Rec (Hom-σ.prop h) }
  ; to∘from = λ b → cong (λ w → record { op = Hom-σ.op b ; prop = w }) (Rec→σ∘σ→Rec (Hom-σ.prop b))
  ; from∘to = λ a → cong (λ w → record { op = Hom-Rec.op a ; prop = w }) (σ→Rec∘Rec→σ (Hom-Rec.prop a))
  }

-- 推论 4（有限维版）：Hom_Sp 与 Hom_Rec 都 ≅ Hom_σ（同一集合 M_σ，恒等双射）
corollary4 : (Hom-Sp ≅ Hom-σ) × (Hom-Rec ≅ Hom-σ)
corollary4 = Sp≅σ , Rec≅σ

-- ==================================================================
-- §8 与有限维具体模型的关系（注释）
-- ==================================================================
{-
  本节公理在具体有限维模型中成立（结构对应）：
  - Op = n×n 复矩阵；_+ₒ_/_*ₒ_ = 矩阵加/乘；_·ₒ_ = 标量乘；𝟘ₒ/𝟙ₒ = 零/单位矩阵
  - A = 自伴矩阵（谱分解 A = U·diag(ev)·U*，有限维谱定理）
  - E i = 第 i 个特征值的谱投影（U·diag(δᵢⱼ)·U*）
  - exp-A = e^(-A) = U·diag(e^(-evᵢ))·U*（矩阵指数）
  - intertwine-imp-proj / intertwine-exp-imp-proj：
    有限维 Fuglede（X 与 A 交换 ⟹ X 与 A 的每个谱投影交换；
    X 与 e^(-A) 交换 ⟹ X 与每个 e^(-evᵢ) 块交换，e^(-x) 单射 + 互异特征值）

  定理 3 的"双射 = 恒等"表述（P1 笔记推论 4）：
  Hom_Sp(E, D(S)) 与 Hom_Rec_D(R(E), S) 在 §2 嵌入下都是 M_σ（本定理），
  自然同构为恒等映射——M-Sp/M-σ/M-Rec 三条件谓词逐点等价即"解空间一致"。
  注：恒等双射的互逆往返一致性（σ→Sp ∘ Sp→σ = id）依赖谱分解
  （spectral-decomp）与谱定理方向（intertwine-imp-proj）之间的一致性公理
  ——有限维由"Eᵢ 是 A 的插值多项式"可证，当前公理集未声明，留待谱定理层
  完整实现时登记。
-}
