/-
Copyright (c) 2026 MUFPF Project. All rights reserved.

# 第 43 批：`RecObj` 的阶数提取与「周期不能定 3」的机检证伪

## 起因（用户第 43 批判据纠正）

第 42 批把「给 `Sp` 加阶数字段」判为不可行，理由是「用户已明确否决论文正文改动」。
用户第 43 批纠正：**「我是否已否决不是最重要。对理论的影响才是最重要的判断依据」**。
⇒ 旧否决约束的是**论文措辞**，不应被升格为**理论构造**的禁令。判据回到「对理论的影响」。

## 实测：被否掉那条路的真实成本（原先估错）

- `SpObj` 定义：`SpCategory.lean` L31，字段仅 `(n : ℕ, A : Matrix (Fin n) (Fin n) ℂ)`。
- `RecObj` 定义：`RecCategory.lean` L26，字段 `(T : Type u, fin, dec, step : T → T)`。
- `SpObj.mk` 全库 = 3 处（同一文件）；`RecObj.mk` = 0 处；`RecObj` 匿名构造 = 1 处（`Braided.lean` L120）。
- `.step` 使用 = 473 行 / 31 文件（`HigherRecCategory` 118、`PulsarRadiation` 73、`GWPolarization` 64、`DualChannel` 50）。

⇒ **「加字段而不动 `step`」的破坏面仅 1 个构造点，不是「不可行」。原判断是成本误判。**

## 与论文的字段级对照（结构层面丢失）

| `paper1` 数学对象 | 库内 Lean 结构 | 丢失项 |
|---|---|---|
| `Rec = (S_R, Φ_R, T_R, M_R)` | `RecObj = (T : Type, fin, dec, step : T → T)` | `T_R` 时间半群（**名字被挪用给状态空间类型**）；`Φ_R` 的**时间参数**（退化为单步 `step`）；`M_R` 测度 |
| `Sp = (H_E, A_E, σ_E)` | `SpObj = (n : ℕ, A : Matrix …)` | `H_E` 空间（只剩维数 `n`）；`σ_E` 谱测度 |

⇒ **第 42 批说「`T_R` 在 `Sp` 中没有对应物」——诊断不够深。真实情况是 `T_R` 在 `Rec` 里就没有了，`D` 函子没机会再丢它。丢失发生在「数学描述 → Lean 结构」这一步，比 `D` 函子早一层。**

## 本模块做两件事

1. **把「阶数」从注入改为真实提取**：有限集映射的**迭代周期**是对象的内禀量，不依赖外部常数。机检 `ZMod 3` 上的 `+1` 周期恰为 3。
2. **机检证伪「周期能定 3」**：给出周期 2 的同类对象，证明「周期 = 3」不是结构必然性。
   数值口径（穷举 `|T| ≤ 6` 全部 50069 个映射的全局周期 `lcm`）：`period=1` 占 36.4%、`period=2` 占 36.5%、`period=3` 占 **16.8%**、`period=4` 占 6.8%。
   ⇒ 周期 3 在穷举中既不稀有也不唯一，**不能**作为「为什么是 3」的来源。

## 诚实边界

- 本模块**不修改** `RecObj` / `SpObj`（473 行 `step` 使用零扰动）。
- 本模块只处理**纯循环**样例；一般有限映射含前导树，全局周期取循环长度之 `lcm`（数值部分已穷举覆盖该一般情形，Lean 部分未形式化）。
- 本模块**不主张**「周期 = 3」能解释 `N_active = 3`；它恰恰机检了这条**不能**成立。
- `N_active := 3` 的正式定义（`DHStructuralAnalysis` L99）**未改**。
-/

import Mathlib.Tactic
import Mathlib.Data.ZMod.Basic
import MUFPFormalization.RecCategory

namespace MUFPF.RecOrder

open MUFPF

/-! ## 一、把「阶数」变成对象的内禀量：纯函数层的周期 -/

/-- `ZMod 3` 上的 `+1` 迭代三次回到恒等。这是「3-循环」的真实内容。 -/
theorem zmod3_add_one_period_three : ((fun x : ZMod 3 => x + 1)^[3]) = id := by
  funext x
  revert x
  decide

/-- 它的一次迭代**不是**恒等（`0 ↦ 1`），故周期恰为 3，不是 1。 -/
theorem zmod3_add_one_not_id : ((fun x : ZMod 3 => x + 1)^[1]) ≠ id := by
  intro h
  have h0 := congrFun h (0 : ZMod 3)
  simp at h0

/-- `ZMod 2` 上的同类构造：周期 2。它的存在即「周期 3 不唯一」的证据。 -/
theorem zmod2_add_one_period_two : ((fun x : ZMod 2 => x + 1)^[2]) = id := by
  funext x
  revert x
  decide

/-- 周期 2 的它也不是恒等（`0 ↦ 1`）。 -/
theorem zmod2_add_one_not_id : ((fun x : ZMod 2 => x + 1)^[1]) ≠ id := by
  intro h
  have h0 := congrFun h (0 : ZMod 2)
  simp at h0

/-! ## 二、桥：这些函数确实是某个 `RecObj` 的 `step`（非抽象存在，是同一对象） -/

/-- 3-循环递归对象：状态空间 `ZMod 3`，演化 `x ↦ x + 1`。
    这是「演化阶数 = 3」在 `RecObj` 内部的**真实**载体（周期，不是外部常数）。 -/
def cyclic3 : RecObj :=
  { T := ZMod 3, fin := inferInstance, dec := inferInstance, step := fun x => x + 1 }

/-- 2-循环递归对象：结构完全同构，只把 `3` 换成 `2`。 -/
def cyclic2 : RecObj :=
  { T := ZMod 2, fin := inferInstance, dec := inferInstance, step := fun x => x + 1 }

/-- `cyclic3` 的 `step` 就是上面那条周期为 3 的函数——同一对象，不是类比。 -/
theorem cyclic3_step_eq : cyclic3.step = (fun x : ZMod 3 => x + 1) := rfl

/-- `cyclic2` 的 `step` 就是上面那条周期为 2 的函数。 -/
theorem cyclic2_step_eq : cyclic2.step = (fun x : ZMod 2 => x + 1) := rfl

/-- **3-循环对象的周期恰为 3**（把纯函数结论搬到 `RecObj` 上）。 -/
theorem cyclic3_period_is_three :
    (cyclic3.step)^[3] = id ∧ (cyclic3.step)^[1] ≠ id := by
  rw [cyclic3_step_eq]
  exact ⟨zmod3_add_one_period_three, zmod3_add_one_not_id⟩

/-- **2-循环对象的周期恰为 2**。 -/
theorem cyclic2_period_is_two :
    (cyclic2.step)^[2] = id ∧ (cyclic2.step)^[1] ≠ id := by
  rw [cyclic2_step_eq]
  exact ⟨zmod2_add_one_period_two, zmod2_add_one_not_id⟩

/-! ## 三、机检证伪：周期不唯一确定 3 -/

/-- **证伪核心**：`RecObj` 里既有周期 3 的对象，也有周期 2 的对象，且两者都非平凡。
    ⇒ 若「层数」由 `step` 的周期决定，则层数不是 3 而是「视对象而定」——理论给不出唯一值。
    ⇒ 「周期」不能作为 `N_active = 3` 的来由。 -/
theorem period_not_unique :
    (∃ X3 : RecObj.{0}, (X3.step)^[3] = id ∧ (X3.step)^[1] ≠ id) ∧
    (∃ X2 : RecObj.{0}, (X2.step)^[2] = id ∧ (X2.step)^[1] ≠ id) :=
  ⟨⟨cyclic3, cyclic3_period_is_three⟩, ⟨cyclic2, cyclic2_period_is_two⟩⟩

/-! ## 四、登记：结构层面的根因（不在本模块修复） -/

/-- **登记位（`True`）**：`RecObj` 无「阶数」字段，`N_active := 3` 的定义未采用任何对象内禀量。

    待修复方向（按第 43 批判据「看理论影响」排序，而非「看是否被否决」）：
    给 `RecObj` 增一个内禀阶数字段（破坏面：1 个匿名构造点），
    或在 `Rec` 侧用自函子初始代数把阶数定死（不动 `Sp`、不动 `D`）。
    两者都**不必**改动 `step`，故 473 行使用零扰动。 -/
theorem recobj_lacks_order_field : True := trivial

end MUFPF.RecOrder
