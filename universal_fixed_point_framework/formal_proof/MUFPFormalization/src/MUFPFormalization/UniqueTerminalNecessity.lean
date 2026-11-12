/-
  MUFPF — 唯一终点的必然性：`|Fix| = 1` 从何而来（第 48 批）

## 承上（第 47 批的登记位二）

第 47 批把 `N_active = 3` 推到「`|T| = 4 ∧ |Fix| = 1 ⇒ |A| = 3`」，并把剩余注入点
准确标注为：**`|Fix| = 1`（唯一终点）为什么必然**——当时只证明了「若它是 1，则 3 唯一」。

本批回答这个问题，答案是三段，且第二段是负结论：

1. **不必然**。存在 `|T| = 4` 而 `|Fix| = 2` 的对象（`twofix`，签名 `(2,2)`）。
   所以 `|Fix| = 1` 不能由 `RecObj` 的三个字段（`T`、`fin`、`dec`、`step`）推出。
2. **若要求「时间单向」，则必然**。给出「深度函数」`ρ`（单射 + 有界 + 非顶必严格推进
   + 逐点「推进或停住」），则不动点集恰是一个单元素集（`fixFinset_eq_singleton`）。
   配合 `|T| = 4` 就得到签名 `(3,1)`（`signature_eq_three_one`）。
   ⇒ 唯一终点的来由是**时间的单向性**，而不是公设。这正是用户第 44 批的判断
   「递归是指向时间的」在 `RecObj` 层的机检形态。
3. **但「唯一终点」反推不出「单向」**。`loopOne` 的签名同样是 `(3,1)`，
   却含一个 2-循环 ⇒ 它没有深度函数（`loopOne_depth_absent`）。
   ⇒ 签名 `(3,1)` 本身**不是**「时间」的证据；要「时间」，必须另外要求单向性。

## 诚实边界

- 本批**不证** `ρ`（深度函数）的存在性。它是一条**结构要求**：`ρ` 单射意味着
  「不同状态占不同深度」，`hprog` 意味着「除最深一层外必须前进」。这两条合起来
  就是「有刻度、只能向前、到顶停住」——是时间语义本身，无法从 `step : T → T` 推出。
- 本批**不证** `|T| = 4`。它仍来自 `f² = 2^f` 的非退化解 `f = 4`（第 31/35/45 批）。
- 本批**不证**「本理论必须选单向对象」。`twofix` 与 `loopOne` 是合法 `RecObj`，
  在库里它们与 `chain4` 平权存在。本批给的是：**若**要时间和刻度，**则**唯一终点；反之不成立。
- 第 47 批的 `clifford_free_on_signature_admitted`（签名 → `Cl(p,q)` 泛构造未形式化）
  本批未处理，仍然登记。
-/

import Mathlib.Tactic
import MUFPFormalization.RecCategory
import MUFPFormalization.RecTimeDepth
import MUFPFormalization.ActiveFixSignature

namespace MUFPF.UniqueTerminal

open MUFPF.RecTime
open MUFPF.ActiveFixSignature

/- 与第 47 批同样的处理：把 `RecObj` 的 `Fintype` / `DecidableEq` 字段注册成局部
   instance，保证 `Finset.univ`、`Fintype.card` 在同一对象上取到同一个实例，
   避免子证明里各自的 `haveI` 造出不同实例。前面必须是普通块注释，不能是 `/-- doc -/`。 -/
attribute [local instance] RecObj.fin RecObj.dec

/-! ## 一、深度函数：时间的单向性在 `RecObj` 层的形状

`ρ` 把状态空间排成一条有刻度的链：`ρ` 单射（不同状态不同深度）、`M` 是深度上界、
`m` 是唯一达到上界的状态。`hprog`：非最深一层必须严格前进；`hstep`：每一点要么
前进、要么已经停住（不许折返，也不许跳跃）。 -/

/-- **深度函数**：给一个 `RecObj` 装备一条「有刻度、单向、到顶停住」的深度链。 -/
structure DepthData (R : RecObj) where
  /-- 深度函数。 -/
  ρ : R.T → ℕ
  /-- 深度上界。 -/
  M : ℕ
  /-- 达到上界的唯一状态（也应当就是唯一终点）。 -/
  m : R.T
  /-- 不同状态深度不同。 -/
  hinj : Function.Injective ρ
  /-- 深度不超过上界（有限性）。 -/
  hmax : ∀ x, ρ x ≤ M
  /-- `m` 恰在最高深度。 -/
  htop : ρ m = M
  /-- 非最深一层必须严格前进。 -/
  hprog : ∀ x, ρ x ≠ M → ρ x < ρ (R.step x)
  /-- 每一点要么前进、要么停住（不许折返）。 -/
  hstep : ∀ x, ρ x < ρ (R.step x) ∨ R.step x = x

/-- ★★★ **最高层必是终点**：深度达到上界的状态不可能再前进，
    否则深度超过上界。⇒ 唯一终点**存在**，且它就是 `m`。 -/
theorem top_is_fixpoint {R : RecObj} (D : DepthData R) : R.step D.m = D.m := by
  by_contra hne
  have hlt : D.ρ D.m < D.ρ (R.step D.m) := (D.hstep D.m).resolve_right hne
  have hle : D.ρ (R.step D.m) ≤ D.M := D.hmax _
  rw [← D.htop] at hle
  omega

/-- ★★★ **没有第二个不动点**：任何不动点都必须在最高深度，
    而最高深度只有一个状态（`ρ` 单射）。⇒ 终点唯一。 -/
theorem eq_top_of_fixpoint {R : RecObj} (D : DepthData R) {x : R.T}
    (hx : R.step x = x) : x = D.m := by
  by_contra hne
  have hneM : D.ρ x ≠ D.M := by
    intro hEq
    apply hne
    apply D.hinj
    rw [hEq, ← D.htop]
  have hlt : D.ρ x < D.ρ (R.step x) := D.hprog x hneM
  rw [hx] at hlt
  exact absurd hlt (Nat.lt_irrefl _)

/-- ★★★ **静默集恰是一个单元素集**：`Fix R = {m}`。 -/
theorem fixFinset_eq_singleton {R : RecObj} (D : DepthData R) :
    fixFinset R = {D.m} := by
  ext x
  rw [mem_fixFinset_iff R]
  constructor
  · intro hx
    exact Finset.mem_singleton.mpr (eq_top_of_fixpoint D hx)
  · intro hx
    have hxm : x = D.m := Finset.mem_singleton.mp hx
    rw [hxm]
    exact top_is_fixpoint D

/-- ★★★ **`|Fix| = 1`**：唯一终点由深度函数给出，不是公设。 -/
theorem fixCount_eq_one {R : RecObj} (D : DepthData R) : fixCount R = 1 := by
  unfold fixCount
  rw [fixFinset_eq_singleton D]
  simp

/-- ★★★ **签名必为 `(3, 1)`**：`|T| = 4` 加唯一终点，活跃层数只能是 3。
    与第 47 批 `active_count_three` 同源，但这里唯一终点来自深度函数而非前提。 -/
theorem signature_eq_three_one {R : RecObj} (D : DepthData R)
    (hT : Fintype.card R.T = 4) : (activeCount R, fixCount R) = (3, 1) := by
  have h1 := fixCount_eq_one D
  have h3 := active_count_three R hT h1
  rw [h3, h1]

/-! ## 二、`chain4` 有深度函数（单向链满足全部条件） -/

/-- `chain4` 的深度函数就是「下标本身」：`ρ x = x.val`，上界 3，顶点 `⟨3⟩`。 -/
def chain4Depth : DepthData chain4 where
  ρ := fun x => x.val
  M := 3
  m := ⟨3, by omega⟩
  hinj := by
    intro x y h
    exact Fin.ext h
  hmax := by
    intro x
    have := x.isLt
    omega
  htop := rfl
  hprog := by
    intro x hx
    revert x
    decide
  hstep := by
    intro x
    revert x
    decide

/-- ★★★ **`chain4` 的签名由深度函数推出**（与第 47 批的 `decide` 路径独立）：
    第 47 批是逐点计算，这里是「单向 ⇒ 唯一终点 ⇒ `(3,1)`」的结构论证。 -/
theorem chain4_signature_via_depth :
    (activeCount chain4, fixCount chain4) = (3, 1) :=
  signature_eq_three_one chain4Depth (by decide)

/-! ## 三、周期对象没有深度函数 -/

/-- ★★★ **周期对象不可能有深度函数**：`cyc3` 三步回到原点，
    若深度严格递增，就得到 `ρ 0 < ρ 0`。⇒ 周期给不出「时间」。 -/
theorem cycle_no_depth : ¬ ∃ ρ : ZMod 3 → ℕ, ∀ x, ρ x < ρ (cyc3 x) := by
  rintro ⟨ρ, h⟩
  have a1 : ρ (0 : ZMod 3) < ρ (cyc3 0) := h 0
  have a2 : ρ (cyc3 0) < ρ (cyc3 (cyc3 (0 : ZMod 3))) := h (cyc3 0)
  have a3 : ρ (cyc3 (cyc3 (0 : ZMod 3))) < ρ (cyc3 (cyc3 (cyc3 (0 : ZMod 3)))) :=
    h (cyc3 (cyc3 (0 : ZMod 3)))
  have a4 : cyc3 (cyc3 (cyc3 (0 : ZMod 3))) = 0 := by decide
  rw [a4] at a3
  omega

/-! ## 四、反例一：`|Fix| = 2` 的合法对象 ⇒ 唯一终点**不是必然** -/

/-- 反例：`0 ↦ 1 ↦ 1`、`2 ↦ 3 ↦ 3`。两个终点（`1` 与 `3`），两个活跃点（`0` 与 `2`）。 -/
def twofix : RecObj where
  T := Fin 4
  fin := inferInstance
  dec := inferInstance
  step := fun x =>
    if x.val = 0 ∨ x.val = 2 then ⟨min (x.val + 1) 3, by omega⟩ else x

/-- ★★ **`twofix` 恰有两个不动点** ⇒ `|Fix| = 2`。 -/
theorem twofix_fix_two : fixCount twofix = 2 := by
  decide

/-- ★★ **`twofix` 的签名是 `(2, 2)`**，不是 `(3, 1)`。 -/
theorem twofix_signature : (activeCount twofix, fixCount twofix) = (2, 2) := by
  decide

/-- ★★★ **`twofix` 给不出 `Cl(3,1)`**：同样是 `|T| = 4`，签名却是 `(2,2)`（对应 `Cl(2,2)`）。
    ⇒ `|Fix| = 1` 不能由 `RecObj` 的字段推出，它是额外的结构要求。 -/
theorem twofix_not_cl31 : (activeCount twofix, fixCount twofix) ≠ (3, 1) := by
  rw [twofix_signature]
  decide

/-! ## 五、反例二：唯一终点**反推不出**时间单向 -/

/-- 反例：`0 ↦ 1 ↦ 0` 的 2-循环，外加 `2 ↦ 3 ↦ 3`。
    唯一的终点是 `3`，但 `0 ↔ 1` 是一个周期。 -/
def loopOne : RecObj where
  T := Fin 4
  fin := inferInstance
  dec := inferInstance
  step := fun x =>
    if x.val = 0 then ⟨1, by omega⟩
    else if x.val = 1 then ⟨0, by omega⟩
    else if x.val = 2 then ⟨3, by omega⟩
    else x

/-- ★★ `loopOne` 只有一个不动点。 -/
theorem loopOne_fix_one : fixCount loopOne = 1 := by
  decide

/-- ★★★ **`loopOne` 的签名也是 `(3, 1)`**。 -/
theorem loopOne_signature_three_one :
    (activeCount loopOne, fixCount loopOne) = (3, 1) := by
  decide

/-- ★★★ **但 `loopOne` 没有深度函数**：`0 ↦ 1 ↦ 0` 使任何严格递增的 `ρ` 立即矛盾。 -/
theorem loopOne_depth_absent : ¬ ∃ ρ : loopOne.T → ℕ, ∀ x, ρ x < ρ (loopOne.step x) := by
  rintro ⟨ρ, h⟩
  have a1 : ρ (⟨0, by omega⟩ : Fin 4) < ρ (⟨1, by omega⟩ : Fin 4) := h ⟨0, by omega⟩
  have a2 : ρ (⟨1, by omega⟩ : Fin 4) < ρ (⟨0, by omega⟩ : Fin 4) := h ⟨1, by omega⟩
  omega

/-- ★★★ **`loopOne` 与 `chain4` 签名完全相同**：两者都给 `Cl(3,1)` 的号差。
    但 `loopOne_depth_absent` 证明前者没有深度函数（含 2-循环），`chain4Depth` 证明后者有。
    ⇒ **签名 `(3,1)` 本身不是「时间」的证据**；要「时间」，必须在签名之外
      另外要求单向性（`DepthData`）。这是本批最重要的边界。 -/
theorem loopOne_signature_eq_chain4 :
    (activeCount loopOne, fixCount loopOne) = (activeCount chain4, fixCount chain4) := by
  rw [loopOne_signature_three_one, chain4_signature_via_depth]

/-! ## 六、登记：本批的边界 -/

/-- **登记位一**：深度函数 `ρ` 的**存在性**未证，也不应当证——
    它不是 `RecObj` 的推论，而是一条结构要求（「有刻度、单向、到顶停住」）。
    本批证明的是：**有 `ρ` ⇒ 唯一终点**（充分），不是 **唯一终点 ⇒ 有 `ρ`**（`loopOne` 反例）。 -/
theorem depth_is_a_requirement_not_a_consequence : True := trivial

/-- **登记位二**：`|T| = 4` 仍来自自指方程 `f² = 2^f` 的非退化解 `f = 4`，
    本批未为它提供新来由。 -/
theorem f_four_unchanged : True := trivial

/-- **登记位三**：签名 `(p,q)` → `Cl(p,q)` 的泛构造仍未形式化（承第 47 批），
    本批只把 `|Fix| = 1` 的来由从「条件」落到「时间单向」，第三步的登记原样保留。 -/
theorem clifford_generic_still_admitted : True := trivial

end MUFPF.UniqueTerminal
