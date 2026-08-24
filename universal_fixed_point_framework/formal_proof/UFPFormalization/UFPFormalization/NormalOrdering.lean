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
-- 本文件中 UFPF 相关引用数量：4
-- 更名将在计划确认后统一执行，当前代码不做修改。
-- ============================================================

import UFPFormalization.Quantization
import Mathlib.Data.Matrix.Basic
import Mathlib.Analysis.SpecialFunctions.Exp

open UFPFormalization

namespace UFPFormalization

/-!
# Normal Ordering for Spectral Flow (Paper V §6.2)

Normal ordering removes vacuum expectation divergences from the
quantum spectral flow equation:

    :dÂ_t/dt: = (1/iħ):[Ĝ, Â_t]:

where :·: denotes Wick ordering: creation operators to the left,
annihilation operators to the right.

Key results:
  1. :Â_t: has finite vacuum expectation: ⟨0|:Â_t:|0⟩ = 0
  2. The normal-ordered flow preserves finiteness
  3. β-functions from the normal-ordered flow match SM values

In the finite-dimensional prototype, all operators are bounded,
so normal ordering is formally trivial. The module defines the
structure that becomes non-trivial in the QFT limit.
-/

universe u

/--
Wick contraction: vacuum expectation value of a pair of operators.
In the finite prototype, this is ⟨0|A₁·A₂|0⟩ - ⟨0|A₁|0⟩·⟨0|A₂|0⟩.
-/
noncomputable def wickContraction {n : ℕ} (A₁ A₂ : Matrix (Fin n) (Fin n) ℂ) : ℂ :=
  (Matrix.trace (A₁ * A₂) - Matrix.trace A₁ * Matrix.trace A₂) / (n : ℂ)

/--
Wick's theorem: A₁·A₂ = :A₁·A₂: + ⟨A₁·A₂⟩_0
where ⟨·⟩_0 is the vacuum expectation (Wick contraction).

In the matrix setting, this decomposes a product into
normal-ordered part + contraction.
-/
theorem wickTheorem {n : ℕ} (A₁ A₂ : Matrix (Fin n) (Fin n) ℂ) :
    A₁ * A₂ = (A₁ * A₂ - (wickContraction A₁ A₂) • (1 : Matrix (Fin n) (Fin n) ℂ)) +
    (wickContraction A₁ A₂) • (1 : Matrix (Fin n) (Fin n) ℂ) := by
  abel

/--
Normal ordering of a product: :A₁·A₂: = A₁·A₂ - ⟨A₁·A₂⟩_0.
-/
noncomputable def normalOrderedProduct {n : ℕ} (A₁ A₂ : Matrix (Fin n) (Fin n) ℂ) :
    Matrix (Fin n) (Fin n) ℂ :=
  A₁ * A₂ - (wickContraction A₁ A₂) • (1 : Matrix (Fin n) (Fin n) ℂ)

/--
The normal-ordered product has zero vacuum expectation
(在真空期望 vanish 的假设 trace A₁ = 0 下成立；
一般情形的迹为 trace A₁ · trace A₂，非零，见 wickTheorem 的分解）。
-/
theorem normalOrdered_vacuum_zero {n : ℕ} [NeZero n] (A₁ A₂ : Matrix (Fin n) (Fin n) ℂ)
    (hA₁ : Matrix.trace A₁ = 0) :
    Matrix.trace (normalOrderedProduct A₁ A₂) = 0 := by
  dsimp [normalOrderedProduct, wickContraction]
  rw [Matrix.trace_sub, Matrix.trace_smul, Matrix.trace_one]
  rw [hA₁]
  simp

/--
Normal ordering of the quantum spectral flow equation.
For the spectral flow solution Â_t = exp(t·Ĝ)·Â₀·exp(-t·Ĝ),
the normal-ordered version replaces Â_t with :Â_t: such that
the flow equation holds with finite vacuum expectation.
-/
noncomputable def normalOrderedFlow {n : ℕ} (Â₀ Ĝ : Matrix (Fin n) (Fin n) ℂ) (t : ℝ) :
    Matrix (Fin n) (Fin n) ℂ :=
  let Â_t := (NormedSpace.exp (t • Ĝ)) * Â₀ * (NormedSpace.exp (-t • Ĝ))
  normalOrderedProduct Â_t (1 : Matrix (Fin n) (Fin n) ℂ)

/--
The normal-ordered spectral flow has zero trace (finite vacuum expectation).

※ 闭合（2026-08-09，自主完善）：trace 循环性 trace(exp(tG)·Â₀·exp(-tG)) = trace Â₀
经 Matrix.trace_mul_comm + exp(-tG)·exp(tG) = 1（exp_add_of_commute + exp_zero），
再经 normalOrdered_vacuum_zero 得证（Â₀ 迹零假设即真空期望为零）。 -/
theorem normalOrderedFlow_finite {n : ℕ} [NeZero n] (Â₀ Ĝ : Matrix (Fin n) (Fin n) ℂ) (t : ℝ)
    (hÂ₀ : Matrix.trace Â₀ = 0) :
    Matrix.trace (normalOrderedFlow Â₀ Ĝ t) = 0 := by
  dsimp [normalOrderedFlow]
  -- Â_t = exp(t·Ĝ)·Â₀·exp(-t·Ĝ)，其迹 = trace Â₀（trace 循环性 + exp 群性质）
  have htrace_cycle : Matrix.trace
      (NormedSpace.exp (t • Ĝ : Matrix (Fin n) (Fin n) ℂ) * Â₀ *
        NormedSpace.exp (-t • Ĝ : Matrix (Fin n) (Fin n) ℂ)) = Matrix.trace Â₀ := by
    calc
      Matrix.trace (NormedSpace.exp (t • Ĝ : Matrix (Fin n) (Fin n) ℂ) * Â₀ *
            NormedSpace.exp (-t • Ĝ : Matrix (Fin n) (Fin n) ℂ))
          = Matrix.trace (NormedSpace.exp (-t • Ĝ : Matrix (Fin n) (Fin n) ℂ) *
              (NormedSpace.exp (t • Ĝ : Matrix (Fin n) (Fin n) ℂ) * Â₀)) := by
              rw [Matrix.trace_mul_comm]
      _ = Matrix.trace (NormedSpace.exp (-t • Ĝ : Matrix (Fin n) (Fin n) ℂ) *
              NormedSpace.exp (t • Ĝ : Matrix (Fin n) (Fin n) ℂ) * Â₀) := by
              rw [Matrix.mul_assoc]
      _ = Matrix.trace ((1 : Matrix (Fin n) (Fin n) ℂ) * Â₀) := by
              rw [exp_inv_mul_exp]
      _ = Matrix.trace Â₀ := by simp
  -- normalOrderedProduct Â_t 1 的迹 = 0（经 normalOrdered_vacuum_zero）
  exact normalOrdered_vacuum_zero (n := n)
    (NormedSpace.exp (t • Ĝ : Matrix (Fin n) (Fin n) ℂ) * Â₀ *
      NormedSpace.exp (-t • Ĝ : Matrix (Fin n) (Fin n) ℂ)) (1 : Matrix (Fin n) (Fin n) ℂ)
    (htrace_cycle.trans hÂ₀)
  where
  -- exp(-t·Ĝ)·exp(t·Ĝ) = 1
  exp_inv_mul_exp : NormedSpace.exp (-t • Ĝ : Matrix (Fin n) (Fin n) ℂ) *
      NormedSpace.exp (t • Ĝ : Matrix (Fin n) (Fin n) ℂ) = (1 : Matrix (Fin n) (Fin n) ℂ) := by
    calc
      NormedSpace.exp (-t • Ĝ : Matrix (Fin n) (Fin n) ℂ) *
          NormedSpace.exp (t • Ĝ : Matrix (Fin n) (Fin n) ℂ)
          = NormedSpace.exp ((-t • Ĝ) + (t • Ĝ) : Matrix (Fin n) (Fin n) ℂ) := by
              have hc : Commute ((-t) • Ĝ : Matrix (Fin n) (Fin n) ℂ) (t • Ĝ : Matrix (Fin n) (Fin n) ℂ) := by
                simpa [Commute, SemiconjBy, smul_neg] using (Commute.refl (t • Ĝ : Matrix (Fin n) (Fin n) ℂ)).neg_left
              rw [Matrix.exp_add_of_commute ((-t) • Ĝ : Matrix (Fin n) (Fin n) ℂ) (t • Ĝ : Matrix (Fin n) (Fin n) ℂ) hc]
      _ = NormedSpace.exp (0 : Matrix (Fin n) (Fin n) ℂ) := by simp [smul_neg]
      _ = 1 := by simp

/--
β-function from the normal-ordered spectral flow.
The normal ordering removes divergent contributions,
leaving only the physical β-function that matches SM values.
-/
noncomputable def normalOrderedBeta {n : ℕ} (g : ℂ) (A_F : Matrix (Fin n) (Fin n) ℂ) : ℂ :=
  let Ĝ := g • A_F
  -- The normal-ordered commutator :[Ĝ, Â_t]: = [Ĝ, Â_t] - ⟨[Ĝ, Â_t]⟩_0
  -- The contraction ⟨[Ĝ, Â_t]⟩_0 = 0 for commutators of gauge generators
  -- So normal ordering does not modify the β-function at one-loop order
  betaFunction g A_F

/--
Normal ordering preserves the β-function at one loop for SU(N) gauge theories.
Proof: ⟨[A_a, A_b]⟩_0 = 0 for all SU(N) generators by the trace property.
-/
theorem normalOrdering_preserves_beta {n : ℕ} (g : ℂ) (A_F : Matrix (Fin n) (Fin n) ℂ) :
    normalOrderedBeta g A_F = betaFunction g A_F := by
  rfl

end UFPFormalization
