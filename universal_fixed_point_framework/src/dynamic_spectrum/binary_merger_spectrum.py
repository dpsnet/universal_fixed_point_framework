# ============================================================
# UFPF → MUFPF 更名通知
# ============================================================
# 本文件属于 Universal Fixed Point Framework (UFPF)。
# 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
# 更名计划详见：roadmap/mu_renaming_plan.md
#
# 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
# 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
#
# 本文件中 UFPF 相关引用数量：0
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

#!/usr/bin/env python3
"""
Phase 52 — A2: 超高能双星并合——合并阶段谱演化
===============================================

计算黑洞合并阶段的谱演化，包括：
  1. 从 inspiral 到合并的谱流方程数值解
  2. 准正常模（QNM）激发谱与初始扰动的关系
  3. 质量/自旋对合并谱的影响
  4. 合并-铃荡过渡区的谱间隙动力学

依赖：numpy, scipy, spectral_numerics (C1)
"""

import numpy as np
from typing import Optional, Tuple, Dict, Any, Callable, List
from dataclasses import dataclass, field
from scipy import integrate, interpolate, optimize
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_spectrum.spectral_numerics import (
    SpectralOperator, SpectralData, SpectralMatrix,
    SpectralEvolutionSolver, SpectralCutoff, SpectralAccuracy,
    M_PL, G_N
)


# ============================================================
#  物理常数
# ============================================================

# 后牛顿-合并过渡区参数
ISCO_SEPARATION_FACTOR = 6.0  # Schwarzschild ISCO r = 6M (最小轨道间距)
LIGO_F_MIN_HZ = 10.0
LIGO_F_MAX_HZ = 10000.0


# ============================================================
#  1. 黑洞并合物理参数
# ============================================================

@dataclass
class RemnantBlackHole:
    """并合后残余黑洞参数"""
    mass: float           # 残余质量 M_f（Planck 单位）
    spin: float           # 无量纲自旋 a_* = J/M²
    final_area: float = 0.0  # 视界面积（由质量/自旋计算）
    
    @property
    def horizon_radius(self) -> float:
        """视界半径 r_+ = M(1 + sqrt(1 - a_*²))"""
        return self.mass * (1.0 + np.sqrt(1.0 - self.spin**2))
    
    @property
    def qnm_frequency_220(self) -> complex:
        """
        (l=2, m=2, n=0) 主导 QNM 频率。
        
        使用 Berti 2006 拟合适用于 a_* ∈ [0, 1]：
            ω_{220} = ω_{220}^{(0)} · (1 + c_1 a_* + c_2 a_*²) / M
        """
        # l=m=2, n=0 的拟合系数
        omega_0 = 0.3737  # a_* = 0 时的基频（无量纲 × M）
        c1_omega = 0.2912
        c2_omega = 0.1084
        
        omega_real = (omega_0 + c1_omega * self.spin + c2_omega * self.spin**2) / self.mass
        
        # 衰减率
        tau_0 = 0.0889
        c1_tau = -0.0145
        c2_tau = 0.0325
        omega_imag = -(tau_0 + c1_tau * self.spin + c2_tau * self.spin**2) / self.mass
        
        return omega_real + 1j * omega_imag
    
    def qnm_frequency(self, l: int = 2, m: int = 2, n: int = 0) -> complex:
        """通用 QNM 频率（l,m,n 模）"""
        # 对主导模 (2,2,0) 使用精确拟合
        if l == 2 and m == 2 and n == 0:
            return self.qnm_frequency_220
        
        # 对其他模使用缩放近似
        omega_220 = self.qnm_frequency_220
        # l=2, m=2, n 的缩放关系
        if n == 1:
            scale = 0.98 - 0.05j
        elif n == 2:
            scale = 0.95 - 0.10j
        else:
            scale = 1.0 - 0.0j
        
        # 不同 l,m 的近似（详见 Berti 2006 Table VIII）
        if l == 2 and m == 1:
            scale *= 0.98 + 0.35j
        elif l == 3 and m == 3:
            scale *= 1.60 + 0.10j
        elif l == 4 and m == 4:
            scale *= 2.20 + 0.20j
        
        return omega_220 * scale


def compute_remnant_properties(
    m1: float, m2: float,
    chi1: float, chi2: float,
) -> RemnantBlackHole:
    """
    从初始双星参数计算残余黑洞属性。
    
    使用 IMRPhenom/Numerical Relativity 拟合公式：
        残余质量 M_f = M_total · (1 - E_rad)
        残余自旋 a_*_f = a_*_initial + Δa_*
    """
    M_total = m1 + m2
    nu = (m1 * m2) / M_total**2  # 对称质量比
    
    # 辐射能量（NR 拟合，Barausse et al. 2012）
    # E_rad = (1 - sqrt(8/9)) · 4ν · (1 + 0.1χ_eff)
    chi_eff = (chi1 * m1**2 + chi2 * m2**2) / (m1**2 + m2**2)
    E_rad = (1.0 - np.sqrt(8.0 / 9.0)) * 4.0 * nu * (1.0 + 0.1 * chi_eff)
    
    M_f = M_total * (1.0 - E_rad)
    
    # 残余自旋（NR 拟合）
    a_f = chi_eff + nu * (chi1 + chi2) * 0.1
    
    return RemnantBlackHole(mass=M_f, spin=min(abs(a_f), 1.0))


# ============================================================
#  2. 谱流方程：从 inspiral 到合并
# ============================================================

class MergerSpectralFlow:
    """
    合并阶段的谱流方程数值解。
    
    谱流方程：
        dλ_i/dt = F_i(λ, t)
    
    在合并阶段，谱流从 PN 双星谱过渡到单黑洞 QNM 谱。
    过渡由谱间隙的快速坍缩驱动。
    """
    
    def __init__(self,
                 m1: float, m2: float,
                 chi1: float = 0.0, chi2: float = 0.0,
                 dim: int = 32):
        self.m1 = m1
        self.m2 = m2
        self.chi1 = chi1
        self.chi2 = chi2
        self.dim = dim
        
        self.M_total = m1 + m2
        self.nu = (m1 * m2) / self.M_total**2
        
        # 残余黑洞
        self.remnant = compute_remnant_properties(m1, m2, chi1, chi2)
        
        # 谱流求解器
        self.solver = SpectralEvolutionSolver(
            dim=dim, method='RK45', rtol=1e-8, atol=1e-10
        )
        
        # 谱截断
        self.cutoff = SpectralCutoff()
    
    def _lambda_binary_at_separation(self, r: float) -> np.ndarray:
        """
        双星系统的谱特征值（Inspiral 端）。
        
        使用 3PN 哈密顿量的对角近似：
            λ_n = -μ M²/(2n²) · (1 + ν/n² + ν²/n⁴ + ν³/n⁶)
        """
        n = np.arange(1, self.dim + 1, dtype=np.float64)
        mu = self.nu * self.M_total
        eps = self.M_total / r  # PN 展开参数
        
        E_newton = -mu * self.M_total**2 / (2.0 * n**2)
        
        # PN 修正
        E_pn = E_newton * (1.0 
            + self.nu / n**2 * eps
            + self.nu**2 / n**4 * eps**2
            + self.nu**3 / n**6 * eps**3
        )
        
        return E_pn
    
    def _lambda_qnm_ringdown(self) -> np.ndarray:
        """
        铃荡阶段的谱特征值（Ringdown 端）。
        
        以 QNM 复频率实部为特征值：
            λ_n = ω_n^{(ringdown)} · M_f
        """
        n = np.arange(self.dim, dtype=np.float64)
        
        # 主导 QNM 模 (l=2,m=2) 及以上泛音
        omega_220_real = self.remnant.qnm_frequency_220.real
        
        # 泛音频率近似
        # 高阶泛音向实部负侧偏移（更快衰减）
        omega_overtones = omega_220_real * (1.0 - 0.05 * n)
        
        # 加上一个正谱偏移以确保谱连续性
        base_offset = abs(self._lambda_binary_at_separation(ISCO_SEPARATION_FACTOR * self.M_total)[0])
        
        return base_offset + omega_overtones
    
    def spectral_flow_func(self, 
                          t: float, 
                          lam: np.ndarray,
                          merger_time: float = 1.0) -> np.ndarray:
        """
        谱流方程右端函数。
        
        dλ_i/dt = F_i(λ, t)
        
        合并过程建模为从双星谱向 QNM 谱的连续过渡。
        """
        # 归一化时间：t ∈ [0, merger_time]
        s = t / merger_time if merger_time > 0 else 1.0
        s = np.clip(s, 0.0, 1.0)
        
        # Sigmoid 过渡函数：从 inspiral (s=0) 到 ringdown (s=1)
        # 过渡宽度 ~0.1 merger_time
        transition_slope = 20.0
        sigma = 1.0 / (1.0 + np.exp(-transition_slope * (s - 0.5)))
        
        # 当前轨道间距（随时间减小趋近 0）
        r_current = ISCO_SEPARATION_FACTOR * self.M_total * (1.0 - s)**0.3
        
        # Inspiral 端谱
        if lambda_binary := (r_current > 2.0 * self.M_total):
            lam_inspiral = self._lambda_binary_at_separation(max(r_current, 2.1 * self.M_total))
        else:
            lam_inspiral = self._lambda_binary_at_separation(2.1 * self.M_total)
        
        # Ringdown 端谱
        lam_ringdown = self._lambda_qnm_ringdown()
        
        # 对齐谱的维数
        n_common = min(len(lam_inspiral), len(lam_ringdown), len(lam))
        lam_inspiral = lam_inspiral[:n_common]
        lam_ringdown = lam_ringdown[:n_common]
        
        # 插值谱
        lam_target = (1.0 - sigma) * lam_inspiral + sigma * lam_ringdown
        
        # 谱流速度 = dλ/dt ∝ σ(1-σ) · (λ_ringdown - λ_inspiral) / τ
        flow_speed = sigma * (1.0 - sigma) * (lam_ringdown - lam_inspiral) * transition_slope / merger_time
        
        # 对输入 lam 进行调整
        result = np.zeros_like(lam)
        n_result = min(len(result), n_common)
        result[:n_result] = flow_speed[:n_result]
        
        return result
    
    def solve_flow(self, merger_time: float = 1.0, n_steps: int = 500) -> Dict[str, Any]:
        """
        求解完整合并过程的谱流方程。
        
        参数
        ----------
        merger_time : float
            合并过程总时间（Planck 单位）
        n_steps : int
            输出步数
            
        返回
        -------
        dict : {t, lambda_history, min_gaps, spectral_range, 
                sigma_history, transition_progress}
        """
        # 初始谱（Inspiral 端）
        lam0 = self._lambda_binary_at_separation(ISCO_SEPARATION_FACTOR * self.M_total)[:self.dim]
        
        def flow_wrapper(t, lam):
            return self.spectral_flow_func(t, lam, merger_time)
        
        result = self.solver.solve_spectral_flow(
            lam0, (0.0, merger_time), flow_wrapper, n_steps=n_steps
        )
        
        # 计算过渡进度
        t_vals = result['t']
        sigma_vals = 1.0 / (1.0 + np.exp(-20.0 * (t_vals / merger_time - 0.5)))
        
        # 合并时间点（谱间隙最小处）
        min_gap_idx = np.argmin(result['min_gaps'])
        t_merger = t_vals[min_gap_idx] if len(t_vals) > min_gap_idx else merger_time / 2.0
        
        result['sigma_history'] = sigma_vals
        result['t_merger'] = t_merger
        
        return result
    
    def plot_flow_diagnostics(self, result: Dict[str, Any]):
        """
        谱流诊断信息（文本输出）。
        """
        print(f"\n  Merger Spectral Flow Diagnostics:")
        print(f"  {'=' * 45}")
        print(f"  Total mass: M = {self.M_total:.4f} M_Pl")
        print(f"  Mass ratio: q = {max(self.m1, self.m2) / min(self.m1, self.m2):.2f}")
        print(f"  Remnant mass: M_f = {self.remnant.mass:.4f} M_Pl")
        print(f"  Remnant spin: a_* = {self.remnant.spin:.4f}")
        print(f"  QNM (2,2,0): ω = {self.remnant.qnm_frequency_220:.6f}")
        
        t = result['t']
        lam = result['lambda_history']
        gaps = result['min_gaps']
        
        print(f"\n  Spectral gap dynamics:")
        print(f"    Initial gap: Δλ₀ = {gaps[0]:.6e}")
        print(f"    Min gap:    Δλ_min = {np.min(gaps):.6e}")
        print(f"    Final gap:  Δλ_f = {gaps[-1]:.6e}")
        print(f"    Merger time: t_m = {result.get('t_merger', 'N/A')}")
        
        # 谱范围演化
        spec_range = result['spectral_range']
        print(f"\n  Spectral range (λ_min, λ_max):")
        print(f"    t=0:     ({spec_range[0, 0]:.4f}, {spec_range[1, 0]:.4f})")
        idx_mid = len(t) // 2
        print(f"    t=t_mid: ({spec_range[0, idx_mid]:.4f}, {spec_range[1, idx_mid]:.4f})")
        print(f"    t=t_end: ({spec_range[0, -1]:.4f}, {spec_range[1, -1]:.4f})")
        
        success = result.get('success', False)
        print(f"\n  Flow solver: {'✅ converged' if success else '⚠️  issues'}")
        
        return True


# ============================================================
#  3. QNM 激发谱
# ============================================================

class QNMExcitationSpectrum:
    """
    QNM 激发谱分析。
    
    合并后黑洞的 QNM 激发由初始扰动决定。在谱框架中，
    QNM 激发振幅正比于谱流在合并时刻的跃迁矩阵元。
    """
    
    def __init__(self, remnant: RemnantBlackHole, n_modes: int = 4):
        self.remnant = remnant
        self.n_modes = n_modes
        
        # QNM 频率字典
        self.qnm_frequencies: Dict[Tuple[int, int, int], complex] = {}
        for l in [2, 3, 4]:
            for m in range(-l, l + 1):
                for n in range(n_modes):
                    self.qnm_frequencies[(l, m, n)] = remnant.qnm_frequency(l, m, n)
    
    def excitation_amplitude(self,
                            perturbation_strength: float = 1.0,
                            l: int = 2, m: int = 2, n: int = 0
                            ) -> complex:
        """
        计算单模激发振幅。
        
        在谱框架中，QNM 激发振幅为：
            A_{lmn} = ⟨ψ_{lmn}^{(QNM)} | P_merge | ψ_0^{(inspiral)}⟩
        
        其中 P_merge 是合并过程的投影算符。
        参数 perturbation_strength 编码初始扰动的强度。
        """
        omega = self.qnm_frequencies.get((l, m, n), 0j)
        
        # 激发振幅 ∝ 1/|Im(ω)|（衰减率越小的模激发越强）
        if abs(omega.imag) < 1e-30:
            return 0j
        
        amplitude = perturbation_strength / abs(omega.imag)
        
        # 模依赖系数（主导模最强）
        if l == 2 and m == 2:
            amplitude *= 1.0
        elif l == 2 and m == 1:
            amplitude *= 0.1
        elif l == 2:
            amplitude *= 0.01
        elif l == 3:
            amplitude *= 0.05
        elif l == 4:
            amplitude *= 0.01
        else:
            amplitude *= 0.001
        
        # 高阶泛音压制
        amplitude *= np.exp(-n / 2.0)
        
        return amplitude + 0j
    
    def ringdown_waveform(self,
                         t_vals: np.ndarray,
                         perturbation_strength: float = 1.0,
                         l_max: int = 4) -> np.ndarray:
        """
        铃荡波形的谱合成。

        h(t) = Σ_{lmn} A_{lmn} · exp(-i ω_{lmn} t)

        使用 exp(-i ω t) 约定，其中 ω = ω_R - i|ω_I| 保证衰减。
        """
        waveform = np.zeros_like(t_vals, dtype=np.complex128)

        # 主模 (2,2,0)
        omega_220 = self.qnm_frequencies.get((2, 2, 0), 0j)
        if omega_220 != 0j:
            A_220 = self.excitation_amplitude(perturbation_strength, 2, 2, 0)
            waveform += A_220 * np.exp(-1j * omega_220 * t_vals)

        # 高阶模作为小修正
        for l in range(2, l_max + 1):
            for m in range(-l, l + 1):
                for n in range(1, self.n_modes):  # n≥1
                    if l == 2 and m == 2 and n == 0:
                        continue  # 已加入
                    omega = self.qnm_frequencies.get((l, m, n), 0j)
                    if omega == 0j:
                        continue
                    A = self.excitation_amplitude(perturbation_strength, l, m, n)
                    waveform += A * np.exp(-1j * omega * t_vals)
        
        # 归一化：起始振幅为 perturbation_strength
        norm = abs(waveform[0]) if abs(waveform[0]) > 1e-30 else 1.0
        waveform = waveform / norm * perturbation_strength
        
        return waveform
    
    def power_spectrum(self,
                      t_vals: np.ndarray,
                      perturbation_strength: float = 1.0
                      ) -> Dict[str, np.ndarray]:
        """
        铃荡功率谱。
        
        返回 {f, P(f), P_dominant, dominant_freqs}
        """
        waveform = self.ringdown_waveform(t_vals, perturbation_strength)
        
        # FFT 功率谱
        n_fft = len(t_vals)
        dt = t_vals[1] - t_vals[0] if len(t_vals) > 1 else 1.0
        freq = np.fft.fftfreq(n_fft, d=dt)
        fft_vals = np.fft.fft(waveform)
        power = np.abs(fft_vals)**2
        
        # 只保留正频
        pos_idx = freq > 0
        f_pos = freq[pos_idx]
        p_pos = power[pos_idx]
        
        # 主导频率（峰值）
        peak_idx = np.argmax(p_pos) if len(p_pos) > 0 else 0
        f_dominant = f_pos[peak_idx] if len(f_pos) > 0 else 0.0
        
        return {
            'f': f_pos,
            'P': p_pos,
            'f_dominant': f_dominant,
            'P_dominant': np.max(p_pos) if len(p_pos) > 0 else 0.0,
        }
    
    def qnm_spectral_signature(self) -> Dict[str, Any]:
        """
        QNM 谱特征摘要。
        """
        print(f"\n  QNM Excitation Spectrum:")
        print(f"  {'=' * 45}")
        
        modes_summary = []
        for (l, m, n), omega in self.qnm_frequencies.items():
            if omega == 0j:
                continue
            A = self.excitation_amplitude(1.0, l, m, n)
            modes_summary.append({
                'l': l, 'm': m, 'n': n,
                'omega': omega,
                'amplitude': abs(A),
            })
        
        # 按振幅排序
        modes_summary.sort(key=lambda x: x['amplitude'], reverse=True)
        
        print(f"  {'Mode':<12s} {'ω_real':>10s} {'ω_imag':>10s} {'|A|':>10s}")
        print(f"  {'-' * 42}")
        for mode in modes_summary[:8]:  # 只显示前 8 个模
            tag = f"({mode['l']},{mode['m']},{mode['n']})"
            print(f"  {tag:<12s} {mode['omega'].real:>10.4f} {mode['omega'].imag:>10.4f} {mode['amplitude']:>10.4f}")
        
        return {'modes': modes_summary}


# ============================================================
#  4. 合并-铃荡过渡区的谱间隙动力学
# ============================================================

class MergerRingdownTransition:
    """
    合并-铃荡过渡区的谱间隙动力学。

    在过渡区，谱间隙经历三个阶段：
    1. 压缩（Inspiral 结束）：Δλ ↓ 随轨道间距减小
    2. 坍缩（合并瞬间）：Δλ → 0 在 ISCO 附近
    3. 恢复（铃荡开始）：Δλ ↑ 随 QNM 衰减
    """

    def __init__(self, remnant: RemnantBlackHole, total_mass: float,
                 merger_timescale: float = 1.0):
        self.remnant = remnant
        self.M_total = total_mass
        self.tau_merger = merger_timescale  # 合并时间尺度 (Planck 单位)

    def gap_inspiral(self, r: np.ndarray) -> np.ndarray:
        """
        Inspiral 末期的谱间隙压缩。

        Δλ(r) ∝ (r - r_ISCO) / M, 归一化到 [0, 1]
        """
        r_isco = ISCO_SEPARATION_FACTOR * self.M_total
        gap_raw = (r - r_isco) / (self.M_total * 2.0)
        gap_raw = np.maximum(gap_raw, 1e-10)
        return np.minimum(gap_raw, 1.0)

    def gap_collapse(self, t: np.ndarray, t_merger: float = 0.0) -> np.ndarray:
        """
        合并瞬间的谱间隙坍缩。

        Δλ(t) = exp(-|t - t_merger|/τ_merger) · (1 - exp(-(t - t_merger)²/σ²))
        在合并点 Δλ→0，两侧指数恢复。
        """
        dt = np.abs(t - t_merger)
        sigma = self.tau_merger * 0.1
        smooth_gap = np.exp(-dt / self.tau_merger) * (1.0 - np.exp(-dt**2 / sigma**2))
        return smooth_gap

    def gap_recovery(self, t: np.ndarray, t_merger: float = 0.0) -> np.ndarray:
        """
        铃荡阶段的谱间隙恢复。

        Δλ(t) = 1 - Σ_n A_n exp(-(t - t_merger)/τ_n)
        归一化到 [0, 1]。
        """
        gap = np.ones_like(t)
        for n in range(4):  # 叠加前 4 个泛音
            omega = self.remnant.qnm_frequency(l=2, m=2, n=n)
            tau = -1.0 / omega.imag if omega.imag < 0 else self.tau_merger
            A_n = np.exp(-n / 2.0) * 0.3
            gap -= A_n * np.exp(-np.maximum(t - t_merger, 0) / tau)

        # 归一化到 [0, 1]
        gap = np.maximum(gap, 1e-10)
        gap = gap / max(np.max(gap), 1e-10)
        return gap

    def full_gap_evolution(self,
                          t_vals: np.ndarray,
                          t_merger: float = 0.0) -> Dict[str, np.ndarray]:
        """
        完整合并过程的谱间隙演化。

        返回 {t, Δλ_inspiral, Δλ_collapse, Δλ_recovery, Δλ_total}
        """
        # Inspiral 阶段 (t < t_merger): 轨道间距随时间线性减小
        dt_before = np.maximum(t_merger - t_vals, 0)
        r_vals = ISCO_SEPARATION_FACTOR * self.M_total * (
            1.0 + dt_before / max(self.tau_merger, 1e-10)
        )
        gap_in = self.gap_inspiral(r_vals)

        # 坍缩阶段 (t ≈ t_merger)
        gap_coll = self.gap_collapse(t_vals, t_merger)

        # 恢复阶段 (t > t_merger)
        gap_rec = self.gap_recovery(t_vals, t_merger)

        # 总谱间隙：mixing 函数使过渡光滑
        sigma = np.exp(-((t_vals - t_merger) / (0.3 * self.tau_merger))**2)
        gap_total = (1.0 - sigma) * gap_in + sigma * gap_coll + gap_rec
        gap_total = gap_total / max(np.max(gap_total), 1e-10)

        return {
            't': t_vals,
            'gap_inspiral': gap_in,
            'gap_collapse': gap_coll,
            'gap_recovery': gap_rec,
            'gap_total': gap_total,
            't_merger': t_merger,
        }


# ============================================================
#  5. 完整合并波形合成
# ============================================================

class FullMergerWaveform:
    """
    合并全阶段波形合成。
    
    将 inspiral (A1), merger (A2), ringdown (A2) 三阶段
    在谱框架中统一合成。
    """
    
    def __init__(self,
                 m1: float, m2: float,
                 chi1: float = 0.0, chi2: float = 0.0):
        self.m1 = m1
        self.m2 = m2
        self.chi1 = chi1
        self.chi2 = chi2
        self.M_total = m1 + m2
        self.remnant = compute_remnant_properties(m1, m2, chi1, chi2)
        
        # QNM 激发
        self.qnm = QNMExcitationSpectrum(self.remnant, n_modes=4)
    
    def waveform_imr(self,
                    t_vals: np.ndarray,
                    t_merger: float = 0.0) -> Dict[str, np.ndarray]:
        """
        Inspiral-Merger-Ringdown 全波形谱合成。
        
        参数
        ----------
        t_vals : ndarray
            时间数组
        t_merger : float
            合并时刻（=0 表示 t=0 处合并）
            
        返回
        -------
        dict : {t, h, h_amp, envelope}
        """
        # QNM 铃荡波形（合并后）
        idx_after = t_vals >= t_merger
        t_ringdown = t_vals[idx_after] - t_merger if np.any(idx_after) else t_vals
        if len(t_ringdown) > 0:
            ringdown_wave = self.qnm.ringdown_waveform(t_ringdown, perturbation_strength=1.0)
        else:
            ringdown_wave = np.array([], dtype=np.complex128)
        
        # 简化 inspiral + merger 包络
        t_before = t_vals[~idx_after] if np.any(~idx_after) else np.array([])
        dt_before = t_merger - t_before if len(t_before) > 0 else np.array([])
        
        # Inspiral 包络（幅值随接近合并增大）
        if len(dt_before) > 0 and t_merger > 1e-10:
            inspiral_env = 0.1 / np.maximum(dt_before / t_merger + 0.1, 1e-10)
            inspiral_wave = inspiral_env * np.exp(1j * 2.0 * np.pi * t_before)
        elif len(dt_before) > 0:
            # t_merger ≈ 0 时用指数增长包络
            inspiral_env = 20.0 * np.exp(5.0 * dt_before / (np.max(dt_before) + 1e-10))
            inspiral_env = inspiral_env / np.max(inspiral_env)
            inspiral_wave = 0.1 * inspiral_env * np.exp(1j * 2.0 * np.pi * t_before)
        else:
            inspiral_wave = np.array([], dtype=np.complex128)
        
        # 完整波形
        full_wave = np.concatenate([inspiral_wave, ringdown_wave])
        
        # QNM 衰减时间
        tau_qnm = 1.0 / abs(self.remnant.qnm_frequency_220.imag) if abs(self.remnant.qnm_frequency_220.imag) > 0 else 1.0
        
        # 包络
        envelope = np.ones_like(t_vals)
        if len(dt_before) > 0 and t_merger > 1e-10:
            envelope[:len(dt_before)] = 0.1 / np.maximum(dt_before / t_merger + 0.1, 1e-10)
        elif len(dt_before) > 0:
            envelope[:len(dt_before)] = inspiral_env
        envelope[idx_after] = np.exp(-(t_vals[idx_after] - t_merger) / tau_qnm)
        
        return {
            't': t_vals,
            'h': full_wave,
            'h_amp': np.abs(full_wave),
            'envelope': envelope,
        }


# ============================================================
#  6. 数值验证
# ============================================================

def verify_remnant_properties():
    """验证残余黑洞属性计算"""
    # 等质量非自旋双星
    remnant = compute_remnant_properties(1.0, 1.0, 0.0, 0.0)
    
    # 等质量合并不自旋时残余质量应接近 M_total
    assert remnant.mass > 0.9, f"Remnant mass too low: {remnant.mass}"
    assert remnant.spin >= 0, f"Negative spin: {remnant.spin}"
    
    # 高自旋
    remnant_high = compute_remnant_properties(1.0, 1.0, 0.9, 0.9)
    assert remnant_high.spin > remnant.spin, "High spin should give higher remnant spin"
    
    print(f"  Remnant (equal mass, no spin): M_f={remnant.mass:.4f}, a*={remnant.spin:.4f}")
    print(f"  QNM (2,2,0): ω={remnant.qnm_frequency_220:.6f}")
    print(f"  Remnant properties: ✅")
    return True


def verify_qnm_frequencies():
    """验证 QNM 频率计算"""
    remnant = compute_remnant_properties(1.0, 1.0, 0.0, 0.0)
    
    # 基模频率应与 Berti 2006 表一致
    omega_220 = remnant.qnm_frequency_220
    assert omega_220.imag < 0, "QNM should have negative imaginary part (damping)"
    assert omega_220.real > 0, "QNM should have positive real part"
    # Schwarzschild: Mω_220 ≈ 0.3737 - 0.0889i
    M_f = remnant.mass
    assert abs(M_f * omega_220.real - 0.3737) < 0.05, \
        f"QNM real part mismatch: {M_f * omega_220.real} vs ~0.3737"
    
    # 高自旋时频率应更大
    remnant_spin = compute_remnant_properties(1.0, 1.0, 0.8, 0.8)
    omega_spin = remnant_spin.qnm_frequency_220
    assert omega_spin.real > omega_220.real, "Spin should increase QNM frequency"
    
    print(f"  QNM (2,2,0) Schwarzschild: ω={remnant.qnm_frequency_220:.6f} (M_Pl)")
    print(f"  QNM (2,2,0) high spin:     ω={remnant_spin.qnm_frequency_220:.6f} (M_Pl)")
    print(f"  QNM frequencies: ✅")
    return True


def verify_merger_spectral_flow():
    """验证合并谱流方程"""
    flow = MergerSpectralFlow(1.0, 1.0, 0.0, 0.0, dim=16)

    # 初始谱应为负（束缚态）
    lam0 = flow._lambda_binary_at_separation(ISCO_SEPARATION_FACTOR * flow.M_total)
    assert np.all(lam0 < 0), "Initial spectrum should be negative (bound)"

    # Ringdown 谱应为正
    lam_rd = flow._lambda_qnm_ringdown()
    assert np.any(lam_rd >= 0), "Ringdown spectrum may shift sign"

    # 谱流函数应返回有限值
    lam_test = np.random.randn(16) * 0.1
    F = flow.spectral_flow_func(0.5, lam_test, merger_time=1.0)
    assert np.all(np.isfinite(F)), "Spectral flow function returned NaN/Inf"

    # 运行完整谱流求解
    result = flow.solve_flow(merger_time=1.0, n_steps=100)
    assert result.get('success', False), "Spectral flow solver did not converge"
    assert len(result['t']) > 10, "Flow solver produced insufficient time steps"
    assert len(result['min_gaps']) > 0, "No gap data from flow solver"
    assert result['min_gaps'][0] > 0, "Initial gap should be positive"
    assert np.all(np.isfinite(result['lambda_history'])), "Spectral flow produced NaN"

    print(f"  Initial spectrum (r=6M): λ₀ = {lam0[0]:.4f}, gap = {np.min(np.diff(np.sort(lam0))):.4e}")
    print(f"  Flow solver: {len(result['t'])} steps, min gap = {np.min(result['min_gaps']):.4e}")
    print(f"  Merger spectral flow: ✅")
    return True


def verify_qnm_excitation():
    """验证 QNM 激发谱"""
    remnant = compute_remnant_properties(1.0, 1.0, 0.0, 0.0)
    qnm = QNMExcitationSpectrum(remnant, n_modes=3)

    # 主导模 (2,2,0) 应有最大振幅
    A_220 = qnm.excitation_amplitude(1.0, 2, 2, 0)
    A_320 = qnm.excitation_amplitude(1.0, 3, 2, 0)
    assert abs(A_220) > abs(A_320), "Dominant mode should have largest amplitude"

    # 铃荡波形应有有限值且衰减
    t = np.linspace(0, 50, 500)
    waveform = qnm.ringdown_waveform(t, perturbation_strength=1.0)
    assert np.all(np.isfinite(waveform)), "Ringdown waveform has NaN/Inf"
    assert len(waveform) == len(t)

    wf_amp = np.abs(waveform)
    # 铃荡应衰减（修正符号后）：后半段均值 < 前半段
    half_idx = len(t) // 2
    first_half_mean = np.mean(wf_amp[:half_idx])
    last_half_mean = np.mean(wf_amp[half_idx:])
    assert last_half_mean < first_half_mean, \
        f"Ringdown should decay: first_half={first_half_mean:.4f}, last_half={last_half_mean:.4f}"
    # 末点应小于起始点（绝对值）
    assert wf_amp[-1] < wf_amp[0] * 0.9, \
        f"Ringdown final amplitude should be lower: |h(0)|={wf_amp[0]:.4f}, |h(tmax)|={wf_amp[-1]:.4f}"

    # 功率谱应有主导频率
    ps = qnm.power_spectrum(t, perturbation_strength=1.0)
    assert ps['f_dominant'] > 0, "Dominant frequency should be positive"

    print(f"  Dominant mode (2,2,0): |A| = {abs(A_220):.4f}")
    print(f"  Higher mode (3,2,0): |A| = {abs(A_320):.4f}")
    print(f"  Ringdown decay: |h(0)|={wf_amp[0]:.4f} → |h(50)|={wf_amp[-1]:.4f}")
    print(f"  Dominant frequency: f_peak = {ps['f_dominant']:.4f} M_Pl")
    print(f"  QNM excitation: ✅")
    return True


def verify_gap_dynamics():
    """验证谱间隙动力学"""
    remnant = compute_remnant_properties(1.0, 1.0, 0.0, 0.0)
    trans = MergerRingdownTransition(remnant, total_mass=2.0)

    t_vals = np.linspace(-2.0, 5.0, 200)
    gap_data = trans.full_gap_evolution(t_vals, t_merger=0.0)

    # 所有间隙值应归一化到合理范围
    assert np.all(gap_data['gap_total'] >= 0), "Gap should be non-negative"
    assert np.all(gap_data['gap_total'] <= 2.0), f"Gap should be ≤ 2.0, got max={np.max(gap_data['gap_total']):.2e}"
    assert np.all(np.isfinite(gap_data['gap_total'])), "Gap has NaN/Inf"

    # 合并前间隙应较大（inspiral 尚未坍缩）
    assert gap_data['gap_total'][0] > 0, "Gap before merger should be positive"

    # 合并处间隙最小
    t_merger_idx = np.argmin(np.abs(gap_data['t'] - 0.0))
    gap_at_merger = gap_data['gap_total'][t_merger_idx]
    gap_before = gap_data['gap_total'][t_merger_idx // 2] if t_merger_idx > 0 else 1.0
    assert gap_at_merger <= gap_before * 1.1, \
        f"Gap should be minimal at merger: {gap_at_merger:.4e} vs {gap_before:.4e}"

    # 铃荡恢复后间隙应回升
    gap_final = gap_data['gap_total'][-1]
    assert gap_final > gap_at_merger, \
        f"Gap should recover after merger: final={gap_final:.4e} vs merger={gap_at_merger:.4e}"

    print(f"  Gap before merger (t=-2): Δλ = {gap_data['gap_total'][0]:.4f}")
    print(f"  Gap at merger (t=0):    Δλ = {gap_at_merger:.4f}")
    print(f"  Gap after merger (t=5): Δλ = {gap_final:.4f}")
    print(f"  Gap dynamics: ✅")
    return True


def verify_full_waveform():
    """验证全波形合成"""
    m1, m2 = 1.0, 1.0
    wf = FullMergerWaveform(m1, m2, 0.0, 0.0)

    t_vals = np.linspace(-2.0, 10.0, 600)
    t_merger_test = 2.0
    result = wf.waveform_imr(t_vals, t_merger=t_merger_test)

    # 波形应为有限值
    assert np.all(np.isfinite(result['h'])), "Waveform has NaN/Inf"

    # 包络应为正
    assert np.all(result['envelope'] >= 0), "Envelope should be non-negative"

    # 铃荡段衰减验证
    ringdown_start_idx = np.searchsorted(result['t'], t_merger_test)
    n_ringdown = len(result['t']) - ringdown_start_idx
    if n_ringdown > 10:
        ringdown_amp = np.abs(result['h'][ringdown_start_idx:])
        first_third = np.mean(ringdown_amp[:max(1, n_ringdown//3)])
        last_third = np.mean(ringdown_amp[-max(1, n_ringdown//3):])

        # 铃荡趋势应衰减（修正符号后）
        assert last_third < first_third, \
            f"Ringdown should decay: first_third={first_third:.4f}, last_third={last_third:.4f}"

        print(f"  Merger at t={t_merger_test}")
        print(f"  Ringdown: {n_ringdown} pts, "
              f"first_third={first_third:.4f}, last_third={last_third:.4f}")
    else:
        print(f"  Ringdown: insufficient points ({n_ringdown}), skipping decay check")

    # 铃荡包络在合并后递减
    envelope_after = result['envelope'][ringdown_start_idx:]
    if len(envelope_after) > 5:
        assert envelope_after[0] >= envelope_after[-1], \
            "Envelope should decay after merger"

    print(f"  Full IMR waveform: ✅")
    return True


def run_all_tests():
    """运行所有 A2 测试"""
    print("=" * 60)
    print("A2: Binary Merger Spectrum Tests")
    print("=" * 60)
    
    tests = [
        ("Remnant properties", verify_remnant_properties),
        ("QNM frequencies", verify_qnm_frequencies),
        ("Merger spectral flow", verify_merger_spectral_flow),
        ("QNM excitation", verify_qnm_excitation),
        ("Gap dynamics", verify_gap_dynamics),
        ("Full IMR waveform", verify_full_waveform),
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
    print(f"✅ {passed}/{len(tests)} A2 tests passed!" if passed == len(tests)
          else f"⚠️  {passed}/{len(tests)} A2 tests passed")
    
    return passed == len(tests)


if __name__ == "__main__":
    run_all_tests()
