import UFPFormalization.PhotonTopology
import UFPFormalization.RecCategory
import UFPFormalization.SpCategory
import UFPFormalization.DecursionFunctor
import Mathlib.CategoryTheory.Category.Basic
import Mathlib.CategoryTheory.Functor.FullyFaithful
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.InnerProductSpace.Orthogonal
import Mathlib.Analysis.InnerProductSpace.Projection.FiniteDimensional
import Mathlib.LinearAlgebra.Projection
import Mathlib.Algebra.Group.Idempotent
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

/-- 典范相容选取（#7 微分几何层代数核心）：度量正交补给出 IsCompl 补空间对
    （V ⊓ Vᗮ = ⊥ 且 V ⊔ Vᗮ = ⊤）——联络的相容选取由度量典范地给出
    （mathlib `isCompl_orthogonal`，有限维下正交投影存在）。 -/
theorem isCompl_orthogonal_standard [FiniteDimensional ℝ E] (V : Submodule ℝ E) :
    IsCompl V Vᗮ := by
  haveI : V.HasOrthogonalProjection := inferInstance
  exact V.isCompl_orthogonal

/-- 与 VerticalHorizontalSplitting 的衔接：g-正交分解 (V, Vᗮ) 满足代数骨架的全部断言
    （inf_bot + sup_top）——联络-度量相容选取存在且典范。 -/
theorem standard_splitting_satisfies (V : Submodule ℝ E) :
    V ⊓ Vᗮ = ⊥ :=
  V.inf_orthogonal_eq_bot

/-! ## 联络 = 幂等投影（开放问题 #7 全微分几何层推进）
   联络（水平子空间选取）的**算子核心** = 幂等投影 P : E →ₗ E（P² = P）：
   沿 H 到 V 的投影满足 ker P = H（水平）、im P = V（垂直）、E = V ⊕ H。
   度量正交补 H = Vᗮ 给出**相容**联络算子（mathlib `LinearMap.projection`/
   `isIdempotentElem_projection`）——联络-度量相容选取的算子表述。 -/

/-- 联络算子的代数形式：幂等投影（P² = P）。 -/
abbrev LinearProjection (P : E →ₗ[ℝ] E) : Prop := IsIdempotentElem P

/-- 联络算子幂等性：沿度量正交补 Vᗮ 到 V 的投影是幂等的（P² = P，
    mathlib `Submodule.isIdempotentElem_projection`）——H = Vᗮ 给出相容联络。 -/
theorem projection_along_orthogonal_idempotent [FiniteDimensional ℝ E] (V : Submodule ℝ E) :
    LinearProjection (V.projection Vᗮ (isCompl_orthogonal_standard V)) :=
  Submodule.isIdempotentElem_projection (isCompl_orthogonal_standard V)

/-- 联络的水平子空间 = 度量正交补：ker P = Vᗮ
    （投影的核 = 沿之投影的子空间，`Submodule.projection_apply_eq_zero_iff`）——相容选取的算子表述。 -/
theorem projection_along_orthogonal_ker [FiniteDimensional ℝ E] (V : Submodule ℝ E) :
    LinearMap.ker (V.projection Vᗮ (isCompl_orthogonal_standard V)) = Vᗮ := by
  ext x
  rw [LinearMap.mem_ker]
  exact Submodule.projection_apply_eq_zero_iff (isCompl_orthogonal_standard V)

/-- 联络的垂直子空间 = V：im P = V（IsProj 唯一性：投影的像 = 其固定点子空间）。 -/
theorem projection_along_orthogonal_range [FiniteDimensional ℝ E] (V : Submodule ℝ E) :
    LinearMap.range (V.projection Vᗮ (isCompl_orthogonal_standard V)) = V := by
  let P : E →ₗ[ℝ] E := V.projection Vᗮ (isCompl_orthogonal_standard V)
  have hIdem : IsIdempotentElem P := by
    exact Submodule.isIdempotentElem_projection (isCompl_orthogonal_standard V)
  have hV : LinearMap.IsProj V P := by
    constructor
    · intro x
      rw [← Submodule.projection_eq_self_iff (isCompl_orthogonal_standard V)]
      change (P * P) x = P x
      exact DFunLike.congr_fun (show P * P = P from hIdem) x
    · intro x hx
      exact (Submodule.projection_eq_self_iff (isCompl_orthogonal_standard V) x).2 hx
  exact LinearMap.IsProj.range hV

/-- 联络-度量相容选取的算子闭合：P 是沿 Vᗮ 到 V 的幂等投影，
    即 E = V ⊕ Vᗮ（IsCompl）由投影算子 P 构造性给出（#7 联络层的代数核心）。 -/
theorem connection_metric_compatible [FiniteDimensional ℝ E] (V : Submodule ℝ E) :
    LinearProjection (V.projection Vᗮ (isCompl_orthogonal_standard V)) ∧
    LinearMap.ker (V.projection Vᗮ (isCompl_orthogonal_standard V)) = Vᗮ ∧
    LinearMap.range (V.projection Vᗮ (isCompl_orthogonal_standard V)) = V := by
  constructor
  · exact projection_along_orthogonal_idempotent V
  · constructor
    · exact projection_along_orthogonal_ker V
    · exact projection_along_orthogonal_range V

/-! ## 曲率层代数骨架（开放问题 #7 全微分几何层推进）
   全微分几何（联络形式/曲率/挠率的完整形式化）登记开放；
   本节给出**李代数值曲率的代数核心**：2-形式的反对称结构——
   曲率 Ω_ij = ∂_i ω_j - ∂_j ω_i + [ω_i, ω_j] 满足 Ω_ji = -Ω_ij，由
   (i) 外微分项的 (i,j) 反对称（差项交换变号）与
   (ii) 李括号反对称 [A,B] = -[B,A] 组合给出。
   数值验证见 paperX_photon_curvature.py。 -/

/-- 反对称化算子：skew(A) = A - A†，满足 skew(A)† = -skew(A)
    —— 曲率作为 2-形式的 (i,j) 指标反对称结构。 -/
theorem skew_antisymm {n : ℕ} (A : Matrix (Fin n) (Fin n) ℂ) :
    (A - A.conjTranspose).conjTranspose = -(A - A.conjTranspose) := by
  simp

/-- 李括号反对称：[A,B] = A·B - B·A 交换参数变号
    —— 曲率 ω∧ω = [ω,ω] 项的李代数值反对称（矩阵李代数）。 -/
theorem lie_bracket_antisymm {n : ℕ} (A B : Matrix (Fin n) (Fin n) ℂ) :
    A * B - B * A = -(B * A - A * B) := by
  abel

/-- 曲率反对称性（代数形式）：Ω_ij 与 Ω_ji 反号
    —— 由外微分项反对称（∂_i ω_j - ∂_j ω_i 交换变号）+ 李括号反对称组合。 -/
theorem curvature_antisymm {n : ℕ} (dwi dwj Ai Aj : Matrix (Fin n) (Fin n) ℂ) :
    (dwi - dwj + (Ai * Aj - Aj * Ai)) =
    - (dwj - dwi + (Aj * Ai - Ai * Aj)) := by
  abel

/-! ## P5-3：Φ = D|_Rec_photon 严格等式的函子层形式化（2026-08-12 推进）
   严格语义（笔记 §3.5 P5-3 / 路线图 62G）："Φ = D|_Rec_photon" 的严格形式 =
   ① 谱化路径交换（对象层定义等式，rfl 级）+ ② 转变效应一致（Φ 的闭→开 = D∘E 的谱差）。
   基础（既有）：photonToRecFunctor（忠实嵌入 E）+ DFunctor（完整 D 函子，DecursionFunctor.lean）
   + bifurcationFunctor（Φ 自函子）。本 P5-3 段补：复合函子构造 + 对象层/态射层严格等式。 -/

/-- 谱化复合函子 DE = D ∘ E : PhotonTopology → SpObj
    ——"D|_Rec_photon" 的函子层实现（D 谱化函子经光子→Rec 忠实嵌入复合）。
    注意 mathlib 复合方向：F.comp G 为先 F 后 G（F ⋙ G），故 E 在前、D 在后。 -/
noncomputable abbrev DE : PhotonTopology ⥤ SpObj :=
  photonToRecFunctor.comp DFunctor

/-- Φ 后谱化函子 PhiSpectral = DE ∘ Φ : PhotonTopology → SpObj
    ——先拓扑转变、再谱化（Φ 谱效应的函子编码）。 -/
noncomputable abbrev PhiSpectral : PhotonTopology ⥤ SpObj :=
  bifurcationFunctor.comp DE

/-- **P5-3 对象层（定义等式，rfl 级）**：Φ 后谱化 = D∘E 作用在 Φ(X) 上——
    Φ 的谱化完全由 D 函子在 Rec 嵌入上的作用给出（无独立谱结构）。 -/
theorem phi_spectral_obj (X : PhotonTopology) :
    PhiSpectral.obj X = DFunctor_obj (photonToRec (bifurcationMap X)) := by
  dsimp [PhiSpectral, DE]
  rfl

/-- **P5-3 对象层（谱化路径交换）**：谱化与 Φ 在对象层交换——
    photonSpectrum = D∘E 的定义（phi_D_object_commute 的 P5-3 表述）。 -/
theorem phi_spectral_commute (X : PhotonTopology) :
    photonSpectrum (bifurcationFunctor.obj X) =
      DFunctor_obj (photonToRec (bifurcationFunctor.obj X)) :=
  phi_D_object_commute X

/-- **P5-3 转变效应一致（对象层）**：Φ 后谱恒为开放谱（PhiSpectral 常值 = DE(open)）——
    Φ 的"闭→开"转变在谱层 = DE 的谱差（DE(closed) ≠ DE(open)，1 维 vs 2 维，
    DE_spectral_bifurcation）。 -/
theorem phi_spectral_constant (X : PhotonTopology) :
    PhiSpectral.obj X = DE.obj photonTopology := by
  change DFunctor_obj (photonToRec (bifurcationMap X)) = DFunctor_obj (photonToRec photonTopology)
  exact bifurcation_spectrum_final X

/-- **P5-3 谱转变非平凡性（D 刻画）**：DE 在闭/开光子拓扑上谱不同（1 维 vs 2 维）——
    D∘E 承载"闭→开"的谱跃迁，Φ 的转变效应完全由 D 在 Rec 嵌入上的作用给出。 -/
theorem DE_spectral_bifurcation :
    DE.obj atomicTopology ≠ DE.obj photonTopology := by
  change DFunctor_obj (photonToRec atomicTopology) ≠ DFunctor_obj (photonToRec photonTopology)
  exact bifurcation_changes_spectrum

/-- **P5-3 态射层（谱效应平凡）**：Φ 的态射在谱化下全为开放谱上的恒等——
    Φ 态射层谱效应平凡，转变效应完全由对象层承载（与 DE_spectral_bifurcation 互补）。
    关键：PhiSpectral.obj X = PhiSpectral.obj Y 定义上成立（bifurcationMap 恒为 opened），
    故矩阵元素比较类型自动统一。 -/
theorem phi_spectral_map_identity {X Y : PhotonTopology} (f : PhotonHom X Y) :
    PhiSpectral.map f = 𝟙 (PhiSpectral.obj X) := by
  apply SpHom.ext
  funext i j
  -- Φ 态射 = opened 恒等（bifurcationFunctor.map f = ⟨rfl⟩）→ Rec 嵌入 = Bool 恒等
  -- → D 像 = 转移矩阵(恒等) = 单位阵
  simp [PhiSpectral, DE, photonToRecFunctor, bifurcationFunctor, bifurcationMap,
    photonHomToRecHom, DFunctor, DFunctor_map, transferMatrix]
  rfl

/-- **P5-3 函子律（PhiSpectral 为函子，复合函子自动）**：保恒等 + 保复合机器证明。 -/
theorem phi_spectral_map_id (X : PhotonTopology) :
    PhiSpectral.map (𝟙 X) = 𝟙 (PhiSpectral.obj X) := by
  simp [PhiSpectral, DE]
  rfl

theorem phi_spectral_map_comp {X Y Z : PhotonTopology} (f : X ⟶ Y) (g : Y ⟶ Z) :
    PhiSpectral.map (f ≫ g) = PhiSpectral.map f ≫ PhiSpectral.map g := by
  simp [PhiSpectral, DE]
  rfl

/-- **P5-3 总结定理（Φ = D|_Rec_photon 严格等式的函子层形式）**：
    ① 对象层：谱化路径交换（phi_spectral_commute，定义等式）+ 转变效应由 D 刻画
    （DE_spectral_bifurcation：DE(closed) ≠ DE(open)；phi_spectral_constant：Φ 后恒开放）；
    ② 态射层：Φ 态射谱化平凡（phi_spectral_map_identity：开放谱恒等）；
    ③ 函子结构：PhiSpectral = DE∘Φ 为函子（phi_spectral_map_id/comp）。
    结论：光子拓扑转变 Φ 的谱效应完全由 D 函子在 Rec 嵌入（E）上的作用给出，
    无独立于 D 的谱结构——"Φ 是 D 函子的特例"在谱化路径意义下严格成立。 -/
theorem P53_strict_equality :
    (∀ X : PhotonTopology, photonSpectrum (bifurcationFunctor.obj X) =
      DFunctor_obj (photonToRec (bifurcationFunctor.obj X))) ∧
    (DE.obj atomicTopology ≠ DE.obj photonTopology) ∧
    (∀ (X Y : PhotonTopology) (f : PhotonHom X Y), PhiSpectral.map f = 𝟙 (PhiSpectral.obj X)) := by
  constructor
  · intro X
    exact phi_spectral_commute X
  · constructor
    · exact DE_spectral_bifurcation
    · intro X Y f
      exact phi_spectral_map_identity f

end UFPFormalization
