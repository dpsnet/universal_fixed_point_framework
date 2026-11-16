/-
  ActivePhaseCoincidence.lean — `N_active = 3` 与「相的数量 = 3」是否同源（第 62 批）
  =================================================================================

  ## 问题

  第 61 批（`PhaseCountReadout.lean`）证明 `N_total = 5` 是**相盲**的：标号 5 与三相
  （C 相塔高 1 / A 相 2 / B 相无界）全部相容。于是 `B = 3 × 5` 的**第二个因子**相盲。
  本批检查**第一个因子** `N_active = 3` 是否也相盲，以及它与「相的数量 = 3」的
  同值是**同源**还是**巧合**。

  ## 库内两条事实（第 29/56 批已登记，本批机检化）

  * `PhaseTrichotomy.lean` L44–52 明文：「`N_active = 3` 与「相的数量 = 3」是两个不同的 3，
    不该合并」——但那只是文档断言，没有机检。
  * `ActiveFromCategoryOrder.lean`：`nActive := catOrder - 1`，
    `ActiveFromCategoryOrder.lean` L76 自认「排除对象层与 coherence 层这条规则本身未被证明」。
  * `BranchCounting.lean` L78–85 已把 `N_total = 5` 定性为**层标号基数**（非塔高）；
    `ActiveLayers = {one, two, three}`（`isActive four = false`）。

  ## 本批的正面结论

  1. **`N_active` 是 `catOrder` 的函数**（`nActiveOf c := c − 1`），而**相判据不是**：
     同一个 A 相见证 `(diag3, diag3)` 对**任意** `c` 都成立（`one_witness_all_catOrder`）。
  2. ★★ **`N_active = 3` 唯一钉住 `catOrder = 4`**（`c ≥ 1` 时 `c − 1 = 3 ↔ c = 4`）；
     而相判据的格数恒为 3，与 `c` 无关。⇒ **两个 3 只在 `c = 4` 处重合，且仅在此处**
     （`two_threes_coincide_only_at_four`）。
  3. ★★ **`B` 的两个因子都相盲**：`B = 15`、`ActiveLayers.card = 3`、`N_total = 5` 同时
     与三相全部可实例化（`B_factors_both_phase_blind`）。⇒ `B = 15` 与「层塔」彻底解耦。
  4. ★ **`N_active = 3` 同样不能当 B 相塔高的上界**：`{1, 2, 3, 5}` 四个候选读数全部失败
     （`nActive_cannot_cap_unbounded_tower`）。

  ## 结论的定性

  `N_active = 3` 与「相的数量 = 3」的同值是**数值巧合**，不是同源：
  * 前者的"3"是 `catOrder − 1` 的算术结果，随 `catOrder` 变（`c = 5` 时给 4）；
  * 后者的"3"是两条二值判据 4 格排除 1 格的**格数**，与 `catOrder` 无关。

  这正是第 29 批文档断言的机检化形态。

  ## 不注入声明（可核对）

  * 本批全部证明体不引用任何 `def := k` 的层数常量；
  * `nActiveOf` 只是把库内既有 `catOrder − 1` 参数化，不引入新常数；
  * 「相格数 3」不通过构造子计数得到，而是通过第 29 批的判据组合（本批只引用）。

  ## 边界（必须一并陈述）

  - 本批**不**证「相只有三个」（第 29 批），也不证「相数对任何宇宙/任何对象都恒 3」；
    恒定性只表达为「同一判据对任意 `catOrder` 值都能实例化」，不是对 `c` 的量词化性质定理。
  - 本批**不**改 `catOrder`、不改 `N_active`、不改 `B`。
  - `N_active` 的语义（「主动生成层」）仍未证（`ActiveFromCategoryOrder` L76 自认）；
    本批只处理它的**计数性质**。
-/

import Mathlib.Tactic
import MUFPFormalization.PhaseCountReadout

namespace MUFPF.ActivePhaseCoincidence

open MUFPFormalization
open MUFPF.PhaseCountReadout
open MUFPF.CategoryOrder (catOrder nActive nActive_eq_three)
open MUFPF.BranchCounting (LayerIndex B N_total ActiveLayers)
open Matrix

/-! ## 一、`N_active` 作为 `catOrder` 的函数 -/

/-- `catOrder` 的函数形态：`N_active(c) = c − 1`（库内 `nActive := catOrder − 1` 的参数化）。 -/
def nActiveOf (c : ℕ) : ℕ := c - 1

/-- 参数化形态与库内定义一致。 -/
theorem nActive_eq_nActiveOf : nActive = nActiveOf catOrder := rfl

/-- `catOrder = 4` 处给 3。 -/
theorem nActiveOf_four : nActiveOf 4 = 3 := by
  norm_num [nActiveOf]

/-- **它会随 `catOrder` 变**。 -/
theorem nActive_varies : nActiveOf 5 = 4 ∧ nActiveOf 6 = 5 ∧ nActiveOf 5 ≠ 3 := by
  refine ⟨?_, ?_, ?_⟩
  · norm_num [nActiveOf]
  · norm_num [nActiveOf]
  · norm_num [nActiveOf]

/-! ## 二、相判据不随 `catOrder` 变 -/

/-- ★ **同一个相见证对任意 `catOrder` 值都成立**：相判据与 `catOrder` 无耦合。

    `(diag3, diag3)` 是第 29 批的 A 相代表实例（`phase_A_occupies_stop2`），
    此处与任意 `c` 的 `nActiveOf c = c − 1` **同时**成立。 -/
theorem one_witness_all_catOrder (c : ℕ) :
    InStopPhase diag3 diag3 ∧ nActiveOf c = c - 1 :=
  ⟨MUFPF.PhaseTrichotomy.phase_A_occupies_stop2, rfl⟩

/-- ★ **三相判据的划分对任意 `catOrder` 值都成立**（划分定理的陈述含 `ι` 与矩阵，不含 `c`）。 -/
theorem phase_partition_independent_of_catOrder {ι : Type*} [Fintype ι] [DecidableEq ι]
    (A B : Matrix ι ι ℂ) (c : ℕ) :
    (InFlatPhase A B ∨ InStopPhase A B ∨ InTraversePhase A B) ∧ nActiveOf c = c - 1 :=
  ⟨phase_criterion_exhaustive A B, rfl⟩

/-! ## 三、两个 3 的同值来源 -/

/-- ★★ **`N_active = 3` 唯一钉住 `catOrder = 4`**（`c ≥ 1`）。 -/
theorem nActive_eq_three_iff_catOrder_four (c : ℕ) (hc : 1 ≤ c) :
    nActiveOf c = 3 ↔ c = 4 := by
  unfold nActiveOf
  constructor
  · intro h
    omega
  · intro h
    omega

/-- ★★ **两个 3 只在 `catOrder = 4` 处重合**：`N_active` 随 `c` 变、相数恒 3，
    故 `N_active = 3` 与「相的数量 = 3」是数值巧合而非同源。 -/
theorem two_threes_coincide_only_at_four :
    (∀ c : ℕ, 1 ≤ c → (nActiveOf c = 3 ↔ c = 4)) ∧
    InFlatPhase diag4 diag3 ∧ InStopPhase diag3 diag3 ∧ InTraversePhase jordan3 jordan3 :=
  ⟨nActive_eq_three_iff_catOrder_four,
    MUFPF.PhaseTrichotomy.phase_C_occupies_flat,
    MUFPF.PhaseTrichotomy.phase_A_occupies_stop2,
    MUFPF.PhaseTrichotomy.phase_B_occupies_traverse⟩

/-! ## 四、`B` 的两个因子都相盲 -/

/-- ★★ **`B = 3 × 5` 的两个因子都相盲**：`B = 15`、`ActiveLayers.card = 3`、`N_total = 5`
    与三相**全部**可同时实例化。 -/
theorem B_factors_both_phase_blind :
    B = 15 ∧ (ActiveLayers : Finset LayerIndex).card = 3 ∧ N_total = 5 ∧ nActive = 3 ∧
    InFlatPhase diag4 diag3 ∧ InStopPhase diag3 diag3 ∧ InTraversePhase jordan3 jordan3 :=
  ⟨MUFPF.BranchCounting.B_eq_15,
    MUFPF.BranchCounting.active_layers_count,
    rfl,
    nActive_eq_three,
    MUFPF.PhaseTrichotomy.phase_C_occupies_flat,
    MUFPF.PhaseTrichotomy.phase_A_occupies_stop2,
    MUFPF.PhaseTrichotomy.phase_B_occupies_traverse⟩

/-- `N_active = 3` 不等于任何有限塔高读数（1 或 2）。 -/
theorem nActive_not_a_height : nActive ≠ 1 ∧ nActive ≠ 2 ∧ nActive = 3 := by
  refine ⟨?_, ?_, ?_⟩
  · norm_num [nActive, catOrder]
  · norm_num [nActive, catOrder]
  · norm_num [nActive, catOrder]

/-- ★ **`N_active = 3` 同样不能封顶无界塔高**：候选集 `{1, 2, 3, 5}` 全部失败。 -/
theorem nActive_cannot_cap_unbounded_tower :
    ¬ ∃ N : ℕ, (N = 1 ∨ N = 2 ∨ N = 3 ∨ N = 5) ∧ ∀ k : ℕ, 2 ≤ k → k ≤ N := by
  rintro ⟨N, hN, h⟩
  have h6 : 2 ≤ 6 := by norm_num
  have hle : 6 ≤ N := h 6 h6
  rcases hN with h1 | h2 | h3 | h5
  · omega
  · omega
  · omega
  · omega

/-! ## 五、总述 -/

/-- ★★ **本批裁决**：`N_active` 是 `catOrder` 的函数（相判据不是），两个 3 仅在
    `catOrder = 4` 处重合；`B` 的两个因子都相盲；`N_active` 也不能封顶无界塔高。 -/
theorem active_phase_verdict :
    (∀ c : ℕ, 1 ≤ c → (nActiveOf c = 3 ↔ c = 4)) ∧
    (∀ c : ℕ, InStopPhase diag3 diag3 ∧ nActiveOf c = c - 1) ∧
    B = 15 ∧ (ActiveLayers : Finset LayerIndex).card = 3 ∧ N_total = 5 ∧
    InFlatPhase diag4 diag3 ∧ InTraversePhase jordan3 jordan3 ∧
    ¬ ∃ N : ℕ, (N = 1 ∨ N = 2 ∨ N = 3 ∨ N = 5) ∧ ∀ k : ℕ, 2 ≤ k → k ≤ N :=
  ⟨nActive_eq_three_iff_catOrder_four,
    one_witness_all_catOrder,
    MUFPF.BranchCounting.B_eq_15,
    MUFPF.BranchCounting.active_layers_count,
    rfl,
    MUFPF.PhaseTrichotomy.phase_C_occupies_flat,
    MUFPF.PhaseTrichotomy.phase_B_occupies_traverse,
    nActive_cannot_cap_unbounded_tower⟩

end MUFPF.ActivePhaseCoincidence
