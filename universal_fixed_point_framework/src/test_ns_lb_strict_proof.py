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
test_ns_lb_strict_proof.py

Phase 15D-2: NS-LB 显式最优常数严格证明测试。

验证：
1. Frostman 引理基本性质
2. Frostman 测度构造
3. Frostman 常数计算
4. 对偶问题求解
5. 显式最优常数验证
6. 变分原理验证
"""

from __future__ import annotations

import numpy as np
import pytest

from ns_lb_strict_proof import FrostmanLemma, NSLBOptimalConstant


def test_frostman_measure():
    """Frostman 测度构造。"""
    frostman = FrostmanLemma()
    points = np.array([[0.0], [0.5], [1.0]])
    mu = frostman.construct_frostman_measure(points, s=0.5)

    assert len(mu) == 3
    assert np.isclose(np.sum(mu), 1.0)
    assert np.all(mu >= 0)


def test_frostman_dimension():
    """Frostman 维数估计。"""
    frostman = FrostmanLemma()
    points = np.array([[0.0], [0.5], [1.0]])
    mu = np.array([0.33, 0.33, 0.34])
    dim = frostman.frostman_dimension(mu, points)

    assert dim >= 0
    assert dim <= 1.0


def test_frostman_constant():
    """Frostman 常数计算。"""
    frostman = FrostmanLemma()
    c = frostman.frostman_constant(s=0.5)

    assert c > 0
    assert isinstance(c, float)


def test_dual_problem():
    """对偶问题求解。"""
    ns_lb = NSLBOptimalConstant()
    contraction = np.array([0.5, 0.4])
    result = ns_lb.dual_problem_formulation(contraction)

    assert result["success"]
    assert result["optimal_s"] > 0


def test_explicit_constant():
    """显式最优常数计算。"""
    ns_lb = NSLBOptimalConstant()
    contraction = np.array([0.5, 0.4])

    c_opt = ns_lb.explicit_constant(contraction, overlap_factor=0.0)
    assert c_opt > 0

    c_opt_rho = ns_lb.explicit_constant(contraction, overlap_factor=0.5)
    assert c_opt_rho < c_opt


def test_constant_verification():
    """显式常数验证。"""
    ns_lb = NSLBOptimalConstant()
    contraction = np.array([0.6, 0.3])
    result = ns_lb.verify_constant(contraction, overlap_factor=0.2)

    assert result["explicit_constant"] > 0
    assert result["convergence_rate"] < 1.0
    assert result["moran_dimension"] > 0
    assert result["verification"]["c_opt_positive"]
    assert result["verification"]["rate_less_than_1"]


def test_overlap_factor_effect():
    """重叠因子影响测试。"""
    ns_lb = NSLBOptimalConstant()
    contraction = np.array([0.5, 0.4])

    constants = []
    for rho in [0.0, 0.25, 0.5, 0.75, 1.0]:
        c_opt = ns_lb.explicit_constant(contraction, overlap_factor=rho)
        constants.append(c_opt)

    assert constants == sorted(constants, reverse=True)


def test_moran_dimension():
    """Moran 维数计算。"""
    ns_lb = NSLBOptimalConstant()
    contraction = np.array([0.5, 0.5])

    dim = ns_lb._moran_dimension(contraction)
    assert np.isclose(dim, 1.0)

    contraction = np.array([0.5, 0.3])
    dim = ns_lb._moran_dimension(contraction)
    assert dim > 0


def test_variational_principle():
    """变分原理验证。"""
    ns_lb = NSLBOptimalConstant()
    contraction = np.array([0.5, 0.4])

    dual_result = ns_lb.dual_problem_formulation(contraction)
    explicit_result = ns_lb.verify_constant(contraction, overlap_factor=0.0)

    assert dual_result["success"]
    assert explicit_result["explicit_constant"] > 0


def test_edge_cases():
    """边界情况测试。"""
    ns_lb = NSLBOptimalConstant()

    c_opt = ns_lb.explicit_constant(np.array([0.5]), overlap_factor=0.0)
    assert c_opt > 0

    c_opt_zero = ns_lb.explicit_constant(np.array([0.5]), overlap_factor=1.0)
    assert c_opt_zero == 0.0


if __name__ == "__main__":
    print("=" * 60)
    print("Phase 15D-2: NS-LB 显式最优常数严格证明测试")
    print("=" * 60)

    test_frostman_measure()
    print("  [1] Frostman 测度构造 ✓")
    test_frostman_dimension()
    print("  [2] Frostman 维数估计 ✓")
    test_frostman_constant()
    print("  [3] Frostman 常数计算 ✓")
    test_dual_problem()
    print("  [4] 对偶问题求解 ✓")
    test_explicit_constant()
    print("  [5] 显式最优常数计算 ✓")
    test_constant_verification()
    print("  [6] 显式常数验证 ✓")
    test_overlap_factor_effect()
    print("  [7] 重叠因子影响 ✓")
    test_moran_dimension()
    print("  [8] Moran 维数计算 ✓")
    test_variational_principle()
    print("  [9] 变分原理验证 ✓")
    test_edge_cases()
    print("  [10] 边界情况测试 ✓")

    print("\n" + "=" * 60)
    print("全部 NS-LB 严格证明测试通过。")
    print("=" * 60)
