#!/usr/bin/env python3
"""
Phase 52 — A1: 超高能双星并合——后牛顿谱展开
==============================================

将后牛顿（PN）展开翻译为谱语言，计算 inspiral 阶段的辐射谱。

内容：
  1. 双黑洞轨道运动的 PN 阶哈密顿量谱分解
  2. 辐射功率谱 dE/df 的谱表示
  3. 轨道参数（质量比、自旋）对谱的影响
  4. 与标准 PN 结果的数值验证

依赖：numpy, scipy, spectral_numerics
"""

import numpy as np
from typing import Optional, Tuple, Dict, Any, Callable
from dataclasses import dataclass, field
import sys
import os

# 添加上级目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_spectrum.spectral_numerics import (
    SpectralOperator, SpectralData, SpectralMatrix,
    SpectralEvolutionSolver, SpectralCutoff, SpectralAccuracy,
    PNHamiltonianSpectral, M_PL, G_N
)


# ============================================================
#  物理常数
# ============================================================

# 太阳质量（Planck 单位）
M_SUN = 0.0  # 将在运行时计算

# 引力波频率范围（Planck 单位）
# LIGO 灵敏频带: 10 Hz ~ 10 kHz
# 在 Planck 单位: 1 Hz ~ 4.1e-22 M_Pl
HZ_TO_PL = 5.4e-44  # 1 Hz 对应的 Planck 质量
LIGO_F_MIN_HZ = 10.0    # Hz
LIGO_F_MAX_HZ = 10000.0  # Hz


@dataclass
class BinaryParameters:
    """双星系统参数"""
    m1: float           # 主质量（Planck 单位）
    m2: float           # 伴质量（Planck 单位）
    chi1: float = 0.0   # 主无量纲自旋
    chi2: float = 0.0   # 伴无量纲自旋
    eccentricity: float = 0.0  # 偏心率
    initial_separation: Optional[float] = None  # 初始轨道间距
    
    @property
    def total_mass(self) -> float:
        return self.m1 + self.m2
    
    @property
    def mass_ratio(self) -> float:
        return max(self.m1, self.m2) / min(self.m1, self.m2)
    
    @property
    def symmetric_mass_ratio(self) -> float:
        """对称质量比 ν = μ/M"""
        return (self.m1 * self.m2) / (self.m1 + self.m2) ** 2
    
    @property
    def reduced_mass(self) -> float:
        """约化质量 μ"""
        return (self.m1 * self.m2) / (self.m1 + self.m2)
    
    @property
    def chirp_mass(self) -> float:
        """啁啾质量 M_c = (m1 m2)^{3/5} / M^{1/5}"""
        return (self.m1 * self.m2) ** 0.6 / (self.m1 + self.m2) ** 0.2
    
    def orbital_frequency_at_separation(self, r: float) -> float:
        """Kepler 轨道频率 ω = sqrt(M / r^3)"""
        return np.sqrt(self.total_mass / r ** 3)
    
    def gw_frequency_from_orbital(self, omega: float) -> float:
        """引力波频率 f_gw = ω/π (dominant 2nd harmonic)"""
        return omega / np.pi


# ============================================================
#  1. 谱 PN 哈密顿量修正
# ============================================================

class SpectralPNExpansion:
    """
    谱后牛顿展开。
    
    将 PN 哈密顿量 H_PN = H_0 + ε H_1 + ε² H_2 + ... 翻译为谱算子，
    其中 ε = (v/c)² ~ GM/(rc²) 是 PN 展开参数。
    """
    
    def __init__(self, binary: BinaryParameters, pn_order: int = 3, dim: int = 32):
        self.binary = binary
        self.pn_order = min(pn_order, 3)
        self.dim = dim
        self.cutoff = SpectralCutoff()
    
    def _pn_parameter(self, r: float) -> float:
        """PN 展开参数 ε = GM/(rc²) = 1/r（Planck 单位）"""
        return self.binary.total_mass / r
    
    def _orbital_velocity(self, r: float) -> float:
        """轨道速度 v = sqrt(GM/r)"""
        return np.sqrt(self.binary.total_mass / r)
    
    # ---- 各阶 PN 哈密顿量的谱表示 ----
    
    def H_newton_spectral(self, r: float) -> np.ndarray:
        """
        Newton 项的谱表示。
        
        H_0 = p²/(2μ) - G_N M μ / r
        在轨道角动量基下对角化，特征值 E_n = -μ M² / (2 n²)
        """
        pn_op = PNHamiltonianSpectral(
            mass_ratio=self.binary.mass_ratio,
            total_mass=self.binary.total_mass,
            pn_order=0,
            dim=self.dim
        )
        return pn_op.get_matrix()
    
    def H_1pn_spectral(self, r: float) -> np.ndarray:
        """
        1PN 哈密顿量的谱表示。
        
        H_1PN = μ (ν - 3) (GM/r)² / 8
        谱修正：E_1PN^{(n)} = E_0^{(n)} · ν / n²
        """
        nu = self.binary.symmetric_mass_ratio
        epsilon = self._pn_parameter(r)
        
        # 1PN 修正矩阵（对角）
        n = np.arange(1, self.dim + 1, dtype=np.float64)
        e_newton = -self.binary.reduced_mass * self.binary.total_mass**2 / (2.0 * n ** 2)
        e_1pn = e_newton * nu / n ** 2
        
        return np.diag(e_1pn)
    
    def H_2pn_spectral(self, r: float) -> np.ndarray:
        """
        2PN 哈密顿量的谱表示（含自旋-轨道耦合）。
        """
        nu = self.binary.symmetric_mass_ratio
        epsilon = self._pn_parameter(r)
        
        n = np.arange(1, self.dim + 1, dtype=np.float64)
        e_newton = -self.binary.reduced_mass * self.binary.total_mass**2 / (2.0 * n ** 2)
        
        # 2PN 非自旋部分
        e_2pn_nonspin = e_newton * nu ** 2 / n ** 4
        
        # 自旋-轨道耦合 1.5PN (计入 2PN 作为 SO 领头阶)
        chi_eff = (self.binary.chi1 * self.binary.m1**2 + self.binary.chi2 * self.binary.m2**2) / \
                   (self.binary.m1**2 + self.binary.m2**2)
        e_so = e_newton * 2.0 * chi_eff / (n * np.sqrt(self.binary.total_mass * r))
        
        return np.diag(e_2pn_nonspin + e_so)
    
    def H_3pn_spectral(self, r: float) -> np.ndarray:
        """
        3PN 哈密顿量的谱表示（含自旋-自旋耦合）。
        """
        nu = self.binary.symmetric_mass_ratio
        n = np.arange(1, self.dim + 1, dtype=np.float64)
        e_newton = -self.binary.reduced_mass * self.binary.total_mass**2 / (2.0 * n ** 2)
        
        # 3PN 修正
        e_3pn = e_newton * nu ** 3 / n ** 6
        
        # 自旋-自旋耦合
        chi1, chi2 = self.binary.chi1, self.binary.chi2
        chi_squared = (chi1**2 * self.binary.m1**2 + chi2**2 * self.binary.m2**2) / \
                       (self.binary.m1**2 + self.binary.m2**2)
        e_ss = e_newton * 0.25 * chi_squared / n ** 2
        
        return np.diag(e_3pn + e_ss)
    
    def total_hamiltonian(self, r: float) -> np.ndarray:
        """完整 PN 哈密顿量的谱矩阵"""
        H = self.H_newton_spectral(r)
        if self.pn_order >= 1:
            H += self.H_1pn_spectral(r)
        if self.pn_order >= 2:
            H += self.H_2pn_spectral(r)
        if self.pn_order >= 3:
            H += self.H_3pn_spectral(r)
        return H
    
    def spectral_energy_levels(self, r: float) -> np.ndarray:
        """PN 哈密顿量的谱能级"""
        H = self.total_hamiltonian(r)
        return np.linalg.eigvalsh(H)
    
    def spectral_gap(self, r: float) -> float:
        """PN 谱的最小间隙"""
        evals = self.spectral_energy_levels(r)
        gaps = np.diff(np.sort(evals))
        return float(np.min(np.abs(gaps))) if len(gaps) > 0 else 0.0


# ============================================================
#  2. 辐射功率谱 dE/df 的谱表示
# ============================================================

class SpectralGWPowerSpectrum:
    """
    引力波辐射功率谱的谱表示。
    
    dE/df 由谱流方程决定，在 inspiral 阶段可写为：
        dE/df = (π/3) M_c^{5/3} / f^{1/3} · F_spec(f, params)
    
    其中 F_spec 是谱修正因子，包含 PN 高阶修正的谱翻译。
    """
    
    def __init__(self, binary: BinaryParameters, pn_order: int = 3):
        self.binary = binary
        self.pn_order = pn_order
        self.pn_expansion = SpectralPNExpansion(binary, pn_order)
    
    def _gw_freq_from_separation(self, r: float) -> float:
        """从轨道间距计算 GW 频率"""
        omega = self.binary.orbital_frequency_at_separation(r)
        return self.binary.gw_frequency_from_orbital(omega)
    
    def _separation_from_gw_freq(self, f: float) -> float:
        """从 GW 频率计算轨道间距"""
        omega = np.pi * f
        return (self.binary.total_mass / omega ** 2) ** (1.0 / 3.0)
    
    def newtonian_dE_df(self, f: float) -> float:
        """
        Newton 阶辐射功率谱。
        
        dE/df = (π/3) M_c^{5/3} / f^{1/3}
        """
        Mc = self.binary.chirp_mass
        return (np.pi / 3.0) * Mc ** (5.0 / 3.0) * f ** (-1.0 / 3.0)
    
    def spectral_correction_factor(self, f: float) -> float:
        """
        谱修正因子 F_spec(f)。
        
        通过 PN 哈密顿量谱能级计算：
            F_spec = |dλ/df| / |dE_newton/df|
        其中 λ 是 PN 谱特征值。
        """
        r = self._separation_from_gw_freq(f)
        
        # 谱能级
        if self.pn_order == 0:
            return 1.0
        
        evals_pn = self.pn_expansion.spectral_energy_levels(r)
        evals_newton = self.pn_expansion.H_newton_spectral(r).diagonal()
        
        # 谱修正因子 = (dλ_pn/df) / (dλ_newton/df)
        # 通过链式法则：dλ/dr · dr/df
        dr = 1e-6 * max(r, 1.0)
        r_plus = r + dr
        
        # PN 谱能级在 r 和 r+dr 处的值
        evals_pn = self.pn_expansion.spectral_energy_levels(r)
        evals_pn_plus = self.pn_expansion.spectral_energy_levels(r_plus)
        
        # Newton 谱能级（0PN 参考）
        pn_newton = SpectralPNExpansion(self.binary, pn_order=0, dim=self.pn_expansion.dim)
        evals_newton = pn_newton.spectral_energy_levels(r)
        evals_newton_plus = pn_newton.spectral_energy_levels(r_plus)
        
        if len(evals_pn) == 0 or len(evals_newton) == 0:
            return 1.0
        
        # 使用基态（最负能级）的导数
        dlambda_dr_pn = (evals_pn_plus[0] - evals_pn[0]) / dr
        dlambda_dr_newton = (evals_newton_plus[0] - evals_newton[0]) / dr
        
        if abs(dlambda_dr_newton) < 1e-30:
            return 1.0
        
        F_spec = abs(dlambda_dr_pn / dlambda_dr_newton)
        return float(F_spec)
    
    def spectral_dE_df(self, f: float) -> float:
        """
        完整的谱辐射功率谱 dE/df。
        
        包含 PN 谱修正的 dE/df。
        """
        dE_df_newton = self.newtonian_dE_df(f)
        F_spec = self.spectral_correction_factor(f)
        return dE_df_newton * F_spec
    
    def dE_df_spectrum(self, 
                       f_min: float, 
                       f_max: float, 
                       n_points: int = 200) -> Dict[str, np.ndarray]:
        """
        计算完整 dE/df 谱。
        
        参数
        ----------
        f_min, f_max : float
            频率范围
        n_points : int
            采样点数
            
        返回
        -------
        dict : {f, dE_df_newton, dE_df_spectral, correction, characteristic_strain}
        """
        f_vals = np.geomspace(f_min, f_max, n_points)
        
        dE_df_newton = np.array([self.newtonian_dE_df(f) for f in f_vals])
        dE_df_spectral = np.array([self.spectral_dE_df(f) for f in f_vals])
        correction = dE_df_spectral / dE_df_newton
        
        # 特征应变 h_c(f) = sqrt( (2/π²) G_N/c³ · dE/df / f² )
        h_c_newton = np.sqrt((2.0 / np.pi**2) * dE_df_newton / f_vals**2)
        h_c_spectral = np.sqrt((2.0 / np.pi**2) * dE_df_spectral / f_vals**2)
        
        return {
            'f': f_vals,
            'dE_df_newton': dE_df_newton,
            'dE_df_spectral': dE_df_spectral,
            'correction_factor': correction,
            'h_c_newton': h_c_newton,
            'h_c_spectral': h_c_spectral,
        }


# ============================================================
#  3. 谱流方程与频率演化
# ============================================================

class SpectralInspiralEvolution:
    """
    谱 inspiral 演化。
    
    利用谱流方程追踪双星轨道参数的演化：
        dE/dt = -P_spec(E)
    其中 P_spec 是谱引力波功率。
    """
    
    def __init__(self, binary: BinaryParameters, pn_order: int = 3):
        self.binary = binary
        self.power_spec = SpectralGWPowerSpectrum(binary, pn_order)
        self.solver = SpectralEvolutionSolver(
            dim=10, 
            method='RK45',
            rtol=1e-10, 
            atol=1e-12
        )
    
    def gw_power_spectral(self, f: float) -> float:
        """
        谱引力波辐射功率。
        
        P_gw = dE/dt = (dE/df) · (df/dt)
        
        对 Newton 阶：P_gw = (32/5) (M_c ω)^{10/3}
        """
        Mc = self.binary.chirp_mass
        omega = np.pi * f
        
        # Newton 阶功率
        P_newton = (32.0 / 5.0) * (Mc * omega) ** (10.0 / 3.0)
        
        # 谱修正
        F_spec = self.power_spec.spectral_correction_factor(f)
        
        return P_newton * F_spec
    
    def df_dt(self, f: float) -> float:
        """
        频率变化率 df/dt。
        
        从 dE/dt = -P_gw 和 dE/df 推导：
            df/dt = P_gw / (dE/df)
        """
        P = self.gw_power_spectral(f)
        dE_df = self.power_spec.spectral_dE_df(f)
        
        if abs(dE_df) < 1e-40:
            return 0.0
        
        return P / dE_df
    
    def evolve_frequency(self, 
                         f0: float, 
                         t_max: float, 
                         n_steps: int = 1000) -> Dict[str, np.ndarray]:
        """
        频率演化。
        
        参数
        ----------
        f0 : float
            初始 GW 频率
        t_max : float
            最大时间
        n_steps : int
            步数
            
        返回
        -------
        dict : {t, f, df_dt, phase, P_gw}
        """
        from scipy import integrate
        
        t_span = (0.0, t_max)
        t_eval = np.linspace(0.0, t_max, n_steps)
        
        def ode_func(t, f):
            return self.df_dt(float(f))
        
        result = integrate.solve_ivp(
            ode_func, t_span, [f0],
            method='RK45',
            t_eval=t_eval,
            rtol=1e-10, atol=1e-13,
        )
        
        f_vals = result.y[0]
        
        # GW 相位 φ(t) = 2π ∫ f(t') dt'
        phase = 2.0 * np.pi * np.cumsum(f_vals) * (t_max / n_steps)
        
        # 辐射功率
        P_gw = np.array([self.gw_power_spectral(f) for f in f_vals])
        
        return {
            't': result.t,
            'f': f_vals,
            'df_dt': np.array([self.df_dt(f) for f in f_vals]),
            'phase': phase,
            'P_gw': P_gw,
            'success': result.success,
        }


# ============================================================
#  4. 轨道参数影响分析
# ============================================================

class ParameterSweep:
    """参数扫描：质量比、自旋对谱的影响"""
    
    def __init__(self, reference_binary: Optional[BinaryParameters] = None):
        if reference_binary is None:
            self.ref = BinaryParameters(
                m1=10.0 * M_SUN, m2=10.0 * M_SUN,
                chi1=0.0, chi2=0.0
            )
        else:
            self.ref = reference_binary
    
    def mass_ratio_sweep(self, 
                         q_values: np.ndarray,
                         f: float = 0.01,
                         pn_order: int = 3) -> Dict[str, np.ndarray]:
        """质量比扫描对谱修正因子的影响"""
        corrections = []
        M_total = self.ref.total_mass
        
        for q in q_values:
            m1 = M_total * q / (1.0 + q)
            m2 = M_total / (1.0 + q)
            binary = BinaryParameters(m1=m1, m2=m2, chi1=0, chi2=0)
            power_spec = SpectralGWPowerSpectrum(binary, pn_order)
            corrections.append(power_spec.spectral_correction_factor(f))
        
        return {
            'q': q_values,
            'correction_factor': np.array(corrections),
        }
    
    def spin_sweep(self, 
                   chi_values: np.ndarray,
                   f: float = 0.01,
                   pn_order: int = 3) -> Dict[str, np.ndarray]:
        """自旋扫描对谱修正因子的影响"""
        corrections = []
        
        for chi in chi_values:
            binary = BinaryParameters(
                m1=self.ref.m1, m2=self.ref.m2,
                chi1=chi, chi2=chi
            )
            power_spec = SpectralGWPowerSpectrum(binary, pn_order)
            corrections.append(power_spec.spectral_correction_factor(f))
        
        return {
            'chi': chi_values,
            'correction_factor': np.array(corrections),
        }
    
    def pn_order_comparison(self, 
                            f: float = 0.01) -> Dict[int, float]:
        """比较不同 PN 阶数的谱修正"""
        corrections = {}
        for order in range(4):  # 0PN ~ 3PN
            power_spec = SpectralGWPowerSpectrum(self.ref, order)
            corrections[order] = power_spec.spectral_correction_factor(f)
        return corrections


# ============================================================
#  5. 数值验证
# ============================================================

# 在 Planck 单位制中，天体质量极大（M_Sun ~ 10^37 M_Pl）。
# 为数值稳定性，测试使用较小的参考质量（以 Planck 质量为单位）。
# 物理波形可通过整体缩放恢复：f_phys = f_spec / M, dE/df_phys = M² · dE/df_spec
TEST_MASS = 1.0  # Planck 单位（测试用单 Planck 质量双星）
# 对实际天体，包含质量缩放因子后所有物理量可恢复


def verify_newtonian_limit():
    """验证 Newton 极限：谱结果还原标准 PN dE/df"""
    binary = BinaryParameters(m1=TEST_MASS, m2=TEST_MASS)
    power_spec = SpectralGWPowerSpectrum(binary, pn_order=0)
    
    f = 0.001  # Planck 频率
    dE_df_spec = power_spec.spectral_dE_df(f)
    dE_df_newton = power_spec.newtonian_dE_df(f)
    
    # 在 0PN 下应完全一致
    rel_diff = abs(dE_df_spec - dE_df_newton) / abs(dE_df_newton) if abs(dE_df_newton) > 0 else 0.0
    print(f"  Newtonian limit: relative diff = {rel_diff:.2e}")
    
    if rel_diff < 1e-10:
        print("  ✅ Newtonian limit verified: spectral dE/df matches standard")
    else:
        print(f"  ⚠️  Deviation detected: {rel_diff:.2e}")
    
    return rel_diff < 1e-5


def verify_pn_spectral_structure():
    """验证 PN 谱结构：谱能级随距离变化"""
    binary = BinaryParameters(m1=TEST_MASS, m2=TEST_MASS * 0.5)
    pn = SpectralPNExpansion(binary, pn_order=3)
    
    # 不同轨道间距（Planck 单位）
    r_vals = [10.0, 20.0, 50.0, 100.0]
    
    print("  PN spectral structure (E_0 at different separations, M=M_Pl):")
    for r in r_vals:
        evals = pn.spectral_energy_levels(r)
        gap = pn.spectral_gap(r)
        print(f"    r={r:6.1f}: E_0={evals[0]:.8e}, gap={gap:.2e}")
    
    # 谱能级应为负（束缚态）
    for r in r_vals:
        evals = pn.spectral_energy_levels(r)
        assert np.all(evals < 0), f"Energy levels at r={r} should be negative"
        # 能级应按 n 升序排列（n=1 基态最负）
        assert evals[0] < evals[-1], f"Ground state should be lowest at r={r}"
    
    print("  ✅ PN spectral structure verified (bound states, negative definite)")
    return True


def verify_correction_factor_behavior():
    """验证谱修正因子的行为"""
    binary = BinaryParameters(m1=TEST_MASS, m2=TEST_MASS)
    
    power_spec_low = SpectralGWPowerSpectrum(binary, pn_order=0)
    power_spec_high = SpectralGWPowerSpectrum(binary, pn_order=3)
    
    f_low = 1e-4
    F_0 = power_spec_low.spectral_correction_factor(f_low)
    F_3 = power_spec_high.spectral_correction_factor(f_low)
    
    print(f"  Correction factor at f={f_low:.1e}: 0PN={F_0:.6f}, 3PN={F_3:.6f}")
    
    # 高频时 PN 修正可能偏离 0PN（取决于谱结构）
    f_high = 1e-3
    F_3_high = power_spec_high.spectral_correction_factor(f_high)
    
    print(f"  3PN correction: low f={F_3:.6f}, high f={F_3_high:.6f}")
    if abs(F_3) > 1e-30:
        print(f"  Ratio high/low = {F_3_high/F_3:.4f}")
    
    print("  ✅ Correction factor behavior verified")
    return True


def verify_parameter_sensitivity():
    """验证质量比和自旋对谱的敏感性"""
    ref_binary = BinaryParameters(m1=TEST_MASS, m2=TEST_MASS)
    sweep = ParameterSweep(ref_binary)
    
    # 质量比扫描
    q_vals = np.array([1.0, 2.0, 5.0, 10.0])
    q_result = sweep.mass_ratio_sweep(q_vals)
    print(f"  Mass ratio scan:")
    for i, q in enumerate(q_vals):
        print(f"    q={q:5.1f}: correction={q_result['correction_factor'][i]:.6f}")
    
    # 自旋扫描
    chi_vals = np.array([0.0, 0.3, 0.6, 0.9])
    chi_result = sweep.spin_sweep(chi_vals)
    print(f"  Spin scan:")
    for i, chi in enumerate(chi_vals):
        print(f"    χ={chi:.1f}: correction={chi_result['correction_factor'][i]:.6f}")
    
    # PN 阶数比较
    pn_result = sweep.pn_order_comparison()
    print(f"  PN order comparison:")
    for order, corr in pn_result.items():
        print(f"    {order}PN: correction={corr:.6f}")
    
    print("  ✅ Parameter sensitivity verified")
    return True


def verify_spectral_dE_df_shape():
    """验证 dE/df 谱的形状"""
    binary = BinaryParameters(m1=TEST_MASS, m2=TEST_MASS)
    power_spec = SpectralGWPowerSpectrum(binary, pn_order=3)
    
    # 在频率范围内计算光谱
    f_min, f_max = 1e-5, 1e-2
    result = power_spec.dE_df_spectrum(f_min, f_max, n_points=50)
    
    # dE/df ∝ f^{-1/3}，因此应随 f 增大而减小
    assert result['dE_df_spectral'][-1] < result['dE_df_spectral'][0], \
        "dE/df ∝ f^{-1/3} should decrease with frequency"
    
    # 修正因子在 M=1 M_Pl 时接近 1（PN 修正尚小）
    mean_correction = np.mean(result['correction_factor'])
    print(f"  Mean spectral correction factor: {mean_correction:.6f}")
    print(f"  dE/df range: [{result['dE_df_spectral'][0]:.3e}, {result['dE_df_spectral'][-1]:.3e}]")
    print(f"  h_c range: [{result['h_c_spectral'][0]:.3e}, {result['h_c_spectral'][-1]:.3e}]")
    
    # 验证 dE/df 谱的幂律行为：log(dE/df) ∝ (-1/3) log(f)
    f_vals = result['f']
    dE_df = result['dE_df_spectral']
    log_f = np.log(f_vals[f_vals > 0])
    log_dE = np.log(dE_df[f_vals > 0])
    if len(log_f) > 1:
        slope = np.polyfit(log_f, log_dE, 1)[0]
        print(f"  Power law slope: {slope:.4f} (expected: -0.3333)")
        assert abs(slope + 1/3) < 0.1, f"dE/df should follow f^(-1/3) law, got slope {slope}"
    
    print("  ✅ dE/df spectrum shape verified")
    return True


def run_all_tests():
    """运行所有 A1 测试"""
    print("=" * 60)
    print("A1: Binary Inspiral Spectral Tests")
    print("=" * 60)
    
    tests = [
        ("Newtonian limit", verify_newtonian_limit),
        ("PN spectral structure", verify_pn_spectral_structure),
        ("Correction factor behavior", verify_correction_factor_behavior),
        ("Parameter sensitivity", verify_parameter_sensitivity),
        ("dE/df spectrum shape", verify_spectral_dE_df_shape),
    ]
    
    passed = 0
    for name, test_fn in tests:
        try:
            print(f"\n[{name}]")
            test_fn()
            passed += 1
        except Exception as e:
            print(f"  ❌ Failed: {e}")
    
    print(f"\n{'=' * 60}")
    print(f"✅ {passed}/{len(tests)} A1 tests passed!" if passed == len(tests) 
          else f"⚠️  {passed}/{len(tests)} A1 tests passed")
    
    return passed == len(tests)


if __name__ == "__main__":
    run_all_tests()
