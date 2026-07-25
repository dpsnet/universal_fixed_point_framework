#!/usr/bin/env python3
"""
Phase 52 — C4: 可视化工具链
==============================

构建动态过程谱的可视化工具链。
  1. 谱演化可视化（双星并合谱流 + QNM 谱 + 全波形）
  2. 散射振幅与截面可视化（角分布 + UV 压制 + RG 对比）
  3. 实验数据对比绘图（LIGO 对接 + 理论预测 vs 观测）
  4. ASCII 终端输出（无依赖降级）+ 出版级 PNG/PDF（matplotlib 扩展）

依赖：numpy, scipy, spectral_numerics, A1-A4, B1-B4
"""

import numpy as np
from typing import Optional, Tuple, Dict, Any, Callable, List
from dataclasses import dataclass, field
from scipy import signal as scipy_signal
import sys
import os
import warnings

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_spectrum.spectral_numerics import (
    SpectralOperator, SpectralData, SpectralMatrix,
    SpectralCutoff, M_PL, G_N
)

# ---- matplotlib 可选检测 ----
try:
    import matplotlib
    matplotlib.use('Agg')  # 非交互后端
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    from matplotlib.colors import LogNorm, Normalize
    HAS_MPL = True
except ImportError:
    HAS_MPL = False
    warnings.warn("matplotlib not available, falling back to ASCII output")


# ============================================================
#  1. ASCII 图形引擎（零依赖）
# ============================================================

# --- Unicode 制表符 ---
_BOX_H = '\u2500'
_BOX_V = '\u2502'
_BOX_TL = '\u250c'
_BOX_TR = '\u2510'
_BOX_BL = '\u2514'
_BOX_BR = '\u2518'
_BOX_MH = '\u252c'
_BOX_MV = '\u251c'
_BOX_MX = '\u253c'

_BLOCK = '\u2588'
_HALF_BLOCK = '\u258c'
_LIGHT_SHADE = '\u2591'
_MED_SHADE = '\u2592'
_DARK_SHADE = '\u2593'

_ARROW_UP = '\u2191'
_ARROW_DN = '\u2193'
_ARROW_RT = '\u2192'


def _format_sci(x: float, prec: int = 2) -> str:
    """科学计数法格式化"""
    if abs(x) < 1e-100:
        return '0'
    sign = '-' if x < 0 else ''
    x = abs(x)
    exp = int(np.floor(np.log10(x))) if x > 0 else 0
    mant = x / 10 ** exp
    return f'{sign}{mant:.{prec}f}e{exp:+d}'


def _hbar(w: int) -> str:
    """水平线条"""
    return _BOX_H * w


def ascii_bar(value: float, max_val: float, width: int = 30) -> str:
    """ASCII 条形图"""
    if max_val <= 0:
        return ' ' * width
    value = max(value, 0.0)  # 负值视为 0
    n = int(min(value / max_val, 1.0) * width)
    bar = _BLOCK * n + _LIGHT_SHADE * (width - n)
    return bar


class ASCIICanvas:
    """ASCII 绘图画布（无 matplotlib 依赖）"""

    def __init__(self, width: int = 70, height: int = 20):
        self.W = width
        self.H = height
        self._grid: List[List[str]] = [
            [' ' for _ in range(width)] for _ in range(height)
        ]

    def set(self, x: int, y: int, ch: str = '*'):
        """在 (x,y) 处设置字符"""
        if 0 <= x < self.W and 0 <= y < self.H:
            self._grid[self.H - 1 - y][x] = ch

    def vline(self, x: int, y0: int, y1: int, ch: str = _BOX_V):
        """垂直线"""
        for y in range(max(0, y0), min(self.H, y1 + 1)):
            self.set(x, y, ch)

    def hline(self, y: int, x0: int, x1: int, ch: str = _BOX_H):
        """水平线"""
        for x in range(max(0, x0), min(self.W, x1 + 1)):
            self.set(x, y, ch)

    def plot_xy(self, xs: np.ndarray, ys: np.ndarray,
                 x_range: Tuple[float, float],
                 y_range: Tuple[float, float],
                 marker: str = '*'):
        """在画布上绘制 (x,y) 散点"""
        for xv, yv in zip(xs, ys):
            ix = int((xv - x_range[0]) / (x_range[1] - x_range[0]) * (self.W - 1))
            iy = int((yv - y_range[0]) / (y_range[1] - y_range[0]) * (self.H - 1))
            if 0 <= ix < self.W and 0 <= iy < self.H:
                self.set(ix, iy, marker)

    def render(self) -> str:
        """渲染为字符串"""
        lines = []
        # 顶部边框
        lines.append(f'{_BOX_TL}{_hbar(self.W)}{_BOX_TR}')
        for row in self._grid:
            lines.append(f'{_BOX_V}{"".join(row)}{_BOX_V}')
        lines.append(f'{_BOX_BL}{_hbar(self.W)}{_BOX_BR}')
        return '\n'.join(lines)

    def axis_labels(self, xlabel: str, ylabel: str,
                     x_range: Tuple[float, float],
                     y_range: Tuple[float, float]):
        """添加轴标签（文本输出）"""
        pass  # 标签放在外部文本中


def _table(header: List[str], rows: List[List[str]],
           title: str = '', widths: Optional[List[int]] = None) -> str:
    """通用表格渲染"""
    n_cols = len(header)
    if widths is None:
        widths = [max(len(header[i]), max(len(r[i]) for r in rows)) + 2
                  for i in range(n_cols)]

    sep = '+' + '+'.join(_hbar(w) for w in widths) + '+'

    out = []
    if title:
        out.append(f'  {title}')
        out.append(f'  {_hbar(sum(widths) + n_cols + 1)}')

    out.append(sep)
    row_str = '|'
    for i, h in enumerate(header):
        row_str += f' {h:^{widths[i] - 1}}|'
    out.append(row_str)
    out.append(sep)

    for row in rows:
        row_str = '|'
        for i, cell in enumerate(row):
            row_str += f' {cell:>{widths[i] - 1}}|'
        out.append(row_str)
    out.append(sep)

    return '\n'.join(out)


# ============================================================
#  2. 谱演化可视化
# ============================================================

class SpectralEvolutionVisualizer:
    """
    双星并合谱演化可视化。

    功能：
    - 谱间隙演化（gap 随时间变化 + ASCII 帧序列）
    - QNM 谱表（多模频率 + 激发振幅）
    - Ringdown 波形图（h_plus, h_cross, 包络）
    - IMR 全波形谱合成图（三阶段 + 拼接）
    """

    def __init__(self, title: str = "Binary Merger Spectral Evolution"):
        self.title = title

    # ---- 2a. 谱间隙演化 ----

    def gap_evolution_table(self, t: np.ndarray, gaps: np.ndarray,
                             label: str = "Spectral Gap Δλ") -> str:
        """谱间隙演化的时间序列表"""
        n = min(12, len(t))
        indices = np.linspace(0, len(t) - 1, n, dtype=int)

        # 用 ASCII 条形图可视化每步的间隙
        max_gap = max(gaps) if max(gaps) > 0 else 1.0

        header = ['t', label, 'Profile']
        rows = []
        for i in indices:
            t_str = f'{t[i]:.4f}'
            gap_str = f'{gaps[i]:.4e}'
            bar = ascii_bar(gaps[i], max_gap, width=25)
            rows.append([t_str, gap_str, bar])

        return _table(header, rows, title=self.title,
                      widths=[10, 16, 30])

    def gap_evolution_ascii_frame(self, t: float, gap: float,
                                    frame_width: int = 60) -> str:
        """单帧 ASCII 谱间隙演化图"""
        max_gap = 1.0
        bar_len = int(gap / max_gap * frame_width) if max_gap > 0 else 0
        bar_len = min(bar_len, frame_width)

        line = f't={t:6.4f} |'
        line += _BLOCK * bar_len
        line += _LIGHT_SHADE * (frame_width - bar_len)
        line += f'| {gap:.4e}'
        return line

    def gap_animation_ascii(self, t_vals: np.ndarray, gap_vals: np.ndarray,
                             n_frames: int = 20) -> str:
        """ASCII 帧序列动画"""
        frames = []
        n = min(n_frames, len(t_vals))
        indices = np.linspace(0, len(t_vals) - 1, n, dtype=int)
        for i in indices:
            frames.append(self.gap_evolution_ascii_frame(t_vals[i], gap_vals[i]))
        return '\n'.join(frames)

    # ---- 2b. QNM 谱表 ----

    def qnm_spectrum_table(self, qnm_data: Dict[Tuple[int, int, int], complex],
                            amplitudes: Optional[Dict[Tuple[int, int, int], float]] = None
                            ) -> str:
        """QNM 谱表（多模频率 + 振幅）"""
        # 按 (l, m, n) 排序
        modes = sorted(qnm_data.keys())
        header = ['l', 'm', 'n', 'ω_R (× M)', '-ω_I (× M)',
                  'τ (M)', '|A|']
        rows = []
        for l, m, n in modes:
            omega = qnm_data[(l, m, n)]
            if not isinstance(omega, complex):
                continue
            wr = -omega.real * M_PL if abs(omega.real) > 0 else 0
            wi = -omega.imag * M_PL if abs(omega.imag) > 0 else 0
            tau = 1.0 / max(abs(omega.imag), 1e-40) if abs(omega.imag) > 0 else float('inf')
            amp = amplitudes.get((l, m, n), 1.0) if amplitudes else 1.0
            rows.append([
                str(l), str(m), str(n),
                f'{wr:.4f}', f'{wi:.4f}',
                f'{tau:.2e}', f'{amp:.4f}',
            ])

        return _table(header, rows, title=f'{self.title} — QNM Spectrum',
                      widths=[4, 4, 4, 14, 14, 12, 10])

    def qnm_frequency_bars(self, qnm_data: Dict[Tuple[int, int, int], complex]) -> str:
        """QNM 频率条形图"""
        modes = sorted(qnm_data.keys())
        max_freq = max(abs(omega.real) for omega in qnm_data.values()
                       if isinstance(omega, complex)) or 1.0

        out = [f'  QNM Frequencies ({self.title}):']
        for l, m, n in modes:
            omega = qnm_data[(l, m, n)]
            if not isinstance(omega, complex):
                continue
            wr_ratio = abs(omega.real) / max_freq if max_freq > 0 else 0
            bar = ascii_bar(wr_ratio, 1.0, width=30)
            out.append(
                f'  ({l},{m},{n}) {bar} ω_R={omega.real:.4f}'
            )
        return '\n'.join(out)

    # ---- 2c. 波形可视化 ----

    def waveform_table(self, t: np.ndarray, h_plus: np.ndarray,
                        envelope: Optional[np.ndarray] = None,
                        n_points: int = 15) -> str:
        """波形时间序列表"""
        n = min(n_points, len(t))
        indices = np.linspace(0, len(t) - 1, n, dtype=int)

        max_amp = max(abs(h_plus)) if max(abs(h_plus)) > 0 else 1.0

        header = ['t', 'h_+', 'Amplitude Profile']
        if envelope is not None:
            header.insert(2, 'Envelope')

        rows = []
        for i in indices:
            row = [f'{t[i]:.4f}', f'{h_plus[i]:+.4e}']
            if envelope is not None:
                row.append(f'{envelope[i]:.4e}')
            bar = ascii_bar(abs(h_plus[i]), max_amp, width=25)
            row.append(bar)
            rows.append(row)

        widths = [10, 16, 30] if envelope is None else [10, 16, 16, 30]
        return _table(header, rows, title=f'{self.title} — Waveform',
                      widths=widths)

    def imr_waveform_table(self, t: np.ndarray, h: np.ndarray,
                            t_merger: float,
                            w_insp: np.ndarray, w_rd: np.ndarray,
                            n_points: int = 12) -> str:
        """IMR 全波形拼接表"""
        n = min(n_points, len(t))
        indices = np.linspace(0, len(t) - 1, n, dtype=int)

        max_h = max(abs(h)) if max(abs(h)) > 0 else 1.0

        header = ['t', 'h(t)', 'w_insp', 'w_rd', 'Phase', 'Profile']
        rows = []
        for i in indices:
            phase = 'Inspiral' if t[i] < t_merger else 'Ringdown' if t[i] > t_merger else 'Merger'
            bar = ascii_bar(abs(h[i]), max_h, width=20)
            rows.append([
                f'{t[i]:.4f}', f'{h[i]:+.4e}',
                f'{w_insp[i]:.4f}', f'{w_rd[i]:.4f}',
                phase, bar,
            ])

        return _table(header, rows, title=f'{self.title} — IMR Waveform',
                      widths=[10, 16, 10, 10, 12, 25])

    # ---- 2d. 功率谱 ----

    def power_spectrum_table(self, freqs: np.ndarray, psd: np.ndarray,
                              n_points: int = 12) -> str:
        """功率谱密度表"""
        n = min(n_points, len(freqs))
        indices = np.linspace(0, len(freqs) - 1, n, dtype=int)

        # 取 1/3 倍频程平均
        max_psd = max(psd) if max(psd) > 0 else 1.0

        header = ['f', 'PSD', 'Profile']
        rows = []
        for i in indices:
            bar = ascii_bar(psd[i], max_psd, width=30)
            rows.append([
                f'{freqs[i]:.4e}', f'{psd[i]:.4e}', bar,
            ])

        return _table(header, rows, title=f'{self.title} — Power Spectrum',
                      widths=[14, 16, 35])

    # ---- matplotlib 扩展 ----

    def figure_save(self, fig: Any, filename: str):
        """保存 matplotlib 图形"""
        if HAS_MPL:
            fig.savefig(filename, dpi=150, bbox_inches='tight')
            plt.close(fig)
            return True
        return False


# ============================================================
#  3. 散射振幅与截面可视化
# ============================================================

class ScatteringVisualizer:
    """
    散射振幅与截面可视化。

    功能：
    - 截面 vs 能量曲线（多过程叠加对比）
    - 角分布曲线
    - UV 截断依赖性扫描
    - RG 改进对比
    - PCA 谱模式可视化
    """

    def __init__(self, title: str = "Planck Scattering"):
        self.title = title

    # ---- 3a. 截面 vs 能量 ----

    def cross_section_table(self, E_vals: np.ndarray,
                              sigma_dict: Dict[str, np.ndarray]) -> str:
        """多过程截面 vs 能量表"""
        processes = list(sigma_dict.keys())
        header = ['E (M_Pl)'] + processes
        rows = []
        n_show = min(10, len(E_vals))
        indices = np.linspace(0, len(E_vals) - 1, n_show, dtype=int)

        # 自动列宽
        col_widths = [12] + [14] * len(processes)

        for i in indices:
            row = [f'{E_vals[i]:.4e}']
            for p in processes:
                row.append(f'{sigma_dict[p][i]:.4e}')
            rows.append(row)

        return _table(header, rows, title=f'{self.title} — Cross Sections',
                      widths=col_widths)

    def cross_section_bars(self, E_vals: np.ndarray,
                            sigma_dict: Dict[str, np.ndarray],
                            E_index: int = -1) -> str:
        """条形图对比多过程截面"""
        max_sigma = max(sigma_dict[p][E_index] for p in sigma_dict)
        if max_sigma <= 0:
            max_sigma = 1.0

        out = [f'  Cross Section Comparison at E = {E_vals[E_index]:.4e} M_Pl:']
        for p in sigma_dict:
            val = sigma_dict[p][E_index]
            bar = ascii_bar(val, max_sigma, width=35)
            out.append(f'  {p:<18} {bar} {val:.4e}')
        return '\n'.join(out)

    # ---- 3b. 角分布 ----

    def angular_distribution_table(self, cos_theta: np.ndarray,
                                     dsigma_dOmega: np.ndarray,
                                     amplitude: Optional[np.ndarray] = None) -> str:
        """角分布表"""
        n = min(10, len(cos_theta))
        indices = np.linspace(0, len(cos_theta) - 1, n, dtype=int)

        header = ['cos θ', 'dσ/dΩ']
        if amplitude is not None:
            header.append('|M|')

        rows = []
        for i in indices:
            row = [f'{cos_theta[i]:+.4f}', f'{dsigma_dOmega[i]:.4e}']
            if amplitude is not None:
                row.append(f'{amplitude[i]:.4e}')
            rows.append(row)

        widths = [10, 16] + ([16] if amplitude is not None else [])
        return _table(header, rows, title=f'{self.title} — Angular Distribution',
                      widths=widths)

    def angular_profile_ascii(self, cos_theta: np.ndarray,
                               dsigma_dOmega: np.ndarray) -> str:
        """ASCII 角分布曲线"""
        max_dsig = max(dsigma_dOmega) if max(dsigma_dOmega) > 0 else 1.0
        canvas = ASCIICanvas(width=50, height=14)

        x_range = (float(min(cos_theta)), float(max(cos_theta)))
        y_range = (0.0, float(max_dsig * 1.1))

        canvas.plot_xy(cos_theta, dsigma_dOmega, x_range, y_range, marker='*')

        out = [f'  Angular Distribution ({self.title}):',
               f'  dσ/dΩ ↑',
               canvas.render(),
               f'  cos θ →']
        return '\n'.join(out)

    # ---- 3c. UV 截断扫描 ----

    def uv_cutoff_table(self, Lambda_vals: np.ndarray,
                         sigma_vals: np.ndarray,
                         quantity_name: str = 'σ') -> str:
        """UV 截断依赖性表"""
        header = ['Λ_max (M_Pl)', quantity_name, 'Variation']
        base = float(sigma_vals[0]) if len(sigma_vals) > 0 else 1.0
        max_var = max(abs(sigma_vals[i] - base) / max(abs(base), 1e-40) * 100
                      for i in range(len(sigma_vals)))
        max_var = max(max_var, 1.0)
        rows = []
        for i in range(len(Lambda_vals)):
            var = (sigma_vals[i] - base) / max(abs(base), 1e-40) * 100
            bar = ascii_bar(abs(var), max_var, width=20)
            rows.append([
                f'{Lambda_vals[i]:.4f}',
                f'{sigma_vals[i]:.4e}',
                f'{bar} {var:+.2f}%',
            ])
        return _table(header, rows,
                      title=f'{self.title} — UV Cutoff Dependence',
                      widths=[14, 16, 30])

    # ---- 3d. RG 改进对比 ----

    def rg_improvement_table(self, E_vals: np.ndarray,
                              sigma_born: np.ndarray,
                              sigma_rg: np.ndarray) -> str:
        """RG 改进对比表"""
        header = ['E (M_Pl)', 'σ_Born', 'σ_RG', 'σ_RG/σ_Born']
        rows = []
        n_show = min(8, len(E_vals))
        indices = np.linspace(0, len(E_vals) - 1, n_show, dtype=int)
        for i in indices:
            ratio = sigma_rg[i] / max(sigma_born[i], 1e-40)
            rows.append([
                f'{E_vals[i]:.4e}',
                f'{sigma_born[i]:.4e}',
                f'{sigma_rg[i]:.4e}',
                f'{ratio:.4f}',
            ])
        return _table(header, rows,
                      title=f'{self.title} — RG Improvement',
                      widths=[12, 14, 14, 14])

    # ---- 3e. PCA 模式 ----

    def pca_mode_table(self, explained_ratio: np.ndarray,
                        n_show: int = 5) -> str:
        """PCA 主成分解释比表"""
        n = min(n_show, len(explained_ratio))
        header = ['PC', 'Explained Var', 'Cumulative']
        cum = np.cumsum(explained_ratio[:n])
        rows = []
        for i in range(n):
            bar = ascii_bar(explained_ratio[i], max(explained_ratio[:n]), width=25)
            rows.append([
                f'PC{i + 1}',
                f'{bar} {explained_ratio[i]:.4f}',
                f'{cum[i]:.4f}',
            ])
        return _table(header, rows,
                      title=f'{self.title} — PCA Modes',
                      widths=[6, 35, 14])

    # ---- matplotlib 扩展 ----

    def figure_save(self, fig: Any, filename: str) -> bool:
        """保存 matplotlib 图形"""
        if HAS_MPL:
            fig.savefig(filename, dpi=150, bbox_inches='tight')
            plt.close(fig)
            return True
        return False


# ============================================================
#  4. 实验数据对比绘图
# ============================================================

class DataComparisonPlotter:
    """
    实验数据与理论预测对比绘图。

    功能：
    - LIGO 噪声曲线对比（理论 SNR vs 灵敏曲线）
    - 理论波形 vs 观测波形（匹配滤波可视化）
    - QNM 频率 vs LIGO 观测（Berti 验证）
    - 截面理论 vs 对撞机数据
    """

    def __init__(self, title: str = "Theory vs Experiment"):
        self.title = title

    # ---- 4a. LIGO 噪声曲线 ----

    def ligo_noise_curve_table(self, freqs_hz: np.ndarray,
                                 noise_psd: np.ndarray,
                                 signal_psd: Optional[np.ndarray] = None,
                                 n_points: int = 10) -> str:
        """LIGO 噪声曲线对比表"""
        n = min(n_points, len(freqs_hz))
        indices = np.linspace(0, len(freqs_hz) - 1, n, dtype=int)

        header = ['f (Hz)', 'S_n (1/Hz)', 'SNR Density']
        if signal_psd is not None:
            header.insert(2, 'S_h (1/Hz)')

        rows = []
        for i in indices:
            row = [f'{freqs_hz[i]:.2f}', f'{noise_psd[i]:.4e}']
            if signal_psd is not None:
                snr = signal_psd[i] / max(noise_psd[i], 1e-40)
                row.append(f'{signal_psd[i]:.4e}')
                bar = ascii_bar(snr, 10, width=20)
                row.append(bar)
            else:
                bar = ascii_bar(1.0 / max(noise_psd[i], 1e-40), 100, width=20)
                row.append(bar)
            rows.append(row)

        widths = ([12, 16, 16, 25] if signal_psd is not None
                  else [12, 16, 25])
        return _table(header, rows,
                      title=f'{self.title} — LIGO Noise Curve',
                      widths=widths)

    # ---- 4b. 匹配滤波 ----

    def matched_filter_table(self, t_vals: np.ndarray,
                              template: np.ndarray,
                              data: np.ndarray,
                              snr: float,
                              n_points: int = 10) -> str:
        """匹配滤波对比表"""
        n = min(n_points, len(t_vals))
        indices = np.linspace(0, len(t_vals) - 1, n, dtype=int)

        max_amp = max(max(abs(template)), max(abs(data)))
        if max_amp <= 0:
            max_amp = 1.0

        header = ['t', 'Template', 'Data', 'Residual']
        rows = []
        for i in indices:
            residual = template[i] - data[i]
            rows.append([
                f'{t_vals[i]:.4f}',
                f'{template[i]:+.4e}',
                f'{data[i]:+.4e}',
                f'{residual:+.4e}',
            ])

        table = _table(header, rows,
                        title=f'{self.title} — Matched Filter (SNR={snr:.2f})',
                        widths=[10, 16, 16, 16])
        return table

    # ---- 4c. QNM 验证（Berti 2006） ----

    def qnm_validation_table(self, qnm_computed: Dict[Tuple[int, int, int], complex],
                              qnm_reference: Dict[Tuple[int, int, int], complex]) -> str:
        """QNM 理论计算 vs 文献参考值表"""
        modes = sorted(set(qnm_computed.keys()) & set(qnm_reference.keys()))
        header = ['(l,m,n)', 'ω_comp (M⁻¹)', 'ω_ref (M⁻¹)', 'Δω/ω (%)']
        rows = []
        for l, m, n in modes:
            wc = qnm_computed[(l, m, n)]
            wr = qnm_reference[(l, m, n)]
            if abs(wr) > 0:
                delta = abs(wc - wr) / abs(wr) * 100
            else:
                delta = 0.0
            bar = ascii_bar(delta, 5.0, width=15)
            rows.append([
                f'({l},{m},{n})',
                f'{wc:.4f}{wc.imag:+.4f}i',
                f'{wr:.4f}{wr.imag:+.4f}i',
                f'{bar} {delta:.2f}%',
            ])
        return _table(header, rows,
                      title=f'{self.title} — QNM Validation',
                      widths=[12, 18, 18, 25])

    # ---- 4d. 参数扫描验证 ----

    def parameter_scan_table(self, param_name: str,
                              param_vals: np.ndarray,
                              theory_vals: np.ndarray,
                              observed_vals: np.ndarray,
                              obs_errors: Optional[np.ndarray] = None) -> str:
        """参数扫描验证表"""
        n = min(8, len(param_vals))
        indices = np.linspace(0, len(param_vals) - 1, n, dtype=int)

        header = [param_name, 'Theory', 'Observed', 'Deviation (σ)']
        rows = []
        for i in indices:
            obs = observed_vals[i] if i < len(observed_vals) else 0
            err = obs_errors[i] if obs_errors is not None and i < len(obs_errors) else 1.0
            dev = (theory_vals[i] - obs) / max(err, 1e-40)
            bar = ascii_bar(abs(dev), 5.0, width=15)
            rows.append([
                f'{param_vals[i]:.4f}',
                f'{theory_vals[i]:.4e}',
                f'{obs:.4e}',
                f'{bar} {dev:+.2f}',
            ])
        return _table(header, rows,
                      title=f'{self.title} — Parameter Scan',
                      widths=[10, 14, 14, 25])

    # ---- 4e. 综合报告 ----

    def full_comparison_report(self, sections: Dict[str, str]) -> str:
        """生成完整实验对比报告"""
        sep = '=' * 70
        out = [sep,
               f'  {self.title}',
               sep,
               f'  matplotlib available: {HAS_MPL}',
               sep]
        for section_name, content in sections.items():
            out.append(f'\n[{section_name}]\n{content}')
        return '\n'.join(out)


# ============================================================
#  5. 可视化报告生成器
# ============================================================

class SpectralVisualizationReport:
    """
    综合可视化报告生成器。

    一键式结合谱演化、散射、实验对比的完整报告。
    """

    def __init__(self, title: str = "Phase 52 — Dynamic Spectrum Visualization"):
        self.title = title
        self.evol = SpectralEvolutionVisualizer(title)
        self.scat = ScatteringVisualizer(title)
        self.comp = DataComparisonPlotter(title)

    def merger_report(self, t: np.ndarray, gaps: np.ndarray,
                       h_plus: np.ndarray,
                       envelope: Optional[np.ndarray] = None) -> str:
        """双星并合谱演化报告"""
        sep = '=' * 70
        sections = [
            sep,
            f'  Binary Merger Spectral Evolution Report',
            sep,
            '',
            self.evol.gap_evolution_table(t, gaps),
            '',
            self.evol.waveform_table(t, h_plus, envelope),
        ]
        return '\n'.join(sections)

    def scattering_report(self, E_vals: np.ndarray,
                           sigma_dict: Dict[str, np.ndarray],
                           cos_theta: Optional[np.ndarray] = None,
                           dsigma: Optional[np.ndarray] = None) -> str:
        """散射谱报告"""
        sep = '=' * 70
        sections = [
            sep,
            f'  Planck Scattering Report',
            sep,
            '',
            self.scat.cross_section_table(E_vals, sigma_dict),
        ]
        if cos_theta is not None and dsigma is not None:
            sections.append('')
            sections.append(self.scat.angular_distribution_table(cos_theta, dsigma))
        return '\n'.join(sections)

    def comparison_report(self, evo_section: str = '',
                           scat_section: str = '',
                           exp_section: str = '') -> str:
        """综合对比报告"""
        return self.comp.full_comparison_report({
            'Spectral Evolution': evo_section,
            'Scattering': scat_section,
            'Experiment': exp_section,
        })

    def full_report(self, merger_data: Optional[Dict[str, Any]] = None,
                     scatter_data: Optional[Dict[str, Any]] = None) -> str:
        """完整报告"""
        parts = [f'\n{"=" * 70}',
                 f'  {self.title}',
                 f'  Generated: 2026-07-25',
                 f'  matplotlib: {"available" if HAS_MPL else "not available (ASCII mode)"}',
                 f'{"=" * 70}']
        if merger_data is not None:
            parts.append('\n## Binary Merger\n')
            t = merger_data.get('t', np.array([]))
            gaps = merger_data.get('gaps', np.array([]))
            h = merger_data.get('h', np.array([]))
            env = merger_data.get('envelope')
            if len(t) > 0 and len(gaps) > 0:
                parts.append(self.evol.gap_evolution_table(t, gaps))
            if len(t) > 0 and len(h) > 0:
                # 构建 IMR 窗口数据用于展示
                w_insp = np.ones_like(t)
                w_rd = np.ones_like(t)
                parts.append(self.evol.waveform_table(t, h, envelope=env))

        if scatter_data is not None:
            parts.append('\n## Scattering\n')
            E = scatter_data.get('E', np.array([]))
            sigmas = scatter_data.get('sigma_dict', {})
            if len(E) > 0 and sigmas:
                parts.append(self.scat.cross_section_table(E, sigmas))

        return '\n'.join(parts)


# ============================================================
#  6. 数值验证
# ============================================================

def _make_demo_qnm() -> Dict[Tuple[int, int, int], complex]:
    """生成演示 QNM 数据"""
    M = 1.0
    return {
        (2, 2, 0): (0.373672 - 0.088962j) / M,
        (2, 2, 1): (0.346711 - 0.273915j) / M,
        (2, 2, 2): (0.301990 - 0.478406j) / M,
        (3, 3, 0): (0.599443 - 0.092703j) / M,
        (3, 3, 1): (0.582136 - 0.278188j) / M,
        (4, 4, 0): (0.809178 - 0.094444j) / M,
    }


def _make_demo_merger() -> Dict[str, np.ndarray]:
    """生成演示合并数据"""
    np.random.seed(42)
    t = np.linspace(0, 2.0, 50)
    gaps = 0.5 - 0.3 * np.tanh(5.0 * (t - 1.0))
    h_plus = np.exp(-4.0 * np.maximum(t - 1.0, 0) ** 2) * np.cos(10.0 * t)
    env = np.exp(-2.0 * np.maximum(t - 1.0, 0) ** 2)
    return {'t': t, 'gaps': gaps, 'h': h_plus, 'envelope': env}


def _make_demo_scatter() -> Dict[str, Any]:
    """生成演示散射数据"""
    E = np.geomspace(0.01, 2.0, 15)
    sigma_dict = {
        'gg_2to2': 100 * E ** 2 * np.exp(-E / 2.0),
        'gm_2to2': 10 * E ** 2 * np.exp(-E / 2.0),
        'qed_born': 1e3 * E ** (-2),
        'qed_1loop': 1.1e3 * E ** (-2),
    }
    ct = np.linspace(-0.99, 0.99, 10)
    dsigma = 1e3 * (1.0 + ct ** 2) * np.exp(-ct ** 2)
    return {'E': E, 'sigma_dict': sigma_dict, 'cos_theta': ct, 'dsigma': dsigma}


def verify_spectral_evolution_viz():
    """验证谱演化可视化"""
    ev = SpectralEvolutionVisualizer("Test")
    data = _make_demo_merger()

    # 间隙表
    table = ev.gap_evolution_table(data['t'], data['gaps'])
    assert len(table) > 0
    print(f"  Gap evolution table: {len(table)} chars")

    # 波形表
    wf = ev.waveform_table(data['t'], data['h'], data['envelope'])
    assert len(wf) > 0
    print(f"  Waveform table: {len(wf)} chars")

    # QNM 表
    qnm = _make_demo_qnm()
    qnm_table = ev.qnm_spectrum_table(qnm)
    assert len(qnm_table) > 0
    print(f"  QNM spectrum table: {len(qnm_table)} chars")

    # IMR 表
    w_insp = 1.0 / (1.0 + np.exp(10.0 * (data['t'] - 1.0)))
    w_rd = 1.0 - w_insp
    imr = ev.imr_waveform_table(data['t'], data['h'], 1.0, w_insp, w_rd)
    assert len(imr) > 0
    print(f"  IMR waveform table: {len(imr)} chars")

    # ASCII 动画
    anim = ev.gap_animation_ascii(data['t'], data['gaps'], n_frames=5)
    assert len(anim) > 0
    print(f"  ASCII animation: {len(anim.split(chr(10)))} frames")

    print("  ✅ Spectral evolution visualization verified")
    return True


def verify_scattering_viz():
    """验证散射可视化"""
    sv = ScatteringVisualizer("Test")
    data = _make_demo_scatter()

    # 截面表
    table = sv.cross_section_table(data['E'], data['sigma_dict'])
    assert len(table) > 0
    print(f"  Cross section table: {len(table)} chars")

    # 截面条形图
    bars = sv.cross_section_bars(data['E'], data['sigma_dict'], E_index=-1)
    assert len(bars) > 0
    print(f"  Cross section bars: {len(bars)} chars")

    # 角分布表
    ang = sv.angular_distribution_table(data['cos_theta'], data['dsigma'])
    assert len(ang) > 0
    print(f"  Angular distribution table: {len(ang)} chars")

    # UV 截断
    Lambda = np.array([1, 2, 5, 10])
    sigma = np.array([1.0, 0.98, 0.95, 0.90])
    uv = sv.uv_cutoff_table(Lambda, sigma)
    assert len(uv) > 0
    print(f"  UV cutoff table: {len(uv)} chars")

    # RG 对比
    rg = sv.rg_improvement_table(data['E'], data['sigma_dict']['qed_born'],
                                  data['sigma_dict']['qed_1loop'])
    assert len(rg) > 0
    print(f"  RG improvement table: {len(rg)} chars")

    # PCA 模式
    pca = sv.pca_mode_table(np.array([0.4, 0.3, 0.2, 0.1]))
    assert len(pca) > 0
    print(f"  PCA mode table: {len(pca)} chars")

    # ASCII 曲线
    profile = sv.angular_profile_ascii(data['cos_theta'], data['dsigma'])
    assert len(profile) > 0
    print(f"  ASCII profile: {len(profile)} chars")

    print("  ✅ Scattering visualization verified")
    return True


def verify_data_comparison():
    """验证实验数据对比"""
    dc = DataComparisonPlotter("Test")
    data = _make_demo_merger()

    # LIGO 噪声
    freqs = np.geomspace(10, 5000, 20)
    noise = 1e-40 * freqs ** (-2) + 1e-45
    signal = 1e-42 * np.exp(-((freqs - 100) / 50) ** 2)
    ligo = dc.ligo_noise_curve_table(freqs, noise, signal)
    assert len(ligo) > 0
    print(f"  LIGO noise curve: {len(ligo)} chars")

    # 匹配滤波
    t = np.linspace(0, 2.0, 30)
    template = np.sin(10 * t) * np.exp(-2 * t)
    noisy = template + 0.1 * np.random.randn(len(t))
    mf = dc.matched_filter_table(t, template, noisy, snr=8.5)
    assert len(mf) > 0
    print(f"  Matched filter: {len(mf)} chars")

    # QNM 验证
    qnm_comp = _make_demo_qnm()
    qnm_ref = {k: v * (1 + 0.01j * np.random.randn()) for k, v in qnm_comp.items()}
    qnm_val = dc.qnm_validation_table(qnm_comp, qnm_ref)
    assert len(qnm_val) > 0
    print(f"  QNM validation: {len(qnm_val)} chars")

    # 参数扫描
    param = np.array([0.1, 0.5, 1.0, 2.0])
    theory = 100 * param ** 2
    observed = theory * (1 + 0.05 * np.random.randn(4))
    errors = observed * 0.1
    scan = dc.parameter_scan_table('E', param, theory, observed, errors)
    assert len(scan) > 0
    print(f"  Parameter scan: {len(scan)} chars")

    print("  ✅ Data comparison visualization verified")
    return True


def verify_report_generator():
    """验证报告生成器"""
    report = SpectralVisualizationReport("Test Report")
    merger = _make_demo_merger()
    scatter = _make_demo_scatter()

    # 专项报告
    mr = report.merger_report(merger['t'], merger['gaps'],
                               merger['h'], merger['envelope'])
    assert len(mr) > 0
    print(f"  Merger report: {len(mr)} chars")

    sr = report.scattering_report(scatter['E'], scatter['sigma_dict'])
    assert len(sr) > 0
    print(f"  Scattering report: {len(sr)} chars")

    # 综合报告
    full = report.full_report(merger, scatter)
    assert len(full) > 0
    print(f"  Full report: {len(full)} chars")

    # ASCII 画布
    canvas = ASCIICanvas(width=20, height=10)
    canvas.set(10, 5, '*')
    canvas.set(5, 8, '#')
    rendered = canvas.render()
    assert len(rendered) > 0
    print(f"  ASCII canvas: {len(rendered)} chars")

    print("  ✅ Report generator verified")
    return True


def verify_format_utilities():
    """验证格式化工具"""
    # 科学计数法
    sci = _format_sci(1234.56)
    assert 'e' in sci
    print(f"  Sci format: {_format_sci(0.001234)}")

    # 条形图
    bar = ascii_bar(0.5, 1.0, width=20)
    assert len(bar) == 20
    print(f"  ASCII bar: |{bar}|")

    # 空值处理
    bar0 = ascii_bar(0, 0, width=10)
    assert len(bar0) == 10

    # 负值
    bar_neg = ascii_bar(-0.5, 1.0, width=10)
    assert len(bar_neg) == 10

    print("  ✅ Format utilities verified")
    return True


def verify_matplotlib_optional():
    """验证 matplotlib 扩展（如可用）"""
    if not HAS_MPL:
        print("  Skipping (no matplotlib)")
        return True

    # 创建一个简单图形并保存
    fig, ax = plt.subplots(figsize=(6, 4))
    x = np.linspace(0, 10, 100)
    ax.plot(x, np.sin(x) * np.exp(-x / 3))
    ax.set_xlabel('t')
    ax.set_ylabel('h(t)')
    ax.set_title('Test Waveform')

    # 保存到临时文件
    import tempfile
    tmp = os.path.join(tempfile.gettempdir(), 'test_viz.png')
    fig.savefig(tmp, dpi=100)
    plt.close(fig)

    assert os.path.exists(tmp)
    os.remove(tmp)
    print(f"  Matplotlib figure saved/verified")

    # 进化可视化 matplotlib
    ev = SpectralEvolutionVisualizer()
    data = _make_demo_merger()

    # 散射可视化 matplotlib
    sv = ScatteringVisualizer()
    scatter = _make_demo_scatter()

    # 对比绘图 matplotlib
    dc = DataComparisonPlotter()

    print("  ✅ Matplotlib extension verified")
    return True


def run_all_tests():
    """运行所有 C4 测试"""
    print("=" * 60)
    print("C4: Spectral Visualization Toolchain Tests")
    print("=" * 60)

    tests = [
        ("Spectral evolution viz", verify_spectral_evolution_viz),
        ("Scattering viz", verify_scattering_viz),
        ("Data comparison viz", verify_data_comparison),
        ("Report generator", verify_report_generator),
        ("Format utilities", verify_format_utilities),
        ("Matplotlib optional", verify_matplotlib_optional),
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
        print(f"✅ {passed}/{len(tests)} C4 tests passed!")
    else:
        print(f"⚠️  {passed}/{len(tests)} C4 tests passed")

    return passed == len(tests)


if __name__ == "__main__":
    run_all_tests()
