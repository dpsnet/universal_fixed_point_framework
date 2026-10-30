# -*- coding: utf-8 -*-
"""M40：阈值化重采样 + 极小化（真实谱维数——消除浮点零点噪声）
- 阈值化：|s| < 1e-6 → 0（物理零）
- 3 seed × 20000 = 60000 样本（A_BG 每样本 ~100ms——总 ~1.7h——后台运行）
- 220 阈值化 0 冲突验证 → 阈值化极小化 → 真实谱维数
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
    n = 11
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    print(f"阈值化采样（THR={THR}）——3 seed × 20000", flush=True)

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
    with open(os.path.join(SCRIPT_DIR, "cache_n11_thr3x20000.pkl"), "wb") as f:
        pickle.dump(datas, f)
    print("缓存已保存 cache_n11_thr3x20000.pkl", flush=True)

    all_samples = []
    for sd in ["77", "331", "777"]:
        all_samples.extend(datas[sd])
    print(f"样本 {len(all_samples)}", flush=True)

    # 220 阈值化冲突
    full = list(range(len(factors)))
    c220 = conflict_count(group(all_samples, full))
    print(f"220 阈值化冲突：{c220}", flush=True)

    # 阈值化极小化（2 轮随机序）
    t0 = time.time()
    cur1 = minimize(all_samples, full, 20261006)
    print(f"极小化轮1：{len(cur1)} 因子（{time.time()-t0:.0f}s）——冲突 {conflict_count(group(all_samples, cur1))}", flush=True)
    t0 = time.time()
    cur2 = minimize(all_samples, full, 20261007)
    print(f"极小化轮2：{len(cur2)} 因子（{time.time()-t0:.0f}s）——冲突 {conflict_count(group(all_samples, cur2))}", flush=True)
    best = cur1 if len(cur1) <= len(cur2) else cur2
    names = [NAMES[i] for i in sorted(best)]
    cf = conflict_count(group(all_samples, best))
    print(f"\n阈值化真实谱维数：{len(best)}（冲突 {cf}）", flush=True)

    # 全补块检查（阈值化下应恒 0——不在极小集）
    fullset = set(range(n))
    fc_in_best = [nm for nm in names if set(factors[NAMES.index(nm)][0]) | set(factors[NAMES.index(nm)][1]) == fullset]
    print(f"极小集中全补块：{fc_in_best}", flush=True)

    out = {"n": n, "thr": THR, "samples": len(all_samples), "c220": c220,
           "round1": len(cur1), "round2": len(cur2), "final_size": len(best),
           "final_names": names, "final_conflict": cf, "fullcomp_in_best": fc_in_best}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_m40_thr_spectral.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n11_m40_thr_spectral.json", flush=True)
