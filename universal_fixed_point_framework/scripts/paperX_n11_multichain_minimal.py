# -*- coding: utf-8 -*-
"""n=11 M8 修复版：140 起点多链最小验证
- seed 77/211/331 各采样 20000 → 从 140 起点（start_idx）逐删链
- 共享 80000 缓存（seed 131）投影 → 各链强闭合级最小 + 跨链单调性
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


def nondet_count(patterns, idx):
    pat_a = defaultdict(set)
    for full, a in patterns:
        pat = tuple(full[i] for i in idx)
        pat_a[pat].add(a)
    return sum(1 for v in pat_a.values() if len(v) > 1)


def build_chain_140(n, factors, start_idx, seed, cap):
    rng = random.Random(seed)
    data = []
    for _ in range(cap):
        omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
        full = tuple(sg_block(omega, zbar, a, b) for a, b in factors)
        data.append((full, round(A_BG(n, omega, zbar), 6)))
    chain = [list(start_idx)]
    cur = list(start_idx)
    while True:
        changed = False
        for i in range(len(cur)):
            trial = cur[:i] + cur[i + 1:]
            if nondet_count(data, trial) == 0:
                cur = trial
                chain.append(list(cur))
                changed = True
                break
        if not changed:
            break
    return data, chain


if __name__ == "__main__":
    n = 11
    t_start = time.time()
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    ac = json.load(open(SCRIPT_DIR + "/paperX_n11_approx_closed.json", encoding="utf-8"))
    cg = json.load(open(SCRIPT_DIR + "/paperX_n11_crossset_greedy.json", encoding="utf-8"))
    start_names = cg["remove_set"] + ac["extra_set"]
    start_idx = [NAMES.index(x) for x in start_names]

    seeds = [77, 211, 331]
    chains = {}
    for sd in seeds:
        data, chain = build_chain_140(n, factors, start_idx, sd, 20000)
        chains[sd] = chain
        print(f"seed {sd}: 140 内部删除链 140→{len(chain[-1])}（{len(chain)} 规模点，{time.time()-t_start:.0f}s）", flush=True)

    # 共享 80000 验证缓存（seed 131，投影到 140 起点子空间）
    rng = random.Random(131)
    big = []
    t0 = time.time()
    for _ in range(80000):
        omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
        full = tuple(sg_block(omega, zbar, a, b) for a, b in factors)
        big.append((full, round(A_BG(n, omega, zbar), 6)))
    print(f"共享 80000 缓存 ({time.time()-t0:.0f}s)", flush=True)

    scale_pts_all = [140, 130, 120, 110, 100, 95, 90, 85, 80, 75, 70, 60, 50, 40, 34]
    results = {}
    for sd in seeds:
        chain = chains[sd]
        sizes = sorted(set(len(c) for c in chain), reverse=True)
        curve = []
        for sz in scale_pts_all:
            if sz not in sizes:
                continue
            idx = next(c for c in chain if len(c) == sz)
            nd = nondet_count(big, idx)
            uniq = len(set(tuple(f[i] for i in idx) for f, _ in big))
            curve.append({"size": sz, "nondet": nd, "unique": uniq, "rate": round(uniq / 80000, 4)})
        ok_sizes = [c["size"] for c in curve if c["nondet"] == 0]
        min_ok = min(ok_sizes) if ok_sizes else None
        fail_sizes = [c["size"] for c in curve if c["nondet"] > 0]
        monotone = True
        for i in range(1, len(curve)):
            if curve[i]["size"] < curve[i - 1]["size"]:
                if curve[i]["nondet"] > curve[i - 1]["nondet"]:
                    monotone = False
        results[sd] = {"min_strong_closed": min_ok,
                       "fail_max": max(fail_sizes) if fail_sizes else None,
                       "monotone": monotone, "curve": curve, "cache_min": len(chain[-1])}
        print(f"seed {sd}: 强闭合级最小 {min_ok}（FAIL 上界 {max(fail_sizes) if fail_sizes else None}）单调 {monotone}", flush=True)

    mins = [r["min_strong_closed"] for r in results.values() if r["min_strong_closed"]]
    res = {"n": n, "chain_seeds": seeds, "verify_seed": 131, "verify_samples": 80000,
           "start_size": len(start_idx), "per_chain": results,
           "min_over_chains": min(mins) if mins else None,
           "max_over_chains": max(mins) if mins else None,
           "all_monotone": all(r["monotone"] for r in results.values()),
           "elapsed_s": round(time.time() - t_start, 1)}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_multichain_minimal.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print(f"DONE ({time.time()-t_start:.0f}s) -> paperX_n11_multichain_minimal.json")
