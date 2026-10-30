# -*- coding: utf-8 -*-
"""M60b：括号值层线性秩跨 n 标度（numpy）
- n=8..12 各 50 样本——矩阵秩（220/n 因子 × n zbar 系数）
- 检验秩标度（预期 ~n-1？）
"""
import os, sys, json, random
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_n11_domain_audit import adj_partition_factors
from paperX_degenerate_family_scan import gen_partial_collinear

if __name__ == "__main__":
    results = {}
    for n in (8, 9, 10, 11, 12):
        factors = adj_partition_factors(n)
        ranks = []
        rng = random.Random(20261008 + n)
        for _ in range(50):
            omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
            M = np.zeros((len(factors), n))
            for k, (a, b) in enumerate(factors):
                SA = sum(omega[x] for x in a)
                SB = sum(omega[y] for y in b)
                for i in range(n):
                    c = 0.0
                    if i in a:
                        c += SB
                    if i in b:
                        c -= SA
                    M[k, i] = omega[i] * c
            ranks.append(np.linalg.matrix_rank(M, tol=1e-8))
        results[str(n)] = {"rank_min": int(min(ranks)), "rank_max": int(max(ranks)),
                           "n_minus_1": n - 1, "n_minus_2": n - 2}
        print(f"n={n}: 秩 {min(ranks)}-{max(ranks)}（n-1={n-1}、n-2={n-2}）", flush=True)

    json.dump(results, open(os.path.join(SCRIPT_DIR, "paperX_n_m60b_rankscale.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("DONE -> paperX_n_m60b_rankscale.json", flush=True)
