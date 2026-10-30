# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-33b：m_b 精化确认——C²×(2⁶(k_max−1)+N_gen·α_t)
================================================================
搜索发现：m_b 系数 453.8377 ≈ 2⁶·7+3·ln7 = 2⁶(k_max−1)+N_gen·α_t（±0.0000%）
验证 + 竞争候选判别（a-规则）+ 与 m_τ 精化模式对比
"""
import math, json

dH   = math.log(15)
dlam_EM = math.pi/(24*dH+72)
C2 = 4*math.log(10)
kmax, Ngen = 8, 3
alpha_t = math.log(7)

m_b_pdg = 4180.0

print("="*104)
print("P7-5e-33b：m_b 精化确认——C²×(2⁶(k_max−1)+N_gen·α_t)")
print("="*104)
print("  PDG m_b = %.1f MeV" % m_b_pdg)
print()

print("① 新候选精确验证：")
coef_new = 2**6*(kmax-1)+Ngen*alpha_t
m_b_new = C2*coef_new
m_b_old = C2*(2**12/9-1)
print("  系数 = 2⁶·(k_max−1)+N_gen·α_t = 64×7+3×ln7 = %.8f" % coef_new)
print("  m_b(新) = C²×%.4f = %.4f MeV（%+.6f%% vs PDG）" % (coef_new, m_b_new, (m_b_new/m_b_pdg-1)*100))
print("  m_b(原) = C²×(2¹²/3²−1) = %.4f MeV（%+.4f%% vs PDG）" % (m_b_old, (m_b_old/m_b_pdg-1)*100))
print()

print("② 竞争候选判别：")
c1 = 2**6*(kmax-1)+Ngen*alpha_t          # 2⁶·7+3ln7：纯计数+对数（代数身份型）
c2 = (2**12/9-1)*(1-dlam_EM/64)          # 454×(1−Δλ_EM/64)：含谱隙修正
c3 = (2**12/9-1)-(kmax-1)*dlam_EM        # 454−7Δλ_EM：含谱隙修正
for name, c in [("2⁶(k_max−1)+N_gen·α_t（代数身份型）", c1),
                ("454×(1−Δλ_EM/64)（谱隙修正型）", c2),
                ("454−7Δλ_EM（谱隙修正型）", c3)]:
    print("  %-36s = %.6f（%+.6f%%）" % (name, c, (c/453.837734-1)*100))
print()
print("  a-规则（P7-5e-31）：m_b a = 12 > 0 堆积型——不带谱隙修正")
print("  → 候选 2/3 含 Δλ 修正——与 a-规则冲突——排除")
print("  → 候选 1 无谱隙修正——a-规则一致——胜出")
print()

print("③ 框架身份结构：")
print("  2⁶ = 64（旋量塔幂）、k_max−1 = 7（P7-4c 登记）、N_gen = 3（代）、α_t = ln7 = ln(k_max−1)")
print("  → 系数 = 2⁶·(k_max−1)+N_gen·ln(k_max−1)——全部框架量——'旋量×框架7 + 代数×上型α'")
print()

print("④ 与 m_τ 精化模式对比：")
print("  m_τ 精化：193−3/40（保留 2⁶·3+1 结构 + 计数修正 3/40）——代数修正型")
print("  m_b 精化：2⁶(k_max−1)+N_gen·α_t（换身份）——代数身份型")
print("  共性：均无谱隙修正（a-规则一致）、均含代数/对数结构——修正体系'代数型'扩展")
print("  差异：m_τ 保留原结构加修正、m_b 整体换身份")
print()

print("⑤ 诚实边界：")
print("  m_b 换身份（2¹²/3²−1 → 2⁶·7+3ln7）是替换候选非精化——原结构 +0.0602% 仍达标")
print("  2⁶·(k_max−1) 的机制（为何旋量幂 6、为何 ×7）待论证")
print("  竞争候选 2/3 精度相近（<0.001%）——判别依赖 a-规则（描述性）")
print()
json.dump({"m_b_pdg": m_b_pdg, "coef_new": coef_new, "m_b_new": m_b_new,
           "dev_pct": (m_b_new/m_b_pdg-1)*100,
           "identity": "2^6*(kmax-1)+Ngen*ln(kmax-1)"},
          open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e33_mb_refined.json","w",encoding="utf-8"), indent=2)
print("JSON 落盘 ✓")
print("exit 0")
