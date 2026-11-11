/-
PR-634 · R2 单块特例：相交点的上界（迹论证）

第 15 批给出的数值依据是 `‖K @ vec I‖ = 1.732 = √3 = ‖vec I‖`（`I` 在 `range` 上的
投影全被投掉 ⇒ `I ∉ range`）。这里给出**不依赖任何浮点计算**的初等机检路径：

  交换子的迹恒为 0，而 `tr(I₃) = 3 ≠ 0` ⇒ `I₃ ∉ range(ad_{J₃})`。

**为什么单独建模块**：`import Mathlib.LinearAlgebra.Matrix.Trace` 会给
`SpLayerSeparability` 既有的 `simpa` / `simp` 链带来扰动（实测 6 处
`Type mismatch: After simplification` + 8 条 `unused simp argument` 警告），
故把迹论证隔离在本模块，主模块的化简链保持原样。

**仍未机检的一步**：`ker(ad_{J₃}) ⊆ span{I₃, J₃, J₃²}`（即 `dim ker ≤ 3`）。
补上它才能把「交集 ⊆ span{J₃, J₃²}」接成完整的 `dim = 2`。
-/
import MUFPFormalization.SpLayerSeparability
import Mathlib.LinearAlgebra.Matrix.Trace

namespace MUFPFormalization

/-- 交换子的迹恒为 0：`trace(A * X - X * A) = 0`。
    依据 `Matrix.trace_sub` 与 `Matrix.trace_mul_comm`（循环性）。 -/
theorem adLin_trace_eq_zero (A X : Matrix (Fin 3) (Fin 3) ℂ) :
    Matrix.trace (adLin A X) = 0 := by
  change Matrix.trace (A * X - X * A) = 0
  rw [Matrix.trace_sub, Matrix.trace_mul_comm A X]
  simp

/-- **B 相相交点的上界关键步**：`I₃ ∉ range(ad_{J₃})`。

    若 `I₃ = [J₃, X]`，取迹得 `tr(I₃) = 0`；而 `tr(I₃) = 3`，矛盾。
    于是 `ker ⊓ range` 中 `I₃` 方向的系数必为 0 ⇒ 交集落在 `span{J₃, J₃²}` 内。 -/
theorem jordan3_identity_not_mem_range :
    (1 : Matrix (Fin 3) (Fin 3) ℂ) ∉ LinearMap.range (adLin jordan3) := by
  intro h
  rcases LinearMap.mem_range.mp h with ⟨X, hX⟩
  have htr := adLin_trace_eq_zero jordan3 X
  rw [hX] at htr
  rw [Matrix.trace_one] at htr
  norm_num at htr

end MUFPFormalization
