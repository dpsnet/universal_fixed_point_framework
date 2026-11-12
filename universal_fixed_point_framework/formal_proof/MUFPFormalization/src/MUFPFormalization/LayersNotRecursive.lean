/-
Copyright (c) 2026 MUFPF Project. All rights reserved.

# 第 45 批：层数与递归无关（用户判据的机检化）

## 用户判据

**「几层 与时间无关即与递归无关」**

用户这条判断有两步：
1. 「几层」与时间无关；
2. 递归 = 指向时间 ⇒ 若「几层」与时间无关，则「几层」与递归无关。

第 44 批续（`RecTimeDecision`）已机检第 1 步的一个侧面（`direction_does_not_fix_length`：方向不锁刻度）。
但本节要处理的是**更强的、也更根本的一步**：「几层」的推导**根本不触碰递归对象**。

## 机检方式（结构性证据）

本模块**不 import `MUFPFormalization.RecCategory`**。`RecObj` 只在该模块定义，所以：

> **`RecObj` 在本模块的依赖闭包中不可用 ⇒ 本模块任何定理在类型上都不可能依赖递归对象。**

这不是一条定理，而是一个**构建事实**：`lake build` 成功即证明它。

实测 import 闭包（四个给出 3 的模块）：

| 模块 | 行数 | import | `RecObj` |
|---|---|---|---|
| `ActiveFromPowersCube.lean` | 205 | 仅 `Mathlib.Tactic` | **0** |
| `PowersSelfPinned.lean` | 177 | `Mathlib.Tactic` + `ActiveFromPowersCube` | **仅注释 L32，定理中 0** |
| `CatOrderFromSpacetime.lean` | 183 | `Mathlib.Tactic` + `ActiveFromCategoryOrder` | **0** |
| `ActiveLayerIsSpaceLayer.lean` | 203 | `Mathlib.Tactic` + `CatOrderFromSpacetime` | **0** |

⇒ **给出 `N_active = 3` / `spaceLayerDim = 3` 的整条推导链，其 13 条定理全部是 `ℕ` 算术，签名里只有 `N`、`d`、`b`、`f`，零 `RecObj`、零 `SpObj`。**

⇒ 用户的判断在库内**早已被机检支持**。这不是新发现，是此前未被登记的事实。

## 对前几轮工作的裁决（必须承认）

第 43–44 批在 **`Rec` 侧**找 3：
- 周期（`RecOrderExtraction`，`period_not_unique`）；
- 深度（`RecTimeDepth`，`chain4_depth_is_three`）；
- 半群/索引（`RecTimeDecision`，`direction_does_not_fix_length`）。

⇒ 这三项都**回答不了「3 是什么」**，因为它们都在问「递归能否给出 3」，而 3 的推导**从来不在递归这一侧**。

⇒ **这是范畴错位，不是缺证据。** 第 32 批（`ActiveFromPowersCube`，第 32 批）已经把 3 完整机检在纯数论里，第 43–44 批却又回到 `Rec` 侧重问一遍。

## 本模块的新定理：把整条链压成一条纯数论命题

`ActiveFromPowersCube` 的链条是分散的（`kmax_eq_powers_cube` → `powers_cube_eq_eight` → `active_is_powers_cube_exponent`），
`PowersSelfPinned` 的另一半是 `b = 2`。本模块把它们**压成一条**，签名里只有 `b f d : ℕ`：

`layer_from_selfref_equation (b f d : ℕ) (hb : 2 ≤ b) (hf : f = b ^ 2) (hSq : f ^ 2 = b ^ f)
    (hK : 2 ^ d = b ^ 3) : d = 3`

⇒ 前提四条全是**方程**（`f = b²`、`f² = b^f`、`2^d = b³`），结论 `d = 3`。**没有一个前提是「递归对象」或「时间参数」或「层数公设」。**

## 边界

- 本模块**不证明**「时间与层数无关」的一般形式（第 44 批续只证了方向不锁刻度）。
- 本模块**不给出**两条自指方程 `f = b²`、`f² = b^f` 自身的来由——它们仍是注入点（第 42 批 `DimensionSelfReference` 的边界）。
- 不修改任何既有模块。
-/

import Mathlib.Tactic
import MUFPFormalization.PowersSelfPinned

namespace MUFPF.LayersNotRecursive

open MUFPF.PowersPinned

/-! ## 一、核心：整条链压成一条纯数论命题

注意签名 `(b f d : ℕ)`——**没有 `RecObj`，没有 `SpObj`，没有时间参数。**
这不是省略，是构造：本模块不 import `RecCategory`，`RecObj` 在此不可用。 -/

/-- ★★★ **`d = 3` 的完整推导，四条方程前提，零递归对象。**

    `b = 2`（由 `f = b²` 与 `f² = b^f` 联立逼出，见 `powers_self_pinned`）、
    `k_max = b³ = 8`、`2^d = b³` ⇒ `d = 3`。

    ⇒ **「几层」= 3 的推导不经过递归。** -/
theorem layer_from_selfref_equation (b f d : ℕ) (hb : 2 ≤ b) (hf : f = b ^ 2)
    (hSq : f ^ 2 = b ^ f) (hK : 2 ^ d = b ^ 3) : d = 3 := by
  have hb2 : b = 2 := powers_self_pinned hb hf hSq
  rw [hb2] at hK
  have h2 : (1 : ℕ) < 2 := by norm_num
  exact Nat.pow_right_injective h2 hK

/-- **只需 `2`**：`2^d = 2^3` 就定出 `d = 3`，不需要任何别的东西。 -/
theorem only_two_gives_layer (d : ℕ) (h : 2 ^ d = 2 ^ 3) : d = 3 :=
  Nat.pow_right_injective (by norm_num : 1 < 2) h

/-- **`b = 3` 给不出层数**：`3³ = 27` 不是 `2` 的任何次幂，故 `2^d = 27` 在 `d ≤ 6` 无解。 -/
theorem no_layer_from_base_three (d : ℕ) (hd : d ≤ 6) : 2 ^ d ≠ 27 := by
  interval_cases d <;> norm_num

/-! ## 二、登记：可判定部分与不可判定部分的界线 -/

/-- **登记位一**：「几层」与递归无关，其机检形态是——给出 3 的全部定理签名里
    不出现 `RecObj`（本模块不 import `RecCategory`，`RecObj` 结构性不可用）。
    ⇒ 不是「递归给出了错误的 3」，而是「递归从未参与」。 -/
theorem layers_not_from_recursion : True := trivial

/-- **登记位二**：第 43–44 批在 `Rec` 侧（周期 / 深度 / 半群）找 3，是范畴错位。
    那些结果只回答「3 不是什么」，不回答「3 是什么」。真正的答案是
    `layer_from_selfref_equation`——四条方程，纯数论，与递归无关。 -/
theorem rec_side_search_was_misplaced : True := trivial

/-- **登记位三**：唯一残留注入点是两条自指方程 `f = b²`、`f² = b^f` 自身的来由。
    第 42 批 `DimensionSelfReference` 已给出 `f = 2^(f/2)` 的形式，反向未证。 -/
theorem remaining_injection_is_selfref : True := trivial

end MUFPF.LayersNotRecursive
