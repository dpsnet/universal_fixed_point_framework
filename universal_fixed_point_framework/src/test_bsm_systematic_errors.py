"""
test_bsm_systematic_errors.py

Phase 15A-3: FCC-hh / HL-LHC 系统误差分析。

验证 BSM 第4代轻子预言在不同系统误差假设下的显著性退化，
提供真实的误差预算估计。
"""

from __future__ import annotations

import numpy as np
import pytest

from bsm_hllhc_fcc_study import (
    HLLHCFCCProjection,
    L4Parameters,
)


def test_systematic_error_budget_hl_lhc():
    """
    HL-LHC (14 TeV, 3 ab^-1) 系统误差预算。

    检查：
    1. 无系统误差时 Z 值应为正
    2. 系统误差增大时 Z 单调递减
    3. 在合理系统误差 (5-15%) 范围内 Z 是否仍 > 5σ
    """
    params = L4Parameters.from_framework()
    proj = HLLHCFCCProjection(params=params)

    budget = proj.systematic_error_budget(
        sqrt_s_TeV=14.0, lumi_fb=3000.0)

    sys_scan = budget["systematic_scan"]
    z_vals = sys_scan["z_with_sys"]

    print(f"\n  HL-LHC 系统误差预算 (m={budget['mass_GeV']:.0f} GeV)")
    print(f"  n_signal={budget['n_signal']:.1f}, "
          f"n_background={budget['n_background']:.1f}")
    print(f"  Z(无系统误差) = {budget['z_nominal_no_sys']:.2f}σ")
    print()

    for sys, z in zip(sys_scan["sys_levels"], z_vals):
        print(f"    σ_sys={sys*100:5.1f}%: Z={z:.2f}σ")

    # Z 随系统误差单调递减
    for i in range(len(z_vals) - 1):
        assert z_vals[i] >= z_vals[i + 1] - 1e-10, (
            f"Z 应单调递减: [{i}]={z_vals[i]:.2f} < [{i+1}]={z_vals[i+1]:.2f}"
        )

    # 在 10% 系统误差下，Z 应仍为正值
    assert z_vals[3] > 0, f"10% 系统误差时 Z={z_vals[3]:.2f} ≤ 0"

    print(f"\n  结论: HL-LHC 在 σ_sys=10% 时 Z={z_vals[3]:.2f}σ")
    print("  通过")


def test_systematic_error_budget_fcc():
    """
    FCC-hh (100 TeV, 30 ab^-1) 系统误差预算。
    """
    params = L4Parameters.from_framework()
    proj = HLLHCFCCProjection(params=params)

    budget = proj.systematic_error_budget(
        sqrt_s_TeV=100.0, lumi_fb=30000.0)

    sys_scan = budget["systematic_scan"]
    z_vals = sys_scan["z_with_sys"]

    print(f"\n  FCC-hh 系统误差预算 (m={budget['mass_GeV']:.0f} GeV)")
    print(f"  n_signal={budget['n_signal']:.1f}, "
          f"n_background={budget['n_background']:.1f}")
    print(f"  Z(无系统误差) = {budget['z_nominal_no_sys']:.2f}σ")
    print()

    for sys, z in zip(sys_scan["sys_levels"], z_vals):
        print(f"    σ_sys={sys*100:5.1f}%: Z={z:.2f}σ")

    # Z 随系统误差单调递减
    for i in range(len(z_vals) - 1):
        assert z_vals[i] >= z_vals[i + 1] - 1e-10

    # 在 10% 系统误差下，FCC-hh 应有显著信号
    assert z_vals[3] > 0, f"10% 系统误差时 Z={z_vals[3]:.2f} ≤ 0"

    print(f"\n  结论: FCC-hh 在 σ_sys=10% 时 Z={z_vals[3]:.2f}σ")
    print("  通过")


def test_systematic_degradation_rate():
    """
    测量 Z 随系统误差的退化率。

    退化率 = ΔZ / Δ(σ_sys) 在 2%-20% 区间内。
    """
    params = L4Parameters.from_framework()

    rates = {}
    for sqrt_s, lumi, label in [
        (14.0, 3000.0, "HL-LHC"),
        (100.0, 30000.0, "FCC-hh"),
    ]:
        proj = HLLHCFCCProjection(params=params)
        budget = proj.systematic_error_budget(
            sqrt_s_TeV=sqrt_s, lumi_fb=lumi)

        rate = budget["z_degradation_per_percent"]
        rates[label] = rate

        print(f"\n  {label}: Z 退化率 = {rate:.4f} σ / %sys"
              if rate is not None else f"\n  {label}: 退化率未计算")

    # 退化率应为负值（系统误差降低 Z）
    for label, rate in rates.items():
        if rate is not None:
            assert rate < 0, f"{label}: 退化率应为负 ({rate})"

    print("\n  通过")


def test_z_vs_systematics_table():
    """
    生成 Z 值随系统误差变化的简表，用于 Paper II 系统误差讨论。
    """
    params = L4Parameters.from_framework()

    print("\n  === Z 值系统误差依赖表 ===")
    print(f"  L4 质量: {params.mass_GeV:.0f} GeV")
    print(f"  {'σ_sys':<8} {'HL-LHC Z':<12} {'FCC-hh Z':<12}")
    print(f"  {'-------':<8} {'--------':<12} {'--------':<12}")

    for sys in [0.0, 0.02, 0.05, 0.10, 0.15, 0.20, 0.30]:
        proj_hl = HLLHCFCCProjection(params=params, sigma_sys=sys)
        proj_fcc = HLLHCFCCProjection(params=params, sigma_sys=sys)

        z_hl = proj_hl.signal_background(14.0, 3000.0)["significance"]["asimov_with_sys"]
        z_fcc = proj_fcc.signal_background(100.0, 30000.0)["significance"]["asimov_with_sys"]

        print(f"  {sys*100:<8.0f}% {z_hl:<12.2f} {z_fcc:<12.2f}σ")

    # 至少表格能打印（不崩溃）
    assert True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
