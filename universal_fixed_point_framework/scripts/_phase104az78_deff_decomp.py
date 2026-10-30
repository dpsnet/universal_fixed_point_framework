# -*- coding: utf-8 -*-
# Phase 104az-78: d_eff 身份新分解验证
# 候选A: 62/3 = N_gen·(k_max−1) − (k_max−3)·σ = 21 − 5σ
# 候选B: 14/3 = 5(1−σ) = (k_max−3)(1−σ)
# 5 = k_max−3 三处重复检验
import numpy as np
from fractions import Fraction

N_gen = 3; k_max = 8
sigma = Fraction(1, 15)
dlmin = (np.sqrt(3)-1)/6.0

# --- 候选A: 62/3 = 21 − 5σ
deff_id = Fraction(62, 3)
exprA = N_gen*(k_max-1) - (k_max-3)*sigma
print(f"候选A: 62/3 = {float(deff_id):.12f}")
print(f"  N_gen·(k_max−1) − (k_max−3)·σ = 3×7 − 5×(1/15) = {float(exprA):.12f}")
print(f"  精确相等? {deff_id == exprA}  (有理数精确比较)")
print(f"  21 − 5σ = 21 − {float(5*sigma):.6f} = {float(21-5*sigma):.12f}")

# --- 候选B: 14/3 = 5(1−σ)
id143 = Fraction(14, 3)
exprB = (k_max-3)*(1-sigma)
print(f"\n候选B: 14/3 = {float(id143):.12f}")
print(f"  (k_max−3)(1−σ) = 5×(1−1/15) = 5×14/15 = {float(exprB):.12f}")
print(f"  精确相等? {id143 == exprB}")

# --- d_eff 双分解
exprC = 16 + 5*(1-sigma)
print(f"\nd_eff = 16 + 5(1−σ) = {float(exprC):.12f} vs 62/3 = {float(deff_id):.12f}")
print(f"  精确相等? {deff_id == exprC}")

# --- 5 = k_max−3 三处重复
print(f"\n5 = k_max−3 三处出现:")
print(f"  ① m_s/T_c = 5Δλ_min − σ²/9 (104az-77)")
print(f"  ② δd_(s) 旧候选 1+5Δλ_min/7 (104az-76, 后被指数形式替代)")
print(f"  ③ 14/3 = 5(1−σ) (本轮)")

# --- 残余重新表达: 残余 = 21 − 5σ − 16 − d_q_cand − ds_cand
sigma_f = 1.0/15.0
d_q_cand = (k_max-1.0)/2.0 + sigma_f**2*2.0**(-0.25)
msTc_cand = 5.0*dlmin - sigma_f**2/N_gen**2
ds_cand = 2.0*np.exp(-msTc_cand)
resid = float(deff_id) - 16.0 - d_q_cand - ds_cand
print(f"\n残余 = 62/3 − 16 − d_q_cand − ds_cand = {resid:.12f}")
print(f"  展开: 5(1−σ) − [7/2 + σ²·2^(−1/4)] − 2e^{{−(5Δλ_min−σ²/9)}}")
print(f"       = 3/2 − 5σ − σ²·2^(−1/4) − 2e^{{−...}}")
print(f"       = {1.5 - 5*sigma_f - sigma_f**2*2.0**(-0.25) - ds_cand:.12f}")

# --- 残余候选分解再搜
print(f"\n残余候选分解:")
print(f"  残余/σ = {resid/sigma_f:.9f}")
print(f"  残余/σ² = {resid/sigma_f**2:.9f}")
print(f"  残余/σ³ = {resid/sigma_f**3:.9f}")
print(f"  残余/Δλ_min = {resid/dlmin:.9f}")
print(f"  残余 × 225 = {resid*225:.9f}")
print(f"  残余 × 3375 = {resid*3375:.9f}")
print(f"  256σ³ = {256*sigma_f**3:.12f} (差 {(resid/(256*sigma_f**3)-1)*100:+.6f}%)")
print(f"  (25/22)σ = {25/22*sigma_f:.12f} (差 {(resid/(25/22*sigma_f)-1)*100:+.6f}%)")
print(f"  5σ²·(1+2^(−1/4)) = {5*sigma_f**2*(1+2.0**(-0.25)):.12f} (差 {(resid/(5*sigma_f**2*(1+2.0**(-0.25)))-1)*100:+.6f}%)")

# --- 结构 d_eff 与 21−5σ 的关系
deff_struct_full = 16.0 + d_q_cand + ds_cand
print(f"\n21 − 结构 = {21.0 - deff_struct_full:.9f}  vs 5σ = {5*sigma_f:.9f}")
print(f"  (21−结构) − 5σ = {21.0 - deff_struct_full - 5*sigma_f:.9f} = 残余 ✓")
