# -*- coding: utf-8 -*-
"""M47：50 轮继续下探（谱维数 < 40 探索）
- 50 轮随机序极小化——记录最小终局
- 最小名单必要性验证
"""
import os, sys, json, pickle, random, time
from collections import defaultdict, Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_n11_domain_audit import adj_partition_factors, factor_name


def conflict_count(pats):
    return sum(1 for vals in pats.values() if len(set(vals)) > 1)


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
    n = 11
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    with open(os.path.join(SCRIPT_DIR, "cache_n11_thr3x20000.pkl"), "rb") as f:
        d = pickle.load(f)
    all_samples = []
    for sd in ["77", "331", "777"]:
        all_samples.extend(d[sd])
    print(f"阈值化样本 {len(all_samples)}", flush=True)

    full = list(range(len(factors)))
    sizes = []
    finals = []
    t0 = time.time()
    for r in range(50):
        cur = minimize(all_samples, full, 20261006 + 100 + r)
        sizes.append(len(cur))
        finals.append([NAMES[i] for i in sorted(cur)])
        if len(cur) <= min(sizes) or (r + 1) % 10 == 0:
            print(f"轮{r+1}：{len(cur)} 因子（{time.time()-t0:.0f}s，当前最小 {min(sizes)}）", flush=True)
    print(f"\n50 轮终局最小：{min(sizes)}、最大：{max(sizes)}、均值：{sum(sizes)/len(sizes):.2f}", flush=True)
    print(f"分布：{dict(Counter(sizes))}", flush=True)

    min_size = min(sizes)
    min_idx = sizes.index(min_size)
    best = finals[min_idx]
    print(f"最小名单（轮{min_idx+1}，{min_size} 因子）", flush=True)
    best_idx = [NAMES.index(x) for x in best]
    sens = {}
    n_nec = 0
    for i in best_idx:
        trial = [x for x in best_idx if x != i]
        c = conflict_count(group(all_samples, trial))
        sens[NAMES[i]] = c
        if c > 0:
            n_nec += 1
    print(f"必要 {n_nec}/{min_size}", flush=True)
    red = [nm for nm, c in sens.items() if c == 0]
    print(f"冗余：{red}", flush=True)

    out = {"n": n, "sizes50": sizes, "min": min_size, "max": max(sizes),
           "mean": round(sum(sizes) / len(sizes), 2), "dist": dict(Counter(sizes)),
           "min_names": best, "min_round": min_idx + 1,
           "sens_min": sens, "min_necessary": n_nec, "min_redundant": red}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_m47_deeper.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n11_m47_deeper.json", flush=True)
