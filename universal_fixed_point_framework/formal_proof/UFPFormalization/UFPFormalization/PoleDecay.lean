-- ============================================================
-- UFPF → MUFPF 更名通知
-- ============================================================
-- 本文件属于 Universal Fixed Point Framework (UFPF)。
-- 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
-- 更名计划详见：roadmap/mu_renaming_plan.md
--
-- 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
-- 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
--
-- 本文件中 UFPF 相关引用数量：2
-- 更名将在计划确认后统一执行，当前代码不做修改。
-- ============================================================

import Mathlib.Data.Complex.Basic
import Mathlib.Analysis.Complex.Trigonometric
import Mathlib.Tactic.Linarith
import Mathlib.Tactic

namespace UFPFormalization

/-!
# PoleDecay — WW 复极点代数骨架（A4 涌现不可逆的极点侧；通用谱/复分析，2026-08-14 去光子前缀）

笔记: notes/06_photon_topology/photon_first_principle_origin.md §3.7
      （自伴性闭合方案 (iii) Friedrichs 模型："约化分母 η(z) 下半平面零点即共振
      ω₀−iγ/2"；开放项"WW 复极点的 Lean 代数骨架"）
论文: paper/paper44_photon_topology.md §7.5 开放问题 7
      （锚点 1 ③："不可逆与因果性是同一数学对象（下半平面极点）的两面"）
数值: scripts/paperX_friedrichs_resonance.py 8/8（z_res=ω_res−iγ/2 第二叶零点，
      P_e(t)≈e^{−γt} 指数衰减匹配极点率）

## 目标（代数骨架，零 sorry）
给定共振极点 z = ω − iγ/2 在下半平面（Im z < 0），自由传播子 e^{−i z t} 的
模方满足 **|e^{−i z t}|² = e^{2·Im z·t} = e^{−γ t}**——"下半平面极点 ⟹ 指数衰减"
（率 −2·Im z = γ > 0）。这是锚点 1 ③"推迟格林函数极点在下半平面"的
代数核心：极点贡献 c_pole(t) = R·e^{−i z t}（R 为留数）⟹ |c_pole(t)|² = |R|²·e^{−γ t}。

## 骨架状态（诚实边界）
1. **本文件已闭合（零 sorry）**：复分析的极点-衰减对应（纯代数/解析事实）。
2. **极点位置 z_res 的求取不在本文件**：z_res 为约化分母第二叶 η_II(z)=0 的
   零点（含对数分支/解析延拓），数学库无可解闭式——由数值脚本
   `paperX_friedrichs_resonance.py` 定量给出（推导级+数值佐证，非 Lean）。
3. **完整谱理论（自伴性/谱测度/共振的算子级定义）**：mathlib 无无界算子理论，
   为库依赖开放项（KatoRellichSkeleton.lean 已闭合其有界原型代数核心）。
-/

noncomputable section

/-- 共振极点指数衰减（代数核心）：
    对复极点 z，传播子相位 e^{−i z t} 的模方 |e^{−i z t}|² = e^{2·Im z·t}。
    Im z < 0（下半平面）⟹ 指数衰减，率 −2·Im z = γ > 0。 -/
theorem resonancePoleDecay {z : ℂ} {t : ℝ} :
    ‖Complex.exp (-Complex.I * z * (t : ℂ))‖ ^ 2 = Real.exp (2 * z.im * t) := by
  rw [Complex.norm_exp]
  have hre : Complex.re (-Complex.I * z * (t : ℂ)) = z.im * t := by
    rw [mul_assoc]
    rw [Complex.mul_re, Complex.mul_im]
    simp
  rw [hre]
  have harg : 2 * z.im * t = 2 * (z.im * t) := by ring
  rw [harg]
  rw [two_mul (z.im * t)]
  rw [Real.exp_add]
  rw [← pow_two]

/-- 共振极点贡献的衰减（带留数系数 R）：
    |R·e^{−i z t}|² = |R|²·e^{2·Im z·t}——指数衰减，振幅常数 |R|² 不变。 -/
theorem resonancePoleDecay_coeff {R z : ℂ} {t : ℝ} :
    ‖R * Complex.exp (-Complex.I * z * (t : ℂ))‖ ^ 2
      = ‖R‖ ^ 2 * Real.exp (2 * z.im * t) := by
  rw [Complex.norm_mul, mul_pow, resonancePoleDecay]

/-- 衰减率正值：下半平面极点（Im z < 0）给出正衰减率 γ = −2·Im z > 0。 -/
theorem resonanceDecayRate_pos {z : ℂ} (hz : z.im < 0) : 0 < -2 * z.im := by
  linarith

/-- 指数衰减的单调性：Im z < 0 时，|e^{−i z t}|² 随 t 严格递减
    （下半平面极点 ⟹ 无回归——锚点 1 ③"主动回跳被排除"的代数形式）。 -/
theorem resonancePoleDecay_mono {z : ℂ} {t₁ t₂ : ℝ} (hz : z.im < 0) (ht : t₁ < t₂) :
    ‖Complex.exp (-Complex.I * z * (t₂ : ℂ))‖ ^ 2
      < ‖Complex.exp (-Complex.I * z * (t₁ : ℂ))‖ ^ 2 := by
  rw [resonancePoleDecay, resonancePoleDecay]
  rw [Real.exp_lt_exp]
  have hmul : z.im * t₂ < z.im * t₁ := by
    exact mul_lt_mul_of_neg_left ht hz
  nlinarith

end

end UFPFormalization
