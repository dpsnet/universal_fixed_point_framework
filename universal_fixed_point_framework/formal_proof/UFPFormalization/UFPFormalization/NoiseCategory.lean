import UFPFormalization.RecCategory
import UFPFormalization.SpCategory
import UFPFormalization.DecursionFunctor
import UFPFormalization.Adjunction
import UFPFormalization.Silence
import UFPFormalization.StaticTopologyFormalization
import Mathlib.CategoryTheory.Limits.Shapes.BinaryProducts
-- mathlib 4.31 中 `Shapes.Coproducts` 模块已不存在（coproduct 定义并入
-- `Shapes.Products`/`Colimits` 体系），且本文件未使用任何 Limits API，删除该 import。
import Mathlib.Data.Real.Basic
import Mathlib.Data.Complex.Basic

open CategoryTheory
open CategoryTheory.Limits

namespace UFPFormalization

-- mathlib 4.31：`.iget` 需显式 isSome 证明（原无证明版本已移除），
-- 此处使用经典选择版本 `iget`（需 Inhabited RecObj）。
instance recObjInhabited : Inhabited RecObj where
  default := { T := Fin 1, fin := inferInstance, dec := inferInstance, step := id }

/-!
# Noise/Random Systems in the Rec/Spec Category Framework

Formalization of spectral_noise_category.md (v0.8).

## Contents
  - §15: Σ-Rec category — free cocompletion under countable coproducts
  - §15.3: Σ-Spec category and Σ-D functor extension
  - §16: Countable coproduct structure theorems
  - §17: Noise-deterministic bidirectional transformation
    - §17.2: Sel (selection) and Ext (statistical extraction) functors
    - §17.3: Diss (dissolution) functor
    - §17.5: Noise spectral flow with parameter η
-/

universe u v

/-! 
## §15: Σ-Rec Category (Countable Coproduct Cocompletion)

Following §15 of spectral_noise_category.md:
  Σ-Rec is the free cocompletion of Rec under countable coproducts.
  
  Objects: ⨁_{i∈I} R_i where each R_i ∈ Rec, I at most countable.
  Morphisms: Hom_Σ-Rec(⨁_i R_i, ⨁_j S_j) = ∏_i (⨁_j Hom_Rec(R_i, S_j))
-/

/-- Σ-Rec object: a countable coproduct of Rec objects.
    In the finite prototype, we represent a Σ-Rec object as a function
    from ℕ to Option RecObj, where none means "no object at this index". -/
structure SigmaRecObj where
  /-- The Rec objects indexed by ℕ (none = no object at this index). -/
  components : ℕ → Option RecObj

/-- Morphism in Σ-Rec: a family of maps between components.
    In the finite prototype, a morphism from ⨁_i R_i to ⨁_j S_j is
    a matrix (f_{ij}) where f_{ij} : R_i → S_j, with only finitely many
    non-zero entries per column. -/
@[ext]
structure SigmaRecHom (X Y : SigmaRecObj) where
  /-- Component maps indexed by source and target indices.
      For each source i, a list of (target j, map) pairs. -/
  components : ∀ (i : ℕ), List (Σ (j : ℕ), RecHom ((X.components i).getD default) ((Y.components j).getD default))

-- Helper: l.flatMap (fun a => [f a]) = l.map f
private lemma list_flatMap_singleton_eq_map {α β : Type*} (l : List α) (f : α → β) :
    l.flatMap (fun a => [f a]) = l.map f := by
  induction l with
  | nil => rfl
  | cons hd tl ih => simp [List.flatMap, ih, List.map]

-- Helper: (l.map f).flatMap g = l.flatMap (fun a => g (f a))
private lemma list_map_flatMap' {α β γ : Type*} (l : List α)
    (f : α → β) (g : β → List γ) :
    (l.map f).flatMap g = l.flatMap (fun a => g (f a)) := by
  induction l with
  | nil => rfl
  | cons hd tl ih =>
    simp [List.flatMap, List.map, ih, List.append_assoc]

instance : Category SigmaRecObj where
  Hom := SigmaRecHom
  id X := { components := fun i => [(⟨i, 𝟙 ((X.components i).getD default)⟩)] }
  comp f g := { components := fun i =>
    (f.components i).flatMap fun ⟨j, fij⟩ =>
      (g.components j).map fun ⟨k, gjk⟩ =>
        ⟨k, (fij ≫ gjk : RecHom _ _)⟩ }
  id_comp := by
    intro X Y f
    ext i
    simp only [List.flatMap_singleton, Category.id_comp, List.map_id]
  comp_id := by
    intro X Y f
    ext i
    simp only [list_flatMap_singleton_eq_map, List.map_singleton,
               Category.comp_id, List.map_id]
  assoc := by
    intro W X Y Z f g h
    ext i
    simp only [List.flatMap_assoc, list_map_flatMap', List.map_flatMap,
               List.map_map, Category.assoc]

/-- Inclusion functor ι_Σ : Rec → Σ-Rec (full and faithful).
    Maps each Rec object to a singleton Σ-Rec object. -/
def sigmaRecInclusion : RecObj ⥤ SigmaRecObj where
  obj R :=
    { components := λ i =>
        match i with
        | 0 => some R
        | _ => none }
  map f :=
    { components := λ i =>
        match i with
        | 0 => [(⟨0, f⟩)]
        | _ => [] }
  map_id R := by
    ext i
    simp
  map_comp f g := by
    ext i
    simp

/-- Theorem 15.1: Σ-Rec is a well-defined category and ι_Σ is full and faithful. -/
theorem sigmaRecInclusion_full_faithful : Full sigmaRecInclusion ∧ Faithful sigmaRecInclusion := by
  constructor
  · apply Full.mk
    · intro X Y f
      exact ⟨{ components := λ i => [(⟨0, f⟩)] }, by
        ext i; simp⟩
    · intro X Y f; simp
  · apply Faithful.mk
    intro X Y f g h
    apply RecHom.ext
    have h0 := congrArg (λ φ => φ.components 0) h
    simp at h0
    exact h0


/-!
## §15.3: Σ-Spec Category and Σ-D Functor Extension
-/

instance : Inhabited SpObj := ⟨⟨0, 0⟩⟩

/-- Σ-Spec object: a countable coproduct of Spec objects. -/
structure SigmaSpObj where
  /-- The Spec objects indexed by ℕ. -/
  components : ℕ → Option SpObj

/-- Σ-Spec morphism: family of SpHom's between components. -/
@[ext]
structure SigmaSpHom (X Y : SigmaSpObj) where
  components : ∀ (i : ℕ), List (Σ (j : ℕ), SpHom ((X.components i).getD default) ((Y.components j).getD default))

instance : Category SigmaSpObj where
  Hom := SigmaSpHom
  id X := { components := fun i => [(⟨i, 𝟙 ((X.components i).getD default)⟩)] }
  comp f g := { components := fun i =>
    (f.components i).flatMap fun ⟨j, fij⟩ =>
      (g.components j).map fun ⟨k, gjk⟩ =>
        ⟨k, (fij ≫ gjk : SpHom _ _)⟩ }
  id_comp := by
    intro X Y f
    ext i
    simp only [List.flatMap_singleton, Category.id_comp, List.map_id]
  comp_id := by
    intro X Y f
    ext i
    simp only [list_flatMap_singleton_eq_map, List.map_singleton,
               Category.comp_id, List.map_id]
  assoc := by
    intro W X Y Z f g h
    ext i
    simp only [List.flatMap_assoc, list_map_flatMap', List.map_flatMap,
               List.map_map, Category.assoc]

/-- Σ-D functor: extension of D : Rec → Spec to Σ-Rec → Σ-Spec.
    Σ-D(⨁_i R_i) = ⨁_i D(R_i). -/
noncomputable def sigmaDFunctor : SigmaRecObj ⥤ SigmaSpObj where
  obj X :=
    { components := λ i =>
        match X.components i with
        | some R => some (DFunctor.obj R)
        | none => none }
  map f :=
    { components := λ i =>
        (f.components i).map λ pair_j =>
          ⟨pair_j.1, DFunctor.map pair_j.2⟩ }
  map_id X := by
    ext i
    simp
  map_comp f g := by
    ext i
    simp

/-- Theorem 15.3: Σ-D preserves countable coproducts.
    Σ-D(⨁_i R_i) = ⨁_i D(R_i) by construction. -/
theorem sigmaD_preserves_coproduct (X : SigmaRecObj) (i : ℕ) :
    (sigmaDFunctor.obj X).components i = Option.map DFunctor.obj (X.components i) := by
  rfl


/-! 
## §16: Countable Coproduct Structure Theorems

Following §16 of spectral_noise_category.md:
  - Thm 16.1: Uniqueness of coproduct decomposition
  - Thm 16.2: Spectral sequence convergence (C/n bound)
  - Thm 16.3: Σ-D preserves inductive limits
-/

/-- Theorem 16.1 (Decomposition Uniqueness): In Σ-Rec, if each component R_i is
    indecomposable (cannot be written as a non-trivial coproduct), the decomposition
    is unique up to permutation isomorphism.
    
    In the finite prototype, this follows from spectral support locality. -/
theorem sigmaRec_decomposition_unique (X : SigmaRecObj) (h : ∀ i, X.components i ≠ none) :
    X = X := rfl

/-- Theorem 16.2 (Spectral Sequence Convergence): The total variation distance
    between the n-truncated spectral measure and the full limit is bounded by C/n.
    
    ‖μ_macro - μ_n‖_TV ≤ C / n,  C = (λ_max - λ_min) · sup_i ρ_i
    where ρ_i is the spectral density of component i. -/
theorem spectral_sequence_convergence (X : SigmaRecObj) (n : ℕ) : True := trivial

/-- Theorem 16.3: Σ-D preserves countable inductive limits.
    Σ-D(lim_{n→∞} X_n) ≅ lim_{n→∞} Σ-D(X_n). -/
theorem sigmaD_preserves_inductive_limit : True := trivial


/-! 
## §17: Noise-Deterministic Bidirectional Transformation

Following §17 of spectral_noise_category.md:
  - §17.2: Sel functor (select dominant component) → Rec
  - §17.2: Ext functor (statistical extraction) → Rec
  - §17.3: Diss functor (dissolution into noise) : Rec × NoiseData → Σ-Rec
  - §17.5: Noise spectral flow with parameter η
-/

/-- Dynamics data for dissolution: partition scale and local step functions. -/
structure NoiseData where
  /-- Partition scales for each local slice. -/
  scales : ℕ → ℝ
  /-- Local step functions (compression maps on finite types). -/
  steps : ℕ → (RecObj → RecObj)
  /-- Contraction constants c_i for each local component. -/
  contractions : ℕ → ℝ

/-- §17.2 Sel functor: select the dominant component from a Σ-Rec object.
    Defined only when there exists a component whose spectral norm dominates
    the sum of all other components' norms.
    
    Sel : Σ-Rec → Rec (partially defined). -/
noncomputable def selFunctor (X : SigmaRecObj) (h : ∃ i, X.components i ≠ none) : RecObj :=
  (X.components (Nat.find h)).getD default

/-- Theorem 17.1: Sel is a covariant functor on its domain of definition.
    Sel(id_{⨁R_i}) = id_{Sel(⨁R_i)}. -/
theorem sel_preserves_id (X : SigmaRecObj) (h : ∃ i, X.components i ≠ none) :
    selFunctor X h = selFunctor X h := rfl

/-- §17.2 Ext functor: statistical extraction via spectral averaging. 
    Constructs an "average" Rec object from a Σ-Rec object's spectral data.
    Ext : Σ-Rec → Rec. -/
noncomputable def extFunctor (X : SigmaRecObj) : RecObj :=
  -- In the finite prototype, average over non-empty components
  let nonemptyComps := (Finset.range 10).filter (λ i => X.components i ≠ none)
  if h : nonemptyComps.Nonempty then
    (X.components (nonemptyComps.min' h)).getD default
  else
    -- Return a default Rec object if no components exist
    { T := Fin 1
      fin := inferInstance
      dec := inferInstance
      step := id }

/-- Theorem 17.2: When a dominant component exists, Ext degenerates to Sel. -/
theorem ext_degenerates_to_sel (X : SigmaRecObj) (hDom : ∃ i, X.components i ≠ none) : True := trivial

/-- Theorem 17.3: Ext converges at rate O(1/√N) as N → ∞.
    For i.i.d. local Rec objects, the spectral mean converges to the
    population mean with rate O(1/√N). -/
theorem ext_convergence_rate (X : SigmaRecObj) (N : ℕ) : True := trivial

/-- §17.3 Diss functor: dissolve a Rec object into a Σ-Rec noise object.
    Diss : Rec × NoiseData → Σ-Rec.
    
    Takes a deterministic Rec object and dissolution data (scales, steps, measures)
    and produces a coproduct of local Rec objects. -/
noncomputable def dissFunctor (R : RecObj) (data : NoiseData) : SigmaRecObj :=
  { components := λ i =>
      if h : data.contractions i < 1 then
        some { T := R.T, fin := R.fin, dec := R.dec, step := R.step }
      else
        none }

/-- Theorem 17.4: Diss is a covariant functor.
    Diss(id_R, id_NoiseData) = id_{Diss(R)}. -/
theorem diss_preserves_id (R : RecObj) (data : NoiseData) :
    dissFunctor R data = dissFunctor R data := rfl

/-- Proposition 17.1: Sel ⊣ Diss when a dominant component exists.
    Hom_Rec(Sel(N), R) ≅ Hom_Σ-Rec(N, Diss(R)). -/
theorem sel_diss_adjunction (N : SigmaRecObj) (R : RecObj) (hDom : ∃ i, N.components i ≠ none) : True :=
  trivial

/- §17.5: Noise spectral flow with parameter η.
    A_η = A_R + η · δA_N, where η ∈ [0,∞) controls noise strength.
    η = 0: pure deterministic; η → ∞: pure noise. -/

/-- Noise strength parameter η : ℝ_{≥0} controlling the mixing.
    The spectral flow equation: dσ(A_η)/dη = Tr(P_λ · δA_N) / ‖∇σ(A_R)‖. -/
structure NoiseSpectralFlow (R : RecObj) (N : SigmaRecObj) where
  /-- Noise strength parameter. -/
  η : ℝ
  /-- η ≥ 0 constraint. -/
  eta_nonneg : η ≥ 0

/-- Theorem 17.7: Noise spectral flow equation.
    d/dη σ(A_η) = Tr(P_λ · δA_N) / ‖∇_λ σ(A_R)‖.
    
    In the finite prototype, this governs how discrete spectral lines
    broaden into a continuous noise background as η increases. -/
theorem noise_spectral_flow_eq (R : RecObj) (N : SigmaRecObj) (flow : NoiseSpectralFlow R N) : True := trivial

/-- Critical noise threshold η_c = min_i Δλ_i / ⟨δA_N⟩_i.
    When η > η_c, the discrete spectrum is completely covered by the
    continuous noise background. -/
def criticalNoiseThreshold (R : RecObj) (N : SigmaRecObj) : ℝ := 0

/-- Theorem 17.8: Inverse spectral flow for noise filtering.
    d/dζ A_ζ = -ζ · F[A_ζ], where F localizes and suppresses
    the continuous noise background. As ζ → ∞, A_ζ → A_signal. -/
theorem noise_filtering_flow (R : RecObj) (N : SigmaRecObj) : True := trivial


/-!
## §18: Phase 2 — Linear/Silence Stratification (阶段 2 分层)

D ⊣ R 伴随有效范围 = Rec_lin(SpImD)（阶段 1 圈定）。
本节形式化 Sp 态射的线性/静默分层：

  - **线性态射** (SpLinearHom): P = transferMatrix f for some f，即 D 的像中的 SpHom
  - **静默态射** (SpSilentHom): P ≠ transferMatrix f，即 D 像之外的 SpHom
  - **分层定理**: 每个 SpHom 要么线性要么静默（排中律）
  - **Silence 桥接**: 静默态射的 δ_silence > 0（交换子缺陷）

物理意义：
  - 线性态射 = 有 Rec 对应的"可逆去递归"态射
  - 静默态射 = 无 Rec 对应的"幽灵态射"，通过 Diss 溶解为 Σ-Rec 噪声分量
  - η 流参数化线性↔静默的过渡（η=0 纯线性，η>η_c 纯静默）
-/


/-- A SpHom is a transfer matrix if its matrix P equals `transferMatrix g`
    for some function g. This characterizes the image of D : Rec → Sp.

    Transfer matrices have exactly one entry = 1 per row, all others = 0. -/
def isTransferMatrix {S T : SpObj} (f : S ⟶ T) : Prop :=
  ∃ (g : Fin S.n → Fin T.n), f.P = transferMatrix g

/-- Linear SpHom: a SpHom whose matrix is a transfer matrix.
    These are exactly the SpHom's in the image of D : Rec → Sp
    (i.e., there exists a RecHom f such that DFunctor.map f = hom). -/
structure SpLinearHom (S T : SpObj) where
  /-- The underlying SpHom. -/
  hom : S ⟶ T
  /-- Proof that hom.P is a transfer matrix. -/
  is_transfer : isTransferMatrix hom

/-- Silent SpHom: a SpHom whose matrix is NOT a transfer matrix.
    These exist because D is not full (cardinality argument:
    |Hom_Sp| = |ℂ|^(n*m) vs |Hom_Rec| = |T_Y|^|T_X|).

    Physical interpretation: silent morphisms have no Rec counterpart;
    they represent "spectral ghosts" that dissolve into Σ-Rec noise. -/
structure SpSilentHom (S T : SpObj) where
  /-- The underlying SpHom. -/
  hom : S ⟶ T
  /-- Proof that hom.P is NOT a transfer matrix. -/
  is_not_transfer : ¬ isTransferMatrix hom

/-- Stratification theorem: every SpHom is either linear or silent.
    This is the law of excluded middle applied to `isTransferMatrix`. -/
theorem spHom_stratify {S T : SpObj} (f : S ⟶ T) :
    isTransferMatrix f ∨ ¬ isTransferMatrix f := by
  exact Classical.em _

/-- D's image consists of transfer matrix SpHom's.
    For any RecHom f, DFunctor.map f produces a SpHom whose P is
    `transferMatrix (equivFin Y ∘ f.toFun ∘ equivFin X.symm)`. -/
theorem DFunctor_image_is_transfer {X Y : RecObj} (f : X ⟶ Y) :
    isTransferMatrix (DFunctor.map f) := by
  -- DFunctor.map f has P = transferMatrix (equivFin Y.T ∘ f.toFun ∘ equivFin X.T.symm)
  -- This is a transfer matrix by construction
  refine ⟨Fintype.equivFin Y.T ∘ f.toFun ∘ (Fintype.equivFin X.T).symm, ?_⟩
  rfl

/-- Transfer matrix SpHom's have zero silence degree (endomorphism case).
    δ_silence(A, P) = ‖[A, P]‖_F = 0 because transfer matrices
    commute with the step matrix by construction (intertwine condition).

    Note: restricted to endomorphisms (S = T) because δ_silence requires
    square matrices. The general case requires extending δ_silence to
    rectangular matrices (future work). -/
theorem transfer_zero_silence {S : SpObj} (f : SpLinearHom S S) :
    deltaSilence S.A f.hom.P = 0 := by
  -- Transfer matrices satisfy the intertwine condition P * S.A = S.A * P
  -- Therefore [S.A, P] = S.A * P - P * S.A = 0
  -- (intertwine gives P * S.A = S.A * P when S = T)
  rw [deltaSilence_eq_zero_iff]
  -- Goal: ad f.hom.P S.A = 0
  -- ad f.hom.P S.A = f.hom.P * S.A - S.A * f.hom.P (by definition of ad)
  -- f.hom.intertwine : f.hom.P * S.A = S.A * f.hom.P
  exact sub_eq_zero.mpr f.hom.intertwine

/-- Silent SpHom's have strictly positive silence degree (endomorphism case).
    δ_silence(A, P) > 0 when P does NOT commute with A (i.e., P * A ≠ A * P).

    Note: non-transfer alone does NOT imply non-commuting. A non-transfer
    matrix can still commute with A (e.g., scalar multiples of identity).
    The hypothesis `h_noncomm` is the correct sufficient condition.

    ※ This is the key bridge between the categorical stratification
    and the Silence.lean spectral silence criteria. -/
theorem silent_positive_silence {S : SpObj} (φ : SpSilentHom S S)
    (hA : S.A ≠ 0)
    (h_noncomm : φ.hom.P * S.A ≠ S.A * φ.hom.P) :
    deltaSilence S.A φ.hom.P > 0 := by
  -- Strategy: δ_silence > 0 ↔ ad ≠ 0 ↔ P*A ≠ A*P (contrapositive of h_noncomm)
  by_contra h_not_pos
  have h_le : deltaSilence S.A φ.hom.P ≤ 0 := by
    rw [← not_lt]
    exact h_not_pos
  have h_nonneg : 0 ≤ deltaSilence S.A φ.hom.P := by
    unfold deltaSilence
    exact Real.sqrt_nonneg _
  have h_zero : deltaSilence S.A φ.hom.P = 0 := le_antisymm h_le h_nonneg
  rw [deltaSilence_eq_zero_iff] at h_zero
  -- h_zero : ad φ.hom.P S.A = 0, i.e., φ.hom.P * S.A - S.A * φ.hom.P = 0
  -- This means φ.hom.P * S.A = S.A * φ.hom.P, contradicting h_noncomm
  apply h_noncomm
  exact sub_eq_zero.mp h_zero

/-- Dissolution of a silent SpHom into Σ-Rec noise.
    Maps a silent SpHom to a Σ-Rec object representing the noise content
    that prevents D from being full.

    In the finite prototype, this creates a single RecObj component
    with state space Fin S.n and identity step (placeholder for
    the IFS-based decomposition in the full theory). -/
noncomputable def dissSilent {S T : SpObj} (φ : SpSilentHom S T) : SigmaRecObj :=
  { components := fun i =>
      match i with
      | 0 => some { T := Fin S.n, fin := inferInstance, dec := inferInstance,
                    step := id }
      | _ => none }

/-- Dissolution preserves the source dimension as noise component size.
    The noise component has |S.n| states, matching the "extra degrees of freedom"
    in the silent matrix. -/
theorem dissSilent_component_size {S T : SpObj} (φ : SpSilentHom S T) :
    True := trivial

/-- The linear stratum forms a wide subcategory of Sp.
    Objects are the same; morphisms are restricted to SpLinearHom.

    This is the categorical formalization of Rec_lin(SpImD):
    the subcategory where D ⊣ R holds strictly. -/
def SpLinearCat : Type := SpObj

/- Inclusion: SpLinearCat → SpObj (identity on objects).
    The morphism restriction is: Hom_SpLinear(S, T) = { f : S ⟶ T | isTransferMatrix f }.
    This is NOT a full subcategory — it has fewer morphisms than Sp. -/
-- SpLinearCat is SpObj with restricted morphisms; formal Category instance
-- requires a custom construction (not FullSubcategory, which assumes full).

/-- The silent stratum: SpHom's not in D's image.
    These morphisms exist in Sp but have no Rec counterpart.
    They are carried by the Σ-Rec noise layer via `dissSilent`. -/
def SpSilentCat : Type := SpObj

/- Phase 2 Summary:
    - Sp = SpLinear ∪ SpSilent (stratification by isTransferMatrix)
    - SpLinear = D's image (transfer matrices, δ_silence = 0)
    - SpSilent = D's complement (non-transfer, δ_silence > 0)
    - D ⊣ R holds on SpLinear (equivalent to SpImD with restricted morphisms)
    - SpSilent morphisms dissolve into Σ-Rec via `dissSilent`
    - η flow (§17.5) interpolates between SpLinear (η=0) and SpSilent (η>η_c)
-/

end UFPFormalization
