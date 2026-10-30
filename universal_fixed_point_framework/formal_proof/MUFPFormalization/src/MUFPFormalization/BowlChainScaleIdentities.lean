/-
# BowlChainScaleIdentities.lean — 碗形链缩小因子 + 分子平方迭代家族（P7-5e-277）

形式化目标（P7-5e-245 碗形链层级判别资产——"逐级缩小"的框架结构）：
  碗形链三层数值逐级缩小（h(2)=7/64 → h'(2)=13/600 → i(2)），缩小因子是
  "缩小因子框架量 + 分子平方迭代"而非分形/套娃（非等比：r2/r1 = 1.347）：

    §1 缩小因子：
       h(2)/h'(2) = 525/104（精确恒等；粗候选 ≈5.048 与 N'=5 差 +0.96%，不断言）；
       h'(2)/i(2) = 15/4 = N_gen·N'/2² = N_gen·(k_max−3)/4（★ 用 i(2)=13/2250 候选
       使缩小因子 r2 精确等于框架量——245 "新观察" 的代数精确化）。
    §2 分子平方迭代家族（分子链平方迭代）：
       13 = 3²+2² = N_gen²+(N_gen−1)²（第一步，13 家族代数根）；
       173 = 13²+2² = C_分子²+(N_gen−1)²（★ 第二步——1/173 候选的分子平方身份）；
       预测第三步分母 173²+2² = 29933（245 递归延续预测，诚实边界：未锁定）。
    §3 i(2) 候选并列（诚实边界登记）：
       i(2) 候选恒等 13/2250 = 4·h'(2)/15（与 1/173 并列——245 登记）；
       框架表达 (k_max+5)/(2·N_gen²·(k_max−3)³) = 13/2250。

★ 诚实边界：
  · 缩小因子 r1 = 525/104 的数值身份（≈5.048 vs N'=5：+0.96%）是粗候选——
    精确分数恒等成立，但不断言 =N'=5；
  · i(2) 身份开放：13/2250 与 1/173 并列候选（245 登记），本文件只形式化
    13/2250 侧使 h'/i 精确 = 15/4 的代数结构，不判定 i(2) 真值；
  · 29933 是 245 递归延续预测（N≥2000 成本高未实测），登记为预测非锁定。

数值先证伪记录（先证伪再证明，模式 8）：
  - p7_5e277_pycheck.py（sympy 精确）：10/10 全通过、残差 0。

关系链：import DerivativeLayerIdentities（h2_identity）+ HPrimeLayerIdentities（hp_identity）
  + JLayerIdentities（j_numerator_kmax）。
-/

import Mathlib.Tactic
import MUFPFormalization.DerivativeLayerIdentities
import MUFPFormalization.HPrimeLayerIdentities
import MUFPFormalization.JLayerIdentities

open MUFPF.BottTower

namespace MUFPF.BowlChainScale

/-! =========================================================
    §1 缩小因子（P7-5e-245 层级判别）
   ========================================================= -/

/-- h(2) = 7/64（引用 DerivativeLayer.h2_identity 跨文件链）。 -/
theorem h2_value_chain : (k_max - 1 : ℚ) / ((2 : ℚ) ^ (k_max - 2)) = 7 / 64 := by
  exact MUFPF.DerivativeLayer.h2_identity

/-- h′(2) = 13/600（引用 HPrimeLayer.hp_identity 跨文件链）。 -/
theorem hprime_value_chain : (k_max + 5 : ℚ) / (3 * k_max * (k_max - 3) ^ 2 : ℚ) = 13 / 600 := by
  exact MUFPF.HPrimeLayer.hp_identity

/-- ★ 缩小因子 r1：h(2)/h′(2) = 525/104（精确恒等；≈5.048 vs N'=5 差 +0.96%——
    诚实边界：粗候选不断言 =N'=5）。 -/
theorem h_hprime_ratio : (7 : ℚ) / 64 / ((13 : ℚ) / 600) = 525 / 104 := by
  norm_num

/-- ★ 缩小因子 r2：h′(2)/i(2) = 15/4（用 i(2)=13/2250 候选——精确 N_gen·N'/2²）。 -/
theorem hprime_over_i2_cand : (13 : ℚ) / 600 / ((13 : ℚ) / 2250) = 15 / 4 := by
  norm_num

/-- ★ 15/4 = N_gen·N'/2² = 3·(k_max−3)/4（r2 的框架量表达，N_gen=3、N'=k_max−3）。 -/
theorem ratio2_framework : (3 : ℚ) * (k_max - 3) / 4 = 15 / 4 := by
  norm_num [k_max_value]

/-! =========================================================
    §2 分子平方迭代家族（245 分子链平方迭代）
   ========================================================= -/

/-- 13 = 3²+2² = N_gen²+(N_gen−1)²（第一步——13 家族代数根，j 分子）。 -/
theorem sq13 : 3 ^ 2 + 2 ^ 2 = 13 := by
  norm_num

/-- ★ 173 = 13²+2² = C_分子²+(N_gen−1)²（第二步——1/173 候选的分子平方身份）。 -/
theorem sq173 : 13 ^ 2 + 2 ^ 2 = 173 := by
  norm_num

/-- ★ 分子平方迭代两步联合：13 = 3²+2² ∧ 173 = 13²+2²。 -/
theorem sq_iter_triple : (3 ^ 2 + 2 ^ 2 = 13) ∧ (13 ^ 2 + 2 ^ 2 = 173) := by
  norm_num

/-- ★ 预测第三步分母：173²+2² = 29933（245 递归延续预测，诚实边界：未锁定）。 -/
theorem iter_pred : 173 ^ 2 + 2 ^ 2 = 29933 := by
  norm_num

/-! =========================================================
    §3 i(2) 候选并列（诚实边界登记）
   ========================================================= -/

/-- ★ i(2) 候选恒等：13/2250 = 4·h′(2)/15 = 4·(13/600)/15（与 1/173 并列，245 登记）。 -/
theorem i2_cand2 : (13 : ℚ) / 2250 = 4 * ((13 : ℚ) / 600) / 15 := by
  norm_num

/-- 2250 = 2·N_gen²·(k_max−3)³（候选分母框架：2·3²·5³）。 -/
theorem i2_cand2_den : 2 * 3 ^ 2 * 5 ^ 3 = 2250 := by
  norm_num

/-- ★ i(2) 候选框架表达：(k_max+5)/(2·N_gen²·(k_max−3)³) = 13/2250。 -/
theorem i2_cand2_kmax : ((k_max + 5 : ℚ)) / (2 * 3 ^ 2 * 5 ^ 3) = 13 / 2250 := by
  norm_num [k_max_value]

end MUFPF.BowlChainScale
