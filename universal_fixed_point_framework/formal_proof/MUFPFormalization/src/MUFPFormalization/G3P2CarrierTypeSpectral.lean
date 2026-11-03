import Mathlib.Algebra.Algebra.Equiv
import Mathlib.Algebra.Algebra.Prod
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Diagonal
import Mathlib.Data.Matrix.Mul
import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.NormNum

import MUFPFormalization.G3P2VNInterface

/-!
# G3-P2-9：载体类型判据的谱刚性——流只依赖模谱比、类型不由代数单独决定（2026-11-03）

对应 `notes/04_lorentz_gravity/递归模同构_立项_时间模流生成链.md` §3（P2）与
roadmap P7-5e-377。P2-7（372）机检了载体类型判据的有限型 I 半边，P2-8（373）搭起
vN / III 型接口。仍留下两个关于「判据本身」的问题：

1. 载体类型判据依赖**态的什么数据**？是否依赖忠实态的绝对规范化？
2. 「载体类型」能否只读作**代数**的性质？

本模块在 `M₂(ℚ) × M₂(ℚ)` 有限块模型内机检：

1. **对角共轭的逐元公式**（`diagConj_entry`）：`diag(d₁,d₂)` 共轭把 `aᵢⱼ` 乘上
   `dᵢ/dⱼ`——流只看见**模谱比**；
2. **模谱比决定流**（`diagConj_eq_of_ratio` / `blockStateAut_eq_of_ratio` /
   `stateFlow_eq_of_ratio`）：两块比值相同 ⟹ 同一块对角流，**与权重绝对值无关**；
3. **规范不变性**（`stateFlow_scale_invariant`）：权重整体放大不改变流；
4. **时间的谱判据**（`stateFlow_trivial_iff_ratio_one`）：态流恒等 ⟺ 两块谱比皆为 1，
   即**时间存在 ⟺ 某块谱比 ≠ 1**（372 判据的规范化无关形式）；
5. **类型不由代数单独决定**（`carrierType_not_algebra_only`）：同一个载体
   `TwoBlockAlg` 上，态流是单位可实现（`stateFlow_unitRealizable`），块交换常数流
   不是（`swapFlow_not_unitRealizable`）——两条都是**非平凡**流；
6. **主定理**（`carrierType_spectral_criterion`）：谱刚性 ∧ 谱判据 ∧ 两侧非平凡
   见证 ∧ 「非恒等于单位可实现」∧「非恒等于非单位可实现」六支合取。

## 记号纪律（沿用 367–373）

- 框架原生 `Δ`（`spExchangeLaw` 交换律偏差）**不出现、不赋值**；
- `Δ_mod` = Tomita–Takesaki 模算子；`M` = 模哈密顿量（自伴算子），
  `Δ_mod = e^{−2πM}`、`σ_t = Ad Δ_mod^{it}`；本模块不把 `M` 当标量；
- 「谱比」`d₁/d₂` 是有限块模型中模权重的比值，**不是**框架原生 `Δ`；
- 「流」只作代数替身（常数切片族），不构造 `ρ^{it}` 复相位、不构造解析延拓，
  也不构造 KMS 本体；

## 诚实边界（不在本模块证明）

- 本模块的「载体类型」仍是 `M₂(ℚ) × M₂(ℚ)` 乘积块模型内的操作性谓词
  `UnitRealizable`；经典因子类型分类（I/II/III）与 Tomita `Δ_mod^{it} ∈ A^×`
  均未形式化（`UnitRealizable` 只是其代数替身）；
- 「谱比决定流」只在**对角忠实态**（`DiagState`）内成立；非对角密度矩阵的
  谱分解未形式化，一般忠实正规态的模流未构造；
- 「类型不由代数单独决定」是**同一有限块代数上的两个流见证**，不声称
  一般 vN 代数上类型谓词的非恒常性；
- 载体（RecObj 的忠实正规态空间/模算子/状态空间）仍未定义、vN 完成性未证
  ⇒ **P2 未成立、G3 未闭合**；不关闭任何项（226 挂起、k(2) 开放）。
-/

namespace MUFPF.G3P2CarrierTypeSpectral

open MUFPF.RecursionModularityOuter
open MUFPF.G3CarrierNecessity
open MUFPF.G3StateNecessity
open MUFPF.G3P2AxisOrthogonality
open MUFPF.G3P2CarrierType
open MUFPF.G3P2VNInterface

/-- 块内模谱比 `d₁/d₂`：有限块模型中模 Hamiltonian 谱间隔的载荷，规范化无关。 -/
def diagRatio (s : DiagState) : ℚ := s.d₁ / s.d₂

/-! ### 对角共轭只看见谱比 -/

/-- ★ 对角共轭的逐元公式：`diag(d₁,d₂)` 共轭把 `aᵢⱼ` 乘上 `dᵢ/dⱼ`。 -/
theorem diagConj_entry (d₁ d₂ : ℚ) (a : BlockMat) (i j : Fin 2) :
    (diagMat d₁ d₂ * a * diagMat d₁⁻¹ d₂⁻¹) i j
      = ((if i = 0 then d₁ else d₂) / (if j = 0 then d₁ else d₂)) * a i j := by
  simp only [diagMat]
  rw [Matrix.mul_assoc, Matrix.diagonal_mul, Matrix.mul_diagonal]
  by_cases hi : i = 0 <;> by_cases hj : j = 0 <;> simp [hi, hj] <;> ring

/-- ★★ 谱比相同 ⟹ 对角共轭相同（与权重的绝对大小无关）。 -/
theorem diagConj_eq_of_ratio {d₁ d₂ e₁ e₂ : ℚ}
    (hd₁ : d₁ ≠ 0) (hd₂ : d₂ ≠ 0) (he₁ : e₁ ≠ 0) (he₂ : e₂ ≠ 0)
    (h : d₁ / d₂ = e₁ / e₂) (a : BlockMat) :
    diagMat d₁ d₂ * a * diagMat d₁⁻¹ d₂⁻¹
      = diagMat e₁ e₂ * a * diagMat e₁⁻¹ e₂⁻¹ := by
  have h12 : d₁ / d₂ = e₁ / e₂ := h
  have hcross : d₁ * e₂ = e₁ * d₂ := (div_eq_div_iff hd₂ he₂).1 h
  have h21 : d₂ / d₁ = e₂ / e₁ := by
    refine (div_eq_div_iff hd₁ he₁).2 ?_
    rw [mul_comm d₂ e₁, mul_comm e₂ d₁]
    exact hcross.symm
  have h11 : d₁ / d₁ = e₁ / e₁ := by rw [div_self hd₁, div_self he₁]
  have h22 : d₂ / d₂ = e₂ / e₂ := by rw [div_self hd₂, div_self he₂]
  ext i j
  rw [diagConj_entry, diagConj_entry]
  fin_cases i <;> fin_cases j <;> simp [h12, h21, h11, h22]

/-- ★★ 块对角态切片只依赖两块谱比。 -/
theorem blockStateAut_eq_of_ratio (s₁ s₂ t₁ t₂ : DiagState)
    (h₁ : diagRatio s₁ = diagRatio t₁) (h₂ : diagRatio s₂ = diagRatio t₂) :
    blockStateAut s₁ s₂ = blockStateAut t₁ t₂ := by
  apply AlgEquiv.ext
  intro a
  apply Prod.ext
  · exact diagConj_eq_of_ratio (ne_of_gt s₁.pos₁) (ne_of_gt s₁.pos₂)
      (ne_of_gt t₁.pos₁) (ne_of_gt t₁.pos₂) h₁ a.1
  · exact diagConj_eq_of_ratio (ne_of_gt s₂.pos₁) (ne_of_gt s₂.pos₂)
      (ne_of_gt t₂.pos₁) (ne_of_gt t₂.pos₂) h₂ a.2

/-- ★★ 态流只依赖两块谱比（规范化无关的算子层陈述）。 -/
theorem stateFlow_eq_of_ratio (s₁ s₂ t₁ t₂ : DiagState)
    (h₁ : diagRatio s₁ = diagRatio t₁) (h₂ : diagRatio s₂ = diagRatio t₂) :
    stateFlow s₁ s₂ = stateFlow t₁ t₂ := by
  funext t
  exact blockStateAut_eq_of_ratio s₁ s₂ t₁ t₂ h₁ h₂

/-- ★ 整体放大权重不改变流（忠实态规范化的具体见证）。 -/
theorem stateFlow_scale_invariant :
    stateFlow ⟨2, 1, by norm_num, by norm_num⟩
        ⟨1/2, 1/2, by norm_num, by norm_num⟩
      = stateFlow ⟨6, 3, by norm_num, by norm_num⟩
          ⟨1/2, 1/2, by norm_num, by norm_num⟩ := by
  apply stateFlow_eq_of_ratio
  · norm_num [diagRatio]
  · rfl

/-! ### 时间的谱判据 -/

/-- ★★ 态流恒等 ⟺ 两块谱比皆为 1（时间存在 ⟺ 某块谱比 ≠ 1）。 -/
theorem stateFlow_trivial_iff_ratio_one (s₁ s₂ : DiagState) :
    stateFlow s₁ s₂ 0 = AlgEquiv.refl ↔ diagRatio s₁ = 1 ∧ diagRatio s₂ = 1 := by
  rw [stateFlow_trivial_iff]
  constructor
  · rintro ⟨h₁, h₂⟩
    exact ⟨(div_eq_one_iff_eq (ne_of_gt s₁.pos₂)).2 h₁,
      (div_eq_one_iff_eq (ne_of_gt s₂.pos₂)).2 h₂⟩
  · rintro ⟨h₁, h₂⟩
    exact ⟨(div_eq_one_iff_eq (ne_of_gt s₁.pos₂)).1 h₁,
      (div_eq_one_iff_eq (ne_of_gt s₂.pos₂)).1 h₂⟩

/-! ### 类型不由代数单独决定 -/

/-- ★★ 有限型 I 的任一忠实对角态流都是单位可实现（非 III）。 -/
theorem stateFlow_unitRealizable (s₁ s₂ : DiagState) :
    UnitRealizable (stateFlow s₁ s₂) :=
  ⟨stateUnitPath s₁ s₂, fun _ => rfl⟩

/-- ★★ 块交换常数流不是单位可实现（操作性 III 实例）。 -/
theorem swapFlow_not_unitRealizable :
    ¬ UnitRealizable (fun _ : ℝ => swapBlockAlgEquiv) := by
  simpa [TypeIII, swapDatum] using swapDatum_typeIII

/-- ★★ 同一载体上存在非平凡的、单位可实现的流。 -/
theorem exists_nontrivial_unitRealizable_flow :
    ∃ σ : ℝ → TwoBlockAlg ≃ₐ[ℚ] TwoBlockAlg,
      UnitRealizable σ ∧ σ 0 ≠ AlgEquiv.refl := by
  refine ⟨stateFlow ⟨2/3, 1/3, by norm_num, by norm_num⟩
      ⟨1/2, 1/2, by norm_num, by norm_num⟩,
    stateFlow_unitRealizable _ _, ?_⟩
  exact blockStateAut_nontrivial _ _ (by norm_num)

/-- ★★ 同一载体上存在非平凡的、非单位可实现的流（块交换）。 -/
theorem exists_nontrivial_not_unitRealizable_flow :
    ∃ σ : ℝ → TwoBlockAlg ≃ₐ[ℚ] TwoBlockAlg,
      ¬ UnitRealizable σ ∧ σ 0 ≠ AlgEquiv.refl := by
  refine ⟨fun _ => swapBlockAlgEquiv, swapFlow_not_unitRealizable, ?_⟩
  exact swapBlock_ne_refl

/-- ★★★ 「单位可实现」不是载体代数的常值性质：同一 `TwoBlockAlg` 上
    存在单位可实现的流，也存在非单位可实现的流。 -/
theorem carrierType_not_algebra_only :
    ¬ (∀ σ : ℝ → TwoBlockAlg ≃ₐ[ℚ] TwoBlockAlg, UnitRealizable σ) ∧
    ¬ (∀ σ : ℝ → TwoBlockAlg ≃ₐ[ℚ] TwoBlockAlg, ¬ UnitRealizable σ) := by
  constructor
  · intro h
    exact swapFlow_not_unitRealizable (h _)
  · intro h
    exact h (stateFlow ⟨1/2, 1/2, by norm_num, by norm_num⟩
      ⟨1/2, 1/2, by norm_num, by norm_num⟩)
      (stateFlow_unitRealizable _ _)

/-! ### 主定理 -/

/-- ★★★ P2-9 主定理（载体类型判据的谱刚性）：
    - 两块谱比相同 ⟹ 同一态流（流只依赖模谱比值，不依赖规范化）；
    - 态流恒等 ⟺ 两块谱比皆为 1；
    - 同一载体上非平凡的单位可实现流存在（块内非标量忠实态）；
    - 同一载体上非平凡的非单位可实现流存在（块交换）；
    - 「恒为单位可实现」与「恒为非单位可实现」都被排除。
    合读：**载体类型判据是谱的**（只依赖 `d₁/d₂`）且**相对态/流而言**，
    不是代数单独决定的；但它仍不是经典因子类型分类（见诚实边界）。 -/
theorem carrierType_spectral_criterion :
    (∀ s₁ s₂ t₁ t₂ : DiagState, diagRatio s₁ = diagRatio t₁ → diagRatio s₂ = diagRatio t₂ →
      stateFlow s₁ s₂ = stateFlow t₁ t₂) ∧
    (∀ s₁ s₂ : DiagState,
      (stateFlow s₁ s₂ 0 = AlgEquiv.refl ↔ diagRatio s₁ = 1 ∧ diagRatio s₂ = 1)) ∧
    (∃ σ : ℝ → TwoBlockAlg ≃ₐ[ℚ] TwoBlockAlg,
      UnitRealizable σ ∧ σ 0 ≠ AlgEquiv.refl) ∧
    (∃ σ : ℝ → TwoBlockAlg ≃ₐ[ℚ] TwoBlockAlg,
      ¬ UnitRealizable σ ∧ σ 0 ≠ AlgEquiv.refl) ∧
    (¬ (∀ σ : ℝ → TwoBlockAlg ≃ₐ[ℚ] TwoBlockAlg, UnitRealizable σ)) ∧
    (¬ (∀ σ : ℝ → TwoBlockAlg ≃ₐ[ℚ] TwoBlockAlg, ¬ UnitRealizable σ)) := by
  refine ⟨?_, ?_, ?_, ?_, carrierType_not_algebra_only.1,
    carrierType_not_algebra_only.2⟩
  · intro s₁ s₂ t₁ t₂ h₁ h₂
    exact stateFlow_eq_of_ratio s₁ s₂ t₁ t₂ h₁ h₂
  · intro s₁ s₂
    exact stateFlow_trivial_iff_ratio_one s₁ s₂
  · exact exists_nontrivial_unitRealizable_flow
  · exact exists_nontrivial_not_unitRealizable_flow

end MUFPF.G3P2CarrierTypeSpectral
