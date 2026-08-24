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

module DHStructural.DHStructuralAnalysis where

{-
  B4: d_H 结构分析与不等式链
  ==============================
  对应 Lean: DHStructuralAnalysis.lean

  核心不等式链：ln 15 < 65/24 < e < 3

  说明：Lean 版本通过 Real.exp_one_gt_d9 / Real.exp_one_lt_d9 机器证明。
  Agda 版本在无标准实数库下，将 ℝ 作为公理类型声明，
  不等式链作为定理陈述（交叉验证 Lean 的定理签名）。
-}

open import Agda.Builtin.Equality using (_≡_; refl)
open import Sp.SpCategory using (ℕ; zero; suc; _×_; _,_; sym; trans; cong; cong₂)
open import NatArith.NatArith

-- 本地不相交并（库未提供 Agda.Builtin.Sum）
data _⊎_ (A : Set) (B : Set) : Set where
  inj₁ : A → A ⊎ B
  inj₂ : B → A ⊎ B

-- 本地 ⊥（库未提供）
data ⊥ : Set where

⊥-elim : {A : Set} → ⊥ → A
⊥-elim ()

-- 本地 subst（库未提供）
subst : {A : Set} {x y : A} (P : A → Set) → x ≡ y → P x → P y
subst P refl p = p

-- ==================================================================
-- §0 实数公理类型
-- ==================================================================

-- ℝ 作为公理类型（不依赖标准库）
postulate
  ℝ : Set

-- 基本运算
postulate
  _+ℝ_ : ℝ → ℝ → ℝ
  _*ℝ_ : ℝ → ℝ → ℝ
  _-ℝ_ : ℝ → ℝ → ℝ
  _/ℝ_ : ℝ → ℝ → ℝ
  _<ℝ_ : ℝ → ℝ → Set
  _≤ℝ_ : ℝ → ℝ → Set
  zeroℝ : ℝ
  oneℝ  : ℝ
  neg-oneℝ : ℝ  -- -1
  negℝ : ℝ → ℝ  -- 一般取负：negℝ x = -x
  natℝ  : ℕ → ℝ  -- 自然数嵌入

-- 实数的合理公理（简化声明）
postulate
  trans-<ℝ : {x y z : ℝ} → x <ℝ y → y <ℝ z → x <ℝ z
  refl-≤ℝ : {x : ℝ} → x ≤ℝ x

-- T3 阶段 0：序代数基础（2026-07-31）
-- 蓝图：notes/00_foundations/spectral_T3_analysis_foundation.md
-- 登记为基础假设（对齐路线图"ℝ 公理体系是基础假设，不计入闭合账目"立场）。
-- 用途：阶段 2 闭合 65/24 < e < 3（exp 级数截断）需要 0<1、乘正性（1/n! > 0）、
--       部分和比较（≤-混合传递）。natℝ 保序嵌入留待阶段 1（依赖 ℕ 序）。
postulate
  zero-lt-one-ℝ : zeroℝ <ℝ oneℝ
  lt-+-mono-ℝ : {a b c d : ℝ} → a <ℝ b → c <ℝ d → (a +ℝ c) <ℝ (b +ℝ d)
  lt-*-pos-ℝ : {a b : ℝ} → zeroℝ <ℝ a → zeroℝ <ℝ b → zeroℝ <ℝ (a *ℝ b)
  lt-≤-trans-ℝ : {x y z : ℝ} → x <ℝ y → y ≤ℝ z → x <ℝ z
  ≤-lt-trans-ℝ : {x y z : ℝ} → x ≤ℝ y → y <ℝ z → x <ℝ z

-- ==================================================================
-- §0.5 T3 阶段 1：ℝ 域公理与 e 的部分和基础（2026-07-31）
-- 蓝图：notes/00_foundations/spectral_T3_analysis_foundation.md
-- 域公理/保序嵌入/除法正性/加正增量登记为基础假设（对齐
-- "ℝ 公理体系是基础假设，不计入闭合账目"立场）；
-- 阶乘/部分和/递增性为可证明结构引理，为阶段 2 闭合 65/24<e<3 铺路。
-- ==================================================================

postulate
  +-assoc-ℝ : (x y z : ℝ) → (x +ℝ y) +ℝ z ≡ x +ℝ (y +ℝ z)
  +-comm-ℝ : (x y : ℝ) → x +ℝ y ≡ y +ℝ x
  +-ident-ℝ : (x : ℝ) → x +ℝ zeroℝ ≡ x
  +-inv-ℝ : (x : ℝ) → x +ℝ negℝ x ≡ zeroℝ
  *-assoc-ℝ : (x y z : ℝ) → (x *ℝ y) *ℝ z ≡ x *ℝ (y *ℝ z)
  *-comm-ℝ : (x y : ℝ) → x *ℝ y ≡ y *ℝ x
  *-ident-ℝ : (x : ℝ) → x *ℝ oneℝ ≡ x
  distrib-ℝ : (x y z : ℝ) → x *ℝ (y +ℝ z) ≡ (x *ℝ y) +ℝ (x *ℝ z)
  natℝ-+ : (m n : ℕ) → natℝ (m +ℕ n) ≡ natℝ m +ℝ natℝ n
  natℝ-* : (m n : ℕ) → natℝ (m *ℕ n) ≡ natℝ m *ℝ natℝ n
  natℝ-suc : (n : ℕ) → natℝ (suc n) ≡ natℝ n +ℝ oneℝ
  natℝ-pos-embed : {n : ℕ} → 0 <ℕ n → zeroℝ <ℝ natℝ n
  natℝ-one : natℝ 1 ≡ oneℝ
  natℝ-<-embed : {m n : ℕ} → m <ℕ n → natℝ m <ℝ natℝ n
  /-pos-ℝ : {a b : ℝ} → zeroℝ <ℝ a → zeroℝ <ℝ b → zeroℝ <ℝ (a /ℝ b)
  add-pos-ℝ : {x y : ℝ} → zeroℝ <ℝ y → x <ℝ (x +ℝ y)
  -- 倒数严格单调（阶段 2 几何上界所需，基础假设）
  recip-mono-ℝ : {a b : ℝ} → zeroℝ <ℝ a → a <ℝ b → (oneℝ /ℝ b) <ℝ (oneℝ /ℝ a)
  -- 分数加法法则与交叉相乘消去（阶段 2 通分所需，基础假设）
  /-add-ℝ : (a b c d : ℝ) → (a /ℝ c) +ℝ (b /ℝ d) ≡ ((a *ℝ d) +ℝ (b *ℝ c)) /ℝ (c *ℝ d)
  /-cross-ℝ : {a b c d : ℝ} → (a *ℝ d) ≡ (b *ℝ c) → (a /ℝ c) ≡ (b /ℝ d)
  -- T3 阶段 2 补充（e < 3 统一上界所需，基础假设）：
  -- 标量并入分子 / x/1 = x / 加法右单调 / 同分母比较 / 严格蕴含非严格
  *-/ℝ : (a b c : ℝ) → (a *ℝ (b /ℝ c)) ≡ ((a *ℝ b) /ℝ c)
  div-one-ℝ : (x : ℝ) → (x /ℝ oneℝ) ≡ x
  lt-+-mono-r-ℝ : {a b c : ℝ} → b <ℝ c → (a +ℝ b) <ℝ (a +ℝ c)
  /-lt-same-den-ℝ : {a b c : ℝ} → a <ℝ b → (a /ℝ c) <ℝ (b /ℝ c)
  <-≤-ℝ : {x y : ℝ} → x <ℝ y → x ≤ℝ y

-- 阶乘（ℕ 层）
factorial : ℕ → ℕ
factorial zero = 1
factorial (suc n) = (suc n) *ℕ factorial n

-- 阶乘恒正：0 <ℕ n!（case factorial m，经等式 e 传递到目标）
factorial-pos : (n : ℕ) → 0 <ℕ factorial n
factorial-pos zero = z<s
factorial-pos (suc n) = helper n (factorial-pos n)
  where
  helper : (m : ℕ) → 0 <ℕ factorial m → 0 <ℕ factorial (suc m)
  helper m h = case-fact m (factorial m) h refl
    where
    case-fact : (m : ℕ) (f : ℕ) → 0 <ℕ f → f ≡ factorial m → 0 <ℕ factorial (suc m)
    case-fact m zero ()
    case-fact m (suc k) z<s e =
      subst (λ x → 0 <ℕ ((suc m) *ℕ x)) e z<s

-- ==================================================================
-- ℕ 层保序引理库（T3 阶段 2 几何上界地基，2026-07-31）
-- 用途：factorial-2^（2^{k-1} ≤ k!）⟹ 1/k! ≤ 1/2^{k-1} ⟹ e < 3。
-- ==================================================================

-- suc 严格单调之逆
s<s-inj : {a b : ℕ} → suc a <ℕ suc b → a <ℕ b
s<s-inj (s<s h) = h

-- +ℕ 保序（左参数）
+ℕ-<-mono-l : {a b c : ℕ} → a <ℕ b → (c +ℕ a) <ℕ (c +ℕ b)
+ℕ-<-mono-l {c = zero}  h = h
+ℕ-<-mono-l {c = suc c} h = s<s (+ℕ-<-mono-l {c = c} h)

-- +ℕ 保序（右参数）
+ℕ-<-mono-r : {a b c : ℕ} → a <ℕ b → (a +ℕ c) <ℕ (b +ℕ c)
+ℕ-<-mono-r {a} {b} {zero} h =
  subst (λ x → x <ℕ (b +ℕ zero)) (sym (+ℕ-zero a))
        (subst (λ y → a <ℕ y) (sym (+ℕ-zero b)) h)
+ℕ-<-mono-r {a} {b} {suc c} h =
  subst (λ x → x <ℕ (b +ℕ suc c)) (sym (+ℕ-suc a c))
        (subst (λ y → suc (a +ℕ c) <ℕ y) (sym (+ℕ-suc b c))
               (s<s (+ℕ-<-mono-r {a} {b} {c} h)))

-- +ℕ 双参数保序
+ℕ-<-mono : {a b c d : ℕ} → a <ℕ b → c <ℕ d → (a +ℕ c) <ℕ (b +ℕ d)
+ℕ-<-mono {b = b} h1 h2 = <-trans (+ℕ-<-mono-r h1) (+ℕ-<-mono-l {c = b} h2)

-- *ℕ 保序（左参数严格）
*ℕ-<-mono-l : {a b c : ℕ} → a <ℕ b → 0 <ℕ c → (c *ℕ a) <ℕ (c *ℕ b)
*ℕ-<-mono-l {c = zero}  h ()
*ℕ-<-mono-l {a} {b} {suc zero} h z<s = +ℕ-<-mono-r {a} {b} {zero} h
*ℕ-<-mono-l {a} {b} {suc (suc c)} h z<s =
  +ℕ-<-mono h (*ℕ-<-mono-l {a} {b} {suc c} h z<s)

-- *ℕ 保序（右参数严格）
*ℕ-<-mono-r : {a b c : ℕ} → a <ℕ b → 0 <ℕ c → (a *ℕ c) <ℕ (b *ℕ c)
*ℕ-<-mono-r {zero} {zero} {c} () hc
*ℕ-<-mono-r {zero} {suc b} {zero} h ()
*ℕ-<-mono-r {zero} {suc b} {suc c} h z<s = z<s
*ℕ-<-mono-r {suc a} {suc b} {c} h hc =
  +ℕ-<-mono-l {c = c} (*ℕ-<-mono-r {a} {b} {c} (s<s-inj h) hc)

-- 2 < 4+m（m ≥ 0）
2-lt-4m : (m : ℕ) → 2 <ℕ (suc (suc (suc (suc m))))
2-lt-4m m = s<s (s<s z<s)

-- 2 的幂 < 阶乘：2^{k-1} <ℕ k!（k ≥ 3）
factorial-2^ : (m : ℕ) → (2^ (suc (suc m))) <ℕ (factorial (suc (suc (suc m))))
factorial-2^ zero = s<s (s<s (s<s (s<s z<s)))
factorial-2^ (suc m) =
  <-trans
    (*ℕ-<-mono-l {2^ (suc (suc m))} {factorial (suc (suc (suc m)))} {2} (factorial-2^ m) z<s)
    (*ℕ-<-mono-r {2} {suc (suc (suc (suc m)))} {factorial (suc (suc (suc m)))}
                 (2-lt-4m m) (factorial-pos (suc (suc (suc m)))))

-- 2 的幂恒正：0 <ℕ 2^n
2^-pos : (n : ℕ) → 0 <ℕ 2^ n
2^-pos zero = z<s
2^-pos (suc n) = helper n (2^-pos n)
  where
  helper : (n : ℕ) → 0 <ℕ 2^ n → 0 <ℕ (2 *ℕ 2^ n)
  helper n h with 2^ n
  helper n h | suc k = z<s

-- 单位分数 1/n!
recip-factorial : ℕ → ℝ
recip-factorial n = natℝ 1 /ℝ natℝ (factorial n)

-- 单位分数恒正：0 < 1/n!
recip-factorial-pos : (n : ℕ) → zeroℝ <ℝ recip-factorial n
recip-factorial-pos n =
  /-pos-ℝ (subst (zeroℝ <ℝ_) (sym natℝ-one) zero-lt-one-ℝ)
          (natℝ-pos-embed (factorial-pos n))

-- e 的部分和：Σ_{k=0}^n 1/k!
partial-e : ℕ → ℝ
partial-e zero = recip-factorial zero
partial-e (suc n) = partial-e n +ℝ recip-factorial (suc n)

-- 部分和严格递增：s_{n+1} = s_n + 1/(n+1)! > s_n
partial-e-suc : (n : ℕ) → partial-e n <ℝ partial-e (suc n)
partial-e-suc n = add-pos-ℝ (recip-factorial-pos (suc n))

-- ==================================================================
-- ℝ 层几何上界（T3 阶段 2，2026-07-31）
-- 1/k! < 1/2^{k-1}（k ≥ 3）：经 factorial-2^ + natℝ 保序 + 倒数单调。
-- ==================================================================

-- 1/2^n（几何级数项）
recip-half : ℕ → ℝ
recip-half n = natℝ 1 /ℝ natℝ (2^ n)

-- 1/k! < 1/2^{k-1}（k = 3+m）
recip-factorial-<-half : (m : ℕ) → recip-factorial (suc (suc (suc m))) <ℝ recip-half (suc (suc m))
recip-factorial-<-half m =
  subst (λ y → (natℝ 1 /ℝ F) <ℝ y)
        (sym (cong (λ z → z /ℝ H) natℝ-one))
        (subst (λ x → x <ℝ (oneℝ /ℝ H))
               (sym (cong (λ z → z /ℝ F) natℝ-one))
               (recip-mono-ℝ ha hab))
  where
  F = natℝ (factorial (suc (suc (suc m))))
  H = natℝ (2^ (suc (suc m)))
  ha : zeroℝ <ℝ H
  ha = natℝ-pos-embed (2^-pos (suc (suc m)))
  hab : H <ℝ F
  hab = natℝ-<-embed (factorial-2^ m)

-- ==================================================================
-- 部分和计算：partial-e 4 ≡ 65/24（T3 阶段 2，2026-07-31）
-- 经 /-add-ℝ 通分（1/1+1/1=2/1 → +1/2=5/2 → +1/6=32/12 → +1/24=780/288）
-- + /-cross-ℝ 交叉相乘（780·24=288·65）；
-- 化简用 natℝ-*/-+ 的 ℕ 层定义性（如 2*ℕ2=4），无需展开 natℝ 具体值。
-- ==================================================================
partial-e-4-value : partial-e 4 ≡ (natℝ 65 /ℝ natℝ 24)
partial-e-4-value =
  trans
    (cong (λ x → ((x +ℝ r2) +ℝ r3) +ℝ r4) inner1)
    (trans
      (cong (λ x → (x +ℝ r3) +ℝ r4) inner2)
      (trans
        (cong (λ x → x +ℝ r4) inner3)
        (trans inner4 (/-cross-ℝ cross))))
  where
  r0 : ℝ
  r0 = natℝ 1 /ℝ natℝ 1
  r1 : ℝ
  r1 = natℝ 1 /ℝ natℝ 1
  r2 : ℝ
  r2 = natℝ 1 /ℝ natℝ 2
  r3 : ℝ
  r3 = natℝ 1 /ℝ natℝ 6
  r4 : ℝ
  r4 = natℝ 1 /ℝ natℝ 24
  -- 1/1 + 1/1 = 2/1
  inner1 : r0 +ℝ r1 ≡ (natℝ 2 /ℝ natℝ 1)
  inner1 = trans (/-add-ℝ (natℝ 1) (natℝ 1) (natℝ 1) (natℝ 1))
                 (cong₂ _/ℝ_ m1 d1)
    where
    m1 : (natℝ 1 *ℝ natℝ 1) +ℝ (natℝ 1 *ℝ natℝ 1) ≡ natℝ 2
    m1 = trans (cong₂ _+ℝ_ (sym (natℝ-* 1 1)) (sym (natℝ-* 1 1))) (sym (natℝ-+ 1 1))
    d1 : natℝ 1 *ℝ natℝ 1 ≡ natℝ 1
    d1 = sym (natℝ-* 1 1)
  -- 2/1 + 1/2 = 5/2
  inner2 : (natℝ 2 /ℝ natℝ 1) +ℝ r2 ≡ (natℝ 5 /ℝ natℝ 2)
  inner2 = trans (/-add-ℝ (natℝ 2) (natℝ 1) (natℝ 1) (natℝ 2))
                 (cong₂ _/ℝ_ m2 d2)
    where
    m2 : (natℝ 2 *ℝ natℝ 2) +ℝ (natℝ 1 *ℝ natℝ 1) ≡ natℝ 5
    m2 = trans (cong₂ _+ℝ_ (sym (natℝ-* 2 2)) (sym (natℝ-* 1 1))) (sym (natℝ-+ 4 1))
    d2 : natℝ 1 *ℝ natℝ 2 ≡ natℝ 2
    d2 = sym (natℝ-* 1 2)
  -- 5/2 + 1/6 = 32/12
  inner3 : (natℝ 5 /ℝ natℝ 2) +ℝ r3 ≡ (natℝ 32 /ℝ natℝ 12)
  inner3 = trans (/-add-ℝ (natℝ 5) (natℝ 1) (natℝ 2) (natℝ 6))
                 (cong₂ _/ℝ_ m3 d3)
    where
    m3 : (natℝ 5 *ℝ natℝ 6) +ℝ (natℝ 1 *ℝ natℝ 2) ≡ natℝ 32
    m3 = trans (cong₂ _+ℝ_ (sym (natℝ-* 5 6)) (sym (natℝ-* 1 2))) (sym (natℝ-+ 30 2))
    d3 : natℝ 2 *ℝ natℝ 6 ≡ natℝ 12
    d3 = sym (natℝ-* 2 6)
  -- 32/12 + 1/24 = 780/288
  inner4 : (natℝ 32 /ℝ natℝ 12) +ℝ r4 ≡ (natℝ 780 /ℝ natℝ 288)
  inner4 = trans (/-add-ℝ (natℝ 32) (natℝ 1) (natℝ 12) (natℝ 24))
                 (cong₂ _/ℝ_ m4 d4)
    where
    m4 : (natℝ 32 *ℝ natℝ 24) +ℝ (natℝ 1 *ℝ natℝ 12) ≡ natℝ 780
    m4 = trans (cong₂ _+ℝ_ (sym (natℝ-* 32 24)) (sym (natℝ-* 1 12))) (sym (natℝ-+ 768 12))
    d4 : natℝ 12 *ℝ natℝ 24 ≡ natℝ 288
    d4 = sym (natℝ-* 12 24)
  -- 780/288 = 65/24（交叉相乘：780·24 = 65·288）
  cross : (natℝ 780 *ℝ natℝ 24) ≡ (natℝ 65 *ℝ natℝ 288)
  cross =
    trans
      (sym (cong₂ _*ℝ_ (sym (natℝ-* 65 12)) refl))
      (trans (*-assoc-ℝ (natℝ 65) (natℝ 12) (natℝ 24))
             (cong (λ x → natℝ 65 *ℝ x) (sym (natℝ-* 12 24))))

-- 部分和计算：partial-e 5 ≡ 163/60（T3 阶段 4，2026-07-31）
-- 经 partial-e-4-value + /-add-ℝ 通分（65/24 + 1/120 = 7824/2880）+ 交叉相乘
-- （7824·60 = 163·2880）
partial-e-5-value : partial-e 5 ≡ (natℝ 163 /ℝ natℝ 60)
partial-e-5-value =
  trans (cong (λ x → x +ℝ recip-factorial 5) partial-e-4-value)
        (trans (cong₂ _+ℝ_ refl (recip-factorial-5))
               (trans (/-add-ℝ (natℝ 65) (natℝ 1) (natℝ 24) (natℝ 120))
                      (trans (cong₂ _/ℝ_ sum-7824 den-2880) (/-cross-ℝ cross))))
  where
  recip-factorial-5 : recip-factorial 5 ≡ (natℝ 1 /ℝ natℝ 120)
  recip-factorial-5 = refl
  -- 65·120 + 1·24 = 7824；24·120 = 2880
  sum-7824 : ((natℝ 65 *ℝ natℝ 120) +ℝ (natℝ 1 *ℝ natℝ 24)) ≡ natℝ 7824
  sum-7824 = trans (sym (cong₂ _+ℝ_ (natℝ-* 65 120) (natℝ-* 1 24))) (sym (natℝ-+ 7800 24))
  den-2880 : (natℝ 24 *ℝ natℝ 120) ≡ natℝ 2880
  den-2880 = sym (natℝ-* 24 120)
  -- 7824/2880 = 163/60（交叉相乘：7824·60 = 163·2880）
  cross : (natℝ 7824 *ℝ natℝ 60) ≡ (natℝ 163 *ℝ natℝ 2880)
  cross = trans (sym (natℝ-* 7824 60)) (natℝ-* 163 2880)

-- ==================================================================
-- e < 3 统一上界（T3 阶段 2，2026-07-31）
-- 策略：partial-e n < 67/24 < 3（固定间隙，sup 层保持严格）。
--   1/k! < 1/2^k（k ≥ 4，ℕ 层 factorial-2^-4：2^k < k!）⟹
--   Σ_{k=4}^n 1/k! < Σ_{k=4}^n 1/2^k < 1/8（geo4-ident 闭式）⟹
--   partial-e n < partial-e 3 + 1/8 = 8/3 + 1/8 = 67/24
--   ⟹（exp-least-ub）exp 1 ≤ 67/24 < 3。
-- ==================================================================

-- 2 < 5+m
2-lt-5m : (m : ℕ) → 2 <ℕ (suc (suc (suc (suc (suc m)))))
2-lt-5m m = s<s (s<s z<s)

-- 2 的幂 < 阶乘：2^k <ℕ k!（k ≥ 4，归纳：base 4<6 乘 4，step 2·2^k < 2·k! < (k+1)·k!）
factorial-2^-4 : (m : ℕ) → (2^ (suc (suc (suc (suc m))))) <ℕ (factorial (suc (suc (suc (suc m)))))
factorial-2^-4 zero =
  *ℕ-<-mono-r {2^ (suc (suc zero))} {factorial (suc (suc (suc zero)))} {2^ (suc (suc zero))}
              (factorial-2^ zero) (2^-pos (suc (suc zero)))
factorial-2^-4 (suc m) =
  <-trans
    (*ℕ-<-mono-l {2^ (suc (suc (suc (suc m))))} {factorial (suc (suc (suc (suc m))))} {2}
                 (factorial-2^-4 m) z<s)
    (*ℕ-<-mono-r {2} {suc (suc (suc (suc (suc m))))} {factorial (suc (suc (suc (suc m))))}
                 (2-lt-5m m) (factorial-pos (suc (suc (suc (suc m))))))

-- 1/k! < 1/2^k（k = 4+m）
recip-factorial-<-half4 : (m : ℕ) → recip-factorial (suc (suc (suc (suc m)))) <ℝ recip-half (suc (suc (suc (suc m))))
recip-factorial-<-half4 m =
  subst (λ y → (natℝ 1 /ℝ F) <ℝ y)
        (sym (cong (λ z → z /ℝ H) natℝ-one))
        (subst (λ x → x <ℝ (oneℝ /ℝ H))
               (sym (cong (λ z → z /ℝ F) natℝ-one))
               (recip-mono-ℝ ha hab))
  where
  F = natℝ (factorial (suc (suc (suc (suc m)))))
  H = natℝ (2^ (suc (suc (suc (suc m)))))
  ha : zeroℝ <ℝ H
  ha = natℝ-pos-embed (2^-pos (suc (suc (suc (suc m)))))
  hab : H <ℝ F
  hab = natℝ-<-embed (factorial-2^-4 m)

-- 1/2^n 恒正：0 < 1/2^n
recip-half-pos : (n : ℕ) → zeroℝ <ℝ recip-half n
recip-half-pos n =
  /-pos-ℝ (subst (zeroℝ <ℝ_) (sym natℝ-one) zero-lt-one-ℝ)
          (natℝ-pos-embed (2^-pos n))

-- natℝ 2 = 1 + 1
natℝ-2≡1+1 : natℝ 2 ≡ oneℝ +ℝ oneℝ
natℝ-2≡1+1 = trans (natℝ-suc 1) (cong (λ x → x +ℝ oneℝ) natℝ-one)

-- a + a = 2·a
dbl : (a : ℝ) → a +ℝ a ≡ (natℝ 2) *ℝ a
dbl a =
  trans
    (trans (cong₂ _+ℝ_ (sym (*-ident-ℝ a)) (sym (*-ident-ℝ a)))
           (sym (distrib-ℝ a oneℝ oneℝ)))
    (trans (*-comm-ℝ a (oneℝ +ℝ oneℝ))
           (cong (λ x → x *ℝ a) (sym natℝ-2≡1+1)))

-- 1/2^{n+1} + 1/2^{n+1} = 1/2^n
dbl-recip : (n : ℕ) → recip-half (suc n) +ℝ recip-half (suc n) ≡ recip-half n
dbl-recip n =
  trans (dbl (recip-half (suc n)))
        (trans (*-/ℝ (natℝ 2) (natℝ 1) (natℝ (2^ (suc n))))
               (trans (cong₂ _/ℝ_ n2-1 refl) (/-cross-ℝ cross)))
  where
  n2-1 : (natℝ 2 *ℝ natℝ 1) ≡ natℝ 2
  n2-1 = trans (sym (natℝ-* 2 1)) refl
  cross : (natℝ 2 *ℝ natℝ (2^ n)) ≡ (natℝ 1 *ℝ natℝ (2^ (suc n)))
  cross = trans (sym (natℝ-* 2 (2^ n)))
          (trans (cong natℝ (sym (+ℕ-zero (2^ (suc n)))))
                 (natℝ-* 1 (2^ (suc n))))

-- 几何尾部：geo4 m = Σ_{k=4}^{4+m} 1/2^k
geo4 : ℕ → ℝ
geo4 zero = recip-half 4
geo4 (suc m) = geo4 m +ℝ recip-half (suc (suc (suc (suc (suc m)))))

-- 闭式：geo4 m + 1/2^{4+m} = 1/8
geo4-ident : (m : ℕ) → geo4 m +ℝ recip-half (suc (suc (suc (suc m)))) ≡ recip-half 3
geo4-ident zero = dbl-recip 3
geo4-ident (suc m) =
  trans (+-assoc-ℝ (geo4 m) r r)
        (trans (cong (λ x → geo4 m +ℝ x) (dbl-recip (suc (suc (suc (suc m))))))
               (geo4-ident m))
  where
  r : ℝ
  r = recip-half (suc (suc (suc (suc (suc m)))))

-- 几何尾部上界：geo4 m < 1/8
geo4-lt-18 : (m : ℕ) → geo4 m <ℝ recip-half 3
geo4-lt-18 m =
  subst (λ z → geo4 m <ℝ z) (geo4-ident m)
        (add-pos-ℝ (recip-half-pos (suc (suc (suc (suc m))))))

-- 阶乘尾部：tail-e4 m = Σ_{k=4}^{4+m} 1/k!
tail-e4 : ℕ → ℝ
tail-e4 zero = recip-factorial 4
tail-e4 (suc m) = tail-e4 m +ℝ recip-factorial (suc (suc (suc (suc (suc m)))))

-- 逐项比较：tail-e4 m < geo4 m
tail-e4-lt-geo4 : (m : ℕ) → tail-e4 m <ℝ geo4 m
tail-e4-lt-geo4 zero = recip-factorial-<-half4 zero
tail-e4-lt-geo4 (suc m) =
  lt-+-mono-ℝ (tail-e4-lt-geo4 m) (recip-factorial-<-half4 (suc m))

-- 部分和计算：partial-e 3 ≡ 8/3（1/1+1/1=2/1 → +1/2=5/2 → +1/6=32/12=8/3）
partial-e-3-value : partial-e 3 ≡ (natℝ 8 /ℝ natℝ 3)
partial-e-3-value =
  trans
    (cong (λ x → (x +ℝ r2) +ℝ r3) inner1)
    (trans
      (cong (λ x → x +ℝ r3) inner2)
      (trans inner3 (/-cross-ℝ cross3)))
  where
  r1 : ℝ
  r1 = natℝ 1 /ℝ natℝ 1
  r2 : ℝ
  r2 = natℝ 1 /ℝ natℝ 2
  r3 : ℝ
  r3 = natℝ 1 /ℝ natℝ 6
  -- 1/1 + 1/1 = 2/1
  inner1 : r1 +ℝ r1 ≡ (natℝ 2 /ℝ natℝ 1)
  inner1 = trans (/-add-ℝ (natℝ 1) (natℝ 1) (natℝ 1) (natℝ 1))
                 (cong₂ _/ℝ_ m1 d1)
    where
    m1 : (natℝ 1 *ℝ natℝ 1) +ℝ (natℝ 1 *ℝ natℝ 1) ≡ natℝ 2
    m1 = trans (cong₂ _+ℝ_ (sym (natℝ-* 1 1)) (sym (natℝ-* 1 1))) (sym (natℝ-+ 1 1))
    d1 : natℝ 1 *ℝ natℝ 1 ≡ natℝ 1
    d1 = sym (natℝ-* 1 1)
  -- 2/1 + 1/2 = 5/2
  inner2 : (natℝ 2 /ℝ natℝ 1) +ℝ r2 ≡ (natℝ 5 /ℝ natℝ 2)
  inner2 = trans (/-add-ℝ (natℝ 2) (natℝ 1) (natℝ 1) (natℝ 2))
                 (cong₂ _/ℝ_ m2 d2)
    where
    m2 : (natℝ 2 *ℝ natℝ 2) +ℝ (natℝ 1 *ℝ natℝ 1) ≡ natℝ 5
    m2 = trans (cong₂ _+ℝ_ (sym (natℝ-* 2 2)) (sym (natℝ-* 1 1))) (sym (natℝ-+ 4 1))
    d2 : natℝ 1 *ℝ natℝ 2 ≡ natℝ 2
    d2 = sym (natℝ-* 1 2)
  -- 5/2 + 1/6 = 32/12
  inner3 : (natℝ 5 /ℝ natℝ 2) +ℝ r3 ≡ (natℝ 32 /ℝ natℝ 12)
  inner3 = trans (/-add-ℝ (natℝ 5) (natℝ 1) (natℝ 2) (natℝ 6))
                 (cong₂ _/ℝ_ m3 d3)
    where
    m3 : (natℝ 5 *ℝ natℝ 6) +ℝ (natℝ 1 *ℝ natℝ 2) ≡ natℝ 32
    m3 = trans (cong₂ _+ℝ_ (sym (natℝ-* 5 6)) (sym (natℝ-* 1 2))) (sym (natℝ-+ 30 2))
    d3 : natℝ 2 *ℝ natℝ 6 ≡ natℝ 12
    d3 = sym (natℝ-* 2 6)
  -- 32/12 = 8/3（交叉相乘：32·3 = 8·12）
  cross3 : (natℝ 32 *ℝ natℝ 3) ≡ (natℝ 8 *ℝ natℝ 12)
  cross3 = trans (sym (natℝ-* 32 3)) (trans (cong natℝ 32·3≡8·12) (natℝ-* 8 12))
    where
    32·3≡8·12 : 32 *ℕ 3 ≡ 8 *ℕ 12
    32·3≡8·12 = refl

-- 分解：partial-e (4+m) = partial-e 3 + tail-e4 m
partial-e-decomp : (m : ℕ) → partial-e (suc (suc (suc (suc m)))) ≡ partial-e 3 +ℝ tail-e4 m
partial-e-decomp zero = refl
partial-e-decomp (suc m) =
  trans (cong (λ x → x +ℝ recip-factorial (suc (suc (suc (suc (suc m)))))) (partial-e-decomp m))
        (+-assoc-ℝ (partial-e 3) (tail-e4 m) (recip-factorial (suc (suc (suc (suc (suc m)))))))

-- 64 < 67（ℕ）
64-lt-67 : 64 <ℕ 67
64-lt-67 = <-trans (<-suc 64) (<-trans (<-suc 65) (<-suc 66))

-- 67 < 72（ℕ）
67-lt-72 : 67 <ℕ 72
67-lt-72 = <-trans (<-suc 67) (<-trans (<-suc 68) (<-trans (<-suc 69) (<-trans (<-suc 70) (<-suc 71))))

-- 8/3 ≡ 64/24
64-24-value : (natℝ 8 /ℝ natℝ 3) ≡ (natℝ 64 /ℝ natℝ 24)
64-24-value = /-cross-ℝ (trans (sym (natℝ-* 8 24)) (trans (cong natℝ 8·24≡64·3) (natℝ-* 64 3)))
  where
  8·24≡64·3 : 8 *ℕ 24 ≡ 64 *ℕ 3
  8·24≡64·3 = refl

-- partial-e 3 < 67/24
p3-lt-67-24 : partial-e 3 <ℝ (natℝ 67 /ℝ natℝ 24)
p3-lt-67-24 =
  subst (λ x → x <ℝ (natℝ 67 /ℝ natℝ 24)) (sym (partial-e-3-value))
    (subst (λ x → x <ℝ (natℝ 67 /ℝ natℝ 24)) (sym 64-24-value)
           (/-lt-same-den-ℝ {natℝ 64} {natℝ 67} {natℝ 24} (natℝ-<-embed 64-lt-67)))

-- 统一上界：partial-e n < 67/24（n ≤ 3 经 partial-e 递增链；n ≥ 4 经尾部比较 + 几何闭式）
partial-e-lt-67-24 : (n : ℕ) → partial-e n <ℝ (natℝ 67 /ℝ natℝ 24)
partial-e-lt-67-24 zero =
  trans-<ℝ (trans-<ℝ (partial-e-suc 0) (trans-<ℝ (partial-e-suc 1) (partial-e-suc 2))) p3-lt-67-24
partial-e-lt-67-24 (suc zero) =
  trans-<ℝ (trans-<ℝ (partial-e-suc 1) (partial-e-suc 2)) p3-lt-67-24
partial-e-lt-67-24 (suc (suc zero)) =
  trans-<ℝ (partial-e-suc 2) p3-lt-67-24
partial-e-lt-67-24 (suc (suc (suc zero))) = p3-lt-67-24
partial-e-lt-67-24 (suc (suc (suc (suc m)))) =
  subst (λ x → x <ℝ (natℝ 67 /ℝ natℝ 24)) (sym (partial-e-decomp m))
    (subst (λ x → (partial-e 3 +ℝ tail-e4 m) <ℝ x) (p3p8-value)
           (trans-<ℝ (lt-+-mono-r-ℝ (tail-e4-lt-geo4 m))
                     (lt-+-mono-r-ℝ (geo4-lt-18 m))))
  where
  p3p8-value : (partial-e 3 +ℝ recip-half 3) ≡ (natℝ 67 /ℝ natℝ 24)
  p3p8-value =
    trans (cong₂ _+ℝ_ (partial-e-3-value) refl)
          (trans (/-add-ℝ (natℝ 8) (natℝ 1) (natℝ 3) (natℝ 8))
                 (cong₂ _/ℝ_ num den))
    where
    num : (natℝ 8 *ℝ natℝ 8) +ℝ (natℝ 1 *ℝ natℝ 3) ≡ natℝ 67
    num = trans (cong₂ _+ℝ_ (sym (natℝ-* 8 8)) (sym (natℝ-* 1 3))) (sym (natℝ-+ 64 3))
    den : (natℝ 3 *ℝ natℝ 8) ≡ natℝ 24
    den = sym (natℝ-* 3 8)

-- 67/24 < 3（= 72/24）
sixtyseven-over-24-lt-3 : (natℝ 67 /ℝ natℝ 24) <ℝ natℝ 3
sixtyseven-over-24-lt-3 =
  subst (λ y → (natℝ 67 /ℝ natℝ 24) <ℝ y) (sym natℝ-3≡72-24)
    (/-lt-same-den-ℝ {natℝ 67} {natℝ 72} {natℝ 24} (natℝ-<-embed 67-lt-72))
  where
  natℝ-3≡72-24 : natℝ 3 ≡ (natℝ 72 /ℝ natℝ 24)
  natℝ-3≡72-24 =
    trans (sym (div-one-ℝ (natℝ 3)))
          (trans (cong (λ x → natℝ 3 /ℝ x) (sym natℝ-one))
                 (/-cross-ℝ (trans (sym (natℝ-* 3 24)) (trans (cong natℝ 3·24≡72·1) (natℝ-* 72 1)))))
    where
    3·24≡72·1 : 3 *ℕ 24 ≡ 72 *ℕ 1
    3·24≡72·1 = refl

-- ==================================================================
-- §1 核心常数
-- ==================================================================

-- 自然对数的底 e = exp(1)
postulate
  e : ℝ
  exp : ℝ → ℝ
  log : ℝ → ℝ
  _^-ℝ_ : ℝ → ℝ → ℝ  -- 实数幂

-- e 的定义：e = exp 1
postulate
  e-def : e ≡ exp oneℝ

-- exp 部分和 < exp x（原"exp 级数截断"定义性公理，**已降为可证明定理**：
-- 见下方 exp-partial-<（2026-08-05，partial-e-suc + exp-partial-≤-ub + lt-≤-trans-ℝ））

-- ==================================================================
-- 完备性与 exp 上确界（T3 阶段 3，2026-07-31）
-- 蓝图 §4：完备性登记为 T3 完备性假设；exp 1 = 部分和的上确界（级数定义）。
-- 用途：e < 3（部分和几何上界 + exp 最小上界）、阶段 3+ 收敛论证。
-- ==================================================================
postulate
  sup-ℝ : (S : ℝ → Set) → ℝ
  sup-upper : (S : ℝ → Set) (x : ℝ) → S x → x ≤ℝ sup-ℝ S
  sup-least : (S : ℝ → Set) (b : ℝ) → ((x : ℝ) → S x → x ≤ℝ b) → sup-ℝ S ≤ℝ b
  exp-partial-≤-ub : (n : ℕ) → partial-e n ≤ℝ exp oneℝ  -- exp 1 是部分和上界
  exp-least-ub : (b : ℝ) → ((n : ℕ) → partial-e n ≤ℝ b) → exp oneℝ ≤ℝ b  -- exp 1 是最小上界

-- **可证**：exp 部分和 < exp 1（**降定理 2026-08-05**，原"exp 级数截断"定义性公理
-- exp-partial-< 不再是 postulate）——partial-e 严格递增（partial-e-suc）+ exp 1 是
-- 部分和上界（exp-partial-≤-ub）+ < 与 ≤ 混合传递（lt-≤-trans-ℝ，阶段 0 基础假设）
exp-partial-< : (n : ℕ) → partial-e n <ℝ exp oneℝ
exp-partial-< n = lt-≤-trans-ℝ (partial-e-suc n) (exp-partial-≤-ub (suc n))

-- Archimedean 性质（桥接登记，2026-08-03）：任意实数存在自然数上界
--（∀a:ℝ. ∃n:ℕ. a ≤ natℝ n；与 sup-ℝ 同级的 ℝ 完备性族标准公理——标准实数模型真。
--  经典数学中可由 sup-ℝ（Dedekind 完备性）推出，但本构造框架缺排中律式步骤
--  （¬∀n. a≤natℝ n ⟹ ∃n. natℝ n > a−1），故显式登记（函数 + 正确性证明，sup-ℝ 模式）。
--  降定理路径 = 标准实数构造（Dedekind 分割/Cauchy 序列完备化中可证）。
--  用途：spec-int-trunc-conv（ℕ-MCT，∫f = supₙ∫min(f,n)）由桥接降为可证明定理，v1.20）
postulate
  archimedean-ub : (a : ℝ) → ℕ
  archimedean-ub-bound : (a : ℝ) → a ≤ℝ natℝ (archimedean-ub a)

-- ln 15
ln15 : ℝ
ln15 = log (natℝ 15)

-- 65/24
sixtyfive-over-24 : ℝ
sixtyfive-over-24 = natℝ 65 /ℝ natℝ 24

-- d_H 的当前最佳唯象拟合值
d-H-fit : ℝ
d-H-fit = natℝ 27095 /ℝ natℝ 10000  -- 2.7095

-- δ = d_H - ln 15
delta-fit : ℝ
delta-fit = d-H-fit -ℝ ln15

-- ==================================================================
-- log/exp 微积分（T3 阶段 3，2026-07-31）
-- 蓝图 §4：log 为 exp 的逆、exp 加性（换底公式基础）为定义性公理；
-- 有序域补充（正乘保序/除法消去/取负保序/负唯一）为基础假设；
-- ln2 与 ln(16/15) 的级数截断界为 scoped 定义性公理
--（对齐 exp-partial-≤-bound 型公理先例：ln2 = Σ_{k≥1} 1/(k·2^k) 取 0.69317，
--  ln(1+1/15) > 1/15 - 1/450 = 29/450 为 ln(1+u) 交替级数 u - u²/2 下界）。
-- 用途：闭合 B4 末项 ln15-lt-65-24（ln15 = 4ln2 + ln(15/16)）。
-- ==================================================================
postulate
  -- log 为 exp 的逆（定义性公理）
  log-exp : (x : ℝ) → log (exp x) ≡ x
  exp-log : (x : ℝ) → exp (log x) ≡ x
  exp-zero : exp zeroℝ ≡ oneℝ
  -- exp 加性（定义性公理，换底公式基础）
  exp-add : (x y : ℝ) → exp (x +ℝ y) ≡ exp x *ℝ exp y
  -- 有序域补充（基础假设）
  *-pos-mono-ℝ : {a b c : ℝ} → zeroℝ <ℝ c → a <ℝ b → (c *ℝ a) <ℝ (c *ℝ b)
  *-/cancel-ℝ : (a b : ℝ) → a *ℝ (b /ℝ a) ≡ b
  neg-<-ℝ : {x y : ℝ} → x <ℝ y → negℝ y <ℝ negℝ x
  -- ln2-lt 已于 2026-08-05 经 §2c log 级数机制（log2-partial + log2-series-ub）闭合为定理
  -- ln15-arith-ax 已于 2026-08-05 经 §2d 闭合为可证明定理（二进制 ℕ 算术 + 同分母比较），
  -- 不再是 scoped 数值公理（自 2026-08-03 v1.35 起尝试，当时因 ~1e9 级大数乘法/105600 层
  -- <-ℕ 链触发 Agda 内存不足；NATTIMES/NATPLUS 绑定后最大扩展因子仅 ~1.25e8，秒级）
  -- T3 阶段 4：exp 正性/严格单调（定义性公理，蓝图 §4；待级数机制实现为可证明定理）
  exp-pos : (x : ℝ) → zeroℝ <ℝ exp x
  exp-mono : {x y : ℝ} → x <ℝ y → exp x <ℝ exp y
  -- rpow 与 exp/log 的关系（定义性公理，蓝图 §4 rpow 内容）：a^b = e^{b·ln a}
  rpow-exp : (a b : ℝ) → (a ^-ℝ b) ≡ exp (b *ℝ log a)
  -- neg-oneℝ 的定义与零吸收（标准有序域事实，基础假设）
  neg-one-ℝ-def : neg-oneℝ ≡ negℝ oneℝ
  *-zero-ℝ : (x : ℝ) → x *ℝ zeroℝ ≡ zeroℝ
  -- 减法定义（标准有序域事实，基础假设）：x - y = x + (-y)
  -- 用途：闭合 B8 `moran-3map-holds`（c₃ 定义含 1 - c₁^d - c₂^d）
  sub-ℝ-def : (x y : ℝ) → (x -ℝ y) ≡ x +ℝ negℝ y
  -- T3 阶段 4 补充：≤ 层有序域公理（标准有序域事实，基础假设）
  -- 用途：闭合 B8 `two-exp-add-exp-lt-one`（2e^{-d²}+e^{-d(3+d)}<1，d≥1）
  --       需要 d²≥1、d(3+d)≥4 的非严格代数 + exp 的 ≤ 单调组合。
  ≤-trans-ℝ : {x y z : ℝ} → x ≤ℝ y → y ≤ℝ z → x ≤ℝ z
  *-≤-mono-ℝ : {a b c : ℝ} → zeroℝ ≤ℝ c → a ≤ℝ b → (a *ℝ c) ≤ℝ (b *ℝ c)
  neg-≤-ℝ : {x y : ℝ} → x ≤ℝ y → negℝ y ≤ℝ negℝ x
  ≤-+-mono-ℝ : {a b c d : ℝ} → a ≤ℝ b → c ≤ℝ d → (a +ℝ c) ≤ℝ (b +ℝ d)
  -- exp 的 ≤ 单调（定义性公理，exp 分析内容；exp-mono 为严格版）
  exp-mono-≤ : {x y : ℝ} → x ≤ℝ y → exp x ≤ℝ exp y
  -- rpow 底数单调（定义性公理，蓝图 §4 rpow 内容）：
  -- 0<a<b ⟹ 0<c ⟹ a^c < b^c（对应 Lean rpow 严格单调，待级数机制实现）
  -- 用途：闭合 B8 `c3-physical-lt-one`（c₃=a^{1/d}<1）与 `c₂<c₃` 排序。
  rpow-mono-ℝ : {a b c : ℝ} → zeroℝ <ℝ a → a <ℝ b → zeroℝ <ℝ c → (a ^-ℝ c) <ℝ (b ^-ℝ c)
  -- rpow 底数单调逆（定义性公理，蓝图 §4 rpow 内容）：
  -- 0<a ⟹ 0<b ⟹ 0<c ⟹ a^c < b^c ⟹ a < b（严格单调 ⟹ 单射）
  -- 用途：闭合 B8 `c₂<c₃`（c₂^d < c₃^d ⟹ c₂ < c₃）。
  rpow-mono-inv-ℝ : {a b c : ℝ} → zeroℝ <ℝ a → zeroℝ <ℝ b → zeroℝ <ℝ c
    → (a ^-ℝ c) <ℝ (b ^-ℝ c) → a <ℝ b
  -- 三分律（定义性公理，标准全序域内容）：x < y ∨ x = y ∨ y < x
  -- 用途：闭合 B4 §4 `glued-recursion-*`（正根唯一性：(y-1)·M = 0，M>0 ⟹ y=1，
  --       经 y<1 / y=1 / y>1 三分排除）。
  trichotomy-ℝ : (x y : ℝ) → (x <ℝ y) ⊎ ((x ≡ y) ⊎ (y <ℝ x))
  -- 零因子消去（定义性公理，标准域内容；可由三分律 + 乘法保序推）：
  -- a·b = 0 ⟹ a = 0 或 b = 0（域无零因子）
  -- 用途：闭合 B4 §4 `glued-recursion-*`（(Bx-1)·M = 0，M>0 ⟹ Bx-1 = 0）。
  zero-factor-ℝ : {a b : ℝ} → (a *ℝ b) ≡ zeroℝ → (a ≡ zeroℝ) ⊎ (b ≡ zeroℝ)
  -- 严格序反自反（定义性公理，标准全序域内容）：x < x ⟹ ⊥
  -- 用途：闭合 B4 §4 `glued-recursion-*`（M>0 且 M=0 ⟹ 0<0 矛盾，排除零因子第二分支）。
  irreflexive-ℝ : {x : ℝ} → x <ℝ x → ⊥

-- 除法消去（**可证**）：a·b = c ⟹ a = c/b（b 消去；*-/cancel-ℝ + *-assoc + *-ident）
--（自 §? 前移 2026-08-03：ln15-arith-ax 闭合（v1.35）的 mul-div-ℝ 依赖，前移供引用）
*-div-impl : {a b c : ℝ} → (a *ℝ b) ≡ c → a ≡ c /ℝ b
*-div-impl {a} {b} {c} h =
  trans (sym (*-ident-ℝ a))
        (trans (cong (λ x → a *ℝ x) (sym (*-/cancel-ℝ b oneℝ)))
               (trans (sym (*-assoc-ℝ a b (oneℝ /ℝ b)))
                      (trans (cong₂ _*ℝ_ h refl)
                             (trans (*-/ℝ c oneℝ b)
                                    (cong₂ _/ℝ_ (*-ident-ℝ c) refl)))))

-- 分数消去（**可证**）：(a·b)/(c·b) = a/c（/-cross-ℝ + *-assoc + *-comm）
--（自 §? 前移 2026-08-03：ln15-arith-ax 闭合（v1.35）的 /-lt-cross-ℝ 依赖，前移供引用）
frac-cancel-ℝ : (a c b : ℝ) → (a *ℝ b) /ℝ (c *ℝ b) ≡ a /ℝ c
frac-cancel-ℝ a c b =
  /-cross-ℝ (trans (*-assoc-ℝ a b c)
                   (cong (λ u → a *ℝ u) (*-comm-ℝ b c)))

-- ln15 算术比较（原 scoped 公理，已于 2026-08-05 经 §2d 闭合为可证明定理）：
-- v1.35 曾尝试 refl 级闭合但触发 Agda 内存不足（大数归一化），确认"工程计算资源不足"；
-- NATTIMES/NATPLUS 二进制算术绑定后最大扩展因子仅 ~1.25e8，秒级闭合。
-- *-div-impl/frac-cancel-ℝ 已前移至 674 后（可证引理，供既有使用处引用）。

-- ==================================================================
-- §2b T3 阶段 3+ 级数机制：exp 任意点级数 + ln1615-lb 闭合（2026-08-05）
-- 蓝图：notes/00_foundations/spectral_T3_analysis_foundation.md §5.5 开放项
-- ------------------------------------------------------------------
-- 目标：scoped 公理 ln1615-lb（ln(16/15) > 29/450）闭合为可证明定理。
-- 等价路径：29/450 < ln(16/15) ⟺ exp(29/450) < 16/15（exp-log + exp-lt-inj）。
-- 机制（新增 1 条定义性公理 exp-tail-bound，替代 1 条 scoped 数值公理）：
--   exp-partial-at ：Σ_{k=0}^n x^k/k!（任意点 exp 级数部分和）
--   exp-tail-bound ：0 ≤ x < 1 ⟹ exp x < S_n(x) + x^{n+1}/(n+1)!·1/(1-x)
--                    （几何尾部上界：Σ_{k≥n+1} x^k/k! ≤ x^{n+1}/(n+1)!·Σ_j x^j，
--                      与 exp-partial-< 同层，exp 级数内容）
-- 闭合链（x = 29/450，0 < x < 1/15 < 1/10）：
--   exp x < S₃(x) + (x⁴/24)·1/(1-x)                [exp-tail-bound 3]
--         < 1 + x + x²/2 + x²/60 + x²/2160         [x³/6 < x²/60、尾部 < x²/2160]
--         = 1 + x + 1117x²/2160
--         < 1 + x + (15/29)x²                      [1117/2160 < 15/29，交叉 32393 < 32400]
--         < 1 + x + x·(1/29)                       [x² < x·(1/15)，15/29·(1/15) = 1/29]
--         < 1 + x + 1/450 = 16/15                  [x = 29/450，29/450·(1/29) = 1/450]
-- 关键设计：全部交叉乘积 ≤ 939600（远低于 1e9 工程墙）；大数 ℕ 比较经
-- <-add-r（m < m + suc k）+ +ℕ 定义性归约构造。
-- ==================================================================

-- 自然数次幂（迭代乘法；独立于 rpow 避免 exp/log 循环）
_^ℕ_ : ℝ → ℕ → ℝ
x ^ℕ zero = oneℝ
x ^ℕ (suc n) = x *ℝ (x ^ℕ n)

-- exp 级数任意点部分和：S_n(x) = Σ_{k=0}^n x^k/k!
exp-partial-at : ℕ → ℝ → ℝ
exp-partial-at zero x = oneℝ
exp-partial-at (suc n) x = exp-partial-at n x +ℝ ((x ^ℕ (suc n)) *ℝ recip-factorial (suc n))

-- exp 任意点级数 sup 定义（2026-08-05，exp-tail-bound 降定理前置②）：
-- exp x = Σ_{k≥0} x^k/k! 的级数 sup 刻画（与 exp-partial-≤-ub/exp-least-ub 同层，
-- exp oneℝ 版的任意点推广；数学上成立 = exp 的级数定义，登记为基础假设层。
-- 用途：exp-tail-bound 降定理的 sup 论证（部分和 ≤ exp x + exp x ≤ 最小上界））
postulate
  exp-partial-at-≤-ub : (n : ℕ) (x : ℝ) → exp-partial-at n x ≤ℝ exp x  -- 部分和 ≤ exp x（任意点）
  exp-least-ub-any : (x : ℝ) (b : ℝ) → ((n : ℕ) → exp-partial-at n x ≤ℝ b) → exp x ≤ℝ b  -- exp x 是最小上界

-- 几何尾部上界（**已闭合为可证定理 exp-tail-bound-thm，2026-08-05 固定间隙路径**）：
--   0 < x < 1 ⟹ exp x < S_n(x) + x^{n+1}/(n+1)!·1/(1-x)
-- 依据：exp x = Σ_{k≥0} x^k/k!，尾部 Σ_{k≥n+1} x^k/k! ≤ x^{n+1}/(n+1)!·Σ_{j≥0}x^j。
-- 闭合路径：tail-term-le（pow-add + factorial-strong + div-pow）⟹ tail-sum ≤
--   系数·geo-x(x/2)（tail-sum-le）⟹ geo-x(x/2) < 1/(1-x/2)（geo-x-lt 特化）⟹
--   部分和 ≤ S_n + 系数·1/(1-x/2)（B''，固定）⟹ exp x ≤ B''（exp-least-ub-any）
--   < S_n + 系数·1/(1-x)（recip-half-gap，固定间隙保持严格）⟹ exp x < B。
-- 注：x = 0 时 exp 0 = 1 = S_n(0)，结论为等号——严格 < 需前提 0 < x（数学上必要）。

-- ==================================================================
-- 几何级数机制（exp-tail-bound 降定理核心前置，2026-08-05）
-- 目标：一般几何和 Σ_{j=0}^m x^j（geo-x）的闭式与 < 1/(1-x) 上界——
--   exp-tail-bound 的尾部界 Σ_{k≥n+1} x^k/k! ≤ x^{n+1}/(n+1)!·Σ_{j≥0}x^j 的基础。
-- 全部**可证**，零新增公理（+/-/*/div 域公理 + 现有 /-add-ℝ、*-/ℝ、div-one-ℝ、
--   *-/cancel-ℝ、add-pos-ℝ、lt-*-pos-ℝ、/-pos-ℝ）。
-- ==================================================================

-- **可证**：(1−x) + x = 1（sub-ℝ-def 展开 + 加法群）
one-sub-add : (x : ℝ) → (oneℝ -ℝ x) +ℝ x ≡ oneℝ
one-sub-add x =
  trans (cong (λ y → y +ℝ x) (sub-ℝ-def oneℝ x))
        (trans (+-assoc-ℝ oneℝ (negℝ x) x)
               (trans (cong (λ y → oneℝ +ℝ y) (+-comm-ℝ (negℝ x) x))
                      (trans (cong (λ y → oneℝ +ℝ y) (+-inv-ℝ x))
                             (+-ident-ℝ oneℝ))))

-- **可证**：x < 1 ⟹ 0 < 1−x（neg-<-ℝ：-1 < -x ⟹ 0 = 1+(-1) < 1+(-x) = 1-x）
one-sub-pos : {x : ℝ} → x <ℝ oneℝ → zeroℝ <ℝ (oneℝ -ℝ x)
one-sub-pos {x} hx =
  subst (λ z → zeroℝ <ℝ z) (sym one-minus-x)
        (subst (λ u → u <ℝ (oneℝ +ℝ negℝ x)) (+-inv-ℝ oneℝ)
               (lt-+-mono-r-ℝ {a = oneℝ} {b = negℝ oneℝ} {c = negℝ x} (neg-<-ℝ hx)))
  where
  one-minus-x : (oneℝ -ℝ x) ≡ (oneℝ +ℝ negℝ x)
  one-minus-x = sub-ℝ-def oneℝ x

-- **可证**：G = 1/(1−x) 满足不动点 G = 1 + x·G
--（1 + x·(1/(1−x)) = (1/(1−x))：/-add-ℝ 通分 + one-sub-add）
G-ident : (x : ℝ) → (oneℝ +ℝ (x *ℝ (oneℝ /ℝ (oneℝ -ℝ x)))) ≡ (oneℝ /ℝ (oneℝ -ℝ x))
G-ident x = trans (cong₂ _+ℝ_ (sym (div-one-ℝ oneℝ)) step2)
            (trans (/-add-ℝ oneℝ x oneℝ (oneℝ -ℝ x))
                   (cong₂ _/ℝ_ sum-eq den-eq))
  where
  step2 : (x *ℝ (oneℝ /ℝ (oneℝ -ℝ x))) ≡ (x /ℝ (oneℝ -ℝ x))
  step2 = trans (*-/ℝ x oneℝ (oneℝ -ℝ x)) (cong₂ _/ℝ_ (*-ident-ℝ x) refl)
  sum-eq : ((oneℝ *ℝ (oneℝ -ℝ x)) +ℝ (x *ℝ oneℝ)) ≡ oneℝ
  sum-eq = trans (cong₂ _+ℝ_ (trans (*-comm-ℝ oneℝ (oneℝ -ℝ x)) (*-ident-ℝ (oneℝ -ℝ x))) (*-ident-ℝ x))
                 (one-sub-add x)
  den-eq : (oneℝ *ℝ (oneℝ -ℝ x)) ≡ (oneℝ -ℝ x)
  den-eq = trans (*-comm-ℝ oneℝ (oneℝ -ℝ x)) (*-ident-ℝ (oneℝ -ℝ x))

-- 一般几何和：geo-x x m = Σ_{j=0}^m x^j（公比 x 任意）
geo-x : ℝ → ℕ → ℝ
geo-x x zero = oneℝ
geo-x x (suc m) = geo-x x m +ℝ (x ^ℕ (suc m))

-- **可证**：x^ℕ 幂正性——0 < x ⟹ 0 < x^{n+1}（归纳，lt-*-pos-ℝ）
power-pos-ℕ : (x : ℝ) → zeroℝ <ℝ x → (n : ℕ) → zeroℝ <ℝ (x ^ℕ (suc n))
power-pos-ℕ x hx zero = subst (λ z → zeroℝ <ℝ z) (sym (*-ident-ℝ x)) hx
power-pos-ℕ x hx (suc n) =
  lt-*-pos-ℝ hx (power-pos-ℕ x hx n)

-- **可证**：几何和闭式（不动点）——geo-x x m + x^{m+1}·G = G（G = 1/(1−x)）
geo-x-ident : (x : ℝ) → (m : ℕ) → (geo-x x m +ℝ ((x ^ℕ (suc m)) *ℝ (oneℝ /ℝ (oneℝ -ℝ x)))) ≡ (oneℝ /ℝ (oneℝ -ℝ x))
geo-x-ident x zero = trans (cong (λ w → oneℝ +ℝ (w *ℝ G)) (*-ident-ℝ x)) (G-ident x)
  where
  G : ℝ
  G = oneℝ /ℝ (oneℝ -ℝ x)
geo-x-ident x (suc m) =
  trans (+-assoc-ℝ (geo-x x m) (x ^ℕ (suc m)) ((x ^ℕ (suc (suc m))) *ℝ G))
        (trans (cong (λ y → geo-x x m +ℝ y) inner-ident) (geo-x-ident x m))
  where
  G : ℝ
  G = oneℝ /ℝ (oneℝ -ℝ x)
  -- x^{m+2} = x·x^{m+1}（定义性）
  pow-expand : (x ^ℕ (suc (suc m))) ≡ (x *ℝ (x ^ℕ (suc m)))
  pow-expand = refl
  -- x^{m+1} + x^{m+2}·G = x^{m+1}·G（x^{m+2} = x·x^{m+1} + 不动点 G = 1 + xG）
  inner-ident : ((x ^ℕ (suc m)) +ℝ ((x ^ℕ (suc (suc m))) *ℝ G)) ≡ ((x ^ℕ (suc m)) *ℝ G)
  inner-ident =
    trans (cong₂ _+ℝ_ (sym (*-ident-ℝ (x ^ℕ (suc m)))) (cong (λ w → w *ℝ G) pow-expand))
          (trans (cong (λ w → ((x ^ℕ (suc m)) *ℝ oneℝ) +ℝ w)
                       (trans (cong (λ w → w *ℝ G) (*-comm-ℝ x (x ^ℕ (suc m))))
                              (*-assoc-ℝ (x ^ℕ (suc m)) x G)))
                 (trans (sym (distrib-ℝ (x ^ℕ (suc m)) oneℝ (x *ℝ G)))
                        (cong (λ w → (x ^ℕ (suc m)) *ℝ w) (G-ident x))))

-- **可证**：几何和 < 闭式——geo-x x m < 1/(1−x)（x > 0；闭式 + 尾项正）
geo-x-lt : (x : ℝ) → zeroℝ <ℝ x → x <ℝ oneℝ → (m : ℕ) → geo-x x m <ℝ (oneℝ /ℝ (oneℝ -ℝ x))
geo-x-lt x hx hlt m =
  subst (λ z → geo-x x m <ℝ z) (geo-x-ident x m)
        (add-pos-ℝ (lt-*-pos-ℝ (power-pos-ℕ x hx m) G-pos))
  where
  G-pos : zeroℝ <ℝ (oneℝ /ℝ (oneℝ -ℝ x))
  G-pos = /-pos-ℝ zero-lt-one-ℝ (one-sub-pos hlt)

-- ==================================================================
-- 部分和分解（exp-tail-bound 降定理前置③核心，2026-08-05）
-- 目标：exp-partial-at (n+1+m) x = exp-partial-at n x + T_n(m)（尾部有限和分解），
--   T_n(m) = Σ_{j=0}^m x^{n+1+j}/(n+1+j)!。索引用 _+ℕr_（未绑定递归，可归约；
--   NATPLUS 绑定的 _+ℕ_ 对开放项不归约——与 <-add 同思路）。
-- ==================================================================

-- 尾部有限和：T_n(m) = Σ_{j=0}^m x^{suc (n +ℕr j)}/factorial(suc (n +ℕr j))
--（m+1 项：k = n+1, ..., n+1+m；索引用 suc 外层（可展开）——suc n +ℕr m 第二个参数
--  为变量不归约）
tail-sum : ℕ → ℕ → ℝ → ℝ
tail-sum n zero x = (x ^ℕ (suc n)) *ℝ recip-factorial (suc n)
tail-sum n (suc m) x = tail-sum n m x +ℝ ((x ^ℕ (suc (suc (n +ℕr m)))) *ℝ recip-factorial (suc (suc (n +ℕr m))))

-- **可证**：部分和分解——exp-partial-at (n+1+m) x = exp-partial-at n x + T_n(m)
--（归纳：base 定义性；step 递归展开 + assoc；n +ℕr (suc m) = suc (n +ℕr m) 定义性）
exp-decomp : (n m : ℕ) (x : ℝ) → exp-partial-at (suc (n +ℕr m)) x ≡ exp-partial-at n x +ℝ tail-sum n m x
exp-decomp n zero x = refl
exp-decomp n (suc m) x =
  trans (cong (λ u → u +ℝ ((x ^ℕ (suc (suc (n +ℕr m)))) *ℝ recip-factorial (suc (suc (n +ℕr m)))))
             (exp-decomp n m x))
        (+-assoc-ℝ (exp-partial-at n x) (tail-sum n m x)
                   ((x ^ℕ (suc (suc (n +ℕr m)))) *ℝ recip-factorial (suc (suc (n +ℕr m)))))

-- ==================================================================
-- 阶乘强估计（固定间隙路径关键，2026-08-05）
-- 目标：(n+1+j)! ≥ (n+1)!·2^ j（ℕ 层，≤ℕ）——tail-sum 逐项 ≤ x^{n+1}/(n+1)!·(x/2)^j
--   的基础（每个额外因子 ≥ 2 ⟹ 几何公比折半 x/2 ⟹ 固定间隙）。
-- 依赖：NatArith §5-6 半环代数 + ≤ℕ（*ℕ-comm/assoc/ident-r、*ℕ-≤-mono-r、z≤n/s≤s）。
-- ==================================================================

-- 2 ≤ 2+k（ℕ 层，≤ℕ）
two-≤-sucsuc : (k : ℕ) → 2 ≤ℕ suc (suc k)
two-≤-sucsuc k = s≤s (s≤s z≤n)

-- **可证**：阶乘强估计——factorial (suc n) *ℕ 2^ j ≤ℕ factorial (suc (n +ℕr j))
--（归纳 j：base *ℕ-ident-r；step 左端 (n+1)!·2^{j+1} = ((n+1)!·2^ j)·2（*ℕ-assoc/comm
--  + 2^ 定义）⟹ 归纳·2（*ℕ-≤-mono-r）⟹ factorial·2 ≤ (n+2+j)!（2 ≤ suc(suc k) +
--  *ℕ-≤-mono-r + factorial 递归 + *ℕ-comm））
factorial-strong : (n j : ℕ) → (factorial (suc n) *ℕ 2^ j) ≤ℕ factorial (suc (n +ℕr j))
factorial-strong n zero =
  subst (λ x → x ≤ℕ factorial (suc n)) (sym (*ℕ-ident-r (factorial (suc n)))) ≤ℕ-refl
factorial-strong n (suc j) =
  subst (λ y → (factorial (suc n) *ℕ 2^ (suc j)) ≤ℕ y)
        (sym (cong (λ z → factorial (suc z)) (+ℕr-suc n j)))
        (subst (λ x → x ≤ℕ factorial (suc (suc (n +ℕr j)))) (sym eq-left)
               (≤ℕ-trans step1 step2))
  where
  -- 归纳 ×2：((n+1)!·2^ j)·2 ≤ ((n+1+j)!)·2
  step1 : ((factorial (suc n) *ℕ 2^ j) *ℕ 2) ≤ℕ (factorial (suc (n +ℕr j)) *ℕ 2)
  step1 = *ℕ-≤-mono-r {a = factorial (suc n) *ℕ 2^ j} {b = factorial (suc (n +ℕr j))} {c = 2}
                      (factorial-strong n j) z<s
  -- 左端：factorial (suc n)·2^{j+1} ≡ ((factorial (suc n)·2^ j)·2)
  eq-left : (factorial (suc n) *ℕ 2^ (suc j)) ≡ ((factorial (suc n) *ℕ 2^ j) *ℕ 2)
  eq-left = trans (cong (λ x → factorial (suc n) *ℕ x) (*ℕ-comm 2 (2^ j)))
                  (sym (*ℕ-assoc (factorial (suc n)) (2^ j) 2))
  -- 右端：((n+1+j)!)·2 ≤ (n+2+j)!（2 ≤ suc(suc k) + *ℕ 保序 + factorial 递归 + *ℕ-comm）
  step2 : (factorial (suc (n +ℕr j)) *ℕ 2) ≤ℕ factorial (suc (suc (n +ℕr j)))
  step2 = subst (λ x → x ≤ℕ ((suc (suc (n +ℕr j))) *ℕ factorial (suc (n +ℕr j))))
                (sym (*ℕ-comm (factorial (suc (n +ℕr j))) 2))
                (*ℕ-≤-mono-r {a = 2} {b = suc (suc (n +ℕr j))} {c = factorial (suc (n +ℕr j))}
                             (two-≤-sucsuc (n +ℕr j)) (factorial-pos (suc (n +ℕr j))))
  -- +ℕr 右端 suc：n +ℕr (suc j) ≡ suc (n +ℕr j)
  +ℕr-suc : (n j : ℕ) → n +ℕr (suc j) ≡ suc (n +ℕr j)
  +ℕr-suc n j = refl

-- ==================================================================
-- 幂加法性与 x/2 引理（固定间隙路径组合前置，2026-08-05）
-- 目标：tail-sum 逐项 ≤ x^{n+1}/(n+1)!·(x/2)^j（pow-add + factorial-strong）
--   + geo-x (x/2) < 1/(1-x/2)（x/2 正性/小于 1）+ 1/(1-x/2) < 1/(1-x)（recip 单调）
-- ==================================================================

-- **可证**：幂加法性——x^{a+b} = x^a·x^b（归纳 b，*-assoc/comm）
pow-add : (x : ℝ) (a b : ℕ) → (x ^ℕ (a +ℕr b)) ≡ (x ^ℕ a) *ℝ (x ^ℕ b)
pow-add x a zero = sym (*-ident-ℝ (x ^ℕ a))
pow-add x a (suc b) =
  trans (cong (λ w → x *ℝ w) (pow-add x a b))
        (trans (sym (*-assoc-ℝ x (x ^ℕ a) (x ^ℕ b)))
               (trans (cong (λ w → w *ℝ (x ^ℕ b)) (*-comm-ℝ x (x ^ℕ a)))
                      (*-assoc-ℝ (x ^ℕ a) x (x ^ℕ b))))

-- 半量记号：x/2
half-x : ℝ → ℝ
half-x x = x /ℝ natℝ 2

-- **可证**：x > 0 ⟹ x/2 > 0（/-pos-ℝ + natℝ-pos-embed z<s）
div-half-pos : {x : ℝ} → zeroℝ <ℝ x → zeroℝ <ℝ half-x x
div-half-pos {x} hx = /-pos-ℝ hx (natℝ-pos-embed z<s)

-- **可证**：x < 1 ⟹ x/2 < 1（x < 1 < 2 ⟹ x/2 < 2/2 = 1，/-lt-same-den-ℝ）
div-half-lt-one : {x : ℝ} → x <ℝ oneℝ → half-x x <ℝ oneℝ
div-half-lt-one {x} hx =
  subst (λ y → half-x x <ℝ y) two-over-two
        (subst (λ w → (x /ℝ natℝ 2) <ℝ w) (cong (λ z → z /ℝ natℝ 2) (sym natℝ-two))
               (/-lt-same-den-ℝ {x} {natℝ 2} {natℝ 2} x-lt-two))
  where
  -- 1 < 2（natℝ 层）
  one-lt-two : oneℝ <ℝ natℝ 2
  one-lt-two = subst (λ z → z <ℝ natℝ 2) natℝ-one (natℝ-<-embed (s<s z<s))
  -- x < 2（x < 1 < 2）
  x-lt-two : x <ℝ natℝ 2
  x-lt-two = trans-<ℝ hx one-lt-two
  natℝ-two : natℝ 2 ≡ natℝ (suc (suc zero))
  natℝ-two = refl
  -- 2/2 = 1
  two-over-two : (natℝ 2 /ℝ natℝ 2) ≡ oneℝ
  two-over-two = trans (/-cross-ℝ {natℝ 2} {oneℝ} {natℝ 2} {oneℝ} cross) (div-one-ℝ oneℝ)
    where
    cross : (natℝ 2 *ℝ oneℝ) ≡ (oneℝ *ℝ natℝ 2)
    cross = trans (*-ident-ℝ (natℝ 2))
                  (sym (trans (*-comm-ℝ oneℝ (natℝ 2)) (*-ident-ℝ (natℝ 2))))

-- **可证**：1/(1-x/2) < 1/(1-x)（recip-mono-ℝ：0 < 1-x < 1-x/2 ⟸ x > 0）
recip-half-gap : {x : ℝ} → zeroℝ <ℝ x → x <ℝ oneℝ →
  (oneℝ /ℝ (oneℝ -ℝ half-x x)) <ℝ (oneℝ /ℝ (oneℝ -ℝ x))
recip-half-gap {x} hx hlt = recip-mono-ℝ (one-sub-pos hlt) sub-gap
  where
  -- x/2 + x/2 = x（x/2·1 + x/2·1 = x/2·(1+1) = x/2·2 = 2·(x/2) = x）
  two-eq : (oneℝ +ℝ oneℝ) ≡ natℝ 2
  two-eq = trans (cong₂ _+ℝ_ (sym natℝ-one) (sym natℝ-one)) (sym (natℝ-+ 1 1))
  half-add-half : (half-x x +ℝ half-x x) ≡ x
  half-add-half = trans step1 step2
    where
    step1 : (half-x x +ℝ half-x x) ≡ ((half-x x) *ℝ natℝ 2)
    step1 = trans (cong₂ _+ℝ_ (sym (*-ident-ℝ (half-x x))) (sym (*-ident-ℝ (half-x x))))
                  (trans (sym (distrib-ℝ (half-x x) oneℝ oneℝ))
                         (cong (λ w → (half-x x) *ℝ w) two-eq))
    step2 : ((half-x x) *ℝ natℝ 2) ≡ x
    step2 = trans (*-comm-ℝ (half-x x) (natℝ 2)) (*-/cancel-ℝ (natℝ 2) x)
  -- x/2 < x（x/2 + x/2 = x ⟹ x/2 < x 经 add-pos-ℝ）
  half-lt-x : half-x x <ℝ x
  half-lt-x = subst (λ z → half-x x <ℝ z) half-add-half (add-pos-ℝ (div-half-pos hx))
  -- 1-x < 1-x/2（x/2 < x ⟹ -x < -x/2（neg-<-ℝ）⟹ 1+(-x) < 1+(-x/2)）
  sub-gap : (oneℝ -ℝ x) <ℝ (oneℝ -ℝ half-x x)
  sub-gap = subst (λ u → u <ℝ (oneℝ -ℝ half-x x)) (sym (sub-ℝ-def oneℝ x))
                  (subst (λ w → (oneℝ +ℝ negℝ x) <ℝ w) (sym (sub-ℝ-def oneℝ (half-x x)))
                         (lt-+-mono-r-ℝ {a = oneℝ} {b = negℝ x} {c = negℝ (half-x x)}
                                        (neg-<-ℝ half-lt-x)))

-- m < m + (k+1)（大数 ℕ 比较构造工具：m +ℕ suc k 定义性归约到 m+k+1）
<-add-r : (m k : ℕ) → m <ℕ (m +ℕ suc k)
<-add-r zero k = z<s
<-add-r (suc m) k = s<s (<-add-r m k)

-- exp 严格单调之逆：exp x < exp y ⟹ x < y（exp-mono 严格 + 三分律 + 反自反，零新增公理）
exp-lt-inj : {x y : ℝ} → exp x <ℝ exp y → x <ℝ y
exp-lt-inj {x} {y} h with trichotomy-ℝ x y
exp-lt-inj {x} {y} h | inj₁ x<y = x<y
exp-lt-inj {x} {y} h | inj₂ (inj₁ x=y) =
  ⊥-elim (irreflexive-ℝ (subst (λ z → z <ℝ exp y) (cong exp x=y) h))
exp-lt-inj {x} {y} h | inj₂ (inj₂ y<x) =
  ⊥-elim (irreflexive-ℝ (trans-<ℝ h (exp-mono y<x)))

-- (a/c)·c = a（商消去，可证：*-comm + *-/cancel-ℝ）
x-over-c-mul-c : {x c : ℝ} → (x /ℝ c) *ℝ c ≡ x
x-over-c-mul-c {x} {c} = trans (*-comm-ℝ (x /ℝ c) c) (*-/cancel-ℝ c x)

-- (x/c)/d = x/(c·d)（双重分数，可证：/-cross-ℝ）
frac-frac-ℝ : (x c d : ℝ) → (x /ℝ c) /ℝ d ≡ x /ℝ (c *ℝ d)
frac-frac-ℝ x c d = /-cross-ℝ {a = x /ℝ c} {b = x} {c = d} {d = c *ℝ d}
  (trans (sym (*-assoc-ℝ (x /ℝ c) c d)) (cong (λ u → u *ℝ d) (x-over-c-mul-c {x} {c})))

-- (a/c)·(b/d) = (a·b)/(c·d)（分数乘法，可证）
mul-div-ℝ : (a b c d : ℝ) → (a /ℝ c) *ℝ (b /ℝ d) ≡ (a *ℝ b) /ℝ (c *ℝ d)
mul-div-ℝ a b c d =
  trans (*-/ℝ (a /ℝ c) b d)
    (trans (cong (λ u → u /ℝ d) (trans (*-comm-ℝ (a /ℝ c) b) (*-/ℝ b a c)))
           (trans (frac-frac-ℝ (b *ℝ a) c d)
                  (cong (λ u → u /ℝ (c *ℝ d)) (*-comm-ℝ b a))))

-- ==================================================================
-- 固定间隙路径组合（exp-tail-bound 降定理收官，2026-08-05）
-- 目标：tail-sum 逐项 ≤ 系数·(x/2)^j（pow-add + factorial-strong + div-pow）
--   + geo-x (x/2) < 1/(1-x/2)（geo-x-lt 特化）+ sup 组合（固定间隙 B'' < B）。
-- ==================================================================

-- **可证**：natℝ 0 = 0（natℝ-one + natℝ-suc zero ⟹ 1 = natℝ 0 + 1 ⟹ 加右消去）
natℝ-zero : natℝ zero ≡ zeroℝ
natℝ-zero = trans (sym (+-ident-ℝ (natℝ zero)))
            (trans (cong (λ u → natℝ zero +ℝ u) (sym (+-inv-ℝ oneℝ)))
            (trans (sym (+-assoc-ℝ (natℝ zero) oneℝ (negℝ oneℝ)))
            (trans (sym (cong (λ u → u +ℝ negℝ oneℝ) h-one))
                   (+-inv-ℝ oneℝ))))
  where
  h-one : oneℝ ≡ (natℝ zero +ℝ oneℝ)
  h-one = trans (sym natℝ-one) (natℝ-suc zero)

-- **可证**：加法右保序（≤ 版）——a ≤ b ⟹ a+c ≤ b+c（三分律）
≤-+-mono-r-ℝ : {a b c : ℝ} → a ≤ℝ b → (a +ℝ c) ≤ℝ (b +ℝ c)
≤-+-mono-r-ℝ {a} {b} {c} hab with trichotomy-ℝ a b
≤-+-mono-r-ℝ {a} {b} {c} hab | inj₁ a<b =
  <-≤-ℝ (subst (λ u → u <ℝ (b +ℝ c)) (sym (+-comm-ℝ a c))
         (subst (λ v → (c +ℝ a) <ℝ v) (sym (+-comm-ℝ b c))
                (lt-+-mono-r-ℝ {a = c} {b = a} {c = b} a<b)))
≤-+-mono-r-ℝ {a} {b} {c} hab | inj₂ (inj₁ a=b) = subst (λ z → (a +ℝ c) ≤ℝ (z +ℝ c)) a=b (refl-≤ℝ)
≤-+-mono-r-ℝ {a} {b} {c} hab | inj₂ (inj₂ b<a) = ⊥-elim (irreflexive-ℝ (≤-lt-trans-ℝ hab b<a))

-- **可证**：suc 保序嵌入——natℝ m ≤ natℝ n ⟹ natℝ (suc m) ≤ natℝ (suc n)
natℝ-suc-mono : {m n : ℕ} → natℝ m ≤ℝ natℝ n → natℝ (suc m) ≤ℝ natℝ (suc n)
natℝ-suc-mono {m} {n} h =
  subst (λ z → natℝ (suc m) ≤ℝ z) (sym (natℝ-suc n))
    (subst (λ w → w ≤ℝ (natℝ n +ℝ oneℝ)) (sym (natℝ-suc m))
           (≤-+-mono-r-ℝ {a = natℝ m} {b = natℝ n} {c = oneℝ} h))

-- **可证**：natℝ zero ≤ natℝ n（n = 0 refl；n ≥ 1 经 natℝ-zero + natℝ-pos-embed）
natℝ-zero-le : (n : ℕ) → natℝ zero ≤ℝ natℝ n
natℝ-zero-le zero = refl-≤ℝ
natℝ-zero-le (suc n) = subst (λ z → z ≤ℝ natℝ (suc n)) (sym natℝ-zero) (<-≤-ℝ (natℝ-pos-embed (z<s {n})))

-- **可证**：倒数非严格单调——0 < a ≤ b ⟹ 1/b ≤ 1/a（三分律：a<b 走 recip-mono-ℝ，
--   a=b 替换，b<a 矛盾）
recip-≤-ℝ : {a b : ℝ} → zeroℝ <ℝ a → a ≤ℝ b → (oneℝ /ℝ b) ≤ℝ (oneℝ /ℝ a)
recip-≤-ℝ {a} {b} ha hab with trichotomy-ℝ a b
recip-≤-ℝ {a} {b} ha hab | inj₁ a<b = <-≤-ℝ (recip-mono-ℝ ha a<b)
recip-≤-ℝ {a} {b} ha hab | inj₂ (inj₁ a=b) = subst (λ z → (oneℝ /ℝ b) ≤ℝ (oneℝ /ℝ z)) (sym a=b) (refl-≤ℝ {oneℝ /ℝ b})
recip-≤-ℝ {a} {b} ha hab | inj₂ (inj₂ b<a) = ⊥-elim (irreflexive-ℝ (≤-lt-trans-ℝ hab b<a))

-- **可证**：幂乘性——(x·y)^j = x^j·y^j（归纳，*-assoc/comm）
pow-mul : (x y : ℝ) (j : ℕ) → ((x *ℝ y) ^ℕ j) ≡ ((x ^ℕ j) *ℝ (y ^ℕ j))
pow-mul x y zero = sym (*-ident-ℝ oneℝ)
pow-mul x y (suc j) =
  trans (cong (λ w → (x *ℝ y) *ℝ w) (pow-mul x y j))
        (trans (sym (*-assoc-ℝ (x *ℝ y) (x ^ℕ j) (y ^ℕ j)))
               (trans (cong (λ w → w *ℝ (y ^ℕ j)) inner)
                      (*-assoc-ℝ (x *ℝ (x ^ℕ j)) y (y ^ℕ j))))
  where
  -- (x·y)·x^j = (x·x^j)·y（assoc + comm + assoc）
  inner : ((x *ℝ y) *ℝ (x ^ℕ j)) ≡ ((x *ℝ (x ^ℕ j)) *ℝ y)
  inner = trans (*-assoc-ℝ x y (x ^ℕ j))
                (trans (cong (λ w → x *ℝ w) (*-comm-ℝ y (x ^ℕ j)))
                       (sym (*-assoc-ℝ x (x ^ℕ j) y)))

-- **可证**：1^j = 1（归纳，*-ident-ℝ）
one-pow : (j : ℕ) → (oneℝ ^ℕ j) ≡ oneℝ
one-pow zero = refl
one-pow (suc j) = trans (cong (λ w → oneℝ *ℝ w) (one-pow j)) (*-ident-ℝ oneℝ)

-- **可证**：除法幂——(x/y)^j = x^j/y^j（归纳，mul-div-ℝ）
div-pow : (x y : ℝ) (j : ℕ) → ((x /ℝ y) ^ℕ j) ≡ ((x ^ℕ j) /ℝ (y ^ℕ j))
div-pow x y zero = sym (div-one-ℝ oneℝ)
div-pow x y (suc j) =
  trans (cong (λ w → (x /ℝ y) *ℝ w) (div-pow x y j))
        (mul-div-ℝ x (x ^ℕ j) y (y ^ℕ j))

-- **可证**：ℕ 层——suc n +ℕr m = suc (n +ℕr m)（归纳 m，+ℕr 第二参数变量不归约）
+ℕr-comm-suc : (n m : ℕ) → (suc n +ℕr m) ≡ suc (n +ℕr m)
+ℕr-comm-suc n zero = refl
+ℕr-comm-suc n (suc m) = cong suc (+ℕr-comm-suc n m)

-- **可证**：ℕ 层保序嵌入（≤ 版）——m ≤ n ⟹ natℝ m ≤ natℝ n
--（归纳 ≤ℕ：z≤n 经 natℝ-zero-le；s≤s 经 ≤-+-mono-r-ℝ 保序 + natℝ-suc-mono）
natℝ-≤-embed : {m n : ℕ} → m ≤ℕ n → natℝ m ≤ℝ natℝ n
natℝ-≤-embed z≤n = natℝ-zero-le _
natℝ-≤-embed (s≤s h) = natℝ-suc-mono (natℝ-≤-embed h)

-- ==================================================================
-- 固定间隙路径·尾部逐项（exp-tail-bound 降定理，2026-08-05）
-- 目标：tail-sum 逐项 ≤ x^{n+1}/(n+1)!·(x/2)^j（recip-factorial-strong-le +
--   pow-add + *-≤-mono-ℝ），全部**可证**，零新增公理。
-- ==================================================================

-- **可证**：x > 0 ⟹ 1−x < 1（(1−x) + x = 1 且 x > 0）
one-sub-lt-one : {x : ℝ} → zeroℝ <ℝ x → (oneℝ -ℝ x) <ℝ oneℝ
one-sub-lt-one {x} hx = subst (λ z → (oneℝ -ℝ x) <ℝ z) (one-sub-add x) (add-pos-ℝ hx)

-- **可证**：1 < 1/(1−x)（recip-mono-ℝ：0 < 1−x < 1 ⟹ 1/1 < 1/(1−x)）
G-gt-one : {x : ℝ} → zeroℝ <ℝ x → x <ℝ oneℝ → oneℝ <ℝ (oneℝ /ℝ (oneℝ -ℝ x))
G-gt-one {x} hx hlt =
  subst (λ z → z <ℝ (oneℝ /ℝ (oneℝ -ℝ x))) (div-one-ℝ oneℝ)
        (recip-mono-ℝ (one-sub-pos hlt) (one-sub-lt-one hx))

-- **可证**：1/(a·b) = (1/a)·(1/b)（mul-div-ℝ 反向）
recip-mul-split : (a b : ℝ) → (oneℝ /ℝ (a *ℝ b)) ≡ ((oneℝ /ℝ a) *ℝ (oneℝ /ℝ b))
recip-mul-split a b =
  sym (trans (mul-div-ℝ oneℝ oneℝ a b) (cong₂ _/ℝ_ (trans (*-ident-ℝ oneℝ) refl) refl))

-- **可证**：1/(n+1+j)! ≤ (1/(n+1)!)·(1/2^j)（factorial-strong + natℝ-≤-embed +
--   recip-≤-ℝ + recip-mul-split）
recip-factorial-strong-le : (n j : ℕ) →
  recip-factorial (suc (n +ℕr j)) ≤ℝ (recip-factorial (suc n) *ℝ (natℝ 1 /ℝ natℝ (2^ j)))
recip-factorial-strong-le n j = stepC
  where
  fs1 : ℝ
  fs1 = natℝ (factorial (suc (n +ℕr j)))
  fsl : ℝ
  fsl = natℝ (factorial (suc n))
  f2 : ℝ
  f2 = natℝ (2^ j)
  -- 分母比较：0 < (n+1)!·2^j ≤ (n+1+j)!
  fs-pos : zeroℝ <ℝ (fsl *ℝ f2)
  fs-pos = lt-*-pos-ℝ (natℝ-pos-embed (factorial-pos (suc n))) (natℝ-pos-embed (2^-pos j))
  fs : (fsl *ℝ f2) ≤ℝ fs1
  fs = subst (λ u → u ≤ℝ fs1) (natℝ-* (factorial (suc n)) (2^ j))
            (natℝ-≤-embed (factorial-strong n j))
  -- 倒数非严格单调：1/(n+1+j)! ≤ 1/((n+1)!·2^j)
  core : (oneℝ /ℝ fs1) ≤ℝ (oneℝ /ℝ (fsl *ℝ f2))
  core = recip-≤-ℝ fs-pos fs
  -- 1/((n+1)!·2^j) = (1/(n+1)!)·(1/2^j)
  split-le : (oneℝ /ℝ fs1) ≤ℝ ((oneℝ /ℝ fsl) *ℝ (oneℝ /ℝ f2))
  split-le = subst (λ z → (oneℝ /ℝ fs1) ≤ℝ z) (recip-mul-split fsl f2) core
  -- natℝ 1 ≡ oneℝ 归位
  stepB : (natℝ 1 /ℝ fs1) ≤ℝ ((oneℝ /ℝ fsl) *ℝ (oneℝ /ℝ f2))
  stepB = subst (λ u → u ≤ℝ ((oneℝ /ℝ fsl) *ℝ (oneℝ /ℝ f2)))
                (sym (cong (λ w → w /ℝ fs1) natℝ-one)) split-le
  stepC : (natℝ 1 /ℝ fs1) ≤ℝ ((natℝ 1 /ℝ fsl) *ℝ (natℝ 1 /ℝ f2))
  stepC = subst (λ v → (natℝ 1 /ℝ fs1) ≤ℝ v)
                (cong₂ _*ℝ_ (sym (cong (λ w → w /ℝ fsl) natℝ-one))
                            (sym (cong (λ w → w /ℝ f2) natℝ-one))) stepB

-- **可证**：2^j 嵌入 = (natℝ 2)^j（归纳 j，natℝ-*）
nat-pow-embed : (j : ℕ) → natℝ (2^ j) ≡ ((natℝ 2) ^ℕ j)
nat-pow-embed zero = natℝ-one
nat-pow-embed (suc j) =
  trans (cong natℝ (2^suc-def j))
        (trans (natℝ-* 2 (2^ j)) (cong (λ w → natℝ 2 *ℝ w) (nat-pow-embed j)))
  where
  -- NATTIMES 绑定下 2^ (suc j) 与 2 *ℕ (2^ j) 不定义性归约，显式搬运
  2^suc-def : (j : ℕ) → 2^ (suc j) ≡ 2 *ℕ (2^ j)
  2^suc-def zero = refl
  2^suc-def (suc j) = refl

-- **可证**：tail-sum 逐项——x^{n+1+j}/(n+1+j)! ≤ (x^{n+1}/(n+1)!)·(x/2)^j
--（pow-add 拆幂 + recip-factorial-strong-le + *-≤-mono-ℝ + div-pow）
tail-term-le : (n j : ℕ) (x : ℝ) → zeroℝ <ℝ x → x <ℝ oneℝ →
  ((x ^ℕ (suc (n +ℕr j))) *ℝ recip-factorial (suc (n +ℕr j)))
    ≤ℝ (((x ^ℕ (suc n)) *ℝ recip-factorial (suc n)) *ℝ (half-x x ^ℕ j))
tail-term-le n j x hx hlt = ≤-trans-ℝ step1 (≤-trans-ℝ step2 final)
  where
  h : ℝ
  h = half-x x
  D : ℝ
  D = x ^ℕ (suc (n +ℕr j))
  X : ℝ
  X = x ^ℕ (suc n)
  Xj : ℝ
  Xj = x ^ℕ j
  R : ℝ
  R = recip-factorial (suc (n +ℕr j))
  Rc : ℝ
  Rc = recip-factorial (suc n)
  Hj : ℝ
  Hj = natℝ 1 /ℝ natℝ (2^ j)
  coef : ℝ
  coef = X *ℝ Rc
  -- D ≡ X·Xj（pow-add + +ℕr-comm-suc）
  eq-D : D ≡ (X *ℝ Xj)
  eq-D = trans (cong (λ w → x ^ℕ w) (sym (+ℕr-comm-suc n j))) (pow-add x (suc n) j)
  -- R ≤ Rc·Hj（recip-factorial-strong-le）
  R-le : R ≤ℝ (Rc *ℝ Hj)
  R-le = recip-factorial-strong-le n j
  -- 0 ≤ D 与 0 ≤ Rc·Hj（乘保序前提）
  D-nonneg : zeroℝ ≤ℝ D
  D-nonneg = <-≤-ℝ (power-pos-ℕ x hx (n +ℕr j))
  RcHj-pos : zeroℝ <ℝ (Rc *ℝ Hj)
  RcHj-pos = lt-*-pos-ℝ (recip-factorial-pos (suc n))
                        (/-pos-ℝ (subst (zeroℝ <ℝ_) (sym natℝ-one) zero-lt-one-ℝ) (natℝ-pos-embed (2^-pos j)))
  -- ① D·R ≤ D·(Rc·Hj)
  step1 : (D *ℝ R) ≤ℝ (D *ℝ (Rc *ℝ Hj))
  step1 = subst (λ u → u ≤ℝ (D *ℝ (Rc *ℝ Hj))) (*-comm-ℝ R D)
          (subst (λ v → (R *ℝ D) ≤ℝ v) (*-comm-ℝ (Rc *ℝ Hj) D)
                 (*-≤-mono-ℝ {a = R} {b = Rc *ℝ Hj} {c = D} D-nonneg R-le))
  -- ② D·(Rc·Hj) ≤ (X·Xj)·(Rc·Hj)
  step2 : (D *ℝ (Rc *ℝ Hj)) ≤ℝ ((X *ℝ Xj) *ℝ (Rc *ℝ Hj))
  step2 = *-≤-mono-ℝ {a = D} {b = X *ℝ Xj} {c = Rc *ℝ Hj} (<-≤-ℝ RcHj-pos)
                     (subst (λ u → D ≤ℝ u) eq-D (refl-≤ℝ {D}))
  -- ③ 代数重排：(X·Xj)·(Rc·Hj) ≡ (X·Rc)·(Xj·Hj)
  step3 : ((X *ℝ Xj) *ℝ (Rc *ℝ Hj)) ≡ (coef *ℝ (Xj *ℝ Hj))
  step3 = trans (*-assoc-ℝ X Xj (Rc *ℝ Hj))
          (trans (cong (λ w → X *ℝ w) (sym (*-assoc-ℝ Xj Rc Hj)))
          (trans (cong (λ w → X *ℝ w) (cong₂ _*ℝ_ (*-comm-ℝ Xj Rc) refl))
          (trans (cong (λ w → X *ℝ w) (*-assoc-ℝ Rc Xj Hj))
                 (sym (*-assoc-ℝ X Rc (Xj *ℝ Hj))))))
  -- ④ Xj·Hj ≡ Xj/2^j ≡ h^j（*-/ℝ + div-pow + nat-pow-embed）
  XjHj-eq : (Xj *ℝ Hj) ≡ ((x ^ℕ j) /ℝ natℝ (2^ j))
  XjHj-eq = trans (*-/ℝ Xj (natℝ 1) (natℝ (2^ j)))
            (cong₂ _/ℝ_ (trans (cong (λ w → Xj *ℝ w) natℝ-one) (*-ident-ℝ Xj)) refl)
  h-eq : (half-x x ^ℕ j) ≡ ((x ^ℕ j) /ℝ natℝ (2^ j))
  h-eq = trans (div-pow x (natℝ 2) j) (cong₂ _/ℝ_ refl (sym (nat-pow-embed j)))
  -- 最终：≤ 链收于 系数·h^j
  final : ((X *ℝ Xj) *ℝ (Rc *ℝ Hj)) ≤ℝ (coef *ℝ (h ^ℕ j))
  final = subst (λ v → ((X *ℝ Xj) *ℝ (Rc *ℝ Hj)) ≤ℝ (coef *ℝ v))
                (sym h-eq)
                (subst (λ u → u ≤ℝ (coef *ℝ ((x ^ℕ j) /ℝ natℝ (2^ j))))
                       (sym step3)
                       (subst (λ w → (coef *ℝ (Xj *ℝ Hj)) ≤ℝ w) (cong₂ _*ℝ_ refl XjHj-eq) (refl-≤ℝ)))

-- ==================================================================
-- 固定间隙路径·尾部求和（exp-tail-bound 降定理，2026-08-05）
-- 目标：T_n(m) ≤ x^{n+1}/(n+1)!·geo-x(x/2,m)（归纳求和：逐项 tail-term-le +
--   ≤-+-mono-r-ℝ + distrib 反向），全部**可证**。
-- ==================================================================

-- **可证**：geo-x (x/2) < 1/(1−x/2)（geo-x-lt 特化；x/2 > 0 且 x/2 < 1）
geo-half-lt : (x : ℝ) → zeroℝ <ℝ x → x <ℝ oneℝ → (m : ℕ) →
  geo-x (half-x x) m <ℝ (oneℝ /ℝ (oneℝ -ℝ half-x x))
geo-half-lt x hx hlt m = geo-x-lt (half-x x) (div-half-pos hx) (div-half-lt-one hlt) m

-- **可证**：tail-sum 和式 ≤ 系数·geo-x(x/2,m)
--（归纳 m：base 定义性 + *-ident-ℝ；step 逐项 tail-term-le + 加法保序 + 分配律）
tail-sum-le : (n m : ℕ) (x : ℝ) → zeroℝ <ℝ x → x <ℝ oneℝ →
  tail-sum n m x ≤ℝ (((x ^ℕ (suc n)) *ℝ recip-factorial (suc n)) *ℝ geo-x (half-x x) m)
tail-sum-le n zero x hx hlt =
  subst (λ u → coef ≤ℝ u) (sym (*-ident-ℝ coef)) (refl-≤ℝ)
  where
  coef : ℝ
  coef = (x ^ℕ (suc n)) *ℝ recip-factorial (suc n)
tail-sum-le n (suc m) x hx hlt =
  ≤-trans-ℝ stepA (≤-trans-ℝ stepB stepC)
  where
  h : ℝ
  h = half-x x
  coef : ℝ
  coef = (x ^ℕ (suc n)) *ℝ recip-factorial (suc n)
  T : ℝ
  T = (x ^ℕ (suc (suc (n +ℕr m)))) *ℝ recip-factorial (suc (suc (n +ℕr m)))
  -- 逐项：T ≤ coef·h^{suc m}
  T-le : T ≤ℝ (coef *ℝ (h ^ℕ (suc m)))
  T-le = tail-term-le n (suc m) x hx hlt
  -- 归纳：tail-sum n m x ≤ coef·geo-x h m
  IH : tail-sum n m x ≤ℝ (coef *ℝ geo-x h m)
  IH = tail-sum-le n m x hx hlt
  -- ① 和式 ≤ coef·geo-x h m + T
  stepA : (tail-sum n m x +ℝ T) ≤ℝ ((coef *ℝ geo-x h m) +ℝ T)
  stepA = ≤-+-mono-r-ℝ {a = tail-sum n m x} {b = coef *ℝ geo-x h m} {c = T} IH
  -- ② ≤ coef·geo-x h m + coef·h^{suc m}
  stepB : ((coef *ℝ geo-x h m) +ℝ T) ≤ℝ ((coef *ℝ geo-x h m) +ℝ (coef *ℝ (h ^ℕ (suc m))))
  stepB = subst (λ v → ((coef *ℝ geo-x h m) +ℝ T) ≤ℝ v)
                (sym (+-comm-ℝ (coef *ℝ geo-x h m) (coef *ℝ (h ^ℕ (suc m)))))
          (subst (λ u → u ≤ℝ ((coef *ℝ (h ^ℕ (suc m))) +ℝ (coef *ℝ geo-x h m)))
                 (+-comm-ℝ T (coef *ℝ geo-x h m))
                 (≤-+-mono-r-ℝ {a = T} {b = coef *ℝ (h ^ℕ (suc m))} {c = coef *ℝ geo-x h m} T-le))
  -- ③ = coef·geo-x h (suc m)（分配律反向 + geo-x 定义）
  stepC : ((coef *ℝ geo-x h m) +ℝ (coef *ℝ (h ^ℕ (suc m)))) ≤ℝ (coef *ℝ geo-x h (suc m))
  stepC = subst (λ u → ((coef *ℝ geo-x h m) +ℝ (coef *ℝ (h ^ℕ (suc m)))) ≤ℝ u)
                (trans (sym (distrib-ℝ coef (geo-x h m) (h ^ℕ (suc m))))
                       (cong (λ w → coef *ℝ w) (sym geo-x-def)))
                (refl-≤ℝ)
    where
    -- geo-x h (suc m) ≡ geo-x h m + h^{suc m}（定义性）
    geo-x-def : geo-x h (suc m) ≡ (geo-x h m +ℝ (h ^ℕ (suc m)))
    geo-x-def = refl

-- ==================================================================
-- 固定间隙路径·sup 组合（exp-tail-bound 降定理收官，2026-08-05）
-- 目标：∀k 部分和 ≤ S_n + 系数·1/(1−x/2)（B''，固定）⟹ exp x ≤ B''
--   < S_n + 系数·1/(1−x)（B，recip-half-gap）⟹ exp-tail-bound 降为可证定理。
-- 全部**可证**，零新增公理。
-- ==================================================================

-- **可证**：≤ 后继分解——n ≤ suc k ⟹ n = suc k 或 n ≤ k
≤-suc-decomp : {n k : ℕ} → n ≤ℕ suc k → (n ≡ suc k) ⊎ (n ≤ℕ k)
≤-suc-decomp {zero} {k} z≤n = inj₂ z≤n
≤-suc-decomp {suc zero} {zero} (s≤s z≤n) = inj₁ refl
≤-suc-decomp {suc n} {suc k} (s≤s h) with ≤-suc-decomp {n} {k} h
≤-suc-decomp {suc n} {suc k} (s≤s h) | inj₁ e = inj₁ (cong suc e)
≤-suc-decomp {suc n} {suc k} (s≤s h) | inj₂ h' = inj₂ (s≤s h')

-- **可证**：ℕ 层 ≤ 三分——a ≤ b 或 b ≤ a
≤-total : (a b : ℕ) → (a ≤ℕ b) ⊎ (b ≤ℕ a)
≤-total zero b = inj₁ z≤n
≤-total (suc a) zero = inj₂ z≤n
≤-total (suc a) (suc b) with ≤-total a b
≤-total (suc a) (suc b) | inj₁ h = inj₁ (s≤s h)
≤-total (suc a) (suc b) | inj₂ h = inj₂ (s≤s h)

-- **可证**：0 +ℕr k = k（归纳 k）
+ℕr-zero-l : (k : ℕ) → 0 +ℕr k ≡ k
+ℕr-zero-l zero = refl
+ℕr-zero-l (suc k) = cong suc (+ℕr-zero-l k)

-- **可证**：n ≤ k ⟹ n +ℕr (k ∸ n) = k（截断减法 = 差）
+ℕr-∸ : (n k : ℕ) → n ≤ℕ k → n +ℕr (k ∸ n) ≡ k
+ℕr-∸ zero k z≤n = trans (cong (λ w → 0 +ℕr w) (∸-zero k)) (+ℕr-zero-l k)
+ℕr-∸ (suc n) (suc k) (s≤s h) = trans (+ℕr-comm-suc n (k ∸ n)) (cong suc (+ℕr-∸ n k h))

-- **可证**：k ≥ n+1 ⟹ k = suc (n +ℕr (k ∸ (n+1)))
tail-repr : (n k : ℕ) → suc n ≤ℕ k → suc (n +ℕr (k ∸ (suc n))) ≡ k
tail-repr n zero ()
tail-repr n (suc k) (s≤s h) = cong suc (+ℕr-∸ n k h)

-- **可证**：部分和单步递增（≤ 版）——S_n ≤ S_{n+1}（项正）
exp-partial-suc-≤ : (n : ℕ) (x : ℝ) → zeroℝ <ℝ x → exp-partial-at n x ≤ℝ exp-partial-at (suc n) x
exp-partial-suc-≤ n x hx =
  <-≤-ℝ (add-pos-ℝ {x = exp-partial-at n x}
                    {y = (x ^ℕ (suc n)) *ℝ recip-factorial (suc n)}
                    (lt-*-pos-ℝ (power-pos-ℕ x hx n) (recip-factorial-pos (suc n))))

-- **可证**：部分和递增（≤ 版）——n ≤ k ⟹ S_n ≤ S_k（归纳 k，≤-suc-decomp）
exp-partial-at-le : (n k : ℕ) → n ≤ℕ k → (x : ℝ) → zeroℝ <ℝ x →
  exp-partial-at n x ≤ℝ exp-partial-at k x
exp-partial-at-le n zero nk x hx with nk
... | z≤n = refl-≤ℝ
exp-partial-at-le n (suc k) nk x hx with ≤-suc-decomp {n} {k} nk
... | inj₁ e =
  subst (λ z → exp-partial-at n x ≤ℝ exp-partial-at z x) e (refl-≤ℝ)
... | inj₂ h' =
  ≤-trans-ℝ (exp-partial-at-le n k h' x hx) (exp-partial-suc-≤ k x hx)

-- 固定间隙上界 B'' = S_n + 系数·1/(1−x/2)
B''-ub : ℕ → ℝ → ℝ
B''-ub n x = exp-partial-at n x +ℝ (((x ^ℕ (suc n)) *ℝ recip-factorial (suc n)) *ℝ (oneℝ /ℝ (oneℝ -ℝ half-x x)))

-- **可证**：尾部部分和 S_{n+1+m} < B''（tail-sum-le + geo-half-lt + 乘正 + 加法严格）
tail-lt-B'' : (n m : ℕ) (x : ℝ) → zeroℝ <ℝ x → x <ℝ oneℝ →
  exp-partial-at (suc (n +ℕr m)) x <ℝ B''-ub n x
tail-lt-B'' n m x hx hlt =
  subst (λ u → u <ℝ (B''-ub n x)) (sym (exp-decomp n m x))
        (≤-lt-trans-ℝ stepA
                      (lt-+-mono-r-ℝ {a = exp-partial-at n x} {b = coef *ℝ geo-x h m}
                                     {c = coef *ℝ G''} coefgeo-lt))
  where
  h : ℝ
  h = half-x x
  coef : ℝ
  coef = (x ^ℕ (suc n)) *ℝ recip-factorial (suc n)
  G'' : ℝ
  G'' = oneℝ /ℝ (oneℝ -ℝ half-x x)
  coef-pos : zeroℝ <ℝ coef
  coef-pos = lt-*-pos-ℝ (power-pos-ℕ x hx n) (recip-factorial-pos (suc n))
  -- coef·geo-x h m < coef·G''（geo-half-lt 乘正）
  coefgeo-lt : (coef *ℝ geo-x h m) <ℝ (coef *ℝ G'')
  coefgeo-lt = *-pos-mono-ℝ {a = geo-x h m} {b = G''} {c = coef} coef-pos (geo-half-lt x hx hlt m)
  -- S_n + tail-sum ≤ S_n + coef·geo-x h m（tail-sum-le + 交换）
  stepA : (exp-partial-at n x +ℝ tail-sum n m x) ≤ℝ (exp-partial-at n x +ℝ (coef *ℝ geo-x h m))
  stepA = subst (λ v → (exp-partial-at n x +ℝ tail-sum n m x) ≤ℝ v)
                (sym (+-comm-ℝ (exp-partial-at n x) (coef *ℝ geo-x h m)))
          (subst (λ u → u ≤ℝ ((coef *ℝ geo-x h m) +ℝ (exp-partial-at n x)))
                 (+-comm-ℝ (tail-sum n m x) (exp-partial-at n x))
                 (≤-+-mono-r-ℝ {a = tail-sum n m x} {b = coef *ℝ geo-x h m}
                               {c = exp-partial-at n x} (tail-sum-le n m x hx hlt)))

-- **可证**：k ≤ n+1 ⟹ S_k ≤ B''（递增 + coef < coef·G''，1 < G''）
partial-suc-le-B'' : (n k : ℕ) → k ≤ℕ suc n → (x : ℝ) → zeroℝ <ℝ x → x <ℝ oneℝ →
  exp-partial-at k x ≤ℝ B''-ub n x
partial-suc-le-B'' n k hk x hx hlt =
  <-≤-ℝ (≤-lt-trans-ℝ (exp-partial-at-le k (suc n) hk x hx)
         (lt-+-mono-r-ℝ {a = exp-partial-at n x} {b = coef} {c = coef *ℝ G''} coef-lt))
  where
  coef : ℝ
  coef = (x ^ℕ (suc n)) *ℝ recip-factorial (suc n)
  G'' : ℝ
  G'' = oneℝ /ℝ (oneℝ -ℝ half-x x)
  coef-pos : zeroℝ <ℝ coef
  coef-pos = lt-*-pos-ℝ (power-pos-ℕ x hx n) (recip-factorial-pos (suc n))
  -- coef < coef·G''（1 < G''：x/2 > 0、x/2 < 1）
  coef-lt : coef <ℝ (coef *ℝ G'')
  coef-lt = subst (λ z → z <ℝ (coef *ℝ G'')) (*-ident-ℝ coef)
            (*-pos-mono-ℝ {a = oneℝ} {b = G''} {c = coef} coef-pos
                          (G-gt-one (div-half-pos hx) (div-half-lt-one hlt)))

-- **可证**：∀k 部分和 ≤ B''（≤-total 三分：k ≤ n+1 或 k ≥ n+1 经 tail-repr）
all-partial-le-B'' : (n k : ℕ) (x : ℝ) → zeroℝ <ℝ x → x <ℝ oneℝ → exp-partial-at k x ≤ℝ B''-ub n x
all-partial-le-B'' n k x hx hlt with ≤-total k (suc n)
all-partial-le-B'' n k x hx hlt | inj₁ hk = partial-suc-le-B'' n k hk x hx hlt
all-partial-le-B'' n k x hx hlt | inj₂ hn =
  <-≤-ℝ (subst (λ z → exp-partial-at z x <ℝ B''-ub n x) (tail-repr n k hn)
               (tail-lt-B'' n (k ∸ suc n) x hx hlt))

-- **可证**：exp x ≤ B''（exp 最小上界 + ∀k 部分和 ≤ B''）
exp-le-B'' : (n : ℕ) (x : ℝ) → zeroℝ <ℝ x → x <ℝ oneℝ → exp x ≤ℝ B''-ub n x
exp-le-B'' n x hx hlt = exp-least-ub-any x (B''-ub n x) (λ k → all-partial-le-B'' n k x hx hlt)

-- **可证**：B'' < B'（recip-half-gap 乘正 + 加法严格）——固定间隙，sup 保持严格
B''-lt-B' : (n : ℕ) (x : ℝ) → zeroℝ <ℝ x → x <ℝ oneℝ →
  B''-ub n x <ℝ (exp-partial-at n x +ℝ (((x ^ℕ (suc n)) *ℝ recip-factorial (suc n)) *ℝ (oneℝ /ℝ (oneℝ -ℝ x))))
B''-lt-B' n x hx hlt =
  lt-+-mono-r-ℝ {a = exp-partial-at n x} {b = coef *ℝ G''} {c = coef *ℝ G'}
                (*-pos-mono-ℝ {a = G''} {b = G'} {c = coef} coef-pos (recip-half-gap hx hlt))
  where
  coef : ℝ
  coef = (x ^ℕ (suc n)) *ℝ recip-factorial (suc n)
  G'' : ℝ
  G'' = oneℝ /ℝ (oneℝ -ℝ half-x x)
  G' : ℝ
  G' = oneℝ /ℝ (oneℝ -ℝ x)
  coef-pos : zeroℝ <ℝ coef
  coef-pos = lt-*-pos-ℝ (power-pos-ℕ x hx n) (recip-factorial-pos (suc n))

-- **可证**：exp-tail-bound 降定理（原 postulate 闭合）——0 < x < 1 ⟹
--   exp x < S_n(x) + x^{n+1}/(n+1)!·1/(1−x)（固定间隙路径：exp ≤ B'' < B'）
exp-tail-bound-thm : (n : ℕ) (x : ℝ) → zeroℝ <ℝ x → x <ℝ oneℝ →
  exp x <ℝ (exp-partial-at n x +ℝ (((x ^ℕ (suc n)) *ℝ recip-factorial (suc n)) *ℝ (oneℝ /ℝ (oneℝ -ℝ x))))
exp-tail-bound-thm n x hx hlt = ≤-lt-trans-ℝ (exp-le-B'' n x hx hlt) (B''-lt-B' n x hx hlt)

-- (a/b)·(c/a) = c/b（分子分母对消，可证：mul-div-ℝ + frac-cancel-ℝ）
cancel-div : (a b c : ℝ) → (a /ℝ b) *ℝ (c /ℝ a) ≡ (c /ℝ b)
cancel-div a b c =
  trans (mul-div-ℝ a c b a)
    (trans (cong (λ u → u /ℝ (b *ℝ a)) (*-comm-ℝ a c))
           (frac-cancel-ℝ c b a))

-- 分数放大（可证）：a/c = (a·d)/(c·d)
frac-scaled-ℝ : (a c d : ℝ) → (a /ℝ c) ≡ ((a *ℝ d) /ℝ (c *ℝ d))
frac-scaled-ℝ a c d = /-cross-ℝ {a = a} {b = a *ℝ d} {c = c} {d = c *ℝ d}
  (trans (cong (λ u → a *ℝ u) (*-comm-ℝ c d)) (sym (*-assoc-ℝ a d c)))

-- x = 29/450；x² = x·x
x-29-450 : ℝ
x-29-450 = natℝ 29 /ℝ natℝ 450

x2 : ℝ
x2 = x-29-450 *ℝ x-29-450

-- x > 0、x² > 0、15/29 > 0
x-pos-29-450 : zeroℝ <ℝ x-29-450
x-pos-29-450 = /-pos-ℝ (natℝ-pos-embed z<s) (natℝ-pos-embed z<s)

x2-pos : zeroℝ <ℝ x2
x2-pos = lt-*-pos-ℝ x-pos-29-450 x-pos-29-450

pos-15-29 : zeroℝ <ℝ (natℝ 15 /ℝ natℝ 29)
pos-15-29 = /-pos-ℝ (natℝ-pos-embed z<s) (natℝ-pos-embed z<s)

-- x < 1/15（29/450 < 30/450 = 1/15，29 < 30）
x-lt-15th : x-29-450 <ℝ (natℝ 1 /ℝ natℝ 15)
x-lt-15th = subst (λ y → x-29-450 <ℝ y) one-15th-eq
                  (/-lt-same-den-ℝ {natℝ 29} {natℝ 30} {natℝ 450} (natℝ-<-embed (<-suc 29)))
  where
  one-15th-eq : (natℝ 30 /ℝ natℝ 450) ≡ (natℝ 1 /ℝ natℝ 15)
  one-15th-eq = /-cross-ℝ (trans (sym (natℝ-* 30 15)) (natℝ-* 1 450))

-- 1/15 < 1/10（倒数单调：0 < 10 < 15）
one-15th-lt-tenth : (natℝ 1 /ℝ natℝ 15) <ℝ (natℝ 1 /ℝ natℝ 10)
one-15th-lt-tenth =
  subst (λ v → (natℝ 1 /ℝ natℝ 15) <ℝ v) (sym e2)
  (subst (λ u → u <ℝ (oneℝ /ℝ natℝ 10)) (sym e1)
         (recip-mono-ℝ {a = natℝ 10} {b = natℝ 15} (natℝ-pos-embed z<s) (natℝ-<-embed 10-lt-15)))
  where
  e1 : (natℝ 1 /ℝ natℝ 15) ≡ (oneℝ /ℝ natℝ 15)
  e1 = cong₂ _/ℝ_ natℝ-one refl
  e2 : (natℝ 1 /ℝ natℝ 10) ≡ (oneℝ /ℝ natℝ 10)
  e2 = cong₂ _/ℝ_ natℝ-one refl
  10-lt-15 : 10 <ℕ 15
  10-lt-15 = <-trans (<-suc 10) (<-trans (<-suc 11) (<-trans (<-suc 12) (<-trans (<-suc 13) (<-suc 14))))

-- x < 1/10（经 1/15 传递）
x-lt-tenth : x-29-450 <ℝ (natℝ 1 /ℝ natℝ 10)
x-lt-tenth = trans-<ℝ x-lt-15th one-15th-lt-tenth

-- x² < x·(1/15)（x > 0 且 x < 1/15）
x-sq-lt-x-15th : x2 <ℝ (x-29-450 *ℝ (natℝ 1 /ℝ natℝ 15))
x-sq-lt-x-15th = *-pos-mono-ℝ {a = x-29-450} {b = natℝ 1 /ℝ natℝ 15} {c = x-29-450} x-pos-29-450 x-lt-15th

-- x·(1/15) = 29/6750
x-mul-15th : x-29-450 *ℝ (natℝ 1 /ℝ natℝ 15) ≡ (natℝ 29 /ℝ natℝ 6750)
x-mul-15th =
  trans (mul-div-ℝ (natℝ 29) (natℝ 1) (natℝ 450) (natℝ 15))
        (cong₂ _/ℝ_ m29 den6750)
  where
  m29 : (natℝ 29 *ℝ natℝ 1) ≡ natℝ 29
  m29 = sym (natℝ-* 29 1)
  den6750 : (natℝ 450 *ℝ natℝ 15) ≡ natℝ 6750
  den6750 = sym (natℝ-* 450 15)

-- x² < 29/6750
x-sq-lt-29-6750 : x2 <ℝ (natℝ 29 /ℝ natℝ 6750)
x-sq-lt-29-6750 = subst (λ y → x2 <ℝ y) x-mul-15th x-sq-lt-x-15th

-- 系数和：1/2 + 1/60 + 1/2160 = 1117/2160（1/2 = 1080/2160、1/60 = 36/2160）
half-2160 : (natℝ 1 /ℝ natℝ 2) ≡ (natℝ 1080 /ℝ natℝ 2160)
half-2160 = /-cross-ℝ (trans (sym (natℝ-* 1 2160)) (natℝ-* 1080 2))

one60-2160 : (natℝ 1 /ℝ natℝ 60) ≡ (natℝ 36 /ℝ natℝ 2160)
one60-2160 = /-cross-ℝ (trans (sym (natℝ-* 1 2160)) (natℝ-* 36 60))

-- 同分母分数加法（本地版，复刻 /-add-same-ℝ，避免前向引用）
same-den-add : (a b c : ℝ) → (a /ℝ c) +ℝ (b /ℝ c) ≡ ((a +ℝ b) /ℝ c)
same-den-add a b c =
  trans (/-add-ℝ a b c c)
        (/-cross-ℝ (trans (*-comm-ℝ ((a *ℝ c) +ℝ (b *ℝ c)) c)
                          (trans (distrib-ℝ c (a *ℝ c) (b *ℝ c))
                                 (trans (cong₂ _+ℝ_ c-mul-ac c-mul-bc)
                                        (trans (cong₂ _+ℝ_ (*-comm-ℝ a (c *ℝ c)) (*-comm-ℝ b (c *ℝ c)))
                                               (trans (sym (distrib-ℝ (c *ℝ c) a b))
                                                      (*-comm-ℝ (c *ℝ c) (a +ℝ b))))))))
  where
  c-mul-ac : (c *ℝ (a *ℝ c)) ≡ (a *ℝ (c *ℝ c))
  c-mul-ac =
    trans (sym (*-assoc-ℝ c a c))
          (trans (cong (λ x → x *ℝ c) (*-comm-ℝ c a))
                 (*-assoc-ℝ a c c))
  c-mul-bc : (c *ℝ (b *ℝ c)) ≡ (b *ℝ (c *ℝ c))
  c-mul-bc =
    trans (sym (*-assoc-ℝ c b c))
          (trans (cong (λ x → x *ℝ c) (*-comm-ℝ c b))
                 (*-assoc-ℝ b c c))

coeff-sum : ((natℝ 1 /ℝ natℝ 2) +ℝ (natℝ 1 /ℝ natℝ 60)) +ℝ (natℝ 1 /ℝ natℝ 2160)
            ≡ (natℝ 1117 /ℝ natℝ 2160)
coeff-sum =
  trans (cong (λ u → u +ℝ (natℝ 1 /ℝ natℝ 2160)) inner)
        (trans (same-den-add (natℝ 1116) (natℝ 1) (natℝ 2160))
               (cong₂ _/ℝ_ n1117 refl))
  where
  n1116 : (natℝ 1080 +ℝ natℝ 36) ≡ natℝ 1116
  n1116 = sym (natℝ-+ 1080 36)
  n1117 : (natℝ 1116 +ℝ natℝ 1) ≡ natℝ 1117
  n1117 = sym (natℝ-+ 1116 1)
  inner : (natℝ 1 /ℝ natℝ 2) +ℝ (natℝ 1 /ℝ natℝ 60) ≡ (natℝ 1116 /ℝ natℝ 2160)
  inner = trans (cong₂ _+ℝ_ half-2160 one60-2160)
                (trans (same-den-add (natℝ 1080) (natℝ 36) (natℝ 2160))
                       (cong₂ _/ℝ_ n1116 refl))

-- 32393 < 32400（ℕ 层，<-add-r + 定义性归约 32393 + 7 = 32400）
+eq-32393 : 32393 +ℕ 7 ≡ 32400
+eq-32393 = refl

32393<32400 : 32393 <ℕ 32400
32393<32400 = subst (λ n → 32393 <ℕ n) (sym +eq-32393) (<-add-r 32393 6)

-- 1117/2160 < 15/29（交叉乘积 32393 < 32400）
C-lt-15-29 : (natℝ 1117 /ℝ natℝ 2160) <ℝ (natℝ 15 /ℝ natℝ 29)
C-lt-15-29 =
  subst (λ y → (natℝ 1117 /ℝ natℝ 2160) <ℝ y) (sym r15)
  (subst (λ x → x <ℝ ((natℝ 15 *ℝ natℝ 2160) /ℝ (natℝ 29 *ℝ natℝ 2160))) (sym r1117)
  (subst (λ d → ((natℝ 1117 *ℝ natℝ 29) /ℝ (natℝ 2160 *ℝ natℝ 29)) <ℝ ((natℝ 15 *ℝ natℝ 2160) /ℝ d)) denom-comm
  (/-lt-same-den-ℝ {natℝ 1117 *ℝ natℝ 29} {natℝ 15 *ℝ natℝ 2160} {natℝ 2160 *ℝ natℝ 29} cross-lt)))
  where
  r1117 : (natℝ 1117 /ℝ natℝ 2160) ≡ ((natℝ 1117 *ℝ natℝ 29) /ℝ (natℝ 2160 *ℝ natℝ 29))
  r1117 = frac-scaled-ℝ (natℝ 1117) (natℝ 2160) (natℝ 29)
  r15 : (natℝ 15 /ℝ natℝ 29) ≡ ((natℝ 15 *ℝ natℝ 2160) /ℝ (natℝ 29 *ℝ natℝ 2160))
  r15 = frac-scaled-ℝ (natℝ 15) (natℝ 29) (natℝ 2160)
  denom-comm : (natℝ 2160 *ℝ natℝ 29) ≡ (natℝ 29 *ℝ natℝ 2160)
  denom-comm = *-comm-ℝ (natℝ 2160) (natℝ 29)
  m1 : (natℝ 1117 *ℝ natℝ 29) ≡ natℝ 32393
  m1 = sym (natℝ-* 1117 29)
  m2 : (natℝ 15 *ℝ natℝ 2160) ≡ natℝ 32400
  m2 = sym (natℝ-* 15 2160)
  cross-lt : (natℝ 1117 *ℝ natℝ 29) <ℝ (natℝ 15 *ℝ natℝ 2160)
  cross-lt = subst (λ x → x <ℝ (natℝ 15 *ℝ natℝ 2160)) (sym m1)
             (subst (λ y → natℝ 32393 <ℝ y) (sym m2) (natℝ-<-embed 32393<32400))

-- ==================================================================
-- §2b 续：S₃ 计算、尾部界、x² 块界与 ln1615-lb 闭合
-- ==================================================================

-- 幂（迭代乘法定义性展开，可证）
pow1 : (x : ℝ) → (x ^ℕ 1) ≡ x
pow1 x = *-ident-ℝ x

pow2 : (x : ℝ) → (x ^ℕ 2) ≡ (x *ℝ x)
pow2 x = cong (λ u → x *ℝ u) (*-ident-ℝ x)

pow3 : (x : ℝ) → (x ^ℕ 3) ≡ ((x *ℝ x) *ℝ x)
pow3 x = trans (cong (λ u → x *ℝ u) (pow2 x)) (sym (*-assoc-ℝ x x x))

-- x^ℕ 4 = (x·x)·(x·x)
x4 : ℝ
x4 = x2 *ℝ x2

pow4-x : (x-29-450 ^ℕ 4) ≡ x4
pow4-x =
  trans (cong (λ u → x-29-450 *ℝ u) (pow3 x-29-450))
        (trans (sym (*-assoc-ℝ x-29-450 x2 x-29-450))
               (trans (cong (λ u → u *ℝ x-29-450) (sym (*-assoc-ℝ x-29-450 x-29-450 x-29-450)))
                      (*-assoc-ℝ x2 x-29-450 x-29-450)))

-- 单位分数具体值（factorial 定义性归约）
rf1 : recip-factorial 1 ≡ oneℝ
rf1 = trans (cong₂ _/ℝ_ refl natℝ-one) (trans (div-one-ℝ (natℝ 1)) natℝ-one)

rf2 : recip-factorial 2 ≡ (natℝ 1 /ℝ natℝ 2)
rf2 = refl

rf3 : recip-factorial 3 ≡ (natℝ 1 /ℝ natℝ 6)
rf3 = refl

rf4 : recip-factorial 4 ≡ (natℝ 1 /ℝ natℝ 24)
rf4 = refl

-- S₃ 项：x·1、x²/2、x³/6
term1-x : (x-29-450 ^ℕ 1) *ℝ recip-factorial 1 ≡ x-29-450
term1-x = trans (cong₂ _*ℝ_ (pow1 x-29-450) rf1) (*-ident-ℝ x-29-450)

term2-x : (x-29-450 ^ℕ 2) *ℝ recip-factorial 2 ≡ x2 /ℝ (natℝ 2)
term2-x =
  trans (cong₂ _*ℝ_ (pow2 x-29-450) refl)
        (trans (*-/ℝ x2 (natℝ 1) (natℝ 2))
               (cong₂ _/ℝ_ (trans (cong₂ _*ℝ_ refl natℝ-one) (*-ident-ℝ x2)) refl))

x3-6 : ℝ
x3-6 = (x2 *ℝ x-29-450) /ℝ (natℝ 6)

term3-x : (x-29-450 ^ℕ 3) *ℝ recip-factorial 3 ≡ x3-6
term3-x =
  trans (cong₂ _*ℝ_ (pow3 x-29-450) refl)
        (trans (*-/ℝ (x2 *ℝ x-29-450) (natℝ 1) (natℝ 6))
               (cong₂ _/ℝ_ (trans (cong₂ _*ℝ_ refl natℝ-one) (*-ident-ℝ (x2 *ℝ x-29-450))) refl))

-- S₃ = exp-partial-at 3 x ≡ ((1 + x) + x²/2) + x³/6
S3-value : exp-partial-at 3 x-29-450 ≡ ((oneℝ +ℝ x-29-450) +ℝ (x2 /ℝ (natℝ 2))) +ℝ x3-6
S3-value =
  trans (cong (λ u → u +ℝ ((x-29-450 ^ℕ 3) *ℝ recip-factorial 3)) s2)
        (cong (λ u → ((oneℝ +ℝ x-29-450) +ℝ (x2 /ℝ (natℝ 2))) +ℝ u) term3-x)
  where
  s1 : exp-partial-at 1 x-29-450 ≡ oneℝ +ℝ x-29-450
  s1 = cong (λ u → oneℝ +ℝ u) term1-x
  s2 : exp-partial-at 2 x-29-450 ≡ (oneℝ +ℝ x-29-450) +ℝ (x2 /ℝ (natℝ 2))
  s2 = trans (cong (λ u → u +ℝ ((x-29-450 ^ℕ 2) *ℝ recip-factorial 2)) s1)
             (cong (λ u → (oneℝ +ℝ x-29-450) +ℝ u) term2-x)

-- x² < 1/100（x < 1/10）
x2-lt-1-100 : x2 <ℝ (natℝ 1 /ℝ natℝ 100)
x2-lt-1-100 = subst (λ y → x2 <ℝ y) tenth-sq
  (trans-<ℝ x-sq-lt-tenth tenth-lt-tenth-sq)
  where
  x-sq-lt-tenth : x2 <ℝ (x-29-450 *ℝ (natℝ 1 /ℝ natℝ 10))
  x-sq-lt-tenth = *-pos-mono-ℝ {a = x-29-450} {b = natℝ 1 /ℝ natℝ 10} {c = x-29-450} x-pos-29-450 x-lt-tenth
  tenth-lt-tenth-sq : (x-29-450 *ℝ (natℝ 1 /ℝ natℝ 10)) <ℝ ((natℝ 1 /ℝ natℝ 10) *ℝ (natℝ 1 /ℝ natℝ 10))
  tenth-lt-tenth-sq =
    subst (λ u → u <ℝ ((natℝ 1 /ℝ natℝ 10) *ℝ (natℝ 1 /ℝ natℝ 10))) (sym (*-comm-ℝ x-29-450 (natℝ 1 /ℝ natℝ 10)))
    (*-pos-mono-ℝ {a = x-29-450} {b = natℝ 1 /ℝ natℝ 10} {c = natℝ 1 /ℝ natℝ 10}
                  (/-pos-ℝ (natℝ-pos-embed z<s) (natℝ-pos-embed z<s)) x-lt-tenth)
  tenth-sq : ((natℝ 1 /ℝ natℝ 10) *ℝ (natℝ 1 /ℝ natℝ 10)) ≡ (natℝ 1 /ℝ natℝ 100)
  tenth-sq = trans (mul-div-ℝ (natℝ 1) (natℝ 1) (natℝ 10) (natℝ 10))
                   (cong₂ _/ℝ_ (sym (natℝ-* 1 1)) (sym (natℝ-* 10 10)))

-- x⁴ < x²·(1/100)
x4-lt-x2-100 : x4 <ℝ (x2 *ℝ (natℝ 1 /ℝ natℝ 100))
x4-lt-x2-100 = *-pos-mono-ℝ {a = x2} {b = natℝ 1 /ℝ natℝ 100} {c = x2} x2-pos x2-lt-1-100

-- 负分数（可证）：-(a/c) = (-a)/c
a-over-c-one : (a c : ℝ) → (a /ℝ c) ≡ a *ℝ (oneℝ /ℝ c)
a-over-c-one a c = trans (cong₂ _/ℝ_ (sym (*-ident-ℝ a)) refl) (sym (*-/ℝ a oneℝ c))

neg-frac-ℝ : (a c : ℝ) → negℝ (a /ℝ c) ≡ (negℝ a) /ℝ c
neg-frac-ℝ a c =
  trans (cong negℝ (a-over-c-one a c))
        (trans (sym (loc-neg-mul a (oneℝ /ℝ c)))
               (trans (*-/ℝ (negℝ a) oneℝ c)
                      (cong₂ _/ℝ_ (*-ident-ℝ (negℝ a)) refl)))
  where
  -- (-x)·y = -(x·y)（仅用域公理；等价于后文顶层 neg-mul-ℝ）
  loc-neg-mul : (x y : ℝ) → (negℝ x) *ℝ y ≡ negℝ (x *ℝ y)
  loc-neg-mul x y =
    loc-neg-unique {a = x *ℝ y} {b = (negℝ x) *ℝ y}
      (trans (sym expand)
             (trans (cong (λ u → u *ℝ y) (+-inv-ℝ x)) (*-zero-l y)))
    where
    -- 加性逆唯一（仅用群公理；等价于后文顶层 neg-unique-ℝ）
    loc-neg-unique : {a b : ℝ} → a +ℝ b ≡ zeroℝ → b ≡ negℝ a
    loc-neg-unique {a} {b} h =
      trans (sym (trans (sym (+-comm-ℝ b zeroℝ)) (+-ident-ℝ b)))
            (trans (cong (λ x → x +ℝ b) (sym (+-inv-ℝ a)))
                   (trans (cong (λ x → x +ℝ b) (+-comm-ℝ a (negℝ a)))
                          (trans (+-assoc-ℝ (negℝ a) a b)
                                 (trans (cong (λ x → negℝ a +ℝ x) h)
                                        (+-ident-ℝ (negℝ a))))))
    -- 0·y = 0（仅用域公理；等价于后文顶层 *-zero-l-ℝ）
    *-zero-l : (y : ℝ) → zeroℝ *ℝ y ≡ zeroℝ
    *-zero-l y = trans (*-comm-ℝ zeroℝ y) (*-zero-ℝ y)
    -- (x + (-x))·y = x·y + (-x)·y
    expand : (x +ℝ negℝ x) *ℝ y ≡ (x *ℝ y) +ℝ ((negℝ x) *ℝ y)
    expand =
      trans (*-comm-ℝ (x +ℝ negℝ x) y)
            (trans (distrib-ℝ y x (negℝ x))
                   (cong₂ _+ℝ_ (*-comm-ℝ y x) (*-comm-ℝ y (negℝ x))))

-- x/6 < 1/60（x < 1/10：x·(1/6) < (1/10)·(1/6) = 1/60）
one-60-eq : ((natℝ 1 /ℝ natℝ 10) *ℝ (natℝ 1 /ℝ natℝ 6)) ≡ (natℝ 1 /ℝ natℝ 60)
one-60-eq = trans (mul-div-ℝ (natℝ 1) (natℝ 1) (natℝ 10) (natℝ 6))
                  (cong₂ _/ℝ_ (sym (natℝ-* 1 1)) (sym (natℝ-* 10 6)))

x-over-6-lt-1-60 : (x-29-450 *ℝ (natℝ 1 /ℝ natℝ 6)) <ℝ (natℝ 1 /ℝ natℝ 60)
x-over-6-lt-1-60 =
  subst (λ w → (x-29-450 *ℝ (natℝ 1 /ℝ natℝ 6)) <ℝ w) one-60-eq
  (subst (λ v → (x-29-450 *ℝ (natℝ 1 /ℝ natℝ 6)) <ℝ v) (*-comm-ℝ (natℝ 1 /ℝ natℝ 6) (natℝ 1 /ℝ natℝ 10))
  (subst (λ u → u <ℝ ((natℝ 1 /ℝ natℝ 6) *ℝ (natℝ 1 /ℝ natℝ 10))) (sym (*-comm-ℝ x-29-450 (natℝ 1 /ℝ natℝ 6)))
  (*-pos-mono-ℝ {a = x-29-450} {b = natℝ 1 /ℝ natℝ 10} {c = natℝ 1 /ℝ natℝ 6}
                (/-pos-ℝ (natℝ-pos-embed z<s) (natℝ-pos-embed z<s)) x-lt-tenth)))

-- x³/6 < x²/60（x³/6 = x²·(x/6)，x/6 < 1/60）
x3-over-6 : x3-6 ≡ x2 *ℝ (x-29-450 *ℝ (natℝ 1 /ℝ natℝ 6))
x3-over-6 =
  trans (sym (*-/ℝ x2 x-29-450 (natℝ 6)))
        (cong (λ u → x2 *ℝ u) (x-over-6))
  where
  x-over-6 : (x-29-450 /ℝ (natℝ 6)) ≡ (x-29-450 *ℝ (natℝ 1 /ℝ natℝ 6))
  x-over-6 = trans (cong₂ _/ℝ_ (trans (sym (*-ident-ℝ x-29-450)) (cong₂ _*ℝ_ refl (sym natℝ-one))) refl)
                   (sym (*-/ℝ x-29-450 (natℝ 1) (natℝ 6)))

x3-6-lt-x2-60 : x3-6 <ℝ (x2 /ℝ (natℝ 60))
x3-6-lt-x2-60 =
  subst (λ y → x3-6 <ℝ y) one60
  (subst (λ x → x <ℝ (x2 *ℝ (natℝ 1 /ℝ natℝ 60))) (sym x3-over-6)
    (*-pos-mono-ℝ {a = x-29-450 *ℝ (natℝ 1 /ℝ natℝ 6)} {b = natℝ 1 /ℝ natℝ 60} {c = x2}
                  x2-pos x-over-6-lt-1-60))
  where
  one60 : (x2 *ℝ (natℝ 1 /ℝ natℝ 60)) ≡ (x2 /ℝ (natℝ 60))
  one60 = trans (*-/ℝ x2 (natℝ 1) (natℝ 60))
                (cong₂ _/ℝ_ (trans (sym (cong₂ _*ℝ_ refl (sym natℝ-one))) (*-ident-ℝ x2)) refl)

-- 9/10 < 1−x（x < 1/10 ⟹ −x > −1/10，1−x = 1+(−x) > 1+(−1/10) = 9/10）
one-tenth : oneℝ ≡ (natℝ 10 /ℝ natℝ 10)
one-tenth = trans (sym nat1-over-1) (/-cross-ℝ (trans (sym (natℝ-* 1 10)) (natℝ-* 10 1)))
  where
  -- (natℝ 1 /ℝ natℝ 1) ≡ oneℝ（natℝ-one + div-one-ℝ 桥接）
  nat1-over-1 : (natℝ 1 /ℝ natℝ 1) ≡ oneℝ
  nat1-over-1 = trans (cong₂ _/ℝ_ natℝ-one refl)
                      (trans (sym (cong₂ _/ℝ_ refl (sym natℝ-one))) (div-one-ℝ oneℝ))

ten-neg-one : (natℝ 10 +ℝ negℝ (natℝ 1)) ≡ natℝ 9
ten-neg-one =
  trans (sym (cong₂ _+ℝ_ (sym (natℝ-+ 9 1)) refl))
        (trans (+-assoc-ℝ (natℝ 9) (natℝ 1) (negℝ (natℝ 1)))
               (trans (cong (λ u → (natℝ 9 +ℝ u)) inv1) (+-ident-ℝ (natℝ 9))))
  where
  inv1 : (natℝ 1 +ℝ negℝ (natℝ 1)) ≡ zeroℝ
  inv1 = trans (cong₂ _+ℝ_ natℝ-one (cong negℝ natℝ-one)) (+-inv-ℝ oneℝ)

one-neg-tenth : (oneℝ +ℝ negℝ (natℝ 1 /ℝ natℝ 10)) ≡ (natℝ 9 /ℝ natℝ 10)
one-neg-tenth =
  subst (λ u → u +ℝ negℝ (natℝ 1 /ℝ natℝ 10) ≡ natℝ 9 /ℝ natℝ 10) (sym one-tenth)
  (subst (λ v → (natℝ 10 /ℝ natℝ 10) +ℝ v ≡ (natℝ 9 /ℝ natℝ 10)) (sym (neg-frac-ℝ (natℝ 1) (natℝ 10)))
    (trans (same-den-add (natℝ 10) (negℝ (natℝ 1)) (natℝ 10))
           (cong₂ _/ℝ_ ten-neg-one refl)))

nine-tenth-lt : (natℝ 9 /ℝ natℝ 10) <ℝ (oneℝ +ℝ negℝ x-29-450)
nine-tenth-lt =
  subst (λ u → u <ℝ (oneℝ +ℝ negℝ x-29-450)) one-neg-tenth
        (lt-+-mono-r-ℝ (neg-<-ℝ x-lt-tenth))

-- ==================================================================
-- §2b 续：尾部界、x² 块界、总装配与 ln1615-lb 闭合
-- ==================================================================

-- 尾部项（与 exp-tail-bound 3 的尾项逐点一致）
T-term : ℝ
T-term = ((x-29-450 ^ℕ 4) *ℝ recip-factorial 4) *ℝ (oneℝ /ℝ (oneℝ -ℝ x-29-450))

T-expand : T-term ≡ (x4 /ℝ (natℝ 24)) *ℝ (oneℝ /ℝ (oneℝ -ℝ x-29-450))
T-expand = cong₂ _*ℝ_ (trans (cong₂ _*ℝ_ pow4-x rf4)
                             (trans (*-/ℝ x4 (natℝ 1) (natℝ 24))
                                    (cong₂ _/ℝ_ (trans (sym (cong₂ _*ℝ_ refl (sym natℝ-one))) (*-ident-ℝ x4)) refl))) refl

-- 1/(9/10) = 10/9
one-over-nine-tenth : (oneℝ /ℝ (natℝ 9 /ℝ natℝ 10)) ≡ (natℝ 10 /ℝ natℝ 9)
one-over-nine-tenth = /-cross-ℝ (trans (one-mul-9) (sym (*-/cancel-ℝ (natℝ 10) (natℝ 9))))
  where
  -- 1·9 = 9（仅用域公理；等价于后文顶层 one-mul-ℝ 实例）
  one-mul-9 : oneℝ *ℝ natℝ 9 ≡ natℝ 9
  one-mul-9 = trans (*-comm-ℝ oneℝ (natℝ 9)) (*-ident-ℝ (natℝ 9))

pos-nine-tenth : zeroℝ <ℝ (natℝ 9 /ℝ natℝ 10)
pos-nine-tenth = /-pos-ℝ (natℝ-pos-embed z<s) (natℝ-pos-embed z<s)

pos-10-9 : zeroℝ <ℝ (natℝ 10 /ℝ natℝ 9)
pos-10-9 = /-pos-ℝ (natℝ-pos-embed z<s) (natℝ-pos-embed z<s)

-- 1/(1−x) < 10/9（9/10 < 1−x，倒数单调）
tail-factor-lt : (oneℝ /ℝ (oneℝ -ℝ x-29-450)) <ℝ (natℝ 10 /ℝ natℝ 9)
tail-factor-lt =
  subst (λ y → (oneℝ /ℝ (oneℝ -ℝ x-29-450)) <ℝ y) one-over-nine-tenth
  (recip-mono-ℝ pos-nine-tenth
    (subst (λ z → (natℝ 9 /ℝ natℝ 10) <ℝ z) (sym (sub-ℝ-def oneℝ x-29-450)) nine-tenth-lt))

-- 尾部 < x²/2160
T-lt : T-term <ℝ (x2 /ℝ (natℝ 2160))
T-lt =
  subst (λ z → z <ℝ (x2 /ℝ (natℝ 2160))) (sym T-expand)
  (subst (λ y → ((x4 /ℝ (natℝ 24)) *ℝ (oneℝ /ℝ (oneℝ -ℝ x-29-450))) <ℝ y) step3-eq
    (trans-<ℝ step1 step2))
  where
  pos-x4-24 : zeroℝ <ℝ (x4 /ℝ (natℝ 24))
  pos-x4-24 = /-pos-ℝ (lt-*-pos-ℝ x2-pos x2-pos) (natℝ-pos-embed z<s)
  step1 : ((x4 /ℝ (natℝ 24)) *ℝ (oneℝ /ℝ (oneℝ -ℝ x-29-450))) <ℝ ((x4 /ℝ (natℝ 24)) *ℝ (natℝ 10 /ℝ natℝ 9))
  step1 = *-pos-mono-ℝ {a = oneℝ /ℝ (oneℝ -ℝ x-29-450)} {b = natℝ 10 /ℝ natℝ 9} {c = x4 /ℝ natℝ 24}
                       pos-x4-24 tail-factor-lt
  x4-24-lt : (x4 /ℝ (natℝ 24)) <ℝ ((x2 *ℝ (natℝ 1 /ℝ natℝ 100)) /ℝ (natℝ 24))
  x4-24-lt = /-lt-same-den-ℝ {x4} {x2 *ℝ (natℝ 1 /ℝ natℝ 100)} {natℝ 24} x4-lt-x2-100
  step2 : ((x4 /ℝ (natℝ 24)) *ℝ (natℝ 10 /ℝ natℝ 9)) <ℝ (((x2 *ℝ (natℝ 1 /ℝ natℝ 100)) /ℝ (natℝ 24)) *ℝ (natℝ 10 /ℝ natℝ 9))
  step2 =
    subst (λ u → u <ℝ (((x2 *ℝ (natℝ 1 /ℝ natℝ 100)) /ℝ (natℝ 24)) *ℝ (natℝ 10 /ℝ natℝ 9)))
          (sym (*-comm-ℝ (x4 /ℝ natℝ 24) (natℝ 10 /ℝ natℝ 9)))
    (subst (λ v → ((natℝ 10 /ℝ natℝ 9) *ℝ (x4 /ℝ natℝ 24)) <ℝ v)
           (sym (*-comm-ℝ ((x2 *ℝ (natℝ 1 /ℝ natℝ 100)) /ℝ (natℝ 24)) (natℝ 10 /ℝ natℝ 9)))
    (*-pos-mono-ℝ {a = x4 /ℝ natℝ 24} {b = (x2 *ℝ (natℝ 1 /ℝ natℝ 100)) /ℝ natℝ 24} {c = natℝ 10 /ℝ natℝ 9}
                  pos-10-9 x4-24-lt))
  step3a : ((x2 *ℝ (natℝ 1 /ℝ natℝ 100)) /ℝ (natℝ 24)) ≡ (x2 /ℝ (natℝ 2400))
  step3a = trans (cong (λ u → u /ℝ (natℝ 24)) (trans (*-/ℝ x2 (natℝ 1) (natℝ 100))
                                                      (cong₂ _/ℝ_ (trans (sym (cong₂ _*ℝ_ refl (sym natℝ-one))) (*-ident-ℝ x2)) refl)))
                 (trans (frac-frac-ℝ x2 (natℝ 100) (natℝ 24))
                        (cong₂ _/ℝ_ refl (sym (natℝ-* 100 24))))
  step3b : (x2 /ℝ (natℝ 2400)) *ℝ (natℝ 10 /ℝ natℝ 9) ≡ (x2 *ℝ (natℝ 10)) /ℝ (natℝ 21600)
  step3b = trans (mul-div-ℝ x2 (natℝ 10) (natℝ 2400) (natℝ 9))
                 (cong₂ _/ℝ_ refl (sym (natℝ-* 2400 9)))
  ten-21600 : (natℝ 10 /ℝ natℝ 21600) ≡ (natℝ 1 /ℝ natℝ 2160)
  ten-21600 = /-cross-ℝ (trans (sym (natℝ-* 10 2160)) (natℝ-* 1 21600))
  step3c : (x2 *ℝ (natℝ 10)) /ℝ (natℝ 21600) ≡ x2 *ℝ (natℝ 1 /ℝ natℝ 2160)
  step3c = trans (sym (*-/ℝ x2 (natℝ 10) (natℝ 21600))) (cong (λ u → x2 *ℝ u) ten-21600)
  step3d : x2 *ℝ (natℝ 1 /ℝ natℝ 2160) ≡ (x2 /ℝ (natℝ 2160))
  step3d = trans (*-/ℝ x2 (natℝ 1) (natℝ 2160))
                 (cong₂ _/ℝ_ (trans (sym (cong₂ _*ℝ_ refl (sym natℝ-one))) (*-ident-ℝ x2)) refl)
  step3-eq : (((x2 *ℝ (natℝ 1 /ℝ natℝ 100)) /ℝ (natℝ 24)) *ℝ (natℝ 10 /ℝ natℝ 9)) ≡ (x2 /ℝ (natℝ 2160))
  step3-eq = trans (cong (λ u → u *ℝ (natℝ 10 /ℝ natℝ 9)) step3a)
             (trans step3b (trans step3c step3d))

-- x²/k = x²·(1/k)
x2-over-k : (k : ℕ) → (x2 /ℝ (natℝ k)) ≡ (x2 *ℝ (natℝ 1 /ℝ natℝ k))
x2-over-k k = trans (cong₂ _/ℝ_ (trans (sym (*-ident-ℝ x2)) (cong₂ _*ℝ_ refl (sym natℝ-one))) refl)
                     (sym (*-/ℝ x2 (natℝ 1) (natℝ k)))

-- x² 块：(x²/2 + x²/60) + x²/2160 = x²·(1117/2160)
x2-block : ℝ
x2-block = ((x2 /ℝ (natℝ 2)) +ℝ (x2 /ℝ (natℝ 60))) +ℝ (x2 /ℝ (natℝ 2160))

x2-block-eq : x2-block ≡ x2 *ℝ (natℝ 1117 /ℝ natℝ 2160)
x2-block-eq =
  trans (cong (λ u → (u +ℝ (x2 /ℝ (natℝ 2160)))) inner1)
        (trans (cong₂ _+ℝ_ refl (x2-over-k 2160))
               (trans (sym (distrib-ℝ x2 ((natℝ 1 /ℝ natℝ 2) +ℝ (natℝ 1 /ℝ natℝ 60)) (natℝ 1 /ℝ natℝ 2160)))
                      (cong (λ u → x2 *ℝ u) coeff-sum)))
  where
  inner1 : (x2 /ℝ (natℝ 2)) +ℝ (x2 /ℝ (natℝ 60)) ≡ x2 *ℝ ((natℝ 1 /ℝ natℝ 2) +ℝ (natℝ 1 /ℝ natℝ 60))
  inner1 = trans (cong₂ _+ℝ_ (x2-over-k 2) (x2-over-k 60))
                 (sym (distrib-ℝ x2 (natℝ 1 /ℝ natℝ 2) (natℝ 1 /ℝ natℝ 60)))

-- (15/29)·(29/6750) = 15/6750
cancel-15-29-6750 : ((natℝ 15 /ℝ natℝ 29) *ℝ (natℝ 29 /ℝ natℝ 6750)) ≡ (natℝ 15 /ℝ natℝ 6750)
cancel-15-29-6750 = trans (*-comm-ℝ (natℝ 15 /ℝ natℝ 29) (natℝ 29 /ℝ natℝ 6750))
                          (cancel-div (natℝ 29) (natℝ 6750) (natℝ 15))

-- 15/6750 = 1/450
fifteen-6750-eq : (natℝ 15 /ℝ natℝ 6750) ≡ (natℝ 1 /ℝ natℝ 450)
fifteen-6750-eq = /-cross-ℝ (trans (sym (natℝ-* 15 450)) (natℝ-* 1 6750))

-- x² 块 < 1/450
x2-block-lt-450 : x2-block <ℝ (natℝ 1 /ℝ natℝ 450)
x2-block-lt-450 =
  subst (λ u → u <ℝ (natℝ 1 /ℝ natℝ 450)) (sym x2-block-eq)
  (subst (λ v → (x2 *ℝ (natℝ 1117 /ℝ natℝ 2160)) <ℝ v) fifteen-6750-eq
  (subst (λ w → (x2 *ℝ (natℝ 1117 /ℝ natℝ 2160)) <ℝ w) cancel-15-29-6750
  (trans-<ℝ (*-pos-mono-ℝ {a = natℝ 1117 /ℝ natℝ 2160} {b = natℝ 15 /ℝ natℝ 29} {c = x2} x2-pos C-lt-15-29)
         (subst (λ z → z <ℝ ((natℝ 15 /ℝ natℝ 29) *ℝ (natℝ 29 /ℝ natℝ 6750))) (sym (*-comm-ℝ x2 (natℝ 15 /ℝ natℝ 29)))
           (*-pos-mono-ℝ {a = x2} {b = natℝ 29 /ℝ natℝ 6750} {c = natℝ 15 /ℝ natℝ 29} pos-15-29 x-sq-lt-29-6750)))))

-- x < 1（经 1/15 < 1）
one-15th-lt-one : (natℝ 1 /ℝ natℝ 15) <ℝ oneℝ
one-15th-lt-one =
  subst (λ y → (natℝ 1 /ℝ natℝ 15) <ℝ y) one-over-one
  (subst (λ y → (natℝ 1 /ℝ natℝ 15) <ℝ y) (cong₂ _/ℝ_ (sym natℝ-one) refl)
  (subst (λ x → x <ℝ (oneℝ /ℝ natℝ 1)) (sym (cong₂ _/ℝ_ natℝ-one refl))
    (recip-mono-ℝ {natℝ 1} {natℝ 15} (natℝ-pos-embed z<s) (natℝ-<-embed 1-lt-15))))
  where
  one-over-one : (natℝ 1 /ℝ natℝ 1) ≡ oneℝ
  one-over-one = trans (cong₂ _/ℝ_ natℝ-one natℝ-one) (div-one-ℝ oneℝ)
  1-lt-15 : 1 <ℕ 15
  1-lt-15 = <-trans (<-suc 1) (<-trans (<-suc 2) (<-trans (<-suc 3) (<-trans (<-suc 4) (<-trans (<-suc 5) (<-trans (<-suc 6) (<-trans (<-suc 7) (<-trans (<-suc 8) (<-trans (<-suc 9) (<-trans (<-suc 10) (<-trans (<-suc 11) (<-trans (<-suc 12) (<-trans (<-suc 13) (<-suc 14)))))))))))))

x-lt-one : x-29-450 <ℝ oneℝ
x-lt-one = trans-<ℝ x-lt-15th one-15th-lt-one

x-≤-0 : zeroℝ ≤ℝ x-29-450
x-≤-0 = <-≤-ℝ x-pos-29-450

-- 装配：exp x < S₃ + T < (A+B+C+D) ≡ A + x²块 < A + 1/450 = 16/15
A : ℝ
A = oneℝ +ℝ x-29-450

assoc-shuffle : (((A +ℝ (x2 /ℝ (natℝ 2))) +ℝ (x2 /ℝ (natℝ 60))) +ℝ (x2 /ℝ (natℝ 2160)))
                ≡ A +ℝ x2-block
assoc-shuffle =
  trans (+-assoc-ℝ (A +ℝ (x2 /ℝ (natℝ 2))) (x2 /ℝ (natℝ 60)) (x2 /ℝ (natℝ 2160)))
  (trans (+-assoc-ℝ A (x2 /ℝ (natℝ 2)) ((x2 /ℝ (natℝ 60)) +ℝ (x2 /ℝ (natℝ 2160))))
         (cong (λ u → A +ℝ u) (sym (+-assoc-ℝ (x2 /ℝ (natℝ 2)) (x2 /ℝ (natℝ 60)) (x2 /ℝ (natℝ 2160))))))

exp-lt-A-E : exp x-29-450 <ℝ (A +ℝ (natℝ 1 /ℝ natℝ 450))
exp-lt-A-E =
  trans-<ℝ (exp-tail-bound-thm 3 x-29-450 x-pos-29-450 x-lt-one)
  (trans-<ℝ (subst (λ z → z <ℝ (((A +ℝ (x2 /ℝ (natℝ 2))) +ℝ (x2 /ℝ (natℝ 60))) +ℝ (x2 /ℝ (natℝ 2160))))
                (sym S3T-eq) (two-mono))
         (subst (λ w → w <ℝ (A +ℝ (natℝ 1 /ℝ natℝ 450))) (sym assoc-shuffle)
                (lt-+-mono-r-ℝ x2-block-lt-450)))
  where
  S3T-eq : (exp-partial-at 3 x-29-450 +ℝ T-term) ≡ (((A +ℝ (x2 /ℝ (natℝ 2))) +ℝ x3-6) +ℝ T-term)
  S3T-eq = cong (λ u → u +ℝ T-term) S3-value
  two-mono : (((A +ℝ (x2 /ℝ (natℝ 2))) +ℝ x3-6) +ℝ T-term)
             <ℝ (((A +ℝ (x2 /ℝ (natℝ 2))) +ℝ (x2 /ℝ (natℝ 60))) +ℝ (x2 /ℝ (natℝ 2160)))
  two-mono = trans-<ℝ Q1 Q2
    where
    -- a < b ⟹ a + c < b + c（本地版，等价于后文顶层 lt-+-mono-l-ℝ）
    loc-mono-l : {a b c : ℝ} → b <ℝ c → (b +ℝ a) <ℝ (c +ℝ a)
    loc-mono-l {a} {b} {c} h =
      subst (λ x → x <ℝ (c +ℝ a)) (sym (+-comm-ℝ b a))
            (subst (λ y → (a +ℝ b) <ℝ y) (sym (+-comm-ℝ c a))
                   (lt-+-mono-r-ℝ {a = a} h))
    U : ℝ
    U = A +ℝ (x2 /ℝ (natℝ 2))
    m1 : (U +ℝ x3-6) <ℝ (U +ℝ (x2 /ℝ (natℝ 60)))
    m1 = lt-+-mono-r-ℝ x3-6-lt-x2-60
    Q1 : ((U +ℝ x3-6) +ℝ T-term) <ℝ ((U +ℝ (x2 /ℝ (natℝ 60))) +ℝ T-term)
    Q1 = loc-mono-l m1
    Q2 : ((U +ℝ (x2 /ℝ (natℝ 60))) +ℝ T-term) <ℝ (((A +ℝ (x2 /ℝ (natℝ 2))) +ℝ (x2 /ℝ (natℝ 60))) +ℝ (x2 /ℝ (natℝ 2160)))
    Q2 = lt-+-mono-r-ℝ T-lt

-- A + 1/450 = 16/15
final-eq : (A +ℝ (natℝ 1 /ℝ natℝ 450)) ≡ (natℝ 16 /ℝ natℝ 15)
final-eq =
  trans (cong (λ u → u +ℝ (natℝ 1 /ℝ natℝ 450)) (cong (λ u → u +ℝ x-29-450) one-450))
        (trans (cong (λ u → u +ℝ (natℝ 1 /ℝ natℝ 450)) x-450-as-29-450)
               (trans (same-den-add (natℝ 479) (natℝ 1) (natℝ 450))
                      (trans (cong₂ _/ℝ_ n480 refl)
                             (/-cross-ℝ (trans (sym (natℝ-* 480 15)) (natℝ-* 16 450))))))
  where
  nat1-over-1 : (natℝ 1 /ℝ natℝ 1) ≡ oneℝ
  nat1-over-1 = trans (cong₂ _/ℝ_ natℝ-one natℝ-one) (div-one-ℝ oneℝ)
  one-450 : oneℝ ≡ (natℝ 450 /ℝ natℝ 450)
  one-450 = trans (sym nat1-over-1) (/-cross-ℝ (trans (sym (natℝ-* 1 450)) (natℝ-* 450 1)))
  x-450-as-29-450 : (natℝ 450 /ℝ natℝ 450) +ℝ x-29-450 ≡ (natℝ 479 /ℝ natℝ 450)
  x-450-as-29-450 = trans (same-den-add (natℝ 450) (natℝ 29) (natℝ 450))
                          (cong₂ _/ℝ_ (sym (natℝ-+ 450 29)) refl)
  n480 : (natℝ 479 +ℝ natℝ 1) ≡ natℝ 480
  n480 = sym (natℝ-+ 479 1)

-- exp(29/450) < 16/15
exp-lt-16-15 : exp x-29-450 <ℝ (natℝ 16 /ℝ natℝ 15)
exp-lt-16-15 = subst (λ y → exp x-29-450 <ℝ y) final-eq exp-lt-A-E

-- ==================================================================
-- ln1615-lb 闭合（2026-08-05，T3 级数机制）：
-- 29/450 < ln(16/15) ⟸ exp(29/450) < exp(ln(16/15)) = 16/15 [exp-log + exp-lt-inj]
-- 不再是 postulate（自 §1 移除）；记账：scoped 数值公理 → 可证明定理
-- ==================================================================
ln1615-lb : (natℝ 29 /ℝ natℝ 450) <ℝ log (natℝ 16 /ℝ natℝ 15)
ln1615-lb =
  exp-lt-inj (subst (λ y → exp x-29-450 <ℝ y) (sym (exp-log (natℝ 16 /ℝ natℝ 15))) exp-lt-16-15)

-- ==================================================================
-- §2c T3 ln2-lt 闭合（2026-08-05，log 级数机制 + 二进制 ℕ 算术）：
-- ln2 < 0.69317。机制：log2-partial（ln 2 的 Σ_{k=1}^n 1/(k·2^k) 部分和）+
-- log2-series-ub（定义性公理：上界 = 部分和 + 几何尾界 1/((n+1)·2^n)）。
-- 大数交叉乘积经 NatArith 的 NATTIMES/NATPLUS 二进制算术 + <-add 差递归
-- （2026-08-05 二进制 ℕ 算术降级路径；此前 v1.35 因 2.8e8 级归一化 OOM）。
-- ==================================================================

-- ln 2 级数部分和：Σ_{k=1}^n 1/(k·2^k)
log2-partial : ℕ → ℝ
log2-partial zero    = zeroℝ
log2-partial (suc n) = log2-partial n +ℝ (oneℝ /ℝ (natℝ (suc n) *ℝ natℝ (2^ (suc n))))

-- log 级数 sup 刻画（登记，2026-08-05 log2-series-ub 降定理前置）：
-- ln 2 = Σ_{k≥1} 1/(k·2^k) 的级数 sup 定义（与 exp-partial-at-≤-ub/exp-least-ub-any
-- 同层，log 级数内容；数学上 ln 2 = -ln(1/2) = Σ_{k≥1} 1/(k·2^k)）。
-- 用途：log2-series-ub 降定理的 sup 论证（部分和 ≤ ln 2 + ln 2 ≤ 最小上界）。
postulate
  log2-partial-≤-ub : (n : ℕ) → log2-partial n ≤ℝ log (natℝ 2)  -- 部分和 ≤ ln 2
  log2-least-ub-any : (b : ℝ) → ((n : ℕ) → log2-partial n ≤ℝ b) → log (natℝ 2) ≤ℝ b  -- ln 2 是最小上界

-- 级数项：1/(k·2^k) 形如 (natℝ 1)/(natℝ (k·2^k))
-- 本地 one-mul-ℝ/zero-add-ℝ（等价于后文顶层同名引理，避免前向引用）
loc-one-mul : (x : ℝ) → oneℝ *ℝ x ≡ x
loc-one-mul x = trans (*-comm-ℝ oneℝ x) (*-ident-ℝ x)

loc-zero-add : (x : ℝ) → zeroℝ +ℝ x ≡ x
loc-zero-add x = trans (+-comm-ℝ zeroℝ x) (+-ident-ℝ x)

log2-term : (k : ℕ) → (oneℝ /ℝ (natℝ k *ℝ natℝ (2^ k))) ≡ (natℝ 1 /ℝ natℝ (k *ℕ 2^ k))
log2-term k =
  /-cross-ℝ (trans (loc-one-mul (natℝ (k *ℕ 2^ k)))
                   (sym (trans (cong₂ _*ℝ_ refl (sym (natℝ-* k (2^ k))))
                               (trans (cong₂ _*ℝ_ natℝ-one refl)
                                      (loc-one-mul (natℝ (k *ℕ 2^ k)))))))

-- 通分到 645120：1/m = s/645120（s·m = 645120）
scale-645120 : (s m : ℕ) → (s *ℕ m) ≡ 645120 → (natℝ 1 /ℝ natℝ m) ≡ (natℝ s /ℝ natℝ 645120)
scale-645120 s m h =
  /-cross-ℝ (trans (trans (cong₂ _*ℝ_ natℝ-one refl) (loc-one-mul (natℝ 645120)))
                   (trans (cong natℝ (sym h))
                          (natℝ-* s m)))

-- 尾项：1/(10·2^9) = 1/5120（并入 645120 分母：126/645120）
tail-5120 : (oneℝ /ℝ (natℝ 10 *ℝ natℝ (2^ 9))) ≡ (natℝ 126 /ℝ natℝ 645120)
tail-5120 = trans tail-1 (scale-645120 126 5120 refl)
  where
  tail-1 : (oneℝ /ℝ (natℝ 10 *ℝ natℝ (2^ 9))) ≡ (natℝ 1 /ℝ natℝ 5120)
  tail-1 = /-cross-ℝ (trans (loc-one-mul (natℝ 5120))
                            (sym (trans (cong₂ _*ℝ_ refl (sym (natℝ-* 10 (2^ 9))))
                                        (trans (cong₂ _*ℝ_ natℝ-one refl)
                                               (loc-one-mul (natℝ 5120))))))

-- log2-partial 9 = Σ 1/(k·2^k)（k=1..9）各通分到 645120
l2p-1 : log2-partial 1 ≡ (natℝ 322560 /ℝ natℝ 645120)
l2p-1 = trans (loc-zero-add (oneℝ /ℝ (natℝ 1 *ℝ natℝ (2^ 1))))
              (trans (log2-term 1) (scale-645120 322560 2 refl))

l2p-2 : log2-partial 2 ≡ (natℝ 403200 /ℝ natℝ 645120)
l2p-2 = trans (cong (λ u → u +ℝ (oneℝ /ℝ (natℝ 2 *ℝ natℝ (2^ 2)))) (l2p-1))
              (trans (cong₂ _+ℝ_ refl (trans (log2-term 2) (scale-645120 80640 8 refl)))
                     (trans (same-den-add (natℝ 322560) (natℝ 80640) (natℝ 645120))
                            (cong₂ _/ℝ_ (sym (natℝ-+ 322560 80640)) refl)))

l2p-3 : log2-partial 3 ≡ (natℝ 430080 /ℝ natℝ 645120)
l2p-3 = trans (cong (λ u → u +ℝ (oneℝ /ℝ (natℝ 3 *ℝ natℝ (2^ 3)))) (l2p-2))
              (trans (cong₂ _+ℝ_ refl (trans (log2-term 3) (scale-645120 26880 24 refl)))
                     (trans (same-den-add (natℝ 403200) (natℝ 26880) (natℝ 645120))
                            (cong₂ _/ℝ_ (sym (natℝ-+ 403200 26880)) refl)))

l2p-4 : log2-partial 4 ≡ (natℝ 440160 /ℝ natℝ 645120)
l2p-4 = trans (cong (λ u → u +ℝ (oneℝ /ℝ (natℝ 4 *ℝ natℝ (2^ 4)))) (l2p-3))
              (trans (cong₂ _+ℝ_ refl (trans (log2-term 4) (scale-645120 10080 64 refl)))
                     (trans (same-den-add (natℝ 430080) (natℝ 10080) (natℝ 645120))
                            (cong₂ _/ℝ_ (sym (natℝ-+ 430080 10080)) refl)))

l2p-5 : log2-partial 5 ≡ (natℝ 444192 /ℝ natℝ 645120)
l2p-5 = trans (cong (λ u → u +ℝ (oneℝ /ℝ (natℝ 5 *ℝ natℝ (2^ 5)))) (l2p-4))
              (trans (cong₂ _+ℝ_ refl (trans (log2-term 5) (scale-645120 4032 160 refl)))
                     (trans (same-den-add (natℝ 440160) (natℝ 4032) (natℝ 645120))
                            (cong₂ _/ℝ_ (sym (natℝ-+ 440160 4032)) refl)))

l2p-6 : log2-partial 6 ≡ (natℝ 445872 /ℝ natℝ 645120)
l2p-6 = trans (cong (λ u → u +ℝ (oneℝ /ℝ (natℝ 6 *ℝ natℝ (2^ 6)))) (l2p-5))
              (trans (cong₂ _+ℝ_ refl (trans (log2-term 6) (scale-645120 1680 384 refl)))
                     (trans (same-den-add (natℝ 444192) (natℝ 1680) (natℝ 645120))
                            (cong₂ _/ℝ_ (sym (natℝ-+ 444192 1680)) refl)))

l2p-7 : log2-partial 7 ≡ (natℝ 446592 /ℝ natℝ 645120)
l2p-7 = trans (cong (λ u → u +ℝ (oneℝ /ℝ (natℝ 7 *ℝ natℝ (2^ 7)))) (l2p-6))
              (trans (cong₂ _+ℝ_ refl (trans (log2-term 7) (scale-645120 720 896 refl)))
                     (trans (same-den-add (natℝ 445872) (natℝ 720) (natℝ 645120))
                            (cong₂ _/ℝ_ (sym (natℝ-+ 445872 720)) refl)))

l2p-8 : log2-partial 8 ≡ (natℝ 446907 /ℝ natℝ 645120)
l2p-8 = trans (cong (λ u → u +ℝ (oneℝ /ℝ (natℝ 8 *ℝ natℝ (2^ 8)))) (l2p-7))
              (trans (cong₂ _+ℝ_ refl (trans (log2-term 8) (scale-645120 315 2048 refl)))
                     (trans (same-den-add (natℝ 446592) (natℝ 315) (natℝ 645120))
                            (cong₂ _/ℝ_ (sym (natℝ-+ 446592 315)) refl)))

l2p-9 : log2-partial 9 ≡ (natℝ 447047 /ℝ natℝ 645120)
l2p-9 = trans (cong (λ u → u +ℝ (oneℝ /ℝ (natℝ 9 *ℝ natℝ (2^ 9)))) (l2p-8))
              (trans (cong₂ _+ℝ_ refl (trans (log2-term 9) (scale-645120 140 4608 refl)))
                     (trans (same-den-add (natℝ 446907) (natℝ 140) (natℝ 645120))
                            (cong₂ _/ℝ_ (sym (natℝ-+ 446907 140)) refl)))

-- ==================================================================
-- §2c' log2-series-ub 降定理（2026-08-05，固定间隙路径）
-- 目标：ln 2 < Σ_{k=1}^n 1/(k·2^k) + 1/((n+1)·2^n)（log2-series-ub）
--   由 postulate 降为可证明定理。机制（与 exp-tail-bound 平行）：
--   部分和 ≤ ln 2（log2-partial-≤-ub）+ ln 2 ≤ 最小上界（log2-least-ub-any）
--   + 更紧尾界 B''n = 第一项 + (1/(n+2))·Σ_{k≥n+2} 1/2^k（固定，不依赖 m）
--   + 固定间隙 B''n < B_n（间隙 = [1/(n+1) - 1/(n+2)]/2^{n+1} > 0）⟹ ln 2 < B_n。
-- ==================================================================

-- **可证**：级数项正——0 < 1/(k·2^k)
log2-term-pos : (n : ℕ) → zeroℝ <ℝ (oneℝ /ℝ (natℝ (suc n) *ℝ natℝ (2^ (suc n))))
log2-term-pos n = /-pos-ℝ zero-lt-one-ℝ
                           (lt-*-pos-ℝ (natℝ-pos-embed z<s) (natℝ-pos-embed (2^-pos (suc n))))

-- **可证**：部分和单步递增（≤ 版）
log2-partial-suc-≤ : (n : ℕ) → log2-partial n ≤ℝ log2-partial (suc n)
log2-partial-suc-≤ n = <-≤-ℝ (add-pos-ℝ {x = log2-partial n}
                                        {y = oneℝ /ℝ (natℝ (suc n) *ℝ natℝ (2^ (suc n)))} (log2-term-pos n))

-- **可证**：部分和递增（≤ 版）——n ≤ k ⟹ log2-partial n ≤ log2-partial k
log2-partial-at-le : (n k : ℕ) → n ≤ℕ k → log2-partial n ≤ℝ log2-partial k
log2-partial-at-le n zero nk with nk
... | z≤n = refl-≤ℝ
log2-partial-at-le n (suc k) nk with ≤-suc-decomp {n} {k} nk
... | inj₁ e = subst (λ z → log2-partial n ≤ℝ log2-partial z) e (refl-≤ℝ)
... | inj₂ h' = ≤-trans-ℝ (log2-partial-at-le n k h') (log2-partial-suc-≤ k)

-- 尾部有限和：T_n(m) = Σ_{j=0}^m 1/((n+1+j)·2^{n+1+j})
log2-tail : ℕ → ℕ → ℝ
log2-tail n zero = oneℝ /ℝ (natℝ (suc (n +ℕr zero)) *ℝ natℝ (2^ (suc (n +ℕr zero))))
log2-tail n (suc m) = log2-tail n m +ℝ (oneℝ /ℝ (natℝ (suc (suc (n +ℕr m))) *ℝ natℝ (2^ (suc (suc (n +ℕr m))))))

-- **可证**：部分和分解——log2-partial (n+1+m) = log2-partial n + T_n(m)
log2-decomp : (n m : ℕ) → log2-partial (suc (n +ℕr m)) ≡ (log2-partial n +ℝ log2-tail n m)
log2-decomp n zero = refl
log2-decomp n (suc m) =
  trans (cong (λ u → u +ℝ (oneℝ /ℝ (natℝ (suc (suc (n +ℕr m))) *ℝ natℝ (2^ (suc (suc (n +ℕr m))))))) (log2-decomp n m))
        (+-assoc-ℝ (log2-partial n) (log2-tail n m)
                   (oneℝ /ℝ (natℝ (suc (suc (n +ℕr m))) *ℝ natℝ (2^ (suc (suc (n +ℕr m)))))))

-- ==================================================================
-- §2c' 基础：1/2 的几何机制（2026-08-05，可证）
-- ==================================================================

-- ℕ 层：2^ (suc j) = 2·2^j（NATTIMES 下显式搬运）
2^suc-expand : (j : ℕ) → 2^ (suc j) ≡ 2 *ℕ (2^ j)
2^suc-expand zero = refl
2^suc-expand (suc j) = refl

-- ℕ 层：2^n·2 = 2^{n+1}
pow2-mul2 : (n : ℕ) → (2^ n) *ℕ 2 ≡ 2^ (suc n)
pow2-mul2 n = trans (*ℕ-comm (2^ n) 2) (2^suc-expand n)

-- **可证**：0 < 1/2
half-one-pos : zeroℝ <ℝ (oneℝ /ℝ natℝ 2)
half-one-pos = /-pos-ℝ zero-lt-one-ℝ (natℝ-pos-embed z<s)

-- **可证**：1 < 2
one-lt-two : oneℝ <ℝ natℝ 2
one-lt-two = subst (λ z → z <ℝ natℝ 2) natℝ-one (natℝ-<-embed (s<s z<s))

-- **可证**：2/2 = 1
two-over-two : (natℝ 2 /ℝ natℝ 2) ≡ oneℝ
two-over-two = trans (/-cross-ℝ {natℝ 2} {oneℝ} {natℝ 2} {oneℝ} cross) (div-one-ℝ oneℝ)
  where
  cross : (natℝ 2 *ℝ oneℝ) ≡ (oneℝ *ℝ natℝ 2)
  cross = trans (*-ident-ℝ (natℝ 2))
                (sym (trans (*-comm-ℝ oneℝ (natℝ 2)) (*-ident-ℝ (natℝ 2))))

-- **可证**：1/2 < 1
half-one-lt-one : (oneℝ /ℝ natℝ 2) <ℝ oneℝ
half-one-lt-one = subst (λ y → (oneℝ /ℝ natℝ 2) <ℝ y) two-over-two
                  (/-lt-same-den-ℝ {oneℝ} {natℝ 2} {natℝ 2} one-lt-two)

-- **可证**：1 + 1 = 2
one-plus-one-two : (oneℝ +ℝ oneℝ) ≡ natℝ 2
one-plus-one-two = trans (cong₂ _+ℝ_ (sym natℝ-one) (sym natℝ-one)) (sym (natℝ-+ 1 1))

-- **可证**：1/2 + 1/2 = 1（(1/2)·2 = 1）
half-add-half-one : ((oneℝ /ℝ natℝ 2) +ℝ (oneℝ /ℝ natℝ 2)) ≡ oneℝ
half-add-half-one = trans step1 step2
  where
  step1 : ((oneℝ /ℝ natℝ 2) +ℝ (oneℝ /ℝ natℝ 2)) ≡ ((oneℝ /ℝ natℝ 2) *ℝ natℝ 2)
  step1 = trans (cong₂ _+ℝ_ (sym (*-ident-ℝ (oneℝ /ℝ natℝ 2))) (sym (*-ident-ℝ (oneℝ /ℝ natℝ 2))))
                (trans (sym (distrib-ℝ (oneℝ /ℝ natℝ 2) oneℝ oneℝ))
                       (cong (λ w → (oneℝ /ℝ natℝ 2) *ℝ w) one-plus-one-two))
  step2 : ((oneℝ /ℝ natℝ 2) *ℝ natℝ 2) ≡ oneℝ
  step2 = trans (*-comm-ℝ (oneℝ /ℝ natℝ 2) (natℝ 2)) (*-/cancel-ℝ (natℝ 2) oneℝ)

-- **可证**：1 − 1/2 = 1/2（1/2 + 1/2 = 1 + 加法群消去）
one-sub-half : (oneℝ -ℝ (oneℝ /ℝ natℝ 2)) ≡ (oneℝ /ℝ natℝ 2)
one-sub-half =
  trans (sub-ℝ-def oneℝ a)
        (trans (cong (λ u → u +ℝ negℝ a) (sym half-add-half-one))
               (trans (+-assoc-ℝ a a (negℝ a))
                      (trans (cong (λ u → a +ℝ u) (+-inv-ℝ a))
                             (+-ident-ℝ a))))
  where
  a : ℝ
  a = oneℝ /ℝ natℝ 2

-- **可证**：1/(1 − 1/2) = 2（交叉相乘 + 消去）
recip-half-two : (oneℝ /ℝ (oneℝ -ℝ (oneℝ /ℝ natℝ 2))) ≡ natℝ 2
recip-half-two =
  trans (cong₂ _/ℝ_ refl one-sub-half)
        (trans (/-cross-ℝ {a = oneℝ} {b = natℝ 2} {c = oneℝ /ℝ natℝ 2} {d = oneℝ}
                          (trans (*-ident-ℝ oneℝ) (sym (*-/cancel-ℝ (natℝ 2) oneℝ))))
               (div-one-ℝ (natℝ 2)))

-- **可证**：geo-x (1/2) j < 2（geo-x-lt 特化：1/(1−1/2) = 2）
geo-half2-lt : (j : ℕ) → geo-x (oneℝ /ℝ natℝ 2) j <ℝ natℝ 2
geo-half2-lt j = subst (λ z → geo-x (oneℝ /ℝ natℝ 2) j <ℝ z) recip-half-two
                 (geo-x-lt (oneℝ /ℝ natℝ 2) half-one-pos half-one-lt-one j)

-- 错位几何和：shift-sum x a j = Σ_{i=0}^j x^{a+i}（归纳定义）
shift-sum : ℝ → ℕ → ℕ → ℝ
shift-sum x a zero = x ^ℕ a
shift-sum x a (suc j) = shift-sum x a j +ℝ (x ^ℕ (a +ℕr (suc j)))

-- **可证**：错位提取公因子——x^a·geo-x x j = shift-sum x a j
geo-shift : (x : ℝ) (a j : ℕ) → ((x ^ℕ a) *ℝ geo-x x j) ≡ shift-sum x a j
geo-shift x a zero = *-ident-ℝ (x ^ℕ a)
geo-shift x a (suc j) =
  trans (distrib-ℝ (x ^ℕ a) (geo-x x j) (x ^ℕ (suc j)))
        (trans (cong₂ _+ℝ_ (geo-shift x a j) refl)
               (cong (λ w → shift-sum x a j +ℝ w) (sym (pow-add x a (suc j)))))

-- **可证**：(1/2)^k = 1/2^k（div-pow + one-pow + nat-pow-embed）
half-pow : (k : ℕ) → ((oneℝ /ℝ natℝ 2) ^ℕ k) ≡ (oneℝ /ℝ natℝ (2^ k))
half-pow k = trans (div-pow oneℝ (natℝ 2) k)
                   (cong₂ _/ℝ_ (one-pow k) (sym (nat-pow-embed k)))

-- **可证**：(1/2)^{a+1}·2 = 1/2^a（分数对消，2·2^a = 2^{a+1}）
half-pow-mul2 : (a : ℕ) → (((oneℝ /ℝ natℝ 2) ^ℕ (suc a)) *ℝ natℝ 2) ≡ (oneℝ /ℝ natℝ (2^ a))
half-pow-mul2 a =
  trans (cong₂ _*ℝ_ (half-pow (suc a)) refl)
        (trans (*-comm-ℝ (oneℝ /ℝ natℝ (2^ (suc a))) (natℝ 2))
               (trans (*-/ℝ (natℝ 2) oneℝ (natℝ (2^ (suc a))))
                      (trans (cong₂ _/ℝ_ (*-ident-ℝ (natℝ 2)) refl)
                             (/-cross-ℝ cross))))
  where
  cross : (natℝ 2 *ℝ natℝ (2^ a)) ≡ (oneℝ *ℝ natℝ (2^ (suc a)))
  cross = trans (sym (natℝ-* 2 (2^ a)))
                (trans (cong natℝ (2^suc-expand a))
                       (sym (loc-one-mul (natℝ (2^ (suc a))))))

-- ==================================================================
-- §2c' 尾部上界（log2-series-ub 降定理，2026-08-05）
-- 目标：Σ_{k≥n+1} 1/(k·2^k) ≤ 1/((n+1)·2^{n+1}) + 1/((n+2)·2^{n+1})（B''n，固定）
-- ==================================================================

-- **可证**：1/(k·2^k) ≤ 1/((n+2)·2^k)（k ≥ n+2；1/k ≤ 1/(n+2)）
tail2-term-le : (n k : ℕ) → (suc (suc n)) ≤ℕ k →
  (oneℝ /ℝ (natℝ k *ℝ natℝ (2^ k))) ≤ℝ (oneℝ /ℝ (natℝ (suc (suc n)) *ℝ natℝ (2^ k)))
tail2-term-le n k h = recip-≤-ℝ den-pos den-le
  where
  den-pos : zeroℝ <ℝ (natℝ (suc (suc n)) *ℝ natℝ (2^ k))
  den-pos = lt-*-pos-ℝ (natℝ-pos-embed z<s) (natℝ-pos-embed (2^-pos k))
  den-le : (natℝ (suc (suc n)) *ℝ natℝ (2^ k)) ≤ℝ (natℝ k *ℝ natℝ (2^ k))
  den-le = *-≤-mono-ℝ {a = natℝ (suc (suc n))} {b = natℝ k} {c = natℝ (2^ k)}
                      (<-≤-ℝ (natℝ-pos-embed (2^-pos k))) (natℝ-≤-embed h)

-- 剩余尾部：Σ_{k=n+2}^{n+2+j} 1/(k·2^k)
log2-rest-sum : ℕ → ℕ → ℝ
log2-rest-sum n zero = oneℝ /ℝ (natℝ (suc (suc (n +ℕr zero))) *ℝ natℝ (2^ (suc (suc (n +ℕr zero)))))
log2-rest-sum n (suc j) = log2-rest-sum n j +ℝ (oneℝ /ℝ (natℝ (suc (suc (n +ℕr (suc j)))) *ℝ natℝ (2^ (suc (suc (n +ℕr (suc j)))))))

-- 剩余几何和：Σ_{k=n+2}^{n+2+j} 1/2^k
rest-geo-sum : ℕ → ℕ → ℝ
rest-geo-sum n zero = oneℝ /ℝ natℝ (2^ (suc (suc (n +ℕr zero))))
rest-geo-sum n (suc j) = rest-geo-sum n j +ℝ (oneℝ /ℝ natℝ (2^ (suc (suc (n +ℕr (suc j))))))

-- **可证**：剩余尾部 ≤ (1/(n+2))·剩余几何和（逐项 tail2-term-le + 加法保序 + 分配律）
tail2-rest-le : (n j : ℕ) → log2-rest-sum n j ≤ℝ ((oneℝ /ℝ natℝ (suc (suc n))) *ℝ rest-geo-sum n j)
tail2-rest-le n zero =
  subst (λ u → u ≤ℝ ((oneℝ /ℝ natℝ (suc (suc n))) *ℝ rest-geo-sum n zero))
        (sym (recip-mul-split (natℝ (suc (suc n))) (natℝ (2^ (suc (suc n))))))
        (refl-≤ℝ)
tail2-rest-le n (suc j) =
  ≤-trans-ℝ stepA (≤-trans-ℝ stepB stepC)
  where
  coef : ℝ
  coef = oneℝ /ℝ natℝ (suc (suc n))
  T : ℝ
  T = oneℝ /ℝ (natℝ (suc (suc (n +ℕr (suc j)))) *ℝ natℝ (2^ (suc (suc (n +ℕr (suc j))))))
  G : ℝ
  G = oneℝ /ℝ natℝ (2^ (suc (suc (n +ℕr (suc j)))))
  -- 逐项：T ≤ coef·G（tail2-term-le + recip-mul-split）
  T-le : T ≤ℝ (coef *ℝ G)
  T-le = subst (λ w → T ≤ℝ w)
               (recip-mul-split (natℝ (suc (suc n))) (natℝ (2^ (suc (suc (n +ℕr (suc j)))))))
               (tail2-term-le n (suc (suc (n +ℕr (suc j)))) (s≤s (s≤s (<-≤ℕ (<-add n j)))))
  -- ① 和 ≤ coef·rest-geo + T
  stepA : (log2-rest-sum n j +ℝ T) ≤ℝ ((coef *ℝ rest-geo-sum n j) +ℝ T)
  stepA = ≤-+-mono-r-ℝ {a = log2-rest-sum n j} {b = coef *ℝ rest-geo-sum n j} {c = T} (tail2-rest-le n j)
  -- ② ≤ coef·rest-geo + coef·G
  stepB : ((coef *ℝ rest-geo-sum n j) +ℝ T) ≤ℝ ((coef *ℝ rest-geo-sum n j) +ℝ (coef *ℝ G))
  stepB = subst (λ v → ((coef *ℝ rest-geo-sum n j) +ℝ T) ≤ℝ v)
                (sym (+-comm-ℝ (coef *ℝ rest-geo-sum n j) (coef *ℝ G)))
          (subst (λ u → u ≤ℝ ((coef *ℝ G) +ℝ (coef *ℝ rest-geo-sum n j)))
                 (+-comm-ℝ T (coef *ℝ rest-geo-sum n j))
                 (≤-+-mono-r-ℝ {a = T} {b = coef *ℝ G} {c = coef *ℝ rest-geo-sum n j} T-le))
  -- ③ = coef·rest-geo (suc j)（分配律反向 + 定义）
  stepC : ((coef *ℝ rest-geo-sum n j) +ℝ (coef *ℝ G)) ≤ℝ (coef *ℝ rest-geo-sum n (suc j))
  stepC = subst (λ u → ((coef *ℝ rest-geo-sum n j) +ℝ (coef *ℝ G)) ≤ℝ u)
                (trans (sym (distrib-ℝ coef (rest-geo-sum n j) G))
                       (cong (λ w → coef *ℝ w) (sym geo-suc-def)))
                (refl-≤ℝ)
    where
    geo-suc-def : rest-geo-sum n (suc j) ≡ (rest-geo-sum n j +ℝ G)
    geo-suc-def = refl

-- **可证**：剩余几何和 = 错位 (1/2)^k 和（归纳 j，half-pow + 索引搬运）
rest-geo-shift : (n j : ℕ) → rest-geo-sum n j ≡ shift-sum (oneℝ /ℝ natℝ 2) (suc (suc n)) j
rest-geo-shift n zero = sym (half-pow (suc (suc n)))
rest-geo-shift n (suc j) =
  trans (cong (λ u → u +ℝ (oneℝ /ℝ natℝ (2^ (suc (suc (n +ℕr (suc j))))))) (rest-geo-shift n j))
        (cong (λ w → shift-sum h (suc (suc n)) j +ℝ w)
              (sym (trans (half-pow ((suc (suc n)) +ℕr (suc j)))
                          (cong (λ v → oneℝ /ℝ natℝ (2^ v)) idx-eq))))
  where
  h : ℝ
  h = oneℝ /ℝ natℝ 2
  idx-eq : ((suc (suc n)) +ℕr (suc j)) ≡ (suc (suc (n +ℕr (suc j))))
  idx-eq = trans (+ℕr-comm-suc (suc n) (suc j)) (cong suc (+ℕr-comm-suc n (suc j)))

-- **可证**：剩余几何和 < 1/2^{n+1}（提取公因子 + geo-x(1/2) < 2）
rest-geo-ub : (n j : ℕ) → rest-geo-sum n j <ℝ (oneℝ /ℝ natℝ (2^ (suc n)))
rest-geo-ub n j = subst (λ w → rest-geo-sum n j <ℝ w) (half-pow-mul2 (suc n))
                  (subst (λ u → u <ℝ ((h ^ℕ (suc (suc n))) *ℝ natℝ 2)) (sym eq) mult-lt)
  where
  h : ℝ
  h = oneℝ /ℝ natℝ 2
  eq : rest-geo-sum n j ≡ ((h ^ℕ (suc (suc n))) *ℝ geo-x h j)
  eq = trans (rest-geo-shift n j) (sym (geo-shift h (suc (suc n)) j))
  hpow-pos : zeroℝ <ℝ (h ^ℕ (suc (suc n)))
  hpow-pos = power-pos-ℕ h half-one-pos (suc n)
  mult-lt : ((h ^ℕ (suc (suc n))) *ℝ geo-x h j) <ℝ ((h ^ℕ (suc (suc n))) *ℝ natℝ 2)
  mult-lt = *-pos-mono-ℝ {a = geo-x h j} {b = natℝ 2} {c = h ^ℕ (suc (suc n))} hpow-pos (geo-half2-lt j)

-- **可证**：剩余尾部 ≤ 1/((n+2)·2^{n+1})（tail2-rest-le + rest-geo-ub + 乘正 + 分数）
tail2-rest-ub : (n j : ℕ) → log2-rest-sum n j ≤ℝ (oneℝ /ℝ (natℝ (suc (suc n)) *ℝ natℝ (2^ (suc n))))
tail2-rest-ub n j = <-≤-ℝ (≤-lt-trans-ℝ (tail2-rest-le n j) (subst (λ z → ((oneℝ /ℝ natℝ (suc (suc n))) *ℝ rest-geo-sum n j) <ℝ z)
                                                                   (sym (recip-mul-split (natℝ (suc (suc n))) (natℝ (2^ (suc n)))))
                                                                   (*-pos-mono-ℝ {a = rest-geo-sum n j}
                                                                                 {b = oneℝ /ℝ natℝ (2^ (suc n))}
                                                                                 {c = oneℝ /ℝ natℝ (suc (suc n))}
                                                                                 coef-pos
                                                                                 (rest-geo-ub n j))))
  where
  coef-pos : zeroℝ <ℝ (oneℝ /ℝ natℝ (suc (suc n)))
  coef-pos = /-pos-ℝ zero-lt-one-ℝ (natℝ-pos-embed z<s)

-- **可证**：尾部分解——log2-tail n (suc m) = 首项 + 剩余（归纳 m）
log2-tail-decomp : (n m : ℕ) → log2-tail n (suc m) ≡ (log2-tail n zero +ℝ log2-rest-sum n m)
log2-tail-decomp n zero = refl
log2-tail-decomp n (suc m) =
  trans (cong (λ u → u +ℝ (oneℝ /ℝ (natℝ (suc (suc (n +ℕr (suc m)))) *ℝ natℝ (2^ (suc (suc (n +ℕr (suc m)))))))) (log2-tail-decomp n m))
        (trans (+-assoc-ℝ (log2-tail n zero) (log2-rest-sum n m)
                          (oneℝ /ℝ (natℝ (suc (suc (n +ℕr (suc m)))) *ℝ natℝ (2^ (suc (suc (n +ℕr (suc m))))))))
               (cong (λ u → (log2-tail n zero) +ℝ u) (sym log2-rest-sum-def)))
  where
  log2-rest-sum-def : log2-rest-sum n (suc m) ≡ (log2-rest-sum n m +ℝ (oneℝ /ℝ (natℝ (suc (suc (n +ℕr (suc m)))) *ℝ natℝ (2^ (suc (suc (n +ℕr (suc m))))))))
  log2-rest-sum-def = refl

-- **可证**：左常数 ≤ 保序——b ≤ c ⟹ a+b ≤ a+c
add-le-l : {a b c : ℝ} → b ≤ℝ c → (a +ℝ b) ≤ℝ (a +ℝ c)
add-le-l {a} {b} {c} h =
  subst (λ v → (a +ℝ b) ≤ℝ v) (sym (+-comm-ℝ a c))
        (subst (λ u → u ≤ℝ (c +ℝ a)) (+-comm-ℝ b a)
               (≤-+-mono-r-ℝ {a = b} {b = c} {c = a} h))

-- 固定上界 B''n = 1/((n+1)·2^{n+1}) + 1/((n+2)·2^{n+1})
B''n : ℕ → ℝ
B''n n = (oneℝ /ℝ (natℝ (suc n) *ℝ natℝ (2^ (suc n)))) +ℝ (oneℝ /ℝ (natℝ (suc (suc n)) *ℝ natℝ (2^ (suc n))))

-- **可证**：尾部 T_n(m) ≤ B''n（m ≥ 1；首项 + 剩余 ≤ 首项 + 1/((n+2)·2^{n+1})）
tail2-le : (n m : ℕ) → log2-tail n (suc m) ≤ℝ (B''n n)
tail2-le n m =
  subst (λ u → u ≤ℝ (B''n n)) (sym (log2-tail-decomp n m))
        (add-le-l {a = log2-tail n zero} {b = log2-rest-sum n m}
                  {c = oneℝ /ℝ (natℝ (suc (suc n)) *ℝ natℝ (2^ (suc n)))}
                  (tail2-rest-ub n m))

-- ==================================================================
-- §2c' 组合收官：log2-series-ub 降定理（2026-08-05）
-- ==================================================================

-- **可证**：a + a = a·2
mul-two-add : (a : ℝ) → (a +ℝ a) ≡ (a *ℝ natℝ 2)
mul-two-add a = trans (cong₂ _+ℝ_ (sym (*-ident-ℝ a)) (sym (*-ident-ℝ a)))
                (trans (sym (distrib-ℝ a oneℝ oneℝ))
                       (cong (λ w → a *ℝ w) one-plus-one-two))

-- **可证**：m ≥ n+1 ⟹ 部分和 m ≤ 部分和 n + B''n（m = n+1 首项吸收；m ≥ n+2 尾部上界）
tail-branch : (n m' : ℕ) → log2-partial (suc (n +ℕr m')) ≤ℝ (log2-partial n +ℝ B''n n)
tail-branch n zero =
  subst (λ u → u ≤ℝ (log2-partial n +ℝ B''n n)) (sym log2-partial-suc-def)
        (add-le-l {a = log2-partial n} {b = t0} {c = t0 +ℝ t1} t0-le)
  where
  t0 : ℝ
  t0 = oneℝ /ℝ (natℝ (suc n) *ℝ natℝ (2^ (suc n)))
  t1 : ℝ
  t1 = oneℝ /ℝ (natℝ (suc (suc n)) *ℝ natℝ (2^ (suc n)))
  log2-partial-suc-def : log2-partial (suc (n +ℕr zero)) ≡ (log2-partial n +ℝ t0)
  log2-partial-suc-def = refl
  t1-pos : zeroℝ <ℝ t1
  t1-pos = /-pos-ℝ zero-lt-one-ℝ
                   (lt-*-pos-ℝ (natℝ-pos-embed z<s) (natℝ-pos-embed (2^-pos (suc n))))
  t0-le : t0 ≤ℝ (t0 +ℝ t1)
  t0-le = <-≤-ℝ (add-pos-ℝ t1-pos)
tail-branch n (suc m') =
  subst (λ u → u ≤ℝ (log2-partial n +ℝ B''n n)) (sym (log2-decomp n (suc m')))
        (add-le-l {a = log2-partial n} {b = log2-tail n (suc m')} {c = B''n n} (tail2-le n m'))

-- **可证**：∀m 部分和 ≤ 部分和 n + B''n（≤-total 三分 + tail-branch）
log2-all-partial-le-B'' : (n m : ℕ) → log2-partial m ≤ℝ (log2-partial n +ℝ B''n n)
log2-all-partial-le-B'' n m with ≤-total m (suc n)
log2-all-partial-le-B'' n m | inj₁ h = ≤-trans-ℝ (log2-partial-at-le m (suc n) h) (tail-branch n zero)
log2-all-partial-le-B'' n m | inj₂ h = subst (λ z → log2-partial z ≤ℝ (log2-partial n +ℝ B''n n)) (tail-repr n m h)
                                     (tail-branch n (m ∸ suc n))

-- **可证**：ln 2 ≤ 部分和 n + B''n（log2-least-ub-any）
log2-le-B'' : (n : ℕ) → log (natℝ 2) ≤ℝ (log2-partial n +ℝ B''n n)
log2-le-B'' n = log2-least-ub-any (log2-partial n +ℝ B''n n) (log2-all-partial-le-B'' n)

-- **可证**：B''n < 尾界 1/((n+1)·2^n)（1/(n+2) < 1/(n+1) 固定间隙）
B''-tail-lt : (n : ℕ) → B''n n <ℝ (oneℝ /ℝ (natℝ (suc n) *ℝ natℝ (2^ n)))
B''-tail-lt n = subst (λ u → (t0 +ℝ t1) <ℝ u) big-eq
                 (lt-+-mono-r-ℝ {a = t0} {b = t1} {c = t0} t1-lt-t0)
  where
  t0 : ℝ
  t0 = oneℝ /ℝ (natℝ (suc n) *ℝ natℝ (2^ (suc n)))
  t1 : ℝ
  t1 = oneℝ /ℝ (natℝ (suc (suc n)) *ℝ natℝ (2^ (suc n)))
  big : ℝ
  big = oneℝ /ℝ (natℝ (suc n) *ℝ natℝ (2^ n))
  den0 : ℝ
  den0 = natℝ (suc n) *ℝ natℝ (2^ (suc n))
  den1 : ℝ
  den1 = natℝ (suc n) *ℝ natℝ (2^ n)
  den0-pos : zeroℝ <ℝ den0
  den0-pos = lt-*-pos-ℝ (natℝ-pos-embed z<s) (natℝ-pos-embed (2^-pos (suc n)))
  den0-lt-den1 : den0 <ℝ (natℝ (suc (suc n)) *ℝ natℝ (2^ (suc n)))
  den0-lt-den1 = subst (λ u → u <ℝ (natℝ (suc (suc n)) *ℝ natℝ (2^ (suc n))))
                       (sym (*-comm-ℝ (natℝ (suc n)) (natℝ (2^ (suc n)))))
                       (subst (λ v → (natℝ (2^ (suc n)) *ℝ natℝ (suc n)) <ℝ v)
                              (sym (*-comm-ℝ (natℝ (suc (suc n))) (natℝ (2^ (suc n)))))
                              (*-pos-mono-ℝ {a = natℝ (suc n)} {b = natℝ (suc (suc n))} {c = natℝ (2^ (suc n))}
                                            (natℝ-pos-embed (2^-pos (suc n))) (natℝ-<-embed (s<s (<-suc n)))))
  -- 1/((n+2)·2^{n+1}) < 1/((n+1)·2^{n+1})
  t1-lt-t0 : t1 <ℝ t0
  t1-lt-t0 = recip-mono-ℝ den0-pos den0-lt-den1
  -- 2·(1/((n+1)·2^{n+1})) = 1/((n+1)·2^n)
  big-eq : (t0 +ℝ t0) ≡ big
  big-eq = trans (mul-two-add t0)
           (trans (*-comm-ℝ t0 (natℝ 2))
           (trans (*-/ℝ (natℝ 2) oneℝ den0)
           (trans (cong₂ _/ℝ_ (*-ident-ℝ (natℝ 2)) refl)
                  (/-cross-ℝ cross))))
    where
      cross : (natℝ 2 *ℝ den1) ≡ (oneℝ *ℝ den0)
      cross = trans (sym (*-assoc-ℝ (natℝ 2) (natℝ (suc n)) (natℝ (2^ n))))
              (trans (cong₂ _*ℝ_ (sym (natℝ-* 2 (suc n))) refl)
                     (trans (sym (natℝ-* (2 *ℕ suc n) (2^ n)))
                            (trans (cong natℝ (trans (cong (λ w → w *ℕ (2^ n)) (*ℕ-comm 2 (suc n)))
                                                   (trans (*ℕ-assoc (suc n) 2 (2^ n))
                                                          (cong (λ w → (suc n) *ℕ w) (sym (2^suc-expand n))))))
                                   (trans (natℝ-* (suc n) (2^ (suc n)))
                                          (sym (loc-one-mul den0))))))

-- **可证**：固定间隙——部分和 n + B''n < 部分和 n + 尾界（lt-+-mono-r-ℝ）
B''-lt-B : (n : ℕ) → (log2-partial n +ℝ B''n n) <ℝ (log2-partial n +ℝ (oneℝ /ℝ (natℝ (suc n) *ℝ natℝ (2^ n))))
B''-lt-B n = lt-+-mono-r-ℝ {a = log2-partial n} {b = B''n n}
                          {c = oneℝ /ℝ (natℝ (suc n) *ℝ natℝ (2^ n))} (B''-tail-lt n)

-- **可证**：log2-series-ub 降定理——ln 2 < Σ_{k=1}^n 1/(k·2^k) + 1/((n+1)·2^n)
--（ln 2 ≤ 部分和 n + B''n（log2-least-ub-any）< 部分和 n + 尾界（固定间隙））
log2-series-ub-thm : (n : ℕ) → log (natℝ 2) <ℝ (log2-partial n +ℝ (oneℝ /ℝ (natℝ (suc n) *ℝ natℝ (2^ n))))
log2-series-ub-thm n = ≤-lt-trans-ℝ (log2-le-B'' n) (B''-lt-B n)

-- ==================================================================
-- §2c'' log 级数下界侧机制（2026-08-05）
-- 目标：部分和严格低于 ln 2（下界侧严格化）——与上界侧 log2-series-ub-thm
--       形成 ln 2 的双侧夹逼；具体下界经部分和计算（l2p-9 = 447047/645120）。
-- 机制（零新增公理；sup 刻画前置登记 §2c）：
--   log2-partial n < log2-partial (suc n) [项正严格递增，add-pos-ℝ]
--   ≤ ln 2 [log2-partial-≤-ub (suc n)] ⟹ 部分和严格低于 ln 2。
-- ==================================================================

-- **可证**：部分和严格递增：log2-partial n < log2-partial (suc n)
log2-partial-suc-< : (n : ℕ) → log2-partial n <ℝ log2-partial (suc n)
log2-partial-suc-< n = add-pos-ℝ (log2-term-pos n)

-- **可证**：log 级数下界侧严格化——部分和严格低于 ln 2
--（log2-partial n < log2-partial (suc n) [严格递增] ≤ ln 2 [sup 刻画]）
log2-series-lb-thm : (n : ℕ) → log2-partial n <ℝ log (natℝ 2)
log2-series-lb-thm n = lt-≤-trans-ℝ (log2-partial-suc-< n) (log2-partial-≤-ub (suc n))

-- ln 2 具体下界：部分和 9 = 447047/645120 < ln 2（log2-series-lb-thm 9）
log2-lb-447047 : (natℝ 447047 /ℝ natℝ 645120) <ℝ log (natℝ 2)
log2-lb-447047 = subst (λ x → x <ℝ log (natℝ 2)) l2p-9 (log2-series-lb-thm 9)

-- log 2 < 447173/645120（部分和 9 = 447047/645120 + 尾界 1/5120 = 126/645120）
log2-ub-447173 : log (natℝ 2) <ℝ (natℝ 447173 /ℝ natℝ 645120)
log2-ub-447173 =
  subst (λ y → log (natℝ 2) <ℝ y) sum-eq (log2-series-ub-thm 9)
  where
  sum-eq : (log2-partial 9 +ℝ (oneℝ /ℝ (natℝ 10 *ℝ natℝ (2^ 9)))) ≡ (natℝ 447173 /ℝ natℝ 645120)
  sum-eq = trans (cong₂ _+ℝ_ l2p-9 tail-5120)
                 (trans (same-den-add (natℝ 447047) (natℝ 126) (natℝ 645120))
                        (cong₂ _/ℝ_ (sym (natℝ-+ 447047 126)) refl))

-- ln 2 双侧夹逼（部分和 9）：447047/645120 < ln 2 < 447173/645120
--（下界：部分和 9 = 447047/645120 [log2-series-lb-thm 9]；
--  上界：部分和 9 + 尾界 1/5120 = 447173/645120 [log2-series-ub-thm 9]）
ln2-squeeze-9 : ((natℝ 447047 /ℝ natℝ 645120) <ℝ log (natℝ 2))
             × (log (natℝ 2) <ℝ (natℝ 447173 /ℝ natℝ 645120))
ln2-squeeze-9 = log2-lb-447047 , log2-ub-447173

-- ==================================================================
-- §2c''' ln 级数高阶精化（2026-08-05）
-- 目标：利用 log2-series-ub-thm / log2-series-lb-thm 对截断序 n 的均匀性，
--       k 阶精化 = 在 n+k 实例化（部分和推进 k 项、尾界收紧 k 阶）：
--         k 阶上界：ln 2 < 部分和 n + Σ_{j=1}^{k} t_{n+j} + 1/((n+k+1)·2^{n+k})
--       一阶（v1.43）：尾界 1/((n+1)·2^n)；**二阶（本节）**：尾界 B''n
--       = t_{n+1} + 1/((n+2)·2^{n+1})——v1.43 的固定界 B''n 由"≤"严格化为
--       "<"（log2-series-ub-thm (suc n) 移位 + 结合律展开），零新增公理。
-- ==================================================================

-- **可证**：二阶下界——部分和推进一项：部分和 n + t_{n+1} < ln 2
--（= log2-series-lb-thm (suc n) 定义性展开，项正严格递增 + sup 刻画）
log2-series-lb2-thm : (n : ℕ) → (log2-partial n +ℝ (oneℝ /ℝ (natℝ (suc n) *ℝ natℝ (2^ (suc n))))) <ℝ log (natℝ 2)
log2-series-lb2-thm n = log2-series-lb-thm (suc n)

-- **可证**：二阶上界——ln 2 < 部分和 n + B''n（B''n = t_{n+1} + 1/((n+2)·2^{n+1})，
-- v1.43 固定界 B''n 严格化；log2-series-ub-thm (suc n) 移位 + 结合律）
log2-series-ub2-thm : (n : ℕ) → log (natℝ 2) <ℝ (log2-partial n +ℝ B''n n)
log2-series-ub2-thm n = subst (λ w → log (natℝ 2) <ℝ w) (+-assoc-ℝ (log2-partial n) t1 t2) (log2-series-ub-thm (suc n))
  where
  t1 : ℝ
  t1 = oneℝ /ℝ (natℝ (suc n) *ℝ natℝ (2^ (suc n)))
  t2 : ℝ
  t2 = oneℝ /ℝ (natℝ (suc (suc n)) *ℝ natℝ (2^ (suc n)))

-- ==================================================================
-- §2c''' 具体高阶夹逼（n=9 二阶上界 / n=10 下界，通分 7096320）
-- ==================================================================

-- 通分到 7096320（= 645120·11 = 2^11·3²·5·7·11，覆盖 k ≤ 11 的 k·2^k 尾项）
scale-7096320 : (s m : ℕ) → (s *ℕ m) ≡ 7096320 → (natℝ 1 /ℝ natℝ m) ≡ (natℝ s /ℝ natℝ 7096320)
scale-7096320 s m h =
  /-cross-ℝ (trans (trans (cong₂ _*ℝ_ natℝ-one refl) (loc-one-mul (natℝ 7096320)))
                   (trans (cong natℝ (sym h)) (natℝ-* s m)))

-- 部分和 9 通分到 7096320：447047/645120 = 4917517/7096320（×11）
l2p-9-7096 : (natℝ 447047 /ℝ natℝ 645120) ≡ (natℝ 4917517 /ℝ natℝ 7096320)
l2p-9-7096 = trans (frac-scaled-ℝ (natℝ 447047) (natℝ 645120) (natℝ 11))
                   (cong₂ _/ℝ_ (sym (natℝ-* 447047 11)) (sym (natℝ-* 645120 11)))

-- 部分和 10 = 部分和 9 + 1/10240 = 4918210/7096320（1/10240 = 693/7096320）
l2p-10-7096 : log2-partial 10 ≡ (natℝ 4918210 /ℝ natℝ 7096320)
l2p-10-7096 = trans (cong (λ u → u +ℝ (oneℝ /ℝ (natℝ 10 *ℝ natℝ (2^ 10)))) (trans l2p-9 l2p-9-7096))
                    (trans (cong₂ _+ℝ_ refl (trans (log2-term 10) (scale-7096320 693 10240 refl)))
                           (trans (same-den-add (natℝ 4917517) (natℝ 693) (natℝ 7096320))
                                  (cong₂ _/ℝ_ (sym (natℝ-+ 4917517 693)) refl)))

-- B''n 9 第二项：1/(11·2^10) = 1/11264 = 630/7096320
l2-b2-11264 : (oneℝ /ℝ (natℝ 11 *ℝ natℝ (2^ 10))) ≡ (natℝ 630 /ℝ natℝ 7096320)
l2-b2-11264 = trans b2-11-1 (scale-7096320 630 11264 refl)
  where
  b2-11-1 : (oneℝ /ℝ (natℝ 11 *ℝ natℝ (2^ 10))) ≡ (natℝ 1 /ℝ natℝ 11264)
  b2-11-1 = /-cross-ℝ (trans (loc-one-mul (natℝ 11264))
                             (sym (trans (cong₂ _*ℝ_ refl (sym (natℝ-* 11 (2^ 10))))
                                         (trans (cong₂ _*ℝ_ natℝ-one refl)
                                                (loc-one-mul (natℝ 11264))))))

-- B''n 9 = 1/(10·2^10) + 1/(11·2^10) = 693/7096320 + 630/7096320 = 1323/7096320
B''n-9-7096 : B''n 9 ≡ (natℝ 1323 /ℝ natℝ 7096320)
B''n-9-7096 = trans (cong₂ _+ℝ_ (trans (log2-term 10) (scale-7096320 693 10240 refl)) l2-b2-11264)
                    (trans (same-den-add (natℝ 693) (natℝ 630) (natℝ 7096320))
                           (cong₂ _/ℝ_ (sym (natℝ-+ 693 630)) refl))

-- 二阶上界具体化：ln 2 < 部分和 9 + B''n 9 = 4918840/7096320（log2-series-ub2-thm 9）
log2-ub2-4918840 : log (natℝ 2) <ℝ (natℝ 4918840 /ℝ natℝ 7096320)
log2-ub2-4918840 = subst (λ y → log (natℝ 2) <ℝ y) sum-eq (log2-series-ub2-thm 9)
  where
  sum-eq : (log2-partial 9 +ℝ B''n 9) ≡ (natℝ 4918840 /ℝ natℝ 7096320)
  sum-eq = trans (cong₂ _+ℝ_ (trans l2p-9 l2p-9-7096) B''n-9-7096)
                 (trans (same-den-add (natℝ 4917517) (natℝ 1323) (natℝ 7096320))
                        (cong₂ _/ℝ_ (sym (natℝ-+ 4917517 1323)) refl))

-- 二阶下界具体化：部分和 10 = 4918210/7096320 < ln 2（log2-series-lb-thm 10）
log2-lb2-4918210 : (natℝ 4918210 /ℝ natℝ 7096320) <ℝ log (natℝ 2)
log2-lb2-4918210 = subst (λ x → x <ℝ log (natℝ 2)) l2p-10-7096 (log2-series-lb-thm 10)

-- 二阶夹逼：4918210/7096320 < ln 2 < 4918840/7096320
--（较 v1.44 一阶夹逼 447047/645120 < ln 2 < 447173/645120 收窄：
--  宽度 630/7096320 ≈ 8.9e-5 < 126/645120 ≈ 2.0e-4）
ln2-squeeze-10 : ((natℝ 4918210 /ℝ natℝ 7096320) <ℝ log (natℝ 2))
              × (log (natℝ 2) <ℝ (natℝ 4918840 /ℝ natℝ 7096320))
ln2-squeeze-10 = log2-lb2-4918210 , log2-ub2-4918840

-- ==================================================================
-- §2c'''' ln(16/15) 级数直接截断机制（2026-08-05，base-16）
-- 目标：ln(16/15) = -ln(15/16) = -ln(1-1/16) = Σ_{k≥1} 1/(k·16^k)
--       由级数直接机制给出双侧夹逼，独立交叉验证 ln1615-lb（exp 侧外第二条路径）。
-- 机制（镜像 §2c' log2-series-ub 的 base-16 版，零新增公理）：
--   前置登记 base-16 级数 sup 刻画（log16-partial-≤-ub + log16-least-ub-any，
--   与 log2 同层的定义性级数刻画）；
--   部分和递增/分解 + 1/16 几何机制（1/(1-1/16) = 16/15）+ 尾部上界
--   B''16n = 1/((n+1)·16^{n+1}) + 1/((n+2)·15·16^{n+1})（固定，不依赖 m；
--   Σ_{k≥n+2} 1/16^k = 1/(15·16^{n+1}) 的 1/15 因子是 base-16 与 base-2 之差）
--   + 固定间隙 B''16n < 2·t_{n+1} ⟹ ln(16/15) < 部分和 n + 2·t_{n+1}。
-- ==================================================================

-- 16 的幂（本地定义，避免 NATTIMES 定义性坑）
pow16 : ℕ → ℕ
pow16 zero = 1
pow16 (suc n) = 16 *ℕ pow16 n

-- ℕ 层：16^{n+1} = 16·16^n（pow16 定义性展开）
pow16-suc-def : (a : ℕ) → pow16 (suc a) ≡ 16 *ℕ pow16 a
pow16-suc-def a = refl

-- 16 的幂恒正：0 < 16^n
pow16-pos : (n : ℕ) → 0 <ℕ pow16 n
pow16-pos zero = z<s
pow16-pos (suc n) = helper n (pow16-pos n)
  where
  helper : (n : ℕ) → 0 <ℕ pow16 n → 0 <ℕ (16 *ℕ pow16 n)
  helper n h with pow16 n
  helper n h | suc k = z<s

-- ℕ 层：natℝ (16^n) = (natℝ 16)^n（归纳 + natℝ-* + ^ℕ 左乘定义性）
nat-pow16-embed : (n : ℕ) → natℝ (pow16 n) ≡ ((natℝ 16) ^ℕ n)
nat-pow16-embed zero = natℝ-one
nat-pow16-embed (suc n) = trans (natℝ-* 16 (pow16 n))
                               (cong (λ x → natℝ 16 *ℝ x) (nat-pow16-embed n))

-- ln(16/15) 级数部分和：Σ_{k=1}^n 1/(k·16^k)
log16-partial : ℕ → ℝ
log16-partial zero    = zeroℝ
log16-partial (suc n) = log16-partial n +ℝ (oneℝ /ℝ (natℝ (suc n) *ℝ natℝ (pow16 (suc n))))

-- base-16 级数 sup 刻画（前置登记，与 log2 同层）：
-- ln(16/15) = Σ_{k≥1} 1/(k·16^k)（-ln(1-1/16) 展开）。
postulate
  log16-partial-≤-ub : (n : ℕ) → log16-partial n ≤ℝ log (natℝ 16 /ℝ natℝ 15)
  log16-least-ub-any : (b : ℝ) → ((n : ℕ) → log16-partial n ≤ℝ b) → log (natℝ 16 /ℝ natℝ 15) ≤ℝ b

-- 级数项：1/(k·16^k) 形如 (natℝ 1)/(natℝ (k·16^k))
log16-term : (k : ℕ) → (oneℝ /ℝ (natℝ k *ℝ natℝ (pow16 k))) ≡ (natℝ 1 /ℝ natℝ (k *ℕ pow16 k))
log16-term k = /-cross-ℝ (trans (loc-one-mul (natℝ (k *ℕ pow16 k)))
                                (sym (trans (cong₂ _*ℝ_ refl (sym (natℝ-* k (pow16 k))))
                                            (trans (cong₂ _*ℝ_ natℝ-one refl)
                                                   (loc-one-mul (natℝ (k *ℕ pow16 k)))))))

-- 项正：0 < 1/(k·16^k)
log16-term-pos : (n : ℕ) → zeroℝ <ℝ (oneℝ /ℝ (natℝ (suc n) *ℝ natℝ (pow16 (suc n))))
log16-term-pos n = /-pos-ℝ zero-lt-one-ℝ
                           (lt-*-pos-ℝ (natℝ-pos-embed z<s) (natℝ-pos-embed (pow16-pos (suc n))))

-- 部分和严格递增：log16-partial n < log16-partial (suc n)
log16-partial-suc-< : (n : ℕ) → log16-partial n <ℝ log16-partial (suc n)
log16-partial-suc-< n = add-pos-ℝ (log16-term-pos n)

-- 部分和递增（≤ 版）
log16-partial-suc-≤ : (n : ℕ) → log16-partial n ≤ℝ log16-partial (suc n)
log16-partial-suc-≤ n = <-≤-ℝ (log16-partial-suc-< n)

-- 部分和递增（≤ 版）——n ≤ k ⟹ log16-partial n ≤ log16-partial k
log16-partial-at-le : (n k : ℕ) → n ≤ℕ k → log16-partial n ≤ℝ log16-partial k
log16-partial-at-le n zero nk with nk
... | z≤n = refl-≤ℝ
log16-partial-at-le n (suc k) nk with ≤-suc-decomp {n} {k} nk
... | inj₁ e = subst (λ z → log16-partial n ≤ℝ log16-partial z) e (refl-≤ℝ)
... | inj₂ h' = ≤-trans-ℝ (log16-partial-at-le n k h') (log16-partial-suc-≤ k)

-- 尾部有限和：T16_n(m) = Σ_{j=0}^m 1/((n+1+j)·16^{n+1+j})
log16-tail : ℕ → ℕ → ℝ
log16-tail n zero = oneℝ /ℝ (natℝ (suc (n +ℕr zero)) *ℝ natℝ (pow16 (suc (n +ℕr zero))))
log16-tail n (suc m) = log16-tail n m +ℝ (oneℝ /ℝ (natℝ (suc (suc (n +ℕr m))) *ℝ natℝ (pow16 (suc (suc (n +ℕr m))))))

-- 部分和分解：log16-partial (n+1+m) = log16-partial n + T16_n(m)
log16-decomp : (n m : ℕ) → log16-partial (suc (n +ℕr m)) ≡ (log16-partial n +ℝ log16-tail n m)
log16-decomp n zero = refl
log16-decomp n (suc m) =
  trans (cong (λ u → u +ℝ (oneℝ /ℝ (natℝ (suc (suc (n +ℕr m))) *ℝ natℝ (pow16 (suc (suc (n +ℕr m))))))) (log16-decomp n m))
        (+-assoc-ℝ (log16-partial n) (log16-tail n m)
                   (oneℝ /ℝ (natℝ (suc (suc (n +ℕr m))) *ℝ natℝ (pow16 (suc (suc (n +ℕr m)))))))

-- ==================================================================
-- §2c'''' 基础：1/16 的几何机制（2026-08-05，可证）
-- ==================================================================

-- **可证**：0 < 1/16
sixteenth-pos : zeroℝ <ℝ (oneℝ /ℝ natℝ 16)
sixteenth-pos = /-pos-ℝ zero-lt-one-ℝ (natℝ-pos-embed z<s)

-- **可证**：1 < 16
one-lt-16 : oneℝ <ℝ natℝ 16
one-lt-16 = subst (λ z → z <ℝ natℝ 16) natℝ-one (natℝ-<-embed (<-add 1 14))

-- **可证**：1 < 15
one-lt-15 : oneℝ <ℝ natℝ 15
one-lt-15 = subst (λ z → z <ℝ natℝ 15) natℝ-one (natℝ-<-embed (<-add 1 13))

-- **可证**：16/16 = 1
sixteen-over-sixteen : (natℝ 16 /ℝ natℝ 16) ≡ oneℝ
sixteen-over-sixteen = trans (/-cross-ℝ {natℝ 16} {oneℝ} {natℝ 16} {oneℝ} cross) (div-one-ℝ oneℝ)
  where
  cross : (natℝ 16 *ℝ oneℝ) ≡ (oneℝ *ℝ natℝ 16)
  cross = trans (*-ident-ℝ (natℝ 16))
                (sym (trans (*-comm-ℝ oneℝ (natℝ 16)) (*-ident-ℝ (natℝ 16))))

-- **可证**：1/16 < 1
sixteenth-lt-one : (oneℝ /ℝ natℝ 16) <ℝ oneℝ
sixteenth-lt-one = subst (λ y → (oneℝ /ℝ natℝ 16) <ℝ y) sixteen-over-sixteen
                  (/-lt-same-den-ℝ {oneℝ} {natℝ 16} {natℝ 16} one-lt-16)

-- **可证**：1/16 + 15/16 = 1（同分母合并）
sixteen-add : (oneℝ /ℝ natℝ 16) +ℝ (natℝ 15 /ℝ natℝ 16) ≡ oneℝ
sixteen-add = trans (cong₂ _+ℝ_ (cong₂ _/ℝ_ (sym natℝ-one) refl) refl)
                    (trans (same-den-add (natℝ 1) (natℝ 15) (natℝ 16))
                           (trans (cong₂ _/ℝ_ (sym (natℝ-+ 1 15)) refl) sixteen-over-sixteen))

-- **可证**：1 − 1/16 = 15/16（1/16 + 15/16 = 1 + 加法群消去）
one-sub-sixteenth : (oneℝ -ℝ (oneℝ /ℝ natℝ 16)) ≡ (natℝ 15 /ℝ natℝ 16)
one-sub-sixteenth =
  trans (sub-ℝ-def oneℝ a)
        (trans (cong (λ u → u +ℝ negℝ a) (sym sixteen-add))
               (trans (+-assoc-ℝ a b (negℝ a))
                      (trans (cong (λ u → a +ℝ u) (+-comm-ℝ b (negℝ a)))
                             (trans (sym (+-assoc-ℝ a (negℝ a) b))
                                    (trans (cong (λ u → u +ℝ b) (+-inv-ℝ a))
                                           (loc-zero-add b))))))
  where
  a : ℝ
  a = oneℝ /ℝ natℝ 16
  b : ℝ
  b = natℝ 15 /ℝ natℝ 16

-- **可证**：1/(1 − 1/16) = 16/15（交叉相乘 + 商消去）
recip-1615 : (oneℝ /ℝ (oneℝ -ℝ (oneℝ /ℝ natℝ 16))) ≡ (natℝ 16 /ℝ natℝ 15)
recip-1615 = trans (cong₂ _/ℝ_ refl one-sub-sixteenth)
                   (/-cross-ℝ (trans (loc-one-mul (natℝ 15)) (sym (*-/cancel-ℝ (natℝ 16) (natℝ 15)))))

-- **可证**：(1/16)^k = 1/16^k（div-pow + one-pow + nat-pow16-embed）
sixteenth-pow : (k : ℕ) → ((oneℝ /ℝ natℝ 16) ^ℕ k) ≡ (oneℝ /ℝ natℝ (pow16 k))
sixteenth-pow k = trans (div-pow oneℝ (natℝ 16) k)
                        (cong₂ _/ℝ_ (one-pow k) (sym (nat-pow16-embed k)))

-- **可证**：(1/16)^{a+1}·16 = 1/16^a（分数对消，16·16^a = 16^{a+1}）
sixteenth-pow-mul16 : (a : ℕ) → (((oneℝ /ℝ natℝ 16) ^ℕ (suc a)) *ℝ natℝ 16) ≡ (oneℝ /ℝ natℝ (pow16 a))
sixteenth-pow-mul16 a =
  trans (cong₂ _*ℝ_ (sixteenth-pow (suc a)) refl)
        (trans (*-comm-ℝ (oneℝ /ℝ natℝ (pow16 (suc a))) (natℝ 16))
               (trans (*-/ℝ (natℝ 16) oneℝ (natℝ (pow16 (suc a))))
                      (trans (cong₂ _/ℝ_ (*-ident-ℝ (natℝ 16)) refl)
                             (/-cross-ℝ cross))))
  where
  cross : (natℝ 16 *ℝ natℝ (pow16 a)) ≡ (oneℝ *ℝ natℝ (pow16 (suc a)))
  cross = trans (sym (natℝ-* 16 (pow16 a)))
                (trans (cong natℝ (pow16-suc-def a))
                       (sym (loc-one-mul (natℝ (pow16 (suc a))))))

-- **可证**：geo-x (1/16) j < 16/15（geo-x-lt 特化：1/(1−1/16) = 16/15）
geo-16th-lt : (j : ℕ) → geo-x (oneℝ /ℝ natℝ 16) j <ℝ (natℝ 16 /ℝ natℝ 15)
geo-16th-lt j = subst (λ z → geo-x (oneℝ /ℝ natℝ 16) j <ℝ z) recip-1615
                 (geo-x-lt (oneℝ /ℝ natℝ 16) sixteenth-pos sixteenth-lt-one j)

-- **可证**：(1/16)^{n+2}·(16/15) = 1/(15·16^{n+1})（乘 16 对消 + 倒数拆分）
sixteenth-geo-tight : (n : ℕ) → (((oneℝ /ℝ natℝ 16) ^ℕ (suc (suc n))) *ℝ (natℝ 16 /ℝ natℝ 15))
                                 ≡ (oneℝ /ℝ (natℝ 15 *ℝ natℝ (pow16 (suc n))))
sixteenth-geo-tight n =
  trans (cong (λ w → A16 *ℝ w) (sym frac-16-15))
        (trans (sym (*-assoc-ℝ A16 (natℝ 16) (oneℝ /ℝ natℝ 15)))
               (trans (cong (λ w → w *ℝ (oneℝ /ℝ natℝ 15)) (sixteenth-pow-mul16 (suc n)))
                      (trans (*-comm-ℝ (oneℝ /ℝ natℝ (pow16 (suc n))) (oneℝ /ℝ natℝ 15))
                             (sym (recip-mul-split (natℝ 15) (natℝ (pow16 (suc n))))))))
  where
  A16 : ℝ
  A16 = (oneℝ /ℝ natℝ 16) ^ℕ (suc (suc n))
  -- 16/15 = 16·(1/15)
  frac-16-15 : (natℝ 16 *ℝ (oneℝ /ℝ natℝ 15)) ≡ (natℝ 16 /ℝ natℝ 15)
  frac-16-15 = trans (*-/ℝ (natℝ 16) oneℝ (natℝ 15))
                     (cong₂ _/ℝ_ (*-ident-ℝ (natℝ 16)) refl)

-- ==================================================================
-- §2c'''' 尾部上界（base-16，镜像 §2c' 尾部块）
-- 目标：Σ_{k≥n+1} 1/(k·16^k) ≤ 1/((n+1)·16^{n+1}) + 1/((n+2)·15·16^{n+1})（B''16n，固定）
-- ==================================================================

-- **可证**：1/(k·16^k) ≤ 1/((n+2)·16^k)（k ≥ n+2）
tail16-term-le : (n k : ℕ) → (suc (suc n)) ≤ℕ k →
  (oneℝ /ℝ (natℝ k *ℝ natℝ (pow16 k))) ≤ℝ (oneℝ /ℝ (natℝ (suc (suc n)) *ℝ natℝ (pow16 k)))
tail16-term-le n k h = recip-≤-ℝ den-pos den-le
  where
  den-pos : zeroℝ <ℝ (natℝ (suc (suc n)) *ℝ natℝ (pow16 k))
  den-pos = lt-*-pos-ℝ (natℝ-pos-embed z<s) (natℝ-pos-embed (pow16-pos k))
  den-le : (natℝ (suc (suc n)) *ℝ natℝ (pow16 k)) ≤ℝ (natℝ k *ℝ natℝ (pow16 k))
  den-le = *-≤-mono-ℝ {a = natℝ (suc (suc n))} {b = natℝ k} {c = natℝ (pow16 k)}
                      (<-≤-ℝ (natℝ-pos-embed (pow16-pos k))) (natℝ-≤-embed h)

-- 剩余尾部：Σ_{k=n+2}^{n+2+j} 1/(k·16^k)
log16-rest-sum : ℕ → ℕ → ℝ
log16-rest-sum n zero = oneℝ /ℝ (natℝ (suc (suc (n +ℕr zero))) *ℝ natℝ (pow16 (suc (suc (n +ℕr zero)))))
log16-rest-sum n (suc j) = log16-rest-sum n j +ℝ (oneℝ /ℝ (natℝ (suc (suc (n +ℕr (suc j)))) *ℝ natℝ (pow16 (suc (suc (n +ℕr (suc j)))))))

-- 剩余几何和：Σ_{k=n+2}^{n+2+j} 1/16^k
rest-geo-sum16 : ℕ → ℕ → ℝ
rest-geo-sum16 n zero = oneℝ /ℝ natℝ (pow16 (suc (suc (n +ℕr zero))))
rest-geo-sum16 n (suc j) = rest-geo-sum16 n j +ℝ (oneℝ /ℝ natℝ (pow16 (suc (suc (n +ℕr (suc j))))))

-- **可证**：剩余尾部 ≤ (1/(n+2))·剩余几何和（逐项 tail16-term-le + 加法保序 + 分配律）
tail16-rest-le : (n j : ℕ) → log16-rest-sum n j ≤ℝ ((oneℝ /ℝ natℝ (suc (suc n))) *ℝ rest-geo-sum16 n j)
tail16-rest-le n zero =
  subst (λ u → u ≤ℝ ((oneℝ /ℝ natℝ (suc (suc n))) *ℝ rest-geo-sum16 n zero))
        (sym (recip-mul-split (natℝ (suc (suc n))) (natℝ (pow16 (suc (suc n))))))
        (refl-≤ℝ)
tail16-rest-le n (suc j) =
  ≤-trans-ℝ stepA (≤-trans-ℝ stepB stepC)
  where
  coef : ℝ
  coef = oneℝ /ℝ natℝ (suc (suc n))
  T : ℝ
  T = oneℝ /ℝ (natℝ (suc (suc (n +ℕr (suc j)))) *ℝ natℝ (pow16 (suc (suc (n +ℕr (suc j))))))
  G : ℝ
  G = oneℝ /ℝ natℝ (pow16 (suc (suc (n +ℕr (suc j)))))
  -- 逐项：T ≤ coef·G（tail16-term-le + recip-mul-split）
  T-le : T ≤ℝ (coef *ℝ G)
  T-le = subst (λ w → T ≤ℝ w)
               (recip-mul-split (natℝ (suc (suc n))) (natℝ (pow16 (suc (suc (n +ℕr (suc j)))))))
               (tail16-term-le n (suc (suc (n +ℕr (suc j)))) (s≤s (s≤s (<-≤ℕ (<-add n j)))))
  -- ① 和 ≤ coef·rest-geo + T
  stepA : (log16-rest-sum n j +ℝ T) ≤ℝ ((coef *ℝ rest-geo-sum16 n j) +ℝ T)
  stepA = ≤-+-mono-r-ℝ {a = log16-rest-sum n j} {b = coef *ℝ rest-geo-sum16 n j} {c = T} (tail16-rest-le n j)
  -- ② ≤ coef·rest-geo + coef·G
  stepB : ((coef *ℝ rest-geo-sum16 n j) +ℝ T) ≤ℝ ((coef *ℝ rest-geo-sum16 n j) +ℝ (coef *ℝ G))
  stepB = subst (λ v → ((coef *ℝ rest-geo-sum16 n j) +ℝ T) ≤ℝ v)
                (sym (+-comm-ℝ (coef *ℝ rest-geo-sum16 n j) (coef *ℝ G)))
          (subst (λ u → u ≤ℝ ((coef *ℝ G) +ℝ (coef *ℝ rest-geo-sum16 n j)))
                 (+-comm-ℝ T (coef *ℝ rest-geo-sum16 n j))
                 (≤-+-mono-r-ℝ {a = T} {b = coef *ℝ G} {c = coef *ℝ rest-geo-sum16 n j} T-le))
  -- ③ = coef·rest-geo (suc j)（分配律反向 + 定义）
  stepC : ((coef *ℝ rest-geo-sum16 n j) +ℝ (coef *ℝ G)) ≤ℝ (coef *ℝ rest-geo-sum16 n (suc j))
  stepC = subst (λ u → ((coef *ℝ rest-geo-sum16 n j) +ℝ (coef *ℝ G)) ≤ℝ u)
                (trans (sym (distrib-ℝ coef (rest-geo-sum16 n j) G))
                       (cong (λ w → coef *ℝ w) (sym geo-suc-def)))
                (refl-≤ℝ)
    where
    geo-suc-def : rest-geo-sum16 n (suc j) ≡ (rest-geo-sum16 n j +ℝ G)
    geo-suc-def = refl

-- **可证**：剩余几何和 = 错位 (1/16)^k 和（归纳 j，sixteenth-pow + 索引搬运）
rest-geo-shift16 : (n j : ℕ) → rest-geo-sum16 n j ≡ shift-sum (oneℝ /ℝ natℝ 16) (suc (suc n)) j
rest-geo-shift16 n zero = sym (sixteenth-pow (suc (suc n)))
rest-geo-shift16 n (suc j) =
  trans (cong (λ u → u +ℝ (oneℝ /ℝ natℝ (pow16 (suc (suc (n +ℕr (suc j))))))) (rest-geo-shift16 n j))
        (cong (λ w → shift-sum h16 (suc (suc n)) j +ℝ w)
              (sym (trans (sixteenth-pow ((suc (suc n)) +ℕr (suc j)))
                          (cong (λ v → oneℝ /ℝ natℝ (pow16 v)) idx-eq))))
  where
  h16 : ℝ
  h16 = oneℝ /ℝ natℝ 16
  idx-eq : ((suc (suc n)) +ℕr (suc j)) ≡ (suc (suc (n +ℕr (suc j))))
  idx-eq = trans (+ℕr-comm-suc (suc n) (suc j)) (cong suc (+ℕr-comm-suc n (suc j)))

-- **可证**：剩余几何和 < 1/(15·16^{n+1})（提取公因子 + geo-x(1/16) < 16/15）
rest-geo-ub16 : (n j : ℕ) → rest-geo-sum16 n j <ℝ (oneℝ /ℝ (natℝ 15 *ℝ natℝ (pow16 (suc n))))
rest-geo-ub16 n j = subst (λ w → rest-geo-sum16 n j <ℝ w) (sixteenth-geo-tight n)
                    (subst (λ u → u <ℝ ((h16 ^ℕ (suc (suc n))) *ℝ (natℝ 16 /ℝ natℝ 15))) (sym eq) mult-lt)
  where
  h16 : ℝ
  h16 = oneℝ /ℝ natℝ 16
  eq : rest-geo-sum16 n j ≡ ((h16 ^ℕ (suc (suc n))) *ℝ geo-x h16 j)
  eq = trans (rest-geo-shift16 n j) (sym (geo-shift h16 (suc (suc n)) j))
  hpow-pos : zeroℝ <ℝ (h16 ^ℕ (suc (suc n)))
  hpow-pos = power-pos-ℕ h16 sixteenth-pos (suc n)
  mult-lt : ((h16 ^ℕ (suc (suc n))) *ℝ geo-x h16 j) <ℝ ((h16 ^ℕ (suc (suc n))) *ℝ (natℝ 16 /ℝ natℝ 15))
  mult-lt = *-pos-mono-ℝ {a = geo-x h16 j} {b = natℝ 16 /ℝ natℝ 15} {c = h16 ^ℕ (suc (suc n))} hpow-pos (geo-16th-lt j)

-- **可证**：剩余尾部 ≤ 1/((n+2)·15·16^{n+1})（tail16-rest-le + rest-geo-ub16 + 乘正 + 分数）
tail16-rest-ub : (n j : ℕ) → log16-rest-sum n j ≤ℝ (oneℝ /ℝ ((natℝ (suc (suc n)) *ℝ natℝ 15) *ℝ natℝ (pow16 (suc n))))
tail16-rest-ub n j = <-≤-ℝ (≤-lt-trans-ℝ (tail16-rest-le n j) (subst (λ z → ((oneℝ /ℝ natℝ (suc (suc n))) *ℝ rest-geo-sum16 n j) <ℝ z)
                                                                   (trans (sym (recip-mul-split (natℝ (suc (suc n))) (natℝ 15 *ℝ natℝ (pow16 (suc n)))))
                                                                          (cong₂ _/ℝ_ refl (sym (*-assoc-ℝ (natℝ (suc (suc n))) (natℝ 15) (natℝ (pow16 (suc n)))))))
                                                                   (*-pos-mono-ℝ {a = rest-geo-sum16 n j}
                                                                                 {b = oneℝ /ℝ (natℝ 15 *ℝ natℝ (pow16 (suc n)))}
                                                                                 {c = oneℝ /ℝ natℝ (suc (suc n))}
                                                                                 coef-pos
                                                                                 (rest-geo-ub16 n j))))
  where
  coef-pos : zeroℝ <ℝ (oneℝ /ℝ natℝ (suc (suc n)))
  coef-pos = /-pos-ℝ zero-lt-one-ℝ (natℝ-pos-embed z<s)

-- **可证**：尾部分解——log16-tail n (suc m) = 首项 + 剩余（归纳 m）
log16-tail-decomp : (n m : ℕ) → log16-tail n (suc m) ≡ (log16-tail n zero +ℝ log16-rest-sum n m)
log16-tail-decomp n zero = refl
log16-tail-decomp n (suc m) =
  trans (cong (λ u → u +ℝ (oneℝ /ℝ (natℝ (suc (suc (n +ℕr (suc m)))) *ℝ natℝ (pow16 (suc (suc (n +ℕr (suc m)))))))) (log16-tail-decomp n m))
        (trans (+-assoc-ℝ (log16-tail n zero) (log16-rest-sum n m)
                          (oneℝ /ℝ (natℝ (suc (suc (n +ℕr (suc m)))) *ℝ natℝ (pow16 (suc (suc (n +ℕr (suc m))))))))
               (cong (λ u → (log16-tail n zero) +ℝ u) (sym log16-rest-sum-def)))
  where
  log16-rest-sum-def : log16-rest-sum n (suc m) ≡ (log16-rest-sum n m +ℝ (oneℝ /ℝ (natℝ (suc (suc (n +ℕr (suc m)))) *ℝ natℝ (pow16 (suc (suc (n +ℕr (suc m))))))))
  log16-rest-sum-def = refl

-- 固定上界 B''16n = 1/((n+1)·16^{n+1}) + 1/((n+2)·15·16^{n+1})
B''16n : ℕ → ℝ
B''16n n = (oneℝ /ℝ (natℝ (suc n) *ℝ natℝ (pow16 (suc n)))) +ℝ (oneℝ /ℝ ((natℝ (suc (suc n)) *ℝ natℝ 15) *ℝ natℝ (pow16 (suc n))))

-- **可证**：尾部 T16_n(m) ≤ B''16n（m ≥ 1；首项 + 剩余）
tail16-le : (n m : ℕ) → log16-tail n (suc m) ≤ℝ (B''16n n)
tail16-le n m =
  subst (λ u → u ≤ℝ (B''16n n)) (sym (log16-tail-decomp n m))
        (add-le-l {a = log16-tail n zero} {b = log16-rest-sum n m}
                  {c = oneℝ /ℝ ((natℝ (suc (suc n)) *ℝ natℝ 15) *ℝ natℝ (pow16 (suc n)))}
                  (tail16-rest-ub n m))

-- ==================================================================
-- §2c'''' 组合收官：log16-series-ub / log16-series-lb（base-16）
-- ==================================================================

-- **可证**：m ≥ n+1 ⟹ 部分和 m ≤ 部分和 n + B''16n（m = n+1 首项吸收；m ≥ n+2 尾部上界）
tail16-branch : (n m' : ℕ) → log16-partial (suc (n +ℕr m')) ≤ℝ (log16-partial n +ℝ B''16n n)
tail16-branch n zero =
  subst (λ u → u ≤ℝ (log16-partial n +ℝ B''16n n)) (sym log16-partial-suc-def)
        (add-le-l {a = log16-partial n} {b = t0} {c = t0 +ℝ t1} t0-le)
  where
  t0 : ℝ
  t0 = oneℝ /ℝ (natℝ (suc n) *ℝ natℝ (pow16 (suc n)))
  t1 : ℝ
  t1 = oneℝ /ℝ ((natℝ (suc (suc n)) *ℝ natℝ 15) *ℝ natℝ (pow16 (suc n)))
  log16-partial-suc-def : log16-partial (suc (n +ℕr zero)) ≡ (log16-partial n +ℝ t0)
  log16-partial-suc-def = refl
  t1-pos : zeroℝ <ℝ t1
  t1-pos = /-pos-ℝ zero-lt-one-ℝ (lt-*-pos-ℝ (lt-*-pos-ℝ (natℝ-pos-embed z<s) (natℝ-pos-embed z<s)) (natℝ-pos-embed (pow16-pos (suc n))))
  t0-le : t0 ≤ℝ (t0 +ℝ t1)
  t0-le = <-≤-ℝ (add-pos-ℝ t1-pos)
tail16-branch n (suc m') =
  subst (λ u → u ≤ℝ (log16-partial n +ℝ B''16n n)) (sym (log16-decomp n (suc m')))
        (add-le-l {a = log16-partial n} {b = log16-tail n (suc m')} {c = B''16n n} (tail16-le n m'))

-- **可证**：∀m 部分和 ≤ 部分和 n + B''16n（≤-total 三分 + tail16-branch）
log16-all-partial-le-B'' : (n m : ℕ) → log16-partial m ≤ℝ (log16-partial n +ℝ B''16n n)
log16-all-partial-le-B'' n m with ≤-total m (suc n)
log16-all-partial-le-B'' n m | inj₁ h = ≤-trans-ℝ (log16-partial-at-le m (suc n) h) (tail16-branch n zero)
log16-all-partial-le-B'' n m | inj₂ h = subst (λ z → log16-partial z ≤ℝ (log16-partial n +ℝ B''16n n)) (tail-repr n m h)
                                     (tail16-branch n (m ∸ suc n))

-- **可证**：ln(16/15) ≤ 部分和 n + B''16n（log16-least-ub-any）
log16-le-B''16 : (n : ℕ) → log (natℝ 16 /ℝ natℝ 15) ≤ℝ (log16-partial n +ℝ B''16n n)
log16-le-B''16 n = log16-least-ub-any (log16-partial n +ℝ B''16n n) (log16-all-partial-le-B'' n)

-- **可证**：B''16n < 2·t_{n+1}（1/((n+2)·15·16^{n+1}) < 1/((n+1)·16^{n+1}) 固定间隙）
B''16-lt-2t : (n : ℕ) → B''16n n <ℝ (natℝ 2 *ℝ (oneℝ /ℝ (natℝ (suc n) *ℝ natℝ (pow16 (suc n)))))
B''16-lt-2t n = subst (λ u → (t0 +ℝ t1) <ℝ u) big-eq
                 (lt-+-mono-r-ℝ {a = t0} {b = t1} {c = t0} t1-lt-t0)
  where
  t0 : ℝ
  t0 = oneℝ /ℝ (natℝ (suc n) *ℝ natℝ (pow16 (suc n)))
  t1 : ℝ
  t1 = oneℝ /ℝ ((natℝ (suc (suc n)) *ℝ natℝ 15) *ℝ natℝ (pow16 (suc n)))
  den0 : ℝ
  den0 = natℝ (suc n) *ℝ natℝ (pow16 (suc n))
  mid : ℝ
  mid = natℝ (suc (suc n)) *ℝ natℝ (pow16 (suc n))
  den1 : ℝ
  den1 = (natℝ (suc (suc n)) *ℝ natℝ 15) *ℝ natℝ (pow16 (suc n))
  den0-pos : zeroℝ <ℝ den0
  den0-pos = lt-*-pos-ℝ (natℝ-pos-embed z<s) (natℝ-pos-embed (pow16-pos (suc n)))
  mid-pos : zeroℝ <ℝ mid
  mid-pos = lt-*-pos-ℝ (natℝ-pos-embed z<s) (natℝ-pos-embed (pow16-pos (suc n)))
  -- (n+1)·16^{n+1} < (n+2)·16^{n+1}
  step1 : den0 <ℝ mid
  step1 = subst (λ u → u <ℝ mid) (sym (*-comm-ℝ (natℝ (suc n)) (natℝ (pow16 (suc n)))))
          (subst (λ v → (natℝ (pow16 (suc n)) *ℝ natℝ (suc n)) <ℝ v)
                 (sym (*-comm-ℝ (natℝ (suc (suc n))) (natℝ (pow16 (suc n)))))
                 (*-pos-mono-ℝ {a = natℝ (suc n)} {b = natℝ (suc (suc n))} {c = natℝ (pow16 (suc n))}
                               (natℝ-pos-embed (pow16-pos (suc n))) (natℝ-<-embed (s<s (<-suc n)))))
  -- mid·15 = (n+2)·15·16^{n+1}
  den1-eq : (mid *ℝ natℝ 15) ≡ den1
  den1-eq = trans (*-assoc-ℝ (natℝ (suc (suc n))) (natℝ (pow16 (suc n))) (natℝ 15))
                  (trans (cong (λ w → natℝ (suc (suc n)) *ℝ w) (*-comm-ℝ (natℝ (pow16 (suc n))) (natℝ 15)))
                         (sym (*-assoc-ℝ (natℝ (suc (suc n))) (natℝ 15) (natℝ (pow16 (suc n))))))
  -- (n+2)·16^{n+1} < (n+2)·15·16^{n+1}
  step2 : mid <ℝ den1
  step2 = subst (λ u → u <ℝ den1) (*-ident-ℝ mid)
          (subst (λ v → (mid *ℝ oneℝ) <ℝ v) den1-eq
                 (*-pos-mono-ℝ {a = oneℝ} {b = natℝ 15} {c = mid} mid-pos one-lt-15))
  -- den0 < den1
  den0-lt-den1 : den0 <ℝ den1
  den0-lt-den1 = trans-<ℝ step1 step2
  -- 1/((n+2)·15·16^{n+1}) < 1/((n+1)·16^{n+1})
  t1-lt-t0 : t1 <ℝ t0
  t1-lt-t0 = recip-mono-ℝ den0-pos den0-lt-den1
  -- t0 + t0 = 2·t0
  big-eq : (t0 +ℝ t0) ≡ (natℝ 2 *ℝ t0)
  big-eq = trans (mul-two-add t0) (*-comm-ℝ t0 (natℝ 2))

-- **可证**：log16-series-ub 机制——ln(16/15) < 部分和 n + 2·t_{n+1}
--（ln(16/15) ≤ 部分和 n + B''16n（log16-least-ub-any）< 部分和 n + 2·t_{n+1}（固定间隙））
log16-series-ub-thm : (n : ℕ) → log (natℝ 16 /ℝ natℝ 15) <ℝ (log16-partial n +ℝ (natℝ 2 *ℝ (oneℝ /ℝ (natℝ (suc n) *ℝ natℝ (pow16 (suc n))))))
log16-series-ub-thm n = ≤-lt-trans-ℝ (log16-le-B''16 n)
                             (lt-+-mono-r-ℝ {a = log16-partial n} {b = B''16n n} (B''16-lt-2t n))

-- **可证**：log 级数下界——部分和严格低于 ln(16/15)
--（log16-partial n < log16-partial (suc n) [严格递增] ≤ ln(16/15) [sup 刻画]）
log16-series-lb-thm : (n : ℕ) → log16-partial n <ℝ log (natℝ 16 /ℝ natℝ 15)
log16-series-lb-thm n = lt-≤-trans-ℝ (log16-partial-suc-< n) (log16-partial-≤-ub (suc n))

-- ==================================================================
-- §2c'''' 具体夹逼（n=2）：33/512 < ln(16/15) < 397/6144
--        + 29/450 < ln(16/15) 独立交叉验证（级数路径，原 ln1615-lb 为 exp 路径）
-- ==================================================================

-- 通分到 512：1/m = s/512（s·m = 512）
scale-512 : (s m : ℕ) → (s *ℕ m) ≡ 512 → (natℝ 1 /ℝ natℝ m) ≡ (natℝ s /ℝ natℝ 512)
scale-512 s m h =
  /-cross-ℝ (trans (trans (cong₂ _*ℝ_ natℝ-one refl) (loc-one-mul (natℝ 512)))
                   (trans (cong natℝ (sym h)) (natℝ-* s m)))

-- log16-partial 1 = 1/16 = 32/512
l16p-1 : log16-partial 1 ≡ (natℝ 32 /ℝ natℝ 512)
l16p-1 = trans (loc-zero-add (oneℝ /ℝ (natℝ 1 *ℝ natℝ (pow16 1))))
              (trans (log16-term 1) (scale-512 32 16 refl))

-- log16-partial 2 = 1/16 + 1/512 = 33/512
l16p-2 : log16-partial 2 ≡ (natℝ 33 /ℝ natℝ 512)
l16p-2 = trans (cong (λ u → u +ℝ (oneℝ /ℝ (natℝ 2 *ℝ natℝ (pow16 2)))) (l16p-1))
              (trans (cong₂ _+ℝ_ refl (trans (log16-term 2) (scale-512 1 512 refl)))
                     (trans (same-den-add (natℝ 32) (natℝ 1) (natℝ 512))
                            (cong₂ _/ℝ_ (sym (natℝ-+ 32 1)) refl)))

-- 下界具体化：部分和 2 = 33/512 < ln(16/15)
log16-lb-33-512 : (natℝ 33 /ℝ natℝ 512) <ℝ log (natℝ 16 /ℝ natℝ 15)
log16-lb-33-512 = subst (λ x → x <ℝ log (natℝ 16 /ℝ natℝ 15)) l16p-2 (log16-series-lb-thm 2)

-- 29/450 < 33/512（交叉：29·512 = 14848 < 33·450 = 14850）
29-450-lt-33-512 : (natℝ 29 /ℝ natℝ 450) <ℝ (natℝ 33 /ℝ natℝ 512)
29-450-lt-33-512 =
  subst (λ y → (natℝ 29 /ℝ natℝ 450) <ℝ y) (sym r33)
  (subst (λ x → x <ℝ ((natℝ 33 *ℝ natℝ 450) /ℝ (natℝ 512 *ℝ natℝ 450))) (sym r29)
  (subst (λ d → ((natℝ 29 *ℝ natℝ 512) /ℝ (natℝ 450 *ℝ natℝ 512)) <ℝ ((natℝ 33 *ℝ natℝ 450) /ℝ d)) denom-comm
  (/-lt-same-den-ℝ {natℝ 29 *ℝ natℝ 512} {natℝ 33 *ℝ natℝ 450} {natℝ 450 *ℝ natℝ 512} cross-lt-29-33)))
  where
  r29 : (natℝ 29 /ℝ natℝ 450) ≡ ((natℝ 29 *ℝ natℝ 512) /ℝ (natℝ 450 *ℝ natℝ 512))
  r29 = frac-scaled-ℝ (natℝ 29) (natℝ 450) (natℝ 512)
  r33 : (natℝ 33 /ℝ natℝ 512) ≡ ((natℝ 33 *ℝ natℝ 450) /ℝ (natℝ 512 *ℝ natℝ 450))
  r33 = frac-scaled-ℝ (natℝ 33) (natℝ 512) (natℝ 450)
  denom-comm : (natℝ 450 *ℝ natℝ 512) ≡ (natℝ 512 *ℝ natℝ 450)
  denom-comm = trans (sym (natℝ-* 450 512)) (natℝ-* 512 450)
  cross-lt-29-33 : (natℝ 29 *ℝ natℝ 512) <ℝ (natℝ 33 *ℝ natℝ 450)
  cross-lt-29-33 = subst (λ z → z <ℝ (natℝ 33 *ℝ natℝ 450)) (natℝ-* 29 512)
                  (subst (λ y → natℝ (29 *ℕ 512) <ℝ y) (natℝ-* 33 450)
                         (natℝ-<-embed prod-lt))
    where
    prod-lt : (29 *ℕ 512) <ℕ (33 *ℕ 450)
    prod-lt = <-add 14848 1

-- 独立交叉验证：29/450 < ln(16/15)（级数路径；原 ln1615-lb 为 exp 路径）
ln1615-lb-direct : (natℝ 29 /ℝ natℝ 450) <ℝ log (natℝ 16 /ℝ natℝ 15)
ln1615-lb-direct = trans-<ℝ (29-450-lt-33-512) log16-lb-33-512

-- 通分到 6144：部分和 2 = 396/6144（33·12 = 396，512·12 = 6144）
l16p-2-6144 : (natℝ 33 /ℝ natℝ 512) ≡ (natℝ 396 /ℝ natℝ 6144)
l16p-2-6144 = trans (frac-scaled-ℝ (natℝ 33) (natℝ 512) (natℝ 12))
                    (cong₂ _/ℝ_ (sym (natℝ-* 33 12)) (sym (natℝ-* 512 12)))

-- 2·t_3 = 2/(3·16^3) = 2/12288 = 1/6144
two-t3 : (natℝ 2 *ℝ (oneℝ /ℝ (natℝ 3 *ℝ natℝ (pow16 3)))) ≡ (natℝ 1 /ℝ natℝ 6144)
two-t3 = trans (cong₂ _*ℝ_ refl (log16-term 3))
               (trans (*-/ℝ (natℝ 2) (natℝ 1) (natℝ 12288))
                      (trans (cong₂ _/ℝ_ (trans (cong (λ w → natℝ 2 *ℝ w) natℝ-one) (*-ident-ℝ (natℝ 2))) refl)
                             (/-cross-ℝ cross)))
  where
  cross : (natℝ 2 *ℝ natℝ 6144) ≡ (natℝ 1 *ℝ natℝ 12288)
  cross = trans (sym (natℝ-* 2 6144))
                (sym (trans (cong₂ _*ℝ_ natℝ-one refl) (loc-one-mul (natℝ 12288))))

-- 上界具体化：ln(16/15) < 部分和 2 + 2·t_3 = 33/512 + 1/6144 = 397/6144
log16-ub-397-6144 : log (natℝ 16 /ℝ natℝ 15) <ℝ (natℝ 397 /ℝ natℝ 6144)
log16-ub-397-6144 = subst (λ y → log (natℝ 16 /ℝ natℝ 15) <ℝ y) sum-eq (log16-series-ub-thm 2)
  where
  sum-eq : (log16-partial 2 +ℝ (natℝ 2 *ℝ (oneℝ /ℝ (natℝ 3 *ℝ natℝ (pow16 3))))) ≡ (natℝ 397 /ℝ natℝ 6144)
  sum-eq = trans (cong₂ _+ℝ_ (trans l16p-2 l16p-2-6144) two-t3)
                 (trans (same-den-add (natℝ 396) (natℝ 1) (natℝ 6144))
                        (cong₂ _/ℝ_ (sym (natℝ-+ 396 1)) refl))

-- 双侧夹逼（n=2）：33/512 < ln(16/15) < 397/6144（宽度 1/6144 ≈ 1.6e-4）
ln16-15-squeeze-2 : ((natℝ 33 /ℝ natℝ 512) <ℝ log (natℝ 16 /ℝ natℝ 15))
                 × (log (natℝ 16 /ℝ natℝ 15) <ℝ (natℝ 397 /ℝ natℝ 6144))
ln16-15-squeeze-2 = log16-lb-33-512 , log16-ub-397-6144

-- ==================================================================
-- §2c''''' ln(16/15) 二阶精化（2026-08-05，base-16 高阶，镜像 v1.45）
-- 目标：二阶上界——ln(16/15) < 部分和 n + t_{n+1} + 2·t_{n+2}（t_k = 1/(k·16^k)），
--       即固定界 B2''16n = t_{n+1} + t_{n+2} + 1/((n+3)·15·16^{n+2}) 严格化。
-- 机制（零新增公理；复用 tail16-rest-ub (suc n) 剩余移位）：
--   剩余移位 log16-rest-shift（log16-rest-sum n (suc m) = t_{n+2} + 剩余 (suc n) m）
--   + 尾部分解 log16-tail2-decomp（T16_n(m≥2) = t_{n+1} + t_{n+2} + 剩余 (suc n)）
--   + ≤-total 在 n+2 三分 + 固定间隙 1/((n+3)·15·16^{n+2}) < t_{n+2}。
-- ==================================================================

-- 二阶固定界 B2''16n = t_{n+1} + t_{n+2} + 1/((n+3)·15·16^{n+2})
B2''16n : ℕ → ℝ
B2''16n n = ((oneℝ /ℝ (natℝ (suc n) *ℝ natℝ (pow16 (suc n)))) +ℝ (oneℝ /ℝ (natℝ (suc (suc n)) *ℝ natℝ (pow16 (suc (suc n)))))) +ℝ (oneℝ /ℝ ((natℝ (suc (suc (suc n))) *ℝ natℝ 15) *ℝ natℝ (pow16 (suc (suc n)))))

-- **可证**：剩余移位——log16-rest-sum n (suc m) = t_{n+2} + 剩余 (suc n) m（归纳 m）
log16-rest-shift : (n m : ℕ) → log16-rest-sum n (suc m) ≡ ((oneℝ /ℝ (natℝ (suc (suc n)) *ℝ natℝ (pow16 (suc (suc n))))) +ℝ log16-rest-sum (suc n) m)
log16-rest-shift n zero = refl
log16-rest-shift n (suc m) =
  trans (cong (λ u → u +ℝ term-idx1) (log16-rest-shift n m))
        (trans (+-assoc-ℝ (t2n n) (log16-rest-sum (suc n) m) term-idx1)
               (cong (λ v → (t2n n) +ℝ ((log16-rest-sum (suc n) m) +ℝ v))
                     (cong (λ w → oneℝ /ℝ (natℝ w *ℝ natℝ (pow16 w))) idx-eq)))
  where
  t2n : ℕ → ℝ
  t2n n = oneℝ /ℝ (natℝ (suc (suc n)) *ℝ natℝ (pow16 (suc (suc n))))
  term-idx1 : ℝ
  term-idx1 = oneℝ /ℝ (natℝ (suc (suc (n +ℕr (suc (suc m))))) *ℝ natℝ (pow16 (suc (suc (n +ℕr (suc (suc m)))))))
  idx-eq : (suc (suc (n +ℕr (suc (suc m))))) ≡ (suc (suc ((suc n) +ℕr (suc m))))
  idx-eq = sym (cong (λ w → suc (suc (suc w))) (+ℕr-comm-suc n m))

-- **可证**：二阶尾部分解——log16-tail n (suc (suc m)) = (t_{n+1} + t_{n+2}) + 剩余 (suc n) m
log16-tail2-decomp : (n m : ℕ) → log16-tail n (suc (suc m)) ≡ ((oneℝ /ℝ (natℝ (suc n) *ℝ natℝ (pow16 (suc n)))) +ℝ (oneℝ /ℝ (natℝ (suc (suc n)) *ℝ natℝ (pow16 (suc (suc n)))))) +ℝ log16-rest-sum (suc n) m
log16-tail2-decomp n m =
  trans (log16-tail-decomp n (suc m))
        (trans (cong (λ u → (t1n n) +ℝ u) (log16-rest-shift n m))
               (sym (+-assoc-ℝ (t1n n) (t2n n) (log16-rest-sum (suc n) m))))
  where
  t1n : ℕ → ℝ
  t1n n = oneℝ /ℝ (natℝ (suc n) *ℝ natℝ (pow16 (suc n)))
  t2n : ℕ → ℝ
  t2n n = oneℝ /ℝ (natℝ (suc (suc n)) *ℝ natℝ (pow16 (suc (suc n))))

-- **可证**：m ≥ n+2 ⟹ 部分和 m ≤ 部分和 n + B2''16n（m = n+2 前两项吸收；m ≥ n+3 二阶尾部上界）
tail16-branch2 : (n m' : ℕ) → log16-partial (suc (suc (n +ℕr m'))) ≤ℝ (log16-partial n +ℝ B2''16n n)
tail16-branch2 n zero =
  subst (λ u → u ≤ℝ (log16-partial n +ℝ B2''16n n)) (sym log16-partial-2-def)
        (add-le-l {a = log16-partial n} {b = (t1 +ℝ t2)} {c = B2''16n n} t12-le)
  where
  t1 : ℝ
  t1 = oneℝ /ℝ (natℝ (suc n) *ℝ natℝ (pow16 (suc n)))
  t2 : ℝ
  t2 = oneℝ /ℝ (natℝ (suc (suc n)) *ℝ natℝ (pow16 (suc (suc n))))
  R : ℝ
  R = oneℝ /ℝ ((natℝ (suc (suc (suc n))) *ℝ natℝ 15) *ℝ natℝ (pow16 (suc (suc n))))
  log16-partial-2-def : log16-partial (suc (suc (n +ℕr zero))) ≡ (log16-partial n +ℝ (t1 +ℝ t2))
  log16-partial-2-def = +-assoc-ℝ (log16-partial n) t1 t2
  R-pos : zeroℝ <ℝ R
  R-pos = /-pos-ℝ zero-lt-one-ℝ (lt-*-pos-ℝ (lt-*-pos-ℝ (natℝ-pos-embed z<s) (natℝ-pos-embed z<s)) (natℝ-pos-embed (pow16-pos (suc (suc n)))))
  t12-le : (t1 +ℝ t2) ≤ℝ B2''16n n
  t12-le = <-≤-ℝ (add-pos-ℝ R-pos)
tail16-branch2 n (suc m') =
  subst (λ u → u ≤ℝ (log16-partial n +ℝ B2''16n n)) (sym (log16-decomp n (suc (suc m'))))
        (subst (λ v → (log16-partial n +ℝ v) ≤ℝ (log16-partial n +ℝ B2''16n n)) (sym (log16-tail2-decomp n m'))
               (add-le-l {a = log16-partial n} {b = (t1 +ℝ t2) +ℝ log16-rest-sum (suc n) m'}
                         {c = B2''16n n}
                         (add-le-l {a = t1 +ℝ t2} {b = log16-rest-sum (suc n) m'} {c = R'}
                                   (tail16-rest-ub (suc n) m'))))
  where
  t1 : ℝ
  t1 = oneℝ /ℝ (natℝ (suc n) *ℝ natℝ (pow16 (suc n)))
  t2 : ℝ
  t2 = oneℝ /ℝ (natℝ (suc (suc n)) *ℝ natℝ (pow16 (suc (suc n))))
  R' : ℝ
  R' = oneℝ /ℝ ((natℝ (suc (suc (suc n))) *ℝ natℝ 15) *ℝ natℝ (pow16 (suc (suc n))))

-- **可证**：∀m 部分和 ≤ 部分和 n + B2''16n（≤-total 在 n+2 三分 + tail16-branch2）
log16-all-partial-le-B2'' : (n m : ℕ) → log16-partial m ≤ℝ (log16-partial n +ℝ B2''16n n)
log16-all-partial-le-B2'' n m with ≤-total m (suc (suc n))
log16-all-partial-le-B2'' n m | inj₁ h = ≤-trans-ℝ (log16-partial-at-le m (suc (suc n)) h) (tail16-branch2 n zero)
log16-all-partial-le-B2'' n m | inj₂ h = subst (λ z → log16-partial z ≤ℝ (log16-partial n +ℝ B2''16n n)) (tail-repr (suc n) m h)
                                     (subst (λ z → log16-partial z ≤ℝ (log16-partial n +ℝ B2''16n n))
                                            (sym (cong suc (+ℕr-comm-suc n (m ∸ suc (suc n)))))
                                            (tail16-branch2 n (m ∸ suc (suc n))))

-- **可证**：ln(16/15) ≤ 部分和 n + B2''16n（log16-least-ub-any）
log16-le-B2'' : (n : ℕ) → log (natℝ 16 /ℝ natℝ 15) ≤ℝ (log16-partial n +ℝ B2''16n n)
log16-le-B2'' n = log16-least-ub-any (log16-partial n +ℝ B2''16n n) (log16-all-partial-le-B2'' n)

-- **可证**：B2''16n < t_{n+1} + 2·t_{n+2}（1/((n+3)·15·16^{n+2}) < t_{n+2} 固定间隙）
B2''-lt-2t2 : (n : ℕ) → B2''16n n <ℝ ((oneℝ /ℝ (natℝ (suc n) *ℝ natℝ (pow16 (suc n)))) +ℝ (natℝ 2 *ℝ (oneℝ /ℝ (natℝ (suc (suc n)) *ℝ natℝ (pow16 (suc (suc n)))))))
B2''-lt-2t2 n = subst (λ u → u <ℝ (t1 +ℝ (natℝ 2 *ℝ t2))) (sym (+-assoc-ℝ t1 t2 R)) step-t1
  where
  t1 : ℝ
  t1 = oneℝ /ℝ (natℝ (suc n) *ℝ natℝ (pow16 (suc n)))
  t2 : ℝ
  t2 = oneℝ /ℝ (natℝ (suc (suc n)) *ℝ natℝ (pow16 (suc (suc n))))
  R : ℝ
  R = oneℝ /ℝ ((natℝ (suc (suc (suc n))) *ℝ natℝ 15) *ℝ natℝ (pow16 (suc (suc n))))
  den2 : ℝ
  den2 = natℝ (suc (suc n)) *ℝ natℝ (pow16 (suc (suc n)))
  mid2 : ℝ
  mid2 = natℝ (suc (suc (suc n))) *ℝ natℝ (pow16 (suc (suc n)))
  denR : ℝ
  denR = (natℝ (suc (suc (suc n))) *ℝ natℝ 15) *ℝ natℝ (pow16 (suc (suc n)))
  den2-pos : zeroℝ <ℝ den2
  den2-pos = lt-*-pos-ℝ (natℝ-pos-embed z<s) (natℝ-pos-embed (pow16-pos (suc (suc n))))
  mid2-pos : zeroℝ <ℝ mid2
  mid2-pos = lt-*-pos-ℝ (natℝ-pos-embed z<s) (natℝ-pos-embed (pow16-pos (suc (suc n))))
  -- (n+2)·16^{n+2} < (n+3)·16^{n+2}
  step1 : den2 <ℝ mid2
  step1 = subst (λ u → u <ℝ mid2) (sym (*-comm-ℝ (natℝ (suc (suc n))) (natℝ (pow16 (suc (suc n))))))
          (subst (λ v → (natℝ (pow16 (suc (suc n))) *ℝ natℝ (suc (suc n))) <ℝ v)
                 (sym (*-comm-ℝ (natℝ (suc (suc (suc n)))) (natℝ (pow16 (suc (suc n))))))
                 (*-pos-mono-ℝ {a = natℝ (suc (suc n))} {b = natℝ (suc (suc (suc n)))} {c = natℝ (pow16 (suc (suc n)))}
                               (natℝ-pos-embed (pow16-pos (suc (suc n)))) (natℝ-<-embed (s<s (s<s (<-suc n))))))
  -- mid2·15 = (n+3)·15·16^{n+2}
  denR-eq : (mid2 *ℝ natℝ 15) ≡ denR
  denR-eq = trans (*-assoc-ℝ (natℝ (suc (suc (suc n)))) (natℝ (pow16 (suc (suc n)))) (natℝ 15))
                  (trans (cong (λ w → natℝ (suc (suc (suc n))) *ℝ w) (*-comm-ℝ (natℝ (pow16 (suc (suc n)))) (natℝ 15)))
                         (sym (*-assoc-ℝ (natℝ (suc (suc (suc n)))) (natℝ 15) (natℝ (pow16 (suc (suc n)))))))
  -- (n+3)·16^{n+2} < (n+3)·15·16^{n+2}
  step2 : mid2 <ℝ denR
  step2 = subst (λ u → u <ℝ denR) (*-ident-ℝ mid2)
          (subst (λ v → (mid2 *ℝ oneℝ) <ℝ v) denR-eq
                 (*-pos-mono-ℝ {a = oneℝ} {b = natℝ 15} {c = mid2} mid2-pos one-lt-15))
  den2-lt-denR : den2 <ℝ denR
  den2-lt-denR = trans-<ℝ step1 step2
  -- R < t2（recip-mono）
  R-lt-t2 : R <ℝ t2
  R-lt-t2 = recip-mono-ℝ den2-pos den2-lt-denR
  -- (t2 + R) < (t2 + t2)
  inner : (t2 +ℝ R) <ℝ (t2 +ℝ t2)
  inner = lt-+-mono-r-ℝ {a = t2} {b = R} {c = t2} R-lt-t2
  -- t2 + t2 = 2·t2
  big-eq2 : (t2 +ℝ t2) ≡ (natℝ 2 *ℝ t2)
  big-eq2 = trans (mul-two-add t2) (*-comm-ℝ t2 (natℝ 2))
  -- t1 + (t2 + R) < t1 + 2·t2
  step-t1 : (t1 +ℝ (t2 +ℝ R)) <ℝ (t1 +ℝ (natℝ 2 *ℝ t2))
  step-t1 = subst (λ v → (t1 +ℝ (t2 +ℝ R)) <ℝ v) (cong (λ u → t1 +ℝ u) big-eq2)
                  (lt-+-mono-r-ℝ {a = t1} {b = t2 +ℝ R} {c = t2 +ℝ t2} inner)

-- **可证**：log16-series-ub2 机制——ln(16/15) < 部分和 n + t_{n+1} + 2·t_{n+2}
--（ln(16/15) ≤ 部分和 n + B2''16n（log16-least-ub-any）< 部分和 n + (t_{n+1} + 2·t_{n+2})（固定间隙））
log16-series-ub2-thm : (n : ℕ) → log (natℝ 16 /ℝ natℝ 15) <ℝ (log16-partial n +ℝ ((oneℝ /ℝ (natℝ (suc n) *ℝ natℝ (pow16 (suc n)))) +ℝ (natℝ 2 *ℝ (oneℝ /ℝ (natℝ (suc (suc n)) *ℝ natℝ (pow16 (suc (suc n))))))))
log16-series-ub2-thm n = ≤-lt-trans-ℝ (log16-le-B2'' n)
                             (lt-+-mono-r-ℝ {a = log16-partial n} {b = B2''16n n} {c = (oneℝ /ℝ (natℝ (suc n) *ℝ natℝ (pow16 (suc n)))) +ℝ (natℝ 2 *ℝ (oneℝ /ℝ (natℝ (suc (suc n)) *ℝ natℝ (pow16 (suc (suc n))))))} (B2''-lt-2t2 n))

-- ==================================================================
-- §2c''''' 具体二阶夹逼（n=2）：33/512 < ln(16/15) < 25379/393216
-- ==================================================================

-- 通分到 393216：1/m = s/393216（s·m = 393216）
scale-393216 : (s m : ℕ) → (s *ℕ m) ≡ 393216 → (natℝ 1 /ℝ natℝ m) ≡ (natℝ s /ℝ natℝ 393216)
scale-393216 s m h =
  /-cross-ℝ (trans (trans (cong₂ _*ℝ_ natℝ-one refl) (loc-one-mul (natℝ 393216)))
                   (trans (cong natℝ (sym h)) (natℝ-* s m)))

-- 2·t_4 = 2/(4·16^4) = 2/262144 = 1/131072
two-t4 : (natℝ 2 *ℝ (oneℝ /ℝ (natℝ 4 *ℝ natℝ (pow16 4)))) ≡ (natℝ 1 /ℝ natℝ 131072)
two-t4 = trans (cong₂ _*ℝ_ refl (log16-term 4))
               (trans (*-/ℝ (natℝ 2) (natℝ 1) (natℝ 262144))
                      (trans (cong₂ _/ℝ_ (trans (cong (λ w → natℝ 2 *ℝ w) natℝ-one) (*-ident-ℝ (natℝ 2))) refl)
                             (/-cross-ℝ cross)))
  where
  cross : (natℝ 2 *ℝ natℝ 131072) ≡ (natℝ 1 *ℝ natℝ 262144)
  cross = trans (sym (natℝ-* 2 131072))
                (sym (trans (cong₂ _*ℝ_ natℝ-one refl) (loc-one-mul (natℝ 262144))))

-- 部分和 2 通分到 393216：33/512 = 25344/393216（33·768 = 25344，512·768 = 393216）
l16p-2-393216 : (natℝ 33 /ℝ natℝ 512) ≡ (natℝ 25344 /ℝ natℝ 393216)
l16p-2-393216 = trans (frac-scaled-ℝ (natℝ 33) (natℝ 512) (natℝ 768))
                      (cong₂ _/ℝ_ (sym (natℝ-* 33 768)) (sym (natℝ-* 512 768)))

-- 二阶上界具体化：ln(16/15) < 部分和 2 + (t_3 + 2·t_4) = 25344/393216 + 35/393216 = 25379/393216
log16-ub2-25379 : log (natℝ 16 /ℝ natℝ 15) <ℝ (natℝ 25379 /ℝ natℝ 393216)
log16-ub2-25379 = subst (λ y → log (natℝ 16 /ℝ natℝ 15) <ℝ y) sum-eq (log16-series-ub2-thm 2)
  where
  sum-eq : (log16-partial 2 +ℝ ((oneℝ /ℝ (natℝ 3 *ℝ natℝ (pow16 3))) +ℝ (natℝ 2 *ℝ (oneℝ /ℝ (natℝ 4 *ℝ natℝ (pow16 4)))))) ≡ (natℝ 25379 /ℝ natℝ 393216)
  sum-eq = trans (cong₂ _+ℝ_ (trans l16p-2 l16p-2-393216) inner)
                 (trans (same-den-add (natℝ 25344) (natℝ 35) (natℝ 393216))
                        (cong₂ _/ℝ_ (sym (natℝ-+ 25344 35)) refl))
    where
    inner : ((oneℝ /ℝ (natℝ 3 *ℝ natℝ (pow16 3))) +ℝ (natℝ 2 *ℝ (oneℝ /ℝ (natℝ 4 *ℝ natℝ (pow16 4))))) ≡ (natℝ 35 /ℝ natℝ 393216)
    inner = trans (cong₂ _+ℝ_ (trans (log16-term 3) (scale-393216 32 12288 refl)) (trans two-t4 (scale-393216 3 131072 refl)))
                  (trans (same-den-add (natℝ 32) (natℝ 3) (natℝ 393216))
                         (cong₂ _/ℝ_ (sym (natℝ-+ 32 3)) refl))

-- 二阶夹逼：33/512 < ln(16/15) < 25379/393216（宽度 35/393216 ≈ 8.9e-5，较 v1.46 的 1/6144 ≈ 1.6e-4 收窄）
ln16-15-squeeze-2b : ((natℝ 33 /ℝ natℝ 512) <ℝ log (natℝ 16 /ℝ natℝ 15))
                  × (log (natℝ 16 /ℝ natℝ 15) <ℝ (natℝ 25379 /ℝ natℝ 393216))
ln16-15-squeeze-2b = log16-lb-33-512 , log16-ub2-25379

-- 交叉乘积比较（二进制算术 + <-add 差递归）：279483125 < 279486144
cross-lt-l2 : (natℝ 447173 *ℝ natℝ 625) <ℝ (natℝ 69317 *ℝ natℝ 4032)
cross-lt-l2 = subst (λ z → z <ℝ (natℝ 69317 *ℝ natℝ 4032)) (natℝ-* 447173 625)
              (subst (λ y → natℝ (447173 *ℕ 625) <ℝ y) (natℝ-* 69317 4032)
                     (natℝ-<-embed prod-lt))
  where
  -- (447173·625 = 279483125) < (69317·4032 = 279486144)，差 3019
  prod-lt : (447173 *ℕ 625) <ℕ (69317 *ℕ 4032)
  prod-lt = <-add 279483125 3018

-- 447173/645120 < 69317/100000（通分到 403200000 后比分子）
l2-lt-69317 : (natℝ 447173 /ℝ natℝ 645120) <ℝ (natℝ 69317 /ℝ natℝ 100000)
l2-lt-69317 =
  subst (λ y → (natℝ 447173 /ℝ natℝ 645120) <ℝ y) (sym r15)
  (subst (λ x → x <ℝ ((natℝ 69317 *ℝ natℝ 4032) /ℝ (natℝ 100000 *ℝ natℝ 4032))) (sym r1117)
  (subst (λ d → ((natℝ 447173 *ℝ natℝ 625) /ℝ (natℝ 645120 *ℝ natℝ 625)) <ℝ ((natℝ 69317 *ℝ natℝ 4032) /ℝ d)) denom-comm
  (/-lt-same-den-ℝ {natℝ 447173 *ℝ natℝ 625} {natℝ 69317 *ℝ natℝ 4032} {natℝ 645120 *ℝ natℝ 625} cross-lt-l2)))
  where
  r1117 : (natℝ 447173 /ℝ natℝ 645120) ≡ ((natℝ 447173 *ℝ natℝ 625) /ℝ (natℝ 645120 *ℝ natℝ 625))
  r1117 = frac-scaled-ℝ (natℝ 447173) (natℝ 645120) (natℝ 625)
  r15 : (natℝ 69317 /ℝ natℝ 100000) ≡ ((natℝ 69317 *ℝ natℝ 4032) /ℝ (natℝ 100000 *ℝ natℝ 4032))
  r15 = frac-scaled-ℝ (natℝ 69317) (natℝ 100000) (natℝ 4032)
  denom-comm : (natℝ 645120 *ℝ natℝ 625) ≡ (natℝ 100000 *ℝ natℝ 4032)
  denom-comm = trans (sym (natℝ-* 645120 625)) (natℝ-* 100000 4032)

-- ln2-lt 闭合（2026-08-05）：不再是 postulate（自 §1 移除）
ln2-lt : log (natℝ 2) <ℝ (natℝ 69317 /ℝ natℝ 100000)
ln2-lt = trans-<ℝ log2-ub-447173 l2-lt-69317

-- ==================================================================
-- §2d T3 ln15-arith-ax 闭合（2026-08-05，二进制 ℕ 算术 + 同分母比较）：
-- 4·(69317/100000) + (-29/450) < 65/24。
-- 机制：A = 277268/100000（*-/ℝ 并入分子，4·69317 二进制算术）+
--       neg-frac-ℝ 取负入分子 + /-add-ℝ 合并为 121870600/45000000；
--       65/24 通分 ×1875000 到 45000000 = 121875000/45000000；
--       同分母直接比分子（差 4400，<-add 差递归）。
--       最大扩展因子 1875000、最大交叉乘积 ~1.25e8（二进制算术秒级；
--       对比 v1.35 的 ~1e9 级大数乘法/105600 层 <-ℕ 链 OOM）。
-- ==================================================================

-- 4·(69317/100000) = 277268/100000（*-/ℝ 并入分子；4·69317 二进制算术定义性）
four-term-2d : (natℝ 4 *ℝ (natℝ 69317 /ℝ natℝ 100000)) ≡ (natℝ 277268 /ℝ natℝ 100000)
four-term-2d = trans (*-/ℝ (natℝ 4) (natℝ 69317) (natℝ 100000))
                     (cong₂ _/ℝ_ (sym (natℝ-* 4 69317)) refl)

-- 本地 (-x)·y = -(x·y)（§2d 内建；规避后文 neg-mul-ℝ/neg-unique-ℝ 前向引用）
loc-neg-mul-2d : (x y : ℝ) → (negℝ x) *ℝ y ≡ negℝ (x *ℝ y)
loc-neg-mul-2d x y =
  loc-neg-unique-2d {a = x *ℝ y} {b = (negℝ x) *ℝ y}
    (trans (sym expand)
           (trans (cong (λ u → u *ℝ y) (+-inv-ℝ x)) (*-zero-l-2d y)))
  where
  -- 加性逆唯一（仅用群公理）
  loc-neg-unique-2d : {a b : ℝ} → a +ℝ b ≡ zeroℝ → b ≡ negℝ a
  loc-neg-unique-2d {a} {b} h =
    trans (sym (trans (sym (+-comm-ℝ b zeroℝ)) (+-ident-ℝ b)))
          (trans (cong (λ x → x +ℝ b) (sym (+-inv-ℝ a)))
                 (trans (cong (λ x → x +ℝ b) (+-comm-ℝ a (negℝ a)))
                        (trans (+-assoc-ℝ (negℝ a) a b)
                               (trans (cong (λ x → negℝ a +ℝ x) h)
                                      (+-ident-ℝ (negℝ a))))))
  -- 0·y = 0（仅用域公理）
  *-zero-l-2d : (y : ℝ) → zeroℝ *ℝ y ≡ zeroℝ
  *-zero-l-2d y = trans (*-comm-ℝ zeroℝ y) (*-zero-ℝ y)
  -- (x + (-x))·y = x·y + (-x)·y
  expand : (x +ℝ negℝ x) *ℝ y ≡ (x *ℝ y) +ℝ ((negℝ x) *ℝ y)
  expand =
    trans (*-comm-ℝ (x +ℝ negℝ x) y)
          (trans (distrib-ℝ y x (negℝ x))
                 (cong₂ _+ℝ_ (*-comm-ℝ y x) (*-comm-ℝ y (negℝ x))))

-- a + (-b) = c（前提 a ≡ c + b，ℕ 层二进制算术下 h 常为 refl）
add-neg-eq-2d : {a b c : ℕ} → a ≡ (c +ℕ b) → (natℝ a +ℝ negℝ (natℝ b)) ≡ natℝ c
add-neg-eq-2d {a} {b} {c} h =
  trans (cong (λ x → x +ℝ negℝ (natℝ b)) na-eq)
        (trans (+-assoc-ℝ (natℝ c) (natℝ b) (negℝ (natℝ b)))
               (trans (cong (λ x → natℝ c +ℝ x) (+-inv-ℝ (natℝ b)))
                      (+-ident-ℝ (natℝ c))))
  where
  na-eq : natℝ a ≡ (natℝ c +ℝ natℝ b)
  na-eq = trans (cong natℝ h) (natℝ-+ c b)

-- 合并：277268/100000 + (-29/450) = 121870600/45000000
sum-2d : ((natℝ 277268 /ℝ natℝ 100000) +ℝ negℝ (natℝ 29 /ℝ natℝ 450)) ≡ (natℝ 121870600 /ℝ natℝ 45000000)
sum-2d = trans (cong₂ _+ℝ_ refl (neg-frac-ℝ (natℝ 29) (natℝ 450)))
          (trans (/-add-ℝ (natℝ 277268) (negℝ (natℝ 29)) (natℝ 100000) (natℝ 450))
                 (cong₂ _/ℝ_ sum-eq den-eq))
  where
  -- 277268·450 = 124770600
  m-124770600 : (natℝ 277268 *ℝ natℝ 450) ≡ natℝ 124770600
  m-124770600 = sym (natℝ-* 277268 450)
  -- (-29)·100000 = -2900000
  m-2900000 : (negℝ (natℝ 29) *ℝ natℝ 100000) ≡ negℝ (natℝ 2900000)
  m-2900000 = trans (loc-neg-mul-2d (natℝ 29) (natℝ 100000))
                    (cong negℝ (sym (natℝ-* 29 100000)))
  -- 124770600 + (-2900000) = 121870600
  add-neg : (natℝ 124770600 +ℝ negℝ (natℝ 2900000)) ≡ natℝ 121870600
  add-neg = add-neg-eq-2d refl
  -- (124770600 + (-2900000)) / 45000000
  sum-eq : ((natℝ 277268 *ℝ natℝ 450) +ℝ (negℝ (natℝ 29) *ℝ natℝ 100000)) ≡ natℝ 121870600
  sum-eq = trans (cong₂ _+ℝ_ m-124770600 m-2900000) add-neg
  -- 100000·450 = 45000000
  den-eq : (natℝ 100000 *ℝ natℝ 450) ≡ natℝ 45000000
  den-eq = sym (natℝ-* 100000 450)

-- 65/24 = 121875000/45000000（通分 ×1875000）
right-2d : (natℝ 65 /ℝ natℝ 24) ≡ (natℝ 121875000 /ℝ natℝ 45000000)
right-2d = trans (frac-scaled-ℝ (natℝ 65) (natℝ 24) (natℝ 1875000))
                 (cong₂ _/ℝ_ (sym (natℝ-* 65 1875000)) (sym (natℝ-* 24 1875000)))

-- 同分母比分子：121870600 < 121875000（差 4400）
num-lt-2d : (natℝ 121870600 /ℝ natℝ 45000000) <ℝ (natℝ 121875000 /ℝ natℝ 45000000)
num-lt-2d = /-lt-same-den-ℝ (natℝ-<-embed num-lt-ℕ)
  where
  num-lt-ℕ : 121870600 <ℕ 121875000
  num-lt-ℕ = <-add 121870600 4399

-- ln15-arith-ax 闭合（2026-08-05）：不再是 postulate（自 §1 移除）
ln15-arith-ax : ((natℝ 4 *ℝ (natℝ 69317 /ℝ natℝ 100000)) +ℝ negℝ (natℝ 29 /ℝ natℝ 450)) <ℝ (natℝ 65 /ℝ natℝ 24)
ln15-arith-ax =
  subst (λ y → L <ℝ y) (sym right-2d)
        (subst (λ x → x <ℝ (natℝ 121875000 /ℝ natℝ 45000000)) (sym sum-l) num-lt-2d)
  where
  L = ((natℝ 4 *ℝ (natℝ 69317 /ℝ natℝ 100000)) +ℝ negℝ (natℝ 29 /ℝ natℝ 450))
  sum-l : L ≡ (natℝ 121870600 /ℝ natℝ 45000000)
  sum-l = trans (cong₂ _+ℝ_ four-term-2d refl) sum-2d


-- exp 单射（**闭合 2026-08-01**：exp-mono 严格单调 + trichotomy-ℝ 三分律 +
-- irreflexive-ℝ 反自反 ⟹ 单射；零新增公理，不再是 postulate。
-- 记账：从账目开放项转为可证明定理）
exp-inj : {x y : ℝ} → exp x ≡ exp y → x ≡ y
exp-inj {x} {y} h with trichotomy-ℝ x y
exp-inj {x} {y} h | inj₁ x<y =
  ⊥-elim (irreflexive-ℝ (subst (λ z → z <ℝ exp y) h (exp-mono x<y)))
exp-inj {x} {y} h | inj₂ (inj₁ x=y) = x=y
exp-inj {x} {y} h | inj₂ (inj₂ y<x) =
  ⊥-elim (irreflexive-ℝ (subst (λ z → z <ℝ exp x) (sym h) (exp-mono y<x)))

-- 加性逆唯一：a + b = 0 ⟹ b = -a（由加法群公理 +-assoc/comm/ident/inv 推出）
neg-unique-ℝ : {a b : ℝ} → a +ℝ b ≡ zeroℝ → b ≡ negℝ a
neg-unique-ℝ {a} {b} h =
  trans (sym (trans (sym (+-comm-ℝ b zeroℝ)) (+-ident-ℝ b)))
        (trans (cong (λ x → x +ℝ b) (sym (+-inv-ℝ a)))
               (trans (cong (λ x → x +ℝ b) (+-comm-ℝ a (negℝ a)))
                      (trans (+-assoc-ℝ (negℝ a) a b)
                             (trans (cong (λ x → negℝ a +ℝ x) h)
                                    (+-ident-ℝ (negℝ a))))))

-- 加法右单调：a < b ⟹ a + c < b + c（由 lt-+-mono-r-ℝ + +-comm-ℝ 推出）
lt-+-mono-l-ℝ : {a b c : ℝ} → a <ℝ b → (a +ℝ c) <ℝ (b +ℝ c)
lt-+-mono-l-ℝ {a} {b} {c} h =
  subst (λ x → x <ℝ (b +ℝ c)) (sym (+-comm-ℝ a c))
        (subst (λ y → (c +ℝ a) <ℝ y) (sym (+-comm-ℝ b c))
               (lt-+-mono-r-ℝ {a = c} h))

-- 取负代数（T3 阶段 4，可证）
-- -0 = 0（0 是 0 的唯一加性逆）
neg-zero : negℝ zeroℝ ≡ zeroℝ
neg-zero = sym (neg-unique-ℝ {a = zeroℝ} {b = zeroℝ} (+-ident-ℝ zeroℝ))

-- -(-x) = x
neg-neg : (x : ℝ) → negℝ (negℝ x) ≡ x
neg-neg x =
  sym (neg-unique-ℝ {a = negℝ x} {b = x}
         (trans (+-comm-ℝ (negℝ x) x) (+-inv-ℝ x)))

-- -1 < 0（经 neg-one-ℝ-def + 取负保序反转）
neg-one-lt-zero : neg-oneℝ <ℝ zeroℝ
neg-one-lt-zero =
  subst (λ x → x <ℝ zeroℝ) (sym neg-one-ℝ-def)
    (subst (λ y → (negℝ oneℝ) <ℝ y) (neg-zero)
           (neg-<-ℝ zero-lt-one-ℝ))

-- 1·x = x
one-mul-ℝ : (x : ℝ) → oneℝ *ℝ x ≡ x
one-mul-ℝ x = trans (*-comm-ℝ oneℝ x) (*-ident-ℝ x)

-- 0·x = 0（零吸收左侧）
*-zero-l-ℝ : (x : ℝ) → zeroℝ *ℝ x ≡ zeroℝ
*-zero-l-ℝ x = trans (*-comm-ℝ zeroℝ x) (*-zero-ℝ x)

-- 0 + x = x
zero-add-ℝ : (x : ℝ) → zeroℝ +ℝ x ≡ x
zero-add-ℝ x = trans (+-comm-ℝ zeroℝ x) (+-ident-ℝ x)

-- (-1)·x = -x（经分配律 + 加性逆唯一）
neg-one-mul : (x : ℝ) → (negℝ oneℝ) *ℝ x ≡ negℝ x
neg-one-mul x =
  neg-unique-ℝ {a = x} {b = (negℝ oneℝ) *ℝ x}
    (trans (sym expand) zero-absorb)
  where
  -- x + (-1)·x = (1 + (-1))·x
  expand : ((oneℝ +ℝ negℝ oneℝ) *ℝ x) ≡ (x +ℝ ((negℝ oneℝ) *ℝ x))
  expand =
    trans (*-comm-ℝ (oneℝ +ℝ negℝ oneℝ) x)
          (trans (distrib-ℝ x oneℝ (negℝ oneℝ))
                 (cong₂ _+ℝ_ (*-ident-ℝ x) (*-comm-ℝ x (negℝ oneℝ))))
  -- (1 + (-1))·x = 0·x = 0
  zero-absorb : (oneℝ +ℝ negℝ oneℝ) *ℝ x ≡ zeroℝ
  zero-absorb = trans (cong (λ y → y *ℝ x) (+-inv-ℝ oneℝ)) (*-zero-l-ℝ x)

-- exp(-x) = 1/exp x（经 exp-add + 加性逆）
exp-recip : (x : ℝ) → exp (negℝ x) ≡ oneℝ /ℝ exp x
exp-recip x =
  trans (sym (div-one-ℝ (exp (negℝ x))))
        (sym (/-cross-ℝ (trans (*-ident-ℝ oneℝ) (sym exp-negx-expx))))
  where
  exp-negx-expx : (exp (negℝ x) *ℝ exp x) ≡ oneℝ
  exp-negx-expx =
    trans (sym (exp-add (negℝ x) x))
          (trans (cong exp (trans (+-comm-ℝ (negℝ x) x) (+-inv-ℝ x)))
                 (exp-zero))

-- a·b = 1 ⟹ b = 1/a（经 (1/a)·a = 1 + 结合律）
*-recip-impl : {a b : ℝ} → (a *ℝ b) ≡ oneℝ → b ≡ oneℝ /ℝ a
*-recip-impl {a} {b} h =
  trans (sym (one-mul-ℝ b))
        (trans (cong (λ x → x *ℝ b) (sym one-over-a-mul-a))
               (trans (*-assoc-ℝ (oneℝ /ℝ a) a b)
                      (trans (cong (λ x → (oneℝ /ℝ a) *ℝ x) h)
                             (*-ident-ℝ (oneℝ /ℝ a)))))
  where
  -- (1/a)·a = 1
  one-over-a-mul-a : (oneℝ /ℝ a) *ℝ a ≡ oneℝ
  one-over-a-mul-a = trans (*-comm-ℝ (oneℝ /ℝ a) a) (*-/cancel-ℝ a oneℝ)

-- (-x)·y = -(x·y)（经分配律 + 加性逆唯一）
neg-mul-ℝ : (x y : ℝ) → (negℝ x) *ℝ y ≡ negℝ (x *ℝ y)
neg-mul-ℝ x y =
  neg-unique-ℝ {a = x *ℝ y} {b = (negℝ x) *ℝ y}
    (trans (sym expand)
           (trans (cong (λ u → u *ℝ y) (+-inv-ℝ x)) (*-zero-l-ℝ y)))
  where
  -- (x + (-x))·y = x·y + (-x)·y
  expand : (x +ℝ negℝ x) *ℝ y ≡ (x *ℝ y) +ℝ ((negℝ x) *ℝ y)
  expand =
    trans (*-comm-ℝ (x +ℝ negℝ x) y)
          (trans (distrib-ℝ y x (negℝ x))
                 (cong₂ _+ℝ_ (*-comm-ℝ y x) (*-comm-ℝ y (negℝ x))))

-- ==================================================================
-- 加法重排与减法抵消（T3 阶段 4，可证）
-- 用途：闭合 B8 `moran-3map-holds`（c₁^d + c₂^d + c₃^d = 1，c₃ 定义含 1-c₁^d-c₂^d）。
-- ==================================================================

-- (a+b)+(c+d) = (a+c)+(b+d)（交换重排）
swap-pair : (a b c d : ℝ) → (a +ℝ b) +ℝ (c +ℝ d) ≡ (a +ℝ c) +ℝ (b +ℝ d)
swap-pair a b c d =
  trans (+-assoc-ℝ a b (c +ℝ d))
        (trans (cong (λ u → a +ℝ u) (+-comm-ℝ b (c +ℝ d)))
               (trans (sym (+-assoc-ℝ a (c +ℝ d) b))
                      (trans (cong (λ u → u +ℝ b) (sym (+-assoc-ℝ a c d)))
                             (trans (+-assoc-ℝ (a +ℝ c) d b)
                                    (cong (λ u → (a +ℝ c) +ℝ u) (+-comm-ℝ d b))))))

-- (x + y) + (-x) = y
add-neg-cancel : (x y : ℝ) → (x +ℝ y) +ℝ negℝ x ≡ y
add-neg-cancel x y =
  trans (+-assoc-ℝ x y (negℝ x))
        (trans (cong (λ u → x +ℝ u) (+-comm-ℝ y (negℝ x)))
               (trans (sym (+-assoc-ℝ x (negℝ x) y))
                      (trans (cong₂ _+ℝ_ (+-inv-ℝ x) refl)
                             (zero-add-ℝ y))))

-- (x + y) + ((z - x) - y) = z（减法定义展开 + 加法重排）
cancel-sub : (x y z : ℝ) → (x +ℝ y) +ℝ ((z -ℝ x) -ℝ y) ≡ z
cancel-sub x y z =
  trans (cong (λ u → (x +ℝ y) +ℝ u) sub-unfold)
        (trans (swap-pair x y (z +ℝ negℝ x) (negℝ y))
               (trans (cong₂ _+ℝ_ refl (+-inv-ℝ y))
                      (trans (+-ident-ℝ (x +ℝ (z +ℝ negℝ x)))
                             (trans (sym (+-assoc-ℝ x z (negℝ x)))
                                    (add-neg-cancel x z)))))
  where
  -- (z - x) - y = (z + (-x)) + (-y)
  sub-unfold : ((z -ℝ x) -ℝ y) ≡ ((z +ℝ negℝ x) +ℝ negℝ y)
  sub-unfold = trans (sub-ℝ-def (z -ℝ x) y)
                     (cong (λ u → u +ℝ negℝ y) (sub-ℝ-def z x))

-- ==================================================================
-- rpow 幂合成（T3 阶段 4，可证）
-- 用途：闭合 B8 `moran-3map-holds`（c₃^d 的 (1/d)·d = 1 约简）。
-- (a^b)^c = a^(b·c)（rpow-exp 展开 + 乘法结合/交换）
-- ==================================================================

-- (a^b)^c = a^(b·c)
rpow-pow : (a b c : ℝ) → ((a ^-ℝ b) ^-ℝ c) ≡ (a ^-ℝ (b *ℝ c))
rpow-pow a b c =
  trans (rpow-exp (a ^-ℝ b) c)
        (trans (cong (λ x → exp (c *ℝ log x)) (rpow-exp a b))
               (trans (cong (λ x → exp (c *ℝ x)) (log-exp (b *ℝ log a)))
                      (trans (cong exp (sym (*-assoc-ℝ c b (log a))))
                             (trans (cong (λ x → exp (x *ℝ log a)) (*-comm-ℝ c b))
                                    (sym (rpow-exp a (b *ℝ c)))))))

-- a^1 = a
rpow-one : (a : ℝ) → (a ^-ℝ oneℝ) ≡ a
rpow-one a =
  trans (rpow-exp a oneℝ)
        (trans (cong exp (one-mul-ℝ (log a)))
               (exp-log a))

-- 幂保持正性：0 < a ⟹ 0 < a^b（a^b = exp(b·log a) > 0）
rpow-pos : {a b : ℝ} → zeroℝ <ℝ a → zeroℝ <ℝ (a ^-ℝ b)
rpow-pos {a} {b} h =
  subst (λ x → zeroℝ <ℝ x) (sym (rpow-exp a b)) (exp-pos (b *ℝ log a))

-- 1 < 2（经 natℝ 嵌入）
one-lt-2-ℝ : oneℝ <ℝ natℝ 2
one-lt-2-ℝ = subst (λ x → x <ℝ natℝ 2) natℝ-one (natℝ-<-embed (<-suc 1))

-- (x+y) + ((-x)+(-y)) = 0（加法重排抵消）
zero-sum : (x y : ℝ) → (x +ℝ y) +ℝ ((negℝ x) +ℝ (negℝ y)) ≡ zeroℝ
zero-sum x y =
  trans (swap-pair x y (negℝ x) (negℝ y))
        (trans (cong₂ _+ℝ_ (+-inv-ℝ x) (+-inv-ℝ y))
               (zero-add-ℝ zeroℝ))

-- x + y < 1 ⟹ 0 < (1-x)-y（减法定义 + 加抵消）
pos-sub : {x y : ℝ} → (x +ℝ y) <ℝ oneℝ → zeroℝ <ℝ ((oneℝ -ℝ x) -ℝ y)
pos-sub {x} {y} h =
  subst (λ z → zeroℝ <ℝ z) (sym sub-unfold)
        (subst (λ w → zeroℝ <ℝ w) (sym (+-assoc-ℝ oneℝ (negℝ x) (negℝ y)))
               (subst (λ u → u <ℝ (oneℝ +ℝ ((negℝ x) +ℝ (negℝ y))))
                      (zero-sum x y)
                      (lt-+-mono-l-ℝ h)))
  where
  sub-unfold : ((oneℝ -ℝ x) -ℝ y) ≡ ((oneℝ +ℝ negℝ x) +ℝ negℝ y)
  sub-unfold =
    trans (sub-ℝ-def (oneℝ -ℝ x) y)
          (cong (λ u → u +ℝ negℝ y) (sub-ℝ-def oneℝ x))

-- 0 < y ⟹ x-y < x（减法递减）
sub-lt : {x y : ℝ} → zeroℝ <ℝ y → (x -ℝ y) <ℝ x
sub-lt {x} {y} h =
  subst (λ w → w <ℝ x) (sym (sub-ℝ-def x y))
        (subst (λ u → (x +ℝ negℝ y) <ℝ u) (+-ident-ℝ x)
               (lt-+-mono-r-ℝ (subst (λ z → (negℝ y) <ℝ z) neg-zero (neg-<-ℝ h))))

-- 0 < x ⟹ 1-x < 1
sub-one-lt : {x : ℝ} → zeroℝ <ℝ x → (oneℝ -ℝ x) <ℝ oneℝ
sub-one-lt {x} h = sub-lt {x = oneℝ} {y = x} h

-- 2·x = x + x（分配律 + 1+1=2）
two-mul-add : (x : ℝ) → (natℝ 2 *ℝ x) ≡ (x +ℝ x)
two-mul-add x =
  trans (cong (λ u → u *ℝ x) (natℝ-+ 1 1))
        (trans (*-comm-ℝ (natℝ 1 +ℝ natℝ 1) x)
               (trans (distrib-ℝ x (natℝ 1) (natℝ 1))
                      (cong₂ _+ℝ_ x-mul-one x-mul-one)))
  where
  -- x·1 = x（natℝ 1 → oneℝ + 单位元）
  x-mul-one : (x *ℝ natℝ 1) ≡ x
  x-mul-one = trans (cong₂ _*ℝ_ refl natℝ-one) (*-ident-ℝ x)

-- 移项：a + b < c ⟹ a < c - b（两边加 -b）
sub-elim : {a b c : ℝ} → (a +ℝ b) <ℝ c → a <ℝ (c -ℝ b)
sub-elim {a} {b} {c} h =
  subst (λ x → x <ℝ (c -ℝ b)) (add-neg-cancel b a)
        (subst (λ y → ((b +ℝ a) +ℝ negℝ b) <ℝ y) (sym (sub-ℝ-def c b))
               (lt-+-mono-l-ℝ (subst (λ u → u <ℝ c) (+-comm-ℝ a b) h)))

-- ==================================================================
-- 除法/取负代数与 ≤ 移项（T3 阶段 4 补充，2026-08-02）
-- 用途：Hilbert 空间层 Cauchy-Schwarz 不等式（阶段 8-2）——
--   t = -⟨x,y⟩/‖y‖² 的展开需 取负×乘 / 乘除结合 / 分数乘除消去；
--   终步 P/q ≤ A 且 0 < q ⟹ P ≤ A·q 需非负侧乘保序。
-- 全部为可证引理（零新增公理）。
-- ==================================================================

-- x·(-y) = -(x·y)（neg-mul-ℝ + 交换律）
neg-mul-r-ℝ : (x y : ℝ) → x *ℝ negℝ y ≡ negℝ (x *ℝ y)
neg-mul-r-ℝ x y = trans (*-comm-ℝ x (negℝ y))
                        (trans (neg-mul-ℝ y x) (cong negℝ (*-comm-ℝ y x)))

-- (-x)·(-y) = x·y（neg-mul-ℝ + neg-mul-r-ℝ + neg-neg）
neg-neg-mul-ℝ : (x y : ℝ) → (negℝ x) *ℝ (negℝ y) ≡ x *ℝ y
neg-neg-mul-ℝ x y =
  trans (neg-mul-ℝ x (negℝ y))
        (trans (cong negℝ (neg-mul-r-ℝ x y))
               (neg-neg (x *ℝ y)))

-- (x/a)/b = x/(a·b)（交叉相乘消去）
div-div-ℝ : (x a b : ℝ) → (x /ℝ a) /ℝ b ≡ x /ℝ (a *ℝ b)
div-div-ℝ x a b =
  /-cross-ℝ (trans (sym (*-assoc-ℝ (x /ℝ a) a b))
                   (cong (λ u → u *ℝ b)
                         (trans (*-comm-ℝ (x /ℝ a) a) (*-/cancel-ℝ a x))))

-- (a/c)·(b/d) = (a·b)/(c·d)（*-/ℝ 两次 + div-div-ℝ）
frac-mul-ℝ : (a b c d : ℝ) → (a /ℝ c) *ℝ (b /ℝ d) ≡ (a *ℝ b) /ℝ (c *ℝ d)
frac-mul-ℝ a b c d =
  trans (*-/ℝ (a /ℝ c) b d)
        (trans (cong (λ u → u /ℝ d)
                     (trans (*-comm-ℝ (a /ℝ c) b)
                            (trans (*-/ℝ b a c)
                                   (cong (λ u → u /ℝ c) (*-comm-ℝ b a)))))
               (div-div-ℝ (a *ℝ b) c d))

-- 0 ≤ a + (-b) ⟹ b ≤ a（移项：两边加 b）
≤-from-nonneg : {a b : ℝ} → zeroℝ ≤ℝ (a +ℝ negℝ b) → b ≤ℝ a
≤-from-nonneg {a} {b} h =
  subst (λ v → b ≤ℝ v) (add-neg-ident a b)
        (subst (λ u → u ≤ℝ ((a +ℝ negℝ b) +ℝ b)) (zero-add-ℝ b)
               (≤-+-mono-ℝ h (refl-≤ℝ {x = b})))
  where
  -- (a + (-b)) + b = a（结合 + 交换 + 逆 + 单位）
  add-neg-ident : (a b : ℝ) → (a +ℝ negℝ b) +ℝ b ≡ a
  add-neg-ident a b =
    trans (+-assoc-ℝ a (negℝ b) b)
          (trans (cong (λ u → a +ℝ u) (+-comm-ℝ (negℝ b) b))
                 (trans (cong (λ u → a +ℝ u) (+-inv-ℝ b))
                        (+-ident-ℝ a)))

-- p/q ≤ a 且 0 ≤ q ⟹ p ≤ a·q（非负侧乘保序 + 乘除消去）
div-≤-mul : {p a q : ℝ} → zeroℝ ≤ℝ q → (p /ℝ q) ≤ℝ a → p ≤ℝ (a *ℝ q)
div-≤-mul {p} {a} {q} hq h =
  subst (λ u → u ≤ℝ (a *ℝ q))
        (trans (*-comm-ℝ (p /ℝ q) q) (*-/cancel-ℝ q p))
        (*-≤-mono-ℝ {a = p /ℝ q} {b = a} {c = q} hq h)

-- t·p 约简：(-(p/q))·p = -(p²/q)（Cauchy-Schwarz 展开的 t 侧）
tp-ident : (p q : ℝ) → (negℝ (p /ℝ q)) *ℝ p ≡ negℝ ((p *ℝ p) /ℝ q)
tp-ident p q =
  trans (neg-mul-ℝ (p /ℝ q) p)
        (cong negℝ (trans (*-comm-ℝ (p /ℝ q) p) (*-/ℝ p p q)))

-- t²·q 约简：(-(p/q))²·q = p²/q（Cauchy-Schwarz 展开的 t² 侧）
ttq-ident : (p q : ℝ) → ((negℝ (p /ℝ q)) *ℝ (negℝ (p /ℝ q))) *ℝ q ≡ ((p *ℝ p) /ℝ q)
ttq-ident p q =
  trans (cong (λ u → u *ℝ q)
              (trans (neg-neg-mul-ℝ (p /ℝ q) (p /ℝ q))
                     (frac-mul-ℝ p p q q)))
        (trans (*-comm-ℝ ((p *ℝ p) /ℝ (q *ℝ q)) q)
               (trans (*-/ℝ q (p *ℝ p) (q *ℝ q))
                      (trans (cong (λ u → u /ℝ (q *ℝ q)) (*-comm-ℝ q (p *ℝ p)))
                             (frac-cancel-ℝ (p *ℝ p) q q))))

-- ==================================================================
-- min-ℝ（测度论层阶段 1 前置，2026-08-02）
-- 用途：无界函数的截断逼近 f_c = min(f, c)（蓝图 §5.15 阶段 7-1）——
--   恒等/exp/φ_t 等无界函数经截断族逼近 ∫f dE = supₙ ∫min(f,n) dE。
-- min-ℝ 经三分律定义（标准有序域事实，可证性质、零新增公理）。
-- ==================================================================

-- min(a,b)：三分律取较小者
min-ℝ : ℝ → ℝ → ℝ
min-ℝ a b with trichotomy-ℝ a b
min-ℝ a b | inj₁ _ = a
min-ℝ a b | inj₂ (inj₁ _) = a
min-ℝ a b | inj₂ (inj₂ _) = b

-- min(a,b) ≤ a
min-≤-l : (a b : ℝ) → min-ℝ a b ≤ℝ a
min-≤-l a b with trichotomy-ℝ a b
min-≤-l a b | inj₁ _ = refl-≤ℝ {x = a}
min-≤-l a b | inj₂ (inj₁ _) = refl-≤ℝ {x = a}
min-≤-l a b | inj₂ (inj₂ b<a) = <-≤-ℝ b<a

-- min(a,b) ≤ b
min-≤-r : (a b : ℝ) → min-ℝ a b ≤ℝ b
min-≤-r a b with trichotomy-ℝ a b
min-≤-r a b | inj₁ a<b = <-≤-ℝ a<b
min-≤-r a b | inj₂ (inj₁ a=b) = subst (λ z → z ≤ℝ b) (sym a=b) (refl-≤ℝ {x = b})
min-≤-r a b | inj₂ (inj₂ _) = refl-≤ℝ {x = b}

-- min 是最小下界：z ≤ a 且 z ≤ b ⟹ z ≤ min(a,b)
min-glb : (z a b : ℝ) → z ≤ℝ a → z ≤ℝ b → z ≤ℝ min-ℝ a b
min-glb z a b hza hzb with trichotomy-ℝ a b
min-glb z a b hza hzb | inj₁ _ = hza
min-glb z a b hza hzb | inj₂ (inj₁ _) = hza
min-glb z a b hza hzb | inj₂ (inj₂ _) = hzb

-- 吸收（左）：a ≤ b ⟹ min(a,b) = a
min-absorp-l : (a b : ℝ) → a ≤ℝ b → min-ℝ a b ≡ a
min-absorp-l a b hab with trichotomy-ℝ a b
min-absorp-l a b hab | inj₁ _ = refl
min-absorp-l a b hab | inj₂ (inj₁ _) = refl
min-absorp-l a b hab | inj₂ (inj₂ b<a) =
  ⊥-elim (irreflexive-ℝ (lt-≤-trans-ℝ b<a hab))

-- 右单调：b ≤ c ⟹ min(a,b) ≤ min(a,c)（min-glb + min-≤-l/r）
min-mono-r : (a b c : ℝ) → b ≤ℝ c → min-ℝ a b ≤ℝ min-ℝ a c
min-mono-r a b c hbc =
  min-glb (min-ℝ a b) a c (min-≤-l a b) (≤-trans-ℝ (min-≤-r a b) hbc)

-- ==================================================================
-- max-ℝ 与正负分解（方案 A 阶段 1，2026-08-03）
-- 用途：fc-poly-le-spec-int 语义重构（笔记 §5.16.8 方案 A）——
--   f⁺ = max(f,0)、f⁻ = max(−f,0)，∫f dE = ∫f⁺ dE − ∫f⁻ dE 的 ℝ 层地基。
-- max 与 min-ℝ 平行（三分律定义），全部可证（零新增公理）。
-- ==================================================================

-- max(a,b)：a < b ⟹ b；a = b ⟹ a；b < a ⟹ a
max-ℝ : ℝ → ℝ → ℝ
max-ℝ a b with trichotomy-ℝ a b
max-ℝ a b | inj₁ _ = b
max-ℝ a b | inj₂ (inj₁ _) = a
max-ℝ a b | inj₂ (inj₂ _) = a

-- a ≤ max(a,b)
max-≤-l : (a b : ℝ) → a ≤ℝ max-ℝ a b
max-≤-l a b with trichotomy-ℝ a b
max-≤-l a b | inj₁ a<b = <-≤-ℝ a<b
max-≤-l a b | inj₂ (inj₁ _) = refl-≤ℝ {x = a}
max-≤-l a b | inj₂ (inj₂ _) = refl-≤ℝ {x = a}

-- b ≤ max(a,b)
max-≤-r : (a b : ℝ) → b ≤ℝ max-ℝ a b
max-≤-r a b with trichotomy-ℝ a b
max-≤-r a b | inj₁ _ = refl-≤ℝ {x = b}
max-≤-r a b | inj₂ (inj₁ a=b) = subst (λ z → b ≤ℝ z) (sym a=b) (refl-≤ℝ {x = b})
max-≤-r a b | inj₂ (inj₂ b<a) = <-≤-ℝ b<a

-- max 是最小上界：a ≤ z 且 b ≤ z ⟹ max(a,b) ≤ z
max-lub : (z a b : ℝ) → a ≤ℝ z → b ≤ℝ z → max-ℝ a b ≤ℝ z
max-lub z a b hza hzb with trichotomy-ℝ a b
max-lub z a b hza hzb | inj₁ _ = hzb
max-lub z a b hza hzb | inj₂ (inj₁ _) = hza
max-lub z a b hza hzb | inj₂ (inj₂ _) = hza

-- 正部特化：0 < a ⟹ max(a,0) = a
max-pos-value : (a : ℝ) → zeroℝ <ℝ a → max-ℝ a zeroℝ ≡ a
max-pos-value a 0<a with trichotomy-ℝ a zeroℝ
max-pos-value a 0<a | inj₁ a<0 =
  ⊥-elim (irreflexive-ℝ (lt-≤-trans-ℝ a<0 (<-≤-ℝ 0<a)))
max-pos-value a 0<a | inj₂ (inj₁ _) = refl
max-pos-value a 0<a | inj₂ (inj₂ _) = refl

-- 负部特化：a < 0 ⟹ max(a,0) = 0
max-neg-value : (a : ℝ) → a <ℝ zeroℝ → max-ℝ a zeroℝ ≡ zeroℝ
max-neg-value a a<0 with trichotomy-ℝ a zeroℝ
max-neg-value a a<0 | inj₁ _ = refl
max-neg-value a a<0 | inj₂ (inj₁ a=0) = a=0
max-neg-value a a<0 | inj₂ (inj₂ 0<a) =
  ⊥-elim (irreflexive-ℝ (lt-≤-trans-ℝ 0<a (<-≤-ℝ a<0)))

-- a < 0 ⟹ 0 < −a（取负反转，neg-<-ℝ + neg-zero）
lt-neg-ℝ : {a : ℝ} → a <ℝ zeroℝ → zeroℝ <ℝ negℝ a
lt-neg-ℝ {a} a<0 = subst (λ z → z <ℝ negℝ a) neg-zero (neg-<-ℝ a<0)

-- 0 < a ⟹ −a < 0（取负反转）
neg-lt-ℝ : {a : ℝ} → zeroℝ <ℝ a → negℝ a <ℝ zeroℝ
neg-lt-ℝ {a} 0<a = subst (λ z → negℝ a <ℝ z) neg-zero (neg-<-ℝ 0<a)

-- max(0,0) = 0（三分支排除：0 < 0 矛盾）
max-zero-zero : max-ℝ zeroℝ zeroℝ ≡ zeroℝ
max-zero-zero with trichotomy-ℝ zeroℝ zeroℝ
max-zero-zero | inj₁ 0<0 = ⊥-elim (irreflexive-ℝ 0<0)
max-zero-zero | inj₂ (inj₁ _) = refl
max-zero-zero | inj₂ (inj₂ 0<0) = ⊥-elim (irreflexive-ℝ 0<0)

-- a − 0 = a（sub-ℝ-def + neg-zero + 加单位）
sub-zero-r : (a : ℝ) → (a -ℝ zeroℝ) ≡ a
sub-zero-r a = trans (sub-ℝ-def a zeroℝ)
                     (trans (cong (λ w → a +ℝ w) neg-zero) (+-ident-ℝ a))

-- 0 − c = −c（sub-ℝ-def + 交换 + 加单位）
zero-sub : (c : ℝ) → (zeroℝ -ℝ c) ≡ negℝ c
zero-sub c = trans (sub-ℝ-def zeroℝ c)
                   (trans (+-comm-ℝ zeroℝ (negℝ c)) (+-ident-ℝ (negℝ c)))

-- 分解：max(a,0) − max(−a,0) = a（f = f⁺ − f⁻ 的 ℝ 值版）
-- 三分律三分 a：a<0 ⟹ 0 − (−a) = a；a=0 ⟹ 0 − 0 = 0；a>0 ⟹ a − 0 = a
max-sub-decomp : (a : ℝ) → (max-ℝ a zeroℝ) -ℝ (max-ℝ (negℝ a) zeroℝ) ≡ a
max-sub-decomp a with trichotomy-ℝ a zeroℝ
max-sub-decomp a | inj₁ a<0 =
  trans (cong (λ v → zeroℝ -ℝ v) (max-pos-value (negℝ a) (lt-neg-ℝ a<0)))
        (trans (zero-sub (negℝ a)) (neg-neg a))
max-sub-decomp a | inj₂ (inj₁ a=0) =
  trans (cong (λ v → a -ℝ v)
              (trans (cong₂ max-ℝ (trans (cong negℝ a=0) neg-zero) refl) max-zero-zero))
        (sub-zero-r a)
max-sub-decomp a | inj₂ (inj₂ 0<a) =
  trans (cong (λ v → a -ℝ v) (max-neg-value (negℝ a) (neg-lt-ℝ 0<a)))
        (sub-zero-r a)

-- 正交性：max(a,0)·max(−a,0) = 0（f⁺·f⁻ = 0，三分律三分 + 零吸收）
max-pos-mul-neg-zero : (a : ℝ) → (max-ℝ a zeroℝ) *ℝ (max-ℝ (negℝ a) zeroℝ) ≡ zeroℝ
max-pos-mul-neg-zero a with trichotomy-ℝ a zeroℝ
max-pos-mul-neg-zero a | inj₁ a<0 = *-zero-l-ℝ (max-ℝ (negℝ a) zeroℝ)
max-pos-mul-neg-zero a | inj₂ (inj₁ a=0) =
  trans (cong (λ v → a *ℝ v)
              (trans (cong₂ max-ℝ (trans (cong negℝ a=0) neg-zero) refl) max-zero-zero))
        (*-zero-ℝ a)
max-pos-mul-neg-zero a | inj₂ (inj₂ 0<a) =
  trans (cong (λ v → a *ℝ v) (max-neg-value (negℝ a) (neg-lt-ℝ 0<a)))
        (*-zero-ℝ a)

-- ==================================================================
-- dyadic 网格 ℝ 基础（方案 A 阶段 4 余项，2026-08-03）
-- 用途：fc-poly-le-spec-int 构造化的 dyadic 阶梯逼近——[0,c] 的 2^k 等分
--   网格点 xⱼ = (j·c)/2^k（natℝ 嵌入 + 除法的非负/保序基础）。
-- ==================================================================

-- **可证**：natℝ 嵌入非负——0 ≤ natℝ j（j=0 经 natℝ-zero；j>0 经 natℝ-pos-embed + <-≤-ℝ）
natℝ-nonneg : (j : ℕ) → zeroℝ ≤ℝ natℝ j
natℝ-nonneg zero = subst (λ z → zeroℝ ≤ℝ z) (sym natℝ-zero) (refl-≤ℝ {x = zeroℝ})
natℝ-nonneg (suc j) = <-≤-ℝ (natℝ-pos-embed (z<s {j}))

-- 零除以正数 = 0（基础假设，标准有序域事实，与 /-pos-ℝ 同层）
postulate
  div-zero-l : (d : ℝ) → zeroℝ /ℝ d ≡ zeroℝ

-- **可证**：非负除以正 = 非负——0 ≤ a 且 0 < d ⟹ 0 ≤ a/d
--（三分律：0<a ⟹ /-pos-ℝ（严格保序）；a=0 ⟹ div-zero-l；a<0 矛盾排除）
div-nonneg : {a d : ℝ} → zeroℝ ≤ℝ a → zeroℝ <ℝ d → zeroℝ ≤ℝ (a /ℝ d)
div-nonneg {a} {d} ha hd with trichotomy-ℝ zeroℝ a
div-nonneg {a} {d} ha hd | inj₁ 0<a = <-≤-ℝ (/-pos-ℝ 0<a hd)
div-nonneg {a} {d} ha hd | inj₂ (inj₁ 0=a) =
  subst (λ z → zeroℝ ≤ℝ (z /ℝ d)) 0=a
        (subst (λ w → zeroℝ ≤ℝ w) (sym (div-zero-l d)) (refl-≤ℝ {x = zeroℝ}))
div-nonneg {a} {d} ha hd | inj₂ (inj₂ a<0) =
  ⊥-elim (irreflexive-ℝ (lt-≤-trans-ℝ a<0 ha))

-- ==================================================================
-- 平方根（分析层扩展，2026-08-02）
-- 用途：Hilbert 空间层阶段 8-2b 收官——norm := √(‖·‖²)（范数公理落地）、
--   三角不等式（C-S 推论）与阶段 8-3 有界算子范数（sup + √）的前提。
-- 平方根为标准分析结构，与 exp/log 同层登记基础假设；
-- 降定理路径：Dedekind 完备性层（√x = sup{y : y² ≤ x} 构造）。
-- ==================================================================
postulate
  sqrt : ℝ → ℝ
  -- 非负性：0 ≤ x ⟹ 0 ≤ √x
  sqrt-nonneg : (x : ℝ) → zeroℝ ≤ℝ x → zeroℝ ≤ℝ sqrt x
  -- (√x)² = x（定义性：x ≥ 0）
  sq-sqrt : (x : ℝ) → zeroℝ ≤ℝ x → (sqrt x) *ℝ (sqrt x) ≡ x
  -- √(x²) = x（x ≥ 0）
  sqrt-sq : (x : ℝ) → zeroℝ ≤ℝ x → sqrt (x *ℝ x) ≡ x
  -- 单调：0 ≤ x ≤ y ⟹ √x ≤ √y
  sqrt-mono : {x y : ℝ} → zeroℝ ≤ℝ x → x ≤ℝ y → sqrt x ≤ℝ sqrt y
  -- √0 = 0
  sqrt-zero : sqrt zeroℝ ≡ zeroℝ
  -- 乘法性：0 ≤ x、0 ≤ y ⟹ √(xy) = √x·√y
  sqrt-mul : (x y : ℝ) → zeroℝ ≤ℝ x → zeroℝ ≤ℝ y → sqrt (x *ℝ y) ≡ (sqrt x) *ℝ (sqrt y)

-- 0 < a ⟹ 0 ≤ a²（乘保序）
pos-sq : (a : ℝ) → zeroℝ <ℝ a → zeroℝ ≤ℝ (a *ℝ a)
pos-sq a ha =
  subst (λ z → z ≤ℝ (a *ℝ a)) (*-zero-l-ℝ a)
        (*-≤-mono-ℝ {a = zeroℝ} {b = a} {c = a} (<-≤-ℝ ha) (<-≤-ℝ ha))

-- a² ≥ 0（三分律：0<a 直接；a=0 平凡；a<0 经 (-a)² = a²）
sq-nonneg-ℝ : (a : ℝ) → zeroℝ ≤ℝ (a *ℝ a)
sq-nonneg-ℝ a with trichotomy-ℝ zeroℝ a
sq-nonneg-ℝ a | inj₁ 0<a = pos-sq a 0<a
sq-nonneg-ℝ a | inj₂ (inj₁ 0=a) =
  subst (λ z → zeroℝ ≤ℝ z)
        (sym (trans (sym (cong₂ _*ℝ_ 0=a 0=a)) (*-zero-ℝ zeroℝ)))
        (refl-≤ℝ {zeroℝ})
sq-nonneg-ℝ a | inj₂ (inj₂ a<0) =
  subst (λ z → zeroℝ ≤ℝ z) (neg-neg-mul-ℝ a a)
        (pos-sq (negℝ a) 0<neg-a)
  where
  -- a < 0 ⟹ 0 < -a（取负保序反转）
  0<neg-a : zeroℝ <ℝ negℝ a
  0<neg-a = subst (λ z → z <ℝ negℝ a) neg-zero (neg-<-ℝ a<0)

-- a ≤ √(a²)（三分律：a<0 经 √(a²) ≥ 0；a≥0 经 sqrt-sq）
le-sqrt-sq : (a : ℝ) → a ≤ℝ sqrt (a *ℝ a)
le-sqrt-sq a with trichotomy-ℝ zeroℝ a
le-sqrt-sq a | inj₁ 0<a =
  subst (λ z → a ≤ℝ z) (sym (sqrt-sq a (<-≤-ℝ 0<a))) (refl-≤ℝ {a})
le-sqrt-sq a | inj₂ (inj₁ 0=a) =
  subst (λ z → a ≤ℝ z) (sym (trans (cong sqrt (trans (sym (cong₂ _*ℝ_ 0=a 0=a)) (*-zero-ℝ zeroℝ)))
                                    sqrt-zero))
        (subst (λ z → z ≤ℝ zeroℝ) 0=a (refl-≤ℝ {zeroℝ}))
le-sqrt-sq a | inj₂ (inj₂ a<0) =
  <-≤-ℝ (lt-≤-trans-ℝ a<0 (sqrt-nonneg (a *ℝ a) (sq-nonneg-ℝ a)))

-- 绝对值（可证定义）：|a| := √(a²)
abs : ℝ → ℝ
abs a = sqrt (a *ℝ a)

-- 0 ≤ a ⟹ |a| = a（abs = √(a²) + sqrt-sq）
abs-pos-ident : (a : ℝ) → zeroℝ ≤ℝ a → abs a ≡ a
abs-pos-ident a ha = sqrt-sq a ha

-- 左侧乘保序：0 ≤ a ⟹ b ≤ c ⟹ a·b ≤ a·c（*-≤-mono-ℝ + 交换律）
*-≤-mono-l-ℝ : (a b c : ℝ) → zeroℝ ≤ℝ a → b ≤ℝ c → (a *ℝ b) ≤ℝ (a *ℝ c)
*-≤-mono-l-ℝ a b c ha hbc =
  subst (λ z → z ≤ℝ (a *ℝ c)) (sym (*-comm-ℝ a b))
        (subst (λ z → (b *ℝ a) ≤ℝ z) (sym (*-comm-ℝ a c))
               (*-≤-mono-ℝ {a = b} {b = c} {c = a} ha hbc))

-- 乘积非负：0 ≤ a 且 0 ≤ b ⟹ 0 ≤ a·b（*-≤-mono-ℝ 以 0 为左端 + 零吸收）
--（测度论逼近引理库阶段 1 前置，2026-08-03：幂单调性 power-mono 的基础组件）
*-nonneg-ℝ : (a b : ℝ) → zeroℝ ≤ℝ a → zeroℝ ≤ℝ b → zeroℝ ≤ℝ (a *ℝ b)
*-nonneg-ℝ a b ha hb =
  subst (λ z → z ≤ℝ (a *ℝ b)) (*-zero-l-ℝ b)
        (*-≤-mono-ℝ {a = zeroℝ} {b = a} {c = b} hb ha)

-- 反对称：a ≤ b 且 b ≤ a ⟹ a = b（三分律排除两严格分支）
≤-antisym : {a b : ℝ} → a ≤ℝ b → b ≤ℝ a → a ≡ b
≤-antisym {a} {b} hab hba with trichotomy-ℝ a b
≤-antisym {a} {b} hab hba | inj₁ a<b = ⊥-elim (irreflexive-ℝ (lt-≤-trans-ℝ a<b hba))
≤-antisym {a} {b} hab hba | inj₂ (inj₁ a=b) = a=b
≤-antisym {a} {b} hab hba | inj₂ (inj₂ b<a) = ⊥-elim (irreflexive-ℝ (lt-≤-trans-ℝ b<a hab))

-- 右侧严格乘保序：0 < c ⟹ a < b ⟹ a·c < b·c（*-pos-mono-ℝ + 交换律）
*-pos-mono-r-ℝ : {a b c : ℝ} → zeroℝ <ℝ c → a <ℝ b → (a *ℝ c) <ℝ (b *ℝ c)
*-pos-mono-r-ℝ {a} {b} {c} hc hab =
  subst (λ z → z <ℝ (b *ℝ c)) (sym (*-comm-ℝ a c))
        (subst (λ z → (c *ℝ a) <ℝ z) (sym (*-comm-ℝ b c))
               (*-pos-mono-ℝ {a = a} {b = b} {c = c} hc hab))

-- (a+b)² = a² + 2ab + b²（分配律 + 重排）
sum-sq-ℝ : (a b : ℝ) → (a +ℝ b) *ℝ (a +ℝ b) ≡ ((a *ℝ a) +ℝ (natℝ 2 *ℝ (a *ℝ b))) +ℝ (b *ℝ b)
sum-sq-ℝ a b = trans expand regroup
  where
  -- (a+b)(a+b) = (a·a + a·b) + (a·b + b·b)
  expand : (a +ℝ b) *ℝ (a +ℝ b) ≡ ((a *ℝ a) +ℝ (a *ℝ b)) +ℝ ((a *ℝ b) +ℝ (b *ℝ b))
  expand =
    trans (distrib-ℝ (a +ℝ b) a b)
          (cong₂ _+ℝ_
                 (trans (*-comm-ℝ (a +ℝ b) a) (distrib-ℝ a a b))
                 (trans (*-comm-ℝ (a +ℝ b) b)
                        (trans (distrib-ℝ b a b)
                               (cong₂ _+ℝ_ (*-comm-ℝ b a) refl))))
  -- 重排：a·b + a·b = 2ab（two-mul-add 反向 + 结合）
  regroup : ((a *ℝ a) +ℝ (a *ℝ b)) +ℝ ((a *ℝ b) +ℝ (b *ℝ b))
    ≡ ((a *ℝ a) +ℝ (natℝ 2 *ℝ (a *ℝ b))) +ℝ (b *ℝ b)
  regroup =
    trans (+-assoc-ℝ (a *ℝ a) (a *ℝ b) ((a *ℝ b) +ℝ (b *ℝ b)))
          (trans (cong (λ u → (a *ℝ a) +ℝ u)
                       (sym (+-assoc-ℝ (a *ℝ b) (a *ℝ b) (b *ℝ b))))
                 (trans (cong (λ u → (a *ℝ a) +ℝ u)
                              (cong₂ _+ℝ_ (sym (two-mul-add (a *ℝ b))) refl))
                        (sym (+-assoc-ℝ (a *ℝ a) (natℝ 2 *ℝ (a *ℝ b)) (b *ℝ b)))))

-- (A+M) + (M+B) = A + 2M + B（三角不等式重排）
two-add-eq : (A M B : ℝ) → (A +ℝ M) +ℝ (M +ℝ B) ≡ (A +ℝ (natℝ 2 *ℝ M)) +ℝ B
two-add-eq A M B =
  trans (+-assoc-ℝ A M (M +ℝ B))
        (trans (cong (λ u → A +ℝ u) (sym (+-assoc-ℝ M M B)))
               (trans (cong (λ u → A +ℝ u) (cong₂ _+ℝ_ (sym (two-mul-add M)) refl))
                      (sym (+-assoc-ℝ A (natℝ 2 *ℝ M) B))))

-- p ≤ M ⟹ (A+p)+(p+B) ≤ (A+M)+(M+B)（≤-+-mono 逐项）
sum-add-≤ : (A p B M : ℝ) → p ≤ℝ M → ((A +ℝ p) +ℝ (p +ℝ B)) ≤ℝ ((A +ℝ M) +ℝ (M +ℝ B))
sum-add-≤ A p B M hpm =
  ≤-+-mono-ℝ (≤-+-mono-ℝ (refl-≤ℝ {A}) hpm)
             (≤-+-mono-ℝ hpm (refl-≤ℝ {B}))

-- ==================================================================
-- B8 two-exp-add-exp-lt-one 辅助（T3 阶段 4，2026-07-31）
-- 目标：d ≥ 1 ⟹ 2e^{-d²} + e^{-d(3+d)} < 1
-- 策略：d² ≥ 1 ⟹ e^{-d²} ≤ e^{-1} < 37/100；d(3+d) ≥ 4 ⟹ e^{-d(3+d)} ≤ e^{-4} < 1/16
--       [e > 2 ⟹ e⁴ > 16 ⟹ e^{-4} < 1/16]；和 < 74/100 + 1/16 = 1284/1600 < 1。
-- ==================================================================

-- 1 ≤ d ⟹ 0 < d（≤-pos 的 DHStructural 版，避免与 IFSFractal 冲突）
≤-pos-ℝ : {d : ℝ} → natℝ 1 ≤ℝ d → zeroℝ <ℝ d
≤-pos-ℝ {d} h = lt-≤-trans-ℝ (subst (λ x → zeroℝ <ℝ x) (sym natℝ-one) zero-lt-one-ℝ) h

-- 1 ≤ d ⟹ 1 ≤ d·d（平方保序）
d-sq-ge-1 : {d : ℝ} → natℝ 1 ≤ℝ d → natℝ 1 ≤ℝ (d *ℝ d)
d-sq-ge-1 {d} h =
  ≤-trans-ℝ h
    (subst (λ x → x ≤ℝ (d *ℝ d)) (trans (cong (λ y → y *ℝ d) natℝ-one) (one-mul-ℝ d))
           (*-≤-mono-ℝ {a = natℝ 1} {b = d} {c = d} (le-0-d) h))
  where
  -- 0 ≤ d
  le-0-d : zeroℝ ≤ℝ d
  le-0-d = <-≤-ℝ (≤-pos-ℝ h)

-- 1 ≤ d ⟹ 4 ≤ d·(3+d)
d-3d-ge-4 : {d : ℝ} → natℝ 1 ≤ℝ d → natℝ 4 ≤ℝ (d *ℝ (natℝ 3 +ℝ d))
d-3d-ge-4 {d} h =
  ≤-trans-ℝ four-le-3d
    (subst (λ x → x ≤ℝ (d *ℝ (natℝ 3 +ℝ d))) (sq-le-3d)
           (*-≤-mono-ℝ {a = natℝ 1} {b = d} {c = natℝ 3 +ℝ d} le-0-3d h))
  where
  -- 4 ≤ 3+d（1 ≤ d ⟹ 1+3 ≤ d+3）
  four-le-3d : natℝ 4 ≤ℝ (natℝ 3 +ℝ d)
  four-le-3d =
    subst (λ x → x ≤ℝ (natℝ 3 +ℝ d)) (sym (natℝ-+ 1 3))
          (subst (λ y → (natℝ 1 +ℝ natℝ 3) ≤ℝ y) (sym (+-comm-ℝ (natℝ 3) d))
                 (≤-+-mono-ℝ h (refl-≤ℝ {x = natℝ 3})))
  -- 0 ≤ 3+d（0 < 3+d 经 <-≤-ℝ）
  le-0-3d : zeroℝ ≤ℝ (natℝ 3 +ℝ d)
  le-0-3d = <-≤-ℝ (subst (λ x → x <ℝ (natℝ 3 +ℝ d)) (+-ident-ℝ zeroℝ)
                          (lt-+-mono-ℝ (natℝ-pos-embed z<s) (≤-pos-ℝ h)))
  -- 1·(3+d) ≡ 3+d（natℝ 1 → oneℝ + 单位元）
  sq-le-3d : (natℝ 1 *ℝ (natℝ 3 +ℝ d)) ≡ (natℝ 3 +ℝ d)
  sq-le-3d = trans (cong (λ y → y *ℝ (natℝ 3 +ℝ d)) natℝ-one) (one-mul-ℝ (natℝ 3 +ℝ d))

-- partial-e 1 = 2（1/1 + 1/1 = 2/1 = 2）
partial-e-1-value : partial-e 1 ≡ natℝ 2
partial-e-1-value =
  trans (cong₂ _+ℝ_ r0 r1)
        (trans (cong₂ _+ℝ_ (sym natℝ-one) (sym natℝ-one)) (sym (natℝ-+ 1 1)))
  where
  -- 1/1 = 1（recip-factorial 0）
  r0 : recip-factorial 0 ≡ oneℝ
  r0 = trans (cong₂ _/ℝ_ natℝ-one natℝ-one) (div-one-ℝ oneℝ)
  -- 1/1 = 1（recip-factorial 1，factorial 1 = 1）
  r1 : recip-factorial 1 ≡ oneℝ
  r1 = trans (cong₂ _/ℝ_ natℝ-one natℝ-one) (div-one-ℝ oneℝ)

-- 2 < e（partial-e 1 = 2 < exp 1 = e）
e-gt-2 : natℝ 2 <ℝ e
e-gt-2 =
  subst (λ y → natℝ 2 <ℝ y) (sym e-def)
    (subst (λ x → x <ℝ exp oneℝ) partial-e-1-value (exp-partial-< 1))

-- 0 < e（exp-pos oneℝ 经 e-def）
e-pos : zeroℝ <ℝ e
e-pos = subst (λ x → zeroℝ <ℝ x) (sym e-def) (exp-pos oneℝ)

-- e·e > 4（e > 2 平方）
e2-gt-4 : natℝ 4 <ℝ (e *ℝ e)
e2-gt-4 =
  subst (λ x → x <ℝ (e *ℝ e)) (sym (natℝ-* 2 2))
        (trans-<ℝ four-lt-2e 2e-lt-ee)
  where
  -- 2·2 < 2·e
  four-lt-2e : (natℝ 2 *ℝ natℝ 2) <ℝ (natℝ 2 *ℝ e)
  four-lt-2e = *-pos-mono-ℝ {a = natℝ 2} {b = e} {c = natℝ 2} (natℝ-pos-embed z<s) e-gt-2
  -- 2·e < e·e（e·2 < e·e 经交换）
  two-e-lt-ee : (e *ℝ natℝ 2) <ℝ (e *ℝ e)
  two-e-lt-ee = *-pos-mono-ℝ {a = natℝ 2} {b = e} {c = e} e-pos e-gt-2
  2e-lt-ee : (natℝ 2 *ℝ e) <ℝ (e *ℝ e)
  2e-lt-ee = subst (λ x → x <ℝ (e *ℝ e)) (sym (*-comm-ℝ (natℝ 2) e)) two-e-lt-ee

-- e·e·e > 8（e² > 4 乘 e）
e3-gt-8 : natℝ 8 <ℝ (e *ℝ (e *ℝ e))
e3-gt-8 =
  subst (λ x → x <ℝ (e *ℝ (e *ℝ e))) (sym (natℝ-* 4 2))
        (trans-<ℝ eight-lt-4e 4e-lt-e3)
  where
  -- 4·2 < 4·e
  eight-lt-4e : (natℝ 4 *ℝ natℝ 2) <ℝ (natℝ 4 *ℝ e)
  eight-lt-4e = *-pos-mono-ℝ {a = natℝ 2} {b = e} {c = natℝ 4} (natℝ-pos-embed z<s) e-gt-2
  -- 4·e < e·(e·e)（e·4 < e·(e·e) 经交换）
  four-e-lt-e3 : (e *ℝ natℝ 4) <ℝ (e *ℝ (e *ℝ e))
  four-e-lt-e3 = *-pos-mono-ℝ {a = natℝ 4} {b = e *ℝ e} {c = e} e-pos e2-gt-4
  4e-lt-e3 : (natℝ 4 *ℝ e) <ℝ (e *ℝ (e *ℝ e))
  4e-lt-e3 = subst (λ x → x <ℝ (e *ℝ (e *ℝ e))) (sym (*-comm-ℝ (natℝ 4) e)) four-e-lt-e3

-- e·e·e·e > 16（e³ > 8 乘 e）
e4-gt-16 : natℝ 16 <ℝ (e *ℝ (e *ℝ (e *ℝ e)))
e4-gt-16 =
  subst (λ x → x <ℝ (e *ℝ (e *ℝ (e *ℝ e)))) (sym (natℝ-* 8 2))
        (trans-<ℝ sixteen-lt-8e 8e-lt-e4)
  where
  -- 8·2 < 8·e
  sixteen-lt-8e : (natℝ 8 *ℝ natℝ 2) <ℝ (natℝ 8 *ℝ e)
  sixteen-lt-8e = *-pos-mono-ℝ {a = natℝ 2} {b = e} {c = natℝ 8} (natℝ-pos-embed z<s) e-gt-2
  -- 8·e < e·(e·(e·e))（e·8 < e·(e·(e·e)) 经交换）
  eight-e-lt-e4 : (e *ℝ natℝ 8) <ℝ (e *ℝ (e *ℝ (e *ℝ e)))
  eight-e-lt-e4 = *-pos-mono-ℝ {a = natℝ 8} {b = e *ℝ (e *ℝ e)} {c = e} e-pos e3-gt-8
  8e-lt-e4 : (natℝ 8 *ℝ e) <ℝ (e *ℝ (e *ℝ (e *ℝ e)))
  8e-lt-e4 = subst (λ x → x <ℝ (e *ℝ (e *ℝ (e *ℝ e)))) (sym (*-comm-ℝ (natℝ 8) e)) eight-e-lt-e4

-- exp(natℝ 2) = e·e（exp-add + e-def）
exp-nat2 : exp (natℝ 2) ≡ e *ℝ e
exp-nat2 =
  trans (cong exp (natℝ-+ 1 1))
        (trans (exp-add (natℝ 1) (natℝ 1))
               (cong₂ _*ℝ_ exp-nat1 exp-nat1))
  where
  exp-nat1 : exp (natℝ 1) ≡ e
  exp-nat1 = trans (cong exp natℝ-one) (sym e-def)

-- exp(natℝ 4) = (e·e)·(e·e)
exp-nat4 : exp (natℝ 4) ≡ (e *ℝ e) *ℝ (e *ℝ e)
exp-nat4 =
  trans (cong exp (natℝ-+ 2 2))
        (trans (exp-add (natℝ 2) (natℝ 2))
               (cong₂ _*ℝ_ exp-nat2 exp-nat2))

-- exp(natℝ 4) = e·(e·(e·e))（结合律重整）
exp-nat4-e4 : exp (natℝ 4) ≡ (e *ℝ (e *ℝ (e *ℝ e)))
exp-nat4-e4 = trans exp-nat4 (*-assoc-ℝ e e (e *ℝ e))

-- 8 < exp 4（8 < 16 < e⁴）
exp-4-gt-8 : natℝ 8 <ℝ exp (natℝ 4)
exp-4-gt-8 =
  subst (λ x → natℝ 8 <ℝ x) (sym exp-nat4-e4)
        (trans-<ℝ (natℝ-<-embed 8-lt-16) e4-gt-16)
  where
  8-lt-16 : 8 <ℕ 16
  8-lt-16 = <-trans (<-suc 8) (<-trans (<-suc 9) (<-trans (<-suc 10) (<-trans (<-suc 11) (<-trans (<-suc 12) (<-trans (<-suc 13) (<-trans (<-suc 14) (<-suc 15)))))))

-- exp(-4) = 1/exp 4 < 1/8（倒数单调）
exp-neg-4-lt-1-8 : exp (negℝ (natℝ 4)) <ℝ (oneℝ /ℝ natℝ 8)
exp-neg-4-lt-1-8 =
  subst (λ x → x <ℝ (oneℝ /ℝ natℝ 8)) (sym (exp-recip (natℝ 4)))
        (recip-mono-ℝ (natℝ-pos-embed z<s) exp-4-gt-8)

-- 1/8 < 13/100（交叉：100 < 104）
one-8-lt-13-100 : (oneℝ /ℝ natℝ 8) <ℝ (natℝ 13 /ℝ natℝ 100)
one-8-lt-13-100 =
  subst (λ x → x <ℝ (natℝ 13 /ℝ natℝ 100)) (sym one-over-8)
        (subst (λ y → (natℝ 100 /ℝ natℝ 800) <ℝ y) (sym thirteen-over-100)
               (/-lt-same-den-ℝ {natℝ 100} {natℝ 104} {natℝ 800} (natℝ-<-embed 100-lt-104)))
  where
  -- 1/8 = 100/800（交叉：1·800 = 100·8）
  one-over-8 : (oneℝ /ℝ natℝ 8) ≡ (natℝ 100 /ℝ natℝ 800)
  one-over-8 = /-cross-ℝ (trans (one-mul-ℝ (natℝ 800)) (natℝ-* 100 8))
  -- 13/100 = 104/800
  thirteen-over-100 : (natℝ 13 /ℝ natℝ 100) ≡ (natℝ 104 /ℝ natℝ 800)
  thirteen-over-100 = /-cross-ℝ (trans (sym (natℝ-* 13 800)) (trans (cong natℝ refl) (natℝ-* 104 100)))
  100-lt-104 : 100 <ℕ 104
  100-lt-104 = <-trans (<-suc 100) (<-trans (<-suc 101) (<-trans (<-suc 102) (<-suc 103)))

-- exp(-4) < 13/100（1/8 < 13/100 传递）
exp-neg-4-lt-13-100 : exp (negℝ (natℝ 4)) <ℝ (natℝ 13 /ℝ natℝ 100)
exp-neg-4-lt-13-100 = trans-<ℝ exp-neg-4-lt-1-8 one-8-lt-13-100

-- 同分母分数加法：(a/c) + (b/c) = (a+b)/c（经 /-add-ℝ 通分 + 交叉相乘）
/-add-same-ℝ : (a b c : ℝ) → (a /ℝ c) +ℝ (b /ℝ c) ≡ ((a +ℝ b) /ℝ c)
/-add-same-ℝ a b c =
  trans (/-add-ℝ a b c c)
        (/-cross-ℝ cross)
  where
  -- ((a·c)+(b·c))·c ≡ (a+b)·(c·c)（交换 + 分配律 + 结合律）
  cross : (((a *ℝ c) +ℝ (b *ℝ c)) *ℝ c) ≡ ((a +ℝ b) *ℝ (c *ℝ c))
  cross =
    trans (*-comm-ℝ ((a *ℝ c) +ℝ (b *ℝ c)) c)
          (trans (distrib-ℝ c (a *ℝ c) (b *ℝ c))
                 (trans (cong₂ _+ℝ_ c-mul-ac c-mul-bc)
                        (trans (cong₂ _+ℝ_ (*-comm-ℝ a (c *ℝ c)) (*-comm-ℝ b (c *ℝ c)))
                               (trans (sym (distrib-ℝ (c *ℝ c) a b))
                                      (*-comm-ℝ (c *ℝ c) (a +ℝ b))))))
    where
    -- c·(a·c) ≡ a·(c·c)
    c-mul-ac : (c *ℝ (a *ℝ c)) ≡ (a *ℝ (c *ℝ c))
    c-mul-ac =
      trans (sym (*-assoc-ℝ c a c))
            (trans (cong (λ x → x *ℝ c) (*-comm-ℝ c a))
                   (*-assoc-ℝ a c c))
    -- c·(b·c) ≡ b·(c·c)
    c-mul-bc : (c *ℝ (b *ℝ c)) ≡ (b *ℝ (c *ℝ c))
    c-mul-bc =
      trans (sym (*-assoc-ℝ c b c))
            (trans (cong (λ x → x *ℝ c) (*-comm-ℝ c b))
                   (*-assoc-ℝ b c c))

-- log 加性（由 exp 加性 + 互逆推出）
log-mul : (a b : ℝ) → log (a *ℝ b) ≡ log a +ℝ log b
log-mul a b =
  trans (cong log (sym (trans (exp-add (log a) (log b))
                              (cong₂ _*ℝ_ (exp-log a) (exp-log b)))))
        (log-exp (log a +ℝ log b))

-- a² = a·a（rpow-exp + 2=1+1 + 分配律 + log 加性）
rpow-2 : (a : ℝ) → (a ^-ℝ (natℝ 2)) ≡ (a *ℝ a)
rpow-2 a =
  trans (rpow-exp a (natℝ 2))
        (trans (cong exp (cong (λ x → x *ℝ log a) (natℝ-+ 1 1)))
               (trans (cong exp (trans (*-comm-ℝ (natℝ 1 +ℝ natℝ 1) (log a))
                                       (trans (distrib-ℝ (log a) (natℝ 1) (natℝ 1))
                                              (cong₂ _+ℝ_ (x-mul-one (log a)) (x-mul-one (log a))))))
                      (trans (cong exp (sym (log-mul a a)))
                             (exp-log (a *ℝ a)))))
  where
  -- x·1 = x（natℝ 1 → oneℝ + 单位元）
  x-mul-one : (x : ℝ) → (x *ℝ natℝ 1) ≡ x
  x-mul-one x = trans (cong₂ _*ℝ_ refl natℝ-one) (*-ident-ℝ x)

-- log 1 = 0
log-one : log oneℝ ≡ zeroℝ
log-one = trans (cong log (sym exp-zero)) (log-exp zeroℝ)

-- 1^b = 1（rpow-exp + log 1 = 0 + 零吸收 + exp 0 = 1）
rpow-one-base : (b : ℝ) → (oneℝ ^-ℝ b) ≡ oneℝ
rpow-one-base b =
  trans (rpow-exp oneℝ b)
        (trans (cong (λ x → exp (b *ℝ x)) log-one)
               (trans (cong exp (*-zero-ℝ b)) exp-zero))

-- x + (x + (x + x)) = 4·x
four-x : (x : ℝ) → x +ℝ (x +ℝ (x +ℝ x)) ≡ (natℝ 4) *ℝ x
four-x x =
  trans (sym (+-assoc-ℝ x x (x +ℝ x)))
        (trans (cong₂ _+ℝ_ (dbl x) (dbl x))
               (trans (dbl (natℝ 2 *ℝ x))
                      (trans (sym (*-assoc-ℝ (natℝ 2) (natℝ 2) x))
                             (cong (λ y → y *ℝ x) (sym (natℝ-* 2 2))))))

-- log 16 = 4·log 2
log-16 : log (natℝ 16) ≡ natℝ 4 *ℝ log (natℝ 2)
log-16 =
  trans (cong log (natℝ-* 2 8))
        (trans (log-mul (natℝ 2) (natℝ 8))
               (trans (cong (λ x → log (natℝ 2) +ℝ x) log-8)
                      (four-x (log (natℝ 2)))))
  where
  log-8 : log (natℝ 8) ≡ log (natℝ 2) +ℝ (log (natℝ 2) +ℝ log (natℝ 2))
  log-8 =
    trans (cong log (natℝ-* 2 4))
          (trans (log-mul (natℝ 2) (natℝ 4))
                 (cong (λ x → log (natℝ 2) +ℝ x) log-4))
    where
    log-4 : log (natℝ 4) ≡ log (natℝ 2) +ℝ log (natℝ 2)
    log-4 = trans (cong log (natℝ-* 2 2)) (log-mul (natℝ 2) (natℝ 2))

-- log(1/x) = -log x（由 log 加性 + log 1 = 0 + 负唯一性）
log-recip : (x : ℝ) → log (oneℝ /ℝ x) ≡ negℝ (log x)
log-recip x =
  neg-unique-ℝ
    (trans (sym (log-mul x (oneℝ /ℝ x)))
           (trans (sym (cong log (sym (*-/cancel-ℝ x oneℝ)))) (log-one)))

-- 15 = 16·(15/16) ⟹ ln15 = 4ln2 + ln(15/16)
ln15-decomp : ln15 ≡ (natℝ 4 *ℝ log (natℝ 2)) +ℝ log (natℝ 15 /ℝ natℝ 16)
ln15-decomp =
  trans (cong log (sym (*-/cancel-ℝ (natℝ 16) (natℝ 15))))
        (trans (log-mul (natℝ 16) (natℝ 15 /ℝ natℝ 16))
               (cong (λ x → x +ℝ log (natℝ 15 /ℝ natℝ 16)) (log-16)))

-- 4·log2 < 4·(69317/100000)
four-log2-lt : (natℝ 4 *ℝ log (natℝ 2)) <ℝ (natℝ 4 *ℝ (natℝ 69317 /ℝ natℝ 100000))
four-log2-lt = *-pos-mono-ℝ {c = natℝ 4} (natℝ-pos-embed z<s) (ln2-lt)

-- 1/(16/15) = 15/16
one-over-1615 : oneℝ /ℝ (natℝ 16 /ℝ natℝ 15) ≡ natℝ 15 /ℝ natℝ 16
one-over-1615 =
  /-cross-ℝ (trans (trans (*-comm-ℝ oneℝ (natℝ 16)) (*-ident-ℝ (natℝ 16)))
                   (sym (*-/cancel-ℝ (natℝ 15) (natℝ 16))))

-- log(15/16) = -log(16/15)
log-1516 : log (natℝ 15 /ℝ natℝ 16) ≡ negℝ (log (natℝ 16 /ℝ natℝ 15))
log-1516 =
  subst (λ x → log x ≡ negℝ (log (natℝ 16 /ℝ natℝ 15))) (one-over-1615)
        (log-recip (natℝ 16 /ℝ natℝ 15))

-- log(15/16) < -29/450
log1516-lt : log (natℝ 15 /ℝ natℝ 16) <ℝ negℝ (natℝ 29 /ℝ natℝ 450)
log1516-lt =
  subst (λ x → x <ℝ negℝ (natℝ 29 /ℝ natℝ 450)) (sym (log-1516))
        (neg-<-ℝ (ln1615-lb))

-- ==================================================================
-- §2 纯数学不等式链
-- ==================================================================

-- ln 15 < 65/24（**T3 阶段 3 闭合 2026-07-31**：ln15 = 4ln2 + ln(15/16)
-- < 4·0.69317 - 29/450 < 65/24，不再是 postulate；
-- log 代数部分全部可证，纯有理比较 ln15-arith-ax 已于 2026-08-05 闭合为定理（§2d））
ln15-lt-65-24 : ln15 <ℝ sixtyfive-over-24
ln15-lt-65-24 =
  subst (λ x → x <ℝ sixtyfive-over-24) (sym (ln15-decomp))
    (trans-<ℝ
      (trans-<ℝ (lt-+-mono-l-ℝ (four-log2-lt))
                (lt-+-mono-r-ℝ (log1516-lt)))
      ln15-arith-ax)

-- 65/24 < e（**T3 阶段 2 闭合 2026-07-31**：partial-e 4 ≡ 65/24 计算证明
-- + exp 级数截断公理 exp-partial-< 4；对应 Lean Real.exp_one_gt_d9）
sixtyfive-over-24-lt-e : sixtyfive-over-24 <ℝ e
sixtyfive-over-24-lt-e =
  subst (λ y → sixtyfive-over-24 <ℝ y) (sym e-def)
    (subst (λ x → x <ℝ exp oneℝ) partial-e-4-value (exp-partial-< 4))

-- e⁻¹ 的改进上界：e⁻¹ < 37/100（对应 Lean: exp_neg_one_lt_37_100）
-- （**T3 阶段 4 闭合 2026-07-31**：e⁻¹ = 1/e < 1/(100/37) = 37/100 [倒数单调]
--   ⟸ 100/37 < 65/24 < e [B4 链 + 交叉相乘 2400 < 2405]；从 IFSFractal 迁入）
exp-neg-one-lt-37-100 : exp neg-oneℝ <ℝ (natℝ 37 /ℝ natℝ 100)
exp-neg-one-lt-37-100 =
  subst (λ x → x <ℝ (natℝ 37 /ℝ natℝ 100)) (sym (exp-neg-one-e))
    (subst (λ y → (oneℝ /ℝ e) <ℝ y) (one-over-100-37)
           (recip-mono-ℝ pos-100-37 100-37-lt-e))
  where
  -- e⁻¹·e = e⁰ = 1
  exp-neg1-exp1 : (exp (negℝ oneℝ) *ℝ exp oneℝ) ≡ oneℝ
  exp-neg1-exp1 =
    trans (sym (exp-add (negℝ oneℝ) oneℝ))
          (trans (cong exp (trans (+-comm-ℝ (negℝ oneℝ) oneℝ) (+-inv-ℝ oneℝ)))
                 (exp-zero))
  -- 1/e = e⁻¹
  one-over-e : oneℝ /ℝ exp oneℝ ≡ exp (negℝ oneℝ)
  one-over-e =
    trans (/-cross-ℝ (trans (*-ident-ℝ oneℝ) (sym exp-neg1-exp1)))
          (div-one-ℝ (exp (negℝ oneℝ)))
  -- e⁻¹ = 1/e
  exp-neg-one-e : exp neg-oneℝ ≡ oneℝ /ℝ e
  exp-neg-one-e =
    trans (cong exp neg-one-ℝ-def)
          (trans (sym one-over-e)
                 (cong (λ x → oneℝ /ℝ x) (sym e-def)))
  -- 1/(100/37) = 37/100
  one-over-100-37 : oneℝ /ℝ (natℝ 100 /ℝ natℝ 37) ≡ natℝ 37 /ℝ natℝ 100
  one-over-100-37 =
    /-cross-ℝ (trans (one-mul-ℝ (natℝ 100)) (sym (*-/cancel-ℝ (natℝ 37) (natℝ 100))))
  -- 0 < 100/37
  pos-100-37 : zeroℝ <ℝ (natℝ 100 /ℝ natℝ 37)
  pos-100-37 = /-pos-ℝ (natℝ-pos-embed z<s) (natℝ-pos-embed z<s)
  c100 : (natℝ 100 /ℝ natℝ 37) ≡ (natℝ 2400 /ℝ natℝ 888)
  c100 = /-cross-ℝ (trans (sym (natℝ-* 100 888)) (trans (cong natℝ refl) (natℝ-* 2400 37)))
  c65 : (natℝ 65 /ℝ natℝ 24) ≡ (natℝ 2405 /ℝ natℝ 888)
  c65 = /-cross-ℝ (trans (sym (natℝ-* 65 888)) (trans (cong natℝ refl) (natℝ-* 2405 24)))
  2400-lt-2405 : 2400 <ℕ 2405
  2400-lt-2405 = <-trans (<-suc 2400) (<-trans (<-suc 2401) (<-trans (<-suc 2402) (<-trans (<-suc 2403) (<-suc 2404))))
  -- 100/37 < 65/24（交叉相乘：100·24 = 2400 < 2405 = 65·37）
  100-37-lt-65-24 : (natℝ 100 /ℝ natℝ 37) <ℝ (natℝ 65 /ℝ natℝ 24)
  100-37-lt-65-24 =
    subst (λ x → x <ℝ (natℝ 65 /ℝ natℝ 24)) (sym c100)
      (subst (λ y → (natℝ 2400 /ℝ natℝ 888) <ℝ y) (sym c65)
             (/-lt-same-den-ℝ {natℝ 2400} {natℝ 2405} {natℝ 888} (natℝ-<-embed 2400-lt-2405)))
  -- 100/37 < 65/24 < e
  100-37-lt-e : (natℝ 100 /ℝ natℝ 37) <ℝ e
  100-37-lt-e = trans-<ℝ 100-37-lt-65-24 sixtyfive-over-24-lt-e

-- exp(-d²) < 37/100（d ≥ 1 ⟹ d² ≥ 1 ⟹ -d² ≤ -1 < 37/100）
exp-neg-d2-lt-37-100 : (d : ℝ) → natℝ 1 ≤ℝ d
  → exp (negℝ (d *ℝ d)) <ℝ (natℝ 37 /ℝ natℝ 100)
exp-neg-d2-lt-37-100 d h =
  ≤-lt-trans-ℝ (exp-mono-≤ (subst (λ z → negℝ (d *ℝ d) ≤ℝ negℝ z) natℝ-one (neg-≤-ℝ (d-sq-ge-1 h))))
               (subst (λ x → x <ℝ (natℝ 37 /ℝ natℝ 100)) (cong exp neg-one-ℝ-def)
                      exp-neg-one-lt-37-100)

-- exp(-d(3+d)) < 13/100（d ≥ 1 ⟹ d(3+d) ≥ 4 ⟹ -d(3+d) ≤ -4 < 13/100）
exp-neg-d3d-lt-13-100 : (d : ℝ) → natℝ 1 ≤ℝ d
  → exp (negℝ (d *ℝ (natℝ 3 +ℝ d))) <ℝ (natℝ 13 /ℝ natℝ 100)
exp-neg-d3d-lt-13-100 d h =
  ≤-lt-trans-ℝ (exp-mono-≤ (neg-≤-ℝ (d-3d-ge-4 h))) exp-neg-4-lt-13-100

-- e < 3（**T3 阶段 2 闭合 2026-07-31**：统一上界 partial-e n < 67/24
-- + exp-least-ub + 67/24 < 3，不再是 postulate）
e-lt-3 : e <ℝ (natℝ 3)
e-lt-3 =
  subst (λ x → x <ℝ natℝ 3) (sym e-def)
    (≤-lt-trans-ℝ
      (exp-least-ub (natℝ 67 /ℝ natℝ 24) (λ n → <-≤-ℝ (partial-e-lt-67-24 n)))
      sixtyseven-over-24-lt-3)

-- 纯数学不等式链：ln 15 < 65/24 < e < 3
inequality-chain-pure-math :
  (ln15 <ℝ sixtyfive-over-24) × (sixtyfive-over-24 <ℝ e) × (e <ℝ natℝ 3)
inequality-chain-pure-math = ln15-lt-65-24 , sixtyfive-over-24-lt-e , e-lt-3

-- 维数间隙：ln 15 < 3（由链传递性）
dimension-gap : ln15 <ℝ natℝ 3
dimension-gap = trans-<ℝ ln15-lt-65-24 (trans-<ℝ sixtyfive-over-24-lt-e e-lt-3)

-- ==================================================================
-- §3 Moran 方程
-- ==================================================================

-- 有效分支数 B = N_active × N_total = 3 × 5 = 15
-- （对应 SpCategory.agda 中的 layerPair-count = 15）
N-active : ℕ
N-active = 3

N-total : ℕ
N-total = 5

B : ℕ
B = 15

-- B = 15
B-eq-15 : B ≡ 15
B-eq-15 = refl

-- 均匀收缩率 r = e⁻¹
r : ℝ
r = exp neg-oneℝ

-- 条件定理：若 B = 15 且 r = e⁻¹，则 B · r^{ln 15} = 1
-- 对应 Lean: dH_from_branching
-- （**T3 阶段 4 闭合 2026-07-31**：(e⁻¹)^{ln15} = e^{ln15·log(e⁻¹)} [rpow-exp]
--   = e^{-ln15} [log(e⁻¹) = -1] = 1/15 [exp-recip + exp-log]，
--   15·(1/15) = 1 [*-/cancel]；不再是 postulate）
dH-from-branching : (natℝ B) *ℝ (r ^-ℝ ln15) ≡ oneℝ
dH-from-branching =
  trans (cong (λ x → natℝ B *ℝ x) r-pow)
        (trans (cong (λ x → natℝ B *ℝ x) (exp-recip ln15))
               (trans (cong (λ x → natℝ B *ℝ (oneℝ /ℝ x)) (exp-log (natℝ 15)))
                      (*-/cancel-ℝ (natℝ 15) oneℝ)))
  where
  -- log(e⁻¹) = -1
  log-exp-neg-one : log (exp neg-oneℝ) ≡ neg-oneℝ
  log-exp-neg-one =
    trans (cong log (cong exp (neg-one-ℝ-def)))
          (trans (log-exp (negℝ oneℝ)) (sym neg-one-ℝ-def))
  -- ln15·(-1) = -ln15
  ln15-neg-one : ln15 *ℝ neg-oneℝ ≡ negℝ ln15
  ln15-neg-one =
    trans (cong₂ _*ℝ_ refl (neg-one-ℝ-def))
          (trans (*-comm-ℝ ln15 (negℝ oneℝ)) (neg-one-mul ln15))
  -- (e⁻¹)^{ln15} = e^{ln15·log(e⁻¹)}
  r-pow : r ^-ℝ ln15 ≡ exp (negℝ ln15)
  r-pow =
    trans (rpow-exp r ln15)
          (trans (cong (λ x → exp (ln15 *ℝ x)) log-exp-neg-one)
                 (cong exp ln15-neg-one))

-- Moran 方程解的存在唯一性（一般 B, r）
-- 对应 Lean: moran_solution_iff
-- （**T3 阶段 4 闭合 2026-07-31**：B·r^x = 1 ⟹ exp(x·log r) = 1/B [rpow-exp + *-recip-impl]
--   ⟹ x·log r = log(1/B) = -log B [log-exp + log-recip] ⟹ x = (-log B)/log r [*-div-impl]
--   = log B/(-log r) [交叉相乘 + neg-mul-ℝ] = log B/log(1/r) [log-recip]；不再是 postulate）
moran-solution-iff : {B r x : ℝ} → (natℝ 1 <ℝ B) → (zeroℝ <ℝ r) → (r <ℝ natℝ 1)
  → ((B *ℝ (r ^-ℝ x)) ≡ oneℝ) → (x ≡ (log B /ℝ log (natℝ 1 /ℝ r)))
moran-solution-iff {B} {r} {x} h1 h2 h3 h =
  trans (*-div-impl x-logr)
        (trans (/-cross-ℝ cross)
               (cong (λ u → log B /ℝ u) (sym log-nat-1-over-r)))
  where
  -- B·r^x = 1 ⟹ exp(x·log r) = 1/B
  exp-x-logr-1B : exp (x *ℝ log r) ≡ oneℝ /ℝ B
  exp-x-logr-1B =
    *-recip-impl {a = B} {b = exp (x *ℝ log r)}
      (trans (sym (cong (λ y → B *ℝ y) (rpow-exp r x))) h)
  -- exp(x·log r) = 1/B ⟹ x·log r = -log B（log 两边）
  x-logr : x *ℝ log r ≡ negℝ (log B)
  x-logr =
    trans (sym (log-exp (x *ℝ log r)))
          (trans (cong log (exp-x-logr-1B)) (log-recip B))
  -- log(1/r) = -log r（natℝ 1 形式）
  log-nat-1-over-r : log (natℝ 1 /ℝ r) ≡ negℝ (log r)
  log-nat-1-over-r = trans (cong (λ u → log (u /ℝ r)) natℝ-one) (log-recip r)
  -- log B·(-log r) = -(log B·log r)
  neg-mul-comm : (log B) *ℝ (negℝ (log r)) ≡ negℝ ((log B) *ℝ (log r))
  neg-mul-comm =
    trans (*-comm-ℝ (log B) (negℝ (log r)))
          (trans (neg-mul-ℝ (log r) (log B))
                 (cong negℝ (*-comm-ℝ (log r) (log B))))
  -- (-log B)·(-log r) = log B·log r
  cross : (negℝ (log B)) *ℝ (negℝ (log r)) ≡ (log B) *ℝ (log r)
  cross =
    trans (neg-mul-ℝ (log B) (negℝ (log r)))
          (trans (cong negℝ neg-mul-comm) (neg-neg (log B *ℝ log r)))

-- d_H = ln 15 的唯一解刻画：15 · (e⁻¹)^x = 1 ⟺ x = ln 15
-- 对应 Lean: dH_moran_solution_unique
-- （**T3 阶段 4 闭合 2026-07-31**：15·(e⁻¹)^x = 1 ⟹ e^{-x} = 1/15 [rpow-exp + *-recip-impl]
--   = e^{-ln15} [exp-recip + exp-log] ⟹ -x = -ln15 [exp-inj] ⟹ x = ln15 [neg-neg]；
--   exp-inj 为定义性公理，记入账目开放项；不再是 postulate）
dH-moran-solution-unique : {x : ℝ} → ((natℝ 15) *ℝ ((exp neg-oneℝ) ^-ℝ x) ≡ oneℝ)
  → (x ≡ ln15)
dH-moran-solution-unique {x} h =
  trans (sym (neg-neg x)) (trans (cong negℝ neg-eq) (neg-neg ln15))
  where
  -- log(e⁻¹) = -1
  log-exp-neg-one : log (exp neg-oneℝ) ≡ neg-oneℝ
  log-exp-neg-one =
    trans (cong log (cong exp (neg-one-ℝ-def)))
          (trans (log-exp (negℝ oneℝ)) (sym neg-one-ℝ-def))
  -- x·(-1) = -x
  x-neg-one : x *ℝ neg-oneℝ ≡ negℝ x
  x-neg-one =
    trans (cong₂ _*ℝ_ refl (neg-one-ℝ-def))
          (trans (*-comm-ℝ x (negℝ oneℝ)) (neg-one-mul x))
  -- (e⁻¹)^x = e^{-x}
  r-pow-x : (exp neg-oneℝ) ^-ℝ x ≡ exp (negℝ x)
  r-pow-x =
    trans (rpow-exp (exp neg-oneℝ) x)
          (trans (cong (λ u → exp (x *ℝ u)) log-exp-neg-one)
                 (cong exp x-neg-one))
  -- 15·(e⁻¹)^x = 1 ⟹ e^{-x} = 1/15
  e-neg-x : exp (negℝ x) ≡ oneℝ /ℝ natℝ 15
  e-neg-x =
    *-recip-impl {a = natℝ 15} {b = exp (negℝ x)}
      (trans (sym (cong (λ y → natℝ 15 *ℝ y) r-pow-x)) h)
  -- e^{-ln15} = 1/15
  e-neg-ln15 : exp (negℝ ln15) ≡ oneℝ /ℝ natℝ 15
  e-neg-ln15 = trans (exp-recip ln15) (cong (λ y → oneℝ /ℝ y) (exp-log (natℝ 15)))
  -- exp(-x) = exp(-ln15) ⟹ -x = -ln15
  neg-eq : negℝ x ≡ negℝ ln15
  neg-eq = exp-inj (trans e-neg-x (sym e-neg-ln15))

-- ==================================================================
-- §4 两级粘合递归不动点
-- ==================================================================

-- 分配展开：B·(B-1) + ρ·B = B·((B-1) + ρ)（ρ·B 交换 + 反分配律）
B-mul-sum : (B ρ : ℝ) → ((B *ℝ (B -ℝ natℝ 1)) +ℝ (ρ *ℝ B)) ≡ (B *ℝ ((B -ℝ natℝ 1) +ℝ ρ))
B-mul-sum B ρ =
  trans (cong₂ _+ℝ_ refl (*-comm-ℝ ρ B))
        (sym (distrib-ℝ B (B -ℝ natℝ 1) ρ))

-- r^{2d} = (r^d)·(r^d)（rpow-pow + rpow-2 + 乘法交换）
rpow-2d-sq : (r d : ℝ) → (r ^-ℝ (natℝ 2 *ℝ d)) ≡ ((r ^-ℝ d) *ℝ (r ^-ℝ d))
rpow-2d-sq r d =
  trans (cong (λ x → r ^-ℝ x) (*-comm-ℝ (natℝ 2) d))
        (trans (sym (rpow-pow r d (natℝ 2)))
               (rpow-2 (r ^-ℝ d)))

-- M = x·(B-1+ρ) + 1 恒正：0 < x ⟹ 0 < B-1+ρ ⟹ 0 < M
glued-M-pos : {B ρ x : ℝ} → zeroℝ <ℝ x → zeroℝ <ℝ (B -ℝ natℝ 1) → zeroℝ ≤ℝ ρ
  → zeroℝ <ℝ ((x *ℝ ((B -ℝ natℝ 1) +ℝ ρ)) +ℝ oneℝ)
glued-M-pos {B} {ρ} {x} hx hB hρ = trans-<ℝ xC-pos (add-pos-ℝ one-lt)
  where
  C : ℝ
  C = (B -ℝ natℝ 1) +ℝ ρ
  -- 0 < C（B-1 ≤ B-1+0 ≤ B-1+ρ，0 < B-1 ≤ C）
  C-pos : zeroℝ <ℝ C
  C-pos =
    lt-≤-trans-ℝ hB
                  (subst (λ u → u ≤ℝ C) (+-ident-ℝ (B -ℝ natℝ 1))
                         (≤-+-mono-ℝ (refl-≤ℝ {x = B -ℝ natℝ 1}) hρ))
  -- 0 < x·C
  xC-pos : zeroℝ <ℝ (x *ℝ C)
  xC-pos = lt-*-pos-ℝ hx C-pos
  one-lt : zeroℝ <ℝ oneℝ
  one-lt = zero-lt-one-ℝ

-- -(x+y) = (-x)+(-y)（取负分配，由负唯一性）
neg-add-ℝ : (x y : ℝ) → negℝ (x +ℝ y) ≡ (negℝ x) +ℝ (negℝ y)
neg-add-ℝ x y =
  sym (neg-unique-ℝ {a = x +ℝ y} {b = (negℝ x) +ℝ (negℝ y)}
        (zero-sum x y))

-- B - (B-1+ρ) = 1 - ρ（展开减法 + 取负分配 + 抵消）
B-sub-C : (B ρ : ℝ) → (B -ℝ ((B -ℝ natℝ 1) +ℝ ρ)) ≡ (natℝ 1 -ℝ ρ)
B-sub-C B ρ =
  trans (sub-ℝ-def B ((B -ℝ natℝ 1) +ℝ ρ))
        (trans (cong (λ x → B +ℝ x) (neg-add-ℝ (B -ℝ natℝ 1) ρ))
               (trans (sym (+-assoc-ℝ B (negℝ (B -ℝ natℝ 1)) (negℝ ρ)))
                      (trans (cong₂ _+ℝ_ core refl)
                             (sym (sub-ℝ-def (natℝ 1) ρ)))))
  where
  -- 核心：B + (-(B-1)) = 1
  core : (B +ℝ (negℝ (B -ℝ natℝ 1))) ≡ natℝ 1
  core =
    trans (cong (λ x → B +ℝ x) (trans (cong negℝ (sub-ℝ-def B (natℝ 1)))
                                      (neg-add-ℝ B (negℝ (natℝ 1)))))
          (trans (sym (+-assoc-ℝ B (negℝ B) (negℝ (negℝ (natℝ 1)))))
                 (trans (cong₂ _+ℝ_ (+-inv-ℝ B) refl)
                        (trans (zero-add-ℝ (negℝ (negℝ (natℝ 1))))
                               (neg-neg (natℝ 1)))))

-- (a-1)·(b+1) = a·b + a - b - 1（展开）
mul-sub-add : (a b : ℝ) → ((a -ℝ oneℝ) *ℝ (b +ℝ oneℝ))
  ≡ (((a *ℝ b) +ℝ a) -ℝ b) -ℝ oneℝ
mul-sub-add a b =
  trans (distrib-ℝ (a -ℝ oneℝ) b oneℝ)
        (trans (cong₂ _+ℝ_ sub-distrib (*-ident-ℝ (a -ℝ oneℝ)))
               (add-assoc-rev))
  where
  -- (a-1)·b = a·b - b
  sub-distrib : ((a -ℝ oneℝ) *ℝ b) ≡ ((a *ℝ b) -ℝ b)
  sub-distrib =
    trans (cong (λ x → x *ℝ b) (sub-ℝ-def a oneℝ))
          (trans (*-comm-ℝ (a +ℝ negℝ oneℝ) b)
                 (trans (distrib-ℝ b a (negℝ oneℝ))
                        (trans (cong₂ _+ℝ_ (*-comm-ℝ b a) (trans (*-comm-ℝ b (negℝ oneℝ)) (neg-one-mul b)))
                               (sym (sub-ℝ-def (a *ℝ b) b)))))
  -- (a·b - b) + (a-1) = (a·b + a) - b - 1（sub-ℝ-def 展开 + 重排）
  add-assoc-rev : ((a *ℝ b) -ℝ b) +ℝ (a -ℝ oneℝ) ≡ (((a *ℝ b) +ℝ a) -ℝ b) -ℝ oneℝ
  add-assoc-rev =
    trans (cong₂ _+ℝ_ (sub-ℝ-def (a *ℝ b) b) (sub-ℝ-def a oneℝ))
          (trans (swap-pair (a *ℝ b) (negℝ b) a (negℝ oneℝ))
                 (trans (sym (+-assoc-ℝ ((a *ℝ b) +ℝ a) (negℝ b) (negℝ oneℝ)))
                        (sym (trans (sub-ℝ-def (((a *ℝ b) +ℝ a) -ℝ b) oneℝ)
                                    (cong (λ x → x +ℝ negℝ oneℝ) (sub-ℝ-def ((a *ℝ b) +ℝ a) b))))))

-- (a-c)·b = a·b - c·b（sub-ℝ-def + 分配律）
sub-mul-distrib : (a c b : ℝ) → ((a -ℝ c) *ℝ b) ≡ ((a *ℝ b) -ℝ (c *ℝ b))
sub-mul-distrib a c b =
  trans (cong (λ x → x *ℝ b) (sub-ℝ-def a c))
        (trans (*-comm-ℝ (a +ℝ negℝ c) b)
               (trans (distrib-ℝ b a (negℝ c))
                      (trans (cong₂ _+ℝ_ (*-comm-ℝ b a)
                                       (trans (*-comm-ℝ b (negℝ c)) (neg-mul-ℝ c b)))
                             (sym (sub-ℝ-def (a *ℝ b) (c *ℝ b))))))

-- A + (B-C) = (A+B) - C（结合律 + 减法定义）
add-sub-assoc : (A B C : ℝ) → (A +ℝ (B -ℝ C)) ≡ ((A +ℝ B) -ℝ C)
add-sub-assoc A B C =
  trans (cong (λ x → A +ℝ x) (sub-ℝ-def B C))
        (trans (sym (+-assoc-ℝ A B (negℝ C)))
               (sym (sub-ℝ-def (A +ℝ B) C)))

-- B·(B-1+ρ)·(x·x) 中 B·C 换回 B(B-1)+ρB（B-mul-sum 反向）
BC-replace : (B ρ x : ℝ) → ((B *ℝ ((B -ℝ natℝ 1) +ℝ ρ)) *ℝ (x *ℝ x))
  ≡ (((B *ℝ (B -ℝ natℝ 1)) +ℝ (ρ *ℝ B)) *ℝ (x *ℝ x))
BC-replace B ρ x = cong (λ u → u *ℝ (x *ℝ x)) (sym (B-mul-sum B ρ))

-- 因式分解：(Bx-1)·(x(B-1+ρ)+1) = (B(B-1)+ρB)x² + (1-ρ)x - 1
-- 链：mul-sub-add ⟹ ((Bx·xC + Bx) - xC) - 1
--   ⟹ ((B·C)x² + Bx - xC) - 1 [Bx-mul-xC]
--   ⟹ ((B·C)x² + (B-C)x) - 1 [sub-mul-distrib 反向 + add-sub-assoc]
--   ⟹ ((B·C)x² + (1-ρ)x) - 1 [B-sub-C]
--   ⟹ ((B(B-1)+ρB)x² + (1-ρ)x) - 1 [BC-replace]
factor-glued : (B ρ x : ℝ)
  → ((((B *ℝ x) -ℝ oneℝ) *ℝ ((x *ℝ ((B -ℝ natℝ 1) +ℝ ρ)) +ℝ oneℝ)))
      ≡ ((((B *ℝ (B -ℝ natℝ 1)) +ℝ (ρ *ℝ B)) *ℝ (x *ℝ x)) +ℝ ((natℝ 1 -ℝ ρ) *ℝ x)) -ℝ oneℝ
factor-glued B ρ x =
  trans (mul-sub-add (B *ℝ x) (x *ℝ C))
        (cong (λ u → u -ℝ oneℝ)
              (trans inner
                     (trans (cong₂ _+ℝ_ (BC-replace B ρ x) refl)
                            (cong₂ _+ℝ_ refl (cong (λ u → u *ℝ x) (B-sub-C B ρ))))))
  where
  C : ℝ
  C = (B -ℝ natℝ 1) +ℝ ρ
  -- Bx·(xC) = (B·C)·(x·x)（结合/交换）
  Bx-mul-xC : ((B *ℝ x) *ℝ (x *ℝ C)) ≡ ((B *ℝ C) *ℝ (x *ℝ x))
  Bx-mul-xC =
    trans (*-assoc-ℝ B x (x *ℝ C))
          (trans (cong (λ u → B *ℝ u) (sym (*-assoc-ℝ x x C)))
                 (trans (cong (λ u → B *ℝ u) (*-comm-ℝ (x *ℝ x) C))
                        (sym (*-assoc-ℝ B C (x *ℝ x)))))
  -- 主体：((Bx·xC + Bx) - xC) = (B·C·x² + (B-C)·x)
  inner : (((B *ℝ x) *ℝ (x *ℝ C)) +ℝ (B *ℝ x)) -ℝ (x *ℝ C)
        ≡ (((B *ℝ C) *ℝ (x *ℝ x)) +ℝ ((B -ℝ C) *ℝ x))
  inner =
    trans (cong (λ u → (u +ℝ (B *ℝ x)) -ℝ (x *ℝ C)) Bx-mul-xC)
          (trans (sym (add-sub-assoc ((B *ℝ C) *ℝ (x *ℝ x)) (B *ℝ x) (x *ℝ C)))
                 (trans (cong₂ _+ℝ_ refl (cong (λ u → (B *ℝ x) -ℝ u) (*-comm-ℝ x C)))
                        (trans (cong₂ _+ℝ_ refl (sym (sub-mul-distrib B C x)))
                               refl)))

-- 递归不动点定理：对任意 ρ ∈ [0,1]，
-- (1-ρ)·r^d + (B(B-1)+ρB)·r^{2d} = 1 ⟺ d = log B / log(1/r)
-- 对应 Lean: glued_recursion_fixed_point
-- （**T3 阶段 4 闭合 2026-07-31**：设 x=r^d，方程经 rpow-2d-sq 化
--   (1-ρ)x + A·x² = 1（A=B(B-1)+ρB）；factor-glued 因式分解
--   (Bx-1)·(x(B-1+ρ)+1) = A·x² + (1-ρ)x - 1 = 0；
--   M=x(B-1+ρ)+1 > 0 [x>0、B-1>0、ρ≥0]；zero-factor-ℝ ⟹ Bx-1=0
--   ⟹ B·r^d = 1 ⟹ moran-solution-iff ⟹ d = log B/log(1/r)；
--   不再是 postulate）

-- a ≡ 1 ⟹ a - 1 ≡ 0
eq-sub-zero : {a : ℝ} → a ≡ oneℝ → (a -ℝ oneℝ) ≡ zeroℝ
eq-sub-zero {a} h =
  trans (cong (λ t → t -ℝ oneℝ) h)
        (trans (sub-ℝ-def oneℝ oneℝ) (+-inv-ℝ oneℝ))

-- a - 1 ≡ 0 ⟹ a ≡ 1
sub-eq-zero : {a : ℝ} → (a -ℝ oneℝ) ≡ zeroℝ → a ≡ oneℝ
sub-eq-zero {a} h =
  trans (sym (neg-neg a))
        (trans (cong negℝ (sym (neg-unique-ℝ {a = a} {b = negℝ oneℝ}
                                    (trans (sym (sub-ℝ-def a oneℝ)) h))))
               (neg-neg oneℝ))

-- 0 < x-y（y < x 移项：y+(-y) < x+(-y)）
lt-sub-pos : {x y : ℝ} → y <ℝ x → zeroℝ <ℝ (x -ℝ y)
lt-sub-pos {x} {y} h =
  subst (λ w → zeroℝ <ℝ w) (sym (sub-ℝ-def x y))
        (subst (λ z → z <ℝ (x +ℝ negℝ y)) (+-inv-ℝ y)
               (lt-+-mono-l-ℝ h))

glued-recursion-fixed-point : {B r d ρ : ℝ}
  → (natℝ 1 <ℝ B) → (zeroℝ <ℝ r) → (r <ℝ natℝ 1) → (zeroℝ ≤ℝ ρ) → (ρ ≤ℝ natℝ 1)
  → (((natℝ 1 -ℝ ρ) *ℝ (r ^-ℝ d)) +ℝ (((B *ℝ (B -ℝ natℝ 1)) +ℝ (ρ *ℝ B)) *ℝ (r ^-ℝ (natℝ 2 *ℝ d))) ≡ oneℝ)
  → (d ≡ (log B /ℝ log (natℝ 1 /ℝ r)))
glued-recursion-fixed-point {B} {r} {d} {ρ} h1 h2 h3 h4 h5 h =
  moran-solution-iff h1 h2 h3 B-r-d-eq
  where
  x : ℝ
  x = r ^-ℝ d
  -- 0 < x（r > 0 幂正）
  x-pos : zeroℝ <ℝ x
  x-pos = rpow-pos h2
  -- 0 < B-1（1 < B）
  B-1-pos : zeroℝ <ℝ (B -ℝ natℝ 1)
  B-1-pos = lt-sub-pos {x = B} {y = natℝ 1} h1
  -- 方程化 x 形式：(1-ρ)x + A·x² ≡ 1（r^{2d} = x·x）
  h-x : (((natℝ 1 -ℝ ρ) *ℝ x) +ℝ (((B *ℝ (B -ℝ natℝ 1)) +ℝ (ρ *ℝ B)) *ℝ (x *ℝ x))) ≡ oneℝ
  h-x =
    trans (cong (λ t → ((natℝ 1 -ℝ ρ) *ℝ x) +ℝ (((B *ℝ (B -ℝ natℝ 1)) +ℝ (ρ *ℝ B)) *ℝ t))
               (sym (rpow-2d-sq r d)))
          h
  -- 交换两项：(A·x² + (1-ρ)x) ≡ 1
  h-swap : ((((B *ℝ (B -ℝ natℝ 1)) +ℝ (ρ *ℝ B)) *ℝ (x *ℝ x)) +ℝ ((natℝ 1 -ℝ ρ) *ℝ x)) ≡ oneℝ
  h-swap =
    subst (λ t → t ≡ oneℝ) (+-comm-ℝ ((natℝ 1 -ℝ ρ) *ℝ x)
                                    (((B *ℝ (B -ℝ natℝ 1)) +ℝ (ρ *ℝ B)) *ℝ (x *ℝ x)))
          h-x
  -- (Bx-1)·M ≡ 0
  prod-zero : (((B *ℝ x) -ℝ oneℝ) *ℝ ((x *ℝ ((B -ℝ natℝ 1) +ℝ ρ)) +ℝ oneℝ)) ≡ zeroℝ
  prod-zero =
    trans (factor-glued B ρ x)
          (eq-sub-zero h-swap)
  -- M > 0
  M-pos : zeroℝ <ℝ ((x *ℝ ((B -ℝ natℝ 1) +ℝ ρ)) +ℝ oneℝ)
  M-pos = glued-M-pos x-pos B-1-pos h4
  -- zero-factor：Bx-1 = 0 或 M = 0
  Bx-eq : ((B *ℝ x) -ℝ oneℝ) ≡ zeroℝ
  Bx-eq = helper (zero-factor-ℝ prod-zero)
    where
    helper : ((((B *ℝ x) -ℝ oneℝ) ≡ zeroℝ) ⊎ (((x *ℝ ((B -ℝ natℝ 1) +ℝ ρ)) +ℝ oneℝ) ≡ zeroℝ))
      → (((B *ℝ x) -ℝ oneℝ) ≡ zeroℝ)
    helper (inj₁ a) = a
    helper (inj₂ b) = ⊥-elim (irreflexive-ℝ (subst (λ t → zeroℝ <ℝ t) b M-pos))
  -- B·r^d = 1
  B-r-d-eq : (B *ℝ (r ^-ℝ d)) ≡ oneℝ
  B-r-d-eq = sub-eq-zero Bx-eq

-- 推论：B = 15、r = e⁻¹ 时，递归把维数锁定在 ln 15
-- 对应 Lean: glued_recursion_dH_eq_ln15
-- （**T3 阶段 4 闭合 2026-07-31**：glued-recursion-fixed-point 特化
--   B=natℝ 15、r=exp neg-oneℝ ⟹ d = log 15/log(1/(e⁻¹))；
--   log(1/(e⁻¹)) = -log(e⁻¹) = -(-1) = 1 [log-recip + log-exp + neg-neg]
--   ⟹ d = log 15/1 = log 15 = ln15 [div-one-ℝ]；不再是 postulate）
glued-recursion-dH-eq-ln15 : {d ρ : ℝ} → (zeroℝ ≤ℝ ρ) → (ρ ≤ℝ natℝ 1)
  → ((((natℝ 1 -ℝ ρ) *ℝ ((exp neg-oneℝ) ^-ℝ d)) +ℝ
      (((natℝ 15 *ℝ (natℝ 15 -ℝ natℝ 1)) +ℝ (ρ *ℝ natℝ 15)) *ℝ
      ((exp neg-oneℝ) ^-ℝ (natℝ 2 *ℝ d)))) ≡ oneℝ)
  → (d ≡ ln15)
glued-recursion-dH-eq-ln15 {d} {ρ} hρ0 hρ1 h =
  trans (glued-recursion-fixed-point {B = natℝ 15} {r = r} {d} {ρ}
                                     B-gt-1 r-pos r-lt-one hρ0 hρ1 h)
        (trans (cong (λ x → log (natℝ 15) /ℝ x) log-1-over-r)
               (div-one-ℝ (log (natℝ 15))))
  where
  -- 1 < 15
  B-gt-1 : natℝ 1 <ℝ natℝ 15
  B-gt-1 =
    natℝ-<-embed (<-trans (<-suc 1) (<-trans (<-suc 2) (<-trans (<-suc 3) (<-trans (<-suc 4) (<-trans (<-suc 5) (<-trans (<-suc 6) (<-trans (<-suc 7) (<-trans (<-suc 8) (<-trans (<-suc 9) (<-trans (<-suc 10) (<-trans (<-suc 11) (<-trans (<-suc 12) (<-trans (<-suc 13) (<-suc 14))))))))))))))
  -- 0 < e⁻¹
  r-pos : zeroℝ <ℝ r
  r-pos = exp-pos neg-oneℝ
  -- e⁻¹ < 1
  r-lt-one : r <ℝ natℝ 1
  r-lt-one =
    subst (λ y → exp neg-oneℝ <ℝ y) (sym natℝ-one)
      (subst (λ y → exp neg-oneℝ <ℝ y) (exp-zero)
             (exp-mono neg-one-lt-zero))
  -- log(1/(e⁻¹)) = 1（log-recip + log-exp + neg-neg）
  log-1-over-r : log (natℝ 1 /ℝ r) ≡ oneℝ
  log-1-over-r =
    trans (cong (λ x → log (x /ℝ r)) natℝ-one)
          (trans (log-recip r)
                 (trans (cong negℝ (log-exp neg-oneℝ))
                        (subst (λ x → negℝ x ≡ oneℝ) (sym neg-one-ℝ-def) (neg-neg oneℝ))))

-- ==================================================================
-- §5 唯象不等式（含 d_H 拟合值）
-- ==================================================================

-- d_H 拟合值下界：65/24 < d_H
-- （**T3 阶段 4 闭合 2026-07-31**：65/24 < 27095/10000 = d-H-fit，公共分母 6000
--   交叉 16250 < 16257 [65·6000 = 16250·24；27095·6000 = 16257·10000，经 5419/2000]；
--   不再是 postulate）
sixtyfive-over-24-lt-dH : sixtyfive-over-24 <ℝ d-H-fit
sixtyfive-over-24-lt-dH =
  subst (λ x → x <ℝ d-H-fit) (sym s65)
    (subst (λ y → (natℝ 16250 /ℝ natℝ 6000) <ℝ y) (sym s27095)
           (/-lt-same-den-ℝ {natℝ 16250} {natℝ 16257} {natℝ 6000}
                            (natℝ-<-embed 16250-lt-16257)))
  where
  -- 65/24 ≡ 16250/6000
  s65 : sixtyfive-over-24 ≡ (natℝ 16250 /ℝ natℝ 6000)
  s65 = /-cross-ℝ (trans (sym (natℝ-* 65 6000)) (trans (cong natℝ refl) (natℝ-* 16250 24)))
  -- d-H-fit ≡ 16257/6000（经 5419/2000 中间步，控制数值规模 ≤ 3.3e7）
  s27095 : d-H-fit ≡ (natℝ 16257 /ℝ natℝ 6000)
  s27095 =
    trans (/-cross-ℝ (trans (sym (natℝ-* 27095 2000)) (trans (cong natℝ refl) (natℝ-* 5419 10000))))
          (/-cross-ℝ (trans (sym (natℝ-* 5419 6000)) (trans (cong natℝ refl) (natℝ-* 16257 2000))))
  16250-lt-16257 : 16250 <ℕ 16257
  16250-lt-16257 = <-trans (<-suc 16250) (<-trans (<-suc 16251) (<-trans (<-suc 16252) (<-trans (<-suc 16253) (<-trans (<-suc 16254) (<-trans (<-suc 16255) (<-suc 16256))))))

-- d_H 拟合值上界：d_H < e
-- （**T3 阶段 4 闭合 2026-07-31**：d-H-fit = 27095/10000 < 27100/10000
--   < 813/300 < 815/300 = 163/60 = partial-e 5 < e [exp-partial-< 5]；
--   不再是 postulate）
dH-lt-e : d-H-fit <ℝ e
dH-lt-e = trans-<ℝ step1 (trans-<ℝ step2 step3)
  where
  27095-lt-27100 : 27095 <ℕ 27100
  27095-lt-27100 = <-trans (<-suc 27095) (<-trans (<-suc 27096) (<-trans (<-suc 27097) (<-trans (<-suc 27098) (<-suc 27099))))
  -- d-H-fit < 27100/10000
  step1 : d-H-fit <ℝ (natℝ 27100 /ℝ natℝ 10000)
  step1 = /-lt-same-den-ℝ {natℝ 27095} {natℝ 27100} {natℝ 10000}
                      (natℝ-<-embed 27095-lt-27100)
  b27100-813 : (natℝ 27100 /ℝ natℝ 10000) ≡ (natℝ 813 /ℝ natℝ 300)
  b27100-813 =
    trans (/-cross-ℝ (trans (sym (natℝ-* 27100 100)) (trans (cong natℝ refl) (natℝ-* 271 10000))))
          (/-cross-ℝ (trans (sym (natℝ-* 271 300)) (trans (cong natℝ refl) (natℝ-* 813 100))))
  b815 : (natℝ 815 /ℝ natℝ 300) ≡ (natℝ 163 /ℝ natℝ 60)
  b815 = /-cross-ℝ (trans (sym (natℝ-* 815 60)) (trans (cong natℝ refl) (natℝ-* 163 300)))
  -- 27100/10000 < 815/300
  step2 : (natℝ 27100 /ℝ natℝ 10000) <ℝ (natℝ 815 /ℝ natℝ 300)
  step2 =
    subst (λ x → x <ℝ (natℝ 815 /ℝ natℝ 300)) (sym b27100-813)
      (/-lt-same-den-ℝ {natℝ 813} {natℝ 815} {natℝ 300}
                       (natℝ-<-embed (<-trans (<-suc 813) (<-suc 814))))
  -- 815/300 = 163/60 = partial-e 5 < e
  step3 : (natℝ 815 /ℝ natℝ 300) <ℝ e
  step3 =
    subst (λ x → x <ℝ e) (sym b815)
      (subst (λ y → (natℝ 163 /ℝ natℝ 60) <ℝ y) (sym e-def)
        (subst (λ x → x <ℝ exp oneℝ) partial-e-5-value (exp-partial-< 5)))

-- 完整不等式链：ln 15 < 65/24 < d_H < e < 3
inequality-chain-full :
  (ln15 <ℝ sixtyfive-over-24) × (sixtyfive-over-24 <ℝ d-H-fit) × (d-H-fit <ℝ e) × (e <ℝ natℝ 3)
inequality-chain-full = ln15-lt-65-24 , sixtyfive-over-24-lt-dH , dH-lt-e , e-lt-3

-- ==================================================================
-- §6 δ 分解
-- ==================================================================

-- δ 观测值定义
delta-observed : delta-fit ≡ (d-H-fit -ℝ ln15)
delta-observed = refl
