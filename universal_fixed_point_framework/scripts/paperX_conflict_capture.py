# -*- coding: utf-8 -*-
"""通用冲突捕获：n=8/9 基座跨集冲突模式投影（含主表回溯对比）
用法：python paperX_conflict_capture.py 8 [9]
输出：paperX_n{n}_conflict_capture.json
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


def get_basis(n):
    base = "E:/workspace/hyper-resolution/universal_fixed_point_framework/scripts/"
    if n == 9:
        d = json.load(open(base + "paperX_n9_final_summary.json", encoding="utf-8"))
        return list(d["base"])
    if n == 8:
        d = json.load(open(base + "paperX_n8_final_summary.json", encoding="utf-8"))
        return list(d["basis"])
    raise ValueError(n)


if __name__ == "__main__":
    args = [x for x in sys.argv[1:]]
    ns = [int(x) for x in args if x.lstrip('-').isdigit()]
    extra_all = [x for x in args if not x.lstrip('-').isdigit()]
    for n in ns or [8]:
        basis = list(dict.fromkeys(get_basis(n) + extra_all))
        factors = adj_partition_factors(n)
        NAMES = [factor_name(a, b) for a, b in factors]
        idx = [NAMES.index(x) for x in basis]
        print(f"n={n} 基座 {len(idx)}/{len(factors)}", flush=True)

        # 主表：pat -> bg（0 非决定确认）
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

        # 跨集冲突记录
        conf = defaultdict(list)
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
                is_conf = (p in main and not bgs <= {main[p]}) or (p not in main and len(bgs) > 1)
                if is_conf:
                    conf[p].extend(recs2[p])
            print(f"seed {sd} 冲突捕获 ({time.time()-t0:.0f}s)", flush=True)

        # 回溯主表：重扫 40000 收集冲突 pat 的主表投影
        conf_pats = set(conf.keys())
        main_proj = defaultdict(set)
        if conf_pats:
            rng = random.Random(131)
            t0 = time.time()
            for _ in range(40000):
                omega, zbar, _ = gen_partial_collinear(n, 0, r1=True, momentum=True, rng=rng)
                pat = tuple(sg_block(omega, zbar, factors[i][0], factors[i][1]) for i in idx)
                if pat in conf_pats:
                    main_proj[pat].add(tuple(sg_block(omega, zbar, factors[k][0], factors[k][1]) for k in range(len(factors))))
            print(f"主表回溯 {time.time()-t0:.0f}s", flush=True)

        # 区分因子 = 主表投影 ∪ 跨集投影（不同 bg）间有变化的非基座因子
        out = []
        for p, recs in conf.items():
            bgs = sorted(set(x[0] for x in recs))
            mbg = main.get(p)
            groups = defaultdict(set)
            for bg, proj in recs:
                groups[bg].add(proj)
            allprojs = set(main_proj.get(p, set()))
            for proj in groups.values():
                allprojs |= proj
            diff = []
            for k in range(len(factors)):
                if k in idx:
                    continue
                vals = set()
                for pr in allprojs:
                    vals.add(pr[k])
                if len(vals) > 1:
                    diff.append(NAMES[k])
            out.append({"pat": "".join(str(x) for x in p), "main_bg": mbg,
                        "seeds_bg": bgs, "n_main_projs": len(main_proj.get(p, set())),
                        "n_seed_records": len(recs),
                        "varying": diff, "n_varying": len(diff)})
            print(f"pat {''.join(str(x) for x in p)}: main_bg={mbg} seeds_bg={bgs} "
                  f"主表投影 {len(main_proj.get(p, set()))} 跨集 {len(recs)} 变化 {len(diff)} -> {diff[:8]}", flush=True)
        with open(os.path.join(SCRIPT_DIR, f"paperX_n{n}_conflict_capture.json"), "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        print(f"n={n} DONE {len(out)}", flush=True)
