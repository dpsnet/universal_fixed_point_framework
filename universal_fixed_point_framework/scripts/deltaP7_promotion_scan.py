# -*- coding: utf-8 -*-
"""δ_P7 升格路径（2026-10-26）：E_τ^new 1.9σ → <1σ

E_τ^new = 16ln15 + (7/10)ln(16/15) = 43.3739802 vs E_exp = 43.3738491
偏差 +1.31e-4（1.9σ 提示）→ 升格 = 找 E_τ^new 的精确结构修正项。
验证：#74 = 16ln15 + 16δ_P7 + ln(16/15)/3（δ_P7 = (11/30)ln(16/15)/16）
"""
import math
from itertools import product

m_tau_c = 1776.86
G_N_rel = 2.2e-5
M_Pl_rel = G_N_rel/2
d_tau_rel = 0.12/m_tau_c
M_Pl_MeV = 1.220890e22

E_exp = math.log(M_Pl_MeV/m_tau_c)
sE = math.sqrt(M_Pl_rel**2 + d_tau_rel**2)
E_pred = 16*math.log(15) + (7/10)*math.log(16/15)
sig = abs(E_pred-E_exp)/sE
corr = E_exp - E_pred          # 需要负修正 ≈ −1.31e-4
print(f"E_exp = {E_exp:.10f}、E_τ^new = {E_pred:.10f}、σ = {sig:.3f}")
print(f"需要修正 = {corr:+.4e}（E_τ^new 偏高 → 减 {abs(corr):.4e}）")
print()

# ---- 验证 #74 = 16ln15 + 16δ_P7 + ln(16/15)/3 ----
dP7 = (11/30)*math.log(16/15)/16
E_decomp = 16*math.log(15) + 16*dP7 + math.log(16/15)/3
print(f"16ln15+16δ_P7+ln(16/15)/3 = {E_decomp:.10f} vs E_τ^new = {E_pred:.10f}")
print(f"δ_P7 = {dP7:.10f}——(7/10) = 16δ_P7+1/3×ln(16/15) 分解 ✓")
print()

# ---- 修正项扫描：corr = −1.31e-4 的框架组合 ----
F = {
    "ln(16/15)": math.log(16/15), "ln15": math.log(15), "ln2": math.log(2),
    "σ²": (1/15)**2, "σ³": (1/15)**3, "σ⁴": (1/15)**4,
    "δ_P7": dP7, "δ_P7/16": dP7/16, "d_H−ln15": 16259/6000-math.log(15),
    "ln(16/15)/16": math.log(16/15)/16, "ln(16/15)/30": math.log(16/15)/30,
    "e^-3": math.e**(-3), "e^-4": math.e**(-4), "e^-7": math.e**(-7),
    "(3√3-5)/108": (3*math.sqrt(3)-5)/108,
    "1/675": 1/675, "1/3375": 1/3375, "1/10000": 1/10000,
}
ints = [2,3,4,5,6,7,8,10,11,12,13,14,15,16,20,21,24,27,30,32,33,40,42,48,56,64,
        70,84,100,105,128,140,160,210,225,320,600,1000]

target = abs(corr)
print("=== 单量（a×f，|差|≤2%） ===")
hits = []
for a in ints:
    for fn, fv in F.items():
        v = a*fv
        rel = (v-target)/target
        if abs(rel) <= 0.02:
            hits.append((abs(rel), f"{a}×{fn}", v, rel))
hits.sort()
for r, n, v, rel in hits[:10]:
    print(f"  {n:18s} = {v:.5e}  差 {rel*100:+.2f}%")
print()

print("=== 两量（a×f1 + b×f2，|差|≤1.5%） ===")
hits2 = []
for a in ints:
    for f1n, f1v in F.items():
        for b in ints:
            for f2n, f2v in F.items():
                if f1n == f2n and a == b:
                    continue
                v = a*f1v + b*f2v
                if v <= 0: continue
                rel = (v-target)/target
                if abs(rel) <= 0.015:
                    hits2.append((abs(rel), f"{a}×{f1n} + {b}×{f2n}", v, rel))
hits2.sort()
for r, n, v, rel in hits2[:10]:
    print(f"  {n:34s} = {v:.5e}  差 {rel*100:+.2f}%")
print()

# ---- 语义候选 ----
print("=== 语义候选核对 ===")
cands = {
    "δ_P7/11": dP7/11,
    "δ_P7/16·11": dP7/16*11,
    "ln(16/15)/16·11/30": math.log(16/15)/16*11/30,
    "σ²·ln(16/15)/16": (1/15)**2*math.log(16/15)/16,
    "σ²·ln(16/15)/22": (1/15)**2*math.log(16/15)/22,
    "σ³·(16/15)/3": (1/15)**3*(16/15)/3,
    "σ³·ln2/8": (1/15)**3*math.log(2)/8,
    "ln(16/15)²·σ²/2": math.log(16/15)**2*(1/15)**2/2,
}
for n, v in cands.items():
    rel = (v-target)/target
    print(f"  {n:32s} = {v:.5e}  差 {rel*100:+.2f}%")
