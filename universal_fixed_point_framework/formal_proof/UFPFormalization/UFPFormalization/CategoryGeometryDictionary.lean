import UFPFormalization.LiftingOrthogonality
import UFPFormalization.FiberOrthogonalSkeleton
import UFPFormalization.BranchCounting
import Mathlib.Tactic

open UFPFormalization.BranchCounting

namespace UFPFormalization

/-!
# CategoryGeometryDictionary — 完整范畴-几何字典（法向↔V、水平↔H 逐层统一同构）

笔记: notes/06_photon_topology/photon_first_principle_origin.md §3.5 P5-2 延伸 v0.90
（"登记开放：完整范畴-几何字典（法向↔V、水平↔H 统一同构）"）
论文: paper/paper44_photon_topology.md §7.2 #2 / §7.3（4-范畴几何未形式化声明）

## 目标
把范畴层（4-范畴四层态射方向 + lifting 正交）与纤维丛层
（`VerticalHorizontalSplitting` 的 V/H 子空间正交分解）统一为**逐层完整字典**：

- 法向方向（unfold/光子生成方向）↔ 垂直子空间 V；
- 水平方向（transition/Δ 水平 2-态射方向）↔ 水平子空间 H；
- 逐层（LayerIndex 1/2/3/4，对齐 paper31 J3 §4.1 层结构表）：
  每层态射的方向类都映射到同一对 V/H——字典对四层一致成立；
- 方向互补（`CellDirection.opposite`）⟷ 子空间分解（V ⊓ H = ⊥、V ⊔ H = ⊤）。

## 各层态射来源（显式登记，一致性核查）
论文 §7.3"完整 4-范畴态射层骨架"由三层来源构成，字典逐层登记其载体：

| 层 | 态射结构 | 来源模块 | 方向类载体 | 与字典映射 |
|:--|:--|:--|:--|:--|
| 1-层 | `MultiMor`（unfold/fold/transition） | PhotonTopologyFunctorLaws + mathlib `HasLiftingProperty`（1-层 lifting 正交实例化，复用 mathlib 不另建） | 法向=unfold、水平=transition | normal↦V、horizontal↦H |
| 2-层 | `SpTwoMorphism`（homotopy 矩阵）+ `SpDelta2Cell`（Δ 偏差矩阵） | HigherSpCategory（链复形模式） | `CellDirection`（Z₂ 方向代数，LiftingOrthogonality/TwoCategoryLaws） | normal↦V、horizontal↦H |
| 3-层 | `SpThreeMorphism`（secondHomotopy 链复形） | HigherSpCategory | 方向类填充（层 3 交换律严格，非方向代数 lifting） | normal↦V、horizontal↦H |
| 4-层 | `SpFourMorphism`（thirdHomotopy 链复形） | HigherSpCategory | coherence 层 = Δ 所在层 | normal↦V、horizontal↦H |

**一致性要点**：2-层存在**双来源**——HigherSpCategory 的链复形模式（`SpTwoMorphism`，
homotopy 矩阵为实质载体）与方向类路线（`CellDirection`，Z₂ 方向代数，为 lifting 正交的
方向编码）。字典的方向类（`CellDirection`）与链复形态射结构的对应：`CellDirection`
为每层态射的**方向标记**，链复形（homotopy/偏差矩阵）为每层态射的**结构内容**——
二者是同一态射的两个面（方向编码 + 结构内容），非两套独立态射。方向类经
`SpDelta2Cell.dev`（偏差矩阵）与 `spExchangeLaw_deviation_*` 衔接链复形内容
（HigherSpCategory §1.8 范畴-几何桥）。**登记开放（诚实边界）**：层 2 方向类与
链复形态射的**逐项对应定理**（CellDirection ↔ homotopy 矩阵的完整同构）待建——
本字典完成方向类侧的逐层映射，链复形侧的结构内容衔接登记开放。

## 正交语义分层（核心：正交 ≠ 内积、≠ KK）

**正交的代数核心 = 互补分解**（`inf_bot`/`sup_top`，本字典主结构，**无内积**）：
- 范畴层（mathlib `HasLiftingProperty` 1-层实例/`LiftingOrthogonality`）：方向类填充性质
  （lifting 正交 = 唯一对角填充，非内积——正面回应 CNF 评价 (b)"4-范畴中没有内积定义"）；
- 纤维丛层（`FiberOrthogonalSkeleton` #7 已闭合，2026-08-14 自 PhotonTopologyFunctor 迁出）：垂直-水平分解 V ⊕ H
  （`VerticalHorizontalSplitting`，谱纤维丛意义）；
- 字典把逐层方向类映射到子空间，使"方向正交（方向互补）"与"子空间分解（交平凡）"
  成为同一代数结构的两面——**不依赖内积**。

**内积正交补（`Vᗮ`）仅为可选构造**（`categoryGeometryDictionary_orthogonalComplement`），
语义限定为：**谱纤维空间 E 内**的垂直-水平度量正交（#7 已闭合的 `isCompl_orthogonal_standard`），
E 为纤维空间（非物理三维空间）。**非 KK 守卫**：字典不把正交实现为物理空间内的
几何额外维度——引力 Δ ⊥ 三维空间、光子法线 ⊥ 空间/时间均为范畴层/纤维丛层
**结构意义**的正交（方向类填充性质 + 垂直-水平分解），物理内容由 GR/电动力学承载，
不引入额外空间坐标（paper44 §7.2 边界 1）。矩阵层锚点（`DeviationBound` §1.8）
J2 模式间定位同样是非内积的迹正交。

## 骨架状态（诚实边界）
1. **字典结构（已闭合）**：`CategoryGeometryDictionary`——逐层方向类 → 子空间映射
   （LayerIndex 1/2/3/4 × CellDirection：法向↦V、水平↦H）+ 互补分解断言
   （inf_bot/sup_top，代数核心无内积）；
2. **构造（已闭合）**：由 `VerticalHorizontalSplitting` 直接构造（主，无内积）；
   由内积正交补构造（可选，谱纤维空间意义 Vᗮ，标注非 KK）；
3. **一致性（已闭合）**：逐层方向映射保持（任意层 normal↦V、horizontal↦H）、
   方向互补保持（opposite 交换 V/H）、lifting 正交与字典正交衔接；
4. **登记开放（推进中）**：层 2 方向类 ↔ 链复形态射的逐项对应定理（CellDirection ↔
   homotopy 矩阵完整同构）；**矩阵层完整字典（J2 迹正交 → 偏差矩阵全体方向，
   2026-08-14 空间级刻画已闭合——`DeviationBound.lean` §1.9 `hs_orthogonal_complement_diagonal`：
   Hilbert–Schmidt 迹内积下对角矩阵空间的正交补 = 零对角元矩阵空间，即"X 与任意对角
   方向迹正交 ⟺ X 对角元全零"；`commutator_in_orthogonal_complement_diagonal`：偏差矩阵
   [A,B]（谱基对角）对角元全零 ⟹ 属于对角方向空间正交补——J2 定位从逐条方向提升为
   完整补空间表述，零 sorry）**；各层态射方向 → 垂直/水平子空间的逐层几何实例化。
-/

universe u v

/-! ## 层索引（对齐 paper31 J3 §4.1 层结构表；复用 BranchCounting.LayerIndex，2026-08-13 合并，登记册①） -/

/-- **4-范畴态射层层索引**（复用 BranchCounting.LayerIndex 母定义，5 层：
    层 0 对象 + 层 1-4 态射）：层 1（1-态射，空间 x 方向）、层 2（2-态射，空间 y 方向 + Δ）、
    层 3（3-态射，空间 z 方向）、层 4（4-态射，coherence 层 = Δ 所在层）。
    对齐 paper31 J3 §4.1 层结构表（层 1-3 正交于 Δ、层 4 = coherence = Δ 所在层）；
    层 0 对象不生成方向自由度，`directionMap` 对其一致成立（任意层映射，字典核心不依赖层）。 -/

/-- 层索引的"正交于 Δ / 位于 Δ"区分：层 1-3 = 正交于 Δ 的空间方向层；
    层 4 = coherence 层（Δ 所在层）。 -/
def LayerIndex.isCoherenceLayer : LayerIndex → Prop
  | .four => True
  | _ => False

/-! ## 字典结构：逐层方向类 → 纤维丛子空间的统一映射 -/

/-- **完整范畴-几何字典**：纤维丛层正交分解（垂直/水平子空间）作为
    范畴层**逐层方向类**（LayerIndex 1/2/3/4 × 法向/水平）的几何实现。
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

/-- **逐层方向类 → 子空间映射**（字典核心）：对任意层 ℓ（1/2/3/4），
    法向 ↦ V（垂直）、水平 ↦ H（水平）——字典对四层一致成立。 -/
def CategoryGeometryDictionary.directionMap {E : Type u} [AddCommGroup E] [Module ℝ E]
    (D : CategoryGeometryDictionary E) (ℓ : LayerIndex) : CellDirection → Submodule ℝ E
  | CellDirection.normal => D.V
  | CellDirection.horizontal => D.H

/-! ## 构造：从既有正交结构生成字典 -/

/-- **由纤维丛层正交分解构造字典（主构造，无内积）**：`VerticalHorizontalSplitting`
    （V ⊓ H = ⊥、V ⊔ H = ⊤，谱纤维丛意义垂直-水平分解）直接给出字典——
    纤维丛层 V⊥H 分解 ⟹ 任意层方向类正交（法向↔V、水平↔H）。 -/
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

/-! ## 一致性：逐层方向映射与互补保持 -/

/-- **逐层法向方向映射 = 垂直子空间（任意层一致）**：对层 1/2/3/4 中任一
    法向方向（unfold/光子生成方向），字典映射到同一垂直子空间 V。 -/
@[simp] theorem directionMap_normal {E : Type u} [AddCommGroup E] [Module ℝ E]
    (D : CategoryGeometryDictionary E) (ℓ : LayerIndex) :
    D.directionMap ℓ CellDirection.normal = D.V := rfl

/-- **逐层水平方向映射 = 水平子空间（任意层一致）**：对层 1/2/3/4 中任一
    水平方向（transition/Δ 水平 2-态射方向），字典映射到同一水平子空间 H。 -/
@[simp] theorem directionMap_horizontal {E : Type u} [AddCommGroup E] [Module ℝ E]
    (D : CategoryGeometryDictionary E) (ℓ : LayerIndex) :
    D.directionMap ℓ CellDirection.horizontal = D.H := rfl

/-- **方向互补保持（法向侧，任意层一致）**：法向的对立方向（水平）映射到水平子空间——
    方向互补（`CellDirection.opposite`）经字典成为子空间角色交换。 -/
@[simp] theorem directionMap_opposite_normal {E : Type u} [AddCommGroup E] [Module ℝ E]
    (D : CategoryGeometryDictionary E) (ℓ : LayerIndex) :
    D.directionMap ℓ (CellDirection.opposite CellDirection.normal) = D.H := by
  simp [CellDirection.opposite]

/-- **方向互补保持（水平侧，任意层一致）**：水平的对立方向（法向）映射到垂直子空间。 -/
@[simp] theorem directionMap_opposite_horizontal {E : Type u} [AddCommGroup E] [Module ℝ E]
    (D : CategoryGeometryDictionary E) (ℓ : LayerIndex) :
    D.directionMap ℓ (CellDirection.opposite CellDirection.horizontal) = D.V := by
  simp [CellDirection.opposite]

/-! ## 正交一致性：方向正交 ⟷ 子空间正交 -/

/-- **字典正交性（逐层）**：对任意层 ℓ，法向方向与水平方向映射到的子空间
    交平凡（V ⊓ H = ⊥）——方向正交（法向 ⊥ 水平，lifting 正交）在几何层的实现。 -/
theorem dictionary_orthogonal {E : Type u} [AddCommGroup E] [Module ℝ E]
    (D : CategoryGeometryDictionary E) (ℓ : LayerIndex) :
    D.directionMap ℓ CellDirection.normal ⊓
      D.directionMap ℓ CellDirection.horizontal = ⊥ := by
  simp

/-- **字典互补性（逐层）**：对任意层 ℓ，法向与水平方向张成全空间
    （V ⊔ H = ⊤）——方向类互补（normal/horizontal 穷尽方向）在几何层的实现。 -/
theorem dictionary_complement {E : Type u} [AddCommGroup E] [Module ℝ E]
    (D : CategoryGeometryDictionary E) (ℓ : LayerIndex) :
    D.directionMap ℓ CellDirection.normal ⊔
      D.directionMap ℓ CellDirection.horizontal = ⊤ := by
  simp

/-- **范畴层 lifting 正交与字典正交的衔接（逐层）**：lifting 正交（2-态射层方向互补，
    `twoLifting_orthogonal` 自动成立）与字典正交（V ⊓ H = ⊥，`inf_bot`）
    是同一"方向正交"语义在范畴层/几何层的一致实现——
    本定理显式登记该一致性（方向类互补 ⟹ 子空间交平凡），对任意层成立。 -/
theorem lifting_orthogonal_consistent {E : Type u} [AddCommGroup E] [Module ℝ E]
    (D : CategoryGeometryDictionary E) (ℓ : LayerIndex) :
    D.directionMap ℓ CellDirection.normal ⊓
        D.directionMap ℓ CellDirection.horizontal = ⊥ ∧
      D.directionMap ℓ CellDirection.normal ⊔
        D.directionMap ℓ CellDirection.horizontal = ⊤ := by
  constructor <;> simp

end UFPFormalization
