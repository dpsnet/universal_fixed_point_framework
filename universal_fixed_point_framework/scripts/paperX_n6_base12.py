# -*- coding: utf-8 -*-
"""n=6 符号约束验证 + 12 基座判定结构：
1. 12 基座是否决定被删 8 因子（流形上确定性）
2. 12 基座下可达模式数、A_BG 取值形态
3. 12 基座模式 → A_BG 的闭式归纳起点：输出全模式判定表（若模式数可控）
"""
import json, os, random, sys
from collections import defaultdict, Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_pair, sg_block
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_n6_fullbasis import sg_pattern6_full

NAMES = ["s1_23","s12_3","s123_4","s56","s23","s1_234","s12_34","s34",
         "s2_34","s23_4","s12","s345_6","s45_6","s45","s3_45","s34_5",
         "s234_5","s61","s2_345","s23_45"]
BASE12 = [0,1,2,3,4,5,7,10,11,12,13,17]  # s1_23,s12_3,s123_4,s56,s23,s1_234,s34,s12,s345_6,s45_6,s45,s61
REMOVED = [i for i in range(20) if i not in BASE12]

def cache_samples(n=50000, seed=41):
    rng = random.Random(seed)
    data = []
    for _ in range(n):
        omega, zbar, pairs = gen_partial_collinear(6, 0, r1=True, momentum=True, rng=rng)
        data.append((sg_pattern6_full(omega, zbar), round(A_BG(6, omega, zbar), 6)))
    return data

if __name__ == "__main__":
    data = cache_samples(50000)
    print(f"缓存样本: {len(data)}")

    # 1) 12 基座决定被删因子？
    base_to_rem = defaultdict(set)  # base tuple -> set of removed-factor tuples
    base_to_abg = defaultdict(set)
    for full, a in data:
        base = tuple(full[i] for i in BASE12)
        rem = tuple(full[i] for i in REMOVED)
        base_to_rem[base].add(rem)
        base_to_abg[base].add(a)
    undet_rem = {b: r for b, r in base_to_rem.items() if len(r) > 1}
    print(f"12 基座决定性: 被删 8 因子 {sum(1 for r in base_to_rem.values() if len(r)==1)}/{len(base_to_rem)} 个基座模式内决定性; 非决定性 {len(undet_rem)}")
    # A_BG 决定性
    undet_abg = {b: v for b, v in base_to_abg.items() if len(v) > 1}
    print(f"12 基座 → A_BG: 决定性 {len(base_to_abg)-len(undet_abg)}/{len(base_to_abg)}, 非决定性 {len(undet_abg)}")
    print(f"12 基座可达模式数: {len(base_to_abg)}")
    # 取值形态
    vc = Counter()
    for v in base_to_abg.values():
        vc[tuple(sorted(v))] += 1
    print(f"取值形态: {dict(vc)}")

    # 被删因子非决定性的具体模式样例（若存在）
    if undet_rem:
        for b, r in list(undet_rem.items())[:3]:
            print(f"  例: base={b[:6]}... rem 值集={sorted(r)}")

    # 2) 判定表导出：12 基座模式 → A_BG（若模式数可控 ≤ 4096）
    table = {}
    for base, vals in base_to_abg.items():
        if len(vals) == 1:
            table[str(list(base))] = list(vals)[0]
    with open(os.path.join(SCRIPT_DIR, "paperX_n6_base12_table.json"), "w", encoding="utf-8") as f:
        json.dump(table, f, ensure_ascii=False)
    print(f"判定表导出: {len(table)} 条目 -> paperX_n6_base12_table.json")

    res = {
        "samples": len(data),
        "base12_patterns": len(base_to_abg),
        "removed_determined": sum(1 for r in base_to_rem.values() if len(r) == 1),
        "removed_nondetermined": len(undet_rem),
        "ABG_determined": len(base_to_abg) - len(undet_abg),
        "ABG_nondetermined": len(undet_abg),
        "value_shapes": {str(k): v for k, v in vc.items()},
    }
    with open(os.path.join(SCRIPT_DIR, "paperX_n6_base12_summary.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("DONE")
