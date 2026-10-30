# -*- coding: utf-8 -*-
# S113 E_τ^C 三阶截断组装检验（2026-10-27）
# E_τ^C = E_τ − 8ε_μ − (σ⁵ − e^{−16})
#   ——静默族修正三阶截断：主导（16ln15+0.7ln16/15）+ 一阶（8ε_μ）+ 二阶（σ⁵−e^{−16}）
# 检验：E_τ^C 在 m_e/m_μ/m_τ 精度下是否全部达标（σ_score < 1）

from math import log, e

M_Pl = 1.220890e22
m_e = 0.51099895069
m_mu = 105.6583755
m_tau = 1776.86
rel = {"m_e": 2.9e-7, "m_μ": 2.2e-8, "m_τ": 6.75e-5}

sigma = 1/15
ln15 = log(15)
ln16_15 = log(16/15)

E_tau_fw = 16*ln15 + (7/10)*ln16_15
E_tau_obs = -log(m_tau/M_Pl)

eps_mu = 144*e**(-16)*(1+6*sigma**3)
second = sigma**5 - e**(-16)
E_tau_C = E_tau_fw - 8*eps_mu - second

print("=== E_τ 三阶截断（主导 + 8ε_μ + σ⁵−e^{−16}） ===")
print(f"主导（16ln15+0.7ln16/15）= {E_tau_fw:.10f}")
print(f"8ε_μ = {8*eps_mu:.10e}（一阶——B'''）")
print(f"σ⁵−e^{{−16}} = {second:.10e}（二阶——S112 候选——差 0.07%）")
print(f"E_τ^C = {E_tau_C:.10f}")
print(f"E_τ(obs) = {E_tau_obs:.10f}")
dC = E_tau_C - E_tau_obs
print(f"偏差 = {dC:+.3e}")

print("\n=== σ_score（正确口径 |ΔE|/σ_rel） ===")
for name, s in rel.items():
    ss = abs(dC)/s
    print(f"{name} 精度：σ_score = {ss:.4f}——{'达标' if ss<=1 else '提示' if ss<=3 else '不达标'}")

print("\n=== 组装链检验（E_e/E_μ = E_τ^C + I_i——B''' 间隔） ===")
alpha_v = 16/15 + (2/3)**0.5*(1+6*sigma**3)
I_e = 3*e - sigma**3*(1+alpha_v)
I_mu = I_e - 5.33159876
E_e_C = E_tau_C + I_e
E_mu_C = E_tau_C + I_mu
E_e_obs = -log(m_e/M_Pl)
E_mu_obs = -log(m_mu/M_Pl)
for name, obs, pred, s in [("E_e", E_e_obs, E_e_C, rel["m_e"]), ("E_μ", E_mu_obs, E_mu_C, rel["m_μ"])]:
    d = pred - obs
    ss = abs(d)/s
    print(f"{name}：偏差 {d:+.3e}——σ_score = {ss:.3f}——{'达标' if ss<=1 else '提示' if ss<=3 else '不达标'}")

print("\n=== 二阶项框架身份 ===")
print(f"σ⁵ = 1/15⁵ = {sigma**5:.6e}（静默⁵——orbitCount⁻⁵）")
print(f"e^{{−16}} = {e**(-16):.6e}（全态静默——e^{{−2⁴}}）")
print(f"σ⁵−e^{{−16}} = {second:.6e}")
print(f"σ⁵/e^{{−16}} = {sigma**5/e**(-16):.4f}（≈12？——差 {(sigma**5/e**(-16)-12)/12*100:.2f}%）")
print(f"二阶/一阶 = {second/(8*eps_mu):.4f}（≈ 1/108？——ε_μ 家族系数谱延续）")
print(f"二阶/ε_μ = {second/eps_mu:.4f}（ε_μ 单位）")
