/-
  IntertwinerRepairAudit.lean — R-g：修补方案的判决（改登记为「T 可逆」是循环；平均型 T 的像空间 2 维）
  =====================================================================================

## 接在什么后面

第 73 批（R-f）判：`T 存在`（C1 猜想）与「桥有信息」互斥——
谱不交 ⟹ 唯一交织子为 0；谱相同/部分重合 ⟹ T 存在但退化为 0 比特或迹桥断；
框架自己的 T（强制平均）是正交投影 ⟹ 无左逆。
四处真断裂至此全部判完，共同结构是「把功能性要求登记成存在性/数值性命题」。

## 本批判什么

修补方向只有一个：把登记从「∃ T，交织」改成「∃ T 可逆，交织」。本批判这个修补是否可解：

| 编号 | 命题 | 判什么 |
|:--|:--|:--|
| ① | `trace_eq_of_invertible_intertwine_real` | 可逆 + 交织 ⟹ `trace` 相等（实矩阵版，自行机检） |
| ② | `repair_is_circular` | 把结论（迹相等）放回前提 ⟹ 修补后桥是同义反复 |
| ③ | `framework_repair_unsolvable` | 框架谱隙情形 `trace` 不等 ⟹ 该修补**无解** |
| ④ | `groupAverage_general_form` | 强制平均的完整形态（对任意 T，不只是对称 T） |
| ⑤ | `no_left_inverse_two_kernels` | 由 ④ ⟹ 像空间 ⊆ span{1, A}（2 维），核 ⊇ 对称无迹（2 维）⟹ 秩 2，不可逆 |

## 判决

- 改登记为「T 可逆」不产生新判据：可逆交织子的存在性**已经蕴含**迹相等（①），
  而迹相等正是迹桥要证的结论（②）。修补 = 把结论搬进前提，桥退化为同义反复。
- 在需要桥的场合（两侧谱不同），该修补**无解**（③）：框架谱隙实例的 `trace` 差 `Δλ_min > 0`。
- 平均型 T 的失效有机制解释（④⑤）：`groupAverage T = (tr T/2)·1 + ((T₀₁−T₁₀)/2)·A`——
  像空间只有 2 维（标量 + 一个固定反对称标量），对称无迹（各向异性）整块被投影掉，核因此 2 维。
  所以「用平均构造 T」不是「差一点可逆」，而是**结构上秩亏一半**。

## 诚实边界

1. ① 是 `MassEquivalenceBridge.trace_eq_of_intertwine` 的实矩阵版（ℂ 版已有机检）；本模块自行重证以避开
   复数转置/共轭记号，不新增假设。
2. ③ 的「无解」只针对 `A_GR = diag(0,2)`、`A_SM = diag(1, 1+Δλ_min)` 这一框架实例（2×2 谱块），
   不宣称一般情形；一般情形的「可逆交织 ⟺ 相似 ⟺ trace/det 全等」是标准线性代数，本模块不形式化。
3. ④ 是纯代数恒等式（对任意实 2×2 矩阵成立），不依赖群表示论；它同时解释了 `groupAverage_isotropy`
   （对称情形 `T₀₁ = T₁₀` ⟹ 反对称项为 0）。
4. ⑤ 的「秩 2」由 ④ 的显式形态读出（像 ⊆ span{1,A}、核 ⊇ span{F,S}），本模块不引入线性映射的秩定义；
   以「两个线性无关核元素 ⟹ 无左逆」机检（`no_left_inverse_two_kernels`）。
5. 不新增常数、不新增公设；`Δλ_min` 只引用 `GNBridgeAudit.dlmin`。
-/

import MUFPFormalization.IntertwinerExistenceAudit
import MUFPFormalization.MassEquivalenceBridge
import Mathlib.Tactic

namespace MUFPF.IntertwinerRepairAudit

open MUFPF.Isotropy
open MUFPF.IntertwinerExistenceAudit (diag2)

/-- 反对称生成元 `A = !![0, 1; −1, 0]`（= −J；强制平均保留下来的唯一非标量分量）。 -/
def rotGen : Matrix (Fin 2) (Fin 2) ℝ := !![(0 : ℝ), 1; -1, 0]

/-- 对称无迹的第二个基元 `S = !![0, 1; 1, 0]`（与 `F = diag(1,−1)` 一起张成对称无迹 2 维）。 -/
def offDiag : Matrix (Fin 2) (Fin 2) ℝ := !![(0 : ℝ), 1; 1, 0]

/-! ## ① 可逆 + 交织 ⟹ 迹相等（实矩阵版，自行机检） -/

/-- ★★ **判①**：`T` 有双侧逆且 `T·B = A·T` ⟹ `trace B = trace A`。
    （实矩阵版；ℂ 版见 `MassEquivalenceBridge.trace_eq_of_intertwine`。） -/
theorem trace_eq_of_invertible_intertwine_real {A B T U : Matrix (Fin 2) (Fin 2) ℝ}
    (hTU : T * U = 1) (hUT : U * T = 1) (h : T * B = A * T) :
    Matrix.trace B = Matrix.trace A := by
  have hB : B = U * A * T := by
    calc B = 1 * B := by simp
      _ = (U * T) * B := by rw [hUT]
      _ = U * (T * B) := by rw [Matrix.mul_assoc]
      _ = U * (A * T) := by rw [h]
      _ = U * A * T := by rw [Matrix.mul_assoc]
  rw [hB]
  calc Matrix.trace (U * A * T) = Matrix.trace (T * (U * A)) :=
        Matrix.trace_mul_comm (U * A) T
    _ = Matrix.trace (T * U * A) := by rw [Matrix.mul_assoc]
    _ = Matrix.trace (1 * A) := by rw [hTU]
    _ = Matrix.trace A := by simp

/-! ## ② 修补是循环：递推（可逆交织 ⟹ 迹相等）就是桥的结论 -/

/-- ★★ **判②**：把登记改成「∃ T 可逆，交织」后，桥的结论 `trace A_GR = trace A_SM`
    已由前提的代数后果直接给出——修补后桥是同义反复（0 比特），不构成新判据。 -/
theorem repair_is_circular :
    (∀ (A_GR A_SM T U : Matrix (Fin 2) (Fin 2) ℝ),
        T * U = 1 → U * T = 1 → T * A_SM = A_GR * T →
        Matrix.trace A_SM = Matrix.trace A_GR) ∧
      (∀ (A_GR A_SM : Matrix (Fin 2) (Fin 2) ℝ),
        Matrix.trace A_SM ≠ Matrix.trace A_GR →
        ¬ ∃ (T U : Matrix (Fin 2) (Fin 2) ℝ),
            T * U = 1 ∧ U * T = 1 ∧ T * A_SM = A_GR * T) := by
  constructor
  · intro A_GR A_SM T U hTU hUT h
    exact trace_eq_of_invertible_intertwine_real hTU hUT h
  · intro A_GR A_SM htr ⟨T, U, hTU, hUT, h⟩
    exact htr (trace_eq_of_invertible_intertwine_real hTU hUT h)

/-! ## ③ 框架谱隙实例：修补无解 -/

/-- **判③**：框架谱隙实例 `A_GR = diag(0,2)`、`A_SM = diag(1, 1+Δλ_min)`
    的 `trace` 差 `Δλ_min > 0` ⟹ 该修补**无解**（不存在可逆交织子）。 -/
theorem framework_repair_unsolvable :
    ¬ ∃ T U : Matrix (Fin 2) (Fin 2) ℝ,
        T * U = 1 ∧ U * T = 1 ∧
          T * diag2 1 (1 + MUFPF.GNBridgeAudit.dlmin) = diag2 0 2 * T := by
  rintro ⟨T, U, hTU, hUT, h⟩
  have htr := trace_eq_of_invertible_intertwine_real (A := diag2 0 2)
    (B := diag2 1 (1 + MUFPF.GNBridgeAudit.dlmin)) hTU hUT h
  have hpos : 0 < MUFPF.GNBridgeAudit.dlmin := MUFPF.GNBridgeAudit.dlmin_pos
  have h2 : Matrix.trace (diag2 0 2) = (2 : ℝ) := by
    simp [diag2, Matrix.trace, Fin.sum_univ_two]
  have h3 : Matrix.trace (diag2 1 (1 + MUFPF.GNBridgeAudit.dlmin)) =
      (2 : ℝ) + MUFPF.GNBridgeAudit.dlmin := by
    simp [diag2, Matrix.trace, Fin.sum_univ_two]; ring
  rw [h3, h2] at htr
  linarith

/-! ## ④ 强制平均的完整形态（对任意 2×2 矩阵，不只是对称） -/

/-- ★★ **判④**：`groupAverage T = (trace T / 2)·1 + ((T₀₁ − T₁₀)/2)·A`。
    对任意实 2×2 矩阵成立：像空间 ⊆ span{1, A}（2 维），对称无迹分量被整块投影掉。
    （对称输入时 `T₀₁ = T₁₀` ⟹ 反对称项归零 ⟹ `(trace/2)·1`，即 `groupAverage_isotropy`。） -/
theorem groupAverage_general_form (T : Matrix (Fin 2) (Fin 2) ℝ) :
    groupAverage T =
      ((T 0 0 + T 1 1) / 2) • (1 : Matrix (Fin 2) (Fin 2) ℝ) +
        ((T 0 1 - T 1 0) / 2) • rotGen := by
  unfold groupAverage rotGen
  unfold R0 R1 R2 R3
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [rot, Real.cos_pi_div_two, Real.sin_pi_div_two, Real.cos_pi, Real.sin_pi,
      Real.cos_neg, Real.sin_neg, Real.cos_zero, Real.sin_zero, Matrix.mul_apply,
      Matrix.vecMul, Matrix.vecHead, Matrix.vecTail, Matrix.cons_val_zero,
      Fin.sum_univ_two, Matrix.smul_apply, Matrix.add_apply]
  <;> ring

/-! ## ⑤ 秩亏一半：两个线性无关核元素 ⟹ 无左逆 -/

/-- `groupAverage F = 0`（`F = diag(1,−1)`，对称无迹基元一）。 -/
theorem groupAverage_F_zero' : groupAverage F = 0 :=
  MUFPF.IntertwinerExistenceAudit.groupAverage_F_zero

/-- **`groupAverage S = 0`**（`S = !![0,1;1,0]`，对称无迹基元二）。 -/
theorem groupAverage_offDiag_zero : groupAverage offDiag = 0 := by
  rw [groupAverage_general_form]
  simp [offDiag, rotGen]

/-- `S ≠ 0`。 -/
theorem offDiag_ne_zero : offDiag ≠ (0 : Matrix (Fin 2) (Fin 2) ℝ) := by
  intro h
  have hh := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 0 1) h
  simp [offDiag] at hh

/-- `F ≠ S`：两个核元素线性无关（在 (0,0) 条目上分别取 1 与 0）。 -/
theorem F_ne_offDiag : F ≠ offDiag := by
  intro h
  have h00 : F 0 0 = offDiag 0 0 := by rw [h]
  simp [F, offDiag] at h00

/-- **判⑤**：两个不同的非零核元素同时被强制平均湮灭 ⟹ 不存在左逆函数
    （否则 `F` 与 `S` 会被压成同一个 `inv 0`）。即「平均型 T」秩亏、不可逆，且亏的是整个对称无迹块。 -/
theorem no_left_inverse_two_kernels :
    ¬ ∃ inv : (Matrix (Fin 2) (Fin 2) ℝ → Matrix (Fin 2) (Fin 2) ℝ),
        ∀ T : Matrix (Fin 2) (Fin 2) ℝ, inv (groupAverage T) = T := by
  rintro ⟨inv, hinv⟩
  have hF : inv (groupAverage F) = F := hinv F
  have hS : inv (groupAverage offDiag) = offDiag := hinv offDiag
  rw [groupAverage_F_zero'] at hF
  rw [groupAverage_offDiag_zero] at hS
  exact F_ne_offDiag (hF.symm.trans hS)

/-- **R-g 判决汇总**：

    ① 可逆 + 交织 ⟹ 迹相等（实矩阵版）；
    ② 修补后的桥 ≡ 迹相等的重述（递推 + 逆否：迹不等 ⟹ 无解）；
    ③ 框架谱隙实例（迹差 = Δλ_min > 0）该修补无解；
    ④ 强制平均完整形态 = (tr/2)·1 + ((T₀₁−T₁₀)/2)·A（像空间 2 维）；
    ⑤ 平均型 T 有 2 维核 ⟹ 无左逆（秩亏一半，非「差一点可逆」）。 -/
theorem repair_verdict :
    (∀ (A_GR A_SM T U : Matrix (Fin 2) (Fin 2) ℝ),
        T * U = 1 → U * T = 1 → T * A_SM = A_GR * T →
        Matrix.trace A_SM = Matrix.trace A_GR) ∧
      (¬ ∃ T U : Matrix (Fin 2) (Fin 2) ℝ,
          T * U = 1 ∧ U * T = 1 ∧
            T * diag2 1 (1 + MUFPF.GNBridgeAudit.dlmin) = diag2 0 2 * T) ∧
      (groupAverage F = 0 ∧ groupAverage offDiag = 0 ∧ F ≠ offDiag) ∧
      (¬ ∃ inv : (Matrix (Fin 2) (Fin 2) ℝ → Matrix (Fin 2) (Fin 2) ℝ),
          ∀ T : Matrix (Fin 2) (Fin 2) ℝ, inv (groupAverage T) = T) :=
  ⟨fun A_GR A_SM T U hTU hUT h =>
      trace_eq_of_invertible_intertwine_real (A := A_GR) (B := A_SM) (T := T) (U := U)
        hTU hUT h,
   framework_repair_unsolvable,
   ⟨groupAverage_F_zero', groupAverage_offDiag_zero, F_ne_offDiag⟩,
   no_left_inverse_two_kernels⟩

end MUFPF.IntertwinerRepairAudit
