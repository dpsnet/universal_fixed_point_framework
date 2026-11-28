/-
MUFPF · 第 87 批 R-t：补 §35.6 记下的缺口 —— `det` 判据在四个量化值上也恒定

§35.6 明确记了一条**未做**的检查：「`det` 对 `±1` 与 `±rotGen` 都是 `1`，但本批未机检，
不声称已查」。本批把这个缺口补上。

结果：`det` 在四个值上恒为 `1`。故 §24 的「换不变量 `det`」那条路，在量化之后同样没有新分支——
与 §35 的迹判据一致：**量化对判据免疫，不只是对迹免疫。**

诚实边界（写死在本批边界里）：
- 本批只查 **2×2 耦合块本身** 的 `det`；**不**查 4×4 载体 `blk A B C D` 的整体 `det`
  （分块行列式乘法律 `det = det A · det D`（`C = 0` 时）依赖 `fromBlocks` 系列引理，
  库内 grep 无返回、本项目未自建该律，故**不声称**已查 4×4）。
-/
import MUFPFormalization.ChiralityGradingAudit

namespace MUFPF.DetCriterionAudit

open Matrix MUFPF.IntertwinerRepairAudit

/-- 判①：单位阵 `det = 1`。 -/
theorem det_one_value : Matrix.det (1 : Matrix (Fin 2) (Fin 2) ℝ) = 1 := by
  rw [Matrix.det_fin_two]
  norm_num [Matrix.one_apply]

/-- 判②：`−1` 的 `det = 1`（2×2 整体取负使 `det` 不变号）。 -/
theorem det_neg_one_value : Matrix.det (-1 : Matrix (Fin 2) (Fin 2) ℝ) = 1 := by
  rw [Matrix.det_fin_two]
  norm_num [Matrix.one_apply, Matrix.neg_apply]

/-- 判③：`det rotGen = 1`。 -/
theorem det_rotGen_value : Matrix.det rotGen = 1 := by
  rw [Matrix.det_fin_two]
  norm_num [rotGen]

/-- 判④：`det (−rotGen) = 1`。 -/
theorem det_neg_rotGen_value : Matrix.det (-rotGen) = 1 := by
  rw [Matrix.det_fin_two]
  norm_num [rotGen, Matrix.neg_apply]

/-- ★★ **判⑤（R-t 判决）**：四个量化耦合值的 `det` **全部等于 1** ⟹
    `det` 作为判据在量化后是**常数**，不产生新的可解分支。
    与 §35 的迹判据合起来：量化对这两条判据都免疫。 -/
theorem det_criterion_immunity :
    (Matrix.det (1 : Matrix (Fin 2) (Fin 2) ℝ) = 1) ∧
      (Matrix.det (-1 : Matrix (Fin 2) (Fin 2) ℝ) = 1) ∧
      (Matrix.det rotGen = 1) ∧
      (Matrix.det (-rotGen) = 1) :=
  ⟨det_one_value, det_neg_one_value, det_rotGen_value, det_neg_rotGen_value⟩

end MUFPF.DetCriterionAudit
