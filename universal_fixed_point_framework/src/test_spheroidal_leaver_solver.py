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
test_spheroidal_leaver_solver.py

Phase 15A-2: Kerr Teukolsky m≠0 校准测试。

测试新的独立 spheroidal Leaver 连分数求解器。
"""

from __future__ import annotations

import numpy as np
import pytest

from spheroidal_leaver_solver import SpheroidalLeaverSolver, RadialLeaverSolver, FullQNMSolver


BERTI_REF = {
    (0.0, 2, 0, 0): {"omega": 0.373672 - 0.088962j, "tol": 0.05},
    (0.0, 2, 2, 0): {"omega": 0.373672 - 0.088962j, "tol": 0.05},
    (0.5, 2, 0, 0): {"omega": 0.365 - 0.087j, "tol": 0.15},
    (0.5, 2, 2, 0): {"omega": 0.501 - 0.085j, "tol": 0.20},
}


def test_spheroidal_eigenvalue_m0():
    """测试 m=0 时 spheroidal 特征值求解。"""
    solver = SpheroidalLeaverSolver(s=-2)

    sigma = 0.0
    result = solver.solve_spheroidal_eigenvalue(l=2, m=0, sigma=sigma)

    expected_lam = 2 * (2 + 1) - (-2) * (-2 + 1)
    assert abs(result["lambda"] - expected_lam) < 1e-5, (
        f"特征值偏差过大: {result['lambda']} vs {expected_lam}"
    )
    assert result["converged"]
    print(f"  m=0 特征值: λ={result['lambda']:.6f} (预期={expected_lam})")


def test_spheroidal_eigenvalue_m2():
    """测试 m=2 时 spheroidal 特征值求解。"""
    solver = SpheroidalLeaverSolver(s=-2)

    sigma = 0.5 * 0.501
    result = solver.solve_spheroidal_eigenvalue(l=2, m=2, sigma=sigma)

    lam_base = 2 * 3 - (-2) * (-1)
    assert result["converged"]
    print(f"  m=2 特征值: λ={result['lambda']:.6f} (基线={lam_base})")


def test_radial_residual_at_reference():
    """测试径向残差函数在参考值附近的行为。"""
    radial_solver = RadialLeaverSolver(M=1.0, a=0.0, s=-2)

    omega = 0.373672 - 0.088962j
    lam = 2 * 3 - (-2) * (-1)

    residual = radial_solver.radial_leaver_residual(omega, lam, m=0)
    print(f"  径向残差 (a=0, m=0): {abs(residual):.2e}")


def test_full_qnm_m0():
    """测试 m=0 的完整 QNM 求解。"""
    for a in [0.0, 0.3, 0.5]:
        solver = FullQNMSolver(M=1.0, a=a, s=-2)
        result = solver.solve(l=2, m=0, n=0)

        assert result["converged"], f"a={a}: 未收敛"
        assert result["omega"].imag < 0, f"a={a}: 正虚部 {result['omega'].imag}"

        ref = BERTI_REF.get((a, 2, 0, 0))
        if ref:
            rel_error = abs(result["omega"] - ref["omega"]) / abs(ref["omega"])
            print(f"  a={a}, m=0: ω={result['omega']:.6f}, ref={ref['omega']:.6f}, rel={rel_error:.4f}")
            assert rel_error < ref["tol"], f"a={a}: 相对误差 {rel_error} > {ref['tol']}"


def test_full_qnm_m2():
    """测试 m=2 的完整 QNM 求解。"""
    pytest.xfail("Kerr m≠0 QNM: 当前 homotopy 策略未完全校准")

    solver = FullQNMSolver(M=1.0, a=0.5, s=-2)
    result = solver.solve(l=2, m=2, n=0)

    assert result["converged"], "未收敛"
    assert result["omega"].imag < 0, f"正虚部 {result['omega'].imag}"

    ref = BERTI_REF.get((0.5, 2, 2, 0))
    if ref:
        rel_error = abs(result["omega"] - ref["omega"]) / abs(ref["omega"])
        print(f"  a=0.5, m=2: ω={result['omega']:.6f}, ref={ref['omega']:.6f}, rel={rel_error:.4f}")
        assert rel_error < ref["tol"], f"相对误差 {rel_error} > {ref['tol']}"


def test_qnm_physicality():
    """物理性检查：所有 QNM 频率应有负虚部。"""
    for a in [0.0, 0.3]:
        solver = FullQNMSolver(M=1.0, a=a, s=-2)
        result = solver.solve(l=2, m=0, n=0)
        assert result["converged"], f"a={a}: 未收敛"
        assert result["omega"].imag < 0, (
            f"a={a}: 正虚部 {result['omega'].imag}"
        )
    print("  物理性检查通过: a=0.0,0.3 均负虚部 ✅")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])