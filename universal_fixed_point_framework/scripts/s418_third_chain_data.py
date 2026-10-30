# -*- coding: utf-8 -*-
"""S418 第三链最新实验数据核算（2026-10-29）
CODATA 2022（NIST 2024-05 发布）+ PDG 2026 轻子质量
vs MUFPF 预言——σ_score 全口径核算
MUFPF 预言：
  α⁻¹ = 72+24ln15+24δ* = 137.035999083426（0.0273σ@2018）
  轻子比值：m_τ/m_μ = e^{I_μ} = 16.8170298348
            m_e/m_μ = e^{−(I_e−I_μ)} = 0.0048363318
            m_τ/m_e = e^{E_e−E_τ^D} = 3477.2284077
"""
import math

print("=== S418 第三链最新实验数据核算 ===")
print()

# MUFPF 预言
alpha_inv_pred = 72 + 24*math.log(15) + 24*(6*(1/15)**3 + 4*(1/15)**5 + 8*(1/15)**7 + 5*(1/15)**8)
I_mu = math.e + 42*math.e**(-6) + 2*(1/15)**5
I_e = 3*math.e - (1/15)**3 * (1 + 16/15 + math.sqrt(2/3)*(1+6*(1/15)**3))
E_e = 16*math.log(15) + (7/10)*math.log(16/15) - 8*144*math.e**(-16) - ((1/15)**5 - math.e**(-16)) - 2*(1/15)**8*(1+1/15) + I_e - (27/80)*math.e**(-19)
E_tau = 16*math.log(15) + (7/10)*math.log(16/15) - 8*144*math.e**(-16) - ((1/15)**5 - math.e**(-16)) - 2*(1/15)**8*(1+1/15)
print(f"[0] MUFPF 预言：")
print(f"  α⁻¹ = {alpha_inv_pred:.12f}")
print(f"  m_τ/m_μ = e^{{I_μ}} = {math.exp(I_mu):.10f}")
print(f"  m_e/m_μ = e^{{-(I_e−I_μ)}} = {math.exp(-(I_e-I_mu)):.10f}")
print(f"  m_τ/m_e = e^{{E_e−E_τ^D}} = {math.exp(E_e-E_tau):.10f}")
print(f"  （推导值）m_τ = e^{{I_μ}} × m_μ、m_e = e^{{-(I_e−I_μ)}} × m_μ")
print()

print("[1] α⁻¹ 第三链核算：")
experiments_alpha = [
    ("CODATA 2018（旧达标口径）", 137.035999084, 0.000000021),
    ("CODATA 2022 总平均（NIST 2024-05）", 137.035999177, 0.000000021),
    ("Fan 2023 g-2 独立通道", 137.035999166, 0.000000016),
]
for name, val, unc in experiments_alpha:
    diff = val - alpha_inv_pred
    sigma = abs(diff) / unc
    grade = "达标" if sigma <= 1 else ("提示" if sigma <= 3 else "不达标")
    print(f"  {name}：{val} ± {unc}")
    print(f"    偏差 {diff:+.3e}——σ_score = {sigma:.2f}——{grade}")
print()

print("[2] 轻子比值第三链核算（PDG 2026）：")
m_e_exp, ue = 0.51099895069, 0.00000000016   # MeV（1.6e-10）
m_mu_exp, umu = 105.6583755, 0.0000023       # MeV（2.3e-9）
m_tau_exp, utau = 1776.93, 0.09              # MeV（PDG 2026 更新！）
print(f"  PDG 2026：m_e = {m_e_exp}±{ue}、m_μ = {m_mu_exp}±{umu}、m_τ = {m_tau_exp}±{utau}")
print()
r_tm_exp = m_tau_exp / m_mu_exp
r_tm_unc = r_tm_exp * math.sqrt((utau/m_tau_exp)**2 + (umu/m_mu_exp)**2)
r_tm_pred = math.exp(I_mu)
sigma_tm = abs(r_tm_exp - r_tm_pred) / r_tm_unc
grade_tm = "达标" if sigma_tm <= 1 else ("提示" if sigma_tm <= 3 else "不达标")
print(f"  m_τ/m_μ：实验 {r_tm_exp:.10f}±{r_tm_unc:.2e} vs 预言 {r_tm_pred:.10f}")
print(f"    σ_score = {sigma_tm:.2f}——{grade_tm}")
print()
r_em_exp = m_e_exp / m_mu_exp
r_em_unc = r_em_exp * math.sqrt((ue/m_e_exp)**2 + (umu/m_mu_exp)**2)
r_em_pred = math.exp(-(I_e - I_mu))
sigma_em = abs(r_em_exp - r_em_pred) / r_em_unc
grade_em = "达标" if sigma_em <= 1 else ("提示" if sigma_em <= 3 else "不达标")
print(f"  m_e/m_μ：实验 {r_em_exp:.10f}±{r_em_unc:.2e} vs 预言 {r_em_pred:.10f}")
print(f"    σ_score = {sigma_em:.2f}——{grade_em}")
print()
r_te_exp = m_tau_exp / m_e_exp
r_te_unc = r_te_exp * math.sqrt((utau/m_tau_exp)**2 + (ue/m_e_exp)**2)
r_te_pred = math.exp(E_e - E_tau)
sigma_te = abs(r_te_exp - r_te_pred) / r_te_unc
grade_te = "达标" if sigma_te <= 1 else ("提示" if sigma_te <= 3 else "不达标")
print(f"  m_τ/m_e：实验 {r_te_exp:.10f}±{r_te_unc:.2e} vs 预言 {r_te_pred:.10f}")
print(f"    σ_score = {sigma_te:.2f}——{grade_te}")
print()

print("[3] 绝对质量核算（M_Pl 内锚 m_τ——PDG 2026）：")
# m_τ(fw) = e^{E_τ^D + I_μ}？MUFPF 轻子质量 = 自然单位制（普朗克质量=1）
# 外部经质量锚定：选 m_μ 或 m_τ 作锚。旧审计：绝对质量（M_Pl 经 m_τ 锚定）
# m_τ 预言（锚 m_μ = 105.6583755）：m_τ = e^{I_μ} × m_μ
m_tau_pred = math.exp(I_mu) * m_mu_exp
sigma_tau_abs = abs(m_tau_exp - m_tau_pred) / utau
grade_tau = "达标" if sigma_tau_abs <= 1 else ("提示" if sigma_tau_abs <= 3 else "不达标")
print(f"  m_τ 预言（锚 m_μ）= {m_tau_pred:.4f} MeV vs 实验 {m_tau_exp}±{utau}")
print(f"    σ_score = {sigma_tau_abs:.2f}——{grade_tau}")
print()

print("[4] 通道口径说明：")
print("  CODATA 2022 总平均 137.035999177(21) 为多通道加权：")
print("    · Rb 反冲（Morel 2020）：137.035999206(11)——已知")
print("    · a_e（Fan 2023）：137.035999166(16)——已知")
print("    · Cs 反冲（Parker 2018）：137.035999046(27)——待查")
print("    ——2022 总平均 ≠ 2018 Cs 通道——通道漂移 = 第三链")
print("      关键检验——需查 CODATA 2022 各通道具体值")
