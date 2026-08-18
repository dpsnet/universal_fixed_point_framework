/-
预研形式化：LU 引理 1 的矩阵代数核心（外部理论预研 §7.35）
====================================================================

推进对象：external_theory_presurvey/external_theory_derivation_chain.md §7.35
（LU 严格证明——引理 1：局域幺正不改变 A|B 约化熵）。

mathlib 谱熵工具评估结论（2026-08-17）：
  mathlib **无现成 Hermitian 谱熵工具**——特征值理论（LinearAlgebra.Eigenspace）
  面向代数闭域线性算子的极小多项式根，无"有限维 Hermitian 矩阵 → 特征值向量
  （Fin n → ℝ）+ Real.log 谱熵"的现成组合；有限维矩阵谱分解（eigenvectorMatrix）
  亦未在 Matrix 层提供。⟹ 引理 1 组件 b（谱熵的"幺正保谱 ⟹ 熵不变"）作为
  开放项（待谱分解/矩阵对数库），本文件不形式化。

本文件形式化引理 1 的**矩阵代数核心（组件 a）**：
  部分迹变换律——Tr_B[(U ⊗ V) ρ (U ⊗ V)ᵀ] = U (Tr_B ρ) Uᵀ（V 正交时被部分迹吸收，U 穿越）。
  已机器证明（零 sorry，§7.61 对策实现，v0.33）：定义（partialTrace/kron）+
  kron_transpose + ortho_inner（VᵀV=1 ⟹ Σ_b V b y₁ V b y₂ = δ_{y₁ y₂}）+
  sum_delta_mul/sum_mul_delta/sum_V_inner_delta（δ 吸收、V 内积吸收）+
  sum_reorder_b_inner（三重求和重排：b 移入最内层）+ 主定理 partialTrace_conj_kron
  （部分迹变换律完整机器证明——kron 展开 ⟹ 求和重排 ⟹ V 正交吸收 ⟹ partialTrace 识别
  ⟹ RHS 展开匹配；Lean 障碍分析见推导链 §7.61）。
  （实正交特例（ℝ）；复酉一般化开放。）

  kron：张量积（Kronecker）矩阵；(U ⊗ V)ᵀ = Uᵀ ⊗ Vᵀ；
  partialTrace：部分迹（对 B 求和，对角 b = b'）。
-/

import Mathlib.Data.Real.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Fintype.BigOperators

open scoped BigOperators
open scoped Matrix

namespace PresurveyFormalization.LuInvariant

/-- 部分迹（对 B 求迹）：Tr_B[ρ]_{a,a'} = Σ_b ρ_{(a,b),(a',b)}。 -/
noncomputable def partialTrace {n m : ℕ} (ρ : Matrix (Fin n × Fin m) (Fin n × Fin m) ℝ) :
    Matrix (Fin n) (Fin n) ℝ :=
  fun a a' => ∑ b : Fin m, ρ (a, b) (a', b)

/-- 张量积（Kronecker 积）：(U ⊗ V)_{(a,b),(a',b')} = U a a' * V b b'。 -/
noncomputable def kron {n m : ℕ} (U : Matrix (Fin n) (Fin n) ℝ) (V : Matrix (Fin m) (Fin m) ℝ) :
    Matrix (Fin n × Fin m) (Fin n × Fin m) ℝ :=
  fun (a, b) (a', b') => U a a' * V b b'

/-- kron 转置：(U ⊗ V)ᵀ = Uᵀ ⊗ Vᵀ。 -/
theorem kron_transpose {n m : ℕ} (U : Matrix (Fin n) (Fin n) ℝ) (V : Matrix (Fin m) (Fin m) ℝ) :
    (kron U V)ᵀ = kron Uᵀ Vᵀ := by
  ext x y
  rfl

/-- 正交内积（VᵀV = 1 时）：Σ_b V b y₁ * V b y₂ = δ_{y₁ y₂}。 -/
lemma ortho_inner (V : Matrix (Fin m) (Fin m) ℝ) (hV : Vᵀ * V = 1)
    (y1 y2 : Fin m) :
    (∑ b : Fin m, V b y1 * V b y2) = if y1 = y2 then 1 else 0 := by
  have hvv : (Vᵀ * V) y2 y1 = (1 : Matrix (Fin m) (Fin m) ℝ) y2 y1 :=
    congrFun (congrFun hV y2) y1
  calc
    (∑ b : Fin m, V b y1 * V b y2) = (Vᵀ * V) y2 y1 := by
      rw [Matrix.mul_apply]
      apply Finset.sum_congr rfl
      intro b _
      rw [Matrix.transpose_apply]
      ring
    _ = (1 : Matrix (Fin m) (Fin m) ℝ) y2 y1 := hvv
    _ = if y1 = y2 then 1 else 0 := by
      rw [Matrix.one_apply]
      by_cases h : y2 = y1
      · have h' : y1 = y2 := h.symm
        rw [if_pos h, if_pos h']
      · have h' : y1 ≠ y2 := fun h12 => h h12.symm
        rw [if_neg h, if_neg h']

/-- δ 吸收：Σ_y2 (if y1 = y2 then 1 else 0) * f y2 = f y1。 -/
lemma sum_delta_mul (y1 : Fin m) (f : Fin m → ℝ) :
    (∑ y2 : Fin m, (if y1 = y2 then (1 : ℝ) else 0) * f y2) = f y1 := by
  calc
    (∑ y2 : Fin m, (if y1 = y2 then (1 : ℝ) else 0) * f y2)
        = ∑ y2 : Fin m, (if y1 = y2 then f y2 else 0) := by
          apply Finset.sum_congr rfl
          intro y2 _
          by_cases h : y1 = y2
          · simp [h]
          · simp [h]
    _ = f y1 := by
          -- 转换条件顺序：if y1 = y2 ⟶ if y2 = y1（sum_ite_eq 的 x = a 形式）
          rw [show (∑ y2 : Fin m, (if y1 = y2 then f y2 else 0)) =
                     ∑ y2 : Fin m, (if y2 = y1 then f y2 else 0) by
            apply Finset.sum_congr rfl
            intro y2 _
            by_cases h : y1 = y2
            · rw [if_pos h, if_pos h.symm]
            · rw [if_neg h, if_neg (fun h2 : y2 = y1 => h h2.symm)]
          ]
          simp

/-- δ 在右侧的版本：Σ_y2 f y2 * δ_{y1 y2} = f y1。 -/
lemma sum_mul_delta (y1 : Fin m) (f : Fin m → ℝ) :
    (∑ y2 : Fin m, f y2 * (if y1 = y2 then (1 : ℝ) else 0)) = f y1 := by
  calc
    (∑ y2 : Fin m, f y2 * (if y1 = y2 then (1 : ℝ) else 0))
        = ∑ y2 : Fin m, (if y1 = y2 then (1 : ℝ) else 0) * f y2 := by
          apply Finset.sum_congr rfl
          intro y2 _
          ring
    _ = f y1 := sum_delta_mul y1 f

/-- V 正交内积吸收（Σ_y2 Σ_b 顺序）：Σ_y2 Σ_b f y2 * (V b y1 * V b y2) = f y1。 -/
lemma sum_V_inner_delta (V : Matrix (Fin m) (Fin m) ℝ) (hV : Vᵀ * V = 1)
    (y1 : Fin m) (f : Fin m → ℝ) :
    (∑ y2 : Fin m, ∑ b : Fin m, f y2 * (V b y1 * V b y2)) = f y1 := by
  calc
    (∑ y2 : Fin m, ∑ b : Fin m, f y2 * (V b y1 * V b y2))
        = ∑ y2 : Fin m, f y2 * (∑ b : Fin m, V b y1 * V b y2) := by
          apply Finset.sum_congr rfl
          intro y2 _
          rw [Finset.mul_sum]
    _ = ∑ y2 : Fin m, f y2 * (if y1 = y2 then (1 : ℝ) else 0) := by
          apply Finset.sum_congr rfl
          intro y2 _
          rw [ortho_inner V hV y1 y2]
    _ = f y1 := sum_mul_delta y1 f

/-- 求和重排引理（§7.61 对策机证实现）：∑ b, ∑ x, ∑ x', T b x x' = ∑ x', ∑ x, ∑ b, T b x x'
    （b 从最外层移入最内层）。显式 Finset.sum_comm，不依赖 simp 的不可控执行顺序。 -/
lemma sum_reorder_b_inner {α β γ : Type*} [Fintype α] [Fintype β] [Fintype γ]
    (T : α → β → γ → ℝ) :
    (∑ b : α, ∑ x : β, ∑ x' : γ, T b x x') =
      ∑ x' : γ, ∑ x : β, ∑ b : α, T b x x' := by
  calc
    (∑ b : α, ∑ x : β, ∑ x' : γ, T b x x')
        = ∑ x : β, ∑ b : α, ∑ x' : γ, T b x x' := by
          conv_lhs =>
            rw [Finset.sum_comm]
    _ = ∑ x : β, ∑ x' : γ, ∑ b : α, T b x x' := by
          apply Finset.sum_congr rfl
          intro x _
          conv_lhs =>
            rw [Finset.sum_comm]
    _ = ∑ x' : γ, ∑ x : β, ∑ b : α, T b x x' := by
          conv_lhs =>
            rw [Finset.sum_comm]

/- 引理 1（组件 a，部分迹变换律）——**完整机器证明（零 sorry，§7.61 对策实现，v0.33）**：
    Tr_B[(U ⊗ V) ρ (U ⊗ V)ᵀ] = U (Tr_B ρ) Uᵀ（V 正交时 B 侧被部分迹吸收，U 穿越）。
    证明结构（推导链 §7.61 数学骨架 5 步逐一机证）：
    ① 展开：simp [Matrix.mul_apply] 展开三矩阵积（对 pair 指标）；
    ② 求和重排：sum_reorder_b_inner——Σ_b 从最外层移入最内层（显式 Finset.sum_comm，
       规避 §7.61 记录的 simp 执行顺序不可控问题）；
    ③ V 正交吸收：ortho_inner（VᵀV=1 ⟹ Σ_b V b y₁ V b y₂ = δ_{y₁ y₂}）；
    ④ δ 吸收：sum_mul_delta（Σ_y2 δ_{y1 y2} ρ = ρ_{y1}）+ Fintype.sum_prod_type 分解 pair
       求和（x'=(x1,y1) 外层、x=(x2,y2) 内层，δ 锚定 y1）；
    ⑤ 收拢：Σ_y1 ρ (x1,y1) (x2,y1) = partialTrace ρ x1 x2（定义 rfl）⟹ RHS 展开匹配
       （U * (P * Uᵀ) 关联 + Matrix.mul_apply + transpose_apply + ring）。
-/
theorem partialTrace_conj_kron {n m : ℕ} (U : Matrix (Fin n) (Fin n) ℝ)
    (V : Matrix (Fin m) (Fin m) ℝ) (hV : Vᵀ * V = 1)
    (ρ : Matrix (Fin n × Fin m) (Fin n × Fin m) ℝ) :
    partialTrace (kron U V * ρ * (kron U V)ᵀ) = U * partialTrace ρ * Uᵀ := by
  ext a a'
  calc
    partialTrace (kron U V * ρ * (kron U V)ᵀ) a a'
        = ∑ b : Fin m, ((kron U V * ρ * (kron U V)ᵀ) (a, b) (a', b)) := rfl
    _ = ∑ b : Fin m, ∑ x : Fin n × Fin m, (kron U V * ρ) (a, b) x * (kron U V)ᵀ x (a', b) := by
          simp only [Matrix.mul_apply]
    _ = ∑ b : Fin m, ∑ x : Fin n × Fin m, ∑ x' : Fin n × Fin m,
          (kron U V (a, b) x' * ρ x' x) * (kron U V)ᵀ x (a', b) := by
          apply Finset.sum_congr rfl
          intro b _
          apply Finset.sum_congr rfl
          intro x _
          rw [Matrix.mul_apply]
          rw [Finset.sum_mul]
    _ = ∑ x' : Fin n × Fin m, ∑ x : Fin n × Fin m, ∑ b : Fin m,
          (kron U V (a, b) x' * ρ x' x) * (kron U V)ᵀ x (a', b) := by
          exact sum_reorder_b_inner (fun (b : Fin m) (x : Fin n × Fin m) (x' : Fin n × Fin m) =>
            (kron U V (a, b) x' * ρ x' x) * (kron U V)ᵀ x (a', b))
    _ = ∑ x' : Fin n × Fin m, ∑ x : Fin n × Fin m, ∑ b : Fin m,
          ((U a x'.1 * V b x'.2) * ρ x' x) * (U a' x.1 * V b x.2) := by
          simp only [kron, Matrix.transpose_apply]
    _ = ∑ x' : Fin n × Fin m, ∑ x : Fin n × Fin m,
          (U a x'.1 * U a' x.1 * ρ x' x) * (∑ b : Fin m, V b x'.2 * V b x.2) := by
          apply Finset.sum_congr rfl
          intro x' _
          apply Finset.sum_congr rfl
          intro x _
          calc
            (∑ b : Fin m, ((U a x'.1 * V b x'.2) * ρ x' x) * (U a' x.1 * V b x.2))
                = ∑ b : Fin m, (U a x'.1 * U a' x.1 * ρ x' x) * (V b x'.2 * V b x.2) := by
                  apply Finset.sum_congr rfl
                  intro b _
                  ring
            _ = (U a x'.1 * U a' x.1 * ρ x' x) * (∑ b : Fin m, V b x'.2 * V b x.2) := by
                  rw [Finset.mul_sum]
    _ = ∑ x' : Fin n × Fin m, ∑ x : Fin n × Fin m,
          (U a x'.1 * U a' x.1 * ρ x' x) * (if x'.2 = x.2 then 1 else 0) := by
          apply Finset.sum_congr rfl
          intro x' _
          apply Finset.sum_congr rfl
          intro x _
          rw [ortho_inner V hV x'.2 x.2]
    _ = ∑ x1 : Fin n, ∑ y1 : Fin m, ∑ x2 : Fin n, ∑ y2 : Fin m,
          (U a x1 * U a' x2 * ρ (x1, y1) (x2, y2)) * (if y1 = y2 then 1 else 0) := by
          simp only [Fintype.sum_prod_type]
    _ = ∑ x1 : Fin n, ∑ y1 : Fin m, ∑ x2 : Fin n,
          (U a x1 * U a' x2) * ρ (x1, y1) (x2, y1) := by
          apply Finset.sum_congr rfl
          intro x1 _
          apply Finset.sum_congr rfl
          intro y1 _
          apply Finset.sum_congr rfl
          intro x2 _
          calc
            (∑ y2 : Fin m, (U a x1 * U a' x2 * ρ (x1, y1) (x2, y2)) * (if y1 = y2 then 1 else 0))
                = (U a x1 * U a' x2) * (∑ y2 : Fin m, ρ (x1, y1) (x2, y2) * (if y1 = y2 then 1 else 0)) := by
                  rw [Finset.mul_sum]
                  apply Finset.sum_congr rfl
                  intro y2 _
                  ring
            _ = (U a x1 * U a' x2) * ρ (x1, y1) (x2, y1) := by
                  rw [sum_mul_delta y1 (fun y2 => ρ (x1, y1) (x2, y2))]
    _ = ∑ x1 : Fin n, ∑ x2 : Fin n, ∑ y1 : Fin m,
          (U a x1 * U a' x2) * ρ (x1, y1) (x2, y1) := by
          apply Finset.sum_congr rfl
          intro x1 _
          conv_lhs =>
            rw [Finset.sum_comm]
    _ = ∑ x1 : Fin n, ∑ x2 : Fin n,
          (U a x1 * U a' x2) * (∑ y1 : Fin m, ρ (x1, y1) (x2, y1)) := by
          apply Finset.sum_congr rfl
          intro x1 _
          apply Finset.sum_congr rfl
          intro x2 _
          rw [Finset.mul_sum]
    _ = ∑ x1 : Fin n, ∑ x2 : Fin n, (U a x1 * U a' x2) * partialTrace ρ x1 x2 := by
          apply Finset.sum_congr rfl
          intro x1 _
          apply Finset.sum_congr rfl
          intro x2 _
          rfl
    _ = (U * partialTrace ρ * Uᵀ) a a' := by
          symm
          calc
            (U * partialTrace ρ * Uᵀ) a a'
                = ∑ x2 : Fin n, ∑ x1 : Fin n, U a x1 * partialTrace ρ x1 x2 * U a' x2 := by
                  simp only [Matrix.mul_apply, Matrix.transpose_apply, Finset.sum_mul, mul_assoc]
            _ = ∑ x1 : Fin n, ∑ x2 : Fin n, U a x1 * partialTrace ρ x1 x2 * U a' x2 := by
                  conv_lhs =>
                    rw [Finset.sum_comm]
            _ = ∑ x1 : Fin n, ∑ x2 : Fin n, (U a x1 * U a' x2) * partialTrace ρ x1 x2 := by
                  apply Finset.sum_congr rfl
                  intro x1 _
                  apply Finset.sum_congr rfl
                  intro x2 _
                  ring

end PresurveyFormalization.LuInvariant
