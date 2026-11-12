/-
Copyright (c) 2026 MUFPF Project. All rights reserved.

# 第 44 批：递归深度（指向时间）与周期（闭环）—— 两类量不可互换

## 用户判据（本批基线）

用户第 44 批原话：**「3 一定不是递归的某种周期，递归是指向时间的」**。

这句话否掉了第 43 批所选的对象类别，而不是它的数值。第 43 批把「阶数」还原为 `step` 的**迭代周期**并证伪（50069 例，周期 3 占 16.76%）——证伪成立，但**对象选错了**：

- **周期**：`step^[p] = id` —— 回到原点，时间可回返（闭环，与方向无关）。
- **递归深度**：`step^[d] = step^[d+1]` —— 到达不动点、不再变化，时间单向停住。

⇒ 递归之「递归」在**时间的单向性**上，不在状态空间的循环长度上。所以「3」若真是递归的量，它必须是**深度**，不可能是**周期**。

## 实测：库里的「时间」三处都不对

| 位置 | 时间形态 | 性质 |
|---|---|---|
| `RecObj.step`（`RecCategory.lean` L26） | `T → T` | **无时间参数** |
| `DynSys.Φ`（`DynSys.lean` L54–56） | `X → X` | **无时间参数**（doc 却称 Evolution rule） |
| `OperatorTheory.koopmanSemigroup`（L52–54） | `exp((-t) • A) * exp((-s) • A) = exp((-(t+s)) • A)`，`t s : ℂ` | 有时间，但 **`ℂ` 可逆** ⇒ 是**群**不是半群 |

而 `paper1` L86–91 要求 `T_R ⊆ ℝ≥0` 是**时间半群**（只向前）。`DynSys.lean` L109 的 `RecObjToDynSys`（`Φ := R.step`）恰好证明库里自己把 `RecObj` 当作「单步映射」。

⇒ **「数学 → Lean 结构」这一步丢掉的不是「时间」这个词，而是时间的两个要件：时间参数本身（`RecObj`/`DynSys` 缺）与单向性（`OperatorTheory` 用 `ℂ` 丢）。**

## 本模块做两件事

1. **把「深度」造成可用对象**：`Fin 4` 上的单向链 `x ↦ min(x+1, 3)`。任意起点 ≤ 3 步到顶，恰需 3 步（起点 0）——**这就是 `f − 1 = 4 − 1 = 3` 的结构语义**，不是「数 3 个构造子」。
2. **机检「周期 ≠ 深度」**：周期对象在第 3 步**折返到原点**（`f^[3] = id ≠ f^[4] = f`），链对象在第 3 步**停住**（`f^[3] = f^[4]`）。同一个数字 3，一个是闭环，一个是时间终点。

## 诚实边界

- **本模块不证明 `f = 4`**。`Fin 4` 是选定的状态空间；`depth = 3` 只是 `4` 的推论。`f = 4` 的必然性仍未证（`f² = 2^f` 的整数解集 `{2,4}`，`f > 8` 未机检）。
- **本模块不证明「深度 = `N_active`」**。它给出的是「4 状态单向链的最长深度 = 3」这一结构事实，`N_active := 3` 的定义（`DHStructuralAnalysis` L99）未改。
- **「周期映射永不收敛」只机检到「第 3 步处不是停住」**（`cyc3^[3] ≠ cyc3^[4]`）。对任意 `d` 的一般论证需要「稳定后保持 + 周期整除」两条引理，未做。
- **深度只对收敛映射有定义**；一般有限映射（含循环）没有深度。
- 本模块**不修改** `RecObj` / `SpObj` / `DynSys` / `OperatorTheory`。
-/

import Mathlib.Tactic
import MUFPFormalization.RecCategory
import MUFPFormalization.RecOrderExtraction

namespace MUFPF.RecTime

open MUFPF

/-! ## 一、单向链：`Fin 4` 上「持续推进、到顶停住」 -/

/-- 4 状态单向链：`x ↦ min (x+1) 3`。到 `3` 后停住（不动点），不可回退。 -/
def chain4 : RecObj where
  T := Fin 4
  fin := inferInstance
  dec := inferInstance
  step := fun x => ⟨min (x.val + 1) 3, by omega⟩

/-- **任意起点 3 步内到顶**：`step^[3] x` 的值为 3。 -/
theorem chain4_any_start_reaches_top (x : Fin 4) : ((chain4.step)^[3] x).val = 3 := by
  revert x
  decide

/-- **3 步后稳定**：`step^[3] = step^[4]`，时间在这里停住（单向、不再变化）。 -/
theorem chain4_stable_at_three : (chain4.step)^[3] = (chain4.step)^[4] := by
  funext x
  revert x
  decide

/-- **恰好需要 3 步，不是 2 步**：`step^[2] ≠ step^[3]`（起点 0 在 2 步后仍在 2）。 -/
theorem chain4_not_stable_at_two : (chain4.step)^[2] ≠ (chain4.step)^[3] := by
  intro h
  have h0 := congrFun h (⟨0, by omega⟩ : Fin 4)
  revert h0
  decide

/-- **深度恰为 3**：最小稳定步数是 3。 -/
theorem chain4_depth_is_three :
    (chain4.step)^[3] = (chain4.step)^[4] ∧ (chain4.step)^[2] ≠ (chain4.step)^[3] :=
  ⟨chain4_stable_at_three, chain4_not_stable_at_two⟩

/-- **深度 = `4 − 1`**：`f − 1` 的结构语义是「`f` 状态单向链的最长深度」，不是算术巧合。 -/
theorem depth_eq_four_sub_one : (3 : ℕ) = 4 - 1 := by norm_num

/-! ## 二、周期对象：第 3 步折返，不是停住

第 43 批已在 `RecObj` 层机检 `cyclic3_period_is_three`（`cyclic3.step^[3] = id`）。
本节在**纯函数层**（`ZMod 3 → ZMod 3`，不经 `RecObj` 包装）给出同一映射的折返行为，
因为包装后的 `cyclic3.T` 不按定义归约（已知类型类合成坑），在包装类型上做逐点计算会失败。 -/

/-- `ZMod 3` 上的加一循环（`cyclic3.step` 的底层函数，同一映射的纯函数形态）。 -/
def cyc3 : ZMod 3 → ZMod 3 := fun x => x + 1

/-- 周期对象第 3 步回到原点：`cyc3^[3] = id`。 -/
theorem cyc3_iterate_three : cyc3^[3] = id := by
  funext x
  revert x
  decide

/-- 周期对象第 4 步回到自身：`cyc3^[4] = cyc3`（因为 `cyc3^[3] = id`）。 -/
theorem cyc3_iterate_four : cyc3^[4] = cyc3 := by
  funext x
  revert x
  decide

/-- 周期对象非恒等：`cyc3 ≠ id`。 -/
theorem cyc3_ne_id : cyc3 ≠ id := by
  intro h
  have h0 : cyc3 (0 : ZMod 3) = id (0 : ZMod 3) := congrFun h 0
  simp only [cyc3, id_eq] at h0
  revert h0
  decide

/-- **第 3 步是折返，不是停住**：`cyc3^[3] ≠ cyc3^[4]`。
    `cyc3^[3] = id` 而 `cyc3^[4] = cyc3 ≠ id` ⇒ 它在第 3 步回到原点而不是停下来。
    这正是「周期是闭环、可回返」的数学内容。 -/
theorem cyc3_folds_back_not_stops : cyc3^[3] ≠ cyc3^[4] := by
  rw [cyc3_iterate_three, cyc3_iterate_four]
  intro h
  exact cyc3_ne_id h.symm

/-! ## 三、机检裁决：同一个 3，两种相反的时间角色 -/

/-- **两个对象，同一个数字 3，两种相反的时间行为**：
    - 周期对象：`cyc3^[3] = id`（回到原点），因此 `cyc3^[3] ≠ cyc3^[4]`（**折返**，时间可回返）；
    - 链对象：`chain4.step^[3] = chain4.step^[4]`（不再变化），因此 `^[2] ≠ ^[3]`（**停住**，时间单向终止）。
    ⇒ 若「3」来自周期，它是闭环长度；若来自深度，它是单向终点。两者不可互换。
    ⇒ 用户判断「3 一定不是递归的某种周期」在结构上成立：递归要的是后者。 -/
theorem period_and_depth_are_different :
    -- 周期对象：3 步回到原点（折返）
    cyc3^[3] = id ∧
    cyc3^[3] ≠ cyc3^[4] ∧
    -- 链对象：3 步停住（终点），且 2 步未停
    ((chain4.step)^[3] = (chain4.step)^[4] ∧ (chain4.step)^[2] ≠ (chain4.step)^[3]) :=
  ⟨cyc3_iterate_three,
   ⟨cyc3_folds_back_not_stops, chain4_depth_is_three⟩⟩

/-! ## 四、登记：时间义务的缺失位置（不在本模块修复） -/

/-- **登记位**：时间义务三处均缺。
    `RecObj.step : T → T` 与 `DynSys.Φ : X → X` 无时间参数；
    `OperatorTheory` 的 `t : ℂ` 可逆，构成群不是半群。
    修复方向（按「对理论的影响」排序）：给 `Φ` 恢复时间参数与半群律 `Φ(t+s) = Φ(t)∘Φ(s)`（`t ≥ 0`），
    使「深度」成为**时间刻度数**而非状态空间的最长链。 -/
theorem time_obligation_missing : True := trivial

end MUFPF.RecTime
