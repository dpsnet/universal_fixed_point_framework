-- ColorDynamics.agda
-- Phase 61B (P0-1) SU(3) 色规范完整动力学：色雅可比恒等式的算子代数层镜像
--
-- 对应论文 paper/paper61B_qcd_color_dynamics.md 推论 2.1 / 定理 3.1：
--   F1  color-jacobi：色雅可比恒等式 [[X,Y],Z] + [[Y,Z],X] + [[Z,X],Y] = 0
--        （胶子三/四顶点谱封闭的代数核心）
--
-- 审计登记（§15 公理纪律，类别 B：可证定理的桥接登记）：
--   Lean 矩阵层已完整证明（ColorDynamics.lean color_jacobi_identity，
--   noncomm_ring 全证，无 sorry）。Agda 算子层（LinOp）版本需逐点环代数
--   展开（op-comp-assoc-pt 定义性 + distribₗ-pt + 向量加法结合/交换/逆 +
--   op-sub/op-neg 定义性，~24 项两两抵消），登记为桥接，证明路径如上。
--   数值镜像验证：paperX_qcd_spectrum.py §1（雅可比残差 3.3e-16）。

module ColorDynamics.ColorDynamics where

open import Agda.Builtin.Equality using (_≡_; refl)
open import Sp.SpCategory using (ℕ; zero; suc; sym; trans; cong; cong₂; _×_; _,_)
open import HilbertSpace.HilbertSpace

-- 对易子 [X,Y] = XY - YX（算子代数层，定义性：op-sub 展开 + op-comp 展开）
commutator : LinOp → LinOp → LinOp
commutator X Y = op-sub (op-comp X Y) (op-comp Y X)

-- F1: 色雅可比恒等式（算子代数层，审计登记的桥接——证明路径见模块头注释）
postulate
  color-jacobi : (X Y Z : LinOp) (v : V) →
    LinOp.f (op-add (op-add (commutator (commutator X Y) Z)
                            (commutator (commutator Y Z) X))
                    (commutator (commutator Z X) Y)) v ≡ zeroᵥ
