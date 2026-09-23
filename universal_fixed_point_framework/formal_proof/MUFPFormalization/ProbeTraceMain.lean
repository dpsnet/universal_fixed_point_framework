import MUFPFormalization.HallEmergence
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Fintype.BigOperators
open Matrix Complex
open scoped BigOperators

namespace MUFPF

-- occFn 取值 ∈ {0,1}
lemma occFn_mem (x : ℝ) : occFn x = 0 ∨ occFn x = 1 := by
  unfold occFn
  split_ifs <;> simp

-- 占据计数
noncomputable def occupiedCount {n : ℕ} (H : Matrix (Fin n) (Fin n) ℂ)
    (hH : H.IsHermitian) : ℕ :=
  (Finset.univ.filter fun i => occFn (hH.eigenvalues i) = 1).card

-- 本征值项 cast ⟺ 计数项
lemma occFn_term_eq2 {n : ℕ} (H : Matrix (Fin n) (Fin n) ℂ) (hH : H.IsHermitian) (i : Fin n) :
    ((occFn (hH.eigenvalues i) : ℝ) : ℂ)
      = (if occFn (hH.eigenvalues i) = 1 then (1 : ℂ) else 0) := by
  have hv := occFn_mem (hH.eigenvalues i)
  rcases hv with h0 | h1
  · rw [h0]
    norm_num
  · rw [h1]
    norm_num

lemma sumOcc_eq_count2 {n : ℕ} (H : Matrix (Fin n) (Fin n) ℂ) (hH : H.IsHermitian) :
    (∑ i : Fin n, ((occFn (hH.eigenvalues i) : ℝ) : ℂ)) = (occupiedCount H hH : ℂ) := by
  classical
  change (∑ i : Fin n, ((occFn (hH.eigenvalues i) : ℝ) : ℂ))
      = ((Finset.univ.filter fun i => occFn (hH.eigenvalues i) = 1).card : ℂ)
  rw [show ((Finset.univ.filter fun i => occFn (hH.eigenvalues i) = 1).card : ℂ)
      = ∑ i : Fin n, (if occFn (hH.eigenvalues i) = 1 then (1 : ℂ) else 0)
      from (Finset.sum_boole).symm.trans (Finset.sum_congr rfl fun i _ => rfl)]
  apply Finset.sum_congr rfl
  intro i hi
  exact (occFn_term_eq2 H hH i).symm

-- trace → 对角 trace
lemma trace_spec_diag {n : ℕ} (H : Matrix (Fin n) (Fin n) ℂ) (hH : H.IsHermitian) :
    (occupiedProjection H hH).trace
      = (Matrix.diagonal (fun i : Fin n => ((occFn (hH.eigenvalues i)) : ℂ))).trace := by
  classical
  let D := Matrix.diagonal (fun i : Fin n => ((occFn (hH.eigenvalues i)) : ℂ))
  let U := (hH.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℂ)
  have hu : star U * U = 1 := by
    exact Matrix.mem_unitaryGroup_iff'.1 hH.eigenvectorUnitary.2
  have hue : occupiedProjection H hH = U * D * star U := by
    dsimp [U, D]
    simp only [occupiedProjection, Matrix.IsHermitian.cfc, Unitary.conjStarAlgAut_apply]
    congr 1
  rw [hue]
  calc (U * D * star U).trace
      = (U * (D * star U)).trace := by rw [Matrix.mul_assoc]
    _ = ((D * star U) * U).trace := by exact Matrix.trace_mul_comm U (D * star U)
    _ = (D * (star U * U)).trace := by rw [Matrix.mul_assoc]
    _ = (D * 1).trace := by rw [hu]
    _ = D.trace := by rw [Matrix.mul_one]

theorem occupiedProjection_trace_eq_count2 {n : ℕ} (H : Matrix (Fin n) (Fin n) ℂ)
    (hH : H.IsHermitian) :
    (occupiedProjection H hH).trace = (occupiedCount H hH : ℂ) := by
  rw [trace_spec_diag H hH]
  rw [Matrix.trace_diagonal]
  exact sumOcc_eq_count2 H hH

theorem occupiedProjection_trace_int2 {n : ℕ} (H : Matrix (Fin n) (Fin n) ℂ)
    (hH : H.IsHermitian) :
    ∃ N : ℕ, (occupiedProjection H hH).trace = (N : ℂ) :=
  ⟨occupiedCount H hH, occupiedProjection_trace_eq_count2 H hH⟩

end MUFPF