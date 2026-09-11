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
  ring

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

end MUFPF
