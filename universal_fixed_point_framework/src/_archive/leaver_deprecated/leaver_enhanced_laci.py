"""
leaver_enhanced_laci.py

增强版 LACI（Local Attractor Capture Index）求解器。

核心思想：
1. 从多个初始猜测出发，使用 Newton-Raphson 找到多个候选根
2. 对每个候选根计算 LACI 指数：
   LACI = ρ/ρ_ref + Δ/Δ_ref + 1/(γ/γ_ref + ε)
   其中：
   - ρ：残差（不动点残差）
   - Δ：分散度（从附近初值收敛到同一根的程度）
   - γ：谱间隙（局部稳定性）
3. 选择 LACI 最小且满足物理约束的解

物理 QNM 根的特征：
- 小残差（ρ → 0）
- 小分散度（Δ → 0，吸引域明确）
- 大谱间隙（γ 较大，稳定吸引子）
"""

from __future__ import annotations

import numpy as np
import cmath


class LeaverEnhancedLACI:
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
    
    def _newton_solve(self, omega0: complex, l: int, m: int, max_iter: int = 50) -> tuple[complex, float]:
        eps = 1e-8
        omega = complex(omega0)
        
        for iteration in range(max_iter):
            f = self._leaver_residual_full(omega, l, m)
            res = abs(f)
            
            if res < 1e-12:
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
            for _ in range(10):
                omega_new = omega + step * complex(delta[0], delta[1])
                if abs(self._leaver_residual_full(omega_new, l, m)) < res * (1.0 + 1e-6):
                    omega = omega_new
                    break
                step *= 0.5
            
            if abs(omega) > 100.0:
                break
        
        final_res = abs(self._leaver_residual_full(omega, l, m))
        return omega, final_res
    
    def _compute_dispersion(self, omega: complex, l: int, m: int, n_samples: int = 8, radius: float = 0.05) -> float:
        angles = np.linspace(0, 2 * np.pi, n_samples, endpoint=False)
        perturbations = [radius * np.exp(1j * theta) for theta in angles]
        
        converged_omegas = []
        for pert in perturbations:
            try:
                omega_pert, res = self._newton_solve(omega + pert, l, m, max_iter=20)
                if res < 1e-6 and abs(omega_pert) < 100:
                    converged_omegas.append(omega_pert)
            except Exception:
                continue
        
        if len(converged_omegas) < 2:
            return float('inf')
        
        mean_omega = np.mean(converged_omegas)
        dispersion = np.sqrt(np.mean([abs(om - mean_omega)**2 for om in converged_omegas]))
        
        return float(dispersion)
    
    def _compute_spectral_gap(self, omega: complex, l: int, m: int, n_dim: int = 10) -> float:
        eps = 1e-6
        
        def F(z):
            f = self._leaver_residual_full(z, l, m)
            return z - f
        
        z0 = omega
        Z = np.zeros((n_dim, n_dim), dtype=complex)
        
        for i in range(n_dim):
            z_pert = z0 + eps * (i + 1)
            for j in range(n_dim):
                z_pert2 = z_pert + eps * 1j * (j + 1)
                z_next = F(z_pert2)
                Z[i, j] = z_next
        
        try:
            cov = np.cov(Z.real, Z.imag)
            eigenvalues = np.linalg.eigvalsh(cov)
            eigenvalues = np.sort(eigenvalues)[::-1]
            
            if len(eigenvalues) >= 2 and eigenvalues[0] > 1e-15:
                gamma = 1.0 - eigenvalues[1] / eigenvalues[0]
            else:
                gamma = 0.5
            
            return max(0.0, min(1.0, gamma))
        except Exception:
            return 0.0
    
    def compute_laci(self, omega: complex, l: int, m: int) -> dict:
        rho = abs(self._leaver_residual_full(omega, l, m))
        
        delta = self._compute_dispersion(omega, l, m)
        
        gamma = self._compute_spectral_gap(omega, l, m)
        
        rho_ref = 1e-10
        delta_ref = 1e-3
        gamma_ref = 0.1
        eps_laci = 1e-3
        
        laci = (rho / rho_ref + delta / delta_ref + 1.0 / (gamma / gamma_ref + eps_laci))
        
        physical = omega.imag < -1e-10 and 0 < omega.real < 2.0
        
        return {
            'omega': omega,
            'rho': rho,
            'delta': delta,
            'gamma': gamma,
            'laci': laci,
            'physical': physical,
        }
    
    def solve(self, l: int, m: int, n: int = 0) -> dict:
        target_a = self.a
        target_m = m
        
        initial_guesses = [
            complex(0.373672, -0.088962),
            complex(0.5, -0.1),
            complex(0.3, -0.05),
            complex(0.4, -0.15),
            complex(0.6, -0.08),
            complex(0.35, -0.09),
            complex(0.45, -0.12),
            complex(0.55, -0.07),
        ]
        
        candidates = []
        
        for guess in initial_guesses:
            try:
                omega, res = self._newton_solve(guess, l, m)
                if res < 1e-6 and abs(omega) < 100:
                    is_duplicate = False
                    for cand in candidates:
                        if abs(omega - cand['omega']) / max(abs(omega), abs(cand['omega']), 1e-10) < 0.05:
                            is_duplicate = True
                            break
                    
                    if not is_duplicate:
                        laci_info = self.compute_laci(omega, l, m)
                        candidates.append(laci_info)
            except Exception:
                continue
        
        physical_candidates = [c for c in candidates if c['physical']]
        
        if physical_candidates:
            best = min(physical_candidates, key=lambda x: x['laci'])
        elif candidates:
            best = min(candidates, key=lambda x: x['laci'])
        else:
            omega, res = self._newton_solve(complex(0.373672, -0.088962), l, m)
            best = self.compute_laci(omega, l, m)
        
        return {
            'omega': best['omega'],
            'l': l,
            'm': m,
            'n': n,
            'residual': best['rho'],
            'laci': best['laci'],
            'rho': best['rho'],
            'delta': best['delta'],
            'gamma': best['gamma'],
            'physical': best['physical'],
            'n_candidates': len(candidates),
        }


def main():
    print("=" * 70)
    print("增强版 LACI Leaver 求解器演示")
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
        solver = LeaverEnhancedLACI(M=1.0, a=tc['a'], s=-2)
        result = solver.solve(l=tc['l'], m=tc['m'], n=tc['n'])
        
        ref = reference_values.get((tc['a'], tc['l'], tc['m']))
        
        print(f"\n--- a={tc['a']}, l={tc['l']}, m={tc['m']}, n={tc['n']} ---")
        print(f"  求解: ω = {result['omega'].real:.6f} {result['omega'].imag:.6f}i")
        print(f"  残差 ρ: {result['rho']:.2e}")
        print(f"  分散度 Δ: {result['delta']:.2e}")
        print(f"  谱间隙 γ: {result['gamma']:.4f}")
        print(f"  LACI 指数: {result['laci']:.2f}")
        print(f"  候选根数: {result['n_candidates']}")
        
        if ref:
            diff_re = abs(result['omega'].real - ref[0])
            diff_im = abs(result['omega'].imag - ref[1])
            print(f"  参考: ω = {ref[0]:.6f} {ref[1]:.6f}i")
            print(f"  偏差: ΔRe = {diff_re:.2e}, ΔIm = {diff_im:.2e}")
        
        print(f"  物理性: {'✅' if result['physical'] else '❌'}")


if __name__ == "__main__":
    main()
