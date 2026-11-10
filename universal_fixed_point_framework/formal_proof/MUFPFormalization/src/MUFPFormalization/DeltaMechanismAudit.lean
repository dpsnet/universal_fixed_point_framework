import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Algebra.BigOperators.Group.Finset.Basic

/-!
# DeltaMechanismAudit.lean — S629：δ 机制化的两块登记来源否证

α⁻¹ = 72 + 24·d_H、d_H = ln15 + δ、δ = 0.0017831 这一层，此前把 δ 的
机制来源登记为「分支非等权（c₁ = S₃·S₄, c₂ = S₄, c₃ ≈ 1）」
（BranchCounting.lean L175–182 / DHStructuralAnalysis.lean L30–37）。
本模块把该登记来源拆成两个可判定命题并否证：

1. **等率加权无关**：若 B 支的收缩率同为 r，则加权 Moran 方程
   Σ_k w_k·r^d = 1 的解只取决于总权重 Σ w_k，与权重如何分配无关。
   ⇒ 「分支非等权（重数不同）」本身**不产生** δ；δ 只能来自率非均匀。

2. **c₃ = 1 阻断 Moran 解**：若 c₁, c₂ > 0 且 c₃ = 1，则
   c₁^d + c₂^d + c₃^d = 1 对任意 d 都无解。
   ⇒ YukawaIFSWeights 的 (c₁,c₂,c₃) 不能充当 d_H 的 Moran 方程来源
   （它们是质量公式 m_i = y_i·c_i^{α} 的收缩因子，不是 d_H 的 15 支权重）。

3. **记号的算术**：|S₃|·|S₄| + |S₄| + 1 = 144 + 24 + 1 = 169 ≠ 15。
   ⇒ 该组合作「重数」读时与 B = 15 不相容。

零 sorry。
-/

namespace MUFPF.DeltaMechanismAudit

open Finset
open scoped BigOperators

/-- 等率加权无关（一）：Σ_k w_k·r^d = (Σ_k w_k)·r^d。
    因 r^d 与分支标号 k 无关，可提到求和号外。 -/
theorem equal_rate_weights_irrelevant (B : ℕ) (w : ℕ → ℝ) (r d : ℝ) :
    Finset.sum (Finset.range B) (fun k => w k * r ^ d) =
      Finset.sum (Finset.range B) (fun k => w k) * r ^ d := by
  rw [Finset.sum_mul]

/-- 等率加权无关（二）：若总权重 = B、且 r^d = B⁻¹，则加权 Moran 方程成立，
    且与 w 的具体分配无关（只要求 Σ w = B）。

    这是对「分支非等权 ⇒ δ ≠ 0」的直接否证：只要各支率相同，
    任何正权重分配都给出同一个解 d = log B / log(1/r)，δ ≡ 0。 -/
theorem weights_only_via_sum (B : ℕ) (hB : 0 < B) (w : ℕ → ℝ)
    (hsum : Finset.sum (Finset.range B) (fun k => w k) = (B : ℝ)) {r d : ℝ}
    (hr : r ^ d = (B : ℝ)⁻¹) :
    Finset.sum (Finset.range B) (fun k => w k * r ^ d) = 1 := by
  rw [equal_rate_weights_irrelevant, hsum, hr]
  exact mul_inv_cancel₀ (by exact_mod_cast (Nat.pos_iff_ne_zero.mp hB))

/-- c₃ = 1 阻断 Moran 解：若 c₁, c₂ > 0，则 c₁^d + c₂^d + 1 ≠ 1 对任意实 d。
    因此 (c₁, c₂, 1) 这组「收缩因子」不可能满足 d_H 的 Moran 方程
    Σ c_i^d = 1 —— 它属于质量公式 m_i = y_i·c_i^{α}，不是 d_H 的分支权重。 -/
theorem c3_one_blocks_moran {c₁ c₂ d : ℝ} (h1 : 0 < c₁) (h2 : 0 < c₂) :
    c₁ ^ d + c₂ ^ d + 1 ≠ 1 := by
  have hp1 : 0 < c₁ ^ d := Real.rpow_pos_of_pos h1 d
  have hp2 : 0 < c₂ ^ d := Real.rpow_pos_of_pos h2 d
  intro h
  linarith

/-- 登记记号的算术核对：|S₃|·|S₄| + |S₄| + 1 = 144 + 24 + 1 = 169，且 169 ≠ 15。
    即该组合作「分支重数」读时，总和与 B = 15 不相容（差 154）。 -/
theorem sigma_weight_sum_is_169 : (144 : ℕ) + 24 + 1 = 169 ∧ (169 : ℕ) ≠ 15 :=
  ⟨by norm_num, by norm_num⟩

/-- 推论：把 (c₁,c₂,c₃) 读作重数时，其总和 169 对应的无扰解是 ln 169，
    与 d_H 的 ln 15 相差 ln(169/15) ≈ 2.4218，远超 δ ≈ 0.0018。
    （数值由 scripts/s629_delta_mechanism_probe.py 给出，此处只钉算术部分。） -/
theorem sigma_weight_sum_ne_fifteen : (144 : ℕ) + 24 + 1 ≠ 15 := by
  norm_num

end MUFPF.DeltaMechanismAudit
