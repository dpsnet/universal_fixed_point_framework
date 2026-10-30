# -*- coding: utf-8 -*-
# 0.7 判别验证（S120 补充——含修正反解）（2026-10-27）
# x = (E_τ_obs + 8ε_μ + 二阶 + 三阶 − 16ln15)/ln(16/15)
# 若 x ≈ 7/10 = Involution/(Powers·Silence)——0.7 框架身份获支持

from math import log, e

sigma = 1/15
M_Pl = 1.220890e22
m_tau = 1776.86
E_tau_obs = log(M_Pl/m_tau)
eps_mu = 144*e**(-16)*(1+6*sigma**3)
second = sigma**5 - e**(-16)
third = 2*sigma**8*(1+sigma)

x = (E_tau_obs + 8*eps_mu + second + third - 16*log(15)) / log(16/15)
print(f"E_τ_obs = {E_tau_obs:.8f}")
print(f"8ε_μ = {8*eps_mu:.6e}、二阶 = {second:.6e}、三阶 = {third:.6e}")
print(f"主导 16ln15 = {16*log(15):.8f}")
print(f"反解 x = {x:.6f}")
print(f"0.7 vs x——差 = {abs(0.7-x)/0.7*100:.4f}%")
print(f"7/10 = Involution/(Powers·Silence)——框架量身份")
