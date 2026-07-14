"""
test_tqft_instance.py

TQFT / 任意子融合范畴实例的单元测试。
"""

import sys
from pathlib import Path
import numpy as np

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_SRC_DIR = _PROJECT_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from tqft_instance import TQFTInstance
from rec_category import RecObject
from spec_category import PositiveSpectralObject


def test_tqft_creation():
    print("\n[测试 1] TQFTInstance 创建与摘要")
    tqft = TQFTInstance(model="ising")
    summary = tqft.summary()

    assert "parameters" in summary
    assert "topological_invariants" in summary
    assert len(summary["topological_invariants"]) == 3
    print(f"  模型: {tqft.model}, 任意子数: {tqft.n_anyons}")
    print("  通过")


def test_rec_object_interface():
    print("\n[测试 2] Rec 对象接口")
    tqft = TQFTInstance(model="ising")
    rec = tqft.to_rec_object()

    assert isinstance(rec, RecObject)
    assert rec.n_points == 3
    assert rec.metadata["type"] == "tqft_quantum_dimensions"
    print(f"  Rec 对象维数: {rec.n_points}")
    print("  通过")


def test_spectral_object_interface():
    print("\n[测试 3] Spectral 对象接口")
    tqft = TQFTInstance(model="ising")
    spec = tqft.to_spectral_object()

    assert isinstance(spec, PositiveSpectralObject)
    assert spec.dim == 3
    assert np.all(spec.spectrum >= -1e-10)
    print(f"  Spectral 对象维数: {spec.dim}")
    print("  通过")


def test_spectral_correspondence():
    print("\n[测试 4] 谱对应 λ_i = exp(-μ_i)")
    tqft = TQFTInstance(model="ising")
    summary = tqft.summary()

    mu = np.array(summary["spectral_operator_eigenvalues"])
    lambdas = np.array(summary["koopman_eigenvalues"])
    lambdas_from_exp = np.sort(np.exp(-mu))
    lambdas_sorted = np.sort(lambdas)

    diff = np.linalg.norm(lambdas_sorted - lambdas_from_exp)
    print(f"  差异 (Frobenius): {diff:.2e}")
    assert diff < 1e-10
    print("  通过")


def test_ising_quantum_dimensions():
    print("\n[测试 5] Ising 量子维度")
    tqft = TQFTInstance(model="ising")
    dims = tqft.topological_spectrum()

    expected = np.array([1.0, np.sqrt(2.0), 1.0])
    assert np.allclose(dims, expected)
    print(f"  量子维度: {dims}")
    print("  通过")


def test_fibonacci_quantum_dimensions():
    print("\n[测试 6] Fibonacci 量子维度")
    tqft = TQFTInstance(model="fibonacci")
    dims = tqft.topological_spectrum()

    phi = 0.5 * (1.0 + np.sqrt(5.0))
    expected = np.array([1.0, phi])
    assert np.allclose(dims, expected)
    print(f"  量子维度: {dims}")
    print("  通过")


def test_custom_invariants():
    print("\n[测试 7] 自定义拓扑不变量")
    custom = [1.0, 2.0, 3.0, 5.0]
    tqft = TQFTInstance(model="custom", user_invariants=custom)

    assert np.allclose(tqft.topological_spectrum(), np.array(custom))
    assert tqft.n_anyons == 4
    print(f"  自定义不变量: {tqft.topological_spectrum()}")
    print("  通过")


def test_parameter_validation():
    print("\n[测试 8] 参数校验")
    try:
        TQFTInstance(model="unknown")
        assert False, "非法 model 应抛出 ValueError"
    except ValueError:
        print("  非法 model 正确抛出 ValueError")

    try:
        TQFTInstance(model="custom", user_invariants=[])
        assert False, "空 user_invariants 应抛出 ValueError"
    except ValueError:
        print("  空 user_invariants 正确抛出 ValueError")

    try:
        TQFTInstance(model="custom", user_invariants=[1.0, -2.0])
        assert False, "负不变量应抛出 ValueError"
    except ValueError:
        print("  负不变量正确抛出 ValueError")
    print("  通过")


def main():
    print("=" * 60)
    print("TQFT / 任意子融合范畴实例接口测试")
    print("=" * 60)

    test_tqft_creation()
    test_rec_object_interface()
    test_spectral_object_interface()
    test_spectral_correspondence()
    test_ising_quantum_dimensions()
    test_fibonacci_quantum_dimensions()
    test_custom_invariants()
    test_parameter_validation()

    print("\n" + "=" * 60)
    print("所有测试通过。")
    print("=" * 60)


if __name__ == "__main__":
    main()
