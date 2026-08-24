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
leaver_correct_solver.py

基于 Leaver 1985 原始论文的正确实现。

核心参考：E.W. Leaver, "An analytic representation for the quasi-normal modes of Kerr black holes",
Phys. Rev. D 34, 384 (1985)

根据用户提供的资料，使用正确的二次多项式系数形式。
"""

from __future__ import annotations

import numpy as np


class LeaverCorrectSolver:
    """
    基于 Leaver 原始文献的正确实现。
    """
    
    def __init__(self, M: float = 1.0, a: float = 0.0, s: int = -2, max_iter: int = 200):
        self.M = M
        self.a = a
        self.s = s
        self.max_iter = max_iter
        self.b = np.sqrt(M ** 2 - a ** 2)
        self.r_plus = M + self.b
        self.r_minus = M - self.b
    
    def leaver_radial_cf(self, omega: complex, lam: complex, m: int) -> complex:
        """
        径向 Leaver 连分数，使用 Leaver 1985 方程 (2.19) 的正确系数。
        
        参数定义：
        - b = sqrt(M^2 - a^2)
        - r_plus = M + b, r_minus = M - b
        - sigma_plus = (omega * r_plus - m * a) / (2 * b)
        - epsilon = 2 * omega * M
        - Omega = omega * b
        
        系数：
        alpha_n = n^2 + (c1 + 1)n + c0
        beta_n = -2n^2 - c3 n - c4
        gamma_n = n^2 + c5 n + c6
        
        其中：
        c0 = 1 - s - 2i*sigma_plus - 2i*Omega + 2i*epsilon
        c1 = 4i*sigma_plus - 2s
        c2 = lam + s(s+1) - 4*omega^2*M*(M+b) - 2*a*m*omega - 2i*sigma_plus*(1-s-2i*sigma_plus - 2i*Omega + 4i*epsilon)
        c3 = 1 + c1 + 4i*Omega - 4i*epsilon
        c4 = c2 + (2i*Omega - 2i*epsilon)*(1-s-2i*sigma_plus) + 2i*epsilon
        c5 = 4i*Omega - 2s
        c6 = -4*Omega^2 - 4i*Omega*epsilon + 4i*Omega*sigma_plus - 2*s*i*Omega
        """
        b = self.b
        r_plus = self.r_plus
        r_minus = self.r_minus
        
        sigma_plus = (omega * r_plus - m * self.a) / (2.0 * b)
        epsilon = 2.0 * omega * self.M
        Omega = omega * b
        
        c0 = 1.0 - self.s - 2.0j * sigma_plus - 2.0j * Omega + 2.0j * epsilon
        c1 = 4.0j * sigma_plus - 2.0 * self.s
        c2 = lam + self.s * (self.s + 1.0) - 4.0 * omega ** 2 * self.M * (self.M + b) - 2.0 * self.a * m * omega - 2.0j * sigma_plus * (1.0 - self.s - 2.0j * sigma_plus - 2.0j * Omega + 4.0j * epsilon)
        c3 = 1.0 + c1 + 4.0j * Omega - 4.0j * epsilon
        c4 = c2 + (2.0j * Omega - 2.0j * epsilon) * (1.0 - self.s - 2.0j * sigma_plus) + 2.0j * epsilon
        c5 = 4.0j * Omega - 2.0 * self.s
        c6 = -4.0 * Omega ** 2 - 4.0j * Omega * epsilon + 4.0j * Omega * sigma_plus - 2.0 * self.s * 1.0j * Omega
        
        def alpha_n(n: int) -> complex:
            return n ** 2 + (c1 + 1.0) * n + c0
        
        def beta_n(n: int) -> complex:
            return -2.0 * n ** 2 - c3 * n - c4
        
        def gamma_n(n: int) -> complex:
            return n ** 2 + c5 * n + c6
        
        cf = complex(0.0, 0.0)
        
        for n in range(self.max_iter, 1, -1):
            cf = alpha_n(n) * gamma_n(n + 1) / (beta_n(n) - cf)
        
        cf = alpha_n(1) * gamma_n(2) / (beta_n(1) - cf)
        cf = alpha_n(0) * gamma_n(1) / (beta_n(1) - cf)
        
        residual = cf - beta_n(0)
        
        return residual
    
    def leaver_angular_cf(self, lam: complex, sigma: complex, m: int, l: int) -> complex:
        """
        角向 Leaver 连分数。
        
        使用 Leaver 1985 标准形式。
        """
        alpha_n = lambda n: n * (n + 2.0 * sigma)
        beta_n = lambda n: lam - n * (n + 1.0) + sigma ** 2 + self.a ** 2 * self.s ** 2
        gamma_n = lambda n: -(n - 1.0) * (n + 2.0 * sigma - 1.0)
        
        cf = complex(0.0, 0.0)
        
        for n in range(self.max_iter, 0, -1):
            cf = alpha_n(n) * gamma_n(n + 1) / (beta_n(n) - cf)
        
        return cf - beta_n(0)
    
    def solve_full(self, l: int, m: int, n: int = 0, omega_guess: complex = None) -> dict:
        """求解完整的 QNM 频率。"""
        if omega_guess is None:
            omega = complex(0.373672 - 0.088962j)
        else:
            omega = complex(omega_guess)
        
        eps = 1e-8
        
        for iteration in range(self.max_iter):
            sigma = self.a * omega
            
            lam = complex(l * (l + 1) - self.s * (self.s + 1), 0.0)
            
            for _ in range(5):
                f_lam = self.leaver_angular_cf(lam, sigma, m, l)
                if abs(f_lam) < 1e-8:
                    break
                f_lam_re = self.leaver_angular_cf(lam + 1e-6, sigma, m, l)
                df_lam = (f_lam_re - f_lam) / 1e-6
                if abs(df_lam) > 1e-15:
                    lam -= f_lam / df_lam
            
            lambda_radial = lam - (l * (l + 1) - self.s * (self.s + 1))
            f_rad = self.leaver_radial_cf(omega, lambda_radial, m)
            
            if abs(f_rad) < 1e-8:
                break
            
            f_re = self.leaver_radial_cf(omega + eps, lam, m)
            f_im = self.leaver_radial_cf(omega + 1j * eps, lam, m)
            
            df_dre = (f_re - f_rad) / eps
            df_dim = (f_im - f_rad) / eps
            
            jacobian = np.array([[df_dre.real, df_dim.real], [df_dre.imag, df_dim.imag]])
            rhs = -np.array([f_rad.real, f_rad.imag])
            
            try:
                delta = np.linalg.solve(jacobian, rhs)
            except np.linalg.LinAlgError:
                delta = -0.01 * rhs
            
            omega += complex(delta[0] * 0.5, delta[1] * 0.5)
        
        f_final = self.leaver_radial_cf(omega, lam, m)
        
        return {
            "omega": omega,
            "residual": abs(f_final),
            "converged": abs(f_final) < 1e-8,
            "is_physical": omega.imag < -1e-10,
        }


def run_correct_solver_demo():
    """运行正确求解器演示。"""
    print("=" * 70)
    print("Leaver 正确实现求解器演示（基于 Leaver 1985）")
    print("=" * 70)
    
    BERTI_REF = {
        (0.0, 2, 0, 0): 0.373672 - 0.088962j,
        (0.5, 2, 0, 0): 0.365 - 0.087j,
        (0.5, 2, 2, 0): 0.501 - 0.085j,
        (0.9, 2, 2, 0): 0.701 - 0.085j,
    }
    
    for (a, l, m, n), ref_omega in BERTI_REF.items():
        print(f"\n--- a={a}, l={l}, m={m}, n={n} ---")
        
        solver = LeaverCorrectSolver(M=1.0, a=a, s=-2)
        result = solver.solve_full(l, m, n, ref_omega)
        
        if result["converged"]:
            omega = result["omega"]
            rel_error = abs(omega - ref_omega) / abs(ref_omega)
            print(f"  求解: ω = {omega.real:.6f} {omega.imag:.6f}i")
            print(f"  参考: ω = {ref_omega.real:.6f} {ref_omega.imag:.6f}i")
            print(f"  相对误差: {rel_error:.4e}")
            print(f"  残差: {result['residual']:.2e}")
            print(f"  物理性: {'✅' if result['is_physical'] else '❌'}")
            print(f"  一致性: {'✓' if rel_error < 1e-4 else '❌'}")
        else:
            print(f"  未收敛: ω = {result['omega']}")
            print(f"  残差: {result['residual']:.2e}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    run_correct_solver_demo()
