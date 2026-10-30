# -*- coding: utf-8 -*-
"""n=11 非决定暴露速率实验（采样代表性理论，登记②落地）
- 38 因子贪心基座，seed 131 累积采样（避免重复采样）
- 递增样本：5000/10000/20000/40000/80000 → 非决定数暴露曲线
- 外推：非决定模式完全暴露所需样本规模（完整闭合预算依据）
"""
import json, os, random, sys, time
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_block
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear


def adj_partition_factors(n):
    names = []
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(i, j):
                a = tuple(range(i, k + 1))
                b = tuple(range(k + 1, j + 1))
                names.append((a, b))
    return names


def factor_name(a, b):
    def s(t):
        return "".join(str(x + 1) for x in t)
    return "s" + s(a) + "_" + s(b)


if __name__ == "__main__":
    n = 11
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    mb = json.load(open(SCRIPT_DIR + "/paperX_n11_minbasis_results.json", encoding="utf-8"))
    base_idx = [NAMES.index(x) for x in mb["remove_set"]]
    print(f"n=11 基座 {len(base_idx)} 因子", flush=True)

    stages = [5000, 10000, 20000, 40000, 80000]
    rng = random.Random(131)
    pat_a = defaultdict(set)      # 累积
    pat_first_seen = {}
    t0 = time.time()
    last = 0
    curve = []
    for target in stages:
        for _ in range(target - last):
            omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
            full = tuple(sg_block(omega, zbar, a, b) for a, b in factors)
            pat = tuple(full[i] for i in base_idx)
            bg = round(A_BG(n, omega, zbar), 6)
            if pat not in pat_a:
                pat_a[pat] = set()
                pat_first_seen[pat] = target
            pat_a[pat].add(bg)
        last = target
        nondet = [p for p in pat_a if len(pat_a[p]) > 1]
        curve.append({"samples": target, "unique_pats": len(pat_a),
                      "nondet": len(nondet),
                      "nondet_pats": [None for _ in nondet]})
        print(f"样本 {target}: 模式 {len(pat_a)} 非决定 {len(nondet)} ({time.time()-t0:.0f}s)", flush=True)

    # 新增非决定暴露（每阶段的增量）
    prev = 0
    for c in curve:
        c["new_nondet"] = c["nondet"] - prev
        prev = c["nondet"]

    # 非决定模式首次暴露分布
    expose = defaultdict(int)
    for p in pat_a:
        if len(pat_a[p]) > 1:
            for st in stages:
                if pat_first_seen[p] <= st:
                    expose[st] += 1
    print("非决定模式暴露曲线:", dict(expose), flush=True)

    res = {"n": n, "base_size": len(base_idx), "seed": 131,
           "curve": curve, "first_exposure": {str(k): v for k, v in expose.items()}}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_exposure.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print(f"DONE ({time.time()-t0:.0f}s) -> paperX_n11_exposure.json")
