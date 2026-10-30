/-
  KappaLambdaAxioms.lean — L14 κΛ 机制动机公理化定理（Phase 104az-144/146）
  =======================================================

  公理 A1（主结构）：κΛ 主结构 = 2·k_max·静默² = 不动点²×静默² = 16×25 = 400
  公理 A2（对合折叠修正）：修正量 = 1 + 1/S(k)，k = k_max，S(k) = 对合折叠对称积

  定理清单 T1–T6（全部纯代数、零 sorry、零 axiom）：
    T1 S(8) = 231            —— InvolutionTripleGap.symprod_8（既有）
    T2 gcd(231, 232) = 1     —— 232/231 最简
    T3 400×(232/231) = (2·k_max·静默²)×(1+1/231)  —— κΛ 恒等分解
    T4 S(k) 在 k∈{4..12} 无 230/232 命中（有限枚举判别）
    T5 231 = 3·7·11 唯一分解  —— symprod_factor（既有）+ Nat 素性
    T6 {230,231,232} 中唯一 S(k) 命中 = 231（链内唯一性——104az-142 代数封闭）

  先证伪（模式 8）：scripts/falsify_T1T6.py——Fraction 精确验证全部成立。

  诚实边界：A1/A2 为机制公设；T1–T6 证明"修正量的代数身份"，
  不证明"机制动机的唯一性"——后者需预言 C 观测裁决（104az-114）。
-/

import Mathlib.Tactic
import MUFPFormalization.InvolutionTripleGap

namespace MUFPF.KappaLambda

open MUFPF.InvolutionGap

/-! =========================================================
    公理 A1：主结构 = 2·k_max·静默² = 400
   ========================================================= -/

/-- 主结构恒等：2·k_max·静默² = 2·8·5² = 400（公理 A1 的数值内容）。 -/
theorem main_structure : (400 : ℝ) = 2 * (8 : ℝ) * (5 : ℝ) ^ 2 := by
  norm_num

/-- 主结构的第二表达：400 = 不动点²×静默² = 4²×5²（16×25）。 -/
theorem main_structure_fp : (400 : ℝ) = (4 : ℝ) ^ 2 * (5 : ℝ) ^ 2 := by
  norm_num

/-! =========================================================
    T2：gcd(231, 232) = 1（232/231 最简分数）
   ========================================================= -/

/-- T2：对合修正分母 231 与内生化分母 232 互质——(232/231) 为最简分数。 -/
theorem T2_gcd : Nat.gcd 231 232 = 1 := by
  norm_num

/-! =========================================================
    T3：κΛ 恒等分解 400×(232/231) = (2·k_max·静默²)·(1+1/231)
   ========================================================= -/

/-- T3：κΛ 内生化候选的恒等分解——主结构 × 对合折叠修正
    400×(232/231) = 400×(1+1/231) = (2·k_max·静默²)×(1+1/S(8))。 -/
theorem T3_kappa_decomp :
    (400 : ℝ) * (232 / 231 : ℝ) = (2 * (8 : ℝ) * (5 : ℝ) ^ 2) * (1 + 1 / symprodS 8) := by
  rw [symprod_8]
  norm_num

/-! =========================================================
    T4：S(k) 在 k∈{4..12} 无 230/232 命中
   ========================================================= -/

/-- T4：对合折叠对称积在推广域 k∈{4..12} 上不取 230/232
    （κΛ 邻域 {230,232} 非对合折叠产物——104az-142 链溯源判别）。 -/
theorem T4_no_neighbor_hit :
    ∀ k : ℕ, 4 ≤ k → k ≤ 12 →
      symprodS (k : ℝ) ≠ 230 ∧ symprodS (k : ℝ) ≠ 232 := by
  intro k hk4 hk12
  interval_cases k <;> norm_num [symprodS]

/-! =========================================================
    T5：231 素分解唯一（配合 InvolutionTripleGap.symprod_factor）
   ========================================================= -/

/-- T5：231 的三因子 3/7/11 均为素数（唯一分解的素因子基础）。 -/
theorem T5_prime_decomp : Nat.Prime 3 ∧ Nat.Prime 7 ∧ Nat.Prime 11 := by
  norm_num

/-! =========================================================
    T6：{230,231,232} 中唯一 S(k) 命中 = 231
   ========================================================= -/

/-- T6：κΛ 邻域 {230,231,232} 中，S(k)（k∈{4..12}）的唯一命中是 231
    ——链内唯一性（104az-142 的代数封闭：230/232 异链、231 对合折叠链内唯一）。 -/
theorem T6_unique_hit :
    ∀ k : ℕ, 4 ≤ k → k ≤ 12 →
      symprodS (k : ℝ) = 230 ∨ symprodS (k : ℝ) = 231 ∨ symprodS (k : ℝ) = 232 →
      symprodS (k : ℝ) = 231 := by
  intro k hk4 hk12 hwin
  have hnot := T4_no_neighbor_hit k hk4 hk12
  rcases hwin with h230 | h231 | h232
  · exfalso
    exact hnot.1 h230
  · exact h231
  · exfalso
    exact hnot.2 h232

/-! =========================================================
    汇总定理：公理化骨架（A1 + T2–T6 合取）
   ========================================================= -/

/-- 公理化骨架总定理：主结构恒等 ∧ 互质 ∧ κΛ 恒等分解 ∧ 无邻域命中 ∧ 素性 ∧ 链内唯一。 -/
theorem axiom_skeleton :
    (400 : ℝ) = 2 * (8 : ℝ) * (5 : ℝ) ^ 2 ∧
    Nat.gcd 231 232 = 1 ∧
    (400 : ℝ) * (232 / 231 : ℝ) = (2 * (8 : ℝ) * (5 : ℝ) ^ 2) * (1 + 1 / symprodS 8) ∧
    (∀ k : ℕ, 4 ≤ k → k ≤ 12 → symprodS (k : ℝ) ≠ 230 ∧ symprodS (k : ℝ) ≠ 232) ∧
    (Nat.Prime 3 ∧ Nat.Prime 7 ∧ Nat.Prime 11) ∧
    (∀ k : ℕ, 4 ≤ k → k ≤ 12 →
      symprodS (k : ℝ) = 230 ∨ symprodS (k : ℝ) = 231 ∨ symprodS (k : ℝ) = 232 →
      symprodS (k : ℝ) = 231) := by
  constructor
  · exact main_structure
  · constructor
    · exact T2_gcd
    · constructor
      · exact T3_kappa_decomp
      · constructor
        · exact T4_no_neighbor_hit
        · constructor
          · exact T5_prime_decomp
          · exact T6_unique_hit

end MUFPF.KappaLambda
