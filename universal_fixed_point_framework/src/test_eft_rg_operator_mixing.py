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
test_eft_rg_operator_mixing.py

EFT RG流算子混合完备性测试。
"""

import pytest
import numpy as np

from eft_rg_operator_mixing import (
    OperatorMixingMatrix,
    RGFlowOperatorMixing,
    OperatorMixingOrthonormality,
    RGFlowInvertibility,
    OperatorMixingCompleteness,
    SMHierarchyOperatorMixing,
)


class TestOperatorMixingMatrix:
    """测试算子混合矩阵。"""
    
    def test_creation(self):
        matrix = np.eye(5)
        mixing = OperatorMixingMatrix(
            matrix=matrix,
            basis_operators=["A", "B", "C", "D", "E"],
            energy_scale_uv=1.0,
            energy_scale_ir=0.1,
            mixing_type="full",
        )
        assert mixing.rank == 5
        assert mixing.is_full_rank
        assert mixing.condition_number == 1.0


class TestRGFlowOperatorMixing:
    """测试RG流算子混合分析器。"""
    
    def test_creation(self):
        analyzer = RGFlowOperatorMixing()
        assert analyzer is not None
    
    def test_construct_mixing_matrix_square(self):
        analyzer = RGFlowOperatorMixing()
        uv_ops = ["A", "B", "C"]
        ir_ops = ["A", "B", "C"]
        
        mixing = analyzer.construct_mixing_matrix(
            uv_operators=uv_ops,
            ir_operators=ir_ops,
            energy_scale_uv=1.0,
            energy_scale_ir=0.1,
        )
        
        assert mixing.matrix.shape == (3, 3)
        assert mixing.mixing_type == "full"
    
    def test_construct_mixing_matrix_rectangular(self):
        analyzer = RGFlowOperatorMixing()
        uv_ops = ["A", "B", "C", "D"]
        ir_ops = ["A", "B"]
        
        mixing = analyzer.construct_mixing_matrix(
            uv_operators=uv_ops,
            ir_operators=ir_ops,
            energy_scale_uv=1.0,
            energy_scale_ir=0.1,
        )
        
        assert mixing.matrix.shape == (2, 4)
        assert mixing.mixing_type == "partial"
    
    def test_compute_mixing_angle(self):
        analyzer = RGFlowOperatorMixing()
        matrix = np.array([[1, 0], [0, 1]])
        
        angle = analyzer.compute_mixing_angle(matrix, 0, 1)
        assert np.isclose(angle, np.pi / 2)


class TestOperatorMixingOrthonormality:
    """测试算子混合正交性条件验证器。"""
    
    def test_creation(self):
        checker = OperatorMixingOrthonormality()
        assert checker is not None
    
    def test_check_orthogonality_identity(self):
        checker = OperatorMixingOrthonormality()
        matrix = np.eye(3)
        
        result = checker.check_orthogonality(matrix)
        assert result["is_orthogonal"]
        assert result["off_diagonal_max"] < 1e-10
    
    def test_check_normalization_identity(self):
        checker = OperatorMixingOrthonormality()
        matrix = np.eye(3)
        
        result = checker.check_normalization(matrix)
        assert result["is_normalized"]
        assert result["norm_deviation"] < 1e-10
    
    def test_check_orthonormality_identity(self):
        checker = OperatorMixingOrthonormality()
        matrix = np.eye(3)
        
        result = checker.check_orthonormality(matrix)
        assert result["is_orthonormal"]
    
    def test_orthogonalize_mixing(self):
        checker = OperatorMixingOrthonormality()
        matrix = np.array([[1, 1], [0, 1]])
        
        orthogonalized = checker.orthogonalize_mixing(matrix)
        assert orthogonalized.shape == (2, 2)


class TestRGFlowInvertibility:
    """测试RG流可逆性证明器。"""
    
    def test_creation(self):
        prover = RGFlowInvertibility()
        assert prover is not None
    
    def test_prove_invertibility_square(self):
        prover = RGFlowInvertibility()
        matrix = np.eye(3)
        
        result = prover.prove_invertibility(matrix, 1.0, 0.1)
        assert result["is_invertible"]
        assert result["inverse_exists"]
        assert result["reconstruction_error"] < 1e-10
    
    def test_prove_invertibility_rectangular_full_rank(self):
        prover = RGFlowInvertibility()
        matrix = np.array([[1, 0, 0], [0, 1, 0]])
        
        result = prover.prove_invertibility(matrix, 1.0, 0.1)
        assert result["is_full_rank"]
        assert result["inverse_exists"]
    
    def test_theorem_statement(self):
        prover = RGFlowInvertibility()
        theorem = prover.theorem_rg_flow_invertibility()
        
        assert "RG流可逆" in theorem
        assert "满秩" in theorem


class TestOperatorMixingCompleteness:
    """测试算子混合完备性证明器。"""
    
    def test_creation(self):
        prover = OperatorMixingCompleteness()
        assert prover is not None
    
    def test_prove_completeness_full_rank(self):
        prover = OperatorMixingCompleteness()
        matrix = np.eye(3)
        
        result = prover.prove_completeness(matrix, ["A", "B", "C"])
        assert result["is_complete"]
        assert result["completeness_ratio"] == 1.0
    
    def test_prove_completeness_partial_rank(self):
        prover = OperatorMixingCompleteness()
        matrix = np.array([[1, 0], [0, 0]])
        
        result = prover.prove_completeness(matrix, ["A", "B"])
        assert not result["is_complete"]
        assert result["completeness_ratio"] == 0.5
    
    def test_theorem_statement(self):
        prover = OperatorMixingCompleteness()
        theorem = prover.theorem_completeness()
        
        assert "算子混合完备" in theorem
        assert "满秩" in theorem


class TestSMHierarchyOperatorMixing:
    """测试标准模型层级算子混合验证器。"""
    
    def test_creation(self):
        sm_hierarchy = SMHierarchyOperatorMixing()
        assert sm_hierarchy is not None
        assert len(sm_hierarchy.sm_operators) == 17
        assert len(sm_hierarchy.ew_operators) == 5
        assert len(sm_hierarchy.gut_operators) == 4
    
    def test_sm_to_ew_mixing(self):
        sm_hierarchy = SMHierarchyOperatorMixing()
        result = sm_hierarchy.sm_to_ew_mixing()
        
        assert result["transition"] == "SM→电弱"
        assert result["mixing_matrix"].matrix.shape == (5, 17)
        assert "orthonormality" in result
        assert "invertibility" in result
        assert "completeness" in result
    
    def test_ew_to_gut_mixing(self):
        sm_hierarchy = SMHierarchyOperatorMixing()
        result = sm_hierarchy.ew_to_gut_mixing()
        
        assert result["transition"] == "电弱→GUT"
        assert result["mixing_matrix"].matrix.shape == (4, 5)
        assert "orthonormality" in result
        assert "invertibility" in result
        assert "completeness" in result
    
    def test_run_complete_analysis(self):
        sm_hierarchy = SMHierarchyOperatorMixing()
        result = sm_hierarchy.run_complete_analysis()
        
        assert "SM→电弱" in result
        assert "电弱→GUT" in result
        assert "overall_completeness" in result
        assert "overall_invertibility" in result
        assert "conclusion" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])