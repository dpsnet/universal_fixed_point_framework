# -*- coding: utf-8 -*-
"""加法组合全谱扫描（2026-10-26）

问题：谱层修正出现加法系数 {11, 29}（δ_P7 的 11/30、Δλ_4 的 231/232）
——为何 11/29 而非其他加法组合（9/6/7/12/8）？
判别候选："纯加法系数"（无乘法等价） = {11, 29}？
"""
import math

n_gen, silence, powers, involution, fixed = 3, 5, 2, 7, 4
kmax = powers**n_gen
sigma = 1/(n_gen*silence)

consts = {"Ngen": n_gen, "Silence": silence, "Powers": powers,
          "Involution": involution, "FixedPoint": fixed, "Kmax": kmax}

print("=== 框架常数乘法身份谱（含幂）===")
mult_ids = {}
# 两两乘积（含自身幂 1..4）
for a, va in consts.items():
    for b, vb in consts.items():
        for ea in range(1, 3):
            for eb in range(1, 3):
                v = (va**ea)*(vb**eb)
                if 0 < v < 100:
                    mult_ids.setdefault(v, []).append(f"{a}^{ea}×{b}^{eb}")

print("乘法身份值（<100）：", sorted(mult_ids.keys()))

print("\n=== 两两加法组合（含幂 1..2）===")
add_combos = {}
for a, va in consts.items():
    for b, vb in consts.items():
        if a == b:
            continue
        for ea in range(1, 3):
            for eb in range(1, 3):
                v = va**ea + vb**eb
                add_combos.setdefault(v, []).append(f"{a}^{ea}+{b}^{eb}")

for v in sorted(add_combos):
    has_mult = v in mult_ids
    tag = "（有乘法等价）" if has_mult else "*** 纯加法（无乘法等价）***"
    print(f"  {v} = {'、'.join(add_combos[v])} {tag}")

print("\n=== 修正中出现集的判别 ===")
appeared = {8: "韦达和/232因子", 11: "δ_P7系数/231分子", 29: "232分母"}
print("出现集：", appeared)
for v in sorted(set(appeared) | set(add_combos)):
    if v in add_combos:
        has_mult = v in mult_ids
        appear_tag = appeared.get(v, "未出现")
        print(f"  {v}: 加法组合 {'、'.join(add_combos[v])} | 乘法等价 {'有' if has_mult else '无'} | 修正出现: {appear_tag}")
