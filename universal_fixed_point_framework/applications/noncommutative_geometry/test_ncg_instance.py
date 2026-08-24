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
test_ncg_instance.py

非交换几何（谱三元组）实例的单元测试。
"""

import sys
from pathlib import Path
import numpy as np

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_SRC_DIR = _PROJECT_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from ncg_instance import NCGInstance
from rec_category import RecObject
from spec_category import PositiveSpectralObject


def test_ncg_creation():
    print("\n[测试 1] NCGInstance 创建与摘要")
    ncg = NCGInstance(n_points=5)
    summary = ncg.summary()

    assert "parameters" in summary
    assert "dirac_eigenvalues" in summary
    assert len(summary["dirac_eigenvalues"]) == 5
    print(f"  本征值数: {len(summary['dirac_eigenvalues'])}, cutoff = {ncg.cutoff}")
    print("  通过")


def test_rec_object_interface():
    print("\n[测试 2] Rec 对象接口")
    ncg = NCGInstance(n_points=5)
    rec = ncg.to_rec_object()

    assert isinstance(rec, RecObject)
    assert rec.n_points == 5
    assert rec.metadata["type"] == "ncg_dirac_spectrum"
    print(f"  Rec 对象维数: {rec.n_points}")
    print("  通过")


def test_spectral_object_interface():
    print("\n[测试 3] Spectral 对象接口")
    ncg = NCGInstance(n_points=5)
    spec = ncg.to_spectral_object()

    assert isinstance(spec, PositiveSpectralObject)
    assert spec.dim == 5
    assert np.all(spec.spectrum >= -1e-10)
    print(f"  Spectral 对象维数: {spec.dim}")
    print("  通过")


def test_spectral_correspondence():
    print("\n[测试 4] 谱对应 λ_i = exp(-μ_i)")
    ncg = NCGInstance(n_points=6)
    summary = ncg.summary()

    mu = np.array(summary["spectral_operator_eigenvalues"])
    lambdas = np.array(summary["koopman_eigenvalues"])
    lambdas_from_exp = np.sort(np.exp(-mu))
    lambdas_sorted = np.sort(lambdas)

    diff = np.linalg.norm(lambdas_sorted - lambdas_from_exp)
    print(f"  差异 (Frobenius): {diff:.2e}")
    assert diff < 1e-10
    print("  通过")


def test_absolute_eigenvalues():
    print("\n[测试 5] |D| 本征值非负")
    custom = [-2.0, -1.0, 0.0, 1.0, 2.0]
    ncg = NCGInstance(eigenvalues=custom)
    abs_eigs = ncg.absolute_eigenvalues()

    assert np.all(abs_eigs >= 0)
    assert np.allclose(abs_eigs, np.array([2.0, 1.0, 0.0, 1.0, 2.0]))
    print(f"  |D| 本征值: {abs_eigs}")
    print("  通过")


def test_custom_eigenvalues():
    print("\n[测试 6] 自定义 Dirac 本征值")
    custom = [0.0, 0.5, 1.5, 3.0]
    ncg = NCGInstance(eigenvalues=custom)

    assert np.allclose(ncg.dirac_eigenvalues(), np.array(custom))
    assert ncg.n_points == 4
    print(f"  自定义本征值: {ncg.dirac_eigenvalues()}")
    print("  通过")


def test_spectral_action():
    print("\n[测试 7] 谱作用计算")
    ncg = NCGInstance(eigenvalues=[0.0, 1.0, 2.0, 3.0], cutoff=2.0)
    action = ncg.spectral_action()

    expected = np.sum(np.exp(-(np.array([0.0, 1.0, 2.0, 3.0]) / 2.0) ** 2))
    assert np.isclose(action, expected)
    print(f"  谱作用 S_Λ(D) ≈ {action:.4f}")
    print("  通过")


def test_parameter_validation():
    print("\n[测试 8] 参数校验")
    try:
        NCGInstance(n_points=0)
        assert False, "n_points=0 应抛出 ValueError"
    except ValueError:
        print("  n_points=0 正确抛出 ValueError")

    try:
        NCGInstance(cutoff=-1.0)
        assert False, "cutoff<=0 应抛出 ValueError"
    except ValueError:
        print("  cutoff<=0 正确抛出 ValueError")
    print("  通过")


def main():
    print("=" * 60)
    print("非交换几何实例接口测试")
    print("=" * 60)

    test_ncg_creation()
    test_rec_object_interface()
    test_spectral_object_interface()
    test_spectral_correspondence()
    test_absolute_eigenvalues()
    test_custom_eigenvalues()
    test_spectral_action()
    test_parameter_validation()

    print("\n" + "=" * 60)
    print("所有测试通过。")
    print("=" * 60)


if __name__ == "__main__":
    main()
