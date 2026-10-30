/- 
# SingleMinusAnchorPair.lean

Phase 77 M37/M38 核心发现形式化（arXiv:2602.12176v2 单负剥离振幅）

**动量双守恒恒等式 B（锚对分解）**：对任何锚 k、任何 p ≠ k，
动量守恒（Σω = 0、Σωz = 0）⇒

    P[k][p] = −Σ_{j≠k,p} P[k][j]

即：任何锚 k 到特殊粒子 p 的单对括号 = 其余锚定单对的负和。
这是恒等式 A（anchor_sum_zero，M43 已闭合）的直接推论（拆出 p 项）。
n=6 的 s61 展开（M37）是该恒等式的特例：s61 = −Σ_{j=2..5} s_{6j}。

证明（纯代数）：
1. 恒等式 A：Σ_{j≠k} P[k][j] = 0（anchor_sum_zero）
2. 拆出 p 项：0 = Σ_{j≠k,p} P[k][j] + P[k][p]（sum_erase_add）
3. linarith：P[k][p] = −Σ_{j≠k,p} P[k][j]

数值先证伪（M38）：恒等式 B 跨 n=6..11 共 78000 检验 0 偏差。

状态：全闭（零 sorry）。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Data.Int.Basic
import Mathlib.Tactic
import MUFPFormalization.SingleMinusAnchorSum

noncomputable section
open scoped BigOperators
open BigOperators

namespace SingleMinusAnchorPair

/-- 锚对分解：P[k][p] = −Σ_{j≠k,p} P[k][j] -/
theorem anchor_pair_decomp {n : ℕ} (ω z : Fin n → ℝ) (k p : Fin n)
    (hpk : p ≠ k)
    (hsum : ∑ i : Fin n, ω i = 0)
    (hmom : ∑ i : Fin n, ω i * z i = 0) :
    ω k * ω p * (z k - z p) =
      - (∑ j ∈ (Finset.univ.erase k).erase p, ω k * ω j * (z k - z j)) := by
  have haz : SingleMinusAnchorSum.anchorSum ω z k = 0 :=
    SingleMinusAnchorSum.anchor_sum_zero ω z k hsum hmom
  unfold SingleMinusAnchorSum.anchorSum at haz
  have hmem : p ∈ Finset.univ.erase k := by
    exact Finset.mem_erase.mpr ⟨hpk, Finset.mem_univ p⟩
  have hsplit : (∑ j ∈ Finset.univ.erase k, ω k * ω j * (z k - z j)) =
      (∑ j ∈ (Finset.univ.erase k).erase p, ω k * ω j * (z k - z j)) +
        ω k * ω p * (z k - z p) := by
    rw [← Finset.sum_erase_add _ (fun j => ω k * ω j * (z k - z j)) hmem]
  linarith

end SingleMinusAnchorPair
