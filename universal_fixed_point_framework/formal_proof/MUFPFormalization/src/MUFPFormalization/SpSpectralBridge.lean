-- ============================================================
-- 谱定理桥：自伴 ⇒ 可酉对角化（D35）
-- ============================================================
-- 补上 D31/D34 登记的那一环：`IsHermitian ⇒ 可酉对角化`。
-- 该环由 Mathlib 的矩阵谱定理提供（`Matrix.IsHermitian.spectral_theorem`，
-- `Mathlib/Analysis/Matrix/Spectrum.lean` L143），本模块只做接口：
--   * 把本库的 `MUFPF.IsHermitian`（`E.A = conjTranspose E.A`）
--     与 Mathlib 的 `Matrix.IsHermitian`（`conjTranspose A = A`）对齐；
--   * 把 `spectral_theorem` 的 `conjStarAlgAut` 形式展开成显式的
--     `A = U * diagonal d * star U`（`U` 酉）。
-- ============================================================

import Mathlib.Analysis.Matrix.Spectrum
import Mathlib.Algebra.Star.UnitaryStarAlgAut
import MUFPFormalization.SpCategory
import MUFPFormalization.SpLayerSeparability

namespace MUFPF

open Matrix

/-- 本库的自伴谓词与 Mathlib 的 `Matrix.IsHermitian` 是同一件事（等号方向相反）。 -/
theorem isHermitian_iff_matrixIsHermitian (E : SpObj) :
    IsHermitian E ↔ Matrix.IsHermitian E.A := by
  unfold IsHermitian Matrix.IsHermitian
  exact ⟨Eq.symm, Eq.symm⟩

/-- **自伴 ⇒ 可酉对角化**（Mathlib 矩阵谱定理的显式形式）：
    存在酉矩阵 `U` 与实对角向量 `d`，使 `A = U * diagonal d * star U`。
    等价写法：`A` 与实对角矩阵酉相似。 -/
theorem hermitian_unitary_diagonalizable {n : ℕ} {A : Matrix (Fin n) (Fin n) ℂ}
    (hA : Matrix.IsHermitian A) :
    ∃ (U : Matrix.unitaryGroup (Fin n) ℂ) (d : Fin n → ℝ),
      A = (U : Matrix (Fin n) (Fin n) ℂ) *
            Matrix.diagonal (fun i => (d i : ℂ)) *
            star (U : Matrix (Fin n) (Fin n) ℂ) := by
  refine ⟨hA.eigenvectorUnitary, hA.eigenvalues, ?_⟩
  have h1 := hA.spectral_theorem
  simpa [Function.comp_def] using h1

/-- `SpObj` 版本：自伴的 `Sp` 对象可酉对角化。 -/
theorem spObj_hermitian_unitary_diagonalizable (E : SpObj) (h : IsHermitian E) :
    ∃ (U : Matrix.unitaryGroup (Fin E.n) ℂ) (d : Fin E.n → ℝ),
      E.A = (U : Matrix (Fin E.n) (Fin E.n) ℂ) *
             Matrix.diagonal (fun i => (d i : ℂ)) *
             star (U : Matrix (Fin E.n) (Fin E.n) ℂ) :=
  hermitian_unitary_diagonalizable ((isHermitian_iff_matrixIsHermitian E).mp h)

end MUFPF

namespace MUFPFormalization

open Matrix

/-! ### 第二环：可酉对角化 ⇒ `ker ∩ im = 0` ⇒ `dev ≡ 0`

分三步：
1. 对角相（任意 `d`，**不要求谱互异**）：`ad_D(X)_ij = (d_i − d_j) · X_ij`
   ⇒ `X ∈ ker` 在 `d_i ≠ d_j` 处置零、`X ∈ im` 在 `d_i = d_j` 处置零，
   两半合起来覆盖所有 `(i,j)` ⇒ 交为零。
2. 酉共轭传输：`star U · ad_{U D Uᴴ}(X) · U = ad_D(star U · X · U)`，
   故 `ker`/`im` 在共轭下互相映射，交为零的性质不变。
3. 自伴 + 谱定理（第一环）⇒ 结论。 -/

/-- `adLin` 的应用式（定义投影）。 -/
lemma adLin_apply {n : ℕ} (A X : Matrix (Fin n) (Fin n) ℂ) :
    adLin A X = A * X - X * A := rfl

/-- 对角矩阵左乘的元素式：`(diag d * X) i j = d i * X i j`。 -/
lemma diagonal_mul_apply {n : ℕ} (d : Fin n → ℂ) (X : Matrix (Fin n) (Fin n) ℂ) (i j : Fin n) :
    (Matrix.diagonal d * X) i j = d i * X i j := by
  simp [Matrix.mul_apply, Matrix.diagonal, Matrix.of_apply, ite_mul, zero_mul]

/-- 对角矩阵右乘的元素式：`(X * diag d) i j = X i j * d j`。 -/
lemma mul_diagonal_apply {n : ℕ} (d : Fin n → ℂ) (X : Matrix (Fin n) (Fin n) ℂ) (i j : Fin n) :
    (X * Matrix.diagonal d) i j = X i j * d j := by
  simp [Matrix.mul_apply, Matrix.diagonal, Matrix.of_apply]

/-- 对角相交换子的元素式：`ad_D(X)_ij = (d_i − d_j) · X_ij`。 -/
lemma adLin_diagonal_apply {n : ℕ} (d : Fin n → ℂ) (X : Matrix (Fin n) (Fin n) ℂ)
    (i j : Fin n) :
    adLin (Matrix.diagonal d) X i j = (d i - d j) * X i j := by
  rw [adLin_apply, Matrix.sub_apply, diagonal_mul_apply, mul_diagonal_apply]
  ring

/-- **对角相零交定理**：对任意对角矩阵（**不要求谱互异**、不要求实），
    `ker(ad_D) ⊓ im(ad_D) = ⊥`。
    证明只用元素式：`d_i = d_j` 处由 `im` 得零（`(d_i − d_j)` 因子），
    `d_i ≠ d_j` 处由 `ker` 得零。两条正好互补覆盖。 -/
theorem diagonal_adLin_ker_inf_range_eq_bot {n : ℕ} (d : Fin n → ℂ) :
    LinearMap.ker (adLin (Matrix.diagonal d)) ⊓
      LinearMap.range (adLin (Matrix.diagonal d)) = ⊥ := by
  rw [Submodule.eq_bot_iff]
  intro X hX
  rw [Submodule.mem_inf, LinearMap.mem_ker, LinearMap.mem_range] at hX
  obtain ⟨hker, Z, hZ⟩ := hX
  ext i j
  by_cases h : d i = d j
  · have hXij : X i j = (d i - d j) * Z i j := by
      rw [← hZ, adLin_diagonal_apply]
    rw [hXij, h]
    simp
  · have h0 : adLin (Matrix.diagonal d) X i j = 0 := by rw [hker]; rfl
    rw [adLin_diagonal_apply] at h0
    exact (mul_eq_zero.mp h0).resolve_left (sub_ne_zero.mpr h)

/-- **酉共轭传输**：`star U · ad_{UDUᴴ}(X) · U = ad_D(star U · X · U)`。
    这是把 `ker`/`im` 从 `D` 相搬回 `A` 相的唯一桥梁。 -/
theorem adLin_conj_apply {n : ℕ} (U D X : Matrix (Fin n) (Fin n) ℂ)
    (hU : star U * U = 1) :
    star U * adLin (U * D * star U) X * U = adLin D (star U * X * U) := by
  simp only [adLin_apply, Matrix.mul_sub, Matrix.sub_mul]
  congr 1
  · calc star U * (U * D * star U * X) * U
        = (star U * U) * D * (star U * X * U) := by noncomm_ring
      _ = D * (star U * X * U) := by rw [hU, one_mul]
  · calc star U * (X * (U * D * star U)) * U
        = (star U * X * U) * D * (star U * U) := by noncomm_ring
      _ = (star U * X * U) * D := by rw [hU, mul_one]

/-- **可酉对角化 ⇒ 零交**：若 `A` 酉相似于对角矩阵，则 `ker(ad_A) ⊓ im(ad_A) = ⊥`。 -/
theorem unitary_diagonalizable_adLin_ker_inf_range_eq_bot {n : ℕ}
    (U : Matrix (Fin n) (Fin n) ℂ) (d : Fin n → ℂ)
    (hU : star U * U = 1) (hU' : U * star U = 1) :
    LinearMap.ker (adLin (U * Matrix.diagonal d * star U)) ⊓
      LinearMap.range (adLin (U * Matrix.diagonal d * star U)) = ⊥ := by
  rw [Submodule.eq_bot_iff]
  intro x hx
  rw [Submodule.mem_inf, LinearMap.mem_ker, LinearMap.mem_range] at hx
  obtain ⟨hker, z, hz⟩ := hx
  have hker' : star U * x * U ∈ LinearMap.ker (adLin (Matrix.diagonal d)) := by
    rw [LinearMap.mem_ker, ← adLin_conj_apply U (Matrix.diagonal d) x hU, hker]
    simp
  have him' : star U * x * U ∈ LinearMap.range (adLin (Matrix.diagonal d)) := by
    rw [LinearMap.mem_range]
    refine ⟨star U * z * U, ?_⟩
    rw [← adLin_conj_apply U (Matrix.diagonal d) z hU, hz]
  have hmem : star U * x * U ∈
      LinearMap.ker (adLin (Matrix.diagonal d)) ⊓
        LinearMap.range (adLin (Matrix.diagonal d)) :=
    Submodule.mem_inf.mpr ⟨hker', him'⟩
  rw [diagonal_adLin_ker_inf_range_eq_bot, Submodule.mem_bot] at hmem
  have hrec : x = U * (star U * x * U) * star U := by
    have h1 : U * (star U * x * U) * star U = (U * star U) * x * (U * star U) := by
      noncomm_ring
    rw [h1, hU', one_mul, mul_one]
  rw [hrec, hmem, Matrix.mul_zero, Matrix.zero_mul]

/-- **自伴 ⇒ 零交**：自伴矩阵的 `ker(ad_A) ⊓ im(ad_A) = ⊥`。
    链路：自伴 ⇒ 可酉对角化（第一环，谱定理）⇒ 对角相零交 ⇒ 酉共轭传输回来。 -/
theorem hermitian_adLin_ker_inf_range_eq_bot {n : ℕ} {A : Matrix (Fin n) (Fin n) ℂ}
    (hA : Matrix.IsHermitian A) :
    LinearMap.ker (adLin A) ⊓ LinearMap.range (adLin A) = ⊥ := by
  obtain ⟨U, d, hU⟩ := MUFPF.hermitian_unitary_diagonalizable hA
  have hstar : star (U : Matrix (Fin n) (Fin n) ℂ) * (U : Matrix (Fin n) (Fin n) ℂ) = 1 :=
    Unitary.coe_star_mul_self U
  have hmul : (U : Matrix (Fin n) (Fin n) ℂ) * star (U : Matrix (Fin n) (Fin n) ℂ) = 1 :=
    Unitary.coe_mul_star_self U
  rw [hU]
  exact unitary_diagonalizable_adLin_ker_inf_range_eq_bot
    (U : Matrix (Fin n) (Fin n) ℂ) (fun i => (d i : ℂ)) hstar hmul

/-- **自伴层内 `dev ≡ 0`**（一般形式，取代 D34 只对 `diag3` 的元素级版本）：
    对任意自伴矩阵，任何落在 `ker ∩ im` 的 `dev` 必为 `0`。 -/
theorem hermitian_dev_eq_zero {n : ℕ} {A dev : Matrix (Fin n) (Fin n) ℂ}
    (hA : Matrix.IsHermitian A)
    (hker : dev ∈ LinearMap.ker (adLin A))
    (him : dev ∈ LinearMap.range (adLin A)) : dev = 0 := by
  have h := hermitian_adLin_ker_inf_range_eq_bot hA
  have hmem : dev ∈ LinearMap.ker (adLin A) ⊓ LinearMap.range (adLin A) :=
    Submodule.mem_inf.mpr ⟨hker, him⟩
  rw [h, Submodule.mem_bot] at hmem
  exact hmem

/-- `SpObj` 版本：自伴 `Sp` 对象的偏差必为零。 -/
theorem spObj_hermitian_dev_eq_zero (E : MUFPF.SpObj) (h : MUFPF.IsHermitian E)
    (dev : Matrix (Fin E.n) (Fin E.n) ℂ)
    (hker : dev ∈ LinearMap.ker (adLin E.A))
    (him : dev ∈ LinearMap.range (adLin E.A)) : dev = 0 :=
  hermitian_dev_eq_zero ((MUFPF.isHermitian_iff_matrixIsHermitian E).mp h) hker him

end MUFPFormalization
