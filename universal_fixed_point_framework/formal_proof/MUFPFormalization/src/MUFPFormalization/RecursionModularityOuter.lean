import Mathlib.Algebra.Algebra.Equiv
import Mathlib.Algebra.Algebra.Prod
import Mathlib.Data.Matrix.Basic
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

- **P1b-2（已完成：非交换块模型）**：两层块对角代数 = M₂(ℚ) × M₂(ℚ)；
  内实现 = 逐块由块内可逆矩阵共轭（`InnerBlockRealization`），
  `innerBlock_preserves_layer` 证明「内实现 ⟹ 层保持」（关键 `conj_eq_zero_iff`
  只用逆元、不用无零因子，故对非交换环成立）；`swapBlock_not_inner` 证明块交换
  是外。**完成性边界**：内实现用「逐块单位对」显式形式（等价于块对角代数内部
  单位对），尚未用 `Subalgebra` 载体或 vN 完成性（σ-弱闭、因子性）表述。
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

/-! ### P1b-2：非交换块模型（两层块对角代数）

前一段的实例是交换情形（内自同构 = 恒等），不含非交换核心。本段给出最小
非交换模型：两层块对角代数 = 两个 2×2 矩阵代数（块内非交换、两块互不相干），
块交换（层 0 ↔ 层 1）是代数自同构；内实现 = 逐块由块内可逆矩阵共轭
（等价于块对角代数的内部单位对）。

关键：单位共轭**不改变块的零性**（`conj_eq_zero_iff` 只用逆元、不用无零因子
——对任意环成立，故矩阵代数适用），因此内实现不能把层 0 的块搬到层 1；
而块交换把 (1,0) 送到 (0,1)，层改变 ⟹ 非内。
-/

section BlockModel

/-- 非交换块：2×2 有理矩阵代数。 -/
abbrev BlockMat := Matrix (Fin 2) (Fin 2) ℚ

/-- 两层块对角代数：两个非交换块的最小模型（非交换核心）。 -/
abbrev TwoBlockAlg := BlockMat × BlockMat

/-- 块层函数：第二块非零 ⟹ 层 1，否则层 0。 -/
def layerOfBlock (p : TwoBlockAlg) : ℕ := if p.2 = 0 then 0 else 1

/-- 块交换（层 0 ↔ 层 1）提升为 ℚ-代数自同构。 -/
def swapBlockAlgEquiv : TwoBlockAlg ≃ₐ[ℚ] TwoBlockAlg where
  toFun p := (p.2, p.1)
  invFun p := (p.2, p.1)
  left_inv p := by rcases p with ⟨a, b⟩; rfl
  right_inv p := by rcases p with ⟨a, b⟩; rfl
  map_mul' p q := by rcases p with ⟨a, b⟩; rcases q with ⟨c, d⟩; rfl
  map_add' p q := by rcases p with ⟨a, b⟩; rcases q with ⟨c, d⟩; rfl
  commutes' x := rfl

/-- 块模型的「内实现」：逐块由块内可逆矩阵的共轭实现
    （= 块对角代数内部单位对的作用，两块独立）。 -/
def InnerBlockRealization (σ : TwoBlockAlg ≃ₐ[ℚ] TwoBlockAlg) : Prop :=
  ∃ u₁ : BlockMatˣ, ∃ u₂ : BlockMatˣ, ∀ a : TwoBlockAlg,
    σ a = ((u₁ : BlockMat) * a.1 * ((u₁⁻¹ : BlockMatˣ) : BlockMat),
           (u₂ : BlockMat) * a.2 * ((u₂⁻¹ : BlockMatˣ) : BlockMat))

/-- ★ 单位共轭保持零性（任意环成立：只用逆元，不用无零因子；
    故非交换的矩阵代数同样适用）。 -/
theorem conj_eq_zero_iff {B : Type*} [Ring B] (u : Bˣ) (a : B) :
    (u : B) * a * ((u⁻¹ : Bˣ) : B) = 0 ↔ a = 0 := by
  constructor
  · intro h
    have h1 : a * ((u⁻¹ : Bˣ) : B) = 0 := by
      have := congrArg (fun x : B => ((u⁻¹ : Bˣ) : B) * x) h
      simpa [mul_assoc, Units.inv_mul] using this
    have h2 : a = 0 := by
      have := congrArg (fun x : B => x * (u : B)) h1
      simpa [mul_assoc, Units.inv_mul, mul_one] using this
    exact h2
  · intro h
    rw [h]
    simp

/-- ★★ 非交换模型的内实现 ⟹ 层保持（块零性被单位共轭保持）。 -/
theorem innerBlock_preserves_layer {σ : TwoBlockAlg ≃ₐ[ℚ] TwoBlockAlg}
    (h : InnerBlockRealization σ) (a : TwoBlockAlg) :
    layerOfBlock (σ a) = layerOfBlock a := by
  obtain ⟨u₁, u₂, hu⟩ := h
  rw [hu a]
  show (if (u₂ : BlockMat) * a.2 * ((u₂⁻¹ : BlockMatˣ) : BlockMat) = 0 then 0 else 1)
      = (if a.2 = 0 then 0 else 1)
  by_cases hzero : a.2 = 0
  · have hc : (u₂ : BlockMat) * a.2 * ((u₂⁻¹ : BlockMatˣ) : BlockMat) = 0 :=
      (conj_eq_zero_iff (u := u₂) (a := a.2)).mpr hzero
    rw [ite_eq_left hc, ite_eq_left hzero]
  · have hc : (u₂ : BlockMat) * a.2 * ((u₂⁻¹ : BlockMatˣ) : BlockMat) ≠ 0 :=
      fun hcontra => hzero ((conj_eq_zero_iff (u := u₂) (a := a.2)).mp hcontra)
    rw [ite_eq_right hc, ite_eq_right hzero]

/-- ★★ 块交换移动层：把 (1,0)（层 0）送到 (0,1)（层 1）。 -/
theorem swapBlock_shifts_layer :
    layerOfBlock (swapBlockAlgEquiv (1, 0)) ≠ layerOfBlock (1, 0) := by
  have hswap : swapBlockAlgEquiv (1, 0) = (0, 1) := rfl
  rw [hswap]
  simp [layerOfBlock]

/-- ★★★ P1b-2 主定理：块交换不是内实现——非交换模型的「外」。
    证明：层移动（swapBlock_shifts_layer）与「内实现 ⟹ 层保持」
    （innerBlock_preserves_layer）矛盾。 -/
theorem swapBlock_not_inner : ¬ InnerBlockRealization swapBlockAlgEquiv := by
  intro h
  exact swapBlock_shifts_layer (innerBlock_preserves_layer h (1, 0))

end BlockModel

end MUFPF.RecursionModularityOuter
