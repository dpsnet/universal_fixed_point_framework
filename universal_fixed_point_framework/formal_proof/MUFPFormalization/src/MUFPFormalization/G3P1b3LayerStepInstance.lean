/-
  G3P1b3LayerStepInstance.lean — G3-P1b-3 层步输入的强度校准：非空性、外性不可去、定向 ⟹ 无有限阶
  ==========================================================================================

  **接 P7-5e-374（`G3P1b3DirectionalConverse.lean`）**：374 把方向性显式化为输入 `LayerStep`
  （每点「保持」或「+k」）与 `LayerAdvance`（每点 +k），并在「层对角皆内实现 + 外」下证出严格升层。
  本轮只做**强度校准**（不新增物理断言、不补位）：

  (i)   `LayerStep` **单独很弱**：恒等对**任意** k 都满足（`layerStep_refl`）——所以「层步」本身
        不强制定向；374 的升层结论**必须**由外性/非对角排除左支（`layerStep_nondiag_ascent`）。
  (ii)  反证外性不可去：`¬ ∀ σ k, LayerStep id σ k → ∃a, σ a = a + k`
        （`not_layerStep_imp_ascent`，取 σ = id、k = 1 即反例）。
  (iii) 非空性：`LayerStep` / `LayerAdvance` 在实际层前进 `advance k` 上有实例
        （`layerStep_advance` / `layerAdvance_advance`），不是空壳谓词。
  (iv)  强度：`LayerAdvance` 对恒等对任何 k ≠ 0 都失败（`layerAdvance_not_refl`），
        且**排除有限阶**：k ≠ 0、m ≠ 0 ⟹ `σ^m ≠ refl`（`layerAdvance_no_power_refl`）。
        与 368 的 `bnotEquiv_period_two` 对照：二阶置换可以是外、可以移动层，但**绝不可能是层前进**。

  **诚实边界（不证明、不补位）**

  - `LayerStep` / `LayerAdvance` 仍是**显式输入**，不是 Tomita `Δ_mod` 或 KMS β=1 的定理；
    「模流生成元非负 ⟹ 每步至多前进 k 层」**未形式化**。
  - 定向 ⟹ 无有限阶只对**给定的层泛函 L** 成立；模流本身仍是周期流（单位谱 `σ_{t+1}=σ_t`），
    因此「无周期」只读作递归层深的单向性，不是 t 上无周期。
  - 载体（RecObj 忠实正规态/模算子/状态空间）与 vN 完成性仍未定义 ⇒ P2 未成立、G3 未闭合；
    不关闭任何项（226 挂起、k(2) 开放）。
  - 框架原生 Δ（`spExchangeLaw` 交换律偏差）全程不出现、不赋值；`M=1` 只读作谱间隔归一 1。
-/

import Mathlib.Tactic
import MUFPFormalization.G3P1b3DirectionalConverse

namespace MUFPF.G3P1b3Witness

open MUFPF.G3P1b3Converse MUFPF.G3P1b3Directional

/-! ### 一、`LayerStep` 单独不强制定向 -/

/-- 恒等是任意 k 的层步（左支恒成立）⟹ 「层步」本身不含方向信息。 -/
theorem layerStep_refl {α : Type*} (L : α → ℕ) (k : ℕ) :
    LayerStep L (fun a => a) k :=
  fun _ => Or.inl rfl

/-- 非对角层步 ⟹ 存在严格升层点（把 374 证明里「排除左支」这一步单列）。 -/
theorem layerStep_nondiag_ascent {α : Type*} {L : α → ℕ} {σ : α → α} {k : ℕ}
    (hstep : LayerStep L σ k) (hnd : ¬ ∀ a : α, L (σ a) = L a) :
    ∃ a : α, L (σ a) = L a + k := by
  push Not at hnd
  obtain ⟨a, ha⟩ := hnd
  rcases hstep a with h | h
  · exact absurd h ha
  · exact ⟨a, h⟩

/-- ★★ 外性/非对角**不可去**：层步单独推不出升层（σ = id、k = 1 即反例）。 -/
theorem not_layerStep_imp_ascent :
    ¬ ∀ (σ : ℕ → ℕ) (k : ℕ), LayerStep (fun n : ℕ => n) σ k →
      ∃ a : ℕ, σ a = a + k := by
  intro h
  obtain ⟨a, ha⟩ := h (fun n => n) 1 (layerStep_refl (fun n : ℕ => n) 1)
  omega

/-! ### 二、非空性：与实际层前进对齐 -/

/-- 层前进 `advance k` 是层步（第二支）。 -/
theorem layerStep_advance (k : ℕ) :
    LayerStep (fun n : ℕ => n) (advance k) k :=
  fun _ => Or.inr rfl

/-- 层前进是强制前进。 -/
theorem layerAdvance_advance (k : ℕ) :
    LayerAdvance (fun n : ℕ => n) (advance k) k :=
  fun _ => rfl

/-! ### 三、强度：`LayerAdvance` 排除恒等与有限阶 -/

variable {R A : Type*} [CommSemiring R] [Ring A] [Algebra R A]

/-- 强制前进对恒等失败（k ≠ 0）。 -/
theorem layerAdvance_not_refl (L : A → ℕ) {k : ℕ} (hk : k ≠ 0) :
    ¬ LayerAdvance L (fun a => a) k := by
  intro h
  have h1 : L (0 : A) = L (0 : A) + k := h (0 : A)
  omega

/-- ★★ 强制前进 ⟹ 无有限阶：k ≠ 0、m ≠ 0 ⟹ `σ^m ≠ refl`。 -/
theorem layerAdvance_no_power_refl {L : A → ℕ} (σ : A ≃ₐ[R] A) {k : ℕ} (hk : k ≠ 0)
    (h : LayerAdvance L (σ : A → A) k) {m : ℕ} (hm : m ≠ 0) :
    iterateAut σ m ≠ AlgEquiv.refl := by
  intro he
  have hc := layerAdvance_iterate_no_return (L := L) σ k hk h hm (0 : A)
  rw [he] at hc
  exact hc rfl

/-- ★ 对照 368：二阶置换 `bnotEquiv` 不可能是非零强制层前进（方向与周期互斥）。 -/
theorem bnotEquiv_not_layerAdvance :
    ¬ ∃ k : ℕ, k ≠ 0 ∧ LayerAdvance boolLayer (bnotEquiv : Bool → Bool) k := by
  rintro ⟨k, _hk, h⟩
  have h1 := h false
  simp [boolLayer, bnotEquiv] at h1
  omega

/-- ★★★ 主定理：层步输入的强度校准（弱性 ∧ 非空性 ∧ 外性不可去 ∧ 与周期不相容）。 -/
theorem input_necessity :
    (∀ (L : ℕ → ℕ) (k : ℕ), LayerStep L (fun n : ℕ => n) k) ∧
    (∀ k : ℕ, LayerStep (fun n : ℕ => n) (advance k) k) ∧
    (∀ k : ℕ, LayerAdvance (fun n : ℕ => n) (advance k) k) ∧
    (¬ ∀ (σ : ℕ → ℕ) (k : ℕ), LayerStep (fun n : ℕ => n) σ k →
      ∃ a : ℕ, σ a = a + k) ∧
    (¬ ∃ k : ℕ, k ≠ 0 ∧ LayerAdvance boolLayer (bnotEquiv : Bool → Bool) k) :=
  ⟨layerStep_refl, layerStep_advance, layerAdvance_advance, not_layerStep_imp_ascent,
    bnotEquiv_not_layerAdvance⟩

end MUFPF.G3P1b3Witness
