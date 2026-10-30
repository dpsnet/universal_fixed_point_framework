/- 
# SingleMinusAnchorSum.lean

Phase 77 M37/M38 核心发现形式化（arXiv:2602.12176v2 单负剥离振幅）

**动量双守恒括号恒等式（恒等式 A）**：对任何锚 k，
动量守恒（Σω = 0、Σωz = 0）⇒

    Σ_{j≠k} P[k][j] = Σ_{j∈univ.erase k} ω_k ω_j (z_k − z_j) = 0

物理意义：任何粒子的"锚定单对括号和"数学恒 0——
跨 n=6..11 数值 102000 检验 0 偏差（M38）——
全补块恒 0 定理（M42 已 Lean 闭合）的直接推广。

证明（纯代数）：
1. 线性展开：Σ_{j≠k} ω_k ω_j (z_k−z_j) = ω_k [z_k Σ_{j≠k} ω_j − Σ_{j≠k} ω_j z_j]
2. erase 求和：Σ_{j≠k} ω_j = −ω_k、Σ_{j≠k} ω_j z_j = −ω_k z_k（sum_erase_add）
3. 代入：ω_k [z_k(−ω_k) − (−ω_k z_k)] = 0

状态：全闭（零 sorry）。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Data.Int.Basic
import Mathlib.Tactic

noncomputable section
open scoped BigOperators
open BigOperators

namespace SingleMinusAnchorSum

/-- 锚 k 的单对括号和：Σ_{j≠k} ω_k ω_j (z_k − z_j) -/
def anchorSum {n : ℕ} (ω z : Fin n → ℝ) (k : Fin n) : ℝ :=
  ∑ j ∈ Finset.univ.erase k, ω k * ω j * (z k - z j)

/-- 线性展开：Σ_{j≠k} ω_k ω_j (z_k−z_j)
    = ω_k [z_k Σ_{j≠k} ω_j − Σ_{j≠k} ω_j z_j] -/
lemma anchorSum_lin {n : ℕ} (ω z : Fin n → ℝ) (k : Fin n) :
    anchorSum ω z k =
      ω k * (z k * (∑ j ∈ Finset.univ.erase k, ω j) -
        (∑ j ∈ Finset.univ.erase k, ω j * z j)) := by
  unfold anchorSum
  calc
    ∑ j ∈ Finset.univ.erase k, (ω k * ω j * (z k - z j))
        = ∑ j ∈ Finset.univ.erase k, (ω k * (z k * ω j - ω j * z j)) := by
          apply Finset.sum_congr rfl
          intro j hj
          ring
    _ = ω k * (∑ j ∈ Finset.univ.erase k, (z k * ω j - ω j * z j)) := by
          rw [← Finset.mul_sum]
    _ = ω k * (z k * (∑ j ∈ Finset.univ.erase k, ω j) -
          (∑ j ∈ Finset.univ.erase k, ω j * z j)) := by
          congr 1
          rw [Finset.sum_sub_distrib]
          congr 1
          rw [← Finset.mul_sum]

/-- 动量双守恒恒等式 A：任何锚 k 的单对括号和恒 0 -/
theorem anchor_sum_zero {n : ℕ} (ω z : Fin n → ℝ) (k : Fin n)
    (hsum : ∑ i : Fin n, ω i = 0)
    (hmom : ∑ i : Fin n, ω i * z i = 0) :
    anchorSum ω z k = 0 := by
  -- erase 求和：Σ_{j≠k} ω = -ω k
  have herase : (∑ j ∈ Finset.univ.erase k, ω j) = - ω k := by
    have hUA : (∑ j ∈ Finset.univ.erase k, ω j) + ω k = 0 := by
      rw [Finset.sum_erase_add _ (fun j => ω j) (Finset.mem_univ k)]
      exact hsum
    linarith
  -- erase 求和：Σ_{j≠k} ωz = -ω k * z k
  have hmom_erase : (∑ j ∈ Finset.univ.erase k, ω j * z j) = - (ω k * z k) := by
    have hUA : (∑ j ∈ Finset.univ.erase k, ω j * z j) + (ω k * z k) = 0 := by
      rw [Finset.sum_erase_add _ (fun j => ω j * z j) (Finset.mem_univ k)]
      exact hmom
    linarith
  rw [anchorSum_lin ω z k, herase, hmom_erase]
  ring

end SingleMinusAnchorSum
