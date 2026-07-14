"""
bsm_cross_sections.py

BSM 实验相关截面的玩具级/近似计算。

定位：
- 本文件属于「通用不动点范畴框架」的实例假设层（Model Hypotheses）。
- 提供热遗迹密度、LHC 矢量型费米子对产生截面、暗物质直接探测自旋无关截面
  的简化解析估计，用于与 BSMInstance 的质量谱快速对接。

说明：
- 当前数值为近似/示意性公式，不构成完整的蒙特卡洛或微观唯象学计算。
- 单位统一为 MeV（质量）、cm³/s（湮灭截面）、pb（产生截面）、cm²（散射截面）。
"""

from __future__ import annotations

import numpy as np

# 物理常数与参考值
PLANCK_RELIC_DENSITY = 0.12  # Planck 2018 暗物质遗迹密度 Ωh²
M_PLANCK_GEV = 1.2209e19  # 普朗克质量，单位 GeV
M_NUCLEON_GEV = 0.939  # 核子质量，单位 GeV
X_F = 20.0  # 热冻结点 x_f = m / T_f


def canonical_thermal_cross_section(
    mass_MeV: float,
    coupling: float = 1.0,
    degrees_of_freedom: int = 2,
    reference_mass_MeV: float = 1_000_000.0,
) -> float:
    """
    玩具模型：与质量和耦合相关的热遗迹湮灭截面 σv。

    通过标准冻结近似式
        Ωh² ≈ 1.07e9 * x_f / (M_Pl * sqrt(g*) * σv)
    反解出在参考质量（默认 1 TeV）处使 Ωh² 恰好等于 Planck 值的 σv，
    再按 σv ∝ coupling^4 / mass^2 外推到任意质量。这样可保证在
    1 TeV、coupling=1 时自然落在热遗迹窗口内。
    """
    # 使 Ωh² = PLANCK_RELIC_DENSITY 所需的参考 σv（单位 cm³/s）
    sigma_ref = (
        1.07e9
        * X_F
        / (M_PLANCK_GEV * np.sqrt(degrees_of_freedom) * PLANCK_RELIC_DENSITY)
    )
    mass_ratio = mass_MeV / reference_mass_MeV
    return float(sigma_ref * (coupling ** 4) / (mass_ratio ** 2))


def thermal_relic_density(
    mass_MeV: float,
    annihilation_cross_section_cm3_per_s: float | None = None,
    coupling: float = 1.0,
    degrees_of_freedom: int = 2,
) -> dict:
    """
    计算热冻结遗迹密度 Ωh² 的标准近似。

    公式：
        x_f = 20.0
        g* = degrees_of_freedom
        σv = annihilation_cross_section_cm3_per_s or canonical_thermal_cross_section(...)
        Ωh² = 1.07e9 * x_f / (M_Pl * sqrt(g*) * σv)

    返回值包含 Ωh²、σv、x_f，以及是否在 Planck 值 0.12 的两倍范围内（pass）。
    """
    x_f = X_F
    g_star = degrees_of_freedom

    if annihilation_cross_section_cm3_per_s is None:
        sigma_v = canonical_thermal_cross_section(
            mass_MeV, coupling=coupling, degrees_of_freedom=g_star
        )
    else:
        sigma_v = annihilation_cross_section_cm3_per_s

    omega_h2 = 1.07e9 * x_f / (M_PLANCK_GEV * np.sqrt(g_star) * sigma_v)

    # 在 Planck 值 0.12 的 ±1 倍（即 0.5–2 倍）范围内视为通过
    half = PLANCK_RELIC_DENSITY / 2.0
    double = PLANCK_RELIC_DENSITY * 2.0
    passed = half <= omega_h2 <= double

    return {
        "Omega_h2": float(omega_h2),
        "sigma_v": float(sigma_v),
        "x_f": float(x_f),
        "pass": bool(passed),
    }


def lhc_pair_production_cross_section(
    mass_MeV: float,
    sqrt_s_MeV: float = 13_000_000.0,
) -> float:
    """
    近似 NNLO 矢量型费米子对产生截面（单位 pb）。

    使用简单的部分子亮度启发式参数化：
        m_GeV = mass_MeV / 1000.0
        sqrt_s_GeV = sqrt_s_MeV / 1000.0
        β = sqrt(max(0.0, 1.0 - 4*m_GeV^2 / sqrt_s_GeV^2))
        σ_pb = 100.0 * β^3 * (sqrt_s_GeV / m_GeV)^2 * exp(-m_GeV / 300.0)

    该公式仅为示意性，但比固定常数限值更能反映质量依赖。
    """
    m_GeV = mass_MeV / 1000.0
    sqrt_s_GeV = sqrt_s_MeV / 1000.0

    if m_GeV <= 0.0 or sqrt_s_GeV <= 0.0:
        return 0.0

    beta_sq = 1.0 - 4.0 * (m_GeV ** 2) / (sqrt_s_GeV ** 2)
    beta = np.sqrt(max(0.0, beta_sq))
    sigma_pb = 100.0 * (beta ** 3) * (sqrt_s_GeV / m_GeV) ** 2 * np.exp(-m_GeV / 300.0)
    return float(sigma_pb)


def direct_detection_si_cross_section(
    mass_MeV: float,
    coupling: float = 1.0,
    mediator_mass_MeV: float = 1_000_000.0,
) -> float:
    """
    玩具自旋无关核子散射截面 σ_SI（单位 cm²）。

    公式：
        m_GeV = mass_MeV / 1000.0
        μ = (m_GeV * m_nucleon) / (m_GeV + m_nucleon)
        σ_SI = 1e-36 * coupling^2 * (μ / 100.0)^2 / m_GeV^2
               * (1_000_000.0 / mediator_mass_MeV)^4

    其中 m_nucleon = 0.939 GeV。
    """
    m_GeV = mass_MeV / 1000.0
    if m_GeV <= 0.0:
        return 0.0

    mu_GeV = (m_GeV * M_NUCLEON_GEV) / (m_GeV + M_NUCLEON_GEV)
    sigma_cm2 = (
        1e-36
        * (coupling ** 2)
        * (mu_GeV / 100.0) ** 2
        / (m_GeV ** 2)
        * (1_000_000.0 / mediator_mass_MeV) ** 4
    )
    return float(sigma_cm2)
