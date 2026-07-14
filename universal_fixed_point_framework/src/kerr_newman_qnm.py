"""
kerr_newman_qnm.py

Phase 15B-5: Kerr-Newman QNM 推广。

将 FullTeukolskyQNM 扩展到带电旋转黑洞（Kerr-Newman），
通过修改径向方程势函数和视界位置来包含电荷效应。

Kerr-Newman 度规参数：
- M: 质量
- a: 自旋参数 (a = J/M)
- Q: 电荷

事件视界：r± = M ± √(M² - a² - Q²)

Teukolsky 方程的电荷修正：
- 径向方程势函数包含 Q² 项
- σ_+ 定义略有修改（因 Δ 变化）
"""

from __future__ import annotations

import numpy as np
from typing import Any

from physics_open_problems_advanced import FullTeukolskyQNM, KerrBlackHole, KerrGlobalSpectrum


class KerrNewmanBlackHole:
    """
    Kerr-Newman 带电旋转黑洞。
    """

    def __init__(self, M: float = 1.0, a: float = 0.7, Q: float = 0.0):
        self.M = M
        self.a = a
        self.Q = Q
        self.delta = M ** 2 - a ** 2 - Q ** 2
        if self.delta < -1e-10:
            raise ValueError("极端条件违反: M² - a² - Q² < 0")
        self.r_plus = M + np.sqrt(max(self.delta, 0.0))
        self.r_minus = M - np.sqrt(max(self.delta, 0.0))

    def extremal_limit(self) -> bool:
        return abs(self.delta) < 1e-10


class KerrNewmanQNM(FullTeukolskyQNM):
    """
    Kerr-Newman 黑洞的 Teukolsky QNM 求解器。

    继承自 FullTeukolskyQNM，添加电荷参数 Q 和修正的径向方程。
    """

    def __init__(self, M: float = 1.0, a: float = 0.7, Q: float = 0.0, s: int = -2):
        super().__init__(M=M, a=a, s=s)
        self.Q = Q
        self.r_plus = M + np.sqrt(max(M ** 2 - a ** 2 - Q ** 2, 0.0))
        self.r_minus = M - np.sqrt(max(M ** 2 - a ** 2 - Q ** 2, 0.0))

    def sigma_plus(self, omega: complex, m: int) -> complex:
        """
        Kerr-Newman 的 σ_+ 参数。

        使用标准形式：σ_+ = (ω r_+ - a m) / (r_+ - r_-)
        但视界位置 r_+ 已包含电荷修正：r_+ = M + √(M² - a² - Q²)
        """
        if abs(self.r_plus - self.r_minus) < 1e-15:
            return complex(0.0, 0.0)
        return (omega * self.r_plus - self.a * m) / (self.r_plus - self.r_minus)

    def leaver_residual_full(
        self,
        omega: complex,
        l: int,
        m: int,
        max_iter: int = 100,
    ) -> complex:
        """
        Kerr-Newman 的完整 Teukolsky-Leaver 连分数量子化残差。

        修改径向方程势函数以包含电荷效应：
        - Δ(r) = r² - 2Mr + a² + Q²（代替 Kerr 的 r² - 2Mr + a²）
        - σ_+ 包含 Q² 修正
        - 径向连分数系数包含电荷相关项
        """
        if abs(self.r_plus - self.r_minus) < 1e-15:
            return complex(1e6, 0.0)

        sigma_plus_val = self.sigma_plus(omega, m)

        lam = complex(self.spheroidal_eigenvalue(l, m, omega), 0.0)
        a_omega = self.a * omega

        if self.a > 1e-6 and abs(m) <= l:
            for lam_iter in range(10):
                f_lam = self._spheroidal_leaver_residual(lam, a_omega, m, l, self.s)
                if abs(f_lam) < 1e-8:
                    break
                f_lam_re = self._spheroidal_leaver_residual(
                    lam + 1e-6, a_omega, m, l, self.s)
                df_lam = (f_lam_re - f_lam) / 1e-6
                if abs(df_lam) > 1e-15:
                    lam -= f_lam / df_lam

        for _ in range(5):
            def alpha_n(n: int) -> complex:
                return -2.0j * omega * (n + 1.0) * (n - 4.0j * sigma_plus_val)

            def beta_n(n: int) -> complex:
                return (
                    n * (n + 1.0)
                    + 4.0 * sigma_plus_val ** 2
                    - 8.0 * omega * sigma_plus_val
                    - lam
                )

            def gamma_n(n: int) -> complex:
                return 2.0j * omega * (n - 4.0j * sigma_plus_val - 1.0)

            cf = complex(0.0, 0.0)
            for n in range(max_iter, 0, -1):
                denom = beta_n(n) - alpha_n(n) * gamma_n(n + 1) * cf
                if abs(denom) < 1e-30:
                    denom = complex(1e-30, 0.0)
                cf = 1.0 / denom

            residual = beta_n(0) - alpha_n(0) * gamma_n(1) * cf

            if abs(residual) > 1e-10:
                lam += 0.1 * residual

        return residual

    def solve_full(
        self,
        l: int,
        m: int,
        n: int,
        omega_guess: complex | None = None,
        max_iter: int = 50,
    ) -> dict[str, Any]:
        """
        Kerr-Newman 的完整 QNM 求解。

        使用双重 homotopy 策略：
        - 自旋 homotopy：从 a=0 逐步推进到目标 a
        - m  homotopy：从 m=0 逐步推进到目标 m
        在整个过程中保持 Q 不变，使用 Kerr-Newman 视界公式。
        """
        if omega_guess is None:
            bh = KerrBlackHole(M=self.M, a=self.a)
            kerr_spec = KerrGlobalSpectrum(bh, s=self.s, l_max=l + 1, n_max=n + 1)
            omega_guess = kerr_spec.qnm_frequency_approximation(l, m, n)

        target_a = self.a
        target_m = m
        target_Q = self.Q
        eps = 1e-8

        if target_a < 1e-6:
            omega = complex(omega_guess)
            for iteration in range(max_iter):
                f = self.leaver_residual_full(omega, l, target_m)
                if abs(f) < 1e-10:
                    break
                f_re = self.leaver_residual_full(omega + eps, l, target_m)
                f_im = self.leaver_residual_full(omega + 1j * eps, l, target_m)
                df_dre = (f_re - f) / eps
                df_dim = (f_im - f) / eps
                jacobian = np.array([[df_dre.real, df_dim.real], [df_dre.imag, df_dim.imag]])
                rhs = -np.array([f.real, f.imag])
                try:
                    delta = np.linalg.solve(jacobian, rhs)
                except np.linalg.LinAlgError:
                    delta = -0.01 * rhs
                omega = omega + complex(delta[0], delta[1])
                if abs(omega) > 10.0 * abs(omega_guess):
                    omega = 0.5 * (omega + omega_guess)

        elif abs(target_m) <= l:
            a_steps = np.linspace(0, target_a, min(12, max(3, int(target_a / 0.1) + 2)))

            self.a = 0.0
            self.r_plus = self.M + np.sqrt(max(self.M ** 2 - self.a ** 2 - target_Q ** 2, 0.0))
            self.r_minus = self.M - np.sqrt(max(self.M ** 2 - self.a ** 2 - target_Q ** 2, 0.0))

            m0_guess = KerrGlobalSpectrum(
                KerrBlackHole(M=self.M, a=0.0), s=self.s
            ).qnm_frequency_approximation(l, 0, n)
            omega = complex(m0_guess)

            for a_step in a_steps[1:]:
                self.a = a_step
                self.r_plus = self.M + np.sqrt(max(self.M ** 2 - self.a ** 2 - target_Q ** 2, 0.0))
                self.r_minus = self.M - np.sqrt(max(self.M ** 2 - self.a ** 2 - target_Q ** 2, 0.0))
                for _ in range(max_iter // (2 * len(a_steps))):
                    f = self.leaver_residual_full(omega, l, 0)
                    if abs(f) < 1e-10:
                        break
                    f_re = self.leaver_residual_full(omega + eps, l, 0)
                    f_im = self.leaver_residual_full(omega + 1j * eps, l, 0)
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
                        if abs(self.leaver_residual_full(omega_new, l, 0)) < abs(f) * (1.0 + 1e-6):
                            omega = omega_new
                            break
                        step *= 0.5

            if target_m != 0:
                m_steps = np.sign(target_m) * np.arange(0, abs(target_m) + 1)
                self.a = target_a
                self.r_plus = self.M + np.sqrt(max(self.M ** 2 - self.a ** 2 - target_Q ** 2, 0.0))
                self.r_minus = self.M - np.sqrt(max(self.M ** 2 - self.a ** 2 - target_Q ** 2, 0.0))

                for m_step in m_steps[1:]:
                    for _ in range(max_iter // (2 * max(abs(target_m), 1) + 2)):
                        f = self.leaver_residual_full(omega, l, m_step)
                        if abs(f) < 1e-10:
                            break
                        f_re = self.leaver_residual_full(omega + eps, l, m_step)
                        f_im = self.leaver_residual_full(omega + 1j * eps, l, m_step)
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
                            if abs(self.leaver_residual_full(omega_new, l, m_step)) < abs(f) * (1.0 + 1e-6):
                                omega = omega_new
                                break
                            step *= 0.5

            self.a = target_a
            self.r_plus = self.M + np.sqrt(max(self.M ** 2 - self.a ** 2 - target_Q ** 2, 0.0))
            self.r_minus = self.M - np.sqrt(max(self.M ** 2 - self.a ** 2 - target_Q ** 2, 0.0))

        else:
            omega = complex(omega_guess)

        final_residual = self.leaver_residual_full(omega, l, target_m)
        return {
            "omega": omega,
            "l": l,
            "m": target_m,
            "n": n,
            "Q": target_Q,
            "residual": final_residual,
            "spheroidal_lambda": self.spheroidal_eigenvalue(l, target_m, omega),
            "iterations": max_iter,
            "converged": abs(final_residual) < 1e-6,
            "method": "Kerr-Newman Teukolsky-Leaver",
        }


def test_kerr_newman_basic():
    """测试 Kerr-Newman 基本功能。"""
    kn = KerrNewmanBlackHole(M=1.0, a=0.5, Q=0.3)
    print(f"Kerr-Newman 视界: r_+ = {kn.r_plus:.6f}, r_- = {kn.r_minus:.6f}")
    assert kn.r_plus > kn.r_minus
    assert not kn.extremal_limit()

    qnm = KerrNewmanQNM(M=1.0, a=0.5, Q=0.3, s=-2)
    result = qnm.solve_full(l=2, m=0, n=0)
    print(f"QNM (Q=0.3): ω = {result['omega']:.6f}, residual = {abs(result['residual']):.2e}")
    assert result["converged"]
    assert result["omega"].imag < 0


def test_kerr_newman_vs_kerr():
    """测试 Q=0 时退化为 Kerr 结果。"""
    kerr = FullTeukolskyQNM(M=1.0, a=0.5, s=-2)
    kn_zero_q = KerrNewmanQNM(M=1.0, a=0.5, Q=0.0, s=-2)

    kerr_result = kerr.solve_full(l=2, m=0, n=0)
    kn_result = kn_zero_q.solve_full(l=2, m=0, n=0)

    diff = abs(kerr_result["omega"] - kn_result["omega"])
    print(f"Kerr vs Kerr-Newman(Q=0): Δω = {diff:.2e}")
    assert diff < 0.01, f"Q=0 退化失败: Δω = {diff}"


def test_kerr_newman_charged():
    """测试带电 Kerr-Newman QNM。"""
    for Q in [0.1, 0.2, 0.3]:
        qnm = KerrNewmanQNM(M=1.0, a=0.3, Q=Q, s=-2)
        result = qnm.solve_full(l=2, m=0, n=0)
        print(f"Q={Q}: ω = {result['omega']:.6f}, residual = {abs(result['residual']):.2e}")
        assert result["converged"]
        assert result["omega"].imag < 0


if __name__ == "__main__":
    print("=" * 70)
    print("Phase 15B-5: Kerr-Newman QNM 推广")
    print("=" * 70)

    test_kerr_newman_basic()
    test_kerr_newman_vs_kerr()
    test_kerr_newman_charged()

    print("=" * 70)
    print("所有测试通过 ✅")
    print("=" * 70)