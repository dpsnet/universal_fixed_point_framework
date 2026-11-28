/-
MUFPF · 第 86 批 R-s：离散化不救迹差 —— §31 的量化和与 §23–§25 的迹阻塞正交

§31 把耦合块量化成四个值 `{1, −1, rotGen, −rotGen}`；§25 的分层载体把「相似（迹相等）」
换成「共存（迹相加）」。两条线此前没有交叉检查过：**量化耦合块能不能把迹差补上？**

本批用机检回答：不能，且理由是结构性的——对角块决定迹，耦合块根本不在迹里。

- `blk A B C D`（§25）的迹 = `trace A + trace D`，与 `B C` 无关；
- 故 `B` 取四个量化值中的任何一个，迹都不动（四个值逐一列出）；
- 框架实例：`trace diag(0,2) = 2`、`trace diag(1,1+δ) = 2+δ`（`δ = Δλ_min > 0`）⟹ 两层迹不等；
- 结论：离散化不能把 §23/§24 的「迹必须相等」阻塞解开，两条线正交。
-/
import MUFPFormalization.LayeredCarrierAudit
import MUFPFormalization.ChiralityGradingAudit

namespace MUFPF.DiscreteCouplingTraceAudit

open Matrix MUFPF.LayeredCarrierAudit MUFPF.IntertwinerExistenceAudit
  MUFPF.IntertwinerRepairAudit

/-- ★ 判①：迹里没有耦合块。`trace (blk A B C D) = trace A + trace D`，
    对**任意** `B C`（重新表述 §25 的 `trace_blk`，作为本批的审计锚）。 -/
theorem coupling_absent_from_trace (A B C D : Matrix (Fin 2) (Fin 2) ℝ) :
    Matrix.trace (blk A B C D) = Matrix.trace A + Matrix.trace D :=
  trace_blk A B C D

/-- ★ 判②：四个量化耦合值**都不动迹**。`B ∈ {1, −1, rotGen, −rotGen}` 逐一列出。 -/
theorem quantized_couplings_do_not_move_trace (A C D : Matrix (Fin 2) (Fin 2) ℝ) :
    Matrix.trace (blk A 1 C D) = Matrix.trace A + Matrix.trace D ∧
    Matrix.trace (blk A (-1) C D) = Matrix.trace A + Matrix.trace D ∧
    Matrix.trace (blk A rotGen C D) = Matrix.trace A + Matrix.trace D ∧
    Matrix.trace (blk A (-rotGen) C D) = Matrix.trace A + Matrix.trace D :=
  ⟨trace_blk A 1 C D, trace_blk A (-1) C D, trace_blk A rotGen C D, trace_blk A (-rotGen) C D⟩

/-- 判③：框架两层迹不相等。`trace diag(0,2) = 2 ≠ 2 + Δλ_min = trace diag(1,1+Δλ_min)`，
    因 `Δλ_min > 0`。 -/
theorem framework_layer_traces_differ :
    Matrix.trace (diag2 0 2) ≠
      Matrix.trace (diag2 1 (1 + MUFPF.GNBridgeAudit.dlmin)) := by
  have h1 : Matrix.trace (diag2 0 2) = (2 : ℝ) := by
    simp [diag2, Matrix.trace, Fin.sum_univ_two]
  have h2 : Matrix.trace (diag2 1 (1 + MUFPF.GNBridgeAudit.dlmin)) =
      2 + MUFPF.GNBridgeAudit.dlmin := by
    simp [diag2, Matrix.trace, Fin.sum_univ_two]; ring
  have hp := MUFPF.GNBridgeAudit.dlmin_pos
  intro hh
  rw [h1, h2] at hh
  linarith

/-- 判③ 辅助：框架实例的载体迹恒为 `4 + Δλ_min`，与耦合块取值无关。 -/
private theorem framework_trace_fixed (B : Matrix (Fin 2) (Fin 2) ℝ) :
    Matrix.trace (blk (diag2 0 2) B 0
        (diag2 1 (1 + MUFPF.GNBridgeAudit.dlmin))) =
      4 + MUFPF.GNBridgeAudit.dlmin := by
  rw [trace_blk]
  have h1 : Matrix.trace (diag2 0 2) = (2 : ℝ) := by
    simp [diag2, Matrix.trace, Fin.sum_univ_two]
  have h2 : Matrix.trace (diag2 1 (1 + MUFPF.GNBridgeAudit.dlmin)) =
      2 + MUFPF.GNBridgeAudit.dlmin := by
    simp [diag2, Matrix.trace, Fin.sum_univ_two]; ring
  rw [h1, h2]; ring

/-- ★ 判④：框架实例的迹在四个量化耦合值下都等于 `4 + Δλ_min`（一个值，不是四个）。 -/
theorem framework_trace_same_for_all_four :
    Matrix.trace (blk (diag2 0 2) 1 0 (diag2 1 (1 + MUFPF.GNBridgeAudit.dlmin))) =
        4 + MUFPF.GNBridgeAudit.dlmin ∧
      Matrix.trace (blk (diag2 0 2) (-1) 0 (diag2 1 (1 + MUFPF.GNBridgeAudit.dlmin))) =
        4 + MUFPF.GNBridgeAudit.dlmin ∧
      Matrix.trace (blk (diag2 0 2) rotGen 0 (diag2 1 (1 + MUFPF.GNBridgeAudit.dlmin))) =
        4 + MUFPF.GNBridgeAudit.dlmin ∧
      Matrix.trace (blk (diag2 0 2) (-rotGen) 0 (diag2 1 (1 + MUFPF.GNBridgeAudit.dlmin))) =
        4 + MUFPF.GNBridgeAudit.dlmin :=
  ⟨framework_trace_fixed 1, framework_trace_fixed (-1),
    framework_trace_fixed rotGen, framework_trace_fixed (-rotGen)⟩

/-- ★★ **判⑤（R-s 判决）**：§31 的量化与 §23–§24 的迹阻塞**正交**。
    三重合取：
    ① 迹不依赖耦合块（任意 `B C`）；
    ② 框架两层迹差 `2 ≠ 2 + Δλ_min` 依然成立；
    ③ 四个量化耦合值给出同一个迹 `4 + Δλ_min`。
    推论：把耦合块从 4 个实参数压到 1 个比特，**没有**给 §19 的谱交织 / §23–§24 的迹等式
    提供任何新的可解分支——量化改变的是自由度，不是可解性。 -/
theorem discrete_coupling_trace_verdict :
    (∀ A B C D : Matrix (Fin 2) (Fin 2) ℝ,
        Matrix.trace (blk A B C D) = Matrix.trace A + Matrix.trace D) ∧
      (Matrix.trace (diag2 0 2) ≠
        Matrix.trace (diag2 1 (1 + MUFPF.GNBridgeAudit.dlmin))) ∧
      (Matrix.trace (blk (diag2 0 2) rotGen 0
          (diag2 1 (1 + MUFPF.GNBridgeAudit.dlmin))) =
        4 + MUFPF.GNBridgeAudit.dlmin) :=
  ⟨coupling_absent_from_trace, framework_layer_traces_differ, framework_trace_fixed rotGen⟩

end MUFPF.DiscreteCouplingTraceAudit
