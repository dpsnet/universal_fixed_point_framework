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
import Mathlib.Data.Fin.VecNotation
import Mathlib.Tactic.FinCases
import Mathlib.Algebra.Module.Pi
import Mathlib.Algebra.Module.LinearMap.End
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NoncommRing
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Algebra.BigOperators.Ring.Finset
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
  ring_nf

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

-- ============================================================
-- §26.6 常 Γ 场桥接：算子曲率 ⟹ 点值骨架曲率
-- ============================================================
-- 里程碑 (a)（sorry_closure_roadmap.md §3.6 剩余里程碑）：
-- 常 Γ 场（沿方向 step 不变）+ step 对易时，曲率算子退化为
-- 骨架曲率的逐点乘法算子；骨架层第二 Bianchi 成立（无挠 + ring）。
-- 这把 §26.4 的算子级主定理与 SpectralMetric.lean 的点值骨架
-- second_bianchi_discrete 连接为同一结构的两个层级。

/-- 逐点常值性：Γ 沿任意方向 step 不变。
    物理含义：均匀联络（平移对称）——∂̃_ρ Γ = 0 的离散对应。 -/
def GammaConstant (F : FrameRecObj) (Γf : GammaField F) : Prop :=
  ∀ ρ (x : F.X.T) r m n, Γf.γ (F.stepD ρ x) r m n = Γf.γ x r m n

/-- 骨架曲率（点值，riemannExplicit 的逐点形态）：
    R̂^r_{sμν}(x) = Σ_l Γ^r_{μl}(x) Γ^l_{νs}(x) − Σ_l Γ^r_{νl}(x) Γ^l_{μs}(x)。
    物理含义：丢弃 ∂̃ 项后的纯代数曲率核心——
    常 Γ 场时与算子曲率重合（curvature_op_constant_field）。 -/
def skeletonCurvature (F : FrameRecObj)
    (γ : F.X.T → Fin 4 → Fin 4 → Fin 4 → ℝ)
    (x : F.X.T) (r s μ ν : Fin 4) : ℝ :=
  sum4 (fun l => γ x r μ l * γ x l ν s) - sum4 (fun l => γ x r ν l * γ x l μ s)

/-- 骨架联络作用（点值 connectionAction 的逐点形态）：
    (connA_ρ T)^r_s = Σ_l Γ^r_{ρl} T^l_s − Σ_l Γ^l_{ρs} T^r_l。 -/
def skeletonConnA (F : FrameRecObj)
    (γ : F.X.T → Fin 4 → Fin 4 → Fin 4 → ℝ)
    (x : F.X.T) (ρ r s : Fin 4) (T : Fin 4 → Fin 4 → ℝ) : ℝ :=
  sum4 (fun l => γ x r ρ l * T l s) - sum4 (fun l => γ x l ρ s * T r l)

/-- 骨架第二 Bianchi 被积式：联络作用对 (ρ, μ, ν) 的循环和。 -/
def skeletonSecondBianchi (F : FrameRecObj)
    (γ : F.X.T → Fin 4 → Fin 4 → Fin 4 → ℝ)
    (x : F.X.T) (r s ρ μ ν : Fin 4) : ℝ :=
  skeletonConnA F γ x ρ r s (fun a b => skeletonCurvature F γ x a b μ ν)
    + skeletonConnA F γ x μ r s (fun a b => skeletonCurvature F γ x a b ν ρ)
    + skeletonConnA F γ x ν r s (fun a b => skeletonCurvature F γ x a b ρ μ)

/-- **桥接引理**：常 Γ 场 + step 对易 ⟹ 曲率算子 = 骨架曲率的逐点乘法：
    (F_{μν} V)(x) = Σ_s R̂^r_{sμν}(x) V^s(x)。
    物理含义：均匀联络下联络的曲率全部来自交换子项
    （差分项 ∂̃Γ 与双移位修正均消失）——
    算子层级（§26.4）退化为点值骨架层级。
    证明：分量展开 + 常值性重写 + ring。 -/
theorem curvature_op_constant_field (F : FrameRecObj) (Γf : GammaField F)
    (h : StepsCommute F) (h_const : GammaConstant F Γf)
    (μ ν : Fin 4) (V : VecField F) (x : F.X.T) (r : Fin 4) :
    (curvatureOp F Γf μ ν) V x r =
      sum4 (fun s => skeletonCurvature F Γf.γ x r s μ ν * V x s) := by
  have hc : ∀ ρ (x : F.X.T) r m n, Γf.γ (F.stepD ρ x) r m n = Γf.γ x r m n := h_const
  rw [curvature_op_apply_comm F Γf h μ ν V x r]
  simp only [hc, sub_self, zero_mul, sum4, skeletonCurvature]
  ring_nf

/-- **骨架层第二 Bianchi 恒等式**（无挠 + 乘法交换律）。
    物理含义：点值骨架曲率的联络作用循环和为零
      Σ_cyc(ρ,μ,ν) connA_ρ R̂_{μν} = 0
    ——与 SpectralMetric.lean 的 second_bianchi_discrete 同构
    （自包含证明，不依赖 SpectralMetric 导入）。
    这是主定理 discrete_second_bianchi_operator 在
    常 Γ 场 + 对易 step 下的点值投影：
    算子 Jacobi 恒等式退化为骨架的代数自洽性。
    证明：sum4 展开 + 无挠性 + ring_nf（~48 个三次单项式两两抵消）。 -/
theorem skeleton_second_bianchi (F : FrameRecObj) (Γf : GammaField F)
    (x : F.X.T) (r s ρ μ ν : Fin 4) :
    skeletonSecondBianchi F Γf.γ x r s ρ μ ν = 0 := by
  simp only [skeletonSecondBianchi, skeletonConnA, skeletonCurvature, sum4,
    Γf.torsion_free]
  ring_nf

-- ============================================================
-- §26.7 度规缩并：骨架层 Einstein 散度（里程碑 (b)）
-- ============================================================
-- 数值预实验（numerical/phase16b_metric_contraction.py，2026-09-12）：
--   1. 离散 Christoffel 公式 Γ^ρ_{μν} = ½ ginv^{ρσ}(∂̃_μ g_{νσ}+∂̃_ν g_{μσ}−∂̃_σ g_{μν})
--      使度量相容残差 A_{ρμν} = ∂̃_ρ g_{μν} − Γ^l_{ρμ}g_{lν} − Γ^l_{ρν}g_{μl}
--      **逐点精确为零**（ginv·g = δ 的逐点收缩，∂̃ 不作用于 ginv）——
--      纯代数恒等式，无需 O(a) 修正（族 P/G 均达机器精度 1e-16）；
--   2. 场层级 Einstein 协变散度 E_ν = Σ_μ(∇̃_μ G^·_ν)^μ **不恒零**：
--      |E|/|G| ~ O(a)（n 倍增减半因子 ~2），且不是 Bianchi 残差
--      度规缩并的倍数（拟合 α≈0，残差 ≈ |E|）——E 是比缩并残差
--      O(a²) 高一阶的离散化 artifact；**场层级不存在恒等式**
--      （开放命题 EinsteinDivergenceFree 维持开放，其离散真值由
--      本节骨架层恒等式 + 连续极限承载）；
--   3. 骨架层（常值场）：无挠 + 度量相容 ⟹ 骨架 Einstein 张量的
--      协变联络作用缩并恒零（ω-联络（Γ^i_{0j}=ω_{ij}, Γ^0_{ij}=−ω_{ij}，
--      ω 反对称）数值精确 0；随机无挠非相容对照全部非零——
--      假设不可去）。
-- 本节形式化 3 的代数核心（曲率斜称 + Ricci 对称）。

/-- 点值骨架曲率（skeletonCurvature 的无标架局部形态，逐点 defeq）。
    注：skeletonCurvature F γ x r s μ ν 的函数体不依赖 F 与 x，
    本副本使骨架层引理摆脱格点语境，纯代数陈述。 -/
def skCurv (γ : Fin 4 → Fin 4 → Fin 4 → ℝ) (r s μ ν : Fin 4) : ℝ :=
  sum4 (fun l => γ r μ l * γ l ν s) - sum4 (fun l => γ r ν l * γ l μ s)

/-- 骨架度规相容（g-斜称形式）：联络 1-形式取值于 𝔰𝔬(g)——
    Σ_a g_{μa} Γ^a_{ρν} + Σ_a g_{νa} Γ^a_{ρμ} = 0。
    物理含义：∇̃_ρ g_{μν} = 0 在常值骨架层（∂̃ = 0）的代数形态。
    数值对应：A_{ρμν} = −Γ^l_{ρμ}g_{lν} − Γ^l_{ρν}g_{μl} = 0
    （g 对称性桥接 g_{μl} = g_{lμ}；phase16b_metric_contraction.py Q1：
    离散 Christoffel 下逐点机器精度为零）。 -/
def SkeletonMetricCompat (γ : Fin 4 → Fin 4 → Fin 4 → ℝ)
    (g : Fin 4 → Fin 4 → ℝ) : Prop :=
  ∀ ρ μ ν, sum4 (fun a => g μ a * γ a ρ ν) + sum4 (fun a => g ν a * γ a ρ μ) = 0

/-- **(gΓ)-交换引理**：相容的直接改写形态——
    Σ_a g_{μa} Γ^a_{ρν} = −Σ_a g_{νa} Γ^a_{ρμ}。 -/
lemma skeleton_g_gamma_exchange (γ : Fin 4 → Fin 4 → Fin 4 → ℝ)
    (g : Fin 4 → Fin 4 → ℝ) (hc : SkeletonMetricCompat γ g) :
    ∀ ρ μ ν, sum4 (fun a => g μ a * γ a ρ ν) = -sum4 (fun a => g ν a * γ a ρ μ) :=
  fun ρ μ ν => by have h := hc ρ μ ν; linarith

/-- **骨架曲率的 g-斜对称性**：相容 + g 对称 ⟹
    Σ_a g_{ra} R̂^a_{sμν} + Σ_a g_{sa} R̂^a_{rμν} = 0
    （降指标曲率 (gR̂)_{rsμν} 对 (r,s) 反对称）。
    物理含义：度量相容联络的曲率算子关于 g 斜称——
    Ricci 对称性与缩并 Bianchi 的代数基石。
    数值对应：phase16b_metric_contraction.py 定理 B 的代数核心。
    证明：g 因子移入内和 → (gΓ)-交换 → 四个二重和按 (a↔l) 对合
    配对（g 对称 + 乘法交换）抵消（G₂ = G₃，G₄ = G₁）。 -/
lemma skeleton_curvature_skew (γ : Fin 4 → Fin 4 → Fin 4 → ℝ)
    (g : Fin 4 → Fin 4 → ℝ) (gsym : ∀ μ ν, g μ ν = g ν μ)
    (hc : SkeletonMetricCompat γ g) (r s μ ν : Fin 4) :
    sum4 (fun a => g r a * skCurv γ a s μ ν)
      + sum4 (fun a => g s a * skCurv γ a r μ ν) = 0 := by
  have hex := skeleton_g_gamma_exchange γ g hc
  -- 四个碎片：g_{ra} Γ^a_{μl} 型因子经 (gΓ)-交换移到另一 Γ 上
  have p1 : sum4 (fun a => g r a * sum4 (fun l => γ a μ l * γ l ν s))
      = -sum4 (fun l => sum4 (fun a => g l a * γ a μ r * γ l ν s)) := by
    have key1 : ∀ a : Fin 4, g r a * ∑ l : Fin 4, γ a μ l * γ l ν s
        = ∑ l : Fin 4, g r a * (γ a μ l * γ l ν s) :=
      fun a => Finset.mul_sum Finset.univ (fun l => γ a μ l * γ l ν s) (g r a)
    have e1 : ∀ l : Fin 4, (∑ a : Fin 4, g r a * (γ a μ l * γ l ν s))
        = -∑ a : Fin 4, g l a * γ a μ r * γ l ν s := fun l => by
      rw [Finset.sum_congr rfl (fun a _ => (mul_assoc (g r a) (γ a μ l) (γ l ν s)).symm),
        ← Finset.sum_mul Finset.univ (fun a => g r a * γ a μ l) (γ l ν s)]
      have h := hex μ r l
      rw [sum4_eq_finset_sum, sum4_eq_finset_sum] at h
      rw [h, neg_mul, Finset.sum_mul Finset.univ (fun a => g l a * γ a μ r) (γ l ν s)]
    simp only [sum4_eq_finset_sum]
    rw [Finset.sum_congr rfl (fun a _ => key1 a), Finset.sum_comm,
      ← Finset.sum_neg_distrib, Finset.sum_congr rfl (fun l _ => e1 l)]
  have p2 : sum4 (fun a => g r a * sum4 (fun l => γ a ν l * γ l μ s))
      = -sum4 (fun l => sum4 (fun a => g l a * γ a ν r * γ l μ s)) := by
    have key2 : ∀ a : Fin 4, g r a * ∑ l : Fin 4, γ a ν l * γ l μ s
        = ∑ l : Fin 4, g r a * (γ a ν l * γ l μ s) :=
      fun a => Finset.mul_sum Finset.univ (fun l => γ a ν l * γ l μ s) (g r a)
    have e2 : ∀ l : Fin 4, (∑ a : Fin 4, g r a * (γ a ν l * γ l μ s))
        = -∑ a : Fin 4, g l a * γ a ν r * γ l μ s := fun l => by
      rw [Finset.sum_congr rfl (fun a _ => (mul_assoc (g r a) (γ a ν l) (γ l μ s)).symm),
        ← Finset.sum_mul Finset.univ (fun a => g r a * γ a ν l) (γ l μ s)]
      have h := hex ν r l
      rw [sum4_eq_finset_sum, sum4_eq_finset_sum] at h
      rw [h, neg_mul, Finset.sum_mul Finset.univ (fun a => g l a * γ a ν r) (γ l μ s)]
    simp only [sum4_eq_finset_sum]
    rw [Finset.sum_congr rfl (fun a _ => key2 a), Finset.sum_comm,
      ← Finset.sum_neg_distrib, Finset.sum_congr rfl (fun l _ => e2 l)]
  have p3 : sum4 (fun a => g s a * sum4 (fun l => γ a μ l * γ l ν r))
      = -sum4 (fun l => sum4 (fun a => g l a * γ a μ s * γ l ν r)) := by
    have key3 : ∀ a : Fin 4, g s a * ∑ l : Fin 4, γ a μ l * γ l ν r
        = ∑ l : Fin 4, g s a * (γ a μ l * γ l ν r) :=
      fun a => Finset.mul_sum Finset.univ (fun l => γ a μ l * γ l ν r) (g s a)
    have e3 : ∀ l : Fin 4, (∑ a : Fin 4, g s a * (γ a μ l * γ l ν r))
        = -∑ a : Fin 4, g l a * γ a μ s * γ l ν r := fun l => by
      rw [Finset.sum_congr rfl (fun a _ => (mul_assoc (g s a) (γ a μ l) (γ l ν r)).symm),
        ← Finset.sum_mul Finset.univ (fun a => g s a * γ a μ l) (γ l ν r)]
      have h := hex μ s l
      rw [sum4_eq_finset_sum, sum4_eq_finset_sum] at h
      rw [h, neg_mul, Finset.sum_mul Finset.univ (fun a => g l a * γ a μ s) (γ l ν r)]
    simp only [sum4_eq_finset_sum]
    rw [Finset.sum_congr rfl (fun a _ => key3 a), Finset.sum_comm,
      ← Finset.sum_neg_distrib, Finset.sum_congr rfl (fun l _ => e3 l)]
  have p4 : sum4 (fun a => g s a * sum4 (fun l => γ a ν l * γ l μ r))
      = -sum4 (fun l => sum4 (fun a => g l a * γ a ν s * γ l μ r)) := by
    have key4 : ∀ a : Fin 4, g s a * ∑ l : Fin 4, γ a ν l * γ l μ r
        = ∑ l : Fin 4, g s a * (γ a ν l * γ l μ r) :=
      fun a => Finset.mul_sum Finset.univ (fun l => γ a ν l * γ l μ r) (g s a)
    have e4 : ∀ l : Fin 4, (∑ a : Fin 4, g s a * (γ a ν l * γ l μ r))
        = -∑ a : Fin 4, g l a * γ a ν s * γ l μ r := fun l => by
      rw [Finset.sum_congr rfl (fun a _ => (mul_assoc (g s a) (γ a ν l) (γ l μ r)).symm),
        ← Finset.sum_mul Finset.univ (fun a => g s a * γ a ν l) (γ l μ r)]
      have h := hex ν s l
      rw [sum4_eq_finset_sum, sum4_eq_finset_sum] at h
      rw [h, neg_mul, Finset.sum_mul Finset.univ (fun a => g l a * γ a ν s) (γ l μ r)]
    simp only [sum4_eq_finset_sum]
    rw [Finset.sum_congr rfl (fun a _ => key4 a), Finset.sum_comm,
      ← Finset.sum_neg_distrib, Finset.sum_congr rfl (fun l _ => e4 l)]
  rw [show sum4 (fun a => g r a * skCurv γ a s μ ν)
      = sum4 (fun a => g r a * sum4 (fun l => γ a μ l * γ l ν s))
        - sum4 (fun a => g r a * sum4 (fun l => γ a ν l * γ l μ s)) from by
        simp only [skCurv, mul_sub, sum4_eq_finset_sum, Finset.sum_sub_distrib],
    show sum4 (fun a => g s a * skCurv γ a r μ ν)
      = sum4 (fun a => g s a * sum4 (fun l => γ a μ l * γ l ν r))
        - sum4 (fun a => g s a * sum4 (fun l => γ a ν l * γ l μ r)) from by
        simp only [skCurv, mul_sub, sum4_eq_finset_sum, Finset.sum_sub_distrib],
    sub_eq_add_neg, sub_eq_add_neg, p1, p2, p3, p4, neg_neg, neg_neg]
  simp only [sum4_eq_finset_sum]
  -- 对合配对：G₂ = G₃、G₄ = G₁（g 对称 + 乘法交换 + 哑元交换）
  have hG23 : (∑ l : Fin 4, ∑ a : Fin 4, (g l a * γ a ν r * γ l μ s))
      = ∑ l : Fin 4, ∑ a : Fin 4, (g l a * γ a μ s * γ l ν r) := by
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro l _
    apply Finset.sum_congr rfl
    intro a _
    rw [gsym a l]
    ring
  have hG41 : (∑ l : Fin 4, ∑ a : Fin 4, (g l a * γ a ν s * γ l μ r))
      = ∑ l : Fin 4, ∑ a : Fin 4, (g l a * γ a μ r * γ l ν s) := by
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro l _
    apply Finset.sum_congr rfl
    intro a _
    rw [gsym a l]
    ring
  linarith [hG23, hG41]

/-- **骨架第一 Bianchi**（代数形式，无挠）：
    R̂^r_{sμν} + R̂^r_{μνs} + R̂^r_{νsμ} = 0。
    证明：sum4 展开 + 无挠 + ring_nf（与 skeleton_second_bianchi 同技术）。 -/
lemma skeleton_first_bianchi (γ : Fin 4 → Fin 4 → Fin 4 → ℝ)
    (tf : ∀ r m n, γ r m n = γ r n m) (r s μ ν : Fin 4) :
    skCurv γ r s μ ν + skCurv γ r μ ν s + skCurv γ r ν s μ = 0 := by
  simp only [skCurv, sum4, tf]
  ring_nf

/-- **骨架 Ricci 对称性**：相容 + g/ginv 对称 + 逆对 ⟹
    Riĉ_{σν} = Riĉ_{νσ}，其中 Riĉ_{σν} := Σ_r R̂^r_{σrν}。
    物理含义：度量相容联络的 Ricci 张量对称——Einstein 张量
    G = Riĉ − ½gR 对称性的直接来源。
    证明：两步。(i) 第一 Bianchi + 末两位反对称 ⟹
    Riĉ_{σν} − Riĉ_{νσ} = −Σ_r R̂^r_{rνσ}（δ-迹）；
    (ii) δ-迹经"斜称 × g 对称"的 g-迹归零 + ginv 逆对与
    ginv 对称把 g-迹归零传递为 δ-迹归零。 -/
lemma skeleton_ricci_symmetric (γ : Fin 4 → Fin 4 → Fin 4 → ℝ)
    (tf : ∀ r m n, γ r m n = γ r n m)
    (g : Fin 4 → Fin 4 → ℝ) (gsym : ∀ μ ν, g μ ν = g ν μ)
    (ginv : Fin 4 → Fin 4 → ℝ) (hginv : ∀ μ ν, ginv μ ν = ginv ν μ)
    (hinv : ∀ μ ν,
      sum4 (fun σ => ginv μ σ * g σ ν) = if μ = ν then 1 else 0)
    (hc : SkeletonMetricCompat γ g) (σ ν : Fin 4) :
    sum4 (fun r => skCurv γ r σ r ν) = sum4 (fun r => skCurv γ r ν r σ) := by
  -- 第一步：A − B = −δ-迹
  have hper : ∀ r : Fin 4, skCurv γ r σ r ν - skCurv γ r ν r σ
      = -skCurv γ r r ν σ := by
    intro r
    have e1 := skeleton_first_bianchi γ tf r σ r ν
    have e2 := skeleton_first_bianchi γ tf r ν r σ
    have e3 : skCurv γ r r σ ν = -skCurv γ r r ν σ := by
      simp only [skCurv, sum4]; ring
    have e4 : skCurv γ r ν σ r = -skCurv γ r ν r σ := by
      simp only [skCurv, sum4]; ring
    have e5 : skCurv γ r σ ν r = -skCurv γ r σ r ν := by
      simp only [skCurv, sum4]; ring
    simp only [skCurv, sum4] at e1 e2 e3 e4 e5 ⊢
    linarith
  have hAB : (∑ r : Fin 4, skCurv γ r σ r ν) - (∑ r : Fin 4, skCurv γ r ν r σ)
      = -∑ r : Fin 4, skCurv γ r r ν σ := by
    rw [← Finset.sum_sub_distrib, ← Finset.sum_neg_distrib]
    apply Finset.sum_congr rfl
    intro r _
    exact hper r
  -- 第二步：δ-迹归零
  have htrace : (∑ r : Fin 4, skCurv γ r r ν σ) = 0 := by
    have hskew := skeleton_curvature_skew γ g gsym hc
    -- δ-插入：x_r = Σ_a (Σ_c ginv r c g c a) · x_a（逆对逐点给出 δ_{ra}）
    have hins' : ∀ r : Fin 4, skCurv γ r r ν σ
        = ∑ a : Fin 4, (∑ c : Fin 4, ginv r c * g c a) * skCurv γ a r ν σ := by
      intro r
      have h1 : (∑ a : Fin 4, (if r = a then (1:ℝ) else 0) * skCurv γ a r ν σ)
          = (if r = r then (1:ℝ) else 0) * skCurv γ r r ν σ :=
        Finset.sum_eq_single (s := Finset.univ)
          (f := fun a => (if r = a then (1:ℝ) else 0) * skCurv γ a r ν σ) r
          (fun b _ hb => by rw [if_neg (Ne.symm hb), zero_mul])
          (fun h => absurd (Finset.mem_univ r) h)
      have hdelta : ∀ a : Fin 4, (if r = a then (1:ℝ) else 0)
          = ∑ c : Fin 4, ginv r c * g c a := by
        intro a
        have h := hinv r a
        rw [sum4_eq_finset_sum] at h
        exact h.symm
      calc skCurv γ r r ν σ
          = (if r = r then (1:ℝ) else 0) * skCurv γ r r ν σ := by rw [if_pos rfl, one_mul]
        _ = ∑ a : Fin 4, (if r = a then (1:ℝ) else 0) * skCurv γ a r ν σ := h1.symm
        _ = ∑ a : Fin 4, (∑ c : Fin 4, ginv r c * g c a) * skCurv γ a r ν σ :=
          Finset.sum_congr rfl (fun a _ => by rw [hdelta a])
    rw [Finset.sum_congr rfl (fun r _ => hins' r)]
    -- step1：内层重排 + ginv 提出，化为 W 形
    have step1 : (∑ r : Fin 4, ∑ a : Fin 4,
          (∑ c : Fin 4, ginv r c * g c a) * skCurv γ a r ν σ)
        = ∑ r : Fin 4, ∑ c : Fin 4, ginv r c
          * (∑ a : Fin 4, g c a * skCurv γ a r ν σ) := by
      apply Finset.sum_congr rfl
      intro r _
      rw [Finset.sum_congr rfl (fun a _ =>
        Finset.sum_mul Finset.univ (fun c => ginv r c * g c a) (skCurv γ a r ν σ)),
        Finset.sum_comm]
      apply Finset.sum_congr rfl
      intro c _
      rw [Finset.sum_congr rfl (fun a _ =>
        mul_assoc (ginv r c) (g c a) (skCurv γ a r ν σ)), ← Finset.mul_sum]
    -- hswap：内层 Σ_a g c a R̂^a_{rνσ} 由斜称重写为 −Σ_a g r a R̂^a_{cνσ}
    have hsw : ∀ r c : Fin 4, ginv r c * (∑ a : Fin 4, g c a * skCurv γ a r ν σ)
        = -(ginv r c * (∑ a : Fin 4, g r a * skCurv γ a c ν σ)) := by
      intro r c
      have hs := hskew c r ν σ
      rw [sum4_eq_finset_sum, sum4_eq_finset_sum] at hs
      rw [show (∑ a : Fin 4, g c a * skCurv γ a r ν σ)
          = -(∑ a : Fin 4, g r a * skCurv γ a c ν σ) from by linarith [hs]]
      rw [mul_neg]
    have hswap : (∑ r : Fin 4, ∑ c : Fin 4, ginv r c
          * (∑ a : Fin 4, g c a * skCurv γ a r ν σ))
        = -∑ r : Fin 4, ∑ c : Fin 4, ginv r c
          * (∑ a : Fin 4, g r a * skCurv γ a c ν σ) := by
      rw [← Finset.sum_neg_distrib]
      apply Finset.sum_congr rfl
      intro r _
      rw [← Finset.sum_neg_distrib]
      apply Finset.sum_congr rfl
      intro c _
      exact hsw r c
    -- hinvol：哑元 (r,c) 对合 + ginv 对称 ⟹ 两级内和恒等
    have hinvol : (∑ r : Fin 4, ∑ c : Fin 4, ginv r c
          * (∑ a : Fin 4, g r a * skCurv γ a c ν σ))
        = ∑ r : Fin 4, ∑ c : Fin 4, ginv r c
          * (∑ a : Fin 4, g c a * skCurv γ a r ν σ) := by
      have h1 : (∑ r : Fin 4, ∑ c : Fin 4, ginv r c
            * (∑ a : Fin 4, g r a * skCurv γ a c ν σ))
          = ∑ c : Fin 4, ∑ r : Fin 4, ginv r c
            * (∑ a : Fin 4, g r a * skCurv γ a c ν σ) := Finset.sum_comm
      rw [h1]
      apply Finset.sum_congr rfl
      intro X _
      apply Finset.sum_congr rfl
      intro Y _
      rw [hginv Y X]
    linarith [step1, hswap, hinvol]
  rw [sum4_eq_finset_sum, sum4_eq_finset_sum]
  linarith [hAB, htrace]

/-- δ-型求和求值：Σ_σ (if σ = μ then 1 else 0) · X σ = X μ。
    数值对应：phase16b_metric_contraction.py 中 ginv·g = δ 的逐点求值。
    证明：sum_eq_single 显式 f 实例 + if_pos（保留 if 形式，calc 闭合——
    if μ = μ 对自由变量不可定义归约）。 -/
lemma sum4_ite_eq' (μ : Fin 4) (X : Fin 4 → ℝ) :
    sum4 (fun σ => (if σ = μ then (1:ℝ) else 0) * X σ) = X μ := by
  rw [sum4_eq_finset_sum]
  have h1 : (∑ σ : Fin 4, (if σ = μ then (1:ℝ) else 0) * X σ)
      = (if μ = μ then (1:ℝ) else 0) * X μ :=
    Finset.sum_eq_single (s := Finset.univ)
      (f := fun σ => (if σ = μ then (1:ℝ) else 0) * X σ) μ
      (fun b _ hb => by rw [if_neg hb, zero_mul])
      (fun h => absurd (Finset.mem_univ μ) h)
  calc (∑ σ : Fin 4, (if σ = μ then (1:ℝ) else 0) * X σ)
      = (if μ = μ then (1:ℝ) else 0) * X μ := h1
    _ = X μ := by rw [if_pos rfl, one_mul]

/-- g–ginv 缩并（交换序）：Σ_a g_{μa} ginv^{aσ} = δ_{σμ}。
    由逆对 hinv（ginv·g 序）经 g/ginv 对称逐项换位。 -/
lemma contraction_g_ginv (g ginv : Fin 4 → Fin 4 → ℝ)
    (gsym : ∀ μ ν, g μ ν = g ν μ) (hginv : ∀ μ ν, ginv μ ν = ginv ν μ)
    (hinv : ∀ μ ν, sum4 (fun σ => ginv μ σ * g σ ν) = if μ = ν then 1 else 0)
    (μ σ : Fin 4) :
    sum4 (fun a => g μ a * ginv a σ) = if σ = μ then 1 else 0 := by
  have h := hinv σ μ
  rw [sum4_eq_finset_sum] at h
  calc sum4 (fun a => g μ a * ginv a σ)
      = ∑ a : Fin 4, ginv σ a * g a μ := by
        rw [sum4_eq_finset_sum]
        apply Finset.sum_congr rfl
        intro a _
        rw [gsym μ a, hginv a σ, mul_comm]
    _ = if σ = μ then 1 else 0 := h

/-- 离散 Christoffel 公式（∂̃ 的抽象骨架形态）：
    Γ^ρ_{μν} = ½ Σ_σ ginv^{ρσ} (∂̃_μ g_{νσ} + ∂̃_ν g_{μσ} − ∂̃_σ g_{μν})，
    其中 d ρ μ ν 表示 ∂̃_ρ g_{μν}（g 对称 ⟹ d 对后两指标对称）。 -/
noncomputable def christoffelDisc (ginv : Fin 4 → Fin 4 → ℝ)
    (d : Fin 4 → Fin 4 → Fin 4 → ℝ) (ρ μ ν : Fin 4) : ℝ :=
  (1/2) * sum4 (fun σ => ginv ρ σ * (d μ ν σ + d ν μ σ - d σ μ ν))

/-- **离散 Christoffel 公式的逐点度量相容**（纯代数恒等式）：
    ∂̃_ρ g_{μν} = Σ_a (g_{μa} Γ^a_{ρν} + g_{νa} Γ^a_{ρμ})。
    数值对应：phase16b_metric_contraction.py Q1（A ≡ 0 逐点精确 ~1e-16，
    ginv·g = δ 不经过 ∂̃）。
    证明骨架：g 因子与 ½ 移入 σ-和（mul_sum）→ 双和交换（sum_comm）→
    缩并 δ（contraction_g_ginv）→ δ 求值（sum4_ite_eq'）→
    d 对称（dsym）+ ring 配对抵消。 -/
lemma discrete_christoffel_metric_compatible
    (g ginv : Fin 4 → Fin 4 → ℝ) (d : Fin 4 → Fin 4 → Fin 4 → ℝ)
    (gsym : ∀ μ ν, g μ ν = g ν μ) (hginv : ∀ μ ν, ginv μ ν = ginv ν μ)
    (hinv : ∀ μ ν, sum4 (fun σ => ginv μ σ * g σ ν) = if μ = ν then 1 else 0)
    (dsym : ∀ ρ μ ν, d ρ μ ν = d ρ ν μ) (ρ μ ν : Fin 4) :
    sum4 (fun a => g μ a * christoffelDisc ginv d a ρ ν
        + g ν a * christoffelDisc ginv d a ρ μ) = d ρ μ ν := by
  have hctr : ∀ m s : Fin 4, (∑ a : Fin 4, g m a * ginv a s)
      = if s = m then 1 else 0 := by
    intro m s
    have h := contraction_g_ginv g ginv gsym hginv hinv m s
    rw [sum4_eq_finset_sum] at h
    exact h
  have hd : ∀ m : Fin 4, ∀ X : Fin 4 → ℝ,
      (∑ σ : Fin 4, (if σ = m then (1:ℝ) else 0) * X σ) = X m := by
    intro m X
    have h := sum4_ite_eq' m X
    rw [sum4_eq_finset_sum] at h
    exact h
  have key1 : ∀ a : Fin 4, g μ a * ((1/2) * ∑ σ : Fin 4,
        ginv a σ * (d ρ ν σ + d ν ρ σ - d σ ρ ν))
      = ∑ σ : Fin 4, (1/2 * (g μ a * ginv a σ))
        * (d ρ ν σ + d ν ρ σ - d σ ρ ν) := fun a => by
    rw [Finset.mul_sum Finset.univ (fun σ => ginv a σ * (d ρ ν σ + d ν ρ σ - d σ ρ ν)) (1/2 : ℝ),
      Finset.mul_sum Finset.univ
        (fun σ => (1/2 : ℝ) * (ginv a σ * (d ρ ν σ + d ν ρ σ - d σ ρ ν))) (g μ a)]
    apply Finset.sum_congr rfl
    intro σ _
    ring
  have key2 : ∀ a : Fin 4, g ν a * ((1/2) * ∑ σ : Fin 4,
        ginv a σ * (d ρ μ σ + d μ ρ σ - d σ ρ μ))
      = ∑ σ : Fin 4, (1/2 * (g ν a * ginv a σ))
        * (d ρ μ σ + d μ ρ σ - d σ ρ μ) := fun a => by
    rw [Finset.mul_sum Finset.univ (fun σ => ginv a σ * (d ρ μ σ + d μ ρ σ - d σ ρ μ)) (1/2 : ℝ),
      Finset.mul_sum Finset.univ
        (fun σ => (1/2 : ℝ) * (ginv a σ * (d ρ μ σ + d μ ρ σ - d σ ρ μ))) (g ν a)]
    apply Finset.sum_congr rfl
    intro σ _
    ring
  have swap1 : (∑ a : Fin 4, ∑ σ : Fin 4, (1/2 * (g μ a * ginv a σ))
        * (d ρ ν σ + d ν ρ σ - d σ ρ ν))
      = ∑ σ : Fin 4, ∑ a : Fin 4, (1/2 * (g μ a * ginv a σ))
        * (d ρ ν σ + d ν ρ σ - d σ ρ ν) := Finset.sum_comm
  have swap2 : (∑ a : Fin 4, ∑ σ : Fin 4, (1/2 * (g ν a * ginv a σ))
        * (d ρ μ σ + d μ ρ σ - d σ ρ μ))
      = ∑ σ : Fin 4, ∑ a : Fin 4, (1/2 * (g ν a * ginv a σ))
        * (d ρ μ σ + d μ ρ σ - d σ ρ μ) := Finset.sum_comm
  have ctr1 : ∀ s : Fin 4, (∑ a : Fin 4, (1/2 * (g μ a * ginv a s))
        * (d ρ ν s + d ν ρ s - d s ρ ν))
      = (if s = μ then (1:ℝ) else 0)
        * ((1/2) * (d ρ ν s + d ν ρ s - d s ρ ν)) := fun s => by
    rw [← Finset.sum_mul Finset.univ (fun a => 1/2 * (g μ a * ginv a s))
        (d ρ ν s + d ν ρ s - d s ρ ν),
      ← Finset.mul_sum Finset.univ (fun a => g μ a * ginv a s) (1/2 : ℝ), hctr μ s]
    ring
  have ctr2 : ∀ s : Fin 4, (∑ a : Fin 4, (1/2 * (g ν a * ginv a s))
        * (d ρ μ s + d μ ρ s - d s ρ μ))
      = (if s = ν then (1:ℝ) else 0)
        * ((1/2) * (d ρ μ s + d μ ρ s - d s ρ μ)) := fun s => by
    rw [← Finset.sum_mul Finset.univ (fun a => 1/2 * (g ν a * ginv a s))
        (d ρ μ s + d μ ρ s - d s ρ μ),
      ← Finset.mul_sum Finset.univ (fun a => g ν a * ginv a s) (1/2 : ℝ), hctr ν s]
    ring
  simp only [christoffelDisc, sum4_eq_finset_sum, Finset.sum_add_distrib]
  rw [Finset.sum_congr rfl (fun a _ => key1 a),
    Finset.sum_congr rfl (fun a _ => key2 a), swap1, swap2,
    Finset.sum_congr rfl (fun s _ => ctr1 s),
    Finset.sum_congr rfl (fun s _ => ctr2 s), hd μ, hd ν]
  show (1/2) * (d ρ ν μ + d ν ρ μ - d μ ρ ν)
      + (1/2) * (d ρ μ ν + d μ ρ ν - d ν ρ μ) = d ρ μ ν
  rw [dsym ρ ν μ]
  ring_nf

/-- 降指标联络 Γ_{abc} := Σ_d g_{ad} Γ^d_{bc}（相容的 (0,2)-型表述载体）。 -/
def skGamma (γ : Fin 4 → Fin 4 → Fin 4 → ℝ) (g : Fin 4 → Fin 4 → ℝ)
    (a b c : Fin 4) : ℝ :=
  sum4 (fun d => g a d * γ d b c)

/-- Γ_{abc} 对 (a,c) 反对称（相容的直接改写）。 -/
lemma skGamma_antisymm (γ : Fin 4 → Fin 4 → Fin 4 → ℝ) (g : Fin 4 → Fin 4 → ℝ)
    (hc : SkeletonMetricCompat γ g) :
    ∀ a b c, skGamma γ g a b c = -skGamma γ g c b a := by
  intro a b c
  have h := hc b a c
  simp only [skGamma]
  linarith

/-- Γ_{abc} 对 (b,c) 对称（无挠的直接改写）。 -/
lemma skGamma_symm23 (γ : Fin 4 → Fin 4 → Fin 4 → ℝ) (g : Fin 4 → Fin 4 → ℝ)
    (tf : ∀ r m n, γ r m n = γ r n m) :
    ∀ a b c, skGamma γ g a b c = skGamma γ g a c b := by
  intro a b c
  simp only [skGamma, sum4_eq_finset_sum]
  apply Finset.sum_congr rfl
  intro d _
  rw [tf d b c]

/-- **澄清性引理（负面结果）**：常值骨架层上，无挠 + 度规相容 ⟹ 联络恒为零。
    轮换论证：Γ_{abc} = Γ_{acb} [无挠] = −Γ_{bca} [反对称] = −Γ_{bac} [无挠]
    = Γ_{cab} [反对称] = Γ_{cba} [无挠] = −Γ_{abc} [反对称]，故 2Γ = 0。
    物理含义：骨架层（∂̃ 缺席）的守恒律研究**必须允许挠率联络**——
    无挠 + 相容的骨架只有零联络，"定理 B"的朴素陈述是空洞的；
    数值上 E_skel = 0 的 ω-联络恰是挠率联络（T^0_{ij} = −2ω_ij）。
    数值对应：phase16b_metric_contraction.py skeleton_layer 对照组。 -/
lemma skGamma_zero_of_torsionfree_compatible (γ : Fin 4 → Fin 4 → Fin 4 → ℝ)
    (g : Fin 4 → Fin 4 → ℝ)
    (tf : ∀ r m n, γ r m n = γ r n m)
    (hc : SkeletonMetricCompat γ g) :
    ∀ a b c, skGamma γ g a b c = 0 := by
  intro a b c
  have anti : ∀ x y z, skGamma γ g x y z = -skGamma γ g z y x :=
    skGamma_antisymm γ g hc
  have sy : ∀ x y z, skGamma γ g x y z = skGamma γ g x z y :=
    skGamma_symm23 γ g tf
  linarith [sy a b c, anti a c b, sy b c a, anti b a c, sy c a b, anti c b a]

-- ============================================================
-- §26.8 恰单零指标族的 Einstein 散度恒等式（方向 (α) 形式化）
-- ============================================================
-- 数值/符号对应（2026-09-11，notes/04 esk_torsion_decomposition.md）：
--   恰单零指标 12 维族 Γ^0_{ij}=D_{ji}, Γ^i_{0j}=C_{ij}, Γ^i_{j0}=D_{ij}
--   （其余分量零，C/D 不需任何对称性——sympy 精确验证），
--   Einstein 散度的空间分量 D_k = Σ_{μ,a} η^{μa} ∇̃_μ G_{ak} (k=1,2,3)
--   多元多项式恒零；时间分量 D₀ = L(C,A)·S + Cub(S) 不恒零。
--   本节形式化空间分量恒等式（sum4 展开 + 矩阵字面量归约 + ring_nf）。

/-- Minkowski 度规 η = diag(−1,1,1,1)（自反逆，升/降指标同一矩阵）。 -/
def mink4 : Fin 4 → Fin 4 → ℝ :=
  ![![-1, 0, 0, 0],
    ![0, 1, 0, 0],
    ![0, 0, 1, 0],
    ![0, 0, 0, 1]]

/-- 恰单零指标联络族（显式 4×4×4 查表形态）：
    Γ^0_{ij}=D_{ji}（0 号块行/列空间部分），Γ^i_{0j}=C_{ij}（i 号块第 0 行），
    Γ^i_{j0}=D_{ij}（i 号块第 0 列），其余为零。
    C D : Fin 4 → Fin 4 → ℝ 任意（仅空间-空间指标出现，无需对称性假设）。 -/
def singleZeroConn (C D : Fin 4 → Fin 4 → ℝ) : Fin 4 → Fin 4 → Fin 4 → ℝ :=
  ![![![0, 0, 0, 0],
      ![0, D 1 1, D 2 1, D 3 1],
      ![0, D 1 2, D 2 2, D 3 2],
      ![0, D 1 3, D 2 3, D 3 3]],
    ![![0, C 1 1, C 1 2, C 1 3],
      ![D 1 1, 0, 0, 0],
      ![D 1 2, 0, 0, 0],
      ![D 1 3, 0, 0, 0]],
    ![![0, C 2 1, C 2 2, C 2 3],
      ![D 2 1, 0, 0, 0],
      ![D 2 2, 0, 0, 0],
      ![D 2 3, 0, 0, 0]],
    ![![0, C 3 1, C 3 2, C 3 3],
      ![D 3 1, 0, 0, 0],
      ![D 3 2, 0, 0, 0],
      ![D 3 3, 0, 0, 0]]]

/-- 骨架 Ricci：Riĉ_{sν} = Σ_r R̂^r_{ s r ν}（skCurv 的 (r,ν) 缩并）。 -/
def skRic (γ : Fin 4 → Fin 4 → Fin 4 → ℝ) (s ν : Fin 4) : ℝ :=
  sum4 (fun r => skCurv γ r s r ν)

/-- 骨架标量曲率：R̂ = Σ_{sν} g^{sν} Riĉ_{sν}。 -/
def skScalar (γ : Fin 4 → Fin 4 → Fin 4 → ℝ) (g : Fin 4 → Fin 4 → ℝ) : ℝ :=
  sum4 (fun s => sum4 (fun ν => g s ν * skRic γ s ν))

/-- 骨架 Einstein 张量：Ĝ_{μν} = Riĉ_{μν} − (1/2) g_{μν} R̂。 -/
noncomputable def skEin (γ : Fin 4 → Fin 4 → Fin 4 → ℝ)
    (g : Fin 4 → Fin 4 → ℝ) (μ ν : Fin 4) : ℝ :=
  skRic γ μ ν - (1/2) * g μ ν * skScalar γ g

/-- 骨架协变联络作用（无 ∂ 项）：∇̃_μ G_{aν} = Σ_l(−Γ^l_{μa}G_{lν} − Γ^l_{μν}G_{al})。 -/
noncomputable def skConnG (γ : Fin 4 → Fin 4 → Fin 4 → ℝ) (g : Fin 4 → Fin 4 → ℝ)
    (μ a ν : Fin 4) : ℝ :=
  sum4 (fun l => -(γ l μ a * skEin γ g l ν) - γ l μ ν * skEin γ g a l)

/-- 骨架 Einstein 散度（第 ν 分量）：D_ν = Σ_{μ,a} g^{μa} ∇̃_μ G_{aν}。 -/
noncomputable def skDiv (γ : Fin 4 → Fin 4 → Fin 4 → ℝ) (g ginv : Fin 4 → Fin 4 → ℝ)
    (ν : Fin 4) : ℝ :=
  sum4 (fun μ => sum4 (fun a => ginv μ a * skConnG γ g μ a ν))

set_option maxHeartbeats 1000000 in
/-- **恰单零指标族空间散度恒等式**（方向 (α) 的 Lean 形式化核心定理）：
    对 singleZeroConn 族，Einstein 散度的空间分量
    D_k = Σ_{μ,a} η^{μa} ∇̃_μ G_{ak}（k = 1, 2, 3）对任意
    C D : Fin 4 → Fin 4 → ℝ 恒为零。
    结构性原因：族内无三空间指标联络分量，散度空间分量的全部单项式
    经 sum4 展开后逐项抵消（~10³ 个三次单项式，ring_nf 闭合）。
    数值对应：phase16b_div4_family.py（sympy 精确，D₁=D₂=D₃≡0）。 -/
theorem single_zero_family_spatial_div_zero (C D : Fin 4 → Fin 4 → ℝ) (k : Fin 3) :
    skDiv (singleZeroConn C D) mink4 mink4 k.succ = 0 := by
  fin_cases k <;>
    (first
      | show skDiv (singleZeroConn C D) mink4 mink4 (1 : Fin 4) = 0
      | show skDiv (singleZeroConn C D) mink4 mink4 (2 : Fin 4) = 0
      | show skDiv (singleZeroConn C D) mink4 mink4 (3 : Fin 4) = 0) <;>
    simp only [skDiv, skConnG, skEin, skScalar, skRic, skCurv, sum4,
      mink4, singleZeroConn, Matrix.cons_val_zero, Matrix.cons_val_one,
      Matrix.cons_val_two, Matrix.cons_val_three,
      Matrix.head_cons, Matrix.tail_cons,
      mul_zero, zero_mul, add_zero, zero_add, neg_zero, sub_zero, zero_sub,
      mul_one, one_mul, one_div]

set_option maxHeartbeats 1000000 in
/-- **ω 联络零点定理（时间分量）**：恰单零指标族内，C 与 D 均反对称
    （即 D = A 为纯 ω 部分、S = 0；挠率 T^0_{ij} = −2A_{ji} 的 ω-联络）时，
    Einstein 散度的时间分量 D₀ = Σ_{μ,a} η^{μa} ∇̃_μ G_{a0} 恒为零。
    与空间分量恒等式（`single_zero_family_spatial_div_zero`）合取即得
    **ω-联络是全散度 D_ν = 0 的零点**——"E_skel 的零点恰是挠率联络"
    的 (α) 方向形式化（族内）。
    前提不可减：数值上 C 保留对称部分时 D₀ ≠ 0（6 项残差，
    phase16b 符号实验 2026-09-12），故 C 反对称是本质条件。
    数值对应：phase16b_eskel_sdecomp.py E_0|_{S=0} ≡ 0。 -/
theorem single_zero_family_time_div_zero_omega (C D : Fin 4 → Fin 4 → ℝ)
    (hC : ∀ i j, C i j = -C j i) (hD : ∀ i j, D i j = -D j i) :
    skDiv (singleZeroConn C D) mink4 mink4 0 = 0 := by
  have c11 : C 1 1 = 0 := by linarith [hC 1 1]
  have c22 : C 2 2 = 0 := by linarith [hC 2 2]
  have c33 : C 3 3 = 0 := by linarith [hC 3 3]
  have d11 : D 1 1 = 0 := by linarith [hD 1 1]
  have d22 : D 2 2 = 0 := by linarith [hD 2 2]
  have d33 : D 3 3 = 0 := by linarith [hD 3 3]
  simp only [skDiv, skConnG, skEin, skScalar, skRic, skCurv, sum4,
    mink4, singleZeroConn, Matrix.cons_val_zero, Matrix.cons_val_one,
    Matrix.cons_val_two, Matrix.cons_val_three,
    Matrix.head_cons, Matrix.tail_cons,
    hC 1 2, hC 1 3, hC 2 3, hD 1 2, hD 1 3, hD 2 3,
    c11, c22, c33, d11, d22, d33,
    mul_zero, zero_mul, add_zero, zero_add, neg_zero, sub_zero, zero_sub,
    mul_one, one_mul, one_div, mul_neg, neg_mul, neg_neg]
  ring

set_option maxHeartbeats 1000000 in
/-- **时间分量挠率泛函分解定理**（方向 (α) 的显式形式化）：恰单零指标族内，
    联络的 (i,j,0)-块写成 D = A + S（A 反对称 = ω 部分，S 对称 = 挠率对称部分），
    C 反对称，则 Einstein 散度的时间分量满足 D₀ = L(C,A)·S + Cub(S)：
    L 对 S 线性、系数为 (C,A) 的二次型（21 项，含 A·C 混合系数）；
    Cub 为只含 S 的 16 项三次型（在 det/tr 标准不变量多项式组合下不分解，
    几何含义待定）；无 S⁰ 项（ω 零点，即 (α)-2）、无 S² 交叉项。
    生成器 numerical/phase16b_d0_lean_gen.py（sympy 校验 D₀ = lin + cub，
    标准原子基底 12 个：C/A 的 i>j 三元组 + S 的 i≤j 六元组）。
    数值对应：phase16b_eskel_sdecomp.py（E_0 对 S 的次数分解）。 -/
theorem single_zero_family_time_div_decomp
    (C A S : Fin 4 → Fin 4 → ℝ)
    (hC : ∀ i j, C i j = -C j i)
    (hA : ∀ i j, A i j = -A j i)
    (hS : ∀ i j, S i j = S j i) :
    skDiv (singleZeroConn C fun i j => A i j + S i j) mink4 mink4 0
      = 2 * (C 2 1) * (A 3 1) * S 2 3 + 2 * (C 3 1) * (A 2 1) * S 2 3
        + 2 * (C 3 1) * (A 3 2) * S 1 2 + 2 * (C 3 2) * (A 3 1) * S 1 2
        + 2 * (A 2 1)^2 * S 3 3 + 6 * (A 2 1) * (A 3 2) * S 1 3
        + 2 * (A 3 1)^2 * S 2 2 + 2 * (A 3 2)^2 * S 1 1
        - 2 * (C 2 1) * (A 2 1) * S 3 3 - 2 * (C 2 1) * (A 3 2) * S 1 3
        - 2 * (C 3 1) * (A 3 1) * S 2 2 - 2 * (C 3 2) * (A 2 1) * S 1 3
        - 2 * (C 3 2) * (A 3 2) * S 1 1 - (A 2 1)^2 * S 1 1
        - (A 2 1)^2 * S 2 2 - 6 * (A 2 1) * (A 3 1) * S 2 3
        - (A 3 1)^2 * S 1 1 - (A 3 1)^2 * S 3 3
        - 6 * (A 3 1) * (A 3 2) * S 1 2 - (A 3 2)^2 * S 2 2
        - (A 3 2)^2 * S 3 3
      + S 1 1 * S 1 2^2 + S 1 1 * S 1 3^2 + S 2 2 * S 1 2^2
        + S 2 2 * S 2 3^2 + S 3 3 * S 1 3^2 + S 3 3 * S 2 3^2
        + 6 * S 1 2 * S 1 3 * S 2 3 - S 1 1^2 * S 2 2 - S 1 1^2 * S 3 3
        - S 1 1 * S 2 2^2 - S 1 1 * S 3 3^2 - 2 * S 1 1 * S 2 3^2
        - S 2 2^2 * S 3 3 - S 2 2 * S 3 3^2 - 2 * S 2 2 * S 1 3^2
        - 2 * S 3 3 * S 1 2^2 := by
  have c11 : C 1 1 = 0 := by linarith [hC 1 1]
  have c22 : C 2 2 = 0 := by linarith [hC 2 2]
  have c33 : C 3 3 = 0 := by linarith [hC 3 3]
  have a11 : A 1 1 = 0 := by linarith [hA 1 1]
  have a22 : A 2 2 = 0 := by linarith [hA 2 2]
  have a33 : A 3 3 = 0 := by linarith [hA 3 3]
  simp only [skDiv, skConnG, skEin, skScalar, skRic, skCurv, sum4,
    mink4, singleZeroConn, Matrix.cons_val_zero, Matrix.cons_val_one,
    Matrix.cons_val_two, Matrix.cons_val_three,
    Matrix.head_cons, Matrix.tail_cons,
    hC 1 2, hC 1 3, hC 2 3, hA 1 2, hA 1 3, hA 2 3,
    hS 2 1, hS 3 1, hS 3 2,
    c11, c22, c33, a11, a22, a33,
    mul_zero, zero_mul, add_zero, zero_add, neg_zero, sub_zero, zero_sub,
    mul_one, one_mul, one_div, mul_neg, neg_mul, neg_neg]
  ring

-- ============================================================
-- §26.9 方向 (β)：∂̃ 的 Leibniz 修正与分量级修正 Bianchi
-- ============================================================
-- 真值路径第一环（sorry_closure_roadmap.md §3.6 方向 (β)）：
-- 守恒律的载体是含 ∂̃ 项的恒等式，其代数源头是 step 差分的
-- Leibniz 修正——数值实验（phase16b_discrete_bianchi.py）发现
-- 朴素分量式离散 Bianchi 残差 ~2–3×|∂̃Γ·Γ|，全部出自修正项
-- ∂̃A·∂̃B。本节形式化：∂̃ 定义 + Leibniz 修正恒等式 +
-- 协变差分的分量公式 + 分量级循环恒等式（修正结构显式保留）。

/-- 沿方向 step 的有限差分导数 ∂̃：场在递归系统上的逐点差分
    (∂̃_ρ T)(x) := T(stepD ρ x) − T(x)。
    物理含义：连续偏导数 ∂_ρ 的离散对应
    （格距归一 T(step ρ x)−T x = a·∂̃，a → 0 时收敛）。 -/
def stepDiff (F : FrameRecObj) (ρ : Fin 4)
    (A : F.X.T → ℝ) : F.X.T → ℝ :=
  fun x => A (F.stepD ρ x) - A x

/-- **离散 Leibniz 修正恒等式**：step 差分作用于乘积场时普通 Leibniz
    规则失效，修正项 ∂̃A·∂̃B 不可忽略：
    ∂̃_ρ(A·B) = ∂̃_ρA·B + A·∂̃_ρB + ∂̃_ρA·∂̃_ρB。
    物理含义：差分算子 ∂̃ = S_ρ − 1 满足 (S−1)(AB) = (S−1)A·B + A·(S−1)B
    + (S−1)A·(S−1)B——移位同态性在差分上的精确失效模式；
    O(a²) 格距下修正项为高阶小量（数值 |B|/|R| ∝ 1/n²），
    但恒等式本身逐点精确（纯移位代数，ring 闭合）。 -/
theorem stepDiff_mul (F : FrameRecObj) (ρ : Fin 4)
    (A B : F.X.T → ℝ) (x : F.X.T) :
    stepDiff F ρ (fun y => A y * B y) x
      = stepDiff F ρ A x * B x + A x * stepDiff F ρ B x
        + stepDiff F ρ A x * stepDiff F ρ B x := by
  simp only [stepDiff]
  ring

/-- 协变差分算子的分量公式：
    (D_ρ W)(x) = W(stepD ρ x) − W(x) + Σ_l Γ^r_{ρl}(x) W^l(x)
    ——移位差分 ∂̃_ρ W + 规范作用，连续 ∇_ρ W = ∂_ρ W + Γ_ρ W
    的离散对应（∂̃ 项与联络项同点取值）。 -/
lemma covDiffOp_apply (F : FrameRecObj) (Γf : GammaField F) (ρ : Fin 4)
    (W : VecField F) (x : F.X.T) (r : Fin 4) :
    (covDiffOp F Γf ρ) W x r
      = W (F.stepD ρ x) r - W x r
        + sum4 (fun l => Γf.γ x r ρ l * W x l) := by
  simp only [covDiffOp, LinearMap.add_apply, LinearMap.sub_apply,
    shiftOp_apply, gaugeOp_apply, Module.End.one_apply,
    ← sum4_eq_finset_sum, sum4, Pi.sub_apply, Pi.add_apply]
  ring

/-- **分量级离散第二 Bianchi 恒等式**（step 语义，修正结构显式保留）：
    对任意向量场 V 与任意点 x、指标 r，
      Σ_cyc(ρ,μ,ν) [ (D_ρ (F_{μν} V))(x) − (F_{μν} (D_ρ V))(x) ]^r = 0，
    其中 D_ρ = ∂̃_ρ + 规范作用（covDiffOp_apply），
    F_{μν} = [D_μ, D_ν]（curvature_op_apply 的分量展开含
    双移位修正、∂̃Γ·V 与 [Γ_μ,Γ_ν]·V 三项）。
    与 skeleton_second_bianchi（∂̃ ≡ 0 的骨架层）的关系：
    本定理是其含 ∂̃ 项的真值载体——修正项（双移位、∂̃Γ、
    Leibniz 修正）在恒等式内精确抵消，连续极限 a → 0 逐型消失。
    证明：算子 Jacobi 恒等式（discrete_second_bianchi_operator）
    经 LinearMap.ext 逐点实例化。 -/
theorem discrete_second_bianchi_components (F : FrameRecObj)
    (Γf : GammaField F) (ρ μ ν : Fin 4)
    (V : VecField F) (x : F.X.T) (r : Fin 4) :
    ((covDiffOp F Γf ρ) ((curvatureOp F Γf μ ν) V) x r
      - (curvatureOp F Γf μ ν) ((covDiffOp F Γf ρ) V) x r)
    + ((covDiffOp F Γf μ) ((curvatureOp F Γf ν ρ) V) x r
      - (curvatureOp F Γf ν ρ) ((covDiffOp F Γf μ) V) x r)
    + ((covDiffOp F Γf ν) ((curvatureOp F Γf ρ μ) V) x r
      - (curvatureOp F Γf ρ μ) ((covDiffOp F Γf ν) V) x r) = 0 := by
  -- h : ((A*B - B*A + ...) V) x r = (0 V) x r；
  -- 算子积 (f*g) V = f (g V)、减法/加法逐点应用与零映射逐点作用均为定义相等（rfl 族），
  -- 目标左端即 h 左端的定义展开，右端 (0 V) x r 与字面 0 亦定义相等。
  have h := congrFun (congrFun
    (LinearMap.ext_iff.1 (discrete_second_bianchi_operator F Γf ρ μ ν) V) x) r
  exact h

-- ============================================================
-- §26.10 方向 (β)-2：算子级 η-度规相容（Leibniz 修正版）
-- ============================================================
-- 数值基础（§26.7 注释，phase16b_metric_contraction.py Q1）：
-- 离散 Christoffel 公式使逐点相容残差 A_{ρμν} = ∂̃_ρ g_{μν}
-- − Γ^l_{ρμ}g_{lν} − Γ^l_{ρν}g_{μl} 精确为零——即联络 1-形式逐点
-- 取值于 𝔰𝔬(g)。本节点把这一逐点代数条件提升为**算子恒等式**：
-- 协变差分 D_ρ 对标量配对 ⟨V,W⟩ 的作用满足 Leibniz 修正律。
-- 修正项 ⟨∂̃V,∂̃W⟩ 是场层级朴素相容偏离的精确代数形态
-- （光滑场上 O(a²)，与 |B|/|R| ∝ 1/n² 的数值观测同阶）——
-- 这是把分量级 Bianchi 缩并成修正散度恒等式所需的结构件。

/-- η-配对：两向量场按 Minkowski 度规逐点缩并的标量场
    ⟨V, W⟩_η(x) := Σ_{r,s} η_{rs} V^r(x) W^s(x)。 -/
def etaPair (F : FrameRecObj) (V W : VecField F) : F.X.T → ℝ :=
  fun x => sum4 (fun r => sum4 (fun s => mink4 r s * (V x r * W x s)))

/-- **算子级 η-度规相容（Leibniz 修正版）**：
    联络逐点取值于 𝔰𝔬(η)（相容假设 hη，即 SkeletonMetricCompat 的
    Minkowski 逐点形态——离散 Christoffel 场满足之，见
    discrete_christoffel_metric_compatible）时，任意向量场 V W 满足
      ∂̃_ρ⟨V, W⟩_η = ⟨D_ρ V, W⟩_η + ⟨V, D_ρ W⟩_η + ⟨∂̃_ρ V, ∂̃_ρ W⟩_η，
    其中 D_ρ = covDiffOp（移位差分 + 规范作用），∂̃_ρ 为纯移位差分。
    物理含义：连续恒等式 ∂_ρ⟨V,W⟩ = ⟨∇V,W⟩ + ⟨V,∇W⟩ 的离散精确形态
    ——离散 Leibniz 修正（stepDiff_mul）贡献第三项 ⟨∂̃V,∂̃W⟩，
    光滑场上为 O(a²) 高阶小量，故朴素相容在差分代数中逐点精确到
    修正项为止；联络项的消去即 hη（𝔰𝔬(η) 条件）。
    证明：配对展开 + 逐分量 Leibniz + Γ 双和经 hη 归零
    （Finset sum_add_distrib/mul_sum/sum_mul 分配 + sum_comm 重排）。 -/
theorem covDiffOp_metric_compatible (F : FrameRecObj) (Γf : GammaField F)
    (hη : ∀ x ρ μ ν, sum4 (fun a => mink4 μ a * Γf.γ x a ρ ν)
        + sum4 (fun a => mink4 ν a * Γf.γ x a ρ μ) = 0)
    (ρ : Fin 4) (V W : VecField F) (x : F.X.T) :
    stepDiff F ρ (etaPair F V W) x
      = sum4 (fun r => sum4 (fun s => mink4 r s *
          ((covDiffOp F Γf ρ) V x r * W x s
            + V x r * ((covDiffOp F Γf ρ) W x s)
            + (V (F.stepD ρ x) r - V x r) * (W (F.stepD ρ x) s - W x s)))) := by
  -- η 对称性（字面矩阵，对角/非对角逐项 rfl）
  have hsym : ∀ i j : Fin 4, mink4 i j = mink4 j i := by
    intro i j; fin_cases i <;> fin_cases j <;> rfl
  -- 逐点 𝔰𝔬(η) 条件的 Finset 形态（bridge sum4）
  have hcomp : ∀ μ ν : Fin 4,
      (∑ a : Fin 4, mink4 μ a * Γf.γ x a ρ ν)
        + (∑ a : Fin 4, mink4 ν a * Γf.γ x a ρ μ) = 0 := by
    intro μ ν
    have h := hη x ρ μ ν
    rwa [sum4_eq_finset_sum, sum4_eq_finset_sum] at h
  -- Γ 双和归零：Σ_r Σ_s η_{rs}((ΓV)^r W^s + V^r (ΓW)^s) = 0
  have hgamma : (∑ r : Fin 4, ∑ s : Fin 4, mink4 r s *
        ((∑ a : Fin 4, Γf.γ x r ρ a * V x a) * W x s
          + V x r * (∑ a : Fin 4, Γf.γ x s ρ a * W x a))) = 0 := by
    -- ① 内层乘积展开为三重和（simp 分配引理归约到同一正规形）
    have key : (∑ r : Fin 4, ∑ s : Fin 4, mink4 r s *
          ((∑ a : Fin 4, Γf.γ x r ρ a * V x a) * W x s
            + V x r * (∑ a : Fin 4, Γf.γ x s ρ a * W x a)))
        = (∑ r : Fin 4, ∑ s : Fin 4, ∑ a : Fin 4,
            mink4 r s * (Γf.γ x r ρ a * V x a * W x s))
          + (∑ r : Fin 4, ∑ s : Fin 4, ∑ a : Fin 4,
            mink4 r s * (V x r * (Γf.γ x s ρ a * W x a))) := by
      simp only [Finset.sum_add_distrib, Finset.mul_sum, Finset.sum_mul, mul_add]
    -- ② 两个三重和分别重排为 (V,W)-系数形态
    have reg1 : (∑ r : Fin 4, ∑ s : Fin 4, ∑ a : Fin 4,
          mink4 r s * (Γf.γ x r ρ a * V x a * W x s))
        = ∑ a : Fin 4, ∑ s : Fin 4,
          (V x a * W x s) * (∑ r : Fin 4, mink4 r s * Γf.γ x r ρ a) := by
      -- ∑ r ∑ s ∑ a → ∑ r ∑ a ∑ s（内层交换）→ ∑ a ∑ r ∑ s（外层交换）→ ∑ a ∑ s ∑ r
      rw [Finset.sum_congr rfl (fun r _ => Finset.sum_comm
        (f := fun s a => mink4 r s * (Γf.γ x r ρ a * V x a * W x s)))]
      rw [Finset.sum_comm (f := fun r a => ∑ s : Fin 4,
          mink4 r s * (Γf.γ x r ρ a * V x a * W x s))]
      apply Finset.sum_congr rfl; intro a _
      rw [Finset.sum_comm (f := fun r s => mink4 r s * (Γf.γ x r ρ a * V x a * W x s))]
      apply Finset.sum_congr rfl; intro s _
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl; intro r _
      ring
    have reg2 : (∑ r : Fin 4, ∑ s : Fin 4, ∑ a : Fin 4,
          mink4 r s * (V x r * (Γf.γ x s ρ a * W x a)))
        = ∑ r : Fin 4, ∑ a : Fin 4,
          (V x r * W x a) * (∑ s : Fin 4, mink4 r s * Γf.γ x s ρ a) := by
      apply Finset.sum_congr rfl; intro r _
      rw [Finset.sum_comm (f := fun s a => mink4 r s * (V x r * (Γf.γ x s ρ a * W x a)))]
      apply Finset.sum_congr rfl; intro a _
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl; intro s _
      ring
    -- ③ 哑元 α-改名使两项同形（defeq）
    have hB : (∑ r : Fin 4, ∑ a : Fin 4, (V x r * W x a) *
          (∑ s : Fin 4, mink4 r s * Γf.γ x s ρ a))
        = ∑ a : Fin 4, ∑ s : Fin 4, (V x a * W x s) *
          (∑ r : Fin 4, mink4 a r * Γf.γ x r ρ s) := rfl
    -- ④ η 对称进入系数括号，逐点归零（hcomp）
    have h1 : ∀ a s : Fin 4, (∑ r : Fin 4, mink4 r s * Γf.γ x r ρ a)
        = ∑ r : Fin 4, mink4 s r * Γf.γ x r ρ a :=
      fun a s => Finset.sum_congr rfl (fun r _ => by rw [hsym r s])
    have hzero : ∀ a s : Fin 4, (V x a * W x s) * (∑ r : Fin 4, mink4 r s * Γf.γ x r ρ a)
          + (V x a * W x s) * (∑ r : Fin 4, mink4 a r * Γf.γ x r ρ s) = 0 := by
      intro a s
      rw [h1 a s, show (V x a * W x s) * (∑ r : Fin 4, mink4 s r * Γf.γ x r ρ a)
            + (V x a * W x s) * (∑ r : Fin 4, mink4 a r * Γf.γ x r ρ s)
          = (V x a * W x s) * ((∑ r : Fin 4, mink4 a r * Γf.γ x r ρ s)
            + (∑ r : Fin 4, mink4 s r * Γf.γ x r ρ a)) from by ring,
        hcomp a s, mul_zero]
    have hzero' : ∀ a : Fin 4,
        (∑ s : Fin 4, (V x a * W x s) * (∑ r : Fin 4, mink4 r s * Γf.γ x r ρ a))
          + (∑ s : Fin 4, (V x a * W x s) * (∑ r : Fin 4, mink4 a r * Γf.γ x r ρ s)) = 0 := by
      intro a
      rw [Finset.sum_add_distrib.symm]
      exact Finset.sum_eq_zero (fun s _ => hzero a s)
    rw [key, reg1, reg2, hB, ← Finset.sum_add_distrib]
    exact Finset.sum_eq_zero (fun a _ => hzero' a)
  -- 主恒等式：D 展开后 Γ 部分恰为 hgamma
  have hmain : (∑ r : Fin 4, ∑ s : Fin 4, mink4 r s *
        (V (F.stepD ρ x) r * W (F.stepD ρ x) s - V x r * W x s))
      = ∑ r : Fin 4, ∑ s : Fin 4, mink4 r s *
          ((covDiffOp F Γf ρ) V x r * W x s
            + V x r * ((covDiffOp F Γf ρ) W x s)
            + (V (F.stepD ρ x) r - V x r) * (W (F.stepD ρ x) s - W x s)) := by
    have hexp : (∑ r : Fin 4, ∑ s : Fin 4, mink4 r s *
          ((covDiffOp F Γf ρ) V x r * W x s
            + V x r * ((covDiffOp F Γf ρ) W x s)
            + (V (F.stepD ρ x) r - V x r) * (W (F.stepD ρ x) s - W x s)))
        = (∑ r : Fin 4, ∑ s : Fin 4, mink4 r s *
            (V (F.stepD ρ x) r * W (F.stepD ρ x) s - V x r * W x s))
          + (∑ r : Fin 4, ∑ s : Fin 4, mink4 r s *
            ((∑ a : Fin 4, Γf.γ x r ρ a * V x a) * W x s
              + V x r * (∑ a : Fin 4, Γf.γ x s ρ a * W x a))) := by
      rw [← Finset.sum_add_distrib]
      apply Finset.sum_congr rfl; intro r _
      rw [← Finset.sum_add_distrib]
      apply Finset.sum_congr rfl; intro s _
      rw [covDiffOp_apply, covDiffOp_apply, sum4_eq_finset_sum, sum4_eq_finset_sum]
      ring
    rw [hexp, hgamma, add_zero]
  -- 组装：LHS 为配对差分，RHS 经 sum4→Finset 桥接
  have hL : stepDiff F ρ (etaPair F V W) x
      = ∑ r : Fin 4, ∑ s : Fin 4, mink4 r s *
        (V (F.stepD ρ x) r * W (F.stepD ρ x) s - V x r * W x s) := by
    rw [show stepDiff F ρ (etaPair F V W) x
        = (∑ r : Fin 4, ∑ s : Fin 4,
            mink4 r s * (V (F.stepD ρ x) r * W (F.stepD ρ x) s))
          - (∑ r : Fin 4, ∑ s : Fin 4, mink4 r s * (V x r * W x s)) from by
      simp only [stepDiff, etaPair, sum4_eq_finset_sum]]
    rw [← Finset.sum_sub_distrib]
    apply Finset.sum_congr rfl; intro r _
    rw [← Finset.sum_sub_distrib]
    apply Finset.sum_congr rfl; intro s _
    ring
  rw [hL, show sum4 (fun r => sum4 (fun s => mink4 r s *
        ((covDiffOp F Γf ρ) V x r * W x s
          + V x r * ((covDiffOp F Γf ρ) W x s)
          + (V (F.stepD ρ x) r - V x r) * (W (F.stepD ρ x) s - W x s))))
      = ∑ r : Fin 4, ∑ s : Fin 4, mink4 r s *
        ((covDiffOp F Γf ρ) V x r * W x s
          + V x r * ((covDiffOp F Γf ρ) W x s)
          + (V (F.stepD ρ x) r - V x r) * (W (F.stepD ρ x) s - W x s))
      from by simp only [sum4_eq_finset_sum], hmain]

-- ============================================================
-- §26.11 方向 (β)-3：修正张量 Bianchi 恒等式（常值试验场限制）
-- ============================================================
-- (β)-1 的算子 Jacobi 恒等式作用于**常值试验场** v̂ = fun _ => v 时，
-- 曲率算子退化为朴素曲率 R̂（含 ∂̃Γ 项，双移位项 v−v 逐点抵消），
-- 按 v 线性提取系数给出 (1,1)-张量形态的**精确**第二 Bianchi：
--   Σ_cyc(λ,μ,ν) (∇̃_lam R̂_{μν} − C_{λμν}) = 0，
-- 其中 ∇̃_lam R̂_{μν} = ∂̃_lam R̂_{μν} + [Γ_λ, R̂_{μν}]（(1,1)-联络项），
-- C_{λμν} = F_{μν} 作用于非常值场 Γ_λ·v 相对逐点矩阵作用的偏差：
--   双移位 Γ_lam 差 + 移位点 ∂̃Γ·Γ_λ。
-- 恒等式分解：D_lam(F_μν v̂) = (∂̃R̂)v + Γ_lam R̂ v（朴素展开），
-- F_μν(D_lam v̂) = R̂_{μν}(Γ_lam v) + C·v，相减后 R̂Γ_λv 项精确抵消。
-- 修正项全部携带 ∂̃Γ 或双移位因子——朴素张量 Bianchi（C ≡ 0 形态）
-- 不精确成立，其残差的代数结构即 C。
-- 数值对应：phase16b_discrete_bianchi.py 算子-分量差 ~2–3×|∂̃Γ·Γ|。

/-- 朴素曲率（数值 riemann_full 的逐点形态）：
    R̂^r_{sμν}(x) = ∂̃_μ Γ^r_{νs}(x) − ∂̃_ν Γ^r_{μs}(x)
      + Σ_l (Γ^r_{μl} Γ^l_{νs} − Γ^r_{νl} Γ^l_{μs})(x)。
    常值试验场上曲率算子的逐点矩阵（curvature_op_const_apply）。 -/
def naiveCurv (F : FrameRecObj) (Γf : GammaField F) (x : F.X.T)
    (r s μ ν : Fin 4) : ℝ :=
  (Γf.γ (F.stepD μ x) r ν s - Γf.γ x r ν s)
    - (Γf.γ (F.stepD ν x) r μ s - Γf.γ x r μ s)
    + sum4 (fun l => Γf.γ x r μ l * Γf.γ x l ν s - Γf.γ x r ν l * Γf.γ x l μ s)

/-- 朴素曲率的协变导数（(1,1)-型联络项）：
    (∇̃_lam R̂_{μν})^r_s = ∂̃_lam R̂^r_{sμν} + Σ_a Γ^r_{λa} R̂^a_{sμν}
      − Σ_a R̂^r_{aμν} Γ^a_{λs}。 -/
def naiveNablaCurv (F : FrameRecObj) (Γf : GammaField F) (lam μ ν : Fin 4)
    (x : F.X.T) (r s : Fin 4) : ℝ :=
  (naiveCurv F Γf (F.stepD lam x) r s μ ν - naiveCurv F Γf x r s μ ν)
    + sum4 (fun a => Γf.γ x r lam a * naiveCurv F Γf x a s μ ν)
    - sum4 (fun a => naiveCurv F Γf x r a μ ν * Γf.γ x a lam s)

/-- 修正项：F_{μν} 作用于非常值场 U = Γ_λ·v 相对逐点矩阵作用 R̂_μν·U 的
    偏差（curvature_op_apply 前三项，U 的 v-系数），经 R̂Γ_λv 项精确抵消后
    化简为纯二阶差分结构：
    C_{λμν}^r_s = [Γ_lam(step_ν step_μ x) − Γ_lam(step_μ step_ν x)]^r_s   （双移位差）
      + Σ_l ∂̃_μ Γ^r_{νl}(x) · ∂̃_μ Γ^l_{λs}(x)
      − Σ_l ∂̃_ν Γ^r_{μl}(x) · ∂̃_ν Γ^l_{λs}(x)，
    其中 ∂̃_μ Γ^r_{νl}(x) = Γ^r_{νl}(step_μ x) − Γ^r_{νl}(x)。
    三项均为二阶差分结构（光滑场上 O(a²)）；step 对易假设下双移位差消失、
    Γ 常值（GammaConstant）下 ∂̃Γ 项消失。 -/
def bianchiCorr (F : FrameRecObj) (Γf : GammaField F) (lam μ ν : Fin 4)
    (x : F.X.T) (r s : Fin 4) : ℝ :=
  (Γf.γ (F.stepD ν (F.stepD μ x)) r lam s - Γf.γ (F.stepD μ (F.stepD ν x)) r lam s)
    + sum4 (fun l =>
        (Γf.γ (F.stepD μ x) r ν l - Γf.γ x r ν l) * (Γf.γ (F.stepD μ x) l lam s - Γf.γ x l lam s))
    - sum4 (fun l =>
        (Γf.γ (F.stepD ν x) r μ l - Γf.γ x r μ l) * (Γf.γ (F.stepD ν x) l lam s - Γf.γ x l lam s))

/-- 常值试验场上的曲率算子 = 朴素曲率的逐点矩阵作用：
    (F_{μν} v̂)(x) = Σ_s R̂^r_{sμν}(x) v^s（v̂ ≡ v 常值）。
    证明：curvature_op_apply 代入常值场——双移位项 v−v 逐点抵消，
    移位点取值 v̂(step) = v，余下恰为 R̂ 的三项（ring 配对）。 -/
lemma curvature_op_const_apply (F : FrameRecObj) (Γf : GammaField F)
    (μ ν : Fin 4) (v : Fin 4 → ℝ) (x : F.X.T) (r : Fin 4) :
    (curvatureOp F Γf μ ν) (fun _ => v) x r
      = sum4 (fun s => naiveCurv F Γf x r s μ ν * v s) := by
  rw [curvature_op_apply]
  simp only [naiveCurv, sum4]
  ring

/-- 线性提取：∀ v, Σ_s B s * v s = 0 ⟹ B s₀ = 0
    （取 v 为 s₀ 处 1 的指示函数，mul_ite 归约 + sum_ite_eq' 求值）。 -/
lemma sum4_coeff_zero {B : Fin 4 → ℝ} (h : ∀ v : Fin 4 → ℝ, sum4 (fun s => B s * v s) = 0)
    (s₀ : Fin 4) : B s₀ = 0 := by
  have h' := h (fun i => if i = s₀ then (1:ℝ) else 0)
  have e : sum4 (fun s => B s * (if s = s₀ then (1:ℝ) else 0)) = B s₀ := by
    rw [sum4_eq_finset_sum]
    have step : (∑ s : Fin 4, B s * (if s = s₀ then (1:ℝ) else 0))
        = ∑ s : Fin 4, (if s = s₀ then B s else 0) :=
      Finset.sum_congr rfl (fun s _ => by simp only [mul_ite, mul_one, mul_zero])
    rw [step, Finset.sum_ite_eq', if_pos (Finset.mem_univ s₀)]
  rw [e] at h'
  exact h'

set_option maxHeartbeats 1000000 in
set_option maxRecDepth 32768 in
/-- **修正张量第二 Bianchi 恒等式**（常值试验场限制的系数形态）：
    算子 Jacobi 恒等式（discrete_second_bianchi_components）作用于常值场
    v̂ = fun _ => v 给出 v-线性恒等式 Σ_s [Σ_cyc(∇̃R̂ − C)]^r_s v^s = 0；
    按系数提取（sum4_coeff_zero）得 (1,1)-张量恒等式
      Σ_cyc(λ,μ,ν) (∇̃_lam R̂_{μν} − C_{λμν})^r_s = 0（精确，无任何假设）。
    物理含义：朴素张量 Bianchi（∇̃_lam R̂ 循环和 ≡ 0）在差分代数中不精确
    成立——修正项 C（双移位 Γ_lam 差 + 移位点 ∂̃Γ·Γ_λ）是其残差的精确
    代数结构；C 的各项携带 ∂̃Γ 或双移位因子，step 对易假设
    （StepsCommute）下双移位项消失、Γ 常值（GammaConstant）下 ∂̃Γ 项
    消失，此时恒等式退化为骨架层 skeleton_second_bianchi
    （与 §26.6 的退化链一致）。
    证明：两侧经 covDiffOp_apply / curvature_op_apply /
    curvature_op_const_apply / hU（常值场的 D_lam v̂ = Γ_λ·v）展开为
    v-多项式，ring 验证恒等（R̂Γ_λv 项在两侧精确抵消）。 -/
theorem discrete_second_bianchi_tensor (F : FrameRecObj) (Γf : GammaField F)
    (lam μ ν : Fin 4) (x : F.X.T) (r s₀ : Fin 4) :
    ((naiveNablaCurv F Γf lam μ ν x r s₀ - bianchiCorr F Γf lam μ ν x r s₀)
      + (naiveNablaCurv F Γf μ ν lam x r s₀ - bianchiCorr F Γf μ ν lam x r s₀)
      + (naiveNablaCurv F Γf ν lam μ x r s₀ - bianchiCorr F Γf ν lam μ x r s₀)) = 0 := by
  apply sum4_coeff_zero _ s₀
  intro v
  have hcomp := discrete_second_bianchi_components F Γf lam μ ν (fun _ => v) x r
  -- 常值场上的协变差分：D_lam v̂ = Γ_λ·v（逐点）
  have hU : ∀ (y : F.X.T) (rr : Fin 4),
      (covDiffOp F Γf lam) (fun _ => v) y rr
        = sum4 (fun l => Γf.γ y rr lam l * v l) := by
    intro y rr
    rw [covDiffOp_apply]
    simp only [sum4]
    ring
  -- v-线性归约：两侧展开为同一 v-多项式
  have e : sum4 (fun s =>
        ((naiveNablaCurv F Γf lam μ ν x r s - bianchiCorr F Γf lam μ ν x r s)
          + (naiveNablaCurv F Γf μ ν lam x r s - bianchiCorr F Γf μ ν lam x r s)
          + (naiveNablaCurv F Γf ν lam μ x r s - bianchiCorr F Γf ν lam μ x r s)) * v s)
      = ((covDiffOp F Γf lam) ((curvatureOp F Γf μ ν) (fun _ => v)) x r
        - (curvatureOp F Γf μ ν) ((covDiffOp F Γf lam) (fun _ => v)) x r)
        + ((covDiffOp F Γf μ) ((curvatureOp F Γf ν lam) (fun _ => v)) x r
          - (curvatureOp F Γf ν lam) ((covDiffOp F Γf μ) (fun _ => v)) x r)
        + ((covDiffOp F Γf ν) ((curvatureOp F Γf lam μ) (fun _ => v)) x r
          - (curvatureOp F Γf lam μ) ((covDiffOp F Γf ν) (fun _ => v)) x r) := by
    simp only [naiveNablaCurv, bianchiCorr, naiveCurv, sum4,
      covDiffOp_apply, curvature_op_apply, curvature_op_const_apply, hU]
    ring
  rw [e, hcomp]

/-- Ricci 张量（裸迹，无度量）：
    Riĉ_{sν}(x) = Σ_r R̂^r{}_{s r ν}(x)。连续极限退化为 Ricci 张量。 -/
def ricciTensor (F : FrameRecObj) (Γf : GammaField F)
    (s ν : Fin 4) (x : F.X.T) : ℝ :=
  sum4 (fun r => naiveCurv F Γf x r s r ν)

/-- 缩并修正项（联络部分之一，来自 ∇̃ 与裸迹的不交换性）：
    K2_{μνs} = Σ_{r,a} Γ^r_{μa} R̂^a{}_{sνr} + Σ_a Riĉ_{aν} Γ^a_{μs}。 -/
def contractConn2 (F : FrameRecObj) (Γf : GammaField F)
    (μ ν : Fin 4) (x : F.X.T) (s : Fin 4) : ℝ :=
  sum4 (fun r => sum4 (fun a => Γf.γ x r μ a * naiveCurv F Γf x a s ν r))
    + sum4 (fun a => ricciTensor F Γf a ν x * Γf.γ x a μ s)

/-- 缩并修正项（联络部分之二）：
    K3_{μνs} = Σ_{r,a} Γ^r_{νa} R̂^a{}_{srμ} − Σ_a Riĉ_{aμ} Γ^a_{νs}。 -/
def contractConn3 (F : FrameRecObj) (Γf : GammaField F)
    (μ ν : Fin 4) (x : F.X.T) (s : Fin 4) : ℝ :=
  sum4 (fun r => sum4 (fun a => Γf.γ x r ν a * naiveCurv F Γf x a s r μ))
    - sum4 (fun a => ricciTensor F Γf a μ x * Γf.γ x a ν s)

/-- 修正项缩并：C 在缩并恒等式三个循环位置上的裸迹之和。 -/
def contractCorr (F : FrameRecObj) (Γf : GammaField F)
    (μ ν : Fin 4) (x : F.X.T) (s : Fin 4) : ℝ :=
  sum4 (fun r => bianchiCorr F Γf r μ ν x r s
    + bianchiCorr F Γf μ ν r x r s
    + bianchiCorr F Γf ν r μ x r s)

set_option maxHeartbeats 1000000 in
set_option maxRecDepth 32768 in
/-- 循环位置二求和引理：Σ_r ∇̃_μ R̂_{νr}(x)^r_s = −∂̃_μ Riĉ_{sν} + K2。
    证明结构：∂̃ 部分经逐点反对称 naiveCurv(x,r,s,ν,r) = −naiveCurv(x,r,s,r,ν)
    归约为 ricciTensor 差；联络第二部分经 Finset.sum_comm 交换求和顺序、
    Finset.sum_mul 因子化后由同一反对称恒等式归约（ring 不自动交换
    求和指标、也不自动提出 (∑)·c 因子——故逐步手工归约）。 -/
lemma sum_nabla_right2 (F : FrameRecObj) (Γf : GammaField F)
    (μ ν : Fin 4) (x : F.X.T) (s : Fin 4) :
    sum4 (fun r => naiveNablaCurv F Γf μ ν r x r s)
    = (-(ricciTensor F Γf s ν (F.stepD μ x) - ricciTensor F Γf s ν x)
        + contractConn2 F Γf μ ν x s) := by
  have h1 : ∀ (r s' : Fin 4), naiveCurv F Γf (F.stepD μ x) r s' ν r
      = - naiveCurv F Γf (F.stepD μ x) r s' r ν := by
    intro r s'; simp only [naiveCurv, sum4]; ring
  have h2 : ∀ (r s' : Fin 4), naiveCurv F Γf x r s' ν r
      = - naiveCurv F Γf x r s' r ν := by
    intro r s'; simp only [naiveCurv, sum4]; ring
  have eA : (∑ r, naiveCurv F Γf (F.stepD μ x) r s ν r) = - ricciTensor F Γf s ν (F.stepD μ x) := by
    simp only [ricciTensor, sum4_eq_finset_sum]
    rw [← Finset.sum_neg_distrib]
    apply Finset.sum_congr rfl
    intro r _
    exact h1 r s
  have eB : (∑ r, naiveCurv F Γf x r s ν r) = - ricciTensor F Γf s ν x := by
    simp only [ricciTensor, sum4_eq_finset_sum]
    rw [← Finset.sum_neg_distrib]
    apply Finset.sum_congr rfl
    intro r _
    exact h2 r s
  have eD : (∑ r, ∑ a, naiveCurv F Γf x r a ν r * Γf.γ x a μ s)
      = - ∑ a, ricciTensor F Γf a ν x * Γf.γ x a μ s := by
    rw [Finset.sum_comm (f := fun r a => naiveCurv F Γf x r a ν r * Γf.γ x a μ s)]
    rw [← Finset.sum_neg_distrib]
    apply Finset.sum_congr rfl
    intro a _
    have hric : (∑ r, naiveCurv F Γf x r a ν r) = - ricciTensor F Γf a ν x := by
      simp only [ricciTensor, sum4_eq_finset_sum]
      rw [← Finset.sum_neg_distrib]
      apply Finset.sum_congr rfl
      intro r _
      exact h2 r a
    have key : (∑ r, naiveCurv F Γf x r a ν r * Γf.γ x a μ s)
        = (∑ r, naiveCurv F Γf x r a ν r) * Γf.γ x a μ s :=
      (Finset.sum_mul _ _ _).symm
    rw [key, hric]
    ring
  have unfold : sum4 (fun r => naiveNablaCurv F Γf μ ν r x r s)
      = (∑ r, (naiveCurv F Γf (F.stepD μ x) r s ν r - naiveCurv F Γf x r s ν r
          + ∑ a, Γf.γ x r μ a * naiveCurv F Γf x a s ν r
          - ∑ a, naiveCurv F Γf x r a ν r * Γf.γ x a μ s)) := by
    simp only [sum4_eq_finset_sum, naiveNablaCurv]
  rw [unfold]
  have split : (∑ r, (naiveCurv F Γf (F.stepD μ x) r s ν r - naiveCurv F Γf x r s ν r
        + ∑ a, Γf.γ x r μ a * naiveCurv F Γf x a s ν r
        - ∑ a, naiveCurv F Γf x r a ν r * Γf.γ x a μ s))
      = (∑ r, naiveCurv F Γf (F.stepD μ x) r s ν r) - (∑ r, naiveCurv F Γf x r s ν r)
        + (∑ r, ∑ a, Γf.γ x r μ a * naiveCurv F Γf x a s ν r)
        - (∑ r, ∑ a, naiveCurv F Γf x r a ν r * Γf.γ x a μ s) := by
    simp only [sub_eq_add_neg, Finset.sum_neg_distrib, Finset.sum_add_distrib]
  rw [split, eA, eB, eD]
  simp only [contractConn2, sum4_eq_finset_sum]
  ring

set_option maxHeartbeats 1000000 in
set_option maxRecDepth 32768 in
/-- 循环位置三求和引理：Σ_r ∇̃_ν R̂_{rμ}(x)^r_s = ∂̃_ν Riĉ_{sμ} + K3。
    比 sum_nabla_right2 简单：此处裸迹与 ricciTensor 定义同向
    （Σ_r naiveCurv(x,r,a,r,μ) = Riĉ_{aμ}），无需反对称归约。 -/
lemma sum_nabla_right3 (F : FrameRecObj) (Γf : GammaField F)
    (μ ν : Fin 4) (x : F.X.T) (s : Fin 4) :
    sum4 (fun r => naiveNablaCurv F Γf ν r μ x r s)
    = ((ricciTensor F Γf s μ (F.stepD ν x) - ricciTensor F Γf s μ x)
        + contractConn3 F Γf μ ν x s) := by
  have hric : ∀ (a : Fin 4), (∑ r, naiveCurv F Γf x r a r μ) = ricciTensor F Γf a μ x := by
    intro a
    simp only [ricciTensor, sum4_eq_finset_sum]
  -- 联络第二部分：交换求和 + 因子化 + 裸迹 = ricci（无需反对称）
  have eD : (∑ r, ∑ a, naiveCurv F Γf x r a r μ * Γf.γ x a ν s)
      = ∑ a, ricciTensor F Γf a μ x * Γf.γ x a ν s := by
    rw [Finset.sum_comm (f := fun r a => naiveCurv F Γf x r a r μ * Γf.γ x a ν s)]
    apply Finset.sum_congr rfl
    intro a _
    have key : (∑ r, naiveCurv F Γf x r a r μ * Γf.γ x a ν s)
        = (∑ r, naiveCurv F Γf x r a r μ) * Γf.γ x a ν s :=
      (Finset.sum_mul _ _ _).symm
    rw [key, hric a]
  have unfold : sum4 (fun r => naiveNablaCurv F Γf ν r μ x r s)
      = (∑ r, (naiveCurv F Γf (F.stepD ν x) r s r μ - naiveCurv F Γf x r s r μ
          + ∑ a, Γf.γ x r ν a * naiveCurv F Γf x a s r μ
          - ∑ a, naiveCurv F Γf x r a r μ * Γf.γ x a ν s)) := by
    simp only [sum4_eq_finset_sum, naiveNablaCurv]
  rw [unfold]
  have split : (∑ r, (naiveCurv F Γf (F.stepD ν x) r s r μ - naiveCurv F Γf x r s r μ
        + ∑ a, Γf.γ x r ν a * naiveCurv F Γf x a s r μ
        - ∑ a, naiveCurv F Γf x r a r μ * Γf.γ x a ν s))
      = (∑ r, naiveCurv F Γf (F.stepD ν x) r s r μ) - (∑ r, naiveCurv F Γf x r s r μ)
        + (∑ r, ∑ a, Γf.γ x r ν a * naiveCurv F Γf x a s r μ)
        - (∑ r, ∑ a, naiveCurv F Γf x r a r μ * Γf.γ x a ν s) := by
    simp only [sub_eq_add_neg, Finset.sum_neg_distrib, Finset.sum_add_distrib]
  rw [split]
  have eA : (∑ r, naiveCurv F Γf (F.stepD ν x) r s r μ) = ricciTensor F Γf s μ (F.stepD ν x) := by
    simp only [ricciTensor, sum4_eq_finset_sum]
  have eB : (∑ r, naiveCurv F Γf x r s r μ) = ricciTensor F Γf s μ x := by
    simp only [ricciTensor, sum4_eq_finset_sum]
  rw [eA, eB, eD]
  simp only [contractConn3, sum4_eq_finset_sum]
  ring

/-- **离散 Riemann 散度恒等式**（裸迹缩并 (β)-3 的第一阶段）：
    Σ_r naiveNablaCurv(r,μ,ν,x,r,s)
      − ∂̃_μ Riĉ_{sν} + ∂̃_ν Riĉ_{sμ}
    = (C 的三位置缩并) − K2 − K3（逐点精确，无任何假设）。
    连续对应：∇^ρ R_{ρsμν} = ∇_μ Ric_{sν} − ∇_ν Ric_{sμ} 的离散修正形态
    ——左侧为 Riemann 张量对 (ρ, s) 的散度，右侧为 Ricci 张量的协变差分
    差；修正项 K2/K3 为联络一阶项（Γ·R̂ 与 Ric·Γ），修正项缩并为
    C 的裸迹（O(a²) 结构）。骨架层（Γ 常值 + step 对易）下 K2/K3 退化为
    骨架恒等式、C 缩并消失，与 §26.6/§26.7 退化链一致。
    证明：对 (β)-3 张量恒等式取 λ = r 并对 r 求和（Finset.sum_eq_zero），
    得 Σ_r Σ_cyc(∇̃R̂ − C) = 0；三个循环位置的和分别用
    sum_nabla_right2 / sum_nabla_right3 归约为 ∂̃Ric ± 修正
    （∂̃ 与求和交换无修正，修正全部来自联络项的指标耦合），
    linarith 组装（ring 不能一次归约：它不交换求和指标顺序、
    也不提出 (∑)·c 因子）。数值验证 numerical/phase16b_beta4_explore.py
    （worst |LHS−RHS| = 2.1e-14）。 -/
theorem discrete_riemann_divergence (F : FrameRecObj) (Γf : GammaField F)
    (μ ν : Fin 4) (x : F.X.T) (s : Fin 4) :
    (sum4 (fun r => naiveNablaCurv F Γf r μ ν x r s)
      - (ricciTensor F Γf s ν (F.stepD μ x) - ricciTensor F Γf s ν x)
      + (ricciTensor F Γf s μ (F.stepD ν x) - ricciTensor F Γf s μ x))
    = contractCorr F Γf μ ν x s
      - contractConn2 F Γf μ ν x s
      - contractConn3 F Γf μ ν x s := by
  have h0 : ∑ r : Fin 4,
      ((naiveNablaCurv F Γf r μ ν x r s - bianchiCorr F Γf r μ ν x r s)
        + (naiveNablaCurv F Γf μ ν r x r s - bianchiCorr F Γf μ ν r x r s)
        + (naiveNablaCurv F Γf ν r μ x r s - bianchiCorr F Γf ν r μ x r s)) = 0 := by
    rw [Finset.sum_eq_zero]
    intro r _
    exact discrete_second_bianchi_tensor F Γf r μ ν x r s
  simp only [Finset.sum_add_distrib, Finset.sum_sub_distrib] at h0
  have eP2 : (∑ r, naiveNablaCurv F Γf μ ν r x r s)
      = (-(ricciTensor F Γf s ν (F.stepD μ x) - ricciTensor F Γf s ν x)
          + contractConn2 F Γf μ ν x s) := by
    rw [← sum4_eq_finset_sum]
    exact sum_nabla_right2 F Γf μ ν x s
  have eP3 : (∑ r, naiveNablaCurv F Γf ν r μ x r s)
      = ((ricciTensor F Γf s μ (F.stepD ν x) - ricciTensor F Γf s μ x)
          + contractConn3 F Γf μ ν x s) := by
    rw [← sum4_eq_finset_sum]
    exact sum_nabla_right3 F Γf μ ν x s
  have ecc : contractCorr F Γf μ ν x s
      = (∑ r, bianchiCorr F Γf r μ ν x r s)
        + ((∑ r, bianchiCorr F Γf μ ν r x r s)
          + (∑ r, bianchiCorr F Γf ν r μ x r s)) := by
    simp only [contractCorr, sum4_eq_finset_sum, Finset.sum_add_distrib, add_assoc]
  rw [sum4_eq_finset_sum]
  linarith [h0, eP2, eP3, ecc]

/-- 度量降指标 (0,4) 曲率：R4_{abcd}(p) = Σ_r g_{ar}(p) R̂^r{}_{bcd}(p)。
    连续对应 g_{rr'} R̂^{r'}{}_{bcd}（Riemann (0,4) 张量）。 -/
def lower4 (F : FrameRecObj) (Γf : GammaField F)
    (g : F.X.T → Fin 4 → Fin 4 → ℝ) (a b c d : Fin 4) (p : F.X.T) : ℝ :=
  sum4 (fun r => g p a r * naiveCurv F Γf p r b c d)

/-- 对偶交换残差（pair-swap residual）：PS_{abcd} = R4_{abcd} − R4_{cdab}。
    连续理论中 R_{abcd} = R_{cdab}（对偶交换），PS ≡ 0；差分代数中
    PS = O(∂̃Γ)（一阶差分结构），是场层级 Ricci 不对称的精确载体。 -/
def pairSwapRes (F : FrameRecObj) (Γf : GammaField F)
    (g : F.X.T → Fin 4 → Fin 4 → ℝ) (a b c d : Fin 4) (p : F.X.T) : ℝ :=
  lower4 F Γf g a b c d p - lower4 F Γf g c d a b p

/-- 度量 Ricci = 裸迹 Ricci（纯 δ-代数，无场方程/对称性假设）：
    Σ_{a,b} ginv^{ab} R4_{bσaν} = Riĉ_{σν}。证明：ginv 因子移入 r-和
    （mul_sum）→ b/r 双和交换（sum_comm）→ 因子化（sum_mul）→
    δ 缩并（hctr）→ δ 求值（sum4_ite_eq'）→ ricciTensor 定义。 -/
lemma metric_ricci_eq (F : FrameRecObj) (Γf : GammaField F)
    (g ginv : F.X.T → Fin 4 → Fin 4 → ℝ)
    (hctr : ∀ p m s, sum4 (fun i => ginv p m i * g p i s) = if s = m then 1 else 0)
    (σ ν : Fin 4) (p : F.X.T) :
    sum4 (fun a => sum4 (fun b => ginv p a b * lower4 F Γf g b σ a ν p))
    = ricciTensor F Γf σ ν p := by
  simp only [lower4, sum4_eq_finset_sum, Finset.mul_sum]
  have e1 : (∑ a, ∑ b, ∑ r, ginv p a b * (g p b r * naiveCurv F Γf p r σ a ν))
      = ∑ a, ∑ r, (∑ b, ginv p a b * g p b r) * naiveCurv F Γf p r σ a ν := by
    apply Finset.sum_congr rfl; intro a _
    rw [Finset.sum_comm (f := fun b r => ginv p a b * (g p b r * naiveCurv F Γf p r σ a ν))]
    apply Finset.sum_congr rfl; intro r _
    calc (∑ b, ginv p a b * (g p b r * naiveCurv F Γf p r σ a ν))
        = ∑ b, (ginv p a b * g p b r) * naiveCurv F Γf p r σ a ν := by
          apply Finset.sum_congr rfl; intro b _; ring
      _ = (∑ b, ginv p a b * g p b r) * naiveCurv F Γf p r σ a ν :=
          (Finset.sum_mul _ _ _).symm
  rw [e1]
  have e2 : (∑ a, ∑ r, (∑ b, ginv p a b * g p b r) * naiveCurv F Γf p r σ a ν)
      = ∑ a, ∑ r, (if r = a then (1:ℝ) else 0) * naiveCurv F Γf p r σ a ν := by
    apply Finset.sum_congr rfl; intro a _
    apply Finset.sum_congr rfl; intro r _
    have h := hctr p a r
    rw [sum4_eq_finset_sum] at h
    rw [h]
  rw [e2]
  have e3 : (∑ a, ∑ r, (if r = a then (1:ℝ) else 0) * naiveCurv F Γf p r σ a ν)
      = ∑ a, naiveCurv F Γf p a σ a ν := by
    apply Finset.sum_congr rfl; intro a _
    rw [← sum4_eq_finset_sum]
    exact sum4_ite_eq' a (fun r => naiveCurv F Γf p r σ a ν)
  rw [e3]
  simp only [ricciTensor, sum4_eq_finset_sum]

set_option maxHeartbeats 1000000 in
set_option maxRecDepth 32768 in
/-- **修正 Ricci 对称性**（场层级，(β)-4 前置缺口闭合）：
    Riĉ_{σν} − Riĉ_{νσ} = ½ ginv^{ab} (PS_{bσaν} − PS_{bνaσ})，
    其中 PS 为 (0,4) 曲率的对偶交换残差。纯代数恒等式（pair swap 分解 +
    ginv·g = δ + ginv 对称），无场方程、无联络假设。
    物理含义：场层级 Ricci 不对称（预实验 ≈0.29·|Ric|）的精确载体是
    PS——连续理论中恒零的对偶交换对称性在差分代数中的残差（O(∂̃Γ)）；
    骨架层（∂̃≡0）下 PS ≡ 0，退化为骨架 Ricci 对称 skeleton_ricci_symmetric。
    证明：metric_ricci_eq 两侧化度量 Ricci = 裸迹 Ricci；pair swap 分解
    A = −A + S（hX/hY 为 ginv 对称下的双和换名，dist 为乘积分配）。 -/
theorem modified_ricci_symmetry (F : FrameRecObj) (Γf : GammaField F)
    (g ginv : F.X.T → Fin 4 → Fin 4 → ℝ)
    (hginv : ∀ p μ ν, ginv p μ ν = ginv p ν μ)
    (hctr : ∀ p m s, sum4 (fun i => ginv p m i * g p i s) = if s = m then 1 else 0)
    (σ ν : Fin 4) (p : F.X.T) :
    ricciTensor F Γf σ ν p - ricciTensor F Γf ν σ p
    = (1/2) * sum4 (fun a => sum4 (fun b => ginv p a b *
        (pairSwapRes F Γf g b σ a ν p - pairSwapRes F Γf g b ν a σ p))) := by
  have e1 := metric_ricci_eq F Γf g ginv hctr σ ν p
  have e2 := metric_ricci_eq F Γf g ginv hctr ν σ p
  rw [← e1, ← e2]
  have hX : (∑ a, ∑ b, ginv p a b * lower4 F Γf g a ν b σ p)
      = ∑ a, ∑ b, ginv p a b * lower4 F Γf g b ν a σ p := by
    rw [Finset.sum_comm (f := fun a b => ginv p a b * lower4 F Γf g a ν b σ p)]
    apply Finset.sum_congr rfl; intro q _
    apply Finset.sum_congr rfl; intro a _
    rw [hginv p a q]
  have hY : (∑ a, ∑ b, ginv p a b * lower4 F Γf g a σ b ν p)
      = ∑ a, ∑ b, ginv p a b * lower4 F Γf g b σ a ν p := by
    rw [Finset.sum_comm (f := fun a b => ginv p a b * lower4 F Γf g a σ b ν p)]
    apply Finset.sum_congr rfl; intro q _
    apply Finset.sum_congr rfl; intro a _
    rw [hginv p a q]
  have dist : (∑ a, ∑ b, ginv p a b *
        (pairSwapRes F Γf g b σ a ν p - pairSwapRes F Γf g b ν a σ p))
      = (∑ a, ∑ b, ginv p a b * lower4 F Γf g b σ a ν p)
        - (∑ a, ∑ b, ginv p a b * lower4 F Γf g a ν b σ p)
        - (∑ a, ∑ b, ginv p a b * lower4 F Γf g b ν a σ p)
        + (∑ a, ∑ b, ginv p a b * lower4 F Γf g a σ b ν p) := by
    rw [← Finset.sum_sub_distrib, ← Finset.sum_sub_distrib,
      ← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl; intro a _
    rw [← Finset.sum_sub_distrib, ← Finset.sum_sub_distrib,
      ← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl; intro b _
    simp only [pairSwapRes, sub_eq_add_neg]
    ring
  simp only [sum4_eq_finset_sum]
  rw [dist, hX, hY]
  ring

-- §26.14 ginv 升指标的 Leibniz 修正（(β)-4 第二阶段缺口②，2026-09-12）

/-- sum4 逐点同余。 -/
lemma sum4_congr {f h : Fin 4 → ℝ} (he : ∀ i, f i = h i) : sum4 f = sum4 h := by
  simp only [sum4, he 0, he 1, he 2, he 3]

/-- **右 δ-解引理**：若 Σ_j A j·g x j s = B s（∀s），且 g/ginv 对称互逆
    （ginv·g = δ），则 A t = Σ_s B s·ginv x s t——即线性方程 A·g = B 在
    互逆对称下的显式解。证明：δ-插入（A j = Σ_s A j·g j s·ginv s t，
    其中 g·ginv = δ 由 g/ginv 双对称从 hctr 推出）+ sum_comm + 因子化。 -/
lemma solve_right (F : FrameRecObj) (g ginv : F.X.T → Fin 4 → Fin 4 → ℝ)
    (hg : ∀ p μ ν, g p μ ν = g p ν μ)
    (hginv : ∀ p μ ν, ginv p μ ν = ginv p ν μ)
    (hctr : ∀ p m s, sum4 (fun i => ginv p m i * g p i s) = if s = m then 1 else 0)
    (A B : Fin 4 → ℝ) (x : F.X.T)
    (hAB : ∀ s, sum4 (fun j => A j * g x j s) = B s) (t : Fin 4) :
    A t = sum4 (fun s => B s * ginv x s t) := by
  have hdelta : ∀ j, sum4 (fun s => g x j s * ginv x s t) = if j = t then 1 else 0 := by
    intro j
    have e : sum4 (fun s => g x j s * ginv x s t)
        = sum4 (fun i => ginv x t i * g x i j) := by
      apply sum4_congr; intro i
      rw [mul_comm, hginv x i t, hg x i j]
    rw [e, hctr x t j]
  calc A t = sum4 (fun j => (if j = t then 1 else 0) * A j) :=
        (sum4_ite_eq' t A).symm
    _ = sum4 (fun j => sum4 (fun s => g x j s * ginv x s t) * A j) := by
        apply sum4_congr; intro j
        rw [hdelta j]
    _ = sum4 (fun s => sum4 (fun j => g x j s * ginv x s t * A j)) := by
        simp only [sum4_eq_finset_sum, Finset.sum_mul]
        rw [Finset.sum_comm (f := fun s j => (g x j s * ginv x s t) * A j)]
    _ = sum4 (fun s => B s * ginv x s t) := by
        apply sum4_congr; intro s
        rw [← hAB s]
        simp only [sum4_eq_finset_sum]
        rw [Finset.sum_mul]
        refine Finset.sum_congr rfl fun j _ => ?_
        ring

/-- **ginv 差分恒等式（左移位变体）**：∂̃_ρ ginv^{μν}(x)
    = −ginv^{μa}(step_ρ x)·∂̃_ρ g_{ab}(x)·ginv^{bν}(x)。
    逐点精确（双 δ + 双对称），连续对应 ∂(g^{-1}) = −g^{-1}∂g g^{-1}。 -/
theorem dginv_left (F : FrameRecObj) (g ginv : F.X.T → Fin 4 → Fin 4 → ℝ)
    (hg : ∀ p μ ν, g p μ ν = g p ν μ)
    (hginv : ∀ p μ ν, ginv p μ ν = ginv p ν μ)
    (hctr : ∀ p m s, sum4 (fun i => ginv p m i * g p i s) = if s = m then 1 else 0)
    (ρ μ ν : Fin 4) (x : F.X.T) :
    ginv (F.stepD ρ x) μ ν - ginv x μ ν
    = -sum4 (fun a => sum4 (fun b => ginv (F.stepD ρ x) μ a
        * (g (F.stepD ρ x) a b - g x a b) * ginv x b ν)) := by
  have hAB : ∀ s, sum4 (fun j => (ginv (F.stepD ρ x) μ j - ginv x μ j) * g x j s)
      = -sum4 (fun a => ginv (F.stepD ρ x) μ a
        * (g (F.stepD ρ x) a s - g x a s)) := by
    intro s
    have e1 := hctr (F.stepD ρ x) μ s
    have e2 := hctr x μ s
    have e3 : sum4 (fun j => ginv (F.stepD ρ x) μ j * g x j s)
        = sum4 (fun j => ginv (F.stepD ρ x) μ j * g (F.stepD ρ x) j s)
          - sum4 (fun j => ginv (F.stepD ρ x) μ j
            * (g (F.stepD ρ x) j s - g x j s)) := by
      unfold sum4; ring
    calc sum4 (fun j => (ginv (F.stepD ρ x) μ j - ginv x μ j) * g x j s)
        = sum4 (fun j => ginv (F.stepD ρ x) μ j * g x j s)
          - sum4 (fun j => ginv x μ j * g x j s) := by unfold sum4; ring
      _ = sum4 (fun j => ginv (F.stepD ρ x) μ j * g (F.stepD ρ x) j s)
          - sum4 (fun j => ginv (F.stepD ρ x) μ j
            * (g (F.stepD ρ x) j s - g x j s))
          - sum4 (fun j => ginv x μ j * g x j s) := by rw [e3]
      _ = (if s = μ then 1 else 0)
          - sum4 (fun j => ginv (F.stepD ρ x) μ j
            * (g (F.stepD ρ x) j s - g x j s))
          - (if s = μ then 1 else 0) := by rw [e1, e2]
      _ = -sum4 (fun a => ginv (F.stepD ρ x) μ a
            * (g (F.stepD ρ x) a s - g x a s)) := by ring
  have hs := solve_right F g ginv hg hginv hctr
    (fun j => ginv (F.stepD ρ x) μ j - ginv x μ j)
    (fun s => -sum4 (fun a => ginv (F.stepD ρ x) μ a
      * (g (F.stepD ρ x) a s - g x a s)))
    x hAB ν
  rw [hs]
  simp only [sum4_eq_finset_sum]
  have step1 : (∑ i, (-∑ a, ginv (F.stepD ρ x) μ a
        * (g (F.stepD ρ x) a i - g x a i)) * ginv x i ν)
      = -∑ i, (∑ a, ginv (F.stepD ρ x) μ a
        * (g (F.stepD ρ x) a i - g x a i)) * ginv x i ν := by
    rw [← Finset.sum_neg_distrib]
    apply Finset.sum_congr rfl; intro i _
    ring
  have step2 : (∑ i, (∑ a, ginv (F.stepD ρ x) μ a
        * (g (F.stepD ρ x) a i - g x a i)) * ginv x i ν)
      = ∑ b, ∑ a, ginv (F.stepD ρ x) μ a
        * (g (F.stepD ρ x) a b - g x a b) * ginv x b ν := by
    have e : (∑ i, (∑ a, ginv (F.stepD ρ x) μ a
          * (g (F.stepD ρ x) a i - g x a i)) * ginv x i ν)
        = ∑ i, ∑ a, ginv (F.stepD ρ x) μ a
          * (g (F.stepD ρ x) a i - g x a i) * ginv x i ν := by
      simp only [Finset.sum_mul]
    rw [e, Finset.sum_comm (f := fun i a => ginv (F.stepD ρ x) μ a
      * (g (F.stepD ρ x) a i - g x a i) * ginv x i ν)]
  rw [step1, step2, Finset.sum_comm (f := fun a b => ginv (F.stepD ρ x) μ a
    * (g (F.stepD ρ x) a b - g x a b) * ginv x b ν)]

/-- **ginv 差分恒等式（右移位变体）**：∂̃_ρ ginv^{μν}(x)
    = −ginv^{μa}(x)·∂̃_ρ g_{ab}(x)·ginv^{bν}(step_ρ x)。
    与 dginv_left 对称（在 step_ρ x 点解方程）。 -/
theorem dginv_right (F : FrameRecObj) (g ginv : F.X.T → Fin 4 → Fin 4 → ℝ)
    (hg : ∀ p μ ν, g p μ ν = g p ν μ)
    (hginv : ∀ p μ ν, ginv p μ ν = ginv p ν μ)
    (hctr : ∀ p m s, sum4 (fun i => ginv p m i * g p i s) = if s = m then 1 else 0)
    (ρ μ ν : Fin 4) (x : F.X.T) :
    ginv (F.stepD ρ x) μ ν - ginv x μ ν
    = -sum4 (fun a => sum4 (fun b => ginv x μ a
        * (g (F.stepD ρ x) a b - g x a b) * ginv (F.stepD ρ x) b ν)) := by
  have hAB : ∀ s, sum4 (fun j => (ginv (F.stepD ρ x) μ j - ginv x μ j)
        * g (F.stepD ρ x) j s)
      = -sum4 (fun a => ginv x μ a * (g (F.stepD ρ x) a s - g x a s)) := by
    intro s
    have e1 := hctr (F.stepD ρ x) μ s
    have e2 := hctr x μ s
    have e3 : sum4 (fun j => ginv x μ j * g (F.stepD ρ x) j s)
        = sum4 (fun j => ginv x μ j * g x j s)
          + sum4 (fun j => ginv x μ j
            * (g (F.stepD ρ x) j s - g x j s)) := by
      unfold sum4; ring
    calc sum4 (fun j => (ginv (F.stepD ρ x) μ j - ginv x μ j)
          * g (F.stepD ρ x) j s)
        = sum4 (fun j => ginv (F.stepD ρ x) μ j * g (F.stepD ρ x) j s)
          - sum4 (fun j => ginv x μ j * g (F.stepD ρ x) j s) := by
          unfold sum4; ring
      _ = sum4 (fun j => ginv (F.stepD ρ x) μ j * g (F.stepD ρ x) j s)
          - sum4 (fun j => ginv x μ j * g x j s)
          - sum4 (fun j => ginv x μ j
            * (g (F.stepD ρ x) j s - g x j s)) := by rw [e3]; ring
      _ = (if s = μ then 1 else 0) - (if s = μ then 1 else 0)
          - sum4 (fun j => ginv x μ j
            * (g (F.stepD ρ x) j s - g x j s)) := by rw [e1, e2]
      _ = -sum4 (fun a => ginv x μ a
            * (g (F.stepD ρ x) a s - g x a s)) := by ring
  have hs := solve_right F g ginv hg hginv hctr
    (fun j => ginv (F.stepD ρ x) μ j - ginv x μ j)
    (fun s => -sum4 (fun a => ginv x μ a
      * (g (F.stepD ρ x) a s - g x a s)))
    (F.stepD ρ x) hAB ν
  rw [hs]
  simp only [sum4_eq_finset_sum]
  have step1 : (∑ i, (-∑ a, ginv x μ a
        * (g (F.stepD ρ x) a i - g x a i)) * ginv (F.stepD ρ x) i ν)
      = -∑ i, (∑ a, ginv x μ a
        * (g (F.stepD ρ x) a i - g x a i)) * ginv (F.stepD ρ x) i ν := by
    rw [← Finset.sum_neg_distrib]
    apply Finset.sum_congr rfl; intro i _
    ring
  have step2 : (∑ i, (∑ a, ginv x μ a
        * (g (F.stepD ρ x) a i - g x a i)) * ginv (F.stepD ρ x) i ν)
      = ∑ b, ∑ a, ginv x μ a
        * (g (F.stepD ρ x) a b - g x a b) * ginv (F.stepD ρ x) b ν := by
    have e : (∑ i, (∑ a, ginv x μ a
          * (g (F.stepD ρ x) a i - g x a i)) * ginv (F.stepD ρ x) i ν)
        = ∑ i, ∑ a, ginv x μ a
          * (g (F.stepD ρ x) a i - g x a i) * ginv (F.stepD ρ x) i ν := by
      simp only [Finset.sum_mul]
    rw [e, Finset.sum_comm (f := fun i a => ginv x μ a
      * (g (F.stepD ρ x) a i - g x a i) * ginv (F.stepD ρ x) i ν)]
  rw [step1, step2, Finset.sum_comm (f := fun a b => ginv x μ a
    * (g (F.stepD ρ x) a b - g x a b) * ginv (F.stepD ρ x) b ν)]

/-- **离散度规相容恒等式**：∂̃_ρ g_{μν}(x) = g_{μλ}(x)·Γ^λ_{ρν}(x)
    + g_{νλ}(x)·Γ^λ_{ρμ}(x)，对任何满足离散 Christoffel 公式
    Γ^r_{μn} = ½ ginv^{rl}(∂̃_μ g_{ln} + ∂̃_n g_{μl} − ∂̃_l g_{nμ}) 的 Γ
    逐点精确成立。纯 δ-代数（δ 在 x 点 + g/ginv 双对称），无场方程。
    连续对应 ∇_ρ g_{μν} = 0（Levi-Civita 相容性）的差分形态；
    升指标 ∇̃^μ = ginv^{μa}∇̃_a 的 Leibniz 修正由 dginv_left/right 给出。 -/
theorem discrete_metric_compatible (F : FrameRecObj)
    (g ginv : F.X.T → Fin 4 → Fin 4 → ℝ)
    (hg : ∀ p μ ν, g p μ ν = g p ν μ)
    (hginv : ∀ p μ ν, ginv p μ ν = ginv p ν μ)
    (hctr : ∀ p m s, sum4 (fun i => ginv p m i * g p i s) = if s = m then 1 else 0)
    (Gam : F.X.T → Fin 4 → Fin 4 → Fin 4 → ℝ)
    (hGam : ∀ x r mu n, Gam x r mu n = (1/2:ℝ) * sum4 (fun l => ginv x r l *
        ((g (F.stepD mu x) l n - g x l n) + (g (F.stepD n x) mu l - g x mu l)
          - (g (F.stepD l x) n mu - g x n mu))))
    (ρ μ ν : Fin 4) (x : F.X.T) :
    g (F.stepD ρ x) μ ν - g x μ ν
    = sum4 (fun la => g x μ la * Gam x la ρ ν)
      + sum4 (fun la => g x ν la * Gam x la ρ μ) := by
  have key0 : ∀ (a : Fin 4) (T : Fin 4 → ℝ),
      sum4 (fun la => g x a la * sum4 (fun l => ginv x la l * T l)) = T a := by
    intro a T
    have hd : ∀ l, (∑ la : Fin 4, g x a la * ginv x la l)
        = if a = l then 1 else 0 := by
      intro l
      have e : (∑ la : Fin 4, g x a la * ginv x la l)
          = ∑ i : Fin 4, ginv x l i * g x i a := by
        apply Finset.sum_congr rfl; intro i _
        rw [mul_comm, hginv x i l, hg x i a]
      rw [e, ← sum4_eq_finset_sum]
      exact hctr x l a
    calc sum4 (fun la => g x a la * sum4 (fun l => ginv x la l * T l))
        = sum4 (fun l => sum4 (fun la => (g x a la * ginv x la l) * T l)) := by
          simp only [sum4_eq_finset_sum]
          rw [show (∑ la, g x a la * ∑ l, ginv x la l * T l)
              = ∑ la, ∑ l, g x a la * (ginv x la l * T l) from by
              refine Finset.sum_congr rfl fun la _ => ?_
              rw [Finset.mul_sum]]
          rw [Finset.sum_comm (f := fun la l => g x a la * (ginv x la l * T l))]
          refine Finset.sum_congr rfl fun l _ => ?_
          refine Finset.sum_congr rfl fun la _ => ?_
          ring
      _ = sum4 (fun l => (if a = l then 1 else 0) * T l) := by
          apply sum4_congr; intro l
          simp only [sum4_eq_finset_sum]
          rw [show (∑ la, g x a la * ginv x la l * T l)
              = (∑ la, g x a la * ginv x la l) * T l
              from (Finset.sum_mul _ _ _).symm, hd l]
      _ = T a := by
          have flip : sum4 (fun l => (if a = l then 1 else 0) * T l)
              = sum4 (fun l => (if l = a then 1 else 0) * T l) := by
            apply sum4_congr; intro l
            by_cases h : a = l
            · simp [h, eq_comm]
            · simp [h, eq_comm]
          rw [flip, sum4_ite_eq' a T]
  have key : ∀ (a : Fin 4) (T : Fin 4 → ℝ),
      sum4 (fun la => g x a la * ((1/2:ℝ) * sum4 (fun l => ginv x la l * T l)))
      = (1/2:ℝ) * T a := by
    intro a T
    have half : sum4 (fun la => g x a la * ((1/2:ℝ) *
          sum4 (fun l => ginv x la l * T l)))
        = (1/2:ℝ) * sum4 (fun la => g x a la * sum4 (fun l => ginv x la l * T l)) := by
      simp only [sum4_eq_finset_sum]
      rw [Finset.mul_sum]
      refine Finset.sum_congr rfl fun la _ => ?_
      ring
    rw [half, key0 a T]
  simp only [hGam]
  rw [key μ (fun l => (g (F.stepD ρ x) l ν - g x l ν)
      + (g (F.stepD ν x) ρ l - g x ρ l) - (g (F.stepD l x) ν ρ - g x ν ρ)),
    key ν (fun l => (g (F.stepD ρ x) l μ - g x l μ)
      + (g (F.stepD μ x) ρ l - g x ρ l) - (g (F.stepD l x) μ ρ - g x μ ρ))]
  rw [hg (F.stepD ρ x) ν μ, hg x ν μ, hg (F.stepD ν x) ρ μ, hg x ρ μ,
    hg (F.stepD μ x) ν ρ, hg x ν ρ]
  ring

end MUFPF
