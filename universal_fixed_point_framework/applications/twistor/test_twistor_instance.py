"""
test_twistor_instance.py

扭量理论实例的单元测试。
"""

import sys
from pathlib import Path
import numpy as np

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_SRC_DIR = _PROJECT_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from twistor_instance import TwistorInstance
from rec_category import RecObject
from spec_category import PositiveSpectralObject


def test_twistor_creation():
    print("\n[测试 1] TwistorInstance 创建与摘要")
    tw = TwistorInstance(n_particles=4, seed=42)
    summary = tw.summary()

    assert "parameters" in summary
    assert "twistor_spectrum" in summary
    assert len(summary["twistor_spectrum"]) == 6  # C(4,2)
    print(f"  粒子数: {tw.n_particles}, 谱长度: {len(summary['twistor_spectrum'])}")
    print("  通过")


def test_rec_object_interface():
    print("\n[测试 2] Rec 对象接口")
    tw = TwistorInstance(n_particles=4, seed=42)
    rec = tw.to_rec_object()

    assert isinstance(rec, RecObject)
    assert rec.n_points == 6
    assert rec.metadata["type"] == "twistor_kinematics"
    print(f"  Rec 对象维数: {rec.n_points}")
    print("  通过")


def test_spectral_object_interface():
    print("\n[测试 3] Spectral 对象接口")
    tw = TwistorInstance(n_particles=4, seed=42)
    spec = tw.to_spectral_object()

    assert isinstance(spec, PositiveSpectralObject)
    assert spec.dim == 6
    assert np.all(spec.spectrum >= -1e-10)
    print(f"  Spectral 对象维数: {spec.dim}")
    print("  通过")


def test_spectral_correspondence():
    print("\n[测试 4] 谱对应 λ_i = exp(-μ_i)")
    tw = TwistorInstance(n_particles=5, seed=123)
    summary = tw.summary()

    mu = np.array(summary["spectral_operator_eigenvalues"])
    lambdas = np.array(summary["koopman_eigenvalues"])
    lambdas_from_exp = np.sort(np.exp(-mu))
    lambdas_sorted = np.sort(lambdas)

    diff = np.linalg.norm(lambdas_sorted - lambdas_from_exp)
    print(f"  差异 (Frobenius): {diff:.2e}")
    assert diff < 1e-10
    print("  通过")


def test_momenta_massless():
    print("\n[测试 5] 动量无质量且 Hermitian")
    tw = TwistorInstance(n_particles=4, seed=7)
    momenta = tw.momenta()

    assert momenta.shape == (4, 2, 2)
    for i, p in enumerate(momenta):
        assert np.allclose(p, p.conj().T)
        det = np.linalg.det(p)
        assert np.isclose(det, 0.0, atol=1e-10)
    print(f"  所有 {len(momenta)} 个动量 det(p_i) ≈ 0")
    print("  通过")


def test_kinematic_invariants():
    print("\n[测试 6] 运动学不变量非负")
    tw = TwistorInstance(n_particles=4, seed=7)

    invariants = []
    for i in range(tw.n_particles):
        for j in range(i + 1, tw.n_particles):
            invariants.append(tw.kinematic_invariant(i, j))
    invariants = np.array(invariants)

    assert np.all(invariants >= 0)
    print(f"  不变量范围: [{invariants.min():.4f}, {invariants.max():.4f}]")
    print("  通过")


def test_string_amplitude_linkage():
    print("\n[测试 7] 与弦论散射振幅联动")
    tw = TwistorInstance(n_particles=4, seed=99)
    s, t = 0.3, 0.5

    amp_open = tw.scattering_amplitude(s, t, string_type="open")
    amp_closed = tw.scattering_amplitude(s, t, string_type="closed")

    assert np.isfinite(amp_open)
    assert np.isfinite(amp_closed)
    print(f"  A_open = {amp_open:.4f}, A_closed = {amp_closed:.4f}")
    print("  通过")


def test_parameter_validation():
    print("\n[测试 8] 参数校验")
    try:
        TwistorInstance(n_particles=1)
        assert False, "n_particles<2 应抛出 ValueError"
    except ValueError:
        print("  n_particles<2 正确抛出 ValueError")

    try:
        TwistorInstance(n_particles=4).scattering_amplitude(0.3, 0.5, string_type="bosonic")
        assert False, "非法 string_type 应抛出 ValueError"
    except ValueError:
        print("  非法 string_type 正确抛出 ValueError")
    print("  通过")


def main():
    print("=" * 60)
    print("扭量理论实例接口测试")
    print("=" * 60)

    test_twistor_creation()
    test_rec_object_interface()
    test_spectral_object_interface()
    test_spectral_correspondence()
    test_momenta_massless()
    test_kinematic_invariants()
    test_string_amplitude_linkage()
    test_parameter_validation()

    print("\n" + "=" * 60)
    print("所有测试通过。")
    print("=" * 60)


if __name__ == "__main__":
    main()
