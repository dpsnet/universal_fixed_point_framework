import numpy as np
r0, a = 8.0, 0.5

# Get correct E, L from circular orbit
sign = 1.0  # prograde
Omega = 1.0 / (r0**1.5 + sign*a)
g_tt = -(1.0 - 2.0/r0)
g_tphi = -2.0*a/r0
g_phiphi = r0**2 + a**2 + 2.0*a**2/r0
denom_sq = -g_tt - 2.0*g_tphi*Omega - g_phiphi*Omega**2
denom = np.sqrt(denom_sq)
E = -(g_tt + g_tphi*Omega)/denom
L = (g_tphi + g_phiphi*Omega)/denom
print(f"E={E:.10f}, L={L:.10f}")

# Check R=0 at circular orbit
Delta = r0**2 - 2*r0 + a**2
R_val = (E*(r0**2+a**2)-a*L)**2 - Delta*(r0**2 + (L-a*E)**2)
print(f"R(r0) = {R_val:.6e} (should be 0)")

# Check the inverse metric condition at circular orbit
inv_metric_val = g_phiphi*E**2 - 2*g_tphi*E*L + g_tt*L**2 - Delta/r0**2
print(f"inv metric cond = {inv_metric_val:.6f} (should be 0)")
print(f"g_phiphi = {g_phiphi:.6f}")
print(f"g_tphi = {g_tphi:.6f}")
print(f"g_tt = {g_tt:.6f}")
print(f"Delta = {Delta:.6f}")

# Check at r_peri = 7.96
r = 7.96
g_tt_r = -(1.0 - 2.0/r)
g_tphi_r = -2.0*a/r
g_phiphi_r = r**2 + a**2 + 2.0*a**2/r
Delta_r = r**2 - 2*r + a**2

inv_val = g_phiphi_r*E**2 - 2*g_tphi_r*E*L + g_tt_r*L**2 - Delta_r/r**2
print(f"\nAt r={r}: inv_metric_cond = {inv_val:.6f}")
print(f"g_phiphi*E² = {g_phiphi_r*E**2:.6f}")
print(f"-2g_tphi*E*L = {-2*g_tphi_r*E*L:.6f}")
print(f"g_tt*L² = {g_tt_r*L**2:.6f}")
print(f"Delta/r² = {Delta_r/r**2:.6f}")
