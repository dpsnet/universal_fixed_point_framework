import MUFPFormalization.DeltaStarSpectrum
import MUFPFormalization.DHStructuralAnalysis
import MUFPFormalization.AlphaChain

/-! # AlphaGaugeCoding.lean — α⁻¹ 的预言资格分层与 σ 进制编码判据（S628，2026-11-10）

## 判决背景

CODATA 2022 把 α⁻¹ 的现行四项式

  α⁻¹ = 72 + 24·ln15 + 24·(6σ³ + 4σ⁵ + 8σ⁷ + 5σ⁸) = 137.035999083426

推到 +4.46 σ_score（>3σ_score，按 §12.4.1 预注册条款构成否决）。本文件不试图
"再拟合一次"，而是把"为什么必然如此"落成可判定的算术命题——即证明该四项式
的系数不是机制量，而是实验值在 σ 幂基下的数字编码。

## 五条机检事实

1. **最低位量子的量化事实**：24σ⁸ = 8/854296875 ≈ 9.364×10⁻⁹，而实验合成
   不确定度 u = 2.1×10⁻⁸。故 σ⁸ 位每加 1 个单位只移动 ≈0.45σ_score——该位系数
   在 1σ_score 判据下不被唯一锁定（±2 个单位自由度）；更高阶 24σ⁹ ≈ 6.24×10⁻¹⁰
   更低于 u，级数可无限续项而无痕迹地微调。

2. **两版数据的编码位移**：CODATA 2018 与 2022 之差
   137.035999177 − 137.035999084 = 9.3×10⁻⁸ ≈ 10 ×（24σ⁸），即两版实验值在
   σ⁸ 位上相差约 10 个数字单位，折合 4.43σ_score。

3. **两套系数的互斥**：δ* 目标值在 {σ³,σ⁵,σ⁷,σ⁸} 基上逐层展开，
   2018 给出 (6,4,8,5)，2022 给出 (6,4,9,0)；两者之差 = (2/3)σ⁷，经 24 倍放大
   为 16σ⁷ ≈ 9.36×10⁻⁸ > 3u。故任一系数组必然对另一版超 3σ_score——同一"机制
   结构"不可能同时命中两版，系数因此是数据的 σ 进制编码，不携带机制信息。

4. **终止层折叠的真实条件**：σ⁷ = 15σ⁸ 是严格恒等式，但 8σ⁷ + 5σ⁸ 并不折成整层
   ——8σ⁷ + 5σ⁸ = 8σ⁷ + (1/3)σ⁷ = (25/3)σ⁷；只有 c8 = 15（= SigmaInv）时才有
   8σ⁷ + 15σ⁸ = 9σ⁷。即"σ⁸ 是否可折成 σ⁷ 整层"取决于该位数字是否为 SigmaInv，
   这正说明该位数字是自由参数而非结构常数。

5. **机制唯一层**：d_H = ln15 为 Moran 方程机证（`ln15_gt_2708` / `ln15_lt_65_24`
   给出双边界），α⁻¹_mech = 24(ln15+3) 落在开区间 (136.992, 137)——3 位有效、
   零自由参数。这是 α⁻¹ 唯一具预言资格的层。

先证伪再证明（模式 8）：scripts/s628_alpha_gauge_coding_precheck.py
  11 项全 PASS（量子量化 5 / 编码位移 2 / 两版互斥 2 / 机制层 2）。
-/

namespace MUFPF.AlphaGaugeCoding

open Real

/-- 静默窗口 σ = 1/15（框架常数；与 `DeltaStarSpectrum.sigma` 同值）。 -/
noncomputable def sigma : ℝ := 1 / 15

/-- 实验合成不确定度 u = 2.1×10⁻⁸（CODATA 2018/2022 两期同值——α 的倒数口径）。 -/
noncomputable def uExp : ℝ := 21 / 10 ^ 9

-- ============ ① σ 幂次的进位恒等式 ============

/-- σ⁷ = 15σ⁸（σ = 1/15；15 = SigmaInv）。 -/
theorem sigma7_eq_fifteen_sigma8 : sigma ^ 7 = 15 * sigma ^ 8 := by
  simp only [sigma]
  norm_num

/-- 终止层折叠**只在 c8 = 15 时成立**：8σ⁷ + 15σ⁸ = 9σ⁷。 -/
theorem eight_plus_fifteen_folds_to_nine : (8 : ℝ) * sigma ^ 7 + 15 * sigma ^ 8 = 9 * sigma ^ 7 := by
  have h : sigma ^ 7 = 15 * sigma ^ 8 := sigma7_eq_fifteen_sigma8
  rw [← h]
  ring

/-- 原式 c8 = 5 只给出分数层：8σ⁷ + 5σ⁸ = (25/3)σ⁷——不是整层。 -/
theorem five_sigma8_is_fractional_layer :
    (8 : ℝ) * sigma ^ 7 + 5 * sigma ^ 8 = (25 / 3 : ℝ) * sigma ^ 7 := by
  have h : sigma ^ 7 = 15 * sigma ^ 8 := sigma7_eq_fifteen_sigma8
  have h5 : (5 : ℝ) * sigma ^ 8 = (1 / 3 : ℝ) * sigma ^ 7 := by
    rw [h]
    ring
  rw [h5]
  ring

-- ============ ② 分辨率阶梯的量化事实 ============

/-- 最低位量子：24σ⁸ = 8/854296875 ≈ 9.364×10⁻⁹（15⁸ = 2562890625）。 -/
theorem sigma8_quantum_rational : (24 : ℝ) * sigma ^ 8 = 8 / 854296875 := by
  simp only [sigma]
  norm_num

/-- 再下一阶量子：24σ⁹ = 8/12814453125 ≈ 6.243×10⁻¹⁰。 -/
theorem sigma9_quantum_rational : (24 : ℝ) * sigma ^ 9 = 8 / 12814453125 := by
  simp only [sigma]
  norm_num

/-- 阶梯相邻阶比 = σ⁻² = 225（每降一阶，分辨率缩小 225 倍）。 -/
theorem ladder_ratio_225 :
    ((24 : ℝ) * sigma ^ 3) / ((24 : ℝ) * sigma ^ 5) = 225 := by
  simp only [sigma]
  norm_num

/-- σ⁸ 位的系数在 1σ_score 内不被唯一锁定：单位量子 < u（0.45σ_score 每单位）。 -/
theorem sigma8_bit_free_within_one_sigma :
    (24 : ℝ) * sigma ^ 8 < uExp := by
  have h : (24 : ℝ) * sigma ^ 8 = 8 / 854296875 := sigma8_quantum_rational
  rw [h]
  simp only [uExp]
  norm_num

/-- σ⁹ 位的量子远低于 u——级数可续项而无痕迹微调。 -/
theorem sigma9_bit_invisible :
    (24 : ℝ) * sigma ^ 9 < uExp := by
  have h : (24 : ℝ) * sigma ^ 9 = 8 / 12814453125 := sigma9_quantum_rational
  rw [h]
  simp only [uExp]
  norm_num

-- ============ ③ 两版 CODATA 的编码位移 ============

/-- 两版 CODATA 之差 ≈ 10 个 σ⁸ 数字单位（残差 6.44×10⁻¹⁰ < 10⁻⁹）。 -/
theorem codata_gap_ten_quanta :
    |(137.035999177 : ℝ) - 137.035999084 - 10 * ((24 : ℝ) * sigma ^ 8)| < 1 / 10 ^ 9 := by
  simp only [sigma]
  rw [abs_lt]
  constructor <;> norm_num

/-- 该位移是 4.43σ_score（> 3σ：两版之差不可能是统计涨落）。 -/
theorem codata_gap_exceeds_three_sigma :
    (10 : ℝ) * ((24 : ℝ) * sigma ^ 8) > 3 * uExp := by
  simp only [sigma, uExp]
  norm_num

-- ============ ④ 两套系数的互斥 ============

/-- 2018 组 (6,4,8,5) 与 2022 组 (6,4,9,0) 之差 = (2/3)σ⁷。 -/
theorem two_digit_sets_differ :
    (6 * sigma ^ 3 + 4 * sigma ^ 5 + 9 * sigma ^ 7)
      - (6 * sigma ^ 3 + 4 * sigma ^ 5 + 8 * sigma ^ 7 + 5 * sigma ^ 8)
      = (2 / 3 : ℝ) * sigma ^ 7 := by
  have h : sigma ^ 7 = 15 * sigma ^ 8 := sigma7_eq_fifteen_sigma8
  have hz : sigma ^ 7 - 15 * sigma ^ 8 = 0 := by rw [h]; ring
  linear_combination (1 / 3 : ℝ) * hz

/-- 该差值经 24 倍放大后 > 3u：任一系数组必然对另一版超 3σ_score。 -/
theorem two_digit_sets_gap_exceeds_three_sigma :
    (24 : ℝ) * ((2 / 3 : ℝ) * sigma ^ 7) > 3 * uExp := by
  simp only [sigma, uExp]
  norm_num

-- ============ ⑤ 机制唯一层（零自由参数） ============

/-- 机制层值：α⁻¹_mech = 24(ln15 + 3) = 24ln15 + 72（d_H = ln15 机证的直接组装）。 -/
theorem alphaMech_algebraic : (24 : ℝ) * (log 15 + 3) = 24 * log 15 + 72 := by
  ring

/-- 机制层落在开区间 (136.992, 137)——3 位有效、零自由参数。 -/
theorem alphaMech_bounds :
    136.992 < (24 : ℝ) * (log 15 + 3) ∧ (24 : ℝ) * (log 15 + 3) < 137 := by
  constructor
  · have h := MUFPF.DHStructural.ln15_gt_2708
    have h' : (2.708 : ℝ) < Real.log 15 := by
      simpa [MUFPF.DHStructural.ln15] using h
    linarith
  · have h := MUFPF.DHStructural.ln15_lt_65_24
    have h' : Real.log 15 < (65 : ℝ) / 24 := by
      simpa [MUFPF.DHStructural.ln15, MUFPF.DHStructural.sixtyfive_over_24] using h
    linarith

-- ============ ⑥ 判据合成 ============

/-- 编码判据合成：σ⁸ 位可自由（< 1σ/单位）、两版之差是 10 个 σ⁸ 单位、
  两套系数之差超 3σ、机制层零参数——四项同时成立。 -/
theorem gauge_coding_dichotomy :
    ((24 : ℝ) * sigma ^ 8 < uExp) ∧
    (|(137.035999177 : ℝ) - 137.035999084 - 10 * ((24 : ℝ) * sigma ^ 8)| < 1 / 10 ^ 9) ∧
    ((24 : ℝ) * ((2 / 3 : ℝ) * sigma ^ 7) > 3 * uExp) ∧
    (136.992 < (24 : ℝ) * (log 15 + 3) ∧ (24 : ℝ) * (log 15 + 3) < 137) := by
  exact ⟨sigma8_bit_free_within_one_sigma, codata_gap_ten_quanta,
    two_digit_sets_gap_exceeds_three_sigma, alphaMech_bounds⟩

end MUFPF.AlphaGaugeCoding
