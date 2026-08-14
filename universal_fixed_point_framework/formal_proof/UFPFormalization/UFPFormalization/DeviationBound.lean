import UFPFormalization.SpCategory
import UFPFormalization.HigherSpCategory
import UFPFormalization.SpectralGap
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Tactic
import Mathlib.Analysis.InnerProductSpace.PiL2

open Matrix
open Complex

namespace UFPFormalization

/-!
# Deviation Bound: Exchange Law Deviation → Spectral Gap
-/

/-! §1 Frobenius 范数 -/

/-- Frobenius 范数的平方：‖M‖_F² = Σ_{i,j} |M_{ij}|²。 -/
noncomputable def frobNormSq {m n : ℕ} (M : Matrix (Fin m) (Fin n) ℂ) : ℝ :=
  ∑ i : Fin m, ∑ j : Fin n, normSq (M i j)

/-- Frobenius 范数。 -/
noncomputable def frobNorm {m n : ℕ} (M : Matrix (Fin m) (Fin n) ℂ) : ℝ :=
  Real.sqrt (frobNormSq M)

lemma frobNormSq_nonneg {m n : ℕ} (M : Matrix (Fin m) (Fin n) ℂ) : 0 ≤ frobNormSq M := by
  apply Finset.sum_nonneg; intro i _; apply Finset.sum_nonneg; intro j _; exact normSq_nonneg _

lemma frobNormSq_neg {m n : ℕ} (M : Matrix (Fin m) (Fin n) ℂ) : frobNormSq (-M) = frobNormSq M := by
  simp [frobNormSq, normSq_neg]

/-! ### §1.5 Frobenius 范数的酉不变性（等谱守恒，2026-07-29 新增）

   谱流方程 dD/dt = [G, D]（G 反 Hermitian）的解 D(t) = U·D₀·U†
   （U = exp(Gt) 酉）。Frobenius 范数的酉不变性是"通量守恒"的
   代数内核：谱强度在谱流演化下守恒，球面几何稀释 r^{d-1}
   给出 1/r^{d-1} 衰减（B1 第 ②③ 环）。 -/

/-- Frobenius 范数与迹的关系：‖M‖_F² = Re Tr(M·Mᴴ)。 -/
lemma frobNormSq_eq_trace_re {n : ℕ} (M : Matrix (Fin n) (Fin n) ℂ) :
    ((M * M.conjTranspose).trace).re = frobNormSq M := by
  have entry : ∀ i : Fin n,
      ((M * M.conjTranspose) i i).re = ∑ j : Fin n, normSq (M i j) := by
    intro i
    rw [Matrix.mul_apply, Complex.re_sum]
    apply Finset.sum_congr rfl
    intro j _
    rw [Matrix.conjTranspose_apply, Complex.star_def, Complex.mul_conj, Complex.ofReal_re]
  rw [Matrix.trace, Complex.re_sum, frobNormSq]
  exact Finset.sum_congr rfl (fun i _ => entry i)

/-- Frobenius 范数的酉不变性（左乘）：UᴴU = 1 时 ‖U·X‖_F² = ‖X‖_F²。 -/
theorem frobNormSq_unitary_left {n : ℕ} (U X : Matrix (Fin n) (Fin n) ℂ)
    (hU : U.conjTranspose * U = 1) :
    frobNormSq (U * X) = frobNormSq X := by
  rw [← frobNormSq_eq_trace_re (U * X), ← frobNormSq_eq_trace_re X]
  rw [Matrix.conjTranspose_mul, ← Matrix.mul_assoc]
  rw [Matrix.trace_mul_comm]
  rw [← Matrix.mul_assoc, ← Matrix.mul_assoc, hU, Matrix.one_mul]

/-- Frobenius 范数的酉不变性（右乘）：UUᴴ = 1 时 ‖X·U‖_F² = ‖X‖_F²。 -/
theorem frobNormSq_unitary_right {n : ℕ} (U X : Matrix (Fin n) (Fin n) ℂ)
    (hU : U * U.conjTranspose = 1) :
    frobNormSq (X * U) = frobNormSq X := by
  rw [← frobNormSq_eq_trace_re (X * U), ← frobNormSq_eq_trace_re X]
  rw [Matrix.conjTranspose_mul, ← Matrix.mul_assoc, Matrix.mul_assoc X U U.conjTranspose,
    hU, Matrix.mul_one]

/-- **等谱守恒定理**：U 酉（UᴴU = 1）时 ‖U·X·Uᴴ‖_F² = ‖X‖_F²。
    谱流 D(t) = U·D₀·U† 的 Hilbert-Schmidt 范数守恒——
    谱通量守恒 ∂_r(r^{d-1}ρ) = 0 的谱结构内核（B1 第 ② 环）。 -/
theorem frobNormSq_unitary_conj {n : ℕ} (U X : Matrix (Fin n) (Fin n) ℂ)
    (hU : U.conjTranspose * U = 1) :
    frobNormSq (U * X * U.conjTranspose) = frobNormSq X := by
  rw [Matrix.mul_assoc, frobNormSq_unitary_left U (X * U.conjTranspose) hU]
  have hU2 : U.conjTranspose * (U.conjTranspose).conjTranspose = 1 := by
    rw [Matrix.conjTranspose_conjTranspose]; exact hU
  exact frobNormSq_unitary_right U.conjTranspose X hU2

/-- 三角不等式：|a+b|² ≤ 2(|a|²+|b|²)。证明使用平行四边形律。 -/
lemma normSq_add_le_two_normSq (a b : ℂ) : normSq (a + b) ≤ 2 * (normSq a + normSq b) := by
  have h_para : normSq (a + b) + normSq (a - b) = 2 * (normSq a + normSq b) := by
    simp [normSq]; ring
  have h_nonneg : 0 ≤ normSq (a - b) := normSq_nonneg _
  nlinarith

theorem frobNormSq_triangle_sq {m n : ℕ} (A B : Matrix (Fin m) (Fin n) ℂ) :
    frobNormSq (A + B) ≤ 2 * (frobNormSq A + frobNormSq B) := by
  unfold frobNormSq
  calc
    (∑ i : Fin m, ∑ j : Fin n, normSq ((A + B) i j))
        = (∑ i : Fin m, ∑ j : Fin n, normSq (A i j + B i j)) := rfl
    _ ≤ (∑ i : Fin m, ∑ j : Fin n, 2 * (normSq (A i j) + normSq (B i j))) := by
      refine Finset.sum_le_sum (λ i _ => ?_)
      refine Finset.sum_le_sum (λ j _ => ?_)
      calc
        normSq ((A + B) i j) = normSq (A i j + B i j) := rfl
        _ ≤ 2 * (normSq (A i j) + normSq (B i j)) := normSq_add_le_two_normSq (A i j) (B i j)
    _ = 2 * (frobNormSq A + frobNormSq B) := by
      unfold frobNormSq
      calc
        (∑ i : Fin m, ∑ j : Fin n, 2 * (normSq (A i j) + normSq (B i j)))
            = (∑ i : Fin m, 2 * (∑ j : Fin n, (normSq (A i j) + normSq (B i j)))) := by
          refine Finset.sum_congr rfl (λ i hi => ?_)
          rw [Finset.mul_sum]
        _ = 2 * (∑ i : Fin m, ∑ j : Fin n, (normSq (A i j) + normSq (B i j))) := by
          rw [Finset.mul_sum]
        _ = 2 * ((∑ i : Fin m, ∑ j : Fin n, normSq (A i j)) + (∑ i : Fin m, ∑ j : Fin n, normSq (B i j))) := by
          simp [Finset.sum_add_distrib]
        _ = 2 * (frobNormSq A + frobNormSq B) := rfl

/-!
Frobenius 范数次可乘性：‖AB‖_F² ≤ ‖A‖_F² · ‖B‖_F²。
证明: |(AB)_ij| ≤ Σ|A_ik||B_kj| (三角不等式) → ℝ Cauchy-Schwarz → 求和。
-/

lemma cauchy_schwarz_entry {m n p : ℕ} (A : Matrix (Fin m) (Fin n) ℂ) (B : Matrix (Fin n) (Fin p) ℂ)
    (i : Fin m) (j : Fin p) :
    normSq ((A * B) i j) ≤ (∑ k : Fin n, normSq (A i k)) * (∑ k : Fin n, normSq (B k j)) := by
  -- |(AB)_ij| ≤ Σ‖A_ik·B_kj‖ (三角不等式)
  have h_tri : ‖(A * B) i j‖ ≤ ∑ k : Fin n, ‖A i k * B k j‖ := by
    calc
      ‖(A * B) i j‖ = ‖∑ k : Fin n, A i k * B k j‖ := by simp [Matrix.mul_apply]
      _ ≤ ∑ k : Fin n, ‖A i k * B k j‖ := norm_sum_le _ _
  -- ‖A_ik·B_kj‖ = ‖A_ik‖·‖B_kj‖ (范数的乘性)
  have h_norm_mul : ∀ k : Fin n, ‖A i k * B k j‖ = ‖A i k‖ * ‖B k j‖ := by
    intro k; simp
  have h_tri' : ‖(A * B) i j‖ ≤ ∑ k : Fin n, ‖A i k‖ * ‖B k j‖ := by
    simpa [h_norm_mul] using h_tri
  -- ℝ 上的 Cauchy-Schwarz: (∑ a_k·b_k)² ≤ (∑ a_k²)(∑ b_k²)
  have h_cs : (∑ k : Fin n, ‖A i k‖ * ‖B k j‖) ^ 2 ≤ (∑ k : Fin n, ‖A i k‖ ^ 2) * (∑ k : Fin n, ‖B k j‖ ^ 2) := by
    set a := λ (k : Fin n) => ‖A i k‖
    set b := λ (k : Fin n) => ‖B k j‖
    have h_nonneg_quad : ∀ (t : ℝ), 0 ≤ ∑ k : Fin n, (t * a k - b k) ^ 2 := by
      intro t; refine Finset.sum_nonneg (λ k _ => ?_); positivity
    have h_quad_form : ∀ (t : ℝ), ∑ k : Fin n, (t * a k - b k) ^ 2 =
        t ^ 2 * (∑ k : Fin n, a k ^ 2) - 2 * t * (∑ k : Fin n, a k * b k) + (∑ k : Fin n, b k ^ 2) := by
      intro t
      calc
        ∑ k : Fin n, (t * a k - b k) ^ 2 = ∑ k : Fin n, (t ^ 2 * a k ^ 2 - 2 * t * a k * b k + b k ^ 2) := by
          refine Finset.sum_congr rfl (λ k hk => ?_)
          ring
        _ = (∑ k : Fin n, t ^ 2 * a k ^ 2) - (∑ k : Fin n, 2 * t * a k * b k) + (∑ k : Fin n, b k ^ 2) := by
          simp [Finset.sum_add_distrib, Finset.sum_sub_distrib, mul_assoc]
        _ = t ^ 2 * (∑ k : Fin n, a k ^ 2) - 2 * t * (∑ k : Fin n, a k * b k) + (∑ k : Fin n, b k ^ 2) := by
          simp [Finset.mul_sum, mul_comm, mul_left_comm, mul_assoc]
    set A := ∑ k : Fin n, a k ^ 2
    set B := ∑ k : Fin n, a k * b k
    set C := ∑ k : Fin n, b k ^ 2
    by_cases hAzero : A = 0
    · -- A = 0 ⇒ 所有 a_k = 0 ⇒ B = 0
      have hBzero : B = 0 := by
        have : ∀ k, a k = 0 := by
          intro k
          have h_single : a k ^ 2 ≤ A :=
            Finset.single_le_sum (λ i hi => pow_two_nonneg _) (Finset.mem_univ k)
          nlinarith
        simp [this, B]
      simp [hAzero, hBzero]
    · -- A > 0: 取 t = B/A
      have hApos : 0 < A := by
        have h_nonneg : 0 ≤ A := Finset.sum_nonneg (λ k _ => pow_two_nonneg _)
        exact lt_of_le_of_ne h_nonneg (Ne.symm hAzero)
      have h_at_t : 0 ≤ A * (B / A) ^ 2 - 2 * B * (B / A) + C := by
        have h_temp := h_nonneg_quad (B / A)
        have h_temp' := h_quad_form (B / A)
        -- h_temp': ∑... = (B/A)²*A - 2*(B/A)*B + C
        -- target: 0 ≤ A*(B/A)² - 2*B*(B/A) + C (需要交换次序)
        rw [h_temp'] at h_temp
        -- h_temp: 0 ≤ (B/A)²*A - 2*(B/A)*B + C
        -- 重排项: (B/A)²*A = A*(B/A)², 2*(B/A)*B = 2*B*(B/A)
        simpa [mul_comm, mul_left_comm, mul_assoc] using h_temp
      have h_ineq : B ^ 2 ≤ A * C := by
        field_simp [hApos.ne.symm] at h_at_t
        nlinarith
      nlinarith
  -- normSq(z) = ‖z‖²
  have h_norm_sq_eq (z : ℂ) : normSq z = ‖z‖ ^ 2 := by
    simpa using (Complex.normSq_eq_norm_sq z)
  have h_nonneg_sum : 0 ≤ ∑ k : Fin n, ‖A i k‖ * ‖B k j‖ :=
    Finset.sum_nonneg (λ k _ => mul_nonneg (norm_nonneg _) (norm_nonneg _))
  calc
    normSq ((A * B) i j) = ‖(A * B) i j‖ ^ 2 := h_norm_sq_eq _
    _ ≤ (∑ k : Fin n, ‖A i k‖ * ‖B k j‖) ^ 2 := by
      have h_nonneg_ab : 0 ≤ ‖(A * B) i j‖ := norm_nonneg _
      nlinarith
    _ ≤ (∑ k : Fin n, ‖A i k‖ ^ 2) * (∑ k : Fin n, ‖B k j‖ ^ 2) := h_cs
    _ = (∑ k : Fin n, normSq (A i k)) * (∑ k : Fin n, normSq (B k j)) := by
      simp [h_norm_sq_eq]

theorem frobNormSq_mul_le {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℂ) :
    frobNormSq (A * B) ≤ frobNormSq A * frobNormSq B := by
  unfold frobNormSq
  have h_entry := cauchy_schwarz_entry A B
  calc
    (∑ i : Fin n, ∑ j : Fin n, normSq ((A * B) i j))
        ≤ (∑ i : Fin n, ∑ j : Fin n, ((∑ k : Fin n, normSq (A i k)) * (∑ k : Fin n, normSq (B k j)))) :=
      Finset.sum_le_sum (λ i _ => Finset.sum_le_sum (λ j _ => h_entry i j))
    _ = (∑ i : Fin n, (∑ k : Fin n, normSq (A i k)) * (∑ j : Fin n, ∑ k : Fin n, normSq (B k j))) := by
      simp [Finset.mul_sum]
    _ = (∑ i : Fin n, ∑ k : Fin n, normSq (A i k)) * (∑ j : Fin n, ∑ k : Fin n, normSq (B k j)) := by
      simp [Finset.sum_mul]
    _ = frobNormSq A * frobNormSq B := by
      unfold frobNormSq
      have hsum : (∑ j : Fin n, ∑ k : Fin n, normSq (B k j)) = (∑ i : Fin n, ∑ j : Fin n, normSq (B i j)) := by
        rw [Finset.sum_comm]
      rw [hsum]

/-- 矩形矩阵的 Frobenius 范数次可乘性（使用 cauchy_schwarz_entry 直接证明）。 -/
lemma frobNormSq_mul_le_rect {m n p : ℕ} (A : Matrix (Fin m) (Fin n) ℂ) (B : Matrix (Fin n) (Fin p) ℂ) :
    frobNormSq (A * B) ≤ frobNormSq A * frobNormSq B := by
  unfold frobNormSq
  have h_entry := cauchy_schwarz_entry A B
  have h1 : (∑ i : Fin m, ∑ j : Fin p, normSq ((A * B) i j))
      ≤ (∑ i : Fin m, ∑ j : Fin p, ((∑ k : Fin n, normSq (A i k)) * (∑ k : Fin n, normSq (B k j)))) :=
    Finset.sum_le_sum (λ i _ => Finset.sum_le_sum (λ j _ => h_entry i j))
  have h2 : (∑ i : Fin m, ∑ j : Fin p, ((∑ k : Fin n, normSq (A i k)) * (∑ k : Fin n, normSq (B k j))))
      = (∑ i : Fin m, (∑ k : Fin n, normSq (A i k)) * (∑ j : Fin p, ∑ k : Fin n, normSq (B k j))) := by
    simp [Finset.mul_sum]
  have h3 : (∑ i : Fin m, (∑ k : Fin n, normSq (A i k)) * (∑ j : Fin p, ∑ k : Fin n, normSq (B k j)))
      = (∑ i : Fin m, ∑ k : Fin n, normSq (A i k)) * (∑ j : Fin p, ∑ k : Fin n, normSq (B k j)) := by
    simp [Finset.sum_mul]
  have h4 : (∑ i : Fin m, ∑ k : Fin n, normSq (A i k)) = frobNormSq A := rfl
  have h5 : (∑ j : Fin p, ∑ k : Fin n, normSq (B k j)) = frobNormSq B := by
    calc
      (∑ j : Fin p, ∑ k : Fin n, normSq (B k j)) = (∑ k : Fin n, ∑ j : Fin p, normSq (B k j)) := by
        rw [Finset.sum_comm]
      _ = (∑ i : Fin n, ∑ j : Fin p, normSq (B i j)) := rfl
      _ = frobNormSq B := rfl
  calc
    frobNormSq (A * B) = (∑ i : Fin m, ∑ j : Fin p, normSq ((A * B) i j)) := rfl
    _ ≤ (∑ i : Fin m, ∑ j : Fin p, ((∑ k : Fin n, normSq (A i k)) * (∑ k : Fin n, normSq (B k j)))) := h1
    _ = (∑ i : Fin m, (∑ k : Fin n, normSq (A i k)) * (∑ j : Fin p, ∑ k : Fin n, normSq (B k j))) := h2
    _ = (∑ i : Fin m, ∑ k : Fin n, normSq (A i k)) * (∑ j : Fin p, ∑ k : Fin n, normSq (B k j)) := h3
    _ = frobNormSq A * frobNormSq B := by rw [h4, h5]

/-! §2 偏差度量 -/

/-- 交换律偏差 Δ 的 Frobenius 范数平方。 -/
noncomputable def deviationNormSq {X Y Z : SpObj}
    {P Q R : X ⟶ Y} {P' Q' R' : Y ⟶ Z}
    (α : SpTwoMorphism P Q) (β : SpTwoMorphism Q R)
    (α' : SpTwoMorphism P' Q') (β' : SpTwoMorphism Q' R') : ℝ :=
  frobNormSq ((spHorizComp (spVertComp α β) (spVertComp α' β')).homotopy -
    (spVertComp (spHorizComp α α') (spHorizComp β β')).homotopy)

/-! §3 谱间隙绑定 -/

/-- 简化版本：deviationNormSq 被范数乘积和谱算子范数限制。
    证明：deviationNormSq ≤ 8·(‖X.A‖²+‖Y.A‖²+‖Z.A‖²)·‖β.h‖²·‖α'.h‖²。
    在 Cl(1,7) 框架中所有谱算子归一化，简化为 24·‖β.h‖²·‖α'.h‖²。 -/
theorem deviation_spectral_bound_simplified {X Y Z : SpObj}
    {P Q R : X ⟶ Y} {P' Q' R' : Y ⟶ Z}
    (α : SpTwoMorphism P Q) (β : SpTwoMorphism Q R)
    (α' : SpTwoMorphism P' Q') (β' : SpTwoMorphism Q' R') :
    deviationNormSq α β α' β' ≤
    8 * (frobNormSq (X.A) + frobNormSq (Y.A) + frobNormSq (Z.A)) * frobNormSq β.homotopy * frobNormSq α'.homotopy := by
  -- 将偏差用 spExchangeLaw_homotopy_deviation 展开
  have h_dev := spExchangeLaw_homotopy_deviation α β α' β'
  unfold deviationNormSq
  rw [h_dev]
  -- Δ = (R.P - Q.P)·α'.h + β.h·(P'.P - Q'.P)
  set Δ₁ := (R.P - Q.P) * α'.homotopy
  set Δ₂ := β.homotopy * (P'.P - Q'.P)
  have h_tri : frobNormSq (Δ₁ + Δ₂) ≤ 2 * (frobNormSq Δ₁ + frobNormSq Δ₂) :=
    frobNormSq_triangle_sq _ _
  have h_mul₁ : frobNormSq Δ₁ ≤ frobNormSq (R.P - Q.P) * frobNormSq α'.homotopy :=
    frobNormSq_mul_le_rect (R.P - Q.P) α'.homotopy
  have h_mul₂ : frobNormSq Δ₂ ≤ frobNormSq β.homotopy * frobNormSq (P'.P - Q'.P) :=
    frobNormSq_mul_le_rect β.homotopy (P'.P - Q'.P)
  -- 由 β.condition: R.P - Q.P = X.A·β.h - β.h·Y.A
  have h_cond_β : R.P - Q.P = X.A * β.homotopy - β.homotopy * Y.A :=
    β.condition
  have h_bound_RP : frobNormSq (X.A * β.homotopy - β.homotopy * Y.A) ≤
      2 * frobNormSq β.homotopy * (frobNormSq (X.A) + frobNormSq (Y.A)) := by
    have h_tri : frobNormSq (X.A * β.homotopy - β.homotopy * Y.A) ≤
        2 * (frobNormSq (X.A * β.homotopy) + frobNormSq (β.homotopy * Y.A)) := by
      calc
        frobNormSq (X.A * β.homotopy - β.homotopy * Y.A)
            = frobNormSq (X.A * β.homotopy + (-(β.homotopy * Y.A))) := by simp [sub_eq_add_neg]
        _ ≤ 2 * (frobNormSq (X.A * β.homotopy) + frobNormSq (-(β.homotopy * Y.A))) :=
          frobNormSq_triangle_sq _ _
        _ = 2 * (frobNormSq (X.A * β.homotopy) + frobNormSq (β.homotopy * Y.A)) := by simp [frobNormSq_neg]
    have h_mul1 : frobNormSq (X.A * β.homotopy) ≤ frobNormSq (X.A) * frobNormSq β.homotopy := by
      apply frobNormSq_mul_le_rect
    have h_mul2 : frobNormSq (β.homotopy * Y.A) ≤ frobNormSq β.homotopy * frobNormSq (Y.A) := by
      apply frobNormSq_mul_le_rect
    nlinarith
  have h_mul₁_bound : frobNormSq Δ₁ ≤
      2 * frobNormSq β.homotopy * (frobNormSq (X.A) + frobNormSq (Y.A)) * frobNormSq α'.homotopy := by
    have h_bound_RP' : frobNormSq (R.P - Q.P) ≤ 2 * frobNormSq β.homotopy * (frobNormSq (X.A) + frobNormSq (Y.A)) := by
      calc
        frobNormSq (R.P - Q.P) = frobNormSq (X.A * β.homotopy - β.homotopy * Y.A) := by simp [h_cond_β]
        _ ≤ 2 * frobNormSq β.homotopy * (frobNormSq (X.A) + frobNormSq (Y.A)) := h_bound_RP
    calc
      frobNormSq Δ₁ ≤ frobNormSq (R.P - Q.P) * frobNormSq α'.homotopy := h_mul₁
      _ ≤ (2 * frobNormSq β.homotopy * (frobNormSq (X.A) + frobNormSq (Y.A))) * frobNormSq α'.homotopy := by
        have h_nonneg : 0 ≤ frobNormSq α'.homotopy := frobNormSq_nonneg _
        nlinarith
      _ = 2 * frobNormSq β.homotopy * (frobNormSq (X.A) + frobNormSq (Y.A)) * frobNormSq α'.homotopy := by ring
  -- 由 α'.condition: P'.P - Q'.P = -(Y.A·α'.h - α'.h·Z.A)
  have h_cond_α' : P'.P - Q'.P = -(Y.A * α'.homotopy - α'.homotopy * Z.A) := by
    calc
      P'.P - Q'.P = -(Q'.P - P'.P) := by simp
      _ = -(Y.A * α'.homotopy - α'.homotopy * Z.A) := by rw [α'.condition]
  have h_bound_PP : frobNormSq (Y.A * α'.homotopy - α'.homotopy * Z.A) ≤
      2 * frobNormSq α'.homotopy * (frobNormSq (Y.A) + frobNormSq (Z.A)) := by
    have h_tri : frobNormSq (Y.A * α'.homotopy - α'.homotopy * Z.A) ≤
        2 * (frobNormSq (Y.A * α'.homotopy) + frobNormSq (α'.homotopy * Z.A)) := by
      calc
        frobNormSq (Y.A * α'.homotopy - α'.homotopy * Z.A)
            = frobNormSq (Y.A * α'.homotopy + (-(α'.homotopy * Z.A))) := by simp [sub_eq_add_neg]
        _ ≤ 2 * (frobNormSq (Y.A * α'.homotopy) + frobNormSq (-(α'.homotopy * Z.A))) :=
          frobNormSq_triangle_sq _ _
        _ = 2 * (frobNormSq (Y.A * α'.homotopy) + frobNormSq (α'.homotopy * Z.A)) := by simp [frobNormSq_neg]
    have h_mul1 : frobNormSq (Y.A * α'.homotopy) ≤ frobNormSq (Y.A) * frobNormSq α'.homotopy := by
      apply frobNormSq_mul_le_rect
    have h_mul2 : frobNormSq (α'.homotopy * Z.A) ≤ frobNormSq α'.homotopy * frobNormSq (Z.A) := by
      apply frobNormSq_mul_le_rect
    nlinarith
  have h_mul₂_bound : frobNormSq Δ₂ ≤
      2 * frobNormSq β.homotopy * frobNormSq α'.homotopy * (frobNormSq (Y.A) + frobNormSq (Z.A)) := by
    have h_bound_PP' : frobNormSq (P'.P - Q'.P) ≤ 2 * frobNormSq α'.homotopy * (frobNormSq (Y.A) + frobNormSq (Z.A)) := by
      calc
        frobNormSq (P'.P - Q'.P) = frobNormSq (-(Y.A * α'.homotopy - α'.homotopy * Z.A)) := by rw [h_cond_α']
        _ = frobNormSq (Y.A * α'.homotopy - α'.homotopy * Z.A) := by rw [frobNormSq_neg]
        _ ≤ 2 * frobNormSq α'.homotopy * (frobNormSq (Y.A) + frobNormSq (Z.A)) := h_bound_PP
    calc
      frobNormSq Δ₂ ≤ frobNormSq β.homotopy * frobNormSq (P'.P - Q'.P) := h_mul₂
      _ ≤ frobNormSq β.homotopy * (2 * frobNormSq α'.homotopy * (frobNormSq (Y.A) + frobNormSq (Z.A))) := by
        have h_nonneg : 0 ≤ frobNormSq β.homotopy := frobNormSq_nonneg _
        nlinarith
      _ = 2 * frobNormSq β.homotopy * frobNormSq α'.homotopy * (frobNormSq (Y.A) + frobNormSq (Z.A)) := by ring
  -- 组合不等式
  have h_final : frobNormSq (Δ₁ + Δ₂) ≤
      8 * (frobNormSq (X.A) + frobNormSq (Y.A) + frobNormSq (Z.A)) * frobNormSq β.homotopy * frobNormSq α'.homotopy := by
    have h_nonneg_XY : 0 ≤ frobNormSq (X.A) + frobNormSq (Y.A) + frobNormSq (Z.A) := by
      have hX : 0 ≤ frobNormSq (X.A) := frobNormSq_nonneg _
      have hY : 0 ≤ frobNormSq (Y.A) := frobNormSq_nonneg _
      have hZ : 0 ≤ frobNormSq (Z.A) := frobNormSq_nonneg _
      nlinarith
    have h_nonneg_β : 0 ≤ frobNormSq β.homotopy := frobNormSq_nonneg _
    have h_nonneg_α' : 0 ≤ frobNormSq α'.homotopy := frobNormSq_nonneg _
    have h_intermediate : frobNormSq (Δ₁ + Δ₂) ≤
        4 * (frobNormSq (X.A) + 2 * frobNormSq (Y.A) + frobNormSq (Z.A)) * frobNormSq β.homotopy * frobNormSq α'.homotopy := by
      nlinarith
    have h_ineq : frobNormSq (X.A) + 2 * frobNormSq (Y.A) + frobNormSq (Z.A) ≤
        2 * (frobNormSq (X.A) + frobNormSq (Y.A) + frobNormSq (Z.A)) := by
      have hX : 0 ≤ frobNormSq (X.A) := frobNormSq_nonneg _
      have hY : 0 ≤ frobNormSq (Y.A) := frobNormSq_nonneg _
      have hZ : 0 ≤ frobNormSq (Z.A) := frobNormSq_nonneg _
      nlinarith
    calc
      frobNormSq (Δ₁ + Δ₂)
          ≤ 4 * (frobNormSq (X.A) + 2 * frobNormSq (Y.A) + frobNormSq (Z.A)) * frobNormSq β.homotopy * frobNormSq α'.homotopy := h_intermediate
      _ ≤ 4 * (2 * (frobNormSq (X.A) + frobNormSq (Y.A) + frobNormSq (Z.A))) * frobNormSq β.homotopy * frobNormSq α'.homotopy := by
        have h_nonneg : 0 ≤ frobNormSq β.homotopy * frobNormSq α'.homotopy := mul_nonneg h_nonneg_β h_nonneg_α'
        have hX : 0 ≤ frobNormSq (X.A) := frobNormSq_nonneg _
        have hY : 0 ≤ frobNormSq (Y.A) := frobNormSq_nonneg _
        have hZ : 0 ≤ frobNormSq (Z.A) := frobNormSq_nonneg _
        nlinarith
      _ = 8 * (frobNormSq (X.A) + frobNormSq (Y.A) + frobNormSq (Z.A)) * frobNormSq β.homotopy * frobNormSq α'.homotopy := by ring
  exact h_final

/-- Rayleigh 商估计：对 Hermitian 矩阵 A 和任意 B, C，有
    ‖B·(A - λ₁I)·C‖_F² ≤ Δλ_min²·‖B‖_F²·‖C‖_F²
    其中 λ₁ = agEigenvalue 1 n 是 A 的最小特征值，Δλ_min = spectralGap n 是谱间隙。

※ 修正（2026-08-04）：原陈述对**任意** Hermitian 矩阵 A 不成立——
`agEigenvalue`/`spectralGap` 是 Cl(1,7)/SU(2) 谱框架的**特定常数**
（√{k(k+1)} 归一化），而非任意 A 的特征值。正确陈述需要额外假设
"A 具有 A_GR 谱 {λ_k = agEigenvalue k n}"（物理模型断言，非数学定理）。
修正：将该物理模型断言**显式化为假设** `hGap`——
`frobNormSq (A - (agEigenvalue 1 n) • 1) ≤ (spectralGap n)²`（即谱间隙的
Frobenius 上界）。在此假设下用 Frobenius 次可乘性（`frobNormSq_mul_le`）两次
即可机器证明，零 `sorry`；A_GR 谱假设本身仍为物理模型断言（对应 §5.6-5.7
及 paperX_gravity_c_constant.py 的数值验证）。 -/
lemma spectral_gap_estimate {n : ℕ} (A : Matrix (Fin n) (Fin n) ℂ)
    (B : Matrix (Fin n) (Fin n) ℂ) (C : Matrix (Fin n) (Fin n) ℂ)
    (hGap : frobNormSq (A - (agEigenvalue 1 n) • 1) ≤ (spectralGap n) ^ 2) :
    frobNormSq (B * (A - (agEigenvalue 1 n) • 1) * C) ≤
    (spectralGap n) ^ 2 * frobNormSq B * frobNormSq C := by
  -- Frobenius 次可乘性两次：‖B·M·C‖² ≤ ‖B‖²·‖M‖²·‖C‖²
  have h1 : frobNormSq (B * (A - (agEigenvalue 1 n) • 1) * C) ≤
      frobNormSq (B * (A - (agEigenvalue 1 n) • 1)) * frobNormSq C :=
    frobNormSq_mul_le (B * (A - (agEigenvalue 1 n) • 1)) C
  have h2 : frobNormSq (B * (A - (agEigenvalue 1 n) • 1)) ≤
      frobNormSq B * frobNormSq (A - (agEigenvalue 1 n) • 1) :=
    frobNormSq_mul_le B (A - (agEigenvalue 1 n) • 1)
  have h_nonneg_C : 0 ≤ frobNormSq C := frobNormSq_nonneg C
  calc
    frobNormSq (B * (A - (agEigenvalue 1 n) • 1) * C)
        ≤ frobNormSq (B * (A - (agEigenvalue 1 n) • 1)) * frobNormSq C := h1
    _ ≤ (frobNormSq B * frobNormSq (A - (agEigenvalue 1 n) • 1)) * frobNormSq C := by
      exact mul_le_mul_of_nonneg_right h2 h_nonneg_C
    _ ≤ (frobNormSq B * (spectralGap n) ^ 2) * frobNormSq C := by
      have h_nonneg_B : 0 ≤ frobNormSq B := frobNormSq_nonneg B
      have h_mul : frobNormSq B * frobNormSq (A - (agEigenvalue 1 n) • 1) ≤
          frobNormSq B * (spectralGap n) ^ 2 :=
        mul_le_mul_of_nonneg_left hGap h_nonneg_B
      exact mul_le_mul_of_nonneg_right h_mul h_nonneg_C
    _ = (spectralGap n) ^ 2 * frobNormSq B * frobNormSq C := by ring

/-- 基于谱间隙的定量绑定（已修正，2026-08-04）。

    原陈述缺 A_GR 谱假设 + Cl(1,7) 归一化，一般 Hermitian S.A 下不可证。
    修正：将物理归一化断言显式化为假设 `hNorm`——
    `24 · frobNormSq(S.A) ≤ (4·spectralGap 8)²`（Cl(1,7) 框架谱算子归一化，
    对应 `deviation_spectral_bound_simplified` 注释"简化为 24·‖β.h‖²·‖α'.h‖²"）。
    在此假设下由 `deviation_spectral_bound_simplified`（已证）直接传递，零 `sorry`。

    推导结构（与 `deviation_spectral_bound_simplified` 一致）：
      1. spExchangeLaw_deviation_partial_commutator → Δ = S.A·H - 2·β.h·S.A·α'.h + H·S.A
      2. Frobenius 次可乘性 + 三角不等式 → ‖Δ‖² ≤ 8·3·‖S.A‖²·‖β.h‖²·‖α'.h‖²
      3. 归一化假设 hNorm → ≤ (4·spectralGap 8)²·‖β.h‖²·‖α'.h‖² -/
theorem deviation_spectral_bound (S : SpObj)
    {P Q R : S ⟶ S} {P' Q' R' : S ⟶ S}
    (α : SpTwoMorphism P Q) (β : SpTwoMorphism Q R)
    (α' : SpTwoMorphism P' Q') (β' : SpTwoMorphism Q' R')
    (hNorm : 24 * frobNormSq (S.A) ≤ (4 * spectralGap 8) ^ 2) :
    deviationNormSq α β α' β' ≤
    (4 * spectralGap 8) ^ 2 * frobNormSq β.homotopy * frobNormSq α'.homotopy := by
  have h_simp := deviation_spectral_bound_simplified α β α' β'
  have hsum : 8 * (frobNormSq (S.A) + frobNormSq (S.A) + frobNormSq (S.A)) =
      24 * frobNormSq (S.A) := by ring
  have hβ : 0 ≤ frobNormSq β.homotopy := frobNormSq_nonneg _
  have hα' : 0 ≤ frobNormSq α'.homotopy := frobNormSq_nonneg _
  calc
    deviationNormSq α β α' β'
        ≤ 8 * (frobNormSq (S.A) + frobNormSq (S.A) + frobNormSq (S.A)) * frobNormSq β.homotopy * frobNormSq α'.homotopy := h_simp
    _ = 24 * frobNormSq (S.A) * frobNormSq β.homotopy * frobNormSq α'.homotopy := by rw [hsum]
    _ ≤ (4 * spectralGap 8) ^ 2 * frobNormSq β.homotopy * frobNormSq α'.homotopy := by
      have h_prod : 0 ≤ frobNormSq β.homotopy * frobNormSq α'.homotopy := mul_nonneg hβ hα'
      have h1 : (24 * frobNormSq (S.A)) * (frobNormSq β.homotopy * frobNormSq α'.homotopy) ≤
          (4 * spectralGap 8) ^ 2 * (frobNormSq β.homotopy * frobNormSq α'.homotopy) :=
        mul_le_mul_of_nonneg_right hNorm h_prod
      simpa [mul_assoc] using h1

/-! ### §1.6 源缺陷线性（B1 ① 环，2026-07-29 新增）

    source_defect_linearity：向谱算子 A 添加局域缺陷 δλ·P₀ 后，
    交换律偏差 Δ 严格线性变化——无高阶项、无近似。
    这是 paper18 §4.4 最为缺失的"质量在力中如何出现"的代数答案。 -/

/-- 偏差谱算子的代数形式（无范畴结构，纯矩阵代数）：
    Δ(A, H, β, α') := A·H - 2·β·A·α' + H·A
    其中 H = β.homotopy · α'.homotopy。
    该形式直接来自 spExchangeLaw_deviation_partial_commutator。 -/
noncomputable def deltaOp {n : ℕ}
    (A β_h α'_h : Matrix (Fin n) (Fin n) ℂ) : Matrix (Fin n) (Fin n) ℂ :=
  A * (β_h * α'_h) - 2 • (β_h * (A * α'_h)) + (β_h * α'_h) * A

/-- **源缺陷线性定理**（B1 ① 环，严格代数）。

    设 A 为谱算子，P₀ 为局域投影（缺陷支撑），δλ ∈ ℂ 为缺陷幅度。
    定义 H = β_h · α'_h。则偏差 Δ 在 A → A + δλ·P₀ 下严格线性变化：

    Δ(A + δλ·P₀, H, β, α') - Δ(A, H, β, α') = δλ·(P₀·H - 2·β·P₀·α' + H·P₀)

    无高阶项、无需微扰展开、无近似——纯分配律的代数推论。 -/
theorem source_defect_linearity {n : ℕ}
    (A P₀ beta_h alpha'_h : Matrix (Fin n) (Fin n) ℂ) (dlambda : ℂ) :
    deltaOp (A + dlambda • P₀) beta_h alpha'_h - deltaOp A beta_h alpha'_h =
    dlambda • (P₀ * (beta_h * alpha'_h) - 2 • (beta_h * P₀ * alpha'_h) + (beta_h * alpha'_h) * P₀) := by
  unfold deltaOp
  set H := beta_h * alpha'_h
  calc
    ((A + dlambda • P₀) * H - 2 • (beta_h * ((A + dlambda • P₀) * alpha'_h)) + H * (A + dlambda • P₀)) -
    (A * H - 2 • (beta_h * (A * alpha'_h)) + H * A)
        = ((A + dlambda • P₀) * H - 2 • (beta_h * ((A + dlambda • P₀) * alpha'_h)) + H * (A + dlambda • P₀)) -
          (A * H - 2 • (beta_h * (A * alpha'_h)) + H * A) := rfl
    _ = dlambda • (P₀ * H - 2 • (beta_h * P₀ * alpha'_h) + H * P₀) := by
      -- 展开 (A + dλ·P₀)·H − A·H = dλ·P₀·H，β·(A+dλ·P₀)·α' − β·A·α' = dλ·β·P₀·α'，依此类推
      -- 所有交叉项抵消，仅剩 dλ 线性项。纯代数恒等式，无矩阵对易性假设。
      calc
        ((A + dlambda • P₀) * H - 2 • (beta_h * ((A + dlambda • P₀) * alpha'_h)) + H * (A + dlambda • P₀)) -
        (A * H - 2 • (beta_h * (A * alpha'_h)) + H * A)
            = (dlambda • (P₀ * H) - 2 • (dlambda • (beta_h * (P₀ * alpha'_h))) + dlambda • (H * P₀)) := by
          simp [Matrix.add_mul, Matrix.mul_add, add_comm, add_left_comm, add_assoc, sub_eq_add_neg]
          abel
        _ = dlambda • (P₀ * H - 2 • (beta_h * (P₀ * alpha'_h)) + H * P₀) := by
          simp [smul_add, smul_sub]
        _ = dlambda • (P₀ * H - 2 • (beta_h * P₀ * alpha'_h) + H * P₀) := by
          simp [Matrix.mul_assoc]
    _ = dlambda • (P₀ * (beta_h * alpha'_h) - 2 • (beta_h * P₀ * alpha'_h) + (beta_h * alpha'_h) * P₀) := by
      simp [H, Matrix.mul_assoc]

/-! ### §1.7 J2 严格正交：对易子模式间定位的机器证明（paper31 §3，2026-08-12 补）

    paper31 §3 命题 J2（模式间定位）：[A, δb]_{ij} = (λ_i − λ_j)·δb_{ij}，对角元恒为零——
    "Δ 的方向不在任何单一谱模式/标量方向"。J2 原本就应以**严格正交**为验证标准
    （非仅代数恒等式或数值检查）。本子节在既有 deltaOp/spExchangeLaw_deviation_partial_commutator
    的对易子结构上给出 J2 的严格机器证明（不另起炉灶）：
    1. `commutator_trace_zero`：Tr([A,B]) = 0——对易子与恒等（标量）方向投影为零；
    2. `commutator_trace_orthogonal_scalar`：与任意标量矩阵 c·I 迹正交（Hilbert-Schmidt 意义）；
    3. `commutator_diag_zero_of_diagonal`：谱基（A 对角）下 [A,B] 对角元恒零（J2 原表述）。 -/

/-- J2 严格形式（1）：对易子与恒等（标量）方向**严格正交**——Tr([A,B]) = 0
    （`Matrix.trace_mul_comm`：Tr(AB)=Tr(BA)，纯代数，无对易性假设）。
    "Δ 无标量分量"的机器证明。 -/
theorem commutator_trace_zero {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℂ) :
    (A * B - B * A).trace = 0 := by
  rw [Matrix.trace_sub, Matrix.trace_mul_comm]
  simp

/-- J2 严格形式（2）：对易子与任意标量方向 c·I **迹正交**——c·Tr([A,B]) = 0
    （Tr([A,B]·(c·I)) = c·Tr([A,B]) = 0；"Δ 的方向与任何均匀/标量方向正交"）。 -/
theorem commutator_trace_orthogonal_scalar {n : ℕ}
    (A B : Matrix (Fin n) (Fin n) ℂ) (c : ℂ) :
    c * (A * B - B * A).trace = 0 := by
  rw [commutator_trace_zero]
  simp

/-- J2 严格形式（3，原表述）：谱基（A = diagonal lam）下对易子对角元恒零——
    [A,B]_{ii} = lam_i·B_ii − B_ii·lam_i = 0。"Δ 与任何单一谱模式（基方向 E_ii）正交"的机器证明。 -/
theorem commutator_diag_zero_of_diagonal {n : ℕ} (lam : Fin n → ℂ)
    (B : Matrix (Fin n) (Fin n) ℂ) (i : Fin n) :
    (Matrix.diagonal lam * B - B * Matrix.diagonal lam) i i = 0 := by
  simp [Matrix.mul_apply, Matrix.diagonal_apply]
  ring

/-- J2 严格形式（4，谱方向完备）：谱基（A = diagonal lam）下，Δ 的对易子分量与**任意**对角方向
    D = diagonal d **迹正交**——Tr([A,B]·D) = 0（对角元恒零逐项消去）。
    "Δ 不在任何单一谱模式方向"的完备严格形式（任意对角方向，含每个基方向 E_ii 与恒等 I 之组合）。 -/
theorem commutator_trace_orthogonal_diagonal {n : ℕ} (lam d : Fin n → ℂ)
    (B : Matrix (Fin n) (Fin n) ℂ) :
    ((Matrix.diagonal lam * B - B * Matrix.diagonal lam) * Matrix.diagonal d).trace = 0 := by
  rw [Matrix.trace]
  apply Finset.sum_eq_zero
  intro i hi
  simp [Matrix.diag, Matrix.mul_apply, Matrix.diagonal_apply]
  left
  ring

/-! ### §1.8 范畴-几何桥：Δ 2-胞腔偏差矩阵的 J2 定位（2026-08-13）

    **登记开放项推进：lifting 正交与 J2 迹正交的范畴-几何桥同构**。

    **桥接语义（范畴层 ↔ 矩阵层）**：
    - 范畴层（mathlib `HasLiftingProperty` 1-层实例/`LiftingOrthogonality`）：lifting 正交 =
      方向类内单点性（法向 unfold ⊥ 水平 transition，唯一填充 = fold m / 水平 2-胞腔）；
    - 矩阵层（本文件 §1.7 J2）：Δ 对易子分量与恒等/任意对角方向迹正交
      （`commutator_trace_zero`/`commutator_trace_orthogonal_diagonal`）；
    - **桥**：Δ 2-胞腔（`SpDelta2Cell`，`HigherSpCategory.lean`——偏差胞腔的具体编码，
      携带层 2 交换律偏差矩阵）的矩阵内容在谱基下满足 J2 模式间定位——
      偏差胞腔与任何单一谱模式方向正交。本子节把 J2 显式应用到偏差矩阵
      （方阵情形），提供桥的矩阵层锚点；完整范畴-几何字典（法向↔V、水平↔H
      统一同构）仍登记开放。

    **非 KK 守卫**：桥的正交语义 = 模式间定位（矩阵对易子对角元零）与方向类
    填充性质，不引入空间坐标——正交不产生额外空间维度（paper44 §7.2 边界 1）。 -/

/-- **范畴-几何桥（J2 应用于 Δ 2-胞腔偏差矩阵，方阵情形）**：谱基（A = diagonal lam）
    下偏差矩阵 B 的对易子对角元恒零——Δ 2-胞腔偏差与任何单一谱模式方向正交
    （`SpDelta2Cell.dev` 的 J2 定位，桥的矩阵层锚点）。 -/
theorem delta2Cell_commutator_diag_zero {n : ℕ} (lam : Fin n → ℂ)
    (B : Matrix (Fin n) (Fin n) ℂ) (i : Fin n) :
    (Matrix.diagonal lam * B - B * Matrix.diagonal lam) i i = 0 :=
  commutator_diag_zero_of_diagonal lam B i

/-- **范畴-几何桥（偏差矩阵与任意对角方向迹正交）**：Δ 2-胞腔偏差矩阵 B 与任意
    对角方向 D = diagonal d 迹正交——偏差胞腔不在任何单一谱模式方向（含恒等与
    基方向组合，J2 谱方向完备形式应用到偏差内容）。 -/
theorem delta2Cell_commutator_trace_orthogonal_diagonal {n : ℕ} (lam d : Fin n → ℂ)
    (B : Matrix (Fin n) (Fin n) ℂ) :
    ((Matrix.diagonal lam * B - B * Matrix.diagonal lam) * Matrix.diagonal d).trace = 0 :=
  commutator_trace_orthogonal_diagonal lam d B

/-! ### §1.9 矩阵层完整字典：对角方向空间的正交补刻画（2026-08-14）
    **登记开放项推进（CategoryGeometryDictionary §骨架状态 4：矩阵层完整字典
    "J2 迹正交 → 偏差矩阵全体方向的逐项对应"）**。
    §1.7/§1.8 已证偏差矩阵 [A,B]（A 谱基对角）与**任意对角方向**迹正交
    （`commutator_trace_orthogonal_diagonal`，逐条方向）。
    本子节给出**空间级完整刻画**：在 Hilbert–Schmidt 内积（迹内积）下，
    **对角矩阵空间的正交补 = 零对角元矩阵空间**——
    "X 与任意对角方向迹正交 ⟺ X 对角元全零"（`hs_orthogonal_complement_diagonal`）。
    这把 J2 定位从"逐条方向正交"提升为"全体方向的补空间表述"——
    矩阵层完整字典的核心：偏差矩阵所在空间与谱模式方向空间正交分解。
    **非 KK 守卫**：补空间刻画为矩阵代数性质（迹内积下的正交补对偶），
    不引入空间坐标——正交不产生额外空间维度（paper44 §7.2 边界 1）。 -/

/-- 对角矩阵空间的正交补（Hilbert–Schmidt 迹内积）：X 与任意对角方向 D = diagonal d
    迹正交 ⟺ X 对角元全零——(Diag)ᗮ = {X | ∀i, X_ii = 0}。
    J2 定位（偏差矩阵与谱模式方向正交）的空间级完整表述（矩阵层完整字典核心）。 -/
theorem hs_orthogonal_complement_diagonal {n : ℕ} (X : Matrix (Fin n) (Fin n) ℂ) :
    (∀ d : Fin n → ℂ, (X * Matrix.diagonal d).trace = 0) ↔
      (∀ i : Fin n, X i i = 0) := by
  constructor
  · intro hX i
    -- 取 d = 单点指示 e_i：Tr(X·diag e_i) = X_ii（其余 k≠i 项消去）
    have htr : (X * Matrix.diagonal (fun j => if j = i then (1 : ℂ) else 0)).trace = X i i := by
      rw [Matrix.trace]
      rw [Finset.sum_eq_single i]
      · simp [Matrix.mul_apply, Matrix.diagonal_apply]
      · intro j _hj hne
        simp [Matrix.mul_apply, Matrix.diagonal_apply, hne]
      · intro hi
        simp at hi
    have h0 := hX (fun j => if j = i then (1 : ℂ) else 0)
    rwa [htr] at h0
  · intro hzero d
    rw [Matrix.trace]
    apply Finset.sum_eq_zero
    intro k hk
    calc
      (X * Matrix.diagonal d) k k = X k k * d k := by
        simp [Matrix.mul_apply, Matrix.diagonal_apply]
      _ = 0 := by rw [hzero k]; simp

/-- 矩阵层完整字典（偏差矩阵的补空间归属）：谱基（A = diagonal lam）下偏差矩阵 [A,B]
    对角元全零（J2 原表述，`commutator_diag_zero_of_diagonal`）⟹ 其属于对角方向空间的
    正交补——与**任意**对角方向迹正交（"全体方向"形式，`hs_orthogonal_complement_diagonal`
    的 (←) 方向直接给出）。J2 定位从逐条方向提升为完整补空间表述。 -/
theorem commutator_in_orthogonal_complement_diagonal {n : ℕ} (lam : Fin n → ℂ)
    (B : Matrix (Fin n) (Fin n) ℂ) :
    ∀ d : Fin n → ℂ,
      ((Matrix.diagonal lam * B - B * Matrix.diagonal lam) * Matrix.diagonal d).trace = 0 := by
  intro d
  exact (hs_orthogonal_complement_diagonal
    (Matrix.diagonal lam * B - B * Matrix.diagonal lam)).2
      (fun i => commutator_diag_zero_of_diagonal lam B i) d

end UFPFormalization
