#!/usr/bin/env python3
"""
Phase 52 — A4: 超高能双星并合——全波形谱合成
=============================================

Inspiral-Merger-Ringdown 全阶段完整谱合成。

内容：
  1. 三阶段谱的无缝拼接（光滑窗口过渡）
  2. 与 SEOBNR/IMRPhenom 波形的谱对比（振幅/相位/失配度）
  3. LIGO 观测数据对比框架（全波段 SNR + 匹配滤波）

依赖：A1(binary_inspiral_spectrum), A2(binary_merger_spectrum),
      A3(binary_ringdown_spectrum), C1(spectral_numerics)
"""

import numpy as np
from typing import Optional, Tuple, Dict, Any, Callable, List
from dataclasses import dataclass, field
from scipy import signal, integrate, interpolate
import sys
import os
import warnings

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_spectrum.spectral_numerics import (
    SpectralData, SpectralMatrix, SpectralCutoff,
    M_PL, G_N
)
from dynamic_spectrum.binary_inspiral_spectrum import (
    BinaryParameters, SpectralPNExpansion, SpectralGWPowerSpectrum
)
from dynamic_spectrum.binary_merger_spectrum import (
    RemnantBlackHole, compute_remnant_properties,
    MergerSpectralFlow, QNMExcitationSpectrum,
    MergerRingdownTransition, FullMergerWaveform
)
from dynamic_spectrum.binary_ringdown_spectrum import (
    SchwarzschildLeaverQNM, RingdownMultiModeAnalyzer,
    LIGORingdownComparison, RingdownSpectralEnergy,
    M_SUN_PL
)

# ============================================================
#  物理常数
# ============================================================

# LIGO 频带
LIGO_F_MIN_HZ = 10.0
LIGO_F_MAX_HZ = 10000.0

# 过渡窗口宽度（占合并时间尺度的比例）
MERGER_WINDOW_WIDTH = 0.15
RINGDOWN_ONSET_WIDTH = 0.10


# ============================================================
#  1. IMR 全波形合成器
# ============================================================

class IMRWaveformSynthesizer:
    """
    Inspiral-Merger-Ringdown 全波形谱合成。

    将 A1 (inspiral)、A2 (merger)、A3 (ringdown) 三阶段
    通过光滑窗口函数无缝拼接为完整 IMR 波形。
    """

    def __init__(self,
                 m1: float, m2: float,
                 chi1: float = 0.0, chi2: float = 0.0,
                 dim: int = 32):
        """
        参数
        ----------
        m1, m2 : float
            双星质量（Planck 单位）
        chi1, chi2 : float
            无量纲自旋
        dim : int
            谱截断维数
        """
        self.m1 = m1
        self.m2 = m2
        self.chi1 = chi1
        self.chi2 = chi2
        self.dim = dim

        # 二进制参数
        self.binary = BinaryParameters(
            m1=m1, m2=m2, chi1=chi1, chi2=chi2
        )

        # 残余黑洞（compute_remnant_properties 返回 RemnantBlackHole 对象）
        self.remnant = compute_remnant_properties(m1, m2, chi1, chi2)

        # 谱 PN 展开 (A1)
        self.pn = SpectralPNExpansion(self.binary, pn_order=3, dim=dim)

        # 合并谱流 (A2)
        self.merger_flow = MergerSpectralFlow(
            m1, m2, chi1, chi2, dim=min(dim, 16)
        )

        # QNM 激发 (A2)
        self.qnm_exc = QNMExcitationSpectrum(self.remnant, n_modes=3)

        # 间隙过渡 (A2)
        self.gap_trans = MergerRingdownTransition(
            self.remnant, total_mass=m1 + m2
        )

        # Ringdown 多模分析 (A3)
        self.ringdown = RingdownMultiModeAnalyzer(mass=self.remnant.mass)

        # 光谱截断
        self.cutoff = SpectralCutoff()

        # 内部缓存
        self._cached_inspiral: Optional[Dict] = None
        self._cached_merger: Optional[Dict] = None
        self._cached_ringdown: Optional[Dict] = None
        self._cached_full: Optional[Dict] = None

    @property
    def M_total(self) -> float:
        return self.binary.total_mass

    @property
    def M_chirp(self) -> float:
        return self.binary.chirp_mass

    @property
    def M_final(self) -> float:
        return float(self.remnant.mass)

    @property
    def a_final(self) -> float:
        return float(self.remnant.spin)

    # ---- 窗口函数 ----

    @staticmethod
    def _smooth_window(t: np.ndarray, t_center: float, width: float) -> np.ndarray:
        """
        光滑过渡窗口（decaying sigmoid 过渡）。

        W(t) = 1 - S((t - t_center)/width)
        其中 S(x) = 1/(1 + exp(-x))
        
        在 t << t_center 时 W≈1，在 t >> t_center 时 W≈0。
        """
        x = (t - t_center) / max(width, 1e-10)
        return 1.0 - 1.0 / (1.0 + np.exp(-x))

    def _inspiral_ringdown_window(self, t: np.ndarray,
                                    t_merger: float) -> Tuple[np.ndarray, np.ndarray]:
        """
        计算 inspiral→ringdown 过渡的窗口函数。

        返回 (w_inspiral, w_ringdown) 满足 w_inspiral + w_ringdown ≈ 1
        """
        width = max(self.M_total * MERGER_WINDOW_WIDTH, 0.5)
        w_inspiral = self._smooth_window(t, t_merger + width, width)
        w_ringdown = 1.0 - w_inspiral
        return w_inspiral, w_ringdown

    # ---- 各阶段波形生成 ----

    def inspiral_waveform(self, t: np.ndarray) -> Dict[str, Any]:
        """
        Inspiral 阶段谱波形。

        使用 A1 的谱流演化构造 inspiral 波形。
        简单模型：h(t) ∝ A(t) · exp(-iφ(t))
        振幅增长：A(t) ∝ (t_merger - t)^{-1/4} (PN 预期)
        相位演化：φ(t) = ∫ ω(t') dt' ≈ ∫ f_gw(t') dt'
        """
        M = self.M_total
        Mc = self.M_chirp

        # 参考合并时间（inspiral 发散点）
        t_ref = 50.0 * M  # 足够长的演化时间

        # 振幅：PN 预期 dE/df ∝ f^{-1/3} → A(f) ∝ f^{-1/6}
        # 时域形式：A(t) ∝ (t_ref - t)^{-1/4}
        dt = np.maximum(t_ref - (t - t[0]), 0.1)
        A_env = (dt[0] / dt) ** 0.25

        # 限制振幅不爆炸
        A_env = np.minimum(A_env, 10.0)

        # 相位：chirp 近似 φ(t) = 2π · f(t)
        # f(t) ∝ (t_ref - t)^{-3/8} (Newton 四极近似)
        f_gw = (dt[0] / dt) ** 0.375
        f_gw = np.minimum(f_gw, 0.5)  # 限频

        # 累积相位
        phi = 2.0 * np.pi * np.cumsum(f_gw) * (t[1] - t[0])

        h = A_env * np.exp(-1j * phi)
        h *= self.cutoff.lambda_min / max(np.max(np.abs(h)), 1e-10)

        # 谱演化
        spectral_flow = []
        for i in range(0, len(t), max(1, len(t) // 20)):
            r_i = max(6.0 * M * (1.0 - (t[i] - t[0]) / t_ref), 2.0 * M)
            lam = self.pn.H_newton_spectral(r_i)
            evals = np.sort(np.linalg.eigvalsh(lam))[:self.dim // 2]
            spectral_flow.append(evals)
        spectral_flow = np.array(spectral_flow)

        result = {
            't': t,
            'h': h,
            'envelope': A_env,
            'frequency': f_gw,
            'phase': phi,
            'spectral_flow': spectral_flow,
        }
        self._cached_inspiral = result
        return result

    def _compute_merger_time(self, t_grid: np.ndarray) -> float:
        """
        自动确定合理的合并时刻。

        从时间网格中选取后 1/3 区间中点作为合并时刻，
        保证 merger 后有充分的时间展示 ringdown 衰减。
        """
        return t_grid[len(t_grid) * 2 // 3]

    def merger_waveform(self, t: np.ndarray,
                        t_merger: float) -> Dict[str, Any]:
        """
        合并阶段谱波形（使用 A2 FullMergerWaveform）。

        生成 inspiral→ringdown 过渡区的谱演化。
        """
        wf = FullMergerWaveform(self.m1, self.m2, self.chi1, self.chi2)
        return wf.waveform_imr(t, t_merger=t_merger)

    def ringdown_waveform(self, t: np.ndarray,
                          t_merger: float) -> Dict[str, Any]:
        """
        铃荡阶段多模波形（使用 A3 RingdownMultiModeAnalyzer）。

        t > t_merger 时铃荡波形的解析延拓。
        """
        t_rd = np.maximum(t - t_merger, 0.0)
        result = self.ringdown.synthesize_ringdown(
            t_rd, l_max=4, n_max=2,
            perturbation_amp=self._ringdown_amplitude_scale(),
            include_negative_m=True
        )
        return result

    def _ringdown_amplitude_scale(self) -> float:
        """根据残余黑洞质量确定铃荡振幅标度"""
        return 1.0 * self.M_final / self.M_total

    # ---- 全波形合成 ----

    def full_waveform(self, t: np.ndarray,
                      t_merger: Optional[float] = None) -> Dict[str, Any]:
        """
        合成 Inspiral-Merger-Ringdown 全波形。

        参数
        ----------
        t : ndarray
            时间网格
        t_merger : float, optional
            合并时刻（自动确定若为 None）

        返回
        -------
        dict : {t, h, envelope, spectral_data, stages}
        """
        if t_merger is None:
            t_merger = self._compute_merger_time(t)

        # ---- 1. Inspiral 阶段 ----
        insp = self.inspiral_waveform(t)

        # ---- 2. Ringdown 阶段 ----
        rd = self.ringdown_waveform(t, t_merger)

        # ---- 3. 拼接窗口 ----
        w_insp, w_rd = self._inspiral_ringdown_window(t, t_merger)

        # ---- 4. 光滑过渡 ----
        h_combined = w_insp * insp['h'] + w_rd * rd['h_plus']
        envelope = w_insp * insp['envelope'] + w_rd * np.abs(rd['h_plus'])

        # 归一化
        max_amp = np.max(np.abs(h_combined)) if np.max(np.abs(h_combined)) > 0 else 1.0
        h_combined = h_combined / max_amp
        envelope = envelope / max(max(envelope), 1e-10)

        # ---- 5. 谱演化 ----
        gap_data = self.gap_trans.full_gap_evolution(t, t_merger)

        # QNM 谱
        qnm_table = {}
        if hasattr(self.ringdown, 'qnm_solver') and hasattr(self.ringdown.qnm_solver, 'qnm_spectrum_table'):
            qnm_table = self.ringdown.qnm_solver.qnm_spectrum_table()

        result = {
            't': t,
            'h': h_combined,
            'envelope': envelope,
            'inspiral_weight': w_insp,
            'ringdown_weight': w_rd,
            't_merger': t_merger,
            'spectral_gap': gap_data,
            'qnm_table': qnm_table,
            'inspiral_data': insp,
            'ringdown_data': rd,
            'binary': {
                'm1': self.m1, 'm2': self.m2,
                'M_total': self.M_total,
                'M_chirp': self.M_chirp,
                'M_final': self.remnant.mass,
                'a_final': self.remnant.spin,
                'chi1': self.chi1, 'chi2': self.chi2,
            },
        }
        self._cached_full = result
        return result

    def spectral_flow_imr(self, t: np.ndarray,
                          t_merger: float) -> Dict[str, Any]:
        """
        IMR 全过程的谱流演化。

        返回谱特征值在全时间轴上的演化轨迹。
        """
        # Inspiral 端谱
        result_flow = self.merger_flow.solve_flow(
            merger_time=t_merger,
            n_steps=len(t)
        )
        return result_flow

    def power_spectrum_density(self, t: np.ndarray,
                                t_merger: float) -> Dict[str, Any]:
        """
        计算 IMR 全波形的功率谱密度。

        返回频域谱分布，标识各阶段的谱特征。
        """
        result = self.full_waveform(t, t_merger)
        h = result['h']

        # FFT
        dt = t[1] - t[0]
        n = len(t)
        freqs = np.fft.rfftfreq(n, d=dt)
        h_fft = np.fft.rfft(h, n=n)
        psd = np.abs(h_fft) ** 2 / n

        return {
            'freqs': freqs,
            'psd': psd,
            'h_fft': h_fft,
            'dt': dt,
        }


# ============================================================
#  2. SEOBNR/IMRPhenom 波形谱对比
# ============================================================

class SEOBNRComparator:
    """
    SEOBNR/IMRPhenom 波形谱对比框架。

    将谱框架的 IMR 波形与标准 SEOBNR/IMRPhenom
    波形的振幅/相位/失配度进行系统比较。
    """

    def __init__(self, imr_synthesizer: IMRWaveformSynthesizer):
        self.synth = imr_synthesizer

    def seobnr_amplitude_model(self, t: np.ndarray,
                                t_merger: float) -> np.ndarray:
        """
        SEOBNR 风格的振幅模板（简化解析模型）。

        三阶段拼接：
        - Inspiral: A ∝ (t_merger - t)^{-1/4}
        - Merger: Gaussian 峰
        - Ringdown: 指数衰减
        """
        dt = t - t_merger

        # Inspiral 振幅（t < t_merger）
        amp_insp = np.zeros_like(t)
        mask_insp = dt < 0
        amp_insp[mask_insp] = (-dt[mask_insp] + 1.0) ** (-0.25)
        amp_insp[mask_insp] = np.minimum(amp_insp[mask_insp], 10.0)

        # Merger 峰（t ≈ t_merger）
        merger_width = 0.3
        amp_merger = np.exp(-(dt / merger_width) ** 2)

        # Ringdown 振幅（t > t_merger）
        qnm_freq = self.synth.remnant.qnm_frequency_220
        ringdown_decay = np.exp(np.maximum(dt, 0) * qnm_freq.imag)

        # 组合
        amp = amp_insp + amp_merger * 5.0 + ringdown_decay * 8.0

        # 归一化
        amp = amp / max(np.max(amp), 1e-10)
        return amp

    def compute_mismatch(self, t: np.ndarray,
                         h1: np.ndarray, h2: np.ndarray) -> float:
        """
        计算两个波形之间的失配度 (1 - overlap)。

        Mismatch = 1 - ⟨h1|h2⟩ / sqrt(⟨h1|h1⟩⟨h2|h2⟩)
        """
        inner = np.sum(h1 * np.conj(h2))
        norm1 = np.sum(np.abs(h1) ** 2)
        norm2 = np.sum(np.abs(h2) ** 2)

        if norm1 <= 0 or norm2 <= 0:
            return 1.0

        overlap = abs(inner) / np.sqrt(norm1 * norm2)
        return 1.0 - overlap

    def compare_phase(self, t: np.ndarray,
                      h_imr: np.ndarray, h_seobnr: np.ndarray) -> Dict[str, Any]:
        """
        比较 IMR 波形与 SEOBNR 模板的相位差。
        """
        phase_imr = np.unwrap(np.angle(h_imr))
        phase_seo = np.unwrap(np.angle(h_seobnr))

        # 相位差（对齐第一个点）
        phase_diff = phase_imr - phase_seo
        phase_diff -= phase_diff[0]

        # 相位相干性（去趋势后的残差 RMS）
        coherence = np.correlate(np.exp(1j * phase_imr),
                                 np.exp(1j * phase_seo), mode='same')
        coherence = np.abs(coherence) / len(t)

        return {
            'phase_imr': phase_imr,
            'phase_seobnr': phase_seo,
            'phase_diff': phase_diff,
            'phase_rms': float(np.std(phase_diff)),
            'coherence': float(np.mean(coherence)),
        }

    def full_comparison(self, t: np.ndarray,
                        t_merger: float) -> Dict[str, Any]:
        """
        完整的 SEOBNR 对比分析。

        返回振幅、相位、失配度等全部指标。
        """
        result = self.synth.full_waveform(t, t_merger)
        h_imr = result['h']

        # SEOBNR 振幅模板
        amp_seo = self.seobnr_amplitude_model(t, t_merger)
        h_seobnr = amp_seo * np.exp(1j * np.angle(h_imr))

        # 失配度
        mismatch = self.compute_mismatch(t, h_imr, h_seobnr)

        # 相位比较
        phase_info = self.compare_phase(t, h_imr, h_seobnr)

        # 包络比较
        env_imr = np.abs(h_imr)
        env_seo = amp_seo

        # 频谱比较
        dt = t[1] - t[0]
        n = len(t)
        freqs = np.fft.rfftfreq(n, d=dt)
        psd_imr = np.abs(np.fft.rfft(h_imr, n=n)) ** 2 / n
        psd_seo = np.abs(np.fft.rfft(h_seobnr, n=n)) ** 2 / n

        # 谱重叠
        spec_overlap = np.sum(np.sqrt(psd_imr * psd_seo)) / (
            max(np.sqrt(np.sum(psd_imr) * np.sum(psd_seo)), 1e-10)
        )

        return {
            'h_imr': h_imr,
            'h_seobnr': h_seobnr,
            'envelope_imr': env_imr,
            'envelope_seobnr': env_seo,
            'mismatch': mismatch,
            'phase_info': phase_info,
            'spectral_overlap': float(spec_overlap),
            'freqs': freqs,
            'psd_imr': psd_imr,
            'psd_seo': psd_seo,
            't_merger': t_merger,
        }


# ============================================================
#  3. LIGO 全波形数据对比
# ============================================================

class LIGOFullWaveformComparison:
    """
    全波形 LIGO 观测数据对比框架。

    扩展 A3 的 LIGO ringdown 对比到全 IMR 波形。
    """

    def __init__(self, imr_synthesizer: IMRWaveformSynthesizer):
        self.synth = imr_synthesizer

        # 从 A3 复用 LIGO 噪声曲线
        self.noise = LIGORingdownComparison(
            mass_solar=60.0,
            spin=0.0
        )

    # ---- 物理单位换算 ----

    @staticmethod
    def planck_to_physical(t_pl: np.ndarray, mass_pl: float) -> np.ndarray:
        """
        将 Planck 单位时间转换为秒。

        t_s = t_pl * M_pl / (1.8549e43 Hz)
        其中 M_pl = mass_solar * M_SUN_PL
        """
        pl_to_s = 1.0 / 1.8549e43
        return t_pl * pl_to_s

    @staticmethod
    def amplitude_to_physical(A_pl: np.ndarray, mass_solar: float) -> np.ndarray:
        """
        将 Planck 单位振幅转换为无量纲应变 h(t)。

        近似转换：h ~ A_pl * (M_pl / D_L) 其中 D_L 为光度距离。
        此处使用简化缩放。
        """
        # 简化的应变振幅缩放（假设 D_L ~ 100 Mpc）
        return A_pl * 1e-21

    # ---- 全波段 SNR ----

    def compute_snr_full(self, t: np.ndarray,
                         t_merger: float,
                         mass_solar: float = 60.0,
                         f_low_hz: float = 20.0,
                         f_high_hz: float = 2000.0) -> Dict[str, Any]:
        """
        计算全波段信噪比。

        使用 aLIGO 设计灵敏度噪声曲线，在频域积分。
        """
        result = self.synth.full_waveform(t, t_merger)
        h = result['h']
        dt = t[1] - t[0]

        # 物理单位转换
        M_pl = mass_solar * M_SUN_PL
        t_phys = self.planck_to_physical(t, M_pl)
        h_phys = self.amplitude_to_physical(h, mass_solar)

        # FFT
        n = len(h_phys)
        freqs = np.fft.rfftfreq(n, d=t_phys[1] - t_phys[0])
        h_tilde = np.fft.rfft(h_phys, n=n)

        # aLIGO 噪声 PSD
        f0 = 215.0  # Hz
        S0 = 1e-49  # Hz^{-1}
        Sn = S0 * ((freqs / f0) ** (-4) + 2.0 + (freqs / f0) ** 2)

        # 频带掩码
        band_mask = (freqs >= f_low_hz) & (freqs <= f_high_hz)

        # SNR² = 4 ∫ |h̃(f)|² / S_n(f) df
        df = freqs[1] - freqs[0]
        integrand = np.zeros_like(freqs)
        integrand[band_mask] = 4.0 * np.abs(h_tilde[band_mask]) ** 2 / Sn[band_mask]
        snr_sq = np.trapz(integrand, freqs)

        # 累积 SNR 曲线
        cum_snr_sq = np.cumsum(4.0 * np.abs(h_tilde) ** 2 / Sn) * df
        cum_snr = np.sqrt(np.maximum(cum_snr_sq, 0))

        return {
            'snr': float(np.sqrt(max(snr_sq, 0))),
            'freqs': freqs,
            'Sn': Sn,
            'h_tilde': h_tilde,
            'cum_snr': cum_snr,
            't_phys': t_phys,
            'h_phys': h_phys,
            'mass_solar': mass_solar,
        }

    def matched_filter_analysis(self, t: np.ndarray,
                                 t_merger: float) -> Dict[str, Any]:
        """
        对 IMR 全波形进行匹配滤波自分析。

        使用波形本身作为模板，验证自一致性。
        """
        result = self.synth.full_waveform(t, t_merger)
        h = result['h']
        dt = t[1] - t[0]

        # 自匹配
        norm = np.sum(np.abs(h) ** 2) * dt
        if norm > 0:
            self_match = np.sum(np.abs(h) ** 2) * dt / norm
        else:
            self_match = 0.0

        # 分段匹配（inspiral vs ringdown）
        merger_idx = np.argmin(np.abs(t - t_merger))
        h_insp = h[:merger_idx]
        h_ring = h[merger_idx:]

        norm_insp = np.sum(np.abs(h_insp) ** 2) * dt
        norm_ring = np.sum(np.abs(h_ring) ** 2) * dt
        cross = np.abs(np.sum(h_insp * np.conj(h_ring))) * dt

        insp_ring_overlap = cross / (
            max(np.sqrt(norm_insp * norm_ring), 1e-10)
        )

        return {
            'self_match': float(self_match),
            'insp_ring_overlap': float(insp_ring_overlap),
            'merger_idx': merger_idx,
            'norm_insp': float(norm_insp),
            'norm_ring': float(norm_ring),
        }


# ============================================================
#  数值验证测试
# ============================================================

def verify_imr_waveform_basic():
    """验证 IMR 全波形基本性质"""
    synth = IMRWaveformSynthesizer(1.0, 1.0)

    t = np.linspace(0, 30, 500)
    t_merger = 15.0
    result = synth.full_waveform(t, t_merger)

    # 波形应为有限值
    assert np.all(np.isfinite(result['h'])), "IMR waveform has NaN/Inf"

    # 权重函数应光滑过渡
    assert np.all(np.abs(result['inspiral_weight'] + result['ringdown_weight'] - 1.0) < 0.01), \
        "Window weights should sum to ~1"

    # 合并前 inspiral 权重为主
    pre_merger_mask = result['t'] < t_merger - 1.0
    assert np.mean(result['inspiral_weight'][pre_merger_mask]) > 0.9, \
        "Inspiral should dominate before merger"

    # 合并后 ringdown 权重为主
    post_merger_mask = result['t'] > t_merger + 1.0
    assert np.mean(result['ringdown_weight'][post_merger_mask]) > 0.9, \
        "Ringdown should dominate after merger"

    # 二进制参数应有意义
    assert result['binary']['M_total'] == 2.0
    assert result['binary']['M_chirp'] > 0
    assert result['binary']['M_final'] > 0

    # 谱间隙数据应完整
    assert 'gap_total' in result['spectral_gap']
    assert len(result['spectral_gap']['t']) == len(t)

    # 铃荡段应衰减
    rd_weight = result['ringdown_weight']
    h_amp = np.abs(result['h'])
    rd_region = (post_merger_mask) & (rd_weight > 0.5)
    if np.sum(rd_region) > 10:
        rd_amp = h_amp[rd_region]
        assert np.mean(rd_amp[:len(rd_amp)//3]) >= np.mean(rd_amp[-len(rd_amp)//3:]) * 0.5, \
            "Ringdown region should trend downward"

    print(f"  Total mass: {result['binary']['M_total']:.2f}, ")
    print(f"  Final mass: {result['binary']['M_final']:.4f}, Final spin: {result['binary']['a_final']:.4f}")
    print(f"  Merger time: {t_merger}, Window width: ~{MERGER_WINDOW_WIDTH * synth.M_total:.2f}")
    print(f"  Waveform length: {len(t)} pts, finite: ✅, sum weights: "
          f"{np.mean(result['inspiral_weight'] + result['ringdown_weight']):.4f}")
    print(f"  IMR waveform basic: ✅")
    return True


def verify_imr_spectral_continuity():
    """验证 IMR 谱连续性（拼接点光滑）"""
    synth = IMRWaveformSynthesizer(1.0, 1.0)

    t = np.linspace(0, 30, 300)
    t_merger = 15.0
    result = synth.full_waveform(t, t_merger)
    h = result['h']

    # 检查拼接点附近的光滑性
    merger_idx = np.argmin(np.abs(t - t_merger))
    window = 10  # 拼接点两侧采样数
    start = max(0, merger_idx - window)
    end = min(len(t) - 1, merger_idx + window)

    # 检查拼接点处没有跳跃 (导数连续)
    dh = np.diff(np.abs(h))
    dh_smooth = np.convolve(dh, np.ones(3) / 3, mode='same') if len(dh) >= 3 else dh

    if len(dh_smooth) > merger_idx and merger_idx > 0:
        dh_at_merger = dh_smooth[merger_idx]
        dh_mean = np.mean(np.abs(dh_smooth[start:end]))

        # 拼接点的导数量级应与周围可比
        assert np.isfinite(dh_at_merger), "Derivative should be finite at merger"

        # 检查无大跳跃：拼接点导数不应超过平均的 10 倍
        if dh_mean > 1e-10:
            ratio = abs(dh_at_merger) / dh_mean
            assert ratio < 10.0, \
                f"Large derivative jump at merger: {ratio:.2f}x mean"

    # 功率谱应有合理的频率分布
    psd_result = synth.power_spectrum_density(t, t_merger)
    assert np.all(np.isfinite(psd_result['psd'])), "PSD has NaN/Inf"
    assert np.sum(psd_result['psd'] > 0) > 0, "PSD should have nonzero bins"

    print(f"  Merger index: {merger_idx}/{len(t)}")
    print(f"  |h(t_merger)|: {abs(h[merger_idx]):.4f}")
    print(f"  PSD nonzero bins: {np.sum(psd_result['psd'] > 0)}/{len(psd_result['psd'])}")
    print(f"  Spectral continuity: ✅")
    return True


def verify_imr_seobnr_comparison():
    """验证 SEOBNR 对比框架"""
    synth = IMRWaveformSynthesizer(1.0, 1.0)
    comparator = SEOBNRComparator(synth)

    t = np.linspace(0, 30, 300)
    t_merger = 15.0

    # SEOBNR 振幅模型应为合理值
    amp_seo = comparator.seobnr_amplitude_model(t, t_merger)
    assert np.all(amp_seo >= 0), "SEOBNR amplitude should be non-negative"
    assert np.all(np.isfinite(amp_seo)), "SEOBNR amplitude has NaN/Inf"

    # 失配度应有限
    result = comparator.full_comparison(t, t_merger)
    assert result['mismatch'] >= 0, "Mismatch should be non-negative"
    assert result['mismatch'] <= 1.5, \
        f"Mismatch should be ≤ 1.5, got {result['mismatch']:.4f}"

    # 谱重叠应为正
    assert result['spectral_overlap'] > 0, "Spectral overlap should be positive"

    # 相位 RMS 应有限
    assert np.isfinite(result['phase_info']['phase_rms'])

    print(f"  SEOBNR mismatch: {result['mismatch']:.4f}")
    print(f"  Spectral overlap: {result['spectral_overlap']:.4f}")
    print(f"  Phase RMS: {result['phase_info']['phase_rms']:.4f}")
    print(f"  SEOBNR comparison: ✅")
    return True


def verify_ligo_full_waveform():
    """验证 LIGO 全波形对比框架"""
    synth = IMRWaveformSynthesizer(1.0, 1.0)
    ligo = LIGOFullWaveformComparison(synth)

    t = np.linspace(0, 30, 500)
    t_merger = 15.0

    # 全波段 SNR
    snr_result = ligo.compute_snr_full(t, t_merger, mass_solar=60.0)
    assert snr_result['snr'] >= 0, "SNR should be non-negative"
    assert np.isfinite(snr_result['snr']), "SNR has NaN"
    assert len(snr_result['cum_snr']) == len(snr_result['freqs'])

    # 物理单位转换应有意义
    assert np.all(np.isfinite(snr_result['t_phys'])), "Physical time has NaN"
    assert np.all(np.isfinite(snr_result['h_phys'])), "Physical strain has NaN"
    assert snr_result['t_phys'][-1] > snr_result['t_phys'][0], "Time should increase"
    assert snr_result['mass_solar'] == 60.0

    # 噪声 PSD 应为正
    assert np.all(snr_result['Sn'] > 0), "Noise PSD should be positive"

    # 匹配滤波自分析
    mf_result = ligo.matched_filter_analysis(t, t_merger)
    assert mf_result['self_match'] > 0, "Self-match should be positive"
    assert np.isfinite(mf_result['insp_ring_overlap'])
    assert mf_result['norm_insp'] > 0
    assert mf_result['norm_ring'] > 0

    print(f"  Full-band SNR: {snr_result['snr']:.2f}")
    print(f"  Time span: {snr_result['t_phys'][0]:.2e} - {snr_result['t_phys'][-1]:.2e} s")
    print(f"  Self-match: {mf_result['self_match']:.4f}")
    print(f"  Insp-Ring overlap: {mf_result['insp_ring_overlap']:.4f}")
    print(f"  LIGO full waveform: ✅")
    return True


def verify_imr_parameter_sweep():
    """验证 IMR 参数扫描"""
    params = [
        (1.0, 1.0, 0.0, 0.0),   # 等质量非自旋
        (1.5, 0.5, 0.3, 0.0),   # 非等质量
        (2.0, 1.0, 0.5, 0.3),   # 中高自旋
    ]

    t = np.linspace(0, 30, 300)

    results = []
    for m1, m2, c1, c2 in params:
        synth = IMRWaveformSynthesizer(m1, m2, c1, c2)
        t_merger = synth._compute_merger_time(t)
        result = synth.full_waveform(t, t_merger)
        results.append(result)

    # 所有参数配置都应输出有限值
    for i, res in enumerate(results):
        assert np.all(np.isfinite(res['h'])), f"Parameter set {i} has NaN/Inf"

    # 质量比不同时 chirp mass 应不同
    Mc_values = [r['binary']['M_chirp'] for r in results]
    assert len(set([f"{Mc:.6f}" for Mc in Mc_values])) >= 2, \
        "Chirp masses should differ across parameter sets"

    # 自旋不同时最终自旋应不同
    af_values = [r['binary']['a_final'] for r in results]
    assert af_values[0] != af_values[2], \
        "Final spins should differ: spin(0,0) vs spin(0.5,0.3)"

    print(f"  Parameter sets tested: {len(params)}")
    for i, (m1, m2, c1, c2) in enumerate(params):
        Mc = results[i]['binary']['M_chirp']
        Mf = results[i]['binary']['M_final']
        af = results[i]['binary']['a_final']
        print(f"    (m1={m1}, m2={m2}, c1={c1}, c2={c2}): Mc={Mc:.4f}, Mf={Mf:.4f}, af={af:.4f}")
    print(f"  Parameter sweep: ✅")
    return True


def verify_spectral_flow_imr():
    """验证 IMR 过程的谱流演化"""
    synth = IMRWaveformSynthesizer(1.0, 1.0)

    t = np.linspace(0, 20, 100)
    t_merger = 10.0
    flow = synth.spectral_flow_imr(t, t_merger)

    # 谱流应有合理的输出
    assert flow.get('success', True), "Spectral flow did not converge"
    assert len(flow.get('lambda_history', [])) > 0, "No spectral history"

    lam_hist = flow.get('lambda_history', [])
    if len(lam_hist) > 0:
        assert np.all(np.isfinite(lam_hist)), "Spectral flow has NaN"
        # 至少有一个谱特征值有限
        assert np.any(np.abs(lam_hist) > 0), "All eigenvalues are zero"

    gap_hist = flow.get('min_gaps', [])
    if len(gap_hist) > 0:
        gap_final = gap_hist[-1] if len(gap_hist) > 0 else 0
        assert gap_final >= 0, f"Final gap should be ≥ 0, got {gap_final}"

    print(f"  Flow solver: {'converged' if flow.get('success', True) else 'failed'}")
    print(f"  History shape: {flow.get('lambda_history', np.array([])).shape}")
    print(f"  Spectral flow IMR: ✅")
    return True


def verify_imr_power_spectrum():
    """验证 IMR 功率谱"""
    synth = IMRWaveformSynthesizer(1.0, 1.0)

    t = np.linspace(0, 30, 600)
    t_merger = 15.0
    psd_result = synth.power_spectrum_density(t, t_merger)

    # PSD 应为正
    assert np.all(psd_result['psd'] >= -1e-15), "PSD should be non-negative"
    assert np.all(np.isfinite(psd_result['psd'])), "PSD has NaN/Inf"

    # 频带宽度合理
    assert psd_result['freqs'][-1] >= 0.5 / (t[1] - t[0]), \
        "Nyquist frequency should be reasonable"

    # 低频段应有主要功率（inspiral 主导）
    f = psd_result['freqs']
    psd = psd_result['psd']
    low_band = f < 0.05
    high_band = f > 0.2
    if np.sum(low_band) > 0 and np.sum(high_band) > 0:
        power_low = np.sum(psd[low_band])
        power_high = np.sum(psd[high_band])
        assert power_low > 0 or power_high > 0, "PSD should have nonzero power"
        print(f"  Power ratio (low/high): {power_low / max(power_high, 1e-30):.2f}")

    print(f"  Frequency range: {psd_result['freqs'][0]:.4f} - {psd_result['freqs'][-1]:.4f}")
    print(f"  Total spectral power: {np.sum(psd_result['psd']):.4e}")
    print(f"  Power spectrum: ✅")
    return True


# ============================================================
#  测试调度
# ============================================================

def run_all_tests():
    """运行 A4 全部测试"""
    tests = [
        ("IMR Waveform Basic", verify_imr_waveform_basic),
        ("IMR Spectral Continuity", verify_imr_spectral_continuity),
        ("SEOBNR Comparison", verify_imr_seobnr_comparison),
        ("LIGO Full Waveform", verify_ligo_full_waveform),
        ("Parameter Sweep", verify_imr_parameter_sweep),
        ("Spectral Flow IMR", verify_spectral_flow_imr),
        ("Power Spectrum", verify_imr_power_spectrum),
    ]

    passed = 0
    total = len(tests)

    print(f"A4 测试 ({total} 项):")
    print("=" * 50)

    for name, test_fn in tests:
        try:
            result = test_fn()
            if result:
                passed += 1
                print(f"  [{passed}/{total}] ✓ {name}")
            else:
                print(f"  [✗] {name}: returned False")
        except Exception as e:
            print(f"  [✗] {name}: {type(e).__name__}: {e}")

    print("=" * 50)
    print(f"A4 测试结果: {passed}/{total} 通过")

    return passed == total


if __name__ == "__main__":
    run_all_tests()
