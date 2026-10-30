# -*- coding: utf-8 -*-
"""ε_e 身份判别（2026-10-26）：m_e 链次级失配（12.6σ_score 残余）

ε_e = I_e_exp − I_e_pred = 8.1539907828 − 8.1539912148 = −4.32e-7
候选：−5σ⁶ = −4.39e-7（差 1.6%）——系统扫描验证 + 更优组合搜索。
"""
import math
from itertools import product

m_e_c, m_mu_c, m_tau_c = 0.51099895069, 105.6583755, 1776.86
sigma = 1/15
s3 = sigma**3
alpha_v = 16/15 + math.sqrt(2/3)
I_e_pred = 3*math.e - s3*(1+alpha_v)
I_e_exp = math.log(m_tau_c/m_e_c)
eps_e = I_e_exp - I_e_pred
print(f"I_e_pred = {I_e_pred:.10f}、I_e_exp = {I_e_exp:.10f}")
print(f"ε_e = {eps_e:+.4e}（需负修正 {abs(eps_e):.4e}）")
print()

# ---- 候选核对 ----
print("=== 已知候选核对 ===")
cands = {
    "−5σ⁶": -5*sigma**6,
    "−σ⁶×5（同）": -5*sigma**6,
    "−e^−15": -math.e**(-15),
    "−σ⁶×5×(16/15)²": -5*sigma**6*(16/15)**2,
    "−σ⁵×(16/15)³/3": -sigma**5*(16/15)**3/3,
    "−σ³·ln(16/15)/16": -s3*math.log(16/15)/16,
    "−σ³·ln(16/15)/32": -s3*math.log(16/15)/32,
    "−σ³·σ³·4": -s3*s3*4,
    "−σ³·e^−3/2": -s3*math.e**(-3)/2,
}
for n, v in cands.items():
    rel = (v-eps_e)/abs(eps_e)
    print(f"  {n:26s} = {v:+.4e}  差 {rel*100:+.2f}%")

print()
# ---- 系统扫描：a×f（|差|≤3%）----
F = {
    "σ⁴": sigma**4, "σ⁵": sigma**5, "σ⁶": sigma**6, "σ⁷": sigma**7, "σ⁸": sigma**8,
    "e^-14": math.e**(-14), "e^-15": math.e**(-15), "e^-16": math.e**(-16), "e^-17": math.e**(-17),
    "ln(16/15)": math.log(16/15), "ln(16/15)²": math.log(16/15)**2,
    "ln2": math.log(2), "ln(16/15)³": math.log(16/15)**3,
    "Δλ³/108": (math.sqrt(3)-1)**3/108, "(3√3-5)/108": (3*math.sqrt(3)-5)/108,
}
ints = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,20,24,27,30,32,40,48,56,60,64,100,128]
tgt = abs(eps_e)
print("=== 单量 a×f（|差|≤3%） ===")
hits = []
for a in ints:
    for fn, fv in F.items():
        v = a*fv
        rel = (v-tgt)/tgt
        if abs(rel) <= 0.03:
            hits.append((abs(rel), f"{a}×{fn}", v, rel))
hits.sort()
for r, n, v, rel in hits[:12]:
    print(f"  {n:16s} = {v:.4e}  差 {rel*100:+.2f}%")

print()
print("=== 两量组合（|差|≤1%） ===")
hits2 = []
for a in ints:
    for f1n, f1v in F.items():
        for b in ints:
            for f2n, f2v in F.items():
                if f1n == f2n and a == b: continue
                v = a*f1v + b*f2v
                if v <= 0: continue
                rel = (v-tgt)/tgt
                if abs(rel) <= 0.01:
                    hits2.append((abs(rel), f"{a}×{f1n} + {b}×{f2n}", v, rel))
hits2.sort()
for r, n, v, rel in hits2[:12]:
    print(f"  {n:34s} = {v:.4e}  差 {rel*100:+.2f}%")

print()
# ---- 结构性判别：ε_e/ε_μ 比例 ----
print("=== ε_e 与 ε_μ 结构关联 ===")
eps_mu = 144*math.e**(-16)
print(f"ε_e/ε_μ = {eps_e/eps_mu:.4f}（≈ −1/37.6）")
print(f"ε_e 若 = −ε_μ×σ⁴×3? : {-eps_mu*sigma**4*3:.4e}（差 {(-eps_mu*sigma**4*3-eps_e)/abs(eps_e)*100:+.1f}%）")
print(f"ε_e 若 = −ε_μ×σ²/9? : {-eps_mu*sigma**2/9:.4e}（差 {(-eps_mu*sigma**2/9-eps_e)/abs(eps_e)*100:+.1f}%）")
print(f"ε_e 若 = −ε_μ×ln(16/15)²? : {-eps_mu*math.log(16/15)**2:.4e}（差 {(-eps_mu*math.log(16/15)**2-eps_e)/abs(eps_e)*100:+.1f}%）")
print(f"ε_e 若 = −ε_μ×σ⁴×8? : {-eps_mu*sigma**4*8:.4e}（差 {(-eps_mu*sigma**4*8-eps_e)/abs(eps_e)*100:+.1f}%）")
