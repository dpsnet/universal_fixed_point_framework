import Mathlib.Tactic

/-!
# FixedPointFactorOrigin.lean — 不动点 `f = 4` 作为 `k_max` / `σ⁻¹` / `N_active` 的共同上游（第 31 批）

## 问题

第 28 批（`SigmaInvActiveSelect.lean`）用 `σ⁻¹ = 15` 的互补分解 `3 × 5` 逼出
`N_active = 3`，但把两件事列为**注入点**：

* 注入点 1：「`σ⁻¹` 恰好是 `M_4 = 2^4 − 1`」——只是数值观测，无机制。
* 注入点 2：「`σ⁻¹` 的互补分解两因子之和恰是 `k_max`」——未证。

本批不去修补第 28 批的说法，而是**换到更上游的一个变量**上重述整条链：
把 `f := 4`（库内 `FixedPoint`）当作唯一输入，看 `k_max`、`σ⁻¹`、`N_active`
是否都由它**代数地**给出。

## 更严重的：第 28 批在库内存在反向定义路径

`SpacetimeDimensionTwoPostulates.lean` L56–74 把 `σ⁻¹` **由 3 定义**：

```
def spaceLayerDim : ℕ := 3
def kMax : ℕ := 2 ^ spaceLayerDim              -- 2^3 = 8
def silenceUnit : ℕ := kMax - spaceLayerDim     -- 8 − 3 = 5
def sigmaInv : ℕ := spaceLayerDim * silenceUnit -- 3 × 5 = 15
```

⇒ 在库内「σ⁻¹ = 15」至少有两条路径：一条以 3 为输入（上），一条是框架常数
`σ = 1/15`（`SilenceFamily.lean`）。**因此第 28 批「从 σ⁻¹ 反推 3」不能算独立推导**——
它可以被读成同义反复。这一点第 28 批的模块头没有指出，本批补上。

## 本批找到的上游：`f² = 2^f`

库内 `σ⁻¹ = 15` 有两个**不含 3** 的表达式：

| 表达式 | 出处 | 内容 |
|---|---|---|
| Mersenne 面 | `SilenceFamily.lean` L862–866 | `σ⁻¹ + 1 = 2^4`（指数 4 = `FixedPoint`） |
| 平方差面 | `SpectralGap.lean` L355 | `15 = (4−1)(4+1)` |
| 全态减单位 | `SilenceFamily.lean` L405 | `15 = 16 − 1` |

把两面相减即得 **`f² = 2^f`**（`f = 4`）。于是：

```
f² = 2^f  ∧  f ≥ 3        （非退化）
  ⇒ f = 4
  ⇒ σ⁻¹ = f² − 1 = (f−1)(f+1) = 3 × 5
  ⇒ N_active = f − 1 = 3
  ⇒ k_max = 2f = 8
  ⇒ 韦达判别式 (2f)² − 4(f²−1) = 4（恒等式，与 f 无关）
```

**关键**：注入点 2（「互补和 = k_max」）在这里不再是观察，而是平方差恒等式
`(f−1)+(f+1) = 2f`；注入点 1（「为何是 M_4」）等价于「`f² = 2^f` 取非退化解」。

`f² = 2^f` 的解集 `{2, 4}` 已在 `OverlapClosedLayerOrigin.lean`
（`overlap_neg_two` / `overlap_neg_four`）机检。`f = 2` 给 `N = 1`（退化），故取 `f = 4`。

## 与「相数 = 3」的关系（本批的诚实结论）

相数 3 来自「2 个二值判据 ⇒ 4 格，排除 1 格」（第 29 批）。于是两个 3 都可写成 `4 − 1`：

| 3 的来处 | 那个 4 | 4 的表达式 | 「4」的含义 |
|---|---|---|---|
| `N_active` | `f = 4` | `2^2` | 不动点：`f² = 2^f` 的非退化解 |
| 相数 | 判据组合格数 | `2^2` | 两个二值判据的笛卡尔积 |

**形式同构（都形如 `4 − 1`），语义仍不同源**：前者那个 2 是幂基（框架常数
`Powers`），后者那个 2 是**判据个数**（层 2 / 层 3 各一个 condition）。两者数值同为 2，
但一个是常数、一个是结构计数——没有理由认为它们是同一个 2。

⇒ 本批**不**声称「两个 3 同源」。声称的是更弱、但可机检的一条：
两个 3 都可写成「某个 `4` 减 1」，而这两个 `4` 的 `2²` 结构是**数值上的重合**，
是否同源仍未闭合。关闭它需要一条把 `Powers`（幂基）与「判据个数」焊上的定理，
库内**没有**。

## 不注入声明

本批的输入只有 `f := 4`（库内既有的 `FixedPoint`）与 `Powers := 2`。`N_active`、`k_max`、
`σ⁻¹` 全部是**输出**，不进入任何前提。对参数陈述的定理（`discriminant_generic`）里
不出现 3、8、15。

## 边界

1. `f = 4` 的**自身来由**不在本批：`FixedPoint` 在库内是 `def`。本批只把「下游三个数」
   归到它，没有把「f = 4」归到更上游。
2. `f² = 2^f` 的解集本批只对 `f < 9` 机检（`decide`），**不**作全域断言；
   全域唯一性需要分析论证，本批不做。
3. 本批不修改第 28 批模块，只在新模块里指出其反向定义路径（见上）。
4. 「两个 3 同源」**未闭合**，理由见上节。
-/

namespace MUFPF.FixedPointOrigin

/-- 不动点 `f = 4`（库内 `ActiveSilentVieta.FixedPoint` 的同一数值）。
    本模块把它作为**唯一上游输入**。 -/
def fixedPoint : ℕ := 4

/-- 幂基 `b = 2`。 -/
def powers : ℕ := 2

/-- ★ **不动点方程**：`f² = 2^f`（`4² = 2⁴ = 16`）。

    这是本批的枢纽：库内 `σ⁻¹ = 15` 的 Mersenne 面（`σ⁻¹+1 = 2^4`）与
    平方差面（`15 = (4−1)(4+1)`）相减即得此式。 -/
theorem fixedpoint_sq_eq_pow : fixedPoint ^ 2 = powers ^ fixedPoint := by
  norm_num [fixedPoint, powers]

/-- **σ⁻¹ = f² − 1**：平方差面（`16 − 1 = 15`）。 -/
theorem sigmaInv_eq_sq_sub_one : fixedPoint ^ 2 - 1 = 15 := by
  norm_num [fixedPoint]

/-- **σ⁻¹ = 2^f − 1**：Mersenne 面（`16 − 1 = 15`）。 -/
theorem sigmaInv_eq_pow_sub_one : powers ^ fixedPoint - 1 = 15 := by
  norm_num [powers, fixedPoint]

/-- 两面相等：`f² − 1 = 2^f − 1`（由 `fixedpoint_sq_eq_pow` 直接来）。 -/
theorem two_faces_agree : fixedPoint ^ 2 - 1 = powers ^ fixedPoint - 1 := by
  rw [fixedpoint_sq_eq_pow]

/-- ★ **平方差分解**：`σ⁻¹ = (f−1)(f+1)`，即 `15 = 3 × 5`。

    这是注入点 2 的真正内容：`3` 不是被选出来的，是 `f − 1`。 -/
theorem sigmaInv_eq_adjacent : (fixedPoint - 1) * (fixedPoint + 1) = 15 := by
  norm_num [fixedPoint]

/-- **两因子之和 = `2f` = `k_max`**：`3 + 5 = 8`。（平方差恒等式的加法面。） -/
theorem adjacent_sum_eq_kmax : (fixedPoint - 1) + (fixedPoint + 1) = 2 * fixedPoint := by
  norm_num [fixedPoint]

/-- `k_max = 2f = 8`。 -/
theorem kmax_eq_two_fixedpoint : 2 * fixedPoint = 8 := by
  norm_num [fixedPoint]

/-- **两因子之差 = `2` = 幂基**：`5 − 3 = 2`。（平方差恒等式的减法面。） -/
theorem adjacent_diff_eq_powers : (fixedPoint + 1) - (fixedPoint - 1) = powers := by
  norm_num [fixedPoint, powers]

/-- ★★ **判别式与 `f` 无关**：对**任意**整数 `f`，`(2f)² − 4(f²−1) = 4`。

    这条说明 `ActiveSilentVieta.vieta_discriminant`（`k_max² − 4σ⁻¹ = 4`）
    **不含关于 `f` 的信息**——它是平方差的恒等式，不是选中 `f = 4` 的判据。
    这同时解释了 `ActiveSilentVieta.lean` L258–261 的登记：
    「判别式为完全平方」不能唯一化 σ⁻¹，唯一性只能在 Mersenne 族内陈述。 -/
theorem discriminant_generic (f : ℤ) : (2 * f) ^ 2 - 4 * (f ^ 2 - 1) = 4 := by
  ring

/-- **`N_active = f − 1`**：`N_active` 由不动点给出，不是独立的选择。

    注意：本定理的**陈述**里以 `fixedPoint − 1` 表达；
    把 `fixedPoint` 换成 4 才出现 3。 -/
theorem active_is_fixedpoint_minus_one : fixedPoint - 1 = 3 := by
  norm_num [fixedPoint]

/-- **`k_max` 与 `σ⁻¹` 同时由 `f` 给出**（打包）。 -/
theorem kmax_and_sigmaInv_from_fixedpoint :
    2 * fixedPoint = 8 ∧ (fixedPoint - 1) * (fixedPoint + 1) = 15 ∧
      fixedPoint - 1 = 3 := by
  refine ⟨?_, ?_, ?_⟩
  · norm_num [fixedPoint]
  · norm_num [fixedPoint]
  · norm_num [fixedPoint]

/-- **`f² = 2^f` 在小范围内的解集是 `{2, 4}`**（另含退化 `0`、`1`）。
    只对 `f < 9` 机检（`decide`），**不作全域断言**。 -/
theorem sq_eq_pow_solutions_small (f : Fin 9) (h : (f : ℕ) ^ 2 = 2 ^ (f : ℕ)) :
    (f : ℕ) = 2 ∨ (f : ℕ) = 4 ∨ (f : ℕ) = 0 ∨ (f : ℕ) = 1 := by
  revert f
  decide

/-- ★ **两个 3 的形式比较**：两条 `4 − 1`，两个 `4` 都写成 `2²`。
    本定理**只记形式事实**，不含任何「同源」断言。 -/
theorem both_threes_are_four_minus_one :
    (fixedPoint - 1 = 3) ∧ (2 ^ 2 = 4) ∧ (fixedPoint = 2 ^ 2) := by
  refine ⟨?_, ?_, ?_⟩
  · norm_num [fixedPoint]
  · norm_num
  · norm_num [fixedPoint]

/-- **相数格数 = `2² = 4`**：两个二值判据的笛卡尔积。

    这里 `2` 是**判据个数**（层 2 的 `HasNontrivialTwoMorphism` 与层 3 的 `AdTraversable2`），
    与 `powers`（幂基）数值相同、来源不同——本批不把二者等同。 -/
theorem phase_cell_count : 2 ^ 2 = 4 := by
  norm_num

/-- **判据个数与格数**：`n = 2 ⇒ 4` 格，减 1 得 3。只记这一条，不对 `n` 作一般断言。 -/
theorem two_conditions_give_four : 2 ^ 2 = 4 ∧ (4 - 1) = 3 := by
  norm_num

end MUFPF.FixedPointOrigin
