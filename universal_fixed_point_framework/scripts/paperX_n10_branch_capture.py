# -*- coding: utf-8 -*-
"""M2 补充：主样本分支捕获——重跑 seed 131 主样本 40000（扩到 200000），
捕获 4 个冲突投影在主样本中的所有出现样本（几何 + A_BG），定位"主表分支"代表点。
若某投影在主样本出现多次且 A_BG 多值 → 模式内多值直接实证（无需跨集）。
"""
import json, os, random, sys, time
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_block
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_n10_criterion import adj_partition_factors


def factor_name(a, b):
    def s(t):
        return "".join(str(x + 1) for x in t)
    return "s" + s(a) + "_" + s(b)


if __name__ == "__main__":
    with open(os.path.join(SCRIPT_DIR, "paperX_n10_conflict_vectors.json"), encoding="utf-8") as f:
        cv = json.load(f)
    factors = adj_partition_factors(10)
    NAMES = [factor_name(a, b) for a, b in factors]
    base_names = cv["base"]
    idx = [NAMES.index(x) for x in base_names]
    targets = [tuple(p["pattern"]) for p in cv["conflict_patterns"]]

    def pattern_on(omega, zbar):
        return tuple(sg_block(omega, zbar, factors[i][0], factors[i][1]) for i in idx)

    n_samples = 200000
    rng = random.Random(131)
    hits = defaultdict(list)
    t0 = time.time()
    for k in range(n_samples):
        omega, zbar, _ = gen_partial_collinear(10, 0, r1=True, momentum=True, rng=rng)
        pat = pattern_on(omega, zbar)
        if pat in targets:
            hits[pat].append({"sample": k, "bg": round(A_BG(10, omega, zbar), 6),
                              "omega": omega, "zbar": zbar})
    print(f"{n_samples} 样本 {time.time()-t0:.0f}s: 命中 {sum(len(v) for v in hits.values())}", flush=True)
    out = {}
    for ti, pat in enumerate(targets):
        hs = hits.get(pat, [])
        vals = {}
        for h in hs:
            vals.setdefault(h["bg"], []).append(h["sample"])
        out[ti] = {"main": cv["conflict_patterns"][ti]["main"], "hits": len(hs),
                   "vals": {str(k): v for k, v in vals.items()},
                   "samples": hs[:20]}
        print(f"target {ti}: hits={len(hs)} vals={ {k: v for k, v in vals.items()} }", flush=True)
    with open(os.path.join(SCRIPT_DIR, "paperX_n10_branch_capture.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("DONE")
