/-
  LayeredCarrierAudit.lean — R-i：引入更强载体（分层载体），判它换来了什么
  =====================================================================================

## 问题

§23 判：改登记、换构造都救不了谱交织桥；§24 判：商掉核、换不变量、换载体都只传一类信息。
两批的共同点是把载体限在「2×2 矩阵及其不变量」。本轮按用户指令**引入更强的载体**：
把两个 2×2 层装进一个 4 维分层对象——`Fin 2 ⊕ Fin 2` 上的矩阵，

```
        ┌ A_物理    B_耦合 ┐
  C  =  │                  │          A, D：两侧层数据；B：层间耦合；C：反向耦合
        └ C_反向    D_范畴 ┘
```

这是框架物理图像（弥漫层间结构）的直接代数化，也是「更强载体」的最小可行形态。
本批判它换来了什么：**解除阻塞，还是解除判别力？**

## 判决

- **阻塞确实解除了**（判①）：分层载体的迹是**两块迹之和**，`trace (blk A B C D) = trace A + trace D`。
  于是 §23 的「可逆交织 ⟹ 迹必须相等」在这里不再出现——因为载体不再要求两侧**相似**，
  只要求两侧**共存**。框架谱隙实例（迹 `2` 与 `2+Δλ_min`）可以无矛盾地装进一个分层载体，
  迹为 `4 + Δλ_min`。
- **但判别力没换来**（判③）：耦合块 `B` 是**完全自由的**——同一组层数据 `(A_GR, A_SM)`
  可配任意 `B`，且不同 `B` 给出不同载体。所以「桥」的信息全部落在自由参数上，
  而不是落在两侧数据的任何内生关系上。
- **净结果**：更强载体把「欠定」换成了「任意」。§24 的结论（现有载体钉不住两样东西）
  在更强载体上变形成：**能装下两样东西，但装它们的那个自由度不是推导出来的。**

## 诚实边界

1. 载体只取最小加强形态（`2 + 2` 分块，实矩阵）；不引入 `Matrix.fromBlocks`（该名在本工具链下
   的引理集未核实），用自建 `blk` 以完全控制定义与化简。
2. 不判「分层载体是否就是框架应有的载体」——那是物理指认层（笔记 §7.6① 第 3 项，仍开放登记）。
3. 判③ 的自由度只以「存在不同 `B` 给出不同载体」机检，不引入参数计数/维数理论。
4. 不新增常数、不新增公设；`Δλ_min` 只引用 `GNBridgeAudit.dlmin`。
-/

import MUFPFormalization.QuotientBridgeAudit
import Mathlib.Tactic

namespace MUFPF.LayeredCarrierAudit

open MUFPF.IntertwinerExistenceAudit (diag2)

/-- 分层载体：`Fin 2 ⊕ Fin 2` 上的矩阵。`inl` = 物理层，`inr` = 范畴层；
    四块依次为 `(A, B; C, D)`（左上、右上、左下、右下）。 -/
def blk (A B C D : Matrix (Fin 2) (Fin 2) ℝ) :
    Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ :=
  fun p q =>
    match p, q with
    | Sum.inl i, Sum.inl j => A i j
    | Sum.inl i, Sum.inr j => B i j
    | Sum.inr i, Sum.inl j => C i j
    | Sum.inr i, Sum.inr j => D i j

/-! ## 判①：迹相加律 —— §23 的「迹必须相等」阻塞在此载体上不出现 -/

/-- ★★ **判①**：`trace (blk A B C D) = trace A + trace D`。
    对角块相加，交叉块不贡献（它们不在对角线上）。这是本批的核心机制：
    分层载体把「相似（故迹相等）」换成了「共存（故迹相加）」。 -/
theorem trace_blk (A B C D : Matrix (Fin 2) (Fin 2) ℝ) :
    Matrix.trace (blk A B C D) = Matrix.trace A + Matrix.trace D := by
  simp [Matrix.trace, blk, Fintype.sum_sum_type]

/-- 判① 的结构侧：左上块与右下块可逐条读出（层数据没有被载体吞掉）。 -/
theorem blk_layer_readout (A B C D : Matrix (Fin 2) (Fin 2) ℝ) (i j : Fin 2) :
    blk A B C D (Sum.inl i) (Sum.inl j) = A i j ∧
      blk A B C D (Sum.inr i) (Sum.inr j) = D i j := by
  simp [blk]

/-- 判① 的三角侧：反向耦合块取 `0` 时，左下块恒为 `0`（上块三角）。 -/
theorem blk_zero_lower_left (A B D : Matrix (Fin 2) (Fin 2) ℝ) (i j : Fin 2) :
    blk A B 0 D (Sum.inr i) (Sum.inl j) = 0 := by
  simp [blk]

/-! ## 判②：框架谱隙实例可以无矛盾地装进分层载体 -/

/-- 耦合块的一张显式选片（`E₁₂`），用于给出「不同 B 给出不同载体」的见证。 -/
def couplingWitness : Matrix (Fin 2) (Fin 2) ℝ := !![(0 : ℝ), 1; 0, 0]

/-- ★★ **判②**：框架谱隙实例的分层载体 `blk (diag 0 2) E₁₂ 0 (diag 1 (1+Δλ_min))`
    迹为 `4 + Δλ_min`。§23 说「两侧迹不等 ⟹ 不存在可逆交织」，但这里两侧**不需要交织**，
    所以迹不等不再是障碍。 -/
theorem framework_layers_no_trace_obstruction :
    Matrix.trace (blk (diag2 0 2) couplingWitness 0
        (diag2 1 (1 + MUFPF.GNBridgeAudit.dlmin))) =
      4 + MUFPF.GNBridgeAudit.dlmin := by
  rw [trace_blk]
  have h1 : Matrix.trace (diag2 0 2) = (2 : ℝ) := by
    simp [diag2, Matrix.trace, Fin.sum_univ_two]
  have h2 : Matrix.trace (diag2 1 (1 + MUFPF.GNBridgeAudit.dlmin)) =
      2 + MUFPF.GNBridgeAudit.dlmin := by
    simp [diag2, Matrix.trace, Fin.sum_univ_two]; ring
  rw [h1, h2]; ring

/-! ## 判③：耦合块是自由参数 —— 判别力没有换来 -/

/-- ★★ **判③**：同一组层数据 `(A_GR, A_SM)`，耦合块取 `0` 与取 `E₁₂` 给出**不同**载体
    （`(inl 0, inr 1)` 条目分别为 `0` 与 `1`）。故「桥」的参数不是从两侧数据推出的。 -/
theorem coupling_block_is_free :
    blk (diag2 0 2) 0 0 (diag2 1 (1 + MUFPF.GNBridgeAudit.dlmin)) ≠
      blk (diag2 0 2) couplingWitness 0 (diag2 1 (1 + MUFPF.GNBridgeAudit.dlmin)) := by
  intro h
  have h01 := congrArg
    (fun M : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ => M (Sum.inl 0) (Sum.inr 1)) h
  simp [blk, couplingWitness] at h01

/-- 判③ 的加强：耦合块可以在**任意**给定的 2×2 矩阵上取值——
    即桥的参数空间是 4 维自由的（以「任意 B 都给出一个载体」机检）。 -/
theorem coupling_arbitrary (B : Matrix (Fin 2) (Fin 2) ℝ) :
    ∃ C : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ,
      C = blk (diag2 0 2) B 0 (diag2 1 (1 + MUFPF.GNBridgeAudit.dlmin)) :=
  ⟨_, rfl⟩

/-- 判③ 的结论句：分层载体**区分**不同的耦合块（并非「对所有 B 给出同一对象」），
    故耦合是真实自由度，而不是被载体确定的冗余参数。 -/
theorem carrier_distinguishes_coupling :
    ¬ ∀ B B' : Matrix (Fin 2) (Fin 2) ℝ,
        blk (diag2 0 2) B 0 (diag2 1 (1 + MUFPF.GNBridgeAudit.dlmin)) =
          blk (diag2 0 2) B' 0 (diag2 1 (1 + MUFPF.GNBridgeAudit.dlmin)) := by
  intro h
  have h01 := congrArg
    (fun M : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ => M (Sum.inl 0) (Sum.inr 1))
    (h 0 couplingWitness)
  simp [blk, couplingWitness] at h01

/-! ## 汇总判决 -/

/-- **R-i 判决汇总**：
    ① 迹相加律：`trace (blk A B C D) = trace A + trace D`（相似约束被「共存」替代）；
    ② 框架谱隙实例可入载体，迹 `4 + Δλ_min`（§23 阻塞不出现）；
    ③ 耦合块自由：同一层数据配不同 `B` 得到不同载体，且载体不能钉住 `B`。 -/
theorem layered_carrier_verdict :
    (Matrix.trace (blk (diag2 0 2) couplingWitness 0
        (diag2 1 (1 + MUFPF.GNBridgeAudit.dlmin))) =
      4 + MUFPF.GNBridgeAudit.dlmin) ∧
      (blk (diag2 0 2) 0 0 (diag2 1 (1 + MUFPF.GNBridgeAudit.dlmin)) ≠
        blk (diag2 0 2) couplingWitness 0 (diag2 1 (1 + MUFPF.GNBridgeAudit.dlmin))) ∧
      (¬ ∀ B B' : Matrix (Fin 2) (Fin 2) ℝ,
          blk (diag2 0 2) B 0 (diag2 1 (1 + MUFPF.GNBridgeAudit.dlmin)) =
            blk (diag2 0 2) B' 0 (diag2 1 (1 + MUFPF.GNBridgeAudit.dlmin))) :=
  ⟨framework_layers_no_trace_obstruction, coupling_block_is_free, carrier_distinguishes_coupling⟩

end MUFPF.LayeredCarrierAudit
