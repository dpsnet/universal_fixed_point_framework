# -*- coding: utf-8 -*-
"""n=10 最小基座大样本检验：40000 样本暴露稀有非决定性模式（n=8/n=9 教训）"""
import json, os, random, sys, time
from collections import Counter, defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_block
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_n10_criterion import adj_partition_factors

BASE = None  # 由 paperX_n10_minbasis_results.json 提供


def factor_name(a, b):
    def s(t):
        return "".join(str(x + 1) for x in t)
    return "s" + s(a) + "_" + s(b)


def pattern_on(omega, zbar, factors, idx):
    return tuple(sg_block(omega, zbar, factors[i][0], factors[i][1]) for i in idx)


if __name__ == "__main__":
    with open(os.path.join(SCRIPT_DIR, "paperX_n10_minbasis_results.json"), encoding="utf-8") as f:
        mb = json.load(f)
    BASE = mb["remove_set"]
    factors = adj_partition_factors(10)
    NAMES = [factor_name(a, b) for a, b in factors]
    idx = [NAMES.index(x) for x in BASE]
    print(f"基座 {len(idx)} 因子: {BASE}", flush=True)

    rng = random.Random(131)
    pat_a = defaultdict(set)
    pat_cnt = Counter()
    t0 = time.time()
    for _ in range(40000):
        omega, zbar, _ = gen_partial_collinear(10, 0, r1=True, momentum=True, rng=rng)
        pat = pattern_on(omega, zbar, factors, idx)
        pat_cnt[pat] += 1
        pat_a[pat].add(round(A_BG(10, omega, zbar), 6))
    nondet = [p for p in pat_a if len(pat_a[p]) > 1]
    print(f"主样本 40000 ({time.time()-t0:.0f}s): 模式 {len(pat_a)} 非决定性 {len(nondet)}", flush=True)
    for p in nondet:
        print(f"  非决定模式 频次 {pat_cnt[p]} 取值 {sorted(pat_a[p])}", flush=True)

    res = {"base": BASE, "size": len(idx), "main_samples": 40000,
           "total_patterns": len(pat_a), "nondet": len(nondet),
           "nondet_details": [{"freq": pat_cnt[p], "vals": sorted(pat_a[p])} for p in nondet]}
    with open(os.path.join(SCRIPT_DIR, "paperX_n10_verify_results.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("DONE -> paperX_n10_verify_results.json")
