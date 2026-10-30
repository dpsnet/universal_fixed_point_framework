# -*- coding: utf-8 -*-
"""n=10 M17：80000 级对齐（59 基座 3 seed × 80000）——反转 50<59 严格确认
- 采样 77/331/777 × 80000（n=10，165 因子，缓存存盘 cache_n10_3x80000.pkl）
- 59 基座非决定判定
"""
import json, os, pickle, random, sys, time
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_block
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear

CACHE = os.path.join(SCRIPT_DIR, "cache_n10_3x80000.pkl")


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
    n = 10
    t_start = time.time()
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    base = json.load(open(SCRIPT_DIR + "/paperX_n10_final_summary_59.json", encoding="utf-8"))
    b59 = [NAMES.index(x) for x in base["base"]]
    print(f"59 基座：{len(b59)} 因子", flush=True)
    seeds = ["77", "331", "777"]

    if os.path.exists(CACHE):
        with open(CACHE, "rb") as f:
            datas = pickle.load(f)
        print("缓存命中", flush=True)
    else:
        datas = {}
        for sd in seeds:
            rng = random.Random(int(sd))
            data = []
            for _ in range(80000):
                omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
                full = tuple(sg_block(omega, zbar, a, b) for a, b in factors)
                data.append((full, round(A_BG(n, omega, zbar), 6)))
            datas[sd] = data
            print(f"seed {sd} 80000 完成 ({time.time()-t_start:.0f}s)", flush=True)
        with open(CACHE, "wb") as f:
            pickle.dump(datas, f)
        print("缓存已保存", flush=True)

    results = {}
    for sd in seeds:
        data = datas[sd]
        nd = nondet_count(data, b59)
        uniq = len(set(tuple(d[i] for i in b59) for d, _ in data))
        results[sd] = {"nondet_80000": nd, "unique_rate": round(uniq / 80000, 4)}
        print(f"seed {sd} @80000: 非决定 {nd} 唯一率 {uniq/80000:.3f}", flush=True)

    all_zero = all(v["nondet_80000"] == 0 for v in results.values())
    res = {"n": n, "basis_size": len(b59), "samples_per_seed": 80000,
           "seeds": seeds, "per_seed": results,
           "all_zero_80000": all_zero,
           "inversion_confirmed": all_zero,  # 50(n=11) < 59(n=10) 需 59 @80000 全 0
           "elapsed_s": round(time.time() - t_start, 1)}
    with open(os.path.join(SCRIPT_DIR, "paperX_n10_audit59_80000.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print(f"DONE ({time.time()-t_start:.0f}s) -> paperX_n10_audit59_80000.json, 反转确认 = {all_zero}")
