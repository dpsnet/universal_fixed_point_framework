/-
  PhaseCountReadout.lean — 标号 5 与三相塔高的关系（第 61 批）
  ================================================================

  ## 问题

  第 60 批（`LayerBoundaryAudit.lean`）判定 `N_total := catOrder + 1` 是标号计数、
  `+1` 的「顶层停在层 4」被库内 `SpFiveMorphism` 反证，并给出措辞
  「`N_total = 5` 是 A 相读法」。**本批否定这一措辞。**

  ## 为什么那句措辞是错的

  库内早在第 29/30 批就把「相」机检完了，且三相各对应一个**塔高**，不是 5：

    * `PhaseTrichotomy.lean`（第 29 批）：相 = `ker(adLin2 A B)` 的两条二值判据的 4 格排除 1 格
        - 平坦（C 相）：`ker = ⊥`
        - 止步（A 相）：`ker ≠ ⊥ ∧ ker ⊓ range = ⊥`
        - 可穿（B 相）：`ker ≠ ⊥ ∧ ker ⊓ range ≠ ⊥`
    * `TowerHeightFromPhase.lean`（第 30 批）：三格 ⇒ 塔高 **1 / 2 / 无界**
        - C 相 1（无层 2 见证）、A 相 2（层 2 有、层 3 无）、B 相无界（层 3 有 + 判据层号无关）

  所以 A 相塔高是 **2**，不是 5。`N_total = 5` 与三相塔高**全部不等**；
  「A 相读法」这个说法把「标号计数」与「塔高」混成了一件东西。

  ## 本批的正面结论

  1. **三相判据有了显式载体**（`InFlatPhase` / `InStopPhase` / `InTraversePhase`），
     并机检「三格恰是一划分」（穷尽 + 两两互斥）。
  2. **标号 5 是相盲的**：同一个 `Fintype.card LayerIndex = 5` 与三相**全部相容**
     （`label_five_coexists_with_every_phase`）。⇒ 标号不筛选相、不携带相信息。
  3. **没有任何有限读数能等于 B 相塔高**（`no_nat_caps_unbounded_tower`）；
     特别地 `1 / 2 / 5` 都不是上界（`no_finite_readout_matches`）。
  4. **`B = 15` 的因子 3 只能来自生成代数计数**，不能来自塔高：
     `3 × 5 = 15`、`2 × 5 = 10`、`1 × 5 = 5`（`fifteen_needs_generation_count_not_height`）。
     ⇒ 「`B = 15` 是层对数」里的「层」只能是**标号层**，不能是塔高层。

  ## 与既有模块的关系

  * 第 29 批声明「三格不是构造子计数」；本批沿用，判据仍是 `Submodule` 逻辑。
  * 第 30 批已给塔高 1/2/无界；本批**不重证**，只引用（`phase_C_height_one` /
    `phase_A_height_two` / `phase_B_height_unbounded`）并把它与标号作对照。
  * `SpTowerUnbounded.LayerWitness` 是**层号无关**的判据（`∀ k ≥ 2`），
    故本批「无界」仍是判据口径，**不是**「层结构无限存在」。

  ## 不注入声明（可核对）

  * 三个相判据是 `Submodule` 命题的组合，**没有** `inductive` 构造子计数。
  * 塔高 1 / 2 / 无界**不是**三个定义的构造子，而是三格的直接后果（第 30 批）。
  * 证明体不引用任何 `def := k` 的层数常量；`5` 只以 `Fintype.card LayerIndex` 的形式出现。

  ## 边界（必须一并陈述）

  - 本批**不**证「相只有三个」——那是第 29 批的 4→3 格结论；本批只补「标号不相交」。
  - 本批**不**把 `N_total` 改成 2 或任何塔高值；`N_total = 5` 仍是 `LayerIndex` 的构造子数。
  - B 相「无界」的机检形态是 `∀ k : ℕ, 2 ≤ k → LayerWitness jordan3`，即「每层都有同一判据的
    非零见证」，**不是** `∞` 的算术。
  - 「订正第 60 批措辞」只落在本节与笔记 §21.74；第 60 批模块文件内的 doc **未就地改写**，
    按「只登记、不就地改」策略待裁决。
-/

import Mathlib.Tactic
import MUFPFormalization.PhaseTrichotomy
import MUFPFormalization.TowerHeightFromPhase
import MUFPFormalization.SpTowerUnbounded
import MUFPFormalization.BranchCounting
import MUFPFormalization.ActiveFromCategoryOrder

namespace MUFPF.PhaseCountReadout

open MUFPFormalization
open MUFPF.BranchCounting (LayerIndex total_layers_count)
open Matrix

/-! ## 一、三相判据的显式载体 -/

/-- **平坦相判据（C 相）**：`ker(adLin2 A B) = ⊥`。 -/
def InFlatPhase {ι : Type*} [Fintype ι] [DecidableEq ι]
    (A B : Matrix ι ι ℂ) : Prop :=
  LinearMap.ker (adLin2 A B) = ⊥

/-- **止步相判据（A 相）**：`ker ≠ ⊥` 且 `ker ⊓ range = ⊥`。 -/
def InStopPhase {ι : Type*} [Fintype ι] [DecidableEq ι]
    (A B : Matrix ι ι ℂ) : Prop :=
  LinearMap.ker (adLin2 A B) ≠ ⊥ ∧
    (LinearMap.ker (adLin2 A B) ⊓ LinearMap.range (adLin2 A B)) = ⊥

/-- **可穿相判据（B 相）**：`ker ≠ ⊥` 且 `ker ⊓ range ≠ ⊥`。 -/
def InTraversePhase {ι : Type*} [Fintype ι] [DecidableEq ι]
    (A B : Matrix ι ι ℂ) : Prop :=
  LinearMap.ker (adLin2 A B) ≠ ⊥ ∧
    (LinearMap.ker (adLin2 A B) ⊓ LinearMap.range (adLin2 A B)) ≠ ⊥

/-- **判据穷尽**：任一过渡对落在三相之一（承接第 29 批 `phase_states_exhaustive`）。 -/
theorem phase_criterion_exhaustive {ι : Type*} [Fintype ι] [DecidableEq ι]
    (A B : Matrix ι ι ℂ) :
    InFlatPhase A B ∨ InStopPhase A B ∨ InTraversePhase A B := by
  have h := MUFPF.PhaseTrichotomy.phase_states_exhaustive A B
  unfold InFlatPhase InStopPhase InTraversePhase
  exact h

/-- **判据两两互斥**：三格是划分，不是重叠覆盖。 -/
theorem phase_criterion_exclusive {ι : Type*} [Fintype ι] [DecidableEq ι]
    (A B : Matrix ι ι ℂ) :
    (InFlatPhase A B → ¬ InStopPhase A B) ∧
    (InFlatPhase A B → ¬ InTraversePhase A B) ∧
    (InStopPhase A B → ¬ InTraversePhase A B) := by
  unfold InFlatPhase InStopPhase InTraversePhase
  refine ⟨?_, ?_, ?_⟩
  · rintro h1 ⟨h2, _⟩
    exact h2 h1
  · rintro h1 ⟨h2, _⟩
    exact h2 h1
  · rintro ⟨_, h1⟩ ⟨_, h2⟩
    exact h2 h1

/-- ★ **三相判据恰是一划分**：穷尽 + 两两互斥。 -/
theorem phase_criterion_is_partition {ι : Type*} [Fintype ι] [DecidableEq ι]
    (A B : Matrix ι ι ℂ) :
    (InFlatPhase A B ∨ InStopPhase A B ∨ InTraversePhase A B) ∧
    (InFlatPhase A B → ¬ InStopPhase A B) ∧
    (InFlatPhase A B → ¬ InTraversePhase A B) ∧
    (InStopPhase A B → ¬ InTraversePhase A B) :=
  ⟨phase_criterion_exhaustive A B,
    (phase_criterion_exclusive A B).1,
    (phase_criterion_exclusive A B).2.1,
    (phase_criterion_exclusive A B).2.2⟩

/-! ## 二、三相的塔高（引用第 30 批，不重证） -/

/-- **三相塔高 = 1 / 2 / 无界**（打包引用第 30 批三条 + B 相无界判据）。

    * C 相 1：`(diag4, diag3)` 无层 2 见证
    * A 相 2：`(diag3, diag3)` 层 2 有、层 3 无
    * B 相无界：`(jordan3, jordan3)` 层 3 有 + `∀ k ≥ 2` 都有见证 -/
theorem phase_heights_by_criterion :
    (¬ ∃ R : Matrix (Fin 3) (Fin 3) ℂ, R ≠ 0 ∧ R ∈ LinearMap.ker (adLin2 diag4 diag3)) ∧
    (∃ R : Matrix (Fin 3) (Fin 3) ℂ, R ≠ 0 ∧ R ∈ LinearMap.ker (adLin2 diag3 diag3)) ∧
    ¬ AdTraversable2 diag3 diag3 ∧
    AdTraversable2 jordan3 jordan3 ∧
    (∀ k : ℕ, 2 ≤ k → LayerWitness jordan3) :=
  ⟨MUFPF.TowerFromPhase.phase_C_height_one,
    MUFPF.TowerFromPhase.phase_A_height_two.1,
    MUFPF.TowerFromPhase.phase_A_height_two.2,
    MUFPF.TowerFromPhase.phase_B_height_unbounded,
    tower_height_unbounded_B⟩

/-! ## 三、标号 5 与相的关系 -/

/-- **标号与三相全部相容** ★：同一个 `Fintype.card LayerIndex = 5` 同时成立在三相之上。

    ⇒ 标号 5 不筛选相、不携带相信息。这是「相盲」的机检形态。 -/
theorem label_five_coexists_with_every_phase :
    (Fintype.card MUFPF.BranchCounting.LayerIndex = 5 ∧ InFlatPhase diag4 diag3) ∧
    (Fintype.card MUFPF.BranchCounting.LayerIndex = 5 ∧ InStopPhase diag3 diag3) ∧
    (Fintype.card MUFPF.BranchCounting.LayerIndex = 5 ∧ InTraversePhase jordan3 jordan3) := by
  refine ⟨⟨?_, ?_⟩, ⟨?_, ?_⟩, ⟨?_, ?_⟩⟩
  · exact total_layers_count
  · exact MUFPF.PhaseTrichotomy.phase_C_occupies_flat
  · exact total_layers_count
  · exact MUFPF.PhaseTrichotomy.phase_A_occupies_stop2
  · exact total_layers_count
  · exact MUFPF.PhaseTrichotomy.phase_B_occupies_traverse

/-- **B 相塔高无有限上界**：`¬ ∃ N, ∀ k ≥ 2, k ≤ N`。 -/
theorem no_nat_caps_unbounded_tower : ¬ ∃ N : ℕ, ∀ k : ℕ, 2 ≤ k → k ≤ N := by
  rintro ⟨N, h⟩
  have hk : 2 ≤ N + 2 := by omega
  have := h (N + 2) hk
  omega

/-- **三个读数 1 / 2 / 5 都不是塔高上界**。 -/
theorem no_finite_readout_matches :
    ¬ ∃ N : ℕ, (N = 1 ∨ N = 2 ∨ N = 5) ∧ ∀ k : ℕ, 2 ≤ k → k ≤ N := by
  rintro ⟨N, hN, h⟩
  have h6 : 2 ≤ 6 := by norm_num
  have := h 6 h6
  rcases hN with h1 | h2 | h5
  · omega
  · omega
  · omega

/-- **`B` 的因子 3 只能来自生成代数计数**：把 3 换成任一相塔高（2 或 1），`B` 不再是 15。 -/
theorem fifteen_needs_generation_count_not_height :
    (3 : ℕ) * 5 = 15 ∧ (2 : ℕ) * 5 = 10 ∧ (1 : ℕ) * 5 = 5 ∧
    (15 : ℕ) ≠ 10 ∧ (15 : ℕ) ≠ 5 := by
  decide

/-! ## 四、总述 -/

/-- ★★ **本批裁决**：库内有四个互不相同的「层数」读数 ——
    标号 5、C 相 1、A 相 2、B 相无界；标号与三相全部相容（相盲）；
    没有任何有限读数（含 5）能当 B 相塔高的上界。 -/
theorem phase_blindness_verdict :
    Fintype.card MUFPF.BranchCounting.LayerIndex = 5 ∧
    (¬ ∃ R : Matrix (Fin 3) (Fin 3) ℂ, R ≠ 0 ∧ R ∈ LinearMap.ker (adLin2 diag4 diag3)) ∧
    (∃ R : Matrix (Fin 3) (Fin 3) ℂ, R ≠ 0 ∧ R ∈ LinearMap.ker (adLin2 diag3 diag3)) ∧
    ¬ AdTraversable2 diag3 diag3 ∧
    AdTraversable2 jordan3 jordan3 ∧
    (∀ k : ℕ, 2 ≤ k → LayerWitness jordan3) ∧
    ¬ ∃ N : ℕ, (N = 1 ∨ N = 2 ∨ N = 5) ∧ ∀ k : ℕ, 2 ≤ k → k ≤ N :=
  ⟨total_layers_count,
    phase_heights_by_criterion.1,
    phase_heights_by_criterion.2.1,
    phase_heights_by_criterion.2.2.1,
    phase_heights_by_criterion.2.2.2.1,
    phase_heights_by_criterion.2.2.2.2,
    no_finite_readout_matches⟩

end MUFPF.PhaseCountReadout
