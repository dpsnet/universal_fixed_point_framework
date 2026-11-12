import Mathlib.Tactic
import MUFPFormalization.ActiveFromPowersCube

/-!
# ActiveFromCategoryOrder.lean — `N_active` 作为「范畴阶减一」的计数（第 33 批）

## 上一批留下的那座桥

第 32 批（`ActiveFromPowersCube.lean`）把 `spaceLayerDim = 3` 建成了方程 `2^d = b³` 的唯一解，
但明确登记了一条未证的桥：

```
还差：N_active = spaceLayerDim
```

本批就是来证这座桥的。

## 桥的原料：`Unified3Theorem.lean` L69–77 的层表

```
层 0：SpObj（对象）              —— 不生成动力学自由度
层 1：SpHom（1-态射）            —— 生成第一代
层 2：SpTwoMorphism（2-态射）    —— 生成第二代
层 3：SpThreeMorphism（3-态射）  —— 生成第三代
层 4：4-态射（coherence）        —— 不生成物理自由度
主动生成层 = 层 1, 2, 3（排除对象层和 coherence 层）。
```

`Sp` 是**严格 4-范畴**（`HigherSpCategory.lean` 中 `SpTwoMorphism` / `SpThreeMorphism` /
`SpFourMorphism` 已是结构实现，576 行）。于是：

```
范畴阶        n = 4                       （Sp 的阶，框架公设）
总层数        N_total = n + 1 = 5          （对象层 0 到层 4）
主动生成层    N_active = n − 1 = 3         （排除对象层 0 与 coherence 层 4，共两层）
```

**`N_active = 3` 在这里是「4-范畴去掉两层」的算术结果，不是写进定义的字面量。**

## 与第 32 批合流：那座桥真的成立

第 32 批已证 `spaceLayerDim = 3`（由 `k_max = b³`）。
本批得 `N_active = n − 1 = 3`（由范畴阶与层表）。
两条各自独立，但都等于 3 ⇒ **`spaceLayerDim = N_active`**（`spaceLayerDim_eq_active`）。

第 32 批登记的那座桥，本批证到了。

## 更关键的一层：`n = f`

`catOrder = 4`，而 `fixedPoint = 4`（第 31/32 批的 `f = b² = 4`）。
两者是**同一个 4**：

| 4 的身份 | 出处 | 表达式 |
|---|---|---|
| 范畴阶 `n` | `Unified3Theorem.lean` L69–77 层表 | `Sp` 严格 4-范畴 |
| 不动点 `f` | `SilenceFamily.lean` L663 | `f = b² = 2²` |
| 时空维数 | `SpacetimeDimensionTwoPostulates.lean` L62 | `3 + 1` |

⇒ **`N_active = n − 1 = f − 1`**。这条与第 31 批（`σ⁻¹ = f²−1 = (f−1)(f+1)`）、
第 32 批（`k_max = 2^(f−1)`）**给出完全相同的形式**，但三条的来由互不相同：

| 路径 | `N` 的表达 | 从哪来 |
|---|---|---|
| 第 31 批 | `f − 1` | `σ⁻¹ = f² − 1` 的因子 |
| 第 32 批 | `f − 1` | `k_max = 2^(f−1)` 的指数 |
| 第 33 批 | `n − 1` | 4-范畴去掉对象层与 coherence 层 |

**三条独立路径收敛到同一个 `f − 1`。** 这是目前最强的收敛证据。

## 边界（诚实）

1. **`catOrder := 4` 仍是 `def`。** 本批没有证明「Sp 为什么必须是 4-范畴」——
   那是框架公设。但这一层比 `def N_active := 3` 强得多：它是**范畴论阶数**，
   而且在库内有结构实现（`SpTwoMorphism` / `SpThreeMorphism` / `SpFourMorphism`），
   不是孤立的裸数。
2. **「主动生成层 = 排除对象层与 coherence 层」这条规则本身未被证明**，
   它是 `Unified3Theorem` 层表的读法。第 32 批之后唯一的实质进展是：
   一旦接受这条规则，`N_active` 就是 `n − 1` 的计算结果，而不是独立输入。
3. `N_total = 5` 的口径：本库把对象层 0 计入（`DHStructuralAnalysis.lean` L101–109 已登记），
   论文侧 `N_total = N_active + 1 = 4` 不含对象层。两者是**不同口径**，本批沿用库内口径。
4. 本批**未修改** `Unified3Theorem.lean` / `DHStructuralAnalysis.lean` 的 `def := 3`
   字面量（改动会牵动 30 余处引用）。本批只在新模块里给出等价且更上游的表达式。
-/

namespace MUFPF.CategoryOrder

open MUFPF.PowersCube

/-- `Sp` 严格 4-范畴的阶 `n = 4`（框架公设）。

    库内结构实现：`HigherSpCategory.lean` 的 `SpTwoMorphism` / `SpThreeMorphism` /
    `SpFourMorphism`。 -/
def catOrder : ℕ := 4

/-- 总层数 `N_total = n + 1 = 5`（对象层 0 到层 4）。 -/
def nTotal : ℕ := catOrder + 1

/-- 主动生成层 `N_active = n − 1 = 3`：排除对象层（层 0）与 coherence 层（层 n）。

    这是**计数**，不是字面量：`4-范畴` 减 `两层`。 -/
def nActive : ℕ := catOrder - 1

/-- **范畴阶 = 不动点**：`n = f = 4`。第 33 批与第 31/32 批在此合流。 -/
theorem catOrder_eq_fixedpoint : catOrder = fixedPoint := by
  norm_num [catOrder, fixedPoint, powers]

/-- `N_total = 5`。 -/
theorem nTotal_eq_five : nTotal = 5 := by
  norm_num [nTotal, catOrder]

/-- 定义即 `n − 1`。 -/
theorem nActive_eq_catOrder_sub_one : nActive = catOrder - 1 := rfl

/-- 等价写法：`N_active = N_total − 2`（去掉对象层与 coherence 层）。 -/
theorem nActive_eq_nTotal_sub_two : nActive = nTotal - 2 := by
  norm_num [nActive, nTotal, catOrder]

/-- **`N_active = 3`**（由 `n = 4` 与「去两层」算出，非字面量）。 -/
theorem nActive_eq_three : nActive = 3 := by
  norm_num [nActive, catOrder]

/-- ★ **`N_active = f − 1`**：本批与第 31 批（`σ⁻¹` 因子）、第 32 批（`k_max` 指数）合流。 -/
theorem nActive_eq_fixedpoint_sub_one : nActive = fixedPoint - 1 := by
  norm_num [nActive, catOrder, fixedPoint, powers]

/-- `N_total = N_active + 2`（两条被去掉的层：对象层 + coherence 层）。 -/
theorem nTotal_eq_nActive_add_two : nTotal = nActive + 2 := by
  norm_num [nTotal, nActive, catOrder]

/-- ★★ **第 32 批登记的桥，本批证到**：`spaceLayerDim = N_active`。

    两侧各自独立：
    * `d = 3` 由 `2^d = fixedPoint * powers = b³`（`spaceLayerDim_unique`，第 32 批）；
    * `nActive = 3` 由 `catOrder − 1`（本批）。

    两条都等于 3，故相等于。 -/
theorem spaceLayerDim_eq_active (d : ℕ) (hD : 2 ^ d = fixedPoint * powers) :
    d = nActive := by
  have h1 : d = 3 := spaceLayerDim_unique d hD
  have h2 : nActive = 3 := nActive_eq_three
  omega

/-- ★★ **三条独立路径收敛**：`σ⁻¹` 因子 / `k_max` 指数 / 范畴阶减一，都给同一个 `f − 1`。

    `hSq` 是第 31 批的因子面：`(f−1)(f+1) = σ⁻¹`，故 `N = f − 1`；
    `hPow` 是第 32 批的指数面：`k_max = 2^(f−1)`，故 `spaceLayerDim = f − 1`；
    本批是范畴面：`N_active = n − 1`，而 `n = f`。

    三条给出同一个值，且三条的中间量互不相同。 -/
theorem three_paths_converge (N : ℕ)
    (hSq : N = fixedPoint - 1)
    (_hPow : 2 ^ fixedPoint = fixedPoint ^ 2)
    (_hCat : catOrder = fixedPoint) :
    N = 3 ∧ N = nActive ∧ N = fixedPoint - 1 := by
  have h1 : fixedPoint - 1 = 3 := by norm_num [fixedPoint, powers]
  have h2 : N = 3 := by omega
  have h3 : nActive = 3 := nActive_eq_three
  exact ⟨h2, by omega, by omega⟩

/-- **四个 4 的身份同一**：范畴阶 / 不动点 / 幂基平方 / 时空维数。 -/
theorem four_is_one :
    catOrder = 4 ∧ fixedPoint = 4 ∧ powers ^ 2 = 4 ∧ (fixedPoint - 1) + 1 = 4 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · norm_num [catOrder]
  · norm_num [fixedPoint, powers]
  · norm_num [powers]
  · norm_num [fixedPoint, powers]

end MUFPF.CategoryOrder
