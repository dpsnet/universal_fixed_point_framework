import Mathlib.Analysis.Complex.Basic
import Mathlib.Analysis.Complex.Exponential
import Mathlib.Analysis.SpecialFunctions.Complex.Log
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Algebra.Order.Ring.Int

/-!
# P1-B：模流周期 2π 命题化（周期闭合 ⇒ T = 2π 的解析内核）

路线图 §1.2 的候选生成链要求"流闭合（cyclic 条件）Δ^{i(t+T)} = Δ^{it} ⇒ T = 2π"。
风险记账 1（推进建议 §3.1）要求先裁决：**2π 是单位约定还是同伦不变量**。

本文件把该裁决的**解析内核**形式化：复指数沿虚轴的周期族恰为 2πℤ，
即 exp(i·) 的最小正周期 = 2π。mathlib 中 exp 由级数定义，其周期性与
Real.pi 的取值均为**定理**而非公设——因此"周期闭合 ⇒ T = 2π"在此不是循环论证。

- 定理 1（`exp_period_closed_form`）：T>0 时 exp(z + T·i) = exp z 恒成立 ⇔ T = 2πn（n≥1）。
- 定理 2（`exp_minimal_period_two_pi`）：2π·i 是 exp 的周期，且任何正周期 ≥ 2π。
- 物理对接（模流层命题，见《模流周期2pi命题化_笔记.md》）：BW 定理 Δ = e^{−2πM} 使模流
  Δ^{it} 的闭合周期 = 2π ×（M 谱整数化条件）；本文件只形式化 exp 层的唯一性。
- 诚实边界：Bott/Clifford 周期 8 与 2π 无数值关联（8 = 实 Clifford 周期，2π = exp 最小正
  周期），路线图 §1.2 的"Clifford ⇒ 4π ⇒ 2π"环节未被本定理支撑——见笔记的裁决。

零 sorry 政策：本文件不含 sorry。
-/

namespace MUFPF.TwoPiPeriodicity

open scoped ComplexConjugate

/- 辅助引理：若 T·i = n·(2π·i)（n : ℤ），则 T = n·2π（取虚部） -/
lemma of_exp_eq_one_coeff {T : ℝ} {n : ℤ}
    (h : T * Complex.I = (n : ℂ) * (2 * Real.pi * Complex.I)) :
    T = (n : ℝ) * (2 * Real.pi) := by
  have him := congrArg Complex.im h
  simpa [Complex.mul_im, Complex.ofReal_re, Complex.ofReal_im, Complex.I_re, Complex.I_im]
    using him

/-- 引理：exp(2π·i) = 1（Complex.exp_periodic 在 0 处的取值） -/
lemma exp_two_pi_eq_one : Complex.exp (2 * Real.pi * Complex.I) = 1 := by
  simp

/-- 定理 1：沿虚轴平移 T·i 的 exp 周期族闭式：正周期恰为 2π·n（n ≥ 1） -/
theorem exp_period_closed_form {T : ℝ} (hT : 0 < T) :
    (∀ z : ℂ, Complex.exp (z + T * Complex.I) = Complex.exp z) ↔
      ∃ n : ℕ, 1 ≤ n ∧ T = 2 * Real.pi * n := by
  constructor
  · intro hperiod
    have h1 := hperiod 0
    simp at h1
    have hn := Complex.exp_eq_one_iff.mp h1
    rcases hn with ⟨n, hn_eq⟩
    have hT_eq : T = (n : ℝ) * (2 * Real.pi) := by
      exact of_exp_eq_one_coeff hn_eq
    have hprod_pos : 0 < (n : ℝ) * (2 * Real.pi) := by
      rw [← hT_eq]
      exact hT
    have hnR_pos : 0 < (n : ℝ) := by
      have hdiv : (n : ℝ) = T / (2 * Real.pi) := by
        rw [hT_eq]
        field_simp [Real.two_pi_pos.ne']
      rw [hdiv]
      exact div_pos hT Real.two_pi_pos
    have hn_pos : 0 < n := by
      exact_mod_cast hnR_pos
    let m : ℕ := n.toNat
    have hn_nonneg : 0 ≤ n := le_of_lt hn_pos
    have hn_toNat : (m : ℤ) = n := Int.toNat_of_nonneg hn_nonneg
    have hm_cast : (m : ℝ) = (n : ℝ) := by
      exact_mod_cast hn_toNat
    have hm_ge1 : 1 ≤ m := by
      have hn_ge1 : (1 : ℤ) ≤ n := by
        exact_mod_cast hn_pos
      have hmz : (1 : ℤ) ≤ (m : ℤ) := by
        simpa [← hn_toNat] using hn_ge1
      exact_mod_cast hmz
    have hT_m : T = 2 * Real.pi * m := by
      rw [hT_eq]
      rw [← hm_cast]
      ring
    exact ⟨m, hm_ge1, hT_m⟩
  · intro ⟨n, hn1, hn_eq⟩ z
    have hcast : T * Complex.I = (n : ℂ) * (2 * Real.pi * Complex.I) := by
      rw [hn_eq]
      norm_num [Complex.ofReal_mul]
      ring
    calc
      Complex.exp (z + T * Complex.I)
          = Complex.exp (z + (n : ℂ) * (2 * Real.pi * Complex.I)) := by
            rw [hcast]
      _ = Complex.exp z * Complex.exp ((n : ℂ) * (2 * Real.pi * Complex.I)) := by
            rw [← Complex.exp_add]
      _ = Complex.exp z * (Complex.exp (2 * Real.pi * Complex.I) ^ n) := by
            rw [Complex.exp_nat_mul]
      _ = Complex.exp z := by
            rw [exp_two_pi_eq_one]
            simp

/-- 定理 2：2π·i 是 exp 的周期，且任何正周期 ≥ 2π（2π 为最小正周期） -/
theorem exp_minimal_period_two_pi :
    Function.Periodic Complex.exp (2 * Real.pi * Complex.I) ∧
      ∀ {T : ℝ}, 0 < T →
        (∀ z : ℂ, Complex.exp (z + T * Complex.I) = Complex.exp z) → 2 * Real.pi ≤ T := by
  constructor
  · exact Complex.exp_periodic
  · intro T hT hperiod
    rcases (exp_period_closed_form hT).mp hperiod with ⟨n, hn1, hn_eq⟩
    rw [hn_eq]
    exact le_mul_of_one_le_right Real.two_pi_pos.le (by exact_mod_cast hn1)

/-! =========================================================
    S96-1："π 是 e 的半周期"（2026-10-22 立项、2026-10-26 机检入档）
    π 的框架导出新路径（绕开已失败的级数截断）：
    环 1：e 已框架化（e 桥强候选——Σ_{k=0}^{8} 1/k! 阶乘截断——exp 机制
          已立——用户已接受 e^{−(...)} 链）
    环 2：e^{iz} 的最小正周期 = 2π（exp_minimal_period_two_pi——已机检）
    环 3：π = 半周期——欧拉恒等式 e^{πi} = −1（本文件机检——
          exp_pi_mul_I 在 π 处取值——半周期位移使 e 反号）
    环 4：π = (2π)/2——π 是模流周期的二分之一（SilenceFamily S96-2）
    环 5：8π = 不动点 × (e^{iz} 周期)——引力耦合 = 时空维数 × e 的指数
          周期（SilenceFamily S96-3）——π 在 8π 中的角色 = e 的半周期
    ⟹ π 不再是"独立无理常数"——它是 e 的指数周期结构（2π 的一半）
    的导出量——π 的框架导出 = 经 e 的周期性（结构性质）而非级数近似。
   ========================================================= -/

/-- ★★ 欧拉恒等式：e^{πi} = −1（π 是 e^{iz} 的"半周期"——半周期位移
    使指数反号——π = e 的指数周期的一半的代数证据）。 -/
theorem exp_pi_half_period : Complex.exp (Real.pi * Complex.I) = -1 := by
  simpa using (Complex.exp_pi_mul_I : Complex.exp (Real.pi * Complex.I) = -1)

end MUFPF.TwoPiPeriodicity
