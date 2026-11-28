/-
  QuantizationResidueAudit.lean — R-u：量化的残余结构（两条判据互不蕴含 + 手性轨道分解）
  =====================================================================================

## 问题

§31（R-o）在用户**接受「保长度」**之后加了第二条结构要求 `B⁴ = 1`，判出
`B ∈ {1, −1, A, −A}`（`A = rotGen`）、残余「一个比特」。§32–§34（R-p/q/r）接着把
这一个比特追到「标号约定」。本批回头查两个**当时只写在散文里、未机检**的点：

- **判①**：`B⁴ = 1` 是否由「保长度」蕴含？若蕴含，它就不是独立要求，§31 的第二条公设可撤。
  答案：**不蕴含**。取 `α = δ = √2/2`（`θ = π/4`），保长度成立而 `B⁴ = −1`。
- **判②**：`F`-共轭手性分级在 §31 的四个值上如何作用？
  答案：四值分成两个二元轨道 `{1, −1}` 与 `{A, −A}`；`F` 固定标量轨道、翻转旋转轨道。
  故「朝向比特」只在旋转轨道上有意义，§33–§34 的赋号结论**以排除 `±1` 为前提**。

## 净结果

1. 「保长度」给出连续统（1 个角），`B⁴ = 1` 把它切到 4 点——**第二条要求是真独立**，
   机检有严格见证，§31 的公设地位不受影响。
2. 四值上 `F` 的轨道结构：`F·1·F = 1`、`F·(−1)·F = −1`（标量轨道：手性平凡）、
   `F·A·F = −A`、`F·(−A)·F = A`（旋转轨道：手性翻转）。四个值两两不同。
3. 于是「一个比特」这个计数**依赖一条额外声明**：`±1` 是「无耦合」（`δ = 0`，层间不交换）。
   若把 `±1` 也算耦合，残余是 2 个 `ℤ/2` 位（族位 + 符号位），而族位**没有手性判据可用**。

## 诚实边界

1. 判①只证「不蕴含」（存在见证），**不**证「保长度 ∧ ¬量化 的集合是连续统」——
   后者由 §30 的「1 个自由角」定性给出，本批不重做参数化。
2. 判②只说轨道结构，**不**把 `±1` 的物理读法（无耦合 / 反耦合）定死；那是指认问题。
3. 本批不引入新数、新对象、新公设；`√2/2` 只是**见证用的实数**，不作框架常数。
-/

import MUFPFormalization.QuarterTurnQuantizationAudit
import MUFPFormalization.ChiralityGradingAudit
import Mathlib.Tactic

namespace MUFPF.QuantizationResidueAudit

open MUFPF.IntertwinerRepairAudit (rotGen)
open MUFPF.DeltaInvarianceAudit (alp dlt)
open MUFPF.Isotropy (F)
open MUFPF.QuarterTurnQuantizationAudit (rot_combo_four)
open MUFPF.ChiralityGradingAudit (conj_fixes_identity conj_flips_rotGen)

/-- 见证用的实数 `√2/2`（只作反例见证，**不是**框架常数）。 -/
noncomputable def halfRootTwo : ℝ := Real.sqrt 2 / 2

/-- `(√2/2)² = 1/2`。 -/
theorem sq_halfRootTwo : halfRootTwo * halfRootTwo = 1 / 2 := by
  unfold halfRootTwo
  have h : Real.sqrt 2 * Real.sqrt 2 = 2 := Real.mul_self_sqrt (by norm_num)
  rw [div_mul_div_comm, h]
  norm_num

/-- ★ 旋转型的 Gram 矩阵：`(x·1 + y·A)ᵀ(x·1 + y·A) = (x²+y²)·1`。 -/
theorem gram_rotForm (x y : ℝ) :
    (x • (1 : Matrix (Fin 2) (Fin 2) ℝ) + y • rotGen).transpose *
        (x • (1 : Matrix (Fin 2) (Fin 2) ℝ) + y • rotGen)
      = (x * x + y * y) • (1 : Matrix (Fin 2) (Fin 2) ℝ) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [rotGen, Matrix.mul_apply, Fin.sum_univ_two, Matrix.transpose_apply,
      Matrix.add_apply, Matrix.smul_apply, Matrix.one_apply]
  all_goals ring

/-- ★ 旋转型的行列式：`det (x·1 + y·A) = x² + y²`。 -/
theorem det_rotForm (x y : ℝ) :
    Matrix.det (x • (1 : Matrix (Fin 2) (Fin 2) ℝ) + y • rotGen) = x * x + y * y := by
  rw [Matrix.det_fin_two]
  simp [rotGen, Matrix.add_apply, Matrix.smul_apply]

/-- 见证矩阵：`α = δ = √2/2`，即 `θ = π/4`。 -/
noncomputable def witnessB : Matrix (Fin 2) (Fin 2) ℝ :=
    halfRootTwo • (1 : Matrix (Fin 2) (Fin 2) ℝ) + halfRootTwo • rotGen

/-- ★★ **判①-a：见证矩阵是保长度的**（`BᵀB = 1 ∧ det B = 1`）。 -/
theorem witness_isometry :
    witnessB.transpose * witnessB = (1 : Matrix (Fin 2) (Fin 2) ℝ) ∧
      Matrix.det witnessB = 1 := by
  have hs : halfRootTwo * halfRootTwo = 1 / 2 := sq_halfRootTwo
  have hsum : halfRootTwo * halfRootTwo + halfRootTwo * halfRootTwo = 1 := by linarith
  constructor
  · unfold witnessB
    rw [gram_rotForm, hsum, one_smul]
  · unfold witnessB
    rw [det_rotForm, hsum]

/-- ★★ **判①-b：见证矩阵的四次幂是 `−1`**（`θ = π/4` ⟹ `B⁴ = −1`）。 -/
theorem witness_fourth :
    witnessB ^ 4 = -(1 : Matrix (Fin 2) (Fin 2) ℝ) := by
  have hs : halfRootTwo * halfRootTwo = 1 / 2 := sq_halfRootTwo
  have hzero : halfRootTwo * halfRootTwo - halfRootTwo * halfRootTwo = 0 := by ring
  have htwice : 2 * (halfRootTwo * halfRootTwo) = 1 := by linarith [hs]
  unfold witnessB
  rw [rot_combo_four]
  simp only [hzero, htwice]
  simp

/-- ★★ **判①-c（判决）：`B⁴ = 1` 不由「保长度」蕴含**。 -/
theorem length_does_not_imply_quantization :
    witnessB.transpose * witnessB = (1 : Matrix (Fin 2) (Fin 2) ℝ) ∧
      Matrix.det witnessB = 1 ∧ witnessB ^ 4 ≠ (1 : Matrix (Fin 2) (Fin 2) ℝ) := by
  obtain ⟨hg, hd⟩ := witness_isometry
  refine ⟨hg, hd, ?_⟩
  intro h
  have hw : witnessB ^ 4 = -(1 : Matrix (Fin 2) (Fin 2) ℝ) := witness_fourth
  rw [hw] at h
  have h00 := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 0 0) h
  simp [Matrix.neg_apply] at h00
  norm_num at h00

/-- 判①的「存在」形态：保长度严格弱于量化。 -/
theorem exists_isometry_not_quantized :
    ∃ B : Matrix (Fin 2) (Fin 2) ℝ,
      B.transpose * B = 1 ∧ Matrix.det B = 1 ∧ B ^ 4 ≠ 1 :=
  ⟨witnessB, length_does_not_imply_quantization.1,
    length_does_not_imply_quantization.2.1, length_does_not_imply_quantization.2.2⟩

/-- ★ **判②-a：`F` 固定标量轨道**（`F·1·F = 1`、`F·(−1)·F = −1`）。 -/
theorem chirality_fixes_scalar_orbit :
    F * (1 : Matrix (Fin 2) (Fin 2) ℝ) * F = 1 ∧
      F * (-(1 : Matrix (Fin 2) (Fin 2) ℝ)) * F = -1 := by
  have h1 : F * (1 : Matrix (Fin 2) (Fin 2) ℝ) * F = 1 := conj_fixes_identity
  refine ⟨h1, ?_⟩
  have hneg : F * (-(1 : Matrix (Fin 2) (Fin 2) ℝ)) * F
      = -(F * (1 : Matrix (Fin 2) (Fin 2) ℝ) * F) := by
    rw [Matrix.mul_neg, Matrix.neg_mul]
  rw [hneg, h1]

/-- ★ **判②-b：`F` 翻转旋转轨道**（`F·A·F = −A`、`F·(−A)·F = A`）。 -/
theorem chirality_flips_rot_orbit :
    F * rotGen * F = -rotGen ∧ F * (-rotGen) * F = rotGen := by
  have hA : F * rotGen * F = -rotGen := conj_flips_rotGen
  refine ⟨hA, ?_⟩
  have hneg : F * (-rotGen) * F = -(F * rotGen * F) := by
    rw [Matrix.mul_neg, Matrix.neg_mul]
  rw [hneg, hA]
  simp

/-- ★★ **判②-c：四值上 `F` 的轨道分解**——两个二元轨道，标量轨道手性平凡、
    旋转轨道手性翻转。 -/
theorem chirality_two_orbits :
    (F * (1 : Matrix (Fin 2) (Fin 2) ℝ) * F = 1 ∧
        F * (-(1 : Matrix (Fin 2) (Fin 2) ℝ)) * F = -1) ∧
      (F * rotGen * F = -rotGen ∧ F * (-rotGen) * F = rotGen) :=
  ⟨chirality_fixes_scalar_orbit, chirality_flips_rot_orbit⟩

/-- ★ 四个值两两不同（「一个比特」的计数前提）。 -/
theorem four_values_pairwise_distinct :
    (1 : Matrix (Fin 2) (Fin 2) ℝ) ≠ -1 ∧
      (1 : Matrix (Fin 2) (Fin 2) ℝ) ≠ rotGen ∧
      (1 : Matrix (Fin 2) (Fin 2) ℝ) ≠ -rotGen ∧
      (-(1 : Matrix (Fin 2) (Fin 2) ℝ)) ≠ rotGen ∧
      (-(1 : Matrix (Fin 2) (Fin 2) ℝ)) ≠ -rotGen ∧
      rotGen ≠ -rotGen := by
  have hOne00 : (1 : Matrix (Fin 2) (Fin 2) ℝ) 0 0 = 1 := by simp
  have hNeg00 : (-(1 : Matrix (Fin 2) (Fin 2) ℝ)) 0 0 = -1 := by simp
  have hR00 : rotGen 0 0 = 0 := by simp [rotGen]
  have hNR00 : (-rotGen) 0 0 = 0 := by simp [rotGen]
  have hR01 : rotGen 0 1 = 1 := by simp [rotGen]
  have hNR01 : (-rotGen) 0 1 = -1 := by simp [rotGen]
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro h
    rw [h] at hOne00
    rw [hNeg00] at hOne00
    norm_num at hOne00
  · intro h
    rw [h] at hOne00
    rw [hR00] at hOne00
    norm_num at hOne00
  · intro h
    rw [h] at hOne00
    rw [hNR00] at hOne00
    norm_num at hOne00
  · intro h
    rw [h] at hNeg00
    rw [hR00] at hNeg00
    norm_num at hNeg00
  · intro h
    rw [h] at hNeg00
    rw [hNR00] at hNeg00
    norm_num at hNeg00
  · intro h
    rw [h] at hR01
    rw [hNR01] at hR01
    norm_num at hR01

/-- **R-u 判决汇总**：
    ① `BᵀB = 1 ∧ det B = 1 ∧ B⁴ ≠ 1` 有见证 ⟹ 量化是**真独立**的第二条要求；
    ② `F` 把四值分成两轨道（标量轨道手性平凡、旋转轨道手性翻转）；
    ③ 四值两两不同 ⟹ §31 的「一个比特」以「`±1` 即无耦合」这条额外声明为前提。 -/
theorem quantization_residue_verdict :
    (∃ B : Matrix (Fin 2) (Fin 2) ℝ,
        B.transpose * B = 1 ∧ Matrix.det B = 1 ∧ B ^ 4 ≠ 1) ∧
      ((F * (1 : Matrix (Fin 2) (Fin 2) ℝ) * F = 1 ∧
          F * (-(1 : Matrix (Fin 2) (Fin 2) ℝ)) * F = -1) ∧
        (F * rotGen * F = -rotGen ∧ F * (-rotGen) * F = rotGen)) ∧
      ((1 : Matrix (Fin 2) (Fin 2) ℝ) ≠ -1 ∧
        (1 : Matrix (Fin 2) (Fin 2) ℝ) ≠ rotGen ∧
        (1 : Matrix (Fin 2) (Fin 2) ℝ) ≠ -rotGen ∧
        (-(1 : Matrix (Fin 2) (Fin 2) ℝ)) ≠ rotGen ∧
        (-(1 : Matrix (Fin 2) (Fin 2) ℝ)) ≠ -rotGen ∧
        rotGen ≠ -rotGen) :=
  ⟨exists_isometry_not_quantized, chirality_two_orbits, four_values_pairwise_distinct⟩

end MUFPF.QuantizationResidueAudit
