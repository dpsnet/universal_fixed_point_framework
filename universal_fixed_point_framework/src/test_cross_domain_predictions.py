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
from cross_domain_predictions import (
    BSMNewPhysicsPredictor,
    KerrQNMCorrections,
    HolographicNewPredictions
)


class TestBSMNewPhysicsPredictor:
    def test_creation(self):
        predictor = BSMNewPhysicsPredictor()
        assert predictor.sm_masses["electron"] == 0.511e-3
        assert predictor.sm_masses["muon"] == 0.1057
        assert predictor.sm_masses["tau"] == 1.777

    def test_predict_fourth_generation(self):
        predictor = BSMNewPhysicsPredictor()
        result = predictor.predict_fourth_generation()
        assert isinstance(result, dict)
        assert "L4" in result
        assert "nu_L4" in result
        assert result["L4"] > 0
        assert result["nu_L4"] > 0

    def test_predict_extra_higgs(self):
        predictor = BSMNewPhysicsPredictor()
        result = predictor.predict_extra_higgs()
        assert isinstance(result, dict)
        assert "H_plus" in result
        assert "H_minus" in result
        assert "H_0" in result
        assert "A_0" in result
        assert result["H_plus"] == result["H_minus"]

    def test_predict_new_gauge_boson(self):
        predictor = BSMNewPhysicsPredictor()
        result = predictor.predict_new_gauge_boson()
        assert isinstance(result, dict)
        assert "Z_prime" in result
        assert "W_prime" in result
        assert "G" in result
        assert result["Z_prime"] > 0
        assert result["W_prime"] > 0
        assert result["G"] > 0

    def test_predict_dark_matter(self):
        predictor = BSMNewPhysicsPredictor()
        result = predictor.predict_dark_matter()
        assert isinstance(result, dict)
        assert "WIMP" in result
        assert "axion" in result
        assert "neutralino" in result
        assert "gravitino" in result
        assert result["WIMP"] > 0

    def test_compute_s_higgs_coupling(self):
        predictor = BSMNewPhysicsPredictor()
        result = predictor.compute_s_higgs_coupling()
        assert isinstance(result, dict)
        assert "lambda_standard" in result
        assert "lambda_correction" in result
        assert "lambda_effective" in result
        assert 0 < result["lambda_effective"] < 1


class TestKerrQNMCorrections:
    def test_creation(self):
        qnm = KerrQNMCorrections()
        assert qnm.G == 6.67e-11
        assert qnm.c == 3e8

    def test_standard_qnm(self):
        qnm = KerrQNMCorrections()
        result = qnm.standard_qnm(mass=10.0, spin=0.9, l=2, m=2, n=0)
        assert isinstance(result, complex)
        assert np.abs(result) > 0

    def test_curvature_correction(self):
        qnm = KerrQNMCorrections()
        result = qnm.curvature_correction(mass=10.0, spin=0.9, l=2, m=2, n=0)
        assert isinstance(result, complex)

    def test_corrected_qnm(self):
        qnm = KerrQNMCorrections()
        result = qnm.corrected_qnm(mass=10.0, spin=0.9, l=2, m=2, n=0)
        assert isinstance(result, complex)
        assert np.abs(result) > 0

    def test_compute_gravitational_wave_form(self):
        qnm = KerrQNMCorrections()
        time = np.linspace(0, 1, 100)
        result = qnm.compute_gravitational_wave_form(mass=10.0, spin=0.9, time=time)
        assert isinstance(result, np.ndarray)
        assert len(result) == 100


class TestHolographicNewPredictions:
    def test_creation(self):
        hp = HolographicNewPredictions()
        assert hp.N_c == 3
        assert hp.g_coupling == 1.0

    def test_predict_operator_dimension(self):
        hp = HolographicNewPredictions()
        result = hp.predict_operator_dimension(scaling_dimension=2.0, twist=2)
        assert isinstance(result, float)
        assert result > 0

    def test_predict_chaos_bound(self):
        hp = HolographicNewPredictions()
        result = hp.predict_chaos_bound()
        assert isinstance(result, float)
        assert result > 0

    def test_predict_cft_correlator(self):
        hp = HolographicNewPredictions()
        result = hp.predict_cft_correlator([2, 2, 2, 2])
        assert isinstance(result, float)
        assert result > 0

    def test_predict_cft_correlator_invalid(self):
        hp = HolographicNewPredictions()
        with pytest.raises(ValueError):
            hp.predict_cft_correlator([2, 2, 2])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])