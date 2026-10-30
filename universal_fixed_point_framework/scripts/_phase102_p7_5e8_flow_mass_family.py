# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-8：流质量族闭式扫描——m_i = κΛ·Δλ_min·(代数闭式) 跨扇区检验
=============================================================================
P7-5e-7 唯一幸存者 M_Q（m_ud ≈ κΛ·Δλ_min·N_gen/k_max，0.03%）扩展为系统检验：
对所有轻子/夸克流质量，找代数闭式 a 使 m_i = κΛ·Δλ_min/a（0.1% 标准）。
候选代数身份库：N_gen 组合、k_max 组合、2 幂次、dH、σ、桥、π 系。
"""
import json
import math

# 框架量
dH   = math.log(15)
ln16 = math.log(16)
br   = math.log(16/15)
br3  = br/3
sig  = 1/15
kap  = 6/math.pi
Lam  = 210.3
kLam = kap*Lam          # 401.643
dlam = 0.0229           # Δλ_min^(EM) 登记值
dlam_exact = math.pi/(24*dH+72)   # P7-5l 框架推导精确值
base = kLam*dlam        # 9.1976
base_exact = kLam*dlam_exact

# 候选代数闭式库 a（分母身份）
CAND = {}
CAND["3/8 (N_gen/k_max)"] = 3/8
CAND["2·N_gen² (18)"] = 2*9
CAND["16"] = 16
CAND["16+2 (18)"] = 18
CAND["3·6 (18)"] = 18
CAND["2·k_max (16)"] = 16
CAND["N_gen·k_max (24)"] = 24
CAND["8·(5+1/8) (41)"] = 41
CAND["k_max² (64)"] = 64
CAND["2·dH"] = 2*dH
CAND["4·dH"] = 4*dH
CAND["16·dH"] = 16*dH
CAND["κ (6/π)"] = kap
CAND["2κ"] = 2*kap
CAND["κ²"] = kap**2
CAND["π"] = math.pi
CAND["2π"] = 2*math.pi
CAND["4π"] = 4*math.pi
CAND["π·dH"] = math.pi*dH
CAND["π/σ"] = math.pi/sig
CAND["1/σ"] = 1/sig
CAND["1/σ²"] = 1/sig**2
CAND["1/σ³"] = 1/sig**3
CAND["1/(2σ)"] = 1/(2*sig)
CAND["1/(2σ/3)"] = 1/(2*sig/3)
CAND["e"] = math.e
CAND["e²"] = math.e**2
CAND["e³"] = math.e**3
CAND["s^1 (e)"] = math.e
CAND["s^2"] = math.e**2
CAND["s^3"] = math.e**3
CAND["√8"] = math.sqrt(8)
CAND["√(8·9)"] = math.sqrt(72)
CAND["ln16"] = ln16
CAND["ln15"] = dH
CAND["2^5 (32)"] = 32
CAND["2^6 (64)"] = 64
CAND["3^3 (27)"] = 27
CAND["3^4 (81)"] = 81
CAND["4^3 (64)"] = 64
CAND["5^2 (25)"] = 25
CAND["2·3·5 (30)"] = 30
CAND["3·5 (15)"] = 15
CAND["7 (k_max−1)"] = 7
CAND["8 (k_max)"] = 8
CAND["k_max+N_gen (11)"] = 11
CAND["k_max−N_gen (5)"] = 5
CAND["k_max·N_gen−1 (23)"] = 23
CAND["k_max·N_gen+2 (26)"] = 26
CAND["(k_max−1)/N_gen"] = 7/3
CAND["k_max/N_gen (8/3)"] = 8/3
CAND["(k_max−1)·N_gen (21)"] = 21
CAND["桥"] = br
CAND["桥·16"] = 16*br
CAND["桥·κ"] = br*kap

# 质量目标 (名称, MeV, 依赖)
MASSES = [
    ("m_e",  0.51099895, "实验"),
    ("m_μ", 105.658375, "实验"),
    ("m_τ", 1776.86,    "实验"),
    ("m_ud", 3.45,       "PDG 流质量"),
    ("m_s", 93.4,        "PDG 流质量"),
    ("m_c", 1270,        "PDG 流质量"),
    ("m_b", 4180,        "PDG 流质量"),
    ("m_t", 172690,      "PDG 流质量"),
]

print("="*100)
print("P7-5e-8：流质量族闭式扫描——m_i = κΛ·Δλ_min/a 跨扇区检验")
print("="*100)
print("  κΛ = %.4f MeV, Δλ_min^(EM) 登记 = %.4f, 框架精确 = %.7f" % (kLam, dlam, dlam_exact))
print("  基底 κΛ·Δλ_min(登记) = %.4f MeV; κΛ·Δλ_min(精确) = %.4f MeV" % (base, base_exact))
print()
print("%-8s %-12s %-10s %-22s %s" % ("质量", "m_i (MeV)", "a = κΛΔλ/m", "最佳闭式 a", "偏差"))
hits = []
for name, m, dep in MASSES:
    a = base/m
    best = None
    for cname, cval in CAND.items():
        dev = abs(a - cval)/a*100
        if best is None or dev < best[1]:
            best = (cname, dev)
    dev = best[1]
    tag = "★" if dev < 0.1 else ("·" if dev < 1 else " ")
    print("%s%-7s %-12.6f %-10.6f %-22s %5.2f%%" % (tag, name, m, a, best[0], dev))
    hits.append((name, m, a, best[0], dev))

print()
print("判定：")
for name, m, a, c, d in hits:
    if d < 0.1:
        print("  ★ %s：a = %.6f ≈ %s（%.2f%%）——独立闭式命中（登记值口径）" % (name, a, c, d))
        m_calc = base / [v for k,v in CAND.items() if k==c][0]
        m_calc_ex = base_exact / [v for k,v in CAND.items() if k==c][0]
        print("     → m ≈ κΛ·Δλ_min^(EM)/%s：登记值口径 %.6f（%.2f%%），框架精确口径 %.6f（%.2f%%）"
              % (c, m_calc, abs(m_calc-m)/m*100, m_calc_ex, abs(m_calc_ex-m)/m*100))
print()
print("★ 比值闭式（不依赖 Δλ_min 取值，谱隙精度无关）：")
m_e, m_ud = 0.51099895, 3.45
ratio = m_e/m_ud
print("  m_e/m_ud = %.6f vs 4/27 = %.6f（偏差 %.2f%%）" % (ratio, 4/27, abs(ratio-4/27)/ratio*100))
print("  4/27 = (k_max/2)/N_gen³ = 2²/3³ —— 纯代数计数闭式（m_e 分母 2·N_gen² ↔ m_ud 分子 N_gen/k_max 之比）")
print("  → 若成立：m_e:m_ud = 2²:3³（轻子:流质量 = 计数闭式比，Δλ_min^(EM) 在比值中消去）")
print()
print("exit 0")
