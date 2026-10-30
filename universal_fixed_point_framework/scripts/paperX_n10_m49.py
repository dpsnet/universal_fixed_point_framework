# -*- coding: utf-8 -*-
"""M49：n=10 阈值化真实谱维数（M40 模板复用）
- THR=1e-6 阈值化重采样（3 seed × 20000 = 60000，A_BG n=10）
- 165 阈值化冲突验证 → 极小化 3 轮 → 谱维数 + 全补检查
"""
import os, sys, json, pickle, random, time
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_n11_domain_audit import adj_partition_factors, factor_name
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_single_minus_bg_recursion import A_BG

THR = 1e-6


def sg_thr(x):
    if x > THR:
        return 1
    if x < -THR:
        return -1
    return 0


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
    n = 10
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    print(f"n={n} 阈值化采样（THR={THR}）——3 seed × 20000", flush=True)

    datas = {}
    t_start = time.time()
    for sd in ["77", "331", "777"]:
        rng = random.Random(int(sd))
        data = []
        for _ in range(20000):
            omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
            full = tuple(sg_thr(sum(omega[x] * omega[y] * (zbar[x] - zbar[y])
                                    for x in a for y in b)) for a, b in factors)
            data.append((full, round(A_BG(n, omega, zbar), 6)))
        datas[sd] = data
        print(f"seed {sd} 完成 ({time.time()-t_start:.0f}s)", flush=True)
    with open(os.path.join(SCRIPT_DIR, "cache_n10_thr3x20000.pkl"), "wb") as f:
        pickle.dump(datas, f)
    print("缓存已保存 cache_n10_thr3x20000.pkl", flush=True)

    all_samples = []
    for sd in ["77", "331", "777"]:
        all_samples.extend(datas[sd])
    print(f"样本 {len(all_samples)}", flush=True)

    full = list(range(len(factors)))
    c_full = conflict_count(group(all_samples, full))
    print(f"165 阈值化冲突：{c_full}", flush=True)

    sizes = []
    t0 = time.time()
    for r in range(3):
        cur = minimize(all_samples, full, 20261006 + r)
        sizes.append(len(cur))
        print(f"极小化轮{r+1}：{len(cur)} 因子（{time.time()-t0:.0f}s）", flush=True)
    best = min(sizes)
    bidx = sizes.index(best)
    # 重新找 best 名单
    cur1 = minimize(all_samples, full, 20261006)
    names = [NAMES[i] for i in sorted(cur1)]
    fc_in = [nm for nm in names if set(factors[NAMES.index(nm)][0]) | set(factors[NAMES.index(nm)][1]) == set(range(n))]
    print(f"\nn=10 谱维数：轮 {sizes}——最小 {best}", flush=True)
    print(f"极小集全补块：{fc_in}", flush=True)

    out = {"n": n, "thr": THR, "samples": len(all_samples), "c_full": c_full,
           "rounds": sizes, "min": best, "min_names": names, "fullcomp_in_min": fc_in}
    with open(os.path.join(SCRIPT_DIR, "paperX_n10_m49_thr_spectral.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n10_m49_thr_spectral.json", flush=True)
