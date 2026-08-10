import UFPFormalization.PhotonTopology
import UFPFormalization.RecCategory
import UFPFormalization.SpCategory
import UFPFormalization.DecursionFunctor
import Mathlib.CategoryTheory.Category.Basic
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
3. **态射层（登记桥接）**：光子拓扑范畴的态射结构（PhotonHom = 拓扑类保持）
   未建立与 RecHom 的嵌入，完整"Φ = D|子范畴"（态射层）登记开放项。

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

/-! ## 纤维丛层正交的代数骨架（开放问题 #7 推进）
   "纤维 ⊥ 基空间"的严格意义 = (垂直子空间 V, 水平子空间 H, 度量 g) 的相容选取:
   V 内在 (ker dπ), H 由联络选取 (非唯一), 正交性由 g 与 H 的相容保证。
   数值演示: paperX_photon_fiber_orthogonality.py (5/5)——标准度量下 V⊥H_f ⟺ f=0
   (联络-度量不相容则不正交); 正交标架度量 g_A 下 V⊥H_A 对任意 A (相容选取 -> 正交)。
   内积层（⟪v,h⟫=0 ⟹ 交平凡）在 mathlib 可证（inner_self_eq_zero），本模块以
   正交的代数推论（V ⊓ H = ⊥）作为结构断言，避免内积记号适配。 -/

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

end UFPFormalization
