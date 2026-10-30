# -*- coding: utf-8 -*-
"""
Phase 104az-75b: d_eff = (k_max²−2)/3 代数身份结构验证
62 = k_max²−2 = 64−2：检验 62 在框架内的其他投影（2 进计数谱）
"""
import math

kmax = 8
Nc = 3; Ngen = 3
sigma = 1/15
CF = (Nc**2-1)/(2*Nc)

# 62 的框架投影
print("=== 62 = k_max²−2 的框架投影 ===")
print(f"k_max = 8 = 2^3 (N_active=3)；k_max² = 64 = 2^6；62 = 2^6 − 2")
print(f"  2^6 − 2 = 64 − 2 = 62 ✓（2 进计数谱：2^6 是全状态计数，−2 是双静默/双奇点剔除？）")
print(f"62/3 = 20.667（÷N_c=3）")

# 62 的分解
print(f"\n62 = 2×31；31 = 2^5 − 1（Mersenne！）")
print(f"  → 62 = 2×(2^5−1) = 2^(1)·(2^5−1)：k_max 族 Mersenne 组合")
print(f"  k_max=8: 8²−2 = 64−2 = 62 = 2(2^5−1)")
print(f"  检查 Mersenne 框架角色：P7-5e-205 已登记 Mersenne 与 65 身份")

# 与登记 (b₀/10)³ 的关系
b0_10 = (9/10)**3
print(f"\n=== 双代数身份重合 ===")
a_id = ((62/3)/(4*math.pi*Nc) * (1/math.sqrt(2)))**(1/3)
print(f"几何正推 a₀(62/3) = {a_id:.9f}")
print(f"计数代数 (b₀/10)³ = {b0_10:.9f}")
print(f"重合度: {(a_id/b0_10-1)*100:+.5f}%")

# 62 在 d_eff 结构中的角色：16 + d_q + δd_s = 20.590 vs 62/3 = 20.667
Z2 = 1.44
dq = Ngen*Nc*(CF/2)*math.sqrt(1/math.sqrt(2))*(1/Z2)
dds = (CF/2)*math.exp(-(CF/2)**2/a_id)*Nc
d_struct = 16 + dq + dds
print(f"\n=== 结构 vs 身份差归因 ===")
print(f"身份 d_eff = {62/3:.6f}；结构 d_eff(a₀身份) = {d_struct:.6f}；差 {(d_struct/(62/3)-1)*100:+.4f}%")
print(f"身份−结构 = {62/3 - d_struct:.6f}")
print(f"  若身份成立：δd_(s) 项 {dds:.6f} 应从何而来？")
print(f"身份要求的非胶子部分 = 62/3 − 16 = {62/3-16:.6f}")
print(f"  结构非胶子部分 = d_q + δd_(s) = {dq+dds:.6f}")
print(f"  差 = {(62/3-16)-(dq+dds):.6f}（0.37% 残余）")
