# -*- coding: utf-8 -*-
"""n=6 判据阶数扫描：k=4 因子联合判据存在性。
若不存在 → 负结果完整（n=6 非零判据无 ≤4 因子解析闭式）。
"""
import json, os, random, sys, itertools
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_n6_fullbasis import sg_pattern6_full
from paperX_n6_base12 import BASE12

NAMES = ["s1_23","s12_3","s123_4","s56","s23","s1_234","s34","s12",
         "s345_6","s45_6","s45","s61"]

def cache(n=80000, seed=81):
    rng = random.Random(seed)
    data = []
    for _ in range(n):
        omega, zbar, pairs = gen_partial_collinear(6, 0, r1=True, momentum=True, rng=rng)
        full = sg_pattern6_full(omega, zbar)
        base = tuple(full[i] for i in BASE12)
        data.append((base, round(A_BG(6, omega, zbar), 6)))
    return data

if __name__ == "__main__":
    data = cache(80000)
    pat_a = {}
    for b, a in data:
        pat_a[b] = a
    nz = {b: a for b, a in pat_a.items() if abs(a) > 1e-9}
    print(f"模式: {len(pat_a)}  非零: {len(nz)}")

    # k=4 全组合（495 组）
    found = []
    min_mixed = None
    min_combo = None
    for comb in itertools.combinations(range(12), 4):
        groups = defaultdict(set)
        for b, a in pat_a.items():
            key = tuple(b[i] for i in comb)
            groups[key].add(1 if abs(a) > 1e-9 else 0)
        m = sum(1 for g in groups.values() if len(g) > 1)
        if m == 0:
            found.append(comb)
        elif min_mixed is None or m < min_mixed:
            min_mixed = m
            min_combo = comb
    print(f"4 因子判据: {len(found)} 个组合")
    if found:
        for c in found[:10]:
            print(f"  {[NAMES[i] for i in c]}")
    else:
        print(f"最接近: 混合组 {min_mixed}, 组合 {[NAMES[i] for i in min_combo]}")
        # 若无 4 因子：5 因子抽查（前 200 组合）
        found5 = []
        for idx, comb in enumerate(itertools.combinations(range(12), 5)):
            if idx >= 200:
                break
            groups = defaultdict(set)
            for b, a in pat_a.items():
                key = tuple(b[i] for i in comb)
                groups[key].add(1 if abs(a) > 1e-9 else 0)
            if all(len(g) == 1 for g in groups.values()):
                found5.append(comb)
        print(f"5 因子判据（抽查前 200 组合）: {len(found5)} 个")
        if found5:
            for c in found5[:5]:
                print(f"  {[NAMES[i] for i in c]}")

    res = {
        "patterns": len(pat_a),
        "nonzero": len(nz),
        "found4": [[NAMES[i] for i in c] for c in found[:30]],
        "min_mixed4": min_mixed,
        "min_combo4": [NAMES[i] for i in min_combo] if min_combo else None,
    }
    with open(os.path.join(SCRIPT_DIR, "paperX_n6_order4_results.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("DONE")
