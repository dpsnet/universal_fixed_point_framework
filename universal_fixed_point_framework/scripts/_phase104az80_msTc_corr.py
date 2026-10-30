# -*- coding: utf-8 -*-
# Phase 104az-80: m_s/T_c 修正项精确化验证
# 候选: 修正项 = σ²/9 · (1 − 1/320), 320 = k_max²·(k_max−3) = 64×5
# m_s/T_c = 5Δλ_min − 319/648000, 319 = k_max²(k_max−3)−1, 648000 = k_max²·N_gen⁴·(k_max−3)³
import numpy as np

N_gen = 3.0; k_max = 8.0
sigma = 1.0/15.0
dlmin = (np.sqrt(3)-1)/6.0
pi = np.pi

# --- a₀ 身份 (d_eff = 62/3)
deff_id = (k_max**2 - 2)/3.0
a0_id = (deff_id/(12*pi*np.sqrt(2)))**(1.0/3.0)

# --- m_s/T_c 实际
msTc_actual = (4.0/9.0)/a0_id   # (C_F/2)²/a₀, C_F=4/3

# --- 修正项实际
corr_actual = 5.0*dlmin - msTc_actual
print(f"=== m_s/T_c 修正项精确化 ===")
print(f"a₀ 身份 = {a0_id:.12f}")
print(f"m_s/T_c 实际 = 4/(9a₀) = {msTc_actual:.12f}")
print(f"5Δλ_min = {5.0*dlmin:.12f}")
print(f"修正项实际 = 5Δλ_min − m_s/T_c = {corr_actual:.12f}")

# --- 候选1: σ²/9
c1 = sigma**2/N_gen**2
# --- 候选2: σ²/9 × (1 − 1/320)
c2 = sigma**2/N_gen**2 * (1 - 1.0/320.0)
# --- 候选3: 319/648000
c3 = 319.0/648000.0
print(f"\n候选1 σ²/9 = {c1:.12f}  dev {(corr_actual/c1-1)*100:+.6f}%")
print(f"候选2 σ²/9×(1−1/320) = {c2:.12f}  dev {(corr_actual/c2-1)*100:+.6f}%")
print(f"候选3 319/648000 = {c3:.12f}  dev {(corr_actual/c3-1)*100:+.6f}%")

# --- m_s/T_c 全式
msTc_c2 = 5.0*dlmin - c2
print(f"\nm_s/T_c 新候选 = 5Δλ_min − σ²/9×(1−1/320) = {msTc_c2:.12f}")
print(f"  vs 实际 {msTc_actual:.12f}: dev {(msTc_c2/msTc_actual-1)*100:+.7f}%")

# --- 320/319/648000 框架分解
print(f"\n320 = k_max²·(k_max−3) = {int(k_max**2*(k_max-3))}")
print(f"319 = k_max²(k_max−3)−1 = {int(k_max**2*(k_max-3)-1)}")
print(f"648000 = k_max²·N_gen⁴·(k_max−3)³ = {int(k_max**2*N_gen**4*(k_max-3)**3)}")

# --- δd_(s) 用新 m_s/T_c
ds_new = 2.0*np.exp(-msTc_c2)
ds_actual = 2.0*np.exp(-msTc_actual)
print(f"\nδd_(s) 新候选 = 2e^{{−(5Δλ_min−319/648000)}} = {ds_new:.12f}")
print(f"δd_(s) 实际 = {ds_actual:.12f}")
print(f"  dev = {(ds_new/ds_actual-1)*100:+.7f}%")

# --- 第4处 5 = k_max−3 确认
print(f"\n5 = k_max−3 第4处: 1/320 = 1/[k_max²(k_max−3)]")
print(f"  前3处: m_s/T_c 主项、δd_(s) 旧候选、14/3 = 5(1−σ)")

# --- 1/320 的其他可能解释
print(f"\n1/320 分解:")
print(f"  320 = 2^6×5 = k_max²×5 ✓")
print(f"  320 = 2^6×5 = 64×5")
print(f"  320 = 2^6×5 = (2^k_max×静默?)")
print(f"  1/320 = 0.003125 = 精确二进制分数")
