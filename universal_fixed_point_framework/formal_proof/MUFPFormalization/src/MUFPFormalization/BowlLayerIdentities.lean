/-
# BowlLayerIdentities.lean — 碗形层锁定候选 {3/512, 7/2048} + 39 第二身份（P7-5e-260aj/ak/an/ao 资产形式化）

形式化目标（碗形链层级判别 245 + 锁定候选 260aj/ak + 39 家族精确链 260an/ao）：
  深阶身份矩阵中碗形层的两个锁定候选与 39 家族链的代数根：

    1/m³ 碗形候选：3/512 = (k_max−5)/2^(k_max+1)     （分子 = k_max−5，分母 = 2^(k_max+1)）
    u²/m³ 候选：   7/2048 = (k_max−1)/2^(k_max+3)    （分子 = k_max−1 静默单元，分母 = 2^(k_max+3)）
    E 分子第二身份：39 = k_max² − 5² = (k_max−5)(k_max+5)   （与第一身份 k_max·5−1 同值）
    双候选关联：   21 = (k_max−5)(k_max−1) = 3·7；分母比 2^(k_max+3)/2^(k_max+1) = 4

数值先证伪记录（先证伪再证明，模式 8）：
  - p7_5e269_pycheck.py（sympy 精确）：14/14 全通过、残差 0。
  覆盖：两碗形候选框架表达、512/2048=2^(k_max+1)/2^(k_max+3)、3=k_max−5、7=k_max−1、
  39 双身份（k_max²−5² 与 k_max·5−1）、21=(k_max−5)(k_max−1)、联合积 21/2²⁰。

关系链：
  KMaxAlgebra.lean 已形式化 k_max=8 代数唯一性（含 silence_unit：7=k_max−1）；
  DeepCoefficientIdentities.lean 已形式化 E=39/2000（Ecoef=(k_max·5−1)/(2⁴·5³)）；
  JLayerIdentities.lean 已形式化 j(2) 层（13=k_max+5、293 三重身份）。
  本文件把碗形层的两个锁定候选升为 Lean 定理，并给出 39 的 k_max²−5² 第二身份——
  即 39 家族链（260an/ao）的代数根：39 同时是 E 分子（镜像 −1 侧）与
  (k_max−5)(k_max+5)（k_max² 与 5² 之差）。
-/

import Mathlib.Tactic
import MUFPFormalization.DeepCoefficientIdentities

open MUFPF.BottTower

namespace MUFPF.BowlLayer

/-! =========================================================
    §1 碗形候选 1/m³：3/512 = (k_max−5)/2^(k_max+1)
   ========================================================= -/

/-- 分母 512 = 2^(k_max+1)。 -/
theorem bowl_den_512 : 2 ^ (k_max + 1) = 512 := by
  norm_num [k_max_value]

/-- 分子 3 = k_max−5。 -/
theorem bowl_num_3 : k_max - 5 = 3 := by
  norm_num [k_max_value]

/-- ★ 锁定候选框架表达：3/512 = (k_max−5)/2^(k_max+1)（碗形层 1/m³）。 -/
theorem bowl_3512 : (k_max - 5 : ℚ) / ((2 : ℚ) ^ (k_max + 1)) = 3 / 512 := by
  norm_num [k_max_value]

/-! =========================================================
    §2 碗形候选 u²/m³：7/2048 = (k_max−1)/2^(k_max+3)
   ========================================================= -/

/-- 分母 2048 = 2^(k_max+3)。 -/
theorem bowl_den_2048 : 2 ^ (k_max + 3) = 2048 := by
  norm_num [k_max_value]

/-- 分子 7 = k_max−1（静默单元，KMaxAlgebra.silence_unit 同值独立证）。 -/
theorem bowl_num_7 : k_max - 1 = 7 := by
  norm_num [k_max_value]

/-- ★ 锁定候选框架表达：7/2048 = (k_max−1)/2^(k_max+3)（碗形层 u²/m³）。 -/
theorem bowl_72048 : (k_max - 1 : ℚ) / ((2 : ℚ) ^ (k_max + 3)) = 7 / 2048 := by
  norm_num [k_max_value]

/-! =========================================================
    §3 E 分子 39 的第二身份（k_max²−5²）
   ========================================================= -/

/-- 39 = k_max² − 5²（k_max² 与 5² 之差）。 -/
theorem e39_square : k_max ^ 2 - 5 ^ 2 = 39 := by
  norm_num [k_max_value]

/-- 39 = (k_max−5)(k_max+5)（因式分解形式）。 -/
theorem e39_factor : (k_max - 5) * (k_max + 5) = 39 := by
  norm_num [k_max_value]

/-- 39 的第一身份（镜像 −1 侧）：k_max·5−1 = 39（与 DeepCoeff.Ecoef 分子一致）。 -/
theorem e39_first_identity : k_max * 5 - 1 = 39 := by
  norm_num [k_max_value]

/-- ★ 双身份同值：k_max²−5² = k_max·5−1（39 家族链代数根：镜像身份与平方差身份一致）。 -/
theorem e39_dual_identity : k_max ^ 2 - 5 ^ 2 = k_max * 5 - 1 := by
  norm_num [k_max_value]

/-! =========================================================
    §4 双候选关联：21 与分母比
   ========================================================= -/

/-- 21 = (k_max−5)(k_max−1)（碗形双候选分子积）。 -/
theorem bowl21 : (k_max - 5) * (k_max - 1) = 21 := by
  norm_num [k_max_value]

/-- 21 = 3·7（数值形式）。 -/
theorem bowl21_num : 3 * 7 = 21 := by
  norm_num

/-- 分母比：2^(k_max+3)/2^(k_max+1) = 4（两碗形候选间隔 2 个 2 幂层）。 -/
theorem bowl_ratio_4 : (2 : ℚ) ^ (k_max + 3) / (2 : ℚ) ^ (k_max + 1) = 4 := by
  norm_num [k_max_value]

/-- 联合积：(3/512)·(7/2048) = 21/2²⁰。 -/
theorem bowl_product : (3 / 512) * (7 / 2048) = 21 / 2 ^ 20 := by
  norm_num

end MUFPF.BowlLayer
