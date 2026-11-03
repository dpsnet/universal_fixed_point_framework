/-
  G3P1b3LocalDiagonal.lean — G3-P1b-3 逆向链：局部化 `hdiag_inner`（全局假设降为单点假设）
  ==========================================================================================

  **接 P7-5e-368 / 374 / 375**：368 的 `outer_not_diagonal` / `outer_moves_modular_weight` 与
  374 的 `layerStep_outer_ascent` / `directional_converse` 都用了**全局假设**

      `hdiag_inner : ∀ τ, (∀ a, L (τ a) = L a) → InnerRealization τ`

  （「**所有**层对角自同构皆内实现」）。本轮把它**局部化**：只对具体 σ 假设

      `LocalInnerOn L σ : LayerDiagonal L σ → InnerRealization σ`

  并配合 `hout : IsOuterAut σ`（`IsOuterAut := ¬ InnerRealization`，368 定义）证出**同样的**
  严格升层、模权改变、非恒等结论（`local_directional_converse`）。同时给出
  `global_implies_local`（全局 ⟹ 局部，故 368/374 的结论是本轮特例）。

  **机检的链条**

  (i)   层对角谓词：`LayerDiagonal L σ := ∀ a, L (σ a) = L a`；与 374 的 `LayerStep L σ 0`
        等价（`layerDiagonal_iff_layerStep_zero`），与「不移动任何层」等价
        （`layerDiagonal_iff_no_move`）；恒等恒为层对角（`layerDiagonal_refl`）。
  (ii)  局部假设：`LocalInnerOn L σ`；恒等自同构自动满足（`localInnerOn_refl`，单位 `1`
        给出内实现），故局部假设**不是**空壳谓词。
  (iii) 局部逆向：`local_outer_not_diagonal`（局部内 + 外 ⟹ σ 非层对角）；
        `local_layerStep_outer_ascent`（再加层步 ⟹ 存在元素被抬高 k 层）；
        `local_layerStep_outer_weight_moves`（k ≠ 0、gap ≠ 0 ⟹ 模权改变）；
        `local_directional_converse`（三支打包）。
  (iv)  与全局的关系：`global_implies_local`（单向；本模块**不声称**逆命题）。
        `local_not_imply_global`：局部假设**严格弱于**全局假设——在谓词层给出反例
        （只在一处要求「对角 ⟹ 内」，别处不要求），故「局部化」有真实内容。

  **诚实边界（不证明、不补位）**

  - 局部化只**削弱假设**，不新增物理断言：`LocalInnerOn` 与 `IsOuterAut` 仍是显式前提，
    `LayerStep` 仍是显式输入（未从 `Δ_mod` 或 KMS 导出）；「模流生成元非负 ⟹ 每步至多前进 k 层」**未形式化**。
  - `local_not_imply_global` 是**谓词层**反例（说明局部/全局不是等价形式），不是代数层
    的「存在某 σ 局部可内实现而另一对角 τ 外」构造——后者需要具体外自同构实例，
    本轮不构造、不声称。
  - 载体（RecObj 忠实正规态/模算子/状态空间）与 vN 完成性仍未定义 ⇒ P2 未成立、G3 未闭合；
    不关闭任何项（226 挂起、k(2) 开放）。
  - 框架原生 Δ（`spExchangeLaw` 交换律偏差）全程不出现、不赋值；`M=1` 只读作谱间隔归一 1。
-/

import Mathlib.Tactic
import MUFPFormalization.G3P1b3DirectionalConverse

namespace MUFPF.G3P1b3Local

open MUFPF.G3P1b3Converse MUFPF.G3P1b3Directional

/-! ### 一、层对角谓词及其等价形式 -/

/-- 层对角：σ 保持每个元素的层。 -/
def LayerDiagonal {α : Type*} (L : α → ℕ) (σ : α → α) : Prop :=
  ∀ a : α, L (σ a) = L a

/-- 层对角 ⟺ 「不存在被移动的层」（非对角即存在移动点）。 -/
theorem layerDiagonal_iff_no_move {α : Type*} (L : α → ℕ) (σ : α → α) :
    LayerDiagonal L σ ↔ ¬ ∃ a : α, L (σ a) ≠ L a := by
  constructor
  · intro h
    rintro ⟨a, ha⟩
    exact ha (h a)
  · intro h a
    by_contra hc
    exact h ⟨a, hc⟩

/-- 恒等是层对角。 -/
theorem layerDiagonal_refl {α : Type*} (L : α → ℕ) :
    LayerDiagonal L (fun a => a) :=
  fun _ => rfl

/-- 层对角 ⟺ 374 的零步层步（`LayerStep L σ 0`）。 -/
theorem layerDiagonal_iff_layerStep_zero {α : Type*} (L : α → ℕ) (σ : α → α) :
    LayerDiagonal L σ ↔ LayerStep L σ 0 :=
  (layerStep_zero_iff L σ).symm

/-! ### 二、局部化假设：只对给定 σ 要求「层对角 ⟹ 内实现」 -/

variable {R A : Type*} [CommSemiring R] [Ring A] [Algebra R A]

/-- 局部内实现假设：**只对给定 σ** 假设「若 σ 层对角则内实现」。 -/
def LocalInnerOn (L : A → ℕ) (σ : A ≃ₐ[R] A) : Prop :=
  LayerDiagonal L (σ : A → A) → InnerRealization σ

/-- ★ 全局 ⟹ 局部：368/374 的全局 `hdiag_inner` 是本轮假设的特例。 -/
theorem global_implies_local {L : A → ℕ}
    (h : ∀ τ : A ≃ₐ[R] A, LayerDiagonal L (τ : A → A) → InnerRealization τ)
    (σ : A ≃ₐ[R] A) : LocalInnerOn L σ :=
  h σ

/-- ★ 局部假设非空壳：恒等自同构由单位 `1` 内实现，故自动满足。 -/
theorem localInnerOn_refl {L : A → ℕ} :
    LocalInnerOn L (AlgEquiv.refl : A ≃ₐ[R] A) := by
  intro _
  refine ⟨1, fun a => ?_⟩
  simp

/-! ### 三、局部逆向：与 368/374 同结论，但只用单点假设 -/

/-- ★★ 局部逆向（结构层）：局部内实现假设 + 外 ⟹ σ 不是层对角。 -/
theorem local_outer_not_diagonal {L : A → ℕ} (σ : A ≃ₐ[R] A)
    (hloc : LocalInnerOn L σ) (hout : IsOuterAut σ) :
    ¬ LayerDiagonal L (σ : A → A) := by
  intro hd
  exact hout (hloc hd)

/-- ★★ 局部逆向（严格升层）：局部内 + 外 + 层步 ⟹ 存在元素被抬高 k 层。 -/
theorem local_layerStep_outer_ascent {L : A → ℕ} (σ : A ≃ₐ[R] A) (k : ℕ)
    (hstep : LayerStep L (σ : A → A) k)
    (hloc : LocalInnerOn L σ) (hout : IsOuterAut σ) :
    ∃ a : A, L (σ a) = L a + k := by
  have hnd : ¬ ∀ a : A, L (σ a) = L a := local_outer_not_diagonal (L := L) σ hloc hout
  push Not at hnd
  obtain ⟨a, ha⟩ := hnd
  rcases hstep a with h | h
  · exact absurd h ha
  · exact ⟨a, h⟩

/-- ★★ 局部逆向（模权后果）：k ≠ 0、gap ≠ 0 ⟹ 存在元素其模权改变。 -/
theorem local_layerStep_outer_weight_moves {L : A → ℕ} (σ : A ≃ₐ[R] A) (k : ℕ) (hk : k ≠ 0)
    (hstep : LayerStep L (σ : A → A) k)
    (hloc : LocalInnerOn L σ) (hout : IsOuterAut σ) (gap : ℝ) (hgap : gap ≠ 0) :
    ∃ a : A, modularWeight gap (L (σ a)) ≠ modularWeight gap (L a) := by
  obtain ⟨a, ha⟩ := local_layerStep_outer_ascent (L := L) σ k hstep hloc hout
  refine ⟨a, fun hw => ?_⟩
  have hEq : L (σ a) = L a := modularWeight_injective gap hgap hw
  omega

/-- ★★★ 局部化主定理：局部内 + 外 + 非零层步 ⟹ 严格升层 ∧ 模权改变 ∧ 非恒等。 -/
theorem local_directional_converse {L : A → ℕ} (gap : ℝ) (hgap : gap ≠ 0) :
    ∀ (σ : A ≃ₐ[R] A) (k : ℕ), k ≠ 0 → LayerStep L (σ : A → A) k →
      LocalInnerOn L σ → IsOuterAut σ →
      (∃ a : A, L (σ a) = L a + k) ∧
      (∃ a : A, modularWeight gap (L (σ a)) ≠ modularWeight gap (L a)) ∧
      σ ≠ AlgEquiv.refl := by
  intro σ k hk hstep hloc hout
  exact ⟨local_layerStep_outer_ascent (L := L) σ k hstep hloc hout,
    local_layerStep_outer_weight_moves (L := L) σ k hk hstep hloc hout gap hgap,
    outer_ne_refl σ hout⟩

/-! ### 四、局部 ≠ 全局：局部化是严格弱化 -/

/-- ★★ 局部假设**严格弱于**全局假设：谓词层反例（D true = False、D false = True、
    I ≡ False、σ = true 时，单点蕴含成立而全局蕴含失败）。故本模块的局部化有真实内容，
    但它**不**声称「局部 ⟹ 全局」。 -/
theorem local_not_imply_global :
    ¬ ∀ (D I : Bool → Prop) (σ : Bool), (D σ → I σ) → ∀ τ : Bool, D τ → I τ := by
  intro h
  have h1 : (fun b : Bool => b = false) true → (fun _ : Bool => False) true := by
    intro hc
    exact absurd hc (by simp)
  exact h (fun b : Bool => b = false) (fun _ : Bool => False) true h1 false rfl

end MUFPF.G3P1b3Local
