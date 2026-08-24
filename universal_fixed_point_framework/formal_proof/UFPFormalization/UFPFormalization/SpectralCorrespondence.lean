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
-- 本文件中 UFPF 相关引用数量：2
-- 更名将在计划确认后统一执行，当前代码不做修改。
-- ============================================================

import Mathlib.Analysis.SpecialFunctions.Complex.Log
import Mathlib.Data.Complex.Basic

namespace UFPFormalization

/-- Spectral correspondence eta : compression eigenvalue mu ↦ operator eigenvalue e^{-mu}. -/
noncomputable def spectralMap (mu : ℂ) : ℂ := Complex.exp (-mu)

/-- Inverse correspondence: operator eigenvalue lambda ↦ compression eigenvalue -log lambda.
    Uses the principal branch of the complex logarithm. -/
noncomputable def spectralInv (lambda : ℂ) : ℂ := -Complex.log lambda

/-- On the principal branch, -log(e^{-mu}) = mu for mu with imaginary part in [-π, π). -/
theorem spectralInv_leftInv {mu : ℂ} (h : mu.im ∈ Set.Ico (-Real.pi) Real.pi) :
    spectralInv (spectralMap mu) = mu := by
  simp [spectralInv, spectralMap]
  rw [Complex.log_exp (show -Real.pi < (-mu).im by simp; linarith [h.1, h.2])
                      (show (-mu).im ≤ Real.pi by simp; linarith [h.1, h.2])]
  simp

/-- e^{-(-log lambda)} = lambda for non-zero lambda. -/
theorem spectralMap_rightInv {lambda : ℂ} (h : lambda ≠ 0) :
    spectralMap (spectralInv lambda) = lambda := by
  simp [spectralInv, spectralMap, Complex.exp_log h]

end UFPFormalization
