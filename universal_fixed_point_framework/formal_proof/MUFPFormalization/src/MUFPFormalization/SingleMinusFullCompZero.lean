/- 
# SingleMinusFullCompZero.lean

Phase 77 M38/M39 推论形式化（arXiv:2602.12176v2 单负剥离振幅）

**全补块恒 0 定理**：对任何 A ⊂ 粒子集，B = 全粒子 \ A，
动量守恒（Σω = 0、Σωz = 0）⇒ 括号积

    [Σ_A, Σ_B] = Σ_{a∈A} Σ_{b∈B} ω_a ω_b (z_a − z_b) = 0

物理意义：前缀块 vs 全补块的符号因子数学恒 0——"守恒的零模式"——
不携带判据信息（Paper 58 谱维数修正的核心，见笔记 §五十四/§五十五）。

证明（纯代数）：
1. 双求和线性展开：[A,B] = (Σ_A ωz)(Σ_B ω) − (Σ_A ω)(Σ_B ωz)
2. 补集求和：Σ_B ω = −Σ_A ω（Σ_univ ω = 0 + 并集拆分）
3. 补集求和：Σ_B ωz = −Σ_A ωz（Σ_univ ωz = 0 + 并集拆分）
4. 代入：= (Σ_A ωz)(−Σ_A ω) − (Σ_A ω)(−(Σ_A ωz)) = 0

数值先证伪（M38/M39）：n=6..11 动量双守恒恒等式 102000 检验 0 偏差；
n=11 全补块阈值化 50000 检验全 0。

状态：全闭（零 sorry）。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Data.Int.Basic
import Mathlib.Tactic

noncomputable section
open scoped BigOperators
open BigOperators

namespace SingleMinusFullCompZero

/-- 括号积 [A,B] = Σ_{a∈A} Σ_{b∈B} ω_a ω_b (z_a − z_b) -/
def bracket {n : ℕ} (ω z : Fin n → ℝ) (A B : Finset (Fin n)) : ℝ :=
  ∑ a ∈ A, ∑ b ∈ B, ω a * ω b * (z a - z b)

/-- 双求和线性展开：∑_{a∈A} ∑_{b∈B} ωa ωb (za−zb)
    = (Σ_A ωz)(Σ_B ω) − (Σ_A ω)(Σ_B ωz) -/
lemma bracket_split {n : ℕ} (ω z : Fin n → ℝ) (A B : Finset (Fin n)) :
    bracket ω z A B =
      (∑ a ∈ A, ω a * z a) * (∑ b ∈ B, ω b) -
        (∑ a ∈ A, ω a) * (∑ b ∈ B, ω b * z b) := by
  unfold bracket
  calc
    ∑ a ∈ A, ∑ b ∈ B, (ω a * ω b * (z a - z b))
        = ∑ a ∈ A, ∑ b ∈ B, ((ω a * z a * ω b) - (ω a * ω b * z b)) := by
          apply Finset.sum_congr rfl
          intro a ha
          apply Finset.sum_congr rfl
          intro b hb
          ring
    _ = ∑ a ∈ A, ((∑ b ∈ B, ω a * z a * ω b) - (∑ b ∈ B, ω a * ω b * z b)) := by
          apply Finset.sum_congr rfl
          intro a ha
          exact Finset.sum_sub_distrib (fun b => ω a * z a * ω b) (fun b => ω a * ω b * z b)
    _ = ∑ a ∈ A, (((ω a * z a) * (∑ b ∈ B, ω b)) - (ω a * (∑ b ∈ B, ω b * z b))) := by
          apply Finset.sum_congr rfl
          intro a ha
          congr 1
          · rw [← Finset.mul_sum]
          · have hcomb : (fun b => ω a * ω b * z b) = (fun b => ω a * (ω b * z b)) := by
              funext b
              ring
            rw [hcomb, ← Finset.mul_sum]
    _ = (∑ a ∈ A, (ω a * z a) * (∑ b ∈ B, ω b)) -
          (∑ a ∈ A, ω a * (∑ b ∈ B, ω b * z b)) := by
          exact Finset.sum_sub_distrib
            (fun a => (ω a * z a) * (∑ b ∈ B, ω b)) (fun a => ω a * (∑ b ∈ B, ω b * z b))
    _ = (∑ a ∈ A, ω a * z a) * (∑ b ∈ B, ω b) -
          (∑ a ∈ A, ω a) * (∑ b ∈ B, ω b * z b) := by
          congr 1
          · rw [← Finset.sum_mul]
          · rw [← Finset.sum_mul]

/-- 全补块恒 0 定理：A∪B = univ、A∩B = ∅、Σω = 0、Σωz = 0 ⇒ [A,B] = 0 -/
theorem fullcomp_zero {n : ℕ} (ω z : Fin n → ℝ) (A B : Finset (Fin n))
    (hdisj : Disjoint A B)
    (hcover : A ∪ B = Finset.univ)
    (hsum : ∑ i : Fin n, ω i = 0)
    (hmom : ∑ i : Fin n, ω i * z i = 0) :
    bracket ω z A B = 0 := by
  -- 补集求和：Σ_B ω = -Σ_A ω
  have hsumB : (∑ b ∈ B, ω b) = - (∑ a ∈ A, ω a) := by
    have hUA : (∑ i : Fin n, ω i) = (∑ i ∈ A, ω i) + (∑ i ∈ B, ω i) := by
      rw [← hcover, Finset.sum_union hdisj]
    linarith
  -- 补集求和：Σ_B ωz = -Σ_A ωz
  have hmomB : (∑ b ∈ B, ω b * z b) = - (∑ a ∈ A, ω a * z a) := by
    have hUA : (∑ i : Fin n, ω i * z i) = (∑ i ∈ A, ω i * z i) + (∑ i ∈ B, ω i * z i) := by
      rw [← hcover, Finset.sum_union hdisj]
    linarith
  rw [bracket_split ω z A B, hsumB, hmomB]
  ring

end SingleMinusFullCompZero
