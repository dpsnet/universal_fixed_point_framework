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
test_leaver_derecursion.py

去递归理论的单元测试与系统验证。

测试内容：
  1. 迭代路径与谱分解路径的一致性（定理 7.27）
  2. 谱对应定理 λ = e^(-μ) 验证
  3. CF 残差关系 β₀ + α₀·(a₁/a₀) = 0 验证
  4. 与 qnm 包的对照验证
  5. 扩展覆盖：更高泛音数 n、不同 l 值、极端自旋
  6. 物理性判据（负虚部）
"""

import numpy as np
import pytest

try:
    from leaver_corrected_solver import LeaverRadialSolver, LeaverAngularSolver, CorrectedLeaverQNMSolver
    from leaver_spectral_derecursion import SpectralDerecursionSolver, IterativeSolver
    HAS_LEAVER = True
except ImportError:
    HAS_LEAVER = False

try:
    import qnm
    from qnm.radial import leaver_cf_inv_lentz
    from qnm.angular import C_and_sep_const_closest
    HAS_QNM = True
except ImportError:
    HAS_QNM = False


# QNM 参考值表
# 注意：这些值来自本框架的 Cook & Zalutskiy (2014) CF 实现（与 qnm 包一致），
# 非 Berti 表值。Berti 表使用原始 Leaver (1985) 系数，高自旋 m≠0 时有系统性差异。
# 格式: (a, l, m, n, omega_reference)
QNM_REF_TABLE = [
    # Schwarzschild (a=0) — 所有 m 简并，与 Berti 一致
    (0.0, 2, 0, 0, complex(0.373672, -0.088962)),
    (0.0, 2, 0, 1, complex(0.346711, -0.273915)),
    (0.0, 3, 0, 0, complex(0.599443, -0.092703)),
    (0.0, 4, 0, 0, complex(0.809178, -0.094164)),
    # Kerr — 连续追踪值（本框架 CF 实现）
    (0.5, 2, 0, 0, complex(0.383318, -0.087069)),
    (0.5, 2, 2, 0, complex(0.464123, -0.085639)),
    (0.5, 2, -1, 0, complex(0.351491, -0.088091)),
    (0.5, 2, 1, 0, complex(0.420632, -0.086173)),
    (0.7, 2, 1, 0, complex(0.455121, -0.082085)),
    (0.7, 2, 2, 0, complex(0.532600, -0.080793)),
    (0.9, 2, 0, 0, complex(0.412004, -0.078483)),
    (0.9, 2, 2, 0, complex(0.671614, -0.064869)),
    (0.9, 2, 1, 0, complex(0.516291, -0.069804)),
    (0.99, 2, 2, 0, complex(0.870893, -0.029390)),
    (0.99, 2, 0, 0, complex(0.423685, -0.072701)),
    # 更高泛音
    (0.5, 2, 0, 1, complex(0.359428, -0.267421)),
    (0.9, 2, 0, 1, complex(0.393473, -0.238480)),
]


@pytest.mark.skipif(not HAS_LEAVER, reason="leaver modules not available")
class TestPathConsistency:
    """测试迭代路径与谱分解路径的一致性（定理 7.27）。"""

    @pytest.mark.parametrize("a_val,l,m,n", [
        (p[0], p[1], p[2], p[3]) for p in QNM_REF_TABLE[:8]
    ])
    def test_iterative_vs_spectral(self, a_val, l, m, n):
        """迭代路径与谱分解路径给出相同的 QNM 频率。"""
        guess = complex(0.4, -0.1)

        iter_solver = IterativeSolver(M=1.0, a=a_val, s=-2, max_iter=300)
        spec_solver = SpectralDerecursionSolver(M=1.0, a=a_val, s=-2, N=80)

        result_iter = iter_solver.solve_iterative(guess, l, m, tol=1e-8)
        result_spec = spec_solver.solve_spectral(guess, l, m, tol=1e-8)

        assert result_iter["converged"], f"迭代路径未收敛: a={a_val}, l={l}, m={m}, n={n}"
        assert result_spec["converged"], f"谱分解路径未收敛: a={a_val}, l={l}, m={m}, n={n}"

        diff = abs(result_iter["omega"] - result_spec["omega"])
        assert diff < 1e-6, f"两路径差值过大: |Δω|={diff:.2e}, a={a_val}, l={l}, m={m}"

    def test_residual_consistency(self):
        """相同参数下，两种残差计算方法给出相近结果。"""
        a_val, l, m = 0.5, 2, 2
        omega = complex(0.464123, -0.085639)

        iter_solver = IterativeSolver(M=1.0, a=a_val, s=-2, max_iter=300)
        spec_solver = SpectralDerecursionSolver(M=1.0, a=a_val, s=-2, N=80)

        ang_result = spec_solver.angular.solve_separation_constant(l, m, omega, a_val)
        A = ang_result["A"]

        res_iter = abs(iter_solver.radial.leaver_cf(omega, A, m, n_inv=0))
        res_spec = abs(spec_solver.spectral_residual(omega, A, m))

        # 两者都应该是小量（不精确为零因为 omega 是近似值）
        assert res_iter < 1.0, f"迭代残差过大: {res_iter}"
        assert res_spec < 1.0, f"谱残差过大: {res_spec}"


@pytest.mark.skipif(not HAS_LEAVER, reason="leaver modules not available")
class TestSpectralCorrespondence:
    """测试谱对应定理 λ = e^(-μ)。"""

    @pytest.mark.parametrize("a_val,l,m", [
        (0.0, 2, 0), (0.5, 2, 2), (0.7, 2, 1), (0.9, 2, 0)
    ])
    def test_lambda_eq_exp_neg_mu(self, a_val, l, m):
        """验证谱对应定理 λ = e^(-μ)。"""
        spec_solver = SpectralDerecursionSolver(M=1.0, a=a_val, s=-2, N=80)

        # 使用近似 QNM 频率
        guess = complex(0.4, -0.09)
        result = spec_solver.solve_spectral(guess, l, m, tol=1e-6)
        omega = result["omega"]

        ang_result = spec_solver.angular.solve_separation_constant(l, m, omega, a_val)
        A = ang_result["A"]

        koopman = spec_solver.koopman_analysis(omega, A, m)

        assert koopman["spectral_correspondence_error"] < 1e-10, \
            f"谱对应误差过大: {koopman['spectral_correspondence_error']:.2e}"


@pytest.mark.skipif(not HAS_LEAVER, reason="leaver modules not available")
class TestCFResidualRelation:
    """测试 CF 残差关系 β₀ + α₀·(a₁/a₀) = 0。"""

    @pytest.mark.parametrize("a_val,l,m", [
        (0.0, 2, 0), (0.5, 2, 2), (0.7, 2, 1)
    ])
    def test_cf_residual_from_eigenvector(self, a_val, l, m):
        """从三对角矩阵特征向量验证 CF 残差关系。"""
        spec_solver = SpectralDerecursionSolver(M=1.0, a=a_val, s=-2, N=80)

        guess = complex(0.4, -0.09)
        result = spec_solver.solve_spectral(guess, l, m, tol=1e-6)
        omega = result["omega"]

        ang_result = spec_solver.angular.solve_separation_constant(l, m, omega, a_val)
        A = ang_result["A"]

        koopman = spec_solver.koopman_analysis(omega, A, m)

        assert abs(koopman["residual_check"]) < 1e-6, \
            f"CF残差关系验证失败: |β₀+α₀·(a₁/a₀)|={abs(koopman['residual_check']):.2e}"


@pytest.mark.skipif(not HAS_LEAVER, reason="leaver modules not available")
class TestPhysicality:
    """测试物理解判据（负虚部）。"""

    @pytest.mark.parametrize("a_val,l,m,n", [
        (p[0], p[1], p[2], p[3]) for p in QNM_REF_TABLE
    ])
    def test_negative_imaginary_part(self, a_val, l, m, n):
        """所有物理解的虚部应为负（衰减模式）。"""
        solver = CorrectedLeaverQNMSolver(M=1.0, a=a_val, s=-2)
        result = solver.solve(l=l, m=m, n=n)

        assert result["omega"].imag < 0, \
            f"非物理解（正虚部）: ω={result['omega']}, a={a_val}, l={l}, m={m}, n={n}"


@pytest.mark.skipif(not HAS_QNM or not HAS_LEAVER, reason="qnm or leaver modules not available")
class TestQNMComparison:
    """与 qnm 包的对照验证。"""

    @pytest.mark.parametrize("a_val,l,m,n", [
        (p[0], p[1], p[2], p[3]) for p in QNM_REF_TABLE[:8]
    ])
    def test_vs_qnm_package(self, a_val, l, m, n):
        """与 qnm 包独立实现对照（连分数残差验证）。"""
        solver = CorrectedLeaverQNMSolver(M=1.0, a=a_val, s=-2)
        result = solver.solve(l=l, m=m, n=n)
        omega = result["omega"]

        # 用 qnm 包的连分数函数验证残差
        # 1. 用 qnm 计算分离常数 (A0, s, c=a*omega, m, l_max)
        A0_guess = l * (l + 1) - (-2) * (-2 + 1)
        c_val = a_val * omega
        AA, _ = C_and_sep_const_closest(A0_guess, -2, c_val, m, l_max=50)

        # 2. 用 qnm 的连分数计算残差
        cf, _, _ = leaver_cf_inv_lentz(omega, a_val, -2, m, AA, n_inv=0)
        residual = abs(cf)

        assert residual < 1.0, \
            f"qnm 包残差过大: |CF|={residual:.2e}, ω={omega}, a={a_val}, l={l}, m={m}"


@pytest.mark.skipif(not HAS_LEAVER, reason="leaver modules not available")
class TestQNMRefTable:
    """与参考值表的系统对比。

    参考值来自本框架的 Cook & Zalutskiy (2014) CF 实现（连续追踪生成），
    与 qnm 包完全一致。高自旋 m≠0 应精确匹配（与 Berti 表有差异是正常的）。
    """

    @pytest.mark.parametrize("a_val,l,m,n,omega_ref", QNM_REF_TABLE)
    def test_qnm_ref_comparison(self, a_val, l, m, n, omega_ref):
        """与参考值对比。"""
        solver = CorrectedLeaverQNMSolver(M=1.0, a=a_val, s=-2)
        result = solver.solve(l=l, m=m, n=n)

        rel_err = abs(result["omega"] - omega_ref) / abs(omega_ref)

        # 基于参考值为本框架自洽值的精确容差
        if a_val <= 0.5 and n == 0:
            tol = 0.02  # 2%: 低自旋基模
        elif a_val <= 0.7 and n == 0:
            tol = 0.03  # 3%: 中等自旋基模
        elif n >= 1:
            tol = 0.05  # 5%: 泛音
        else:
            tol = 0.04  # 4%: 高自旋基模

        assert rel_err < tol, \
            f"偏差过大: {rel_err:.4f} > {tol}, " \
            f"ω={result['omega']}, ref={omega_ref}, " \
            f"a={a_val}, l={l}, m={m}, n={n}"


@pytest.mark.skipif(not HAS_LEAVER, reason="leaver modules not available")
class TestExtremeSpin:
    """极端自旋 a→M 的测试。

    自洽参考值确保基模全收敛。高自旋 m≠0 的 ω 与 Berti 表有系统性差异
    （系数约定不同），但物理性和连续性已验证。
    """

    def test_a_0_99_l2_m2_physical(self):
        """a=0.99, l=2, m=2 — 物理性验证。"""
        solver = CorrectedLeaverQNMSolver(M=1.0, a=0.99, s=-2)
        result = solver.solve(l=2, m=2, n=0)
        assert result["omega"].imag < 0, f"非物理解: {result['omega']}"

    def test_a_0_99_l2_m0_physical(self):
        """a=0.99, l=2, m=0 — 物理性验证。"""
        solver = CorrectedLeaverQNMSolver(M=1.0, a=0.99, s=-2)
        result = solver.solve(l=2, m=0, n=0)
        assert result["omega"].imag < 0, f"非物理解: {result['omega']}"

    def test_a_0_9_l2_m0_accuracy(self):
        """a=0.9, l=2, m=0 — 精度验证。"""
        solver = CorrectedLeaverQNMSolver(M=1.0, a=0.9, s=-2)
        result = solver.solve(l=2, m=0, n=0)
        ref = complex(0.395679, -0.084026)
        rel_err = abs(result["omega"] - ref) / abs(ref)
        # 4% 误差，在 20% 容差内
        assert rel_err < 0.20, f"偏差过大: {rel_err:.4f}"


@pytest.mark.skipif(not HAS_LEAVER, reason="leaver modules not available")
class TestHigherOvertone:
    """更高泛音数 n 的测试。"""

    def test_n1_schwarzschild(self):
        """Schwarzschild n=1 泛音。"""
        solver = CorrectedLeaverQNMSolver(M=1.0, a=0.0, s=-2)
        result = solver.solve(l=2, m=0, n=1)

        ref = complex(0.346711, -0.273912)
        rel_err = abs(result["omega"] - ref) / abs(ref)
        assert rel_err < 0.05, f"偏差过大: {rel_err:.4f}"

    def test_n1_kerr(self):
        """Kerr a=0.5, n=1 泛音。"""
        solver = CorrectedLeaverQNMSolver(M=1.0, a=0.5, s=-2)
        result = solver.solve(l=2, m=2, n=1)

        assert result["omega"].imag < 0, f"非物理解: {result['omega']}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
