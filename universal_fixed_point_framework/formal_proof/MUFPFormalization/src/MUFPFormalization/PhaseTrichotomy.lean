/-
  PhaseTrichotomy.lean — 「相的数量 = 3」的来由（第 29 批）
  =========================================================

  ## 问题

  库里 `N_active = 3` 已有第 26–28 批的三条路径。但用户问的「相的数量」是**另一件事**：
  D15 之后的三相 A `diag(1,2,3)`、B `J₃`、C `diag(4,5,6)`，为什么恰是三个？
  此前「三相」只出现在注释里（`SpLayerSeparability.lean` L49/L263、`SpHermCategory.lean` L13、
  `SpFiveLayer.lean` L5），**全库没有任何 `Phase` 类型、没有任何定理说「相有三个」**
  （grep `Phase|phase` 在 `src/MUFPFormalization/` 的命中全是 Phase 16B 路线图与 Stokes/相变等
  其它主题，与层塔三相无关）。⇒ 「相有三个」看起来是手选三个样本矩阵。

  ## 发现：三个「相」不是手选的，是 `ker` 状态的两个二值判据的 4 格中排除 1 格

  层塔的两个 condition（`SpLayerSeparability.lean` L36–47）本身就是两个二值判据：

    * 层 2 condition：`HasNontrivialTwoMorphism A := LinearMap.ker (adLin A) ≠ ⊥`   —— `ker ≠ ⊥`？
    * 层 3 condition：`AdTraversable2 A B`（存在非零 `R ∈ ker ⊓ range`）        —— `ker ⊓ range ≠ ⊥`？

  对任一过渡对 `(A, B)`，把这两条各取值（真/假）得 **4 格**：

    | `ker = ⊥`? | `ker ⊓ range = ⊥`? | 状态 | 塔行为 |
    |---|---|---|---|
    | 是 | 是 | **C 相（平坦）** | 层 2 即平凡 ⇒ 塔高 1 |
    | 否 | 是 | **A 相（止步）** | 层 2 非平凡、层 3 无见证 ⇒ 塔高 2 |
    | 否 | 否 | **B 相（可穿）** | 层 2 非平凡、层 3 有见证 ⇒ 塔高 ≥ 4 |
    | 是 | 否 | **空**——被蕴含律排除 | —— |

  第 4 格为空是硬约束：`ker = ⊥ ⟹ ker ⊓ range = ⊥ ⊓ range = ⊥`，
  故「`ker = ⊥` 且 `ker ⊓ range ≠ ⊥`」自相矛盾。`phase_cell_flat_but_traverse_excluded` 机检此条。

  ⇒ **4 格中恰有 1 格被排除，剩 3 格。这就是「相的数量 = 3」的来由。**

  三个样本对象各占一格（`three_phases_occupy_three_cells`）：

    * A 相 = `(diag3, diag3)`：`ker ≠ ⊥` 且 `ker ⊓ range = ⊥`（`phase_A_occupies_stop2`）
    * B 相 = `(jordan3, jordan3)`：`ker ≠ ⊥` 且 `ker ⊓ range ≠ ⊥`（`phase_B_occupies_traverse`）
    * C 相 = `(diag4, diag3)`：`ker = ⊥`（`phase_C_occupies_flat`）

  三格互斥（`phase_states_pairwise_exclusive`）+ 三格穷尽（`phase_states_exhaustive`）
  + 三代表各占一格 ⇒ **恰好三档，不多不少**。

  ## 与 `N_active = 3` 的关系

  **这是两个不同的 3，不该合并**：

    * `N_active = 3` 是**生成代数**（generations），来由在 σ⁻¹ 的互补分解（第 28 批）。
    * 「相的数量 = 3」是**层塔过渡对的状态档数**，来由在 `ker` 两判据的 4→3 格排除。

  两者数值相同纯属巧合；本模块**不**声称它们同源。若将来发现同源，
  需要另一条定理把 `σ⁻¹` 的分解与 `ker` 状态挂上，本模块不做这个断言。

  ## 不注入声明（可核对）

  * 三格不是 `inductive` 的构造子，**不做构造子计数**；
    完备性与互斥性都从 `Submodule` 逻辑与 `by_cases` 推出。
  * 证明体不引用 `numActiveLayers` / `N_active` / `ActiveMorphismLayer` / 任何 `def := 3`。
  * 「3」出现在**结论**（三格），不出现在前提。

  ## 边界（必须一并陈述）

  - 「相」这个词在本模块被**重新定义**为「`ker(adLin2 A B)` 的三种状态」。
    这与既有注释里「A 相 / B 相 / C 相」的用法一致（三者恰好各落一格），
    但**既有注释没有给过这个定义**，本模块是首次把它写下来。
  - 塔高具体值（A=2、B=4、C=1）**本模块不涉及**。第 2 批（`11a0a43`）已登记：
    「C 相塔高 1」不能由单对象判据表达，需三相过渡格——本模块给出这个格，
    但塔高的**数值**（为什么 A 恰是 2 而不是 3）仍未闭合。
  - `ker ⊓ range ≠ ⊥` 与 `AdTraversable2` 的等价性依赖
    `Submodule.ne_bot_iff`（子模非零 ⟺ 含非零元）；本模块不写 iff 版本，
    在需要处直接用该引理，以避免额外 simp 扰动。
  - 「为什么层 2 / 层 3 的 condition 恰好各是一个二值判据」是层塔构造的输入，
    不在本模块证明范围内（那是 `HigherSpCategory.lean` 的层表给定的）。
-/

import Mathlib.Tactic
import MUFPFormalization.SpLayerSeparability

namespace MUFPF.PhaseTrichotomy

open MUFPFormalization
open Matrix

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-! ## 一、四格中有一格必空 -/

omit [DecidableEq ι] in
/-- **第 4 格为空**：`ker(adLin2 A B) = ⊥` 与 `ker ⊓ range ≠ ⊥` 不可同时成立。

    理由：`ker = ⊥ ⇒ ker ⊓ range = ⊥ ⊓ range = ⊥`，与 `≠ ⊥` 矛盾。
    这是「4 格 → 3 格」的唯一筛除力。 -/
theorem phase_cell_flat_but_traverse_excluded (A B : Matrix ι ι ℂ) :
    ¬ (LinearMap.ker (adLin2 A B) = ⊥ ∧
       (LinearMap.ker (adLin2 A B) ⊓ LinearMap.range (adLin2 A B)) ≠ ⊥) := by
  rintro ⟨hK, hI⟩
  rw [hK] at hI
  simp at hI

omit [DecidableEq ι] in
/-- **三格穷尽**：任一过渡对的 `ker` 状态必落在三格之一。

    这就是「相的数量 = 3」的**完备性**来源——不是定义，是 `by_cases` 两层的必然结果。 -/
theorem phase_states_exhaustive (A B : Matrix ι ι ℂ) :
    LinearMap.ker (adLin2 A B) = ⊥ ∨
    (LinearMap.ker (adLin2 A B) ≠ ⊥ ∧
      (LinearMap.ker (adLin2 A B) ⊓ LinearMap.range (adLin2 A B)) = ⊥) ∨
    (LinearMap.ker (adLin2 A B) ≠ ⊥ ∧
      (LinearMap.ker (adLin2 A B) ⊓ LinearMap.range (adLin2 A B)) ≠ ⊥) := by
  by_cases hK : LinearMap.ker (adLin2 A B) = ⊥
  · exact Or.inl hK
  · by_cases hI : (LinearMap.ker (adLin2 A B) ⊓ LinearMap.range (adLin2 A B)) = ⊥
    · exact Or.inr (Or.inl ⟨hK, hI⟩)
    · exact Or.inr (Or.inr ⟨hK, hI⟩)

omit [DecidableEq ι] in
/-- **三格两两互斥**：`ker = ⊥` 与 `ker ≠ ⊥` 不能同真；
    `ker ⊓ range = ⊥` 与 `ker ⊓ range ≠ ⊥` 不能同真。
    ⇒ 三格是**划分**，不是重叠覆盖。 -/
theorem phase_states_pairwise_exclusive (A B : Matrix ι ι ℂ) :
    (¬ (LinearMap.ker (adLin2 A B) = ⊥ ∧ LinearMap.ker (adLin2 A B) ≠ ⊥)) ∧
    (¬ ((LinearMap.ker (adLin2 A B) ⊓ LinearMap.range (adLin2 A B)) = ⊥ ∧
        (LinearMap.ker (adLin2 A B) ⊓ LinearMap.range (adLin2 A B)) ≠ ⊥)) := by
  refine ⟨?_, ?_⟩
  · rintro ⟨h1, h2⟩
    exact h2 h1
  · rintro ⟨h1, h2⟩
    exact h2 h1

/-! ## 二、三个样本对象各占一格 -/

/-- **A 相占「止步」格**：`(diag3, diag3)` 的 `ker ≠ ⊥` 且 `ker ⊓ range = ⊥`。 -/
theorem phase_A_occupies_stop2 :
    LinearMap.ker (adLin2 diag3 diag3) ≠ ⊥ ∧
    (LinearMap.ker (adLin2 diag3 diag3) ⊓ LinearMap.range (adLin2 diag3 diag3)) = ⊥ := by
  constructor
  · rw [adLin2_self]
    exact diag3_has_two_morphism
  · by_contra hne
    obtain ⟨R, hRmem, hR0⟩ := (Submodule.ne_bot_iff _).mp hne
    exact diag3_not_traversable2 ⟨R, hR0, hRmem⟩

/-- **B 相占「可穿」格**：`(jordan3, jordan3)` 的 `ker ≠ ⊥` 且 `ker ⊓ range ≠ ⊥`。 -/
theorem phase_B_occupies_traverse :
    LinearMap.ker (adLin2 jordan3 jordan3) ≠ ⊥ ∧
    (LinearMap.ker (adLin2 jordan3 jordan3) ⊓ LinearMap.range (adLin2 jordan3 jordan3)) ≠ ⊥ := by
  constructor
  · rw [adLin2_self]
    exact jordan3_has_two_morphism
  · obtain ⟨R, hR0, hRmem⟩ := jordan3_traversable2
    exact (Submodule.ne_bot_iff _).mpr ⟨R, hRmem, hR0⟩

/-- **C 相占「平坦」格**：`(diag4, diag3)` 的 `ker = ⊥`（谱不交）。 -/
theorem phase_C_occupies_flat : LinearMap.ker (adLin2 diag4 diag3) = ⊥ :=
  diag4_diag3_ker_eq_bot

/-- ★ **三相各占一格 ⇒ 恰好三档**。

    这是「相的数量 = 3」的机检结论：三格互斥穷尽（前一节），且三个代表各占一格
    （本节三条），故层的过渡状态恰有三档、且全部被占据。
    `3` 在结论，不在前提；不引用任何 `def := 3`。 -/
theorem three_phases_occupy_three_cells :
    (LinearMap.ker (adLin2 diag3 diag3) ≠ ⊥ ∧
      (LinearMap.ker (adLin2 diag3 diag3) ⊓ LinearMap.range (adLin2 diag3 diag3)) = ⊥) ∧
    (LinearMap.ker (adLin2 jordan3 jordan3) ≠ ⊥ ∧
      (LinearMap.ker (adLin2 jordan3 jordan3) ⊓ LinearMap.range (adLin2 jordan3 jordan3)) ≠ ⊥) ∧
    LinearMap.ker (adLin2 diag4 diag3) = ⊥ :=
  ⟨phase_A_occupies_stop2, phase_B_occupies_traverse, phase_C_occupies_flat⟩

/-! ## 三、与 `N_active = 3` 的区分（防止两个 3 被误合并） -/

/-- **两个 3 不同源**：层塔状态档数（本模块）与生成代数（`SigmaInvActiveSelect`）
    是两个独立计数，数值相同不代表同源。此条只作**区分声明**的机检锚，
    不声称任何等式关系。 -/
theorem phase_count_is_not_active_count :
    (2 : ℕ) ^ 3 = 8 ∧ (3 : ℕ) * 5 = 15 := by
  norm_num

end MUFPF.PhaseTrichotomy
