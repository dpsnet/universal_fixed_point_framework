/-
# HPrimeLayerIdentities.lean — h′(2) 层身份 13/600 强候选 + 13 家族分子链（P7-5e-273）

形式化目标（P7-5e-181 h′(2) 提取锁定 + 245 分子链平方迭代 + 260y 同源登记）：
  碗形链第 2 层 h′(2) 的强候选身份与其分子 13 的家族链：

    · 分子 13 三重身份：13 = 2·k_max−3（C 分子）= k_max+5（j 分子）= N_gen²+(N_gen−1)² = 3²+2²
      ——13 同时是 C=13/128 与 h′=13/600 的分子（260y：与 C=13/128 分子同源）；
    · h′(2) = 13/600 = (k_max+5)/(N_gen·k_max·(k_max−3)²)
      （P7-5e-181：h′(2)=0.02166536 锁定级提取 → 13/600 强候选 −0.006%；
       N_gen=3=ActiveMorphismLayer 基数、N′=k_max−3=5 邻居基）；
    · C 分母 2^(k_max−1)=128 vs h′ 分母 600：128/600 = 16/75；
    · h(2)/h′(2) 缩小因子 = (7/64)/(13/600) = 525/104（245 粗候选：≈5.048 近 N′=5，+0.96%）。

★ 诚实边界：
  · h′(2)=13/600 是**强候选**（−0.006%，身份候选非锁定）——提取为锁定级（181），身份为强候选；
  · 缩小因子 525/104≈5.048 是 245 的粗候选（+0.96%），只登记精确有理数恒等，不断言 = N′；
  · i(2)（碗形第 3 层）身份开放（1/173 等无 0.05% 内干净命中）——不形式化。

数值先证伪记录（先证伪再证明，模式 8）：
  - p7_5e273_pycheck.py（sympy 精确）：11/11 全通过、残差 0。

关系链：import JLayerIdentities（13=k_max+5 跨文件）。
-/

import Mathlib.Tactic
import MUFPFormalization.JLayerIdentities

open MUFPF.BottTower

namespace MUFPF.HPrimeLayer

/-! =========================================================
    §1 分子 13 三重身份（C 分子 / j 分子 / 平方和）
   ========================================================= -/

/-- 13 = 2·k_max−3（C 分子，DeepCoeff.Ccoef 分子）。 -/
theorem molecular_13_c : 2 * k_max - 3 = 13 := by
  norm_num [k_max_value]

/-- 13 = k_max+5（j 分子，引用 JLayer.j_numerator_kmax 跨文件链）。 -/
theorem molecular_13_j : k_max + 5 = 13 := by
  exact MUFPF.JLayer.j_numerator_kmax

/-- 13 = N_gen²+(N_gen−1)² = 3²+2²（245 分子链平方迭代起点）。 -/
theorem molecular_13_sq : 3 ^ 2 + 2 ^ 2 = 13 := by
  norm_num

/-- ★ 分子 13 三重身份联合（C 分子 / j 分子 / 平方和——13 家族分子链）。 -/
theorem molecular_13_triple :
    (2 * k_max - 3 = 13) ∧ (k_max + 5 = 13) ∧ (3 ^ 2 + 2 ^ 2 = 13) := by
  norm_num [k_max_value]

/-! =========================================================
    §2 h′(2) = 13/600 强候选
   ========================================================= -/

/-- 邻居基 N′ = k_max−3 = 5（引用 KMaxAlgebra.neighbor_base）。 -/
theorem hp_neighbor_base : k_max - 3 = 5 := by
  exact MUFPF.KMaxAlgebra.neighbor_base

/-- 分母 600 = N_gen·k_max·(k_max−3)²（N_gen=3、k_max=8、N′²=25）。 -/
theorem hp_den_600 : 3 * k_max * (k_max - 3) ^ 2 = 600 := by
  norm_num [k_max_value]

/-- (k_max−3)² = 25（邻居基平方）。 -/
theorem hp_den_neighbor_sq : (k_max - 3) ^ 2 = 25 := by
  norm_num [k_max_value]

/-- ★ h′(2) 强候选框架表达：13/600 = (k_max+5)/(N_gen·k_max·(k_max−3)²)。 -/
theorem hp_identity : (k_max + 5 : ℚ) / (3 * k_max * (k_max - 3) ^ 2 : ℚ) = 13 / 600 := by
  norm_num [k_max_value]

/-! =========================================================
    §3 C/h′ 分母对比
   ========================================================= -/

/-- C 分母 2^(k_max−1) = 128（引用 KMaxAlgebra.c_denominator_cl7 数值）。 -/
theorem c_den_128 : 2 ^ (k_max - 1) = 128 := by
  norm_num [k_max_value]

/-- ★ C/h′ 分母比：128/600 = 16/75。 -/
theorem hp_c_den_ratio : (2 ^ (k_max - 1) : ℚ) / (3 * k_max * (k_max - 3) ^ 2 : ℚ) = 16 / 75 := by
  norm_num [k_max_value]

/-! =========================================================
    §4 h(2)/h′(2) 缩小因子（245 粗候选登记）
   ========================================================= -/

/-- ★ 缩小因子精确恒等：h(2)/h′(2) = (7/64)/(13/600) = 525/104（≈5.048，245 粗候选近 N′=5，+0.96%）。 -/
theorem hp_h_ratio : (7 : ℚ) / 64 / ((13 : ℚ) / 600) = 525 / 104 := by
  norm_num

end MUFPF.HPrimeLayer
