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
from spectral_silence_compactification import (
    CompactificationParameters,
    KKModeSpectrum,
    CompactificationSilenceChecker,
    CompactificationSilenceEquivalence,
    CompactificationNumericalVerification
)


class TestCompactificationParameters:
    def test_creation(self):
        params = CompactificationParameters(
            radius=1e-15,
            extra_dimensions=6,
            topology="torus"
        )
        assert params.radius == 1e-15
        assert params.extra_dimensions == 6
        assert params.topology == "torus"


class TestKKModeSpectrum:
    def test_creation(self):
        params = CompactificationParameters(radius=1e-15, extra_dimensions=6)
        kk = KKModeSpectrum(params)
        assert kk.R == 1e-15
        assert kk.d == 6

    def test_torus_kk_masses(self):
        params = CompactificationParameters(radius=1e-15, extra_dimensions=6)
        kk = KKModeSpectrum(params)
        masses = kk.kk_masses(max_n=10)
        assert isinstance(masses, np.ndarray)
        assert len(masses) == 60
        assert all(m > 0 for m in masses)

    def test_cy_kk_masses(self):
        params = CompactificationParameters(radius=1e-15, extra_dimensions=6, topology="calabi-yau")
        kk = KKModeSpectrum(params)
        masses = kk.kk_masses(max_n=10)
        assert isinstance(masses, np.ndarray)
        assert len(masses) == 60

    def test_spectral_density(self):
        params = CompactificationParameters(radius=1e-15, extra_dimensions=6)
        kk = KKModeSpectrum(params)
        density = kk.spectral_density(1e15)
        assert isinstance(density, float)

    def test_continuous_approximation(self):
        params = CompactificationParameters(radius=1e-15, extra_dimensions=6)
        kk = KKModeSpectrum(params)
        result = kk.continuous_approximation(1e12)
        assert isinstance(result, bool)


class TestCompactificationSilenceChecker:
    def test_creation(self):
        params = CompactificationParameters(radius=1e-15, extra_dimensions=6)
        kk = KKModeSpectrum(params)
        checker = CompactificationSilenceChecker(kk)
        assert checker is not None

    def test_check_S1(self):
        params = CompactificationParameters(radius=1e-15, extra_dimensions=6)
        kk = KKModeSpectrum(params)
        checker = CompactificationSilenceChecker(kk)
        result = checker.check_S1_continuous(1e12)
        assert isinstance(result, bool)

    def test_check_S2(self):
        params = CompactificationParameters(radius=1e-15, extra_dimensions=6)
        kk = KKModeSpectrum(params)
        checker = CompactificationSilenceChecker(kk)
        result = checker.check_S2_measure_zero(1e12)
        assert isinstance(result, bool)

    def test_check_S3(self):
        params = CompactificationParameters(radius=1e-15, extra_dimensions=6)
        kk = KKModeSpectrum(params)
        checker = CompactificationSilenceChecker(kk)
        result = checker.check_S3_laci(1e12)
        assert isinstance(result, bool)

    def test_check_S4(self):
        params = CompactificationParameters(radius=1e-15, extra_dimensions=6)
        kk = KKModeSpectrum(params)
        checker = CompactificationSilenceChecker(kk)
        result = checker.check_S4_orbit_weight()
        assert result is True

    def test_silence_degree(self):
        params = CompactificationParameters(radius=1e-15, extra_dimensions=6)
        kk = KKModeSpectrum(params)
        checker = CompactificationSilenceChecker(kk)
        degree = checker.silence_degree(1e12)
        assert isinstance(degree, float)
        assert 0 <= degree <= 1

    def test_is_spectral_silence(self):
        params = CompactificationParameters(radius=1e-15, extra_dimensions=6)
        kk = KKModeSpectrum(params)
        checker = CompactificationSilenceChecker(kk)
        result = checker.is_spectral_silence(1e12)
        assert isinstance(result, bool)


class TestCompactificationSilenceEquivalence:
    def test_creation(self):
        equiv = CompactificationSilenceEquivalence()
        assert equiv is not None

    def test_theorem(self):
        equiv = CompactificationSilenceEquivalence()
        result = equiv.theorem_finite_radius_equivalence()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_critical_radius(self):
        equiv = CompactificationSilenceEquivalence()
        R_c = equiv.critical_radius(1e12, 6)
        assert isinstance(R_c, float)
        assert R_c > 0

    def test_error_estimate(self):
        equiv = CompactificationSilenceEquivalence()
        delta = equiv.error_estimate(1e-15, 1e12)
        assert isinstance(delta, float)
        assert 0 <= delta <= 1

    def test_observability_threshold(self):
        equiv = CompactificationSilenceEquivalence()
        threshold = equiv.observability_threshold(1e-15, 1e12)
        assert isinstance(threshold, float)


class TestCompactificationNumericalVerification:
    def test_creation(self):
        verifier = CompactificationNumericalVerification()
        assert verifier is not None

    def test_verify_torus(self):
        verifier = CompactificationNumericalVerification()
        radii = [1e-16, 1e-15, 1e-14]
        result = verifier.verify_torus_compactification(radii, 1e12)
        assert isinstance(result, dict)
        assert "results" in result
        assert len(result["results"]) == 3

    def test_verify_cy(self):
        verifier = CompactificationNumericalVerification()
        radii = [1e-16, 1e-15]
        result = verifier.verify_cy_compactification(radii, 1e12)
        assert isinstance(result, dict)
        assert "topology" in result
        assert result["topology"] == "calabi-yau"

    def test_phase_diagram(self):
        verifier = CompactificationNumericalVerification()
        energy_scales = [1e11, 1e12, 1e13]
        radii = [1e-16, 1e-15, 1e-14]
        diagram = verifier.phase_diagram(energy_scales, radii)
        assert isinstance(diagram, np.ndarray)
        assert diagram.shape == (3, 3)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])