# -*- coding: utf-8 -*-
# Phase 104az-83: F_np "织 a 口径"完全闭式化验证 (a₀ 有 √3 型闭式后)
# F_np(a) = a₀·(1−δ)/Δλ₃, a₀ = 4/[9(5Δλ_min − 319/648000)] — 不含 π 的全框架闭式
import numpy as np

N_gen = 3.0; k_max = 8.0
sigma = 1.0/15.0
dlmin = (np.sqrt(3)-1)/6.0
dl3 = np.sqrt(2)*dlmin
delta = sigma**2*N_gen/3.0  # σ²·C_F/4 = σ²/3 = 1/675? C_F = 4/3 → δ = σ²/3
# 修正: δ = σ²·C_F/4 = σ²·(4/3)/4 = σ²/3
delta = sigma**2/3.0

print("=== F_np 两口径对比 ===")
# 口径1: 织³ = (b₀/10)³
base3 = (N_gen**2/(N_gen+k_max-1))**3
F1 = base3*(1-sigma**2/N_gen)/dl3
print(f"口径1 织³: (b₀/10)³·(1−σ²/N_c)/Δλ₃ = {F1:.8f}  (vs 4.220: {(F1/4.220-1)*100:+.4f}%)")

# 口径2: 织 a (a₀ 身份 + √3 型闭式)
a0_id = ((62.0/3.0)/(12*np.pi*np.sqrt(2)))**(1.0/3.0)   # π 型 (104az-75)
a0_sqrt3 = 4.0/(9*(5*dlmin - 319.0/648000.0))            # √3 型 (104az-80)
F2a = a0_id*(1-sigma**2/N_gen)/dl3
F2b = a0_sqrt3*(1-sigma**2/N_gen)/dl3
print(f"口径2a 织a(π型): a₀·(1−δ)/Δλ₃ = {F2a:.8f}  (vs 4.220: {(F2a/4.220-1)*100:+.4f}%)")
print(f"口径2b 织a(√3型): a₀'·(1−δ)/Δλ₃ = {F2b:.8f}  (vs 4.220: {(F2b/4.220-1)*100:+.4f}%)")
print(f"  a₀ π型 = {a0_id:.10f}, a₀ √3型 = {a0_sqrt3:.10f}")
print(f"  两口径 a₀ 差 = {(a0_sqrt3/a0_id-1)*100:.3e}%")

print("\n=== F_np 织a口径的 √3 型全框架闭式 ===")
# F_np = 4(674/675)/[9√2·Δλ_min(5Δλ_min − 319/648000)]
num = 4*(674.0/675.0)
den = 9*np.sqrt(2)*dlmin*(5*dlmin - 319.0/648000.0)
F3 = num/den
print(f"闭式: 4·(674/675)/[9√2·Δλ_min(5Δλ_min−319/648000)] = {F3:.8f}")
print(f"  分解: 674/675 = 1−σ²/N_gen = 修")
print(f"        9 = N_gen², √2 = 双谱隙桥, Δλ_min = 基谱隙")
print(f"        (5Δλ_min−319/648000) = m_s/T_c 身份 (104az-80)")

print("\n=== F_np × m_s/T_c 检查 ===")
msTc = 5*dlmin - 319.0/648000.0
prod = F3*msTc
print(f"F_np × m_s/T_c = {F3:.8f} × {msTc:.10f} = {prod:.8f}")
print(f"  18/7 = {18/7:.8f}, 差 = {(prod/(18/7)-1)*100:+.4f}%")
print(f"  2.5715 ≈ ?")

print("\n=== F_np / m_s/T_c ===")
ratio = F3/msTc
print(f"F_np/m_s/T_c = {ratio:.6f}")
print(f"  k_max−1 = 7? 差 {(ratio/7-1)*100:+.2f}%")
print(f"  6.921 ≈ 7−σ = 6.933? 差 {(ratio/(7-sigma)-1)*100:+.2f}%")
print(f"  7−σ−σ² = 6.929? 差 {(ratio/(7-sigma-sigma**2)-1)*100:+.2f}%")

print("\n=== 织³ vs a₀ 关系再检 ===")
print(f"(b₀/10)³ = {base3:.10f}, a₀ = {a0_sqrt3:.10f}")
print(f"  差 = {(a0_sqrt3/base3-1)*100:+.4f}%  (104az-70: +0.0186%)")
print(f"  a₀/(b₀/10)³ = {a0_sqrt3/base3:.10f}")
print(f"  1+σ²/27 = {1+sigma**2/27:.10f}? 差 {(a0_sqrt3/base3/(1+sigma**2/27)-1)*100:+.4f}%")
print(f"  (1+σ/3)² = {(1+sigma/3)**2:.10f}? 差 {(a0_sqrt3/base3/((1+sigma/3)**2)-1)*100:+.4f}%")
