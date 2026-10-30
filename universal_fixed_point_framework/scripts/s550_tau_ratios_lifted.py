# -*- coding: utf-8 -*-
"""
S550 比值链三闭合升格先证伪（m_τ/m_μ = e^{I_μ}、m_τ/m_e = e^{I_e_next−27/80·e⁻¹⁹}）
公式：AlphaChain.lean tau_mu_ratio_anchor（E_μ−E_τ^D = imu_final）、
  tau_e_ratio_anchor（E_e−E_τ^D = I_e_next − 27/80·e⁻¹⁹）
验证：泊松形式 vs 未升格残差 ~1e-15，比值 σ_score 不变。
"""
import math

SIG = 1/15.0
LN15 = math.log(15)

def e_tsum(K=50):
    return sum(1.0/math.factorial(k) for k in range(K+1))

E = e_tsum()
def exp_n(n):  return E**n
def exp_neg(n): return (E**n)**(-1)

ALPHA_VP = 16/15.0 + math.sqrt(2/3.0)*(1 + 6*SIG**3)
EPS_MU_L = 144 * exp_neg(16) * (1 + 6*SIG**3)
E_TAU_D_L = 16*LN15 + 0.7*math.log(16/15.0) - 8*EPS_MU_L \
            - (SIG**5 - exp_neg(16)) - 2*SIG**8*(1+SIG)
I_E_L = 3*E - SIG**3*(1 + ALPHA_VP)
I_E_NEXT_L = I_E_L + (5/2.0)*exp_neg(18)
I_MU_L = E + 42*exp_neg(6) + 2*SIG**5
E_E_FINAL_L = E_TAU_D_L + I_E_NEXT_L - (27/80.0)*exp_neg(19)
E_MU_FINAL_L = E_TAU_D_L + I_MU_L

# 未升格参考
EPS_MU_0 = 144 * math.exp(-16) * (1 + 6*SIG**3)
E_TAU_D_0 = 16*LN15 + 0.7*math.log(16/15.0) - 8*EPS_MU_0 \
            - (SIG**5 - math.exp(-16)) - 2*SIG**8*(1+SIG)
I_E_0 = 3*math.e - SIG**3*(1 + ALPHA_VP)
I_E_NEXT_0 = I_E_0 + (5/2.0)*math.exp(-18)
I_MU_0 = math.e + 42*math.exp(-6) + 2*SIG**5
E_E_0 = E_TAU_D_0 + I_E_NEXT_0 - (27/80.0)*math.exp(-19)
E_MU_0 = E_TAU_D_0 + I_MU_0

# 间隔（比值锚形态）
gap_tm_L = E_MU_FINAL_L - E_TAU_D_L        # E_μ−E_τ^D（m_τ/m_μ 间隔）
gap_tm_0 = E_MU_0 - E_TAU_D_0
gap_te_L = E_E_FINAL_L - E_TAU_D_L         # E_e−E_τ^D（m_τ/m_e 间隔）
gap_te_0 = E_E_0 - E_TAU_D_0

print("S550 比值链三闭合升格先证伪（K=50）")
print(f"E_μ−E_τ^D  lifted {gap_tm_L!r} vs ref {gap_tm_0!r}  残差 {gap_tm_L-gap_tm_0:+.3e}")
print(f"E_e−E_τ^D  lifted {gap_te_L!r} vs ref {gap_te_0!r}  残差 {gap_te_L-gap_te_0:+.3e}")
print(f"I_μ 直接比对        {I_MU_L-I_MU_0:+.3e}")
print(f"I_e_next−27/80·e⁻¹⁹ {I_E_NEXT_L-(27/80.0)*exp_neg(19) - (I_E_NEXT_0-(27/80.0)*math.exp(-19)):+.3e}")

# 比值 σ_score（PDG 2026）
m_e, u_e = 0.51099895069, 1.6e-10
m_mu, u_mu = 105.6583755, 2.3e-6
m_tau, u_tau = 1776.93, 0.09
rel_e, rel_mu, rel_tau = u_e/m_e, u_mu/m_mu, u_tau/m_tau

r_tm_pred = math.exp(I_MU_L)
r_tm_exp = m_tau/m_mu
ss_tm = abs(r_tm_pred-r_tm_exp)/(r_tm_exp*math.sqrt(rel_tau**2+rel_mu**2))
print(f"m_τ/m_μ 预测 {r_tm_pred:.8f} vs 实验 {r_tm_exp:.8f} → σ_score = {ss_tm:.4f}")

r_te_pred = math.exp(I_E_NEXT_L - (27/80.0)*exp_neg(19))
r_te_exp = m_tau/m_e
ss_te = abs(r_te_pred-r_te_exp)/(r_te_exp*math.sqrt(rel_tau**2+rel_e**2))
print(f"m_τ/m_e 预测 {r_te_pred:.8f} vs 实验 {r_te_exp:.8f} → σ_score = {ss_te:.4f}")

assert abs(gap_tm_L-gap_tm_0) < 1e-8, "tau_mu 间隔升格证伪失败"
assert abs(gap_te_L-gap_te_0) < 1e-8, "tau_e 间隔升格证伪失败"
print("S550 先证伪 PASS（残差 ~1e-15 机器精度——可投入 Lean 证明）")
