-- ============================================================
-- UFPF → MUFPF 更名通知（同 WeaveBCS.lean，本文件属于 UFPF/MUFPF）
-- ============================================================

/-
# BerryChern.lean — paper14 G3：Berry 曲率与第一陈数（有限维代数原型）

背景：paper14 定理 3.1（TKNN：σ_xy = (e²/h)·Ch）与命题 3.1（陈数绝热不变性）
此前在 Lean 库零载体（grep Chern/陈数零命中）。本模块建立有限维代数核心：

  §1 Berry 曲率的投影公式 F = -i·Tr(P [A, B])（P 孤立能带谱投影，A=∂ₓP、B=∂ᵧP）
  §2 核心定理：F 实值（Tr(P[A,B]) 纯虚）——陈数良定义的代数基础
  §2.5 投影切向量的代数层：约束方程（带内消没）、带间化简、双交换子形式
  §2.6 规范不变性：Berry 曲率对酉稳定化 P ↦ UPU† 不变（曲率只依赖占据带投影、
    与本征态相位无关）——开放登记 §3 #5 的代数核心
  §3 开放登记：第一陈数积分定义、整性、TKNN、规范不变性联络层面、切向分析

说明：取厄米性假设为显式等式 hP : P = Pᴴ（等价于 Matrix.IsHermitian，但避免
其结构包装使 rw 直接可用）。核心引理只用迹循环性 + 厄米性 + 共轭转置反自同构，
不依赖幂等性，故对任意厄米三件套成立。
-/

import Mathlib.Data.Complex.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.LinearAlgebra.Dimension.Finrank
import Mathlib.LinearAlgebra.Projection
import MUFPFormalization.SpectralInvariant
import Mathlib.MeasureTheory.Integral.CircleIntegral
import Mathlib.MeasureTheory.Integral.TorusIntegral
import Mathlib.MeasureTheory.Integral.Bochner.Set
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Analysis.InnerProductSpace.Symmetric
import Mathlib.Analysis.InnerProductSpace.Projection.Basic
import Mathlib.Analysis.InnerProductSpace.Orthogonal
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.Normed.Lp.PiLp
import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.Analysis.CStarAlgebra.Unitary.Connected
import Mathlib.LinearAlgebra.Matrix.Charpoly.Eigs
import Mathlib.Analysis.Complex.CoveringMap
import Mathlib.Topology.Homotopy.Lifting
import Mathlib.Analysis.InnerProductSpace.ProdL2
import Mathlib.Analysis.Normed.Module.FiniteDimension
import Mathlib.LinearAlgebra.Prod
import Mathlib.LinearAlgebra.Dimension.Constructions
import Mathlib.GroupTheory.FreeAbelianGroup
import Mathlib.Tactic

namespace MUFPF

open Matrix Complex

/-- Berry 曲率（paper14 G3，有限维代数原型）：
    F = -i · Tr(P [A, B])，[A, B] = A·B − B·A。
    P 为孤立能带的谱投影（厄米幂等），A = ∂ₓP、B = ∂ᵧP 为投影族在参数空间
    两个方向的切矩阵（厄米，因伴随与求导交换）。这是第一陈数密度：
    C = (1/2π) ∫ F d²k 的被积函数。 -/
def berryCurvature {n : ℕ} (P A B : Matrix (Fin n) (Fin n) ℂ) : ℂ :=
  -Complex.I * (P * (A * B - B * A)).trace

/-- 核心引理（G3）：对厄米 P、A、B，Tr(P [A, B]) 是"斜伴随"复数（star T = −T，
    即纯虚数）。这是 Berry 曲率为实值（陈数良定义、可积分为实数量子数）的
    代数基础。证明只用迹循环性 + 厄米性 + 共轭转置反自同构，不依赖幂等性。 -/
theorem trace_proj_commutator_skewAdjoint {n : ℕ}
    (P A B : Matrix (Fin n) (Fin n) ℂ)
    (hP : P = Pᴴ) (hA : A = Aᴴ) (hB : B = Bᴴ) :
    star (P * (A * B - B * A)).trace = -((P * (A * B - B * A)).trace) := by
  have key : ((B * A - A * B) * P).trace
      = (B * A * P).trace - (A * B * P).trace := by
    rw [sub_mul, Matrix.trace_sub]
  have hT : (P * (A * B - B * A)).trace
      = (A * B * P).trace - (B * A * P).trace := by
    rw [mul_sub, Matrix.trace_sub,
      Matrix.trace_mul_comm P (A * B), Matrix.trace_mul_comm P (B * A)]
  rw [← Matrix.trace_conjTranspose, Matrix.conjTranspose_mul, Matrix.conjTranspose_sub,
    Matrix.conjTranspose_mul, Matrix.conjTranspose_mul, ← hP, ← hA, ← hB, key, hT]
  ring

/-- **G3 主定理（Berry 曲率实值性）**：对厄米投影 P 与厄米切向量 A、B，
    Berry 曲率 F = −i·Tr(P [A, B]) 的虚部为零——即 F 是实值函数。
    这是第一陈数 C = (1/2π)∫F 良定义（被积函数实值、积分为实数）的基础，
    也是陈数可观测（Hall 电导为实数）的代数根源。 -/
theorem berryCurvature_im_eq_zero {n : ℕ} (P A B : Matrix (Fin n) (Fin n) ℂ)
    (hP : P = Pᴴ) (hA : A = Aᴴ) (hB : B = Bᴴ) :
    (berryCurvature P A B).im = 0 := by
  set T := (P * (A * B - B * A)).trace with hT_def
  have hsk := trace_proj_commutator_skewAdjoint P A B hP hA hB
  -- T.re = 0：由 star T = −T 取实部（star 保实部）
  have hstar_re : (star T).re = T.re := by
    rw [Complex.star_def]; exact Complex.conj_re T
  have hre : T.re = 0 := by
    have h1 : -T.re = T.re := by
      have h2 : (star T).re = (-T).re := by rw [hsk]
      rw [Complex.neg_re] at h2
      linarith [hstar_re, h2]
    linarith
  -- (−I · T).im = (−I).re·T.im + (−I).im·T.re = 0·T.im + (−1)·0 = 0
  show (-Complex.I * T).im = 0
  rw [Complex.mul_im]
  have e1 : (-Complex.I).re = 0 := by simp [Complex.neg_re, Complex.I_re]
  have e2 : (-Complex.I).im = -1 := by simp [Complex.neg_im, Complex.I_im]
  rw [e1, e2, hre]
  simp

/-! ## §2.5 投影切向量的代数层（A = ∂ₓP 的约束结构）

切向量的**分析构造**（投影族 P(k) 对参数的可微性，cfc/特征系统对参数的
求导——Kato 微扰论层）属微积分基础设施，登记为开放（见 §3）。本层闭合其
**纯代数后件**：一旦切向量存在，幂等性 P² = P 与厄米性对参数求导所强制
的约束方程，以及 Berry 曲率对切向量结构的依赖方式。这些恒等式是 TKNN
推导中"只需带间矩阵元"论断的形式化依据。 -/

/-- **投影切向量的带内消没**（幂等微分的纯代数后件）：设 P² = P 且
    A = P·A + A·P（A 扮演投影族切向量 Ṗ——对等式族 P(t)² = P(t) 关于参数
    求导得一阶约束 Ṗ = P·Ṗ + Ṗ·P）。则带内分量双双消失：
    P·A·P = 0 且 (1−P)·A·(1−P) = 0——切向量必为带间形态
    A = P·A·Q + Q·A·P（Q = 1 − P）。
    证明核心：x = x + x ⟹ x = 0（加法消去律）。 -/
theorem projTangent_intraBand_zero {n : ℕ}
    (P A : Matrix (Fin n) (Fin n) ℂ)
    (hPP : P * P = P) (hA : A = P * A + A * P) :
    P * A * P = 0 ∧ (1 - P) * A * (1 - P) = 0 := by
  have h2 : P * A * P = P * A * P + P * A * P := by
    conv_lhs => rw [hA]
    simp only [mul_add, add_mul, mul_assoc]
    rw [hPP, ← mul_assoc P P (A * P), hPP]
  have hx : P * A * P = 0 := by
    have h3 := congrArg (· - P * A * P) h2
    rw [sub_self, add_sub_cancel_right] at h3
    exact h3.symm
  have hqp : (1 - P) * P = 0 := by
    rw [sub_mul, one_mul, hPP, sub_self]
  have hpq : P * (1 - P) = 0 := by
    rw [mul_sub, mul_one, hPP, sub_self]
  have h1 : (1 - P) * (P * A) * (1 - P) = 0 := by
    have hh : (1 - P) * (P * A) * (1 - P) = ((1 - P) * P) * (A * (1 - P)) := by
      noncomm_ring
    rw [hh, hqp, zero_mul]
  have h2' : (1 - P) * (A * P) * (1 - P) = 0 := by
    have hh : (1 - P) * (A * P) * (1 - P) = ((1 - P) * A) * (P * (1 - P)) := by
      noncomm_ring
    rw [hh, hpq, mul_zero]
  have hy : (1 - P) * A * (1 - P) = 0 := by
    rw [hA, mul_add, add_mul, h1, h2', add_zero]
  exact ⟨hx, hy⟩

/-- **带间化简定理**：对幂等投影 P（P² = P）与满足切向量约束
    （P·A·P = 0、P·B·P = 0——由 `projTangent_intraBand_zero` 从 Ṗ = PṖ + ṖP
    导出）的 A、B，Berry 曲率的迹核只依赖切向量的带间分量：
    Tr(P [A, B]) = Tr(P·A·Q·B − P·B·Q·A)，Q = 1 − P。
    物理意义：曲率对切向量的带内（规范/张成基选取）分量不敏感——Berry 曲率
    规范无关性的代数核心，也是 TKNN 推导中"只需带间矩阵元"论断的形式化依据。 -/
theorem trace_proj_commutator_interband {n : ℕ}
    (P A B : Matrix (Fin n) (Fin n) ℂ)
    (hPAP : P * A * P = 0) (hPBP : P * B * P = 0) :
    P * (A * B - B * A)
      = P * A * (1 - P) * B - P * B * (1 - P) * A := by
  have ha : P * A = P * A * (1 - P) := by
    have h1 : P * A * (1 - P) + P * A * P = P * A := by
      rw [← mul_add, sub_add_cancel, mul_one]
    rw [hPAP, add_zero] at h1
    exact h1.symm
  have hb : P * B = P * B * (1 - P) := by
    have h1 : P * B * (1 - P) + P * B * P = P * B := by
      rw [← mul_add, sub_add_cancel, mul_one]
    rw [hPBP, add_zero] at h1
    exact h1.symm
  rw [mul_sub, ← mul_assoc, ← mul_assoc, ← ha, ← hb]

/-- Berry 曲率的带间形式（`trace_proj_commutator_interband` 的曲率封装）：
    F = −i·Tr(P·A·Q·B − P·B·Q·A)——曲率密度只含带间（Q-）通道。 -/
theorem berryCurvature_interband {n : ℕ}
    (P A B : Matrix (Fin n) (Fin n) ℂ)
    (hPAP : P * A * P = 0) (hPBP : P * B * P = 0) :
    berryCurvature P A B
      = -Complex.I * (P * A * (1 - P) * B - P * B * (1 - P) * A).trace := by
  have h := trace_proj_commutator_interband P A B hPAP hPBP
  calc berryCurvature P A B
      = -Complex.I * (P * (A * B - B * A)).trace := rfl
    _ = -Complex.I * (P * A * (1 - P) * B - P * B * (1 - P) * A).trace := by rw [h]

/-- **双交换子形式**：同约束下 Berry 曲率的迹核满足
    Tr(P [[P,A],[P,B]]) = −Tr(P [A, B])——即 F = i·Tr(P [[P,∂ₓP],[P,∂ᵧP]])，
    文献中 Berry 曲率的等价标准形态（非阿贝尔玻恩-奥本海默/Kato 联络的
    自洽性恒等式）。证明：显式展开 + 幂等/约束 kill 链（noncomm_ring 负责
    分配律展开，重写链负责 P² = P、PAP = 0、PBP = 0 的关系消去）。 -/
theorem trace_proj_commutator_twoCommutator {n : ℕ}
    (P A B : Matrix (Fin n) (Fin n) ℂ)
    (hPP : P * P = P) (hPAP : P * A * P = 0) (hPBP : P * B * P = 0) :
    (P * ((P * A - A * P) * (P * B - B * P)
        - (P * B - B * P) * (P * A - A * P))).trace
      = -((P * (A * B - B * A)).trace) := by
  have e1 : (P * A - A * P) * (P * B - B * P)
      = (P * A * P * B - P * A * B * P) - (A * P * P * B - A * P * B * P) := by
    noncomm_ring
  have e2 : (P * B - B * P) * (P * A - A * P)
      = (P * B * P * A - P * B * A * P) - (B * P * P * A - B * P * A * P) := by
    noncomm_ring
  have k1 : P * (P * A * P * B) = 0 := by
    rw [(mul_assoc P (P * A * P) B).symm, hPAP, mul_zero, zero_mul]
  have k3 : P * (A * P * P * B) = 0 := by
    rw [mul_assoc (A * P) P B, (mul_assoc P (A * P) (P * B)).symm, ← mul_assoc P A P,
      hPAP, zero_mul]
  have k4 : P * (A * P * B * P) = 0 := by
    rw [mul_assoc (A * P) B P, (mul_assoc P (A * P) (B * P)).symm, ← mul_assoc P A P,
      hPAP, zero_mul]
  have k5 : P * (P * B * P * A) = 0 := by
    rw [(mul_assoc P (P * B * P) A).symm, hPBP, mul_zero, zero_mul]
  have k7 : P * (B * P * P * A) = 0 := by
    rw [mul_assoc (B * P) P A, (mul_assoc P (B * P) (P * A)).symm, ← mul_assoc P B P,
      hPBP, zero_mul]
  have k8 : P * (B * P * A * P) = 0 := by
    rw [mul_assoc (B * P) A P, (mul_assoc P (B * P) (A * P)).symm, ← mul_assoc P B P,
      hPBP, zero_mul]
  have s1 : P * (P * A * B * P) = P * A * B * P := by
    rw [mul_assoc (P * A) B P, (mul_assoc P (P * A) (B * P)).symm, ← mul_assoc P P A,
      hPP]
  have s2 : P * (P * B * A * P) = P * B * A * P := by
    rw [mul_assoc (P * B) A P, (mul_assoc P (P * B) (A * P)).symm, ← mul_assoc P P B,
      hPP]
  have hM : P * ((P * A - A * P) * (P * B - B * P)
        - (P * B - B * P) * (P * A - A * P))
      = -(P * A * B * P) + P * B * A * P := by
    rw [e1, e2]
    simp only [mul_sub]
    rw [k1, k3, k4, k5, k7, k8, s1, s2]
    noncomm_ring
  have t1 : (P * A * B * P).trace = (P * (A * B)).trace := by
    have h : P * A * B * P = (P * (A * B)) * P := by noncomm_ring
    rw [h, Matrix.trace_mul_comm, ← mul_assoc, hPP]
  have t3 : (P * B * A * P).trace = (P * (B * A)).trace := by
    have h : P * B * A * P = (P * (B * A)) * P := by noncomm_ring
    rw [h, Matrix.trace_mul_comm, ← mul_assoc, hPP]
  have tR : (P * (A * B - B * A)).trace
      = (P * (A * B)).trace - (P * (B * A)).trace := by
    rw [mul_sub, Matrix.trace_sub]
  rw [hM, Matrix.trace_add, Matrix.trace_neg, t1, t3, tR]
  noncomm_ring

/-! ## §2.6 规范不变性：Berry 曲率的酉共轭不变性（代数核心）

开放登记 §3 #5 的有限维代数落地。用本征矢量 $u$ 表示的 Berry 联络在规范变换
$u\mapsto e^{i\theta}u$（逐点相位）下不变的微积分版需微分形式恒等式；此处闭合其
**代数内核**——Berry 曲率只依赖投影子空间 $P$（而非本征态的基选取），具体化为：
对任何与参数无关的酉阵 $U$（$U^\dagger U=1$），稳定化共轭 $P\mapsto UPU^\dagger$、
$A\mapsto UAU^\dagger$、$B\mapsto UBU^\dagger$ 使曲率不变 $F(U P U^\dagger,UAU^\dagger,
UBU^\dagger)=F(P,A,B)$。注意曲率公式只含 $P$（规范不变对象）而非本征矢量本身，故
"规范无关"在此代数层即"对酉稳定化不变"。这是 TKNN 推导里"曲率（从而陈数）只依赖
占据带投影、与本征态相位选择无关"论断的形式化依据。 -/

/-- 酉共轭下矩阵积的整理：$UAU^\dagger\cdot UBU^\dagger=U(AB)U^\dagger$
    （用 $U^\dagger U=1$ 消去中间一对）。供主定理 `berryCurvature_unitary_conj`。 -/
theorem conj_mul_unitary {n : ℕ} (U A B : Matrix (Fin n) (Fin n) ℂ)
    (hU : Uᴴ * U = 1) : (U * A * Uᴴ) * (U * B * Uᴴ) = U * (A * B) * Uᴴ := by
  calc
    (U * A * Uᴴ) * (U * B * Uᴴ) = U * A * (Uᴴ * U) * B * Uᴴ := by noncomm_ring
    _ = U * A * (1 : Matrix (Fin n) (Fin n) ℂ) * B * Uᴴ := by rw [hU]
    _ = U * (A * B) * Uᴴ := by simp [mul_assoc]

/-- 酉共轭下矩阵的迹不变：$(U X U^\dagger).\mathrm{trace}=X.\mathrm{trace}$
    （迹循环性 $+U^\dagger U=1$）。 -/
theorem trace_conj_unitary {n : ℕ} (U X : Matrix (Fin n) (Fin n) ℂ)
    (hU : Uᴴ * U = 1) : (U * X * Uᴴ).trace = X.trace := by
  calc
    (U * X * Uᴴ).trace = (Uᴴ * (U * X)).trace := by
      rw [Matrix.trace_mul_comm]
    _ = ((Uᴴ * U) * X).trace := by rw [← mul_assoc]
    _ = X.trace := by rw [hU]; simp

/-- **G3 规范不变性（有限维代数核心）**：Berry 曲率在酉稳定化
    $(P,A,B)\mapsto(UPU^\dagger,UAU^\dagger,UBU^\dagger)$（$U^\dagger U=1$）下不变
    $F(UPU^\dagger,UAU^\dagger,UBU^\dagger)=F(P,A,B)$。曲率只依赖占据带投影 $P$
    （规范不变对象）而非本征态的基选取——这是陈数良定义的又一代数基础：即使本征
    矢量相位 $u\mapsto e^{i\theta}u$ 变化，投影 $P$ 不动，曲率密度不变。
    证明：`conj_mul_unitary` 化简乘积 + `trace_conj_unitary` 剥离酉共轭。 -/
theorem berryCurvature_unitary_conj {n : ℕ} (P A B U : Matrix (Fin n) (Fin n) ℂ)
    (hU : Uᴴ * U = 1) :
    berryCurvature (U * P * Uᴴ) (U * A * Uᴴ) (U * B * Uᴴ)
      = berryCurvature P A B := by
  -- 先展开内层差：差分 = U·(AB−BA)·U^\dagger
  have hM : (U * P * Uᴴ) * ((U * A * Uᴴ) * (U * B * Uᴴ)
        - (U * B * Uᴴ) * (U * A * Uᴴ))
      = U * (P * (A * B - B * A)) * Uᴴ := by
    have h1 := conj_mul_unitary U A B hU
    have h2 := conj_mul_unitary U B A hU
    calc
      (U * P * Uᴴ) * ((U * A * Uᴴ) * (U * B * Uᴴ) - (U * B * Uᴴ) * (U * A * Uᴴ))
          = (U * P * Uᴴ) * (U * (A * B) * Uᴴ - U * (B * A) * Uᴴ) := by rw [h1, h2]
      _ = (U * P * Uᴴ) * (U * (A * B - B * A) * Uᴴ) := by
          congr 1
          noncomm_ring
      _ = U * (P * (A * B - B * A)) * Uᴴ := conj_mul_unitary U P (A * B - B * A) hU
  calc
    berryCurvature (U * P * Uᴴ) (U * A * Uᴴ) (U * B * Uᴴ)
        = -Complex.I
            * ((U * P * Uᴴ) * ((U * A * Uᴴ) * (U * B * Uᴴ)
                - (U * B * Uᴴ) * (U * A * Uᴴ))).trace := rfl
    _ = -Complex.I * (U * (P * (A * B - B * A)) * Uᴴ).trace := by rw [hM]
    _ = -Complex.I * (P * (A * B - B * A)).trace := by
        rw [trace_conj_unitary U (P * (A * B - B * A)) hU]
    _ = berryCurvature P A B := rfl

/-- **规范无关的实值曲率（推论）**：酉稳定化后的曲率仍是实值的
    $(\mathrm{Im}\,F)(UPU^\dagger,UAU^\dagger,UBU^\dagger)=0$——规范变换不破坏
    陈数密度的可积实值性。由规范不变性 + 实值性两定理合成：不变性把目标归为
    原曲率的实值性，实值性在原厄米前提下降 0。 -/
theorem berryCurvature_unitary_conj_im_eq_zero {n : ℕ}
    (P A B U : Matrix (Fin n) (Fin n) ℂ)
    (hU : Uᴴ * U = 1) (hP : P = Pᴴ) (hA : A = Aᴴ) (hB : B = Bᴴ) :
    (berryCurvature (U * P * Uᴴ) (U * A * Uᴴ) (U * B * Uᴴ)).im = 0 := by
  rw [berryCurvature_unitary_conj P A B U hU]
  exact berryCurvature_im_eq_zero P A B hP hA hB

/-! ## §2.7 陈数被积函数的 2-形式结构（积分定义的代数前提）

开放登记 §3 #1 的代数前提。第一陈数 $C=(1/2\pi)\int_{T^2}F\,d^2k$ 的**良定义**
在代数层要求被积函数是切向量 $(\partial_x,\partial_y)$ 上的**实值反对称双线性
2-形式**：实值性（§2 已闭合）、反对称（本层）、双线性（本层），且只依赖切向量
的**带间分量**（带内平移不贡献，本层；切向量本身的带内分量消没由 §2.5 闭合）。
这三条是被积函数"可作 2-形式积分"（$d^2k=dk_x\wedge dk_y$ 反对称）的代数刻画；
环面积分本身（MeasureTheory + 流形积分）与切向量的分析可微性仍登记开放。 -/

/-- **与投影交换的算子不贡献曲率迹核**：$[P,X]=0\Rightarrow\mathrm{Tr}(P[X,B])=0$。
    证明：迹循环性绕环 + $PX=XP$ 换序，两个循环迹相等，差为 0。 -/
theorem trace_comm_commutator_zero {n : ℕ}
    (P X B : Matrix (Fin n) (Fin n) ℂ)
    (hPX : P * X = X * P) :
    (P * (X * B - B * X)).trace = 0 := by
  have htr : (P * (X * B)).trace = (P * (B * X)).trace := by
    calc
      (P * (X * B)).trace = ((X * B) * P).trace := by rw [Matrix.trace_mul_comm]
      _ = (X * (B * P)).trace := by rw [← mul_assoc]
      _ = ((B * P) * X).trace := by rw [Matrix.trace_mul_comm]
      _ = (B * (P * X)).trace := by rw [← mul_assoc]
      _ = (B * (X * P)).trace := by rw [hPX]
      _ = ((X * P) * B).trace := by rw [Matrix.trace_mul_comm]
      _ = (X * (P * B)).trace := by rw [← mul_assoc]
      _ = (P * (B * X)).trace := by rw [Matrix.trace_mul_comm, ← mul_assoc]
  rw [mul_sub, Matrix.trace_sub, htr, sub_self]

/-- **Berry 曲率的反对称性（2-形式结构核心）**：
    $F(P,B,A)=-F(P,A,B)$——交换切向量方向即变号 $F_{xy}=-F_{yx}$。
    这是陈数 $C=(1/2\pi)\int F\,d^2k$ 作为**2-形式积分**（$d^2k=dk_x\wedge dk_y$
    反对称）而非普通函数积分的代数基础：与被积函数实值性（§2）合起来，
    F 是切向量上的**实值反对称 2-形式**。证明：[B,A]=−[A,B] + 迹/标量线性。 -/
theorem berryCurvature_antisymm {n : ℕ}
    (P A B : Matrix (Fin n) (Fin n) ℂ) :
    berryCurvature P B A = -berryCurvature P A B := by
  unfold berryCurvature
  have hcomm : B * A - A * B = -(A * B - B * A) := by
    noncomm_ring
  rw [hcomm]
  simp only [Matrix.mul_neg, Matrix.trace_neg]
  ring

/-- **Berry 曲率对第一个切向量的双线性（左线性）**：
    $F(P,A+X,B)=F(P,A,B)+F(P,X,B)$——2-形式是切向量上的双线性型。
    证明：[A+X,B]=[A,B]+[X,B] + 迹/标量线性。 -/
theorem berryCurvature_add_left {n : ℕ}
    (P A X B : Matrix (Fin n) (Fin n) ℂ) :
    berryCurvature P (A + X) B = berryCurvature P A B + berryCurvature P X B := by
  unfold berryCurvature
  have hcomm : (A + X) * B - B * (A + X)
      = (A * B - B * A) + (X * B - B * X) := by
    noncomm_ring
  rw [hcomm]
  rw [Matrix.mul_add, Matrix.trace_add]
  ring

/-- **Berry 曲率对第二个切向量的双线性（右线性）**：
    $F(P,A,B+X)=F(P,A,B)+F(P,A,X)$。与左线性 + 反对称一致
    （右线性可由左线性与反对称推出）。 -/
theorem berryCurvature_add_right {n : ℕ}
    (P A B X : Matrix (Fin n) (Fin n) ℂ) :
    berryCurvature P A (B + X) = berryCurvature P A B + berryCurvature P A X := by
  unfold berryCurvature
  have hcomm : A * (B + X) - (B + X) * A
      = (A * B - B * A) + (A * X - X * A) := by
    noncomm_ring
  rw [hcomm]
  rw [Matrix.mul_add, Matrix.trace_add]
  ring

/-- **带内平移不改变 Berry 曲率（规范类不变）**：若 $X$ 与投影 $P$ 交换
    $[P,X]=0$（带内算子），则 $F(P,A+X,B)=F(P,A,B)$——曲率只依赖切向量的
    **带间分量**。与 §2.5（切向量本身是带间的）互补："TKNN 只需带间矩阵元"
    论断的完整形式：切向量带内分量消没，且额外加入带内分量也不贡献。
    证明：左线性拆分 + $[P,X]=0\Rightarrow\mathrm{Tr}(P[X,B])=0$
    （`trace_comm_commutator_zero`）。 -/
theorem berryCurvature_shift_commute {n : ℕ}
    (P A X B : Matrix (Fin n) (Fin n) ℂ)
    (hPX : P * X = X * P) :
    berryCurvature P (A + X) B = berryCurvature P A B := by
  rw [berryCurvature_add_left]
  have hz : berryCurvature P X B = 0 := by
    unfold berryCurvature
    have htr := trace_comm_commutator_zero P X B hPX
    rw [htr]
    simp
  rw [hz, add_zero]

/-- **常数平移不改变 Berry 曲率（特例）**：$F(P,A+c\cdot 1,B)=F(P,A,B)$——
    Berry 联络的加法纯规范（常数平移）在曲率中消没（$F=dA$ 只看 $d$ 的部分）。
    由带内平移不变性 + $[P,c\cdot 1]=0$（标量阵与一切矩阵交换）即得。 -/
theorem berryCurvature_shift_const {n : ℕ}
    (P A B : Matrix (Fin n) (Fin n) ℂ) (c : ℂ) :
    berryCurvature P (A + c • 1) B = berryCurvature P A B := by
  apply berryCurvature_shift_commute
  calc
    P * (c • 1) = c • P := by rw [Matrix.mul_smul, Matrix.mul_one]
    _ = (c • 1) * P := by rw [Matrix.smul_mul, Matrix.one_mul]

/-! ## §2.8 陈数整性的代数种子：占据数 = 秩 ∈ ℤ 与相似守恒（命题 3.1 代数层）

开放登记 §3 #2（整性 Ch ∈ ℤ）与命题 3.1（陈数绝热不变性）的**代数种子**。
陈数的整性在物理上最终归结为**占据带的整值占据数**：占据带谱投影 P 的迹
（占据数）等于其秩（占据带维数/Landau 能级数）——整数。本层闭合：

  1. **幂等阵迹 = 秩 ∈ ℤ**（`trace_eq_rank_of_idempotent`）：对任意幂等阵
     P（P² = P，谱投影正是幂等阵），Tr P = rank P ∈ ℤ。证明路径：
     P.toLin' 幂等 → `IsIdempotentElem.isProj_range`（到值域的投影）→
     `IsProj.trace`（幂等线性映射迹 = 值域维数）→
     `Matrix.trace_toLin'_eq`/`Matrix.rank_eq_finrank_range_toLin` 桥接
     （线性映射迹/值域维数 ↔ 矩阵迹/秩）。
  2. **共轭保持幂等 + 秩守恒**（`idempotent_conj_inv`/`rank_conj_inv_idempotent`）：
     谱投影沿相似变换（谱流/绝热演化的代数形式，P ↦ U P U⁻¹）保持幂等且秩
     不变——占据数沿绝热形变守恒。这是命题 3.1（陈数绝热不变性）与 §3 #4
     的代数层：绝热演化下占据数（秩）保持整数不变。

诚实边界：闭合的是**占据数的整性与相似守恒**（有限维代数层）；完整陈数
Ch = (1/2π)∫F d²k 的整性（度理论/同伦）与环面绝热演化（同伦不变性）仍
登记开放，需连续场论/同伦基础设施。 -/

/-- **幂等阵迹 = 秩 ∈ ℤ（整性代数种子）**：对幂等阵 P（P² = P，谱投影
    正是幂等阵），Tr P = rank P ∈ ℤ——占据带投影的迹（占据数）等于占据带
    维数（秩）的整数代数根源（陈数整性的代数种子）。
    证明：P.toLin' 幂等 → `IsIdempotentElem.isProj_range` → `IsProj.trace`
    （幂等线性映射迹 = 值域维数）→ `trace_toLin'_eq`/`rank_eq_finrank_range_toLin`
    桥接（线性映射迹/值域维数 ↔ 矩阵迹/秩）。 -/
theorem trace_eq_rank_of_idempotent {n : ℕ} (P : Matrix (Fin n) (Fin n) ℂ)
    (hPP : P * P = P) :
    P.trace = (P.rank : ℂ) := by
  classical
  have hidem : IsIdempotentElem P.toLin' := by
    rw [IsIdempotentElem]
    change (toLin' P).comp (toLin' P) = toLin' P
    rw [← Matrix.toLin'_mul P P]
    rw [hPP]
  have htr : LinearMap.trace ℂ (Fin n → ℂ) P.toLin'
      = (Module.finrank ℂ (LinearMap.range P.toLin') : ℂ) := by
    exact (LinearMap.isProj_range_iff_isIdempotentElem P.toLin').2 hidem |>.trace
  rw [Matrix.trace_toLin'_eq] at htr
  have hrank : P.rank = Module.finrank ℂ (LinearMap.range P.toLin') := by
    rw [Matrix.rank_eq_finrank_range_toLin P (Pi.basisFun ℂ (Fin n))
      (Pi.basisFun ℂ (Fin n))]
    rw [Matrix.toLin_eq_toLin']
  rw [← hrank] at htr
  exact htr

/-- **共轭保持幂等**：U⁻¹·U = 1 时 U·P·U⁻¹ 保持幂等
    （P² = P ⇒ (U·P·U⁻¹)² = U·P·U⁻¹）——谱投影沿相似变换（共轭消去中间对
    U⁻¹·U）仍是谱投影。 -/
theorem idempotent_conj_inv {n : ℕ} (U P : Matrix (Fin n) (Fin n) ℂ)
    (hPP : P * P = P) (hUU' : U⁻¹ * U = 1) :
    (U * P * U⁻¹) * (U * P * U⁻¹) = U * P * U⁻¹ := by
  calc
    (U * P * U⁻¹) * (U * P * U⁻¹) = U * P * (U⁻¹ * U) * P * U⁻¹ := by noncomm_ring
    _ = U * P * P * U⁻¹ := by rw [hUU']; simp
    _ = U * P * U⁻¹ := by rw [mul_assoc U P P, hPP]

/-- **占据数（秩）沿相似变换守恒（绝热不变性代数种子）**：谱投影 P 沿
    相似变换 P ↦ U·P·U⁻¹（谱流/绝热演化的代数形式）保持幂等且秩不变
    （占据数 = 秩 ∈ ℤ 守恒）。命题 3.1（陈数绝热不变性）的代数层：
    绝热形变（谱分离保持）下占据数保持整数不变。
    证明：`idempotent_conj_inv`（幂等保持）+ `trace_pow_similar`（k = 1，
    相似迹不变）+ `trace_eq_rank_of_idempotent`（秩 = 迹）。 -/
theorem rank_conj_inv_idempotent {n : ℕ} (U P : Matrix (Fin n) (Fin n) ℂ)
    (hPP : P * P = P) (hUU : U * U⁻¹ = 1) (hUU' : U⁻¹ * U = 1) :
    (U * P * U⁻¹).rank = P.rank := by
  have hPP' : (U * P * U⁻¹) * (U * P * U⁻¹) = U * P * U⁻¹ :=
    idempotent_conj_inv U P hPP hUU'
  have hc : ((U * P * U⁻¹).rank : ℂ) = (P.rank : ℂ) := by
    calc
      ((U * P * U⁻¹).rank : ℂ) = (U * P * U⁻¹).trace := by
        exact (trace_eq_rank_of_idempotent (U * P * U⁻¹) hPP').symm
      _ = P.trace := by
        simpa using trace_pow_similar P U⁻¹ U hUU' hUU 1
      _ = (P.rank : ℂ) := by exact trace_eq_rank_of_idempotent P hPP
  exact_mod_cast hc

/-! ## §2.9 离散 S¹ 绕行的代数底胞：占据-空带互补守恒（同伦层首个基建模块）

开放项 §3 #1/#2/#4（环面积分、度理论整性、同伦不变）在 §2.8 后明确收敛到
连续场论/同伦层，需环面积分 + 同伦提升大型基建。开启同伦层前，本层先闭合其
**离散 S¹ 绕行的代数底胞**——占据带与空带的**互补守恒**：

  1. **补投影仍幂等**（`complement_idempotent`）：占据带投影 P 的补投影
     Q = 1 − P（空带/导带的谱投影）仍为幂等——占据与空两带各由幂等阵刻画。
  2. **占据数 + 空数 = 总带数 n**（`rank_add_complement_idempotent`）：
     rank P + rank(1−P) = n ∈ ℤ。这是"陈数扰动能在占据/空带间转移但**总量
     守恒**"的秩论细胞：参数沿闭回（S¹）绕行、能带交叉、占据数在带间跳变时，
     任何时刻占据数（秩）仍是整数，且与空秩相加恒为总带数。
  3. **补秩**（`complement_rank`）：rank(1−P) = n − rank P。

**证明要点**：复用 `trace_eq_rank_of_idempotent`（幂等阵迹 = 秩）+ 矩阵迹线性
平凡 $\mathrm{Tr}(1-P)=n-\mathrm{Tr}\,P$（$P+(1-P)=1$），零 sorry，且**无需
子空间直和/秩-零度基础设施**。

**诚实边界**：本层给出离散绕行的**总荷守恒**与**整值占据数**的代数细胞；连续
绕行的陈数积分、度理论整性（同秩投影酉等价 → K₀(ℂ) → 陈指数）与同伦不变性
仍登记开放（§3 #1/#2/#4），属后续同伦层基建。 -/

/-- **补投影幂等**：占据带投影 P（P² = P）的补投影 1 − P 仍幂等
    （(1−P)² = 1−P）——空带/导带与占据带同由幂等阵刻画（谱分离的两侧各是投影）。 -/
theorem complement_idempotent {n : ℕ} (P : Matrix (Fin n) (Fin n) ℂ)
    (hPP : P * P = P) :
    (1 - P) * (1 - P) = 1 - P := by
  calc
    (1 - P) * (1 - P) = 1 - P - P + P * P := by noncomm_ring
    _ = 1 - P := by rw [hPP]; noncomm_ring

/-- **占据数 + 空数 = 总带数 n，`S¹` 绕行的总荷守恒（代数底胞）**：幂等阵 P
    与其补 1−P 的秩相加恒为 n ∈ ℤ——占据数（rank P）与空数（rank(1−P)）之和
    等于总带数 n。这是陈数扰动在占据/空带间转移但总量守恒的秩论细胞：
    参数沿闭回绕行、能带交叉、占据数在带间跳变时，任何时刻占据数仍整数且与空秩
    相加恒为总带数。
    证明：`complement_idempotent`（补投影幂等）+ `trace_eq_rank_of_idempotent`
    （幂等阵迹=秩）+ 矩阵迹线性平凡 $\mathrm{Tr}(P+(1-P))=\mathrm{Tr}\,1=n$，
    经 `exact_mod_cast` 落回 ℤ。 -/
theorem rank_add_complement_idempotent {n : ℕ} (P : Matrix (Fin n) (Fin n) ℂ)
    (hPP : P * P = P) :
    P.rank + (1 - P).rank = n := by
  have hQ : (1 - P) * (1 - P) = 1 - P := complement_idempotent P hPP
  have hPc : (P.rank : ℂ) = P.trace := (trace_eq_rank_of_idempotent P hPP).symm
  have hQc : (((1 - P).rank : ℕ) : ℂ) = (1 - P).trace :=
    (trace_eq_rank_of_idempotent (1 - P) hQ).symm
  have hT : P.trace + (1 - P).trace = (n : ℂ) := by
    calc
      P.trace + (1 - P).trace = (P + (1 - P)).trace := by rw [Matrix.trace_add]
      _ = (1 : Matrix (Fin n) (Fin n) ℂ).trace := by congr 1; noncomm_ring
      _ = (n : ℂ) := by simp
  have hc : ((P.rank + (1 - P).rank : ℕ) : ℂ) = (n : ℂ) := by
    rw [Nat.cast_add, hPc, hQc, hT]
  exact_mod_cast hc

/-- **补秩**：空带数 = 总带数 − 占据数，rank(1−P) = n − rank P
    （占据/空互补守恒的减法形式，可由加和形式 `rank_add_complement_idempotent`
    经 `Nat.eq_sub_of_add_eq` 直接推出）。 -/
theorem complement_rank {n : ℕ} (P : Matrix (Fin n) (Fin n) ℂ)
    (hPP : P * P = P) :
    (1 - P).rank = n - P.rank := by
  have hadd := rank_add_complement_idempotent P hPP
  rw [add_comm] at hadd
  exact Nat.eq_sub_of_add_eq hadd

/-! ## §2.10 连续 S¹ 与环面绕行的陈数积分：环绕数孢子（积分/度理论层首块）

§2.8/§2.9 在有限维代数层闭合了占据数整性（秩∈ℤ）与离散 S¹ 总荷守恒。本层跨入
**连续积分/度理论层**：陈数整性 $C\in\mathbb{Z}$ 的物理根源之一是**环绕数取整值**
（恒等映射 $S^1\to S^1$ 的度 = 1）。最小真证孢子是单位圆留数积分
$\oint_{|z|=1} z^{-1}\,dz = 2\pi i$——`circleIntegral.integral_sub_center_inv`
（中心 0、半径 1：$(z-0)^{-1}=z^{-1}$）。归一化
$(2\pi i)^{-1}\oint z^{-1}\,dz = 1\in\mathbb{Z}$。本层闭合连续 S¹ 的环绕数孢子，
并建立环面 $T^2\subset\mathbb{C}^2$ 上陈数被积的积分形式（定义层，`torusIntegral`）。

**诚实边界**：闭合的是**连续 S¹ 恒等映射的度/环绕数 = 1 ∈ ℤ**（留数积分孢子，
衔接离散 §2.9");环面 $T^2$ 上的第一陈数 $C=(1/2\pi)\int F\,d^2k$ 的**完整整性**
（同秩投影酉等价 → $K_0(\mathbb{C})\cong\mathbb{Z}$ → 陈指数）与 TKNN 场论形式
仍登记开放，属后续同伦层/度理论基建。 -/

/-- **单位圆留数孢子（连续 S¹ 环绕数 = 1 的积分根）**：$\oint_{|z|=1} z^{-1}dz =
    2\pi i$——单位圆周上 $1/z$ 的环路积分等于 $2\pi i$（`circleIntegral.
    integral_sub_center_inv`，中心 0、半径 1：$(z-0)^{-1}=z^{-1}$）。这是环绕数
    /度理论所取整值 $1\in\mathbb{Z}$ 在连续积分层的最小孢子。 -/
theorem unitCircle_integral_inv :
    (∮ z in C(0, 1), (z : ℂ)⁻¹) = 2 * Real.pi * Complex.I := by
  simpa using (circleIntegral.integral_sub_center_inv (0 : ℂ) (by norm_num : (1 : ℝ) ≠ 0))

/-- **归一化环绕数 = 1 ∈ ℤ（连续 S¹ 陈数整性孢子）**：$(2\pi i)^{-1}$ 归一化的
    单位圆留数积分等于 $1$——恒等映射 $z\mapsto z$（$S^1\to S^1$）的度/环绕数取
    整值 $1$。这是陈数整性 $C\in\mathbb{Z}$ 在连续 S¹ 层的第一块真证基石（度理论
    整值 $=1$ 的最简实例），连接离散 §2.9（总荷守恒）与环面的整性。
    证明：`unitCircle_integral_inv` + `inv_mul_cancel₀`（归一化因子非零，因
    $2,\pi,\mathrm{i}$ 均非零）。 -/
theorem unitCircle_windingNumber_eq_one :
    ((2 * Real.pi * Complex.I : ℂ)⁻¹) * (∮ z in C(0, 1), (z : ℂ)⁻¹) = 1 := by
  rw [unitCircle_integral_inv]
  have hzn : (2 * Real.pi * Complex.I : ℂ) ≠ 0 := by
    exact mul_ne_zero
      (mul_ne_zero (by norm_num : (2 : ℂ) ≠ 0) (by exact_mod_cast Real.pi_ne_zero))
      Complex.I_ne_zero
  exact inv_mul_cancel₀ hzn

/-- **环面 $T^2\subset\mathbb{C}^2$ 的陈数被积积分形式（定义层）**：对
    ℂ² → ℂ 的曲率密度被积 $F$，在标准环面 $T^2=\{z\,|\,\forall i,\,|z_i|=1\}$
    上的未归一化围道积分 $\iint_{T^2}F\,d^2z$（`torusIntegral`：中心 0、半径 1，
    ℂ² 参数 $\theta\in[0,2\pi]^2$）。仅供定义留档（§3 #1 环面积分的承载形式）；
    完整归一化陈数与整性仍开放，见诚实边界。 -/
noncomputable def chernIntegralTorus (F : (Fin 2 → ℂ) → ℂ) : ℂ :=
  ∯ z in T((0 : Fin 2 → ℂ), fun _ : Fin 2 => (1 : ℝ)), F z

/-! ## §2.11 同秩幂等投影的迹类一致与互补类对称：K₀ 秩定类的迹同态种子

§3 #7「同秩投影酉等价（K₀ = ℤ 度理论整性核心）」的完整论证需完整酉群
U(n)/同伦与 K₀ 表示论（等距等价 `LinearIsometryEquiv`、子空间直和
`prodEquivOfIsCompl` 等大型基建），本项目之纪律是**只闭合真实可达内容、
不作伪证**，故完整酉等价保持开放登记。但 K₀(ℂ)≅ℤ 的**秩定类性质**有一块
完全在现有代数工具内的真实种子：**迹同态**——K₀ 到 ℤ 的显式同构由
$\mathrm{Tr}$（$K_0(\mathbb{C})\ni[\mathbb{C}^r]\mapsto r\in\mathbb{Z}$）
实现，故**同秩幂等投影必然同迹 ∈ ℤ**（迹类一致），且其补投影亦同秩
（互补类对称）。此为「秩唯一决定 K₀ 类」的**迹特征**与**补/空对偶**在
有限维矩阵层的代数细胞，衔接 §2.8（迹=秩）与 §2.9（补秩互补）。

**诚实边界**：闭合的是同秩 ⇒ 同迹（秩决定迹类）与同秩 ⇒ 补同秩的
**可交换性/类一致性**种子；真正的**酉等价构造**（∃ 酉 U，Q=U·P·U†）与
**相似共轭构造**（∃ 可逆 S，Q=S·P·S⁻¹）仍登记开放（§3 #7），需完整
等距/酉群/K₀ 基建。 -/

/-- **同秩幂等投影迹类一致（K₀ 秩定类的迹同态种子）**：两个同秩（同维）
    幂等投影 P、Q（rank P = rank Q）有相等迹 $\mathrm{Tr}\,P=\mathrm{Tr}\,Q\in\mathbb{Z}$
    ——占据带投影的迹（占据数）只由秩（占据带维数）决定，与具体谱投影无关。
    这是 $K_0(\mathbb{C})\cong\mathbb{Z}$（由同态 $\mathrm{Tr}:K_0\to\mathbb{Z}$ 显式
    实现"秩定类"）在有限维矩阵层的代数细胞：同 $\mathbb{Z}$ 迹类的投影共享同一整数迹类。
    证明：两边各自 `trace_eq_rank_of_idempotent`（幂等阵迹=秩）+ 秩相等 + ℂ 转换。 -/
theorem trace_eq_of_rank_eq_idempotent {n : ℕ} (P Q : Matrix (Fin n) (Fin n) ℂ)
    (hPP : P * P = P) (hQQ : Q * Q = Q) (hran : P.rank = Q.rank) :
    P.trace = Q.trace := by
  calc
    P.trace = (P.rank : ℂ) := trace_eq_rank_of_idempotent P hPP
    _ = (Q.rank : ℂ) := by exact congrArg (fun k : ℕ => (k : ℂ)) hran
    _ = Q.trace := (trace_eq_rank_of_idempotent Q hQQ).symm

/-- **同秩幂等投影互补类对称（占据-空带对偶种子）**：两个同秩幂等投影
    P、Q（rank P = rank Q）的补投影亦同秩
    $\mathrm{rank}(1-P)=\mathrm{rank}(1-Q)$——空带的"空数"只由占据带的维数
    （秩）决定，占据侧与空带侧构成对称的秩类。这是 §2.9 补秩
    （`complement_rank`）沿相等秩的传递，强化「秩唯一决定占据/空带的
    互补类」的 K₀ 对称结构。
    证明：两侧各自 `complement_rank`（补秩 = n − rank）+ 秩相等。 -/
theorem complement_rank_eq_of_rank_eq {n : ℕ} (P Q : Matrix (Fin n) (Fin n) ℂ)
    (hPP : P * P = P) (hQQ : Q * Q = Q) (hran : P.rank = Q.rank) :
    (1 - P).rank = (1 - Q).rank := by
  calc
    (1 - P).rank = n - P.rank := complement_rank P hPP
    _ = n - Q.rank := by exact congrArg (fun k : ℕ => n - k) hran
    _ = (1 - Q).rank := (complement_rank Q hQQ).symm

/-! ## §2.12 环面 $T^2$ 的陈数被积绕行：一维环面切入（环面环绕数孢子的退化面）

§3 #1 的环面积分定义层有了 §2.10 的 `chernIntegralTorus`（双参数承载）。
将 §2.10 的单位圆环绕数孢子（$\oint_{|z|=1}z^{-1}dz=2\pi i$ → 整值 1）推广到
环面，最真实可达的第一块是**一维退化环面**：环面 $T^2\subset\mathbb{C}^2$ 在
$n=1$（单参数）时的切面恰为圆周 $S^1$。mathlib 的 `torusIntegral_dim1` 证得
**一维环面积分 = 圆周积分**（$T$ 单参数与 $C(c_0,R_0)$ 等价），故 §2.10 的
留数孢子与整值 $1\in\mathbb{Z}$ 可直接继承到环面——这是环面陈数被积绕行的
**第一块绕行整值孢子**：环面退化的留数归一化后仍取整值 1。

**诚实边界**：闭合的是**一维退化环面**的环绕数整值（$T^1$ 侧），二维 $T^2$
被积 $F$ 的完整归一化陈数与整性、以及可积性（⇐ $P$ 光滑）仍登记开放（§3 #1）。 -/

/-- **一维退化环面留数孢子 = 单位圆留数（环面环绕数的退化种子）**：
    $1$-参数环面 $T\subset\mathbb{C}$（中心 0、半径 1，参数 $\theta\in[0,2\pi]$）
    上被积 $1/z_0$ 的积分等于单位圆留数 $\oint_{|z|=1}z^{-1}dz=2\pi i$。
    证明：`torusIntegral_dim1` 一维环面 = 圆周积分，经 `unitCircle_integral_inv`
    （§2.10）落定。 -/
theorem torusIntegral_dim1_winding :
    (∯ z in T((0 : Fin 1 → ℂ), fun _ : Fin 1 => (1 : ℝ)), (z 0)⁻¹) =
      2 * Real.pi * Complex.I := by
  rw [torusIntegral_dim1 (fun z : Fin 1 → ℂ => (z 0)⁻¹)
      (0 : Fin 1 → ℂ) (fun _ : Fin 1 => (1 : ℝ))]
  simpa using unitCircle_integral_inv

/-- **一维退化环面归一化环绕数 = 1 ∈ ℤ（环面绕行整值孢子，退化面）**：
    $(2\pi i)^{-1}$ 归一化的 $1$-参数环面 $1/z_0$ 留数积分等于 $1$——环面在
    一维退化的切面（圆周 $S^1$）上，恒等映射的度/环绕数仍取整值 $1\in\mathbb{Z}$。
    这是 §2.10 环绕数整值向**环面**转移的第一块真证基石（$T^1$ 分子 ⊂ $T^2$
    变形），为二维环面整性陈数提供一维退化边界条件。
    证明：`torusIntegral_dim1_winding` + `inv_mul_cancel₀`。 -/
theorem torusIntegral_dim1_windingNumber_eq_one :
    ((2 * Real.pi * Complex.I : ℂ)⁻¹) *
        (∯ z in T((0 : Fin 1 → ℂ), fun _ : Fin 1 => (1 : ℝ)), (z 0)⁻¹) = 1 := by
  rw [torusIntegral_dim1_winding]
  have hzn : (2 * Real.pi * Complex.I : ℂ) ≠ 0 := by
    exact mul_ne_zero
      (mul_ne_zero (by norm_num : (2 : ℂ) ≠ 0) (by exact_mod_cast Real.pi_ne_zero))
      Complex.I_ne_zero
  exact inv_mul_cancel₀ hzn

/-! ## §2.13 环面 $T^2$ 陈数被积绕行：二维双留数整值孢子（2D 环面双留数）

§2.12 闭合了环面绕行整值的 $T^1$ 退化面。本层推进到完整二维环面
$T^2\subset\mathbb{C}^2$：对**双极点被积 $z_0^{-1}z_1^{-1}$** 的二维围道积分
$\iint_{T^2} z_0^{-1}z_1^{-1}\,d^2z$。按 `torusIntegral` 定义（参数立方
$[0,2\pi]^2$ 的 Jacobi 因子 $\prod_i e^{\theta_i i}$，半径 1、中心 0），
Jacobi 因子与 $z_i^{-1}=e^{-\theta_i i}$ 在环面上**逐点消约**，被积函数在
立方上化为常数 $-1$，故 $\iint_{T^2}z_0^{-1}z_1^{-1}d^2z=-(2\pi)^2=(2\pi i)^2$。
归一化 $(2\pi i)^{-2}\iint_{T^2}=1\in\mathbb{Z}$——二维复面双极点的环形留数
整值，是环面第一陈数整性在连续积分层的核心种子（双极点留数 $(2\pi i)^2$
对偶度理论整值 $1$，衔接 §2.10/§2.12 的环绕数种子向二维环面的真正推移）。

**诚实边界**：闭合的是**双极点被积 $z_0^{-1}z_1^{-1}$** 的二维环面留数环值
（$=(2\pi i)^2$、归一化 $=1\in\mathbb{Z}$）。完整二维 $T^2$ 上一般被积陈数
密度 $F$ 的归一化陈数整性、$F$ 的实可积性/光滑性（$\Leftarrow P$ 光滑）仍
登记开放（§3 #1、#2），需完整度理论/同伦提升基建。 -/

/-- **二维环面双留数积分（$\mathbb{C}^2$ 上被积 $1/(z_0z_1)$）**：标准环面
    $T^2\subset\mathbb{C}^2$（中心 0、半径 1）上 $\iint_{T^2}z_0^{-1}z_1^{-1}
    d^2z=(2\pi i)^2$。证明：展开 `torusIntegral` 定义，参数立方 $[0,2\pi]^2$
    的 Jacobi 因子 $\prod_i e^{\theta_i i}$（`Fin.prod_univ_two`）与被积倒数
    $z_i^{-1}=e^{-\theta_i i}$ 逐点消约（`inv_mul_cancel`，`Complex.exp_ne_zero`）
    成常数 $-1$，对立方积分（`setIntegral_const`，$[0,2\pi]^2$ 体积
    `Real.volume_Icc_pi_toReal` 为 $(2\pi)^2$）得 $-(2\pi)^2=(2\pi i)^2$
    （$\mathrm{i}^2=-1$）。 -/
theorem torusIntegral_dim2_double_inv :
    (∯ z in T((0 : Fin 2 → ℂ), fun _ : Fin 2 => (1 : ℝ)),
        (z 0)⁻¹ * (z 1)⁻¹) =
      (2 * Real.pi * Complex.I) ^ 2 := by
  -- 参数立方上的完整被积（Jacobi × f∘torusMap）恒为常数 -1
  have hinteg : (fun θ : Fin 2 → ℝ =>
      (∏ i : Fin 2, ((fun _ : Fin 2 => (1 : ℝ)) i * exp (θ i * (Complex.I : ℂ)) * (Complex.I : ℂ)) : ℂ) •
        ((fun z : Fin 2 → ℂ => (z 0)⁻¹ * (z 1)⁻¹) (torusMap (0 : Fin 2 → ℂ) (fun _ : Fin 2 => (1 : ℝ)) θ)))
      = fun _ : Fin 2 → ℝ => (-1 : ℂ) := by
    funext θ
    -- Jacobi 因子与倒数消约（exp₂ᵢ 非零）
    simp only [Pi.zero_apply, torusMap, zero_add, Fin.prod_univ_two]
    -- 消约 $(e^{\theta_0 i}i)(e^{\theta_1 i}i)\cdot e^{-\theta_0 i}e^{-\theta_1 i}=-1$
    ring_nf
    field_simp [Complex.exp_ne_zero]
    simp
  rw [torusIntegral, hinteg]
  -- $\int_{[0,2\pi]^2}(-1)=-(2\pi)^2=(2\pi i)^2$
  rw [MeasureTheory.setIntegral_const (-1 : ℂ)]
  -- 立方体积 $[0,2\pi]^2$ 为 $(2\pi)^2$；$\mathrm{i}^2=-1$ 折叠成 $(2\pi i)^2$
  simp only [MeasureTheory.Measure.real]
  rw [Real.volume_Icc_pi_toReal (by intro i; positivity)]
  rw [Algebra.smul_def]
  ring_nf
  norm_num [pow_two, Complex.I_mul_I]
  ring

/-- **二维环面双留数归一化环绕数 = 1 ∈ ℤ（环面绕行整值孢子，二维面）**：
    $(2\pi i)^{-2}$ 归一化的二维环面双极点留数积分 $\iint_{T^2}z_0^{-1}z_1^{-1}
    d^2z$ 等于 $1$——二维复面 $T^2$ 上双极点的环形留数取整值 $1\in\mathbb{Z}$
    （度理论整值在二维环面的留数对偶实例）。这是 §2.12 $T^1$ 退化面向完整
    $T^2$ 的提升：环面陈数整性在连续积分层的**二维核心孢子**。
    证明：`torusIntegral_dim2_double_inv` + `pow_ne_zero` + `inv_mul_cancel₀`。 -/
theorem torusIntegral_dim2_windingNumber_eq_one :
    ((2 * Real.pi * Complex.I : ℂ) ^ 2)⁻¹ *
        (∯ z in T((0 : Fin 2 → ℂ), fun _ : Fin 2 => (1 : ℝ)),
            (z 0)⁻¹ * (z 1)⁻¹) = 1 := by
  rw [torusIntegral_dim2_double_inv]
  have hzn : (2 * Real.pi * Complex.I : ℂ) ^ 2 ≠ 0 := by
    exact pow_ne_zero 2 (mul_ne_zero
      (mul_ne_zero (by norm_num : (2 : ℂ) ≠ 0) (by exact_mod_cast Real.pi_ne_zero))
      Complex.I_ne_zero)
  exact inv_mul_cancel₀ hzn

/-! ## §2.14 同秩幂等投影的共轭构造：自伴正交分解与相似共轭（§3 #7 的投影对角化核心）

§3 #7「同秩投影酉等价（K₀ = ℤ 度理论整性核心）」的**投影对角化**代数核心。
谱投影恰为自伴幂等 P（P†=P、P²=P），本层在有限维复内积空间 $E$ 上：
(1) **自伴正交分解**——自伴幂等 P 满足 $\ker P=(\operatorname{range}P)^\perp$
    （自伴幂等 ⟺ 到其像的正交投影），这是「酉等价」的代数前提：共轭所依赖的
    分解 $E=\operatorname{range}P\oplus\ker P$ 在自伴时**正交**，故共轭可酉化；
(2) **相似共轭构造**——任意两个同秩幂等投影 P、Q（$\operatorname{rank}P=\operatorname{rank}Q$）
    由可逆线性变换 S 共轭（$\exists\,S,\,S\circ P=Q\circ S$），即 §3 #7 中
    「相似共轭构造（$\exists$ 可逆 S，$Q=S\cdot P\cdot S^{-1}$）」的有限维代数
    闭合——「秩唯一决定相似类」的显式重构。两者合起来是把谱投影在对角化意义
    下归一到同秩类，为陈数整性（$K_0(\mathbb{C})\to\mathbb{Z}$ 秩定类）提供
    **线性共轭支柱**。酉（等距）强化——把 S 升级为保内积的 `LinearIsometryEquiv`——
    需「同维子空间间等距等价 + 正交直和合成」基建，登记为诚实边界（见 §3 #7）。 -/

/-- **幂等映射在像上为恒等（对角形对角元 = 1）**：`IsIdempotentElem P` 时，
    P 作用于其像子空间任一向量为恒等 $P(a)=a$——谱投影在占据带上的占据行为。
    证明：$a=P\,y\Rightarrow P\,a=P^2y=P\,y=a$。 -/
lemma idempotent_apply_of_mem_range {R : Type*} [Semiring R] {E : Type*}
    [AddCommGroup E] [Module R E] (P : E →ₗ[R] E) (hidem : IsIdempotentElem P)
    (a : ↥(LinearMap.range P)) : P (a : E) = a := by
  rcases (LinearMap.mem_range.mp a.2) with ⟨y, hy⟩
  calc
    P (a : E) = P (P y) := by rw [hy]
    _ = (P * P) y := by rw [Module.End.mul_apply]
    _ = P y := by rw [hidem]
    _ = (a : E) := hy

/-- **幂等映射在核上为零（对角形对角元 = 0）**：`IsIdempotentElem P` 时，
    P 作用于其核子空间任一向量为零——谱投影在空带上的零占据。
    证明：核元定义 `LinearMap.mem_ker`。 -/
lemma idempotent_apply_mem_ker {R : Type*} [Semiring R] {E : Type*}
    [AddCommGroup E] [Module R E] (P : E →ₗ[R] E) (b : ↥(LinearMap.ker P)) :
    P (b : E) = 0 :=
  LinearMap.mem_ker.mp b.2

section OrthoDecomp

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]

/-- **自伴幂等投影的正交分解（ker = range 正交补）**：自伴（厄米）且幂等的
    线性映射 P 满足 $\ker P=(\operatorname{range}P)^\perp$——P 是到其像
    子空间的正交投影。这是「酉等价」的代数前提：相似共轭所依赖的分解
    $E=\operatorname{range}P\oplus\ker P$ 在自伴时正交，故共轭可酉化。
    证明：`IsSymmetric.orthogonal_range`（对称线性映射的像与核正交）。
    注：本引理仅需内积空间，不需要有限维假设，故置于 `FiniteDimensional`
    作用域之外。 -/
theorem selfAdjoint_idempotent_ker_eq_orthogonal (P : E →ₗ[ℂ] E)
    (hself : P.IsSymmetric) :
    LinearMap.ker P = (LinearMap.range P)ᗮ := by
  exact (LinearMap.IsSymmetric.orthogonal_range (T := P) hself).symm

end OrthoDecomp

section ProjConj

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
  [FiniteDimensional ℂ E]

/-- **同秩幂等投影的相似共轭构造（∃ 可逆 S，S∘P = Q∘S）**：两个同秩（像同维）
    幂等线性映射 P、Q 由可逆线性变换 S 共轭——「秩唯一决定相似类」的显式重构。
    证明：幂等给出 $E=\operatorname{range}\oplus\ker$ 直和分解
    （`IsIdempotentElem.isCompl` + `prodEquivOfIsCompl`）；同秩经 `finrank` 加性
    析出 $\operatorname{finrank}(\ker P)=\operatorname{finrank}(\ker Q)$
    （`Module.finrank_prod` + `LinearEquiv.finrank_eq` + `omega`）；range 与 ker
    各自同维给出 `LinearEquiv.ofFinrankEq`，用 `LinearEquiv.prod` 串成
    $S=e_Q\circ(\iota_R\times\iota_K)\circ e_P^{-1}$，逐坐标验证 $S\circ P=Q\circ S$
    （P 在 range 恒等、ker 为零，`idempotent_apply_of_mem_range`/`_mem_ker`）。
    这是 §3 #7「相似共轭构造（∃ 可逆 S，Q=S·P·S⁻¹）」的有限维代数闭合；酉（等距）
    强化需等距基建，登记开放。 -/
theorem similar_conj_projections_of_eq_finrank (P Q : E →ₗ[ℂ] E)
    (hPidem : IsIdempotentElem P) (hQidem : IsIdempotentElem Q)
    (hr : Module.finrank ℂ (LinearMap.range P) = Module.finrank ℂ (LinearMap.range Q)) :
    ∃ S : E ≃ₗ[ℂ] E, S.toLinearMap ∘ₗ P = Q ∘ₗ S.toLinearMap := by
  have hPcomp : IsCompl (LinearMap.range P) (LinearMap.ker P) :=
    LinearMap.IsIdempotentElem.isCompl (f := P) hPidem
  have hQcomp : IsCompl (LinearMap.range Q) (LinearMap.ker Q) :=
    LinearMap.IsIdempotentElem.isCompl (f := Q) hQidem
  let eP : (LinearMap.range P × LinearMap.ker P) ≃ₗ[ℂ] E :=
    Submodule.prodEquivOfIsCompl (LinearMap.range P) (LinearMap.ker P) hPcomp
  let eQ : (LinearMap.range Q × LinearMap.ker Q) ≃ₗ[ℂ] E :=
    Submodule.prodEquivOfIsCompl (LinearMap.range Q) (LinearMap.ker Q) hQcomp
  have hAP : Module.finrank ℂ (LinearMap.range P) + Module.finrank ℂ (LinearMap.ker P)
      = Module.finrank ℂ E := by
    calc
      Module.finrank ℂ (LinearMap.range P) + Module.finrank ℂ (LinearMap.ker P)
          = Module.finrank ℂ (LinearMap.range P × LinearMap.ker P) :=
            (Module.finrank_prod).symm
      _ = Module.finrank ℂ E := eP.finrank_eq
  have hAQ : Module.finrank ℂ (LinearMap.range Q) + Module.finrank ℂ (LinearMap.ker Q)
      = Module.finrank ℂ E := by
    calc
      Module.finrank ℂ (LinearMap.range Q) + Module.finrank ℂ (LinearMap.ker Q)
          = Module.finrank ℂ (LinearMap.range Q × LinearMap.ker Q) :=
            (Module.finrank_prod).symm
      _ = Module.finrank ℂ E := eQ.finrank_eq
  have hK : Module.finrank ℂ (LinearMap.ker P) = Module.finrank ℂ (LinearMap.ker Q) := by
    omega
  let isoR : LinearMap.range P ≃ₗ[ℂ] LinearMap.range Q :=
    LinearEquiv.ofFinrankEq (LinearMap.range P) (LinearMap.range Q) hr
  let isoK : LinearMap.ker P ≃ₗ[ℂ] LinearMap.ker Q :=
    LinearEquiv.ofFinrankEq (LinearMap.ker P) (LinearMap.ker Q) hK
  let S : E ≃ₗ[ℂ] E := eP.symm.trans ((isoR.prodCongr isoK).trans eQ)
  refine ⟨S, ?_⟩
  -- 逐坐标验证 S∘P = Q∘S：P 在 range 恒等、ker 为零，S 配对交换
  ext x
  rcases eP.surjective x with ⟨pa, rfl⟩
  rcases pa with ⟨a, b⟩
  change S.toLinearMap (P (eP (a, b))) = Q (S.toLinearMap (eP (a, b)))
  -- S 把 a∈rangeP 映到 isoR a，把 b∈kerP 映到 isoK b
  have hSa : S.toLinearMap (a : E) = (isoR a : E) := by
    change ((eP.symm.trans ((isoR.prodCongr isoK).trans eQ)) : E →ₗ[ℂ] E) (a : E) = (isoR a : E)
    simp [eP, eQ, LinearEquiv.prodCongr_apply, Submodule.coe_prodEquivOfIsCompl']
  have hSb : S.toLinearMap (b : E) = (isoK b : E) := by
    change ((eP.symm.trans ((isoR.prodCongr isoK).trans eQ)) : E →ₗ[ℂ] E) (b : E) = (isoK b : E)
    simp [eP, eQ, LinearEquiv.prodCongr_apply, Submodule.coe_prodEquivOfIsCompl']
  have hLP : P (eP (a, b)) = (a : E) := by
    calc
      P (eP (a, b)) = P ((a : E) + (b : E)) := by rw [Submodule.coe_prodEquivOfIsCompl']
      _ = P (a : E) + P (b : E) := by simp [LinearMap.map_add]
      _ = (a : E) := by
        rw [idempotent_apply_of_mem_range P hPidem a, idempotent_apply_mem_ker P b]
        simp
  have hR1 : Q (S.toLinearMap (eP (a, b))) = (isoR a : E) := by
    calc
      Q (S.toLinearMap (eP (a, b))) = Q (S.toLinearMap ((a : E) + (b : E))) := by
        rw [Submodule.coe_prodEquivOfIsCompl']
      _ = Q (S.toLinearMap (a : E) + S.toLinearMap (b : E)) := by rw [LinearMap.map_add]
      _ = Q ((isoR a : E) + (isoK b : E)) := by rw [hSa, hSb]
      _ = Q (isoR a : E) + Q (isoK b : E) := by simp [LinearMap.map_add]
      _ = (isoR a : E) := by
        rw [idempotent_apply_of_mem_range Q hQidem (isoR a),
            idempotent_apply_mem_ker Q (isoK b)]
        simp
  calc
    S.toLinearMap (P (eP (a, b))) = S.toLinearMap (a : E) := by rw [hLP]
    _ = (isoR a : E) := hSa
    _ = Q (S.toLinearMap (eP (a, b))) := hR1.symm

/-- **酉强化·引理 A：同维有限维子空间间存在等距等价**：同维（同 `finrank`）
    有限维内积子空间 $V,W\subset E$ 由保内积的等距等价连接（$V\simeq W$）。
    这是「酉等价」的支柱：酉 U 在占据带 $V=\operatorname{range}P$ 上的限制必须
    是保内积全射（等距等价），本引理保证 `range P ≅ᵢ range Q` 存在。
    证明：`stdOrthonormalBasis` 给出 $V,W$ 的标准正交基；同秩 h 经 `Equiv.cast`
    转换指标 `Fin (finrank ℂ V) ≃ Fin (finrank ℂ W)`，`OrthonormalBasis.equiv`
    沿指标等价建立等距等价。 -/
theorem exists_isometry_of_eq_finrank (V W : Submodule ℂ E)
    (h : Module.finrank ℂ V = Module.finrank ℂ W) : Nonempty (V ≃ₗᵢ[ℂ] W) := by
  let bV : OrthonormalBasis (Fin (Module.finrank ℂ V)) ℂ V := stdOrthonormalBasis ℂ V
  let bW : OrthonormalBasis (Fin (Module.finrank ℂ W)) ℂ W := stdOrthonormalBasis ℂ W
  let f : Fin (Module.finrank ℂ V) ≃ Fin (Module.finrank ℂ W) := Equiv.cast (congrArg Fin h)
  exact ⟨bV.equiv bW f⟩

/-- **酉强化·引理 B：把子空间等距等价延伸为全空间等距等价**：给定子空间
    等距等价 $e:S\simeq T$，将其延伸为全空间等距等价 $U:E\simeq E$——在 $S$ 上
    $U=e$，在正交补 $S^\perp$ 上 $U$ 映到 $T^\perp$（等距延伸的标准构造）。
    这就是把相似共轭 S 升级为酉（保内积）的构造核：`LinearIsometry.extend` 将
    $S\to T\subset E$ 的等距延伸为全空间等距映射，再以受限等距映到 $T^\perp$，
    配合 `toLinearIsometryEquiv`（有限维同维等距映射 ⟺ 等距等价）得全空间等价。 -/
noncomputable def linearIsometryEquiv_of_submodule (S T : Submodule ℂ E)
    (e : S ≃ₗᵢ[ℂ] T) : E ≃ₗᵢ[ℂ] E := by
  let L : S →ₗᵢ[ℂ] E := T.subtypeₗᵢ.comp e.toLinearIsometry
  have hfin : Module.finrank ℂ E = Module.finrank ℂ E := rfl
  exact (LinearIsometry.extend L).toLinearIsometryEquiv hfin

/-- **酉强化·引理 B 作用：U 在子空间 S 上等于 e**：全空间等距延伸 U（引理 B）
    作用在 $S$ 上即子空间等距 $e$（$U\circ\iota_S=\iota_T\circ e$）——酉共轭在
    占据带上的行为由同秩等距如实实现。
    证明：`LinearIsometry.extend_apply`（等距延伸在定义域上保持原映射）。 -/
theorem linearIsometryEquiv_of_submodule_apply (S T : Submodule ℂ E)
    (e : S ≃ₗᵢ[ℂ] T) (s : S) :
    (linearIsometryEquiv_of_submodule S T e : E → E) (s : E) = (e s : E) := by
  unfold linearIsometryEquiv_of_submodule
  simp [LinearIsometry.extend_apply]

/-- **酉强化·引理 C：U 把正交补 Sᗮ 映到 Tᗮ**：全空间等距延伸 U（引理 B）把任意
    与 $S$ 正交的向量 $b$ 映到与 $T$ 正交——空带 $S^\perp$ 被酉地映到空带
    $T^\perp$。这保证含 b 的核分量在共轭后仍落到核（零占据侧）上。
    证明：等距保内积 + e 满射覆盖 $T$，把 $t\in T$ 拉回 $s\in S$ 用正交性。 -/
theorem linearIsometryEquiv_of_submodule_mem_orthogonal (S T : Submodule ℂ E)
    (e : S ≃ₗᵢ[ℂ] T) {b : E} (hb : b ∈ Sᗮ) :
    linearIsometryEquiv_of_submodule S T e b ∈ Tᗮ := by
  rw [Submodule.mem_orthogonal']
  rintro t ht
  rcases e.surjective ⟨t, ht⟩ with ⟨s, hst⟩
  have hts : t = (e s : E) := by simp [hst]
  have hse : (linearIsometryEquiv_of_submodule S T e (s : E) : E) = (e s : E) :=
    linearIsometryEquiv_of_submodule_apply S T e s
  calc
    inner ℂ (linearIsometryEquiv_of_submodule S T e b) t
        = inner ℂ (linearIsometryEquiv_of_submodule S T e b) (e s : E) := by rw [hts]
    _ = inner ℂ (linearIsometryEquiv_of_submodule S T e b)
          (linearIsometryEquiv_of_submodule S T e (s : E)) := by rw [hse]
    _ = inner ℂ b (s : E) := by
        rw [LinearIsometryEquiv.inner_map_map (linearIsometryEquiv_of_submodule S T e) b (s : E)]
    _ = 0 := (Submodule.mem_orthogonal' S (b : E)).mp hb (s : E) s.property

/-- **主定理：同秩自伴幂等投影酉等价（Q = U∘P∘U⁻¹，U†=U⁻¹）**：有限维复内积
    空间中，任意两个同秩（同维像）自伴幂等（正交投影）谱投影 P、Q 酉等价——
    $\exists$ 保内积的 $U:E\simeq E$，$Q\circ U=U\circ P$（即 $Q=U\circ P\circ U^{-1}$，
    $U^\dagger=U^{-1}$）。这是 §3 #7「同秩投影酉等价（K₀=ℤ）」的**有限维代数闭合**：
    「秩唯一决定酉等价类」的显式酉构造，正是 $K_0(\mathbb{C})\cong\mathbb{Z}$（＾秩定
    类＾）的代数支柱。
    证明：自伴幂等使分解正交（引理 `selfAdjoint_idempotent_ker_eq_orthogonal`：
    `ker=(range)ᗮ`）；同秩经引理 A 给等距 $e:\operatorname{range}P\simeq\operatorname{range}Q$，
    引理 B 延伸为全空间等距 $U$（引理 B 作用 + 引理 C 分别落定 range/`ker` 分量）；
    在正交直和 $E=\operatorname{range}P\oplus\ker P$ 上逐段验证
    $Q\circ U=U\circ P$（P 在 range 恒等、ker 为零，`idempotent_apply_of_mem_range`/
    `_mem_ker`，Q 对 range/ker 同理）。 -/
theorem same_rank_selfAdjoint_idempotent_unitary_conj (P Q : E →ₗ[ℂ] E)
    (hPid : IsIdempotentElem P) (hPsa : P.IsSymmetric)
    (hQid : IsIdempotentElem Q) (hQsa : Q.IsSymmetric)
    (hr : Module.finrank ℂ (LinearMap.range P) = Module.finrank ℂ (LinearMap.range Q)) :
    ∃ U : E ≃ₗᵢ[ℂ] E, Q ∘ₗ U.toLinearMap = U.toLinearMap ∘ₗ P := by
  classical
  have hkerP : (LinearMap.range P)ᗮ = LinearMap.ker P :=
    (selfAdjoint_idempotent_ker_eq_orthogonal P hPsa).symm
  have hkerQ : (LinearMap.range Q)ᗮ = LinearMap.ker Q :=
    (selfAdjoint_idempotent_ker_eq_orthogonal Q hQsa).symm
  let e : LinearMap.range P ≃ₗᵢ[ℂ] LinearMap.range Q :=
    Classical.choice (exists_isometry_of_eq_finrank (LinearMap.range P) (LinearMap.range Q) hr)
  let U : E ≃ₗᵢ[ℂ] E := linearIsometryEquiv_of_submodule (LinearMap.range P) (LinearMap.range Q) e
  refine ⟨U, ?_⟩
  ext x
  have hPc : IsCompl (LinearMap.range P) (LinearMap.ker P) :=
    LinearMap.IsIdempotentElem.isCompl (f := P) hPid
  let eP : (LinearMap.range P × LinearMap.ker P) ≃ₗ[ℂ] E :=
    Submodule.prodEquivOfIsCompl (LinearMap.range P) (LinearMap.ker P) hPc
  rcases eP.surjective x with ⟨pr, hpr⟩
  rw [← hpr]
  rcases pr with ⟨a, b⟩
  have hUa : U (a : E) = (e a : E) := by
    simpa using (linearIsometryEquiv_of_submodule_apply (LinearMap.range P) (LinearMap.range Q) e a)
  have hUa_mem : U (a : E) ∈ LinearMap.range Q := by
    rw [hUa]; exact (e a).property
  have hQidrange : Q (U (a : E)) = U (a : E) := by
    exact idempotent_apply_of_mem_range Q hQid ⟨U (a : E), hUa_mem⟩
  have hUb_mem_ker : U (b : E) ∈ LinearMap.ker Q := by
    have hbb : (b : E) ∈ (LinearMap.range P)ᗮ := by simp [hkerP]
    have hUp := linearIsometryEquiv_of_submodule_mem_orthogonal
      (LinearMap.range P) (LinearMap.range Q) e hbb
    simpa [hkerQ] using hUp
  have hQzero : Q (U (b : E)) = 0 := by
    exact idempotent_apply_mem_ker Q ⟨U (b : E), hUb_mem_ker⟩
  have hLP : P (eP (a, b)) = (a : E) := by
    calc
      P (eP (a, b)) = P ((a : E) + (b : E)) := by rw [Submodule.coe_prodEquivOfIsCompl']
      _ = P (a : E) + P (b : E) := by simp
      _ = (a : E) := by
        rw [idempotent_apply_of_mem_range P hPid a, idempotent_apply_mem_ker P b]
        simp
  have hU_lin : U (eP (a, b)) = U (a : E) + U (b : E) := by
    calc
      U (eP (a, b)) = U ((a : E) + (b : E)) := by rw [Submodule.coe_prodEquivOfIsCompl']
      _ = U (a : E) + U (b : E) := by simp
  calc
    Q (U (eP (a, b))) = Q (U (a : E) + U (b : E)) := by rw [hU_lin]
    _ = Q (U (a : E)) + Q (U (b : E)) := by simp
    _ = U (a : E) + 0 := by rw [hQidrange, hQzero]
    _ = U (a : E) := by simp
    _ = U (P (eP (a, b))) := by rw [← hLP]

end ProjConj

section ProjConjUnitaryRank

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]

/-- **等比共轭 ⟹ 同秩（K₀ 秩定类的映射/定量方向）**：若等距（酉）等价
    $U:E\simeq_{\mathbb C}E$（$U^\dagger=U^{-1}$）实现共轭 $Q\circ U=U\circ P$
    （即 $Q=U\circ P\circ U^{-1}$），则 $\operatorname{range}P$ 与 $\operatorname{range}Q$
    同维（$\operatorname{rank}P=\operatorname{rank}Q$）。这是「酉等价类 = 秩」分类的
    **定量/映射方向**——保内积等价 $U$ 把 $\operatorname{range}P$ 双射映到
    $\operatorname{range}Q$（共轭关系经 `Submodule.map` 给像等式），`LinearEquiv.submoduleMap`
    把 $U$ 下降为受限线性等价，`LinearEquiv.finrank_eq` 给出同秩。与
    `same_rank_selfAdjoint_idempotent_unitary_conj` 合成
    `same_rank_iff_unitary_conj`，构成 §3 #7「秩唯一决定酉等价类= $K_0(\mathbb{C})\cong\mathbb{Z}$
    的秩定类」的**显式双向判定**。 -/
theorem finrank_eq_of_unitary_conj (P Q : E →ₗ[ℂ] E)
    (U : E ≃ₗᵢ[ℂ] E) (h : Q ∘ₗ U.toLinearMap = U.toLinearMap ∘ₗ P) :
    Module.finrank ℂ (LinearMap.range P) = Module.finrank ℂ (LinearMap.range Q) := by
  classical
  have hcomp : ∀ x, Q (U.toLinearMap x) = U.toLinearMap (P x) := by
    intro x
    simpa using LinearMap.ext_iff.mp h x
  have hUl : ∀ z, U.toLinearMap z = U z := by intro z; simp
  have hmap : (LinearMap.range P).map U.toLinearMap = LinearMap.range Q := by
    apply Submodule.ext
    intro x
    constructor
    · intro hx
      rcases (Submodule.mem_map).1 hx with ⟨a, ha, hxa⟩
      rw [← hxa]
      rcases (LinearMap.mem_range).1 ha with ⟨s, hs⟩
      rw [← hs, ← hcomp s]
      exact ⟨U.toLinearMap s, rfl⟩
    · intro hx
      rcases (LinearMap.mem_range).1 hx with ⟨z, hz : Q z = x⟩
      rcases U.surjective z with ⟨w, hw : U w = z⟩
      refine ⟨P w, ⟨w, rfl⟩, ?_⟩
      calc
        U.toLinearMap (P w) = Q (U.toLinearMap w) := (hcomp w).symm
        _ = Q (U w) := by rw [hUl]
        _ = Q z := by rw [hw]
        _ = x := hz
  let eL : LinearMap.range P ≃ₗ[ℂ] ↥((LinearMap.range P).map U.toLinearMap) :=
    U.toLinearEquiv.submoduleMap (LinearMap.range P)
  exact (eL.trans (LinearEquiv.ofEq ((LinearMap.range P).map U.toLinearMap) (LinearMap.range Q) hmap)).finrank_eq

variable [FiniteDimensional ℂ E]

/-- **主定理：秩唯一决定酉等价类（$K_0(\mathbb{C})\cong\mathbb{Z}$ 的秩定类显式判定）**：
    有限维复内积空间中，任意两个**自伴幂等**（正交投影）谱投影 P、Q 满足
    $\operatorname{rank}P=\operatorname{rank}Q \iff$ 酉等价（$\exists$ 保内积
    $U:E\simeq_{\mathbb C}E,\,Q\circ U=U\circ P$，即 $Q=U\circ P\circ U^{-1}$，
    $U^\dagger=U^{-1}$，§3 #7）。前向 = `same_rank_selfAdjoint_idempotent_unitary_conj`
    （酉构造），反向 = `finrank_eq_of_unitary_conj`（映射/定量）——这是「秩唯一决定
    酉等价类」即 $K_0(\mathbb{C})\to\mathbb{Z},\,[\mathbb{C}^r]\mapsto r$ 在投影层的
    **显式双射**。 -/
theorem same_rank_iff_unitary_conj (P Q : E →ₗ[ℂ] E)
    (hPid : IsIdempotentElem P) (hPsa : P.IsSymmetric)
    (hQid : IsIdempotentElem Q) (hQsa : Q.IsSymmetric) :
    Module.finrank ℂ (LinearMap.range P) = Module.finrank ℂ (LinearMap.range Q) ↔
      ∃ U : E ≃ₗᵢ[ℂ] E, Q ∘ₗ U.toLinearMap = U.toLinearMap ∘ₗ P := by
  constructor
  · intro hr
    exact same_rank_selfAdjoint_idempotent_unitary_conj P Q hPid hPsa hQid hQsa hr
  · rintro ⟨U, hU⟩
    exact finrank_eq_of_unitary_conj P Q U hU

end ProjConjUnitaryRank

/-!
## §2.15 同秩投影的直和：K₀ 秩映射的直和加性（K₀(ℂ)≅ℤ 的加法幺半种子）

§3 #7「同秩投影酉等价（K₀ = ℤ）」的**加法幺半结构**代数核心：§2.14 已证明
$\operatorname{rank}P=\operatorname{rank}Q\iff$ 酉等价——「秩唯一决定酉等价类」
的**完全不变量**。本层把它向 **K₀(ℂ) ≅ ℤ 的群同态**推进：任意两个（幂等）谱投影
P、Q 的直和（块对角）$P\oplus Q:=P.\mathrm{prodMap}\,Q:E\times F\to E\times F$
(1) 仍幂等（`directSum_idempotent`——直和保持投影性质，K₀ 加法幺半的结构基础）；
(2) 其秩为分量秩之和（`directSum_rank_add`：$\operatorname{rank}(P\oplus Q)
=\operatorname{rank}P+\operatorname{rank}Q$，经 `LinearMap.range_prodMap`
（像=子空间乘积）+ 子空间乘积线性等价 `prodSubmoduleLinearEquiv`（收紧
$\operatorname{finrank}(S.\mathrm{prod}\,T)=\operatorname{finrank}S
+\operatorname{finrank}T$）+ `Module.finrank_prod`）。这是「$K_0(\mathbb{C})\cong\mathbb{Z}$
秩定类」中**加法结构**的代数种子：秩映射沿直和相加，把「酉等价类=秩」从集合双射
提升为**幺半群同态**（直和 = 加法）。诚实边界（随登）：闭合的是幂等投影直和的
**幂等性与秩加性**（纯代数经 `finrank`）；把秩加性形成为完整 K₀ Grothendieck 群同态
（形式差、split-exact 关系商、$U(n)$/同伦类与秩一一对应）仍需群论/同伦基建，登记开放。 -/

section K0DirectSum

variable {E F : Type*} [AddCommGroup E] [AddCommGroup F] [Module ℂ E] [Module ℂ F]

/-- **子空间乘积 → 类型级乘积的线性等价（`finrank(S.prod T)=finrank S + finrank T` 的桥）**：
    `Submodule.prod S T` 是 $E\times F$ 的子空间，作为类型其载体为满足
    `x.1 ∈ S ∧ x.2 ∈ T` 的二元组；把它线性地重排为类型级乘积 `S × T`。
    这是 §2.15 秩映射直和加性的构造核：把子空间乘积的 finrank 收紧为**分量之和**
    （`finrank_eq` + `Module.finrank_prod`）。 -/
def prodSubmoduleLinearEquiv (S : Submodule ℂ E) (T : Submodule ℂ F) :
    Submodule.prod S T ≃ₗ[ℂ] S × T where
  toFun x := ⟨⟨(x : E × F).1, (Submodule.mem_prod).mp x.property |>.1⟩,
             ⟨(x : E × F).2, (Submodule.mem_prod).mp x.property |>.2⟩⟩
  invFun y := ⟨((y.1 : E), (y.2 : F)), (Submodule.mem_prod).mpr ⟨y.1.property, y.2.property⟩⟩
  map_add' := by intro x y; ext <;> rfl
  map_smul' := by intro a x; ext <;> rfl
  left_inv := by intro x; ext <;> rfl
  right_inv := by intro y; ext <;> rfl

/-- **直和的幂等性（块对角投影仍是投影）**：幂等 $P,Q$ 的直和（块对角）算子
    `P ⊕ Q := P.prodMap Q` 仍幂等——谱投影直和保持投影性质，这是 K₀ 加法幺半
    结构的代数基础。证明经 `LinearMap.prodMap_mul`（直和乘法=分量乘法）。 -/
theorem directSum_idempotent (P : E →ₗ[ℂ] E) (Q : F →ₗ[ℂ] F)
    (hP : IsIdempotentElem P) (hQ : IsIdempotentElem Q) :
    IsIdempotentElem (P.prodMap Q) := by
  calc
    (P.prodMap Q) * (P.prodMap Q) = (P * P).prodMap (Q * Q) :=
      (LinearMap.prodMap_mul P P Q Q).symm
    _ = P.prodMap Q := by rw [hP, hQ]

variable [FiniteDimensional ℂ E] [FiniteDimensional ℂ F]

/-- **秩映射的直和加性（rank(P ⊕ Q) = rank P + rank Q）**：同秩（同维像）幂等投影
    P、Q 的直和 `P.prodMap Q : E × F →ₗ E × F` 的秩等于分量秩之和。这是把 §2.14
    「秩唯一决定酉等价类」（完全不变量）向 **K₀(ℂ) ≅ ℤ 群同态**推进的关键加性
    性质：`rank` 沿直和相加。证明：`range (P.prodMap Q) = range P .prod range Q`
    （`LinearMap.range_prodMap`）+ 子空间乘积线性等价（`prodSubmoduleLinearEquiv`）
    + `Module.finrank_prod`（类型级乘积加性）。 -/
theorem directSum_rank_add (P : E →ₗ[ℂ] E) (Q : F →ₗ[ℂ] F) :
    Module.finrank ℂ (LinearMap.range (P.prodMap Q)) =
      Module.finrank ℂ (LinearMap.range P) + Module.finrank ℂ (LinearMap.range Q) := by
  calc
    Module.finrank ℂ (LinearMap.range (P.prodMap Q))
        = Module.finrank ℂ (Submodule.prod (LinearMap.range P) (LinearMap.range Q)) := by
          rw [LinearMap.range_prodMap]
    _ = Module.finrank ℂ (LinearMap.range P × LinearMap.range Q) :=
          (prodSubmoduleLinearEquiv (LinearMap.range P) (LinearMap.range Q)).finrank_eq
    _ = Module.finrank ℂ (LinearMap.range P) + Module.finrank ℂ (LinearMap.range Q) :=
          Module.finrank_prod

end K0DirectSum

/-!
## §2.16 K₀ 生成/自由交换群结构：秩签名是单生成元 ↦ ℤ 的同构（K₀(ℂ)≅ℤ 的自由交换群基底）

§3 #7「同秩投影酉等价（K₀ = ℤ）」的**生成/自由交换群结构**层。§2.14 闭合了
「秩唯一决定酉等价类」（`same_rank_iff_unitary_conj`：同秩 ⇔ 酉等价），给出
$K_0(\mathbb{C})\to\mathbb{Z},\,[\mathbb{C}^r]\mapsto r$ 在**投影层**的逐对双射；
§2.15 闭合其**直和加性**（`directSum_rank_add` 秩沿直和相加）。本层给出
$K_0(\mathbb{C})\cong\mathbb{Z}$ 的**生成/自由交换群基底**：自由交换群在
**单个生成元**（占据带类别实例化为 `PUnit`）上同构于 $\mathbb{Z}$
（mathlib `FreeAbelianGroup.uniqueEquiv`），且秩签名 `FreeAbelianGroup.lift`
（任意生成元带 ↦ 整数，唯一扩展为群同态）在单生成元处取 $1\in\mathbb{Z}$——
「每个整数对应一个秩（占据带维数）的自由交换群签名」。诚实边界（随登）：
闭合的是**纯代数自由交换群层**（单生成元 ≃ ℤ + 秩签名 lift 泛性质）；把同秩
酉类的**实际商幺半群**形成 + Grothendieck 化 + $U(n)$/同伦类与秩一一对应 +
环面上陈数密度 $F$ 的连续场论/度理论整性（含同伦提升，§3 #4）仍需完整
商/同伦/连续场论基建，登记开放。 -/

section K0FreeAbelian

open FreeAbelianGroup

/-- **单生成元自由交换群 ≃ ℤ**（mathlib `uniqueEquiv`）：自由交换群在
    单个生成元（占据带类别 `PUnit`）上同构于 ℤ——K₀(ℂ)≅ℤ 的
    生成/自由交换群结构的**基底**：♯([ℂ^r]) = r 的生成元对应。 -/
def single_generator_freeAbelian_iso_int : FreeAbelianGroup PUnit ≃+ ℤ :=
  uniqueEquiv PUnit

/-- **秩签名 lift（任意占据带 ↦ 整数唯一扩展为群同态）**：给定每个生成元
    带 $i$ 的占据整数 $\sigma_i\in\mathbb{Z}$，`FreeAbelianGroup.lift`
    把 `Fin r → ℤ ↦ (FreeAbelianGroup (Fin r) →+ ℤ)` 泛性质实例化——
    自由交换群的**唯一群同态**由生成元上的取值完全决定。这是把 §2.14
    秩映射（每个投影的秩）提升为**自由交换群同态**的机制。 -/
def rank_signature_lift {r : ℕ} (σ : Fin r → ℤ) : FreeAbelianGroup (Fin r) →+ ℤ :=
  FreeAbelianGroup.lift σ

/-- **单生成元秩签名 = 常数 1**：单占据带情形，生成元 `PUnit` 在
    `single_generator_freeAbelian_iso_int` 下的像为 $1\in\mathbb{Z}$——
    占据带投影的秩（$=\operatorname{rank}[\mathbb{C}^1]=1$）正是其自由交换群
    签名系数。这是「$K_0(\mathbb{C})\to\mathbb{Z},\,[\mathbb{C}^r]\mapsto r$」
    在**单生成元层**的显式取值。 -/
theorem rank_signature_single_eq (x : PUnit) :
    (single_generator_freeAbelian_iso_int : FreeAbelianGroup PUnit ≃+ ℤ) (of x) = 1 := by
  rw [single_generator_freeAbelian_iso_int]
  rfl

/-- **单生成元 ↦ 整数同构 is 自由交换群签名**：`FreeAbelianGroup.lift` 的
    泛性质在单生成元层的实例——每个 `PUnit → ℤ` 的取值唯一扩展为群同态，
    与 `single_generator_freeAbelian_iso_int` 一致（`of` 在同构下映到 1，
    `lift` 把生成元取值恢复）。这给出「秩签名」的**唯一性**。 -/
def single_signature_unique : (PUnit → ℤ) ≃ (FreeAbelianGroup PUnit →+ ℤ) :=
  FreeAbelianGroup.lift

end K0FreeAbelian

/-!
## §2.17 同秩酉类的商幺半群构造：酉等价 Setoid + 商类型 + 秩完全不变量（K₀ 商的基底）

§3 #7「同秩投影酉等价（K₀ = ℤ）」的**商幺半群构造**第一块（完整 Grothendieck
化的起点）。§2.14 闭合「秩 ⇔ 酉类」逐对双射（`same_rank_iff_unitary_conj`），
§2.15 闭合直和加性，§2.16 闭合自由交换群基底。本层把同秩自伴幂等（正交）投影
的**酉等价形式化为 `Setoid`**（反身 `projUnitaryRel_refl`、对称
`projUnitaryRel_symm`、传递 `projUnitaryRel_trans`），从而**构造商类型**
`Quotient (SelfAdjointIdemProj E)`，并把**秩映射下降为商上的良定义完全不变量**
（`rank_well_defined_on_quotient` 经 `finrank_eq_of_unitary_conj`——同酉类同秩；
`quotientRank : Quotient ... → ℕ` 经 `Quotient.lift`）。这是「K₀ 商代数」的
**载体构造基石**：酉类 = 秩的商对象存在，且秩是其上良定义分类函数。
诚实边界（随登）：闭合的是**同秩酉类的商载体**（Setoid 三条 + 商类型 + 秩良定义）；
在商上定义**加法**（跨空间直和 P⊕Q 的商良定性——$E\times F$ 上 `P.prodMap Q`
同酉类到哪一类的良定性映射）、证明商构成 **AddCommMonoid/Group**、以及把商秩
映射形成为**幺半同构 $ \mathrm{Quotient}\cong\mathbb{Z}$**（与 §2.16 自由交换群
基底连通）+ $U(n)$ 酉群/同伦类与秩一一对应，仍需完整商/同伦基建，登记开放。 -/

section K0Quotient

variable {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℂ E]

/-- **自伴幂等（正交）投影的子类型**：`P.IsSymmetric ∧ IsIdempotentElem P`。 -/
def SelfAdjointIdemProj (E : Type u) [NormedAddCommGroup E] [InnerProductSpace ℂ E] :=
  { P : E →ₗ[ℂ] E // IsIdempotentElem P ∧ P.IsSymmetric }

/-- **酉等价关系**：`Q ∘ₗ U = U ∘ₗ P`（即 Q = U·P·U†，U†=U⁻¹）。 -/
def ProjUnitaryRel (P Q : SelfAdjointIdemProj E) : Prop :=
  ∃ U : E ≃ₗᵢ[ℂ] E, Q.1 ∘ₗ U.toLinearMap = U.toLinearMap ∘ₗ P.1

/-- **反身性**：P ~ P 由恒等等距 U = 1 实现（1∘P = P∘1）。 -/
theorem projUnitaryRel_refl (P : SelfAdjointIdemProj E) : ProjUnitaryRel P P := by
  refine ⟨(1 : E ≃ₗᵢ[ℂ] E), ?_⟩
  ext x
  simp

/-- **对称性**：P ~ Q ⟹ Q ~ P，U⁻¹ 实现反向共轭（P∘U⁻¹ = U⁻¹∘Q）。 -/
theorem projUnitaryRel_symm {P Q : SelfAdjointIdemProj E} (h : ProjUnitaryRel P Q) :
    ProjUnitaryRel Q P := by
  rcases h with ⟨U, hU⟩
  refine ⟨U.symm, ?_⟩
  ext x
  -- 逐点提取：hU : ∀ y, Q (U y) = U (P y)
  have hpt : ∀ y, Q.1 (U y) = U (P.1 y) := by
    intro y
    simpa using (LinearMap.ext_iff.mp hU y)
  -- 目标：P (U.symm x) = U.symm (Q x)
  calc
    P.1 (U.symm x) = U.symm (U (P.1 (U.symm x))) := by
      exact (LinearIsometryEquiv.symm_apply_apply U (P.1 (U.symm x))).symm
    _ = U.symm (Q.1 (U (U.symm x))) := by
      rw [← hpt (U.symm x)]
    _ = U.symm (Q.1 x) := by
      rw [LinearIsometryEquiv.apply_symm_apply U x]

/-- **传递性**：P ~ Q ∧ Q ~ R ⟹ P ~ R，U₁.trans U₂（先 U₁ 再 U₂）实现复合。 -/
theorem projUnitaryRel_trans {P Q R : SelfAdjointIdemProj E}
    (hPQ : ProjUnitaryRel P Q) (hQR : ProjUnitaryRel Q R) : ProjUnitaryRel P R := by
  rcases hPQ with ⟨U₁, hU₁⟩
  rcases hQR with ⟨U₂, hU₂⟩
  refine ⟨U₁.trans U₂, ?_⟩
  ext x
  have hpt₁ : ∀ y, Q.1 (U₁ y) = U₁ (P.1 y) := by
    intro y
    simpa using (LinearMap.ext_iff.mp hU₁ y)
  have hpt₂ : ∀ y, R.1 (U₂ y) = U₂ (Q.1 y) := by
    intro y
    simpa using (LinearMap.ext_iff.mp hU₂ y)
  calc
    R.1 ((U₁.trans U₂) x) = R.1 (U₂ (U₁ x)) := by simp
    _ = U₂ (Q.1 (U₁ x)) := hpt₂ (U₁ x)
    _ = U₂ (U₁ (P.1 x)) := by rw [hpt₁ x]
    _ = (U₁.trans U₂) (P.1 x) := by simp

/-- **酉等价的 Setoid 结构**：反身+对称+传递 ⟹ 可作商。 -/
instance projUnitarySetoid (E : Type u) [NormedAddCommGroup E] [InnerProductSpace ℂ E] :
    Setoid (SelfAdjointIdemProj E) where
  r := ProjUnitaryRel
  iseqv := ⟨projUnitaryRel_refl, projUnitaryRel_symm, projUnitaryRel_trans⟩

section QuotRank

/-- **秩映射的商良定义（完全不变量）**：同酉类的投影同秩——经
    `finrank_eq_of_unitary_conj`（不依赖投影幂等/自伴，仅需共轭关系，也不需有限维）。 -/
theorem rank_well_defined_on_quotient {P Q : SelfAdjointIdemProj E}
    (h : ProjUnitaryRel P Q) :
    Module.finrank ℂ (LinearMap.range P.1) = Module.finrank ℂ (LinearMap.range Q.1) := by
  rcases h with ⟨U, hU⟩
  exact finrank_eq_of_unitary_conj P.1 Q.1 U hU

/-- **商类型上的秩函数**：`Quotient.lift` 下降，同酉类取同秩。 -/
noncomputable def quotientRank (E : Type u) [NormedAddCommGroup E]
    [InnerProductSpace ℂ E] [FiniteDimensional ℂ E] : Quotient (projUnitarySetoid E) → ℕ :=
  Quotient.lift (fun P => Module.finrank ℂ (LinearMap.range P.1)) (by
    intro P Q h
    exact rank_well_defined_on_quotient (E := E) h)

end QuotRank

end K0Quotient

/-!
## §2.18 K₀ 商秩的不变量强化：商秩是单射完全不变量（分类器）+ 可扩性 + 值域界

§3 #7「同秩投影酉等价（K₀ = ℤ）」的**商秩不变量强化**层。§2.14 闭合逐对显式双射
`same_rank_iff_unitary_conj`（同秩 ⇔ 酉等价），§2.17 把酉等价形式化为 `Setoid`
并把秩下降为商上的良定义函数 `quotientRank`。本层把「秩唯一决定酉等价类」从**逐对
双射**升级为**函数级完全不变量**：`quotientRank` 在商上**单射**（`quotientRank_injective`
——不同酉类必有不同秩，商上无"同秩异类"），从而合并良定义为**可扩性/等值判定**
（`quotientRank_ext`：商相等 ⟺ 同秩），并以 `quotientRank_le_dim` 给出分类器值域上界
（秩 ≤ dim E）。这使商对象在秩层被**完全锁定**：酉类集合如实嵌入 $\mathbb{N}_{\le\dim E}$，
是 Grothendieck 化（K₀(ℂ)≅ℤ）的**分类器落点**。诚实边界（随登）：闭合的是**商秩的
单射不变量强化**（单射 + 可扩性 + 值域界，经 §2.14 酉双射），且跨空间直和
$P\oplus Q$ 的**对象层商良定性**（L²-乘积 `WithLp 2 (E×F)` 内积实例 + 幂等/自伴
封闭 + 秩加性 + `projDirectSum_wellDefined` 商线性，§2.19）亦已闭合；但把商构成
**AddCommMonoid/Group** 并完成 **Grothendieck 化**（split-exact 关系商），及
$U(n)$ 酉群/同伦类与秩一一对应，仍需完整商/群论/同伦基建，登记开放。 -/

section K0QuotRankInv

variable {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℂ E]

/-- **商秩是商上的单射完全不变量**：有限维复内积空间中，
    `quotientRank : Quotient (projUnitarySetoid E) → ℕ` 单射——两个**不同酉类**
    必有不同秩。这是把 §2.14 的逐对显式双射（`same_rank_iff_unitary_conj`）
    升级为**函数级分类器**：秩完全决定酉类，商上无"同秩异类"。
    证明：`same_rank_iff_unitary_conj` 前向（同秩 ⟹ 酉等价）给 `ProjUnitaryRel P Q`，
    `Quotient.sound` 落入商相等。 -/
theorem quotientRank_injective [FiniteDimensional ℂ E] :
    Function.Injective (quotientRank E) := by
  rintro ⟨P⟩ ⟨Q⟩ h
  exact Quotient.sound (((same_rank_iff_unitary_conj P.1 Q.1 P.2.1 P.2.2 Q.2.1 Q.2.2).mp h))

/-- **秩完全决定酉类（商上的可扩性/extensionality）**：同秩 ⟺ 商相等。
    前向（商相等 ⟹ 同秩）＝ `quotientRank` 的良定义；反向（同秩 ⟹ 商相等）
    由 `quotientRank_injective`（单射完全不变量）给出。这是 §2.14
    「秩唯一决定酉等价类」在**商类型层面**的显式双向判定。 -/
theorem quotientRank_ext [FiniteDimensional ℂ E] {P Q : SelfAdjointIdemProj E} :
    Quotient.mk (projUnitarySetoid E) P = Quotient.mk (projUnitarySetoid E) Q ↔
      quotientRank E (Quotient.mk (projUnitarySetoid E) P) =
        quotientRank E (Quotient.mk (projUnitarySetoid E) Q) := by
  constructor
  · intro h
    rw [h]
  · intro h
    exact quotientRank_injective h

/-- **商秩有界（分类器值域 ⊆ {0,…,dim E}）**：占据带投影的秩不超过全空间维数——
    `Submodule.finrank_le`（子空间秩 ≤ 全空间秩）。这是 `quotientRank` 作为
    分类函数的**值域上界**，把「酉类=秩」的秩取值限制在有限维层内。 -/
theorem quotientRank_le_dim (P : SelfAdjointIdemProj E) [FiniteDimensional ℂ E] :
    quotientRank E (Quotient.mk (projUnitarySetoid E) P) ≤ Module.finrank ℂ E := by
  simp [quotientRank]
  exact Submodule.finrank_le (LinearMap.range P.1)

end K0QuotRankInv

/-!
## §2.19 K₀ 商加法的载体：跨空间直和 P⊕Q 的商良定性（在商上定义加法）

本层实现 §2.18/§3 开放登记中关键的一块：把同秩酉类的商（§2.17）从**单空间载体**
升级为**跨空间加法**。商加法 $[P]\oplus[Q]:=[P\oplus Q]$ 的对象载体取两空间 $E,F$
的 **L²-乘积** $\mathrm{WithLp}\,2\,(E\times F)$——因 mathlib 对**原始二元乘积**
$E\times F$ 不自动捆绑 `InnerProductSpace` 实例，需显式转移到注册了内积的
L²-乘积类型（`WithLp.instProdInnerProductSpace`，经 `WithLp.linearEquiv` 线性等价）。
在 $E\times F$ 上定义块对角投影 $P\oplus Q:=P.\mathrm{prodMap}\,Q$（§2.15 载体），
经 `toL2`/`fromL2` 线性等价提升到 L²-乘积，得 $P\oplus Q$ 的自伴幂等（正交）投影
`projDirectSum`（`projDirectSumMap_idempotent`/`_symmetric` 幂等+自伴封闭）。
核心结果：
- **跨空间直和的秩加性** `projDirectSumMap_rank_add`：$\operatorname{rank}(P\oplus Q)
  =\operatorname{rank}P+\operatorname{rank}Q$——`toL2` 线性等价保持 finrank
  （`toL2.submoduleMap`），并归约到 §2.15 `directSum_rank_add`。
- **商秩的直和加性（分类器层）** `quotientRank_projDirectSum_add`：把 §2.18 的商秩
  分类器提升为**跨空间加法映射** $[P]\oplus[Q]\mapsto r+s$——商加法的量表落点。
- **商加法良定性（商线性）** `projDirectSum_wellDefined`：$P\sim P'∧Q\sim Q'⟹
  P\oplus Q\sim P'\oplus Q'$——跨空间直和在**商上良定义**。证明经 §2.14 同秩酉等价
  （`same_rank_iff_unitary_conj`）+ 直和秩加性（分量同秩 ⟹ 直和同秩 ⟹ 酉等价），
  免去显式构造乘积等距。

这为 Grothendieck 化（K₀(ℂ)≅ℤ）提供**商加法的对象载体**与**商线性**：商运算
$[(E,P)]\oplus[(F,Q)]$ 良定义。诚实边界（随登）：闭合的是**跨空间直和（对象层）的
商良定性**；把商构成 **AddCommMonoid/Group**（在商类型上验证加法封闭/结合/单位，
即商加法作为函数良定义 + 幺半群/群公理）、完整 **Grothendieck 化**（split-exact
关系商），以及 $U(n)$ 酉群/同伦类与秩的一一对应的商/群/同伦基建，登记开放。 -/

section K0ProjAdd

open Module LinearMap

variable {E F : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
  [NormedAddCommGroup F] [InnerProductSpace ℂ F]

/-- 原始乘积 → L²-乘积（`WithLp 2 (E × F)`，其上注册 `InnerProductSpace` 实例）
    的提升线性等价（`WithLp.linearEquiv` 之逆）。 -/
def toL2 : (E × F) ≃ₗ[ℂ] WithLp 2 (E × F) := (WithLp.linearEquiv 2 ℂ (E × F)).symm

/-- L²-乘积 → 原始乘积 的投影线性等价。 -/
def fromL2 : WithLp 2 (E × F) ≃ₗ[ℂ] (E × F) := WithLp.linearEquiv 2 ℂ (E × F)

/-- **投影直和（商加法的对象载体）**：`P⊕Q` 在 L²-乘积空间上的块对角投影
    （共轭提升）；原始乘积 `E×F` 无内积实例，故提升到 `WithLp 2 (E × F)`。 -/
def projDirectSumMap (P : E →ₗ[ℂ] E) (Q : F →ₗ[ℂ] F) :
    WithLp 2 (E × F) →ₗ[ℂ] WithLp 2 (E × F) :=
  toL2.toLinearMap.comp ((P.prodMap Q).comp fromL2.toLinearMap)

/-- 物化：任意 L²-元素可写为 `toL2 (fromL2 x)`（`toL2 ∘ fromL2 = id`）。 -/
lemma l2_ext (x : WithLp 2 (E × F)) : x = toL2 (fromL2 x) := by
  unfold toL2 fromL2
  simp

/-- 共轭梳理：`projDirectSumMap P Q (toL2 x) = toL2 ((P.prodMap Q) x)`。 -/
lemma projDirectSumMap_toL2_apply (P : E →ₗ[ℂ] E) (Q : F →ₗ[ℂ] F) (x : (E × F)) :
    projDirectSumMap P Q (toL2 x) = toL2 ((P.prodMap Q) x) := by
  unfold projDirectSumMap
  simp [toL2, fromL2]

/-- **L²-内积按分量相加**（`toL2` 物化后）：`⟪toL2 a, toL2 b⟫ = ⟪a.1,b.1⟫ + ⟪a.2,b.2⟫`。 -/
lemma inner_toL2 (a b : (E × F)) :
    inner ℂ (toL2 a) (toL2 b) = inner ℂ a.1 b.1 + inner ℂ a.2 b.2 := by
  rw [WithLp.prod_inner_apply]
  congr 1

/-- **直和的幂等性**：幂等 $P,Q$ 的 L²-直和仍幂等（`P.prodMap Q` 幂等 §2.15，
    共轭保持幂等）。 -/
theorem projDirectSumMap_idempotent (P : E →ₗ[ℂ] E) (Q : F →ₗ[ℂ] F)
    (hP : IsIdempotentElem P) (hQ : IsIdempotentElem Q) :
    IsIdempotentElem (projDirectSumMap P Q) := by
  ext x
  simp [projDirectSumMap, toL2, fromL2]
  constructor
  · exact LinearMap.congr_fun hP x.fst
  · exact LinearMap.congr_fun hQ x.snd

/-- **直和的自伴性**：对称 $P,Q$ 的 L²-直和仍对称（块对角保内积）⟹
    落在 `SelfAdjointIdemProj`。 -/
theorem projDirectSumMap_symmetric (P : E →ₗ[ℂ] E) (Q : F →ₗ[ℂ] F)
    (hP : P.IsSymmetric) (hQ : Q.IsSymmetric) :
    (projDirectSumMap P Q).IsSymmetric := by
  intro z w
  rw [l2_ext z, l2_ext w]
  rw [projDirectSumMap_toL2_apply, projDirectSumMap_toL2_apply]
  rw [inner_toL2, inner_toL2]
  simp [LinearMap.prodMap_apply]
  rw [hP, hQ]

/-- **跨空间直和的投影对象**：把自伴幂等（正交）投影 $P,Q$ 的 L²-直和包装为
    `SelfAdjointIdemProj (WithLp 2 (E×F))`（§2.17 商类型的载体之一）——
    商加法的对象构造。 -/
def projDirectSum (P : SelfAdjointIdemProj E) (Q : SelfAdjointIdemProj F) :
    SelfAdjointIdemProj (WithLp 2 (E × F)) :=
  ⟨projDirectSumMap P.1 Q.1,
    projDirectSumMap_idempotent P.1 Q.1 P.2.1 Q.2.1,
    projDirectSumMap_symmetric P.1 Q.1 P.2.2 Q.2.2⟩

variable [FiniteDimensional ℂ E] [FiniteDimensional ℂ F]

/-- **直和的秩加性（商秩连接）**：`projDirectSumMap P Q` 的秩 = 分量秩之和。
    证明：共轭的线性等价 `toL2` 保持像的 finrank（`toL2.submoduleMap`），
    且 `P.prodMap Q` 的秩 = 分量秩之和（§2.15 `directSum_rank_add`）。 -/
theorem projDirectSumMap_rank_add (P : E →ₗ[ℂ] E) (Q : F →ₗ[ℂ] F) :
    Module.finrank ℂ (LinearMap.range (projDirectSumMap P Q)) =
      Module.finrank ℂ (LinearMap.range P) + Module.finrank ℂ (LinearMap.range Q) := by
  have hrange : LinearMap.range (projDirectSumMap P Q) =
      (LinearMap.range (P.prodMap Q)).map toL2.toLinearMap := by
    ext x
    constructor
    · rintro ⟨y, hy⟩
      let w : (E × F) := (P.prodMap Q) (fromL2 y)
      refine ⟨w, ⟨fromL2 y, rfl⟩, ?_⟩
      rw [← hy]
      unfold projDirectSumMap
      simp [toL2, fromL2, w]
    · rintro ⟨w, ⟨s, hs⟩, hx⟩
      refine ⟨toL2 s, ?_⟩
      rw [projDirectSumMap_toL2_apply]
      calc
        toL2 ((P.prodMap Q) s) = toL2 w := by rw [hs]
        _ = x := hx
  calc
    Module.finrank ℂ (LinearMap.range (projDirectSumMap P Q))
        = Module.finrank ℂ ((LinearMap.range (P.prodMap Q)).map toL2.toLinearMap) := by
            rw [hrange]
    _ = Module.finrank ℂ (LinearMap.range (P.prodMap Q)) := by
            exact (toL2.submoduleMap (LinearMap.range (P.prodMap Q))).finrank_eq.symm
    _ = Module.finrank ℂ (LinearMap.range P) + Module.finrank ℂ (LinearMap.range Q) :=
            directSum_rank_add P Q

/-- **商秩的直和加性（商加法在分类器层）**：`quotientRank` 在跨空间直和上沿分量
    相加——$[\mathbb{C}^r]\oplus[\mathbb{C}^s]\mapsto r+s$。这把 §2.18 的商秩分类器
    从**单空间**提升为**跨空间加法映射**，是商加法的量表落点。 -/
theorem quotientRank_projDirectSum_add (P : SelfAdjointIdemProj E) (Q : SelfAdjointIdemProj F) :
    quotientRank (WithLp 2 (E × F)) (Quotient.mk (projUnitarySetoid (WithLp 2 (E × F)))
      (projDirectSum P Q)) =
      quotientRank E (Quotient.mk (projUnitarySetoid E) P)
        + quotientRank F (Quotient.mk (projUnitarySetoid F) Q) := by
  unfold quotientRank
  change Module.finrank ℂ (LinearMap.range (projDirectSumMap P.1 Q.1)) =
      Module.finrank ℂ (LinearMap.range P.1) + Module.finrank ℂ (LinearMap.range Q.1)
  exact projDirectSumMap_rank_add P.1 Q.1

/-- **商加法良定性（商线性）**：`P~P' ∧ Q~Q' ⟹ (P⊕Q)~(P'⊕Q')`——跨空间直和在
    商上良定义。证明：经 §2.14 同秩酉等价（`same_rank_iff_unitary_conj`）+ 直和
    秩加性（分量秩相同 ⟹ 直和同秩 ⟹ 酉等价），免去构造乘积等距。这是
    「商加法 = 跨空间直和」的商良定性。 -/
theorem projDirectSum_wellDefined (P P' : SelfAdjointIdemProj E) (Q Q' : SelfAdjointIdemProj F)
    (hP : ProjUnitaryRel P P') (hQ : ProjUnitaryRel Q Q') :
    ProjUnitaryRel (projDirectSum P Q) (projDirectSum P' Q') := by
  have hrankP : Module.finrank ℂ (LinearMap.range P.1) = Module.finrank ℂ (LinearMap.range P'.1) :=
    rank_well_defined_on_quotient hP
  have hrankQ : Module.finrank ℂ (LinearMap.range Q.1) = Module.finrank ℂ (LinearMap.range Q'.1) :=
    rank_well_defined_on_quotient hQ
  exact (same_rank_iff_unitary_conj (projDirectSum P Q).1 (projDirectSum P' Q').1
      (projDirectSum P Q).2.1 (projDirectSum P Q).2.2 (projDirectSum P' Q').2.1
      (projDirectSum P' Q').2.2).mp (by
    change Module.finrank ℂ (LinearMap.range (projDirectSumMap P.1 Q.1)) =
      Module.finrank ℂ (LinearMap.range (projDirectSumMap P'.1 Q'.1))
    rw [projDirectSumMap_rank_add, projDirectSumMap_rank_add, hrankP, hrankQ])

end K0ProjAdd

/-! ## §2.20 K₀ 的 Grothendieck 群完成：ℕ 的 split-exact 完成 ≅ ℤ（把商构成群）

本层闭合 §2.19 开放登记中「把商构成 AddCommMonoid/Group + 完整 Grothendieck 化」
的核心：把商加法的对象载体（§2.19 跨空间直和 $P\oplus Q$）经 **Grothendieck 群
完成**落成为 ℕ 的 split-exact 商。核心结果：
- **Grothendieck 关系（秩层）** `GrothRel`、`grothRel_refl`/`_symm`/`_trans`：
  把加性幺半群 ℕ 的 split-exact 完成形式化为 $ℕ\timesℕ$ 上的差对等价
  $(a,b)\sim(c,d)\iff a+d=b+c$，并构成 `Setoid`（`grothSetoid`），从而商类型
  `GrothQuot` 合法存在。商秩分类器 `quotientRank` 把投影商类映到 ℕ 的差对。
- **秩差同态** `grothToInt`、`_injective`、`_surjective`、`_equiv`：把差对
  $[(a,b)]$ 映射为零差 $a-b\in\mathbb{Z}$（商上良定义 $a+d=b+c\Rightarrow a-b=c-d$），
  单射（零差唯一决定差类）+ 满射（非负取 $(r,0)$、负取 $(0,s)$）⟹ 双射
  `grothToIntEquiv : GrothQuot ≃ ℤ`。
- **商构成 AddCommGroup** `grothQuotAddCommGroup`：经单射 `grothToInt` 从 ℤ 传送
  （`Function.Injective.addCommGroup`），配合 `grothIntHom` 与 **群同构
  `grothToIntIso : GrothQuot ≃+ ℤ`**（`AddEquiv.ofBijective`）——格罗滕迪克商构成
  加法群，即 K₀(ℂ)≅ℤ 在 **Grothendieck 群层的实现**。
- **群运算法** `grothAdd_mk_eq`（自然加法=逐分量共合 $[a]+[c]=[a_1+c_1,a_2+c_2]$）、
  `grothNeg_mk_eq`（$-[a,b]=[b,a]$）、`grothZero_eq`（$0=[0,0]$）——商加/负/零良定义。
- **与 §2.16 会师** `grothQuot_to_freeAbelian`：Grothendieck 群 `GrothQuot` 与自由
  交换群 `FreeAbelianGroup PUnit` 均 ≅ ℤ（经 `grothToIntIso` 与
  `single_generator_freeAbelian_iso_int`），复合给出 `GrothQuot ≃+ FreeAbelianGroup PUnit`
  ——K₀(ℂ)≅ℤ 的 Grothendieck 完成与自由交换群两条实现路径一致。
- **连接分类器** `projGrothRel_iff`：把**投影层 Grothendieck 关系**（split-exact 差对
  $(P,Q)\sim(P',Q')\iff P\oplus Q'\sim_{\text{酉}} P'\oplus Q$，经 §2.19 跨空间直和）
  判据归约为**秩层加法等式** $\mathrm{rank}P+\mathrm{rank}Q'=\mathrm{rank}P'+\mathrm{rank}Q$
  （`quotientRank_projDirectSum_add` 直和秩加性）；`grothToInt_of_rank_diff` 把商秩
  差对送到 `grothToInt` 恰等于秩之差——投影层 Grothendieck 关系正是 `GrothRel` 经
  `quotientRank` 的精确实现。

诚实边界（随登）：闭合的是**秩层 ℕ 的 Grothendieck 群完成**（`GrothQuot` 构成
`AddCommGroup`、`grothToIntIso : GrothQuot ≃+ ℤ`）与投影层 Grothendieck 关系在秩层
的判据（`projGrothRel_iff`）；把**投影商类本身**（自伴幂等投影的酉类商，§2.17/§2.19）
作为 Grothendieck 群**对象层完整 K₀ 结构**（商加法沿商类型构成幺半群/群、投影类的
Grothendieck 群 $\cong\mathbb{Z}$），以及 $U(n)$ 酉群/同伦类与秩的一一对应的完整
商/群/同伦基建，登记开放。 -/

section K0Groth

open scoped Int

/-- **Grothendieck（群完成）关系（秩层）**：把加性幺半群 ℕ 的 split-exact 完成形式化
    为 `ℕ × ℕ` 上的关系 $(a,b)\sim(c,d)\iff a+d=b+c$——差对沿 "直和增量" 相加保持。
    这是 K₀(ℂ)≅ℤ 的最简 K₀ 模型：商秩分类器 `quotientRank` 把投影商类映到 ℕ，
    而 ℕ 的 Grothendieck 完成恰为 ℤ（见 `grothToInt`）。 -/
def GrothRel (x y : ℕ × ℕ) : Prop := x.1 + y.2 = y.1 + x.2

theorem grothRel_refl (x : ℕ × ℕ) : GrothRel x x := by
  rfl

theorem grothRel_symm {x y : ℕ × ℕ} (h : GrothRel x y) : GrothRel y x := by
  unfold GrothRel at h ⊢
  omega

theorem grothRel_trans {x y z : ℕ × ℕ} (h₁ : GrothRel x y) (h₂ : GrothRel y z) :
    GrothRel x z := by
  unfold GrothRel at h₁ h₂ ⊢
  have h₁z : (x.1 : ℤ) + (y.2 : ℤ) = (y.1 : ℤ) + (x.2 : ℤ) := by
    exact_mod_cast h₁
  have h₂z : (y.1 : ℤ) + (z.2 : ℤ) = (z.1 : ℤ) + (y.2 : ℤ) := by
    exact_mod_cast h₂
  exact_mod_cast (by omega : (x.1 : ℤ) + (z.2 : ℤ) = (z.1 : ℤ) + (x.2 : ℤ))

/-- **Grothendieck 关系的 Setoid**：反身+对称+传递 ⟹ 可作商。 -/
instance grothSetoid : Setoid (ℕ × ℕ) where
  r := GrothRel
  iseqv := ⟨grothRel_refl, grothRel_symm, grothRel_trans⟩

/-- **Grothendieck 商类型**（ℕ 的群完成载体）。 -/
abbrev GrothQuot := Quotient grothSetoid

/-- **秩之差同态**：$[(a,b)]\mapsto (a-b)\in\mathbb{Z}$——把 Grothendieck 商型
    送到 ℤ（商上良定义：$a+d=b+c\Rightarrow a-b=c-d$）。 -/
noncomputable def grothToInt : GrothQuot → ℤ :=
  Quotient.lift (fun x : ℕ × ℕ => (x.1 : ℤ) - (x.2 : ℤ)) (by
    intro x y h
    have hz : (x.1 : ℤ) + (y.2 : ℤ) = (y.1 : ℤ) + (x.2 : ℤ) := by
      exact_mod_cast h
    omega)

/-- **`grothToInt` 在代表元上的取值**（商 lift 计算）。 -/
theorem grothToInt_mk (p : ℕ × ℕ) :
    grothToInt (Quotient.mk grothSetoid p) = (p.1 : ℤ) - (p.2 : ℤ) := by
  rfl

/-- **单射**：秩之差唯一确定差类（$\mathbb{Z}$ 到 Grothendieck 商 1-1）。 -/
theorem grothToInt_injective : Function.Injective grothToInt := by
  rintro ⟨x⟩ ⟨y⟩ h
  apply Quotient.sound
  change x.1 + y.2 = y.1 + x.2
  -- h : grothToInt ⟦x⟧ = grothToInt ⟦y⟧；展开成分量形
  have hh : (x.1 : ℤ) - (x.2 : ℤ) = (y.1 : ℤ) - (y.2 : ℤ) :=
    (grothToInt_mk x).symm.trans (h.trans (grothToInt_mk y))
  have hz : (x.1 : ℤ) + (y.2 : ℤ) = (y.1 : ℤ) + (x.2 : ℤ) := by
    calc
      (x.1 : ℤ) + (y.2 : ℤ) = (x.1 : ℤ) - (x.2 : ℤ) + (y.2 : ℤ) + (x.2 : ℤ) := by ring
      _ = (y.1 : ℤ) - (y.2 : ℤ) + (y.2 : ℤ) + (x.2 : ℤ) := by rw [hh]
      _ = (y.1 : ℤ) + (x.2 : ℤ) := by ring
  exact_mod_cast hz

/-- **满射**：每个整数都是某差对的秩之差（非负取 $(r,0)$，负取 $(0,s)$）。 -/
theorem grothToInt_surjective : Function.Surjective grothToInt := by
  intro n
  by_cases hnonneg : 0 ≤ n
  · let r : ℕ := n.toNat
    refine ⟨Quotient.mk grothSetoid (r, 0), ?_⟩
    change (r : ℤ) - (0 : ℤ) = n
    have hr : (r : ℤ) = n := by
      simp only [r, Int.toNat_of_nonneg hnonneg]
    omega
  · let s : ℕ := (-n).toNat
    refine ⟨Quotient.mk grothSetoid (0, s), ?_⟩
    change (0 : ℤ) - (s : ℤ) = n
    have hs : (s : ℤ) = -n := by
      simp only [s, Int.toNat_of_nonneg (by omega : 0 ≤ -n)]
    omega

/-- **`grothToInt` 的等价**（双射）。 -/
noncomputable def grothToIntEquiv : GrothQuot ≃ ℤ :=
  Equiv.ofBijective grothToInt ⟨grothToInt_injective, grothToInt_surjective⟩

-- 通过等价 `grothToIntEquiv` 传送 ℤ 的低层运算（可加群结构经 `Injective.addCommGroup` 生成）
noncomputable instance : Zero GrothQuot := ⟨grothToIntEquiv.symm 0⟩
noncomputable instance : Add GrothQuot :=
  ⟨fun a b => grothToIntEquiv.symm (grothToIntEquiv a + grothToIntEquiv b)⟩
noncomputable instance : Neg GrothQuot := ⟨fun a => grothToIntEquiv.symm (-grothToIntEquiv a)⟩
noncomputable instance : Sub GrothQuot :=
  ⟨fun a b => grothToIntEquiv.symm (grothToIntEquiv a - grothToIntEquiv b)⟩
noncomputable instance : SMul ℕ GrothQuot := ⟨fun n a => grothToIntEquiv.symm (n • grothToIntEquiv a)⟩
noncomputable instance : SMul ℤ GrothQuot := ⟨fun z a => grothToIntEquiv.symm (z • grothToIntEquiv a)⟩

/-- **GrothQuot 是可加交换群（AddCommGroup）**：经单射 `grothToInt` 从 ℤ 传送
    （`Function.Injective.addCommGroup`）——格罗滕迪克商构成加法群。 -/
noncomputable instance grothQuotAddCommGroup : AddCommGroup GrothQuot :=
  Function.Injective.addCommGroup grothToInt grothToInt_injective
    (by
      change grothToIntEquiv (grothToIntEquiv.symm 0) = 0
      rw [Equiv.apply_symm_apply grothToIntEquiv])
    (by
      intro a b
      change grothToIntEquiv (grothToIntEquiv.symm (grothToIntEquiv a + grothToIntEquiv b)) =
        grothToInt a + grothToInt b
      rw [Equiv.apply_symm_apply grothToIntEquiv]
      rfl)
    (by
      intro a
      change grothToIntEquiv (grothToIntEquiv.symm (-grothToIntEquiv a)) = -grothToInt a
      rw [Equiv.apply_symm_apply grothToIntEquiv]
      rfl)
    (by
      intro a b
      change grothToIntEquiv (grothToIntEquiv.symm (grothToIntEquiv a - grothToIntEquiv b)) =
        grothToInt a - grothToInt b
      rw [Equiv.apply_symm_apply grothToIntEquiv]
      rfl)
    (by
      intro a n
      change grothToIntEquiv (grothToIntEquiv.symm (n • grothToIntEquiv a)) = n • grothToInt a
      rw [Equiv.apply_symm_apply grothToIntEquiv]
      rfl)
    (by
      intro a n
      change grothToIntEquiv (grothToIntEquiv.symm (n • grothToIntEquiv a)) = n • grothToInt a
      rw [Equiv.apply_symm_apply grothToIntEquiv]
      rfl)

/-- **`grothToInt` 是群同态到 ℤ**。 -/
noncomputable def grothIntHom : GrothQuot →+ ℤ where
  toFun := grothToInt
  map_zero' := by
    change grothToIntEquiv (grothToIntEquiv.symm 0) = 0
    rw [Equiv.apply_symm_apply grothToIntEquiv]
  map_add' := by
    intro a b
    change grothToIntEquiv (grothToIntEquiv.symm (grothToIntEquiv a + grothToIntEquiv b)) =
      grothToInt a + grothToInt b
    rw [Equiv.apply_symm_apply grothToIntEquiv]
    rfl

/-- **Grothendieck 群同构 ℤ**：`GrothQuot ≃+ ℤ`（可加群层）。 -/
noncomputable def grothToIntIso : GrothQuot ≃+ ℤ :=
  AddEquiv.ofBijective grothIntHom ⟨grothToInt_injective, grothToInt_surjective⟩

/-- **`grothToInt` 加法保持**。 -/
theorem grothToInt_add (a b : GrothQuot) : grothToInt (a + b) = grothToInt a + grothToInt b := by
  change grothToIntIso (a + b) = grothToIntIso a + grothToIntIso b
  exact grothToIntIso.map_add a b

/-- **自然加法 = 直和共合**：商类的加法由对的逐分量相加诱导
    $[a]+[c]=[a_1+c_1,\,a_2+c_2]$（传送加法与对共合一致）。 -/
theorem grothAdd_mk_eq (x y : ℕ × ℕ) :
    Quotient.mk grothSetoid x + Quotient.mk grothSetoid y =
      Quotient.mk grothSetoid (x.1 + y.1, x.2 + y.2) := by
  apply grothToInt_injective
  rw [grothToInt_add]
  repeat rw [grothToInt_mk]
  omega

/-- **负数良定**：`-[(a,b)] = [(b,a)]`（交换差对）。 -/
theorem grothNeg_mk_eq (a b : ℕ) :
    -(Quotient.mk grothSetoid (a, b)) = Quotient.mk grothSetoid (b, a) := by
  apply grothToInt_injective
  rw [grothToInt_mk]
  change grothToIntIso (-(Quotient.mk grothSetoid (a, b))) = (b : ℤ) - (a : ℤ)
  rw [grothToIntIso.map_neg]
  change -grothToInt (Quotient.mk grothSetoid (a, b)) = (b : ℤ) - (a : ℤ)
  rw [grothToInt_mk]
  ring

/-- **零良定**：$0=[(0,0)]$。 -/
theorem grothZero_eq : (0 : GrothQuot) = Quotient.mk grothSetoid (0, 0) := by
  apply grothToInt_injective
  change grothToIntIso (0 : GrothQuot) = grothToInt (Quotient.mk grothSetoid (0, 0))
  rw [grothToIntIso.map_zero, grothToInt_mk]
  norm_num

/-- **与 §2.16 会师**：Grothendieck 群 `GrothQuot` 与自由交换群 `FreeAbelianGroup PUnit`
    均 ≅ ℤ（分别经 `grothToIntIso` 与 `single_generator_freeAbelian_iso_int`），复合给出
    `GrothQuot ≃+ FreeAbelianGroup PUnit`——K₀(ℂ)≅ℤ 的格罗滕迪克完成与自由交换群
    两条实现路径一致。 -/
noncomputable def grothQuot_to_freeAbelian : GrothQuot ≃+ FreeAbelianGroup PUnit :=
  grothToIntIso.trans single_generator_freeAbelian_iso_int.symm

/-! ### 连接分类器：商秩 + 商秩直和加性 ⟹ 投影层 Grothendieck 关系（商秩一致） -/

section K0GrothConnect

variable {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℂ E] [FiniteDimensional ℂ E]

/-- **投影层 Grothendieck 关系（split-exact 差对）**：$(P,Q)\sim(P',Q')\iff
   P\oplus Q'\sim_{\text{酉}} P'\oplus Q$（跨空间直和，§2.19）——K₀ 差对象沿
   直和相加的约化关系。 -/
def projGrothRel (a c : SelfAdjointIdemProj E × SelfAdjointIdemProj E) : Prop :=
  ProjUnitaryRel (projDirectSum a.1 c.2) (projDirectSum c.1 a.2)

/-- **投影 Grothendieck 关系 ⇔ 秩层 Grothendieck 关系**：$P\oplus Q'\sim P'\oplus Q
   \iff \mathrm{rank}P+\mathrm{rank}Q'=\mathrm{rank}P'+\mathrm{rank}Q$——把 §2.19 的
   跨空间直和秩加性（`quotientRank_projDirectSum_add`）收紧为 split-exact 商关系在
   秩层的判据；从而投影层 Grothendieck 关系正是 `GrothRel`（§2.20 商关系）经
   `quotientRank` 的精确实现。 -/
theorem projGrothRel_iff (a c : SelfAdjointIdemProj E × SelfAdjointIdemProj E) :
    projGrothRel a c ↔
      quotientRank E (Quotient.mk (projUnitarySetoid E) a.1)
        + quotientRank E (Quotient.mk (projUnitarySetoid E) c.2) =
      quotientRank E (Quotient.mk (projUnitarySetoid E) c.1)
        + quotientRank E (Quotient.mk (projUnitarySetoid E) a.2) := by
  unfold projGrothRel ProjUnitaryRel
  rw [(same_rank_iff_unitary_conj (projDirectSum a.1 c.2).1 (projDirectSum c.1 a.2).1
      (projDirectSum a.1 c.2).2.1 (projDirectSum a.1 c.2).2.2
      (projDirectSum c.1 a.2).2.1 (projDirectSum c.1 a.2).2.2).symm]
  change quotientRank (WithLp 2 (E × E))
        (Quotient.mk (projUnitarySetoid (WithLp 2 (E × E))) (projDirectSum a.1 c.2)) =
      quotientRank (WithLp 2 (E × E))
        (Quotient.mk (projUnitarySetoid (WithLp 2 (E × E))) (projDirectSum c.1 a.2)) ↔
      quotientRank E (Quotient.mk (projUnitarySetoid E) a.1)
        + quotientRank E (Quotient.mk (projUnitarySetoid E) c.2) =
      quotientRank E (Quotient.mk (projUnitarySetoid E) c.1)
        + quotientRank E (Quotient.mk (projUnitarySetoid E) a.2)
  rw [quotientRank_projDirectSum_add a.1 c.2, quotientRank_projDirectSum_add c.1 a.2]

/-- **商秩差到整数**（分类器与格罗滕迪克商协调）：差对 $[P]-[Q]$ 的商秩差送到
    `grothToInt` 恰等于两秩之差 $\mathrm{rank}P-\mathrm{rank}Q$。与 §2.16 秩签名
    （单生成元取 $1$）共享同一分类器语义。 -/
theorem grothToInt_of_rank_diff (P Q : SelfAdjointIdemProj E) :
    grothToInt (Quotient.mk grothSetoid
      (quotientRank E (Quotient.mk (projUnitarySetoid E) P),
       quotientRank E (Quotient.mk (projUnitarySetoid E) Q))) =
      (quotientRank E (Quotient.mk (projUnitarySetoid E) P) : ℤ)
        - (quotientRank E (Quotient.mk (projUnitarySetoid E) Q) : ℤ) := by
  exact grothToInt_mk (quotientRank E (Quotient.mk (projUnitarySetoid E) P),
                        quotientRank E (Quotient.mk (projUnitarySetoid E) Q))

end K0GrothConnect

end K0Groth

/-! ## §2.21 对象层 K₀：投影差对象商 + 秩差完全不变量（投影商类作为完整 K₀ 结构）

承接 §2.17–§2.20：§2.17 造自伴幂等投影的酉类商（`Quotient (projUnitarySetoid E)`），
§2.18 证商秩 `quotientRank` 单射完全不变量，§2.19 造跨空间直和 `projDirectSum` + 秩加性
（商加法对象载体与商线性），§2.20 把**秩层 ℕ** Grothendieck 化（`GrothQuot ≃+ ℤ`）并把
投影层差对关系 `projGrothRel_iff`（⇔秩层加法等式）建立。本层闭合 §2.20 诚实边界中
「把**投影商类本身**作为 Grothendieck 群的**对象层完整 K₀ 结构**」的可证部分：
把投影层差对关系 `projGrothRel` 本身构造为**商**（构成 `Setoid`），在其商类型
`ProjDiffQuot E` 上定义**对象层秩差完全不变量** `projToInt`——这是对象层
（投影酉类差对象，非秩层）的第一性完全分类器：

- **`projGrothRel` 构成 Setoid**：`projGrothRel_refl`/`_symm`/`_trans`（经
  `projGrothRel_iff` 把酉等价差对关系降为秩层 ℕ 加法等式，复用 §2.20 `GrothRel`
  的反身/对称/传递），实例化 `projGrothSetoid`——**投影差对象商类型合法存在**。
- **对象层差商类型** `ProjDiffQuot E := Quotient (projGrothSetoid E)`，设想为 K₀
  差对象 $[P]-[Q]$；`projMk E P Q` 为代表元构造。
- **秩差完全不变量（对象层分类器）** `projToInt E : ProjDiffQuot E → ℤ`：
  $[(P,Q)]\mapsto \mathrm{rank}P-\mathrm{rank}Q$——商上良定义（`Quotient.lift`，
  酉等价差对 ⟹ 秩差不变）、`projToInt_mk` 代表元计算、`projToInt_injective` 单射
  （不同差对象必有不同秩差 ⟹ 差商类被秩差唯一锁定 = 完全不变量）。
- **与秩层 Grothendieck 群交接** `projToInt_eq_grothToInt`：
  $\mathrm{projToInt}\,[P-Q]=\mathrm{grothToInt}\,[(r_P,r_Q)]$——对象层分类器经
  §2.20 `grothToInt` 因子分解嵌入 `GrothQuot ≃+ ℤ`，即对象层秩差不变量与秩层
  Grothendieck 群同一语义。
- **加性/群同态种子** `projToInt_projDirectSum_add`：分类器沿跨空间直和分解
  $[(P\oplus Q,\,P'\oplus Q')]\mapsto([P]-[P'])+([Q]-[Q'])$（经 §2.19
  `quotientRank_projDirectSum_add` 直和秩加性）——**对象层 K₀ 群同态的种子**：
  分类器作为差对象"加法"下的加性同态。

诚实边界（随登）：本层对象层闭合的是**商载体 + 秩差完全不变量（单射）**——即
「对象 = 投影酉类差对象」的分类器层。诚实的结构性区分保留：① `projToInt` 是**单射**
而非双射——对固定有限维 $E$，秩差被界于 $[-\dim E,\dim E]$，值域是 $\mathbb{Z}$ 的
有界子集，故**对象层秩差嵌入 $\mathbb{Z}$**；完整双射/群同构
`ProjDiffQuot ≃+ ℤ` 需把空间 $E$ 的维数取遍（即将差对象商沿所有有限维空间直和闭包，
即 Grothendieck 群 $\mathrm{K}_0(\mathbb{C})\cong\mathbb{Z}$ 的**跨维度并**），本模块未
实施绑定所有维度的商/直和闭包，登记开放。② 对象层**商加法构成幺半群/群**的公理
（在 `ProjDiffQuot E` 本身上定义加法并验证结合/交换/单位）未在本层逐公理构造——因对
固定有限维空间直接定义加法需要把 $[(P,Q)]+[(P',Q')]$ 翻译回同一商类型（跨空间直和
$P\oplus Q'$ 落入更大空间 $E\times E$，其差对象不在同一商类型内），故诚实的对象层群
结构经**秩差分类器单射嵌入 $\mathbb{Z}$ 的子结构**实现（`projToInt_isEmbedding` 思考路径），
而非在同一商类型上定义闭会封闭加法；完整对象层群 $\cong\mathbb{Z}$ 依赖 §2.16 自由交换群
`single_generator_freeAbelian_iso_int` 与 §2.20 `grothToIntIso` 的跨维度会师（已闭合）。
-/

section K0Object

open Module

variable {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℂ E] [FiniteDimensional ℂ E]

/-- **反身**：差对象 `a ~ a`——经 §2.20 `projGrothRel_iff` 降到秩层加法等式（自等）。 -/
theorem projGrothRel_refl (a : SelfAdjointIdemProj E × SelfAdjointIdemProj E) :
    projGrothRel a a := by
  rw [projGrothRel_iff]

/-- **对称**：`a ~ c → c ~ a`（秩层加法对称，§2.20 `GrothRel` 对称）。 -/
theorem projGrothRel_symm {a c : SelfAdjointIdemProj E × SelfAdjointIdemProj E}
    (h : projGrothRel a c) : projGrothRel c a := by
  rw [projGrothRel_iff] at h ⊢
  omega

/-- **传递**：`a ~ b ∧ b ~ c → a ~ c`（秩层 Grothendieck 关系传递，§2.20
    `GrothRel` 传递）。 -/
theorem projGrothRel_trans {a b c : SelfAdjointIdemProj E × SelfAdjointIdemProj E}
    (h₁ : projGrothRel a b) (h₂ : projGrothRel b c) : projGrothRel a c := by
  rw [projGrothRel_iff] at h₁ h₂ ⊢
  omega

/-- **对象层 Grothendieck 关系的 Setoid**（反身+对称+传递 ⟹ 可作商）——投影差对象
    商类型的合法性。 -/
instance projGrothSetoid (E : Type u) [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    [FiniteDimensional ℂ E] : Setoid (SelfAdjointIdemProj E × SelfAdjointIdemProj E) where
  r := projGrothRel
  iseqv := ⟨projGrothRel_refl, projGrothRel_symm, projGrothRel_trans⟩

/-- **对象层差对象商类型**（投影商类的 Grothendieck 差商）：元素设想为 K₀ 差对象
    $[P]-[Q]$，$P,Q$ 为自伴幂等（正交）投影。 -/
abbrev ProjDiffQuot (E : Type u) [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    [FiniteDimensional ℂ E] := Quotient (projGrothSetoid E)

-- 代表元构造：`projMk E P Q := [(P,Q)]`。
set_option linter.unusedVariables false in
abbrev projMk (E : Type u) [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    [FiniteDimensional ℂ E] (P Q : SelfAdjointIdemProj E) : ProjDiffQuot E :=
  Quotient.mk (projGrothSetoid E) (P, Q)

/-- **秩差完全不变量（对象层分类器）**：$\mathrm{projToInt}\,E\,[(P,Q)]=\mathrm{rank}P
    -\mathrm{rank}Q$，把对象层差对象商送到 $\mathbb{Z}$。商上良定义（`Quotient.lift`）：
    `projGrothRel` 经 §2.20 `projGrothRel_iff` 降到秩层加法等式 ⟹ 酉等价差对秩差不变。 -/
noncomputable def projToInt (E : Type u) [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    [FiniteDimensional ℂ E] : ProjDiffQuot E → ℤ :=
  Quotient.lift (fun a : SelfAdjointIdemProj E × SelfAdjointIdemProj E =>
    (quotientRank E (Quotient.mk (projUnitarySetoid E) a.1) : ℤ)
      - (quotientRank E (Quotient.mk (projUnitarySetoid E) a.2) : ℤ)) (by
    intro a c h
    change projGrothRel a c at h
    rw [projGrothRel_iff] at h
    have hz : (quotientRank E (Quotient.mk (projUnitarySetoid E) a.1) : ℤ)
        + (quotientRank E (Quotient.mk (projUnitarySetoid E) c.2) : ℤ) =
      (quotientRank E (Quotient.mk (projUnitarySetoid E) c.1) : ℤ)
        + (quotientRank E (Quotient.mk (projUnitarySetoid E) a.2) : ℤ) := by
      exact_mod_cast h
    omega)

/-- **`projToInt` 代表元计算**：$\mathrm{projToInt}\,E\,[(P,Q)]=\mathrm{rank}P
    -\mathrm{rank}Q$。 -/
theorem projToInt_mk (P Q : SelfAdjointIdemProj E) :
    projToInt E (Quotient.mk (projGrothSetoid E) (P, Q)) =
      (quotientRank E (Quotient.mk (projUnitarySetoid E) P) : ℤ)
        - (quotientRank E (Quotient.mk (projUnitarySetoid E) Q) : ℤ) := by
  rfl

/-- **与秩层 Grothendieck 群交接**：$\mathrm{projToInt}\,[P-Q]=\mathrm{grothToInt}\,
    [(r_P,r_Q)]$——对象层分类器经 §2.20 `grothToInt` 因子分解（`grothToInt_of_rank_diff`），
    即对象层秩差不变量与秩层 `GrothQuot ≃+ ℤ` 同一语义。 -/
theorem projToInt_eq_grothToInt (P Q : SelfAdjointIdemProj E) :
    projToInt E (projMk E P Q) = grothToInt (Quotient.mk grothSetoid
      (quotientRank E (Quotient.mk (projUnitarySetoid E) P),
       quotientRank E (Quotient.mk (projUnitarySetoid E) Q))) := by
  rw [projToInt_mk]
  exact grothToInt_of_rank_diff P Q

/-- **单射完全不变量**：不同差对象 ⟹ 不同秩差；等价地，$\mathrm{rank}P-\mathrm{rank}Q$
    相等唯一决定对象层差商类（商秩差作为单射分类器）。 -/
theorem projToInt_injective : Function.Injective (projToInt E) := by
  rintro ⟨a⟩ ⟨c⟩ h
  apply Quotient.sound
  change projGrothRel a c
  rw [projGrothRel_iff]
  have hg : grothToInt (Quotient.mk grothSetoid
        (quotientRank E (Quotient.mk (projUnitarySetoid E) a.1),
         quotientRank E (Quotient.mk (projUnitarySetoid E) a.2))) =
      grothToInt (Quotient.mk grothSetoid
        (quotientRank E (Quotient.mk (projUnitarySetoid E) c.1),
         quotientRank E (Quotient.mk (projUnitarySetoid E) c.2))) := by
    rw [← projToInt_eq_grothToInt a.1 a.2, ← projToInt_eq_grothToInt c.1 c.2]
    change projToInt E (Quotient.mk (projGrothSetoid E) (a.1, a.2)) =
      projToInt E (Quotient.mk (projGrothSetoid E) (c.1, c.2))
    exact h
  have hG : GrothRel (quotientRank E (Quotient.mk (projUnitarySetoid E) a.1),
                       quotientRank E (Quotient.mk (projUnitarySetoid E) a.2))
      (quotientRank E (Quotient.mk (projUnitarySetoid E) c.1),
       quotientRank E (Quotient.mk (projUnitarySetoid E) c.2)) :=
    Quotient.exact (grothToInt_injective hg)
  simpa [GrothRel] using hG

end K0Object

/-! ### 对象层加性：秩差分类器沿跨空间直和分解（K₀ 群同态的种子） -/

section K0ObjectAdd

open Module

variable {E F : Type u} [NormedAddCommGroup E] [InnerProductSpace ℂ E] [FiniteDimensional ℂ E]
  [NormedAddCommGroup F] [InnerProductSpace ℂ F] [FiniteDimensional ℂ F]

/-- **对象层秩差分类器的直和加性**：$\mathrm{projToInt}\,[(P\oplus Q,\,P'\oplus Q')]
    =([P]-[P'])+([Q]-[Q'])$——把 §2.19 的 `quotientRank_projDirectSum_add`（商秩直和加性）
    提升为对象层 K₀ 群同态的种子：分类器沿跨空间直和是加性同态。 -/
theorem projToInt_projDirectSum_add (P P' : SelfAdjointIdemProj E) (Q Q' : SelfAdjointIdemProj F) :
    projToInt (WithLp 2 (E × F)) (Quotient.mk (projGrothSetoid (WithLp 2 (E × F)))
      (projDirectSum P Q, projDirectSum P' Q')) =
      projToInt E (projMk E P P') + projToInt F (projMk F Q Q') := by
  rw [projToInt_mk (E := WithLp 2 (E × F)) (projDirectSum P Q) (projDirectSum P' Q'),
      projToInt_mk (E := E) P P', projToInt_mk (E := F) Q Q']
  rw [quotientRank_projDirectSum_add P Q, quotientRank_projDirectSum_add P' Q']
  omega

end K0ObjectAdd

/-!
## §2.22 对象层分类器的精确值域：各秩投影的可实现性 + 像恰为有界整数区间（跨维度闭会展碍的显式演示）

承接 §2.21 诚实边界①：`projToInt` 是把差对象商**单射嵌入 $\mathbb{Z}$ 的有界子结构**
（固定有限维 $E$，秩差被界于 $[-\dim E,\dim E]$）而非双射。本层把这条有界单射的**值域**
精确刻画出来，并显式演示"为何它只是有界区间、而非 $\mathbb{Z}$ 的加法子幺半群"：

- **各秩投影可实现** `projOfRank`：对每个秩 $k\le\dim E$，用标准正交基
  $\{e_0,\dots,e_{\dim E-1}\}$ 的前 $k$ 个张成子空间 $U_k$，其正交投影
  $U_k.\mathrm{starProjection}$ 幂等且自伴（`isSymmetricProjection_starProjection`），
  落在 `SelfAdjointIdemProj E`；且 $U_k$ 由前 $k$ 个标准正交基向量张成
  （`finrank_span_eq_card` + 线性无关），故 $\mathrm{rank}\,P_k=k$。
- **秩恰为 $k$ 的证明** `projOfRank_rankE`：$\mathrm{rank}\,P_k=\operatorname{finrank} E= k$。
- **整数值可达（分类器满射到区间）**：对任意 $r\in[-\dim E,\dim E]\cap\mathbb{Z}$，存在
  差对象 $[P]-[Q]$ 使 $\mathrm{projToInt}=r$：$r\ge0$ 取 $P$=秩 $r$ 投影、$Q$=零投影；
  $r<0$ 取 $P$=零投影、$Q$=秩 $(-r)$ 投影。⟹ 精确值域底座。
- **值域恰为有界区间** `projToInt_range_Icc`：$\mathrm{range}\,(\mathrm{projToInt}\,E)
  =\{r\in\mathbb{Z}\mid -\alpha\le r\le\alpha\}$，其中 $\alpha=\dim E$。左包含由
  `quotientRank_le_dim`（秩 $\le\dim E$）与非负性；右包含由整数值可达。
- **闭会展碍 / 非加法子幺半群** `projToInt_range_not_submonoid`：存在 $a,b$ 都在像中而
  $a+b$ 不在像中（如 $a=b=\alpha$，则 $2\alpha\notin[-\alpha,\alpha]$，当 $\alpha\ge1$）⟹
  像**不是 $\mathbb{Z}$ 的加法子幺半群**——这是跨维度直和闭包（Grothendieck 群完成）的
  必要性所在：固定空间内差对象加法无法封闭，须把所有有限维空间沿直和取并。

诚实边界（随登）：本层闭合的是**值域精确刻画 + 各秩投影可实现性**——即 `projToInt` 的
像**如实等于** $[-\dim E,\dim E]\cap\mathbb{Z}$，从而 `projToInt` 是**到有界区间的双射**，
其像作为 $\mathbb{Z}$ 子集**非加法子幺半群**（闭会展碍）。仍登记开放：① 把投影商类本身构成
跨空间直和闭包下的**完整对象层群** $\mathrm{ProjDiffQuot}\cong\mathbb{Z}$（本层只演示
单空间闭会展碍，未构造沿所有有限维空间的直和并集）；② 对象层商加法在**同一商类型**上
逐公理构成幺半群/群（§2.21 诚实边界②，须把差对象加法翻译回同类型，闭会展碍使单空间不可行）；
③ $U(n)$ 酉群/同伦类与秩一一对应。
-/

section K0Range

open Module

variable {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℂ E] [FiniteDimensional ℂ E]

/-- **各秩投影的可实现性**：对 $k\le\dim E$，取标准正交基前 $k$ 个基向量张成的子空间
    $U_k$，其正交投影 $U_k.\mathrm{starProjection}$ 幂等且自伴 ⟹ 落在 `SelfAdjointIdemProj E`。 -/
noncomputable def projOfRank (k : ℕ) (hk : k ≤ Module.finrank ℂ E) : SelfAdjointIdemProj E := by
  let U : Submodule ℂ E := Submodule.span ℂ
    (Set.range (fun i : Fin k => (stdOrthonormalBasis ℂ E) (Fin.castLE hk i)))
  refine ⟨(U.starProjection : E →ₗ[ℂ] E), ?_, ?_⟩
  · exact (Submodule.isSymmetricProjection_starProjection U).isIdempotentElem
  · exact (Submodule.isSymmetricProjection_starProjection U).isSymmetric

/-- **每种秩的投影存在且秩恰为 $k$**：$U_k$ 由前 $k$ 个标准正交基向量张成，故
    $\operatorname{finrank} U_k=k$（标准正交基诱导线性无关，`finrank_span_eq_card`）；
    `starProjection` 的像即 $U_k$（`range_starProjection`）。 -/
theorem projOfRank_rankE (k : ℕ) (hk : k ≤ Module.finrank ℂ E) :
    Module.finrank ℂ (LinearMap.range (projOfRank k hk).1) = k := by
  let U : Submodule ℂ E := Submodule.span ℂ
    (Set.range (fun i : Fin k => (stdOrthonormalBasis ℂ E) (Fin.castLE hk i)))
  change Module.finrank ℂ (LinearMap.range (U.starProjection : E →ₗ[ℂ] E)) = k
  rw [U.range_starProjection]
  dsimp [U, projOfRank]
  let b : OrthonormalBasis (Fin (Module.finrank ℂ E)) ℂ E := stdOrthonormalBasis ℂ E
  have hb : LinearIndependent ℂ (b : Fin (Module.finrank ℂ E) → E) := by
    simpa using b.toBasis.linearIndependent
  have hlin : LinearIndependent ℂ (⇑b ∘ Fin.castLE hk : Fin k → E) :=
    hb.comp (Fin.castLE hk) (Fin.castLE_injective hk)
  have hc : Module.finrank ℂ (Submodule.span ℂ (Set.range (⇑b ∘ Fin.castLE hk))) = k := by
    simpa using (finrank_span_eq_card (R := ℂ) (b := (⇑b ∘ Fin.castLE hk : Fin k → E)) hlin)
  change Module.finrank ℂ (Submodule.span ℂ (Set.range (⇑b ∘ Fin.castLE hk))) = k
  exact hc

/-- **秩在商上的取值**：商秩 `quotientRank` 对 `projOfRank k` 取恰为 $k$。 -/
theorem projOfRank_rank (k : ℕ) (hk : k ≤ Module.finrank ℂ E) :
    quotientRank E (Quotient.mk (projUnitarySetoid E) (projOfRank k hk)) = k := by
  change Module.finrank ℂ (LinearMap.range (projOfRank k hk).1) = k
  exact projOfRank_rankE k hk

/-- **零投影（秩 0）**：各秩投影中 $k=0$ 者，即空张成 $\bot$ 的正交投影（零映射）。 -/
theorem projZero_rank :
    quotientRank E (Quotient.mk (projUnitarySetoid E) (projOfRank 0 (Nat.zero_le _))) = 0 := by
  exact projOfRank_rank 0 (Nat.zero_le _)

/-- **非负整数值可达**：对每个 $k\le\dim E$，差对象 $[\mathbb{C}^k]-[0]$ 的秩差
    $\mathrm{projToInt}$ 恰为 $k$（正像：秩 $k$ 投影 − 零投影）。 -/
theorem projToInt_reaches_nat (k : ℕ) (hk : k ≤ Module.finrank ℂ E) :
    projToInt E (projMk E (projOfRank k hk) (projOfRank 0 (Nat.zero_le _))) = (k : ℤ) := by
  rw [projToInt_mk]
  rw [projOfRank_rank, projZero_rank]
  norm_num

/-- **负整数值可达**：对每个 $k\le\dim E$，差对象 $[0]-[\mathbb{C}^k]$ 的秩差
    $\mathrm{projToInt}$ 恰为 $-k$（负像：零投影 − 秩 $k$ 投影）。 -/
theorem projToInt_reaches_neg (k : ℕ) (hk : k ≤ Module.finrank ℂ E) :
    projToInt E (projMk E (projOfRank 0 (Nat.zero_le _)) (projOfRank k hk)) = (-(k : ℤ)) := by
  rw [projToInt_mk]
  rw [projZero_rank, projOfRank_rank]
  norm_num

/-- **秩差分类器值域上界**：对任意差对象 $\mathrm{projToInt}\,E\,y$，其值被界于
    $[-\dim E,\dim E]$（因其为两枚秩各被界于 $[0,\dim E]$ 的投影之差：
    $0\le\mathrm{rank}\,P,\mathrm{rank}\,Q\le\dim E$）。 -/
lemma projToInt_mem_range_Icc {y : ProjDiffQuot E} :
    -(Module.finrank ℂ E : ℤ) ≤ projToInt E y ∧ projToInt E y ≤ (Module.finrank ℂ E : ℤ) := by
  refine Quotient.inductionOn y ?_
  rintro ⟨P, Q⟩
  let rP : ℕ := quotientRank E (Quotient.mk (projUnitarySetoid E) P)
  let rQ : ℕ := quotientRank E (Quotient.mk (projUnitarySetoid E) Q)
  rw [projToInt_mk P Q]
  have hrP_le : (rP : ℤ) ≤ (Module.finrank ℂ E : ℤ) := by
    exact_mod_cast quotientRank_le_dim P
  have hrQ_le : (rQ : ℤ) ≤ (Module.finrank ℂ E : ℤ) := by
    exact_mod_cast quotientRank_le_dim Q
  have hrP_nonneg : (0 : ℤ) ≤ (rP : ℤ) := by exact_mod_cast Nat.zero_le rP
  have hrQ_nonneg : (0 : ℤ) ≤ (rQ : ℤ) := by exact_mod_cast Nat.zero_le rQ
  constructor <;> omega

/-- **值域恰为有界整数区间**：$\mathrm{range}\,(\mathrm{projToInt}\,E)=\{r\in\mathbb{Z}
    \mid -\alpha\le r\le\alpha\}$，其中 $\alpha=\dim E$。左包含（$\subseteq$）由
    `projToInt_mem_range_Icc`（秩界于 $[0,\dim E]$ ⟹ 秩差界于 $[-\dim E,\dim E]$）；
    右包含（$\supseteq$）对 $r\ge 0$ 与 $r<0$ 分正负，分别用 `projToInt_reaches_nat`
    与 `projToInt_reaches_neg` 构造实现投影对。⟹ `projToInt` 是**到有界区间的双射**
    （满射由本定理，单射由 §2.21 `projToInt_injective`）。 -/
theorem projToInt_range_Icc :
    Set.range (projToInt E) =
      {r : ℤ | -(Module.finrank ℂ E : ℤ) ≤ r ∧ r ≤ (Module.finrank ℂ E : ℤ)} := by
  ext r
  constructor
  · rintro ⟨y, hy⟩
    rw [← hy]
    exact projToInt_mem_range_Icc (E := E) (y := y)
  · intro h
    have hlo : -(Module.finrank ℂ E : ℤ) ≤ r := h.1
    have hhi : r ≤ (Module.finrank ℂ E : ℤ) := h.2
    by_cases hr : 0 ≤ r
    · have hk_toNat : (r.toNat : ℤ) ≤ (Module.finrank ℂ E : ℤ) := by
        simpa [Int.toNat_of_nonneg hr] using hhi
      have hk : r.toNat ≤ Module.finrank ℂ E := by exact_mod_cast hk_toNat
      have fr : (r.toNat : ℤ) = r := Int.toNat_of_nonneg hr
      refine ⟨projMk E (projOfRank r.toNat hk) (projOfRank 0 (Nat.zero_le _)), ?_⟩
      exact (projToInt_reaches_nat r.toNat hk).trans fr
    · have hnr : 0 ≤ -r := by omega
      have hm : -r ≤ (Module.finrank ℂ E : ℤ) := by omega
      have hk_toNat : ((-r).toNat : ℤ) ≤ (Module.finrank ℂ E : ℤ) := by
        simpa [Int.toNat_of_nonneg hnr] using hm
      have hk : (-r).toNat ≤ Module.finrank ℂ E := by exact_mod_cast hk_toNat
      have fr : -((-r).toNat : ℤ) = r := by
        rw [Int.toNat_of_nonneg hnr]
        exact neg_neg r
      refine ⟨projMk E (projOfRank 0 (Nat.zero_le _)) (projOfRank (-r).toNat hk), ?_⟩
      exact (projToInt_reaches_neg (-r).toNat hk).trans fr

/-- **像非 $\mathbb{Z}$ 加法子幺半群（闭会展碍）**：存在 $a,b$ 都在像中而 $a+b$ 不在像
    （取 $a=b=\alpha$，则 $2\alpha\notin[-\alpha,\alpha]$，当 $\dim E\ge1$）⟹ 像**不是
    $\mathbb{Z}$ 的加法子幺半群**——固定空间内差对象加法无法在值域内封闭（跨维度直和
    闭包 / Grothendieck 群完成的必要性所在）。 -/
theorem projToInt_range_not_submonoid (hdim : 1 ≤ Module.finrank ℂ E) :
    ∃ a b : ℤ, a ∈ Set.range (projToInt E) ∧ b ∈ Set.range (projToInt E)
      ∧ a + b ∉ Set.range (projToInt E) := by
  let α : ℤ := (Module.finrank ℂ E : ℤ)
  refine ⟨α, α, ?_, ?_, ?_⟩
  · dsimp [α]
    rw [Set.mem_range]
    exact ⟨projMk E (projOfRank (Module.finrank ℂ E) le_rfl)
      (projOfRank 0 (Nat.zero_le _)), projToInt_reaches_nat (Module.finrank ℂ E) le_rfl⟩
  · dsimp [α]
    rw [Set.mem_range]
    exact ⟨projMk E (projOfRank (Module.finrank ℂ E) le_rfl)
      (projOfRank 0 (Nat.zero_le _)), projToInt_reaches_nat (Module.finrank ℂ E) le_rfl⟩
  · dsimp [α]
    rw [Set.mem_range]
    intro herr
    rcases herr with ⟨y, hy⟩
    have hb := projToInt_mem_range_Icc (E := E) (y := y)
    rw [hy] at hb
    have ha : (1 : ℤ) ≤ (Module.finrank ℂ E : ℤ) := by exact_mod_cast hdim
    omega

end K0Range

/-!
## §2.23 跨维度标准实现：K₀(ℂ)≅ℤ 的秩-1 生成与整体群同构（对象层分组基座）

§3 #7「同秩投影酉等价（K₀ = ℤ）」G3 第三块（完整对象层 K₀ ≅ ℤ 的收口基座）。
§2.21 把投影差对象商 `ProjDiffQuot E` 配秩差完全不变量 `projToInt E : ProjDiffQuot E → ℤ`
（单射嵌入 $[-\dim E,\dim E]$），§2.22 证 `projToInt` 的像**恰为** $[-\dim E,\dim E]\cap\mathbb{Z}$
（到有界区间的双射），并演示像**非**加法子幺半群（`2\alpha\notin[-\alpha,\alpha]$`）——固定单空间
的商加法不封闭，正因对象层完整群结构必须**跨维度直和闭包**。本层把"维数取遍"落成显式构造：
`EuclideanSpace ℂ (Fin n)` 作跨维度标准空间，证明 **各秩投影类跨维度可同时实现**、**每个整数
（不论多大多小）都能被某维数空间的投影类实现**（跨维度满射到 ℤ）、**秩-1 类 $[\mathbb{C}^1]$
生成整个 Grothendieck 群**（每个类都是 $(k,\cdot)$ 到秩-1 类的 $\mathbb{Z}$ 倍），并给出对象层
分类器与秩的直接等式 `projToInt E [P,0] = rank P`。这三点配合 §2.16（`FreeAbelianGroup PUnit ≃+ ℤ`）、
§2.20（`grothToIntIso : GrothQuot ≃+ ℤ`）、§2.21 `projToInt_eq_grothToInt`（投影类经秩因子嵌入
$\mathbb{Z}$）把「对象层投影类 = 秩 = $\mathbb{Z}$」的跨维度分组/生成与整体同构落成可计算基建。
诚实边界（随登）：闭合的是**秩层的跨维度分组基底**（秩-1 生成 + 跨维度满射 + 分类器=秩），
即"整体秩是 $\mathbb{Z}$ 双射：跨维度单射（§2.21）+ 本层跨维度满射 + 加法（§2.19 直和秩加性）"；
对象层**同一商类型的完整 `AddCommGroup` 结构**（$U(n)$ 酉群/同伦类与秩一一对应、投影类的
Grothendieck 群 ≅ ℤ 作为对象层双射到整个 $\mathbb{Z}$ 的显式同构）仍登记开放。
-/

section K0Canonical

open scoped Int

variable {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℂ E] [FiniteDimensional ℂ E]

/-- **跨维度标准 n 维空间**：取 `EuclideanSpace ℂ (Fin n)`（= `PiLp 2 (Fin n → ℂ)`）
    作各秩投影的标准实现载体——正是 §2.22 各秩投影 `projOfRank` 构造的跨维度版本基座。
    每个可数维数都有此标准空间，从而把"维数取遍"落成显式可达。 -/
abbrev canonicalSpace (n : ℕ) := EuclideanSpace ℂ (Fin n)

/-- **标准空间的确切维数**：$\operatorname{finrank}_{\mathbb{C}}(\mathbb{C}^n)=n$。 -/
lemma canonicalSpace_finrank (n : ℕ) : Module.finrank ℂ (canonicalSpace n) = n := by
  simp [canonicalSpace, EuclideanSpace]

/-- **秩-1 规范投影的类取 1（生成元 $[\mathbb{C}^1]\mapsto 1$）**：一维标准空间上的
    秩-1 投影类 $\mathbb{C}^1$ 在分类器下映到 $1\in\mathbb{Z}$。 -/
theorem rankOne_class_projToInt :
    projToInt (canonicalSpace 1)
      (projMk (canonicalSpace 1)
        (projOfRank 1 (by rw [canonicalSpace_finrank])) (projOfRank 0 (Nat.zero_le _))) = 1 := by
  exact projToInt_reaches_nat 1 (by rw [canonicalSpace_finrank])

/-- **秩-1 类不依赖维数：任何 $\ge1$ 维空间的秩-1 投影类秩差都是 1**（跨维度一致，
    是"所有 $\mathbb{C}^1$ 同构类一致"在分类器层的体现）。 -/
theorem rankOne_class_any_dim (n : ℕ) (hn : 1 ≤ n) :
    projToInt (canonicalSpace n)
      (projMk (canonicalSpace n)
        (projOfRank 1 (by rw [canonicalSpace_finrank]; omega))
        (projOfRank 0 (Nat.zero_le _))) = 1 := by
  exact projToInt_reaches_nat 1 (by rw [canonicalSpace_finrank]; omega)

/-- **跨维度满射：每个整数都是某维数标准空间上投影类的秩差**（整体秩分类映满 $\mathbb{Z}$）。
    §2.22 单空间像界于 $[-\dim E,\dim E]$；这里把维数取遍（$r\ge0$ 取 $\mathbb{C}^r$、
    $r<0$ 取 $\mathbb{C}^{-r}$），每个整数都能被实现——配合 §2.21 `projToInt` 单射，
    是"跨维度整体秩是 $\mathbb{Z}$ 双射"的满射一半。 -/
theorem crossDim_reaches_any (r : ℤ) :
    ∃ n : ℕ, ∃ P Q : SelfAdjointIdemProj (canonicalSpace n),
      projToInt (canonicalSpace n) (projMk (canonicalSpace n) P Q) = r := by
  by_cases hr : 0 ≤ r
  · let k : ℕ := r.toNat
    have hk_le : k ≤ Module.finrank ℂ (canonicalSpace k) := by rw [canonicalSpace_finrank]
    refine ⟨k, projOfRank k hk_le, projOfRank 0 (Nat.zero_le _), ?_⟩
    have hkz : (k : ℤ) = r := by
      simpa [k] using Int.toNat_of_nonneg hr
    simpa [hkz] using projToInt_reaches_nat k hk_le
  · let k : ℕ := (-r).toNat
    have hk_le : k ≤ Module.finrank ℂ (canonicalSpace k) := by rw [canonicalSpace_finrank]
    refine ⟨k, projOfRank 0 (Nat.zero_le _), projOfRank k hk_le, ?_⟩
    have hnr : 0 ≤ -r := by omega
    have hkz : (k : ℤ) = -r := by
      simpa [k] using Int.toNat_of_nonneg hnr
    have fr : -(k : ℤ) = r := by
      rw [hkz]
      exact neg_neg r
    simpa [fr] using projToInt_reaches_neg k hk_le

/-- **秩-1 类在 Grothendieck 群 `GrothQuot` 中的代表元** $[(1,0)]$：生成元 $[\mathbb{C}^1]$。 -/
def grothOneClass : GrothQuot := Quotient.mk grothSetoid (1, 0)

/-- **生成元类的秩差 = 1**：$[(1,0)]\mapsto 1$。 -/
lemma grothToInt_grothOneClass : grothToInt grothOneClass = 1 := by
  rw [grothOneClass, grothToInt_mk]
  norm_num

/-- `grothToIntIso` 作为函数就是 `grothToInt`（`AddEquiv.ofBijective` 包装）。 -/
lemma grothToIntIso_apply (x : GrothQuot) : grothToIntIso x = grothToInt x := by
  rfl

/-- **整体生成：K₀(ℂ) 由秩-1 类 $[\mathbb{C}^1]$ 生成**——每个 Grothendieck 类都是
    秩-1 类的 $\mathbb{Z}$ 倍（在 ℤ 加群上 $k\cdot[\mathbb{C}^1]=[(k,0)]$）。这是
    `K₀(ℂ)\cong\mathbb{Z}` 的**生成元层**真语句：一切投影类都在秩-1 类的整倍中。 -/
theorem grothQuot_generated_by_one (x : GrothQuot) : ∃ n : ℤ, x = n • grothOneClass := by
  let r : ℤ := grothToInt x
  refine ⟨r, ?_⟩
  apply grothToIntIso.injective
  rw [map_zsmul]
  have hg : grothToIntIso grothOneClass = 1 := by
    rw [grothToIntIso_apply]
    exact grothToInt_grothOneClass
  have hx : grothToIntIso x = r := by
    rw [grothToIntIso_apply]
  rw [hg, hx]
  simp

/-- **对象层分类器即秩**：$\mathrm{projToInt}\,E\,[P,0]=\operatorname{rank}P$——对象层
    差对象商在分类器下恰映到其差秩（跨维度 K₀ ≅ ℤ 中即 `rank P · [ℂ¹]` 的秩分量）。 -/
theorem projClass_int_eq_rank (P : SelfAdjointIdemProj E) :
    projToInt E (projMk E P (projOfRank 0 (Nat.zero_le _))) =
      (Module.finrank ℂ (LinearMap.range (P.1 : E →ₗ[ℂ] E)) : ℤ) := by
  rw [projToInt_mk]
  have hP : quotientRank E (Quotient.mk (projUnitarySetoid E) P) =
      Module.finrank ℂ (LinearMap.range (P.1 : E →ₗ[ℂ] E)) := by
    rw [quotientRank, Quotient.lift_mk]
  have hQ : quotientRank E (Quotient.mk (projUnitarySetoid E) (projOfRank 0 (Nat.zero_le _))) = 0 :=
    projOfRank_rank 0 (Nat.zero_le _)
  rw [hP, hQ]
  simp

end K0Canonical

/-!
## §2.24 对象层 K₀ 群：跨维度直和闭包下的 `ProjClass ≃+ ℤ`（对象层完整群同构）

§3 #7「同秩投影酉等价（K₀ = ℤ）」G3 第四块（**完整对象层 K₀ ≅ ℤ 的收口**）。
§2.21 把投影差对象商 `ProjDiffQuot E` 配秩差完全不变量 `projToInt`（单射嵌入），§2.22 证其像
**恰为** $[-\dim E,\dim E]\cap\mathbb{Z}$（到有界区间的双射）并演示闭会展碍，§2.23 给出跨维度
满射到 $\mathbb{Z}$ 与秩-1 生成。本层把"维数取遍"从**分类器层**推进到**对象层群结构**：
以 `EuclideanSpace ℂ (Fin n)` 的跨维度和型等距 `canonicalSpaceAddIso`（`ℂ^{n+m} ≃ₗᵢ ℂ^n × ℂ^m`，
经 `PiLp.sumPiLpEquivProdLpPiLp` + `finSumFinEquiv`）把 §2.19 的直和投影搬回规范空间
（`projDirectSumCanon`，沿等距共轭 `conjProj`，幂等 + 自伴 + 保秩），从而在**跨维度对象层载体**
`ProjPoint = Σ n, ProjDiffQuot (ℂ^n)` 上定义**由直和诱导的加法** `+`，证明整体秩分类器
`projPointRank` 沿该加法**加性**（`projPointRank_add`，经 §2.19 `quotientRank_projDirectSum_add`）。
再按秩相等作商得**对象层 K₀ 类** `ProjClass`，证 `projClassRank : ProjClass ≃ ℤ`（单射 + 满射，
满射用 §2.23 `crossDim_reaches_any`），并**从 ℤ 传送群结构**（`projClassAddCommGroup`，
`Function.Injective.addCommGroup`）得**对象层群同构** `projClassRankIso : ProjClass ≃+ ℤ`。
关键**自然性**定理 `projClassMk_add`：类加法**恰由跨维度直和实现**——`[a] + [b] = [a ⊕ b]`，
即 §2.20 秩层 Grothendieck 群 `GrothQuot ≃+ ℤ` 在**对象层的显式实现**。
诚实边界（随登）：闭合的是**对象层群结构 ≅ ℤ**（载体 + 直和诱导加法 + 群公理 + 与 ℤ 的群同构 +
类加法即直和的自然性）；仍登记开放：① $U(n)$ 酉群/同伦类与秩一一对应（把逐对双射提升到
群结构层）；② 环面上陈数密度 $F$ 的连续场论/度理论整性（含同伦提升，§3 #4）。
-/

section K0ClassGroup

open scoped Int

/-- **跨维度和型等距**：$\mathbb{C}^{n+m}\simeq_{\mathbb{C}}\mathbb{C}^n\times\mathbb{C}^m$
    作为内积空间（等距）。经 `LinearIsometryEquiv.piLpCongrLeft`（指标重排）+ mathlib
    `PiLp.sumPiLpEquivProdLpPiLp`（`PiLp` 和型的等距分解，右端为 L²-乘积 `WithLp 2`）复合。 -/
noncomputable def canonicalSpaceAddIso (n m : ℕ) :
    canonicalSpace (n + m) ≃ₗᵢ[ℂ] WithLp 2 (canonicalSpace n × canonicalSpace m) :=
  (LinearIsometryEquiv.piLpCongrLeft 2 ℂ ℂ (finSumFinEquiv).symm).trans
    (PiLp.sumPiLpEquivProdLpPiLp 2 (fun _ : Fin n ⊕ Fin m => ℂ))

/-- **沿线性等距共轭投影**：`P ↦ e ∘ P ∘ e⁻¹` 仍自伴幂等（幂等由复合消约 + `P` 幂等，
    自伴由 `LinearMap.isSymmetric_linearIsometryEquiv_conj_iff`）——把投影在等距同构的空间间搬运。 -/
noncomputable def conjProj {X Y : Type} [NormedAddCommGroup X] [InnerProductSpace ℂ X]
    [NormedAddCommGroup Y] [InnerProductSpace ℂ Y]
    (e : X ≃ₗᵢ[ℂ] Y) (P : SelfAdjointIdemProj X) : SelfAdjointIdemProj Y :=
  ⟨(e.toLinearMap.comp P.1).comp e.symm.toLinearMap, by
     rw [IsIdempotentElem, Module.End.mul_eq_comp]
     ext y
     change e (P.1 (e.symm (e (P.1 (e.symm y))))) = e (P.1 (e.symm y))
     rw [LinearIsometryEquiv.symm_apply_apply]
     congr 1
     have h : P.1 * P.1 = P.1 := P.2.1
     have h2 := congrArg (fun f : X →ₗ[ℂ] X => f (e.symm y)) h
     simpa only [Module.End.mul_eq_comp, LinearMap.comp_apply] using h2,
   (LinearMap.isSymmetric_linearIsometryEquiv_conj_iff P.1 e).mpr P.2.2⟩

/-- **共轭保秩**：`rank (e P e⁻¹) = rank P`（像集为 `(range P).map e`，线性等距保 finrank）。 -/
theorem conjProj_rank {X Y : Type} [NormedAddCommGroup X] [InnerProductSpace ℂ X]
    [FiniteDimensional ℂ X] [NormedAddCommGroup Y] [InnerProductSpace ℂ Y]
    [FiniteDimensional ℂ Y] (e : X ≃ₗᵢ[ℂ] Y) (P : SelfAdjointIdemProj X) :
    Module.finrank ℂ (LinearMap.range (conjProj e P).1) =
      Module.finrank ℂ (LinearMap.range P.1) := by
  show Module.finrank ℂ (LinearMap.range ((e.toLinearMap.comp P.1).comp e.symm.toLinearMap)) =
    Module.finrank ℂ (LinearMap.range P.1)
  rw [LinearMap.range_comp,
    LinearMap.range_eq_top.mpr e.symm.surjective, Submodule.map_top,
    LinearMap.range_comp]
  exact LinearEquiv.finrank_map_eq e.toLinearEquiv _

/-- **规范空间上的跨维度直和投影**：把 §2.19 的 `projDirectSum`（落在 `WithLp 2 (E×F)`）
    沿 `canonicalSpaceAddIso` 搬回规范空间 $\mathbb{C}^{n+m}$。 -/
noncomputable def projDirectSumCanon {n m : ℕ}
    (P : SelfAdjointIdemProj (canonicalSpace n)) (Q : SelfAdjointIdemProj (canonicalSpace m)) :
    SelfAdjointIdemProj (canonicalSpace (n + m)) :=
  conjProj (canonicalSpaceAddIso n m).symm (projDirectSum P Q)

/-- **规范直和投影的秩 = 分量秩之和**（共轭保秩 + §2.19 直和秩加性）。 -/
theorem projDirectSumCanon_rank {n m : ℕ}
    (P : SelfAdjointIdemProj (canonicalSpace n)) (Q : SelfAdjointIdemProj (canonicalSpace m)) :
    Module.finrank ℂ (LinearMap.range (projDirectSumCanon P Q).1) =
      Module.finrank ℂ (LinearMap.range (projDirectSum P Q).1) :=
  conjProj_rank (canonicalSpaceAddIso n m).symm (projDirectSum P Q)

/-- **对象层分类器沿规范跨维度直和的加性**：
    $\mathrm{projToInt}\,[(P\oplus Q)-(P'\oplus Q')]=([P]-[P'])+([Q]-[Q'])$
    （共轭保秩把规范直和拉回 §2.19 `quotientRank_projDirectSum_add`）。 -/
theorem projToInt_projDirectSumCanon_add {n m : ℕ}
    (P P' : SelfAdjointIdemProj (canonicalSpace n))
    (Q Q' : SelfAdjointIdemProj (canonicalSpace m)) :
    projToInt (canonicalSpace (n + m))
        (projMk (canonicalSpace (n + m))
          (projDirectSumCanon P Q) (projDirectSumCanon P' Q')) =
      projToInt (canonicalSpace n) (projMk (canonicalSpace n) P P') +
        projToInt (canonicalSpace m) (projMk (canonicalSpace m) Q Q') := by
  rw [projToInt_mk, projToInt_mk, projToInt_mk]
  have h1 : quotientRank (canonicalSpace (n + m))
        (Quotient.mk (projUnitarySetoid (canonicalSpace (n + m))) (projDirectSumCanon P Q)) =
      quotientRank (WithLp 2 (canonicalSpace n × canonicalSpace m))
        (Quotient.mk (projUnitarySetoid (WithLp 2 (canonicalSpace n × canonicalSpace m)))
          (projDirectSum P Q)) := by
    rw [quotientRank, quotientRank, Quotient.lift_mk, Quotient.lift_mk]
    exact projDirectSumCanon_rank P Q
  have h2 : quotientRank (canonicalSpace (n + m))
        (Quotient.mk (projUnitarySetoid (canonicalSpace (n + m))) (projDirectSumCanon P' Q')) =
      quotientRank (WithLp 2 (canonicalSpace n × canonicalSpace m))
        (Quotient.mk (projUnitarySetoid (WithLp 2 (canonicalSpace n × canonicalSpace m)))
          (projDirectSum P' Q')) := by
    rw [quotientRank, quotientRank, Quotient.lift_mk, Quotient.lift_mk]
    exact projDirectSumCanon_rank P' Q'
  rw [h1, h2, quotientRank_projDirectSum_add P Q, quotientRank_projDirectSum_add P' Q']
  omega

/-- **跨维度对象层 K₀ 载体**：各维数标准空间上投影差类的不交并 $\bigsqcup_n \mathrm{ProjDiffQuot}\,\mathbb{C}^n$。 -/
abbrev ProjPoint := Σ n : ℕ, ProjDiffQuot (canonicalSpace n)

/-- **整体秩分类器**：$\mathrm{ProjPoint}\to\mathbb{Z}$，取所在空间的秩差。 -/
noncomputable def projPointRank (a : ProjPoint) : ℤ := projToInt (canonicalSpace a.1) a.2

/-- **对象层差类的跨维度直和**（双重商 `Quotient.lift₂` 良定：经 `projToInt` 单射 + 直和加性）。 -/
noncomputable def projDiffSumCanon {n m : ℕ} (x : ProjDiffQuot (canonicalSpace n))
    (y : ProjDiffQuot (canonicalSpace m)) : ProjDiffQuot (canonicalSpace (n + m)) :=
  Quotient.lift₂
    (fun (p : SelfAdjointIdemProj (canonicalSpace n) × SelfAdjointIdemProj (canonicalSpace n))
         (q : SelfAdjointIdemProj (canonicalSpace m) × SelfAdjointIdemProj (canonicalSpace m)) =>
      projMk (canonicalSpace (n + m))
        (projDirectSumCanon p.1 q.1) (projDirectSumCanon p.2 q.2))
    (by
      intro p q p' q' hp hq
      apply projToInt_injective
      rw [projToInt_projDirectSumCanon_add, projToInt_projDirectSumCanon_add]
      have hp' : projMk (canonicalSpace n) p.1 p.2 =
          projMk (canonicalSpace n) p'.1 p'.2 := by
        simpa [projMk] using Quotient.sound hp
      have hq' : projMk (canonicalSpace m) q.1 q.2 =
          projMk (canonicalSpace m) q'.1 q'.2 := by
        simpa [projMk] using Quotient.sound hq
      rw [hp', hq'])
    x y

/-- **直和在代表元上的计算**（`Quotient.lift₂` 计算规则）。 -/
theorem projDiffSumCanon_mk {n m : ℕ} (P P' : SelfAdjointIdemProj (canonicalSpace n))
    (Q Q' : SelfAdjointIdemProj (canonicalSpace m)) :
    projDiffSumCanon (projMk (canonicalSpace n) P P') (projMk (canonicalSpace m) Q Q') =
      projMk (canonicalSpace (n + m))
        (projDirectSumCanon P Q) (projDirectSumCanon P' Q') :=
  rfl

/-- **对象层 K₀ 载体上的加法**（跨维度直和，维数相加）。 -/
noncomputable instance : Add ProjPoint where
  add a b := ⟨a.1 + b.1, projDiffSumCanon a.2 b.2⟩

/-- **整体秩分类器沿跨维度直和加性**：$\mathrm{projPointRank}(a+b)=\mathrm{projPointRank}\,a+\mathrm{projPointRank}\,b$。 -/
theorem projPointRank_add (a b : ProjPoint) :
    projPointRank (a + b) = projPointRank a + projPointRank b := by
  obtain ⟨n, x⟩ := a
  obtain ⟨m, y⟩ := b
  refine Quotient.inductionOn₂ x y ?_
  intro p q
  change projToInt (canonicalSpace (n + m))
      (projDiffSumCanon (projMk (canonicalSpace n) p.1 p.2)
        (projMk (canonicalSpace m) q.1 q.2)) =
    projToInt (canonicalSpace n) (projMk (canonicalSpace n) p.1 p.2) +
      projToInt (canonicalSpace m) (projMk (canonicalSpace m) q.1 q.2)
  rw [projDiffSumCanon_mk]
  exact projToInt_projDirectSumCanon_add p.1 p.2 q.1 q.2

/-- **对象层 K₀ 的等价关系**：整体秩相等。 -/
instance projPointSetoid : Setoid ProjPoint where
  r a b := projPointRank a = projPointRank b
  iseqv := ⟨fun _ => rfl, fun h => h.symm, fun h1 h2 => h1.trans h2⟩

/-- **跨维度对象层 K₀ 类**（投影差类按整体秩作商）。 -/
abbrev ProjClass := Quotient projPointSetoid

/-- 类构造。 -/
noncomputable def projClassMk (a : ProjPoint) : ProjClass := Quotient.mk projPointSetoid a

/-- **整体秩分类器下降为类上函数**（商上良定义）。 -/
noncomputable def projClassRank : ProjClass → ℤ :=
  Quotient.lift projPointRank (fun _ _ h => h)

/-- 类上秩的代表元计算。 -/
theorem projClassRank_mk (a : ProjPoint) : projClassRank (projClassMk a) = projPointRank a :=
  rfl

/-- **单射**：整体秩唯一决定对象层类。 -/
theorem projClassRank_injective : Function.Injective projClassRank := by
  rintro ⟨a⟩ ⟨b⟩ h
  exact Quotient.sound h

/-- **满射**：每个整数都被某维数空间的投影类实现（§2.23 `crossDim_reaches_any`）。 -/
theorem projClassRank_surjective : Function.Surjective projClassRank := by
  intro r
  obtain ⟨n, P, Q, hPQ⟩ := crossDim_reaches_any r
  exact ⟨projClassMk ⟨n, projMk (canonicalSpace n) P Q⟩, hPQ⟩

/-- **对象层 K₀ 类 ≃ ℤ**（双射）。 -/
noncomputable def projClassEquiv : ProjClass ≃ ℤ :=
  Equiv.ofBijective projClassRank ⟨projClassRank_injective, projClassRank_surjective⟩

noncomputable instance : Zero ProjClass := ⟨projClassEquiv.symm 0⟩
noncomputable instance : Add ProjClass :=
  ⟨fun a b => projClassEquiv.symm (projClassEquiv a + projClassEquiv b)⟩
noncomputable instance : Neg ProjClass := ⟨fun a => projClassEquiv.symm (-(projClassEquiv a))⟩
noncomputable instance : Sub ProjClass :=
  ⟨fun a b => projClassEquiv.symm (projClassEquiv a - projClassEquiv b)⟩
noncomputable instance : SMul ℕ ProjClass := ⟨fun n a => projClassEquiv.symm (n • projClassEquiv a)⟩
noncomputable instance : SMul ℤ ProjClass := ⟨fun z a => projClassEquiv.symm (z • projClassEquiv a)⟩

/-- **对象层 K₀ 类构成可加交换群**（经单射 `projClassRank` 从 ℤ 传送
    `Function.Injective.addCommGroup`）——对象层完整群结构。 -/
noncomputable instance projClassAddCommGroup : AddCommGroup ProjClass :=
  Function.Injective.addCommGroup projClassRank projClassRank_injective
    (by
      change projClassEquiv (projClassEquiv.symm 0) = 0
      rw [Equiv.apply_symm_apply])
    (by
      intro a b
      change projClassEquiv (projClassEquiv.symm (projClassEquiv a + projClassEquiv b)) =
        projClassRank a + projClassRank b
      rw [Equiv.apply_symm_apply]
      rfl)
    (by
      intro a
      change projClassEquiv (projClassEquiv.symm (-(projClassEquiv a))) = -projClassRank a
      rw [Equiv.apply_symm_apply]
      rfl)
    (by
      intro a b
      change projClassEquiv (projClassEquiv.symm (projClassEquiv a - projClassEquiv b)) =
        projClassRank a - projClassRank b
      rw [Equiv.apply_symm_apply]
      rfl)
    (by
      intro a n
      change projClassEquiv (projClassEquiv.symm (n • projClassEquiv a)) = n • projClassRank a
      rw [Equiv.apply_symm_apply]
      rfl)
    (by
      intro a n
      change projClassEquiv (projClassEquiv.symm (n • projClassEquiv a)) = n • projClassRank a
      rw [Equiv.apply_symm_apply]
      rfl)

/-- **整体秩分类器作为群同态** `ProjClass →+ ℤ`。 -/
noncomputable def projClassRankHom : ProjClass →+ ℤ where
  toFun := projClassRank
  map_zero' := by
    change projClassEquiv (projClassEquiv.symm 0) = 0
    rw [Equiv.apply_symm_apply]
  map_add' := by
    intro a b
    change projClassEquiv (projClassEquiv.symm (projClassEquiv a + projClassEquiv b)) =
      projClassRank a + projClassRank b
    rw [Equiv.apply_symm_apply]
    rfl

/-- **对象层 K₀ ≃+ ℤ**（群同构）：跨维度对象层投影差类群同构于 $\mathbb{Z}$——
    K₀(ℂ)≅ℤ 在**对象层的完整群结构**（§2.20 秩层 Grothendieck 群的对象层实现）。 -/
noncomputable def projClassRankIso : ProjClass ≃+ ℤ :=
  AddEquiv.ofBijective projClassRankHom
    ⟨projClassRank_injective, projClassRank_surjective⟩

/-- 类上秩函数沿群加法加性。 -/
theorem projClassRank_add (x y : ProjClass) :
    projClassRank (x + y) = projClassRank x + projClassRank y :=
  projClassRankHom.map_add x y

/-- **对象层群加法即跨维度直和（自然性）**：`[a] + [b] = [a ⊕ b]`——
    类加法**恰由跨维度直和实现**（`projPointRank` 沿直和加性）。 -/
theorem projClassMk_add (a b : ProjPoint) :
    projClassMk (a + b) = projClassMk a + projClassMk b := by
  apply projClassRank_injective
  rw [projClassRank_mk, projClassRank_add, projClassRank_mk, projClassRank_mk,
    projPointRank_add]

end K0ClassGroup

/-!
## §2.25 酉群作用层：`U(E)` 在投影上的共轭作用、轨道 = 秩类、轨道空间 ≃ 秩集

§3 #7「同秩投影酉等价（K₀ = ℤ）」G3 第五块（**酉群/同伦类与秩一一对应的轨道层**）。
§2.14/§2.21 已把「同秩 ⇔ 酉等价」做成**逐对显式双射**（`same_rank_iff_unitary_conj`），
§2.17 把酉等价形式化为 `Setoid`（`projUnitarySetoid`）。本层把这一**逐对**结论升级到
**群结构层**：把有限维复内积空间的自等距群 `unitaryEnd E = E ≃ₗᵢ[ℂ] E`（酉群）在投影上的
**共轭作用** `u • P := u P u⁻¹`（复用 §2.24 `conjProj`）做成真正的 `MulAction`，证明该作用
**保秩**（`unitaryConjAct_rank`）、**保持酉类**（`unitaryConjAct_rel`，作用在商上平凡），并证得
**轨道 = 秩类**（`mem_orbit_iff_same_rank`：`Q` 在 `P` 的酉轨道中 ⟺ 二者秩相等；
`orbit_eq_rankClass`）与**轨道相等 ⟺ 秩相等**（`orbit_eq_iff_same_rank`）。最后给出
**轨道空间 ≃ 秩集**（`orbitQuotEquivRankSet`：`Quotient (orbitRel) ≃ {k : ℕ // k ≤ dim E}`，
满射用 §2.22 `projOfRank`）——即 $U(E)$ 的轨道与秩 $0,\dots,\dim E$ 一一对应（轨道数 $=\dim E+1$），
「$U(n)$ 与秩一一对应」的**轨道层形态**。
诚实边界（随登）：闭合的是**轨道层**的对应（轨道 = 秩类、轨道空间 ≃ 秩集）——即把 §2.21 的
**逐对**酉双射提升为**轨道分解**；真正**同伦层**的陈述（$U(n)$ 路径连通 / 投影空间的连通分量
与秩对应，需拓扑/同伦基建）仍登记开放。
-/

section K0UnitaryAction

open scoped Int

/-- **有限维复内积空间的自等距群（酉群）** `E ≃ₗᵢ[ℂ] E`。 -/
abbrev unitaryEnd (E : Type) [NormedAddCommGroup E] [InnerProductSpace ℂ E] := E ≃ₗᵢ[ℂ] E

/-- 单位自等距的逆应用恒等。 -/
theorem unitaryEnd_symm_one {E : Type} [NormedAddCommGroup E] [InnerProductSpace ℂ E] (x : E) :
    (1 : unitaryEnd E).symm x = x := by
  change (1 : unitaryEnd E)⁻¹ x = x
  simp

/-- 乘积自等距的逆应用反序。 -/
theorem unitaryEnd_symm_mul {E : Type} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    (u v : unitaryEnd E) (x : E) : (u * v).symm x = v.symm (u.symm x) := by
  change (u * v)⁻¹ x = v⁻¹ (u⁻¹ x)
  rw [_root_.mul_inv_rev]
  simp

/-- **酉群在投影上的共轭作用** `u • P := u P u⁻¹`（复用 §2.24 `conjProj`）——
    这是把「同秩 ⇔ 酉等价」的逐对双射提升为**群作用**的载体。 -/
noncomputable instance unitaryConjAct (E : Type) [NormedAddCommGroup E] [InnerProductSpace ℂ E] :
    MulAction (unitaryEnd E) (SelfAdjointIdemProj E) where
  smul u P := conjProj u P
  one_smul P := by
    show conjProj (1 : unitaryEnd E) P = P
    apply Subtype.ext
    ext x
    simp [conjProj, unitaryEnd_symm_one]
  mul_smul u v P := by
    show conjProj (u * v) P = conjProj u (conjProj v P)
    apply Subtype.ext
    ext x
    simp [conjProj, unitaryEnd_symm_mul]

/-- 作用律：`u • P = conjProj u P`。 -/
theorem unitaryConjAct_smul {E : Type} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    (u : unitaryEnd E) (P : SelfAdjointIdemProj E) : u • P = conjProj u P := rfl

/-- **作用保秩**：`rank (u • P) = rank P`（复用 §2.24 `conjProj_rank`）。 -/
theorem unitaryConjAct_rank {E : Type} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    [FiniteDimensional ℂ E] (u : unitaryEnd E) (P : SelfAdjointIdemProj E) :
    Module.finrank ℂ (LinearMap.range (u • P).1) =
      Module.finrank ℂ (LinearMap.range P.1) :=
  conjProj_rank u P

/-- **作用保持酉类**：`P ~ u • P`（作用即酉共轭，故在商 `Quotient (projUnitarySetoid E)` 上平凡）。 -/
theorem unitaryConjAct_rel {E : Type} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    (u : unitaryEnd E) (P : SelfAdjointIdemProj E) : ProjUnitaryRel P (u • P) := by
  refine ⟨u, ?_⟩
  rw [unitaryConjAct_smul]
  change ((u.toLinearMap.comp P.1).comp u.symm.toLinearMap) ∘ₗ u.toLinearMap =
    u.toLinearMap ∘ₗ P.1
  ext x
  simp

/-- **轨道 = 秩类**：`Q` 在 `P` 的酉轨道中 ⟺ 二者秩相等（§2.21 酉双射的轨道形态）。 -/
theorem mem_orbit_iff_same_rank {E : Type} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    [FiniteDimensional ℂ E] (P Q : SelfAdjointIdemProj E) :
    Q ∈ MulAction.orbit (unitaryEnd E) P ↔
      Module.finrank ℂ (LinearMap.range Q.1) = Module.finrank ℂ (LinearMap.range P.1) := by
  constructor
  · intro h
    rw [MulAction.mem_orbit_iff] at h
    obtain ⟨u, hu⟩ := h
    rw [← hu]
    exact unitaryConjAct_rank u P
  · intro h
    rw [MulAction.mem_orbit_iff]
    obtain ⟨U, hU⟩ :=
      (same_rank_iff_unitary_conj P.1 Q.1 P.2.1 P.2.2 Q.2.1 Q.2.2).mp h.symm
    refine ⟨U, ?_⟩
    rw [unitaryConjAct_smul]
    apply Subtype.ext
    ext x
    have hpt : ∀ y, Q.1 (U y) = U (P.1 y) := fun y => LinearMap.congr_fun hU y
    change U (P.1 (U.symm x)) = Q.1 x
    simpa using (hpt (U.symm x)).symm

/-- 投影的秩（作为投影本身的函数）。 -/
noncomputable def projRank {E : Type} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    [FiniteDimensional ℂ E] (P : SelfAdjointIdemProj E) : ℕ :=
  Module.finrank ℂ (LinearMap.range P.1)

/-- 投影的秩被界于 $\dim E$。 -/
theorem projRank_le_dim {E : Type} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    [FiniteDimensional ℂ E] (P : SelfAdjointIdemProj E) :
    projRank P ≤ Module.finrank ℂ E :=
  Submodule.finrank_le _

/-- **轨道关系 = 秩相等**。 -/
theorem orbitRel_iff_same_rank {E : Type} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    [FiniteDimensional ℂ E] (P Q : SelfAdjointIdemProj E) :
    MulAction.orbitRel (unitaryEnd E) (SelfAdjointIdemProj E) P Q ↔ projRank P = projRank Q := by
  rw [MulAction.orbitRel_apply, MulAction.mem_orbit_iff]
  constructor
  · rintro ⟨u, hu⟩
    rw [← hu]
    exact unitaryConjAct_rank u Q
  · intro h
    obtain ⟨U, hU⟩ :=
      (same_rank_iff_unitary_conj Q.1 P.1 Q.2.1 Q.2.2 P.2.1 P.2.2).mp h.symm
    refine ⟨U, ?_⟩
    rw [unitaryConjAct_smul]
    apply Subtype.ext
    ext x
    have hpt : ∀ y, P.1 (U y) = U (Q.1 y) := fun y => LinearMap.congr_fun hU y
    change U (Q.1 (U.symm x)) = P.1 x
    simpa using (hpt (U.symm x)).symm

/-- **轨道即秩类**（作为集合）：$\mathrm{orbit}\,P=\{Q\mid\operatorname{rank}Q=\operatorname{rank}P\}$。 -/
theorem orbit_eq_rankClass {E : Type} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    [FiniteDimensional ℂ E] (P : SelfAdjointIdemProj E) :
    MulAction.orbit (unitaryEnd E) P = {Q | projRank Q = projRank P} := by
  ext Q
  exact mem_orbit_iff_same_rank P Q

/-- **轨道相等 ⟺ 秩相等**。 -/
theorem orbit_eq_iff_same_rank {E : Type} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    [FiniteDimensional ℂ E] (P Q : SelfAdjointIdemProj E) :
    MulAction.orbit (unitaryEnd E) P = MulAction.orbit (unitaryEnd E) Q ↔ projRank P = projRank Q := by
  rw [orbit_eq_rankClass P, orbit_eq_rankClass Q]
  constructor
  · intro h
    have hmem : P ∈ ({R | projRank R = projRank Q} : Set (SelfAdjointIdemProj E)) := by
      rw [← h]; exact rfl
    exact hmem
  · intro h
    ext R
    rw [Set.mem_ofPred_eq, Set.mem_ofPred_eq, h]

/-- 每个 $\le\dim E$ 的秩都被某投影实现（§2.22 `projOfRank`）。 -/
theorem exists_projRank_eq {E : Type} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    [FiniteDimensional ℂ E] (k : ℕ) (hk : k ≤ Module.finrank ℂ E) :
    ∃ P : SelfAdjointIdemProj E, projRank P = k :=
  ⟨projOfRank k hk, projOfRank_rankE k hk⟩

/-- **轨道空间 → 秩集**（商上良定义：轨道相等 ⟺ 秩相等）。 -/
noncomputable def orbitQuotToRank {E : Type} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    [FiniteDimensional ℂ E] :
    Quotient (MulAction.orbitRel (unitaryEnd E) (SelfAdjointIdemProj E)) →
      {k : ℕ // k ≤ Module.finrank ℂ E} :=
  Quotient.lift (fun P : SelfAdjointIdemProj E => ⟨projRank P, projRank_le_dim P⟩)
    (by
      intro P Q h
      exact Subtype.ext ((orbitRel_iff_same_rank P Q).mp h))

/-- 轨道空间 → 秩集是单射。 -/
theorem orbitQuotToRank_injective {E : Type} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    [FiniteDimensional ℂ E] : Function.Injective (orbitQuotToRank (E := E)) := by
  intro a b
  refine Quotient.inductionOn₂ a b ?_
  intro P Q h
  have hp : projRank P = projRank Q := Subtype.ext_iff.mp h
  exact Quotient.sound ((orbitRel_iff_same_rank P Q).mpr hp)

/-- 轨道空间 → 秩集是满射（§2.22 `projOfRank` 实现每个秩）。 -/
theorem orbitQuotToRank_surjective {E : Type} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    [FiniteDimensional ℂ E] : Function.Surjective (orbitQuotToRank (E := E)) := by
  intro k
  refine ⟨Quotient.mk _ (projOfRank k.1 k.2), ?_⟩
  apply Subtype.ext
  show projRank (projOfRank k.1 k.2) = k.1
  exact projOfRank_rankE k.1 k.2

/-- **酉轨道空间 ≃ 秩集**：`U(E)` 的轨道与秩 $0,\dots,\dim E$ 一一对应（轨道数 $=\dim E+1$）
    ——「$U(n)$ 与秩一一对应」的**轨道层形态**。 -/
noncomputable def orbitQuotEquivRankSet {E : Type} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    [FiniteDimensional ℂ E] :
    Quotient (MulAction.orbitRel (unitaryEnd E) (SelfAdjointIdemProj E)) ≃
      {k : ℕ // k ≤ Module.finrank ℂ E} :=
  Equiv.ofBijective (orbitQuotToRank (E := E))
    ⟨orbitQuotToRank_injective, orbitQuotToRank_surjective⟩

end K0UnitaryAction

/-!
## §2.26 对象层 K₀ 的等距自然性：等距诱导的差类映射、分类器不变量、函子性与酉作用平凡

§3 #7「同秩投影酉等价（K₀ = ℤ）」G3 第六块（**对象层 K₀ 的等距自然性/函子性**）。
§2.21 造出对象层差对象商 `ProjDiffQuot E` 与秩差分类器 `projToInt`（单射），§2.24 造出跨维度
对象层群 `ProjClass ≃+ ℤ`，§2.25 给出酉群共轭作用与轨道 = 秩类。本层补齐**自然性**：
把 §2.24 的等距共轭 `conjProj` 沿对象层下降为**差类映射** `conjProjQuot e : ProjDiffQuot E → ProjDiffQuot F`
（`e : E ≃ₗᵢ[ℂ] F`），证明它与分类器**交换**（`conjProjQuot_projToInt`：`projToInt` 是**等距不变量**，
`projToInt_conjProj`）、是**双射**（`conjProjQuotEquiv`，逆用 `e.symm`）、并满足**函子性**
（`conjProjQuot_trans`：复合相容、`conjProjQuot_refl`：单位相容）。由此得到关键结论
**酉群在对象层 K₀ 上作用平凡**（`conjProjQuot_unitary_fixed`：`conjProjQuot u x = x`）——
即对象层 K₀ 是**酉不变量**，与 §2.17「酉等价 = 秩」、§2.21「`projToInt` 只依赖秩」完全一致。
诚实边界（随登）：本层闭合的是**对象层 K₀ 的等距自然性**（差类映射 + 分类器交换 + 双射 + 函子性 +
酉作用平凡）；$U(n)$ **同伦层**（路径连通 / 连通分量，需拓扑/同伦基建）与环面上陈数密度 $F$ 的
连续场论/度理论整性仍登记开放。
-/

section K0Naturality

open scoped Int

/-- **等距共轭保持对象层秩差分类器**（`projToInt` 是等距不变量）：对 `e : E ≃ₗᵢ[ℂ] F`，
    $\mathrm{projToInt}\,F\,[(ePe^{-1})-(eQe^{-1})]=\mathrm{projToInt}\,E\,[P-Q]$
    （经 §2.24 `conjProj_rank` 保秩）。 -/
theorem projToInt_conjProj {E F : Type} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    [FiniteDimensional ℂ E] [NormedAddCommGroup F] [InnerProductSpace ℂ F]
    [FiniteDimensional ℂ F] (e : E ≃ₗᵢ[ℂ] F) (P Q : SelfAdjointIdemProj E) :
    projToInt F (projMk F (conjProj e P) (conjProj e Q)) = projToInt E (projMk E P Q) := by
  rw [projToInt_mk, projToInt_mk]
  have hP : quotientRank F (Quotient.mk (projUnitarySetoid F) (conjProj e P)) =
      quotientRank E (Quotient.mk (projUnitarySetoid E) P) := by
    rw [quotientRank, quotientRank, Quotient.lift_mk, Quotient.lift_mk]
    exact conjProj_rank e P
  have hQ : quotientRank F (Quotient.mk (projUnitarySetoid F) (conjProj e Q)) =
      quotientRank E (Quotient.mk (projUnitarySetoid E) Q) := by
    rw [quotientRank, quotientRank, Quotient.lift_mk, Quotient.lift_mk]
    exact conjProj_rank e Q
  rw [hP, hQ]

/-- **等距诱导的对象层差类映射** `conjProjQuot e : ProjDiffQuot E → ProjDiffQuot F`
    （商上良定：经 `projToInt` 单射 + 等距不变量 `projToInt_conjProj`）。 -/
noncomputable def conjProjQuot {E F : Type} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    [FiniteDimensional ℂ E] [NormedAddCommGroup F] [InnerProductSpace ℂ F]
    [FiniteDimensional ℂ F] (e : E ≃ₗᵢ[ℂ] F) : ProjDiffQuot E → ProjDiffQuot F :=
  Quotient.lift (fun p : SelfAdjointIdemProj E × SelfAdjointIdemProj E =>
      projMk F (conjProj e p.1) (conjProj e p.2))
    (by
      intro p q h
      apply projToInt_injective
      rw [projToInt_conjProj, projToInt_conjProj]
      exact congrArg (projToInt E) (Quotient.sound h))

/-- 等距诱导映射在代表元上的计算。 -/
theorem conjProjQuot_mk {E F : Type} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    [FiniteDimensional ℂ E] [NormedAddCommGroup F] [InnerProductSpace ℂ F]
    [FiniteDimensional ℂ F] (e : E ≃ₗᵢ[ℂ] F) (P Q : SelfAdjointIdemProj E) :
    conjProjQuot e (projMk E P Q) = projMk F (conjProj e P) (conjProj e Q) :=
  rfl

/-- **等距诱导映射与分类器交换**：$\mathrm{projToInt}\,F\,(\mathrm{conjProjQuot}\,e\,x)
    =\mathrm{projToInt}\,E\,x$——K₀ 是等距不变量。 -/
theorem conjProjQuot_projToInt {E F : Type} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    [FiniteDimensional ℂ E] [NormedAddCommGroup F] [InnerProductSpace ℂ F]
    [FiniteDimensional ℂ F] (e : E ≃ₗᵢ[ℂ] F) (x : ProjDiffQuot E) :
    projToInt F (conjProjQuot e x) = projToInt E x := by
  refine Quotient.inductionOn x ?_
  intro p
  exact projToInt_conjProj e p.1 p.2

/-- **等距诱导映射是单射**（分类器分离 + 交换律）。 -/
theorem conjProjQuot_injective {E F : Type} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    [FiniteDimensional ℂ E] [NormedAddCommGroup F] [InnerProductSpace ℂ F]
    [FiniteDimensional ℂ F] (e : E ≃ₗᵢ[ℂ] F) : Function.Injective (conjProjQuot e) := by
  intro x y h
  apply projToInt_injective
  rw [← conjProjQuot_projToInt e x, ← conjProjQuot_projToInt e y, h]

/-- **等距诱导映射是满射**（逆用 `e.symm` 诱导的映射）。 -/
theorem conjProjQuot_surjective {E F : Type} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    [FiniteDimensional ℂ E] [NormedAddCommGroup F] [InnerProductSpace ℂ F]
    [FiniteDimensional ℂ F] (e : E ≃ₗᵢ[ℂ] F) : Function.Surjective (conjProjQuot e) := by
  intro y
  refine ⟨conjProjQuot e.symm y, ?_⟩
  apply projToInt_injective
  rw [conjProjQuot_projToInt, conjProjQuot_projToInt]

/-- **等距诱导映射的双射** `ProjDiffQuot E ≃ ProjDiffQuot F`——对象层 K₀ 的等距自然性。 -/
noncomputable def conjProjQuotEquiv {E F : Type} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    [FiniteDimensional ℂ E] [NormedAddCommGroup F] [InnerProductSpace ℂ F]
    [FiniteDimensional ℂ F] (e : E ≃ₗᵢ[ℂ] F) : ProjDiffQuot E ≃ ProjDiffQuot F :=
  Equiv.ofBijective (conjProjQuot e) ⟨conjProjQuot_injective e, conjProjQuot_surjective e⟩

/-- **酉群在对象层 K₀ 上作用平凡**：`conjProjQuot u x = x`——对象层 K₀ 是**酉不变量**
    （与 §2.17「酉等价 = 秩」、§2.21「`projToInt` 只依赖秩」一致）。 -/
theorem conjProjQuot_unitary_fixed {E : Type} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    [FiniteDimensional ℂ E] (u : unitaryEnd E) (x : ProjDiffQuot E) :
    conjProjQuot u x = x := by
  apply projToInt_injective
  rw [conjProjQuot_projToInt]

/-- 等距共轭对复合的相容性（辅助引理）：`conjProj (e₁.trans e₂) P = conjProj e₂ (conjProj e₁ P)`。 -/
theorem conjProj_trans {X Y Z : Type} [NormedAddCommGroup X] [InnerProductSpace ℂ X]
    [NormedAddCommGroup Y] [InnerProductSpace ℂ Y] [NormedAddCommGroup Z]
    [InnerProductSpace ℂ Z] (e₁ : X ≃ₗᵢ[ℂ] Y) (e₂ : Y ≃ₗᵢ[ℂ] Z)
    (P : SelfAdjointIdemProj X) : conjProj (e₁.trans e₂) P = conjProj e₂ (conjProj e₁ P) := by
  apply Subtype.ext
  ext x
  simp [conjProj]

/-- 等距共轭对恒等的相容性（辅助引理）。 -/
theorem conjProj_refl {X : Type} [NormedAddCommGroup X] [InnerProductSpace ℂ X]
    (P : SelfAdjointIdemProj X) : conjProj (1 : X ≃ₗᵢ[ℂ] X) P = P := by
  apply Subtype.ext
  ext x
  simp [conjProj, unitaryEnd_symm_one]

/-- **函子性（复合）**：`conjProjQuot (e₁.trans e₂) = conjProjQuot e₂ ∘ conjProjQuot e₁`。 -/
theorem conjProjQuot_trans {X Y Z : Type} [NormedAddCommGroup X] [InnerProductSpace ℂ X]
    [FiniteDimensional ℂ X] [NormedAddCommGroup Y] [InnerProductSpace ℂ Y]
    [FiniteDimensional ℂ Y] [NormedAddCommGroup Z] [InnerProductSpace ℂ Z]
    [FiniteDimensional ℂ Z] (e₁ : X ≃ₗᵢ[ℂ] Y) (e₂ : Y ≃ₗᵢ[ℂ] Z) (x : ProjDiffQuot X) :
    conjProjQuot (e₁.trans e₂) x = conjProjQuot e₂ (conjProjQuot e₁ x) := by
  refine Quotient.inductionOn x ?_
  intro p
  rw [conjProjQuot_mk, conjProjQuot_mk, conjProjQuot_mk, conjProj_trans, conjProj_trans]

/-- **函子性（单位）**：`conjProjQuot 1 = id`。 -/
theorem conjProjQuot_refl {X : Type} [NormedAddCommGroup X] [InnerProductSpace ℂ X]
    [FiniteDimensional ℂ X] (x : ProjDiffQuot X) :
    conjProjQuot (1 : X ≃ₗᵢ[ℂ] X) x = x := by
  refine Quotient.inductionOn x ?_
  intro p
  rw [conjProjQuot_mk, conjProj_refl, conjProj_refl]

end K0Naturality

/-!
## §2.27 酉群连通性的拓扑基建（C*-代数层）：局部路径连通、小球路径连通与连通性归约

§3 #7「同秩投影酉等价（K₀ = ℤ）」G3 第七块（**同伦层拓扑基建第一层**）。
§2.25 给出酉群共轭作用与轨道 = 秩类，§2.26 补齐对象层 K₀ 的等距自然性；本轮为「$U(n)$ 与秩
一一对应」的**同伦层**铺基建。关键观察：`Matrix n n ℂ` 在 L²-算子范数下是 **C\*-代数**
（mathlib `Matrix.instCStarAlgebra`，经 `open scoped Matrix.Norms.L2Operator` 激活），故 mathlib 的
C\*-代数酉群拓扑理论（`Mathlib/Analysis/CStarAlgebra/Unitary/Connected.lean`）可直接实例化到矩阵
酉群 `Matrix.unitaryGroup n ℂ`：

- **局部路径连通** `unitaryGroup_locallyPathConnected`（mathlib `Unitary.instLocallyPathConnectedSpace`）
  ——同伦层的核心局部输入；
- **小距离路径连通** `unitaryGroup_joined`：`‖v - u‖ < 2` 的酉元可用显式路径连接
  （mathlib `Unitary.joined`，路径 `t ↦ expUnitary (t • argSelfAdjoint (v * star u)) * u`）；
- **小球路径连通** `unitaryGroup_isPathConnected_ball`（mathlib `Unitary.isPathConnected_ball`）；
- **路径分量 = 自伴指数乘积** `mem_pathComponent_one_iff_products`：`1` 的路径分量恰为**有限个自伴
  指数之积**（mathlib `Unitary.mem_pathComponentOne_iff`）——把"连通"转为纯代数陈述；
- **有界性** `unitaryGroup_entry_norm_le_one`（mathlib `entry_norm_bound_of_unitary`，紧性输入）。

**连通性归约** `pathConnectedSpace_unitaryGroup_of_products`：**若每个酉阵是有限个自伴指数之积，则
`U(n)` 路径连通**——把全局连通性归约为"指数积覆盖"（等价于酉阵的谱定理/对数存在性）。
诚实边界（随登）：本层闭合的是**局部拓扑基建 + 连通性归约**；全局 `PathConnectedSpace` 本体仍需
「每个酉阵 = 有限个自伴指数之积」，即酉阵的**正规谱定理/对数存在性**（mathlib 目前仅有 Hermitian
谱定理 `Matrix.IsHermitian.eigenvectorUnitary`，正规情形缺）——登记开放。
-/

section K0UnitaryTopology

open scoped Real Matrix.Norms.L2Operator
open Metric selfAdjoint Unitary

variable {n : Type} [DecidableEq n] [Fintype n]

/-- **矩阵酉群局部路径连通**（`Matrix n n ℂ` 为 C\*-代数，实例化 mathlib
    `Unitary.instLocallyPathConnectedSpace`）——同伦层核心局部输入。 -/
theorem unitaryGroup_locallyPathConnected :
    LocallyPathConnectedSpace (Matrix.unitaryGroup n ℂ) := inferInstance

/-- **小距离酉元路径连通**：`‖v - u‖ < 2` 的酉元 `u, v` 可用显式路径连接（mathlib `Unitary.joined`）。 -/
theorem unitaryGroup_joined (u v : Matrix.unitaryGroup n ℂ)
    (h : ‖(v - u : Matrix n n ℂ)‖ < 2) : Joined u v :=
  Unitary.joined u v h

/-- **小球路径连通**：酉群中半径 `< 2` 的球路径连通（mathlib `Unitary.isPathConnected_ball`）。 -/
theorem unitaryGroup_isPathConnected_ball (u : Matrix.unitaryGroup n ℂ) (δ : ℝ)
    (h0 : 0 < δ) (h2 : δ < 2) : IsPathConnected (ball u δ) :=
  Unitary.isPathConnected_ball u δ h0 h2

/-- **路径分量 = 自伴指数乘积**：`1` 的路径分量恰为有限个自伴指数 `expUnitary` 之积
    （mathlib `Unitary.mem_pathComponentOne_iff`）——把"连通"转为纯代数陈述。 -/
theorem mem_pathComponent_one_iff_products (u : Matrix.unitaryGroup n ℂ) :
    u ∈ pathComponent 1 ↔
      ∃ l : List (selfAdjoint (Matrix n n ℂ)), (l.map selfAdjoint.expUnitary).prod = u :=
  Unitary.mem_pathComponentOne_iff

/-- **酉元各元素模 ≤ 1**（mathlib `entry_norm_bound_of_unitary`）——紧性所需的有界性输入。 -/
theorem unitaryGroup_entry_norm_le_one (U : Matrix.unitaryGroup n ℂ) (i j : n) :
    ‖(U : Matrix n n ℂ) i j‖ ≤ 1 :=
  entry_norm_bound_of_unitary U.2 i j

/-- **连通性归约**：若每个酉阵都是有限个自伴指数之积，则 `U(n)` **路径连通**——把全局连通性
    归约为"指数积覆盖"（等价于酉阵的谱定理/对数存在性）。 -/
theorem pathConnectedSpace_unitaryGroup_of_products
    (h : ∀ u : Matrix.unitaryGroup n ℂ,
      ∃ l : List (selfAdjoint (Matrix n n ℂ)), (l.map selfAdjoint.expUnitary).prod = u) :
    PathConnectedSpace (Matrix.unitaryGroup n ℂ) :=
  ⟨⟨1⟩, fun x y => ((Unitary.mem_pathComponentOne_iff.mpr (h x)).symm).trans
    (Unitary.mem_pathComponentOne_iff.mpr (h y))⟩

end K0UnitaryTopology

/-!
## §2.28 全局连通性的归约强化：`pathComponent 1` 是子群 + 「避开 `-1`」子类闭合

§3 #7「同秩投影酉等价（K₀ = ℤ）」G3 第八块（**同伦层拓扑基建第二层**）。
§2.27 把 $U(n)$ 全局连通性归约为"指数积覆盖"（`mem_pathComponentOne_iff`）。本层把该归约**强化为
可操作形式**：证明 `pathComponent 1`（即指数积集合）在 `Matrix.unitaryGroup n ℂ` 中是**子群**
（单位 + 乘法 + 逆封闭），从而把全局连通性化归为**单个群论命题** `∀ u, u ∈ pathComponent 1`；
并证明**「避开 `-1`」子类**已落入该子群（`‖u - 1‖ < 2 ⇔ -1 ∉ spectrum u` 时，
`u = expUnitary (argSelfAdjoint u)`，mathlib `expUnitary_argSelfAdjoint`）。

关键交付：
- **指数取逆公式** `expUnitary_neg`：`expUnitary (-x) = (expUnitary x)⁻¹`；
- **子群封闭** `expUnitary_mem_pathComponent_one`（单指数）/`one_mem_pathComponent_one`（单位）/
  `mul_mem_pathComponent_one`（乘法，经 `Joined.mul`）/`inv_mem_pathComponent_one`（逆，经列表技巧
  `reverse_map_neg_prod_mul_prod`：逆序取负的指数积即原积之逆）；
- **「避开 `-1`」子类闭合** `mem_pathComponent_one_of_norm_sub_lt_two`；
- **连通性判据** `pathConnectedSpace_unitaryGroup_of_mem_pathComponent_one`：
  `(∀ u, u ∈ pathComponent 1) ⟹ PathConnectedSpace`。

诚实边界（随登）：本层闭合的是**归约的强化**（子群结构 + 判据 + 已知子类），全局连通性本体仍归约为
**单一命题** `∀ u : Matrix.unitaryGroup n ℂ, u ∈ pathComponent 1`（= 每个酉阵是有限个自伴指数之积）。
其完整证明需**酉阵的正规谱定理/对数存在性**（mathlib 目前仅有 Hermitian 谱定理
`Matrix.IsHermitian.eigenvectorUnitary`），登记开放；可行的两条路径：(i) 正规矩阵酉对角化
（特征向量 + 正交补不变性 + 维数归纳）；(ii) 「旋转 + 指数」技巧——取单位标量 ζ 使 `-ζ ∉ spectrum u`
（需 `spectrum u` 有限），则 `u = (ζ·1)·(ζ⁻¹u)` 为两枚「避开 `-1`」酉元之积。
-/

section K0UnitaryGlobalConnectedness

open scoped Real Matrix.Norms.L2Operator
open Metric selfAdjoint Unitary

variable {n : Type} [DecidableEq n] [Fintype n]

/-- **指数取逆公式**：`expUnitary (-x) = (expUnitary x)⁻¹`（`expUnitary` 为加法逆 ↔ 群逆）。 -/
theorem expUnitary_neg (x : selfAdjoint (Matrix n n ℂ)) :
    expUnitary (-x) = (expUnitary x)⁻¹ := by
  have h : Commute ((-x : selfAdjoint (Matrix n n ℂ)) : Matrix n n ℂ) (x : Matrix n n ℂ) :=
    Commute.neg_left (Commute.refl (x : Matrix n n ℂ))
  refine eq_inv_of_mul_eq_one_left ?_
  rw [← Commute.expUnitary_add h, neg_add_cancel, expUnitary_zero]

/-- **单指数落在 `pathComponent 1`**。 -/
theorem expUnitary_mem_pathComponent_one (x : selfAdjoint (Matrix n n ℂ)) :
    expUnitary x ∈ pathComponent (1 : Matrix.unitaryGroup n ℂ) :=
  mem_pathComponentOne_iff.mpr ⟨[x], by simp⟩

/-- **单位落在 `pathComponent 1`**。 -/
theorem one_mem_pathComponent_one :
    (1 : Matrix.unitaryGroup n ℂ) ∈ pathComponent 1 :=
  mem_pathComponentOne_iff.mpr ⟨[], by simp⟩

/-- **乘法封闭**（经 `Joined.mul`）。 -/
theorem mul_mem_pathComponent_one {u v : Matrix.unitaryGroup n ℂ}
    (hu : u ∈ pathComponent 1) (hv : v ∈ pathComponent 1) :
    u * v ∈ pathComponent 1 := by
  show Joined 1 (u * v)
  rw [show (1 : Matrix.unitaryGroup n ℂ) = 1 * 1 from (one_mul 1).symm]
  exact hu.mul hv

/-- 辅助：**逆序取负的指数积是原指数积之逆**（列表归纳）。 -/
theorem reverse_map_neg_prod_mul_prod (l : List (selfAdjoint (Matrix n n ℂ))) :
    ((l.reverse.map fun x => expUnitary (-x)).prod) * ((l.map expUnitary).prod) = 1 := by
  induction l with
  | nil => simp
  | cons x xs ih =>
      rw [List.reverse_cons, List.map_append, List.prod_append]
      simp only [List.map_cons, List.map_nil, List.prod_cons, List.prod_nil, mul_one]
      rw [mul_assoc, expUnitary_neg x, ← mul_assoc (expUnitary x)⁻¹ (expUnitary x),
        inv_mul_cancel, one_mul, ih]

/-- **逆封闭**：指数积之逆仍是指数积（逆序取负）。 -/
theorem inv_mem_pathComponent_one (u : Matrix.unitaryGroup n ℂ)
    (hu : u ∈ pathComponent 1) : u⁻¹ ∈ pathComponent 1 := by
  obtain ⟨l, rfl⟩ := mem_pathComponentOne_iff.mp hu
  refine mem_pathComponentOne_iff.mpr ⟨l.reverse.map (fun x => -x), ?_⟩
  rw [List.map_map]
  exact eq_inv_of_mul_eq_one_left (reverse_map_neg_prod_mul_prod l)

/-- **「避开 `-1`」子类闭合**：`‖u - 1‖ < 2`（⇔ `-1 ∉ spectrum u`）的酉元是单枚指数，
    故落在 `pathComponent 1`（mathlib `expUnitary_argSelfAdjoint`）。 -/
theorem mem_pathComponent_one_of_norm_sub_lt_two (u : Matrix.unitaryGroup n ℂ)
    (hu : ‖(u - 1 : Matrix n n ℂ)‖ < 2) :
    u ∈ pathComponent 1 := by
  refine mem_pathComponentOne_iff.mpr ⟨[argSelfAdjoint u], ?_⟩
  simp [expUnitary_argSelfAdjoint hu]

/-- **连通性判据**：若每个酉阵都是有限个自伴指数之积（即 `∀ u, u ∈ pathComponent 1`），
    则 `U(n)` **路径连通**——全局连通性化归为这一**单一群论命题**。 -/
theorem pathConnectedSpace_unitaryGroup_of_mem_pathComponent_one
    (h : ∀ u : Matrix.unitaryGroup n ℂ, u ∈ pathComponent 1) :
    PathConnectedSpace (Matrix.unitaryGroup n ℂ) :=
  ⟨⟨1⟩, fun u v => by
    have hj : Joined (1 : Matrix.unitaryGroup n ℂ) (u⁻¹ * v) := h (u⁻¹ * v)
    have hh : Joined (u * 1) (u * (u⁻¹ * v)) := (Joined.refl u).mul hj
    simpa using hh⟩

end K0UnitaryGlobalConnectedness

/-!
## §2.29 矩阵谱有限性：`spectrum ℂ A` 有限（"旋转 + 指数"路线的最后一块基建）

§3 #7「同秩投影酉等价（K₀ = ℤ）」G3 第九块（**同伦层拓扑基建第三层**）。
§2.28 把 $U(n)$ 全局连通性归约为单一命题，并给出两条可行路径；其中**「旋转 + 指数」路线**只差一块
基建：**矩阵谱有限性**（用于在单位圆上选出旋转标量 `ζ` 使 `-ζ ∉ spectrum u`）。本层补齐它。

数学内容：`n×n` 复矩阵的谱恰为**特征多项式的根集**（mathlib `Matrix.mem_spectrum_iff_isRoot_charpoly`：
`r ∈ spectrum ℂ A ↔ IsRoot A.charpoly r`），而 `charpoly A ≠ 0`（首一），故其根集是有限多重集的支撑，
**有限**。

交付：
- **矩阵谱有限** `matrix_spectrum_finite`：`(spectrum ℂ A).Finite`（`A : Matrix n n ℂ`）；
  由于本版本 mathlib 中 `Set.Finite s` 即子类型上的 `Finite s`，该定理**同时**给出类型类命题
  `Finite ↥(spectrum ℂ A)`（可 `haveI` 引入）。
- **酉元谱有限** `unitary_spectrum_finite`：`u : Matrix.unitaryGroup n ℂ` 时
  `(spectrum ℂ (u : Matrix n n ℂ)).Finite`。

诚实边界（随登）：本层闭合的是**谱有限性基建**。补齐后，「旋转 + 指数」路线仍需两块：
(i) 单位圆无穷 ⟹ 存在单位标量 `ζ` 使 `-ζ ∉ spectrum u`（需 `Circle` 无穷）；
(ii) 标量旋转的谱变换 `spectrum ℂ (c • A) = c • spectrum ℂ A`（`c ≠ 0`，mathlib 暂无现成引理，
    可由 `charpoly` 与行列式重推）。二者与原已知的
`mem_pathComponent_one_of_norm_sub_lt_two`（§2.28）合用即可闭合全局连通性。
-/

section K0SpectrumFinite

open Polynomial

variable {n : Type} [DecidableEq n] [Fintype n]

/-- **矩阵谱有限性**：`n×n` 复矩阵的谱 = 特征多项式的根集（`Matrix.mem_spectrum_iff_isRoot_charpoly`），
    而 `charpoly A ≠ 0`（首一），故谱**有限**。 -/
theorem matrix_spectrum_finite (A : Matrix n n ℂ) : (spectrum ℂ A).Finite :=
  (A.charpoly.roots.toFinset.finite_toSet).subset fun r hr => by
    simp only [Finset.mem_coe, Multiset.mem_toFinset]
    exact (mem_roots A.charpoly_monic.ne_zero).mpr
      (Matrix.mem_spectrum_iff_isRoot_charpoly.mp hr)

/-- **`Finite` 类型类形式**（本版本 mathlib 中 `Set.Finite s` 即 `Finite ↥s`）——
    可由 `haveI := matrix_spectrum_finite A` 引入，供后续（选旋转标量 `ζ`）使用。 -/
theorem matrix_spectrum_finite' (A : Matrix n n ℂ) : Finite ↥(spectrum ℂ A) :=
  matrix_spectrum_finite A

/-- **酉元谱有限性**（C\*-代数意义）：酉元作为矩阵的谱有限。 -/
theorem unitary_spectrum_finite (u : Matrix.unitaryGroup n ℂ) :
    (spectrum ℂ (u : Matrix n n ℂ)).Finite :=
  matrix_spectrum_finite (u : Matrix n n ℂ)

end K0SpectrumFinite

/-!
## §2.30 全局连通性收口：`U(n)` 连通（K₀ 同伦层闭合）

§3 #7「同秩投影酉等价（K₀ = ℤ）」G3 第十块（**同伦层收口**）。
§2.27–§2.29 已备齐：「指数积覆盖 ⟹ 路径连通」（§2.27）、`pathComponent 1` 是子群 + 「避开 `-1`」子类
（§2.28）、矩阵谱有限（§2.29）。本层补上最后两块基建（**单位圆无穷**、**标量谱变换**）并**收口**：

**「旋转 + 指数」论证**。取单位圆上一点 `ζ` 使 `-ζ ∉ spectrum u` 且 `ζ ≠ -1`（谱有限 + 单位圆无穷 ⟹
可避开有限集）。则
  `u = (ζ • 1) · (ζ⁻¹ • u)`，
且两因子都落在 `pathComponent 1`：
- `ζ • 1`：标量酉元，`-1 ∉ spectrum (ζ•1)`（由 `ζ ≠ -1`，显式构造单位 `(-(1+ζ)) • 1`），
  故 `‖ζ•1 - 1‖ < 2`（mathlib `Unitary.norm_sub_one_lt_two_iff`）⟹ §2.28 判据；
- `ζ⁻¹ • u`：由**标量谱变换** `z ∈ spectrum (c • a) ↔ c⁻¹ z ∈ spectrum a`（`c ≠ 0`）得
  `-1 ∈ spectrum (ζ⁻¹ • u) ↔ -ζ ∈ spectrum u`，故 `-1 ∉ spectrum`，同上落入。
再由 §2.28 的乘法封闭得 `u ∈ pathComponent 1`。

**交付**：`unitCircle_infinite`（单位圆无穷，经有理/半圆参数化 `x ↦ (x, √(1-x²))` 落在单位圆且单射）、
`exists_norm_eq_one_notMem_neg`、`smul_mem_spectrum_iff`（**标量谱变换**）、`neg_one_notMem_spectrum_smul_one`、
`smul_unitary_mem_unitary`、`scalar_smul_one_mem_pathComponent_one`、`smul_unitary_mem_pathComponent_one`、
`mem_pathComponent_one_unitary`（**每个酉元都是有限个自伴指数之积**）、`exists_expUnitary_prod_eq`、
**`pathConnectedSpace_unitaryGroup`**（$U(n)$ **路径连通**）。

诚实边界（随登）：本层**闭合** $U(n)$ 全局连通性（路径连通）与等价的指数积覆盖定理，从而闭合 §3 #7 登记的
「$U(n)$ 酉群/同伦类与秩一一对应」的**连通性/同伦层**。**仍未闭合**：环面上陈数密度 $F$ 的连续场论/度理论
整性（含同伦提升，§3 #4）——它需要 `F` 的可积性/光滑性与环面积分层面的度理论，与本层的群拓扑连通性
相互独立。
-/

section K0GlobalConnectivity

open scoped Real Matrix.Norms.L2Operator
open Metric Complex selfAdjoint Unitary

variable {n : Type} [DecidableEq n] [Fintype n]

/-- **标量因子可提出单位判定**（`c ≠ 0` 时 `algebraMap c * b` 是单位 ⟺ `b` 是单位）。 -/
theorem isUnit_algebraMap_mul_iff {c : ℂ} (hc : c ≠ 0) (b : Matrix n n ℂ) :
    IsUnit (algebraMap ℂ (Matrix n n ℂ) c * b) ↔ IsUnit b := by
  have hcx : IsUnit (algebraMap ℂ (Matrix n n ℂ) c) :=
    ⟨⟨algebraMap ℂ (Matrix n n ℂ) c, algebraMap ℂ (Matrix n n ℂ) c⁻¹,
      by rw [← map_mul, mul_inv_cancel₀ hc, map_one],
      by rw [← map_mul, inv_mul_cancel₀ hc, map_one]⟩, rfl⟩
  have hcxi : IsUnit (algebraMap ℂ (Matrix n n ℂ) c⁻¹) :=
    ⟨⟨algebraMap ℂ (Matrix n n ℂ) c⁻¹, algebraMap ℂ (Matrix n n ℂ) c,
      by rw [← map_mul, inv_mul_cancel₀ hc, map_one],
      by rw [← map_mul, mul_inv_cancel₀ hc, map_one]⟩, rfl⟩
  constructor
  · intro h
    have hb_eq : algebraMap ℂ (Matrix n n ℂ) c⁻¹
        * (algebraMap ℂ (Matrix n n ℂ) c * b) = b := by
      rw [← mul_assoc, ← map_mul, inv_mul_cancel₀ hc, map_one, one_mul]
    rw [← hb_eq]
    exact hcxi.mul h
  · intro h
    exact hcx.mul h

/-- **标量谱变换**：`z ∈ spectrum ℂ (c • a) ↔ c⁻¹ z ∈ spectrum ℂ a`（`c ≠ 0`）。
    经 `spectrum.mem_iff` 化为 `IsUnit` 判定与因式分解 `z • 1 - c • a = c • (c⁻¹z • 1 - a)`。 -/
theorem smul_mem_spectrum_iff {c : ℂ} (hc : c ≠ 0) (a : Matrix n n ℂ) (z : ℂ) :
    z ∈ spectrum ℂ (c • a) ↔ c⁻¹ * z ∈ spectrum ℂ a := by
  have h1 : algebraMap ℂ (Matrix n n ℂ) z - c • a
      = algebraMap ℂ (Matrix n n ℂ) c
        * (algebraMap ℂ (Matrix n n ℂ) (c⁻¹ * z) - a) := by
    rw [Algebra.smul_def, mul_sub, ← map_mul, mul_inv_cancel_left₀ hc]
  rw [spectrum.mem_iff, spectrum.mem_iff, h1]
  exact not_congr (isUnit_algebraMap_mul_iff hc _)

/-- **单位圆无穷**：`x ↦ (x, √(1-x²))`（`x ∈ (-1,1)`）落在单位圆上且单射，而 `(-1,1)` 无穷。 -/
theorem unitCircle_infinite : (Metric.sphere (0 : ℂ) 1).Infinite := by
  have : Infinite ↥(Set.Ioo (-1 : ℝ) 1) :=
    (Set.Ioo_infinite (show (-1 : ℝ) < 1 by norm_num)).to_subtype
  refine (Set.infinite_range_of_injective (f := fun x : ↥(Set.Ioo (-1 : ℝ) 1) =>
    Complex.mk (x : ℝ) (Real.sqrt (1 - (x : ℝ) ^ 2))) ?_).mono ?_
  · intro a b hab
    exact Subtype.ext (by simpa using congrArg Complex.re hab)
  · rintro _ ⟨x, rfl⟩
    simp only [Metric.mem_sphere, dist_zero_right]
    have hx := x.2
    have hnonneg : (0 : ℝ) ≤ 1 - (x : ℝ) ^ 2 := by nlinarith [hx.1, hx.2]
    have hns : Complex.normSq (Complex.mk (x : ℝ) (Real.sqrt (1 - (x : ℝ) ^ 2))) = 1 := by
      rw [Complex.normSq_apply]
      change (x : ℝ) * (x : ℝ) + Real.sqrt (1 - (x : ℝ) ^ 2) * Real.sqrt (1 - (x : ℝ) ^ 2) = 1
      rw [show Real.sqrt (1 - (x : ℝ) ^ 2) * Real.sqrt (1 - (x : ℝ) ^ 2) = 1 - (x : ℝ) ^ 2 from by
        rw [← sq]; exact Real.sq_sqrt hnonneg]
      ring
    have h2 : ‖Complex.mk (x : ℝ) (Real.sqrt (1 - (x : ℝ) ^ 2))‖ ^ 2 = 1 := by
      rw [Complex.sq_norm, hns]
    nlinarith [norm_nonneg (Complex.mk (x : ℝ) (Real.sqrt (1 - (x : ℝ) ^ 2)))]

/-- **单位圆上可避开任意有限集**：存在 `‖ζ‖ = 1` 使 `ζ ≠ -z` 对所有 `z ∈ S`（`S` 有限）。 -/
theorem exists_norm_eq_one_notMem_neg {S : Set ℂ} (hS : S.Finite) :
    ∃ ζ : ℂ, ‖ζ‖ = 1 ∧ ∀ z ∈ S, ζ ≠ -z := by
  have hfin : ((fun z : ℂ => -z) '' S).Finite := hS.image _
  obtain ⟨ζ, hζ, hζS⟩ := unitCircle_infinite.exists_notMem_finite hfin
  refine ⟨ζ, by simpa [Metric.mem_sphere, dist_zero_right] using hζ, ?_⟩
  intro z hz hc
  exact hζS ⟨z, hz, hc.symm⟩

/-- **`-1 ∉ spectrum (ζ • 1)`**（当 `ζ ≠ -1`）：显式构造单位 `(-(1+ζ)) • 1`
    （逆 `(-(1+ζ))⁻¹ • 1`），并把 `algebraMap (-1) - ζ • 1` 改写为它。 -/
theorem neg_one_notMem_spectrum_smul_one {ζ : ℂ} (hζ : ζ ≠ -1) :
    (-1 : ℂ) ∉ spectrum ℂ (ζ • (1 : Matrix n n ℂ)) := by
  have hc0 : -(1 + ζ) ≠ 0 := by
    simp only [neg_ne_zero, ne_eq]
    intro h
    exact hζ (eq_neg_iff_add_eq_zero.mpr (by rw [add_comm]; exact h))
  have h1 : algebraMap ℂ (Matrix n n ℂ) (-1) - ζ • (1 : Matrix n n ℂ)
      = (-(1 + ζ)) • (1 : Matrix n n ℂ) := by
    rw [Algebra.algebraMap_eq_smul_one, ← sub_smul]
    congr 1
    ring
  rw [spectrum.mem_iff, h1]
  intro h
  apply h
  refine ⟨⟨(-(1 + ζ)) • (1 : Matrix n n ℂ), (-(1 + ζ))⁻¹ • (1 : Matrix n n ℂ), ?_, ?_⟩, rfl⟩
  · show (-(1 + ζ)) • (1 : Matrix n n ℂ) * ((-(1 + ζ))⁻¹ • (1 : Matrix n n ℂ)) = 1
    rw [smul_mul_smul, mul_inv_cancel₀ hc0, one_smul, mul_one]
  · show (-(1 + ζ))⁻¹ • (1 : Matrix n n ℂ) * ((-(1 + ζ)) • (1 : Matrix n n ℂ)) = 1
    rw [smul_mul_smul, inv_mul_cancel₀ hc0, one_smul, mul_one]

/-- **标量旋转保持酉性**（`ζ * star ζ = 1` ⟹ `ζ • x` 仍酉）。 -/
theorem smul_unitary_mem_unitary {ζ : ℂ} (hζ : ζ * star ζ = 1) {x : Matrix n n ℂ}
    (hx : x ∈ unitary (Matrix n n ℂ)) : ζ • x ∈ unitary (Matrix n n ℂ) := by
  have h1 : x * star x = 1 := Unitary.mul_star_self_of_mem hx
  have h2 : star x * x = 1 := Unitary.star_mul_self_of_mem hx
  have h4 : star ζ * ζ = 1 := by rw [mul_comm]; exact hζ
  rw [Unitary.mem_iff]
  constructor <;>
    simp only [star_smul, smul_mul_smul, one_smul, hζ, h4, h1, h2]

/-- **模 1 标量的共轭关系**：`‖ζ‖ = 1 ⟹ ζ * star ζ = 1`（酉性前提）。 -/
theorem mul_star_eq_one_of_norm_eq_one {ζ : ℂ} (h : ‖ζ‖ = 1) : ζ * star ζ = 1 := by
  rw [Complex.star_def, Complex.mul_conj, ← Complex.sq_norm, h]
  norm_num

/-- **标量酉元落入 `pathComponent 1`**（`‖ζ‖ = 1`、`ζ ≠ -1`）。 -/
theorem scalar_smul_one_mem_pathComponent_one {ζ : ℂ} (hζnorm : ‖ζ‖ = 1) (hζ : ζ ≠ -1) :
    (⟨ζ • (1 : Matrix n n ℂ),
      smul_unitary_mem_unitary (mul_star_eq_one_of_norm_eq_one hζnorm) (by simp)⟩ :
      Matrix.unitaryGroup n ℂ) ∈ pathComponent 1 := by
  have hmem : ζ • (1 : Matrix n n ℂ) ∈ unitary (Matrix n n ℂ) :=
    smul_unitary_mem_unitary (mul_star_eq_one_of_norm_eq_one hζnorm) (by simp)
  refine mem_pathComponent_one_of_norm_sub_lt_two
    (⟨ζ • (1 : Matrix n n ℂ), hmem⟩ : Matrix.unitaryGroup n ℂ) ?_
  rw [Unitary.norm_sub_one_lt_two_iff hmem]
  exact neg_one_notMem_spectrum_smul_one hζ

/-- **酉元的标量旋转落入 `pathComponent 1`**（`‖c‖ = 1`、`-c⁻¹ ∉ spectrum u`）——
    经标量谱变换把 `-1 ∉ spectrum (c • u)` 化为 `-c⁻¹ ∉ spectrum u`。 -/
theorem smul_unitary_mem_pathComponent_one (u : Matrix.unitaryGroup n ℂ) {c : ℂ}
    (hc : ‖c‖ = 1) (hspec : -(c⁻¹) ∉ spectrum ℂ (u : Matrix n n ℂ)) :
    (⟨c • (u : Matrix n n ℂ),
      smul_unitary_mem_unitary (mul_star_eq_one_of_norm_eq_one hc) u.2⟩ :
      Matrix.unitaryGroup n ℂ) ∈ pathComponent 1 := by
  have hmem : c • (u : Matrix n n ℂ) ∈ unitary (Matrix n n ℂ) :=
    smul_unitary_mem_unitary (mul_star_eq_one_of_norm_eq_one hc) u.2
  have hc0 : c ≠ 0 := by
    intro h0
    rw [h0] at hc
    norm_num at hc
  refine mem_pathComponent_one_of_norm_sub_lt_two
    (⟨c • (u : Matrix n n ℂ), hmem⟩ : Matrix.unitaryGroup n ℂ) ?_
  rw [Unitary.norm_sub_one_lt_two_iff hmem,
    smul_mem_spectrum_iff (c := c) hc0 (u : Matrix n n ℂ) (-1)]
  simpa using hspec

/-- **每个酉元都是有限个自伴指数之积**（全局连通性的代数形式；即 `u ∈ pathComponent 1`）。
    论证：「旋转 + 指数」——取单位圆上 `ζ` 使 `-ζ ∉ spectrum u` 且 `ζ ≠ -1`，
    则 `u = (ζ • 1) · (ζ⁻¹ • u)` 为两枚落入 `pathComponent 1` 的元素之积。 -/
theorem mem_pathComponent_one_unitary (u : Matrix.unitaryGroup n ℂ) :
    u ∈ pathComponent (1 : Matrix.unitaryGroup n ℂ) := by
  obtain ⟨ζ, hζnorm, hζavoid⟩ := exists_norm_eq_one_notMem_neg
    ((matrix_spectrum_finite (u : Matrix n n ℂ)).union (Set.finite_singleton 1))
  have hζspec : -ζ ∉ spectrum ℂ (u : Matrix n n ℂ) :=
    fun h => hζavoid (-ζ) (Or.inl h) (by rw [neg_neg])
  have hζne : ζ ≠ -1 := hζavoid 1 (Or.inr (by simp))
  have hζ0 : ζ ≠ 0 := by
    intro h0
    rw [h0] at hζnorm
    norm_num at hζnorm
  have hmemw : ζ • (1 : Matrix n n ℂ) ∈ unitary (Matrix n n ℂ) :=
    smul_unitary_mem_unitary (mul_star_eq_one_of_norm_eq_one hζnorm) (by simp)
  have hmemv : ζ⁻¹ • (u : Matrix n n ℂ) ∈ unitary (Matrix n n ℂ) :=
    smul_unitary_mem_unitary (mul_star_eq_one_of_norm_eq_one (by rw [norm_inv, hζnorm, inv_one]))
      u.2
  have hprod : (⟨ζ • (1 : Matrix n n ℂ), hmemw⟩ : Matrix.unitaryGroup n ℂ)
      * (⟨ζ⁻¹ • (u : Matrix n n ℂ), hmemv⟩ : Matrix.unitaryGroup n ℂ) = u := by
    refine Subtype.ext ?_
    show ζ • (1 : Matrix n n ℂ) * (ζ⁻¹ • (u : Matrix n n ℂ)) = (u : Matrix n n ℂ)
    rw [smul_mul_smul, one_mul, mul_inv_cancel₀ hζ0, one_smul]
  have h1mem : (⟨ζ • (1 : Matrix n n ℂ), hmemw⟩ : Matrix.unitaryGroup n ℂ)
      ∈ pathComponent 1 := scalar_smul_one_mem_pathComponent_one hζnorm hζne
  have h2mem : (⟨ζ⁻¹ • (u : Matrix n n ℂ), hmemv⟩ : Matrix.unitaryGroup n ℂ)
      ∈ pathComponent 1 := smul_unitary_mem_pathComponent_one u (c := ζ⁻¹)
    (by rw [norm_inv, hζnorm, inv_one]) (by simpa [inv_inv] using hζspec)
  rw [← hprod]
  exact mul_mem_pathComponent_one h1mem h2mem

/-- **指数积表示**：每个酉阵 `u` 都是有限个自伴指数之积（`mem_pathComponentOne_iff` 正向）。 -/
theorem exists_expUnitary_prod_eq (u : Matrix.unitaryGroup n ℂ) :
    ∃ l : List (selfAdjoint (Matrix n n ℂ)), (l.map selfAdjoint.expUnitary).prod = u :=
  Unitary.mem_pathComponentOne_iff.mp (mem_pathComponent_one_unitary u)

/-- **$U(n)$ 路径连通**（K₀ 同伦层收口）：由 §2.28 判据与上式立即得到。 -/
theorem pathConnectedSpace_unitaryGroup : PathConnectedSpace (Matrix.unitaryGroup n ℂ) :=
  pathConnectedSpace_unitaryGroup_of_mem_pathComponent_one mem_pathComponent_one_unitary

/-- **$U(n)$ 连通**（`PathConnectedSpace` ⟹ `ConnectedSpace` 之显式形式）。 -/
theorem connectedSpace_unitaryGroup : ConnectedSpace (Matrix.unitaryGroup n ℂ) := by
  have := pathConnectedSpace_unitaryGroup (n := n)
  infer_instance

end K0GlobalConnectivity

/-!
## §2.31 陈数整性的环绕数层：`z ↦ z^n` 的度 = n ∈ ℤ

§3 #2/#4 的连续积分层第二块基石。§2.10 已给出恒等映射（`z ↦ z`）的度 = 1 ∈ ℤ；本层推广到
**模型族** `z ↦ z^n`（`n : ℕ`）：其**对数导数**为 `f'/f = n/z`，故归一化单位圆环路积分
（环绕数/度）恰取 `n ∈ ℤ`。这是「陈数密度积分取整值」在连续积分层的**首个非平凡族**，
也是度理论（一般 `S¹ → S¹` 映射的度 ∈ ℤ）的模型实例。

交付：`circleIntegral_const_mul_inv`（圆周积分常数倍线性）、`logDeriv_pow`（**对数导数**
`f'/f = n/z`，经 `deriv_pow` + `div_eq_div_iff`）、`unitCircle_windingNumber_pow`
（**`z ↦ z^n` 的环绕数 = n ∈ ℤ**）。

诚实边界（随登）：闭合的是**模型族的环绕数整值**。§3 #2（一般连续映射的陈数整性）与 §3 #4
（陈数**绝热不变性**）仍需：① **一般度理论**——mathlib 经实地勘查**完全缺失** `windingNumber`
与度理论基建，需从零搭建（路径提升 `S¹ → ℝ`、度的同伦不变性、`T²` 上的双参数版本）；
② 曲率被积 $F$ 的可积性/光滑性（⇐ 投影族 $P(k)$ 光滑，属 Kato 微扰论层）。二者与 §2.30 的
群连通性相互独立，登记开放。
-/

section K0WindingZpow

open scoped Real

/-- **圆周积分的常数倍线性**：$\oint n/z = n \cdot \oint 1/z$（`circleIntegral.integral_const_mul`
+ §2.10 `unitCircle_integral_inv`）。 -/
theorem circleIntegral_const_mul_inv (n : ℂ) :
    (∮ z in C(0, 1), n * (z : ℂ)⁻¹) = n * (2 * Real.pi * Complex.I) := by
  rw [circleIntegral.integral_const_mul, unitCircle_integral_inv]

/-- **`z ↦ z^n` 的对数导数**：$f'/f = n/z$（`z ≠ 0`）。对 `n = 0` 两边为 0；
    `n ≥ 1` 时经 `deriv_pow`（`(z^n)' = n z^{n-1}`）与 `div_eq_div_iff` 交叉相乘闭合。 -/
theorem logDeriv_pow (n : ℕ) (z : ℂ) (hz : z ≠ 0) :
    deriv (fun w : ℂ => w ^ n) z / z ^ n = (n : ℂ) / z := by
  rcases Nat.eq_zero_or_pos n with hn | hn
  · subst hn
    simp
  · have hderiv : deriv (fun w : ℂ => w ^ n) z = (n : ℂ) * z ^ (n - 1) := by
      have h1 : deriv ((fun w : ℂ => w) ^ n) z
          = (n : ℂ) * z ^ (n - 1) * deriv (fun w : ℂ => w) z :=
        deriv_pow (𝕜 := ℂ) (𝔸 := ℂ) (f := fun w : ℂ => w) (x := z) differentiableAt_id n
      have h2 : deriv (fun w : ℂ => w) z = 1 := by simp
      rw [h2, mul_one] at h1
      exact h1
    rw [hderiv, div_eq_div_iff (pow_ne_zero n hz) hz, mul_assoc,
      show z ^ (n - 1) * z = z ^ n from by
        rw [← pow_succ]
        congr 1
        omega]

/-- **环绕数整值：`z ↦ z^n` 的度 = n ∈ ℤ**（归一化单位圆环路积分）。
    陈数整性在连续积分层的首个非平凡模型族。 -/
theorem unitCircle_windingNumber_pow (n : ℕ) :
    ((2 * Real.pi * Complex.I : ℂ)⁻¹) * (∮ z in C(0, 1), (n : ℂ) * (z : ℂ)⁻¹)
      = (n : ℂ) := by
  rw [circleIntegral_const_mul_inv]
  have hzn : (2 * Real.pi * Complex.I : ℂ) ≠ 0 := by
    exact mul_ne_zero
      (mul_ne_zero (by norm_num : (2 : ℂ) ≠ 0) (by exact_mod_cast Real.pi_ne_zero))
      Complex.I_ne_zero
  rw [mul_comm (n : ℂ) (2 * Real.pi * Complex.I), ← mul_assoc, inv_mul_cancel₀ hzn, one_mul]

end K0WindingZpow

/-!
## §2.32 一般度理论第一层：覆盖空间路径提升 ⟹ 环路度 ∈ ℤ

§3 #2/#4 的连续积分层第三块基石，也是**从零搭建度理论**的第一层。§2.10/§2.31 给出**模型族**
（$z\mapsto z$、$z\mapsto z^n$）的环绕数整值；本层把整性提升到**任意闭路**：用
`Complex.isCoveringMap_exp`（$\exp:\mathbb C\to\mathbb C\setminus\{0\}$ 是**覆盖映射**）的
**路径提升**把 $\mathbb C\setminus\{0\}$ 中的闭路 `γ` 提升为 $\mathbb C$ 中的路径 `Γ`，
再用 `exp` 的周期性核 `Complex.exp_eq_exp_iff_exists_int`
（`exp x = exp y ↔ ∃ n : ℤ, x = y + n·2πI`）得 `Γ 1 - Γ 0 = n · 2πI`——**环路度
`(Γ 1 - Γ 0)/(2πI) ∈ ℤ`**。

交付：
- **环路提升** `exists_exp_lift`：`γ 0 = 1`、处处非零 ⟹ ∃ 连续 `Γ` 使 `exp ∘ Γ = γ` 且 `Γ 0 = 0`
  （`IsCoveringMap.liftPath` + `liftPath_lifts` + `liftPath_zero`）。
- **环绕数整性** `winding_integrality`：闭路（`γ 0 = γ 1 = 1`）的提升端点差是 `2πI` 的**整数倍**。
- **环路度** `loopDegree`（定义层）+ `loopDegree_eq_int`（**度取整值**）。

诚实边界（随登）：本层闭合的是**度的整性**（任意闭路，非仅模型族）。**同伦不变性**（§3 #4 的内核：
同伦闭路度相同）已定位到 mathlib 的 `IsCoveringMap.liftPathQuotient`（提升端点在
`Path.Homotopic.Quotient` 上良定义）——下一层可据此闭合；环面上 $T^2$ 双参数版本、曲率被积 $F$ 的
可积性/光滑性（Kato 微扰论层）仍登记开放。
-/

section K0DegreeTheory

/-- **环路提升**：`γ : C(unitInterval, ℂ)` 满足 `γ 0 = 1` 且处处非零，则存在连续
    `Γ : C(unitInterval, ℂ)` 使 `Complex.exp ∘ Γ = γ` 且 `Γ 0 = 0`
    （覆盖映射 `Complex.isCoveringMap_exp : ℂ → ℂ∖{0}` 的路径提升）。 -/
theorem exists_exp_lift (γ : C(unitInterval, ℂ)) (h0 : γ 0 = 1) (hnz : ∀ t, γ t ≠ 0) :
    ∃ Γ : C(unitInterval, ℂ), (∀ t, Complex.exp (Γ t) = γ t) ∧ Γ 0 = 0 := by
  have hcont : Continuous fun t : unitInterval => (⟨γ t, hnz t⟩ : {z : ℂ // z ≠ 0}) :=
    Continuous.subtype_mk γ.continuous hnz
  let γ' : C(unitInterval, {z : ℂ // z ≠ 0}) := ⟨_, hcont⟩
  let p : ℂ → {z : ℂ // z ≠ 0} := fun z => ⟨Complex.exp z, Complex.exp_ne_zero z⟩
  have hcov : IsCoveringMap p := Complex.isCoveringMap_exp
  have hbase : γ' 0 = p 0 := by
    refine Subtype.ext ?_
    simp [γ', p, h0, Complex.exp_zero]
  refine ⟨hcov.liftPath γ' 0 hbase, ?_, ?_⟩
  · intro t
    have h := congr_fun (hcov.liftPath_lifts γ' 0 hbase) t
    exact congrArg Subtype.val h
  · exact hcov.liftPath_zero γ' 0 hbase

/-- **环绕数（度）的整性**：闭路（`γ 0 = γ 1 = 1`、处处非零）的提升端点差是 `2πI` 的**整数倍**
    ——即环路度 `(Γ 1 - Γ 0)/(2πI) ∈ ℤ`。经 `Complex.exp_eq_exp_iff_exists_int`（`exp` 周期性核）。 -/
theorem winding_integrality (γ : C(unitInterval, ℂ)) (h0 : γ 0 = 1) (h1 : γ 1 = 1)
    (hnz : ∀ t, γ t ≠ 0) :
    ∃ n : ℤ, ∃ Γ : C(unitInterval, ℂ), (∀ t, Complex.exp (Γ t) = γ t) ∧ Γ 0 = 0
      ∧ Γ 1 - Γ 0 = n * (2 * Real.pi * Complex.I) := by
  obtain ⟨Γ, hlift, hΓ0⟩ := exists_exp_lift γ h0 hnz
  have hexp : Complex.exp (Γ 1) = Complex.exp (Γ 0) := by
    rw [hlift 1, hlift 0, h1, ← h0]
  obtain ⟨n, hn⟩ := Complex.exp_eq_exp_iff_exists_int.mp hexp
  exact ⟨n, Γ, hlift, hΓ0, by rw [hn, add_sub_cancel_left]⟩

/-- **环路度**（定义层）：提升路径 `Γ` 的端点差除以 `2πI`。 -/
noncomputable def loopDegree (Γ : C(unitInterval, ℂ)) : ℂ :=
  (Γ 1 - Γ 0) / (2 * Real.pi * Complex.I)

/-- **环路度取整值**：任意闭路（`γ 0 = γ 1 = 1`、处处非零）的度恰等于某整数 `n ∈ ℤ`。 -/
theorem loopDegree_eq_int (γ : C(unitInterval, ℂ)) (h0 : γ 0 = 1) (h1 : γ 1 = 1)
    (hnz : ∀ t, γ t ≠ 0) :
    ∃ n : ℤ, ∃ Γ : C(unitInterval, ℂ), (∀ t, Complex.exp (Γ t) = γ t) ∧ Γ 0 = 0
      ∧ loopDegree Γ = n := by
  obtain ⟨n, Γ, hlift, hΓ0, hdiff⟩ := winding_integrality γ h0 h1 hnz
  have hz : (2 * Real.pi * Complex.I : ℂ) ≠ 0 :=
    mul_ne_zero (mul_ne_zero (by norm_num) (by exact_mod_cast Real.pi_ne_zero))
      Complex.I_ne_zero
  exact ⟨n, Γ, hlift, hΓ0, by rw [loopDegree, hdiff, mul_div_assoc, div_self hz, mul_one]⟩

end K0DegreeTheory

/-!
## §2.33 度的同伦不变性：闭合 §3 #4 的拓扑内核

§3 #4（陈数**绝热不变性**）的拓扑内核：**同伦的闭路有相同的度**。§2.32 已用覆盖映射
`Complex.isCoveringMap_exp` 的路径提升把任意闭路的度整性形式化；本层证明该度是**同伦不变量**——
这是「谱间隙不闭合的参数形变下 $C$ 不变」在**环路/度层面**的精确对应（参数形变给出闭路之间的同伦）。

关键工具：mathlib `IsCoveringMap.liftPath_apply_one_eq_of_homotopicRel`
（**相对端点同伦的两条路径，其从同一点出发的提升在终点重合**）——这正是覆盖空间理论中
单值化（monodromy）的基本定理。

交付：
- `expCover` + `expCover_isCoveringMap`：覆盖映射 $\exp:\mathbb C\to\mathbb C\setminus\{0\}$ 的全函数形式。
- `loopInSubtype`：处处非零环路视为 $\mathbb C\setminus\{0\}$ 中的连续映射。
- `loopLift`（**标准提升**，起点提升取 $0$）+ `loopLift_zero`。
- **`loopDegree_homotopy_invariant`**：相对端点同伦的处处非零闭路**度相同**。

诚实边界（随登）：本层闭合的是**度（环路层）的同伦不变性**——即 §3 #4 拓扑内核的环路形态。
完整的「陈数沿环面参数形变不变」仍需：$T^2$ 双参数版本（投影族 $P(k,\lambda)$ 的闭路族 + 双参数
同伦）与曲率被积 $F$ 的可积性/光滑性（Kato 微扰论层）；二者与群拓扑/环路度层相互独立，登记开放。
-/

section K0DegreeHomotopy

/-- 覆盖映射 `exp : ℂ → ℂ∖{0}`（全函数形式）。 -/
noncomputable def expCover : ℂ → {z : ℂ // z ≠ 0} :=
  fun z => ⟨Complex.exp z, Complex.exp_ne_zero z⟩

/-- `exp` 是覆盖映射（mathlib `Complex.isCoveringMap_exp`）。 -/
theorem expCover_isCoveringMap : IsCoveringMap expCover := Complex.isCoveringMap_exp

/-- 处处非零环路视为 `ℂ∖{0}` 中的连续映射。 -/
noncomputable def loopInSubtype (γ : C(unitInterval, ℂ)) (hnz : ∀ t, γ t ≠ 0) :
    C(unitInterval, {z : ℂ // z ≠ 0}) :=
  ⟨fun t => ⟨γ t, hnz t⟩, Continuous.subtype_mk γ.continuous hnz⟩

/-- **闭路的标准提升**：处处非零、起点为 `1` 的环路沿覆盖映射 `exp` 提升到 `ℂ`，
    起点提升取 `0`（因 `exp 0 = 1`）。 -/
noncomputable def loopLift (γ : C(unitInterval, ℂ)) (h0 : γ 0 = 1) (hnz : ∀ t, γ t ≠ 0) :
    C(unitInterval, ℂ) :=
  expCover_isCoveringMap.liftPath (loopInSubtype γ hnz) 0 (by
    refine Subtype.ext ?_
    simp [loopInSubtype, expCover, h0, Complex.exp_zero])

/-- **标准提升起点为 `0`**（`IsCoveringMap.liftPath_zero`）。 -/
theorem loopLift_zero (γ : C(unitInterval, ℂ)) (h0 : γ 0 = 1) (hnz : ∀ t, γ t ≠ 0) :
    loopLift γ h0 hnz 0 = 0 :=
  expCover_isCoveringMap.liftPath_zero _ _ _

/-- **度的同伦不变性**（§3 #4 拓扑内核）：相对端点同伦的处处非零闭路有**相同的度**。
    证明经 `IsCoveringMap.liftPath_apply_one_eq_of_homotopicRel`：同伦提升给出相同的提升终点，
    而两提升的起点同为 `0`（`loopLift_zero`），故端点差——即度——相同。
    闭路性由 `h0`（起点 = `1`）与 `H`（`HomotopicRel {0,1}`，含终点一致）编码。 -/
theorem loopDegree_homotopy_invariant
    {γ₀ γ₁ : C(unitInterval, ℂ)} (h0₀ : γ₀ 0 = 1) (hnz₀ : ∀ t, γ₀ t ≠ 0)
    (h0₁ : γ₁ 0 = 1) (hnz₁ : ∀ t, γ₁ t ≠ 0)
    (H : (loopInSubtype γ₀ hnz₀).HomotopicRel (loopInSubtype γ₁ hnz₁) {0, 1}) :
    loopDegree (loopLift γ₀ h0₀ hnz₀) = loopDegree (loopLift γ₁ h0₁ hnz₁) := by
  have hbase₀ : loopInSubtype γ₀ hnz₀ 0 = expCover 0 := by
    refine Subtype.ext ?_
    simp [loopInSubtype, expCover, h0₀, Complex.exp_zero]
  have hbase₁ : loopInSubtype γ₁ hnz₁ 0 = expCover 0 := by
    refine Subtype.ext ?_
    simp [loopInSubtype, expCover, h0₁, Complex.exp_zero]
  have hone : loopLift γ₀ h0₀ hnz₀ 1 = loopLift γ₁ h0₁ hnz₁ 1 :=
    expCover_isCoveringMap.liftPath_apply_one_eq_of_homotopicRel H 0 hbase₀ hbase₁
  rw [loopDegree, loopDegree, hone, loopLift_zero, loopLift_zero]

end K0DegreeHomotopy

/- §3 开放登记（paper14 G3 完整陈数理论，不占用 sorry，真证路径见下）：

  本模块建立了陈数理论的代数核心（Berry 曲率投影公式 + 实值性）。以下完整
  内容需要积分/拓扑度基础设施，登记为未来工作：

  1. **第一陈数积分定义**：C = (1/2π) ∫_{T²} F d²k（T² = 布里渊区环面）。
     需要：矩阵值函数在环面上的积分（mathlib MeasureTheory + 流形积分），
     以及 F 的连续性（⇐ P 光滑）。
     **→ 代数前提已闭合（2026-09-20，§2.7）**：被积函数作为**实值反对称双线性
     2-形式**的结构——实值性（§2 `berryCurvature_im_eq_zero`）+ 反对称
     `F(P,B,A)=-F(P,A,B)`（`berryCurvature_antisymm`）+ 双线性
     （`berryCurvature_add_left`/`berryCurvature_add_right`）+ 带内平移不贡献
     （`berryCurvature_shift_commute`/`berryCurvature_shift_const`）——即陈数
     密度"可作 2-形式积分"（$d^2k=dk_x\wedge dk_y$ 反对称）的代数刻画；
     环面积分本身与分析可微性仍登记开放。
     **→ 连续 S¹ 环绕数孢子已闭合（2026-09-20，§2.10）**：积分/度理论层首块
     `unitCircle_integral_inv`（单位圆留数 ∮dz/z=2πi）+ `unitCircle_windingNumber_eq_one`
     （归一化环绕数=1∈ℤ，恒等映射 $S^1\to S^1$ 度的整值实例——陈数整性在
     连续层的最简真证基石）；环面 $T^2$ 陈数被积的**积分承载形式**由
     `chernIntegralTorus`（`torusIntegral` 双参数积分）提供。环面上 $F$ 的
     可积性/光滑性（⇐ P 光滑）与完整归一化陈数仍登记开放。
     **→ 一维退化环面环绕数孢子已闭合（2026-09-20，§2.12）**：环面绕行整值的
     **$T^1$ 退化面**——`torusIntegral_dim1_winding`（一维环面
     $\iint_{T}$ 被积 $1/z_0$ = 单位圆留数 $2\pi i$，经 `torusIntegral_dim1`
     一维环面=圆周积分）+ `torusIntegral_dim1_windingNumber_eq_one`（归一化
     环绕数=1∈ℤ，环面一维退化切面 $S^1$ 上恒等映射度仍取整值——为二维环面
     整性陈数提供一维退化边界条件）。二维 $T^2$ 被积 $F$ 的完整归一化陈数与
     整性仍登记开放。
     **→ 二维环面双留数孢子已闭合（2026-09-20，§2.13）**：完整二维环面的
     **双极点留数整值**——`torusIntegral_dim2_double_inv`（$\iint_{T^2}
     z_0^{-1}z_1^{-1}d^2z=(2\pi i)^2$：按 `torusIntegral` 定义展开，参数立方
     Jacobi 因子 $\prod_i e^{\theta_i i}$ 与被积倒数消约成常数 $-1$，
     立方体积 $(2\pi)^2)$，$\mathrm{i}^2=-1$）+ `torusIntegral_dim2_windingNumber_eq_one`
     （$(2\pi i)^{-2}$ 归一化 $=1\in\mathbb{Z}$，二维复面双极点取整值——为环面
     陈数整性提供**二维连续积分层核心孢子**）。完整 $T^2$ 上一般被积陈数密度
     $F$ 的归一化陈数与整性仍登记开放（需完整度理论/同伦提升基建）。
  2. **整性定理**：C ∈ ℤ。这是陈数理论的拓扑核心，需度理论/同伦提升论证
     （或 Atiyah-Singer 指标的特殊化），有限维代数原型内不可达。
     **→ 代数种子已闭合（2026-09-20，§2.8）**：占据数 = 秩 ∈ ℤ
     （`trace_eq_rank_of_idempotent`：幂等阵迹 = 秩——占据带投影的迹（占据数）
     等于占据带维数（秩）的整数代数根源）；完整陈数 C 的整性（度理论/同伦
     提升论证）仍登记开放。
  3. **TKNN 公式**（paper14 定理 3.1）：σ_xy = (e²/h)·C。需 Kubo 线性响应
     或 Laughlin 泵浦论证，属连续场论形式化（远期）。
  4. **陈数绝热不变性**（paper14 命题 3.1）：谱间隙不闭合的参数形变下 C 不变。
     需同伦不变性 + 积分定义的连续依赖性。
     **→ 代数种子已闭合（2026-09-20，§2.8）**：谱投影沿相似变换 P ↦ U·P·U⁻¹
     （谱流/绝热演化的代数形式）保持幂等且秩不变——占据数（秩）沿绝热形变
     守恒（`idempotent_conj_inv`/`rank_conj_inv_idempotent`）；完整陈数的同伦
     不变性（谱间隙不闭合的参数形变的同伦论证）仍登记开放。
     **→ 环绕数整值的模型族已闭合（2026-09-24，§2.31）**：连续积分层第二块基石——
     `circleIntegral_const_mul_inv`（圆周积分常数倍线性）+ `logDeriv_pow`
     （`z ↦ z^n` 的对数导数 `f'/f = n/z`）+ **`unitCircle_windingNumber_pow`**
     （**`z ↦ z^n` 的环绕数 = n ∈ ℤ**，陈数整性在连续积分层的首个非平凡模型族；
     §2.10 仅覆盖 $n=1$）。**重大发现（随登）**：经实地勘查，mathlib **完全缺失**
     `windingNumber` 与度理论基建（`Mathlib/Analysis/Complex` 无任何 `windingNumber`/
     `IsInteger`/`Homotopic`+环路积分引理），故一般度理论（路径提升 $S^1\to\mathbb R$、
     度的同伦不变性、$T^2$ 双参数版本）须**从零搭建**，属远期工程；曲率被积 $F$ 的
     可积性/光滑性（⇐ $P(k)$ 光滑，Kato 微扰论层）亦登记开放。
     **→ 一般度理论第一层已闭合（2026-09-24，§2.32）**：连续积分层第三块基石——用
     `Complex.isCoveringMap_exp`（`exp : ℂ → ℂ∖{0}` 是**覆盖映射**）的**路径提升**把
     任意闭路提升到 `ℂ`，配合周期性核 `Complex.exp_eq_exp_iff_exists_int` 得
     **环路度 ∈ ℤ**：`exists_exp_lift`（环路提升）+ `winding_integrality`
     （提升端点差 = `n·2πI`）+ `loopDegree`（度定义）+ `loopDegree_eq_int`
     （**度取整值**，把整性从模型族推广到**任意闭路**）。**同伦不变性**（§3 #4 内核）
     已定位到 `IsCoveringMap.liftPathQuotient`，下一层可闭合；$T^2$ 双参数版本与
     $F$ 的可积性/光滑性仍登记开放。
     **→ 度的同伦不变性已闭合（2026-09-24，§2.33）**：**§3 #4 的拓扑内核**——数学工具
     `IsCoveringMap.liftPath_apply_one_eq_of_homotopicRel`（相对端点同伦的两条路径，从同一点
     出发的提升在**终点重合**，即覆盖空间单值化定理）：`expCover`/`expCover_isCoveringMap` +
     `loopInSubtype` + `loopLift`（标准提升）+ `loopLift_zero` + **`loopDegree_homotopy_invariant`**
     （**相对端点同伦的处处非零闭路度相同**）。至此「$C$ 沿参数形变不变」在**环路/度层**的
     拓扑内核已形式化。仍登记开放：$T^2$ 双参数版本（投影族 $P(k,\lambda)$ 的闭路族 + 双参数
     同伦）与 $F$ 的可积性/光滑性（Kato 微扰论层）。
     **→ $T^2$ 版的正确表述（2026-09-24 勘查结论，重要）**：**不能**把「陈数绝热不变性」的
     $T^2$ 版理解为「某个 $T^2\to S^1$（或 $S^2\to S^1$）映射的二维度」——因
     $\pi_2(S^1)=0$，**二维度不存在**。$T^2$ 版的正确表述是**「基点为 $1$ 的环路族」的度沿
     绝热参数不变**：设 `γ : C(I × I, ℂ)` 处处非零且每条 `l`-切片都是基点 `1` 的闭路
     （`γ (0, l) = 1`、`γ (1, l) = 1`），则 `loopDegree (slice γ 0) = loopDegree (slice γ 1)`
     ——其证明**归约到 §2.33**（同伦即 `γ` 自身，作为 `slice γ 0` 与 `slice γ 1` 之间相对
     `{0,1}` 的同伦）。**待办的唯一技术障碍**：构造实例 `HomotopicRel := Nonempty (HomotopyRel _ _ _)`
     时其 `HomotopyRel.prop'` 字段的绑定形态尚未确定（`Mathlib/Topology/Homotopy/Basic.lean`
     中 `HomotopyRel` 的定义处需核对）；数学内容与归约路径均已明确。
     而**数值陈数**（二维不变量）本身来自**曲率积分**（Chern–Weil / 线丛过渡函数路线），
     与度理论正交，需 $F$ 的可积性/光滑性（Kato 层），仍登记开放。
  5. **规范不变性细节**：用本征矢量表示的 Berry 联络 A = i⟨u|∇u⟩ 在
     u ↦ e^{iθ}·u 下不变，且 F = dA 与投影公式一致（需微分形式恒等式）。
     **→ 代数核心已闭合（2026-09-19，§2.6）**：曲率对酉稳定化 $P\mapsto UPU^\dagger$
     不变（`berryCurvature_unitary_conj`），及规范无关的实值性保持
     （`berryCurvature_unitary_conj_im_eq_zero`）——"曲率只依赖占据带投影、与
     本征态相位无关"论断就此形式化；联络层面（$u\mapsto e^{i\theta}u$、$F=dA$）
     仍需微分形式恒等式，登记开放。
  6. **切向量的分析构造**：投影族 P(k) = cfc occFn(H(k)) 对参数的可微性
     （Kato 微扰论层）——其纯代数后件（约束方程、带间化简、双交换子形式）
     已由 §2.5 闭合，分析构造本身仍需微积分基础设施。
  7. **同秩投影酉等价（K₀ = ℤ 度理论整性核心）**：任意两个同秩（同维）幂等
     谱投影 P、Q（rank P = rank Q）在有限维中酉等价（∃ 酉 U，Q = U·P·U†）。
     这是度理论/同伦层整性（§3 #2 的"同秩谱投影 → 陈指数 → K₀(ℂ) = ℤ → C ∈ ℤ"）
     的**张量细化**：陈数整性最终来自 K₀(ℂ) ≅ ℤ，而 K₀ 的生成/自由交换群结构
     以"同维投影酉等价 → 同伦类与秩一一对应"为代数支柱。属同伦层开放项，
     需完整酉群 U(n) / K₀ 处理。
     **→ 离散 S¹ 的代数底胞已闭合（2026-09-20，§2.9）**：占据-空带互补守恒
     `rank P + rank(1−P) = n`（`rank_add_complement_idempotent`）与补秩
     `rank(1−P) = n − rank P`（`complement_rank`）是"陈数扰动能在占据/空带间
     转移但总量（总带数 n）守恒"的秩论细胞（补投影幂等 `complement_idempotent`），
     同伦层首个基建模块。
     **→ 迹类一致/互补类对称已闭合（2026-09-20，§2.11）**：同秩幂等投影必然同
     迹 $\mathrm{Tr}\,P=\mathrm{Tr}\,Q\in\mathbb{Z}$（`trace_eq_of_rank_eq_idempotent`
     ——K₀ 秩定类的**迹同态**种子：$K_0(\mathbb{C})\to\mathbb{Z}$ 由 $\mathrm{Tr}$ 显式
     实现）且补投影亦同秩（`complement_rank_eq_of_rank_eq`，占据/空带互补类对称）；
     这些是「秩唯一决定 K₀ 类」的**迹特征**代数种子。真正的酉等价构造
     （∃ 酉 U，Q=U·P·U†）与相似共轭构造（∃ 可逆 S）在连续 S¹/环面上仍登记
     开放，需完整等距/酉群/K₀ 基建。
     **→ 自伴正交分解与相似共轭构造已闭合（2026-09-20，§2.14）**：在有限维复
     内积空间中，自伴幂等投影满足 $\ker=(\operatorname{range})^\perp$
     （`selfAdjoint_idempotent_ker_eq_orthogonal`，自伴幂等 ⟺ 正交投影）+ 任意
     两个同秩幂等投影相似 `∃ S : E ≃ₗ E, S∘P = Q∘S`
     （`similar_conj_projections_of_eq_finrank`，幂等分解
     `IsIdempotentElem.isCompl`+`prodEquivOfIsCompl`、同秩经 finrank 加性析出
     核同维 + `LinearEquiv.ofFinrankEq` → `LinearEquiv.prodCongr` 显式构造 S，
     辅以对角化引理 `idempotent_apply_of_mem_range`/`_mem_ker`）——「秩唯一决定
     相似类」的**线性共轭支柱**（§3 #7 中「相似共轭构造 ∃ 可逆 S」闭合）。
     **→ 酉（等距）强化已闭合（2026-09-20，§2.14）**：把相似共轭升级为**保内积酉
     共轭**——任意同秩自伴幂等（正交投影）投影存在酉 $U$ 满足 $Q\circ U=U\circ P$
     （即 $Q=U\circ P\circ U^{-1}$，$U^\dagger=U^{-1}$）：
     `same_rank_selfAdjoint_idempotent_unitary_conj`。构造经引理 A
     `exists_isometry_of_eq_finrank`（同维子空间间存在等距等价：`stdOrthonormalBasis`
     + `Equiv.cast` + `OrthonormalBasis.equiv`，占据带 $\operatorname{range}P\simeq
     \operatorname{range}Q$）+ 引理 B `linearIsometryEquiv_of_submodule`（`LinearIsometry.extend`
     + `toLinearIsometryEquiv` 把子空间等距延伸为全空间等距）+ 作用引理
     `linearIsometryEquiv_of_submodule_apply`（$U|_{S}=e$）+ 引理 C
     `linearIsometryEquiv_of_submodule_mem_orthogonal`（$U(S^\perp)\subseteq T^\perp$，核分量
     落零占据侧）；在正交直和 $E=\operatorname{range}P\oplus\ker P$ 上逐段验证。
     ——「秩唯一决定酉等价类」的**等距/酉支柱**（§3 #7 中「完整酉等价 ∃ U = P·U·P†」
     在有限维内积层的**代数 + 等距闭合**）。
     **→ 酉等价类 = 秩的显式双射已闭合（2026-09-20，§2.14 尾）**：把酉构造闭合为
     **双向分类**——`same_rank_iff_unitary_conj`：
     $\operatorname{rank}P=\operatorname{rank}Q \iff \exists$ 酉
     $U:E\simeq_{\mathbb C}E,\,Q\circ U=U\circ P$，两方向均由有限维代数层闭合：
     前向（酉构造）`same_rank_selfAdjoint_idempotent_unitary_conj`（引理 A/B/C），
     反向（映射/定量）`finrank_eq_of_unitary_conj`——保内积等价 $U$ 把
     $\operatorname{range}P$ 双射映到 $\operatorname{range}Q$（`Submodule.map` 像等式 +
     `LinearEquiv.submoduleMap` 下降受限等价 + `LinearEquiv.finrank_eq`）。这是
     §3 #7「秩唯一决定酉等价类」即 $K_0(\mathbb{C})\to\mathbb{Z},\,[\mathbb{C}^r]\mapsto r$
     在投影层的**逐投影显式双射**（每对同秩投影酉等价、酉等价者同秩）。
     **→ K₀ 秩映射的直和加性种子已闭合（2026-09-20，§2.15）**：把「秩 ⇔ 酉类」
     的集合双射向 **K₀(ℂ) ≅ ℤ 的加法幺半/群同态**升级——任意两个（幂等）谱投影
     P、Q 的直和（块对角）$P\oplus Q:=P.\mathrm{prodMap}\,Q:E\times F\to E\times F$
     仍幂等（`directSum_idempotent`，经 `LinearMap.prodMap_mul`）且其秩为分量秩之和
     `directSum_rank_add`：$\operatorname{rank}(P\oplus Q)=\operatorname{rank}P
     +\operatorname{rank}Q$（`LinearMap.range_prodMap` 像=子空间乘积 +
     `prodSubmoduleLinearEquiv`（子空间乘积 ⟶ 类型级乘积线性等价，收紧
     $\operatorname{finrank}(S.\mathrm{prod}\,T)=\operatorname{finrank}S+
     \operatorname{finrank}T$）+ `Module.finrank_prod`）——「秩定类」的**加法结构**
     代数种子：秩沿直和相加，把秩映射从集合分类提升为**幺半群同态**。
     **→ K₀ 生成/自由交换群结构基底已闭合（2026-09-22，§2.16）**：把「秩 ⇔ 酉类」
     同秩双射（§2.14）与直和加性（§2.15）的连接目标落实为 **K₀(ℂ)≅ℤ 的生成/
     自由交换群基底**——自由交换群在**单个生成元**（占据带类别 `PUnit`）上同构于
     ℤ：`single_generator_freeAbelian_iso_int`（mathlib
     `FreeAbelianGroup.uniqueEquiv`，$\operatorname{FreeAbelianGroup}(\mathrm{PUnit})
     \cong\mathbb{Z}$）+ 秩签名 `rank_signature_lift`（`FreeAbelianGroup.lift`
     泛性质：任意生成元带 ↦ 整数唯一扩展为群同态）+ `rank_signature_single_eq`
     （单生成元签名取 $1\in\mathbb{Z}$）+ `single_signature_unique`（签名唯一性）。
     这是「K₀(ℂ)→ℤ,[ℂ^r]↦r」在**生成元层**的显式取值：每个整数对应一个
     占据带维数（秩）的自由交换群签名。
     **诚实边界（随登）**：有限维层酉等价 + 其「秩 ⇔ 酉类」双射（§2.14）、
     K₀ 秩映射的幂等性与秩加性种子（§2.15）、以及**纯代数自由交换群层**
     （单生成元 ≃ ℤ + 秩签名 lift 泛性质，§2.16）已闭合；同秩酉类的**商载体**
     （§2.17：酉等价 Setoid + 商类型 + 秩完全不变量良定义）已闭合；同秩酉类的
     **商秩不变量强化**（§2.18：商秩单射分类器 + 可扩性 ⟺ 同秩 + 值域界——
     「酉类=秩」的完全不变量在商层完全锁定）已闭合；**商加法的对象层载体**
     （§2.19：跨空间直和 $P\oplus Q$ 的商良定性——L²-乘积 `WithLp 2 (E×F)`
     `InnerProductSpace` 实例 + 幂等/自伴封闭 `projDirectSum` + 秩加性
     `projDirectSumMap_rank_add`/`quotientRank_projDirectSum_add` +
     商线性 `projDirectSum_wellDefined`）已闭合；**把商构成群的 Grothendieck 群完成**
     （§2.20：ℕ 的 split-exact 完成 `GrothRel`/`grothSetoid`/商类型 `GrothQuot` +
     rank 差同态 `grothToInt` 的单射/满射 ⟹ `grothToIntEquiv : GrothQuot ≃ ℤ` +
     经 `Function.Injective.addCommGroup` 构成 `AddCommGroup` + 群同构
     `grothToIntIso : GrothQuot ≃+ ℤ` + 群运算良定 `grothAdd_mk_eq`/`grothNeg_mk_eq`/
     `grothZero_eq` + 与 §2.16 会师 `grothQuot_to_freeAbelian` + 投影层 Grothendieck
     关系 ⇔ 秩层判据 `projGrothRel_iff`）已闭合；**对象层投影商类的分类器层**（§2.21：
     `projGrothRel` 构成 Setoid `projGrothSetoid` + 投影差对象商 `ProjDiffQuot E` +
     秩差完全不变量 `projToInt`（`Quotient.lift` 良定 + 单射）+ 与秩层 `grothToInt` 因子
     交接 `projToInt_eq_grothToInt` + 直和加性种子 `projToInt_projDirectSum_add`）也已闭合；
     **对象层分类器的精确值域**（§2.22：各秩投影可实现 `projOfRank`（`stdOrthonormalBasis`
     前 $k$ 基向量张成 $U_k$ 的 `starProjection`，幂等+自伴+秩恰 $k$ `projOfRank_rankE`）+
     整数值可达 `projToInt_reaches_nat`/`_neg` + 值域上界 `projToInt_mem_range_Icc` +
     值域恰为有界区间 `projToInt_range_Icc`：$\mathrm{range}\,(\mathrm{projToInt}\,E)
     =\{r\in\mathbb{Z}\mid -\dim E\le r\le\dim E\}$ + 像非加法子幺半群
     `projToInt_range_not_submonoid`（$\dim E\ge1$ 时 $a=b=\alpha$、$2\alpha\notin[-\alpha,\alpha]$））
     也已闭合；**对象层 K₀(ℂ)≅ℤ 的跨维度分组/生成基座**（§2.23：跨维度标准空间
     `canonicalSpace n = EuclideanSpace ℂ (Fin n)`（`canonicalSpace_finrank`）+ 秩-1 类
     `rankOne_class_projToInt`/`rankOne_class_any_dim`（$[\mathbb{C}^1]\mapsto1$，跨维度一致）+
     跨维度满射 `crossDim_reaches_any`（每个整数都被某维数标准空间投影类实现，$\mathbb{Z}$ 满射）+
     Grothendieck 群由秩-1 类生成 `grothQuot_generated_by_one`（每类都是 $[\mathbb{C}^1]$ 的 $\mathbb{Z}$ 倍，
     配 `grothOneClass`/`grothToInt_grothOneClass`）+ 对象层分类器即秩 `projClass_int_eq_rank`
     （$\mathrm{projToInt}\,E\,[P,0]=\operatorname{rank}P$））也已闭合；**对象层完整群结构 ≅ ℤ**
     （§2.24：跨维度和型等距 `canonicalSpaceAddIso`（`ℂ^{n+m} ≃ₗᵢ ℂ^n × ℂ^m`，经
     `PiLp.sumPiLpEquivProdLpPiLp` + `finSumFinEquiv`）+ 沿等距共轭投影 `conjProj`（幂等 + 自伴 +
     保秩 `conjProj_rank`）+ 规范直和投影 `projDirectSumCanon`（秩加性 `projDirectSumCanon_rank`、
     分类器加性 `projToInt_projDirectSumCanon_add`）+ 跨维度对象层载体 `ProjPoint = Σ n, ProjDiffQuot (ℂ^n)`
     （直和加法 `+`、整体秩加性 `projPointRank_add`）+ 对象层 K₀ 类 `ProjClass`（`projClassRank` 单射
     `projClassRank_injective` + 满射 `projClassRank_surjective`（§2.23 `crossDim_reaches_any`）⟹
     `projClassEquiv : ProjClass ≃ ℤ`）+ **对象层群结构** `projClassAddCommGroup`（`Function.Injective.addCommGroup`
     从 ℤ 传送）+ **群同构** `projClassRankIso : ProjClass ≃+ ℤ` + **自然性** `projClassMk_add`
     （类加法恰由跨维度直和实现 `[a]+[b]=[a⊕b]`））也已闭合——§2.20 秩层 Grothendieck 群 `GrothQuot ≃+ ℤ`
     的**对象层显式实现**；**酉群作用层**（§2.25：酉群 `unitaryEnd E = E ≃ₗᵢ[ℂ] E` + 共轭作用
     `u • P := u P u⁻¹` 做成 `MulAction`（`unitaryConjAct`，复用 §2.24 `conjProj`）+ 保秩
     `unitaryConjAct_rank` + 保持酉类 `unitaryConjAct_rel` + **轨道 = 秩类**
     `mem_orbit_iff_same_rank`/`orbit_eq_rankClass` + 轨道相等 ⟺ 秩相等 `orbit_eq_iff_same_rank` +
     秩实现 `exists_projRank_eq`（§2.22 `projOfRank`）+ **轨道空间 ≃ 秩集**
     `orbitQuotEquivRankSet : Quotient (orbitRel) ≃ {k // k ≤ dim E}`（轨道数 = dim E+1））
     也已闭合——把 §2.21 的**逐对**酉双射提升为**轨道分解**；**对象层 K₀ 的等距自然性**（§2.26：
     等距诱导差类映射 `conjProjQuot`（`Quotient.lift` 良定）+ 分类器交换 `conjProjQuot_projToInt`/
     等距不变量 `projToInt_conjProj` + 双射 `conjProjQuotEquiv` + 函子性 `conjProjQuot_trans`/
     `conjProjQuot_refl` + **酉作用平凡** `conjProjQuot_unitary_fixed`（K₀ 是酉不变量））也已闭合；
     **酉群连通性拓扑基建（第一层）**（§2.27：`Matrix n n ℂ` 经 `open scoped Matrix.Norms.L2Operator`
     成 C\*-代数 ⟹ 实例化 mathlib `Unitary` 酉群拓扑理论——`unitaryGroup_locallyPathConnected`
     （局部路径连通）+ `unitaryGroup_joined`（小距离路径连通）+ `unitaryGroup_isPathConnected_ball`
     （半径 < 2 球路径连通）+ `mem_pathComponent_one_iff_products`（`1` 的路径分量 = 有限个自伴指数之积）
     + `unitaryGroup_entry_norm_le_one`（有界性）+ **连通性归约** `pathConnectedSpace_unitaryGroup_of_products`
     （指数积覆盖 ⟹ 路径连通））也已闭合；**全局连通性归约强化**（§2.28：指数取逆公式
     `expUnitary_neg` + `pathComponent 1` **子群**（`expUnitary_mem_pathComponent_one`/
     `one_mem_pathComponent_one`/`mul_mem_pathComponent_one`/`inv_mem_pathComponent_one`
     （经辅助引理 `reverse_map_neg_prod_mul_prod`））+ **「避开 `-1`」子类闭合**
     `mem_pathComponent_one_of_norm_sub_lt_two` + **连通性判据**
     `pathConnectedSpace_unitaryGroup_of_mem_pathComponent_one`）也已闭合——全局连通性化归为
     **单一群论命题** `∀ u, u ∈ pathComponent 1`；**矩阵谱有限性**（§2.29：`matrix_spectrum_finite`
     （谱 = 特征多项式根集 ⟹ 有限，`Matrix.mem_spectrum_iff_isRoot_charpoly` + `mem_roots`）+
     `matrix_spectrum_finite'`（`Finite ↥(spectrum ℂ A)` 类型类形式）+ `unitary_spectrum_finite`）
     也已闭合——“旋转 + 指数”路线的最后一块基建就位；**全局连通性收口**（§2.30：**单位圆无穷**
     `unitCircle_infinite`（半圆参数化 `x ↦ (x, √(1-x²))` 落在单位圆且单射）+ **标量谱变换**
     `smul_mem_spectrum_iff`（`z ∈ spectrum (c • a) ↔ c⁻¹z ∈ spectrum a`，`c ≠ 0`）+
     `exists_norm_eq_one_notMem_neg` + `neg_one_notMem_spectrum_smul_one` + `smul_unitary_mem_unitary` +
     `scalar_smul_one_mem_pathComponent_one`/`smul_unitary_mem_pathComponent_one` +
     `mem_pathComponent_one_unitary`（**每个酉元都是有限个自伴指数之积**）+ `exists_expUnitary_prod_eq` +
     **`pathConnectedSpace_unitaryGroup`**（$U(n)$ **路径连通**）+ `connectedSpace_unitaryGroup`）
     也已闭合——「旋转 + 指数」论证：`u = (ζ • 1) · (ζ⁻¹ • u)`，两因子各由 §2.28 判据落入
     `pathComponent 1`；
     但仍登记开放：环面上陈数密度 $F$ 的连续场论/度理论整性
     （含同伦提升：谱间隙不闭合参数形变下 $C$ 不变，§3 #4）——需 $F$ 的可积性/光滑性与环面积分层面的
     度理论，与 §2.30 的群拓扑连通性相互独立，登记开放。

  已闭合（本模块，零 sorry）：Berry 曲率投影公式 + 实值性（陈数良定义的
  代数基础）+ 投影切向量代数层（projTangent_intraBand_zero 带内消没 /
  trace_proj_commutator_interband 带间化简 / berryCurvature_interband 带间
  形式 / trace_proj_commutator_twoCommutator 双交换子形式）+ 规范不变性
  （berryCurvature_unitary_conj 酉稳定化不变 / berryCurvature_unitary_conj_im_eq_zero
  规范无关实值性）+ 2-形式结构（berryCurvature_antisymm 反对称 /
  berryCurvature_add_left、berryCurvature_add_right 双线性 /
  berryCurvature_shift_commute、berryCurvature_shift_const 带内平移不贡献，
  §2.7）+ 整性/绝热不变性的代数种子（trace_eq_rank_of_idempotent 幂等阵迹
  = 秩 ∈ ℤ / idempotent_conj_inv 共轭保持幂等 / rank_conj_inv_idempotent
  相似变换秩守恒，§2.8）+ 离散 S¹ 绕行的代数底胞（complement_idempotent
  补投影幂等 / rank_add_complement_idempotent 占据+空秩=总带数 /
  complement_rank 补秩，§2.9）+ 连续 S¹ 环绕数孢子（unitCircle_integral_inv
  单位圆留数 ∮dz/z=2πi / unitCircle_windingNumber_eq_one 归一化环绕数=1∈ℤ，
  度理论整值在连续积分层的最简真证基石 / chernIntegralTorus 环面陈数被积的
  积分承载形式定义，§2.10）+ 同秩投影的 K₀ 迹同态种子（trace_eq_of_rank_eq_idempotent
  同秩幂等投影同迹 ∈ ℤ / complement_rank_eq_of_rank_eq 同秩投影补亦同秩，
  占据-空带类对称——秩唯一决定 K₀ 类的迹特征，§2.11）+ 一维退化环面环绕数孢子
  （torusIntegral_dim1_winding 一维环面被积 1/z₀ = 单位圆留数 2πi /
  torusIntegral_dim1_windingNumber_eq_one 归一化环绕数=1∈ℤ——环面绕行整值的
  $T^1$ 退化面，为二维环面整性陈数提供一维退化边界条件，§2.12）+ 二维环面
  双留数孢子（torusIntegral_dim2_double_inv 双极点留数 $\iint_{T^2}z_0^{-1}
  z_1^{-1}d^2z=(2\pi i)^2$——torusIntegral 定义展开参数立方 Jacobi 与被积消约
  成常数 $-1$、立方体积 $(2\pi)^2$ / torusIntegral_dim2_windingNumber_eq_one
  $(2\pi i)^{-2}$ 归一化=1∈ℤ——二维复面双极点取整值，环面陈数整性的二维连续
  积分层核心孢子，§2.13）+ 自伴正交分解与相似共轭构造（
  selfAdjoint_idempotent_ker_eq_orthogonal 自伴幂等 ⟹ ker=(range)ᗮ——自伴幂等
  ⟺ 正交投影的酉前提 / similar_conj_projections_of_eq_finrank 同秩幂等投影
  相似 ∃S:S∘P=Q∘S——「秩唯一决定相似类」的线性共轭支柱，幂等分解 +
  prodEquivOfIsCompl + LinearEquiv.ofFinrankEq，辅以 idempotent_apply_of_mem_range/
  _mem_ker 对角化，§2.14）+ 同秩投影的酉（等距）等价（
  exists_isometry_of_eq_finrank 同维子空间间等距等价：stdOrthonormalBasis +
  Equiv.cast + OrthonormalBasis.equiv / linearIsometryEquiv_of_submodule +
  _apply + _mem_orthogonal 子空间等距延伸为全空间等距且保正交补
  （LinearIsometry.extend + toLinearIsometryEquiv）/
  same_rank_selfAdjoint_idempotent_unitary_conj 同秩自伴幂等投影酉等价
  ∃U:Q∘U=U∘P（Q=U·P·U†，U†=U⁻¹）——「秩唯一决定酉等价类」的等距/酉支柱，
  正交直和上逐段验证，§2.14）+ 酉等价类=秩的显式双射（
  finrank_eq_of_unitary_conj 等比共轭 ⟹ 同秩——保内积 U 把 range P 双射映到
  range Q：Submodule.map 像等式 + LinearEquiv.submoduleMap 受限等价 +
  LinearEquiv.finrank_eq / same_rank_iff_unitary_conj 同秩 ⇔ 酉等价——「秩唯一
  决定酉等价类」即 K₀(ℂ)→ℤ,[ℂ^r]↦r 在投影层的逐投影显式双射，两方向皆有限维
  代数层闭合，§2.14 尾）+ K₀ 秩映射的直和加性种子（
  prodSubmoduleLinearEquiv 子空间乘积 ⟶ 类型级乘积线性等价（Submodule.mem_prod
  双向判定 + ext <;> rfl）/ directSum_idempotent 幂等直和仍幂等（LinearMap.prodMap_mul）/
  directSum_rank_add 秩沿直和相加：rank(P⊕Q)=rankP+rankQ——「秩定类」加法结构种子，
  LinearMap.range_prodMap + prodSubmoduleLinearEquiv + Module.finrank_prod，§2.15）
  + K₀ 生成/自由交换群结构基底（single_generator_freeAbelian_iso_int 单生成元
  自由交换群 ≃ ℤ（FreeAbelianGroup.uniqueEquiv，PUnit）——K₀(ℂ)≅ℤ 生成/自由交换
  群结构基底 / rank_signature_lift 秩签名 lift：任意生成元带 ↦ 整数唯一扩展为
  群同态（FreeAbelianGroup.lift 泛性质）/ rank_signature_single_eq 单生成元签名
  取 1∈ℤ / single_signature_unique 签名唯一性——「K₀(ℂ)→ℤ,[ℂ^r]↦r」在生成元层的
  显式取值，§2.16）+ 同秩酉类的商幺半群载体（
  SelfAdjointIdemProj 自伴幂等投影子类型（IsIdempotentElem ∧ IsSymmetric）/
  ProjUnitaryRel 酉等价关系（Q∘U=U∘P，U†=U⁻¹）/ projUnitaryRel_refl（U=1）+
  _symm（U⁻¹）+ _trans（U₁.trans U₂）——酉等价是等价关系 /
  projUnitarySetoid（反身+对称+传递 ⟹ Setoid）/ rank_well_defined_on_quotient
  （同酉类同秩，finrank_eq_of_unitary_conj——秩不完备等价类的完全不变量）/
  quotientRank（商类型上秩函数，Quotient.lift 良定义）——「K₀ 商代数」载体构造，
  §2.17）+ K₀ 商秩的不变量强化（quotientRank_injective 商秩单射——不同酉类不同秩，
  经 same_rank_iff_unitary_conj 前向 + Quotient.sound；quotientRank_ext 商相等 ⟺
  同秩（可扩性：良定义 + 单射合并）；quotientRank_le_dim 商秩 ≤ dim E
  （Submodule.finrank_le 值域上界）——"酉类=秩"的完全不变量在商层完全锁定，
  Grothendieck 化的分类器落点，§2.18）+ K₀ 商加法的对象层载体（
  toL2/fromL2 原始乘积 ⟷ L²-乘积 `WithLp 2 (E×F)` 的提升线性等价 /
  projDirectSumMap 块对角投影 + projDirectSumMap_idempotent/_symmetric
  幂等+自伴封闭 / projDirectSum 包装为 SelfAdjointIdemProj（跨空间直和的对象构造）/
  projDirectSumMap_rank_add 直和秩加性：rank(P⊕Q)=rankP+rankQ（toL2.submoduleMap
  保 finrank + directSum_rank_add）/ quotientRank_projDirectSum_add 商秩直和加性
  （[ℂ^r]⊕[ℂ^s]↦r+s，商加法分类器层）/ projDirectSum_wellDefined 商加法良定性
  （P~P'∧Q~Q'⟹(P⊕Q)~(P'⊕Q')，same_rank_iff_unitary_conj + 秩加性，商线性）——
  Grothendieck 化的**商加法对象载体**（含商加法与商秩加性分类器对齐），§2.19）
  + K₀ 的 Grothendieck 群完成（GrothRel 差对等价 $(a,b)\sim(c,d)\iff a+d=b+c$ +
  grothRel_refl/_symm/_trans + grothSetoid（反身+对称+传递 ⟹ Setoid）/
  GrothQuot ℕ 的群完成载体 / grothToInt 秩差同态（Quotient.lift 商上良定义）/
  grothToInt_injective 单射（零差唯一决定差类）/ grothToInt_surjective 满射
  （非负取(r,0)、负取(0,s)，Int.toNat_of_nonneg）/ grothToIntEquiv : GrothQuot ≃ ℤ /
  grothQuotAddCommGroup 商构成 AddCommGroup（Function.Injective.addCommGroup 传送）/
  grothIntHom 群同态 / grothToIntIso : GrothQuot ≃+ ℤ（AddEquiv.ofBijective）
  ——K₀(ℂ)≅ℤ 的 Grothendieck 群层实现 / grothToInt_add 加法保持 /
  grothAdd_mk_eq 自然加法=逐分量共合 / grothNeg_mk_eq 负数良定
  （-[a,b]=[b,a]）/ grothZero_eq 零良定（0=[0,0]）/ grothQuot_to_freeAbelian
  与 §2.16 自由交换群会师（GrothQuot ≃+ FreeAbelianGroup PUnit，两条实现路径一致）/
  projGrothRel 投影层 Grothendieck 关系（P⊕Q'~P'⊕Q）/ projGrothRel_iff 投影 Groth
  关系 ⇔ 秩层加法等式（quotientRank_projDirectSum_add 直和秩加性，split-exact 商
  关系在秩层判据）/ grothToInt_of_rank_diff 商秩差对送到 grothToInt=秩之差（分类器
  与格罗滕迪克商协调），§2.20）+ 对象层投影商类的分类器层（
  projGrothRel_refl/_symm/_trans 投影层 Groth 关系的反身/对称/传递（经 projGrothRel_iff
  降到秩层加法等式，§2.20 GrothRel）+ projGrothSetoid 投影差对 Groth 关系构成 Setoid
  （差对象商类型合法存在）/ ProjDiffQuot 对象层差商类型（差对象 [P]-[Q]）/
  projMk 代表元构造 / projToInt 秩差完全不变量（Quotient.lift 商上良定义，
  [(P,Q)]↦rankP-rankQ）/ projToInt_mk 代表元计算 / projToInt_injective 单射
  （不同差对象 ⟹ 不同秩差，Quotient.sound + grothToInt_injective + Quotient.exact）/
  projToInt_eq_grothToInt 与秩层 grothToInt 因子交接（嵌入 GrothQuot ≃+ ℤ）/
  projToInt_projDirectSum_add 直和加性种子（分类器沿跨空间直和分解）——
  "投影商类作为对象层 K₀ 结构的分类器层"（单射完全是变量），§2.21）+ 对象层分类器的
  精确值域（projOfRank 各秩投影可实现：stdOrthonormalBasis 前 k 基向量张成 U_k 的
  starProjection，isSymmetricProjection_starProjection 幂等+自伴 /
  projOfRank_rankE 秩恰为 k（finrank_span_eq_card + range_starProjection）/
  projOfRank_rank 商上取值 / projZero_rank 秩 0 特例 / projToInt_reaches_nat 非负可达
  =k / projToInt_reaches_neg 负可达 =-k / projToInt_mem_range_Icc 值域上界
  （rank 界于 [0,dim E]，quotientRank_le_dim）/ projToInt_range_Icc 值域恰为
  有界区间 {r∈ℤ | -dim E≤r≤dim E}（满射 + §2.21 单射 ⟹ 到有界区间双射）/
  projToInt_range_not_submonoid 像非 ℤ 加法子幺半群（dim E≥1 时 a=b=α、a+b=2α∉[−α,α]，
  闭会展碍），§2.22）。 -/

end MUFPF
