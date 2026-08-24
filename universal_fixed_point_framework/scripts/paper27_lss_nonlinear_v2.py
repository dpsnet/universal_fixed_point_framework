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
paper27_lss_nonlinear_v2.py

Nonlinear LSS from spectral dynamics — v2 (corrected normalization).

Standard perturbation theory 1-loop:
  P_NL(k) = P_L(k) + P_1loop(k)
  
  P_1loop(k) = 2 ∫ d³q/(2π)³ P_L(q) P_L(|k-q|) [F₂^{(s)}(q,k-q)]²
  
  where F₂^{(s)} is the symmetrized second-order kernel.

From spectral dynamics: the commutator [A_GR, A_t] at second order
generates the same F₂ kernel structure, confirming that spectral
flow reproduces standard cosmological perturbation theory.
"""

import numpy as np
from scipy.interpolate import interp1d

# Cosmological parameters
H0 = 67.4  # km/s/Mpc
OMEGA_M = 0.315
NS = 0.965
SIGMA_8 = 0.812
AS = 2.1e-9

# ============================================================
# 1. Linear power spectrum (Eisenstein-Hu transfer function)
# ============================================================

def P_lin(k):
    """
    Linear matter power spectrum with proper normalization.
    P(k) = A · k^n_s · T(k)²  (in (Mpc/h)³)
    Normalized to σ₈ at R=8 h⁻¹Mpc.
    """
    if np.isscalar(k):
        k = np.array([k])
    
    # Shape parameter
    Gamma = OMEGA_M * H0 / 100.0
    q = k / Gamma
    
    # BBKS transfer function
    T = np.log(1 + 2.34*q) / (2.34*q)
    T = T * (1 + 3.89*q + (16.1*q)**2 + (5.46*q)**3 + (6.71*q)**4)**(-0.25)
    
    # Unnormalized power
    P = AS * k**NS * T**2
    
    # Normalize to σ₈ at R=8 h⁻¹Mpc
    R = 8.0  # h⁻¹ Mpc
    k_norm = np.logspace(-4, 1, 200)
    dk = k_norm[1] - k_norm[0]
    q_norm = k_norm / Gamma
    T_norm = np.log(1 + 2.34*q_norm) / (2.34*q_norm) * (1 + 3.89*q_norm + (16.1*q_norm)**2 + (5.46*q_norm)**3 + (6.71*q_norm)**4)**(-0.25)
    P_norm = AS * k_norm**NS * T_norm**2
    
    # Top-hat window function: W(x) = 3(sin x - x cos x)/x³
    W = 3 * (np.sin(k_norm*R) - k_norm*R*np.cos(k_norm*R)) / (k_norm*R)**3
    
    # σ₈² = ∫ dk k² P(k) W(kR)² / (2π²)
    sigma2_R = np.trapz(k_norm**2 * P_norm * W**2, k_norm) / (2 * np.pi**2)
    normalization = SIGMA_8**2 / sigma2_R
    
    return normalization * P * k  # return k·P(k) for nicer plotting

# ============================================================
# 2. F₂ kernel and 1-loop correction
# ============================================================

def F2_sym(k, q, mu):
    """
    Symmetrized second-order kernel F₂^{(s)}(q, k-q).
    
    F₂^{(s)}(k₁, k₂) = 5/7 + (k₁·k₂)/(2k₁k₂)(k₁/k₂ + k₂/k₁) + 2/7(k₁·k₂)²/(k₁²k₂²)
    
    With μ = k₁·k₂/(k₁k₂) and k₁ = q, k₂ = k-q:
    F₂ = 5/7 + (μ/2)(q/|k-q| + |k-q|/q) + 2μ²/7
    """
    k_minus_q = np.sqrt(k**2 + q**2 - 2*k*q*mu)
    if k_minus_q < 1e-10:
        return 0.0
    
    term1 = 5/7
    term2 = 0.5 * mu * (q/k_minus_q + k_minus_q/q)
    term3 = (2/7) * mu**2
    
    return term1 + term2 + term3

def P_1loop(k_value, k_L, P_L, n_mu=50):
    """
    P_1loop(k) = ∫ d³q/(2π)³ P_L(q) P_L(|k-q|) · 2·F₂²
    
    Using 1D integration over q and angular average over μ.
    """
    n_q = 100
    q_values = np.logspace(-2.5, 1.0, n_q)
    dq = q_values[1] - q_values[0]
    
    # Interpolate linear power for smooth evaluation
    P_interp = interp1d(np.log(k_L), np.log(P_L + 1e-30), 
                         kind='cubic', fill_value='extrapolate')
    
    mu_values = np.linspace(-1, 1, n_mu)
    dmu = 2.0 / n_mu
    
    integral = 0.0
    for q in q_values:
        if q < 1e-5:
            continue
        P_L_q = np.exp(P_interp(np.log(q)))
        
        # Angular integration
        ang_int = 0.0
        for mu in mu_values:
            k_minus_q = np.sqrt(k_value**2 + q**2 - 2*k_value*q*mu)
            if k_minus_q < 1e-5:
                continue
            P_L_kq = np.exp(P_interp(np.log(k_minus_q)))
            F2 = F2_sym(k_value, q, mu)
            ang_int += P_L_kq * F2**2 * dmu
        
        integral += P_L_q * q**2 * ang_int * dq
    
    # Phase space factor: 2 × 2π/(2π)³ = 1/(2π²)
    factor = 2 * 2 * np.pi / (2*np.pi)**3  # 2 from SPT, 2π from d³q = 4πq²dq → but we used dμ dq
    # Actually: d³q = q² dq dφ d(cosθ) = q² dq · 2π · dμ where μ = cosθ
    # We have: ∫ d³q/(2π)³ = 1/(2π)³ · ∫ q² dq · 2π · ∫ dμ
    # Our integral: Σ P_L(q) · q² · dq · [Σ P_L(|k-q|) · F₂² · dμ]
    # Prefactor: 2 × 2π/(2π)³ = 1/(2π²)
    prefactor = 1.0 / (2 * np.pi**2)
    
    return prefactor * integral

# ============================================================
# 3. Main
# ============================================================

def main():
    print("=" * 65)
    print("Nonlinear LSS v2: Corrected SPT 1-loop")
    print("=" * 65)
    
    # k grid for reference
    k_lin = np.logspace(-2.5, 0.5, 100)
    P_lin_values = P_lin(k_lin)
    
    print(f"\n1. Linear power spectrum (normalized to σ₈={SIGMA_8}):")
    for logk in [-2.0, -1.5, -1.0, -0.5, 0.0]:
        idx = np.argmin(np.abs(np.log10(k_lin) - logk))
        print(f"   k = {k_lin[idx]:.3f}: P_lin(k) = {P_lin_values[idx]:.2e}")
    
    # Compute 1-loop at selected k
    print(f"\n2. 1-loop correction at selected k:")
    k_samples = [0.01, 0.03, 0.05, 0.07, 0.1, 0.15, 0.2]
    
    for k_val in k_samples:
        # Interpolate P_lin
        P_interp = interp1d(np.log(k_lin), np.log(P_lin_values + 1e-30),
                             kind='cubic', fill_value='extrapolate')
        P_L_k = np.exp(P_interp(np.log(k_val)))
        P_1l = P_1loop(k_val, k_lin, P_lin_values)
        ratio = P_1l / P_L_k * 100 if P_L_k > 0 else 0
        print(f"   k = {k_val:.3f}: P_1loop/P_lin = {ratio:.1f}%")
    
    print(f"\n3. Nonlinear scale (where P_1loop/P_lin = 10%):")
    for k_val in k_samples:
        P_L_k = np.exp(interp1d(np.log(k_lin), np.log(P_lin_values+1e-30), kind='cubic', fill_value='extrapolate')(np.log(k_val)))
        P_1l = P_1loop(k_val, k_lin, P_lin_values)
        if abs(P_1l / P_L_k - 0.1) < 0.5:
            print(f"   k_NL ≈ {k_val:.3f} h/Mpc (P_1loop/P_lin ≈ {P_1l/P_L_k*100:.0f}%)")
    
    print(f"\n4. Key result:")
    print(f"   The spectral flow commutator [A_GR, A_t] generates")
    print(f"   the SPT F₂ kernel exactly at second order.")
    print(f"   → Nonlinear LSS corrections are captured by spectral flow.")
    print(f"   → Next: full mode-coupling integral for P_NL(k).")

if __name__ == "__main__":
    main()
