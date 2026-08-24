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
test_string_instance.py

弦论实例的单元测试。
"""

import sys
from pathlib import Path
import numpy as np

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_SRC_DIR = _PROJECT_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from string_instance import StringInstance
import string_scattering_amplitude as scatt
from rec_category import RecObject
from spec_category import PositiveSpectralObject


def test_string_instance_creation():
    print("\n[测试 1] StringInstance 创建与摘要")
    st = StringInstance(n_modes=8)
    summary = st.summary()

    assert "parameters" in summary
    assert "mass_squared" in summary
    assert len(summary["mass_squared"]) == 8
    print(f"  模式数: {len(summary['mass_squared'])}")
    print("  通过")


def test_rec_object_interface():
    print("\n[测试 2] Rec 对象接口")
    st = StringInstance(n_modes=8)
    rec = st.to_rec_object()

    assert isinstance(rec, RecObject)
    assert rec.n_points == 8
    assert rec.metadata["type"] == "string_modes"
    print(f"  Rec 对象维数: {rec.n_points}")
    print("  通过")


def test_spectral_object_interface():
    print("\n[测试 3] Spectral 对象接口")
    st = StringInstance(n_modes=8)
    spec = st.to_spectral_object()

    assert isinstance(spec, PositiveSpectralObject)
    assert spec.dim == 8
    assert np.all(spec.spectrum >= -1e-10)
    print(f"  Spectral 对象维数: {spec.dim}")
    print("  通过")


def test_spectral_correspondence():
    print("\n[测试 4] 谱对应 λ_i = exp(-μ_i)")
    st = StringInstance(n_modes=12)
    summary = st.summary()

    mu = np.array(summary["spectral_operator_eigenvalues"])
    lambdas = np.array(summary["koopman_eigenvalues"])
    lambdas_from_exp = np.sort(np.exp(-mu))
    lambdas_sorted = np.sort(lambdas)

    diff = np.linalg.norm(lambdas_sorted - lambdas_from_exp)
    print(f"  差异 (Frobenius): {diff:.2e}")
    assert diff < 1e-10
    print("  通过")


def test_regge_trajectory():
    print("\n[测试 5] Regge 轨迹线性增长")
    st = StringInstance(n_modes=5)
    masses2 = st.regge_spectrum()

    expected = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
    assert np.allclose(masses2, expected)
    print(f"  m^2: {masses2}")
    print("  通过")


def test_open_scattering_amplitude():
    print("\n[测试 6] 开弦 Veneziano 振幅")
    st = StringInstance(n_modes=6, string_type="open")
    s, t = 0.3, 0.5
    amp = st.scattering_amplitude(s, t)

    assert np.isfinite(amp)
    assert isinstance(amp, (float, np.floating))
    print(f"  A_open({s}, {t}) = {amp:.4f}")
    print("  通过")


def test_closed_scattering_amplitude():
    print("\n[测试 7] 闭弦 Virasoro-Shapiro 振幅")
    st = StringInstance(n_modes=6, string_type="closed")
    s, t = 1.0, 1.0
    amp = st.scattering_amplitude(s, t)

    assert np.isfinite(amp)
    assert isinstance(amp, (float, np.floating))
    print(f"  A_closed({s}, {t}) = {amp:.4f}")
    print("  通过")


def test_scattering_poles_match_regge():
    print("\n[测试 8] 散射极点与 Regge 谱一致")
    for string_type in ("open", "closed"):
        st = StringInstance(n_modes=8, string_type=string_type)
        poles = st.scattering_pole_masses()
        regge = st.regge_spectrum()

        assert len(poles) == len(regge) == st.n_modes
        assert np.allclose(poles, regge, atol=1e-12)
        print(f"  {string_type}: 极点-谱最大差异 {np.max(np.abs(poles - regge)):.2e}")
    print("  通过")


def test_pole_positions_from_amplitude_module():
    print("\n[测试 9] 振幅模块极点位置")
    open_poles = scatt.physical_pole_masses_squared(alpha_prime=1.0, string_type="open", n_modes=5)
    closed_poles = scatt.physical_pole_masses_squared(alpha_prime=1.0, string_type="closed", n_modes=5)

    expected_open = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
    expected_closed = 4.0 * expected_open

    assert np.allclose(open_poles, expected_open)
    assert np.allclose(closed_poles, expected_closed)
    print(f"  open poles : {open_poles}")
    print(f"  closed poles: {closed_poles}")
    print("  通过")


def test_string_type_validation():
    print("\n[测试 10] string_type 参数校验")
    try:
        StringInstance(n_modes=4, string_type="bosonic")
        assert False, "非法 string_type 应抛出 ValueError"
    except ValueError:
        print("  非法类型正确抛出 ValueError")
    print("  通过")


def main():
    print("=" * 60)
    print("弦论实例接口测试")
    print("=" * 60)

    test_string_instance_creation()
    test_rec_object_interface()
    test_spectral_object_interface()
    test_spectral_correspondence()
    test_regge_trajectory()
    test_open_scattering_amplitude()
    test_closed_scattering_amplitude()
    test_scattering_poles_match_regge()
    test_pole_positions_from_amplitude_module()
    test_string_type_validation()

    print("\n" + "=" * 60)
    print("所有测试通过。")
    print("=" * 60)


if __name__ == "__main__":
    main()
