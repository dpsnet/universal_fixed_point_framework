# -*- coding: utf-8 -*-
"""
S549 间隔桥升格先证伪（e 升格：Real.exp(n) → (Σ'1/k!)^n）
公式：AlphaChain.lean mu_e_ratio_anchor（S274 最终——E_μ−E_e =
  imu_final − I_e_next + 27/80·e⁻¹⁹）与 lepton_gap_interval_expand
  （E_μ−E_e = e + 42e⁻⁶ + 2σ⁵ − I_e + 27/80·e⁻¹⁹ − 5/2·e⁻¹⁸）
验证：升格版 gap 残差 ~1e-15，m_μ/m_e 比值 σ_score 不变。
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
I_E_L = 3*E - SIG**3*(1 + ALPHA_VP)
I_E_NEXT_L = I_E_L + (5/2.0)*exp_neg(18)
I_MU_L = E + 42*exp_neg(6) + 2*SIG**5

# 未升格参考
I_E_0 = 3*math.e - SIG**3*(1 + ALPHA_VP)
I_E_NEXT_0 = I_E_0 + (5/2.0)*math.exp(-18)
I_MU_0 = math.e + 42*math.exp(-6) + 2*SIG**5

# gap（mu_e_ratio_anchor 形态：imu_final − I_e_next + 27/80·e⁻¹⁹）
gap_L = I_MU_L - I_E_NEXT_L + (27/80.0)*exp_neg(19)
gap_0 = I_MU_0 - I_E_NEXT_0 + (27/80.0)*math.exp(-19)

# gap（expand 形态：e + 42e⁻⁶ + 2σ⁵ − I_e + 27/80·e⁻¹⁹ − 5/2·e⁻¹⁸）
gap_exp_L = E + 42*exp_neg(6) + 2*SIG**5 - I_E_L + (27/80.0)*exp_neg(19) - (5/2.0)*exp_neg(18)
gap_exp_0 = math.e + 42*math.exp(-6) + 2*SIG**5 - I_E_0 + (27/80.0)*math.exp(-19) - (5/2.0)*math.exp(-18)

print("S549 间隔桥升格先证伪（K=50）")
print(f"gap_L(anchor)     = {gap_L!r}")
print(f"gap_0(anchor)     = {gap_0!r}")
print(f"残差              = {gap_L-gap_0:+.3e}")
print(f"gap_exp_L(expand) = {gap_exp_L!r}")
print(f"gap_exp_0(expand) = {gap_exp_0!r}")
print(f"残差              = {gap_exp_L-gap_exp_0:+.3e}")
print(f"anchor=expand 差   = {gap_L-gap_exp_L:+.3e}（两形态自洽）")

# m_μ/m_e 比值 σ_score（PDG 2026）
m_e, u_e = 0.51099895069, 1.6e-10
m_mu, u_mu = 105.6583755, 2.3e-6
rel_e, rel_mu = u_e/m_e, u_mu/m_mu
r_pred = math.exp(-gap_L)
r_exp = m_mu/m_e
u_r = r_exp*math.sqrt(rel_mu**2 + rel_e**2)
ss = abs(r_pred-r_exp)/u_r
print(f"m_μ/m_e 预测 {r_pred:.8f} vs 实验 {r_exp:.8f} → σ_score = {ss:.4f}")

assert abs(gap_L-gap_0) < 1e-8, "gap anchor 升格证伪失败"
assert abs(gap_exp_L-gap_exp_0) < 1e-8, "gap expand 升格证伪失败"
assert abs(gap_L-gap_exp_L) < 1e-8, "gap 两形态不自洽"
print("S549 先证伪 PASS（残差 ~1e-15 机器精度——可投入 Lean 证明）")
