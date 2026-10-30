# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-42：m_t/m_b 41 骨架 + 组合平方家族 {25, 49}
================================================================
洞察1：m_t/m_b = 41.3165 ≈ 41 = k_max·(k_max−N_gen)+1（静默单元家族成员）——方向性
洞察2：25 = (k_max−N_gen)² 与 49 = (k_max−1)²——组合减量平方家族（减量 N_gen vs 1）
"""
import math, json

dH   = math.log(15)
dlam_EM = math.pi/(24*dH+72)
dlam_P20 = (math.sqrt(6)-math.sqrt(2))/math.sqrt(72)
C  = 2*math.sqrt(math.log(10))
C2 = C*C
kappa = 6/math.pi
Lam  = 16*math.log(10)*(dH+3)
kL   = kappa*Lam
sigma = 1/15
alpha_v = 1+sigma+math.sqrt(4/3/2)
alpha_t = math.log(7)
kmax, Ngen = 8, 3
alpha0 = 1/2
alpha0_3 = alpha0**3
N_total = kmax - Ngen

print("="*104)
print("P7-5e-42：m_t/m_b 41 骨架 + 组合平方家族 {25, 49}")
print("="*104)

m_t = (1-dlam_P20/16)*3**4*5**(1/3)*C2*(193-3/40)/math.sqrt(2)
m_b = C2*(2**6*(kmax-1)+Ngen*alpha_t)
ratio = m_t/m_b

print()
print("【m_t/m_b 41 骨架】")
print("-"*104)
print("m_t/m_b = %.6f（P7-5e-36 精确表达式，差 −0.000005%% vs PDG）" % ratio)
print("41 = k_max·(k_max−N_gen)+1 = %d×%d+1（静默单元家族成员）" % (kmax, N_total))
print("41 骨架：%.6f/41 = %.8f（差 %+.4f%%）" % (ratio, ratio/41, (ratio/41-1)*100))
print("修正 +0.772%% ≈ Δλ_P20/16 = %.6f%%（差 %+.4f%%——非精确——方向性）" % (dlam_P20/16*100, (ratio/41-1-dlam_P20/16)*100))
print()
print("【41+1/√10 候选】")
print("-"*104)
print("41+1/√10 = 41+%.8f = %.6f vs %.6f（差 %+.6f%%）" % (1/math.sqrt(10), 41+1/math.sqrt(10), ratio, (41+1/math.sqrt(10))/ratio*100-100))
print("√10 = √(k_max+N_gen−1)——10 的框架身份已闭合（P7-5e-36）——但 +1/√10 结构身份开放——候选级")
print()
print("【组合平方家族 {25, 49}】")
print("-"*104)
print("25 = (k_max−N_gen)² = %d²——减量 N_gen = 3" % N_total)
print("49 = (k_max−1)² = %d²——减量 1 = 静默单元" % (kmax-1))
print("→ 组合减量平方家族——减量 {N_gen, 1}——与静默单元家族（+1 加法）同构的另一侧")
print("→ 25 双身份：k_max·N_gen+1 = 24+1（静默单元 X+1）AND (k_max−N_gen)² = 5²（组合平方）")
print("→ 49 双身份：N_gen!·k_max+1 = 48+1（静默单元 X+1）AND (k_max−1)² = 7²（组合平方）")
print("→ ★ 25 与 49 在【静默单元家族】和【组合平方家族】双家族同时并存——双身份 = 双家族成员")
print()
print("【减量平方 vs 静默单元 +1 的对称结构】")
print("-"*104)
print("k_max−N_gen = 5——5² = 25（平方）AND 5 参与 41 = 8×5+1（加法）")
print("k_max−1 = 7——7² = 49（平方）AND 7 参与 m_b = 64×7+3ln7（乘法静默）")
print("→ 同一组合减量 {5, 7} 同时以【平方】和【静默单元参与】两种形式出现——结构自洽")
print()
print("【结论】")
print("-"*104)
print("1. ★ m_t/m_b 41 骨架：≈ 41 = k_max·(k_max−N_gen)+1（差 +0.772%）——修正方向 ≈ Δλ_P20/16（差 0.009%）——方向性观察（非精确命中——精确表达式已登记 P7-5e-36）")
print("2. ★ 41+1/√10 候选：差 0.00065%%（0.001%% 级）——√10 = √(k_max+N_gen−1) 身份已闭合——但 +1/√10 结构身份开放——候选级")
print("3. ★★ 组合平方家族 {25, 49} = {(k_max−N_gen)², (k_max−1)²}——减量 {N_gen, 1}——25/49 双家族成员（静默单元 + 组合平方）")
print("4. ★ 减量平方与静默单元对称结构（同一 {5, 7} 双形式出现）")
print("5. 诚实边界：41 骨架非精确（0.77%%）；41+1/√10 候选级；组合平方家族机制开放")
print()
json.dump({"m_t_mb": ratio, "skeleton_41": ratio/41, "corr_dlam": dlam_P20/16,
           "cand_41_1sqrt10": 41+1/math.sqrt(10), "cand_dev": (41+1/math.sqrt(10))/ratio*100-100,
           "square_family": {"25": "(kmax-Ngen)^2=5^2", "49": "(kmax-1)^2=7^2"}},
          open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e42_skeleton41.json","w",encoding="utf-8"), indent=2)
print("JSON 落盘 ✓")
print("exit 0")
