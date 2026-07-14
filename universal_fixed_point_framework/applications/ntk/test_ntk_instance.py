"""
test_ntk_instance.py

NTK 实例的单元测试：验证 NTKInstance 符合抽象框架接口，
并验证谱对应 λ_i = exp(-μ_i) 在 NTK 训练动态中成立。
"""

import sys
from pathlib import Path
import numpy as np

# 将项目 src 目录加入路径
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_SRC_DIR = _PROJECT_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from ntk_instance import NTKInstance, parse_cifar10_ntk_results
from rec_category import RecObject
from spec_category import PositiveSpectralObject


def test_ntk_instance_creation():
    """测试 NTKInstance 可以正常创建并计算摘要。"""
    print("\n[测试 1] NTKInstance 创建与摘要")
    ntk = NTKInstance(n_samples=10)
    summary = ntk.summary()

    assert "parameters" in summary
    assert "ntk_spectrum" in summary
    assert "koopman_eigenvalues" in summary
    assert "spectral_operator_eigenvalues" in summary
    print(f"  NTK 谱长度: {len(summary['ntk_spectrum'])}")
    print("  通过")


def test_rec_object_interface():
    """测试 to_rec_object 返回合法的 RecObject。"""
    print("\n[测试 2] Rec 对象接口")
    ntk = NTKInstance(n_samples=10)
    rec = ntk.to_rec_object()

    assert isinstance(rec, RecObject)
    assert rec.n_points == 10
    assert rec.metadata["type"] == "NTK_training"
    print(f"  Rec 对象维数: {rec.n_points}")
    print("  通过")


def test_spectral_object_interface():
    """测试 to_spectral_object 返回合法的 PositiveSpectralObject。"""
    print("\n[测试 3] Spectral 对象接口")
    ntk = NTKInstance(n_samples=10)
    spec = ntk.to_spectral_object()

    assert isinstance(spec, PositiveSpectralObject)
    assert spec.dim == 10
    assert np.all(spec.spectrum >= -1e-10)
    print(f"  Spectral 对象维数: {spec.dim}")
    print(f"  谱范围: [{spec.spectrum.min():.4f}, {spec.spectrum.max():.4f}]")
    print("  通过")


def test_spectral_correspondence():
    """验证 NTK 训练动态中的 λ_i = exp(-μ_i)。"""
    print("\n[测试 4] 谱对应 λ_i = exp(-μ_i)")
    ntk = NTKInstance(n_samples=20)
    summary = ntk.summary()

    mu = np.array(summary["spectral_operator_eigenvalues"])
    lambdas = np.array(summary["koopman_eigenvalues"])
    lambdas_from_exp = np.sort(np.exp(-mu))
    lambdas_sorted = np.sort(lambdas)

    diff = np.linalg.norm(lambdas_sorted - lambdas_from_exp)
    print(f"  差异 (Frobenius 范数): {diff:.2e}")
    assert diff < 1e-10, "谱对应未通过"
    print("  通过")


def test_custom_ntk_spectrum():
    """测试可以传入自定义 NTK 谱。"""
    print("\n[测试 5] 自定义 NTK 谱")
    custom_spectrum = np.array([1.0, 0.5, 0.25, 0.125])
    ntk = NTKInstance(n_samples=4, ntk_spectrum=custom_spectrum)
    summary = ntk.summary()

    assert np.allclose(
        np.array(summary["ntk_spectrum"]),
        custom_spectrum,
    )
    print(f"  自定义谱: {custom_spectrum}")
    print("  通过")


def test_cifar10_real_spectrum():
    """测试从真实 CIFAR-10 NTK 实验结果构造实例。"""
    print("\n[测试 6] 真实 CIFAR-10 NTK 谱对接")
    ntk = NTKInstance.from_cifar10_experiment()
    summary = ntk.summary()

    assert ntk.metadata["type"] == "NTK_CIFAR10_real"
    assert ntk.n_samples == 20
    assert "alpha" in ntk.metadata
    assert "beta" in ntk.metadata

    mu = np.array(summary["spectral_operator_eigenvalues"])
    lambdas = np.array(summary["koopman_eigenvalues"])
    lambdas_from_exp = np.sort(np.exp(-mu))
    diff = np.linalg.norm(np.sort(lambdas) - lambdas_from_exp)

    print(f"  数据集: {ntk.metadata['dataset']}")
    print(f"  样本数: {ntk.n_samples}")
    print(f"  alpha={ntk.metadata['alpha']:.6f}, beta={ntk.metadata['beta']:.6f}")
    print(f"  谱对应差异: {diff:.2e}")
    assert diff < 1e-10, "真实 NTK 谱对应未通过"
    print("  通过")


def main():
    print("=" * 60)
    print("NTK 实例接口测试")
    print("=" * 60)

    test_ntk_instance_creation()
    test_rec_object_interface()
    test_spectral_object_interface()
    test_spectral_correspondence()
    test_custom_ntk_spectrum()
    test_cifar10_real_spectrum()

    print("\n" + "=" * 60)
    print("所有测试通过。")
    print("=" * 60)


if __name__ == "__main__":
    main()
