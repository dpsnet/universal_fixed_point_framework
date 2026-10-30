# -*- coding: utf-8 -*-
"""假设 D 验证：α_v 的 √(2/3) 项修正 η 身份（2026-10-26）

I_e 失配替代解释：I_e' = 3e − σ³(1 + α_v')——α_v' = 16/15 + √(2/3)(1−η)
需要 η 使 I_e' = I_e_exp。扫描 η 的框架身份。
"""
import math
from itertools import product

sigma = 1/15
s2 = sigma**2; s3 = sigma**3
sqrt23 = math.sqrt(2/3)
I_e_pred = 3*math.e - s3*(1 + 16/15 + sqrt23)
m_e_c, m_tau_c = 0.51099895069, 1776.86
I_e_exp = math.log(m_tau_c/m_e_c)
dI = I_e_pred - I_e_exp          # +4.32e-7
eta = dI/(s3*sqrt23)             # η = dI/(σ³√(2/3))
print(f"I_e_pred = {I_e_pred:.10f}、I_e_exp = {I_e_exp:.10f}、dI = {dI:+.4e}")
print(f"η_needed = {eta:.6e}（√(2/3) 项修正因子 (1−η)）")
print()

# ---- η 候选 ----
print("=== η 单量候选核对 ===")
cands = {
    "σ²×2/5": s2*2/5,
    "σ²×(1+σ²)×2/5": s2*(1+s2)*2/5,
    "σ³×6": s3*6,
    "σ³×(静默+1)": s3*6,
    "σ³×静默×1.2": s3*5*1.2,
    "σ²/静默/2.8": s2/5/2.8,
    "σ³×2√2": s3*2*math.sqrt(2),
    "ln(16/15)/36": math.log(16/15)/36,
    "ln(16/15)²×静默²": math.log(16/15)**2*25,
    "σ²×(16/15)×3/16": s2*(16/15)*3/16,
}
for n, v in cands.items():
    rel = (v-eta)/eta
    print(f"  {n:26s} = {v:.6e}  差 {rel*100:+.2f}%")

print()
# ---- 系统扫描：η = a×σ²×b/5 型 / a×σ^k ----
F = {"σ²": s2, "σ³": s3, "σ⁴": sigma**4, "σ²(1+σ²)": s2*(1+s2),
     "σ²(1+2σ²)": s2*(1+2*s2), "σ³(1+σ³)": s3*(1+s3), "ln(16/15)": math.log(16/15),
     "ln(16/15)²": math.log(16/15)**2, "e^-5": math.e**(-5), "e^-6": math.e**(-6)}
ints = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,20,24,30,32,40,48,56,60,64]
print("=== 单量 a×f（|差|≤2%） ===")
hits = []
for a in ints:
    for fn, fv in F.items():
        v = a*fv
        rel = (v-eta)/eta
        if abs(rel) <= 0.02:
            hits.append((abs(rel), f"{a}×{fn}", v, rel))
hits.sort()
for r, n, v, rel in hits[:12]:
    print(f"  {n:18s} = {v:.6e}  差 {rel*100:+.2f}%")
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
                rel = (v-eta)/eta
                if abs(rel) <= 0.01:
                    hits2.append((abs(rel), f"{a}×{f1n} + {b}×{f2n}", v, rel))
hits2.sort()
for r, n, v, rel in hits2[:10]:
    print(f"  {n:30s} = {v:.6e}  差 {rel*100:+.2f}%")

print()
# ---- 修正后 σ 数（用最优候选 η 代入）----
# 方向修正：I_e 需减小 → α_v 需增大 → √(2/3) 项 (1+η)
eta_best = 6*s3          # η = 6σ³ = N_gen!·σ³
av_new = 16/15 + sqrt23*(1+eta_best)
I_e_new = 3*math.e - s3*(1+av_new)
rel_e = 2.935e-8
print(f"=== 假设 D 验证（η = +6σ³ = N_gen!·σ³）===")
print(f"I_e' = {I_e_new:.10f} vs 实验 {I_e_exp:.10f}")
print(f"σ（无 m_τ 窗口精度） = {abs(I_e_new-I_e_exp)/(I_e_exp*rel_e):.1f}（原 {abs(dI)/(I_e_exp*rel_e):.1f}σ）")
print(f"√(2/3) 修正 = +{sqrt23*eta_best:.4e}（绝对）——α_v' = {av_new:.6f}")
print()

# ---- 完整双修正体系：m_e/m_μ 窗口残余 ----
eps_mu = 144*math.e**(-16)
I_mu_prime = math.log(16) + math.e**(-3) + eps_mu
I_em_prime = I_e_new - I_mu_prime
m_mu_c = 105.6583755
I_em_exp = math.log(m_mu_c/m_e_c)
rel_cross = math.sqrt(rel_e**2+2.177e-8**2)
print("=== 双修正体系（α_v 修正 + ε_μ）m_e/m_μ 窗口 ===")
print(f"I_e'−I_μ' = {I_em_prime:.10f} vs 实验 {I_em_exp:.10f}")
print(f"σ_score = {abs(I_em_prime-I_em_exp)/rel_cross:.1f}（原 456σ_score → ε_μ 后 12.6σ_score → 双修正后？）")
print()
print("=== ε_μ 精确值核对（修正后 I_μ 偏差） ===")
print(f"I_μ'−I_μ_exp = {I_mu_prime-2.8223920238:+.3e}")

