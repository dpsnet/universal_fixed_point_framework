# -*- coding: utf-8 -*-
# S111 口径勘误重算（2026-10-27）
# 用户指出 m_e/m_μ 不达标——核查 S108/S109 的 σ_score 口径
# 正确口径：E = −ln(m/M_Pl)——|ΔE| ≈ |Δm/m|——σ_score(E) = |ΔE|/σ_rel
#   （σ_rel = m 的相对不确定度——ln 传播）
# 错误口径（S108 曾用）：|ΔE|/(E·σ_rel)——多除一个 E——少乘一个 E

from math import log

M_Pl = 1.220890e22
m_e = 0.51099895069
m_mu = 105.6583755
m_tau = 1776.86
rel = {"m_e": 2.9e-7, "m_μ": 2.2e-8, "m_τ": 6.75e-5}   # 相对不确定度

ln15 = log(15)
ln16_15 = log(16/15)
E_tau_fw = 16*ln15 + (7/10)*ln16_15

E_tau_obs = -log(m_tau/M_Pl)
E_mu_obs = -log(m_mu/M_Pl)
E_e_obs = -log(m_e/M_Pl)

d_tau = E_tau_fw - E_tau_obs
print("=== 口径对比（E_τ 主框架——同一偏差 1.31e-4） ===")
print(f"偏差 |ΔE_τ| = {abs(d_tau):.3e}")
print(f"#74 口径：σ_score = |ΔE|/σ_rel = {abs(d_tau)/rel['m_τ']:.3f}（提示级 1~3）")
print(f"S108 口径：σ_score = |ΔE|/(E·σ_rel) = {abs(d_tau)/(E_tau_obs*rel['m_τ']):.4f}（错误——少乘 E）")
print(f"⟹ S108 的 0.045 达标 = 口径错误——正确 = 1.9σ_score 提示级（#74 原登记）")

print("\n=== 各链正确口径重算（σ_score = |ΔE|/σ_rel） ===")
# E_τ 主框架
print(f"E_τ(主框架 16ln15+0.7ln16/15)：σ_score = {abs(d_tau)/rel['m_τ']:.2f}（提示级）")
# E_e/E_μ 组装（E_τ(fw) + I_i——S109 候选）
sigma = 1/15
alpha_v = 16/15 + (2/3)**0.5*(1+6*sigma**3)
I_e = 3*2.718281828459045 - sigma**3*(1+alpha_v)
I_mu = I_e - 5.33159876
E_e_asm = E_tau_fw + I_e
E_mu_asm = E_tau_fw + I_mu
d_e = E_e_asm - E_e_obs
d_mu = E_mu_asm - E_mu_obs
print(f"E_e(组装 E_τ(fw)+I_e)：差 {d_e:.2e}——σ_score = {abs(d_e)/rel['m_e']:.0f}（严重不达标）")
print(f"E_μ(组装 E_τ(fw)+I_μ)：差 {d_mu:.2e}——σ_score = {abs(d_mu)/rel['m_μ']:.0f}（严重不达标）")

print("\n=== B''' 修正后（E_τ^B——0.018σ_score m_τ 口径） ===")
# E_τ^B 的 |ΔE| = 0.018·σ_rel(τ)
d_tauB = 0.018*rel['m_τ']
print(f"E_τ^B 偏差 = {d_tauB:.2e}（m_τ 口径 0.018σ_score 达标）")
print(f"  在 m_e 精度：σ_score = {d_tauB/rel['m_e']:.1f}（{'不达标' if d_tauB/rel['m_e']>3 else '达标'}）")
print(f"  在 m_μ 精度：σ_score = {d_tauB/rel['m_μ']:.0f}（不达标）")
print(f"⟹ B''' 修正后 E_τ^B 在 m_τ 精度达标——但绝对偏差继承到 m_e/m_μ 精度仍不达标")

print("\n=== 核心开放项（绝对精度） ===")
print(f"E_τ 框架公式的绝对精度要求：达 m_e 级 → |ΔE| < σ_rel(e) = 2.9e-7（相对 3e-7）")
print(f"当前主框架 |ΔE| = 1.31e-4——差 {1.31e-4/2.9e-7:.0f} 倍")
print(f"当前 B''' 修正后 |ΔE| = {d_tauB:.2e}——差 {d_tauB/2.9e-7:.1f} 倍")
print(f"⟹ 需要 E_τ 框架公式的更高阶修正（ε_e 类/第三链）——'绝对链精度提升'是主攻")
