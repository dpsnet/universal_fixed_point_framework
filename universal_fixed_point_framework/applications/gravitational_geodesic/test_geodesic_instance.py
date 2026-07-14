"""
test_geodesic_instance.py

引力测地线实例的单元测试。
"""

import sys
from pathlib import Path
import numpy as np

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_SRC_DIR = _PROJECT_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from geodesic_instance import GeodesicInstance
from rec_category import RecObject
from spec_category import PositiveSpectralObject
import schwarzschild_geodesic_verification as schw
import kerr_geodesic_verification as kerr
import geodesic_integrator as gint
import kerr_geodesic_integrator as kgint


def test_geodesic_instance_creation():
    print("\n[测试 1] GeodesicInstance 创建与摘要")
    geo = GeodesicInstance(n_states=4)
    summary = geo.summary()

    assert "parameters" in summary
    assert "lyapunov_exponents" in summary
    assert len(summary["lyapunov_exponents"]) == 4
    print(f"  Lyapunov 指数: {np.round(summary['lyapunov_exponents'], 4)}")
    print("  通过")


def test_rec_object_interface():
    print("\n[测试 2] Rec 对象接口")
    geo = GeodesicInstance(n_states=4)
    rec = geo.to_rec_object()

    assert isinstance(rec, RecObject)
    assert rec.n_points == 4
    assert rec.metadata["type"] == "geodesic_deviation"
    print(f"  Rec 对象维数: {rec.n_points}")
    print("  通过")


def test_spectral_object_interface():
    print("\n[测试 3] Spectral 对象接口")
    geo = GeodesicInstance(n_states=4)
    spec = geo.to_spectral_object()

    assert isinstance(spec, PositiveSpectralObject)
    assert spec.dim == 4
    assert np.all(spec.spectrum >= -1e-10)
    print(f"  Spectral 对象维数: {spec.dim}")
    print("  通过")


def test_spectral_correspondence():
    print("\n[测试 4] 谱对应 λ_i = exp(-μ_i)")
    geo = GeodesicInstance(n_states=6)
    summary = geo.summary()

    mu = np.array(summary["spectral_operator_eigenvalues"])
    lambdas = np.array(summary["koopman_eigenvalues"])
    lambdas_from_exp = np.sort(np.exp(-mu))
    lambdas_sorted = np.sort(lambdas)

    diff = np.linalg.norm(lambdas_sorted - lambdas_from_exp)
    print(f"  差异 (Frobenius): {diff:.2e}")
    assert diff < 1e-10
    print("  通过")


def test_lyapunov_ordering():
    print("\n[测试 5] Lyapunov 指数排序")
    geo = GeodesicInstance(n_states=5)
    lyaps = geo.lyapunov_exponents()

    # 由于曲率耦合随方向增强，Lyapunov 指数应递增
    assert np.all(np.diff(np.sort(lyaps)) > 0)
    print(f"  Lyapunov 指数: {np.round(np.sort(lyaps), 4)}")
    print("  通过")


def test_schwarzschild_metric():
    print("\n[测试 6] Schwarzschild 真实度规模式")
    radii = [7.0, 8.0, 10.0, 15.0]
    geo = GeodesicInstance(metric="schwarzschild", radii=radii)
    summary = geo.summary()

    assert geo.n_states == 2 * len(radii)
    assert geo.metric == "schwarzschild"
    assert isinstance(geo.to_rec_object(), RecObject)
    assert isinstance(geo.to_spectral_object(), PositiveSpectralObject)

    expected = np.sort(schw.spectrum(radii))
    actual = np.sort(np.array(summary["lyapunov_exponents"]))
    assert np.allclose(actual, expected, atol=1e-12)
    print(f"  n_states: {geo.n_states}, 频率与解析公式一致")
    print("  通过")


def test_kerr_metric():
    print("\n[测试 7] Kerr 真实度规模式")
    radii = [6.0, 8.0, 10.0, 15.0]
    spin = 0.5
    geo = GeodesicInstance(metric="kerr", radii=radii, spin=spin)
    summary = geo.summary()

    assert geo.n_states == 2 * len(radii)
    assert geo.metric == "kerr"
    assert isinstance(geo.to_rec_object(), RecObject)
    assert isinstance(geo.to_spectral_object(), PositiveSpectralObject)

    expected = np.sort(kerr.spectrum(radii, spin))
    actual = np.sort(np.array(summary["lyapunov_exponents"]))
    assert np.allclose(actual, expected, atol=1e-12)
    print(f"  n_states: {geo.n_states}, spin={spin}, 频率与解析公式一致")
    print("  通过")


def test_real_metric_spectral_correspondence():
    print("\n[测试 8] 真实度规模式谱对应")
    for metric in ("schwarzschild", "kerr"):
        kwargs = {"metric": metric, "radii": [7.0, 10.0, 15.0]}
        if metric == "kerr":
            kwargs["spin"] = 0.3
        geo = GeodesicInstance(**kwargs)
        summary = geo.summary()

        mu = np.array(summary["spectral_operator_eigenvalues"])
        lambdas = np.array(summary["koopman_eigenvalues"])
        lambdas_from_exp = np.sort(np.exp(-mu))
        lambdas_sorted = np.sort(lambdas)

        diff = np.linalg.norm(lambdas_sorted - lambdas_from_exp)
        print(f"  {metric}: 差异 (Frobenius) = {diff:.2e}")
        assert diff < 1e-10
    print("  通过")


def test_schwarzschild_kerr_consistency_at_zero_spin():
    print("\n[测试 9] Kerr a=0 退化为 Schwarzschild")
    radii = [7.0, 8.0, 10.0, 15.0]
    geo_schw = GeodesicInstance(metric="schwarzschild", radii=radii)
    geo_kerr = GeodesicInstance(metric="kerr", radii=radii, spin=0.0)

    assert np.allclose(
        np.sort(geo_schw.lyapunov_exponents()),
        np.sort(geo_kerr.lyapunov_exponents()),
        atol=1e-12,
    )
    print("  a=0 时 Kerr 与 Schwarzschild 频率一致")
    print("  通过")


def test_metric_validation():
    print("\n[测试 10] 参数校验")
    try:
        GeodesicInstance(metric="reissner")
        assert False, "非法 metric 应抛出 ValueError"
    except ValueError:
        print("  非法 metric 正确抛出 ValueError")

    try:
        GeodesicInstance(metric="kerr", spin=1.5)
        assert False, "|a|>=1 应抛出 ValueError"
    except ValueError:
        print("  Kerr 自旋越界正确抛出 ValueError")

    try:
        GeodesicInstance(metric="schwarzschild", radii=[5.0])
        assert False, "r<6 应抛出 ValueError"
    except ValueError:
        print("  Schwarzschild 半径小于 ISCO 正确抛出 ValueError")
    print("  通过")


def test_numerical_validation():
    print("\n[测试 11] Schwarzschild 数值积分验证")
    radii = [8.0, 10.0, 15.0]
    geo = GeodesicInstance(metric="schwarzschild", radii=radii)
    validation = geo.numerical_validation(tolerance=5e-2)

    assert validation is not None
    assert "overall_pass" in validation
    assert validation["overall_pass"] is True
    print(f"  容差: {validation['tolerance']}, 整体通过: {validation['overall_pass']}")
    print("  通过")


def test_synthetic_numerical_validation_none():
    print("\n[测试 12] synthetic 模式 numerical_validation 返回 None")
    geo = GeodesicInstance(metric="synthetic", n_states=4)
    validation = geo.numerical_validation()

    assert validation is None
    print("  synthetic 模式正确返回 None")
    print("  通过")


def test_kerr_numerical_validation():
    print("\n[测试 13] Kerr 数值积分验证")
    radii = [8.0, 10.0, 15.0]
    geo = GeodesicInstance(metric="kerr", radii=radii, spin=0.5)
    validation = geo.numerical_validation(tolerance=5e-2)

    assert validation is not None
    assert "overall_pass" in validation
    assert validation["overall_pass"] is True
    print(f"  容差: {validation['tolerance']}, a={validation['a']}, 整体通过: {validation['overall_pass']}")
    print("  通过")


def test_kerr_a0_equals_schwarzschild():
    print("\n[测试 14] Kerr a=0 与 Schwarzschild 数值积分一致性")
    radii = [8.0, 10.0, 15.0]
    for r0 in radii:
        res_s = gint.radial_frequency_numerical(r0)
        res_k = kgint.radial_frequency_numerical(r0, a=0.0)
        ratio = res_k["Omega_r_numerical"] / res_s["Omega_r_numerical"]
        assert abs(1.0 - ratio) < 0.05, f"r0={r0}: ratio={ratio:.6f} > 5%"
        print(f"  r0={r0:.0f}: Schw={res_s['Omega_r_numerical']:.6f}, Kerr(a=0)={res_k['Omega_r_numerical']:.6f}, 差异={abs(1.0-ratio)*100:.2f}%")
    print("  通过")


def test_kerr_retrograde():
    print("\n[测试 15] Kerr 逆行数值积分 (a=0.5, e=0.05)")
    radii = [12.0, 15.0, 20.0]
    for r0 in radii:
        res = kgint.radial_frequency_numerical(r0, a=0.5, eccentricity=5e-2, prograde=False)
        passed = res["relative_error"] < 0.2
        print(f"  r0={r0:.0f}: Ω_r(数值)={res['Omega_r_numerical']:.6f}, Ω_r(解析)={res['Omega_r_analytic']:.6f}, 误差={res['relative_error']:.2%} {'通过' if passed else '失败'}")
        assert passed
    print("  通过")


def test_kerr_large_eccentricity():
    print("\n[测试 16] Kerr 大偏心率数值积分 (a=0.5, e=0.3)")
    radii = [8.0, 10.0]
    for r0 in radii:
        res = kgint.radial_frequency_numerical(r0, a=0.5, eccentricity=0.3, prograde=True)
        passed = res["relative_error"] < 0.3
        print(f"  r0={r0:.0f}: Ω_r(数值)={res['Omega_r_numerical']:.6f}, Ω_r(解析)={res['Omega_r_analytic']:.6f}, 误差={res['relative_error']:.2%} {'通过' if passed else '失败'}")
        assert passed
    print("  通过")


def test_kerr_lyapunov_integrable():
    print("\n[测试 17] Kerr 可积性验证：最大 Lyapunov 指数 ≈ 0")
    for r0 in [8.0, 10.0, 15.0]:
        lyap = kgint.maximum_lyapunov_exponent(r0, a=0.5, n_periods=10)
        assert abs(lyap["lambda_max"]) < 1e-10, f"r0={r0}: λ_max={lyap['lambda_max']:.2e} > 1e-10"
        print(f"  r0={r0:.0f}: λ_max = {lyap['lambda_max']:.2e}")
    print("  通过")


def test_kerr_non_equatorial():
    print("\n[测试 18] Kerr 非赤道面轨道 (Carter Q ≠ 0)")
    tau, states = kgint.integrate_non_equatorial_orbit(
        15.0, np.pi / 3.0, a=0.5, n_periods=3, steps_per_period=500
    )
    theta = states[:, 2]
    theta_range = theta.max() - theta.min()
    assert theta_range > 1e-4, f"极向振荡幅度过小: Δθ={theta_range:.6f}"
    assert theta.min() > 0, f"θ 进入负值: min(θ)={theta.min():.4f}"
    assert theta.max() < np.pi, f"θ 超过 π: max(θ)={theta.max():.4f}"
    print(f"  θ范围=[{theta.min():.4f}, {theta.max():.4f}], Δθ={theta_range:.4f}")
    print("  通过")


def test_non_equatorial_theta_degeneracy():
    print("\n[测试 19] 非赤道面 θ→π/2 退化至赤道面")
    tau_eq, states_eq = kgint.integrate_bound_orbit(15.0, a=0.5, n_periods=3)
    tau_ne, states_ne = kgint.integrate_non_equatorial_orbit(
        15.0, np.pi / 2.0 + 1e-4, a=0.5, n_periods=3
    )
    r_eq, r_ne = states_eq[:100, 0], states_ne[:100, 0]
    max_diff = np.max(np.abs(r_eq - r_ne))
    print(f"  赤道面 vs 准赤道面最大差异 = {max_diff:.6e}")
    assert max_diff < 0.1, f"退化失败: max_diff={max_diff:.2e}"
    print("  通过（r⁴ 近似下可接受）")


def test_lyapunov_diagnosis_geodesic_instance():
    print("\n[测试 20] GeodesicInstance.lyapunov_diagnosis 接口")
    for metric in ("schwarzschild", "kerr"):
        kwargs = {"metric": metric, "radii": [10.0]}
        if metric == "kerr":
            kwargs["spin"] = 0.5
        geo = GeodesicInstance(**kwargs)
        diag = geo.lyapunov_diagnosis(n_periods=10)
        assert "lambda_max" in diag
        assert "risk" in diag
        assert diag["metric"] == metric
        print(f"  {metric}: λ={diag['lambda_max']:.2e}, risk={diag['risk']}")
    synthetic = GeodesicInstance(metric="synthetic")
    diag_syn = synthetic.lyapunov_diagnosis()
    assert diag_syn["risk"] == "N/A"
    print(f"  synthetic: {diag_syn['interpretation']}")
    print("  通过")


def test_non_equatorial_prograde_retrograde():
    print("\n[测试 21] 非赤道面顺行 vs 逆行 (r⁴ 近似)")
    # 顺行
    tau_p, states_p = kgint.integrate_non_equatorial_orbit(
        15.0, np.pi / 3.0, a=0.5, prograde=True, n_periods=3
    )
    theta_p = states_p[:, 2]
    # 逆行
    tau_r, states_r = kgint.integrate_non_equatorial_orbit(
        15.0, np.pi / 3.0, a=0.5, prograde=False, n_periods=3
    )
    theta_r = states_r[:, 2]
    print(f"  顺行: Δθ={abs(theta_p.max()-theta_p.min()):.4f}")
    print(f"  逆行: Δθ={abs(theta_r.max()-theta_r.min()):.4f}")
    assert theta_p.min() > 0 and theta_r.min() > 0
    assert theta_p.max() < np.pi and theta_r.max() < np.pi
    print("  通过")


def test_non_equatorial_zero_eccentricity():
    print("\n[测试 22] 非赤道面 e=0 纯 θ 振荡")
    tau, states = kgint.integrate_non_equatorial_orbit(
        15.0, np.pi / 3.0, a=0.5, n_periods=5, steps_per_period=500
    )
    r, theta = states[:, 0], states[:, 2]
    theta_range = theta.max() - theta.min()
    print(f"  θ范围=[{theta.min():.4f}, {theta.max():.4f}], Δθ={theta_range:.4f}")
    assert theta.min() > 0, f"θ 进入负值: min(θ)={theta.min():.4f}"
    assert theta.max() < np.pi, f"θ 超过 π: max(θ)={theta.max():.4f}"
    assert theta_range > 0.1, f"极向振荡不足: Δθ={theta_range:.4f}"
    print("  通过")


def main():
    print("=" * 60)
    print("引力测地线实例接口测试")
    print("=" * 60)

    test_geodesic_instance_creation()
    test_rec_object_interface()
    test_spectral_object_interface()
    test_spectral_correspondence()
    test_lyapunov_ordering()
    test_schwarzschild_metric()
    test_kerr_metric()
    test_real_metric_spectral_correspondence()
    test_schwarzschild_kerr_consistency_at_zero_spin()
    test_metric_validation()
    test_numerical_validation()
    test_synthetic_numerical_validation_none()
    test_kerr_numerical_validation()
    test_kerr_a0_equals_schwarzschild()
    test_kerr_retrograde()
    test_kerr_large_eccentricity()
    test_kerr_lyapunov_integrable()
    test_kerr_non_equatorial()
    test_non_equatorial_theta_degeneracy()
    test_lyapunov_diagnosis_geodesic_instance()
    test_non_equatorial_prograde_retrograde()
    test_non_equatorial_zero_eccentricity()

    print("\n" + "=" * 60)
    print("所有测试通过。")
    print("=" * 60)


if __name__ == "__main__":
    main()
