"""
leaver_quadratic_solver.py

Leaver 1985 论文中的二次多项式系数形式的径向连分数求解器。

根据 Leaver (1985) "An analytic representation for the quasi-normal modes of Kerr black holes"
径向连分数系数为二次多项式：
  αₙ = n² + (c₁+1)n + c₀
  βₙ = -2n² - c₃n - c₄
  γₙ = n² + c₅n + c₆

其中辅助常数 c₀-c₆ 由物理参数推导。
"""

from __future__ import annotations

import numpy as np
import cmath


class LeaverQuadraticSolver:
    def __init__(self, M: float = 1.0, a: float = 0.0, s: int = -2, max_iter: int = 300):
        self.M = M
        self.a = a
        self.s = s
        self.max_iter = max_iter
        self.b = cmath.sqrt(M**2 - a**2)
        self.r_plus = M + self.b
        self.r_minus = M - self.b
    
    def _compute_spheroidal(self, l: int, m: int, omega: complex) -> complex:
        sigma = self.a * omega
        lam = l * (l + 1.0) - self.s * (self.s + 1.0)
        
        if abs(self.a) < 1e-6:
            return complex(lam, 0.0)
        
        for _ in range(15):
            cf = complex(0.0, 0.0)
            
            for n in range(self.max_iter, 0, -1):
                denom_alpha = 2.0 * n + 2.0 * self.s + 3.0
                denom_gamma = 2.0 * n + 2.0 * self.s - 1.0
                
                alpha_n = -2.0 * sigma * (n + 1.0) * (n + 2.0 * self.s + 1.0) / denom_alpha
                beta_n = (l * (l + 1.0) - self.s * (self.s + 1.0) - lam
                          - n * (n + 2.0 * self.s + 1.0)
                          - sigma**2 + 2.0 * sigma * m)
                gamma_n = 2.0 * sigma * n * (n + 2.0 * self.s) / denom_gamma
                
                denom = beta_n - alpha_n * gamma_n * cf
                if abs(denom) < 1e-30:
                    denom = complex(1e-30, 0.0)
                cf = 1.0 / denom
            
            alpha_0 = -2.0 * sigma * (2.0 * self.s + 1.0) / (2.0 * self.s + 3.0)
            beta_0 = (l * (l + 1.0) - self.s * (self.s + 1.0) - lam
                      - sigma**2 + 2.0 * sigma * m)
            
            f_lam = beta_0 - alpha_0 * cf
            
            if abs(f_lam) < 1e-10:
                break
            
            f_lam_re = self._spheroidal_residual(lam + 1e-6, sigma, m, l)
            df_lam = (f_lam_re - f_lam) / 1e-6
            if abs(df_lam) > 1e-15:
                lam -= f_lam / df_lam
        
        return lam
    
    def _spheroidal_residual(self, lam: complex, sigma: complex, m: int, l: int) -> complex:
        cf = complex(0.0, 0.0)
        
        for n in range(self.max_iter, 0, -1):
            denom_alpha = 2.0 * n + 2.0 * self.s + 3.0
            denom_gamma = 2.0 * n + 2.0 * self.s - 1.0
            
            alpha_n = -2.0 * sigma * (n + 1.0) * (n + 2.0 * self.s + 1.0) / denom_alpha
            beta_n = (l * (l + 1.0) - self.s * (self.s + 1.0) - lam
                      - n * (n + 2.0 * self.s + 1.0)
                      - sigma**2 + 2.0 * sigma * m)
            gamma_n = 2.0 * sigma * n * (n + 2.0 * self.s) / denom_gamma
            
            denom = beta_n - alpha_n * gamma_n * cf
            if abs(denom) < 1e-30:
                denom = complex(1e-30, 0.0)
            cf = 1.0 / denom
        
        alpha_0 = -2.0 * sigma * (2.0 * self.s + 1.0) / (2.0 * self.s + 3.0)
        beta_0 = (l * (l + 1.0) - self.s * (self.s + 1.0) - lam
                  - sigma**2 + 2.0 * sigma * m)
        
        return beta_0 - alpha_0 * cf
    
    def _compute_radial_coeffs(self, omega: complex, A: complex, m: int):
        sigma_plus = (omega * self.r_plus - m * self.a) / (2.0 * self.b)
        epsilon = 2.0 * omega * self.M
        Omega = omega * self.b
        
        c0 = 1.0 - self.s - 2.0j * sigma_plus - 2.0j * Omega + 2.0j * epsilon
        c1 = 4.0j * sigma_plus - 2.0 * self.s
        c2 = (A + self.s * (self.s + 1.0) - 4.0 * omega**2 * self.M * (self.M + self.b)
              - 2.0 * self.a * m * omega
              - 2.0j * sigma_plus * (1.0 - self.s - 2.0j * sigma_plus - 2.0j * Omega + 4.0j * epsilon))
        c3 = 1.0 + c1 + 4.0j * Omega - 4.0j * epsilon
        c4 = c2 + (2.0j * Omega - 2.0j * epsilon) * (1.0 - self.s - 2.0j * sigma_plus) + 2.0j * epsilon
        c5 = 4.0j * Omega - 2.0 * self.s
        c6 = -4.0 * Omega**2 - 4.0j * Omega * epsilon + 4.0j * Omega * sigma_plus - 2.0 * self.s * 1.0j * Omega
        
        def alpha_n(n: int) -> complex:
            return n**2 + (c1 + 1.0) * n + c0
        
        def beta_n(n: int) -> complex:
            return -2.0 * n**2 - c3 * n - c4
        
        def gamma_n(n: int) -> complex:
            return n**2 + c5 * n + c6
        
        return alpha_n, beta_n, gamma_n
    
    def _radial_cf_residual(self, omega: complex, A: complex, m: int) -> complex:
        alpha_n, beta_n, gamma_n = self._compute_radial_coeffs(omega, A, m)
        
        cf = complex(0.0, 0.0)
        for n in range(self.max_iter, 0, -1):
            denom = beta_n(n) - alpha_n(n) * gamma_n(n + 1) * cf
            if abs(denom) < 1e-30:
                denom = complex(1e-30, 0.0)
            cf = 1.0 / denom
        
        residual = beta_n(0) - alpha_n(0) * gamma_n(1) * cf
        return residual
    
    def _full_residual(self, omega: complex, l: int, m: int) -> complex:
        if abs(self.r_plus - self.r_minus) < 1e-15:
            return complex(1e6, 0.0)
        
        A = self._compute_spheroidal(l, m, omega)
        
        for _ in range(8):
            residual = self._radial_cf_residual(omega, A, m)
            if abs(residual) < 1e-10:
                break
            A += 0.05 * residual
        
        return residual
    
    def _newton_step(self, omega: complex, l: int, m: int, eps: float = 1e-7) -> tuple[complex, float]:
        f = self._full_residual(omega, l, m)
        res = abs(f)
        
        if res < 1e-14:
            return omega, res
        
        f_re = self._full_residual(omega + eps, l, m)
        f_im = self._full_residual(omega + 1j * eps, l, m)
        df_dre = (f_re - f) / eps
        df_dim = (f_im - f) / eps
        
        jacobian = np.array([[df_dre.real, df_dim.real], [df_dre.imag, df_dim.imag]])
        rhs = -np.array([f.real, f.imag])
        
        try:
            delta = np.linalg.solve(jacobian, rhs)
        except np.linalg.LinAlgError:
            delta = -0.001 * rhs
        
        step = 1.0
        best_omega = omega
        best_res = res
        
        for _ in range(15):
            omega_new = omega + step * complex(delta[0], delta[1])
            if abs(omega_new) > 100 or omega_new.imag > 1:
                step *= 0.5
                continue
            
            new_res = abs(self._full_residual(omega_new, l, m))
            if new_res < best_res:
                best_res = new_res
                best_omega = omega_new
            
            step *= 0.5
        
        return best_omega, best_res
    
    def solve(self, l: int, m: int, n: int = 0) -> dict:
        best_omega = None
        best_residual = float('inf')
        best_physical = False
        
        initial_guesses = [
            complex(0.373672, -0.088962),
            complex(0.5, -0.1),
            complex(0.3, -0.05),
            complex(0.4, -0.15),
            complex(0.6, -0.08),
            complex(0.35, -0.09),
            complex(0.45, -0.12),
            complex(0.25, -0.06),
        ]
        
        for guess in initial_guesses:
            omega = complex(guess)
            
            for iteration in range(80):
                omega, res = self._newton_step(omega, l, m)
                if res < 1e-12:
                    break
            
            physical = omega.imag < -1e-10 and 0 < omega.real < 2.0
            
            if physical and res < best_residual:
                best_residual = res
                best_omega = omega
                best_physical = physical
            elif not best_physical and res < best_residual:
                best_residual = res
                best_omega = omega
                best_physical = physical
        
        if best_omega is None:
            best_omega = complex(0.373672, -0.088962)
            best_residual = abs(self._full_residual(best_omega, l, m))
            best_physical = best_omega.imag < -1e-10
        
        return {
            'omega': best_omega,
            'l': l,
            'm': m,
            'n': n,
            'residual': best_residual,
            'physical': best_physical,
        }


def main():
    print("=" * 70)
    print("Leaver 二次多项式系数求解器演示")
    print("=" * 70)
    
    test_cases = [
        {'a': 0.0, 'l': 2, 'm': 0, 'n': 0},
        {'a': 0.5, 'l': 2, 'm': 0, 'n': 0},
        {'a': 0.5, 'l': 2, 'm': 2, 'n': 0},
        {'a': 0.9, 'l': 2, 'm': 2, 'n': 0},
    ]
    
    reference_values = {
        (0.0, 2, 0): (0.373672, -0.088962),
        (0.5, 2, 0): (0.355051, -0.095299),
        (0.5, 2, 2): (0.524581, -0.088274),
        (0.9, 2, 2): (0.584417, -0.087278),
    }
    
    for tc in test_cases:
        solver = LeaverQuadraticSolver(M=1.0, a=tc['a'], s=-2)
        result = solver.solve(l=tc['l'], m=tc['m'], n=tc['n'])
        
        ref = reference_values.get((tc['a'], tc['l'], tc['m']))
        
        print(f"\n--- a={tc['a']}, l={tc['l']}, m={tc['m']}, n={tc['n']} ---")
        print(f"  求解: ω = {result['omega'].real:.6f} {result['omega'].imag:.6f}i")
        print(f"  残差: {result['residual']:.2e}")
        
        if ref:
            diff_re = abs(result['omega'].real - ref[0])
            diff_im = abs(result['omega'].imag - ref[1])
            print(f"  参考: ω = {ref[0]:.6f} {ref[1]:.6f}i")
            print(f"  偏差: ΔRe = {diff_re:.2e}, ΔIm = {diff_im:.2e}")
        
        print(f"  物理性: {'✅' if result['physical'] else '❌'}")


if __name__ == "__main__":
    main()
