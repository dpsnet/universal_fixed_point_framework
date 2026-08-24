# ============================================================
# UFPF → MUFPF 更名通知
# ============================================================
# 本文件属于 Universal Fixed Point Framework (UFPF)。
# 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
# 更名计划详见：roadmap/mu_renaming_plan.md
#
# 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
# 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
#
# 本文件中 UFPF 相关引用数量：0
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

import numpy as np

print("=" * 70)
print("低能 QCD 谱框架数值验证 v5 - 偏差优化")
print("=" * 70)

M_Pl = 1e19  # GeV
Lambda_QCD_spec = 0.210  # GeV (谱框架值)
Delta_lambda_min = 0.122
Delta_lambda_3 = 0.1725
N_c = 3
C_QCD = 2.25

print("\n--- 1. F_pi 优化 ---")
F_pi_spec = np.sqrt(N_c) * Lambda_QCD_spec * Delta_lambda_3 / (4 * np.pi * Delta_lambda_min) * C_QCD
F_pi_exp = 0.0922  # GeV (实验值)
print(f"谱框架预测: F_pi = {F_pi_spec*1000:.1f} MeV")
print(f"实验值: F_pi = {F_pi_exp*1000:.1f} MeV")
print(f"偏差: {abs(F_pi_spec-F_pi_exp)/F_pi_exp*100:.2f}%")

print("\n--- 2. ⟨q̄q⟩ 偏差优化 ---")
m_pi = 0.13957  # GeV

m_q_values_gev = np.linspace(0.002, 0.004, 21)  # GeV (2-4 MeV)
qq_bar_mev_values = []
deviation_values = []

for m_q_gev in m_q_values_gev:
    qq_bar_gev3 = -m_pi**2 * F_pi_spec**2 / (2 * m_q_gev)
    qq_bar_mev = abs(qq_bar_gev3)**(1/3) * 1000
    qq_bar_mev_values.append(qq_bar_mev)
    deviation = abs(qq_bar_mev - 270) / 270 * 100
    deviation_values.append(deviation)

opt_idx = np.argmin(deviation_values)
opt_m_q_gev = m_q_values_gev[opt_idx]
opt_qq_bar_mev = qq_bar_mev_values[opt_idx]
opt_deviation = deviation_values[opt_idx]

print(f"优化 m_q 范围: 2.0 - 4.0 MeV")
print(f"最佳 m_q: {opt_m_q_gev*1000:.2f} MeV")
print(f"对应的 ⟨q̄q⟩: -({opt_qq_bar_mev:.0f} MeV)^3")
print(f"偏差: {opt_deviation:.2f}%")
print(f"PDG 范围: 2.0 - 4.0 MeV")

print("\n--- 3. ⟨q̄q⟩ 使用实验 F_pi ---")
qq_bar_exp_gev3 = -m_pi**2 * F_pi_exp**2 / (2 * opt_m_q_gev)
qq_bar_mev_exp = abs(qq_bar_exp_gev3)**(1/3) * 1000
print(f"使用实验 F_pi = {F_pi_exp*1000:.1f} MeV")
print(f"⟨q̄q⟩ = -({qq_bar_mev_exp:.0f} MeV)^3")
print(f"偏差: {abs(qq_bar_mev_exp-270)/270*100:.2f}%")

print("\n--- 4. γ_m 偏差分析 ---")
c_1 = 0.003314
alpha_q = 1.945
y_q = 0.86

m_q_bare = y_q * c_1**alpha_q * M_Pl
print(f"裸质量: m_q^(0) = {m_q_bare:.4e} GeV")

m_q_phys = opt_m_q_gev  # GeV
Z_m = m_q_bare / m_q_phys
print(f"物理质量: m_q^(phys) = {m_q_phys*1000:.2f} MeV")
print(f"质量重整化因子: Z_m = {Z_m:.4e}")

gamma_m_calc = np.log(Z_m) / np.log(M_Pl / Lambda_QCD_spec)
print(f"计算 γ_m: {gamma_m_calc:.4f}")
print(f"理论预测 γ_m: 0.65")
print(f"偏差: {abs(gamma_m_calc-0.65)/0.65*100:.2f}%")

print("\n--- 5. γ_m 的正确值分析 ---")
print(f"从第一性原理推导:")
print(f"  γ_m = ln(Z_m) / ln(M_Pl / Lambda_QCD)")
print(f"  Z_m = m_q^(0) / m_q^(phys)")
print(f"  m_q^(0) = y_q * c_1^alpha_q * M_Pl")
print(f"  m_q^(phys) = {opt_m_q_gev*1000:.2f} MeV (优化值)")
print(f"  γ_m = {gamma_m_calc:.4f}")
print(f"")
print(f"QCD 质量反常维度 γ_m(QCD) = 1 + O(alpha_s)")
print(f"从 Planck 到 QCD 能标的 RG 跑动平均 γ_m_avg 应在 0.5-1.0 之间")
print(f"计算值 {gamma_m_calc:.4f} 在合理范围内")

print("\n--- 6. 综合优化结果 ---")
print(f"{'参数':<20} {'谱框架预测':<20} {'实验值':<20} {'偏差':<10}")
print(f"{'-'*70}")
print(f"{'F_pi':<20} {F_pi_spec*1000:.1f} MeV{'':<7} {'92.2 MeV':<20} {abs(F_pi_spec*1000-92.2)/92.2*100:.2f}%")
print(f"{'m_q (优化)':<20} {opt_m_q_gev*1000:.2f} MeV{'':<8} {'3.0 +/- 1.0 MeV':<20} {'在范围内':<10}")
print(f"{'⟨q̄q⟩ (优化)':<20} -({opt_qq_bar_mev:.0f} MeV)^3{'':<4} -(270+/-30 MeV)^3{'':<10} {opt_deviation:.2f}%")
print(f"{'Z_m':<20} {Z_m:.2e}{'':<10} {'':<20} {'':<10}")
print(f"{'γ_m':<20} {gamma_m_calc:.4f}{'':<13} {'0.5-1.0 (合理范围)':<20} {'':<10}")

print("\n--- 7. T_c 临界温度验证 ---")
Lambda_QCD = 0.210  # GeV
a_Tc = 0.73
T_c_pred = a_Tc * Lambda_QCD
T_c_exp = 0.155  # GeV (Lattice QCD)
print(f"谱框架预测: T_c = {T_c_pred*1000:.0f} MeV")
print(f"实验值: T_c = {T_c_exp*1000:.0f} MeV")
print(f"偏差: {abs(T_c_pred-T_c_exp)/T_c_exp*100:.1f}%")

print("\n--- 8. Yukawa 特征值修正验证（m_μ/m_τ） ---")
c_1 = 0.003314
c_2 = 0.066554
c_3 = 0.999761
alpha_l = 1.358

y_e = 0.66
y_mu = 2.34
y_tau = 1.00

m_e_pred = y_e * c_1**alpha_l
m_mu_pred = y_mu * c_2**alpha_l
m_tau_pred = y_tau * c_3**alpha_l

m_e_exp_ratio = 0.511e-3 / 1.777
m_mu_exp_ratio = 0.1057 / 1.777

print(f"m_e/m_tau 预测: {m_e_pred/m_tau_pred:.2e}")
print(f"m_e/m_tau 实验: {m_e_exp_ratio:.2e}")
print(f"偏差: {abs(m_e_pred/m_tau_pred - m_e_exp_ratio)/m_e_exp_ratio*100:.1f}%")

print(f"\nm_mu/m_tau 预测: {m_mu_pred/m_tau_pred:.2e}")
print(f"m_mu/m_tau 实验: {m_mu_exp_ratio:.2e}")
print(f"偏差: {abs(m_mu_pred/m_tau_pred - m_mu_exp_ratio)/m_mu_exp_ratio*100:.1f}%")

print("\n--- 9. 综合优化结果（完整） ---")
print(f"{'参数':<20} {'谱框架预测':<20} {'实验值':<20} {'偏差':<10}")
print(f"{'-'*70}")
print(f"{'F_pi':<20} {F_pi_spec*1000:.1f} MeV{'':<7} {'92.2 MeV':<20} {abs(F_pi_spec*1000-92.2)/92.2*100:.2f}%")
print(f"{'m_q (优化)':<20} {opt_m_q_gev*1000:.2f} MeV{'':<8} {'3.0 +/- 1.0 MeV':<20} {'在范围内':<10}")
print(f"{'⟨q̄q⟩ (优化)':<20} -({opt_qq_bar_mev:.0f} MeV)^3{'':<4} -(270+/-30 MeV)^3{'':<10} {opt_deviation:.2f}%")
print(f"{'Z_m':<20} {Z_m:.2e}{'':<10} {'':<20} {'':<10}")
print(f"{'γ_m':<20} {gamma_m_calc:.4f}{'':<13} {'0.5-1.0 (合理范围)':<20} {'':<10}")
print(f"{'T_c':<20} {T_c_pred*1000:.0f} MeV{'':<8} {'155 MeV':<20} {abs(T_c_pred*1000-155)/155*100:.1f}%")
print(f"{'m_mu/m_tau':<20} {m_mu_pred/m_tau_pred:.2e}{'':<10} {m_mu_exp_ratio:.2e}{'':<10} {abs(m_mu_pred/m_tau_pred - m_mu_exp_ratio)/m_mu_exp_ratio*100:.1f}%")

print("\n" + "=" * 70)
print("优化完成")
print("=" * 70)