# -*- coding: utf-8 -*-
"""140 基座暴露速率实验（Phase 77 登记①）：饱和性验证
- 140 因子近似闭合基座（48 + 92 补因子）
- seed 131 累积采样 20000 → 40000 → 80000
- 对照：38 基座暴露曲线（2/4/20/79/243 @5000..80000）
- 判定：若 80000 样本仍 0 非决定 → 140 为强跨集闭合（升格）；若暴露 → 近似闭合确认 + 结构保证强化
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
    ac = json.load(open(SCRIPT_DIR + "/paperX_n11_approx_closed.json", encoding="utf-8"))
    base_names = ac["base_set"] if "base_set" in ac else None
    # approx_closed.json 无 base_set 字段（只有 extra_set）——从 crossset_greedy 取 base
    cg = json.load(open(SCRIPT_DIR + "/paperX_n11_crossset_greedy.json", encoding="utf-8"))
    closed_names = cg["remove_set"] + ac["extra_set"]
    closed_idx = [NAMES.index(x) for x in closed_names]
    print(f"n=11 140 基座（{len(closed_idx)} 因子）暴露速率实验", flush=True)

    stages = [20000, 40000, 80000]
    rng = random.Random(131)
    pat_a = defaultdict(set)
    last = 0
    curve = []
    for target in stages:
        t0 = time.time()
        for _ in range(target - last):
            omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
            full = tuple(sg_block(omega, zbar, a, b) for a, b in factors)
            pat = tuple(full[i] for i in closed_idx)
            pat_a[pat].add(round(A_BG(n, omega, zbar), 6))
        last = target
        nondet = [p for p in pat_a if len(pat_a[p]) > 1]
        curve.append({"samples": target, "unique_pats": len(pat_a), "nondet": len(nondet)})
        print(f"样本 {target}: 模式 {len(pat_a)} 非决定 {len(nondet)} ({time.time()-t0:.0f}s)", flush=True)

    final_nondet = curve[-1]["nondet"]
    print(f"结论: 80000 样本非决定 {final_nondet} -> {'强跨集闭合（饱和）' if final_nondet == 0 else '近似闭合确认（未饱和）'}", flush=True)

    res = {"n": n, "base_type": "approx_140", "base_size": len(closed_idx),
           "seed": 131, "curve": curve,
           "saturated": final_nondet == 0,
           "elapsed_s": round(time.time() - t_start, 1)}
    with open(os.path.join(SCRIPT_DIR, "paperX_n11_140_exposure.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print(f"DONE ({time.time()-t_start:.0f}s) -> paperX_n11_140_exposure.json")
