# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-48：m_c 双基底（恒等 A）+ 修正形式 = 质量半区
================================================================
洞察1：m_c = κΛ×√10 = C²×√10/Δλ_EM——恒等 A（κΛ×Δλ_EM = C²）连接双基底——m_c 是谱隙链 C² 基底成员
洞察2：m_c 系数 √10/Δλ_EM = 137.895 ≈ 1/α_EM（差 0.66%——方向性——charm 耦合身份）
洞察3：修正形式 = 质量半区——轻半（e/ud/s < 100 MeV）外挂、重半（c/τ/b > 1 GeV）内嵌
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

m_c_kL = kL*math.sqrt(10)
m_c_C2 = C2*math.sqrt(10)/dlam_EM
inv_alpha = 24*(dH+3)

print("="*104)
print("P7-5e-48：m_c 双基底（恒等 A）+ 修正形式质量半区")
print("="*104)

print()
print("【★★ m_c 双基底——恒等 A 连接】")
print("-"*104)
print("m_c = κΛ×√10 = %.4f MeV（P7-5e-23/24——+0.0049%%）" % m_c_kL)
print("     = C²×√10/Δλ_EM = %.4f MeV（恒等 A：κΛ×Δλ_EM = C²）" % m_c_C2)
print("→ 两个基底恒等——m_c 是谱隙链 C² 基底成员（系数 √10/Δλ_EM）——非独立结构")
print("  系数 √10/Δλ_EM = %.3f——√10 = √(k_max+N_gen−1) 身份已闭合——Δλ_EM = 谱隙（Rec 层）" % (math.sqrt(10)/dlam_EM))
print()
print("【m_c 系数 ≈ 1/α_EM——charm 耦合身份（方向性）】")
print("-"*104)
mc_coef = math.sqrt(10)/dlam_EM
print("m_c 系数 = √10/Δλ_EM = %.4f" % mc_coef)
print("1/α_EM（框架）= 24(d_H+3) = %.4f——差 %+.4f%%" % (inv_alpha, (mc_coef/inv_alpha-1)*100))
print("→ m_c 系数在电磁耦合标度附近——方向性观察（非精确——0.66%% 差）")
print()
print("【修正形式 = 质量半区——轻外挂/重内嵌】")
print("-"*104)
members = [("m_e", 0.51, "外挂 −δ"), ("m_ud", 3.45, "外挂 −δ"), ("m_s", 93.4, "外挂 +δ"),
           ("m_c", 1270, "内嵌 √10/Δλ_EM"), ("m_τ", 1776, "内嵌 −3/40"), ("m_b", 4180, "内嵌 +3ln7")]
print("成员      质量(MeV)   修正形式")
for name, m, f in members:
    half = "轻半" if m < 100 else "重半"
    print("%-6s %8.0f   %-16s %s" % (name, m, f, half))
print()
print("→ ★★ 修正形式 = 质量半区：轻半（e/ud/s < 100 MeV）谱隙外挂、重半（c/τ/b > 1 GeV）系数内嵌")
print("→ 分界在 s/c 之间（93 → 1270 MeV——质量跳跃）——非纯代依赖（m_s 与 m_c 同代但形式不同）")
print("→ 重半内嵌与三代静默（τ/b）相关——但 c 无静默——两个结构（内嵌/静默）独立")
print()
print("【结论】")
print("-"*104)
print("1. ★★ m_c = κΛ×√10 = C²×√10/Δλ_EM——恒等 A 连接双基底——m_c 是谱隙链 C² 基底成员（非独立结构）")
print("2. ★ m_c 系数 √10/Δλ_EM = 137.895 ≈ 1/α_EM（差 0.66%%——方向性——charm 耦合身份——非精确）")
print("3. ★★ 修正形式 = 质量半区：轻半外挂（e/ud/s）、重半内嵌（c/τ/b）——分界在 s/c 质量跳跃")
print("4. 诚实边界：m_c 系数 0.66%% 非精确；轻/重半区机制开放；内嵌与静默的独立关系开放")
print()
json.dump({"mc_dual": {"kL": m_c_kL, "C2": m_c_C2, "identical": abs(m_c_kL-m_c_C2)<1e-6},
           "mc_coef_vs_alpha": (mc_coef/inv_alpha-1)*100,
           "corr_half": {"light": "external", "heavy": "embedded"}},
          open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e48_mc_dual.json","w",encoding="utf-8"), indent=2)
print("JSON 落盘 ✓")
print("exit 0")
