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
test_asymptotic_safety_instance.py

渐近安全实例的单元测试。
"""

import sys
from pathlib import Path
import numpy as np

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_SRC_DIR = _PROJECT_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from asymptotic_safety_instance import AsymptoticSafetyInstance
from rec_category import RecObject
from spec_category import PositiveSpectralObject


def test_as_creation():
    print("\n[测试 1] AsymptoticSafetyInstance 创建与摘要")
    a_s = AsymptoticSafetyInstance(n_couplings=4)
    summary = a_s.summary()

    assert "parameters" in summary
    assert "critical_exponents" in summary
    assert len(summary["critical_exponents"]) == 4
    print(f"  耦合数: {a_s.n_couplings}")
    print("  通过")


def test_rec_object_interface():
    print("\n[测试 2] Rec 对象接口")
    a_s = AsymptoticSafetyInstance(n_couplings=4)
    rec = a_s.to_rec_object()

    assert isinstance(rec, RecObject)
    assert rec.n_points == 4
    assert rec.metadata["type"] == "asymptotic_safety_spectrum"
    print(f"  Rec 对象维数: {rec.n_points}")
    print("  通过")


def test_spectral_object_interface():
    print("\n[测试 3] Spectral 对象接口")
    a_s = AsymptoticSafetyInstance(n_couplings=4)
    spec = a_s.to_spectral_object()

    assert isinstance(spec, PositiveSpectralObject)
    assert spec.dim == 4
    assert np.all(spec.spectrum >= -1e-10)
    print(f"  Spectral 对象维数: {spec.dim}")
    print("  通过")


def test_spectral_correspondence():
    print("\n[测试 4] 谱对应 λ_i = exp(-μ_i)")
    a_s = AsymptoticSafetyInstance(n_couplings=6)
    summary = a_s.summary()

    mu = np.array(summary["spectral_operator_eigenvalues"])
    lambdas = np.array(summary["koopman_eigenvalues"])
    lambdas_from_exp = np.sort(np.exp(-mu))
    lambdas_sorted = np.sort(lambdas)

    diff = np.linalg.norm(lambdas_sorted - lambdas_from_exp)
    print(f"  差异 (Frobenius): {diff:.2e}")
    assert diff < 1e-10
    print("  通过")


def test_critical_exponents_nonnegative():
    print("\n[测试 5] 临界指数非负")
    a_s = AsymptoticSafetyInstance(n_couplings=5)
    exponents = a_s.critical_exponent_spectrum()

    assert np.all(exponents >= 0)
    print(f"  临界指数: {exponents}")
    print("  通过")


def test_custom_critical_exponents():
    print("\n[测试 6] 自定义临界指数")
    custom = [0.5, 1.2, 2.3, 0.8]
    a_s = AsymptoticSafetyInstance(critical_exponents=custom)

    assert np.allclose(a_s.critical_exponent_spectrum(), np.array(custom))
    assert a_s.n_couplings == 4
    print(f"  自定义临界指数: {a_s.critical_exponent_spectrum()}")
    print("  通过")


def test_parameter_validation():
    print("\n[测试 7] 参数校验")
    try:
        AsymptoticSafetyInstance(n_couplings=0)
        assert False, "n_couplings=0 应抛出 ValueError"
    except ValueError:
        print("  n_couplings=0 正确抛出 ValueError")

    try:
        AsymptoticSafetyInstance(critical_exponents=[1.0, -0.5])
        assert False, "负临界指数应抛出 ValueError"
    except ValueError:
        print("  负临界指数正确抛出 ValueError")
    print("  通过")


def main():
    print("=" * 60)
    print("渐近安全实例接口测试")
    print("=" * 60)

    test_as_creation()
    test_rec_object_interface()
    test_spectral_object_interface()
    test_spectral_correspondence()
    test_critical_exponents_nonnegative()
    test_custom_critical_exponents()
    test_parameter_validation()

    print("\n" + "=" * 60)
    print("所有测试通过。")
    print("=" * 60)


if __name__ == "__main__":
    main()
