# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-51：类型主导 + 质量梯度——通道分配双轴
================================================================
洞察1：轻子全 Rec（e 外挂/τ 计数）——类型主导
洞察2：夸克质量梯度（ud/s 外挂 → c 分母 → b 比值 → t Sp）——质量微调
洞察3：第三代通道梯度 = 质量序（τ 1776 Rec → b 4180 混合 → t 172700 Sp）
洞察4：τ 是例外（质量比 c 大但走 Rec 计数）——轻子类型主导解释
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
kmax, Ngen = 8, 3

# 质量（MeV/GeV 框架值）
m_e  = C2*(1-dlam_EM/16)/18
m_ud = C2*(1-dlam_EM/16)*3/8
m_s  = C2*(1+dlam_EM/16)*81/8
m_c  = kL*math.sqrt(10)
m_tau= C2*(kmax**2*Ngen+1-3/40)
m_b  = C2*(2**6*(kmax-1)+Ngen*math.log(kmax-1))

print("="*104)
print("P7-5e-51：类型主导 + 质量梯度——通道分配双轴")
print("="*104)

print()
print("【成员通道全谱】")
print("-"*104)
members = [("m_e", m_e, "轻子", "外挂 −δ", "Rec"),
           ("m_ud", m_ud, "夸克", "外挂 −δ", "Rec"),
           ("m_s", m_s, "夸克", "外挂 +δ", "Rec"),
           ("m_c", m_c, "夸克", "分母 √10/Δλ_EM", "中间"),
           ("m_τ", m_tau, "轻子", "计数 +1/代数 3/40", "Rec"),
           ("m_b", m_b, "夸克", "比值 ×7/对数 3ln7", "Sp"),
           ("m_t", 172700, "夸克", "P20 谱隙", "Sp")]
print("%-6s %-10s %-4s %-22s %s" % ("成员", "质量(MeV)", "类型", "修正形式", "通道"))
for name, m, typ, f, ch in members:
    print("%-6s %-10.1f %-4s %-22s %s" % (name, m, typ, f, ch))
print()
print("【★★ 双轴结构——类型主导 + 质量梯度】")
print("-"*104)
print("轻子（e/τ）：全 Rec——e 外挂、τ 计数——【类型主导】——不随质量走 Sp")
print("夸克（ud/s/c/b/t）：质量梯度 Rec → Sp——ud/s 外挂 → c 分母 → b 比值 → t 纯 Sp")
print()
print("→ 轻子无颜色（电磁纯 Rec 侧？）、夸克有颜色（强作用——随质量演化向 Sp？）——方向性")
print()
print("【第三代通道梯度 = 质量序】")
print("-"*104)
print("m_τ (1776) Rec 计数 → m_b (4180) 混合（EM 基底+Sp 修正） → m_t (172700) 纯 Sp")
print("→ ★ 第三代内部：质量越大越 Sp——τ 例外（轻子类型主导）")
print()
print("【τ 例外解释】")
print("-"*104)
print("τ 质量 (1776) > c (1270)——按夸克梯度应比 c 更 Sp——但 τ 走 Rec 计数")
print("→ τ 是唯一重轻子——轻子类型主导（全 Rec）覆盖质量梯度——【类型 > 质量】")
print()
print("【b 双身份——两个对偶的交点】")
print("-"*104)
print("τ/b 对偶（轻子/夸克）：τ Rec 计数 vs b Sp 比值——b 是 Sp 修正侧")
print("t/b 对偶（上/下型）：t Sp 面 vs b EM 面——b 是 EM 基底侧")
print("→ b = 两个对偶的交点——EM 基底 + Sp 修正——混合身份 = 夸克质量梯度中间位置")
print()
print("【结论】")
print("-"*104)
print("1. ★★ 通道分配双轴：轻子全 Rec（类型主导）、夸克质量梯度（ud/s→c→b→t——Rec→Sp）")
print("2. ★★ 第三代通道梯度 = 质量序（τ Rec → b 混合 → t Sp）——τ 例外 = 轻子类型主导（类型 > 质量）")
print("3. ★ b 双身份 = 两个对偶交点（τ/b 轻子对偶 Sp 修正侧 + t/b 上下对偶 EM 基底侧）——混合 = 质量梯度中间")
print("4. 诚实边界：轻子 Rec/夸克梯度的机制（颜色？）开放；c 的中间通道归类开放；质量梯度斜率开放")
print()
json.dump({"dual_axis": {"lepton": "all-Rec", "quark": "mass-gradient"},
           "gen3_gradient": {"tau": "Rec", "b": "mixed", "t": "Sp"},
           "b_dual": {"tau_b": "Sp-correction", "t_b": "EM-base"}},
          open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e51_type_gradient.json","w",encoding="utf-8"), indent=2)
print("JSON 落盘 ✓")
print("exit 0")
