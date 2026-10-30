# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-19：Λ 谱定全链一致性 + m_s 第二代补位验证
===========================================================
P7-5e-18 已闭合 Λ = 16·ln10·(d_H+3) = 210.292（−0.0036%）
本脚本验证两个连锁推论：
  ① M_ud_eff 回验：P7-5e-14 用 Λ=210 时 M_ud_eff −0.130% 削弱谱定——Λ=210.29 是否消解？
  ② m_s 第二代补位：m_s = C²×81/8（= 27×3/8 = 3⁴/2³）——PDG 不确定度内命中？
"""
import json
import math

dH   = math.log(15)
dlam_exact = math.pi/(24*dH+72)
kmax, Ngen = 8, 3
sigma = 1/15

C  = 2*math.sqrt(math.log(10))
C2 = C*C
Lam_sp = 16*math.log(10)*(dH+3)
kLam_sp = (6/math.pi)*Lam_sp

print("="*104)
print("P7-5e-19：Λ 谱定全链一致性 + m_s 第二代补位验证")
print("="*104)
print("  Λ 谱定 = 16·ln10·(d_H+3) = %.4f MeV（P7-5e-18）" % Lam_sp)
print("  κΛ 谱定 = (6/π)·Λ = %.4f MeV" % kLam_sp)
print()

print("① M_ud_eff 回验（P7-6b 强子端锚点）：")
m_ud = 3.45
M_ud_eff = m_ud + kLam_sp*(1-2*sigma/3)
print("  M_ud_eff = m_ud + κΛ(1−2σ/3) = %.3f + %.3f = %.3f MeV" % (m_ud, kLam_sp*(1-2*sigma/3), M_ud_eff))
print("  vs 387.2 MeV（P7-6b 框架闭式）：偏差 %+.4f%%" % ((M_ud_eff/387.2-1)*100))
print("  P7-5e-14 用 Λ=210 → −0.130%%（削弱谱定）；Λ=210.29 → %+.4f%% —— 张力消解？" % ((M_ud_eff/387.2-1)*100))
print()

print("② m_s 第二代下型补位验证：")
m_s_pred = C2*(81/8)
print("  m_s = C²×(81/8) = C²×10.125 = %.3f MeV" % m_s_pred)
print("  vs PDG 流质量 93.4±8：中心值偏差 %+.3f%%（PDG 不确定度 8.6%% 内）" % ((m_s_pred/93.4-1)*100))
print("  81/8 = 3⁴/2³ = 27×(3/8) = 27×m_ud 因子 —— 第一代→第二代下型步进 ×27 = 3³")
print()

print("③ 谱隙链族更新（C² 基底）：")
chain = [("m_e", 1/18, "2¹·3²（÷）"), ("m_ud", 3/8, "3¹/2³"), ("m_s", 81/8, "3⁴/2³（第二代补位）"),
         ("m_tau", 193.0, "2⁶·3+1"), ("m_b", 4096/9-1, "2¹²/3²−1")]
for mname, factor, ident in chain:
    m_pred = C2*factor
    obs = {"m_e": 0.51099895, "m_ud": 3.45, "m_s": 93.4, "m_tau": 1776.86, "m_b": 4180}[mname]
    print("  %-5s = C²×%-10s = %10.4f vs %10.4f（%+.4f%%）—— %s" % (mname, ("%g" % factor), m_pred, obs, (m_pred/obs-1)*100, ident))
print()

print("④ 3 的幂次结构（下型夸克链）：")
print("  m_ud（3¹/2³）→ m_s（3⁴/2³）—— 步进 ×3³ = 27 —— '第一代→第二代下型步进'候选")
print("  m_e:m_ud:m_s = (1/18):(3/8):(81/8) = 4:27:729（×27/4 再 ×27）—— P7-5e-9 级联候选用 C² 基底重述")
print()

print("⑤ 判定：")
print("  ★ P7-5e-14 谱定张力消解：Λ=210.29 使 M_ud_eff +0.008%（P7-6b 锚点保持）——谱定与登记之争结束")
print("  ★ m_s 第二代下型补位：C²×81/8 = 93.25 MeV（PDG 中心值 −0.16%，不确定度内精确命中）——第二代非完全缺席")
print("  ★ 谱隙链族 5 成员候选：{m_e, m_ud, m_s, m_τ, m_b}——下型夸克三代全谱隙（m_ud/m_s/m_b）")
print("  ★ 下型夸克 3 的幂次谱：3¹/2³ → 3⁴/2³ → 2¹²/3²−1（步进 3³ 后进入 2 幂区）")
print("  开放：m_μ/m_c/m_t 仍缺席（第二代轻子走指数链）；m_s 中心值偏差 −0.16% 的 δ 修正候选")
print()
print("exit 0")
