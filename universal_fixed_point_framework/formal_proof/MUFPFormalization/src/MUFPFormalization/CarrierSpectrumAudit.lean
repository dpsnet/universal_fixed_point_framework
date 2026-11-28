/-
  CarrierSpectrumAudit.lean — R-y：载体层特征多项式的分块分解（C = 0），并判载体谱是否真持有两层谱
  ==========================================================================================

## 问题

§44 判「谱给出一半」：层内谱（`det (t • 1 − diag2 a b) = (t−a)(t−b)`）在**层内**把两个谱值分开，
但 4×4 载体整体的特征多项式没有算，故「载体层谱 = 两层谱的并」只是散文猜测，
登记为 `CARRIER_CHARPOLY_FACTOR`。本批落地该分解并判它的后果。

## 结果

1. `t • 1 − blk A B 0 D = blk (t • 1 − A) (−B) 0 (t • 1 − D)`（`shift_blk`，两个分块代数引理
   `blk_smul_one`、`blk_sub` 都是逐条目 `rfl` 级 simp）。
2. **`CARRIER_CHARPOLY_FACTOR`（`C = 0`）**：`det (t • 1 − blk A B 0 D) = det (t • 1 − A) · det (t • 1 − D)`
   对**任意** `t`、**任意** `B` 成立（`det_shift_blk`，用 §38 的 `det_blk_zero_lower_left`）。
3. 载体谱**完整持有两层四个根**，且与 `B` 无关：`0`、`2`（物理层）、`1`、`1 + Δλ_min`（范畴层）
   都是载体特征方程的根（`carrier_root_zero` / `carrier_root_two` / `carrier_root_one` /
   `carrier_root_sm`，各自对任意 `B`），四者两两不同（`roots_pairwise_distinct`）。

## 判决

- §44 的「谱给一半」在载体层**升级为「谱给全部、只缺归属」**：载体特征多项式是两层特征多项式之积，
  故其根集恰为两层根集的无序并；四个根齐全、互不相同、且对耦合块 `B` 完全盲（`B` 只在非对角块，
  上块三角的谱与它无关）。
- 因此「载体不足」的最后一层不是**信息缺失**，而是**归属标记**：`{0, 2, 1, 1+Δλ_min}` 这个多重集
  把两层的全部数值都摆出来了，唯独不告诉观察者哪两个属于物理层。而「归属」正是 §34 判为**定义**
  的那类东西（槽标号）。于是断裂的末端与 §22 的 `T`、§34 的符号同型：**不是算不出，是分不开**。

## 诚实边界

1. 只做 `C = 0`（上块三角）情形；`C ≠ 0` 的载体谱须经 Schur 补，本批不做（登记 `CARRIER_SPECTRUM_TWO_WAY`）。
2. 谱以「特征根（`det (t • 1 − M) = 0`）」机检，不引入 `Polynomial` 与 `charpoly` 类型；
   「特征多项式 = 两块之积」在 `det` 逐点层面成立，多项式层面的等式不作主张。
3. 不判「谱读数是不是框架应当采用的那一个」——那是物理指认层。
4. 不新增常数、不新增公设；`Δλ_min` 只引用 `GNBridgeAudit.dlmin`。
-/

import MUFPFormalization.LayeredCarrierAudit
import MUFPFormalization.CarrierDetAudit
import MUFPFormalization.ScalarReadoutAudit
import Mathlib.Tactic

namespace MUFPF.CarrierSpectrumAudit

open MUFPF.IntertwinerExistenceAudit (diag2 dlmin_in_unit_interval)
open MUFPF.LayeredCarrierAudit (blk)
open MUFPF.CarrierDetAudit (det_blk_zero_lower_left)
open MUFPF.ScalarReadoutAudit (det_shift_diag2)
open MUFPF.GNBridgeAudit (dlmin dlmin_pos)

/-! ## 分块代数：单位阵的分块、分块减法 -/

/-- `Fin 2 ⊕ Fin 2` 上的单位阵按两颗 2×2 单位阵分块：`t • 1 = blk (t • 1) 0 0 (t • 1)`。 -/
theorem blk_smul_one (t : ℝ) :
    t • (1 : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ) =
      blk (t • (1 : Matrix (Fin 2) (Fin 2) ℝ)) 0 0 (t • (1 : Matrix (Fin 2) (Fin 2) ℝ)) := by
  ext p q
  rcases p with i | i <;> rcases q with j | j <;>
    simp [blk, Matrix.smul_apply, Matrix.one_apply]

/-- 分块矩阵的减法逐块进行：`blk A B C D − blk A' B' C' D' = blk (A−A') (B−B') (C−C') (D−D')`。 -/
theorem blk_sub (A B C D A' B' C' D' : Matrix (Fin 2) (Fin 2) ℝ) :
    blk A B C D - blk A' B' C' D' = blk (A - A') (B - B') (C - C') (D - D') := by
  ext p q
  rcases p with i | i <;> rcases q with j | j <;>
    simp [blk, Matrix.sub_apply]

/-- 谱平移的分块形式：`t • 1 − blk A B 0 D = blk (t • 1 − A) (−B) 0 (t • 1 − D)`。 -/
theorem shift_blk (t : ℝ) (A B D : Matrix (Fin 2) (Fin 2) ℝ) :
    t • (1 : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ) - blk A B 0 D =
      blk (t • (1 : Matrix (Fin 2) (Fin 2) ℝ) - A) (-B) 0
        (t • (1 : Matrix (Fin 2) (Fin 2) ℝ) - D) := by
  rw [blk_smul_one, blk_sub]
  simp

/-! ## `CARRIER_CHARPOLY_FACTOR`：载体特征行列式 = 两层特征行列式之积 -/

/-- ★★ **`CARRIER_CHARPOLY_FACTOR`（`C = 0`）：载体层特征行列式分解**。
    `det (t • 1 − blk A B 0 D) = det (t • 1 − A) · det (t • 1 − D)`，对**任意** `t`、**任意** `B`。 -/
theorem det_shift_blk (t : ℝ) (A B D : Matrix (Fin 2) (Fin 2) ℝ) :
    Matrix.det (t • (1 : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ) - blk A B 0 D) =
      Matrix.det (t • (1 : Matrix (Fin 2) (Fin 2) ℝ) - A) *
        Matrix.det (t • (1 : Matrix (Fin 2) (Fin 2) ℝ) - D) := by
  rw [shift_blk, det_blk_zero_lower_left]

/-- ★ **物理层的根 `2` 也是载体的根**：`det (2 • 1 − blk A_GR B 0 A_SM) = 0`，对任意 `B`。 -/
theorem carrier_root_two (B : Matrix (Fin 2) (Fin 2) ℝ) :
    Matrix.det ((2 : ℝ) • (1 : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ) -
        blk (diag2 (0 : ℝ) 2) B 0 (diag2 (1 : ℝ) (1 + dlmin))) = 0 := by
  rw [det_shift_blk]
  have h1 : Matrix.det ((2 : ℝ) • (1 : Matrix (Fin 2) (Fin 2) ℝ) - diag2 (0 : ℝ) 2) = 0 := by
    rw [det_shift_diag2]; norm_num
  rw [h1, zero_mul]

/-- ★ **范畴层的根 `1` 也是载体的根**：`det (1 • 1 − blk A_GR B 0 A_SM) = 0`，对任意 `B`。 -/
theorem carrier_root_one (B : Matrix (Fin 2) (Fin 2) ℝ) :
    Matrix.det ((1 : ℝ) • (1 : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ) -
        blk (diag2 (0 : ℝ) 2) B 0 (diag2 (1 : ℝ) (1 + dlmin))) = 0 := by
  rw [det_shift_blk]
  have h2 : Matrix.det ((1 : ℝ) • (1 : Matrix (Fin 2) (Fin 2) ℝ) -
      diag2 (1 : ℝ) (1 + dlmin)) = 0 := by
    rw [det_shift_diag2]; ring
  rw [h2, mul_zero]

/-- ★ **物理层的根 `0` 也是载体的根**：`det (0 • 1 − blk A_GR B 0 A_SM) = 0`，对任意 `B`。 -/
theorem carrier_root_zero (B : Matrix (Fin 2) (Fin 2) ℝ) :
    Matrix.det ((0 : ℝ) • (1 : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ) -
        blk (diag2 (0 : ℝ) 2) B 0 (diag2 (1 : ℝ) (1 + dlmin))) = 0 := by
  rw [det_shift_blk]
  have h1 : Matrix.det ((0 : ℝ) • (1 : Matrix (Fin 2) (Fin 2) ℝ) - diag2 (0 : ℝ) 2) = 0 := by
    rw [det_shift_diag2]; norm_num
  rw [h1, zero_mul]

/-- ★★ **范畴层的根 `1 + Δλ_min` 也是载体的根**：`det ((1+Δλ_min) • 1 − blk …) = 0`，对任意 `B`。 -/
theorem carrier_root_sm (B : Matrix (Fin 2) (Fin 2) ℝ) :
    Matrix.det ((1 + dlmin) • (1 : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ) -
        blk (diag2 (0 : ℝ) 2) B 0 (diag2 (1 : ℝ) (1 + dlmin))) = 0 := by
  rw [det_shift_blk]
  have h2 : Matrix.det ((1 + dlmin) • (1 : Matrix (Fin 2) (Fin 2) ℝ) -
      diag2 (1 : ℝ) (1 + dlmin)) = 0 := by
    rw [det_shift_diag2]
    have hz : ((1 + dlmin) - (1 + dlmin) : ℝ) = 0 := by ring
    rw [hz, mul_zero]
  rw [h2, mul_zero]

/-! ## 四根两两不同 -/

/-- ★★ **载体谱的四个根两两不同**：`0, 2, 1, 1 + Δλ_min`（`4×4` 载体恰有四个根，故这四个就是全部）。 -/
theorem roots_pairwise_distinct :
    (0 : ℝ) ≠ 2 ∧ (0 : ℝ) ≠ 1 ∧ (0 : ℝ) ≠ 1 + dlmin ∧
      (2 : ℝ) ≠ 1 ∧ (2 : ℝ) ≠ 1 + dlmin ∧ (1 : ℝ) ≠ 1 + dlmin := by
  have hpos : 0 < dlmin := dlmin_pos
  have hlt : dlmin < 1 := dlmin_in_unit_interval.2
  refine ⟨by norm_num, by norm_num, by linarith, by norm_num, by linarith, by linarith⟩

/-! ## 汇总判决 -/

/-- **R-y 判决汇总**：
    ① 载体特征行列式分解（`C = 0`，`det_shift_blk`，对任意 `t`、任意 `B` 成立）；
    ② 两层四个谱值 `0, 2, 1, 1+Δλ_min` 全是载体谱的根（各对任意 `B`）；
    ③ 四根两两不同 ⟹ `4×4` 载体的谱**就是**这四根的无序并，且与耦合块 `B` 无关。
    故载体不足的最后一层是「归属标记」，不是「信息缺失」。 -/
theorem carrier_spectrum_verdict :
    (∀ t : ℝ, ∀ A B D : Matrix (Fin 2) (Fin 2) ℝ,
        Matrix.det (t • (1 : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ) - blk A B 0 D) =
          Matrix.det (t • (1 : Matrix (Fin 2) (Fin 2) ℝ) - A) *
            Matrix.det (t • (1 : Matrix (Fin 2) (Fin 2) ℝ) - D)) ∧
      (∀ B : Matrix (Fin 2) (Fin 2) ℝ,
        Matrix.det ((2 : ℝ) • (1 : Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℝ) -
          blk (diag2 (0 : ℝ) 2) B 0 (diag2 (1 : ℝ) (1 + dlmin))) = 0) ∧
      ((0 : ℝ) ≠ 2 ∧ (0 : ℝ) ≠ 1 ∧ (0 : ℝ) ≠ 1 + dlmin ∧
        (2 : ℝ) ≠ 1 ∧ (2 : ℝ) ≠ 1 + dlmin ∧ (1 : ℝ) ≠ 1 + dlmin) :=
  ⟨det_shift_blk, carrier_root_two, roots_pairwise_distinct⟩

end MUFPF.CarrierSpectrumAudit
