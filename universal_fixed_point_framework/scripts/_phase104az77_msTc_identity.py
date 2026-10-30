# -*- coding: utf-8 -*-
# Phase 104az-77: m_s/T_c 代数身份候选验证
# 候选: m_s/T_c = 5*Δλ_min − σ²/N_gen²  (5Δλ_min − σ²/9)
# 关联: δd_(s) = 2·e^{−m_s/T_c}; a₀ 闭式反推
import numpy as np

N_c = 3.0
N_f = 3.0
N_gen = 3.0
k_max = 8.0
sigma = 1.0/15.0
C_F = (N_c**2 - 1)/(2*N_c)          # 4/3
dlmin = (np.sqrt(3) - 1)/6.0        # Δλ_min
dl3 = np.sqrt(2)*dlmin              # Δλ₃
pi = np.pi

# --- a₀ 身份 (104az-75 锁定): d_eff = (k_max²−2)/3 = 62/3
deff_id = (k_max**2 - 2)/3.0
a0_id = (deff_id/(12*pi*np.sqrt(2)))**(1.0/3.0)
print(f"a₀ 身份 = [(62/3)/(12π√2)]^(1/3) = {a0_id:.12f}")
print(f"paper17 a₀ = 0.729135 -> dev {(a0_id/0.729135 - 1)*100:+.6f}%")

# --- m_s/T_c 实际 (104az-72: (C_F/2)²/a₀)
msTc_actual = (C_F/2.0)**2 / a0_id
print(f"\nm_s/T_c 实际 = (C_F/2)²/a₀ = 4/(9a₀) = {msTc_actual:.12f}")

# --- 候选: 5Δλ_min − σ²/9
cand = 5.0*dlmin - sigma**2/N_gen**2
print(f"候选 m_s/T_c = 5Δλ_min − σ²/9 = {cand:.12f}")
print(f"  5Δλ_min = {5.0*dlmin:.12f},  σ²/9 = {sigma**2/N_gen**2:.12f}")
dev = (msTc_actual/cand - 1)*100
print(f"  实际/候选 相对差 = {dev:+.7f}%")

# --- 反推: 若候选精确, a₀' = 4/(45Δλ_min − σ²)
a0_prime = 4.0/(45.0*dlmin - sigma**2)
print(f"\n反推 a₀' = 4/(45Δλ_min − σ²) = {a0_prime:.12f}")
print(f"  a₀'/a₀ 相对差 = {(a0_prime/a0_id - 1)*100:+.7f}%")

# --- δd_(s) 两个口径
ds_actual = 2.0*np.exp(-msTc_actual)
ds_cand = 2.0*np.exp(-cand)
ds_cand2 = 1.0 + 5.0*dlmin/7.0   # 104az-76 候选
print(f"\nδd_(s) 实际 (2e^{{-m_s/T_c}}) = {ds_actual:.12f}")
print(f"  δd_(s) 用候选 m_s/T_c     = {ds_cand:.12f}  dev {(ds_actual/ds_cand - 1)*100:+.6f}%")
print(f"  δd_(s) 候选 1+5Δλ_min/7   = {ds_cand2:.12f}  dev {(ds_actual/ds_cand2 - 1)*100:+.6f}%")

# --- m_s/T_c 的 Δλ_min 倍数检验
ratio = msTc_actual/dlmin
print(f"\nm_s/T_c/Δλ_min = {ratio:.10f}  (≈5? 差 {(ratio-5)*100:+.6f}%)")
print(f"  5Δλ_min − m_s/T_c = {5.0*dlmin - msTc_actual:.10f}  (σ²/9 = {sigma**2/N_gen**2:.10f})")
print(f"  (5Δλ_min − m_s/T_c)/(σ²/9) = {(5.0*dlmin - msTc_actual)/(sigma**2/N_gen**2):.10f}  (≈1?)")

# --- 5Δλ_min 框架呼应收敛: 5 = k_max−3
print(f"\n5 = k_max−3 = {k_max-3:.0f}  (框架数)")
print(f"σ²/9 = 1/{int(225*9):d} = 1/{int(N_gen**2*225):d}  (静默²/代²)")
