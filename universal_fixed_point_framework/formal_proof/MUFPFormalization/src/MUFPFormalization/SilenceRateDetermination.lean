/-
# 静默率 `r = e⁻¹` 的地位审计

## 本批要回答的问题

第 54 批把注入点收窄为三项：**建模层（含 `f² = 2^f`）、`N_total = 5`、`r = e⁻¹`**。
本批攻第三项，方法是先查它在库内的**真实地位**，而不是先假设它有来由。

## 勘察事实（逐字核读，非推测）

`DHStructuralAnalysis.lean` L83 与 L117 都写「`r = e⁻¹`（信息论最优静默因子，**定理 R1**）」，
同文件第六章 L556 把它标为「`[✅] 步骤 2`：证明在零阶近似下分支均匀收缩 `r = e⁻¹`」。
但同文件 L118 只有：

    noncomputable def r : ℝ := Real.exp (-1)

⇒ `r` 是**裸定义**，其 doc 声称的「定理 R1」在库内并不承担这个任务。

那么「定理 R1」是什么？库内同名定理只有一处：

    RAP1_weight_uniqueness.lean L16：RAP-1: 定理 R1 — 加权严格 n-范畴权重函数的唯一性

其陈述（L19–25）：权重 `w : {1,…,n} → (0,1]` 满足
(W1) 只依赖层级、(W2) 复合乘性 `w_{k+l} = w_k · w_l`、(W3) 归一化 `w_1 = s ∈ (0,1]`，
则该权重恰为 `w_k = s^k`。

**⇒ R1 的输出是「形式 = 指数族」，`s` 是自由参数，R1 对 `s` 的值一无所知。**
`weight_uniqueness`（L60）的签名也确认这一点：它对**任意** `s` 成立。

⇒ 所以「`r = e⁻¹` 来自定理 R1」是**误标**：R1 给的是 `r = s^k` 这个族，
不是 `s = e⁻¹` 这个点。`CoherenceToBranching.lean` L408 自己写「~~目前只有信息论动机（定理 R1）~~」，
`DHThreeSources.lean` L61–62 也写「**不证「`r = e⁻¹` 必然」**……本文件不重证 R1」——
两处都已承认 R1 不含此值。

## 本批证明什么

既然 R1 不锁值，`r = e⁻¹` 的**唯一可利用结构**就只能是它与 `d_H` 的关系。
本批证明：

    （给定 B = 15）「Moran 方程的解恰为 d = ln 15」 ⟺ 「s = e⁻¹」

⇒ 即：`r = e⁻¹` 与 `d_H = ln 15` **不是两条独立信息，而是同一个条件的两种写法**。
这与第 54 批对 `σ⁻¹` 两形式的处理完全同构（那次是 `f²−1` 与 `2^f−1` 归约到 `f² = 2^f`）。

## 本批的裁决

- `r = e⁻¹` 与 `d_H = ln 15` 二者只能算**一个**注入点，不是两个；
- 「信息论最优」这条独立动机在库内**零机检**，本批不补，登记为开口；
- 唯象上二者也不精确对齐：`d_fit = 2.7095` 反推得 `s = 0.368076`，
  与 `e⁻¹ = 0.367879` 相对偏差 `5.35 × 10⁻⁴`，正是 `δ = 0.00145` 的来源。
  ⇒ `s = e⁻¹` 在拟合意义上同样**不是精确值**。

## 与既有模块的关系

- `DHStructuralAnalysis`：提供 `ln15`、`r`、`moran_solution_iff`。
- `RAP1_weight_uniqueness`：提供 `weight_uniqueness`（形式侧）。
- 本批不 import `Rec` / `Sp`，只在实数层做「率 ↔ 维数」的等价判定。
-/

import Mathlib.Tactic
import MUFPFormalization.DHStructuralAnalysis

namespace MUFPF.SilenceRate

open MUFPF.DHStructural

/-! ## 一、R1 锁形式、不锁值 -/

/-- ★★ **R1 的形式侧对任意 `s` 成立**：`s^(k+l) = s^k · s^l`。

⇒ 这条恒等式对**所有**实数 `s` 成立，包括 `s ≠ e⁻¹`。所以「R1 成立」
不能推出「`s = e⁻¹`」——R1 的信息量止于「形式是指数族」。 -/
theorem cauchy_family_free (s : ℝ) :
    ∀ k l : ℕ, s ^ (k + l) = s ^ k * s ^ l := by
  intro k l
  exact pow_add s k l

/-- ★★ **`e⁻¹ ≠ e⁻²`**：指数族里不同参数给不同族。 -/
theorem exp_neg_one_ne_exp_neg_two : Real.exp (-1 : ℝ) ≠ Real.exp (-2 : ℝ) := by
  intro h
  have h' : (-1 : ℝ) = -2 := Real.exp_injective h
  norm_num at h'

/-- ★★ `e⁻¹ < 1`（供后文作 `0 < s < 1` 的实例）。 -/
theorem exp_neg_one_lt_one : Real.exp (-1 : ℝ) < 1 := by
  have h : (-1 : ℝ) < 0 := by norm_num
  calc
    Real.exp (-1 : ℝ) < Real.exp 0 := Real.exp_lt_exp.mpr h
    _ = 1 := Real.exp_zero

/-- ★★★ **R1 的净信息量**：形式对所有 `s` 成立，而不同的 `s` 给出不同的族。

⇒ 三句合起来说明「R1 之后 `s` 仍完全自由」——这是把 `r = e⁻¹` 从「定理推论」
降为「自由参数取的一个值」的机检依据。 -/
theorem r1_locks_form_not_value :
    (∀ s : ℝ, ∀ k l : ℕ, s ^ (k + l) = s ^ k * s ^ l) ∧
    Real.exp (-1 : ℝ) ≠ Real.exp (-2 : ℝ) ∧
    Real.exp (-1 : ℝ) < 1 :=
  ⟨cauchy_family_free, exp_neg_one_ne_exp_neg_two, exp_neg_one_lt_one⟩

/-! ## 二、主定理：`d = ln 15` 与 `s = e⁻¹` 是同一条件 -/

/-- ★★★ **给定 `B = 15`，要求 Moran 解恰为 `ln 15`，则收缩率唯一为 `e⁻¹`**。

证明：`15 · s^ln15 = 1` ⇒ `s^ln15 = 15⁻¹` ⇒ 取对数 ⇒ `ln 15 · ln s = −ln 15`
⇒ `ln 15 ≠ 0` ⇒ `ln s = −1` ⇒ `s = e⁻¹`。

⇒ 这条把「`r = e⁻¹`」从「独立假设」变成「`d_H = ln 15` 的等价表述」。 -/
theorem moran_pins_rate (s : ℝ) (hs : 0 < s) (hs1 : s < 1) :
    (15 : ℝ) * s ^ (Real.log 15) = 1 ↔ s = Real.exp (-1 : ℝ) := by
  have h15 : (0 : ℝ) < Real.log 15 := Real.log_pos (by norm_num)
  have h15ne : Real.log 15 ≠ 0 := ne_of_gt h15
  constructor
  · intro h
    have h1 : s ^ (Real.log 15) = (15 : ℝ)⁻¹ := eq_inv_of_mul_eq_one_right h
    have h2 : Real.log 15 * Real.log s = -(Real.log 15) := by
      have := congrArg Real.log h1
      rw [Real.log_rpow hs, Real.log_inv] at this
      exact this
    have h4 : Real.log s = -1 := by
      have hdiv := congrArg (fun x : ℝ => x / Real.log 15) h2
      field_simp at hdiv
      linarith
    calc
      s = Real.exp (Real.log s) := (Real.exp_log hs).symm
      _ = Real.exp (-1) := by rw [h4]
  · intro h
    subst h
    have hexp : Real.exp (-1 : ℝ) ^ (Real.log 15) = (15 : ℝ)⁻¹ := by
      rw [Real.rpow_def_of_pos (Real.exp_pos _), Real.log_exp]
      rw [show (-1 : ℝ) * Real.log 15 = -(Real.log 15) from by ring, Real.exp_neg,
        Real.exp_log (by norm_num : (0 : ℝ) < 15)]
    rw [hexp]
    exact mul_inv_cancel₀ (by norm_num : (15 : ℝ) ≠ 0)

/-- ★★ **率 ↔ 维数的一般双射**（`B = 15`）：`15 · s^d = 1 ⟺ d = ln 15 / (−ln s)`。

⇒ 这给出 `s` 与 `d` 的一一对应，故「固定 `s`」与「固定 `d`」是同一份约束。 -/
theorem moran_dim_from_rate (s d : ℝ) (hs : 0 < s) (hs1 : s < 1) :
    (15 : ℝ) * s ^ d = 1 ↔ d = (Real.log 15) / (-(Real.log s)) := by
  have h15 : (1 : ℝ) < 15 := by norm_num
  have h := moran_solution_iff (B := (15 : ℝ)) (r := s) (x := d) h15 hs hs1
  have hlog : Real.log (1 / s) = -(Real.log s) := by
    rw [Real.log_div one_ne_zero (ne_of_gt hs), Real.log_one, zero_sub]
  rw [hlog] at h
  exact h

/-- ★★★ **主裁决：`r = e⁻¹` 与 `d_H = ln 15` 是同一个条件，不是两条独立注入点**。

形式：对任意 `(s, d)`（`0 < s < 1`），

    （`15 · s^d = 1` 且 `d = ln 15`） ⟺ （`s = e⁻¹` 且 `d = ln 15`）

⇒ 左⇒右：把 `d` 代入 `ln 15`，Moran 方程即 `15 · s^ln15 = 1`，用 `moran_pins_rate` 得 `s = e⁻¹`。
右⇒左：`s = e⁻¹` 时 `15 · (e⁻¹)^ln15 = 1`（同一引理的逆方向）。

⇒ 这条是本批对「推出 3」主线的净贡献：注入点表里原本并列的
「`d_H = ln 15`」与「`r = e⁻¹`」两项，实为**一项**。 -/
theorem silence_rate_is_not_independent (s d : ℝ) (hs : 0 < s) (hs1 : s < 1) :
    ((15 : ℝ) * s ^ d = 1 ∧ d = Real.log 15) ↔
      (s = Real.exp (-1 : ℝ) ∧ d = Real.log 15) := by
  constructor
  · rintro ⟨hm, hd⟩
    subst hd
    exact ⟨(moran_pins_rate s hs hs1).mp hm, rfl⟩
  · rintro ⟨hse, hd⟩
    subst hse
    subst hd
    refine ⟨?_, rfl⟩
    exact (moran_pins_rate (Real.exp (-1)) (Real.exp_pos _) exp_neg_one_lt_one).mpr rfl

/-- ★★★ **本批总述**：R1 只锁形式；`r = e⁻¹` 与 `d_H = ln 15` 等价。

⇒ 于是「`r = e⁻¹` 的来由」这一问题被**精确化**为两条互斥的候选：
   (a) 独立动机（「信息论最优静默因子」）——库内零机检，本批未补；
   (b) 拟合反推（由 `d_H` 的唯象值反解 `s`）——数值上给出 `s = 0.368076`，
       与 `e⁻¹` 相差 `5.35 × 10⁻⁴`，即它并不精确。
⇒ 二者都不是机检结论，故 `r = e⁻¹` 的**值**仍敞开，但其**地位**已从「定理推论」
降为「自由参数的一次选取」。 -/
theorem silence_rate_audit :
    (∀ s : ℝ, ∀ k l : ℕ, s ^ (k + l) = s ^ k * s ^ l) ∧
    (∀ s : ℝ, 0 < s → s < 1 → ((15 : ℝ) * s ^ (Real.log 15) = 1 ↔ s = Real.exp (-1))) ∧
    (∀ s d : ℝ, 0 < s → s < 1 →
      (((15 : ℝ) * s ^ d = 1 ∧ d = Real.log 15) ↔ (s = Real.exp (-1 : ℝ) ∧ d = Real.log 15))) := by
  refine ⟨cauchy_family_free, ?_, ?_⟩
  · intro s hs hs1
    exact moran_pins_rate s hs hs1
  · intro s d hs hs1
    exact silence_rate_is_not_independent s d hs hs1

end MUFPF.SilenceRate
