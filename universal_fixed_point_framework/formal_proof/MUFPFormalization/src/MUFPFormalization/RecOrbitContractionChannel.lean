import Mathlib.Analysis.SpecificLimits.Basic
import Mathlib.Topology.MetricSpace.Pseudo.Lemmas
import Mathlib.Logic.Function.Iterate
import MUFPFormalization.CompositeDepth
import MUFPFormalization.PublicResidueIdentity
import MUFPFormalization.RecOrbitContraction

/-! # RecOrbitContractionChannel.lean — 收缩层的来源：冻结闭合 σ 乘子通道（S626）

## 动机

`RecOrbitContraction.lean`（S625）把收缩层收口为**条件命题**：
给定 `|step x − a| ≤ c|x − a|` 且 `c < 1`，则迭代按几何律被 `c^n|x − a|` 界住并收敛到 `a`。
该文件同时如实标注：**不证明本框架的 `step` 满足该条件**——「压缩的来源」仍为开口。
本文件查证这一开口：压缩条件在本框架内究竟有无来源，还是只能作为外加假设。

## 本轮查证：来源存在，且在库内已被机检

两处既有结构已经钉住压缩机制，本文件只做**接线**（不重证）：

1. **收缩率**：§10b 的 IFS 收缩因子 `S₄ = e^{-d}` 在机器证明实例 `d = ln 15` 处取值 `1/15`，
   而 `1/15 = σ`——由 `RecOrbitContraction.silent_factor_c2_ln15_eq_sigma` 机检同一。
2. **压缩实现**：G1 冻结闭合的**数值（度量）通道** `CompositeDepth.freezeClosure := fun x => σ * x`
   （S563 C1：每穿越一个静默层引入一个 σ 因子；S568/S569 通道分离：数值通道 `φ_metric = σ` 乘子），
   其级联已机检为 `CompositeDepth.freezeClosure_cascade : freezeClosureIterate n 1 = σ^n`。

即：压缩率（σ）与压缩实现（σ 乘子）都是库内既有对象，故「压缩条件」在本框架内**不是外加参数**。

## 结论（本文件定理）

1. `composite_sigma_eq_public_sigma`：`CompositeDepth.sigma = PublicResidueIdentity.sigma`（同一常数）。
2. `freezeClosure_pos` / `freezeClosure_lt_one`：`0 < σ`、`σ < 1`（压缩率合法）。
3. `freezeClosure_abs_eq`：`|freezeClosure x| = σ|x|`。
4. `freezeClosure_contracts`：`|freezeClosure x − 0| = σ|x − 0|`——压缩条件在该通道上是**等式**。
5. `freezeClosure_iterate_abs_eq`：`|freezeClosure^[n] x| = σ^n|x|`——**等式级**几何律（强于 S625 的 `≤`）。
6. `freezeClosure_iterate_tendsto`：`freezeClosure^[n] x → 0`（把 S625 的收敛定理实例化，非重证）。
7. `freezeClosure_fixed_iff`：`freezeClosure x = x ↔ x = 0`——唯一不动点，即「周期塌成不动点」的
   具体机制在该通道上成立（`σ ≠ 1` 使乘子除零外无不动点）。
8. `freezeClosureIterate_eq_iterate`：库内自定义迭代与标准 `Function.iterate` 一致（两套记号对齐）。
9. `double_step_refutes_contraction`：`step x = 2x` 不满足 `1/15` 条件——条件有判别力，非全体平凡。
10. `sigma_contraction_channel_realized`：存在 step 与不动点使压缩条件（等式级）与收敛同时成立。
11. `contraction_condition_discriminating`：条件既不空（第 10 条）也不全（第 9 条）。

## 边界（如实标注，不越界）

- 本文件钉住的是**数值/度量通道**（`φ_metric` = σ 乘子）。机制通道 `φ_mech = exp(−t·a)`
  （Koopman 半群窗口损失，`MinkowskiBoost.scalar_contraction` 已锚）是另一条，不参与 σ 数值。
- **一般 `step`**（抽象态射，非 ℝ 乘子）是否满足该压缩条件，仍取决于其具体实现——本文件
  **不声称**一般 step 满足，只证明该框架内存在一条已机检的压缩通道，且条件本身有判别力。
- 因此「压缩的来源」由 S625 的「无来源」降为「数值通道有来源（等式级、机检），一般 step 的实现仍开放」。
-/

namespace MUFPF

open Filter
open scoped Topology

/-- 框架常数 σ 在 `CompositeDepth` 与 `PublicResidueIdentity` 两处定义是同一常数。 -/
theorem composite_sigma_eq_public_sigma :
    MUFPF.CompositeDepth.sigma = MUFPF.PublicResidueIdentity.sigma := by
  unfold MUFPF.CompositeDepth.sigma MUFPF.PublicResidueIdentity.sigma
  norm_num

/-- σ 为正（压缩率合法）。 -/
theorem freezeClosure_pos : (0 : ℝ) < MUFPF.CompositeDepth.sigma := by
  unfold MUFPF.CompositeDepth.sigma
  norm_num

/-- σ 小于 1（压缩率合法）。 -/
theorem freezeClosure_lt_one : MUFPF.CompositeDepth.sigma < 1 := by
  unfold MUFPF.CompositeDepth.sigma
  norm_num

/-- 冻结闭合（σ 乘子）的幅值作用：`|freezeClosure x| = σ|x|`。 -/
theorem freezeClosure_abs_eq (x : ℝ) :
    |MUFPF.CompositeDepth.freezeClosure x| = MUFPF.CompositeDepth.sigma * |x| := by
  simp [MUFPF.CompositeDepth.freezeClosure, abs_mul, abs_of_pos freezeClosure_pos]

/-- 冻结闭合在不动点 0 处**等式级**满足 S625 的压缩条件形态。 -/
theorem freezeClosure_contracts (x : ℝ) :
    |MUFPF.CompositeDepth.freezeClosure x - 0| = MUFPF.CompositeDepth.sigma * |x - 0| := by
  simpa using freezeClosure_abs_eq x

/-- 迭代的等式级几何律：`|freezeClosure^[n] x| = σ^n|x|`（强于 S625 的 `≤`）。 -/
theorem freezeClosure_iterate_abs_eq (x : ℝ) (n : ℕ) :
    |(MUFPF.CompositeDepth.freezeClosure)^[n] x| = MUFPF.CompositeDepth.sigma ^ n * |x| := by
  induction n with
  | zero => simp
  | succ k ih =>
      rw [Function.iterate_succ_apply', freezeClosure_abs_eq, ih, pow_succ]
      ring

/-- 冻结闭合迭代收敛到 0（实例化 S625 的 `contraction_iterate_tendsto`）。 -/
theorem freezeClosure_iterate_tendsto (x : ℝ) :
    Tendsto (fun n : ℕ => (MUFPF.CompositeDepth.freezeClosure)^[n] x) atTop (𝓝 0) := by
  refine contraction_iterate_tendsto (step := MUFPF.CompositeDepth.freezeClosure)
    (a := 0) (c := MUFPF.CompositeDepth.sigma) (le_of_lt freezeClosure_pos) freezeClosure_lt_one
    (fun y => le_of_eq (freezeClosure_contracts y)) x

/-- 冻结闭合的唯一不动点是 0（`σ ≠ 1`）——「周期塌成不动点」的具体机制。 -/
theorem freezeClosure_fixed_iff (x : ℝ) :
    MUFPF.CompositeDepth.freezeClosure x = x ↔ x = 0 := by
  have hσ : MUFPF.CompositeDepth.sigma ≠ 1 := by
    unfold MUFPF.CompositeDepth.sigma
    norm_num
  constructor
  · intro h
    have h2 : MUFPF.CompositeDepth.sigma * x = x := by
      simpa [MUFPF.CompositeDepth.freezeClosure] using h
    have h' : (MUFPF.CompositeDepth.sigma - 1) * x = 0 := by nlinarith
    have hne : MUFPF.CompositeDepth.sigma - 1 ≠ 0 := sub_ne_zero.mpr hσ
    exact (mul_eq_zero.mp h').resolve_left hne
  · intro h
    subst h
    simp [MUFPF.CompositeDepth.freezeClosure]

/-- 库内自定义迭代（`freezeClosureIterate`）与标准 `Function.iterate` 一致。 -/
theorem freezeClosureIterate_eq_iterate (n : ℕ) (x : ℝ) :
    MUFPF.CompositeDepth.freezeClosureIterate n x = (MUFPF.CompositeDepth.freezeClosure)^[n] x := by
  induction n generalizing x with
  | zero => simp [MUFPF.CompositeDepth.freezeClosureIterate]
  | succ k ih =>
      rw [MUFPF.CompositeDepth.freezeClosureIterate]
      rw [ih (MUFPF.CompositeDepth.freezeClosure x)]
      rw [Function.iterate_succ_apply MUFPF.CompositeDepth.freezeClosure k x]

/-- `step x = 2x` 不满足 σ 压缩条件——条件有判别力。 -/
theorem double_step_refutes_contraction :
    ¬ (∀ x : ℝ, |(fun y : ℝ => 2 * y) x - 0| ≤ (1 / 15 : ℝ) * |x - 0|) := by
  intro h
  have h1 := h 1
  norm_num at h1

/-- 压缩通道实现：存在 step 与不动点，使压缩条件（等式级）与收敛同时成立。 -/
theorem sigma_contraction_channel_realized :
    ∃ (step : ℝ → ℝ) (a : ℝ),
      (∀ x, |step x - a| = (1 / 15 : ℝ) * |x - a|) ∧
      Tendsto (fun n : ℕ => step^[n] (1 : ℝ)) atTop (𝓝 a) := by
  refine ⟨MUFPF.CompositeDepth.freezeClosure, 0, ?_, ?_⟩
  · intro x
    rw [freezeClosure_contracts, MUFPF.CompositeDepth.sigma]
  · exact freezeClosure_iterate_tendsto 1

/-- 压缩条件既不空（存在实现）也不全（存在反例）——有判别力。 -/
theorem contraction_condition_discriminating :
    (∃ (step : ℝ → ℝ) (a : ℝ), ∀ x, |step x - a| ≤ MUFPF.CompositeDepth.sigma * |x - a|) ∧
      ¬ (∀ (step : ℝ → ℝ) (a : ℝ) (x : ℝ),
        |step x - a| ≤ MUFPF.CompositeDepth.sigma * |x - a|) := by
  refine ⟨⟨MUFPF.CompositeDepth.freezeClosure, 0, fun x => le_of_eq (freezeClosure_contracts x)⟩, ?_⟩
  intro h
  have h1 := h (fun y : ℝ => 2 * y) 0 1
  norm_num [MUFPF.CompositeDepth.sigma] at h1

end MUFPF
