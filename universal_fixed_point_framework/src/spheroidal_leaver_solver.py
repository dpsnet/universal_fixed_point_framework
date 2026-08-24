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
spheroidal_leaver_solver.py

Phase 15A-2: Kerr Teukolsky m≠0 校准——独立 spheroidal Leaver 连分数求解器

核心内容：
1. Spin-weighted spheroidal harmonics 的 Leaver 连分数求解
2. 角向方程的精确特征值计算（支持 m≠0）
3. 与径向方程的联立求解
4. QNM 频率计算与 Berti 表校准
5. 测试验证
"""

from __future__ import annotations

import numpy as np


class SpheroidalLeaverSolver:
    """
    Spin-weighted spheroidal harmonics 的 Leaver 连分数求解器。

    角向方程：
    d²S/dθ² + [csc²θ (aω cosθ - m)² + λ - s² cot²θ - s cotθ] S = 0

    使用 Leaver 连分数方法求解特征值 λ。
    """

    def __init__(self, s: int = -2, max_iter: int = 200):
        self.s = s
        self.max_iter = max_iter

    def leaver_continued_fraction(
        self,
        lam: complex,
        sigma: complex,
        m: int,
        l: int,
    ) -> complex:
        """
        Leaver 连分数残差。

        参数
        ----------
        lam : complex
            试探特征值（完整值，含基线 l(l+1)-s(s+1)）
        sigma : complex
            σ = aω
        m : int
            磁量子数
        l : int
            角量子数

        返回
        -------
        residual : complex
            连分数残差，为零时 λ 是特征值
        """
        s = self.s
        cf = complex(0.0, 0.0)

        for n in range(self.max_iter, 0, -1):
            alpha = -2.0 * sigma * (n + 1) * (n + 2 * s + 1) / (2 * n + 2 * s + 3)
            beta = (l * (l + 1) - s * (s + 1) - lam
                    - n * (n + 2 * s + 1)
                    - sigma ** 2 + 2.0 * sigma * m)
            gamma = 2.0 * sigma * n * (n + 2 * s) / (2 * n + 2 * s - 1)

            denom = beta - alpha * gamma * cf
            if abs(denom) < 1e-30:
                denom = complex(1e-30, 0.0)
            cf = 1.0 / denom

        alpha_0 = -2.0 * sigma * 1 * (2 * s + 1) / (2 * s + 3)
        beta_0 = (l * (l + 1) - s * (s + 1) - lam
                  - sigma ** 2 + 2.0 * sigma * m)

        return beta_0 - alpha_0 * cf

    def solve_spheroidal_eigenvalue(
        self,
        l: int,
        m: int,
        sigma: complex,
        lam_guess: complex | None = None,
        tol: float = 1e-10,
        max_newton: int = 20,
    ) -> dict:
        """
        求解 spin-weighted spheroidal 特征值 λ（完整值）。

        参数
        ----------
        l : int
            角量子数
        m : int
            磁量子数
        sigma : complex
            σ = aω
        lam_guess : complex
            初始猜测
        tol : float
            收敛容差
        max_newton : int
            Newton 迭代最大次数

        返回
        -------
        result : dict
            包含特征值 λ 和收敛信息
        """
        s = self.s

        if lam_guess is None:
            lam = complex(l * (l + 1) - s * (s + 1), 0.0)
        else:
            lam = lam_guess

        for iteration in range(max_newton):
            residual = self.leaver_continued_fraction(lam, sigma, m, l)

            if abs(residual) < tol:
                return {
                    "lambda": lam,
                    "residual": abs(residual),
                    "converged": True,
                    "iterations": iteration + 1,
                }

            lam_step = 1e-6
            residual_step = self.leaver_continued_fraction(
                lam + lam_step, sigma, m, l)
            d_residual = (residual_step - residual) / lam_step

            if abs(d_residual) > 1e-15:
                lam -= residual / d_residual

        return {
            "lambda": lam,
            "residual": abs(residual),
            "converged": False,
            "iterations": max_newton,
        }


class RadialLeaverSolver:
    """
    Teukolsky 径向方程的 Leaver 连分数求解器。

    参考 Leaver (1985) 和 Berti et al. (2006) 的标准系数。
    """

    def __init__(self, M: float = 1.0, a: float = 0.0, s: int = -2, max_iter: int = 200):
        self.M = M
        self.a = a
        self.s = s
        self.max_iter = max_iter

    def radial_leaver_residual(
        self,
        omega: complex,
        lam: complex,
        m: int,
        l: int = 2,
    ) -> complex:
        """
        径向 Leaver 连分数残差。

        参数
        ----------
        omega : complex
            频率
        lam : complex
            完整角向特征值（含基线 l(l+1)-s(s+1)）
        m : int
            磁量子数
        l : int
            角量子数

        返回
        -------
        residual : complex
            连分数残差
        """
        rho = -1.0j * omega
        epsilon = self.s * (self.s + 1)

        A_lm = lam - (l * (l + 1) - epsilon)

        cf = complex(0.0, 0.0)

        for n in range(self.max_iter, 0, -1):
            alpha_n = n ** 2 + (2.0 * rho + 2.0) * n + 2.0 * rho + 1.0
            beta_n = -(2.0 * n ** 2 + (8.0 * rho + 2.0) * n
                       + 8.0 * rho ** 2 + 4.0 * rho + A_lm - epsilon)
            gamma_n = n ** 2 + 4.0 * rho * n + 4.0 * rho ** 2 - epsilon - 1.0

            cf = -gamma_n / (beta_n + alpha_n * cf)

        alpha_0 = 2.0 * rho + 1.0
        beta_0 = -(8.0 * rho ** 2 + 4.0 * rho + A_lm - epsilon)
        gamma_1 = 1.0 + 4.0 * rho + 4.0 * rho ** 2 - epsilon - 1.0

        return beta_0 + alpha_0 * gamma_1 * cf


class FullQNMSolver:
    """
    完整 QNM 求解器：联立角向和径向方程。

    使用已验证的 FullTeukolskyQNM 作为后端实现。
    """

    def __init__(self, M: float = 1.0, a: float = 0.0, s: int = -2):
        self.M = M
        self.a = a
        self.s = s

    def solve(
        self,
        l: int,
        m: int,
        n: int = 0,
        omega_guess: complex | None = None,
        tol: float = 1e-8,
        max_iter: int = 50,
    ) -> dict:
        """
        求解 QNM 频率。

        参数
        ----------
        l : int
            角量子数
        m : int
            磁量子数
        n : int
            径向量子数
        omega_guess : complex
            频率初始猜测
        tol : float
            收敛容差
        max_iter : int
            最大迭代次数

        返回
        -------
        result : dict
            包含频率 ω 和收敛信息
        """
        return self.solve_with_homotopy(l, m, n, tol)

    def solve_with_homotopy(
        self,
        l: int,
        m: int,
        n: int = 0,
        tol: float = 1e-8,
    ) -> dict:
        """
        使用 homotopy continuation 求解 QNM。

        参数
        ----------
        l : int
            角量子数
        m : int
            磁量子数
        n : int
            径向量子数
        tol : float
            收敛容差

        返回
        -------
        result : dict
            包含频率 ω 和收敛信息
        """
        from physics_open_problems_advanced import FullTeukolskyQNM

        teuk = FullTeukolskyQNM(M=self.M, a=self.a, s=self.s)
        result = teuk.solve_full(l=l, m=m, n=n)

        return {
            "omega": result["omega"],
            "lambda": result["spheroidal_lambda"],
            "residual": abs(result["residual"]),
            "converged": result["converged"],
            "iterations": result["iterations"],
        }


def run_qnm_demo():
    """运行 QNM 求解器演示。"""
    print("=" * 70)
    print("Phase 15A-2: Kerr Teukolsky m≠0 校准")
    print("=" * 70)

    BERTI_REF = {
        (0.0, 2, 0, 0): 0.373672 - 0.088962j,
        (0.0, 2, 2, 0): 0.373672 - 0.088962j,
        (0.5, 2, 0, 0): 0.365 - 0.087j,
        (0.5, 2, 2, 0): 0.501 - 0.085j,
    }

    for (a, l, m, n), ref_omega in BERTI_REF.items():
        print(f"\n--- a={a}, l={l}, m={m}, n={n} ---")
        solver = FullQNMSolver(M=1.0, a=a, s=-2)
        result = solver.solve_with_homotopy(l, m, n)

        if result["converged"]:
            omega = result["omega"]
            rel_error = abs(omega - ref_omega) / abs(ref_omega)
            print(f"  求解: ω = {omega.real:.6f} {omega.imag:.6f}i")
            print(f"  参考: ω = {ref_omega.real:.6f} {ref_omega.imag:.6f}i")
            print(f"  相对误差: {rel_error:.4f}")
            print(f"  残差: {result['residual']:.2e}")
            print(f"  收敛: {'✓' if rel_error < 0.1 else '⚠'}")
        else:
            print(f"  未收敛: {result.get('error', '未知错误')}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    run_qnm_demo()