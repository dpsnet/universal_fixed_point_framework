"""
test_error_budget.py

Phase 15C-4: 误差预算体系测试。

验证：
1. 误差源的独立性与组合
2. 各环节（Rec/Spec/预言/实验）的误差估计
3. 误差链传播的平方和规则
"""

from __future__ import annotations

import numpy as np
import pytest

from error_budget import (
    ErrorSource,
    ErrorBudget,
    estimate_rec_error,
    estimate_spec_error,
    estimate_physical_prediction_error,
    estimate_rkhs_error,
    estimate_gn_emergence_error,
    error_propagation_chain,
)


def test_error_source_creation():
    """误差源应正确存储属性。"""
    src = ErrorSource(
        name="test", absolute_error=0.1, relative_error=0.05,
        description="test", category="numerical",
    )
    assert src.name == "test"
    assert src.absolute_error == 0.1
    assert src.relative_error == 0.05
    assert src.category == "numerical"


def test_error_budget_total_empty():
    """空误差预算的总误差应为 0。"""
    budget = ErrorBudget()
    assert budget.total_absolute() == 0.0
    assert budget.total_relative() == 0.0


def test_error_budget_total_quadrature():
    """多项误差的平方和规则。"""
    budget = ErrorBudget()
    budget.truncation_error = ErrorSource(
        "trunc", 3.0, 0.01, "", "theoretical")
    budget.sampling_error = ErrorSource(
        "sampling", 4.0, 0.01, "", "numerical")
    # sqrt(3²+4²) = 5
    assert abs(budget.total_absolute() - 5.0) < 1e-10


def test_error_budget_dominant():
    """应正确识别主导误差。"""
    budget = ErrorBudget()
    budget.truncation_error = ErrorSource(
        "small", 1.0, 0.01, "", "theoretical")
    budget.sampling_error = ErrorSource(
        "large", 10.0, 0.01, "", "numerical")
    assert budget.dominant_error() == "large"
    assert budget.total_absolute() > 10.0


def test_estimate_rec_error():
    """Rec 层误差估计应随迭代次数递减。"""
    e1, _ = estimate_rec_error(n_iterations=10, n_samples=100, spectral_gap=0.5)
    e2, _ = estimate_rec_error(n_iterations=100, n_samples=1000, spectral_gap=0.5)
    assert e2 < e1


def test_estimate_spec_error():
    """Spec 层误差估计应随截断阶数递减。"""
    e1, _ = estimate_spec_error(eigenvalue_noise=1e-8, n_eigenvalues=10, truncation_order=1)
    e2, _ = estimate_spec_error(eigenvalue_noise=1e-8, n_eigenvalues=10, truncation_order=10)
    assert e2 < e1


def test_physical_prediction_budget():
    """物理预言误差预算应包含理论、数值、实验三类误差。"""
    budget = estimate_physical_prediction_error(
        mass_uncertainty=0.05, coupling_uncertainty=0.10)
    assert budget.approximation_error is not None
    assert budget.truncation_error is not None
    assert budget.systematic_error is not None
    assert budget.dominant_error() is not None


def test_rkhs_convergence_budget():
    """RKHS 收敛误差应随 N 增加而减少。"""
    b1 = estimate_rkhs_error(n_points=100, d_frac=1.5, smoothness=1.0)
    b2 = estimate_rkhs_error(n_points=10000, d_frac=1.5, smoothness=1.0)
    assert b2.total_absolute() < b1.total_absolute()


def test_gn_emergence_budget():
    """G_N 导出误差应为极小的数值误差。"""
    budget = estimate_gn_emergence_error()
    assert budget.convergence_error is not None
    assert budget.convergence_error.absolute_error < 1e-12


def test_error_propagation_chain():
    """误差链传播应正确识别主导环节。"""
    chain = error_propagation_chain(
        rec_error=0.01, spec_error=0.01,
        prediction_error=0.10, experiment_error=0.20,
    )
    assert chain["dominant"] == "实验对比"
    assert chain["total"] > 0.20


def test_error_budget_summary_contains_dominant():
    """预算摘要应包含主导误差信息。"""
    budget = ErrorBudget()
    budget.systematic_error = ErrorSource(
        "系统误差", 5.0, 0.10, "主要系统不确定性", "experimental")
    summary = budget.summary()
    assert "系统误差" in summary
    assert "主导误差" in summary


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
