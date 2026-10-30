# -*- coding: utf-8 -*-
"""模式空间增长对照实验（采样代表性理论，登记②第一步）：
各阶贪心基座（minbasis 级）在统一采样规模 20000（seed 131）下的：
- 唯一模式数 / 唯一率（模式空间稀疏度随 n）
- 基座非决定数（贪心基座质量随 n）
- 单样本耗时
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


def load_base(n):
    f = {6: "paperX_n6_minbasis_results.json", 7: "paperX_n7_minbasis_results.json",
         8: "paperX_n8_minbasis_results.json", 9: "paperX_n9_minbasis_results.json",
         10: "paperX_n10_minbasis_results.json", 11: "paperX_n11_minbasis_results.json"}[n]
    j = json.load(open(SCRIPT_DIR + "/" + f, encoding="utf-8"))
    return j["remove_set"]


if __name__ == "__main__":
    NS = 20000
    SEED = 131
    rows = []
    for n in (6, 7, 8, 9, 10, 11):
        if n == 6:
            from paperX_n6_fullbasis import sg_pattern6_full
            NAMES6 = ["s1_23","s12_3","s123_4","s56","s23","s1_234","s12_34","s34",
                      "s2_34","s23_4","s12","s345_6","s45_6","s45","s3_45","s34_5",
                      "s234_5","s61","s2_345","s23_45"]
            base_names = load_base(6)
            base_idx = [NAMES6.index(x) for x in base_names]
            def full_vec(omega, zbar):
                return tuple(sg_pattern6_full(omega, zbar))
        else:
            factors = adj_partition_factors(n)
            NAMES = [factor_name(a, b) for a, b in factors]
            base_names = load_base(n)
            base_idx = [NAMES.index(x) for x in base_names]
            def full_vec(omega, zbar, factors=factors):
                return tuple(sg_block(omega, zbar, a, b) for a, b in factors)
        rng = random.Random(SEED)
        pat_cnt = defaultdict(int)
        pat_a = defaultdict(set)
        t0 = time.time()
        for _ in range(NS):
            omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
            full = full_vec(omega, zbar)
            pat = tuple(full[i] for i in base_idx)
            pat_cnt[pat] += 1
            pat_a[pat].add(round(A_BG(n, omega, zbar), 6))
        dt = time.time() - t0
        uniq = len(pat_cnt)
        nondet = sum(1 for v in pat_a.values() if len(v) > 1)
        ftot = 20 if n == 6 else len(factors)
        rows.append({"n": n, "base_size": len(base_idx), "samples": NS,
                     "unique_pats": uniq, "unique_rate": round(uniq / NS, 4),
                     "nondet": nondet, "secs": round(dt, 1),
                     "ms_per_sample": round(dt / NS * 1000, 2),
                     "factors_total": ftot})
        print(f"n={n}: 基座 {len(base_idx)} 模式 {uniq}/{NS} 唯一率 {uniq/NS:.3f} 非决定 {nondet} ({dt:.0f}s)", flush=True)

    with open(SCRIPT_DIR + "/paperX_mode_space_growth.json", "w", encoding="utf-8") as f:
        json.dump({"samples": NS, "seed": SEED, "rows": rows}, f, ensure_ascii=False, indent=2)
    print("DONE -> paperX_mode_space_growth.json")
