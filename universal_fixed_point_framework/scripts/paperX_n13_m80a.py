# -*- coding: utf-8 -*-
"""M80a：n=13 标度外推（粗测 3×2000=6000）
- 阈值化采样 + R1 通式生长 + 最小化
- 验证：谱维数 26 普适常数（n≥11）在 n=13 是否成立
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


def r1_formula(n):
    r1 = []
    for m in range(2, n):
        r1.append("s%s_%s" % (str(m), str(m + 1)))
    for m in range(1, n - 1):
        r1.append("s1_%s" % "".join(str(x) for x in range(2, m + 2)))
    return r1


def grow(samples, names, NAMES, factors, max_steps=400):
    idx = [NAMES.index(x) for x in names if x in NAMES]
    used = set(idx)
    cur = list(idx)
    c = conflict_count(group(samples, cur))
    growth = []
    step = 0
    while c > 0 and step < max_steps:
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
    n = 13
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    print(f"n={n} 阈值化采样（3×2000=6000）——因子空间 {len(factors)}", flush=True)
    t0 = time.time()
    datas = {}
    for sd in ["77", "331", "777"]:
        rng = random.Random(int(sd))
        data = []
        for _ in range(2000):
            omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
            full = tuple(sg_thr(sum(omega[x] * omega[y] * (zbar[x] - zbar[y])
                                    for x in a for y in b)) for a, b in factors)
            data.append((full, round(A_BG(n, omega, zbar), 6)))
        datas[sd] = data
        print(f"seed {sd} 完成（{time.time()-t0:.0f}s）", flush=True)
    samples = []
    for sd in ["77", "331", "777"]:
        samples.extend(datas[sd])
    with open(os.path.join(SCRIPT_DIR, "cache_n13_thr3x2000.pkl"), "wb") as f:
        pickle.dump(datas, f)
    print(f"样本 {len(samples)}——缓存已存", flush=True)

    r1 = r1_formula(n)
    cur, growth, cf = grow(samples, r1, NAMES, factors)
    print(f"R1 生长：{len(r1)} + {len(growth)} = {len(cur)} 因子冲突 {cf}", flush=True)
    sizes = []
    for r in range(3):
        sizes.append(len(minimize(samples, cur, 20261008 + r)))
    print(f"最小化 3 轮：{sizes}——最佳 {min(sizes)}", flush=True)

    out = {"n": n, "samples": len(samples), "factors": len(factors),
           "r1_size": len(r1), "growth": growth, "grow_size": len(cur),
           "grow_conflict": cf, "min_sizes": sizes, "min": min(sizes)}
    with open(os.path.join(SCRIPT_DIR, "paperX_n13_m80a_scale.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n13_m80a_scale.json", flush=True)
