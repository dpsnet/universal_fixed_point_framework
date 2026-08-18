/-
预研形式化：R 重构唯一性（外部理论预研 §7.56）
====================================================================

推进对象：external_theory_presurvey/external_theory_derivation_chain.md §7.56
（R 唯一性严格定义：谱像忠实性 = 谱定理 + 分支结构）。

命题（§7.56）：R 从谱像唯一重构——给定谱像（特征值向量 d）+ 分支结构
（特征子空间），对角算子 A = Matrix.diagonal d 在么正等价意义下唯一。

形式化范围（诚实标注）：
  本节形式化重构唯一性的**代数核心**（v0.34 补谱投影层）：
    ① `diagonal_injective`：Matrix.diagonal 单射——谱像（特征值向量）⟹
       对角算子唯一（R 重构唯一性的基础）；
    ② `spectrum_determines_operator`：同一算子的两个对角实现必有相同
       特征值向量（R 重构唯一性：谱像忠实性）；
    ③ `spectral_projection_unique`/`spectral_projection_exists_unique`：**特征
       子空间直和 ⟹ 谱投影唯一**（v0.34，§7.64 完整形式化）——分支 i 的谱投影
       （像 = span{e_i}、零化其余分支）唯一确定 = E_ii = diag(δ_ij)；"分支结构
       ⟹ 投影唯一"的投影层闭环（§7.56 开放项"对角实现 + 特征子空间直和
       ⟹ 投影唯一"闭合）；
  §7.15 A3 严格化已机证分支 = 1 维特征子空间（`branch_eigenspace_eq_span`），
  提供分支结构 = 特征子空间的机证支撑（引用，不重复）；
  "分支结构 = 时间位置"（§7.54/§7.55）为候选，不在此形式化。
-/

import Mathlib.Data.Real.Basic
import Mathlib.Data.Matrix.Diagonal

open scoped Matrix

namespace PresurveyFormalization.RUniqueness

/-- 分支索引：16 个分支（§7.15 A3：旋量空间 S ≅ ℝ¹⁶ 谱分解）。 -/
abbrev Branch := Fin 16

/-- 谱像：特征值向量 d 决定对角算子（§7.56：谱像 = 特征值多重集）。 -/
def SpectralOperator (d : Branch → ℝ) : Matrix Branch Branch ℝ :=
  Matrix.diagonal d

/--
R 重构唯一性的基础（§7.56 步骤 1）：Matrix.diagonal 单射——
谱像（特征值向量 d）唯一确定对角算子。
-/
theorem diagonal_injective :
    Function.Injective (Matrix.diagonal : (Branch → ℝ) → Matrix Branch Branch ℝ) := by
  intro d₁ d₂ h
  funext i
  have hii : Matrix.diagonal d₁ i i = Matrix.diagonal d₂ i i := by
    exact congrFun (congrFun h i) i
  simpa [Matrix.diagonal] using hii

/--
R 重构唯一性（§7.56 步骤 4）：同一算子 A 的两个对角实现必有相同特征值
向量（谱像忠实性）——从谱像重构的算子唯一。
-/
theorem spectrum_determines_operator (A : Matrix Branch Branch ℝ)
    (d₁ d₂ : Branch → ℝ) (h₁ : A = Matrix.diagonal d₁) (h₂ : A = Matrix.diagonal d₂) :
    d₁ = d₂ := by
  rw [h₁] at h₂
  exact diagonal_injective h₂

/--
谱像 ⟹ 算子唯一（§7.56 时间性版本的代数核心）：相同特征值向量 d 决定
唯一对角算子——特征值（尺度）+ 分支结构（特征子空间）⟹ 唯一重构。
-/
theorem spectral_operator_unique (d : Branch → ℝ) :
    ∃! A : Matrix Branch Branch ℝ, A = Matrix.diagonal d := by
  refine ⟨Matrix.diagonal d, rfl, ?_⟩
  intro A hA
  exact hA

/--
分支 i 的谱投影（标准基投影 E_ii）：像 = span{e_i}、零化其余分支。
-/
def branchProjection (i : Branch) : Matrix Branch Branch ℝ :=
  fun j k => if j = i ∧ k = i then (1 : ℝ) else 0

/--
谱投影唯一（§7.56 完整形式化，v0.34）：特征子空间直和 ⟹ 投影唯一。
分支 i 的谱投影 P（作用于分支 i = 恒等、零化其余分支——即像 = span{e_i} =
分支 i 的特征子空间（A3 机证 `branch_eigenspace_eq_span`）、核含其余分支）唯一
确定 = 标准基投影 E_ii。这正是"R 从谱像 + 分支结构唯一重构"的投影层内容：
分支结构（特征子空间直和）⟹ 每个分支的谱投影唯一。
-/
theorem spectral_projection_unique (i : Branch) (P : Matrix Branch Branch ℝ)
    (hP_on : ∀ j : Branch, P j i = if j = i then (1 : ℝ) else 0)
    (hP_off : ∀ k j : Branch, j ≠ i → P k j = 0) :
    P = branchProjection i := by
  ext j k
  by_cases h : k = i
  · subst k
    rw [hP_on]
    by_cases hj : j = i
    · simp [branchProjection, hj]
    · simp [branchProjection, hj]
  · rw [hP_off j k h]
    by_cases jk : j = k
    · have hji : j ≠ i := fun hji => h (by rw [jk.symm]; exact hji)
      simp [branchProjection, hji]
    · by_cases ji : j = i
      · have hki : k ≠ i := fun hki => jk (by rw [ji, hki])
        simp [branchProjection, ji, hki]
      · simp [branchProjection, ji]

/--
谱投影存在唯一（§7.56 完整形式化）：分支 i 的谱投影存在且唯一。
（存在性 = 标准基投影 E_ii 满足像/核条件；唯一性 = `spectral_projection_unique`。）
-/
theorem spectral_projection_exists_unique (i : Branch) :
    ∃! P : Matrix Branch Branch ℝ,
      (∀ j : Branch, P j i = if j = i then (1 : ℝ) else 0) ∧
      (∀ k j : Branch, j ≠ i → P k j = 0) := by
  refine ⟨branchProjection i, ⟨?_, ?_⟩, ?_⟩
  · intro j
    by_cases hj : j = i
    · simp [branchProjection, hj]
    · simp [branchProjection, hj]
  · intro k j hj
    by_cases jk : k = j
    · have hki : k ≠ i := fun hki => hj (by rw [jk.symm]; exact hki)
      simp [branchProjection, hki]
    · by_cases ki : k = i
      · have hji : j ≠ i := fun hji => jk (by rw [hji, ki])
        simp [branchProjection, ki, hji]
      · simp [branchProjection, ki]
  · intro P hP
    exact spectral_projection_unique i P hP.1 hP.2

end PresurveyFormalization.RUniqueness
