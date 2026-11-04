import Mathlib.Algebra.Algebra.Equiv
import Mathlib.Algebra.Algebra.Prod
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Mul
import Mathlib.Data.Rat.Defs
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.Tactic.NormNum

import MUFPFormalization.G3P2VNInterface

/-!
# G3-P2-10：非对角忠实态的单位可实现性——类型判据拆除对角化限制（2026-11-04）

对应 `notes/04_lorentz_gravity/递归模同构_立项_时间模流生成链.md` §3（P2）与
roadmap P7-5e-378。P2-9（377）把载体类型判据读成「谱比决定流、类型不由代数单独
决定」，但其「非 III」半边只在**对角忠实态**（`DiagState`）内成立，非对角密度矩阵
的谱分解未形式化。本模块去掉「对角」这一限制：

1. **一般忠实正定块态**（`FaithfulBlockState`）：对称矩阵 `[[a,b],[b,c]]` 的正定
   条件编码为 `0 < a` 与 `0 < a*c − b²`；由行列式非零得到代数单位
   （`FaithfulBlockState.unit`）——**不需要对角化/谱分解**；
2. **单位共轭恒等 ⟺ 态为标量**（`conj_trivial_iff`）：`Ad ρ = id` 当且仅当
   `ρ` 是标量矩阵；证明只用与 `E₁₂` 的交换子，不用特征值；
3. **非标量 ⟹ 存在非平凡共轭**（`conj_nontrivial`）：逆否形式；
4. **任一忠实正定块态流单位可实现**（`faithfulFlow_unitRealizable`）：
   常数单位路径；
5. **非平凡判据**（`faithfulFlow_trivial_iff` / `faithfulFlow_nontrivial`）：
   两块的流恒等 ⟺ 两块都标量；某块非标量 ⟹ 流非平凡；
6. **非对角见证**（`nonDiagonalState` / `nonDiagonalFlow_nontrivial`）：
   `[[2,1],[1,1]]` 是忠实正定、非对角、非标量的态，其流非平凡且单位可实现；
7. **主定理**（`faithfulBlockState_criterion`）：三支合取——所有忠实正定块态流
   单位可实现；流恒等 ⟺ 两块标量；存在非对角非平凡流。

## 记号纪律（沿用 367–377）

- 框架原生 `Δ`（`spExchangeLaw` 交换律偏差）**不出现、不赋值**；
- `Δ_mod` = Tomita–Takesaki 模算子；`M` = 模哈密顿量（自伴算子），
  `Δ_mod = e^{−2πM}`、`σ_t = Ad Δ_mod^{it}`；本模块不把 `M` 当标量；
- 本模块的「态流」是**态矩阵自身的共轭** `Ad ρ`（代数替身），不是 `ρ^{it}`；
  不构造复相位、不构造解析延拓，也不构造 KMS 本体。

## 诚实边界（不在本模块证明）

- 「忠实正定」只编码为 `0 < a`、`0 < a*c − b²`（有限维 2×2）；正规性、
  σ-弱闭、因子性、一般维数正定性均未形式化；
- `Ad ρ` 只是模流 `Ad Δ_mod^{it}` 的**代数替身**；`ρ^{it}` 复相位、解析延拓、
  KMS 本体未构造；因此「单位可实现」仍不是从 KMS 条件推出的定理；
- **谱比判据仍只对对角态成立**（377）：非对角态的模谱/特征值分解未形式化；
  本模块只拆掉「非 III 半边」的对角化限制，不声称非对角态的谱刚性；
- 经典因子 I/II/III 分类、Tomita `Δ_mod^{it} ∈ A^×` 未形式化；载体（RecObj 的
  忠实正规态空间/模算子/状态空间）仍未定义、vN 完成性未证
  ⇒ **P2 未成立、G3 未闭合**；不关闭任何项（226 挂起、k(2) 开放）。
- **操作性判据仍未形式化**：本模块只给出代数层「单位共轭恒等 ⟺ 标量」的等价，
  不构造任何可观测的模流读出协议，因此不声称「载体类型可被实验操作判定」。
-/

namespace MUFPF.G3P2FaithfulBlockState

open MUFPF.RecursionModularityOuter
open MUFPF.G3CarrierNecessity
open MUFPF.G3StateNecessity
open MUFPF.G3P2AxisOrthogonality
open MUFPF.G3P2CarrierType
open MUFPF.G3P2VNInterface

/-- 一般 2×2 忠实正定块态（对称矩阵 `[[a,b],[b,c]]`）。
    **忠实性编码**：`0 < a` 且 `0 < a*c − b²`（2×2 正定的 Sylvester 判据）。 -/
structure FaithfulBlockState where
  a : ℚ
  b : ℚ
  c : ℚ
  pos_a : 0 < a
  pos_det : 0 < a * c - b * b

/-- 态矩阵 `[[a,b],[b,c]]`（显式 if 形式，避免依赖矩阵记法模块的构建产物）。 -/
def FaithfulBlockState.mat (s : FaithfulBlockState) : BlockMat :=
  fun i j => if i = 0 then (if j = 0 then s.a else s.b)
    else (if j = 0 then s.b else s.c)

/-- 态矩阵的行列式。 -/
def FaithfulBlockState.det (s : FaithfulBlockState) : ℚ := s.a * s.c - s.b * s.b

/-- 行列式与显式式一致。 -/
theorem FaithfulBlockState.det_eq (s : FaithfulBlockState) :
    s.mat.det = s.det := by
  simp [FaithfulBlockState.mat, FaithfulBlockState.det, Matrix.det_fin_two]

/-- 行列式为可逆元（正定 ⟹ 非零）。 -/
theorem FaithfulBlockState.isUnit_det (s : FaithfulBlockState) : IsUnit s.mat.det := by
  rw [s.det_eq]
  exact isUnit_iff_ne_zero.mpr (ne_of_gt s.pos_det)

/-- 由可逆矩阵构造代数单位（`Matrix.nonsing_inv` 给出双侧逆）。 -/
noncomputable def matUnit (A : BlockMat) (h : IsUnit A.det) : BlockMatˣ where
  val := A
  inv := A⁻¹
  val_inv := Matrix.mul_nonsing_inv A h
  inv_val := Matrix.nonsing_inv_mul A h

/-- 忠实正定块态给出的代数单位（模实现的代数替身）。 -/
noncomputable def FaithfulBlockState.unit (s : FaithfulBlockState) : BlockMatˣ :=
  matUnit s.mat s.isUnit_det

/-- 块内标量性：态矩阵是标量矩阵。 -/
def FaithfulBlockState.isScalar (s : FaithfulBlockState) : Prop :=
  ∃ c : ℚ, s.mat = algebraMap ℚ BlockMat c

/-- ★★ 单位共轭恒等 ⟺ 态为标量（只用与 `E₁₂` 的交换子，不用特征值）。 -/
theorem FaithfulBlockState.conj_trivial_iff (s : FaithfulBlockState) :
    (∀ A : BlockMat, s.mat * A * s.mat⁻¹ = A) ↔ s.isScalar := by
  constructor
  · intro h
    have hcomm : ∀ A : BlockMat, s.mat * A = A * s.mat := by
      intro A
      have hA := congrArg (fun M : BlockMat => M * s.mat) (h A)
      simpa [Matrix.mul_assoc, Matrix.nonsing_inv_mul s.mat s.isUnit_det, mul_one] using hA
    have hb : s.b = 0 := by
      have := congrArg (fun M : BlockMat => M 0 0) (hcomm e12)
      simpa [FaithfulBlockState.mat, e12, Matrix.mul_apply, Fin.sum_univ_two] using this.symm
    have hac : s.a = s.c := by
      have := congrArg (fun M : BlockMat => M 0 1) (hcomm e12)
      simpa [FaithfulBlockState.mat, e12, Matrix.mul_apply, Fin.sum_univ_two] using this
    refine ⟨s.a, ?_⟩
    ext i j
    fin_cases i <;> fin_cases j <;>
      simp [FaithfulBlockState.mat, hb, hac, Matrix.algebraMap_matrix_apply]
  · rintro ⟨c, hc⟩
    have hc' : (s.unit : BlockMat) = algebraMap ℚ BlockMat c := by
      simpa [FaithfulBlockState.unit, matUnit] using hc
    intro A
    exact conj_trivial_of_scalar s.unit c hc' A

/-- ★★ 非标量 ⟹ 存在非平凡共轭（共轭恒等必标量的逆否）。 -/
theorem FaithfulBlockState.conj_nontrivial (s : FaithfulBlockState) (h : ¬ s.isScalar) :
    ∃ A : BlockMat, s.mat * A * s.mat⁻¹ ≠ A := by
  by_contra hc
  push Not at hc
  exact h (s.conj_trivial_iff.1 hc)

/-- 两块的一般忠实态流（`Ad ρ` 的常数切片族）。 -/
noncomputable def faithfulFlow (s₁ s₂ : FaithfulBlockState) :
    ℝ → TwoBlockAlg ≃ₐ[ℚ] TwoBlockAlg :=
  fun _ => blockwiseAut s₁.unit s₂.unit

/-- ★★ 任一忠实正定块态流都单位可实现（常数单位路径，不需要对角化）。 -/
theorem faithfulFlow_unitRealizable (s₁ s₂ : FaithfulBlockState) :
    UnitRealizable (faithfulFlow s₁ s₂) :=
  ⟨fun _ => prodUnit s₁.unit s₂.unit, fun _ => rfl⟩

/-- 块对角自同构作用于第一块的具体形式。 -/
theorem blockwiseAut_fst (u₁ u₂ : BlockMatˣ) (A : BlockMat) :
    (blockwiseAut u₁ u₂ (A, 0)).1 =
      (u₁ : BlockMat) * A * ((u₁⁻¹ : BlockMatˣ) : BlockMat) := by
  simp [blockwiseAut, innerAutEquiv, prodUnit]

/-- 块对角自同构作用于第二块的具体形式。 -/
theorem blockwiseAut_snd (u₁ u₂ : BlockMatˣ) (A : BlockMat) :
    (blockwiseAut u₁ u₂ (0, A)).2 =
      (u₂ : BlockMat) * A * ((u₂⁻¹ : BlockMatˣ) : BlockMat) := by
  simp [blockwiseAut, innerAutEquiv, prodUnit]

/-- ★★ 两块流恒等 ⟺ 两块都标量。 -/
theorem faithfulFlow_trivial_iff (s₁ s₂ : FaithfulBlockState) :
    faithfulFlow s₁ s₂ 0 = AlgEquiv.refl ↔ s₁.isScalar ∧ s₂.isScalar := by
  constructor
  · intro h
    have hfix₁ : ∀ A : BlockMat, s₁.mat * A * s₁.mat⁻¹ = A := by
      intro A
      have hA := congrArg
        (fun e : TwoBlockAlg ≃ₐ[ℚ] TwoBlockAlg => (e (A, 0)).1) h
      simpa [faithfulFlow, blockwiseAut_fst, FaithfulBlockState.unit, matUnit] using hA
    have hfix₂ : ∀ A : BlockMat, s₂.mat * A * s₂.mat⁻¹ = A := by
      intro A
      have hA := congrArg
        (fun e : TwoBlockAlg ≃ₐ[ℚ] TwoBlockAlg => (e (0, A)).2) h
      simpa [faithfulFlow, blockwiseAut_snd, FaithfulBlockState.unit, matUnit] using hA
    exact ⟨s₁.conj_trivial_iff.1 hfix₁, s₂.conj_trivial_iff.1 hfix₂⟩
  · rintro ⟨h₁, h₂⟩
    apply AlgEquiv.ext
    intro a
    apply Prod.ext
    · have := s₁.conj_trivial_iff.2 h₁ a.1
      simpa [faithfulFlow, blockwiseAut, innerAutEquiv, prodUnit, FaithfulBlockState.unit, matUnit]
        using this
    · have := s₂.conj_trivial_iff.2 h₂ a.2
      simpa [faithfulFlow, blockwiseAut, innerAutEquiv, prodUnit, FaithfulBlockState.unit, matUnit]
        using this

/-- ★★ 某块非标量 ⟹ 流非平凡。 -/
theorem faithfulFlow_nontrivial (s₁ s₂ : FaithfulBlockState)
    (h : ¬ s₁.isScalar ∨ ¬ s₂.isScalar) :
    faithfulFlow s₁ s₂ 0 ≠ AlgEquiv.refl := by
  intro hrefl
  have htriv := (faithfulFlow_trivial_iff s₁ s₂).1 hrefl
  rcases h with h₁ | h₂
  · exact h₁ htriv.1
  · exact h₂ htriv.2

/-- 非对角忠实正定见证 `[[2,1],[1,1]]`（`det = 1`、`b = 1 ≠ 0`）。 -/
def nonDiagonalState : FaithfulBlockState where
  a := 2
  b := 1
  c := 1
  pos_a := by norm_num
  pos_det := by norm_num

/-- 非对角见证不是标量。 -/
theorem nonDiagonalState_not_scalar : ¬ nonDiagonalState.isScalar := by
  rintro ⟨c, hc⟩
  have hb : (1 : ℚ) = 0 := by
    have h := congrArg (fun M : BlockMat => M 0 1) hc
    simp [nonDiagonalState, FaithfulBlockState.mat, Matrix.algebraMap_matrix_apply] at h
  norm_num at hb

/-- ★★ 非对角见证的流非平凡。 -/
theorem nonDiagonalFlow_nontrivial :
    faithfulFlow nonDiagonalState nonDiagonalState 0 ≠ AlgEquiv.refl :=
  faithfulFlow_nontrivial _ _ (Or.inl nonDiagonalState_not_scalar)

/-- ★★★ P2-10 主定理：类型判据的非 III 半边不需要对角化。
    - 任一忠实正定块态流都单位可实现；
    - 流恒等 ⟺ 两块都标量；
    - 存在非对角、非标量、非平凡的忠实态流。
    合读：有限块模型中的「非 III / 内实现」判据可扩展到**一般（含非对角）**
    忠实正定态，而不依赖谱分解；但 `Ad ρ` 仍是模流的代数替身，
    且谱比判据（377）仍只对对角态成立（见诚实边界）。 -/
theorem faithfulBlockState_criterion :
    (∀ s₁ s₂ : FaithfulBlockState, UnitRealizable (faithfulFlow s₁ s₂)) ∧
    (∀ s₁ s₂ : FaithfulBlockState,
      (faithfulFlow s₁ s₂ 0 = AlgEquiv.refl ↔ s₁.isScalar ∧ s₂.isScalar)) ∧
    (∃ s₁ s₂ : FaithfulBlockState,
      ¬ s₁.isScalar ∧ faithfulFlow s₁ s₂ 0 ≠ AlgEquiv.refl) := by
  refine ⟨faithfulFlow_unitRealizable, ?_, ?_⟩
  · intro s₁ s₂
    exact faithfulFlow_trivial_iff s₁ s₂
  · exact ⟨nonDiagonalState, nonDiagonalState,
      nonDiagonalState_not_scalar, nonDiagonalFlow_nontrivial⟩

end MUFPF.G3P2FaithfulBlockState
