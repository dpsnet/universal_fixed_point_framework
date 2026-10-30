# -*- coding: utf-8 -*-
"""M44：43 强极小验证（阈值化缓存多轮随机序）
- 读 cache_n11_thr3x20000.pkl（60000 样本）
- 5 轮随机序正确极小化（从 220 全因子）——全部终局 43？
- 43 必要性（逐删验证）
"""
import os, sys, json, pickle, random, time
from collections import defaultdict

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
    for r in range(5):
        cur = minimize(all_samples, full, 20261006 + r)
        sizes.append(len(cur))
        finals.append([NAMES[i] for i in sorted(cur)])
        print(f"轮{r+1}：{len(cur)} 因子（{time.time()-t0:.0f}s）", flush=True)
    print(f"\n5 轮终局：{sizes}", flush=True)
    common = set(finals[0])
    for f in finals[1:]:
        common &= set(f)
    print(f"5 轮公共因子：{len(common)}", flush=True)

    # 43 名单必要性（逐删）
    if len(finals[0]) == 43:
        best_idx = [NAMES.index(x) for x in finals[0]]
        sens = {}
        for i in best_idx:
            trial = [x for x in best_idx if x != i]
            c = conflict_count(group(all_samples, trial))
            sens[NAMES[i]] = c
            if c > 0:
                print(f"删 {NAMES[i]} → {c} 冲突", flush=True)
        print(f"\n必要性验证：{len([v for v in sens.values() if v > 0])}/{len(sens)} 必要", flush=True)

        out = {"n": n, "sizes": sizes, "common5": len(common),
               "final43": finals[0], "sensitivity": sens}
        with open(os.path.join(SCRIPT_DIR, "paperX_n11_m44_strongmin.json"), "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
        print("DONE -> paperX_n11_m44_strongmin.json", flush=True)
