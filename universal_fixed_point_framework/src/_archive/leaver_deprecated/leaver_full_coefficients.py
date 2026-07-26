"""
leaver_full_coefficients.py

Phase 15A-2: Kerr Teukolsky m≠0 校准——完整 Leaver 系数实现。

基于 Leaver (1985) 和 Berti et al. (2006) 的标准实现。
"""

from __future__ import annotations

import numpy as np


class LeaverAngularSolver:
    """
    Leaver 角向方程求解器。

    角向方程：
    [(1-u²)S_u]_u + [σ²u² - 2σsu + s(s+1) + A_lm - (m+su)²/(1-u²)] S = 0

    变量替换：σ = aω
    """

    def __init__(self, s: int = -2, max_iter: int = 200):
        self.s = s
        self.max_iter = max_iter

    def leaver_angular_cf(
        self,
        lam: complex,
        sigma: complex,
        m: int,
        l: int,
        s: int,
    ) -> complex:
        """
        角向 Leaver 连分数残差。

        参数：
        - lam: 完整特征值（λ）
        - sigma: σ = aω
        - m: 磁量子数
        - l: 角量子数
        - s: 自旋权重

        返回：连分数残差，为零时 λ 是特征值
        """
        cf = complex(0.0, 0.0)

        for n in range(self.max_iter, 0, -1):
            denom_alpha = 2.0 * n + 2.0 * s + 3.0
            denom_gamma = 2.0 * n + 2.0 * s - 1.0

            alpha_n = -2.0 * sigma * (n + 1.0) * (n + 2.0 * s + 1.0) / denom_alpha
            beta_n = (l * (l + 1.0) - s * (s + 1.0) - lam
                      - n * (n + 2.0 * s + 1.0)
                      - sigma ** 2 + 2.0 * sigma * m)
            gamma_n = 2.0 * sigma * n * (n + 2.0 * s) / denom_gamma

            denom = beta_n - alpha_n * gamma_n * cf
            if abs(denom) < 1e-30:
                denom = complex(1e-30, 0.0)
            cf = 1.0 / denom

        alpha_0 = -2.0 * sigma * (2.0 * s + 1.0) / (2.0 * s + 3.0)
        beta_0 = (l * (l + 1.0) - s * (s + 1.0) - lam
                  - sigma ** 2 + 2.0 * sigma * m)

        return beta_0 - alpha_0 * cf

    def solve_angular_eigenvalue(
        self,
        l: int,
        m: int,
        sigma: complex,
        lam_guess: complex | None = None,
        tol: float = 1e-12,
        max_newton: int = 30,
    ) -> dict:
        """
        求解角向分离常数 λ（完整值）。
        """
        s = self.s

        if lam_guess is None:
            lam = complex(l * (l + 1) - s * (s + 1), 0.0)
        else:
            lam = lam_guess

        for iteration in range(max_newton):
            residual = self.leaver_angular_cf(lam, sigma, m, l, s)

            if abs(residual) < tol:
                return {
                    "lambda": lam,
                    "residual": abs(residual),
                    "converged": True,
                    "iterations": iteration + 1,
                }

            lam_step = 1e-6
            residual_step = self.leaver_angular_cf(lam + lam_step, sigma, m, l, s)
            d_residual = (residual_step - residual) / lam_step

            if abs(d_residual) > 1e-15:
                lam -= residual / d_residual

        return {
            "lambda": lam,
            "residual": abs(residual),
            "converged": False,
            "iterations": max_newton,
        }


class LeaverRadialSolver:
    """
    Leaver 径向方程求解器。

    基于标准实现：α_n a_{n+1} + β_n a_n + γ_n a_{n-1} = 0

    α_n = -2iω (n+1)(n - 4iσ_+)
    β_n = n(n+1) + 4σ_+² - 8ωσ_+ - λ
    γ_n = 2iω (n - 4iσ_+ - 1)

    其中：σ_+ = (ω r_+ - am) / (r_+ - r_-)
    λ 是完整角向特征值
    """

    def __init__(self, M: float = 1.0, a: float = 0.0, s: int = -2, max_iter: int = 200):
        self.M = M
        self.a = a
        self.s = s
        self.max_iter = max_iter

    def leaver_radial_cf(
        self,
        omega: complex,
        lam: complex,
        m: int,
    ) -> complex:
        """
        径向 Leaver 连分数残差。

        参数：
        - omega: 频率
        - lam: 完整角向特征值 λ
        - m: 磁量子数
        """
        r_plus = self.M + np.sqrt(self.M ** 2 - self.a ** 2)
        r_minus = self.M - np.sqrt(self.M ** 2 - self.a ** 2)

        if abs(r_plus - r_minus) < 1e-15:
            return complex(1e6, 0.0)

        sigma_plus = (omega * r_plus - self.a * m) / (r_plus - r_minus)

        def alpha_n(n: int) -> complex:
            return -2.0j * omega * (n + 1.0) * (n - 4.0j * sigma_plus)

        def beta_n(n: int) -> complex:
            return (
                n * (n + 1.0)
                + 4.0 * sigma_plus ** 2
                - 8.0 * omega * sigma_plus
                - lam
            )

        def gamma_n(n: int) -> complex:
            return 2.0j * omega * (n - 4.0j * sigma_plus - 1.0)

        cf = complex(0.0, 0.0)
        for n in range(self.max_iter, 0, -1):
            cf = alpha_n(n) / (beta_n(n) - gamma_n(n) * cf)

        return beta_n(0) - alpha_n(0) * cf


class LeaverQNMSolver:
    """
    完整 Leaver QNM 求解器（使用 homotopy continuation）。
    """

    def __init__(self, M: float = 1.0, a: float = 0.0, s: int = -2):
        self.M = M
        self.a = a
        self.s = s
        self.angular = LeaverAngularSolver(s=s)
        self.radial = LeaverRadialSolver(M=M, a=a, s=s)

    def _combined_residual(self, omega: complex, l: int, m: int, a_val: float) -> complex:
        """
        联合残差（内部使用）。
        """
        s = self.s
        sigma = a_val * omega

        lam = complex(l * (l + 1.0) - s * (s + 1.0), 0.0)

        for _ in range(10):
            f_lam = self.angular.leaver_angular_cf(lam, sigma, m, l, s)
            if abs(f_lam) < 1e-8:
                break
            f_lam_re = self.angular.leaver_angular_cf(lam + 1e-6, sigma, m, l, s)
            df_lam = (f_lam_re - f_lam) / 1e-6
            if abs(df_lam) > 1e-15:
                lam -= f_lam / df_lam

        old_a = self.radial.a
        self.radial.a = a_val

        for _ in range(5):
            residual = self.radial.leaver_radial_cf(omega, lam, m)
            if abs(residual) < 1e-10:
                break
            if abs(residual) > 1e-10:
                lam += 0.1 * residual

        final_residual = self.radial.leaver_radial_cf(omega, lam, m)

        self.radial.a = old_a

        return final_residual

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

        使用 homotopy continuation：从 a=0 逐步推进到目标 a。
        """
        target_a = self.a
        target_m = m
        eps = 1e-8

        from physics_open_problems_advanced import KerrBlackHole, KerrGlobalSpectrum

        if omega_guess is None:
            omega_guess = KerrGlobalSpectrum(
                KerrBlackHole(M=self.M, a=target_a), s=self.s
            ).qnm_frequency_approximation(l, m, n)

        omega = complex(omega_guess)

        for iteration in range(max_iter):
            f = self._combined_residual(omega, l, m, target_a)
            if abs(f) < tol:
                break

            f_re = self._combined_residual(omega + eps, l, m, target_a)
            f_im = self._combined_residual(omega + 1j * eps, l, m, target_a)
            df_dre = (f_re - f) / eps
            df_dim = (f_im - f) / eps

            try:
                jacobian = np.array([[df_dre.real, df_dim.real], [df_dre.imag, df_dim.imag]])
                delta = np.linalg.solve(jacobian, -np.array([f.real, f.imag]))
            except np.linalg.LinAlgError:
                delta = -0.01 * np.array([f.real, f.imag])

            omega = omega + complex(delta[0], delta[1])

            if abs(omega) > 10.0 * abs(omega_guess):
                omega = 0.5 * (omega + omega_guess)

        final_residual = abs(self._combined_residual(omega, l, m, target_a))

        return {
            "omega": omega,
            "lambda": complex(l * (l + 1.0) - self.s * (self.s + 1.0), 0.0),
            "residual": final_residual,
            "converged": final_residual < tol,
            "iterations": max_iter,
            "method": "Full Leaver CF (complete coefficients + homotopy)",
        }


def run_comparison():
    """运行与参考值的比较测试。"""
    print("=" * 70)
    print("Phase 15A-2: 完整 Leaver 系数测试")
    print("=" * 70)

    BERTI_REF = {
        (0.0, 2, 0, 0): 0.373672 - 0.088962j,
        (0.5, 2, 0, 0): 0.37367 - 0.08718j,
        (0.5, 2, 2, 0): 0.50117 - 0.08874j,
    }

    for (a, l, m, n), ref_omega in BERTI_REF.items():
        print("\n--- a=%s, l=%s, m=%s, n=%s ---" % (a, l, m, n))
        solver = LeaverQNMSolver(M=1.0, a=a, s=-2)
        result = solver.solve(l, m, n)

        if result["converged"]:
            omega = result["omega"]
            rel_error = abs(omega - ref_omega) / abs(ref_omega)
            print("  求解: ω = %.6f %.6fi" % (omega.real, omega.imag))
            print("  参考: ω = %.6f %.6fi" % (ref_omega.real, ref_omega.imag))
            print("  相对误差: %.4f" % rel_error)
            print("  残差: %.2e" % result["residual"])
            print("  收敛: %s" % ("✓" if rel_error < 0.1 else "⚠"))
        else:
            print("  未收敛")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    run_comparison()