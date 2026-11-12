/-
  SelfRefUniqueness.lean — 第 51 批：两条自指方程的全域解集

  ## 本批要解决什么

第 45/49/50 批把 PR-634 主线的上游注入点一路收窄，最后只剩一条：

> `f = b²` 与 `f² = b^f` 这两条自指方程**自身为什么取这两个**。

「为什么取这两个」是建模选择，Lean 里无法证。但这句话可以拆成两半：

1. **数值层**：这两条方程在 `b ≥ 2`、`f ≥ 2` 下有多少组解？若只有一组，则「取这两条」
   就唯一决定了 `(b, f) = (2, 4)`，不存在第二组候选。
2. **建模层**：为什么理论要从自指方程出发（而不是从别的东西出发）。

第 (1) 半是可证的，本批就做这一半；第 (2) 半登记为建模选择。

## 为什么这条以前没闭合

第 31 批 `FixedPointFactorOrigin.sq_eq_pow_solutions_small` 只对 `f : Fin 9` 机检
（`decide`），陈述里明写「**不作全域断言**」。⇒ OPEN_ITEMS 第 26 条：

> `f² = 2^f` 全域解集未证（只机检 `f < 9`，解集 `{2,4}`）。

本批给它全域证明：`2 ≤ f ⇒ f² = 2^f ⇒ f ∈ {2, 4}`，并推广到一般基底 `b`：
`f² = b^f ∧ 2 ≤ b ∧ 2 ≤ f ⟺ (b, f) ∈ {(2,2), (2,4)}`，
再叠加 `f = b²` 后唯一化到 `(2, 4)`。

## 证明骨架

全域闭合的关键是一条纯初等不等式：

* `f ≥ 5 ⇒ f² < 2^f`（`two_pow_gt_sq`，对 `f` 从 5 起归纳：`f² ≥ 5f ≥ 2f+1` 给出 `2f² ≥ (f+1)²`）
* `3 ≤ b ⇒ 2 ≤ f ⇒ f² < b^f`（`pow_gt_sq_of_three_le`，把上一条经 `2^f ≤ b^f` 抬高到任意 `b`）

⇒ 于是 `b ≥ 3` 一律无解，`b = 2` 且 `f ≥ 5` 一律无解；只剩 `b = 2`、`f ∈ {2,3,4}`
三格，逐格判定：`f=2` ✓、`f=3` ✗（`8 ≠ 9`）、`f=4` ✓。
-/

import Mathlib.Tactic
import MUFPFormalization.LayersNotRecursive

namespace MUFPF.SelfRefUniqueness

/-! ## 一、全域不等式：`f ≥ 5` 时 `2^f` 严格压过 `f²` -/

/-- **`f ≥ 5 ⇒ f² < 2^f`**（全域，不再限于 `f < 9`）。

归纳步用两个事实：`2 · 2^f > 2 · f²`（由归纳假设）与 `2 · f² ≥ (f+1)²`
（即 `f² ≥ 2f + 1`，由 `5 ≤ f` 保证）。 -/
theorem two_pow_gt_sq (f : ℕ) (hf : 5 ≤ f) : f ^ 2 < 2 ^ f := by
  induction f, hf using Nat.le_induction with
  | base => norm_num
  | succ n hn ih =>
      have hn5 : 5 ≤ n := hn
      have ih' : n ^ 2 < 2 ^ n := ih
      have h5 : 5 * n ≤ n * n := by nlinarith
      have hsq : (n + 1) ^ 2 ≤ 2 * n ^ 2 := by nlinarith
      have hmul : 2 * n ^ 2 < 2 * 2 ^ n :=
        Nat.mul_lt_mul_of_pos_left ih' (by norm_num)
      calc (n + 1) ^ 2 ≤ 2 * n ^ 2 := hsq
        _ < 2 * 2 ^ n := hmul
        _ = 2 ^ (n + 1) := by rw [pow_succ]; ring

/-- **`b ≥ 3 ⇒ f ≥ 2 ⇒ f² < b^f`**：把 `2^f` 的上界抬到任意基底。

于是「`b ≥ 3` 时 `f² = b^f` 无解」是直接的。 -/
theorem pow_gt_sq_of_three_le (b f : ℕ) (hb : 3 ≤ b) (hf : 2 ≤ f) : f ^ 2 < b ^ f := by
  have hb2 : 2 ≤ b := by omega
  rcases Nat.lt_or_ge f 5 with hlt | hge
  · have hpow : 3 ^ f ≤ b ^ f := Nat.pow_le_pow_left hb f
    interval_cases f
    · calc 2 ^ 2 = 4 := by norm_num
        _ < 3 ^ 2 := by norm_num
        _ ≤ b ^ 2 := hpow
    · calc 3 ^ 2 = 9 := by norm_num
        _ < 3 ^ 3 := by norm_num
        _ ≤ b ^ 3 := hpow
    · calc 4 ^ 2 = 16 := by norm_num
        _ < 3 ^ 4 := by norm_num
        _ ≤ b ^ 4 := hpow
  · have h2 : 2 ^ f ≤ b ^ f := Nat.pow_le_pow_left hb2 f
    exact lt_of_lt_of_le (two_pow_gt_sq f hge) h2

/-! ## 二、全域解集：`f² = b^f` 只有 `(2,2)` 与 `(2,4)` -/

/-- ★★★ **`f² = b^f` 的全域解集**（`b ≥ 2`、`f ≥ 2`）：

`f² = b^f  ⟺  b = 2 ∧ (f = 2 ∨ f = 4)`。

这条把 OPEN_ITEMS 第 26 条（「只机检 `f < 9`」）升级为全域双向结论，
并第一次给出「基底不是 2 就无解」的显式证明（不再是数值枚举）。 -/
theorem sq_eq_pow_iff (b f : ℕ) (hb : 2 ≤ b) (hf : 2 ≤ f) :
    (f ^ 2 = b ^ f) ↔ (b = 2 ∧ (f = 2 ∨ f = 4)) := by
  constructor
  · intro h
    rcases Nat.lt_or_ge b 3 with hblt | hbge
    · -- b = 2
      have hb2 : b = 2 := by omega
      subst hb2
      rcases Nat.lt_or_ge f 5 with hflt | hfge
      · interval_cases f
        · -- f = 2：4 = 4，成立
          exact ⟨rfl, Or.inl rfl⟩
        · -- f = 3：9 = 8，矛盾
          norm_num at h
        · -- f = 4：16 = 16，成立
          exact ⟨rfl, Or.inr rfl⟩
      · -- f ≥ 5：f² < 2^f，矛盾
        have := two_pow_gt_sq f hfge
        omega
    · -- b ≥ 3：f² < b^f，矛盾
      have := pow_gt_sq_of_three_le b f hbge hf
      omega
  · rintro ⟨rfl, hf' | hf'⟩
    · subst hf'
      norm_num
    · subst hf'
      norm_num

/-! ## 三、加 `f = b²` 后唯一化到 `(2, 4)` -/

/-- ★★★ **两条自指方程的唯一解**：`f = b² ∧ f² = b^f ∧ 2 ≤ b ∧ 2 ≤ f ⟺ b = 2 ∧ f = 4`。

⇒ 第 45/49/50 批遗留的「唯一原始注入点」，其**数值层**在此闭合：
只要理论取这两条自指方程，`(b, f)` 就被唯一钉死为 `(2, 4)`，
不存在「换个 `b` 也行」的第二条候选路径。 -/
theorem selfref_unique (b f : ℕ) (hb : 2 ≤ b) (hf : 2 ≤ f) :
    (f = b ^ 2 ∧ f ^ 2 = b ^ f) ↔ (b = 2 ∧ f = 4) := by
  constructor
  · rintro ⟨hfb, hsq⟩
    have h1 := (sq_eq_pow_iff b f hb hf).mp hsq
    rcases h1 with ⟨hb2, hf2 | hf4⟩
    · -- f = 2 与 f = b² = 4 矛盾
      subst hb2
      subst hf2
      omega
    · exact ⟨hb2, hf4⟩
  · rintro ⟨rfl, rfl⟩
    norm_num

/-- ★★★ **自指方程 ⇒ 指数 `d = 3`**（与本批唯一性焊接第 45 批的定义链）。

给定 `b`、`f`、`d`，若 `2 ≤ b`、`f = b²`、`f² = b^f`、`2^d = b^3`，
则 `b = 2 ∧ f = 4 ∧ d = 3`。

这条把三件事接成一条链：**两条自指方程有解 ⟹ 解唯一 ⟹ 唯一的解给出 `d = 3`**。
⇒ `N_active = spaceLayerDim = 3` 的算术来源不再是「取 3」，而是「两条自指方程的解
代入 `2^d = b^3` 后只能是 3」。 -/
theorem d_is_three_from_selfref (b f d : ℕ) (hb : 2 ≤ b) (hf : 2 ≤ f)
    (hfb : f = b ^ 2) (hsq : f ^ 2 = b ^ f) (hK : 2 ^ d = b ^ 3) :
    b = 2 ∧ f = 4 ∧ d = 3 := by
  have h1 := (selfref_unique b f hb hf).mp ⟨hfb, hsq⟩
  rcases h1 with ⟨hb2, hf4⟩
  subst hb2
  subst hf4
  refine ⟨rfl, rfl, ?_⟩
  have hd : d = 3 := Nat.pow_right_injective (by norm_num) hK
  exact hd

/-! ## 四、与第 45 批的接口：前提可满足性

第 45 批 `LayersNotRecursive.layer_from_selfref_equation` 的形态是

```
(b f d : ℕ) (hb : 2 ≤ b) (hf : f = b ^ 2) (hSq : f ^ 2 = b ^ f) (hK : 2 ^ d = b ^ 3) → d = 3
```

它证的是「**若**前提成立**则** `d = 3`」，但从未回答「前提成立吗」——
若前提不可满足，那条定理就是空谈（与第 50 批 `NoNontrivialCycle` 第一版的陷阱同型）。
本批的 `selfref_unique` 正好补上这一环：前提**可满足**，且**只有一组**赋值。
-/

/-- 第 45 批定理的前提可满足（给出显式见证 `b = 2, f = 4, d = 3`）。 -/
theorem layer_premises_satisfiable :
    ∃ b f d : ℕ, 2 ≤ b ∧ f = b ^ 2 ∧ f ^ 2 = b ^ f ∧ 2 ^ d = b ^ 3 ∧ d = 3 :=
  ⟨2, 4, 3, by norm_num, by norm_num, by norm_num, by norm_num, by norm_num⟩

/-- 前提的赋值**唯一**：任何满足前提的 `b f d` 都等于 `(2, 4, 3)`。 -/
theorem layer_premises_unique (b f d : ℕ) (hb : 2 ≤ b) (hf : f = b ^ 2)
    (hsq : f ^ 2 = b ^ f) (hK : 2 ^ d = b ^ 3) : b = 2 ∧ f = 4 ∧ d = 3 := by
  have hf2 : 2 ≤ f := by rw [hf]; nlinarith
  exact d_is_three_from_selfref b f d hb hf2 hf hsq hK

/-- 与第 45 批主定理对接：唯一赋值代入后 `d = 3`（复用 `layer_from_selfref_equation`）。 -/
theorem layer_from_selfref_equation_direct (b f d : ℕ) (hb : 2 ≤ b) (hf : f = b ^ 2)
    (hsq : f ^ 2 = b ^ f) (hK : 2 ^ d = b ^ 3) : d = 3 :=
  MUFPF.LayersNotRecursive.layer_from_selfref_equation b f d hb hf hsq hK

/-! ## 五、登记：本批的边界 -/

/-- 登记位：本批闭合的是两条自指方程的**数值层**（解集唯一）。

未闭合的是**建模层**：为什么理论要从「`f = b²` 与 `f² = b^f`」这两个方程出发，
而不是从别的自指关系出发。这一层不是数学命题，无法机检；
它属于「框架的出发点选择」，与第 42 批「抽象丢失在数学→Lean 结构」同一层级，
但更难——因为它连「丢失」的容器都还没有。 -/
theorem modeling_choice_still_open : True := trivial

/-- 登记位：`f² = b^f` 在 `b = 1` 与 `f = 0/1` 的退化格上另有解，
本批的陈述统一带 `2 ≤ b`、`2 ≤ f` 两个非退化前提，未覆盖退化格。

退化格不影响主线（`b ≥ 2` 是第 45 批 `hb` 的既定前提），但如需全域无条件的解集刻画，
需另做一条不带前提的版本，那里会出现 `(1,0)`、`(1,1)` 一类平凡解。 -/
theorem degenerate_cells_not_covered : True := trivial

end MUFPF.SelfRefUniqueness
