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
test_causal_set_instance.py

因果集实例的单元测试。
"""

import sys
from pathlib import Path
import numpy as np

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_SRC_DIR = _PROJECT_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from causal_set_instance import CausalSetInstance
from rec_category import RecObject
from spec_category import PositiveSpectralObject


def test_causal_set_creation():
    print("\n[测试 1] CausalSetInstance 创建与摘要")
    cs = CausalSetInstance(n_elements=10, seed=42)
    summary = cs.summary()

    assert "parameters" in summary
    assert "future_cardinalities" in summary
    assert len(summary["future_cardinalities"]) == 10
    print(f"  元素数: {cs.n_elements}, 因果关系数: {summary['causal_relations']}")
    print("  通过")


def test_rec_object_interface():
    print("\n[测试 2] Rec 对象接口")
    cs = CausalSetInstance(n_elements=10, seed=42)
    rec = cs.to_rec_object()

    assert isinstance(rec, RecObject)
    assert rec.n_points == 10
    assert rec.metadata["type"] == "causal_set"
    print(f"  Rec 对象维数: {rec.n_points}")
    print("  通过")


def test_spectral_object_interface():
    print("\n[测试 3] Spectral 对象接口")
    cs = CausalSetInstance(n_elements=10, seed=42)
    spec = cs.to_spectral_object()

    assert isinstance(spec, PositiveSpectralObject)
    assert spec.dim == 10
    assert np.all(spec.spectrum >= -1e-10)
    print(f"  Spectral 对象维数: {spec.dim}")
    print("  通过")


def test_spectral_correspondence():
    print("\n[测试 4] 谱对应 λ_i = exp(-μ_i)")
    cs = CausalSetInstance(n_elements=15, seed=123)
    summary = cs.summary()

    mu = np.array(summary["spectral_operator_eigenvalues"])
    lambdas = np.array(summary["koopman_eigenvalues"])
    lambdas_from_exp = np.sort(np.exp(-mu))
    lambdas_sorted = np.sort(lambdas)

    diff = np.linalg.norm(lambdas_sorted - lambdas_from_exp)
    print(f"  差异 (Frobenius): {diff:.2e}")
    assert diff < 1e-10
    print("  通过")


def test_future_cardinalities_nonnegative():
    print("\n[测试 5] 将来基数非负")
    cs = CausalSetInstance(n_elements=12, seed=7)
    cards = cs.future_cardinalities()

    assert np.all(cards >= 0)
    assert cards.dtype == float
    print(f"  将来基数范围: [{cards.min():.0f}, {cards.max():.0f}]")
    print("  通过")


def test_causal_matrix_upper_triangular():
    print("\n[测试 6] 因果矩阵严格上三角")
    cs = CausalSetInstance(n_elements=10, seed=99)
    C = cs.causal_matrix()

    assert np.all(np.diag(C) == 0)
    assert np.all(np.tril(C, k=-1) == 0)
    print(f"  非零元数: {np.count_nonzero(C)}")
    print("  通过")


def test_parameter_validation():
    print("\n[测试 7] 参数校验")
    try:
        CausalSetInstance(n_elements=1)
        assert False, "n_elements<2 应抛出 ValueError"
    except ValueError:
        print("  n_elements<2 正确抛出 ValueError")

    try:
        CausalSetInstance(spacetime_dimension=1)
        assert False, "spacetime_dimension<2 应抛出 ValueError"
    except ValueError:
        print("  spacetime_dimension<2 正确抛出 ValueError")
    print("  通过")


def main():
    print("=" * 60)
    print("因果集实例接口测试")
    print("=" * 60)

    test_causal_set_creation()
    test_rec_object_interface()
    test_spectral_object_interface()
    test_spectral_correspondence()
    test_future_cardinalities_nonnegative()
    test_causal_matrix_upper_triangular()
    test_parameter_validation()

    print("\n" + "=" * 60)
    print("所有测试通过。")
    print("=" * 60)


if __name__ == "__main__":
    main()
