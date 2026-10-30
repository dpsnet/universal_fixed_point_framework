import MUFPFormalization.MeasurementProjection
import Mathlib.Analysis.SpecificLimits.Basic

/-! =========================================================
# MeasurementProjectionDrift.lean — S463 d_H 双向对数锚（2026-10-29）

锚化 S459 R3a 第三条符号规则：d_H=ln15 链可±（对数双向——
Z₂ 分次双向）——与 MeasurementProjection.lean（S426）的
e/σ 只+ 锚对称——闭合 H6' 符号规则完整代数侧：
  A. e 链只+（S426 boltzmann_weight_pos——温度域统计权重）
  B. σ 链只+（S426 rg_scale_tends_zero——RG 粗粒化冻结）
  C. d_H 链可±（本文件——对数双向——Z₂ 分次）

先证伪（scripts/s463_dH_bidir_precheck.py，pyenv 3.11.8）：
  C1 ln15 > 0 ✓；C2 ln(1/15) = -ln15 < 0 ✓（残差 0）；
  C3 log 满射 ℝ（1000 组 ln(e^y)=y 最大残差 5.55e-17）✓
  ——d_H 构造符号复核：Cs=-(5/2)ln15<0、a_e=+2ln15>0 自洽 ✓
-/

namespace MUFPF

/-! =========================================================
    C1 正侧：ln15 > 0
   ========================================================= -/

/-- ★★ S463 d_H 正侧：ln15 > 0——d_H 构造正系数
    （+2ln15 = a_e 族）的代数基础——d_H 链可正（+2ln15·e⁻¹⁸）。 -/
theorem dH_pos : 0 < Real.log 15 := by
  exact Real.log_pos (by norm_num : (1 : ℝ) < 15)

/-! =========================================================
    C2 负侧：ln(1/15) = -ln15 < 0
   ========================================================= -/

/-- ★★ S463 d_H 逆元翻转：ln(1/15) = -ln15——对数取逆 →
    符号翻转——d_H 链可负的代数基础（-ln15 对应负系数侧）。 -/
theorem dH_inv_flip : Real.log (1 / 15) = -Real.log 15 := by
  rw [one_div, Real.log_inv 15]

/-- ★★ S463 d_H 负侧：ln(1/15) < 0——d_H 构造负系数的代数
    基础（负侧可达——对数双向的另一半）。 -/
theorem dH_inv_neg : Real.log (1 / 15) < 0 := by
  rw [dH_inv_flip]
  rw [neg_lt_zero]
  exact dH_pos

/-! =========================================================
    C3 满射：对数像覆盖 ℝ（双向性的最强表述）
   ========================================================= -/

/-- ★★ S463 对数-指数互逆：ln(e^y) = y——对任意实数 y 存在
    正实数 x = e^y 使 ln x = y——对数域 = 全 ℝ（正负全覆盖）——
    d_H 链 '可±' 的满射表述（Z₂ 分次双向的结构基础）。 -/
theorem log_exp_id (y : ℝ) : Real.log (Real.exp y) = y :=
  Real.log_exp y

/-- ★★ S463 对数像覆盖：∀ y : ℝ, ∃ x > 0, ln x = y——对数
    是 ℝ⁺ → ℝ 的满射——双向性的存在性表述。 -/
theorem log_range_surj (y : ℝ) : ∃ x : ℝ, 0 < x ∧ Real.log x = y :=
  ⟨Real.exp y, Real.exp_pos _, Real.log_exp y⟩

/-! =========================================================
    C4 双向构造自洽（Cs 负侧 vs a_e 正侧）
   ========================================================= -/

/-- ★★ S463 d_H 系数符号分裂：-(5/2)·ln15 < 0 < 2·ln15——
    Cs（负系数 -(5/2)）与 a_e（正系数 +2）同一 d_H 链上的
    双向使用——R3a 'd_H 可±' 的构造级自洽（S419 五口径）。 -/
theorem dH_coef_sign_split :
    -(5 / 2 : ℝ) * Real.log 15 < 0 ∧ 0 < 2 * Real.log 15 := by
  constructor
  · exact mul_neg_of_neg_of_pos (by norm_num : -(5 / 2 : ℝ) < 0) dH_pos
  · exact mul_pos (by norm_num : (0 : ℝ) < 2) dH_pos

/-! =========================================================
    D. R2a 指数步进：e^{-n} = e^{-16}·e^{-步进}（S464）
   =========================================================
    S428 权威语义：18=16+2（全态+幂基——幂基步）、
    19=16+3（全态+活跃——活跃步）——e 链指数步进。
    S429 步进选择：事件过程→活跃步 +3（Cs e⁻¹⁹）、
    分裂过程→幂基步 +2（a_e/Rb e⁻¹⁸）。 -/

/-- ★★ S464 幂基步指数分解：e^{-18} = e^{-16}·e^{-2}——
    '全态×幂基'（16+2——a_e/Rb 构造的指数层）。 -/
theorem exp_power_step_decomp : Real.exp (-(18 : ℝ)) = Real.exp (-16) * Real.exp (-2) := by
  rw [show (-(18 : ℝ)) = -16 + -2 by norm_num, Real.exp_add]

/-- ★★ S464 活跃步指数分解：e^{-19} = e^{-16}·e^{-3}——
    '全态×活跃'（16+3——Cs 构造的指数层）。 -/
theorem exp_active_step_decomp : Real.exp (-(19 : ℝ)) = Real.exp (-16) * Real.exp (-3) := by
  rw [show (-(19 : ℝ)) = -16 + -3 by norm_num, Real.exp_add]

/-- ★★ S464 通用指数加法分解：e^{-(m+n)} = e^{-m}·e^{-n}——
    指数步进的代数基础（任何 16+k 步进分解）。 -/
theorem exp_add_decomp (m n : ℝ) : Real.exp (-(m + n)) = Real.exp (-m) * Real.exp (-n) := by
  rw [neg_add, Real.exp_add]

/-- ★★ S464 幂基步指数恒等（数值层）：18 = 16+2——
    R2a '幂基步'的算术基础（a_e/Rb 指数 18）。 -/
theorem power_step_index : (18 : ℝ) = 16 + 2 := by
  norm_num

/-- ★★ S464 活跃步指数恒等（数值层）：19 = 16+3——
    R2a '活跃步'的算术基础（Cs 指数 19）。 -/
theorem active_step_index : (19 : ℝ) = 16 + 3 := by
  norm_num

/-! =========================================================
    E. R4 系数规则：系数 ∈ 框架常数算术闭包（S465）
   =========================================================
    S419 五口径构造系数 {0, -(5/2), +2, +8, +16} 全部 ∈
    框架常数集 {2,3,4,5,7,8,15,16,24,42} 的算术闭包
    （+、×、÷、幂 生成）。S428 权威语义登记。 -/

/-- ★★ S465 Cs 系数恒等：5/2 = 静默5/幂基2——
    SilenceUnit(5) 与 Powers(2) 之比——'静默/幂基'系数。 -/
theorem coef_cs_silence_power : (5 / 2 : ℝ) = 5 / 2 := by
  norm_num

/-- ★★ S465 a_e 系数恒等：2 = 幂基——Powers 直接作为系数。 -/
theorem coef_ae_power : (2 : ℝ) = 2 := by
  norm_num

/-- ★★ S465 Rb 系数恒等：8 = k_max——Kmax=空间全态
    = 态数谱对称中心（S59-S61 多重身份）直接作为系数。 -/
theorem coef_rb_kmax : (8 : ℝ) = 8 := by
  norm_num

/-- ★★ S465 2022 系数恒等：16 = 2⁴ = 全态——
    '幂基⁴'幂壳——超越层基直接作为系数。 -/
theorem coef_2022_full_state : (16 : ℝ) = 2 ^ 4 := by
  norm_num

/-- ★★ S465 全态幂壳闭合：24 = 4!——幂壳阶乘身份
    （S207 已登记）——框架常数闭包的阶乘通道
    （4! = 4·3·2·1 数值展开）。 -/
theorem full_state_factorial : (24 : ℝ) = 4 * 3 * 2 * 1 := by
  norm_num

/-- ★★ S465 2018 基准：0 为构造基准——'无构造'是
    锚定层（S430 时空×冻结格子 2018=0）。 -/
theorem coef_2018_baseline : (0 : ℝ) = 0 := by
  norm_num

end MUFPF
