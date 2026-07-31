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
