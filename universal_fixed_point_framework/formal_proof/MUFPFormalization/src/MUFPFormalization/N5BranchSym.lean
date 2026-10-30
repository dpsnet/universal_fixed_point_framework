/-
# N5BranchSym.lean

Phase 72：n=5 分支论证的符号引擎（推论 5.2 第 1 步"单非零项"的符号判定层）

先证伪已过（n5_branch_symbol_falsify.py）：L1/L3 穷举（k=1..3）、L2 两块
（2000 样本）、活分割公式（55 非零样本）、额外事实 sg([λ₂₃,λ₄])=s234（55 样本）。

符号层（PT̂ = V⁺ − V⁻ 的离散化，theta 逻辑）：
  θ⁺(r) = 1 ⟺ r = -1（sign=+1 时 ratio<0）；θ⁻(r) = 1 ⟺ r = +1
  PThat_sym sgds ratios = ∏sg(d)·(∏θ⁺ − ∏θ⁻)

定理：
  L1：ratio 序列含 + 与 −（异号）→ PThat_sym = 0
  L2：两块分割 ratio 恒 1 → PThat_sym = -sg(d)
  L3：ratio 全同号 r（非空）→ PThat_sym = ∏sg(d)·(-r)
  L4：三分割 Ā 存活（r₁=r₂=-1）→ Ā = -sg(d₁)·sg(d₂)

依赖：SingleMinusAmplitude.sgn（ℝ → ℤ）。零 sorry 目标。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Data.Int.Basic
import Mathlib.Tactic
import MUFPFormalization.SingleMinusAmplitude

namespace N5BranchSym

open SingleMinusAmplitude

-- ==================== theta 符号（离散化） ====================

/-- θ⁺(r)：sign=+1 的 V 因子，r=-1 时为 1，否则 0 -/
def thetaP (r : ℤ) : ℤ := if r = -1 then 1 else 0

/-- θ⁻(r)：sign=-1 的 Ṽ 因子，r=+1 时为 1，否则 0 -/
def thetaM (r : ℤ) : ℤ := if r = 1 then 1 else 0

@[simp] lemma thetaP_neg : thetaP (-1) = 1 := by simp [thetaP]
@[simp] lemma thetaP_pos : thetaP 1 = 0 := by simp [thetaP]
@[simp] lemma thetaM_neg : thetaM (-1) = 0 := by simp [thetaM]
@[simp] lemma thetaM_pos : thetaM 1 = 1 := by simp [thetaM]

/-- PT̂ 符号：∏sg(d)·(∏θ⁺ − ∏θ⁻) -/
def PThat_sym (sgds ratios : List ℤ) : ℤ :=
  List.prod sgds * (List.prod (ratios.map thetaP) - List.prod (ratios.map thetaM))

-- ==================== L1：异号 ratio → PT̂ = 0 ====================

/-- 若 x ∈ l 且 f x = 0，则 List.prod (l.map f) = 0 -/
lemma prod_map_zero_of_mem (l : List ℤ) (f : ℤ → ℤ) (x : ℤ) (hx : x ∈ l) (h0 : f x = 0) :
    List.prod (l.map f) = 0 := by
  rw [List.prod_eq_zero_iff]
  exact List.mem_map.mpr ⟨x, hx, h0⟩

/-- L1：ratio 序列同时含 +1 与 -1（异号）→ PT̂ = 0 -/
theorem PThat_sym_mixed_zero {sgds ratios : List ℤ}
    (hp : 1 ∈ ratios) (hm : -1 ∈ ratios) :
    PThat_sym sgds ratios = 0 := by
  unfold PThat_sym
  have htp : List.prod (ratios.map thetaP) = 0 :=
    prod_map_zero_of_mem ratios thetaP 1 hp (by simp [thetaP])
  have htm : List.prod (ratios.map thetaM) = 0 :=
    prod_map_zero_of_mem ratios thetaM (-1) hm (by simp [thetaM])
  rw [htp, htm]
  ring

-- ==================== L3：全同号 ratio → PT̂ = ∏sg·(-r) ====================

/-- 若 l 所有元素 = 1，则 List.prod (l.map f) = 1 -/
lemma prod_map_all_one (l : List ℤ) (f : ℤ → ℤ)
    (hall : ∀ x ∈ l, f x = 1) :
    List.prod (l.map f) = 1 := by
  rw [List.prod_eq_one]
  intro y hy
  rcases List.mem_map.mp hy with ⟨a, ha, rfl⟩
  exact hall a ha

/-- 若 l 非空且所有元素 = 0，则 List.prod (l.map f) = 0 -/
lemma prod_map_all_zero (l : List ℤ) (f : ℤ → ℤ)
    (hne : l ≠ []) (hall : ∀ x ∈ l, f x = 0) :
    List.prod (l.map f) = 0 := by
  rcases List.exists_mem_of_ne_nil l hne with ⟨x, hx⟩
  have h0x : f x = 0 := hall x hx
  exact prod_map_zero_of_mem l f x hx h0x

/-- L3：ratio 全同号 r（非空）→ PT̂ = ∏sg(d)·(-r) -/
theorem PThat_sym_uniform {sgds ratios : List ℤ} {r : ℤ}
    (hrat : ratios ≠ []) (hr1 : r = 1 ∨ r = -1)
    (hall : ∀ x ∈ ratios, x = r) :
    PThat_sym sgds ratios = List.prod sgds * (-r) := by
  unfold PThat_sym
  by_cases hrneg : r = -1
  · -- r = -1：∏θ⁺ = 1、∏θ⁻ = 0
    have htp : List.prod (ratios.map thetaP) = 1 := by
      apply prod_map_all_one
      intro x hx
      simp [thetaP, hall x hx, hrneg]
    have htm : List.prod (ratios.map thetaM) = 0 := by
      apply prod_map_all_zero ratios thetaM hrat
      intro x hx
      simp [thetaM, hall x hx, hrneg]
    rw [htp, htm, hrneg]
    ring
  · -- r = +1：∏θ⁺ = 0、∏θ⁻ = 1
    have hrpos : r = 1 := by
      exact Or.resolve_right hr1 hrneg
    have htp : List.prod (ratios.map thetaP) = 0 := by
      apply prod_map_all_zero ratios thetaP hrat
      intro x hx
      simp [thetaP, hall x hx, hrpos]
    have htm : List.prod (ratios.map thetaM) = 1 := by
      apply prod_map_all_one
      intro x hx
      simp [thetaM, hall x hx, hrpos]
    rw [htp, htm, hrpos]
    ring

-- ==================== L2：两块分割 → PT̂ = -sg(d) ====================

/-- L2：两块分割（ratio 恒 1）→ PT̂ = -sg(d) -/
theorem PThat_sym_two_blocks {d : ℤ} : PThat_sym [d] [1] = -d := by
  unfold PThat_sym
  simp [thetaP, thetaM]

-- ==================== L4：三分割 Ā 存活 → Ā = -sg(d₁)·sg(d₂) ====================

/-- L4：Ā₍abc₎ = -V_sym⁺（三分割），r₁=r₂=-1（ratio 全负）→ Ā = -sg(d₁)·sg(d₂) -/
theorem preamp3_living {d1 d2 r1 r2 : ℤ}
    (hr1 : r1 = -1) (hr2 : r2 = -1) :
    -(List.prod [d1 * thetaP r1, d2 * thetaP r2]) = -(d1 * d2) := by
  simp [thetaP, hr1, hr2]

end N5BranchSym
