#!/usr/bin/env python3
"""
_dirac_polynomial_solver.py —— Dirac QNM 多项式形式连分数求解器

使用 Cook-Zalutskiy (2014) 的 D 系数多项式形式，扩展支持半整数自旋 s=-0.5。

核心改进：
1. 放弃 _spin_weight_coeff.py 中错误的乘积形式系数
2. 使用 LeaverResidual 的 D 系数公式（已验证对 s=-2 正确）
3. 适当修改类型签名支持 float s, l, m
4. 修复 MatrixAngularSolver 对半整数 l 的支持

参考：
    Cook & Zalutskiy (2014) Phys. Rev. D 90, 124021
    Leaver (1985) Proc. R. Soc. Lond. A 402, 285-298
    Dolan & Gair (2006) arXiv:gr-qc/0612024
"""

from __future__ import annotations

import numpy as np
import sys, os
from typing import Optional, Dict, Any, Tuple, List, Callable

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dynamic_spectrum"))


# ============================================================
# 1. 修正后的矩阵法角向求解器（支持半整数自旋）
# ============================================================

class DiracMatrixAngularSolver:
    """
    角向 Dirac 自旋加权椭球谐函数求解器（矩阵谱方法）。

    扩展自 leaver_unified_solver.py 的 MatrixAngularSolver：
    - 支持 float s（半整数自旋）
    - 自动处理半整数 l_min 的矩阵尺寸
    - 使用 np.linspace 代替 np.arange 避免步长误解
    """

    def __init__(self, s: float = -0.5, l_max: int = 15):
        self.s = s
        self.l_max = l_max

    def _calF(self, l: float, m: float) -> float:
        """
        F(l,m) = sqrt(((l+1)²-m²)/(2l+3)(2l+1)) * sqrt(((l+1)²-s²)/(l+1)²)
        """
        if (0 == self.s) and (0 == l + 1):
            return 0.
        # 对半整数 l，l+1 > 0 总是成立
        return (np.sqrt(((l + 1) ** 2 - m * m) / (2 * l + 3) / (2 * l + 1))
                * np.sqrt(((l + 1) ** 2 - self.s * self.s) / (l + 1) ** 2))

    def _calG(self, l: float, m: float) -> float:
        """
        G(l,m) = sqrt((l²-m²)/(4l²-1)) * sqrt(1 - s²/l²)
        
        对 l = |s|（最小 l），不存在 l-1 耦合，返回 0。
        """
        l_min = max(abs(self.s), abs(m))
        if l <= l_min:
            return 0.
        return np.sqrt((l * l - m * m) / (4 * l * l - 1)) * np.sqrt(1 - self.s * self.s / l / l)

    def _calH(self, l: float, m: float) -> float:
        """
        H(l,m) = -m·s / (l(l+1))
        """
        if 0 == l or 0 == self.s:
            return 0.
        return -m * self.s / (l * (l + 1))

    def _calA(self, l: float, m: float) -> float:
        return self._calF(l, m) * self._calF(l + 1, m)

    def _calD(self, l: float, m: float) -> float:
        return self._calF(l, m) * (self._calH(l + 1, m) + self._calH(l, m))

    def _calB(self, l: float, m: float) -> float:
        return (self._calF(l, m) * self._calG(l + 1, m)
                + self._calG(l, m) * self._calF(l - 1, m)
                + self._calH(l, m) ** 2)

    def _calE(self, l: float, m: float) -> float:
        return self._calG(l, m) * (self._calH(l - 1, m) + self._calH(l, m))

    def _calC(self, l: float, m: float) -> float:
        return self._calG(l, m) * self._calG(l - 1, m)

    def _swsphericalh_A(self, l: float, m: float) -> float:
        return l * (l + 1) - self.s * (self.s + 1)

    def _M_matrix_elem(self, c: complex, m: float, l: float, lprime: float) -> complex:
        if lprime == l - 2:
            return -c * c * self._calA(lprime, m)
        if lprime == l - 1:
            return (-c * c * self._calD(lprime, m) + 2 * c * self.s * self._calF(lprime, m))
        if lprime == l:
            return (self._swsphericalh_A(lprime, m)
                    - c * c * self._calB(lprime, m)
                    + 2 * c * self.s * self._calH(lprime, m))
        if lprime == l + 1:
            return (-c * c * self._calE(lprime, m) + 2 * c * self.s * self._calG(lprime, m))
        if lprime == l + 2:
            return -c * c * self._calC(lprime, m)
        return 0.j

    def solve_eigenvalue(self, l: float, m: float, sigma: complex,
                         A_ref: Optional[complex] = None) -> Dict[str, Any]:
        """
        求解角向分离常数 λ_{slm}。

        参数:
            l: 角量子数（整数或半整数）
            m: 磁量子数（整数或半整数）
            sigma: σ = a·ω
            A_ref: 参考特征值（分支跟踪）

        返回:
            { 'A': complex, 'eigenvector': ndarray, 'ells': ndarray }
        """
        c = sigma
        l_min = max(abs(self.s), abs(m))

        # l_max 确保包含足够的基函数
        # 对半整数 l，从 l_min 以步长 1 增加到 l_max_val
        # 确保总数量 n_ell 是整数
        n_base_ells = max(self.l_max, int(l) + 5)
        
        # 构造 l 序列
        ells = np.linspace(l_min, n_base_ells, int(n_base_ells - l_min + 1))
        n_ell = len(ells)

        M_mat = np.zeros((n_ell, n_ell), dtype=complex)

        for i, li in enumerate(ells):
            for j, lj in enumerate(ells):
                M_mat[i, j] = self._M_matrix_elem(c, m, li, lj)

        eigenvalues, eigenvectors = np.linalg.eig(M_mat)

        if A_ref is not None and np.isfinite(A_ref):
            ref_val = A_ref
        else:
            ref_val = l * (l + 1) - self.s * (self.s + 1)

        idx = np.argmin(np.abs(eigenvalues - ref_val))

        return {
            "A": eigenvalues[idx],
            "eigenvector": eigenvectors[:, idx],
            "ells": ells,
            "l_min": l_min,
            "converged": True,
        }


# ============================================================
# 2. Dirac 径向多项式形式连分数（Cook-Zalutskiy D 系数）
# ============================================================

class DiracPolynomialSolver:
    """
    Dirac QNM 多项式形式连分数求解器。

    使用 Cook-Zalutskiy (2014) 的 D 系数多项式形式。
    核心假设：D 系数公式对任意 s 有效（包括半整数自旋）。
    """

    def __init__(self, M: float = 1.0, a: float = 0.0,
                 s: float = -0.5, max_iter: int = 200):
        self.M = M
        self.a = a
        self.s = s
        self.max_iter = max_iter
        self.r_plus = M + np.sqrt(max(0.0, M ** 2 - a ** 2))
        self.r_minus = M - np.sqrt(max(0.0, M ** 2 - a ** 2))
        self._angular_solver = DiracMatrixAngularSolver(s=s)

    # ------------------------------------------------------------------
    #  角向特征值
    # ------------------------------------------------------------------

    def angular_eigenvalue(self, l: float, m: float, omega: complex,
                           lam_guess: Optional[complex] = None) -> complex:
        """
        用矩阵谱方法求角向特征值 λ。

        a=0 时退化为精确值 λ = l(l+1) - s(s+1)（对任意 ω）。
        """
        if abs(self.a) < 1e-15:
            # Schwarzschild a=0 时，λ 是实数且与 ω 无关
            return complex(l * (l + 1) - self.s * (self.s + 1), 0.0)

        sigma = self.a * omega
        result = self._angular_solver.solve_eigenvalue(
            l=l, m=m, sigma=sigma, A_ref=lam_guess)
        return result["A"]

    # ------------------------------------------------------------------
    #  径向 D 系数（Cook-Zalutskiy 2014 Eq.31）
    # ------------------------------------------------------------------

    def _D_coeffs(self, omega: complex, lam: complex,
                   m: float) -> np.ndarray:
        """
        Cook-Zalutskiy 多项式形式的 D₀-D₄ 系数。

        公式中的参数通过 Teukolsky 方程推导：
        - xi = -s - i·σ₊  （视界入射波指数）
        - eta = -i·σ₋     （内视界指数）
        - zeta = iω       （无穷远处出射波指数）
        """
        # M=1 归一化
        root = np.sqrt(max(0.0, 1.0 - self.a ** 2))
        r_p = 1.0 + root
        r_m = 1.0 - root

        sigma_p = (2.0 * omega * r_p - self.a * m) / (2.0 * root)
        sigma_m = (2.0 * omega * r_m - self.a * m) / (2.0 * root)

        s = self.s
        zeta = 1.0j * omega
        xi = -s - 1.0j * sigma_p
        eta = -1.0j * sigma_m

        p = root * zeta
        # alpha = 1 + s + ξ + η - 2ζ + s
        alpha = 1.0 + s + xi + eta - 2.0 * zeta + s
        gamma_coef = 1.0 + s + 2.0 * eta
        delta = 1.0 + s + 2.0 * xi

        # sigma 项（包含自旋相关耦合）
        # 4isωr 项在坐标变换后贡献 4·s·ω² 到 D 系数：
        #   s=-2: 4*(-2)*ω² = -8ω²  （Cook-Zalutskiy 原始公式）
        #   s=-1: 4*(-1)*ω² = -4ω²
        #   s=-0.5: 4*(-0.5)*ω² = -2ω²
        sigma_D = (lam + self.a ** 2 * omega ** 2 + 4.0 * s * omega ** 2
                   + p * (2.0 * alpha + gamma_coef - delta)
                   + (1.0 + s - 0.5 * (gamma_coef + delta))
                   * (s + 0.5 * (gamma_coef + delta)))

        D = np.zeros(5, dtype=complex)
        D[0] = delta
        D[1] = 4.0 * p - 2.0 * alpha + gamma_coef - delta - 2.0
        D[2] = 2.0 * alpha - gamma_coef + 2.0
        D[3] = alpha * (4.0 * p - delta) - sigma_D
        D[4] = alpha * (alpha - gamma_coef + 1.0)
        return D

    def _polynomial_alpha(self, n: int, D: np.ndarray) -> complex:
        return n * n + (D[0] + 1.0) * n + D[0]

    def _polynomial_beta(self, n: int, D: np.ndarray) -> complex:
        return -2.0 * n * n + (D[1] + 2.0) * n + D[3]

    def _polynomial_gamma(self, n: int, D: np.ndarray) -> complex:
        return n * n + (D[2] - 3.0) * n + D[4] - D[2] + 2.0

    # ------------------------------------------------------------------
    #  径向连分数求值
    # ------------------------------------------------------------------

    def radial_cf_polynomial(self, omega: complex, lam: complex,
                              m: float, n_inv: int = 0) -> complex:
        """
        径向多项式形式连分数 Rₙ(ω) 的值。

        使用反转连分数（inverted continued fraction）：
            R₀(ω) = β₀ - γ₀·R¹F - α₀·R¹B = 0

        对 n_inv=0：标准连分数条件 R₀(ω) = 0。
        对 n_inv=n：第 n 泛音。
        """
        D = self._D_coeffs(omega, lam, m)

        # 前向迭代
        conv1 = 0.0j
        for i in range(0, n_inv):
            denom = self._polynomial_beta(i, D) - self._polynomial_gamma(i, D) * conv1
            if abs(denom) < 1e-30:
                denom = 1e-30j
            conv1 = self._polynomial_alpha(i, D) / denom

        # 后向迭代
        conv2 = 0.0j
        for i in range(self.max_iter, n_inv, -1):
            denom = self._polynomial_beta(i, D) - self._polynomial_alpha(i, D) * conv2
            if abs(denom) < 1e-30:
                denom = 1e-30j
            conv2 = self._polynomial_gamma(i, D) / denom

        return (self._polynomial_beta(n_inv, D)
                - self._polynomial_gamma(n_inv, D) * conv1
                - self._polynomial_alpha(n_inv, D) * conv2)

    # ------------------------------------------------------------------
    #  Müller 法求 QNM 频率
    # ------------------------------------------------------------------

    def find_qnm(self, l: float, m: float, n: int = 0,
                  omega_guess: Optional[complex] = None,
                  lam: Optional[complex] = None,
                  max_iter: int = 50,
                  tol: float = 1e-10) -> Dict[str, Any]:
        """
        求 Dirac QNM 频率 ω。

        使用 Müller 法在复 ω 平面求径向 CF 残差的零点。
        """
        if omega_guess is None:
            if abs(self.a) < 1e-10:
                # Schwarzschild 参考值
                ref_table = {
                    (0.5, 0.5): 0.378721 - 0.096458j,
                    (0.5, -0.5): 0.378721 - 0.096458j,
                    (1.5, 1.5): 0.522988 - 0.089964j,
                    (1.5, -1.5): 0.522988 - 0.089964j,
                    (2.5, 2.5): 0.640418 - 0.091694j,
                }
                omega_guess = ref_table.get((l, m), complex(0.4, -0.09))
            else:
                omega_guess = complex(0.35 + 0.5 * self.a * m / (l + 0.5),
                                      -0.097 + 0.02 * self.a * self.a)

        # 角向特征值
        if lam is None:
            lam = self.angular_eigenvalue(l, m, omega_guess)

        # 残差函数
        def cf_residual(w: complex) -> complex:
            nonlocal lam
            if abs(self.a) > 1e-10:
                lam = self.angular_eigenvalue(l, m, w, lam_guess=lam)
            return self.radial_cf_polynomial(w, lam, m, n_inv=n)

        # Müller 法初始点
        w0 = omega_guess
        w1 = omega_guess * complex(1.005, 0.0)
        w2 = omega_guess * complex(1.0, 0.005)

        def muller_step(f, x0, x1, x2):
            f0, f1, f2 = f(x0), f(x1), f(x2)
            h1 = x1 - x0
            h2 = x2 - x1
            d1 = (f1 - f0) / h1
            d2 = (f2 - f1) / h2
            a = (d2 - d1) / (h2 + h1)

            if abs(a) < 1e-30:
                if abs(d2) < 1e-30:
                    return x2 + 0.1
                return x2 - f2 / d2

            b = d2 + h2 * a
            disc = np.sqrt(b ** 2 - 4.0 * a * f2)

            if abs(b + disc) > abs(b - disc):
                denom = b + disc
            else:
                denom = b - disc

            if abs(denom) < 1e-30:
                return x2 + 0.1

            return x2 - 2.0 * f2 / denom

        for iteration in range(max_iter):
            w_new = muller_step(cf_residual, w0, w1, w2)
            residual = abs(cf_residual(w_new))

            if residual < tol:
                return {
                    'omega': w_new,
                    'cf_residual': residual,
                    'lam': lam,
                    'converged': True,
                    'iterations': iteration + 1,
                }

            w0, w1, w2 = w1, w2, w_new

        return {
            'omega': w2,
            'cf_residual': abs(cf_residual(w2)),
            'lam': lam,
            'converged': False,
            'iterations': max_iter,
        }


# ============================================================
# 3. 验证函数
# ============================================================

def verify_at_reference():
    """验证多项式形式在参考频率处的残差。"""
    print("=" * 80)
    print("验证：多项式形式 D 系数在参考频率处的残差")
    print("=" * 80)

    # 测试用例：s=-2 (引力) 和 s=-0.5 (Dirac)
    test_cases = [
        # (s, l, m, a, ω_ref, λ, 名称)
        (-2, 2, 0, 0.0, 0.373672 - 0.088962j, 4.0, "引力 s=-2"),
        (-0.5, 0.5, 0.5, 0.0, 0.378721 - 0.096458j, 1.0, "Dirac s=-0.5 l=0.5"),
        (-0.5, 1.5, 1.5, 0.0, 0.522988 - 0.089964j, 3.0, "Dirac s=-0.5 l=1.5"),
        (-0.5, 2.5, 2.5, 0.0, 0.640418 - 0.091694j, 7.0, "Dirac s=-0.5 l=2.5"),
        # s=-1 (电磁) 作为额外验证
        (-1, 1, 0, 0.0, 0.2483 - 0.0926j, 2.0, "EM s=-1 l=1"),
    ]

    for s, l, m, a, omega, lam, name in test_cases:
        solver = DiracPolynomialSolver(M=1.0, a=a, s=s, max_iter=300)

        print(f"\n  [{name}]")
        print(f"    ω_ref = {omega:.12f}")
        print(f"    λ     = {lam:.10f}")

        r = solver.radial_cf_polynomial(omega, lam, m, n_inv=0)
        r2 = solver.radial_cf_polynomial(omega, lam, m, n_inv=1)

        print(f"    |R₀(ω_ref)| = {abs(r):.6e}")
        print(f"    |R₁(ω_ref)| = {abs(r2):.6e}")

        if abs(r) < 1e-3:
            print(f"    → ✓ 多项式形式在参考频率处残差可接受")
        else:
            print(f"    → ✗ 残差较大，需要进一步检查 D 系数")
            # 打印 D 系数帮助诊断
            D = solver._D_coeffs(omega, lam, m)
            print(f"    D₀-D₄ = {D}")


def verify_n_convergence():
    """验证连分数截断 N 的收敛性。"""
    print("\n" + "=" * 80)
    print("验证：连分数截断 N 的收敛性")
    print("=" * 80)

    test_cases = [
        (-2, 2, 0, 0.0, 0.373672 - 0.088962j, 4.0, "引力 s=-2"),
        (-0.5, 0.5, 0.5, 0.0, 0.378721 - 0.096458j, 1.0, "Dirac s=-0.5"),
    ]

    for s, l, m, a, omega, lam, name in test_cases:
        print(f"\n  [{name}]")
        print(f"  {'N':<8} {'|R₀|':<16} {'Δ|R₀|':<16}")

        prev_r = None
        for N in [30, 50, 80, 100, 150, 200, 300, 400]:
            solver = DiracPolynomialSolver(M=1.0, a=a, s=s, max_iter=N)
            r = solver.radial_cf_polynomial(omega, lam, m)
            delta = abs(abs(r) - abs(prev_r)) if prev_r is not None else float('inf')
            print(f"  {N:<8} {abs(r):<16.6e} {delta:<16.2e}")
            prev_r = r


def test_qnm_finding():
    """测试用 Müller 法求 QNM 频率。"""
    print("\n" + "=" * 80)
    print("测试：Müller 法求 Dirac QNM")
    print("=" * 80)

    test_cases = [
        (-0.5, 0.0, 0.5, 0.5, 0),
        (-0.5, 0.0, 1.5, 1.5, 0),
        (-0.5, 0.0, 2.5, 2.5, 0),
    ]

    for s, a, l, m, n in test_cases:
        solver = DiracPolynomialSolver(M=1.0, a=a, s=s, max_iter=300)
        result = solver.find_qnm(l, m, n=n, max_iter=50, tol=1e-10)

        status = "✓" if result['converged'] else "✗"
        print(f"  s={s:.1f} a={a:.3f} l={l:.1f} m={m:+.1f} n={n}: "
              f"ω = {result['omega'].real:.10f} {result['omega'].imag:+.10f}i "
              f"|R₀| = {result['cf_residual']:.2e} {status}")


if __name__ == "__main__":
    verify_at_reference()
    verify_n_convergence()
    test_qnm_finding()
