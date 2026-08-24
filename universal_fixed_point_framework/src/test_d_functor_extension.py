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
test_d_functor_extension.py

Phase 15B-1/2: D 函子定义域扩展 + Freyd 放宽条件测试。

验证：
1. PVM 投影算子性质
2. 谱积分正确性
3. 连续谱对象构造
4. 扩展 D 函子映射
5. Freyd 有限极限保持
6. ε-解集条件
7. 弱伴随关系
"""

from __future__ import annotations

import numpy as np
import pytest

from rec_category import RecObject
from spec_category import PositiveSpectralObject
from d_functor_extension import (
    ProjectionValuedMeasure,
    ContinuousSpectralObject,
    ExtendedDecursionFunctor,
    FreydRelaxation,
)


def test_pvm_idempotency():
    """PVM 投影算子幂等性：P² = P。"""
    n = 4
    eigenvalues = np.array([0.1, 0.3, 0.5, 0.7])
    eigenvectors = np.eye(n)
    pvm = ProjectionValuedMeasure(eigenvalues, eigenvectors)

    P = pvm.project((0.2, 0.6))
    P_squared = P @ P

    assert np.allclose(P_squared, P), "投影算子应满足 P² = P"


def test_pvm_projection_orthogonality():
    """PVM 投影算子正交性：E(Δ₁)E(Δ₂) = 0 当 Δ₁∩Δ₂=∅。"""
    n = 4
    eigenvalues = np.array([0.1, 0.3, 0.5, 0.7])
    eigenvectors = np.eye(n)
    pvm = ProjectionValuedMeasure(eigenvalues, eigenvectors)

    P1 = pvm.project((0.0, 0.4))
    P2 = pvm.project((0.6, 1.0))

    product = P1 @ P2
    assert np.allclose(product, np.zeros_like(product)), "不相交区间投影应正交"


def test_pvm_spectral_integral():
    """谱积分正确性：∫ λ dE(λ) = A。"""
    n = 4
    eigenvalues = np.array([0.1, 0.3, 0.5, 0.7])
    eigenvectors = np.eye(n)
    pvm = ProjectionValuedMeasure(eigenvalues, eigenvectors)

    A = pvm.spectral_integral(lambda x: x)
    expected_A = np.diag(eigenvalues)

    assert np.allclose(A, expected_A), "谱积分应返回对角化的 A"


def test_continuous_spectral_object_from_positive():
    """从正谱对象构造连续谱对象。"""
    n = 3
    A = np.diag([0.2, 0.5, 0.8])
    E = PositiveSpectralObject(operator_A=A)

    cont_E = ContinuousSpectralObject.from_positive_spectral_object(E)

    assert cont_E.dim == n
    assert np.allclose(cont_E.operator_A, A)


def test_continuous_spectral_object_types():
    """不同谱类型的连续谱对象构造。"""
    n = 8
    seed = 42

    cont_E = ContinuousSpectralObject.from_continuous_spectrum(n, "continuous", seed)
    assert cont_E.spectral_type == "continuous"
    assert cont_E.dim == n

    sc_E = ContinuousSpectralObject.from_continuous_spectrum(n, "singular_continuous", seed)
    assert sc_E.spectral_type == "singular_continuous"

    mixed_E = ContinuousSpectralObject.from_continuous_spectrum(n, "mixed", seed)
    assert mixed_E.spectral_type == "mixed"


def test_extended_d_functor_map_object():
    """扩展 D 函子对象映射。"""
    n = 4
    rng = np.random.RandomState(42)
    state_space = np.eye(n)
    evolution = rng.rand(n, n)
    evolution = evolution / np.sum(evolution, axis=1, keepdims=True)

    R = RecObject(state_space=state_space, evolution=evolution)

    ext_D = ExtendedDecursionFunctor()
    cont_E = ext_D.map_object_continuous(R)

    assert cont_E.dim == n
    assert np.allclose(cont_E.operator_A, cont_E.operator_A.conj().T), "A 应为 Hermitian"


def test_extended_d_functor_spectral_integral():
    """扩展 D 函子谱积分。"""
    n = 4
    rng = np.random.RandomState(42)
    state_space = np.eye(n)
    evolution = rng.rand(n, n)
    evolution = evolution / np.sum(evolution, axis=1, keepdims=True)

    R = RecObject(state_space=state_space, evolution=evolution)

    ext_D = ExtendedDecursionFunctor()

    A_squared = ext_D.spectral_integral(R, lambda x: x**2)
    A_squared_direct = ext_D.spectral_integral_direct(R, lambda A: A @ A)

    assert np.allclose(A_squared, A_squared_direct), "谱积分 A² 应等于 A@A"


def test_freyd_preserves_finite_limits():
    """Freyd 条件：D 保持有限极限。"""
    n = 2
    evolution = np.diag([0.8, 0.6])
    state_space = np.eye(n)

    R = RecObject(state_space=state_space, evolution=evolution)

    freyd = FreydRelaxation()
    result = freyd.preserves_finite_limits(R, R)

    assert result, "D 应保持有限极限"


def test_freyd_epsilon_solution_set():
    """Freyd 条件：ε-解集条件。"""
    n = 4
    A = np.diag(np.linspace(0.1, 1.0, n))
    E = PositiveSpectralObject(operator_A=A)

    freyd = FreydRelaxation()
    result = freyd.epsilon_solution_set(E, epsilon=1e-6)

    assert result, "应满足 ε-解集条件"


def test_freyd_weak_adjoint_pair():
    """Freyd 条件：弱伴随关系。"""
    n = 2
    evolution = np.diag([0.8, 0.6])
    state_space = np.eye(n)

    R = RecObject(state_space=state_space, evolution=evolution)
    E = PositiveSpectralObject(operator_A=np.diag([0.2, 0.5]))

    freyd = FreydRelaxation()
    result = freyd.weak_adjoint_pair(R, E, epsilon=1e-6)

    assert result["left_triangle_ok"], "左三角恒等式应满足"
    assert result["right_triangle_ok"], "右三角恒等式应满足"


def test_freyd_full_conditions():
    """Freyd 放宽条件完整验证。"""
    n = 2
    evolution = np.diag([0.8, 0.6])
    state_space = np.eye(n)

    R = RecObject(state_space=state_space, evolution=evolution)
    E = PositiveSpectralObject(operator_A=np.diag([0.2, 0.5]))

    freyd = FreydRelaxation()
    results = freyd.verify_freyd_conditions(R, E)

    assert results["all_conditions_met"], "所有 Freyd 放宽条件应满足"


if __name__ == "__main__":
    print("=" * 60)
    print("Phase 15B-1/2: D 函子扩展 + Freyd 放宽条件测试")
    print("=" * 60)

    test_pvm_idempotency()
    print("  [1] PVM 幂等性 ✓")
    test_pvm_projection_orthogonality()
    print("  [2] PVM 正交性 ✓")
    test_pvm_spectral_integral()
    print("  [3] PVM 谱积分 ✓")
    test_continuous_spectral_object_from_positive()
    print("  [4] 连续谱对象构造 ✓")
    test_continuous_spectral_object_types()
    print("  [5] 不同谱类型 ✓")
    test_extended_d_functor_map_object()
    print("  [6] 扩展 D 函子映射 ✓")
    test_extended_d_functor_spectral_integral()
    print("  [7] 扩展 D 函子谱积分 ✓")
    test_freyd_preserves_finite_limits()
    print("  [8] Freyd 有限极限保持 ✓")
    test_freyd_epsilon_solution_set()
    print("  [9] Freyd ε-解集条件 ✓")
    test_freyd_weak_adjoint_pair()
    print("  [10] Freyd 弱伴随关系 ✓")
    test_freyd_full_conditions()
    print("  [11] Freyd 完整条件 ✓")

    print("\n" + "=" * 60)
    print("全部 D 函子扩展测试通过。")
    print("=" * 60)
