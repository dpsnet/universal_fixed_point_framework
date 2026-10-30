import Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus
import Mathlib.Analysis.Calculus.ContDiff.Basic
import Mathlib.Analysis.Calculus.ContDiff.Deriv
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.IteratedDeriv.Defs
import Mathlib.Analysis.Calculus.IteratedDeriv.Lemmas

/-!
# κ=1/4 审计条目形式化（P1-A，2026-10-23）

来源：`notes/04_lorentz_gravity/kappa_1of4_审计与G内生清单.md` §7 的三条可机检条目。
背景：2311.13990（Fröb–Much–Papadopoulos, PTEP 2024 021A01）式 20→21→24 的 κ=1/4G_N 推导。
审计结论（已在 docs 落盘）："4"的算术来源 = 模流权重 w(u)=u(u+2ℓ) 的二阶导（w''=2）×
零平均长度（2ℓ）÷ 权重系数（16G_Nℓ）→ 2·(2ℓ)/(16ℓ) = 1/4。

本文件三条定理：
1. `weight_boundary_zero`/`weight_iterDeriv_two`/`weight_nonpos`——权重性质；
2. `integral_identity`——积分恒等式 ∫_{−2ℓ}^{0} w(u)A''(u)du = 2∫A du − 2ℓ[A(0)+A(−2ℓ)]
   （证明路径：乘积法则 + 微积分基本定理，g=w·A' 与 h=w'·A 各做一次分部积分）；
3. `coeff_arithmetic`/`kappa_quarter`——系数组合与式 24 整体系数。

零 sorry 政策：本文件不含 sorry。
-/

namespace MUFPF.KappaAudit

noncomputable section

open scoped Interval

open MeasureTheory

-- ============================================================
-- 权重函数 w(u) = u(u+2ℓ)（式 17 的模流权重）
-- ============================================================

/-- 模流权重 w(u) = u(u+2ℓ) -/
def weight (ell : ℝ) (u : ℝ) : ℝ := u * (u + 2 * ell)

/-- 条目 1a：w(0) = 0 -/
lemma weight_zero (ell : ℝ) : weight ell 0 = 0 := by
  simp [weight]

/-- 条目 1b：w(−2ℓ) = 0 -/
lemma weight_neg_two_mul (ell : ℝ) : weight ell (-2 * ell) = 0 := by
  simp [weight]

/-- 条目 1：w(0)=0 且 w(−2ℓ)=0（边界消失，式 21→24 的关键） -/
lemma weight_boundary_zero (ell : ℝ) :
    weight ell (-2 * ell) = 0 ∧ weight ell 0 = 0 := by
  constructor <;> simp [weight]

/-- 权重导数：w'(u) = 2u + 2ℓ -/
lemma weight_deriv (ell u : ℝ) : deriv (weight ell) u = 2 * u + 2 * ell := by
  unfold weight
  change deriv ((fun u : ℝ => u) * fun u : ℝ => u + 2 * ell) u = 2 * u + 2 * ell
  have hf : DifferentiableAt ℝ (fun u : ℝ => u) u := differentiableAt_id
  have hg : DifferentiableAt ℝ (fun u : ℝ => u + 2 * ell) u := by
    fun_prop
  rw [deriv_mul hf hg]
  rw [deriv_id'']
  have hg1 : DifferentiableAt ℝ (fun u : ℝ => u) u := differentiableAt_id
  have hg2 : DifferentiableAt ℝ (fun _ : ℝ => 2 * ell) u := by
    fun_prop
  change (fun x : ℝ => 1) u * (u + 2 * ell) + u * deriv ((fun u : ℝ => u) + fun _ : ℝ => 2 * ell) u = 2 * u + 2 * ell
  rw [deriv_add hg1 hg2]
  rw [deriv_id'']
  simp
  ring

/-- 仿射函数导数：deriv (2u + 2ℓ) = 2 -/
lemma affine_deriv (ell u : ℝ) : deriv (fun u : ℝ => 2 * u + 2 * ell) u = 2 := by
  change deriv ((fun u : ℝ => 2 * u) + fun _ : ℝ => 2 * ell) u = 2
  have h1 : DifferentiableAt ℝ (fun u : ℝ => 2 * u) u := by
    fun_prop
  have h2 : DifferentiableAt ℝ (fun _ : ℝ => 2 * ell) u := by
    fun_prop
  rw [deriv_add h1 h2]
  change deriv ((fun _ : ℝ => (2 : ℝ)) * fun u : ℝ => u) u + deriv (fun _ : ℝ => 2 * ell) u = 2
  have hc : DifferentiableAt ℝ (fun _ : ℝ => (2 : ℝ)) u := differentiableAt_const (c := (2 : ℝ))
  have hid : DifferentiableAt ℝ (fun u : ℝ => u) u := differentiableAt_id
  rw [deriv_mul hc hid]
  rw [deriv_id'']
  rw [deriv_const]
  simp

/-- 条目 1c：w'' = 2（iteratedDeriv 2 w = 常值 2） -/
lemma weight_iterDeriv_two (ell : ℝ) : iteratedDeriv 2 (weight ell) = fun _ => 2 := by
  funext u
  rw [iteratedDeriv_succ, iteratedDeriv_one]
  have hw_eq : deriv (weight ell) = fun u => 2 * u + 2 * ell := by
    funext u
    rw [weight_deriv]
  rw [hw_eq]
  exact affine_deriv ell u

/-- 条目 1d：u ∈ [−2ℓ, 0]（ℓ ≥ 0）时 w(u) ≤ 0——熵被积函数的正性来源 -/
lemma weight_nonpos (_hell : 0 ≤ ell) {u : ℝ} (hu : u ∈ Set.Icc (-2 * ell) 0) :
    weight ell u ≤ 0 := by
  have h1 : u ≤ 0 := hu.2
  have h2 : 0 ≤ u + 2 * ell := by
    linarith [hu.1]
  simpa [weight] using (mul_nonpos_of_nonpos_of_nonneg h1 h2)

-- ============================================================
-- 条目 2：积分恒等式（式 20 → 21 的算术内核）
-- ============================================================

/-- 积分恒等式：∫_{−2ℓ}^{0} u(u+2ℓ)·A''(u) du = 2∫A du − 2ℓ[A(0)+A(−2ℓ)]
    证明（乘积法则 + 微积分基本定理，w=u(u+2ℓ)，w(0)=w(−2ℓ)=0）：
    g = w·A'：∫g' = g(b)−g(a) = 0 ⇒ ∫w·A'' = −∫w'·A'
    h = w'·A：∫h' = h(b)−h(a) = 2ℓ[A(a)+A(b)] = ∫w''·A + ∫w'·A' = 2∫A + ∫w'·A'
    ⇒ ∫w·A'' = −(2ℓ[A(a)+A(b)] − 2∫A) = 2∫A − 2ℓ[A(0)+A(−2ℓ)] -/
lemma integral_identity (A : ℝ → ℝ) (ell : ℝ) (hA : ContDiff ℝ 2 A) :
    (∫ u in (-2 * ell)..0, weight ell u * iteratedDeriv 2 A u) =
      2 * (∫ u in (-2 * ell)..0, A u) - 2 * ell * (A 0 + A (-2 * ell)) := by
  let a : ℝ := -2 * ell
  let b : ℝ := 0
  let w : ℝ → ℝ := weight ell
  let wp : ℝ → ℝ := fun u => 2 * u + 2 * ell
  have ha : a = -2 * ell := rfl
  have hb : b = 0 := rfl
  -- 光滑性事实
  have hcw : Continuous w := by
    simp [w]
    unfold weight
    continuity
  have hcwp : Continuous wp := by
    unfold wp
    continuity
  have hdw (u : ℝ) : DifferentiableAt ℝ w u := by
    simp [w]
    unfold weight
    fun_prop
  have hdwp (u : ℝ) : DifferentiableAt ℝ wp u := by
    unfold wp
    fun_prop
  have hcA : Continuous A := hA.continuous
  have hcA' : Continuous (deriv A) := by
    have h := hA.continuous_iteratedDeriv 1 (by norm_num)
    rwa [iteratedDeriv_one] at h
  have hdA' (u : ℝ) : DifferentiableAt ℝ (deriv A) u := by
    have h := hA.differentiable_iteratedDeriv 1 (by norm_num)
    rw [iteratedDeriv_one] at h
    exact h.differentiableAt
  have hcA'' : Continuous (iteratedDeriv 2 A) := hA.continuous_iteratedDeriv 2 le_rfl
  have hwp_eq : deriv w = wp := by
    funext u
    simp [w, wp, weight_deriv]
  have hdwp2 : deriv wp = fun _ => 2 := by
    funext u
    exact affine_deriv ell u
  -- 可积性（连续 ⇒ IntervalIntegrable）
  have hintwA'' : IntervalIntegrable (fun u => w u * iteratedDeriv 2 A u) volume a b :=
    (hcw.mul hcA'').continuousOn.intervalIntegrable
  have hintwpA' : IntervalIntegrable (fun u => wp u * deriv A u) volume a b :=
    (hcwp.mul hcA').continuousOn.intervalIntegrable
  have hc2A : Continuous (fun u => (deriv wp) u * A u) := by
    rw [hdwp2]
    exact (continuous_const.mul hcA)
  have hint2A : IntervalIntegrable (fun u => (deriv wp) u * A u) volume a b :=
    hc2A.continuousOn.intervalIntegrable
  -- g = w·A'：dg = wp·A' + w·A''；∫dg = 0（边界 w(a)=w(b)=0）
  have hdg (u : ℝ) :
      deriv (fun u => w u * deriv A u) u = wp u * deriv A u + w u * iteratedDeriv 2 A u := by
    change deriv (w * deriv A) u = wp u * deriv A u + w u * iteratedDeriv 2 A u
    rw [deriv_mul (hdw u) (hdA' u)]
    rw [hwp_eq]
    rw [← iteratedDeriv_one, ← iteratedDeriv_succ]
  have hcg' : Continuous (fun u => wp u * deriv A u + w u * iteratedDeriv 2 A u) :=
    (hcwp.mul hcA').add (hcw.mul hcA'')
  have hderiv_g : deriv (fun u => w u * deriv A u)
      = fun u => wp u * deriv A u + w u * iteratedDeriv 2 A u := by
    funext u
    exact hdg u
  have hftc_g := intervalIntegral.integral_deriv_eq_sub' (f := fun u => w u * deriv A u)
    (f' := fun u => wp u * deriv A u + w u * iteratedDeriv 2 A u)
    (a := a) (b := b) hderiv_g
    (by intro x hx; exact (hdw x).mul (hdA' x))
    (ContinuousOn.mono hcg'.continuousOn (Set.subset_univ (Set.uIcc a b)))
  have hzero : w b * deriv A b - w a * deriv A a = 0 := by
    rw [ha, hb]
    have h1 : w 0 = 0 := by
      simpa [w] using weight_zero ell
    have h2 : w (-(2 * ell)) = 0 := by
      simpa [w] using weight_neg_two_mul ell
    simp [h1, h2]
  have hftc0 : (∫ u in a..b, deriv (fun u => w u * deriv A u) u) = 0 := by
    rw [hderiv_g]
    rw [hftc_g, hzero]
  have hsplit : (∫ u in a..b, wp u * deriv A u) + (∫ u in a..b, w u * iteratedDeriv 2 A u) = 0 := by
    have hsum := intervalIntegral.integral_add hintwpA' hintwA''
    have hcongr : (∫ u in a..b, wp u * deriv A u + w u * iteratedDeriv 2 A u)
        = (∫ u in a..b, deriv (fun u => w u * deriv A u) u) :=
      intervalIntegral.integral_congr (fun u _ => (hdg u).symm)
    rw [← hsum, hcongr, hftc0]
  have hstep1 : (∫ u in a..b, w u * iteratedDeriv 2 A u) = - (∫ u in a..b, wp u * deriv A u) := by
    linarith [hsplit]
  -- h = wp·A：dh = (deriv wp)·A + wp·A'；∫dh = 2ℓ[A(a)+A(b)]
  have hdh (u : ℝ) :
      deriv (fun u => wp u * A u) u = (deriv wp) u * A u + wp u * deriv A u := by
    change deriv (wp * A) u = (deriv wp) u * A u + wp u * deriv A u
    rw [deriv_mul (hdwp u) (hA.differentiable (by norm_num)).differentiableAt]
  have hch' : Continuous (fun u => (deriv wp) u * A u + wp u * deriv A u) :=
    hc2A.add (hcwp.mul hcA')
  have hderiv_h : deriv (fun u => wp u * A u)
      = fun u => (deriv wp) u * A u + wp u * deriv A u := by
    funext u
    exact hdh u
  have hftc_h := intervalIntegral.integral_deriv_eq_sub' (f := fun u => wp u * A u)
    (f' := fun u => (deriv wp) u * A u + wp u * deriv A u)
    (a := a) (b := b) hderiv_h
    (by intro x hx; exact (hdwp x).mul (hA.differentiable (by norm_num)).differentiableAt)
    (ContinuousOn.mono hch'.continuousOn (Set.subset_univ (Set.uIcc a b)))
  have hbnd_h : wp b * A b - wp a * A a = 2 * ell * (A a + A b) := by
    rw [ha, hb]
    unfold wp
    ring
  have hftc_h_val : (∫ u in a..b, deriv (fun u => wp u * A u) u) = 2 * ell * (A a + A b) := by
    rw [hderiv_h]
    rw [hftc_h, hbnd_h]
  have h2A : (∫ u in a..b, (deriv wp) u * A u) = 2 * (∫ u in a..b, A u) := by
    have hdwp2' : ∀ u, (deriv wp) u = 2 := by
      intro u
      rw [hdwp2]
    calc
      (∫ u in a..b, (deriv wp) u * A u) = (∫ u in a..b, 2 * A u) :=
        intervalIntegral.integral_congr (fun u _ => by rw [hdwp2'])
      _ = 2 * (∫ u in a..b, A u) := intervalIntegral.integral_const_mul (2 : ℝ) A
  have hsum2 : (∫ u in a..b, (deriv wp) u * A u) + (∫ u in a..b, wp u * deriv A u)
      = (∫ u in a..b, deriv (fun u => wp u * A u) u) := by
    have hsum := intervalIntegral.integral_add hint2A hintwpA'
    rw [← hsum]
    exact intervalIntegral.integral_congr (fun u _ => (hdh u).symm)
  have hstep2 : (∫ u in a..b, wp u * deriv A u) = 2 * ell * (A a + A b) - 2 * (∫ u in a..b, A u) := by
    have htmp : (∫ u in a..b, wp u * deriv A u)
        = (∫ u in a..b, deriv (fun u => wp u * A u) u) - (∫ u in a..b, (deriv wp) u * A u) := by
      linarith [hsum2]
    rw [htmp, hftc_h_val, h2A]
  -- 组装
  have hfinal : (∫ u in a..b, w u * iteratedDeriv 2 A u) =
      2 * (∫ u in a..b, A u) - 2 * ell * (A a + A b) := by
    rw [hstep1, hstep2]
    ring
  simpa [w, ha, hb, add_comm, add_left_comm, add_assoc, mul_add, add_mul] using hfinal

-- ============================================================
-- 条目 3：系数组合 2·(2ℓ)/(16ℓ) = 1/4 与 κ=1/4 整体系数
-- ============================================================

/-- 条目 3a：2·(2ℓ)/(16ℓ) = 1/4（ℓ ≠ 0）——"4"的算术来源 -/
lemma coeff_arithmetic (ell : ℝ) (hell : ell ≠ 0) :
    (2 * (2 * ell)) / (16 * ell) = (1 : ℝ) / 4 := by
  field_simp [hell]
  ring

/-- 条目 3b：κ=1/4 整体系数（式 24 的形式）
    由 integral_identity 乘以 1/(16G_Nℓ)，并把 ⟨⟨A⟩⟩=(1/2ℓ)∫A du 代入 -/
lemma kappa_quarter (A : ℝ → ℝ) (ell GN : ℝ) (hA : ContDiff ℝ 2 A)
    (hell : ell ≠ 0) (hGN : GN ≠ 0) :
    (1 / (16 * GN * ell)) * (∫ u in (-2 * ell)..0, weight ell u * iteratedDeriv 2 A u) =
      (1 / (4 * GN)) * ((1 / (2 * ell)) * (∫ u in (-2 * ell)..0, A u))
        - (A 0 + A (-2 * ell)) / (8 * GN) := by
  rw [integral_identity A ell hA]
  field_simp [hell, hGN]
  ring

end

end MUFPF.KappaAudit
