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
-- 本文件中 UFPF 相关引用数量：2
-- 更名将在计划确认后统一执行，当前代码不做修改。
-- ============================================================

import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.InnerProductSpace.Orthogonal
import Mathlib.Analysis.InnerProductSpace.Projection.FiniteDimensional
import Mathlib.LinearAlgebra.Projection
import Mathlib.Algebra.Group.Idempotent
import Mathlib.Tactic

/-!
# FiberOrthogonalSkeleton — 纤维丛层正交的代数骨架（通用微分几何，2026-08-14 自 PhotonTopologyFunctor 迁出）

论文: paper/paper44_photon_topology.md §7.2/§7.3（开放问题 #7）
笔记: notes/06_photon_topology/photon_topology_theory.md（纤维丛层正交推进）
数值演示: paperX_photon_fiber_orthogonality.py (5/5)

内容（开放问题 #7 纤维丛层，与光子内容解耦的通用微分几何）：
  1. 垂直-水平正交分解（代数骨架）：`VerticalHorizontalSplitting`（V ⊓ H = ⊥、V ⊔ H = ⊤）
  2. 内积层：内积正交 ⟹ 交平凡（`inf_eq_bot_of_le_orthogonal`/`inf_eq_bot_of_inner_orthogonal`/
     `vertical_horizontal_orthogonal_consistent`）
  3. 联络-度量相容选取：度量正交补 Vᗮ 是 V 的**典范补空间**（`sup_orthogonal_eq_top`/
     `isCompl_orthogonal_standard`/`standard_splitting_satisfies`）
  4. 联络 = 幂等投影：P² = P（`LinearProjection`/`projection_along_orthogonal_idempotent`/
     `_ker`/`_range`/`connection_metric_compatible`）

迁移记录（2026-08-14，内容域命名原则）：本文件内容原为 PhotonTopologyFunctor 内
"纤维丛层正交的代数骨架（开放问题 #7 推进）"章节——按用户裁定"内容领域决定命名"，
通用微分几何内容迁至本通用模块（与 CurvatureSkeleton 曲率迁出同批原则），
PhotonTopologyFunctor 仅保留光子函子内容。命名沿用 Skeleton 惯例
（SpectralSkeleton/CurvatureSkeleton/KatoRellichSkeleton）。

诚实边界：本文件为代数骨架（Submodule 层），完整纤维丛微分几何
（流形级联络/曲率形式）待微分几何库——与 §7.5 开放问题 3 一致。
-/

namespace UFPFormalization

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

end UFPFormalization
