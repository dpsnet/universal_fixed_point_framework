module HilbertSpace.HilbertSpace where

{-
  Hilbert 空间层（阶段 8，2026-08-01 立项启动）
  =============================================
  对应蓝图: notes/00_foundations/spectral_T3_analysis_foundation.md §5.15（阶段 8 立项）
  目标：从 Hilbert 空间结构（内积）建立范数与有界算子理论——
    使 SpectralTheory §12 的 C*-范数公理（‖_‖/norm-pos/norm-submul/norm-power/
    norm-zero/norm-ident/norm-tri）与 norm-contraction（谱半径 = 范数）降为
    可证明定理（降定理路径的实质起点，对应 §15 审计 H 类）。
  本层第一阶段（2026-08-01）：向量空间 + 内积基础。
    - V（载体）+ 实向量空间公理 + 实内积公理 = **基础假设**
      （Hilbert 空间公理是标准分析结构，对齐"ℝ 公理是基础假设"立场；
      模型必然性 = 希尔伯特空间理论）
    - 范数以**范数平方** ‖v‖² := ⟨v,v⟩ 处理（√ 待分析层扩展；
      平方形式已足够支撑正定性/标量/加性类性质）。
    - 首批可证引理：右加性/右标量（内积对称性 + 左线性的对偶）、
      ‖a·v‖² = a²·‖v‖²（标量齐次）、‖0‖² = 0（零元）、‖v‖² ≥ 0（正性）。
  本层第二阶段（2026-08-02）：Cauchy-Schwarz 不等式。
    - ⟨x,y⟩² ≤ ‖x‖²·‖y‖²（范数公理依赖的核心不等式）**可证**：
      三分律分 ‖y‖² = 0 / > 0 / < 0（后两者经正定性/正性排除）；
      ‖y‖² > 0 时取 t = -⟨x,y⟩/‖y‖²，⟨x+ty, x+ty⟩ ≥ 0 展开为
      ‖x‖² - ⟨x,y⟩²/‖y‖² ≥ 0，乘正 ‖y‖² 得 ⟨x,y⟩² ≤ ‖x‖²·‖y‖²。
    - 前置：DHStructural 新增可证 ℝ 引理（取负×乘/乘除结合/分数乘除消去/
      ≤ 移项/非负侧乘保序——零新增公理）。
  本层第二阶段 b（2026-08-02）：范数公理落地（√ 分析层扩展 + 三角不等式）。
    - DHStructural 分析层扩展：sqrt（基础假设，与 exp/log 同层）+ 可证
      sq-nonneg-ℝ（a²≥0）/le-sqrt-sq（a≤√(a²)）/abs（|a|:=√(a²)）/sum-sq-ℝ
      （(a+b)²=a²+2ab+b²）/two-add-eq/sum-add-≤（三角不等式重排）。
    - **可证**：norm := √(‖·‖²)——norm-nonneg（正性）、cs-norm（⟨x,y⟩≤‖x‖‖y‖）、
      norm-sq-add（‖x+y‖² 展开）、norm-sq-tri（‖x+y‖²≤(‖x‖+‖y‖)²）、
      norm-tri（三角不等式）、norm-zero/norm-def（正定性）、
      norm-scalar（齐次 ‖a·v‖=|a|‖v‖）——范数公理（正性/齐次/三角/正定性）落地。
  阶段 3（2026-08-02）：有界线性算子 + 算子范数（sup + √）。
    - LinOp（线性算子 record）+ 算子代数（zero/add/comp）+ 线性 ⟹ T0=0；
    - 算子范数 ‖T‖ := sup_{‖v‖≤1} ‖Tv‖（sup-ℝ 完备性假设）；
    - **可证**：op-norm-nonneg（‖T‖ ≥ 0，T0=0 是单位球成员）、op-norm-upper
      （‖v‖≤1 ⟹ ‖Tv‖≤‖T‖）、op-norm-tri（‖S+T‖ ≤ ‖S‖+‖T‖，norm-tri + sup-least）。
    - 待（8-3b）：缩放引理 ⟹ op-norm-submul（‖ST‖ ≤ ‖S‖‖T‖）。
  阶段 4+（待）：自伴 C* 恒等（norm-power）、算子拓扑（strong-continuity）、
    谱半径公式（norm-contraction）。
-}

open import Agda.Builtin.Equality using (_≡_; refl)
open import Sp.SpCategory using (sym; trans; cong; cong₂; _×_; _,_)

-- ℝ 层（复用 DHStructural：T3 已建的有序域 + 完备性机制）
open import DHStructural.DHStructuralAnalysis
  using (ℝ; zeroℝ; oneℝ; _+ℝ_; _*ℝ_; _≤ℝ_; _<ℝ_; _/ℝ_; negℝ; subst;
         +-assoc-ℝ; +-comm-ℝ; +-ident-ℝ; +-inv-ℝ; *-assoc-ℝ; *-zero-ℝ;
         refl-≤ℝ; ≤-trans-ℝ; ≤-+-mono-ℝ; <-≤-ℝ; lt-≤-trans-ℝ; trichotomy-ℝ; irreflexive-ℝ;
         zero-add-ℝ; natℝ; sqrt; sqrt-nonneg; sq-sqrt; sqrt-sq; sqrt-mono; sqrt-zero; sqrt-mul;
         abs; sq-nonneg-ℝ; le-sqrt-sq; sum-sq-ℝ; two-add-eq; sum-add-≤;
         sup-ℝ; sup-upper; sup-least; zero-lt-one-ℝ;
         tp-ident; ttq-ident; ≤-from-nonneg; div-≤-mul;
         ⊥; ⊥-elim; _⊎_; inj₁; inj₂)

-- ==================================================================
-- §1 向量空间与内积（基础假设）
-- ==================================================================

-- 实向量空间 V（基础假设：实向量空间公理，标准线性代数结构）
postulate
  V : Set
  _+ᵥ_ : V → V → V
  _·ᵥ_ : ℝ → V → V
  zeroᵥ : V
  +ᵥ-assoc : (x y z : V) → (x +ᵥ y) +ᵥ z ≡ x +ᵥ (y +ᵥ z)
  +ᵥ-comm : (x y : V) → x +ᵥ y ≡ y +ᵥ x
  +ᵥ-ident : (x : V) → x +ᵥ zeroᵥ ≡ x
  ·ᵥ-assoc : (a b : ℝ) (x : V) → a ·ᵥ (b ·ᵥ x) ≡ (a *ℝ b) ·ᵥ x
  ·ᵥ-ident : (x : V) → oneℝ ·ᵥ x ≡ x
  ·ᵥ-distrib-l : (a : ℝ) (x y : V) → a ·ᵥ (x +ᵥ y) ≡ (a ·ᵥ x) +ᵥ (a ·ᵥ y)
  ·ᵥ-distrib-r : (a b : ℝ) (x : V) → (a +ℝ b) ·ᵥ x ≡ (a ·ᵥ x) +ᵥ (b ·ᵥ x)

-- 实内积（基础假设：实内积公理；正定性给出范数平方的非负性与零性）
postulate
  _⟨⟩_ : V → V → ℝ
  -- 对称性：⟨x,y⟩ = ⟨y,x⟩
  ip-sym : (x y : V) → x ⟨⟩ y ≡ y ⟨⟩ x
  -- 左线性：⟨x+y,z⟩ = ⟨x,z⟩ + ⟨y,z⟩（右线性经对称性可证）
  ip-add-l : (x y z : V) → (x +ᵥ y) ⟨⟩ z ≡ (x ⟨⟩ z) +ℝ (y ⟨⟩ z)
  -- 左标量：⟨a·x,y⟩ = a·⟨x,y⟩（右标量经对称性可证）
  ip-scalar-l : (a : ℝ) (x y : V) → (a ·ᵥ x) ⟨⟩ y ≡ a *ℝ (x ⟨⟩ y)
  -- 正性：⟨x,x⟩ ≥ 0
  ip-pos : (x : V) → zeroℝ ≤ℝ (x ⟨⟩ x)
  -- 正定性：⟨x,x⟩ = 0 ⟹ x = 0
  ip-def : (x : V) → x ⟨⟩ x ≡ zeroℝ → x ≡ zeroᵥ

-- ==================================================================
-- §2 范数平方（‖v‖² := ⟨v,v⟩；√ 待分析层扩展）
-- ==================================================================

-- 范数平方：‖v‖² := ⟨v,v⟩
norm-sq : V → ℝ
norm-sq v = v ⟨⟩ v

-- **可证**：右加性（内积对称性 + 左加性的对偶）
ip-add-r : (x y z : V) → x ⟨⟩ (y +ᵥ z) ≡ (x ⟨⟩ y) +ℝ (x ⟨⟩ z)
ip-add-r x y z =
  trans (ip-sym x (y +ᵥ z))
        (trans (ip-add-l y z x)
               (cong₂ _+ℝ_ (ip-sym y x) (ip-sym z x)))

-- **可证**：右标量（内积对称性 + 左标量的对偶）
ip-scalar-r : (a : ℝ) (x y : V) → x ⟨⟩ (a ·ᵥ y) ≡ a *ℝ (x ⟨⟩ y)
ip-scalar-r a x y =
  trans (ip-sym x (a ·ᵥ y))
        (trans (ip-scalar-l a y x)
               (cong (λ t → a *ℝ t) (ip-sym y x)))

-- **可证**：‖a·v‖² = a²·‖v‖²（标量齐次：左标量 + 右标量 + *-assoc-ℝ）
norm-sq-scalar : (a : ℝ) (v : V) → norm-sq (a ·ᵥ v) ≡ (a *ℝ a) *ℝ norm-sq v
norm-sq-scalar a v =
  trans (ip-scalar-l a v (a ·ᵥ v))
        (trans (cong (λ t → a *ℝ t) (ip-scalar-r a v v))
               (sym (*-assoc-ℝ a a (v ⟨⟩ v))))

-- **可证**：‖v‖² ≥ 0（内积正性）
norm-sq-nonneg : (v : V) → zeroℝ ≤ℝ norm-sq v
norm-sq-nonneg v = ip-pos v

-- **可证**：‖0‖² = 0（零元：⟨0,0⟩ = ⟨0+0,0⟩ = ⟨0,0⟩+⟨0,0⟩ ⟹ ⟨0,0⟩ = 0）
norm-sq-zero : norm-sq zeroᵥ ≡ zeroℝ
norm-sq-zero = double-self-zero t-double
  where
  -- ⟨0,0⟩ = ⟨0+0,0⟩ = ⟨0,0⟩+⟨0,0⟩（+ᵥ-ident + 左加性）
  t-double : zeroᵥ ⟨⟩ zeroᵥ ≡ (zeroᵥ ⟨⟩ zeroᵥ) +ℝ (zeroᵥ ⟨⟩ zeroᵥ)
  t-double =
    trans (cong (λ w → w ⟨⟩ zeroᵥ) (sym (+ᵥ-ident zeroᵥ)))
          (ip-add-l zeroᵥ zeroᵥ zeroᵥ)
  -- ℝ 层：t = t+t ⟹ t = 0（+ᵥ 侧双自零的 ℝ 对应）
  double-self-zero : {t : ℝ} → t ≡ t +ℝ t → t ≡ zeroℝ
  double-self-zero {t} h = trans (sym step1) step2
    where
    -- (t+t)+(-t) = t+0 = t（结合 + 逆 + 单位）
    step1 : (t +ℝ t) +ℝ negℝ t ≡ t
    step1 = trans (+-assoc-ℝ t t (negℝ t))
                  (trans (cong (λ s → t +ℝ s) (+-inv-ℝ t))
                         (+-ident-ℝ t))
    -- (t+t)+(-t) = t+(-t) = 0（h + 逆）
    step2 : (t +ℝ t) +ℝ negℝ t ≡ zeroℝ
    step2 = trans (cong (λ s → s +ℝ negℝ t) (sym h)) (+-inv-ℝ t)

-- ==================================================================
-- §3 Cauchy-Schwarz 不等式（阶段 8-2，2026-08-02）
-- ==================================================================

-- **可证**：⟨x,0⟩ = 0（对称性 + 0 的自加性 + ℝ 双自零）
ip-zero-r : (x : V) → x ⟨⟩ zeroᵥ ≡ zeroℝ
ip-zero-r x = trans (ip-sym x zeroᵥ) (double-self-zero t-double)
  where
  -- ⟨0,x⟩ = ⟨0+0,x⟩ = ⟨0,x⟩+⟨0,x⟩（+ᵥ-ident + 左加性）
  t-double : zeroᵥ ⟨⟩ x ≡ (zeroᵥ ⟨⟩ x) +ℝ (zeroᵥ ⟨⟩ x)
  t-double =
    trans (cong (λ w → w ⟨⟩ x) (sym (+ᵥ-ident zeroᵥ)))
          (ip-add-l zeroᵥ zeroᵥ x)
  -- ℝ 层：t = t+t ⟹ t = 0（与 norm-sq-zero 同机制）
  double-self-zero : {t : ℝ} → t ≡ t +ℝ t → t ≡ zeroℝ
  double-self-zero {t} h = trans (sym step1) step2
    where
    step1 : (t +ℝ t) +ℝ negℝ t ≡ t
    step1 = trans (+-assoc-ℝ t t (negℝ t))
                  (trans (cong (λ s → t +ℝ s) (+-inv-ℝ t))
                         (+-ident-ℝ t))
    step2 : (t +ℝ t) +ℝ negℝ t ≡ zeroℝ
    step2 = trans (cong (λ s → s +ℝ negℝ t) (sym h)) (+-inv-ℝ t)

-- **可证**：⟨0,x⟩ = 0（对称性 + ⟨x,0⟩ = 0）
ip-zero-l : (x : V) → zeroᵥ ⟨⟩ x ≡ zeroℝ
ip-zero-l x = trans (ip-sym zeroᵥ x) (ip-zero-r x)

-- **可证**：⟨x+ay, x+ay⟩ 展开（左/右加性 + 左/右标量 + 对称性）
ip-expand : (a : ℝ) (x y : V) →
  (x +ᵥ (a ·ᵥ y)) ⟨⟩ (x +ᵥ (a ·ᵥ y))
  ≡ (norm-sq x +ℝ (a *ℝ (x ⟨⟩ y))) +ℝ ((a *ℝ (x ⟨⟩ y)) +ℝ ((a *ℝ a) *ℝ norm-sq y))
ip-expand a x y =
  trans (ip-add-l x (a ·ᵥ y) (x +ᵥ (a ·ᵥ y)))
        (cong₂ _+ℝ_
          (trans (ip-add-r x x (a ·ᵥ y))
                 (cong₂ _+ℝ_ refl (ip-scalar-r a x y)))
          (trans (ip-add-r (a ·ᵥ y) x (a ·ᵥ y))
                 (cong₂ _+ℝ_
                   (trans (ip-scalar-l a y x)
                          (cong (λ u → a *ℝ u) (ip-sym y x)))
                   (trans (ip-scalar-l a y (a ·ᵥ y))
                          (trans (cong (λ u → a *ℝ u) (ip-scalar-r a y y))
                                 (sym (*-assoc-ℝ a a (y ⟨⟩ y))))))))

-- Cauchy-Schwarz 核心约简（纯 ℝ 代数）：t = -(p/q) 时
--   (A + t·p) + (t·p + t²·q) ≡ A - p²/q（tp-ident + ttq-ident + 加性逆/单位）
cs-core : (p A q : ℝ) →
  (A +ℝ ((negℝ (p /ℝ q)) *ℝ p)) +ℝ (((negℝ (p /ℝ q)) *ℝ p) +ℝ (((negℝ (p /ℝ q)) *ℝ (negℝ (p /ℝ q))) *ℝ q))
  ≡ A +ℝ negℝ ((p *ℝ p) /ℝ q)
cs-core p A q =
  trans (cong₂ _+ℝ_
                (cong (λ u → A +ℝ u) (tp-ident p q))
                (cong₂ _+ℝ_ (tp-ident p q) (ttq-ident p q)))
        (trans (cong₂ _+ℝ_ refl (trans (+-comm-ℝ (negℝ ((p *ℝ p) /ℝ q)) ((p *ℝ p) /ℝ q))
                                       (+-inv-ℝ ((p *ℝ p) /ℝ q))))
               (+-ident-ℝ (A +ℝ negℝ ((p *ℝ p) /ℝ q))))

-- **可证**：Cauchy-Schwarz（Hilbert 空间层核心——范数公理依赖它）
--   ⟨x,y⟩² ≤ ‖x‖²·‖y‖²
-- 思路：三分律分 ‖y‖² = 0 / > 0 / < 0（后两者经正定性/正性排除）；
--   ‖y‖² > 0 时取 t = -⟨x,y⟩/‖y‖²，⟨x+ty, x+ty⟩ ≥ 0 展开为
--   ‖x‖² - ⟨x,y⟩²/‖y‖² ≥ 0，乘正 ‖y‖² 得 ⟨x,y⟩² ≤ ‖x‖²·‖y‖²。
cauchy-schwarz : (x y : V) → ((x ⟨⟩ y) *ℝ (x ⟨⟩ y)) ≤ℝ (norm-sq x *ℝ norm-sq y)
cauchy-schwarz x y with trichotomy-ℝ zeroℝ (norm-sq y)
cauchy-schwarz x y | inj₁ q-pos = final
  where
  p : ℝ
  p = x ⟨⟩ y
  A : ℝ
  A = norm-sq x
  q : ℝ
  q = norm-sq y
  t : ℝ
  t = negℝ (p /ℝ q)

  -- 0 < q ⟹ 0 ≤ q
  zero≤q : zeroℝ ≤ℝ q
  zero≤q = <-≤-ℝ q-pos

  -- ⟨x+ty, x+ty⟩ ≥ 0（内积正性）
  h0 : zeroℝ ≤ℝ ((x +ᵥ (t ·ᵥ y)) ⟨⟩ (x +ᵥ (t ·ᵥ y)))
  h0 = ip-pos (x +ᵥ (t ·ᵥ y))

  -- 展开：⟨x+ty,x+ty⟩ = (A + t·p) + (t·p + t²·q)
  h1 : (x +ᵥ (t ·ᵥ y)) ⟨⟩ (x +ᵥ (t ·ᵥ y)) ≡ (A +ℝ (t *ℝ p)) +ℝ ((t *ℝ p) +ℝ ((t *ℝ t) *ℝ q))
  h1 = ip-expand t x y

  -- 约简：t·p = -p²/q、t²·q = p²/q ⟹ (A+t·p)+(t·p+t²·q) = A - p²/q
  h2 : (x +ᵥ (t ·ᵥ y)) ⟨⟩ (x +ᵥ (t ·ᵥ y)) ≡ A +ℝ negℝ ((p *ℝ p) /ℝ q)
  h2 = trans h1 (cs-core p A q)

  -- 0 ≤ A - p²/q ⟹ p²/q ≤ A（移项）
  h3 : ((p *ℝ p) /ℝ q) ≤ℝ A
  h3 = ≤-from-nonneg (subst (λ u → zeroℝ ≤ℝ u) h2 h0)

  -- 乘正 q：p² ≤ A·q（非负侧乘保序 + 乘除消去）
  final : ((x ⟨⟩ y) *ℝ (x ⟨⟩ y)) ≤ℝ (norm-sq x *ℝ norm-sq y)
  final = div-≤-mul {p = p *ℝ p} {a = A} {q = q} zero≤q h3

-- ‖y‖² = 0 分支：正定性 ⟹ y = 0 ⟹ ⟨x,y⟩² = 0 = ‖x‖²·‖y‖²
cauchy-schwarz x y | inj₂ (inj₁ q-zero) =
  subst (λ v → ((x ⟨⟩ y) *ℝ (x ⟨⟩ y)) ≤ℝ v) (sym Aq-zero)
        (subst (λ u → u ≤ℝ zeroℝ) (sym pp-zero)
               (refl-≤ℝ {zeroℝ}))
  where
  -- ‖y‖² = 0 ⟹ y = 0（正定性）
  y-zero : y ≡ zeroᵥ
  y-zero = ip-def y (sym q-zero)
  -- x⟨⟩y = 0（y = 0 + ⟨x,0⟩ = 0）
  p-eq : x ⟨⟩ y ≡ zeroℝ
  p-eq = trans (cong (λ w → x ⟨⟩ w) y-zero) (ip-zero-r x)
  -- ⟨x,y⟩² = 0
  pp-zero : (x ⟨⟩ y) *ℝ (x ⟨⟩ y) ≡ zeroℝ
  pp-zero = trans (cong₂ _*ℝ_ p-eq p-eq) (*-zero-ℝ zeroℝ)
  -- ‖x‖²·‖y‖² = 0（‖y‖² = 0 + 零吸收）
  Aq-zero : norm-sq x *ℝ norm-sq y ≡ zeroℝ
  Aq-zero = trans (cong (λ u → norm-sq x *ℝ u) q-eq) (*-zero-ℝ (norm-sq x))
    where
    q-eq : norm-sq y ≡ zeroℝ
    q-eq = trans (cong₂ _⟨⟩_ y-zero y-zero) norm-sq-zero

-- ‖y‖² < 0 分支：与正性 0 ≤ ‖y‖² 矛盾（lt-≤-trans + 反自反）
cauchy-schwarz x y | inj₂ (inj₂ q-neg) =
  ⊥-elim (irreflexive-ℝ (lt-≤-trans-ℝ q-neg (ip-pos y)))

-- ==================================================================
-- §4 范数公理落地（阶段 8-2b，2026-08-02：√ 分析层扩展 + 三角不等式）
-- ==================================================================

-- 范数：‖v‖ := √⟨v,v⟩（√ 分析层扩展）
norm : V → ℝ
norm v = sqrt (norm-sq v)

-- **可证**：‖v‖ ≥ 0（正性：√ 非负）
norm-nonneg : (v : V) → zeroℝ ≤ℝ norm v
norm-nonneg v = sqrt-nonneg (norm-sq v) (ip-pos v)

-- **可证**：C-S 的范数形式——⟨x,y⟩ ≤ ‖x‖·‖y‖
--（a ≤ √(a²) [le-sqrt-sq] + √ 单调 [sqrt-mono] + √ 乘法性 [sqrt-mul]）
cs-norm : (x y : V) → (x ⟨⟩ y) ≤ℝ (norm x *ℝ norm y)
cs-norm x y =
  ≤-trans-ℝ (le-sqrt-sq (x ⟨⟩ y))
    (subst (λ z → sqrt ((x ⟨⟩ y) *ℝ (x ⟨⟩ y)) ≤ℝ z)
           (sqrt-mul (norm-sq x) (norm-sq y) (ip-pos x) (ip-pos y))
           (sqrt-mono (sq-nonneg-ℝ (x ⟨⟩ y)) (cauchy-schwarz x y)))

-- **可证**：‖x+y‖² 展开——‖x+y‖² = (‖x‖²+⟨x,y⟩)+(⟨x,y⟩+‖y‖²)
norm-sq-add : (x y : V) → norm-sq (x +ᵥ y) ≡ (norm-sq x +ℝ (x ⟨⟩ y)) +ℝ ((x ⟨⟩ y) +ℝ norm-sq y)
norm-sq-add x y =
  trans (ip-add-l x y (x +ᵥ y))
        (cong₂ _+ℝ_ (ip-add-r x x y)
                     (trans (ip-add-r y x y) (cong₂ _+ℝ_ (ip-sym y x) refl)))

-- **可证**：‖v‖² = ‖v‖·‖v‖（sq-sqrt）
norm-sq-norm : (v : V) → norm-sq v ≡ norm v *ℝ norm v
norm-sq-norm v = sym (sq-sqrt (norm-sq v) (ip-pos v))

-- **可证**：(‖x‖+‖y‖)² = ‖x‖² + 2·(‖x‖·‖y‖) + ‖y‖²（sum-sq-ℝ + norm-sq-norm）
norm-sum-sq : (x y : V) → (norm x +ℝ norm y) *ℝ (norm x +ℝ norm y)
  ≡ (norm-sq x +ℝ (natℝ 2 *ℝ (norm x *ℝ norm y))) +ℝ norm-sq y
norm-sum-sq x y =
  trans (sum-sq-ℝ (norm x) (norm y))
        (cong₂ _+ℝ_ (cong₂ _+ℝ_ (sym (norm-sq-norm x)) refl)
                     (sym (norm-sq-norm y)))

-- **可证**：‖x+y‖² ≤ (‖x‖+‖y‖)²
--（‖x+y‖² = (A+p)+(p+B) [norm-sq-add] ≤ (A+M)+(M+B) [sum-add-≤ + cs-norm]
--  = A+2M+B [two-add-eq] = (‖x‖+‖y‖)² [norm-sum-sq]）
norm-sq-tri : (x y : V) → norm-sq (x +ᵥ y) ≤ℝ ((norm x +ℝ norm y) *ℝ (norm x +ℝ norm y))
norm-sq-tri x y =
  subst (λ u → u ≤ℝ ((norm x +ℝ norm y) *ℝ (norm x +ℝ norm y)))
        (sym (norm-sq-add x y))
        (subst (λ v → ((norm-sq x +ℝ (x ⟨⟩ y)) +ℝ ((x ⟨⟩ y) +ℝ norm-sq y)) ≤ℝ v)
               (sym (norm-sum-sq x y))
               (subst (λ v → ((norm-sq x +ℝ (x ⟨⟩ y)) +ℝ ((x ⟨⟩ y) +ℝ norm-sq y)) ≤ℝ v)
                      (two-add-eq (norm-sq x) (norm x *ℝ norm y) (norm-sq y))
                      (sum-add-≤ (norm-sq x) (x ⟨⟩ y) (norm-sq y) (norm x *ℝ norm y)
                                 (cs-norm x y))))

-- **可证**：0 ≤ ‖x‖+‖y‖（三角不等式 √ 侧的非负性前提）
sum-nonneg : (x y : V) → zeroℝ ≤ℝ (norm x +ℝ norm y)
sum-nonneg x y =
  subst (λ z → z ≤ℝ (norm x +ℝ norm y)) (zero-add-ℝ zeroℝ)
        (≤-+-mono-ℝ (norm-nonneg x) (norm-nonneg y))

-- **可证**：三角不等式——‖x+y‖ ≤ ‖x‖+‖y‖
--（√ 单调于 ‖x+y‖² ≤ (‖x‖+‖y‖)² + √((‖x‖+‖y‖)²) = ‖x‖+‖y‖ [sqrt-sq]）
norm-tri : (x y : V) → norm (x +ᵥ y) ≤ℝ (norm x +ℝ norm y)
norm-tri x y =
  subst (λ w → sqrt (norm-sq (x +ᵥ y)) ≤ℝ w)
        (sqrt-sq (norm x +ℝ norm y) (sum-nonneg x y))
        (sqrt-mono (ip-pos (x +ᵥ y)) (norm-sq-tri x y))

-- **可证**：‖0‖ = 0（零元）
norm-zero : norm zeroᵥ ≡ zeroℝ
norm-zero = trans (cong sqrt norm-sq-zero) sqrt-zero

-- **可证**：正定性——‖v‖ = 0 ⟹ v = 0（(√‖v‖²)² = ‖v‖² = 0 + ip-def）
norm-def : (v : V) → norm v ≡ zeroℝ → v ≡ zeroᵥ
norm-def v h = ip-def v (trans (sym (sq-sqrt (norm-sq v) (ip-pos v)))
                               (trans (cong₂ _*ℝ_ h h) (*-zero-ℝ zeroℝ)))

-- **可证**：齐次——‖a·v‖ = |a|·‖v‖（√ 乘法性 + ‖a·v‖² = a²‖v‖²）
norm-scalar : (a : ℝ) (v : V) → norm (a ·ᵥ v) ≡ abs a *ℝ norm v
norm-scalar a v =
  trans (cong sqrt (norm-sq-scalar a v))
        (sqrt-mul (a *ℝ a) (norm-sq v) (sq-nonneg-ℝ a) (ip-pos v))

-- ==================================================================
-- §5 有界线性算子 + 算子范数（阶段 8-3，2026-08-02）
-- ==================================================================

-- 本地 Σ（Set 层依赖对，库未提供；构造子 ex 避免与 _×_ 的 _,_ 冲突）
data Σ (A : Set) (B : A → Set) : Set where
  ex : (a : A) → B a → Σ A B

-- 线性算子 B(H)：f : V → V 保持加性与标量乘
record LinOp : Set where
  field
    f : V → V
    lin-add : (x y : V) → f (x +ᵥ y) ≡ f x +ᵥ f y
    lin-scalar : (a : ℝ) (x : V) → f (a ·ᵥ x) ≡ a ·ᵥ f x

-- **可证**（V 层双自零）：w = w + w ⟹ w = 0（⟨w,w⟩ = ⟨w,w⟩+⟨w,w⟩ + 正定性）
v-double-zero : {w : V} → w ≡ w +ᵥ w → w ≡ zeroᵥ
v-double-zero {w} h = ip-def w (double-self-zero step1)
  where
  -- ⟨w,w⟩ = ⟨w+w,w⟩ = ⟨w,w⟩+⟨w,w⟩
  step1 : w ⟨⟩ w ≡ (w ⟨⟩ w) +ℝ (w ⟨⟩ w)
  step1 = trans (cong (λ u → u ⟨⟩ w) h) (ip-add-l w w w)
  -- ℝ 双自零：t = t+t ⟹ t = 0
  double-self-zero : {t : ℝ} → t ≡ t +ℝ t → t ≡ zeroℝ
  double-self-zero {t} h' = trans (sym s1) s2
    where
    s1 : (t +ℝ t) +ℝ negℝ t ≡ t
    s1 = trans (+-assoc-ℝ t t (negℝ t))
               (trans (cong (λ s → t +ℝ s) (+-inv-ℝ t)) (+-ident-ℝ t))
    s2 : (t +ℝ t) +ℝ negℝ t ≡ zeroℝ
    s2 = trans (cong (λ s → s +ℝ negℝ t) (sym h')) (+-inv-ℝ t)

-- **可证**：线性 ⟹ T(0) = 0（T(0) = T(0+0) = T0 + T0 ⟹ 双自零）
lin-zero : (T : LinOp) → LinOp.f T zeroᵥ ≡ zeroᵥ
lin-zero T = v-double-zero double
  where
  double : LinOp.f T zeroᵥ ≡ LinOp.f T zeroᵥ +ᵥ LinOp.f T zeroᵥ
  double =
    trans (cong (λ w → LinOp.f T w) (sym (+ᵥ-ident zeroᵥ)))
          (LinOp.lin-add T zeroᵥ zeroᵥ)

-- **可证**：标量零吸收 a·0 = 0（a·0 = a·(0+0) = a·0 + a·0 ⟹ 双自零）
scalar-zero : (a : ℝ) → a ·ᵥ zeroᵥ ≡ zeroᵥ
scalar-zero a = v-double-zero double
  where
  double : a ·ᵥ zeroᵥ ≡ (a ·ᵥ zeroᵥ) +ᵥ (a ·ᵥ zeroᵥ)
  double =
    trans (cong (λ w → a ·ᵥ w) (sym (+ᵥ-ident zeroᵥ)))
          (·ᵥ-distrib-l a zeroᵥ zeroᵥ)

-- **可证**（V 层交换重排）：(a+b)+(c+d) = (a+c)+(b+d)
swap-pair-ᵥ : (a b c d : V) → (a +ᵥ b) +ᵥ (c +ᵥ d) ≡ (a +ᵥ c) +ᵥ (b +ᵥ d)
swap-pair-ᵥ a b c d =
  trans (+ᵥ-assoc a b (c +ᵥ d))
        (trans (cong (λ u → a +ᵥ u) (+ᵥ-comm b (c +ᵥ d)))
               (trans (sym (+ᵥ-assoc a (c +ᵥ d) b))
                      (trans (cong (λ u → u +ᵥ b) (sym (+ᵥ-assoc a c d)))
                             (trans (+ᵥ-assoc (a +ᵥ c) d b)
                                    (cong (λ u → (a +ᵥ c) +ᵥ u) (+ᵥ-comm d b))))))

-- 零算子（点态零，线性性经 +ᵥ-ident/scalar-zero）
zero-op : LinOp
zero-op = record
  { f = λ _ → zeroᵥ
  ; lin-add = λ x y → sym (+ᵥ-ident zeroᵥ)
  ; lin-scalar = λ a x → sym (scalar-zero a)
  }

-- 逐点加法（线性性经 swap-pair-ᵥ / ·ᵥ-distrib-l 反向）
op-add : LinOp → LinOp → LinOp
op-add S T = record
  { f = λ x → LinOp.f S x +ᵥ LinOp.f T x
  ; lin-add = λ x y →
      trans (cong₂ _+ᵥ_ (LinOp.lin-add S x y) (LinOp.lin-add T x y))
            (swap-pair-ᵥ (LinOp.f S x) (LinOp.f S y) (LinOp.f T x) (LinOp.f T y))
  ; lin-scalar = λ a x →
      trans (cong₂ _+ᵥ_ (LinOp.lin-scalar S a x) (LinOp.lin-scalar T a x))
            (sym (·ᵥ-distrib-l a (LinOp.f S x) (LinOp.f T x)))
  }

-- 复合（线性性经逐层传递）
op-comp : LinOp → LinOp → LinOp
op-comp S T = record
  { f = λ x → LinOp.f S (LinOp.f T x)
  ; lin-add = λ x y →
      trans (cong (LinOp.f S) (LinOp.lin-add T x y))
            (LinOp.lin-add S (LinOp.f T x) (LinOp.f T y))
  ; lin-scalar = λ a x →
      trans (cong (LinOp.f S) (LinOp.lin-scalar T a x))
            (LinOp.lin-scalar S a (LinOp.f T x))
  }

-- 算子范数族（共享谓词：‖v‖ ≤ 1 且 r = ‖Tv‖）
op-fam : LinOp → ℝ → Set
op-fam T = λ r → Σ V (λ v → (norm v ≤ℝ oneℝ) × (r ≡ norm (LinOp.f T v)))

-- 算子范数：‖T‖ := sup_{‖v‖≤1} ‖Tv‖（sup-ℝ 完备性基础假设）
op-norm : LinOp → ℝ
op-norm T = sup-ℝ (op-fam T)

-- **可证**：‖T‖ ≥ 0（T(0) = 0 是单位球内成员，sup-upper）
op-norm-nonneg : (T : LinOp) → zeroℝ ≤ℝ op-norm T
op-norm-nonneg T = sup-upper (op-fam T) zeroℝ (ex zeroᵥ (norm-zero-≤-one , norm-T-zero))
  where
  -- ‖0‖ ≤ 1（‖0‖ = 0 ≤ 1）
  norm-zero-≤-one : norm zeroᵥ ≤ℝ oneℝ
  norm-zero-≤-one = subst (λ z → z ≤ℝ oneℝ) (sym norm-zero) (<-≤-ℝ zero-lt-one-ℝ)
  -- 0 = ‖T0‖（T0 = 0 + ‖0‖ = 0）
  norm-T-zero : zeroℝ ≡ norm (LinOp.f T zeroᵥ)
  norm-T-zero = sym (trans (cong norm (lin-zero T)) norm-zero)

-- **可证**：上界性——‖v‖ ≤ 1 ⟹ ‖Tv‖ ≤ ‖T‖（sup-upper 直接）
op-norm-upper : (T : LinOp) (v : V) → norm v ≤ℝ oneℝ → norm (LinOp.f T v) ≤ℝ op-norm T
op-norm-upper T v hv = sup-upper (op-fam T) (norm (LinOp.f T v)) (ex v (hv , refl))

-- **可证**：‖S+T‖ ≤ ‖S‖+‖T‖（norm-tri 逐点 + sup-least）
op-norm-tri : (S T : LinOp) → op-norm (op-add S T) ≤ℝ (op-norm S +ℝ op-norm T)
op-norm-tri S T = sup-least (op-fam (op-add S T)) (op-norm S +ℝ op-norm T) bound
  where
  bound : (r : ℝ) → op-fam (op-add S T) r → r ≤ℝ (op-norm S +ℝ op-norm T)
  bound r (ex v (hv , refl)) =
    ≤-trans-ℝ (norm-tri (LinOp.f S v) (LinOp.f T v))
              (≤-+-mono-ℝ (op-norm-upper S v hv) (op-norm-upper T v hv))

-- 本层状态：
--  - 向量空间 + 内积基础登记（基础假设，注明模型必然性 = 希尔伯特空间理论）。
--  - 内积双线性（右加性/右标量经对称性可证）；范数平方的齐次/正性/零性可证。
--  - 阶段 2（✅ 2026-08-02）：Cauchy-Schwarz（⟨x,y⟩² ≤ ‖x‖²·‖y‖²，
--    三分律 + t = -⟨x,y⟩/‖y‖² 判别式，全部可证、零新增公理）；
--    DHStructural 前置：取负×乘/乘除结合/分数乘除消去/≤ 移项/非负侧乘保序（可证）。
--  - 阶段 2b（✅ 2026-08-02）：范数公理落地——norm := √(‖·‖²)（√ 分析层扩展），
--    正性 norm-nonneg / 齐次 norm-scalar（|a|·‖v‖）/ 三角 norm-tri /
--    正定性 norm-zero/norm-def 全部可证（依赖 C-S 的 cs-norm 形式）。
--  - 阶段 3（✅ 2026-08-02）：有界线性算子 + 算子范数——LinOp record +
--    算子代数（zero-op/op-add/op-comp）+ 线性⟹T0=0；op-norm := sup_{‖v‖≤1}‖Tv‖
--    （sup-ℝ 完备性假设）；op-norm-nonneg/op-norm-upper/op-norm-tri 可证。
--    待（8-3b）：缩放引理 ⟹ op-norm-submul（‖ST‖ ≤ ‖S‖‖T‖）。
--  - 阶段 4+（待）：自伴算子 + C* 恒等（norm-power）⟹
--    SpectralTheory §12 C*-范数公理降定理路径。
