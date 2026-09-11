-- ============================================================
-- §26. 离散协变 Bianchi（Phase 16B 真值路径）
-- ============================================================
-- 背景（sorry_closure_roadmap.md §3.6，2026-09-11 证伪与处置）：
--   点值代数骨架 second_bianchi_discrete（无 ∂ 项）已机器证明，
--   但 Einstein 散度恒假——守恒律的载体在偏导数 ∂ 项。
--   数值预实验（numerical/phase16b_discrete_bianchi.py，2026-09-11）：
--   1. 朴素分量式含 ∂̃ 的离散第二 Bianchi 不成立（残差 ~2–3 × |∂̃Γ·Γ|，
--      离散 Leibniz 修正 ∂̃(AB)=∂̃A·B+A·∂̃B+∂̃A·∂̃B 不可忽略）；
--   2. 算子形式精确成立：把协变差分 D_ρ 视为场空间自同态，
--      曲率 F_{μν} = [D_μ, D_ν]，第二 Bianchi = 算子 Jacobi 恒等式
--      Σ_cyc [D_ρ, F_{μν}] = 0，无条件精确（数值 1e-15）；
--   3. 分量式以 O(a²) 相对误差连续极限恢复（|B|/|R| ∝ 1/n²）。
--
-- 本模块形式化结论 2（精确离散第二 Bianchi，算子形式）及其分量展开。
-- 与格点规范论同构：Bianchi 是联络代数 Jacobi 恒等式，
-- 不需要任何假设（无挠、对易、度量相容均不必需）。
-- ============================================================

import Mathlib.Data.Real.Basic
import Mathlib.Algebra.Module.Pi
import Mathlib.Algebra.Module.LinearMap.End
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NoncommRing
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Data.Fintype.BigOperators
import MUFPFormalization.RecCategory

namespace MUFPF

open Module
open scoped BigOperators

/-- Fin 4 显式求和（与 SpectralMetric.lean 的 sum4 同定义本地副本）。
    注：不直接 import SpectralMetric——其 `EinsteinTensor` 与
    SpacetimeStack.lean 同名声明在聚合根 import 时冲突（2026-09-11 实测）。
    若未来 SpectralMetric 被纳入聚合根，应删除本副本并统一引用。 -/
def sum4 (f : Fin 4 → ℝ) : ℝ := f 0 + f 1 + f 2 + f 3

/-- sum4 与 Finset.sum 的等价性（桥接引理，同 SpectralMetric.lean）。 -/
lemma sum4_eq_finset_sum (f : Fin 4 → ℝ) :
    sum4 f = ∑ i : Fin 4, f i := by
  simp [sum4, Fin.sum_univ_four]

-- ============================================================
-- §26.1 标架递归对象与方向 step
-- ============================================================

/-- 标架递归对象：RecObj 配备四方向 step。
    物理含义：递归系统的状态空间被视为时空格点，
    stepD ρ 是沿坐标方向 ρ 的演化（ρ = 0 时间，1..3 空间）。
    连续极限下 stepD ρ x − x → a·e_ρ（格距 a → 0）。 -/
structure FrameRecObj where
  X : RecObj
  stepD : Fin 4 → X.T → X.T

/-- 方向 step 对易性：相邻路径无关（格点平直性）。
    物理含义：先沿 ρ 再沿 σ 与先沿 σ 再沿 ρ 到达同一状态——
    连续极限 ∂_ρ∂_σ = ∂_σ∂_ρ 的离散对应。
    注：算子级 Bianchi（§26.4）不需要此假设；
    分量级展开（§26.5）的"无双移位项"形式才需要。 -/
def StepsCommute (F : FrameRecObj) : Prop :=
  ∀ ρ σ (x : F.X.T), F.stepD ρ (F.stepD σ x) = F.stepD σ (F.stepD ρ x)

/-- 向量场：状态空间上逐点取值的四分量场。
    物理含义：时空格点上的矢量场 V^r(x)。
    用 abbrev 使 Pi 的 AddCommGroup / Module 实例直接可用。 -/
abbrev VecField (F : FrameRecObj) := F.X.T → Fin 4 → ℝ

-- ============================================================
-- §26.2 Christoffel 场
-- ============================================================

/-- Christoffel 场：每个状态点一组无挠 Christoffel 符号。
    物理含义：联络系数逐点分布 Γ^r_{mn}(x)——
    连续极限下由 Levi-Civita 公式从度规场导出。 -/
structure GammaField (F : FrameRecObj) where
  γ : F.X.T → Fin 4 → Fin 4 → Fin 4 → ℝ
  /-- 逐点无挠性：Γ^r_{mn}(x) = Γ^r_{nm}(x) -/
  torsion_free : ∀ x r m n, γ x r m n = γ x r n m

-- ============================================================
-- §26.3 协变差分算子（场空间自同态）
-- ============================================================
-- 设计（对应格点规范论的协变导数）：
--   场空间 V = VecField F 是实向量空间，
--   其上自同态代数 Module.End ℝ V 是环（乘法 = 复合），
--   协变差分 D_ρ = S_ρ + A_ρ − 1 ∈ End：
--     S_ρ 移位算子：(S_ρ V)(x) = V(stepD ρ x)  [∂̃ 的移位部分]
--     A_ρ 规范作用：(A_ρ V)(x) = Γ_ρ(x)·V(x)    [联络项]
--     1   恒等：    对应 ∂̃ 的 −V(x) 项
--   曲率 F_{μν} = [D_μ, D_ν]（End 环中的交换子）。

/-- 移位算子：沿方向 ρ 的场值平移。
    物理含义：离散偏导数的移位部分 (S_ρ V)(x) = V(stepD ρ x)。 -/
noncomputable def shiftOp (F : FrameRecObj) (ρ : Fin 4) :
    Module.End ℝ (VecField F) where
  toFun V := fun x => V (F.stepD ρ x)
  map_add' _ _ := funext fun _ => rfl
  map_smul' _ _ := funext fun _ => rfl

/-- 移位算子的作用公式（definitional）。 -/
@[simp] lemma shiftOp_apply (F : FrameRecObj) (ρ : Fin 4)
    (V : VecField F) (x : F.X.T) :
    (shiftOp F ρ V) x = V (F.stepD ρ x) := rfl

/-- 规范作用算子：联络系数的逐点矩阵作用。
    物理含义：(A_ρ V)^r(x) = Σ_l Γ^r_{ρl}(x) V^l(x)——
    连续协变导数 ∇_ρ V = ∂_ρ V + Γ_ρ V 的联络项。 -/
noncomputable def gaugeOp (F : FrameRecObj) (Γf : GammaField F) (ρ : Fin 4) :
    Module.End ℝ (VecField F) where
  toFun V := fun x r => ∑ l : Fin 4, Γf.γ x r ρ l * V x l
  map_add' V W := by
    ext x r
    simp only [Pi.add_apply]
    rw [← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro l _
    ring
  map_smul' c V := by
    ext x r
    simp only [Pi.smul_apply, smul_eq_mul, RingHom.id_apply]
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro l _
    ring

/-- 规范作用算子的作用公式（definitional）。 -/
@[simp] lemma gaugeOp_apply (F : FrameRecObj) (Γf : GammaField F) (ρ : Fin 4)
    (V : VecField F) (x : F.X.T) (r : Fin 4) :
    (gaugeOp F Γf ρ V) x r = ∑ l : Fin 4, Γf.γ x r ρ l * V x l := rfl

/-- 协变差分算子（离散协变导数）。
    物理含义：D_ρ = 移位 − 恒等 + 规范作用，
    即 (D_ρ V)(x) = V(stepD ρ x) − V(x) + Γ_ρ(x)·V(x)
    ——沿 RecObj step 的有限差分导数 ∂̃_ρ 加联络项
    （sorry_closure_roadmap.md §3.6 真值路径的算子实现）。 -/
noncomputable def covDiffOp (F : FrameRecObj) (Γf : GammaField F) (ρ : Fin 4) :
    Module.End ℝ (VecField F) :=
  shiftOp F ρ + gaugeOp F Γf ρ - 1

/-- 曲率算子：协变差分交换子。
    物理含义：F_{μν} = D_μ D_ν − D_ν D_μ——
    连续曲率 R_{μν} = [∇_μ, ∇_ν] 的离散对应。 -/
noncomputable def curvatureOp (F : FrameRecObj) (Γf : GammaField F)
    (μ ν : Fin 4) : Module.End ℝ (VecField F) :=
  covDiffOp F Γf μ * covDiffOp F Γf ν - covDiffOp F Γf ν * covDiffOp F Γf μ

-- ============================================================
-- §26.4 离散第二 Bianchi 恒等式（算子形式，主定理）
-- ============================================================
-- 数学内容：任意三个自同态的 Jacobi 恒等式
--   [A,[B,C]] + [B,[C,A]] + [C,[A,B]] = 0。
-- 这是**无条件精确**的纯非交换恒等式——
-- 无挠性、step 对易、度量相容均不必需；
-- 这些假设只进入分量级解释（§26.5）与连续极限。

/-- 抽象 Jacobi 恒等式：任意环上三个元素的循环交换子和为零。
    纯非交换恒等式，对任意加法群 + 双线性结合乘法成立（Bianchi 的代数核心）。
    对一般向量空间 V 陈述（noncomm_ring 在此通用形态下闭合）。 -/
theorem end_jacobi_cyclic {V : Type*} [AddCommGroup V] [Module ℝ V]
    (A B C : Module.End ℝ V) :
    A * (B * C - C * B) - (B * C - C * B) * A
      + (B * (C * A - A * C) - (C * A - A * C) * B)
      + (C * (A * B - B * A) - (A * B - B * A) * C) = 0 := by
  noncomm_ring

/-- 离散第二 Bianchi 恒等式（算子形式）。
    物理含义：沿任意三个方向的协变差分满足
      Σ_cyc(ρ,μ,ν) [D_ρ, F_{μν}] = 0
    其中 F_{μν} = [D_μ, D_ν] 为曲率算子。
    这是连续第二 Bianchi 恒等式
      ∇_[ρ R_{μν]] = 0
    在离散联络代数中的精确对应——
    守恒律的载体（被证伪的点值骨架所缺失的算子结构）。
    证明：Jacobi 恒等式（end_jacobi_cyclic 的实例）。 -/
theorem discrete_second_bianchi_operator (F : FrameRecObj)
    (Γf : GammaField F) (ρ μ ν : Fin 4) :
    (covDiffOp F Γf ρ * curvatureOp F Γf μ ν - curvatureOp F Γf μ ν * covDiffOp F Γf ρ)
      + (covDiffOp F Γf μ * curvatureOp F Γf ν ρ - curvatureOp F Γf ν ρ * covDiffOp F Γf μ)
      + (covDiffOp F Γf ν * curvatureOp F Γf ρ μ - curvatureOp F Γf ρ μ * covDiffOp F Γf ν)
    = 0 := by
  unfold curvatureOp
  exact end_jacobi_cyclic (covDiffOp F Γf ρ) (covDiffOp F Γf μ) (covDiffOp F Γf ν)

-- ============================================================
-- §26.5 移位算子对易性与曲率的分量展开
-- ============================================================

/-- 移位算子对易：step 对易假设 ⟹ 移位算子交换。
    物理含义：格点上沿不同方向的平移可交换
    （连续极限 ∂_μ∂_σ = ∂_σ∂_μ 的离散对应）。 -/
theorem shiftOp_commute (F : FrameRecObj) (h : StepsCommute F) (ρ σ : Fin 4) :
    shiftOp F ρ * shiftOp F σ = shiftOp F σ * shiftOp F ρ := by
  apply LinearMap.ext
  intro V
  funext x r
  exact congrArg (fun y => V y r) (h σ ρ x)

/-- 曲率算子的完整分量展开（无假设，双移位项显式保留）。
    物理含义：F_{μν} V(x) 的逐点展开为
      V(stepD ν (stepD μ x)) − V(stepD μ (stepD ν x))   [双移位修正项，对易假设下消失]
      + ∂̃_μ Γ_ν(x)·V(stepD μ x) − ∂̃_ν Γ_μ(x)·V(stepD ν x)
      + [Γ_μ, Γ_ν](x)·V(x)
    其中 ∂̃_μ Γ_ν(x) := Γ_ν(stepD μ x) − Γ_ν(x)。
    第三、四、五项正是连续曲率的离散对应：
    ∂_μΓ_ν − ∂_νΓ_μ + [Γ_μ, Γ_ν]。
    修正（双移位项与场在移位点的取值）为 O(a) 量级，
    连续极限 a → 0 时消失（数值验证 |B|/|R| ∝ 1/n²，
    numerical/phase16b_discrete_bianchi.py）。 -/
theorem curvature_op_apply (F : FrameRecObj) (Γf : GammaField F) (μ ν : Fin 4)
    (V : VecField F) (x : F.X.T) (r : Fin 4) :
    (curvatureOp F Γf μ ν) V x r =
      V (F.stepD ν (F.stepD μ x)) r - V (F.stepD μ (F.stepD ν x)) r
      + sum4 (fun l => (Γf.γ (F.stepD μ x) r ν l - Γf.γ x r ν l) * V (F.stepD μ x) l)
      - sum4 (fun l => (Γf.γ (F.stepD ν x) r μ l - Γf.γ x r μ l) * V (F.stepD ν x) l)
      + sum4 (fun l =>
          sum4 (fun m =>
            Γf.γ x r μ m * Γf.γ x m ν l - Γf.γ x r ν m * Γf.γ x m μ l) * V x l) := by
  simp only [curvatureOp, covDiffOp, Module.End.mul_apply, LinearMap.sub_apply,
    LinearMap.add_apply, Module.End.one_apply, shiftOp_apply, gaugeOp_apply,
    Pi.add_apply, Pi.sub_apply, ← sum4_eq_finset_sum, sum4]
  ring

/-- 曲率分量展开（step 对易假设下）：双移位修正项消失。
    物理含义：格点平直（方向 step 对易）时，
    曲率算子退化为"差分联络 + 交换子"的纯局域形式——
    与连续曲率 R_{μν} = ∂_μΓ_ν − ∂_νΓ_μ + [Γ_μ,Γ_ν] 逐项对应。 -/
theorem curvature_op_apply_comm (F : FrameRecObj) (Γf : GammaField F)
    (h : StepsCommute F) (μ ν : Fin 4)
    (V : VecField F) (x : F.X.T) (r : Fin 4) :
    (curvatureOp F Γf μ ν) V x r =
      sum4 (fun l => (Γf.γ (F.stepD μ x) r ν l - Γf.γ x r ν l) * V (F.stepD μ x) l)
      - sum4 (fun l => (Γf.γ (F.stepD ν x) r μ l - Γf.γ x r μ l) * V (F.stepD ν x) l)
      + sum4 (fun l =>
          sum4 (fun m =>
            Γf.γ x r μ m * Γf.γ x m ν l - Γf.γ x r ν m * Γf.γ x m μ l) * V x l) := by
  rw [curvature_op_apply, h ν μ x, sub_self, zero_add]

end MUFPF
