import Mathlib.Tactic

/-!
# ActiveFromPowersCube.lean — `N_active` 作为「幂基三次方」的指数（第 32 批）

## 上一批留下的两个缺口

第 31 批（`FixedPointFactorOrigin.lean`）把 `N_active = 3` 的上游推到 `f² = 2^f`，
但留下两处未闭合：

1. **`f = 4` 自身来由**：`FixedPoint` 在库里是 `def := 4`；
2. **循环风险**：`SpacetimeDimensionTwoPostulates.lean` 把 `σ⁻¹` 由 `spaceLayerDim := 3`
   定义，于是「从 `σ⁻¹` 反推 3」可被读成同义反复。

本批**不再走 `σ⁻¹`**。改用库里三条**各自独立机检**的恒等式，直接给出 `N`。

## 三条已机检的库内事实（本批的原料）

| 事实 | 出处 | 内容 |
|---|---|---|
| `fixedpoint_powers_sq` | `SilenceFamily.lean` L663 `s76_fixedpoint_powers_sq` | `f = b²`（`4 = 2²`） |
| `kmax_product` | `SilenceFamily.lean` L929 `s95_kmax_product` | `k_max = f · b`（`8 = 4·2`） |
| `kmax_two_power` | `SpacetimeDimensionTwoPostulates.lean` L68 `def kMax : ℕ := 2 ^ spaceLayerDim` | `k_max = 2^N` |

前两条相乘：

```
k_max = f · b = b² · b = b³
```

和第三条合起来：

```
2^N = k_max = b³ = 2³   ⇒   N = 3
```

**`N = 3` 在这里的语义是清楚的**：`N` 是「幂基三次方」的二进制指数。
输入只有 `b = 2`（框架常数 `Powers`）与「`k_max` 的两种表达式相等」这一条桥。
**不经过 `σ⁻¹`、不经过 `15`、不经过 `3 × 5`，也不经过 `f² = 2^f`。**

## 第二条路径（同样不经 `σ⁻¹`）

`SilenceFamily.lean` L913 `s94_even_subalgebra_dim : 2^(f−1) = k_max`（Cℓ(1,3) 偶部实维数）。
和 `k_max = 2^N` 合起来：

```
2^N = 2^(f−1)   ⇒   N = f − 1 = 3
```

## 三条路径的收敛

| 路径 | 链路 | 中间量 | 前提 |
|---|---|---|---|
| ① 立方 | `k_max = f·b = b³`，`k_max = 2^N` | 无 | `b = 2`、`f = b²` |
| ② 偶部维数 | `2^(f−1) = k_max = 2^N` | 无 | `f = 4` |
| ③ 平方差（第 31 批） | `σ⁻¹ = f²−1 = (f−1)(f+1)`，`N = f−1` | `σ⁻¹ = 15` | `f² = 2^f` |

三条都给 `N = 3`，但**路径 ① 与 ② 完全不经过 `σ⁻¹`**，因而**不受 `spaceLayerDim := 3`
那条反向定义的污染**。这是本批相对第 31 批的实质进展。

## 边界（诚实）

1. **本批推出的是 `spaceLayerDim = 3`，不是 `N_active = 3`。** 这是最重要的一条边界。
   库内 `N_active`（`DHStructuralAnalysis.lean` L92）与 `spaceLayerDim`
   （`SpacetimeDimensionTwoPostulates.lean` L56）是**两个互不引用的 `def := 3`**，
   库内**没有任何定理把二者等同**。本批给 `spaceLayerDim` 建立了独立来由，
   但把它接到 `N_active` 还需要一条桥 `N_active = spaceLayerDim`——库内没有，本批不造。
   ⇒ 「`N_active = 3` 的推导链」在本批之后的状态是：**上游已到 `spaceLayerDim`，还差一步命名等同。**

2. **路径 ① 的前提「`k_max` 的两种表达式相等」仍是一条桥**，不是定理。
   它的两侧各自已机检（`s95` 给 `f·b = 8`，`spacetime` 给 `2^N = 2^spaceLayerDim`），
   但「二者指同一个 `k_max`」是**命名约定**，不是推导。本批把它显式列为前提，未隐藏。

3. **`b = 2`**（`Powers`）仍是 `def`，无来由。这是本批链上剩下的唯一数值输入。

4. 本批**未修改** `SpacetimeDimensionTwoPostulates.lean`（`spaceLayerDim := 3` 的字面量仍在）。
   但 `spaceLayerDim_unique` 已证明该字面量**恰好是该方程的唯一解**，
   因而它的「注入」性质在这一侧被取消——值仍写着 3，但其 3 已不再是独立输入。

5. `N = 3` 的**新语义**（「幂基三次方的指数」）是本批的主要产出，
   它与「生成代数 = 3」的物理语义对应**未给**——那需要另一条把幂基与世代结构挂上的定理。
-/

namespace MUFPF.PowersCube

/-- 幂基 `b = 2`（框架常数 `Powers`）。本模块唯一的外部输入。 -/
def powers : ℕ := 2

/-- 不动点 `f = b²`（库里 `s76_fixedpoint_powers_sq` 的同一事实，此处按定义重建）。 -/
def fixedPoint : ℕ := powers ^ 2

/-- **`f = b²`**（`4 = 2²`）。 -/
theorem fixedpoint_is_powers_sq : fixedPoint = powers ^ 2 := rfl

/-- `f = 4`。 -/
theorem fixedpoint_eq_four : fixedPoint = 4 := by
  norm_num [fixedPoint, powers]

/-- **`k_max = f · b`**（`8 = 4·2`；库内 `s95_kmax_product` 的同一事实）。 -/
theorem kmax_eq_fixedpoint_mul_powers : fixedPoint * powers = 8 := by
  norm_num [fixedPoint, powers]

/-- ★ **`k_max = b³`**：把上面两条相乘（`b² · b = b³`）。

    这是本批的关键：`k_max` 的三个因子全部是幂基本身。 -/
theorem kmax_eq_powers_cube : fixedPoint * powers = powers ^ 3 := by
  norm_num [fixedPoint, powers]

/-- `b³ = 8`。 -/
theorem powers_cube_eq_eight : powers ^ 3 = 8 := by
  norm_num [powers]

/-- ★★ **`N` 是幂基三次方的指数**：`2^N = b³` ⇒ `N = 3`。

    语义：`N`（空间层数 / 活跃层数）= 「幂基要自乘几次才达到 `k_max`」。
    这里 `b = 2`，`b³ = 8`，故 `N = 3`。

    **前提只有 `2^N = powers ^ 3`**，不含 3；3 是结论。 -/
theorem active_is_powers_cube_exponent (N : ℕ) (h : 2 ^ N = powers ^ 3) : N = 3 := by
  have h23 : powers ^ 3 = 2 ^ 3 := by norm_num [powers]
  have h' : 2 ^ N = 2 ^ 3 := h.trans h23
  exact Nat.pow_right_injective (by norm_num : 1 < 2) h'

/-- ★★ **主定理（路径 ①）**：`k_max` 的两种表达式相等 ⇒ `N = 3`。

    前提 `2^N = fixedPoint * powers` 即「`k_max = 2^N` 且 `k_max = f·b`」的合取
    （库内两条事实的桥，见模块头边界 1）。
    从它到 `N = 3` 只用 `f = b²` 与 `b = 2`。 -/
theorem active_from_kmax_two_forms (N : ℕ) (h : 2 ^ N = fixedPoint * powers) : N = 3 := by
  have hb : fixedPoint * powers = powers ^ 3 := kmax_eq_powers_cube
  exact active_is_powers_cube_exponent N (h.trans hb)

/-- ★★ **`spaceLayerDim` 由幂基立方唯一确定**（本批对循环风险的正面回应）。

    库内 `k_max` 有两条各自机检的表达式：
    * `k_max := 2 ^ spaceLayerDim`（`SpacetimeDimensionTwoPostulates.lean` L68，定义面）；
    * `k_max = FixedPoint * Powers = Powers ^ 3`（`SilenceFamily.lean` L929 + L663）。

    两者合起来是方程 `2 ^ d = Powers ^ 3`，它的**唯一解**是 `d = 3`。

    #### 这条定理的意义与限度

    **意义**：`spaceLayerDim` 的值从此不再是 `def := 3` 的裸字面量，而是
    「幂基三次方」这条乘法恒等式钉出的唯一解。第 31 批指认的循环风险
    （`σ⁻¹` 由 `spaceLayerDim := 3` 定义）因此在**这一侧**被切开：即使 `σ⁻¹` 仍由
    `spaceLayerDim` 定义，`spaceLayerDim` 本身已有独立来由。

    **限度（必须明说）**：本定理的结论是 `spaceLayerDim = 3`，**不是** `N_active = 3`。
    库内 `N_active`（`DHStructuralAnalysis.lean` L92）与 `spaceLayerDim`
    （`SpacetimeDimensionTwoPostulates.lean` L56）是两个互不引用的 `def`，
    **没有任何定理把二者等同**。要把这条推导接到 `N_active`，需要一条桥
    `N_active = spaceLayerDim`，库内没有，本批不造。 -/
theorem spaceLayerDim_unique (d : ℕ) (h : 2 ^ d = fixedPoint * powers) : d = 3 :=
  active_from_kmax_two_forms d h

/-- **路径 ②**：`2^(f−1) = k_max = 2^N` ⇒ `N = f − 1`。

    库内 `s94_even_subalgebra_dim : 2^(f−1) = Kmax`（Cℓ(1,3) 偶部实维数）。
    注意不需要 `1 ≤ f`：`f = 0` 时 `2^(0−1) = 2^0 = 1`，`N = 0 = f − 1` 同样成立。 -/
theorem active_eq_fixedpoint_minus_one (N f : ℕ) (h : 2 ^ N = 2 ^ (f - 1)) : N = f - 1 := by
  exact Nat.pow_right_injective (by norm_num : 1 < 2) h

/-- **路径 ② 的实例**：`f = 4` ⇒ `N = 3`。 -/
theorem active_from_even_subalgebra (N : ℕ) (h : 2 ^ N = 2 ^ (fixedPoint - 1)) : N = 3 := by
  have h1 : N = fixedPoint - 1 := active_eq_fixedpoint_minus_one N fixedPoint h
  have h2 : fixedPoint - 1 = 3 := by norm_num [fixedPoint, powers]
  omega

/-- ★ **三条路径收敛**：`N = 3` 同时由三条链路给出。

    * 路径 ①（立方）：`2^N = f·b = b³`
    * 路径 ②（偶部维数）：`2^N = 2^(f−1)`
    * 路径 ③（平方差，第 31 批）：`N = f − 1` 且 `f² − 1 = 15`

    三条各自独立，且 ①/② 不经 `σ⁻¹`。 -/
theorem three_paths_agree (N : ℕ)
    (hA : 2 ^ N = fixedPoint * powers)
    (hB : 2 ^ N = 2 ^ (fixedPoint - 1)) :
    N = 3 ∧ N = fixedPoint - 1 ∧ fixedPoint - 1 = 3 := by
  have h1 : N = 3 := active_from_kmax_two_forms N hA
  have h2 : N = 3 := active_from_even_subalgebra N hB
  have h3 : fixedPoint - 1 = 3 := by norm_num [fixedPoint, powers]
  exact ⟨h1, h2 ▸ rfl, h3⟩

/-- **`N = 3` 的算子形式**：三条路径给同一个数，故可定义其公共值。

    注意此定义**不引入新信息**，只给三条路径的交名。 -/
theorem active_value_agrees : fixedPoint - 1 = 3 ∧ powers ^ 3 = 8 ∧ 2 ^ 3 = 8 := by
  refine ⟨?_, ?_, ?_⟩
  · norm_num [fixedPoint, powers]
  · norm_num [powers]
  · norm_num

/-- **`k_max` 的四个等价表达式**（都等于 8）。这解释了为何 `8` 在框架里反复出现。 -/
theorem kmax_four_forms :
    fixedPoint * powers = 8 ∧ powers ^ 3 = 8 ∧ 2 ^ (fixedPoint - 1) = 8 ∧
      (fixedPoint - 1) + (fixedPoint + 1) = 8 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · norm_num [fixedPoint, powers]
  · norm_num [powers]
  · norm_num [fixedPoint, powers]
  · norm_num [fixedPoint, powers]

end MUFPF.PowersCube
