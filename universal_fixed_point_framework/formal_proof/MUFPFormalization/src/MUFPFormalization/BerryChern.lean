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
  §3 开放登记：第一陈数积分定义、整性、TKNN、规范不变性详细形式

说明：取厄米性假设为显式等式 hP : P = Pᴴ（等价于 Matrix.IsHermitian，但避免
其结构包装使 rw 直接可用）。核心引理只用迹循环性 + 厄米性 + 共轭转置反自同构，
不依赖幂等性，故对任意厄米三件套成立。
-/

import Mathlib.Data.Complex.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
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

/- §3 开放登记（paper14 G3 完整陈数理论，不占用 sorry，真证路径见下）：

  本模块建立了陈数理论的代数核心（Berry 曲率投影公式 + 实值性）。以下完整
  内容需要积分/拓扑度基础设施，登记为未来工作：

  1. **第一陈数积分定义**：C = (1/2π) ∫_{T²} F d²k（T² = 布里渊区环面）。
     需要：矩阵值函数在环面上的积分（mathlib MeasureTheory + 流形积分），
     以及 F 的连续性（⇐ P 光滑）。
  2. **整性定理**：C ∈ ℤ。这是陈数理论的拓扑核心，需度理论/同伦提升论证
     （或 Atiyah-Singer 指标的特殊化），有限维代数原型内不可达。
  3. **TKNN 公式**（paper14 定理 3.1）：σ_xy = (e²/h)·C。需 Kubo 线性响应
     或 Laughlin 泵浦论证，属连续场论形式化（远期）。
  4. **陈数绝热不变性**（paper14 命题 3.1）：谱间隙不闭合的参数形变下 C 不变。
     需同伦不变性 + 积分定义的连续依赖性。
  5. **规范不变性细节**：用本征矢量表示的 Berry 联络 A = i⟨u|∇u⟩ 在
     u ↦ e^{iθ}·u 下不变，且 F = dA 与投影公式一致（需微分形式恒等式）。
  6. **切向量的分析构造**：投影族 P(k) = cfc occFn(H(k)) 对参数的可微性
     （Kato 微扰论层）——其纯代数后件（约束方程、带间化简、双交换子形式）
     已由 §2.5 闭合，分析构造本身仍需微积分基础设施。

  已闭合（本模块，零 sorry）：Berry 曲率投影公式 + 实值性（陈数良定义的
  代数基础）+ 投影切向量代数层（projTangent_intraBand_zero 带内消没 /
  trace_proj_commutator_interband 带间化简 / berryCurvature_interband 带间
  形式 / trace_proj_commutator_twoCommutator 双交换子形式）。-/

end MUFPF
