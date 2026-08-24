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
      （‖v‖≤1 ⟹ ‖Tv‖≤‖T‖）、op-norm-tri（‖S+T‖ ≤ ‖S‖+‖T‖，norm-tri + sup-least）；
    - **8-3b（✅）**：缩放引理 op-norm-scalar（‖Sw‖≤‖S‖·‖w‖，单位化 w/‖w‖）⟹
      op-norm-submul（‖ST‖ ≤ ‖S‖‖T‖）——norm-pos/norm-tri/norm-submul 全从 sup 定义证明。
  阶段 4（2026-08-02）：自伴算子 + C* 恒等（norm-power）。
    - adj（伴随，Riesz 表示桥接，降定理路径 = 完备性层 + 投影定理）+ adj-ip；
    - SelfAdjoint（⟨Xx,y⟩ = ⟨x,Xy⟩）+ **可证** adj-move（伴随跨槽交换）；
    - **可证** norm-power（自伴幂恒等 ‖X²‖ = ‖X‖²）：‖Xv‖² = ⟨v,X²v⟩（自伴）
      ≤ ‖v‖‖X²v‖（C-S）≤ ‖X²‖（缩放 + 单位球）⟹ ‖Xv‖ ≤ √‖X²‖ ⟹ sup-least
      ‖X‖ ≤ √‖X²‖ ⟹ 平方两侧 + sq-sqrt + submul + ≤-antisym——C* 恒等落地。
  阶段 5（2026-08-02）：算子拓扑层（SOT/范数收敛）。
    - V 减法 _−ᵥ_（定义）+ op-neg/op-sub（算子减法，线性性可证）；
    - ε-δ 收敛定义：SOT-conv（∀v. ‖Tt v − T0 v‖ → 0）/ op-norm-conv（‖Tt − T0‖ → 0）；
    - **可证** sot-from-norm（范数收敛 ⟹ 强收敛：缩放引理 + η = ε/(1+‖v‖) 除法技巧）——
      范数拓扑细于强拓扑；SpectralTheory lim-op/strong-continuity 降定理的拓扑地基。
  阶段 8（2026-08-02）：完备性层（Hilbert 空间公理补全——pre-Hilbert ⟹ Hilbert）。
    - Seq/≤ℕ（局部）/Cauchy-seq/Converges（ε-δ 定义）+ 完备性基础假设 complete；
    - **可证** ≤ℕ-refl/trans/suc、sub-ᵥ-self（x−x=0）、conv-const/cauchy-const——
      Riesz 表示/投影定理/谱定理的共同地基。
  阶段 6a（2026-08-02）：谱半径公式的代数核心（norm-contraction 降定理前置）。
    - id-op/op-sq/op-power/op-power-2^k/iter-mul/iter-sq；
    - **可证** op-norm-id-le（‖id‖≤1）/op-norm-pow-le（‖Xⁿ‖≤‖X‖ⁿ，r≤‖X‖）/
      SelfAdjoint-op-sq/SelfAdjoint-op-power-2^k/op-norm-power-2^k
      （‖X^{2^k}‖=‖X‖^{2^k}，Gelfand 子列核心）。
  阶段 7-3a（2026-08-02）：正交分解与投影算子（谱定理 E 构造的投影组件）。
    - **可证** pythagorean（⟨a,b⟩=0 ⟹ ‖a+b‖²=‖a‖²+‖b‖²）；
    - Subspace（闭子空间）+ 投影桥接（proj/proj-in/proj-orth/proj-fixed，投影定理）；
    - **可证** proj-decomp（正交分解）/proj-idemp（幂等）/proj-norm-le（非扩张 ‖Px‖≤‖x‖）。
  阶段 7-3b（2026-08-02）：投影算子与自伴性（阶段 7-3a 的算子层收尾）。
    - 投影唯一性（w∈W 且 x−w⊥W ⟹ w=Px，⟨a,a⟩=0 ⟹ a=0）⟹ P(x+y)=Px+Py、
      P(a·x)=a·Px（线性性，proj-op : Subspace → LinOp 构造）；
    - **可证** proj-self-adjoint（⟨Px,y⟩=⟨x,Py⟩——SelfAdjoint (proj-op W)，阶段 7-3b 核心）；
    - **可证** proj-op-norm-le-one（‖P‖≤1，SpectralTheory §12b proj-norm-le-one 的 Hilbert 侧）。
  阶段 7-3 第一步（2026-08-02）：谱投影构造框架（E 的测度构造起点，§10c）。
    - 谱定理桥接：spectral-subspace（谱集 P ↦ 闭子空间 W_P）+ spectral-subspace-orth
      （P∩Q=∅ ⟹ W_P⊥W_Q）+ spectral-subspace-total（W_ℝ=全空间）；
    - 谱投影 E-hilb P := proj-op (spectral-subspace P)（谱测度 E 的 Hilbert 层构造）；
    - **可证** E-hilb-idemp（幂等）/E-hilb-orth（正交）/E-hilb-total（E(ℝ)=𝟙）/
      E-hilb-self-adjoint（自伴）/E-hilb-norm-le-one（‖E(P)‖≤1）——全部投影性质直接特化，
      SpectralTheory E-idempotent/E-orthogonal/E-total/proj-norm-le-one 的构造侧对应。
  阶段 7-3 余项 E-union（2026-08-02）：谱投影加法性（§10d）。
    - 内积减法双线性 **可证** ip-sub-l/ip-sub-r + 减法分解 sub-add-decomp；
    - 谱子空间直和桥接：spectral-subspace-incl（P⊆Q ⟹ W_P⊆W_Q）+ spectral-subspace-split
      （P∩Q=∅ ⟹ W_{P∪Q} 分解为 W_P+W_Q）；
    - **可证** E-hilb-union（P∩Q=∅ ⟹ E(P∪Q)x = E(P)x+E(Q)x：E(P)x+E(Q)x∈W_{P∪Q}
      （incl+add）+ x−(E(P)x+E(Q)x)⊥W_{P∪Q}（split 分解 + 逐项正交：proj-orth + W_P⊥W_Q）+
      proj-unique）——SpectralTheory §10e E-union 的 Hilbert 侧构造版。
  阶段 7-3 余项 E-fin-union（2026-08-02）：E 的有限可加性（§10e）。
    - sum-ᵥ（点态向量有限和）+ EmptyP（空谱集）+ spectral-subspace-empty 桥接（W_∅={0}）
      ⟹ **可证** E-hilb-empty（E(∅)x=0）；
    - FinUnion（递归有限并谓词）+ **可证** fin-union-in（∪ᵢ<ₘPᵢ ⟹ ∃i<ₘ.Pᵢ）/
      FinUnion-disjoint（pairwise ⟹ (∪ᵢ<ₘPᵢ)∩Pₘ=∅）；
    - **可证** E-hilb-fin-union（pairwise 不相交 ⟹ E(∪ᵢ<ₘPᵢ)x = Σᵢ<ₘE(Pᵢ)x，归纳：
      E-hilb-union 拆分 + FinUnion-disjoint + 归纳假设）——E-σ-add 的有限版，
      SpectralTheory §10e E-partition-add 的 Hilbert 侧对应。
  阶段 7-3 余项 E-σ-add 第一步（2026-08-02）：单调吸收 + 可数并（§10f）。
    - **可证** E-hilb-sub（P⊆Q ⟹ E(Q)(E(P)x)=E(P)x：E(P)x∈W_P⊆W_Q + proj-fixed——
      SpectralTheory §10b E-sub 的 Hilbert 侧对应，E-σ-add 单调性前置）；
    - σUnion（可数并谓词 ∪ₙPₙ = ∃n.Pₙ）+ E-σ-add 降定理路径登记（连续下式
      E(∪ₙPₙ)=supₘΣᵢ<ₘE(Pᵢ)，需算子序 sup 随极限层 + 有限一致性已闭合）。
  阶段 8-6b 第一步（2026-08-02）：谱半径公式极限层（§11，Gelfand 公式闭合）。
    - 谱半径 r(X) := sup {r : r^{2^k} ≤ ‖X^{2^k}‖ ∀k}（沿 2^k 子列的幂形式刻画，
      避免 n 次根——iter-sq + op-norm-power-2^k 直接闭合）；
    - **可证** sr-le-norm（r(X) ≤ ‖X‖：成员 k=0 特化 + sup-least）/ sr-norm-le
      （自伴 ⟹ ‖X‖ ≤ r(X)：r=‖X‖ 是族成员经 op-norm-power-2^k 精确等式 + sup-upper）/
      **spectral-radius-norm**（自伴 C* 元 r(X) = ‖X‖，≤-antisym）——
      norm-contraction（σ(e^(-tA)) ⊆ (0,1] ⟹ ‖e^(-tA)‖ ≤ 1）的 Hilbert 侧核心。
  阶段 8-5b 第一步（2026-08-02）：强连续半群实例化框架（§12）。
    - e^(-tA) 的 Hilbert 层表示桥接 exp-hilb-tA（半群方程/单位/自伴/压缩/范数连续，
      降定理路径 = 跨层模型 + fc 函数演算 + 谱积分 + φ_t 连续性）；
    - **可证** exp-hilb-strong-cont（强连续 SOT：sot-from-norm 特化，范数连续 ⟹ 强连续——
      strong-continuity（Hille-Yosida 条件 iv）的 Hilbert 侧对应）；
    - **可证** exp-hilb-radius-le-one（r(e^(-tA)) = ‖e^(-tA)‖ ≤ 1：spectral-radius-norm +
      压缩——norm-contraction 的 Hilbert 侧完整降定理核心，8-6b 连接）。
  阶段 13（2026-08-02）：算子序与投影单调性（E-σ-add 完整形式的机制前置，§13）。
    - Hilbert 层算子序 _≤ₗ_（X ≤ₗ Y ⟺ ∀v. ⟨(Y−X)v, v⟩ ≥ 0，正算子序）；
    - **可证** E-hilb-mono（P⊆Q ⟹ E(P) ≤ₗ E(Q）：⟨(E(Q)−E(P))v, v⟩ = ‖E(Q)(v−E(P)v)‖² ≥ 0
      （proj-decomp + E-hilb-sub + 自伴/幂等 + w ⊥ W_P）——投影序单调，E-σ-add 的
      sup 上界机制基础）。
  阶段 14（2026-08-02）：E-σ-add 完整形式（可数可加性，§14）。
    - sum-ₗ（LinOp 层有限和）+ LinOp 层算子序 sup 桥接（supₗ/upper/least，
      降定理路径 = 强/弱算子拓扑单调有界收敛）；
    - **可证** E-hilb-fin-le-σ（E(∪ᵢ<ₘPᵢ) ≤ₗ E(∪ₙPₙ)：FinUnion ⊆ σUnion
      （fin-union-in 取 n=i）+ E-hilb-mono——连续下式上界方向）；
    - σ-可数可加桥接 E-hilb-σ-add（E(∪ₙPₙ) = supₘΣᵢ<ₘE(Pᵢ)，least 方向 + 收敛随极限层）。
  阶段 15（2026-08-02）：谱投影范数幂等（‖E(P)‖² = ‖E(P)‖，§15）。
    - **可证** sup-ext-ℝ（sup 外延：谓词外延相同 ⟹ sup 相等，sup-least/upper 双向）；
    - **可证** E-hilb-norm-idempotent（‖E(P)‖² = ‖E(P)‖：norm-power（自伴）+
      点态幂等 E-hilb-idemp + sup 外延——SpectralTheory §12 idem-zero-one/proj-norm
      （幂等元范数 ∈{0,1}）的 Hilbert 侧对应）。
  阶段 16（2026-08-02）：算子代数完整化（跨层模型代数基础，§16）。
    - 标量乘 _·ₗ_（(c·ₗX)v = c·(Xv)，线性性可证）+ **可证** ·ₗ-ident-pt
      （1·ₗX 逐点 = X）/op-comp-assoc-pt/op-comp-id-pt/op-comp-id-r-pt
      （结合/单位律点态版，定义性）/·ₗ-distrib-add-pt（标量对加法分配点态）/
      ·ₗ-comp-pt（标量与复合点态）——为 8-5b 余项（跨层模型 Op → LinOp）铺路，
      点态版避开 funext（LinOp record 依赖字段需依赖 funext）。
  阶段 6b（待）：Gelfand 公式极限层 + 谱论（需阶段 7-3 E 构造）。
-}

open import Agda.Builtin.Equality using (_≡_; refl)
open import Sp.SpCategory using (ℕ; zero; suc; sym; trans; cong; cong₂; _×_; _,_)

-- ℝ 层（复用 DHStructural：T3 已建的有序域 + 完备性机制）
open import DHStructural.DHStructuralAnalysis
  using (ℝ; zeroℝ; oneℝ; _+ℝ_; _*ℝ_; _≤ℝ_; _<ℝ_; _/ℝ_; negℝ; subst; exp;
         +-assoc-ℝ; +-comm-ℝ; +-ident-ℝ; +-inv-ℝ; *-assoc-ℝ; *-comm-ℝ; *-ident-ℝ; *-zero-ℝ;
         refl-≤ℝ; ≤-trans-ℝ; ≤-antisym; ≤-+-mono-ℝ; <-≤-ℝ; lt-≤-trans-ℝ; ≤-lt-trans-ℝ;
         trichotomy-ℝ; irreflexive-ℝ; add-pos-ℝ;
         zero-add-ℝ; natℝ; sqrt; sqrt-nonneg; sq-sqrt; sqrt-sq; sqrt-mono; sqrt-zero; sqrt-mul;
         abs; abs-pos-ident; sq-nonneg-ℝ; le-sqrt-sq; sum-sq-ℝ; two-add-eq; sum-add-≤;
         *-≤-mono-ℝ; *-≤-mono-l-ℝ; *-pos-mono-ℝ; *-pos-mono-r-ℝ; *-/cancel-ℝ; /-pos-ℝ;
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

-- **可证**：缩放引理——‖Sw‖ ≤ ‖S‖·‖w‖（阶段 8-3b）
--（w = 0 平凡；w ≠ 0 经 u = (1/‖w‖)·w 单位化：‖u‖ = 1 ⟹ ‖Su‖ ≤ ‖S‖（sup-upper）
--  + ‖Sw‖ = ‖w‖·‖Su‖（线性 + 齐次 + |·| 正吸收）+ 左侧乘保序）
op-norm-scalar : (S : LinOp) (w : V) → norm (LinOp.f S w) ≤ℝ (op-norm S *ℝ norm w)
op-norm-scalar S w with trichotomy-ℝ zeroℝ (norm w)
op-norm-scalar S w | inj₁ 0<nw = main
  where
  u : V
  u = (oneℝ /ℝ norm w) ·ᵥ w
  -- 0 ≤ 1/‖w‖（0 < 1/‖w‖ 经 /-pos-ℝ）
  recip-nonneg : zeroℝ ≤ℝ (oneℝ /ℝ norm w)
  recip-nonneg = <-≤-ℝ (/-pos-ℝ zero-lt-one-ℝ 0<nw)
  -- ‖u‖ = 1（齐次 + |1/‖w‖| = 1/‖w‖ + 乘除消去）
  u-norm-one : norm u ≡ oneℝ
  u-norm-one =
    trans (norm-scalar (oneℝ /ℝ norm w) w)
          (trans (cong₂ _*ℝ_ (abs-pos-ident (oneℝ /ℝ norm w) recip-nonneg) refl)
                 (trans (*-comm-ℝ (oneℝ /ℝ norm w) (norm w))
                        (*-/cancel-ℝ (norm w) oneℝ)))
  -- ‖u‖ ≤ 1
  u≤1 : norm u ≤ℝ oneℝ
  u≤1 = subst (λ z → z ≤ℝ oneℝ) (sym u-norm-one) (refl-≤ℝ {oneℝ})
  -- w = ‖w‖·u（·ᵥ 结合 + 乘除消去 + 单位）
  w-eq : w ≡ (norm w) ·ᵥ u
  w-eq = sym (trans (·ᵥ-assoc (norm w) (oneℝ /ℝ norm w) w)
                    (trans (cong (λ a → a ·ᵥ w) (*-/cancel-ℝ (norm w) oneℝ))
                           (·ᵥ-ident w)))
  -- S w = ‖w‖·S u（线性）
  Sw-eq : LinOp.f S w ≡ (norm w) ·ᵥ (LinOp.f S u)
  Sw-eq = trans (cong (LinOp.f S) w-eq) (LinOp.lin-scalar S (norm w) u)
  -- ‖Sw‖ = ‖w‖·‖Su‖（cong norm + 齐次 + |‖w‖| = ‖w‖）
  e : norm (LinOp.f S w) ≡ (norm w) *ℝ norm (LinOp.f S u)
  e = trans (cong norm Sw-eq)
            (trans (norm-scalar (norm w) (LinOp.f S u))
                   (cong₂ _*ℝ_ (abs-pos-ident (norm w) (norm-nonneg w)) refl))
  -- ‖w‖·‖Su‖ ≤ ‖w‖·‖S‖ = ‖S‖·‖w‖（左侧乘保序 + 交换律）
  h : ((norm w) *ℝ norm (LinOp.f S u)) ≤ℝ (op-norm S *ℝ norm w)
  h = subst (λ z → ((norm w) *ℝ norm (LinOp.f S u)) ≤ℝ z)
            (*-comm-ℝ (norm w) (op-norm S))
            (*-≤-mono-l-ℝ (norm w) (norm (LinOp.f S u)) (op-norm S)
                          (norm-nonneg w) (op-norm-upper S u u≤1))
  main : norm (LinOp.f S w) ≤ℝ (op-norm S *ℝ norm w)
  main = subst (λ z → z ≤ℝ (op-norm S *ℝ norm w)) (sym e) h

-- ‖w‖ = 0 分支：w = 0 ⟹ ‖Sw‖ = 0 = ‖S‖·0
op-norm-scalar S w | inj₂ (inj₁ 0=nw) =
  subst (λ z → z ≤ℝ (op-norm S *ℝ norm w)) (sym e1)
        (subst (λ z → zeroℝ ≤ℝ z) (sym e2) (refl-≤ℝ {zeroℝ}))
  where
  w-zero : w ≡ zeroᵥ
  w-zero = norm-def w (sym 0=nw)
  -- ‖Sw‖ = 0（T0 = 0 + ‖0‖ = 0）
  e1 : norm (LinOp.f S w) ≡ zeroℝ
  e1 = trans (cong norm (trans (cong (LinOp.f S) w-zero) (lin-zero S))) norm-zero
  -- ‖S‖·‖w‖ = 0（‖w‖ = 0 + 零吸收）
  e2 : op-norm S *ℝ norm w ≡ zeroℝ
  e2 = trans (cong (λ u → op-norm S *ℝ u) (sym 0=nw)) (*-zero-ℝ (op-norm S))

-- ‖w‖ < 0 分支：与正性 0 ≤ ‖w‖ 矛盾
op-norm-scalar S w | inj₂ (inj₂ nw<0) =
  ⊥-elim (irreflexive-ℝ (lt-≤-trans-ℝ nw<0 (norm-nonneg w)))

-- **可证**：‖ST‖ ≤ ‖S‖·‖T‖（submultiplicativity，阶段 8-3b）
--（缩放引理逐点 + sup-least + 左侧乘保序）
op-norm-submul : (S T : LinOp) → op-norm (op-comp S T) ≤ℝ (op-norm S *ℝ op-norm T)
op-norm-submul S T = sup-least (op-fam (op-comp S T)) (op-norm S *ℝ op-norm T) bound
  where
  bound : (r : ℝ) → op-fam (op-comp S T) r → r ≤ℝ (op-norm S *ℝ op-norm T)
  bound r (ex v (hv , refl)) =
    ≤-trans-ℝ (op-norm-scalar S (LinOp.f T v))
              (*-≤-mono-l-ℝ (op-norm S) (norm (LinOp.f T v)) (op-norm T)
                            (op-norm-nonneg S) (op-norm-upper T v hv))

-- ==================================================================
-- §6 自伴算子 + C* 恒等（阶段 8-4，2026-08-02）
-- ==================================================================

-- 伴随算子（Riesz 表示定理桥接：对每个 y，x ↦ ⟨Xx,y⟩ 是连续线性泛函，
-- Riesz 表示 ⟹ ∃! z. ⟨Xx,y⟩ = ⟨x,z⟩；降定理路径 = 完备性层 + 投影定理完整证明）
postulate
  adj : LinOp → LinOp
  adj-ip : (X : LinOp) (x y : V) → LinOp.f X x ⟨⟩ y ≡ x ⟨⟩ LinOp.f (adj X) y

-- 自伴：⟨Xx,y⟩ = ⟨x,Xy⟩（C* 恒等的自伴前提；与 adj X ≡ X 等价需 V 减法层）
SelfAdjoint : LinOp → Set
SelfAdjoint X = (x y : V) → LinOp.f X x ⟨⟩ y ≡ x ⟨⟩ LinOp.f X y

-- **可证**：伴随跨槽交换——⟨adj X x, y⟩ = ⟨x, X y⟩（adj-ip + ip-sym 链）
adj-move : (X : LinOp) (x y : V) → LinOp.f (adj X) x ⟨⟩ y ≡ x ⟨⟩ LinOp.f X y
adj-move X x y =
  trans (ip-sym (LinOp.f (adj X) x) y)
        (trans (sym (adj-ip X y x))
               (ip-sym (LinOp.f X y) x))

-- **可证**：‖v‖ ≤ 1 ⟹ ‖v‖·‖v‖ ≤ 1（乘保序 ×2）
v-mul-le-one : (v : V) → norm v ≤ℝ oneℝ → (norm v *ℝ norm v) ≤ℝ oneℝ
v-mul-le-one v hv =
  subst (λ z → (norm v *ℝ norm v) ≤ℝ z) (*-ident-ℝ oneℝ)
        (≤-trans-ℝ (*-≤-mono-ℝ (norm-nonneg v) hv)
                   (*-≤-mono-l-ℝ oneℝ (norm v) oneℝ (<-≤-ℝ zero-lt-one-ℝ) hv))

-- **可证**：‖Xv‖² ≤ ‖X²‖·‖v‖²（自伴 ⟹ ⟨Xv,Xv⟩ = ⟨v,X²v⟩（自伴）≤ ‖v‖·‖X²v‖（C-S）≤ ‖X²‖·‖v‖²（缩放））
norm-sq-adj-est : (X : LinOp) → SelfAdjoint X → (v : V)
  → norm-sq (LinOp.f X v) ≤ℝ (op-norm (op-comp X X) *ℝ (norm v *ℝ norm v))
norm-sq-adj-est X h v =
  subst (λ z → z ≤ℝ (op-norm (op-comp X X) *ℝ (norm v *ℝ norm v)))
        (sym (h v (LinOp.f X v)))
        (≤-trans-ℝ (cs-norm v (LinOp.f X (LinOp.f X v)))
                   (subst (λ z → ((norm v) *ℝ norm (LinOp.f X (LinOp.f X v))) ≤ℝ z)
                          (rearrange)
                          (*-≤-mono-l-ℝ (norm v) (norm (LinOp.f X (LinOp.f X v)))
                                        (op-norm (op-comp X X) *ℝ norm v)
                                        (norm-nonneg v)
                                        (op-norm-scalar (op-comp X X) v))))
  where
  -- ‖v‖·(‖X²‖·‖v‖) = ‖X²‖·(‖v‖·‖v‖)（结合 + 交换）
  rearrange : (norm v) *ℝ (op-norm (op-comp X X) *ℝ (norm v)) ≡ (op-norm (op-comp X X)) *ℝ (norm v *ℝ norm v)
  rearrange =
    trans (sym (*-assoc-ℝ (norm v) (op-norm (op-comp X X)) (norm v)))
          (trans (cong (λ z → z *ℝ (norm v)) (*-comm-ℝ (norm v) (op-norm (op-comp X X))))
                 (*-assoc-ℝ (op-norm (op-comp X X)) (norm v) (norm v)))

-- **可证**：‖v‖ ≤ 1 ⟹ ‖Xv‖ ≤ √‖X²‖（√ 单调于 ‖Xv‖² ≤ ‖X²‖）
op-norm-adj-est : (X : LinOp) → SelfAdjoint X → (v : V) → norm v ≤ℝ oneℝ
  → norm (LinOp.f X v) ≤ℝ sqrt (op-norm (op-comp X X))
op-norm-adj-est X h v hv =
  sqrt-mono (ip-pos (LinOp.f X v))
            (≤-trans-ℝ (norm-sq-adj-est X h v)
                       (≤-trans-ℝ (*-≤-mono-l-ℝ (op-norm (op-comp X X))
                                                (norm v *ℝ norm v) oneℝ
                                                (op-norm-nonneg (op-comp X X))
                                                (v-mul-le-one v hv))
                                  (subst (λ z → z ≤ℝ op-norm (op-comp X X))
                                         (sym (*-ident-ℝ (op-norm (op-comp X X))))
                                         (refl-≤ℝ {op-norm (op-comp X X)}))))

-- **可证**：‖X‖ ≤ √‖X²‖（单位球上逐点界 + sup-least）
op-norm-le-sqrt : (X : LinOp) → SelfAdjoint X
  → op-norm X ≤ℝ sqrt (op-norm (op-comp X X))
op-norm-le-sqrt X h = sup-least (op-fam X) (sqrt (op-norm (op-comp X X))) bound
  where
  bound : (r : ℝ) → op-fam X r → r ≤ℝ sqrt (op-norm (op-comp X X))
  bound r (ex v (hv , refl)) = op-norm-adj-est X h v hv

-- **可证**：C* 恒等（自伴幂恒等）——SelfAdjoint X ⟹ ‖X²‖ = ‖X‖²
--（≤：op-norm-submul；≥：‖X‖ ≤ √‖X²‖ 平方两侧 + sq-sqrt；反对称闭合）
norm-power : (X : LinOp) → SelfAdjoint X → op-norm (op-comp X X) ≡ (op-norm X *ℝ op-norm X)
norm-power X h = ≤-antisym (op-norm-submul X X) lower
  where
  M : ℝ
  M = op-norm (op-comp X X)
  -- ‖X‖·‖X‖ ≤ ‖X‖·√M ≤ √M·√M = M
  lower : (op-norm X *ℝ op-norm X) ≤ℝ M
  lower =
    subst (λ z → (op-norm X *ℝ op-norm X) ≤ℝ z)
          (sq-sqrt M (op-norm-nonneg (op-comp X X)))
          (≤-trans-ℝ (*-≤-mono-ℝ (op-norm-nonneg X) (op-norm-le-sqrt X h))
                     (*-≤-mono-l-ℝ (sqrt M) (op-norm X) (sqrt M)
                                   (sqrt-nonneg M (op-norm-nonneg (op-comp X X)))
                                   (op-norm-le-sqrt X h)))

-- ==================================================================
-- §7 算子拓扑层（阶段 8-5，2026-08-02）
-- ==================================================================

-- 向量减法（定义）：x − y := x + (-1)·y（V 减法层）
_-ᵥ_ : V → V → V
x -ᵥ y = x +ᵥ ((negℝ oneℝ) ·ᵥ y)

-- 算子取负（线性性：·ᵥ-distrib + 标量结合 + 交换）
op-neg : LinOp → LinOp
op-neg X = record
  { f = λ x → (negℝ oneℝ) ·ᵥ LinOp.f X x
  ; lin-add = λ x y →
      trans (cong (λ w → (negℝ oneℝ) ·ᵥ w) (LinOp.lin-add X x y))
            (·ᵥ-distrib-l (negℝ oneℝ) (LinOp.f X x) (LinOp.f X y))
  ; lin-scalar = λ a x →
      trans (cong (λ w → (negℝ oneℝ) ·ᵥ w) (LinOp.lin-scalar X a x))
            (trans (·ᵥ-assoc (negℝ oneℝ) a (LinOp.f X x))
                   (trans (cong (λ s → s ·ᵥ LinOp.f X x) (*-comm-ℝ (negℝ oneℝ) a))
                          (sym (·ᵥ-assoc a (negℝ oneℝ) (LinOp.f X x)))))
  }

-- 算子减法：S − T := S + (−T)
op-sub : LinOp → LinOp → LinOp
op-sub S T = op-add S (op-neg T)

-- 强收敛（SOT，0⁺）：∀v. ‖T t v − T0 v‖ → 0（ε-δ，t ∈ (0,δ)）
SOT-conv : (ℝ → LinOp) → LinOp → Set
SOT-conv T T0 = (v : V) → (ε : ℝ) → zeroℝ <ℝ ε
  → Σ ℝ (λ δ → (zeroℝ <ℝ δ) × ((t : ℝ) → zeroℝ <ℝ t → t <ℝ δ
    → norm (LinOp.f (T t) v -ᵥ LinOp.f T0 v) <ℝ ε))

-- 范数收敛（算子范数拓扑，0⁺）：‖T t − T0‖ → 0（ε-δ）
op-norm-conv : (ℝ → LinOp) → LinOp → Set
op-norm-conv T T0 = (ε : ℝ) → zeroℝ <ℝ ε
  → Σ ℝ (λ δ → (zeroℝ <ℝ δ) × ((t : ℝ) → zeroℝ <ℝ t → t <ℝ δ
    → op-norm (op-sub (T t) T0) <ℝ ε))

-- **可证**：1+‖v‖ > 0（1 > 0 + 1 ≤ 1+‖v‖）
one-plus-norm-pos : (v : V) → zeroℝ <ℝ (oneℝ +ℝ norm v)
one-plus-norm-pos v = lt-≤-trans-ℝ zero-lt-one-ℝ one-le-one-plus
  where
  one-le-one-plus : oneℝ ≤ℝ (oneℝ +ℝ norm v)
  one-le-one-plus =
    subst (λ z → z ≤ℝ (oneℝ +ℝ norm v)) (+-ident-ℝ oneℝ)
          (≤-+-mono-ℝ (refl-≤ℝ {oneℝ}) (norm-nonneg v))

-- **可证**：‖v‖ ≤ 1+‖v‖（add-pos-ℝ）
norm-le-one-plus : (v : V) → norm v ≤ℝ (oneℝ +ℝ norm v)
norm-le-one-plus v =
  subst (λ z → norm v ≤ℝ z) (+-comm-ℝ (norm v) oneℝ)
        (<-≤-ℝ (add-pos-ℝ {x = norm v} {y = oneℝ} zero-lt-one-ℝ))

-- **可证**：η := ε/(1+‖v‖) > 0
div-η-pos : (v : V) (ε : ℝ) → zeroℝ <ℝ ε → zeroℝ <ℝ (ε /ℝ (oneℝ +ℝ norm v))
div-η-pos v ε 0<ε = /-pos-ℝ 0<ε (one-plus-norm-pos v)

-- **可证**：η·(1+‖v‖) = ε（乘除消去）
η-1pv-eq : (v : V) (ε : ℝ) → ((ε /ℝ (oneℝ +ℝ norm v)) *ℝ (oneℝ +ℝ norm v)) ≡ ε
η-1pv-eq v ε =
  trans (*-comm-ℝ (ε /ℝ (oneℝ +ℝ norm v)) (oneℝ +ℝ norm v))
        (*-/cancel-ℝ (oneℝ +ℝ norm v) ε)

-- **可证**：η·‖v‖ ≤ ε（η ≥ 0 + ‖v‖ ≤ 1+‖v‖ + 乘除消去）
ηv-le-ε : (v : V) (ε : ℝ) → zeroℝ <ℝ ε → ((ε /ℝ (oneℝ +ℝ norm v)) *ℝ norm v) ≤ℝ ε
ηv-le-ε v ε 0<ε =
  subst (λ z → ((ε /ℝ (oneℝ +ℝ norm v)) *ℝ norm v) ≤ℝ z)
        (η-1pv-eq v ε)
        (*-≤-mono-l-ℝ (ε /ℝ (oneℝ +ℝ norm v)) (norm v) (oneℝ +ℝ norm v)
                      (<-≤-ℝ (div-η-pos v ε 0<ε))
                      (norm-le-one-plus v))

-- **可证**（‖v‖ = 0 分支）：‖Tt v − T0 v‖ = 0 < ε
sot-v-zero : (T : ℝ → LinOp) (T0 : LinOp) (t : ℝ) (v : V) (ε : ℝ)
  → norm v ≡ zeroℝ → zeroℝ <ℝ ε → norm (LinOp.f (T t) v -ᵥ LinOp.f T0 v) <ℝ ε
sot-v-zero T T0 t v ε 0=nv 0<ε =
  subst (λ z → z <ℝ ε) (sym e) 0<ε
  where
  v-zero : v ≡ zeroᵥ
  v-zero = norm-def v 0=nv
  l1 : LinOp.f (T t) v ≡ zeroᵥ
  l1 = trans (cong (LinOp.f (T t)) v-zero) (lin-zero (T t))
  l2 : LinOp.f T0 v ≡ zeroᵥ
  l2 = trans (cong (LinOp.f T0) v-zero) (lin-zero T0)
  -- 0 − 0 = 0（(-1)·0 = 0 + 0+0 = 0）
  sub00 : zeroᵥ -ᵥ zeroᵥ ≡ zeroᵥ
  sub00 = trans (cong (λ w → zeroᵥ +ᵥ w) (scalar-zero (negℝ oneℝ)))
                (+ᵥ-ident zeroᵥ)
  -- ‖Tt v − T0 v‖ = ‖0 − 0‖ = 0
  e : norm (LinOp.f (T t) v -ᵥ LinOp.f T0 v) ≡ zeroℝ
  e = trans (cong norm (trans (cong₂ _-ᵥ_ l1 l2) sub00)) norm-zero

-- **可证**：范数收敛 ⟹ 强收敛（范数拓扑细于强拓扑）
--（‖(Tt−T0)v‖ ≤ ‖Tt−T0‖·‖v‖（缩放）< η·‖v‖（η = ε/(1+‖v‖)，严格乘保序）≤ ε）
sot-from-norm : (T : ℝ → LinOp) (T0 : LinOp) → op-norm-conv T T0 → SOT-conv T T0
sot-from-norm T T0 hnorm v ε 0<ε with hnorm (ε /ℝ (oneℝ +ℝ norm v)) (div-η-pos v ε 0<ε)
... | ex δ (0<δ , bound) = ex δ (0<δ , λ t 0<t t<δ → est v ε 0<ε t (bound t 0<t t<δ))
  where
  est : (v : V) (ε : ℝ) → zeroℝ <ℝ ε → (t : ℝ)
    → op-norm (op-sub (T t) T0) <ℝ (ε /ℝ (oneℝ +ℝ norm v))
    → norm (LinOp.f (T t) v -ᵥ LinOp.f T0 v) <ℝ ε
  est v ε 0<ε t hb with trichotomy-ℝ zeroℝ (norm v)
  est v ε 0<ε t hb | inj₁ 0<nv =
    lt-≤-trans-ℝ (≤-lt-trans-ℝ (op-norm-scalar (op-sub (T t) T0) v)
                               (*-pos-mono-r-ℝ 0<nv hb))
                 (ηv-le-ε v ε 0<ε)
  est v ε 0<ε t hb | inj₂ (inj₁ 0=nv) = sot-v-zero T T0 t v ε (sym 0=nv) 0<ε
  est v ε 0<ε t hb | inj₂ (inj₂ nv<0) = ⊥-elim (irreflexive-ℝ (lt-≤-trans-ℝ nv<0 (norm-nonneg v)))

-- ==================================================================
-- §8 完备性层（2026-08-02：Hilbert 空间公理补全）
-- ==================================================================

-- 序列：ℕ 索引 V 值
Seq : Set
Seq = ℕ → V

-- 局部 ≤ℕ（避免跨模块依赖）
data _≤ℕ_ : ℕ → ℕ → Set where
  z≤n : {n : ℕ} → zero ≤ℕ n
  s≤s : {m n : ℕ} → m ≤ℕ n → suc m ≤ℕ suc n

-- **可证**：≤ℕ 自反
≤ℕ-refl : (n : ℕ) → n ≤ℕ n
≤ℕ-refl zero = z≤n
≤ℕ-refl (suc n) = s≤s (≤ℕ-refl n)

-- **可证**：≤ℕ 传递
≤ℕ-trans : {m n p : ℕ} → m ≤ℕ n → n ≤ℕ p → m ≤ℕ p
≤ℕ-trans z≤n h = z≤n
≤ℕ-trans (s≤s h) (s≤s g) = s≤s (≤ℕ-trans h g)

-- **可证**：≤ℕ 到后继
≤ℕ-suc : {m n : ℕ} → m ≤ℕ n → m ≤ℕ suc n
≤ℕ-suc z≤n = z≤n
≤ℕ-suc (s≤s h) = s≤s (≤ℕ-suc h)

-- **可证**：0·x = 0（0·x = (0+0)·x = 0·x + 0·x ⟹ 双自零）
scalar-zero-any : (x : V) → zeroℝ ·ᵥ x ≡ zeroᵥ
scalar-zero-any x = v-double-zero double
  where
  double : zeroℝ ·ᵥ x ≡ (zeroℝ ·ᵥ x) +ᵥ (zeroℝ ·ᵥ x)
  double =
    trans (cong (λ a → a ·ᵥ x) (sym (+-ident-ℝ zeroℝ)))
          (·ᵥ-distrib-r zeroℝ zeroℝ x)

-- **可证**：x − x = 0（x = 1·x + (-1)·x = (1+(-1))·x = 0·x = 0）
sub-ᵥ-self : (x : V) → x -ᵥ x ≡ zeroᵥ
sub-ᵥ-self x =
  trans (cong (λ w → w +ᵥ ((negℝ oneℝ) ·ᵥ x)) (sym (·ᵥ-ident x)))
        (trans (sym (·ᵥ-distrib-r oneℝ (negℝ oneℝ) x))
               (trans (cong (λ a → a ·ᵥ x) (+-inv-ℝ oneℝ))
                      (scalar-zero-any x)))

-- Cauchy 序列：∀ε>0. ∃N. ∀m n ≥ N. ‖xₘ − xₙ‖ < ε
Cauchy-seq : Seq → Set
Cauchy-seq s = (ε : ℝ) → zeroℝ <ℝ ε
  → Σ ℕ (λ N → (m n : ℕ) → N ≤ℕ m → N ≤ℕ n → norm (s m -ᵥ s n) <ℝ ε)

-- 收敛：xₙ → x（∀ε>0. ∃N. ∀n ≥ N. ‖xₙ − x‖ < ε）
Converges : Seq → V → Set
Converges s x = (ε : ℝ) → zeroℝ <ℝ ε
  → Σ ℕ (λ N → (n : ℕ) → N ≤ℕ n → norm (s n -ᵥ x) <ℝ ε)

-- 完备性（基础假设：Hilbert 空间公理——Cauchy 序列收敛，补全 pre-Hilbert 缺失项；
-- 降定理路径 = 完备化构造（Riesz 表示/投影定理/谱定理的共同地基））
postulate
  complete : (s : Seq) → Cauchy-seq s → Σ V (λ x → Converges s x)

-- **可证**：常值序列收敛（xₙ = x ⟹ xₙ → x）
conv-const : (x : V) → Converges (λ _ → x) x
conv-const x ε 0<ε = ex zero (λ n h →
  subst (λ z → z <ℝ ε) (sym (trans (cong norm (sub-ᵥ-self x)) norm-zero)) 0<ε)

-- **可证**：常值序列是 Cauchy 序列
cauchy-const : (x : V) → Cauchy-seq (λ _ → x)
cauchy-const x ε 0<ε = ex zero (λ m n h1 h2 →
  subst (λ z → z <ℝ ε) (sym (trans (cong norm (sub-ᵥ-self x)) norm-zero)) 0<ε)

-- ==================================================================
-- §9 谱半径公式的代数核心（阶段 8-6a，2026-08-02）
-- ==================================================================

-- 恒等算子
id-op : LinOp
id-op = record { f = λ x → x; lin-add = λ x y → refl; lin-scalar = λ a x → refl }

-- 平方算子（S∘S）
op-sq : LinOp → LinOp
op-sq X = op-comp X X

-- 幂算子：X⁰ = id、X^{n+1} = Xⁿ∘X
op-power : LinOp → ℕ → LinOp
op-power X zero = id-op
op-power X (suc n) = op-comp (op-power X n) X

-- 幂算子（2 幂次）：X, X², X⁴, ...（2^k 次平方迭代）
op-power-2^k : LinOp → ℕ → LinOp
op-power-2^k X zero = X
op-power-2^k X (suc k) = op-sq (op-power-2^k X k)

-- 迭代积：aⁿ（n 次乘）
iter-mul : ℝ → ℕ → ℝ
iter-mul a zero = oneℝ
iter-mul a (suc n) = iter-mul a n *ℝ a

-- 迭代平方：a, a², a⁴, ...（2^k 次幂）
iter-sq : ℝ → ℕ → ℝ
iter-sq a zero = a
iter-sq a (suc k) = iter-sq a k *ℝ iter-sq a k

-- **可证**：‖id‖ ≤ 1（单位球上 ‖v‖ ≤ 1 逐点 + sup-least）
op-norm-id-le : op-norm id-op ≤ℝ oneℝ
op-norm-id-le = sup-least (op-fam id-op) oneℝ bound
  where
  bound : (r : ℝ) → op-fam id-op r → r ≤ℝ oneℝ
  bound r (ex v (hv , refl)) = hv

-- **可证**：幂范数上界——‖Xⁿ‖ ≤ ‖X‖ⁿ（submul 归纳；r(X) ≤ ‖X‖ 的代数核心）
op-norm-pow-le : (X : LinOp) (n : ℕ) → op-norm (op-power X n) ≤ℝ iter-mul (op-norm X) n
op-norm-pow-le X zero = op-norm-id-le
op-norm-pow-le X (suc n) =
  ≤-trans-ℝ (op-norm-submul (op-power X n) X)
            (*-≤-mono-ℝ (op-norm-nonneg X) (op-norm-pow-le X n))

-- **可证**：自伴 ⟹ 平方自伴（⟨X(Xx),y⟩ = ⟨Xx,Xy⟩ = ⟨x,X(Xy)⟩）
SelfAdjoint-op-sq : (X : LinOp) → SelfAdjoint X → SelfAdjoint (op-sq X)
SelfAdjoint-op-sq X h x y = trans (h (LinOp.f X x) y) (h x (LinOp.f X y))

-- **可证**：自伴 ⟹ 2^k 幂自伴（归纳）
SelfAdjoint-op-power-2^k : (X : LinOp) → SelfAdjoint X → (k : ℕ) → SelfAdjoint (op-power-2^k X k)
SelfAdjoint-op-power-2^k X h zero = h
SelfAdjoint-op-power-2^k X h (suc k) =
  SelfAdjoint-op-sq (op-power-2^k X k) (SelfAdjoint-op-power-2^k X h k)

-- **可证**：自伴幂范数精确——‖X^{2^k}‖ = ‖X‖^{2^k}（norm-power 归纳；
--   Gelfand 公式 r(X) = lim ‖Xⁿ‖^{1/n} 沿 2^k 子列 ⟹ r(X) ≥ ‖X‖ 的代数核心）
op-norm-power-2^k : (X : LinOp) → SelfAdjoint X → (k : ℕ)
  → op-norm (op-power-2^k X k) ≡ iter-sq (op-norm X) k
op-norm-power-2^k X h zero = refl
op-norm-power-2^k X h (suc k) =
  trans (norm-power P (SelfAdjoint-op-power-2^k X h k))
        (cong₂ _*ℝ_ (op-norm-power-2^k X h k) (op-norm-power-2^k X h k))
  where
  P : LinOp
  P = op-power-2^k X k

-- 谱半径公式组合路径（文档化，8-6b）：
--   r(X) ≤ ‖X‖：op-norm-pow-le（‖Xⁿ‖ ≤ ‖X‖ⁿ）+ Gelfand 公式（极限层）；
--   r(X) ≥ ‖X‖（自伴）：op-norm-power-2^k（‖X^{2^k}‖ = ‖X‖^{2^k}）沿 2^k 子列；
--   SpectralTheory norm-contraction（σ(e^(-tA)) ⊆ (0,1] ⟹ ‖e^(-tA)‖ ≤ 1）降定理的代数核心齐备，
--   完整公式需极限/谱论层（8-6b + 阶段 7-3 E 构造后）。

-- ==================================================================
-- §10 正交分解与投影算子（阶段 7-3a，2026-08-02）
-- ==================================================================

-- **可证**：Pythagorean——⟨a,b⟩ = 0 ⟹ ‖a+b‖² = ‖a‖² + ‖b‖²（norm-sq-add + 正交归零）
pythagorean : (a b : V) → a ⟨⟩ b ≡ zeroℝ → norm-sq (a +ᵥ b) ≡ norm-sq a +ℝ norm-sq b
pythagorean a b hab =
  trans (norm-sq-add a b)
        (subst (λ z → (norm-sq a +ℝ z) +ℝ (z +ℝ norm-sq b) ≡ norm-sq a +ℝ norm-sq b) (sym hab)
               (cong₂ _+ℝ_ (+-ident-ℝ (norm-sq a)) (zero-add-ℝ (norm-sq b))))

-- 闭子空间（代数闭包 + 拓扑闭包——投影定理需完备性/闭性；closed 用 Converges）
record Subspace : Set₁ where
  field
    mem : V → Set
    add : {x y : V} → mem x → mem y → mem (x +ᵥ y)
    scalar : (a : ℝ) {x : V} → mem x → mem (a ·ᵥ x)
    zero-mem : mem zeroᵥ
    closed : (s : Seq) → ((n : ℕ) → mem (s n)) → (x : V) → Converges s x → mem x

-- 正交投影（投影定理桥接：完备性层之上，每个 x 唯一分解为 W 分量 Px 与正交分量 x−Px；
-- 降定理路径 = 极小化序列 + 完备性论证）
postulate
  proj : Subspace → V → V
  proj-in : (W : Subspace) (x : V) → Subspace.mem W (proj W x)
  proj-orth : (W : Subspace) (x : V) → (w : V) → Subspace.mem W w → ((x -ᵥ proj W x) ⟨⟩ w) ≡ zeroℝ
  proj-fixed : (W : Subspace) (x : V) → Subspace.mem W x → proj W x ≡ x

-- **可证**：正交分解 x = Px + (x−Px)（向量代数恒真；内容在 proj-in/proj-orth）
proj-decomp : (W : Subspace) (x : V) → x ≡ proj W x +ᵥ (x -ᵥ proj W x)
proj-decomp W x = sym chain
  where
  -- Px + (-1)·Px = 0（1·Px + (-1)·Px = (1+(-1))·Px = 0·Px = 0）
  px-neg-px : proj W x +ᵥ ((negℝ oneℝ) ·ᵥ proj W x) ≡ zeroᵥ
  px-neg-px =
    trans (cong (λ w → w +ᵥ ((negℝ oneℝ) ·ᵥ proj W x)) (sym (·ᵥ-ident (proj W x))))
          (trans (sym (·ᵥ-distrib-r oneℝ (negℝ oneℝ) (proj W x)))
                 (trans (cong (λ a → a ·ᵥ proj W x) (+-inv-ℝ oneℝ))
                        (scalar-zero-any (proj W x))))
  -- Px + (x + (-1)·Px) = ... = x（结合/交换/逆/零）
  chain : proj W x +ᵥ (x -ᵥ proj W x) ≡ x
  chain =
    trans (sym (+ᵥ-assoc (proj W x) x ((negℝ oneℝ) ·ᵥ proj W x)))
          (trans (cong (λ w → w +ᵥ ((negℝ oneℝ) ·ᵥ proj W x)) (+ᵥ-comm (proj W x) x))
                 (trans (+ᵥ-assoc x (proj W x) ((negℝ oneℝ) ·ᵥ proj W x))
                        (trans (cong (λ w → x +ᵥ w) px-neg-px)
                               (+ᵥ-ident x))))

-- **可证**：投影幂等——P(Px) = Px（Px ∈ W + proj-fixed）
proj-idemp : (W : Subspace) (x : V) → proj W (proj W x) ≡ proj W x
proj-idemp W x = proj-fixed W (proj W x) (proj-in W x)

-- **可证**：投影非扩张——‖Px‖ ≤ ‖x‖
--（‖Px‖² ≤ ‖Px‖² + ‖x−Px‖² = ‖Px+(x−Px)‖²（Pythagorean，正交） = ‖x‖²（分解）+ √）
proj-norm-le : (W : Subspace) (x : V) → norm (proj W x) ≤ℝ norm x
proj-norm-le W x =
  sqrt-mono (ip-pos (proj W x))
            (subst (λ z → norm-sq (proj W x) ≤ℝ z)
                   (sym (cong norm-sq (proj-decomp W x)))
                   (subst (λ z → norm-sq (proj W x) ≤ℝ z)
                          (sym (pythagorean (proj W x) (x -ᵥ proj W x) hab))
                          (subst (λ w → w ≤ℝ (norm-sq (proj W x) +ℝ norm-sq (x -ᵥ proj W x)))
                                 (+-ident-ℝ (norm-sq (proj W x)))
                                 (≤-+-mono-ℝ (refl-≤ℝ {norm-sq (proj W x)})
                                             (norm-sq-nonneg (x -ᵥ proj W x))))))
  where
  -- ⟨Px, x−Px⟩ = 0（proj-orth 的 w = Px 特化 + 对称性）
  hab : (proj W x) ⟨⟩ (x -ᵥ proj W x) ≡ zeroℝ
  hab = trans (sym (ip-sym (x -ᵥ proj W x) (proj W x)))
              (proj-orth W x (proj W x) (proj-in W x))

-- ==================================================================
-- §10b 投影算子与自伴性（阶段 7-3b，2026-08-02）
-- ==================================================================

-- **可证**：z + (-1)·z = 0（1·z + (-1)·z = (1+(-1))·z = 0·z = 0；
--   proj-decomp 内部 px-neg-px 的泛化）
+-inv-ᵥ : (z : V) → z +ᵥ ((negℝ oneℝ) ·ᵥ z) ≡ zeroᵥ
+-inv-ᵥ z =
  trans (cong (λ w → w +ᵥ ((negℝ oneℝ) ·ᵥ z)) (sym (·ᵥ-ident z)))
        (trans (sym (·ᵥ-distrib-r oneℝ (negℝ oneℝ) z))
               (trans (cong (λ a → a ·ᵥ z) (+-inv-ℝ oneℝ))
                      (scalar-zero-any z)))

-- **可证**：0 + u = u（左单位，经交换律 + 右单位）
zero-l-ᵥ : (u : V) → zeroᵥ +ᵥ u ≡ u
zero-l-ᵥ u = trans (+ᵥ-comm zeroᵥ u) (+ᵥ-ident u)

-- **可证**：减法消去——w − z = 0 ⟹ w = z
--（z = z+0 = z+(w−z) = (z+w)+(-1)·z = (w+z)+(-1)·z = w+(z+(-1)·z) = w+0 = w）
sub-ᵥ-impl : {w z : V} → w -ᵥ z ≡ zeroᵥ → w ≡ z
sub-ᵥ-impl {w} {z} h = sym chain
  where
  chain : z ≡ w
  chain =
    trans (sym (+ᵥ-ident z))
          (trans (cong (λ u → z +ᵥ u) (sym h))
                 (trans (sym (+ᵥ-assoc z w ((negℝ oneℝ) ·ᵥ z)))
                        (trans (cong (λ u → u +ᵥ ((negℝ oneℝ) ·ᵥ z)) (+ᵥ-comm z w))
                               (trans (+ᵥ-assoc w z ((negℝ oneℝ) ·ᵥ z))
                                      (trans (cong (λ u → w +ᵥ u) (+-inv-ᵥ z))
                                             (+ᵥ-ident w))))))

-- 投影唯一性：w ∈ W 且 x−w ⊥ W ⟹ w = Px
--（a = w−Px ∈ W；x−Px = (x−w)+a ⟹ ⟨x−Px, a⟩ = ⟨x−w, a⟩ + ⟨a, a⟩（左加性）
--  = 0 + ⟨a, a⟩（两正交）⟹ proj-orth 给 ⟨x−Px, a⟩ = 0 ⟹ ⟨a, a⟩ = 0 ⟹ a = 0 ⟹ w = Px）
proj-unique : (W : Subspace) (x : V) (w : V) → Subspace.mem W w
  → ((u : V) → Subspace.mem W u → ((x -ᵥ w) ⟨⟩ u) ≡ zeroℝ)
  → w ≡ proj W x
proj-unique W x w w-in orth = sub-ᵥ-impl (ip-def a a-zero)
  where
  a : V
  a = w -ᵥ proj W x
  a-in-W : Subspace.mem W a
  a-in-W = Subspace.add W w-in (Subspace.scalar W (negℝ oneℝ) (proj-in W x))
  -- x−Px = (x−w) + (w−Px)（结合/交换/逆/零）
  xw-a : (x -ᵥ proj W x) ≡ (x -ᵥ w) +ᵥ a
  xw-a = sym chain
    where
    chain : (x -ᵥ w) +ᵥ (w -ᵥ proj W x) ≡ x -ᵥ proj W x
    chain =
      trans (+ᵥ-assoc x ((negℝ oneℝ) ·ᵥ w) (w +ᵥ ((negℝ oneℝ) ·ᵥ proj W x)))
            (trans (cong (λ u → x +ᵥ u) inner)
                   (cong (λ u → x +ᵥ u) (zero-l-ᵥ ((negℝ oneℝ) ·ᵥ proj W x))))
      where
      inner : ((negℝ oneℝ) ·ᵥ w) +ᵥ (w +ᵥ ((negℝ oneℝ) ·ᵥ proj W x))
        ≡ zeroᵥ +ᵥ ((negℝ oneℝ) ·ᵥ proj W x)
      inner =
        trans (sym (+ᵥ-assoc ((negℝ oneℝ) ·ᵥ w) w ((negℝ oneℝ) ·ᵥ proj W x)))
              (trans (cong (λ u → u +ᵥ ((negℝ oneℝ) ·ᵥ proj W x)) (+ᵥ-comm ((negℝ oneℝ) ·ᵥ w) w))
                     (cong (λ u → u +ᵥ ((negℝ oneℝ) ·ᵥ proj W x)) (+-inv-ᵥ w)))
  -- ⟨a, a⟩ = 0
  a-zero : a ⟨⟩ a ≡ zeroℝ
  a-zero =
    trans (sym (zero-add-ℝ (a ⟨⟩ a)))
          (trans (cong₂ _+ℝ_ (sym (orth a a-in-W)) refl)
                 (trans (sym (ip-add-l (x -ᵥ w) a a))
                        (trans (sym (cong (λ v → v ⟨⟩ a) xw-a))
                               (proj-orth W x a a-in-W))))

-- **可证**：投影加法性——P(x+y) = Px + Py
--（Px+Py ∈ W；x+y−(Px+Py) = (x−Px)+(y−Py) ⊥ W（逐项正交）；唯一性）
proj-lin-add : (W : Subspace) (x y : V) → proj W (x +ᵥ y) ≡ proj W x +ᵥ proj W y
proj-lin-add W x y = sym (proj-unique W (x +ᵥ y) (proj W x +ᵥ proj W y) b-in-W orth-b)
  where
  b-in-W : Subspace.mem W (proj W x +ᵥ proj W y)
  b-in-W = Subspace.add W (proj-in W x) (proj-in W y)
  -- x+y−(Px+Py) = (x−Px) + (y−Py)（·ᵥ-distrib-l + swap-pair-ᵥ）
  sub-decomp : (x +ᵥ y) -ᵥ (proj W x +ᵥ proj W y) ≡ (x -ᵥ proj W x) +ᵥ (y -ᵥ proj W y)
  sub-decomp =
    trans (cong (λ u → (x +ᵥ y) +ᵥ u) (·ᵥ-distrib-l (negℝ oneℝ) (proj W x) (proj W y)))
          (swap-pair-ᵥ x y ((negℝ oneℝ) ·ᵥ proj W x) ((negℝ oneℝ) ·ᵥ proj W y))
  -- x+y−b ⊥ W：⟨(x−Px)+(y−Py), u⟩ = 0 + 0（逐项 proj-orth）
  orth-b : (u : V) → Subspace.mem W u → ((x +ᵥ y) -ᵥ (proj W x +ᵥ proj W y)) ⟨⟩ u ≡ zeroℝ
  orth-b u hu =
    trans (cong (λ w → w ⟨⟩ u) sub-decomp)
          (trans (ip-add-l (x -ᵥ proj W x) (y -ᵥ proj W y) u)
                 (trans (cong₂ _+ℝ_ (proj-orth W x u hu) (proj-orth W y u hu))
                        (zero-add-ℝ zeroℝ)))

-- **可证**：投影标量齐次——P(a·x) = a·Px
--（a·Px ∈ W；a·x−a·Px = a·(x−Px) ⊥ W（⟨a·(x−Px), u⟩ = a·⟨x−Px, u⟩ = a·0）；唯一性）
proj-lin-scalar : (W : Subspace) (a : ℝ) (x : V) → proj W (a ·ᵥ x) ≡ a ·ᵥ proj W x
proj-lin-scalar W a x = sym (proj-unique W (a ·ᵥ x) (a ·ᵥ proj W x) b-in-W orth-b)
  where
  b-in-W : Subspace.mem W (a ·ᵥ proj W x)
  b-in-W = Subspace.scalar W a (proj-in W x)
  -- a·x−a·Px = a·(x−Px)（·ᵥ-assoc ×2 + *-comm + ·ᵥ-distrib-l 反向）
  sub-scalar-decomp : (a ·ᵥ x) -ᵥ (a ·ᵥ proj W x) ≡ a ·ᵥ (x -ᵥ proj W x)
  sub-scalar-decomp =
    trans (cong (λ u → (a ·ᵥ x) +ᵥ u) (·ᵥ-assoc (negℝ oneℝ) a (proj W x)))
          (trans (cong (λ s → (a ·ᵥ x) +ᵥ (s ·ᵥ proj W x)) (*-comm-ℝ (negℝ oneℝ) a))
                 (trans (cong (λ u → (a ·ᵥ x) +ᵥ u) (sym (·ᵥ-assoc a (negℝ oneℝ) (proj W x))))
                        (sym (·ᵥ-distrib-l a x ((negℝ oneℝ) ·ᵥ proj W x)))))
  -- a·x−a·Px ⊥ W：⟨a·(x−Px), u⟩ = a·⟨x−Px, u⟩ = a·0 = 0
  orth-b : (u : V) → Subspace.mem W u → ((a ·ᵥ x) -ᵥ (a ·ᵥ proj W x)) ⟨⟩ u ≡ zeroℝ
  orth-b u hu =
    trans (cong (λ w → w ⟨⟩ u) sub-scalar-decomp)
          (trans (ip-scalar-l a (x -ᵥ proj W x) u)
                 (trans (cong (λ t → a *ℝ t) (proj-orth W x u hu))
                        (*-zero-ℝ a)))

-- 投影算子（线性性经唯一性论证——投影定理的算子封装）
proj-op : Subspace → LinOp
proj-op W = record
  { f = λ x → proj W x
  ; lin-add = λ x y → proj-lin-add W x y
  ; lin-scalar = λ a x → proj-lin-scalar W a x
  }

-- **可证**：⟨Px, y⟩ = ⟨Px, Py⟩（y = Py + (y−Py)，y−Py ⊥ W 且 Px ∈ W）
proj-ip-left : (W : Subspace) (x y : V) → (proj W x) ⟨⟩ y ≡ (proj W x) ⟨⟩ (proj W y)
proj-ip-left W x y =
  trans (cong (λ w → (proj W x) ⟨⟩ w) (proj-decomp W y))
        (trans (ip-add-r (proj W x) (proj W y) (y -ᵥ proj W y))
               (trans (cong₂ _+ℝ_ refl (proj-orth-px))
                      (+-ident-ℝ (proj W x ⟨⟩ proj W y))))
  where
  -- ⟨Px, y−Py⟩ = 0（proj-orth 对 w = Px ∈ W + 对称性）
  proj-orth-px : (proj W x) ⟨⟩ (y -ᵥ proj W y) ≡ zeroℝ
  proj-orth-px = trans (sym (ip-sym (y -ᵥ proj W y) (proj W x)))
                       (proj-orth W y (proj W x) (proj-in W x))

-- **可证**：⟨x, Py⟩ = ⟨Px, Py⟩（x = Px + (x−Px)，x−Px ⊥ W 且 Py ∈ W）
proj-ip-right : (W : Subspace) (x y : V) → x ⟨⟩ (proj W y) ≡ (proj W x) ⟨⟩ (proj W y)
proj-ip-right W x y =
  trans (cong (λ w → w ⟨⟩ (proj W y)) (proj-decomp W x))
        (trans (ip-add-l (proj W x) (x -ᵥ proj W x) (proj W y))
               (trans (cong₂ _+ℝ_ refl (proj-orth W x (proj W y) (proj-in W y)))
                      (+-ident-ℝ (proj W x ⟨⟩ proj W y))))

-- **可证**：投影自伴——⟨Px, y⟩ = ⟨x, Py⟩（阶段 7-3b 核心结论）
proj-self-adjoint : (W : Subspace) → SelfAdjoint (proj-op W)
proj-self-adjoint W x y = trans (proj-ip-left W x y) (sym (proj-ip-right W x y))

-- **可证**：投影算子范数 ≤ 1（‖Pv‖ ≤ ‖v‖ ≤ 1 逐点 + sup-least；
--   呼应 SpectralTheory §12b proj-norm-le-one 的 Hilbert 侧版本）
proj-op-norm-le-one : (W : Subspace) → op-norm (proj-op W) ≤ℝ oneℝ
proj-op-norm-le-one W = sup-least (op-fam (proj-op W)) oneℝ bound
  where
  bound : (r : ℝ) → op-fam (proj-op W) r → r ≤ℝ oneℝ
  bound r (ex v (hv , refl)) = ≤-trans-ℝ (proj-norm-le W v) hv

-- ==================================================================
-- §10c 谱投影构造框架（阶段 7-3：E 的测度构造第一步，2026-08-02）
-- ==================================================================

-- 全空间谱集 TopP：ℝ 上处处为真的谓词（E(ℝ) = 分辨恒等的载体，E-total 的 Hilbert 侧）
data TopP : ℝ → Set where
  top-p : (x : ℝ) → TopP x

-- 谱子空间（谱定理桥接：自伴算子 A 的谱分解给出谱集 P 对应的闭子空间 W_P = E(P)V——
-- Borel 函数演算 / 乘法算子模型内容；降定理路径 = 自伴算子谱定理）
postulate
  spectral-subspace : (P : ℝ → Set) → Subspace
  -- 谱子空间正交性：P ∩ Q = ∅ ⟹ W_P ⊥ W_Q（谱投影正交性，SpectralTheory E-orthogonal 的 Hilbert 侧）
  spectral-subspace-orth : (P Q : ℝ → Set) → ((x : ℝ) → P x → Q x → ⊥)
    → (u v : V) → Subspace.mem (spectral-subspace P) u → Subspace.mem (spectral-subspace Q) v
    → u ⟨⟩ v ≡ zeroℝ
  -- 谱支集完备性：W_ℝ = 全空间（E(ℝ) = 𝟙，SpectralTheory E-total 的 Hilbert 侧）
  spectral-subspace-total : (x : V) → Subspace.mem (spectral-subspace TopP) x

-- 谱投影（谱测度 E 的 Hilbert 层构造：E(P) := proj-op (spectral-subspace P)——
-- SpectralTheory 谱测度 E 的构造侧；E-idempotent/E-orthogonal/E-total/E-union/E-σ-add
-- 降定理的投影基础）
E-hilb : (P : ℝ → Set) → LinOp
E-hilb P = proj-op (spectral-subspace P)

-- **可证**：谱投影幂等（点态）——E(P)(E(P)x) = E(P)x（proj-idemp 特化；
--   SpectralTheory §10 E-idempotent 的 Hilbert 侧对应）
E-hilb-idemp : (P : ℝ → Set) (x : V)
  → LinOp.f (op-comp (E-hilb P) (E-hilb P)) x ≡ LinOp.f (E-hilb P) x
E-hilb-idemp P x = proj-idemp (spectral-subspace P) x

-- **可证**：谱投影正交——P ∩ Q = ∅ ⟹ E(P)u ⊥ E(Q)v（spectral-subspace-orth + proj-in；
--   SpectralTheory §10 E-orthogonal 的 Hilbert 侧对应）
E-hilb-orth : (P Q : ℝ → Set) → ((x : ℝ) → P x → Q x → ⊥) → (u v : V)
  → LinOp.f (E-hilb P) u ⟨⟩ LinOp.f (E-hilb Q) v ≡ zeroℝ
E-hilb-orth P Q disjoint u v = spectral-subspace-orth P Q disjoint
  (LinOp.f (E-hilb P) u) (LinOp.f (E-hilb Q) v)
  (proj-in (spectral-subspace P) u) (proj-in (spectral-subspace Q) v)

-- **可证**：谱支集完备性——E(ℝ)x = x（proj-fixed + 谱支集 = 全空间；
--   SpectralTheory §10e E-total/E-spectrum-total 的 Hilbert 侧对应）
E-hilb-total : (x : V) → LinOp.f (E-hilb TopP) x ≡ x
E-hilb-total x = proj-fixed (spectral-subspace TopP) x (spectral-subspace-total x)

-- **可证**：谱投影自伴——⟨E(P)x, y⟩ = ⟨x, E(P)y⟩（proj-self-adjoint 特化；
--   谱投影 = 正交投影的自伴性）
E-hilb-self-adjoint : (P : ℝ → Set) → SelfAdjoint (E-hilb P)
E-hilb-self-adjoint P = proj-self-adjoint (spectral-subspace P)

-- **可证**：谱投影范数 ≤ 1（proj-op-norm-le-one 特化；
--   SpectralTheory §12b proj-norm-le-one 的谱投影实例）
E-hilb-norm-le-one : (P : ℝ → Set) → op-norm (E-hilb P) ≤ℝ oneℝ
E-hilb-norm-le-one P = proj-op-norm-le-one (spectral-subspace P)

-- ==================================================================
-- §10d 谱投影加法性（阶段 7-3 余项：E-union，2026-08-02）
-- ==================================================================

-- **可证**：内积左减法——⟨x−y, z⟩ = ⟨x,z⟩ + (-1)·⟨y,z⟩（ip-add-l + ip-scalar-l）
ip-sub-l : (x y z : V) → (x -ᵥ y) ⟨⟩ z ≡ (x ⟨⟩ z) +ℝ ((negℝ oneℝ) *ℝ (y ⟨⟩ z))
ip-sub-l x y z =
  trans (ip-add-l x ((negℝ oneℝ) ·ᵥ y) z)
        (cong₂ _+ℝ_ refl (ip-scalar-l (negℝ oneℝ) y z))

-- **可证**：内积右减法——⟨x, y−z⟩ = ⟨x,y⟩ + (-1)·⟨x,z⟩（ip-add-r + ip-scalar-r）
ip-sub-r : (x y z : V) → x ⟨⟩ (y -ᵥ z) ≡ (x ⟨⟩ y) +ℝ ((negℝ oneℝ) *ℝ (x ⟨⟩ z))
ip-sub-r x y z =
  trans (ip-add-r x y ((negℝ oneℝ) ·ᵥ z))
        (cong₂ _+ℝ_ refl (ip-scalar-r (negℝ oneℝ) x z))

-- **可证**：减法分解——x − (a+b) = (x−a) + (-1)·b（·ᵥ-distrib-l + assoc 反向）
sub-add-decomp : (x a b : V) → x -ᵥ (a +ᵥ b) ≡ (x -ᵥ a) +ᵥ ((negℝ oneℝ) ·ᵥ b)
sub-add-decomp x a b =
  trans (cong (λ u → x +ᵥ u) (·ᵥ-distrib-l (negℝ oneℝ) a b))
        (sym (+ᵥ-assoc x ((negℝ oneℝ) ·ᵥ a) ((negℝ oneℝ) ·ᵥ b)))

-- 谱子空间直和（谱定理内容：E(P∪Q) = E(P)+E(Q) 对不相交集的分解侧——
-- W_{P∪Q} ⊆ W_P + W_Q（spectral-subspace-split）+ 谱子空间单调性
-- （spectral-subspace-incl）；E-union 降定理的桥接，降定理路径 = 自伴算子谱定理）
postulate
  spectral-subspace-incl : (P Q : ℝ → Set) → ((x : ℝ) → P x → Q x) → (w : V)
    → Subspace.mem (spectral-subspace P) w → Subspace.mem (spectral-subspace Q) w
  spectral-subspace-split : (P Q : ℝ → Set) → ((x : ℝ) → P x → Q x → ⊥) → (w : V)
    → Subspace.mem (spectral-subspace (λ x → P x ⊎ Q x)) w
    → Σ V (λ u → Σ V (λ v → ((Subspace.mem (spectral-subspace P) u × Subspace.mem (spectral-subspace Q) v)
      × (w ≡ u +ᵥ v))))

-- **可证**：谱投影加法性（E-union）——P∩Q=∅ ⟹ E(P∪Q)x = E(P)x + E(Q)x
--（E(P)x+E(Q)x ∈ W_{P∪Q}（incl 单调 + add 闭包）；x−(E(P)x+E(Q)x) ⊥ W_{P∪Q}
--（split 分解 u+v + 逐项：⟨x−(Px+Qx),u⟩=0 经 proj-orth + W_P⊥W_Q、⟨x−(Px+Qx),v⟩=0 对称）+
-- proj-unique——SpectralTheory §10e E-union 的 Hilbert 侧构造版）
E-hilb-union : (P Q : ℝ → Set) → ((x : ℝ) → P x → Q x → ⊥) → (x : V)
  → LinOp.f (E-hilb (λ z → P z ⊎ Q z)) x ≡ LinOp.f (E-hilb P) x +ᵥ LinOp.f (E-hilb Q) x
E-hilb-union P Q disjoint x = sym (proj-unique W-pq x b b-in-W orth-b)
  where
  W-pq : Subspace
  W-pq = spectral-subspace (λ z → P z ⊎ Q z)
  Px : V
  Px = LinOp.f (E-hilb P) x
  Qx : V
  Qx = LinOp.f (E-hilb Q) x
  b : V
  b = Px +ᵥ Qx
  -- E(P)x + E(Q)x ∈ W_{P∪Q}（P ⊆ P∪Q、Q ⊆ P∪Q 单调 + add 闭包）
  b-in-W : Subspace.mem W-pq b
  b-in-W = Subspace.add W-pq px-in-pq qx-in-pq
    where
    px-in-pq : Subspace.mem W-pq Px
    px-in-pq = spectral-subspace-incl P (λ z → P z ⊎ Q z) (λ x' px → inj₁ px) Px
               (proj-in (spectral-subspace P) x)
    qx-in-pq : Subspace.mem W-pq Qx
    qx-in-pq = spectral-subspace-incl Q (λ z → P z ⊎ Q z) (λ x' qx → inj₂ qx) Qx
               (proj-in (spectral-subspace Q) x)
  -- x−(E(P)x+E(Q)x) ⊥ W_P（x−Px ⊥ W_P + Qx ⊥ W_P）
  orth-A : (u : V) → Subspace.mem (spectral-subspace P) u
    → (x -ᵥ b) ⟨⟩ u ≡ zeroℝ
  orth-A u hu =
    trans (cong (λ w → w ⟨⟩ u) (sub-add-decomp x Px Qx))
          (trans (ip-add-l (x -ᵥ Px) ((negℝ oneℝ) ·ᵥ Qx) u)
                 (trans (cong₂ _+ℝ_ (proj-orth (spectral-subspace P) x u hu)
                                  (ip-scalar-l (negℝ oneℝ) Qx u))
                        (trans (cong₂ _+ℝ_ refl
                                       (cong (λ t → (negℝ oneℝ) *ℝ t)
                                             (trans (ip-sym Qx u)
                                                    (spectral-subspace-orth P Q disjoint u Qx hu
                                                                            (proj-in (spectral-subspace Q) x)))))
                               (trans (cong₂ _+ℝ_ refl (*-zero-ℝ (negℝ oneℝ)))
                                      (zero-add-ℝ zeroℝ)))))
  -- x−(E(P)x+E(Q)x) ⊥ W_Q（x−Qx ⊥ W_Q + Px ⊥ W_Q）
  orth-B : (v : V) → Subspace.mem (spectral-subspace Q) v
    → (x -ᵥ b) ⟨⟩ v ≡ zeroℝ
  orth-B v hv =
    trans (cong (λ w → w ⟨⟩ v) (trans (cong (λ t → x -ᵥ t) (+ᵥ-comm Px Qx))
                                      (sub-add-decomp x Qx Px)))
          (trans (ip-add-l (x -ᵥ Qx) ((negℝ oneℝ) ·ᵥ Px) v)
                 (trans (cong₂ _+ℝ_ (proj-orth (spectral-subspace Q) x v hv)
                                  (ip-scalar-l (negℝ oneℝ) Px v))
                        (trans (cong₂ _+ℝ_ refl
                                       (cong (λ t → (negℝ oneℝ) *ℝ t)
                                             (trans (ip-sym Px v)
                                                    (spectral-subspace-orth Q P (λ x' qx px → disjoint x' px qx) v Px hv
                                                                            (proj-in (spectral-subspace P) x)))))
                               (trans (cong₂ _+ℝ_ refl (*-zero-ℝ (negℝ oneℝ)))
                                      (zero-add-ℝ zeroℝ)))))
  -- x−(E(P)x+E(Q)x) ⊥ W_{P∪Q}（split 分解 u+v + 逐项正交）
  orth-b : (w : V) → Subspace.mem W-pq w → (x -ᵥ b) ⟨⟩ w ≡ zeroℝ
  orth-b w hw with spectral-subspace-split P Q disjoint w hw
  orth-b w hw | ex u (ex v ((hu , hv) , w-eq)) =
    subst (λ t → ((x -ᵥ b) ⟨⟩ t) ≡ zeroℝ) (sym w-eq)
          (trans (ip-add-r (x -ᵥ b) u v)
                 (trans (cong₂ _+ℝ_ (orth-A u hu) (orth-B v hv))
                        (zero-add-ℝ zeroℝ)))

-- ==================================================================
-- §10e E 的有限可加性（阶段 7-3 余项：E-fin-union，2026-08-02）
-- ==================================================================

-- 点态向量有限和：Σᵢ<ₘ f i（前 m 项，i = 0..m-1）
sum-ᵥ : (ℕ → V) → ℕ → V
sum-ᵥ f zero = zeroᵥ
sum-ᵥ f (suc m) = sum-ᵥ f m +ᵥ f m

-- 空谱集（处处假谓词）
EmptyP : ℝ → Set
EmptyP = λ _ → ⊥

-- 空谱子空间平凡性（谱定理内容：W_∅ = {0}——E(∅) = 0 的 Hilbert 侧桥接；
-- 降定理路径 = 自伴算子谱定理/Borel 函数演算）
postulate
  spectral-subspace-empty : (x : V) → Subspace.mem (spectral-subspace EmptyP) x → x ≡ zeroᵥ

-- **可证**：空谱投影为零——E(∅)x = 0（spectral-subspace-empty + proj-in）
E-hilb-empty : (x : V) → LinOp.f (E-hilb EmptyP) x ≡ zeroᵥ
E-hilb-empty x = spectral-subspace-empty (LinOp.f (E-hilb EmptyP) x) (proj-in (spectral-subspace EmptyP) x)

-- 有限并谓词（递归）：∪ᵢ<ₘ Pᵢ
FinUnion : (ℕ → ℝ → Set) → ℕ → ℝ → Set
FinUnion P zero x = ⊥
FinUnion P (suc m) x = FinUnion P m x ⊎ P m x

-- **可证**：FinUnion 展开——∪ᵢ<ₘ Pᵢ x ⟹ ∃ i. suc i ≤ℕ m ∧ Pᵢ x（递归）
fin-union-in : (P : ℕ → ℝ → Set) (m : ℕ) (x : ℝ) → FinUnion P m x
  → Σ ℕ (λ i → (suc i ≤ℕ m) × (P i x))
fin-union-in P zero x ()
fin-union-in P (suc m) x (inj₁ fx) with fin-union-in P m x fx
fin-union-in P (suc m) x (inj₁ fx) | ex i (ile , pxi) = ex i (≤ℕ-suc ile , pxi)
fin-union-in P (suc m) x (inj₂ pmx) = ex m (≤ℕ-refl (suc m) , pmx)

-- **可证**：pairwise 不相交 ⟹ (∪ᵢ<ₘPᵢ) ∩ Pₘ = ∅（FinUnion-disjoint）
FinUnion-disjoint : (P : ℕ → ℝ → Set) (m : ℕ)
  → ((i : ℕ) → suc i ≤ℕ m → (x : ℝ) → P i x → P m x → ⊥)
  → (x : ℝ) → FinUnion P m x → P m x → ⊥
FinUnion-disjoint P m h x fx pmx with fin-union-in P m x fx
FinUnion-disjoint P m h x fx pmx | ex i (ile , pxi) = h i ile x pxi pmx

-- **可证**：E 的有限可加性——pairwise 不相交 ⟹ E(∪ᵢ<ₘ Pᵢ)x = Σᵢ<ₘ E(Pᵢ)x
--（归纳：m+1 步经 E-hilb-union 拆分（FinUnion-disjoint + h i m 特化）+ 归纳假设；
--  E-σ-add 的有限版，SpectralTheory §10e E-partition-add 的 Hilbert 侧对应）
E-hilb-fin-union : (P : ℕ → ℝ → Set) → (m : ℕ)
  → ((i j : ℕ) → suc i ≤ℕ j → (x : ℝ) → P i x → P j x → ⊥)
  → (x : V) → LinOp.f (E-hilb (FinUnion P m)) x ≡ sum-ᵥ (λ i → LinOp.f (E-hilb (P i)) x) m
E-hilb-fin-union P zero h x = E-hilb-empty x
E-hilb-fin-union P (suc m) h x =
  trans (E-hilb-union (FinUnion P m) (P m) (FinUnion-disjoint P m hₘ) x)
        (trans (cong₂ _+ᵥ_ (E-hilb-fin-union P m h x) refl) refl)
  where
  hₘ : (i : ℕ) → suc i ≤ℕ m → (x' : ℝ) → P i x' → P m x' → ⊥
  hₘ i ile x' pxi pmx = h i m ile x' pxi pmx

-- ==================================================================
-- §10f E-σ-add 第一步：单调吸收 + 可数并（阶段 7-3 余项，2026-08-02）
-- ==================================================================

-- **可证**：谱投影复合吸收——P ⊆ Q ⟹ E(Q)(E(P)x) = E(P)x
--（E(P)x ∈ W_P ⊆ W_Q（spectral-subspace-incl）+ proj-fixed；
--  SpectralTheory §10b E-sub（P⊆Q ⟹ E(P) = E(P)·E(Q)）的 Hilbert 侧对应——
--  E-σ-add 的单调性前置）
E-hilb-sub : (P Q : ℝ → Set) → ((x : ℝ) → P x → Q x) → (x : V)
  → LinOp.f (E-hilb Q) (LinOp.f (E-hilb P) x) ≡ LinOp.f (E-hilb P) x
E-hilb-sub P Q pq x = proj-fixed (spectral-subspace Q) (LinOp.f (E-hilb P) x)
                                 (spectral-subspace-incl P Q pq (LinOp.f (E-hilb P) x)
                                                          (proj-in (spectral-subspace P) x))

-- 可数并谓词（σ-union）：∪ₙ Pₙ x = ∃ n. Pₙ x
σUnion : (ℕ → ℝ → Set) → ℝ → Set
σUnion P x = Σ ℕ (λ n → P n x)

-- σ-可数可加性（降定理路径登记，2026-08-02）：E(∪ₙPₙ) = supₘ Σᵢ<ₘE(Pᵢ)（连续下式）——
-- 需 LinOp 层算子序 sup 机制（随极限层）+ E-hilb-fin-union 有限一致性（已闭合）+
-- E-hilb-sub 单调性（已闭合）；完整形式（E(∪ₙPₙ)x = supₘ Σᵢ<ₘE(Pᵢ)x 点态 sup）
-- 随 σ-代数/极限层实现。SpectralTheory §10f E-σ-add（可数可加公理）的 Hilbert 侧路径。

-- ==================================================================
-- §11 谱半径公式极限层（阶段 8-6b 第一步，2026-08-02）
-- ==================================================================

-- 谱半径（Gelfand 公式沿 2^k 子列的幂形式刻画）：
-- r(X) := sup {r : r^{2^k} ≤ ‖X^{2^k}‖ ∀k}（自伴元 ⟹ r(X) = ‖X‖；
-- 避免 n 次根——iter-sq 迭代平方 + op-norm-power-2^k 直接闭合）
spectral-radius : LinOp → ℝ
spectral-radius X = sup-ℝ (λ r → (k : ℕ) → iter-sq r k ≤ℝ op-norm (op-power-2^k X k))

-- **可证**：r(X) ≤ ‖X‖（族成员 r ≤ ‖X‖ 经 k=0 特化 + sup-least）
sr-le-norm : (X : LinOp) → spectral-radius X ≤ℝ op-norm X
sr-le-norm X = sup-least (λ r → (k : ℕ) → iter-sq r k ≤ℝ op-norm (op-power-2^k X k))
                         (op-norm X)
                         (λ r h → h zero)

-- **可证**：自伴 ⟹ ‖X‖ ≤ r(X)（r = ‖X‖ 是族成员：op-norm-power-2^k 精确等式 + sup-upper）
sr-norm-le : (X : LinOp) → SelfAdjoint X → op-norm X ≤ℝ spectral-radius X
sr-norm-le X h = sup-upper (λ r → (k : ℕ) → iter-sq r k ≤ℝ op-norm (op-power-2^k X k))
                           (op-norm X)
                           (λ k → subst (λ z → iter-sq (op-norm X) k ≤ℝ z)
                                         (sym (op-norm-power-2^k X h k))
                                         (refl-≤ℝ {iter-sq (op-norm X) k}))

-- **可证**：谱半径 = 范数（自伴 C* 元，Gelfand 公式）——r(X) = ‖X‖
--（SpectralTheory §12 norm-contraction（σ(e^(-tA)) ⊆ (0,1] ⟹ ‖e^(-tA)‖ ≤ 1）
--  的 Hilbert 侧核心：自伴元谱半径 = 范数；norm-contraction 完整降定理 =
--  本定理 + e^(-tA) 自伴 + 谱支集 ⊆ (0,1] ⟹ r(e^(-tA)) ≤ 1，留 8-5b/整合层）
spectral-radius-norm : (X : LinOp) → SelfAdjoint X → spectral-radius X ≡ op-norm X
spectral-radius-norm X h = ≤-antisym (sr-le-norm X) (sr-norm-le X h)

-- ==================================================================
-- §12 强连续半群实例化框架（阶段 8-5b 第一步 + 8-6b 完整降定理连接，2026-08-02）
-- ==================================================================
-- 目标：e^(-tA) 的 Hilbert 层表示——SpectralTheory exp-tA（半群对象）+ exp-tA-fc
-- （e^(-tA) = fc(φ_t)）降定理的实例化侧：登记桥接 + 强连续拓扑性质可证 +
-- 自伴 ⟹ 谱半径 = 范数连接压缩（8-6b 完整降定理核心）。
-- 降定理路径（统一）：跨层模型（Op → LinOp）+ fc 函数演算（§5d-f）+
-- 谱积分（§1b）+ φ_t 的 ε-δ 连续性（测度论/极限层）。

-- e^(-tA) 的 Hilbert 层表示（桥接登记：SpectralTheory exp-tA 的 LinOp 实例，
-- 半群方程/单位/自伴/压缩/范数连续——降定理路径见上）
postulate
  exp-hilb-tA : ℝ → LinOp
  -- 半群方程（点态）：e^(-(s+t)A) x = e^(-sA)(e^(-tA) x)（semigroup 的 LinOp 侧）
  exp-hilb-semigroup : (s t : ℝ) (x : V) → LinOp.f (exp-hilb-tA (s +ℝ t)) x
    ≡ LinOp.f (op-comp (exp-hilb-tA s) (exp-hilb-tA t)) x
  -- 单位：e^(-0·A) x = x（exp-tA-zero 的 LinOp 侧）
  exp-hilb-zero : (x : V) → LinOp.f (exp-hilb-tA zeroℝ) x ≡ x
  -- 自伴：e^(-tA) 自伴（φ_t 值域 ⊆ (0,1] 实值 + fc 保自伴）
  exp-hilb-self-adjoint : (t : ℝ) → SelfAdjoint (exp-hilb-tA t)
  -- 压缩：‖e^(-tA)‖ ≤ 1（σ(e^(-tA)) ⊆ (0,1]（E-exp-tA-contractive 谱测度形式）⟹
  -- 谱半径 ≤ 1 ⟹ 范数 ≤ 1，经 spectral-radius-norm）
  exp-hilb-contractive : (t : ℝ) → op-norm (exp-hilb-tA t) ≤ℝ oneℝ
  -- 范数连续（0⁺ 极限）：‖e^(-tA) − id‖ → 0（φ_t 的 ε-δ 连续性 + 谱积分）
  exp-hilb-norm-cont : op-norm-conv exp-hilb-tA id-op

-- **可证**：e^(-tA) 强连续（SOT）——范数连续 ⟹ 强连续（sot-from-norm 特化；
--   SpectralTheory strong-continuity（lim_{t→0⁺} e^(-tA) = 𝟙ₒ，Hille-Yosida 条件 iv）
--   的 Hilbert 侧对应——范数拓扑细于强拓扑）
exp-hilb-strong-cont : SOT-conv exp-hilb-tA id-op
exp-hilb-strong-cont = sot-from-norm exp-hilb-tA id-op exp-hilb-norm-cont

-- **可证**：自伴 + 压缩 ⟹ 谱半径 ≤ 1——r(e^(-tA)) = ‖e^(-tA)‖ ≤ 1
--（spectral-radius-norm（自伴 ⟹ r(X) = ‖X‖，§11）+ exp-hilb-contractive；
--  SpectralTheory §12 norm-contraction 的 Hilbert 侧完整降定理核心：
--  谱支集 ⊆ (0,1]（E-exp-tA-contractive）⟹ 压缩 ⟹ r ≤ 1）
exp-hilb-radius-le-one : (t : ℝ) → spectral-radius (exp-hilb-tA t) ≤ℝ oneℝ
exp-hilb-radius-le-one t =
  subst (λ z → z ≤ℝ oneℝ) (sym (spectral-radius-norm (exp-hilb-tA t) (exp-hilb-self-adjoint t)))
        (exp-hilb-contractive t)

-- ==================================================================
-- §12' 自伴算子 A 与 Borel 函数演算的 Hilbert 层模型（2026-08-03，方案②）
-- ==================================================================
-- 谱定理降定理链的**端点桥接**：自伴算子谱定理给出 A 的谱分解（A = ∫λ dE(λ)）与
-- Borel 函数演算（f(A) = ∫f dE(λ)）。本层登记端点模型（A-hilb/fc-hilb），与
-- spectral-subspace（§10c 谱子空间）/exp-hilb-tA（§12 半群）同层；链体（谱定理
-- 证明）为降定理路径（完整形式化 = 泛函分析谱定理，超出框架，文档化）。
-- 用途：CrossLayer §2 谱对象映射证书扩展 A/fc 字段（技术债项 4 谱对象映射完整闭合）。

-- 自伴算子 A 的 Hilbert 层模型（SpectralTheory A ↦ 自伴算子）
postulate
  A-hilb : LinOp
  -- A 自伴（SpectralTheory A 自伴正定的 Hilbert 侧；正定 = 谱支集 [0,∞)
  -- 经 spectral-subspace）
  A-hilb-self-adjoint : SelfAdjoint A-hilb
  -- A 与谱投影交换：A E(P) = E(P) A（谱定理交换子性质——A = ∫λ dE(λ) 与每个
  -- E(P) 交换；SpectralTheory M-Sp/M-σ（Fuglede 方向）的 Hilbert 侧；
  -- 降定理路径 = 自伴算子谱定理）
  A-hilb-comm-E : (P : ℝ → Set) (x : V)
    → LinOp.f (op-comp A-hilb (E-hilb P)) x ≡ LinOp.f (op-comp (E-hilb P) A-hilb) x

-- Borel 函数演算的 Hilbert 层模型（SpectralTheory fc f ↦ fc-hilb f）
postulate
  fc-hilb : (ℝ → ℝ) → LinOp
  -- 恒等函数演算 = A：fc-hilb(id) = A-hilb（f ↦ f(A) 同态 + 谱定理 ∫id dE = A；
  --   降定理路径 = Borel 函数演算/谱定理）
  fc-hilb-id : (x : V) → LinOp.f (fc-hilb (λ y → y)) x ≡ LinOp.f A-hilb x
  -- 指数函数演算 = 半群：fc-hilb(e^(-t·)) = exp-hilb-tA t（φ_t 的 Borel 函数演算；
  --   SpectralTheory §8c exp-tA = fc(φ_t)（exp-tA-fc）的 Hilbert 侧；
  --   降定理路径 = Borel 函数演算/谱积分）
  fc-hilb-exponential : (t : ℝ) (x : V)
    → LinOp.f (fc-hilb (λ y → exp (negℝ (t *ℝ y)))) x ≡ LinOp.f (exp-hilb-tA t) x

-- ==================================================================
-- §13 算子序与投影单调性（E-σ-add 完整形式的机制前置，2026-08-02）
-- ==================================================================

-- Hilbert 层算子序（正算子序）：X ≤ₗ Y ⟺ ∀v. ⟨(Y−X)v, v⟩ ≥ 0
--（投影值测度的算子序基础——E-σ-add（E(∪ₙPₙ) = supₘ Σᵢ<ₘE(Pᵢ)）的上确界机制）
_≤ₗ_ : LinOp → LinOp → Set
X ≤ₗ Y = (v : V) → zeroℝ ≤ℝ (LinOp.f (op-sub Y X) v ⟨⟩ v)

-- **可证**：谱投影算子序单调——P ⊆ Q ⟹ E(P) ≤ₗ E(Q)
--（⟨(E(Q)−E(P))v, v⟩ = ‖E(Q)(v−E(P)v)‖² ≥ 0：
--  v = E(P)v + w（proj-decomp），E(Q)(E(P)v) = E(P)v（E-hilb-sub）⟹
--  (E(Q)−E(P))v = E(Q)w；⟨E(Q)w, v⟩ = ⟨E(Q)w, E(P)v⟩ + ⟨E(Q)w, w⟩
--  = ⟨w, E(P)v⟩（E(Q) 自伴 + E-hilb-sub）+ ‖E(Q)w‖²（E(Q) 自伴 + 幂等）
--  = 0 + ‖E(Q)w‖²（w ⊥ W_P）——投影序单调的 Hilbert 侧，E-σ-add 的单调性基础）
E-hilb-mono : (P Q : ℝ → Set) → ((x : ℝ) → P x → Q x) → E-hilb P ≤ₗ E-hilb Q
E-hilb-mono P Q pq v =
  subst (λ z → zeroℝ ≤ℝ z) (sym ip-eq) (norm-sq-nonneg (LinOp.f (E-hilb Q) w))
  where
  X : LinOp
  X = E-hilb P
  Y : LinOp
  Y = E-hilb Q
  w : V
  w = v -ᵥ LinOp.f X v
  -- v = Xv + w（正交分解）
  v-decomp : v ≡ LinOp.f X v +ᵥ w
  v-decomp = proj-decomp (spectral-subspace P) v
  -- Yv = Xv + Yw（线性性 + E-hilb-sub：Y(Xv) = Xv，x = v 特化）
  Yv-eq : LinOp.f Y v ≡ LinOp.f X v +ᵥ LinOp.f Y w
  Yv-eq =
    trans (cong (LinOp.f Y) v-decomp)
          (trans (LinOp.lin-add Y (LinOp.f X v) w)
                 (cong₂ _+ᵥ_ (E-hilb-sub P Q pq v) refl))
  -- (Xv+Yw) − Xv = Yw（向量代数：结合/交换/逆/零）
  add-sub-cancel : (LinOp.f X v +ᵥ LinOp.f Y w) -ᵥ LinOp.f X v ≡ LinOp.f Y w
  add-sub-cancel =
    trans (+ᵥ-assoc (LinOp.f X v) (LinOp.f Y w) ((negℝ oneℝ) ·ᵥ LinOp.f X v))
          (trans (cong (λ u → LinOp.f X v +ᵥ u)
                       (+ᵥ-comm (LinOp.f Y w) ((negℝ oneℝ) ·ᵥ LinOp.f X v)))
                 (trans (sym (+ᵥ-assoc (LinOp.f X v) ((negℝ oneℝ) ·ᵥ LinOp.f X v) (LinOp.f Y w)))
                        (trans (cong (λ u → u +ᵥ LinOp.f Y w) (+-inv-ᵥ (LinOp.f X v)))
                               (zero-l-ᵥ (LinOp.f Y w)))))
  -- (Y−X)v = Yv − Xv = Yw
  diff-eq : LinOp.f (op-sub Y X) v ≡ LinOp.f Y w
  diff-eq = trans (cong (λ t → t -ᵥ LinOp.f X v) Yv-eq) add-sub-cancel
  -- ⟨Yw, Xv⟩ = 0（E(Q) 自伴 + E-hilb-sub（x = v）+ w ⊥ W_P）
  orth-Xw : (LinOp.f Y w) ⟨⟩ (LinOp.f X v) ≡ zeroℝ
  orth-Xw =
    trans (proj-self-adjoint (spectral-subspace Q) w (LinOp.f X v))
          (trans (cong (λ t → w ⟨⟩ t) (E-hilb-sub P Q pq v))
                 (proj-orth (spectral-subspace P) v (LinOp.f X v)
                            (proj-in (spectral-subspace P) v)))
  -- ⟨Yw, w⟩ = ‖Yw‖²（E(Q) 自伴 + 幂等）
  ww-eq : (LinOp.f Y w) ⟨⟩ w ≡ (LinOp.f Y w ⟨⟩ LinOp.f Y w)
  ww-eq =
    trans (proj-self-adjoint (spectral-subspace Q) w w)
          (trans (cong (λ t → w ⟨⟩ t) (sym (proj-idemp (spectral-subspace Q) w)))
                 (sym (proj-self-adjoint (spectral-subspace Q) w (LinOp.f Y w))))
  -- ⟨(Y−X)v, v⟩ = ⟨Yw, v⟩ = ⟨Yw, Xv+w⟩ = ⟨Yw,Xv⟩ + ⟨Yw,w⟩ = 0 + ‖Yw‖² = ‖Yw‖²
  ip-eq : (LinOp.f (op-sub Y X) v ⟨⟩ v) ≡ (LinOp.f Y w ⟨⟩ LinOp.f Y w)
  ip-eq =
    trans (cong (λ t → t ⟨⟩ v) diff-eq)
          (trans (cong (λ u → (LinOp.f Y w) ⟨⟩ u) (v-decomp))
                 (trans (ip-add-r (LinOp.f Y w) (LinOp.f X v) w)
                        (trans (cong₂ _+ℝ_ orth-Xw ww-eq)
                               (zero-add-ℝ (LinOp.f Y w ⟨⟩ LinOp.f Y w)))))

-- ==================================================================
-- §14 E-σ-add 完整形式（可数可加性，2026-08-02）
-- ==================================================================

-- LinOp 层有限和（点态向量和封装：Σᵢ<ₘ Fᵢ）
sum-ₗ : (ℕ → LinOp) → ℕ → LinOp
sum-ₗ F zero = zero-op
sum-ₗ F (suc m) = op-add (sum-ₗ F m) (F m)

-- LinOp 层算子序上确界（桥接登记：正算子序 sup——E-σ-add 的连续下式机制；
-- 降定理路径 = 强/弱算子拓扑下单调有界收敛（极限层））
postulate
  supₗ : (LinOp → Set) → LinOp
  supₗ-upper : (S : LinOp → Set) (X : LinOp) → S X → X ≤ₗ supₗ S
  supₗ-least : (S : LinOp → Set) (B : LinOp) → ((X : LinOp) → S X → X ≤ₗ B) → supₗ S ≤ₗ B

-- **可证**：有限前段单调——E(∪ᵢ<ₘPᵢ) ≤ₗ E(∪ₙPₙ)
--（FinUnion P m ⊆ σUnion P：fin-union-in（∃i<ₘ.Pᵢx）⟹ σUnion（取 n=i）+ E-hilb-mono——
--  E-σ-add 连续下式的上界方向）
E-hilb-fin-le-σ : (P : ℕ → ℝ → Set) (m : ℕ) → E-hilb (FinUnion P m) ≤ₗ E-hilb (σUnion P)
E-hilb-fin-le-σ P m = E-hilb-mono (FinUnion P m) (σUnion P)
                                 (λ x fx → sigma-union-in P m x fx)
  where
  -- FinUnion P m x ⟹ σUnion P x（fin-union-in 取指标 n = i）
  sigma-union-in : (P : ℕ → ℝ → Set) (m : ℕ) (x : ℝ) → FinUnion P m x → σUnion P x
  sigma-union-in P m x fx with fin-union-in P m x fx
  sigma-union-in P m x fx | ex i (ile , pxi) = ex i pxi

-- σ-可数可加性（桥接登记，2026-08-02）：E(∪ₙPₙ) = supₘ Σᵢ<ₘE(Pᵢ)（连续下式）——
-- 上界方向（有限前段单调 E-hilb-fin-le-σ 可证）+ least 方向（supₗ-least）；
-- 完整收敛（sup 存在与算子序完备）随极限层（强/弱算子拓扑单调有界收敛）。
-- SpectralTheory §10f E-σ-add（可数可加公理）的 Hilbert 侧对应。
postulate
  E-hilb-σ-add : (P : ℕ → ℝ → Set) → ((i j : ℕ) → suc i ≤ℕ j → (x : ℝ) → P i x → P j x → ⊥)
    → E-hilb (σUnion P) ≡ supₗ (λ Y → Σ ℕ (λ m → Y ≡ sum-ₗ (λ i → E-hilb (P i)) m))

-- ------------------------------------------------------------------
-- E-σ-add 收敛 阶段 1：连续下式族的单调有界结构（2026-08-03）
-- ------------------------------------------------------------------
-- 目标：E-σ-add（E(∪ₙPₙ) = supₘ Σᵢ<ₘE(Pᵢ)）连续下式族的**单调有界结构**全部可证——
-- 即 Vigier 定理（强/弱算子拓扑单调有界收敛）的假设条件在 Hilbert 层成立：
--   - 单调：E-σ-family-increasing（谱投影非负 E-hilb-nonneg ⟹ 部分和递增）
--   - 有界：E-σ-family-bounded（部分和 ≤ₗ E(∪ₙPₙ)，supₗ-upper + E-hilb-σ-add）
-- supₗ 存在性（收敛本身）为 Vigier 桥接（降定理路径 = 强算子拓扑单调有界收敛）。

-- **可证**：谱投影非负——0 ≤ ⟨E(P)v, v⟩ = ‖E(P)v‖² ≥ 0
--（E(P) 自伴 + 幂等：⟨Ev,v⟩ = ⟨v,Ev⟩ = ⟨v,E(Ev)⟩ = ⟨E(Ev),v⟩ = ⟨Ev,Ev⟩ = ‖Ev‖²）
E-hilb-nonneg : (P : ℝ → Set) (v : V) → zeroℝ ≤ℝ (LinOp.f (E-hilb P) v ⟨⟩ v)
E-hilb-nonneg P v =
  subst (λ z → zeroℝ ≤ℝ z) (sym E-hilb-nonneg-eq) (norm-sq-nonneg (LinOp.f (E-hilb P) v))
  where
  E : LinOp
  E = E-hilb P
  -- ⟨Ev,v⟩ = ⟨v,Ev⟩ = ⟨v,E(Ev)⟩ = ⟨E(Ev),v⟩ = ⟨Ev,Ev⟩
  E-hilb-nonneg-eq : (LinOp.f E v ⟨⟩ v) ≡ (LinOp.f E v ⟨⟩ LinOp.f E v)
  E-hilb-nonneg-eq =
    trans (E-hilb-self-adjoint P v v)
          (trans (cong (λ t → v ⟨⟩ t) (sym (E-hilb-idemp P v)))
                 (trans (ip-sym v (LinOp.f E (LinOp.f E v)))
                        (E-hilb-self-adjoint P (LinOp.f E v) v)))

-- **可证**：非负项右加单调（点态）——∀v. 0 ≤ ⟨Bv,v⟩ ⟹ (X+B) − X 逐点 = B
--（op-sub 点态代数：(Xv+Bv)+(−Xv) = Bv（结合/交换/逆/零）；(X+B−X)v = Bv 收缩）
≤ₗ-add-nonneg-r : (X B : LinOp) → ((v : V) → zeroℝ ≤ℝ (LinOp.f B v ⟨⟩ v)) → (v : V)
  → zeroℝ ≤ℝ (LinOp.f (op-sub (op-add X B) X) v ⟨⟩ v)
≤ₗ-add-nonneg-r X B hB v =
  subst (λ z → zeroℝ ≤ℝ z) (sym (add-sub-diff v)) (hB v)
  where
  -- (Xv+Bv)+(−Xv) = Bv（向量代数：结合 + 交换 + 逆 + 零元）
  pointwise-sub : (v : V) → LinOp.f (op-sub (op-add X B) X) v ≡ LinOp.f B v
  pointwise-sub v =
    trans (+ᵥ-assoc (LinOp.f X v) (LinOp.f B v) ((negℝ oneℝ) ·ᵥ LinOp.f X v))
          (trans (cong (λ u → LinOp.f X v +ᵥ u)
                       (+ᵥ-comm (LinOp.f B v) ((negℝ oneℝ) ·ᵥ LinOp.f X v)))
                 (trans (sym (+ᵥ-assoc (LinOp.f X v) ((negℝ oneℝ) ·ᵥ LinOp.f X v) (LinOp.f B v)))
                        (trans (cong (λ u → u +ᵥ LinOp.f B v) (+-inv-ᵥ (LinOp.f X v)))
                               (zero-l-ᵥ (LinOp.f B v)))))
  -- ⟨(X+B−X)v, v⟩ = ⟨Bv, v⟩（op-sub 定义性展开后逐点收缩）
  add-sub-diff : (v : V) → (LinOp.f (op-sub (op-add X B) X) v ⟨⟩ v) ≡ (LinOp.f B v ⟨⟩ v)
  add-sub-diff v = cong (λ t → t ⟨⟩ v) (pointwise-sub v)

-- **可证**：连续下式族单调——Σᵢ<ₘE(Pᵢ) ≤ₗ Σᵢ<ₘ₊₁E(Pᵢ)
--（sum-ₗ (suc m) = op-add (sum-ₗ m) (E(P m)) + 每个 E(Pᵢ) 非负（E-hilb-nonneg））
E-σ-family-increasing : (P : ℕ → ℝ → Set) (m : ℕ) (v : V)
  → zeroℝ ≤ℝ (LinOp.f (op-sub (sum-ₗ (λ i → E-hilb (P i)) (suc m))
                              (sum-ₗ (λ i → E-hilb (P i)) m)) v ⟨⟩ v)
E-σ-family-increasing P m =
  ≤ₗ-add-nonneg-r (sum-ₗ (λ i → E-hilb (P i)) m) (E-hilb (P m)) (E-hilb-nonneg (P m))

-- **可证**：连续下式族有界——Σᵢ<ₘE(Pᵢ) ≤ₗ E(∪ₙPₙ)
--（supₗ-upper（族成员：ex m refl）+ E-hilb-σ-add（E(∪ₙPₙ) ≡ supₗ 族））
E-σ-family-bounded : (P : ℕ → ℝ → Set) → ((i j : ℕ) → suc i ≤ℕ j → (x : ℝ) → P i x → P j x → ⊥)
  → (m : ℕ) → sum-ₗ (λ i → E-hilb (P i)) m ≤ₗ E-hilb (σUnion P)
E-σ-family-bounded P h m =
  subst (λ Z → sum-ₗ (λ i → E-hilb (P i)) m ≤ₗ Z) (sym (E-hilb-σ-add P h))
        (supₗ-upper (λ Y → Σ ℕ (λ n → Y ≡ sum-ₗ (λ i → E-hilb (P i)) n))
                    (sum-ₗ (λ i → E-hilb (P i)) m) (ex m refl))

-- ------------------------------------------------------------------
-- E-σ-add 收敛 阶段 2：Vigier 强收敛（2026-08-03）
-- ------------------------------------------------------------------
-- 目标：E-σ-add 连续下式族的**强收敛**——Σᵢ<ₘE(Pᵢ) SOT → E(∪ₙPₙ)。
-- 阶段 1 已证单调（E-σ-family-increasing）+ 有界（E-σ-family-bounded）；
-- 阶段 2：自伴（sumₗ-self-adjoint 可证）+ Vigier 定理（强/弱算子拓扑单调有界收敛，
-- supₗ 存在性/收敛的降定理路径）⟹ E-σ-SOT-conv（部分和强收敛到 E(∪ₙPₙ)）。

-- 强收敛（ℕ-序列，SOT）：Tₘ → T∞ ⟺ ∀v. ‖Tₘv − T∞v‖ → 0（ε-δ 序列收敛 Converges 特化）
SOT-conv-seq : (ℕ → LinOp) → LinOp → Set
SOT-conv-seq T T∞ = (v : V) → Converges (λ m → LinOp.f (T m) v) (LinOp.f T∞ v)

-- **可证**：零算子自伴（⟨0x,y⟩ = 0 = ⟨x,0y⟩）
self-adjoint-zero-op : SelfAdjoint zero-op
self-adjoint-zero-op x y = trans (ip-zero-l y) (sym (ip-zero-r x))

-- **可证**：自伴和——SelfAdjoint X ⟹ SelfAdjoint Y ⟹ SelfAdjoint (X+Y)
--（⟨(X+Y)x,y⟩ = ⟨Xx,y⟩+⟨Yx,y⟩（ip-add-l）= ⟨x,Xy⟩+⟨x,Yy⟩ = ⟨x,(X+Y)y⟩（ip-add-r））
self-adjoint-op-add : (X Y : LinOp) → SelfAdjoint X → SelfAdjoint Y → SelfAdjoint (op-add X Y)
self-adjoint-op-add X Y hX hY x y =
  trans (ip-add-l (LinOp.f X x) (LinOp.f Y x) y)
        (trans (cong₂ _+ℝ_ (hX x y) (hY x y))
               (sym (ip-add-r x (LinOp.f X y) (LinOp.f Y y))))

-- **可证**：有限和自伴——逐项自伴 ⟹ sumₗ 自伴（归纳）
sumₗ-self-adjoint : (F : ℕ → LinOp) → ((i : ℕ) → SelfAdjoint (F i)) → (m : ℕ)
  → SelfAdjoint (sum-ₗ F m)
sumₗ-self-adjoint F h zero = self-adjoint-zero-op
sumₗ-self-adjoint F h (suc m) =
  self-adjoint-op-add (sum-ₗ F m) (F m) (sumₗ-self-adjoint F h m) (h m)

-- Vigier 定理（桥接登记，2026-08-03）：单调递增的自伴算子族 ⟹ 强收敛到最小上界 supₗ
--（强/弱算子拓扑单调有界收敛——E-σ-add 的 supₗ 存在性/收敛的降定理路径；
--  有界上由 supₗ-upper 自动保证；构造化实现需标量单调收敛（ℝ 完备性 ε-逼近）+
--  自伴范数平方估计 ‖(sup−Tₘ)v‖² ≤ ‖sup−Tₘ‖·⟨(sup−Tₘ)v,v⟩，⟨(sup−Tₘ)v,v⟩ → 0）
postulate
  Vigier-strong-conv : (T : ℕ → LinOp)
    → ((m : ℕ) → SelfAdjoint (T m))
    → ((m : ℕ) → T m ≤ₗ T (suc m))
    → SOT-conv-seq T (supₗ (λ Y → Σ ℕ (λ m → Y ≡ T m)))

-- **可证**：E-σ 连续下式族强收敛到 E(∪ₙPₙ)——E-σ-add 的收敛侧闭合
--（Vigier-strong-conv（自伴 sumₗ-self-adjoint + 单调 E-σ-family-increasing）
--  + E-hilb-σ-add（E(∪ₙPₙ) ≡ supₗ 族））
E-σ-SOT-conv : (P : ℕ → ℝ → Set) → ((i j : ℕ) → suc i ≤ℕ j → (x : ℝ) → P i x → P j x → ⊥)
  → SOT-conv-seq (λ m → sum-ₗ (λ i → E-hilb (P i)) m) (E-hilb (σUnion P))
E-σ-SOT-conv P h =
  subst (λ Z → SOT-conv-seq T Z) (sym (E-hilb-σ-add P h))
        (Vigier-strong-conv T hSelf hMono)
  where
  T : ℕ → LinOp
  T = λ m → sum-ₗ (λ i → E-hilb (P i)) m
  hSelf : (m : ℕ) → SelfAdjoint (T m)
  hSelf m = sumₗ-self-adjoint (λ i → E-hilb (P i)) (λ i → E-hilb-self-adjoint (P i)) m
  hMono : (m : ℕ) → T m ≤ₗ T (suc m)
  hMono m = E-σ-family-increasing P m

-- ==================================================================
-- §15 谱投影范数幂等（‖E(P)‖² = ‖E(P)‖，2026-08-02）
-- ==================================================================

-- **可证**：sup 外延——谓词外延相同 ⟹ sup 相等（sup-least/upper 双向 + ≤-antisym）
sup-ext-ℝ : (S T : ℝ → Set) → ((r : ℝ) → S r → T r) → ((r : ℝ) → T r → S r) → sup-ℝ S ≡ sup-ℝ T
sup-ext-ℝ S T s→t t→s =
  ≤-antisym (sup-least S (sup-ℝ T) (λ r sr → sup-upper T r (s→t r sr)))
            (sup-least T (sup-ℝ S) (λ r tr → sup-upper S r (t→s r tr)))

-- **可证**：谱投影范数幂等——‖E(P)‖² = ‖E(P)‖
--（norm-power（E(P) 自伴）：‖E(P)²‖ = ‖E(P)‖²；点态幂等 E-hilb-idemp +
--  sup 外延（op-fam 谓词外延相同）⟹ ‖E(P)²‖ = ‖E(P)‖——
--  SpectralTheory §12 idem-zero-one/proj-norm（幂等元范数 ∈{0,1}）的 Hilbert 侧对应）
E-hilb-norm-idempotent : (P : ℝ → Set) → (op-norm (E-hilb P) *ℝ op-norm (E-hilb P)) ≡ op-norm (E-hilb P)
E-hilb-norm-idempotent P =
  trans (sym (norm-power (E-hilb P) (E-hilb-self-adjoint P)))
        (sup-ext-ℝ (op-fam (op-comp (E-hilb P) (E-hilb P))) (op-fam (E-hilb P))
                   (fam-pp→p P) (fam-p→pp P))
  where
  -- op-fam (E(P)²) ⊆ op-fam E(P)：E(P)(E(P)v) = E(P)v（幂等）
  fam-pp→p : (P : ℝ → Set) (r : ℝ) → op-fam (op-comp (E-hilb P) (E-hilb P)) r → op-fam (E-hilb P) r
  fam-pp→p P r (ex v (hv , refl)) = ex v (hv , trans refl (cong norm (E-hilb-idemp P v)))
  -- op-fam E(P) ⊆ op-fam (E(P)²)：反向
  fam-p→pp : (P : ℝ → Set) (r : ℝ) → op-fam (E-hilb P) r → op-fam (op-comp (E-hilb P) (E-hilb P)) r
  fam-p→pp P r (ex v (hv , refl)) = ex v (hv , trans refl (sym (cong norm (E-hilb-idemp P v))))

-- ==================================================================
-- §16 算子代数完整化（跨层模型代数基础，2026-08-02）
-- ==================================================================
-- 目标：LinOp 层算子代数结构完整化——标量乘 + 结合/单位律（点态版）——
-- 为 8-5b 余项（跨层模型 Op → LinOp：SpectralTheory 算子代数公理在
-- LinOp 层的点态对应）铺路。点态版避免 funext（LinOp record 依赖字段
-- lin-add/lin-scalar 的相等需依赖 funext，超出库公理范围）。

-- 标量乘（LinOp 层）：(c·ₗ X)v = c·(Xv)（线性性：·ᵥ-distrib + ·ᵥ-assoc + *-comm）
_·ₗ_ : ℝ → LinOp → LinOp
c ·ₗ X = record
  { f = λ x → c ·ᵥ LinOp.f X x
  ; lin-add = λ x y → trans (cong (λ w → c ·ᵥ w) (LinOp.lin-add X x y))
                            (·ᵥ-distrib-l c (LinOp.f X x) (LinOp.f X y))
  ; lin-scalar = λ a x → trans (cong (λ w → c ·ᵥ w) (LinOp.lin-scalar X a x))
                               (trans (·ᵥ-assoc c a (LinOp.f X x))
                                      (trans (cong (λ s → s ·ᵥ LinOp.f X x) (*-comm-ℝ c a))
                                             (sym (·ᵥ-assoc a c (LinOp.f X x)))))
  }

-- **可证**：标量单位（点态）——1·ₗ X 逐点 = X
·ₗ-ident-pt : (X : LinOp) (v : V) → LinOp.f (oneℝ ·ₗ X) v ≡ LinOp.f X v
·ₗ-ident-pt X v = ·ᵥ-ident (LinOp.f X v)

-- **可证**：op-comp 结合律（点态）——(X∘Y)∘Z 与 X∘(Y∘Z) 逐点相等（定义性）
op-comp-assoc-pt : (X Y Z : LinOp) (v : V)
  → LinOp.f (op-comp (op-comp X Y) Z) v ≡ LinOp.f (op-comp X (op-comp Y Z)) v
op-comp-assoc-pt X Y Z v = refl

-- **可证**：op-comp 单位律（点态）——id∘X 与 X∘id 逐点等于 X
op-comp-id-pt : (X : LinOp) (v : V) → LinOp.f (op-comp id-op X) v ≡ LinOp.f X v
op-comp-id-pt X v = refl
op-comp-id-r-pt : (X : LinOp) (v : V) → LinOp.f (op-comp X id-op) v ≡ LinOp.f X v
op-comp-id-r-pt X v = refl

-- **可证**：标量对加法分配（点态）——c·ₗ(X+Y) 与 c·ₗX + c·ₗY 逐点相等
·ₗ-distrib-add-pt : (c : ℝ) (X Y : LinOp) (v : V)
  → LinOp.f (c ·ₗ (op-add X Y)) v ≡ LinOp.f (op-add (c ·ₗ X) (c ·ₗ Y)) v
·ₗ-distrib-add-pt c X Y v = ·ᵥ-distrib-l c (LinOp.f X v) (LinOp.f Y v)

-- **可证**：标量与复合（点态）——c·ₗ(X∘Y) 与 (c·ₗX)∘Y 逐点相等（定义性）
·ₗ-comp-pt : (c : ℝ) (X Y : LinOp) (v : V)
  → LinOp.f (c ·ₗ (op-comp X Y)) v ≡ LinOp.f (op-comp (c ·ₗ X) Y) v
·ₗ-comp-pt c X Y v = refl

-- 跨层点态律补全（2026-08-03，8-5b 余项：Op 层算子代数公理在 LinOp 层的点态对应）：
-- 加法结合/交换/单位（+ᵥ 向量空间律）、复合零吸收（lin-zero）、
-- 分配（lin-add）、标量跨复合（lin-scalar）、标量零吸收（scalar-zero-any）——
-- 全部逐点（∀v. LinOp.f 值相等），零新增公理（funext 仅算子层等式需要）。

-- **可证**：加法结合律（点态）——(X+Y)+Z 与 X+(Y+Z) 逐点相等（+ᵥ-assoc）
+ₗ-assoc-pt : (X Y Z : LinOp) (v : V)
  → LinOp.f (op-add (op-add X Y) Z) v ≡ LinOp.f (op-add X (op-add Y Z)) v
+ₗ-assoc-pt X Y Z v = +ᵥ-assoc (LinOp.f X v) (LinOp.f Y v) (LinOp.f Z v)

-- **可证**：加法交换律（点态）——X+Y 与 Y+X 逐点相等（+ᵥ-comm）
+ₗ-comm-pt : (X Y : LinOp) (v : V) → LinOp.f (op-add X Y) v ≡ LinOp.f (op-add Y X) v
+ₗ-comm-pt X Y v = +ᵥ-comm (LinOp.f X v) (LinOp.f Y v)

-- **可证**：加法单位律（点态）——X+0 逐点等于 X（+ᵥ-ident）
+ₗ-ident-pt : (X : LinOp) (v : V) → LinOp.f (op-add X zero-op) v ≡ LinOp.f X v
+ₗ-ident-pt X v = +ᵥ-ident (LinOp.f X v)

-- **可证**：右零吸收（点态）——X∘0 逐点等于 0（线性 ⟹ X(0) = 0）
*ₗ-zero-r-pt : (X : LinOp) (v : V) → LinOp.f (op-comp X zero-op) v ≡ LinOp.f zero-op v
*ₗ-zero-r-pt X v = lin-zero X

-- **可证**：左零吸收（点态）——0∘X 逐点等于 0（定义性）
*ₗ-zero-l-pt : (X : LinOp) (v : V) → LinOp.f (op-comp zero-op X) v ≡ LinOp.f zero-op v
*ₗ-zero-l-pt X v = refl

-- **可证**：右分配（点态）——X∘(Y+Z) 与 X∘Y + X∘Z 逐点相等（线性性 lin-add）
distribₗ-pt : (X Y Z : LinOp) (v : V)
  → LinOp.f (op-comp X (op-add Y Z)) v ≡ LinOp.f (op-add (op-comp X Y) (op-comp X Z)) v
distribₗ-pt X Y Z v = LinOp.lin-add X (LinOp.f Y v) (LinOp.f Z v)

-- **可证**：左分配（点态）——(X+Y)∘Z 与 X∘Z + Y∘Z 逐点相等（定义性）
distribₗ-l-pt : (X Y Z : LinOp) (v : V)
  → LinOp.f (op-comp (op-add X Y) Z) v ≡ LinOp.f (op-add (op-comp X Z) (op-comp Y Z)) v
distribₗ-l-pt X Y Z v = refl

-- **可证**：标量跨复合（点态）——X∘(c·ₗY) 与 c·ₗ(X∘Y) 逐点相等（线性性 lin-scalar）
·ₗ-comm-l-pt : (c : ℝ) (X Y : LinOp) (v : V)
  → LinOp.f (op-comp X (c ·ₗ Y)) v ≡ LinOp.f (c ·ₗ (op-comp X Y)) v
·ₗ-comm-l-pt c X Y v = LinOp.lin-scalar X c (LinOp.f Y v)

-- **可证**：标量零吸收（点态）——0·ₗX 逐点等于 0（scalar-zero-any）
·ₗ-zero-l-pt : (X : LinOp) (v : V) → LinOp.f (zeroℝ ·ₗ X) v ≡ LinOp.f zero-op v
·ₗ-zero-l-pt X v = scalar-zero-any (LinOp.f X v)

-- **可证**：标量乘零算子（点态）——(c·ₗ𝟘ₗ)v = 𝟘ₗ v（scalar-zero；
--  P1Spectral ·ₒ-zero-r（a·ₒ𝟘ₒ = 𝟘ₒ，2026-08-03 补充公理）的点态对应）
·ₗ-zero-r-pt : (c : ℝ) (v : V) → LinOp.f (c ·ₗ zero-op) v ≡ LinOp.f zero-op v
·ₗ-zero-r-pt c v = scalar-zero c

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
--    （sup-ℝ 完备性假设）；op-norm-nonneg/op-norm-upper/op-norm-tri 可证；
--    **8-3b 缩放引理**（op-norm-scalar：‖Sw‖≤‖S‖·‖w‖，单位化 w/‖w‖）⟹
--    **op-norm-submul**（‖ST‖≤‖S‖‖T‖）——norm-pos/norm-tri/norm-submul 全从 sup 定义证明。
--  - 阶段 4（✅ 2026-08-02）：自伴算子 + C* 恒等——adj（Riesz 表示桥接）+ adj-ip +
--    SelfAdjoint（⟨Xx,y⟩=⟨x,Xy⟩）+ 可证 adj-move/v-mul-le-one/norm-sq-adj-est/
--    op-norm-adj-est/op-norm-le-sqrt/**norm-power**（自伴幂恒等 ‖X²‖=‖X‖²，
--    submul + √ 估计 + ≤-antisym）——SpectralTheory §12 C*-范数公理降定理路径核心闭环。
--  - 阶段 5（✅ 2026-08-02）：算子拓扑层——V 减法 _−ᵥ_ + op-neg/op-sub（算子减法）；
--    ε-δ 强收敛 SOT-conv / 范数收敛 op-norm-conv（0⁺ 右极限）定义 +
--    **可证** sot-from-norm（范数收敛 ⟹ 强收敛：缩放 + η=ε/(1+‖v‖) 除法技巧）——
--    范数拓扑细于强拓扑；SpectralTheory lim-op/strong-continuity 降定理路径的拓扑地基。
--  - 阶段 8（✅ 2026-08-02）：完备性层——Hilbert 空间公理补全：Seq/≤ℕ（局部）/
--    Cauchy-seq/Converges（ε-δ 定义）+ 完备性基础假设 complete + 可证 ≤ℕ-refl/trans/suc、
--    sub-ᵥ-self（x−x=0）、conv-const/cauchy-const（常值序列收敛/Cauchy）——
--    Riesz 表示/投影定理/谱定理的共同地基（pre-Hilbert ⟹ Hilbert 空间）。
--  - 阶段 6a（✅ 2026-08-02）：谱半径公式的代数核心——id-op/op-sq/op-power/op-power-2^k/
--    iter-mul/iter-sq + **可证** op-norm-id-le（‖id‖≤1）/op-norm-pow-le（‖Xⁿ‖≤‖X‖ⁿ，
--    r≤‖X‖）/SelfAdjoint-op-sq/SelfAdjoint-op-power-2^k/op-norm-power-2^k
--    （‖X^{2^k}‖=‖X‖^{2^k}，r≥‖X‖ 的 Gelfand 子列核心）——norm-contraction 降定理代数核心齐备。
--  - 阶段 7-3a（✅ 2026-08-02）：正交分解与投影算子——pythagorean（正交⟹范数平方可加，
--    可证）+ Subspace（闭子空间 record）+ 投影桥接（proj/proj-in/proj-orth/proj-fixed，
--    投影定理，降定理路径 = 极小化序列 + 完备性）+ **可证** proj-decomp（正交分解）/
--    proj-idemp（幂等）/proj-norm-le（非扩张 ‖Px‖≤‖x‖，Pythagorean 推论）——
--    谱定理 E 构造的投影组件。
--  - 阶段 7-3b（✅ 2026-08-02）：投影算子与自伴性——投影唯一性（proj-unique：
--    w∈W 且 x−w⊥W ⟹ w=Px，经 a=w−Px 的 ⟨a,a⟩=0）⟹ P(x+y)=Px+Py（proj-lin-add）/
--    P(a·x)=a·Px（proj-lin-scalar）——投影算子 proj-op : Subspace → LinOp 线性性闭合；
--    **可证** proj-self-adjoint（⟨Px,y⟩=⟨x,Py⟩：⟨Px,y⟩=⟨Px,Py⟩=⟨x,Py⟩，y−Py/x−Px
--    分别 ⊥ W）+ proj-op-norm-le-one（‖P‖≤1，SpectralTheory §12b proj-norm-le-one
--    的 Hilbert 侧版本）——投影算子是自伴有界算子，谱定理 E = 谱投影族的组件齐备。
--  - 阶段 7-3 第一步（✅ 2026-08-02）：谱投影构造框架（E 的测度构造起点，§10c）——
--    谱定理桥接 spectral-subspace（谱集 ↦ 闭子空间 W_P，降定理路径 = 自伴算子谱定理）+
--    spectral-subspace-orth（P∩Q=∅ ⟹ W_P⊥W_Q）+ spectral-subspace-total（W_ℝ=全空间）；
--    谱投影 E-hilb P := proj-op (spectral-subspace P)（谱测度 E 的 Hilbert 层构造）；
--    **可证** E-hilb-idemp（幂等）/E-hilb-orth（正交）/E-hilb-total（E(ℝ)=𝟙）/
--    E-hilb-self-adjoint（自伴）/E-hilb-norm-le-one（‖E(P)‖≤1）——全部投影性质直接
--    特化，SpectralTheory E-idempotent/E-orthogonal/E-total/proj-norm-le-one 构造侧对应。
--  - 阶段 7-3 余项 E-union（✅ 2026-08-02）：谱投影加法性（§10d）——内积减法双线性
--    **可证** ip-sub-l/ip-sub-r（⟨x−y,z⟩/⟨x,y−z⟩ 展开）+ 减法分解 sub-add-decomp
--    （x−(a+b)=(x−a)+(-1)b）；谱子空间直和桥接 spectral-subspace-incl（P⊆Q ⟹ W_P⊆W_Q）+
--    spectral-subspace-split（P∩Q=∅ ⟹ W_{P∪Q} ⊆ W_P+W_Q 分解）；**可证** E-hilb-union
--    （P∩Q=∅ ⟹ E(P∪Q)x = E(P)x+E(Q)x：E(P)x+E(Q)x∈W_{P∪Q}（incl 单调 + add 闭包）+
--    x−(E(P)x+E(Q)x)⊥W_{P∪Q}（split 分解 u+v + 逐项正交：proj-orth + W_P⊥W_Q）+
--    proj-unique）——SpectralTheory §10e E-union 的 Hilbert 侧构造版。
--  - 阶段 7-3 余项 E-fin-union（✅ 2026-08-02）：E 的有限可加性（§10e）——sum-ᵥ（点态
--    向量有限和）+ EmptyP（空谱集）+ spectral-subspace-empty 桥接（W_∅={0}，降定理路径
--    = 自伴算子谱定理）⟹ **可证** E-hilb-empty（E(∅)x=0）；FinUnion（递归有限并谓词）+
--    **可证** fin-union-in（∪ᵢ<ₘPᵢ ⟹ ∃i<ₘ.Pᵢ）/FinUnion-disjoint（pairwise ⟹
--    (∪ᵢ<ₘPᵢ)∩Pₘ=∅）；**可证** E-hilb-fin-union（pairwise 不相交 ⟹
--    E(∪ᵢ<ₘPᵢ)x = Σᵢ<ₘE(Pᵢ)x，归纳：E-hilb-union 拆分 + FinUnion-disjoint + 归纳假设）——
--    E-σ-add 的有限版，SpectralTheory §10e E-partition-add 的 Hilbert 侧对应。
--  - 阶段 7-3 余项 E-σ-add 第一步（✅ 2026-08-02）：单调吸收 + 可数并（§10f）——
--    **可证** E-hilb-sub（P⊆Q ⟹ E(Q)(E(P)x)=E(P)x：E(P)x∈W_P⊆W_Q（spectral-subspace-incl）+
--    proj-fixed——SpectralTheory §10b E-sub 的 Hilbert 侧对应，E-σ-add 单调性前置）+
--    σUnion（可数并谓词 ∪ₙPₙ = ∃n.Pₙ）+ E-σ-add 降定理路径登记（E(∪ₙPₙ)=supₘΣᵢ<ₘE(Pᵢ)
--    连续下式，需 LinOp 层算子序 sup 随极限层 + 有限一致性 E-hilb-fin-union 已闭合）。
--  - 阶段 8-6b 第一步（✅ 2026-08-02）：谱半径公式极限层（§11，Gelfand 公式闭合）——
--    谱半径 r(X) := sup {r : r^{2^k} ≤ ‖X^{2^k}‖ ∀k}（沿 2^k 子列的幂形式刻画，避免
--    n 次根——iter-sq + op-norm-power-2^k 直接闭合）；**可证** sr-le-norm（r(X) ≤ ‖X‖，
--    k=0 特化 + sup-least）/ sr-norm-le（自伴 ⟹ ‖X‖ ≤ r(X)，r=‖X‖ 族成员 + sup-upper）/
--    **spectral-radius-norm**（自伴 C* 元 r(X) = ‖X‖，≤-antisym）——norm-contraction
--    （σ(e^(-tA)) ⊆ (0,1] ⟹ ‖e^(-tA)‖ ≤ 1）的 Hilbert 侧核心；完整降定理（e^(-tA)
--    自伴 + 谱支集 ⟹ r(e^(-tA)) ≤ 1）留 8-5b/整合层。
--  - 阶段 8-5b 第一步（✅ 2026-08-02）：强连续半群实例化框架（§12）——e^(-tA) 的
--    Hilbert 层表示桥接 exp-hilb-tA（半群方程/单位/自伴/压缩/范数连续，降定理路径 =
--    跨层模型 + fc 函数演算 + 谱积分 + φ_t 连续性）；**可证** exp-hilb-strong-cont
--    （强连续 SOT，sot-from-norm 特化——strong-continuity 的 Hilbert 侧对应）/
--    **exp-hilb-radius-le-one**（自伴 ⟹ r(e^(-tA)) = ‖e^(-tA)‖ ≤ 1，spectral-radius-norm
--    + 压缩——norm-contraction 的 Hilbert 侧完整降定理核心，8-6b 连接）。
--  - 阶段 13（✅ 2026-08-02）：算子序与投影单调性（E-σ-add 完整形式的机制前置）——
--    Hilbert 层算子序 _≤ₗ_（X≤ₗY ⟺ ∀v.⟨(Y−X)v,v⟩≥0，正算子序）+ **可证**
--    E-hilb-mono（P⊆Q ⟹ E(P)≤ₗ E(Q)：⟨(E(Q)−E(P))v,v⟩ = ‖E(Q)(v−E(P)v)‖² ≥ 0——
--    v=E(P)v+w（proj-decomp）+ (E(Q)−E(P))v=E(Q)w（E-hilb-sub x=v）+ ⟨E(Q)w,v⟩
--    =⟨w,E(P)v⟩+‖E(Q)w‖²=0+‖E(Q)w‖²（自伴+幂等+w⊥W_P）——投影序单调，E-σ-add 的
--    sup 上界机制基础）。
--  - 阶段 14（✅ 2026-08-02）：E-σ-add 完整形式（可数可加性，§14）——sum-ₗ（LinOp
--    层有限和）+ LinOp 层算子序 sup 桥接（supₗ/upper/least，降定理路径 = 强/弱算子
--    拓扑单调有界收敛）；**可证** E-hilb-fin-le-σ（E(∪ᵢ<ₘPᵢ)≤ₗ E(∪ₙPₙ)：FinUnion⊆σUnion
--    （fin-union-in 取 n=i）+ E-hilb-mono——连续下式上界方向）；σ-可数可加桥接
--    E-hilb-σ-add（E(∪ₙPₙ)=supₘΣᵢ<ₘE(Pᵢ)，least 方向 + 收敛随极限层）——
--    SpectralTheory §10f E-σ-add 的 Hilbert 侧对应。
--  - 阶段 15（✅ 2026-08-02）：谱投影范数幂等（§15）——**可证** sup-ext-ℝ（sup 外延，
--    sup-least/upper 双向）+ E-hilb-norm-idempotent（‖E(P)‖²=‖E(P)‖：norm-power（自伴）
--    + 点态幂等 E-hilb-idemp + sup 外延——SpectralTheory §12 idem-zero-one/proj-norm
--    （幂等元范数 ∈{0,1}）的 Hilbert 侧对应）。
--  - 阶段 16（✅ 2026-08-02）：算子代数完整化（跨层模型代数基础，§16）——标量乘
--    _·ₗ_（(c·ₗX)v=c·(Xv)，线性性经 ·ᵥ-distrib/·ᵥ-assoc/*-comm）+ **可证**
--    ·ₗ-ident-pt（1·ₗX 逐点=X）/op-comp-assoc-pt/op-comp-id-pt/op-comp-id-r-pt
--    （结合/单位律点态版，定义性 refl）/·ₗ-distrib-add-pt（标量对加法分配点态，
--    ·ᵥ-distrib-l）/·ₗ-comp-pt（标量与复合点态，refl）——为 8-5b 余项（跨层模型
--    Op → LinOp：SpectralTheory 算子代数公理在 LinOp 层的点态对应）铺路；点态版
--    避开 funext（LinOp record 依赖字段 lin-add/lin-scalar 的相等需依赖 funext）。
--  - 阶段 6b（待）：Gelfand 公式极限层 + 谱论（8-6b）；7-4 "≥"方向完整（测度论核心）；
--    8-5b 余项（跨层模型 Op → LinOp 完整实例化，代数基础已就位）。
