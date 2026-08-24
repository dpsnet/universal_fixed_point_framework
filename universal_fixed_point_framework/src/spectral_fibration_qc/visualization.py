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

"""
visualization.py — 统一可视化模块
====================================
使用 matplotlib 'Agg' 后端生成谱纤维分析所需的图表：
  - 各层谱间隙柱状图
  - 嵌套纤维链图
  - 谱交织条件矩阵热力图
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np

from .layer_base import FiberLayer, FibrationChain
from .layer_reac import ReacLayer
from .layer_corr import CorrLayer
from .layer_vib import VibLayer
from .layer_intraionic import IntraIonicLayer
from .layer_ionic import IonicLayer
from .layer_solv import SolvLayer
from .layer_spin import SpinLayer
from .natural_transform import intertwining_matrix

# ── 全局绘图设置 ──
rcParams['font.family'] = 'DejaVu Sans'
rcParams['axes.unicode_minus'] = False
rcParams['figure.dpi'] = 120


def plot_layer_summary(layers, figsize=(10, 6), save_path=None):
    """绘制各层的谱间隙柱状图。

    Parameters
    ----------
    layers : list of FiberLayer
        待展示的纤维层列表。
    figsize : tuple
        图形尺寸。
    save_path : str or None
        保存路径，None 时返回 figure。

    Returns
    -------
    fig : Figure or None
    """
    names = []
    gaps = []
    dims = []
    gammas = []

    for layer in layers:
        summary = layer.get_summary()
        names.append(summary.get("name", layer.name))
        gaps.append(summary.get("spectral_gap", 0.0))
        dims.append(summary.get("fiber_dim", 1))
        gammas.append(summary.get("dissipation_gamma", 0.0))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

    x = np.arange(len(names))
    colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(names)))

    # 左图：谱间隙
    bars1 = ax1.bar(x, gaps, color=colors, alpha=0.8, edgecolor='black', lw=0.5)
    ax1.set_xlabel('Layer')
    ax1.set_ylabel(r'Spectral gap $\delta_{\rm spec}$ (eV)')
    ax1.set_title('Spectral gap by layer')
    ax1.set_xticks(x)
    ax1.set_xticklabels(names, rotation=45, ha='right', fontsize=9)
    ax1.grid(True, alpha=0.3, axis='y')

    # 在柱上标值
    for bar, gap in zip(bars1, gaps):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                 f'{gap:.3f}', ha='center', va='bottom', fontsize=8)

    # 右图：纤维维数与 dissipation
    ax2_twin = ax2.twinx()
    bars2 = ax2.bar(x - 0.2, dims, width=0.35, color='#2196F3', alpha=0.7,
                    label='Fiber dim')
    bars3 = ax2_twin.bar(x + 0.2, gammas, width=0.35, color='#FF5722', alpha=0.7,
                         label=r'$\gamma$')
    ax2.set_xlabel('Layer')
    ax2.set_ylabel('Fiber dimension')
    ax2_twin.set_ylabel(r'Dissipation $\gamma$')
    ax2.set_title('Fiber dimension & dissipation')
    ax2.set_xticks(x)
    ax2.set_xticklabels(names, rotation=45, ha='right', fontsize=9)
    ax2.legend(loc='upper left', fontsize=8)
    ax2_twin.legend(loc='upper right', fontsize=8)
    ax2.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        return None
    return fig


def plot_fibration_chain(chain, figsize=(12, 4), save_path=None):
    """绘制嵌套纤维链图。

    Parameters
    ----------
    chain : FibrationChain
        待展示的纤维链。
    figsize : tuple
        图形尺寸。
    save_path : str or None
        保存路径。

    Returns
    -------
    fig : Figure or None
    """
    n_layers = len(chain.layers)
    if n_layers == 0:
        return None

    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(-0.5, n_layers - 0.5)
    ax.set_ylim(-1, 1)
    ax.set_aspect('equal')
    ax.axis('off')

    colors = plt.cm.Set2(np.linspace(0, 1, n_layers))

    for i, layer in enumerate(chain.layers):
        summary = layer.get_summary()
        gap = summary.get("spectral_gap", 0.0)
        label = f"{layer.name}\ngap={gap:.3f}eV"

        # 绘制纤维层圆圈
        circle = plt.Circle((i, 0), 0.35 + 0.05 * layer.fiber_dim,
                            color=colors[i], alpha=0.7, ec='black', lw=1.5)
        ax.add_patch(circle)
        ax.text(i, 0, label, ha='center', va='center', fontsize=8,
                fontweight='bold')

        # 层间箭头（自然变换）
        if i < n_layers - 1:
            ax.annotate('', xy=(i + 0.5, 0.15), xytext=(i + 0.5, -0.15),
                        arrowprops=dict(arrowstyle='<->', color='gray',
                                        lw=1.5, alpha=0.6))
            eps = chain.transforms[i].intertwining_epsilon if i < len(
                chain.transforms) else 0.05
            ax.text(i + 0.5, 0.25, f'η={eps}', ha='center', va='bottom',
                    fontsize=7, color='gray')

    ax.set_title('Spectral Fibration Chain', fontsize=13, fontweight='bold')

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        return None
    return fig


def plot_intertwining_matrix(chain, figsize=(8, 7), save_path=None):
    """绘制谱交织条件矩阵热力图。

    Parameters
    ----------
    chain : FibrationChain
        纤维链。
    figsize : tuple
        图形尺寸。
    save_path : str or None
        保存路径。

    Returns
    -------
    fig : Figure or None
    """
    n = len(chain.layers)
    if n == 0:
        return None

    mat = intertwining_matrix(chain)
    names = chain.get_layer_names()

    fig, ax = plt.subplots(figsize=figsize)
    im = ax.imshow(mat, cmap='YlOrRd', aspect='auto', interpolation='nearest')

    cbar = plt.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label('Intertwining error', fontsize=10)

    ax.set_xticks(np.arange(n))
    ax.set_yticks(np.arange(n))
    ax.set_xticklabels(names, rotation=45, ha='right', fontsize=9)
    ax.set_yticklabels(names, fontsize=9)
    ax.set_title('Intertwining Condition Matrix', fontsize=13, fontweight='bold')

    # 在格子中标值
    for i in range(n):
        for j in range(n):
            val = mat[i, j]
            if np.isfinite(val):
                color = 'white' if val > mat.max() * 0.5 else 'black'
                ax.text(j, i, f'{val:.3f}', ha='center', va='center',
                        fontsize=7, color=color)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        return None
    return fig
