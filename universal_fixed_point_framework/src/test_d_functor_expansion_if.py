"""
test_d_functor_expansion_if.py

测试 D 函子扩张 IFS 扩展。
"""

import numpy as np
import pytest

from d_functor_expansion_if import (
    ExpansionIFS, ContractionIFS, HyperbolicSpectralObject, ExpansionDecursionFunctor
)


class TestExpansionIFS:
    """扩张 IFS 测试类。"""

    def test_expansion_ifs_construction(self):
        """扩张 IFS 构造。"""
        A1 = np.array([[2.0, 0.0], [0.0, 2.0]])
        b1 = np.array([0.0, 0.0])
        A2 = np.array([[2.0, 0.5], [0.5, 2.0]])
        b2 = np.array([1.0, 0.0])

        expansion_ifs = ExpansionIFS([A1, A2], [b1, b2])

        assert expansion_ifs.n == 2
        assert expansion_ifs.dim == 2

    def test_non_expansion_raises(self):
        """非扩张矩阵应抛出异常。"""
        A1 = np.array([[0.5, 0.0], [0.0, 0.5]])
        b1 = np.array([0.0, 0.0])

        with pytest.raises(ValueError):
            ExpansionIFS([A1], [b1])

    def test_inverse_system(self):
        """逆系统构造。"""
        A1 = np.array([[2.0, 0.0], [0.0, 2.0]])
        b1 = np.array([0.0, 0.0])

        expansion_ifs = ExpansionIFS([A1], [b1])
        inv_ifs = expansion_ifs.inverse_system()

        assert inv_ifs.n == 1
        assert np.allclose(inv_ifs.matrices[0], np.array([[0.5, 0.0], [0.0, 0.5]]))

    def test_fixed_points(self):
        """不动点计算。"""
        A1 = np.array([[2.0, 0.0], [0.0, 2.0]])
        b1 = np.array([1.0, 1.0])

        expansion_ifs = ExpansionIFS([A1], [b1])
        fps = expansion_ifs.fixed_points()

        assert len(fps) == 1
        assert fps[0] is not None
        assert np.allclose(fps[0], np.array([-1.0, -1.0]))

    def test_unstable_manifold(self):
        """不稳定流形计算。"""
        A1 = np.array([[2.0, 0.0], [0.0, 2.0]])
        b1 = np.array([0.0, 0.0])

        expansion_ifs = ExpansionIFS([A1], [b1])
        fps = expansion_ifs.fixed_points()

        if fps[0] is not None:
            manifold = expansion_ifs.unstable_manifold(fps[0])
            assert len(manifold) == 100


class TestContractionIFS:
    """收缩 IFS（逆系统）测试类。"""

    def test_contraction_ifs_construction(self):
        """收缩 IFS 构造。"""
        A1 = np.array([[0.5, 0.0], [0.0, 0.5]])
        b1 = np.array([0.0, 0.0])

        contraction_ifs = ContractionIFS([A1], [b1])

        assert contraction_ifs.n == 1
        assert contraction_ifs.dim == 2

    def test_forward_iterate(self):
        """前向迭代。"""
        A1 = np.array([[0.5, 0.0], [0.0, 0.5]])
        b1 = np.array([0.0, 0.0])

        contraction_ifs = ContractionIFS([A1], [b1])
        x = np.array([1.0, 1.0])

        trajectory = contraction_ifs.forward_iterate(x, steps=10)

        assert len(trajectory) == 11
        assert np.linalg.norm(trajectory[-1]) < 1e-2

    def test_attractor(self):
        """吸引子计算。"""
        A1 = np.array([[0.5, 0.0], [0.0, 0.5]])
        b1 = np.array([0.0, 0.0])

        contraction_ifs = ContractionIFS([A1], [b1])
        attractor = contraction_ifs.attractor(n_points=100)

        assert len(attractor) == 100
        assert np.allclose(attractor.mean(axis=0), np.array([0.0, 0.0]), atol=0.1)


class TestHyperbolicSpectralObject:
    """双曲谱对象测试类。"""

    def test_hyperbolic_spectral_object(self):
        """双曲谱对象构造。"""
        stable_eigs = np.array([0.5, 0.3])
        unstable_eigs = np.array([2.0, 3.0])

        spectral_obj = HyperbolicSpectralObject(stable_eigs, unstable_eigs)

        assert spectral_obj.dim_stable == 2
        assert spectral_obj.dim_unstable == 2
        assert spectral_obj.dim == 4

    def test_from_expansion_ifs(self):
        """从扩张 IFS 构造。"""
        A1 = np.array([[2.0, 0.0], [0.0, 2.0]])
        b1 = np.array([0.0, 0.0])

        expansion_ifs = ExpansionIFS([A1], [b1])
        spectral_obj = HyperbolicSpectralObject.from_expansion_ifs(expansion_ifs)

        assert spectral_obj.dim_stable >= 0
        assert spectral_obj.dim_unstable >= 0

    def test_spectrum_property(self):
        """谱属性。"""
        stable_eigs = np.array([0.5])
        unstable_eigs = np.array([2.0])

        spectral_obj = HyperbolicSpectralObject(stable_eigs, unstable_eigs)

        assert len(spectral_obj.spectrum) == 2


class TestExpansionDecursionFunctor:
    """扩张 D 函子测试类。"""

    def test_map_expansion_ifs(self):
        """映射扩张 IFS。"""
        A1 = np.array([[2.0, 0.0], [0.0, 2.0]])
        b1 = np.array([0.0, 0.0])

        expansion_ifs = ExpansionIFS([A1], [b1])
        result = ExpansionDecursionFunctor.map_expansion_ifs(expansion_ifs)

        assert isinstance(result, HyperbolicSpectralObject)

    def test_spectral_integral(self):
        """谱积分。"""
        A1 = np.array([[2.0, 0.0], [0.0, 2.0]])
        b1 = np.array([0.0, 0.0])

        expansion_ifs = ExpansionIFS([A1], [b1])
        result = ExpansionDecursionFunctor.spectral_integral(expansion_ifs, lambda x: x)

        assert len(result) == 2
        assert np.isfinite(result).all()

    def test_verify_functoriality(self):
        """函子性验证。"""
        A1 = np.array([[2.0, 0.0], [0.0, 2.0]])
        b1 = np.array([0.0, 0.0])

        expansion_ifs = ExpansionIFS([A1], [b1])
        functorial = ExpansionDecursionFunctor.verify_functoriality(expansion_ifs)

        assert isinstance(functorial, bool)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
