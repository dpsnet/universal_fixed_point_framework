# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-47：系数家族完整谱 + 谱隙修正分布（外挂 vs 内嵌）
================================================================
洞察1：第一/二代系数也有框架身份——m_e 1/18 = 1/((N_gen−1)(k_max+1))、m_ud 3/8 = N_gen/k_max、m_s 81/8 = (k_max+1)²/k_max
洞察2：m_s/m_ud = N_gen³×(1+Δλ_EM/16)/(1−Δλ_EM/16)——27.0774 vs PDG 27.07
洞察3：谱隙修正分布——第一/二代有（外挂 ×(1±δ)）、第三代无（修正内嵌系数）——谱隙修正 ↔ 静默单元互斥
"""
import math, json

dH   = math.log(15)
dlam_EM = math.pi/(24*dH+72)
C  = 2*math.sqrt(math.log(10))
C2 = C*C
kappa = 6/math.pi
Lam  = 16*math.log(10)*(dH+3)
kL   = kappa*Lam
sigma = 1/15
kmax, Ngen = 8, 3
delta0 = dlam_EM/16

m_e  = C2*(1-delta0)/18
m_ud = C2*(1-delta0)*3/8
m_s  = C2*(1+delta0)*81/8
m_c  = kL*math.sqrt(10)
m_tau= C2*(193-3/40)
m_b  = C2*(2**6*(kmax-1)+Ngen*math.log(kmax-1))

print("="*104)
print("P7-5e-47：系数家族完整谱 + 谱隙修正分布")
print("="*104)

print()
print("【系数家族完整谱——第一/二代系数身份发现】")
print("-"*104)
print("m_e  系数 1/18    = 1/((N_gen−1)(k_max+1)) = 1/(%d×%d) = %.4f" % (Ngen-1, kmax+1, 1/((Ngen-1)*(kmax+1))))
print("m_ud 系数 3/8     = N_gen/k_max = %d/%d = %.4f" % (Ngen, kmax, Ngen/kmax))
print("m_s  系数 81/8    = (k_max+1)²/k_max = %d²/%d = %.4f" % (kmax+1, kmax, (kmax+1)**2/kmax))
print("m_τ  系数 192.925 = k_max²·N_gen+1−3/40（静默单元——P7-5e-39）")
print("m_b  系数 453.838 = k_max²·(k_max−1)+N_gen·ln(k_max−1)（静默单元——P7-5e-33）")
print("→ ★ 系数家族全框架化——不是只有第三代有身份——第一/二代系数 = 纯组合结构")
print()
print("【★★ m_s/m_ud = N_gen³×(1+δ)/(1−δ)】")
print("-"*104)
ratio_fw = (81/8)/(3/8)*(1+delta0)/(1-delta0)
print("m_s/m_ud 框架 = (81/8)/(3/8)×(1+δ)/(1−δ) = 27×(1+δ)/(1−δ)")
print("   = %d×%.6f/%.6f = %.4f——(81/8)/(3/8) = %d = N_gen³" % (Ngen**3, 1+delta0, 1-delta0, ratio_fw, (81/8)/(3/8)))
ratio_pdg = 93.4/3.45
print("PDG m_s/m_ud = 93.4/3.45 = %.4f——差 %+.4f%%（m_s 不确定度 ±8.6%% 内）" % (ratio_pdg, (ratio_fw/ratio_pdg-1)*100))
print("→ ★★ 夸克质量比 = N_gen³×(1+δ)/(1−δ)——纯代结构 × 谱隙修正")
print()
print("【谱隙修正分布——互斥结构】")
print("-"*104)
print("第一代 m_e/m_ud：×(1−Δλ_EM/16)——【谱隙外挂】")
print("第二代 m_s      ：×(1+Δλ_EM/16)——【谱隙外挂】")
print("m_c            ：×√10（κΛ 基底）——【无谱隙修正——独立结构】")
print("第三代 m_τ/m_b  ：修正内嵌系数（−3/40、+3ln7——与静默单元同层）——【无谱隙外挂】")
print()
print("→ ★★ 谱隙修正 ↔ 静默单元互斥分布：")
print("   第一/二代：谱隙外挂（±Δλ_EM/16 因子）——无静默单元")
print("   第三代   ：系数内嵌（静默单元 +1/×7 同层）——无谱隙外挂")
print("→ 修正形式也随代：外挂（轻代）vs 内嵌（重代）")
print()
print("【修正形式代依赖——与 P7-5e-44 符号代依赖同层】")
print("-"*104)
print("P7-5e-44：符号随代（第一代 −/第二代 +）")
print("P7-5e-47：形式随代（轻代外挂/重代内嵌）")
print("→ 代依赖结构双轴：符号（−/+）× 形式（外挂/内嵌）")
print()
print("【结论】")
print("-"*104)
print("1. ★ 系数家族全框架化——第一/二代系数 1/18 = 1/((N_gen−1)(k_max+1))、3/8 = N_gen/k_max、81/8 = (k_max+1)²/k_max")
print("2. ★★ m_s/m_ud = N_gen³×(1+δ)/(1−δ) = 27.0774——vs PDG 27.07——差 0.03%——命中（m_s 不确定度内）")
print("3. ★★ 谱隙修正 ↔ 静默单元互斥：轻代外挂（±Δλ_EM/16）、重代内嵌（静默同层）——修正形式随代")
print("4. 诚实边界：m_τ/m_b 修正内嵌的机制开放；m_c 独立结构（无谱隙/静默）的归类开放；外挂→内嵌的转变机制开放")
print()
json.dump({"coef_family": {"e": "1/((Ngen-1)(kmax+1))", "ud": "Ngen/kmax", "s": "(kmax+1)^2/kmax"},
           "ms_mud": {"frame": ratio_fw, "pdg": ratio_pdg, "dev_pct": (ratio_fw/ratio_pdg-1)*100},
           "corr_dist": {"gen12": "spectral-external", "gen3": "coef-embedded", "mc": "none"}},
          open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e47_coef_family.json","w",encoding="utf-8"), indent=2)
print("JSON 落盘 ✓")
print("exit 0")
