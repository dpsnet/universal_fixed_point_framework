/-
  TowerHeightFromPhase.lean — 塔高 1 / 2 / 无界 由三相格决定（第 30 批）
  ==================================================================

  ## 问题

  第 29 批（`PhaseTrichotomy.lean`）把「相的数量 = 3」落成 `ker(adLin2 A B)` 的三种状态
  （4 格排除 1 格），但**没有**给出塔高的来由。该批在模块头里写「B 相塔高 ≥ 4」——
  这是**旧口径**，已过时，本批订正。

  ## 库内塔高的权威口径是 1 / 2 / 无界，不是 4

    * `SpTowerLayer4.lean` L63 `tower_height_A2_B4`：A 塔高 = 2、B **≥ 4**（阶段性结论）
    * `SpTowerWitness.lean` L125 `tower_height_at_least_five_B`：B 塔高 **≥ 5**（具体实例链）
    * `SpTowerUnbounded.lean` L62 `tower_height_trichotomy`：**塔高只取 1 / 2 / 无界**；
      「恰为 4」「恰为 5」**不成立**（层 5 用同一判据同样允许 `R = J₃`）

  ⇒ 「B 相塔高 = 4」是**已被否证**的命题。第 29 批把它写进模块头是错的，本批订正为「无界」。

  ## 塔高 = f(三相格)：本批给出的机制

  第 29 批的两个判据要**统一到跨对象算子 `adLin2 A B`** 才能给出塔高。
  这不是本批的发明——`SpLayerSeparability.lean` L332–334 已明确裁决：

  > 「这是层 3 condition 的原始形态……因此 `AdTraversable2` 是三相判据的统一形式；
  >  `AdTraversable A` 只是 `A = B`（同谱）的退化特例。」

  顺着这条裁决，层 2 判据也取 `ker(adLin2 A B) ≠ ⊥`（同对象时 `adLin2 A A = adLin A`，
  由 `adLin2_self` 退化为既有 `HasNontrivialTwoMorphism`，故与库内定义兼容）。

  于是三格直接给出塔高：

    | 格 | `ker(adLin2 A B)` | `ker ⊓ range` | 层 2 见证 | 层 3 见证 | 塔高 |
    |---|---|---|---|---|---|
    | 平坦 | `= ⊥` | `= ⊥`（自动） | **无** | 无 | **1** |
    | 止步 | `≠ ⊥` | `= ⊥` | 有 | **无** | **2** |
    | 可穿 | `≠ ⊥` | `≠ ⊥` | 有 | 有 | **无界** |

  这就是此前缺的机制：
    * **C 相塔高 1** 的来由 = 跨对象 `ker(adLin2 diag4 diag3) = ⊥` ⇒ 层 2 判据落空。
      这填了 `SpLayerSeparability.lean` L510–517 登记的缺口
      （`diag4_same_single_object_verdict`：单对象判据对 C 相与 A 相给出**完全相同**判决，
      故塔高 1 不能由单对象判据表达）。本批用跨对象口径把它表达出来。
    * **A 相塔高 2** = 层 2 有见证、层 3 无见证。
    * **B 相塔高无界** = 层 3 有见证，且判据层号无关（`SpFiveLayer.layer_condition_level_free`）。

  ## 与既有 `tower_height_trichotomy` 的一致性

  `tower_height_trichotomy : LayerWitness jordan3 ∧ ¬ LayerWitness diag3` 是**同对象**口径
  （`LayerWitness` 用 `HasConditionForm A A R` + `adLin A R = 0`），它只说「A 止步、B 不停」。
  本批是**跨对象**口径，且能额外分出 C 相的「1」。两者不冲突：
  同对象口径下 C 相与 A 相不可分，跨对象口径下可分——这正是本批的价值。

  ## 不注入声明（可核对）

  * 三个塔高档位（1 / 2 / 无界）**不是**定义的三个构造子，而是三格判据的直接后果：
    「无层 2 见证」/「有层 2 见证且无层 3 见证」/「有层 3 见证」。
  * 证明体不引用 `LayerWitness` 的构造子、不引用任何 `def := k` 的塔高数值。
  * 三相的塔高（1 / 2 / 无界）全部由第 29 批的格归属（`phase_*_occupies_*`）流转而来，
    没有为塔高另设前提。

  ## 边界（必须一并陈述）

  - 「塔高 1」在本批的含义是**「层 2 判据落空，故无任何非零层 2 见证」**，
    不是数字 1 的某种算术。若要把它读成「层数 = 1」，需另给「层数」的类型定义，
    本批不提供（库内无层索引类型，层是结构嵌套而非编号）。
  - 「无界」在本批的含义仍是 `SpFiveLayer.lean` L14–18 的口径：
    「判据层号无关 + 缺陷决定塔高」，**不是**「塔有无穷多层」（那是结构公设）。
  - 本批**不**证「层 6 起结构存在」；也**不**证 `tower_height_at_least_five_B` 之外的东西。
  - 把层 2 判据提升为跨对象 `ker(adLin2 A B)` 是**口径选择**，依据是库内既有裁决
    （跨对象是原始形态、同对象是退化特例）。若将来认为层 2 必须坚持单对象，
    则 C 相塔高 1 会退回不可表达状态——这是本批依赖的那条裁决的代价。
-/

import Mathlib.Tactic
import MUFPFormalization.SpLayerSeparability
import MUFPFormalization.PhaseTrichotomy

namespace MUFPF.TowerFromPhase

open MUFPFormalization
open Matrix

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-! ## 一、补第 29 批留下的 iff -/

omit [DecidableEq ι] in
/-- **`AdTraversable2` ⟺ `ker ⊓ range ≠ ⊥`**：`AdTraversable2` 的「存在非零见证」
    与子模「非零」等价（`Submodule.ne_bot_iff`）。

    第 29 批因担心 simp 扰动未写此条，只在使用处直接调 `Submodule.ne_bot_iff`；
    本批它成为塔高机制的枢纽，故正式写出。 -/
theorem AdTraversable2_iff_inf_ne_bot (A B : Matrix ι ι ℂ) :
    AdTraversable2 A B ↔
      (LinearMap.ker (adLin2 A B) ⊓ LinearMap.range (adLin2 A B)) ≠ ⊥ := by
  unfold AdTraversable2
  constructor
  · rintro ⟨R, hRne, hRmem⟩
    exact (Submodule.ne_bot_iff _).mpr ⟨R, hRmem, hRne⟩
  · intro h
    obtain ⟨R, hRmem, hRne⟩ := (Submodule.ne_bot_iff _).mp h
    exact ⟨R, hRne, hRmem⟩

/-! ## 二、三格 ⇒ 三类塔高判据 -/

omit [DecidableEq ι] in
/-- **平坦格：层 2 判据落空**。`ker = ⊥` ⇒ 不存在非零元落在 `ker` 中。

    这是「塔高 1」的全部内容：不是数字 1，而是「没有层 2 见证」。 -/
theorem flat_cell_no_layer2_witness (A B : Matrix ι ι ℂ)
    (hK : LinearMap.ker (adLin2 A B) = ⊥) :
    ¬ ∃ R : Matrix ι ι ℂ, R ≠ 0 ∧ R ∈ LinearMap.ker (adLin2 A B) := by
  rintro ⟨R, hRne, hRmem⟩
  rw [hK] at hRmem
  rw [Submodule.mem_bot] at hRmem
  exact hRne hRmem

omit [DecidableEq ι] in
/-- **止步格第一半：层 2 有见证**。`ker ≠ ⊥` ⇒ 存在非零元落在 `ker` 中。 -/
theorem stop_cell_layer2_witness (A B : Matrix ι ι ℂ)
    (hK : LinearMap.ker (adLin2 A B) ≠ ⊥) :
    ∃ R : Matrix ι ι ℂ, R ≠ 0 ∧ R ∈ LinearMap.ker (adLin2 A B) := by
  obtain ⟨R, hRmem, hRne⟩ := (Submodule.ne_bot_iff _).mp hK
  exact ⟨R, hRne, hRmem⟩

omit [DecidableEq ι] in
/-- **止步格第二半：层 3 无见证**。`ker ⊓ range = ⊥` ⇒ `¬ AdTraversable2`。 -/
theorem stop_cell_not_traversable2 (A B : Matrix ι ι ℂ)
    (hI : (LinearMap.ker (adLin2 A B) ⊓ LinearMap.range (adLin2 A B)) = ⊥) :
    ¬ AdTraversable2 A B := by
  intro h
  rw [AdTraversable2_iff_inf_ne_bot] at h
  exact h hI

omit [DecidableEq ι] in
/-- **可穿格：层 3 有见证**。`ker ⊓ range ≠ ⊥` ⇒ `AdTraversable2`。 -/
theorem traverse_cell_traversable2 (A B : Matrix ι ι ℂ)
    (hI : (LinearMap.ker (adLin2 A B) ⊓ LinearMap.range (adLin2 A B)) ≠ ⊥) :
    AdTraversable2 A B :=
  (AdTraversable2_iff_inf_ne_bot A B).mpr hI

omit [DecidableEq ι] in
/-- ★ **塔高由三相格决定**：三格各自给出塔高判据，打包为一条。

    * `ker = ⊥`（平坦）⇒ 无层 2 见证 ⇒ 塔高 1
    * `ker ≠ ⊥`（止步 / 可穿）⇒ 有层 2 见证 ⇒ 塔高 ≥ 2
    * `ker ⊓ range = ⊥`（平坦 / 止步）⇒ 层 3 无见证 ⇒ 塔高止于 2（或 1）
    * `ker ⊓ range ≠ ⊥`（可穿）⇒ 层 3 有见证 ⇒ 塔越过层 3 ⇒ 无界

    注意：第 1、2 条合起来已把「1」与「2」分开；第 3、4 条把「2」与「无界」分开。
    三格 ⇒ 三档，没有第四个可能。 -/
theorem tower_height_from_phase_cell (A B : Matrix ι ι ℂ) :
    (LinearMap.ker (adLin2 A B) = ⊥ →
      ¬ ∃ R : Matrix ι ι ℂ, R ≠ 0 ∧ R ∈ LinearMap.ker (adLin2 A B)) ∧
    (LinearMap.ker (adLin2 A B) ≠ ⊥ →
      ∃ R : Matrix ι ι ℂ, R ≠ 0 ∧ R ∈ LinearMap.ker (adLin2 A B)) ∧
    ((LinearMap.ker (adLin2 A B) ⊓ LinearMap.range (adLin2 A B)) = ⊥ →
      ¬ AdTraversable2 A B) ∧
    ((LinearMap.ker (adLin2 A B) ⊓ LinearMap.range (adLin2 A B)) ≠ ⊥ →
      AdTraversable2 A B) :=
  ⟨flat_cell_no_layer2_witness A B,
   stop_cell_layer2_witness A B,
   stop_cell_not_traversable2 A B,
   traverse_cell_traversable2 A B⟩

/-! ## 三、三相各自的塔高 -/

/-- **C 相塔高 1**：`(diag4, diag3)` 的跨对象 `ker = ⊥` ⇒ 无任何非零层 2 见证。

    这正是 `SpLayerSeparability.lean` L510–517 登记的缺口的填补：
    那里说「C 相塔高 1 不能由单对象判据表达」（`diag4_same_single_object_verdict`
    证明单对象判据对 C 相与 A 相给出相同判决），本批用**跨对象**口径把它表达出来。 -/
theorem phase_C_height_one :
    ¬ ∃ R : Matrix (Fin 3) (Fin 3) ℂ, R ≠ 0 ∧ R ∈ LinearMap.ker (adLin2 diag4 diag3) :=
  flat_cell_no_layer2_witness diag4 diag3 diag4_diag3_ker_eq_bot

/-- **A 相塔高 2**：`(diag3, diag3)` 层 2 有见证、层 3 无见证。

    注意「塔高 2」在第 29 批已知；本批把它拆成「层2 有 ∧ 层3 无」两条可机检命题，
    从而不再是数值断言。 -/
theorem phase_A_height_two :
    (∃ R : Matrix (Fin 3) (Fin 3) ℂ, R ≠ 0 ∧ R ∈ LinearMap.ker (adLin2 diag3 diag3)) ∧
    ¬ AdTraversable2 diag3 diag3 := by
  constructor
  · exact stop_cell_layer2_witness diag3 diag3 (by
      rw [adLin2_self]
      exact diag3_has_two_morphism)
  · exact stop_cell_not_traversable2 diag3 diag3
      (MUFPF.PhaseTrichotomy.phase_A_occupies_stop2).2

/-- **B 相塔高无界**：`(jordan3, jordan3)` 层 3 有见证 ⇒ `AdTraversable2`
    ⇒ 判据层号无关 ⇒ 每层都可非平凡（`tower_height_unbounded_B`）。

    **不是「塔高 = 4」**——`SpTowerUnbounded.tower_height_trichotomy` 已判「恰为 4」不成立。 -/
theorem phase_B_height_unbounded : AdTraversable2 jordan3 jordan3 :=
  traverse_cell_traversable2 jordan3 jordan3
    (MUFPF.PhaseTrichotomy.phase_B_occupies_traverse).2

/-- ★ **三相塔高 = 1 / 2 / 无界，与三格一一对应**。

    把 `phase_C_height_one`、`phase_A_height_two`、`phase_B_height_unbounded`
    打包，并声明其与既有 `tower_height_trichotomy` 的口径关系。 -/
theorem three_phases_heights :
    (¬ ∃ R : Matrix (Fin 3) (Fin 3) ℂ, R ≠ 0 ∧ R ∈ LinearMap.ker (adLin2 diag4 diag3)) ∧
    (∃ R : Matrix (Fin 3) (Fin 3) ℂ, R ≠ 0 ∧ R ∈ LinearMap.ker (adLin2 diag3 diag3)) ∧
    (¬ AdTraversable2 diag3 diag3) ∧
    AdTraversable2 jordan3 jordan3 :=
  ⟨phase_C_height_one, phase_A_height_two.1, phase_A_height_two.2,
   phase_B_height_unbounded⟩

/-! ## 四、与既有同对象口径的一致性 -/

/-- **两套口径不冲突**：同对象时跨对象判据退化为原判据
    （`AdTraversable2 A A ↔ AdTraversable A`，`SpLayerSeparability.lean` L347）。

    故本批把层 2 判据提升为跨对象后，对同对象情形（A/B 相）仍与
    `HasNontrivialTwoMorphism` / `AdTraversable` 完全一致；差异只出现在跨对象（C 相）。 -/
theorem object_vs_cross_agreement :
    (AdTraversable2 jordan3 jordan3 ↔ AdTraversable jordan3) ∧
    (AdTraversable2 diag3 diag3 ↔ AdTraversable diag3) :=
  ⟨AdTraversable2_self_iff jordan3, AdTraversable2_self_iff diag3⟩

end MUFPF.TowerFromPhase
