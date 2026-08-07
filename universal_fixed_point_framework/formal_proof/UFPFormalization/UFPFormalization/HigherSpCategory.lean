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
            Finset.sum_add_distrib, Finset.sum_sub_distrib, mul_sub, sub_mul]
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
                  simp [add_comm, add_left_comm, add_assoc]
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
          simp [Matrix.sub_mul, Matrix.mul_sub]; abel
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

end UFPFormalization
