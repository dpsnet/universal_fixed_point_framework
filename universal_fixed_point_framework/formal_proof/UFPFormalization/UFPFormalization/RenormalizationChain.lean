import UFPFormalization.InflationDynamics
import UFPFormalization.AInfinityAlgebra
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Tactic

open Matrix

namespace UFPFormalization

/-!
# Renormalization Chain (Phase 61C)

量子重整化完整链条（论文 `paper/paper61C_renormalization_chain.md`）：

  F1  adG_preserves_hermitian：G 反 Hermitian 时 [G,A] 保 Hermitian——
      一阶对易子 = 单圈 β 的谱生成元（定理 3.2 的代数基础）。
  F2  iterated_adG_preserves_hermitian：所有阶迭代对易子 ad_G^n(A) 保
      Hermitian——圈数-对易子阶数对应 β^(n) ↔ ad_G^n(A_t) 的代数核心。
  F3  spectral_flow_preserves_hermitian：谱流保 Hermitian（引用
      InflationDynamics，定理 3.1 特征值实性的前提）。

谱流方程 dA_t/dt = [G, A_t] 的 n 阶迭代展开对应 n 阶对易子（BCH 结构），
即 n 圈 β 的谱生成元（Paper V §6 匹配模式，数值 12/12）。
-/

/-- F1: G 反 Hermitian（G† = -G）且 A Hermitian 时，[G,A] = GA - AG 为 Hermitian。
    一阶对易子 = 单圈 β 的谱生成元（定理 3.2）。数值验证：`paperX_rg_chain.py` C7。 -/
theorem adG_preserves_hermitian {n : ℕ} (G A : Matrix (Fin n) (Fin n) ℂ)
    (hG : G.conjTranspose = -G) (hA : A.IsHermitian) :
    (G * A - A * G).IsHermitian := by
  unfold Matrix.IsHermitian
  rw [Matrix.conjTranspose_sub, Matrix.conjTranspose_mul, Matrix.conjTranspose_mul, hA, hG]
  simp [mul_neg, neg_mul, sub_eq_add_neg, add_comm, add_left_comm, add_assoc]

/-- F2: 所有阶迭代对易子 ad_G^n(A) 保 Hermitian——
    圈数-对易子阶数对应 β^(n) ↔ ad_G^n(A_t) 的代数闭合（定理 3.2）。 -/
theorem iterated_adG_preserves_hermitian {n : ℕ} (G A : Matrix (Fin n) (Fin n) ℂ)
    (hG : G.conjTranspose = -G) (hA : A.IsHermitian) :
    ∀ k : ℕ, ((ad G)^[k] A).IsHermitian := by
  -- 加强归纳：对任意 Hermitian 起点 B，迭代 k 次后仍 Hermitian
  have h_iter : ∀ (k : ℕ) (B : Matrix (Fin n) (Fin n) ℂ),
      B.IsHermitian → ((ad G)^[k] B).IsHermitian := by
    intro k
    induction k with
    | zero =>
        intro B hB
        simpa [Function.iterate_zero] using hB
    | succ k ihk =>
        intro B hB
        rw [Function.iterate_succ_apply]
        exact ihk (ad G B) (adG_preserves_hermitian G B hG hB)
  intro k
  exact h_iter k A hA

/-- F3: 谱流保 Hermitian（引用 InflationDynamics）——
    定理 3.1 中特征值 λ_k(t) = ⟨k|A_t|k⟩ 实性的前提。 -/
theorem spectral_flow_preserves_hermitian_reference {n : ℕ} (A₀ A_F : Matrix (Fin n) (Fin n) ℂ)
    (t : ℝ) (hA : A₀.IsHermitian) (hG : A_F.conjTranspose = -A_F) :
    (spectralFlow A₀ A_F t).IsHermitian :=
  spectral_flow_self_adjoint A₀ A_F t hA hG

end UFPFormalization
