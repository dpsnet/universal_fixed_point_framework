import Mathlib.Algebra.Algebra.Equiv
import Mathlib.Algebra.Algebra.Prod
import Mathlib.Algebra.Algebra.Subalgebra.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Block
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
  验证上述判据不空转；
- `inner_fixes_central`：内实现固定中心元（`c * b = b * c ∀ b ⟹ σ c = c`）
  ——「内共轭不移动中心」的一般判据；
- `swapBlock_not_inner`（P1b-2 块模型）：两层非交换块代数上块交换是外；
- `swapSubAlg_not_inner`（P1b-2 完成性收口）：同一模型改以 **`Subalgebra` 载体**
  （M₄ 内块对角子代数）与**代数内部单位** `u : 𝔄ˣ` 表述内实现，块交换仍是外。

## 诚实边界（登记缺口，不在本文件证明）

- **P1b-2（已完成：非交换块模型 + Subalgebra 载体收口）**：两层块对角代数
  = M₂(ℚ) × M₂(ℚ)。①块模型：内实现 = 逐块由块内可逆矩阵共轭
  （`InnerBlockRealization`），`innerBlock_preserves_layer` 证明「内实现 ⟹ 层保持」
  （关键 `conj_eq_zero_iff` 只用逆元、不用无零因子，故对非交换环成立）。②完成性
  收口：`blockDiagAlgHom` 把该代数嵌入 M₄ 的块对角位置，`𝔄 := blockDiagAlgHom.range`
  为 `Subalgebra` 载体，内实现 = 代数**自身**单位 `∃ u : 𝔄ˣ`（不再外显「逐块单位对」），
  判别用 `inner_fixes_central`（中心元不动）。**完成性边界**：此处「外」是相对
  `𝔄ˣ` 而言（实现酉不在代数内），不含 vN 完成性（σ-弱闭、因子性）。
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

/-- ★★ 内实现固定中心元：内共轭不移动中心（`c` 与全代数交换 ⟹ σ c = c）。
    这是与层函数判据并列的第二判别：中心元在 σ 下被移动 ⟹ 外。 -/
theorem inner_fixes_central {c : A} (hc : ∀ b : A, c * b = b * c)
    {σ : A ≃ₐ[R] A} (h : InnerRealization σ) : σ c = c := by
  obtain ⟨u, hu⟩ := h
  rw [hu c, ← hc (u : A), mul_assoc, Units.mul_inv, mul_one]

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

/-! ### P1b-2 完成性收口：Subalgebra 载体

上一段的内实现是「逐块单位对」的显式形式。本段把它升格为**代数内部单位**：
把两层块对角代数实现为 M₄（索引 `Fin 2 ⊕ Fin 2`）的子代数
`𝔄 := blockDiagAlgHom.range`，内实现改为 `∃ u : 𝔄ˣ`（`𝔄` 自身的单位），
即 OC2 的口径「实现酉属于代数本身」。

判别用中心元不动（`inner_fixes_central`）：块投影 `blockDiagP₀ = (1, 0)` 在 `𝔄`
中是中心元，块交换把它送到 `blockDiagP₁ = (0, 1)`，故块交换不是 `𝔄ˣ` 内实现
——在 Subalgebra 载体上仍得 `IsOuterAut`。
-/

section SubalgebraModel

/-- 4×4 载体积：`Fin 2 ⊕ Fin 2` 索引的有理矩阵（含两层 2×2 块）。 -/
abbrev BlockMat4 := Matrix (Fin 2 ⊕ Fin 2) (Fin 2 ⊕ Fin 2) ℚ

/-- 块对角嵌入 `M₂ × M₂ →ₐ[ℚ] M₄`（非对角块置零）。 -/
def blockDiagAlgHom : TwoBlockAlg →ₐ[ℚ] BlockMat4 where
  toFun p := Matrix.fromBlocks p.1 0 0 p.2
  map_one' := by
    show Matrix.fromBlocks (1 : BlockMat) 0 0 (1 : BlockMat) = (1 : BlockMat4)
    simp
  map_mul' p q := by
    show Matrix.fromBlocks (p.1 * q.1) 0 0 (p.2 * q.2)
        = Matrix.fromBlocks p.1 0 0 p.2 * Matrix.fromBlocks q.1 0 0 q.2
    rw [Matrix.fromBlocks_multiply]
    simp
  map_zero' := by
    show Matrix.fromBlocks (0 : BlockMat) 0 0 (0 : BlockMat) = (0 : BlockMat4)
    simp
  map_add' p q := by
    show Matrix.fromBlocks (p.1 + q.1) 0 0 (p.2 + q.2)
        = Matrix.fromBlocks p.1 0 0 p.2 + Matrix.fromBlocks q.1 0 0 q.2
    rw [Matrix.fromBlocks_add]
    simp
  commutes' x := by
    ext i j
    rcases i with i | i <;> rcases j with j | j <;> simp [Matrix.algebraMap_matrix_apply]

/-- 两层块对角代数作为 M₄ 的子代数（**Subalgebra 载体** `𝔄`）。 -/
def blockDiagSubalgebra : Subalgebra ℚ BlockMat4 := blockDiagAlgHom.range

/-- 块对角嵌入是单射（整体块相等 ⟺ 四个块相等）。 -/
theorem blockDiagAlgHom_injective : Function.Injective blockDiagAlgHom := by
  intro p q h
  have h' : Matrix.fromBlocks p.1 (0 : BlockMat) (0 : BlockMat) p.2
      = Matrix.fromBlocks q.1 (0 : BlockMat) (0 : BlockMat) q.2 := h
  rw [Matrix.fromBlocks_inj] at h'
  exact Prod.ext h'.1 h'.2.2.2

/-- `M₂ × M₂ ≃ₐ[ℚ] 𝔄`：块对角代数与子代数载体的等价（载体迁移通道）。 -/
noncomputable def blockDiagEquiv : TwoBlockAlg ≃ₐ[ℚ] blockDiagSubalgebra :=
  AlgEquiv.ofInjective blockDiagAlgHom blockDiagAlgHom_injective

/-- 层 0 的块投影 `(1, 0)`，作为 `𝔄` 的元素。 -/
def blockDiagP₀ : blockDiagSubalgebra :=
  ⟨blockDiagAlgHom (1, 0), blockDiagAlgHom.mem_range_self (1, 0)⟩

/-- 层 1 的块投影 `(0, 1)`，作为 `𝔄` 的元素。 -/
def blockDiagP₁ : blockDiagSubalgebra :=
  ⟨blockDiagAlgHom (0, 1), blockDiagAlgHom.mem_range_self (0, 1)⟩

/-- ★ `blockDiagP₀` 是 `𝔄` 的中心元：与全部元素交换（块对角乘法的第一块单位）。 -/
theorem blockDiagP₀_central (y : blockDiagSubalgebra) :
    blockDiagP₀ * y = y * blockDiagP₀ := by
  obtain ⟨q, hq⟩ := y.property
  apply Subtype.ext
  change (blockDiagP₀ : BlockMat4) * (y : BlockMat4) = (y : BlockMat4) * (blockDiagP₀ : BlockMat4)
  rw [← hq]
  show Matrix.fromBlocks (1 : BlockMat) (0 : BlockMat) (0 : BlockMat) (0 : BlockMat)
      * Matrix.fromBlocks q.1 (0 : BlockMat) (0 : BlockMat) q.2
      = Matrix.fromBlocks q.1 (0 : BlockMat) (0 : BlockMat) q.2
      * Matrix.fromBlocks (1 : BlockMat) (0 : BlockMat) (0 : BlockMat) (0 : BlockMat)
  rw [Matrix.fromBlocks_multiply, Matrix.fromBlocks_multiply]
  simp

/-- ★ 两个块投影不同：`blockDiagP₀ ≠ blockDiagP₁`。 -/
theorem blockDiagP₀_ne_P₁ : blockDiagP₀ ≠ blockDiagP₁ := by
  intro hcon
  have hval : Matrix.fromBlocks (1 : BlockMat) (0 : BlockMat) (0 : BlockMat) (0 : BlockMat)
      = Matrix.fromBlocks (0 : BlockMat) (0 : BlockMat) (0 : BlockMat) (1 : BlockMat) :=
    congrArg Subtype.val hcon
  rw [Matrix.fromBlocks_inj] at hval
  exact one_ne_zero hval.1

/-- 块交换提升到子代数载体：`𝔄 ≃ₐ[ℚ] 𝔄`（经 `M₂ × M₂` 的块交换）。 -/
noncomputable def swapSubAlgEquiv : blockDiagSubalgebra ≃ₐ[ℚ] blockDiagSubalgebra :=
  blockDiagEquiv.symm.trans (swapBlockAlgEquiv.trans blockDiagEquiv)

/-- 载体一致性：`blockDiagP₀ = blockDiagEquiv (1, 0)`。 -/
theorem blockDiagP₀_eq_blockDiagEquiv : blockDiagP₀ = blockDiagEquiv (1, 0) := by
  apply Subtype.ext
  show (blockDiagP₀ : BlockMat4) = (blockDiagEquiv (1, 0) : BlockMat4)
  rw [show (blockDiagEquiv (1, 0) : BlockMat4) = blockDiagAlgHom (1, 0) from
    AlgEquiv.ofInjective_apply blockDiagAlgHom blockDiagAlgHom_injective (1, 0)]
  rfl

/-- 载体一致性：`blockDiagP₁ = blockDiagEquiv (0, 1)`。 -/
theorem blockDiagP₁_eq_blockDiagEquiv : blockDiagP₁ = blockDiagEquiv (0, 1) := by
  apply Subtype.ext
  show (blockDiagP₁ : BlockMat4) = (blockDiagEquiv (0, 1) : BlockMat4)
  rw [show (blockDiagEquiv (0, 1) : BlockMat4) = blockDiagAlgHom (0, 1) from
    AlgEquiv.ofInjective_apply blockDiagAlgHom blockDiagAlgHom_injective (0, 1)]
  rfl

/-- ★★ 块交换在 Subalgebra 载体上移动块投影：`σ P₀ = P₁`。 -/
theorem swapSubAlg_moves : swapSubAlgEquiv blockDiagP₀ = blockDiagP₁ := by
  change blockDiagEquiv (swapBlockAlgEquiv (blockDiagEquiv.symm blockDiagP₀)) = blockDiagP₁
  rw [blockDiagP₀_eq_blockDiagEquiv, AlgEquiv.symm_apply_apply]
  exact blockDiagP₁_eq_blockDiagEquiv.symm

/-- ★★ 层被移动：`σ P₀ ≠ P₀`。 -/
theorem swapSubAlg_shifts : swapSubAlgEquiv blockDiagP₀ ≠ blockDiagP₀ := by
  rw [swapSubAlg_moves]
  exact blockDiagP₀_ne_P₁.symm

/-- ★★★ P1b-2 完成性收口主定理：块交换不是 `𝔄ˣ` 内实现
    ——在 Subalgebra 载体与「代数内部单位」的表述下，「外」依旧成立。 -/
theorem swapSubAlg_not_inner : ¬ InnerRealization swapSubAlgEquiv := by
  intro h
  exact swapSubAlg_shifts
    (inner_fixes_central (c := blockDiagP₀) (fun y => blockDiagP₀_central y) h)

/-- 同一结论的 `IsOuterAut` 形式（与 P1b-1 的 OC2 口径一致）。 -/
theorem swapSubAlg_outer : IsOuterAut swapSubAlgEquiv := swapSubAlg_not_inner

end SubalgebraModel

end MUFPF.RecursionModularityOuter
