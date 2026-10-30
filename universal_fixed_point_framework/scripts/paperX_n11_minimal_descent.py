# -*- coding: utf-8 -*-
"""n=11 M6：140 最小性验证（贪心逐删 → 临界展开点）
- 20000 缓存（seed 131）：full 220 维向量 + bg（一次性采样，逐删判定全在缓存上）
- 从 140 出发贪心逐删：每步检查缓存上 0 非决定（决定性判据）
- 输出缓存级最小基座 → 80000 样本暴露速率验证（强闭合是否保持）
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


def nondet_count(data, idx):
    pat_a = defaultdict(set)
    for full, a in data:
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
    print(f"n=11 起点 140 因子，缓存采样 20000...", flush=True)

    # 缓存采样
    rng = random.Random(131)
    data = []
    t0 = time.time()
    for _ in range(20000):
        omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
        full = tuple(sg_block(omega, zbar, a, b) for a, b in factors)
        data.append((full, round(A_BG(n, omega, zbar), 6)))
    print(f"缓存 20000 ({time.time()-t0:.0f}s)", flush=True)

    # 贪心逐删（每步缓存 0 非决定）
    cur = list(start_idx)
    removed = []
    changed = True
    passes = 0
    while changed:
        changed = False
        passes += 1
        for i in range(len(cur)):
            trial = cur[:i] + cur[i + 1:]
            if nondet_count(data, trial) == 0:
                cur = trial
                changed = True
                removed.append(i)
                print(f"  删除 {len(start_idx)-len(cur)} 个 (pass {passes}, {time.time()-t_start:.0f}s)", flush=True)
                break
    print(f"缓存级最小基座 ({len(cur)}/{len(start_idx)}): 非决定 {nondet_count(data, cur)}", flush=True)
    print(f"删除序列（140→{len(cur)}，共 {len(removed)} 步）", flush=True)
    print(f"最小基座因子: {[NAMES[i] for i in cur]}", flush=True)

    # 80000 验证（seed 131 新样本）
    rng = random.Random(131)
    pat_a = defaultdict(set)
    t0 = time.time()
    for _ in range(80000):
        omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
        full = tuple(sg_block(omega, zbar, a, b) for a, b in factors)
        pat = tuple(full[i] for i in cur)
        pat_a[pat].add(round(A_BG(n, omega, zbar), 6))
    nd = sum(1 for v in pat_a.values() if len(v) > 1)
    uniq = len(pat_a)
    print(f"80000 验证: 唯一 {uniq}/80000 ({uniq/80000:.3f}) 非决定 {nd} -> {'强闭合保持' if nd == 0 else 'FAIL（缓存级最小不可靠）'}", flush=True)

    res = {"n": n, "start_size": len(start_idx), "cache": 20000, "cache_seed": 131,
           "min_size_cache": len(cur), "min_set_cache": [NAMES[i] for i in cur],
           "removed_count": len(removed),
           "verify_samples": 80000, "verify_unique": uniq, "verify_nondet": nd,
           "strong_closed": nd == 0,
           "elapsed_s": round(time.time() - t_start, 1)}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_minimal_descent.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print(f"DONE ({time.time()-t_start:.0f}s) -> paperX_n11_minimal_descent.json")
