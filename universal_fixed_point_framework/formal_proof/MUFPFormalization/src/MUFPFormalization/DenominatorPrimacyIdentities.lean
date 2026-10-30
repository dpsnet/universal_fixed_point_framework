import MUFPFormalization.CoreConstantWindowIdentities
import MUFPFormalization.PowerTwoSilentIdentities

/-!
# P7-5e-209 ⑨ 分母第一性：D(n)−1 线性因子分解与 1/B*(n) 闭式合并

数值先证伪（勿重跑）：`scripts/_phase102_p7_5e209_dn_minus1_linear_factor.py` + 同目录 json
（XX1~XX5 全 ok=true，2026-10-16）。

核心内容（登记原文 209 ⑨）：
- XX1：D(n)−1 = 2^(n−1)·(7n+2)——闭式分母的 '−1 结构' = 2 的幂 × 线性因子，n 依赖显式；
- XX2：1/B*(n)（129 闭式 n/2+1/7+1/(7·2^n)，n≥1）合并为单分数 = D(n)/(7·2^n)；
- XX3：n=1 例外——真实 1/B*(1)=332/455=332/(7·65)，分母从 7·2=14 放大到 7·65=455（+1/65 修正的机制=分母放大）；
- XX4：7n+2 命中框架量仅 n=9（65=8²+1 修正锚点）、n=10（72=8·9 满格×静默单元）；n=11..16（79/86/93/100/107/114）非静默类；
- XX5：65 三重核对（8²+1 = 7·8+9 = 5·13，7·9+2 归约——代数等价非新身份）。

诚实边界：XX1/XX2 代数恒等（闭式展开/合并直接给出）、XX3 闭式 129 定义的直接结果、
XX4 枚举事实、XX5 核对无新身份——候选层未升定案层。
-/

namespace MUFPF.DenominatorPrimacy

open MUFPF.CoreConstantWindow

/-- XX1：D(n)−1 = 2^(n−1)·(7n+2)——Dn 定义直接展开（Nat 截断减下 n=0 亦成立）。 -/
theorem dn_minus1_linear_factor (n : ℕ) : Dn n - 1 = 2^(n-1) * (7*n + 2) := by
  rw [xx1_dn]
  exact Nat.add_sub_cancel (2^(n-1) * (7*n + 2)) 1

/-- 129 闭式 1/B*(n) = n/2 + 1/7 + 1/(7·2^n)（通道闭式；n=1 时 = 5/7 纯闭式，真实值需 +1/65 修正见 XX3）。 -/
noncomputable def bstarClosed (n : ℕ) : ℚ := (n : ℚ) / 2 + 1 / 7 + 1 / (7 * (2 : ℚ) ^ n)

/-- XX2：1/B*(n) = D(n)/(7·2^n)（n≥1，闭式合并单分数——代数恒等）。 -/
theorem bstar_closed_den (k : ℕ) :
    bstarClosed (k + 1) = (Dn (k + 1) : ℚ) / (7 * (2 : ℚ) ^ (k + 1)) := by
  unfold bstarClosed
  rw [show Dn (k + 1) = 2 ^ k * (7 * (k + 1) + 2) + 1 by
    rw [xx1_dn]
    simp]
  rw [pow_succ]
  field_simp
  norm_cast
  ring_nf

/-- XX3：n=1 纯闭式 = 5/7（未修正）。 -/
theorem bstar1_closed_plain : bstarClosed 1 = 5 / 7 := by
  unfold bstarClosed
  norm_num

/-- XX3：真实 1/B*(1) = 5/7 + 1/65 = 332/455（引用 278 b1_seed_frac——+1/65 修正）。 -/
theorem bstar1_corrected : (5 : ℚ) / 7 + 1 / 65 = 332 / 455 :=
  MUFPF.PowerTwoSilent.b1_seed_frac

/-- XX3：修正后 ≠ 纯闭式（差 = 1/65——修正非平凡）。 -/
theorem bstar1_corrected_ne_plain : bstarClosed 1 ≠ 332 / 455 := by
  unfold bstarClosed
  norm_num

/-- XX3：分母放大机制 7·2=14 → 7·65=455（修正 = 分母放大）。 -/
theorem den_correction : 7 * 2 = 14 ∧ 7 * 65 = 455 := by
  norm_num

/-- XX4：7n+2 命中 n=9：65 = 8²+1 修正锚点。 -/
theorem lf_n9 : 7 * 9 + 2 = 65 ∧ 65 = 8^2 + 1 := by
  norm_num

/-- XX4：7n+2 命中 n=10：72 = 8·9 满格×静默单元。 -/
theorem lf_n10 : 7 * 10 + 2 = 72 ∧ 72 = 8 * 9 := by
  norm_num

/-- XX4：n=11..16 线性因子值 {79,86,93,100,107,114} 枚举核对。 -/
theorem lf_nonhit_values :
    (7 * 11 + 2 = 79) ∧ (7 * 12 + 2 = 86) ∧ (7 * 13 + 2 = 93) ∧
    (7 * 14 + 2 = 100) ∧ (7 * 15 + 2 = 107) ∧ (7 * 16 + 2 = 114) := by
  norm_num

/-- XX4：n=11..16 非静默类（7n+2 的 mod 8 值 {7,6,5,4,3,2} 全 ≠1）。 -/
theorem lf_non_silent :
    (7 * 11 + 2) % 8 ≠ 1 ∧ (7 * 12 + 2) % 8 ≠ 1 ∧ (7 * 13 + 2) % 8 ≠ 1 ∧
    (7 * 14 + 2) % 8 ≠ 1 ∧ (7 * 15 + 2) % 8 ≠ 1 ∧ (7 * 16 + 2) % 8 ≠ 1 := by
  norm_num

/-- XX5：65 三重核对（8²+1 = 7·8+9 = 5·13 代数等价；7·9+2 归约到 8²+1——非新身份）。 -/
theorem s65_check : 8^2 + 1 = 65 ∧ 7 * 8 + 9 = 65 ∧ 5 * 13 = 65 ∧ 7 * 9 + 2 = 65 := by
  norm_num

/-- 联合主定理：分母第一性闭合——XX1 线性因子分解 × XX2 闭式合并 × XX3 修正 × XX4 命中/枚举 × XX5 核对。 -/
theorem denominator_primacy_judgement :
    (∀ n : ℕ, Dn n - 1 = 2^(n-1) * (7*n + 2)) ∧
    (∀ k : ℕ, bstarClosed (k + 1) = (Dn (k + 1) : ℚ) / (7 * (2 : ℚ) ^ (k + 1))) ∧
    bstarClosed 1 = 5 / 7 ∧
    (5 : ℚ) / 7 + 1 / 65 = 332 / 455 ∧
    bstarClosed 1 ≠ 332 / 455 ∧
    7 * 9 + 2 = 65 ∧
    7 * 10 + 2 = 72 ∧
    (7 * 11 + 2) % 8 ≠ 1 ∧ (7 * 12 + 2) % 8 ≠ 1 ∧ (7 * 13 + 2) % 8 ≠ 1 ∧
    (7 * 14 + 2) % 8 ≠ 1 ∧ (7 * 15 + 2) % 8 ≠ 1 ∧ (7 * 16 + 2) % 8 ≠ 1 ∧
    8^2 + 1 = 65 ∧
    5 * 13 = 65 := by
  constructor
  · intro n
    exact dn_minus1_linear_factor n
  constructor
  · intro k
    exact bstar_closed_den k
  constructor
  · exact bstar1_closed_plain
  constructor
  · exact bstar1_corrected
  constructor
  · exact bstar1_corrected_ne_plain
  constructor
  · norm_num
  constructor
  · norm_num
  constructor
  · norm_num
  constructor
  · norm_num
  constructor
  · norm_num
  constructor
  · norm_num
  constructor
  · norm_num
  constructor
  · norm_num
  constructor
  · norm_num
  · norm_num

end MUFPF.DenominatorPrimacy
