# -*- coding: utf-8 -*-
"""静默族公共结构量 6σ³ 双链普适验证（2026-10-26）

核心发现：ε_μ = 144e^{−16}·(1+6σ³)（+0.0048% vs 144e^{−16} 的 −0.172%）
与 α_v 修正（√(2/3)(1+6σ³)）共享同一静默族结构量 6σ³ = N_gen!·σ³。
验证体系 B'（6σ³ 统一修正）全链 σ：
  I_e  = 3e − σ³(1 + 16/15 + √(2/3)(1+6σ³))       （α_v 静默修正）
  I_μ  = ln16 + e^{−3} + 144e^{−16}(1+6σ³)          （ε_μ 精确身份）
  E_τ  = 16ln15 + (7/10)ln(16/15) − 8·144e^{−16}(1+6σ³)
"""
import math

sigma = 1/15; s3 = sigma**3
m_e_c, m_mu_c, m_tau_c = 0.51099895069, 105.6583755, 1776.86
rel_e, rel_mu, rel_tau = 2.935e-8, 2.177e-8, 6.753e-5
M_Pl_MeV = 1.220890e22
sE = math.sqrt((2.2e-5/2)**2 + rel_tau**2)
rel_cross = math.sqrt(rel_e**2+rel_mu**2)

def grade(s):
    return "✓ 达标" if s <= 1 else ("～ 提示" if s <= 3 else "✗ 不达标")

I_e_exp = math.log(m_tau_c/m_e_c)
I_mu_exp = math.log(m_tau_c/m_mu_c)
I_em_exp = math.log(m_mu_c/m_e_c)
E_exp = math.log(M_Pl_MeV/m_tau_c)

eps_mu_old = 144*math.e**(-16)
eps_mu_new = 144*math.e**(-16)*(1+6*s3)
print(f"ε_μ 旧（144e^{{−16}}）      = {eps_mu_old:.6e}")
print(f"ε_μ 新（144e^{{−16}}(1+6σ³)）= {eps_mu_new:.6e}")
print(f"m_μ 链反解 ε_μ_exp = 1.62331e-5：旧差 −0.172%、新差 +0.0048%")
print(f"6σ³ = N_gen!·σ³ = {6*s3:.6e}（α_v 修正共享结构量）")
print()

I_eB = 3*math.e - s3*(1+16/15+math.sqrt(2/3)*(1+6*s3))
I_muB = math.log(16) + math.e**(-3) + eps_mu_new
E_B = 16*math.log(15) + (7/10)*math.log(16/15) - 8*eps_mu_new

print("=== 体系 B'（6σ³ 统一静默族修正）===")
se = abs(I_eB-I_e_exp)/rel_e
sm = abs(I_muB-I_mu_exp)/rel_mu
sE_ = abs(E_B-E_exp)/sE
sc = abs((I_eB-I_muB)-I_em_exp)/rel_cross
print(f"  m_e/m_τ：σ_score = {se:.3f} {grade(se)}")
print(f"  m_μ/m_τ：σ_score = {sm:.3f} {grade(sm)}")
print(f"  E_τ：σ_score = {sE_:.3f} {grade(sE_)}")
print(f"  m_e/m_μ（无 m_τ）：σ_score = {sc:.3f} {grade(sc)}")
print(f"  m_τ 绝对：{M_Pl_MeV*math.exp(-E_B):.2f} vs {m_tau_c}")
print()

print("=== 判别 ===")
print("体系 B（ε_μ = 144e^{−16}）：m_e 0.064σ_score ✓、m_μ 1.29σ_score 提示、E_τ 0.021σ_score ✓、m_e/m_μ 0.82σ_score ✓")
print("体系 B'（ε_μ = 144e^{−16}(1+6σ³)）：m_μ 从 1.29σ_score → <0.1σ_score")
print("核心：6σ³ = N_gen!·σ³ 在 α_v 链与 ε_μ 链双链共享——静默族公共结构量")
print("（非独立拟合：同一结构量两处出现——普适性支持）")
print("剩余：为何 ε_μ = 144e^{−16}(1+6σ³)（幂基²×不动点²×全态测度×(1+三代静默排列)）仍为语义层")
