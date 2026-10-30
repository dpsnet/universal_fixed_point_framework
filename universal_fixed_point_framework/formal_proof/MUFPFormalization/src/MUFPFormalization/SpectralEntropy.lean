import Mathlib.Tactic
import Mathlib.Data.Fintype.Basic
import Mathlib.Analysis.Matrix.HermitianFunctionalCalculus
import MUFPFormalization.HolographicEntropyDegeneration

/-!
# 谱熵算符（S1 语义立项·阶段 1：对角密度矩阵版）

对应 `notes/04_lorentz_gravity/S1矩阵版熵算符.md`（2026-10-23，S3 立项后按建议次序推进 S1）。
候选签名：`spEntropy : SpObj → ℝ`（熵算符 on Sp 对象）。

本文件交付 **S1 阶段 1**：密度矩阵在本征基（对角）下的谱熵
`densityEntropy w = -Σ wᵢ·log(wᵢ)`（0·log0 分支显式处理，wᵢ=0 项贡献 0），
并把简并平权密度 ρ = (1/g)·I_g ⊕ 0 的熵桥接回**已机检权重熵** `entropyOfRange`：
- `densityEntropy`：对角密度权重版的谱熵（S=-(1/V)Tr(A ln A) 的有限维对角口径，
  Paper VII §5.1）；
- `densityEntropy_eq_entropyOfRange`：简并平权密度（前 g 个权重 = 1/g、其余 0）
  的谱熵 = 权重熵 entropyOfRange g（S1 ↔ 1a 对齐）；
- `spEntropy_eq_log_flat_degenerate`：S = ln g（简并基态谱熵，g 重简并最大混合态）；
- `area_eq_entropy_flat`：面积=熵组装句（d=4·ln g ⟹ A/4 = S，桥归约闭环）。

**阶段 2（登记，本文件不含）**：任意 Hermitian 密度矩阵 -Tr(A ln A)，
经 HermitianFunctionalCalculus（`hH.cfc (fun x => Real.log x)`，模板
BCSFermiEmergence.lean 的 cfc 用法）+ 谱定理归约——完整 spEntropy : SpObj → ℝ
待阶段 2；本文件的对角口径在物理上是本征基表述，与 2 在谱分解下等价（登记未证）。

零 sorry 政策：本文件不含 sorry。
-/

namespace MUFPF.SpectralEntropy

/-- 谱熵（对角密度矩阵版）：S = -Σᵢ wᵢ·log(wᵢ)，wᵢ=0 项显式贡献 0
    （0·log0 = 0 的有限维处理；Paper VII §5.1 口径）。 -/
noncomputable def densityEntropy {n : ℕ} (w : Fin n → ℝ) : ℝ :=
  - (Finset.univ.sum (fun i : Fin n => if w i = 0 then 0 else w i * Real.log (w i)))

/-- 计数引理：Fin n 中值 < g 的元素个数 = g（g ≤ n）。 -/
theorem card_lt_filter (n g : ℕ) (hg : g ≤ n) :
    (Finset.univ.filter (fun i : Fin n => i.1 < g)).card = g := by
  let f : Fin g → Fin n := fun j => ⟨j.1, lt_of_lt_of_le j.2 hg⟩
  have hinj : Function.Injective f := by
    intro a b hab
    apply Fin.ext
    simpa [f] using congrArg Fin.val hab
  have himage : Finset.univ.image f = Finset.univ.filter (fun i : Fin n => i.1 < g) := by
    ext i
    constructor
    · intro hmem
      rw [Finset.mem_image] at hmem
      rcases hmem with ⟨j, _hj, hf⟩
      simp [f, ← hf, j.2]
    · intro hi
      rw [Finset.mem_filter] at hi
      rcases hi with ⟨_, hi⟩
      let j : Fin g := ⟨i.1, hi⟩
      exact Finset.mem_image.mpr ⟨j, by simp, by simp [f, j]⟩
  rw [← himage]
  rw [Finset.card_image_of_injective _ hinj]
  simp

/-- S1 ↔ 1a 对齐：简并平权密度（前 g 个权重 = 1/g、其余 0）的谱熵 = 权重熵 entropyOfRange g。 -/
theorem densityEntropy_eq_entropyOfRange {n g : ℕ} (hg : 0 < g) (hle : g ≤ n)
    (w : Fin n → ℝ) (hw : ∀ i : Fin n, w i = if i.1 < g then (1 : ℝ) / (g : ℝ) else 0) :
    densityEntropy w = MUFPF.HolographicEntropy.entropyOfRange g := by
  let c : ℝ := (1 : ℝ) / (g : ℝ) * Real.log ((1 : ℝ) / (g : ℝ))
  have hterm : ∀ i : Fin n, (if w i = 0 then 0 else w i * Real.log (w i)) =
      if i.1 < g then c else 0 := by
    intro i
    by_cases hi : i.1 < g
    · have hgR : (g : ℝ) ≠ 0 := by exact_mod_cast (ne_of_gt hg)
      have hwi : w i = (1 : ℝ) / (g : ℝ) := by simp [hw i, hi]
      simp [hwi, hi, hgR, c]
    · have hwi0 : w i = 0 := by simp [hw i, hi]
      simp [hwi0, hi]
  unfold densityEntropy MUFPF.HolographicEntropy.entropyOfRange
  have hleft : (Finset.univ.sum (fun i : Fin n => if w i = 0 then 0 else w i * Real.log (w i)))
      = (g : ℝ) * c := by
    calc
      (Finset.univ.sum (fun i : Fin n => if w i = 0 then 0 else w i * Real.log (w i)))
          = Finset.univ.sum (fun i : Fin n => if i.1 < g then c else 0) := by
              apply Finset.sum_congr rfl
              intro i _hi
              exact hterm i
      _ = (Finset.univ.filter (fun i : Fin n => i.1 < g)).sum (fun _ : Fin n => c) := by
              rw [← Finset.sum_filter]
      _ = (g : ℝ) * c := by
              rw [Finset.sum_const]
              rw [nsmul_eq_mul]
              rw [card_lt_filter n g hle]
  have hright : (Finset.range g).sum (fun _ : ℕ => c) = (g : ℝ) * c := by
    rw [Finset.sum_const]
    rw [Finset.card_range]
    rw [nsmul_eq_mul]
  rw [hleft, hright]

/-- 简并基态谱熵：ρ = (1/g)·I_g ⊕ 0 的谱熵 = ln g（0 < g，g ≤ n）。 -/
theorem spEntropy_eq_log_flat_degenerate {n g : ℕ} (hg : 0 < g) (hle : g ≤ n)
    (w : Fin n → ℝ) (hw : ∀ i : Fin n, w i = if i.1 < g then (1 : ℝ) / (g : ℝ) else 0) :
    densityEntropy w = Real.log (g : ℝ) := by
  rw [densityEntropy_eq_entropyOfRange hg hle w hw]
  exact MUFPF.HolographicEntropy.uniform_entropy_eq_log_g g hg

/-- 面积=熵组装句（S1 侧闭环）：d = 4·ln g 且密度为 g 重简并平权时，A/4 = S
    （codim=2、M_Pl=1；桥归约 AdjunctionHolographicBridge 的熵侧落地）。 -/
theorem area_eq_entropy_flat {n g : ℕ} {d : ℝ} (hg : 0 < g) (hle : g ≤ n)
    (w : Fin n → ℝ) (hw : ∀ i : Fin n, w i = if i.1 < g then (1 : ℝ) / (g : ℝ) else 0)
    (hd : d = 4 * Real.log (g : ℝ)) :
    d / 4 = densityEntropy w := by
  rw [hd]
  rw [spEntropy_eq_log_flat_degenerate hg hle w hw]
  norm_num

/-! ## S1 阶段 2：任意 Hermitian 密度矩阵谱熵（-Tr(A ln A)，特征值口径，2026-10-24）

阶段 1 只做对角口径；阶段 2 用 `hA.eigenvalues`（谱定理特征值）定义任意 Hermitian 的谱熵：
S = -Σᵢ λᵢ·log(λᵢ) = -Tr(A ln A)（A 为密度矩阵时 λᵢ ∈ [0,1]）。
本文件固化：
- `matrixSpectralEntropy`：特征值口径定义（cfc 形态 -Tr(A ln A) 经谱定理与此一致，登记）；
- ★ `spectralEntropy_nonneg_of_density`：密度矩阵（0 ≤ λ ≤ 1）⟹ 谱熵 ≥ 0
  （对应 2310/2311 相对熵正性与 `relEntropyDisc_nonneg` 同族的熵非负性判据）。
- 开放证明目标（登记，本文件不含）：`spectralEntropy_diagonal_eq_densityEntropy`——
  对角 Hermitian 的矩阵谱熵 = 对角口径 densityEntropy（需特征值 multiset = 对角元
  multiset 的排序无关重排引理，mathlib 无现成；阶段 2 完成度以本节为准）。
-/

/-- 谱熵（任意 Hermitian，特征值口径）：S = -Σᵢ λᵢ·log(λᵢ)（-Tr(A ln A) 的谱形态；
    A 为密度矩阵时 λᵢ ∈ [0,1]，0·log0 项由 log 全函数约定 = 0）。 -/
noncomputable def matrixSpectralEntropy {n : ℕ} (A : Matrix (Fin n) (Fin n) ℂ)
    (hA : A.IsHermitian) : ℝ :=
  - (Finset.univ.sum (fun i : Fin n => hA.eigenvalues i * Real.log (hA.eigenvalues i)))

/-- ★ 密度矩阵谱熵非负：任意 Hermitian 密度矩阵（特征值 λᵢ ∈ [0,1]）⟹ S ≥ 0
    （-Tr(A ln A) ≥ 0；对应相对熵正性判据族）。 -/
theorem spectralEntropy_nonneg_of_density {n : ℕ} (A : Matrix (Fin n) (Fin n) ℂ)
    (hA : A.IsHermitian) (hl0 : ∀ i : Fin n, 0 ≤ hA.eigenvalues i)
    (hl1 : ∀ i : Fin n, hA.eigenvalues i ≤ 1) :
    0 ≤ matrixSpectralEntropy A hA := by
  unfold matrixSpectralEntropy
  rw [neg_nonneg]
  apply Finset.sum_nonpos
  intro i hi
  have hlog_le : Real.log (hA.eigenvalues i) ≤ 0 :=
    Real.log_nonpos (hl0 i) (hl1 i)
  exact mul_nonpos_of_nonneg_of_nonpos (hl0 i) hlog_le

end MUFPF.SpectralEntropy
