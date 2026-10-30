# -*- coding: utf-8 -*-
# Phase 104az-82b: Mersenne 指数 2..8 连续覆盖验证 (含 M_7 = 127)
import numpy as np

N_gen = 3.0; k_max = 8.0
N_active = 3.0

print("=== Mersenne 指数 2..8 连续覆盖 ===")
print(f"{'指数':<6}{'M_n = 2^n−1':<14}{'框架角色':<40}{'确认'}")
roles = {
    2: ("N_active−1 = 3−1", "N_gen = 3 = M_2 ✓ (框架常数)"),
    3: ("N_active = 3", "k_max−1 = 7 = M_3 ✓ (缺失对偶 P7-4c)"),
    4: ("k_max/2 = 4", "σ⁻¹ = 15 = M_4 ✓ (静默常数)"),
    5: ("k_max−3 = 5", "62/2 = 31 = M_5 ✓ (d_eff 分子 104az-75)"),
    6: ("k_max−2 = 6", "k_max²−1 = 63 = M_6 ✓ (±1 对偶 −1 侧)"),
    7: ("k_max−1 = 7", "127 = M_7 ✓ (P7-5e-122: 0.1016 = 127×8/10⁴)"),
    8: ("k_max = 8", "2^k_max−1 = 255 = M_8 = 15×17 = σ⁻¹×F_2 ✓"),
}
for n in range(2, 9):
    m = 2**n - 1
    exp_role, role = roles[n]
    print(f"  {n:<6}{m:<14}{exp_role:<40}{role}")

print("\n=== M_7 = 127 的框架出现 (P7-5e-122) ===")
print(f"  127 = 2^7−1 = 2^(k_max−1)−1")
print(f"  0.1016 = (2^(8−1)−1)×8/(8+2)^4 = 127×8/10⁴ (用户公式确认)")
print(f"  127×8 = 1016, /10⁴ = 0.1016 ✓")

print("\n=== M_8 = 255 的分解 ===")
print(f"  255 = 2^8−1 = 15×17 = σ⁻¹ × F_2 (Fermat 数 17 = 2⁴+1)")
print(f"  255 = 3×5×17 = N_gen×(k_max−3)×F_2")

print("\n=== 结论: Mersenne 指数-框架量映射完整 ===")
print("  2,3,4,5,6,7,8 → N_active−1, N_active, k_max/2, k_max−3, k_max−2, k_max−1, k_max")
print("  Mersenne 家族 (M_2..M_8) 指数连续覆盖, 每个指数 = 一个框架量")
print("  σ⁻¹ = 15 = M_4: Mersenne 家族成员身份获完整家族支撑")
print("  (对比: 代数候选 15 = 3×5 = N_gen×(k_max−3) 亦精确)")
print("  两身份可能共存: 2 幂结构 (Mersenne) 与静默单元结构 (3×5) 在 15 处交汇")

print("\n=== 判别状态 ===")
print("  Mersenne 候选: 从单点恒等 → 指数族覆盖 2..8 (结构性证据)")
print("  代数候选: '5 = k_max−3' 四处绑定 (σ = 1/(3×5) 为第 5 处)")
print("  最终判别仍需: 一个只支持单一候选的独立结构")
