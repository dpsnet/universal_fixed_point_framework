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
-- 本文件中 UFPF 相关引用数量：0
-- 更名将在计划确认后统一执行，当前代码不做修改。
-- ============================================================

import Mathlib.Analysis.Normed.Algebra.MatrixExponential
import Mathlib.LinearAlgebra.Matrix.ConjTranspose
import Mathlib.Tactic
import MUFPFormalization.SpectralDynamics
import MUFPFormalization.SpectralInvariant

open Matrix

namespace MUFPF

/-!
# GPVortex.lean — paper14 §4.2 涡旋＝谱规范分支 + 拓扑荷守恒（代数核心，G4）

对应 paper14 §4.2 命题 4.2 / 推论 4.2 的**有限维代数核心**：

  命题 4.2：GP 谱流方程的涡旋解对应 A_GP 的规范变换 A_GP → U_n† A_GP U_n
            （U_n 幺正）；涡旋拓扑荷 n ∈ ℤ 是谱流方程的拓扑不变量。
  推论 4.2：涡旋拓扑荷在谱流方程演化下不变（dn/dt = 0）。

本模块在有限维矩阵代数层将这两条命题的**谱代数根源**机证闭合（零 sorry）：

  1. 谱流幺正规范协变（`spectralFlow_unitary_conj`）：对幺正 U
     （U†U = UU† = 1），规范分支 (U†A₀U, U†A_FU) 的谱流恰为原谱流的
     规范共轭。即**规范变换与谱流映射交换**——"涡旋＝规范分支"的谱代数
     内容：涡旋支与原来支沿谱流保持相同的谱动力学结构。
  2. 规范分支保全部迹幂（`vortex_trace_gaugeInvariant`）：任一幺正规范
     分支 U†AU 满足 tr((U†AU)^k) = tr(A^k)（SpectrInvariant.trace_pow_similar
     的直接实例化）。迹幂经 Newton 恒等式完全决定谱，故规范分支与原来支
     共享全部谱（拓扑荷的谱决定部分）。
  3. 涡旋荷沿时间与规范的守恒（`vortex_charge_conservation`）：规范分支
     谱流与原谱流在每个时刻 t 的迹幂全等——推论 4.2"dn/dt = 0"的有限维
     代数版本。

## 诚实边界

- 这里闭合的是**谱代数根源**：规范变换保持谱流结构、保迹幂（谱）。真实
  涡旋拓扑荷 n ∈ ℤ 的**严格 winding-number 定义**（U_n = e^{inφ}，φ 方位角）
  与同伦不变性需连续场论（S¹ → U(1) 的度），为已登记开放问题，本模块不
   axiomatize。
- 连续性方程 ∂_t ρ + ∇·(ρ𝐯) = 0 到谱流方程的翻译、GP 方程（PDE）本身
  到谱流方程的"等价"形式改写仍属【谱公理】层（GPEmergence/paper14 标注），
  亦不在本模块范围。
-/

/-! §1 谱流幺正规范协变（命题 4.2 的谱代数内容） -/

/-- **命题 4.2（谱代数核心）**：对幺正 U（U.conjTranspose * U = 1 且
    U * U.conjTranspose = 1），谱流的幺正规范共轭与谱流映射交换：
    spectralFlow (U†·A₀·U) (U†·A_F·U) t = U†·(spectralFlow A₀ A_F t)·U。
    即规范分支 (U†A₀U, U†A_FU) 的谱流恰是原谱流的规范共轭——"涡旋＝
    规范分支"与"涡旋沿谱流保持结构"的代数根据。 -/
theorem spectralFlow_unitary_conj {n : ℕ} (U A₀ A_F : Matrix (Fin n) (Fin n) ℂ)
    (hUinv : U.conjTranspose * U = 1) (hUstar : U * U.conjTranspose = 1) (t : ℝ) :
    spectralFlow (U.conjTranspose * A₀ * U) (U.conjTranspose * A_F * U) t
      = U.conjTranspose * spectralFlow A₀ A_F t * U := by
  classical
  set V : Matrix (Fin n) (Fin n) ℂ := U.conjTranspose with hV_def
  have hUV : U * V = 1 := by simpa [V] using hUstar
  have hVU : V * U = 1 := by simpa [V] using hUinv
  have hVin : V⁻¹ = U := Matrix.inv_eq_right_inv hVU
  have hVunit : IsUnit V := ⟨Units.mk V U hVU hUV, rfl⟩
  -- 标量穿透：a · (V·C·U) = V·(a·C)·U
  have hs (a : ℝ) (C : Matrix (Fin n) (Fin n) ℂ) : a • (V * C * U) = V * (a • C) * U := by
    rw [← Matrix.smul_mul, ← Matrix.mul_smul]
  -- 指数共轭：exp(a · (V·A_F·U)) = V·exp(a·A_F)·U
  have hExp (a : ℝ) :
      NormedSpace.exp (a • (V * A_F * U)) = V * NormedSpace.exp (a • A_F) * U := by
    rw [hs a A_F]
    conv_lhs => rw [← hVin]
    rw [Matrix.exp_conj V (a • A_F) hVunit]
    rw [hVin]
  -- 主等价：两端谱流的乘积结构在消去 U·V = 1 后一致
  unfold spectralFlow
  rw [hExp t, hExp (-t)]
  rw [neg_smul]
  set E0 : Matrix (Fin n) (Fin n) ℂ := NormedSpace.exp (t • A_F) with hE0
  set E1 : Matrix (Fin n) (Fin n) ℂ := NormedSpace.exp (-(t • A_F)) with hE1
  calc
    (V * E0 * U) * (V * A₀ * U) * (V * E1 * U)
        = V * E0 * (U * V) * A₀ * (U * V) * E1 * U := by noncomm_ring
    _ = V * E0 * A₀ * E1 * U := by
          rw [hUV]
          simp
    _ = V * (E0 * A₀ * E1) * U := by noncomm_ring

/-! §2 规范分支保全部迹幂（推论 4.2 的谱决定部分） -/

/-- **规范分支保谱**：对幺正 U，tr((U†·A·U)^k) = tr(A^k)。
    迹幂经 Newton 恒等式完全决定谱（计重数），故幺正规范分支与原来支共享
    全部谱——涡旋拓扑荷的谱决定部分在规范分支下不变。 -/
theorem vortex_trace_gaugeInvariant {n : ℕ} (U A : Matrix (Fin n) (Fin n) ℂ)
    (hUinv : U.conjTranspose * U = 1) (hUstar : U * U.conjTranspose = 1) (k : ℕ) :
    ((U.conjTranspose * A * U) ^ k).trace = (A ^ k).trace := by
  exact trace_pow_similar A U U.conjTranspose hUstar hUinv k

/-! §3 涡旋荷守恒（推论 4.2 的有限维代数版本） -/

/-- **推论 4.2（代数版本）**：规范分支谱流与原谱流在每个时刻 t 的全
    迹幂全等——涡旋拓扑荷的谱决定部分既沿谱流（时间）不变、也在幺正规范
    分支下不变。有限维层对 paper14 "dn/dt = 0" 的机器证明。 -/
theorem vortex_charge_conservation {n : ℕ} (U A₀ A_F : Matrix (Fin n) (Fin n) ℂ)
    (hUinv : U.conjTranspose * U = 1) (hUstar : U * U.conjTranspose = 1)
    (t : ℝ) (k : ℕ) :
    ((spectralFlow (U.conjTranspose * A₀ * U) (U.conjTranspose * A_F * U) t) ^ k).trace
      = (spectralFlow A₀ A_F t ^ k).trace := by
  rw [spectralFlow_unitary_conj U A₀ A_F hUinv hUstar t]
  exact vortex_trace_gaugeInvariant U (spectralFlow A₀ A_F t) hUinv hUstar k

end MUFPF