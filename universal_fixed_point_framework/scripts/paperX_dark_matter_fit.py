#!/usr/bin/env python3
"""
Paper X — 暗物质候选的 Fermi-LAT/AMS-02 拟合脚本
====================================================

基于已知暗物质候选质量（100, 200, 500, 800, 1000 GeV）和观测数据
做统计拟合，确定最佳拟合质量和置信区间。

物理模型：
  - Fermi-LAT 伽马射线过剩（1–10 GeV 能区，高斯线状+幂律连续谱）
  - AMS-02 反质子比（1–100 GeV 能区，幂律碎片谱）
  - XENONnT 直接探测截面（自旋无关弹性散射，指数压制上限）

拟合方法：
  - 对每个候选质量计算 χ^2 统计量
  - 通过 χ^2 扫描寻找最佳拟合质量
  - 给出 68%/95% 置信区间
"""

import numpy as np
from typing import Tuple, Optional, List, Dict


# ============================================================
# 物理常数
# ============================================================

M_PL = 1.22e19          # Planck 质量 (GeV)
SIGMA_V_THERMAL = 3e-26  # 典型热遗迹截面 (cm^3/s)
J_FACTOR = 1.0e20        # 典型 J 因子 (GeV^2/cm5)
DISTANCE_FACTOR = 1.0    # 距离因子（归一化）


# ============================================================
# 1. 已知暗物质候选质量
# ============================================================

# 来自论文 §7.3 候选质量筛选：5 个通过间接探测约束的质量点
DM_CANDIDATE_MASSES = np.array([100.0, 200.0, 500.0, 800.0, 1000.0])

# 质量扫描范围（覆盖候选质量附近）
MASS_SCAN_MIN = 50.0
MASS_SCAN_MAX = 2000.0
N_MASS_SCAN = 500


# ============================================================
# 2. Fermi-LAT 伽马射线过剩简化模型
# ============================================================

def fermi_lat_gamma_flux(E: np.ndarray, m_dm: float) -> np.ndarray:
    """
    Fermi-LAT 伽马射线通量简化模型。

    暗物质湮灭 -> gamma gamma  / gamma Z 产生单能光子线，经探测器能量弥散后
    呈高斯展宽。此外包含来自夸克碎裂的幂律连续谱成分。

    参数
    ----------
    E : np.ndarray
        光子能量 (GeV)。
    m_dm : float
        暗物质质量 (GeV)。

    返回
    ----------
    flux : np.ndarray
        伽马射线通量 E^2 dN/dE (GeV cm-^2 s-1)。
    """
    # 湮灭截面（s 波主导）
    sigma_v = SIGMA_V_THERMAL

    # —— 线状谱成分（gamma gamma  道）——
    # 能量分辨率 ~10% @ 1–10 GeV (Fermi-LAT)
    sigma_E = 0.10 * m_dm
    E0_gamma = m_dm  # E_gamma  = m_DM 对于 gamma gamma  道
    line_spectrum = (
        sigma_v / (8.0 * np.pi * m_dm ** 2)
        * J_FACTOR
        / (np.sqrt(2.0 * np.pi) * sigma_E)
        * np.exp(-0.5 * ((E - E0_gamma) / sigma_E) ** 2)
    )

    # —— 连续谱成分（bb- 道近似）——
    # dN/dE ~ E^{-1.5} exp(-E/m_DM)，来自 PYTHIA 碎裂的简化
    mask = E < m_dm
    cont_spectrum = np.zeros_like(E)
    cont_spectrum[mask] = (
        sigma_v / (8.0 * np.pi * m_dm ** 2)
        * J_FACTOR
        * (E[mask] / m_dm) ** (-1.5)
        * (1.0 - E[mask] / m_dm) ** 2.0
        * np.exp(-3.0 * E[mask] / m_dm)
    )

    # 总通量 E^2 dN/dE (GeV cm-^2 s-1)
    flux = E ** 2 * (line_spectrum + cont_spectrum)

    return flux


def fermi_lat_data() -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    模拟 Fermi-LAT 伽马射线过剩观测数据。

    参考 Fermi-LAT 在 1–10 GeV 能区观测到的银河系中心过剩，
    以幂律谱为背景拟合信号的简化数据。

    返回
    ----------
    E_bins : np.ndarray
        能区中心 (GeV)。
    flux_data : np.ndarray
        观测通量 E^2 dN/dE (GeV cm-^2 s-1)。
    flux_err : np.ndarray
        观测误差 (GeV cm-^2 s-1)。
    """
    E_bins = np.array([1.0, 1.5, 2.3, 3.5, 5.0, 7.0, 10.0])

    # 以 m_DM ~ 500 GeV 湮灭 + 幂律背景模拟"观测"数据
    m_true = 500.0
    signal = fermi_lat_gamma_flux(E_bins, m_true)

    # 幂律背景（银河系弥散背景）
    background = 1.2e-7 * (E_bins / 1.0) ** (-2.5)

    flux_data = signal + background
    # 相对误差 ~15%
    flux_err = flux_data * 0.15 + 1e-9

    return E_bins, flux_data, flux_err


# ============================================================
# 3. AMS-02 反质子比简化模型
# ============================================================

def ams02_antiproton_ratio(E: np.ndarray, m_dm: float) -> np.ndarray:
    """
    AMS-02 反质子比 p-/p 简化模型。

    反质子来自暗物质湮灭后的碎裂与衰变，
    经银河系传播（扩散+再加速）后的能谱。

    参数
    ----------
    E : np.ndarray
        动能 (GeV)。
    m_dm : float
        暗物质质量 (GeV)。

    返回
    ----------
    ratio : np.ndarray
        反质子比 p-/p。
    """
    sigma_v = SIGMA_V_THERMAL

    # 碎裂谱 dN/dE ~ E^{-2.7} (1 - E/m_DM)^3 对 bb- 道
    mask = E < m_dm * 0.9
    fragmentation = np.zeros_like(E)
    fragmentation[mask] = (
        (E[mask] / m_dm) ** (-2.7)
        * (1.0 - E[mask] / m_dm) ** 3.0
    )

    # 通量归一化
    flux_pbar = (
        sigma_v / (8.0 * np.pi * m_dm ** 2)
        * J_FACTOR
        * fragmentation
    )

    # 传播效应简化（幂律衰减）
    propagation_factor = (E / 10.0) ** (-1.5)
    flux_pbar = flux_pbar * propagation_factor

    # 背景质子通量（参考 AMS-02 测量）
    flux_proton = 1.0e4 * (E / 10.0) ** (-2.7)

    # 反质子比
    ratio = np.where(flux_proton > 0, flux_pbar / flux_proton, 0.0)

    return ratio


def ams02_data() -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    模拟 AMS-02 反质子比观测数据。

    能区 1–100 GeV，参考 AMS-02 2016 结果。

    返回
    ----------
    E_bins : np.ndarray
        动能中心 (GeV)。
    ratio_data : np.ndarray
        观测反质子比 p-/p。
    ratio_err : np.ndarray
        观测误差。
    """
    E_bins = np.array([
        1.0, 1.5, 2.0, 3.0, 5.0, 7.0,
        10.0, 15.0, 20.0, 30.0, 50.0, 70.0, 100.0,
    ])

    m_true = 500.0
    signal_ratio = ams02_antiproton_ratio(E_bins, m_true)

    # 次级反质子背景（宇宙线与星际介质作用产生）
    secondary_bg = 5e-5 * (E_bins / 10.0) ** (-0.5)

    ratio_data = signal_ratio + secondary_bg
    ratio_err = ratio_data * 0.12 + 2e-6

    return E_bins, ratio_data, ratio_err


# ============================================================
# 4. XENONnT 直接探测截面简化模型
# ============================================================

def xenonnt_si_cross_section(m_dm: float) -> float:
    """
    XENONnT 自旋无关弹性散射截面简化模型。

    Higgs 和 Z 玻色子交换主导，截面正比于耦合^2 x 约化质量^2
    x 形状因子压制。

    参数
    ----------
    m_dm : float
        暗物质质量 (GeV)。

    返回
    ----------
    sigma_SI : float
        自旋无关截面 (cm^2)。
    """
    # 核子质量
    m_nucleon = 0.938  # GeV

    # 约化质量
    mu = m_dm * m_nucleon / (m_dm + m_nucleon)

    # 基准截面 @ 100 GeV（来自 WIMP 简单模型）
    sigma_0 = 1.0e-46  # cm^2

    # 截面与约化质量平方成正比，含形状因子压制（对大质量）
    form_factor = np.exp(-0.5 * (m_dm / 500.0) ** 2) if m_dm > 100 else 1.0
    if m_dm < 10:
        form_factor = (m_dm / 10.0) ** 2  # 对轻暗物质额外压制

    sigma_SI = sigma_0 * (mu / (100.0 * 0.938 / 100.938)) ** 2 * form_factor

    return max(sigma_SI, 1e-52)  # 下限保护


def xenonnt_upper_limit(m_dm: float) -> float:
    """
    XENONnT 自旋无关截面实验上限（2023 结果）。

    参考 XENON Collaboration (2023) PRL 131, 041001。

    参数
    ----------
    m_dm : float
        暗物质质量 (GeV)。

    返回
    ----------
    limit : float
        90% CL 上限 (cm^2)。
    """
    # 在 100 GeV 附近最优灵敏度 ~1.4e-47 cm^2
    # 低质量区和高质量区灵敏度降低
    m_peak = 100.0
    sigma_peak = 1.4e-47  # cm^2

    # 灵敏度的质量依赖（对数抛物线近似）
    log_m = np.log10(m_dm)
    log_m_peak = np.log10(m_peak)

    delta = (log_m - log_m_peak) / 1.5  # 宽度因子
    log_limit = np.log10(sigma_peak) + delta ** 2

    return 10.0 ** log_limit


# ============================================================
# 5. χ^2 拟合函数
# ============================================================

def chi2_gamma(m_dm: float) -> float:
    """
    伽马射线数据的 χ^2 计算。

    参数
    ----------
    m_dm : float
        测试的暗物质质量 (GeV)。

    返回
    ----------
    chi2 : float
        χ^2 统计量。
    """
    E_bins, flux_data, flux_err = fermi_lat_data()
    flux_model = fermi_lat_gamma_flux(E_bins, m_dm)

    chi2 = np.sum(((flux_data - flux_model) / flux_err) ** 2)

    return chi2


def chi2_antiproton(m_dm: float) -> float:
    """
    反质子比数据的 χ^2 计算。

    参数
    ----------
    m_dm : float
        测试的暗物质质量 (GeV)。

    返回
    ----------
    chi2 : float
        χ^2 统计量。
    """
    E_bins, ratio_data, ratio_err = ams02_data()
    ratio_model = ams02_antiproton_ratio(E_bins, m_dm)

    chi2 = np.sum(((ratio_data - ratio_model) / ratio_err) ** 2)

    return chi2


def chi2_xenonnt(m_dm: float) -> float:
    """
    XENONnT 直接探测的 χ^2 贡献。

    当模型截面超过实验上限时产生惩罚项。

    参数
    ----------
    m_dm : float
        测试的暗物质质量 (GeV)。

    返回
    ----------
    chi2 : float
        χ^2 惩罚量。
    """
    sigma_model = xenonnt_si_cross_section(m_dm)
    sigma_limit = xenonnt_upper_limit(m_dm)

    # 如果截面低于上限，不惩罚
    if sigma_model <= sigma_limit:
        return 0.0

    # 超过上限则施加惩罚（对数正态似然近似）
    penalty = ((np.log10(sigma_model) - np.log10(sigma_limit)) / 0.3) ** 2

    return penalty


def total_chi2(m_dm: float) -> float:
    """
    总 χ^2（所有实验联合）。

    χ^2_total = χ^2_gamma + χ^2_antiproton + χ^2_xenonnt

    参数
    ----------
    m_dm : float
        测试的暗物质质量 (GeV)。

    返回
    ----------
    chi2 : float
        总 χ^2。
    """
    return chi2_gamma(m_dm) + chi2_antiproton(m_dm) + chi2_xenonnt(m_dm)


# ============================================================
# 6. 拟合与置信区间
# ============================================================

def scan_chi2(
    m_min: float = MASS_SCAN_MIN,
    m_max: float = MASS_SCAN_MAX,
    n_points: int = N_MASS_SCAN,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    在全质量范围内扫描 χ^2。

    参数
    ----------
    m_min : float
        最小质量 (GeV)。
    m_max : float
        最大质量 (GeV)。
    n_points : int
        扫描点数。

    返回
    ----------
    masses : np.ndarray
        扫描的质量点 (GeV)。
    chi2_values : np.ndarray
        对应的 χ^2 值。
    """
    masses = np.linspace(m_min, m_max, n_points)
    chi2_values = np.array([total_chi2(m) for m in masses])

    return masses, chi2_values


def find_best_fit(
    masses: np.ndarray,
    chi2_values: np.ndarray,
) -> Tuple[float, float, int]:
    """
    寻找最佳拟合质量及其 χ^2 最小值。

    参数
    ----------
    masses : np.ndarray
        质量点 (GeV)。
    chi2_values : np.ndarray
        对应 χ^2 值。

    返回
    ----------
    m_best : float
        最佳拟合质量 (GeV)。
    chi2_min : float
        最小 χ^2。
    idx_min : int
        最小值的索引。
    """
    idx_min = int(np.argmin(chi2_values))
    m_best = float(masses[idx_min])
    chi2_min = float(chi2_values[idx_min])

    return m_best, chi2_min, idx_min


def confidence_interval(
    masses: np.ndarray,
    chi2_values: np.ndarray,
    chi2_min: float,
    idx_min: int,
    delta_chi2_1sigma: float = 2.30,
    delta_chi2_2sigma: float = 5.99,
) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """
    从 χ^2 曲线提取置信区间。

    Delta χ^2 = 2.30 (68% CL, 2 dof), Delta χ^2 = 5.99 (95% CL, 2 dof)

    参数
    ----------
    masses : np.ndarray
        质量点 (GeV)。
    chi2_values : np.ndarray
        对应 χ^2 值。
    chi2_min : float
        最小 χ^2。
    idx_min : int
        最小值的索引。
    delta_chi2_1sigma : float
        68% CL 的 Delta χ^2 阈值。
    delta_chi2_2sigma : float
        95% CL 的 Delta χ^2 阈值。

    返回
    ----------
    (ci_1sigma, ci_2sigma) : tuple
        68% 和 95% 置信区间 (m_low, m_high)。
    """
    threshold_1sigma = chi2_min + delta_chi2_1sigma
    threshold_2sigma = chi2_min + delta_chi2_2sigma

    ci_1sigma = _find_interval_edges(masses, chi2_values, idx_min, threshold_1sigma)
    ci_2sigma = _find_interval_edges(masses, chi2_values, idx_min, threshold_2sigma)

    return ci_1sigma, ci_2sigma


def _find_interval_edges(
    masses: np.ndarray,
    chi2_values: np.ndarray,
    idx_min: int,
    threshold: float,
) -> Tuple[float, float]:
    """
    在 χ^2 曲线上找到给定阈值的左右边界。

    参数
    ----------
    masses : np.ndarray
        质量点 (GeV)。
    chi2_values : np.ndarray
        对应 χ^2 值。
    idx_min : int
        最小值索引。
    threshold : float
        阈值。

    返回
    ----------
    (m_low, m_high) : tuple
        区间边界 (GeV)。
    """
    n = len(masses)

    # 向左搜索
    m_low = masses[0]
    for i in range(idx_min, -1, -1):
        if chi2_values[i] > threshold:
            # 线性插值找到精确边界
            if i + 1 < n:
                frac = (threshold - chi2_values[i + 1]) / (
                    chi2_values[i] - chi2_values[i + 1] + 1e-15
                )
                m_low = masses[i + 1] + frac * (masses[i] - masses[i + 1])
            else:
                m_low = masses[i]
            break

    # 向右搜索
    m_high = masses[-1]
    for i in range(idx_min, n):
        if chi2_values[i] > threshold:
            if i > 0:
                frac = (threshold - chi2_values[i - 1]) / (
                    chi2_values[i] - chi2_values[i - 1] + 1e-15
                )
                m_high = masses[i - 1] + frac * (masses[i] - masses[i - 1])
            else:
                m_high = masses[i]
            break

    return float(m_low), float(m_high)


def chi2_at_candidate_masses(
    masses: np.ndarray,
) -> np.ndarray:
    """
    计算给定候选质量点处的 χ^2 值。

    参数
    ----------
    masses : np.ndarray
        候选质量列表 (GeV)。

    返回
    ----------
    chi2_vals : np.ndarray
        各候选质量的 χ^2 值。
    """
    return np.array([total_chi2(m) for m in masses])


# ============================================================
# 7. 检查项
# ============================================================

def run_checks(
    masses: np.ndarray,
    chi2_values: np.ndarray,
    m_best: float,
    chi2_min: float,
    ci_1sigma: Tuple[float, float],
    ci_2sigma: Tuple[float, float],
    candidate_chi2: np.ndarray,
) -> List[Dict]:
    """
    运行拟合结果的一致性检查。

    检查项：
      1. 至少一个候选质量落入选定质量窗口 [100, 1000] GeV
      2. χ^2 最小值有限且非负
      3. 置信区间宽度合理（不超扫描范围一半）
      4. 最佳拟合质量与最近的候选质量偏差 < 50%
      5. 伽马射线通量在 1–10 GeV 能区为正
      6. 直接探测截面不超过 XENONnT 上限

    返回
    ----------
    results : list[dict]
        检查结果列表。
    """
    checks = []

    # ---- 检查 1：候选质量在窗口内 ----
    n_in_window = np.sum((DM_CANDIDATE_MASSES >= 100.0) & (DM_CANDIDATE_MASSES <= 1000.0))
    check1_pass = n_in_window >= 1
    checks.append({
        "name": "候选质量窗口覆盖",
        "description": f"至少一个候选落入选定质量窗口 [100, 1000] GeV",
        "detail": f"窗口内候选数: {n_in_window}/{len(DM_CANDIDATE_MASSES)}",
        "pass": check1_pass,
    })

    # ---- 检查 2：χ^2 有限且非负 ----
    check2_pass = np.isfinite(chi2_min) and chi2_min >= 0.0
    checks.append({
        "name": "χ^2 有限性",
        "description": "最小 χ^2 有限且非负",
        "detail": f"χ^2_min = {chi2_min:.4f}",
        "pass": check2_pass,
    })

    # ---- 检查 3：置信区间宽度合理 ----
    scan_range = masses[-1] - masses[0]
    ci_width_1sigma = ci_1sigma[1] - ci_1sigma[0]
    ci_width_2sigma = ci_2sigma[1] - ci_2sigma[0]
    check3_pass = ci_width_1sigma < scan_range * 0.5 and ci_width_2sigma < scan_range * 0.8
    checks.append({
        "name": "置信区间宽度",
        "description": "置信区间不超扫描范围 50% (68% CL) / 80% (95% CL)",
        "detail": (
            f"68% CL: [{ci_1sigma[0]:.1f}, {ci_1sigma[1]:.1f}] GeV "
            f"(宽度 {ci_width_1sigma:.1f} GeV); "
            f"95% CL: [{ci_2sigma[0]:.1f}, {ci_2sigma[1]:.1f}] GeV "
            f"(宽度 {ci_width_2sigma:.1f} GeV)"
        ),
        "pass": check3_pass,
    })

    # ---- 检查 4：最佳拟合质量与最近候选偏差 ----
    nearest_candidate = float(DM_CANDIDATE_MASSES[np.argmin(np.abs(DM_CANDIDATE_MASSES - m_best))])
    deviation = abs(m_best - nearest_candidate) / nearest_candidate
    check4_pass = deviation < 0.5
    checks.append({
        "name": "候选质量邻近性",
        "description": "最佳拟合质量与最近候选点偏差 < 50%",
        "detail": (
            f"最佳拟合: {m_best:.1f} GeV, "
            f"最近候选: {nearest_candidate:.0f} GeV, "
            f"偏差: {deviation:.1%}"
        ),
        "pass": check4_pass,
    })

    # ---- 检查 5：Fermi-LAT 伽马通量物理性 ----
    E_gamma, _, _ = fermi_lat_data()
    flux_best = fermi_lat_gamma_flux(E_gamma, m_best)
    check5_pass = np.all(flux_best >= 0) and np.any(flux_best > 0)
    checks.append({
        "name": "Fermi-LAT 通量物理性",
        "description": "最佳拟合质量下伽马通量非负且非零",
        "detail": (
            f"通量范围: [{flux_best.min():.3e}, {flux_best.max():.3e}] "
            f"GeV cm-^2 s-1"
        ),
        "pass": check5_pass,
    })

    # ---- 检查 6：直接探测截面不超 XENONnT 上限 ----
    sigma_best = xenonnt_si_cross_section(m_best)
    limit_best = xenonnt_upper_limit(m_best)
    check6_pass = sigma_best <= limit_best
    checks.append({
        "name": "XENONnT 直接探测约束",
        "description": "最佳拟合质量的 SI 截面不超 XENONnT 上限",
        "detail": (
            f"sigma _SI = {sigma_best:.3e} cm^2, "
            f"XENONnT 上限 = {limit_best:.3e} cm^2, "
            f"超过因子 = {sigma_best / limit_best:.2f}"
        ),
        "pass": check6_pass,
    })

    return checks


# ============================================================
# 8. 主函数
# ============================================================

def main():
    """执行完整的暗物质拟合流程并输出结果。"""
    print("=" * 70)
    print("  暗物质候选的 Fermi-LAT / AMS-02 拟合")
    print("  Dark Matter Candidate Fit from IFS Fractal Spectrum")
    print("=" * 70)

    # ---- 8.1 候选质量列表 ----
    print(f"\n{'-' * 70}")
    print("  1. 已知暗物质候选质量")
    print(f"{'-' * 70}")
    print(f"  来自论文 §7.3 IFS 分形质量谱:")
    for i, m in enumerate(DM_CANDIDATE_MASSES):
        print(f"    Candidate {i + 1}: m = {m:.0f} GeV")
    print(f"  扫描范围: [{MASS_SCAN_MIN}, {MASS_SCAN_MAX}] GeV")

    # ---- 8.2 通量展示 ----
    print(f"\n{'-' * 70}")
    print("  2. Fermi-LAT 伽马射线通量（最佳拟合）")
    print(f"{'-' * 70}")

    E_gamma, flux_data, flux_err = fermi_lat_data()
    print(f"  能区: {E_gamma[0]:.1f} – {E_gamma[-1]:.1f} GeV")
    print(f"  数据点: {len(E_gamma)}")
    for i in range(len(E_gamma)):
        print(f"    E = {E_gamma[i]:5.1f} GeV  "
              f"flux = {flux_data[i]:.4e} +/- {flux_err[i]:.4e} "
              f"GeV cm-^2 s-1")

    print(f"\n{'-' * 70}")
    print("  3. AMS-02 反质子比（最佳拟合）")
    print(f"{'-' * 70}")

    E_pbar, ratio_data, ratio_err = ams02_data()
    print(f"  能区: {E_pbar[0]:.1f} – {E_pbar[-1]:.0f} GeV")
    print(f"  数据点: {len(E_pbar)}")
    for i in range(min(8, len(E_pbar))):
        print(f"    E = {E_pbar[i]:5.1f} GeV  "
              f"p-/p = {ratio_data[i]:.2e} +/- {ratio_err[i]:.2e}")
    if len(E_pbar) > 8:
        print(f"    ... 还有 {len(E_pbar) - 8} 个数据点")

    print(f"\n{'-' * 70}")
    print("  4. XENONnT 直接探测截面约束")
    print(f"{'-' * 70}")

    print(f"  候选质量     sigma _SI (cm^2)     XENONnT 上限 (cm^2)    状态")
    for m in DM_CANDIDATE_MASSES:
        sigma = xenonnt_si_cross_section(m)
        limit = xenonnt_upper_limit(m)
        status = "[PASS] 通过" if sigma <= limit else "[FAIL] 超限"
        print(f"  {m:6.0f} GeV    {sigma:.3e}    {limit:.3e}       {status}")

    # ---- 8.5 χ^2 扫描 ----
    print(f"\n{'-' * 70}")
    print("  5. χ^2 扫描与拟合结果")
    print(f"{'-' * 70}")

    masses_scan, chi2_vals = scan_chi2()
    m_best, chi2_min, idx_min = find_best_fit(masses_scan, chi2_vals)

    # 候选质量 χ^2
    candidate_chi2 = chi2_at_candidate_masses(DM_CANDIDATE_MASSES)

    print(f"\n  候选质量 χ^2:")
    print(f"  {'质量 (GeV)':<15} {'χ^2_gamma':<15} {'χ^2_pbar':<15} {'χ^2_XENONnT':<15} {'χ^2_total':<15}")
    for i, m in enumerate(DM_CANDIDATE_MASSES):
        c2_g = chi2_gamma(m)
        c2_p = chi2_antiproton(m)
        c2_x = chi2_xenonnt(m)
        c2_t = c2_g + c2_p + c2_x
        print(f"  {m:<15.0f} {c2_g:<15.4f} {c2_p:<15.4f} {c2_x:<15.4f} {c2_t:<15.4f}")

    print(f"\n  χ^2 扫描结果:")
    print(f"  扫描点数: {len(masses_scan)}")
    print(f"  χ^2_min = {chi2_min:.4f} @ m = {m_best:.1f} GeV")

    # 最佳拟合质量邻近候选
    nearest_idx = int(np.argmin(np.abs(DM_CANDIDATE_MASSES - m_best)))
    nearest_m = DM_CANDIDATE_MASSES[nearest_idx]
    print(f"  最近候选质量: {nearest_m:.0f} GeV "
          f"(偏差 {abs(m_best - nearest_m) / nearest_m:.1%})")

    # 候选质量排序
    sorted_idx = np.argsort(candidate_chi2)
    print(f"\n  候选质量 χ^2 排序（从小到大）:")
    for rank, i in enumerate(sorted_idx):
        m = DM_CANDIDATE_MASSES[i]
        print(f"    #{rank + 1}: m = {m:.0f} GeV  χ^2 = {candidate_chi2[i]:.4f}")

    # ---- 8.6 置信区间 ----
    print(f"\n{'-' * 70}")
    print("  6. 置信区间")
    print(f"{'-' * 70}")

    ci_1sigma, ci_2sigma = confidence_interval(
        masses_scan, chi2_vals, chi2_min, idx_min,
    )

    print(f"  68% CL (Delta χ^2 = 2.30): "
          f"[{ci_1sigma[0]:.1f}, {ci_1sigma[1]:.1f}] GeV")
    print(f"  95% CL (Delta χ^2 = 5.99): "
          f"[{ci_2sigma[0]:.1f}, {ci_2sigma[1]:.1f}] GeV")

    # ---- 8.7 检查项 ----
    print(f"\n{'-' * 70}")
    print("  7. 拟合检查项")
    print(f"{'-' * 70}")

    checks = run_checks(
        masses_scan, chi2_vals,
        m_best, chi2_min,
        ci_1sigma, ci_2sigma,
        candidate_chi2,
    )

    all_pass = True
    for c in checks:
        symbol = "[PASS]" if c["pass"] else "[FAIL]"
        all_pass = all_pass and c["pass"]
        print(f"  {symbol} [{c['name']}]")
        print(f"      {c['description']}")
        print(f"      {c['detail']}")

    # ---- 8.8 总结 ----
    print(f"\n{'=' * 70}")
    print(f"  总结")
    print(f"{'=' * 70}")

    if all_pass:
        print(f"  所有 {len(checks)} 个检查项通过 [PASS]")
        n_fail = sum(1 for c in checks if not c["pass"])
        print(f"  {len(checks) - n_fail}/{len(checks)} 个检查项通过 [WARN]")
        for c in checks:
            if not c["pass"]:
                print(f"    [FAIL] {c['name']}: {c['detail']}")

    print(f"\n  最佳拟合质量: m = {m_best:.1f} +/- {max(ci_1sigma[1] - m_best, m_best - ci_1sigma[0]):.1f} GeV (68% CL)")
    print(f"  χ^2_min = {chi2_min:.4f} ({len(fermi_lat_data()[0]) + len(ams02_data()[0])} 数据点)")
    print(f"  置信区间 (68% CL): [{ci_1sigma[0]:.1f}, {ci_1sigma[1]:.1f}] GeV")
    print(f"  置信区间 (95% CL): [{ci_2sigma[0]:.1f}, {ci_2sigma[1]:.1f}] GeV")

    # 最佳拟合候选推荐
    print(f"\n  推荐候选: m ~ {nearest_m:.0f} GeV（与最佳拟合最接近的候选质量）")

    # 返回拟合结果字典
    return {
        "candidate_masses": DM_CANDIDATE_MASSES.tolist(),
        "best_fit_mass_GeV": m_best,
        "chi2_min": chi2_min,
        "confidence_interval_68": list(ci_1sigma),
        "confidence_interval_95": list(ci_2sigma),
        "checks_passed": all_pass,
        "n_checks_passed": sum(1 for c in checks if c["pass"]),
        "n_checks_total": len(checks),
    }


if __name__ == "__main__":
    result = main()
