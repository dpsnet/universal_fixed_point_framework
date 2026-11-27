/-
  ReverseReadoutAudit.lean — 逆向读数审计：读数能否反定范畴参数？
  ==================================================================

## 要判的是什么

`CategoryPhysicsCoupling.lean` §4 已经造出第一条跨层定理：

    K₄ / m = deflectionStep4Coeff = B ^ 2 / 32 = 225 / 32

其中 `deflectionStep4Coeff` 的定义体含范畴阶 `catOrder`。§13 结尾登记了下一步：
「构造两个不同的范畴参数赋值，使物理读数完全相同」——若造得出，逆向多解就从推断
变成机检结论；若造不出（读数可唯一反定 `catOrder`），那是更强的好消息。

本模块把两种可能**同时**机检，不预设答案。

## 三条待判命题

| 编号 | 命题 | 判什么 |
|---|---|---|
| ① | `stepCoeff` 严格单调 ⟹ 单射 | 连续物理读数能否唯一反定窗口长度 |
| ② | `routeLayerPair` 非单射（15 有四解） | 离散读数（分支数 15）能否唯一反定「层对」赋值 |
| ③ | `routeOrder` 在 n ≥ 1 上单射 | 离散读数能否唯一反定范畴阶 |

## 结果（先给结论，证明在下面）

- ① **成立**：`stepCoeff` 严格递增，故读数 `K₄/m` 唯一确定 `n`，进而唯一确定
  `catOrder = 4`。连续读数这条路，逆向是**单解**的。
- ② **成立**：`routeLayerPair (1,15) = routeLayerPair (3,5) = routeLayerPair (5,3)
  = routeLayerPair (15,1) = 15`。分支数 15 在层对路线下有**四解**，框架取 (3,5)
  只是其中之一，且读数本身不携带「取哪一个」的信息。
- ③ **成立**：`routeOrder` 在 `n ≥ 1` 上单射，故 15 在范畴阶路线上唯一给出 `n = 4`。

⇒ **逆向的可逆性取决于路线，不取决于读数。** 同一个 15，走因子路线多解、走阶路线
单解。这是「逆向 = 约化，不是重构」的机检版本：读数能把参数压到唯一，但压不出
「这个参数是从哪条路线产生的」。

## 诚实边界

1. ① 证明的是「读数 ⟹ 窗口长度唯一」，**不是**「读数 ⟹ 范畴结构唯一」。窗口长度
   被取为 `catOrder` 本身是 `CategoryPhysicsCoupling` 的定义选择，不是物理强制。
2. ② 的「四解」是**算术事实**（15 的因子对），不是新物理。它的意义在于：第 63 批
   把 `B = 3 × 5` 读作层对计数时，该读数在原理上无法排除 `1 × 15` 之类的读法；
   排除靠的是层的语义（主动层数 3、总层数 5），不是靠读数。
3. ③ 的单射性只对 `n ≥ 1` 成立：`n = 0` 时 `0² − 1` 在 `ℕ` 上截断取 0，与 `n = 1`
   的 0 重合。这不是缺陷，是 `ℕ` 截断减法的边界，须写明。
4. 本模块不主张「物理读数等于 `stepCoeff`」。它主张的是：**若**取该读数，**则**逆向
   唯一；这条蕴含是本模块的全部内容。
-/

import Mathlib.Analysis.Complex.Trigonometric
import Mathlib.Tactic
import MUFPFormalization.CategoryPhysicsCoupling

open MUFPF.CategoryPhysicsCoupling
open MUFPF.CategoryOrder

namespace MUFPF.ReverseReadoutAudit

/-! =========================================================
    §1 物理侧读数：n 步窗口能量系数的闭式
   =========================================================
-/

/-- `n` 步偏转窗口的能量系数闭式 `K_n / m = (2^n − 1)² / 2^(n+1)`。

    `n = 4` 时 `225/32`（`CategoryPhysicsCoupling.deflectionStep4Coeff_eq_rational`）。 -/
noncomputable def stepCoeff (n : ℕ) : ℝ :=
  ((2 : ℝ) ^ n - 1) ^ 2 / ((2 : ℝ) ^ (n + 1))

/-- 该读数就是 §4 的物理量：`deflectionStep4Coeff = stepCoeff catOrder`。 -/
theorem readout_eq :
    deflectionStep4Coeff = stepCoeff catOrder := by
  rw [deflectionStep4Coeff_eq_silent_sq]
  rfl

/-! =========================================================
    §2 判①：读数严格递增 ⟹ 单射 ⟹ 唯一反定窗口长度
   =========================================================

    差分形式：`stepCoeff (n+1) − stepCoeff n = (2 · (2^n)² − 1) / (4 · 2^n)`。
    分子在 `2^n ≥ 1` 时恒正（`2a² − 1 ≥ 1 > 0`），分母恒正，故严格递增。
-/

/-- 相邻两读数之差。 -/
theorem stepCoeff_succ_sub (n : ℕ) :
    stepCoeff (n + 1) - stepCoeff n
      = (2 * ((2 : ℝ) ^ n) ^ 2 - 1) / (4 * (2 : ℝ) ^ n) := by
  unfold stepCoeff
  rw [pow_add (2 : ℝ) n 2, pow_add (2 : ℝ) n 1]
  norm_num
  field_simp
  ring

/-- **严格递增**：`stepCoeff n < stepCoeff (n+1)`。 -/
theorem stepCoeff_succ_gt (n : ℕ) : stepCoeff n < stepCoeff (n + 1) := by
  have ha1 : (1 : ℝ) ≤ (2 : ℝ) ^ n := by
    induction n with
    | zero => norm_num
    | succ k ih =>
      rw [pow_succ]
      nlinarith
  have hdiff := stepCoeff_succ_sub n
  have hnum : (0 : ℝ) < 2 * ((2 : ℝ) ^ n) ^ 2 - 1 := by nlinarith
  have hden : (0 : ℝ) < 4 * (2 : ℝ) ^ n := by positivity
  have hpos : (0 : ℝ) < stepCoeff (n + 1) - stepCoeff n := by
    rw [hdiff]
    exact div_pos hnum hden
  linarith

/-- `stepCoeff` 在 `ℕ` 上严格单调。 -/
theorem stepCoeff_strictMono : StrictMono stepCoeff :=
  strictMono_nat_of_lt_succ stepCoeff_succ_gt

/-- **单射**：不同窗口长度给出不同读数。 -/
theorem stepCoeff_injective : Function.Injective stepCoeff :=
  stepCoeff_strictMono.injective

/-- 判①的判决：**读数唯一反定窗口长度**。

    给定任一 `n`，若其读数为 `K₄/m`，则 `n = catOrder = 4`。 -/
theorem readout_recovers_order (n : ℕ)
    (h : stepCoeff n = deflectionStep4Coeff) : n = catOrder := by
  have h' : stepCoeff n = stepCoeff catOrder := by
    rw [← readout_eq]
    exact h
  exact stepCoeff_injective h'

/-- 上条的数值化形式：读到 `225/32` 就只能是 4 步窗口。 -/
theorem readout_recovers_four (n : ℕ)
    (h : stepCoeff n = 225 / 32) : n = 4 := by
  have h' : stepCoeff n = deflectionStep4Coeff := by
    rw [deflectionStep4Coeff_eq_rational]
    exact h
  have := readout_recovers_order n h'
  rw [this]
  rfl

/-! =========================================================
    §3 判②：离散读数 15 在「层对路线」下有四解
   =========================================================
-/

/-- 层对路线：给定（主动层数，总层数）读出分支数。 -/
def routeLayerPair (p : ℕ × ℕ) : ℕ := p.1 * p.2

/-- 15 在层对路线下的四个原像：`1×15`、`3×5`、`5×3`、`15×1`。 -/
theorem routeLayerPair_fiber_four :
    routeLayerPair (1, 15) = 15 ∧ routeLayerPair (3, 5) = 15 ∧
    routeLayerPair (5, 3) = 15 ∧ routeLayerPair (15, 1) = 15 := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> norm_num [routeLayerPair]

/-- **多解**：框架取的 `(3,5)` 不是唯一原像——存在另一个赋值给出同一读数。 -/
theorem layer_route_underdetermined :
    ∃ p : ℕ × ℕ, p ≠ (3, 5) ∧ routeLayerPair p = routeLayerPair (3, 5) :=
  ⟨(1, 15), by norm_num, by norm_num [routeLayerPair]⟩

/-- **非单射**（判②的判决）：层对路线不能由读数反定赋值。 -/
theorem routeLayerPair_not_injective : ¬ Function.Injective routeLayerPair := by
  intro h
  have hne : (3, 5) ≠ (5, 3) := by norm_num
  have heq : routeLayerPair (3, 5) = routeLayerPair (5, 3) := by
    norm_num [routeLayerPair]
  exact hne (h heq)

/-! =========================================================
    §4 判③：离散读数 15 在「范畴阶路线」下唯一
   =========================================================
-/

/-- 范畴阶路线（ℝ 值口径）：`B = n² − 1`。

    取 ℝ 值而非 ℕ 值，是为了避开 `ℕ` 截断减法在 `n = 0` 处的伪重合
    （`0² − 1` 截断为 `0`，与 `1² − 1` 相同）。对 `n ≥ 1` 两者数值一致。 -/
noncomputable def routeOrder (n : ℕ) : ℝ := (n : ℝ) ^ 2 - 1

/-- **单射（n ≥ 1）**：`n² − 1 = m² − 1 ⟹ n = m`。 -/
theorem routeOrder_inj (n m : ℕ) (hn : 1 ≤ n) (hm : 1 ≤ m)
    (h : routeOrder n = routeOrder m) : n = m := by
  unfold routeOrder at h
  have hc : ((n : ℝ)) ^ 2 = ((m : ℝ)) ^ 2 := by linarith
  have hfac : ((n : ℝ) - (m : ℝ)) * ((n : ℝ) + (m : ℝ)) = 0 := by
    calc ((n : ℝ) - (m : ℝ)) * ((n : ℝ) + (m : ℝ))
        = ((n : ℝ)) ^ 2 - ((m : ℝ)) ^ 2 := by ring
      _ = 0 := by linarith
  have hn0 : (0 : ℝ) < (n : ℝ) := by exact_mod_cast (by omega : 0 < n)
  have hm0 : (0 : ℝ) < (m : ℝ) := by exact_mod_cast (by omega : 0 < m)
  have hpos : (0 : ℝ) < ((n : ℝ)) + ((m : ℝ)) := by linarith
  have hnm : ((n : ℝ)) = ((m : ℝ)) := by
    rcases mul_eq_zero.mp hfac with h1 | h1
    · linarith
    · linarith
  exact_mod_cast hnm

/-- 判③的判决：读到 15 就只能是 `n = 4`（在阶路线上）。 -/
theorem routeOrder_recovers_four (n : ℕ) (hn : 1 ≤ n) (h : routeOrder n = 15) : n = 4 := by
  have h4 : routeOrder 4 = 15 := by norm_num [routeOrder]
  have := routeOrder_inj n 4 hn (by norm_num) (h.trans h4.symm)
  exact this

/-! =========================================================
    §5 判决汇总：可逆性取决于路线，不取决于读数
   =========================================================
-/

/-- **本条即本模块的结论**：

    1. 连续读数（窗口能量系数）严格递增 ⟹ 单射 ⟹ 可唯一反定窗口长度；
    2. 离散读数 15 走层对路线 ⟹ 非单射 ⟹ 四解；
    3. 离散读数 15 走范畴阶路线 ⟹ 单射 ⟹ 唯一反定 `n = 4`。

    ⇒ 同一个读数 `15`，在两条路线上给出「多解」与「单解」两种结果。
      读数本身不携带「走的是哪条路线」的信息，故逆向只能约化到参数，
      不能约化到产生参数的结构。 -/
theorem reverse_readout_verdict :
    Function.Injective stepCoeff ∧
    ¬ Function.Injective routeLayerPair ∧
    (∀ n m : ℕ, 1 ≤ n → 1 ≤ m → routeOrder n = routeOrder m → n = m) :=
  ⟨stepCoeff_injective, routeLayerPair_not_injective, routeOrder_inj⟩

/-- 结论的否定形式（同一读数、不同可逆性）：

    存在两个读数函数 `f = routeLayerPair ∘ (·,·)` 与 `g = routeOrder`，
    使 `f (3,5) = g 4 = 15`，而 `f` 非单射、`g` 在 `n ≥ 1` 上单射。
    即「读数相同 ⟹ 逆向唯一性相同」不成立。 -/
theorem reversibility_is_route_dependent :
    (routeLayerPair (3, 5) : ℝ) = routeOrder 4 ∧
    ¬ Function.Injective routeLayerPair ∧
    (∀ n m : ℕ, 1 ≤ n → 1 ≤ m → routeOrder n = routeOrder m → n = m) := by
  refine ⟨?_, routeLayerPair_not_injective, routeOrder_inj⟩
  norm_num [routeLayerPair, routeOrder]

end MUFPF.ReverseReadoutAudit
