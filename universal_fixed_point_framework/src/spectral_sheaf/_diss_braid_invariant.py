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
_diss_braid_invariant.py

Phase 59C-54C.2: Rec_diss 谱不变量与辫子交叉数计算

功能：
1. Koopman 算子构造与谱计算
2. 非正规性度量（交换子范数、条件数）
3. 伪谱计算
4. 辫子交叉数估算（基于单值群置换）
5. D_diss 谱不变量计算
"""

from __future__ import annotations

import numpy as np
from typing import Dict, Optional, Tuple
from scipy.linalg import eigvals, norm, svdvals


# ─── 1. Koopman 算子构造 ────────────────────────────────────────

def construct_koopman(alpha: np.ndarray, beta: np.ndarray,
                      gamma: np.ndarray) -> np.ndarray:
    """
    从 Leaver 三项递推系数构造 Koopman 算子。

    递推: alpha_n * a_{n+1} + beta_n * a_n + gamma_n * a_{n-1} = 0
    展开为 2N×2N 稀疏矩阵 K:
        K[2n, 2n]   = -beta_n / alpha_n
        K[2n, 2n+1] = -gamma_n / alpha_n
        K[2n+1, 2n] = 1
        K[2n+1, 2n+1] = 0

    Parameters
    ----------
    alpha, beta, gamma : ndarray, shape (N,)
        递推系数（已评估于特定 omega）。

    Returns
    -------
    K : ndarray, shape (2N, 2N)
        Koopman 算子矩阵。
    """
    N = len(alpha)
    K = np.zeros((2 * N, 2 * N), dtype=complex)

    for n in range(N):
        if abs(alpha[n]) > 1e-30:
            K[2 * n, 2 * n] = -beta[n] / alpha[n]
            K[2 * n, 2 * n + 1] = -gamma[n] / alpha[n]
        K[2 * n + 1, 2 * n] = 1.0

    return K


# ─── 2. 非正规性度量 ────────────────────────────────────────────

def nonnormality_measures(U: np.ndarray) -> Dict[str, float]:
    """
    计算 Koopman 算子的非正规性度量。

    Parameters
    ----------
    U : ndarray, shape (M, M)
        Koopman 算子。

    Returns
    -------
    measures : dict
        nu1: 交换子范数 ||U^†U - UU^†|| / ||U||^2
        nu2: 条件数 cond(U)
        nu3: 伪谱半径比 (max ||(zI-U)^{-1}||) / epsilon
        spectral_radius: 谱半径 max|λ|
    """
    measures = {}

    # nu1: 交换子范数
    commutator = U.conj().T @ U - U @ U.conj().T
    measures["nu1"] = norm(commutator, 2) / (norm(U, 2) ** 2 + 1e-30)

    # nu2: 条件数
    measures["nu2"] = np.linalg.cond(U)

    # 谱半径
    evals = eigvals(U)
    measures["spectral_radius"] = np.max(np.abs(evals))

    # nu3: 伪谱指标（粗估计）
    try:
        U_inv = np.linalg.inv(U)
        measures["nu3"] = norm(U_inv, 2) * norm(U, 2)
    except np.linalg.LinAlgError:
        measures["nu3"] = np.inf

    return measures


# ─── 3. 伪谱计算（网格法） ──────────────────────────────────────

def pseudospectrum(U: np.ndarray, epsilon: float = 1e-3,
                   n_grid: int = 50) -> Dict:
    """
    计算 Koopman 算子的 epsilon-伪谱区域。

    Parameters
    ----------
    U : ndarray, shape (M, M)
    epsilon : float
        伪谱容差。
    n_grid : int
        网格密度（用于可视化需要，非网格法时使用 SVD）。

    Returns
    -------
    result : dict
        spectral_set: 谱集
        pseudo_radius: 伪谱半径
        condition_estimate: 条件数估计
    """
    evals = eigvals(U)
    M = U.shape[0]

    # 使用 SVD 估计伪谱半径 (||(zI-U)^{-1}|| 的峰值)
    # 粗略方法: 在谱附近采样
    sample_points = []
    for ev in evals:
        for r in [0.01, 0.05, 0.1, 0.5]:
            for theta in np.linspace(0, 2 * np.pi, 8):
                sample_points.append(ev + r * np.exp(1j * theta))

    resolvent_norms = []
    for z in sample_points:
        try:
            R = np.linalg.inv(z * np.eye(M) - U)
            resolvent_norms.append(norm(R, 2))
        except np.linalg.LinAlgError:
            resolvent_norms.append(np.inf)

    resolvent_norms = np.array(resolvent_norms)
    pseudo_radius = np.max(resolvent_norms)

    # 伪谱区域面积估计
    n_singular = np.sum(resolvent_norms > 1.0 / epsilon)

    return {
        "spectral_set": evals,
        "pseudo_radius": float(pseudo_radius),
        "pseudo_area_fraction": float(n_singular / len(sample_points)),
        "spectral_gap": float(_spectral_gap(evals)),
    }


def _spectral_gap(evals: np.ndarray) -> float:
    """计算谱间隙。"""
    sorted_abs = np.sort(np.abs(evals))
    if len(sorted_abs) < 2:
        return 0.0
    return float(sorted_abs[-1] - sorted_abs[-2])


# ─── 4. 辫子交叉数估算 ────────────────────────────────────────

def braid_crossing_number(U_sequence: list) -> int:
    """
    沿参数路径估算辫子交叉数。

    对 Koopman 算子序列 {U_k}，计算相邻算子的谱叶置换，累加为交叉数。

    Parameters
    ----------
    U_sequence : list of ndarray
        沿同伦路径的 Koopman 算子序列 [U_0, U_1, ..., U_K]。

    Returns
    -------
    k : int
        总辫子交叉数（最小对换分解长度之和）。
    """
    k_total = 0
    prev_evals = eigvals(U_sequence[0])

    for U_cur in U_sequence[1:]:
        cur_evals = eigvals(U_cur)

        # 匈牙利匹配：找出最近的谱叶对应关系
        n = len(prev_evals)
        cost = np.abs(prev_evals[:, None] - cur_evals[None, :])
        from scipy.optimize import linear_sum_assignment
        row_ind, col_ind = linear_sum_assignment(cost)

        # 置换与交叉数
        permutation = col_ind[np.argsort(row_ind)]
        k_total += _permutation_crossings(permutation)

        prev_evals = cur_evals[col_ind[np.argsort(row_ind)]]

    return k_total


def _permutation_crossings(perm: np.ndarray) -> int:
    """
    计算置换的最小相邻对换分解长度（逆序数）。

    Parameters
    ----------
    perm : ndarray
        置换数组 (perm[i] = 元素 i 的新位置)。

    Returns
    -------
    k : int
        逆序数 = 最小相邻对换分解长度。
    """
    n = len(perm)
    inv_count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if perm[i] > perm[j]:
                inv_count += 1
    return inv_count


# ─── 5. D_diss 谱不变量 ─────────────────────────────────────────

def diss_spectral_invariants(U: np.ndarray) -> Dict:
    """
    计算 D_diss 谱不变量集合。

    Parameters
    ----------
    U : ndarray, shape (M, M)

    Returns
    -------
    invariants : dict
        gamma: 谱间隙
        pseudo_bound: 伪谱扰动界 C
        nonnormality: 非正规性度量
        effective_dim: 有效维数
    """
    evals = eigvals(U)
    sorted_abs = np.sort(np.abs(evals))

    # 谱间隙
    gamma = _spectral_gap(evals)

    # 伪谱扰动界（估计）
    nonnorm = nonnormality_measures(U)
    C_est = nonnorm["nu2"] / (nonnorm["spectral_radius"] + 1e-30)

    # 有效维数（基于谱能量分布）
    energy_frac = np.cumsum(sorted_abs[::-1]) / np.sum(sorted_abs)
    eff_dim = int(np.sum(energy_frac < 0.95)) + 1

    return {
        "gamma": gamma,
        "pseudo_bound_C": float(C_est),
        "nu2_condition": nonnorm["nu2"],
        "spectral_radius": nonnorm["spectral_radius"],
        "effective_dimension": eff_dim,
    }


# ─── 6. 综合验证 ────────────────────────────────────────────────

def run_braid_invariant_validation(
    omegas_list: list,
    alpha_fn, beta_fn, gamma_fn,
) -> Dict:
    """
    综合验证辫子交叉数与 D_diss 不变量的对应关系。

    Parameters
    ----------
    omegas_list : list of list of complex
        沿同伦路径的 QNM 频率序列（每组对应一个同伦路径）。
    alpha_fn, beta_fn, gamma_fn : callable
        递推系数函数 alpha_n(omega, n) 等。

    Returns
    -------
    results : dict
        包含所有不变量和相关性的字典。
    """
    all_ks = []
    all_gammas = []

    for omegas in omegas_list:
        U_seq = []
        for omega in omegas:
            N = 100
            al = np.array([alpha_fn(omega, n) for n in range(N)])
            be = np.array([beta_fn(omega, n) for n in range(N)])
            ga = np.array([gamma_fn(omega, n) for n in range(N)])
            U_seq.append(construct_koopman(al, be, ga))

        # 辫子交叉数
        k = braid_crossing_number(U_seq)

        # 终点 D_diss 不变量
        inv = diss_spectral_invariants(U_seq[-1])

        all_ks.append(k)
        all_gammas.append(inv["gamma"])

    # 计算 Spearman 相关性
    from scipy.stats import spearmanr
    rho, p_value = spearmanr(all_ks, all_gammas)

    return {
        "ks": all_ks,
        "gammas": all_gammas,
        "spearman_rho": float(rho),
        "spearman_p": float(p_value),
        "correlation_significant": bool(p_value < 0.05),
    }


if __name__ == "__main__":
    # 简单自测
    print("=" * 50)
    print("D_diss 辫子不变量模块自测")
    print("=" * 50)

    # 构造一个简单 Koopman 算子
    N = 10
    np.random.seed(42)
    alpha = np.ones(N, dtype=complex) * (1.0 + 0.0j)
    beta = np.ones(N, dtype=complex) * (-2.0 + 0.0j)
    gamma = np.ones(N, dtype=complex) * (1.0 + 0.0j)

    U = construct_koopman(alpha, beta, gamma)
    print(f"\nKoopman 算子形状: {U.shape}")

    # 非正规性度量
    measures = nonnormality_measures(U)
    print(f"\n非正规性度量:")
    for k, v in measures.items():
        print(f"  {k}: {v:.4f}")

    # D_diss 不变量
    inv = diss_spectral_invariants(U)
    print(f"\nD_diss 谱不变量:")
    for k, v in inv.items():
        print(f"  {k}: {v:.4f}")

    # 伪谱
    ps = pseudospectrum(U, epsilon=1e-3)
    print(f"\n伪谱:")
    print(f"  pseudo_radius: {ps['pseudo_radius']:.4f}")
    print(f"  spectral_gap:  {ps['spectral_gap']:.4f}")
    print(f"  伪谱面积比:    {ps['pseudo_area_fraction']:.4f}")

    print("\n✅ 自测完成")
