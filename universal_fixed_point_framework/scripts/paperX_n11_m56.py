# -*- coding: utf-8 -*-
"""M56：n=11 样本量-谱维数曲线（采样依赖性量化）
- 从 60000 阈值化缓存取子集：10000/20000/30000/45000/60000
- 每档 R1 生长 + 最小化——谱维数 vs 样本量
- 收敛行为判断（是否趋向极限）
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


def r1_formula(n):
    r1 = []
    for m in range(2, n):
        r1.append("s%s_%s" % (str(m), str(m + 1)))
    for m in range(1, n - 1):
        r1.append("s1_%s" % "".join(str(x) for x in range(2, m + 2)))
    return r1


def grow(samples, names, NAMES, factors):
    idx = [NAMES.index(x) for x in names if x in NAMES]
    used = set(idx)
    cur = list(idx)
    c = conflict_count(group(samples, cur))
    growth = []
    step = 0
    while c > 0 and step < 300:
        best = None
        best_c = c
        for i in range(len(factors)):
            if i in used:
                continue
            ci = conflict_count(group(samples, cur + [i]))
            if ci < best_c:
                best_c = ci
                best = i
        if best is None:
            break
        cur.append(best)
        used.add(best)
        growth.append((NAMES[best], best_c))
        c = best_c
        step += 1
    return cur, growth, c


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
    print(f"全量 {len(all_samples)} 样本", flush=True)
    r1 = r1_formula(n)

    # 每档 = 从全量取前 N 个（保持 seed 顺序：77 前 20000、331 前 20000...）
    results = {}
    for N in [10000, 20000, 30000, 45000, 60000]:
        sub = all_samples[:N]
        t0 = time.time()
        # R1 生长
        cur, growth, cf = grow(sub, r1, NAMES, factors)
        # 最小化（3 轮取最小）
        sizes = []
        for r in range(3):
            sizes.append(len(minimize(sub, cur, 20261007 + r)))
        best = min(sizes)
        results[str(N)] = {"grow": len(cur), "grow_conflict": cf,
                           "min_sizes": sizes, "min": best}
        print(f"样本 {N}：生长 {len(cur)}（冲突 {cf}）——最小化 {sizes}——最佳 {best}（{time.time()-t0:.0f}s）", flush=True)

    with open(os.path.join(SCRIPT_DIR, "paperX_n11_m56_samplescan.json"), "w", encoding="utf-8") as f:
        json.dump({"n": n, "results": results}, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n11_m56_samplescan.json", flush=True)
