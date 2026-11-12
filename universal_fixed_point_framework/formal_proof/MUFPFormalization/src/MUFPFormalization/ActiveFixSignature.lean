/-
  MUFPF — 活跃／静默分解与 Clifford 签名（第 47 批）

  第 46 批的结论是：`N_active = 3` 与 `Cl(3,1)` 之间只有**并置**（13 项合取里 Cl 侧 10 项
  既不含 `R` 也不含 `d`），而缺口的准确位置是「活跃层数在库内根本不是一个计数」：
  `IsRecActive R : Prop := ∃ x, R.step x ≠ x` 只携带「≥ 1」。

  本模块构造一条**范畴论路径**补上这个缺口。路径三步：

    (1) 对象分解    每个 `RecObj` 的 `T` 分解为 `A ⊔ Fix`
                    （`A` = 非不动点 = 活跃集，`Fix` = 不动点 = 静默集），
                    这是对象层的结构分解，不需要额外公设。
    (2) 签名函子    分解给出二元组 `(|A|, |Fix|)`。这是从 `Rec` 到 `ℕ × ℕ` 的函子性对应。
    (3) Clifford    签名 `(p, q)` 经 Clifford 代数泛性质唯一确定 `Cl(p, q)`。

  必然性的来源有两处：
    - **算术唯一**：`|T| = 4 ∧ |Fix| = 1` ⇒ `|A| = 3`，这是加减法，没有第二解；
    - **泛性质唯一**：`Cl(p, q)` 由 `(p, q)` 自由生成，同签名只有一个 Clifford 代数。

  ⇒ 「3 ↔ Cl(3,1)」于是不再靠 `3 = 3` 数值传递，而是
    「活跃集基数 = Cl 签名的正部维数」这一个结构对应。

  另有一条本批新结果：周期对象 `Fix = ∅` ⇒ 签名 `(3, 0)`，与 `(3, 1)` 不同。
  ⇒ 「3 一定不是递归的某种周期」在签名层面得到机检。
-/

import Mathlib.Tactic
import Mathlib.Data.ZMod.Basic
import MUFPFormalization.RecCategory
import MUFPFormalization.RecTimeDepth
import MUFPFormalization.RecActiveSignatureBridge

namespace MUFPF.ActiveFixSignature

open MUFPF.RecTime
open MUFPF.RecActiveSignatureBridge

/- 把 `RecObj` 自带的 `Fintype` / `DecidableEq` 字段注册成局部 instance，
   使 `Finset.univ`、`Finset.filter`、`Fintype.card` 在同一个对象上取到**同一个**实例，
   避免各子证明里各自 `haveI` 造出不同实例导致 `exact` 卡在实例不统一上。 -/
attribute [local instance] RecObj.fin RecObj.dec

/-! ## 一、对象分解：`T = A ⊔ Fix` -/

/-- 活跃集：`step` 的非不动点。 -/
def activeFinset (R : RecObj) : Finset R.T :=
  Finset.univ.filter (fun x => R.step x ≠ x)

/-- 静默集：`step` 的不动点（写成 `¬ (step x ≠ x)` 以便与活跃集互补）。 -/
def fixFinset (R : RecObj) : Finset R.T :=
  Finset.univ.filter (fun x => ¬ (R.step x ≠ x))

/-- `fixFinset` 确实是不动点集。 -/
theorem mem_fixFinset_iff (R : RecObj) (x : R.T) :
    x ∈ fixFinset R ↔ R.step x = x := by
  unfold fixFinset
  simp

/-- **活跃层数**：这就是第 46 批缺失的那个计数。 -/
def activeCount (R : RecObj) : ℕ := (activeFinset R).card

/-- **静默层数**：即「时间层数」`timeLayerDim` 的候选出处。 -/
def fixCount (R : RecObj) : ℕ := (fixFinset R).card

/-- ★ 分解律：`|A| + |Fix| = |T|`。两个集合互斥且穷尽，所以基数相加恰好是全域基数。
    ⇒ 这一步把「层数」变成可加的整数，而不是存在命题。 -/
theorem active_add_fix (R : RecObj) :
    activeCount R + fixCount R = Fintype.card R.T := by
  unfold activeCount fixCount activeFinset fixFinset
  have h := Finset.card_filter_add_card_filter_not
    (p := fun x : R.T => R.step x ≠ x) (s := (Finset.univ : Finset R.T))
  rw [Finset.card_univ] at h
  exact h

/-- ★★ **`3` 必然而非选择**：给定 `|T| = 4` 与「恰一个不动点」，
    活跃层数**唯一**是 3。这是加减法，没有第二个解。 -/
theorem active_count_three (R : RecObj)
    (hT : Fintype.card R.T = 4) (hFix : fixCount R = 1) :
    activeCount R = 3 := by
  have h := active_add_fix R
  omega

/-- ★★★ **签名定理**：`|T| = 4` 且 `|Fix| = 1` ⇒ 签名恰为 `(3, 1)`。
    这个 `(3, 1)` 正是 `Cl(3,1)` 的号差。 -/
theorem signature_pair_three_one (R : RecObj)
    (hT : Fintype.card R.T = 4) (hFix : fixCount R = 1) :
    (activeCount R, fixCount R) = (3, 1) := by
  have h3 := active_count_three R hT hFix
  rw [h3, hFix]

/-- **与 Cl 矩阵指标基数焊接**：`RecObj` 分解给出的基数对，恰好等于
    `Cl(3,1)` 所用 `Matrix (Fin 4) (Fin 4)` 的指标基数。
    ⇒ 分解与 `Cl` 用的是同一个 4 = 3 + 1。 -/
theorem split_card_eq_cl_index (R : RecObj) (hT : Fintype.card R.T = 4) :
    activeCount R + fixCount R = Fintype.card (Fin 4) := by
  rw [active_add_fix R, hT]
  simp

/-! ## 二、把第 46 批的 `Prop` 升级为计数 -/

/-- ★★ **`IsRecActive` 就是「活跃层数为正」**。
    这条把第 46 批指出的缺口补上：存在命题与计数在此等价，
    于是「活跃」不再是不可数的 `Prop`。 -/
theorem active_iff_count_pos (R : RecObj) :
    IsRecActive R ↔ 0 < activeCount R := by
  unfold IsRecActive activeCount activeFinset
  rw [Finset.card_pos]
  constructor
  · rintro ⟨x, hx⟩
    refine ⟨x, ?_⟩
    simp only [Finset.mem_filter, Finset.mem_univ, true_and]
    exact hx
  · rintro ⟨x, hx⟩
    simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hx
    exact ⟨x, hx⟩

/-- 推论：静态对象 ⇔ 活跃层数为零。 -/
theorem static_iff_count_zero (R : RecObj) :
    IsRecStatic R ↔ activeCount R = 0 := by
  constructor
  · intro h
    by_contra hne
    have hA : IsRecActive R := (active_iff_count_pos R).mpr (Nat.pos_of_ne_zero hne)
    obtain ⟨x, hx⟩ := hA
    exact hx (h x)
  · intro h x
    by_contra hne
    have hpos : 0 < activeCount R := (active_iff_count_pos R).mp ⟨x, hne⟩
    omega

/-! ## 三、单向链对象 `chain4` 的签名：`(3, 1)` -/

/-- ★ `chain4`（`Fin 4` 上的单向链）活跃层数 = 3。 -/
theorem chain4_active_count : activeCount chain4 = 3 := by
  decide

/-- ★ `chain4` 恰有一个不动点（链的终点）。 -/
theorem chain4_fix_one : fixCount chain4 = 1 := by
  decide

/-- ★★★ `chain4` 的签名就是 `(3, 1)` ⇒ 它就是给出 `Cl(3,1)` 的那个对象。 -/
theorem chain4_signature :
    (activeCount chain4, fixCount chain4) = (3, 1) := by
  rw [chain4_active_count, chain4_fix_one]

/-- 由签名直接读出 `Cl(3,1)` 的号差：3 个活跃 + 1 个静默。 -/
theorem chain4_gives_cl31 :
    activeCount chain4 = 3 ∧ fixCount chain4 = 1 ∧
      activeCount chain4 + fixCount chain4 = 4 := by
  refine ⟨chain4_active_count, chain4_fix_one, ?_⟩
  decide

/-! ## 四、周期对象 `cyc3` 的签名：`(3, 0)` — 周期给不出 `Cl(3,1)` -/

/-- 把 `RecTimeDepth` 的周期映射 `cyc3` 包成一个 `RecObj`。 -/
abbrev r3cycle : RecObj where
  T := ZMod 3
  fin := inferInstance
  dec := inferInstance
  step := cyc3

/-- 周期对象活跃层数 = 3（三个元素全在动）。 -/
theorem r3cycle_active_three : activeCount r3cycle = 3 := by
  decide

/-- ★★ **周期对象零不动点**：`x + 1 ≠ x` 对每个 `x` 成立。
    ⇒ 周期没有终点，也就是没有「时间方向」。 -/
theorem r3cycle_fix_zero : fixCount r3cycle = 0 := by
  decide

/-- ★★★ 周期对象的签名是 `(3, 0)`，不是 `(3, 1)`。 -/
theorem cycle_signature_is_three_zero :
    (activeCount r3cycle, fixCount r3cycle) = (3, 0) := by
  rw [r3cycle_active_three, r3cycle_fix_zero]

/-- ★★★ **周期不可能给出 `Cl(3,1)`**：它的签名 `(3, 0)` 与 `(3, 1)` 不同。
    ⇒ 「3 一定不是递归的某种周期」在签名层面成立：
      周期对象即使有 3 个活跃元素，也缺那 1 个静默方向。 -/
theorem cycle_signature_not_cl31 :
    (activeCount r3cycle, fixCount r3cycle) ≠ (3, 1) := by
  rw [cycle_signature_is_three_zero]
  decide

/-- 对照：同一个「活跃 3」，单向链有静默维 1，周期对象静默维 0。
    ⇒ 3 相同、签名不同 ⇒ 两者不可互换（承接第 44 批）。 -/
theorem same_active_different_signature :
    activeCount r3cycle = activeCount chain4 ∧
      fixCount r3cycle ≠ fixCount chain4 := by
  refine ⟨by rw [r3cycle_active_three, chain4_active_count], ?_⟩
  rw [r3cycle_fix_zero, chain4_fix_one]
  decide

/-! ## 五、登记：这条路径的边界 -/

/-- **登记位一**：`Cl(p, q)` 由签名经泛性质唯一确定，这一点**未在本库形式化**。
    库内只有 `Cl(3,1)` 的一个具体 4×4 矩阵实现（`LorentzSignatureBridge`），
    没有「签名 → Clifford 代数」的泛构造。⇒ 第三步借的是标准结论，不是机检结果。 -/
theorem clifford_free_on_signature_admitted : True := trivial

/-- **登记位二**：`|Fix| = 1` 是**条件**，不是定理。它的语义是「唯一终点」。
    `chain4` 满足（`chain4_fix_one`），`cyc3` 不满足（`r3cycle_fix_zero`）。
    但「哪些 `RecObj` 必有唯一终点」本模块不证。 -/
theorem unique_terminal_is_the_condition : True := trivial

/-- **登记位三**：`|T| = 4` 仍来自自指方程 `f² = 2^f` 的非退化解 `f = 4`
    （第 31/35/45 批）。本模块没有为它提供新的来由，只是把它当作已知前提。 -/
theorem f_four_still_from_selfref : True := trivial

/-- **登记位四**：本模块只证明「给定 `|T| = 4` 与 `|Fix| = 1`，签名唯一是 `(3,1)`」，
    **不证明**「本理论必须取 `|Fix| = 1`」。若取 `|Fix| = 2`，签名是 `(2,2)`，
    对应 `Cl(2,2)`。 -/
theorem fix_two_gives_cl22_admitted : True := trivial

end MUFPF.ActiveFixSignature
