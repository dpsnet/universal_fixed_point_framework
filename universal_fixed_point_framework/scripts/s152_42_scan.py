# -*- coding: utf-8 -*-
"""S152 ConfinementDomain=42 框架语义扫描（先证伪）
42 = 约束域（框架常数——S147-S151 多次登记未定）
扫描：所有框架量的整洁组合（乘积/加减/幂）——判别哪个语义候选
"""
import numpy as np
from itertools import combinations

N_gen, K_max, Powers, Silence, Involution, FixedPoint = 3, 8, 2, 5, 7, 4
SigmaInv = 15
full = 16  # 全态 2^4

print("=== S152: 42 的框架量分解扫描 ===\n")
print(f"框架量: N_gen={N_gen}, K_max={K_max}, Powers={Powers}, "
      f"Silence={Silence}, Involution={Involution}, FixedPoint={FixedPoint}, "
      f"σ⁻¹={SigmaInv}, 全态={full}")

# 1. 三原始量乘积（组合）
print("\n=== 1. 三量乘积（全组合） ===")
vals = {"N_gen":3, "K_max":8, "Powers":2, "Silence":5, "Involution":7, "FixedPoint":4, "σ⁻¹":15, "全态":16}
found = []
for r in [2, 3]:
    for combo in combinations(vals.items(), r):
        names = [n for n, _ in combo]
        prod = 1
        for _, v in combo:
            prod *= v
        if prod == 42:
            found.append((names, prod))
for names, prod in found:
    print(f"  {'×'.join(names)} = {prod} ✓")

# 2. 加减组合（两量 ± 三量）
print("\n=== 2. 加减组合 ===")
for (n1, v1), (n2, v2) in combinations(vals.items(), 2):
    if v1 * v2 + v1 == 42 or v1 * v2 + v2 == 42:
        print(f"  {n1}×{n2}+{n1 or n2} 命中")
    if v1 * v2 - v1 == 42 or v1 * v2 - v2 == 42:
        print(f"  {n1}×{n2}−{n1 or n2} 命中")
    if v1 + v2 == 42 or v1 - v2 == 42 or v2 - v1 == 42:
        print(f"  {n1}±{n2} = 42")

print("\n=== 3. 候选分解判别 ===")
cands = {
    "2×3×7（幂基×活跃×对合）": 2*3*7,
    "3×14（活跃×(全态−幂基)）": 3*14,
    "3×(15−1)（活跃×(σ⁻¹−1)）": 3*(15-1),
    "8×5+2（k_max×静默+幂基）": 8*5+2,
    "16×3−6（全态×活跃−6）": 16*3-6,
    "7×6（对合×活跃×幂基）": 7*6,
    "15×3−3（σ⁻¹×活跃−活跃）": 15*3-3,
    "2×21（幂基×21）": 2*21,
    "4×10+2（不动点×10+2）": 4*10+2,
    "5×8+2（静默×k_max+幂基）": 5*8+2,
}
for k, v in cands.items():
    print(f"  {k:28s} = {v} {'✓' if v == 42 else '✗'}")

print("\n=== 4. 语义候选排序 ===")
print("A. 2×3×7 = 幂基×活跃代×对合——三个原始框架量乘积（无加减修正）")
print("B. 3×(16−2) = 活跃代×(全态−幂基)——'约束域 = 活跃代×(非平凡态)'")
print("C. 8×5+2 = k_max×静默+幂基——'谱最大×冻结区+幂基'（带+2修正）")
print("D. 6×7 = (活跃×幂基)×对合——同 A 重组")
print("\n→ 最整洁：A（三个原始量纯乘积）与 B（活跃×(全态−幂基)）")
print("→ 语义候选：约束域 = 活跃代×对合×幂基（三公设派生量乘积）")
print("  or 活跃代×(全态−幂基)（'活跃代支配非平凡态'——14 = 非幂基态）")
print("→ 均登记候选——禁拟合——待判别")

print("\n=== 5. 42 的物理联想（登记——不强行） ===")
print("SU(3) 禁闭域？QCD 禁闭尺度？42 = 7×6（对合×完全数 6）？")
print("——登记为观察级——不采用（禁拟合）")
