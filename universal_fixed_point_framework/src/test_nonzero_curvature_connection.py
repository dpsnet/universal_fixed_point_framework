"""
test_nonzero_curvature_connection.py

Phase 15D-3: 纤维丛非零曲率联络测试。

验证：
1. Levi-Civita 联络构造
2. 规范联络构造
3. 曲率张量计算
4. 规范场曲率计算
5. 平行移动
6. 环绕计算
7. Bianchi 恒等式验证
8. Clifford 联络构造
"""

from __future__ import annotations

import numpy as np
import pytest

from nonzero_curvature_connection import FiberBundleConnection, CliffordConnection


def test_levicivita_connection():
    """Levi-Civita 联络构造。"""
    fb = FiberBundleConnection(base_dim=4, fiber_dim=8)
    metric = np.diag([1, -1, -1, -1])

    Gamma = fb.levicivita_connection(metric)

    assert Gamma.shape == (4, 4, 4)


def test_gauge_connection():
    """规范联络构造。"""
    fb = FiberBundleConnection(base_dim=4, fiber_dim=8)
    gauge_field = np.random.randn(4, 8, 8)

    A = fb.gauge_connection(gauge_field)

    assert A.shape == (4, 8, 8)


def test_total_connection():
    """总联络构造。"""
    fb = FiberBundleConnection(base_dim=4, fiber_dim=8)
    metric = np.diag([1, -1, -1, -1])
    gauge_field = np.random.randn(4, 8, 8)

    connection = fb.total_connection(metric, gauge_field)

    assert "levicivita" in connection
    assert "gauge" in connection
    assert connection["levicivita"].shape == (4, 4, 4)
    assert connection["gauge"].shape == (4, 8, 8)


def test_curvature_tensor():
    """曲率张量计算。"""
    fb = FiberBundleConnection(base_dim=4, fiber_dim=8)
    metric = np.array([
        [1, 0, 0, 0],
        [0, -2, 0, 0],
        [0, 0, -3, 0],
        [0, 0, 0, -4]
    ])
    gauge_field = np.random.randn(4, 8, 8)

    connection = fb.total_connection(metric, gauge_field)
    R = fb.curvature_tensor(connection)

    assert R.shape == (4, 4, 4, 4)

    F = fb.gauge_curvature(gauge_field)
    assert np.linalg.norm(F) > 0, "规范场曲率不应为零"


def test_gauge_curvature():
    """规范场曲率计算。"""
    fb = FiberBundleConnection(base_dim=4, fiber_dim=8)
    gauge_field = np.random.randn(4, 8, 8) + 1j * np.random.randn(4, 8, 8)

    F = fb.gauge_curvature(gauge_field)

    assert F.shape == (4, 4, 8, 8)
    assert np.linalg.norm(F) > 0, "场强不应为零"


def test_parallel_transport():
    """平行移动。"""
    fb = FiberBundleConnection(base_dim=4, fiber_dim=8)
    metric = np.diag([1, -1, -1, -1])
    gauge_field = np.random.randn(4, 8, 8)

    connection = fb.total_connection(metric, gauge_field)
    vector = np.random.randn(8)
    path = np.array([[0, 0, 0, 0], [0.1, 0, 0, 0]])

    transported = fb.parallel_transport(connection, vector, path)

    assert transported.shape == (8,)


def test_holonomy():
    """环绕计算。"""
    fb = FiberBundleConnection(base_dim=4, fiber_dim=8)
    metric = np.diag([1, -1, -1, -1])
    gauge_field = np.random.randn(4, 8, 8)

    connection = fb.total_connection(metric, gauge_field)
    closed_path = np.array([[0, 0, 0, 0], [0.1, 0, 0, 0], [0.1, 0.1, 0, 0], [0, 0.1, 0, 0], [0, 0, 0, 0]])

    holonomy = fb.holonomy(connection, closed_path)

    assert holonomy.shape == (8, 8)


def test_bianchi_identity():
    """Bianchi 恒等式验证。"""
    fb = FiberBundleConnection(base_dim=4, fiber_dim=8)
    metric = np.diag([1, -1, -1, -1])
    gauge_field = np.random.randn(4, 8, 8)

    connection = fb.total_connection(metric, gauge_field)
    violation = fb.verify_bianchi_identity(connection)

    assert violation < 1.0, "Bianchi 恒等式违背应较小"


def test_clifford_connection():
    """Clifford 联络构造。"""
    cl_conn = CliffordConnection(p=1, q=7)

    A_cl = cl_conn.clifford_gauge_field(coupling=0.1)
    assert A_cl.shape == (8, 16, 16)

    D_cl = cl_conn.dirac_operator_with_connection(A_cl)
    assert D_cl.shape == (16, 16)


def test_curvature_nonzero():
    """验证非零曲率。"""
    fb = FiberBundleConnection(base_dim=4, fiber_dim=8)
    metric = np.diag([1, -1, -1, -1])
    gauge_field = np.random.randn(4, 8, 8) + 1j * np.random.randn(4, 8, 8)

    F = fb.gauge_curvature(gauge_field)

    assert np.linalg.norm(F) > 1e-10, "规范场曲率不应为零"


if __name__ == "__main__":
    print("=" * 60)
    print("Phase 15D-3: 纤维丛非零曲率联络测试")
    print("=" * 60)

    test_levicivita_connection()
    print("  [1] Levi-Civita 联络构造 ✓")
    test_gauge_connection()
    print("  [2] 规范联络构造 ✓")
    test_total_connection()
    print("  [3] 总联络构造 ✓")
    test_curvature_tensor()
    print("  [4] 曲率张量计算 ✓")
    test_gauge_curvature()
    print("  [5] 规范场曲率计算 ✓")
    test_parallel_transport()
    print("  [6] 平行移动 ✓")
    test_holonomy()
    print("  [7] 环绕计算 ✓")
    test_bianchi_identity()
    print("  [8] Bianchi 恒等式验证 ✓")
    test_clifford_connection()
    print("  [9] Clifford 联络构造 ✓")
    test_curvature_nonzero()
    print("  [10] 非零曲率验证 ✓")

    print("\n" + "=" * 60)
    print("全部非零曲率联络测试通过。")
    print("=" * 60)
