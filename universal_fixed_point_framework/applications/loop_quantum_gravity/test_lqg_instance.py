"""
test_lqg_instance.py

圈量子引力实例的单元测试。
"""

import sys
from pathlib import Path
import numpy as np

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_SRC_DIR = _PROJECT_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from lqg_instance import LQGInstance
from rec_category import RecObject
from spec_category import PositiveSpectralObject


def test_lqg_creation():
    print("\n[测试 1] LQGInstance 创建与摘要")
    lqg = LQGInstance(n_edges=5)
    summary = lqg.summary()

    assert "parameters" in summary
    assert "area_spectrum" in summary
    assert len(summary["area_spectrum"]) == 5
    print(f"  边数: {len(summary['area_spectrum'])}, Immirzi γ = {lqg.immirzi}")
    print("  通过")


def test_rec_object_interface():
    print("\n[测试 2] Rec 对象接口")
    lqg = LQGInstance(n_edges=5)
    rec = lqg.to_rec_object()

    assert isinstance(rec, RecObject)
    assert rec.n_points == 5
    assert rec.metadata["type"] == "lqg_area_spectrum"
    print(f"  Rec 对象维数: {rec.n_points}")
    print("  通过")


def test_spectral_object_interface():
    print("\n[测试 3] Spectral 对象接口")
    lqg = LQGInstance(n_edges=5)
    spec = lqg.to_spectral_object()

    assert isinstance(spec, PositiveSpectralObject)
    assert spec.dim == 5
    assert np.all(spec.spectrum >= -1e-10)
    print(f"  Spectral 对象维数: {spec.dim}")
    print("  通过")


def test_spectral_correspondence():
    print("\n[测试 4] 谱对应 λ_i = exp(-μ_i)")
    lqg = LQGInstance(n_edges=7)
    summary = lqg.summary()

    mu = np.array(summary["spectral_operator_eigenvalues"])
    lambdas = np.array(summary["koopman_eigenvalues"])
    lambdas_from_exp = np.sort(np.exp(-mu))
    lambdas_sorted = np.sort(lambdas)

    diff = np.linalg.norm(lambdas_sorted - lambdas_from_exp)
    print(f"  差异 (Frobenius): {diff:.2e}")
    assert diff < 1e-10
    print("  通过")


def test_area_spectrum_monotonic():
    print("\n[测试 5] 面积谱随自旋单调递增")
    lqg = LQGInstance(n_edges=6)
    areas = lqg.area_spectrum()
    spins = lqg.spins()

    assert np.all(np.diff(areas) > 0)
    assert np.all(areas > 0)
    assert spins[0] == lqg.spin_step
    print(f"  面积范围: [{areas[0]:.4f}, {areas[-1]:.4f}] ℓ_P²")
    print("  通过")


def test_integer_spin_spectrum():
    print("\n[测试 6] 整数自旋谱")
    lqg = LQGInstance(n_edges=4, spin_step=1.0)
    spins = lqg.spins()

    assert np.allclose(spins, np.array([1.0, 2.0, 3.0, 4.0]))
    print(f"  整数自旋: {spins}")
    print("  通过")


def test_parameter_validation():
    print("\n[测试 7] 参数校验")
    try:
        LQGInstance(n_edges=0)
        assert False, "n_edges=0 应抛出 ValueError"
    except ValueError:
        print("  n_edges=0 正确抛出 ValueError")

    try:
        LQGInstance(immirzi=-0.1)
        assert False, "immirzi<=0 应抛出 ValueError"
    except ValueError:
        print("  immirzi<=0 正确抛出 ValueError")

    try:
        LQGInstance(spin_step=0.3)
        assert False, "非法 spin_step 应抛出 ValueError"
    except ValueError:
        print("  非法 spin_step 正确抛出 ValueError")
    print("  通过")


def main():
    print("=" * 60)
    print("圈量子引力实例接口测试")
    print("=" * 60)

    test_lqg_creation()
    test_rec_object_interface()
    test_spectral_object_interface()
    test_spectral_correspondence()
    test_area_spectrum_monotonic()
    test_integer_spin_spectrum()
    test_parameter_validation()

    print("\n" + "=" * 60)
    print("所有测试通过。")
    print("=" * 60)


if __name__ == "__main__":
    main()
