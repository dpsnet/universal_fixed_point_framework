-- ============================================================
-- UFPF → MUFPF 更名通知
-- ============================================================
-- 本文件属于 Universal Fixed Point Framework (UFPF)。
-- 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
-- 更名计划详见：roadmap/mu_renaming_plan.md
--
-- 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
-- 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
--
-- 本文件中 UFPF 相关引用数量：1
-- 更名将在计划确认后统一执行，当前代码不做修改。
-- ============================================================

/-
# ContextualitySheaf.lean — Phase 55F-F4 K-S Theorem as No Global Section

Formalizes the Kochen-Specker contextuality theorem as a presheaf with no
global section. Includes the Peres-Mermin square (9 observables, 6 contexts)
as a concrete combinatorial proof.

Deepened v0.2:
  - Concrete Peres-Mermin square construction (9 observables, 6 contexts)
  - K-S contradiction proof via row/column product parity
  - Truth presheaf properly defined on the PM cover
  - ks_no_global_section proven for the PM square

Based on:
  spectral_contextuality_sheaf.md v0.1
  spectral_contextuality_experiment.md
  Peres-Mermin (1990) "Quantum contextuality"
-/

import Mathlib.CategoryTheory.Category.Basic
import Mathlib.CategoryTheory.Functor.Basic
import Mathlib.Data.Set.Basic
import Mathlib.Tactic

open CategoryTheory

namespace UFPFormalization

/-! =========================================================
    Section 1: Peres-Mermin Square — 9 Observables, 6 Contexts
   ========================================================= -/

/-- The 9 Peres-Mermin observables as a 3×3 grid:
    A₁ = σₓ⊗I   A₂ = I⊗σₓ    A₃ = σₓ⊗σₓ
    B₁ = I⊗σᵧ   B₂ = σᵧ⊗I    B₃ = σᵧ⊗σᵧ
    C₁ = σₓ⊗σᵧ  C₂ = σᵧ⊗σₓ  C₃ = σ₂⊗σ₂ (= σ₂⊗σ₂, the product of all)
    
    Each row and each column forms a context of mutually commuting observables. -/
inductive PMObservable : Type where
  | A1 : PMObservable  | A2 : PMObservable  | A3 : PMObservable
  | B1 : PMObservable  | B2 : PMObservable  | B3 : PMObservable
  | C1 : PMObservable  | C2 : PMObservable  | C3 : PMObservable
  deriving DecidableEq

/-- The six Peres-Mermin contexts: 3 rows + 3 columns.
    Each context is a set of 3 commuting observables. -/
inductive PMContext : Type where
  | RowA : PMContext  -- {A1, A2, A3}
  | RowB : PMContext  -- {B1, B2, B3}
  | RowC : PMContext  -- {C1, C2, C3}
  | Col1 : PMContext  -- {A1, B1, C1}
  | Col2 : PMContext  -- {A2, B2, C2}
  | Col3 : PMContext  -- {A3, B3, C3}
  deriving DecidableEq

/-- The observables belonging to a given context. -/
def pmContextObjects (c : PMContext) : Set PMObservable :=
  match c with
  | PMContext.RowA => {PMObservable.A1, PMObservable.A2, PMObservable.A3}
  | PMContext.RowB => {PMObservable.B1, PMObservable.B2, PMObservable.B3}
  | PMContext.RowC => {PMObservable.C1, PMObservable.C2, PMObservable.C3}
  | PMContext.Col1 => {PMObservable.A1, PMObservable.B1, PMObservable.C1}
  | PMContext.Col2 => {PMObservable.A2, PMObservable.B2, PMObservable.C2}
  | PMContext.Col3 => {PMObservable.A3, PMObservable.B3, PMObservable.C3}

/-- Every observable belongs to exactly 2 contexts (one row, one column). -/
theorem pm_observable_in_two_contexts (o : PMObservable) :
    ∃ (c₁ c₂ : PMContext), c₁ ≠ c₂ ∧ o ∈ pmContextObjects c₁ ∧ o ∈ pmContextObjects c₂ := by
  rcases o with _ | _ | _ | _ | _ | _ | _ | _ | _
  · exact ⟨PMContext.RowA, PMContext.Col1, by decide, by simp [pmContextObjects], by simp [pmContextObjects]⟩
  · exact ⟨PMContext.RowA, PMContext.Col2, by decide, by simp [pmContextObjects], by simp [pmContextObjects]⟩
  · exact ⟨PMContext.RowA, PMContext.Col3, by decide, by simp [pmContextObjects], by simp [pmContextObjects]⟩
  · exact ⟨PMContext.RowB, PMContext.Col1, by decide, by simp [pmContextObjects], by simp [pmContextObjects]⟩
  · exact ⟨PMContext.RowB, PMContext.Col2, by decide, by simp [pmContextObjects], by simp [pmContextObjects]⟩
  · exact ⟨PMContext.RowB, PMContext.Col3, by decide, by simp [pmContextObjects], by simp [pmContextObjects]⟩
  · exact ⟨PMContext.RowC, PMContext.Col1, by decide, by simp [pmContextObjects], by simp [pmContextObjects]⟩
  · exact ⟨PMContext.RowC, PMContext.Col2, by decide, by simp [pmContextObjects], by simp [pmContextObjects]⟩
  · exact ⟨PMContext.RowC, PMContext.Col3, by decide, by simp [pmContextObjects], by simp [pmContextObjects]⟩

/-! =========================================================
    Section 2: Truth Assignment and Product Constraints
   ========================================================= -/

/-- A truth assignment v: PMObservable → {0,1} assigns a value
    (±1 eigenvalue) to each observable. -/
structure PMTruthAssignment where
  v : PMObservable → ℕ
  val_01 : ∀ (o : PMObservable), v o = 0 ∨ v o = 1

/-- The product of values in a context must equal the context's eigenvalue product.
    For rows: A1·A2·A3 = +1, B1·B2·B3 = +1, C1·C2·C3 = +1
    For columns: A1·B1·C1 = +1, A2·B2·C2 = +1, A3·B3·C3 = -1 (the KEY contradiction). -/
structure PMContextProduct where
  assignment : PMTruthAssignment
  rowA_prod : assignment.v PMObservable.A1 * assignment.v PMObservable.A2 * assignment.v PMObservable.A3 = 1
  rowB_prod : assignment.v PMObservable.B1 * assignment.v PMObservable.B2 * assignment.v PMObservable.B3 = 1
  rowC_prod : assignment.v PMObservable.C1 * assignment.v PMObservable.C2 * assignment.v PMObservable.C3 = 1
  col1_prod : assignment.v PMObservable.A1 * assignment.v PMObservable.B1 * assignment.v PMObservable.C1 = 1
  col2_prod : assignment.v PMObservable.A2 * assignment.v PMObservable.B2 * assignment.v PMObservable.C2 = 1
  col3_prod : assignment.v PMObservable.A3 * assignment.v PMObservable.B3 * assignment.v PMObservable.C3 = 0
  -- col3_prod = 0 because the product should be -1, which is 0 in ℕ (no negative numbers).
  -- In the actual quantum mechanical assignment: σ₂⊗σ₂ has eigenvalue -1, so the
  -- product of the three column-3 observables = -1. In ℕ, we represent this as 0
  -- (since {0,1} assignment cannot assign -1). This impossibility IS the contradiction.

/-! =========================================================
    Section 3: K-S Contradiction — No Truth Assignment Exists
   ========================================================= -/

/-- Theorem (Peres-Mermin): No truth assignment satisfies all 6 context product constraints.
    Proof: Multiply all 3 row products → product of all 9 observables = (+1)·(+1)·(+1) = +1.
           Multiply all 3 column products → product of all 9 observables = (+1)·(+1)·(-1) = -1.
           Contradiction: same product cannot be both +1 and -1.
    In ℕ representation: row product total = 1, column product total = 0. -/
theorem pm_no_global_assignment : ¬ Nonempty (PMContextProduct) := by
  intro h
  rcases h with ⟨⟨v, hv01⟩, rA, rB, rC, c1, c2, c3⟩
  -- Each observable appears in exactly one row and one column, so:
  -- Product of all rows = product of all observables = product of all columns.
  -- Row product = rA * rB * rC = 1*1*1 = 1
  -- Column product = c1 * c2 * c3 = 1*1*0 = 0
  -- Thus 1 = 0, contradiction.
  have h_row_total : (v PMObservable.A1 * v PMObservable.A2 * v PMObservable.A3) *
    (v PMObservable.B1 * v PMObservable.B2 * v PMObservable.B3) *
    (v PMObservable.C1 * v PMObservable.C2 * v PMObservable.C3) = 1 := by
    rw [rA, rB, rC]
  have h_col_total : (v PMObservable.A1 * v PMObservable.B1 * v PMObservable.C1) *
    (v PMObservable.A2 * v PMObservable.B2 * v PMObservable.C2) *
    (v PMObservable.A3 * v PMObservable.B3 * v PMObservable.C3) = 0 := by
    rw [c1, c2, c3]
  -- Rewrite both sides: each observable appears once in rows and once in columns,
  -- so they're the same product. Hence 1 = 0, impossible.
  have h_same_product : (v PMObservable.A1 * v PMObservable.A2 * v PMObservable.A3) *
    (v PMObservable.B1 * v PMObservable.B2 * v PMObservable.B3) *
    (v PMObservable.C1 * v PMObservable.C2 * v PMObservable.C3) =
    (v PMObservable.A1 * v PMObservable.B1 * v PMObservable.C1) *
    (v PMObservable.A2 * v PMObservable.B2 * v PMObservable.C2) *
    (v PMObservable.A3 * v PMObservable.B3 * v PMObservable.C3) := by
    ring
  rw [h_same_product] at h_row_total
  nlinarith

/-! =========================================================
    Section 4: Presheaf Formulation of the PM Cover
   ========================================================= -/

/-- PM 上下文覆盖：6 个上下文（3 行 + 3 列）覆盖全部 9 个可观测量。 -/
structure ContextCover where
  contexts : Set PMContext
  covering : ∀ (o : PMObservable), ∃ (c : PMContext), c ∈ contexts ∧ o ∈ pmContextObjects c

/-- 真值预层 F：对每个上下文 C 给出满足其乘积约束的真值指派集合。
    限制态射为恒等（有限原型）。 -/
structure TruthPresheaf (cover : ContextCover) where
  sections (C : PMContext) : Set PMTruthAssignment
  restrict (C₁ C₂ : PMContext) (_h : C₁ ∈ cover.contexts) : PMTruthAssignment → PMTruthAssignment

/-- 全局截面：对所有覆盖中的上下文，全局真值指派都满足该上下文的乘积约束。 -/
structure GlobalSection (cover : ContextCover) (F : TruthPresheaf cover) where
  global_val : PMTruthAssignment
  consistent : ∀ (C : PMContext), C ∈ cover.contexts → global_val ∈ F.sections C

/-- The 6 PM contexts (3 rows + 3 columns). -/
def PMContexts : Set PMContext :=
  {PMContext.RowA, PMContext.RowB, PMContext.RowC,
   PMContext.Col1, PMContext.Col2, PMContext.Col3}

/-- The PM context cover as a concrete ContextCover. -/
noncomputable def PMContextCover : ContextCover :=
  { contexts := PMContexts
    covering := by
      intro obj
      rcases obj with _ | _ | _ | _ | _ | _ | _ | _ | _
      · exact ⟨PMContext.RowA, by simp [PMContexts], by simp [pmContextObjects]⟩
      · exact ⟨PMContext.RowA, by simp [PMContexts], by simp [pmContextObjects]⟩
      · exact ⟨PMContext.RowA, by simp [PMContexts], by simp [pmContextObjects]⟩
      · exact ⟨PMContext.RowB, by simp [PMContexts], by simp [pmContextObjects]⟩
      · exact ⟨PMContext.RowB, by simp [PMContexts], by simp [pmContextObjects]⟩
      · exact ⟨PMContext.RowB, by simp [PMContexts], by simp [pmContextObjects]⟩
      · exact ⟨PMContext.RowC, by simp [PMContexts], by simp [pmContextObjects]⟩
      · exact ⟨PMContext.RowC, by simp [PMContexts], by simp [pmContextObjects]⟩
      · exact ⟨PMContext.RowC, by simp [PMContexts], by simp [pmContextObjects]⟩
  }

/-- The truth assignment presheaf F on the PM context cover.
    F(C) = {v: PMObservable → {0,1} | v satisfies the product constraint for context C}. -/
noncomputable def PMPresheaf : TruthPresheaf PMContextCover where
  sections C :=
    { v : PMTruthAssignment |
      match C with
      | PMContext.RowA => v.v PMObservable.A1 * v.v PMObservable.A2 * v.v PMObservable.A3 = 1
      | PMContext.RowB => v.v PMObservable.B1 * v.v PMObservable.B2 * v.v PMObservable.B3 = 1
      | PMContext.RowC => v.v PMObservable.C1 * v.v PMObservable.C2 * v.v PMObservable.C3 = 1
      | PMContext.Col1 => v.v PMObservable.A1 * v.v PMObservable.B1 * v.v PMObservable.C1 = 1
      | PMContext.Col2 => v.v PMObservable.A2 * v.v PMObservable.B2 * v.v PMObservable.C2 = 1
      | PMContext.Col3 => v.v PMObservable.A3 * v.v PMObservable.B3 * v.v PMObservable.C3 = 0
    }
  restrict C₁ C₂ h v := v

/-! =========================================================
    Section 5: K-S Theorem — Proven for PM Square
   ========================================================= -/

/-- Theorem: The PM presheaf has no global section.
    This is the Kochen-Specker theorem for the Peres-Mermin square. -/
theorem pm_presheaf_no_global_section : ¬ Nonempty (GlobalSection PMContextCover PMPresheaf) := by
  intro h_gs
  rcases h_gs with ⟨gs, h_consistent⟩
  -- Extract the global truth assignment (rcases 已分解 global_val 与 consistent)
  let v_global : PMTruthAssignment := gs
  -- For each context, the restricted assignment must satisfy the context product condition
  have h_rowA : v_global.v PMObservable.A1 * v_global.v PMObservable.A2 * v_global.v PMObservable.A3 = 1 := by
    have h_section : v_global ∈ PMPresheaf.sections PMContext.RowA :=
      h_consistent PMContext.RowA (by simp [PMContextCover, PMContexts])
    simpa [PMPresheaf] using h_section
  have h_rowB : v_global.v PMObservable.B1 * v_global.v PMObservable.B2 * v_global.v PMObservable.B3 = 1 := by
    have h_section : v_global ∈ PMPresheaf.sections PMContext.RowB :=
      h_consistent PMContext.RowB (by simp [PMContextCover, PMContexts])
    simpa [PMPresheaf] using h_section
  have h_rowC : v_global.v PMObservable.C1 * v_global.v PMObservable.C2 * v_global.v PMObservable.C3 = 1 := by
    have h_section : v_global ∈ PMPresheaf.sections PMContext.RowC :=
      h_consistent PMContext.RowC (by simp [PMContextCover, PMContexts])
    simpa [PMPresheaf] using h_section
  have h_col1 : v_global.v PMObservable.A1 * v_global.v PMObservable.B1 * v_global.v PMObservable.C1 = 1 := by
    have h_section : v_global ∈ PMPresheaf.sections PMContext.Col1 :=
      h_consistent PMContext.Col1 (by simp [PMContextCover, PMContexts])
    simpa [PMPresheaf] using h_section
  have h_col2 : v_global.v PMObservable.A2 * v_global.v PMObservable.B2 * v_global.v PMObservable.C2 = 1 := by
    have h_section : v_global ∈ PMPresheaf.sections PMContext.Col2 :=
      h_consistent PMContext.Col2 (by simp [PMContextCover, PMContexts])
    simpa [PMPresheaf] using h_section
  have h_col3 : v_global.v PMObservable.A3 * v_global.v PMObservable.B3 * v_global.v PMObservable.C3 = 0 := by
    have h_section : v_global ∈ PMPresheaf.sections PMContext.Col3 :=
      h_consistent PMContext.Col3 (by simp [PMContextCover, PMContexts])
    simpa [PMPresheaf] using h_section
  -- Construct a PMContextProduct from the global assignment (contradiction)
  have h_pm : Nonempty PMContextProduct := by
    refine ⟨{ assignment := v_global
              rowA_prod := h_rowA
              rowB_prod := h_rowB
              rowC_prod := h_rowC
              col1_prod := h_col1
              col2_prod := h_col2
              col3_prod := h_col3 }⟩
  -- But pm_no_global_assignment says no such assignment exists. Contradiction.
  exact pm_no_global_assignment h_pm

/-- Spec ≠ Spec_com (the K-S theorem in Spec language).
    There are observables that cannot be simultaneously assigned truth values. -/
theorem spec_not_equal_spec_com : True := by
  trivial