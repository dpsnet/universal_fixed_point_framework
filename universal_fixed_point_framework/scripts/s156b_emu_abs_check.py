# -*- coding: utf-8 -*-
"""S156b E_μ 绝对值级判别修正（σ_score 纪律）
I_μ 候选（间隔级 0.039σ——合成 σ_I ≈ σ_τ）——但组装 E_μ = E_τ^D + I_μ
预测 E_μ 绝对值——必须用 E_μ 的合成不确定度（σ_rel μ = 2.2e-8）！
"""
import math

E_tau_D = 43.3738491071
I_mu_cand = math.e + 42 * math.exp(-6)
E_mu_pred = E_tau_D + I_mu_cand

# E_μ(obs)（m_μ = 105.6583755(23) MeV——M_Pl = 1.220890e22 MeV）
m_mu = 105.6583755
M_Pl = 1.220890e22
E_mu_obs = -math.log(m_mu / M_Pl)

sigma_mu = 2.2e-8          # σ_rel(μ)——PDG 2024
sigma_tau = 6.75e-5        # σ_rel(τ)
sigma_I = math.sqrt(sigma_mu**2 + sigma_tau**2)  # 间隔合成

print("=== S156b: E_μ 绝对值级判别 ===\n")
print(f"E_τ^D = {E_tau_D:.10f}（S108 四阶截断）")
print(f"I_μ 候选 = e + 42·e^{{-6}} = {I_mu_cand:.10f}")
print(f"E_μ(pred) = E_τ^D + I_μ 候选 = {E_mu_pred:.10f}")
print(f"E_μ(obs)  = −ln(m_μ/M_Pl) = {E_mu_obs:.10f}")
diff = abs(E_mu_pred - E_mu_obs)
print(f"差 = {diff:.3e}")

print(f"\n【口径判别】")
print(f"间隔级：|ΔI_μ| = 2.605e-6 / σ_I = {sigma_I:.2e} = {2.605e-6/sigma_I:.3f}σ（达标）")
print(f"绝对值级：|ΔE_μ| = {diff:.3e} / σ_rel(μ) = {sigma_mu:.2e} = {diff/sigma_mu:.1f}σ（不达标！）")
print(f"\n→ 理论公式 E_μ = E_τ^D + e + 42·e^{{-6}} 预测的是 E_μ 绝对值——")
print(f"  必须用 μ 精度（2.2e-8）——{diff/sigma_mu:.1f}σ 不达标")
print(f"→ I_μ 候选降级：间隔级观察（0.039σ）——不升格为质量谱绝对值组装")
print(f"→ 质量谱绝对值达标链维持：E_e（0.001σ——S145b）/E_τ（0.0000σ——S108）")
