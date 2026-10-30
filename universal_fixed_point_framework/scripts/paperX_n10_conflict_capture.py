# -*- coding: utf-8 -*-
"""M1：捕获 n=10 独立复核（seed 77/211）中 4 个冲突模式的完整 49 维因子投影 + 几何参数
- 主样本 40000（seed 131）建判定表值集合
- 独立复核逐样本比对：投影 p ∈ 主表 且 round(A_BG,6) ∉ 主表值 → 冲突实例（存投影/主值/独立值/omega/zbar/seed）
- 输出 paperX_n10_conflict_vectors.json
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


def pattern_on(omega, zbar, factors, idx):
    return tuple(sg_block(omega, zbar, factors[i][0], factors[i][1]) for i in idx)


if __name__ == "__main__":
    # 基座：final_base（49 因子，与 verify2 v2 一致）
    with open(os.path.join(SCRIPT_DIR, "paperX_n10_final_base.json"), encoding="utf-8") as f:
        fb = json.load(f)
    base_names = fb["base"]
    factors = adj_partition_factors(10)
    NAMES = [factor_name(a, b) for a, b in factors]
    idx = [NAMES.index(x) for x in base_names]
    print(f"基座 {len(idx)} 因子", flush=True)

    # 主样本 40000：值集合（判定表）
    rng = random.Random(131)
    pat_a = defaultdict(set)
    t0 = time.time()
    for _ in range(40000):
        omega, zbar, _ = gen_partial_collinear(10, 0, r1=True, momentum=True, rng=rng)
        pat = pattern_on(omega, zbar, factors, idx)
        pat_a[pat].add(round(A_BG(10, omega, zbar), 6))
    print(f"主样本 40000 ({time.time()-t0:.0f}s): 模式 {len(pat_a)}", flush=True)

    # 独立复核 seed 77/211：捕获冲突实例（投影 + 主值 + 独立值 + 几何）
    conflicts = []
    for seed in (77, 211):
        rng = random.Random(seed)
        t0 = time.time()
        bad = 0
        for k in range(15000):
            omega, zbar, cps = gen_partial_collinear(10, 0, r1=True, momentum=True, rng=rng)
            pat = pattern_on(omega, zbar, factors, idx)
            v = round(A_BG(10, omega, zbar), 6)
            if pat in pat_a and v not in pat_a[pat]:
                bad += 1
                conflicts.append({
                    "seed": seed, "sample": k, "main": list(pat_a[pat])[0],
                    "indep": v, "pattern": [int(x) for x in pat],
                    "omega": [round(float(w), 12) for w in omega],
                    "zbar": [round(float(z), 12) for z in zbar],
                    "collinear_pairs": [[int(a), int(b)] for a, b in cps],
                })
        print(f"seed {seed}: 冲突 {bad} ({time.time()-t0:.0f}s)", flush=True)

    # 冲突模式去重汇总
    seen = {}
    for c in conflicts:
        key = tuple(c["pattern"])
        seen.setdefault(key, {"main": c["main"], "indep": {}, "instances": 0})
        seen[key]["instances"] += 1
        seen[key]["indep"].setdefault(c["indep"], []).append([c["seed"], c["sample"]])
    out = {"base": base_names, "base_size": len(idx), "conflicts_total": len(conflicts),
           "conflict_patterns": [{"pattern": [int(x) for x in k], "main": v["main"],
                                  "indep": {str(vi): inst for vi, inst in v["indep"].items()},
                                  "instances": v["instances"]} for k, v in seen.items()],
           "detail": conflicts}
    with open(os.path.join(SCRIPT_DIR, "paperX_n10_conflict_vectors.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"冲突实例 {len(conflicts)}, 去重模式 {len(seen)} -> paperX_n10_conflict_vectors.json")
    print("DONE")
