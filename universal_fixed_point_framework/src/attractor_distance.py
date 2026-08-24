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
attractor_distance.py

局部吸引子与全域不动点距离度量的计算工具。

核心指标：
1. 残差范数 rho: ||F(V) - V||
2. 吸引子分散度 Delta: 多初始点收敛解之间的最大距离
3. 谱间隙 gamma: 1 - max(|lambda_i| < 1)
4. 局部吸引子捕获指数 LACI
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable
import numpy as np
from scipy.linalg import eigvals

from fixed_point_solver import FixedPointSolver
from rec_category import RecObject
from spec_category import PositiveSpectralObject


@dataclass
class AttractorMetrics:
    """局部吸引子捕获的几何度量。"""
    residual: float          # 不动点残差 rho
    dispersion: float        # 吸引子分散度 Delta
    spectral_gap: float      # 谱间隙 gamma
    perturbation_sensitivity: float  # 扰动敏感度 chi
    laci: float              # 局部吸引子捕获指数


def hutchinson_residual(K: np.ndarray, mu: np.ndarray) -> float:
    """
    计算 Hutchinson 测度不动点残差：
        rho = ||K @ mu - mu||
    """
    return float(np.linalg.norm(K @ mu - mu))


def spectral_gap(K: np.ndarray, tol: float = 1e-10) -> float:
    """
    计算转移矩阵 K 的谱间隙。

    对列随机矩阵，最大特征值为 1。谱间隙定义为
        gamma = 1 - max(|lambda_i|) for |lambda_i| < 1
    """
    eigenvalues = eigvals(K)
    magnitudes = np.abs(eigenvalues)
    # 排除最大特征值（通常为 1）
    sub_dominant = magnitudes[magnitudes < 1.0 - tol]
    if len(sub_dominant) == 0:
        return 0.0
    return float(1.0 - np.max(sub_dominant))


def attractor_dispersion(
    F: Callable[[np.ndarray], np.ndarray],
    dim: int,
    n_trials: int = 10,
    max_iter: int = 1000,
    tol: float = 1e-10,
    distance: Callable[[np.ndarray, np.ndarray], float] | None = None,
) -> tuple[float, list[np.ndarray]]:
    """
    从多个随机初始点运行不动点迭代，计算收敛解的分散度。

    参数
    ----------
    F : Callable
        不动点映射。
    dim : int
        状态空间维度。
    n_trials : int
        随机初始点数量。
    max_iter, tol : 迭代参数
    distance : Callable, optional
        距离函数，默认欧几里得范数。

    返回
    -------
    (Delta, fixed_points)
    """
    if distance is None:
        distance = lambda a, b: float(np.linalg.norm(a - b))

    fixed_points = []
    for _ in range(n_trials):
        x0 = np.random.rand(dim)
        x0 = x0 / x0.sum() if x0.sum() > 0 else x0
        result = FixedPointSolver.solve_generic(
            F=F,
            x0=x0,
            distance=distance,
            tol=tol,
            max_iter=max_iter,
        )
        if result.converged:
            fixed_points.append(np.asarray(result.fixed_point).flatten())

    if len(fixed_points) < 2:
        return 0.0, fixed_points

    Delta = 0.0
    for i in range(len(fixed_points)):
        for j in range(i + 1, len(fixed_points)):
            d = distance(fixed_points[i], fixed_points[j])
            if d > Delta:
                Delta = d
    return Delta, fixed_points


def perturbation_sensitivity(
    F: Callable[[np.ndarray], np.ndarray],
    V: np.ndarray,
    epsilon: float = 1e-6,
) -> float:
    """
    计算不动点残差对 V 的扰动敏感度：
        chi = ||F(V + eps * dV) - (V + eps * dV)|| / epsilon
    其中 dV 是随机单位方向。
    """
    dV = np.random.randn(*V.shape)
    dV = dV / (np.linalg.norm(dV) + 1e-30)
    V_perturbed = V + epsilon * dV
    residual_perturbed = float(np.linalg.norm(F(V_perturbed) - V_perturbed))
    return residual_perturbed / epsilon


def compute_laci(
    K: np.ndarray,
    mu: np.ndarray,
    rho_ref: float = 1e-6,
    Delta_ref: float = 1.0,
    gamma_ref: float = 0.5,
    epsilon: float = 1e-12,
) -> AttractorMetrics:
    """
    计算局部吸引子捕获指数 LACI。

    参数
    ----------
    K : np.ndarray
        转移矩阵（Frobenius-Perron 型）。
    mu : np.ndarray
        当前数值解（Hutchinson 测度）。
    rho_ref, Delta_ref, gamma_ref : float
        参考值，用于归一化。
    epsilon : float
        避免除零。
    """
    rho = hutchinson_residual(K, mu)
    gamma = spectral_gap(K)
    Delta, _ = attractor_dispersion(
        F=lambda x: K @ x / (K @ x).sum(),
        dim=len(mu),
        n_trials=10,
    )
    chi = perturbation_sensitivity(
        F=lambda x: K @ x / (K @ x).sum(),
        V=mu,
    )

    laci = (
        rho / (rho_ref + epsilon)
        + Delta / (Delta_ref + epsilon)
        + 1.0 / (gamma / (gamma_ref + epsilon) + epsilon)
    )

    return AttractorMetrics(
        residual=rho,
        dispersion=Delta,
        spectral_gap=gamma,
        perturbation_sensitivity=chi,
        laci=laci,
    )


def diagnose_rec_object(K: np.ndarray, mu: np.ndarray) -> dict:
    """
    对给定的转移矩阵 K 和测度 mu 输出过拟合诊断报告。
    """
    metrics = compute_laci(K, mu)
    return {
        "residual": metrics.residual,
        "dispersion": metrics.dispersion,
        "spectral_gap": metrics.spectral_gap,
        "perturbation_sensitivity": metrics.perturbation_sensitivity,
        "laci": metrics.laci,
        "risk_level": (
            "high" if metrics.laci > 100
            else "medium" if metrics.laci > 10
            else "low"
        ),
    }


def diagnose_rec_object_from_instance(rec: RecObject) -> dict:
    """
    对 Rec 对象直接输出 LACI 诊断报告。

    要求 rec.evolution 为 Koopman/Frobenius-Perron 转移矩阵 K。
    测度 mu 通过 Hutchinson 不动点迭代求得。
    """
    if not isinstance(rec.evolution, np.ndarray):
        raise TypeError("当前原型仅支持 evolution 为矩阵的 RecObject")
    K = rec.evolution
    # 求解 Hutchinson 不变测度作为当前数值解
    result = FixedPointSolver.solve_hutchinson_measure(K)
    mu = result.fixed_point
    return diagnose_rec_object(K, mu)


def diagnose_spectral_object(spec: PositiveSpectralObject) -> dict:
    """
    对 Spec 对象输出 LACI 诊断报告。

    将谱算子 A 的 Koopman 矩阵 K = exp(-A) 视为转移矩阵，
    求解其 Hutchinson 不变测度后计算 LACI。
    """
    K = spec.koopman_matrix
    result = FixedPointSolver.solve_hutchinson_measure(K)
    mu = result.fixed_point
    return diagnose_rec_object(K, mu)
