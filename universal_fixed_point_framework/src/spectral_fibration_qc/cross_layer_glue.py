"""
cross_layer_glue.py — 跨界粘合实现
====================================
实现 §4.4 的跨界粘合公式，将高层（高分辨率）和低层（低分辨率）
的谱流通过 delta_spec 间隙和 kappa 耦合系数粘合。

公式：
  A_cross = A_high ⊗ A_low + kappa · δ_spec · (|high><low| + |low><high|)
其中 δ_spec 为谱间隙，kappa 为跨界耦合强度。
"""

import numpy as np

from .layer_base import FiberLayer
from .utils import convert_numpy, L_CORR_DEFAULT


def cross_layer_glue(A_high, A_low, delta_spec, kappa=0.05):
    """跨界粘合：将高层和低层谱流粘合为跨界流。

    Parameters
    ----------
    A_high : ndarray
        高层（高分辨率）的谱流矩阵 (n_high × n_high)。
    A_low : ndarray
        低层（低分辨率）的谱流矩阵 (n_low × n_low)。
    delta_spec : float
        两层之间的谱间隙 [eV]。
    kappa : float
        跨界耦合强度参数，默认 0.05。

    Returns
    -------
    A_cross : ndarray
        粘合后的跨界谱流矩阵 ((n_high + n_low) × (n_high + n_low))。

    Notes
    -----
    粘合矩阵的分块结构：
    ┌─────────────────┬──────────────────┐
    │  A_high          │  kappa·δ_spec·I  │
    │  (n_high×n_high) │  (n_high×n_low)  │
    ├─────────────────┼──────────────────┤
    │  kappa·δ_spec·I  │  A_low           │
    │  (n_low×n_high)  │  (n_low×n_low)   │
    └─────────────────┴──────────────────┘
    """
    A_high = np.asarray(A_high, dtype=float)
    A_low = np.asarray(A_low, dtype=float)
    n_high = A_high.shape[0]
    n_low = A_low.shape[0]

    # 构造分块粘合矩阵
    A_cross = np.zeros((n_high + n_low, n_high + n_low))

    # 对角块
    A_cross[:n_high, :n_high] = A_high
    A_cross[n_high:, n_high:] = A_low

    # 非对角块：耦合项 kappa · δ_spec
    coupling = kappa * delta_spec
    for i in range(min(n_high, n_low)):
        A_cross[i, n_high + i] = coupling
        A_cross[n_high + i, i] = coupling

    return A_cross


def glue_layers(high_layer, low_layer, kappa=0.05, xi_test=None):
    """将两个 FiberLayer 的谱流通过跨界粘合合并。

    Parameters
    ----------
    high_layer : FiberLayer
        高层（高分辨率）纤维层。
    low_layer : FiberLayer
        低层（低分辨率）纤维层。
    kappa : float
        跨界耦合强度，默认 0.05。
    xi_test : ndarray or None
        测试坐标，默认为 linspace(-1, 1, 5)。

    Returns
    -------
    A_cross : ndarray
        粘合后的跨界流矩阵。
    """
    if xi_test is None:
        xi_test = np.linspace(-1, 1, 5)

    # 获取两层的谱流
    flow_high = high_layer.compute_spectral_flow(xi_test)
    flow_low = low_layer.compute_spectral_flow(xi_test)

    # 构造对角谱流矩阵（作为流算子的简化表示）
    A_high = np.diag(flow_high)
    A_low = np.diag(flow_low)

    # 谱间隙取两层间隙的平均
    summary_high = high_layer.get_summary()
    summary_low = low_layer.get_summary()
    delta_spec = 0.5 * (summary_high.get("spectral_gap", 0.0) +
                        summary_low.get("spectral_gap", 0.0))

    return cross_layer_glue(A_high, A_low, delta_spec, kappa)


def glue_chain(chain, kappa=0.05):
    """将 FibrationChain 中所有相邻层依次粘合。

    Parameters
    ----------
    chain : FibrationChain
        待粘合的纤维链。
    kappa : float
        跨界耦合强度。

    Returns
    -------
    A_total : ndarray
        所有层依次粘合后的总跨界流矩阵。
    glued_pairs : list of dict
        每对粘合的信息。
    """
    if len(chain.layers) < 2:
        raise ValueError("链中至少需要 2 层才能粘合")

    glued_pairs = []
    xi_test = np.linspace(-1, 1, 5)

    # 从第一对开始
    A_cross = glue_layers(chain.layers[0], chain.layers[1],
                          kappa=kappa, xi_test=xi_test)
    glued_pairs.append({
        "high": chain.layers[0].name,
        "low": chain.layers[1].name,
        "dim": A_cross.shape[0],
    })

    # 依次粘合剩余层
    for i in range(2, len(chain.layers)):
        prev_flow = chain.layers[i - 1].compute_spectral_flow(xi_test)
        curr_flow = chain.layers[i].compute_spectral_flow(xi_test)
        A_prev = np.diag(prev_flow)
        A_curr = np.diag(curr_flow)

        summary_prev = chain.layers[i - 1].get_summary()
        summary_curr = chain.layers[i].get_summary()
        delta_spec = 0.5 * (summary_prev.get("spectral_gap", 0.0) +
                            summary_curr.get("spectral_gap", 0.0))

        # 扩展到粘合后的总矩阵
        n_existing = A_cross.shape[0]
        n_new = A_curr.shape[0]
        A_new = np.zeros((n_existing + n_new, n_existing + n_new))
        A_new[:n_existing, :n_existing] = A_cross
        A_new[n_existing:, n_existing:] = A_curr

        coupling = kappa * delta_spec
        for j in range(min(n_existing, n_new)):
            A_new[j, n_existing + j] = coupling
            A_new[n_existing + j, j] = coupling

        A_cross = A_new
        glued_pairs.append({
            "high": chain.layers[i - 1].name,
            "low": chain.layers[i].name,
            "dim": A_cross.shape[0],
        })

    return A_cross, glued_pairs
