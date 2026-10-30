me = 0.51099895
L = 210.219
mud = me*27/4
kappa = 6/3.141592653589793
sigma = 1/15
dress = kappa*L*(1-2*sigma/3)
Mud_eff = mud + dress
m_rho = 2*Mud_eff

pdg_rho = 775.26   # PDG 2024 rho0 e+e-：775.26 +- 0.23
print("m_rho =", m_rho, " vs PDG", pdg_rho, " =", (m_rho-pdg_rho)/pdg_rho*100, "%")
gap = pdg_rho - m_rho
print("缺口 =", gap, " gap/L =", gap/L)

# 候选：1/196 = 1/(4*(k_max-1)^2) = 1/(4*49)
c1 = L/196
print("Lambda/196 =", c1, " dev =", (c1-gap)/gap*100, "%")
print("m_rho' =", m_rho+c1, " vs PDG =", (m_rho+c1-pdg_rho)/pdg_rho*100, "%")

# 对比：Delta_lambda_min/24
import math
dlmin = (math.sqrt(3)-1)/6
c2 = dlmin*L/24 if False else L*(dlmin/24)
# 实际：Delta_lambda_min/24 是 gap/L 的候选
c2b = dlmin/24
print("dlmin/24 =", c2b, " vs gap/L =", gap/L, " dev =", (c2b-gap/L)/(gap/L)*100, "%")

# 大缺口/64、/100 对比
b0gap = L*9/25
print("b0gap/64 =", b0gap/64, " dev =", (b0gap/64-gap)/gap*100, "%")
print("b0gap/100 =", b0gap/100, " dev =", (b0gap/100-gap)/gap*100, "%")

# Lambda 双口径摆动（210.0 vs 210.3）
for L2 in [210.0, 210.3]:
    dress2 = kappa*L2*(1-2*sigma/3)
    rho2 = 2*(mud+dress2)
    g2 = pdg_rho - rho2
    print("L =", L2, " m_rho =", rho2, " 缺口 =", g2, " vs L2/196 =", L2/196, " dev =", (L2/196-g2)/g2*100, "%")
