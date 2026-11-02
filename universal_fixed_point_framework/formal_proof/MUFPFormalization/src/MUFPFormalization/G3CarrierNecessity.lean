import Mathlib.Algebra.Algebra.Equiv
import Mathlib.Algebra.Algebra.Prod
import Mathlib.Algebra.Algebra.Subalgebra.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Block
import Mathlib.Data.Rat.Defs
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.NormNum

import MUFPFormalization.RecursionModularityOuter

/-!
# G3-P2-4：载体必要性判别（交换载体 / 块标量模流 / 内流与外步互斥，2026-11-02）

对应 `notes/04_lorentz_gravity/递归模同构_立项_时间模流生成链.md` §3（P2）与
roadmap P7-5e-369。P1b-3（368）已把「外 ⟹ 模权不可内吸收」机检；本模块处理
其**载体侧**缺口：RecObj 的忠实正规态/模算子/状态空间尚未定义。

## 记号纪律（沿用 367/368）

- 框架原生 `Δ`（`spExchangeLaw` 交换律偏差）**不出现、不赋值**；
- `Δ_mod` = Tomita–Takesaki 模算子；`M` = **模哈密顿量**（自伴算子），
  `Δ_mod = e^{−2πM}`、`σ_t = Ad Δ_mod^{it} = Ad e^{−2πitM}`；
- 本模块不对框架 `Δ` 作任何数值赋值，也不把 `M` 当标量。

## 本模块机检的三条载体判别

1. **中心单位共轭平凡**（`conj_eq_of_commute`）：与 `a` 交换的单位 `u` 的共轭
   不动 `a`。由此，块标量（层对角）单位的作用是恒等
   （`blockScalarRealization_trivial`）——**层内迹态（模 Hamilton 量在块内标量）
   不产生模流**，层权 `e^{−2πn}` 单独不构成时间推进。
2. **交换载体判别**（`isOuter_iff_ne_refl`）：交换代数上「外 ⟺ 非恒等」；
   而任何内流（每个时刻都内实现）在交换代数上必恒等于单位流
   （`innerFlow_all_refl_of_commutative`）。故交换载体无法同时承载
   **非平凡模流**与**非平凡外步**——载体必须非交换。
3. **内流与外步互斥**（`innerFlow_slice_not_outer` / `outer_slice_not_innerFlow`）：
   若一个流每个时刻都内实现，则其任何切片都不是外自同构。
   Tomita 侧事实是「模流切片由 `Δ_mod^{it} ∈ A^×` 实现，故内」；因此
   **P1 的外步 `σ_s` 不可能是任何忠实正规态的模流时刻**——P1（外性/单向）
   与 P2（KMS 时间）是两条独立腿，而不是同一条。

## 诚实边界（不在本模块证明）

- **Tomita 事实「模流切片内实现」未形式化**：本模块只形式化其代数替身
  `InnerFlow`（每时刻内实现的流）；`Δ_mod^{it} ∈ A^×` 属算子代数层，未在
  Lean/Mathlib 机检。
- **忠实正规态的存在性/唯一性未形式化**：有限维情形的正规性自动成立，
  但不构造 vN 代数与 σ-弱闭、因子性；vN 完成性仍缺。
- **载体（RecObj 的态空间）未定义**：本模块只给载体**必要条件**，不构造载体。
- 因此 **P2 未成立、G3 未闭合**；不关闭任何项（226 挂起、k(2) 开放）。
-/

namespace MUFPF.G3CarrierNecessity

open MUFPF.RecursionModularityOuter

variable {R A : Type*} [CommSemiring R] [Ring A] [Algebra R A]

/-- ★ 内流：每个时刻的切片都是内自同构。
    这是「模流切片内实现」（Tomita：`σ_t = Ad Δ_mod^{it}`，`Δ_mod^{it} ∈ A^×`）
    的代数替身——本定义只编码「切片全内」，不引用 `Δ_mod`。 -/
def InnerFlow (σ : ℝ → A ≃ₐ[R] A) : Prop := ∀ t : ℝ, InnerRealization (σ t)

/-- ★★ 与 `a` 交换的单位共轭不动 `a`（中心单位作用平凡）。 -/
theorem conj_eq_of_commute (u : Aˣ) (a : A) (h : (u : A) * a = a * (u : A)) :
    (u : A) * a * ((u⁻¹ : Aˣ) : A) = a := by
  rw [h, mul_assoc, Units.mul_inv, mul_one]

/-- 恒等自同构是内实现（单位 1 共轭）。 -/
theorem refl_inner : InnerRealization (AlgEquiv.refl : A ≃ₐ[R] A) := by
  refine ⟨1, ?_⟩
  intro a
  simp

/-- 恒等自同构不是外自同构。 -/
theorem not_outer_refl : ¬ IsOuterAut (AlgEquiv.refl : A ≃ₐ[R] A) :=
  fun h => h refl_inner

section Commutative

variable {R A : Type*} [CommSemiring R] [CommRing A] [Algebra R A]

/-- ★★ 交换载体判别：**外 ⟺ 非恒等**。
    一面是 `isOuter_of_ne_refl`（非恒等 ⟹ 外），另一面是恒等本身内实现。 -/
theorem isOuter_iff_ne_refl {σ : A ≃ₐ[R] A} :
    IsOuterAut σ ↔ σ ≠ AlgEquiv.refl := by
  constructor
  · intro hout h
    rw [h] at hout
    exact hout refl_inner
  · exact isOuter_of_ne_refl

/-- ★★★ 交换载体上任何内流恒等于单位流：`InnerFlow σ ⟹ σ t = refl`。
    即交换载体**没有非平凡模流**可言（内实现必恒等）。 -/
theorem innerFlow_all_refl_of_commutative (σ : ℝ → A ≃ₐ[R] A) (h : InnerFlow σ) :
    ∀ t : ℝ, σ t = AlgEquiv.refl :=
  fun t => inner_eq_refl_of_commutative (h t)

/-- ★★ 内流的切片不是外自同构。 -/
theorem innerFlow_slice_not_outer (σ : ℝ → A ≃ₐ[R] A) (h : InnerFlow σ) (t : ℝ) :
    ¬ IsOuterAut (σ t) :=
  fun hout => hout (h t)

/-- ★★★ 外步与内流互斥：若某时刻切片是外自同构，则整个流不是内流。
    读法（Tomita）：外步 `σ_s` 不可能是任何忠实正规态的模流时刻。 -/
theorem outer_slice_not_innerFlow (σ : ℝ → A ≃ₐ[R] A) {t : ℝ}
    (h : IsOuterAut (σ t)) : ¬ InnerFlow σ :=
  fun hflow => h (hflow t)

end Commutative

/-! ### 块标量（层对角）模流：层内迹态不产生时间推进

两层块模型复用 P1b-2 的 `TwoBlockAlg = M₂(ℚ) × M₂(ℚ)`。块标量单位
= 每块由标量矩阵实现（等价于层内迹态 / 模 Hamilton 量在块内标量）。
标量矩阵与全矩阵交换，故其共轭作用恒等（`conj_eq_of_commute`）。
-/

section BlockScalar

/-- ★ 块标量实现：两块各由**标量矩阵**单位共轭实现
    （层内迹态 / 层对角生成元的代数形式）。 -/
def BlockScalarRealization (σ : TwoBlockAlg ≃ₐ[ℚ] TwoBlockAlg) : Prop :=
  ∃ u₁ : BlockMatˣ, ∃ u₂ : BlockMatˣ,
    (∃ c₁ : ℚ, (u₁ : BlockMat) = algebraMap ℚ BlockMat c₁) ∧
    (∃ c₂ : ℚ, (u₂ : BlockMat) = algebraMap ℚ BlockMat c₂) ∧
    ∀ a : TwoBlockAlg,
      σ a = ((u₁ : BlockMat) * a.1 * ((u₁⁻¹ : BlockMatˣ) : BlockMat),
             (u₂ : BlockMat) * a.2 * ((u₂⁻¹ : BlockMatˣ) : BlockMat))

/-- ★ 块标量流：每一时刻都是块标量实现（层对角模流的代数替身）。 -/
def BlockScalarFlow (σ : ℝ → TwoBlockAlg ≃ₐ[ℚ] TwoBlockAlg) : Prop :=
  ∀ t : ℝ, BlockScalarRealization (σ t)

/-- ★ 标量矩阵与任意矩阵交换。 -/
theorem scalarMat_commute (c : ℚ) (b : BlockMat) :
    algebraMap ℚ BlockMat c * b = b * algebraMap ℚ BlockMat c :=
  Algebra.commutes c b

/-- 块标量实现 ⟹ 逐块内实现（前者是后者的子情形）。 -/
theorem blockScalarRealization_imp_innerBlock {σ : TwoBlockAlg ≃ₐ[ℚ] TwoBlockAlg}
    (h : BlockScalarRealization σ) : InnerBlockRealization σ := by
  obtain ⟨u₁, u₂, _h₁, _h₂, ha⟩ := h
  exact ⟨u₁, u₂, ha⟩

/-- ★★★ 块标量实现必为恒等：层内迹态（模 Hamilton 量块内标量）的模流平凡。
    证明：标量矩阵与全矩阵交换 ⟹ 每块共轭恒等（`conj_eq_of_commute`）。 -/
theorem blockScalarRealization_trivial {σ : TwoBlockAlg ≃ₐ[ℚ] TwoBlockAlg}
    (h : BlockScalarRealization σ) : σ = AlgEquiv.refl := by
  obtain ⟨u₁, u₂, ⟨c₁, hc₁⟩, ⟨c₂, hc₂⟩, ha⟩ := h
  apply AlgEquiv.ext
  intro a
  obtain ⟨a₁, a₂⟩ := a
  rw [ha (a₁, a₂)]
  change ((u₁ : BlockMat) * a₁ * ((u₁⁻¹ : BlockMatˣ) : BlockMat),
          (u₂ : BlockMat) * a₂ * ((u₂⁻¹ : BlockMatˣ) : BlockMat)) = (a₁, a₂)
  apply Prod.ext
  · show (u₁ : BlockMat) * a₁ * ((u₁⁻¹ : BlockMatˣ) : BlockMat) = a₁
    have hcomm : (u₁ : BlockMat) * a₁ = a₁ * (u₁ : BlockMat) := by
      rw [hc₁]
      exact scalarMat_commute c₁ a₁
    exact conj_eq_of_commute u₁ a₁ hcomm
  · show (u₂ : BlockMat) * a₂ * ((u₂⁻¹ : BlockMatˣ) : BlockMat) = a₂
    have hcomm : (u₂ : BlockMat) * a₂ = a₂ * (u₂ : BlockMat) := by
      rw [hc₂]
      exact scalarMat_commute c₂ a₂
    exact conj_eq_of_commute u₂ a₂ hcomm

/-- ★★ 块交换不是块标量实现：外步不能被「层对角单位」吸收
    （与 P1b-2 的 `swapBlock_not_inner` 合并）。 -/
theorem swapBlock_not_blockScalar : ¬ BlockScalarRealization swapBlockAlgEquiv := by
  intro h
  exact swapBlock_not_inner (blockScalarRealization_imp_innerBlock h)

/-- ★★ 块标量流恒等于单位流。 -/
theorem blockScalarFlow_all_refl (σ : ℝ → TwoBlockAlg ≃ₐ[ℚ] TwoBlockAlg)
    (h : BlockScalarFlow σ) : ∀ t : ℝ, σ t = AlgEquiv.refl :=
  fun t => blockScalarRealization_trivial (h t)

/-- ★★★ 外步不是块标量（层对角）流：层对角模流的时间推进与外性互斥。 -/
theorem outer_not_blockScalarFlow (σ : ℝ → TwoBlockAlg ≃ₐ[ℚ] TwoBlockAlg) {t : ℝ}
    (h : IsOuterAut (σ t)) : ¬ BlockScalarFlow σ := by
  intro hflow
  rw [blockScalarFlow_all_refl σ hflow t] at h
  exact not_outer_refl h

/-- 外自同构必不是块标量实现（同一判别的单时刻形式）。 -/
theorem outer_not_blockScalarRealization {σ : TwoBlockAlg ≃ₐ[ℚ] TwoBlockAlg}
    (h : IsOuterAut σ) : ¬ BlockScalarRealization σ := by
  intro hb
  rw [blockScalarRealization_trivial hb] at h
  exact not_outer_refl h

end BlockScalar

end MUFPF.G3CarrierNecessity
