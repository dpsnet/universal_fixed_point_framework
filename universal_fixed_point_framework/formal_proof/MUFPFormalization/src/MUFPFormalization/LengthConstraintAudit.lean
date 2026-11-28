/-
  LengthConstraintAudit.lean — R-n：「保长度」约束把耦合块从 4 个自由参数降到 1 个角
  =====================================================================================

## 问题

§28 判：耦合块 `B = α·1 + β·F + γ·S + δ·A` 的 4 个参数都有库内身份，但经框架平均
（`groupAverage`）只剩 `α`、`δ` 两个，且两者的大小都没有判据。§29（R-m）又判：
`α` 的不变群 ⊇ `GL(2)`，`δ` 的不变群 ⊇ `SO(2)`——**`δ` 的判据不可能来自「任意基变换下的不变性」，
只能来自「保长度」结构**。

于是有唯一的自然入口：对耦合块施加「保长度」约束（`BᵀB = 1` 且 `det B = 1`，即 `B ∈ SO(2)`），
看 4 个参数剩几个。

## 判据与答案

**判①：保长度 ⟹ 只剩 `α`、`δ`，且两者被绑成一条圆。**

`BᵀB = 1 ∧ det B = 1` ⟹ `β = γ = 0`、`B = α·1 + δ·A`、`α² + δ² = 1`。
（证明的关键恒等式：由两条正交列方程与 `det = 1`，得
`(B₀₀−B₁₁)² + (B₀₁+B₁₀)² = 2 − 2·det B = 0`，故 `B₀₀ = B₁₁`、`B₀₁ = −B₁₀`。）

**判②：保长度的耦合块恰是 `groupAverage` 的不动点。**

`B ∈ SO(2)` ⟹ `groupAverage B = B`。即耦合块不再有任何「被平均抹掉」的分量。

**判③：两个判据指向同一子空间。**

框架平均抹掉的（`β·F + γ·S`，对称无迹 2 维）与保长度排除的（`β`、`γ`）
是**同一个** 2 维子空间。故「保长度」不是外来附加条件，而是把框架已有的正交投影
（`groupAverage` 本身是正交投影）的要求延伸到耦合块上。

## 净结果

> 4 参数 →（保长度）→ 2 参数且**不独立**（`α² + δ² = 1`）→ **1 个自由角 `θ`**。
> 也就是说：`α`、`δ` 的大小不再是两个独立的无判据数，而是一个角的两条分量。

这把 §28 的「两个大小都无判据」降到「一个角无判据」。剩下的开口因此明确为：
**`θ` 的内生来源**——不是「两个数怎么定」，而是「这一个角由什么定」。

## 诚实边界

1. 「保长度」是**新提出的结构要求**，不是框架已有定理。本批只证明「若接受该要求，则 4 → 1」，
   不声称框架必须接受它；是否接受留待理论裁决（与 §24.6、§27.6 同级的开口）。
2. 只证 `SO(2)`（`det = 1`）分支；`det = −1` 的反射分支未展开（那会给 `δ` 翻号，见 R-m）。
3. 角 `θ` 的具体生成机制（相位/时间耦合等）本批不做，不做任何猜测性连接。
4. 不新增常数、不新增公设。
-/

import MUFPFormalization.DeltaInvarianceAudit
import Mathlib.Tactic

namespace MUFPF.LengthConstraintAudit

open MUFPF.DeltaInvarianceAudit (alp dlt)
open MUFPF.IntertwinerRepairAudit (rotGen offDiag groupAverage_general_form)
open MUFPF.Isotropy (groupAverage F)
open MUFPF.CouplingDecompAudit (avg_kills_symmetric_traceless)

/-- `β(X) := (X₀₀ − X₁₁)/2`：`F`（分谱差）方向的系数。 -/
noncomputable def bta (X : Matrix (Fin 2) (Fin 2) ℝ) : ℝ := (X 0 0 - X 1 1) / 2

/-- `γ(X) := (X₀₁ + X₁₀)/2`：`S`（对称非对角）方向的系数。 -/
noncomputable def gma (X : Matrix (Fin 2) (Fin 2) ℝ) : ℝ := (X 0 1 + X 1 0) / 2

/-- ★★ **判①**：`BᵀB = 1 ∧ det B = 1` ⟹ 耦合块是「旋转形」：
    `β = γ = 0`、`B = α·1 + δ·A`、且 `α² + δ² = 1`（一条圆）。

    证明骨架：由 `BᵀB = 1` 的两条列方程与 `det B = 1` 直接得
    `(B₀₀−B₁₁)² + (B₀₁+B₁₀)² = 0`（因为两者之和 = `2 − 2·det B`），
    故两个平方项各自为零 ⟹ `B₀₀ = B₁₁`、`B₀₁ = −B₁₀`；再代回列方程即得圆关系。 -/
theorem orth_forces_rotation_form (B : Matrix (Fin 2) (Fin 2) ℝ)
    (hgram : B.transpose * B = 1) (hdet : Matrix.det B = 1) :
    bta B = 0 ∧ gma B = 0 ∧
      (alp B * alp B + dlt B * dlt B = 1) ∧
      B = alp B • (1 : Matrix (Fin 2) (Fin 2) ℝ) + dlt B • rotGen := by
  -- 两条列方程与行列式
  have h00 : B 0 0 * B 0 0 + B 1 0 * B 1 0 = 1 := by
    have := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 0 0) hgram
    simpa [Matrix.mul_apply, Fin.sum_univ_two, Matrix.transpose_apply] using this
  have h11 : B 0 1 * B 0 1 + B 1 1 * B 1 1 = 1 := by
    have := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 1 1) hgram
    simpa [Matrix.mul_apply, Fin.sum_univ_two, Matrix.transpose_apply] using this
  have hdet' : B 0 0 * B 1 1 - B 0 1 * B 1 0 = 1 := by
    simpa [Matrix.det_fin_two] using hdet
  -- 关键恒等式：两个平方项之和为零
  have hsum : (B 0 0 - B 1 1) * (B 0 0 - B 1 1) + (B 0 1 + B 1 0) * (B 0 1 + B 1 0) = 0 := by
    nlinarith [h00, h11, hdet']
  have hs1 : (B 0 0 - B 1 1) * (B 0 0 - B 1 1) = 0 := by
    nlinarith [hsum, mul_self_nonneg (B 0 0 - B 1 1), mul_self_nonneg (B 0 1 + B 1 0)]
  have hs2 : (B 0 1 + B 1 0) * (B 0 1 + B 1 0) = 0 := by
    nlinarith [hsum, mul_self_nonneg (B 0 0 - B 1 1), mul_self_nonneg (B 0 1 + B 1 0)]
  have hb1 : B 0 0 = B 1 1 := by
    rcases mul_eq_zero.mp hs1 with h | h <;> linarith
  have hb2 : B 0 1 = -B 1 0 := by
    rcases mul_eq_zero.mp hs2 with h | h <;> linarith
  -- 圆关系
  have hcirc : alp B * alp B + dlt B * dlt B = 1 := by
    simp only [alp, dlt]
    nlinarith [h00, hb1, hb2]
  -- 旋转形
  have hform : B = alp B • (1 : Matrix (Fin 2) (Fin 2) ℝ) + dlt B • rotGen := by
    ext i j
    fin_cases i <;> fin_cases j <;> simp [alp, dlt, rotGen, hb1, hb2] <;> ring
  refine ⟨?_, ?_, hcirc, hform⟩
  · simp only [bta]
    linarith
  · simp only [gma]
    linarith

/-- ★★ **判②**：保长度的耦合块是 `groupAverage` 的**不动点**：`groupAverage B = B`。
    即耦合块不再含任何「被平均抹掉」的分量。 -/
theorem isometry_is_fixed_by_average (B : Matrix (Fin 2) (Fin 2) ℝ)
    (hgram : B.transpose * B = 1) (hdet : Matrix.det B = 1) :
    groupAverage B = B := by
  obtain ⟨-, -, -, hform⟩ := orth_forces_rotation_form B hgram hdet
  rw [groupAverage_general_form]
  simp only [alp, dlt] at hform ⊢
  rw [← hform]

/-- ★★ **判③**：两个判据指向同一子空间——框架平均抹掉的 `β·F + γ·S`（对称无迹 2 维）
    与保长度排除的 `β`、`γ` 是同一件事。 -/
theorem average_and_isometry_share_kernel :
    (∀ β γ : ℝ, groupAverage (β • F + γ • offDiag) = 0) ∧
      (∀ B : Matrix (Fin 2) (Fin 2) ℝ, B.transpose * B = 1 → Matrix.det B = 1 →
        bta B = 0 ∧ gma B = 0) := by
  refine ⟨?_, ?_⟩
  · exact avg_kills_symmetric_traceless
  · intro B hgram hdet
    obtain ⟨hb, hg, -⟩ := orth_forces_rotation_form B hgram hdet
    exact ⟨hb, hg⟩

/-- **R-n 判决汇总**：`SO(2)` 约束下
    ① `β = γ = 0`；
    ② `B = α·1 + δ·A` 且 `α² + δ² = 1`（4 参数 → 1 个角）；
    ③ `groupAverage B = B`（耦合块落在平均的固定集）；
    ④ 平均抹掉的子空间与保长度排除的子空间相同。 -/
theorem length_constraint_verdict :
    (∀ B : Matrix (Fin 2) (Fin 2) ℝ, B.transpose * B = 1 → Matrix.det B = 1 →
      bta B = 0 ∧ gma B = 0 ∧
        (alp B * alp B + dlt B * dlt B = 1) ∧
        groupAverage B = B ∧
        B = alp B • (1 : Matrix (Fin 2) (Fin 2) ℝ) + dlt B • rotGen) := by
  intro B hgram hdet
  obtain ⟨hb, hg, hcirc, hform⟩ := orth_forces_rotation_form B hgram hdet
  exact ⟨hb, hg, hcirc, isometry_is_fixed_by_average B hgram hdet, hform⟩

end MUFPF.LengthConstraintAudit
