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

import numpy as np
import pytest
from holographic_quantum_corrections import (
    HolographicEntanglementEntropy,
    BlackHoleEntropy,
    HolographicSpectralSilence,
    BES_TBA_Curvature_Correction
)


class TestHolographicEntanglementEntropy:
    def test_creation(self):
        he = HolographicEntanglementEntropy(newton_constant=1.0)
        assert he.G_N == 1.0

    def test_classical_area(self):
        he = HolographicEntanglementEntropy(newton_constant=1.0)
        area = 100.0
        result = he.classical_area(area)
        assert np.isclose(result, 25.0)

    def test_quantum_correction(self):
        he = HolographicEntanglementEntropy(newton_constant=1.0)
        area = 100.0
        curvature = np.array([[1.0, 0, 0, 0], [0, 1.0, 0, 0], [0, 0, -1.0, 0], [0, 0, 0, -1.0]])
        result = he.quantum_correction(curvature, area)
        assert isinstance(result, float)

    def test_full_entropy(self):
        he = HolographicEntanglementEntropy(newton_constant=1.0)
        area = 100.0
        curvature = np.array([[1.0, 0, 0, 0], [0, 1.0, 0, 0], [0, 0, -1.0, 0], [0, 0, 0, -1.0]])
        result = he.full_entropy(area, curvature)
        assert isinstance(result, float)
        assert result > 0


class TestBlackHoleEntropy:
    def test_creation(self):
        bh = BlackHoleEntropy(newton_constant=1.0)
        assert bh.G_N == 1.0

    def test_bekenstein_hawking(self):
        bh = BlackHoleEntropy(newton_constant=1.0)
        area = 16 * np.pi
        result = bh.bekenstein_hawking(area)
        assert np.isclose(result, 4 * np.pi)

    def test_curvature_correction(self):
        bh = BlackHoleEntropy(newton_constant=1.0)
        area = 16 * np.pi
        curvature = 0.01
        result = bh.curvature_correction(area, curvature)
        assert isinstance(result, float)

    def test_quantum_gravity_correction(self):
        bh = BlackHoleEntropy(newton_constant=1.0)
        area = 16 * np.pi
        result = bh.quantum_gravity_correction(area)
        assert isinstance(result, float)

    def test_full_entropy(self):
        bh = BlackHoleEntropy(newton_constant=1.0)
        area = 16 * np.pi
        curvature = 0.01
        result = bh.full_entropy(area, curvature)
        assert isinstance(result, float)
        assert result > 0


class TestHolographicSpectralSilence:
    def test_creation(self):
        hd = HolographicSpectralSilence()
        assert hd is not None

    def test_compute_silence_degree(self):
        hd = HolographicSpectralSilence()
        result = hd.compute_silence_degree(bulk_dim=5, boundary_dim=4, curvature_scale=1e-6)
        assert isinstance(result, float)
        assert 0 < result < 1

    def test_holographic_laci(self):
        hd = HolographicSpectralSilence()
        result = hd.holographic_laci(cft_central_charge=1.0, adS_radius=1.0)
        assert isinstance(result, float)

    def test_verify_spectral_silence(self):
        hd = HolographicSpectralSilence()
        cft = {"central_charge": 1.0, "dimension": 4}
        adS = {"radius": 1.0, "dimension": 5, "curvature": 1.0}
        result = hd.verify_spectral_silence(cft, adS)
        assert isinstance(result, dict)
        assert "silence_degree" in result
        assert "laci_index" in result
        assert "is_spectral_silence" in result


class TestBES_TBA_Curvature_Correction:
    def test_creation(self):
        bes = BES_TBA_Curvature_Correction()
        assert bes.N_c == 3
        assert bes.g_coupling == 1.0

    def test_standard_bes_energy(self):
        bes = BES_TBA_Curvature_Correction()
        lambda_ = 1.0
        result = bes.standard_bes_energy(lambda_)
        assert isinstance(result, float)
        assert result > 0

    def test_curvature_corrected_energy(self):
        bes = BES_TBA_Curvature_Correction()
        lambda_ = 1.0
        curvature = 0.01
        result = bes.curvature_corrected_energy(lambda_, curvature)
        assert isinstance(result, float)
        assert result > 0

    def test_compute_spectrum(self):
        bes = BES_TBA_Curvature_Correction()
        lambda_values = np.array([1.0, 2.0, 3.0])
        curvature = 0.01
        result = bes.compute_spectrum(lambda_values, curvature)
        assert isinstance(result, np.ndarray)
        assert len(result) == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])