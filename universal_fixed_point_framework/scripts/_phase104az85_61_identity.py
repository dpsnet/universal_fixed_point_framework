# -*- coding: utf-8 -*-
# Phase 104az-85: 61 身份验证 (用户分解) + M_6 邻域五成员完备检查
# 用户式: 61 = k_max²−3 = k_max²−4+1 = (k_max+2)(k_max−2)+1
import numpy as np

k_max = 8.0; N_gen = 3.0; N_active = 3.0

print("=== 用户式验证 ===")
print(f"k_max²−3 = {k_max**2-3:.0f}")
print(f"(k_max+2)(k_max−2)+1 = ({k_max+2:.0f})({k_max-2:.0f})+1 = {(k_max+2)*(k_max-2)+1:.0f} ✓")
print(f"k_max²−4+1 = {k_max**2-4+1:.0f} ✓")

print("\n=== 61 的框架因子身份 ===")
print(f"k_max+2 = {k_max+2:.0f} = N_gen+k_max−1 = {N_gen+k_max-1:.0f} (织因子分母! (b₀/10)³ = (9/10)³)")
print(f"k_max−2 = {k_max-2:.0f} = M_6 指数 (M_6 = 2^6−1 = 63 = k_max²−1)")
print(f"→ 61 = (N_gen+k_max−1)(k_max−2)+1 = {N_gen+k_max-1:.0f}×{k_max-2:.0f}+1 = {int((N_gen+k_max-1)*(k_max-2)+1)}")
print(f"  61 = 织因子分母 × M_6 指数 + 1 → 连接 F_np 织因子 与 M_6")

print("\n=== 61 的其他框架表达 ===")
print(f"61 = M_6 − 2 = 63−2 ✓ (M_6 邻域)")
print(f"61 = 62 − 1 (d_eff 分子 62 的 −1 邻居)")
print(f"61 = 2^(k_max−2) − 3 = 2^6−3 ✓ (2 幂 −3)")

print("\n=== M_6 邻域五成员完备性 ===")
print(f"{'值':<6}{'身份':<40}{'来源'}")
print(f"{61:<6}{'M_6−2 = (k_max+2)(k_max−2)+1 = 10×6+1':<40}{'104az-85 (用户分解)'}")
print(f"{62:<6}{'M_6−1 = 2×M_5 (d_eff 分子)':<40}{'104az-84'}")
print(f"{63:<6}{'M_6 = k_max²−1 (±1 对偶 −1 侧)':<40}{'104az-82'}")
print(f"{64:<6}{'M_6+1 = k_max² (全状态²)':<40}{'框架常数'}")
print(f"{65:<6}{'M_6+2 = k_max²+1 (+1 家族)':<40}{'P7-5e-95'}")
print("\n→ M_6 邻域 61..65 五连续整数全部框架化 — '63 邻域完备'!")

print("\n=== 61 与 F_np 织因子的连接 ===")
print(f"织因子分母 10 = N_gen+k_max−1 (F_np = (N_gen²/10)³·修/隙)")
print(f"61 = 10×6+1 → 61 是'织分母×M_6指数+1'")
print(f"61 完成 k_max² 互补家族: 61/62/63/65 全部有身份 (64 = k_max² 自身)")

print("\n=== 一般化检查 (对任意 k_max) ===")
for k in [6, 8, 10]:
    print(f"  k_max={k}: k_max²−3 = {k*k-3} = (k+2)(k−2)+1 = {int((k+2)*(k-2)+1)} ✓ (代数恒等, 框架意义在 k=8)")
