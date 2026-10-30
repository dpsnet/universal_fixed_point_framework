# -*- coding: utf-8 -*-
"""ε_μ 身份判别（2026-10-26）：P7-4d 隐藏失配修正项框架化

σ_score 口径重判暴露：I_μ 公式偏差 = I_μ_exp − I_μ_pred = 1.62e-5（m_e/m_μ 窗口 456σ_score）。
本脚本：① 精确确定 ε_μ；② 系统扫描框架组合（≤0.3% 容差）；③ 候选排序。
"""
import math
from itertools import product

# ---- 实验口径 ----
m_e_c, m_mu_c, m_tau_c = 0.51099895069, 105.6583755, 1776.86
I_mu_exp = math.log(m_tau_c/m_mu_c)
I_e_exp  = math.log(m_tau_c/m_e_c)

# ---- 框架公式 ----
sigma = 1/15
s3 = sigma**3
s4 = sigma**4
alpha_v = 16/15 + math.sqrt(2/3)
I_e_pred = 3*math.e - s3*(1+alpha_v)
I_mu_pred_base = math.log(16) + math.e**(-3)

eps_mu = I_mu_exp - I_mu_pred_base
print("=== ε_μ 精确值 ===")
print(f"I_μ_exp     = {I_mu_exp:.10f}")
print(f"I_μ_pred    = {I_mu_pred_base:.10f}  （ln16+e^(−3)）")
print(f"ε_μ = 差    = {eps_mu:.3e}（需要 +{eps_mu:.3e} 修正）")
print(f"1/60000     = {1/60000:.3e}（差 {(1/60000-eps_mu)/eps_mu*100:+.2f}%）")
print()

# ---- 框架常数族 ----
F = {
    "ln(16/15)": math.log(16/15), "ln15": math.log(15), "ln16": math.log(16),
    "ln2": math.log(2), "e^-3": math.e**(-3), "e^-4": math.e**(-4),
    "e^-16": math.e**(-16), "σ³": s3, "σ⁴": s4, "σ⁵": sigma**5,
    "σ³·σ": s3*sigma, "Δλ_min²": (math.sqrt(3)-1)**2, "Δλ_min³": (math.sqrt(3)-1)**3,
    "Δλ³/108": (math.sqrt(3)-1)**3/108, "(3√3-5)/108": (3*math.sqrt(3)-5)/108,
    "1/675": 1/675, "1/3375": 1/3375, "1/50625": 1/50625,
    "√(C_F/2)": math.sqrt(2/3), "√(2/3)": math.sqrt(2/3),
}
ints = [2,3,4,5,7,8,10,11,12,13,14,15,16,20,21,24,27,28,30,32,40,42,48,56,60,
        64,84,100,105,125,128,160,193,210,225,320,3375,50625,60000,675,1000]

print("=== 单量扫描（a×f，|差|≤0.3%） ===")
hits = []
for a in ints:
    for fname, fval in F.items():
        v = a*fval
        rel = (v - eps_mu)/eps_mu
        if abs(rel) <= 3e-3:
            hits.append((abs(rel), f"{a}×{fname}", v, rel))
hits.sort()
for r, name, v, rel in hits[:12]:
    print(f"  {name:22s} = {v:.4e}  差 {rel*100:+.2f}%")

print()
print("=== 两量组合（a×f1 + b×f2，|差|≤0.2%） ===")
hits2 = []
for a in ints:
    for f1n, f1v in F.items():
        for b in ints:
            for f2n, f2v in F.items():
                if f1n == f2n and a == b:
                    continue
                v = a*f1v + b*f2v
                if v <= 0:
                    continue
                rel = (v - eps_mu)/eps_mu
                if abs(rel) <= 2e-3:
                    hits2.append((abs(rel), f"{a}×{f1n} + {b}×{f2n}", v, rel))
hits2.sort()
for r, name, v, rel in hits2[:10]:
    print(f"  {name:38s} = {v:.4e}  差 {rel*100:+.2f}%")

print()
print("=== 关键单量候选核对 ===")
cands = {
    "ln(16/15)²·σ³·13": math.log(16/15)**2*s3*13,
    "e^-3·σ³·(16/15)²": math.e**(-3)*s3*(16/15)**2,
    "e^-3·σ³·(1+α_v)/2": math.e**(-3)*s3*(1+alpha_v)/2,
    "ln(16/15)²·σ³·(k_max+静默)": math.log(16/15)**2*s3*13,
    "σ⁴·(16/15)·3": s4*(16/15)*3,
    "Δλ_min³·σ·8": (math.sqrt(3)-1)**3*sigma*8,
    "σ³·ln2·4": s3*math.log(2)*4,
}
for n, v in cands.items():
    rel = (v - eps_mu)/eps_mu
    print(f"  {n:38s} = {v:.4e}  差 {rel*100:+.2f}%")

print()
print("=== 语义候选：ε_μ 若 = σ³·(16/15)^k·(1+α_v)^j 型 ===")
for k in range(0, 4):
    for j in range(0, 2):
        v = s3*(16/15)**k*(1+alpha_v)**j
        rel = (v - eps_mu)/eps_mu
        print(f"  σ³·(16/15)^{k}·(1+α_v)^{j} = {v:.4e}  差 {rel*100:+.2f}%")
