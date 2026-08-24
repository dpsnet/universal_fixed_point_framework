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
open import Sp.SpCategory using (ℕ; zero; suc; sym; cong; trans)

-- ==================================================================
-- §0 基础运算（从 Unified3 迁入，作为算术基础库）
-- ==================================================================

-- ℕ 加法与乘法
-- 2026-08-05 二进制 ℕ 算术降级路径：NATPLUS/NATTIMES 绑定启用 Agda 内置任意精度
-- 算术（O(log²)，无 suc 链），使 ~1e8 级交叉乘积可行（此前 2.8e8 处 OOM）。递归
-- 方程保留（引理按模式匹配仍成立），归约经内建加速。
_+ℕ_ : ℕ → ℕ → ℕ
zero  +ℕ m = m
suc n +ℕ m = suc (n +ℕ m)

{-# BUILTIN NATPLUS _+ℕ_ #-}

_*ℕ_ : ℕ → ℕ → ℕ
zero  *ℕ m = zero
suc n *ℕ m = m +ℕ (n *ℕ m)

{-# BUILTIN NATTIMES _*ℕ_ #-}

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

-- ==================================================================
-- 大数比较基础设施（2026-08-05，二进制 ℕ 算术降级路径）
-- 目标：ln2-lt/ln15-arith-ax 所需 ~1e8 级交叉乘积比较。
-- 字面量经 BUILTIN NATURAL 为紧凑二进制；_+ℕ_/_*ℕ_ 仍为递归定义
-- （线性慢）。这里提供"差值递归"不等式：证明深度 = 差值 k，而非 m，
-- 使大数 m < n（n-m 小）可用 O(k²) 规模构造，无需展开 m。
-- ==================================================================

-- 右递归加法：m + (k+1) 只做 k+1 步归约（第二参数递归）
_+ℕr_ : ℕ → ℕ → ℕ
m +ℕr zero    = m
m +ℕr (suc n) = suc (m +ℕr n)

-- m < m + (k+1)：递归深度 = k（差），配合 _+ℕr_ 的 O(k) 归约
<-add : (m k : ℕ) → m <ℕ (m +ℕr suc k)
<-add m zero    = <-suc m
<-add m (suc k) = <-trans (<-add m k) (<-suc (m +ℕr suc k))

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

-- ==================================================================
-- §5 ℕ 半环代数（2026-08-05，exp-tail-bound 降定理阶乘强估计基础）
-- +ℕ/*ℕ 的交换/结合/单位（归纳按定义方程，BUILTIN 绑定不影响方程匹配）
-- ==================================================================

-- 加法交换
+ℕ-comm : (m n : ℕ) → m +ℕ n ≡ n +ℕ m
+ℕ-comm zero    n = sym (+ℕ-zero n)
+ℕ-comm (suc m) n = trans (cong suc (+ℕ-comm m n)) (sym (+ℕ-suc n m))

-- 加法结合
+ℕ-assoc : (m n p : ℕ) → (m +ℕ n) +ℕ p ≡ m +ℕ (n +ℕ p)
+ℕ-assoc zero    n p = refl
+ℕ-assoc (suc m) n p = cong suc (+ℕ-assoc m n p)

-- 乘法右零：m·0 = 0
*ℕ-zero-r : (m : ℕ) → m *ℕ zero ≡ zero
*ℕ-zero-r zero    = refl
*ℕ-zero-r (suc m) = cong (λ x → zero +ℕ x) (*ℕ-zero-r m)

-- 乘法右单位：m·1 = m
*ℕ-ident-r : (m : ℕ) → m *ℕ 1 ≡ m
*ℕ-ident-r zero    = refl
*ℕ-ident-r (suc m) = cong (λ x → 1 +ℕ x) (*ℕ-ident-r m)

-- 乘法右端 suc：n·(1+m) = n + n·m
*ℕ-suc-r : (n m : ℕ) → n *ℕ (suc m) ≡ n +ℕ (n *ℕ m)
*ℕ-suc-r zero m = refl
*ℕ-suc-r (suc n) m =
  trans (cong (λ x → suc m +ℕ x) (*ℕ-suc-r n m))
        (trans (sym (+ℕ-assoc (suc m) n (n *ℕ m)))
               (trans (cong (λ x → x +ℕ (n *ℕ m)) (+ℕ-comm (suc m) n))
                      (trans (+ℕ-assoc n (suc m) (n *ℕ m))
                             (+ℕ-suc n (m +ℕ (n *ℕ m))))))

-- 乘法交换
*ℕ-comm : (m n : ℕ) → m *ℕ n ≡ n *ℕ m
*ℕ-comm zero    n = sym (*ℕ-zero-r n)
*ℕ-comm (suc m) n =
  trans (cong (λ x → n +ℕ x) (*ℕ-comm m n))
        (sym (*ℕ-suc-r n m))

-- 乘法右分配：(a+b)·c = a·c + b·c
*ℕ-distrib-r : (a b c : ℕ) → (a +ℕ b) *ℕ c ≡ (a *ℕ c) +ℕ (b *ℕ c)
*ℕ-distrib-r zero    b c = refl
*ℕ-distrib-r (suc a) b c =
  trans (cong (λ x → c +ℕ x) (*ℕ-distrib-r a b c))
        (sym (+ℕ-assoc c (a *ℕ c) (b *ℕ c)))

-- 乘法结合
*ℕ-assoc : (m n p : ℕ) → (m *ℕ n) *ℕ p ≡ m *ℕ (n *ℕ p)
*ℕ-assoc zero n p = refl
*ℕ-assoc (suc m) n p =
  trans (*ℕ-distrib-r n (m *ℕ n) p)
        (cong (λ x → (n *ℕ p) +ℕ x) (*ℕ-assoc m n p))

-- ==================================================================
-- §6 ≤ℕ 非严格序（2026-08-05，阶乘强估计基础）
-- ==================================================================

infix 4 _≤ℕ_
data _≤ℕ_ : ℕ → ℕ → Set where
  z≤n : {n : ℕ} → zero ≤ℕ n
  s≤s : {m n : ℕ} → m ≤ℕ n → suc m ≤ℕ suc n

-- 自反
≤ℕ-refl : {m : ℕ} → m ≤ℕ m
≤ℕ-refl {zero}    = z≤n
≤ℕ-refl {suc m}   = s≤s ≤ℕ-refl

-- 传递
≤ℕ-trans : {m n p : ℕ} → m ≤ℕ n → n ≤ℕ p → m ≤ℕ p
≤ℕ-trans z≤n       _         = z≤n
≤ℕ-trans (s≤s hmn) (s≤s hnp) = s≤s (≤ℕ-trans hmn hnp)

-- 从 <ℕ 到 ≤ℕ
<-≤ℕ : {m n : ℕ} → m <ℕ n → m ≤ℕ n
<-≤ℕ z<s        = z≤n
<-≤ℕ (s<s h)    = s≤s (<-≤ℕ h)

-- suc 单调
≤ℕ-suc : {m n : ℕ} → m ≤ℕ n → suc m ≤ℕ suc n
≤ℕ-suc = s≤s

-- *ℕ 保序（右因子）：a ≤ b ⟹ 0 < c ⟹ a·c ≤ b·c
*ℕ-≤-mono-r : {a b c : ℕ} → a ≤ℕ b → 0 <ℕ c → (a *ℕ c) ≤ℕ (b *ℕ c)
*ℕ-≤-mono-r {c = zero}  _ ()
*ℕ-≤-mono-r {a = zero}  {b} {suc k} z≤n _ = z≤n
*ℕ-≤-mono-r {a = suc a} {suc b} {suc k} (s≤s hab) _ =
  +ℕ-≤-mono-r {a = a *ℕ suc k} {b = b *ℕ suc k} {c = suc k}
               (*ℕ-≤-mono-r {a} {b} {suc k} hab z<s)
  where
  +ℕ-≤-mono-r : {a b c : ℕ} → a ≤ℕ b → (c +ℕ a) ≤ℕ (c +ℕ b)
  +ℕ-≤-mono-r {c = zero}  h = h
  +ℕ-≤-mono-r {c = suc c} h = s≤s (+ℕ-≤-mono-r {c = c} h)
