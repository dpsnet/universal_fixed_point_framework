# -*- coding: utf-8 -*-
"""n=11 M12：45 因子跨集审计（5 seed × 20000，与 n≤10 同口径）
- 读 45 基座（paperX_n11_core_descent.json combo_min_set）
- 5 seed（77/211/331/777/555）× 20000 采样——每缓存测 45 非决定 + 唯一率
- 全 0 非决定 → 阶数规律反转确认
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


def nondet_count(patterns, idx):
    pat_a = defaultdict(set)
    for full, a in patterns:
        pat = tuple(full[i] for i in idx)
        pat_a[pat].add(a)
    return sum(1 for v in pat_a.values() if len(v) > 1)


if __name__ == "__main__":
    n = 11
    t_start = time.time()
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    cd = json.load(open(SCRIPT_DIR + "/paperX_n11_core_descent.json", encoding="utf-8"))
    b45 = [NAMES.index(x) for x in cd["combo_min_set"]]
    print(f"审计基座：45 因子（{len(b45)}）", flush=True)

    seeds = [77, 211, 331, 777, 555]
    per = {}
    all_pass = True
    for sd in seeds:
        rng = random.Random(sd)
        data = []
        for _ in range(20000):
            omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
            full = tuple(sg_block(omega, zbar, a, b) for a, b in factors)
            data.append((full, round(A_BG(n, omega, zbar), 6)))
        nd = nondet_count(data, b45)
        uniq = len(set(tuple(f[i] for i in b45) for f, _ in data))
        per[str(sd)] = {"nondet": nd, "unique": uniq, "rate": round(uniq / 20000, 4)}
        if nd > 0:
            all_pass = False
        print(f"seed {sd}: 非决定 {nd} 唯一率 {uniq/20000:.3f} ({time.time()-t_start:.0f}s)", flush=True)

    res = {"n": n, "basis_size": len(b45), "seeds": seeds, "samples_per_seed": 20000,
           "per_seed": per, "crossset_pass": all_pass,
           "order_reversal_confirmed": all_pass,
           "elapsed_s": round(time.time() - t_start, 1)}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_crossset_audit45.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print(f"DONE ({time.time()-t_start:.0f}s) -> paperX_n11_crossset_audit45.json")
