/-
PR-634 · R2 单块特例：`dim ker ≤ 3`（R2 等式闭合的最后一步）

`[J₃, X] = 0` 给出 9 个元素方程，其中 6 个有效方程恰好锁定
`X = X₀₀ • I₃ + X₀₁ • J₃ + X₀₂ • J₃²`。手推（`[J,X] i j = X (i+1) j − X i (j−1)`）：

  (0,0): X₁₀ = 0        (0,1): X₁₁ = X₀₀      (0,2): X₁₂ = X₀₁
  (1,0): X₂₀ = 0        (1,1): X₂₁ = X₁₀ = 0  (1,2): X₂₂ = X₁₁ = X₀₀
  (2,*): 恒等（3 条非约束）

⇒ `ker(ad_{J₃}) ⊆ span{I₃, J₃, J₃²}`，维数 `≤ 3`。
配合 `SpJ3TraceBound.jordan3_identity_not_mem_range`（`I₃ ∉ range`）
⇒ `ker ⊓ range ⊆ span{J₃, J₃²}` ⇒ `dim ≤ 2`；
配合 `SpLayerSeparability.jordan3_ker_inf_range_contains_two_independent`（`dim ≥ 2`）
⇒ `dim = 2`，与数值侧（`rank ad_J = 6`、闭式 `n − #blocks = 3 − 1 = 2`）一致。

本模块只 import `SpLayerSeparability`，**不** import `Matrix.Trace`，
以免重蹈 §21.29.8.2 的 simp 扰动。
-/
import MUFPFormalization.SpLayerSeparability

namespace MUFPFormalization

/-- **`ker` 的显式结构**：任何与 `J₃` 交换的 `3 × 3` 复矩阵都是 `J₃` 的次数 ≤ 2 的多项式。
    等价陈述：`ker(ad_{J₃}) ⊆ span{I₃, J₃, J₃²}`，即 `dim ker ≤ 3`。
    数值侧由 `rank ad_{J₃} = 9 − 3 = 6` 给出，这里是其 Lean 版本的**显式形式**。 -/
theorem jordan3_ker_mem_span (X : Matrix (Fin 3) (Fin 3) ℂ)
    (h : X ∈ LinearMap.ker (adLin jordan3)) :
    X = X 0 0 • (1 : Matrix (Fin 3) (Fin 3) ℂ) + X 0 1 • jordan3 + X 0 2 • jordan3Sq := by
  have hX : jordan3 * X = X * jordan3 := by
    rw [LinearMap.mem_ker] at h
    change jordan3 * X - X * jordan3 = 0 at h
    exact sub_eq_zero.mp h
  have e10 : X 1 0 = 0 := by
    have hc := congrArg (fun M : Matrix (Fin 3) (Fin 3) ℂ => M (0 : Fin 3) (0 : Fin 3)) hX
    simp [Matrix.mul_apply, jordan3, Matrix.of_apply, Fin.sum_univ_succ] at hc
    simpa using hc
  have e11 : X 1 1 = X 0 0 := by
    have hc := congrArg (fun M : Matrix (Fin 3) (Fin 3) ℂ => M (0 : Fin 3) (1 : Fin 3)) hX
    simp [Matrix.mul_apply, jordan3, Matrix.of_apply, Fin.sum_univ_succ] at hc
    simpa using hc
  have e12 : X 1 2 = X 0 1 := by
    have hc := congrArg (fun M : Matrix (Fin 3) (Fin 3) ℂ => M (0 : Fin 3) (2 : Fin 3)) hX
    simp [Matrix.mul_apply, jordan3, Matrix.of_apply, Fin.sum_univ_succ] at hc
    simpa using hc
  have e20 : X 2 0 = 0 := by
    have hc := congrArg (fun M : Matrix (Fin 3) (Fin 3) ℂ => M (1 : Fin 3) (0 : Fin 3)) hX
    simp [Matrix.mul_apply, jordan3, Matrix.of_apply, Fin.sum_univ_succ] at hc
    simpa using hc
  have e21 : X 2 1 = 0 := by
    have hc := congrArg (fun M : Matrix (Fin 3) (Fin 3) ℂ => M (1 : Fin 3) (1 : Fin 3)) hX
    simp [Matrix.mul_apply, jordan3, Matrix.of_apply, Fin.sum_univ_succ] at hc
    rw [e10] at hc
    simpa using hc
  have e22 : X 2 2 = X 0 0 := by
    have hc := congrArg (fun M : Matrix (Fin 3) (Fin 3) ℂ => M (1 : Fin 3) (2 : Fin 3)) hX
    simp [Matrix.mul_apply, jordan3, Matrix.of_apply, Fin.sum_univ_succ] at hc
    rw [e11] at hc
    simpa using hc
  ext i j
  fin_cases i <;> fin_cases j
  all_goals simp [jordan3, jordan3Sq, Matrix.add_apply, Matrix.smul_apply,
    Matrix.of_apply, smul_eq_mul, e10, e11, e12, e20, e21, e22]

end MUFPFormalization
