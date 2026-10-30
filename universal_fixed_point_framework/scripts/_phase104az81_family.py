# -*- coding: utf-8 -*-
# Phase 104az-81: 319/648000 修正的家族结构检验
# 发现候选: 319 = k_max²(k_max−3)−1 与 39 = k_max(k_max−3)−1 同属 k_max^j(k_max−3)−1 家族
import numpy as np

N_gen = 3.0; k_max = 8.0
sigma = 1.0/15.0

print("=== k_max^j·(k_max−3) − 1 家族 ===")
for j in range(0, 6):
    v = int(k_max**j*(k_max-3) - 1)
    print(f"  j={j}: k_max^{j}·(k_max−3)−1 = {v}")

print("\n=== 家族已知成员对照 ===")
print(f"  39 = j=1 (P7-5e-244 静默单元家族登记, E=39/2000)")
print(f"  319 = j=2 (本轮 修正项分子 319/648000)")
print(f"  4 = j=0 (k_max−3)−1 = 5−1)")

print("\n=== 家族比值关系 ===")
for j in range(1, 5):
    vj = int(k_max**j*(k_max-3) - 1)
    vprev = int(k_max**(j-1)*(k_max-3) - 1)
    ratio = vj/vprev if vprev else float('inf')
    print(f"  成员{j-1}→{j}: {vprev} → {vj} (×{ratio:.4f})")

print("\n=== 319/648000 修正项的家族重写 ===")
# 修正项 = [k_max²(k_max−3)−1]/[k_max²·N_gen⁴·(k_max−3)³]
num = int(k_max**2*(k_max-3) - 1)
den = int(k_max**2*N_gen**4*(k_max-3)**3)
print(f"  319/648000 = {num}/{den}")
print(f"  = [k_max²(k_max−3)−1]/[k_max²·N_gen⁴·(k_max−3)³]")
print(f"  = 319/(64·81·125)")

print("\n=== 1/320 的框架表达 ===")
# 1/320 = σ²·N_gen²(k_max−3)/k_max²
expr = sigma**2 * N_gen**2*(k_max-3)/k_max**2
print(f"  σ²·N_gen²(k_max−3)/k_max² = {expr:.10f} (应 = 1/320 = {1/320:.10f})")
# 1/320 = N_gen·σ/k_max²
expr2 = N_gen*sigma/k_max**2
print(f"  N_gen·σ/k_max² = {expr2:.10f}")
# 1/320 = 1/[(k_max−3)·k_max²]  (因 N_gen·σ = 1/(k_max−3))
expr3 = 1.0/((k_max-3)*k_max**2)
print(f"  1/[(k_max−3)·k_max²] = {expr3:.10f}")
# 关键恒等: N_gen·σ = 1/(k_max−3)?
print(f"\n  N_gen·σ = {N_gen*sigma:.6f}, 1/(k_max−3) = {1/(k_max-3):.6f}")

print("\n=== 修正项减法形式 ===")
# 修正项 = σ²/9 − σ²/2880, 2880 = N_gen²·k_max²·(k_max−3)
c1 = sigma**2/N_gen**2
c2 = sigma**2/(N_gen**2 * k_max**2 * (k_max-3))
print(f"  σ²/N_gen² = {c1:.12f}")
print(f"  σ²/(N_gen²·k_max²·(k_max−3)) = {c2:.12f}")
print(f"  差 = {c1-c2:.12f} (应 = 319/648000 = {319/648000:.12f})")

print("\n=== 39 vs 319 的框架联系 ===")
print(f"  319 = 8×39 + 7 = k_max×39 + (k_max−1)")
print(f"  39 = 8×4 + 7 = k_max×(k_max−3−1) + (k_max−1)?")
print(f"  39 = 8×5−1, 319 = 8×40−1 = 8×(8×5)−1")
print(f"  39→319: ×8+7 = ×k_max+(k_max−1)")

print("\n=== 648000 框架分解 ===")
print(f"  648000 = 2^6·3^4·5^3 = 64×81×125")
print(f"  64 = k_max² = 2^6")
print(f"  81 = N_gen⁴ = 3^4")
print(f"  125 = (k_max−3)³ = 5^3")
print(f"  指数: 6,4,3 = k_max−2, N_gen+1, k_max−5?")
