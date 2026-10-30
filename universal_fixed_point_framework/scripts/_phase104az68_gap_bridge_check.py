# -*- coding: utf-8 -*-
"""Phase 104az-68: Lambda gap <-> dual spectral gap bridge check

Bridge identity: Delta_lambda_P20 = (sqrt(3)-1)/N_gen! with N_gen=3
              = (sqrt(3)-1)/6 = Delta_lambda_min (paper20 T3: (sqrt(6)-sqrt(2))/sqrt(72) equiv)
F_np denominator: Delta_lambda_3 = sqrt(2)*Delta_lambda_min = sqrt(2)*Delta_lambda_P20
=> Lambda gap (line B #454) shares the same spectral-gap family as dual-gap duality (line B #455).
Output: pure ASCII only.
"""
import math

N_gen = 3
k_max = 8

# Delta_lambda_min two forms (paper20 T3 machine-proved equivalent)
dlmin_a = (math.sqrt(6) - math.sqrt(2)) / math.sqrt(72)
dlmin_b = (math.sqrt(3) - 1) / 6.0
print("Delta_lambda_min form A =", dlmin_a)
print("Delta_lambda_min form B =", dlmin_b)
print("A == B exact:", abs(dlmin_a - dlmin_b) < 1e-15)

# Delta_lambda_P20 (Sp layer, P20 gauge): (sqrt(3)-1)/N_gen!
import math as _m
dlP20 = (math.sqrt(3) - 1) / _m.factorial(N_gen)
print("Delta_lambda_P20 =", dlP20)
print("Delta_lambda_P20 == Delta_lambda_min:", abs(dlP20 - dlmin_a) < 1e-15)

# Delta_lambda_3 = sqrt(2)*Delta_lambda_min = sqrt(2)*Delta_lambda_P20
dl3 = math.sqrt(2) * dlmin_a
print("Delta_lambda_3 =", dl3)
print("sqrt(2)*dlP20 == dl3:", abs(math.sqrt(2)*dlP20 - dl3) < 1e-15)

# F_np in P20 terms
delta = 1.0/675.0
F_np = (N_gen**2/(N_gen+k_max-1))**3 * (1-delta) / dl3
print("F_np =", F_np)
print("rel dev vs 4.220 =", (F_np/4.220 - 1)*100, "%")

# dual gap interlock: Delta_lambda_P20 / Delta_lambda_EM = 7^2/C^2
# Delta_lambda_EM = pi/(k_max*N_gen*(d_H+3)); d_H = ln15 + delta
d_H = math.log(15) + delta
dlEM = math.pi / (k_max * N_gen * (d_H + 3))
ratio = dlP20 / dlEM
print("Delta_lambda_EM =", dlEM)
print("dlP20/dlEM =", ratio)
print("7^2/C^2 =", 49.0/(4.0*math.log(10.0)))
print("interlock match:", abs(ratio - 49.0/(4*math.log(10.0))) < 1e-6)
