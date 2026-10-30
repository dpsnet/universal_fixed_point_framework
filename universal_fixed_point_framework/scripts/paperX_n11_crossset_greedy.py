# -*- coding: utf-8 -*-
"""n=11 跨集充分性贪心重跑（登记①关键实验）
- 5 seed（77/211/331/777/555）各采样 20000 = 100000 样本缓存
- 贪心删除：候选删除必须**所有 5 seed 缓存上充分**（跨集判定）才删
- 对照：单缓存贪心 38 因子（minbasis）→ 跨集贪心应更大更充分
- 独立 seed 131 × 20000 复核非决定数
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


def cache_samples(n_samples, seed, factors, n=11):
    rng = random.Random(seed)
    data = []
    t0 = time.time()
    for _ in range(n_samples):
        omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
        full = tuple(sg_block(omega, zbar, a, b) for a, b in factors)
        data.append((full, round(A_BG(n, omega, zbar), 6)))
    print(f"  seed {seed} 采样 {n_samples} ({time.time()-t0:.0f}s)", flush=True)
    return data


def sufficient_on(data, idx):
    pat_a = defaultdict(set)
    for full, a in data:
        pat = tuple(full[i] for i in idx)
        pat_a[pat].add(a)
    return all(len(v) == 1 for v in pat_a.values())


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
    print(f"n=11 全集 {len(factors)} 因子", flush=True)

    SEEDS = (77, 211, 331, 777, 555)
    caches = [cache_samples(20000, sd, factors) for sd in SEEDS]
    print(f"5 缓存采样完成 ({time.time()-t_start:.0f}s)", flush=True)

    # 跨集贪心删除：每步 5 缓存全充分才删
    cur = list(range(len(factors)))
    changed = True
    passes = 0
    while changed:
        changed = False
        passes += 1
        for i in range(len(cur)):
            trial = cur[:i] + cur[i + 1:]
            if all(sufficient_on(c, trial) for c in caches):
                cur = trial
                changed = True
                print(f"  删除 {len(factors)-len(cur)} 个 (pass {passes}, {time.time()-t_start:.0f}s)", flush=True)
                break
    print(f"跨集贪心删除最小集 ({len(cur)}/{len(factors)}): {[NAMES[i] for i in cur]}", flush=True)

    # 独立复核 seed 131
    data_v = cache_samples(20000, 131, factors)
    nd = nondet_count(data_v, cur)
    print(f"独立 20000 复核: 非决定 {nd} -> {'PASS' if nd == 0 else 'FAIL'}", flush=True)

    res = {"n": n, "greedy_type": "crossset_5seed", "factors_total": len(factors),
           "remove_set": [NAMES[i] for i in cur], "remove_size": len(cur),
           "verify_seed": 131, "verify_samples": 20000, "verify_nondet": nd,
           "verify_pass": nd == 0, "elapsed_s": round(time.time() - t_start, 1)}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_crossset_greedy.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print(f"DONE ({time.time()-t_start:.0f}s) -> paperX_n11_crossset_greedy.json")
