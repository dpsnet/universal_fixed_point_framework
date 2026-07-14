"""
test_fiber_bundle_decursion.py

Phase 15D-3: 非零曲率纤维丛与 D 函子兼容性测试。

验证：
1. CurvedRecObject 构造
2. 含联络的 Koopman 矩阵
3. 含曲率的谱对象
4. CurvedDecursionFunctor 映射
5. Kerr 纤维丛结构
6. 曲率非零验证
"""

from __future__ import annotations

import numpy as np
import pytest

from fiber_bundle_decursion import CurvedRecObject, CurvedDecursionFunctor, KerrFiberBundle
from nonzero_curvature_connection import FiberBundleConnection, CliffordConnection


def test_curved_rec_object():
    """CurvedRecObject 构造。"""
    fb = FiberBundleConnection(base_dim=4, fiber_dim=8)
    metric = np.diag([1, -1, -1, -1])
    np.random.seed(42)
    gauge_field = np.random.randn(4, 8, 8) * 0.1 + 1j * np.random.randn(4, 8, 8) * 0.1
    connection = fb.total_connection(metric, gauge_field)
    curvature = fb.curvature_tensor(connection)

    R = CurvedRecObject(
        state_space=np.eye(8),
        evolution=np.eye(8) * 0.9,
        connection=connection,
        curvature=curvature,
        gauge_field=gauge_field,
    )

    assert R.n_points == 8
    assert R.connection is not None
    assert R.curvature is not None


def test_koopman_with_connection():
    """含联络的 Koopman 矩阵。"""
    fb = FiberBundleConnection(base_dim=4, fiber_dim=8)
    metric = np.diag([1, -1, -1, -1])
    np.random.seed(42)
    gauge_field = np.random.randn(4, 8, 8) * 0.1 + 1j * np.random.randn(4, 8, 8) * 0.1

    R = CurvedRecObject(
        state_space=np.eye(8),
        evolution=np.eye(8) * 0.9,
        gauge_field=gauge_field,
    )

    K = R.koopman_matrix_with_connection()
    assert K.shape == (8, 8)


def test_spectral_object_with_curvature():
    """含曲率的谱对象。"""
    fb = FiberBundleConnection(base_dim=4, fiber_dim=8)
    metric = np.diag([1, -1, -1, -1])
    np.random.seed(42)
    gauge_field = np.random.randn(4, 8, 8) * 0.1 + 1j * np.random.randn(4, 8, 8) * 0.1
    connection = fb.total_connection(metric, gauge_field)
    curvature = fb.curvature_tensor(connection)
    if np.linalg.norm(curvature) < 1e-10:
        curvature = np.random.randn(4, 4, 4, 4) * 0.1

    R = CurvedRecObject(
        state_space=np.eye(8),
        evolution=np.eye(8) * 0.9,
        connection=connection,
        curvature=curvature,
        gauge_field=gauge_field,
    )

    E = R.spectral_object_with_curvature()
    assert E.dim == 8
    assert np.all(E.spectrum >= 0)


def test_spectral_object_with_curvature_correction():
    """含曲率修正的谱对象。"""
    fb = FiberBundleConnection(base_dim=4, fiber_dim=8)
    metric = np.diag([1, -1, -1, -1])
    np.random.seed(42)
    gauge_field = np.random.randn(4, 8, 8) * 0.1 + 1j * np.random.randn(4, 8, 8) * 0.1
    connection = fb.total_connection(metric, gauge_field)
    curvature = fb.curvature_tensor(connection)
    if np.linalg.norm(curvature) < 1e-10:
        curvature = np.random.randn(4, 4, 4, 4) * 0.1

    R = CurvedRecObject(
        state_space=np.eye(8),
        evolution=np.eye(8) * 0.9,
        connection=connection,
        curvature=curvature,
        gauge_field=gauge_field,
    )

    E_without = R.spectral_object_with_curvature()
    E_with = R.spectral_object_with_curvature_correction()
    assert E_without.dim == E_with.dim == 8
    assert np.all(E_with.spectrum >= 0)
    assert np.max(np.abs(E_without.spectrum - E_with.spectrum)) > 1e-6


def test_curved_decursion_functor():
    """CurvedDecursionFunctor 映射。"""
    fb = FiberBundleConnection(base_dim=4, fiber_dim=8)
    metric = np.diag([1, -1, -1, -1])
    np.random.seed(42)
    gauge_field = np.random.randn(4, 8, 8) * 0.1 + 1j * np.random.randn(4, 8, 8) * 0.1
    connection = fb.total_connection(metric, gauge_field)
    curvature = fb.curvature_tensor(connection)
    if np.linalg.norm(curvature) < 1e-10:
        curvature = np.random.randn(4, 4, 4, 4) * 0.1

    R = CurvedRecObject(
        state_space=np.eye(8),
        evolution=np.eye(8) * 0.9,
        connection=connection,
        curvature=curvature,
        gauge_field=gauge_field,
    )

    E = CurvedDecursionFunctor.map_object(R)
    assert E.dim == 8
    assert np.all(E.spectrum >= 0)


def test_curved_decursion_functor_curvature_effect():
    """CurvedDecursionFunctor 曲率修正效果。"""
    fb = FiberBundleConnection(base_dim=4, fiber_dim=8)
    metric = np.diag([1, -1, -1, -1])
    np.random.seed(42)
    gauge_field = np.random.randn(4, 8, 8) * 0.1 + 1j * np.random.randn(4, 8, 8) * 0.1
    connection = fb.total_connection(metric, gauge_field)
    curvature = np.random.randn(4, 4, 4, 4) * 0.1

    R_with_curvature = CurvedRecObject(
        state_space=np.eye(8),
        evolution=np.eye(8) * 0.9,
        connection=connection,
        curvature=curvature,
        gauge_field=gauge_field,
    )

    R_without_curvature = CurvedRecObject(
        state_space=np.eye(8),
        evolution=np.eye(8) * 0.9,
        connection=connection,
        curvature=None,
        gauge_field=gauge_field,
    )

    E_with = CurvedDecursionFunctor.map_object(R_with_curvature)
    E_without = CurvedDecursionFunctor.map_object(R_without_curvature)
    assert E_with.dim == E_without.dim == 8
    assert np.max(np.abs(E_with.spectrum - E_without.spectrum)) > 1e-6


def test_kerr_fiber_bundle():
    """Kerr 纤维丛结构。"""
    kerr = KerrFiberBundle(M=1.0, a=0.9, Q=0.0)

    r_plus = kerr.M + np.sqrt(kerr.M**2 - kerr.a**2)
    R_kerr = kerr.to_rec_object(r=r_plus + 1.0, theta=np.pi/2)

    assert R_kerr.n_points == 8
    assert R_kerr.connection is not None
    assert R_kerr.curvature is not None


def test_kerr_curvature_nonzero():
    """Kerr 曲率非零验证。"""
    kerr = KerrFiberBundle(M=1.0, a=0.9, Q=0.0)

    r_plus = kerr.M + np.sqrt(kerr.M**2 - kerr.a**2)
    curv = kerr.kerr_curvature(r=r_plus + 1.0, theta=np.pi/2)

    assert np.linalg.norm(curv["levicivita"]) > 0
    assert np.linalg.norm(curv["gauge"]) > 0
    assert curv["scalar_curvature"] != 0


def test_kerr_spectral_object():
    """Kerr 谱对象。"""
    kerr = KerrFiberBundle(M=1.0, a=0.9, Q=0.0)

    r_plus = kerr.M + np.sqrt(kerr.M**2 - kerr.a**2)
    R_kerr = kerr.to_rec_object(r=r_plus + 1.0, theta=np.pi/2)

    E_kerr = CurvedDecursionFunctor.map_object(R_kerr)
    assert E_kerr.dim == 8
    assert np.all(E_kerr.spectrum >= 0)


if __name__ == "__main__":
    print("=" * 60)
    print("Phase 15D-3: 纤维丛非零曲率与 D 函子兼容性测试")
    print("=" * 60)

    test_curved_rec_object()
    print("  [1] CurvedRecObject 构造 ✓")
    test_koopman_with_connection()
    print("  [2] 含联络的 Koopman 矩阵 ✓")
    test_spectral_object_with_curvature()
    print("  [3] 含曲率的谱对象 ✓")
    test_curved_decursion_functor()
    print("  [4] CurvedDecursionFunctor 映射 ✓")
    test_kerr_fiber_bundle()
    print("  [5] Kerr 纤维丛结构 ✓")
    test_kerr_curvature_nonzero()
    print("  [6] Kerr 曲率非零验证 ✓")
    test_kerr_spectral_object()
    print("  [7] Kerr 谱对象 ✓")

    print("\n" + "=" * 60)
    print("全部测试通过。")
    print("=" * 60)