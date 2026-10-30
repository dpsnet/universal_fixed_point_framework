# -*- coding: utf-8 -*-
"""n=11 记号完备性诊断：基座非决定模式 → 全集 220 因子能否区分？
若存在"基座非决定且全集也非决定"的模式 → n=11 相邻分割记号不完备（需扩展记号）
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
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    mb = json.load(open(SCRIPT_DIR + "/paperX_n11_minbasis_results.json", encoding="utf-8"))
    base_idx = [NAMES.index(x) for x in mb["remove_set"]]

    rng = random.Random(131)
    rec = defaultdict(list)   # 基座 pat -> [(full, bg)]
    t0 = time.time()
    for _ in range(20000):
        omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
        full = tuple(sg_block(omega, zbar, a, b) for a, b in factors)
        pat = tuple(full[i] for i in base_idx)
        bg = round(A_BG(n, omega, zbar), 6)
        if len(rec[pat]) < 6:
            rec[pat].append((full, bg))
    print(f"采样 20000 ({time.time()-t0:.0f}s)", flush=True)

    base_nondet = [p for p, rs in rec.items() if len(set(r[1] for r in rs)) > 1]
    print(f"基座非决定模式: {len(base_nondet)}", flush=True)

    full_nondet = 0
    full_distinguish = 0
    cases = []
    for p in base_nondet:
        rs = rec[p]
        fulls = [r[0] for r in rs]
        bgs = set(r[1] for r in rs)
        # 全集区分：同基座 pat 内，全集向量是否与 bg 一一对应（决定）
        full2bg = {}
        uniq = True
        for r in rs:
            f, bg = r
            if f in full2bg and full2bg[f] != bg:
                uniq = False
                break
            full2bg[f] = bg
        if uniq:
            full_distinguish += 1
        else:
            full_nondet += 1
            cases.append({"pat": None, "n": len(rs), "bgs": sorted(bgs),
                          "full2bg": {str(f): bg for f, bg in full2bg.items()}})
    print(f"全集可区分: {full_distinguish}  全集仍非决定: {full_nondet}", flush=True)
    for c in cases[:5]:
        print(f"  非决定样本数 {c['n']}  bg取值 {c['bgs']}  全集向量数 {len(c['full2bg'])}", flush=True)

    res = {"n": n, "samples": 20000, "base_nondet": len(base_nondet),
           "full_distinguish": full_distinguish, "full_nondet": full_nondet,
           "cases": cases}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_completeness_diag.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("DONE -> paperX_n11_completeness_diag.json")
