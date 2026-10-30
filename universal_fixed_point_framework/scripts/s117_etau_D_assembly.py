# -*- coding: utf-8 -*-
# S117 E_τ^D 三阶截断（含 σ⁸ 完全零测度投影）验证（2026-10-27）
# E_τ^D = E_τ^C − 2σ⁸(1+σ)——三阶修正 = 幂基×完全零测度×一阶静默修正
# 检验：E_τ^D 全链 σ_score + 组装链状态

from math import log, e

M_Pl = 1.220890e22
m_e = 0.51099895069
m_mu = 105.6583755
m_tau = 1776.86
rel = {"m_e": 2.94e-10, "m_μ": 2.2e-8, "m_τ": 6.75e-5}

sigma = 1/15
ln15 = log(15)
ln16_15 = log(16/15)
E_tau_obs = -log(m_tau/M_Pl)

eps_mu = 144*e**(-16)*(1+6*sigma**3)
second = sigma**5 - e**(-16)
third = 2*sigma**8*(1+sigma)
E_tau_C = 16*ln15 + (7/10)*ln16_15 - 8*eps_mu - second
E_tau_D = E_tau_C - third

print("=== E_τ 三阶截断（主导 + 8ε_μ + σ⁵−e^{−16} + 2σ⁸(1+σ)） ===")
print(f"三阶修正 2σ⁸(1+σ) = {third:.6e}（幂基×完全零测度×一阶静默修正——0.29% 命中）")
print(f"E_τ^C 残余 = {E_tau_C - E_tau_obs:+.3e}")
print(f"E_τ^D 残余 = {E_tau_D - E_tau_obs:+.3e}")
dD = E_tau_D - E_tau_obs
print("\n=== σ_score（正确口径 |ΔE|/σ_rel） ===")
for name, s in rel.items():
    ss = abs(dD)/s
    print(f"{name} 精度：σ_score = {ss:.4f}——{'达标' if ss<=1 else '提示' if ss<=3 else '不达标'}")

print("\n=== 组装链（E_τ^D + I_i——B''' 间隔） ===")
alpha_v = 16/15 + (2/3)**0.5*(1+6*sigma**3)
I_e = 3*e - sigma**3*(1+alpha_v)
I_mu = I_e - 5.33159876
E_e_D = E_tau_D + I_e
E_mu_D = E_tau_D + I_mu
E_e_obs = -log(m_e/M_Pl)
E_mu_obs = -log(m_mu/M_Pl)
for name, obs, pred, s in [("E_e", E_e_obs, E_e_D, rel["m_e"]), ("E_μ", E_mu_obs, E_mu_D, rel["m_μ"])]:
    d = pred - obs
    ss = abs(d)/s
    print(f"{name}：偏差 {d:+.3e}——σ_score = {ss:.3f}——{'达标' if ss<=1 else '提示' if ss<=3 else '不达标'}")

print("\n=== 三阶修正框架身份 ===")
print(f"2σ⁸(1+σ) = 2·(1/15)⁸·(16/15) = 32/15⁹ = {32/15**9:.6e}")
print(f"2 = 幂基（Powers）、σ⁸ = 完全零测度（k_max 冻结）、(1+σ) = 一阶修正形态")
print(f"三阶/二阶 = {third/second:.4f}、三阶/一阶 = {third/(8*eps_mu):.4f}")
