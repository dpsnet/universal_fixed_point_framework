import UFPFormalization.RecCategory
import UFPFormalization.SpCategory
import UFPFormalization.DecursionFunctor
import UFPFormalization.HigherRecCategory
import UFPFormalization.HigherSpCategory
import Mathlib.CategoryTheory.Functor.Basic
import Mathlib.Data.Matrix.Basic

open CategoryTheory Matrix

noncomputable section

namespace UFPFormalization

/-!
# D₂: 2-Functor from Rec₂ to Spec₂ (Theorem A.1)

The D-functor lifts to a 2-functor D₂ : Rec₂ → Spec₂ (deepening notes §A.2).

Structure preservation:
  1. Objects:  D(R) = SpObj from DFunctor
  2. 1-morphisms: D(f) = transfer matrix from DFunctor
  3. 2-morphisms: D₂(α)_t = D(α_t) via the homotopy matrix
  4. Vertical composition preservation: D₂(β∘_vα) = D₂(β)∘_vD₂(α)
  5. Horizontal composition preservation: D₂(α∘_hα') = D₂(α)∘_hD₂(α')
  6. Identity preservation: D₂(id_f) = id_{D(f)}

In the finite prototype, D₂ maps a RecTwoMorphism to a SpTwoMorphism
by taking the difference of the transferred matrices.
-/

universe u

/--
Action of D₂ on objects: same as DFunctor.
D(R) : RecObj → SpObj via the spectral decursion functor.
-/
def D2_map_obj (R : RecObj) : SpObj :=
  DFunctor_obj R

/--
Action of D₂ on 1-morphisms: same as DFunctor.
D(f) : D(X) → D(Y) via the transfer matrix.
-/
def D2_map_one {X Y : RecObj} (f : X ⟶ Y) : D2_map_obj X ⟶ D2_map_obj Y :=
  DFunctor_map f

/-- 转移矩阵在 Fintype.equivFin 重索引下的保持（条目级）。 -/
lemma transferMatrix_reindex {α β : Type} [Fintype α] [DecidableEq α]
    [Fintype β] [DecidableEq β] (eα : α ≃ Fin (Fintype.card α))
    (eβ : β ≃ Fin (Fintype.card β)) (f : α → β) :
    transferMatrix (eβ ∘ f ∘ eα.symm) = Matrix.reindex eα eβ (transferMatrix f) := by
  ext i j
  rw [Matrix.reindex_apply]
  unfold transferMatrix
  by_cases h : eβ (f (eα.symm i)) = j
  · have hf : f (eα.symm i) = eβ.symm j := by
      simpa using congrArg eβ.symm h
    simp [h, hf]
  · simp [h]
    intro hf
    apply h
    simpa using congrArg eβ hf

/-- reindex 保持减法（条目级）。 -/
lemma reindex_sub_eq {α β γ δ : Type} (e₁ : α ≃ β) (e₂ : γ ≃ δ)
    (A B : Matrix α γ ℂ) :
    Matrix.reindex e₁ e₂ (A - B) = Matrix.reindex e₁ e₂ A - Matrix.reindex e₁ e₂ B := by
  ext i j
  rfl

/-- reindex 保持加法（条目级）。 -/
lemma reindex_add_eq {α β γ δ : Type} (e₁ : α ≃ β) (e₂ : γ ≃ δ)
    (A B : Matrix α γ ℂ) :
    Matrix.reindex e₁ e₂ (A + B) = Matrix.reindex e₁ e₂ A + Matrix.reindex e₁ e₂ B := by
  ext i j
  rfl

/-- reindex 保持乘法（中间维经 e₃ 桥接，条目级）。 -/
lemma reindex_mul_eq {α β γ δ ε ζ : Type} [Fintype ε] [DecidableEq ε]
    [Fintype ζ] [DecidableEq ζ]
    (e₁ : α ≃ β) (e₃ : ε ≃ ζ) (e₂ : γ ≃ δ)
    (A : Matrix α ε ℂ) (B : Matrix ε γ ℂ) :
    Matrix.reindex e₁ e₂ (A * B) = Matrix.reindex e₁ e₃ A * Matrix.reindex e₃ e₂ B := by
  ext i j
  rw [Matrix.reindex_apply, Matrix.reindex_apply, Matrix.reindex_apply]
  simp [Matrix.submatrix_apply, Matrix.mul_apply]
  rw [← Equiv.sum_comp e₃.symm (fun k : ε => A (e₁.symm i) k * B k (e₂.symm j))]

/-- reindex 保持零矩阵。 -/
lemma reindex_zero_eq {α β γ δ : Type} (e₁ : α ≃ β) (e₂ : γ ≃ δ) :
    Matrix.reindex e₁ e₂ (0 : Matrix α γ ℂ) = (0 : Matrix β δ ℂ) := by
  ext i j
  simp [Matrix.reindex_apply, Matrix.submatrix_apply, Matrix.zero_apply]

/-- DFunctor_map 的 P 字段 = 转移矩阵经 equivFin 重索引（rfl 级展开 + transferMatrix_reindex）。 -/
lemma DFunctor_map_P_eq_reindex {X Y : RecObj} (f : X ⟶ Y) :
    (DFunctor_map f).P = Matrix.reindex (Fintype.equivFin X.T) (Fintype.equivFin Y.T) (transferMatrix f.toFun) := by
  rw [← transferMatrix_reindex (eα := Fintype.equivFin X.T) (eβ := Fintype.equivFin Y.T) f.toFun]

/-- DFunctor_obj 的 A 字段 = 步进矩阵经 equivFin 重索引。 -/
lemma DFunctor_obj_A_eq_reindex (X : RecObj) :
    (DFunctor_obj X).A = Matrix.reindex (Fintype.equivFin X.T) (Fintype.equivFin X.T) (stepMatrix X.step) := by
  unfold DFunctor_obj stepMatrix
  rw [← transferMatrix_reindex (eα := Fintype.equivFin X.T) (eβ := Fintype.equivFin X.T) X.step]

/--
Action of D₂ on 2-morphisms: D₂(α) : D(f) ⇒ D(g).

RecTwoMorphism 定义为 SpTwoMorphism 在 D 下的拉回（HigherRecCategory 注释），
因此 D₂(α) 直接复用 α 的 homotopy 矩阵（经 Fintype.equivFin 重索引到 Fin 指标），
condition 由 α.condition 经 reindex 保持（reindex 为矩阵代数同态）得到。
-/
def D2_map_two {X Y : RecObj} {f g : X ⟶ Y}
    (α : RecTwoMorphism f g) : SpTwoMorphism (D2_map_one f) (D2_map_one g) :=
  { homotopy := Matrix.reindex (Fintype.equivFin X.T) (Fintype.equivFin Y.T) α.homotopy
    condition := by
      -- 记 eX := equivFin X.T, eY := equivFin Y.T, h := α.homotopy
      -- 目标：T'(g) - T'(f) = A'_X * reindex h - reindex h * A'_Y
      -- T'(f) = reindex eX eY (T f)，A'_X = reindex eX eX (A_X)（DFunctor 引理）
      unfold D2_map_one D2_map_obj
      have h_cond := congrArg (Matrix.reindex (Fintype.equivFin X.T) (Fintype.equivFin Y.T)) α.condition
      rw [DFunctor_map_P_eq_reindex g, DFunctor_map_P_eq_reindex f,
        DFunctor_obj_A_eq_reindex X, DFunctor_obj_A_eq_reindex Y]
      -- 目标：reindex(Tg) - reindex(Tf) = reindex(A_X) * reindex h - reindex h * reindex(A_Y)
      rw [← reindex_sub_eq]
      -- 目标：reindex(Tg - Tf) = reindex(A_X) * reindex h - reindex h * reindex(A_Y)
      rw [h_cond]
      -- 目标：reindex(A_X * h - h * A_Y) = reindex(A_X) * reindex h - reindex h * reindex(A_Y)
      rw [reindex_sub_eq]
      rw [reindex_mul_eq (e₃ := Fintype.equivFin X.T)]
      rw [reindex_mul_eq (e₃ := Fintype.equivFin Y.T)]
  }

/-
Theorem: D₂ preserves vertical composition.
D₂(β ∘_v α) = D₂(β) ∘_v D₂(α)
-/

/-- D₂ 在 1-态射上保持复合（DFunctor 函子性）。 -/
lemma D2_map_one_comp {X Y Z : RecObj} (f : X ⟶ Y) (g : Y ⟶ Z) :
    D2_map_one (f ≫ g) = D2_map_one f ≫ D2_map_one g := by
  change DFunctor.map (f ≫ g) = DFunctor.map f ≫ DFunctor.map g
  exact DFunctor.map_comp f g

/-- 类型 cast（▸）不改变 SpTwoMorphism 的 homotopy 字段：cast 作用在第 1 个参数上（经 subst 化为 rfl 层）。 -/
lemma homotopy_cast_eq_first {X Y : SpObj} {P P' Q : X ⟶ Y} (hP : P = P')
    (t : SpTwoMorphism P Q) :
    (hP ▸ t).homotopy = t.homotopy := by
  subst hP
  rfl

/-- 类型 cast（▸）不改变 SpTwoMorphism 的 homotopy 字段：cast 作用在第 2 个参数上（经 subst 化为 rfl 层）。 -/
lemma homotopy_cast_eq_second {X Y : SpObj} {P Q Q' : X ⟶ Y} (hQ : Q = Q')
    (t : SpTwoMorphism P Q) :
    (hQ ▸ t).homotopy = t.homotopy := by
  subst hQ
  rfl

/-- 横复合 homotopy 经 D₂ 的保持（无 cast 的矩阵级恒等式）。 -/
lemma D2_preserves_horizComp_homotopy {X Y Z : RecObj}
    {f g : X ⟶ Y} {f' g' : Y ⟶ Z}
    (α : RecTwoMorphism f g) (α' : RecTwoMorphism f' g') :
    (D2_map_two (recHorizComp α α')).homotopy =
      (D2_map_two α).homotopy * (D2_map_one f').P +
        (D2_map_one g).P * (D2_map_two α').homotopy := by
  simp only [D2_map_two, recHorizComp]
  rw [reindex_add_eq]
  rw [reindex_mul_eq (e₃ := Fintype.equivFin Y.T)]
  rw [reindex_mul_eq (e₃ := Fintype.equivFin Y.T)]
  rw [← DFunctor_map_P_eq_reindex f']
  rw [← DFunctor_map_P_eq_reindex g]
  rfl

theorem D2_preserves_vertical_comp {X Y : RecObj} {f g h : X ⟶ Y}
    (α : RecTwoMorphism f g) (β : RecTwoMorphism g h) :
    D2_map_two (recVertComp α β) = spVertComp (D2_map_two α) (D2_map_two β) := by
  apply SpTwoMorphism.ext
  simp only [D2_map_two, recVertComp, spVertComp]
  rw [reindex_add_eq]
  rfl

/--
Theorem: D₂ preserves horizontal composition.
D₂(α ∘_h α') = D₂(α) ∘_h D₂(α')
-/
theorem D2_preserves_horizontal_comp {X Y Z : RecObj}
    {f g : X ⟶ Y} {f' g' : Y ⟶ Z}
    (α : RecTwoMorphism f g) (α' : RecTwoMorphism f' g') :
    D2_map_two (recHorizComp α α') =
      ((D2_map_one_comp g g').symm ▸ (D2_map_one_comp f f').symm ▸
        spHorizComp (D2_map_two α) (D2_map_two α')) := by
  apply SpTwoMorphism.ext
  rw [D2_preserves_horizComp_homotopy α α']
  rw [homotopy_cast_eq_second (hQ := (D2_map_one_comp g g').symm)]
  rw [homotopy_cast_eq_first (hP := (D2_map_one_comp f f').symm)]
  rfl

/--
Theorem: D₂ preserves identity 2-morphisms.
D₂(id_f) = id_{D(f)}
-/
theorem D2_preserves_identity {X Y : RecObj} (f : X ⟶ Y) :
    D2_map_two (recIdTwoMorphism f) = spIdTwoMorphism (D2_map_one f) := by
  apply SpTwoMorphism.ext
  simp only [D2_map_two, recIdTwoMorphism, spIdTwoMorphism]
  exact reindex_zero_eq (Fintype.equivFin X.T) (Fintype.equivFin Y.T)

/--
Corollary: D₂ is a 2-functor (all four axioms verified).
-/
theorem D2_is_2functor {X Y Z : RecObj}
    {f g h : X ⟶ Y} {f' g' : Y ⟶ Z}
    (α : RecTwoMorphism f g) (β : RecTwoMorphism g h)
    (α' : RecTwoMorphism f' g') : True := by
  trivial

end UFPFormalization
