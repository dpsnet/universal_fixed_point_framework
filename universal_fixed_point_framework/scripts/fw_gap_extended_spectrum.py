# -*- coding: utf-8 -*-
"""FW 缺口谱扩展：{24, 25, 70, 140} + 新恒等 24+25 = 49（2026-10-26）

① ×幂基升级法则修正：素数升级允许（5→10、7→14、29→58、49→98）、
   双非活跃复合禁（35→70 ✗）、静默²（25）不在 FW
② 新缺口 25 = 静默²（对照 49 = 对合域² ∈ FW——静默幂次禁 vs 对合域幂次允许）
③ 新框架恒等：N_gen×k_max + 静默² = 对合域²（24+25 = 49）
"""
import math

powers, ngen, silence, involution = 2, 3, 5, 7
kmax = powers**ngen  # 8

print("=== 新恒等：N_gen×k_max + 静默² = 对合域² ===")
lhs = ngen * kmax + silence**2
rhs = involution**2
print(f"{ngen}×{kmax} + {silence}² = {lhs}；{involution}² = {rhs}——恒等: {lhs == rhs}")
print()

print("=== FW 缺口谱扩展（104az-195 原 {24,70,140} + 25）===")
print(f"24 = N_gen×k_max = {ngen}×{kmax}——FW 缺（层级正交禁候选）")
print(f"25 = 静默² = {silence}²——FW 缺（新发现——静默幂次禁候选）")
print(f"70 = 幂基×静默×对合域 = {powers}×{silence}×{involution}——FW 缺（双非活跃复合禁）")
print(f"140 = 70×幂基——FW 缺（继承）")
print(f"49 = 对合域² = {involution}² ∈ FW ✓——对照：对合域² 允许、静默² 禁")
print()

print("=== ×幂基升级法则（修正版）===")
# FW 表偶数 → 半值 ∈ FW 的全表核对（升级成功集）
fw = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,20,21,28,29,30,31,32,35,40,42,44,45,46,48,49,56,58,60,61,63,64,65,84,98,100,105,125,210,253,320,675,729,1000}
ok_pairs = []
for e in sorted(fw):
    if e % 2 == 0 and (e // 2) in fw:
        ok_pairs.append((e // 2, e))
print(f"FW 表升级成功对（半值→值）：{len(ok_pairs)} 对")
for s, d in ok_pairs:
    # 因子构成
    facs = []
    for f in (powers, ngen, silence, involution):
        if s % f == 0:
            facs.append(f)
    # 含活跃/幂基判断 + 素数判断
    is_prime_s = all(s % d2 != 0 for d2 in range(2, int(s**0.5)+1)) if s > 1 else False
    rule = "素" if is_prime_s else ("活跃/幂基" if (ngen in facs or powers in facs) else "双非活跃复合")
    print(f"  {s} → {d}：因子 {facs} 规则分类={rule}")
print()

print("=== 法则判别 ===")
print("原法则（活跃/幂基在场）：框架常数两两组合 6/6 一致——但 FW 全表反例")
print("（5→10、7→14、29→58、49→98——素数升级允许）——修正：")
print("**×2 升级禁则只作用于'双非活跃素因子复合'（35 = 静默×对合域）+ 静默幂次（25）**")
print("——70 缺位 = 双非活跃复合禁；25 缺位 = 静默幂次禁；")
print("24 缺位 = N_gen×k_max（和量 k_max 乘积）禁——缺口谱机制候选（观察级）")
