/-
# σ⁻¹ 的「函数形式」来由：两条生成路线在 `f = 4` 处不可区分

## 本批要回答的问题

第 51 批把 `f = 4` 钉成 `f² = b^f` 的唯一非平凡解（`selfref_unique`），于是注入点下移到：

> **`σ⁻¹ = 15` 为什么写成 `f² − 1` 这个函数形式？**

本批检查这条开口是否可闭合。库内 `σ⁻¹ = 15` 实际有**两条互不相干**的生成记录：

| 路线 | 形式 | 出处 |
|---|---|---|
| A | `f² − 1`（完美平方差 `(f−1)(f+1)`） | `SpectralGap.sigma_inv_square_minus_one`（L352） |
| B | `2^f − 1`（Mersenne `M_f`） | 第 40 批「两个 15 = 一个 `M_4` 的三条 Mersenne 表示」 |

两条在 `f = 4` 处都给出 15。本批证明的结论是**负面的**：

1. 两形式**在且仅在** `f = 4`（以及 `f = 2` 这个退化点）重合（`sq_mer_coincide_iff`）；
2. 在 `f = 3`（8 vs 7）与 `f = 5`（24 vs 31）处分道（`divergence_table`）；
3. 数值 15 **不能**从两形式中挑出一条：`sigmaInvSq f = 15 ↔ f = 4`，`sigmaInvMer f = 15 ↔ f = 4`，
   两条反解都唯一指向 `f = 4`，故 15 对「形式」完全无信息量（`value_fifteen_does_not_determine_form`）；
4. 更强的干扰：第三条候选 `2^(f−1) − 1` 在 `f = 5` 也给 15（`pm_inv_eq_fifteen_at_five`）
   ⇒ 「数值 15」连 `f` 都不能唯一决定。

⇒ **裁决**：`σ⁻¹ = f² − 1` 的函数形式**不由数值 15 决定**；它要么由额外的结构要求
（「`σ⁻¹` 必须是 `不动点 ± 1` 之积」这条对称性）决定，要么仍是建模选择。
本批只把「数值可定形式」这条可能的闭合路径**证伪**，不声称已经给出正面的形式来由。

## 与既有模块的关系

- 复用 `SelfRefUniqueness.sq_eq_pow_iff`（全域 `f² = b^f` 解集）与 `two_pow_gt_sq`（`f ≥ 5 ⇒ f² < 2^f`）。
- 不 import `RecCategory` / `DepthExistence` 一侧：本批与时间结构无关，纯算术 + 一条不等式。
-/

import Mathlib.Tactic
import MUFPFormalization.SelfRefUniqueness

namespace MUFPF.SigmaFormOrigin

open MUFPF.SelfRefUniqueness

/-! ## 一、纯算术引理 -/

/-- `a − 1 = b − 1` 在两端都 `≥ 1` 时反推 `a = b`（避免 `Nat` 减法截断，坑 162）。 -/
theorem sub_one_injective {a b : ℕ} (ha : 1 ≤ a) (hb : 1 ≤ b)
    (h : a - 1 = b - 1) : a = b := by
  omega

/-- 非零数的平方 `≥ 1`。 -/
theorem sq_pos_of_ne_zero {f : ℕ} (hf : f ≠ 0) : 1 ≤ f ^ 2 := by
  have hpos : 0 < f ^ 2 := pow_pos (Nat.pos_of_ne_zero hf) 2
  omega

/-! ## 二、三条候选形式 -/

/-- **路线 A**：`σ⁻¹ = f² − 1`（完美平方差 `(f−1)(f+1)`）。库内出处 `SpectralGap` L352。 -/
def sigmaInvSq (f : ℕ) : ℕ := f ^ 2 - 1

/-- **路线 B**：`σ⁻¹ = 2^f − 1`（Mersenne `M_f`）。第 40 批 `M_4 = 15` 的表示。 -/
def sigmaInvMer (f : ℕ) : ℕ := 2 ^ f - 1

/-- **路线 C**（干扰项）：`σ⁻¹ = 2^(f−1) − 1`。这是 `k_max = 2^(f−1)` 的邻接形式。 -/
def sigmaInvPow (f : ℕ) : ℕ := 2 ^ (f - 1) - 1

/-! ## 三、主定理：两形式只在 `f = 4` 重合（`f ≥ 3`） -/

/-- ★★★ **`f² − 1 = 2^f − 1 ⟺ f = 4`（对 `f ≥ 3`）**。

证明走第 51 批的全域解集：由 `sub_one_injective` 脱掉两侧 `−1` 得 `f² = 2^f`，
再用 `sq_eq_pow_iff 2 f` 得 `f = 2 ∨ f = 4`，最后 `3 ≤ f` 排除 `f = 2`。

⇒ **这不是「两条路线互相印证」，而是「两条路线在一个点上碰巧同值」**：
离开 `f = 4`，它们立刻分道。 -/
theorem sq_mer_coincide_iff (f : ℕ) (hf : 3 ≤ f) :
    sigmaInvSq f = sigmaInvMer f ↔ f = 4 := by
  change (f ^ 2 - 1 = 2 ^ f - 1) ↔ f = 4
  have hle1 : 1 ≤ f ^ 2 := sq_pos_of_ne_zero (by omega)
  have hle2 : 1 ≤ 2 ^ f := by
    have hpos : 0 < 2 ^ f := pow_pos (by norm_num) f
    omega
  constructor
  · intro h
    have hsq : f ^ 2 = 2 ^ f := sub_one_injective hle1 hle2 h
    have hres := (sq_eq_pow_iff 2 f (by norm_num) (by omega)).mp hsq
    rcases hres with ⟨_, hf2 | hf4⟩
    · omega
    · exact hf4
  · intro h
    subst h
    norm_num [sigmaInvSq, sigmaInvMer]

/-- 退化重合点：`f = 2` 处两形式同值 3（`f² − 1 = 3`、`2² − 1 = 3`）。

⇒ 因此「两形式重合」的解集是 `{2, 4}`，`f = 2` 是平凡角点，`f = 4` 才是框架取值点。 -/
theorem sq_mer_coincide_at_two :
    sigmaInvSq 2 = 3 ∧ sigmaInvMer 2 = 3 := by
  constructor <;> norm_num [sigmaInvSq, sigmaInvMer]

/-! ## 四、分歧点的显式值（`f = 3` / `4` / `5`） -/

/-- ★★ **三形式在 `f = 3 / 4 / 5` 的取值表**（本批核心证据）：

| `f` | `f²−1` | `2^f−1` | `2^(f−1)−1` |
|---|---|---|---|
| 3 | 8 | 7 | 3 |
| 4 | **15** | **15** | 7 |
| 5 | 24 | 31 | **15** |

⇒ `f = 4` 是 A/B 唯一同值处；而 `f = 5` 处 C 也落到 15 ⇒ 「15」这个数值同时是
`f²−1`（在 f=4）、`2^f−1`（在 f=4）、`2^(f−1)−1`（在 f=5）三条曲线的交点值。 -/
theorem divergence_table :
    sigmaInvSq 3 = 8 ∧ sigmaInvMer 3 = 7 ∧ sigmaInvPow 3 = 3 ∧
    sigmaInvSq 4 = 15 ∧ sigmaInvMer 4 = 15 ∧ sigmaInvPow 4 = 7 ∧
    sigmaInvSq 5 = 24 ∧ sigmaInvMer 5 = 31 ∧ sigmaInvPow 5 = 15 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;>
    norm_num [sigmaInvSq, sigmaInvMer, sigmaInvPow]

/-! ## 五、数值 15 的反解：两条线 A/B 都唯一指向 `f = 4`，线 C 指向 `f = 5` -/

/-- ★★ **`f² − 1 = 15 ⟺ f = 4`**（路线 A 的数值反解唯一）。 -/
theorem sq_inv_eq_fifteen_iff (f : ℕ) : sigmaInvSq f = 15 ↔ f = 4 := by
  change (f ^ 2 - 1 = 15) ↔ f = 4
  constructor
  · intro h
    have hf : f ≠ 0 := by
      rintro rfl
      norm_num at h
    have h1 : 1 ≤ f ^ 2 := sq_pos_of_ne_zero hf
    have hsq : f ^ 2 = 16 := by omega
    have hle : f ≤ 4 := by
      by_contra hc
      push Not at hc
      have h5 : 5 ≤ f := by omega
      have hmul : 5 * f ≤ f ^ 2 := by
        calc 5 * f ≤ f * f := Nat.mul_le_mul_right f h5
          _ = f ^ 2 := by ring
      have h25 : 25 ≤ f ^ 2 := by
        calc 25 = 5 * 5 := by norm_num
          _ ≤ 5 * f := Nat.mul_le_mul_left 5 h5
          _ ≤ f ^ 2 := hmul
      omega
    interval_cases f
    · norm_num at hsq
    · norm_num at hsq
    · norm_num at hsq
    · norm_num at hsq
    · rfl
  · intro h
    subst h
    norm_num [sigmaInvSq]

/-- ★★ **`2^f − 1 = 15 ⟺ f = 4`**（路线 B 的数值反解唯一）。 -/
theorem mer_inv_eq_fifteen_iff (f : ℕ) : sigmaInvMer f = 15 ↔ f = 4 := by
  change (2 ^ f - 1 = 15) ↔ f = 4
  constructor
  · intro h
    have hle2 : 1 ≤ 2 ^ f := by
      have hpos : 0 < 2 ^ f := pow_pos (by norm_num) f
      omega
    have hsq : 2 ^ f = 16 := by omega
    have hle : f ≤ 4 := by
      by_contra hc
      push Not at hc
      have h5 : 5 ≤ f := by omega
      have hgt := two_pow_gt_sq f h5
      have hmul : 5 * f ≤ f ^ 2 := by
        calc 5 * f ≤ f * f := Nat.mul_le_mul_right f h5
          _ = f ^ 2 := by ring
      have h25 : 25 ≤ f ^ 2 := by
        calc 25 = 5 * 5 := by norm_num
          _ ≤ 5 * f := Nat.mul_le_mul_left 5 h5
          _ ≤ f ^ 2 := hmul
      omega
    interval_cases f
    · norm_num at hsq
    · norm_num at hsq
    · norm_num at hsq
    · norm_num at hsq
    · rfl
  · intro h
    subst h
    norm_num [sigmaInvMer]

/-- ★ **路线 C 在 `f = 5` 也给 15**（`2^(5−1) − 1 = 15`）。

⇒ 这一条是本批最不舒服的事实：「15」并不专属 `f = 4`——把指数换成 `f − 1`，
同一个 15 就搬到 `f = 5` 上。故「数值 15 ⇒ `f = 4` ⇒ `σ⁻¹ = f²−1`」这条推理链
**不能**闭合形式来由。 -/
theorem pm_inv_eq_fifteen_at_five : sigmaInvPow 5 = 15 := by
  norm_num [sigmaInvPow]

/-! ## 六、负面主结论 -/

/-- ★★★ **数值 15 不决定函数形式**（本批的正式裁决）。

三层证据合成：
1. A 与 B 在 `f = 4` 同值 15，却在 `f = 3`、`f = 5` 分道 ⇒ 15 无法在 A/B 之间取舍；
2. A、B 在 15 处的反解都唯一指向 `f = 4` ⇒ 15 对 A/B 的「形式」零信息量；
3. C 在 `f = 5` 也给 15 ⇒ 15 甚至不能唯一钉住 `f`。

⇒ 因此 `σ⁻¹ = f² − 1` **不能**由「它必须等于 15」推出。要闭合这条开口，
必须引入数值之外的额外结构（候选：`σ⁻¹` 的因子必须是 `不动点 ± 1`，即 `3 = 4−1`、`5 = 4+1`，
这是一条**对称性**要求，Mersenne 形式不具备）。本批只证伪「数值定形式」，不给正面来由。 -/
theorem value_fifteen_does_not_determine_form :
    sigmaInvSq 4 = sigmaInvMer 4 ∧
    sigmaInvSq 3 ≠ sigmaInvMer 3 ∧
    sigmaInvSq 5 ≠ sigmaInvMer 5 ∧
    sigmaInvPow 5 = 15 ∧
    sigmaInvSq 5 ≠ 15 ∧
    sigmaInvMer 5 ≠ 15 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩ <;>
    norm_num [sigmaInvSq, sigmaInvMer, sigmaInvPow]

/-- ★ **`f ≥ 5` 时 A 严格小于 B**（`f² − 1 < 2^f − 1`）。

⇒ 这是 `two_pow_gt_sq` 的「减一版」：离开 `f = 4` 后 Mersenne 曲线永久压过平方曲线，
故两者不可能在别处再碰头。 -/
theorem sq_mer_gap_positive (f : ℕ) (hf : 5 ≤ f) :
    sigmaInvSq f < sigmaInvMer f := by
  change f ^ 2 - 1 < 2 ^ f - 1
  have hgt := two_pow_gt_sq f hf
  have hle1 : 1 ≤ f ^ 2 := sq_pos_of_ne_zero (by omega)
  have hle2 : 1 ≤ 2 ^ f := by
    have hpos : 0 < 2 ^ f := pow_pos (by norm_num) f
    omega
  omega

/-- **全域闭合**：把重合、分歧、反解三件事合成一条总述。 -/
theorem sigma_form_summary :
    (∀ f : ℕ, 3 ≤ f → (sigmaInvSq f = sigmaInvMer f ↔ f = 4)) ∧
    sigmaInvSq 4 = 15 ∧ sigmaInvMer 4 = 15 ∧ sigmaInvPow 5 = 15 ∧
    (∀ f : ℕ, sigmaInvSq f = 15 ↔ f = 4) ∧
    (∀ f : ℕ, sigmaInvMer f = 15 ↔ f = 4) := by
  refine ⟨?_, by norm_num [sigmaInvSq], by norm_num [sigmaInvMer],
    by norm_num [sigmaInvPow], sq_inv_eq_fifteen_iff, mer_inv_eq_fifteen_iff⟩
  intro f hf
  exact sq_mer_coincide_iff f hf

end MUFPF.SigmaFormOrigin
