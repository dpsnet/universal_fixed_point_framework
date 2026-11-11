/-
PR-634 · R2 单块特例：相交点的显式结构（`dim = 2` 的结构版闭合）

三块拼接：
  1. `SpJ3KernelBound.jordan3_ker_mem_span`：`R ∈ ker ⇒ R = R₀₀ • I + R₀₁ • J + R₀₂ • J²`；
  2. `SpJ3TraceBound.adLin_trace_eq_zero`：交换子迹恒零 ⇒ `R ∈ range ⇒ trace R = 0`；
  3. `trace R = 3 * R₀₀`（由 1 展开 + `trace I = 3`、`trace J = trace J² = 0`）。
⇒ `R₀₀ = 0` ⇒ `R = R₀₁ • J + R₀₂ • J²`，即 `ker ⊓ range ⊆ span{J₃, J₃²}`。

配合 `SpLayerSeparability.jordan3_ker_inf_range_contains_two_independent`（`dim ≥ 2`）
⇒ 交集恰为 `span{J₃, J₃²}`，维数 `= 2`。这是 R2 单块 `n = 3` 的**结构版等式闭合**，
且全程零浮点，与数值侧（`rank ad_J = 6`、闭式 `n − #blocks = 3 − 1 = 2`）一致。
-/
import MUFPFormalization.SpJ3TraceBound
import MUFPFormalization.SpJ3KernelBound

namespace MUFPFormalization

/-- **R2 单块 `n = 3` 的相交点结构**：`ker ⊓ range` 中任何元素都落在 `span{J₃, J₃²}` 内。
    于是该交集维数 `≤ 2`；与 `dim ≥ 2` 合起来给出 `dim = 2`。 -/
theorem jordan3_ker_inf_range_mem_span (R : Matrix (Fin 3) (Fin 3) ℂ)
    (h : R ∈ LinearMap.ker (adLin jordan3) ⊓ LinearMap.range (adLin jordan3)) :
    ∃ b c : ℂ, R = b • jordan3 + c • jordan3Sq := by
  obtain ⟨hk, hr⟩ := Submodule.mem_inf.mp h
  -- 1. ker ⇒ 显式多项式形式
  have hspan := jordan3_ker_mem_span R hk
  -- 2. range ⇒ 迹为零
  have htr : Matrix.trace R = 0 := by
    obtain ⟨X, hX⟩ := LinearMap.mem_range.mp hr
    rw [← hX]
    exact adLin_trace_eq_zero jordan3 X
  -- 3. 展开形式的迹 = 3 * R₀₀（只改左侧，避免 hspan 误重写 R₀₁/R₀₂）
  have htr2 : Matrix.trace R = 3 * R 0 0 := by
    conv_lhs => rw [hspan]
    rw [Matrix.trace_add, Matrix.trace_add, Matrix.trace_smul, Matrix.trace_smul,
      Matrix.trace_smul, Matrix.trace_one]
    simp [jordan3, jordan3Sq, Matrix.trace, Matrix.of_apply, Fin.sum_univ_three]
    ring
  have h3 : (3 : ℂ) ≠ 0 := by norm_num
  have ha : R 0 0 = 0 := by
    have h0 : (3 : ℂ) * R 0 0 = 0 := by rw [← htr2, htr]
    exact (mul_eq_zero.mp h0).resolve_left h3
  refine ⟨R 0 1, R 0 2, ?_⟩
  conv_lhs => rw [hspan, ha]
  simp [smul_eq_mul, zero_smul]

end MUFPFormalization
