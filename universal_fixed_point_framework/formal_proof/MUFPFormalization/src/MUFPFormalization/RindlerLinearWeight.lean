import Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus
import Mathlib.Analysis.Calculus.ContDiff.Basic
import Mathlib.Analysis.Calculus.ContDiff.Deriv
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.IteratedDeriv.Defs
import Mathlib.Analysis.Calculus.IteratedDeriv.Lemmas

/-!
# Rindler 线性权重：∫x·A'' 主项系数 = 0（P2-A 遗留候选）

来源：`notes/04_lorentz_gravity/Rindler区_kappa重算.md` §6 第 4 条（Lean 追加候选）。
背景：平直 Rindler 楔形（2607.07810 式 4.29）的模流权重 w_R(x¹) = x¹（线性，x¹ ∈ [0,R]），
与 dS 钻石（2311.13990 式 24）的二次权重 w(u)=u(u+2ℓ)（w''=2，主项系数 c=2）对照：
同一"分部积分模板 ∫w·A'' = c·∫A + 边界项"下，线性权重 w''=0 ⇒ **主项系数 c=0**——
Rindler 楔形无熵面积律主项的机器证明（κ 非普适裁决的显式机制）。

本文件一条定理：
1. `rindler_integral_identity`——∫₀^R x·A''(x)dx = R·A'(R) − A(R) + A(0)
   （一次分部积分：g = x·A'，∫g' = R·A'(R) − 0·A'(0)；∫A' = A(R) − A(0)；
   对比 KappaAudit.lean 的 integral_identity（二次权重，需两次分部积分、c=2）。

零 sorry 政策：本文件不含 sorry。
-/

namespace MUFPF.RindlerLinearWeight

noncomputable section

open scoped Interval

open MeasureTheory

/-- 线性权重：w_R(x) = x（2607.07810 式 4.29 的 Rindler 模流权重） -/
def rindler_weight (x : ℝ) : ℝ := x

/-- 权重性质：w'' = 0（线性函数二阶导为零）——c=0 的来源 -/
lemma rindler_weight_iterDeriv_two (x : ℝ) :
    iteratedDeriv 2 rindler_weight x = 0 := by
  unfold rindler_weight
  rw [iteratedDeriv_succ, iteratedDeriv_one]
  have hd1 : deriv (fun x : ℝ => x) = fun _ => 1 := by
    funext x
    rw [deriv_id'']
  rw [hd1]
  simp

/-- 积分恒等式：∫₀^R x·A''(x)dx = R·A'(R) − A(R) + A(0)（线性权重主项系数 0）
    证明（一次分部积分 + 微积分基本定理，w(x)=x，端点 g(0)=0·A'(0)=0）：
    g = x·A'：dg = A' + x·A'' ⇒ ∫dg = g(R)−g(0) = R·A'(R)
    ⇒ ∫x·A'' = R·A'(R) − ∫A' = R·A'(R) − (A(R) − A(0)) -/
lemma rindler_integral_identity (A : ℝ → ℝ) (R : ℝ) (hA : ContDiff ℝ 2 A) :
    (∫ u in 0..R, u * iteratedDeriv 2 A u) = R * deriv A R - A R + A 0 := by
  let a : ℝ := 0
  let b : ℝ := R
  have ha : a = 0 := rfl
  have hb : b = R := rfl
  -- 光滑性事实
  have hcA : Continuous A := hA.continuous
  have hcA' : Continuous (deriv A) := by
    have h := hA.continuous_iteratedDeriv 1 (by norm_num)
    rwa [iteratedDeriv_one] at h
  have hcA'' : Continuous (iteratedDeriv 2 A) := hA.continuous_iteratedDeriv 2 le_rfl
  have hdA' (u : ℝ) : DifferentiableAt ℝ (deriv A) u := by
    have h := hA.differentiable_iteratedDeriv 1 (by norm_num)
    rw [iteratedDeriv_one] at h
    exact h.differentiableAt
  have hdA0 (u : ℝ) : DifferentiableAt ℝ A u := by
    have h := hA.differentiable_iteratedDeriv 0 (by norm_num)
    exact h.differentiableAt
  -- 可积性
  have hintuA'' : IntervalIntegrable (fun u => u * iteratedDeriv 2 A u) volume a b :=
    (continuous_id.mul hcA'').continuousOn.intervalIntegrable
  have hintA' : IntervalIntegrable (fun u => deriv A u) volume a b :=
    hcA'.continuousOn.intervalIntegrable
  -- g = x·A'：dg = A' + x·A''；∫dg = R·A'(R)（端点 g(0)=0）
  have hdg (u : ℝ) :
      deriv (fun u => u * deriv A u) u = deriv A u + u * iteratedDeriv 2 A u := by
    change deriv ((fun u : ℝ => u) * fun u : ℝ => deriv A u) u = deriv A u + u * iteratedDeriv 2 A u
    have hf : DifferentiableAt ℝ (fun u : ℝ => u) u := differentiableAt_id
    have hg : DifferentiableAt ℝ (fun u : ℝ => deriv A u) u := hdA' u
    rw [deriv_mul hf hg]
    rw [deriv_id'']
    rw [← iteratedDeriv_one, ← iteratedDeriv_succ]
    simp
  have hcg' : Continuous (fun u => deriv A u + u * iteratedDeriv 2 A u) :=
    hcA'.add (continuous_id.mul hcA'')
  have hderiv_g : deriv (fun u => u * deriv A u)
      = fun u => deriv A u + u * iteratedDeriv 2 A u := by
    funext u
    exact hdg u
  have hftc_g := intervalIntegral.integral_deriv_eq_sub' (f := fun u => u * deriv A u)
    (f' := fun u => deriv A u + u * iteratedDeriv 2 A u)
    (a := a) (b := b) hderiv_g
    (by intro x hx; exact (differentiableAt_id).mul (hdA' x))
    (ContinuousOn.mono hcg'.continuousOn (Set.subset_univ (Set.uIcc a b)))
  have hbnd_g : b * deriv A b - a * deriv A a = R * deriv A R := by
    rw [ha, hb]
    ring
  have hftc_g_val : (∫ u in a..b, deriv (fun u => u * deriv A u) u) = R * deriv A R := by
    rw [hderiv_g]
    rw [hftc_g, hbnd_g]
  have hsplit : (∫ u in a..b, deriv A u) + (∫ u in a..b, u * iteratedDeriv 2 A u)
      = R * deriv A R := by
    have hsum := intervalIntegral.integral_add hintA' hintuA''
    have hcongr : (∫ u in a..b, deriv A u + u * iteratedDeriv 2 A u)
        = (∫ u in a..b, deriv (fun u => u * deriv A u) u) :=
      intervalIntegral.integral_congr (fun u _ => (hdg u).symm)
    rw [← hsum, hcongr, hftc_g_val]
  -- ∫A' = A(R) − A(0)（FTC）
  have hftcA := intervalIntegral.integral_deriv_eq_sub' (f := fun u => A u)
    (f' := fun u => deriv A u)
    (a := a) (b := b) (by funext u; rfl)
    (by intro x hx; exact hdA0 x)
    (ContinuousOn.mono hcA'.continuousOn (Set.subset_univ (Set.uIcc a b)))
  have hbndA : A b - A a = A R - A 0 := by
    rw [ha, hb]
  have hftcA_val : (∫ u in a..b, deriv A u) = A R - A 0 := by
    rw [hftcA, hbndA]
  -- 组装：∫x·A'' = R·A'(R) − (A(R) − A(0))
  have hfinal : (∫ u in a..b, u * iteratedDeriv 2 A u) = R * deriv A R - A R + A 0 := by
    have htmp : (∫ u in a..b, u * iteratedDeriv 2 A u)
        = R * deriv A R - (∫ u in a..b, deriv A u) := by
      linarith [hsplit]
    rw [htmp, hftcA_val]
    ring
  simpa [ha, hb] using hfinal

/-- 推论：线性权重主项系数 c = 0（∫x·A'' 表达式中无 ∫A 项）
    对照 dS 二次权重（KappaAudit.integral_identity，c=2）——Rindler 无面积律主项的算术依据 -/
theorem rindler_no_area_law_term (A : ℝ → ℝ) (R : ℝ) (hA : ContDiff ℝ 2 A) :
    (∫ u in 0..R, u * iteratedDeriv 2 A u) = R * deriv A R - A R + A 0 :=
  rindler_integral_identity A R hA

end

end MUFPF.RindlerLinearWeight
