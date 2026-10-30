# -*- coding: utf-8 -*-
"""M50：28 名单验证 + 最小化下探（R1 生长路径）
- M48 的 R1 18+10=28 名单：0 冲突复验 + 必要性逐删
- 从 28 继续删（能否更小？）
- 多轮随机删序（从 28 起点——找 28 的最小化）
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

    # R1 18 + 追加 10 = 28
    m48 = json.load(open(os.path.join(SCRIPT_DIR, "paperX_n11_m48_r1growth.json"), encoding="utf-8"))
    r1 = m48["r1_names"]
    growth = [x for x, _ in m48["growth"]]
    names28 = r1 + growth
    idx28 = [NAMES.index(x) for x in names28]
    c28 = conflict_count(group(all_samples, idx28))
    print(f"R1 28 因子冲突复验：{c28}", flush=True)

    # 28 必要性
    sens = {}
    n_nec = 0
    for i in idx28:
        trial = [x for x in idx28 if x != i]
        c = conflict_count(group(all_samples, trial))
        sens[NAMES[i]] = c
        if c > 0:
            n_nec += 1
    print(f"28 必要 {n_nec}/28", flush=True)
    red = [nm for nm, c in sens.items() if c == 0]
    print(f"28 冗余：{red}", flush=True)

    # 从 28 多轮随机删序最小化（找 < 28 可能）
    sizes = []
    t0 = time.time()
    for r in range(10):
        cur = minimize(all_samples, idx28, 20261006 + r)
        sizes.append(len(cur))
        print(f"28起点轮{r+1}：{len(cur)} 因子（{time.time()-t0:.0f}s）", flush=True)
    print(f"\n28 起点 10 轮终局：{sizes}——最小 {min(sizes)}", flush=True)

    out = {"n": n, "r1": r1, "growth": growth, "names28": names28,
           "c28": c28, "sens28": sens, "n28_necessary": n_nec, "redundant28": red,
           "sizes_from28": sizes, "min_from28": min(sizes)}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_m50_r1min.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n11_m50_r1min.json", flush=True)
