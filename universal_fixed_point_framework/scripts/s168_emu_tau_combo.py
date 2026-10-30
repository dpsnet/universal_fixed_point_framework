# -*- coding: utf-8 -*-
"""S168 候选：E_μ = I_μ + E_τ（先证伪——σ_score 判定）
E_μ(obs)=46.196241、σ_rel(μ)=2.2e-8（S129 勘误口径）
I_μ = e + 42·e^{-6}（S156——间隔级命中 0.039σ）
E_τ = 43.373849（S108 框架组装——0.0000σ）
观察：E_μ(obs) - I_μ ≈ 43.373849 = E_τ(obs)
"""
import math

print("=== S168: E_μ = I_μ + E_τ 候选验证（先证伪） ===\n")

e = math.e
I_mu = e + 42 * e**(-6)
E_tau_obs = 43.373849
E_mu_obs = 46.196241
sigma_rel_mu = 2.2e-8

print(f"e         = {e:.12f}")
print(f"I_μ       = {I_mu:.12f}  (e + 42·e^-6)")
print(f"E_τ(obs)  = {E_tau_obs:.12f}")
print(f"I_μ+E_τ   = {I_mu + E_tau_obs:.12f}")
print(f"E_μ(obs)  = {E_mu_obs:.12f}")
diff = abs((I_mu + E_tau_obs) - E_mu_obs)
sigma_score = diff / sigma_rel_mu
print(f"\n|I_μ+E_τ − E_μ| = {diff:.3e}")
print(f"σ_score = {sigma_score:.3f}  (σ_rel(μ)=2.2e-8)")
print(f"判定：{('达标 ≤1σ' if sigma_score <= 1 else ('提示 1-3σ' if sigma_score <= 3 else '不达标 >3σ'))}")

# 反向：E_τ 由 E_μ − I_μ 反推
print(f"\nE_μ(obs) − I_μ = {E_mu_obs - I_mu:.12f}")
print(f"E_τ(obs)       = {E_tau_obs:.12f}")
print(f"差值 = {(E_mu_obs - I_mu) - E_tau_obs:.3e}")

# 分解：E_τ = 43.373849 的框架形态（S108——0.0000σ）
print(f"\n=== E_τ 框架形态衔接 ===")
print(f"42 + 1.373849（约束域 42 + 余项 1.373849）")
print(f"1.373849 = e/2 - 0.011663（e/2=1.3591409）——非精确")
print(f"43.373849 / 42 = {43.373849/42:.6f}（≈ 1.03271）")
print(f"43.373849 = 16 + 27.373849（幂基平方 16）")
print(f"43.373849 ≈ 3e² + 21.24（3e²=22.167）——非精确")
print(f"→ E_τ 的精确框架形态待 S108 原文（0.0000σ 已成立——")
print(f"  本探索只验证 E_μ = I_μ + E_τ 的组合结构）")
