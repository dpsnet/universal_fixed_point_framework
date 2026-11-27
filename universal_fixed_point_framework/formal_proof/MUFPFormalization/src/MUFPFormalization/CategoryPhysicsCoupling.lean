/-
  CategoryPhysicsCoupling.lean — 范畴层常数进入物理侧陈述的最小共享符号模块
  ============================================================================

## 为什么单独开一个模块

`notes/inverse_constraint_audit.md` §10–§11 的 R-b 依赖闭包审计给出一个二分：

| 定理类型 | 是否含范畴层常数 | 逆向约束力 |
|---|---|---|
| 能不依赖常数独立机检（C2 / C3 / C4） | 不含 | 零：删它不变 |
| 依赖常数机检（黑洞 / Kerr / 量子引力等） | 含，且以之为**假设** | 被污染：用前提证前提 |

二分穷尽 ⟹ 在既有依赖图下「从物理层逆向推出范畴层」结构性不可能。结论里
给出的唯一出路是：**把范畴层常数写进物理侧定理的陈述**（而非注释）。

本模块就是这条出路的第一块砖，规模刻意压到最小，只回答一个是非题：
「范畴阶 `catOrder` 能不能作为参数真出现在一条物理量的定义与定理里，并且
零 sorry 地证出来？」——能，则逆向有了第一条缝；不能，则「两侧不可桥接」
是结构事实而非表达问题。

## 共享符号的落点：4 步时间轴偏转窗口

物理侧的原像取自 `notes/04_lorentz_gravity/mass_time_deflection_intuition.md`：

    φ_n = n · ln 2,   θ_n = arcsin(tanh(n ln 2)),   K_n = m (cosh(n ln 2) − 1)

第 4 步（n = 4）给出 K₄ = 225 m / 32，且 4 步窗口的 16 个态被读作 Cl(1,3)
的 16 维表示，非标量部分正是 15 个「静默层」。

这段物理叙述里的「4」目前是**外生输入**；本模块把它换成 `catOrder`：

    windowSteps := catOrder

于是 `catOrder` 不再只是范畴层的一个计数，而作为**窗口长度**进入
`deflectionStep4Coeff` 的定义，并作为指数进入 `2 ^ windowSteps` 的计数。
证明项里因此必然出现 `catOrder`（`rw [catOrder]` 无法被删掉），
这就是 R-b 二分里「含常数」的那一半，而不是注释里的提及。

## 证到了什么（性质分类要分清）

1. **数值合流**：`B = catOrder ^ 2 − 1 = 2 ^ catOrder − 1 = 15`。三条
   独立定义（层对计数 / 范畴阶 / 幂链）在 Lean 里第一次被同一条定理串起来。
   但这只是**数值合流**，不构成「B 由 catOrder 导出」——`B` 的定义仍走
   `ActiveLayers.card * N_total`，其中 3 与 5 是两个独立的读法。
   §2 用 `layer_card_eq_nActive` / `layer_total_eq_nTotal` 把这两条读法
   接到 `catOrder − 1` / `catOrder + 1` 上，但这仍是「两个定义恰好相等」。
2. **`n² = 2^n` 在 n = 4 的锁定**：`catOrder ^ 2 = 2 ^ catOrder`。这是
   框架内被反复引用的一元生成方程，此处第一次以 `catOrder` 为主角机检。
3. **物理量的实数等式**：`deflectionStep4Coeff = B ^ 2 / 32 = 225 / 32`。
   左边是物理侧的能量系数（含 `catOrder`），右边是范畴侧的分支数 `B`。
   这是本模块唯一的「跨层定理」：陈述里同时出现两个不同层的常数。
4. **勾股结构**：4 步窗口的偏转角给出 255-32-257 三元组，
   即 `(2^(2n) − 1, 2^(n+1), 2^(2n) + 1)`，在 n = 4 时成立。

## 诚实边界

- **没有证明「物理必须用 catOrder」**。本模块证明的是「一旦把窗口长度取为
  `catOrder`，全部相关等式零 sorry 成立」。窗口长度为什么是 4（从而等于
  `catOrder`）仍是框架公设，不是本模块的结论。
- **数值合流 ≠ 结构同一**。`B = catOrder ^ 2 − 1` 是三条路径的数值相遇，
  与第 63 批登记的「四口径 15 / 12 / 9 / 6」并不冲突：本模块只钉住了
  `N_active × N_total` 这一口径等于 `n² − 1`。
- **反过来仍不可用**。「B = 15」不能用来反推 `catOrder = 4` 之外的信息：
  本模块让常数进了陈述，但陈述的**方向仍是范畴 → 物理**。逆向要走通，
  还需要一条「给定物理读数 ⟹ 唯一范畴参数」的定理，本模块没有提供。
- 全部结论均为 `decide` / `norm_num` / `rw` 级别，没有引入新公设、
  没有 `sorry`、没有 `axiom`。
-/

import Mathlib.Analysis.Complex.Trigonometric
import Mathlib.Tactic
import MUFPFormalization.BranchCounting
import MUFPFormalization.ActiveFromCategoryOrder

open MUFPF.BranchCounting
open MUFPF.CategoryOrder

namespace MUFPF.CategoryPhysicsCoupling

/-! =========================================================
    §1 共享符号：把窗口长度取为范畴阶
   =========================================================

    `windowSteps` 是本模块的枢纽：物理侧只认「窗口长度」这个数，
    而这个数在此**定义为** `catOrder`。此后所有物理量的定义都经它
    携带范畴层常数。
-/

/-- 时间轴偏转窗口的步数 = 范畴阶 `catOrder`。

    物理原像：`notes/04_lorentz_gravity/mass_time_deflection_intuition.md`
    的 4 步窗口（`φ_n = n ln 2`，n = 1..4）。此处把 4 换成 `catOrder`，
    `catOrder` 因之进入下面所有物理侧陈述。 -/
def windowSteps : ℕ := catOrder

/-- `windowSteps = 4`。 -/
theorem windowSteps_eq_four : windowSteps = 4 := by
  norm_num [windowSteps, MUFPF.CategoryOrder.catOrder]

/-! =========================================================
    §2 层计数与范畴阶的对接
   =========================================================

    `BranchCounting` 用 `ActiveLayers.card = 3` 与 `N_total = 5` 得到 `B`；
    `CategoryOrder` 用 `catOrder − 1 = 3` 与 `catOrder + 1 = 5`。
    本节证两条读法数值相等——**这是数值对接，不是导出**。
-/

/-- 主动层计数等于 `catOrder − 1`（`nActive` 的定义式）。 -/
theorem layer_card_eq_nActive :
    (ActiveLayers : Finset LayerIndex).card = nActive := by
  rw [active_layers_count, nActive_eq_three]

/-- 总层计数等于 `catOrder + 1`（`nTotal` 的定义式）。 -/
theorem layer_total_eq_nTotal : N_total = nTotal := by
  norm_num [MUFPF.BranchCounting.N_total, MUFPF.CategoryOrder.nTotal,
    MUFPF.CategoryOrder.catOrder]

/-- **`B` 由范畴阶的 ±1 邻域给出**：`B = (n − 1)(n + 1) = n² − 1`。

    注意方向：本定理证明的是「`B` 的定义值恰好等于 `catOrder` 的表达式」，
    不是「`B` 从 `catOrder` 推出」。 -/
theorem B_eq_catOrder_sq_sub_one : B = catOrder ^ 2 - 1 := by
  unfold MUFPF.BranchCounting.B MUFPF.BranchCounting.N_total
  rw [active_layers_count]
  norm_num [MUFPF.CategoryOrder.catOrder]

/-! =========================================================
    §3 窗口态数与静默层数（物理 16 态 ⟷ 范畴 15 分支）
   =========================================================
-/

/-- 4 步窗口的态数 `2 ^ windowSteps = 16`（Cl(1,3) 的 16 维表示）。 -/
theorem window_states : 2 ^ windowSteps = 16 := by
  norm_num [windowSteps, MUFPF.CategoryOrder.catOrder]

/-- 非标量静默层数 `2 ^ windowSteps − 1 = B`（15）。

    这是物理侧「16 态去掉标量态」与范畴侧「分支数」的数值合流。 -/
theorem silent_layers_eq_B : 2 ^ windowSteps - 1 = B := by
  rw [window_states, MUFPF.BranchCounting.B_eq_15]

/-- **一元生成方程在 n = 4 的锁定**：`catOrder ^ 2 = 2 ^ catOrder`。

    `n² = 2^n` 的整数解为 n = 2 与 n = 4；框架取 n = 4。此处第一次以
    `catOrder` 为主角机检该等式。 -/
theorem order_power_lock : windowSteps ^ 2 = 2 ^ windowSteps := by
  norm_num [windowSteps, MUFPF.CategoryOrder.catOrder]

/-- 4 步窗口的偏转角给出 255-32-257 勾股三元组：

    `(2^(2n) − 1)² + (2^(n+1))² = (2^(2n) + 1)²`，n = 4 时即
    `255² + 32² = 257²`（`tan θ₄ = 255/32`，`cos θ₄ = 32/257`）。 -/
theorem deflection_triple :
    (2 ^ (2 * windowSteps) - 1) ^ 2 + (2 ^ (windowSteps + 1)) ^ 2
      = (2 ^ (2 * windowSteps) + 1) ^ 2 := by
  rw [windowSteps_eq_four]
  norm_num

/-! =========================================================
    §4 跨层定理：物理量 = 范畴常数
   =========================================================

    `deflectionStep4Coeff` 是物理侧的**无量纲能量系数** `K₄/m`：
        定义 = cosh(windowSteps · ln 2) − 1
    它的定义表达式里含 `catOrder`；下面的定理把它等于 `B ^ 2 / 32`，
    陈述里含范畴层的 `B`。这是本模块唯一的跨层等式。
-/

/-- 4 步偏转窗口的能量系数 `K₄ / m = cosh(4 ln 2) − 1`。

    `windowSteps` 携带 `catOrder`，故此定义**不是**注释式提及，
    而是把范畴层常数写进物理量的定义体。 -/
noncomputable def deflectionStep4Coeff : ℝ :=
  Real.cosh ((windowSteps : ℝ) * Real.log 2) - 1

/-- `exp(windowSteps · ln 2) = 2 ^ windowSteps`。 -/
theorem exp_window : Real.exp ((windowSteps : ℝ) * Real.log 2) = (2 : ℝ) ^ windowSteps := by
  rw [Real.exp_nat_mul, Real.exp_log (by norm_num : (0 : ℝ) < 2)]

/-- `cosh(windowSteps · ln 2) = (2^n + 2^(−n)) / 2`。 -/
theorem cosh_window :
    Real.cosh ((windowSteps : ℝ) * Real.log 2)
      = ((2 : ℝ) ^ windowSteps + ((2 : ℝ) ^ windowSteps)⁻¹) / 2 := by
  rw [Real.cosh_eq, exp_window]
  have hneg : Real.exp (-((windowSteps : ℝ) * Real.log 2))
      = ((2 : ℝ) ^ windowSteps)⁻¹ := by
    rw [Real.exp_neg, exp_window]
  rw [hneg]

/-- **跨层定理**：`K₄ / m = B² / 32`。

    物理侧：4 步窗口的能量系数（`225/32 ≈ 7.03`，见
    `mass_time_deflection_intuition.md` §7.7）；
    范畴侧：分支数 `B = 15`。
    两边由同一条 `catOrder` 串起，证明项必须同时展开 `windowSteps` 与 `B`。 -/
theorem deflectionStep4Coeff_eq_B_sq :
    deflectionStep4Coeff = (B : ℝ) ^ 2 / 32 := by
  unfold deflectionStep4Coeff
  rw [cosh_window, windowSteps_eq_four, MUFPF.BranchCounting.B_eq_15]
  norm_num

/-- 跨层定理的有理数形式：`K₄ / m = 225 / 32`。 -/
theorem deflectionStep4Coeff_eq_rational : deflectionStep4Coeff = 225 / 32 := by
  rw [deflectionStep4Coeff_eq_B_sq, MUFPF.BranchCounting.B_eq_15]
  norm_num

/-- 与本模块第 3 节一致：`K₄ / m = (2^n − 1)² / 2^(n+1)`，n = 4 时 `225/32`。 -/
theorem deflectionStep4Coeff_eq_silent_sq :
    deflectionStep4Coeff = ((2 : ℝ) ^ windowSteps - 1) ^ 2 / ((2 : ℝ) ^ (windowSteps + 1)) := by
  rw [deflectionStep4Coeff_eq_rational, windowSteps_eq_four]
  norm_num

/-! =========================================================
    §5 自检清单（本模块对 R-b 二分回答了什么）
   =========================================================
-/

/-- 本模块的机检收束：`catOrder` 出现在物理量的定义体（`windowSteps`），
    且两条跨层等式零 sorry 成立。

    这是「共享符号」实验的通过判据；逆向方向的唯一性定理仍缺。 -/
theorem coupling_witness :
    windowSteps = catOrder ∧
    deflectionStep4Coeff = (B : ℝ) ^ 2 / 32 ∧
    2 ^ windowSteps - 1 = B :=
  ⟨rfl, deflectionStep4Coeff_eq_B_sq, silent_layers_eq_B⟩

end MUFPF.CategoryPhysicsCoupling
