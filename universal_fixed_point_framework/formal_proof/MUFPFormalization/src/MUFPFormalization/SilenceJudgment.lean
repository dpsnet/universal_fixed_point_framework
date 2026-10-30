import Mathlib.Tactic
import MUFPFormalization.EccentricPeriodicOrbit
import MUFPFormalization.SilenceModel

/-!
# 静默判据框架类：静默 ⟺ 独立不动点（RecObj 级公设）

用户裁决（2026-10-24）：静默 = 闭合冻结（独立不动点，结构保留）+ 作为可观测量
零测度，非"丢弃"。公设形态 = "独立不动点（闭合冻结）⟺ 静默（零测度）"。
SilenceModel.lean 已给分层模型实例（`independentFixed_iff_mem`，可证定理）。

本文件把公设提升为 RecObj 级框架判据（class）：
- `SilenceJudgment X`：静默窗集合（`silentSet : Finset X.T`，零测度窗口判据）；
- `inActiveOrbit X x`：x 属于某条活跃循环（周期轨道且含非静默元素）；
- `independentFixed X x`：不动 ∧ 非活跃循环成员 = 闭合冻结；
- `IndependentFixedIffSilent X`：公设字段（静默⟹不动 + 独立不动点⟺静默窗）；
- ★ `full_independentFixed_iff_full_silent`：全独立不动点 ⟺ 全静默
  （"恒等 ⟹ 全静默"双向链 RecObj 级闭环）；
- 模型实例：`silenceRec15_layered S`（SilenceModel 定理逐字段验证，非恒假）。

诚实边界：class 字段 = 框架语义公设（非全局 axiom 声明，实例必须满足）；
14（层 4 单点窗）天然不动但不静默的边界由 `inActiveOrbit` 精确排除
（14 ∉ S 时属活跃循环成员，非独立不动点）。

零 sorry 政策：本文件不含 sorry。
-/

namespace MUFPF

open MUFPF.EccentricOrbit

/-- 静默窗集合：RecObj 上静默（表达零测度）窗口的 Finset 判据。
    语义 = 闭合冻结 + 零测度（2026-10-24 用户裁决，非丢弃）。 -/
class SilenceJudgment (X : RecObj) where
  silentSet : Finset X.T

/-- 活跃循环成员：x 从某非静默周期点迭代可达（= x 在含非静默元素的周期轨道上）。 -/
def inActiveOrbit (X : RecObj) [J : SilenceJudgment X] (x : X.T) : Prop :=
  ∃ y : X.T, periodicPoint X y ∧ y ∉ J.silentSet ∧ ∃ n : ℕ, X.step^[n] y = x

/-- 独立不动点（闭合冻结）：不动 ∧ 非活跃循环成员。 -/
def independentFixed (X : RecObj) [J : SilenceJudgment X] (x : X.T) : Prop :=
  X.step x = x ∧ ¬ inActiveOrbit X x

/-- 静默判据公设：静默 ⟹ 不动；独立不动点（闭合冻结）⟺ 静默（零测度）。 -/
class IndependentFixedIffSilent (X : RecObj) [J : SilenceJudgment X] where
  silent_fixed : ∀ x : X.T, x ∈ J.silentSet → X.step x = x
  independentFixed_iff : ∀ x : X.T, independentFixed X x ↔ x ∈ J.silentSet

/-- 静默窗成员 = 不动点（RecObj 级，公设字段导出）。 -/
theorem silent_fixed_of_mem (X : RecObj) [J : SilenceJudgment X]
    [I : IndependentFixedIffSilent X] {x : X.T} (hx : x ∈ J.silentSet) :
    X.step x = x :=
  I.silent_fixed x hx

/-- 全静默 ⟹ 全不动（公设 1 全量化版）。 -/
theorem all_silent_all_fixed (X : RecObj) [J : SilenceJudgment X]
    [I : IndependentFixedIffSilent X] (hS : J.silentSet = Finset.univ) :
    ∀ x : X.T, X.step x = x := by
  intro x
  exact I.silent_fixed x (by simp [hS])

/-- ★ "恒等 ⟹ 全静默" RecObj 级闭环：全独立不动点（闭合冻结）⟺ 全静默（零测度）。 -/
theorem full_independentFixed_iff_full_silent (X : RecObj) [J : SilenceJudgment X]
    [I : IndependentFixedIffSilent X] :
    (∀ x : X.T, independentFixed X x) ↔ J.silentSet = Finset.univ := by
  constructor
  · intro h
    ext x
    constructor
    · intro hxS
      exact Finset.mem_univ x
    · intro _
      exact (I.independentFixed_iff x).mp (h x)
  · intro hS x
    exact (I.independentFixed_iff x).mpr (by simp [hS])

/-! ## 分层模型实例：silenceRec15_layered S

SilenceModel.lean 的 `silenceRec15_layered S`（15 组合窗口分层静默模型）满足
`SilenceJudgment` 与 `IndependentFixedIffSilent`：
- `silentSet := S`（静默窗集合）；
- 静默 ⟹ 不动：`silentStep_mem`（既有）；
- 独立不动点 ⟺ 静默窗：桥 = 完全活跃层 ↔ `inActiveOrbit`
  （层内循环保持层成员；非静默周期点必在完全活跃层；层内迭代可达 ⟹ 同层）。 -/

open MUFPF.PeriodicOrbitCount

/-- 模型实例：静默窗集合 = S。 -/
instance silenceModelJudgment (S : Finset (Fin 15)) : SilenceJudgment (silenceRec15_layered S) where
  silentSet := S

/-- 层内后继保持层成员：layeredStep 不离开所在层。 -/
lemma layeredStep_mem_layer {L : Finset (Fin 15)} (hLmem : L ∈ layers) {z : Fin 15}
    (hz : z ∈ L) : layeredStep z ∈ L := by
  simp [layers] at hLmem
  rcases hLmem with rfl | rfl | rfl | rfl
  · simp [layer1] at hz
    rcases hz with rfl | rfl | rfl | rfl
    all_goals native_decide
  · simp [layer2] at hz
    rcases hz with rfl | rfl | rfl | rfl | rfl | rfl
    all_goals native_decide
  · simp [layer3] at hz
    rcases hz with rfl | rfl | rfl | rfl
    all_goals native_decide
  · simp [layer4] at hz
    rcases hz with rfl
    all_goals native_decide

/-- 完全活跃层上 silentStep = layeredStep（层成员全部非静默），保持层成员。 -/
lemma silentStep_mem_layer {L : Finset (Fin 15)} (hLmem : L ∈ layers)
    {S : Finset (Fin 15)} (hLem : L ∩ S = ∅) {z : Fin 15} (hz : z ∈ L) :
    silentStep S z ∈ L := by
  have hzS : z ∉ S := by
    intro hzS
    have hzInter : z ∈ L ∩ S := Finset.mem_inter.mpr ⟨hz, hzS⟩
    simp [hLem] at hzInter
  rw [silentStep_not_mem S hzS]
  exact layeredStep_mem_layer hLmem hz

/-- 完全活跃层上 silentStep 迭代保持层成员。 -/
lemma silentStep_iterate_mem_layer (n : ℕ) {L : Finset (Fin 15)} (hLmem : L ∈ layers)
    {S : Finset (Fin 15)} (hLem : L ∩ S = ∅) {z : Fin 15} (hz : z ∈ L) :
    (silentStep S)^[n] z ∈ L := by
  induction n generalizing z with
  | zero => exact hz
  | succ n ih =>
      rw [Function.iterate_succ_apply]
      exact ih (silentStep_mem_layer hLmem hLem hz)

/-- RecObj.step 迭代 = silentStep 迭代（投影桥迭代版，函数外延替换）。 -/
lemma iterate_step_eq_iterate_silentStep (n : ℕ) (S : Finset (Fin 15)) (y : Fin 15) :
    (silenceRec15_layered S).step^[n] y = (silentStep S)^[n] y := by
  have hstep : (silenceRec15_layered S).step = silentStep S := by
    funext z
    exact silenceRec15_layered_step S z
  rw [hstep]
  rfl

/-- 完全活跃层成员 ⟹ 活跃循环成员（y = x 自身，周期点 + 非静默 + 迭代 0 步可达）。 -/
lemma inActiveOrbit_of_activeLayer (S : Finset (Fin 15)) {L : Finset (Fin 15)}
    (hLmem : L ∈ layers) {x : Fin 15} (hxL : x ∈ L) (hLem : L ∩ S = ∅) :
    inActiveOrbit (silenceRec15_layered S) x := by
  change ∃ y : Fin 15, periodicPoint (silenceRec15_layered S) y ∧ y ∉ S ∧
    ∃ n : ℕ, (silenceRec15_layered S).step^[n] y = x
  refine ⟨x, ?_, ?_, ⟨0, rfl⟩⟩
  · exact (periodicPoint_iff S x).mpr (Or.inr ⟨L, hLmem, hxL, hLem⟩)
  · intro hxS
    have hxInter : x ∈ L ∩ S := Finset.mem_inter.mpr ⟨hxL, hxS⟩
    simp [hLem] at hxInter

/-- 活跃循环成员 ⟹ 所在完全活跃层（非静默周期点轨道上全部元素同层）。 -/
lemma inActiveOrbit_implies_activeLayer (S : Finset (Fin 15)) {x : Fin 15}
    (hin : inActiveOrbit (silenceRec15_layered S) x) :
    ∃ L ∈ layers, x ∈ L ∧ L ∩ S = ∅ := by
  change ∃ y : Fin 15, periodicPoint (silenceRec15_layered S) y ∧ y ∉ S ∧
    ∃ n : ℕ, (silenceRec15_layered S).step^[n] y = x at hin
  rcases hin with ⟨y, hyper, hyS, n, hynx⟩
  rcases (periodicPoint_iff S y).mp hyper with hyS' | hL
  · exact False.elim (hyS hyS')
  · rcases hL with ⟨L, hLmem, hyL, hLem⟩
    have hynx' : (silentStep S)^[n] y = x := by
      rw [← iterate_step_eq_iterate_silentStep n S y]
      exact hynx
    have hmem : (silentStep S)^[n] y ∈ L := silentStep_iterate_mem_layer n hLmem hLem hyL
    have hxL : x ∈ L := by
      rwa [hynx'] at hmem
    exact ⟨L, hLmem, hxL, hLem⟩

/-- 模型实例：分层静默模型满足静默判据公设（逐字段验证，零 axiom）。 -/
instance silenceModelProps (S : Finset (Fin 15)) : IndependentFixedIffSilent (silenceRec15_layered S) where
  silent_fixed := by
    change ∀ x : Fin 15, x ∈ S → (silenceRec15_layered S).step x = x
    intro x hx
    rw [silenceRec15_layered_step]
    exact silentStep_mem S hx
  independentFixed_iff := by
    change ∀ x : Fin 15, independentFixed (silenceRec15_layered S) x ↔ x ∈ S
    intro x
    constructor
    · intro hx
      rcases hx with ⟨hfix, hnot⟩
      have hfixS : silentStep S x = x := by
        rw [← silenceRec15_layered_step]
        exact hfix
      rcases (fixed_iff_mem_or_14 S x).mp hfixS with hxS | hx14
      · exact hxS
      · by_contra hxS
        subst hx14
        have hLem : layer4 ∩ S = ∅ := by
          ext m
          simp [layer4]
          intro hm14 hmS
          exact hxS (by simpa [hm14] using hmS)
        exact False.elim (hnot (inActiveOrbit_of_activeLayer S (by simp [layers])
          (by simp [layer4] : (14 : Fin 15) ∈ layer4) hLem))
    · intro hxS
      constructor
      · rw [silenceRec15_layered_step]
        exact silentStep_mem S hxS
      · intro hin
        rcases (inActiveOrbit_implies_activeLayer S hin) with ⟨L, hLmem, hxL, hLem⟩
        have hxInter : x ∈ L ∩ S := Finset.mem_inter.mpr ⟨hxL, hxS⟩
        simp [hLem] at hxInter

/-- 模型验证："恒等 ⟹ 全静默"在分层模型上的 RecObj 级闭环实例
    （全独立不动点 ⟺ S=univ；14 为活跃循环成员被排除，与 2⁴−1=15 解集一致）。 -/
example (S : Finset (Fin 15)) :
    (∀ x : Fin 15, independentFixed (silenceRec15_layered S) x) ↔ S = Finset.univ := by
  change (∀ x : (silenceRec15_layered S).T, independentFixed (silenceRec15_layered S) x) ↔
    (silenceModelJudgment S).silentSet = Finset.univ
  exact full_independentFixed_iff_full_silent (silenceRec15_layered S)

/-- ★ g=15 合拢定理：简并度 15 的解集 = 全独立不动点（全静默闭合冻结极限）∨ 模型边界
    例外（S = univ.erase 14：层 4 单点窗 14 为活跃循环成员、完成态结构保留、非独立
    不动点）——把映射层解集（orbitCount_eq_15_iff）与静默语义层（full_...）合拢，
    "冻结≠静默"的最后实例在简并度公式中显式呈现。 -/
theorem orbitCount_eq_15_char_silence (S : Finset (Fin 15)) :
    orbitCount (silenceRec15_layered S) = 15 ↔
      (∀ x : Fin 15, independentFixed (silenceRec15_layered S) x) ∨ S = Finset.univ.erase 14 := by
  rw [orbitCount_eq_15_iff S]
  constructor
  · intro h
    rcases h with hS | hS14
    · left
      change ∀ x : (silenceRec15_layered S).T, independentFixed (silenceRec15_layered S) x
      exact (full_independentFixed_iff_full_silent (silenceRec15_layered S)).mpr hS
    · right
      exact hS14
  · intro h
    rcases h with hfix | hS14
    · left
      change (silenceModelJudgment S).silentSet = Finset.univ
      exact (full_independentFixed_iff_full_silent (silenceRec15_layered S)).mp hfix
    · right
      exact hS14

end MUFPF
