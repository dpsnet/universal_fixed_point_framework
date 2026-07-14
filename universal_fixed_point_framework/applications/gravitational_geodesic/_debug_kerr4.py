import kerr_geodesic_integrator as kgi
import numpy as np

# Test
r0, a = 8.0, 0.5
for ecc in [5e-3, 0.1, 0.3]:
    r_peri = r0 * (1 - ecc)
    E_circ, L_circ = kgi.circular_orbit_constants(r0, a)
    E1, E2 = kgi._turning_point_energy(r_peri, L_circ, a)
    E = E1 if abs(E1 - E_circ) < abs(E2 - E_circ) else E2
    print(f"ecc={ecc:.3f}: r_peri={r_peri:.4f}, E_circ={E_circ:.8f}, E1={E1:.8f}, E2={E2:.8f}, E={E:.8f}")
    
    # Check R at r_peri
    Delta = r_peri**2 - 2*r_peri + a**2
    term = E*(r_peri**2 + a**2) - a*L_circ
    R_val = term**2 - Delta*(r_peri**2 + (L_circ-a*E)**2)
    print(f"  R(r_peri) = {R_val:.6e} (should be ~0)")
    
    # Check R'(r_peri) - positive means pericenter
    dterm_dr = 2*E*r_peri
    dDelta_dr = 2*r_peri - 2
    dR_dr = 2*term*dterm_dr - dDelta_dr*(r_peri**2+(L_circ-a*E)**2) - Delta*2*r_peri
    print(f"  R'(r_peri) = {dR_dr:.6f} (positive = pericenter)")
    
    # Quick integration test
    try:
        tau, states = kgi.integrate_bound_orbit(r0, a, eccentricity=ecc, n_periods=3, steps_per_period=500)
        r = states[:, 0]
        print(f"  r min/max: {r.min():.4f}/{r.max():.4f}")
        peri = kgi.find_pericenters(tau, r)
        print(f"  n_peri: {len(peri)}")
    except Exception as ex:
        print(f"  Error: {ex}")
