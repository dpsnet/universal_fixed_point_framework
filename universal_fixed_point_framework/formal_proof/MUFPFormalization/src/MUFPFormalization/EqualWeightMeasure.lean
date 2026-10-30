/-
## EqualWeightMeasure.lean —— S531 等权公设内生化 Lean 锚（2026-10-29）

等权公设内生化（S531——脚本 s531_equal_weight_internalization.py 先证伪 PASS）：
  静默冻结（范畴公设：无演化）⟹ 概率分布不变（冻结 = 演化生成元作用平凡）
  + 无标号对象（S98：S_k 置换对称）⟹ 唯一不变测度 = 均匀 ⟹ 排列概率 1/k!
  ⟹ EGF 泊松系数（Σ_{k=0}^{8} 1/k! = 109601/40320——ExpTruncation.lean 已锚）

本文件锚定两个结构定理：
  ① 传递群唯一不变概率测度 = 均匀（perm_invariant_eq_constant +
     constant_probability_uniform + perm_invariant_unique_uniform）
  ② 冻结 ⟹ 分布不变（frozen_evolution_distribution_invariant）
  ③ 组合结构衔接（sym_group_card_factorial——|S_k| = k!）

依赖纪律：精细引入（Mathlib.Tactic + Mathlib.Data.Real.Basic + Equiv/Fintype 叶子模块），
  禁止 import Mathlib 全量引入。
-/
import Mathlib.Tactic
import Mathlib.Data.Real.Basic
import Mathlib.Logic.Equiv.Basic
import Mathlib.Data.Nat.Factorial.Basic
import Mathlib.Data.Fintype.Perm

noncomputable section

open scoped BigOperators

namespace EqualWeightMeasure

/-! ## 定义：概率分布与置换不变性 -/

/-- 概率分布：非负且和为 1（概率公理层）。 -/
def IsProbabilityDistribution {n : ℕ} (p : Fin n → ℝ) : Prop :=
  (∀ i, 0 ≤ p i) ∧ (∑ i, p i = 1)

/-- 置换不变性：S_k 群作用不改变分布（无标号对象——S98）。 -/
def PermInvariant {n : ℕ} (p : Fin n → ℝ) : Prop :=
  ∀ σ : Equiv.Perm (Fin n), ∀ i, p (σ i) = p i

/-- 冻结演化：静默层无演化（范畴公设语义——冻结 = 恒等作用）。 -/
def FrozenEvolution {n : ℕ} (E : Fin n → Fin n) : Prop :=
  ∀ i, E i = i

/-! ## 定理 1：置换不变 ⟹ 每点相等（传递性——swap 生成对称群） -/

/-- 置换不变 ⟹ 每点相等（对称群传递作用——swap 生成元）。 -/
theorem perm_invariant_eq_constant {n : ℕ} (p : Fin n → ℝ)
    (h : PermInvariant p) : ∀ i j : Fin n, p i = p j := by
  intro i j
  by_cases hij : i = j
  · rw [hij]
  · have hs := h (Equiv.swap i j) i
    have hswap : (Equiv.swap i j) i = j := Equiv.swap_apply_left i j
    rw [hswap] at hs
    exact hs.symm

/-! ## 定理 2：等常量 + 和为 1 ⟹ 每点 = 1/n -/

/-- 等常量分布且和为 1 ⟹ 每点概率 = 1/n（n 非空）。 -/
theorem constant_probability_uniform {n : ℕ} (hn : n ≠ 0) (p : Fin n → ℝ)
    (hconst : ∀ i j : Fin n, p i = p j) (hsum : ∑ i, p i = 1) :
    ∀ i, p i = (1 : ℝ) / n := by
  intro i
  let i0 : Fin n := ⟨0, Nat.pos_of_ne_zero hn⟩
  have hc : p i = p i0 := hconst i i0
  have hsumc : ∑ j : Fin n, p i0 = 1 := by
    rw [← hsum]
    apply Finset.sum_congr rfl
    intro j hj
    exact hconst i0 j
  have hnsum : ∑ j : Fin n, p i0 = (n : ℝ) * p i0 := by
    rw [Finset.sum_const]
    simp
  have hnmul : (n : ℝ) * p i0 = 1 := by
    rw [← hnsum, hsumc]
  have hcval : p i0 = (1 : ℝ) / n := by
    field_simp [hn]
    simpa [mul_comm] using hnmul
  calc
    p i = p i0 := hc
    _ = (1 : ℝ) / n := hcval

/-! ## 定理 3：置换不变概率分布 ⟹ 均匀（传递群唯一不变测度） -/

/-- ★ 传递群唯一不变概率测度 = 均匀（S531 核心结构定理）。
    置换不变 + 概率分布 ⟹ 每点概率 = 1/n。 -/
theorem perm_invariant_unique_uniform {n : ℕ} (hn : n ≠ 0) (p : Fin n → ℝ)
    (hprob : IsProbabilityDistribution p) (hinv : PermInvariant p) :
    ∀ i, p i = (1 : ℝ) / n := by
  exact constant_probability_uniform hn p
    (perm_invariant_eq_constant p hinv) hprob.2

/-! ## 定理 4：冻结 ⟹ 分布不变（静默层演化平凡） -/

/-- ★ 冻结演化（恒等作用）⟹ 概率分布不变（S531：静默冻结纯内生论证）。 -/
theorem frozen_evolution_distribution_invariant {n : ℕ} (p : Fin n → ℝ)
    (E : Fin n → Fin n) (hE : FrozenEvolution E) :
    ∀ i, p (E i) = p i := by
  intro i
  simp [hE i]

/-! ## 定理 5：均匀分布是概率分布（窗口等权求和——概率公理层） -/

/-- 均匀分布 ∑_i (1/n) = 1（n 非空——window_equal_weights_sum 的推广）。 -/
theorem uniform_distribution_sum_eq {n : ℕ} (hn : n ≠ 0) :
    (∑ _ : Fin n, (1 : ℝ) / n) = 1 := by
  rw [Finset.sum_const]
  simp [hn]

/-! ## 定理 6：组合结构衔接——|S_k| = k!（无标号对象排列计数——S98） -/

/-- ★ |S_k| = k!：k 个对象无标号排列计数（Fintype.card_perm——S98 组合结构层）。 -/
theorem sym_group_card_factorial (k : ℕ) :
    Fintype.card (Equiv.Perm (Fin k)) = Nat.factorial k := by
  simp [Fintype.card_perm]

/-! ## 定理 7：均匀分布置换不变性（自洽闭环——等权确实满足对称） -/

/-- 均匀分布满足置换不变（等权测度 = 对称群不动点——自洽性）。 -/
theorem uniform_perm_invariant {n : ℕ} :
    PermInvariant (fun _ : Fin n => (1 : ℝ) / n) := by
  intro σ _
  simp

end EqualWeightMeasure
