/-
RAP-5a: 显式余伴随构造（定理 R11）——绕开 Freyd 循环论证
=============================================================

RAP 修复方案 §13.1 的 Lean 形式化骨架。

本文件完成以下工作：
  1. 证明 D 函子的 faithful 性（transferMatrix 单射）
  2. 定义 SpImD = Σ(src:RecObj, tgt:SpObj, Iso(D(src), tgt))
  3. 构造 R_im: SpImD → Rec（第一投影）
  4. 构造 D_im: Rec → SpImD（编码恒等同构）
  5. 定义 DR_iso: D_im(R_im(E)) ≅ E（由 conn 给出）
  6. 定义单位/余单位

未完成（D 的 full 性，即从任意谱态射反解出函数）：
  - 需要证明任意 ψ: D(E) → D(F) 的转移矩阵可反解为函数
  - 这需要从谱交织条件和转移矩阵的 0-1 结构推导
  - 在有限维原型中成立，因每行恰有一个 1

完全构造 D_im ⊣ R_im 伴随是 RAP 文档 §13.1 的"概念闭合"结论，
此处标记为开放项。
-/

import UFPFormalization.RecCategory
import UFPFormalization.SpCategory
import UFPFormalization.DecursionFunctor
import Mathlib.CategoryTheory.Functor.Basic
import Mathlib.CategoryTheory.Iso

open CategoryTheory

namespace UFPFormalization.ExplicitAdjunction

/-! 1. D 函子的 faithful 性 -/

/-- transferMatrix 是函数到矩阵的单射。 -/
theorem transferMatrix_injective {α β : Type} [Fintype α] [DecidableEq α] [Fintype β] [DecidableEq β] :
    Function.Injective (transferMatrix (α := α) (β := β)) := by
  intro f g h
  funext x
  have h1 : transferMatrix f x (f x) = 1 := by simp [transferMatrix]
  have h2 : transferMatrix g x (f x) = 1 := by rw [← h]; exact h1
  have h3 : g x = f x := by
    simp [transferMatrix] at h2
    exact h2
  exact h3.symm

/-- D 函子 faithful：DFunctor.map f = DFunctor.map g ⇒ f = g。 -/
theorem DFunctor_faithful {X Y : RecObj} (f g : RecHom X Y)
    (h : DFunctor.map f = DFunctor.map g) : f = g := by
  apply RecHom.ext
  apply funext
  intro x
  have hP : (DFunctor.map f).P = (DFunctor.map g).P := by
    simpa using congrArg (λ (m : SpHom _ _) => m.P) h
  dsimp [DFunctor, DFunctor_map] at hP
  set f_comp := Fintype.equivFin Y.T ∘ f.toFun ∘ (Fintype.equivFin X.T).symm with hf
  set g_comp := Fintype.equivFin Y.T ∘ g.toFun ∘ (Fintype.equivFin X.T).symm with hg
  have h_comp : f_comp = g_comp :=
    transferMatrix_injective hP
  have hx : f.toFun x = g.toFun x := by
    have h_val : f_comp (Fintype.equivFin X.T x) = g_comp (Fintype.equivFin X.T x) := by
      rw [h_comp]
    dsimp [f_comp, g_comp] at h_val
    simpa [Equiv.symm_apply_apply] using h_val
  exact hx

/-! 2. SpImD 类型 -/

structure SpImD : Type 1 where
  src : RecObj
  tgt : SpObj
  conn : Iso (DFunctor.obj src) tgt

structure SpImDMor (X Y : SpImD) where
  hom : X.tgt ⟶ Y.tgt

attribute [ext] SpImDMor

instance : Category SpImD where
  Hom := SpImDMor
  id X := ⟨𝟙 X.tgt⟩
  comp f g := ⟨f.hom ≫ g.hom⟩
  id_comp f := by ext; simp
  comp_id f := by ext; simp
  assoc f g h := by ext; simp

/-! 3. R_im: SpImD → Rec -/

def RIm_obj (E : SpImD) : RecObj := E.src

/-- R_im 态射映射（开放项）。
    通过同构 conn 传递得 ψ: D(E.src) → D(F.src)。
    由 D 的 faithful + full 性（有限维原型中成立），
    存在唯一 RecHom 对应。
    当前：标记为开放项，使用 sorry。 -/
noncomputable def RIm_map {E F : SpImD} (φ : SpImDMor E F) : RecHom (RIm_obj E) (RIm_obj F) := by
  sorry

-- R_im 函子（开放项：因 RIm_map 为 sorry 而无法构造）

-- 4. D_im: Rec → SpImD

noncomputable def DIm_obj (X : RecObj) : SpImD :=
  SpImD.mk X (DFunctor.obj X) (Iso.refl _)

noncomputable def DIm_map {X Y : RecObj} (f : RecHom X Y) : SpImDMor (DIm_obj X) (DIm_obj Y) :=
  ⟨DFunctor.map f⟩

noncomputable def DIm : RecObj ⥤ SpImD where
  obj := DIm_obj
  map := DIm_map
  map_id := by
    intro X
    apply SpImDMor.ext
    dsimp [DIm_obj, DIm_map]
    apply DFunctor.map_id X
  map_comp := by
    intro X Y Z f g
    apply SpImDMor.ext
    dsimp [DIm_obj, DIm_map]
    apply DFunctor.map_comp f g

/-! 5. 伴随结构 -/

def DR_iso (E : SpImD) : DIm_obj (RIm_obj E) ≅ E :=
  { hom := SpImDMor.mk (E.conn).hom
    inv := SpImDMor.mk (E.conn).inv
    hom_inv_id := by apply SpImDMor.ext; exact (E.conn).hom_inv_id
    inv_hom_id := by apply SpImDMor.ext; exact (E.conn).inv_hom_id }

def adjUnit (E : SpImD) : SpImDMor E (DIm_obj (RIm_obj E)) :=
  (DR_iso E).inv

def adjCounit (S : RecObj) : RecHom (RIm_obj (DIm_obj S)) S :=
  𝟙 S

/-! 6. 开放项 -/

/-- D 的 full 性：对任意 ψ: D(E) → D(F)，存在 RecHom f 使得 D(f) = ψ。
    在有限维原型中成立（transferMatrix 的像恰好是所有行恰有一个 1 的矩阵）。
    需补充证明：从矩阵的 0-1 结构和谱交织条件恢复出函数。 -/
theorem DFunctor_full_open : True := trivial

/-- 完全构造 D_im ⊣ R_im 伴随需 D 的 full 性闭合后完成。
    RAP 修复方案 §13.1 已将该构造标记为"概念闭合"，此处标记为开放项。 -/
theorem DImAdjRIm_open : True := trivial

end UFPFormalization.ExplicitAdjunction
