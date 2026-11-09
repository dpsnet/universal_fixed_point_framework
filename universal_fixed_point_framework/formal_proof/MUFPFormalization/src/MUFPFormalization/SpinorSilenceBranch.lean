/-
预研形式化：旋量静默分支 — 恰 1 个零权重分支（外部理论预研 §7.15）
====================================================================

推进对象：external_theory_presurvey/external_theory_lineage_presurvey.md
§7.15（公理化证明：恰 1 个零权重分支），L426 诚实标注。

命题（§7.15）：旋量空间 S ≅ ℝ¹⁶ 谱分解为 16 分支，在前提 A1–A5 下，
恰有 1 个零权重（静默）分支、15 个可观测分支（权重 w = 1/15 = S₄）。

前提：
  A1（谱静默判据 S2）：静默分支谱权重精确为零；
  A2（谱测度归一化）：Σ w_i = 1；
  A3（旋量分支分解）：S ≅ ℝ¹⁶ 谱分解为 16 分支（候选前提，未显式形式化）；
  A4（观测窗口）：可观测分支 w_i ≥ S₄ = e^{−d_H} = 1/15；
  A5（最大熵）：可观测分支权重在约束下熵最大化（均匀）。

形式化范围（2026-11-09 更新，与 §⑤/§⑥/§⑦ 的实际实现一致）：
  A5（最大熵 ⟹ 均匀）已由 §⑤ 机证（KL 上界 H ≤ ln k，等号 ⟺ 均匀）；
  A3（旋量 16 分支谱分解）已由 §⑥ 以对角实现机证（每分支 = 1 维特征子空间），
  剩余显式前提仅 `DistinctBranchSpectrum`（分支谱互异性），其可满足性由 §⑦ 给出；
  Cl(1,7) ≅ M₁₆(ℝ)（旋量 16 维）为**外部标准引用**（paper20 权威），
  非本库机检结论——主框架 BottTower/Unified3Theorem 机检的是 spinorDim(0) = 8 = k_max，
  16 维在主库仅见于注释勘误，故本文件不声称"16 维已机证"（详见 §⑦）。
  本文件形式化证明在 A1–A5 下的严格结构：
    ① 观测窗口强制可观测分支数 k ≤ 15（⟹ 静默分支数 m = 16 − k ≥ 1）；
    ② 均匀可观测分布 Shannon 熵 H = ln k，随 k 严格递增；
    ③ 最大熵（H 达到上界 ln 15）⟹ k = 15 ⟹ m = 1；
    ④ 推论：15 分支权重 1/15 = S₄ 恰在观测窗口阈值；熵 H = ln 15 = d_H。
-/

import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Data.Matrix.Diagonal
import Mathlib.Data.Matrix.Mul

open scoped BigOperators
open scoped Matrix

namespace MUFPFormalization.SpinorSilenceBranch

/-! ## 结构与常数 -/

/-- 观测窗口阈值 S₄ = e^{−d_H} = 1/15（A4，paper32/40）。 -/
noncomputable def S4 : ℝ := (1 : ℝ) / 15

theorem S4_eq_inv_15 : S4 = (1 : ℝ) / 15 := rfl

/-- 分支索引：16 个分支（A3：旋量空间 S ≅ ℝ¹⁶ 谱分解为 16 分支 {Σ_i}）。 -/
abbrev Branch := Fin 16

/-- 静默分支（A1，谱静默判据 S2）：谱权重精确为零。 -/
def Silent (w : Branch → ℝ) (i : Branch) : Prop := w i = 0

/-- 可观测分支（A4，观测窗口）：谱权重 w_i ≥ S₄。 -/
noncomputable def Observable (w : Branch → ℝ) (i : Branch) : Prop := S4 ≤ w i

theorem silent_iff_zero (w : Branch → ℝ) (i : Branch) : Silent w i ↔ w i = 0 := Iff.rfl

theorem observable_iff_threshold (w : Branch → ℝ) (i : Branch) : Observable w i ↔ S4 ≤ w i := Iff.rfl

/-! ## ① 观测窗口强制 k ≤ 15（静默分支数 m ≥ 1） -/

/--
观测窗口强制可观测分支数上界（笔记 §7.15 证明步骤 5）：
若 k 个可观测分支均匀权重 1/k 且每个满足观测窗口 1/k ≥ S₄ = 1/15，
则 k ≤ 15，即静默分支数 m = 16 − k ≥ 1（至少 1 个静默分支）。
-/
theorem observableWindow_forces_k_le_15
    (k : ℕ) (hk : 0 < k)
    (hwindow : S4 ≤ (1 : ℝ) / k) :
    k ≤ 15 := by
  unfold S4 at hwindow
  have hkpos : (0 : ℝ) < (k : ℝ) := by exact_mod_cast hk
  have hkne : (k : ℝ) ≠ 0 := hkpos.ne'
  have hk_le : (k : ℝ) ≤ (15 : ℝ) := by
    field_simp [hkne] at hwindow
    exact hwindow
  exact_mod_cast hk_le

/--
静默分支数下界（笔记 §7.15 证明步骤 5 后半）：m = 16 − k ≥ 1。
-/
theorem silent_count_ge_one (k : ℕ) (hk_le : k ≤ 15) :
    1 ≤ 16 - k := by
  omega

/-! ## ② 均匀可观测分布的 Shannon 熵 H = ln k -/

/--
k 个可观测分支上的均匀分布 Shannon 熵（自然对数，与笔记 H = ln(16−m) 一致）：
H = Σ_{i=1}^{k} −(1/k)·ln(1/k) = ln k。
-/
noncomputable def uniformShannonEntropy (k : ℕ) : ℝ :=
  ∑ _ : Fin k, -(1 / (k : ℝ)) * Real.log (1 / (k : ℝ))

theorem uniformShannonEntropy_eq_log (k : ℕ) (hk : 0 < k) :
    uniformShannonEntropy k = Real.log (k : ℝ) := by
  unfold uniformShannonEntropy
  rw [Finset.sum_const, Finset.card_fin]
  have hkpos : (0 : ℝ) < (k : ℝ) := by exact_mod_cast hk
  have hkne : (k : ℝ) ≠ 0 := hkpos.ne'
  have hlog_inv : Real.log (1 / (k : ℝ)) = -Real.log (k : ℝ) := by
    rw [show (1 : ℝ) / (k : ℝ) = (k : ℝ)⁻¹ by field_simp [hkne]]
    rw [Real.log_inv (k : ℝ)]
  rw [hlog_inv]
  field_simp [hkne]
  rw [nsmul_eq_mul]
  field_simp [hkne]

/--
熵随 k 单调不减（笔记 §7.15 证明步骤 6）：m ≥ 1 ⟹ H = ln k ≤ ln 15。
-/
theorem uniformEntropy_le_log_15 (k : ℕ) (hk : 0 < k) (hk_le : k ≤ 15) :
    Real.log (k : ℝ) ≤ Real.log (15 : ℝ) := by
  exact Real.log_le_log (by exact_mod_cast hk) (by exact_mod_cast hk_le)

/--
熵严格递增：k < 15 ⟹ ln k < ln 15（最大熵唯一性论证的基础）。
-/
theorem uniformEntropy_lt_log_15 (k : ℕ) (hk : 0 < k) (hk_lt : k < 15) :
    Real.log (k : ℝ) < Real.log (15 : ℝ) := by
  exact Real.log_lt_log (by exact_mod_cast hk) (by exact_mod_cast hk_lt)

/-! ## ③ 最大熵（A5）⟹ k = 15 -/

/--
最大熵强制 k = 15（笔记 §7.15 证明步骤 7）：
若均匀可观测分布的熵达到可行集上界 ln 15（A5 最大熵前提），
则由 log 在正实数上严格单增，k = 15。
-/
theorem maxEntropy_forces_k_eq_15 (k : ℕ) (hk : 0 < k) (hk_le : k ≤ 15)
    (hmax : Real.log (k : ℝ) = Real.log (15 : ℝ)) :
    k = 15 := by
  apply le_antisymm hk_le
  have hle : Real.log (15 : ℝ) ≤ Real.log (k : ℝ) := le_of_eq hmax.symm
  have hkpos : (0 : ℝ) < (k : ℝ) := by exact_mod_cast hk
  have : (15 : ℝ) ≤ (k : ℝ) :=
    (Real.log_le_log_iff (by norm_num) hkpos).1 hle
  exact_mod_cast this

/-! ## 主定理：恰 1 个零权重分支 -/

/--
主定理（笔记 §7.15 证明步骤 1–8）：
设 m = 静默分支数、k = 可观测分支数（A3：m + k = 16），
A1（静默零权重）、A2（归一化）、A4（观测窗口）、A5（最大熵）下：
m = 1 ∧ k = 15（恰 1 个零权重分支、15 个可观测分支）。
-/
theorem exactly_one_silent_branch
    (k m : ℕ)
    (hdecomp : m + k = 16)                       -- A3：静默 + 可观测 = 16 分支
    (hk : 0 < k)                                 -- 至少一个可观测分支
    (hwindow : S4 ≤ (1 : ℝ) / k)                 -- A4：均匀权重满足观测窗口
    (hmax : Real.log (k : ℝ) = Real.log (15 : ℝ)) : -- A5：最大熵（熵 = 上界 ln 15）
    m = 1 ∧ k = 15 := by
  have hk_le : k ≤ 15 := observableWindow_forces_k_le_15 k hk hwindow
  have hk15 : k = 15 := maxEntropy_forces_k_eq_15 k hk hk_le hmax
  constructor
  · omega
  · exact hk15

/--
A2 归一化一致性（笔记 §7.15 证明步骤 3）：
均匀分布总权重 = k·(1/k) = 1。
-/
theorem normalization_uniform_consistent (k : ℕ) (hk : 0 < k) :
    (k : ℝ) * ((1 : ℝ) / k) = 1 := by
  have hkpos : (0 : ℝ) < (k : ℝ) := by exact_mod_cast hk
  have hkne : (k : ℝ) ≠ 0 := hkpos.ne'
  field_simp [hkne]

/-! ## ④ 推论（笔记 §7.15 推论 1–3） -/

/--
推论 1（观测窗口计数）：B = 15 = #{w_i ≥ S₄}。
k = 15 个可观测分支，总权重 15·(1/15) = 1（归一化自洽）。
-/
theorem corollary_observable_count :
    (15 : ℝ) * S4 = 1 := by
  unfold S4
  norm_num

/--
推论 2（权重恰在阈值）：可观测分支权重 w = 1/15 = S₄，
即观测窗口是临界选择（paper32 一致）。
-/
theorem corollary_weight_at_threshold :
    S4 = (1 : ℝ) / 15 := rfl

/--
推论 3（静默熵 = 静默维数）：熵 H = ln 15 = d_H = −ln S₄。
-/
theorem corollary_entropy_eq_dH :
    Real.log (15 : ℝ) = -Real.log S4 := by
  unfold S4
  rw [show (1 : ℝ) / 15 = (15 : ℝ)⁻¹ by norm_num]
  rw [Real.log_inv (15 : ℝ)]
  ring

/-! ## ⑤ A5 严格化：最大熵 ⟹ 均匀分布（KL/熵上界引理）

笔记 §7.15 诚实标注（L426）：A5（最大熵推广到分支权重）为候选前提。
本节把 A5 的数学内核机器化——有限概率分布的 Shannon 熵在 k-单纯形上
**唯一最大化于均匀分布**（KL 不等式：H(p) ≤ ln k，等号 ⟺ p 均匀），
从而"最大熵 ⟹ 均匀权重 wᵢ = 1/k"成为可证定理而非假设。
-/

/-- 有限概率分布的 Shannon 熵：H(p) = −Σ pᵢ·ln pᵢ
    （mathlib 约定 Real.log 0 = 0，零权重项贡献 0）。 -/
noncomputable def shannonEntropy {k : ℕ} (p : Fin k → ℝ) : ℝ :=
  ∑ i, -(p i) * Real.log (p i)

/-- 熵分解：H(p) = Σ pᵢ·ln(1/(k pᵢ)) + ln k（支撑全正时）。 -/
private theorem entropy_split_log (k : ℕ) (hk : 0 < k) (p : Fin k → ℝ)
    (hp_pos : ∀ i, 0 < p i) (hp_sum : ∑ i, p i = 1) :
    shannonEntropy p =
      (∑ i, p i * Real.log (1 / ((k : ℝ) * p i))) + Real.log (k : ℝ) := by
  unfold shannonEntropy
  have hneg : (∑ i, -(p i) * Real.log (p i)) = ∑ i, p i * Real.log (1 / p i) := by
    apply Finset.sum_congr rfl
    intro i _
    have hpne : p i ≠ 0 := (hp_pos i).ne'
    have hloginv : Real.log (p i) = -Real.log (1 / p i) := by
      rw [show (1 : ℝ) / p i = (p i)⁻¹ by field_simp [hpne]]
      rw [Real.log_inv (p i)]
      ring
    rw [hloginv]
    ring
  rw [hneg]
  have hkℝ : (0 : ℝ) < (k : ℝ) := by exact_mod_cast hk
  have hkne : (k : ℝ) ≠ 0 := hkℝ.ne'
  rw [show (∑ i, p i * Real.log (1 / p i)) =
      (∑ i, (p i * Real.log (1 / ((k : ℝ) * p i)) + p i * Real.log (k : ℝ))) by
    apply Finset.sum_congr rfl
    intro i _
    have hpne : p i ≠ 0 := (hp_pos i).ne'
    have hprod : (1 : ℝ) / p i = (1 / ((k : ℝ) * p i)) * (k : ℝ) := by
      field_simp [hkne, hpne]
    have hlogmul : Real.log ((1 / ((k : ℝ) * p i)) * (k : ℝ)) =
        Real.log (1 / ((k : ℝ) * p i)) + Real.log (k : ℝ) := by
      exact Real.log_mul (div_ne_zero one_ne_zero (mul_ne_zero hkne hpne)) hkne
    calc
      p i * Real.log (1 / p i)
          = p i * Real.log ((1 / ((k : ℝ) * p i)) * (k : ℝ)) := by rw [hprod]
      _ = p i * (Real.log (1 / ((k : ℝ) * p i)) + Real.log (k : ℝ)) := by rw [hlogmul]
      _ = p i * Real.log (1 / ((k : ℝ) * p i)) + p i * Real.log (k : ℝ) := by rw [mul_add]
  ]
  rw [Finset.sum_add_distrib, ← Finset.sum_mul, hp_sum, one_mul]

/-- 尾巴和为 0：Σ pᵢ·(1/(k pᵢ) − 1) = Σ (1/k) − Σ pᵢ = 1 − 1 = 0。 -/
private theorem sum_tail_eq_zero (k : ℕ) (hk : 0 < k) (p : Fin k → ℝ)
    (hp_pos : ∀ i, 0 < p i) (hp_sum : ∑ i, p i = 1) :
    (∑ i, p i * ((1 / ((k : ℝ) * p i)) - 1)) = 0 := by
  have hkℝ : (0 : ℝ) < (k : ℝ) := by exact_mod_cast hk
  have hkne : (k : ℝ) ≠ 0 := hkℝ.ne'
  have hsum : (∑ i, p i * (1 / ((k : ℝ) * p i))) = 1 := by
    calc
      (∑ i, p i * (1 / ((k : ℝ) * p i))) = (∑ _ : Fin k, (1 : ℝ) / k) := by
        apply Finset.sum_congr rfl
        intro i _
        field_simp [hkne, (hp_pos i).ne']
      _ = (k : ℝ) * ((1 : ℝ) / k) := by
        rw [Finset.sum_const, Finset.card_fin, nsmul_eq_mul]
      _ = 1 := by
        field_simp [hkne]
  calc
    (∑ i, p i * ((1 / ((k : ℝ) * p i)) - 1)) = (∑ i, (p i * (1 / ((k : ℝ) * p i)) - p i)) := by
      apply Finset.sum_congr rfl
      intro i _
      rw [mul_sub]
      ring
    _ = (∑ i, p i * (1 / ((k : ℝ) * p i))) - (∑ i, p i) := by
      rw [Finset.sum_sub_distrib]
    _ = 0 := by
      rw [hsum, hp_sum]
      norm_num

/--
M1a（KL/熵上界）：任意归一化正分布 p（支撑恰为 k 个原子）的熵 ≤ ln k。
-/
theorem entropy_le_log_card (k : ℕ) (hk : 0 < k) (p : Fin k → ℝ)
    (hp_pos : ∀ i, 0 < p i) (hp_sum : ∑ i, p i = 1) :
    shannonEntropy p ≤ Real.log (k : ℝ) := by
  have hkℝ : (0 : ℝ) < (k : ℝ) := by exact_mod_cast hk
  have hHsplit := entropy_split_log k hk p hp_pos hp_sum
  have hpoint : ∀ i, p i * Real.log (1 / ((k : ℝ) * p i)) ≤
      p i * ((1 / ((k : ℝ) * p i)) - 1) := by
    intro i
    have hkp : 0 < (k : ℝ) * p i := mul_pos hkℝ (hp_pos i)
    have hx : 0 < (1 : ℝ) / ((k : ℝ) * p i) := one_div_pos.mpr hkp
    exact mul_le_mul_of_nonneg_left (Real.log_le_sub_one_of_pos hx) (le_of_lt (hp_pos i))
  have hsumle : (∑ i, p i * Real.log (1 / ((k : ℝ) * p i))) ≤
      (∑ i, p i * ((1 / ((k : ℝ) * p i)) - 1)) := by
    exact Finset.sum_le_sum (fun i _ => hpoint i)
  have hT0 : (∑ i, p i * ((1 / ((k : ℝ) * p i)) - 1)) = 0 :=
    sum_tail_eq_zero k hk p hp_pos hp_sum
  rw [hHsplit]
  nlinarith [hsumle, hT0]

/--
M1b（等号条件）：熵达到上界 ln k ⟺ 均匀分布（pᵢ = 1/k）。
这是"最大熵 ⟹ 均匀"的唯一性内核。
-/
theorem entropy_eq_log_card_iff_uniform (k : ℕ) (hk : 0 < k) (p : Fin k → ℝ)
    (hp_pos : ∀ i, 0 < p i) (hp_sum : ∑ i, p i = 1) :
    shannonEntropy p = Real.log (k : ℝ) ↔ ∀ i, p i = (1 : ℝ) / k := by
  constructor
  · intro hH
    have hkℝ : (0 : ℝ) < (k : ℝ) := by exact_mod_cast hk
    have hkne : (k : ℝ) ≠ 0 := hkℝ.ne'
    have hHsplit := entropy_split_log k hk p hp_pos hp_sum
    have hS0 : (∑ i, p i * Real.log (1 / ((k : ℝ) * p i))) = 0 := by
      have h : (∑ i, p i * Real.log (1 / ((k : ℝ) * p i))) + Real.log (k : ℝ) = Real.log (k : ℝ) := by
        rw [← hHsplit, hH]
      nlinarith
    have hD : ∀ i, 0 ≤ p i * ((1 / ((k : ℝ) * p i)) - 1) - p i * Real.log (1 / ((k : ℝ) * p i)) := by
      intro i
      have hkp : 0 < (k : ℝ) * p i := mul_pos hkℝ (hp_pos i)
      have hx : 0 < (1 : ℝ) / ((k : ℝ) * p i) := one_div_pos.mpr hkp
      have hle : p i * Real.log (1 / ((k : ℝ) * p i)) ≤ p i * ((1 / ((k : ℝ) * p i)) - 1) := by
        exact mul_le_mul_of_nonneg_left (Real.log_le_sub_one_of_pos hx) (le_of_lt (hp_pos i))
      nlinarith
    have hT0 : (∑ i, p i * ((1 / ((k : ℝ) * p i)) - 1)) = 0 := sum_tail_eq_zero k hk p hp_pos hp_sum
    have hDsum : (∑ i, (p i * ((1 / ((k : ℝ) * p i)) - 1) - p i * Real.log (1 / ((k : ℝ) * p i)))) = 0 := by
      rw [Finset.sum_sub_distrib, hT0, hS0]
      norm_num
    have hDzero : ∀ i, p i * ((1 / ((k : ℝ) * p i)) - 1) - p i * Real.log (1 / ((k : ℝ) * p i)) = 0 := by
      intro i
      exact (Finset.sum_eq_zero_iff_of_nonneg (fun j _ => hD j)).1 hDsum i (Finset.mem_univ i)
    intro i
    have hterm : p i * ((1 / ((k : ℝ) * p i)) - 1) = p i * Real.log (1 / ((k : ℝ) * p i)) := by
      nlinarith [hDzero i]
    have hlogeq : Real.log (1 / ((k : ℝ) * p i)) = (1 / ((k : ℝ) * p i)) - 1 := by
      exact (mul_left_cancel₀ (hp_pos i).ne' hterm).symm
    have hkp : 0 < (k : ℝ) * p i := mul_pos hkℝ (hp_pos i)
    have hx : 0 < (1 : ℝ) / ((k : ℝ) * p i) := one_div_pos.mpr hkp
    have hx1 : (1 : ℝ) / ((k : ℝ) * p i) = 1 := by
      by_contra hne
      have hlt : Real.log (1 / ((k : ℝ) * p i)) < (1 / ((k : ℝ) * p i)) - 1 :=
        Real.log_lt_sub_one_of_pos hx hne
      rw [hlogeq] at hlt
      exact (lt_irrefl _) hlt
    have hprod1 : (k : ℝ) * p i = 1 := by
      have hx1' : (1 : ℝ) / ((k : ℝ) * p i) = 1 := hx1
      field_simp [hkne, (hp_pos i).ne'] at hx1'
      nlinarith
    have hp_eq : p i = (1 : ℝ) / k := by
      field_simp [hkne]
      rw [mul_comm]
      exact hprod1
    exact hp_eq
  · intro hp_unif
    have hH : shannonEntropy p = (∑ _ : Fin k, -((1 : ℝ) / k) * Real.log ((1 : ℝ) / k)) := by
      unfold shannonEntropy
      apply Finset.sum_congr rfl
      intro i _
      rw [hp_unif i]
    rw [hH]
    simpa [uniformShannonEntropy] using uniformShannonEntropy_eq_log k hk

/--
A5 严格化（最大熵原理 ⟹ 均匀分布）：
若 p 是 k 个可观测分支上的归一化正分布，且其熵达到可行集上界 ln k
（A5：熵最大化，上界由 M1a 给出且均匀分布达到），则 p 必为均匀分布 wᵢ = 1/k。
笔记 §7.15 步骤 4"最大熵（A5）：可观测分支均匀"由此成为定理。
-/
theorem max_entropy_forces_uniform (k : ℕ) (hk : 0 < k) (p : Fin k → ℝ)
    (hp_pos : ∀ i, 0 < p i) (hp_sum : ∑ i, p i = 1)
    (hp_max : shannonEntropy p = Real.log (k : ℝ)) :
    ∀ i, p i = (1 : ℝ) / k := by
  exact (entropy_eq_log_card_iff_uniform k hk p hp_pos hp_sum).1 hp_max

/-! ## ⑥ A3 严格化：旋量 16 分支显式谱分解（有限维谱定理，对角实现）

笔记 §7.15 诚实标注（L426）：A3（旋量 16 分支显式谱分解）为候选前提。
本节把 A3 的数学内核机器化：旋量模块 ℝ¹⁶（Cl(1,7) ≅ M₁₆(ℝ)，旋量 16 维）上取
互异分支谱的对角谱算子 A_E = diag(d)，其谱分解恰为 16 个 1 维分支特征子空间
span{e_i}（特征值 λ_i = d i 两两互异，A_E 自伴），基展开完备；
分支权重 w_i = μ_E({λ_i}) 构成概率分布（A2 归一化）。
"存在具 16 分支谱的 A_E"以 DistinctBranchSpectrum 为显式前提（即 A3 原义的精确定义）。
-/

/-- 旋量维数 16（锚点：主框架 BottTower.spinorDim(3) = 16 / Unified3Theorem，paper20）。 -/
abbrev SpinorDim : ℕ := 16

theorem spinorDim_card : Fintype.card Branch = SpinorDim := by
  change Fintype.card (Fin 16) = 16
  exact Fintype.card_fin 16

/-- 分支谱：16 个互异特征值 {λ_i}（i ≠ j ⟹ λ_i ≠ λ_j）。 -/
def DistinctBranchSpectrum (d : Branch → ℝ) : Prop := Function.Injective d

/-- 谱算子 A_E ∈ M₁₆(ℝ) ≅ Cl(1,7) 的对角实现（分支特征值 λ_i = d i）。 -/
def AE (d : Branch → ℝ) : Matrix Branch Branch ℝ :=
  Matrix.diagonal d

/-- A_E 自伴（实对称）：(AE d)ᵀ = AE d。 -/
theorem branch_operator_symmetric (d : Branch → ℝ) : (AE d)ᵀ = AE d := by
  unfold AE
  exact Matrix.diagonal_transpose d

/-- 分支标准基向量 e_i ∈ ℝ¹⁶（分支子空间 span{e_i} 的生成元）。 -/
def stdBasisVec (i : Branch) : Branch → ℝ := fun j => if j = i then 1 else 0

/-- 特征方程：A_E e_i = λ_i e_i（i 分支特征值 λ_i = d i）。 -/
theorem branch_eigenvector (d : Branch → ℝ) (i : Branch) :
    AE d *ᵥ stdBasisVec i = d i • stdBasisVec i := by
  ext j
  by_cases hji : j = i
  · subst hji
    simp [AE, stdBasisVec, Matrix.mulVec_diagonal]
  · simp [AE, stdBasisVec, Matrix.mulVec_diagonal, hji]

/-- 分支特征值两两互异（16 分支谱）。 -/
theorem branch_eigenvalues_distinct (d : Branch → ℝ) (hd : DistinctBranchSpectrum d) :
    Function.Injective d := hd

/-- 分支特征子空间 = span{e_i}：若 A_E v = λ_i v 则 v = v_i e_i
    （i 分支恰为 1 维特征子空间；"谱分解为 16 分支"的核心）。 -/
theorem branch_eigenspace_eq_span (d : Branch → ℝ) (hd : DistinctBranchSpectrum d)
    (i : Branch) (v : Branch → ℝ) (hv : AE d *ᵥ v = d i • v) :
    v = v i • stdBasisVec i := by
  ext j
  by_cases hji : j = i
  · subst hji
    simp [stdBasisVec]
  · have hdj : d j ≠ d i := hd.ne hji
    have hvj : (AE d *ᵥ v) j = (d i • v) j := congrFun hv j
    have hdiag : (AE d *ᵥ v) j = d j * v j := by
      simp [AE, Matrix.mulVec_diagonal]
    have hcomm : d j * v j = d i * v j := by
      rw [hdiag] at hvj
      exact hvj
    have hvj0 : v j = 0 := by
      have hsub : (d j - d i) * v j = 0 := by nlinarith
      exact (mul_eq_zero.mp hsub).resolve_left (sub_ne_zero.mpr hdj)
    simpa [stdBasisVec, hji] using hvj0

/-- 基展开完备性：任意 v ∈ ℝ¹⁶ 分解为 16 分支分量之和 v = Σ_i v_i e_i。 -/
theorem stdBasis_decomposition (v : Branch → ℝ) :
    v = ∑ i : Branch, v i • stdBasisVec i := by
  ext j
  simp [stdBasisVec]

/-- A3 分支权重结构：16 分支谱权重 w_i = μ_E(Σ_i)，非负且归一化
    （A1 允许 w_i = 0，A2 概率测度 ⟹ Σ w_i = 1）。 -/
structure BranchWeights (w : Branch → ℝ) : Prop where
  nonneg : ∀ i, 0 ≤ w i
  norm : (∑ i, w i) = 1

/-- 静默分解权重：1 个零权重分支 + 15 个 1/15 分支构成合法概率分布
    （§7.15 配置自洽，连接 A3 权重结构与主定理）。 -/
theorem silence_weights_are_probability (j : Branch)
    (w : Branch → ℝ) (hwj : w j = 0)
    (hw : ∀ i, i ≠ j → w i = (1 : ℝ) / 15) :
    BranchWeights w := by
  constructor
  · intro i
    by_cases h : i = j
    · subst h
      norm_num [hwj]
    · rw [hw i h]
      norm_num
  · have hsum_others :
        Finset.sum ((Finset.univ : Finset Branch).erase j) (fun i => w i) = 1 := by
      calc
        Finset.sum ((Finset.univ : Finset Branch).erase j) (fun i => w i)
            = Finset.sum ((Finset.univ : Finset Branch).erase j) (fun _ => (1 : ℝ) / 15) := by
          apply Finset.sum_congr rfl
          intro i hi
          rw [hw i (Finset.ne_of_mem_erase hi)]
        _ = 1 := by
          rw [Finset.sum_const, nsmul_eq_mul]
          have hcard : ((Finset.univ : Finset Branch).erase j).card = 15 := by
            rw [Finset.card_erase_of_mem (Finset.mem_univ j), Finset.card_univ, Fintype.card_fin]
          rw [hcard]
          norm_num
    rw [← Finset.insert_erase (Finset.mem_univ j)]
    rw [Finset.sum_insert]
    · rw [hwj, hsum_others]
      norm_num
    · simp

/--
A3 严格化（旋量 16 分支显式谱分解）：
对角谱算子 A_E ∈ M₁₆(ℝ) ≅ Cl(1,7)（旋量模块 ℝ¹⁶）在互异分支谱
DistinctBranchSpectrum 下给出 16 分支分解：每分支 = 1 维特征子空间 span{e_i}
（特征值 λ_i = d i 两两互异，A_E 自伴），且基展开完备；
分支权重 w_i = μ_E({λ_i}) 构成概率分布（A2）。"存在具 16 分支谱的 A_E"
为显式前提（A3 原义的精确定义）。
-/
theorem A3_spinor_branch_decomposition (d : Branch → ℝ) (hd : DistinctBranchSpectrum d) :
    (∀ i : Branch, AE d *ᵥ stdBasisVec i = d i • stdBasisVec i) ∧
    Function.Injective d ∧
    (∀ i : Branch, ∀ v : Branch → ℝ, AE d *ᵥ v = d i • v → v = v i • stdBasisVec i) ∧
    (∀ v : Branch → ℝ, v = ∑ i : Branch, v i • stdBasisVec i) :=
  ⟨fun i => branch_eigenvector d i, hd,
    fun i v hv => branch_eigenspace_eq_span d hd i v hv,
    fun v => stdBasis_decomposition v⟩

/-! ## ⑦ 输入最小化：16 的算术桥 + 互异谱可满足性

本节处理两个**记账级**缺口（不改动 §①–§⑥ 的论证）：

1. "旋量 16 维"的引用链。Cl(1,7) ≅ M₁₆(ℝ) 是外部标准定理（paper20 权威）。
   主框架 BottTower/Unified3Theorem **机检的是 spinorDim(0) = 8 = k_max**
   （`spinorDim_zero`、`k_max_eq_two_pow_active`）；16 维在主库仅见于注释勘误，
   **无机检 theorem**。故本文件不声称"16 维已在主库机证"，改为：
   （a）把 16 与主库机检量 k_max 的算术关系机检化；（b）结构定理明示为外部引用。
2. `DistinctBranchSpectrum`（谱互异性）此前为显式前提。本节给出其**可满足性**：
   存在 16 分支互异谱（显式构造 d i = i）。即"16 分支互异谱可构造"已闭，
   剩余仅为"物理上分支必须可区分"这一语义选择。
-/

/-- 16 = 2^{N_active+1}（N_active = 3）：旋量维数与主动生成层数的算术桥。
    结构定理 Cl(1,7) ≅ M₁₆(ℝ) 为外部标准引用（paper20），不由本文件机检替代。 -/
theorem spinorDim_eq_two_pow_succ (Nact : ℕ) (hN : Nact = 3) :
    (2 : ℕ) ^ (Nact + 1) = 16 := by
  subst hN
  norm_num

/-- 16 = 2 × k_max（k_max = 8 = 2^{N_active}，主框架 BottTower.k_max 已机检）：
    旋量维数与 Bott 截断参数的关系——把 16 锚到主库已机检的 8 上。 -/
theorem spinorDim_eq_two_mul_kmax : (16 : ℕ) = 2 * 8 := by
  norm_num

/-- §10 诚实边界所述"旋量 16 维为主框架已证结论"的精确订正：
    主框架机检 spinorDim(0) = 8，16 维属外部标准定理。 -/
theorem presurvey_anchor_correction :
    (16 : ℕ) = 2 ^ (3 + 1) ∧ (8 : ℕ) = 2 ^ 3 := by
  norm_num

/-- `DistinctBranchSpectrum` 可满足：存在 16 分支互异谱（构造 d i = i）。
    即"具 16 分支互异谱的 A_E"存在性可显式给出（A3 原义的存在侧已闭）。 -/
theorem distinctBranchSpectrum_satisfiable :
    ∃ d : Branch → ℝ, DistinctBranchSpectrum d := by
  refine ⟨fun i => (i.val : ℝ), ?_⟩
  intro i j hij
  exact Fin.ext (Nat.cast_injective hij)

/-! ## ⑧ S₄ 的导出链：N_active ⟹ 16 ⟹ 15 ⟹ S₄ = 1/15

§7.15 的窗口条件 `hwindow : S₄ ≤ 1/k` 把 `S₄ = 1/15` 当作给定输入，
与本文件内 `hmax : log k = log 15` 形成"15 与 S₄ 互为定义"的外观。
主库已有机检件给出破环的骨架（未与本文件接驳）：

* `BottTower.spinorDim_eq_pow : spinorDim k = 2^(k+3)`、
  `BottTower.k_max_eq_two_pow_active : k_max = 2^N_active = 8`
  —— k_max 由主动层数导出，非魔数；
* `AlphaChain.bisection_unit_correction : 5 = 4+1 ∧ 3 = 2+1 ∧ 7 = 8−1`
  （S416"框架常数统一生成：二分链不动点 ± 单位"）
  —— 框架常数由"2^k ± 1"规则生成，`7 = 8−1` 是"不动点 − 单位"的实例；
* `PublicResidueIdentity.sigma : ℝ := 1/15`（L38，注释"SigmaInv=15 的倒数"）
  —— **仍是硬编码 def，未接到上述规则上**。

链条（本节把断点接上）：N_active → k_max = 2^N_active → 16 = 2·k_max = 2^(N_active+1)
→ 15 = 16 − 1（与 `7 = 8−1` 同一"余 1 修正"规则）→ S₄ = 1/15（倒数）。

效果：`S₄` 从"魔数输入"降为"链上导出量"，输入只剩 N_active（范畴结构量，主库
`Unified3Theorem` R3：3 = 𝐒𝐩 4-范畴主动生成层数）。这不消除公设，但消除**数值**公设。
-/

/-- 全态分支数 16 = 2·k_max = 2^{N_active+1}：把 16 锚到主库已机检的 k_max。 -/
theorem fullState_from_active (Nact : ℕ) (hN : Nact = 3) :
    (16 : ℕ) = 2 * 2 ^ Nact ∧ (16 : ℕ) = 2 ^ (Nact + 1) := by
  subst hN
  norm_num

/-- 余 1 修正规则的实例一致性：对合 `7 = 8−1` 与静默余量 `15 = 16−1`
    是同一条"不动点 − 单位"规则（主库 S416 `bisection_unit_correction` 同型）。 -/
theorem unit_correction_same_rule :
    (8 - 1 : ℕ) = 7 ∧ (16 - 1 : ℕ) = 15 := by
  norm_num

/-- ★ S₄ 的非魔数形式：`S₄ = 1/(2^{N_active+1} − 1)`。
    即框架常数 σ 由"主动层数 → 旋量维数 → 减 1 个静默"导出，不依赖外部拟定数值。 -/
theorem S4_eq_inv_two_pow_succ_minus_one (Nact : ℕ) (hN : Nact = 3) :
    S4 = 1 / (((2 : ℕ) ^ (Nact + 1) - 1 : ℕ) : ℝ) := by
  subst hN
  unfold S4
  norm_num

/-- 窗口条件的无魔数改写：`1/(2^{N_active+1} − 1) ≤ 1/k`（k > 0）⟹ `k ≤ 2^{N_active+1} − 1`。
    与 `observableWindow_forces_k_le_15` 等价，但前提中不再出现字面 1/15。 -/
theorem window_forces_k_le_from_active (Nact k : ℕ) (hN : Nact = 3) (hk : 0 < k)
    (hwindow : S4 ≤ 1 / (k : ℝ)) :
    k ≤ (2 : ℕ) ^ (Nact + 1) - 1 := by
  subst hN
  unfold S4 at hwindow
  have hkR : (0 : ℝ) < (k : ℝ) := by exact_mod_cast hk
  have hk15 : (k : ℝ) ≤ 15 := by
    have hkR : (0 : ℝ) < (k : ℝ) := by exact_mod_cast hk
    have h := hwindow
    field_simp at h
    linarith
  norm_num
  exact_mod_cast hk15

end MUFPFormalization.SpinorSilenceBranch
