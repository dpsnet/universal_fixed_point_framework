-- InflationDynamics.agda
-- Phase 61A (P1-4) 暴涨完整动力学：动态连续极限的 Hilbert 层形式化
--
-- 对应论文 paper/paper61A_inflation_dynamics.md 定理 D3.1 的算子代数核心：
--   F1  unitary-conj-self-adjoint：酉共轭 U·D·U† 保持自伴（D3.1(1)）
--   F2  flow-self-adjoint：谱流族 D(t) = Uₜ·D₀·Uₜ† 保持自伴（D3.1(2)）
--
-- 说明：
--   1. 自伴性保持不需要酉性假设——伴随 U† 已携带内积传输；
--      酉性（U∘U† = id）用于谱不变性 σ(U·D·U†) = σ(D)（Lean
--      spectral_invariance / frobNormSq_unitary_conj 已证）。
--   2. 拟对称嵌入的几何保持（Tukia–Väisälä，B2 定理 5.5）为文档级定理。
--   3. 谱流 Uₜ = exp(tG) 的酉性由 exp(-tG) = exp(tG)† 给出（Lean
--      spectral_flow_exp_conjTranspose 已证）。

module InflationDynamics.InflationDynamics where

open import Agda.Builtin.Equality using (_≡_; refl)
open import Sp.SpCategory using (ℕ; zero; suc; sym; trans; cong; cong₂; _×_; _,_)
open import HilbertSpace.HilbertSpace

-- 酉（幺正）算子：U ∘ U† = id（逐点）。用于谱流 = 酉相似（谱不变性前提）。
Unitary : LinOp → Set
Unitary U = (x : V) → LinOp.f (op-comp U (adj U)) x ≡ x

-- F1: 酉共轭保持自伴（定理 D3.1(1) 算子代数核心）。
-- 证明：⟨U X U† x, y⟩ = ⟨X U† x, U† y⟩（adj-ip U）
--                    = ⟨U† x, X U† y⟩（hX：SelfAdjoint X）
--                    = ⟨x, U X U† y⟩（adj-move U）
unitary-conj-self-adjoint : (U X : LinOp) → SelfAdjoint X → Unitary U →
  SelfAdjoint (op-comp (op-comp U X) (adj U))
unitary-conj-self-adjoint U X hX _ x y =
  trans (adj-ip U (LinOp.f X (LinOp.f (adj U) x)) y)
        (trans (hX (LinOp.f (adj U) x) (LinOp.f (adj U) y))
               (adj-move U x (LinOp.f X (LinOp.f (adj U) y))))

-- F2: 谱流族 D(t) = Uₜ·D₀·Uₜ† 保持自伴（定理 D3.1(2) 算子代数核心）。
-- Uₜ = exp(tG)（G 反 Hermitian，exp-hilb-tA 层）的酉性为文档级假设。
flow-self-adjoint : (Uₜ D₀ : LinOp) → SelfAdjoint D₀ → Unitary Uₜ →
  SelfAdjoint (op-comp (op-comp Uₜ D₀) (adj Uₜ))
flow-self-adjoint = unitary-conj-self-adjoint
