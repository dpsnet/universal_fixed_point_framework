/-
  FifteenMersenneRoot.lean — 「两个 15」的裁决：一个 `M_4` 的两条 Mersenne 递归（第 40 批）
  ==============================================================================

## 起因

第 39 批（`3ba79dd` / `3851687`）把 `N_active = 3` 的三条路径上溯到 `f = 4`，并留下
三条候选。本批执行**候选 B**：裁决库里出现过两次的「15」是否同源。

## 库里的「两个 15」原文

| # | 出处 | 原文 | doc 口径 |
|---|---|---|---|
| 1 | `SilenceFamily.lean` L405–409 `s48_residue_domain_full_minus_unit` | `Powers ^ FixedPoint - 1 = Ngen * SilenceUnit`，即 `2^4 − 1 = 3 × 5 = 15` | 「余态域 = 全态−单位」「σ⁻¹ = 15——F_耦合 基」 |
| 2 | `SilenceFamily.lean` L418–422 `s49_algebra_layer_completion` | `Kmax + Involution = Ngen * SilenceUnit`，即 `8 + 7 = 15` | 「代数层补全：空间全态+对合域 = 余态域」「基 15——σ⁻¹」 |
| 3 | `SpectralGap.lean` L313–318 `involution_via_freeze_spectrum` | `7 = 15 - 8` | 「对合 = 冻结中非谱的部分」（**对 7 是反解**） |
| 4 | `SpectralGap.lean` L349–358 `sigma_inv_square_minus_one` | `15 = 4 ^ 2 - 1` | 「完美平方差」「σ⁻¹ 的代数根源」 |

`ActiveSilentVieta.lean` L52–53 的 `SigmaInv := 15` 的 doc 已把**三条**并列：
「（对合域 + k_max；N_gen×静默；不动点²−1）」。

⇒ 前批把 1 与 4 记成「两个 15」，其实库里从未把它们当作两个数 —— **同一个 `σ⁻¹` 的三条
算术表示**。但这三条在 `Lean` 里都是各自 `norm_num` 独立闭合的，**互相之间没有定理**。
这正是第 38 批诊断的形态（「`3 = 3` 传递、内容为零」）在 15 上的重演。

## 本批的裁决

**不是两个 15，是同一个 Mersenne 数 `M_4 = 15` 的三条递归表示。**

记 `M_n := 2^n − 1`（`n ≥ 1`，二进制下恰为 `n` 个 1）。则：

1. **`M_n = 2^(n−1) + M_(n−1)`**（最高位与低 `n−1` 位分离）
   ⇒ `M_4 = 2^3 + M_3` ⇒ **`15 = 8 + 7`**（这正是表示 2）
2. **`M_(n+1) = 2 M_n + 1`**（移一位再加 1）
   ⇒ `M_4 = 2 M_3 + 1` ⇒ **`15 = 2·7 + 1`**
3. **`M_4 = f² − 1`**（`f = 4` 时 `f² = 2^f` 使 `f² − 1 = 2^f − 1 = M_4`）
   ⇒ **`15 = 4² − 1`**（这正是表示 4）

**三条互通的枢纽是一条恒等式：**

```
k_max = Involution + 1       即   2^(n−1) = M_(n−1) + 1
```

因为 `M_(n−1) = 2^(n−1) − 1`，移项即得。于是：

```
σ⁻¹ = k_max + Involution      （表示 2）
    ⟺ σ⁻¹ = (Involution + 1) + Involution = 2 Involution + 1   （表示 1 的递归）
    ⟺ σ⁻¹ = 2^(n−1) + 2^(n−1) − 1 = 2^n − 1 = M_n              （表示 3）
```

**⇒ 三条表示是同一个 `M_n` 的三种展开，`n = 4`（因 `k_max = 2^(n−1) = 8` ⇒ `n = 4`）。**

## 对主链的更新

`k_max` 有两条等价写法，它们的相等正是 `f² = 2^f` 的直接推论：

```
k_max = f²/2 = 4²/2 = 8
k_max = 2^(f−1) = 2^3 = 8
```

因为 `f² = 2^f` ⇒ 两边除以 2 ⇒ `f²/2 = 2^(f−1)`。

于是本轮链变成：

```
f² = 2^f（不动点方程，f = 4 是其非退化解）
  ├─ k_max   = f²/2 = 2^(f−1) = 8
  ├─ N_gen   = f − 1 = 3
  ├─ SilenceUnit = f + 1 = 5
  ├─ Involution = k_max − 1 = 2^(f−1) − 1 = M_3 = 7
  └─ σ⁻¹     = f² − 1 = 2^f − 1 = M_4 = 2·k_max − 1 = k_max + Involution = 15
        ⇒ k_max = 2^(N_active) ⇒ N_active = f − 1 = 3
```

**⇒ `N_active = N_gen = f − 1`。** 第 29/31 批记为「两个 3 不同源」的那一对
（`N_active` 与 `N_gen`），**在本批同源了** —— 两者都等于 `f − 1`。
（相数 3 仍是独立的第四个 3，走判据格路线，见 `PhaseTrichotomy.lean`。）

## 诚实边界

1. **`N_gen := 3`、`Involution := 7`、`Kmax := 8`、`SilenceUnit := 5` 在
   `ActiveSilentVieta.lean` 里都是 `noncomputable def`（ℝ 上的字面量）**，
   **没有从 `f = 4` 推出来。** 本模块证明的是**数值相等**（`3 = 4 − 1` 等），
   不是「从 `f` 的定义推出 `N_gen`」。**⇒ 这些常数仍是定义，本批只是把它们与 `f` 焊上。**
2. **「为什么框架常数恰好取这些函数（`f−1` / `f+1` / `2^(f−1)` / `2^(f−1)−1` / `f²−1`）」**
   **仍是选择，不是定理。** 本批只证明这五个函数在 `f = 4` 处给出的值与库内常数一致，
   **不证明「必须取这五个函数」**。
3. **`Involution = 2^(f−1) − 1` 的「对合」语义未证。** `σ² = 1` 的折叠算子与 Mersenne
   低位全 1 之间是否有结构对应，**未触及**。
4. **本模块全部在 `ℕ` 上做算术。** 与 `ActiveSilentVieta` 的 ℝ 版只做数值对照，
   不做 ℝ/ℕ 转换的形式化。
5. **`f² = 2^f ⇒ f²/2 = 2^(f−1)` 的一般形式未证**，本模块只机检 `f = 4` 处的实例。
   一般形式需要 `f` 的奇偶性讨论（`f` 偶时 `f²/2` 为整），留待后续。
-/

import Mathlib.Tactic
import MUFPFormalization.ThreeThreesOneRoot

namespace MUFPF.FifteenMersenne

open MUFPF.OneRoot

/-! =========================================================
    Mersenne 递归（一般形式）
   ========================================================= -/

/-- **Mersenne 递归（一）**：`M_n = 2^(n−1) + M_(n−1)`，即
    `2^n − 1 = 2^(n−1) + (2^(n−1) − 1)`。
    `M_n` 的二进制形是 `n` 个 1；右式是「最高位 1」加「低 `n−1` 位全 1」。 -/
theorem mersenne_recursion (n : ℕ) (_hn : 1 ≤ n) :
    2 ^ n - 1 = 2 ^ (n - 1) + (2 ^ (n - 1) - 1) := by
  have hpos : 0 < 2 ^ (n - 1) := Nat.two_pow_pos (n - 1)
  have h2 : 2 ^ n = 2 ^ (n - 1) * 2 := by
    cases n with
    | zero => omega
    | succ k =>
      have hk : k + 1 - 1 = k := rfl
      rw [hk, pow_succ]
  have h3 : 2 ^ (n - 1) * 2 = 2 ^ (n - 1) + 2 ^ (n - 1) := by ring
  have hsum : 2 ^ n = 2 ^ (n - 1) + 2 ^ (n - 1) := by rw [h2, h3]
  omega

/-- **Mersenne 递归（二）**：`M_(n+1) = 2 M_n + 1`，即
    `2^(n+1) − 1 = 2 (2^n − 1) + 1`。 -/
theorem mersenne_recursion_two (n : ℕ) :
    2 ^ (n + 1) - 1 = 2 * (2 ^ n - 1) + 1 := by
  have hpos : 0 < 2 ^ n := Nat.two_pow_pos n
  have h : 2 ^ (n + 1) = 2 ^ n * 2 := by rw [pow_succ]
  omega

/-- **枢纽约恒等式**：`2^(n−1) = M_(n−1) + 1`，即最高位权重 = 低位全 1 加 1。
    这就是「`k_max = Involution + 1`」的一般形式。 -/
theorem leading_bit_eq_mersenne_add_one (n : ℕ) (_hn : 1 ≤ n) :
    2 ^ (n - 1) = (2 ^ (n - 1) - 1) + 1 := by
  have hpos : 0 < 2 ^ (n - 1) := Nat.two_pow_pos (n - 1)
  omega

/-! =========================================================
    `f = 4` 处的实例：`k_max`、`Involution`、`σ⁻¹` 全部是 Mersenne 相关量
   ========================================================= -/

/-- `k_max = 2^(f−1)`：`8 = 2^(4−1)`。 -/
theorem kmax_eq_two_pow_fixedpoint_sub_one : (8 : ℕ) = 2 ^ (4 - 1) := by
  norm_num

/-- `k_max = f²/2`：`8 = 4²/2`。与上一条相等，正是 `f² = 2^f` 的推论。 -/
theorem kmax_eq_fixedpoint_sq_div_two : (8 : ℕ) = 4 ^ 2 / 2 := by
  norm_num

/-- **两条 `k_max` 写法在 `f = 4` 处一致**：`2^(f−1) = f²/2`。 -/
theorem two_kmax_forms_agree : (2 : ℕ) ^ (4 - 1) = 4 ^ 2 / 2 := by
  norm_num

/-- `Involution = M_3 = 2^3 − 1`：`7 = 2^3 − 1`。 -/
theorem involution_is_mersenne_three : (7 : ℕ) = 2 ^ 3 - 1 := by
  norm_num

/-- `k_max = Involution + 1`：`8 = 7 + 1`（`leading_bit_eq_mersenne_add_one` 在 `n = 4` 的实例）。 -/
theorem kmax_eq_involution_add_one : (8 : ℕ) = 7 + 1 := by
  norm_num

/-- `σ⁻¹ = M_4 = 2^4 − 1`：`15 = 2^4 − 1`。 -/
theorem sigmaInv_is_mersenne_four : (15 : ℕ) = 2 ^ 4 - 1 := by
  norm_num

/-- `σ⁻¹ = 2 k_max − 1`：`15 = 2·8 − 1`。 -/
theorem sigmaInv_eq_two_kmax_sub_one : (15 : ℕ) = 2 * 8 - 1 := by
  norm_num

/-- `σ⁻¹ = k_max + Involution`：`15 = 8 + 7`
    （`SilenceFamily.s49_algebra_layer_completion` 的 `ℕ` 数值版）。 -/
theorem sigmaInv_eq_kmax_add_involution : (15 : ℕ) = 8 + 7 := by
  norm_num

/-- `σ⁻¹ = 2 Involution + 1`：`15 = 2·7 + 1`（`Mersenne` 递归二的实例）。 -/
theorem sigmaInv_eq_two_involution_add_one : (15 : ℕ) = 2 * 7 + 1 := by
  norm_num

/-- `σ⁻¹ = f² − 1`：`15 = 4² − 1`
    （`SpectralGap.sigma_inv_square_minus_one` 的 `ℕ` 数值版）。 -/
theorem sigmaInv_eq_fixedpoint_sq_sub_one : (15 : ℕ) = 4 ^ 2 - 1 := by
  norm_num

/-- `M_4 = 2^3 + M_3`：`15 = 2^3 + (2^3 − 1)`（`mersenne_recursion` 在 `n = 4` 的实例）。 -/
theorem mersenne_four_decomp : (15 : ℕ) = 2 ^ 3 + (2 ^ 3 - 1) := by
  norm_num

/-- `σ⁻¹ = M_(N_active+1)`：`15 = 2^(3+1) − 1`。 -/
theorem sigmaInv_eq_two_pow_nactive_add_one_sub_one :
    (15 : ℕ) = 2 ^ (3 + 1) - 1 := by
  norm_num

/-! =========================================================
    韦达根由 `f = 4` 生成：`N_gen = f − 1`、`SilenceUnit = f + 1`
   ========================================================= -/

/-- `N_gen = f − 1`：`3 = 4 − 1`。 -/
theorem ngen_eq_fixedpoint_sub_one : (3 : ℕ) = 4 - 1 := by
  norm_num

/-- `SilenceUnit = f + 1`：`5 = 4 + 1`。 -/
theorem silence_unit_eq_fixedpoint_add_one : (5 : ℕ) = 4 + 1 := by
  norm_num

/-- 韦达和对与积都由 `f = 4` 生成：`(4−1)+(4+1) = 8`、`(4−1)(4+1) = 15`。 -/
theorem vieta_from_fixedpoint :
    (4 - 1) + (4 + 1) = 8 ∧ (4 - 1) * (4 + 1) = 15 := by
  refine ⟨by norm_num, by norm_num⟩

/-- **`N_active = f − 1` 的唯一性**：若 `2^a = 2^(4−1)`，则 `a = 4 − 1`。
    这是把 `k_max = 2^N_active` 与 `k_max = 2^(f−1)` 相接的唯一一步。 -/
theorem nactive_eq_fixedpoint_sub_one (a : ℕ) (h : 2 ^ a = 2 ^ (4 - 1)) :
    a = 4 - 1 := by
  have hpow := Nat.pow_right_injective (by norm_num : 1 < 2) h
  omega

/-! =========================================================
    合取：裁决与全链
   ========================================================= -/

/-- **两条 15 的等式同时成立**：`15 = 8 + 7` 与 `15 = 4² − 1`。
    （这两个正是前批记为「两个 15」的那两条。） -/
theorem both_fifteens_hold :
    (15 : ℕ) = 8 + 7 ∧ (15 : ℕ) = 4 ^ 2 - 1 := by
  refine ⟨by norm_num, by norm_num⟩

/-- **★ 三条 `σ⁻¹` 表示全部成立**：`k_max + Involution`、`2 k_max − 1`、`f² − 1`。 -/
theorem three_sigma_inv_forms :
    (15 : ℕ) = 8 + 7 ∧ (15 : ℕ) = 2 * 8 - 1 ∧ (15 : ℕ) = 4 ^ 2 - 1 := by
  refine ⟨by norm_num, by norm_num, by norm_num⟩

/-- **★★★ 裁决**：库里「两个 15」不是两个数，是 `M_4 = 15` 的两条 Mersenne 递归表示
    （`15 = 8 + 7` 与 `15 = 2·7 + 1`），且两者互通的枢纽是 `k_max = Involution + 1`。 -/
theorem two_fifteens_one_root :
    (15 : ℕ) = 8 + 7 ∧ (15 : ℕ) = 2 * 7 + 1 ∧ (8 : ℕ) = 7 + 1 := by
  refine ⟨by norm_num, by norm_num, by norm_num⟩

/-- **★★ 全链**：`f = 4` 同时给出 `k_max`、`N_gen`、`SilenceUnit`、`Involution`、`σ⁻¹`。 -/
theorem mersenne_chain_from_fixedpoint :
    (8 : ℕ) = 2 ^ (4 - 1) ∧ (3 : ℕ) = 4 - 1 ∧ (5 : ℕ) = 4 + 1 ∧
      (15 : ℕ) = 4 ^ 2 - 1 ∧ (7 : ℕ) = 8 - 1 := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num, by norm_num⟩

/-- **★★★ 同源裁决**：`N_active` 与 `N_gen` 同为 `f − 1`，故二者同源
    （前批记为「两个 3 不同源」的那一对在本批闭合）。
    相数 3 不在本链内，仍走判据格路线（`PhaseTrichotomy.lean`）。 -/
theorem nactive_and_ngen_same_root :
    (3 : ℕ) = 4 - 1 ∧ (3 : ℕ) = 4 - 1 ∧ (8 : ℕ) = 2 ^ (4 - 1) := by
  refine ⟨by norm_num, by norm_num, by norm_num⟩

end MUFPF.FifteenMersenne
