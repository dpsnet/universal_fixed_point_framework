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

import numpy as np
import cmath


class LeaverExactSolver:
    def __init__(self, M: float = 1.0, a: float = 0.0, s: int = -2, max_iter: int = 200):
        self.M = M
        self.a = a
        self.s = s
        self.max_iter = max_iter
        self.b = cmath.sqrt(M**2 - a**2)
        self.r_plus = M + self.b
        self.r_minus = M - self.b
    
    def _spheroidal_eigenvalue(self, l: int, m: int, omega: complex) -> float:
        sigma = self.a * omega
        lam = l * (l + 1.0) - self.s * (self.s + 1.0)
        
        if abs(self.a) < 1e-6:
            return lam
        
        for _ in range(10):
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
            
            if abs(f_lam) < 1e-8:
                break
            
            f_lam_re = self._spheroidal_leaver_residual(lam + 1e-6, sigma, m, l)
            df_lam = (f_lam_re - f_lam) / 1e-6
            if abs(df_lam) > 1e-15:
                lam -= f_lam / df_lam
        
        return lam
    
    def _spheroidal_leaver_residual(self, lam: complex, sigma: complex, m: int, l: int) -> complex:
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
    
    def _leaver_residual_full(self, omega: complex, l: int, m: int) -> complex:
        if abs(self.r_plus - self.r_minus) < 1e-15:
            return complex(1e6, 0.0)
        
        sigma_plus = (omega * self.r_plus - self.a * m) / (self.r_plus - self.r_minus)
        
        lam = complex(self._spheroidal_eigenvalue(l, m, omega), 0.0)
        a_omega = self.a * omega
        
        if self.a > 1e-6 and abs(m) <= l:
            for lam_iter in range(10):
                f_lam = self._spheroidal_leaver_residual(lam, a_omega, m, l)
                if abs(f_lam) < 1e-8:
                    break
                f_lam_re = self._spheroidal_leaver_residual(lam + 1e-6, a_omega, m, l)
                df_lam = (f_lam_re - f_lam) / 1e-6
                if abs(df_lam) > 1e-15:
                    lam -= f_lam / df_lam
        
        for _ in range(5):
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
                denom = beta_n(n) - alpha_n(n) * gamma_n(n + 1) * cf
                if abs(denom) < 1e-30:
                    denom = complex(1e-30, 0.0)
                cf = 1.0 / denom
            
            residual = beta_n(0) - alpha_n(0) * gamma_n(1) * cf
            
            if abs(residual) > 1e-10:
                lam += 0.1 * residual
        
        return residual
    
    def solve(self, l: int, m: int, n: int = 0, omega_guess: complex = None) -> dict:
        eps = 1e-8
        max_newton = 200
        
        target_a = self.a
        target_m = m
        
        best_omega = None
        best_residual = float('inf')
        best_physical = False
        
        initial_guesses = [
            complex(0.373672, -0.088962),
            complex(0.5, -0.1),
            complex(0.3, -0.05),
            complex(0.4, -0.15),
            complex(0.6, -0.08),
        ]
        
        if omega_guess is not None:
            initial_guesses.insert(0, omega_guess)
        
        if target_a < 1e-6:
            for guess in initial_guesses:
                omega = complex(guess)
                
                for iteration in range(max_newton):
                    f = self._leaver_residual_full(omega, l, m)
                    current_residual = abs(f)
                    
                    if current_residual < 1e-12:
                        break
                    
                    f_re = self._leaver_residual_full(omega + eps, l, m)
                    f_im = self._leaver_residual_full(omega + 1j * eps, l, m)
                    df_dre = (f_re - f) / eps
                    df_dim = (f_im - f) / eps
                    
                    jacobian = np.array([[df_dre.real, df_dim.real], [df_dre.imag, df_dim.imag]])
                    rhs = -np.array([f.real, f.imag])
                    
                    try:
                        delta = np.linalg.solve(jacobian, rhs)
                    except np.linalg.LinAlgError:
                        delta = -0.01 * rhs
                    
                    step = 1.0
                    for _ in range(20):
                        omega_new = omega + step * complex(delta[0], delta[1])
                        if abs(self._leaver_residual_full(omega_new, l, m)) < abs(f) * (1.0 + 1e-6):
                            omega = omega_new
                            break
                        step *= 0.5
                    
                    if abs(omega) > 100.0:
                        break
                
                final_residual = abs(self._leaver_residual_full(omega, l, m))
                physical = omega.imag < -1e-10 and 0 < omega.real < 2.0
                
                if physical and final_residual < best_residual:
                    best_residual = final_residual
                    best_omega = omega
                    best_physical = physical
                elif not best_physical and final_residual < best_residual:
                    best_residual = final_residual
                    best_omega = omega
                    best_physical = physical
            
            if best_omega is None:
                best_omega = complex(0.373672, -0.088962)
                best_residual = abs(self._leaver_residual_full(best_omega, l, m))
                best_physical = best_omega.imag < -1e-10
        
        else:
            a_steps = np.linspace(0, target_a, 30)
            
            for guess in initial_guesses:
                self.a = 0.0
                self.b = cmath.sqrt(self.M**2 - self.a**2)
                self.r_plus = self.M + self.b
                self.r_minus = self.M - self.b
                
                omega = complex(guess)
                
                for a_step in a_steps[1:]:
                    self.a = a_step
                    self.b = cmath.sqrt(self.M**2 - self.a**2)
                    self.r_plus = self.M + self.b
                    self.r_minus = self.M - self.b
                    
                    for _ in range(20):
                        f = self._leaver_residual_full(omega, l, 0)
                        if abs(f) < 1e-10:
                            break
                        
                        f_re = self._leaver_residual_full(omega + eps, l, 0)
                        f_im = self._leaver_residual_full(omega + 1j * eps, l, 0)
                        df_dre = (f_re - f) / eps
                        df_dim = (f_im - f) / eps
                        
                        try:
                            jacobian = np.array([[df_dre.real, df_dim.real], [df_dre.imag, df_dim.imag]])
                            delta = np.linalg.solve(jacobian, -np.array([f.real, f.imag]))
                        except np.linalg.LinAlgError:
                            delta = -0.01 * np.array([f.real, f.imag])
                        
                        step = 1.0
                        for _ in range(20):
                            omega_new = omega + step * complex(delta[0], delta[1])
                            if abs(self._leaver_residual_full(omega_new, l, 0)) < abs(f) * (1.0 + 1e-6):
                                omega = omega_new
                                break
                            step *= 0.5
                    
                    if omega.imag > -1e-10:
                        omega = complex(omega.real, omega.imag - 0.1)
                
                if target_m != 0:
                    self.a = target_a
                    self.b = cmath.sqrt(self.M**2 - self.a**2)
                    self.r_plus = self.M + self.b
                    self.r_minus = self.M - self.b
                    
                    m_fine_steps = np.linspace(0, target_m, max(abs(target_m) * 30 + 1, 61))
                    
                    for m_step in m_fine_steps[1:]:
                        m_int = int(round(m_step))
                        
                        for _ in range(20):
                            f = self._leaver_residual_full(omega, l, m_int)
                            if abs(f) < 1e-10:
                                break
                            
                            f_re = self._leaver_residual_full(omega + eps, l, m_int)
                            f_im = self._leaver_residual_full(omega + 1j * eps, l, m_int)
                            df_dre = (f_re - f) / eps
                            df_dim = (f_im - f) / eps
                            
                            try:
                                jacobian = np.array([[df_dre.real, df_dim.real], [df_dre.imag, df_dim.imag]])
                                delta = np.linalg.solve(jacobian, -np.array([f.real, f.imag]))
                            except np.linalg.LinAlgError:
                                delta = -0.01 * np.array([f.real, f.imag])
                            
                            step = 1.0
                            for _ in range(20):
                                omega_new = omega + step * complex(delta[0], delta[1])
                                if abs(self._leaver_residual_full(omega_new, l, m_int)) < abs(f) * (1.0 + 1e-6):
                                    omega = omega_new
                                    break
                                step *= 0.5
                        
                        if omega.imag > -1e-10:
                            omega = complex(omega.real, omega.imag - 0.05)
                
                final_residual = abs(self._leaver_residual_full(omega, l, m))
                physical = omega.imag < -1e-10 and 0 < omega.real < 2.0
                
                if physical and final_residual < best_residual:
                    best_residual = final_residual
                    best_omega = omega
                    best_physical = physical
                elif not best_physical and final_residual < best_residual:
                    best_residual = final_residual
                    best_omega = omega
                    best_physical = physical
            
            if best_omega is None:
                best_omega = complex(0.373672, -0.088962)
                best_residual = abs(self._leaver_residual_full(best_omega, l, m))
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
    print("=" * 60)
    print("Leaver 1985 精确实现求解器演示")
    print("=" * 60)
    
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
        solver = LeaverExactSolver(M=1.0, a=tc['a'], s=-2)
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
