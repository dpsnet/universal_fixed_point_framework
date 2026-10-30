# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-9：质量比值闭式族扫描——m_i/m_j = 代数计数闭式 系统检验
=========================================================================
P7-5e-8 的 m_e/m_ud = 4/27（0.02%）若孤立可能是巧合——扩展为全比值系统扫描：
8 质量（3 轻子 + 5 夸克/流质量）× 全对 = 28 个比值 vs 代数闭式库（k_max/N_gen 计数系）。
判定：≥3 个 <0.1% 命中 → "质量比 = 代数计数闭式"族成形（非孤立）。
"""
import json
import math

dH = math.log(15)
sig = 1/15

# 质量 (名称, MeV, 依赖)
M = [
    ("m_e",  0.51099895, "实验"),
    ("m_μ", 105.658375, "实验"),
    ("m_τ", 1776.86,    "实验"),
    ("m_ud", 3.45,       "PDG 流"),
    ("m_s", 93.4,        "PDG 流"),
    ("m_c", 1270,        "PDG 流"),
    ("m_b", 4180,        "PDG 流"),
    ("m_t", 172690,      "PDG 流"),
]

# 代数闭式库（k_max=8、N_gen=3 计数系 + 少量谱量）
CAND = {}
ints = list(range(1, 41)) + [64, 81, 100, 128, 200, 205, 206, 207, 256]
for i in ints:
    CAND[str(i)] = float(i)
    CAND["1/%d" % i] = 1.0/i
# k_max/N_gen 计数组合
CAND["k_max/N_gen"] = 8/3
CAND["N_gen/k_max"] = 3/8
CAND["k_max/(2·N_gen²)"] = 8/18
CAND["2·N_gen²"] = 18.0
CAND["(k_max−1)/N_gen"] = 7/3
CAND["N_gen/(k_max−1)"] = 3/7
CAND["(k_max−3)/(k_max−1)"] = 5/7
CAND["(k_max−2)/(k_max−1)"] = 6/7
CAND["k_max/(k_max+1)"] = 8/9
CAND["(k_max−1)/(k_max+1)"] = 7/9
CAND["N_gen²"] = 9.0
CAND["N_gen³"] = 27.0
CAND["1/N_gen³"] = 1/27
CAND["N_gen⁴"] = 81.0
CAND["k_max²"] = 64.0
CAND["k_max²+N_gen"] = 67.0
CAND["k_max²−N_gen"] = 61.0
CAND["k_max²−1"] = 63.0
CAND["k_max²+1"] = 65.0
CAND["2·k_max"] = 16.0
CAND["2·k_max−1"] = 15.0
CAND["2·k_max+1"] = 17.0
CAND["3·k_max"] = 24.0
CAND["3·k_max−1"] = 23.0
CAND["2·N_gen²+1"] = 19.0
CAND["3·N_gen²"] = 27.0
CAND["4/27"] = 4/27
CAND["2²/3³"] = 4/27
CAND["3·69"] = 207.0
CAND["41·5"] = 205.0
CAND["(k_max²+k_max−3)·N_gen"] = 207.0
CAND["41"] = 41.0
CAND["41/3"] = 41/3
CAND["8·(5+1/8)"] = 41.0
CAND["dH"] = dH
CAND["dH/2"] = dH/2
CAND["2·dH"] = 2*dH
CAND["σ"] = sig
CAND["1/σ"] = 1/sig
CAND["1/(2σ)"] = 1/(2*sig)
CAND["1/(2σ/3)"] = 1/(2*sig/3)

print("="*100)
print("P7-5e-9：质量比值闭式族扫描——m_i/m_j = 代数计数闭式 系统检验")
print("="*100)
print("%-16s %-12s %-24s %s" % ("比值", "数值", "最佳闭式", "偏差"))
rows = []
for i in range(len(M)):
    for j in range(i+1, len(M)):
        ni, mi, di = M[i]
        nj, mj, dj = M[j]
        r = mi/mj
        # 候选闭式
        best = None
        for cname, cval in CAND.items():
            dev = abs(r - cval)/r*100
            if best is None or dev < best[1]:
                best = (cname, dev)
        rows.append((ni+"/"+nj, r, best[0], best[1]))
# 按偏差排序，先显示命中
rows.sort(key=lambda x: x[3])
for name, r, c, d in rows:
    tag = "★" if d < 0.1 else ("·" if d < 1 else " ")
    print("%s%-15s %-12.6f %-24s %5.2f%%" % (tag, name, r, c, d))

hits = [r for r in rows if r[3] < 0.1]
print()
print("★ <0.1%% 命中：%d/28" % len(hits))
for name, r, c, d in hits:
    print("   %s = %.6f ≈ %s（%.2f%%）" % (name, r, c, d))
print()
print("判定：")
if len(hits) >= 3:
    print("  ≥3 个独立命中 → '质量比 = 代数计数闭式'族成形（非孤立）")
else:
    print("  <3 个独立命中 → m_e/m_ud = 4/27 仍可能孤立（族未成形）")
print("  注意：m_c/m_s/m_b/m_t 为 PDG 流质量（±10-30 MeV 不确定度）——含流质量的命中可信度受限")
print()
print("exit 0")
