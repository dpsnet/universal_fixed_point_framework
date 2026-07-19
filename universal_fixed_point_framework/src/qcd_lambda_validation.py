import math

M_PL = 1.22e19  # GeV
M_Z = 91.1876   # GeV
ALPHA_S_MZ = 0.1179

b1 = 7
b2 = 26
b3 = -109/3

delta_lambda_min = 0.122
delta_lambda_3 = delta_lambda_min * math.sqrt(2)
ALPHA_S_0 = delta_lambda_3 / (4 * math.pi)

ln_ratio = math.log(M_PL / M_Z)
alpha_s_inv_MPl = 1/ALPHA_S_MZ + b1/(2*math.pi) * ln_ratio
alpha_s_MSbar_MPl = 1 / alpha_s_inv_MPl

Z_s = alpha_s_MSbar_MPl / ALPHA_S_0

print("=== 参数输入 ===")
print(f"delta_lambda_min = {delta_lambda_min}")
print(f"delta_lambda_3 = {delta_lambda_3}")
print(f"alpha_s^(0)(M_Pl) = {ALPHA_S_0}")
print(f"alpha_s(M_Z) = {ALPHA_S_MZ}")
print(f"ln(M_Pl/M_Z) = {ln_ratio}")

print("\n=== 方案转换因子 ===")
print(f"alpha_s^MS-bar(M_Pl) = {alpha_s_MSbar_MPl}")
print(f"Z_s = alpha_s^MS-bar / alpha_s^(0) = {Z_s}")

print("\n=== 1-loop RGE 从 M_Pl 跑到 Lambda_QCD ===")
lambda_qcd_1loop = M_PL * math.exp(-2*math.pi/b1 * 1/(Z_s * ALPHA_S_0))
print(f"Lambda_QCD (1-loop, Z_s 修正) = {lambda_qcd_1loop} GeV = {lambda_qcd_1loop * 1e3} MeV")

lambda_qcd_1loop_raw = M_PL * math.exp(-2*math.pi/b1 * 1/ALPHA_S_0)
print(f"Lambda_QCD (1-loop, 未修正) = {lambda_qcd_1loop_raw} GeV = {lambda_qcd_1loop_raw * 1e3} MeV")

print("\n=== 标准 RGE 从 M_Z 跑到 Lambda_QCD（验证）===")
lambda_qcd_std = M_Z * math.exp(-2*math.pi/b1 * 1/ALPHA_S_MZ)
print(f"Lambda_QCD (标准从 M_Z) = {lambda_qcd_std} GeV")

print("\n=== 2-loop RGE ===")
alpha_s_inv = 1/(Z_s * ALPHA_S_0)
x = -1/(Z_s * ALPHA_S_0) / (b1/(2*math.pi) + b2/((2*math.pi)**2) * (Z_s * ALPHA_S_0))
lambda_qcd_2loop = M_PL * math.exp(x)
print(f"Lambda_QCD (2-loop, Z_s 修正) = {lambda_qcd_2loop} GeV = {lambda_qcd_2loop * 1e3} MeV")

print("\n=== 3-loop RGE ===")
alpha_s = Z_s * ALPHA_S_0
denom = b1/(2*math.pi) + b2/((2*math.pi)**2) * alpha_s + b3/((2*math.pi)**3) * alpha_s**2
x3 = -1/alpha_s / denom
lambda_qcd_3loop = M_PL * math.exp(x3)
print(f"Lambda_QCD (3-loop, Z_s 修正) = {lambda_qcd_3loop} GeV = {lambda_qcd_3loop * 1e3} MeV")

print("\n=== F_pi 计算 ===")
N_c = 3
F_pi = math.sqrt(N_c) * lambda_qcd_1loop_raw * 1e3 / (4*math.pi)
print(f"F_pi (1-loop 未修正) = {F_pi} MeV")
F_pi_corr = math.sqrt(N_c) * lambda_qcd_1loop * 1e3 / (4*math.pi)
print(f"F_pi (1-loop Z_s 修正) = {F_pi_corr} MeV")

print("\n=== 手征凝聚 (使用实验输入) ===")
m_pi = 139.57  # MeV
F_pi_exp = 92.2  # MeV
m_q = 3.0      # MeV (PDG)
qq = -m_pi**2 * F_pi_exp**2 / (2 * m_q)
print(f"<q̄q> = -m_pi^2 * F_pi^2 / (2 * m_q) = {qq} MeV^3")
qq_gev = qq / 1e9
print(f"<q̄q> = {qq_gev} GeV^3")
qq_scale = abs(qq)**(1/3)
print(f"|<q̄q>|^(1/3) = {qq_scale} MeV")

print("\n=== c_i 与 <q̄q> 联系 ===")
c1 = 0.003314
alpha_q = 1.229
m_q_planck = c1**alpha_q
print(f"m_q^(0) = c1^alpha_q = {m_q_planck} (Planck 能标)")
Z_m = m_q / m_q_planck / 1e9
print(f"Z_m = m_q^(phys) / m_q^(0) = {Z_m}")