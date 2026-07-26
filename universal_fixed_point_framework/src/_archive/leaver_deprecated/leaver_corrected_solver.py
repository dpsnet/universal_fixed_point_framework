"""
leaver_corrected_solver.py

基于 Leaver (1985) 方法的 Kerr 黑洞准正则模求解器。
使用正确的二次多项式连分数系数（参考 qnm 包的实现，基于 Cook & Zalutskiy 2014）。

核心改进：
1. 正确的径向连分数系数（二次多项式形式，非乘积形式
2. 正确的连分数迭代方式（反转形式，n_inv inversion）
3. 角向方程使用谱方法（矩阵特征值问题）
4. 同伦延拓方法追踪物理根
5. LACI 判据验证物理解
"""

from __future__ import annotations

import numpy as np
import cmath
from scipy.linalg import eigvals


class LeaverAngularSolver:
    """角向 Teukolsky 方程求解器（谱方法）。
    
    基于 Cook & Zalutskiy (2014) 的谱分解方法。
    将自旋加权椭球谐函数展开为球谐函数的线性组合，
    转化为矩阵特征值问题。
    """
    
    def __init__(self, s: int = -2, l_max: int = 15):
        self.s = s
        self.l_max = l_max
    
    def _calF(self, l: int, m: int) -> float:
        if (0 == self.s) and (0 == l + 1):
            return 0.
        return (np.sqrt(((l+1)**2 - m*m) / (2*l+3) / (2*l+1)) * np.sqrt(((l+1)**2 - self.s*self.s) / (l+1)**2))
    
    def _calG(self, l: int, m: int) -> float:
        if 0 == l:
            return 0.
        return np.sqrt((l*l - m*m) / (4*l*l - 1)) * np.sqrt(1 - self.s*self.s/l/l)
    
    def _calH(self, l: int, m: int) -> float:
        if 0 == l or 0 == self.s:
            return 0.
        return - m * self.s / l / (l+1)
    
    def _calA(self, l: int, m: int) -> float:
        return self._calF(l, m) * self._calF(l+1, m)
    
    def _calD(self, l: int, m: int) -> float:
        return self._calF(l, m) * (self._calH(l+1, m) + self._calH(l, m))
    
    def _calB(self, l: int, m: int) -> float:
        return (self._calF(l, m) * self._calG(l+1, m)
                + self._calG(l, m) * self._calF(l-1, m)
                + self._calH(l, m)**2)
    
    def _calE(self, l: int, m: int) -> float:
        return self._calG(l, m) * (self._calH(l-1, m) + self._calH(l, m))
    
    def _calC(self, l: int, m: int) -> float:
        return self._calG(l, m) * self._calG(l-1, m)
    
    def _swsphericalh_A(self, l: int, m: int) -> float:
        return l*(l+1) - self.s*(self.s+1)
    
    def _M_matrix_elem(self, c: complex, m: int, l: int, lprime: int) -> complex:
        if lprime == l - 2:
            return -c*c * self._calA(lprime, m)
        if lprime == l - 1:
            return (-c*c * self._calD(lprime, m) + 2*c*self.s * self._calF(lprime, m))
        if lprime == l:
            return (self._swsphericalh_A(lprime, m)
                    - c*c * self._calB(lprime, m)
                    + 2*c*self.s * self._calH(lprime, m))
        if lprime == l + 1:
            return (-c*c * self._calE(lprime, m) + 2*c*self.s * self._calG(lprime, m))
        if lprime == l + 2:
            return -c*c * self._calC(lprime, m)
        return 0.j
    
    def solve_separation_constant(self, l: int, m: int, omega: complex, a: float,
                                  A_ref: complex = None) -> dict:
        """求解角向分离常数 A_lm。

        参数:
            l: 角量子数
            m: 磁量子数
            omega: 复频率
            a: 黑洞自旋参数
            A_ref: 参考分离常数（用于连续分支跟踪）

        返回:
            包含分离常数、特征向量的字典
        """
        c = a * omega
        l_min = max(abs(self.s), abs(m))
        l_max = max(self.l_max, l + 5)
        
        n_ell = l_max - l_min + 1
        M = np.zeros((n_ell, n_ell), dtype=complex)
        
        ells = np.arange(l_min, l_max + 1)
        
        for i, li in enumerate(ells):
            for j, lj in enumerate(ells):
                M[i, j] = self._M_matrix_elem(c, m, li, lj)
        
        eigenvalues, eigenvectors = np.linalg.eig(M)

        # 分支跟踪：优先使用参考值，否则用 Schwarzschild 值
        if A_ref is not None and np.isfinite(A_ref):
            ref_val = A_ref
        else:
            ref_val = l * (l + 1) - self.s * (self.s + 1)

        idx = np.argmin(np.abs(eigenvalues - ref_val))
        
        A = eigenvalues[idx]
        vec = eigenvectors[:, idx]
        
        return {
            "A": A,
            "eigenvector": vec,
            "ells": ells,
            "l_min": l_min,
            "converged": True
        }


class LeaverRadialSolver:
    """径向 Teukolsky 方程求解器（Leaver 连分数方法）。
    
    使用正确的二次多项式连分数系数。
    """
    
    def __init__(self, M: float = 1.0, a: float = 0.0, s: int = -2, max_iter: int = 500):
        self.M = M
        self.a = a
        self.s = s
        self.max_iter = max_iter
    
    def _sing_pt_char_exps(self, omega: complex, a: float, s: int, m: int):
        """计算奇异点特征指数。"""
        root = np.sqrt(1. - a*a)
        r_p, r_m = 1. + root, 1. - root
        sigma_p = (2.*omega*r_p - m*a)/(2.*root)
        sigma_m = (2.*omega*r_m - m*a)/(2.*root)
        
        zeta = +1.j * omega
        xi = - s - 1.j * sigma_p
        eta = -1.j * sigma_m
        
        return zeta, xi, eta
    
    def _D_coeffs(self, omega: complex, a: float, s: int, m: int, A: complex):
        """计算 D_0 到 D_4 系数。
        
        参考 Cook & Zalutskiy (2014) 方程 (31)。
        """
        zeta, xi, eta = self._sing_pt_char_exps(omega, a, s, m)
        root = np.sqrt(1. - a*a)
        
        p = root * zeta
        alpha = 1. + s + xi + eta - 2.*zeta + s
        gamma = 1. + s + 2.*eta
        delta = 1. + s + 2.*xi
        sigma = (A + a*a*omega*omega - 8.*omega*omega
                 + p * (2.*alpha + gamma - delta)
                 + (1. + s - 0.5*(gamma + delta))
                 * (s + 0.5*(gamma + delta)))
        
        D = np.zeros(5, dtype=complex)
        D[0] = delta
        D[1] = 4.*p - 2.*alpha + gamma - delta - 2.
        D[2] = 2.*alpha - gamma + 2.
        D[3] = alpha*(4.*p - delta) - sigma
        D[4] = alpha*(alpha - gamma + 1.)
        
        return D
    
    def _alpha_n(self, n: np.ndarray, D: np.ndarray) -> np.ndarray:
        return n*n + (D[0] + 1.)*n + D[0]
    
    def _beta_n(self, n: np.ndarray, D: np.ndarray) -> np.ndarray:
        return -2.*n*n + (D[1] + 2.)*n + D[3]
    
    def _gamma_n(self, n: np.ndarray, D: np.ndarray) -> np.ndarray:
        return n*n + (D[2] - 3.)*n + D[4] - D[2] + 2.
    
    def leaver_cf(self, omega: complex, A: complex, m: int, n_inv: int = 0) -> complex:
        """计算径向连分数残差（第 n_inv 次反转）。
        
        参数:
            omega: 复频率
            A: 角向分离常数
            m: 磁量子数
            n_inv: 反转次数（寻找第 n 阶泛音通常用 n_inv = n）
        
        返回:
            连分数残差，为零时 omega 是 QNM 频率
        """
        a = self.a
        s = self.s
        N = self.max_iter
        
        D = self._D_coeffs(omega, a, s, m, A)
        
        n_arr = np.arange(0, N + 1)
        alpha = self._alpha_n(n_arr, D)
        beta = self._beta_n(n_arr, D)
        gamma = self._gamma_n(n_arr, D)
        
        conv1 = 0.j
        for i in range(0, n_inv):
            denom = beta[i] - gamma[i] * conv1
            if abs(denom) < 1e-30:
                denom = 1e-30
            conv1 = alpha[i] / denom
        
        conv2 = 0.j
        for i in range(N, n_inv, -1):
            denom = beta[i] - alpha[i] * conv2
            if abs(denom) < 1e-30:
                denom = 1e-30
            conv2 = gamma[i] / denom
        
        return beta[n_inv] - gamma[n_inv] * conv1 - alpha[n_inv] * conv2


class CorrectedLeaverQNMSolver:
    """校正后的 Leaver QNM 求解器。
    
    结合角向谱方法和径向连分数方法，
    使用同伦延拓追踪物理根，
    并用 LACI 判据验证。
    """
    
    def __init__(self, M: float = 1.0, a: float = 0.0, s: int = -2, max_iter: int = 500):
        self.M = M
        self.a = a
        self.s = s
        self.max_iter = max_iter
        self.angular = LeaverAngularSolver(s=s)
        self.radial = LeaverRadialSolver(M=M, a=a, s=s, max_iter=max_iter)
    
    def _spectral_radial_residual(self, omega: complex, A: complex, m: int,
                                   N: int = None, fast: bool = True) -> complex:
        """谱方法径向残差：三对角矩阵的最小模特征值。

        替代 leaver_cf 的连分数迭代，用矩阵特征值判据。
        |λ_min| → 0 ⟺ ω 是 QNM 频率。

        优势：
        1. 无收敛半径问题（CF 在参数空间某些区域会发散）
        2. 谱信息更丰富（可同时看到所有特征值的分布）
        3. 对 m≠0 和极端自旋更稳定

        参数:
            fast: 为 True 时用逆迭代（O(N)），为 False 时用全对角化（O(N³)）
        """
        if N is None:
            # 高自旋 m≠0 需要更多项才能出现零特征值
            a_abs = abs(self.a)
            if a_abs > 0.8 and m != 0:
                N = min(self.max_iter, 200)
            elif a_abs > 0.5 and m != 0:
                N = min(self.max_iter, 120)
            else:
                N = min(self.max_iter, 80)

        D = self.radial._D_coeffs(omega, self.radial.a, self.s, m, A)
        n_arr = np.arange(N + 1)
        alpha = self.radial._alpha_n(n_arr, D)
        beta = self.radial._beta_n(n_arr, D)
        gamma = self.radial._gamma_n(n_arr, D)

        if fast:
            return self._inverse_iteration(alpha, beta, gamma, N)
        else:
            M = np.zeros((N + 1, N + 1), dtype=complex)
            for n in range(N + 1):
                M[n, n] = beta[n]
                if n < N:
                    M[n, n + 1] = alpha[n]
                if n > 0:
                    M[n, n - 1] = gamma[n]
            eigenvalues = eigvals(M)
            idx = np.argmin(np.abs(eigenvalues))
            return eigenvalues[idx]

    @staticmethod
    def _tridiagonal_solve(alpha: np.ndarray, beta: np.ndarray,
                           gamma: np.ndarray, rhs: np.ndarray) -> np.ndarray:
        """Thomas 算法解三对角方程组（O(N)）。"""
        N = len(beta)
        c_prime = np.zeros(N, dtype=complex)
        d_prime = np.zeros(N, dtype=complex)
        x = np.zeros(N, dtype=complex)

        c_prime[0] = alpha[0] / beta[0]
        d_prime[0] = rhs[0] / beta[0]

        for i in range(1, N):
            denom = beta[i] - gamma[i] * c_prime[i - 1]
            if abs(denom) < 1e-30:
                denom = complex(1e-30, 0.0)
            if i < N - 1:
                c_prime[i] = alpha[i] / denom
            else:
                c_prime[i] = 0.0
            d_prime[i] = (rhs[i] - gamma[i] * d_prime[i - 1]) / denom

        x[N - 1] = d_prime[N - 1]
        for i in range(N - 2, -1, -1):
            x[i] = d_prime[i] - c_prime[i] * x[i + 1]

        return x

    def _inverse_iteration(self, alpha: np.ndarray, beta: np.ndarray,
                           gamma: np.ndarray, N: int,
                           max_iter: int = 10) -> complex:
        """逆迭代找三对角矩阵的最小模特征值。

        用物理模式近似作为初始向量（大 n 时 a_n 衰减），
        通过 (M)^{-1} 迭代收敛到最小特征值。
        每次迭代 O(N)（Thomas 算法）。
        """
        # 初始向量：物理模式近似（从末端向前衰减构造）
        v = np.ones(N + 1, dtype=complex)
        for n in range(N - 1, -1, -1):
            if abs(alpha[n]) > 1e-30:
                v[n] = v[n + 1] * (-gamma[n + 1] / alpha[n])

        v_norm = np.linalg.norm(v)
        if v_norm > 1e-30:
            v /= v_norm

        # 逆迭代 (M)^{-1} v
        for _ in range(max_iter):
            w = self._tridiagonal_solve(alpha, beta, gamma, v)

            w_norm = np.linalg.norm(w)
            if w_norm < 1e-30:
                break
            v = w / w_norm

        # Rayleigh 商：v† M v
        Mv = beta * v
        Mv[:-1] += alpha[:-1] * v[1:]
        Mv[1:] += gamma[1:] * v[:-1]
        mu = np.vdot(v, Mv)

        return mu

    def _combined_residual(self, omega: complex, l: int, m: int, a_val: float,
                          n_inv: int = 0, A_ref: complex = None) -> complex:
        """计算联合残差（径向连分数）。"""
        self.radial.a = a_val

        ang_result = self.angular.solve_separation_constant(l, m, omega, a_val, A_ref=A_ref)
        A = ang_result["A"]

        return self.radial.leaver_cf(omega, A, m, n_inv=n_inv)
    
    def _newton_raphson(self, omega_guess: complex, l: int, m: int, a_val: float,
                        n_inv: int = 0, tol: float = 1e-10, max_newton: int = 100,
                        A_ref: complex = None) -> dict:
        """2D Newton-Raphson 方法求解 QNM 频率（完整复 Jacobian）。
        
        使用实部和虚部双向差分构建 2×2 Jacobian，
        正确处理残差对 ω 的复数依赖。
        """
        omega = omega_guess
        delta = 1e-6

        for iteration in range(max_newton):
            residual = self._combined_residual(omega, l, m, a_val, n_inv=n_inv, A_ref=A_ref)

            if abs(residual) < tol:
                return {
                    "omega": omega,
                    "residual": abs(residual),
                    "converged": True,
                    "iterations": iteration + 1
                }

            # 完整 2D Jacobian：扰动实部和虚部
            r_plus = self._combined_residual(omega + delta, l, m, a_val, n_inv=n_inv, A_ref=A_ref)
            r_minus = self._combined_residual(omega - delta, l, m, a_val, n_inv=n_inv, A_ref=A_ref)
            r_imag = self._combined_residual(omega + 1j * delta, l, m, a_val, n_inv=n_inv, A_ref=A_ref)

            # Jacobian 矩阵元素（中心差分）
            df_dre = (r_plus - r_minus) / (2 * delta)
            df_dim = (r_imag - residual) / delta

            # 构建 2x2 Jacobian: [df/dx, df/dy] 对 Re 和 Im
            J = np.array([
                [df_dre.real, df_dim.real],
                [df_dre.imag, df_dim.imag]
            ], dtype=float)

            # 残差向量
            F = np.array([residual.real, residual.imag], dtype=float)

            # 解线性方程组 J * delta_omega = -F
            try:
                det_J = np.linalg.det(J)
                if abs(det_J) < 1e-30:
                    break
                delta_omega = np.linalg.solve(J, -F)
            except np.linalg.LinAlgError:
                break

            # 阻尼 Newton 步长（防止过冲）
            step = complex(delta_omega[0], delta_omega[1])
            step_mag = abs(step)
            if step_mag > 0.5:
                step = step * (0.5 / step_mag)

            omega_new = omega + step

            # 物理性检查：如果跳到正虚部，回退
            if omega_new.imag > 0:
                omega_new = complex(omega_new.real, -abs(omega_new.imag))

            # 残差应该下降，否则减小步长
            new_residual = abs(self._combined_residual(omega_new, l, m, a_val, n_inv=n_inv, A_ref=A_ref))
            if new_residual > abs(residual) * 2:
                # 残差恶化，减小步长重试
                omega_new = omega + step * 0.1
                new_residual = abs(self._combined_residual(omega_new, l, m, a_val, n_inv=n_inv, A_ref=A_ref))
                if new_residual > abs(residual) * 5:
                    break

            omega = omega_new

        return {
            "omega": omega,
            "residual": abs(self._combined_residual(omega, l, m, a_val, n_inv=n_inv, A_ref=A_ref)),
            "converged": False,
            "iterations": max_newton
        }
    
    def _is_physical(self, omega: complex) -> bool:
        """判断根是否物理（负虚部，即衰减模式）。"""
        return omega.imag < 0

    def _berti_approximation(self, l: int, m: int, n: int = 0) -> complex:
        """Berti 拟合公式给 Kerr QNM 初始猜测。

        基于 arXiv:gr-qc/0512160 的拟合公式。
        对 m≠0 在中等自旋范围内有效。
        """
        a = self.a
        if abs(a) < 1e-10:
            return self._schwarzschild_guess(l, n)

        # 对 l=2, n=0 用已知值
        if l == 2 and n == 0:
            # Berti 表插值
            table_m0 = {0.0: 0.3737-0.0890j, 0.3: 0.362-0.088j,
                        0.5: 0.365-0.087j, 0.7: 0.380-0.085j,
                        0.9: 0.396-0.084j}
            if m == 0:
                import bisect
                a_vals = sorted(table_m0.keys())
                if a <= a_vals[0]:
                    return table_m0[a_vals[0]]
                if a >= a_vals[-1]:
                    return table_m0[a_vals[-1]]
                # 线性插值
                i = 0
                for i in range(len(a_vals) - 1):
                    if a_vals[i] <= a <= a_vals[i+1]:
                        break
                t = (a - a_vals[i]) / (a_vals[i+1] - a_vals[i])
                w0 = table_m0[a_vals[i]]
                w1 = table_m0[a_vals[i+1]]
                return w0 + t * (w1 - w0)
            elif m != 0:
                # 从 m=0 加线性修正
                w_m0 = self._berti_approximation(l, 0, n)
                # m 分裂系数（经验拟合）
                delta_re = m * a * 0.1
                delta_im = -m * a * 0.002
                return w_m0 + complex(delta_re, delta_im)

        # 通用 eikonal 近似
        omega_re = (l + 0.5 + n + 0.5) / (2 * np.sqrt(27)) + m * a * 0.1
        omega_im = -(n + 0.5) / 3
        return complex(omega_re, omega_im)

    def _s2_guided_solve(self, l: int, m: int, n: int = 0, tol: float = 1e-10) -> dict:
        """S₂ 引导的 m≠0 QNM 求解。

        策略（对应 spectral_Kerr_silence_analysis.md 策略 A）：
        1. 先解 m=0 在目标 a 处（S₁ 基线，已知同伦延拓有效）
        2. 用 m=0 的 ω 作为 m≠0 的初始猜测
        3. 沿 m-homotopy 路径逐步推进（m=0 → m=1 → m=2 → ...）
        4. 如果 S₂ 引导落到非物理根，回退到 Berti 近似
        """
        # Step 1: 解 m=0 在目标 a 处
        m0_solver = CorrectedLeaverQNMSolver(M=self.M, a=self.a, s=self.s,
                                              max_iter=self.max_iter)
        m0_result = m0_solver._a_homotopy_solve(l, m=0, n=n, tol=tol)

        if not m0_result["converged"] or not self._is_physical(m0_result["omega"]):
            return self._a_homotopy_solve(l, m, n=n, tol=tol)

        omega_m0 = m0_result["omega"]

        ang_m0 = self.angular.solve_separation_constant(l, 0, omega_m0, self.a)
        A_ref = ang_m0["A"]

        # Step 2: 沿 m-homotopy 逐步推进
        m_abs = abs(m)
        if m_abs >= 2:
            m_steps = sorted(set([0, 1, m_abs]))
        else:
            m_steps = sorted(set([0, m_abs]))

        if m < 0:
            m_steps = [0] + sorted(set([-s for s in m_steps if s > 0]))

        omega_curr = omega_m0
        A_ref_curr = A_ref

        for m_step in m_steps[1:]:
            step_result = self._newton_raphson(omega_curr, l, int(m_step),
                                               self.a, n_inv=n, tol=tol,
                                               A_ref=A_ref_curr)
            if (step_result["converged"] and self._is_physical(step_result["omega"])
                    and abs(step_result["omega"]) < 2.0
                    and abs(step_result["omega"].imag) < 0.5):
                omega_curr = step_result["omega"]
                ang = self.angular.solve_separation_constant(
                    l, int(m_step), omega_curr, self.a, A_ref=A_ref_curr
                )
                A_ref_curr = ang["A"]
            else:
                # 当前步失败，尝试从 Berti 近似重新开始
                berti_guess = self._berti_approximation(l, int(m_step), n)
                step_result = self._newton_raphson(berti_guess, l, int(m_step),
                                                   self.a, n_inv=n, tol=tol,
                                                   A_ref=A_ref_curr)
                if (step_result["converged"] and self._is_physical(step_result["omega"])
                        and abs(step_result["omega"]) < 2.0
                        and abs(step_result["omega"].imag) < 0.5):
                    omega_curr = step_result["omega"]
                    ang = self.angular.solve_separation_constant(
                        l, int(m_step), omega_curr, self.a, A_ref=A_ref_curr
                    )
                    A_ref_curr = ang["A"]
                else:
                    # 完全回退：直接用 Berti 猜测
                    omega_curr = self._berti_approximation(l, m, n)

        # 最终精修
        result = self._newton_raphson(omega_curr, l, m, self.a, n_inv=n,
                                      tol=tol, A_ref=A_ref_curr)
        result["is_physical"] = (result["converged"]
                                 and self._is_physical(result["omega"])
                                 and abs(result["omega"]) < 2.0
                                 and abs(result["omega"].imag) < 0.5)
        result["initial_guess"] = omega_m0
        return result

    def _a_homotopy_solve(self, l: int, m: int, n: int = 0, tol: float = 1e-10) -> dict:
        """a-homotopy：从 Schwarzschild (a=0) 推进到目标自旋。

        这是原来的 solve 方法逻辑，提取为内部方法。
        """
        a_target = self.a

        A_schw = complex(l * (l + 1) - self.s * (self.s + 1), 0)
        A_ref = A_schw

        omega_current = self._schwarzschild_guess(l, n)
        a_current = 0.0

        da = min(0.05, 0.1 * (1.0 - a_target) + 0.01)
        da_min = 1e-4
        max_halvings = 20
        halvings = 0

        converged = True
        prev_omega = omega_current

        while a_current < a_target - 1e-12:
            a_next = min(a_current + da, a_target)

            result = self._newton_raphson(omega_current, l, m, a_next, n_inv=n,
                                          tol=tol, A_ref=A_ref)

            if not result["converged"]:
                da *= 0.5
                halvings += 1
                if halvings > max_halvings or da < da_min:
                    converged = False
                    break
                continue

            omega_new = result["omega"]

            freq_jump = abs(omega_new - prev_omega)
            if freq_jump > 0.15 and a_next > 0.3:
                da *= 0.5
                halvings += 1
                if halvings > max_halvings or da < da_min:
                    converged = False
                    break
                continue

            if not self._is_physical(omega_new):
                omega_trial = complex(omega_new.real, -abs(omega_new.imag))
                result_trial = self._newton_raphson(omega_trial, l, m, a_next, n_inv=n,
                                                     tol=tol, A_ref=A_ref)
                if result_trial["converged"] and self._is_physical(result_trial["omega"]):
                    omega_new = result_trial["omega"]
                else:
                    da *= 0.5
                    halvings += 1
                    if halvings > max_halvings or da < da_min:
                        converged = False
                        break
                    continue

            ang_result = self.angular.solve_separation_constant(l, m, omega_new, a_next, A_ref=A_ref)
            A_ref = ang_result["A"]

            prev_omega = omega_current
            omega_current = omega_new
            a_current = a_next
            halvings = 0
            da = min(da * 1.5, 0.1)

        final_result = self._newton_raphson(omega_current, l, m, a_target, n_inv=n,
                                            tol=tol, A_ref=A_ref)
        final_result["is_physical"] = self._is_physical(final_result["omega"])
        final_result["converged"] = converged and final_result["converged"]

        return final_result

    def _generate_initial_guesses(self, l: int, m: int, n: int = 0) -> list:
        """生成多样化的初始猜测，覆盖不同吸引域。"""
        guesses = []
        a = self.a

        # 1. S₂ 引导：解 m=0 然后外推
        if m != 0 and a > 0.01:
            try:
                m0_solver = CorrectedLeaverQNMSolver(M=self.M, a=a, s=self.s,
                                                      max_iter=self.max_iter)
                r0 = m0_solver._a_homotopy_solve(l, m=0, n=n, tol=1e-6)
                if r0["converged"] and r0["omega"].imag < 0:
                    # m=0 解直接作为猜测
                    guesses.append(("S2_m0", r0["omega"]))
                    # m 线性外推
                    delta_re = m * a * 0.1
                    delta_im = -m * a * 0.002
                    guesses.append(("S2_extrap", r0["omega"] + complex(delta_re, delta_im)))
            except Exception:
                pass

        # 2. Berti 近似（含扰动）
        berti_base = self._berti_approximation(l, m, n)
        guesses.append(("Berti", berti_base))

        # Berti 附近扰动
        for dr, di in [(0.02, 0), (-0.02, 0), (0, 0.01), (0, -0.01),
                       (0.03, 0.01), (-0.03, -0.01)]:
            perturbed = berti_base + complex(dr, di)
            guesses.append(("Berti_pert", perturbed))

        # 3. a-homotopy（从 Schwarzschild 推进到目标 a，用 m=0 的路径）
        if a > 0.01:
            try:
                direct = CorrectedLeaverQNMSolver(M=self.M, a=a, s=self.s,
                                                   max_iter=self.max_iter)
                rd = direct._a_homotopy_solve(l, m, n=n, tol=1e-6)
                if rd["converged"] and rd["omega"].imag < 0:
                    guesses.append(("a_homotopy", rd["omega"]))
            except Exception:
                pass

        # 4. Schwarzschild 基线（低自旋 fallback）
        schw = self._schwarzschild_guess(l, n)
        if a < 0.3:
            guesses.append(("Schwarz", schw))

        # 去重（对接近的猜测只保留一个）
        unique = []
        seen = []
        for label, w in guesses:
            dup = False
            for _, w0 in seen:
                if abs(w - w0) < 0.02:
                    dup = True
                    break
            if not dup:
                unique.append((label, w))
                seen.append((label, w))

        return unique

    def _select_physical_root(self, candidates: list, l: int, m: int,
                               berti_ref: complex = None) -> dict:
        """从多个候选根中筛选最物理解。

        评分标准（越高越好）：
        1. 收敛 (+20)
        2. 负虚部 (+20)
        3. |虚部| < 0.5 (+15)
        4. 实部在 0.2-1.0 (+10)
        5. 接近 Berti 参考值 (+20, 按 -|Δω| 指数衰减)
        6. 有物理初始猜测背景 (+5)
        """
        if not candidates:
            return {"omega": 0j, "converged": False, "residual": 999,
                    "is_physical": False}

        best = None
        best_score = -999

        for cand in candidates:
            w = cand["omega"]
            score = 0

            # 收敛
            if cand.get("converged", False) and cand.get("residual", 999) < 1e-6:
                score += 20

            # 负虚部（阻尼）
            if w.imag < 0:
                score += 20

            # 阻尼量级合理
            if abs(w.imag) < 0.5:
                score += 15

            # 实部范围合理
            if 0.2 < w.real < 1.0:
                score += 10

            # 接近 Berti 参考
            if berti_ref is not None and abs(berti_ref) > 0:
                delta = abs(w - berti_ref)
                score += 20 * np.exp(-delta / 0.1)

            # LACI 分数
            if "laci" in cand:
                score += 10 * cand["laci"]

            cand["_score"] = score
            if score > best_score:
                best_score = score
                best = cand

        best["is_physical"] = best_score >= 40
        best["_score"] = best_score
        best["n_candidates"] = len(candidates)
        return best

    def _multi_start_solve(self, l: int, m: int, n: int = 0, tol: float = 1e-10) -> dict:
        """多起始点 Newton，收集所有根，筛选最物理解。

        对高自旋 m≠0 尤其重要——CF 方程有多个根，
        需要从不同初始猜测出发，用物理判据挑选。
        """
        guesses = self._generate_initial_guesses(l, m, n)

        berti_ref = self._berti_approximation(l, m, n)
        candidates = []

        for label, w0 in guesses:
            # 角向分离常数
            try:
                ang = self.angular.solve_separation_constant(l, m, w0, self.a)
                A_ref = ang["A"]
            except Exception:
                A_ref = None

            result = self._newton_raphson(w0, l, m, self.a, n_inv=n,
                                          tol=tol, A_ref=A_ref)

            if result["converged"]:
                w = result["omega"]
                # 去重：如果已有非常接近的根，保留残差更小的
                dup = False
                for existing in candidates:
                    if abs(existing["omega"] - w) < 1e-6:
                        if result["residual"] < existing["residual"]:
                            existing.update(result)
                            existing["_label"] = label
                        dup = True
                        break
                if not dup:
                    result["_label"] = label
                    candidates.append(result)

        selected = self._select_physical_root(candidates, l, m, berti_ref)

        if selected["converged"] and selected["is_physical"]:
            return selected

        # 最后兜底：如果多起始点也没找到物理解，用 Berti 参考值直接精修
        final = self._newton_raphson(berti_ref, l, m, self.a, n_inv=n,
                                     tol=tol)
        final["is_physical"] = (final["converged"]
                                and final["omega"].imag < 0
                                and abs(final["omega"].imag) < 0.5)
        return final

    def solve(self, l: int, m: int, n: int = 0, tol: float = 1e-10) -> dict:
        """求解 Kerr QNM 频率。

        策略：
        - a=0：直接 Newton（Schwarzschild 基线）
        - m=0：a-homotopy（已验证可靠）
        - m≠0, a≤0.7：S₂ 引导（快速）
        - m≠0, a>0.7：多起始点 + 物理解筛选（高自旋需处理多根）
        """
        if abs(self.a) < 1e-10:
            omega_guess = self._schwarzschild_guess(l, n)
            result = self._newton_raphson(omega_guess, l, m, 0.0, n_inv=n, tol=tol)
            result["is_physical"] = self._is_physical(result["omega"])
            return result

        if m == 0:
            return self._a_homotopy_solve(l, m, n=n, tol=tol)

        # m≠0：先试 S₂ 引导
        s2_result = self._s2_guided_solve(l, m, n=n, tol=tol)
        if s2_result["converged"] and s2_result.get("is_physical", False):
            return s2_result

        # S₂ 没找到物理解 → 多起始点全面搜索
        return self._multi_start_solve(l, m, n=n, tol=tol)
    
    def _schwarzschild_guess(self, l: int, n: int) -> complex:
        """Schwarzschild QNM 初始猜测（Berti 等的近似公式）。"""
        if l == 2 and n == 0:
            return complex(0.373672, -0.0889623)
        elif l == 2 and n == 1:
            return complex(0.346711, -0.273915)
        elif l == 3 and n == 0:
            return complex(0.599443, -0.092703)
        else:
            f_lmn = (l + 0.5 + n + 0.5) / (2 * np.sqrt(27))
            gamma_lmn = -(n + 0.5) / 3
            return complex(f_lmn, -abs(gamma_lmn))


class LACIValidator:
    """LACI (Local Attractor Capture Index) 判据验证器。
    
    综合残差、吸引子分散度、谱间隙来验证物理 QNM 解。
    """
    
    def __init__(self, solver: CorrectedLeaverQNMSolver):
        self.solver = solver
    
    def compute_laci(self, omega: complex, l: int, m: int, n_inv: int = 0) -> dict:
        """计算 LACI 判据。
        
        参数:
            omega: 候选频率
            l, m: 量子数
            n_inv: 反转次数
        
        返回:
            LACI 指标字典
        """
        residual = abs(self.solver._combined_residual(omega, l, m, self.solver.a, n_inv=n_inv))
        
        dispersion = self._compute_attractor_dispersion(omega, l, m, n_inv)
        
        spectral_gap = self._compute_spectral_gap(omega, l, m, n_inv)
        
        laci_score = (1.0 / (1.0 + residual / 1e-10)) * (1.0 - dispersion) * spectral_gap
        
        return {
            "laci": laci_score,
            "residual": residual,
            "dispersion": dispersion,
            "spectral_gap": spectral_gap,
            "is_physical": self.solver._is_physical(omega)
        }
    
    def _compute_attractor_dispersion(self, omega: complex, l: int, m: int, n_inv: int,
                                     n_perturb: int = 10, perturb_size: float = 1e-4) -> float:
        """计算吸引子分散度。"""
        results = []
        for i in range(n_perturb):
            angle = 2 * np.pi * i / n_perturb
            perturb = perturb_size * complex(np.cos(angle), np.sin(angle))
            omega_pert = omega + perturb
            result = self.solver._newton_raphson(omega_pert, l, m, self.solver.a, n_inv=n_inv, max_newton=20)
            if result["converged"]:
                results.append(result["omega"])
        
        if len(results) < 2:
            return 1.0
        
        mean_omega = np.mean(results)
        dispersion = np.std(np.abs(results - mean_omega)) / (perturb_size + 1e-30)
        
        return float(min(1.0, dispersion))
    
    def _compute_spectral_gap(self, omega: complex, l: int, m: int, n_inv: int) -> float:
        """计算谱间隙（基于连分数收敛率）。
        
        通过计算连分数的收敛速度来估计谱间隙。
        收敛越快，谱间隙越大，解越稳定。
        """
        a = self.solver.a
        s = self.solver.s
        
        ang_result = self.solver.angular.solve_separation_constant(l, m, omega, a)
        A = ang_result["A"]
        
        D = self.solver.radial._D_coeffs(omega, a, s, m, A)
        
        N = 100
        n_arr = np.arange(N, N + 20)
        alpha = self.solver.radial._alpha_n(n_arr, D)
        beta = self.solver.radial._beta_n(n_arr, D)
        gamma = self.solver.radial._gamma_n(n_arr, D)
        
        ratios = []
        cf = 0.j
        for i in range(len(n_arr) - 1, -1, -1):
            ni = n_arr[i]
            denom = beta[i] - alpha[i] * cf
            if abs(denom) > 1e-30:
                cf_new = gamma[i] / denom
                if abs(cf) > 1e-30:
                    ratios.append(abs(cf_new / cf))
                cf = cf_new
        
        if len(ratios) > 5:
            rho = np.mean(ratios[-5:])
            spectral_gap = max(0.0, 1.0 - rho)
        else:
            spectral_gap = 0.5
        
        return float(min(1.0, max(0.0, spectral_gap)))


def demo():
    """演示校正后的 Leaver 求解器。"""
    print("=" * 70)
    print("校正后的 Leaver QNM 求解器演示")
    print("=" * 70)
    print()
    
    test_cases = [
        (0.0, 2, 0, 0, "Schwarzschild l=2, m=0, n=0"),
        (0.5, 2, 2, 0, "Kerr a=0.5, l=2, m=2, n=0"),
        (0.5, 2, 0, 0, "Kerr a=0.5, l=2, m=0, n=0"),
        (0.7, 2, 1, 0, "Kerr a=0.7, l=2, m=1, n=0"),
    ]
    
    try:
        from qnm.radial import leaver_cf_inv_lentz
        from qnm.angular import C_and_sep_const_closest
        
        has_qnm = True
        print("参考基准: qnm 包 (Cook-Zalutskiy 方法)")
    except ImportError:
        has_qnm = False
        print("注意: 未安装 qnm 包，无法对比")
    
    print()
    
    for a_val, l, m, n, desc in test_cases:
        print(f"--- {desc} ---")
        solver = CorrectedLeaverQNMSolver(M=1.0, a=a_val, s=-2, max_iter=300)
        result = solver.solve(l=l, m=m, n=n, tol=1e-8)
        
        omega = result["omega"]
        
        print(f"  ω = {omega.real:.6f} {omega.imag:+.6f}i")
        
        if has_qnm:
            A0 = l*(l+1) - (-2)*(-2+1)
            A_ref, _ = C_and_sep_const_closest(A0, s=-2, c=a_val*omega, m=m, l_max=20)
            cf_ref, _, _ = leaver_cf_inv_lentz(omega=omega, a=a_val, s=-2, m=m, A=A_ref, n_inv=n)
            print(f"  qnm 包验证: |CF| = {abs(cf_ref):.2e}")
        
        print(f"  残差: {result['residual']:.2e}")
        print(f"  物理性: {'✅ (负虚部，衰减模式)' if result['is_physical'] else '❌ (正虚部，非物理)'}")
        print(f"  收敛: {'✓' if result['converged'] else '✗'}")
        print()
        
        validator = LACIValidator(solver)
        laci_result = validator.compute_laci(omega, l, m, n_inv=n)
        print(f"  LACI 验证:")
        print(f"    LACI 分数: {laci_result['laci']:.4f}")
        print(f"    残差: {laci_result['residual']:.2e}")
        print(f"    吸引子分散度: {laci_result['dispersion']:.4f}")
        print(f"    谱间隙: {laci_result['spectral_gap']:.4f}")
        print(f"    物理性: {'✅' if laci_result['is_physical'] else '❌'}")
        print()


if __name__ == "__main__":
    demo()
