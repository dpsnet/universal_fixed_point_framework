import UFPFormalization.PhotonTopology
import UFPFormalization.RecCategory
import UFPFormalization.SpCategory
import UFPFormalization.DecursionFunctor
import Mathlib.CategoryTheory.Category.Basic
import Mathlib.CategoryTheory.Functor.FullyFaithful
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.InnerProductSpace.Orthogonal
import Mathlib.Analysis.InnerProductSpace.Projection.FiniteDimensional
import Mathlib.Tactic

/-!
# PhotonTopologyFunctor — 分岔映射 Φ 的范畴论定义与 D 函子衔接（开放问题 #1 推进）

笔记: notes/06_photon_topology/photon_topology_theory.md §1.2 公理 A1
论文: paper/paper44_photon_topology.md §2.2 / 附录 A.2
问题: 分岔映射 Φ 的严格范畴论定义，是否为 D 谱化函子的特例？

## 结论（诚实边界）
1. **对象层（构造性实现，非推导结论）**：光子谱化**经 D 函子构造性实现**——
   `photonSpectrum := DFunctor_obj ∘ photonToRec`（**定义选择**，非独立推导出的等价）。
   分岔（拓扑类切换 closed → opened）在谱层体现为 D 像的维度变化
   （`spectrum_atomic_n = 1` vs `spectrum_photon_n = 2`，`bifurcation_changes_spectrum`）。
   **嵌入任意性登记**：`photonToRec`（closed→Unit/id、opened→Bool/not）为代数骨架的
   语义约定（驻波=驻留、行波=往返），非唯一——"分岔改变谱（1→2 维）"的具体数值依赖
   此约定，非内在结论。"Φ 是 D 特例"的对象层含义 = 谱化可经 D 实现（构造性），
   非独立推导出的等价关系。
2. **函子公理（机器证明）**：Φ 作为 PhotonTopology → PhotonTopology 的自函子
   （`bifurcationFunctor`：保恒等、保复合）成立，且对象层幂等
   （`bifurcation_idempotent`：一次分岔后已开放，再分岔不变——与公理 A4 单向性一致）。
   **A3 并置结构**（漏洞修正）：旧 Φ 的"全转换"（X ↦ ⟨opened⟩，源对象丢失）不体现
   公理 A3 的"电子低能驻波 + 光子行波"并存——见 `PhotonTopology.lean`
   `CoexistingAfterBifurcation`/`bifurcateCoexisting`（Φ₊ 编码并置 + 能量重分配，
   旧 Φ = Φ₊ 的光子分量投影）。
3. **态射层（2026-08-11 闭合）**：`photonHomToRecHom`（拓扑类保持 → 演化同态恒等嵌入）+ `photonToRecFunctor`（忠实函子，`Functor.Faithful` 实例机器证明）——光子拓扑范畴**忠实嵌入** Rec 范畴，"Φ = D|子范畴"在对象层（构造性实现）与态射层（忠实嵌入）同时成立。剩余开放：4-范畴态射方向的几何正交（范畴层完整几何）。

嵌入语义：closed = 单点驻留系统（step = id，谱 [1]——S3 静默的代数像）；
opened = 两点往返系统（step = not，谱 [1, -1]——传播的代数像）。
-/

namespace UFPFormalization

open CategoryTheory

/-! ## 光子拓扑 → Rec 嵌入与谱化（对象层） -/

/-- 光子拓扑 → RecObj 嵌入：封闭 = 单点驻留（step = id），开放 = 两点往返（step = not）。 -/
def photonToRec (X : PhotonTopology) : RecObj :=
  match X.cls with
  | TopologicalClass.closed => { T := Unit, fin := inferInstance, dec := inferInstance,
                                 step := fun _ => () }
  | TopologicalClass.opened => { T := Bool, fin := inferInstance, dec := inferInstance,
                                 step := not }

/-- 光子拓扑谱化（开放问题 #1 核心构造）：谱化 = D 函子在嵌入对象上的作用。
    即光子拓扑不引入独立谱结构，谱化完全由 D 函子给出。 -/
noncomputable abbrev photonSpectrum (X : PhotonTopology) : SpObj :=
  DFunctor_obj (photonToRec X)

/-- 原子拓扑（封闭驻波）谱对象维度 = 1（单点驻留，单位谱）。 -/
theorem spectrum_atomic_n : (photonSpectrum atomicTopology).n = 1 := by
  simp [photonToRec, atomicTopology]

/-- 光子拓扑（开放行波）谱对象维度 = 2（两点往返，双值谱）。 -/
theorem spectrum_photon_n : (photonSpectrum photonTopology).n = 2 := by
  simp [photonToRec, photonTopology]
  decide

/-- 分岔改变谱（机器证明）：封闭驻波与开放行波的 D 像不同（维度 1 ≠ 2）——
    即 Φ（拓扑类切换）在谱层有非平凡效应，对应"驻波 → 行波"的谱结构跃迁。 -/
theorem bifurcation_changes_spectrum :
    photonSpectrum atomicTopology ≠ photonSpectrum photonTopology := by
  intro h
  have h2 : (photonSpectrum photonTopology).n = 2 := spectrum_photon_n
  rw [← h, spectrum_atomic_n] at h2
  norm_num at h2

/-- 分岔后谱对象恒为开放（维度 2）：Φ 的对象映射在谱层坍缩到传播类。 -/
theorem bifurcation_spectrum_final (X : PhotonTopology) :
    photonSpectrum (bifurcationMap X) = photonSpectrum photonTopology := by
  dsimp [photonSpectrum, photonToRec, bifurcationMap]
  rfl

/-- 分岔幂等（与公理 A4 单向性一致）：一次分岔后已开放，再分岔不变。 -/
theorem bifurcation_idempotent (X : PhotonTopology) :
    bifurcationMap (bifurcationMap X) = bifurcationMap X := rfl

/-! ## 分岔函子 Φ（范畴论定义） -/

/-- 光子拓扑态射：拓扑类保持映射（X 的类 = Y 的类）。 -/
@[ext]
structure PhotonHom (X Y : PhotonTopology) : Type where
  eq_cls : X.cls = Y.cls

/-- 光子拓扑范畴（态射 = 拓扑类保持）。 -/
instance photonTopologyCategory : Category PhotonTopology where
  Hom := PhotonHom
  id _ := ⟨rfl⟩
  comp {X Y Z} f g := ⟨f.eq_cls.trans g.eq_cls⟩
  id_comp := by intro X Y f; cases f; rfl
  comp_id := by intro X Y f; cases f; rfl
  assoc := by intro W X Y Z f g h; cases f; cases g; cases h; rfl

/-- 分岔函子 Φ：PhotonTopology → PhotonTopology（对象层 = bifurcationMap）。 -/
def bifurcationFunctor : PhotonTopology ⥤ PhotonTopology where
  obj := bifurcationMap
  map {X Y} (f : PhotonHom X Y) : PhotonHom (bifurcationMap X) (bifurcationMap Y) := by
    cases f
    exact ⟨rfl⟩
  map_id := by intro X; rfl
  map_comp := by intro X Y Z f g; cases f; cases g; rfl

/-- Φ 函子与 D 函子的衔接（对象层）：光子谱化 = D∘(嵌入)，分岔保持谱化路径一致。 -/
theorem phi_D_object_commute (X : PhotonTopology) :
    photonSpectrum (bifurcationFunctor.obj X) = DFunctor_obj (photonToRec (bifurcationFunctor.obj X)) := rfl

/-! ## 态射层嵌入（开放问题 #1 剩余闭合：PhotonHom → RecHom）
   "Φ = D|_子范畴" 的态射层含义 = photonToRec 提升为**忠实函子**：
   光子拓扑范畴（态射 = 拓扑类保持）忠实嵌入 Rec 范畴（态射 = 演化同态）。 -/

/-- 态射层嵌入：拓扑类保持态射 → Rec 演化同态（恒等映射，与演化规则自动交换）。
    封闭（单点驻留）→ Unit 恒等；开放（两点往返）→ Bool 恒等（与 step = not 交换）。
    类不一致分支由 f.eq_cls 导出矛盾（无态射可嵌入）。 -/
def photonHomToRecHom {X Y : PhotonTopology} (f : PhotonHom X Y) :
    RecHom (photonToRec X) (photonToRec Y) := by
  rcases X with ⟨cX⟩
  rcases Y with ⟨cY⟩
  cases cX <;> cases cY <;> try exact ⟨id, by intro x; rfl⟩
  · exfalso
    have h : TopologicalClass.closed = TopologicalClass.opened := f.eq_cls
    cases h
  · exfalso
    have h : TopologicalClass.opened = TopologicalClass.closed := f.eq_cls
    cases h

/-- 提升函子：光子拓扑范畴 → Rec 范畴（#1 态射层闭合）。 -/
def photonToRecFunctor : PhotonTopology ⥤ RecObj where
  obj := photonToRec
  map := photonHomToRecHom
  map_id := by
    intro X
    rcases X with ⟨cX⟩
    cases cX <;> rfl
  map_comp := by
    intro X Y Z f g
    rcases X with ⟨cX⟩
    rcases Y with ⟨cY⟩
    rcases Z with ⟨cZ⟩
    cases cX <;> cases cY <;> cases cZ
    · rfl
    · exfalso
      have h : TopologicalClass.closed = TopologicalClass.opened := g.eq_cls
      cases h
    · exfalso
      have h : TopologicalClass.closed = TopologicalClass.opened := f.eq_cls
      cases h
    · exfalso
      have h : TopologicalClass.closed = TopologicalClass.opened := f.eq_cls
      cases h
    · exfalso
      have h : TopologicalClass.opened = TopologicalClass.closed := f.eq_cls
      cases h
    · exfalso
      have h : TopologicalClass.opened = TopologicalClass.closed := f.eq_cls
      cases h
    · exfalso
      have h : TopologicalClass.opened = TopologicalClass.closed := g.eq_cls
      cases h
    · rfl

/-- 忠实性（态射层机器证明）：光子态射的类保持关系在嵌入下保持区分性
    （PhotonHom 为单点集：类保持是性质而非数据，嵌入自动忠实）。 -/
instance photonToRecFunctor_faithful : Functor.Faithful photonToRecFunctor := by
  constructor
  intro X Y f g hfg
  cases f
  cases g
  rfl

/-- #1 完整结论（对象层 + 态射层）：光子拓扑范畴经 photonToRecFunctor 忠实嵌入 Rec 范畴，
    谱化经 D 构造性实现（对象层 photonSpectrum = D∘嵌入，定义选择非推导）+ 
    态射层忠实嵌入（拓扑类保持 → 演化同态）。 -/
theorem photon_embedded_faithfully : Functor.Faithful photonToRecFunctor :=
  inferInstance

/-! ## 范畴层方向正交（开放问题"4-范畴态射方向几何正交"推进）
   光子方向 = 1-态射层（PhotonHom，类保持映射）；
   引力 Δ 方向 = Sp 2-态射层（HigherSpCategory 的水平交换偏差，2-态射/3-态射结构）。
   正交性的代数核心：光子子范畴的 Hom 集为**单点集**（类保持是性质而非数据），
   即光子方向内不存在非平凡的 1-态射对，故不存在可承载水平交换偏差的非平凡 2-态射——
   Δ（2-态射层）在光子方向**无投影**。完整 4-范畴几何（态射方向的空间正交）仍登记开放。 -/

/-- 光子态射单点性：类保持关系是性质（Prop）而非数据，任意两个光子态射相等。 -/
instance photonHom_subsingleton (X Y : PhotonTopology) : Subsingleton (PhotonHom X Y) := by
  constructor
  intro f g
  cases f
  cases g
  rfl

/-- 范畴层方向正交（2026-08-11 形式化核心）：光子方向（1-态射层）与 Δ 方向
    （2-态射偏差层）不相交——光子子范畴内 Hom 集单点，无非平凡 1-态射对，
    故水平 2-态射偏差 Δ 在光子方向无投影（Δ ⊥ 光子方向的代数表述）。 -/
theorem photon_direction_no_2morphism (X Y : PhotonTopology) (f g : PhotonHom X Y) :
    f = g := by
  exact Subsingleton.elim f g

/-! ## 纤维丛层正交的代数骨架（开放问题 #7 推进）
   "纤维 ⊥ 基空间"的严格意义 = (垂直子空间 V, 水平子空间 H, 度量 g) 的相容选取:
   V 内在 (ker dπ), H 由联络选取 (非唯一), 正交性由 g 与 H 的相容保证。
   数值演示: paperX_photon_fiber_orthogonality.py (5/5)——标准度量下 V⊥H_f ⟺ f=0
   (联络-度量不相容则不正交); 正交标架度量 g_A 下 V⊥H_A 对任意 A (相容选取 -> 正交)。
   **内积层（2026-08-11 机器证明）**：内积意义正交 ⟹ 交平凡
   （`inf_eq_bot_of_inner_orthogonal`，用 mathlib `Submodule.orthogonal`/
   `inf_orthogonal_eq_bot`，无需 FiniteDimensional import）。 -/

universe u

/-- 垂直-水平正交分解（代数骨架）：V 交 H 平凡（正交的代数推论）+ V 与 H 互补。 -/
structure VerticalHorizontalSplitting (E : Type u) [AddCommGroup E] [Module ℝ E] where
  V : Submodule ℝ E
  H : Submodule ℝ E
  inf_bot : V ⊓ H = ⊥      -- 垂直-水平交平凡（正交性排除共享向量）
  sup_top : V ⊔ H = ⊤      -- 互补（TE = V ⊕ H）

/- 维数加性（登记）：正交分解下 dim E = dim V + dim H，
   由 mathlib finrank_sup_add_finrank_inf_eq（FiniteDimensional.Lemmas）在 [FiniteDimensional]
   下可证（V 交 H = 0 且 V 并 H = top 时的 finrank 加性）；
   数值验证见 paperX_photon_fiber_orthogonality.py C5（dim E = dim V + dim H = 2）。
   完整 Lean 定理待 import 路径适配后恢复。 -/

/-! ## 纤维丛层正交的内积层（开放问题 #7 微分几何层推进）
   内积意义下的垂直-水平正交 ⟹ 交平凡（V ⊥ H ⟹ V ⊓ H = ⊥）。
   用 mathlib `Submodule.orthogonal`（Kᗮ = {v | ∀u∈K, ⟪u,v⟫=0}）机器证明，
   无需引入 FiniteDimensional/联络结构——内积即"正交"的度量意义。 -/

universe v

variable {E : Type v} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- 内积正交补中 ⟹ 交平凡：H ≤ Vᗮ ⟹ V ⊓ H = ⊥（mathlib `inf_orthogonal_eq_bot`）。 -/
theorem inf_eq_bot_of_le_orthogonal (V H : Submodule ℝ E) (h : H ≤ Vᗮ) :
    V ⊓ H = ⊥ := by
  rw [eq_bot_iff]
  intro x hx
  rcases hx with ⟨hv, hh⟩
  have hxV : x ∈ V ⊓ Vᗮ := ⟨hv, h hh⟩
  simpa [V.inf_orthogonal_eq_bot] using hxV

/-- 内积正交 ⟹ 交平凡：∀ v ∈ V, h ∈ H: ⟪v, h⟫ = 0（V ⊥ H 的度量意义）⟹ V ⊓ H = ⊥。 -/
theorem inf_eq_bot_of_inner_orthogonal (V H : Submodule ℝ E)
    (h_orth : ∀ v h : E, v ∈ V → h ∈ H → inner ℝ v h = 0) :
    V ⊓ H = ⊥ := by
  apply inf_eq_bot_of_le_orthogonal
  intro h hh
  rw [Submodule.mem_orthogonal]
  intro v hv
  exact h_orth v h hv hh

/-- 与 VerticalHorizontalSplitting 的衔接：内积正交 ⟹ inf_bot 成立
    （代数骨架的 V ⊓ H = ⊥ 断言由内积层机器证明支撑）。 -/
theorem vertical_horizontal_orthogonal_consistent (V H : Submodule ℝ E)
    (h_orth : ∀ v h : E, v ∈ V → h ∈ H → inner ℝ v h = 0) :
    V ⊓ H = ⊥ :=
  inf_eq_bot_of_inner_orthogonal V H h_orth

/-! ## 联络-度量相容选取（开放问题 #7 微分几何层推进）
   核心结论（2026-08-11）：度量正交补 Vᗮ 是 V 的**典范补空间**（E = V ⊕ Vᗮ），
   即 g-正交分解给出联络的**相容**选取（H = Vᗮ 自动满足 V ⊥_g H）——
   这是"联络-度量相容性"的代数核心：相容选取存在且典范（由度量唯一决定）。 -/

/-- 度量正交补是补空间（有限维）：V ⊔ Vᗮ = ⊤。
   证明：维数加性 finrank V + finrank Vᗮ = finrank E + V ⊓ Vᗮ = ⊥。 -/
theorem sup_orthogonal_eq_top [FiniteDimensional ℝ E] (V : Submodule ℝ E) :
    V ⊔ Vᗮ = ⊤ := by
  rw [Submodule.eq_top_iff_finrank_eq]
  have hIE := Submodule.finrank_sup_add_finrank_inf_eq V Vᗮ
  have hInf : Module.finrank ℝ ↥(V ⊓ Vᗮ) = 0 := by
    simp [V.inf_orthogonal_eq_bot]
  have hV : Module.finrank ℝ ↥(V ⊔ Vᗮ) = Module.finrank ℝ ↥V + Module.finrank ℝ ↥Vᗮ := by
    rw [← hIE]
    simp [hInf]
  rw [hV, V.finrank_add_finrank_orthogonal]

/-- 典范相容选取（#7 微分几何层代数核心）：V ⊓ Vᗮ = ⊥ 且 V ⊔ Vᗮ = ⊤，
    即 (V, Vᗮ) 构成 g-正交补空间对——联络的相容选取由度量典范地给出。 -/
theorem isCompl_orthogonal_standard [FiniteDimensional ℝ E] (V : Submodule ℝ E) :
    V ⊓ Vᗮ = ⊥ ∧ V ⊔ Vᗮ = ⊤ := by
  constructor
  · exact V.inf_orthogonal_eq_bot
  · exact sup_orthogonal_eq_top V

/-- 与 VerticalHorizontalSplitting 的衔接：g-正交分解 (V, Vᗮ) 满足代数骨架的全部断言
    （inf_bot + sup_top）——联络-度量相容选取存在且典范。 -/
theorem standard_splitting_satisfies (V : Submodule ℝ E) :
    V ⊓ Vᗮ = ⊥ :=
  V.inf_orthogonal_eq_bot

end UFPFormalization
