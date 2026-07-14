"""
test_sm_instance.py

标准模型实例的单元测试：验证 SMInstance 符合抽象框架接口，
并能复现旧 sm_mass_complete_v5.py 的核心质量预测趋势。
"""

import sys
from pathlib import Path
import numpy as np

# 将项目 src 目录加入路径
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_SRC_DIR = _PROJECT_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from sm_instance import SMInstance
from rec_category import RecObject
from spec_category import PositiveSpectralObject
from attractor_distance import (
    diagnose_rec_object_from_instance,
    diagnose_spectral_object,
)


def test_sm_instance_creation():
    """测试 SMInstance 可以正常创建并计算摘要。"""
    print("\n[测试 1] SMInstance 创建与摘要")
    sm = SMInstance()
    summary = sm.summary()

    assert "parameters" in summary
    assert "sector_weights" in summary
    assert "fermion_masses_MeV" in summary
    assert len(summary["fermion_masses_MeV"]) == 9

    print(f"  扇区测度: {np.round(summary['sector_weights'], 4)}")
    print(f"  费米子质量数: {len(summary['fermion_masses_MeV'])}")
    print("  通过")


def test_rec_object_interface():
    """测试 to_rec_object 返回合法的 RecObject。"""
    print("\n[测试 2] Rec 对象接口")
    sm = SMInstance()
    rec = sm.to_rec_object()

    assert isinstance(rec, RecObject)
    assert rec.n_points == len(sm.ifs_c)
    assert rec.metadata["type"] == "SM_IFS"
    assert rec.metadata["clifford_signature"] == (1, 7)

    print(f"  Rec 对象维数: {rec.n_points}")
    print(f"  metadata: {rec.metadata}")
    print("  通过")


def test_spectral_object_interface():
    """测试 to_spectral_object 返回合法的 PositiveSpectralObject。"""
    print("\n[测试 3] Spectral 对象接口")
    sm = SMInstance()
    spec = sm.to_spectral_object()

    assert isinstance(spec, PositiveSpectralObject)
    assert spec.dim == 9  # 9 个费米子（不含中微子）
    assert np.all(spec.spectrum >= -1e-10)  # 正半定

    print(f"  Spectral 对象维数: {spec.dim}")
    print(f"  谱 σ(A): {np.round(spec.spectrum, 4)}")
    print("  通过")


def test_mass_prediction_trend():
    """测试质量预测符合 SM 的定性趋势：t > b > τ > c > s > μ > d > u > e。"""
    print("\n[测试 4] 质量预测定性趋势")
    sm = SMInstance()
    masses = sm.fermion_masses()

    expected_order = ["t", "b", "τ", "c", "s", "μ", "d", "u", "e"]
    actual_order = sorted(masses.keys(), key=lambda k: masses[k], reverse=True)

    print(f"  预测顺序: {actual_order}")
    print(f"  期望顺序: {expected_order}")
    assert actual_order == expected_order, "质量顺序与预期不符"
    print("  通过")


def test_top_anchor():
    """测试 top 质量被锚定到 SM 值。"""
    print("\n[测试 5] top 质量锚定")
    sm = SMInstance()
    masses = sm.fermion_masses()
    assert abs(masses["t"] - 173100.0) < 1e-3
    print(f"  m_t 预测 = {masses['t']:.6f} MeV")
    print("  通过")


def test_gauge_couplings():
    """测试规范耦合常数在合理范围内。"""
    print("\n[测试 6] 规范耦合常数")
    sm = SMInstance()
    g = sm.gauge_couplings_ew_scale()
    alpha = sm.gauge_alpha()

    print(f"  g₁ = {g['g1']:.4f}, α₁ = {alpha['g1']:.6f}")
    print(f"  g₂ = {g['g2']:.4f}, α₂ = {alpha['g2']:.6f}")
    print(f"  g₃ = {g['g3']:.4f}, α₃ = {alpha['g3']:.6f}")

    # 检查 g 是否在合理范围
    # g₁ = sqrt(4π/60) ≈ 0.46, g₂ = sqrt(4π/30) ≈ 0.65, g₃ = sqrt(4π/9) ≈ 1.18
    assert 0.4 < g["g1"] < 0.5
    assert 0.6 < g["g2"] < 0.7
    assert 1.1 < g["g3"] < 1.3
    print("  通过")


def test_higgs_sector():
    """测试 Higgs 扇区输出。"""
    print("\n[测试 7] Higgs 扇区")
    sm = SMInstance()
    lam = sm.higgs_quartic_coupling()
    m_h = sm.higgs_mass()

    print(f"  λ = {lam:.4f}, m_H = {m_h:.1f} MeV")

    assert lam > 0.0
    assert 100000 < m_h < 150000  # 100–150 GeV
    print("  通过")


def test_neutrino_masses():
    """测试中微子质量在合理范围且符合正常层级。"""
    print("\n[测试 8] 中微子质量（See-saw）")
    sm = SMInstance()
    nu = sm.neutrino_masses_eV()

    total_mass = sum(nu.values())
    print(f"  m(ν_e) = {nu['ν_e']:.6e} eV")
    print(f"  m(ν_μ) = {nu['ν_μ']:.6e} eV")
    print(f"  m(ν_τ) = {nu['ν_τ']:.6e} eV")
    print(f"  Σ m_ν = {total_mass:.6e} eV")

    # 正常层级：νe < νμ < ντ
    assert nu["ν_e"] < nu["ν_μ"] < nu["ν_τ"], "正常层级不成立"
    # Planck 2018 上限
    assert total_mass < 0.15, "中微子质量总和超出 Planck 上限"
    print("  通过")


def test_all_fermion_count():
    """测试全部 12 个费米子质量。"""
    print("\n[测试 9] 全部费米子（含中微子）")
    sm = SMInstance()
    all_m = sm.all_fermion_masses()

    assert len(all_m) == 12
    print(f"  费米子总数: {len(all_m)} (9 夸克/带电轻子 + 3 中微子)")
    print("  通过")


def test_spectral_object_with_neutrinos():
    """测试包含中微子的 Spectral 对象维数。"""
    print("\n[测试 10] 含中微子的 Spectral 对象")
    sm = SMInstance()
    spec = sm.to_spectral_object()

    # 注意：to_spectral_object 目前只用 fermion_masses（不含中微子），
    # 因此维数仍为 9。all_fermion_masses 包含中微子但尚未影响 spec。
    assert spec.dim == 9
    print(f"  Spectral 对象维数: {spec.dim}（中微子尚未计入 spec 构造）")
    print("  通过")


def test_laci_diagnosis():
    """测试 SM 实例的 Rec/Spec 对象均可计算 LACI 诊断。"""
    print("\n[测试 6] LACI 局部吸引子捕获诊断")
    sm = SMInstance()
    rec = sm.to_rec_object()
    spec = sm.to_spectral_object()

    rec_report = diagnose_rec_object_from_instance(rec)
    spec_report = diagnose_spectral_object(spec)

    for name, report in [("Rec", rec_report), ("Spec", spec_report)]:
        print(f"  {name}: LACI = {report['laci']:.4f}, risk = {report['risk_level']}")
        assert "laci" in report
        assert report["risk_level"] in {"low", "medium", "high"}

    print("  通过")


def test_fixed_point_sector_weights():
    """测试通过不动点方程求解的扇区测度与解析结果一致。"""
    print("\n[测试 7] 扇区测度的 Hutchinson 不动点求解")
    sm = SMInstance()
    direct = sm.compute_sector_weights()
    fixed_point = sm.solve_sector_weights_by_fixed_point()

    print(f"  直接计算: {np.round(direct, 6)}")
    print(f"  不动点解: {np.round(fixed_point, 6)}")
    assert np.allclose(direct, fixed_point, atol=1e-8), "不动点测度与解析结果不一致"
    print("  通过")


def test_fixed_point_masses():
    """测试通过不动点测度计算的质量谱与原结果一致。"""
    print("\n[测试 8] 基于不动点测度的质量谱")
    sm = SMInstance()
    direct = sm.fermion_masses()
    fp = sm.fermion_masses_from_fixed_point()

    for name in direct:
        print(f"  {name}: direct = {direct[name]:.4f}, fixed-point = {fp[name]:.4f}")
        assert np.isclose(direct[name], fp[name], rtol=1e-6)
    print("  通过")


def main():
    print("=" * 60)
    print("标准模型实例接口测试")
    print("=" * 60)

    test_sm_instance_creation()
    test_rec_object_interface()
    test_spectral_object_interface()
    test_mass_prediction_trend()
    test_top_anchor()
    test_gauge_couplings()
    test_higgs_sector()
    test_neutrino_masses()
    test_all_fermion_count()
    test_spectral_object_with_neutrinos()
    test_laci_diagnosis()
    test_fixed_point_sector_weights()
    test_fixed_point_masses()

    print("\n" + "=" * 60)
    print("所有测试通过。")
    print("=" * 60)


if __name__ == "__main__":
    main()
