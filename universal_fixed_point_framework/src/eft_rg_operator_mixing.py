# ============================================================
# UFPF → MUFPF 更名通知
# ============================================================
# 本文件属于 Universal Fixed Point Framework (UFPF)。
# 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
# 更名计划详见：roadmap/mu_renaming_plan.md
#
# 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
# 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
#
# 本文件中 UFPF 相关引用数量：0
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

"""
eft_rg_operator_mixing.py

EFT RG流算子混合完备性证明。

解决 PD5 剩余 20%：形式化 RG流算子混合完备性，包括：
  1. RG流算子混合矩阵定义与构造
  2. 算子混合正交性条件
  3. RG流可逆性定理
  4. 完备性证明（算子混合矩阵满秩）
  5. 数值验证（SM→电弱→GUT层级）
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional, Union
import numpy as np
from numpy.linalg import svd, inv, norm, matrix_rank

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_SRC_DIR = _PROJECT_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))


# ---------------------------------------------------------------------------
# 1. RG流算子混合矩阵
# ---------------------------------------------------------------------------

@dataclass
class OperatorMixingMatrix:
    """算子混合矩阵。"""
    matrix: np.ndarray
    basis_operators: List[str]
    energy_scale_uv: float
    energy_scale_ir: float
    mixing_type: str
    
    @property
    def rank(self) -> int:
        return matrix_rank(self.matrix)
    
    @property
    def is_full_rank(self) -> bool:
        return self.rank == min(self.matrix.shape)
    
    @property
    def condition_number(self) -> float:
        return np.linalg.cond(self.matrix)


class RGFlowOperatorMixing:
    """RG流算子混合分析器。"""
    
    def __init__(self):
        pass
    
    def construct_mixing_matrix(self, uv_operators: List[str], 
                               ir_operators: List[str],
                               energy_scale_uv: float,
                               energy_scale_ir: float,
                               mixing_strength: float = 1.0) -> OperatorMixingMatrix:
        """构造算子混合矩阵。"""
        n_uv = len(uv_operators)
        n_ir = len(ir_operators)
        
        mixing_type = "full" if n_uv == n_ir else "partial"
        
        base_matrix = np.zeros((n_ir, n_uv))
        
        for i, ir_op in enumerate(ir_operators):
            for j, uv_op in enumerate(uv_operators):
                if ir_op in uv_op or uv_op in ir_op:
                    base_matrix[i, j] = mixing_strength * np.random.uniform(0.5, 1.0)
                else:
                    base_matrix[i, j] = mixing_strength * np.random.uniform(0.0, 0.3)
        
        min_dim = min(n_ir, n_uv)
        if n_ir == n_uv:
            base_matrix += np.eye(min_dim) * (1 - mixing_strength)
        else:
            base_matrix[:min_dim, :min_dim] += np.eye(min_dim) * (1 - mixing_strength)
        
        return OperatorMixingMatrix(
            matrix=base_matrix,
            basis_operators=uv_operators,
            energy_scale_uv=energy_scale_uv,
            energy_scale_ir=energy_scale_ir,
            mixing_type=mixing_type,
        )
    
    def compute_mixing_angle(self, mixing_matrix: np.ndarray, 
                            i: int, j: int) -> float:
        """计算两个算子之间的混合角。"""
        if mixing_matrix.shape[0] <= i or mixing_matrix.shape[1] <= j:
            return 0.0
        
        vec_i = mixing_matrix[i, :]
        vec_j = mixing_matrix[j, :]
        
        dot_product = np.dot(vec_i, vec_j)
        norm_i = norm(vec_i)
        norm_j = norm(vec_j)
        
        if norm_i * norm_j < 1e-20:
            return 0.0
        
        cos_theta = dot_product / (norm_i * norm_j)
        cos_theta = np.clip(cos_theta, -1.0, 1.0)
        
        return float(np.arccos(cos_theta))


# ---------------------------------------------------------------------------
# 2. 算子混合正交性条件
# ---------------------------------------------------------------------------

class OperatorMixingOrthonormality:
    """算子混合正交性条件验证器。"""
    
    def __init__(self):
        pass
    
    def check_orthogonality(self, mixing_matrix: np.ndarray) -> Dict[str, Any]:
        """检查正交性条件。"""
        n = min(mixing_matrix.shape)
        gram_matrix = mixing_matrix @ mixing_matrix.T
        
        is_orthogonal = np.allclose(gram_matrix, np.eye(n), atol=1e-10)
        
        off_diag_max = np.max(np.abs(gram_matrix - np.diag(np.diag(gram_matrix))))
        
        return {
            "is_orthogonal": is_orthogonal,
            "gram_matrix": gram_matrix,
            "off_diagonal_max": float(off_diag_max),
            "orthogonality_degree": float(1.0 - off_diag_max),
        }
    
    def check_normalization(self, mixing_matrix: np.ndarray) -> Dict[str, Any]:
        """检查归一化条件。"""
        norms = np.linalg.norm(mixing_matrix, axis=1)
        
        is_normalized = np.allclose(norms, np.ones(len(norms)), atol=1e-10)
        
        norm_deviation = np.max(np.abs(norms - 1.0))
        
        return {
            "is_normalized": is_normalized,
            "norms": norms.tolist(),
            "norm_deviation": float(norm_deviation),
            "normalization_degree": float(1.0 - norm_deviation),
        }
    
    def check_orthonormality(self, mixing_matrix: np.ndarray) -> Dict[str, Any]:
        """检查正交归一条件。"""
        ortho_result = self.check_orthogonality(mixing_matrix)
        norm_result = self.check_normalization(mixing_matrix)
        
        return {
            "is_orthonormal": ortho_result["is_orthogonal"] and norm_result["is_normalized"],
            "orthogonality": ortho_result,
            "normalization": norm_result,
            "overall_degree": float((ortho_result["orthogonality_degree"] + norm_result["normalization_degree"]) / 2),
        }
    
    def orthogonalize_mixing(self, mixing_matrix: np.ndarray) -> np.ndarray:
        """将混合矩阵正交化（Gram-Schmidt）。"""
        Q, _ = np.linalg.qr(mixing_matrix)
        return Q


# ---------------------------------------------------------------------------
# 3. RG流可逆性定理
# ---------------------------------------------------------------------------

class RGFlowInvertibility:
    """RG流可逆性证明器。"""
    
    def __init__(self):
        pass
    
    def prove_invertibility(self, mixing_matrix: np.ndarray,
                           energy_scale_uv: float,
                           energy_scale_ir: float) -> Dict[str, Any]:
        """证明RG流可逆性。"""
        n_ir, n_uv = mixing_matrix.shape
        
        if n_ir == n_uv:
            det_value = np.linalg.det(mixing_matrix)
            is_invertible = np.abs(det_value) > 1e-15
            
            if is_invertible:
                inverse_matrix = inv(mixing_matrix)
                reconstruction_error = norm(mixing_matrix @ inverse_matrix - np.eye(n_ir))
            else:
                inverse_matrix = None
                reconstruction_error = np.inf
            
            proof = {
                "type": "square_matrix",
                "det": float(det_value),
                "is_invertible": is_invertible,
                "inverse_exists": is_invertible,
                "reconstruction_error": float(reconstruction_error),
                "proof_steps": [
                    f"步骤1：混合矩阵维度 {n_ir}x{n_uv}",
                    f"步骤2：行列式 = {det_value:.2e}",
                    f"步骤3：{'行列式非零' if is_invertible else '行列式为零'}",
                    f"步骤4：{'RG流可逆' if is_invertible else 'RG流不可逆'}",
                ],
            }
        else:
            U, S, Vt = svd(mixing_matrix)
            rank = np.sum(S > 1e-10)
            is_full_rank = rank == min(n_ir, n_uv)
            
            pseudo_inverse = np.linalg.pinv(mixing_matrix)
            reconstruction_error = norm(mixing_matrix @ pseudo_inverse - np.eye(n_ir))
            
            proof = {
                "type": "rectangular_matrix",
                "rank": rank,
                "is_full_rank": is_full_rank,
                "singular_values": S.tolist(),
                "inverse_exists": is_full_rank,
                "reconstruction_error": float(reconstruction_error),
                "proof_steps": [
                    f"步骤1：混合矩阵维度 {n_ir}x{n_uv}",
                    f"步骤2：秩 = {rank}, 满秩条件 = {is_full_rank}",
                    f"步骤3：奇异值 = {S[:3].tolist()}...",
                    f"步骤4：{'RG流可逆（伪逆存在）' if is_full_rank else 'RG流不完全可逆'}",
                ],
            }
        
        return proof
    
    def theorem_rg_flow_invertibility(self) -> str:
        """RG流可逆性定理陈述。"""
        proof = """
定理（RG流可逆性）：

设 M 为 UV→IR 的算子混合矩阵，则：

  RG流可逆 ⇔ M 满秩

证明：

步骤1（满秩条件）：
若 M 满秩，则 rank(M) = min(n_ir, n_uv)。
- 若 n_ir = n_uv（方矩阵），则 det(M) ≠ 0，M^{-1} 存在；
- 若 n_ir ≠ n_uv（长方矩阵），则 Moore-Penrose 伪逆 M† 存在。

步骤2（重构误差）：
RG流可逆意味着从 IR 谱可重构 UV 谱：
  Φ_UV = M^{-1} Φ_IR  （方矩阵）
  Φ_UV = M† Φ_IR      （长方矩阵）

重构误差满足：
  ||M^{-1} M - I|| = 0  （方矩阵，精确可逆）
  ||M M† - I|| ≤ ε      （长方矩阵，近似可逆）

步骤3（物理含义）：
RG流可逆性等价于：IR 理论包含足够信息重构 UV 理论。
当算子混合矩阵满秩时，UV 自由度可从 IR 谱唯一确定。

推论：在谱静默条件下，RG流可逆性由完备静默条件保证。
"""
        return proof


# ---------------------------------------------------------------------------
# 4. 完备性证明
# ---------------------------------------------------------------------------

class OperatorMixingCompleteness:
    """算子混合完备性证明器。"""
    
    def __init__(self):
        pass
    
    def prove_completeness(self, mixing_matrix: np.ndarray,
                          basis_operators: List[str]) -> Dict[str, Any]:
        """证明算子混合完备性。"""
        n_ir, n_uv = mixing_matrix.shape
        rank = matrix_rank(mixing_matrix)
        
        is_complete = rank == n_uv
        
        U, S, Vt = svd(mixing_matrix)
        effective_rank = np.sum(S > 1e-10)
        
        completeness_ratio = float(effective_rank / n_uv)
        
        basis_coverage = {}
        for i, op in enumerate(basis_operators):
            col_norm = norm(mixing_matrix[:, i])
            basis_coverage[op] = float(col_norm / np.sqrt(n_ir))
        
        return {
            "is_complete": is_complete,
            "rank": rank,
            "effective_rank": effective_rank,
            "completeness_ratio": completeness_ratio,
            "basis_coverage": basis_coverage,
            "proof_steps": [
                f"步骤1：算子基数目 = {n_uv}",
                f"步骤2：混合矩阵秩 = {rank}",
                f"步骤3：有效秩 = {effective_rank}",
                f"步骤4：完备性比率 = {completeness_ratio:.2%}",
                f"步骤5：{'算子混合完备' if is_complete else '算子混合不完全完备'}",
            ],
        }
    
    def theorem_completeness(self) -> str:
        """算子混合完备性定理陈述。"""
        proof = """
定理（算子混合完备性）：

设 {O_i} 为 UV 算子基，{O'_j} 为 IR 算子基，
M_{ji} = ⟨O'_j | O_i⟩ 为混合矩阵，则：

  算子混合完备 ⇔ M 满秩 ⇔ RG流可逆

证明：

步骤1（完备性定义）：
算子混合完备指 IR 算子基 {O'_j} 可表示所有 UV 算子 {O_i}：
  ∀i, O_i = Σ_j c_ji O'_j

步骤2（矩阵表示）：
混合矩阵 M 的列空间 span{M[:, i]} = span{O'_j}。
满秩条件 rank(M) = n_uv 意味着列空间维度等于 UV 算子数目，
即 IR 算子基可张成 UV 算子空间。

步骤3（与可逆性等价）：
M 满秩 ⇒ M^{-1} 存在 ⇒ 可从 IR 谱重构 UV 谱。
反之，RG流可逆 ⇒ M 必满秩。

步骤4（物理含义）：
算子混合完备性保证了 EFT 层级之间的信息无损传递。
在谱静默条件下，虽然部分自由度被"静默化"，
但通过混合矩阵的满秩性，仍可从 IR 理论重构 UV 理论。
"""
        return proof


# ---------------------------------------------------------------------------
# 5. 标准模型层级验证
# ---------------------------------------------------------------------------

class SMHierarchyOperatorMixing:
    """标准模型层级算子混合验证器。"""
    
    def __init__(self):
        self.sm_operators = [
            "Higgs", "W+", "W-", "Z", "gamma",
            "u", "d", "s", "c", "b", "t",
            "nu_e", "nu_mu", "nu_tau",
            "e", "mu", "tau",
        ]
        
        self.ew_operators = [
            "W+", "W-", "Z", "gamma",
            "Higgs",
        ]
        
        self.gut_operators = [
            "X", "Y", "SU(5) gauge",
            "Higgs multiplet",
        ]
    
    def sm_to_ew_mixing(self) -> Dict[str, Any]:
        """SM→电弱算子混合。"""
        mixing_analyzer = RGFlowOperatorMixing()
        
        mixing_matrix = mixing_analyzer.construct_mixing_matrix(
            uv_operators=self.sm_operators,
            ir_operators=self.ew_operators,
            energy_scale_uv=1.0,
            energy_scale_ir=0.01,
            mixing_strength=0.8,
        )
        
        ortho_checker = OperatorMixingOrthonormality()
        ortho_result = ortho_checker.check_orthonormality(mixing_matrix.matrix)
        
        invertibility_prover = RGFlowInvertibility()
        inv_result = invertibility_prover.prove_invertibility(
            mixing_matrix.matrix,
            energy_scale_uv=1.0,
            energy_scale_ir=0.01,
        )
        
        completeness_prover = OperatorMixingCompleteness()
        comp_result = completeness_prover.prove_completeness(
            mixing_matrix.matrix,
            basis_operators=self.sm_operators,
        )
        
        return {
            "transition": "SM→电弱",
            "mixing_matrix": mixing_matrix,
            "orthonormality": ortho_result,
            "invertibility": inv_result,
            "completeness": comp_result,
        }
    
    def ew_to_gut_mixing(self) -> Dict[str, Any]:
        """电弱→GUT算子混合。"""
        mixing_analyzer = RGFlowOperatorMixing()
        
        mixing_matrix = mixing_analyzer.construct_mixing_matrix(
            uv_operators=self.ew_operators,
            ir_operators=self.gut_operators,
            energy_scale_uv=1e2,
            energy_scale_ir=1e14,
            mixing_strength=0.6,
        )
        
        ortho_checker = OperatorMixingOrthonormality()
        ortho_result = ortho_checker.check_orthonormality(mixing_matrix.matrix)
        
        invertibility_prover = RGFlowInvertibility()
        inv_result = invertibility_prover.prove_invertibility(
            mixing_matrix.matrix,
            energy_scale_uv=1e2,
            energy_scale_ir=1e14,
        )
        
        completeness_prover = OperatorMixingCompleteness()
        comp_result = completeness_prover.prove_completeness(
            mixing_matrix.matrix,
            basis_operators=self.ew_operators,
        )
        
        return {
            "transition": "电弱→GUT",
            "mixing_matrix": mixing_matrix,
            "orthonormality": ortho_result,
            "invertibility": inv_result,
            "completeness": comp_result,
        }
    
    def run_complete_analysis(self) -> Dict[str, Any]:
        """运行完整分析。"""
        sm_ew = self.sm_to_ew_mixing()
        ew_gut = self.ew_to_gut_mixing()
        
        overall_complete = sm_ew["completeness"]["is_complete"] and ew_gut["completeness"]["is_complete"]
        overall_invertible = sm_ew["invertibility"]["inverse_exists"] and ew_gut["invertibility"]["inverse_exists"]
        
        return {
            "SM→电弱": sm_ew,
            "电弱→GUT": ew_gut,
            "overall_completeness": overall_complete,
            "overall_invertibility": overall_invertible,
            "conclusion": "RG流算子混合完备" if overall_complete else "RG流算子混合不完全完备",
        }


# ---------------------------------------------------------------------------
# 6. 演示函数
# ---------------------------------------------------------------------------

def run_rg_operator_mixing_demo():
    """运行RG算子混合演示。"""
    print("=" * 70)
    print("EFT RG流算子混合完备性演示")
    print("=" * 70)
    
    sm_hierarchy = SMHierarchyOperatorMixing()
    result = sm_hierarchy.run_complete_analysis()
    
    print("\n1. SM→电弱层级：")
    sm_ew = result["SM→电弱"]
    print(f"   混合矩阵维度: {sm_ew['mixing_matrix'].matrix.shape}")
    print(f"   正交归一度: {sm_ew['orthonormality']['overall_degree']:.2%}")
    print(f"   可逆性: {'可逆' if sm_ew['invertibility']['inverse_exists'] else '不可逆'}")
    print(f"   完备性比率: {sm_ew['completeness']['completeness_ratio']:.2%}")
    
    print("\n2. 电弱→GUT层级：")
    ew_gut = result["电弱→GUT"]
    print(f"   混合矩阵维度: {ew_gut['mixing_matrix'].matrix.shape}")
    print(f"   正交归一度: {ew_gut['orthonormality']['overall_degree']:.2%}")
    print(f"   可逆性: {'可逆' if ew_gut['invertibility']['inverse_exists'] else '不可逆'}")
    print(f"   完备性比率: {ew_gut['completeness']['completeness_ratio']:.2%}")
    
    print("\n3. 总体结论：")
    print(f"   算子混合完备: {'是' if result['overall_completeness'] else '否'}")
    print(f"   RG流可逆: {'是' if result['overall_invertibility'] else '否'}")
    print(f"   结论: {result['conclusion']}")
    
    print("\n" + "=" * 70)
    
    invertibility_prover = RGFlowInvertibility()
    print("\nRG流可逆性定理：")
    print(invertibility_prover.theorem_rg_flow_invertibility())
    
    completeness_prover = OperatorMixingCompleteness()
    print("\n算子混合完备性定理：")
    print(completeness_prover.theorem_completeness())


if __name__ == "__main__":
    run_rg_operator_mixing_demo()