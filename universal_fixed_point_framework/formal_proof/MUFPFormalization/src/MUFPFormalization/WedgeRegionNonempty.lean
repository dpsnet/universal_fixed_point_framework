import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Algebra.Order.Field.Basic
import Mathlib.Topology.Algebra.Order.Field
import Mathlib.Data.Real.Basic

/-!
# P2-B 可机检判据 C1：de Sitter 楔形区非空性

对应 `notes/04_lorentz_gravity/dS符号论证_笔记.md` §4 判据 C1：在 ℝ^{n,1}（号差 (−,+,...,+)）中，
类空嵌入双曲面 X^A X_A = +H⁻² 的楔形区 W_j = {X^j > |X^0|} 非空。

- 号差约定：X^A X_A = −(X⁰)² + Σ_{i=1}^n (X^i)²（2310.12185 §2，dS 嵌入 X^A X_A = H⁻²）；
- 显式构造：X⁰ = 0、X^j = H⁻¹（j 固定空间方向）、其余 0：
  验证 −0² + (H⁻¹)² = H⁻² ∧ H⁻¹ > |0| —— 需要 H > 0（hH）；
- 意义：Λ 的符号论证把落点放在 C1（楔形区存在性），AdS 类时嵌入（−H⁻²）无该结构
  （C2 候选，见笔记 §6）。本文件只形式化 dS 侧的存在性（C1），不产生新物理。

零 sorry 政策：本文件不含 sorry。
-/

namespace MUFPF.WedgeRegion

open scoped BigOperators

/-- C1：类空嵌入双曲面上的楔形区 W_j = {X^j > |X^0|} 非空（n 空间维，j : Fin n 固定楔方向）。
    显式构造：X⁰ = 0，X^j = H⁻¹，其余空间坐标 0。 -/
theorem dS_wedge_region_nonempty {n : ℕ} (j : Fin n) (H : ℝ) (hH : 0 < H) :
    ∃ x0 : ℝ, ∃ x : Fin n → ℝ,
      -x0 ^ 2 + (∑ i : Fin n, (x i) ^ 2) = (H ^ 2)⁻¹ ∧ x j > |x0| := by
  refine ⟨0, fun i => if i = j then H⁻¹ else 0, ?_⟩
  constructor
  · have hsum : (∑ i : Fin n, (if i = j then H⁻¹ else 0) ^ 2) = (H⁻¹) ^ 2 := by
      rw [Fintype.sum_eq_single j]
      · simp
      · intro b hb
        simp [hb]
    rw [hsum]
    rw [inv_pow]
    simp
  · simp
    exact hH

/-- 推论（数值自检用）：n=3（ℝ^{3,1}，物理时空维 4）、H>0 时楔形区非空。 -/
theorem dS_wedge_region_nonempty_3plus1 (j : Fin 3) (H : ℝ) (hH : 0 < H) :
    ∃ x0 : ℝ, ∃ x : Fin 3 → ℝ,
      -x0 ^ 2 + (∑ i : Fin 3, (x i) ^ 2) = (H ^ 2)⁻¹ ∧ x j > |x0| :=
  dS_wedge_region_nonempty j H hH

end MUFPF.WedgeRegion
