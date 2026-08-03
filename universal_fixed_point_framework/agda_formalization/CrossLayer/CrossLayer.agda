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
open import DHStructural.DHStructuralAnalysis using (ℝ; zeroℝ; oneℝ)

-- Op 层（P1Spectral：抽象算子代数公理，跨层验证的源；SpectralTheory 复用同一 Op）
open import P1Spectral.P1Spectral
  using (Op; _+ₒ_; _*ₒ_; _·ₒ_; 𝟘ₒ; 𝟙ₒ)

-- LinOp 层（HilbertSpace：具体线性算子，跨层验证的目标；§16 点态律全齐）
open import HilbertSpace.HilbertSpace
  using (V; LinOp; zero-op; op-add; op-comp; id-op; _·ₗ_;
         +ₗ-assoc-pt; +ₗ-comm-pt; +ₗ-ident-pt;
         op-comp-assoc-pt; op-comp-id-pt; op-comp-id-r-pt;
         *ₗ-zero-r-pt; *ₗ-zero-l-pt; distribₗ-pt; distribₗ-l-pt;
         ·ₗ-comp-pt; ·ₗ-comm-l-pt; ·ₗ-zero-l-pt)

-- 打开 LinOp 记录模块：投影 f（与 lin-add/lin-scalar）进入作用域
--（Agda 的 using 子句不支持 `LinOp.f` 限定投影名解析，用 open 记录方式引入）
open LinOp

-- 点态算子代数见证（跨层模型证书）：LinOp 层逐点满足 Op 层全部算子代数公理
--（+ₒ-assoc / +ₒ-comm / +ₒ-ident / *ₒ-assoc / *ₒ-ident / *ₒ-ident-l /
--  *ₒ-zero-r / *ₒ-zero-l / distribₒ / distribₒ-l / ·ₒ-comm / ·ₒ-comm-l / ·ₒ-zero-l——
--  13 组公理，逐点形式 = ∀v. LinOp.f 值相等）
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
  }
