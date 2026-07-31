module NatArith.NatArith where

{-
  NatArith：ℕ 算术引理库（路径 B 闭合用，无标准库依赖）
  =======================================================
  目标：为 T1（纯 ℕ/组合 postulate 闭合）与 T2（结构增强）提供
  最小但完整的 ℕ 算术引理，均为归纳/refl 直接证明，无 postulate。

  已含：
    +ℕ-suc      n + (1+m) = 1+(n+m)
    +ℕ-zero     n + 0 = n
    2*ℕ         2n = n + n
    ∸-zero      n - 0 = n
    ∸-1         (1+n) - 1 = n
    half        折半（结构递归）
    half-double half (n+n) = n
    half-2*ℕ    half (2n) = n
    half-8      half 8 = 4
-}

open import Agda.Builtin.Equality using (_≡_; refl)
open import Sp.SpCategory using (ℕ; zero; suc)
open import Rec.RecCategory using (cong; trans)

-- ==================================================================
-- §0 基础运算（从 Unified3 迁入，作为算术基础库）
-- ==================================================================

-- ℕ 加法与乘法
_+ℕ_ : ℕ → ℕ → ℕ
zero  +ℕ m = m
suc n +ℕ m = suc (n +ℕ m)

_*ℕ_ : ℕ → ℕ → ℕ
zero  *ℕ m = zero
suc n *ℕ m = m +ℕ (n *ℕ m)

-- 2 的幂
2^ : ℕ → ℕ
2^ zero    = 1
2^ (suc n) = 2 *ℕ (2^ n)

-- ==================================================================
-- §1 加法引理
-- ==================================================================

-- 加法右端换 suc
+ℕ-suc : (n m : ℕ) → n +ℕ (suc m) ≡ suc (n +ℕ m)
+ℕ-suc zero    m = refl
+ℕ-suc (suc n) m = cong suc (+ℕ-suc n m)

-- 加零右消：n + 0 = n
+ℕ-zero : (n : ℕ) → n +ℕ zero ≡ n
+ℕ-zero zero    = refl
+ℕ-zero (suc n) = cong suc (+ℕ-zero n)

-- 两倍：2n = n + n
2*ℕ : (n : ℕ) → 2 *ℕ n ≡ n +ℕ n
2*ℕ n = cong (λ x → n +ℕ x) (+ℕ-zero n)

-- ==================================================================
-- §2 截断减法引理
-- ==================================================================

-- 截断减法（B7 迁入，作为基础库）
_∸_ : ℕ → ℕ → ℕ
zero  ∸ m     = zero
suc n ∸ zero  = suc n
suc n ∸ suc m = n ∸ m

-- 减零恒等：n - 0 = n
∸-zero : (n : ℕ) → n ∸ zero ≡ n
∸-zero zero    = refl
∸-zero (suc n) = refl

-- 减一：suc n - 1 = n
∸-1 : (n : ℕ) → suc n ∸ 1 ≡ n
∸-1 n = ∸-zero n

-- 折半（结构递归）
half : ℕ → ℕ
half zero       = zero
half (suc zero) = zero
half (suc (suc n)) = suc (half n)

-- half 8 = 4
half-8 : half 8 ≡ 4
half-8 = refl

-- half (n + n) = n
half-double : (n : ℕ) → half (n +ℕ n) ≡ n
half-double zero = refl
half-double (suc m) =
  trans (cong half (cong suc (+ℕ-suc m m)))
        (cong suc (half-double m))

-- half (2n) = n
half-2*ℕ : (n : ℕ) → half (2 *ℕ n) ≡ n
half-2*ℕ n = trans (cong half (2*ℕ n)) (half-double n)

-- ==================================================================
-- §3 严格小于与良基递归（T1 闭合 log2 所需）
-- ==================================================================

infix 4 _<ℕ_
data _<ℕ_ : ℕ → ℕ → Set where
  z<s : {n : ℕ} → zero <ℕ suc n
  s<s : {m n : ℕ} → m <ℕ n → suc m <ℕ suc n

-- 传递性
<-trans : {a b c : ℕ} → a <ℕ b → b <ℕ c → a <ℕ c
<-trans z<s (s<s h) = z<s
<-trans (s<s h₁) (s<s h₂) = s<s (<-trans h₁ h₂)

-- 自反后继：n < 1+n
<-suc : (n : ℕ) → n <ℕ suc n
<-suc zero    = z<s
<-suc (suc n) = s<s (<-suc n)

-- 折半严格递减：half n < 1+n
half-lt : (n : ℕ) → half n <ℕ suc n
half-lt zero          = z<s
half-lt (suc zero)    = z<s
half-lt (suc (suc m)) = s<s (<-trans (half-lt m) (<-suc (suc m)))

-- 可达性（Acc）
data Acc (x : ℕ) : Set where
  acc : (∀ y → y <ℕ x → Acc y) → Acc x

s<s-inv : {m n : ℕ} → suc m <ℕ suc n → m <ℕ n
s<s-inv (s<s h) = h

acc-suc : (n : ℕ) → Acc n → Acc (suc n)
acc-suc n (acc h) = acc λ
  { zero    _        → acc (λ _ ())
  ; (suc m) sm<sn    → acc-suc m (h m (s<s-inv sm<sn))
  }

-- <ℕ 良基：每个数可达
wf-acc : (n : ℕ) → Acc n
wf-acc zero    = acc (λ y ())
wf-acc (suc n) = acc-suc n (wf-acc n)

-- 良基递归算子
wfRec : (P : ℕ → Set) → (∀ n → (∀ m → m <ℕ n → P m) → P n) → (n : ℕ) → Acc n → P n
wfRec P step n (acc h) = step n (λ m m<n → wfRec P step m (h m m<n))

-- 免 Acc 的递归入口
rec : (P : ℕ → Set) → (∀ n → (∀ m → m <ℕ n → P m) → P n) → (n : ℕ) → P n
rec P step n = wfRec P step n (wf-acc n)

-- ==================================================================
-- §4 log₂（T1 闭合：良基递归定义，具体值完全规范化）
-- ==================================================================

-- 递归步：log2 n = 1 + log2 ⌊n/2⌋（对 n ≥ 2）
log2-step : (n : ℕ) → (∀ m → m <ℕ n → ℕ) → ℕ
log2-step zero        f = zero
log2-step (suc zero)  f = zero
log2-step (suc (suc n)) f = suc (f (half (suc (suc n))) (s<s (half-lt n)))

-- log₂（总函数；具体值如 log2 8 可完全规范化）
log2 : ℕ → ℕ
log2 = rec (λ _ → ℕ) log2-step

-- log₂ 8 = 3（具体计算，refl）
log2-8 : log2 8 ≡ 3
log2-8 = refl
