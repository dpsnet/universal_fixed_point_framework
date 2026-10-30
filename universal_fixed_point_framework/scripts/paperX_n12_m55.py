# -*- coding: utf-8 -*-
"""M55：n=12 R1 生长外推（减量样本——饱和验证）
- 3 seed × 2000 = 6000 阈值化（n=12 A_BG 慢——粗验证）
- R1 通式 → 贪心追加 → 完备大小（预测生长 ~30、最小化 ~27）
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


def grow(samples, names, NAMES, factors):
    idx = [NAMES.index(x) for x in names if x in NAMES]
    used = set(idx)
    cur = list(idx)
    c = conflict_count(group(samples, cur))
    growth = []
    step = 0
    while c > 0 and step < 400:
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


if __name__ == "__main__":
    n = 12
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    print(f"n={n} 阈值化采样（3×2000=6000）", flush=True)
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
    with open(os.path.join(SCRIPT_DIR, "cache_n12_thr3x2000.pkl"), "wb") as f:
        pickle.dump(datas, f)
    print(f"样本 {len(samples)}——缓存已存", flush=True)

    r1 = r1_formula(n)
    c_r1 = conflict_count(group(samples, [NAMES.index(x) for x in r1]))
    print(f"R1 通式 {len(r1)} 因子冲突 {c_r1}", flush=True)
    cur, growth, cf = grow(samples, r1, NAMES, factors)
    names = [NAMES[i] for i in sorted(cur)]
    print(f"生长追加 {len(growth)}——总 {len(cur)} 因子冲突 {cf}", flush=True)
    print(f"追加：{growth}", flush=True)

    # 最小化（删冗余）
    random.seed(20261007)
    cur2 = list(cur)
    random.shuffle(cur2)
    while True:
        rem = False
        for i in list(cur2):
            trial = [x for x in cur2 if x != i]
            if conflict_count(group(samples, trial)) == 0:
                cur2 = trial
                rem = True
        if not rem:
            break
    print(f"最小化后：{len(cur2)} 因子冲突 {conflict_count(group(samples, cur2))}", flush=True)

    out = {"n": n, "samples": len(samples), "r1_size": len(r1), "c_r1": c_r1,
           "growth": growth, "final_size": len(cur), "final_conflict": cf,
           "min_size": len(cur2), "min_names": [NAMES[i] for i in sorted(cur2)]}
    with open(os.path.join(SCRIPT_DIR, "paperX_n12_m55_scale.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nDONE -> paperX_n12_m55_scale.json", flush=True)
