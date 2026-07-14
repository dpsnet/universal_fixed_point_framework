"""
test_bsm_oblique.py

验证 BSM 第四代轻子对电弱精密观测 S/T 参数的贡献。
"""

from __future__ import annotations

import numpy as np
import pytest

from bsm_oblique_parameters import (
    FourthGenFermionDoublet,
    mass_splitting_scan,
    exclusion_estimate,
)

# 理论预期值（Peskin-Takeuchi 公式）
DELTA_S_DEGENERATE = 1.0 / (6.0 * np.pi)  # ≈ 0.053


def test_delta_s_degenerate_limit():
    """简并双分量 (m_l4 = m_nu4) 的 ΔS 应恰好等于 1/(6π)。"""
    fg = FourthGenFermionDoublet(m_l4=1470.0, m_nu4=1470.0)
    ds = fg.delta_S()
    assert abs(ds - DELTA_S_DEGENERATE) < 1e-10, (
        f"ΔS = {ds:.6f}, expected {DELTA_S_DEGENERATE:.6f}"
    )


def test_delta_t_degenerate_limit():
    """简并双分量的 ΔT 应恰好等于 0（SU(2) 对称性保护）。"""
    fg = FourthGenFermionDoublet(m_l4=1470.0, m_nu4=1470.0)
    dt = fg.delta_T()
    assert abs(dt) < 1e-10, f"ΔT = {dt:.6e}, expected 0"


def test_delta_s_splitting_log_dependence():
    """质量分裂时 ΔS 应有对数依赖。"""
    fg1 = FourthGenFermionDoublet(m_l4=1470.0, m_nu4=1470.0)
    fg2 = FourthGenFermionDoublet(m_l4=1470.0, m_nu4=1000.0)
    ds1 = fg1.delta_S()
    ds2 = fg2.delta_S()

    # 质量分裂会改变 ΔS
    assert abs(ds1 - ds2) > 1e-6, "质量分裂应改变 ΔS"
    # ΔS 的变化应在合理范围
    assert abs(ds1 - ds2) < 1.0, "ΔS 变化过大"


def test_delta_t_splitting_positive():
    """质量分裂 (m_l4 > m_nu4) 应产生正 ΔT。"""
    fg = FourthGenFermionDoublet(m_l4=1470.0, m_nu4=1000.0)
    dt = fg.delta_T()
    assert dt > 0, f"质量分裂时应 ΔT > 0, 实际 ΔT = {dt:.6f}"


def test_mass_splitting_scan():
    """质量分裂扫描应单调递增（预设从低到高）。"""
    results = mass_splitting_scan()
    for i in range(len(results) - 1):
        assert results[i]["mass_ratio"] < results[i + 1]["mass_ratio"], (
            "质量比应单调递增"
        )


def test_framework_prediction_ew_constraint():
    """
    框架预言（m_L4=1470 GeV, m_nu4=1470 GeV 简并）对电弱精密约束的兼容性。
    """
    fg = FourthGenFermionDoublet()
    summary = fg.summary()

    print(f"\n  框架预言 ΔS = {summary['delta_S']:.4f}")
    print(f"  框架预言 ΔT = {summary['delta_T']:.4f}")
    print(f"  与 PDG 联合拟合偏差: χ² = {summary['chi2_total']:.2f}")

    status = exclusion_estimate(summary["delta_S"], summary["delta_T"])
    print(f"  电弱精密检验: {status}")

    # 简并双分量时 ΔT=0，与 PDG 约束无显著偏离
    # 该测试验证框架预言不被电弱精密数据排除
    assert summary["chi2_total"] < 10.0, (
        f"框架预言 χ² = {summary['chi2_total']:.1f} > 10"
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
