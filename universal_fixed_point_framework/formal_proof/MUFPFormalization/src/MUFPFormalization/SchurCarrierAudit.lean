/-
  SchurCarrierAudit.lean — R-w：一般分块行列式（Schur 补），判 §24「det 0 比特」的条件性
  =====================================================================================

## 问题

§38（R-v）证了三角情形 `det (blk A B 0 D) = det A · det D`，并判「载体层 `det` 恒 `0`」。
但那条律里 `C = 0` 是**§25 自己选定的构造**（只建了单向下耦合）。本批问两件事：

1. `C ≠ 0` 的一般情形，`det` 是多少？
2. §38 那句「`det` 恒零」到底是**奇异层**造成的，还是**`C = 0`** 造成的？

## 答案

- **一般律**：`det (blk A B C D) = det D · det (A − B·⅟D·C)`（`D` 可逆时）。
  Mathlib 有 `Matrix.det_fromBlocks₂₂` 正是这条（围绕右下块的 Schur 补展开）。
- 于是 `B` **只通过 `A − B·⅟D·C` 这一项进入**。`C = 0` 时该项退化为 `A`，`B` 完全消失——
  §38 的「`B`-盲」不只是奇异层的功劳，**一半是 `C = 0` 的构造选择**。
- **框架实例**两个零**各自独立**：`A_GR = diag(0,2)` 奇异使层数据被清零；`C = 0` 使耦合被清零。
  两者叠加才得到 §38 的恒零。
- **`C ≠ 0` 时 `det` 确实能看见 `B`**：见证 `A = D = 1`、`C = 1`，`B = 0` 给 `det = 1`、
  `B = 1` 给 `det = 0`——两个不同读数。

## 净结果（对 §24 的精确化）

> §24 判「换不变量 `det` ⟹ 0 比特」，这条判词**以单向下耦合为载体前提**。
> 在双向耦合（`C ≠ 0`）的载体上，`det` 会随 `B` 变，故不是「0 比特」而是「1 个混合标量」：
> 它把层数据与耦合乘在一起，既不纯也不分。

即：`det` 的问题不是「读不到」，而是「读到的是一团乘积」。这与 §38 的结论不冲突——
§38 说的是「§25 那个载体上恒零」，本批补的是「换载体它就变得能读，但读的是混合量」。

## 诚实边界

1. 一般律只在 `D` 可逆时成立（Mathlib 的 `det_fromBlocks₂₂` 需要 `[Invertible D]`）；
   `A` 侧的对称版本（`det_fromBlocks₁₁`，需 `[Invertible A]`）本批不用，因为框架里 `A_GR` 奇异。
2. 见证用的是最简载体（`A = D = 1`，`C = 1`），**不是**框架实例；框架实例的双向版本
   （`det = det A_SM · det(A_GR − B·⅟A_SM·C)` 的具体数值）**未算**——须先显式构造 `⅟A_SM`，
   留作开口 `TWO_WAY_FRAMEWORK_DET`。
3. 不声称「1 个混合标量能承担桥」；那要看它能否同时拆出 `2` 与 `2+Δλ_min`，本批不做。
4. 不新增常数、不新增公设。
-/

import MUFPFormalization.CarrierDetAudit
import Mathlib.Tactic

namespace MUFPF.SchurCarrierAudit

open MUFPF.IntertwinerExistenceAudit (diag2)
open MUFPF.LayeredCarrierAudit (blk)
open MUFPF.CarrierDetAudit (framework_gr_det_zero framework_sm_det)
open MUFPF.GNBridgeAudit (dlmin dlmin_pos)

/-- `blk` 与 `Matrix.fromBlocks` 在**任意**四块下逐条目相同。 -/
theorem blk_eq_fromBlocks_gen (A B C D : Matrix (Fin 2) (Fin 2) ℝ) :
    blk A B C D = Matrix.fromBlocks A B C D := by
  ext p q
  rcases p with i | i <;> rcases q with j | j <;> simp [blk]

/-- ★★ **一般分块行列式（Schur 补）**：`D` 可逆时
    `det (blk A B C D) = det D · det (A − B·⅟D·C)`。 -/
theorem det_blk_schur (A B C D : Matrix (Fin 2) (Fin 2) ℝ) [Invertible D] :
    Matrix.det (blk A B C D) = Matrix.det D * Matrix.det (A - B * ⅟D * C) := by
  rw [blk_eq_fromBlocks_gen, Matrix.det_fromBlocks₂₂]

/-- ★ **`C = 0` 时 `det` 对 `B` 盲**（一般层数据、`D` 可逆）：
    Schur 项退化为 `A`，`B` 不进读数。 -/
theorem one_way_det_blind (A B B' D : Matrix (Fin 2) (Fin 2) ℝ) [Invertible D] :
    Matrix.det (blk A B 0 D) = Matrix.det (blk A B' 0 D) := by
  rw [det_blk_schur, det_blk_schur]
  simp only [Matrix.mul_zero, sub_zero]

/-- ★★ **判：`C ≠ 0` 时 `det` 随 `B` 变（见证一）**：`A = D = 1`、`C = 1`、`B = 1` ⟹ `det = 0`。 -/
theorem det_sees_coupling_zero :
    Matrix.det (blk (1 : Matrix (Fin 2) (Fin 2) ℝ) (1 : Matrix (Fin 2) (Fin 2) ℝ)
        (1 : Matrix (Fin 2) (Fin 2) ℝ) (1 : Matrix (Fin 2) (Fin 2) ℝ)) = 0 := by
  rw [blk_eq_fromBlocks_gen, Matrix.det_fromBlocks_one₂₂]
  simp

/-- ★★ **判：`C ≠ 0` 时 `det` 随 `B` 变（见证二）**：同层数据、`B = 0` ⟹ `det = 1`。 -/
theorem det_sees_coupling_unchanged :
    Matrix.det (blk (1 : Matrix (Fin 2) (Fin 2) ℝ) (0 : Matrix (Fin 2) (Fin 2) ℝ)
        (1 : Matrix (Fin 2) (Fin 2) ℝ) (1 : Matrix (Fin 2) (Fin 2) ℝ)) = 1 := by
  rw [blk_eq_fromBlocks_gen, Matrix.det_fromBlocks_one₂₂]
  simp

/-- ★★ **判：一般情形下 `det` 不是 `B`-盲**（两读数不同）。 -/
theorem det_not_blind_when_reverse_nonzero :
    Matrix.det (blk (1 : Matrix (Fin 2) (Fin 2) ℝ) (1 : Matrix (Fin 2) (Fin 2) ℝ)
        (1 : Matrix (Fin 2) (Fin 2) ℝ) (1 : Matrix (Fin 2) (Fin 2) ℝ)) ≠
      Matrix.det (blk (1 : Matrix (Fin 2) (Fin 2) ℝ) (0 : Matrix (Fin 2) (Fin 2) ℝ)
        (1 : Matrix (Fin 2) (Fin 2) ℝ) (1 : Matrix (Fin 2) (Fin 2) ℝ)) := by
  rw [det_sees_coupling_zero, det_sees_coupling_unchanged]
  norm_num

/-- 框架范畴层 `A_SM = diag(1, 1+Δλ_min)` 的行列式非零（故可逆）。 -/
theorem framework_sm_det_ne_zero : Matrix.det (diag2 (1 : ℝ) (1 + dlmin)) ≠ 0 := by
  rw [framework_sm_det]
  intro h
  have : (0 : ℝ) < 1 + dlmin := by linarith [dlmin_pos]
  linarith

/-- 框架范畴层的可逆实例（由 `det ≠ 0` 造），使 Schur 律可在框架实例上直接调用。 -/
noncomputable instance instFrameworkSmInvertible : Invertible (diag2 (1 : ℝ) (1 + dlmin)) :=
  Matrix.invertibleOfIsUnitDet _ (isUnit_iff_ne_zero.mpr framework_sm_det_ne_zero)

/-- ★★ **判：框架实例（`C = 0`）经 Schur 律仍得 `0`**，且此时 `B` 根本不进公式。 -/
theorem framework_det_zero_via_schur (B : Matrix (Fin 2) (Fin 2) ℝ) :
    Matrix.det (blk (diag2 (0 : ℝ) 2) B 0 (diag2 (1 : ℝ) (1 + dlmin))) = 0 := by
  rw [det_blk_schur]
  simp only [sub_zero, framework_gr_det_zero, mul_zero]

/-- **R-w 判决汇总**（一般律本身即 `det_blk_schur`）：
    ② `C = 0` ⟹ `B` 盲（§38 的「载体 `det` 恒零」有一半来自这个构造选择）；
    ③ `C ≠ 0` ⟹ `det` 随 `B` 变（见证两个读数 `0` 与 `1`）；
    ④ 框架实例（`C = 0`）经 Schur 律仍得 `0`。 -/
theorem schur_carrier_verdict :
    (∀ A B B' D : Matrix (Fin 2) (Fin 2) ℝ, Invertible D →
        Matrix.det (blk A B 0 D) = Matrix.det (blk A B' 0 D)) ∧
      (Matrix.det (blk (1 : Matrix (Fin 2) (Fin 2) ℝ) (1 : Matrix (Fin 2) (Fin 2) ℝ)
          (1 : Matrix (Fin 2) (Fin 2) ℝ) (1 : Matrix (Fin 2) (Fin 2) ℝ)) ≠
        Matrix.det (blk (1 : Matrix (Fin 2) (Fin 2) ℝ) (0 : Matrix (Fin 2) (Fin 2) ℝ)
          (1 : Matrix (Fin 2) (Fin 2) ℝ) (1 : Matrix (Fin 2) (Fin 2) ℝ))) ∧
      (∀ B : Matrix (Fin 2) (Fin 2) ℝ,
        Matrix.det (blk (diag2 (0 : ℝ) 2) B 0 (diag2 (1 : ℝ) (1 + dlmin))) = 0) :=
  ⟨fun A B B' D hD => @one_way_det_blind A B B' D hD,
    det_not_blind_when_reverse_nonzero, framework_det_zero_via_schur⟩

end MUFPF.SchurCarrierAudit
