# -*- coding: utf-8 -*-
# S108 E_τ 框架组装连接先证伪（2026-10-27）
# 候选：E_τ（框架生成——AlphaChain——16·ln15 + (7/10)·ln(16/15)——全框架量）
#   ⟺ −ln(m_τ/M_Pl)（S107 模流对数——实验质量）
# 若差在 σ_score ≤ 1 内——"质量谱第一个框架生成的 E 值"从判别级升格

from math import log

# 框架常数
ln15 = log(15)          # ln(σ⁻¹)——静默窗口对数
ln16_15 = log(16/15)    # ln(1+σ)——σ 修正对数
E_tau_fw = 16*ln15 + (7/10)*ln16_15
print(f"E_τ(框架) = 16·ln15 + (7/10)·ln(16/15) = {E_tau_fw:.10f}")
print(f"  主项 16·ln15 = {16*ln15:.10f}  修正 (7/10)·ln(16/15) = {0.7*ln16_15:.10f}")

# 实验：m_τ = 1776.86 MeV、M_Pl = 1.220890e22 MeV
m_tau = 1776.86
M_Pl = 1.220890e22
E_tau_obs = -log(m_tau / M_Pl)
print(f"E_τ(观测) = −ln(m_τ/M_Pl) = {E_tau_obs:.10f}")

diff = E_tau_fw - E_tau_obs
print(f"\n差 = E_τ(框架) − E_τ(观测) = {diff:.8f}")
print(f"相对差 = {abs(diff)/E_tau_obs*100:.4f}%  = {abs(diff)/E_tau_obs:.2e}")

# σ_score：m_τ 相对不确定度 6.75e-5（PDG 2024 主导瓶颈）
# E 的相对不确定度 ≈ m 的相对不确定度（E = −ln(m/M_Pl)——dE = −dm/m）
sigma_rel = 6.75e-5
sigma_score = abs(diff) / (E_tau_obs * sigma_rel)
print(f"σ_score = |框架−观测|/(E·σ_rel) = {sigma_score:.3f}（σ_rel = {sigma_rel}）")
print(f"达标（≤1）？ {sigma_score <= 1}")

# 口径核查：E_τ^new（#74——含 8ε_μ 修正——σ_score 0.018 版本）
# E_τ^new = E_τ − 8·ε_μ？——ε_μ 修正量
print(f"\n=== 框架组件核查（全框架量） ===")
print(f"16 = 2⁴（全态窗口——Cl(1,3)）")
print(f"ln15 = ln(σ⁻¹)——静默窗口对数（S104——15 = orbitCount）")
print(f"7/10 = (k_max−1)/(N_gen+k_max−1) = (8−1)/(3+8−1)（Etau_ratio_seven_tenths_id——已机检）")
print(f"ln(16/15) = ln(1+σ)——σ 修正对数")
print(f"⟹ E_τ = −16·ln σ + (7/10)·ln(1+σ)——纯静默窗口/σ 结构")
