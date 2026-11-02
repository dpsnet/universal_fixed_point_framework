import Mathlib.Algebra.Algebra.Equiv
import Mathlib.Algebra.Algebra.Prod
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Diagonal
import Mathlib.Data.Matrix.Mul
import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.NormNum

import MUFPFormalization.G3CarrierNecessity

/-!
# G3-P2-5：态侧必要性判别（块内标量态 ⟹ 模流恒等；非标量权重 ⟹ 非平凡共轭，2026-11-02）

对应 `notes/04_lorentz_gravity/递归模同构_立项_时间模流生成链.md` §3（P2）与
roadmap P7-5e-370。P2-4（369）已机检**代数侧**载体必要条件（交换载体无模流、
块标量实现恒等、外步不是模流时刻）；本模块补其**态侧**一半：

- 忠实正规态**存在**不等于给出**非平凡时间**：块内标量（迹态型）忠实态
  的模实现是标量共轭，故模流恒等；
- 只有**块内非标量权重**（密度算子在该块内特征值不等）才给出非平凡共轭；
- 因此「层权 `e^{−2πn}` 随层变化」在态侧同样不够：层权只在块间起作用，
  块内标量仍是恒等（与 369 的 C10 同一结论的态侧读法）。

## 记号纪律（沿用 367/368/369）

- 框架原生 `Δ`（`spExchangeLaw` 交换律偏差）**不出现、不赋值**；
- `Δ_mod` = Tomita–Takesaki 模算子；`M` = **模哈密顿量**（自伴算子），
  `Δ_mod = e^{−2πM}`、`σ_t = Ad Δ_mod^{it} = Ad e^{−2πitM}`；
- 本模块不对框架 `Δ` 作任何数值赋值，也不把 `M` 当标量。

## 本模块机检的态侧判别

1. **块内标量 ⟺ 对角权重相等**（`diagMat_isScalar_iff`）。
2. **块内标量态 ⟹ 模实现恒等**（`DiagState.conj_trivial`）。
3. **块内非标量态 ⟹ 存在非平凡共轭**（`DiagState.conj_nontrivial`）：
   权重比 `d₁/d₂ ≠ 1` 时，非对角元素 `e12` 被缩放 `d₁/d₂`。
   逆否：共轭恒等 ⟹ 权重相等（`nontrivial_imp_nonScalar`）。
4. **忠实 ≠ 非平凡时间**（`faithful_not_imp_nontrivial`）：块标量忠实态
   与非标量忠实态都存在，前者恒等、后者非平凡。
5. **层权不同仍恒等**（`layerWeight_blockScalar_trivial`）：两层块内标量、
   块间权重不等，全块共轭仍恒等——**层权单独不构成时间**。

## 诚实边界（不在本模块证明）

- **「忠实」只编码为对角权重为正**（`0 < d₁`、`0 < d₂`）：有限维因子上
  「正定 ⟺ 忠实」、正规性、σ-弱闭与因子性均未形式化。
- **未构造 `ρ^{it}` 的复相位**：只证「非标量权重 ⟹ 存在非平凡共轭」的
  代数骨架；具体模流时刻的相位未形式化。
- **非对角（一般密度矩阵）态的谱分解未形式化**：只处理对角（层权）态。
- **载体（RecObj 的忠实正规态空间/模算子）仍未定义，vN 完成性未证**；
  Tomita 事实 `Δ_mod^{it} ∈ A^×` 未形式化。
- 因此 **P2 未成立、G3 未闭合**；不关闭任何项（226 挂起、k(2) 开放）。
-/

namespace MUFPF.G3StateNecessity

open MUFPF.RecursionModularityOuter
open MUFPF.G3CarrierNecessity

/-- 对角权重矩阵 `diag(d₁, d₂)`（有限维块内密度算子的形状）。 -/
def diagMat (d₁ d₂ : ℚ) : BlockMat :=
  Matrix.diagonal (fun i : Fin 2 => if i = 0 then d₁ else d₂)

/-- 偏离对角线元素 `E₁₂`（块内相干探针）。 -/
def e12 : BlockMat :=
  fun i j => if i = 0 ∧ j = 1 then (1 : ℚ) else 0

/-- 同权重对角矩阵是标量矩阵。 -/
theorem diagMat_self_eq_algebraMap (c : ℚ) :
    diagMat c c = algebraMap ℚ BlockMat c := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [diagMat, Matrix.algebraMap_matrix_apply]

/-- 对角权重矩阵是标量矩阵 ⟺ 两权重相等。 -/
theorem diagMat_isScalar_iff (d₁ d₂ : ℚ) :
    (∃ c : ℚ, diagMat d₁ d₂ = algebraMap ℚ BlockMat c) ↔ d₁ = d₂ := by
  constructor
  · rintro ⟨c, hc⟩
    have h00 : d₁ = c := by
      have := congrArg (fun m : BlockMat => m 0 0) hc
      simpa [diagMat, Matrix.algebraMap_matrix_apply] using this
    have h11 : d₂ = c := by
      have := congrArg (fun m : BlockMat => m 1 1) hc
      simpa [diagMat, Matrix.algebraMap_matrix_apply] using this
    rw [h00, h11]
  · intro h
    refine ⟨d₁, ?_⟩
    rw [h.symm]
    exact diagMat_self_eq_algebraMap d₁

/-- 对角权重单位 `diag(d₁, d₂)`（权重非零故可逆）。 -/
def diagUnit (d₁ d₂ : ℚ) (h₁ : d₁ ≠ 0) (h₂ : d₂ ≠ 0) : BlockMatˣ where
  val := diagMat d₁ d₂
  inv := diagMat d₁⁻¹ d₂⁻¹
  val_inv := by
    rw [diagMat, diagMat, Matrix.diagonal_mul_diagonal, ← Matrix.diagonal_one]
    congr 1
    funext i
    fin_cases i <;> simp [h₁, h₂, mul_inv_cancel₀]
  inv_val := by
    rw [diagMat, diagMat, Matrix.diagonal_mul_diagonal, ← Matrix.diagonal_one]
    congr 1
    funext i
    fin_cases i <;> simp [h₁, h₂, inv_mul_cancel₀]

/-- 单位共轭公式：`u E₁₂ u⁻¹ = (d₁/d₂) • E₁₂`。 -/
theorem conj_e12_of_diagUnit (u : BlockMatˣ) (d₁ d₂ : ℚ)
    (hval : (u : BlockMat) = diagMat d₁ d₂)
    (hinv : ((u⁻¹ : BlockMatˣ) : BlockMat) = diagMat d₁⁻¹ d₂⁻¹) :
    (u : BlockMat) * e12 * ((u⁻¹ : BlockMatˣ) : BlockMat) = (d₁ / d₂) • e12 := by
  have hmul : diagMat d₁ d₂ * e12 = d₁ • e12 := by
    ext i j
    by_cases h : i = 0 ∧ j = 1
    · rw [h.1, h.2]
      simp [diagMat, e12]
    · simp [diagMat, e12, h]
  have hmul' : e12 * diagMat d₁⁻¹ d₂⁻¹ = d₂⁻¹ • e12 := by
    ext i j
    by_cases h : i = 0 ∧ j = 1
    · rw [h.1, h.2]
      simp [diagMat, e12]
    · simp [diagMat, e12, h]
  rw [hval, hinv, hmul, Matrix.smul_mul, hmul', smul_smul, div_eq_mul_inv]

/-- 标量实现的共轭恒等（复用 P2-4 的 `conj_eq_of_commute`）。 -/
theorem conj_trivial_of_scalar (u : BlockMatˣ) (c : ℚ)
    (hc : (u : BlockMat) = algebraMap ℚ BlockMat c) (a : BlockMat) :
    (u : BlockMat) * a * ((u⁻¹ : BlockMatˣ) : BlockMat) = a := by
  refine conj_eq_of_commute u a ?_
  rw [hc]
  exact scalarMat_commute c a

/-- 权重比不为 1（非标量权重探针非平凡）。 -/
theorem weightRatio_ne_one {d₁ d₂ : ℚ} (h₂ : d₂ ≠ 0) (hne : d₁ ≠ d₂) :
    d₁ / d₂ ≠ 1 := by
  intro h
  apply hne
  have h1 : d₁ * d₂⁻¹ = 1 := by simpa [div_eq_mul_inv] using h
  calc d₁ = d₁ * (d₂⁻¹ * d₂) := by rw [inv_mul_cancel₀ h₂, mul_one]
    _ = (d₁ * d₂⁻¹) * d₂ := by rw [mul_assoc]
    _ = 1 * d₂ := by rw [h1]
    _ = d₂ := one_mul d₂

/-- 对角态：两个正权重（有限维块内对角密度算子形状）。
    **忠实性编码**：`0 < d₁`、`0 < d₂`（「正定 ⟺ 忠实」未形式化）。 -/
structure DiagState where
  d₁ : ℚ
  d₂ : ℚ
  pos₁ : 0 < d₁
  pos₂ : 0 < d₂

/-- 对角态的块内标量性：两权重相等（迹态型）。 -/
def DiagState.blockScalar (s : DiagState) : Prop := s.d₁ = s.d₂

/-- 对角态的单位（模实现的代数替身）。 -/
def DiagState.unit (s : DiagState) : BlockMatˣ :=
  diagUnit s.d₁ s.d₂ (ne_of_gt s.pos₁) (ne_of_gt s.pos₂)

/-- 块内标量忠实态 ⟹ 模实现恒等（迹态型不产生时间推进）。 -/
theorem DiagState.conj_trivial (s : DiagState) (h : s.blockScalar) (a : BlockMat) :
    (s.unit : BlockMat) * a * ((s.unit⁻¹ : BlockMatˣ) : BlockMat) = a := by
  refine conj_trivial_of_scalar s.unit s.d₁ ?_ a
  show diagMat s.d₁ s.d₂ = algebraMap ℚ BlockMat s.d₁
  rw [h.symm]
  exact diagMat_self_eq_algebraMap s.d₁

/-- 块内非标量忠实态 ⟹ 存在非平凡共轭（时间推进的必要条件）。 -/
theorem DiagState.conj_nontrivial (s : DiagState) (h : s.d₁ ≠ s.d₂) :
    ∃ a : BlockMat,
      (s.unit : BlockMat) * a * ((s.unit⁻¹ : BlockMatˣ) : BlockMat) ≠ a := by
  refine ⟨e12, ?_⟩
  have hval : (s.unit : BlockMat) = diagMat s.d₁ s.d₂ := rfl
  have hinv : ((s.unit⁻¹ : BlockMatˣ) : BlockMat) = diagMat s.d₁⁻¹ s.d₂⁻¹ := rfl
  have hconj : (s.unit : BlockMat) * e12 * ((s.unit⁻¹ : BlockMatˣ) : BlockMat)
      = (s.d₁ / s.d₂) • e12 := conj_e12_of_diagUnit s.unit s.d₁ s.d₂ hval hinv
  rw [hconj]
  intro hfix
  have hentry : s.d₁ / s.d₂ = 1 := by
    have := congrArg (fun m : BlockMat => m 0 1) hfix
    simpa [Pi.smul_apply, e12] using this
  exact weightRatio_ne_one (ne_of_gt s.pos₂) h hentry

/-- 非平凡共轭 ⟹ 态在块内非标量（共轭恒等必块内标量）。 -/
theorem nontrivial_imp_nonScalar (s : DiagState)
    (h : ∃ a : BlockMat,
      (s.unit : BlockMat) * a * ((s.unit⁻¹ : BlockMatˣ) : BlockMat) ≠ a) :
    s.d₁ ≠ s.d₂ := by
  intro heq
  obtain ⟨a, ha⟩ := h
  exact ha (s.conj_trivial heq a)

/-- 忠实性本身不决定时间：块标量忠实态（恒等）与非标量忠实态（非平凡）并存。 -/
theorem faithful_not_imp_nontrivial :
    (∃ s : DiagState, ∀ a : BlockMat,
      (s.unit : BlockMat) * a * ((s.unit⁻¹ : BlockMatˣ) : BlockMat) = a)
    ∧ (∃ s : DiagState, ∃ a : BlockMat,
      (s.unit : BlockMat) * a * ((s.unit⁻¹ : BlockMatˣ) : BlockMat) ≠ a) := by
  constructor
  · refine ⟨⟨1/2, 1/2, by norm_num, by norm_num⟩, ?_⟩
    intro a
    exact DiagState.conj_trivial ⟨1/2, 1/2, by norm_num, by norm_num⟩
      (show (1/2 : ℚ) = 1/2 from rfl) a
  · refine ⟨⟨2/3, 1/3, by norm_num, by norm_num⟩, ?_⟩
    exact DiagState.conj_nontrivial ⟨2/3, 1/3, by norm_num, by norm_num⟩ (by norm_num)

/-- 层权不同但块内标量仍恒等：两层块共轭逐块平凡（层权单独不构成时间）。 -/
theorem layerWeight_blockScalar_trivial (c₁ c₂ : ℚ) (h₁ : c₁ ≠ 0) (h₂ : c₂ ≠ 0)
    (a : TwoBlockAlg) :
    (((diagUnit c₁ c₁ h₁ h₁ : BlockMatˣ) : BlockMat) * a.1
        * (((diagUnit c₁ c₁ h₁ h₁)⁻¹ : BlockMatˣ) : BlockMat),
     ((diagUnit c₂ c₂ h₂ h₂ : BlockMatˣ) : BlockMat) * a.2
        * (((diagUnit c₂ c₂ h₂ h₂)⁻¹ : BlockMatˣ) : BlockMat)) = a := by
  refine Prod.ext ?_ ?_
  · exact conj_trivial_of_scalar (diagUnit c₁ c₁ h₁ h₁) c₁
      (diagMat_self_eq_algebraMap c₁) a.1
  · exact conj_trivial_of_scalar (diagUnit c₂ c₂ h₂ h₂) c₂
      (diagMat_self_eq_algebraMap c₂) a.2

end MUFPF.G3StateNecessity
