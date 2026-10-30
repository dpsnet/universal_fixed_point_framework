-- ============================================================
-- ExpTruncation.lean — e 内生化桥：代数阶截断的有理恒等与误差界构件
-- ============================================================
-- 背景（e 内生化桥 104az-197/198，笔记 notes/e_internalization_bridge.md）：
--   框架代数阶 k_max = 8 内的 exp 机制截断：Σ_{k=0}^{8} 1/k! = 109601/40320
--   （1e-6 级逼近 e；8! = 40320 = 2⁷·3²·5·7 全框架分解；|S₈| = 8!）
--
-- 定理 1（已闭合）：截断和 = 精确有理数 109601/40320（norm_num）
-- 引理 A/B/C（已闭合）：误差界构件——9!·10^(n−9) ≤ n!、1/n! 倒数上界、等比级数和
-- 定理 2（待闭合，缺口登记）：|e − 109601/40320| ≤ 10/(9·9!)
--
-- 零 sorry 政策：本文件不含 sorry。

import Mathlib.Tactic
import Mathlib.Data.Real.Basic

open scoped BigOperators

namespace MUFPF.ExpTruncation

-- 框架组合对象总数 k_max = 8（三重锁定：通道数 P7-5e-91 / dim Cl(3) / Bott 塔 (1,7) 截断）
def kMax : ℕ := 8

-- 截断和（有理）：Σ_{k=0}^{K} 1/k!
def eTrunc (K : ℕ) : ℚ :=
  ∑ k ∈ Finset.range (K + 1), (1 : ℚ) / (k.factorial : ℚ)

-- 参数化截断（实数）：Σ_{k=0}^{K} x^k/k!（S99 卷积恢复分析的精度基础）
noncomputable def eTruncArg (K : ℕ) (x : ℝ) : ℝ :=
  ∑ k ∈ Finset.range (K + 1), x ^ k / (k.factorial : ℝ)

-- 定理 1：Σ_{k=0}^{8} 1/k! = 109601/40320（精确有理恒等）
theorem eTrunc_kMax_exact :
    eTrunc kMax = 109601 / 40320 := by
  norm_num [eTrunc, kMax]

-- 推论：截断和分母 = 8! = 40320 = |S₈|（8 阶排列计数）；109601 = 40320·e 的 8 阶截断分子
-- 数值验证（先证伪再证明）：109601/40320 = 2.71827876984127...，|e − ·| = 3.0586e-6 < 10/(9·9!) = 3.062e-6 ✓

-- ------------------------------------------------------------
-- 引理 A：对 n ≥ 9，9! · 10^{n−9} ≤ n!（余项上界核心）
-- ------------------------------------------------------------
lemma factorial_ge_nine_pow (n : ℕ) (hn : 9 ≤ n) :
    Nat.factorial 9 * 10 ^ (n - 9) ≤ n.factorial := by
  induction' n with n ih
  · omega
  · by_cases h9 : 9 ≤ n
    · have hih := ih h9
      have h10 : 10 ≤ n + 1 := by omega
      have hsub : (n + 1) - 9 = (n - 9) + 1 := by omega
      have hstep1 : Nat.factorial 9 * 10 ^ (n - 9) * 10 ≤ n.factorial * 10 := by
        exact Nat.mul_le_mul_right 10 hih
      have hstep2 : n.factorial * 10 ≤ n.factorial * (n + 1) := by
        exact Nat.mul_le_mul_left n.factorial h10
      calc
        Nat.factorial 9 * 10 ^ ((n + 1) - 9) = Nat.factorial 9 * (10 ^ (n - 9) * 10) := by
          rw [hsub, pow_succ]
        _ = Nat.factorial 9 * 10 ^ (n - 9) * 10 := by ring
        _ ≤ n.factorial * 10 := hstep1
        _ ≤ n.factorial * (n + 1) := hstep2
        _ = (n + 1).factorial := by
          rw [Nat.factorial_succ]
          ring
    · -- ¬ 9 ≤ n 且 9 ≤ n+1 ⇒ n = 8，直接验证
      have hn8 : n = 8 := by omega
      subst n
      norm_num

-- ------------------------------------------------------------
-- 引理 B：1/n! ≤ 1/(9!·10^{n−9})（实数版，由引理 A 推出）
-- ------------------------------------------------------------
lemma inv_factorial_le (n : ℕ) (hn : 9 ≤ n) :
    ((1 : ℝ) / n.factorial) ≤ 1 / (Nat.factorial 9 * 10 ^ (n - 9)) := by
  have hle : (Nat.factorial 9 * 10 ^ (n - 9) : ℝ) ≤ (n.factorial : ℝ) := by
    exact_mod_cast factorial_ge_nine_pow n hn
  have hpos : (0 : ℝ) < Nat.factorial 9 * 10 ^ (n - 9) := by
    exact_mod_cast (Nat.mul_pos (Nat.factorial_pos 9) (pow_pos (by norm_num : 0 < 10) (n - 9)))
  have hposn : (0 : ℝ) < n.factorial := by exact_mod_cast Nat.factorial_pos n
  exact one_div_le_one_div_of_le hpos hle

-- ------------------------------------------------------------
-- 引理 C：等比级数 ∑' j, (1/10)^j = 10/9（mathlib: tsum_geometric_of_abs_lt_one）
-- ------------------------------------------------------------
lemma geom_sum_tail :
    (∑' j : ℕ, ((1 : ℝ) / 10) ^ j) = 10 / 9 := by
  have h : (∑' j : ℕ, ((1 : ℝ) / 10) ^ j) = (1 - (1 : ℝ) / 10)⁻¹ := by
    exact tsum_geometric_of_abs_lt_one (r := (1 : ℝ) / 10) (by norm_num)
  rw [h]
  norm_num

-- ------------------------------------------------------------
-- 引理 D（初等）：尾和部分上界
--   对任意 N ≥ 9：Σ_{k=9}^{N} 1/k! ≤ 10/(9·9!)
--   证明：差值 = 平移尾和（归纳）→ 逐项 ≤ 1/(9!·10^j)（引理 B）
--         → 等比部分和 ≤ 10/9（geom_sum_eq）
-- ------------------------------------------------------------
lemma tail_partial_bound (N : ℕ) (hN : 9 ≤ N) :
    (∑ k ∈ Finset.range (N + 1), ((1 : ℝ) / k.factorial)) -
      (∑ k ∈ Finset.range 9, ((1 : ℝ) / k.factorial)) ≤ 10 / (9 * (Nat.factorial 9 : ℝ)) := by
  -- 差值 = Σ_{j ∈ range (N−8)} 1/((j+9)!)（对 N 归纳）
  have hshift :
      (∑ k ∈ Finset.range (N + 1), ((1 : ℝ) / k.factorial)) -
      (∑ k ∈ Finset.range 9, ((1 : ℝ) / k.factorial)) =
      (∑ j ∈ Finset.range (N - 8), ((1 : ℝ) / (j + 9).factorial)) := by
    induction' N with N ih
    · omega
    · by_cases h9 : 9 ≤ N
      · have hih := ih h9
        have hL : (∑ k ∈ Finset.range (N + 2), ((1 : ℝ) / k.factorial)) =
            (∑ k ∈ Finset.range (N + 1), ((1 : ℝ) / k.factorial)) + ((1 : ℝ) / (N + 1).factorial) := by
          have hsucc := Finset.sum_range_succ (fun k : ℕ => ((1 : ℝ) / k.factorial)) (N + 1)
          simpa [show N + 2 = (N + 1) + 1 by omega] using hsucc
        have hR : (∑ j ∈ Finset.range (N - 7), ((1 : ℝ) / (j + 9).factorial)) =
            (∑ j ∈ Finset.range (N - 8), ((1 : ℝ) / (j + 9).factorial)) + ((1 : ℝ) / (N + 1).factorial) := by
          have hdim : N - 7 = (N - 8) + 1 := by omega
          rw [hdim]
          have hsucc := Finset.sum_range_succ (fun j : ℕ => ((1 : ℝ) / (j + 9).factorial)) (N - 8)
          simpa [show (N - 8) + 9 = N + 1 by omega] using hsucc
        calc
          (∑ k ∈ Finset.range (N + 2), ((1 : ℝ) / k.factorial)) -
              (∑ k ∈ Finset.range 9, ((1 : ℝ) / k.factorial))
              = (∑ k ∈ Finset.range (N + 1), ((1 : ℝ) / k.factorial)) +
                  ((1 : ℝ) / (N + 1).factorial) - (∑ k ∈ Finset.range 9, ((1 : ℝ) / k.factorial)) := by
                rw [hL]
          _ = ((∑ k ∈ Finset.range (N + 1), ((1 : ℝ) / k.factorial)) -
                  (∑ k ∈ Finset.range 9, ((1 : ℝ) / k.factorial))) + ((1 : ℝ) / (N + 1).factorial) := by
                ring
          _ = (∑ j ∈ Finset.range (N - 8), ((1 : ℝ) / (j + 9).factorial)) +
                  ((1 : ℝ) / (N + 1).factorial) := by
                rw [hih]
          _ = (∑ j ∈ Finset.range (N - 7), ((1 : ℝ) / (j + 9).factorial)) := by
                rw [hR]
      · have hN8 : N = 8 := by omega
        subst N
        norm_num [Finset.sum_range_succ]
  rw [hshift]
  -- 逐项 ≤ 1/(9!·10^j)（引理 B，n = j+9；显式 ℝ 类型）
  have hterm (j : ℕ) : ((1 : ℝ) / (j + 9).factorial) ≤
      (1 : ℝ) / ((Nat.factorial 9 : ℝ) * (10 : ℝ) ^ j) := by
    have hb := inv_factorial_le (j + 9) (by omega)
    simpa [Nat.add_sub_cancel] using hb
  have h1 : (∑ j ∈ Finset.range (N - 8), ((1 : ℝ) / (j + 9).factorial)) ≤
      (∑ j ∈ Finset.range (N - 8), (1 : ℝ) / ((Nat.factorial 9 : ℝ) * (10 : ℝ) ^ j)) := by
    exact Finset.sum_le_sum (fun j _ => hterm j)
  refine le_trans h1 ?_
  -- 等比部分和 ≤ 10/9（geom_sum_eq）
  have hg : (∑ j ∈ Finset.range (N - 8), ((1 : ℝ) / 10) ^ j) ≤ 10 / 9 := by
    have hgeom := geom_sum_eq (by norm_num : ((1 : ℝ) / 10) ≠ 1) (N - 8)
    rw [hgeom]
    have ha : 0 ≤ ((1 : ℝ) / 10) ^ (N - 8) := by positivity
    have hden : 0 < 1 - (1 : ℝ) / 10 := by norm_num
    have heq : ((((1 : ℝ) / 10) ^ (N - 8)) - 1) / (((1 : ℝ) / 10) - 1) =
        (1 - ((1 : ℝ) / 10) ^ (N - 8)) / (1 - (1 : ℝ) / 10) := by ring_nf
    rw [heq]
    calc
      (1 - ((1 : ℝ) / 10) ^ (N - 8)) / (1 - (1 : ℝ) / 10) ≤ 1 / (1 - (1 : ℝ) / 10) := by
        exact div_le_div_of_nonneg_right (by nlinarith [ha]) (le_of_lt hden)
      _ = 10 / 9 := by norm_num
  -- 1/(9!·10^j) = (1/9!)·(1/10)^j；提取公共因子
  have hfact : (∑ j ∈ Finset.range (N - 8), (1 : ℝ) / ((Nat.factorial 9 : ℝ) * (10 : ℝ) ^ j)) =
      (1 / (Nat.factorial 9 : ℝ)) * (∑ j ∈ Finset.range (N - 8), ((1 : ℝ) / 10) ^ j) := by
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro j hj
    field_simp
    rw [← mul_pow]
    norm_num
  rw [hfact]
  calc
    (1 / (Nat.factorial 9 : ℝ)) * (∑ j ∈ Finset.range (N - 8), ((1 : ℝ) / 10) ^ j)
        ≤ (1 / (Nat.factorial 9 : ℝ)) * (10 / 9) := by
      exact mul_le_mul_of_nonneg_left hg (by positivity)
    _ = 10 / (9 * (Nat.factorial 9 : ℝ)) := by ring

-- ------------------------------------------------------------
-- 定理 2（闭合 2026-10-26）：|e − eTrunc kMax| ≤ 10/(9·9!)
--   路径：mathlib Real.exp_bound（x = 1, n = 9）
--         |exp 1 − Σ_{m<9} 1/m!| ≤ |1|^9·(9+1)/(9!·9) = 10/(9·9!)
--   先证伪：|e − 109601/40320| = 3.0586e-6 < 10/(9·9!) = 3.062e-6 ✓
--           （scripts/s98_exp_remainder_check.py——残差 −3.3e-9）
-- ------------------------------------------------------------
theorem eRemainder_bound :
    |Real.exp 1 - (eTrunc kMax : ℝ)| ≤ (10 : ℝ) / (9 * (Nat.factorial 9 : ℝ)) := by
  have hb := Real.exp_bound (x := (1 : ℝ)) (n := 9) (by norm_num) (by norm_num)
  -- hb : |Real.exp 1 - ∑ m ∈ Finset.range 9, 1 ^ m / ↑m.factorial|
  --      ≤ |1| ^ 9 * (↑9.succ / (↑9.factorial * ↑9))
  have heq : (eTrunc kMax : ℝ) = (∑ m ∈ Finset.range 9, (1 : ℝ) ^ m / (m.factorial : ℝ)) := by
    unfold eTrunc kMax
    norm_num
  rw [← heq] at hb
  -- 化简右侧：|1|^9·(9+1)/(9!·9) = 10/(9·9!) = 1/326592
  norm_num at hb
  norm_num
  exact hb

-- ------------------------------------------------------------
-- S99 推论：卷积放大界（2026-10-26）
--   |eTrunc² − e²| ≤ δ·(2e + δ)，δ = 10/(9·9!)
--   |a²−b²| = |a−b|·|a+b|（sq_sub_sq）——|a−b| ≤ δ（定理 2）——
--   |a+b| ≤ 2e+δ（三角不等式）
--   数值（先证伪）：e8² vs e² = 1.6628e-5 ≤ 3.06e-6·(5.437+3.06e-6)
--   　             = 1.664e-5 ✓（scripts/s99_conv_bias_check.py）
--   物理意义：截断平方的偏差 ≈ 2e·δ——"平方放大单侧余项 2e 倍"
-- ------------------------------------------------------------
theorem eTrunc_conv_sq_bias :
    |(eTrunc kMax : ℝ) ^ 2 - (Real.exp 1) ^ 2| ≤
      (10 : ℝ) / (9 * (Nat.factorial 9 : ℝ)) *
        (2 * Real.exp 1 + (10 : ℝ) / (9 * (Nat.factorial 9 : ℝ))) := by
  set δ := (10 : ℝ) / (9 * (Nat.factorial 9 : ℝ))
  have hδ : |Real.exp 1 - (eTrunc kMax : ℝ)| ≤ δ := eRemainder_bound
  have habs : |(eTrunc kMax : ℝ) - Real.exp 1| ≤ δ := by
    rw [abs_sub_comm]
    exact hδ
  have hab1 : |(eTrunc kMax : ℝ)| ≤ Real.exp 1 + δ := by
    have htri : |(eTrunc kMax : ℝ)| ≤
        |(eTrunc kMax : ℝ) - Real.exp 1| + |Real.exp 1| := by
      simpa [sub_add_cancel] using
        (abs_add_le ((eTrunc kMax : ℝ) - Real.exp 1) (Real.exp 1))
    have hlin : |(eTrunc kMax : ℝ) - Real.exp 1| + |Real.exp 1| ≤ δ + Real.exp 1 := by
      rw [abs_of_nonneg (le_of_lt (Real.exp_pos 1))]
      exact add_le_add_left habs (Real.exp 1)
    exact (le_trans htri hlin).trans (le_of_eq (by ring : δ + Real.exp 1 = Real.exp 1 + δ))
  have hbnd : |(eTrunc kMax : ℝ) + Real.exp 1| ≤ 2 * Real.exp 1 + δ := by
    have htri : |(eTrunc kMax : ℝ) + Real.exp 1| ≤
        |(eTrunc kMax : ℝ)| + |Real.exp 1| := abs_add_le _ _
    have hlin : |(eTrunc kMax : ℝ)| + |Real.exp 1| ≤ (Real.exp 1 + δ) + Real.exp 1 := by
      rw [abs_of_nonneg (le_of_lt (Real.exp_pos 1))]
      exact add_le_add_left hab1 (Real.exp 1)
    calc
      |(eTrunc kMax : ℝ) + Real.exp 1| ≤ |(eTrunc kMax : ℝ)| + |Real.exp 1| := htri
      _ ≤ (Real.exp 1 + δ) + Real.exp 1 := hlin
      _ = 2 * Real.exp 1 + δ := by ring
  have hfac : |(eTrunc kMax : ℝ) ^ 2 - (Real.exp 1) ^ 2| =
      |(eTrunc kMax : ℝ) - Real.exp 1| * |(eTrunc kMax : ℝ) + Real.exp 1| := by
    rw [← abs_mul]
    congr 1
    rw [sq_sub_sq]
    ring
  rw [hfac]
  exact mul_le_mul habs hbnd (abs_nonneg _) (by
    unfold δ
    positivity)

-- ------------------------------------------------------------
-- S99 推广：参数化余项界（2026-10-26）
--   eRemainder_bound_arg：对 |x| ≤ 1、任意 K：
--     |exp x − Σ_{k=0}^{K} x^k/k!| ≤ |x|^(K+1)·((K+1)+1)/((K+1)!·(K+1))
--   路径：mathlib Real.exp_bound（n = K+1——精确匹配）
--   意义：框架代数阶 8 内 exp 机制对任意参数的余项界——S99 卷积
--   恢复分析（e^{0.5} 侧）的精度基础
-- ------------------------------------------------------------
theorem eRemainder_bound_arg {x : ℝ} (hx : |x| ≤ 1) (K : ℕ) :
    |Real.exp x - eTruncArg K x| ≤ |x| ^ (K + 1) *
      (((K + 1 : ℕ).succ : ℝ) / (((K + 1 : ℕ).factorial : ℝ) * ((K + 1 : ℕ) : ℝ))) := by
  have hb := Real.exp_bound (x := x) (n := K + 1) hx (by omega)
  have heq : eTruncArg K x = ∑ m ∈ Finset.range (K + 1), x ^ m / (m.factorial : ℝ) := rfl
  rw [heq]
  exact hb

-- 特例（x = 1/2, K = 8）：e^{0.5} 的 8 阶截断余项界
--   |e^{0.5} − Σ_{k=0}^{8} 0.5^k/k!| ≤ (1/2)^9·10/(9·9!) = 10/(512·9·9!)
theorem eRemainder_bound_half :
    |Real.exp (1 / 2 : ℝ) - eTruncArg 8 (1 / 2 : ℝ)| ≤
      ((1 / 2 : ℝ) ^ 9) * (10 : ℝ) / (9 * (Nat.factorial 9 : ℝ)) := by
  have hb := eRemainder_bound_arg (x := (1 / 2 : ℝ)) (by norm_num) 8
  norm_num at hb
  norm_num
  exact hb

-- ------------------------------------------------------------
-- S101：截断卷积系数恒等锚（2026-10-26）
--   conv_coeff_anchor_8：Σ_{k=0}^{8} (0.5^k/k!)·(0.5^{8-k}/(8-k)!) = 1/8!
--   二项式卷积恒等（Σ_{k≤8} choose(8,k) = 2^8 = 256）在 n=8 处的
--   具体呈现——"卷积恢复"（S99/S100）的组合学根源：e^{0.5} 截断卷积
--   的 n≤8 系数精确等于 e^1 系数（n=8 是最深阶——最有代表性）
-- ------------------------------------------------------------
theorem conv_coeff_anchor_8 :
    ∑ k ∈ Finset.range 9,
        ((1 / 2 : ℝ) ^ k / (k.factorial : ℝ)) *
          ((1 / 2 : ℝ) ^ (8 - k) / ((8 - k).factorial : ℝ))
      = (1 : ℝ) ^ 8 / ((8 : ℕ).factorial : ℝ) := by
  norm_num

-- ------------------------------------------------------------
-- S102：模流一参数群性质（时间可加性——e 的加法律）（2026-10-26）
--   E1 深化（裸 Δ 与递归时间伴随）的算子幂侧锚：
--   文献"模流 = 时间"——Δ_mod^{it} = e^{it·ln Δ_mod}——一参数群
--   （时间可加性：Δ^{i(t+s)} = Δ^{it}·Δ^{is}——群同态 ℝ → Aut）
--   用单位圆上的复指数实现（S96/S97 周期资产复用）：
--   e^{i(t+s)} = e^{it}·e^{is}——"时间的可加性 = exp 的加法律
--   （Complex.exp_add）= e 的加法律——e = 计数 EGF（S98）——
--   时间可加性来自计数结构"
-- ------------------------------------------------------------
theorem modflow_group_prop (t s : ℝ) :
    Complex.exp (Complex.I * (t + s)) =
      Complex.exp (Complex.I * t) * Complex.exp (Complex.I * s) := by
  have hdist : Complex.I * (t + s) = Complex.I * t + Complex.I * s := by ring
  rw [hdist, Complex.exp_add]

-- 时间反转（逆元）：e^{it}·e^{−it} = 1——模流的可逆性
theorem modflow_inv (t : ℝ) :
    Complex.exp (Complex.I * t) * Complex.exp (-(Complex.I * t)) = 1 := by
  rw [← Complex.exp_add]
  have hz : Complex.I * t + (-(Complex.I * t)) = 0 := by ring
  rw [hz]
  norm_num

-- 恒等元（t = 0）：e^{i·0} = 1——模流的单位
theorem modflow_identity :
    Complex.exp (Complex.I * 0) = 1 := by
  norm_num

-- ------------------------------------------------------------
-- S103：256 三重身份（2026-10-27）
--   frame_count_256：2^8 = 16^2 = Σ_{k≤8} choose(8,k) = 256
--   ——K_max = 8 层递归的框架计数结构——幂基翻倍（2^8）、16 态窗口
--   平方（16²）、组合计数（Σchoose——二项式卷积恒等 Σchoose = 2^n 在
--   n = 8 处——S101 锚的结构版——256 = 0.5^8·256/8! = 1/8! 的计数来源）
-- ------------------------------------------------------------
theorem frame_count_256 :
    (2 : ℕ) ^ 8 = 16 ^ 2 ∧ (2 : ℕ) ^ 8 = ∑ k ∈ Finset.range 9, Nat.choose 8 k := by
  constructor
  · norm_num
  · decide

end MUFPF.ExpTruncation
