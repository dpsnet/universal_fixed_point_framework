# -*- coding: utf-8 -*-
"""Phase 75 对照：n=8 代表补因子 flip（s1_2345678）——强度谱单调性对照
- 8 因子基座 23 + s1_2345678 删除后 = 22+7？不——38 类似：23+8 补因子，去 s1_2345678 = 30 因子
- 随机游走 5 冲突起点 × 20000 步，检测"去 s1_2345678 后同模式跳变"
"""
import json, os, random, sys, time
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from paperX_single_minus_numerics import sg_block
from paperX_single_minus_bg_recursion import A_BG
from paperX_degenerate_family_scan import gen_partial_collinear
from paperX_n10_criterion import adj_partition_factors

EXTRA8 = ["s1_23456", "s1_2345678", "s12_345678", "s123_45678", "s12345_678",
           "s1234567_8", "s23456_78", "s1234_56"]


def factor_name(a, b):
    def s(t):
        return "".join(str(x + 1) for x in t)
    return "s" + s(a) + "_" + s(b)


if __name__ == "__main__":
    n = 8
    tgt = "s1_2345678"
    base = "E:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/"
    d = json.load(open(base + "paperX_n8_final_summary.json", encoding="utf-8"))
    basis0 = list(d["basis"])
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    idx0 = [NAMES.index(x) for x in basis0]
    ex_idx = [NAMES.index(x) for x in EXTRA8]
    drop_idx = sorted(set(idx0 + ex_idx) - {NAMES.index(tgt)})
    print(f"n=8 基座去 {tgt}: {len(drop_idx)} 因子", flush=True)

    # 冲突起点（23 因子版跨集冲突）
    pat_set = defaultdict(list)
    for sd in (77, 211, 331, 777, 555):
        rng = random.Random(sd)
        for _ in range(15000):
            omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
            pat = tuple(sg_block(omega, zbar, factors[i][0], factors[i][1]) for i in idx0)
            pat_set[pat].append((round(A_BG(n, omega, zbar), 6), omega, zbar))
    main_bg = {}
    rng = random.Random(131)
    pa = defaultdict(set)
    for _ in range(40000):
        omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
        pat = tuple(sg_block(omega, zbar, factors[i][0], factors[i][1]) for i in idx0)
        pa[pat].add(round(A_BG(n, omega, zbar), 6))
    for p, v in pa.items():
        main_bg[p] = list(v)[0]
    conf_geo = []
    seen = set()
    for p, recs in pat_set.items():
        if (p in main_bg and not {x[0] for x in recs} <= {main_bg[p]}) or (p not in main_bg and len({x[0] for x in recs}) > 1):
            if p not in seen:
                conf_geo.append((recs[0][1], recs[0][2]))
                seen.add(p)
    print(f"冲突起点 {len(conf_geo)}", flush=True)

    flips = 0
    t0 = time.time()
    for si, (omega0, zbar0) in enumerate(conf_geo):
        rng = random.Random(8000 + si)
        prev = None
        for k in range(20000):
            w = [omega0[a] * (1.0 + rng.uniform(-0.3, 0.3)) for a in range(n - 1)]
            w.append(-sum(w))
            if w[n - 1] >= 0:
                continue
            z = [zbar0[i] + rng.uniform(-0.9, 0.9) for i in range(n - 1)]
            s = sum(w[:n - 1])
            z.append(sum(w[i] * z[i] for i in range(n - 1)) / s)
            pat = tuple(sg_block(omega, zbar, factors[k][0], factors[k][1]) for k in drop_idx)
            bg = round(A_BG(n, w, z), 6)
            if prev is not None:
                pbg, ppat = prev
                if abs(bg - pbg) > 1e-9 and pat == ppat:
                    flips += 1
            prev = (bg, pat)
    print(f"{tgt}: flip={flips} ({time.time()-t0:.0f}s)", flush=True)
    with open(os.path.join(SCRIPT_DIR, "paperX_n8_flip_s1_2345678.json"), "w", encoding="utf-8") as f:
        json.dump({"factor": tgt, "flip": flips, "steps": len(conf_geo) * 20000}, f, ensure_ascii=False, indent=2)
    print("DONE")
