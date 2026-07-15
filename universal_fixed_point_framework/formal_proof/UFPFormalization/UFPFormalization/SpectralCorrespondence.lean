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
