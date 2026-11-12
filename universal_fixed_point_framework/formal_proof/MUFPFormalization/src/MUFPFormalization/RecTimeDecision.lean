/-
Copyright (c) 2026 MUFPF Project. All rights reserved.

# 第 44 批（续）：递归能否被确定性判定为时间？

## 用户问题

**「递归本身不能确定性的判定为时间吗?」**

## 三层回答（本模块机检第一、二层，第三层是登记）

### 第一层：半群律是白给的，判不出方向

迭代族 `f^[n]` 对**任意**映射 `f` 都满足 `f^[m+n] = f^[m] ∘ f^[n]`（结合律的性质，与 `f` 的语义无关）。
⇒ 若「递归 = 时间」的判据是半群律 `Φ(t+s) = Φ(t)∘Φ(s)`，那么这条判据**对一切单步映射恒真**，不携带任何方向信息。
⇒ 库里 `RecObj.step` / `DynSys.Φ` 恰好是单步映射，所以它们「天然是半群」——而这个「是」是空的。

### 第二层：方向来自索引，不来自递归

时间轴的方向性只能由**索引结构**提供：
- `ℕ` 索引：`n < n+1` 严格递增，**不可回返** ⇒ 半群（单向）。
- `ℤ` / `ℂ` 索引：`t` 可取负 ⇒ 可以走回去 ⇒ **群**（双向）。

这也正是 `OperatorTheory.lean` L52–54 的问题：`koopmanSemigroup` 用 `t s : ℂ`，所以它是**群**；论文 `paper1` L86–91 要求 `T_R ⊆ ℝ≥0`，是**半群**。

⇒ **判定的真正所在是「索引选 `ℕ` 还是 `ℂ`」。这是选择，不是从递归推导出来的定理。**

### 第三层：即使判出方向，也判不出刻度

良基性（`WellFounded`）是递归合法性的判据——它禁止无穷回退，因此**在判出「递归合法」的一刻就已判出了「有一个不可回返的方向」**。但 `WellFounded` 是 `Prop`，类型上不携带长度。

⇒ **方向的判定给「有没有时间」，不给「时间有几层」。**

⇒ 所以「3」不属于可判定部分。它是**刻度数量**，而刻度的数量既不能从半群律（白给）得到，也不能从良基性（无长度）得到。

## 本模块机检的结论

- `iterate_two_always_semigroup`：`f^[2] = f^[1] ∘ f^[1]` 对任意 `f` 成立 ⇒ 半群律不区分任何两个映射。
- `nat_index_strict`：`ℕ` 索引严格单向（`n < n+1`）。
- `direction_does_not_fix_length`（核心负面）：两个单向收敛族，半群律都成立（白给），但收敛步数一个是 1、一个是 3 ⇒ **方向不决定长度**。
- `third_not_from_direction`：登记位——「3」不能从方向判定得到。
- `time_direction_is_choice`：登记位——`T_R ⊆ ℝ≥0` 是选择（半群而非群），不是定理。

## 诚实边界

- 本模块**不证明**「良基 ⇒ 单向」的一般形式（用 `WellFounded.irrefl` 只能给出不可自反，完整论证需要「无无穷下降链」的构造）。
- 本模块**不给出**「刻度」的正确来源。它只证明「刻度不从方向来」。
- `f1` 与 `chain4` 是具体例子，不是「所有单向族」的量化。
- 不修改 `RecObj` / `DynSys` / `OperatorTheory` / `RecTimeDepth`。
-/

import Mathlib.Tactic
import MUFPFormalization.RecCategory
import MUFPFormalization.RecTimeDepth

namespace MUFPF.RecTimeDecision

open MUFPF
open MUFPF.RecTime

/-! ## 一、半群律是白给的 -/

/-- **半群律不携带方向信息**：`f^[2] = f^[1] ∘ f^[1]` 对**任意** `α → α` 成立。
    这不是关于时间的定理，是关于函数复合结合律的同义反复。 -/
theorem iterate_two_always_semigroup {α : Type} (f : α → α) :
    f^[2] = f^[1] ∘ f^[1] := by
  funext x
  rfl

/-- **方向来自索引**：`ℕ` 索引严格递增，`n < n + 1`，不可回返。 -/
theorem nat_index_strict (n : ℕ) : n < n + 1 :=
  Nat.lt_succ_self n

/-! ## 二、一阶收敛族（步数 1） -/

/-- `Fin 2` 上的常映射：1 步即到不动点。 -/
def f1 : Fin 2 → Fin 2 := fun _ => ⟨1, by omega⟩

/-- `f1` 一步收敛：`f1^[1] = f1^[2]`。 -/
theorem f1_converges_in_one : (f1)^[1] = (f1)^[2] := by
  funext x
  revert x
  decide

/-! ## 三、核心负面结果：方向存在，不锁刻度 -/

/-- **方向不决定长度**：`f1` 与 `chain4.step` 都是单向收敛族，半群律对两者**都**成立
    （因为对任意映射都成立，见 `iterate_two_always_semigroup`），
    但它们的收敛步数不同——`f1` 一步到位，`chain4.step` 需要三步。
    ⇒ 「单向 + 半群」这两个属性**不能**区分 1 与 3，因此不能定出刻度。 -/
theorem direction_does_not_fix_length :
    -- 两者都满足半群律（白给）
    ((f1)^[2] = (f1)^[1] ∘ (f1)^[1]) ∧
    ((chain4.step)^[2] = (chain4.step)^[1] ∘ (chain4.step)^[1]) ∧
    -- 但步数不同：一个 1 步，一个 3 步
    ((f1)^[1] = (f1)^[2]) ∧
    ((chain4.step)^[3] = (chain4.step)^[4] ∧ (chain4.step)^[2] ≠ (chain4.step)^[3]) :=
  ⟨iterate_two_always_semigroup f1,
   iterate_two_always_semigroup chain4.step,
   f1_converges_in_one,
   chain4_depth_is_three⟩

/-! ## 四、登记：可判定部分与不可判定部分的界线 -/

/-- **登记位一**：良基性给出「不可回返」，但它是 `Prop`，类型上不携带长度。
    ⇒ 递归的合法性判据能判出「有时间」，判不出「时间几步」。
    （完整论证需「无无穷下降链」的构造，本模块只登记，不证。） -/
theorem direction_gives_no_length : True := trivial

/-- **登记位二**：「3」不属于可判定部分。
    半群律白给（对任意映射成立）、良基性无长度，两条路都到不了「3」。
    ⇒ 「3」必须来自方向之外的输入（如 `f := 4`）。 -/
theorem third_not_from_direction : True := trivial

/-- **登记位三**：`T_R ⊆ ℝ≥0`（半群）是**选择**，不是定理。
    `paper1` L86–91 选了 `ℝ≥0`；`OperatorTheory.lean` L52–54 选了 `ℂ`（群）。
    两者都自洽，差别只在「要不要允许时间倒退」。 -/
theorem time_direction_is_choice : True := trivial

end MUFPF.RecTimeDecision
