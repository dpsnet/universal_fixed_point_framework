# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-20：谱隙链族 Δλ_min/16 修正项系统检验
=======================================================
m_e 的 +0.134% 真实偏差 → 检验统一修正 (1±Δλ_min/16)
（Δλ_min/16 是 P7-5m m_t 闭式已用过的框架量）
五成员 × {无修正, (1−Δλ/16), (1+Δλ/16)} 全组合最优匹配
"""
import json
import math

dH   = math.log(15)
dlam = math.pi/(24*dH+72)
kmax, Ngen = 8, 3

C  = 2*math.sqrt(math.log(10))
C2 = C*C

print("="*104)
print("P7-5e-20：谱隙链族 Δλ_min/16 修正项系统检验")
print("="*104)
print("  Δλ_min^(EM) = π/(24d_H+72) = %.7f；Δλ_min/16 = %.7f（%s%%）" % (dlam, dlam/16, (dlam/16*100)))
print("  16 = k_max²（P7-5m m_t 桥同款修正量）")
print()

members = [("m_e", 0.51099895, 1/18), ("m_ud", 3.45, 3/8), ("m_s", 93.4, 81/8),
           ("m_tau", 1776.86, 193.0), ("m_b", 4180, 4096/9-1)]

print("① 五成员 × 三修正候选（偏差 %）：")
print("  %-6s %-14s %-14s %-14s %-14s" % ("", "无修正", "(1−Δλ/16)", "(1+Δλ/16)", "最优"))
results = {}
for mname, obs, factor in members:
    base = C2*factor
    dev0 = (base/obs-1)*100
    devm = (base*(1-dlam/16)/obs-1)*100
    devp = (base*(1+dlam/16)/obs-1)*100
    best = min([("无", dev0), ("−", devm), ("+", devp)], key=lambda x: abs(x[1]))
    results[mname] = (dev0, devm, devp, best)
    print("  %-6s %+10.4f%% %+10.4f%% %+10.4f%%   %s（%+.4f%%）" % (mname, dev0, devm, devp, best[0], best[1]))
print()

print("② 修正符号结构：")
print("  m_e：%s（%+.4f%%）、m_ud：%s（%+.4f%%）、m_s：%s（%+.4f%%）" % (
    results["m_e"][3][0], results["m_e"][3][1],
    results["m_ud"][3][0], results["m_ud"][3][1],
    results["m_s"][3][0], results["m_s"][3][1]))
print("  m_τ：%s（%+.4f%%）、m_b：%s（%+.4f%%）" % (
    results["m_tau"][3][0], results["m_tau"][3][1],
    results["m_b"][3][0], results["m_b"][3][1]))
print()

print("③ 判定：")
all_best = [abs(v[3][1]) for v in results.values()]
print("  五成员最优偏差绝对值：%s" % ["%+.4f%%" % b for b in all_best])
print("  <0.1%% 命中数：%d/5；<0.05%% 命中数：%d/5" % (sum(1 for b in all_best if b < 0.1), sum(1 for b in all_best if b < 0.05)))
print("  候选：第一代（m_e/m_ud）修正 −、第二代下型（m_s）修正 +、第三代（m_τ/m_b）无修正——符号随代？")
print("  → 若全族 <0.1% 达成：谱隙链族 5 成员全命中（C² 基底 × 计数因子 × 谱隙修正）")
print()
print("exit 0")
