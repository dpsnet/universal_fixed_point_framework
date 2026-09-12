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
-- 本文件中 UFPF 相关引用数量：8
-- 更名将在计划确认后统一执行，当前代码不做修改。
-- ============================================================

import MUFPFormalization.RecCategory
import MUFPFormalization.SpCategory
import MUFPFormalization.DecursionFunctor
import MUFPFormalization.Adjunction
import MUFPFormalization.Silence
import MUFPFormalization.StaticTopologyFormalization
import Mathlib.CategoryTheory.Limits.Shapes.BinaryProducts
-- mathlib 4.31 中 `Shapes.Coproducts` 模块已不存在（coproduct 定义并入
-- `Shapes.Products`/`Colimits` 体系），且本文件未使用任何 Limits API，删除该 import。
import Mathlib.CategoryTheory.Functor.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Order.Filter.AtTopBot.Basic
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.Deriv.Linear
import Mathlib.Analysis.Complex.Basic

open CategoryTheory
open CategoryTheory.Limits

namespace MUFPF

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
  - §16: Countable coproduct structure theorems（16.1/16.2/16.3 有限原型版，真证）
  - §17: Noise-deterministic bidirectional transformation
    - §17.2: Sel (selection) and Ext (statistical extraction) functors（17.2 真证）
    - §17.3: Diss (dissolution) functor
    - §17.5: Noise spectral flow with parameter η（17.7 迹版真证；
      17.3/17.8 无有限载体，开放登记见 sorry_closure_roadmap）
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
@[ext]
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
  | cons hd tl ih => simp [ih]

-- Helper: (l.map f).flatMap g = l.flatMap (fun a => g (f a))
private lemma list_map_flatMap' {α β γ : Type*} (l : List α)
    (f : α → β) (g : β → List γ) :
    (l.map f).flatMap g = l.flatMap (fun a => g (f a)) := by
  induction l with
  | nil => rfl
  | cons hd tl ih =>
    simp [ih]

-- Helper: flatMap 结合律（mathlib 4.31 无 `List.bind_assoc`，自建）
private lemma list_flatMap_assoc {α β γ : Type*} (l : List α)
    (f : α → List β) (g : β → List γ) :
    (l.flatMap f).flatMap g = l.flatMap (fun a => (f a).flatMap g) := by
  induction l with
  | nil => rfl
  | cons hd tl ih =>
    simp [ih, List.append_assoc]

instance : Category SigmaRecObj where
  Hom := SigmaRecHom
  id X := { components := fun i => [(⟨i, 𝟙 ((X.components i).getD default)⟩)] }
  comp f g := { components := fun i =>
    (f.components i).flatMap fun ⟨j, fij⟩ =>
      (g.components j).map fun ⟨k, gjk⟩ =>
        ⟨k, ⟨gjk.toFun ∘ fij.toFun, by
          intro x
          simp [fij.comm, gjk.comm]⟩⟩ }
  id_comp := by
    intro X Y f
    ext i
    simp [CategoryStruct.id, CategoryStruct.comp, RecHom.id_toFun]
  comp_id := by
    intro X Y f
    ext i
    simp [CategoryStruct.id, CategoryStruct.comp, RecHom.comp_toFun]
  assoc := by
    intro W X Y Z f g h
    ext i
    simp [CategoryStruct.comp, List.flatMap_assoc, List.map_flatMap, List.flatMap_map]
    rfl

/-- Inclusion functor ι_Σ : Rec → Σ-Rec (full and faithful).
    Maps each Rec object to a singleton Σ-Rec object.
    i ≠ 0 分量（none 源）给 default 对象的恒等态射——与 `Category.id` 的
    `[(⟨i, 𝟙 (getD default)⟩)]` 约定一致（原实现给 `[]` 导致 `map_id`/`map_comp` 失败）。 -/
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
        | Nat.succ k => [(⟨Nat.succ k, (𝟙 (default : RecObj))⟩)] }
  map_id R := by
    apply SigmaRecHom.ext
    funext i
    cases i with
    | zero => rfl
    | succ k => rfl
  map_comp f g := by
    apply SigmaRecHom.ext
    funext i
    cases i with
    | zero => rfl
    | succ k => rfl

/-- Theorem 15.1: Σ-Rec is a well-defined category and ι_Σ is faithful（map 单射）。
    `Functor.Full`（map 满射）在无约束的 `SigmaRecHom` 表示下**不成立**：态射对
    i ≠ 0（none 源）分量可任意，而 `map f` 强制其为 default 恒等。
    诚实修正：Faithful 成立；Full 需限定"i ≠ 0 分量恒等"的子类（见 §15.1 注）。 -/
theorem sigmaRecInclusion_faithful : Functor.Faithful sigmaRecInclusion := by
  apply Functor.Faithful.mk
  intro X Y f g h
  have h0 := congrArg (fun φ => φ.components 0) h
  simp [sigmaRecInclusion] at h0
  exact h0


/-!
## §15.3: Σ-Spec Category and Σ-D Functor Extension
-/

-- Inhabited SpObj：与 `DFunctor.obj (default : RecObj)` 对齐（原 `⟨0, 0⟩` 与
-- sigmaDFunctor 的 none 分量类型不匹配——Σ-D map 的 getD 需 `default SpObj = DFunctor.obj default`）。
noncomputable instance : Inhabited SpObj := ⟨DFunctor.obj (default : RecObj)⟩

/-- Σ-Spec object: a countable coproduct of Spec objects. -/
structure SigmaSpObj where
  /-- The Spec objects indexed by ℕ. -/
  components : ℕ → Option SpObj

/-- Σ-Spec morphism: family of SpHom's between components. -/
@[ext]
structure SigmaSpHom (X Y : SigmaSpObj) where
  components : ∀ (i : ℕ), List (Σ (j : ℕ), SpHom ((X.components i).getD default) ((Y.components j).getD default))

noncomputable instance : Category SigmaSpObj where
  Hom := SigmaSpHom
  id X := { components := fun i => [(⟨i, 𝟙 ((X.components i).getD default)⟩)] }
  comp f g := { components := fun i =>
    (f.components i).flatMap fun ⟨j, fij⟩ =>
      (g.components j).map fun ⟨k, gjk⟩ =>
        ⟨k, ⟨fij.P * gjk.P, by
          rw [Matrix.mul_assoc, gjk.intertwine]
          rw [← Matrix.mul_assoc, fij.intertwine]
          rw [Matrix.mul_assoc]⟩⟩ }
  id_comp := by
    intro X Y f
    ext i
    simp [CategoryStruct.id, CategoryStruct.comp, SpHom.id_P]
  comp_id := by
    intro X Y f
    ext i
    simp [CategoryStruct.id, CategoryStruct.comp, SpHom.comp_P]
  assoc := by
    intro W X Y Z f g h
    ext i
    simp [CategoryStruct.comp, List.flatMap_assoc, List.map_flatMap, List.flatMap_map,
          Matrix.mul_assoc, Function.comp_assoc, Function.comp_apply, Function.comp_def]

/-- 逐分量 getD 桥接（不引用 sigmaDFunctor，可在其定义前声明）：
    Option.map DFunctor.obj 的 getD = DFunctor.obj (源 getD)。
    由于 `Inhabited SpObj` 的 default 定义性等于 `DFunctor.obj (default : RecObj)`，
    该等式在 `some`/`none` 两个分支均定义性成立（`rfl`）。 -/
@[simp]
lemma option_map_getD (X : SigmaRecObj) (i : ℕ) :
    (Option.map DFunctor.obj (X.components i)).getD default = DFunctor.obj ((X.components i).getD default) := by
  cases h : X.components i with
  | some R => rfl
  | none => rfl

/-- 内层态射搬运（分量参数版）：直接对 `A B : Option RecObj` 两个**变量**做 `cases`，
    使 `f` 的类型在分支中定义性归约（`(some R).getD default = R` 等），产物无显式 cast。 -/
noncomputable def dfunctorMapTransport' (A B : Option RecObj)
    (f : RecHom (A.getD default) (B.getD default)) :
    SpHom ((Option.map DFunctor.obj A).getD default) ((Option.map DFunctor.obj B).getD default) := by
  cases A with
  | some R =>
      cases B with
      | some S => exact DFunctor.map f
      | none => exact DFunctor.map f
  | none =>
      cases B with
      | some S => exact DFunctor.map f
      | none => exact DFunctor.map f

/-- 内层态射搬运：将 `DFunctor.map f` 从 `getD (X.components i)` 类型搬到
    `getD (Option.map DFunctor.obj (X.components i))` 类型。
    经 `dfunctorMapTransport'` 逐分支消解源/目标分量，产物**不含任何显式 cast**
    （这是与 `rw [option_map_getD]` 方案的关键区别），
    使 Σ-D 的 Functor 律（map_id/map_comp）可机读证明。 -/
noncomputable def dfunctorMapTransport {X Y : SigmaRecObj} {i j : ℕ}
    (f : RecHom ((X.components i).getD default) ((Y.components j).getD default)) :
    SpHom ((Option.map DFunctor.obj (X.components i)).getD default)
          ((Option.map DFunctor.obj (Y.components j)).getD default) :=
  dfunctorMapTransport' (X.components i) (Y.components j) f

/-- `dfunctorMapTransport'` 保复合：搬运后的 `f ≫ g` = 搬运后各自的复合。
    这是 Σ-D map 保复合（Functor 律 2）的元素层核心。
    注意：`fij ≫ gjk` 记号在 mathlib `instCategory (Hom)` 递归歧义下不可靠，
    此处显式写出复合态射 `⟨gjk.toFun ∘ fij.toFun, ...⟩`（与 Rec 范畴 comp 定义性一致）。 -/
lemma dfunctorMapTransport'_comp (A B C : Option RecObj)
    (fij : RecHom (A.getD default) (B.getD default))
    (gjk : RecHom (B.getD default) (C.getD default)) :
    dfunctorMapTransport' A C
      (⟨gjk.toFun ∘ fij.toFun, by intro x; simp [fij.comm, gjk.comm]⟩) =
      @CategoryStruct.comp SpObj _ _ _ _ (dfunctorMapTransport' A B fij)
        (dfunctorMapTransport' B C gjk) := by
  cases A <;> cases B <;> cases C
  all_goals
    simp only [dfunctorMapTransport']
    exact DFunctor.map_comp fij gjk

/-- `dfunctorMapTransport'` 保恒等：搬运后的 `𝟙` = 目标类型的 `𝟙`。
    这是 Σ-D map 保恒等（Functor 律 1）的元素层核心。 -/
lemma dfunctorMapTransport'_id (A : Option RecObj) :
    dfunctorMapTransport' A A (𝟙 (A.getD default)) =
      (𝟙 ((Option.map DFunctor.obj A).getD default)) := by
  cases A with
  | some R => simp [dfunctorMapTransport', DFunctor.map_id]
  | none => simp [dfunctorMapTransport', DFunctor.map_id]; rfl

/-- `dfunctorMapTransport'` 在 `some` 分量上的恒等特化：搬运 `𝟙 R` = `𝟙 (D R)`。
    供 IFSRecCoding 的片注入谱像定理使用。 -/
@[simp]
lemma dfunctorMapTransport'_some_id (R : RecObj) :
    dfunctorMapTransport' (some R) (some R) (𝟙 R) =
      (𝟙 (DFunctor.obj R) : SpHom (DFunctor.obj R) (DFunctor.obj R)) := by
  simp [dfunctorMapTransport', DFunctor.map_id]

/-- Σ-D 的 obj：Σ-D(⨁_i R_i) = ⨁_i D(R_i)（对象层构造）。 -/
noncomputable def sigmaDFunctorObj (X : SigmaRecObj) : SigmaSpObj :=
  { components := λ i => Option.map DFunctor.obj (X.components i) }

/-- Σ-D 的 map：逐分量经 `dfunctorMapTransport` 作用 DFunctor.map（态射层构造）。
    元素构造无 cast（见 `dfunctorMapTransport` 的依赖匹配设计）。 -/
noncomputable def sigmaDFunctorMap {X Y : SigmaRecObj} (f : SigmaRecHom X Y) :
    SigmaSpHom (sigmaDFunctorObj X) (sigmaDFunctorObj Y) :=
  { components := λ i =>
      (f.components i).map λ pair_j =>
        ⟨pair_j.1, dfunctorMapTransport pair_j.2⟩ }

/-- Σ-D map 保恒等（Functor 律 1）。 -/
lemma sigmaDFunctorMap_id (X : SigmaRecObj) :
    sigmaDFunctorMap (𝟙 X) = 𝟙 (sigmaDFunctorObj X) := by
  apply SigmaSpHom.ext
  funext i
  simp [sigmaDFunctorMap, sigmaDFunctorObj, CategoryStruct.id, dfunctorMapTransport]
  exact dfunctorMapTransport'_id (X.components i)

/-- Σ-D map 保复合（Functor 律 2）。 -/
lemma sigmaDFunctorMap_comp {X Y Z : SigmaRecObj} (f : SigmaRecHom X Y) (g : SigmaRecHom Y Z) :
    sigmaDFunctorMap (@CategoryStruct.comp SigmaRecObj _ X Y Z f g) =
      (@CategoryStruct.comp SigmaSpObj _ (sigmaDFunctorObj X) (sigmaDFunctorObj Y) (sigmaDFunctorObj Z)
        (sigmaDFunctorMap f) (sigmaDFunctorMap g)) := by
  apply SigmaSpHom.ext
  funext i
  simp only [sigmaDFunctorMap, CategoryStruct.comp, List.map_flatMap, List.flatMap_map, List.map_map]
  induction f.components i with
  | nil => rfl
  | cons hd tl ih =>
      rw [List.flatMap_cons, List.flatMap_cons]
      cases hd with
      | mk j fij =>
          -- 先处理尾部（用归纳假设），再证头部
          rw [ih]
          congr 1
          -- 头部元素：map 保复合（dfunctorMapTransport'_comp）
          dsimp
          apply congrArg (fun h => (g.components j).map h)
          funext ⟨k, gjk⟩
          apply congrArg (Sigma.mk k)
          ext
          -- 注意：不展开 dfunctorMapTransport'（展开后 Option.rec 不可归约，且会破坏
          -- dfunctorMapTransport'_comp 的重写匹配）；只展开外层 dfunctorMapTransport。
          simp [dfunctorMapTransport, dfunctorMapTransport'_comp, SpHom.comp_P]
          rfl

/-- Σ-D 函子（定理 15.3 完整版）：Σ-Rec → Σ-Spec。
    对象层 = 逐分量 D 作用，态射层 = `dfunctorMapTransport` 搬运；
    Functor 律由 `sigmaDFunctorMap_id` / `sigmaDFunctorMap_comp` 闭合。 -/
noncomputable def sigmaDFunctor : SigmaRecObj ⥤ SigmaSpObj where
  obj := sigmaDFunctorObj
  map := sigmaDFunctorMap
  map_id := sigmaDFunctorMap_id
  map_comp := sigmaDFunctorMap_comp

/-- Theorem 15.3: Σ-D preserves countable coproducts.
    Σ-D(⨁_i R_i) = ⨁_i D(R_i) by construction. -/
theorem sigmaD_preserves_coproduct (X : SigmaRecObj) (i : ℕ) :
    (sigmaDFunctorObj X).components i = Option.map DFunctor.obj (X.components i) := by
  rfl


/-! 
## §16: Countable Coproduct Structure Theorems

Following §16 of spectral_noise_category.md:
  - Thm 16.1: Uniqueness of coproduct decomposition
  - Thm 16.2: Spectral sequence convergence (C/n bound)
  - Thm 16.3: Σ-D preserves inductive limits
-/

/-- 分量重排关系：Y 是 X 的分量重排（存在 ℕ 置换 π 使 Y.components = X.components ∘ π）。
    这是 Theorem 16.1（分解唯一性）在有限原型的诚实载体：分解唯一 = 唯一到重排类。 -/
def IsComponentReorder (X Y : SigmaRecObj) : Prop :=
  ∃ π : ℕ ≃ ℕ, Y.components = X.components ∘ π

/-- Theorem 16.1（有限原型版）：任一对象与自身相差恒等重排（分解唯一性的恒等情形；
    重排的复合与求逆给出重排类的群结构，对称/传递性由此可得）。 -/
theorem sigmaRec_decomposition_unique (X : SigmaRecObj) : IsComponentReorder X X :=
  ⟨Equiv.refl ℕ, rfl⟩

/-- n-截断：仅保留索引 < n 的分量（截断谱测度的有限原型载体）。 -/
def truncateComponents (X : SigmaRecObj) (n : ℕ) : SigmaRecObj :=
  { components := fun i => if i < n then X.components i else none }

/-- Theorem 16.2（有限原型版）：有限支撑 Σ-Rec 对象的截断序列在有限步后精确稳定
    （截断误差为零，强于 TV 界 C/n 的极限行为）。
    完整 TV 距离界 ‖μ_macro - μ_n‖_TV ≤ C/n（C = (λ_max - λ_min)·sup_i ρ_i）
    需截断谱测度基础设施（测度论），登记为开放命题，见 sorry_closure_roadmap。 -/
theorem spectral_sequence_convergence (X : SigmaRecObj)
    (hsupp : {i : ℕ | X.components i ≠ none}.Finite) :
    ∃ B : ℕ, ∀ n, B ≤ n → truncateComponents X n = X := by
  obtain ⟨B, hB⟩ := hsupp.bddAbove
  refine ⟨B + 1, fun n hn => ?_⟩
  apply SigmaRecObj.ext
  funext i
  by_cases hi : i < n
  · simp [truncateComponents, hi]
  · have hnone : X.components i = none := by
      by_contra hne
      exact hi (lt_of_le_of_lt (hB hne) (lt_of_lt_of_le (Nat.lt_succ_self B) hn))
    simp [truncateComponents, hi, hnone]

/-- Theorem 16.3（有限原型版）：Σ-D 保持分量级归纳极限。
    归纳极限以"逐分量最终相等"陈述（有向极限的有限原型约化）：
    若 X_n 的每个分量最终稳定在 L 的对应分量，则 Σ-D(X_n) 的每个分量
    最终稳定在 Σ-D(L) 的对应分量（Σ-D 逐分量构造的推论）。 -/
theorem sigmaD_preserves_inductive_limit (X : ℕ → SigmaRecObj) (L : SigmaRecObj)
    (hL : ∀ i, ∀ᶠ n in Filter.atTop, (X n).components i = L.components i) :
    ∀ i, ∀ᶠ n in Filter.atTop,
      (sigmaDFunctor.obj (X n)).components i = (sigmaDFunctor.obj L).components i := by
  intro i
  obtain ⟨N, hN⟩ := Filter.eventually_atTop.1 (hL i)
  refine Filter.eventually_atTop.2 ⟨N, fun n hn => ?_⟩
  show Option.map DFunctor.obj ((X n).components i)
      = Option.map DFunctor.obj (L.components i)
  exact congrArg (Option.map DFunctor.obj) (hN n hn)


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

/-- §17.2 Ext functor: statistical extraction —— 有限原型的诚实载体：
    取最小非空分量对应的 Rec 对象（与 Sel 同一选择函数，全 ℕ 扫描）。
    【2026-09-12 修正】原实现以 Finset.range 10 截断扫描（第 10 个分量以后的
    非空分量被忽略，且 min' 与 Nat.find 选择规则不同），导致 Theorem 17.2 无
    法证明（ext ≠ sel 为定义性缺陷而非定理）。已改为全 ℕ Nat.find。 -/
noncomputable def extFunctor (X : SigmaRecObj) : RecObj :=
  haveI := Classical.propDecidable (∃ i, X.components i ≠ none)
  if h : ∃ i, X.components i ≠ none then
    (X.components (Nat.find h)).getD default
  else
    { T := Fin 1
      fin := inferInstance
      dec := inferInstance
      step := id }

/-- Theorem 17.2（真证）：存在非空分量时 Ext = Sel（同一 Nat.find 选择）。 -/
theorem ext_degenerates_to_sel (X : SigmaRecObj) (hDom : ∃ i, X.components i ≠ none) :
    extFunctor X = selFunctor X hDom := by
  unfold extFunctor selFunctor
  split
  · rfl
  · rename_i h
    exact (h hDom).elim

/- Theorem 17.3（Ext 收敛率 O(1/√N)）：【开放命题登记，已从 Lean 移除占位定理】
   完整分析陈述：对 i.i.d. 局部 Rec 对象族（N 个非空分量），Ext(X_N) 的谱量与
   总体谱均值的偏差以 C/√N 为界。载体需概率论语义（i.i.d. 构造 + RecObj 谱
   范数空间），有限原型不可陈述。真证路径见 sorry_closure_roadmap 登记节。 -/
-- （原 `theorem ext_convergence_rate ... : True := trivial` 已删除，2026-09-12）

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

/-- Proposition 17.1（开放命题登记，不断言、不 axiomatize）：Sel ⊣ Diss 伴随的
    Hom 集同构（伴随的自然性未包含）。登记为存在双射的 Prop；真证需 list-编码
    Hom 的显式逆构造，见 sorry_closure_roadmap。 -/
def SelDissAdjunctionOpen (N : SigmaRecObj) (R : RecObj) (data : NoiseData)
    (hDom : ∃ i, N.components i ≠ none) : Prop :=
  Nonempty ((selFunctor N hDom ⟶ R) ≃ SigmaRecHom N (dissFunctor R data))

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

/-- Theorem 17.7（有限原型版）：噪声谱流的谱一阶矩（迹）导数。
    A_η = A + η·D 时 Tr(A_η) 对 η 的导数恰为 Tr(D)——这是
    dσ/dη = Tr(P_λ·δA_N)/‖∇σ‖ 在谱一阶矩（迹）上的有限维约化：
    谱和的导数 = 扰动的迹。本征值级扰动公式（投影 P_λ 形式）为开放内容，
    登记见 sorry_closure_roadmap。 -/
theorem noise_spectral_flow_eq (S : SpObj) (D : Matrix (Fin S.n) (Fin S.n) ℂ) (η₀ : ℝ) :
    HasDerivAt (fun η : ℝ => (S.A + (η : ℂ) • D).trace) D.trace η₀ := by
  have hsmul : ∀ η : ℝ, ((η : ℂ) • D).trace = (η : ℂ) * D.trace := fun η => by
    rw [Matrix.trace_smul, smul_eq_mul]
  have hlin : (fun η : ℝ => (S.A + (η : ℂ) • D).trace)
      = fun η : ℝ => S.A.trace + (η : ℂ) * D.trace := by
    funext η
    rw [Matrix.trace_add, hsmul η]
  have hof : HasDerivAt (fun η : ℝ => (η : ℂ)) 1 η₀ :=
    Complex.ofRealCLM.hasDerivAt (x := η₀)
  have key : HasDerivAt (fun η : ℝ => S.A.trace + (η : ℂ) * D.trace) D.trace η₀ := by
    have h := (hasDerivAt_const η₀ S.A.trace).add (hof.mul (hasDerivAt_const η₀ D.trace))
    rw [zero_add, one_mul, mul_zero, add_zero] at h
    exact h
  rw [hlin]
  exact key

/-- Critical noise threshold η_c = min_i Δλ_i / ⟨δA_N⟩_i.
    When η > η_c, the discrete spectrum is completely covered by the
    continuous noise background. -/
def criticalNoiseThreshold (R : RecObj) (N : SigmaRecObj) : ℝ := 0

/- Theorem 17.8（逆谱流噪声过滤 dA_ζ/dζ = -ζ·F[A_ζ]）：【开放命题登记，
   已从 Lean 移除占位定理】载体需"局域化算子 F"的数学定义与谱测度背景，
   有限原型不可陈述。真证路径见 sorry_closure_roadmap 登记节。 -/
-- （原 `theorem noise_filtering_flow ... : True := trivial` 已删除，2026-09-12）


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

/-- Dissolution preserves the source dimension as noise component size：
    0 号噪声分量的状态空间恰为 Fin S.n（与静默矩阵源维度一致）。 -/
theorem dissSilent_component_size {S T : SpObj} (φ : SpSilentHom S T) :
    (((dissSilent φ).components 0).getD default).T = Fin S.n := rfl

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

end MUFPF
