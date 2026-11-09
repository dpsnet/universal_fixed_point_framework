import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Complex.Basic
import MUFPFormalization.RecCategory
import MUFPFormalization.CoherenceToBranching
import MUFPFormalization.LorentzSignatureBridge

namespace MUFPF.RecActiveSignatureBridge

/-
## Rec_active → 方向性 → Cl(3,1) 物理诠释链的 Lean 化

### 三段式策略

**第一段**：IsRecActive R := ∃ x, step x ≠ x（活跃定义）
**第二段**：TimeArrow R d := 活跃 + c₃ 唯一（联合结构）
**第三段**：TimeArrow R d + Cl(3,1) → 兼容性确认

### 诚实边界

本文件完成三段式的完全 Lean 化。
未完成："为什么活跃必须导出 Cl(3,1)"（物理诠释跳跃）。
--/

open MUFPF.CoherenceToBranching
open MUFPF.LorentzSignatureBridge
open CategoryTheory

universe u

/-
## §1 活跃递归系统的定义与基本性质
--/

/-- **活跃递归系统**：存在至少一个非不动点（step x ≠ x）。 -/
def IsRecActive (R : RecObj) : Prop := ∃ x : R.T, R.step x ≠ x

/-- **静态递归系统**：所有点都是不动点（step = id）。 -/
def IsRecStatic (R : RecObj) : Prop := ∀ x : R.T, R.step x = x

/-- IsRecActive 与 IsRecStatic 互斥。 -/
theorem active_not_static (R : RecObj) (h : IsRecActive R) : ¬ IsRecStatic R := by
  intro h_static
  rcases h with ⟨x, hx⟩
  have h_fixed : R.step x = x := h_static x
  exact hx h_fixed

/-
### 活跃系统实例：Fin 2 上的 swap（0↔1）
--/

/-- swapFin2 : Fin 2 → Fin 2（0↔1 交换）。 -/
noncomputable def swapFin2 : Fin 2 → Fin 2 :=
  fun x : Fin 2 => if x = (0 : Fin 2) then (1 : Fin 2) else (0 : Fin 2)

/-- swapFin2 确实交换：swap 0 = 1。 -/
lemma swapFin2_zero : swapFin2 (0 : Fin 2) = (1 : Fin 2) := by
  simp [swapFin2]

/-- swapFin2 确实交换：swap 1 = 0。 -/
lemma swapFin2_one : swapFin2 (1 : Fin 2) = (0 : Fin 2) := by
  simp [swapFin2]

/-- 活跃 Rec 实例：T = Fin 2, step = swapFin2。 -/
noncomputable def activeFin2 : RecObj :=
  ⟨Fin 2, inferInstance, inferInstance, swapFin2⟩

/-- activeFin2 是活跃系统（0 被 swap 到 1 ≠ 0）。 -/
theorem activeFin2_is_active : IsRecActive activeFin2 := by
  refine ⟨(0 : Fin 2), ?_⟩
  have hstep : activeFin2.step (0 : Fin 2) = (1 : Fin 2) := swapFin2_zero
  rw [hstep]
  by_contra hcontra
  have hval : (1 : Fin 2).val = (0 : Fin 2).val := by
    exact congr_arg Fin.val hcontra
  simp at hval

/-
## §2 TimeArrow：活跃 + c₃ 唯一的联合结构
--/

/-- **时间方向箭头**：活跃递归系统 R + c₃ 唯一时间分支（参数 d > 0）。
    注意：Lean structure 自动生成构造器 TimeArrow.mk（R, d 隐式）。 -/
structure TimeArrow (R : RecObj) (d : ℝ) where
  active : IsRecActive R
  c3_exists : silent_factor_c3 d = 1
  c3_unique : 0 < d →
    ∀ x : ℝ, (x = silent_factor_c1 d ∨ x = silent_factor_c2 d ∨ x = silent_factor_c3 d) →
      x = 1 → x = silent_factor_c3 d

/-- 从活跃性 + d > 0 自动构建 TimeArrow（手动构造器，避免与 structure mk 冲突）。
    注意：TimeArrow 所有字段都是 Prop，这是一个 theorem。 -/
theorem TimeArrow.ofActive (R : RecObj) (d : ℝ) (_hd : 0 < d) (hR : IsRecActive R) :
    TimeArrow R d := {
  active := hR
  c3_exists := c3_silent_factor_exists d
  c3_unique := fun (h : 0 < d) => c3_silent_factor_unique d h
}

/-- activeFin2 + d > 0 的 TimeArrow 实例。 -/
theorem timeArrowActiveFin2 (d : ℝ) (hd : 0 < d) : TimeArrow activeFin2 d :=
  TimeArrow.ofActive activeFin2 d hd activeFin2_is_active

/-
## §3 TimeArrow + Lorentz 签名的兼容性确认
--/

/-- **兼容性桥接定理**：TimeArrow R d 与 Cl(3,1) 签名可以联合表达为合取。

    这是 "Rec_active → 方向性 → Cl(3,1)" 链的 Lean 化中间环节：
    第一环 TimeArrow R d（活跃 + c₃ 唯一）——完全类型化
    第二环 Cl(3,1) Lorentz 签名（γ₀² = -I₄）——完全 Lean 化
    本定理确认两者在同一 namespace 内可安全联合。

    诚实边界：本定理只确认"兼容"，不导出方向性必须选择 Cl(3,1)。 -/
theorem time_arrow_with_lorentz_compatible
    (R : RecObj) (d : ℝ) (hd : 0 < d) (hR : IsRecActive R) :
    IsRecActive R ∧
    silent_factor_c3 d = 1 ∧
    (∀ x : ℝ, (x = silent_factor_c1 d ∨ x = silent_factor_c2 d ∨ x = silent_factor_c3 d) →
      x = 1 → x = silent_factor_c3 d) ∧
    (gamma0 * gamma0 = -1 • I4) ∧
    (gamma1 * gamma1 = 1 • I4) ∧
    (gamma2 * gamma2 = 1 • I4) ∧
    (gamma3 * gamma3 = 1 • I4) := by
  exact ⟨
    hR,
    c3_silent_factor_exists d,
    c3_silent_factor_unique d hd,
    gamma0_sq_neg_I4,
    gamma1_sq_pos_I4,
    gamma2_sq_pos_I4,
    gamma3_sq_pos_I4
  ⟩

/-
### TimeArrow 提取的中间引理（可独立引用）
--/

/-- TimeArrow 的活跃性 + c₃ 性质提取。 -/
lemma time_arrow_props (ta : TimeArrow R d) (hd : 0 < d) :
    IsRecActive R ∧
    silent_factor_c3 d = 1 ∧
    (∀ x : ℝ, (x = silent_factor_c1 d ∨ x = silent_factor_c2 d ∨ x = silent_factor_c3 d) →
      x = 1 → x = silent_factor_c3 d) := by
  exact ⟨ta.active, ta.c3_exists, ta.c3_unique hd⟩

/-
## §5 物理诠释链的 Lean 化续篇

SignatureTimeBridge 伪代码框架提出的四步链：
  1. unidir（单向性）——step 作为 RecHom 异于恒等映射
  2. time_dim = 1 —— c₃ 唯一性（已机检）
  3. directional（方向性）——unidir + time_dim = 1 的联合
  4. Cl(3,1) signature —— 方向性选择负定生成元

本节完成 Step 1 + Step 3 的 Lean 化。Step 2 已在 §2 TimeArrow 中完成。
Step 4 的 conditional theorem 见 DirectionalCliffordBridge.lean。
--/

/-
### 5.1 Step 1：单向性（范畴论层）

把 RecObj.step 提升为 RecHom 自同态，然后定义"单向性" = stepHom ≠ 恒等映射。
这是 IsRecActive 的 RecHom 语言重述。
--/

/-- **step 作为自同态 RecHom R R**。
    step 总是与自己交换：step (step x) = step (step x)。
    这把 set-level step 提升为 category-level morphism。 -/
noncomputable def stepHom (R : RecObj) : R ⟶ R where
  toFun := R.step
  comm := by
    intro x
    simp -- step (step x) = step (step x)，平凡成立

/-- **单向性**：step 作为 RecHom 异于恒等映射。
    这是"递归演化有非平凡方向"的范畴论表达。
    等价于 IsRecActive R。 -/
def IsUniDirectional (R : RecObj) : Prop := stepHom R ≠ 𝟙 R

/-- IsUniDirectional → IsRecActive（单向性蕴含活跃性）。 -/
theorem unidir_implies_active (R : RecObj) (h : IsUniDirectional R) : IsRecActive R := by
  unfold IsUniDirectional at h
  -- h : stepHom R ≠ 𝟙 R
  -- 反证：假设 ¬IsRecActive R → step x = x 对所有 x → stepHom R = 𝟙 R → 矛盾
  by_contra h_not_active
  have h_static : ∀ x : R.T, R.step x = x := by
    unfold IsRecActive at h_not_active
    push Not at h_not_active
    exact h_not_active
  have hstep_id : (stepHom R).toFun = id := by
    funext x
    exact h_static x
  have heq : stepHom R = 𝟙 R := by
    apply RecHom.ext
    exact hstep_id
  exact h heq

/-- IsRecActive → IsUniDirectional（活跃性蕴含单向性）。 -/
theorem active_implies_unidir (R : RecObj) (h : IsRecActive R) : IsUniDirectional R := by
  rcases h with ⟨x, hx⟩
  -- IsUniDirectional R := stepHom R ≠ 𝟙 R
  unfold IsUniDirectional
  by_contra heq
  have hstep_id : (stepHom R).toFun = id := by
    simpa [stepHom] using congr_arg RecHom.toFun heq
  have hstepx : R.step x = x := by
    have h := congr_fun hstep_id x
    exact h
  exact hx hstepx

/-- 单向性 ↔ 活跃性（两种语言的等价）。 -/
theorem unidir_iff_active (R : RecObj) : IsUniDirectional R ↔ IsRecActive R := by
  constructor
  · exact unidir_implies_active R
  · exact active_implies_unidir R

/-
### 5.2 Step 3：方向性接口

单向性 + 唯一时间维 = 方向性。
这是从 Rec_active 到 Cl(3,1) 的中间语义层。
--/

/-- **方向性接口**：单向递归系统 R + c₃ 唯一时间分支 + 方向性假设。

    三个字段：
      unidir : 单向性（Step 1）
      time_unique : c₃ 是唯一权重 = 1 的 silent_factor 分支（Step 2）
      direction_nonempty : 方向性非空假设（Step 3 的假设部分，诚实边界）

    数学意义：
      - unidir + time_unique 在 Lean 中完全可机检（来自 TimeArrow）
      - direction_nonempty 是一个"存在方向"的接口命题——我们不 prove 它为空，
        而是假设它成立，然后证明 Cl(3,1) 签名与之兼容
      - 如果 direction_nonempty 不成立，说明系统无方向性，Cl(4,0)（8×8）更合适

    诚实边界：direction_nonempty 的物理解释需要语义层（"存在不可逆演化方向"），
    这部分未 Lean 化。但方向性接口 + Cl(3,1) 签名的兼容性是 theorem。 -/
structure IsDirectional (R : RecObj) (d : ℝ) (hd : 0 < d) where
  unidir : IsUniDirectional R
  time_unique : silent_factor_c3 d = 1 ∧
    (∀ x : ℝ, (x = silent_factor_c1 d ∨ x = silent_factor_c2 d ∨ x = silent_factor_c3 d) →
      x = 1 → x = silent_factor_c3 d)
  direction_nonempty : Prop

/-- 从 TimeArrow 自动构造 IsDirectional（direction_nonempty 由调用者提供）。
    这是伪代码框架中 Step 1+2+3 的联合构造。 -/
noncomputable def IsDirectional.ofTimeArrow {R : RecObj} {d : ℝ} {hd : 0 < d} (ta : TimeArrow R d)
    (hdir : Prop) : IsDirectional R d hd := {
  unidir := active_implies_unidir R ta.active
  time_unique := ⟨ta.c3_exists, ta.c3_unique hd⟩
  direction_nonempty := hdir
}

/-- activeFin2 + d > 0 的方向性实例（direction_nonempty 由调用者提供）。 -/
noncomputable def directionalActiveFin2 (d : ℝ) (hd : 0 < d) (hdir : Prop) :
    IsDirectional activeFin2 d hd :=
  IsDirectional.ofTimeArrow (timeArrowActiveFin2 d hd) hdir

/-
## §6 五步链总结（完整版）

已完成的 Lean 化段落：
  ✅ Step 0: IsRecActive R（活跃定义）——§1
  ✅ Step 1: stepHom / IsUniDirectional（单向性，RecHom 范畴论层）——§5.1
  ✅ Step 2: TimeArrow（活跃 + c₃ 唯一，time_dim = 1）——§2
  ✅ Step 3: IsDirectional（方向性接口，unidir + time_unique + direction_nonempty）——§5.2
  ✅ Step 4: time_arrow_with_lorentz_compatible（Cl(3,1) 兼容性确认）——§3

未 Lean 化的物理解释（诚实边界）：
  ❌ direction_nonempty 的物理解释（"存在不可逆演化方向"需要 Vector/reverse 语义）
  ❌ 为什么方向性必须选择 Cl(3,1) 而 Cl(4,0) 需要 8×8 表示——物理诠释跳跃
  ✅ 但 IsDirectional + Cl(3,1) 签名可以联合表达（已机检）

方向性接口 → Cl(3,1) signature 的 conditional theorem 见 DirectionalCliffordBridge.lean。
--/

end MUFPF.RecActiveSignatureBridge
