/-
  G3P1b3DirectionalConverse.lean — G3-P1b-3 真逆向的条件形式：层步定向 ⟹ 严格升层
  ==========================================================================================

  **接 P7-5e-368（`G3P1b3ConverseModular.lean`）**：368 已机检「外 ⟹ 模权不可被内实现吸收」
  （`outer_not_diagonal` / `outer_moves_modular_weight`），但**没有做**「外 ⟹ 严格升层」：
  后者需要一层**方向性**——每步只能「保持」或「前进 k 层」，不能后退。方向性在物理侧来自
  KMS β=1 下模流生成元 `M ≥ 0` 的符号（Stone：`σ_t = Ad e^{−2πitM}`），**本模块把它作为
  显式输入 `LayerStep` 写出来，不从 Δ_mod/KMS 导出**（诚实边界见下）。

  **本模块机检的链条（条件形式）**

  (i)   层步定义：`LayerStep L σ k := ∀ a, L (σ a) = L a ∨ L (σ a) = L a + k`；
        `k = 0` 时两支重合 ⟹ 退化为「层对角」（`layerStep_zero_iff`）。
  (ii)  定向逆向：若层对角自同构皆内实现（`hdiag_inner`，与 368 同口径），则**外 + 层步
        ⟹ 严格升层**：存在 a 使 `L (σ a) = L a + k`（`layerStep_outer_ascent`）。
  (iii) 模权后果：严格升层 ⟹ 该元素模权改变（`layerStep_outer_weight_moves`）；
        gap > 0 时模权**严格下降**（`ascent_weight_decreases`，`e^{−2π·gap·k} < 1`）。
  (iv)  单向桥接：若更强制地每点都前进 k（`LayerAdvance`），则 m 步迭代给出
        `L (σ^m a) = L a + m·k = advanceIter k m (L a)`（`layerAdvance_iterate` /
        `layerAdvance_iterate_eq_advanceIter`），k ≠ 0、m ≠ 0 时无回退
        （`layerAdvance_iterate_no_return`）。这把 368 的 `advanceIter_no_return` 接到
        具体层泛函上，**不宣称由外性推出单向**（P1a' `p1a_no_cycle` 已机检）。
  (v)   反例（定向性是真输入）：Bool 层泛函 `boolLayer` 下，非恒等置换 `bnotEquiv`
        移动层（`bnotEquiv_moves_layer`），但**不是任何 k 的层步**
        （`bnotEquiv_not_directed`）——「外/非对角」本身给不出方向。

  **诚实边界（不证明、不补位）**

  - `LayerStep` / `LayerAdvance` 是**显式输入**，不是从 Tomita `Δ_mod` 或 KMS β=1 推出的定理；
    「模流生成元非负 ⟹ 每步至多前进 k 层」这一步**未形式化**。
  - 载体（RecObj 忠实正规态/模算子/状态空间）与 vN 完成性仍未定义 ⇒ P2 未成立、G3 未闭合；
    不关闭任何项（226 挂起、k(2) 开放）。
  - 框架原生 Δ（`spExchangeLaw` 交换律偏差）全程不出现、不赋值；`M=1` 只读作谱间隔归一 1。
-/

import Mathlib.Tactic
import MUFPFormalization.G3P1b3ConverseModular

namespace MUFPF.G3P1b3Directional

open MUFPF.G3P1b3Converse

/-- 层步：σ 在每一点要么**保持**层，要么**前进 k 层**（不后退）。
    方向性（`+k` 而非任意移动）是显式输入，见模块头部「诚实边界」。 -/
def LayerStep {α : Type*} (L : α → ℕ) (σ : α → α) (k : ℕ) : Prop :=
  ∀ a : α, L (σ a) = L a ∨ L (σ a) = L a + k

/-- 强制层前进：每点都恰好 `+k` 层（比 `LayerStep` 强）。 -/
def LayerAdvance {α : Type*} (L : α → ℕ) (σ : α → α) (k : ℕ) : Prop :=
  ∀ a : α, L (σ a) = L a + k

/-- 自同构的 m 次迭代（只用于桥接 `advanceIter`，避免依赖群幂 API）。 -/
def iterateAut {R A : Type*} [CommSemiring R] [Semiring A] [Algebra R A]
    (σ : A ≃ₐ[R] A) : ℕ → A ≃ₐ[R] A
  | 0 => AlgEquiv.refl
  | m + 1 => (iterateAut σ m).trans σ

/-- 迭代一步的取值：`(σ^{m+1}) a = σ ((σ^m) a)`。 -/
theorem iterateAut_succ_apply {R A : Type*} [CommSemiring R] [Semiring A] [Algebra R A]
    (σ : A ≃ₐ[R] A) (m : ℕ) (a : A) :
    iterateAut σ (m + 1) a = σ (iterateAut σ m a) := by
  simp [iterateAut, AlgEquiv.trans_apply]

/-- `k = 0` 的层步两支重合 ⟹ 恰好是「层对角」。 -/
theorem layerStep_zero_iff {α : Type*} (L : α → ℕ) (σ : α → α) :
    LayerStep L σ 0 ↔ ∀ a : α, L (σ a) = L a := by
  simp [LayerStep]

/-- 强制前进 ⟹ 层步。 -/
theorem layer_step_of_advance {α : Type*} {L : α → ℕ} {σ : α → α} {k : ℕ}
    (h : LayerAdvance L σ k) : LayerStep L σ k :=
  fun a => Or.inr (h a)

variable {R A : Type*} [CommSemiring R] [Ring A] [Algebra R A]

/-- 外自同构不可能是恒等（恒等由单位 `1` 内实现）。 -/
theorem outer_ne_refl (σ : A ≃ₐ[R] A) (hout : IsOuterAut σ) : σ ≠ AlgEquiv.refl := by
  intro h
  apply hout
  refine ⟨1, fun a => ?_⟩
  have ha : σ a = a := by rw [h]; rfl
  rw [ha]
  simp

/-- ★★ 定向逆向（严格升层）：层对角皆内实现 ⟹ 外 + 层步 ⟹ 存在元素被抬高 k 层。 -/
theorem layerStep_outer_ascent {L : A → ℕ} (σ : A ≃ₐ[R] A) (k : ℕ)
    (hstep : LayerStep L (σ : A → A) k)
    (hdiag_inner : ∀ τ : A ≃ₐ[R] A, (∀ a, L (τ a) = L a) → InnerRealization τ)
    (hout : IsOuterAut σ) : ∃ a : A, L (σ a) = L a + k := by
  have hnd := outer_not_diagonal (L := L) σ hdiag_inner hout
  push Not at hnd
  obtain ⟨a, ha⟩ := hnd
  rcases hstep a with h | h
  · exact absurd h ha
  · exact ⟨a, h⟩

/-- ★★ 严格升层 ⟹ 模权改变（gap ≠ 0 时的单射性推论）。 -/
theorem layerStep_outer_weight_moves {L : A → ℕ} (σ : A ≃ₐ[R] A) (k : ℕ) (hk : k ≠ 0)
    (hstep : LayerStep L (σ : A → A) k)
    (hdiag_inner : ∀ τ : A ≃ₐ[R] A, (∀ a, L (τ a) = L a) → InnerRealization τ)
    (hout : IsOuterAut σ) (gap : ℝ) (hgap : gap ≠ 0) :
    ∃ a : A, modularWeight gap (L (σ a)) ≠ modularWeight gap (L a) := by
  obtain ⟨a, ha⟩ := layerStep_outer_ascent (L := L) σ k hstep hdiag_inner hout
  refine ⟨a, fun hw => ?_⟩
  have hEq : L (σ a) = L a := modularWeight_injective gap hgap hw
  omega

/-- ★ 方向量化：gap > 0 时，前进 k 层使模权**严格下降**（层权比 `e^{−2π·gap·k} < 1`）。 -/
theorem ascent_weight_decreases (gap : ℝ) (hgap : 0 < gap) {n k : ℕ} (hk : k ≠ 0) :
    modularWeight gap (n + k) < modularWeight gap n := by
  have hkpos : (0 : ℝ) < (k : ℝ) := by exact_mod_cast Nat.pos_of_ne_zero hk
  have hpi : 0 < Real.pi := Real.pi_pos
  have h2 : (0 : ℝ) < 2 := by norm_num
  have hprod : 0 < 2 * Real.pi * gap * (k : ℝ) :=
    mul_pos (mul_pos (mul_pos h2 hpi) hgap) hkpos
  have hneg : -(2 * Real.pi * gap * (k : ℝ)) < 0 := by linarith
  have hexp : Real.exp (-(2 * Real.pi * gap * (k : ℝ))) < 1 := by
    have h := (Real.exp_lt_exp (x := -(2 * Real.pi * gap * (k : ℝ))) (y := 0)).2 hneg
    simpa using h
  have hw : modularWeight gap (n + k) =
      modularWeight gap n * Real.exp (-(2 * Real.pi * gap * (k : ℝ))) := by
    rw [modularWeight_add]
    simp [modularWeight]
  have hposw : 0 < modularWeight gap n := by
    rw [modularWeight]
    exact Real.exp_pos _
  rw [hw]
  simpa using mul_lt_mul_of_pos_left hexp hposw

/-- ★★ 单向桥接：每点前进 k ⟹ m 步后恰为 `L a + m·k`。 -/
theorem layerAdvance_iterate {L : A → ℕ} (σ : A ≃ₐ[R] A) (k : ℕ)
    (h : LayerAdvance L (σ : A → A) k) (m : ℕ) (a : A) :
    L (iterateAut σ m a) = L a + m * k := by
  induction m with
  | zero => simp [iterateAut]
  | succ m ih =>
      rw [iterateAut_succ_apply, h, ih, Nat.succ_mul]
      omega

/-- ★★ 与 368 的 `advanceIter` 对齐：迭代的层作用 = `advanceIter k m (L a)`。 -/
theorem layerAdvance_iterate_eq_advanceIter {L : A → ℕ} (σ : A ≃ₐ[R] A) (k : ℕ)
    (h : LayerAdvance L (σ : A → A) k) (m : ℕ) (a : A) :
    L (iterateAut σ m a) = advanceIter k m (L a) := by
  rw [layerAdvance_iterate (L := L) σ k h m a, advanceIter_eq]

/-- ★★ 无回退（层泛函版）：k ≠ 0、m ≠ 0 ⟹ 迭代后回到原层不可能。 -/
theorem layerAdvance_iterate_no_return {L : A → ℕ} (σ : A ≃ₐ[R] A) (k : ℕ) (hk : k ≠ 0)
    (h : LayerAdvance L (σ : A → A) k) {m : ℕ} (hm : m ≠ 0) (a : A) :
    L (iterateAut σ m a) ≠ L a := by
  rw [layerAdvance_iterate (L := L) σ k h m a]
  intro hc
  have hmk : m * k = 0 := by omega
  exact (Nat.mul_ne_zero hm hk) hmk

/-- ★★★ 主定理（条件逆向打包）：层对角皆内实现时，外 + 非零层步 ⟹
    严格升层 ∧ 模权改变 ∧ 非恒等。 -/
theorem directional_converse {L : A → ℕ} (gap : ℝ) (hgap : gap ≠ 0)
    (hdiag_inner : ∀ τ : A ≃ₐ[R] A, (∀ a, L (τ a) = L a) → InnerRealization τ) :
    ∀ (σ : A ≃ₐ[R] A) (k : ℕ), k ≠ 0 → LayerStep L (σ : A → A) k → IsOuterAut σ →
      (∃ a : A, L (σ a) = L a + k) ∧
      (∃ a : A, modularWeight gap (L (σ a)) ≠ modularWeight gap (L a)) ∧
      σ ≠ AlgEquiv.refl := by
  intro σ k hk hstep hout
  exact ⟨layerStep_outer_ascent (L := L) σ k hstep hdiag_inner hout,
    layerStep_outer_weight_moves (L := L) σ k hk hstep hdiag_inner hout gap hgap,
    outer_ne_refl σ hout⟩

/-! ### 反例：定向性是真输入（非对角/外本身给不出方向） -/

/-- Bool 二点层泛函：`true ↦ 0`、`false ↦ 1`。 -/
def boolLayer (b : Bool) : ℕ := if b then 0 else 1

/-- `bnotEquiv` 确实移动层（不是层对角）。 -/
theorem bnotEquiv_moves_layer : boolLayer (bnotEquiv false) ≠ boolLayer false := by
  simp [boolLayer, bnotEquiv]

/-- ★★ 但 `bnotEquiv` 不是任何 k 的层步（它同时「后退」）⟹ 方向不能由置换结构自动得到。 -/
theorem bnotEquiv_not_directed :
    ¬ ∃ k : ℕ, LayerStep boolLayer (bnotEquiv : Bool → Bool) k := by
  rintro ⟨k, hk⟩
  have h := hk false
  simp [boolLayer, bnotEquiv] at h
  omega

end MUFPF.G3P1b3Directional
