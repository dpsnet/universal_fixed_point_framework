/-
预研形式化：层熵分解恒等式（外部理论预研 §7.53）
====================================================================

推进对象：external_theory_presurvey/external_theory_derivation_chain.md §7.53
（前提候选 μ(层 k) ∝ S_k 的一致性验证——熵分解恒等式精确成立）。

命题（§7.53）：若 15 个可观测分支分成 k 层（层 i 有 n_i 分支，Σ n_i = 15），
每分支权重均匀 w = 1/15（§7.15 A5 机证），层概率 p_i = n_i/15，则：
  **ln 15 = H({p_i}) + Σ p_i·ln n_i**（层分布熵 + 层内熵加权 = 总熵）
此恒等式对任意层划分（n_i > 0，Σ n_i = 15）精确成立（代数强制：
n_i/p_i = 15 ⟹ Σ p_i ln(n_i/p_i) = ln 15）。

形式化范围（诚实标注）：
  本节形式化熵分解恒等式的**代数核心**：总熵 ln 15 = 层分布熵 + 层内熵加权
  （任意层划分，n_i/p_i = 15 代数强制）；§7.52 的前提候选 μ(层 k) ∝ S_k
  （层保留度 = 层谱权重）不在此形式化（候选前提）。
-/

import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic

open scoped BigOperators

namespace PresurveyFormalization.LayerEntropy

/-- 层概率：层 i 的总权重 p_i = n_i/15（层 i 有 n_i 个分支，每分支权重 1/15）。 -/
noncomputable def layerProb {k : ℕ} (n : Fin k → ℕ) (i : Fin k) : ℝ :=
  (n i : ℝ) / 15

/-- 层概率归一化：Σ_i p_i = 1（Σ n_i = 15 时）。 -/
theorem layerProb_sum_eq_one {k : ℕ} (n : Fin k → ℕ) (hn : (∑ i : Fin k, n i) = 15) :
    (∑ i : Fin k, layerProb n i) = 1 := by
  unfold layerProb
  have h : (∑ i : Fin k, (n i : ℝ)) = (15 : ℝ) := by
    exact_mod_cast hn
  calc
    (∑ i : Fin k, (n i : ℝ) / 15)
        = (∑ i : Fin k, (n i : ℝ) * (1 / 15)) := by
          apply Finset.sum_congr rfl
          intro i _
          ring
    _ = (∑ i : Fin k, (n i : ℝ)) * (1 / 15) := by
          rw [← Finset.sum_mul]
    _ = (15 : ℝ) * (1 / 15) := by
          rw [h]
    _ = 1 := by
          norm_num

/-- 熵分解恒等式（§7.53 核心）：总熵 ln 15 = 层分布熵 H({p_i}) + 层内熵加权 Σ p_i·ln n_i。
    对任意层划分（n_i > 0，Σ n_i = 15）精确成立（n_i/p_i = 15 代数强制）。 -/
theorem entropy_decomposition_eq_log_15 {k : ℕ} (n : Fin k → ℕ)
    (hn : (∑ i : Fin k, n i) = 15) (hpos : ∀ i : Fin k, 0 < n i) :
    (-∑ i : Fin k, layerProb n i * Real.log (layerProb n i))
      + (∑ i : Fin k, layerProb n i * Real.log (n i : ℝ)) = Real.log (15 : ℝ) := by
  calc
    (-∑ i : Fin k, layerProb n i * Real.log (layerProb n i))
        + (∑ i : Fin k, layerProb n i * Real.log (n i : ℝ))
        = ∑ i : Fin k, layerProb n i * (Real.log (n i : ℝ) - Real.log (layerProb n i)) := by
          have hneg : (-∑ i : Fin k, layerProb n i * Real.log (layerProb n i)) +
              (∑ i : Fin k, layerProb n i * Real.log (n i : ℝ))
              = (∑ i : Fin k, layerProb n i * Real.log (n i : ℝ)) -
                (∑ i : Fin k, layerProb n i * Real.log (layerProb n i)) := by ring
          rw [hneg]
          rw [← Finset.sum_sub_distrib]
          apply Finset.sum_congr rfl
          intro i _
          ring
    _ = ∑ i : Fin k, layerProb n i * Real.log ((n i : ℝ) / layerProb n i) := by
          apply Finset.sum_congr rfl
          intro i _
          have hpi : 0 < layerProb n i := by
            unfold layerProb
            exact div_pos (by exact_mod_cast hpos i) (by norm_num)
          have hni : 0 < (n i : ℝ) := by exact_mod_cast hpos i
          have hlog : Real.log ((n i : ℝ) / layerProb n i) =
              Real.log (n i : ℝ) - Real.log (layerProb n i) :=
            Real.log_div hni.ne' hpi.ne'
          rw [hlog]
    _ = ∑ i : Fin k, layerProb n i * Real.log (15 : ℝ) := by
          apply Finset.sum_congr rfl
          intro i _
          have hni : (n i : ℝ) ≠ 0 := by exact_mod_cast (ne_of_gt (hpos i))
          have hlog : Real.log ((n i : ℝ) / layerProb n i) = Real.log (15 : ℝ) := by
            unfold layerProb
            rw [show (n i : ℝ) / ((n i : ℝ) / 15) = 15 by field_simp [hni]]
          rw [hlog]
    _ = Real.log (15 : ℝ) := by
          rw [← Finset.sum_mul]
          rw [layerProb_sum_eq_one n hn]
          simp

end PresurveyFormalization.LayerEntropy
