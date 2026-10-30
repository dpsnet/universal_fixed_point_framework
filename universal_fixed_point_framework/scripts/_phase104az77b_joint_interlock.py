# -*- coding: utf-8 -*-
# Phase 104az-77b: d_q + δd_(s) 候选联合互锁检验
import numpy as np

N_c = 3.0; N_f = 3.0; N_gen = 3.0; k_max = 8.0
sigma = 1.0/15.0
C_F = (N_c**2 - 1)/(2*N_c)
dlmin = (np.sqrt(3) - 1)/6.0
pi = np.pi

# --- a₀ 身份 (104az-75)
deff_id = (k_max**2 - 2)/3.0
a0_id = (deff_id/(12*pi*np.sqrt(2)))**(1.0/3.0)

# --- 结构组件 (104az-72/76 定义)
# d_q 结构 = Nf·Nc·(C_F/2)·√(dlmin/dl3)·(1/Z2), Z2=(6/5)²
Z2 = (6.0/5.0)**2
d_q_struct = N_f*N_c*(C_F/2.0)*np.sqrt(dlmin/(np.sqrt(2)*dlmin))*(1.0/Z2)
msTc_actual = (C_F/2.0)**2/a0_id
ds_struct = 2.0*np.exp(-msTc_actual)
print(f"结构: d_q = {d_q_struct:.12f},  δd_(s) = {ds_struct:.12f},  和 = {d_q_struct+ds_struct:.12f}")

# --- 候选身份
d_q_cand = (k_max-1.0)/2.0 + sigma**2*np.sqrt(dlmin/(np.sqrt(2)*dlmin))
msTc_cand = 5.0*dlmin - sigma**2/N_gen**2
ds_cand = 2.0*np.exp(-msTc_cand)
print(f"候选: d_q = {d_q_cand:.12f},  δd_(s) = {ds_cand:.12f},  和 = {d_q_cand+ds_cand:.12f}")

# --- 联合互锁
sum_struct = d_q_struct + ds_struct
sum_cand = d_q_cand + ds_cand
dev_sum = (sum_cand/sum_struct - 1)*100
print(f"\n★★ 联合互锁: 候选和/结构和 相对差 = {dev_sum:+.7f}%  (锁定级 <0.0001%?)")

# 组件级
dev_dq = (d_q_cand/d_q_struct - 1)*100
dev_ds = (ds_cand/ds_struct - 1)*100
print(f"组件级: d_q {dev_dq:+.6f}%,  δd_(s) {dev_ds:+.6f}%")

# --- 联合身份目标判别
targets = {
    "N_gen²/2 + 3Δλ_min/4": N_gen**2/2.0 + 3.0*dlmin/4.0,
    "14/3 (paper17 分解)": 14.0/3.0,
}
print(f"\n联合候选和 = {sum_cand:.12f}")
for name, val in targets.items():
    print(f"  vs {name} = {val:.12f}: dev {(sum_cand/val-1)*100:+.6f}%")

# --- 结构 d_eff vs 身份 d_eff
deff_struct = 16.0 + sum_struct
deff_cand = 16.0 + sum_cand
print(f"\nd_eff 结构 = 16 + 结构和 = {deff_struct:.12f}")
print(f"d_eff 候选 = 16 + 候选和 = {deff_cand:.12f}")
print(f"d_eff 身份 = 62/3 = {deff_id:.12f}")
print(f"  结构/身份 dev = {(deff_struct/deff_id-1)*100:+.6f}%")
print(f"  候选/身份 dev = {(deff_cand/deff_id-1)*100:+.6f}%")

# --- 残余 0.0757 分解尝试
resid = deff_id - deff_cand
print(f"\n残余 d_eff 身份−候选 = {resid:.10f}")
print(f"  残余/σ² = {resid/sigma**2:.6f}  (σ²=1/225=0.004444)")
print(f"  残余/Δλ_min = {resid/dlmin:.6f}")
print(f"  残余×225 = {resid*225:.8f}")
print(f"  残余×2025 = {resid*2025:.6f}")

# --- Z2 互锁复验 (用候选 d_q)
Z2_star = N_f*N_c*(C_F/2.0)*np.sqrt(dlmin/(np.sqrt(2)*dlmin))/d_q_cand
print(f"\nZ2* (用候选 d_q) = {Z2_star:.12f} vs (6/5)² = {Z2**0.5*Z2**0.5:.12f} (={Z2:.6f})")
print(f"  dev = {(Z2_star/Z2-1)*100:+.7f}%")
