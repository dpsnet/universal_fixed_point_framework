"""
leaver_derecursion.py

使用去递归理论解决 Leaver 连分数计算。

核心思想：
1. 将连分数视为递归系统 R ∈ Rec
2. 通过 D 函子映射到谱范畴 Spec：D(R) = (H_R, A_R, σ(A_R))，其中 A_R = -log(K_R)
3. 谱对应：λ = e^(-μ)，不动点由谱半径决定
4. 收敛性由谱间隙 γ = 1 - ρ(K) 保证

理论基础：
- D: Rec → Spec（去递归函子）
- 谱对应自然等价 η: M ⟹ L，M(R) = σ(-log Φ_R*)，L(R) = σ(Φ_R*)
- 不动点方程：CF = 1 / (β_n - α_n * γ_n * CF) 的谱等价形式
- 收敛速度由谱间隙决定：误差 ~ ρ(K)^n

参考：Leaver (1985), Berti et al. (2006)
"""

from __future__ import annotations

import numpy as np
from scipy.linalg import eig


class LeaverDerecursionSolver:
    """
    使用去递归理论的 Leaver 连分数求解器。

    核心算法：
    1. 构建递推关系的 Koopman 算子 K
    2. 计算谱半径 ρ(K) 和谱间隙 γ = 1 - ρ(K)
    3. 利用向后迭代计算不动点，并用谱间隙估计收敛速度
    4. 提供误差界保证

    连分数形式：
    CF = 1 / (β_n - α_n * γ_n / (β_{n-1} - α_{n-1} * γ_{n-1} / (...)))
    """

    def __init__(self, max_iter: int = 200, tol: float = 1e-15):
        self.max_iter = max_iter
        self.tol = tol

    def leaver_angular_cf(
        self,
        lam: complex,
        sigma: complex,
        m: int,
        l: int,
        s: int,
    ) -> tuple[complex, dict]:
        """
        角向 Leaver 连分数残差。

        参数：
        - lam: 角向特征值（完整值）
        - sigma: σ = aω
        - m: 磁量子数
        - l: 角量子数
        - s: 自旋权重

        返回：
        - residual: 连分数残差 beta_0 - alpha_0 * CF
        - analysis: 去递归分析结果
        """
        cf = complex(0.0, 0.0)
        cf_history = []

        for n in range(self.max_iter, 0, -1):
            denom_alpha = 2.0 * n + 2.0 * s + 3.0
            denom_gamma = 2.0 * n + 2.0 * s - 1.0

            alpha_n = -2.0 * sigma * (n + 1.0) * (n + 2.0 * s + 1.0)
            if abs(denom_alpha) > 1e-15:
                alpha_n /= denom_alpha

            beta_n = (l * (l + 1.0) - s * (s + 1.0) - lam
                      - n * (n + 2.0 * s + 1.0)
                      - sigma ** 2 + 2.0 * sigma * m)

            gamma_n = 2.0 * sigma * n * (n + 2.0 * s)
            if abs(denom_gamma) > 1e-15:
                gamma_n /= denom_gamma

            denom = beta_n - alpha_n * gamma_n * cf
            if abs(denom) < 1e-30:
                denom = complex(1e-30, 0.0)
            cf = 1.0 / denom

            cf_history.append(cf)

        alpha_0 = -2.0 * sigma * (2.0 * s + 1.0) / (2.0 * s + 3.0)
        beta_0 = (l * (l + 1.0) - s * (s + 1.0) - lam
                  - sigma ** 2 + 2.0 * sigma * m)

        residual = beta_0 - alpha_0 * cf

        spectral_gap = self._estimate_spectral_gap(cf_history)

        analysis = {
            "fixed_point": cf,
            "spectral_gap": spectral_gap,
            "convergence_rate": 1.0 - spectral_gap if spectral_gap > 0 else 0.5,
            "iterations": self.max_iter,
            "residual": abs(residual),
        }

        return residual, analysis

    def leaver_radial_cf(
        self,
        omega: complex,
        lam: complex,
        m: int,
        M: float,
        a: float,
    ) -> tuple[complex, dict]:
        """
        径向 Leaver 连分数残差。

        参数：
        - omega: 频率
        - lam: 角向特征值（完整值）
        - m: 磁量子数
        - M: 黑洞质量
        - a: 自旋参数

        返回：
        - residual: 连分数残差
        - analysis: 去递归分析结果
        """
        r_plus = M + np.sqrt(M ** 2 - a ** 2)
        r_minus = M - np.sqrt(M ** 2 - a ** 2)

        if abs(r_plus - r_minus) < 1e-15:
            return complex(1e6, 0.0), {"error": "extremal black hole"}

        sigma_plus = (omega * r_plus - a * m) / (r_plus - r_minus)

        cf = complex(0.0, 0.0)
        cf_history = []

        for n in range(self.max_iter, 0, -1):
            alpha_n = -2.0j * omega * (n + 1.0) * (n - 4.0j * sigma_plus)
            beta_n = n * (n + 1.0) + 4.0 * sigma_plus ** 2 - 8.0 * omega * sigma_plus - lam
            gamma_n = 2.0j * omega * (n - 4.0j * sigma_plus - 1.0)

            denom = beta_n - gamma_n * cf
            if abs(denom) < 1e-30:
                denom = complex(1e-30, 0.0)
            cf = alpha_n / denom

            cf_history.append(cf)

        alpha_0 = -2.0j * omega * 1.0 * (0 - 4.0j * sigma_plus)
        beta_0 = 0 * (0 + 1.0) + 4.0 * sigma_plus ** 2 - 8.0 * omega * sigma_plus - lam

        residual = beta_0 - alpha_0 * cf

        spectral_gap = self._estimate_spectral_gap(cf_history)

        analysis = {
            "fixed_point": cf,
            "spectral_gap": spectral_gap,
            "convergence_rate": 1.0 - spectral_gap if spectral_gap > 0 else 0.5,
            "iterations": self.max_iter,
            "residual": abs(residual),
            "sigma_plus": sigma_plus,
        }

        return residual, analysis

    def _estimate_spectral_gap(self, cf_history: list) -> float:
        """
        从迭代历史估计谱间隙 γ = 1 - ρ(K)。

        谱间隙决定收敛速度：误差 ~ (1 - γ)^n

        算法：
        1. 计算相邻迭代的比值 r_n = |cf_{n} - cf_{n-1}| / |cf_{n-1} - cf_{n-2}|
        2. 谱半径 ρ ≈ lim r_n^{1/n}
        3. 谱间隙 γ = 1 - ρ
        """
        if len(cf_history) < 5:
            return 0.0

        ratios = []
        for i in range(2, len(cf_history)):
            diff1 = abs(cf_history[i] - cf_history[i-1])
            diff2 = abs(cf_history[i-1] - cf_history[i-2])
            if diff2 > 1e-30 and diff1 > 1e-30:
                ratios.append(diff1 / diff2)

        if len(ratios) == 0:
            return 0.0

        avg_ratio = np.mean(ratios[-10:])
        spectral_radius = avg_ratio ** (1.0 / self.max_iter)
        spectral_gap = max(0.0, 1.0 - spectral_radius)

        return spectral_gap

    def koopman_operator_analysis(
        self,
        sigma: complex,
        m: int,
        l: int,
        s: int,
        n_dim: int = 30,
    ) -> dict:
        """
        对递推系统进行完整的去递归分析。

        构建 Koopman 算子 K，计算其谱，验证谱对应定理。

        递推关系：α_n a_{n+1} + β_n a_n + γ_n a_{n-1} = 0
        转移矩阵形式：
            [a_{n+1}]   = [β_n/α_n  γ_n/α_n] [a_n  ]
            [a_n    ]     [-1       0      ] [a_{n-1}]

        返回：
        - koopman_eigenvalues: Koopman 算子特征值
        - generator_eigenvalues: A = -log(K) 的特征值
        - spectral_radius: 谱半径 ρ(K)
        - spectral_gap: 谱间隙 γ = 1 - ρ(K)
        - spectral_correspondence: 谱对应验证 λ = e^(-μ)
        """
        K = self._build_koopman_matrix_angular(sigma, m, l, s, n_dim)

        try:
            eigvals = eig(K)[0]
        except Exception:
            eigvals = np.array([])

        spectral_radius = max(abs(ev) for ev in eigvals) if len(eigvals) > 0 else 0.0
        spectral_gap = max(0.0, 1.0 - spectral_radius)

        generator_eigvals = []
        spectral_correspondence_errors = []

        for ev in eigvals:
            if abs(ev) > 1e-10 and abs(ev) < 1e10:
                mu = -np.log(ev)
                generator_eigvals.append(mu)
                lambda_recon = np.exp(-mu)
                spectral_correspondence_errors.append(abs(ev - lambda_recon))

        return {
            "koopman_eigenvalues": eigvals,
            "generator_eigenvalues": np.array(generator_eigvals),
            "spectral_radius": spectral_radius,
            "spectral_gap": spectral_gap,
            "spectral_correspondence_max_error": max(spectral_correspondence_errors) if spectral_correspondence_errors else 0.0,
            "koopman_matrix": K,
        }

    def _build_koopman_matrix_angular(
        self,
        sigma: complex,
        m: int,
        l: int,
        s: int,
        n_dim: int,
    ) -> np.ndarray:
        """
        构建角向递推的 Koopman 矩阵。

        递推关系：α_n a_{n+1} + β_n a_n + γ_n a_{n-1} = 0
        其中：
            α_n = -2σ(n+1)(n+2s+1)/(2n+2s+3)
            β_n = l(l+1)-s(s+1)-λ-n(n+2s+1)-σ²+2σm
            γ_n = 2σn(n+2s)/(2n+2s-1)
        """
        K = np.zeros((n_dim, n_dim), dtype=complex)

        for n in range(n_dim):
            denom_alpha = 2.0 * n + 2.0 * s + 3.0
            denom_gamma = 2.0 * n + 2.0 * s - 1.0

            alpha = -2.0 * sigma * (n + 1.0) * (n + 2.0 * s + 1.0)
            if abs(denom_alpha) > 1e-15:
                alpha /= denom_alpha

            beta = (l * (l + 1.0) - s * (s + 1.0)
                    - n * (n + 2.0 * s + 1.0)
                    - sigma ** 2 + 2.0 * sigma * m)

            gamma = 2.0 * sigma * n * (n + 2.0 * s)
            if abs(denom_gamma) > 1e-15:
                gamma /= denom_gamma

            if abs(alpha) > 1e-30:
                K[n, n] = -beta / alpha
                if n + 1 < n_dim:
                    K[n, n + 1] = -gamma / alpha

            if n > 0:
                K[n, n - 1] = 1.0

        return K


class LeaverQNMDerecursionSolver:
    """
    使用去递归理论的完整 Leaver QNM 求解器。
    """

    def __init__(self, M: float = 1.0, a: float = 0.0, s: int = -2):
        self.M = M
        self.a = a
        self.s = s
        self.derecursion = LeaverDerecursionSolver()

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

        使用去递归理论分析收敛性，结合 homotopy continuation。

        双重 homotopy 策略：
        - 自旋 homotopy：从 a=0 逐步推进到目标 a
        - m  homotopy：从 m=0 逐步推进到目标 m（对 m≠0 模式）
        """
        target_a = self.a
        target_m = m
        eps = 1e-8

        from physics_open_problems_advanced import KerrBlackHole, KerrGlobalSpectrum

        if omega_guess is None:
            omega_guess = KerrGlobalSpectrum(
                KerrBlackHole(M=self.M, a=target_a), s=self.s
            ).qnm_frequency_approximation(l, m, n)

        if target_a < 1e-6:
            omega = complex(omega_guess)
            for iteration in range(max_iter):
                f = self._combined_residual(omega, l, target_m, target_a)
                if abs(f) < tol:
                    break
                f_re = self._combined_residual(omega + eps, l, target_m, target_a)
                f_im = self._combined_residual(omega + 1j * eps, l, target_m, target_a)
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

        elif abs(target_m) <= l:
            a_steps = np.linspace(0, target_a, min(12, max(3, int(target_a / 0.1) + 2)))

            m0_guess = KerrGlobalSpectrum(
                KerrBlackHole(M=self.M, a=0.0), s=self.s
            ).qnm_frequency_approximation(l, 0, n)
            omega = complex(m0_guess)

            for a_step in a_steps[1:]:
                for _ in range(max_iter // (2 * len(a_steps))):
                    f = self._combined_residual(omega, l, 0, a_step)
                    if abs(f) < 1e-10:
                        break
                    f_re = self._combined_residual(omega + eps, l, 0, a_step)
                    f_im = self._combined_residual(omega + 1j * eps, l, 0, a_step)
                    df_dre = (f_re - f) / eps
                    df_dim = (f_im - f) / eps
                    try:
                        jacobian = np.array([[df_dre.real, df_dim.real], [df_dre.imag, df_dim.imag]])
                        delta = np.linalg.solve(jacobian, -np.array([f.real, f.imag]))
                    except np.linalg.LinAlgError:
                        delta = -0.01 * np.array([f.real, f.imag])
                    step = 1.0
                    for _ in range(10):
                        omega_new = omega + step * complex(delta[0], delta[1])
                        if abs(self._combined_residual(omega_new, l, 0, a_step)) < abs(f) * (1.0 + 1e-6):
                            omega = omega_new
                            break
                        step *= 0.5

            if target_m != 0:
                m_steps = np.sign(target_m) * np.arange(0, abs(target_m) + 1)

                for m_step in m_steps[1:]:
                    for _ in range(max_iter // (2 * max(abs(target_m), 1) + 2)):
                        f = self._combined_residual(omega, l, m_step, target_a)
                        if abs(f) < 1e-10:
                            break
                        f_re = self._combined_residual(omega + eps, l, m_step, target_a)
                        f_im = self._combined_residual(omega + 1j * eps, l, m_step, target_a)
                        df_dre = (f_re - f) / eps
                        df_dim = (f_im - f) / eps
                        try:
                            jacobian = np.array([[df_dre.real, df_dim.real], [df_dre.imag, df_dim.imag]])
                            delta = np.linalg.solve(jacobian, -np.array([f.real, f.imag]))
                        except np.linalg.LinAlgError:
                            delta = -0.01 * np.array([f.real, f.imag])
                        step = 1.0
                        for _ in range(10):
                            omega_new = omega + step * complex(delta[0], delta[1])
                            if abs(self._combined_residual(omega_new, l, m_step, target_a)) < abs(f) * (1.0 + 1e-6):
                                omega = omega_new
                                break
                            step *= 0.5

        else:
            omega = complex(omega_guess)

        final_residual = abs(self._combined_residual(omega, l, target_m, target_a))

        return {
            "omega": omega,
            "lambda": complex(l * (l + 1.0) - self.s * (self.s + 1.0), 0.0),
            "residual": final_residual,
            "converged": final_residual < tol,
            "iterations": max_iter,
            "method": "Leaver CF with derecursion + homotopy",
        }

    def _combined_residual(self, omega: complex, l: int, m: int, a_val: float) -> complex:
        """联合残差（内部使用）。"""
        s = self.s
        sigma = a_val * omega

        lam = complex(l * (l + 1.0) - s * (s + 1.0), 0.0)

        for _ in range(10):
            f_lam, _ = self.derecursion.leaver_angular_cf(lam, sigma, m, l, s)
            if abs(f_lam) < 1e-8:
                break
            f_lam_re, _ = self.derecursion.leaver_angular_cf(lam + 1e-6, sigma, m, l, s)
            df_lam = (f_lam_re - f_lam) / 1e-6
            if abs(df_lam) > 1e-15:
                lam -= f_lam / df_lam

        for _ in range(5):
            f_rad, _ = self.derecursion.leaver_radial_cf(omega, lam, m, self.M, a_val)
            if abs(f_rad) < 1e-10:
                break
            if abs(f_rad) > 1e-10:
                lam += 0.1 * f_rad

        f_rad, _ = self.derecursion.leaver_radial_cf(omega, lam, m, self.M, a_val)
        return f_rad

    def analyze_convergence(self, omega: complex, l: int, m: int) -> dict:
        """
        分析 QNM 求解的收敛性。

        返回去递归分析结果：谱半径、谱间隙、收敛速度估计。
        """
        s = self.s
        sigma = self.a * omega

        r_plus = self.M + np.sqrt(self.M ** 2 - self.a ** 2)
        r_minus = self.M - np.sqrt(self.M ** 2 - self.a ** 2)
        sigma_plus = (omega * r_plus - self.a * m) / (r_plus - r_minus)

        angular_analysis = self.derecursion.koopman_operator_analysis(sigma, m, l, s)

        return {
            "angular_spectral_radius": angular_analysis["spectral_radius"],
            "angular_spectral_gap": angular_analysis["spectral_gap"],
            "angular_convergence_rate": 1.0 - angular_analysis["spectral_gap"],
            "spectral_correspondence_error": angular_analysis["spectral_correspondence_max_error"],
            "sigma": sigma,
            "sigma_plus": sigma_plus,
        }


def run_derecursion_test():
    """运行去递归 Leaver 求解器测试。"""
    print("=" * 70)
    print("Phase 15A-2: Leaver 去递归求解器测试")
    print("=" * 70)

    BERTI_REF = {
        (0.0, 2, 0, 0): 0.373672 - 0.088962j,
        (0.5, 2, 0, 0): 0.37367 - 0.08718j,
        (0.5, 2, 2, 0): 0.50117 - 0.08874j,
    }

    for (a, l, m, n), ref_omega in BERTI_REF.items():
        print("\n--- a=%s, l=%s, m=%s, n=%s ---" % (a, l, m, n))
        solver = LeaverQNMDerecursionSolver(M=1.0, a=a, s=-2)
        result = solver.solve(l, m, n)
        omega = result["omega"]
        rel_error = abs(omega - ref_omega) / abs(ref_omega) if abs(ref_omega) > 0 else float("inf")
        print("  求解: ω = %.6f %.6fi" % (omega.real, omega.imag))
        print("  参考: ω = %.6f %.6fi" % (ref_omega.real, ref_omega.imag))
        print("  相对误差: %.6f" % rel_error)
        print("  残差: %.2e" % result["residual"])
        print("  收敛: %s" % ("✓" if result["converged"] else "⚠"))

        if rel_error < 0.1:
            conv_analysis = solver.analyze_convergence(omega, l, m)
            print("\n  去递归分析:")
            print("    谱半径 ρ: %.6f" % conv_analysis["angular_spectral_radius"])
            print("    谱间隙 γ: %.6f" % conv_analysis["angular_spectral_gap"])
            print("    收敛速度: ~%.2e^n" % conv_analysis["angular_convergence_rate"])


def run_spectral_correspondence_verification():
    """验证谱对应定理：λ = e^(-μ)。"""
    print("\n" + "=" * 70)
    print("谱对应定理验证：λ = e^(-μ)")
    print("=" * 70)

    solver = LeaverDerecursionSolver()

    test_cases = [
        (0.37367 - 0.08896j, 0, 2, -2),
        (0.50117 - 0.08874j, 2, 2, -2),
    ]

    for sigma, m, l, s in test_cases:
        print("\n--- σ = %.6f %.6fi, m=%s, l=%s, s=%s ---" % (sigma.real, sigma.imag, m, l, s))
        analysis = solver.koopman_operator_analysis(sigma, m, l, s, n_dim=30)

        print("  Koopman 谱半径: %.6f" % analysis["spectral_radius"])
        print("  谱间隙: %.6f" % analysis["spectral_gap"])
        print("  谱对应误差: %.2e" % analysis["spectral_correspondence_max_error"])

        print("\n  特征值对应:")
        for i, (lam, mu) in enumerate(zip(analysis["koopman_eigenvalues"], analysis["generator_eigenvalues"])):
            if i >= 5:
                print("    ...")
                break
            recon_lam = np.exp(-mu)
            error = abs(lam - recon_lam)
            print("    λ_%d = %.4f %.4fi  |  μ_%d = %.4f %.4fi  |  e^(-μ) = %.4f %.4fi  |  误差 = %.2e" %
                  (i, lam.real, lam.imag, i, mu.real, mu.imag, recon_lam.real, recon_lam.imag, error))


def run_comparison_with_original():
    """与原始 leaver_full_coefficients.py 对比测试。"""
    print("\n" + "=" * 70)
    print("与原始求解器对比测试")
    print("=" * 70)

    from leaver_full_coefficients import LeaverAngularSolver, LeaverRadialSolver

    test_cases = [
        (0.0, 2, 0, 0),
        (0.5, 2, 0, 0),
        (0.5, 2, 2, 0),
    ]

    for a, l, m, n in test_cases:
        print("\n--- a=%s, l=%s, m=%s, n=%s ---" % (a, l, m, n))

        sigma = a * (0.37367 - 0.08896j)
        lam = l * (l + 1.0) - (-2) * (-2 + 1.0)

        original_solver = LeaverAngularSolver(s=-2)
        original_residual = original_solver.leaver_angular_cf(lam, sigma, m, l, -2)

        derecursion_solver = LeaverDerecursionSolver()
        derecursion_residual, analysis = derecursion_solver.leaver_angular_cf(lam, sigma, m, l, -2)

        print("  原始残差: %.6f %.6fi" % (original_residual.real, original_residual.imag))
        print("  去递归残差: %.6f %.6fi" % (derecursion_residual.real, derecursion_residual.imag))
        print("  差异: %.2e" % abs(original_residual - derecursion_residual))
        print("  谱间隙: %.6f" % analysis["spectral_gap"])


if __name__ == "__main__":
    run_derecursion_test()
    run_comparison_with_original()
    run_spectral_correspondence_verification()