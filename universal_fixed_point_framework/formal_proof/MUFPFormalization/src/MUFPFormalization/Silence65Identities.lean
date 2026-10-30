/-
# Silence65Identities.lean — 65 修正三重框架身份 + 39/65 同族（P7-5e-275）

形式化目标（P7-5e-95e~99 65 修正锁定资产 + 269 39 家族）：
  通道数闭式 1/B*(m) = |m|·α₀ + 1/(k_max−1) + 1/((k_max−1)·2^|m|) 中 m=−1 独享 +1/65
  （★★★★★ 0.00015% 命中、Richardson 外推确认）的身份链：

    · 65 = k_max²+1（主身份）
        = 2⁶+1（Fermat 型）
        = 5·13 = (k_max−3)(k_max+5)（与 39 = (k_max−5)(k_max+5) 同族，共享 (k_max+5) 因子）
        = N_Weyl³+1 = 4³+1（N_Weyl=4 = k_max/2）；
    · 39/65 同族：65/39 = (k_max−3)/(k_max−5) = 5/3（共享因子约去）、
      65−39 = 26 = 2·13、39·65 = 2535 = 3·5·13²。

★ 诚实边界：
  · 65 修正的物理身份（m=−1 独享、满格通道闭合静默余数）是 95e~99 的判别锁定
    （★★★★★ 0.00015% 级）——本文件只机器验证代数恒等；
  · "为何 65 独享 m=−1"（机制）维持开放（65 身份链成立但选择机制未推导）；
  · N_Weyl=4 语义（Weyl 层）为候选登记，代数 4³+1=65 是精确恒等。

数值先证伪记录（先证伪再证明，模式 8）：
  - p7_5e275_pycheck.py（sympy 精确）：11/11 全通过、残差 0。

关系链：import BowlLayerIdentities（39 家族跨文件）。
-/

import Mathlib.Tactic
import MUFPFormalization.BowlLayerIdentities

open MUFPF.BottTower

namespace MUFPF.Silence65

/-! =========================================================
    §1 65 框架身份（m=−1 独享修正）
   ========================================================= -/

/-- ★ 65 = k_max²+1（m=−1 独享修正主身份，95e~99 锁定）。 -/
theorem s65_kmax : k_max ^ 2 + 1 = 65 := by
  norm_num [k_max_value]

/-- 65 = 2⁶+1（Fermat 型幂+1）。 -/
theorem s65_pow6 : 2 ^ 6 + 1 = 65 := by
  norm_num

/-- ★ 65 = (k_max−3)(k_max+5) = 5·13（与 39 同族共享 (k_max+5)）。 -/
theorem s65_factor : (k_max - 3) * (k_max + 5) = 65 := by
  norm_num [k_max_value]

/-- 65 = N_Weyl³+1 = 4³+1（N_Weyl=4 = k_max/2，Weyl 层候选登记）。 -/
theorem s65_weyl : 4 ^ 3 + 1 = 65 := by
  norm_num

/-- ★ 65 三重联合：(k_max²+1 = 2⁶+1 = (k_max−3)(k_max+5) = 65)。 -/
theorem s65_triple :
    (k_max ^ 2 + 1 = 65) ∧ (2 ^ 6 + 1 = 65) ∧ ((k_max - 3) * (k_max + 5) = 65) := by
  norm_num [k_max_value]

/-! =========================================================
    §2 39/65 同族（共享 (k_max+5) 因子）
   ========================================================= -/

/-- 39 = (k_max−5)(k_max+5)（引用 BowlLayer.e39_factor 跨文件链）。 -/
theorem s39_factor : (k_max - 5) * (k_max + 5) = 39 := by
  exact MUFPF.BowlLayer.e39_factor

/-- ★ 65/39 = (k_max−3)/(k_max−5) = 5/3（共享 (k_max+5) 因子约去——同族指纹）。 -/
theorem s65_over_39 : ((k_max - 3) * (k_max + 5) : ℚ) / ((k_max - 5) * (k_max + 5) : ℚ) = 5 / 3 := by
  norm_num [k_max_value]

/-- 65−39 = 26（同族差）。 -/
theorem s65_minus39 : 65 - 39 = 26 := by
  norm_num

/-- 26 = 2·13（差是 13 家族倍数）。 -/
theorem s65_minus39_times13 : 2 * 13 = 26 := by
  norm_num

/-- ★ 39·65 = 2535 = 3·5·13²（同族乘积 = (k_max−5)(k_max−3)(k_max+5)²）。 -/
theorem s39_times_65 : ((k_max - 5) * (k_max - 3) * (k_max + 5) ^ 2) = 2535 := by
  norm_num [k_max_value]

end MUFPF.Silence65
