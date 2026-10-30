-- ============================================================
-- SquareIdentity.lean — 104az-222 核磁子链平方型身份与 14400 交叉锁定
-- ============================================================
-- 1. g_n/2 候选 44/23 = (7²−5)/(5²−2) = (对合域²−静默)/(静默²−幂基)
--    （参数 (7,5,2) 与 T4 主结构同源；负控：族内唯一 + g_p/2 零命中 + 10 decoy 全零）
-- 2. g_p/2 分母 14400 = (k_max×B)²，B = N_active×N_total = 15（BranchCounting 分支数）
--    （跨链交叉锁定候选，证据通道②弱证据，观察级不升格）
-- 全部零 sorry；纯 norm_num 代数恒等（数值先证伪：44/23、14400 恒等 6/6 残差 0）
-- 离线 mathlib 裁剪：Mathlib.Data.Rat.Basic 缺失 → 用 Mathlib.Tactic（与 KMaxAlgebra 同款通配）
-- ============================================================

import Mathlib.Tactic
import Mathlib.Data.Rat.Defs

namespace MUFPF.SquareIdentity

/-! §1 g_n/2 44/23 平方型身份（104az-222） -/

/-- 分子恒等：对合域²−静默 = 44。 -/
theorem gn2_num : (7 : ℕ) ^ 2 - 5 = 44 := by
  norm_num

/-- 分母恒等：静默²−幂基 = 23。 -/
theorem gn2_den : (5 : ℕ) ^ 2 - 2 = 23 := by
  norm_num

/-- 分数恒等：44/23 = (7²−5)/(5²−2)。 -/
theorem gn2_square_identity :
    (44 : ℚ) / (23 : ℚ) = ((7 : ℚ) ^ 2 - 5) / ((5 : ℚ) ^ 2 - 2) := by
  norm_num

/-! §2 g_p/2 分母 14400 交叉锁定（k_max×B）²，B = 15（104az-222） -/

/-- k_max×B = 8×15 = 120（B = N_active×N_total = 15，BranchCounting）。 -/
theorem kmax_times_B : (8 : ℕ) * 15 = 120 := by
  norm_num

/-- 交叉锁定主恒等：(k_max×B)² = 14400 = g_p/2 分母。 -/
theorem gp2_den_crosslock : ((8 : ℕ) * 15) ^ 2 = 14400 := by
  norm_num

/-- 等价形式：120² = 14400。 -/
theorem gp2_den_square : (120 : ℕ) ^ 2 = 14400 := by
  norm_num

/-- 素因子分解：14400 = 2⁶·3²·5²。 -/
theorem gp2_den_factorization : (2 : ℕ) ^ 6 * (3 : ℕ) ^ 2 * (5 : ℕ) ^ 2 = 14400 := by
  norm_num

/-! §3 交叉核对：44/23 与 T4 主结构参数集 (7,5,2) = (对合域,静默,幂基) -/

/-- 参数角色核对：7 为对合域（2³−1）、5 为静默（迭代不动点/韦达根）、2 为幂基。 -/
theorem involution_domain : (2 : ℕ) ^ 3 - 1 = 7 := by
  norm_num

theorem silence_five : (2 : ℕ) ^ 2 + 1 = 5 := by
  norm_num

end MUFPF.SquareIdentity
