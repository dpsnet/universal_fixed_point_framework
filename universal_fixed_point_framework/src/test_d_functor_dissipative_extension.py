"""
test_d_functor_dissipative_extension.py

Phase 15D-1: D 函子耗散扩展测试。

验证：
1. 非自伴算子伪谱理论
2. 耗散半群性质
3. D 函子耗散扩展映射
4. 广义伴随关系验证
5. Henon 映射耗散版本
"""

from __future__ import annotations

import numpy as np
import pytest

from d_functor_dissipative_extension import (
    NonSelfAdjointSpectralTheory,
    DissipativeSemigroup,
    DissipativeDecursionFunctor,
    HenonMapDissipative,
)


def test_non_self_adjoint_spectrum():
    """非自伴算子谱分解。"""
    op = np.array([[1, 2], [3, 4]], dtype=complex)
    nsa = NonSelfAdjointSpectralTheory(op)
    spec_info = nsa.spectrum_with_dissipation()

    assert len(spec_info["eigenvalues"]) == 2
    assert not spec_info["is_self_adjoint"]


def test_pseudospectrum():
    """伪谱计算。"""
    op = np.array([[0, 1], [-1, 0]], dtype=complex)
    nsa = NonSelfAdjointSpectralTheory(op)
    pseudospec = nsa.pseudospectrum(epsilon=0.1, n_points=30)

    assert len(pseudospec) > 0


def test_dissipative_semigroup():
    """耗散半群性质。"""
    generator = np.array([[-1, 0], [0, -2]])
    semigroup = DissipativeSemigroup(generator)

    assert semigroup.is_dissipative()
    assert semigroup.decay_rate() >= 0

    T = semigroup.semigroup(t=1.0)
    assert T.shape == (2, 2)


def test_long_time_behavior():
    """长时间行为分析。"""
    generator = np.array([[-0.5, 0], [0, -1.0]])
    semigroup = DissipativeSemigroup(generator)
    behavior = semigroup.long_time_behavior()

    assert behavior["asymptotic_state"] == "equilibrium"
    assert behavior["dominant_decay_rate"] > 0


def test_dissipative_decursion_functor():
    """D 函子耗散扩展映射。"""
    rec_op = np.array([[-0.8, 0.2], [0.3, -0.7]])
    d_functor = DissipativeDecursionFunctor()
    spec_obj = d_functor.dissipative_rec_to_spec(rec_op, dissipation_rate=0.1)

    assert spec_obj["dissipation_rate"] == 0.1
    assert spec_obj["semigroup_properties"]["is_dissipative"]


def test_spec_to_rec_inverse():
    """谱对象逆重构递归算子。"""
    rec_op = np.array([[0.8, 0.2], [0.3, 0.7]])
    d_functor = DissipativeDecursionFunctor()
    spec_obj = d_functor.dissipative_rec_to_spec(rec_op, dissipation_rate=0.1)
    rec_op_recovered = d_functor.spec_to_dissipative_rec(spec_obj)

    assert np.allclose(rec_op_recovered, rec_op)


def test_dissipative_adjoint():
    """广义伴随关系验证。"""
    rec_op = np.array([[0.8, 0.2], [0.3, 0.7]])
    d_functor = DissipativeDecursionFunctor()
    result = d_functor.verify_dissipative_adjoint(rec_op, dissipation_rate=0.1)

    assert result["valid"]
    assert result["forward_error"] < 1.0
    assert result["backward_error"] < 1.0


def test_henon_map_basic():
    """Henon 映射基本性质。"""
    henon = HenonMapDissipative(a=1.4, b=0.3, dissipation=0.01)

    J = henon.jacobian(0.0, 0.0)
    assert J.shape == (2, 2)

    lyap = henon.lyapunov_exponents(n_iter=1000)
    assert len(lyap) == 2


def test_henon_dissipation():
    """Henon 映射耗散性验证。"""
    henon = HenonMapDissipative(a=1.4, b=0.3, dissipation=0.05)
    lyap = henon.lyapunov_exponents(n_iter=10000)

    total_lyap = sum(lyap)
    assert total_lyap < 0, f"耗散系统总 Lyapunov 指数应为负，实际为 {total_lyap}"


def test_henon_operator():
    """Henon 映射算子离散化。"""
    henon = HenonMapDissipative(a=1.4, b=0.3, dissipation=0.01)
    op = henon.to_operator(n_grid=8)

    assert op.shape[0] == op.shape[1]
    assert op.shape[0] == 64


if __name__ == "__main__":
    print("=" * 60)
    print("Phase 15D-1: D 函子耗散扩展测试")
    print("=" * 60)

    test_non_self_adjoint_spectrum()
    print("  [1] 非自伴算子谱分解 ✓")
    test_pseudospectrum()
    print("  [2] 伪谱计算 ✓")
    test_dissipative_semigroup()
    print("  [3] 耗散半群性质 ✓")
    test_long_time_behavior()
    print("  [4] 长时间行为分析 ✓")
    test_dissipative_decursion_functor()
    print("  [5] D 函子耗散扩展 ✓")
    test_spec_to_rec_inverse()
    print("  [6] 逆重构验证 ✓")
    test_dissipative_adjoint()
    print("  [7] 广义伴随验证 ✓")
    test_henon_map_basic()
    print("  [8] Henon 映射基本性质 ✓")
    test_henon_dissipation()
    print("  [9] Henon 耗散性验证 ✓")
    test_henon_operator()
    print("  [10] Henon 算子离散化 ✓")

    print("\n" + "=" * 60)
    print("全部耗散扩展测试通过。")
    print("=" * 60)
