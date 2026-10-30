# -*- coding: utf-8 -*-
"""S172 E_μ 口径复核——σ_score 合成不确定度重判
修正：σ_rel 是相对不确定度——绝对不确定度 = 值×σ_rel
E_μ = E_τ + I_μ 组合（I_μ = e + 42·e^{-6}）——重判
"""
import math

print("=== S172: E_μ 口径复核（合成不确定度重判） ===\n")

e = math.e
I_mu = e + 42 * e**(-6)
E_tau_obs = 43.373849
E_mu_obs = 46.196241

# PDG 相对不确定度（S129/S132 勘误口径）
sig_rel_e = 2.94e-10
sig_rel_mu = 2.2e-8
sig_rel_tau = 6.75e-5

# 绝对不确定度
sig_e_abs = 51.527839889074 * sig_rel_e
sig_mu_abs = E_mu_obs * sig_rel_mu
sig_tau_abs = E_tau_obs * sig_rel_tau

print(f"I_μ     = {I_mu:.10f}  (e + 42·e^-6)")
print(f"E_μ(obs)= {E_mu_obs:.6f}")
print(f"E_τ(obs)= {E_tau_obs:.6f}")
print(f"间隔 E_μ−E_τ = {E_mu_obs - E_tau_obs:.10f}")
print(f"|I_μ − 间隔| = {abs(I_mu - (E_mu_obs - E_tau_obs)):.3e}")

print(f"\n=== 绝对不确定度（值×σ_rel——修正口径） ===")
print(f"σ_e,abs  = {sig_e_abs:.3e}  (51.53×2.94e-10)")
print(f"σ_μ,abs  = {sig_mu_abs:.3e}  (46.20×2.2e-8)")
print(f"σ_τ,abs  = {sig_tau_abs:.3e}  (43.37×6.75e-5)")

# 判定 A：E_μ 组装对 E_μ 观测——用 E_μ 自身绝对误差
diff = abs((E_tau_obs + I_mu) - E_mu_obs)
print(f"\n=== 判定 A：E_μ = E_τ+I_μ vs E_μ(obs) ===")
print(f"|E_τ+I_μ − E_μ| = {diff:.3e}")
print(f"σ_score(用σ_μ,abs) = {diff/sig_mu_abs:.3f}  → {'达标≤1σ' if diff/sig_mu_abs<=1 else ('提示1-3σ' if diff/sig_mu_abs<=3 else '不达标>3σ')}")

# 判定 B：合成不确定度（E_τ 观测误差主导——I_μ 框架量精确）
sig_synth = math.sqrt(sig_tau_abs**2 + 0**2)
print(f"\n=== 判定 B：合成不确定度口径（预测=E_τ_obs+I_μ_frame） ===")
print(f"σ_synth = {sig_synth:.3e}（E_τ 观测误差主导——I_μ 框架量 0 误差）")
print(f"σ_score(合成) = {diff/sig_synth:.4f}  → {'达标≤1σ' if diff/sig_synth<=1 else ('提示1-3σ' if diff/sig_synth<=3 else '不达标>3σ')}")

# 判定 C：间隔级（E_μ−E_τ vs I_μ）
print(f"\n=== 判定 C：间隔级（I_μ vs E_μ−E_τ） ===")
sig_interval = math.sqrt(sig_mu_abs**2 + sig_tau_abs**2)
print(f"σ_interval = {sig_interval:.3e}")
print(f"σ_score(间隔) = {abs(I_mu-(E_mu_obs-E_tau_obs))/sig_interval:.4f}  → {'达标≤1σ' if abs(I_mu-(E_mu_obs-E_tau_obs))/sig_interval<=1 else ('提示1-3σ' if abs(I_mu-(E_mu_obs-E_tau_obs))/sig_interval<=3 else '不达标>3σ')}")

print("\n=== 结论 ===")
print("  S156b 的 '118.3σ 绝对值不达标' = 2.58e-6/2.2e-8——")
print("    把相对不确定度当绝对用——**口径错误**")
print("  正确：σ_μ,abs = 46.2×2.2e-8 = 1.02e-6")
print("  判定 A（E_μ 自身误差）：2.5σ——提示级")
print("  判定 B（合成——E_τ 误差主导）：0.0009σ——达标")
print("  判定 C（间隔 E_μ−E_τ）：0.0009σ——达标")
print("  → E_μ = E_τ + I_μ 组合成立（取决于口径）——")
print("    E_μ 从'不达标'修正为'达标/提示级'候选")
print("  ⚠ 诚实警示：差 2.58e-6 完全由 I_μ 候选残余决定——")
print("    组合达标依赖 I_μ 精确度（当前差在 τ 误差内）——")
print("    结构 E_μ=E_τ+I_μ 保留——I_μ 残余 2.58e-6 待解释")
