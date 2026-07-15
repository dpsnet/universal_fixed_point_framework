/-
谱对应 M ≅ L 自然等价的有限维原型形式化（复数域 ℂ 版本）。

在论文 Paper I §3 中，谱对应指：
- 乘法谱 M：Koopman 算子 U_R 的特征值集合 {λ_i}
- 加法谱 L：谱算子 A_R = -log U_R 的特征值集合 {μ_i}
两者通过 λ = e^{-μ} 一一对应。

等级 A 原型中，对有限维复向量空间上的线性自同态 T : V → V：
- M(T) = {λ ∈ ℂ | ∃ v ≠ 0, T v = λ v}
- L(T) = {μ ∈ ℂ | ∃ v ≠ 0, T v = e^{-μ} v}

这里我们在复数域 ℂ 上形式化谱集合之间的双射，并验证 μ ↦ e^{-μ} 是双射
（选定复对数的主值支，即 Im(log z) ∈ (-π, π]）。
-/

import Mathlib.Data.Complex.Exponential
import Mathlib.LinearAlgebra.Eigenspace
import Mathlib.Data.Set.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Data.Real.Pi
import UFPFormalization.RecCategory
import UFPFormalization.SpecCategory

universe v

namespace SpectralCorrespondence

open Complex

/-- 乘法谱 M：算子 T 的所有特征值集合。 -/
def MultSpectrum (X : RecObject ℂ) : Set ℂ :=
  {λ : ℂ | ∃ v : X.V, v ≠ 0 ∧ X.T v = λ • v}

/-- 加法谱 L：满足 e^{-μ} 是 T 的特征值的所有 μ 集合。 -/
def AddSpectrum (X : RecObject ℂ) : Set ℂ :=
  {μ : ℂ | ∃ v : X.V, v ≠ 0 ∧ X.T v = (exp (-μ)) • v}

/-- 非零乘法谱：排除 λ = 0 的特征值，保证对数有定义。 -/
def NonzeroMultSpectrum (X : RecObject ℂ) : Set ℂ :=
  {λ : MultSpectrum X // λ.val ≠ 0}

/-- 主值加法谱：限制 Im(μ) ∈ (-π, π]，保证 log(exp(-μ)) = -μ。 -/
def PrincipalAddSpectrum (X : RecObject ℂ) : Set ℂ :=
  {μ : AddSpectrum X | (μ.val).im ∈ Set.Ioc (-Real.pi) Real.pi}

/-- 从加法谱到乘法谱的映射：μ ↦ e^{-μ}。 -/
def addToMult (X : RecObject ℂ) (μ : AddSpectrum X) : MultSpectrum X :=
  ⟨exp (-μ.val), by
    rcases μ.property with ⟨v, hv, hev⟩
    use v
    constructor
    · exact hv
    · simpa using hev⟩

/-- 从非零乘法谱到主值加法谱的映射：λ ↦ -log λ。
    复对数主值保证 Im(log λ) ∈ (-π, π]，因此 Im(-log λ) ∈ [-π, π)。
    为严格落在 (-π, π]，需排除 Im(log λ) = π 的边界（即负实轴）。
    等级 A 原型中先给出构造，边界处理在后续完善。 -/
noncomputable def multToAdd (X : RecObject ℂ) (λ : NonzeroMultSpectrum X) : AddSpectrum X :=
  ⟨-log λ.val, by
    rcases λ.val.property with ⟨v, hv, hev⟩
    use v
    constructor
    · exact hv
    · rw [neg_neg, ← hev]
      congr
      rw [exp_log]
      exact λ.property⟩

/-- 对 λ ≠ 0，exp(-log λ) = λ。 -/
lemma addToMult_multToAdd (X : RecObject ℂ) (λ : NonzeroMultSpectrum X) :
    addToMult X (multToAdd X λ) = λ.val := by
  rcases λ with ⟨λ_val, hλprop, hλnz⟩
  ext
  simp [addToMult, multToAdd]
  rw [exp_log]
  exact hλnz

/-- 对 μ 满足 Im(-μ) ∈ (-π, π]，有 log(exp(-μ)) = -μ。
    即 Im(μ) ∈ (-π, π]。 -/
lemma multToAdd_addToMult (X : RecObject ℂ) (μ : AddSpectrum X)
    (hμ : (μ.val).im ∈ Set.Ioc (-Real.pi) Real.pi) :
    multToAdd X (⟨addToMult X μ, by simpa using hμ⟩ : PrincipalAddSpectrum X) = μ := by
  rcases μ with ⟨μ_val, hμprop⟩
  ext
  simp [addToMult, multToAdd]
  have h : -μ_val ≠ 0 := by
    intro h0
    have : μ_val = 0 := by calc
      μ_val = -(-μ_val) := by ring
      _ = 0 := by rw [h0]; ring
    -- 若 μ_val = 0，则 Im(μ_val) = 0 ∈ (-π, π]，不影响；但 exp(-μ_val) = 1 ≠ 0，不影响特征值
    -- 此处仅用于应用 log_exp 的条件
    simp [this]
  have h2 : (exp (-μ_val)).im = 0 := by simp
  -- 使用 log_exp 的主值条件：-μ_val 的虚部在 (-π, π]
  have h3 : (-μ_val).im ∈ Set.Ioc (-Real.pi) Real.pi := by
    simp
    exact hμ
  rw [Complex.log_exp]
  · ring
  · -- 验证 log_exp 的条件
    sorry

/-- M ≅ L：非零乘法谱与主值加法谱作为集合的双射。 -/
noncomputable def spectrumEquiv (X : RecObject ℂ) :
    NonzeroMultSpectrum X ≃ PrincipalAddSpectrum X where
  toFun λnz :=
    let μ := multToAdd X λnz
    ⟨μ, by
      rcases λnz with ⟨λ_val, hλprop, hλnz⟩
      simp [multToAdd]
      -- 复对数主值定义保证 Im(log λ) ∈ (-π, π]
      -- 因此 Im(-log λ) ∈ [-π, π)；严格 (-π, π] 需排除边界
      sorry⟩
  invFun μrange :=
    let λ := addToMult X μrange.val
    ⟨λ, by
      rcases μrange with ⟨μ, hμprop, hμrange⟩
      rcases μ.property with ⟨v, hv, hev⟩
      simp [addToMult]
      intro hλ0
      rw [hλ0] at hev
      simp at hev
      exact hv (by simpa using hev)⟩
  left_inv := by
    intro ⟨λ, hλprop, hλnz⟩
    simp
    ext
    simp [addToMult, multToAdd, exp_log, hλnz]
  right_inv := by
    intro ⟨μ, hμprop, hμrange⟩
    simp
    ext
    simp [addToMult, multToAdd]
    -- 在主值支内 log(exp(-μ)) = -μ
    sorry

end SpectralCorrespondence
