# Phase 102b 阶段 2 E3：判别预言内生化——ℓ_B 标度、B_crit(ξ=1)、五维判别矩阵
# 全内生：alpha/m_e 框架值 + SI 定义常数；B 为环境坐标（合法非框架常数）
import math

dH = math.log(15) + 1/675
alpha_EM = 1/(24*(dH+3))       # 1/137.02876
m_e_MeV = 0.51096
e_C = 1.602176634e-19
hbar = 1.054571817e-34
c_m = 2.99792458e8
kg_per_MeV = 1.78266192e-30
m_e_kg = m_e_MeV * kg_per_MeV
eps0 = 8.8541878128e-12
# 实验口径
alpha_exp = 1/137.035999084
m_e_exp_kg = 0.51099895 * kg_per_MeV

# ---- 内生基础量 ----
def B_AU_T(m_e_kg, alpha):
    # RYD(J)/mu_B(J/T)：RYD = alpha^2*m_e*c^2/2，mu_B = e*hbar/2m_e
    RYD_J = alpha**2 * m_e_kg * c_m**2 / 2
    muB = e_C * hbar / (2 * m_e_kg)
    return RYD_J / muB

BAU_e = B_AU_T(m_e_kg, alpha_EM)          # 内生 235041 T
BAU_x = B_AU_T(m_e_exp_kg, alpha_exp)

def a0(m_e_kg, alpha):
    return hbar / (m_e_kg * c_m * alpha)   # 玻尔半径（m）
a0e = a0(m_e_kg, alpha_EM); a0x = a0(m_e_exp_kg, alpha_exp)

print(f"B_AU 内生 {BAU_e:.0f} T vs 外部 {BAU_x:.0f} T  dev {(BAU_e/BAU_x-1)*100:+.4f}%")
print(f"a0  内生 {a0e:.3e} m vs 外部 {a0x:.3e} m  dev {(a0e/a0x-1)*100:+.4f}%")
print()

# ---- ℓ_B 标度：ℓ_B = sqrt(hbar/(e*B))——全 SI 定义常数（B 环境坐标）----
def lB(B_T):
    return math.sqrt(hbar / (e_C * B_T))   # m
print("ℓ_B(B)（纯 SI——无框架常数参与——标度律本身即预言）:")
for B in [1e3, 3e3, 1e4, 3e4, 1e5, 2.35e5]:
    print(f"  B={B:8.0f} T: ℓ_B = {lB(B):.3e} m = {lB(B)/a0e:.2f} a₀(内生)")

# ---- 压缩比 ξ(n,B) = n²/ℓ_B（a.u.：ℓ_B 以 a₀ 单位、B 以 B_AU 单位）----
# 内生 a.u. 制：B_au = B_T/BAU、ℓ_B_au = 1/sqrt(B_au)——ξ = n²*sqrt(B_au)
def xi(n, B_T, BAU):
    return n**2 * math.sqrt(B_T / BAU)
names = {3:"Hα",4:"Hβ",5:"Hγ",6:"Hδ",7:"Hε"}
print("\n压缩比 ξ(n,B) @ 30 MG（内生 vs 外部——Phase 100 P4 数值复现）:")
for n, nm in names.items():
    x_e = xi(n, 3e4*0.1*100*10, BAU_e)  # 30 MG = 3e4 T？——1 MG=100 T——30 MG=3000 T
    # 修正：30 MG = 3e4 T？——1 T = 1e-3·1e6 G？——1 MG = 1e6 G = 100 T——30 MG = 3000 T
    x_e = xi(n, 3000, BAU_e)
    x_x = xi(n, 3000, BAU_x)
    print(f"  {nm:3s} n={n}: 内生 {x_e:.2f}   外部 {x_x:.2f}")

# ---- B_crit(ξ=1) = B_AU/n⁴——内生序列（1 MG = 100 T）----
print("\n禁戒临界 B_crit(ξ=1) = B_AU/n⁴（内生——Phase 100 P4 数值复现）:")
for n, nm in names.items():
    bc_e = BAU_e / n**4 / 100  # MG
    bc_x = BAU_x / n**4 / 100
    print(f"  {nm:3s}: 内生 {bc_e:.1f} MG   外部 {bc_x:.1f} MG")

# ---- 五维判别矩阵内生化（阈值全内生）----
print("\n五维判别矩阵（内生阈值）：")
print(f"  ① 布居/吸收：B < B_ion(n)（内生 B_ion = B_AU/n²）——吸收正常（A_total≠0）")
for n, nm in names.items():
    print(f"     {nm}: B_ion 内生 {BAU_e/n**2/100:.1f} MG")
print(f"  ② 辐射/逃逸产额：Φ_escape ↓ = σ^N（静默屏障——N=k_max=8 框架）")
print(f"  ③ 寿命：正常（A_total 非零——τ 不延长）")
print(f"  ④ 光电离：截面正常——连续谱不变（拓扑判别点 vs Fano 连续增强）")
print(f"  ⑤ 偏振：η_σ=(1-A_σ)·2/3（σ 填充抑制——TRK 2/3）——π 保持")
print(f"  ⑥ 标度：ℓ_B ∝ B^-1/2（纯 SI）——ξ=n²√(B/B_AU)（B_AU 内生）")
