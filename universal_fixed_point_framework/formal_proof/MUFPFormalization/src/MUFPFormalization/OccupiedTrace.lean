import MUFPFormalization.HallEmergence
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Fintype.BigOperators

/-! # OccupiedTrace.lean — 占据投影迹的整数量子化（S615c，2026-11-09）

来源：原 `formal_proof/MUFPFormalization/ProbeTraceMain.lean`（库外探针文件，未纳入构建），
2026-11-09 按"预研/探针成果应自包含进主库"的裁决并入 `src/`，命名空间不变（`MUFPF`）。

补的是 `HallEmergence` 的一个缺口：该模块已有机检 `occupiedProjection` 的 Hermitian 性、
幂等性与 `[H, P] = 0` 交换性，但没有把**迹**与**占据本征值计数**对上。本文件给出：

  occFn_mem                    占据指示函数取值 ∈ {0,1}
  occFn_term_eq2               指示值作为 ℂ 项 = 布尔指示（0/1 二值化）
  sumOcc_eq_count2             迹求和 = 占据计数（求和与计数的桥）
  trace_spec_diag              Tr(occupiedProjection) = Tr(diag(occFn(λ_i)))
                               （经 eigenvectorUnitary 共轭不变性归约为对角迹）
  occupiedProjection_trace_eq_count2
                               Tr(P_occ) = occupiedCount（占据投影迹 = 占据本征值个数）
  occupiedProjection_trace_int2
                               Tr(P_occ) ∈ ℕ（迹为整数）

物理含义：占据投影的迹即填充数，其整数性是把"占据"从定义提升为可测不变量——
Hall 侧量子化（σ_xy 取整数量子）所需的"填充数整数"凭证。注意诚实边界：整数性来自
`occupiedCount` 的 Finset 计数定义经迹归约得到，不构成"迹必为整数"的独立拓扑论证。
-/

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
  have h1 : (∑ i : Fin n, ((occFn (hH.eigenvalues i) : ℝ) : ℂ))
      = ∑ i : Fin n, (if occFn (hH.eigenvalues i) = 1 then (1 : ℂ) else 0) :=
    Finset.sum_congr rfl fun i _ => occFn_term_eq2 H hH i
  rw [h1, Finset.sum_boole]
  simp [occupiedCount]

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
