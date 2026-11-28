/-
  CarrierDetAudit.lean — R-v：4×4 分块行列式律落地（补 `DET_4x4_BLOCK_LAW`），并判载体层 `det` 的结局
  =====================================================================================

## 问题

§36（R-t）在 2×2 耦合块上判 `det ≡ 1`；§37（R-u）把量化的残余结构查完。两批都在同一处留了开口：

> 4×4 载体 `blk A B C D` 的整体 `det` **未查**——分块乘法律 `det (blk A B 0 D) = det A · det D`
> 依赖 `fromBlocks` 系列引理，当时未核实，登记为 `DET_4x4_BLOCK_LAW` 待建。

本批把这条律落地，并顺势给出载体层 `det` 的判决。

## 判决（三条，后两条是前一条的推论）

1. **`DET_4x4_BLOCK_LAW` 成立**：`det (blk A B 0 D) = det A · det D`（对**任意** `A B D`）。
   做法：先证 `blk A B 0 D = Matrix.fromBlocks A B 0 D`（逐条目，`fromBlocks` 的四个 `_apply` 引理都是 `rfl` 级 simp），
   再直接引用 Mathlib 的 `Matrix.det_fromBlocks_zero₂₁`。
2. **载体层 `det` 与耦合块无关**：`B` 换成 `B'` 读数不变——`det` 在载体层同样是 `B`-盲的。
   这条比 §36 的 2×2 判决更强：不只是「量化后恒定」，而是「**任何**耦合值都读不到」。
3. **框架实例上载体 `det` 恒为 `0`**：因为物理层 `A_GR = diag(0, 2)` 是**奇异的**（`det = 0`），
   故 `det A · det D = 0 · (1+Δλ_min) = 0`，与 `B` 无关。

## 净结果

载体层两条经典不变量**不对称**：

| 不变量 | 载体层读数 | 是否含层数据 | 是否含耦合 |
| --- | --- | --- | --- |
| `trace` | `4 + Δλ_min`（≠ 0） | 含（`2` 与 `2+Δλ_min` 相加） | 不含 |
| `det` | `0`（恒） | **不含**（被奇异层清零） | 不含 |

所以「换不变量 `det`」这条路在载体层**比在 2×2 层更早死**：不是「恒定但非零」，而是「恒为零」。
唯一还活着的经典不变量是 `trace`，而 `trace` 只能做到「共存」，做不到「传递」——§25 的判决不变。

## 诚实边界

1. 只证 `C = 0`（上块三角）的分块乘法律；`C ≠ 0` 的完整分块行列式**不做**（需要 Schur 补，超出本批目标）。
2. 不判「框架物理层是否应当奇异」——那是物理指认层，`A_GR = diag(0,2)` 是既有登记（§20）。
3. 不改 §24/§25 的判决，只补它们的适用范围：`det` 这条路的两级失败现在都在机检里。
4. 不新增常数、不新增公设。
-/

import MUFPFormalization.LayeredCarrierAudit
import MUFPFormalization.QuarterTurnQuantizationAudit
import Mathlib.Tactic

namespace MUFPF.CarrierDetAudit

open MUFPF.IntertwinerExistenceAudit (diag2)
open MUFPF.LayeredCarrierAudit (blk trace_blk framework_layers_no_trace_obstruction)
open MUFPF.IntertwinerRepairAudit (rotGen)
open MUFPF.GNBridgeAudit (dlmin dlmin_pos)

/-- `blk` 与 Mathlib 的 `Matrix.fromBlocks` 在 `C = 0` 时逐条目相同。 -/
theorem blk_eq_fromBlocks (A B : Matrix (Fin 2) (Fin 2) ℝ) (D : Matrix (Fin 2) (Fin 2) ℝ) :
    blk A B 0 D = Matrix.fromBlocks A B 0 D := by
  ext p q
  rcases p with i | i <;> rcases q with j | j <;> simp [blk]

/-- ★★ **`DET_4x4_BLOCK_LAW`：分块乘法律**。`det (blk A B 0 D) = det A · det D`
    对**任意** `A`、`B`、`D` 成立（`C = 0` 的上块三角情形）。 -/
theorem det_blk_zero_lower_left (A B D : Matrix (Fin 2) (Fin 2) ℝ) :
    Matrix.det (blk A B 0 D) = Matrix.det A * Matrix.det D := by
  rw [blk_eq_fromBlocks, Matrix.det_fromBlocks_zero₂₁]

/-- 对角 2×2 矩阵的行列式：`det (diag2 a b) = a * b`。 -/
theorem det_diag2 (a b : ℝ) : Matrix.det (diag2 a b) = a * b := by
  rw [Matrix.det_fin_two]
  simp [diag2]

/-- 框架物理层 `A_GR = diag(0,2)` 的行列式为 `0`（该层**奇异**）。 -/
theorem framework_gr_det_zero : Matrix.det (diag2 (0 : ℝ) 2) = 0 := by
  rw [det_diag2]; norm_num

/-- 框架范畴层 `A_SM = diag(1, 1+Δλ_min)` 的行列式为 `1 + Δλ_min`。 -/
theorem framework_sm_det : Matrix.det (diag2 (1 : ℝ) (1 + dlmin)) = 1 + dlmin := by
  rw [det_diag2]; ring

/-- ★★ **判②**：载体层 `det` 与耦合块无关——`B` 换成任意 `B'`，读数不变。 -/
theorem carrier_det_blind (A B B' D : Matrix (Fin 2) (Fin 2) ℝ) :
    Matrix.det (blk A B 0 D) = Matrix.det (blk A B' 0 D) := by
  rw [det_blk_zero_lower_left, det_blk_zero_lower_left]

/-- ★★ **判③**：框架实例上载体 `det` 恒为 `0`——被奇异层清零，与 `B` 无关。 -/
theorem carrier_det_vanishes (B : Matrix (Fin 2) (Fin 2) ℝ) :
    Matrix.det (blk (diag2 (0 : ℝ) 2) B 0 (diag2 (1 : ℝ) (1 + dlmin))) = 0 := by
  rw [det_blk_zero_lower_left, framework_gr_det_zero, framework_sm_det]
  ring

/-- 判③ 的四值形态：§31 的四个量化耦合值给出**同一个** `det = 0`。 -/
theorem carrier_det_zero_for_four_values :
    Matrix.det (blk (diag2 (0 : ℝ) 2) (1 : Matrix (Fin 2) (Fin 2) ℝ) 0
        (diag2 (1 : ℝ) (1 + dlmin))) = 0 ∧
      Matrix.det (blk (diag2 (0 : ℝ) 2) (-1 : Matrix (Fin 2) (Fin 2) ℝ) 0
          (diag2 (1 : ℝ) (1 + dlmin))) = 0 ∧
      Matrix.det (blk (diag2 (0 : ℝ) 2) rotGen 0
          (diag2 (1 : ℝ) (1 + dlmin))) = 0 ∧
      Matrix.det (blk (diag2 (0 : ℝ) 2) (-rotGen) 0
          (diag2 (1 : ℝ) (1 + dlmin))) = 0 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · exact carrier_det_vanishes 1
  · exact carrier_det_vanishes (-1)
  · exact carrier_det_vanishes rotGen
  · exact carrier_det_vanishes (-rotGen)

/-- 载体层的迹不为 `0`（对照：`det` 恒零而迹非零）。 -/
theorem carrier_trace_nonzero :
    Matrix.trace (blk (diag2 (0 : ℝ) 2) (1 : Matrix (Fin 2) (Fin 2) ℝ) 0
        (diag2 (1 : ℝ) (1 + dlmin))) ≠ 0 := by
  have h : Matrix.trace (blk (diag2 (0 : ℝ) 2) (1 : Matrix (Fin 2) (Fin 2) ℝ) 0
      (diag2 (1 : ℝ) (1 + dlmin))) = 4 + dlmin := by
    rw [trace_blk]
    have h1 : Matrix.trace (diag2 (0 : ℝ) 2) = (2 : ℝ) := by
      simp [diag2, Matrix.trace, Fin.sum_univ_two]
    have h2 : Matrix.trace (diag2 (1 : ℝ) (1 + dlmin)) = 2 + dlmin := by
      simp [diag2, Matrix.trace, Fin.sum_univ_two]; ring
    rw [h1, h2]; ring
  rw [h]
  intro hz
  have hpos : (0 : ℝ) < 4 + dlmin := by linarith [dlmin_pos]
  linarith

/-- ★★ **判①（不变量不对称）**：载体层 `det` 恒 `0`、`trace` 非 `0` ⟹
    两条经典不变量在载体层地位不同——`det` 被奇异层清零。 -/
theorem det_vs_trace_asymmetry :
    Matrix.det (blk (diag2 (0 : ℝ) 2) (1 : Matrix (Fin 2) (Fin 2) ℝ) 0
        (diag2 (1 : ℝ) (1 + dlmin))) = 0 ∧
      Matrix.trace (blk (diag2 (0 : ℝ) 2) (1 : Matrix (Fin 2) (Fin 2) ℝ) 0
        (diag2 (1 : ℝ) (1 + dlmin))) ≠ 0 :=
  ⟨carrier_det_vanishes 1, carrier_trace_nonzero⟩

/-- **R-v 判决汇总**：
    ① `det (blk A B 0 D) = det A · det D`（`DET_4x4_BLOCK_LAW` 落地）；
    ② 载体 `det` 对耦合 `B` 盲（任意 `B`、`B'` 同读数）；
    ③ 框架实例载体 `det ≡ 0`（奇异层清零），而 `trace = 4 + Δλ_min ≠ 0`。 -/
theorem carrier_det_verdict :
    (∀ A B D : Matrix (Fin 2) (Fin 2) ℝ,
        Matrix.det (blk A B 0 D) = Matrix.det A * Matrix.det D) ∧
      (∀ A B B' D : Matrix (Fin 2) (Fin 2) ℝ,
        Matrix.det (blk A B 0 D) = Matrix.det (blk A B' 0 D)) ∧
      (∀ B : Matrix (Fin 2) (Fin 2) ℝ,
        Matrix.det (blk (diag2 (0 : ℝ) 2) B 0 (diag2 (1 : ℝ) (1 + dlmin))) = 0) ∧
      (Matrix.trace (blk (diag2 (0 : ℝ) 2) (1 : Matrix (Fin 2) (Fin 2) ℝ) 0
        (diag2 (1 : ℝ) (1 + dlmin))) ≠ 0) :=
  ⟨det_blk_zero_lower_left, carrier_det_blind, carrier_det_vanishes, carrier_trace_nonzero⟩

end MUFPF.CarrierDetAudit
