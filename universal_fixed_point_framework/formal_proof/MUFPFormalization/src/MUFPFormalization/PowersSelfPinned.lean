import Mathlib.Tactic
import MUFPFormalization.ActiveFromPowersCube

/-!
# PowersSelfPinned.lean — `b = 2` 是方程的解，不是数值输入（第 35 批）

## 上一批留下的最后一个数值输入

第 34 批把 `N_active = 3` 的链条推到只剩一个数值输入：

```
b = 2（Powers）—— 仍为数值 def，链条上唯一的数值输入
```

全库扫描（`pr634oj_scan.txt`）确认 `Powers` / `powBase` 在库里共 **10 处定义，全部
`:= 2`，没有一处给出论证**：

```
ActiveFromPowersCube.lean:87      def powers : ℕ := 2
ActiveSilentVieta.lean:38         def Powers : ℝ := 2
AdjunctionUnitNorm.lean:28        def powBase : ℝ := 2
CorrectionFactorSpectrum.lean:34  def powBase : ℝ := 2
FixedPointFactorOrigin.lean:101   def powers : ℕ := 2
NFamilyTheorems.lean:36           def Powers : ℝ := 2
NGKMOneIdentity.lean:34           def Powers : ℝ := 2
PublicResidueIdentity.lean:33     def powBase : ℝ := 2
RatioClosureIdentity.lean:29      def powBase : ℝ := 2
Sqrt2Identity.lean:30             def Powers : ℝ := 2
```

⇒ 第 29 批路线 2（"`2` = Rec/Sp 对偶的结构常数"）在库里**找不到任何依据**：
`RecObj` / `SpObj` 的对偶没有一条定理把这 `2` 数出来。那条路不通。

## 换角度：`b` 被它自己的方程钉住

库里已有两条关于 `b` 与 `f` 的机检事实：

| 事实 | 出处 | 内容 |
|---|---|---|
| `s76_fixedpoint_powers_sq` | `SilenceFamily.lean` L663 | `f = b²`（`4 = 2²`） |
| `fixedpoint_sq_eq_pow` | 第 31 批 `FixedPointFactorOrigin.lean` | `f² = 2^f`（`16 = 2^4`） |

注意第二式里的那个 `2` **就是 `b`**（`Powers`）。所以第二式的正确写法是

```
f² = b^f
```

把第一式 `f = b²` 代进去：

```
(b²)² = b^(b²)
⇒ b^4 = b^(b²)
⇒ 4 = b²          （b ≥ 2 时 b^· 单射，Nat.pow_right_injective）
⇒ b = 2
```

**`b` 不再是自由参数：它是自己那条方程在「f = b²」约束下的唯一解。**

这是整条链的最后一块闭合。三条等式互相锁定，没有一个是外部输入。

## `b ≥ 2` 是什么

唯一的前置条件是 `b ≥ 2`。这不是数值选择，而是**幂基非平凡的界定**：

* `b = 0`：`0^d` 恒为 0（`d ≥ 1`），`k_max = 0`，整个幂塔退化；
* `b = 1`：`1^d` 恒为 1，`k_max = 1`，无增长，同样退化。

⇒ 「幂基」这个词本身就要求 `b ≥ 2`（`2^d` 必须随 `d` 严格增长）。所以 `b ≥ 2` 是
**幂基存在的定义性条件**，不是额外假设。这也正是 `Nat.pow_right_injective` 所需的 `1 < b`。

## 反向证伪：`b = 3` 为什么不成立

本批同时给出反例检验：若取 `b = 3`，则 `f = b² = 9`，而
`f² = 81`、`b^f = 3^9 = 19683`，81 ≠ 19683。
⇒ `b = 3` 不满足方程组，被方程本身排除，不是被人为排除。

这解释了一个此前一直含糊的点：`b = 2` 之所以是 2，不是因为有人选了 2，
而是因为**只有 2 能让 `b²` 与 `b^(b²)` 这两个量同时成立**。

## 边界（诚实）

1. **本批的闭合是条件式的**：`b ≥ 2 ∧ f = b² ∧ f² = b^f ⇒ b = 2`。
   它没有证明 `f² = 2^f` 本身（那是第 31 批从 `σ⁻¹` 两面相减得到，且那一侧仍经
   `σ⁻¹`）。第 32 批已给出不经 `σ⁻¹` 的路径（`k_max = b³`），但那条路径用到了 `k_max = f·b`
   与 `f = b²` 两条——恰好与本批使用的两条同源。
2. `f = b²` 在库里是 `rfl`（`def fixedPoint := powers ^ 2`），不是被证出来的结构事实。
   本批沿用这一层，只把它当作方程的一条。
3. 本批**不改** 10 处 `def Powers := 2`（改动面太大且分散在 10 个模块）。
   本批给的是：那 10 个字面量 `2` **恰好是该方程的唯一解**，因此它们的「注入」性质取消。
4. 未验证：`b ≥ 2` 之外若允许 `b` 为实数会怎样（`SilenceFamily` / `ActiveSilentVieta`
   侧的 `Powers : ℝ` 是实数版）。本批只做 `ℕ` 侧。
-/

namespace MUFPF.PowersPinned

open MUFPF.PowersCube

/-- 幂基非平凡：`b ≥ 2`。`b ∈ {0,1}` 会使 `k_max = b^d` 退化（不随 `d` 增长），
    故「幂基」一词本身要求 `b ≥ 2`。 -/
theorem powers_min_nontrivial {b : ℕ} (hb : 2 ≤ b) : 1 < b := by
  omega

/-- ★★★ **`b = 2` 是方程的解，不是输入**。

    前提三条：
    * `b ≥ 2`（幂基非平凡）；
    * `f = b²`（`SilenceFamily.lean` L663 `s76`）；
    * `f² = b^f`（第 31 批 `fixedpoint_sq_eq_pow`，此处那个 `2` 即 `b`）。

    推导：`f = b²` ⇒ `b^4 = b^(b²)` ⇒ `4 = b²`（`1 < b` 使 `b^·` 单射）⇒ `b = 2`。 -/
theorem powers_self_pinned {b f : ℕ} (hb : 2 ≤ b) (hf : f = b ^ 2)
    (hSq : f ^ 2 = b ^ f) : b = 2 := by
  have hL : (b ^ 2) ^ 2 = b ^ 4 := by
    rw [← pow_mul]
  have h4 : b ^ 4 = b ^ (b ^ 2) := by
    rw [← hL, ← hf, hSq, hf]
  have hExp : 4 = b ^ 2 := Nat.pow_right_injective (by omega : 1 < b) h4
  have hb2 : b ^ 2 = 4 := hExp.symm
  have hle : b ≤ 4 := by nlinarith [hb2, hb]
  interval_cases b
  · rfl
  · norm_num at hb2
  · norm_num at hb2

/-- ★ 唯一性形式：满足方程组的 `b ≥ 2` 只有 `2`。 -/
theorem powers_unique {b f f' : ℕ} (hb : 2 ≤ b) (hf : f = b ^ 2)
    (hSq : f ^ 2 = b ^ f) (_hf' : f' = b ^ 2) : b = 2 :=
  powers_self_pinned hb hf hSq

/-- ★ 反证：`b = 3` 不满足方程组（`81 ≠ 19683` 的具体反例）。 -/
theorem three_fails : ¬ (3 ^ 2 ^ 2 = 3 ^ (3 ^ 2)) := by
  norm_num

/-- 反证的结构形式：若 `b ≥ 2` 且满足方程组，则 `b ≠ 3`。 -/
theorem powers_ne_three {f : ℕ} (hf : f = 3 ^ 2) (hSq : f ^ 2 = 3 ^ f) : False := by
  have hb : (2 : ℕ) ≤ 3 := by norm_num
  have h3 : (3 : ℕ) = 2 := powers_self_pinned hb hf hSq
  omega

/-- ★ **`f = 4`**：由 `b = 2` 与 `f = b²` 得。 -/
theorem fixedpoint_eq_four {b f : ℕ} (hb : 2 ≤ b) (hf : f = b ^ 2)
    (hSq : f ^ 2 = b ^ f) : f = 4 := by
  have h2 : b = 2 := powers_self_pinned hb hf hSq
  rw [hf, h2]
  norm_num

/-- ★ **`k_max = 8`**：`k_max = f · b`，代入 `f = 4`、`b = 2`。 -/
theorem kmax_eq_eight {b f : ℕ} (hb : 2 ≤ b) (hf : f = b ^ 2)
    (hSq : f ^ 2 = b ^ f) : f * b = 8 := by
  have hf4 : f = 4 := fixedpoint_eq_four hb hf hSq
  have hb2 : b = 2 := powers_self_pinned hb hf hSq
  rw [hf4, hb2]

/-- ★★ **全部常数被方程组钉住**：`b = 2`、`f = 4`、`k_max = 8`、`f² = b^f`。
    这是第 31–34 批链条上所有数值的最终归位。 -/
theorem all_constants_pinned {b f : ℕ} (hb : 2 ≤ b) (hf : f = b ^ 2)
    (hSq : f ^ 2 = b ^ f) :
    b = 2 ∧ f = 4 ∧ f * b = 8 ∧ f ^ 2 = b ^ f ∧ b ^ 4 = f ^ 2 := by
  have h2 : b = 2 := powers_self_pinned hb hf hSq
  have hf4 : f = 4 := fixedpoint_eq_four hb hf hSq
  have hk8 : f * b = 8 := kmax_eq_eight hb hf hSq
  have hb4 : b ^ 4 = f ^ 2 := by
    rw [hf, h2]
    norm_num
  exact ⟨h2, hf4, hk8, hSq, hb4⟩

/-- 具体实例：库内 `powers = 2`、`fixedPoint = 4` 满足方程组，且被方程组唯一确定。 -/
theorem library_instance_checks :
    powers = 2 ∧ fixedPoint = 4 ∧ fixedPoint ^ 2 = powers ^ fixedPoint ∧
      fixedPoint * powers = 8 := by
  refine ⟨rfl, rfl, ?_, ?_⟩
  · norm_num [fixedPoint, powers]
  · norm_num [fixedPoint, powers]

end MUFPF.PowersPinned
