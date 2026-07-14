"""
test_ads_cft_instance.py

AdS/CFT 实例的单元测试。
"""

import sys
from pathlib import Path
import numpy as np

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_SRC_DIR = _PROJECT_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from ads_cft_instance import AdSCFTInstance
from rec_category import RecObject
from spec_category import PositiveSpectralObject


def test_ads_cft_creation():
    print("\n[测试 1] AdSCFTInstance 创建与摘要")
    ads = AdSCFTInstance(n_operators=6)
    summary = ads.summary()

    assert "parameters" in summary
    assert "scaling_dimensions" in summary
    assert len(summary["scaling_dimensions"]) == 6
    print(f"  算子数: {len(summary['scaling_dimensions'])}, c = {ads.central_charge}")
    print("  通过")


def test_rec_object_interface():
    print("\n[测试 2] Rec 对象接口")
    ads = AdSCFTInstance(n_operators=6)
    rec = ads.to_rec_object()

    assert isinstance(rec, RecObject)
    assert rec.n_points == 6
    assert rec.metadata["type"] == "ads_cft_primary_spectrum"
    print(f"  Rec 对象维数: {rec.n_points}")
    print("  通过")


def test_spectral_object_interface():
    print("\n[测试 3] Spectral 对象接口")
    ads = AdSCFTInstance(n_operators=6)
    spec = ads.to_spectral_object()

    assert isinstance(spec, PositiveSpectralObject)
    assert spec.dim == 6
    assert np.all(spec.spectrum >= -1e-10)
    print(f"  Spectral 对象维数: {spec.dim}")
    print("  通过")


def test_spectral_correspondence():
    print("\n[测试 4] 谱对应 λ_i = exp(-μ_i)")
    ads = AdSCFTInstance(n_operators=8)
    summary = ads.summary()

    mu = np.array(summary["spectral_operator_eigenvalues"])
    lambdas = np.array(summary["koopman_eigenvalues"])
    lambdas_from_exp = np.sort(np.exp(-mu))
    lambdas_sorted = np.sort(lambdas)

    diff = np.linalg.norm(lambdas_sorted - lambdas_from_exp)
    print(f"  差异 (Frobenius): {diff:.2e}")
    assert diff < 1e-10
    print("  通过")


def test_scaling_dimensions_nonnegative():
    print("\n[测试 5] 标度维数非负且 identity 维数为零")
    ads = AdSCFTInstance(n_operators=6)
    dims = ads.scaling_dimensions()

    assert np.all(dims >= 0)
    assert dims[0] == 0.0
    print(f"  标度维数: {dims}")
    print("  通过")


def test_custom_dimensions():
    print("\n[测试 6] 自定义标度维数")
    custom_dims = [0.0, 1.0, 1.5, 2.0, 2.5]
    ads = AdSCFTInstance(n_operators=5, operator_dimensions=custom_dims)

    assert np.allclose(ads.scaling_dimensions(), np.array(custom_dims))
    print(f"  自定义维数: {ads.scaling_dimensions()}")
    print("  通过")


def test_parameter_validation():
    print("\n[测试 7] 参数校验")
    try:
        AdSCFTInstance(n_operators=0)
        assert False, "n_operators=0 应抛出 ValueError"
    except ValueError:
        print("  n_operators=0 正确抛出 ValueError")

    try:
        AdSCFTInstance(central_charge=-1.0)
        assert False, "central_charge<=0 应抛出 ValueError"
    except ValueError:
        print("  central_charge<=0 正确抛出 ValueError")

    try:
        AdSCFTInstance(n_operators=3, operator_dimensions=[0.0, 1.0])
        assert False, "operator_dimensions 长度不一致应抛出 ValueError"
    except ValueError:
        print("  operator_dimensions 长度不一致正确抛出 ValueError")

    try:
        AdSCFTInstance(n_operators=2, operator_dimensions=[0.0, -1.0])
        assert False, "负维数应抛出 ValueError"
    except ValueError:
        print("  负维数正确抛出 ValueError")
    print("  通过")


def main():
    print("=" * 60)
    print("AdS/CFT 实例接口测试")
    print("=" * 60)

    test_ads_cft_creation()
    test_rec_object_interface()
    test_spectral_object_interface()
    test_spectral_correspondence()
    test_scaling_dimensions_nonnegative()
    test_custom_dimensions()
    test_parameter_validation()

    print("\n" + "=" * 60)
    print("所有测试通过。")
    print("=" * 60)


if __name__ == "__main__":
    main()
