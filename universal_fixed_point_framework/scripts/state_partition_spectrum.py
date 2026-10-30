# -*- coding: utf-8 -*-
"""态分割谱的结构——k_max±{对合域, 活跃}（2026-10-26）

态分割谱 {1,5,11,15}（16 的四重特异分割）——
  1+15 = 5+11 = 16（两组互补对）
发现候选：{1,5,11,15} = {8−7, 8−3, 8+3, 8+7} = k_max±{对合域, 活跃}？
"""
n_gen, silence, powers, involution, fixed = 3, 5, 2, 7, 4
kmax = powers**n_gen
active = n_gen

print("=== 态分割谱 {1,5,11,15} 的 k_max± 结构 ===")
vals = [kmax-involution, kmax-active, kmax+active, kmax+involution]
names = ["k_max−对合域", "k_max−活跃", "k_max+活跃", "k_max+对合域"]
print("1 = k_max−对合域 = 8−7:", kmax-involution, "✓")
print("5 = k_max−活跃 = 8−3:", kmax-active, "✓")
print("11 = k_max+活跃 = 8+3:", kmax+active, "✓")
print("15 = k_max+对合域 = 8+7:", kmax+involution, "✓")
print("→ 态分割谱 = k_max±{对合域, 活跃}——围绕空间全态 8 对称 ✓")

print("\n=== 互补对 ===")
print(f"1+15 = {1+15} = 16 = 2×k_max ✓（k_max−对合域 + k_max+对合域）")
print(f"5+11 = {5+11} = 16 = 2×k_max ✓（k_max−活跃 + k_max+活跃）")
print("→ 两组互补对 = 围绕 k_max 的对称 ±对合域、±活跃")

print("\n=== 互补对距离 ===")
print(f"15−11 = {15-11} = 4 = 不动点 ✓")
print(f"5−1 = {5-1} = 4 = 不动点 ✓")
print("→ 两组互补对的距离 = 不动点 4——分割的均匀步长")

print("\n=== 内/外环结构 ===")
print("内环：5、11（k_max±活跃——静默、显态）——静默机制的核心对")
print("外环：1、15（k_max±对合域——单位、余态域）——定态域的对")
print("活跃± → 内环（静默/显态）——对合域± → 外环（定态/余态）")

print("\n=== 与 11 四重身份/态组合的连接 ===")
print("11 = k_max+活跃（态谱成员——显态内环上侧）")
print("15 = k_max+对合域（余态域——σ⁻¹——16−1 定态余）")
print("5 = k_max−活跃（静默——态组合诠释 = 三矢量+伪标量）")
print("1 = k_max−对合域（单位/定态）")
print("→ 态数几何：冻结窗口的特殊态数全部由 k_max±{对合域,活跃} 生成")
