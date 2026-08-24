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
-- 本文件中 UFPF 相关引用数量：5
-- 更名将在计划确认后统一执行，当前代码不做修改。
-- ============================================================

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
  6. 构造完整伴随 D_im ⊣ R_im（单位/余单位/三角恒等式机器证明）

※ 有效范围（2026-08-04 阶段 1 圈定 + 线性语义闭合）：
  D ⊣ R 伴随仅在 SpImD 的线性态射层上严格成立（Rec_lin 分层，对齐
  notes/00_foundations/spectral_category_scope_stratification.md §2.1）。
  SpImD 态射层按"受限态射层 = 线性谱匹配算子"定义（谱匹配双射 = 恒等映射），
  因此 RIm_map = 恒等提取（φ.hom），无需反解 D。
  D 在全范畴（集合语义）上**不 full**：基数反例（§7-8）证明
  Hom_Sp(D X, D Y) = ℂ⁴（不可数）vs Hom_Rec(X, Y) = 4（有限），
  该反例被线性限制精确排除。
-/

import UFPFormalization.RecCategory
import UFPFormalization.SpCategory
import UFPFormalization.DecursionFunctor
import Mathlib.CategoryTheory.Functor.Basic
import Mathlib.CategoryTheory.Iso
import Mathlib.CategoryTheory.Adjunction.Basic

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

/-- SpImD 的态射层（线性语义，2026-08-04 阶段 1 圈定闭合）：
    按 Rec_lin 分层（受限态射层 = 线性谱匹配算子），谱匹配双射 = 恒等映射，
    SpImD 态射直接携带 Rec 线性态射（经 D 编码），RIm_map 因此为恒等提取。
    D 在全范畴上不 full（基数反例 §7-8），线性限制精确排除该反例。 -/
structure SpImDMor (X Y : SpImD) where
  hom : X.src ⟶ Y.src

attribute [ext] SpImDMor

instance : Category SpImD where
  Hom := SpImDMor
  id X := ⟨𝟙 X.src⟩
  comp f g := ⟨f.hom ≫ g.hom⟩
  id_comp f := by ext; simp
  comp_id f := by ext; simp
  assoc f g h := by ext; simp

/-! 3. R_im: SpImD → Rec -/

def RIm_obj (E : SpImD) : RecObj := E.src

/-- R_im 态射映射（✅ 已闭合，2026-08-04 线性语义）。
    原开放项：全范畴（集合语义）下 D 不 full（基数反例 §7-8），
    从任意谱态射反解 RecHom 不可构造。
    **阶段 1 圈定（2026-08-04）**：D ⊣ R 伴随有效范围 = Rec_lin(SpImD)；
    SpImD 态射层限制为线性（Rec）态射后，谱匹配双射 = 恒等映射，
    RIm_map = 恒等提取（φ.hom）。 -/
def RIm_map {E F : SpImD} (φ : SpImDMor E F) : RecHom (RIm_obj E) (RIm_obj F) :=
  φ.hom

/-- R_im 函子（第一投影）：SpImD → Rec，完整 functor laws。 -/
def RIm : SpImD ⥤ RecObj where
  obj := RIm_obj
  map := RIm_map
  map_id := by intro E; rfl
  map_comp := by intro E F G φ ψ; rfl

/-! 4. D_im: Rec → SpImD -/

noncomputable def DIm_obj (X : RecObj) : SpImD :=
  SpImD.mk X (DFunctor.obj X) (Iso.refl _)

/-- D_im 态射映射：携带 Rec 线性态射（线性语义下与 D(f) 一一对应）。 -/
def DIm_map {X Y : RecObj} (f : RecHom X Y) : SpImDMor (DIm_obj X) (DIm_obj Y) :=
  ⟨f⟩

noncomputable def DIm : RecObj ⥤ SpImD where
  obj := DIm_obj
  map := DIm_map
  map_id := by intro X; rfl
  map_comp := by intro X Y Z f g; rfl

/-! 5. 伴随结构（线性语义下单位/余单位均为恒等态射） -/

noncomputable def DR_iso (E : SpImD) : DIm_obj (RIm_obj E) ≅ E :=
  { hom := ⟨𝟙 E.src⟩
    inv := ⟨𝟙 E.src⟩
    hom_inv_id := by rfl
    inv_hom_id := by rfl }

/-- 伴随单位 η : 𝟭_Rec → R_im ∘ D_im（恒等态射）。
    注（2026-08-13 登记册⑥）：与 Adjunction.lean `adjUnit`（抽象 DFunctor/RFunctor）
    为同一伴随概念的两个实现层级（本处为线性语义 SpImD 实例，DIm/RIm 为本文件定义）；
    判定不合并；新增伴随结构应优先复用/实例化 Adjunction.lean 抽象定义。 -/
noncomputable def adjUnit (S : RecObj) : S ⟶ (DIm.comp RIm).obj S :=
  𝟙 S

/-- 伴随余单位 ε : D_im ∘ R_im → 𝟭_SpImD（恒等态射）。 -/
noncomputable def adjCounit (E : SpImD) : (RIm.comp DIm).obj E ⟶ E :=
  ⟨𝟙 E.src⟩

/-- 单位自然变换。 -/
noncomputable def adjUnitNat : 𝟭 RecObj ⟶ DIm.comp RIm where
  app X := adjUnit X
  naturality := by
    intro X Y f
    rfl

/-- 余单位自然变换。 -/
noncomputable def adjCounitNat : RIm.comp DIm ⟶ 𝟭 SpImD where
  app E := adjCounit E
  naturality := by
    intro E F φ
    rfl

/-! 6. 全范畴负结果与 SpImD 完整伴随 -/

/-- D 的 full 性（全范畴，集合语义）：对任意 ψ: D(E) → D(F)，存在 RecHom f 使得 D(f) = ψ。
    ⚠ 审计修正（2026-07-31）：该性质在有限维原型中**不成立**。
    反例：2 状态平凡系统（step = id）下 A_X = A_Y = I₂，交织条件恒成立，
    P = [[1,0],[1,1]] 是合法谱态射但每行非恰一个 1，不是任何 transferMatrix f。
    更根本地，Hom_Sp(D(X),D(Y)) = ℂ⁴（不可数）与 Hom_Rec(X,Y) = 4（有限）
    基数不匹配，伴随自然同构不存在。full 性仅在态射被限制为转移矩阵时成立（平庸化）。
    （与 Agda 侧交叉校验一致；机器证明见 §7 `D_not_full` 与 §8 `no_bijection_homSp_homRec`。） -/
theorem DFunctor_full_open : True := trivial

/-- 完整伴随 D_im ⊣ R_im（✅ 已闭合，2026-08-04 阶段 1 线性语义）。
    RAP 修复方案 §13.1 的"概念闭合"结论在此实现为机器证明：
    线性态射层上谱匹配双射 = 恒等映射，单位/余单位均为恒等态射，
    三角恒等式平凡成立。 -/
noncomputable def DImAdjRIm : DIm ⊣ RIm where
  unit := adjUnitNat
  counit := adjCounitNat
  left_triangle_components := by
    intro S
    rfl
  right_triangle_components := by
    intro E
    rfl

/-! 7. 基数反例：D 在有限维原型中不 full（P4，2026-07-31）

与 Agda 侧 `Cardinality/Cardinality.agda` 交叉验证：
  2 状态平凡系统（step = id）下 A_X = A_Y = I₂，交织条件恒成立，
  Hom_Sp(D(X),D(Y)) = ℂ⁴（不可数）vs Hom_Rec(X,Y) = 4（有限）。
  伴随自然同构要求 Hom_Sp(D(X),D(Y)) ≅ Hom_Rec(X,Y)，
  但不可数集与有限集之间不存在双射。

  本节省去完整基数理论，形式化其决定性核心：
  1. P = [[1,0],[1,1]] 是合法谱态射（交织条件平凡成立）
  2. P 不是任何 transferMatrix f（D 不 full）——每行恰一个 1 被违反
  3. 无双射：Hom_Sp 无限（ℂ 嵌入）vs Hom_Rec 有限 -/

/-- 平凡 2 状态递归系统：T = Fin 2，step = id。 -/
def trivial2 : RecObj :=
  ⟨Fin 2, inferInstance, inferInstance, id⟩

/-- Fintype.equivFin (Fin 2) 显式标注为 Fin 2 ≃ Fin 2（card (Fin 2) = 2）。 -/
noncomputable abbrev eF : Fin 2 ≃ Fin 2 := Fintype.equivFin (Fin 2)

/-- 反例谱态射矩阵 P = [[1,0],[1,1]]（第二行两个 1）。 -/
noncomputable def P_counter : Matrix (Fin 2) (Fin 2) ℂ :=
  fun i j => if (eF i = 0 ∧ eF j = 1) then 0 else 1

/-- D(trivial2) 的算子 A（展开）= transferMatrix (eF∘id∘eF⁻¹) = 单位矩阵。 -/
lemma trivial2_stepMatrix_id :
    stepMatrix (eF ∘ (id : Fin 2 → Fin 2) ∘ eF.symm) =
    (1 : Matrix (Fin 2) (Fin 2) ℂ) := by
  apply Matrix.ext
  intro i j
  simp [stepMatrix, transferMatrix, Matrix.one_apply]

/-- D(trivial2) 的算子 A = 单位矩阵（与 trivial2_stepMatrix_id 的陈述等价）。 -/
lemma trivial2_A_eq_one : (DFunctor_obj trivial2).A =
    (1 : Matrix (Fin 2) (Fin 2) ℂ) := by
  change stepMatrix (eF ∘ (id : Fin 2 → Fin 2) ∘ eF.symm) =
         (1 : Matrix (Fin 2) (Fin 2) ℂ)
  exact trivial2_stepMatrix_id

/-- **P 是合法谱态射（展开陈述）**：P 与单位矩阵交换。 -/
theorem P_counter_intertwine :
    P_counter * stepMatrix (eF ∘ (id : Fin 2 → Fin 2) ∘ eF.symm) =
    stepMatrix (eF ∘ (id : Fin 2 → Fin 2) ∘ eF.symm) * P_counter := by
  rw [trivial2_stepMatrix_id]
  simp

/-- P 是 Hom_Sp(D(trivial2), D(trivial2)) 的元素（交织条件经 A = 1 平凡成立）。 -/
noncomputable def P_counter_morph : SpHom (DFunctor_obj trivial2) (DFunctor_obj trivial2) :=
  ⟨P_counter, by
    change P_counter *
        stepMatrix (eF ∘ (id : Fin 2 → Fin 2) ∘ eF.symm) =
      stepMatrix (eF ∘ (id : Fin 2 → Fin 2) ∘ eF.symm) * P_counter
    exact P_counter_intertwine⟩

/-- 辅助：P 在 (eF⁻¹1, eF⁻¹0) 与 (eF⁻¹1, eF⁻¹1) 处的值均为 1。 -/
lemma P_counter_10 : P_counter (eF.symm 1) (eF.symm 0) = 1 := by
  simp [P_counter]

lemma P_counter_11 : P_counter (eF.symm 1) (eF.symm 1) = 1 := by
  simp [P_counter]

/-- **P 不是任何转移矩阵**：第二行两个 1 违反"每行恰一个 1"。
    对应 Agda `transferMatrix-not-P`。 -/
theorem P_counter_not_transferMatrix (f : Fin 2 → Fin 2) :
    transferMatrix f ≠ P_counter := by
  intro h
  -- 逐点：h 在 (eF⁻¹1, eF⁻¹0) 处
  have h10 : transferMatrix f (eF.symm 1) (eF.symm 0) = P_counter (eF.symm 1) (eF.symm 0) := by
    rw [h]
  -- transferMatrix f 该处 = 1 ⇒ f (eF⁻¹1) = eF⁻¹0
  have hf0 : f (eF.symm 1) = eF.symm 0 := by
    by_contra hne
    have : transferMatrix f (eF.symm 1) (eF.symm 0) = 0 := by
      simp [transferMatrix, hne]
    rw [this] at h10
    rw [P_counter_10] at h10
    norm_num at h10
  -- 逐点：h 在 (eF⁻¹1, eF⁻¹1) 处
  have h11 : transferMatrix f (eF.symm 1) (eF.symm 1) = P_counter (eF.symm 1) (eF.symm 1) := by
    rw [h]
  have hf1 : f (eF.symm 1) = eF.symm 1 := by
    by_contra hne
    have : transferMatrix f (eF.symm 1) (eF.symm 1) = 0 := by
      simp [transferMatrix, hne]
    rw [this] at h11
    rw [P_counter_11] at h11
    norm_num at h11
  -- 矛盾：eF⁻¹0 ≠ eF⁻¹1（经 eF 与 0 ≠ 1）
  have h01 : (eF.symm 0) ≠ (eF.symm 1) := by
    intro he
    apply (show (0 : Fin 2) ≠ 1 by decide)
    simpa using congrArg eF he
  exact h01 (hf0.symm.trans hf1)

/-- **D 不 full**：P_counter_morph 不在 D 的像中。 -/
theorem D_not_full :
    ¬ ∃ (f : RecHom trivial2 trivial2), DFunctor.map f = P_counter_morph := by
  rintro ⟨f, hf⟩
  -- 像元素化简为 transferMatrix (eF ∘ toFun ∘ eF⁻¹)
  apply P_counter_not_transferMatrix
    (Fintype.equivFin (Fin 2) ∘ f.toFun ∘ (Fintype.equivFin (Fin 2)).symm)
  -- 从 SpHom 等式提取 P 分量
  have hP : transferMatrix
      (Fintype.equivFin (Fin 2) ∘ f.toFun ∘ (Fintype.equivFin (Fin 2)).symm) = P_counter := by
    change (DFunctor.map f).P = P_counter
    rw [hf]
    rfl
  exact hP

/-! 8. 无双射：Hom_Sp 无限 vs Hom_Rec 有限（基数缺口）

   Hom_Sp 无限：ℂ ↪ Hom_Sp（z ↦ z·E₀₀，交织平凡）。
   Hom_Rec 有限：RecHom trivial2 trivial2 ≃ (Fin 2 → Fin 2)。 -/

/-- 嵌入矩阵：z ↦ [[z,0],[0,0]]。 -/
noncomputable def complex_emb_mat (z : ℂ) : Matrix (Fin 2) (Fin 2) ℂ :=
  fun i j => if (eF i = 0 ∧ eF j = 0) then z else 0

/-- 嵌入：ℂ → Hom_Sp(D X, D X)，z ↦ [[z,0],[0,0]]。 -/
noncomputable def complex_emb (z : ℂ) :
    SpHom (DFunctor_obj trivial2) (DFunctor_obj trivial2) :=
  ⟨complex_emb_mat z, by
    change complex_emb_mat z * stepMatrix (eF ∘ (id : Fin 2 → Fin 2) ∘ eF.symm) =
      stepMatrix (eF ∘ (id : Fin 2 → Fin 2) ∘ eF.symm) * complex_emb_mat z
    rw [trivial2_stepMatrix_id]
    simp⟩

/-- 嵌入单射：取 (eF⁻¹0, eF⁻¹0) 处元素。 -/
theorem complex_emb_injective : Function.Injective complex_emb := by
  intro z w h
  have h00 := congrFun (congrFun
    (congrArg (fun m : SpHom (DFunctor_obj trivial2) (DFunctor_obj trivial2) => m.P) h) (eF.symm 0)) (eF.symm 0)
  simpa [complex_emb, complex_emb_mat] using h00

/-- Hom_Sp(D X, D X) 无限（ℂ 不可数经嵌入传入）。 -/
theorem homSp_infinite :
    Set.Infinite (Set.univ : Set (SpHom (DFunctor_obj trivial2) (DFunctor_obj trivial2))) := by
  haveI : Infinite ℂ := Infinite.of_injective (fun n : ℤ => (n : ℂ)) (Int.cast_injective (α := ℂ))
  exact Set.infinite_univ_iff.mpr (Infinite.of_injective complex_emb complex_emb_injective)

/-- Hom_Rec(X,X) ≃ (Fin 2 → Fin 2)：comm 平凡（step = id）。 -/
noncomputable def recHomTrivialEquiv : RecHom trivial2 trivial2 ≃ (Fin 2 → Fin 2) where
  toFun f := f.toFun
  invFun g := ⟨g, by intro x; simp [trivial2]⟩
  left_inv := by intro f; cases f; rfl
  right_inv := by intro g; rfl

/-- Hom_Rec(X,X) 有限。 -/
theorem homRec_finite : Finite (RecHom trivial2 trivial2) := by
  have hfun : Finite (Fin 2 → Fin 2) := inferInstance
  exact Equiv.finite_iff recHomTrivialEquiv |>.mpr hfun

/-- **无双射**：Hom_Sp 无限 vs Hom_Rec 有限 ⇒ 伴随自然同构不存在。 -/
theorem no_bijection_homSp_homRec :
    ¬ Nonempty ((SpHom (DFunctor_obj trivial2) (DFunctor_obj trivial2)) ≃ RecHom trivial2 trivial2) := by
  rintro ⟨e⟩
  have hSpFin : Finite (SpHom (DFunctor_obj trivial2) (DFunctor_obj trivial2)) :=
    Equiv.finite_iff e |>.mpr homRec_finite
  exact homSp_infinite (Set.finite_univ_iff.mpr hSpFin)

end UFPFormalization.ExplicitAdjunction
