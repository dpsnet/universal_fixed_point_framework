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
-- 本文件中 UFPF 相关引用数量：3
-- 更名将在计划确认后统一执行，当前代码不做修改。
-- ============================================================

/-
  SilenceObservationAllocation.lean — 静默方向到观测层（纵向 1 + 横向 3）分配的机器证明骨架
  ============================================================================

  推进笔记: notes/04_lorentz_gravity/silence_direction_allocation.md
  论文锚点: paper40 §5.10（观测层权重算子 = 朗道横向投影，D1-D10）;
            paper32 T1-T8（Cl(1,7) = 1 时间 ⊕ 3 可见空间 ⊕ 4 静默内部）;
            paper11 附录 C（α 截断 dim=32 = Cl(9,1) Level 1）;
            paper20 §5.8（Bott 塔）。

  ## 目标

  "Cl(1,7) 4 静默方向 ↔ 观测层（纵向 1 + 横向 3）对应"的机器证明。
  本文件建立**可严格证明的数学骨架**（纯线性代数 + 维度计数），
  物理映射（静默方向 → 规范纵向 / 光子法向）为注释层标注，不作定理声称：

  1. 观测层正交分解：ℝ⁴ = V_long ⊕ V_trans，V_long ⊥ V_trans
     （V_long = span{qhat} 纵向 1 维，V_trans = V_longᗮ 横向 3 维）。
  2. 维度计数：dim V_long = 1、dim V_trans = 3、dim E = 4。
  3. 朗道横向投影：W = 到 V_trans 的投影，ker W = V_long（规范纵向/静默）、
     im W = V_trans（可见横向）——paper40 D3-D5 的算子表述。
  4. 静默计数对应：Cl(1,7) 静默 4 方向（paper32 silent_dimensions_eq_four）
     ↔ 观测层 V_long(1) + V_trans(3) = 4 —— 维度对应（非物理同一性，见诚实边界）。

  ## 诚实边界

  - 本文件证明的是**数学骨架**：ℝ⁴ 的正交分解、维度计数、朗道投影的
    ker/im 结构——全部为纯线性代数定理，可机器验证。
  - "静默 4 方向 ↔ 观测层 (1+3)" 的**物理对应**（静默方向映射到规范纵向/
    光子法向）仍为 [衔接] 候选——本文件不声称该物理映射，
    仅在注释层标注维度对应（4 = 1 + 3）。
  - Cl(1,7) 静默计数的现有机器证明（CoherenceToBranching.lean
    silent_dimensions_eq_four）不重复——本文件引用其结论作为计数锚点注释。

  状态: 2026-08-15 v0.2（复用 FiberOrthogonalSkeleton 引理修正）。
-/

import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.InnerProductSpace.Orthogonal
import Mathlib.Analysis.InnerProductSpace.Projection.FiniteDimensional
import Mathlib.LinearAlgebra.Projection
import Mathlib.LinearAlgebra.FiniteDimensional.Basic
import Mathlib.Tactic
import UFPFormalization.FiberOrthogonalSkeleton

namespace UFPFormalization

/-! ## 观测层正交分解：E = V_long ⊕ V_trans -/

variable {E : Type} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- 观测层纵向子空间 = 传播方向 qhat 的生成子空间（V_long = span{qhat}，1 维）。 -/
def longitudinalSubspace (qhat : E) : Submodule ℝ E :=
  Submodule.span ℝ ({qhat} : Set E)

/-- 观测层横向子空间 = 纵向的正交补（V_trans = V_longᗮ，3 维）。 -/
noncomputable abbrev transverseSubspace [FiniteDimensional ℝ E] (qhat : E) : Submodule ℝ E :=
  (longitudinalSubspace qhat)ᗮ

/-- 观测层正交分解：V_long ⊓ V_trans = ⊥（纵向与横向交平凡，正交性代数推论）。 -/
theorem longitudinal_inf_transverse_eq_bot [FiniteDimensional ℝ E] (qhat : E) :
    longitudinalSubspace qhat ⊓ transverseSubspace qhat = ⊥ := by
  simpa [transverseSubspace] using (longitudinalSubspace qhat).inf_orthogonal_eq_bot

/-- 观测层正交分解：V_long ⊔ V_trans = ⊤（纵向与横向张成整个观测层）。 -/
theorem longitudinal_sup_transverse_eq_top [FiniteDimensional ℝ E] (qhat : E) :
    longitudinalSubspace qhat ⊔ transverseSubspace qhat = ⊤ := by
  simpa [transverseSubspace] using sup_orthogonal_eq_top (longitudinalSubspace qhat)

/-- 纵向子空间维度 = 1：dim span{qhat} = 1（qhat ≠ 0 时）。
    用 mathlib `finrank_span_singleton`（Mathlib.LinearAlgebra.FiniteDimensional.Basic）。 -/
theorem dim_longitudinal (qhat : E) (hq : qhat ≠ 0) :
    Module.finrank ℝ (longitudinalSubspace qhat) = 1 := by
  have hspan : Submodule.span ℝ ({qhat} : Set E) = longitudinalSubspace qhat := by
    rfl
  rw [← hspan]
  exact finrank_span_singleton hq

/-- 横向子空间维度：dim V_trans = dim E − dim V_long（有限维正交补维度加性）。 -/
theorem dim_transverse_of_dim_E [FiniteDimensional ℝ E] {d : ℕ} (hd : Module.finrank ℝ E = d)
    (qhat : E) (hq : qhat ≠ 0) :
    Module.finrank ℝ (transverseSubspace qhat) = d - 1 := by
  have hV : Module.finrank ℝ (longitudinalSubspace qhat) = 1 := dim_longitudinal qhat hq
  have hadd := (longitudinalSubspace qhat).finrank_add_finrank_orthogonal
  -- hadd: finrank V + finrank Vᗮ = finrank E；取对称得到目标方向
  have hE : Module.finrank ℝ E = Module.finrank ℝ (longitudinalSubspace qhat) +
      Module.finrank ℝ (transverseSubspace qhat) := by
    simpa [transverseSubspace] using hadd.symm
  rw [hV, hd] at hE
  omega

/-- 四维观测层的横向维度：dim V_trans = 3（dim E = 4，dim V_long = 1）。 -/
theorem dim_transverse_four (E : Type) [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] (h4 : Module.finrank ℝ E = 4)
    (qhat : E) (hq : qhat ≠ 0) :
    Module.finrank ℝ (transverseSubspace qhat) = 3 := by
  have h := dim_transverse_of_dim_E (E := E) h4 qhat hq
  omega

/-! ## 朗道横向投影：W = 到 V_trans 的投影，ker W = V_long、im W = V_trans -/

/-- 朗道横向投影 = 到横向子空间 V_trans 的正交投影（paper40 D5：W = 1₄ − qhat·qhatᵀ）。 -/
noncomputable def landauProjection [FiniteDimensional ℝ E] (qhat : E) : E →ₗ[ℝ] E :=
  (transverseSubspace qhat).projection (transverseSubspace qhat)ᗮ
    (isCompl_orthogonal_standard (transverseSubspace qhat))

/-- 朗道投影是幂等投影（W² = W，paper40 D1：正交投影）。 -/
theorem landauProjection_idempotent [FiniteDimensional ℝ E] (qhat : E) :
    IsIdempotentElem (landauProjection qhat) := by
  unfold landauProjection
  exact Submodule.isIdempotentElem_projection (isCompl_orthogonal_standard (transverseSubspace qhat))

/-- 朗道投影的核 = 横向子空间的正交补（ker W = (V_trans)ᗮ）。
    在正交分解下 (V_trans)ᗮ = V_long（对偶补的双对偶，paper40 D3：纵向 = 规范静默）。
    复用 FiberOrthogonalSkeleton `projection_along_orthogonal_ker`。 -/
theorem landauProjection_ker [FiniteDimensional ℝ E] (qhat : E) :
    LinearMap.ker (landauProjection qhat) = (transverseSubspace qhat)ᗮ := by
  unfold landauProjection
  exact projection_along_orthogonal_ker (transverseSubspace qhat)

/-- 朗道投影的像 = 横向子空间（im W = V_trans，paper40 D4：im W = span{qhat}⊥）。
    复用 FiberOrthogonalSkeleton `projection_along_orthogonal_range`。 -/
theorem landauProjection_range [FiniteDimensional ℝ E] (qhat : E) :
    LinearMap.range (landauProjection qhat) = transverseSubspace qhat := by
  unfold landauProjection
  exact projection_along_orthogonal_range (transverseSubspace qhat)

/-! ## 静默计数对应（维度层）

   Cl(1,7) 静默 4 方向（paper32：4 = N_total − 1，silent_dimensions_eq_four）
   ↔ 观测层纵向 V_long(1) + 横向 V_trans(3) = 4 —— **维度对应**：
   观测层的纵向-横向分解（1 + 3 = 4）与 Cl(1,7) 静默方向数（4）在维度上一致。
   物理映射（静默方向 → 规范纵向 / 光子法向）为 [衔接] 注释层，不作定理声称。
   -/

/-- 维度对应恒等式：观测层纵向(1) + 横向(3) = 4 = Cl(1,7) 静默方向数。
    本定理为纯算术恒等式，作为维度对应锚点（物理对应见注释层）。 -/
theorem silence_observation_dimension_correspondence :
    1 + 3 = 4 := by norm_num

end UFPFormalization
