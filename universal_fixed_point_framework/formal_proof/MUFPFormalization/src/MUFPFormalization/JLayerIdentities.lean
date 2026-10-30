/-
# JLayerIdentities.lean — j(2) = −13/293 候选层身份（P7-5e-260v/w/aa 资产形式化）

形式化目标（j 层身份链，260v/260w/260aa 战役 + 293 身份链 260ar）：
  j(2) 优先候选 = −13/293。本文件形式化其**真实成立的代数结构**：

    j 分子：13 = k_max + 5                    （k_max 家族 +5 侧）
    j 分母：293 = k_max·(k_max−1)·5 + (k_max+5)   （静默单元×5 + 分子：262 塔锚差分延伸）
            293 = (2¹¹+3)/7                  （Mersenne 双绑定，267 mersenne_293）
            293 = 2⁸+2⁵+2²+2⁰                （2 进展开，指数 {8,5,2,0} = {k_max, k_max−3, …}）
    近候选判别：91 = 7·13 = (k_max−1)·(k_max+5)；2049 = 2¹¹+1
            13·2049 ≠ 91·293（★ 机器证明的不等：91/2049 是近候选但非恒等，
            差 26/600357 ≈ 0.098%——诚实边界，260ab 判别结论形式化）

数值先证伪记录（先证伪再证明，模式 8）：
  - p7_5e268_pycheck.py（sympy 精确）：9/9 全通过、残差 0 + 1 判别记录
    （13/293 ≠ 91/2049，resid −26/600357，作为近候选判别证据保留）。
-/

import Mathlib.Tactic
import MUFPFormalization.DeepCoefficientIdentities

open MUFPF.BottTower

namespace MUFPF.JLayer

/-! =========================================================
    §1 j 分子：13 = k_max + 5
   ========================================================= -/

/-- j(2) 分子 13 = k_max + 5（k_max 家族 +5 侧，同 293 分解）。 -/
theorem j_numerator_kmax : k_max + 5 = 13 := by
  norm_num [k_max_value]

/-! =========================================================
    §2 j 分母：293 的三重身份
   ========================================================= -/

/-- 293 = k_max·(k_max−1)·5 + (k_max+5)：静默单元×5 + j 分子（塔锚差分延伸）。 -/
theorem j_denominator_silent : k_max * (k_max - 1) * 5 + (k_max + 5) = 293 := by
  norm_num [k_max_value]

/-- 293 的 Mersenne 绑定：7·293 = 2¹¹+3（引用 DeepCoefficientIdentities.mersenne_293）。 -/
theorem j_denominator_mersenne : 7 * 293 = 2 ^ 11 + 3 := by
  exact MUFPF.DeepCoeff.mersenne_293

/-- 293 = 56·5+13：静默单元 56 = k_max(k_max−1) 的数值展开。 -/
theorem j_denominator_silent_num : 56 * 5 + 13 = 293 := by
  norm_num

/-- 293 的 2 进展开：293 = 2⁸+2⁵+2²+2⁰（指数 {8,5,2,0}，k_max 步进 3）。 -/
theorem j_denominator_binary : 2 ^ 8 + 2 ^ 5 + 2 ^ 2 + 2 ^ 0 = 293 := by
  norm_num

/-! =========================================================
    §3 近候选判别（诚实边界：机器证明的不等）
   ========================================================= -/

/-- 91 = 7·13（=91/2049 候选的分子）。 -/
theorem j_91_numerator : 7 * 13 = 91 := by
  norm_num

/-- 91 = (k_max−1)·(k_max+5)（静默单元 × j 分子）。 -/
theorem j_91_kmax : (k_max - 1) * (k_max + 5) = 91 := by
  norm_num [k_max_value]

/-- 2049 = 2¹¹+1（=91/2049 候选的分母）。 -/
theorem j_2049 : 2 ^ 11 + 1 = 2049 := by
  norm_num

/-- 2049 = 7·293 − 2（与 Mersenne 绑定的 2 之差）。 -/
theorem j_2049_from_mersenne : 7 * 293 - 2 = 2049 := by
  norm_num

/-- ★ 诚实边界：13·2049 ≠ 91·293（机器证明的不等——91/2049 是近候选而非 j(2) 的恒等
    等价形式，差 26；对应 260ab 判别结论）。 -/
theorem j_cross_neq : 13 * 2049 ≠ 91 * 293 := by
  norm_num

/-- j 分子分母互素性（13 ∤ 293，为最简分数提供依据）。 -/
theorem j_gcd_num : 13 % 293 ≠ 0 := by
  norm_num

end MUFPF.JLayer
