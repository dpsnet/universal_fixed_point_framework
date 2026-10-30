# -*- coding: utf-8 -*-
"""n=11 跨集一致性审计 + 冲突捕获（M2 v2，修正配对逻辑）
- 基座：贪心 38 因子
- 主样本 15000（seed 131）+ 5 seed × 5000
- 冲突捕获：对每个冲突 pat，同 pat 内采两个样本（bg 不同）→ 全集因子中两者值不同的 = 缺失因子候选
"""
import json, os, random, sys, time
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_block
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear


def adj_partition_factors(n):
    names = []
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(i, j):
                a = tuple(range(i, k + 1))
                b = tuple(range(k + 1, j + 1))
                names.append((a, b))
    return names


def factor_name(a, b):
    def s(t):
        return "".join(str(x + 1) for x in t)
    return "s" + s(a) + "_" + s(b)


if __name__ == "__main__":
    n = 11
    t_start = time.time()
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    mb = json.load(open(SCRIPT_DIR + "/paperX_n11_minbasis_results.json", encoding="utf-8"))
    base_names = mb["remove_set"]
    base_idx = [NAMES.index(x) for x in base_names]
    print(f"n=11 基座 {len(base_idx)} 因子", flush=True)

    rng = random.Random(131)
    pat_a = defaultdict(set)
    t0 = time.time()
    for _ in range(15000):
        omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
        full = tuple(sg_block(omega, zbar, a, b) for a, b in factors)
        pat = tuple(full[i] for i in base_idx)
        pat_a[pat].add(round(A_BG(n, omega, zbar), 6))
    main_nondet = [p for p in pat_a if len(pat_a[p]) > 1]
    print(f"主样本 15000 ({time.time()-t0:.0f}s): 模式 {len(pat_a)} 非决定 {len(main_nondet)}", flush=True)

    conflict_pats = {}
    for sd in (77, 211, 331, 777, 555):
        rng = random.Random(sd)
        pat2 = defaultdict(set)
        t0 = time.time()
        for _ in range(5000):
            omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
            full = tuple(sg_block(omega, zbar, a, b) for a, b in factors)
            pat = tuple(full[i] for i in base_idx)
            pat2[pat].add(round(A_BG(n, omega, zbar), 6))
        bad = 0
        for p, vals in pat2.items():
            if len(vals) > 1:
                bad += 1
                conflict_pats[p] = sorted(vals)
            elif p in pat_a and not vals <= pat_a[p]:
                bad += 1
        print(f"seed {sd}: 冲突 {bad} ({time.time()-t0:.0f}s)", flush=True)

    print(f"跨集冲突模式数: {len(conflict_pats)}", flush=True)

    missing = defaultdict(int)
    for p, vals in conflict_pats.items():
        rng = random.Random(991 + len(missing))
        pair = None
        seen = []
        for _ in range(30000):
            omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
            full = tuple(sg_block(omega, zbar, a, b) for a, b in factors)
            pp = tuple(full[i] for i in base_idx)
            if pp != p:
                continue
            bg = round(A_BG(n, omega, zbar), 6)
            for prev_full, prev_bg in seen:
                if abs(prev_bg - bg) > 1e-6:
                    pair = (prev_full, full)
                    break
            if pair:
                break
            seen.append((full, bg))
            if len(seen) > 3:
                seen.pop(0)
        if pair:
            f1, f2 = pair
            for i, nm in enumerate(NAMES):
                if abs(f1[i] - f2[i]) > 1e-9:
                    missing[nm] += 1
    print("缺失因子候选（覆盖冲突模式数降序）:", flush=True)
    top = sorted(missing.items(), key=lambda kv: -kv[1])[:25]
    for nm, c in top:
        print(f"  {nm}: {c}", flush=True)

    res = {"n": n, "base_size": len(base_idx), "base_set": base_names,
           "main_samples": 15000, "main_nondet": len(main_nondet),
           "conflict_pats": len(conflict_pats),
           "missing_candidates_top": [nm for nm, _ in top],
           "missing_counts": {nm: c for nm, c in top}}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_conflict_capture.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print(f"DONE ({time.time()-t_start:.0f}s) -> paperX_n11_conflict_capture.json")
