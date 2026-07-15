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
    
    def solve(self, l: int, m: int, n: int = 0, tol: float = 1e-10) -> dict:
        """求解 Kerr QNM 频率。

        使用自适应同伦延拓方法，从 Schwarzschild 出发，
        逐步增加自旋参数到目标值。包含：
        - 自适应步长（失败时减半，成功时尝试加倍）
        - 模式跟踪（检测频率跳变，回退重试）
        - 分支跟踪（分离常数 A 连续追踪）
        - 物理性检查（负虚部）
        """
        if abs(self.a) < 1e-10:
            omega_guess = self._schwarzschild_guess(l, n)
            result = self._newton_raphson(omega_guess, l, m, 0.0, n_inv=n, tol=tol)
            result["is_physical"] = self._is_physical(result["omega"])
            return result

        a_target = self.a

        # 初始 A（Schwarzschild 值）
        A_schw = complex(l * (l + 1) - self.s * (self.s + 1), 0)
        A_ref = A_schw

        # 自适应同伦延拓
        omega_current = self._schwarzschild_guess(l, n)
        a_current = 0.0

        # 初始步长：高自旋时用更小的步长
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

            # 模式跟踪：检测频率跳变
            freq_jump = abs(omega_new - prev_omega)
            if freq_jump > 0.15 and a_next > 0.3:
                da *= 0.5
                halvings += 1
                if halvings > max_halvings or da < da_min:
                    converged = False
                    break
                continue

            # 物理性检查
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

            # 成功：更新 A_ref 用于下一步分支跟踪
            ang_result = self.angular.solve_separation_constant(l, m, omega_new, a_next, A_ref=A_ref)
            A_ref = ang_result["A"]

            prev_omega = omega_current
            omega_current = omega_new
            a_current = a_next
            halvings = 0
            da = min(da * 1.5, 0.1)

        # 最终精修
        final_result = self._newton_raphson(omega_current, l, m, a_target, n_inv=n,
                                            tol=tol, A_ref=A_ref)
        final_result["is_physical"] = self._is_physical(final_result["omega"])
        final_result["converged"] = converged and final_result["converged"]

        return final_result
    
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
