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
example_fixed_point.py

不动点求解器测试用例：
1. 通用不动点：求解 x = cos(x)
2. Hutchinson 不变测度：μ = K μ
3. 谱算子不动点：A = -log(K)
"""

import numpy as np
from fixed_point_solver import (
    FixedPointSolver,
    solve_fixed_point,
    measure_distance,
)
from spec_category import PositiveSpectralObject


def test_scalar_cosine():
    """测试通用不动点迭代：x = cos(x)。"""
    print("\n[测试 1] 标量不动点 x = cos(x)")
    result = solve_fixed_point(
        F=lambda x: np.cos(x),
        x0=np.array([0.5]),
        tol=1e-12,
        max_iter=100,
    )
    print(f"  不动点: {result.fixed_point[0]:.10f}")
    print(f"  收敛: {result.converged}, 迭代次数: {result.iterations}")
    assert result.converged, "标量不动点未收敛"
    assert abs(result.fixed_point[0] - np.cos(result.fixed_point[0])) < 1e-10


def test_hutchinson_measure():
    """测试 Hutchinson 不变测度：μ = K μ。"""
    print("\n[测试 2] Hutchinson 不变测度 μ = K μ")
    # 构造一个列随机矩阵，使不动点测度集中在第一个状态
    K = np.array([
        [1.0, 0.9, 0.8],
        [0.0, 0.1, 0.1],
        [0.0, 0.0, 0.1],
    ])
    K = K / K.sum(axis=0, keepdims=True)  # 列归一化

    result = FixedPointSolver.solve_hutchinson_measure(
        K=K,
        mu0=np.ones(3) / 3,
        tol=1e-12,
        max_iter=1000,
    )
    mu = result.fixed_point
    print(f"  不动点测度 μ: {mu}")
    print(f"  收敛: {result.converged}, 迭代次数: {result.iterations}")
    print(f"  验证 K @ μ ≈ μ 误差: {np.linalg.norm(K @ mu - mu):.2e}")
    assert result.converged, "Hutchinson 测度未收敛"
    assert np.allclose(K @ mu, mu, atol=1e-10)
    assert mu[0] > 0.9, "不动点测度未集中在主吸引子"


def test_spectral_operator():
    """测试谱算子不动点：A = -log(K)。"""
    print("\n[测试 3] 谱算子不动点 A = -log(K)")
    K = np.diag([1.0, 0.8, 0.64])
    result = FixedPointSolver.solve_spectral_operator(
        K=K,
        tol=1e-10,
        max_iter=100,
    )
    E = result.fixed_point
    print(f"  谱算子 A:\n{E.operator_A}")
    print(f"  谱 σ(A): {E.spectrum}")
    print(f"  收敛: {result.converged}, 迭代次数: {result.iterations}")
    assert result.converged, "谱算子不动点未收敛"
    expected_spectrum = np.array([0.0, -np.log(0.8), -np.log(0.64)])
    assert np.allclose(np.sort(E.spectrum), np.sort(expected_spectrum), atol=1e-10)


def main():
    print("=" * 60)
    print("不动点求解器测试")
    print("=" * 60)

    test_scalar_cosine()
    test_hutchinson_measure()
    test_spectral_operator()

    print("\n" + "=" * 60)
    print("所有测试通过。")
    print("=" * 60)


if __name__ == "__main__":
    main()
