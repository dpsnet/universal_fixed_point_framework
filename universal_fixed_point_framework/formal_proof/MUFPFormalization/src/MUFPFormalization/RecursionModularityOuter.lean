import Mathlib.Algebra.Algebra.Equiv
import Mathlib.Algebra.Algebra.Prod
import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-!
# P1b 定义层：外自同构的代数定义与「层移动 ⟹ 外」结构定理（2026-11-01）

对应 `notes/04_lorentz_gravity/递归模同构_立项_时间模流生成链.md` §3（P1），
判据口径见 OC2：**外自同构 = 实现酉不属于代数本身**。

## 定义层（本文件新建，均为纯代数，不依赖模算子 Δ_mod / KMS）

- `InnerRealization σ`：σ 由代数内部单位 u 的共轭实现（内自同构）；
- `IsOuterAut σ`：不存在这样的内部单位（外自同构）——即 OC2 的代数形式。

## 结构定理（本文件机检）

- `layer_eq_of_inner`：内实现 ⟹ 任何「单位共轭不变的层函数 L」在 σ 下不变；
- `isOuter_of_layer_shift`：若 σ 把某个元素的层移动（L(σ a₀) ≠ L a₀），
  则 σ 不是内自同构——**「内自同构不能越层」**，即 OC3 否定式同型
  （不留在同层 ↔ 不留在代数内）的代数报文；
- `isOuter_of_strictLayer`：严格升层（L(σ a₀) = L a₀ + 1）⟹ 外
  ——与 P1a 的 `StrictLayer` 同形状；
- `inner_eq_refl_of_commutative` / `isOuter_of_ne_refl`：交换代数中内自同构
  必为恒等——外性在该情形的退化判别；
- `swap_outer_witness`：非空实例（ℚ × ℚ 上坐标交换 = 层 0 ↔ 层 1），
  验证上述判据不空转。

## 诚实边界（登记缺口，不在本文件证明）

- **P1b-2（非交换实例）**：本文件实例是交换情形（内自同构 = 恒等），
  尚不覆盖模流的非交换核心；块对角层保持代数（M_n 块层 / 单位共轭保持
  块层）是下一步。
- **P1b-3（逆向）**：外 ⟹ 单向／无回退 ⟹ 无周期——需 RecObj 上的模算子
  Δ_mod 与 KMS（β = 1）层，属 P2。
- **vN 完成性**：σ-弱闭、因子性在 Lean/Mathlib 无现成形式化；本文件
  只给代数骨架，**不声称 P1 成立**（入轨/判别 ≠ 成立/闭合）。
-/

namespace MUFPF.RecursionModularityOuter

variable {R A : Type*} [CommSemiring R] [Ring A] [Algebra R A]

/-- ★ 内实现：σ 由代数内部单位 u 的共轭实现（内自同构）。 -/
def InnerRealization (σ : A ≃ₐ[R] A) : Prop :=
  ∃ u : Aˣ, ∀ a : A, σ a = (u : A) * a * ((u⁻¹ : Aˣ) : A)

/-- ★ 外自同构：不存在代数内部单位实现共轭（OC2 的代数定义）。
    纯代数概念——不引用模算子 Δ_mod，也不引用 KMS 条件。 -/
def IsOuterAut (σ : A ≃ₐ[R] A) : Prop := ¬ InnerRealization σ

/-- ★★ 内实现 ⟹ 单位共轭不变的层函数在 σ 下不变
    （「内自同构不能越层」的正面形式）。 -/
theorem layer_eq_of_inner {α : Type*} (L : A → α)
    (hL : ∀ (u : Aˣ) (a : A), L ((u : A) * a * ((u⁻¹ : Aˣ) : A)) = L a)
    {σ : A ≃ₐ[R] A} (h : InnerRealization σ) (a : A) : L (σ a) = L a := by
  obtain ⟨u, hu⟩ := h
  rw [hu a]
  exact hL u a

/-- ★★ 层移动 ⟹ 外（P1b 的核心结构定理）：
    若某个元素的层在 σ 下改变，则 σ 不可能由代数内部单位实现。 -/
theorem isOuter_of_layer_shift {α : Type*} (L : A → α)
    (hL : ∀ (u : Aˣ) (a : A), L ((u : A) * a * ((u⁻¹ : Aˣ) : A)) = L a)
    (σ : A ≃ₐ[R] A) (a₀ : A) (hshift : L (σ a₀) ≠ L a₀) : IsOuterAut σ := by
  intro hin
  exact hshift (layer_eq_of_inner L hL hin a₀)

/-- ★★ 严格升层 ⟹ 外：与 P1a 的 `StrictLayer`（ev 严格升层）同形状的
    层函数版——「递归一层 = 时间递进一层」在代数侧读作「单位共轭不能
    把层号推进 1」。 -/
theorem isOuter_of_strictLayer (L : A → ℕ)
    (hL : ∀ (u : Aˣ) (a : A), L ((u : A) * a * ((u⁻¹ : Aˣ) : A)) = L a)
    (σ : A ≃ₐ[R] A) (a₀ : A) (hσ : L (σ a₀) = L a₀ + 1) : IsOuterAut σ := by
  refine isOuter_of_layer_shift L hL σ a₀ ?_
  intro hcon
  rw [hσ] at hcon
  exact Nat.succ_ne_self (L a₀) hcon

section Commutative

variable {R A : Type*} [CommSemiring R] [CommRing A] [Algebra R A]

/-- 交换代数中，单位共轭平凡（= 恒等）：u a u⁻¹ = a。 -/
theorem conj_eq_self_of_commutative (u : Aˣ) (a : A) :
    (u : A) * a * ((u⁻¹ : Aˣ) : A) = a := by
  rw [mul_comm (u : A) a, mul_assoc, Units.mul_inv, mul_one]

/-- 交换代数中内自同构必为恒等（外性在该情形的退化判别）。 -/
theorem inner_eq_refl_of_commutative {σ : A ≃ₐ[R] A}
    (h : InnerRealization σ) : σ = AlgEquiv.refl := by
  obtain ⟨u, hu⟩ := h
  ext a
  rw [hu a, conj_eq_self_of_commutative]
  rfl

/-- 交换代数中：非恒等 ⟹ 外。 -/
theorem isOuter_of_ne_refl {σ : A ≃ₐ[R] A}
    (h : σ ≠ AlgEquiv.refl) : IsOuterAut σ := by
  intro hin
  exact h (inner_eq_refl_of_commutative hin)

end Commutative

/-! 非空实例：ℚ × ℚ 上的坐标交换 = 层 0 ↔ 层 1，
    `L p = if p.1 = 0 then 0 else 1`——层 0/1 由第一分量是否为 0 标注。 -/

/-- 坐标交换提升为 ℚ-代数自同构。 -/
def swapAlgEquiv : (ℚ × ℚ) ≃ₐ[ℚ] (ℚ × ℚ) where
  toFun p := (p.2, p.1)
  invFun p := (p.2, p.1)
  left_inv p := by rcases p with ⟨a, b⟩; rfl
  right_inv p := by rcases p with ⟨a, b⟩; rfl
  map_mul' p q := by rcases p with ⟨a, b⟩; rcases q with ⟨c, d⟩; rfl
  map_add' p q := by rcases p with ⟨a, b⟩; rcases q with ⟨c, d⟩; rfl
  commutes' x := rfl

/-- 实例层函数：第一分量非零 ⟹ 层 1，否则层 0。 -/
def layerOfPair (p : ℚ × ℚ) : ℕ := if p.1 = 0 then 0 else 1

/-- ★★ 非空实例：坐标交换把 (1,0)（层 1）送到 (0,1)（层 0）——
    层改变 ⟹ 交换是外自同构（判据不空转）。 -/
theorem swap_outer_witness :
    IsOuterAut (R := ℚ) (A := ℚ × ℚ) swapAlgEquiv := by
  refine isOuter_of_layer_shift (R := ℚ) (A := ℚ × ℚ) (L := layerOfPair)
    (σ := swapAlgEquiv) (a₀ := (1, 0)) ?_ ?_
  · intro u a
    exact congrArg layerOfPair (conj_eq_self_of_commutative u a)
  · show layerOfPair (swapAlgEquiv (1, 0)) ≠ layerOfPair (1, 0)
    have h : swapAlgEquiv (1, 0) = (0, 1) := rfl
    rw [h]
    norm_num [layerOfPair]

end MUFPF.RecursionModularityOuter
