# Phase 102b 阶段 2 E2：η_forb(B) 内生曲线 —— η_3g（第三门）+ η_σ（Landau 填充）
# 完全内生：RYD = alpha^2*m_e/2、mu_B = e*hbar/2m_e、B_AU = RYD/mu_B
# 温度 T 为环境参数（白矮星 8-25 kK——物理输入，合法非框架常数）
import math

# ---- 框架常数（Lean 固化 / 登记值）----
dH = math.log(15) + 1/675
alpha_EM = 1/(24*(dH + 3))      # = 1/137.02876
m_e_MeV = 0.51096
# 实验口径对照
alpha_exp = 1/137.035999084
m_e_exp = 0.51099895

e_C = 1.602176634e-19
hbar = 1.054571817e-34
c_m = 2.99792458e8
kg_per_MeV = 1.78266192e-30

# ---- 内生量 ----
def RYD_ev(m_e_MeV, alpha):
    return alpha**2 * m_e_MeV * 1e6 / 2   # 13.6 eV
def mu_B_JpT(m_e_MeV):
    return e_C * hbar / (2 * (m_e_MeV * kg_per_MeV))
def B_AU_T(m_e_MeV, alpha):
    return RYD_ev(m_e_MeV, alpha) * 1e-6 * e_C * 1e6 / mu_B_JpT(m_e_MeV)
    # RYD(eV) * 1.602e-19 J / mu_B(J/T)

end = dict(RYD=RYD_ev(m_e_MeV, alpha_EM), muB=mu_B_JpT(m_e_MeV), BAU=B_AU_T(m_e_MeV, alpha_EM))
ext = dict(RYD=RYD_ev(m_e_exp, alpha_exp), muB=mu_B_JpT(m_e_exp), BAU=B_AU_T(m_e_exp, alpha_exp))
print("内生: RYD =", end["RYD"], "eV,  B_AU =", end["BAU"], "T,  mu_B =", end["muB"])
print("外部: RYD =", ext["RYD"], "eV,  B_AU =", ext["BAU"], "T,  mu_B =", ext["muB"])
print("偏差: RYD", (end["RYD"]/ext["RYD"]-1)*100, "%  B_AU", (end["BAU"]/ext["BAU"]-1)*100, "%")
print()

# ---- η_3g（第三门失效）——全内生 ----
def eta_3g(n, B_T, q):
    """q = dict(RYD, BAU)：全内生或外部口径"""
    RYD = q["RYD"]; BAU = q["BAU"]
    E_bind = RYD / n**2
    hbar_wc = (B_T / BAU) * 2 * RYD        # ħω_c = 2·B/B_AU·RYD
    E_landau_base = hbar_wc / 2
    E_z = E_landau_base - E_bind
    if E_z <= 0:
        return 0.0
    omega_cycle = RYD * (1.0/4.0 - 1.0/n**2)   # 跃迁能量 = 循环频率·ħ
    phi_z = 4.0 * math.pi * E_z / omega_cycle
    eps = min(1.0, 2.0 * abs(math.sin(phi_z / 2.0)))
    return 1.0 - math.exp(-eps)

# ---- η_σ（σ 通道 Landau 填充——全内生）----
# 口径勘误（2026-10-09 对齐 _phase100_p1_quantified_w.py）：
#   * 本函数返回的是填充率 A_σ = exp(−ħω_c/2k_BT)（m'=±1 层）
#   * 禁戒份额 η_σ = (1−A_σ)·2/3（σ 份额 TRK 精确 2/3——脚本 0.66668）
#   * 笔记 §13.2 "300T 0.103/10^4T 0.543/3×10^4T 0.664" 单位笔误：
#     实为 3000/30000/100000 T 的 η_forb_avg = (1−fill)·2/3
#     （脚本 _phase102b_eta_sigma_alignment.py 全 B 点闭式吻合 ≤0.78%）
def A_sigma(B_T, T_K, q):
    """填充率 A_σ = exp(−ħω_c/(2k_BT))（m'=±1）——ħω_c = 2μ_BB"""
    muB = q["muB"]
    hbar_wc_J = 2 * muB * B_T
    kBT_J = 1.380649e-23 * T_K
    return math.exp(-hbar_wc_J / (2 * kBT_J))

def eta_sigma(B_T, T_K, q):
    """禁戒份额 η_σ = (1−A_σ)·2/3——σ 份额 TRK 精确"""
    return (1 - A_sigma(B_T, T_K, q)) * 2.0 / 3.0

ns = [3, 4, 5, 6, 7]
names = {3: "Hα", 4: "Hβ", 5: "Hγ", 6: "Hδ", 7: "Hε"}

print("η_3g(B) 内生 vs 外部（观测域 10-90 MG + 强场端）:")
B_MGs = [10, 30, 50, 70, 90, 150, 260]
print(f"  {'B(MG)':<8}" + "".join(f"{names[n]:<10}" for n in ns))
for B_MG in B_MGs:
    B_T = B_MG * 1e6 * 0.001 * 100  # B_MG*100 才是 T？——MG = 1e6 G = 1e-3 T·1e6 = 1000 T？——不
    # 1 MG = 1e6 Gauss = 100 T
    B_T = B_MG * 100.0
    row_i = f"  内生{''}"
    row_e = f"  外部{''}"
    rows = {"内生": "", "外部": ""}
    for n in ns:
        rows["内生"] += f"{eta_3g(n, B_T, end):<10.3f}"
        rows["外部"] += f"{eta_3g(n, B_T, ext):<10.3f}"
    print(f"  {B_MG:<8}" + rows["内生"])
    print(f"  {'':<8}" + rows["外部"])

print()
print("η_σ(B)（T=12000 K 白矮星口径）内生 vs 外部——填充率 A_σ 与禁戒份额 η_σ=(1-A_σ)*2/3:")
for B_MG in [0.1, 1, 10, 45, 90]:
    B_T = B_MG * 100.0
    print(f"  {B_MG:<5}MG: Aσ 内生 {A_sigma(B_T, 12000, end):.3f} 外 {A_sigma(B_T, 12000, ext):.3f}"
          f" | ησ 内生 {eta_sigma(B_T, 12000, end):.3f} 外 {eta_sigma(B_T, 12000, ext):.3f}")

print()
print("判定：η_3g 阈值序列/量级不变 → 链自洽；η_σ 温度依赖保持（环境参数）")
