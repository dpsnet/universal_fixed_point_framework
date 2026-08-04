-- BlackHoleDynamics.agda
-- Phase 61D (P1-3) 黑洞量子演化：信息保持、蒸发终点与量子反弹的 Hilbert 层形式化
--
-- 对应论文 paper/paper61D_black_hole_quantum_evolution.md：
--   F1  flow-self-adjoint：谱流 A_t = U·A₀·U† 保持自伴（信息载体结构稳定）
--   F2  spectrum-preserved（登记）：谱保持 σ(A₀) = σ(A_t)，双向机器证明在 Lean
--       （BlackHoleInformation.lean：bhInformationPreserved_iff / spectralFlow_inv）
--   F3  evaporation-monotone（登记）：蒸发质量单调递减 M(t+dt) < M(t)，Lean
--       （BlackHoleEvolution.lean：bhMass_decreasing）已证
--   F4  planck-termination（登记）：蒸发在 Planck 尺度终止，M(t_pl) = M_Pl 且
--       ∀ t < t_pl, M(t) > M_Pl（无裸奇点），Lean
--       （BlackHoleEvolution.lean：bhMass_at_planck / bhMass_above_planck_before）已证
--   F5  bounce-seed（登记）：Planck 残留黑洞成为量子反弹种子，反弹点 H²(ρ_c) = 0，
--       Lean（BlackHoleBounce.lean：bhPlanckRemnant_is_bounce_seed /
--       hubbleSquared_zero_at_critical）已证
--
-- 说明：
--   1. 谱流 Uₜ = exp(t·G) 的酉性由 exp(-tG)·exp(tG) = id 给出
--      （Lean 侧 spectralFlow_inv / matrix_exp_smul_neg 机器证明）。
--   2. 本模块聚焦 Hilbert 层算子代数核心（自伴保持 = 物理量实在性保持），
--      谱不变性/蒸发单调性/Planck 终止/反弹衔接等标量定理在 Lean 侧已机器证明，
--      此处登记引用。

module BlackHoleDynamics.BlackHoleDynamics where

open import Agda.Builtin.Equality using (_≡_; refl)
open import Sp.SpCategory using (ℕ; zero; suc; sym; trans; cong; cong₂; _×_; _,_)
open import HilbertSpace.HilbertSpace

-- 酉（幺正）算子：U ∘ U† = id（逐点）。用于谱流 = 酉相似（谱不变性前提）。
Unitary : LinOp → Set
Unitary U = (x : V) → LinOp.f (op-comp U (adj U)) x ≡ x

-- 谱流（Hilbert 层）：A_t = Uₜ·A₀·Uₜ†（Uₜ = exp(t·G) 酉，文档级假设）
spectral-flow : LinOp → LinOp → LinOp
spectral-flow U A₀ = op-comp (op-comp U A₀) (adj U)

-- F1: 谱流保持自伴（信息载体结构稳定）。
-- 证明：⟨U A₀ U† x, y⟩ = ⟨A₀ U† x, U† y⟩（adj-ip U）
--                    = ⟨U† x, A₀ U† y⟩（hA₀：SelfAdjoint A₀）
--                    = ⟨x, U A₀ U† y⟩（adj-move U）
flow-self-adjoint : (U A₀ : LinOp) → SelfAdjoint A₀ → Unitary U →
  SelfAdjoint (spectral-flow U A₀)
flow-self-adjoint U A₀ hA₀ _ x y =
  trans (adj-ip U (LinOp.f A₀ (LinOp.f (adj U) x)) y)
        (trans (hA₀ (LinOp.f (adj U) x) (LinOp.f (adj U) y))
               (adj-move U x (LinOp.f A₀ (LinOp.f (adj U) y))))
