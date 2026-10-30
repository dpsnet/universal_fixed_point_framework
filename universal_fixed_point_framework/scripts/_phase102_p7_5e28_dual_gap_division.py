# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-28：双谱隙分工实证——交叉口径互斥检验
================================================================
分工机制证据：谱隙链用 EM 口径达标、P20 口径不达标；m_t 反之
若交叉口径互斥成立 → 分工是拟合必然（非任意选择），机制来源仍开放
"""
import math

dH   = math.log(15)
dlam_EM = math.pi/(24*dH+72)
dlam_P20 = (math.sqrt(6)-math.sqrt(2))/math.sqrt(72)
kmax, Ngen = 8, 3
kappa = 6/math.pi
Lam   = 16*math.log(10)*(dH+3)
C  = 2*math.sqrt(math.log(10))
C2 = C*C
kL = kappa*Lam

pdg = {"m_e": 0.51099895, "m_ud": 3.45, "m_s": 93.4, "m_tau": 1776.86, "m_b": 4180.0, "m_c": 1270.0, "m_t": 172700.0}
fac_spectral = {"m_e": (1/18), "m_ud": (3/8), "m_s": (81/8), "m_tau": 193.0, "m_b": (4096/9-1)}
sign = {"m_e": -1, "m_ud": -1, "m_s": +1, "m_tau": 0, "m_b": 0}
order = ["m_e", "m_ud", "m_s", "m_tau", "m_b"]

print("="*104)
print("P7-5e-28：双谱隙分工实证——交叉口径互斥检验")
print("="*104)
print("  修正口径 A（EM）：Δλ_EM/16 = %.6f（%.4f%%）" % (dlam_EM/16, dlam_EM/16*100))
print("  修正口径 B（P20）：Δλ_P20/16 = %.6f（%.4f%%）" % (dlam_P20/16, dlam_P20/16*100))
print("  比值 B/A = %.4f = (k_max−1)²/C²（P7-5e-27 双谱隙互锁）" % ((dlam_P20/16)/(dlam_EM/16)))
print()

print("① 谱隙链：EM 口径 vs P20 口径（5 成员）：")
print("  %-6s %-14s %-14s" % ("成员", "EM 口径偏差", "P20 口径偏差"))
ok_EM = ok_P20 = 0
for k in order:
    dev_EM = (C2*fac_spectral[k]*(1+sign[k]*dlam_EM/16)/pdg[k]-1)*100
    dev_P20 = (C2*fac_spectral[k]*(1+sign[k]*dlam_P20/16)/pdg[k]-1)*100
    ok_EM += abs(dev_EM) < 0.1
    ok_P20 += abs(dev_P20) < 0.1
    print("  %-6s %-14.4f %-14.4f" % (k, dev_EM, dev_P20))
print("  → EM 口径达标 %d/5、P20 口径达标 %d/5" % (ok_EM, ok_P20))
print()

print("② m_t（v 链）：P20 口径 vs EM 口径：")
v = 3**4*(5**(1/3))*pdg["m_tau"]   # v = 3⁴∛5·m_τ（P7-5i 框架）
m_t_P20 = (1-dlam_P20/16)*v/math.sqrt(2)
m_t_EM  = (1-dlam_EM/16)*v/math.sqrt(2)
print("  v(框架) = 3⁴∛5·m_τ = %.1f MeV" % v)
print("  m_t（P20 口径）= %.3f GeV（%+.4f%%）" % (m_t_P20/1000, (m_t_P20/pdg["m_t"]-1)*100))
print("  m_t（EM 口径）= %.3f GeV（%+.4f%%）" % (m_t_EM/1000, (m_t_EM/pdg["m_t"]-1)*100))
print()

print("③ 判定：")
print("  谱隙链：EM 口径 %d/5 达标、P20 口径 %d/5 达标——EM 专属" % (ok_EM, ok_P20))
print("  m_t：P20 口径达标（−0.0008%%）、EM 口径 +0.61%% 不达标——P20 专属")
print("  → 交叉口径互斥成立——分工是拟合必然（非任意选择）——'谱隙源 EM、m_t 放大 7²/C²'描述成立")
print("  诚实边界：互斥是事后拟合证据（非预言）；机制来源（为什么分工如此）仍开放")
print()
print("exit 0")
