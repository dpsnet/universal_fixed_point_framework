import Mathlib.Tactic
import Mathlib.Algebra.Lie.OfAssociative
import Mathlib.Data.Complex.Basic
import MUFPFormalization.Clifford

/-!
# 换位子李代数骨架：Δ ⟹ 群作用的代数底座（2026-10-25）

回答"Δ 是不是导致弥漫结构携带群作用"的代数层：

- 框架内 Δ = 交换律偏差（HigherSpCategory.lean），其矩阵内容 = 交换律 LHS−RHS 的
  homotopy 差（`spDelta2Cell_eq_homotopy_deviation` 已机检）——即**换位子**形式；
- 数学三段（李理论）：① Δ≠0 ⟹ 非交换（本模块 `commutator_ne_zero_iff_ne_mul`）；
  ② 换位子满足 Jacobi ⟹ 构成李代数（本模块 ★`jacobi_identity`，mathlib
  `LieRing.ofAssociativeRing` 保证任意结合环换位子即李括号）；
  ③ 李代数 ⟹ 伴随作用（Leibniz/导子，本模块 `adjoint_leibniz`，mathlib
  `lieRingSelfModule`）——群作用由 Δ 的换位子结构**内禀给出**，非外加对称性假设。

Pauli 特例（数值已验证 `scripts/commutator_jacobi_probe.py`）：Δ = [σz,σx] = 2iσy
⟹ su(2) ⟹ SU(2) 伴随作用 = SO(3) 旋转群 ⟹ O(n) 作用在弥漫结构上。

诚实边界：本模块为**代数骨架**（换位子/LieRing/Leibniz，全机检）；exp/李群（连续）层、
"弥漫结构的 Δ 恰好是这些换位子"的指认、以及 spDelta2Cell ⟹ 群作用的范畴衔接为
论证/指认层。

数值先证伪：实/复矩阵 Jacobi + 反对称残差 <1e-8 ALL PASS；[σz,σx]=2iσy、
{σz,σx}=0、[σz,σx]≠0 精确成立。
-/

namespace MUFPF.CommutatorLie

-- 任意结合环（矩阵）的换位子 = 李括号（mathlib：LieRing.ofAssociativeRing）
attribute [local instance 100] LieRing.ofAssociativeRing

open Matrix

/-- 矩阵换位子：[A,B] = A·B − B·A（= 结合环换位子 = LieRing.ofAssociativeRing 的括号）。 -/
def commutator {n : ℕ} {R : Type*} [Ring R] (A B : Matrix (Fin n) (Fin n) R) :
    Matrix (Fin n) (Fin n) R :=
  A * B - B * A

/-- 换位子与 mathlib 李括号同一（rfl 级）。 -/
lemma commutator_eq_lieBracket {n : ℕ} {R : Type*} [Ring R] (A B : Matrix (Fin n) (Fin n) R) :
    commutator A B = ⁅A, B⁆ := by
  rfl

/-- ★ Jacobi 恒等式：[A,[B,C]] + [B,[C,A]] + [C,[A,B]] = 0——换位子构成李代数（李括号公理全检）。 -/
theorem jacobi_identity {n : ℕ} {R : Type*} [Ring R] (A B C : Matrix (Fin n) (Fin n) R) :
    commutator A (commutator B C) + commutator B (commutator C A) +
      commutator C (commutator A B) = 0 := by
  simpa [commutator, LieRing.of_associative_ring_bracket] using (lie_jacobi A B C)

/-- 反对称：[B,A] = −[A,B]。 -/
theorem anticommutative {n : ℕ} {R : Type*} [Ring R] (A B : Matrix (Fin n) (Fin n) R) :
    commutator B A = -commutator A B := by
  simp [commutator]

/-- 自换位子为零：[A,A] = 0。 -/
theorem commutator_self_zero {n : ℕ} {R : Type*} [Ring R] (A : Matrix (Fin n) (Fin n) R) :
    commutator A A = 0 := by
  simp [commutator]

/-- ★ 伴随导子（Leibniz）：[A,[B,C]] = [[A,B],C] + [B,[A,C]]——ad(A) = [A,·] 是李括号的导子，
    李代数模作用（伴随作用）内禀存在（mathlib lie_lie/lieRingSelfModule）。 -/
theorem adjoint_leibniz {n : ℕ} {R : Type*} [Ring R]
    (A B C : Matrix (Fin n) (Fin n) R) :
    commutator A (commutator B C) =
      commutator (commutator A B) C + commutator B (commutator A C) := by
  have h : commutator (commutator A B) C =
      commutator A (commutator B C) - commutator B (commutator A C) := by
    simpa [commutator, LieRing.of_associative_ring_bracket] using (lie_lie A B C)
  have hplus : commutator (commutator A B) C + commutator B (commutator A C) =
      commutator A (commutator B C) := by
    calc
      commutator (commutator A B) C + commutator B (commutator A C) =
          (commutator A (commutator B C) - commutator B (commutator A C)) +
            commutator B (commutator A C) := by rw [h]
      _ = commutator A (commutator B C) := by abel
  exact hplus.symm

/-- ★ Δ ≠ 0 ⟺ 非交换：换位子非零当且仅当两算符不可交换（交换律偏差 = 换位子非零）。
    —— 这正是"Δ（交换律偏差）非平凡 ⟹ 弥漫结构由非交换算子族生成"的代数判定。 -/
theorem commutator_ne_zero_iff_ne_mul {n : ℕ} {R : Type*} [Ring R]
    (A B : Matrix (Fin n) (Fin n) R) :
    commutator A B ≠ 0 ↔ A * B ≠ B * A := by
  rw [commutator, sub_ne_zero]

/-- 反对易 ⟹ 换位子非零的充分条件：若 A·B + B·A = 0 且 2·(A·B) ≠ 0，
    则 [A,B] = 2·(A·B) ≠ 0（Pauli 层 Δ=[σz,σx]=2iσy 的代数形式）。 -/
theorem commutator_twice_of_anticomm {n : ℕ} {R : Type*} [Ring R]
    (A B : Matrix (Fin n) (Fin n) R)
    (hanticomm : A * B + B * A = 0) :
    commutator A B = (2 : R) • (A * B) := by
  rw [commutator]
  have h2 : - (A * B) = B * A := by
    calc
      - (A * B) = (A * B + B * A) - (A * B) := by rw [hanticomm]; simp
      _ = B * A := by abel
  calc
    A * B - B * A = A * B - (- (A * B)) := by rw [h2.symm]
    _ = A * B + A * B := by simp [sub_eq_add_neg]
    _ = (2 : R) • (A * B) := by rw [two_smul]

/-! ## LieAlgebra 双线性（2026-10-25 追加）

`LieRing.ofAssociativeRing` 给 LieRing 结构；以下四条补齐**标量/加法双线性**
（mathlib LieAlgebra 类公理 `lie_smul`/`add_lie`/`lie_add` 的显式矩阵形态），
矩阵换位子构成 ℝ/ℂ-李代数的三件套全检。数值先证伪
`scripts/commutator_lie_bilinear_probe.py`（加法+标量双线性最差残差 2.7e-15 ALL PASS）。
-/

/-- 加法线性（第一变量）：[A+C, B] = [A,B] + [C,B]（LieRing.add_lie 显式形态）。 -/
theorem commutator_add_left {n : ℕ} {R : Type*} [Ring R]
    (A B C : Matrix (Fin n) (Fin n) R) :
    commutator (A + C) B = commutator A B + commutator C B := by
  simp [commutator, add_mul, mul_add]
  abel_nf

/-- 加法线性（第二变量）：[A, B+C] = [A,B] + [A,C]（LieRing.lie_add 显式形态）。 -/
theorem commutator_add_right {n : ℕ} {R : Type*} [Ring R]
    (A B C : Matrix (Fin n) (Fin n) R) :
    commutator A (B + C) = commutator A B + commutator A C := by
  simp [commutator, add_mul, mul_add]
  abel_nf

/-- ★ 标量线性（第一变量）：[a·A, B] = a·[A,B]（LieModule 推出）。 -/
theorem commutator_smul_left {n : ℕ} {R : Type*} [CommRing R]
    (a : R) (A B : Matrix (Fin n) (Fin n) R) :
    commutator (a • A) B = a • commutator A B := by
  simp [commutator, smul_sub]

/-- ★ 标量线性（第二变量）：[A, a·B] = a·[A,B]（LieAlgebra.lie_smul 公理显式形态）。 -/
theorem commutator_smul_right {n : ℕ} {R : Type*} [CommRing R]
    (a : R) (A B : Matrix (Fin n) (Fin n) R) :
    commutator A (a • B) = a • commutator A B := by
  simp [commutator, smul_sub]

/-! ## Pauli su(2) 特例（2026-10-25 追加）

复用 `MUFPF.Clifford` 既有资产：`e_10` = σz（diag(1,−1)，实）、`e1_20` = σx、
`e2_20` = σy（复 2×2）、★`e_20_anticomm`（σxσy 反对易，已机检）。

定理：★[σx,σy] = 2iσz（反对易 ⟹ 换位子 = 2·乘积 + 乘积 = iσz）、★Δ=[σz,σx] = 2iσy
（交换律偏差的 Pauli 本体）——su(2) 生成元两两非交换 ⟹ Δ≠0 显式实例，
Δ ⟹ 群作用（SU(2)/SO(3) 旋转）的代数层钉死。数值先证伪
`scripts/commutator_lie_bilinear_probe.py`（换位子表残差 0、反对易残差 0、σxσy=iσz 精确）。
-/

/-- σz（复 2×2）= diag(1,−1)：时间生成元 e_10 的复系数版（Cl(1,0) 生成元，平方 +1）。 -/
def sigmaZc {n : ℕ} (hn : n = 2) : Matrix (Fin n) (Fin n) ℂ := by
  subst hn; exact !![1, 0; 0, -1]

/-- σx·σy = i·σz（Cl(2,0) 生成元乘积 = i·时间生成元）。 -/
theorem e1e2_eq_i_sigmaZ {n : ℕ} (hn : n = 2) :
    e1_20 hn * e2_20 hn = (Complex.I : ℂ) • sigmaZc hn := by
  subst hn
  funext i j
  fin_cases i <;> fin_cases j <;>
    (simp [e1_20, e2_20, sigmaZc]; try ring)

/-- ★ Pauli su(2) 换位子：[σx,σy] = 2iσz——Cl(2,0) 生成元反对易 ⟹ 换位子 = 2·(乘积)（Δ 结构）。 -/
theorem pauli_su2_commutator_e1e2 {n : ℕ} (hn : n = 2) :
    commutator (e1_20 hn) (e2_20 hn) = (2 : ℂ) • ((Complex.I : ℂ) • sigmaZc hn) := by
  have hanti : e1_20 hn * e2_20 hn + e2_20 hn * e1_20 hn = 0 := by
    rw [e_20_anticomm]
    simp
  have ht := commutator_twice_of_anticomm (e1_20 hn) (e2_20 hn) hanti
  rw [e1e2_eq_i_sigmaZ hn] at ht
  exact ht

/-- ★ Pauli Δ 非平凡：[σx,σy] ≠ 0（su(2) 生成元两两非交换——Δ≠0 的显式实例）。 -/
theorem pauli_commutator_nontrivial_e1e2 {n : ℕ} (hn : n = 2) :
    commutator (e1_20 hn) (e2_20 hn) ≠ 0 := by
  rw [pauli_su2_commutator_e1e2 hn]
  subst hn
  intro h
  have h00 := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℂ => M 0 0) h
  have hval : ((2 : ℂ) • ((Complex.I : ℂ) • sigmaZc rfl)) 0 0 ≠ 0 := by
    simp [sigmaZc]
  exact hval (by simpa using h00)

/-- ★ Δ = [σz,σx] = 2iσy：时间生成元与 σx 的换位子（交换律偏差的 Pauli 本体，
    数值 [σz,σx]=2iσy 精确成立）。 -/
theorem delta_pauli_zx {n : ℕ} (hn : n = 2) :
    commutator (sigmaZc hn) (e1_20 hn) = (2 : ℂ) • ((Complex.I : ℂ) • e2_20 hn) := by
  subst hn
  funext i j
  fin_cases i <;> fin_cases j <;>
    (simp [commutator, sigmaZc, e1_20, e2_20]; try ring)

/-! =========================================================
    S93 补翼：1×1 矩阵交换（非交换排除标量——"4 维 = 非交换最小实现"
    的代数侧论证——2026-10-26——立项文档 §8.9 候选 B 增强）
    1×1 矩阵代数 = 标量域（交换）⟹ 非交换需要 ≥ 2×2 表示
    ⟹ 2×2 矩阵空间 = 2² = 4 维（S93——SilenceFamily）——与静默闭合
    （S92：15 要求 16 态 = 4 维）双重收敛。
   ========================================================= -/

/-- ★★ 1×1 矩阵交换：标量代数交换——非交换（Δ≠0）排除 1×1 最小实现。 -/
theorem one_by_one_commutes {R : Type*} [CommRing R] (a b : R) :
    (!![a] : Matrix (Fin 1) (Fin 1) R) * !![b] = !![b] * !![a] := by
  ext i j
  fin_cases i <;> fin_cases j
  simp [Matrix.mul_apply]

/-- ★★ 1×1 换位子恒零：标量域换位子 = 0（非交换性在 1×1 不可能——
    Δ≠0 要求 ≥ 2×2 表示——最小矩阵实现 2×2——2² = 4 维）。 -/
theorem one_by_one_commutator_zero {R : Type*} [CommRing R] (a b : R) :
    commutator (!![a] : Matrix (Fin 1) (Fin 1) R) !![b] = 0 := by
  ext i j
  fin_cases i <;> fin_cases j
  simp [commutator, Matrix.mul_apply]

end MUFPF.CommutatorLie
