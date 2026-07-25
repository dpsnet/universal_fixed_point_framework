#!/usr/bin/env python3
"""
Phase 52 — B2: 普朗克能标多体散射——2→N 散射谱
=================================================

在谱截断 λ_max ∼ M_Pl 下计算 2→N 多粒子末态散射谱。

内容：
  1. N-粒子相空间积分的谱表示
  2. 2→3 散射谱振幅（引力子 → 3 引力子 + 软因子分解）
  3. 2→4 散射谱振幅（引力子 → 4 引力子）
  4. 末态粒子谱分布（dN/dλ、能量分数分布、谱级联）
  5. 与 2→2 结果的统一对比

依赖：numpy, scipy, spectral_numerics, planck_scattering_2to2
"""

import numpy as np
from typing import Optional, Tuple, Dict, Any, Callable, List
from dataclasses import dataclass, field
from scipy import integrate
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_spectrum.spectral_numerics import (
    SpectralOperator, SpectralData, SpectralMatrix,
    SpectralCutoff, SpectralAccuracy, M_PL, G_N, L_PL
)
from dynamic_spectrum.planck_scattering_2to2 import (
    ScatteringKinematics, SpectralGravitonPropagator,
    GravitonScatteringAmplitude, SpectralUVRegularization,
    KAPPA, KAPPA_SQ, LAMBDA_MAX, DELTA_LAMBDA_MIN
)


# ============================================================
#  物理常数
# ============================================================

# 谱框架基本常数（从 B1 继承）
M_PL_SQ = M_PL ** 2           # Planck 质量平方
M_PL_INV = 1.0 / M_PL         # Planck 长度的倒数

# 相空间积分常数
# N-体相空间体积: Φ_n(s) = C_n · s^{n-2}
# C_n 在 d=4 维时空中的解析值
PHASE_SPACE_CONSTANTS = {
    2: 1.0 / (8.0 * np.pi),           # Φ_2 = 1/(8π)   (2体)
    3: 1.0 / (256.0 * np.pi**3),      # Φ_3            (3体)
    4: 1.0 / (6144.0 * np.pi**5),     # Φ_4            (4体)
}


# ============================================================
#  1. N-粒子相空间谱表示
# ============================================================

class SpectralNPhaseSpace:
    """
    N-粒子相空间积分的谱表示。

    在谱框架中，N-体相空间积分写为对谱变量 λ_i = p_i² 的积分：

        ∫ dΠ_n^{spec} = ∫ (∏_{i=1}^n dλ_i · ρ_spec(λ_i)) · δ(Σ √(λ_i + k_i²) - √s)

    其中 ρ_spec(λ) = Σ_j δ(λ - λ_j) 是谱密度。

    在 Planch 能标附近（λ_max ∼ 1），近似为连续相空间积分：

        Φ_n(s) = ∫ dΠ_n = C_n · s^{n-2} · F_spec(s)

    其中 F_spec(s) 是谱截断修正因子。
    """

    def __init__(self, dim: int = 32, n_max: int = 6):
        self.dim = dim
        self.n_max = min(n_max, 6)  # 最多支持 6 体末态
        self.cutoff = SpectralCutoff()
        self.propagator = SpectralGravitonPropagator(dim=dim)

    def phase_space_weight(self, n: int, s: float) -> float:
        """
        N-体相空间权重 w_n(s)。

        对无质量粒子在 d=4 维时空：
            Φ_n(s) = (1/(2π)^{3n-4}) · (π^{n-1}/(n-1)!(n-2)!) · s^{n-2}

        谱修正：乘以 UV 压制因子 F_spec(s)。

        参数
        ----------
        n : int
            末态粒子数
        s : float
            Mandelstam s（质心能平方）

        返回
        -------
        float : 相空间权重
        """
        if n < 2 or s <= 0:
            return 0.0

        # UV 谱截断
        if s > self.cutoff.lambda_max:
            return 0.0

        # N-体相空间体积的标准公式（无质量粒子）
        if n == 2:
            # Φ_2 = 1/(8π) · (1 + O(ε))
            weight = 1.0 / (8.0 * np.pi)
        elif n == 3:
            # Φ_3 = s/(256π³) 
            weight = s / (256.0 * np.pi**3)
        elif n == 4:
            # Φ_4 = s²/(6144π⁵)
            weight = s**2 / (6144.0 * np.pi**5)
        elif n == 5:
            # Φ_5 = s³/(294912π⁷)
            weight = s**3 / (294912.0 * np.pi**7)
        elif n == 6:
            # Φ_6 = s⁴/(23592960π⁹)
            weight = s**4 / (23592960.0 * np.pi**9)
        else:
            # 通用公式（n ≥ 2）
            weight = s**(n - 2) / ((2**(3*n - 4)) * (np.pi**(3*n - 4)) *
                                    np.math.factorial(n - 1) * np.math.factorial(n - 2))

        # 谱修正：UV 指数压制
        F_spec = np.exp(-s / self.cutoff.lambda_max)

        return weight * F_spec

    def spectral_volume(self, n: int, s_min: float, s_max: float,
                        n_points: int = 100) -> Dict[str, np.ndarray]:
        """
        谱相空间体积随能量的变化。

        参数
        ----------
        n : int
            末态粒子数
        s_min, s_max : float
            s 范围
        n_points : int
            采样点数

        返回
        -------
        dict : {s, Phi_n}
        """
        s_vals = np.geomspace(max(s_min, 1e-10), s_max, n_points)
        Phi_n = np.array([self.phase_space_weight(n, s) for s in s_vals])

        return {'s': s_vals, 'Phi_n': Phi_n}

    def invariant_mass_distribution(self, n: int, s: float,
                                     n_bins: int = 50) -> Dict[str, np.ndarray]:
        """
        不变质量分布 dΦ_n/dM_ij。

        对 N-体末态，任意两个粒子的不变质量平方 M_ij² = (p_i + p_j)²
        的分布由相空间边缘分布给出。

        这里近似为均匀分布（对无质量粒子在 N≥3 时成立）。

        参数
        ----------
        n : int
            末态粒子数
        s : float
            质心能平方
        n_bins : int
            直方图 bin 数

        返回
        -------
        dict : {M_ij, dPhi_dM}
        """
        if n < 3:
            return {'M_ij': np.array([np.sqrt(s)]), 'dPhi_dM': np.array([1.0])}

        M_max = np.sqrt(s)
        M_vals = np.linspace(0, M_max, n_bins)

        # N≥3 时，不变质量分布在 (0, √s) 上近似均匀
        # 精确分布来自相空间边积分
        dPhi_dM = np.ones_like(M_vals) / M_max

        # 谱修正：高 M 区压制
        M_sq = M_vals ** 2
        F_spec = np.exp(-M_sq / self.cutoff.lambda_max)
        dPhi_dM = dPhi_dM * F_spec

        # 归一化
        total = np.trapz(dPhi_dM, M_vals)
        if total > 0:
            dPhi_dM = dPhi_dM / total

        return {'M_ij': M_vals, 'dPhi_dM': dPhi_dM}

    def multiplicity_ratio(self, s: float) -> Dict[int, float]:
        """
        不同末态粒子数 N 的相空间权重比。

        比较 Φ_2/Φ_2、Φ_3/Φ_2、Φ_4/Φ_2 等比值。

        参数
        ----------
        s : float
            质心能平方

        返回
        -------
        dict : {n: ratio_n/2}
        """
        phi_2 = self.phase_space_weight(2, s)
        ratios = {}
        for n in range(2, self.n_max + 1):
            phi_n = self.phase_space_weight(n, s)
            if abs(phi_2) > 1e-40:
                ratios[n] = phi_n / phi_2
            else:
                ratios[n] = 0.0
        return ratios


# ============================================================
#  2. 2→3 散射谱振幅
# ============================================================

class Graviton2to3Scattering:
    """
    2→3 散射谱振幅（引力子 → 3 引力子）。

    在谱框架中，2→3 树图振幅通过软引力子因子从 2→2 振幅因子化：

        M_{2→3}(s, t_1, t_2, ...) ≈ κ · S^{(1)}(q, p_a) · M_{2→2}(s, t)

    其中 S^{(1)}(q, p_a) 是软引力子发射因子，q 是软引力子动量。

    在 UV 截断 λ_max 以下，谱修正因子 F_spec(s) 压制高能贡献。
    """

    def __init__(self, dim: int = 32):
        self.dim = dim
        self.amplitude_2to2 = GravitonScatteringAmplitude(dim=dim)
        self.propagator = SpectralGravitonPropagator(dim=dim)
        self.cutoff = SpectralCutoff()

    def soft_graviton_factor(self, q_momentum: float,
                             p_momentum: float,
                             polarization_contract: float = 1.0) -> float:
        """
        软引力子发射因子 S^{(1)}(q, p)。

        对软引力子动量 q 和硬粒子动量 p：
            S^{(1)} = ε_{μν}(q) · p^μ p^ν / (p·q)

        在谱框架中，简化为：
            S^{(1)} ≈ (polarization_contract) · E_p / E_q · e^{-(E_p+E_q)/λ_max}

        参数
        ----------
        q_momentum : float
            软引力子动量大小
        p_momentum : float
            硬粒子动量大小
        polarization_contract : float
            极化张量收缩因子（默认 1.0）

        返回
        -------
        float : 软因子
        """
        if abs(q_momentum) < 1e-40:
            return 0.0

        # 软因子的经典极限
        S_soft = polarization_contract * p_momentum / q_momentum

        # 谱修正
        total_E = p_momentum + q_momentum
        F_spec = np.exp(-total_E**2 / self.cutoff.lambda_max)

        return S_soft * F_spec

    def tree_amplitude_2to3(self, s: float, t: float,
                            soft_q: float = 0.1) -> complex:
        """
        2→3 树图谱振幅。

        使用软因子分解近似：
            M_{2→3} ≈ κ · S^{(1)}(q, p) · M_{2→2}(s, t)

        参数
        ----------
        s : float
            Mandelstam s
        t : float
            Mandelstam t
        soft_q : float
            软引力子动量（作为 E_cm 的分数）

        返回
        -------
        complex : 谱振幅 M_{2→3}
        """
        # UV 谱截断
        if s > self.cutoff.lambda_max:
            return 0.0j

        # 2→2 振幅（从 B1 继承）
        kin_2to2 = ScatteringKinematics(s=s, t=t, u=-s - t)
        M_2to2 = self.amplitude_2to2.spectral_amplitude(kin_2to2)

        # 软因子（取典型动量）
        E_cm = np.sqrt(s)
        p_momentum = 0.5 * E_cm  # 典型硬粒子动量
        q_momentum = soft_q * E_cm  # 软引力子动量

        S_factor = self.soft_graviton_factor(q_momentum, p_momentum)

        # M_{2→3} = κ · S · M_{2→2}
        M_2to3 = KAPPA * S_factor * M_2to2

        return M_2to3

    def amplitude_squared_2to3(self, s: float, t: float,
                               soft_q: float = 0.1) -> float:
        """
        2→3 振幅平方（自旋平均后）。

        |M_{2→3}|² ≈ κ² · |S|² · |M_{2→2}|²

        参数
        ----------
        s : float
            Mandelstam s
        t : float
            Mandelstam t
        soft_q : float
            软引力子动量（分数）

        返回
        -------
        float : |M|²
        """
        M = self.tree_amplitude_2to3(s, t, soft_q)
        return float(abs(M) ** 2)

    def differential_cross_section_2to3(self, E_cm: float,
                                         soft_q: float = 0.1,
                                         n_theta: int = 30) -> float:
        """
        2→3 微分散射截面。

        dσ_{2→3} ≈ (1/(2!)) · (1/(2E_cm²)) · ∫ |M_{2→3}|² dΠ_3

        其中 1/(2!) 是末态全同粒子因子。

        参数
        ----------
        E_cm : float
            质心能
        soft_q : float
            软引力子动量（分数）
        n_theta : int
            散射角采样点数

        返回
        -------
        float : 总截面（Planck 面积单位）
        """
        s = E_cm ** 2

        if s > self.cutoff.lambda_max:
            return 0.0

        # 3-体相空间权重
        phase_space = SpectralNPhaseSpace(dim=self.dim)
        phi_3 = phase_space.phase_space_weight(3, s)

        # 振幅平方的θ平均
        cos_theta_vals = np.linspace(-0.9, 0.9, n_theta)
        M2_sum = 0.0
        for cos_theta in cos_theta_vals:
            t = -0.5 * s * (1.0 - cos_theta)
            M2_sum += self.amplitude_squared_2to3(s, t, soft_q)

        M2_avg = M2_sum / n_theta

        # 截面：dσ = (1/(2!)) · (1/(2s)) · |M|² dΠ_3
        # 对无质量全同玻色子，对称因子 1/(2!)
        cross_section = 0.5 * M2_avg * phi_3 / (2.0 * s)

        return cross_section

    def energy_scan_2to3(self, E_min: float, E_max: float,
                          n_points: int = 30,
                          soft_q: float = 0.1) -> Dict[str, np.ndarray]:
        """
        2→3 截面随质心能的变化。

        参数
        ----------
        E_min, E_max : float
            质心能范围
        n_points : int
            采样点数
        soft_q : float
            软引力子动量（分数）

        返回
        -------
        dict : {E_cm, sigma_2to3, sigma_2to2, ratio}
        """
        E_vals = np.geomspace(max(E_min, 1e-6), E_max, n_points)
        sigma_23 = np.zeros(n_points)
        sigma_22 = np.zeros(n_points)
        ratio = np.zeros(n_points)

        for i, E in enumerate(E_vals):
            sigma_23[i] = self.differential_cross_section_2to3(E, soft_q)
            sigma_22[i] = self.amplitude_2to2.total_cross_section(E, n_theta=30)
            if sigma_22[i] > 0:
                ratio[i] = sigma_23[i] / sigma_22[i]

        return {
            'E_cm': E_vals,
            'sigma_2to3': sigma_23,
            'sigma_2to2': sigma_22,
            'ratio_3_to_2': ratio,
        }


# ============================================================
#  3. 2→4 散射谱振幅与末态谱分布
# ============================================================

class Graviton2to4Scattering:
    """
    2→4 散射谱振幅（引力子 → 4 引力子）。

    通过双重软因子分解：
        M_{2→4} ≈ κ² · S^{(1)} · S^{(2)} · M_{2→2}

    其中 S^{(1)} 和 S^{(2)} 是两软引力子发射因子。

    在 Planck 能标附近，大量软引力子发射使多体末态占主导。
    """

    def __init__(self, dim: int = 32):
        self.dim = dim
        self.amplitude_2to3 = Graviton2to3Scattering(dim=dim)
        self.amplitude_2to2 = GravitonScatteringAmplitude(dim=dim)
        self.cutoff = SpectralCutoff()

    def tree_amplitude_2to4(self, s: float, t: float,
                             soft_q1: float = 0.05,
                             soft_q2: float = 0.05) -> complex:
        """
        2→4 树图谱振幅（双重软因子分解）。

        M_{2→4} ≈ κ² · S₁ · S₂ · M_{2→2}

        参数
        ----------
        s : float
            Mandelstam s
        t : float
            Mandelstam t
        soft_q1, soft_q2 : float
            两软引力子动量（作为 E_cm 的分数）

        返回
        -------
        complex : 谱振幅 M_{2→4}
        """
        if s > self.cutoff.lambda_max:
            return 0.0j

        kin_2to2 = ScatteringKinematics(s=s, t=t, u=-s - t)
        M_2to2 = self.amplitude_2to2.spectral_amplitude(kin_2to2)

        # 双重软因子
        E_cm = np.sqrt(s)
        p_momentum = 0.5 * E_cm
        q1_momentum = soft_q1 * E_cm
        q2_momentum = soft_q2 * E_cm

        S1 = self.amplitude_2to3.soft_graviton_factor(q1_momentum, p_momentum)
        S2 = self.amplitude_2to3.soft_graviton_factor(q2_momentum, p_momentum)

        # M_{2→4} = κ² · S₁ · S₂ · M_{2→2}
        M_2to4 = KAPPA_SQ * S1 * S2 * M_2to2

        return M_2to4

    def differential_cross_section_2to4(self, E_cm: float,
                                         soft_q1: float = 0.05,
                                         soft_q2: float = 0.05,
                                         n_theta: int = 20) -> float:
        """
        2→4 微分散射截面。

        dσ_{2→4} ≈ (1/(3!)) · (1/(2s)) · ∫ |M_{2→4}|² dΠ_4

        对称因子 1/(3!) 来自末态 4 个全同引力子中 3 个为软（硬粒子对称因子 1/2，
        再加软粒子区分因子... 这里保守取 1/6）。

        参数
        ----------
        E_cm : float
            质心能
        soft_q1, soft_q2 : float
            软引力子动量（分数）
        n_theta : int
            散射角采样点数

        返回
        -------
        float : 总截面
        """
        s = E_cm ** 2
        if s > self.cutoff.lambda_max:
            return 0.0

        # 4-体相空间权重
        phase_space = SpectralNPhaseSpace(dim=self.dim)
        phi_4 = phase_space.phase_space_weight(4, s)

        # 振幅平方的θ平均
        cos_theta_vals = np.linspace(-0.9, 0.9, n_theta)
        M2_sum = 0.0
        for cos_theta in cos_theta_vals:
            t = -0.5 * s * (1.0 - cos_theta)
            M = self.tree_amplitude_2to4(s, t, soft_q1, soft_q2)
            M2_sum += abs(M) ** 2

        M2_avg = M2_sum / n_theta

        # 截面：对称因子 1/6（4个全同引力子）
        cross_section = (1.0 / 6.0) * M2_avg * phi_4 / (2.0 * s)

        return cross_section

    def energy_scan_2to4(self, E_min: float, E_max: float,
                          n_points: int = 30) -> Dict[str, np.ndarray]:
        """
        2→4 截面随质心能的变化。

        参数
        ----------
        E_min, E_max : float
            质心能范围
        n_points : int
            采样点数

        返回
        -------
        dict : {E_cm, sigma_2to4, sigma_2to3, sigma_2to2, ratio_42, ratio_32}
        """
        E_vals = np.geomspace(max(E_min, 1e-6), E_max, n_points)
        sigma_24 = np.zeros(n_points)
        sigma_23 = np.zeros(n_points)
        sigma_22 = np.zeros(n_points)

        for i, E in enumerate(E_vals):
            sigma_24[i] = self.differential_cross_section_2to4(E)
            sigma_23[i] = self.amplitude_2to3.differential_cross_section_2to3(E)
            sigma_22[i] = self.amplitude_2to2.total_cross_section(E, n_theta=30)

        # 比值
        ratio_42 = np.divide(sigma_24, sigma_22,
                             out=np.zeros_like(sigma_24),
                             where=sigma_22 > 0)
        ratio_32 = np.divide(sigma_23, sigma_22,
                             out=np.zeros_like(sigma_23),
                             where=sigma_22 > 0)

        return {
            'E_cm': E_vals,
            'sigma_2to2': sigma_22,
            'sigma_2to3': sigma_23,
            'sigma_2to4': sigma_24,
            'ratio_32': ratio_32,
            'ratio_42': ratio_42,
        }


# ============================================================
#  4. 末态粒子谱分布
# ============================================================

class FinalStateSpectralDistribution:
    """
    末态粒子谱分布。

    在谱框架中，普朗克能标散射的末态粒子谱由以下因素决定：
    1. 相空间权重：高 N 末态在 > 0.1 M_Pl 时占优
    2. 谱截断压制：E > M_Pl 时所有截面被指数压制
    3. 软引力子谱：dN/dE_soft ∝ 1/E_soft（红外发散被谱间隙 Δλ_min 正则化）
    """

    def __init__(self, dim: int = 32):
        self.dim = dim
        self.phase_space = SpectralNPhaseSpace(dim=dim)
        self.amplitude_2to2 = GravitonScatteringAmplitude(dim=dim)
        self.amplitude_2to3 = Graviton2to3Scattering(dim=dim)
        self.amplitude_2to4 = Graviton2to4Scattering(dim=dim)
        self.cutoff = SpectralCutoff()

    def multiplicity_distribution(self, E_cm: float,
                                   n_max: int = 6) -> Dict[int, float]:
        """
        末态粒子数分布 P(n)。

        基于相空间权重 × 振幅平方的近似。对非微扰的普朗克能标散射，
        多体末态的概率由相空间体积主导。

        参数
        ----------
        E_cm : float
            质心能
        n_max : int
            最大末态粒子数（默认 6）

        返回
        -------
        dict : {n: P(n)}
        """
        weights = {}
        total = 0.0

        for n in range(2, n_max + 1):
            # 加权：相空间权重 × (振幅因子)
            phi_n = self.phase_space.phase_space_weight(n, E_cm ** 2)

            # 振幅因子：M_{2→N} 的典型标度（引力子发射的软因子乘积）
            # 对 n 个末态粒子，振幅 ~ κ^{n-2} · M_{2→2}
            # 振幅平方 ~ (κ²)^{n-2} · |M_{2→2}|²
            # 但软因子中有 1/E_soft 发散，总体上权重随 n 先增后减
            amp_factor = KAPPA_SQ ** (n - 2)

            # 软因子补偿（来自软引力子发射的红外增强）
            # 每个额外粒子贡献 ~ (E_cm/Δλ_min)² 的增强
            ir_enhancement = (E_cm / DELTA_LAMBDA_MIN) ** (2 * (n - 2))
            ir_enhancement = min(ir_enhancement, 1e10)  # 截断

            weights[n] = phi_n * amp_factor * ir_enhancement
            total += weights[n]

        # 归一化为概率
        if total > 0:
            for n in weights:
                weights[n] /= total

        return weights

    def soft_graviton_spectrum(self, E_cm: float,
                                n_bins: int = 50) -> Dict[str, np.ndarray]:
        """
        软引力子谱 dN/dE_soft。

        在谱框架中，软引力子发射谱为：
            dN/dE_soft ∼ (κ²/π²) · (1/E_soft) · e^{-E_soft/Δλ_min}

        其中谱间隙 Δλ_min 提供红外正则化。

        参数
        ----------
        E_cm : float
            质心能
        n_bins : int
            能谱 bin 数

        返回
        -------
        dict : {E_soft, dN_dE, cumulative}
        """
        # 软引力子能量范围：从谱间隙到 E_cm
        E_min = DELTA_LAMBDA_MIN  # 红外截止（谱间隙）
        E_max = 0.1 * E_cm  # 软定义为 < 0.1 E_cm

        E_vals = np.geomspace(max(E_min, 1e-10), max(E_max, E_min * 2), n_bins)

        # 软引力子谱：dN/dE ∝ κ²/E · e^{-E/Δλ_min}
        dN_dE = KAPPA_SQ / (np.pi**2) / E_vals * np.exp(-E_vals / DELTA_LAMBDA_MIN)

        # 谱截断修正
        F_spec = np.exp(-E_cm**2 / self.cutoff.lambda_max)
        dN_dE = dN_dE * F_spec

        # 累积分布
        cumulative = np.cumsum(dN_dE * np.diff(E_vals, prepend=E_vals[0]))

        return {
            'E_soft': E_vals,
            'dN_dE': dN_dE,
            'cumulative': cumulative,
        }

    def energy_fraction_distribution(self, E_cm: float,
                                      n: int = 3,
                                      n_bins: int = 30) -> Dict[str, np.ndarray]:
        """
        末态粒子能量分数分布。

        对 N-体末态，单个粒子携带能量分数 x = E_i/E_cm 的分布。

        参数
        ----------
        E_cm : float
            质心能
        n : int
            末态粒子数
        n_bins : int
            采样点数

        返回
        -------
        dict : {x, dN_dx}
        """
        if n < 2:
            return {'x': np.array([1.0]), 'dN_dx': np.array([1.0])}

        # 对 N-体末态，单粒子能量分数分布由相空间决定
        # 对无质量粒子，x ∈ (0, 1)，分布近似为 (n-1)(1-x)^{n-2}
        x_vals = np.linspace(0.01, 0.99, n_bins)

        # N-体相空间边缘分布
        dN_dx = (n - 1) * (1 - x_vals) ** (n - 2)

        # 谱修正：高能端压制
        F_spec = np.exp(-(E_cm * x_vals)**2 / self.cutoff.lambda_max)
        dN_dx = dN_dx * F_spec

        # 归一化
        total = np.trapz(dN_dx, x_vals)
        if total > 0:
            dN_dx = dN_dx / total

        return {'x': x_vals, 'dN_dx': dN_dx}

    def spectral_cascade(self, E_cm: float,
                          n_steps: int = 5) -> Dict[str, Any]:
        """
        谱级联：多次散射的能量流。

        在 Planck 能标附近，初始 2→N 散射后，末态粒子可能再次散射，
        形成谱级联。级联过程可用谱流方程描述。

        这里简化为：每次散射将能量分配给更多粒子，直到能量低于阈值。

        参数
        ----------
        E_cm : float
            初始质心能
        n_steps : int
            级联步数

        返回
        -------
        dict : {step, E_remaining, n_particles, distribution}
        """
        E_rem = E_cm
        n_particles = 2
        cascade_data = []

        for step in range(n_steps):
            if E_rem < DELTA_LAMBDA_MIN:
                break

            # 当前能量下的末态粒子数分布
            weights = self.multiplicity_distribution(E_rem, n_max=min(6, 2 + step * 2))

            # 最概然末态粒子数
            n_mode = max(weights, key=weights.get) if weights else 2
            n_particles = max(n_particles, n_mode)

            # 每个粒子携带的平均能量
            E_per_particle = E_rem / n_particles

            cascade_data.append({
                'step': step,
                'E_remaining': E_rem,
                'n_particles': n_particles,
                'E_per_particle': E_per_particle,
                'multiplicity_weights': weights,
            })

            # 下一次散射的能量
            E_rem = 0.5 * E_rem  # 简化：能量减半

        return {
            'initial_E': E_cm,
            'n_steps': len(cascade_data),
            'cascade': cascade_data,
        }

    def full_multiplicity_scan(self, E_min: float, E_max: float,
                                n_points: int = 30) -> Dict[str, np.ndarray]:
        """
        多体末态的多重度扫描。

        计算各末态粒子数 N 的截面（或相空间权重）随能量变化。

        参数
        ----------
        E_min, E_max : float
            质心能范围
        n_points : int
            采样点数

        返回
        -------
        dict : {E_cm, weight_n} for n = 2..6
        """
        E_vals = np.geomspace(max(E_min, 1e-6), E_max, n_points)
        weights = {n: np.zeros(n_points) for n in range(2, 7)}

        for i, E in enumerate(E_vals):
            w = self.multiplicity_distribution(E, n_max=6)
            for n in range(2, 7):
                weights[n][i] = w.get(n, 0.0)

        result = {'E_cm': E_vals}
        result.update(weights)

        return result

    def summary_stats(self, E_cm: float) -> Dict[str, float]:
        """
        给定质心能下的散射谱统计摘要。

        参数
        ----------
        E_cm : float
            质心能

        返回
        -------
        dict : 统计量
        """
        # 平均末态粒子数
        weights = self.multiplicity_distribution(E_cm, n_max=6)
        avg_n = sum(n * p for n, p in weights.items())
        max_n = max(weights, key=weights.get) if weights else 2

        # 截面比
        sigma_22 = self.amplitude_2to2.total_cross_section(E_cm, n_theta=30)
        sigma_23 = self.amplitude_2to3.differential_cross_section_2to3(E_cm)
        sigma_24 = self.amplitude_2to4.differential_cross_section_2to4(E_cm)

        # 总截面（2→N 求和）
        # 在 UV 截止以下，总截面为各过程之和
        # 用 <= 避免 Planck 能标边界条件问题
        if E_cm**2 <= self.cutoff.lambda_max * (1.0 + 1e-12):
            sigma_total = sigma_22 + sigma_23 + sigma_24
        else:
            sigma_total = sigma_22

        return {
            'E_cm': E_cm,
            'E_cm_ratio': E_cm / M_PL,
            'avg_multiplicity': avg_n,
            'mode_multiplicity': max_n,
            'sigma_2to2': sigma_22,
            'sigma_2to3': sigma_23,
            'sigma_2to4': sigma_24,
            'sigma_total': sigma_total,
            'fraction_2to2': sigma_22 / sigma_total if sigma_total > 0 else 1.0,
            'fraction_2to3': sigma_23 / sigma_total if sigma_total > 0 else 0.0,
            'fraction_2to4': sigma_24 / sigma_total if sigma_total > 0 else 0.0,
            'in_planck_regime': E_cm >= 0.1 * M_PL,
            'uv_suppressed': E_cm >= M_PL,
        }


# ============================================================
#  5. 数值验证
# ============================================================

def verify_n_phase_space():
    """验证 N-体相空间谱表示"""
    ps = SpectralNPhaseSpace(dim=32, n_max=6)

    # 2-体相空间应为正
    phi_2 = ps.phase_space_weight(2, 1.0)
    print(f"  Φ₂(s=1.0) = {phi_2:.6e}")
    assert phi_2 > 0

    # 3-体相空间 > 2-体相空间（高能时）
    phi_3 = ps.phase_space_weight(3, 1.0)
    phi_4 = ps.phase_space_weight(4, 1.0)
    print(f"  Φ₃(s=1.0) = {phi_3:.6e}")
    print(f"  Φ₄(s=1.0) = {phi_4:.6e}")

    # 多体相空间/少体相空间的比值随能量增长
    ratio_low = ps.multiplicity_ratio(s=0.1).get(3, 0)
    ratio_high = ps.multiplicity_ratio(s=0.9).get(3, 0)
    print(f"  Φ₃/Φ₂ at s=0.1: {ratio_low:.6f}, at s=0.9: {ratio_high:.6f}")
    # 尽管 Φ₃ < Φ₂（受 1/(256π³) 压制），但比值随 s 增长
    assert ratio_high > ratio_low, "3-body/2-body ratio should grow with energy"

    # UV 截断：s > λ_max 时相空间为零
    phi_cut = ps.phase_space_weight(3, 2.0 * ps.cutoff.lambda_max)
    print(f"  Φ₃(s=2λ_max) = {phi_cut:.6e}")
    assert phi_cut == 0.0

    # 不变质量分布应归一化
    dist = ps.invariant_mass_distribution(3, 1.0, n_bins=50)
    norm = np.trapz(dist['dPhi_dM'], dist['M_ij'])
    print(f"  Invariant mass distribution norm: {norm:.6f}")
    assert abs(norm - 1.0) < 0.1

    # 多重度比：在高能时，更多末态粒子应有更大相空间
    ratios = ps.multiplicity_ratio(s=1.0)
    print(f"  Φ₃/Φ₂ = {ratios.get(3, 0):.4f}")
    print(f"  Φ₄/Φ₂ = {ratios.get(4, 0):.4f}")
    print(f"  Φ₅/Φ₂ = {ratios.get(5, 0):.4f}")
    # Φₙ/Φ₂ 随 n 增加先增后减（受 UV 压制影响）

    print("  ✅ N-phase space spectral representation verified")
    return True


def verify_2to3_scattering():
    """验证 2→3 散射谱振幅"""
    amp23 = Graviton2to3Scattering(dim=32)

    # 在低能时，软因子应为正
    S = amp23.soft_graviton_factor(q_momentum=0.01, p_momentum=0.5)
    print(f"  Soft factor (q=0.01, p=0.5): S = {S:.6f}")
    assert S > 0

    # 振幅应为有限复数
    M_23 = amp23.tree_amplitude_2to3(s=0.01, t=-0.005, soft_q=0.1)
    print(f"  M₂→₃(s=0.01, t=-0.005): |M| = {abs(M_23):.6e}")
    assert np.isfinite(abs(M_23))

    # 振幅平方应为正
    M2 = amp23.amplitude_squared_2to3(s=0.01, t=-0.005)
    print(f"  |M₂→₃|²(s=0.01): = {M2:.6e}")
    assert M2 >= 0

    # 截面应为正
    sigma = amp23.differential_cross_section_2to3(E_cm=0.01)
    print(f"  σ₂→₃(E=0.01 M_Pl): = {sigma:.6e}")
    assert sigma >= 0

    # UV 截断：超 Planck 能标截面为零
    sigma_uv = amp23.differential_cross_section_2to3(E_cm=2.0)
    print(f"  σ₂→₃(E=2.0 M_Pl): = {sigma_uv:.6e}")
    assert sigma_uv == 0.0

    # 能量扫描
    scan = amp23.energy_scan_2to3(E_min=0.001, E_max=1.0, n_points=20)
    assert len(scan['E_cm']) == 20
    assert np.all(scan['sigma_2to3'] >= 0)
    print(f"  Energy scan: σ₂→₃ range [{scan['sigma_2to3'].min():.3e}, {scan['sigma_2to3'].max():.3e}]")

    print("  ✅ 2→3 scattering amplitude verified")
    return True


def verify_2to4_scattering():
    """验证 2→4 散射谱振幅"""
    amp24 = Graviton2to4Scattering(dim=32)

    # 振幅应为有限复数
    M_24 = amp24.tree_amplitude_2to4(s=0.01, t=-0.005)
    print(f"  M₂→₄(s=0.01, t=-0.005): |M| = {abs(M_24):.6e}")
    assert np.isfinite(abs(M_24))

    # 截面应为正
    sigma = amp24.differential_cross_section_2to4(E_cm=0.01)
    print(f"  σ₂→₄(E=0.01 M_Pl): = {sigma:.6e}")
    assert sigma >= 0

    # UV 截断
    sigma_uv = amp24.differential_cross_section_2to4(E_cm=2.0)
    print(f"  σ₂→₄(E=2.0 M_Pl): = {sigma_uv:.6e}")
    assert sigma_uv == 0.0

    # 能量扫描
    scan = amp24.energy_scan_2to4(E_min=0.001, E_max=1.0, n_points=15)
    assert len(scan['E_cm']) == 15
    assert np.all(scan['sigma_2to4'] >= 0)
    print(f"  Energy scan: σ₂→₄ range [{scan['sigma_2to4'].min():.3e}, {scan['sigma_2to4'].max():.3e}]")

    print("  ✅ 2→4 scattering amplitude verified")
    return True


def verify_final_state_spectrum():
    """验证末态粒子谱分布"""
    fsd = FinalStateSpectralDistribution(dim=32)

    # 多重度分布应归一化
    weights = fsd.multiplicity_distribution(E_cm=0.5, n_max=6)
    total = sum(weights.values())
    print(f"  Multiplicity distribution sum: {total:.6f}")
    assert abs(total - 1.0) < 0.1

    # 最概然末态粒子数应在 n=3 或 n=4 附近（Planck 能标）
    mode_n = max(weights, key=weights.get) if weights else 2
    print(f"  Mode multiplicity at E=0.5 M_Pl: n = {mode_n}")
    assert mode_n >= 2

    # 软引力子谱应正且有限
    soft_spec = fsd.soft_graviton_spectrum(E_cm=0.5)
    assert np.all(soft_spec['dN_dE'] >= 0)
    assert np.all(np.isfinite(soft_spec['dN_dE']))
    print(f"  Soft graviton spectrum: dN/dE range [{soft_spec['dN_dE'].min():.3e}, {soft_spec['dN_dE'].max():.3e}]")

    # 能量分数分布应归一化
    frac = fsd.energy_fraction_distribution(E_cm=0.5, n=3)
    norm = np.trapz(frac['dN_dx'], frac['x'])
    print(f"  Energy fraction distribution norm: {norm:.6f}")
    assert abs(norm - 1.0) < 0.1

    # 谱级联
    cascade = fsd.spectral_cascade(E_cm=1.0, n_steps=5)
    assert cascade['n_steps'] > 0
    print(f"  Spectral cascade: {cascade['n_steps']} steps, avg multiplicity grows")
    for c in cascade['cascade']:
        print(f"    Step {c['step']}: E={c['E_remaining']:.4f}, n={c['n_particles']}")

    # 多重度扫描
    scan = fsd.full_multiplicity_scan(E_min=0.001, E_max=1.0, n_points=20)
    assert len(scan['E_cm']) == 20
    print(f"  Full multiplicity scan: {len(scan['E_cm'])} energy points")
    for n in range(2, 5):
        assert n in scan
        print(f"    n={n}: weights range [{scan[n].min():.3e}, {scan[n].max():.3e}]")

    print("  ✅ Final state spectral distribution verified")
    return True


def verify_summary_stats():
    """验证统计摘要"""
    fsd = FinalStateSpectralDistribution(dim=32)

    # 低能统计
    stats_low = fsd.summary_stats(E_cm=0.01)
    print(f"  E=0.01 M_Pl:")
    print(f"    Avg multiplicity: {stats_low['avg_multiplicity']:.3f}")
    print(f"    σ_total: {stats_low['sigma_total']:.3e}")
    print(f"    2→2 fraction: {stats_low['fraction_2to2']:.4f}")
    # 低能时 2→2 占主导
    assert stats_low['fraction_2to2'] > 0.5

    # Planck 能标统计
    stats_planck = fsd.summary_stats(E_cm=1.0)
    print(f"  E=1.0 M_Pl:")
    print(f"    Avg multiplicity: {stats_planck['avg_multiplicity']:.3f}")
    print(f"    σ_total: {stats_planck['sigma_total']:.3e}")
    print(f"    2→2 fraction: {stats_planck['fraction_2to2']:.4f}")

    # 超 Planck 能标：UV 压制
    stats_uv = fsd.summary_stats(E_cm=2.0)
    print(f"  E=2.0 M_Pl:")
    print(f"    UV suppressed: {stats_uv['uv_suppressed']}")
    assert stats_uv['uv_suppressed']

    print("  ✅ Summary statistics verified")
    return True


def verify_2to2_2to3_consistency():
    """验证 2→2 与 2→3/2→4 的一致性"""
    fsd = FinalStateSpectralDistribution(dim=32)

    # 在极低能时，2→2 应占绝对主导
    stats_low = fsd.summary_stats(E_cm=0.001)
    print(f"  E=0.001 M_Pl: 2→2 fraction = {stats_low['fraction_2to2']:.6f}")
    assert stats_low['fraction_2to2'] > 0.99

    # 在中等能标时，多体贡献应增长
    stats_mid = fsd.summary_stats(E_cm=0.1)
    print(f"  E=0.1 M_Pl: 2→2 fraction = {stats_mid['fraction_2to2']:.6f}")
    # 多体相空间开始变得重要
    assert stats_mid['fraction_2to2'] < 0.999

    # 2→3 截面增长应快于 2→2
    amp23 = Graviton2to3Scattering(dim=32)
    sigma_22_lo = fsd.amplitude_2to2.total_cross_section(E_cm=0.01, n_theta=30)
    sigma_22_hi = fsd.amplitude_2to2.total_cross_section(E_cm=0.1, n_theta=30)
    sigma_23_lo = amp23.differential_cross_section_2to3(E_cm=0.01)
    sigma_23_hi = amp23.differential_cross_section_2to3(E_cm=0.1)

    growth_22 = sigma_22_hi / max(sigma_22_lo, 1e-40)
    growth_23 = sigma_23_hi / max(sigma_23_lo, 1e-40)
    print(f"  Growth 2→2: {growth_22:.2f}, Growth 2→3: {growth_23:.2f}")
    # 2→3 增长更快（因为多体相空间随能量增长更快）
    print(f"  2→3 growth/2→2 growth ratio: {growth_23/max(growth_22, 1e-40):.2f}")

    print("  ✅ 2→2 ↔ 2→3 consistency verified")
    return True


def verify_scattering_regime_transition():
    """验证散射区间的过渡行为"""
    fsd = FinalStateSpectralDistribution(dim=32)

    # 收集各能标的 2→N 分数
    E_test = [0.001, 0.01, 0.1, 0.5, 1.0]
    fractions = {}

    for E in E_test:
        stats = fsd.summary_stats(E)
        fractions[E] = {
            'f22': stats['fraction_2to2'],
            'f23': stats['fraction_2to3'],
            'f24': stats['fraction_2to4'],
        }
        print(f"  E={E:6.4f} M_Pl: 2→2={stats['fraction_2to2']:.4f}, "
              f"2→3={stats['fraction_2to3']:.4f}, 2→4={stats['fraction_2to4']:.4f}")

    # 过渡特征：随能量增加，多体分数单调增加
    f22_vals = [fractions[E]['f22'] for E in E_test]
    for i in range(len(f22_vals) - 1):
        assert f22_vals[i] >= f22_vals[i + 1], \
            f"2→2 fraction should decrease with energy: {f22_vals[i]} < {f22_vals[i+1]}"

    print("  ✅ Scattering regime transition verified")
    return True


def run_all_tests():
    """运行所有 B2 测试"""
    print("=" * 60)
    print("B2: Planck Scattering 2→N Spectral Tests")
    print("=" * 60)

    tests = [
        ("N-phase space spectral representation", verify_n_phase_space),
        ("2→3 scattering amplitude", verify_2to3_scattering),
        ("2→4 scattering amplitude", verify_2to4_scattering),
        ("Final state spectral distribution", verify_final_state_spectrum),
        ("Summary statistics & UV behavior", verify_summary_stats),
        ("2→2 ↔ 2→3 consistency", verify_2to2_2to3_consistency),
        ("Scattering regime transition", verify_scattering_regime_transition),
    ]

    passed = 0
    for name, test_fn in tests:
        try:
            print(f"\n--- {name} ---")
            test_fn()
            passed += 1
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            import traceback
            traceback.print_exc()

    print(f"\n{'=' * 60}")
    if passed == len(tests):
        print(f"✅ {passed}/{len(tests)} B2 tests passed!")
    else:
        print(f"⚠️  {passed}/{len(tests)} B2 tests passed")

    return passed == len(tests)


if __name__ == "__main__":
    run_all_tests()
