# -*- coding: utf-8 -*-
"""n=11 M14：46 的 80000 级多 seed 确认
- 复用 cache_n11_5seed.pkl（前 20000）
- 77/331/777 续采 60000（同 seed 累积到 80000）→ 46 非决定
"""
import json, os, pickle, random, sys, time
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_block
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear

CACHE = os.path.join(SCRIPT_DIR, "cache_n11_5seed.pkl")


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


def nondet_count(patterns, idx):
    pat_a = defaultdict(set)
    for full, a in patterns:
        pat = tuple(full[i] for i in idx)
        pat_a[pat].add(a)
    return sum(1 for v in pat_a.values() if len(v) > 1)


if __name__ == "__main__":
    n = 11
    t_start = time.time()
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    fj = json.load(open(SCRIPT_DIR + "/paperX_n11_fill45.json", encoding="utf-8"))
    b46 = [NAMES.index(x) for x in fj["final_set"]]
    print(f"确认基座：46 因子", flush=True)

    with open(CACHE, "rb") as f:
        datas = pickle.load(f)
    print("缓存前 20000 已载入", flush=True)

    # 续采 77/331/777 到 80000（同 seed 累积：先消耗前 20000 再采 60000）
    extend = ["77", "331", "777"]
    results = {}
    for sd in extend:
        rng = random.Random(int(sd))
        # 消耗前 20000（只需几何生成，不需 bg）
        for _ in range(20000):
            gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
        # 续采 60000
        data = []
        for _ in range(60000):
            omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
            full = tuple(sg_block(omega, zbar, a, b) for a, b in factors)
            data.append((full, round(A_BG(n, omega, zbar), 6)))
        nd = nondet_count(data, b46)
        uniq = len(set(tuple(f[i] for i in b46) for f, _ in data))
        results[sd] = {"nondet_extra60000": nd, "unique_extra60000": uniq,
                       "rate_extra60000": round(uniq / 60000, 4)}
        print(f"seed {sd} 续采 60000: 非决定 {nd} 唯一率 {uniq/60000:.3f} ({time.time()-t_start:.0f}s)", flush=True)

    res = {"n": n, "basis_size": len(b46), "extend_seeds": extend,
           "samples_extended": 60000, "cache_prefix": 20000,
           "per_seed": results,
           "all_zero": all(v["nondet_extra60000"] == 0 for v in results.values()),
           "elapsed_s": round(time.time() - t_start, 1)}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_audit46_80000.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print(f"DONE ({time.time()-t_start:.0f}s) -> paperX_n11_audit46_80000.json")
