# -*- coding: utf-8 -*-
"""M36b：n=10 随机序 5 轮强化（确认谱维数下界分布）"""
import os, json, pickle, sys, random, time
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_n11_domain_audit import adj_partition_factors, factor_name


def sg(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def conflict_count(pats):
    return sum(1 for vals in pats.values() if len({sg(v) for v in vals}) > 1)


def group(samples, idx):
    pat = defaultdict(list)
    for facs, a in samples:
        pat[tuple(facs[i] for i in idx)].append(a)
    return pat


def minimize(samples, start_idx, seed):
    random.seed(seed)
    cur = list(start_idx)
    random.shuffle(cur)
    while True:
        removed_any = False
        for i in list(cur):
            trial = [x for x in cur if x != i]
            if conflict_count(group(samples, trial)) == 0:
                cur = trial
                removed_any = True
        if not removed_any:
            break
    return cur


if __name__ == "__main__":
    n = 10
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    with open(os.path.join(SCRIPT_DIR, "cache_n10_3x80000.pkl"), "rb") as f:
        d = pickle.load(f)
    all_samples = []
    for sd in d:
        all_samples.extend(d[sd])
    full = list(range(len(factors)))

    t0 = time.time()
    sizes = []
    for k in range(5):
        cur = minimize(all_samples, full, 1000 + k)
        sizes.append(len(cur))
        print(f"  轮 {k+1}: 终局 {len(cur)}（{time.time()-t0:.0f}s）")
    print(f"分布：{sorted(set(sizes))}——最小 {min(sizes)}——出现 {[sizes.count(m) for m in sorted(set(sizes))]}")
    out = {"n": n, "rounds_sizes": sizes, "min_size": min(sizes)}
    with open(os.path.join(SCRIPT_DIR, "paperX_n10_m36b_rounds.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n10_m36b_rounds.json")
