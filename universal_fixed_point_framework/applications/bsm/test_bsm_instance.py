"""
test_bsm_instance.py

BSM 新费米子实例的单元测试。
"""

import sys
from pathlib import Path
import numpy as np

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_SRC_DIR = _PROJECT_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from bsm_instance import BSMInstance
from rec_category import RecObject
from spec_category import PositiveSpectralObject
import bsm_experiment_constraints as constraints
import bsm_cross_sections as xs


def test_bsm_instance_creation():
    print("\n[测试 1] BSMInstance 创建与摘要")
    bsm = BSMInstance(bsm_charge=2.0, n_generations=3)
    summary = bsm.summary()

    assert "parameters" in summary
    assert "bsm_masses_MeV" in summary
    assert len(summary["bsm_masses_MeV"]) == 3
    print(f"  BSM 质量数: {len(summary['bsm_masses_MeV'])}")
    print("  通过")


def test_rec_object_interface():
    print("\n[测试 2] Rec 对象接口")
    bsm = BSMInstance(bsm_charge=2.0)
    rec = bsm.to_rec_object()

    assert isinstance(rec, RecObject)
    assert rec.n_points == 2
    assert rec.metadata["type"] == "BSM_IFS"
    print(f"  Rec 对象维数: {rec.n_points}")
    print("  通过")


def test_spectral_object_interface():
    print("\n[测试 3] Spectral 对象接口")
    bsm = BSMInstance(bsm_charge=2.0, n_generations=3)
    spec = bsm.to_spectral_object()

    assert isinstance(spec, PositiveSpectralObject)
    assert spec.dim == 3
    assert np.all(spec.spectrum >= -1e-10)
    print(f"  Spectral 对象维数: {spec.dim}")
    print("  通过")


def test_bsm_charge_variation():
    print("\n[测试 4] 不同 BSM 荷产生不同质量谱")
    bsm1 = BSMInstance(bsm_charge=1.0)
    bsm2 = BSMInstance(bsm_charge=3.0)

    m1 = list(bsm1.bsm_masses().values())
    m2 = list(bsm2.bsm_masses().values())

    print(f"  charge=1: {np.round(m1, 2)}")
    print(f"  charge=3: {np.round(m2, 2)}")
    assert not np.allclose(m1, m2)
    print("  通过")


def test_mass_ordering():
    print("\n[测试 5] BSM 质量递增顺序")
    bsm = BSMInstance(bsm_charge=2.0, n_generations=3)
    masses = list(bsm.bsm_masses().values())

    assert np.all(np.diff(masses) > 0)
    print(f"  BSM 质量: {np.round(masses, 2)}")
    print("  通过")


def test_experimental_constraints_structure():
    print("\n[测试 6] 实验约束接口结构")
    bsm = BSMInstance(bsm_charge=2.0, n_generations=3)
    ec = bsm.experimental_constraints()

    assert "lhc" in ec
    assert "relic_density" in ec
    assert "direct_detection" in ec
    assert "overall_pass" in ec
    assert isinstance(ec["overall_pass"], bool)
    print(f"  整体通过: {ec['overall_pass']}")
    print("  通过")


def test_lhc_constraint_pass_and_fail():
    print("\n[测试 7] LHC 直接搜寻约束")
    below_limit = {"VLF": 500_000.0}   # 0.5 TeV，应失败
    above_limit = {"VLF": 2_000_000.0} # 2.0 TeV，应通过

    res_below = constraints.lhc_vector_like_fermion_constraint(below_limit)
    res_above = constraints.lhc_vector_like_fermion_constraint(above_limit)

    assert not res_below["overall_pass"]
    assert res_above["overall_pass"]
    print("  0.5 TeV 排除，2.0 TeV 通过")
    print("  通过")


def test_relic_density_constraint():
    print("\n[测试 8] 暗物质遗迹密度约束")
    # 1 TeV、耦合=1 时 toy 截面恰好等于热遗迹截面
    res = constraints.relic_density_constraint(1_000_000.0, coupling=1.0)
    assert res["pass"]

    # 10 TeV、耦合=1 时截面过小，应失败
    res2 = constraints.relic_density_constraint(10_000_000.0, coupling=1.0)
    assert not res2["pass"]
    print(f"  1 TeV pass={res['pass']}, 10 TeV pass={res2['pass']}")
    print("  通过")


def test_direct_detection_constraint():
    print("\n[测试 9] 暗物质直接探测约束")
    # 300 GeV 时 toy σ_SI（coupling=1）低于 XENON1T/LZ 型上限
    res = constraints.direct_detection_constraint(300_000.0, coupling=1.0)
    assert res["pass"]

    # 人为给出极高的 σ_SI，应失败
    res2 = constraints.direct_detection_constraint(
        300_000.0,
        spin_independent_cross_section_cm2=1e-40,
    )
    assert not res2["pass"]
    print(f"  toy 截面 pass={res['pass']}, 1e-40 cm² pass={res2['pass']}")
    print("  通过")


def test_thermal_relic_cross_section():
    print("\n[测试 10] 热遗迹密度近似")
    # 1 TeV、coupling=1 时 canonical 截面使 Ωh² 接近 Planck 值，应通过
    res_1tev = xs.thermal_relic_density(1_000_000.0, coupling=1.0)
    assert res_1tev["pass"]

    # 极重粒子截面过小，导致 Ωh² 远离 0.12，应失败
    res_heavy = xs.thermal_relic_density(10_000_000.0, coupling=1.0)
    assert not res_heavy["pass"]

    print(f"  1 TeV: Ωh²={res_1tev['Omega_h2']:.3f}, pass={res_1tev['pass']}")
    print(f"  10 TeV: Ωh²={res_heavy['Omega_h2']:.3f}, pass={res_heavy['pass']}")
    print("  通过")


def test_lhc_pair_production_cross_section():
    print("\n[测试 11] LHC 对产生截面质量依赖")
    m1, m2, m3 = 1_000_000.0, 2_000_000.0, 5_000_000.0
    s1 = xs.lhc_pair_production_cross_section(m1)
    s2 = xs.lhc_pair_production_cross_section(m2)
    s3 = xs.lhc_pair_production_cross_section(m3)

    assert np.isfinite(s1) and np.isfinite(s2) and np.isfinite(s3)
    assert s1 > s2 > s3 > 0.0
    print(f"  1 TeV: {s1:.3f} pb")
    print(f"  2 TeV: {s2:.3f} pb")
    print(f"  5 TeV: {s3:.3f} pb")
    print("  通过")


def test_direct_detection_si_cross_section():
    print("\n[测试 12] 直接探测自旋无关截面")
    sigma_si = xs.direct_detection_si_cross_section(100_000.0, coupling=1.0)
    assert np.isfinite(sigma_si)
    assert sigma_si > 0.0
    print(f"  100 GeV σ_SI = {sigma_si:.3e} cm²")
    print("  通过")


def test_bsm_instance_cross_sections():
    print("\n[测试 13] BSMInstance.cross_sections() 接口")
    bsm = BSMInstance(bsm_charge=2.0, n_generations=3)
    cs = bsm.cross_sections()

    expected_keys = {
        "mass_MeV",
        "mass_GeV",
        "thermal_relic_density",
        "lhc_pair_production",
        "direct_detection_si",
    }
    assert expected_keys.issubset(cs.keys())
    assert cs["thermal_relic_density"]["pass"] in (True, False)
    assert np.isfinite(cs["lhc_pair_production"])
    print(f"  最轻质量: {cs['mass_GeV']:.1f} GeV")
    print(f"  截面键: {list(cs.keys())}")
    print("  通过")


def main():
    print("=" * 60)
    print("BSM 新费米子实例接口测试")
    print("=" * 60)

    test_bsm_instance_creation()
    test_rec_object_interface()
    test_spectral_object_interface()
    test_bsm_charge_variation()
    test_mass_ordering()
    test_experimental_constraints_structure()
    test_lhc_constraint_pass_and_fail()
    test_relic_density_constraint()
    test_direct_detection_constraint()
    test_thermal_relic_cross_section()
    test_lhc_pair_production_cross_section()
    test_direct_detection_si_cross_section()
    test_bsm_instance_cross_sections()

    print("\n" + "=" * 60)
    print("所有测试通过。")
    print("=" * 60)


if __name__ == "__main__":
    main()
