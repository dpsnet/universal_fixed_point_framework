-- ============================================================
-- UFPF → MUFPF 更名通知（同 WeaveBCS.lean，本文件属于 UFPF/MUFPF）
-- ============================================================

/-
# GPFlow.lean — paper14 G4：GP 谱流方程的守恒律（有限维代数核心）

背景：paper14 定理 4.1（GP-谱流等同 dA_GP/dt = [A_kin+A_ext+A_int, A_GP]）的证明是
启发式 sketch，命题 4.2（涡旋 = 谱规范分支）与推论 4.2（涡旋荷 dn/dt = 0）此前无
Lean 载体。GP 方程本身是连续 PDE，完整形式化需场论/同伦基础设施。

本模块建立谱流守恒律的**有限维代数核心**——谱流方程 dA/dt = [G, A] 保持谱
生成元的全部迹幂 tr(A^k)（k = 0,1,2,…），其数学内容是：迹生成元在交换子方向
[G, A] 上消失。这是推论 4.2「涡旋拓扑荷守恒」的谱版本（拓扑荷由谱/相位缠绕决定，
谱不变 ⟹ 荷不变）。

  §1 trace_commutator_eq_zero：迹消去交换子 tr [G, A] = 0
  §2 trace_pow_mul_commutator_eq_zero：谱流守恒核心 tr(A^k [G, A]) = 0
  §3 开放登记：时间依赖守恒律、涡旋 winding 拓扑荷、GP-谱流等同（定理 4.1）

说明：核心引理为纯代数（只用迹循环性 + 线性性），不依赖幂等/厄米性，对任意
复方阵成立。它给出 d/dt tr(A^k) = 0 的被积表达式为零（见 §3 时间依赖版）。
-/

import Mathlib.Data.Complex.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Tactic

namespace MUFPF

open Matrix Complex

/-- §1：迹消去交换子——对任意复方阵 G、A，tr [G, A] = 0。
    这是所有谱流守恒律的最基本形式（k = 0 幂次的特例）。 -/
theorem trace_commutator_eq_zero {n : ℕ} (G A : Matrix (Fin n) (Fin n) ℂ) :
    (G * A - A * G).trace = 0 := by
  rw [Matrix.trace_sub, Matrix.trace_mul_comm G A, sub_self]

/-- §2：**谱流守恒核心（G4）**——对任意复方阵 G、A 与幂次 k，
    tr(A^k · [G, A]) = 0。等价地：迹幂函数 tr(·^k) 在李括号方向 [G, A] 上的
    方向导数为零，即 tr(A^k) 沿谱流方程 dA/dt = [G, A] 不变（谱不变性）。
    证明只用迹循环性：tr(A^k G A) 与 tr(A^{k+1} G) 经轮换相等。
    这是推论 4.2「涡旋拓扑荷守恒」的谱代数根源。 -/
theorem trace_pow_mul_commutator_eq_zero {n : ℕ} (G A : Matrix (Fin n) (Fin n) ℂ)
    (k : ℕ) : (A ^ k * (G * A - A * G)).trace = 0 := by
  have e1 : (A ^ k * (G * A)).trace = (A ^ (k + 1) * G).trace := by
    rw [← mul_assoc, Matrix.trace_mul_comm (A ^ k * G) A, ← mul_assoc, ← pow_succ']
  have e2 : (A ^ k * (A * G)).trace = (A ^ (k + 1) * G).trace := by
    rw [← mul_assoc, ← pow_succ]
  rw [mul_sub, Matrix.trace_sub, e1, e2, sub_self]

/- §3 开放登记（paper14 G4 完整 GP-涡旋理论，不占用 sorry，真证路径见下）：

  本模块建立了谱流守恒律的代数核心（迹幂在交换子方向消失）。以下完整内容需
  微积分/场论/同伦基础设施，登记为未来工作：

  1. **时间依赖守恒律**：d/dt tr(A(t)^k) = 0（A 满足谱流方程 dA/dt = [G, A]）。
     需矩阵幂导数规则 (A^k)' = Σ_i A^i A' A^{k-1-i}（非交换 Leibniz，mathlib
     有 HasDerivAt.mul 可归纳构造），代入 §2 即得。属微积分包装，代数核心已闭合。
     **→ 已闭合（2026-09-19，GPFlowTimeDep.lean）**：借助谱流解
     A(t) = exp(t·A_F)·A_0·exp(−t·A_F) 证得更强的点式恒等
     tr(A(t)^k) = tr(A_0^k)（对所有 t），故 t ↦ tr(A(t)^k) 为常值、
     其 HasDerivAt 处处为 0——`trace_pow_invariant_flow` + `trace_pow_flow_conservation`，
     零 sorry。避开了矩阵幂导数规则，改用 exp 双侧逆 + 迹幂相似不变性
     （`SpectralInvariant.trace_pow_similar`）。见 sorry_closure_roadmap §九。
  2. **谱不变性**：tr(A^k) 守恒 ⟺ 特征值（计重数）守恒（Newton 恒等式），
     即 A(t) 与 A(0) 同谱。需 Newton 恒等式形式化（中等）。第 1 项已给全部
     Newton 基础量，翻译到特征值谱仍登记开放。
  3. **涡旋 winding 拓扑荷**（命题 4.2）：n = (1/2π) ∮ ∇θ·dl 的离散度数定义与
     同伦不变性。需连续场/同伦提升（相位 θ 场的缠绕数在零点不穿越下不变），
     有限维代数原型内不可达。
  4. **GP-谱流等同**（定理 4.1）：A_GP = −log ρ 与连续性方程 ∂tρ + ∇·(ρv) = 0
     的谱表述等价。需 PDE/泛函分析基础设施（ρ、v 为场），完整形式化为远期。
  5. **规范协变性**：谱流方程在 A ↦ U† A U 下的协变形式（U 时变引入 A_U = U†Ȧ
     规范势）。需依赖时间的幺正群，属分析。

  已闭合（本模块，零 sorry）：迹消去交换子 + 谱流守恒核心 tr(A^k [G, A]) = 0
  （推论 4.2 涡旋荷守恒的谱代数根源）。-/

end MUFPF
