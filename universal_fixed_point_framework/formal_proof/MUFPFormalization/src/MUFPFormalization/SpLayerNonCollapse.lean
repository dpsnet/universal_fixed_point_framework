import MUFPFormalization.HigherSpCategory

/-!
# 层塔不塌缩：对「H³ = 0」假设的机检证伪

## 背景

`HigherSpCategory.lean` 给出 Sp 的四阶层结构（1-态射 `SpHom`、2-态射 `SpTwoMorphism`、
3-态射 `SpThreeMorphism`、4-态射 `SpFourMorphism`）。论文 §4.2 的层索引约定把层 4 定为
coherence 层、「不产生新的非平凡态射类型」，并由此读出 `N_active = 3`。

此前讨论提出一个把该约定升格为定理的候选路线：证明 **H³ = 0**，即层 4 的右端项
`Τ.secondHomotopy − Ξ.secondHomotopy` 恒落在交换子 `d_A(H) = A_X·H − H·A_Y` 的像内，
从而层 4 永远自动可解、不产生新的独立障碍。

## 本文件机检的结论

该路线**不成立**，理由是结构性的：

1. `layer4_gap_in_kernel`：**两个 3-态射的 `secondHomotopy` 之差恒在 `d_A` 的核内。**
   因为二者都是同一个非齐次方程 `d_A(K) = β.homotopy − α.homotopy` 的解，差必被 `d_A` 抹平。
   于是层 4 有解 ⟺ 该差 ∈ `ker d_A ∩ im d_A`。

2. `layer4_noncollapse`：取 `A = [[0,1],[0,0]]`（2×2 幂零 Jordan 块），
   `ker ∩ im = span{E₁₂}` **非零**，据此显式构造出 `threeA ≠ threeB` 且
   `SpFourMorphism threeA threeB` 非空的实例。故「层 4 只有退化态射」为假。

数值侧先证伪（`probe_h3.py`，pyenv）：对角谱 / 谱不交 / 随机 8 组均得 `dim(ker∩im) = 0`，
而 2×2 幂零 Jordan 得 1、3×3 得 2——即 `ker ∩ im ≠ 0` 恰在 **`A` 不可对角化**时出现。

## 对 N_active = 3 的含义（如实登记，不作正面断言）

`ker ∩ im = 0` 时塔从层 2 起全部塌缩；`ker ∩ im ≠ 0` 时层 4 及更高可无限延续。
**「恰 3 层」不落在 `d_A` 代数结构的任何一种自然终止里**，它因此只能来自层索引约定，
或需要一条本文件未提供的额外截断原则。本文件只证伪 H³ = 0，不主张任何替代路线成立。
-/

namespace MUFPF

open CategoryTheory Matrix

/-- 层 4 的右端项在交换子的核内：两个 3-态射之差被 `d_A` 抹平。

    证明只用两个 3-态射各自的 `condition`：二者都是同一非齐次方程的解，差归零。 -/
theorem layer4_gap_in_kernel {X Y : SpObj} {P Q : X ⟶ Y} {α β : SpTwoMorphism P Q}
    (Ξ Τ : SpThreeMorphism α β) :
    X.A * (Τ.secondHomotopy - Ξ.secondHomotopy)
      - (Τ.secondHomotopy - Ξ.secondHomotopy) * Y.A = 0 := by
  calc X.A * (Τ.secondHomotopy - Ξ.secondHomotopy)
          - (Τ.secondHomotopy - Ξ.secondHomotopy) * Y.A
      = (X.A * Τ.secondHomotopy - X.A * Ξ.secondHomotopy)
          - (Τ.secondHomotopy * Y.A - Ξ.secondHomotopy * Y.A) := by
        rw [Matrix.mul_sub, Matrix.sub_mul]
    _ = (X.A * Τ.secondHomotopy - Τ.secondHomotopy * Y.A)
          - (X.A * Ξ.secondHomotopy - Ξ.secondHomotopy * Y.A) := by
        abel
    _ = (β.homotopy - α.homotopy) - (β.homotopy - α.homotopy) := by
        rw [← Τ.condition, ← Ξ.condition]
    _ = 0 := by abel

/-! ## 反例实例：2×2 幂零 Jordan 块

`A = J = [[0,1],[0,0]]`（`A_X = A_Y = J`）。此时

  `d_A(H) = J·H − H·J = [[H₂₁, H₂₂ − H₁₁], [0, −H₂₁]]`

`ker = {[[a,b],[0,a]]}`（2 维）、`im = {[[p,q],[0,−p]]}`（3 维），
`ker ∩ im = span{E₁₂}`（1 维，非零）。下面把这条链显式造出来。 -/

/-- 2×2 幂零 Jordan 块。 -/
def jordanMat : Matrix (Fin 2) (Fin 2) ℂ := !![0, 1; 0, 0]

/-- 反例所用的谱对象（`n = 2`，`A = J`）。

    声明为 `abbrev`：`jordanObj.n` 需在隐式透明级别下也能归约为字面 `2`，
    否则 `Matrix (Fin jordanObj.n) (Fin jordanObj.n) ℂ` 与 `Matrix (Fin 2) (Fin 2) ℂ`
    在 `rw`／`simp` 里无法统一。 -/
abbrev jordanObj : SpObj := ⟨2, jordanMat⟩

/-- `E₁₂ = [[0,1],[0,0]]`：落在 `ker ∩ im` 内的那个元素。 -/
def matE12 : Matrix (Fin 2) (Fin 2) ℂ := !![0, 1; 0, 0]

/-- `E₂₂ = [[0,0],[0,1]]`：`d_A(E₂₂) = E₁₂` 的原像。 -/
def matE22 : Matrix (Fin 2) (Fin 2) ℂ := !![0, 0; 0, 1]

/-- 零 1-态射（`d_A(0) = 0`，合法）。 -/
def homZero : jordanObj ⟶ jordanObj := ⟨0, by simp⟩

/-- 以 `E₁₂` 为交织矩阵的 1-态射。`E₁₂·J = J·E₁₂ = 0`，故合法。 -/
def homE12 : jordanObj ⟶ jordanObj :=
  ⟨matE12, by
    ext i j
    fin_cases i <;> fin_cases j <;> simp [matE12, jordanObj, jordanMat]⟩

/-- 2×2 幂零 Jordan 块的交换子作用：`d_A(H) = J·H − H·J` 的逐分量形式。 -/
theorem jordan_commutator_apply (H : Matrix (Fin 2) (Fin 2) ℂ) :
    jordanMat * H - H * jordanMat
      = !![H 1 0, H 1 1 - H 0 0; 0, -(H 1 0)] := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [jordanMat, Matrix.mul_apply, Matrix.sub_apply, Matrix.vecMul, Matrix.vecHead,
      Matrix.vecTail, Fin.sum_univ_two]

/-- `E₁₂` 在核内：`d_A(E₁₂) = 0`。 -/
theorem jordan_E12_in_ker : jordanMat * matE12 - matE12 * jordanMat = 0 := by
  rw [jordan_commutator_apply]
  ext i j
  fin_cases i <;> fin_cases j <;> simp [matE12, Matrix.zero_apply]

/-- `d_A(E₂₂) = E₁₂`：`E₁₂` 落在像内。 -/
theorem jordan_E22_maps_to_E12 : jordanMat * matE22 - matE22 * jordanMat = matE12 := by
  rw [jordan_commutator_apply]
  ext i j
  fin_cases i <;> fin_cases j <;> simp [matE22, matE12]

/-! ### 层 2：两条 2-态射 `twoA`、`twoB`（`P = 0`，`Q = E₁₂`）

`Q − P = E₁₂`，而 `d_A(E₂₂) = E₁₂`，故 `homotopy = E₂₂` 给出合法 2-态射。
`d_A(E₁₂) = 0`，故把它再叠一层仍是合法解。 -/

/-- `homotopy = E₂₂` 的 2-态射：`0 ⟹ E₁₂`。 -/
def twoA : SpTwoMorphism homZero homE12 :=
  { homotopy := matE22
    condition := by
      show homE12.P - homZero.P = jordanMat * matE22 - matE22 * jordanMat
      rw [jordan_commutator_apply]
      ext i j
      fin_cases i <;> fin_cases j <;>
        simp [homZero, homE12, matE22, matE12, Matrix.zero_apply] }

/-- `homotopy = E₂₂ + E₁₂` 的 2-态射：与 `twoA` 同端点，但插值矩阵不同。 -/
def twoB : SpTwoMorphism homZero homE12 :=
  { homotopy := matE22 + matE12
    condition := by
      show homE12.P - homZero.P
        = jordanMat * (matE22 + matE12) - (matE22 + matE12) * jordanMat
      rw [jordan_commutator_apply (matE22 + matE12)]
      ext i j
      fin_cases i <;> fin_cases j <;>
        simp [homZero, homE12, matE22, matE12, Matrix.add_apply, Matrix.zero_apply] }

/-! ### 层 3：两条 3-态射 `threeA`、`threeB`（`α = twoA`，`β = twoB`）

`β − α = E₁₂`；`secondHomotopy = E₂₂` 与 `secondHomotopy = E₂₂ + E₁₂` 都给出 `E₁₂`，
因而是两条互不相同的合法 3-态射。 -/

/-- `secondHomotopy = E₂₂` 的 3-态射：`twoA ⇛ twoB`。 -/
def threeA : SpThreeMorphism twoA twoB :=
  { secondHomotopy := matE22
    condition := by
      show twoB.homotopy - twoA.homotopy = jordanMat * matE22 - matE22 * jordanMat
      rw [jordan_commutator_apply]
      ext i j
      fin_cases i <;> fin_cases j <;>
        simp [twoA, twoB, matE22, matE12, Matrix.sub_apply] }

/-- `secondHomotopy = E₂₂ + E₁₂` 的 3-态射：同为 `twoA ⇛ twoB`，但与 `threeA` 不同。 -/
def threeB : SpThreeMorphism twoA twoB :=
  { secondHomotopy := matE22 + matE12
    condition := by
      show twoB.homotopy - twoA.homotopy
        = jordanMat * (matE22 + matE12) - (matE22 + matE12) * jordanMat
      rw [jordan_commutator_apply (matE22 + matE12)]
      ext i j
      fin_cases i <;> fin_cases j <;>
        simp [twoA, twoB, matE22, matE12, Matrix.add_apply, Matrix.sub_apply] }

/-- `threeA` 的 `secondHomotopy` 定义性地等于 `E₂₂`。 -/
theorem threeA_secondHomotopy_eq : threeA.secondHomotopy = matE22 := rfl

/-- `threeB` 的 `secondHomotopy` 定义性地等于 `E₂₂ + E₁₂`。 -/
theorem threeB_secondHomotopy_eq : threeB.secondHomotopy = matE22 + matE12 := rfl

/-- `threeA ≠ threeB`：二者 `secondHomotopy` 在 `(0,1)` 分量上分别为 `0` 与 `1`。 -/
theorem threeA_ne_threeB : threeA ≠ threeB := by
  intro h
  have hs : threeA.secondHomotopy = threeB.secondHomotopy := by rw [h]
  have h01 : threeA.secondHomotopy (0 : Fin 2) (1 : Fin 2)
      = threeB.secondHomotopy (0 : Fin 2) (1 : Fin 2) := by rw [hs]
  simp only [threeA, threeB, matE22, matE12, Matrix.add_apply] at h01
  norm_num at h01

/-! ### 层 4：`SpFourMorphism threeA threeB` 非空

`threeB.secondHomotopy − threeA.secondHomotopy = E₁₂`，而 `E₁₂ = d_A(E₂₂)`，
故 `thirdHomotopy = E₂₂` 使其条件成立。这就是「层 4 仍产生非平凡态射」的机检反例。 -/

/-- `thirdHomotopy = E₂₂` 的 4-态射：`threeA ⇛ threeB`。 -/
def fourAB : SpFourMorphism threeA threeB :=
  { thirdHomotopy := matE22
    condition := by
      show threeB.secondHomotopy - threeA.secondHomotopy
        = jordanMat * matE22 - matE22 * jordanMat
      rw [threeB_secondHomotopy_eq, threeA_secondHomotopy_eq, jordan_E22_maps_to_E12,
        add_sub_cancel_left] }

/-- **H³ = 0 的机检反例**：存在两条互不相同的 3-态射，其间的 4-态射非空。

    故「层 4 的右端项恒落在 `im d_A` 之外、层 4 只有退化相干态射」为假：
    在 `ker ∩ im ≠ 0` 的谱形（此处为 2×2 幂零 Jordan 块）下，层塔不塌缩。 -/
theorem layer4_noncollapse :
    threeA ≠ threeB ∧ Nonempty (SpFourMorphism threeA threeB) :=
  ⟨threeA_ne_threeB, ⟨fourAB⟩⟩

end MUFPF
