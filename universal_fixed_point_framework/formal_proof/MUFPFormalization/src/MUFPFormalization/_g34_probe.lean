import MUFPFormalization.BerryChern
import Mathlib.Tactic

namespace MUFPF

namespace Probe34

/-- `λ`-切片：`γ(·, λ)`。 -/
noncomputable def slice (γ : C(unitInterval × unitInterval, ℂ)) (λ : unitInterval) :
    C(unitInterval, ℂ) :=
  ⟨fun t => γ (t, λ), γ.continuous.comp (continuous_id.prodMk continuous_const)⟩

/-- **度的绝热不变性**（§3 #4 完整陈述层）：设 `γ : C(I × I, ℂ)` 处处非零、且每条 `λ`-切片
    都是基点 `1` 的闭路（`γ (0, λ) = 1`、`γ (1, λ) = 1`），则两端切片的**度相同**——
    即度沿绝热参数 `λ` 不变。同伦由 `γ` 自身给出。 -/
theorem loopDegree_adiabatic_invariant
    (γ : C(unitInterval × unitInterval, ℂ)) (hnz : ∀ p, γ p ≠ 0)
    (h0 : ∀ λ, γ (0, λ) = 1) (h1 : ∀ λ, γ (1, λ) = 1) :
    loopDegree (loopLift (slice γ 0) (by simpa [slice] using h0 0)
        (fun t => by simpa [slice] using hnz (t, 0)))
      = loopDegree (loopLift (slice γ 1) (by simpa [slice] using h0 1)
        (fun t => by simpa [slice] using hnz (t, 1))) := by
  refine loopDegree_homotopy_invariant (γ₀ := slice γ 0) (γ₁ := slice γ 1)
    (by simpa [slice] using h0 0) (fun t => by simpa [slice] using hnz (t, 0))
    (by simpa [slice] using h0 1) (fun t => by simpa [slice] using hnz (t, 1)) ?_
  refine ⟨⟨⟨fun p : unitInterval × unitInterval => (⟨γ p, hnz p⟩ : {z : ℂ // z ≠ 0}), ?_⟩, ?_, ?_⟩, ?_⟩
  · exact Continuous.subtype_mk γ.continuous hnz
  · intro t
    exact Subtype.ext (by simpa [slice] using (h0 0 : γ (0, 0) = 1).trans (h0 t).symm) ▸ rfl
  · intro t
    exact Subtype.ext (by simpa [slice] using (h1 0 : γ (1, 0) = 1).trans (h1 t).symm) ▸ rfl
  · intro s hs
    rcases hs with h | h
    · subst h
      exact Subtype.ext (by simp only [slice]; exact (h0 0).trans (h0 1).symm)
    · subst h
      exact Subtype.ext (by simp only [slice]; exact (h1 0).trans (h1 1).symm)

end Probe34

end MUFPF
