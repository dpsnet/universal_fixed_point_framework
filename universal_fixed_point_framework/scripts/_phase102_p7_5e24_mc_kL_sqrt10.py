# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-24：m_c = κΛ·√10 候选精确验证
================================================================
发现：m_c/(κΛ) ≈ 3.162 ≈ √10 = √(N_gen+k_max−1)——框架量候选
等价形式：m_c = κΛ·√10 = C²·√10/Δλ_min（π 消去恒等式 κΛΔλ = C²）
"""
import math

dH   = math.log(15)
dlam = math.pi/(24*dH+72)
kmax, Ngen = 8, 3
kappa = 6/math.pi
Lam   = 16*math.log(10)*(dH+3)          # P7-5e-18 谱定
C  = 2*math.sqrt(math.log(10))
C2 = C*C

kL = kappa*Lam
mc_pdg = 1270.0

print("="*104)
print("P7-5e-24：m_c = κΛ·√10 候选精确验证")
print("="*104)
print("  框架量：κ = 6/π = %.6f、Λ = 16ln10(dH+3) = %.6f、κΛ = %.6f" % (kappa, Lam, kL))
print("  √10 = √(N_gen+k_max−1) = %.6f" % math.sqrt(10))
print()

mc_1 = kL*math.sqrt(10)
mc_2 = C2*math.sqrt(10)/dlam
print("① 直接：m_c = κΛ·√10 = %.4f MeV（vs PDG 1270，%+.4f%%）" % (mc_1, (mc_1/mc_pdg-1)*100))
print("② 等价：m_c = C²·√10/Δλ = %.4f MeV（%+.4f%%）——π 消去恒等下的重述" % (mc_2, (mc_2/mc_pdg-1)*100))
print()

# 数值邻域检验：√10 是否唯一框架量候选？
print("③ √n 邻域扫描（n = N_gen+k_max−1 = 10 及其邻域）：")
for n in range(8, 13):
    v = kL*math.sqrt(n)
    print("  κΛ·√%d = %.3f（%+.4f%%）" % (n, v, (v/mc_pdg-1)*100))
print()

print("④ 身份结构分析：")
print("  m_c = κΛ·√(N_gen+k_max−1)——κΛ 标度（强子标度谱量）× √计数")
print("  κΛ 身份：κ² = (6/π)² 胶子谱量平方（paper40 定理5.3 骨架）+ Λ = 16ln10(dH+3) 谱定（P7-5e-18）")
print("  √10 = √(N_gen+k_max−1) = √(3+7)——√计数新形态（非 2^a·3^b±1）")
print("  → m_c 填补谱隙链空缺（上型第二代）——但走 κΛ×√n 链（非 C²×2^a3^b 族）")
print()

print("⑤ 判定：")
if abs(mc_1/mc_pdg-1) < 0.001:
    print("  ★★★ m_c = κΛ·√10 命中 %+.4f%%（0.1%% 标准内）——新成员候选（κΛ×√计数形态）" % ((mc_1/mc_pdg-1)*100))
    print("  等价重述：m_c = C²·√10/Δλ_min——谱隙基底×√计数÷谱隙——与谱隙链同框架")
    print("  → 上型第二代补位候选——分工图景：谱隙链（C²×2^a3^b±1）× 5 成员 + κΛ×√n 链（m_c）")
else:
    print("  未达标——m_c 候选排除")
print()
print("exit 0")
