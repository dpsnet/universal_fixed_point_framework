/-
# 框架常数的「平方表示 / 指数表示」统一于一

## 本批要回答的问题

第 53 批证明：`σ⁻¹ = 15` 的两条生成路线（`f²−1` 与 `2^f−1`）只在 `f = 4` 重合，
故「数值 15 不决定函数形式」，并把开口登记为「为什么因子必须关于不动点对称」。

本批把这个「两条路线竞争」的读法**推翻**，给出结构性重述：

> 框架的三个核心常数——全态 `16`、谱宽 `k_max = 8`、`σ⁻¹ = 15`——
> 各自都有一对「平方表示」与「指数表示」。这三对表示的同值条件
> **全部归约到同一条自指方程** `f² = 2^f`，而不是三个独立的巧合。

因此 `f² − 1` 与 `2^f − 1` 在 `f = 4` 处**不是两条竞争路线撞车**，
而是**同一条方程的两个等价写法**。第 53 批的负面结论由此被收窄：
不再是「数值 15 无法挑出形式」，而是「在 `f = 4` 处根本不需要挑」。

## 三对表示

| 常数 | 平方表示 | 指数表示 | 归约到 |
|---|---|---|---|
| 全态 `16` | `f²` | `2^f` | `f² = 2^f` |
| 谱宽 `k_max = 8` | `f² / 2`（双倍形式 `2 · f²`） | `2^(f−1)`（双倍形式 `2 · 2^(f−1) = 2^f`） | `f² = 2^f` |
| `σ⁻¹ = 15` | `f² − 1` | `2^f − 1` | `f² = 2^f` |

⇒ 三条归约（`sub_one_reduces`、`double_reduces`、`double_exp_identity`）都是纯算术恒等式，
不需要任何新假设；它们把「三对表示是否同值」这个表面上的三个问题压成同一个问题。

## 一个必须先说清的坑

`k_max` 的平方形式若按 `f² / 2` 写成 **Nat 除法**，会因截断而在 `f = 3` 处误判：
`9 / 2 = 4 = 2^(3−1)`，于是 `f = 3` 也「成立」。数值先证伪脚本用 `Fraction` 复算，
`f = 3` 处 `9/2` 与 `4` 不等；本模块因此一律用**双倍形式** `2 · f²` 与 `2 · 2^(f−1)`
（后者恒等于 `2^f`），完全绕开除法截断。

## 与既有模块的关系

- `SigmaFormOrigin`：提供 `sigmaInvSq` / `sigmaInvMer` / `sub_one_injective`。
- `SelfRefUniqueness`：提供 `sq_eq_pow_iff`（全域 `f² = b^f` 解集）。
- 不 import 任何 `Rec` / `Sp` 结构：本批是常数层的算术统一，不涉及时间结构。
-/

import Mathlib.Tactic
import MUFPFormalization.SelfRefUniqueness
import MUFPFormalization.SigmaFormOrigin

namespace MUFPF.ConstantDualForms

open MUFPF.SelfRefUniqueness MUFPF.SigmaFormOrigin

/-! ## 一、三条归约：三个表面问题压成一条方程 -/

/-- ★★★ **`σ⁻¹` 的两条形式同值 ⟺ 自指方程成立**。

⇒ 这是第 53 批 `sq_mer_coincide_iff` 的「归约版」：把结论从 `f = 4` 改为
`f² = 2^f`，从而显露出**两条形式之间没有独立内容**——它们的差值恒等于
「自指方程的残差」。 -/
theorem sub_one_reduces (f : ℕ) (hf : 2 ≤ f) :
    (sigmaInvSq f = sigmaInvMer f) ↔ f ^ 2 = 2 ^ f := by
  change (f ^ 2 - 1 = 2 ^ f - 1) ↔ f ^ 2 = 2 ^ f
  have hle1 : 1 ≤ f ^ 2 := sq_pos_of_ne_zero (by omega)
  have hle2 : 1 ≤ 2 ^ f := by
    have hpos : 0 < 2 ^ f := pow_pos (by norm_num) f
    omega
  constructor
  · intro h
    exact sub_one_injective hle1 hle2 h
  · intro h
    rw [h]

/-- ★★ **谱宽的平方形式（双倍）⟺ 自指方程**。

`2 · f² = 2 · 2^f` 与 `f² = 2^f` 在 `Nat` 上等价（乘法左消去），
故「`k_max` 的平方表示与指数表示同值」也是一句只关于 `f² = 2^f` 的话。 -/
theorem double_reduces (f : ℕ) :
    (2 * f ^ 2 = 2 * 2 ^ f) ↔ f ^ 2 = 2 ^ f := by
  constructor
  · intro h
    exact Nat.mul_left_cancel (by norm_num) h
  · intro h
    rw [h]

/-- ★★ **指数侧的恒等式**：`2 · 2^(f−1) = 2^f`（`f ≥ 1`）。

⇒ 于是 `2 · 2^(f−1)` 就是 `2^f` 的另一种写法，`k_max` 的指数表示不含额外信息。 -/
theorem double_exp_identity (f : ℕ) (hf : 1 ≤ f) : 2 * 2 ^ (f - 1) = 2 ^ f := by
  obtain ⟨n, rfl⟩ : ∃ n, f = n + 1 := ⟨f - 1, by omega⟩
  rw [Nat.add_sub_cancel]
  rw [pow_succ]
  ring

/-! ## 二、自指方程在框架域内唯一指向 `f = 4` -/

/-- ★★★ **`f ≥ 3 ⇒ f² = 2^f ⟺ f = 4`**（第 51 批全域解集在框架域内的收紧）。 -/
theorem sq_selfref_iff_four (f : ℕ) (hf : 3 ≤ f) : f ^ 2 = 2 ^ f ↔ f = 4 := by
  constructor
  · intro h
    have hres := (sq_eq_pow_iff 2 f (by norm_num) (by omega)).mp h
    rcases hres with ⟨_, hf2 | hf4⟩
    · omega
    · exact hf4
  · intro h
    subst h
    norm_num

/-! ## 三、主定理：三条表示统一于一条方程，该方程唯一指向 `f = 4` -/

/-- ★★★ **两条形式不是竞争路线，而是同一条方程的两个写法**。

两段合成：
1. `σ⁻¹` 的两条形式同值 ⟺ `f² = 2^f`（`sub_one_reduces`）；
2. `f² = 2^f`（在 `f ≥ 3` 上）⟺ `f = 4`（`sq_selfref_iff_four`）。

⇒ 若两条形式在 `f = 4` 同值，那不是「巧合撞车」，而是**它们表达的是同一件事**：
`f` 同时满足「平方」与「指数」两种刻画。第 53 批的「数值 15 不决定形式」
由此被收窄为：**在 `f = 4` 处不需要决定**，因为两者等价。 -/
theorem dual_forms_same_equation (f : ℕ) (hf : 3 ≤ f) :
    (sigmaInvSq f = sigmaInvMer f) ↔ f = 4 := by
  have hred := sub_one_reduces f (by omega)
  have hself := sq_selfref_iff_four f hf
  exact hred.trans hself

/-- ★★★ **三个常数的双表示在 `f = 4` 处全部对齐**。

| 常数 | 平方侧 | 指数侧 |
|---|---|---|
| 全态 `16` | `4² = 16` | `2⁴ = 16` |
| 谱宽 `k_max = 8` | `4²/2 = 8` | `2⁴/2 = 2³ = 8` |
| `σ⁻¹ = 15` | `4² − 1 = 15` | `2⁴ − 1 = 15` |

⇒ 后两条与前一条的关系：`k_max` 的表示对就是全态表示对**除以 2**（同一对，
不是独立的一对）；`σ⁻¹` 的表示对是全态表示对**各减 1**（同样不是独立的一对）。
⇒ 故「三对表示」实为**一对表示加两次平移**，统一性比表面看更强。 -/
theorem three_constants_dual_at_four :
    (4 : ℕ) ^ 2 = 16 ∧ (4 : ℕ) ^ 2 / 2 = 8 ∧ (4 : ℕ) ^ 2 - 1 = 15 ∧
    2 ^ 4 = 16 ∧ 2 ^ (4 - 1) = 8 ∧ 2 ^ 4 - 1 = 15 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩ <;> norm_num

/-- ★★★ **三条表示的同值点完全重合于 `f = 4`（`f ≥ 3`）**。

⇒ 这是「三对表示统一于一」的定量版：不是三条曲线各自碰巧在 `f = 4` 相交，
而是它们的**交点集合恒等**（都是单点集 `{4}`）。 -/
theorem all_three_pin_four (f : ℕ) (hf : 3 ≤ f) :
    ((sigmaInvSq f = sigmaInvMer f) ↔ f = 4) ∧
    ((2 * f ^ 2 = 2 * 2 ^ f) ↔ f = 4) ∧
    (f ^ 2 = 2 ^ f ↔ f = 4) := by
  refine ⟨?_, ?_, ?_⟩
  · exact dual_forms_same_equation f hf
  · have h := double_reduces f
    exact h.trans (sq_selfref_iff_four f hf)
  · exact sq_selfref_iff_four f hf

/-! ## 四、裁决：注入点上移 -/

/-- ★★★ **本批的正式裁决**（负面转正面后的净结果）：

1. `σ⁻¹` 的两条形式同值 ⟺ `f² = 2^f`（无独立内容）；
2. `k_max` 的双表示同值 ⟺ `f² = 2^f`（同样无独立内容）；
3. 全态的两种写法同值 ⟺ `f² = 2^f`（这是方程本身）。

⇒ **三条表示不构成三个需分别回答的问题**。第 53 批登记的
`sigma_form_symmetry_requirement_open`（「因子须关于不动点对称」）由此**作废**：
不需要这条额外要求，因为平方形式与指数形式在 `f = 4` 处等价。

⇒ 真正的注入点因此上移一级：不再是「为什么选 `f² − 1` 而不是 `2^f − 1`」，
而是「**为什么框架取 `f² = 2^f` 这条自指方程**」。这条与第 45/51 批登记的
建模层缺口（`modeling_choice_still_open`）合流，同一处缺口。 -/
theorem dual_form_verdict :
    (∀ f : ℕ, 2 ≤ f → ((sigmaInvSq f = sigmaInvMer f) ↔ f ^ 2 = 2 ^ f)) ∧
    (∀ f : ℕ, (2 * f ^ 2 = 2 * 2 ^ f) ↔ f ^ 2 = 2 ^ f) ∧
    (∀ f : ℕ, 1 ≤ f → 2 * 2 ^ (f - 1) = 2 ^ f) ∧
    (∀ f : ℕ, 3 ≤ f → (f ^ 2 = 2 ^ f ↔ f = 4)) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro f hf
    exact sub_one_reduces f hf
  · intro f
    exact double_reduces f
  · intro f hf
    exact double_exp_identity f hf
  · intro f hf
    exact sq_selfref_iff_four f hf

end MUFPF.ConstantDualForms
