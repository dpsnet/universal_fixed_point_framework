# -*- coding: utf-8 -*-
"""Phase 75 推进：n=9 补因子随机游走 flip 检测（区分者强度谱最细端复核）
- 对 11 个补因子逐一检测：38 因子基座去掉该因子 → 37 因子投影下随机游走同模式跳变（bg 变投影不变）计数 = flip
- 与 n=10 s2_3/s3_4（flip=14/8）同标准可比
- 起点：冲突 pat 样本几何（27 因子版跨集冲突）
输出：paperX_n9_walk_flips.json
"""
import json, os, random, sys, time
from collections import defaultdict, Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_block
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_n10_criterion import adj_partition_factors

EXTRA = ["s12_3456", "s1234_56789", "s123456_789", "s12345678_9",
         "s1_23456", "s123_456", "s1234567_89", "s23_45", "s2_345678",
         "s23456_789", "s456_789"]


def factor_name(a, b):
    def s(t):
        return "".join(str(x + 1) for x in t)
    return "s" + s(a) + "_" + s(b)


if __name__ == "__main__":
    n = 9
    base = "E:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/"
    d = json.load(open(base + "paperX_n9_final_summary.json", encoding="utf-8"))
    basis0 = list(d["base"])
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    idx0 = [NAMES.index(x) for x in basis0]
    ex_idx = [NAMES.index(x) for x in EXTRA]
    full_idx = idx0 + ex_idx
    print(f"n=9 基座 {len(full_idx)} (27+11)", flush=True)

    # 1) 找冲突 pat 样本几何（27 因子版：跨集同 pat 多值）
    pat27_idx = idx0
    conf_geo = []
    pat_set = defaultdict(list)
    for sd in (77, 211, 331, 777, 555):
        rng = random.Random(sd)
        for _ in range(15000):
            omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
            pat = tuple(sg_block(omega, zbar, factors[i][0], factors[i][1]) for i in pat27_idx)
            pat_set[pat].append((round(A_BG(n, omega, zbar), 6), omega, zbar))
    # 主表 pat → bg
    main_bg = {}
    rng = random.Random(131)
    pa = defaultdict(set)
    for _ in range(40000):
        omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
        pat = tuple(sg_block(omega, zbar, factors[i][0], factors[i][1]) for i in pat27_idx)
        pa[pat].add(round(A_BG(n, omega, zbar), 6))
    for p, v in pa.items():
        main_bg[p] = list(v)[0]
    seen = set()
    for p, recs in pat_set.items():
        if p in main_bg:
            if not {x[0] for x in recs} <= {main_bg[p]}:
                if p not in seen:
                    conf_geo.append((recs[0][1], recs[0][2]))  # 一个冲突样本几何
                    seen.add(p)
        elif len({x[0] for x in recs}) > 1:
            if p not in seen:
                conf_geo.append((recs[0][1], recs[0][2]))
                seen.add(p)
    print(f"冲突 pat 样本 {len(conf_geo)}（几何起点）", flush=True)

    # 2) 逐补因子 flip：随机游走检测"去该因子后投影不变 bg 变"
    results = []
    for ei, ef in enumerate(EXTRA):
        drop_idx = full_idx[:]
        drop_idx.remove(ex_idx[ei])
        drop_idx.sort()
        di_set = set(drop_idx)

        def pat_drop(omega, zbar):
            return tuple(sg_block(omega, zbar, factors[k][0], factors[k][1]) for k in di_set)

        flips = 0
        t0 = time.time()
        for si, (omega0, zbar0) in enumerate(conf_geo):
            rng = random.Random(9000 + ei * 100 + si)
            prev = None
            for k in range(40000):
                w = [omega0[a] * (1.0 + rng.uniform(-0.3, 0.3)) for a in range(n - 1)]
                w.append(-sum(w))
                if w[n - 1] >= 0:
                    continue
                z = [zbar0[i] + rng.uniform(-0.9, 0.9) for i in range(n - 1)]
                s = sum(w[:n - 1])
                z.append(sum(w[i] * z[i] for i in range(n - 1)) / s)
                pat = pat_drop(w, z)
                bg = round(A_BG(n, w, z), 6)
                if prev is not None:
                    pbg, ppat = prev
                    if abs(bg - pbg) > 1e-9 and pat == ppat:
                        flips += 1
                prev = (bg, pat)
        print(f"{ef}: flip={flips} ({time.time()-t0:.0f}s)", flush=True)
        results.append({"factor": ef, "flip": flips})

    with open(os.path.join(SCRIPT_DIR, "paperX_n9_walk_flips.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("DONE")
