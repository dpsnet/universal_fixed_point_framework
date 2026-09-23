-- ============================================================
-- GPFlowTimeDep.lean — paper14 G4：谱流的时间依赖守恒律（有限维代数闭合）
-- ============================================================

/-
# GPFlowTimeDep.lean — G4 时间依赖守恒律：tr(A(t)^k) 沿谱流恒定

背景：GPFlow.lean §3 开放登记第 1 项「时间依赖守恒律：d/dt tr(A(t)^k) = 0」。
GP 谱流方程的解是 A(t) = exp(t·A_F)·A₀·exp(−t·A_F)（spectralFlow，SpectralDynamics）。
本模块证明的是**比 d/dt = 0 更强的点式恒等**：

    tr(A(t)^k) = tr(A₀^k)    对所有 t（同时即 d/dt tr(A(t)^k) = 0）

推导链（纯代数，不需要 exp 的导数）：

  1. exp(t·A_F) 与 exp(−t·A_F) 互为双侧逆。矩阵不是 DivisionRing，故不能用
     exp_neg（需 DivisionRing）；改用 exp_add_of_commute（Commute.refl 取负）
     + exp_zero：exp x·exp(−x) = exp(x + −x) = exp 0 = 1，反向同理由
     Commute.refl 取负左 给出。exp 保谱流结构。
  2. **谱流点式保迹幂**（SpectralInvariant.trace_pow_similar 实例化）：A(t) 与 A₀
     经 exp(t·A_F) 相似，相似保持全部迹幂 tr(·^k)——经 Newton 恒等式即保谱。
  3. 该函数 t ↦ tr(A(t)^k) 为常值函数（恒等于 tr(A₀^k)），故其 HasDerivAt 为 0
     ——这给出 d/dt tr(A(t)^k) = 0（时间依赖守恒律，GPFlow §3 #1 闭合）。

物理含义：tr(A(t)^k) 沿 GP 谱流方程 dA/dt=[A_F,A] 不变，是推论 4.2「涡旋拓扑
荷守恒 dn/dt=0」的**逐时刻（时间依赖）**谱版本——比 GPFlow 的交换子方向消失
（瞬时）再进一步：守恒在解曲线上逐点成立，无需微分。

数学内容（全部零 sorry）：
  §1 exp_smul_mul_exp_neg_smul：exp(t·A)·exp(−t·A) = 1（右逆）
  §2 exp_neg_smul_mul_exp_smul：exp(−t·A)·exp(t·A) = 1（左逆）
  §3 trace_pow_invariant_flow：**核心**——tr(spectralFlow A₀ A_F t ^ k) = tr(A₀^k)
  §4 trace_pow_flow_conservation：d/dt tr(A(t)^k) = 0（HasDerivAt 常值）
  §5 spectralFlow_charpoly_eq：特征多项式沿解曲线逐点不变（相似保特征多项式，
    比迹幂更强一层）
  §6 开放登记：特征值计重数逐点恒定（需根多重数基础设施）、依赖时间的幺正
    规范势（U 时变）协变形式

诚实边界：本模块不证明 dA/dt = [A_F, A] 的生成元级时间导数（需 exp 的导数，
此 mathlib 版本无该引理，合适范数球/级数导数基础设施缺席）；我们证明的是
**迹幂在解曲线上逐点恒定**这一守恒律本身，其蕴含 d/dt tr(A^k) = 0 而无需求
exp 导数。-/

import Mathlib.Data.Complex.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.LinearAlgebra.Matrix.Charpoly.Basic
import Mathlib.LinearAlgebra.Matrix.Charpoly.Eigs
import Mathlib.Algebra.Polynomial.Roots
import Mathlib.Analysis.Complex.Polynomial.Basic
import Mathlib.Analysis.Normed.Algebra.MatrixExponential
import Mathlib.Analysis.Calculus.Deriv.Basic
import MUFPFormalization.SpectralInvariant
import MUFPFormalization.SpectralDynamics

open Matrix

namespace MUFPF

variable {n : ℕ}

/-- §1：exp 的右逆性——exp(t·A)·exp(−t·A) = 1。矩阵非 DivisionRing，故不用
    exp_neg（需 NormedCommRing）；用 Matrix.exp_add_of_commute
    （Commute (t·A) (−(t·A))，由 Commute.refl 取负）+ 加性消去 + exp_zero：
    exp x·exp(−x) = exp(x + (−x)) = exp 0 = 1。 -/
theorem exp_smul_mul_exp_neg_smul (t : ℝ) (A : Matrix (Fin n) (Fin n) ℂ) :
    NormedSpace.exp (t • A) * NormedSpace.exp (-t • A) = 1 := by
  have hneg : NormedSpace.exp (-t • A) = NormedSpace.exp (-(t • A)) := by
    rw [neg_smul]
  rw [hneg]
  have hcomm : Commute (t • A) (-(t • A)) := (Commute.refl (t • A)).neg_right
  calc
    NormedSpace.exp (t • A) * NormedSpace.exp (-(t • A))
        = NormedSpace.exp (t • A + (-(t • A))) :=
          (Matrix.exp_add_of_commute (t • A) (-(t • A)) hcomm).symm
    _ = NormedSpace.exp (0 : Matrix (Fin n) (Fin n) ℂ) := by rw [add_neg_cancel]
    _ = 1 := NormedSpace.exp_zero

/-- §2：exp 的左逆性——exp(−t·A)·exp(t·A) = 1。同 §1，用 Commute.refl 取负左。 -/
theorem exp_neg_smul_mul_exp_smul (t : ℝ) (A : Matrix (Fin n) (Fin n) ℂ) :
    NormedSpace.exp (-t • A) * NormedSpace.exp (t • A) = 1 := by
  have hneg : NormedSpace.exp (-t • A) = NormedSpace.exp (-(t • A)) := by
    rw [neg_smul]
  rw [hneg]
  have hcomm : Commute (-(t • A)) (t • A) := (Commute.refl (t • A)).neg_left
  calc
    NormedSpace.exp (-(t • A)) * NormedSpace.exp (t • A)
        = NormedSpace.exp (-(t • A) + t • A) :=
          (Matrix.exp_add_of_commute (-(t • A)) (t • A) hcomm).symm
    _ = NormedSpace.exp (0 : Matrix (Fin n) (Fin n) ℂ) := by rw [neg_add_cancel]
    _ = 1 := NormedSpace.exp_zero

/-- §3：**核心——谱流点式保迹幂（时间依赖守恒）**。对任意 A₀、A_F 与幂次 k，
    tr(spectralFlow A₀ A_F t ^ k) = tr(A₀^k) 对所有 t 成立。由 §1/§2 得
    exp(t·A_F) 与 exp(−t·A_F) 互为双侧逆，故 A(t) 与 A₀ 相似于互逆对；
    迹幂相似不变性（SpectralInvariant.trace_pow_similar）逐点闭合。经 Newton
    恒等式，这蕴含 A(t) 与 A₀ 同谱——谱流保谱逐瞬间。 -/
theorem trace_pow_invariant_flow (A₀ A_F : Matrix (Fin n) (Fin n) ℂ) (t : ℝ) (k : ℕ) :
    ((spectralFlow A₀ A_F t) ^ k).trace = (A₀ ^ k).trace := by
  unfold spectralFlow
  exact trace_pow_similar A₀ (NormedSpace.exp (-t • A_F)) (NormedSpace.exp (t • A_F))
    (exp_neg_smul_mul_exp_smul t A_F) (exp_smul_mul_exp_neg_smul t A_F) k

/-- §4：**时间依赖守恒律（微分形式）**——函数 t ↦ tr(A(t)^k) 为常值（恒等于
    tr(A₀^k)，§3 对每个 t 成立），故其导数处处为 0：
    d/dt tr(A(t)^k) = 0。这是 GPFlow §3 #1 登记项的闭合；比交换子方向消失
    （GPFlow.trace_pow_mul_commutator_eq_zero，瞬时）更进一步：守恒沿解曲线
    逐点成立。 -/
theorem trace_pow_flow_conservation (A₀ A_F : Matrix (Fin n) (Fin n) ℂ)
    (t : ℝ) (k : ℕ) :
    HasDerivAt (fun τ : ℝ => ((spectralFlow A₀ A_F τ) ^ k).trace) (0 : ℂ) t := by
  have hconst :
      (fun τ : ℝ => ((spectralFlow A₀ A_F τ) ^ k).trace) = fun _ : ℝ => (A₀ ^ k).trace := by
    funext τ
    exact trace_pow_invariant_flow A₀ A_F τ k
  rw [hconst]
  exact hasDerivAt_const (F := ℂ) (𝕜 := ℝ) (c := (A₀ ^ k).trace) (x := t)

/-- §5：**谱沿解曲线的逐点恒定（特征多项式层）**。谱流解
    spectralFlow A₀ A_F t = exp(t·A_F)·A₀·exp(−t·A_F) 本就是 A₀ 的相似矩阵
    （§1/§2 给出 exp(t·A_F) 与 exp(−t·A_F) 互为双侧逆）；相似保持特征多项式
    （mathlib `Matrix.charpoly_units_conj`），故特征多项式沿解曲线逐点不变。
    这比 §3 的迹幂守恒更强一层（特征多项式 ⟹ 全部迹幂，Newton 恒等式），
    直接确立"谱在解曲线上恒定元"这一 GPFlow §3 #2 谱不变性的点式版本。 -/
theorem spectralFlow_charpoly_eq (A₀ A_F : Matrix (Fin n) (Fin n) ℂ) (t : ℝ) :
    (spectralFlow A₀ A_F t).charpoly = A₀.charpoly := by
  -- exp(t·A_F) 可逆（单位元），逆为 exp(−t·A_F)（§1/§2 双侧逆）
  let u : (Matrix (Fin n) (Fin n) ℂ)ˣ :=
    ⟨NormedSpace.exp (t • A_F), NormedSpace.exp (-t • A_F),
      exp_smul_mul_exp_neg_smul t A_F, exp_neg_smul_mul_exp_smul t A_F⟩
  -- charpoly_units_conj：u·A₀·u⁻¹ 与 A₀ 相似 ⟹ 特征多项式相同
  --（u⁻¹.val = exp(−t·A_F)，故 spectralFlow = u.val·A₀·(u⁻¹).val）
  have hsim : spectralFlow A₀ A_F t = u.val * A₀ * (u⁻¹).val := by
    simp [spectralFlow, u]
  simp [hsim, Matrix.charpoly_units_conj]

/- §6 开放登记（paper14 G4 时间依赖部分，不占用 sorry，真证路径见下）：

  1. **特征值（计重数）逐点恒定**：§5 已证特征多项式沿解曲线逐点不变
     （`spectralFlow_charpoly_eq`）；特征多项式 ⟹ 特征值多重集只需**乘法分解**
     引理（首一多项式恰有 k 个根，计重数）——需 `Polynomial` 根多重数基础设施
     （中等）。§3 的迹幂同一（`trace_pow_invariant_flow`）给出同一结论的
     Newton 等价面（遍所有 k），两路最终汇聚于"谱恒定"。
  2. **生成元级时间导数**：dA/dt = [A_F, A]（谱流方程的生成元形式）。需
     exp 的导数（d/dt exp(t·A_F)），此 mathlib 版本在 NormedSpace.exp 上缺席
     Fréchet/级数导数引理；矩阵非 DivisionRing 亦阻断 exp_neg。以"迹幂逐点
     恒定"这一守恒正确性均有保障（本模块），生成元级导数属基础设施缺口。
  3. **依赖时间的幺正规范势**：U = U(t) 时变时 A ↦ U(t)†·A·U(t) 的协变导数
     引入规范势 U†·U̇（GPFlow §3 #5）。需依赖时间的幺正群与分析，属远期。

  已闭合（本模块，零 sorry）：exp(t·A)·exp(±t·A) 双侧逆 + 谱流点式保迹幂
  tr(A(t)^k)=tr(A₀^k) + 时间依赖守恒律 d/dt tr(A(t)^k) = 0 + 特征多项式逐点
  恒定（`spectralFlow_charpoly_eq`）+ 特征值多重集逐点恒定（`spectralFlow_roots_eq`）
  + 行列式守恒（`spectralFlow_det_eq`，v1.11 闭合）。-/

/-- §6：**特征值多重集（计重数）**。矩阵 A 的（复）特征值带重数的多重集，
    定义为特征多项式的根多重集 `Polynomial.roots`。ℂ 是代数闭域，故任意方阵
    的特征多项式在 ℂ 中完全分裂，`roots` 恰含 n（=维度）个根（计重数）——
    这正是"谱"作为带重数多次集的代数载体。 -/
noncomputable def spectrum_mulset (A : Matrix (Fin n) (Fin n) ℂ) : Multiset ℂ :=
  A.charpoly.roots

/-- §6 核心：**谱流保特征值多重集**（谱沿解曲线逐点恒定的多重集形式）。由
    §5 `spectralFlow_charpoly_eq`（特征多项式逐点恒定）+ `congrArg`（对
    `Polynomial.roots` 替换）即得：A(t) 与 A₀ 的特征值带重数完全相同的多重集。
    这是 §6 开放登记第 1 项（特征值计重数逐点恒定）的闭合——比 §3 的迹幂同一
    （Newton 等价面）与 §5 的特征多项式更直接地落在"谱集"本身。 -/
theorem spectralFlow_roots_eq (A₀ A_F : Matrix (Fin n) (Fin n) ℂ) (t : ℝ) :
    spectrum_mulset (spectralFlow A₀ A_F t) = spectrum_mulset A₀ := by
  unfold spectrum_mulset
  exact congrArg Polynomial.roots (spectralFlow_charpoly_eq A₀ A_F t)

/-- §6 推论：**行列式（特征值乘积）逐点守恒**。行列式 = 特征多项式根之积
    （ℂ 代数闭，`Matrix.det_eq_prod_roots_charpoly`），而特征多项式沿解曲线
    逐点不变（§5），故 det A(t) = det A₀。这是涡旋拓扑荷守恒 dn/dt=0 的
    **标量不变量**落点：谱恒定 ⟹ 特征值乘积恒定。 -/
theorem spectralFlow_det_eq (A₀ A_F : Matrix (Fin n) (Fin n) ℂ) (t : ℝ) :
    (spectralFlow A₀ A_F t).det = A₀.det := by
  calc
    (spectralFlow A₀ A_F t).det = (spectralFlow A₀ A_F t).charpoly.roots.prod :=
      Matrix.det_eq_prod_roots_charpoly (spectralFlow A₀ A_F t)
    _ = A₀.charpoly.roots.prod := by
      apply congr_arg Multiset.prod
      exact spectralFlow_roots_eq A₀ A_F t
    _ = A₀.det := (Matrix.det_eq_prod_roots_charpoly A₀).symm

end MUFPF