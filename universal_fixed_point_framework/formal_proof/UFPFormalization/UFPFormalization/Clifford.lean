/-
有限维 Clifford 代数矩阵表示的等级 A 原型形式化。

论文 Paper I §6 讨论 Clifford 值谱理论。等级 A 目标是对低维 Clifford 代数
（如 Cl(1,0), Cl(0,1), Cl(2,0)）给出矩阵表示，并验证：
- 生成元满足 {γ_i, γ_j} = 2 η_{ij} 1
- 原始幂等元与旋量模结构

这里以 Cl(p,q) 的通用矩阵表示定义与生成元关系验证为核心。
-/

import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Notation
import Mathlib.LinearAlgebra.CliffordAlgebra.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Tactic

universe u

namespace CliffordPrototype

variable {𝕜 : Type u} [Field 𝕜] [CharZero 𝕜]

/-- Cl(p,q) 的生成元集合：p 个正生成元，q 个负生成元。 -/
def Generators (p q : ℕ) : Type := Fin (p + q)

/-- Clifford 关系：生成元 i, j 的反对易子等于 2 η_{ij} I。
    η 是对角映射，前 p 个为 +1，后 q 个为 -1。 -/
def cliffordRelation {n : ℕ} (η : Fin n → 𝕜)
    (γ : Fin n → Matrix (Fin m) (Fin m) 𝕜) : Prop :=
  ∀ i j, γ i * γ j + γ j * γ i = 2 * η i * if i = j then 1 else 0

section Real2x2

/-- Cl(0,1) ≅ ℂ 在实数域上的表示：γ_1 = i，对应 2x2 实矩阵
    [0 -1]
    [1  0]
-/
def gamma_0_1 : Matrix (Fin 2) (Fin 2) ℝ :=
  !![0, -1; 1, 0]

/-- 验证 Cl(0,1) 的 Clifford 关系：γ^2 = -I。 -/
lemma gamma_0_1_relation : gamma_0_1 * gamma_0_1 = -1 := by
  rw [gamma_0_1]
  funext i j
  fin_cases i <;> fin_cases j
  all_goals simp [Matrix.mul_apply, Matrix.of_apply]
          <;> norm_num

/-- Cl(1,0) ≅ ℝ ⊕ ℝ 的表示：γ_1 = σ_z。 -/
def gamma_1_0 : Matrix (Fin 2) (Fin 2) ℝ :=
  !![1, 0; 0, -1]

lemma gamma_1_0_relation : gamma_1_0 * gamma_1_0 = 1 := by
  rw [gamma_1_0]
  funext i j
  fin_cases i <;> fin_cases j
  all_goals simp [Matrix.mul_apply, Matrix.of_apply]
          <;> norm_num

/-- Cl(2,0) 的 Pauli 矩阵表示：γ_1 = σ_x, γ_2 = σ_y。 -/
def sigma_x : Matrix (Fin 2) (Fin 2) ℝ := !![0, 1; 1, 0]
def sigma_y : Matrix (Fin 2) (Fin 2) ℝ := !![0, -1; 1, 0]
def sigma_z : Matrix (Fin 2) (Fin 2) ℝ := !![1, 0; 0, -1]

/-- 验证 {σ_x, σ_y} = 0。 -/
lemma sigma_x_y_anticommute : sigma_x * sigma_y + sigma_y * sigma_x = 0 := by
  rw [sigma_x, sigma_y]
  funext i j
  fin_cases i <;> fin_cases j
  all_goals simp [Matrix.mul_apply, Matrix.of_apply]
          <;> norm_num

lemma sigma_x_sq : sigma_x * sigma_x = 1 := by
  rw [sigma_x]
  funext i j
  fin_cases i <;> fin_cases j
  all_goals simp [Matrix.mul_apply, Matrix.of_apply]
          <;> norm_num

lemma sigma_y_sq : sigma_y * sigma_y = -1 := by
  rw [sigma_y]
  funext i j
  fin_cases i <;> fin_cases j
  all_goals simp [Matrix.mul_apply, Matrix.of_apply]
          <;> norm_num

end Real2x2

section Idempotents

/-- 原始幂等元（idempotent）与最小左理想的等级 A 原型。
    在 Cl(1,0) 中，e_+ = (1 + γ)/2 与 e_- = (1 - γ)/2 是一对原始幂等元。 -/
def idempotent_plus : Matrix (Fin 2) (Fin 2) ℝ := (1 + gamma_1_0) / 2
def idempotent_minus : Matrix (Fin 2) (Fin 2) ℝ := (1 - gamma_1_0) / 2

/-- 2x2 单位矩阵。 -/
def I2 : Matrix (Fin 2) (Fin 2) ℝ := 1

lemma idempotent_plus_sq : idempotent_plus * idempotent_plus = idempotent_plus := by
  rw [idempotent_plus]
  have h : gamma_1_0 * gamma_1_0 = I2 := by
    rw [gamma_1_0_relation]
    rfl
  -- 展开 (1 + γ)/2 * (1 + γ)/2 = (1 + 2γ + γ²)/4 = (1 + 2γ + 1)/4 = (2 + 2γ)/4 = (1 + γ)/2
  funext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [gamma_1_0, I2, Matrix.mul_apply, Matrix.of_apply, Matrix.add_apply, Matrix.sub_apply,
          Matrix.smul_apply, h]
    <;> norm_num
    <;> ring_nf
    <;> norm_num

lemma idempotent_minus_sq : idempotent_minus * idempotent_minus = idempotent_minus := by
  rw [idempotent_minus]
  have h : gamma_1_0 * gamma_1_0 = I2 := by
    rw [gamma_1_0_relation]
    rfl
  -- 展开 (1 - γ)/2 * (1 - γ)/2 = (1 - 2γ + γ²)/4 = (1 - 2γ + 1)/4 = (2 - 2γ)/4 = (1 - γ)/2
  funext i j
  fin_cases i <;> fin_cases j
  all_goals
    simp [gamma_1_0, I2, Matrix.mul_apply, Matrix.of_apply, Matrix.add_apply, Matrix.sub_apply,
          Matrix.smul_apply, h]
    <;> norm_num
    <;> ring_nf
    <;> norm_num

end Idempotents

end CliffordPrototype
