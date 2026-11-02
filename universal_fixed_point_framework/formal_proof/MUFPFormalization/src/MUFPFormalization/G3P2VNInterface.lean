import Mathlib.Algebra.Algebra.Equiv
import Mathlib.Algebra.Algebra.Prod
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Mul
import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.NormNum

import MUFPFormalization.G3P2CarrierType

/-!
# G3-P2-8：载体类型接口骨架（vN / KMS 侧，只定义、不宣称证明，2026-11-03）

对应 roadmap P7-5e-373。P2-7（372）已把「载体类型判据」的**有限型 I 半边**机检完毕；
本模块搭起通向 vN / III 型的**接口**，刻意只做四件事：

1. `ModularDatum`：载体-流数据（代数 + 流），**不**内含 KMS 条件、**不**对流的解析性作假设；
2. `UnitRealizable`：流可由代数单位路径实现——即 Tomita 事实 `Δ_mod^{it} ∈ A^×` 的代数替身；
3. `TypeIII`：**操作性定义** `¬ UnitRealizable`（不是经典因子类型分类，二者关系未证）；
4. `UnitRealizableDatum`：把「有限型 I ⟹ 单位可实现」写成**显式字段**（模型输入），
   而不是从 KMS 推出的定理；并证明该数据必内、不外、非 III。

## 记号纪律（沿用 367–372）

- 框架原生 `Δ`（`spExchangeLaw` 交换律偏差）**不出现、不赋值**；`Δ_mod ≠ 1` 不作假设；
- `M`（模哈密顿量）不作标量；本模块不构造 `ρ^{it}` 复相位、不构造解析延拓；
- 本模块**没有任何 `axiom`、没有 `sorry`、没有 `Classical.choice` 之外的公设**；
  `TypeIII` 是操作性定义，不是对 III 型因子的存在性断言。

## 诚实边界（接口骨架的全部缺口）

- `TypeIII` 只定义为「模流不可由代数单位路径实现」，与 Takesaki 的因子类型分类
  （I / II / III）之间的等价**未证明**；
- 「III 型因子存在外模流」**未形式化**，本模块只用块交换给出一个操作性 III 实例
  （`swapDatum`），它不是任何忠实态的模流（372 已证）；
- Tomita `Δ_mod^{it} ∈ A^×` 在 `UnitRealizableDatum` 中是**字段假设**，不是定理；
- 载体（RecObj 的忠实正规态空间/模算子/状态空间）仍未定义、vN 完成性未证
  ⇒ **P2 未成立、G3 未闭合**；不关闭任何项（226 挂起、k(2) 开放）。
-/

namespace MUFPF.G3P2VNInterface

open MUFPF.RecursionModularityOuter
open MUFPF.G3CarrierNecessity
open MUFPF.G3StateNecessity
open MUFPF.G3P2AxisOrthogonality
open MUFPF.G3P2CarrierType

variable {R A : Type*} [CommSemiring R] [Ring A] [Algebra R A]

/-- 载体-流数据：只含代数与流，不含 KMS 条件（接口，不作为公设）。 -/
structure ModularDatum where
  flow : ℝ → A ≃ₐ[R] A

/-- 流可由代数单位路径实现（`Δ_mod^{it} ∈ A^×` 的代数替身）。 -/
def UnitRealizable (σ : ℝ → A ≃ₐ[R] A) : Prop :=
  ∃ u : ℝ → Aˣ, ∀ t : ℝ, σ t = innerAutEquiv (R := R) (A := A) (u t)

/-- 操作性类型谓词：模流不可由代数单位路径实现（**不是**经典因子类型分类）。 -/
def TypeIII (D : ModularDatum (R := R) (A := A)) : Prop :=
  ¬ UnitRealizable D.flow

/-- 「有限型 I ⟹ 单位可实现」被显式化为数据字段（模型输入，不是 KMS 定理）。 -/
structure UnitRealizableDatum extends ModularDatum (R := R) (A := A) where
  unitPath : ℝ → Aˣ
  realizes : ∀ t : ℝ, flow t = innerAutEquiv (R := R) (A := A) (unitPath t)

/-- 单位可实现数据必内。 -/
theorem unitRealizableDatum_inner (D : UnitRealizableDatum (R := R) (A := A)) :
    InnerFlow D.flow :=
  fun t => by
    rw [D.realizes t]
    exact innerAutEquiv_inner (R := R) (A := A) (D.unitPath t)

/-- 单位可实现数据不可能是外流。 -/
theorem unitRealizableDatum_not_outer (D : UnitRealizableDatum (R := R) (A := A)) :
    ¬ OuterFlow D.flow := by
  intro h
  exact h 0 (unitRealizableDatum_inner D 0)

/-- 单位可实现数据不是操作性 III（即 III 与单位可实现互斥）。 -/
theorem unitRealizableDatum_not_typeIII (D : UnitRealizableDatum (R := R) (A := A)) :
    ¬ TypeIII D.toModularDatum := by
  intro h
  exact h ⟨D.unitPath, D.realizes⟩

/-- ★ 桥接：P2-4 的 `InnerFlow`（逐时刻内实现）与载体侧的 `UnitRealizable`
    （存在单位路径）等价。逐时刻存在用选择公理拼成路径。 -/
theorem innerFlow_iff_unitRealizable (σ : ℝ → A ≃ₐ[R] A) :
    InnerFlow σ ↔ UnitRealizable σ := by
  constructor
  · intro h
    refine ⟨fun t => Classical.choose (h t), fun t => ?_⟩
    exact AlgEquiv.ext (fun a => Classical.choose_spec (h t) a)
  · rintro ⟨u, hu⟩
    intro t
    rw [hu t]
    exact innerAutEquiv_inner (R := R) (A := A) (u t)

/-- ★ 桥接：非内流 ⟺ 存在某个时刻是外自同构（经典否定搬运）。 -/
theorem not_innerFlow_iff_exists_outer (σ : ℝ → A ≃ₐ[R] A) :
    ¬ InnerFlow σ ↔ ∃ t : ℝ, IsOuterAut (σ t) := by
  simp only [InnerFlow, IsOuterAut, not_forall]

/-! ### 有限型 I 实例：把模型输入显式化 -/

/-- 块对角忠实态的单位路径（常数）。 -/
def stateUnitPath (s₁ s₂ : DiagState) : ℝ → TwoBlockAlgˣ :=
  fun _ => prodUnit s₁.unit s₂.unit

/-- 有限型 I 的单位可实现数据。 -/
def stateDatum (s₁ s₂ : DiagState) : UnitRealizableDatum (R := ℚ) (A := TwoBlockAlg) where
  flow := stateFlow s₁ s₂
  unitPath := stateUnitPath s₁ s₂
  realizes := fun _ => rfl

/-- 块交换的常数流数据（操作性 III 实例，不是忠实态模流）。 -/
def swapDatum : ModularDatum (R := ℚ) (A := TwoBlockAlg) where
  flow := fun _ => swapBlockAlgEquiv

/-- 块交换常数流在操作性定义下是 III（不可由单位路径实现）。 -/
theorem swapDatum_typeIII : TypeIII swapDatum := by
  rintro ⟨u, hu⟩
  have hout : IsOuterAut swapBlockAlgEquiv := swapBlock_outer
  have hσ : swapBlockAlgEquiv = innerAutEquiv (R := ℚ) (A := TwoBlockAlg) (u 0) := hu 0
  rw [hσ] at hout
  exact hout (innerAutEquiv_inner (R := ℚ) (A := TwoBlockAlg) (u 0))

/-! ### 接口主定理 -/

/-- ★★★ P2-8 接口主定理（只有定义与桥接，不含未证存在性）：
    - 单位可实现数据 ⇒ 内流、非外流、非操作性 III；
    - 有限型 I 的任一忠实对角态都是单位可实现数据；
    - 非平凡时间存在（2/3,1/3）；
    - 操作性 III 实例存在（块交换常数流），且它不是任何忠实态流（372 已证）。 -/
theorem carrierType_interface :
    (∀ D : UnitRealizableDatum (R := ℚ) (A := TwoBlockAlg),
        InnerFlow D.flow ∧ ¬ OuterFlow D.flow ∧ ¬ TypeIII D.toModularDatum) ∧
    (∀ s₁ s₂ : DiagState, ¬ TypeIII (stateDatum s₁ s₂).toModularDatum) ∧
    (∃ s₁ s₂ : DiagState, (stateDatum s₁ s₂).flow 0 ≠ AlgEquiv.refl) ∧
    (TypeIII swapDatum ∧ IsOuterAut swapBlockAlgEquiv) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro D
    exact ⟨unitRealizableDatum_inner D, unitRealizableDatum_not_outer D,
      unitRealizableDatum_not_typeIII D⟩
  · intro s₁ s₂
    exact unitRealizableDatum_not_typeIII (stateDatum s₁ s₂)
  · refine ⟨⟨2/3, 1/3, by norm_num, by norm_num⟩,
      ⟨1/2, 1/2, by norm_num, by norm_num⟩, ?_⟩
    exact blockStateAut_nontrivial _ _ (by norm_num)
  · exact ⟨swapDatum_typeIII, swapBlock_outer⟩

end MUFPF.G3P2VNInterface
