# -*- coding: utf-8 -*-
# Phase 104az-82: "−1 减法族"大统一验证 (Mersenne 家族在框架的多点出现)
import numpy as np

N_gen = 3.0; k_max = 8.0
N_active = 3.0  # log2(k_max)

print("=== '−1 减法族' 成员与 Mersenne 身份 ===")
members = [
    ("7 = k_max−1 缺失对偶", 7, 2**3-1, 3),
    ("15 = σ⁻¹", 15, 2**4-1, 4),
    ("31 = 62/2 (d_eff 分子因子)", 31, 2**5-1, 5),
    ("63 = k_max²−1", 63, 2**6-1, 6),
    ("255 = 2^k_max−1", 255, 2**8-1, 8),
]
for name, v, mers, exp in members:
    print(f"  {name}: {v} = 2^{exp}−1 = M_{exp}? {v == mers}")

print("\n=== 静默 −1 侧家族 (k_max^j·(k_max−3)−1) ===")
for j in range(1, 4):
    v = int(k_max**j*(k_max-3) - 1)
    print(f"  j={j}: k_max^{j}·(k_max−3)−1 = {v}")

print("\n=== 指数-框架量映射 ===")
mapping = {
    2: "N_active−1 = 3−1", 3: "N_active = 3", 4: "k_max/2 = 4",
    5: "k_max−3 = 5", 6: "k_max−2 = 6", 8: "k_max = 8",
}
for exp, meaning in mapping.items():
    v = 2**exp - 1
    print(f"  M_{exp} = {v}: 指数 {exp} = {meaning}")

print("\n=== ±1 对偶家族 (P7-5e-95 +1 侧 / −1 侧) ===")
print(f"  +1 侧: 65 = k_max²+1 (P7-5e-95 静默 +1 家族, 1/65 = m=−1 修正)")
print(f"  −1 侧: 63 = k_max²−1 (M_6, 对偶)")
print(f"  +1 侧: 25 = 8×3+1, 41 = 8×5+1, 49 = 8×6+1, 65 = 8×8+1, 193 = 8×24+1")
print(f"  −1 侧: 39 = 8×5−1, 319 = 64×5−1 (k_max^j·5−1)")

print("\n=== 关键: 7 = M_3 = k_max−1, 3 = N_active ===")
print(f"  7 = 2^3−1, 指数 3 = N_active = log2(k_max)")
print(f"  k_max−1 = 7: 缺失对偶的 Mersenne 身份 (P7-4c 缺失对偶 + Mersenne 汇合)")

print("\n=== σ 身份判别更新 ===")
print("  候选2 (Mersenne): σ⁻¹ = 15 = M_4, 家族多点出现:")
print("    M_2 = 3 = N_gen ✓")
print("    M_3 = 7 = k_max−1 (缺失对偶) ✓")
print("    M_4 = 15 = σ⁻¹ ✓")
print("    M_5 = 31 = 62/2 (d_eff 分子) ✓")
print("    M_6 = 63 = k_max²−1 (±1 对偶 −1 侧) ✓")
print("  候选1 (代数): σ = 1/[N_gen(k_max−3)] = 1/15, '5=k_max−3' 四处绑定")
print("  结论: 两个身份可能共存 — 15 同时是 M_4 与 3×5")
print("        (2 幂结构与静默单元结构在 15 处交汇)")

print("\n=== Mersenne 家族在框架的角色清单 ===")
print("  P7-5e-2: 15=16−1, 7=8−1 Mersenne 型减法族 (已登记)")
print("  104az-75: 62=2×(2^5−1)=2×31 Mersenne 31 投影 (已登记)")
print("  P7-5e-95: 65=k_max²+1 静默 +1 家族 (已登记)")
print("  104az-81/82: 39/319 静默 −1 家族, 63=k_max²−1 对偶 (本轮)")
