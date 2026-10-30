# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-10：m_e-m_ud 闭合四边形交叉验证
================================================
m_ud 的两条独立框架路径 + m_e 的谱隙路径 + 比值恒等式：
  路径 A（代数比值）：m_ud = (27/4)·m_e —— m_e:m_ud = 2²:3³（P7-5e-8）
  路径 B（谱隙链）：  m_ud = κΛ·Δλ_min^(EM)·(3/8)（P7-5e-7/8）
  路径 C（谱隙链）：  m_e  = κΛ·Δλ_min^(EM)/18（P7-5e-8）
  恒等式：A/B/C 两两兼容 ⇔ m_e:m_ud = 4:27（A 是 B、C 的推论）
检验：两路径对 m_ud 的预测差（交叉验证残差）、三等式闭合一致性。
"""
import json
import math

dH   = math.log(15)
kap  = 6/math.pi
Lam  = 210.3
kLam = kap*Lam
dlam_reg   = 0.0229                     # Δλ_min^(EM) 登记值
dlam_exact = math.pi/(24*dH+72)         # P7-5l 框架推导精确值
m_e_exp  = 0.51099895
m_ud_pdg = 3.45

print("="*104)
print("P7-5e-10：m_e-m_ud 闭合四边形交叉验证")
print("="*104)
print("  框架量：κΛ = %.4f MeV（Λ = 210.3 登记）" % kLam)
print("  Δλ_min^(EM)：登记 %.4f / 框架精确 %.7f（π/(24d_H+72)，P7-5l）" % (dlam_reg, dlam_exact))
print()

rows = []
for dlam_name, dlam in [("登记值口径", dlam_reg), ("框架精确值口径", dlam_exact)]:
    print("── %s ──" % dlam_name)
    # 路径 C：m_e = κΛ·Δλ_min/18
    m_e_C = kLam*dlam/18
    # 路径 B：m_ud = κΛ·Δλ_min·3/8
    m_ud_B = kLam*dlam*3/8
    # 路径 A：m_ud = 27/4·m_e
    m_ud_A_exp = 27/4*m_e_exp
    m_ud_A_C  = 27/4*m_e_C
    print("  路径 C（m_e = κΛΔλ/18）      = %.6f vs 实验 %.6f（%+.4f%%）" % (m_e_C, m_e_exp, (m_e_C/m_e_exp-1)*100))
    print("  路径 B（m_ud = κΛΔλ·3/8）    = %.6f vs PDG %.6f（%+.4f%%）" % (m_ud_B, m_ud_pdg, (m_ud_B/m_ud_pdg-1)*100))
    print("  路径 A（m_ud = 27/4·m_e）     = %.6f（用实验 m_e）/ %.6f（用路径 C m_e）" % (m_ud_A_exp, m_ud_A_C))
    dev_AB = abs(m_ud_A_C - m_ud_B)/m_ud_B*100
    print("  ★ 交叉验证：|m_ud(A) − m_ud(B)|/m_ud = %.4f%%" % dev_AB)
    rows.append((dlam_name, m_e_C, m_ud_B, m_ud_A_exp, m_ud_A_C, dev_AB))

print()
print("闭合四边形：")
print("  m_e ──×27/4──→ m_ud（代数比值 4:27，Δλ_min 消去）")
print("    ↑                    ↑")
print("    ÷18                  ×3/8")
print("  κΛ·Δλ_min^(EM) ←──────┘（同一基底）")
print()
print("  恒等式检验：m_e:m_ud = (κΛΔλ/18):(κΛΔλ·3/8) = (1/18):(3/8) = 8:54 = 4:27 ✓（代数闭合）")
print()
print("判定（诚实区分恒等式 vs 独立交叉验证）：")
print("  ★ 族内代数闭合（必然恒等式）：m_e:m_ud = (1/18):(3/8) = 4:27——27/4×1/18 = 3/8 使 A、B 在框架内是同一族")
print("  ★ 独立交叉验证（真实）：实验 m_e = 0.510999 命中路径 C（κΛΔλ/18，登记值口径 −0.004%%）")
print("                          PDG m_ud = 3.450 命中路径 B（κΛΔλ·3/8，登记值口径 −0.026%%）")
print("                          —— 两个独立测量值分别落在同族框架结构上（输入无交集：m_e 实验 vs κΛ/Δλ_min 框架量）")
print("  ★ m_ud 内生化进展：从纯外部输入 → 框架族交叉点（比值 4/27 消去谱隙、精度无关）")
print("  绝对标度精度边界：框架精确值口径 m_e +0.14%%/m_ud +0.12%%（0.1%% 边缘）——受 κΛ（Λ=210.3）与 Δλ_min^(EM) 精度限制")
print("  第一代专属：m_μ/m_s（第二代）不在四边形（m_μ 走 e 指数链 206.77、m_s 级联 0.27%% 不达标）")
print("  —— '代数比四边形'为第一代结构签名（候选）")
print()
print("exit 0")
