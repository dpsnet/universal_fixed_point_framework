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

-- exp 的级数截断：部分和 < exp x（定义性公理，对应 Lean exp 级数；T3 阶段 2）
postulate
  exp-partial-< : (n : ℕ) → partial-e n <ℝ exp oneℝ

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
  -- log 级数截断（定义性公理，scoped；进闭合账目为开放项）
  ln2-lt : log (natℝ 2) <ℝ (natℝ 69317 /ℝ natℝ 100000)   -- ln2 < 0.69317
  ln1615-lb : (natℝ 29 /ℝ natℝ 450) <ℝ log (natℝ 16 /ℝ natℝ 15)  -- ln(1+1/15) > 29/450
  -- ln15 算术比较（账目开放项，scoped 数值公理）：4·0.69317 - 29/450 ≈ 2.7082356 < 65/24 ≈ 2.7083333。
  -- 分母 100000/450/24，交叉乘积 ~1e9-1e11 超出可手写 ℕ 链（对比 e < 3 的 288 规模可手算），
  -- 属资源/实践静默：纯有理比较在标准分析中可计算验证（数值见注释），但框架归一化能力不可达。
  ln15-arith-ax : ((natℝ 4 *ℝ (natℝ 69317 /ℝ natℝ 100000)) +ℝ negℝ (natℝ 29 /ℝ natℝ 450)) <ℝ (natℝ 65 /ℝ natℝ 24)
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

-- a·b = c ⟹ a = c/b（乘除消去）
*-div-impl : {a b c : ℝ} → (a *ℝ b) ≡ c → a ≡ c /ℝ b
*-div-impl {a} {b} {c} h =
  trans (sym (*-ident-ℝ a))
        (trans (cong (λ x → a *ℝ x) (sym (*-/cancel-ℝ b oneℝ)))
               (trans (sym (*-assoc-ℝ a b (oneℝ /ℝ b)))
                      (trans (cong₂ _*ℝ_ h refl)
                             (trans (*-/ℝ c oneℝ b)
                                    (cong₂ _/ℝ_ (*-ident-ℝ c) refl)))))

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

-- (a·b)/(c·b) = a/c（交叉相乘消去）
frac-cancel-ℝ : (a c b : ℝ) → (a *ℝ b) /ℝ (c *ℝ b) ≡ a /ℝ c
frac-cancel-ℝ a c b =
  /-cross-ℝ (trans (*-assoc-ℝ a b c)
                   (cong (λ u → a *ℝ u) (*-comm-ℝ b c)))

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
-- log 代数部分全部可证，仅纯有理比较按 scoped 公理 ln15-arith-ax 登记）
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
