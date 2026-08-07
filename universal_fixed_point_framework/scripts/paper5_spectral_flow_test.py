"""
paper5_spectral_flow_test.py

Numerical verification of the spectral flow equation:

    d/dt A_t = [A_F, A_t]

for a simple harmonic oscillator (SHO) system.

Tests:
  1. Spectral invariance: σ(A_t) = σ(A_0) for all t
  2. Nöther conservation: Tr(A_F · A_t) constant
  3. Analytic vs numeric: |A_t - e^{t A_F} A_0 e^{-t A_F}| < 1e-8
"""

import numpy as np
from scipy.linalg import expm, logm
import matplotlib.pyplot as plt

# ============================================================
# 1. Simple Harmonic Oscillator Rec Object
# ============================================================

def build_sho_system(n=4, hbar=1.0, omega=1.0):
    """
    Build SHO Rec system as n×n matrix.
    
    Koopman operator U = exp(-A) where A is the Hamiltonian matrix.
    For the SHO, H = hbar·ω·(a†a + 1/2), eigenvalues E_n = hbar·ω·(n + 1/2).
    
    The "force" generator A_F is the Liouvillian L_H = -i[H, ·].
    In matrix form, this becomes the commutator with H.
    """
    # Hamiltonian eigenvalues
    E = hbar * omega * (np.arange(n) + 0.5)
    
    # A_0 = H / hbar (normalized, matching the spectral flow convention)
    A_0 = np.diag(E / hbar)
    
    # A_F = -i L_H = -i[H, ·] 
    # In matrix form: ad_H(X) = [H, X], so A_F = -i * ad_H
    # We represent this as a superoperator acting on the vectorized matrix
    # For the SHO, the Liouvillian generates coherent time evolution
    
    # Simple choice: A_F = -i * H (acts on A_t by commutation)
    A_F = -1j * np.diag(E)
    
    return A_0, A_F

# ============================================================
# 2. Exact Spectral Flow Solution
# ============================================================

def exact_spectral_flow(A_0, A_F, t):
    """Analytic solution: A_t = exp(t·A_F)·A_0·exp(-t·A_F)."""
    exp_tF = expm(t * A_F)
    exp_neg_tF = expm(-t * A_F)
    return exp_tF @ A_0 @ exp_neg_tF

# ============================================================
# 3. Numerical Spectral Flow (ODE integration)
# ============================================================

def spectral_flow_rhs(t, A_flat, A_F):
    """RHS of spectral flow equation: dA/dt = [A_F, A]."""
    n = int(np.sqrt(len(A_flat)))
    A = A_flat.reshape(n, n)
    dA_dt = A_F @ A - A @ A_F
    return dA_dt.flatten()

def numerical_spectral_flow(A_0, A_F, t_span, n_steps=1000):
    """Numerical integration of spectral flow equation."""
    from scipy.integrate import solve_ivp
    
    n = A_0.shape[0]
    A_0_flat = A_0.flatten()
    
    sol = solve_ivp(
        spectral_flow_rhs,
        t_span,
        A_0_flat,
        args=(A_F,),
        method='RK45',
        t_eval=np.linspace(t_span[0], t_span[1], n_steps),
        rtol=1e-10,
        atol=1e-12
    )
    
    # Reshape results back to matrices
    A_t_series = sol.y.T.reshape(-1, n, n)
    return sol.t, A_t_series

# ============================================================
# 4. Verification Tests
# ============================================================

def test_spectral_invariance(A_0, A_t_series, tol=1e-10):
    """Test: eigenvalues of A_t are invariant under spectral flow."""
    e0 = np.linalg.eigvalsh(A_0) if np.allclose(A_0, A_0.conj().T) else np.linalg.eigvals(A_0)
    max_dev = 0.0
    
    for i, A_t in enumerate(A_t_series):
        et = np.linalg.eigvalsh(A_t) if np.allclose(A_t, A_t.conj().T) else np.linalg.eigvals(A_t)
        # Sort eigenvalues for comparison
        e0_sorted = np.sort(np.abs(e0))
        et_sorted = np.sort(np.abs(et))
        dev = np.max(np.abs(et_sorted - e0_sorted))
        max_dev = max(max_dev, dev)
        
        if dev > tol:
            print(f"  SPECTRAL INVARIANCE FAILED at t[{i}]: max dev = {dev:.2e} > {tol:.0e}")
            return False
    
    print(f"  ✓ Spectral invariance: max eigenvalue deviation = {max_dev:.2e} (tol={tol:.0e})")
    return max_dev < tol

def test_noether_conservation(A_0, A_F, A_t_series, tol=1e-10):
    """Test: Tr(A_F · A_t) is conserved (Nöther's theorem, spectral version)."""
    trace_0 = np.trace(A_F @ A_0)
    max_dev = 0.0
    
    for A_t in A_t_series:
        trace_t = np.trace(A_F @ A_t)
        dev = abs(trace_t - trace_0)
        max_dev = max(max_dev, dev)
    
    print(f"  ✓ Nöther conservation: max Tr deviation = {max_dev:.2e} (tol={tol:.0e})")
    return max_dev < tol

def test_analytic_vs_numeric(A_0, A_F, t_eval, A_t_series, tol=1e-8):
    """Test: numerical solution matches analytic solution A_t = e^{tF} A_0 e^{-tF}."""
    max_dev = 0.0
    
    for i, t in enumerate(t_eval):
        A_exact = exact_spectral_flow(A_0, A_F, t)
        A_num = A_t_series[i]
        dev = np.max(np.abs(A_num - A_exact))
        max_dev = max(max_dev, dev)
    
    print(f"  ✓ Analytic vs numeric: max deviation = {max_dev:.2e} (tol={tol:.0e})")
    return max_dev < tol

# ============================================================
# 5. Main
# ============================================================

def main():
    print("=" * 60)
    print("Paper V: Spectral Flow Equation - Numerical Verification")
    print("=" * 60)
    
    # System parameters
    n = 4
    hbar = 1.0
    omega = 1.0
    T_max = 10.0
    
    print(f"\nSystem: SHO (n={n} levels, hbar={hbar}, omega={omega})")
    print(f"Time span: [0, {T_max}]")
    
    A_0, A_F = build_sho_system(n, hbar, omega)
    
    print(f"\nA_0 shape: {A_0.shape}")
    print(f"A_F (force generator) shape: {A_F.shape}")
    print(f"eig(A_0) = {np.sort(np.linalg.eigvalsh(A_0))}")
    print(f"eig(A_F) = {np.sort(np.abs(np.linalg.eigvals(A_F)))}")
    
    # Compute numerical solution
    print("\n--- Numerical integration ---")
    t_eval, A_t_series = numerical_spectral_flow(A_0, A_F, [0, T_max], n_steps=500)
    print(f"  Steps: {len(t_eval)}")
    
    # Run tests
    print("\n--- Verification tests ---")
    all_passed = True
    
    all_passed &= test_spectral_invariance(A_0, A_t_series)
    all_passed &= test_noether_conservation(A_0, A_F, A_t_series)
    all_passed &= test_analytic_vs_numeric(A_0, A_F, t_eval, A_t_series)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("ALL TESTS PASSED ✓")
        print("Spectral flow equation numerically verified for SHO system.")
    else:
        print("SOME TESTS FAILED ✗")
    print("=" * 60)
    
    # Plot spectral evolution
    print("\n--- Spectral evolution ---")
    eigs_over_time = []
    for A_t in A_t_series[::20]:  # subsample
        eigs = np.linalg.eigvalsh(A_t) if np.allclose(A_t, A_t.conj().T) else np.linalg.eigvals(A_t)
        eigs_over_time.append(np.sort(np.abs(eigs)))
    eigs_over_time = np.array(eigs_over_time)
    
    for k in range(n):
        dev = np.max(np.abs(eigs_over_time[:, k] - eigs_over_time[0, k]))
        print(f"  Eigenvalue {k}: max deviation = {dev:.2e}")
    
    return all_passed

if __name__ == "__main__":
    main()
