import Mathlib.Data.Complex.Basic
import Mathlib.Analysis.SpecialFunctions.Complex.Log
import Mathlib.Analysis.SpecialFunctions.Complex.Arg
import Mathlib.Topology.Algebra.Circle
import Mathlib.Analysis.SpecialFunctions.Exponential
import Mathlib.Analysis.Complex.LineIntegrals.Basic
open Complex
open scoped Real

example (z : ℂ) (hz : z ≠ 0) : Complex.exp (Complex.log z) = z := by
  rw [Complex.exp_log hz]

example (z : ℂ) (h : Complex.exp z = 1) : z = 2 * ↑Real.pi * Complex.I * (Classical.choose (Complex.exists_pow_mul_eq_exp h)) := by
  -- 检测 Complex.exp 的周期整性引理存在性
  sorry

-- 检测 unit_circle 与绕数基础
example (z : unit_circle) : ∃ k : ℤ, Complex.arg z = (2 * ↑Real.pi * (k : ℝ)) := by
  sorry