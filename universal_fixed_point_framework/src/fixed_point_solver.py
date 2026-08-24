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
fixed_point_solver.py

全域不动点方程 F[V] = V 的数值求解器。

提供：
1. 通用不动点迭代（Picard / Banach 迭代）
2. 针对 PositiveSpectralObject 的谱算子不动点求解
3. 针对概率测度向量的 Hutchinson 型不动点求解

所有迭代算法均作为「数值工具」出现，不侵入理论公理本体。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Any
import numpy as np
from spec_category import PositiveSpectralObject


@dataclass
class FixedPointResult:
    """不动点求解结果。"""
    fixed_point: Any
    converged: bool
    iterations: int
    residual_history: list[float] = field(default_factory=list)


def generic_fixed_point_iteration(
    F: Callable[[Any], Any],
    x0: Any,
    distance: Callable[[Any, Any], float],
    tol: float = 1e-10,
    max_iter: int = 1000,
    verbose: bool = False,
) -> FixedPointResult:
    """
    通用不动点迭代：x_{k+1} = F(x_k)。

    参数
    ----------
    F : Callable[[Any], Any]
        不动点映射。
    x0 : Any
        初始猜测。
    distance : Callable[[Any, Any], float]
        两点之间的距离函数。
    tol : float
        收敛容差。
    max_iter : int
        最大迭代次数。
    verbose : bool
        是否打印迭代信息。

    返回
    -------
    FixedPointResult
    """
    x = x0
    residuals = []
    for k in range(max_iter):
        x_next = F(x)
        res = distance(x_next, x)
        residuals.append(res)
        if verbose and k % 100 == 0:
            print(f"  iter {k}: residual = {res:.6e}")
        if res < tol:
            return FixedPointResult(
                fixed_point=x_next,
                converged=True,
                iterations=k + 1,
                residual_history=residuals,
            )
        x = x_next
    return FixedPointResult(
        fixed_point=x,
        converged=False,
        iterations=max_iter,
        residual_history=residuals,
    )


def spectral_object_distance(E1: PositiveSpectralObject, E2: PositiveSpectralObject) -> float:
    """两个谱对象之间的距离：谱算子差的 Frobenius 范数。"""
    return np.linalg.norm(E1.operator_A - E2.operator_A, ord="fro")


def hutchinson_operator(K: np.ndarray, mu: np.ndarray) -> np.ndarray:
    """
    Hutchinson 型算子：μ -> K μ。

    参数
    ----------
    K : np.ndarray
        Frobenius-Perron 型转移矩阵（列随机），形状 (n, n)。
    mu : np.ndarray
        概率测度向量，形状 (n,)，非负且和为 1。

    返回
    -------
    np.ndarray
        新的测度向量，已归一化为概率分布。
    """
    mu_next = K @ mu
    s = mu_next.sum()
    if s > 0:
        mu_next = mu_next / s
    return mu_next


def measure_distance(mu1: np.ndarray, mu2: np.ndarray) -> float:
    """两个概率测度向量之间的全变差距离。"""
    return 0.5 * np.sum(np.abs(mu1 - mu2))


class FixedPointSolver:
    """
    全域不动点方程 F[V] = V 的求解器入口。

    提供针对常见子不动点方程的便捷方法：
    - solve_spectral_operator: 求解谱算子不动点
    - solve_hutchinson_measure: 求解 Hutchinson 不变测度
    - solve_generic: 通用不动点映射
    """

    @staticmethod
    def solve_generic(
        F: Callable[[Any], Any],
        x0: Any,
        distance: Callable[[Any, Any], float],
        tol: float = 1e-10,
        max_iter: int = 1000,
        verbose: bool = False,
    ) -> FixedPointResult:
        """通用不动点迭代入口。"""
        return generic_fixed_point_iteration(
            F=F,
            x0=x0,
            distance=distance,
            tol=tol,
            max_iter=max_iter,
            verbose=verbose,
        )

    @staticmethod
    def solve_spectral_operator(
        K: np.ndarray,
        A0: np.ndarray | None = None,
        tol: float = 1e-10,
        max_iter: int = 1000,
        verbose: bool = False,
    ) -> FixedPointResult:
        """
        求解谱算子不动点：A = -log(K)。

        在原型阶段，由于 K 是给定的压缩转移矩阵，不动点方程退化为
        直接计算 A = -log(K)。本函数用不动点迭代框架包装这一计算：
            A_{k+1} = -log(K)
        该迭代一步即收敛，同时保留与通用框架统一的接口。
        后续可替换为更复杂的自洽方程，如 A = -log(K(A))。
        """
        n = K.shape[0]
        if A0 is None:
            A0 = np.zeros((n, n))

        # 目标不动点：A_star = -log(K)
        A_star = PositiveSpectralObject.from_koopman(K).operator_A

        def F(A: np.ndarray) -> np.ndarray:
            # 恒等目标迭代：直接返回已知不动点
            # 在实际应用中，可替换为 A = -log(K(A)) 等自洽映射
            return A_star

        result = generic_fixed_point_iteration(
            F=F,
            x0=A0,
            distance=lambda A1, A2: np.linalg.norm(A1 - A2, ord="fro"),
            tol=tol,
            max_iter=max_iter,
            verbose=verbose,
        )
        # 将不动点包装为 PositiveSpectralObject
        result.fixed_point = PositiveSpectralObject(operator_A=result.fixed_point)
        return result

    @staticmethod
    def solve_hutchinson_measure(
        K: np.ndarray,
        mu0: np.ndarray | None = None,
        tol: float = 1e-10,
        max_iter: int = 1000,
        verbose: bool = False,
    ) -> FixedPointResult:
        """
        求解 Hutchinson 不变测度：μ = K μ。

        参数
        ----------
        K : np.ndarray
            列随机转移矩阵。
        mu0 : np.ndarray, optional
            初始概率测度。默认均匀分布。
        """
        n = K.shape[0]
        if mu0 is None:
            mu0 = np.ones(n) / n

        result = generic_fixed_point_iteration(
            F=lambda mu: hutchinson_operator(K, mu),
            x0=mu0,
            distance=measure_distance,
            tol=tol,
            max_iter=max_iter,
            verbose=verbose,
        )
        return result


# 便捷函数
def solve_fixed_point(
    F: Callable[[Any], Any],
    x0: Any,
    distance: Callable[[Any, Any], float] | None = None,
    tol: float = 1e-10,
    max_iter: int = 1000,
    verbose: bool = False,
) -> FixedPointResult:
    """
    最简接口：求解 x = F(x)。

    若未提供 distance，默认使用欧几里得范数（要求 x 可转换为 np.ndarray）。
    """
    if distance is None:
        distance = lambda a, b: float(np.linalg.norm(np.asarray(a) - np.asarray(b)))
    return FixedPointSolver.solve_generic(
        F=F, x0=x0, distance=distance, tol=tol, max_iter=max_iter, verbose=verbose
    )


def is_weak_spectral_match(
    A: np.ndarray,
    K: np.ndarray,
    tol: float = 1e-6,
) -> bool:
    """
    验证谱算子 A 与 Koopman 矩阵 K 在 weak 意义下相容。

    weak 相容性要求 exp(-A) 与 K 具有相同谱（作为多重集合），
    而不要求矩阵等式 exp(-A) = K 精确成立。这为 weak 交织模式
    下的不动点求解提供了可计算的判据。
    """
    if A.shape != K.shape:
        return False
    lam_A = np.linalg.eigvalsh(A)
    lam_K = np.linalg.eigvals(K)
    lam_from_A = np.sort(np.exp(-lam_A))
    lam_K = np.sort(np.real(lam_K))
    return np.allclose(lam_from_A, lam_K, atol=tol)
