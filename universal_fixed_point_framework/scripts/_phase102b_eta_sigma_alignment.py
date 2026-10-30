# η_σ 口径对齐验证：η_forb(P1) = (1 - fill) * sigma_fraction
# fill = exp(-|m|*omega_c/2/kB/T)，omega_c = 1.16e-4*B eV，m=1，T=12000K
# sigma_fraction = 0.66668（P1 脚本数值——= TRK 2/3）
import math

def fill(B_T, T_K=12000.0):
    omega_c = 1.16e-4 * B_T       # eV（= hbar*eB/m_e）
    dE = 1 * omega_c / 2.0        # |m|=1 层间隔
    kB_T = 8.617333262e-5 * T_K   # eV
    return math.exp(-dE / kB_T)

sf = 2.0/3.0   # sigma_fraction（脚本 0.66668 ≈ 2/3——TRK）

# P1 脚本曲线对照
p1 = {100: 0.0037, 300: 0.0111, 1000: 0.0364, 3000: 0.1032,
      10000: 0.2862, 30000: 0.5428, 100000: 0.6642}
print("B(T)     P1脚本    (1-fill)*2/3   偏差")
for B, eta1 in p1.items():
    eta2 = (1 - fill(B)) * sf
    print(f"{B:7.0f}   {eta1:.4f}      {eta2:.4f}         {(eta1-eta2)/eta1*100:+.2f}%")

# 内生口径（alpha/m_e 框架值——E2 脚本 mu_B 内生）：
# fill = exp(-mu_B*B/kB/T)——mu_B 内生 9.2747e-24 J/T
dH = math.log(15) + 1/675
alpha_EM = 1/(24*(dH+3))
m_e_MeV = 0.51096
e_C = 1.602176634e-19; hbar = 1.054571817e-34
kg_per_MeV = 1.78266192e-30
m_e_kg = m_e_MeV * kg_per_MeV
muB = e_C*hbar/(2*m_e_kg)
kB_J = 1.380649e-23
def fill_end(B_T, T_K=12000.0):
    dE_J = muB * B_T            # |m|=1 Landau 间隔 = mu_B*B（m=1）
    return math.exp(-dE_J/(kB_J*T_K))
print("\n内生口径 η_σ = (1-fill_end)*2/3：")
for B in [300, 1000, 3000, 10000, 30000, 100000]:
    print(f"  B={B:6.0f} T: fill={fill_end(B):.4f}  eta={(1-fill_end(B))*sf:.4f}")

print("\n口径结论：")
print("  1. 笔记 §13.2 '300 T 0.103/10^4 T 0.543/3×10^4 T 0.664' 单位笔误——")
print("     实为 P1 脚本 3000/30000/100000 T 的 η_forb_avg")
print("  2. η_σ（禁戒份额）= (1-fill)·σ_份额——σ_份额 = 2/3（TRK 精确，脚本 0.66668）")
print("  3. E2 脚本 η_σ 标注实为填充率 A_σ（=fill）——非禁戒份额——修标注")
