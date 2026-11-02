import Mathlib.Algebra.Algebra.Equiv
import Mathlib.Algebra.Algebra.Prod
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Mul
import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.NormNum

import MUFPFormalization.G3P2AxisOrthogonality

/-!
# G3-P2-7：载体类型判据——有限型 I 的模流必内，外流不可由忠实态生成（2026-11-03）

对应 `notes/04_lorentz_gravity/递归模同构_立项_时间模流生成链.md` §3（P2）与
roadmap P7-5e-372。P2-4（369）给载体侧必要条件，P2-5（370）给态侧必要条件，
P2-6（371）证明内/外轴对 P2 无判别力。371 的结语指出：P2 判据只能落在
**载体类型**（模算子/态的谱结构）。本模块给出该判据在有限块模型中的可机检部分：

1. **单位路径流必内**（`unitFlow_inner`）：有限维中模实现由代数内部单位给出，
   故任意单位路径流都是内流；
2. **外 ⟹ 无单位实现**（`outer_not_unitFlow`）：若自同构是外，则它不可能等于任何
   单位共轭 `Ad u`——即模算子 `Δ_mod^{it}` 不在代数单位群内（Tomita 的代数替身读法）；
3. **有限型 I 的忠实态流全内**（`finiteTypeI_stateFlow_inner` / `..._not_outer`）：
   对角忠实态的模实现被编码为单位共轭，故其流必内、不可能是外流；
4. **时间的精确判据**（`stateFlow_trivial_iff`）：有限型 I 中态流恒等 ⟺ 两个块内
   权重相等；即**时间存在 ⟺ 块内非标量**（P2-5 的判据形式，补上第二块的对称情形）；
5. **载体类型判据主定理**（`carrierType_criterion`）：有限型 I 内「所有态流皆内、
   无态流为外、非平凡时间存在、且块交换（唯一外自同构）不能是任何态流」四条合取。

## 记号纪律（沿用 367–371）

- 框架原生 `Δ`（`spExchangeLaw` 交换律偏差）**不出现、不赋值**；
- `Δ_mod` = Tomita–Takesaki 模算子；`M` = 模哈密顿量（自伴算子），
  `Δ_mod = e^{−2πM}`、`σ_t = Ad Δ_mod^{it}`；本模块不把 `M` 当标量；
- 「流」只作代数替身（`ℝ → A ≃ₐ[R] A`），不构造 `ρ^{it}` 复相位、不构造解析延拓。

## 诚实边界（不在本模块证明）

- 本模块的「有限型 I」只指 `M₂(ℚ) × M₂(ℚ)` 这一乘积块模型；经典
  「I/II 型因子模流由 `ρ^{it} ∈ A^×` 实现」未形式化，**III 型因子外模流的
  存在性**也未形式化；
- Tomita 事实 `Δ_mod^{it} ∈ A^×` 在本模块中是**模型输入**（`DiagState.unit`
  编码），不是从 KMS 条件推出的定理；
- 未构造连续性/强连续、解析延拓与 KMS 本体；「流」为常数切片族；
- 载体（RecObj 的忠实正规态空间/模算子/状态空间）仍未定义、vN 完成性未证
  ⇒ **P2 未成立、G3 未闭合**；不关闭任何项（226 挂起、k(2) 开放）。
-/

namespace MUFPF.G3P2CarrierType

open MUFPF.RecursionModularityOuter
open MUFPF.G3CarrierNecessity
open MUFPF.G3StateNecessity
open MUFPF.G3P2AxisOrthogonality

variable {R A : Type*} [CommSemiring R] [Ring A] [Algebra R A]

/-- 任意单位路径给出的流（有限维模实现的代数替身）。 -/
def unitFlow (u : ℝ → Aˣ) : ℝ → A ≃ₐ[R] A :=
  fun t => innerAutEquiv (R := R) (A := A) (u t)

/-- ★ 单位路径流必内：有限维中模实现由代数内部单位给出。 -/
theorem unitFlow_inner (u : ℝ → Aˣ) : InnerFlow (unitFlow (R := R) (A := A) u) :=
  fun t => innerAutEquiv_inner (R := R) (A := A) (u t)

/-- 外流：每个时刻都外（不是内实现）。 -/
def OuterFlow (σ : ℝ → A ≃ₐ[R] A) : Prop := ∀ t : ℝ, IsOuterAut (σ t)

/-- ★★ 外 ⟹ 无单位实现：若 `σ` 是外自同构，则不存在单位 `u` 使 `σ = Ad u`。
    这是「模算子 `Δ_mod^{it}` 不在代数单位群内」的代数替身。 -/
theorem outer_not_unitFlow (σ : A ≃ₐ[R] A) (hout : IsOuterAut σ) :
    ¬ ∃ u : Aˣ, σ = innerAutEquiv (R := R) (A := A) u := by
  rintro ⟨u, rfl⟩
  exact hout (innerAutEquiv_inner (R := R) (A := A) u)

/-- ★ 单位路径流不可能是外流（内与外互斥）。 -/
theorem unitFlow_not_outer (u : ℝ → Aˣ) :
    ¬ OuterFlow (unitFlow (R := R) (A := A) u) := by
  intro h
  exact h 0 (unitFlow_inner (R := R) (A := A) u 0)

/-! ### 有限型 I：忠实对角态的模流 -/

/-- 有限型 I 中的态流：块对角忠实态的模实现切片族（复用 371 的 `blockStateFlow`）。 -/
def stateFlow (s₁ s₂ : DiagState) : ℝ → TwoBlockAlg ≃ₐ[ℚ] TwoBlockAlg :=
  blockStateFlow s₁ s₂

/-- ★★ 有限型 I 的忠实态流全内。 -/
theorem finiteTypeI_stateFlow_inner (s₁ s₂ : DiagState) :
    InnerFlow (stateFlow s₁ s₂) :=
  blockStateFlow_inner s₁ s₂

/-- ★★ 有限型 I 的忠实态流不可能是外流（外流在该模型内不可由忠实态生成）。 -/
theorem finiteTypeI_stateFlow_not_outer (s₁ s₂ : DiagState) :
    ¬ OuterFlow (stateFlow s₁ s₂) := by
  intro h
  exact h 0 (blockStateAut_inner s₁ s₂)

/-- 第二块非标量 ⟹ 块对角切片非恒等（补 371 第一块情形的对称版本）。 -/
theorem blockStateAut_nontrivial_snd (s₁ s₂ : DiagState) (h : s₂.d₁ ≠ s₂.d₂) :
    blockStateAut s₁ s₂ ≠ AlgEquiv.refl := by
  obtain ⟨a, ha⟩ := s₂.conj_nontrivial h
  intro he
  have h2 : blockStateAut s₁ s₂ (0, a) = (0, a) := by
    rw [he]
    rfl
  have h3 : ((0 : BlockMat),
      (s₂.unit : BlockMat) * a * ((s₂.unit⁻¹ : BlockMatˣ) : BlockMat)) = (0, a) := by
    simpa [blockStateAut, blockwiseAut, prodUnit, innerAutEquiv] using h2
  exact ha (congrArg Prod.snd h3)

/-- ★★ 时间的精确判据：有限型 I 中态流恒等 ⟺ 两个块内权重都相等
    （即「时间存在 ⟺ 每个块内非标量」）。 -/
theorem stateFlow_trivial_iff (s₁ s₂ : DiagState) :
    stateFlow s₁ s₂ 0 = AlgEquiv.refl ↔ s₁.blockScalar ∧ s₂.blockScalar := by
  constructor
  · intro h
    constructor
    · by_contra h₁
      exact blockStateAut_nontrivial s₁ s₂ h₁ h
    · by_contra h₂
      exact blockStateAut_nontrivial_snd s₁ s₂ h₂ h
  · rintro ⟨h₁, h₂⟩
    exact blockStateAut_trivial s₁ s₂ h₁ h₂

/-! ### 载体类型判据主定理 -/

/-- ★★★ P2-7 主定理（载体类型判据的可机检部分）：
    - 有限型 I 中所有忠实态流都是内流；
    - 因而没有忠实态流是外流；
    - 非平凡时间存在，且恰在块内非标量时出现；
    - 块交换（本模型唯一外自同构）不是任何忠实态流的时刻切片。
    合读：**载体类型（模流能否被代数单位实现）才是 P2 的判据**；内/外轴本身无判别力。 -/
theorem carrierType_criterion :
    (∀ s₁ s₂ : DiagState, InnerFlow (stateFlow s₁ s₂)) ∧
    (∀ s₁ s₂ : DiagState, ¬ OuterFlow (stateFlow s₁ s₂)) ∧
    (∀ s₁ s₂ : DiagState,
        (stateFlow s₁ s₂ 0 = AlgEquiv.refl ↔ s₁.blockScalar ∧ s₂.blockScalar)) ∧
    (∃ s₁ s₂ : DiagState, stateFlow s₁ s₂ 0 ≠ AlgEquiv.refl) ∧
    (¬ ∃ s₁ s₂ : DiagState, ∀ a : TwoBlockAlg,
        swapBlockAlgEquiv a = stateFlow s₁ s₂ 0 a) := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · intro s₁ s₂
    exact finiteTypeI_stateFlow_inner s₁ s₂
  · intro s₁ s₂
    exact finiteTypeI_stateFlow_not_outer s₁ s₂
  · intro s₁ s₂
    exact stateFlow_trivial_iff s₁ s₂
  · refine ⟨⟨2/3, 1/3, by norm_num, by norm_num⟩,
      ⟨1/2, 1/2, by norm_num, by norm_num⟩, ?_⟩
    exact blockStateAut_nontrivial _ _ (by norm_num)
  · rintro ⟨s₁, s₂, h⟩
    have h1 := h (1, 0)
    have h2 : stateFlow s₁ s₂ 0 (1, 0) = (1, 0) := by
      simpa [stateFlow, blockStateFlow, blockStateAut] using
        blockwiseAut_one_zero s₁.unit s₂.unit
    have h3 : ((0 : BlockMat), (1 : BlockMat)) = ((1 : BlockMat), (0 : BlockMat)) := by
      calc ((0 : BlockMat), (1 : BlockMat)) = swapBlockAlgEquiv (1, 0) := rfl
        _ = stateFlow s₁ s₂ 0 (1, 0) := h1
        _ = ((1 : BlockMat), (0 : BlockMat)) := h2
    exact one_ne_zero ((congrArg Prod.fst h3).symm)

end MUFPF.G3P2CarrierType
