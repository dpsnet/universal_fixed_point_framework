/-
## ExpTsumAnchor.lean —— S533 e 升格解析锚（2026-10-29）

e 升格命题（S531 等权公设内生化 → S532 Lean 基底）的解析侧缺口：
  "1/k! 泊松归一化级数 = e" 需要无穷级数 tsum 锚——
  现有 ExpTruncation.lean 只锚截断和（Σ_{k=0}^8 1/k! = 109601/40320 + 余项界
  10/(9·9!)）——缺 e = Σ'_{k=0}^∞ 1/k! 的定义式。

本文件锚定：Real.exp 1 = ∑' k, 1/k!（泊松级数定义式）
  路径：Real.exp_eq_exp_ℝ（Real.exp = NormedSpace.exp——数学分析定义）
      + NormedSpace.exp_eq_tsum_div（NormedSpace.exp x = ∑' n, x^n/n!——级数恒等）
  —— 这是 e 的**定义式**（内部推导恒等），非外部公式：
     1/k! 系数源自等权公设（S531/S532 已 Lean 化）——本文件只锚
     "级数求和 = e" 这一步。

依赖纪律：精细引入（本模块承载分析重依赖，ExpTruncation/EqualWeightMeasure
  保持轻量）。
-/
import Mathlib.Tactic
import Mathlib.Data.Real.Basic
import Mathlib.Analysis.Normed.Algebra.Exponential
import Mathlib.Analysis.SpecialFunctions.Exponential

open scoped BigOperators

namespace MUFPF.ExpTsumAnchor

/-- ★ e = Σ'_{k=0}^∞ 1/k!（泊松归一化无穷级数定义式——e 升格解析锚）。
    路径：Real.exp_eq_exp_ℝ（Real.exp = NormedSpace.exp——数学分析定义）
        + NormedSpace.exp_eq_tsum_div
          （NormedSpace.exp x = ∑' n, x^n/n!——级数恒等）
    先证伪（S531 脚本）：Σ_{k=0}^8 1/k! = 109601/40320 = 2.71827877，
    |e − ·| = 3.0586e-6 < 10/(9·9!) = 3.062e-6 ✓（ExpTruncation.eRemainder_bound）。 -/
theorem exp_one_tsum :
    Real.exp 1 = ∑' k : ℕ, (1 : ℝ) / k.factorial := by
  rw [Real.exp_eq_exp_ℝ, NormedSpace.exp_eq_tsum_div]
  simp

/-- 推论：e > 0（概率归一化的正性——泊松测度非退化）。 -/
theorem exp_one_pos : 0 < Real.exp 1 :=
  Real.exp_pos 1

/-- 推论：泊松归一化系数级数收敛（1/k! 绝对收敛——概率测度合法）。 -/
theorem exp_one_summable : Summable fun k : ℕ => (1 : ℝ) / k.factorial := by
  have hs := NormedSpace.expSeries_summable' (𝕂 := ℝ) (𝔸 := ℝ) (x := (1 : ℝ))
  -- hs : Summable fun n => (n !⁻¹ : ℝ) • 1 ^ n
  simpa [div_eq_mul_inv, one_pow] using hs

end MUFPF.ExpTsumAnchor
