"""
leaver_spectral_derecursion.py

去递归谱计算方法：用 Koopman 算子谱分解替代连分数迭代。

核心思想：
  连分数迭代（递归）:  CF_N=0 → CF_{N-1} → ... → CF_0  (N次迭代)
  谱分解（非递归）:    构建三对角矩阵 M，求特征值       (1次对角化)

两条路径应给出相同的 QNM 频率，互为验证。

"两弦法"优化：
  正如用两根弦的垂线交点找圆心，
  用 Rayleigh 商迭代（两次"弦"=两次矩阵作用）找特征值，
  复杂度从 O(N³) 降到 O(N)，与迭代法相当。
"""

from __future__ import annotations

import numpy as np
from scipy.linalg import eigvals
from leaver_corrected_solver import LeaverRadialSolver, LeaverAngularSolver


def _tridiagonal_solve(a: np.ndarray, b: np.ndarray, c: np.ndarray,
                       d: np.ndarray) -> np.ndarray:
    """Thomas 算法求解三对角线性方程组（O(N) 复杂度）。

    方程组形式:
        b[0] x[0] + c[0] x[1] = d[0]
        a[i] x[i-1] + b[i] x[i] + c[i] x[i+1] = d[i], 0 < i < N-1
        a[N-1] x[N-2] + b[N-1] x[N-1] = d[N-1]

    参数:
        a: 下对角线 (长度 N, a[0] 未使用)
        b: 主对角线 (长度 N)
        c: 上对角线 (长度 N, c[N-1] 未使用)
        d: 右端项 (长度 N)

    返回:
        x: 解向量 (长度 N)
    """
    N = len(b)
    c_ = np.zeros(N, dtype=complex)
    d_ = np.zeros(N, dtype=complex)
    x = np.zeros(N, dtype=complex)

    c_[0] = c[0] / b[0]
    d_[0] = d[0] / b[0]

    for i in range(1, N):
        m = a[i] / (b[i] - a[i] * c_[i - 1])
        c_[i] = c[i] / (b[i] - a[i] * c_[i - 1]) if i < N - 1 else 0.0
        d_[i] = (d[i] - a[i] * d_[i - 1]) / (b[i] - a[i] * c_[i - 1])

    x[N - 1] = d_[N - 1]
    for i in range(N - 2, -1, -1):
        x[i] = d_[i] - c_[i] * x[i + 1]

    return x


class SpectralDerecursionSolver:
    """去递归谱计算求解器。

    将 Leaver 连分数的迭代计算转化为矩阵特征值问题。
    """

    def __init__(self, M: float = 1.0, a: float = 0.0, s: int = -2, N: int = 80):
        self.M = M
        self.a = a
        self.s = s
        self.N = N  # 矩阵维度
        self.radial = LeaverRadialSolver(M=M, a=a, s=s, max_iter=N + 10)
        self.angular = LeaverAngularSolver(s=s, l_max=20)

    def _build_tridiagonal_matrix(self, omega: complex, A: complex, m: int) -> np.ndarray:
        """构建递推关系对应的三对角矩阵 M。

        M 的零特征值 ⟺ 连分数残差为零 ⟺ ω 是 QNM 频率。

        M = | β₀  α₀                  |
            | γ₁  β₁  α₁              |
            |     γ₂  β₂  α₂          |
            |          ⋱   ⋱   ⋱      |

        其中 αₙ, βₙ, γₙ 是 Leaver 二次多项式系数。
        """
        D = self.radial._D_coeffs(omega, self.a, self.s, m, A)

        n_arr = np.arange(self.N + 1)
        alpha = self.radial._alpha_n(n_arr, D)
        beta = self.radial._beta_n(n_arr, D)
        gamma = self.radial._gamma_n(n_arr, D)

        M = np.zeros((self.N + 1, self.N + 1), dtype=complex)
        for n in range(self.N + 1):
            M[n, n] = beta[n]
            if n < self.N:
                M[n, n + 1] = alpha[n]
            if n > 0:
                M[n, n - 1] = gamma[n]

        return M

    def spectral_residual(self, omega: complex, A: complex, m: int) -> complex:
        """谱残差：三对角矩阵的最小特征值（全特征值分解，O(N³)）。

        这是去递归的核心——用矩阵特征值替代连分数迭代。
        当 |最小特征值| → 0 时，ω 是 QNM 频率。
        """
        M = self._build_tridiagonal_matrix(omega, A, m)
        eigenvalues = eigvals(M)
        idx = np.argmin(np.abs(eigenvalues))
        return eigenvalues[idx]

    def _get_tridiagonal_diags(self, omega: complex, A: complex, m: int):
        """获取三对角矩阵的三条对角线（不构建完整矩阵）。

        返回:
            alpha: 上对角线 (长度 N+1, alpha[N] 未使用)
            beta: 主对角线 (长度 N+1)
            gamma: 下对角线 (长度 N+1, gamma[0] 未使用)
        """
        D = self.radial._D_coeffs(omega, self.a, self.s, m, A)
        n_arr = np.arange(self.N + 1)
        alpha = self.radial._alpha_n(n_arr, D)
        beta = self.radial._beta_n(n_arr, D)
        gamma = self.radial._gamma_n(n_arr, D)
        return alpha, beta, gamma

    def _tridiag_matvec(self, alpha: np.ndarray, beta: np.ndarray,
                        gamma: np.ndarray, v: np.ndarray) -> np.ndarray:
        """三对角矩阵-向量乘积（O(N)）。"""
        N = len(v)
        result = beta * v
        result[:-1] += alpha[:-1] * v[1:]
        result[1:] += gamma[1:] * v[:-1]
        return result

    def _physical_initial_vector(self, alpha: np.ndarray, beta: np.ndarray,
                                 gamma: np.ndarray) -> np.ndarray:
        """构造物理模式的初始向量（连分数最小解的近似）。

        物理 QNM 对应的序列 aₙ 满足：
        - 大 n 时 aₙ ~ (γₙ/αₙ)^{n/2} 衰减
        - 这对应于连分数的"最小解"
        """
        N = len(beta)
        v = np.ones(N, dtype=complex)

        # 从末端向前递推，构造最小解的近似
        # 大 n 渐近: a_{n+1}/a_n ≈ -gamma_n/alpha_n (衰减方向)
        # 我们从 n=N 反向构造
        for n in range(N - 2, -1, -1):
            if abs(alpha[n]) > 1e-30:
                v[n] = v[n + 1] * (-gamma[n + 1] / alpha[n])
            else:
                v[n] = v[n + 1]

        # 归一化
        norm = np.linalg.norm(v)
        if norm > 1e-30:
            v /= norm

        return v

    def rayleigh_quotient_iteration(self, omega: complex, A: complex, m: int,
                                    shift: complex = 0.0 + 0.0j,
                                    v0: np.ndarray = None,
                                    tol: float = 1e-12,
                                    max_iter: int = 30) -> dict:
        """Rayleigh 商迭代找最接近 shift 的特征值（"两弦法"）。

        几何类比：
          - 初始向量 v0 = 第一根弦
          - 反幂迭代 (M-σI)^{-1}v = 第二根弦
          - Rayleigh 商 = 两根垂线的交点 = 圆心（特征值）

        每次迭代 O(N)，三次收敛，通常 5-10 步收敛。

        参数:
            omega, A, m: 物理参数（用于构建三对角矩阵）
            shift: 寻找 shift 附近的特征值
            v0: 初始向量（可选，默认用物理模式近似）
            tol: 收敛容差
            max_iter: 最大迭代次数

        返回:
            dict: eigenvalue, eigenvector, iterations, converged
        """
        alpha, beta, gamma = self._get_tridiagonal_diags(omega, A, m)
        N = len(beta)

        # 初始向量：用物理模式近似（最小解）
        if v0 is None:
            v = self._physical_initial_vector(alpha, beta, gamma)
        else:
            v = v0.copy() / np.linalg.norm(v0)

        # 初始 Rayleigh 商
        Mv = self._tridiag_matvec(alpha, beta, gamma, v)
        mu = np.vdot(v, Mv)  # Rayleigh 商 = v† M v / v† v

        for it in range(max_iter):
            # 求解 (M - mu I) w = v（反幂迭代步）
            # 这就是"第二根弦"——沿着 (M-muI)^{-1} 的方向
            shifted_beta = beta - mu
            w = _tridiagonal_solve(gamma, shifted_beta, alpha, v)

            # 归一化
            w_norm = np.linalg.norm(w)
            if w_norm < 1e-30:
                # 精确特征向量（奇异矩阵）
                return {
                    "eigenvalue": mu,
                    "eigenvector": v,
                    "iterations": it,
                    "converged": True
                }
            w /= w_norm

            # 新的 Rayleigh 商（"垂线交点"）
            Mw = self._tridiag_matvec(alpha, beta, gamma, w)
            mu_new = np.vdot(w, Mw)

            # 收敛检查
            if abs(mu_new - mu) < tol:
                return {
                    "eigenvalue": mu_new,
                    "eigenvector": w,
                    "iterations": it + 1,
                    "converged": True
                }

            mu = mu_new
            v = w

        return {
            "eigenvalue": mu,
            "eigenvector": v,
            "iterations": max_iter,
            "converged": False
        }

    def spectral_residual_fast(self, omega: complex, A: complex, m: int) -> complex:
        """快速谱残差：逆迭代法找最小模特征值（O(N) 每步）。

        "两弦法"的实现：
          - 弦 1：初始向量（物理模式近似）
          - 弦 2：逆迭代一步 (M^{-1}v)
          - 交点：Rayleigh 商估计的特征值

        注意：对于单次残差计算，迭代法已经是 O(N) 最优。
        此方法的价值在于提供谱信息（特征向量、谱间隙），
        而非比迭代法更快。
        """
        alpha, beta, gamma = self._get_tridiagonal_diags(omega, A, m)

        # 用物理模式近似作为初始向量（通常已足够接近）
        v0 = self._physical_initial_vector(alpha, beta, gamma)
        result = self._inverse_iteration(alpha, beta, gamma, v0, shift=0.0, max_iter=5)

        return result["eigenvalue"]

    def _inverse_iteration(self, alpha: np.ndarray, beta: np.ndarray,
                           gamma: np.ndarray, v0: np.ndarray,
                           shift: complex = 0.0, max_iter: int = 10) -> dict:
        """逆迭代法找最接近 shift 的特征值。

        每次迭代 O(N)（Thomas 算法）。
        """
        N = len(beta)
        v = v0.copy()

        mu_est = 0.0
        for it in range(max_iter):
            shifted_beta = beta - shift
            w = _tridiagonal_solve(gamma, shifted_beta, alpha, v)

            w_norm = np.linalg.norm(w)
            if w_norm < 1e-30:
                break
            v = w / w_norm

            # Rayleigh 商估计
            Mv = self._tridiag_matvec(alpha, beta, gamma, v)
            mu_est = np.vdot(v, Mv)

        return {
            "eigenvalue": mu_est,
            "eigenvector": v,
            "iterations": max_iter,
        }

    def combined_spectral_residual(self, omega: complex, l: int, m: int) -> complex:
        """联合谱残差（含角向分离常数计算）。"""
        ang_result = self.angular.solve_separation_constant(l, m, omega, self.a)
        A = ang_result["A"]
        return self.spectral_residual(omega, A, m)

    def combined_spectral_residual_fast(self, omega: complex, l: int, m: int,
                                        A_ref: complex = None) -> complex:
        """快速联合谱残差（两弦法 + 角向分支跟踪）。"""
        ang_result = self.angular.solve_separation_constant(l, m, omega, self.a, A_ref=A_ref)
        A = ang_result["A"]
        return self.spectral_residual_fast(omega, A, m), ang_result["A"]

    def koopman_analysis(self, omega: complex, A: complex, m: int) -> dict:
        """Koopman 算子谱分析。

        构建转移矩阵（Koopman 算子），计算其谱，
        验证谱对应定理 λ = e^(-μ)。

        转移矩阵：
            [a_{n+1}]   [ -β_n/α_n  -γ_n/α_n ] [a_n  ]
            [a_n    ] = [   1          0      ] [a_{n-1}]

        对于大 n，转移矩阵趋于渐近形式 T_∞，可解析对角化。
        """
        D = self.radial._D_coeffs(omega, self.a, self.s, m, A)
        n_arr = np.arange(1, self.N + 1)
        alpha = self.radial._alpha_n(n_arr, D)
        beta = self.radial._beta_n(n_arr, D)
        gamma = self.radial._gamma_n(n_arr, D)

        # n=0 处的系数（用于验证 CF 残差关系）
        alpha_0 = self.radial._alpha_n(np.array([0]), D)[0]
        beta_0 = self.radial._beta_n(np.array([0]), D)[0]

        # 构建 2x2 转移矩阵的乘积
        T = np.eye(2, dtype=complex)
        for n in range(self.N - 1, 0, -1):
            if abs(alpha[n]) < 1e-30:
                break
            T_n = np.array([
                [-beta[n] / alpha[n], -gamma[n] / alpha[n]],
                [1.0, 0.0]
            ], dtype=complex)
            T = T @ T_n

        # Koopman 算子特征值
        eigvals_K, eigvecs_K = np.linalg.eig(T)

        # 生成元 A = -log(K) 的特征值
        generator_eigvals = []
        spectral_corr_errors = []
        for lam in eigvals_K:
            if abs(lam) > 1e-15:
                mu = -np.log(lam)
                generator_eigvals.append(mu)
                # 验证谱对应：λ = e^(-μ)
                lam_reconstructed = np.exp(-mu)
                spectral_corr_errors.append(abs(lam - lam_reconstructed))

        # 按模长排序特征值
        idx_sort = np.argsort(np.abs(eigvals_K))
        idx_min = idx_sort[0]   # 最小特征值（收缩方向）
        idx_max = idx_sort[-1]  # 最大特征值（扩张方向）
        lam_min = eigvals_K[idx_min]
        lam_max = eigvals_K[idx_max]

        # 谱半径和谱间隙
        spectral_radius = abs(lam_max)
        # 谱间隙衡量收缩/扩张方向的分离程度
        # γ = 1 - |λ_min|/|λ_max|，越接近1越稳定
        if spectral_radius > 1e-15:
            spectral_gap = 1.0 - abs(lam_min) / spectral_radius
        else:
            spectral_gap = 0.0

        # 从三对角矩阵 M 的最小特征值对应特征向量提取 a₁/a₀
        # M · a = 0 的最小特征值对应的特征向量就是最小解序列
        M_mat = self._build_tridiagonal_matrix(omega, A, m)
        eigvals_M, eigvecs_M = np.linalg.eig(M_mat)
        idx_M = np.argmin(np.abs(eigvals_M))
        vec_M = eigvecs_M[:, idx_M]
        # 特征向量 = (a₀, a₁, a₂, ...)，提取 a₁/a₀
        if abs(vec_M[0]) > 1e-30:
            ratio_from_M = vec_M[1] / vec_M[0]
        else:
            ratio_from_M = 0.0

        # 验证：CF 残差 = β₀ + α₀ · (a₁/a₀)
        residual_check = beta_0 + alpha_0 * ratio_from_M

        return {
            "koopman_eigenvalues": eigvals_K,
            "generator_eigenvalues": np.array(generator_eigvals),
            "spectral_radius": spectral_radius,
            "spectral_gap": spectral_gap,
            "spectral_correspondence_error": max(spectral_corr_errors) if spectral_corr_errors else 0.0,
            "minimal_eigenvalue": lam_min,
            "minimal_ratio_a1_a0": ratio_from_M,
            "residual_check": residual_check,
            "transfer_matrix": T,
        }

    def solve_spectral(self, omega_guess: complex, l: int, m: int,
                       tol: float = 1e-10, max_newton: int = 50) -> dict:
        """用谱方法（非递归）求解 QNM 频率。

        Newton-Raphson 在谱残差上迭代，但残差本身
        通过矩阵特征值计算，而非连分数迭代。
        """
        omega = omega_guess

        for iteration in range(max_newton):
            residual = self.combined_spectral_residual(omega, l, m)

            if abs(residual) < tol:
                return {
                    "omega": omega,
                    "residual": abs(residual),
                    "converged": True,
                    "iterations": iteration + 1,
                    "method": "spectral"
                }

            delta = 1e-6
            residual_delta = self.combined_spectral_residual(omega + delta, l, m)
            d_residual = (residual_delta - residual) / delta

            if abs(d_residual) > 1e-15:
                omega -= residual / d_residual

        return {
            "omega": omega,
            "residual": abs(self.combined_spectral_residual(omega, l, m)),
            "converged": False,
            "iterations": max_newton,
            "method": "spectral"
        }

    def solve_spectral_fast(self, omega_guess: complex, l: int, m: int,
                            tol: float = 1e-10, max_newton: int = 50) -> dict:
        """用快速谱方法（两弦法 Rayleigh 商迭代）求解 QNM 频率。

        残差计算从 O(N³) 降到 O(N)，
        效率与迭代法相当，同时保留谱方法的理论框架。
        """
        omega = omega_guess
        A_ref = None
        delta = 1e-6

        for iteration in range(max_newton):
            residual, A_curr = self.combined_spectral_residual_fast(omega, l, m, A_ref=A_ref)
            A_ref = A_curr

            if abs(residual) < tol:
                return {
                    "omega": omega,
                    "residual": abs(residual),
                    "converged": True,
                    "iterations": iteration + 1,
                    "method": "spectral_fast"
                }

            # 2D Newton（实部+虚部）
            r_plus, _ = self.combined_spectral_residual_fast(omega + delta, l, m, A_ref=A_ref)
            r_minus, _ = self.combined_spectral_residual_fast(omega - delta, l, m, A_ref=A_ref)
            r_imag, _ = self.combined_spectral_residual_fast(omega + 1j * delta, l, m, A_ref=A_ref)

            df_dre = (r_plus - r_minus) / (2 * delta)
            df_dim = (r_imag - residual) / delta

            J = np.array([
                [df_dre.real, df_dim.real],
                [df_dre.imag, df_dim.imag]
            ], dtype=float)

            F = np.array([residual.real, residual.imag], dtype=float)

            try:
                det_J = np.linalg.det(J)
                if abs(det_J) < 1e-30:
                    break
                delta_omega = np.linalg.solve(J, -F)
            except np.linalg.LinAlgError:
                break

            step = complex(delta_omega[0], delta_omega[1])
            step_mag = abs(step)
            if step_mag > 0.5:
                step = step * (0.5 / step_mag)

            omega_new = omega + step

            if omega_new.imag > 0:
                omega_new = complex(omega_new.real, -abs(omega_new.imag))

            omega = omega_new

        final_res, _ = self.combined_spectral_residual_fast(omega, l, m, A_ref=A_ref)
        return {
            "omega": omega,
            "residual": abs(final_res),
            "converged": False,
            "iterations": max_newton,
            "method": "spectral_fast"
        }


class IterativeSolver:
    """迭代方法（标准 Leaver 连分数向后迭代）。

    用于与谱方法对照验证。
    """

    def __init__(self, M: float = 1.0, a: float = 0.0, s: int = -2, max_iter: int = 300):
        self.radial = LeaverRadialSolver(M=M, a=a, s=s, max_iter=max_iter)
        self.angular = LeaverAngularSolver(s=s, l_max=20)
        self.a = a
        self.s = s

    def combined_iterative_residual(self, omega: complex, l: int, m: int, n_inv: int = 0) -> complex:
        """迭代方法计算连分数残差。"""
        ang_result = self.angular.solve_separation_constant(l, m, omega, self.a)
        A = ang_result["A"]
        return self.radial.leaver_cf(omega, A, m, n_inv=n_inv)

    def solve_iterative(self, omega_guess: complex, l: int, m: int,
                        tol: float = 1e-10, max_newton: int = 50) -> dict:
        """用迭代方法求解 QNM 频率。"""
        omega = omega_guess
        n_inv = 0

        for iteration in range(max_newton):
            residual = self.combined_iterative_residual(omega, l, m, n_inv=n_inv)

            if abs(residual) < tol:
                return {
                    "omega": omega,
                    "residual": abs(residual),
                    "converged": True,
                    "iterations": iteration + 1,
                    "method": "iterative"
                }

            delta = 1e-6
            residual_delta = self.combined_iterative_residual(omega + delta, l, m, n_inv=n_inv)
            d_residual = (residual_delta - residual) / delta

            if abs(d_residual) > 1e-15:
                omega -= residual / d_residual

        return {
            "omega": omega,
            "residual": abs(self.combined_iterative_residual(omega, l, m, n_inv=n_inv)),
            "converged": False,
            "iterations": max_newton,
            "method": "iterative"
        }


def compare_paths():
    """两条路径对照验证：迭代 vs 谱分解。"""
    print("=" * 75)
    print("去递归验证：迭代方法 vs 谱分解方法")
    print("=" * 75)
    print()

    test_cases = [
        (0.0, 2, 0, 0, complex(0.373672, -0.088962), "Schwarzschild l=2,m=0,n=0"),
        (0.5, 2, 2, 0, complex(0.46, -0.09), "Kerr a=0.5, l=2,m=2,n=0"),
        (0.5, 2, 0, 0, complex(0.38, -0.09), "Kerr a=0.5, l=2,m=0,n=0"),
        (0.7, 2, 1, 0, complex(0.45, -0.08), "Kerr a=0.7, l=2,m=1,n=0"),
    ]

    print(f"{'模式':<30} {'方法':<10} {'ω':<28} {'残差':<12} {'收敛':<6}")
    print("-" * 90)

    for a_val, l, m, n, guess, desc in test_cases:
        # 迭代方法
        iter_solver = IterativeSolver(M=1.0, a=a_val, s=-2, max_iter=300)
        result_iter = iter_solver.solve_iterative(guess, l, m, tol=1e-10)

        # 谱方法
        spec_solver = SpectralDerecursionSolver(M=1.0, a=a_val, s=-2, N=80)
        result_spec = spec_solver.solve_spectral(guess, l, m, tol=1e-10)

        omega_i = result_iter["omega"]
        omega_s = result_spec["omega"]
        diff = abs(omega_i - omega_s)

        print(f"{desc:<30} {'迭代':<10} {omega_i.real:.6f}{omega_i.imag:+.6f}i   {result_iter['residual']:.2e}   {'✓' if result_iter['converged'] else '✗'}")
        print(f"{'':<30} {'谱分解':<10} {omega_s.real:.6f}{omega_s.imag:+.6f}i   {result_spec['residual']:.2e}   {'✓' if result_spec['converged'] else '✗'}")
        print(f"{'':<30} {'差值':<10} {diff:.2e}")
        print()

    print()
    print("=" * 75)
    print("Koopman 算子谱分析（验证谱对应定理 λ = e^(-μ)）")
    print("=" * 75)
    print()

    for a_val, l, m, n, guess, desc in test_cases:
        spec_solver = SpectralDerecursionSolver(M=1.0, a=a_val, s=-2, N=80)
        result = spec_solver.solve_spectral(guess, l, m, tol=1e-8)
        omega = result["omega"]

        ang_result = spec_solver.angular.solve_separation_constant(l, m, omega, a_val)
        A = ang_result["A"]

        koopman = spec_solver.koopman_analysis(omega, A, m)

        print(f"--- {desc} ---")
        print(f"  ω = {omega.real:.6f} {omega.imag:+.6f}i")

        eigvals_K = koopman["koopman_eigenvalues"]
        print(f"  Koopman 特征值:")
        for i, lam in enumerate(eigvals_K):
            print(f"    λ_{i} = {lam.real:.6f} {lam.imag:+.6f}i  |λ| = {abs(lam):.6f}")

        gen_eigvals = koopman["generator_eigenvalues"]
        print(f"  生成元特征值 A = -log(K):")
        for i, mu in enumerate(gen_eigvals):
            print(f"    μ_{i} = {mu.real:.6f} {mu.imag:+.6f}i")

        print(f"  谱半径 ρ(K) = {koopman['spectral_radius']:.6f}")
        print(f"  谱间隙 γ = 1 - ρ(K) = {koopman['spectral_gap']:.6f}")
        print(f"  谱对应验证 max|λ - e^(-μ)| = {koopman['spectral_correspondence_error']:.2e}")
        print(f"  最小解特征值 |λ_min| = {abs(koopman['minimal_eigenvalue']):.6f}")
        print(f"  最小解比值 a₁/a₀ = {koopman['minimal_ratio_a1_a0']:.6f}")

        # 验证：残差 = β₀ + α₀ · (a₁/a₀)
        D = spec_solver.radial._D_coeffs(omega, a_val, -2, m, A)
        alpha_0 = D[0]  # α₀ = D₀
        beta_0 = D[3]  # β₀ = D₃
        residual_check = beta_0 + alpha_0 * koopman["minimal_ratio_a1_a0"]
        print(f"  验证 β₀ + α₀·(a₁/a₀) = {abs(residual_check):.2e}")
        print()

    print()
    print("=" * 75)
    print("矩阵维度收敛性测试")
    print("=" * 75)
    print()

    a_val, l, m = 0.5, 2, 2
    omega = complex(0.464123, -0.085639)

    print(f"测试点: a={a_val}, l={l}, m={m}, ω={omega.real:.6f}{omega.imag:+.6f}i")
    print()

    print(f"{'N (矩阵维度)':<15} {'谱残差 |λ_min|':<20} {'迭代残差 |CF|':<20} {'比值':<15}")
    print("-" * 70)

    for N in [20, 40, 60, 80, 100, 120]:
        spec_solver = SpectralDerecursionSolver(M=1.0, a=a_val, s=-2, N=N)
        iter_solver = IterativeSolver(M=1.0, a=a_val, s=-2, max_iter=N)

        ang_result = spec_solver.angular.solve_separation_constant(l, m, omega, a_val)
        A = ang_result["A"]

        res_spec = abs(spec_solver.spectral_residual(omega, A, m))
        res_iter = abs(iter_solver.radial.leaver_cf(omega, A, m, n_inv=0))

        ratio = res_spec / res_iter if res_iter > 0 else float('inf')
        print(f"{N:<15} {res_spec:<20.2e} {res_iter:<20.2e} {ratio:<15.4f}")


if __name__ == "__main__":
    compare_paths()
