/-
PR-634 · R5.1 机检化（第一步）

把 `A` 的交换子作用 `X ↦ A * X - X * A` 提升为 ℂ-线性映射，
并按 D25 定义「defect 可穿越性」：存在非零 R 落在 `im(ad_A)`。

本模块**只新增**定义，不改动 `SpCategory.lean` / `HigherSpCategory.lean`。
-/
import Mathlib.Data.Complex.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Diagonal
import Mathlib.Data.Fin.VecNotation
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Algebra.Module.LinearMap.Basic
import Mathlib.Algebra.Module.Submodule.Basic
import Mathlib.Tactic.Abel

namespace MUFPFormalization

open Matrix

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- 交换子作用：`X ↦ A * X - X * A`，作为 ℂ-线性映射。
    这是 𝐒𝐩 层塔中贯穿所有层的同一个 `d_A`（`HigherSpCategory.lean` L236–239）。 -/
def adLin (A : Matrix ι ι ℂ) : Matrix ι ι ℂ →ₗ[ℂ] Matrix ι ι ℂ where
  toFun X := A * X - X * A
  map_add' X Y := by
    rw [Matrix.mul_add, Matrix.add_mul]
    abel
  map_smul' c X := by
    rw [Matrix.mul_smul, Matrix.smul_mul, ← smul_sub]
    rfl

/-- **层 2 非平凡性**：存在非零 2-态射，等价于 `ker(ad_A) ≠ ⊥`。
    层 2 的右端是 `Q.P - P.P`，而 P/Q 均满足层 1 交织，故右端为 0；
    此时只要 `ker ≠ 0` 就能取非零 `α.homotopy`。 -/
def HasNontrivialTwoMorphism (A : Matrix ι ι ℂ) : Prop :=
  LinearMap.ker (adLin A) ≠ ⊥

/-- **层 k ≥ 3 的 defect 可穿越性（D25）**：存在非零 `R ∈ ker(ad_A) ⊓ im(ad_A)`。
    右端 `R = β.homotopy - α.homotopy` 本身落在 `ker`（两层 2-态射各自满足层 2 condition，
    其差亦然），因此判据取核像之交，而非单取 `im`。
    注意这**不是**「该层有态射」：`R = 0` 时 x 可取 `ker` 中非零元，但那是层内 loop。 -/
def AdTraversable (A : Matrix ι ι ℂ) : Prop :=
  ∃ R : Matrix ι ι ℂ, R ≠ 0 ∧ R ∈ LinearMap.ker (adLin A) ⊓ LinearMap.range (adLin A)

/-! ### 具体对象：A 相 `diag(1,2,3)` 与 B 相 `J₃` -/

/-- A 相的谱值 `(1, 2, 3)`。 -/
abbrev diag3Val : Fin 3 → ℂ := ![1, 2, 3]

/-- A 相代表：可对角、谱互异 `diag(1,2,3)`。
    写成显式 `Matrix.of`（而非 `Matrix.diagonal`），使元素级证明可复用
    `Matrix.of_apply` + `Fin.sum_univ_succ` 的化简链。 -/
abbrev diag3 : Matrix (Fin 3) (Fin 3) ℂ := Matrix.of ![![1, 0, 0], ![0, 2, 0], ![0, 0, 3]]

/-- B 相代表：单个 3×3 Jordan 块（`ker(ad) ∩ im(ad) ≠ 0`）。 -/
abbrev jordan3 : Matrix (Fin 3) (Fin 3) ℂ := Matrix.of ![![0, 1, 0], ![0, 0, 1], ![0, 0, 0]]

theorem jordan3_ne_zero : jordan3 ≠ 0 := by
  intro h
  have h01 := congrArg (fun M : Matrix (Fin 3) (Fin 3) ℂ => M (0 : Fin 3) (1 : Fin 3)) h
  simp [jordan3, Matrix.of_apply] at h01

/-- B 相：`J₃ ∈ ker(ad_{J₃})`（因为 `[J, J] = 0`）。 -/
theorem jordan3_mem_ker : jordan3 ∈ LinearMap.ker (adLin jordan3) := by
  rw [LinearMap.mem_ker]
  simp [adLin]

/-- B 相：`J₃ ∈ im(ad_{J₃})`，见证 `h = diag(0,1,2)`（逐项 `i² − 2i(i−1) + (i−1)² = 1`）。 -/
theorem jordan3_mem_range : jordan3 ∈ LinearMap.range (adLin jordan3) := by
  refine ⟨Matrix.of ![![0, 0, 0], ![0, 1, 0], ![0, 0, 2]], ?_⟩
  ext i j
  fin_cases i
  all_goals fin_cases j
  all_goals simp [adLin, jordan3, Matrix.of_apply, Matrix.mul_apply, Fin.sum_univ_succ]
  all_goals norm_num

/-- B 相层 3 可穿越：存在非零 `R = J₃ ∈ ker ⊓ range`。 -/
theorem jordan3_traversable : AdTraversable jordan3 :=
  ⟨jordan3, jordan3_ne_zero,
    Submodule.mem_inf.mpr ⟨jordan3_mem_ker, jordan3_mem_range⟩⟩

/-- B 相层 2 非平凡：`ker(ad_{J₃}) ≠ ⊥`（由 `J₃ ∈ ker` 且 `J₃ ≠ 0` 直接给出）。 -/
theorem jordan3_has_two_morphism : HasNontrivialTwoMorphism jordan3 := by
  intro h
  have hmem : jordan3 ∈ (⊥ : Submodule ℂ (Matrix (Fin 3) (Fin 3) ℂ)) := by
    rw [← h]
    exact jordan3_mem_ker
  rw [Submodule.mem_bot] at hmem
  exact jordan3_ne_zero hmem

/-! ### A 相判定：层 2 非平凡、层 3 不可穿越 -/

/-- 对角矩阵从左侧作用的元素式：`(diag3 * X) i j = d i * X i j`。 -/
lemma diag3_mul_apply (X : Matrix (Fin 3) (Fin 3) ℂ) (i j : Fin 3) :
    (diag3 * X) i j = diag3Val i * X i j := by
  rw [Matrix.mul_apply]
  fin_cases i
  all_goals simp [Matrix.of_apply, Fin.sum_univ_succ]

/-- 对角矩阵从右侧作用的元素式：`(X * diag3) i j = X i j * d j`。 -/
lemma mul_diag3_apply (X : Matrix (Fin 3) (Fin 3) ℂ) (i j : Fin 3) :
    (X * diag3) i j = X i j * diag3Val j := by
  rw [Matrix.mul_apply]
  fin_cases j
  all_goals simp [Matrix.of_apply, Fin.sum_univ_succ]

/-- A 相层 2 非平凡：`diag(1,0,0) ∈ ker(ad_{diag3})` 且非零。 -/
theorem diag3_has_two_morphism : HasNontrivialTwoMorphism diag3 := by
  intro hbot
  set D : Matrix (Fin 3) (Fin 3) ℂ := Matrix.of ![![1, 0, 0], ![0, 0, 0], ![0, 0, 0]] with hDdef
  have hDker : D ∈ LinearMap.ker (adLin diag3) := by
    rw [LinearMap.mem_ker]
    change diag3 * D - D * diag3 = 0
    ext i j
    fin_cases i <;> fin_cases j <;>
      simp [hDdef, Matrix.of_apply, Matrix.mul_apply, Fin.sum_univ_succ, Matrix.sub_apply,
        Matrix.zero_apply]
  have hDne : D ≠ 0 := by
    intro hz
    have h00 := congrArg (fun M : Matrix (Fin 3) (Fin 3) ℂ => M 0 0) hz
    simp [hDdef, Matrix.of_apply, Matrix.zero_apply] at h00
  have hmem : D ∈ (⊥ : Submodule ℂ (Matrix (Fin 3) (Fin 3) ℂ)) := by
    rw [← hbot]
    exact hDker
  rw [Submodule.mem_bot] at hmem
  exact hDne hmem

/-- **A 相层 3 不可穿越**（层 3 分离 A/B 的 Lean 侧判据）：
    `ker(ad_{diag3}) ⊓ range(ad_{diag3}) = ⊥`，故不存在非零可穿越 defect。

    论证结构：`R ∈ ker ⊓ range` 时，`R = ad_{diag3}(X)`；对角位 `d_i * X_ii - X_ii * d_i = 0`
    强制 `R_ii = 0`，非对角位 `(d_i - d_j) * R_ij = 0` 且 `d_i ≠ d_j` 强制 `R_ij = 0`。 -/
theorem diag3_ker_inf_range_eq_bot :
    LinearMap.ker (adLin diag3) ⊓ LinearMap.range (adLin diag3) = ⊥ := by
  rw [Submodule.eq_bot_iff]
  intro R hR
  rw [Submodule.mem_inf] at hR
  obtain ⟨hker, hrange⟩ := hR
  obtain ⟨X, hX⟩ := hrange
  have hker' : adLin diag3 R = 0 := LinearMap.mem_ker.mp hker
  have hXe : ∀ i j : Fin 3, diag3Val i * X i j - X i j * diag3Val j = R i j := by
    intro i j
    have h := congrArg (fun M : Matrix (Fin 3) (Fin 3) ℂ => M i j) hX
    simpa [adLin, LinearMap.coe_mk, AddHom.coe_mk, Pi.sub_apply, Matrix.sub_apply,
      diag3_mul_apply, mul_diag3_apply] using h
  have hKe : ∀ i j : Fin 3, diag3Val i * R i j - R i j * diag3Val j = 0 := by
    intro i j
    have h := congrArg (fun M : Matrix (Fin 3) (Fin 3) ℂ => M i j) hker'
    simpa [adLin, LinearMap.coe_mk, AddHom.coe_mk, Pi.sub_apply, Matrix.sub_apply,
      diag3_mul_apply, mul_diag3_apply, Matrix.zero_apply] using h
  ext i j
  by_cases hij : i = j
  · subst hij
    have h0 := hXe i i
    have hz : R i i = 0 := by
      rw [← h0]
      ring
    simpa [Matrix.zero_apply] using hz
  · have h0 := hKe i j
    have hd : diag3Val i - diag3Val j ≠ 0 := by
      revert hij
      fin_cases i <;> fin_cases j <;> simp [diag3Val] <;> norm_num
    have hmul : (diag3Val i - diag3Val j) * R i j = 0 := by
      calc (diag3Val i - diag3Val j) * R i j
          = diag3Val i * R i j - diag3Val j * R i j := by ring
        _ = diag3Val i * R i j - R i j * diag3Val j := by ring
        _ = 0 := h0
    rcases mul_eq_zero.mp hmul with h | h
    · exact absurd h hd
    · simpa [Matrix.zero_apply] using h

/-- A 相层 3 **不可穿越**：`¬ AdTraversable diag3`。
    直接由 `diag3_ker_inf_range_eq_bot` 与「非零」矛盾推出。 -/
theorem diag3_not_traversable : ¬ AdTraversable diag3 := by
  rintro ⟨R, hne, hmem⟩
  rw [diag3_ker_inf_range_eq_bot] at hmem
  rw [Submodule.mem_bot] at hmem
  exact hne hmem

/-- **层 3 是 A 相与 B 相的分离判据**（D24 甲的 Lean 侧定理化）：
    同一塔结构下，`J₃` 的层 3 defect 可穿越、`diag(1,2,3)` 的不可穿越。
    这是「层 2 无法区分 A/B、层 3 才行」的合成命题，把原子级判定连成一条可引用定理。 -/
theorem layer3_separates_A_B :
    AdTraversable jordan3 ∧ ¬ AdTraversable diag3 :=
  ⟨jordan3_traversable, diag3_not_traversable⟩

end MUFPFormalization
