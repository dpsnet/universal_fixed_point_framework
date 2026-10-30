# -*- coding: utf-8 -*-
# Phase 104az-79: d_eff 三项结构分解验证
# 62/3 = 16 + 7/2 + 7/6  (胶子 16 + 半缺失对偶 7/2 + 六分缺失对偶 7/6)
# δd_(s) 身份要求 = 7/6 − σ²·2^(−1/4) vs 机制值 2e^{−(5Δλ_min−σ²/9)}
import numpy as np
from fractions import Fraction

N_gen = 3; k_max = 8
sigma = Fraction(1, 15)
sigma_f = 1.0/15.0
dlmin = (np.sqrt(3)-1)/6.0

# --- 1) 62/3 = 16 + 7/2 + 7/6 精确验证
deff = Fraction(62, 3)
d_g = 16          # 胶子部分 (k_max/2)²
d_q_main = Fraction(k_max-1, 2)   # 7/2
d_res = Fraction(k_max-1, 6)      # 7/6
print("=== 1) d_eff 三项结构分解 ===")
print(f"62/3 = {float(deff):.12f}")
print(f"16 + 7/2 + 7/6 = {float(d_g) + float(d_q_main) + float(d_res):.12f}")
print(f"精确相等? {deff == d_g + d_q_main + d_res}")
print(f"  16 = (k_max/2)² = {int(k_max/2)**2}")
print(f"  7/2 = (k_max−1)/2 (半缺失对偶)")
print(f"  7/6 = (k_max−1)/6 (六分缺失对偶)")
print(f"  7·(1/2+1/6) = 7·2/3 = {float(Fraction(7,1)*Fraction(2,3)):.12f} = 14/3 ✓")

# --- 2) δd_(s) 身份要求闭式
dq_cand = Fraction(k_max-1, 2) + sigma**2 * Fraction(2)**Fraction(-1, 4)  # 近似(分数近似2^(−1/4))
# 用浮点更精确
d_q_cand_f = (k_max-1.0)/2.0 + sigma_f**2 * 2.0**(-0.25)
ds_req_f = 7.0/6.0 - sigma_f**2 * 2.0**(-0.25)   # 身份要求 = 7/6 − σ²·2^(−1/4)
msTc_cand = 5.0*dlmin - sigma_f**2/N_gen**2
ds_mech_f = 2.0*np.exp(-msTc_cand)               # 机制值身份
print("\n=== 2) δd_(s) 两候选身份对比 ===")
print(f"身份要求 δd_(s)^req = 7/6 − σ²·2^(−1/4) = {ds_req_f:.12f}")
print(f"机制身份 δd_(s)^mech = 2e^{{−(5Δλ_min−σ²/9)}} = {ds_mech_f:.12f}")
print(f"  差 = {ds_req_f - ds_mech_f:.9f}  (相对 {(ds_req_f/ds_mech_f-1)*100:+.4f}%)")
print(f"  机制值(实际) = 2e^{{−m_s/T_c}} = {2.0*np.exp(-(4.0/9.0)/((62.0/3.0)/(12*np.pi*np.sqrt(2)))**(1.0/3.0)):.12f}")

# --- 3) d_q + δd_(s)^req = 14/3 精确（σ²·2^(−1/4) 抵消）
print("\n=== 3) 抵消验证 ===")
print(f"d_q_cand + δd_(s)^req = {d_q_cand_f + ds_req_f:.12f}")
print(f"14/3 = {14.0/3.0:.12f}  (差 {(d_q_cand_f+ds_req_f)/(14.0/3.0)-1:.2e})")
print(f"  σ²·2^(−1/4) 在 d_q 为 +，在 δd_(s)^req 为 −，抵消 ✓")

# --- 4) 62 双形式等价
print("\n=== 4) 62 双形式 ===")
print(f"62 = 2^6−2 = {2**6-2} (104az-75 计数谱)")
print(f"62 = 3×16 + 3×7/2 + 3×7/6 = {3*16 + 3*7/2 + 3*7/6} (本轮结构)")
print(f"  等价? {2**6-2 == 3*16 + 3*7/2 + 3*7/6}")

# --- 5) 结构三项 vs 身份三项对照
print("\n=== 5) 结构 vs 身份三项对照 ===")
ds_struct = 2.0*np.exp(-msTc_cand)
print(f"身份: 16 + 7/2 + 7/6 = {16+3.5+7.0/6.0:.9f}")
print(f"结构: 16 + d_q_cand + δd_(s)^mech = {16+d_q_cand_f+ds_mech_f:.9f}")
print(f"  d_q_cand vs 7/2: {d_q_cand_f:.9f} vs 3.5 (修正 {sigma_f**2*2.0**(-0.25):.9f})")
print(f"  δd_(s)^mech vs 7/6: {ds_mech_f:.9f} vs {7.0/6.0:.9f}")
print(f"  6.5% 差 = 机制项偏离身份分解项")

# --- 6) 6.5% 差分解尝试
ratio = ds_req_f/ds_mech_f
print(f"\n=== 6) 6.5% 差分解 ===")
print(f"δd_(s)^req/δd_(s)^mech = {ratio:.9f}")
print(f"  ln(ratio) = {np.log(ratio):.9f}  (σ = {sigma_f:.9f}, 比 {np.log(ratio)/sigma_f:.6f})")
print(f"  1/(1−σ) = {1/(1-sigma_f):.9f} (比 {ratio/(1/(1-sigma_f)):.6f})")
print(f"  (1+σ) = {1+sigma_f:.9f} (比 {ratio/(1+sigma_f):.6f})")
print(f"  16/15 = {16.0/15.0:.9f} (比 {ratio/(16.0/15.0):.6f})")
