import Mathlib.Algebra.Algebra.Equiv
import Mathlib.Algebra.Algebra.Prod
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Mul
import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.NormNum

import MUFPFormalization.G3StateNecessity

/-!
# G3-P2-6：内/外轴与恒等/非恒等轴的正交判别（2026-11-02）

对应 `notes/04_lorentz_gravity/递归模同构_立项_时间模流生成链.md` §3（P2）与
roadmap P7-5e-371。P2-4（369）给出载体侧必要条件（载体必须非交换、外步不是模流
时刻），P2-5（370）给出态侧必要条件（块内非标量）。两条合读仍留下一个判别问题：

**「内流/外步」这一轴，能否充当 P2（模流时间）的判据？**

本模块在两层非交换块模型（`M₂(ℚ) × M₂(ℚ)`，有限型 I 代数）内机检：

1. **任意单位共轭都是内实现**（`innerAutEquiv` / `innerAutEquiv_inner`）：
   由代数自身单位 `u ∈ A^×` 给出的 `Ad u` 是 `AlgEquiv`，且按定义
   满足 `InnerRealization`——**在有限块模型中「内实现」是构造性普遍的**；
2. **块内忠实对角态的两类切片都在内实现之内**：迹态型（块内标量）给出恒等，
   非标量权重给出非平凡共轭（`blockStateAut_trivial` / `blockStateAut_nontrivial`）
   ——**「时间」（非平凡共轭）不必是外**；
3. **块交换是外**（`swapBlock_outer` / `swapBlock_ne_refl`）——**外也不必是时间**
   （它甚至不是任何对角忠实态的块对角切片，`blockwiseAut_ne_swap`）；
4. 两条轴因此**正交**（`axes_orthogonal`）：
   - （内，恒等）存在；（内，非平凡）存在；
   - （外，非平凡）存在；（外，恒等）不存在。
   即「内/外」不决定「时间/非时间」，反向亦不成立。

## 记号纪律（沿用 367/368/369/370）

- 框架原生 `Δ`（`spExchangeLaw` 交换律偏差）**不出现、不赋值**；
- `Δ_mod` = Tomita–Takesaki 模算子；`M` = 模哈密顿量（自伴算子），
  `Δ_mod = e^{−2πM}`、`σ_t = Ad Δ_mod^{it}`；本模块不把 `M` 当标量；
- 本模块中的「流」只作**代数替身**（常数切片族，编码「每一时刻切片」），
  不构造 `ρ^{it}` 复相位，也不构造解析延拓。

## 诚实边界（不在本模块证明）

- **有限型 I 的普遍内流只是本模型的结论**：`M₂(ℚ) × M₂(ℚ)` 上任意单位共轭
  都是内实现；经典事实「I/II 型因子的模流由 `ρ^{it} ∈ A^×` 实现」未形式化，
  **III 型因子的外模流**（Tomita）也未形式化。
- 因此本模块给出的是**判别性 no-go**：内/外轴在有限块模型内对 P2 无判别力；
  P2 的判据必须落在模算子/态的谱结构（载体类型），而 **RecObj 的忠实正规态
  空间、模算子与 vN 完成性仍未定义**。
- 未构造连续性/强连续、解析延拓与 KMS 本体；「流」为常数切片族。
- 因此 **P2 未成立、G3 未闭合**；不关闭任何项（226 挂起、k(2) 开放）。
-/

namespace MUFPF.G3P2AxisOrthogonality

open MUFPF.RecursionModularityOuter
open MUFPF.G3CarrierNecessity
open MUFPF.G3StateNecessity

variable {R A : Type*} [CommSemiring R] [Ring A] [Algebra R A]

/-- 单位共轭 `Ad u` 提升为 `R`-代数自同构（内实现的代数本体）。 -/
def innerAutEquiv (u : Aˣ) : A ≃ₐ[R] A where
  toFun a := (u : A) * a * ((u⁻¹ : Aˣ) : A)
  invFun a := ((u⁻¹ : Aˣ) : A) * a * (u : A)
  left_inv a := by
    show ((u⁻¹ : Aˣ) : A) * ((u : A) * a * ((u⁻¹ : Aˣ) : A)) * (u : A) = a
    rw [mul_assoc, mul_assoc, Units.inv_mul, mul_one, Units.inv_mul_cancel_left]
  right_inv a := by
    show (u : A) * (((u⁻¹ : Aˣ) : A) * a * (u : A)) * ((u⁻¹ : Aˣ) : A) = a
    rw [mul_assoc, mul_assoc, Units.mul_inv, mul_one, Units.mul_inv_cancel_left]
  map_mul' a b := by
    show (u : A) * (a * b) * ((u⁻¹ : Aˣ) : A)
      = ((u : A) * a * ((u⁻¹ : Aˣ) : A)) * ((u : A) * b * ((u⁻¹ : Aˣ) : A))
    have hL : (u : A) * (a * b) * ((u⁻¹ : Aˣ) : A)
        = (u : A) * (a * (b * ((u⁻¹ : Aˣ) : A))) := by
      rw [mul_assoc, mul_assoc]
    have hR : ((u : A) * a * ((u⁻¹ : Aˣ) : A)) * ((u : A) * b * ((u⁻¹ : Aˣ) : A))
        = (u : A) * (a * (b * ((u⁻¹ : Aˣ) : A))) := by
      rw [mul_assoc, mul_assoc, mul_assoc,
        Units.inv_mul_cancel_left u (b * ((u⁻¹ : Aˣ) : A))]
    rw [hL, hR]
  map_add' a b := by
    show (u : A) * (a + b) * ((u⁻¹ : Aˣ) : A)
      = (u : A) * a * ((u⁻¹ : Aˣ) : A) + (u : A) * b * ((u⁻¹ : Aˣ) : A)
    rw [mul_add, add_mul]
  commutes' r := by
    show (u : A) * algebraMap R A r * ((u⁻¹ : Aˣ) : A) = algebraMap R A r
    have hc : (u : A) * algebraMap R A r = algebraMap R A r * (u : A) :=
      (Algebra.commutes (R := R) (A := A) r (u : A)).symm
    rw [hc, mul_assoc, Units.mul_inv, mul_one]

/-- ★ 由代数内部单位给出的共轭是内实现（按定义）。 -/
theorem innerAutEquiv_inner (u : Aˣ) :
    InnerRealization (innerAutEquiv (R := R) (A := A) u) :=
  ⟨u, fun _ => rfl⟩

/-! ### 乘积代数：单位分解与块对角自同构

两层块代数 `BlockMat × BlockMat` 的单位是单位对。下面给出分量投影与合成，
使「块对角自同构」可以显式写成 `A^×` 共轭——不引入任何逐块公设。
-/

/-- 乘积代数单位的第一个分量（块 0 的单位）。 -/
def unitFst {A B : Type*} [Monoid A] [Monoid B] (u : (A × B)ˣ) : Aˣ where
  val := u.val.1
  inv := (u⁻¹).val.1
  val_inv := (Prod.ext_iff.mp u.val_inv).1
  inv_val := (Prod.ext_iff.mp u.inv_val).1

/-- 乘积代数单位的第二个分量（块 1 的单位）。 -/
def unitSnd {A B : Type*} [Monoid A] [Monoid B] (u : (A × B)ˣ) : Bˣ where
  val := u.val.2
  inv := (u⁻¹).val.2
  val_inv := (Prod.ext_iff.mp u.val_inv).2
  inv_val := (Prod.ext_iff.mp u.inv_val).2

/-- 由两个块内单位合成乘积代数的单位（块对角单位的合取）。 -/
def prodUnit {A B : Type*} [Monoid A] [Monoid B] (u : Aˣ) (v : Bˣ) : (A × B)ˣ where
  val := ((u : A), (v : B))
  inv := ((u⁻¹ : Aˣ), (v⁻¹ : Bˣ))
  val_inv := Prod.ext u.val_inv v.val_inv
  inv_val := Prod.ext u.inv_val v.inv_val

/-- 乘积代数上任何内实现都给出逐块内实现（单位分解）。 -/
theorem innerRealization_imp_innerBlock {σ : TwoBlockAlg ≃ₐ[ℚ] TwoBlockAlg}
    (h : InnerRealization σ) : InnerBlockRealization σ := by
  obtain ⟨u, hu⟩ := h
  refine ⟨unitFst u, unitSnd u, fun a => ?_⟩
  have hpair := hu a
  apply Prod.ext
  · exact (Prod.ext_iff.mp hpair).1
  · exact (Prod.ext_iff.mp hpair).2

/-- ★ 块交换是外自同构（由 369 的 `swapBlock_not_inner` 经单位分解）。 -/
theorem swapBlock_outer : IsOuterAut swapBlockAlgEquiv :=
  fun h => swapBlock_not_inner (innerRealization_imp_innerBlock h)

/-- ★ 块交换不是恒等（非平凡外步的见证）。 -/
theorem swapBlock_ne_refl :
    swapBlockAlgEquiv ≠ (AlgEquiv.refl : TwoBlockAlg ≃ₐ[ℚ] TwoBlockAlg) := by
  intro h
  have h1 : swapBlockAlgEquiv (1, 0) = (AlgEquiv.refl : TwoBlockAlg ≃ₐ[ℚ] TwoBlockAlg) (1, 0) := by
    rw [h]
  have h2 : ((0 : BlockMat), (1 : BlockMat)) = ((1 : BlockMat), (0 : BlockMat)) := h1
  have h3 : (1 : BlockMat) = 0 := congrArg Prod.snd h2
  exact one_ne_zero h3

/-- 块对角自同构：由两个块内单位合成（`A^×` 共轭的内实现）。 -/
def blockwiseAut (u₁ u₂ : BlockMatˣ) : TwoBlockAlg ≃ₐ[ℚ] TwoBlockAlg :=
  innerAutEquiv (R := ℚ) (A := TwoBlockAlg) (prodUnit u₁ u₂)

/-- ★ 块对角自同构是内实现（实现元 = 单位对）。 -/
theorem blockwiseAut_inner (u₁ u₂ : BlockMatˣ) :
    InnerRealization (blockwiseAut u₁ u₂) :=
  innerAutEquiv_inner (prodUnit u₁ u₂)

/-- 块对角自同构固定 `(1, 0)`：第一块单位共轭不动块内单位。 -/
theorem blockwiseAut_one_zero (u₁ u₂ : BlockMatˣ) :
    blockwiseAut u₁ u₂ (1, 0) = (1, 0) := by
  show ((u₁ : BlockMat) * (1 : BlockMat) * ((u₁⁻¹ : BlockMatˣ) : BlockMat),
        (u₂ : BlockMat) * (0 : BlockMat) * ((u₂⁻¹ : BlockMatˣ) : BlockMat)) = (1, 0)
  rw [mul_one, mul_zero]
  simp

/-- ★★ 块内单位共轭不可能等于块交换：前者保持块 0，后者把块 0 搬到块 1。
    即「外」不可能是任何块对角（内）切片的极限读数。 -/
theorem blockwiseAut_ne_swap (u₁ u₂ : BlockMatˣ) :
    blockwiseAut u₁ u₂ ≠ swapBlockAlgEquiv := by
  intro h
  have h1 : blockwiseAut u₁ u₂ (1, 0) = swapBlockAlgEquiv (1, 0) := by rw [h]
  rw [blockwiseAut_one_zero] at h1
  have h2 : ((1 : BlockMat), (0 : BlockMat)) = ((0 : BlockMat), (1 : BlockMat)) := h1
  have h3 : (1 : BlockMat) = 0 := congrArg Prod.fst h2
  exact one_ne_zero h3

/-! ### 态侧：块对角忠实态的两类切片

`DiagState`（370）给出块内正权重。由 `blockwiseAut s₁.unit s₂.unit` 得到
块对角态切片：块内标量 ⟹ 恒等；块内非标量 ⟹ 非平凡。两类都是内实现。
-/

/-- 块对角态切片（两个块内忠实态的模实现合成）。 -/
def blockStateAut (s₁ s₂ : DiagState) : TwoBlockAlg ≃ₐ[ℚ] TwoBlockAlg :=
  blockwiseAut s₁.unit s₂.unit

/-- ★ 块对角态切片是内实现（无论块内标量与否）。 -/
theorem blockStateAut_inner (s₁ s₂ : DiagState) :
    InnerRealization (blockStateAut s₁ s₂) :=
  blockwiseAut_inner s₁.unit s₂.unit

/-- ★★ 块内皆标量 ⟹ 切片恒等（迹态型，无时间推进）。 -/
theorem blockStateAut_trivial (s₁ s₂ : DiagState)
    (h₁ : s₁.blockScalar) (h₂ : s₂.blockScalar) :
    blockStateAut s₁ s₂ = AlgEquiv.refl := by
  apply AlgEquiv.ext
  intro a
  obtain ⟨a₁, a₂⟩ := a
  apply Prod.ext
  · exact s₁.conj_trivial h₁ a₁
  · exact s₂.conj_trivial h₂ a₂

/-- ★★ 任一块内非标量 ⟹ 切片非恒等（非平凡时间，却仍是内实现）。 -/
theorem blockStateAut_nontrivial (s₁ s₂ : DiagState) (h : s₁.d₁ ≠ s₁.d₂) :
    blockStateAut s₁ s₂ ≠ AlgEquiv.refl := by
  obtain ⟨a, ha⟩ := s₁.conj_nontrivial h
  intro he
  have h2 : blockStateAut s₁ s₂ (a, 0) = (a, 0) := by
    rw [he]
    rfl
  have h3 : ((s₁.unit : BlockMat) * a * ((s₁.unit⁻¹ : BlockMatˣ) : BlockMat), (0 : BlockMat))
      = (a, 0) := by
    simpa [blockStateAut, blockwiseAut, prodUnit, innerAutEquiv] using h2
  exact ha (congrArg Prod.fst h3)

/-- 块对角态流（每时刻同一切片；「流」的代数替身，不构造连续性）。 -/
def blockStateFlow (s₁ s₂ : DiagState) : ℝ → TwoBlockAlg ≃ₐ[ℚ] TwoBlockAlg :=
  fun _ => blockStateAut s₁ s₂

/-- ★★ 内流普遍性：任意块对角忠实态给出内流（内/外轴无判别力）。 -/
theorem blockStateFlow_inner (s₁ s₂ : DiagState) :
    InnerFlow (blockStateFlow s₁ s₂) :=
  fun _ => blockStateAut_inner s₁ s₂

/-! ### 正交判别（两条轴的独立组合） -/

/-- ★★★ P2-6 主定理：内/外轴与恒等/非恒等轴**正交**。
    - （内，恒等）存在：块内标量态的块对角切片；
    - （内，非平凡）存在：块内非标量态（2/3, 1/3）的块对角切片；
    - （外，非平凡）存在：块交换；
    - （外，恒等）不存在：恒等是内实现（`not_outer_refl`）。
    故「内/外」既不能推出「时间」，也不能由「时间」推出——两条轴不可互换。 -/
theorem axes_orthogonal :
    (∃ s₁ s₂ : DiagState, blockStateAut s₁ s₂ = AlgEquiv.refl) ∧
    (∃ s₁ s₂ : DiagState, blockStateAut s₁ s₂ ≠ AlgEquiv.refl) ∧
    (∃ σ : TwoBlockAlg ≃ₐ[ℚ] TwoBlockAlg,
        IsOuterAut σ ∧ σ ≠ AlgEquiv.refl) ∧
    (¬ ∃ σ : TwoBlockAlg ≃ₐ[ℚ] TwoBlockAlg,
        IsOuterAut σ ∧ σ = AlgEquiv.refl) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · exact ⟨⟨1/2, 1/2, by norm_num, by norm_num⟩,
      ⟨1/2, 1/2, by norm_num, by norm_num⟩, blockStateAut_trivial _ _ rfl rfl⟩
  · exact ⟨⟨2/3, 1/3, by norm_num, by norm_num⟩,
      ⟨1/2, 1/2, by norm_num, by norm_num⟩, blockStateAut_nontrivial _ _ (by norm_num)⟩
  · exact ⟨swapBlockAlgEquiv, swapBlock_outer, swapBlock_ne_refl⟩
  · rintro ⟨σ, hout, hrefl⟩
    rw [hrefl] at hout
    exact not_outer_refl hout

end MUFPF.G3P2AxisOrthogonality
