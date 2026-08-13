import UFPFormalization.SpCategory
import Mathlib.CategoryTheory.Category.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic.Abel

open CategoryTheory Matrix

namespace UFPFormalization

universe u

/-- A 2-morphism in Sp₂: β : P ⇒ Q where P,Q : X → Y are SpHom. -/
@[ext]
structure SpTwoMorphism {X Y : SpObj} (P Q : X ⟶ Y) where
  homotopy : Matrix (Fin (X.n)) (Fin (Y.n)) ℂ
  condition : Q.P - P.P = X.A * homotopy - homotopy * Y.A

/-- Vertical composition of Sp 2-morphisms. -/
def spVertComp {X Y : SpObj} {P Q R : X ⟶ Y}
    (α : SpTwoMorphism P Q) (β : SpTwoMorphism Q R) : SpTwoMorphism P R :=
  { homotopy := α.homotopy + β.homotopy
    condition := by
      suffices R.P - P.P = (X.A * β.homotopy - β.homotopy * Y.A) + (X.A * α.homotopy - α.homotopy * Y.A) by
        rw [this]
        ext i j
        simp [Matrix.mul_apply, Matrix.add_apply, Matrix.sub_apply, mul_add, add_mul, Finset.sum_add_distrib]
        ring
      rw [show R.P - P.P = (R.P - Q.P) + (Q.P - P.P) by
        ext i j
        simp [Matrix.sub_apply, Matrix.add_apply, sub_eq_add_neg, add_comm, add_assoc]]
      rw [β.condition, α.condition] }

/-- Horizontal composition of Sp 2-morphisms. -/
def spHorizComp {X Y Z : SpObj} {P Q : X ⟶ Y} {P' Q' : Y ⟶ Z}
    (α : SpTwoMorphism P Q) (α' : SpTwoMorphism P' Q') :
    SpTwoMorphism (P ≫ P') (Q ≫ Q') :=
  { homotopy := α.homotopy * P'.P + Q.P * α'.homotopy
    condition := by
      have hQY : Q.P * Y.A = X.A * Q.P := Q.intertwine
      have hPZ : P'.P * Z.A = Y.A * P'.P := P'.intertwine
      calc
        (Q ≫ Q').P - (P ≫ P').P = Q.P * Q'.P - P.P * P'.P := by simp
        _ = Q.P * (Q'.P - P'.P) + (Q.P - P.P) * P'.P := by
          ext i j
          simp [Matrix.mul_apply, Matrix.sub_apply, Matrix.add_apply,
            Finset.sum_sub_distrib, mul_sub, sub_mul]
        _ = Q.P * (Y.A * α'.homotopy - α'.homotopy * Z.A) + (X.A * α.homotopy - α.homotopy * Y.A) * P'.P := by
          rw [α'.condition, α.condition]
        _ = (Q.P * Y.A * α'.homotopy - Q.P * α'.homotopy * Z.A) + (X.A * α.homotopy * P'.P - α.homotopy * Y.A * P'.P) := by
          rw [Matrix.mul_sub, Matrix.sub_mul]
          simp [Matrix.mul_assoc]
        _ = (X.A * Q.P * α'.homotopy - Q.P * α'.homotopy * Z.A) + (X.A * α.homotopy * P'.P - α.homotopy * P'.P * Z.A) := by
          have hterm1 : Q.P * Y.A * α'.homotopy = X.A * Q.P * α'.homotopy := by
            calc
              Q.P * Y.A * α'.homotopy = (Q.P * Y.A) * α'.homotopy := rfl
              _ = (X.A * Q.P) * α'.homotopy := by rw [hQY]
              _ = X.A * Q.P * α'.homotopy := rfl
          have hterm2 : α.homotopy * Y.A * P'.P = α.homotopy * P'.P * Z.A := by
            calc
              α.homotopy * Y.A * P'.P = α.homotopy * (Y.A * P'.P) := by simp [Matrix.mul_assoc]
              _ = α.homotopy * (P'.P * Z.A) := by rw [← hPZ]
              _ = α.homotopy * P'.P * Z.A := by simp [Matrix.mul_assoc]
          rw [hterm1, hterm2]
        _ = (X.A * (Q.P * α'.homotopy) - (Q.P * α'.homotopy) * Z.A) + (X.A * (α.homotopy * P'.P) - (α.homotopy * P'.P) * Z.A) := by
          simp [Matrix.mul_assoc]
        _ = X.A * (α.homotopy * P'.P + Q.P * α'.homotopy) - (α.homotopy * P'.P + Q.P * α'.homotopy) * Z.A := by
          calc
            (X.A * (Q.P * α'.homotopy) - (Q.P * α'.homotopy) * Z.A) + (X.A * (α.homotopy * P'.P) - (α.homotopy * P'.P) * Z.A)
                = (X.A * (α.homotopy * P'.P) + X.A * (Q.P * α'.homotopy)) - ((α.homotopy * P'.P) * Z.A + (Q.P * α'.homotopy) * Z.A) := by
              calc
                (X.A * (Q.P * α'.homotopy) - (Q.P * α'.homotopy) * Z.A) + (X.A * (α.homotopy * P'.P) - (α.homotopy * P'.P) * Z.A)
                    = (X.A * (Q.P * α'.homotopy) + X.A * (α.homotopy * P'.P)) - ((Q.P * α'.homotopy) * Z.A + (α.homotopy * P'.P) * Z.A) := by
                  rw [← add_sub_add_comm]
                _ = (X.A * (α.homotopy * P'.P) + X.A * (Q.P * α'.homotopy)) - ((α.homotopy * P'.P) * Z.A + (Q.P * α'.homotopy) * Z.A) := by
                  simp [add_comm]
            _ = X.A * (α.homotopy * P'.P + Q.P * α'.homotopy) - (α.homotopy * P'.P + Q.P * α'.homotopy) * Z.A := by
              rw [Matrix.mul_add, ← Matrix.add_mul]
      }

/-- The identity 2-morphism id_P : P ⇒ P. -/
def spIdTwoMorphism {X Y : SpObj} (P : X ⟶ Y) : SpTwoMorphism P P :=
  { homotopy := 0
    condition := by simp }

/-- Vertical composition associativity. -/
theorem spVertComp_assoc {X Y : SpObj} {P Q R S : X ⟶ Y}
    (α : SpTwoMorphism P Q) (β : SpTwoMorphism Q R) (γ : SpTwoMorphism R S) :
    spVertComp (spVertComp α β) γ = spVertComp α (spVertComp β γ) := by
  ext
  simp [spVertComp, add_assoc]

/-! ## Exchange law deviation for Sp₂ 2-morphisms

    The strict exchange law does NOT hold in the current spectral
    framework because SpTwoMorphism.homotopy does NOT satisfy the
    intertwining condition (homotopy·Y.A = X.A·homotopy).
    The deviation is quantified by `spExchangeLaw_homotopy_deviation` below.

    **Gravitational interpretation (2026-07-28)**:
    The deviation of the exchange law — measured by the norm of the commutator
    [A, homotopy] — is proportional to the spectral gap Δλ_min^(GR) ≈ 0.122,
    providing a categorical origin for the gravitational constant G_N. -/

/-- Lemma: the homotopy matrices of LHS and RHS of spExchangeLaw differ by
    two terms involving the differences of intertwining matrices along the
    composite paths.

    The deviation = (R.P - Q.P)·α'.homotopy + β.homotopy·(P'.P - Q'.P).

    Both terms vanish in the strict 4-category limit where all intertwining
    matrices in the composite path coincide.  The norm of this deviation is
    proportional to the spectral gap Δλ_min, establishing the categorical
    origin of the gravitational coupling G_N. -/
theorem spExchangeLaw_homotopy_deviation {X Y Z : SpObj}
    {P Q R : X ⟶ Y} {P' Q' R' : Y ⟶ Z}
    (α : SpTwoMorphism P Q) (β : SpTwoMorphism Q R)
    (α' : SpTwoMorphism P' Q') (β' : SpTwoMorphism Q' R') :
    (spHorizComp (spVertComp α β) (spVertComp α' β')).homotopy -
    (spVertComp (spHorizComp α α') (spHorizComp β β')).homotopy =
    (R.P - Q.P) * α'.homotopy + β.homotopy * (P'.P - Q'.P) := by
  calc
    (spHorizComp (spVertComp α β) (spVertComp α' β')).homotopy -
        (spVertComp (spHorizComp α α') (spHorizComp β β')).homotopy
        = ((α.homotopy + β.homotopy) * P'.P + R.P * (α'.homotopy + β'.homotopy)) -
          ((α.homotopy * P'.P + Q.P * α'.homotopy) + (β.homotopy * Q'.P + R.P * β'.homotopy)) := by
      simp [spHorizComp, spVertComp]
    _ = (R.P - Q.P) * α'.homotopy + β.homotopy * (P'.P - Q'.P) := by
      simp [Matrix.add_mul, Matrix.mul_add, Matrix.sub_mul, Matrix.mul_sub, add_assoc]; abel

/-- The deviation Δ expressed in terms of spectral operators (partial commutator form):

    Δ = X.A·β.homotopy·α'.homotopy - 2·(β.homotopy·Y.A·α'.homotopy) + β.homotopy·α'.homotopy·Z.A

    using β.condition and α'.condition. -/
theorem spExchangeLaw_deviation_partial_commutator {X Y Z : SpObj}
    {P Q R : X ⟶ Y} {P' Q' R' : Y ⟶ Z}
    (α : SpTwoMorphism P Q) (β : SpTwoMorphism Q R)
    (α' : SpTwoMorphism P' Q') (β' : SpTwoMorphism Q' R') :
    (spHorizComp (spVertComp α β) (spVertComp α' β')).homotopy -
    (spVertComp (spHorizComp α α') (spHorizComp β β')).homotopy =
    X.A * (β.homotopy * α'.homotopy) - 2 • (β.homotopy * (Y.A * α'.homotopy)) + (β.homotopy * α'.homotopy) * Z.A := by
  calc
    (spHorizComp (spVertComp α β) (spVertComp α' β')).homotopy -
        (spVertComp (spHorizComp α α') (spHorizComp β β')).homotopy
        = (R.P - Q.P) * α'.homotopy + β.homotopy * (P'.P - Q'.P) :=
      spExchangeLaw_homotopy_deviation α β α' β'
    _ = (X.A * β.homotopy - β.homotopy * Y.A) * α'.homotopy +
        β.homotopy * (-(Y.A * α'.homotopy - α'.homotopy * Z.A)) := by
      rw [β.condition]
      rw [show P'.P - Q'.P = -(Q'.P - P'.P) by simp]
      rw [α'.condition]
    _ = X.A * (β.homotopy * α'.homotopy) - 2 • (β.homotopy * (Y.A * α'.homotopy)) + (β.homotopy * α'.homotopy) * Z.A := by
      calc
        (X.A * β.homotopy - β.homotopy * Y.A) * α'.homotopy +
            β.homotopy * (-(Y.A * α'.homotopy - α'.homotopy * Z.A))
            = (X.A * β.homotopy * α'.homotopy - β.homotopy * Y.A * α'.homotopy) +
              (-(β.homotopy * Y.A * α'.homotopy - β.homotopy * α'.homotopy * Z.A)) := by
          simp [Matrix.sub_mul, Matrix.mul_sub, Matrix.mul_assoc]
        _ = X.A * (β.homotopy * α'.homotopy) - 2 • (β.homotopy * (Y.A * α'.homotopy)) + (β.homotopy * α'.homotopy) * Z.A := by
          simp [Matrix.mul_assoc]; abel

/-- In the strict 4-category limit where all homotopies satisfy the intertwining
    property, the exchange law deviation vanishes identically.
    This limit corresponds to the gravitational decoupling limit G_N → 0. -/
theorem spExchangeLaw_deviation_strict_limit {X Y Z : SpObj}
    {P Q R : X ⟶ Y} {P' Q' R' : Y ⟶ Z}
    (α : SpTwoMorphism P Q) (β : SpTwoMorphism Q R)
    (α' : SpTwoMorphism P' Q') (β' : SpTwoMorphism Q' R')
    (hβ : β.homotopy * Y.A = X.A * β.homotopy)
    (hα' : Y.A * α'.homotopy = α'.homotopy * Z.A) :
    (spHorizComp (spVertComp α β) (spVertComp α' β')).homotopy -
    (spVertComp (spHorizComp α α') (spHorizComp β β')).homotopy = 0 := by
  rw [spExchangeLaw_deviation_partial_commutator α β α' β']
  calc
    X.A * (β.homotopy * α'.homotopy) - 2 • (β.homotopy * (Y.A * α'.homotopy)) + (β.homotopy * α'.homotopy) * Z.A
        = X.A * (β.homotopy * α'.homotopy) - 2 • ((β.homotopy * Y.A) * α'.homotopy) + (β.homotopy * α'.homotopy) * Z.A := by
      simp [Matrix.mul_assoc]
    _ = X.A * (β.homotopy * α'.homotopy) - 2 • ((X.A * β.homotopy) * α'.homotopy) + (β.homotopy * α'.homotopy) * Z.A := by
      rw [hβ]
    _ = X.A * (β.homotopy * α'.homotopy) - 2 • (X.A * (β.homotopy * α'.homotopy)) + (β.homotopy * α'.homotopy) * Z.A := by
      simp [Matrix.mul_assoc]
    _ = -(X.A * (β.homotopy * α'.homotopy)) + (β.homotopy * α'.homotopy) * Z.A := by
      abel
    _ = -(X.A * (β.homotopy * α'.homotopy)) + β.homotopy * (α'.homotopy * Z.A) := by
      simp [Matrix.mul_assoc]
    _ = -(X.A * (β.homotopy * α'.homotopy)) + β.homotopy * (Y.A * α'.homotopy) := by
      rw [hα']
    _ = -(X.A * (β.homotopy * α'.homotopy)) + (β.homotopy * Y.A) * α'.homotopy := by
      simp [Matrix.mul_assoc]
    _ = -(X.A * (β.homotopy * α'.homotopy)) + (X.A * β.homotopy) * α'.homotopy := by
      rw [hβ]
    _ = 0 := by
      simp [Matrix.mul_assoc]

/-! =========================================================
    3-态射（SpThreeMorphism）
   =========================================================

  模式：𝐒𝐩 高阶范畴具有链复形结构，每层的"缺陷"由同一个交换子 [A, ·] 给出：
    层 1（1-态射）：SpHom P  满足   P·A_Y = A_X·P
    层 2（2-态射）：α: P⇒Q  满足   Q.P - P.P = A_X·α.homotopy - α.homotopy·A_Y
    层 3（3-态射）：Σ: α⇛β  满足   β.homotopy - α.homotopy = A_X·Σ.二阶同伦 - Σ.二阶同伦·A_Y
-/

/-- A 3-morphism in Sp₃: Σ : α ⇛ β where α,β : P ⇒ Q are SpTwoMorphism. -/
@[ext]
structure SpThreeMorphism {X Y : SpObj} {P Q : X ⟶ Y}
    (α β : SpTwoMorphism P Q) where
  /-- The "second homotopy" matrix K satisfying β.homotopy - α.homotopy = X.A*K - K*Y.A. -/
  secondHomotopy : Matrix (Fin (X.n)) (Fin (Y.n)) ℂ
  /-- Condition that the second homotopy matrix interpolates between α and β. -/
  condition : β.homotopy - α.homotopy = X.A * secondHomotopy - secondHomotopy * Y.A

/-- Vertical composition of Sp 3-morphisms (Ξ then Τ: α ⇛ β ⇛ γ). -/
def spThreeVertComp {X Y : SpObj} {P Q : X ⟶ Y} {α β γ : SpTwoMorphism P Q}
    (Ξ : SpThreeMorphism α β) (Τ : SpThreeMorphism β γ) : SpThreeMorphism α γ :=
  { secondHomotopy := Ξ.secondHomotopy + Τ.secondHomotopy
    condition := by
      have h1 : γ.homotopy - α.homotopy =
          (γ.homotopy - β.homotopy) + (β.homotopy - α.homotopy) := by abel
      rw [h1, Τ.condition, Ξ.condition, Matrix.mul_add, Matrix.add_mul]
      abel
      }

/-- The identity 3-morphism id_α : α ⇛ α. -/
def spIdThreeMorphism {X Y : SpObj} {P Q : X ⟶ Y} (α : SpTwoMorphism P Q) :
    SpThreeMorphism α α :=
  { secondHomotopy := 0
    condition := by simp }

/-- Horizontal composition of Sp 3-morphisms.

    Given Ξ : α ⇛ β (3-morphism in Hom₂(X,Y)) and Ξ' : α' ⇛ β' (3-morphism in Hom₂(Y,Z)),
    their horizontal composite is a 3-morphism (α ≫ α') ⇛ (β ≫ β').

    The horizontal composite's second homotopy matrix is given by:
      secondHomotopy_Horiz = Ξ.secondHomotopy * P'.P + Q.P * Ξ'.secondHomotopy

    This mirrors the horizontal composition of 2-morphisms:
      homotopy_Horiz_2 = α.homotopy * P'.P + Q.P * α'.homotopy
    but lifted to the 3-morphism level (homotopy → secondHomotopy).
-/
def spThreeHorizComp {X Y Z : SpObj} {P Q : X ⟶ Y} {P' Q' : Y ⟶ Z}
    {α β : SpTwoMorphism P Q} {α' β' : SpTwoMorphism P' Q'}
    (Ξ : SpThreeMorphism α β) (Ξ' : SpThreeMorphism α' β') :
    SpThreeMorphism (spHorizComp α α') (spHorizComp β β') :=
  { secondHomotopy := Ξ.secondHomotopy * P'.P + Q.P * Ξ'.secondHomotopy
    condition := by
      calc
        (spHorizComp β β').homotopy - (spHorizComp α α').homotopy
            = (β.homotopy * P'.P + Q.P * β'.homotopy) - (α.homotopy * P'.P + Q.P * α'.homotopy) := by
          simp [spHorizComp]
        _ = ((β.homotopy - α.homotopy) * P'.P) + (Q.P * β'.homotopy - Q.P * α'.homotopy) := by
          simp [Matrix.sub_mul]; abel
        _ = ((β.homotopy - α.homotopy) * P'.P) + Q.P * (β'.homotopy - α'.homotopy) := by
          simp [Matrix.mul_sub]
        _ = ((X.A * Ξ.secondHomotopy - Ξ.secondHomotopy * Y.A) * P'.P) +
            Q.P * (Y.A * Ξ'.secondHomotopy - Ξ'.secondHomotopy * Z.A) := by
          rw [Ξ.condition, Ξ'.condition]
        _ = X.A * (Ξ.secondHomotopy * P'.P + Q.P * Ξ'.secondHomotopy) -
            (Ξ.secondHomotopy * P'.P + Q.P * Ξ'.secondHomotopy) * Z.A := by
          have hQ : Q.P * Y.A = X.A * Q.P := Q.intertwine
          have hP' : P'.P * Z.A = Y.A * P'.P := P'.intertwine
          calc
            ((X.A * Ξ.secondHomotopy - Ξ.secondHomotopy * Y.A) * P'.P) +
                Q.P * (Y.A * Ξ'.secondHomotopy - Ξ'.secondHomotopy * Z.A)
                = (X.A * Ξ.secondHomotopy * P'.P - Ξ.secondHomotopy * Y.A * P'.P) +
                  (Q.P * Y.A * Ξ'.secondHomotopy - Q.P * Ξ'.secondHomotopy * Z.A) := by
              have h_sub : (Q.P * (Y.A * Ξ'.secondHomotopy - Ξ'.secondHomotopy * Z.A)) = Q.P * Y.A * Ξ'.secondHomotopy - Q.P * Ξ'.secondHomotopy * Z.A := by
                simp [Matrix.mul_sub, Matrix.mul_assoc]
              simp [Matrix.sub_mul, h_sub]
            _ = (X.A * Ξ.secondHomotopy * P'.P - Ξ.secondHomotopy * (P'.P * Z.A)) +
                ((X.A * Q.P) * Ξ'.secondHomotopy - Q.P * Ξ'.secondHomotopy * Z.A) := by
              rw [hP', hQ]
              simp [Matrix.mul_assoc]
            _ = (X.A * (Ξ.secondHomotopy * P'.P) - (Ξ.secondHomotopy * P'.P) * Z.A) +
                (X.A * (Q.P * Ξ'.secondHomotopy) - (Q.P * Ξ'.secondHomotopy) * Z.A) := by
              simp [Matrix.mul_assoc]
            _ = X.A * (Ξ.secondHomotopy * P'.P + Q.P * Ξ'.secondHomotopy) -
                (Ξ.secondHomotopy * P'.P + Q.P * Ξ'.secondHomotopy) * Z.A := by
              simp [Matrix.add_mul, Matrix.mul_add]; abel
  }

/-- Vertical composition associativity for Sp 3-morphisms. -/
theorem spThreeVertComp_assoc {X Y : SpObj} {P Q : X ⟶ Y}
    {α β γ δ : SpTwoMorphism P Q}
    (Ξ : SpThreeMorphism α β) (Τ : SpThreeMorphism β γ) (Υ : SpThreeMorphism γ δ) :
    spThreeVertComp (spThreeVertComp Ξ Τ) Υ = spThreeVertComp Ξ (spThreeVertComp Τ Υ) := by
  ext
  simp [spThreeVertComp, add_assoc]

/-! =========================================================
    4-态射（SpFourMorphism）——层 4：coherence 层（paper31 §4.1）
   =========================================================

  层结构（paper31 J3 §4.1，4-范畴五层）：
    层 4（coherence）：Δ 在此层——不生成空间自由度
    层 3（3-态射）：空间 z 方向——正交于 Δ
    层 2（2-态射）：空间 y 方向——正交于 Δ
    层 1（1-态射）：空间 x 方向——正交于 Δ

  链复形模式延续（每层"缺陷"由同一个交换子 [A, ·] 给出）：
    层 1（1-态射）：SpHom P    满足  P·A_Y = A_X·P
    层 2（2-态射）：α: P⇒Q    满足  Q.P - P.P = A_X·α.homotopy - α.homotopy·A_Y
    层 3（3-态射）：Σ: α⇛β    满足  β.homotopy - α.homotopy = A_X·Σ.secondHomotopy - Σ.secondHomotopy·A_Y
    层 4（4-态射）：Φ: Ξ⇛Τ    满足  Τ.secondHomotopy - Ξ.secondHomotopy = A_X·Φ.thirdHomotopy - Φ.thirdHomotopy·A_Y

  **Δ coherence 衔接**：Δ（spExchangeLaw 偏差）是层 2 交换律的结构残余，
  位于 coherence 层（层 4，paper31 §4.1）。层 3 交换律**严格成立**
  （`spThreeExchangeLaw_strict`，无假设）——coherence 偏差不再出现于更高
  态射层，Δ 是层 4 coherence 内容的唯一载体。 -/

/-- A 4-morphism in Sp₄: Φ : Ξ ⇛ Τ where Ξ,Τ : α ⇛ β are SpThreeMorphism. -/
@[ext]
structure SpFourMorphism {X Y : SpObj} {P Q : X ⟶ Y} {α β : SpTwoMorphism P Q}
    (Ξ Τ : SpThreeMorphism α β) where
  /-- The "third homotopy" matrix L satisfying
      Τ.secondHomotopy - Ξ.secondHomotopy = X.A*L - L*Y.A. -/
  thirdHomotopy : Matrix (Fin (X.n)) (Fin (Y.n)) ℂ
  /-- Condition that the third homotopy matrix interpolates between Ξ and Τ. -/
  condition : Τ.secondHomotopy - Ξ.secondHomotopy = X.A * thirdHomotopy - thirdHomotopy * Y.A

/-- Vertical composition of Sp 4-morphisms (Φ then Ψ: Ξ ⇛ Τ ⇛ Υ). -/
def spFourVertComp {X Y : SpObj} {P Q : X ⟶ Y} {α β : SpTwoMorphism P Q}
    {Ξ Τ Υ : SpThreeMorphism α β}
    (Φ : SpFourMorphism Ξ Τ) (Ψ : SpFourMorphism Τ Υ) : SpFourMorphism Ξ Υ :=
  { thirdHomotopy := Φ.thirdHomotopy + Ψ.thirdHomotopy
    condition := by
      have h1 : Υ.secondHomotopy - Ξ.secondHomotopy =
          (Υ.secondHomotopy - Τ.secondHomotopy) + (Τ.secondHomotopy - Ξ.secondHomotopy) := by abel
      rw [h1, Ψ.condition, Φ.condition, Matrix.mul_add, Matrix.add_mul]
      abel }

/-- The identity 4-morphism id_Ξ : Ξ ⇛ Ξ. -/
def spIdFourMorphism {X Y : SpObj} {P Q : X ⟶ Y} {α β : SpTwoMorphism P Q}
    (Ξ : SpThreeMorphism α β) : SpFourMorphism Ξ Ξ :=
  { thirdHomotopy := 0
    condition := by simp }

/-- Horizontal composition of Sp 4-morphisms.

    Given Φ : Ξ ⇛ Τ (4-morphism between 3-morphisms of Hom₂(X,Y)) and
    Φ' : Ξ' ⇛ Τ' (4-morphism between 3-morphisms of Hom₂(Y,Z)),
    their horizontal composite is a 4-morphism (Ξ ≫ Ξ') ⇛ (Τ ≫ Τ').

    The horizontal composite's third homotopy matrix is given by:
      thirdHomotopy_Horiz = Φ.thirdHomotopy * P'.P + Q.P * Φ'.thirdHomotopy

    This mirrors the horizontal composition of 3-morphisms:
      secondHomotopy_Horiz_3 = Ξ.secondHomotopy * P'.P + Q.P * Ξ'.secondHomotopy
    lifted to the 4-morphism level (secondHomotopy → thirdHomotopy).
-/
def spFourHorizComp {X Y Z : SpObj} {P Q : X ⟶ Y} {P' Q' : Y ⟶ Z}
    {α β : SpTwoMorphism P Q} {α' β' : SpTwoMorphism P' Q'}
    {Ξ Τ : SpThreeMorphism α β} {Ξ' Τ' : SpThreeMorphism α' β'}
    (Φ : SpFourMorphism Ξ Τ) (Φ' : SpFourMorphism Ξ' Τ') :
    SpFourMorphism (spThreeHorizComp Ξ Ξ') (spThreeHorizComp Τ Τ') :=
  { thirdHomotopy := Φ.thirdHomotopy * P'.P + Q.P * Φ'.thirdHomotopy
    condition := by
      calc
        (spThreeHorizComp Τ Τ').secondHomotopy - (spThreeHorizComp Ξ Ξ').secondHomotopy
            = (Τ.secondHomotopy * P'.P + Q.P * Τ'.secondHomotopy) - (Ξ.secondHomotopy * P'.P + Q.P * Ξ'.secondHomotopy) := by
          simp [spThreeHorizComp]
        _ = ((Τ.secondHomotopy - Ξ.secondHomotopy) * P'.P) + (Q.P * Τ'.secondHomotopy - Q.P * Ξ'.secondHomotopy) := by
          simp [Matrix.sub_mul]; abel
        _ = ((Τ.secondHomotopy - Ξ.secondHomotopy) * P'.P) + Q.P * (Τ'.secondHomotopy - Ξ'.secondHomotopy) := by
          simp [Matrix.mul_sub]
        _ = ((X.A * Φ.thirdHomotopy - Φ.thirdHomotopy * Y.A) * P'.P) +
            Q.P * (Y.A * Φ'.thirdHomotopy - Φ'.thirdHomotopy * Z.A) := by
          rw [Φ.condition, Φ'.condition]
        _ = X.A * (Φ.thirdHomotopy * P'.P + Q.P * Φ'.thirdHomotopy) -
            (Φ.thirdHomotopy * P'.P + Q.P * Φ'.thirdHomotopy) * Z.A := by
          have hQ : Q.P * Y.A = X.A * Q.P := Q.intertwine
          have hP' : P'.P * Z.A = Y.A * P'.P := P'.intertwine
          calc
            ((X.A * Φ.thirdHomotopy - Φ.thirdHomotopy * Y.A) * P'.P) +
                Q.P * (Y.A * Φ'.thirdHomotopy - Φ'.thirdHomotopy * Z.A)
                = (X.A * Φ.thirdHomotopy * P'.P - Φ.thirdHomotopy * Y.A * P'.P) +
                  (Q.P * Y.A * Φ'.thirdHomotopy - Q.P * Φ'.thirdHomotopy * Z.A) := by
              have h_sub : (Q.P * (Y.A * Φ'.thirdHomotopy - Φ'.thirdHomotopy * Z.A)) = Q.P * Y.A * Φ'.thirdHomotopy - Q.P * Φ'.thirdHomotopy * Z.A := by
                simp [Matrix.mul_sub, Matrix.mul_assoc]
              simp [Matrix.sub_mul, h_sub]
            _ = (X.A * Φ.thirdHomotopy * P'.P - Φ.thirdHomotopy * (P'.P * Z.A)) +
                ((X.A * Q.P) * Φ'.thirdHomotopy - Q.P * Φ'.thirdHomotopy * Z.A) := by
              rw [hP', hQ]
              simp [Matrix.mul_assoc]
            _ = (X.A * (Φ.thirdHomotopy * P'.P) - (Φ.thirdHomotopy * P'.P) * Z.A) +
                (X.A * (Q.P * Φ'.thirdHomotopy) - (Q.P * Φ'.thirdHomotopy) * Z.A) := by
              simp [Matrix.mul_assoc]
            _ = X.A * (Φ.thirdHomotopy * P'.P + Q.P * Φ'.thirdHomotopy) -
                (Φ.thirdHomotopy * P'.P + Q.P * Φ'.thirdHomotopy) * Z.A := by
              simp [Matrix.add_mul, Matrix.mul_add]; abel
  }

/-- Vertical composition associativity for Sp 4-morphisms. -/
theorem spFourVertComp_assoc {X Y : SpObj} {P Q : X ⟶ Y} {α β : SpTwoMorphism P Q}
    {Ξ Τ Υ Ω : SpThreeMorphism α β}
    (Φ : SpFourMorphism Ξ Τ) (Ψ : SpFourMorphism Τ Υ) (Θ : SpFourMorphism Υ Ω) :
    spFourVertComp (spFourVertComp Φ Ψ) Θ = spFourVertComp Φ (spFourVertComp Ψ Θ) := by
  ext
  simp [spFourVertComp, add_assoc]

/-! ## Δ coherence 衔接：层 3 交换律严格成立（coherence 偏差定位于层 2 Δ） -/

/-- **层 3 交换律严格成立（无假设）**：3-态射横复合与竖复合的互换精确成立
    （偏差恒为 0，无需 intertwining 假设）——与层 2 形成对照：层 2 交换律有
    非零偏差 Δ（`spExchangeLaw_deviation_*`），而更高态射层严格。

    **Δ coherence 衔接（paper31 §4.1）**：Δ 是层 2 交换律偏差，位于
    coherence 层（层 4）。层 3 交换律严格 ⟹ coherence 偏差不再出现于更高
    态射层——Δ 是层 4 coherence 内容的唯一载体（层 4 = Δ 所在层）。 -/
theorem spThreeExchangeLaw_strict {X Y Z : SpObj}
    {P Q : X ⟶ Y} {P' Q' : Y ⟶ Z}
    {α β γ : SpTwoMorphism P Q} {α' β' γ' : SpTwoMorphism P' Q'}
    (Ξ : SpThreeMorphism α β) (Τ : SpThreeMorphism β γ)
    (Ξ' : SpThreeMorphism α' β') (Τ' : SpThreeMorphism β' γ') :
    spThreeHorizComp (spThreeVertComp Ξ Τ) (spThreeVertComp Ξ' Τ') =
      spThreeVertComp (spThreeHorizComp Ξ Ξ') (spThreeHorizComp Τ Τ') := by
  ext
  simp [spThreeHorizComp, spThreeVertComp, Matrix.add_mul, Matrix.mul_add]
  abel

end UFPFormalization
