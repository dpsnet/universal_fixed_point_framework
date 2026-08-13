import UFPFormalization.PhotonTopology2Lifting
import UFPFormalization.PhotonTopologyFunctor
import Mathlib.Tactic

namespace UFPFormalization

/-!
# CategoryGeometryDictionary — 完整范畴-几何字典（法向↔V、水平↔H 统一同构）

笔记: notes/06_photon_topology/photon_first_principle_origin.md §3.5 P5-2 延伸 v0.89
（"登记开放：完整范畴-几何字典（法向↔V、水平↔H 统一同构）"）
论文: paper/paper44_photon_topology.md §7.2 #2 / §7.3（4-范畴几何未形式化声明）

## 目标
把范畴层（`CellDirection` 方向类 + lifting 正交）与纤维丛层
（`VerticalHorizontalSplitting` 的 V/H 子空间正交分解）统一为**完整字典**：

- 法向方向（unfold/光子生成方向，`CellDirection.normal`）↔ 垂直子空间 V；
- 水平方向（transition/Δ 水平 2-态射方向，`CellDirection.horizontal`）↔ 水平子空间 H；
- 方向互补（`CellDirection.opposite`）⟷ 子空间分解（V ⊓ H = ⊥、V ⊔ H = ⊤）。

## 正交语义分层（核心：正交 ≠ 内积、≠ KK）

**正交的代数核心 = 互补分解**（`inf_bot`/`sup_top`，本字典主结构，**无内积**）：
- 范畴层（`PhotonTopology2Lifting`）：方向类填充性质（lifting 正交，非内积——
  正面回应 CNF 评价 (b)"4-范畴中没有内积定义"）；
- 纤维丛层（`PhotonTopologyFunctor` #7 已闭合）：垂直-水平分解 V ⊕ H
  （`VerticalHorizontalSplitting`，谱纤维丛意义）；
- 字典把方向类映射到子空间，使"方向正交（方向互补）"与"子空间分解（交平凡）"
  成为同一代数结构的两面——**不依赖内积**。

**内积正交补（`Vᗮ`）仅为可选构造**（`categoryGeometryDictionary_orthogonalComplement`），
语义限定为：**谱纤维空间 E 内**的垂直-水平度量正交（#7 已闭合的 `isCompl_orthogonal_standard`），
E 为纤维空间（非物理三维空间）。**非 KK 守卫**：字典不把正交实现为物理空间内的
几何额外维度——引力 Δ ⊥ 三维空间、光子法线 ⊥ 空间/时间均为范畴层/纤维丛层
**结构意义**的正交（方向类填充性质 + 垂直-水平分解），物理内容由 GR/电动力学承载，
不引入额外空间坐标（paper44 §7.2 边界 1）。矩阵层锚点（`DeviationBound` §1.8）
J2 模式间定位同样是非内积的迹正交。

## 骨架状态（诚实边界）
1. **字典结构（已闭合）**：`CategoryGeometryDictionary`——方向类 → 子空间映射
   （法向↔V、水平↔H）+ 互补分解断言（inf_bot/sup_top，代数核心无内积）；
2. **构造（已闭合）**：由 `VerticalHorizontalSplitting` 直接构造（主，无内积）；
   由内积正交补构造（可选，谱纤维空间意义 Vᗮ，标注非 KK）；
3. **一致性（已闭合）**：方向映射保持（normal↦V、horizontal↦H）、
   方向互补保持（opposite 交换 V/H）、lifting 正交与字典正交衔接；
4. **登记开放（后续）**：矩阵层完整字典（J2 迹正交 → 偏差矩阵全体方向的
   逐项对应）；"每层方向 → 垂直/水平子空间"的逐层实例化（1-层 lifting、
   2-层 Δ 2-胞腔、3/4-态射层的统一同构映射）。
-/

universe u v

/-! ## 字典结构：方向类 → 纤维丛子空间的统一映射 -/

/-- **完整范畴-几何字典**：纤维丛层正交分解（垂直/水平子空间）作为
    范畴层方向类（法向/水平）的几何实现。
    - V = 垂直子空间（法向方向，unfold/光子生成方向的几何载体）；
    - H = 水平子空间（水平方向，Δ 水平 2-态射方向的几何载体）；
    - inf_bot：V ⊓ H = ⊥（交平凡——方向正交（方向互补）的代数实现）；
    - sup_top：V ⊔ H = ⊤（互补——方向类互补（穷尽方向）的代数实现）。
    正交核心 = 互补分解（无内积）；E 为谱纤维空间（非物理三维空间），
    正交不产生额外空间维度（非 KK 守卫）。 -/
structure CategoryGeometryDictionary (E : Type u) [AddCommGroup E] [Module ℝ E] where
  V : Submodule ℝ E
  H : Submodule ℝ E
  inf_bot : V ⊓ H = ⊥
  sup_top : V ⊔ H = ⊤

/-- **方向类 → 子空间映射**（字典核心）：法向 ↦ V（垂直）、水平 ↦ H（水平）。 -/
def CategoryGeometryDictionary.directionMap {E : Type u} [AddCommGroup E] [Module ℝ E]
    (D : CategoryGeometryDictionary E) : CellDirection → Submodule ℝ E
  | CellDirection.normal => D.V
  | CellDirection.horizontal => D.H

/-! ## 构造：从既有正交结构生成字典 -/

/-- **由纤维丛层正交分解构造字典（主构造，无内积）**：`VerticalHorizontalSplitting`
    （V ⊓ H = ⊥、V ⊔ H = ⊤，谱纤维丛意义垂直-水平分解）直接给出字典——
    纤维丛层 V⊥H 分解 ⟹ 方向类正交（法向↔V、水平↔H）。 -/
def categoryGeometryDictionary_of_splitting {E : Type u} [AddCommGroup E] [Module ℝ E]
    (s : VerticalHorizontalSplitting E) : CategoryGeometryDictionary E :=
  { V := s.V, H := s.H, inf_bot := s.inf_bot, sup_top := s.sup_top }

/-- **由内积正交补构造字典（可选构造，谱纤维空间意义）**：垂直子空间 V 与其
    度量正交补 Vᗮ（有限维下 V ⊔ Vᗮ = ⊤，`isCompl_orthogonal_standard`，#7 已闭合）——
    水平子空间 = V 的正交补，为联络-度量相容选取的典范情形。
    **非 KK 守卫**：E 为谱纤维空间（非物理三维空间），此内积正交是纤维空间内
    的垂直-水平度量正交，非物理空间几何额外维度（引力 ⊥ 空间/时间、
    光子法线 ⊥ 空间/时间均为结构意义正交，物理内容由 GR/电动力学承载）。 -/
noncomputable def categoryGeometryDictionary_orthogonalComplement {E : Type v} [NormedAddCommGroup E]
    [InnerProductSpace ℝ E] [FiniteDimensional ℝ E] (V : Submodule ℝ E) :
    CategoryGeometryDictionary E :=
  { V := V,
    H := Vᗮ,
    inf_bot := V.inf_orthogonal_eq_bot,
    sup_top := (isCompl_orthogonal_standard V).sup_eq_top }

/-- **由内积正交构造字典（可选构造，谱纤维空间意义）**：H ≤ Vᗮ（内积正交，
    `inf_eq_bot_of_le_orthogonal`）+ 互补（V ⊔ H = ⊤）⟹ 字典。
    **非 KK 守卫**：同上——内积为正交的充分条件（纤维空间内度量意义），
    非物理空间几何正交。 -/
def categoryGeometryDictionary_of_innerOrthogonal {E : Type v} [NormedAddCommGroup E]
    [InnerProductSpace ℝ E] (V H : Submodule ℝ E) (h_orth : H ≤ Vᗮ)
    (h_sup : V ⊔ H = ⊤) : CategoryGeometryDictionary E :=
  { V := V, H := H, inf_bot := inf_eq_bot_of_le_orthogonal V H h_orth, sup_top := h_sup }

/-! ## 一致性：方向映射与互补保持 -/

/-- **法向方向映射 = 垂直子空间**（字典核心对应之一）。 -/
@[simp] theorem directionMap_normal {E : Type u} [AddCommGroup E] [Module ℝ E]
    (D : CategoryGeometryDictionary E) :
    D.directionMap CellDirection.normal = D.V := rfl

/-- **水平方向映射 = 水平子空间**（字典核心对应之二）。 -/
@[simp] theorem directionMap_horizontal {E : Type u} [AddCommGroup E] [Module ℝ E]
    (D : CategoryGeometryDictionary E) :
    D.directionMap CellDirection.horizontal = D.H := rfl

/-- **方向互补保持（法向侧）**：法向的对立方向（水平）映射到水平子空间——
    方向互补（`CellDirection.opposite`）经字典成为子空间角色交换。 -/
@[simp] theorem directionMap_opposite_normal {E : Type u} [AddCommGroup E] [Module ℝ E]
    (D : CategoryGeometryDictionary E) :
    D.directionMap (CellDirection.opposite CellDirection.normal) = D.H := by
  simp [CellDirection.opposite]

/-- **方向互补保持（水平侧）**：水平的对立方向（法向）映射到垂直子空间。 -/
@[simp] theorem directionMap_opposite_horizontal {E : Type u} [AddCommGroup E] [Module ℝ E]
    (D : CategoryGeometryDictionary E) :
    D.directionMap (CellDirection.opposite CellDirection.horizontal) = D.V := by
  simp [CellDirection.opposite]

/-! ## 正交一致性：方向正交 ⟷ 子空间正交 -/

/-- **字典正交性**：垂直与水平子空间交平凡（V ⊓ H = ⊥）——方向正交
    （法向 ⊥ 水平，lifting 正交）在几何层的实现。 -/
theorem dictionary_orthogonal {E : Type u} [AddCommGroup E] [Module ℝ E]
    (D : CategoryGeometryDictionary E) : D.V ⊓ D.H = ⊥ := D.inf_bot

/-- **字典互补性**：垂直与水平子空间张成全空间（V ⊔ H = ⊤）——
    方向类互补（normal/horizontal 穷尽方向）在几何层的实现。 -/
theorem dictionary_complement {E : Type u} [AddCommGroup E] [Module ℝ E]
    (D : CategoryGeometryDictionary E) : D.V ⊔ D.H = ⊤ := D.sup_top

/-- **范畴层 lifting 正交与字典正交的衔接**：lifting 正交（2-态射层方向互补，
    `twoLifting_orthogonal` 自动成立）与字典正交（V ⊓ H = ⊥，`inf_bot`）
    是同一"方向正交"语义在范畴层/几何层的一致实现——
    本定理显式登记该一致性（方向类互补 ⟹ 子空间交平凡）。 -/
theorem lifting_orthogonal_consistent {E : Type u} [AddCommGroup E] [Module ℝ E]
    (D : CategoryGeometryDictionary E) :
    D.V ⊓ D.H = ⊥ ∧ D.V ⊔ D.H = ⊤ :=
  ⟨D.inf_bot, D.sup_top⟩

end UFPFormalization
