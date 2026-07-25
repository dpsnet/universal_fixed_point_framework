"""
natural_transform.py — 自然变换检验与谱交织条件
=================================================
实现谱纤维之间的自然变换等价性检验：
  - 投影算子谱交织条件
  - 链总误差传播计算
"""

import numpy as np

from .layer_base import FiberLayer, FibrationChain


def check_intertwining(A_i, A_j, projection_op):
    """检验两个谱流算子 A_i, A_j 之间的谱交织条件。

    交织条件要求：
      ‖A_i P - P A_j‖ < epsilon
    其中 P 为投影算子。

    Parameters
    ----------
    A_i : ndarray
        谱流算子 A_i 的矩阵表示。
    A_j : ndarray
        谱流算子 A_j 的矩阵表示。
    projection_op : ndarray
        投影算子 P 的矩阵表示。

    Returns
    -------
    epsilon : float
        实际交织误差 ‖A_i P - P A_j‖。
    passed : bool
        若 epsilon < 0.05 则认为通过。
    """
    A_i = np.asarray(A_i, dtype=float)
    A_j = np.asarray(A_j, dtype=float)
    P = np.asarray(projection_op, dtype=float)

    commutator = A_i @ P - P @ A_j
    epsilon = float(np.linalg.norm(commutator, ord=2))
    passed = epsilon < 0.05
    return epsilon, passed


def natural_transform_error(chain):
    """计算纤维链上所有自然变换的总误差。

    对链中每对相邻层，使用谱流数值差作为变换误差，
    返回各误差的 2-范数。

    Parameters
    ----------
    chain : FibrationChain
        待评估的纤维链。

    Returns
    -------
    total_error : float
        所有相邻层谱流差异的 2-范数。
    epsilon_per_pair : list of float
        每对相邻层各自的误差。
    """
    errors = []
    xi_test = np.linspace(-1, 1, 20)

    for i in range(len(chain.layers) - 1):
        try:
            flow_i = chain.layers[i].compute_spectral_flow(xi_test)
            flow_j = chain.layers[i + 1].compute_spectral_flow(xi_test)
            err = float(np.linalg.norm(flow_i - flow_j))
        except Exception:
            err = np.inf
        errors.append(err)

    total = float(np.sqrt(sum(e ** 2 for e in errors
                              if np.isfinite(e))))
    return total, errors


def intertwining_matrix(chain, xi_test=None):
    """计算纤维链上所有层对之间的谱交织误差矩阵。

    Parameters
    ----------
    chain : FibrationChain
        纤维链。
    xi_test : ndarray or None
        谱流测试坐标。默认 linspace(-1, 1, 20)。

    Returns
    -------
    matrix : ndarray
        n_layers × n_layers 的误差矩阵（对称）。
    """
    if xi_test is None:
        xi_test = np.linspace(-1, 1, 20)

    n = len(chain.layers)
    mat = np.zeros((n, n))

    for i in range(n):
        for j in range(i + 1, n):
            try:
                flow_i = chain.layers[i].compute_spectral_flow(xi_test)
                flow_j = chain.layers[j].compute_spectral_flow(xi_test)
                err = float(np.linalg.norm(flow_i - flow_j))
            except Exception:
                err = np.inf
            mat[i, j] = err
            mat[j, i] = err

    return mat
