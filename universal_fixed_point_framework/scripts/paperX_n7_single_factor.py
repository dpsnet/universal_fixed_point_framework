# -*- coding: utf-8 -*-
"""n=7 单因子非零率平坦性检验（对照 n=6：各因子分支非零率≈0.18 平坦）。
若平坦 → n=7 无单因子非零判据（与 n=6 低阶负结果一致，阶数增长持续性证据）
"""
import json, os, random, sys, time
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_n7_criterion import adj_partition_factors, sg_pattern7
from paperX_n7_minbasis import factor_name

N7 = 7


def run(n_samples=20000, seed=13):
    factors = adj_partition_factors(N7)
    with open(os.path.join(SCRIPT_DIR, "paperX_n7_minbasis_results.json"), encoding="utf-8") as f:
        res = json.load(f)
    names = [factor_name(a, b) for a, b in factors]
    idx = [names.index(x) for x in res["remove_set"]]
    basis = res["remove_set"]

    rng = random.Random(seed)
    # 每因子每分支：非零样本数 / 样本数
    cnt = defaultdict(int)
    nz = defaultdict(int)
    t0 = time.time()
    for _ in range(n_samples):
        omega, zbar, _ = gen_partial_collinear(N7, 0, r1=True, momentum=True, rng=rng)
        full = sg_pattern7(omega, zbar, factors)
        a = round(A_BG(N7, omega, zbar), 6)
        for i in range(len(idx)):
            key = (basis[i], full[idx[i]])
            cnt[key] += 1
            if abs(a) > 1e-9:
                nz[key] += 1
    print(f"样本 {n_samples} ({time.time()-t0:.0f}s) — 单因子分支非零率:")
    rates = []
    for name in basis:
        r_p = nz.get((name, 1), 0) / max(cnt.get((name, 1), 1), 1)
        r_n = nz.get((name, -1), 0) / max(cnt.get((name, -1), 1), 1)
        rates.append((name, r_p, r_n))
        print(f"  {name:12s}  +1: {r_p:.3f} ({cnt.get((name,1),0)})   -1: {r_n:.3f} ({cnt.get((name,-1),0)})")
    flat = all(abs(a - b) < 0.03 for _, a, b in rates) and max(a for _, a, b in rates) - min(b for _, a, b in rates) < 0.15
    print(f"平坦性: {'✅ 平坦（无单因子判据）' if flat else '⚠ 非平坦（存在单因子倾向）'}")
    res_out = {"samples": n_samples, "rates": {n: [round(a, 4), round(b, 4)] for n, a, b in rates}}
    with open(os.path.join(SCRIPT_DIR, "paperX_n7_single_factor_results.json"), "w", encoding="utf-8") as f:
        json.dump(res_out, f, ensure_ascii=False, indent=2)
    print("DONE")


if __name__ == "__main__":
    run()
