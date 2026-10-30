# -*- coding: utf-8 -*-
"""n=11 M7：强闭合级最小二分搜索（删除链 + 80000 投影）
- 20000 缓存（seed 131）逐删记录删除链（140→34）
- 80000 缓存（单次采样）对链上多规模点投影验证非决定
- 二分定位：0 非决定 → 下探；FAIL → 上探
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


if __name__ == "__main__":
    n = 11
    t_start = time.time()
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    ac = json.load(open(SCRIPT_DIR + "/paperX_n11_approx_closed.json", encoding="utf-8"))
    cg = json.load(open(SCRIPT_DIR + "/paperX_n11_crossset_greedy.json", encoding="utf-8"))
    start_names = cg["remove_set"] + ac["extra_set"]
    start_idx = [NAMES.index(x) for x in start_names]
    print(f"n=11 起点 140 因子", flush=True)

    # ---- 20000 缓存逐删记录删除链 ----
    rng = random.Random(131)
    data = []
    t0 = time.time()
    for _ in range(20000):
        omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
        full = tuple(sg_block(omega, zbar, a, b) for a, b in factors)
        data.append((full, round(A_BG(n, omega, zbar), 6)))
    print(f"缓存 20000 ({time.time()-t0:.0f}s)", flush=True)

    chain = [list(start_idx)]  # chain[0] = 140 因子全集起点
    cur = list(start_idx)
    changed = True
    passes = 0
    while changed:
        changed = False
        passes += 1
        for i in range(len(cur)):
            trial = cur[:i] + cur[i + 1:]
            if nondet_count(data, trial) == 0:
                cur = trial
                chain.append(list(cur))
                changed = True
                break
    print(f"删除链：140 → {len(cur)}（{len(chain)} 个规模点，{time.time()-t_start:.0f}s）", flush=True)

    # ---- 80000 缓存（单次采样，投影到链上规模点）----
    rng = random.Random(131)
    big = []
    t0 = time.time()
    for _ in range(80000):
        omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
        full = tuple(sg_block(omega, zbar, a, b) for a, b in factors)
        big.append((full, round(A_BG(n, omega, zbar), 6)))
    print(f"缓存 80000 ({time.time()-t0:.0f}s)", flush=True)

    # 链上规模点选择：二分框架 + 全链投影曲线
    sizes = sorted(set(len(c) for c in chain), reverse=True)
    scale_pts = [140, 120, 105, 90, 75, 60, 50, 40, 34]
    scale_pts = [s for s in scale_pts if s in sizes]
    curve = []
    for sz in scale_pts:
        idx = next(c for c in chain if len(c) == sz)
        nd = nondet_count(big, idx)
        uniq = len(set(tuple(f[i] for i in idx) for f, _ in big))
        curve.append({"size": sz, "nondet": nd, "unique": uniq, "rate": round(uniq / 80000, 4)})
        print(f"规模 {sz}: 非决定 {nd} 唯一率 {uniq/80000:.3f}", flush=True)
    # 二分下探：找到最小 0 非决定规模
    ok_sizes = [c["size"] for c in curve if c["nondet"] == 0]
    min_ok = min(ok_sizes) if ok_sizes else None
    fail_max = max([c["size"] for c in curve if c["nondet"] > 0] + [34])
    print(f"强闭合级最小（链上上界）：{min_ok}；FAIL 上界：{fail_max}", flush=True)

    res = {"n": n, "cache_chain": 20000, "verify": 80000, "seed": 131,
           "start_size": len(start_idx), "cache_min": len(cur),
           "curve": curve, "min_strong_closed_chain": min_ok,
           "fail_upper": fail_max,
           "elapsed_s": round(time.time() - t_start, 1)}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_bisect_minimal.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print(f"DONE ({time.time()-t_start:.0f}s) -> paperX_n11_bisect_minimal.json")
