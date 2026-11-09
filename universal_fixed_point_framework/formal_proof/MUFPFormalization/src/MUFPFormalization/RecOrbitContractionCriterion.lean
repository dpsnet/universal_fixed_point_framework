import Mathlib.Analysis.SpecificLimits.Basic
import Mathlib.Topology.MetricSpace.Pseudo.Lemmas
import Mathlib.Logic.Function.Iterate
import MUFPFormalization.CompositeDepth
import MUFPFormalization.RecOrbitContraction

/-!
# 收缩判据：线性实现下的充要条件（S627——2026-11-10）

## 动机：把一条「开口」改成「已判定的分类命题」

S624 的 `step` 是 `step : α → α`，即**任意自映射**——库内不存在「本框架的 `step`」
这一具体对象。S626 已机检 `step x = 2x` 不满足压缩条件
（`double_step_refutes_contraction`）。两件事合起来的含义不是「答案未知」，而是：

> 「一般 `step` 是否按 σ 收缩」在**抽象层面为假**（其为任意映射，反例已机检），
> 故这句话在抽象层面没有真值，只能对**具体实现**逐个判定。

本文件给出该判定在**乘子型（线性）实现**下的**充要判据**：

    `k` 满足 `|k · x| ≤ σ|x|`（∀ x） ⟺ `|k| ≤ σ` ⟺ `k ∈ [-σ, σ]`。

于是「本框架哪条通道通过判定」从开放式追问变成一次**区间归属检查**；
数值通道 `CompositeDepth.freezeClosure`（`k = σ`）恰好落在区间右端点。

## 判据的覆盖范围（边界，如实标注）

- **覆盖**：乘子型 step，即 `x ↦ k · x`。含数值（度量）通道 `freezeClosure`（`k = σ`）。
- **不覆盖**：非乘子型 step（仿射带平移 `x ↦ k x + b`、分段、非线性）——本文件不给
  一般判据。若框架内出现此类实现，须另立判据；这是本轮缩小后**仍然开放**的部分。
- 判据是**紧的**：`k` 只要超过 σ 千分之一（`1001/15000`），逐点条件即失败
  （`%TEMP%\pre_s627.txt` 数值预检，Fraction 精确算术，0 mismatch）。
- 本文件**不主张**「框架内不存在第三条通道」——通道完备性未证，不作断言。

## 结论（十条定理，零 sorry）

1. `linear_step_contracts_iff`：乘子型收缩 ⟺ `|k| ≤ σ`（充要，非充分）。
2. `contracting_multipliers_eq_Icc`：收缩乘子族恰是闭区间 `[-σ, σ]`。
3. `sigma_mem_contracting_multipliers`：σ 通过判定。
4. `neg_sigma_mem_contracting_multipliers`：`-σ` 亦通过（区间对称）。
5. `two_not_mem_contracting_multipliers`：`2` 不通过。
6. `two_fails_criterion`：`x ↦ 2x` 不满足判据（与 S626 反例一致的乘子版）。
7. `linear_step_iterate_bound`：任一通过判据的 `k`，n 步幅值 ≤ `σ^n|x|`（统一速率界）。
8. `linear_step_converges`：任一通过判据的 `k`，迭代收敛到 0。
9. `linear_step_criterion_and_rate`：7、8 合并为一条可引用结论。
10. `freezeClosure_multiplier_at_endpoint`：数值通道乘子恰为 σ（区间右端点）。

零 sorry 政策：本文件不含 sorry。
-/

namespace MUFPF

open Filter
open scoped Topology

/-- **判据主定理**：乘子 `k` 的线性 step 满足压缩条件 ⟺ `|k| ≤ σ`。

    正向只需取 `x = 1`（`|k · 1| = |k| ≤ σ`）；反向用 `|k x| = |k||x|` 与
    `|k| ≤ σ` 逐点相乘。故这是**充要**判据，不是充分条件：任何超过 σ 的乘子
    都必然在某处违约。 -/
theorem linear_step_contracts_iff (k : ℝ) :
    (∀ x : ℝ, |k * x| ≤ (1 / 15 : ℝ) * |x|) ↔ |k| ≤ 1 / 15 := by
  constructor
  · intro h
    have h1 : |k * 1| ≤ (1 / 15 : ℝ) * |1| := h 1
    simpa using h1
  · intro hk x
    rw [abs_mul]
    exact mul_le_mul_of_nonneg_right hk (abs_nonneg x)

/-- 收缩乘子族恰是闭区间 `[-σ, σ]`：判据的集合版。 -/
theorem contracting_multipliers_eq_Icc (k : ℝ) :
    (∀ x : ℝ, |k * x| ≤ (1 / 15 : ℝ) * |x|) ↔
      k ∈ Set.Icc (-(1 / 15 : ℝ)) (1 / 15 : ℝ) := by
  rw [linear_step_contracts_iff k, Set.mem_Icc]
  exact ⟨fun h => abs_le.1 h, fun h => abs_le.2 h⟩

/-- σ 本身通过判据（族非空）。 -/
theorem sigma_mem_contracting_multipliers :
    (1 / 15 : ℝ) ∈ Set.Icc (-(1 / 15 : ℝ)) (1 / 15 : ℝ) := by
  rw [Set.mem_Icc]
  constructor <;> norm_num

/-- 负向乘子 `-σ` 亦通过判据（族关于原点对称，可逆冻结同样收缩）。 -/
theorem neg_sigma_mem_contracting_multipliers :
    (-(1 / 15 : ℝ)) ∈ Set.Icc (-(1 / 15 : ℝ)) (1 / 15 : ℝ) := by
  rw [Set.mem_Icc]
  constructor <;> norm_num

/-- `2` 不通过判据（族非全）。 -/
theorem two_not_mem_contracting_multipliers :
    (2 : ℝ) ∉ Set.Icc (-(1 / 15 : ℝ)) (1 / 15 : ℝ) := by
  rw [Set.mem_Icc]
  intro h
  linarith [h.2]

/-- `x ↦ 2 x` 不满足压缩判据（S626 反例 `double_step_refutes_contraction` 的乘子版）。 -/
theorem two_fails_criterion :
    ¬ (∀ x : ℝ, |(2 : ℝ) * x| ≤ (1 / 15 : ℝ) * |x|) := by
  intro h
  have h1 : |(2 : ℝ) * 1| ≤ (1 / 15 : ℝ) * |1| := h 1
  norm_num at h1

/-- **统一速率界**：任一通过判据的乘子 `k`，其迭代幅值被 σ^n|x| 界住。

    注意界只依赖判据（`|k| ≤ σ`），与 `k` 的具体取值无关——故框架内所有通过判定的
    数值通道共享同一速率上界 σ^n。 -/
theorem linear_step_iterate_bound {k : ℝ} (hk : |k| ≤ 1 / 15) (x : ℝ) (n : ℕ) :
    |(fun y : ℝ => k * y)^[n] x| ≤ (1 / 15 : ℝ) ^ n * |x| := by
  have hstep : ∀ y : ℝ, |(fun y : ℝ => k * y) y - 0| ≤ (1 / 15 : ℝ) * |y - 0| := by
    intro y
    simp only [sub_zero, abs_mul]
    exact mul_le_mul_of_nonneg_right hk (abs_nonneg y)
  have := contraction_iterate_bound (step := fun y : ℝ => k * y) (a := 0) (c := 1 / 15)
    (by norm_num) hstep x n
  simpa using this

/-- 任一通过判据的乘子 `k`，迭代收敛到唯一不动点 0。 -/
theorem linear_step_converges {k : ℝ} (hk : |k| ≤ 1 / 15) (x : ℝ) :
    Tendsto (fun n : ℕ => (fun y : ℝ => k * y)^[n] x) atTop (𝓝 0) := by
  refine contraction_iterate_tendsto (step := fun y : ℝ => k * y) (a := 0)
    (c := 1 / 15) (by norm_num) (by norm_num) ?_ x
  intro y
  simp only [sub_zero, abs_mul]
  exact mul_le_mul_of_nonneg_right hk (abs_nonneg y)

/-- 判据通过 ⟹ 「速率 + 收敛」同时成立：一条可直接引用的合并结论。 -/
theorem linear_step_criterion_and_rate {k : ℝ} (hk : |k| ≤ 1 / 15) (x : ℝ) :
    (∀ n : ℕ, |(fun y : ℝ => k * y)^[n] x| ≤ (1 / 15 : ℝ) ^ n * |x|) ∧
      Tendsto (fun n : ℕ => (fun y : ℝ => k * y)^[n] x) atTop (𝓝 0) :=
  ⟨fun n => linear_step_iterate_bound hk x n, linear_step_converges hk x⟩

/-- **与数值通道对齐**：`CompositeDepth.freezeClosure` 的乘子恰为 σ，
    即判据区间的右端点——框架的数值通道取的是「可通过判定的最大乘子」（收缩最慢者），
    而不是某个更小的人为取值。 -/
theorem freezeClosure_multiplier_at_endpoint :
    CompositeDepth.freezeClosure 1 = (1 / 15 : ℝ) ∧
      (1 / 15 : ℝ) ∈ Set.Icc (-(1 / 15 : ℝ)) (1 / 15 : ℝ) := by
  refine ⟨?_, sigma_mem_contracting_multipliers⟩
  unfold CompositeDepth.freezeClosure CompositeDepth.sigma
  norm_num

end MUFPF
