/-
# DerivativeLayerIdentities.lean — 碗形链导数层锁定身份 {h(2), h″(2), i′(2)}（P7-5e-260p/q/r/s/t + 296-298 资产形式化）

形式化目标（碗形链层级判别 245 的导数层——h/g/f 函数系导数身份）：
  深阶身份矩阵中导数层三个**锁定身份**的 k_max 框架表达：

    h(2)  = 7/64 = (k_max−1)/2^(k_max−2)          （296-298：h(2)=7/64 判别 → C 解析锁定）
    i′(2) = −39/2048 = −(k_max−5)(k_max+5)/2^(k_max+3)  （260p/q/r 统计锁定；分子 39 接 269 家族链）
    h″(2) = −19/2048 = −(2·k_max+3)/2^(k_max+3)   （260s/260t h″ 证伪与命中）

  关联恒等：
    h(2)/C = 2(k_max−1)/(2k_max−3) = 14/13       （h(2) 判别 → C 解析锁定的数值链）
    |i′(2)|/7 = (k_max−5)(k_max+5)/(k_max−1) = 39/7  （i′ 与碗形 7/2048 同分母 2^(k_max+3)）

数值先证伪记录（先证伪再证明，模式 8）：
  - p7_5e270_pycheck.py（sympy 精确）：14/14 全通过、残差 0。
  覆盖：h(2)/i′(2)/h″(2) 三锁定身份的框架表达、19=2k_max+3、h(2)/C=14/13、
  |i′(2)|/7=39/7、同分母 2048。

关系链（跨文件）：
  KMaxAlgebra.lean → 268 JLayerIdentities.lean → 269 BowlLayerIdentities.lean → 本文件
  本文件引用 BowlLayer.e39_factor（39=(k_max−5)(k_max+5)）与 BowlLayer.bowl_den_2048（2048=2^(k_max+3)）。
-/

import Mathlib.Tactic
import MUFPFormalization.BowlLayerIdentities

open MUFPF.BottTower

namespace MUFPF.DerivativeLayer

/-! =========================================================
    §1 h(2) = 7/64（C 解析锁定的中间量，296-298）
   ========================================================= -/

/-- h(2) 分子 7 = k_max−1（静默单元）。 -/
theorem h2_num : k_max - 1 = 7 := by
  norm_num [k_max_value]

/-- h(2) 分母 64 = 2^(k_max−2)。 -/
theorem h2_den : 2 ^ (k_max - 2) = 64 := by
  norm_num [k_max_value]

/-- ★ h(2) 框架表达：7/64 = (k_max−1)/2^(k_max−2)。 -/
theorem h2_identity : (k_max - 1 : ℚ) / ((2 : ℚ) ^ (k_max - 2)) = 7 / 64 := by
  norm_num [k_max_value]

/-! =========================================================
    §2 i′(2) = −39/2048（260p/q/r 统计锁定）
   ========================================================= -/

/-- i′(2) 分子 39 = (k_max−5)(k_max+5)（引用 269 BowlLayer.e39_factor，跨文件链）。 -/
theorem ip_num_39 : (k_max - 5) * (k_max + 5) = 39 := by
  exact MUFPF.BowlLayer.e39_factor

/-- i′(2) 分母 2048 = 2^(k_max+3)（引用 269 BowlLayer.bowl_den_2048——与碗形 7/2048 同分母）。 -/
theorem ip_den_2048 : 2 ^ (k_max + 3) = 2048 := by
  exact MUFPF.BowlLayer.bowl_den_2048

/-- ★ i′(2) 框架表达：−39/2048 = −(k_max−5)(k_max+5)/2^(k_max+3)。 -/
theorem ip_identity :
    -((k_max - 5 : ℚ) * (k_max + 5 : ℚ)) / ((2 : ℚ) ^ (k_max + 3)) = -39 / 2048 := by
  norm_num [k_max_value]

/-! =========================================================
    §3 h″(2) = −19/2048（260s/260t 命中）
   ========================================================= -/

/-- h″(2) 分子 19 = 2·k_max+3。 -/
theorem h2p_num : 2 * k_max + 3 = 19 := by
  norm_num [k_max_value]

/-- ★ h″(2) 框架表达：−19/2048 = −(2·k_max+3)/2^(k_max+3)。 -/
theorem h2p_identity : -((2 * k_max + 3 : ℚ)) / ((2 : ℚ) ^ (k_max + 3)) = -19 / 2048 := by
  norm_num [k_max_value]

/-! =========================================================
    §4 关联恒等
   ========================================================= -/

/-- ★ h(2)/C = 2(k_max−1)/(2k_max−3)（h(2) 判别 → C 解析锁定的数值链；C=(2k_max−3)/2^(k_max−1)）。 -/
theorem h2_c_ratio :
    ((k_max - 1 : ℚ) / (2 : ℚ) ^ (k_max - 2)) /
      ((2 * k_max - 3 : ℚ) / (2 : ℚ) ^ (k_max - 1)) = 2 * (k_max - 1) / (2 * k_max - 3) := by
  norm_num [k_max_value]

/-- h(2)/C 数值 = 14/13。 -/
theorem h2_c_ratio_num : (7 : ℚ) / 64 / ((13 : ℚ) / 128) = 14 / 13 := by
  norm_num

/-- ★ |i′(2)| 与碗形 7/2048 同分母关联：39/7 = (k_max−5)(k_max+5)/(k_max−1)。 -/
theorem ip_bowl_ratio : ((k_max - 5) * (k_max + 5) : ℚ) / (k_max - 1 : ℚ) = 39 / 7 := by
  norm_num [k_max_value]

/-- h″ 与 i′ 量级比：19/39 = (2·k_max+3)/((k_max−5)(k_max+5))（同分母 2^(k_max+3) 下分子比）。 -/
theorem h2p_ip_ratio : ((2 * k_max + 3) : ℚ) / ((k_max - 5) * (k_max + 5) : ℚ) = 19 / 39 := by
  norm_num [k_max_value]

end MUFPF.DerivativeLayer
