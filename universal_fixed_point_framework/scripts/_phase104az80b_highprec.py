# -*- coding: utf-8 -*-
# Phase 104az-80b: m_s/T_c 候选高精度恒等检验 (mpmath 50位)
import mpmath as mp

mp.mp.dps = 50

N_gen = mp.mpf(3); k_max = mp.mpf(8)
sigma = mp.mpf(1)/mp.mpf(15)
dlmin = (mp.sqrt(3)-1)/6
pi = mp.pi

# --- a₀ 身份: [(62/3)/(12π√2)]^(1/3)
deff_id = (k_max**2 - 2)/3
a0_id = (deff_id/(12*pi*mp.sqrt(2)))**(mp.mpf(1)/3)
print(f"a₀ 身份 (50位) = {mp.nstr(a0_id, 50)}")

# --- m_s/T_c 实际 = 4/(9a₀)
msTc_actual = mp.mpf(4)/(9*a0_id)
print(f"m_s/T_c 实际 = 4/(9a₀) = {mp.nstr(msTc_actual, 50)}")

# --- 候选 = 5Δλ_min − 319/648000
cand = 5*dlmin - mp.mpf(319)/mp.mpf(648000)
print(f"m_s/T_c 候选 = 5Δλ_min − 319/648000 = {mp.nstr(cand, 50)}")

# --- 精确差
diff = msTc_actual - cand
print(f"\n精确差 = 实际 − 候选 = {mp.nstr(diff, 30)}")
print(f"相对差 = {mp.nstr(diff/msTc_actual * 100, 20)}%")

# --- 反推: 若候选为真, a₀' = 4/(9·候选)
a0_prime = mp.mpf(4)/(9*cand)
print(f"\n反推 a₀' = 4/(9·候选) = {mp.nstr(a0_prime, 50)}")
print(f"a₀ 身份 vs a₀': 差 = {mp.nstr(a0_prime - a0_id, 30)}")

# --- 是否精确恒等? 比较 (5Δλ_min − 319/648000) 与 4/(9a₀)
# 若 a₀ 闭式 = 4/(45Δλ_min − 2871/648000) 精确, 则 a₀ = 4/(9·候选)
# 验证: 45Δλ_min − 2871/648000 = 9·候选?
cand9 = 9*cand
expr_alt = 45*dlmin - mp.mpf(2871)/mp.mpf(648000)
print(f"\n9·候选 = {mp.nstr(cand9, 30)}")
print(f"45Δλ_min − 2871/648000 = {mp.nstr(expr_alt, 30)}")
print(f"差 = {mp.nstr(cand9 - expr_alt, 30)}")

# --- δd_(s) 高精度
ds_actual = 2*mp.e**(-msTc_actual)
ds_cand = 2*mp.e**(-cand)
print(f"\nδd_(s) 实际 = {mp.nstr(ds_actual, 40)}")
print(f"δd_(s) 候选 = {mp.nstr(ds_cand, 40)}")
print(f"相对差 = {mp.nstr((ds_cand/ds_actual - 1)*100, 20)}%")

# --- 319/648000 框架分解确认
print(f"\n319 = k_max²(k_max−3)−1 = {int(k_max**2*(k_max-3))-1}")
print(f"648000 = k_max²·N_gen⁴·(k_max−3)³ = {int(k_max**2*N_gen**4*(k_max-3)**3)}")
print(f"2871 = 9×319 = {9*319}")
