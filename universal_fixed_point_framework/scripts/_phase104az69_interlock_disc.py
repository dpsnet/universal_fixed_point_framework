# -*- coding: utf-8 -*-
"""Phase 104az-69: interlock ratio tension root-cause discrimination

Tension found in 104az-68: dlP20/dlEM computed via decomposition form
  Delta_lambda_EM = pi/(k_max*N_gen*(d_H+3))   (P7-5e-29)
gives 5.3217, vs registered 5.3203.

Hypothesis: registered 5.3203 comes from identity A / identity B ratio:
  kL*dlEM = 4ln10 (identity A, algebraic, +0.0000%)
  kL*dlP20 = 49.0021 (identity B, +0.0043%)
  => dlP20/dlEM = 49.0021/4ln10 = 5.32034
So the registered value is self-consistent under the canonical (identity-A)
definition; the decomposition form is an *approximate* equivalent that only
matches if d_H satisfies d_H = Lambda/(16 ln10) - 3.

Output: pure ASCII only.
"""
import math

N_gen = 3
k_max = 8
N_c = 3
sigma = 1.0/15.0
delta = sigma**2 / N_c          # 1/675
dH_new = math.log(15) + delta   # 2.7095317 (framework registered)
dH_old = 2.7095                 # old compromise value

kL = 6.0/math.pi * 210.3        # kappa*Lambda, Lambda = 210.3 (P7-6f dual-gauge)

dlP20 = (math.sqrt(3) - 1) / math.factorial(N_gen)   # = dlmin = 0.12200847
print("dlP20 =", dlP20)

# Identity A: kL * dlEM_A = 4 ln10 (algebraic, +0.0000%)
dlEM_A = 4.0*math.log(10.0) / kL
print("dlEM_A (identity A, Lambda=210.3) =", dlEM_A)
print("check kL*dlEM_A =", kL*dlEM_A, "vs 4ln10 =", 4*math.log(10))

# Identity B: kL * dlP20 = 49.0021 (numeric, +0.0043%)
print("kL*dlP20 =", kL*dlP20, "(49.0021 expected, +0.0043%)")

# Ratio canonical: identityB/identityA
ratio_canon = (kL*dlP20)/(4.0*math.log(10.0))
print("ratio canonical =", ratio_canon)
print("49/4ln10 =", 49.0/(4*math.log(10)))
print("49.0021/4ln10 =", 49.0021/(4*math.log(10)))

# Decomposition form with new d_H
dlEM_dec_new = math.pi/(k_max*N_gen*(dH_new+3))
print("dlEM decomposition (dH=ln15+1/675) =", dlEM_dec_new)
print("ratio via decomposition new dH =", dlP20/dlEM_dec_new)

# Decomposition form with old d_H
dlEM_dec_old = math.pi/(k_max*N_gen*(dH_old+3))
print("dlEM decomposition (dH=2.7095) =", dlEM_dec_old)
print("ratio via decomposition old dH =", dlP20/dlEM_dec_old)

# What d_H makes decomposition == identity A?
dH_req = 210.3/(16.0*math.log(10.0)) - 3
print("d_H required for decomposition==identityA =", dH_req)
print("framework dH =", dH_new, " diff =", (dH_req/dH_new - 1)*100, "%")

# Percent deviations
print("--- deviations ---")
print("decomp(new)/idA - 1 =", (dlEM_dec_new/dlEM_A - 1)*100, "%")
print("ratio_dec_new/ratio_canon - 1 =", ((dlP20/dlEM_dec_new)/ratio_canon - 1)*100, "%")
print("ratio_dec_old/ratio_canon - 1 =", ((dlP20/dlEM_dec_old)/ratio_canon - 1)*100, "%")
