# -*- coding: utf-8 -*-
"""n=9 冲突模式捕获：记录冲突样本的 (pat, bg) + 全 120 因子投影
对每个冲突 pat：对比不同 bg 组的投影差异 → 缺失因子候选（随 bg 变化的因子）
输出：paperX_n9_conflict_capture.json
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
    n = 9
    base = "E:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/"
    d = json.load(open(base + "paperX_n9_final_summary.json", encoding="utf-8"))
    basis = list(d["base"])
    factors = adj_partition_factors(n)
    NAMES = [factor_name(a, b) for a, b in factors]
    idx = [NAMES.index(x) for x in basis]
    print(f"n=9 基座 {len(idx)}/120", flush=True)

    # 主表
    rng = random.Random(131)
    main = {}
    pat_a = defaultdict(set)
    for _ in range(40000):
        omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
        pat = tuple(sg_block(omega, zbar, factors[i][0], factors[i][1]) for i in idx)
        pat_a[pat].add(round(A_BG(n, omega, zbar), 6))
    for p, v in pat_a.items():
        main[p] = list(v)[0]
    print(f"主表 {len(main)} 模式 0 非决定", flush=True)

    # 冲突样本捕获（5 seed 全部）：只记录真正冲突（同 pat 不同 bg）
    # 类型1：pat 在主表但 bg 与主表不同（跨集推翻主表）
    # 类型2：pat 不在主表但跨集内同 pat 多 bg（新模式内部非决定）
    conf = defaultdict(list)  # pat -> [(bg, fullproj)]
    for sd in (331, 777, 555, 77, 211):
        rng = random.Random(sd)
        pat2 = defaultdict(set)
        recs2 = defaultdict(list)
        t0 = time.time()
        for _ in range(15000):
            omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
            pat = tuple(sg_block(omega, zbar, factors[i][0], factors[i][1]) for i in idx)
            bg = round(A_BG(n, omega, zbar), 6)
            pat2[pat].add(bg)
            recs2[pat].append((bg, tuple(sg_block(omega, zbar, factors[k][0], factors[k][1]) for k in range(len(factors)))))
        for p, bgs in pat2.items():
            is_conf = False
            if p in main and not bgs <= {main[p]}:
                is_conf = True  # 类型1：推翻主表
            elif p not in main and len(bgs) > 1:
                is_conf = True  # 类型2：新模式内部非决定
            if is_conf:
                conf[p].extend(recs2[p])
        print(f"seed {sd} 冲突捕获 ({time.time()-t0:.0f}s)", flush=True)

    # 汇总：每个冲突 pat 的 bg 值分布 + 主表 bg
    out = []
    for p, recs in conf.items():
        bgs = sorted(set(x[0] for x in recs))
        mbg = main.get(p)
        # 非基座因子：哪个在该 pat 的不同 bg 间有变化
        diff = []
        bg_groups = defaultdict(set)
        for bg, proj in recs:
            bg_groups[bg].add(proj)
        for k in range(len(factors)):
            if k in idx:
                continue
            vals = set()
            for proj in bg_groups.values():
                for pr in proj:
                    vals.add(pr[k])
            if len(vals) > 1:
                diff.append(NAMES[k])
        out.append({"pat": "".join(str(x) for x in p), "main_bg": mbg,
                    "seeds_bg": bgs, "n_records": len(recs),
                    "varying_nonbasis": diff[:30], "n_varying": len(diff)})
        print(f"pat {''.join(str(x) for x in p)}: main_bg={mbg} seeds_bg={bgs} 变化因子 {len(diff)} -> {diff[:10]}", flush=True)

    with open(os.path.join(SCRIPT_DIR, "paperX_n9_conflict_capture.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("DONE", len(out))
