/-
预研形式化：时间分支结构 — 双指标刻画（外部理论预研 §7.34）
====================================================================

推进对象：external_theory_presurvey/external_theory_derivation_chain.md §7.34
（时间分支双指标刻画：w = 0（谱静默）∧ c₃ = 1（演化非静默）∧ t（演化参数））。

命题（§7.34）：时间 = 演化轴由三个独立指标共同刻画：
  ① 分支谱权重 w_time = 0（谱静默，§7.15 S2 判据——时间不占 16 分支可观测权重）；
  ② 静默权重 c₃ = 1（演化非静默，paper33——时间/递归分支永不静默，完全保留）；
  ③ 演化参数 t（paper44 A4——时间推进一切转变，σ_S3 单向 1 → 0）。
"静默双义"（§7.32）：w（谱权重意义静默）与 c（演化意义非静默）是两个独立指标，
同一实体两个维度同时成立不矛盾。

形式化范围（诚实标注）：
  ① 谱权重 w_time = 0 复用 §7.15 的 Silent/零权重分支结构（恰 1 个已机器证明）；
  ② 静默权重 c（paper33 c_k 保留程度）在此形式化为独立函数，c_t = 1（全保留）；
     双指标一致配置存在（w 归一化合法 ∧ w_t = 0 ∧ c_t = 1）为本节关键定理；
  ③ 演化参数 t 的单向演化骨架在此独立重构（TimeEvolution：before/after + directional
     ——代数核心与主框架 PhotonTopology.bifurcation_directional 同构，不复制定理）。
  本节不重复证明 paper44/paper33 的既有定理；"时间分支 = §7.15 静默分支"为建模指派
  （§7.34 诚实标注）。
-/

import Mathlib.Data.Real.Basic
import Mathlib.Data.Fin.Basic
import PresurveyFormalization.SpinorSilenceBranch

open scoped BigOperators
open PresurveyFormalization.SpinorSilenceBranch

namespace PresurveyFormalization.TimeBranch

/-! ## 指标 ① 与 ②：谱权重 w 与静默权重 c 的独立性 -/

/-- 时间分支谱权重为零（指标①：谱静默，§7.15 S2 / §7.34）——
    等价于 SpinorSilenceBranch.Silent（谱权重精确为零的静默分支）。 -/
def TimeSilent (w : Branch → ℝ) (t : Branch) : Prop := Silent w t

/-- 静默权重 c（paper33：c_k 为保留程度；c_t = 1 全保留 = 永不静默）。 -/
noncomputable def silenceWeight (c : Branch → ℝ) (i : Branch) : ℝ := c i

/-- 时间分支静默权重全保留（指标②：c₃ = 1，演化非静默，paper33 c₃ = 1）。 -/
def TimeNeverSilent (c : Branch → ℝ) (t : Branch) : Prop := c t = 1

/-- 双指标一致配置存在（§7.34 关键定理）：谱权重 w 为合法概率分布
    （A2 归一化：1 个零权重分支 + 15 个等权 1/15，§7.15），同时
    时间分支谱权重 w_t = 0（谱静默）且静默权重 c_t = 1（演化非静默）——
    两个指标独立、可同时满足、无矛盾（"静默双义"§7.32 的机器表述）。 -/
theorem dual_indicators_consistent (t : Branch) (w : Branch → ℝ)
    (hwj : w t = 0) (hw : ∀ i, i ≠ t → w i = (1 : ℝ) / 15) :
    ∃ c : Branch → ℝ, BranchWeights w ∧ TimeSilent w t ∧ TimeNeverSilent c t := by
  let c : Branch → ℝ := fun _ => 1
  refine ⟨c, ?_, ?_, ?_⟩
  · exact silence_weights_are_probability t w hwj hw
  · exact hwj
  · rfl

/-- 时间分支唯一性（§7.34 指派：时间分支 = §7.15 恰 1 个零权重分支）：
    在 A3/A4/A5 前提下恰有 1 个静默分支（时间分支），15 个可观测分支。 -/
theorem time_branch_uniqueness (k m : ℕ) (hdecomp : m + k = 16)
    (hk : 0 < k) (hwindow : S4 ≤ (1 : ℝ) / k)
    (hmax : Real.log (k : ℝ) = Real.log (15 : ℝ)) :
    m = 1 ∧ k = 15 :=
  exactly_one_silent_branch k m hdecomp hk hwindow hmax

/-! ## 指标 ③：演化参数 t 的单向演化骨架（A4 代数核心，预研独立重构） -/

/-- 时间演化结构（指标③，paper44 A4 代数核心）：
    以演化参数 t : ℝ 推进，静默指标 σ(t) 在分岔时刻 tStar 处
    由封闭（静默，true）瞬间切换为开放（解除，false）。 -/
structure TimeEvolution where
  tStar : ℝ
  silent : ℝ → Bool
  before : ∀ t : ℝ, t < tStar → silent t = true
  after : ∀ t : ℝ, tStar ≤ t → silent t = false

/-- 方向性（A4：t₁ < tStar < t₂ ⟹ σ_S3 单向 1 → 0，分岔瞬间完成，不可逆）——
    PhotonTopology.bifurcation_directional 的预研独立重构（代数核心同构）。 -/
theorem TimeEvolution.directional (E : TimeEvolution) (t₁ t₂ : ℝ)
    (h₁ : t₁ < E.tStar) (h₂ : E.tStar < t₂) :
    E.silent t₁ = true ∧ E.silent t₂ = false :=
  ⟨E.before t₁ h₁, E.after t₂ (le_of_lt h₂)⟩

/-- 过程性（A4 前段）：t < tStar 封闭拓扑类，静默完整。 -/
theorem TimeEvolution.before_silent (E : TimeEvolution) (t : ℝ) (h : t < E.tStar) :
    E.silent t = true := E.before t h

/-- 过程性（A4 后段）：t ≥ tStar 开放拓扑类，静默解除。 -/
theorem TimeEvolution.after_silent (E : TimeEvolution) (t : ℝ) (h : E.tStar ≤ t) :
    E.silent t = false := E.after t h

/-! ## 三指标综合：时间分支 = 静默分支 + 演化载体 -/

/-- 综合（§7.34）：时间分支（谱权重 0）同时承载单向演化（以 t 为参数）——
    指标①（谱静默）与指标③（演化单向）叠加在时间分支上，互不冲突。 -/
theorem time_branch_carries_evolution (w : Branch → ℝ) (t : Branch)
    (hw_silent : TimeSilent w t) (E : TimeEvolution) :
    TimeSilent w t ∧
      ∀ t₁ t₂ : ℝ, t₁ < E.tStar → E.tStar < t₂ →
        E.silent t₁ = true ∧ E.silent t₂ = false :=
  ⟨hw_silent, fun t₁ t₂ h₁ h₂ => E.directional t₁ t₂ h₁ h₂⟩

end PresurveyFormalization.TimeBranch
