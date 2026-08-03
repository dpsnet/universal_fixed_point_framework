module CrossLayer.CrossLayer where

{-
  8-5b 余项：跨层模型 Op → LinOp（SpectralTheory 算子代数公理的 LinOp 层点态验证，
  2026-08-03）
  =====================================================================
  对应笔记: notes/00_foundations/spectral_T3_analysis_foundation.md §5.16.4/§5.16.5
  对应路线图: roadmap/phase60_category_verification.md v1.13+（8-5b 余项）

  目标：把 SpectralTheory/P1Spectral 的抽象算子代数（Op 层，P1Spectral §2 公理）
  用 HilbertSpace 的具体线性算子（LinOp 层，§5/§16）实例化——验证 LinOp 层
  **逐点**满足 Op 层全部算子代数公理（跨层模型的第一步：对象映射 + 基本性质验证）。

  跨层对应表（抽象 Op 层 ↦ 具体 LinOp 层）：
    Op        ↦ LinOp
    _+ₒ_      ↦ op-add
    _*ₒ_      ↦ op-comp
    _·ₒ_      ↦ _·ₗ_
    𝟘ₒ        ↦ zero-op
    𝟙ₒ        ↦ id-op
    +ₒ-assoc  ↦ +ₗ-assoc-pt     （LinOp.f 值级，**可证**，+ᵥ-assoc）
    +ₒ-comm   ↦ +ₗ-comm-pt      （**可证**，+ᵥ-comm）
    +ₒ-ident  ↦ +ₗ-ident-pt     （**可证**，+ᵥ-ident）
    *ₒ-assoc  ↦ op-comp-assoc-pt（**可证**，定义性）
    *ₒ-ident  ↦ op-comp-id-r-pt （**可证**，定义性）
    *ₒ-ident-l ↦ op-comp-id-pt  （**可证**，定义性）
    *ₒ-zero-r ↦ *ₗ-zero-r-pt    （**可证**，lin-zero：T0=0）
    *ₒ-zero-l ↦ *ₗ-zero-l-pt    （**可证**，定义性）
    distribₒ  ↦ distribₗ-pt     （**可证**，线性性 lin-add）
    distribₒ-l ↦ distribₗ-l-pt  （**可证**，定义性）
    ·ₒ-comm   ↦ ·ₗ-comp-pt      （**可证**，定义性）
    ·ₒ-comm-l ↦ ·ₗ-comm-l-pt    （**可证**，线性性 lin-scalar）
    ·ₒ-zero-l ↦ ·ₗ-zero-l-pt    （**可证**，scalar-zero-any）
    ·ₒ-zero-r ↦ ·ₗ-zero-r-pt    （**可证**，scalar-zero；v1.24 补充公理对应）

  funext 限制：LinOp 是 record（f/lin-add/lin-scalar 三字段），算子层等式
  （op-add (op-add X Y) Z ≡ op-add X (op-add Y Z) 等）需 f 字段函数相等
  （funext）+ 证明字段相等（命题外延），超出库公理范围（P4 先例）——
  故跨层模型交付"逐点对应"（∀v. LinOp.f 值相等），全部可证（零新增公理）。

  开放项（funext 受限，不登记 postulate）：
    - 算子层等式版公理（+ₒ-assoc 等 15 条在 LinOp 层的算子级版本）；
    - 对象映射 op-lin : Op → LinOp 及其保结构（op-lin (X +ₒ Y) ≡ op-add
      (op-lin X) (op-lin Y) 等）——降定理路径 = 完整 Hilbert 层实现
      （Op := LinOp 时 op-lin = id，保结构恒真）；
    - 谱对象映射（A ↦ 自伴算子、E P ↦ E-hilb P、fc f ↦ Borel 函数演算、
      exp-tA t ↦ exp-hilb-tA t）——随各降定理链闭合。
-}

open import Agda.Builtin.Equality using (_≡_; refl)
open import Sp.SpCategory using (sym)

-- ℝ 层
open import DHStructural.DHStructuralAnalysis using (ℝ; zeroℝ; oneℝ; _+ℝ_; _*ℝ_; _≤ℝ_; _⊎_; ⊥; exp; negℝ)

-- Op 层（P1Spectral：抽象算子代数公理，跨层验证的源；SpectralTheory 复用同一 Op）
open import P1Spectral.P1Spectral
  using (Op; _+ₒ_; _*ₒ_; _·ₒ_; 𝟘ₒ; 𝟙ₒ)

-- LinOp 层（HilbertSpace：具体线性算子，跨层验证的目标；§16 点态律全齐）
open import HilbertSpace.HilbertSpace
  using (V; LinOp; zero-op; op-add; op-comp; id-op; _·ₗ_; _+ᵥ_; _⟨⟩_; op-norm;
         TopP; SelfAdjoint;
         E-hilb; E-hilb-idemp; E-hilb-orth; E-hilb-total;
         E-hilb-self-adjoint; E-hilb-norm-le-one; E-hilb-union;
         exp-hilb-tA; exp-hilb-semigroup; exp-hilb-zero;
         exp-hilb-self-adjoint; exp-hilb-contractive;
         A-hilb; A-hilb-self-adjoint; A-hilb-comm-E;
         fc-hilb; fc-hilb-id; fc-hilb-exponential;
         +ₗ-assoc-pt; +ₗ-comm-pt; +ₗ-ident-pt;
         op-comp-assoc-pt; op-comp-id-pt; op-comp-id-r-pt;
         *ₗ-zero-r-pt; *ₗ-zero-l-pt; distribₗ-pt; distribₗ-l-pt;
         ·ₗ-comp-pt; ·ₗ-comm-l-pt; ·ₗ-zero-l-pt; ·ₗ-zero-r-pt)

-- 打开 LinOp 记录模块：投影 f（与 lin-add/lin-scalar）进入作用域
--（Agda 的 using 子句不支持 `LinOp.f` 限定投影名解析，用 open 记录方式引入）
open LinOp

-- 点态算子代数见证（跨层模型证书）：LinOp 层逐点满足 Op 层全部算子代数公理
--（+ₒ-assoc / +ₒ-comm / +ₒ-ident / *ₒ-assoc / *ₒ-ident / *ₒ-ident-l /
--  *ₒ-zero-r / *ₒ-zero-l / distribₒ / distribₒ-l / ·ₒ-comm / ·ₒ-comm-l /
--  ·ₒ-zero-l / ·ₒ-zero-r——14 组公理，逐点形式 = ∀v. LinOp.f 值相等）
record OpAlgPt : Set where
  field
    -- +ₒ-assoc 点态
    +ₗ-assoc : (X Y Z : LinOp) (v : V)
      → f (op-add (op-add X Y) Z) v ≡ f (op-add X (op-add Y Z)) v
    -- +ₒ-comm 点态
    +ₗ-comm : (X Y : LinOp) (v : V) → f (op-add X Y) v ≡ f (op-add Y X) v
    -- +ₒ-ident 点态
    +ₗ-ident : (X : LinOp) (v : V) → f (op-add X zero-op) v ≡ f X v
    -- *ₒ-assoc 点态
    *ₗ-assoc : (X Y Z : LinOp) (v : V)
      → f (op-comp (op-comp X Y) Z) v ≡ f (op-comp X (op-comp Y Z)) v
    -- *ₒ-ident 点态
    *ₗ-ident : (X : LinOp) (v : V) → f (op-comp X id-op) v ≡ f X v
    -- *ₒ-ident-l 点态
    *ₗ-ident-l : (X : LinOp) (v : V) → f (op-comp id-op X) v ≡ f X v
    -- *ₒ-zero-r 点态
    *ₗ-zero-r : (X : LinOp) (v : V) → f (op-comp X zero-op) v ≡ f zero-op v
    -- *ₒ-zero-l 点态
    *ₗ-zero-l : (X : LinOp) (v : V) → f (op-comp zero-op X) v ≡ f zero-op v
    -- distribₒ 点态
    distribₗ : (X Y Z : LinOp) (v : V)
      → f (op-comp X (op-add Y Z)) v ≡ f (op-add (op-comp X Y) (op-comp X Z)) v
    -- distribₒ-l 点态
    distribₗ-l : (X Y Z : LinOp) (v : V)
      → f (op-comp (op-add X Y) Z) v ≡ f (op-add (op-comp X Z) (op-comp Y Z)) v
    -- ·ₒ-comm 点态（((a·ₗX)∘Y)v = (a·ₗ(X∘Y))v）
    ·ₗ-comm : (c : ℝ) (X Y : LinOp) (v : V)
      → f (op-comp (c ·ₗ X) Y) v ≡ f (c ·ₗ (op-comp X Y)) v
    -- ·ₒ-comm-l 点态
    ·ₗ-comm-l : (c : ℝ) (X Y : LinOp) (v : V)
      → f (op-comp X (c ·ₗ Y)) v ≡ f (c ·ₗ (op-comp X Y)) v
    -- ·ₒ-zero-l 点态
    ·ₗ-zero-l : (X : LinOp) (v : V) → f (zeroℝ ·ₗ X) v ≡ f zero-op v
    -- ·ₒ-zero-r 点态（标量乘零算子：(c·ₗ𝟘ₗ)v = 𝟘ₗ v，v1.24 补充）
    ·ₗ-zero-r : (c : ℝ) (v : V) → f (c ·ₗ zero-op) v ≡ f zero-op v

-- **可证（零新增公理）**：LinOp 层逐点满足 Op 层算子代数公理——
-- 跨层模型验证证书实例化（字段全部来自 HilbertSpace §16 点态律）
op-alg-pt : OpAlgPt
op-alg-pt = record
  { +ₗ-assoc = +ₗ-assoc-pt
  ; +ₗ-comm = +ₗ-comm-pt
  ; +ₗ-ident = +ₗ-ident-pt
  ; *ₗ-assoc = op-comp-assoc-pt
  ; *ₗ-ident = op-comp-id-r-pt
  ; *ₗ-ident-l = op-comp-id-pt
  ; *ₗ-zero-r = *ₗ-zero-r-pt
  ; *ₗ-zero-l = *ₗ-zero-l-pt
  ; distribₗ = distribₗ-pt
  ; distribₗ-l = distribₗ-l-pt
  ; ·ₗ-comm = λ c X Y v → sym (·ₗ-comp-pt c X Y v)
  ; ·ₗ-comm-l = ·ₗ-comm-l-pt
  ; ·ₗ-zero-l = ·ₗ-zero-l-pt
  ; ·ₗ-zero-r = ·ₗ-zero-r-pt
  }

-- ==================================================================
-- §2 谱对象映射证书（跨层模型第二步：谱论公理 → Hilbert 构造，2026-08-03）
-- ==================================================================
-- 目标：把 SpectralTheory 谱论公理族（§1 E / exp-tA）在 Hilbert 层的构造对应
-- （E P ↦ E-hilb P、exp-tA t ↦ exp-hilb-tA t）组织为可证证书——§15 审计
-- 跨层降定理映射（E-total/E-union/E-σ-add ↔ HilbertSpace §10c-e/§14、
-- 半群 ↔ §12）的形式化版本（A4 跨层完整实例化的谱对象映射部分）。
-- 形式：点态/性质断言（∀v. 值级等式 / 内积正交 / 范数 ≤ 1 / 自伴谓词），
-- 避开 funext（算子级等式（如 E-idempotent 的 E P *ₒ E P ≡ E P）在 LinOp 层
-- 需函数外延性提升，P4 先例；对象映射 op-lin 的等式保结构同理，留降定理链）。
-- 字段类型即 SpectralTheory 公理模式（E-idempotent/E-orthogonal/E-total/
-- E-union/semigroup/exp-tA-zero）在 LinOp 层的对应签名。

record SpectralObjPt : Set₁ where
  field
    -- E-idempotent（E P *ₒ E P ≡ E P）点态对应：E(P)(E(P)x) = E(P)x
    E-idem-pt : (P : ℝ → Set) (x : V)
      → LinOp.f (op-comp (E-hilb P) (E-hilb P)) x ≡ LinOp.f (E-hilb P) x
    -- E-orthogonal（P∩Q=∅ ⟹ E P *ₒ E Q ≡ 𝟘ₒ）对应（内积正交版）：
    -- P∩Q=∅ ⟹ ⟨E(P)u, E(Q)v⟩ = 0（E(P)u ⊥ E(Q)v）
    E-orth-ip : (P Q : ℝ → Set) → ((x : ℝ) → P x → Q x → ⊥) → (u v : V)
      → LinOp.f (E-hilb P) u ⟨⟩ LinOp.f (E-hilb Q) v ≡ zeroℝ
    -- E-total（E(ℝ) = 𝟙ₒ）点态对应：E(ℝ)x = x
    E-total-pt : (x : V) → LinOp.f (E-hilb TopP) x ≡ x
    -- 谱投影自伴（⟨E(P)x, y⟩ = ⟨x, E(P)y⟩）
    E-self-adjoint : (P : ℝ → Set) → SelfAdjoint (E-hilb P)
    -- 谱投影范数 ≤ 1（proj-norm-le-one 的谱投影实例）
    E-norm-le-one : (P : ℝ → Set) → op-norm (E-hilb P) ≤ℝ oneℝ
    -- E-union（P∩Q=∅ ⟹ E(P∪Q) ≡ E(P) + E(Q)）点态对应：E(P∪Q)x = E(P)x + E(Q)x
    E-union-pt : (P Q : ℝ → Set) → ((x : ℝ) → P x → Q x → ⊥) → (x : V)
      → LinOp.f (E-hilb (λ z → P z ⊎ Q z)) x ≡ LinOp.f (E-hilb P) x +ᵥ LinOp.f (E-hilb Q) x
    -- semigroup（exp-tA(s+t) ≡ exp-tA s *ₒ exp-tA t）点态对应
    exp-tA-semigroup-pt : (s t : ℝ) (x : V)
      → LinOp.f (exp-hilb-tA (s +ℝ t)) x
        ≡ LinOp.f (op-comp (exp-hilb-tA s) (exp-hilb-tA t)) x
    -- exp-tA-zero（exp-tA 0 ≡ 𝟙ₒ）点态对应：e^(0A)x = x
    exp-tA-zero-pt : (x : V) → LinOp.f (exp-hilb-tA zeroℝ) x ≡ x
    -- exp-tA-self-adjoint（e^(-tA) 自伴）
    exp-tA-self-adjoint : (t : ℝ) → SelfAdjoint (exp-hilb-tA t)
    -- 压缩（‖e^(-tA)‖ ≤ 1）
    exp-tA-contractive : (t : ℝ) → op-norm (exp-hilb-tA t) ≤ℝ oneℝ
    -- §12' A/fc 对象映射（2026-08-03，方案②）：谱定理降定理链端点桥接——
    -- A ↦ A-hilb（自伴算子）、fc f ↦ fc-hilb f（Borel 函数演算）；链体（谱定理
    -- 证明）为降定理路径，与 spectral-subspace/exp-hilb-tA 同层桥接
    -- A 自伴（SpectralTheory A 自伴正定的 Hilbert 侧）
    A-self-adjoint-hilb : SelfAdjoint A-hilb
    -- A 与谱投影交换（A E(P) = E(P) A，M-Sp/M-σ 的 Hilbert 侧）
    A-comm-E-hilb-pt : (P : ℝ → Set) (x : V)
      → LinOp.f (op-comp A-hilb (E-hilb P)) x ≡ LinOp.f (op-comp (E-hilb P) A-hilb) x
    -- 恒等函数演算 = A（fc-hilb(id) = A-hilb，∫id dE = A 的 Hilbert 侧）
    fc-hilb-id-A-pt : (x : V) → LinOp.f (fc-hilb (λ y → y)) x ≡ LinOp.f A-hilb x
    -- 指数函数演算 = 半群（fc-hilb(e^(-t·)) = exp-hilb-tA t，§8c exp-tA = fc(φ_t)）
    fc-hilb-exp-tA-pt : (t : ℝ) (x : V)
      → LinOp.f (fc-hilb (λ y → exp (negℝ (t *ℝ y)))) x ≡ LinOp.f (exp-hilb-tA t) x

-- **可证（E 族零新增公理；exp-tA 族字段为 §12 桥接）**：谱对象映射证书实例化——
-- E 族字段全部来自 HilbertSpace §10c-§10e 可证定理（E-hilb-idemp/orth/total/
-- self-adjoint/norm-le-one/union），exp-tA 族字段来自 §12 半群桥接
-- （exp-hilb-semigroup/zero/self-adjoint/contractive）
spectral-obj-pt : SpectralObjPt
spectral-obj-pt = record
  { E-idem-pt = E-hilb-idemp
  ; E-orth-ip = E-hilb-orth
  ; E-total-pt = E-hilb-total
  ; E-self-adjoint = E-hilb-self-adjoint
  ; E-norm-le-one = E-hilb-norm-le-one
  ; E-union-pt = E-hilb-union
  ; exp-tA-semigroup-pt = exp-hilb-semigroup
  ; exp-tA-zero-pt = exp-hilb-zero
  ; exp-tA-self-adjoint = exp-hilb-self-adjoint
  ; exp-tA-contractive = exp-hilb-contractive
  ; A-self-adjoint-hilb = A-hilb-self-adjoint
  ; A-comm-E-hilb-pt = A-hilb-comm-E
  ; fc-hilb-id-A-pt = fc-hilb-id
  ; fc-hilb-exp-tA-pt = fc-hilb-exponential
  }
