/-
# TowerCeilingTimeClosure.lean — G5：5 = 时间闭 ⇒ 塔止 2⁴（P7-5e-361）
=========================================================================

对应 `P7-5e_最新研究成果_2026-10-30.md` 第六十四节（G5：下游可延——
「5 = 时间闭机检化，M-time」），只把「塔止 2⁴」由**条件必然**升为**条件定理**，
不动任何读数。

## 本文件做什么

把六十三节的三条条件写成**显式假设**，再机检其推论：

  · 条件 1｜递归即时间：开放步是 ℕ 链（前缀性 `hpre`）；
  · 条件 2｜5 = 时间闭：第 5 步冻结（`¬ Steps 5`）；
  · 条件 3｜Δφ = ln2、4 步全代数：第 4 步开放（`Steps 4`）；
  · I-V1 候选（4 sinh ln2 = 3、4 cosh ln2 = 5）的算子读数机检。

## 定理清单

  · `closure_eq_five` / `closure_eq_succ`：5 = 4 + 1（韦达根和 / 单步 γ 分母）；
  · `state_open` / `state_closure`：2⁴ = 16、2⁵ = 32 = 2 × 2⁴；
  · `tower_ceiling`：★ 给定「前缀性 + 第 4 步开放 + 第 5 步不开放」，
    任何开放步 n 都满足 n ≤ 4（塔止 2⁴）；
  · `four_is_last_open`：第 4 步开放 ∧ 第 5 步不开放 ∧ 所有开放步 ≤ 4；
  · `four_sinh_log_two` / `four_cosh_log_two`：4 sinh(ln2) = 3、4 cosh(ln2) = 5；
  · `g5_conditional_backbone`：以上并置。

## 诚实边界（必须原样保留）

  · **条件定理 ≠ 范畴导出**：`tower_ceiling` 把三条条件作为**假设**；
    三条本身（尤其「5 = 时间闭」是语义指认 + 机检算术）**未从范畴导出**；
  · Rec ↔ 模流桥 P1–P4 仍「未定义」⇒ 范畴级必然性未闭合（与六十三节同口径）；
  · 不动任何读数：本文件不含任何新的物理数值，2⁴/2⁵ 只作计数；
  · 「为何指数必须落地」的机制仍未给出；M-time 仍只是候选，不升定案层；
  · **G5 未闭合**。不关闭任何项（226 挂起、k(2) 开放）。
-/

import Mathlib.Tactic
import MUFPFormalization.KMaxAlgebra

namespace MUFPF.TowerCeilingTimeClosure

/-! =========================================================
    §1 两个计数：最后开放步 4、时间闭 5
   ========================================================= -/

/-- 最后开放递归步数（Δφ = ln2 下 2⁴ = 16 为全态）。 -/
def openStepCount : ℕ := 4

/-- 时间闭单元（静默 5 = 冻结区整点数）。 -/
def closureUnit : ℕ := 5

/-- 时间闭 = 最后开放步 + 1（5 = 4 + 1；韦达根和 / 单步 γ 分母读数）。 -/
theorem closure_eq_succ : closureUnit = openStepCount + 1 := by
  norm_num [closureUnit, openStepCount]

/-- 时间闭单元 = 5（共享 G4 静默单元；本文件不重证其来源）。 -/
theorem closure_eq_five : closureUnit = 5 := by
  norm_num [closureUnit]

/-- 开放全态计数 = 16 = 2⁴。 -/
theorem state_open : 2 ^ openStepCount = 16 := by
  norm_num [openStepCount]

/-- 时间闭处的态计数 = 32 = 2 × 2⁴（非开放态空间的计数层定位）。 -/
theorem state_closure : 2 ^ closureUnit = 2 * 2 ^ openStepCount := by
  norm_num [closureUnit, openStepCount]

/-! =========================================================
    §2 ★ 条件定理：塔止 2⁴
   ========================================================= -/

/-- ★★ 塔止 2⁴（条件定理）：给定
    (i) 前缀性（递归步一旦开放，其下各步皆开放）；
    (ii) 第 4 步开放（Δφ = ln2 与 4 步全代数）；
    (iii) 第 5 步不开放（5 = 时间闭），
    则第 4 步开放且任何开放步 n 满足 n ≤ 4（塔止 2⁴）。
    ※ 三条均为**假设**，本定理不声称其从范畴导出。 -/
theorem tower_ceiling (Steps : ℕ → Prop)
    (hpre : ∀ n m : ℕ, Steps n → m ≤ n → Steps m)
    (open_four : Steps 4) (closed_five : ¬ Steps 5) :
    Steps 4 ∧ ∀ n : ℕ, Steps n → n ≤ 4 := by
  refine ⟨open_four, ?_⟩
  intro n hn
  by_contra h
  have h5n : 5 ≤ n := by omega
  exact closed_five (hpre n 5 hn h5n)

/-- 与 tower_ceiling 等价的「无开放步越过时间闭」。 -/
theorem no_open_step_at_closure (Steps : ℕ → Prop)
    (hpre : ∀ n m : ℕ, Steps n → m ≤ n → Steps m) (closed_five : ¬ Steps 5) :
    ¬ Steps 5 ∧ ∀ n : ℕ, Steps n → n < 5 := by
  refine ⟨closed_five, ?_⟩
  intro n hn
  have h4 : n ≤ 4 := by
    by_contra h
    have h5n : 5 ≤ n := by omega
    exact closed_five (hpre n 5 hn h5n)
  omega

/-- ★ 第 4 步是最后开放步：开放 ∧ 第 5 步不开放 ∧ 所有开放步 ≤ 4。 -/
theorem four_is_last_open (Steps : ℕ → Prop)
    (hpre : ∀ n m : ℕ, Steps n → m ≤ n → Steps m)
    (open_four : Steps 4) (closed_five : ¬ Steps 5) :
    Steps openStepCount ∧ ¬ Steps closureUnit ∧
      ∀ n : ℕ, Steps n → n ≤ openStepCount := by
  refine ⟨?_, ?_, ?_⟩
  · norm_num [openStepCount]; exact open_four
  · norm_num [closureUnit]; exact closed_five
  · intro n hn
    exact (tower_ceiling Steps hpre open_four closed_five).2 n hn

/-! =========================================================
    §3 I-V1 候选的算子读数（4 sinh ln2 = 3、4 cosh ln2 = 5）
   ========================================================= -/

/-- 4 sinh(ln 2) = 3：时间开的算子读数（奇支 / 推进）。 -/
theorem four_sinh_log_two : 4 * Real.sinh (Real.log 2) = 3 := by
  rw [Real.sinh_eq]
  rw [Real.exp_log (by norm_num : (0 : ℝ) < 2)]
  rw [Real.exp_neg, Real.exp_log (by norm_num : (0 : ℝ) < 2)]
  norm_num

/-- 4 cosh(ln 2) = 5：时间闭的算子读数（偶支 / 闭合）。 -/
theorem four_cosh_log_two : 4 * Real.cosh (Real.log 2) = 5 := by
  rw [Real.cosh_eq]
  rw [Real.exp_log (by norm_num : (0 : ℝ) < 2)]
  rw [Real.exp_neg, Real.exp_log (by norm_num : (0 : ℝ) < 2)]
  norm_num

/-- I-V1 候选的韦达对：{4 sinh ln2, 4 cosh ln2} = {3, 5}，和 8、积 15。 -/
theorem iv1_vieta_pair :
    4 * Real.sinh (Real.log 2) = 3 ∧ 4 * Real.cosh (Real.log 2) = 5 ∧
      (3 + 5 = 8 ∧ 3 * 5 = 15) := by
  refine ⟨four_sinh_log_two, four_cosh_log_two, ?_, ?_⟩
  · norm_num
  · norm_num

/-! =========================================================
    §4 总装：G5 条件骨架
   ========================================================= -/

/-- G5 条件骨架：5 = 4 + 1 ∧ 2⁴ = 16 ∧ 2⁵ = 2×2⁴ ∧ I-V1 读数 ∧
    （Given 三条件）塔止 2⁴。※ 条件定理，非范畴导出；G5 未闭合。 -/
theorem g5_conditional_backbone :
    closureUnit = openStepCount + 1 ∧
      2 ^ openStepCount = 16 ∧ 2 ^ closureUnit = 2 * 2 ^ openStepCount ∧
      (4 * Real.sinh (Real.log 2) = 3 ∧ 4 * Real.cosh (Real.log 2) = 5) ∧
      (∀ (Steps : ℕ → Prop),
        (∀ n m : ℕ, Steps n → m ≤ n → Steps m) → Steps 4 → ¬ Steps 5 →
          Steps 4 ∧ ∀ n : ℕ, Steps n → n ≤ 4) := by
  refine ⟨closure_eq_succ, state_open, state_closure, ?_, ?_⟩
  · exact ⟨four_sinh_log_two, four_cosh_log_two⟩
  · intro Steps hpre open_four closed_five
    exact tower_ceiling Steps hpre open_four closed_five

end MUFPF.TowerCeilingTimeClosure
