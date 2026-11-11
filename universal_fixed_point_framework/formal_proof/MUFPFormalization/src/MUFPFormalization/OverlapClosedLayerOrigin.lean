/-
OverlapClosedLayerOrigin.lean — A（RecSpOverlap）的候选空间归位
=======================================================

问题（第 26 批登记的「整条链最软一环」）
--------------------------------------
第 26 批用两条结构前提 A、B 逼出 m = 3：

  A｜RecSpOverlap k := 2 ^ (k - 2) = k ^ 2
  B｜BottDoubling k m := k = 2 ^ m

但 A 本身只有代数形式，没有来由：为什么 Rec 的 2 幂与 Sp 的平方
必须在塔截断处重合？当时登记为未闭合。

本模块的答案（第 27 批）
----------------------
A 不是凭空假设。它的候选空间早已被库里一条独立机检定理限死：

  SigmaIntersectionBottTower.sigma_intersection_closed
    交汇方程 N·(2j − N) = 2^j − 1  （k_max = 2j）
    的整数解只有 j ∈ {1, 2, 4}，
    即 k_max ∈ {2, 4, 8} —— 三个封闭层。

  该定理的证明依赖 SigmaIntersectionBottTower.bound_prod：
    N·(2j − N) = j² − (N − j)² ≤ j²
  这条恒等式正是「Sp 侧平方」的真正来源：j² 是二次型 N·(2j − N) 的
  极大值，等号取在对称点 N = j。

于是 A 的作用不是「假设一个巧合」，而是「在三个封闭层里筛一个」：
  k_max = 2 → 2^0 = 1 ≠ 2^2 = 4      A 不成立
  k_max = 4 → 2^2 = 4 ≠ 4^2 = 16     A 不成立
  k_max = 8 → 2^6 = 64 = 8^2 = 64    A 成立（唯一）

本模块机检这一点：overlap_on_closed_layers。

进一步的读法（vieta_step_gives_pow_sq）
--------------------------------------
交汇方程的每个解都有 |N − j| = 1（N 取 j ± 1），此时
  (j − 1)·(j + 1) = j² − 1 = 2^j − 1  ⇒  j² = 2^j
而 j² = 2^j 的解是 j ∈ {2, 4}。所以两个封闭层 4 与 8 都满足
「Sp 二次型极值 = Rec 2 幂」这一弱形式；A 用指数 k − 2（而不是
对称形式）把 j = 2 那一支排掉，只留下 j = 4。

  j = 2：j² = 2^(2j−4) 即 4 = 2^0 = 1      不成立
  j = 4：j² = 2^(2j−4) 即 16 = 2^4 = 16     成立

这说明 A 的强度恰好足以区分「平方 = 平方的退化重合」与
「平方 = 2 幂的真重合」。

边界（与结论同时陈述）
--------------------
1. 本模块不证明 A。A 仍是前提。本模块证明的是：A 的候选空间已被
   独立机检的封闭层枚举限成 {2, 4, 8}，且 A 在该集合上唯一选中 8。
   A 从「对任意 k 的假设」降为「在三候选中筛选」——这是强度下降，
   不是证明。
2. 「为什么必须取最深封闭层」仍未闭合。本模块只给出
   「若要求 Sp 二次型极值与 Rec 2 幂相等，则只能是 8」，
   不给出「为什么框架必须要求这个相等」。这一条继续登记为缺口。
3. 本模块与 j² = 2^j 的 j = 2 分支无关：A 在 k_max = 4 处不成立，
   已由 overlap_neg_four 机检。

先证伪再证明（模式 8）
--------------------
scripts/pr634ob_falsify.py：交汇解集 {2,4,8}；A 在 k=1..16 仅 k=1（退化）
与 k=8 成立；封闭层上只有 8；bound_prod 恒等式抽查 6/6；|N−j|=1 时
j² = 2^j 在 j=2,4 均成立；j²=2^j 解为 {2,4}；A 半指数形式仅 j=4。
VERDICT_ALL_OK = True
-/

import Mathlib.Tactic
import MUFPFormalization.ActiveLayerDerivation
import MUFPFormalization.SigmaIntersectionBottTower

namespace MUFPF.OverlapClosedLayer

open MUFPF.ActiveLayerDerivation
open MUFPF.BottTower

/-! =========================================================
    ① 封闭层枚举以 k_max = 2j 形式导出（引用已有机检定理）
    ========================================================= -/

/-- σ 交汇方程的解给出 k_max = 2j ∈ {2, 4, 8}。
    本条只是 SigmaIntersectionBottTower.sigma_intersection_closed 的
    k_max 形式重述——它把「封闭层只有三层」变成可机检锚点。 -/
theorem closed_kmax_candidates (j N : ℕ) (hN1 : 1 ≤ N) (hNlt : N < 2 * j)
    (hEq : N * (2 * j - N) = 2 ^ j - 1) :
    2 * j = 2 ∨ 2 * j = 4 ∨ 2 * j = 8 := by
  have h := MUFPF.SigmaIntersection.sigma_intersection_closed j N hN1 hNlt hEq
  rcases h with h1 | h2 | h4
  · left; rw [h1]
  · right; left; rw [h2]
  · right; right; rw [h4]

/-! =========================================================
    ② A 在三个封闭层上的取值（唯一选中 8）
    ========================================================= -/

/-- k = 2 不满足 A：2^0 = 1 ≠ 2^2 = 4。 -/
theorem overlap_neg_two : ¬ RecSpOverlap 2 := by
  unfold RecSpOverlap
  norm_num

/-- k = 4 不满足 A：2^2 = 4 ≠ 4^2 = 16。 -/
theorem overlap_neg_four : ¬ RecSpOverlap 4 := by
  unfold RecSpOverlap
  norm_num

/-- k = 8 满足 A：2^6 = 64 = 8^2。 -/
theorem overlap_pos_eight : RecSpOverlap 8 := by
  unfold RecSpOverlap
  norm_num

/-- **A 的候选空间归位**：在封闭层集合 {2, 4, 8} 中，A 只在 k = 8 成立。 -/
theorem overlap_on_closed_layers (k : ℕ) (hk : k = 2 ∨ k = 4 ∨ k = 8)
    (hA : RecSpOverlap k) : k = 8 := by
  rcases hk with rfl | rfl | rfl
  · exact absurd hA overlap_neg_two
  · exact absurd hA overlap_neg_four
  · rfl

/-- 合并陈述：A 在封闭层上恰选中最大的一层。 -/
theorem overlap_selects_max_closed :
    (RecSpOverlap 8 ∧ ¬ RecSpOverlap 2 ∧ ¬ RecSpOverlap 4) ∧
    (∀ k : ℕ, (k = 2 ∨ k = 4 ∨ k = 8) → RecSpOverlap k → k = 8) := by
  refine ⟨⟨overlap_pos_eight, overlap_neg_two, overlap_neg_four⟩, ?_⟩
  intro k hk hA
  exact overlap_on_closed_layers k hk hA

/-! =========================================================
    ③ 交汇取 N = j ± 1 时的退化形式：j² = 2^j
    ========================================================= -/

/-- 交汇方程在 |N − j| = 1 处退化为 (j−1)(j+1) = 2^j − 1，展开即 j² = 2^j。
    本条给出「Sp 二次型极值 = Rec 2 幂」的弱形式（加法形式，避免 Nat 减法）。 -/
theorem vieta_step_gives_pow_sq (j : ℕ) (hj : 1 ≤ j)
    (h : (j - 1) * (j + 1) + 1 = 2 ^ j) : j ^ 2 = 2 ^ j := by
  have hfac : (j - 1) * (j + 1) + 1 = j ^ 2 := by
    cases j with
    | zero => omega
    | succ n =>
      simp
      ring
  rw [hfac] at h
  exact h

/-! =========================================================
    ④ 最终归位陈述
    ========================================================= -/

/-- **A 的来由**：A 一旦成立，k 必是三个封闭层中最大的那一个。
    把 A 与「封闭层只有 {2,4,8}」两条合起来读：
    A 不是假设一个巧合，而是在独立机检的三候选中筛出 8。 -/
theorem overlap_lies_on_max_closed_layer (k : ℕ) (hk2 : 2 ≤ k)
    (hA : RecSpOverlap k) : k = 8 ∧ (k = 2 ∨ k = 4 ∨ k = 8) := by
  have h8 : k = 8 := MUFPF.KMaxAlgebra.kmax_unique k hk2 hA
  exact ⟨h8, Or.inr (Or.inr h8)⟩

end MUFPF.OverlapClosedLayer
