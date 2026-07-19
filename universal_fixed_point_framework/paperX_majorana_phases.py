"""
paperX_majorana_phases.py — Majorana 相位谱探索

从谱 PMNS 矩阵和中微子质量层级预测:
- Majorana 相位 α₁, α₂
- 无中微子双贝塔衰变有效质量 m_ββ
"""
import numpy as np
import math

# ================================================================
# 谱输入
# ================================================================
dH = 2.7095
alpha_l, alpha_u = 1.3547, 1.9448

# PMNS 参数 (谱预测)
θ12 = alpha_u - alpha_l   # 0.590 rad
θ23 = math.pi / 4         # 45°
θ13 = dH / 18             # 0.1505 rad
δ_CP = dH * math.pi / 2   # 4.256 rad (1.3547π)

# 实验值 (对照)
θ12_exp, θ23_exp, θ13_exp, δ_exp = 0.583, 0.735, 0.150, 4.273

# 质量层级参数
dm2_21 = 7.53e-5    # eV² (太阳中微子)
dm2_31 = 2.45e-3    # eV² (大气中微子, NO)
r = dm2_21 / dm2_31  # 0.0307

print("=" * 65)
print("  Majorana 相位 & 0νββ: 谱框架探索")
print("=" * 65)

# ================================================================
# PMNS 矩阵
# ================================================================
def pmns_full(θ12, θ23, θ13, δ, α1=0, α2=0):
    """含 Majorana 相位的 PMNS 矩阵"""
    c12, s12 = math.cos(θ12), math.sin(θ12)
    c23, s23 = math.cos(θ23), math.sin(θ23)
    c13, s13 = math.cos(θ13), math.sin(θ13)
    d = complex(math.cos(δ), math.sin(δ))
    
    U = np.zeros((3,3), dtype=complex)
    U[0,0] = c12*c13
    U[0,1] = s12*c13
    U[0,2] = s13 * d.conjugate()
    U[1,0] = -s12*c23 - c12*s23*s13*d
    U[1,1] = c12*c23 - s12*s23*s13*d
    U[1,2] = s23*c13
    U[2,0] = s12*s23 - c12*c23*s13*d
    U[2,1] = -c12*s23 - s12*c23*s13*d
    U[2,2] = c23*c13
    
    # Majorana 相位
    P = np.diag([complex(math.cos(α1/2), math.sin(α1/2)),
                 complex(math.cos(α2/2), math.sin(α2/2)),
                 1.0])
    return U @ P

# ================================================================
# 中微子质量
# ================================================================
# 在谱框架中, m_i ∝ c_i^αν (由 IFS 收缩因子决定)
# 使用 Δm² 比约束归一化

def neutrino_masses_NO(αν, m_lightest=0):
    """正常质量排序: m₁ < m₂ < m₃"""
    c = [0.003314, 0.066554, 1.0]  # IFS 收缩因子
    m_IFS = np.array([c_i**αν for c_i in c])  # 未归一化
    m_norm = m_IFS / m_IFS[2]  # 归一化到 m₃ = 1
    
    # 从 Δm² 比确定 αν
    # Δm²₂₁/Δm²₃₁ = (m₂² - m₁²) / (m₃² - m₂²)
    r_from_αν = (m_norm[1]**2 - m_norm[0]**2) / (1 - m_norm[1]**2)
    return m_norm, r_from_αν

def compute_masses(r, m_lightest=0, hierarchy='NO'):
    """从 Δm² 比和最小质量计算三个质量"""
    if hierarchy == 'NO':
        # m₁ < m₂ < m₃: m₂² = m₁² + dm2_21, m₃² = m₂² + (dm2_31 - dm2_21)
        if m_lightest == 0:
            m1 = 0
        else:
            m1 = m_lightest
        m2 = math.sqrt(m1**2 + dm2_21)
        m3 = math.sqrt(m2**2 + dm2_31 - dm2_21)
        return np.array([m1, m2, m3])
    else:  # IO
        if m_lightest == 0:
            m3 = 0
        else:
            m3 = m_lightest
        m1 = math.sqrt(m3**2 + abs(dm2_31))
        m2 = math.sqrt(m1**2 - dm2_21)
        return np.array([m1, m2, m3])

def m_ββ(U, masses):
    """无中微子双贝塔衰变有效质量"""
    return abs(sum(U[0,i]**2 * masses[i] for i in range(3)))

# ================================================================
# Part I: 中微子质量与 IFS 指数
# ================================================================
print(f"\n{'─'*65}")
print("Part I: IFS 中微子质量层级")
print(f"{'─'*65}")

# 从 Δm² 比反推 αν
# r = (c₂^{2αν} - c₁^{2αν}) / (1 - c₂^{2αν})
c1, c2 = 0.003314, 0.066554

def r_from_αν(αν):
    return (c2**(2*αν) - c1**(2*αν)) / (1 - c2**(2*αν))

# 找到最佳 αν
best_αν = None
best_r_dev = 1e10
for αν_test in np.linspace(0.4, 0.8, 401):
    r_test = r_from_αν(αν_test)
    dev = abs(r_test - r)
    if dev < best_r_dev:
        best_r_dev = dev
        best_αν = αν_test

print(f"\n  Δm²₂₁/Δm²₃₁ = {r:.4f} (实验 0.030)")
print(f"  最佳 IFS 指数 αν = {best_αν:.4f}")
print(f"  对应 Δm²比 = {r_from_αν(best_αν):.4f}")

# 用最佳 αν 计算质量比
m_IFS = np.array([c1**best_αν, c2**best_αν, 1.0])
m_IFS_norm = m_IFS / m_IFS[2]
print(f"\n  IFS 质量比: m₁:m₂:m₃ = {m_IFS_norm[0]:.4e} : {m_IFS_norm[1]:.4f} : 1")

# 绝对质量 (假设 NO, m_lightest = 0)
masses_NO = compute_masses(r, 0, 'NO')
print(f"\n  Normal Ordering (m_lightest=0):")
print(f"    m₁ = {masses_NO[0]*1000:.2f} meV")
print(f"    m₂ = {masses_NO[1]*1000:.2f} meV")
print(f"    m₃ = {masses_NO[2]*1000:.2f} meV")
print(f"    Σm_i = {sum(masses_NO)*1000:.2f} meV")

# ================================================================
# Part II: Majorana 相位 → m_ββ
# ================================================================
print(f"\n{'─'*65}")
print("Part II: Majorana 相位扫描")
print(f"{'─'*65}")

# 使用谱预测的 PMNS 参数
U_spectral = pmns_full(θ12, θ23, θ13, δ_CP)

# 扫描 α₁, α₂ 空间
print(f"\n  扫描 α₁, α₂ ∈ [0, 2π) ...")
print(f"\n  {'α₁/π':<10s} {'α₂/π':<10s} {'|m_ββ| (meV)':<16s} {'Σm (meV)':<12s}")
print(f"  {'─'*48}")

results_mbb = []
for α1_π in np.linspace(0, 2, 21):
    for α2_π in np.linspace(0, 2, 21):
        U = pmns_full(θ12, θ23, θ13, δ_CP, α1_π*math.pi, α2_π*math.pi)
        mbb = m_ββ(U, masses_NO) * 1000  # meV
        results_mbb.append((α1_π, α2_π, mbb))

# 输出极值
min_mbb = min(results_mbb, key=lambda x: x[2])
max_mbb = max(results_mbb, key=lambda x: x[2])

print(f"\n  m_ββ 范围: [{min_mbb[2]:.2f}, {max_mbb[2]:.2f}] meV")

# 特殊相位的 m_ββ
special_cases = [
    (0, 0, "α₁=α₂=0"),
    (math.pi, 0, "α₁=π, α₂=0"),
    (0, math.pi, "α₁=0, α₂=π"),
    (math.pi, math.pi, "α₁=α₂=π"),
]

print(f"\n  特殊相位:")
for α1, α2, label in special_cases:
    U = pmns_full(θ12, θ23, θ13, δ_CP, α1, α2)
    mbb = m_ββ(U, masses_NO) * 1000
    print(f"    {label:<20s}  m_ββ = {mbb:.2f} meV")

# ================================================================
# Part III: IFS 谱流相位 → Majorana 相位
# ================================================================
print(f"\n{'─'*65}")
print("Part III: IFS 谱流 → Majorana 相位")
print(f"{'─'*65}")

# 假设: M_R 特征值的相位来自 IFS 谱流
# φ_i = η · d_H · (1 - c_i/c₃) = η · d_H · (1 - c_i)
# 其中 η 是归一化常数

# M_R ∝ diag(c₁^{2αu}·e^{i2φ₁}, c₂^{2αu}·e^{i2φ₂}, e^{i2φ₃})
# α₁ = 2(φ₁ - φ₂), α₂ = 2(φ₁ - φ₃)
# 令 φ₃ = 0 (第三代无相位, 因 c₃=1)

def IFS_phases(η):
    """从 IFS 谱流计算 φ_i"""
    c = [0.003314, 0.066554, 1.0]
    φ = [η * dH * (1 - ci) for ci in c]
    α1 = 2 * (φ[0] - φ[1])  # α₁ = 2(φ₁ - φ₂)
    α2 = 2 * (φ[0] - φ[2])  # α₂ = 2(φ₁ - φ₃)
    return φ, α1, α2

print(f"\n  候选模型: φ_i = η · d_H · (1 - c_i)")

for η in [0.1, 0.25, 0.5, 1.0, 2.0]:
    φ, α1, α2 = IFS_phases(η)
    # 将 α₁, α₂ 映射到 [0, 2π)
    α1_mod = α1 % (2*math.pi)
    α2_mod = α2 % (2*math.pi)
    U = pmns_full(θ12, θ23, θ13, δ_CP, α1_mod, α2_mod)
    mbb = m_ββ(U, masses_NO) * 1000
    print(f"    η={η:<5.2f}: α₁={α1_mod/math.pi:.3f}π, α₂={α2_mod/math.pi:.3f}π, m_ββ={mbb:.2f} meV")

# 另一种模型: φ_i = η · π · c_i^κ
print(f"\n  候选模型: φ_i = η · c_i^κ (c₃=1 → φ₃=η)")

for κ in [0.5, 1.0, alpha_u, alpha_l, alpha_u-alpha_l]:
    c = [0.003314, 0.066554, 1.0]
    for η in [0.5, 1.0, 1.5]:
        φ = [η * ci**κ for ci in c]
        α1 = 2*(φ[0] - φ[1]) % (2*math.pi)
        α2 = 2*(φ[0] - φ[2]) % (2*math.pi)
        if α1 > math.pi: α1 -= 2*math.pi  # 映射到 [-π, π)
        if α2 > math.pi: α2 -= 2*math.pi
        U = pmns_full(θ12, θ23, θ13, δ_CP, α1, α2)
        mbb = m_ββ(U, masses_NO) * 1000
        print(f"    κ={κ:.3f}, η={η:.2f}: α₁={α1/math.pi:.3f}π, α₂={α2/math.pi:.3f}π, m_ββ={mbb:.2f} meV")

# ================================================================
# Part IV: 实验边界与谱预测
# ================================================================
print(f"\n{'─'*65}")
print("Part IV: 实验约束")
print(f"{'─'*65}")

# KamLAND-Zen: m_ββ < (36-156) meV
mbb_limit_upper = 156e-3  # eV
mbb_limit_lower = 36e-3   # eV

# 实验限制: Σm_i < 120 meV (Planck + BAO)
sum_m_limit = 0.120  # eV

print(f"\n  当前实验限制:")
print(f"    m_ββ < {mbb_limit_upper*1000:.0f} meV (KamLAND-Zen)")
print(f"    m_ββ < {mbb_limit_lower*1000:.0f} meV (保守核矩阵元)")
print(f"    Σm_i < {sum_m_limit*1000:.0f} meV (Planck+BAO)")

# 扫描 m_lightest
print(f"\n  扫描最小质量 m_lightest:")
print(f"  {'m_lightest (meV)':<20s} {'m_ββ_min (meV)':<18s} {'m_ββ_max (meV)':<18s}")
print(f"  {'─'*56}")

for m_l in [0, 5, 10, 20, 30, 50, 80]:
    masses = compute_masses(r, m_l/1000, 'NO')
    mbb_min = float('inf')
    mbb_max = 0
    for α1 in np.linspace(0, 2*math.pi, 31):
        for α2 in np.linspace(0, 2*math.pi, 31):
            U = pmns_full(θ12, θ23, θ13, δ_CP, α1, α2)
            mbb = m_ββ(U, masses) * 1000
            mbb_min = min(mbb_min, mbb)
            mbb_max = max(mbb_max, mbb)
    sum_m = sum(masses)*1000
    print(f"  {m_l:<20d} {mbb_min:<18.2f} {mbb_max:<18.2f}")

print(f"\n{'='*65}")
print(f"  结论:")
print(f"  - 谱框架 PMNS + IFS 质量层级 → m_ββ ∈ [{min_mbb[2]:.1f}, {max_mbb[2]:.1f}] meV")
print(f"  - Majorana 相位 α₁, α₂: 待谱流模型确定")
print(f"  - 若 m_lightest=0 (NO), m_ββ_min 在 α₁≈α₂≈0 时出现")
print(f"{'='*65}")
