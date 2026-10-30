# -*- coding: utf-8 -*-
"""Phase 104az-67: b0 = N_gen^2 identity chain check (Lambda gap family connection)

New unregistered identity: with N_f = N_gen = 3, b0 = (11*N_c - 2*N_f)/3 = 9 = N_gen^2.
Consequences:
  - F_np component (b0/10)^3 = (N_gen^2/(N_gen+k_max-1))^3 = 729/1000
  - D11 gap 9/25 = b0/(k_max-N_gen)^2 = N_gen^2/(8-3)^2 -- same numerator family
Output: pure ASCII only (PowerShell stdout constraint).
"""
import math

N_c = 3
N_f = 3          # framework effective flavor count = N_gen
N_gen = 3
k_max = 8

# b0 with N_f = N_gen
b0 = (11*N_c - 2*N_f)/3
print("b0 (N_f=N_gen=3) =", b0)
print("N_gen^2 =", N_gen**2)
print("b0 == N_gen^2:", abs(b0 - N_gen**2) < 1e-15)

# 10 = N_gen + k_max - 1
ten = N_gen + k_max - 1
print("N_gen+k_max-1 =", ten)

# (b0/10)^3 = (N_gen^2/(N_gen+k_max-1))^3
fnp_base = (b0/10.0)**3
fnp_base2 = (N_gen**2/ten)**3
print("(b0/10)^3 =", fnp_base)
print("(N_gen^2/(N_gen+k_max-1))^3 =", fnp_base2)
print("equal:", abs(fnp_base - fnp_base2) < 1e-15)
print("3^6 =", 3**6, "= 729 check")

# Delta_lambda_min and Delta_lambda_3
dlmin = (math.sqrt(3) - 1)/6.0
dl3 = math.sqrt(2)*dlmin
print("Delta_lambda_min =", dlmin)
print("Delta_lambda_3 =", dl3)

# delta = 1/675 (locked via SilenceDeltaIdentity)
delta = 1.0/675.0
print("delta =", delta, "= sigma^2/N_c check:", abs(delta - (1/15.0)**2/N_c) < 1e-15)

# F_np = (b0/10)^3 (1-delta) / Delta_lambda_3
F_np = fnp_base*(1-delta)/dl3
print("F_np =", F_np)
# target 4.220 (gap), relative deviation
gap_target = 4.220
print("rel dev vs 4.220 =", (F_np/gap_target - 1)*100, "%")

# D11 gap family: 9/25 = b0/(k_max-N_gen)^2 = N_gen^2/(8-3)^2
gapD11 = b0/(k_max - N_gen)**2
print("D11 gap 9/25 =", gapD11)
print("N_gen^2/(k_max-N_gen)^2 =", N_gen**2/(k_max-N_gen)**2)

# Family connection: both gaps share numerator N_gen^2
# Lambda gap factor: N_gen^6 / (N_gen+k_max-1)^3  (=(b0/10)^3)
print("Lambda gap numerator N_gen^6 =", N_gen**6, "check 729")
print("m_N gap numerator N_gen^2 =", N_gen**2, "check 9")

# full F_np in pure framework quantities
F_np_pure = (N_gen**2/(N_gen+k_max-1))**3*(1-(1/15.0)**2/N_c)/(math.sqrt(2)*(math.sqrt(3)-1)/6.0)
print("F_np pure framework form =", F_np_pure)
print("consistent:", abs(F_np_pure - F_np) < 1e-15)

# Lambda = M_Pl * exp(-8*pi^2/(b0*dl3)) * F_np  (structure check)
# M_Pl in MeV: 1.221e22 GeV = 1.221e28 MeV... use framework value M_Pl = 1.221e22 (GeV -> MeV = *1e3)
M_Pl_MeV = 1.221e22*1e3
pert = math.exp(-8*math.pi**2/(b0*dl3))
Lam = M_Pl_MeV*pert*F_np
print("Lambda via F_np =", Lam, "MeV (target ~210.3)")
print("ratio to 210.3 =", Lam/210.3)
