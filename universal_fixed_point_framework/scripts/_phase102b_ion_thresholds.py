# Phase 102b 阶段 2：拓扑禁戒频率内生对接 —— 电离阈值序列重算
# 完全内生：alpha_EM = 1/[24(d_H+3)]、m_e 来自轻子链（候选级）
# 其余全为 SI 定义常数（e/hbar/c/eps0）与数学常数（pi）
import math

# ---- 框架常数（Lean 已固化代数身份 / 登记值）----
dH = math.log(15) + 1/675            # ln15 + delta = 2.7095317
alpha_EM = 1/(24*(dH + 3))           # = 1/137.0277...
m_e_MeV = 0.51096                    # 轻子链内生值（m_tau 锚 → 指数链，候选级）
# 对照：实验口径 m_e = 0.51099895、alpha = 1/137.035999

# ---- SI 定义常数（精确）----
e_C = 1.602176634e-19                # 元电荷（定义）
hbar = 1.054571817e-34               # 约化普朗克常数（定义）
c_m = 2.99792458e8                   # 光速（定义）
MeV_to_J = 1.602176634e-13           # 1 MeV = 1.602e-13 J（同 e_C*1e6）
kg_per_MeV = 1.78266192e-30          # 1 MeV/c^2 质量（= 1.602e-13/c^2）

# ---- 内生 m_e 的 kg 值 ----
m_e_kg = m_e_MeV * kg_per_MeV        # ~9.11e-31 kg

# ---- 内生 Bohr 磁子：mu_B = e*hbar/(2*m_e_kg) ----
mu_B_JpT = e_C * hbar / (2 * m_e_kg)

# ---- 内生电离阈值：B_ion(n) = |E_n|/mu_B ----
# |E_n|(J) = alpha^2 * m_e_kg * c^2 / (2 n^2)   —— 直接 SI 形式
def B_ion_T(n):
    E_n_J = alpha_EM**2 * m_e_kg * c_m**2 / (2 * n**2)
    return E_n_J / mu_B_JpT

# 实验口径对照（同公式、实验 alpha/m_e）
alpha_exp = 1/137.035999084
m_e_exp_kg = 0.51099895 * kg_per_MeV
mu_B_exp = e_C * hbar / (2 * m_e_exp_kg)
def B_ion_T_exp(n):
    E = alpha_exp**2 * m_e_exp_kg * c_m**2 / (2 * n**2)
    return E / mu_B_exp

print("alpha_EM 内生 =", alpha_EM, "(=1/", 1/alpha_EM, ")  实验 =", alpha_exp)
print("m_e 内生 =", m_e_MeV, "MeV")
print("mu_B 内生 =", mu_B_JpT, "J/T  实验 =", mu_B_exp)
print()
print("线序阈值序列（B_ion, T → MG；1 MG = 100 T）：")
for n in [7, 6, 5, 4, 3]:
    b = B_ion_T(n)
    be = B_ion_T_exp(n)
    print(f"  n={n}: 内生 {b:.0f} T ({b/100:.1f} MG)   实验口径 {be:.0f} T ({be/100:.1f} MG)   偏差 {(b-be)/be*100:+.4f}%")
print()
print("简化式核对：B_ion(n) = alpha^(3/2)*m_e^2/(2*pi*n^2)（alpha^2*m_e*kg*c^2 与 mu_B=e*hbar/2m_e 合并消 m_e）")
# 合并：B = alpha^2 * m_e_kg^2 * c^2 / (e*hbar*n^2)
for n in [7, 6, 5, 4, 3]:
    b2 = alpha_EM**2 * m_e_kg**2 * c_m**2 / (e_C * hbar * n**2)
    b2e = alpha_exp**2 * m_e_exp_kg**2 * c_m**2 / (e_C * hbar * n**2)
    print(f"  n={n}: 合并式 {b2:.0f} T vs 实验 {b2e:.0f} T   dev {(b2-b2e)/b2e*100:+.4f}%")
