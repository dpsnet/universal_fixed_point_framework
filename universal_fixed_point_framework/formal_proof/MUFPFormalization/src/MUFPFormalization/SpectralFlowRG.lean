-- ============================================================
-- UFPF → MUFPF 更名通知
-- ============================================================
-- 本文件属于 Universal Fixed Point Framework (UFPF)。
-- 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
-- 更名计划详见：roadmap/mu_renaming_plan.md
-- ============================================================

import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic
import MUFPFormalization.WeaveBCS
import MUFPFormalization.SuperfluidBridge

open Real

namespace MUFPF

/-!
# SpectralFlowRG.lean — 谱流 RG 多级常演化（Paper LVII §8.6d）

把 §8.6b 的单一自洽倍率 1/r* 分解为**谱流 RG 多级常演化**：

    Δλ_min --1/√3--> Δλ_min^(EM) --√3/r*--> δ_SC

其中 Δλ_min^(EM) = dl_1 = dl_min/√3 是 U(1) 电磁谱间隙（SU(2) Casimir 谱间隙比
Δλ₁:Δλ₂:Δλ₃ = 1/√3:1:√2 的第一分量）。中间级 Δλ_min^(EM) 由规范谱间隙结构
**唯一确定**（非自由参数），两级倍率把单级黑箱 1/r* 显式化为一个纯规范表示因子
（1/√3，来自 SU(2) Casimir）乘一个 BCS 谱流动力学因子（√3/r*）。

核心不变式（链一致性）：两级路径 ≡ 单级自洽倍率，即

    δ_SC / Δλ_min = (Δλ_min^(EM)/Δλ_min) · (δ_SC/Δλ_min^(EM)) = 1/r*.

等价地，用"降级倍率" k₁·k₂ = r* 表达：k₁ = Δλ_min/Δλ_min^(EM) = √3，
k₂ = Δλ_min^(EM)/δ_SC = √(1/3)·r* = r*/√3。

诚实边界（与 MUFPF-RN-ENDO-001 §4 一致）：
- 本文件形式化的是**代数因子分解**（multi-stage factorization），不是谱流方程
  的动力学 RG 常演化——把逐级倍率由谱流方程逐级重解（而非后验代入 k₂ = r*/√3）
  仍待发展（见 Paper LVII §8.7#5 剩余方向）。
- a_BCS、E_F 仍是物理输入；范畴 Δ 内生的是 Δλ_min、Δλ_min^(EM)（=dl_1，
  Cl(1,7)/SU(2) Casimir 谱间隙，定理）与 r* 的方程唯一性。
- 两级链不按能标单调排列（Δλ_min^(EM) < Δλ_min < δ_SC），故此处"常演化"指
  固定倍率的两级因子分解，而非单调重整化流。
-/

/-! ## Section 1: 电磁中间级谱间隙 Δλ_min^(EM) -/

/-- 电磁（U(1)）谱间隙中间级：Δλ_min^(EM) = dl_1 = dl_min/√3。
    来自 SU(2) Casimir 谱间隙比 Δλ₁:Δλ₂:Δλ₃ = 1/√3:1:√2（`WeaveBCS.dl_1`）。 -/
noncomputable def dl_min_EM : ℝ := dl_1

/-- Δλ_min^(EM) = dl_1（与电磁规范谱间隙的定义链接）。 -/
theorem dl_min_EM_eq_dl1 : dl_min_EM = dl_1 := rfl

/-- 辅助恒等式：√3 · √(1/3) = 1。 -/
private theorem sqrt3_mul_sqrt13 : Real.sqrt 3 * Real.sqrt (1 / 3 : ℝ) = 1 := by
  have h13 : Real.sqrt (1 / 3 : ℝ) = (Real.sqrt 3)⁻¹ := by
    rw [show (1 / 3 : ℝ) = (3 : ℝ)⁻¹ by norm_num, Real.sqrt_inv]
  rw [h13]
  field_simp [ne_of_gt (Real.sqrt_pos_of_pos (by norm_num : (0 : ℝ) < 3))]

/-- 辅助恒等式：√(1/3) · √3 = 1。 -/
private theorem sqrt13_mul_sqrt3 : Real.sqrt (1 / 3 : ℝ) * Real.sqrt 3 = 1 := by
  rw [mul_comm, sqrt3_mul_sqrt13]

/-- 中间级谱间隙严格为正：Δλ_min^(EM) = √(1/3)·dl_min > 0。 -/
theorem dl_min_EM_pos : 0 < dl_min_EM := by
  unfold dl_min_EM dl_1
  exact mul_pos (Real.sqrt_pos_of_pos (by norm_num : (0 : ℝ) < 1 / 3)) dl_min_pos

/-! ## Section 2: 降级倍率 k₁、k₂（乘积 = r*） -/

/-- 谱流 RG 第 1 级倍率（Δλ_min → Δλ_min^(EM)）：k₁ = Δλ_min/Δλ_min^(EM) = √3。
    纯规范表示常数（SU(2) Casimir 归一化）。 -/
noncomputable def RG_k1 : ℝ := dl_min / dl_min_EM

/-- 谱流 RG 第 2 级倍率（Δλ_min^(EM) → δ_SC）：k₂ = Δλ_min^(EM)/δ_SC = r*/√3。
    折叠 BCS 谱流自洽动力学（经 r*）。 -/
noncomputable def RG_k2 : ℝ := dl_min_EM / deltaSC_categorical

/-- k₁ = √3。 -/
theorem RG_k1_eq_sqrt3 : RG_k1 = Real.sqrt 3 := by
  unfold RG_k1 dl_min_EM dl_1
  have ha : Real.sqrt (1 / 3 : ℝ) ≠ 0 :=
    ne_of_gt (Real.sqrt_pos_of_pos (by norm_num : (0 : ℝ) < 1 / 3))
  calc
    dl_min / (Real.sqrt (1 / 3 : ℝ) * dl_min) = 1 / Real.sqrt (1 / 3 : ℝ) := by
      field_simp [dl_min_pos.ne', ha]
    _ = Real.sqrt 3 := by
      field_simp [ha]
      exact sqrt13_mul_sqrt3.symm

/-- k₂ = √(1/3)·r* = r*/√3。 -/
theorem RG_k2_eq : RG_k2 = Real.sqrt (1 / 3 : ℝ) * r_star := by
  unfold RG_k2 deltaSC_categorical dl_min_EM dl_1
  field_simp [dl_min_pos.ne', r_star_pos.ne']

/-- **折叠（乘积闭合）**：k₁·k₂ = r*——两级倍率的乘积重现自洽唯一根。
    这是"多级常演化 ≡ 单级自洽"的核心代数不变式。 -/
theorem RG_telescoping : RG_k1 * RG_k2 = r_star := by
  rw [RG_k1_eq_sqrt3, RG_k2_eq, ← mul_assoc, sqrt3_mul_sqrt13]
  ring

/-! ## Section 3: 链一致性（两级路径 = 单级路径） -/

/-- 合成：把两级倍率代回，δ_SC = Δλ_min/(k₁·k₂) 精确重现单级 δ_SC = Δλ_min/r*。 -/
theorem RG_chain_reproduces_single : deltaSC_categorical = dl_min / (RG_k1 * RG_k2) := by
  unfold deltaSC_categorical
  rw [RG_telescoping]

/-- 无量纲增长因子 f₁ = Δλ_min^(EM)/Δλ_min = 1/√3（纯规范表示，SU(2) Casimir）。 -/
noncomputable def RG_f1 : ℝ := dl_min_EM / dl_min

/-- 无量纲增长因子 f₂ = δ_SC/Δλ_min^(EM) = √3/r*（BCS 谱流动力学）。 -/
noncomputable def RG_f2 : ℝ := deltaSC_categorical / dl_min_EM

/-- f₁ = 1/√3。 -/
theorem RG_f1_eq : RG_f1 = 1 / Real.sqrt 3 := by
  unfold RG_f1 dl_min_EM dl_1
  have ha : Real.sqrt (1 / 3 : ℝ) ≠ 0 :=
    ne_of_gt (Real.sqrt_pos_of_pos (by norm_num : (0 : ℝ) < 1 / 3))
  field_simp [dl_min_pos.ne', ha]
  exact sqrt13_mul_sqrt3

/-- f₂ = √3/r*。 -/
theorem RG_f2_eq : RG_f2 = Real.sqrt 3 / r_star := by
  unfold RG_f2 deltaSC_categorical dl_min_EM dl_1
  have ha : Real.sqrt (1 / 3 : ℝ) ≠ 0 :=
    ne_of_gt (Real.sqrt_pos_of_pos (by norm_num : (0 : ℝ) < 1 / 3))
  field_simp [dl_min_pos.ne', r_star_pos.ne', ha]
  have h : Real.sqrt (1 / 3 : ℝ) * Real.sqrt 3 = 1 := sqrt13_mul_sqrt3
  nlinarith

/-- **多级常演化定理（链一致性）**：δ_SC/Δλ_min 经 EM 中间级的两级增长因子
    连乘（f₁·f₂）精确等于单级自洽倍率 1/r*——路径与中间级选择无关。 -/
theorem gap_ratio_telescoping :
    deltaSC_categorical / dl_min = RG_f1 * RG_f2 := by
  unfold RG_f1 RG_f2 dl_min_EM deltaSC_categorical dl_1
  field_simp [dl_min_pos.ne', r_star_pos.ne', dl_min_EM_pos.ne']

/-- 与 §8.6b 的单级结果对齐：δ_SC/Δλ_min = 1/r*（两级路径之和形式的等价刻画）。 -/
theorem gap_ratio_multistage_eq_single :
    RG_f1 * RG_f2 = 1 / r_star := by
  rw [← gap_ratio_telescoping]
  exact gap_ratio_categorical

end MUFPF