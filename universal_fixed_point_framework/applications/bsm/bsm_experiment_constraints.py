"""
bsm_experiment_constraints.py

BSM 实验约束接口：将 LHC 直接搜寻、暗物质遗迹密度与直接探测的简化约束
整合为可与 BSMInstance 对接的验证模块。

定位：
- 本文件属于「通用不动点范畴框架」的实例假设层（Model Hypotheses）。
- 这些约束不是理论核心，只是用于判断 BSM 新费米子谱是否与现有实验相容。

说明：
- 当前数值为保守近似（原型阶段），不构成完整的唯象学分析。
- 单位统一为 MeV（质量）与 cm³/s（湮灭截面）、cm²（散射截面）。
"""

from __future__ import annotations

import numpy as np

import bsm_cross_sections as xs

# LHC 对矢量型重费米子（VLF）的直接搜寻下限（保守取值，约 1.2–1.5 TeV）
LHC_VLF_MASS_LIMIT_MEV = 1_200_000.0  # 1.2 TeV

# Planck 2018 暗物质遗迹密度
PLANCK_RELIC_DENSITY = 0.12

# 典型热遗迹湮灭截面（WIMP miracle 标准值）
THERMAL_RELIC_CROSS_SECTION_CM3_PER_S = 3e-26

# 10 GeV - 100 TeV 视为 WIMP 暗物质质量扫描区间
WIMP_MASS_RANGE_MEV = (10_000.0, 100_000_000.0)


def lhc_vector_like_fermion_constraint(masses_MeV: dict[str, float]) -> dict:
    """
    LHC 对矢量型重费米子的直接质量下限约束。

    返回每个粒子的 pass/fail 与整体结果。
    """
    results = {
        "experiment": "LHC direct search (VLF)",
        "limit_MeV": LHC_VLF_MASS_LIMIT_MEV,
        "limit_GeV": LHC_VLF_MASS_LIMIT_MEV / 1_000.0,
        "per_particle": {},
        "overall_pass": True,
    }
    for name, mass in masses_MeV.items():
        passed = mass >= LHC_VLF_MASS_LIMIT_MEV
        results["per_particle"][name] = {
            "mass_MeV": mass,
            "mass_GeV": mass / 1_000.0,
            "pass": passed,
        }
        if not passed:
            results["overall_pass"] = False
    return results


def thermal_relic_cross_section(
    mass_MeV: float,
    coupling: float = 1.0,
    reference_mass_MeV: float = 1_000_000.0,
) -> float:
    """
    玩具模型：热遗迹湮灭截面随质量与耦合的变化。

    取 σv ∝ coupling^4 / mass^2，并在 mass=1 TeV、coupling=1 时归一化到
    THERMAL_RELIC_CROSS_SECTION_CM3_PER_S。
    """
    mass_ratio = mass_MeV / reference_mass_MeV
    return THERMAL_RELIC_CROSS_SECTION_CM3_PER_S * (coupling ** 4) / (mass_ratio ** 2)


def relic_density_constraint(
    mass_MeV: float,
    annihilation_cross_section_cm3_per_s: float | None = None,
    coupling: float = 1.0,
    degrees_of_freedom: int = 2,
) -> dict:
    """
    暗物质遗迹密度约束。

    若未提供 annihilation_cross_section，则调用 xs.thermal_relic_density
    由质量与耦合估算；否则使用给定截面计算 Ωh²。
    """
    relic = xs.thermal_relic_density(
        mass_MeV,
        annihilation_cross_section_cm3_per_s=annihilation_cross_section_cm3_per_s,
        coupling=coupling,
        degrees_of_freedom=degrees_of_freedom,
    )

    # 保持原有接口的同时补充 Ωh² 与 x_f
    ratio = relic["Omega_h2"] / PLANCK_RELIC_DENSITY
    return {
        "experiment": "Planck relic density",
        "target_density": PLANCK_RELIC_DENSITY,
        "mass_MeV": mass_MeV,
        "mass_GeV": mass_MeV / 1_000.0,
        "sigma_v_cm3_per_s": relic["sigma_v"],
        "Omega_h2": relic["Omega_h2"],
        "x_f": relic["x_f"],
        "ratio_to_thermal": ratio,
        "pass": relic["pass"],
    }


def xenon1t_spin_independent_limit(mass_MeV: float) -> float:
    """
    XENON1T/LZ 型直接探测实验的近似自旋无关截面上限（cm²）。

    使用一个简化包络：
        log10(σ_max/cm²) ≈ -45 + 0.5 * log10(m/100 GeV)
    在 m ≈ 100 GeV 时约为 10^{-45} cm²。
    """
    mass_GeV = mass_MeV / 1_000.0
    if mass_GeV <= 0:
        return np.inf
    log10_sigma = -45.0 + 0.5 * np.log10(mass_GeV / 100.0)
    return 10.0 ** log10_sigma


def direct_detection_constraint(
    mass_MeV: float,
    spin_independent_cross_section_cm2: float | None = None,
    coupling: float = 1.0,
    mediator_mass_MeV: float = 1_000_000.0,
) -> dict:
    """
    暗物质直接探测约束。

    若未提供 spin_independent_cross_section，则调用 xs.direct_detection_si_cross_section
    由质量、耦合与中介子质量估算。
    """
    mass_GeV = mass_MeV / 1_000.0
    limit = xenon1t_spin_independent_limit(mass_MeV)

    if spin_independent_cross_section_cm2 is None:
        sigma_si = xs.direct_detection_si_cross_section(
            mass_MeV, coupling=coupling, mediator_mass_MeV=mediator_mass_MeV
        )
    else:
        sigma_si = spin_independent_cross_section_cm2

    return {
        "experiment": "XENON1T/LZ spin-independent direct detection",
        "mass_MeV": mass_MeV,
        "mass_GeV": mass_GeV,
        "sigma_SI_cm2": sigma_si,
        "sigma_SI_limit_cm2": limit,
        "pass": sigma_si <= limit,
    }


def lhc_pair_production_constraint(
    mass_MeV: float,
    sqrt_s_MeV: float = 13_000_000.0,
    min_sigma_pb: float = 0.01,
) -> dict:
    """
    LHC 矢量型重费米子对产生截面的探测灵敏度约束。

    使用 xs.lhc_pair_production_cross_section 计算近似 NNLO 截面，
    当预测截面大于灵敏度阈值 min_sigma_pb 时视为可被探测（pass=True）。
    """
    sigma_pb = xs.lhc_pair_production_cross_section(mass_MeV, sqrt_s_MeV=sqrt_s_MeV)
    return {
        "experiment": "LHC pair production (NNLO approximate)",
        "mass_MeV": mass_MeV,
        "mass_GeV": mass_MeV / 1_000.0,
        "sigma_pb": sigma_pb,
        "min_sigma_pb": min_sigma_pb,
        "pass": sigma_pb >= min_sigma_pb,
    }


def check_all(
    masses_MeV: dict[str, float],
    dark_matter_candidate_mass_MeV: float | None = None,
    annihilation_cross_section_cm3_per_s: float | None = None,
    spin_independent_cross_section_cm2: float | None = None,
    coupling: float = 1.0,
    include_lhc_pair_production: bool = False,
) -> dict:
    """
    综合 LHC、遗迹密度与直接探测约束。

    若未指定 dark_matter_candidate_mass，则默认使用最轻的 BSM 粒子。
    可通过 include_lhc_pair_production=True 额外开启对产生截面检查。
    """
    results = {
        "lhc": lhc_vector_like_fermion_constraint(masses_MeV),
    }

    if dark_matter_candidate_mass_MeV is None and masses_MeV:
        dark_matter_candidate_mass_MeV = min(masses_MeV.values())

    if dark_matter_candidate_mass_MeV is not None:
        results["relic_density"] = relic_density_constraint(
            dark_matter_candidate_mass_MeV,
            annihilation_cross_section_cm3_per_s,
            coupling,
        )
        results["direct_detection"] = direct_detection_constraint(
            dark_matter_candidate_mass_MeV,
            spin_independent_cross_section_cm2,
            coupling,
        )

    if include_lhc_pair_production and dark_matter_candidate_mass_MeV is not None:
        results["lhc_pair_production"] = lhc_pair_production_constraint(
            dark_matter_candidate_mass_MeV,
        )

    results["overall_pass"] = all(
        r.get("overall_pass", r.get("pass", True)) for r in results.values()
    )
    return results


if __name__ == "__main__":
    print("=" * 60)
    print("BSM 实验约束接口（原型近似）")
    print("=" * 60)

    toy_masses = {
        "VLF_1": 500_000.0,   # 0.5 TeV，应被 LHC 排除
        "VLF_2": 1_500_000.0, # 1.5 TeV，应通过 LHC
        "VLF_3": 2_000_000.0,
    }
    results = check_all(toy_masses, coupling=1.0)

    print("\n[LHC 直接搜寻]")
    for name, info in results["lhc"]["per_particle"].items():
        status = "通过" if info["pass"] else "排除"
        print(f"  {name}: {info['mass_GeV']:.1f} GeV — {status}")

    print("\n[遗迹密度]")
    rd = results["relic_density"]
    print(f"  质量: {rd['mass_GeV']:.1f} GeV")
    print(f"  σv: {rd['sigma_v_cm3_per_s']:.2e} cm³/s")
    print(f"  与热遗迹截面比值: {rd['ratio_to_thermal']:.2f}")
    print(f"  通过: {rd['pass']}")

    print("\n[直接探测]")
    dd = results["direct_detection"]
    print(f"  质量: {dd['mass_GeV']:.1f} GeV")
    print(f"  σ_SI: {dd['sigma_SI_cm2']:.2e} cm²")
    print(f"  上限: {dd['sigma_SI_limit_cm2']:.2e} cm²")
    print(f"  通过: {dd['pass']}")

    print(f"\n[综合结果] 整体通过: {results['overall_pass']}")
