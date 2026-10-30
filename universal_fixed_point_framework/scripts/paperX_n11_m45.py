# -*- coding: utf-8 -*-
"""M45：43 必要性 + 极小分布深化
- 对 M40 的 43 名单逐删验证（必要性）
- 10 轮随机序极小化——大小分布（43-47？更低？）
- 交叉：不同极小集的大小区间
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

    # 1) 43 名单必要性（M40 的 final_names）
    m40 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_m40_thr_spectral.json"), encoding="utf-8"))
    names43 = m40["final_names"]
    idx43 = [NAMES.index(x) for x in names43]
    print(f"M40 43 名单必要性验证：", flush=True)
    sens = {}
    n_necessary = 0
    for i in idx43:
        trial = [x for x in idx43 if x != i]
        c = conflict_count(group(all_samples, trial))
        sens[NAMES[i]] = c
        if c > 0:
            n_necessary += 1
    print(f"必要 {n_necessary}/43（其余删除后仍 0 冲突——冗余）", flush=True)
    red = [nm for nm, c in sens.items() if c == 0]
    print(f"冗余因子：{red}", flush=True)

    # 2) 10 轮随机序极小化分布
    full = list(range(len(factors)))
    sizes = []
    t0 = time.time()
    for r in range(10):
        cur = minimize(all_samples, full, 20261006 + r)
        sizes.append(len(cur))
        print(f"轮{r+1}：{len(cur)} 因子（{time.time()-t0:.0f}s）", flush=True)
    print(f"\n10 轮终局：{sizes}", flush=True)
    print(f"最小 {min(sizes)}、最大 {max(sizes)}、均值 {sum(sizes)/len(sizes):.1f}", flush=True)

    out = {"n": n, "sens43": sens, "n43_necessary": n_necessary,
           "redundant_in_43": red, "sizes10": sizes, "min": min(sizes), "max": max(sizes)}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_m45_strongmin2.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n11_m45_strongmin2.json", flush=True)
