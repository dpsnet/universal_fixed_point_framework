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
test_spectral_silence_axiomatization.py

测试谱静默测度论公理化定义。
"""

import numpy as np
import pytest

from spectral_silence_axiomatization import SpectralSilenceAxioms


class TestSpectralSilenceAxioms:
    """谱静默公理测试类。"""

    def setup_method(self):
        """初始化测试环境。"""
        self.axioms = SpectralSilenceAxioms()

    def test_axiom_A1_valid(self):
        """A1: 有效概率测度。"""
        measure = np.array([0.25, 0.25, 0.25, 0.25])
        support = np.array([0.0, 0.25, 0.5, 0.75])

        result = self.axioms.axiom_A1(measure, support)
        assert result is True or np.isclose(result, True)

    def test_axiom_A1_invalid_mass(self):
        """A1: 无效概率测度（质量不为1）。"""
        measure = np.array([0.3, 0.3, 0.3])
        support = np.array([0.0, 0.5, 1.0])

        result = self.axioms.axiom_A1(measure, support)
        assert result is False or np.isclose(result, False)

    def test_axiom_A1_invalid_negative(self):
        """A1: 无效概率测度（负值）。"""
        measure = np.array([0.5, -0.1, 0.6])
        support = np.array([0.0, 0.5, 1.0])

        result = self.axioms.axiom_A1(measure, support)
        assert result is False or np.isclose(result, False)

    def test_axiom_A2_range(self):
        """A2: 静默度范围在 [0, 1]。"""
        cantor_points = np.array([0.0, 1.0, 0.25, 0.75])
        cantor_measure = np.ones(4) / 4

        silence = self.axioms.axiom_A2(cantor_measure, cantor_points)

        assert 0.0 <= silence <= 1.0

    def test_axiom_A3_range(self):
        """A3: 维度比范围在 [0, 1]。"""
        cantor_points = np.array([0.0, 1.0, 0.25, 0.75])
        cantor_measure = np.ones(4) / 4

        ratio = self.axioms.axiom_A3(cantor_measure, cantor_points)

        assert 0.0 <= ratio <= 1.0

    def test_axiom_A4_laci_finite(self):
        """A4: LACI 有限值。"""
        points = np.array([0.0, 0.1, 0.2, 0.3])
        measure = np.ones(4) / 4

        laci = self.axioms.axiom_A4(measure, points)

        assert np.isfinite(laci)

    def test_criterion_S1_cantor(self):
        """S1: Cantor 集满足分形结构。"""
        cantor_points = np.array([0.0, 1.0, 0.25, 0.75, 0.125, 0.375, 0.625, 0.875])
        cantor_measure = np.ones(8) / 8

        result = self.axioms.criterion_S1(cantor_measure, cantor_points)
        assert result is True or result == 1

    def test_criterion_S1_continuous(self):
        """S1: 连续支撑不满足分形结构。"""
        continuous_points = np.linspace(0, 1, 100)
        continuous_measure = np.ones(100) / 100

        result = self.axioms.criterion_S1(continuous_measure, continuous_points)
        assert result is False or result == 0

    def test_criterion_S2_discrete(self):
        """S2: 离散谱满足（无连续分量）。"""
        discrete_points = np.array([0.0, 0.5, 1.0])
        discrete_measure = np.ones(3) / 3

        result = self.axioms.criterion_S2(discrete_measure, discrete_points)
        assert result is True or result == 1

    def test_criterion_S2_continuous(self):
        """S2: 连续谱不满足（有连续分量）。"""
        continuous_points = np.linspace(0, 1, 100)
        continuous_measure = np.ones(100) / 100

        result = self.axioms.criterion_S2(continuous_measure, continuous_points)
        assert result is False or result == 0

    def test_criterion_S3_dense(self):
        """S3: 稠密点集满足（LACI 大，自适应阈值）。"""
        dense_points = np.array([i / 1000.0 for i in range(1000)])
        dense_measure = np.ones(1000) / 1000

        result = self.axioms.criterion_S3(dense_measure, dense_points)
        assert result is True or result == 1

    def test_criterion_S3_sparse(self):
        """S3: 稀疏点集不满足（LACI 小，自适应阈值）。"""
        sparse_points = np.array([0.0, 0.5, 1.0])
        sparse_measure = np.ones(3) / 3

        result = self.axioms.criterion_S3(sparse_measure, sparse_points)
        assert result is False or result == 0

    def test_criterion_S4_uniform(self):
        """S4: 均匀分布满足（最大概率 <= 0.5）。"""
        points = np.array([0.0, 0.25, 0.5, 0.75])
        measure = np.ones(4) / 4

        result = self.axioms.criterion_S4(measure, points)
        assert result is True or result == 1

    def test_criterion_S4_nonuniform(self):
        """S4: 非均匀分布不满足（最大概率 > 0.5）。"""
        points = np.array([0.0, 0.25, 0.5, 0.75])
        measure = np.array([0.6, 0.2, 0.1, 0.1])

        result = self.axioms.criterion_S4(measure, points)
        assert result is False or result == 0

    def test_silence_degree_comprehensive(self):
        """综合静默度计算。"""
        cantor_points = np.array([0.0, 1.0, 0.25, 0.75, 0.125, 0.375, 0.625, 0.875])
        cantor_measure = np.ones(8) / 8

        result = self.axioms.silence_degree_axiomatic(cantor_measure, cantor_points)

        assert "axiom_A1_valid" in result
        assert "silence_degree_A2" in result
        assert "dimension_ratio_A3" in result
        assert "laci_A4" in result
        assert "S1" in result
        assert "S2" in result
        assert "S3" in result
        assert "S4" in result
        assert "satisfied_criteria" in result
        assert "overall_silence_degree" in result
        assert 0.0 <= result["overall_silence_degree"] <= 1.0

    def test_independence_verification(self):
        """判据独立性验证。"""
        independence = self.axioms.verify_independence()

        assert len(independence) == 4
        for key in ["S1_only", "S2_only", "S3_only", "S4_only"]:
            assert key in independence

    def test_completeness_verification(self):
        """判据完备性验证。"""
        completeness = self.axioms.verify_completeness()

        assert "theorem" in completeness
        assert "proof_sketch" in completeness
        assert "counterexamples" in completeness

    def test_hausdorff_dimension_estimate(self):
        """Hausdorff 维数估计。"""
        cantor_points = np.array([0.0, 1.0, 0.25, 0.75])
        cantor_measure = np.ones(4) / 4

        dim_h = self.axioms._hausdorff_dimension_estimate(cantor_measure, cantor_points)

        assert dim_h >= 0.0
        assert dim_h <= 1.0

    def test_overall_silence_degree_range(self):
        """综合静默度范围。"""
        points = np.array([0.0, 0.5, 1.0])
        measure = np.ones(3) / 3

        degree = self.axioms._overall_silence_degree(measure, points)

        assert 0.0 <= degree <= 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
