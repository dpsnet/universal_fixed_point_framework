/-
  G3P1b3ConverseModular.lean — G3-P1b-3 真逆向：模哈密顿量 M 的单位层间隔 ⟹ 模权不可内吸收
  ==========================================================================================

  **记号（P7-5e-368，按用户更正）**：文献侧 **M = 模哈密顿量**（自伴算子，Tomita–Takesaki），
  `Δ_mod = e^{−2πM}`，模流 `σ_t = Ad Δ_mod^{it} = Ad e^{−2πitM}`；M 是流的生成元
  （`Δ_mod^{it} = e^{−2πitM}`，Stone）。**M 不是可任取值的标量系数**——367 的数值结论
  （`Δ_mod = e^{−2π}`、层权比 `e^{−2π}`、K 每层 2π）保持不变，但「M=1」的正确读法是
  **模哈密顿量在层塔上的谱间隔归一为 1**（`spec M = ℤ`，相邻层 `m_{n+1}−m_n = 1`），
  不是把某个标量赋值为 1。框架原生 Δ（`spExchangeLaw` 交换律偏差）全程不出现、不赋值。

  **本模块的模型**：M 取对角（层塔），`m_n = gap · n + const`；只保留**谱间隔 gap**
  （常数项在模权中给出整体归一，不影响层间比）。层 n 的模权 = `e^{−2π·m_n}`，
  相邻层比 = `e^{−2π·gap}`。gap ≠ 0 ⟺ M 在层塔上非平凡 ⟺ 模权单射。

  **机检的三层结构**

  (i)   模权层：`modularWeight gap n = e^{−(2π·gap)n}`；gap ≠ 0 ⟹ 层权单射；
        相邻层比 `e^{−2π·gap}`，gap = 1（单位层间隔，M = N）⟹ `e^{−2π}`。
  (ii)  刚性层：保持全部层权的层置换必为恒等（单射性推论）；故「层移动」=「模权移动」。
  (iii) 条件逆向：若「层对角自同构皆为内实现」，则外自同构 ⟹ 非层对角 ⟹
        存在元素其模权改变（**外性 ⟹ 模权不可被内实现吸收**）；再叠加**单向层作用**
        （每步前进 k ≠ 0 层）⟹ 任意 m ≠ 0 步回不到原层、模权也回不到原值。

  **诚实边界（不证明、并给出反例结构）**

  - **外性单独 ⟹ 无周期 是假命题**：非平凡层置换可以有限阶（`bnotEquiv` 二阶）；
    外性（非对角）与周期性相容。单向性必须作为独立结构输入（与 P1a `StrictLayer` 同源）。
  - **模流本身是周期的**：单位层间隔下 `σ_{t+1} = σ_t`（`Δ_mod^{it}` 参数周期 1/m）。
    故 P1b-3 的「无周期」只能读作**递归层深的单向性**（P1a 口径），不能读作模流在 t 上无周期；
    「深度记录走了多远，相位记录是否闭合」（342 的互补结构）在此再次成立。
  - 载体（RecObj 忠实正规态/模算子/状态空间）与 vN 完成性仍未定义 ⇒ P2 未成立、
    G3 未闭合；不关闭任何项（226 挂起、k(2) 开放）。
-/

import Mathlib.Tactic
import Mathlib.Data.Complex.Basic

namespace MUFPF.G3P1b3Converse

/-- 模权：层 n 的模权 `e^{−(2π·gap)n}`。
    `gap` = 模哈密顿量 M 在层塔上的相邻谱间隔（`m_{n+1}−m_n`）；M 自身为自伴算子，
    本模块只取其谱。 -/
noncomputable def modularWeight (gap : ℝ) (n : ℕ) : ℝ := Real.exp (-(2 * Real.pi * gap * (n : ℝ)))

/-- 第 0 层模权 = 1。 -/
theorem modularWeight_zero (gap : ℝ) : modularWeight gap 0 = 1 := by
  simp [modularWeight]

/-- 相邻层模权比 = `e^{−2π·gap}`（gap = 1 时 = `e^{−2π}`，与 365/367 一致）。 -/
theorem modularWeight_succ (gap : ℝ) (n : ℕ) :
    modularWeight gap (n + 1) = modularWeight gap n * Real.exp (-(2 * Real.pi * gap)) := by
  rw [modularWeight, modularWeight, ← Real.exp_add]
  congr 1
  push_cast
  ring

/-- 层权加法分解：`w(n+k) = w(n) · w(k)`。 -/
theorem modularWeight_add (gap : ℝ) (n k : ℕ) :
    modularWeight gap (n + k) = modularWeight gap n * modularWeight gap k := by
  rw [modularWeight, modularWeight, modularWeight, ← Real.exp_add]
  congr 1
  push_cast
  ring

/-- ★ 谱间隔 gap ≠ 0 ⟹ 层权单射：不同层的模权不同。 -/
theorem modularWeight_injective (gap : ℝ) (hgap : gap ≠ 0) :
    Function.Injective (modularWeight gap) := by
  intro n m h
  have harg : -(2 * Real.pi * gap * (n : ℝ)) = -(2 * Real.pi * gap * (m : ℝ)) :=
    Real.exp_injective h
  have hcast : (n : ℝ) = (m : ℝ) := by
    have hcoef : 2 * Real.pi * gap ≠ 0 := by
      exact mul_ne_zero (mul_ne_zero (by norm_num) (ne_of_gt Real.pi_pos)) hgap
    have hmul : 2 * Real.pi * gap * ((n : ℝ) - (m : ℝ)) = 0 := by linarith
    rcases mul_eq_zero.mp hmul with hzero | hzero
    · exact absurd hzero hcoef
    · linarith
  exact Nat.cast_injective hcast

/-- ★ n ≠ 0 ⟹ 第 n 层模权 ≠ 第 0 层模权。 -/
theorem modularWeight_step_ne (gap : ℝ) (hgap : gap ≠ 0) {n : ℕ} (hn : n ≠ 0) :
    modularWeight gap n ≠ modularWeight gap 0 := by
  intro h
  exact hn (modularWeight_injective gap hgap h)

/-- gap = 0（M 在层塔上为常数）⟹ 全部层权坍缩为 1：单射性失效，
    「谱间隔 ≠ 0」是必要前提（M = c·1 时模流平凡）。 -/
theorem modularWeight_degenerate (n : ℕ) : modularWeight 0 n = 1 := by
  simp [modularWeight]

/-- ★ 单位层间隔（gap = 1，M = 层数算子 N）⟹ 单层模权比 `e^{−2π}`。 -/
theorem modularWeight_unit_gap :
    modularWeight 1 1 = Real.exp (-(2 * Real.pi)) := by
  rw [modularWeight]
  norm_num

/-- ★★ 刚性：保持全部层权的层置换必为恒等（层权单射的直接推论）。 -/
theorem weight_perm_rigid (gap : ℝ) (hgap : gap ≠ 0) (τ : ℕ ≃ ℕ)
    (h : ∀ n, modularWeight gap (τ n) = modularWeight gap n) : τ = Equiv.refl ℕ := by
  ext n
  exact modularWeight_injective gap hgap (h n)

/-- ★★ 逆否读法：非恒等的层置换必移动某一层的模权。 -/
theorem weight_perm_moves (gap : ℝ) (hgap : gap ≠ 0) (τ : ℕ ≃ ℕ)
    (h : τ ≠ Equiv.refl ℕ) : ∃ n, modularWeight gap (τ n) ≠ modularWeight gap n := by
  by_contra hc
  push Not at hc
  exact h (weight_perm_rigid gap hgap τ hc)

/-! ### 单向层作用：每步前进 k ≠ 0 层 ⟹ 无回退（递归深度单向） -/

/-- 单向层步：`advance k n = n + k`。 -/
def advance (k : ℕ) (n : ℕ) : ℕ := n + k

/-- m 步单向迭代（递归定义，避免依赖迭代算子 API）。 -/
def advanceIter (k : ℕ) : ℕ → ℕ → ℕ
  | 0, n => n
  | m + 1, n => advance k (advanceIter k m n)

/-- 迭代闭式：`advanceIter k m n = n + m·k`。 -/
theorem advanceIter_eq (k m n : ℕ) : advanceIter k m n = n + m * k := by
  induction m with
  | zero => simp [advanceIter]
  | succ m ih =>
      simp [advanceIter, ih, advance, Nat.succ_mul]
      omega

/-- ★★ 无回退：k ≠ 0 且 m ≠ 0 ⟹ m 步后回不到原层（递归深度单向，无周期）。 -/
theorem advanceIter_no_return (k n : ℕ) (hk : k ≠ 0) {m : ℕ} (hm : m ≠ 0) :
    advanceIter k m n ≠ n := by
  rw [advanceIter_eq]
  intro h
  have hmk : m * k = 0 := by omega
  rcases Nat.mul_eq_zero.mp hmk with h1 | h1
  · exact hm h1
  · exact hk h1

/-- ★★ 模权随单向步移动：k ≠ 0、m ≠ 0 ⟹ 模权 ≠ 原值（权重的无周期读法）。 -/
theorem advanceIter_weight_moves (gap : ℝ) (hgap : gap ≠ 0) (k n : ℕ) (hk : k ≠ 0)
    {m : ℕ} (hm : m ≠ 0) : modularWeight gap (advanceIter k m n) ≠ modularWeight gap n := by
  rw [advanceIter_eq]
  have hmk : m * k ≠ 0 := Nat.mul_ne_zero hm hk
  intro h
  have hnm : n + m * k = n := modularWeight_injective gap hgap h
  exact hmk (by omega)

/-! ### 条件逆向：外性 ⟹ 模权不可被内实现吸收 -/

variable {R A : Type*} [CommSemiring R] [Ring A] [Algebra R A]

/-- 内实现：σ 由代数内部单位的共轭实现（OC2 口径，与 P1b 定义层同形）。 -/
def InnerRealization (σ : A ≃ₐ[R] A) : Prop :=
  ∃ u : Aˣ, ∀ a : A, σ a = (u : A) * a * ((u⁻¹ : Aˣ) : A)

/-- 外自同构：不存在代数内部单位实现。 -/
def IsOuterAut (σ : A ≃ₐ[R] A) : Prop := ¬ InnerRealization σ

/-- 层移动 ⟹ 外（与 P1b-1/P1b-2 的 `isOuter_of_layer_shift` 同形）。 -/
theorem isOuter_of_layer_shift {L : A → ℕ}
    (hL : ∀ (u : Aˣ) (a : A), L ((u : A) * a * ((u⁻¹ : Aˣ) : A)) = L a)
    (σ : A ≃ₐ[R] A) (a₀ : A) (hshift : L (σ a₀) ≠ L a₀) : IsOuterAut σ := by
  intro hin
  obtain ⟨u, hu⟩ := hin
  refine hshift ?_
  rw [hu a₀]
  exact hL u a₀

/-- ★★ 条件逆向（结构层）：若层对角自同构皆为内实现，则外自同构必非层对角。 -/
theorem outer_not_diagonal {L : A → ℕ} (σ : A ≃ₐ[R] A)
    (hdiag_inner : ∀ τ : A ≃ₐ[R] A, (∀ a, L (τ a) = L a) → InnerRealization τ)
    (hout : IsOuterAut σ) : ¬ ∀ a, L (σ a) = L a := by
  intro hd
  exact hout (hdiag_inner σ hd)

/-- ★★★ 条件逆向主定理：外性 + 模权单射（谱间隔 ≠ 0）⟹ 存在元素其模权改变
    ——「外」不能被任何内实现吸收成层权守恒。 -/
theorem outer_moves_modular_weight {L : A → ℕ} (σ : A ≃ₐ[R] A) (gap : ℝ) (hgap : gap ≠ 0)
    (hdiag_inner : ∀ τ : A ≃ₐ[R] A, (∀ a, L (τ a) = L a) → InnerRealization τ)
    (hout : IsOuterAut σ) : ∃ a, modularWeight gap (L (σ a)) ≠ modularWeight gap (L a) := by
  have hnd := outer_not_diagonal (L := L) σ hdiag_inner hout
  push Not at hnd
  obtain ⟨a, ha⟩ := hnd
  exact ⟨a, fun hw => ha (modularWeight_injective gap hgap hw)⟩

/-! ### 反例结构：非平凡层置换可以有限阶（「外 ⟹ 无周期」不成立）

`bnotEquiv` 是 Bool 上的非恒等置换（层 0 ↔ 层 1），但二阶（`τ² = id`）。
配合单射模权，它移动模权（w(1) ≠ w(0)），却仍是周期置换——说明**单向性是
独立输入**，不能由「非对角/外」单独推出。 -/

/-- Bool 上的非恒等置换（层 0 ↔ 层 1）。 -/
def bnotEquiv : Bool ≃ Bool where
  toFun := Bool.not
  invFun := Bool.not
  left_inv b := by cases b <;> rfl
  right_inv b := by cases b <;> rfl

/-- 非恒等：`bnotEquiv ≠ refl`。 -/
theorem bnotEquiv_ne_refl : bnotEquiv ≠ Equiv.refl Bool := by
  intro h
  have h' := congrArg (fun e : Bool ≃ Bool => e true) h
  simp [bnotEquiv] at h'

/-- 二阶：`bnotEquiv · bnotEquiv = refl`（周期 2）。 -/
theorem bnotEquiv_period_two :
    bnotEquiv.trans bnotEquiv = Equiv.refl Bool := by
  ext b
  cases b <;> rfl

end MUFPF.G3P1b3Converse
