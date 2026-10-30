# -*- coding: utf-8 -*-
"""59 因子独立复核扩展：seed 331 / 777 / 555 各 15000（跨集一致性稳健性）
用法：python paperX_n10_indep59.py 331 777 555
"""
import json, os, random, sys, time
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_block
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_n10_criterion import adj_partition_factors


def factor_name(a, b):
    def s(t):
        return "".join(str(x + 1) for x in t)
    return "s" + s(a) + "_" + s(b)


if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [331, 777, 555]
    # 59 因子基座：final_base + 7 前缀 + s2_3 + s3_4
    with open(os.path.join(SCRIPT_DIR, "paperX_n10_final_base.json"), encoding="utf-8") as f:
        fb = json.load(f)
    base_names = list(dict.fromkeys(fb["base"] + ["s23_45678910", "s234_5678910", "s2345_678910",
                                                  "s23456_78910", "s234567_8910", "s2345678_910",
                                                  "s23456789_10", "s2_3", "s3_4"]))
    factors = adj_partition_factors(10)
    NAMES = [factor_name(a, b) for a, b in factors]
    idx = [NAMES.index(x) for x in base_names]
    print(f"基座 {len(idx)} 因子", flush=True)

    # 主表 59 维
    rng = random.Random(131)
    pat_a = defaultdict(set)
    for _ in range(40000):
        omega, zbar, _ = gen_partial_collinear(10, 0, r1=True, momentum=True, rng=rng)
        pat = tuple(sg_block(omega, zbar, factors[i][0], factors[i][1]) for i in idx)
        pat_a[pat].add(round(A_BG(10, omega, zbar), 6))
    print(f"主表 {len(pat_a)} 模式", flush=True)

    tot = 0
    for seed in seeds:
        rng = random.Random(seed)
        pat_a2 = defaultdict(set)
        bad = 0
        t0 = time.time()
        for _ in range(15000):
            omega, zbar, _ = gen_partial_collinear(10, 0, r1=True, momentum=True, rng=rng)
            pat = tuple(sg_block(omega, zbar, factors[i][0], factors[i][1]) for i in idx)
            pat_a2[pat].add(round(A_BG(10, omega, zbar), 6))
        for p, vals in pat_a2.items():
            if len(vals) > 1:
                bad += 1
            if p in pat_a and not vals <= pat_a[p]:
                bad += 1
        tot += bad
        print(f"seed {seed}: 模式 {len(pat_a2)} 冲突 {bad} ({time.time()-t0:.0f}s)", flush=True)
    print(f"总计冲突 {tot} -> {'PASS' if tot == 0 else 'FAIL'}")
    with open(os.path.join(SCRIPT_DIR, "paperX_n10_indep59_summary.json"), "w", encoding="utf-8") as f:
        json.dump({"base_size": len(idx), "seeds": seeds, "violations": tot, "pass": tot == 0},
                  f, ensure_ascii=False, indent=2)
    print("DONE")
