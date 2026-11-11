/-
PR-634 · R5.1 机检化（第一步）

把 `A` 的交换子作用 `X ↦ A * X - X * A` 提升为 ℂ-线性映射，
并按 D25 定义「defect 可穿越性」：存在非零 R 落在 `im(ad_A)`。

本模块**只新增**定义，不改动 `SpCategory.lean` / `HigherSpCategory.lean`。
-/
import Mathlib.Data.Complex.Basic
import Mathlib.LinearAlgebra.Matrix.ConjTranspose
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

/-! ### C 相判定：谱不交 ⇒ 层 2 平凡（跨对象算子） -/

/-- C 相代表：谱 `(4,5,6)`，与 `diag3` 的 `(1,2,3)` 不相交。 -/
abbrev diag4Val : Fin 3 → ℂ := ![4, 5, 6]

/-- C 相矩阵 `diag(4,5,6)`（显式矩阵，同 `diag3` 的理由）。 -/
abbrev diag4 : Matrix (Fin 3) (Fin 3) ℂ := Matrix.of ![![4, 0, 0], ![0, 5, 0], ![0, 0, 6]]

/-- **跨对象交换子作用**：`X ↦ A * X - X * B`（源对象 `A`、目标对象 `B`）。
    这才是层塔 condition 的真实形态——`β.homotopy - α.homotopy = X.A * h - h * Y.A`
    （`HigherSpCategory.lean` L246）源、目标各出一个矩阵；`adLin A` 只是 `A = B` 的退化特例。 -/
def adLin2 (A B : Matrix ι ι ℂ) : Matrix ι ι ℂ →ₗ[ℂ] Matrix ι ι ℂ where
  toFun X := A * X - X * B
  map_add' X Y := by
    rw [Matrix.mul_add, Matrix.add_mul]
    abel
  map_smul' c X := by
    rw [Matrix.mul_smul, Matrix.smul_mul, ← smul_sub]
    rfl

lemma diag4_mul_apply (X : Matrix (Fin 3) (Fin 3) ℂ) (i j : Fin 3) :
    (diag4 * X) i j = diag4Val i * X i j := by
  rw [Matrix.mul_apply]
  fin_cases i
  all_goals simp [Matrix.of_apply, Fin.sum_univ_succ]

/-- 谱 `(4,5,6)` 与 `(1,2,3)` 不交 ⇒ 任意分量差非零（Sylvester 可逆性的全部内容）。 -/
lemma diag4Val_sub_diag3Val_ne_zero (i j : Fin 3) : diag4Val i - diag3Val j ≠ 0 := by
  fin_cases i <;> fin_cases j <;> (simp [diag4Val, diag3Val]; norm_num)

/-- **C 相层 2 平凡**：`ker(adLin2 diag4 diag3) = ⊥`。
    即不存在非零 `h` 满足 `diag4 * h - h * diag3 = 0`——这正是「谱不交 ⇒ 层 2 无 defect 可承接」。
    与 R1 表第一行（C 相塔高 1）一致，且把「`ker H = 0`」的判据落到跨对象算子本身，而非 `A` 自身可逆。 -/
theorem diag4_diag3_ker_eq_bot : LinearMap.ker (adLin2 diag4 diag3) = ⊥ := by
  rw [Submodule.eq_bot_iff]
  intro R hR
  rw [LinearMap.mem_ker] at hR
  ext i j
  have h : diag4Val i * R i j - R i j * diag3Val j = 0 := by
    have h0 := congrArg (fun M : Matrix (Fin 3) (Fin 3) ℂ => M i j) hR
    simpa [adLin2, LinearMap.coe_mk, AddHom.coe_mk, Pi.sub_apply, Matrix.sub_apply,
      diag4_mul_apply, mul_diag3_apply, Matrix.zero_apply] using h0
  have hmul : (diag4Val i - diag3Val j) * R i j = 0 := by
    calc (diag4Val i - diag3Val j) * R i j
        = diag4Val i * R i j - diag3Val j * R i j := by ring
      _ = diag4Val i * R i j - R i j * diag3Val j := by ring
      _ = 0 := h
  exact (mul_eq_zero.mp hmul).resolve_left (diag4Val_sub_diag3Val_ne_zero i j)

/-! ### 三相代表与论文自伴层 `Sp` 的归属（D31） -/

/-- **A 相代表落在自伴层内**：`diag3` 等于自身的共轭转置。
    即 A 相（`ker H ≠ 0`、`ker H ∩ im H = 0`、塔高 2）的代表满足论文命题 2.4.4 L211 的自伴条件，
    故 `⟨3, diag3⟩` 满足 `MUFPF.IsHermitian`（`SpCategory.lean`）。 -/
theorem diag3_conjTranspose_eq : diag3 = Matrix.conjTranspose diag3 := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [diag3, Matrix.conjTranspose_apply, Matrix.of_apply]

/-- **B 相代表不在自伴层内**：`jordan3` 不等于自身的共轭转置。
    `(0,1)` 位为 `1`，而共轭转置的 `(0,1)` 位取 `jordan3 1 0` 的共轭，即 `0`。
    ⇒ `AdTraversable jordan3` 成立，但 `⟨3, jordan3⟩` 不满足 `MUFPF.IsHermitian`：
    B 相的对象属于 `Sp_ℂ`（复谱层），不属于论文 `Sp`（自伴层）。 -/
theorem jordan3_conjTranspose_ne : jordan3 ≠ Matrix.conjTranspose jordan3 := by
  intro h
  have h01 := congrArg (fun M : Matrix (Fin 3) (Fin 3) ℂ => M 0 1) h
  simp [jordan3, Matrix.conjTranspose_apply, Matrix.of_apply] at h01

/-! ### 判据的跨对象统一（D32） -/

/-- **跨对象版可穿越判据**：见证 `R` 同时落在 `ker` 与 `im` 中。
    这是层 3 condition 的原始形态（源对象 `A`、目标对象 `B` 各出一个矩阵给出右端），
    因此 `AdTraversable2` 是三相判据的统一形式；`AdTraversable A` 只是 `A = B`（同谱）的退化特例。 -/
def AdTraversable2 (A B : Matrix ι ι ℂ) : Prop :=
  ∃ R, R ≠ 0 ∧ R ∈ LinearMap.ker (adLin2 A B) ⊓ LinearMap.range (adLin2 A B)

/- 同对象退化：`adLin2 A A = adLin A`。 -/
omit [DecidableEq ι] in
lemma adLin2_self (A : Matrix ι ι ℂ) : adLin2 A A = adLin A := by
  apply LinearMap.ext
  intro X
  rfl

/- 判据的一致性：同谱（`A = B`）时跨对象判据退化为原判据，两套定义不冲突。 -/
omit [DecidableEq ι] in
theorem AdTraversable2_self_iff (A : Matrix ι ι ℂ) :
    AdTraversable2 A A ↔ AdTraversable A := by
  unfold AdTraversable2 AdTraversable
  rw [adLin2_self]

/-- B 相在跨对象判据下仍可穿越。 -/
theorem jordan3_traversable2 : AdTraversable2 jordan3 jordan3 :=
  (AdTraversable2_self_iff jordan3).mpr jordan3_traversable

/-- A 相在跨对象判据下仍不可穿越。 -/
theorem diag3_not_traversable2 : ¬ AdTraversable2 diag3 diag3 := by
  rw [AdTraversable2_self_iff]
  exact diag3_not_traversable

/-- 跨对象统一判据下的层 3 分离性（与 `layer3_separates_A_B` 同内容，判据侧已统一到 `adLin2`）。 -/
theorem layer3_separates_A_B_cross :
    AdTraversable2 jordan3 jordan3 ∧ ¬ AdTraversable2 diag3 diag3 :=
  ⟨jordan3_traversable2, diag3_not_traversable2⟩

/-! ### 塔高判定的机检二分（D33） -/

/-- **B 相：塔越过层 2**。层 2 有非平凡 2-态射，且层 3 存在非零可穿越见证。 -/
theorem jordan3_extends_past_layer2 :
    HasNontrivialTwoMorphism jordan3 ∧ AdTraversable jordan3 :=
  ⟨jordan3_has_two_morphism, jordan3_traversable⟩

/-- **A 相：塔止于层 2**。层 2 有非平凡 2-态射，但层 3 无任何非零可穿越见证。 -/
theorem diag3_stops_at_layer2 :
    HasNontrivialTwoMorphism diag3 ∧ ¬ AdTraversable diag3 :=
  ⟨diag3_has_two_morphism, diag3_not_traversable⟩

/-- 跨对象判据下的同一二分（B 相侧）。 -/
theorem jordan3_extends_past_layer2_cross :
    HasNontrivialTwoMorphism jordan3 ∧ AdTraversable2 jordan3 jordan3 :=
  ⟨jordan3_has_two_morphism, jordan3_traversable2⟩

/-- **塔高的机检二分**（同一层 2 判据之下）：B 相能继续上升、A 相不能。
    这是「判据能区分 A/B」与「塔高数值不同」之间的第一段连接。
    层 3 以上（直到层 4）的重复适用由 R5.2 的逐层同形性承接（34/34 行、0 差异，`pr634r5homo2.txt`），
    Lean 侧机检覆盖到层 3。 -/
theorem tower_continues_or_stops :
    (HasNontrivialTwoMorphism jordan3 ∧ AdTraversable jordan3) ∧
    (HasNontrivialTwoMorphism diag3 ∧ ¬ AdTraversable diag3) :=
  ⟨jordan3_extends_past_layer2, diag3_stops_at_layer2⟩

/-! ### 自伴层内 `dev ≡ 0` 与非自伴层 `dev ≠ 0`（D34） -/

/-- **自伴层内 `Δ` 恒为零（元素级形式）**：任何落在 `ker ∩ im` 中的矩阵必为零。
    原因链：`diag3` 自伴且已在特征基（对角、谱互异）⇒ `ker = 对角、im = 对角元为零` ⇒ 交为零。
    论文命题 2.4.4 L211 的自伴层 `Sp` 内正对应此情形，故「自伴层内 `Δ ≡ 0` 是定理」.
    未机检环节：`自伴 ⇒ 可酉对角化`（谱定理量级），故此处以「已对角」为前提。 -/
theorem diag3_dev_eq_zero (dev : Matrix (Fin 3) (Fin 3) ℂ)
    (h : dev ∈ LinearMap.ker (adLin diag3) ⊓ LinearMap.range (adLin diag3)) :
    dev = 0 := by
  rw [diag3_ker_inf_range_eq_bot] at h
  rw [Submodule.mem_bot] at h
  exact h

/-- **非自伴层 `Δ` 可以非零**：`jordan3` 自身就落在 `ker ∩ im` 中且不为零。
    这是 D22 分野的对称侧：B 相（含 Jordan 块、非自伴，属 `Sp_ℂ`）确有非零 `Δ`。 -/
theorem jordan3_dev_can_be_nonzero :
    jordan3 ∈ LinearMap.ker (adLin jordan3) ⊓ LinearMap.range (adLin jordan3) ∧
      jordan3 ≠ 0 :=
  ⟨Submodule.mem_inf.mpr ⟨jordan3_mem_ker, jordan3_mem_range⟩, jordan3_ne_zero⟩

/-- **两层的对比合成**：自伴层内 `dev ≡ 0`，非自伴层存在非零 `dev`。
    两条并列即 D22「`Sp` 有两层」在 `Δ` 上的机检形式。 -/
theorem dev_zero_iff_selfadjoint_layer :
    (∀ dev : Matrix (Fin 3) (Fin 3) ℂ,
        dev ∈ LinearMap.ker (adLin diag3) ⊓ LinearMap.range (adLin diag3) → dev = 0) ∧
      (∃ dev : Matrix (Fin 3) (Fin 3) ℂ,
        dev ∈ LinearMap.ker (adLin jordan3) ⊓ LinearMap.range (adLin jordan3) ∧ dev ≠ 0) :=
  ⟨diag3_dev_eq_zero, ⟨jordan3, jordan3_dev_can_be_nonzero⟩⟩

end MUFPFormalization
